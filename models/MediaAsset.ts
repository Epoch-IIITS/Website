import mongoose, { Schema, type Document } from "mongoose"

export type MediaAssetStatus = "pending" | "attached" | "deletion_pending" | "deleted" | "failed"

export interface IMediaAsset extends Document {
  assetId?: string
  publicId: string
  url: string
  resourceType: "image"
  folder: string
  purpose?: string
  status: MediaAssetStatus
  source: "upload" | "legacy"
  uploadedBy?: string
  lastError?: string
  deletedAt?: Date
  expiresAt?: Date
  createdAt: Date
  updatedAt: Date
}

const MediaAssetSchema = new Schema<IMediaAsset>(
  {
    assetId: { type: String },
    publicId: { type: String, required: true, unique: true },
    url: { type: String, required: true },
    resourceType: { type: String, enum: ["image"], default: "image", required: true },
    folder: { type: String, required: true },
    purpose: { type: String },
    status: {
      type: String,
      enum: ["pending", "attached", "deletion_pending", "deleted", "failed"],
      default: "pending",
      required: true,
    },
    source: { type: String, enum: ["upload", "legacy"], default: "legacy", required: true },
    uploadedBy: { type: String },
    lastError: { type: String },
    deletedAt: { type: Date },
    expiresAt: { type: Date },
  },
  { timestamps: true },
)

MediaAssetSchema.index({ status: 1, createdAt: 1 })
MediaAssetSchema.index({ url: 1 })
MediaAssetSchema.index({ expiresAt: 1 }, { expireAfterSeconds: 0 })

export default mongoose.models.MediaAsset || mongoose.model<IMediaAsset>("MediaAsset", MediaAssetSchema)
