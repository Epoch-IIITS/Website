import mongoose, { type ClientSession } from "mongoose"
import type { Session } from "next-auth"
import type { NextRequest } from "next/server"
import AuditLog, { type AuditAction, type IAuditChange } from "@/models/AuditLog"

type AuditScalar = string | number | boolean | null

export interface AuditDraft {
  action: AuditAction
  entityType: string
  entityId: string
  entityLabel: string
  summary: string
  changes?: IAuditChange[]
  sideEffects?: Record<string, string | number | boolean>
}

interface AuditedMutationResult<T> {
  value: T
  logs: AuditDraft[]
}

function addSixMonths(value: Date) {
  const result = new Date(value)
  const originalDay = result.getUTCDate()
  result.setUTCDate(1)
  result.setUTCMonth(result.getUTCMonth() + 6)
  const lastDay = new Date(Date.UTC(result.getUTCFullYear(), result.getUTCMonth() + 1, 0)).getUTCDate()
  result.setUTCDate(Math.min(originalDay, lastDay))
  return result
}

function routeFor(request: NextRequest) {
  try {
    return request.nextUrl.pathname
  } catch {
    return new URL(request.url).pathname
  }
}

function auditActor(session: Session) {
  return {
    id: String(session.user.id),
    name: String(session.user.name || "Administrator").slice(0, 150),
    email: String(session.user.email || "unknown").slice(0, 254),
    role: String(session.user.role || "admin").slice(0, 50),
  }
}

function plain(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== "object") return {}
  if ("toObject" in value && typeof value.toObject === "function") {
    return value.toObject() as Record<string, unknown>
  }
  return value as Record<string, unknown>
}

function auditValue(value: unknown): AuditScalar {
  if (value === undefined || value === null || value === "") return null
  if (value instanceof Date) return value.toISOString()
  if (typeof value === "string") return value.slice(0, 500)
  if (typeof value === "number" || typeof value === "boolean") return value
  if (value instanceof mongoose.Types.ObjectId) return value.toString()

  const serialized = JSON.stringify(value, (_key, nested) => {
    if (nested instanceof Date) return nested.toISOString()
    if (nested instanceof mongoose.Types.ObjectId) return nested.toString()
    return nested
  })
  return serialized?.slice(0, 500) || null
}

export function diffAuditFields(
  beforeValue: unknown,
  afterValue: unknown,
  fields: readonly string[],
): IAuditChange[] {
  const before = plain(beforeValue)
  const after = plain(afterValue)

  return fields.flatMap((field) => {
    const previous = auditValue(before[field])
    const next = auditValue(after[field])
    return previous === next ? [] : [{ field, before: previous, after: next }]
  })
}

export function countChange(field: string, before: unknown[], after: unknown[]): IAuditChange[] {
  return JSON.stringify(before) === JSON.stringify(after)
    ? []
    : [{ field, before: `${before.length} item${before.length === 1 ? "" : "s"}`, after: `${after.length} item${after.length === 1 ? "" : "s"}` }]
}

export function textContentChange(field: string, before: unknown, after: unknown): IAuditChange[] {
  const previous = typeof before === "string" ? before : ""
  const next = typeof after === "string" ? after : ""
  return previous === next
    ? []
    : [{
      field,
      before: previous ? `${previous.length} characters` : null,
      after: next ? `${next.length} characters` : null,
    }]
}

export async function runAuditedMutation<T>(
  session: Session,
  request: NextRequest,
  mutation: (databaseSession: ClientSession) => Promise<AuditedMutationResult<T>>,
): Promise<T> {
  await AuditLog.init()
  const operationId = crypto.randomUUID()

  return mongoose.connection.transaction(async (databaseSession) => {
    const result = await mutation(databaseSession)
    if (result.logs.length) {
      const createdAt = new Date()
      await AuditLog.create(
        result.logs.map((entry) => ({
          ...entry,
          operationId,
          entityLabel: entry.entityLabel.slice(0, 200),
          summary: entry.summary.slice(0, 500),
          actor: auditActor(session),
          changes: entry.changes || [],
          route: routeFor(request),
          method: request.method,
          createdAt,
          expiresAt: addSixMonths(createdAt),
        })),
        { session: databaseSession },
      )
    }
    return result.value
  })
}
