import mongoose, { Schema, type Document } from "mongoose"

export interface IInitiative extends Document {
  title: string
  status: "active" | "completed"
  participants: mongoose.Types.ObjectId[]
  createdBy: mongoose.Types.ObjectId
  completedAt?: Date
  createdAt: Date
  updatedAt: Date
}

const initiativeSchema = new Schema<IInitiative>({
  title: { type: String, required: true, trim: true },
  status: { type: String, enum: ["active", "completed"], default: "active" },
  participants: [{ type: Schema.Types.ObjectId, ref: "User" }],
  createdBy: { type: Schema.Types.ObjectId, ref: "User", required: true },
  completedAt: Date,
}, { timestamps: true })
initiativeSchema.index({ status: 1, updatedAt: -1 })
initiativeSchema.index({ participants: 1, status: 1 })

export interface IInitiativeTask extends Document {
  initiative: mongoose.Types.ObjectId
  title: string
  description: string
  dueAt?: Date
  assignees: mongoose.Types.ObjectId[]
  status: "todo" | "done"
  createdBy: mongoose.Types.ObjectId
  createdAt: Date
  updatedAt: Date
}

const taskSchema = new Schema<IInitiativeTask>({
  initiative: { type: Schema.Types.ObjectId, ref: "Initiative", required: true },
  title: { type: String, required: true, trim: true },
  description: { type: String, default: "" },
  dueAt: Date,
  assignees: [{ type: Schema.Types.ObjectId, ref: "User" }],
  status: { type: String, enum: ["todo", "done"], default: "todo" },
  createdBy: { type: Schema.Types.ObjectId, ref: "User", required: true },
}, { timestamps: true })
taskSchema.index({ initiative: 1, status: 1, dueAt: 1 })

export interface IInitiativeBlock extends Document {
  initiative: mongoose.Types.ObjectId
  type: "note" | "question" | "reference"
  title: string
  content: string
  url: string
  taggedUsers: mongoose.Types.ObjectId[]
  x: number
  y: number
  width?: number
  height?: number
  version: number
  createdBy: mongoose.Types.ObjectId
  createdAt: Date
  updatedAt: Date
}

const blockSchema = new Schema<IInitiativeBlock>({
  initiative: { type: Schema.Types.ObjectId, ref: "Initiative", required: true },
  type: { type: String, enum: ["note", "question", "reference"], required: true },
  title: { type: String, default: "" },
  content: { type: String, default: "" },
  url: { type: String, default: "" },
  taggedUsers: [{ type: Schema.Types.ObjectId, ref: "User" }],
  x: { type: Number, default: 0 },
  y: { type: Number, default: 0 },
  width: { type: Number, min: 240, max: 900 },
  height: { type: Number, min: 160, max: 800 },
  version: { type: Number, default: 0 },
  createdBy: { type: Schema.Types.ObjectId, ref: "User", required: true },
}, { timestamps: true })
blockSchema.index({ initiative: 1, createdAt: 1 })

export interface IInitiativeReply extends Document {
  initiative: mongoose.Types.ObjectId
  block: mongoose.Types.ObjectId
  body: string
  createdBy: mongoose.Types.ObjectId
  createdAt: Date
}

const replySchema = new Schema<IInitiativeReply>({
  initiative: { type: Schema.Types.ObjectId, ref: "Initiative", required: true },
  block: { type: Schema.Types.ObjectId, ref: "InitiativeBlock", required: true },
  body: { type: String, required: true },
  createdBy: { type: Schema.Types.ObjectId, ref: "User", required: true },
}, { timestamps: true })
replySchema.index({ initiative: 1, block: 1, createdAt: 1 })

export interface IInitiativeTaskComment extends Document {
  initiative: mongoose.Types.ObjectId
  task: mongoose.Types.ObjectId
  body: string
  mentions: mongoose.Types.ObjectId[]
  createdBy: mongoose.Types.ObjectId
  createdAt: Date
}

const taskCommentSchema = new Schema<IInitiativeTaskComment>({
  initiative: { type: Schema.Types.ObjectId, ref: "Initiative", required: true },
  task: { type: Schema.Types.ObjectId, ref: "InitiativeTask", required: true },
  body: { type: String, required: true },
  mentions: [{ type: Schema.Types.ObjectId, ref: "User" }],
  createdBy: { type: Schema.Types.ObjectId, ref: "User", required: true },
}, { timestamps: true })
taskCommentSchema.index({ initiative: 1, task: 1, createdAt: 1 })

export const Initiative = mongoose.models.Initiative || mongoose.model<IInitiative>("Initiative", initiativeSchema)
export const InitiativeTask = mongoose.models.InitiativeTask || mongoose.model<IInitiativeTask>("InitiativeTask", taskSchema)
export const InitiativeBlock = mongoose.models.InitiativeBlock || mongoose.model<IInitiativeBlock>("InitiativeBlock", blockSchema)
export const InitiativeReply = mongoose.models.InitiativeReply || mongoose.model<IInitiativeReply>("InitiativeReply", replySchema)
export const InitiativeTaskComment = mongoose.models.InitiativeTaskComment || mongoose.model<IInitiativeTaskComment>("InitiativeTaskComment", taskCommentSchema)
