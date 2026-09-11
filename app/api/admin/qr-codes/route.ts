import { NextRequest, NextResponse } from "next/server"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import connectDB from "@/lib/mongodb"
import { qrCodeSchema } from "@/lib/validations"
import { createQRCodeSlug, getPublicOrigin, isHttpUrl } from "@/lib/qr-code"
import GeneratedQRCode from "@/models/GeneratedQRCode"
import QRCodeScan from "@/models/QRCodeScan"

function responseRecord(record: Record<string, any>, origin: string, analytics?: Record<string, any>) {
  const id = String(record._id)
  return {
    ...record,
    _id: id,
    imageUrl: `/api/admin/qr-codes/${id}/image`,
    trackedUrl: record.trackingEnabled ? `${origin}/q/${record.slug}` : null,
    analytics: {
      totalScans: analytics?.totalScans || 0,
      uniqueScans: analytics?.uniqueScans || 0,
      firstScannedAt: analytics?.firstScannedAt || null,
      lastScannedAt: analytics?.lastScannedAt || null,
    },
  }
}

async function requireAdmin() {
  const session = await getServerSession(authOptions)
  if (!session?.user || session.user.role !== "admin" || !session.user.id) return null
  return session
}

export async function GET(request: NextRequest) {
  try {
    const session = await requireAdmin()
    if (!session) return NextResponse.json({ error: "Admin access required" }, { status: 401 })

    await connectDB()
    const records = await GeneratedQRCode.find()
      .populate("createdBy", "name")
      .sort({ createdAt: -1, _id: -1 })
      .limit(100)
      .lean()

    const ids = records.map((record: any) => record._id)
    const scanTotals = ids.length ? await QRCodeScan.aggregate([
      { $match: { qrCode: { $in: ids } } },
      {
        $group: {
          _id: "$qrCode",
          totalScans: { $sum: "$scanCount" },
          uniqueScans: { $sum: 1 },
          firstScannedAt: { $min: "$firstScannedAt" },
          lastScannedAt: { $max: "$lastScannedAt" },
        },
      },
    ]) : []
    const analyticsById = new Map(scanTotals.map((item: any) => [String(item._id), item]))
    const origin = getPublicOrigin(request.nextUrl.origin)

    return NextResponse.json({
      qrCodes: records.map((record: any) => responseRecord(record, origin, analyticsById.get(String(record._id)))),
    }, { headers: { "Cache-Control": "no-store" } })
  } catch (error) {
    console.error("QR code list error:", error)
    return NextResponse.json({ error: "Unable to load QR codes" }, { status: 500 })
  }
}

export async function POST(request: NextRequest) {
  try {
    const session = await requireAdmin()
    if (!session) return NextResponse.json({ error: "Admin access required" }, { status: 401 })

    const parsed = qrCodeSchema.safeParse(await request.json())
    if (!parsed.success) {
      return NextResponse.json({ error: parsed.error.issues[0]?.message || "Invalid QR code details" }, { status: 400 })
    }

    const contentType = isHttpUrl(parsed.data.content) ? "url" : "text"
    if (parsed.data.trackingEnabled && contentType !== "url") {
      return NextResponse.json({ error: "Tracking is available only for http or https URLs" }, { status: 400 })
    }

    await connectDB()
    await GeneratedQRCode.init()

    let record
    for (let attempt = 0; attempt < 3; attempt += 1) {
      try {
        record = await GeneratedQRCode.create({
          ...parsed.data,
          contentType,
          slug: createQRCodeSlug(),
          createdBy: session.user.id,
        })
        break
      } catch (error: any) {
        if (error?.code !== 11000 || attempt === 2) throw error
      }
    }
    if (!record) throw new Error("Unable to allocate QR code identifier")

    const origin = getPublicOrigin(request.nextUrl.origin)
    return NextResponse.json({ qrCode: responseRecord(record.toObject(), origin) }, { status: 201 })
  } catch (error) {
    console.error("QR code creation error:", error)
    return NextResponse.json({ error: "Unable to create QR code" }, { status: 500 })
  }
}
