import "server-only"
import { createHmac } from "node:crypto"
import { z } from "zod"
import type { LearnExecutionResult } from "@/lib/learn/types"
import { packBySlug } from "@/lib/learn/pack"

export const EXECUTION_UNAVAILABLE = "Python execution is currently unavailable."
export const MAX_CODE_BYTES = 16000

const testResultSchema = z.object({ name: z.string().max(120), passed: z.boolean(), message: z.string().max(1000).optional() })
const responseSchema = z.object({
  passed: z.number().int().min(0),
  total: z.number().int().min(1),
  status: z.enum(["passed", "failed"]),
  tests: z.array(testResultSchema).max(20).optional(),
  output: z.string().max(4096).optional(),
  failed: z.array(z.string().regex(/^test_\w{1,100}$/)).max(100).optional(),
})

// The executor limits requests per client; this is how often a client may try again.
export type RateLimited = { rateLimited: true; retryAfter: number; inFlight: boolean }

export function isRateLimited(value: unknown): value is RateLimited {
  return typeof value === "object" && value !== null && (value as RateLimited).rateLimited === true
}

export function rateLimitMessage(limited: RateLimited) {
  return limited.inFlight
    ? "Your previous run is still being graded. Try again when it finishes."
    : `Too many requests. Try again in ${limited.retryAfter} s.`
}

const rateLimitSchema = z.object({ error: z.string().max(100), retryAfter: z.number().int().min(1).max(3600) })

export async function executeOnVps(mode: "run" | "submit", slug: string, code: string, userId: string): Promise<LearnExecutionResult | RateLimited | null> {
  const rawUrl = process.env.LEARN_EXECUTOR_URL
  const token = process.env.LEARN_EXECUTOR_TOKEN
  if (!rawUrl || !token) return null
  let url: URL
  try {
    url = new URL(rawUrl)
    if (url.protocol !== "https:" || url.username || url.password || url.search || url.hash) return null
    url.pathname = "/execute"
  } catch {
    return null
  }
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      // A keyed hash identifies the user to the executor's rate limiter without revealing the id.
      body: JSON.stringify({ mode, slug, code, client: createHmac("sha256", token).update(`learn-user:${userId}`).digest("hex") }),
      cache: "no-store",
      // The executor may queue a request for up to 30 s, then allow the job 30 s.
      signal: AbortSignal.timeout(58000),
    })
    if (response.status === 429) {
      const limited = rateLimitSchema.safeParse(await response.json())
      if (!limited.success) return null
      return { rateLimited: true, retryAfter: limited.data.retryAfter, inFlight: limited.data.error === "A request is already running" }
    }
    if (!response.ok) return null
    const parsed = responseSchema.safeParse(await response.json())
    if (!parsed.success) return null
    const result = parsed.data
    const pack = packBySlug(slug)
    const expected = mode === "run" ? pack?.visibleTests.length : pack?.testCount
    if (!pack || !expected || result.total !== expected || result.passed > result.total || (result.status === "passed") !== (result.passed === result.total)) return null
    if (mode === "submit") {
      // Names of failed checks (never their code), kept only when they agree with the counts.
      const failed = result.failed && result.failed.length === result.total - result.passed && new Set(result.failed).size === result.failed.length ? result.failed : undefined
      return { passed: result.passed, total: result.total, status: result.status, ...(failed?.length ? { failedTests: failed } : {}) }
    }
    const expectedNames = new Set(pack.visibleTests.map((test) => test.name))
    if (!result.tests || result.tests.length !== expected || result.tests.some((test) => !expectedNames.has(test.name))) return null
    return { passed: result.passed, total: result.total, status: result.status, tests: result.tests.map((test) => ({ name: test.name, passed: test.passed })) }
  } catch {
    return null
  }
}
