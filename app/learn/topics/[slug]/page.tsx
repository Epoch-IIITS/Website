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

  return <LearnShell active="explore"><div className="mx-auto max-w-6xl px-4 pb-16 pt-6 sm:px-7 lg:pt-8 xl:px-10">
    <header className="flex flex-wrap items-center justify-between gap-x-4 gap-y-3 border-b border-border/70 pb-5">
      <div className="flex min-w-0 flex-1 items-center gap-3">
        <div className="min-w-0"><p className="text-xs sm:truncate text-muted-foreground">{topic.title} · {topic.problemCount} problems{topic.optionalCount ? ` · ${topic.optionalCount} optional` : ""}{topic.projectCount ? ` · ${topic.projectCount} project ideas` : ""}</p><h1 className="mt-0.5 text-2xl font-semibold tracking-tight">Problem sheet</h1></div>
      </div>
      <div className="contents sm:flex sm:shrink-0 sm:items-center sm:gap-3">
        {first && <Link href={`/learn/problems/${first.slug}`} className="order-last flex h-11 w-full items-center justify-center gap-2 rounded-md bg-primary px-4 text-sm font-medium text-primary-foreground sm:order-none sm:inline-flex sm:h-auto sm:w-auto sm:rounded-none sm:bg-transparent sm:px-0 sm:text-xs sm:text-primary sm:hover:underline"><span className="truncate">Start with {first.title}</span><ArrowRight className="h-3.5 w-3.5 shrink-0" /></Link>}
        <TopicInfoDialog topic={topic} prerequisites={topic.prerequisites.map((slug) => ({ slug, title: topicTitle(slug) }))} />
      </div>
    </header>
    <ProblemSheet problems={sheet} projects={topicProjects(topic.slug)} />
  </div></LearnShell>
}
