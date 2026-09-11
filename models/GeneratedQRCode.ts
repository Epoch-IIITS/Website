import mongoose from "mongoose"

const generatedQRCodeSchema = new mongoose.Schema({
  name: { type: String, required: true, trim: true, maxlength: 100 },
  content: { type: String, required: true, trim: true, maxlength: 2000 },
  contentType: { type: String, enum: ["url", "text"], required: true },
  slug: { type: String, required: true, unique: true, index: true },
  trackingEnabled: { type: Boolean, required: true, default: false },
  foregroundColor: { type: String, required: true, default: "#0f172a" },
  backgroundColor: { type: String, required: true, default: "#ffffff" },
  size: { type: Number, enum: [256, 512, 1024], required: true, default: 512 },
  margin: { type: Number, min: 0, max: 8, required: true, default: 2 },
  errorCorrectionLevel: { type: String, enum: ["M", "H"], required: true, default: "M" },
  createdBy: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
}, { timestamps: true })

generatedQRCodeSchema.index({ createdAt: -1, _id: -1 })

export default mongoose.models.GeneratedQRCode
  || mongoose.model("GeneratedQRCode", generatedQRCodeSchema)
