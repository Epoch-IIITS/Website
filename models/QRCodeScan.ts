import mongoose from "mongoose"

const qrCodeScanSchema = new mongoose.Schema({
  qrCode: { type: mongoose.Schema.Types.ObjectId, ref: "GeneratedQRCode", required: true },
  fingerprintHash: { type: String, required: true, minlength: 64, maxlength: 64 },
  scanCount: { type: Number, min: 1, required: true },
  firstScannedAt: { type: Date, required: true },
  lastScannedAt: { type: Date, required: true },
}, { timestamps: true })

qrCodeScanSchema.index({ qrCode: 1, fingerprintHash: 1 }, { unique: true })
qrCodeScanSchema.index({ qrCode: 1, lastScannedAt: -1 })

export default mongoose.models.QRCodeScan
  || mongoose.model("QRCodeScan", qrCodeScanSchema)
