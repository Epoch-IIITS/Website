import { NextRequest, NextResponse } from "next/server"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import { runAuditedMutation } from "@/lib/audit-log"
import User from "@/models/User"
import { Initiative, InitiativeBlock, InitiativeReply, InitiativeTask } from "@/models/Initiative"
import { initiativeActor } from "@/lib/initiatives/access"
import { initiativeCreate } from "@/lib/initiatives/validation"

export async function GET() {
  try {
    const actor = await initiativeActor()
    if (!actor) return NextResponse.json({ error: "Sign in required" }, { status: 401 })
    if (!actor.eligible) return NextResponse.json({ error: "Team membership required" }, { status: 403 })
    const filter = actor.admin ? {} : { participants: actor.id }
    const initiatives = await Initiative.find(filter)
      .select("-description")
      .populate("participants", "name image")
      .sort({ status: 1, updatedAt: -1 })
      .lean()
    const ids = initiatives.map(item => item._id)
    const [tasks, questions, answered] = await Promise.all([
      InitiativeTask.find({ initiative: { $in: ids } }).select("initiative title status dueAt").lean(),
      InitiativeBlock.find({ initiative: { $in: ids }, type: "question" }).select("_id initiative title content").lean(),
      InitiativeReply.distinct("block", { initiative: { $in: ids } }),
    ])
    const answeredIds = new Set(answered.map(String))
    const now = Date.now()
    return NextResponse.json(initiatives.map(item => {
      const ownTasks = tasks.filter(task => String(task.initiative) === String(item._id))
      const pending = ownTasks.filter(task => task.status !== "done")
      const openQuestions = questions.filter(question => String(question.initiative) === String(item._id) && !answeredIds.has(String(question._id)))
      return {
        ...item,
        pendingTasks: pending.length,
        overdueTasks: pending.filter(task => task.dueAt && new Date(task.dueAt).getTime() < now).length,
        nextTasks: pending.sort((a, b) => (a.dueAt ? new Date(a.dueAt).getTime() : Infinity) - (b.dueAt ? new Date(b.dueAt).getTime() : Infinity)).slice(0, 3).map(task => ({ title: task.title, dueAt: task.dueAt })),
        unansweredQuestions: openQuestions.length,
        firstOpenQuestion: openQuestions[0]?.title || openQuestions[0]?.content,
      }
    }), { headers: { "Cache-Control": "private, no-store" } })
  } catch (error) {
    console.error("Initiatives list error:", error)
    return NextResponse.json({ error: "Unable to load initiatives" }, { status: 500 })
  }
}

export async function POST(request: NextRequest) {
  try {
    const actor = await initiativeActor()
    if (!actor) return NextResponse.json({ error: "Sign in required" }, { status: 401 })
    if (!actor.eligible) return NextResponse.json({ error: "Team membership required" }, { status: 403 })
    if (!actor.admin) return NextResponse.json({ error: "Admin access required" }, { status: 403 })
    const parsed = initiativeCreate.safeParse(await request.json())
    if (!parsed.success) return NextResponse.json({ error: parsed.error.issues[0]?.message || "Invalid initiative" }, { status: 400 })
    const participants = [...new Set([...parsed.data.participants, actor.id])]
    const count = await User.countDocuments({ _id: { $in: participants } })
    if (count !== participants.length) return NextResponse.json({ error: "Choose existing accounts as participants" }, { status: 400 })
    const session = await getServerSession(authOptions)
    if (!session) return NextResponse.json({ error: "Sign in required" }, { status: 401 })
    const initiative = await runAuditedMutation(session, request, async databaseSession => {
      const [created] = await Initiative.create([{ ...parsed.data, participants, createdBy: actor.id }], { session: databaseSession })
      return {
        value: created,
        logs: [{
          action: "create",
          entityType: "initiative",
          entityId: String(created._id),
          entityLabel: created.title,
          summary: `Created initiative “${created.title}”`,
          changes: [],
        }],
      }
    })
    return NextResponse.json(initiative, { status: 201 })
  } catch (error) {
    console.error("Initiative creation error:", error)
    return NextResponse.json({ error: "Unable to create initiative" }, { status: 500 })
  }
}
