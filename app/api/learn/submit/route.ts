import { NextResponse } from "next/server"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import connectDB from "@/lib/mongodb"
import LearnSubmission from "@/models/LearnSubmission"
import { executeOnVps, EXECUTION_UNAVAILABLE, isRateLimited, rateLimitMessage } from "@/lib/learn/executor"
import { parseLearnRequest } from "@/lib/learn/request"

// Grading can wait in the executor queue before it runs; see lib/learn/executor.ts.
export const maxDuration = 60

export async function POST(request: Request) {
  const session = await getServerSession(authOptions)
  if (!session?.user?.id) return NextResponse.json({ error: "Sign in to submit this problem." }, { status: 401 })
  const body = await parseLearnRequest(request)
  if (!body) return NextResponse.json({ error: "Invalid problem or code." }, { status: 400 })
  const result = await executeOnVps("submit", body.slug, body.code, session.user.id)
  if (isRateLimited(result)) return NextResponse.json({ error: rateLimitMessage(result) }, { status: 429, headers: { "Retry-After": String(result.retryAfter) } })
  if (!result) return NextResponse.json({ error: EXECUTION_UNAVAILABLE }, { status: 503 })
  try {
    await connectDB()
    const submission = await LearnSubmission.create({
      user: session.user.id,
      problemSlug: body.slug,
      code: body.code,
      passed: result.passed,
      total: result.total,
      status: result.status,
    })
    return NextResponse.json({ ...result, submissionId: submission._id.toString() }, { status: 201, headers: { "Cache-Control": "no-store" } })
  } catch {
    return NextResponse.json({ error: "Unable to save your submission. Please try again." }, { status: 500 })
  }
}
