import mongoose, { Schema, type Document } from "mongoose"

export type AuditAction = "create" | "update" | "delete"

export interface IAuditChange {
  field: string
  before: string | number | boolean | null
  after: string | number | boolean | null
}

export interface IAuditLog extends Document {
  operationId: string
  action: AuditAction
  entityType: string
  entityId: string
  entityLabel: string
  actor: {
    id: string
    name: string
    email: string
    role: string
  }
  summary: string
  changes: IAuditChange[]
  sideEffects?: Record<string, string | number | boolean>
  route: string
  method: string
  createdAt: Date
  expiresAt: Date
}

const auditChangeSchema = new Schema<IAuditChange>(
  {
    field: { type: String, required: true, maxlength: 100 },
    before: { type: Schema.Types.Mixed, default: null },
    after: { type: Schema.Types.Mixed, default: null },
  },
  { _id: false },
)

const auditLogSchema = new Schema<IAuditLog>(
  {
    operationId: { type: String, required: true, index: true },
    action: { type: String, enum: ["create", "update", "delete"], required: true },
    entityType: { type: String, required: true, maxlength: 80 },
    entityId: { type: String, required: true, maxlength: 100 },
    entityLabel: { type: String, required: true, maxlength: 200 },
    actor: {
      _id: false,
      id: { type: String, required: true, maxlength: 100 },
      name: { type: String, required: true, maxlength: 150 },
      email: { type: String, required: true, maxlength: 254 },
      role: { type: String, required: true, maxlength: 50 },
    },
    summary: { type: String, required: true, maxlength: 500 },
    changes: { type: [auditChangeSchema], default: [] },
    sideEffects: { type: Schema.Types.Mixed },
    route: { type: String, required: true, maxlength: 300 },
    method: { type: String, required: true, maxlength: 10 },
    createdAt: { type: Date, required: true },
    expiresAt: { type: Date, required: true },
  },
  { versionKey: false },
)

auditLogSchema.index({ createdAt: -1, _id: -1 })
auditLogSchema.index({ action: 1, createdAt: -1 })
auditLogSchema.index({ entityType: 1, createdAt: -1 })
auditLogSchema.index({ "actor.id": 1, createdAt: -1 })
auditLogSchema.index({ expiresAt: 1 }, { expireAfterSeconds: 0 })

export default mongoose.models.AuditLog
  || mongoose.model<IAuditLog>("AuditLog", auditLogSchema)
