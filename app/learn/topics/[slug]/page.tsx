import type { Metadata } from "next"
import Link from "next/link"
import { notFound } from "next/navigation"
import { ArrowRight } from "lucide-react"
import { LearnShell } from "@/components/learn/learn-shell"
import { ProblemSheet } from "@/components/learn/problem-sheet"
import { TopicInfoDialog } from "@/components/learn/topic-info-dialog"
import { topicBySlug, topicProblems, topicProjects, topicTitle, topics } from "@/lib/learn/data"

type Props = { params: Promise<{ slug: string }> }

export function generateStaticParams() {
  return topics.map((topic) => ({ slug: topic.slug }))
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const topic = topicBySlug((await params).slug)
  return { title: topic ? `${topic.title} · Learn | Epoch` : "Topic not found | Epoch" }
}

export default async function LearnTopicPage({ params }: Props) {
  const topic = topicBySlug((await params).slug)
  if (!topic) notFound()
  const sheet = topicProblems(topic.slug)
  const first = sheet[0]

  return <LearnShell active="explore"><div className="mx-auto max-w-6xl px-7 pb-16 pt-8 xl:px-10">
    <header className="flex items-center justify-between gap-4 border-b border-border/70 pb-5">
      <div className="flex min-w-0 items-center gap-3">
        <div className="min-w-0"><p className="truncate text-xs text-muted-foreground">{topic.title} · {topic.problemCount} problems{topic.optionalCount ? ` · ${topic.optionalCount} optional` : ""}{topic.projectCount ? ` · ${topic.projectCount} project ideas` : ""}</p><h1 className="mt-0.5 text-2xl font-semibold tracking-tight">Problem sheet</h1></div>
      </div>
      <div className="flex shrink-0 items-center gap-3">
        {first && <Link href={`/learn/problems/${first.slug}`} className="inline-flex items-center gap-2 text-xs font-medium text-primary hover:underline">Start with {first.title}<ArrowRight className="h-3.5 w-3.5" /></Link>}
        <TopicInfoDialog topic={topic} prerequisites={topic.prerequisites.map((slug) => ({ slug, title: topicTitle(slug) }))} />
      </div>
    </header>
    <ProblemSheet problems={sheet} projects={topicProjects(topic.slug)} />
  </div></LearnShell>
}
