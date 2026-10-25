import "server-only"
import connectDB from "@/lib/mongodb"
import LearnSubmission from "@/models/LearnSubmission"
import User from "@/models/User"
import { problems } from "@/lib/learn/data"

// Institute emails look like name.l23@iiits.in; the two digits identify the batch.
const BATCH_EMAIL = /^[^@\s]+\.[a-z](\d{2})@iiits\.in$/i

export function emailBatch(email: string) {
  return BATCH_EMAIL.exec(email.trim())?.[1] ?? null
}

export type Learner = {
  id: string
  name: string
  email: string
  image: string | null
  batch: string | null
  completed: number
  lastSolvedAt: string
}

// Members with at least one passing submission, counting distinct problems that still exist.
export async function getLearners(batch?: string) {
  await connectDB()
  const slugs = problems.map((problem) => problem.slug)
  const rows = await LearnSubmission.aggregate<{ _id: unknown; slugs: string[]; lastSolvedAt: Date }>([
    { $match: { status: "passed", problemSlug: { $in: slugs } } },
    { $group: { _id: "$user", slugs: { $addToSet: "$problemSlug" }, lastSolvedAt: { $max: "$createdAt" } } },
  ])
  const users = await User.find({ _id: { $in: rows.map((row) => row._id) } }).select("name email image").lean() as { _id: { toString(): string }; name: string; email: string; image?: string }[]
  const byId = new Map(users.map((user) => [user._id.toString(), user]))
  const learners: Learner[] = []
  for (const row of rows) {
    const user = byId.get(String(row._id))
    if (!user) continue
    learners.push({
      id: user._id.toString(), name: user.name, email: user.email, image: user.image ?? null,
      batch: emailBatch(user.email), completed: row.slugs.length, lastSolvedAt: new Date(row.lastSolvedAt).toISOString(),
    })
  }
  const batches = [...new Set(learners.map((learner) => learner.batch).filter((value): value is string => value !== null))].sort()
  const shown = batch ? learners.filter((learner) => learner.batch === batch) : learners
  shown.sort((a, b) => b.completed - a.completed || a.name.localeCompare(b.name))
  return { learners: shown, batches, total: learners.length }
}
