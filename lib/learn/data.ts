import catalogue from "@/lib/learn/catalogue.generated.json"
import type { LearnProblem, LearnProject, LearnTopic, PathItem } from "@/lib/learn/types"

export const topics = catalogue.topics as LearnTopic[]
export const problems = catalogue.problems as LearnProblem[]
export const projects = catalogue.projects as LearnProject[]
// Steps that count towards completion: every graded step except optional deep dives.
export const requiredProblems = problems.filter((problem) => !problem.optional)

export function topicBySlug(slug: string) {
  return topics.find((topic) => topic.slug === slug)
}

export function problemBySlug(slug: string) {
  return problems.find((problem) => problem.slug === slug)
}

export function projectBySlug(slug: string) {
  return projects.find((project) => project.slug === slug)
}

export function topicProblems(slug: string) {
  return problems.filter((problem) => problem.topicSlug === slug)
}

export function topicProjects(slug: string) {
  return projects.filter((project) => project.topicSlug === slug)
}

// A topic's graded steps with each project idea placed after the step it follows.
export function topicPath(slug: string): PathItem[] {
  const items: PathItem[] = topicProjects(slug).filter((project) => !project.after).map((item) => ({ kind: "project", item }))
  for (const problem of topicProblems(slug)) {
    items.push({ kind: "problem", item: problem })
    for (const project of topicProjects(slug)) if (project.after === problem.slug) items.push({ kind: "project", item: project })
  }
  return items
}

// The whole path in order, for previous/next navigation.
export const learnPath = topics.flatMap((topic) => topicPath(topic.slug))

export function pathHref(entry: PathItem) {
  return entry.kind === "project" ? `/learn/projects/${entry.item.slug}` : `/learn/problems/${entry.item.slug}`
}

export function topicTitle(slug: string) {
  return topicBySlug(slug)?.title ?? slug
}

export function problemById(id: string) {
  return problems.find((problem) => problem.id === id)
}
