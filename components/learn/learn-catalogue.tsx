"use client"

import { useEffect, useMemo, useState } from "react"
import Link from "next/link"
import { ArrowRight, ChevronRight, Search } from "lucide-react"
import { Input } from "@/components/ui/input"
import { OptionalBadge, ProjectMark, SolvedMark } from "@/components/learn/solved-mark"
import { topics, problems, projects, problemBySlug, requiredProblems, topicPath, pathHref } from "@/lib/learn/data"

const filters = [
  { id: "all", label: "All topics" },
  { id: "foundations", label: "Foundations" },
  { id: "models", label: "Build models" },
  { id: "frontiers", label: "Explore further" },
] as const

type Filter = (typeof filters)[number]["id"]

const groups: Record<Exclude<Filter, "all">, string[]> = {
  foundations: ["python", "mathematics", "statistics", "numpy", "pandas", "fastapi"],
  models: ["machine-learning", "deep-learning", "nlp", "llms", "computer-vision"],
  frontiers: ["explainable-ai", "federated-learning", "reinforcement-learning", "agentic-ai"],
}
export function LearnCatalogue() {
  const [query, setQuery] = useState("")
  const [filter, setFilter] = useState<Filter>("all")
  const [openTopic, setOpenTopic] = useState<string | null>(null)
  const [closedSearchTopic, setClosedSearchTopic] = useState<string | null>(null)
  const [current, setCurrent] = useState(problems[0])
  const [savedProgress, setSavedProgress] = useState(false)
  const [solved, setSolved] = useState<Set<string>>(() => new Set())
  useEffect(() => {
    let cancelled = false
    fetch("/api/learn/progress", { cache: "no-store" }).then((response) => response.ok ? response.json() : null).then((data) => {
      if (cancelled || !data) return
      const problem = problemBySlug(data.continueProblem?.slug)
      if (problem) setCurrent(problem)
      if (Array.isArray(data.completedSlugs)) setSolved(new Set(data.completedSlugs.filter((slug: unknown): slug is string => typeof slug === "string")))
      setSavedProgress(true)
    }).catch(() => {})
    return () => { cancelled = true }
  }, [])
  const search = query.trim().toLowerCase()
  const shown = useMemo(() => topics.filter((topic) => {
    if (filter !== "all" && !groups[filter].includes(topic.slug)) return false
    if (!search) return true
    return `${topic.title} ${topic.description} ${topic.outcome}`.toLowerCase().includes(search)
      || topicPath(topic.slug).some(({ item }) => `${item.id} ${item.title} ${item.tags.join(" ")}`.toLowerCase().includes(search))
  }), [filter, search])

  return <div className="px-7 pb-16 pt-9 xl:px-10 2xl:px-14">
    <div className="flex items-end justify-between gap-4 border-b border-border/70 pb-5">
      <h1 id="catalogue-heading" className="text-2xl font-semibold tracking-tight">Topics</h1>
      <span className="text-xs text-muted-foreground">{topics.length} topics · {requiredProblems.length} problems{projects.length ? ` · ${projects.length} project ideas` : ""}</span>
    </div>

    <div className="mt-6 grid gap-7 xl:grid-cols-[minmax(0,1fr)_260px] 2xl:grid-cols-[minmax(0,1fr)_280px]">
      <section aria-labelledby="catalogue-heading" className="min-w-0">
        <div className="flex items-end justify-between gap-4">
          <p className="text-xs text-muted-foreground">Choose a topic or search for a problem.</p>
          <span className="text-xs tabular-nums text-muted-foreground">{shown.length} / {topics.length} topics</span>
        </div>
        <div className="mt-5 flex flex-wrap items-center gap-3">
          <div className="relative min-w-[250px] flex-1"><Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" /><Input aria-label="Search topics and problems" value={query} onChange={(event) => { setQuery(event.target.value); setClosedSearchTopic(null) }} placeholder="Search topics or problems" className="h-10 rounded-md border-border/80 bg-card pl-10" /></div>
          <div className="flex flex-wrap gap-1" role="group" aria-label="Topic filters">{filters.map((item) => <button type="button" key={item.id} onClick={() => setFilter(item.id)} aria-pressed={filter === item.id} className={`rounded-md px-3 py-2 text-xs font-medium transition-colors ${filter === item.id ? "bg-muted text-foreground" : "text-muted-foreground hover:bg-muted/60 hover:text-foreground"}`}>{item.label}</button>)}</div>
        </div>

        {shown.length ? <div className="mt-5 overflow-hidden rounded-lg border border-border/80 bg-card">
          {shown.map((topic) => {
            const topicMatches = `${topic.title} ${topic.description} ${topic.outcome}`.toLowerCase().includes(search)
            const topicItems = topicPath(topic.slug).filter(({ item }) => !search || topicMatches || `${item.id} ${item.title} ${item.tags.join(" ")}`.toLowerCase().includes(search))
            const expanded = search ? closedSearchTopic !== topic.slug : openTopic === topic.slug
            const solvedCount = requiredProblems.filter((problem) => problem.topicSlug === topic.slug && solved.has(problem.slug)).length
            const percent = topic.problemCount ? Math.round((solvedCount / topic.problemCount) * 100) : 0
            return <div key={topic.slug} className="border-b border-border/70 last:border-b-0">
              <div className="flex items-center gap-1 px-2 transition-colors hover:bg-muted/35">
                <button type="button" onClick={() => search ? setClosedSearchTopic(expanded ? topic.slug : null) : setOpenTopic(expanded ? null : topic.slug)} aria-label={`${expanded ? "Collapse" : "Expand"} ${topic.title} problems`} aria-expanded={expanded} className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-muted hover:text-primary"><ChevronRight className={`h-4 w-4 transition-transform ${expanded ? "rotate-90" : ""}`} /></button>
                <Link href={`/learn/topics/${topic.slug}`} className="group flex min-w-0 flex-1 items-center gap-3 py-3 pr-2">
                  <span className="min-w-0 flex-1 truncate text-sm font-medium group-hover:text-primary">{topic.title}</span>
                  <span className="hidden h-1.5 w-20 shrink-0 overflow-hidden rounded-full bg-muted xl:block" role="progressbar" aria-label={`${topic.title} problems solved`} aria-valuemin={0} aria-valuemax={topic.problemCount} aria-valuenow={solvedCount} aria-valuetext={`${solvedCount} of ${topic.problemCount} solved`}><span className="block h-full rounded-full bg-primary transition-[width]" style={{ width: `${percent}%` }} /></span>
                  <span className="w-20 shrink-0 text-right text-xs tabular-nums text-muted-foreground">{topic.problemCount} problems</span>
                </Link>
              </div>
              {expanded && <div className="border-t border-border/70 bg-muted/20 px-4 py-2">
                <div>{topicItems.map((entry) => {
                  const { item } = entry
                  return <Link key={item.id} href={pathHref(entry)} className="flex items-center gap-3 border-b border-border/50 py-2 text-xs hover:text-primary">
                    {entry.kind === "project" ? <ProjectMark /> : <SolvedMark solved={solved.has(item.slug)} />}
                    <span className="min-w-0 flex-1 truncate">{item.title}</span>
                    {entry.kind === "problem" && entry.item.optional && <OptionalBadge />}
                    <span className="capitalize text-muted-foreground">{entry.kind === "project" ? "Project idea" : entry.item.difficulty}</span><ChevronRight className="h-3 w-3" />
                  </Link>
                })}</div>
                <Link href={`/learn/topics/${topic.slug}`} className="mt-2 inline-flex items-center gap-1 text-xs font-medium text-primary hover:underline">View full sheet <ArrowRight className="h-3 w-3" /></Link>
              </div>}
            </div>
          })}
        </div> : <div className="mt-5 rounded-lg border border-dashed border-border bg-card p-10 text-center"><p className="text-sm font-medium">No topics found</p><p className="mt-1 text-xs text-muted-foreground">Try a different topic, concept, or problem name.</p><button className="mt-4 text-xs font-medium text-primary hover:underline" onClick={() => { setQuery(""); setFilter("all") }}>Clear filters</button></div>}
      </section>

      <aside className="space-y-5" aria-label="Learning guide">
        <div className="rounded-lg border border-border/80 bg-card p-5">
          <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-muted-foreground">{savedProgress ? "Continue learning" : "Start practising"}</p>
          <p className="mt-5 text-xs text-primary">{current.id}</p>
          <h3 className="mt-1 text-base font-semibold">{current.title}</h3>
          <p className="mt-2 text-xs leading-5 text-muted-foreground">Open the editor and try the visible tests.</p>
          <Link href={`/learn/problems/${current.slug}`} className="mt-5 flex items-center justify-between border-t border-border/70 pt-4 text-xs font-medium hover:text-primary">Open problem <ArrowRight className="h-3.5 w-3.5" /></Link>
        </div>
        <div className="rounded-lg border border-border/80 bg-card p-5">
          <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-muted-foreground">Study flow</p>
          <ol className="mt-4 space-y-3 text-xs leading-5 text-muted-foreground"><li><span className="mr-2 tabular-nums text-primary">01</span>Read a concept article.</li><li><span className="mr-2 tabular-nums text-primary">02</span>Try its Python problem.</li><li><span className="mr-2 tabular-nums text-primary">03</span>Use hints when you need them.</li></ol>
          <p className="mt-5 border-t border-border/70 pt-4 text-[11px] leading-5 text-muted-foreground">Run checks visible tests for practice. Sign in and Submit for trusted grading and saved progress.</p>
        </div>
      </aside>
    </div>
  </div>
}
