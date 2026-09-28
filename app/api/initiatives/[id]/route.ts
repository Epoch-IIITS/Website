import { NextRequest, NextResponse } from "next/server"
import mongoose, { type ClientSession } from "mongoose"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import { runAuditedMutation, type AuditDraft } from "@/lib/audit-log"
import { attemptMediaCleanup, ensureMediaStorage, reconcileMediaUrls } from "@/lib/media-assets"
import User from "@/models/User"
import { Initiative, InitiativeBlock, InitiativeReply, InitiativeTask, InitiativeTaskComment } from "@/models/Initiative"
import { accessibleInitiative, initiativeActor, participantIds } from "@/lib/initiatives/access"
import { initiativeAction } from "@/lib/initiatives/validation"

type Context = { params: Promise<{ id: string }> }
class ActionError extends Error {
  constructor(message: string, public status: number) { super(message) }
}

export async function GET(_request: NextRequest, { params }: Context) {
  try {
    const actor = await initiativeActor()
    if (!actor) return NextResponse.json({ error: "Sign in required" }, { status: 401 })
    if (!actor.eligible) return NextResponse.json({ error: "Team membership required" }, { status: 403 })
    const initiative = await accessibleInitiative((await params).id, actor)
    if (!initiative) return NextResponse.json({ error: "Initiative not found" }, { status: 404 })
    const [tasks, comments, blocks, replies] = await Promise.all([
      InitiativeTask.find({ initiative: initiative._id }).populate("assignees", "name image").sort({ status: 1, dueAt: 1, createdAt: 1 }).lean(),
      InitiativeTaskComment.find({ initiative: initiative._id }).populate("createdBy", "name image").sort({ createdAt: 1 }).lean(),
      InitiativeBlock.find({ initiative: initiative._id }).populate("taggedUsers", "name image").sort({ createdAt: 1 }).lean(),
      InitiativeReply.find({ initiative: initiative._id }).populate("createdBy", "name image").sort({ createdAt: 1 }).lean(),
    ])
    await initiative.populate("participants", "name image")
    const initiativeData = initiative.toJSON()
    delete (initiativeData as typeof initiativeData & { description?: string }).description
    return NextResponse.json({ initiative: initiativeData, tasks: tasks.map(task => ({ ...task, status: task.status === "done" ? "done" : "todo" })), comments, blocks, replies, actor }, { headers: { "Cache-Control": "private, no-store" } })
  } catch (error) {
    console.error("Initiative load error:", error)
    return NextResponse.json({ error: "Unable to load initiative" }, { status: 500 })
  }
}

export async function PATCH(request: NextRequest, { params }: Context) {
  try {
    const actor = await initiativeActor()
    if (!actor) return NextResponse.json({ error: "Sign in required" }, { status: 401 })
    if (!actor.eligible) return NextResponse.json({ error: "Team membership required" }, { status: 403 })
    const actorId = actor.id
    const isAdmin = actor.admin
    const initiative = await accessibleInitiative((await params).id, actor)
    if (!initiative) return NextResponse.json({ error: "Initiative not found" }, { status: 404 })
    const parsed = initiativeAction.safeParse(await request.json())
    if (!parsed.success) return NextResponse.json({ error: parsed.error.issues[0]?.message || "Invalid change" }, { status: 400 })
    const input = parsed.data
    const adminAction = input.action === "details" || input.action === "participants" || input.action === "status"
    if (adminAction && !actor.admin) return NextResponse.json({ error: "Admin access required" }, { status: 403 })
    if (initiative.status === "completed" && input.action !== "status") {
      return NextResponse.json({ error: "Reopen this initiative before editing" }, { status: 409 })
    }
    const changesMedia = input.action === "block.create" || input.action === "block.update" || input.action === "block.delete"
    if (changesMedia) await ensureMediaStorage()
    const cleanupPublicIds = new Set<string>()
    const initiativeId = initiative._id
    async function perform(databaseSession: ClientSession): Promise<AuditDraft> {
      const initiative = await Initiative.findById(initiativeId).session(databaseSession)
      if (!initiative || (!isAdmin && !participantIds(initiative).includes(actorId))) throw new ActionError("Initiative not found", 404)
      if (initiative.status === "completed" && input.action !== "status") throw new ActionError("Reopen this initiative before editing", 409)
      const options = { session: databaseSession }
      const participants = participantIds(initiative)
      let entityType = "initiative"
      let entityId = String(initiative._id)
      let action: AuditDraft["action"] = "update"
      let summary = `Updated initiative “${initiative.title}”`
      if (input.action === "details") {
        initiative.$session(databaseSession || null)
        initiative.title = input.title
        await initiative.save(options)
      } else if (input.action === "participants") {
        const selected = [...new Set([...input.participants, initiative.createdBy.toString()])]
        const count = await User.countDocuments({ _id: { $in: selected } }).session(databaseSession || null)
        if (count !== selected.length) throw new ActionError("Choose existing accounts as participants", 400)
        const removed = participants.filter(id => !selected.includes(id))
        initiative.$session(databaseSession || null)
        initiative.participants = selected.map(id => new mongoose.Types.ObjectId(id))
        await initiative.save(options)
        if (removed.length) {
          await InitiativeTask.updateMany({ initiative: initiative._id }, { $pull: { assignees: { $in: removed } } }, options)
          await InitiativeBlock.updateMany({ initiative: initiative._id }, { $pull: { taggedUsers: { $in: removed } } }, options)
        }
        summary = `Updated participants for initiative “${initiative.title}”`
      } else if (input.action === "status") {
        initiative.$session(databaseSession || null)
        initiative.status = input.status
        initiative.completedAt = input.status === "completed" ? new Date() : undefined
        await initiative.save(options)
        summary = `${input.status === "completed" ? "Archived" : "Reopened"} initiative “${initiative.title}”`
      } else {
        const assigned = "assignees" in input ? input.assignees : "taggedUsers" in input ? input.taggedUsers : "mentions" in input ? input.mentions : []
        if (assigned.some(id => !participants.includes(id))) throw new ActionError("Tags and assignees must be initiative participants", 400)
        if (input.action === "task.create") {
          const [task] = await InitiativeTask.create([{ initiative: initiative._id, title: input.title, description: input.description, dueAt: input.dueAt ? new Date(input.dueAt) : undefined, assignees: input.assignees, createdBy: actorId }], options)
          entityType = "initiative_task"; entityId = String(task._id); action = "create"; summary = `Created a task in “${initiative.title}”`
        } else if (input.action === "task.update") {
          const updated = await InitiativeTask.findOneAndUpdate({ _id: input.id, initiative: initiative._id }, { $set: { title: input.title, description: input.description, dueAt: input.dueAt ? new Date(input.dueAt) : null, assignees: input.assignees } }, { ...options, returnDocument: "after", runValidators: true })
          if (!updated) throw new ActionError("Task not found", 404)
          entityType = "initiative_task"; entityId = input.id; summary = `Updated a task in “${initiative.title}”`
        } else if (input.action === "task.status") {
          const updated = await InitiativeTask.findOneAndUpdate({ _id: input.id, initiative: initiative._id }, { $set: { status: input.status } }, { ...options, returnDocument: "after", runValidators: true })
          if (!updated) throw new ActionError("Task not found", 404)
          entityType = "initiative_task"; entityId = input.id; summary = `Marked a task as ${input.status === "done" ? "done" : "to do"} in “${initiative.title}”`
        } else if (input.action === "task.delete") {
          const task = await InitiativeTask.findOne({ _id: input.id, initiative: initiative._id }).session(databaseSession || null)
          if (!task) throw new ActionError("Task not found", 404)
          if (!isAdmin && String(task.createdBy) !== actorId) throw new ActionError("Only the task creator or an admin can delete it", 403)
          await InitiativeTaskComment.deleteMany({ initiative: initiative._id, task: input.id }, options)
          await InitiativeTask.deleteOne({ _id: input.id, initiative: initiative._id }, options)
          entityType = "initiative_task"; entityId = input.id; action = "delete"; summary = `Deleted a task from “${initiative.title}”`
        } else if (input.action === "task.comment.create") {
          const task = await InitiativeTask.exists({ _id: input.taskId, initiative: initiative._id }).session(databaseSession || null)
          if (!task) throw new ActionError("Task not found", 404)
          const [comment] = await InitiativeTaskComment.create([{ initiative: initiative._id, task: input.taskId, body: input.body, mentions: input.mentions, createdBy: actorId }], options)
          entityType = "initiative_task_comment"; entityId = String(comment._id); action = "create"; summary = `Commented on a task in “${initiative.title}”`
        } else if (input.action === "block.create") {
          if (input.type === "question" && !input.content) throw new ActionError("Enter a question", 400)
          if (input.type === "reference" && !input.url) throw new ActionError("Enter a reference URL", 400)
          const [block] = await InitiativeBlock.create([{ initiative: initiative._id, ...input, createdBy: actorId }], options)
          if (databaseSession) await reconcileMediaUrls({ beforeUrls: [], afterUrls: [input.url], reason: `Added initiative block ${block._id}`, session: databaseSession })
          entityType = "initiative_block"; entityId = String(block._id); action = "create"; summary = `Added a ${input.type} card to “${initiative.title}”`
        } else if (input.action === "block.update") {
          const before = await InitiativeBlock.findOne({ _id: input.id, initiative: initiative._id }).session(databaseSession || null)
          if (!before) throw new ActionError("Card not found", 404)
          const updated = await InitiativeBlock.findOneAndUpdate({ _id: input.id, initiative: initiative._id, version: input.version }, { $set: { title: input.title, content: input.content, url: input.url, taggedUsers: input.taggedUsers, x: input.x, y: input.y, ...(input.width !== undefined ? { width: input.width } : {}), ...(input.height !== undefined ? { height: input.height } : {}) }, $inc: { version: 1 } }, { ...options, returnDocument: "after", runValidators: true })
          if (!updated) throw new ActionError("This card changed elsewhere. Reload before saving.", 409)
          if (databaseSession) {
            const queued = await reconcileMediaUrls({ beforeUrls: [before.url], afterUrls: [input.url], reason: `Updated initiative block ${input.id}`, session: databaseSession })
            queued.forEach(id => cleanupPublicIds.add(id))
          }
          entityType = "initiative_block"; entityId = input.id; summary = `Updated a canvas card in “${initiative.title}”`
        } else if (input.action === "block.delete") {
          const block = await InitiativeBlock.findOne({ _id: input.id, initiative: initiative._id }).session(databaseSession || null)
          if (!block) throw new ActionError("Card not found", 404)
          if (!isAdmin && String(block.createdBy) !== actorId) throw new ActionError("Only the card creator or an admin can delete it", 403)
          await InitiativeReply.deleteMany({ initiative: initiative._id, block: input.id }, options)
          await InitiativeBlock.deleteOne({ _id: input.id, initiative: initiative._id }, options)
          if (databaseSession) {
            const queued = await reconcileMediaUrls({ beforeUrls: [block.url], afterUrls: [], reason: `Deleted initiative block ${input.id}`, session: databaseSession })
            queued.forEach(id => cleanupPublicIds.add(id))
          }
          entityType = "initiative_block"; entityId = input.id; action = "delete"; summary = `Deleted a canvas card from “${initiative.title}”`
        } else if (input.action === "reply.create") {
          const question = await InitiativeBlock.exists({ _id: input.blockId, initiative: initiative._id, type: "question" }).session(databaseSession || null)
          if (!question) throw new ActionError("Question not found", 404)
          const [reply] = await InitiativeReply.create([{ initiative: initiative._id, block: input.blockId, body: input.body, createdBy: actorId }], options)
          entityType = "initiative_reply"; entityId = String(reply._id); action = "create"; summary = `Replied to a question in “${initiative.title}”`
        }
        await Initiative.updateOne({ _id: initiative._id }, { $set: { updatedAt: new Date() } }, options)
      }
      return { action, entityType, entityId, entityLabel: initiative.title, summary, changes: [] }
    }
    if (actor.admin) {
      const session = await getServerSession(authOptions)
      if (!session) return NextResponse.json({ error: "Sign in required" }, { status: 401 })
      await runAuditedMutation(session, request, async databaseSession => {
        const log = await perform(databaseSession)
        return { value: true, logs: [log] }
      })
    } else {
      await mongoose.connection.transaction(async databaseSession => { await perform(databaseSession) })
    }
    await attemptMediaCleanup([...cleanupPublicIds])
    return NextResponse.json({ ok: true })
  } catch (error) {
    if (error instanceof ActionError) return NextResponse.json({ error: error.message }, { status: error.status })
    console.error("Initiative update error:", error)
    return NextResponse.json({ error: "Unable to save change" }, { status: 500 })
  }
}

export async function DELETE(request: NextRequest, { params }: Context) {
  try {
    const actor = await initiativeActor()
    if (!actor) return NextResponse.json({ error: "Sign in required" }, { status: 401 })
    if (!actor.eligible) return NextResponse.json({ error: "Team membership required" }, { status: 403 })
    if (!actor.admin) return NextResponse.json({ error: "Admin access required" }, { status: 403 })
    const initiative = await accessibleInitiative((await params).id, actor)
    if (!initiative) return NextResponse.json({ error: "Initiative not found" }, { status: 404 })
    const session = await getServerSession(authOptions)
    if (!session) return NextResponse.json({ error: "Sign in required" }, { status: 401 })
    await ensureMediaStorage()
    const cleanupPublicIds = await runAuditedMutation(session, request, async databaseSession => {
      const current = await Initiative.findById(initiative._id).session(databaseSession)
      if (!current) throw new ActionError("Initiative not found", 404)
      const filter = { initiative: current._id }
      const blocks = await InitiativeBlock.find(filter).select("url").session(databaseSession).lean()
      const queued = await reconcileMediaUrls({ beforeUrls: blocks.map(block => block.url), afterUrls: [], reason: `Deleted initiative ${current._id}`, session: databaseSession })
      const tasks = await InitiativeTask.deleteMany(filter, { session: databaseSession })
      const comments = await InitiativeTaskComment.deleteMany(filter, { session: databaseSession })
      const cards = await InitiativeBlock.deleteMany(filter, { session: databaseSession })
      const replies = await InitiativeReply.deleteMany(filter, { session: databaseSession })
      await Initiative.deleteOne({ _id: current._id }, { session: databaseSession })
      return {
        value: queued,
        logs: [{
          action: "delete" as const,
          entityType: "initiative",
          entityId: String(current._id),
          entityLabel: current.title,
          summary: `Deleted initiative “${current.title}” and ${tasks.deletedCount} tasks, ${comments.deletedCount} comments, ${cards.deletedCount} canvas cards, and ${replies.deletedCount} replies`,
          changes: [],
        }],
      }
    })
    await attemptMediaCleanup(cleanupPublicIds)
    return NextResponse.json({ ok: true })
  } catch (error) {
    if (error instanceof ActionError) return NextResponse.json({ error: error.message }, { status: error.status })
    console.error("Initiative deletion error:", error)
    return NextResponse.json({ error: "Unable to delete initiative" }, { status: 500 })
  }
}
