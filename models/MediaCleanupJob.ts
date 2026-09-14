import mongoose, { Schema, type Document } from "mongoose"

export type MediaCleanupStatus = "pending" | "processing" | "failed" | "completed" | "cancelled"

export interface IMediaCleanupJob extends Document {
  publicId: string
  url: string
  resourceType: "image"
  reason: string
  status: MediaCleanupStatus
  attempts: number
  lastError?: string
  processingStartedAt?: Date
  completedAt?: Date
  expiresAt?: Date
  createdAt: Date
  updatedAt: Date
}

const MediaCleanupJobSchema = new Schema<IMediaCleanupJob>(
  {
    publicId: { type: String, required: true, unique: true },
    url: { type: String, required: true },
    resourceType: { type: String, enum: ["image"], default: "image", required: true },
    reason: { type: String, required: true },
    status: {
      type: String,
      enum: ["pending", "processing", "failed", "completed", "cancelled"],
      default: "pending",
      required: true,
    },
    attempts: { type: Number, default: 0, required: true },
    lastError: { type: String },
    processingStartedAt: { type: Date },
    completedAt: { type: Date },
    expiresAt: { type: Date },
  },
  { timestamps: true },
)

MediaCleanupJobSchema.index({ status: 1, createdAt: 1 })
MediaCleanupJobSchema.index({ expiresAt: 1 }, { expireAfterSeconds: 0 })

export default mongoose.models.MediaCleanupJob ||
  mongoose.model<IMediaCleanupJob>("MediaCleanupJob", MediaCleanupJobSchema)
