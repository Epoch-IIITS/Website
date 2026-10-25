import { type NextRequest, NextResponse } from "next/server"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import { getLearners } from "@/lib/learn/learners"

// Admin-only list of members who have passed at least one Learn problem, optionally for one batch.
export async function GET(request: NextRequest) {
  const session = await getServerSession(authOptions)
  if (!session?.user || session.user.role !== "admin") return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
  const batch = request.nextUrl.searchParams.get("batch") ?? ""
  if (batch && !/^\d{2}$/.test(batch)) return NextResponse.json({ error: "Batch must be two digits." }, { status: 400 })
  try {
    return NextResponse.json(await getLearners(batch || undefined), { headers: { "Cache-Control": "private, no-store" } })
  } catch {
    return NextResponse.json({ error: "Unable to load learners." }, { status: 500 })
  }
}
