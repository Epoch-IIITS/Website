import { NextRequest, NextResponse } from "next/server"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import connectDB from "@/lib/mongodb"
import ContactQuery from "@/models/ContactQuery"

export async function DELETE(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user || session.user.role !== "admin") {
      return NextResponse.json({ error: "Admin access required" }, { status: session ? 403 : 401 })
    }
    const { id } = await params
    if (!/^[a-f\d]{24}$/i.test(id)) {
      return NextResponse.json({ error: "Invalid query ID" }, { status: 400 })
    }
    await connectDB()
    const deleted = await ContactQuery.findByIdAndDelete(id)
    if (!deleted) {
      return NextResponse.json({ error: "This query has already been deleted" }, { status: 404 })
    }
    return NextResponse.json({ message: "Query deleted" })
  } catch {
    return NextResponse.json({ error: "Unable to delete the query. Please try again." }, { status: 500 })
  }
}
