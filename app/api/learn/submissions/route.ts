import { NextRequest, NextResponse } from "next/server"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import connectDB from "@/lib/mongodb"
import LearnSubmission from "@/models/LearnSubmission"
import { problemBySlug } from "@/lib/learn/data"

export async function GET(request: NextRequest) {
  const session = await getServerSession(authOptions)
  if (!session?.user?.id) return NextResponse.json({ error: "Sign in to view submissions." }, { status: 401 })
  const slug = request.nextUrl.searchParams.get("slug") ?? ""
  if (!problemBySlug(slug)) return NextResponse.json({ error: "Unknown problem." }, { status: 400 })
  try {
    await connectDB()
    const latest = await LearnSubmission.findOne({ user: session.user.id, problemSlug: slug }).select("code passed total status createdAt").sort({ createdAt: -1 }).lean() as { code: string; passed: number; total: number; status: string; createdAt: Date } | null
    return NextResponse.json({ latest }, { headers: { "Cache-Control": "private, no-store" } })
  } catch {
    return NextResponse.json({ error: "Unable to load your submission." }, { status: 500 })
  }
}
