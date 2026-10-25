import { NextResponse } from "next/server"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import { getLearnProgress } from "@/lib/learn/progress"

export async function GET() {
  const session = await getServerSession(authOptions)
  if (!session?.user?.id) return NextResponse.json({ error: "Sign in to view your progress." }, { status: 401 })
  try {
    return NextResponse.json(await getLearnProgress(session.user.id), { headers: { "Cache-Control": "no-store" } })
  } catch {
    return NextResponse.json({ error: "Unable to load progress." }, { status: 500 })
  }
}
