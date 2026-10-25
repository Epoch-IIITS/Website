import type { Metadata } from "next"
import Link from "next/link"
import { notFound } from "next/navigation"
import { ArrowLeft, ArrowRight, ChevronRight } from "lucide-react"
import "katex/dist/katex.min.css"
import { LearnShell } from "@/components/learn/learn-shell"
import { ProblemWorkspace } from "@/components/learn/problem-workspace"
import { OptionalBadge } from "@/components/learn/solved-mark"
import { learnPath, pathHref, problemBySlug, topicTitle } from "@/lib/learn/data"
import { packBySlug } from "@/lib/learn/pack"
import { publicProblemPack } from "@/lib/learn/public-pack"
import { markdownHtml } from "@/lib/learn/markdown"

type Props = { params: Promise<{ slug: string }> }

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const problem = problemBySlug((await params).slug)
  return { title: problem ? `${problem.title} · Learn | Epoch` : "Problem not found | Epoch" }
}

export default async function LearnProblemPage({ params }: Props) {
  const slug = (await params).slug
  const pack = packBySlug(slug)
  if (!pack) notFound()
  const position = learnPath.findIndex((entry) => entry.kind === "problem" && entry.item.slug === slug)
  const previous = learnPath[position - 1]
  const next = learnPath[position + 1]

  return <LearnShell active="problem"><div className="flex h-screen min-h-0 flex-col gap-2 p-2">
    <div className="flex h-11 shrink-0 items-center justify-between gap-3 rounded-md border border-border bg-card px-4">
      <nav aria-label="Breadcrumb" className="flex min-w-0 items-center gap-2 text-xs text-muted-foreground"><Link href="/learn" className="hover:text-foreground">Learn</Link><ChevronRight className="h-3 w-3 shrink-0" /><Link href={`/learn/topics/${pack.topicSlug}`} className="truncate hover:text-foreground">{topicTitle(pack.topicSlug)}</Link><ChevronRight className="h-3 w-3 shrink-0" /><span className="text-foreground">{pack.id}</span>{pack.optional && <OptionalBadge />}</nav>
      <div className="flex shrink-0 items-center gap-2 border-l border-border pl-3 text-xs"><Link href={`/learn/topics/${pack.topicSlug}`} aria-label="Back to problem sheet" title="Back to problem sheet" className="rounded p-1.5 text-muted-foreground hover:bg-muted hover:text-foreground"><ArrowLeft className="h-4 w-4" /></Link><span className="hidden text-muted-foreground xl:inline">Sheet</span><span className="mx-1 h-4 border-l border-border" />{previous ? <Link href={pathHref(previous)} aria-label={`Previous: ${previous.item.title}`} title={`Previous: ${previous.item.title}`} className="rounded p-1.5 text-muted-foreground hover:bg-muted hover:text-foreground"><ArrowLeft className="h-4 w-4" /></Link> : <span className="w-7" />}{next ? <Link href={pathHref(next)} aria-label={`Next: ${next.item.title}`} title={`Next: ${next.item.title}`} className="rounded p-1.5 text-muted-foreground hover:bg-muted hover:text-foreground"><ArrowRight className="h-4 w-4" /></Link> : <span className="w-7" />}</div>
    </div>
    <ProblemWorkspace pack={publicProblemPack(pack)} articleHtml={markdownHtml(pack.article)} statementHtml={markdownHtml(pack.statement)} />
  </div></LearnShell>
}
