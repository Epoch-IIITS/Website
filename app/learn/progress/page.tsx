import type { Metadata } from "next"
import Link from "next/link"
import { getServerSession } from "next-auth"
import { ArrowRight, ArrowUpRight } from "lucide-react"
import { LearnShell } from "@/components/learn/learn-shell"
import { problems, topics } from "@/lib/learn/data"
import { authOptions } from "@/lib/auth"
import { getLearnProgress } from "@/lib/learn/progress"

export const dynamic = "force-dynamic"

export const metadata: Metadata = {
  title: "Progress · Learn | Epoch",
  description: "Your saved progress across the curriculum.",
}

export default async function LearnProgressPage() {
  const session = await getServerSession(authOptions)
  if (!session?.user?.id) return <LearnShell active="progress"><div className="mx-auto max-w-3xl px-7 pt-12"><h1 className="text-2xl font-semibold">Your progress</h1><p className="mt-3 text-sm text-muted-foreground">Sign in to save submissions and see your progress.</p><Link href="/auth/signin?callbackUrl=%2Flearn%2Fprogress" className="mt-5 inline-flex text-sm font-medium text-primary underline">Sign in</Link></div></LearnShell>
  let progress: Awaited<ReturnType<typeof getLearnProgress>>
  try { progress = await getLearnProgress(session.user.id) }
  catch { return <LearnShell active="progress"><div className="mx-auto max-w-3xl px-7 pt-12"><h1 className="text-2xl font-semibold">Your progress</h1><p role="alert" className="mt-3 text-sm text-destructive">Unable to load progress. Please try again.</p></div></LearnShell> }
  const complete = progress.completed
  const completedByTopic = progress.byTopic
  const current = progress.continueProblem ?? problems[0]
  return <LearnShell active="progress"><div className="px-7 pb-16 pt-8 xl:px-10 2xl:px-14">
    <h1 className="sr-only">Progress</h1>
    <div className="grid gap-7 xl:grid-cols-[minmax(0,1fr)_260px] 2xl:grid-cols-[minmax(0,1fr)_280px]">
      <div className="min-w-0">
        <section className="overflow-hidden rounded-lg border border-border/80 bg-card" aria-label="Progress summary">
          <div className="grid grid-cols-3 divide-x divide-border/70">
            <div className="px-5 py-5"><strong className="text-2xl font-semibold tabular-nums">{complete}<span className="text-sm font-normal text-muted-foreground"> / {progress.total}</span></strong><p className="mt-1 text-xs text-muted-foreground">problems complete</p></div>
            <div className="px-5 py-5"><strong className="text-2xl font-semibold tabular-nums">{progress.topicsComplete}<span className="text-sm font-normal text-muted-foreground"> / {progress.totalTopics}</span></strong><p className="mt-1 text-xs text-muted-foreground">topics complete</p></div>
            <div className="px-5 py-5"><strong className="text-2xl font-semibold tabular-nums">{Math.round(complete / progress.total * 100)}%</strong><p className="mt-1 text-xs text-muted-foreground">of the practice path</p></div>
          </div>
        </section>
        <section className="mt-7" aria-labelledby="topic-progress-heading"><div className="flex items-end justify-between"><div><h2 id="topic-progress-heading" className="text-xl font-semibold tracking-tight">Topic progress</h2><p className="mt-1 text-xs text-muted-foreground">Passing trusted submissions · {progress.attempts} total attempts</p></div><span className="text-xs text-muted-foreground">{topics.length} topics</span></div>
          <div className="mt-5 overflow-hidden rounded-lg border border-border/80 bg-card">{topics.map((topic, index) => {
            const count = completedByTopic[topic.slug] ?? 0
            const percentage = Math.round(count / topic.problemCount * 100)
            return <Link key={topic.slug} href={`/learn/topics/${topic.slug}`} className="group flex min-h-[65px] items-center gap-4 border-b border-border/70 px-5 py-3 transition-colors last:border-b-0 hover:bg-muted/35"><span className="w-7 shrink-0 text-xs tabular-nums text-muted-foreground">{String(index + 1).padStart(2, "0")}</span><span className="min-w-0 flex-1 text-sm font-medium group-hover:text-primary">{topic.title}</span><div className="hidden h-1 w-20 overflow-hidden rounded-full bg-muted xl:block"><div className="h-full bg-primary" style={{ width: `${percentage}%` }} /></div><span className="w-16 shrink-0 text-right text-xs tabular-nums text-muted-foreground">{count} / {topic.problemCount}</span><ArrowUpRight className="h-4 w-4 text-muted-foreground group-hover:text-primary" /></Link>
          })}</div>
        </section>
      </div>
      <aside className="space-y-5" aria-label="Next steps"><div className="rounded-lg border border-border/80 bg-card p-5"><p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-muted-foreground">Continue learning</p><p className="mt-5 text-xs text-primary">{current.id}</p><h2 className="mt-1 text-base font-semibold">{current.title}</h2><Link href={`/learn/problems/${current.slug}`} className="mt-5 flex items-center justify-between border-t border-border/70 pt-4 text-xs font-medium hover:text-primary">Open problem <ArrowRight className="h-3.5 w-3.5" /></Link></div><div className="rounded-lg border border-border/80 bg-card p-5"><p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-muted-foreground">Explore</p><p className="mt-3 text-xs leading-5 text-muted-foreground">Choose any topic when you are ready to try something new.</p><Link href="/learn" className="mt-4 inline-flex items-center gap-1 text-xs font-medium text-primary hover:underline">Browse catalogue <ArrowRight className="h-3.5 w-3.5" /></Link></div></aside>
    </div>
  </div></LearnShell>
}
