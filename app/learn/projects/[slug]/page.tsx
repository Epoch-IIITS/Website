import type { Metadata } from "next"
import Link from "next/link"
import { notFound } from "next/navigation"
import { ArrowLeft, ArrowRight, ChevronRight, Lightbulb } from "lucide-react"
import { LearnShell } from "@/components/learn/learn-shell"
import { ProjectMilestones } from "@/components/learn/project-milestones"
import { learnPath, pathHref, projectBySlug, projects, topicTitle } from "@/lib/learn/data"
import { projectPageBySlug } from "@/lib/learn/project"
import { markdownHtml } from "@/lib/learn/markdown"

type Props = { params: Promise<{ slug: string }> }

export function generateStaticParams() {
  return projects.map((project) => ({ slug: project.slug }))
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const project = projectBySlug((await params).slug)
  return { title: project ? `${project.title} · Project idea · Learn | Epoch` : "Project not found | Epoch" }
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return <section className="mt-8 border-t border-border/70 pt-6"><h2 className="text-sm font-semibold">{title}</h2>{children}</section>
}

// Project ideas are ungraded reading pages: no editor, Run or Submit.
export default async function LearnProjectPage({ params }: Props) {
  const slug = (await params).slug
  const project = projectPageBySlug(slug)
  if (!project) notFound()
  const position = learnPath.findIndex((entry) => entry.kind === "project" && entry.item.slug === slug)
  const previous = learnPath[position - 1]
  const next = learnPath[position + 1]

  return <LearnShell active="explore"><div className="mx-auto max-w-3xl px-7 pb-16 pt-8 xl:px-10">
    <div className="flex items-center justify-between gap-3 border-b border-border/70 pb-4">
      <nav aria-label="Breadcrumb" className="flex min-w-0 items-center gap-2 text-xs text-muted-foreground"><Link href="/learn" className="hover:text-foreground">Learn</Link><ChevronRight className="h-3 w-3 shrink-0" /><Link href={`/learn/topics/${project.topicSlug}`} className="truncate hover:text-foreground">{topicTitle(project.topicSlug)}</Link><ChevronRight className="h-3 w-3 shrink-0" /><span className="text-foreground">{project.id}</span></nav>
      <div className="flex shrink-0 items-center gap-1 text-xs">{previous ? <Link href={pathHref(previous)} aria-label={`Previous: ${previous.item.title}`} title={`Previous: ${previous.item.title}`} className="rounded p-1.5 text-muted-foreground hover:bg-muted hover:text-foreground"><ArrowLeft className="h-4 w-4" /></Link> : <span className="w-7" />}{next ? <Link href={pathHref(next)} aria-label={`Next: ${next.item.title}`} title={`Next: ${next.item.title}`} className="rounded p-1.5 text-muted-foreground hover:bg-muted hover:text-foreground"><ArrowRight className="h-4 w-4" /></Link> : <span className="w-7" />}</div>
    </div>
    <header className="mt-7">
      <p className="flex items-center gap-1.5 text-[10px] font-semibold uppercase tracking-[0.16em] text-primary"><Lightbulb className="h-3.5 w-3.5" aria-hidden="true" />Project idea · ungraded</p>
      <h1 className="mt-2 text-2xl font-semibold tracking-tight">{project.title}</h1>
    </header>
    <article className="learn-prose mt-5" dangerouslySetInnerHTML={{ __html: markdownHtml(project.brief) }} />
    <Section title="You will use"><ul className="mt-3 flex flex-wrap gap-2">{project.uses.map((step) => <li key={step.slug}><Link href={`/learn/problems/${step.slug}`} className="inline-flex items-center gap-1.5 rounded-md border border-border px-2 py-1 text-xs hover:border-primary/50 hover:text-primary"><span className="tabular-nums text-muted-foreground">{step.id}</span>{step.title}</Link></li>)}</ul></Section>
    <Section title="Milestones"><p className="mt-1 text-xs text-muted-foreground">Build the smallest working version first. Ticks are saved in this browser only.</p><ProjectMilestones slug={project.slug} milestones={project.milestones} /></Section>
    <Section title="Stretch goals"><ul className="mt-3 list-disc space-y-1.5 pl-5 text-sm leading-6">{project.stretch.map((goal) => <li key={goal}>{goal}</li>)}</ul></Section>
    <Section title="Data"><article className="learn-prose mt-3" dangerouslySetInnerHTML={{ __html: markdownHtml(project.data) }} /></Section>
    <Section title="Run it yourself"><article className="learn-prose mt-3" dangerouslySetInnerHTML={{ __html: markdownHtml(project.setup) }} /></Section>
  </div></LearnShell>
}
