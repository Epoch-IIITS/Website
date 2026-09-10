import { NextRequest, NextResponse } from "next/server"
import connectDB from "@/lib/mongodb"
import ContactQuery from "@/models/ContactQuery"
import { contactQuerySchema } from "@/lib/validations"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"

export async function POST(request: NextRequest) {
  let body: unknown
  try {
    body = await request.json()
  } catch {
    return NextResponse.json({ error: "Invalid message format" }, { status: 400 })
  }
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user?.email) {
      return NextResponse.json({ error: "Please log in to send a message" }, { status: 401 })
    }
    if (body && typeof body === "object" && !Array.isArray(body)) {
      body = { ...body, email: session.user.email }
    }
    const parsed = contactQuerySchema.safeParse(body)
    if (!parsed.success) {
      return NextResponse.json({ error: parsed.error.issues[0].message }, { status: 400 })
    }
    await connectDB()
    await ContactQuery.create(parsed.data)
    return NextResponse.json({ message: "Message received" }, { status: 201 })
  } catch {
    return NextResponse.json({ error: "Unable to send your message. Please try again." }, { status: 500 })
  }
}
