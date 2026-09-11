import mongoose, { Schema, type Document } from "mongoose"

export interface IRSVP extends Document {
  event: mongoose.Types.ObjectId
  user: mongoose.Types.ObjectId
  ticketId: string
  capacitySlot?: number
  createdAt: Date
  updatedAt: Date
}

const RSVPSchema = new Schema<IRSVP>(
  {
    event: {
      type: Schema.Types.ObjectId,
      ref: "Event",
      required: true,
    },
    user: {
      type: Schema.Types.ObjectId,
      ref: "User",
      required: true,
    },
    ticketId: {
      type: String,
      unique: true,
      required: true,
    },
    capacitySlot: {
      type: Number,
      min: 1,
    },
  },
  {
    timestamps: true,
  },
)

RSVPSchema.index({ event: 1, user: 1 }, { unique: true })
RSVPSchema.index(
  { event: 1, capacitySlot: 1 },
  { unique: true, partialFilterExpression: { capacitySlot: { $type: "number" } } },
)

export default mongoose.models.RSVP || mongoose.model<IRSVP>("RSVP", RSVPSchema)
