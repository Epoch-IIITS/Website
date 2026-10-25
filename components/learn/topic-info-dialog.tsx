"use client"

import Link from "next/link"
import { ArrowUpRight, CircleHelp } from "lucide-react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import type { LearnTopic } from "@/lib/learn/types"

type Prerequisite = { slug: string; title: string }

export function TopicInfoDialog({ topic, prerequisites }: { topic: LearnTopic; prerequisites: Prerequisite[] }) {
  return <Dialog>
    <DialogTrigger asChild>
      <button type="button" aria-label={`About ${topic.title}`} title={`About ${topic.title}`} className="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-md border border-border bg-card text-muted-foreground transition-colors hover:border-primary/50 hover:text-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring">
        <CircleHelp className="h-4 w-4" />
      </button>
    </DialogTrigger>
    <DialogContent className="flex max-h-[85vh] max-w-2xl flex-col gap-0 overflow-hidden p-0">
      <DialogHeader className="shrink-0 border-b border-border/70 px-6 py-5 pr-12">
        <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-primary">{topic.prefix} · Topic guide</p>
        <DialogTitle className="text-xl">{topic.title}</DialogTitle>
        <DialogDescription className="pt-2 leading-6">{topic.description}</DialogDescription>
      </DialogHeader>
      <div className="min-h-0 overflow-y-auto px-6 py-5">
        <div className="grid gap-5 sm:grid-cols-2">
          <section>
            <h2 className="text-[10px] font-semibold uppercase tracking-[0.15em] text-muted-foreground">What you will learn</h2>
            <p className="mt-2 text-sm leading-6">{topic.outcome}</p>
          </section>
          <section className="border-t border-border/70 pt-5 sm:border-l sm:border-t-0 sm:pl-5 sm:pt-0">
            <h2 className="text-[10px] font-semibold uppercase tracking-[0.15em] text-muted-foreground">Before you begin</h2>
            {prerequisites.length ? <div className="mt-2 flex flex-wrap gap-2">{prerequisites.map(({ slug, title }) => <Link key={slug} href={`/learn/topics/${slug}`} className="inline-flex items-center gap-1 rounded-md border border-border px-2 py-1 text-xs hover:border-primary/50 hover:text-primary">{title}<ArrowUpRight className="h-3 w-3" /></Link>)}</div> : <p className="mt-2 text-sm text-muted-foreground">No prerequisites. Start here.</p>}
          </section>
        </div>

        <dl className="mt-6 grid grid-cols-2 divide-x divide-border/70 rounded-md border border-border/70 bg-muted/20 py-3 text-center">
          <div><dt className="text-[10px] text-muted-foreground">Problems</dt><dd className="mt-1 text-sm font-semibold tabular-nums">{topic.problemCount}</dd></div>
          <div><dt className="text-[10px] text-muted-foreground">Levels</dt><dd className="mt-1 text-sm font-semibold tabular-nums">3</dd></div>
        </dl>

        <section className="mt-6 border-t border-border/70 pt-5">
          <h2 className="text-[10px] font-semibold uppercase tracking-[0.15em] text-muted-foreground">Curated resources</h2>
          <p className="mt-2 text-xs text-muted-foreground">Further reading from this topic&apos;s references.</p>
          <div className="mt-3 divide-y divide-border/70">{topic.resources.map((resource) => <a key={resource.id} href={resource.url} target="_blank" rel="noopener noreferrer" className="group flex items-start justify-between gap-4 py-3 first:pt-0"><div><p className="text-xs font-medium group-hover:text-primary">{resource.title}</p><p className="mt-1 text-[11px] text-muted-foreground">{resource.author}</p></div><ArrowUpRight className="mt-0.5 h-3.5 w-3.5 shrink-0 text-muted-foreground group-hover:text-primary" /></a>)}</div>
        </section>
      </div>
    </DialogContent>
  </Dialog>
}
