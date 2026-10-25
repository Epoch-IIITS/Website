import { z } from "zod"
import { MAX_CODE_BYTES } from "@/lib/learn/executor"
import { packBySlug } from "@/lib/learn/pack"

const bodySchema = z.object({ slug: z.string().min(1).max(100), code: z.string().min(1).max(MAX_CODE_BYTES) })

export async function parseLearnRequest(request: Request) {
  const length = Number(request.headers.get("content-length"))
  if (Number.isFinite(length) && length > MAX_CODE_BYTES * 2) return null
  try {
    const body = bodySchema.safeParse(await request.json())
    if (!body.success || Buffer.byteLength(body.data.code, "utf8") > MAX_CODE_BYTES || !packBySlug(body.data.slug)) return null
    return body.data
  } catch {
    return null
  }
}
