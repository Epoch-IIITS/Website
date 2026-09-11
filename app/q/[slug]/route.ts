import { NextRequest, NextResponse } from "next/server"
import connectDB from "@/lib/mongodb"
import { createScanFingerprint, isHttpUrl } from "@/lib/qr-code"
import GeneratedQRCode from "@/models/GeneratedQRCode"
import QRCodeScan from "@/models/QRCodeScan"

export const dynamic = "force-dynamic"

async function recordScan(qrCodeId: unknown, request: NextRequest) {
  const now = new Date()
  const fingerprintHash = createScanFingerprint(request.headers)
  await QRCodeScan.init()

  try {
    await QRCodeScan.updateOne(
      { qrCode: qrCodeId, fingerprintHash },
      {
        $inc: { scanCount: 1 },
        $set: { lastScannedAt: now },
        $setOnInsert: { firstScannedAt: now },
      },
      { upsert: true },
    )
  } catch (error: any) {
    // Concurrent first scans can race the unique index. Count the losing request
    // against the record created by the winner.
    if (error?.code !== 11000) throw error
    await QRCodeScan.updateOne(
      { qrCode: qrCodeId, fingerprintHash },
      { $inc: { scanCount: 1 }, $set: { lastScannedAt: now } },
    )
  }
}

export async function GET(request: NextRequest, { params }: { params: Promise<{ slug: string }> }) {
  try {
    const { slug } = await params
    if (!/^[A-Za-z0-9_-]{12}$/.test(slug)) {
      return NextResponse.json({ error: "Tracked QR code not found" }, { status: 404 })
    }

    await connectDB()
    const qrCode = await GeneratedQRCode.findOne({
      slug,
      trackingEnabled: true,
      contentType: "url",
    }).select("_id content").lean()

    if (!qrCode || !isHttpUrl(qrCode.content)) {
      return NextResponse.json({ error: "Tracked QR code not found" }, { status: 404 })
    }

    try {
      await recordScan(qrCode._id, request)
    } catch (error) {
      // A temporary analytics failure must not break the destination link.
      console.error("QR scan tracking error:", error)
    }

    return NextResponse.redirect(qrCode.content, 302)
  } catch (error) {
    console.error("Tracked QR redirect error:", error)
    return NextResponse.json({ error: "Unable to open this QR code" }, { status: 500 })
  }
}
