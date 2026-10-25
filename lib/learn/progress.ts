import "server-only"
import connectDB from "@/lib/mongodb"
import LearnSubmission from "@/models/LearnSubmission"
import { problems, requiredProblems, topics } from "@/lib/learn/data"

export async function getLearnProgress(userId: string) {
  await connectDB()
  const [accepted, latest, attempts] = await Promise.all([
    LearnSubmission.distinct("problemSlug", { user: userId, status: "passed" }) as Promise<string[]>,
    LearnSubmission.findOne({ user: userId }).select("problemSlug status createdAt").sort({ createdAt: -1 }).lean() as Promise<{ problemSlug: string; status: "passed" | "failed"; createdAt: Date } | null>,
    LearnSubmission.countDocuments({ user: userId }) as Promise<number>,
  ])
  // completedSlugs includes optional deep dives (for their marks); the counts use required steps only.
  const validSlugs = new Set(problems.map((problem) => problem.slug))
  const completedSlugs = [...new Set(accepted.filter((slug) => validSlugs.has(slug)))]
  const completed = new Set(completedSlugs)
  const required = requiredProblems.filter((problem) => completed.has(problem.slug))
  const byTopic = Object.fromEntries(topics.map((topic) => [topic.slug, required.filter((problem) => problem.topicSlug === topic.slug).length])) as Record<string, number>
  const topicsComplete = topics.filter((topic) => byTopic[topic.slug] === topic.problemCount).length
  const lastProblem = problems.find((problem) => problem.slug === latest?.problemSlug)
  const continueProblem = (latest?.status === "failed" ? lastProblem : undefined) ?? requiredProblems.find((problem) => !completed.has(problem.slug)) ?? lastProblem ?? problems[0]
  return { completedSlugs, completed: required.length, total: requiredProblems.length, topicsComplete, totalTopics: topics.length, byTopic, attempts, continueProblem: continueProblem ? { id: continueProblem.id, slug: continueProblem.slug, title: continueProblem.title, topicSlug: continueProblem.topicSlug } : null }
}
