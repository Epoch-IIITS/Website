import { NextResponse } from "next/server"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import { executeOnVps, EXECUTION_UNAVAILABLE, isRateLimited, rateLimitMessage } from "@/lib/learn/executor"
import { parseLearnRequest } from "@/lib/learn/request"

// Grading can wait in the executor queue before it runs; see lib/learn/executor.ts.
export const maxDuration = 60

// Server Run is the fallback for problems that cannot run in the browser; it needs an account so the
// executor can rate-limit each user.
export async function POST(request: Request) {
  const session = await getServerSession(authOptions)
  if (!session?.user?.id) return NextResponse.json({ error: "Sign in to run this problem." }, { status: 401 })
  const body = await parseLearnRequest(request)
  if (!body) return NextResponse.json({ error: "Invalid problem or code." }, { status: 400 })
  const result = await executeOnVps("run", body.slug, body.code, session.user.id)
  if (isRateLimited(result)) return NextResponse.json({ error: rateLimitMessage(result) }, { status: 429, headers: { "Retry-After": String(result.retryAfter) } })
  if (!result) return NextResponse.json({ error: EXECUTION_UNAVAILABLE }, { status: 503 })
  return NextResponse.json(result, { headers: { "Cache-Control": "no-store" } })
}
