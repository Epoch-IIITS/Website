import { NextRequest, NextResponse } from "next/server"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import connectDB from "@/lib/mongodb"
import ContactQuery from "@/models/ContactQuery"

export async function GET(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user || session.user.role !== "admin") {
      return NextResponse.json({ error: "Admin access required" }, { status: session ? 403 : 401 })
    }
    const page = Number(request.nextUrl.searchParams.get("page") || "1")
    if (!Number.isSafeInteger(page) || page < 1 || page > 100000) {
      return NextResponse.json({ error: "Invalid page number" }, { status: 400 })
    }
    const limit = 20
    await connectDB()
    const [queries, total] = await Promise.all([
      ContactQuery.find().select("firstName lastName email subject message createdAt").sort({ createdAt: -1, _id: -1 }).skip((page - 1) * limit).limit(limit).lean(),
      ContactQuery.countDocuments(),
    ])
    return NextResponse.json({ queries, pagination: { page, total, pages: Math.ceil(total / limit) } }, { headers: { "Cache-Control": "no-store" } })
  } catch {
    return NextResponse.json({ error: "Unable to load contact queries" }, { status: 500 })
  }
}
