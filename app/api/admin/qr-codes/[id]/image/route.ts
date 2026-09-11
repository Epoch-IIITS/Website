import { NextRequest, NextResponse } from "next/server"
import { getServerSession } from "next-auth"
import mongoose from "mongoose"
import QRCode from "qrcode"
import { authOptions } from "@/lib/auth"
import connectDB from "@/lib/mongodb"
import { getQRCodePayload } from "@/lib/qr-code"
import GeneratedQRCode from "@/models/GeneratedQRCode"

export async function GET(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user || session.user.role !== "admin") {
      return NextResponse.json({ error: "Admin access required" }, { status: session ? 403 : 401 })
    }

    const { id } = await params
    if (!mongoose.Types.ObjectId.isValid(id)) {
      return NextResponse.json({ error: "Invalid QR code ID" }, { status: 400 })
    }

    await connectDB()
    const record = await GeneratedQRCode.findById(id).lean()
    if (!record) return NextResponse.json({ error: "QR code not found" }, { status: 404 })

    const buffer = await QRCode.toBuffer(getQRCodePayload(record as any, request.nextUrl.origin), {
      type: "png",
      width: record.size,
      margin: record.margin,
      errorCorrectionLevel: record.errorCorrectionLevel,
      color: { dark: record.foregroundColor, light: record.backgroundColor },
    })
    const safeName = record.name.replace(/[^a-z0-9_-]+/gi, "-").replace(/^-|-$/g, "").slice(0, 80) || "qr-code"
    const download = request.nextUrl.searchParams.get("download") === "1"

    return new NextResponse(new Uint8Array(buffer), {
      headers: {
        "Content-Type": "image/png",
        "Content-Disposition": `${download ? "attachment" : "inline"}; filename="${safeName}.png"`,
        "Cache-Control": "private, no-store",
      },
    })
  } catch (error) {
    console.error("QR code image error:", error)
    return NextResponse.json({ error: "Unable to generate QR code image" }, { status: 500 })
  }
}
