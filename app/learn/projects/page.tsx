import type { Metadata } from "next"
import Link from "next/link"
import { ChevronRight } from "lucide-react"
import { LearnShell } from "@/components/learn/learn-shell"
import { ProjectMark } from "@/components/learn/solved-mark"
import { projects, topics } from "@/lib/learn/data"

export const metadata: Metadata = {
  title: "Project ideas · Learn | Epoch",
  description: `${projects.length} ungraded project ideas that put each Learn topic into practice.`,
}

export default function LearnProjectsPage() {
  const groups = topics
    .map((topic) => ({ topic, items: projects.filter((project) => project.topicSlug === topic.slug) }))
    .filter((group) => group.items.length > 0)

  return <LearnShell active="projects"><div className="px-4 pb-16 pt-6 sm:px-7 lg:pt-9 xl:px-10 2xl:px-14">
    <div className="flex items-end justify-between gap-4 border-b border-border/70 pb-5">
      <h1 className="text-2xl font-semibold tracking-tight">Projects</h1>
      <span className="text-right text-xs text-muted-foreground">{projects.length} project ideas · ungraded</span>
    </div>
    <p className="mt-6 max-w-2xl text-sm leading-6 text-muted-foreground">Build something real with what each topic teaches. Project ideas have milestones and stretch goals but no tests, so work through them at your own pace.</p>
    <div className="mt-6 space-y-8">
      {groups.map(({ topic, items }) => <section key={topic.slug} aria-labelledby={`projects-${topic.slug}`}>
        <h2 id={`projects-${topic.slug}`} className="kicker mb-3">{topic.title}</h2>
        <ul className="overflow-hidden rounded-xl border bg-card">
          {items.map((project) => <li key={project.slug} className="border-b last:border-b-0">
            <Link href={`/learn/projects/${project.slug}`} className="group flex min-h-14 items-center gap-4 px-4 py-3 transition-colors hover:bg-muted/40 sm:px-5">
              <ProjectMark />
              <span className="w-14 shrink-0 font-mono text-xs text-subtle">{project.id}</span>
              <span className="min-w-0 flex-1 text-sm font-medium group-hover:text-primary">{project.title}</span>
              <span className="hidden truncate font-mono text-xs text-muted-foreground sm:block">{project.tags.slice(0, 3).join(" · ")}</span>
              <ChevronRight className="h-4 w-4 shrink-0 text-subtle" aria-hidden="true" />
            </Link>
          </li>)}
        </ul>
      </section>)}
    </div>
  </div></LearnShell>
}
