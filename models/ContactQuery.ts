import mongoose from "mongoose"

const contactQuerySchema = new mongoose.Schema({
  firstName: { type: String, required: true, trim: true, maxlength: 80 },
  lastName: { type: String, required: true, trim: true, maxlength: 80 },
  email: { type: String, required: true, trim: true, lowercase: true, maxlength: 254 },
  subject: { type: String, required: true, trim: true, maxlength: 200 },
  message: { type: String, required: true, trim: true, maxlength: 5000 },
}, { timestamps: true })

contactQuerySchema.index({ createdAt: -1, _id: -1 })

export default mongoose.models.ContactQuery || mongoose.model("ContactQuery", contactQuerySchema)
