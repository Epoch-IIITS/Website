import mongoose, { Schema, type Document } from "mongoose"

export interface ILearnSubmission extends Document {
  user: mongoose.Types.ObjectId
  problemSlug: string
  code: string
  passed: number
  total: number
  status: "passed" | "failed"
  createdAt: Date
}

const LearnSubmissionSchema = new Schema<ILearnSubmission>({
  user: { type: Schema.Types.ObjectId, ref: "User", required: true, index: true },
  problemSlug: { type: String, required: true, index: true },
  code: { type: String, required: true, maxlength: 16000 },
  passed: { type: Number, required: true, min: 0 },
  total: { type: Number, required: true, min: 1 },
  status: { type: String, enum: ["passed", "failed"], required: true },
}, { timestamps: { createdAt: true, updatedAt: false } })

LearnSubmissionSchema.index({ user: 1, problemSlug: 1, createdAt: -1 })

export default mongoose.models.LearnSubmission || mongoose.model<ILearnSubmission>("LearnSubmission", LearnSubmissionSchema)
