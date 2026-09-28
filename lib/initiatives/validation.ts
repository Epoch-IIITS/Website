import { z } from "zod"

const objectId = z.string().regex(/^[a-f\d]{24}$/i)
const users = z.array(objectId).max(100).default([])
const httpUrl = z.string().url().refine(value => {
  try {
    const protocol = new URL(value).protocol
    return protocol === "http:" || protocol === "https:"
  } catch {
    return false
  }
}, "Use an http or https link")

export const initiativeCreate = z.object({
  title: z.string().trim().min(1).max(120),
  participants: users,
})

export const initiativeAction = z.discriminatedUnion("action", [
  z.object({ action: z.literal("details"), title: z.string().trim().min(1).max(120) }),
  z.object({ action: z.literal("participants"), participants: users }),
  z.object({ action: z.literal("status"), status: z.enum(["active", "completed"]) }),
  z.object({ action: z.literal("task.create"), title: z.string().trim().min(1).max(160), description: z.string().trim().max(4000).default(""), dueAt: z.string().datetime().nullable().default(null), assignees: users }),
  z.object({ action: z.literal("task.update"), id: objectId, title: z.string().trim().min(1).max(160), description: z.string().trim().max(4000), dueAt: z.string().datetime().nullable(), assignees: users }),
  z.object({ action: z.literal("task.status"), id: objectId, status: z.enum(["todo", "done"]) }),
  z.object({ action: z.literal("task.delete"), id: objectId }),
  z.object({ action: z.literal("task.comment.create"), taskId: objectId, body: z.string().trim().min(1).max(4000), mentions: users }),
  z.object({ action: z.literal("block.create"), type: z.enum(["note", "question", "reference"]), title: z.string().trim().max(160), content: z.string().trim().max(10000), url: z.union([httpUrl, z.literal("")]).default(""), taggedUsers: users, x: z.number().finite().min(-1000000).max(1000000), y: z.number().finite().min(-1000000).max(1000000) }),
  z.object({ action: z.literal("block.update"), id: objectId, version: z.number().int().min(0), title: z.string().trim().max(160), content: z.string().trim().max(10000), url: z.union([httpUrl, z.literal("")]), taggedUsers: users, x: z.number().finite().min(-1000000).max(1000000), y: z.number().finite().min(-1000000).max(1000000), width: z.number().int().min(240).max(900).optional(), height: z.number().int().min(160).max(800).optional() }),
  z.object({ action: z.literal("block.delete"), id: objectId }),
  z.object({ action: z.literal("reply.create"), blockId: objectId, body: z.string().trim().min(1).max(4000) }),
])
