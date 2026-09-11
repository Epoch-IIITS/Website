import { NextRequest, NextResponse } from "next/server"
import { getServerSession } from "next-auth"
import mongoose from "mongoose"
import { authOptions } from "@/lib/auth"
import connectDB from "@/lib/mongodb"
import GeneratedQRCode from "@/models/GeneratedQRCode"
import QRCodeScan from "@/models/QRCodeScan"

export async function DELETE(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
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
    let deleted = false
    await mongoose.connection.transaction(async transaction => {
      const qrCode = await GeneratedQRCode.findByIdAndDelete(id, { session: transaction })
      if (!qrCode) return
      await QRCodeScan.deleteMany({ qrCode: id }, { session: transaction })
      deleted = true
    })

    if (!deleted) {
      return NextResponse.json({ error: "This QR code has already been deleted" }, { status: 404 })
    }
    return NextResponse.json({ message: "QR code deleted" })
  } catch (error) {
    console.error("QR code deletion error:", error)
    return NextResponse.json({ error: "Unable to delete the QR code" }, { status: 500 })
  }
}
