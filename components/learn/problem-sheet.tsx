"use client"

import { useMemo, useState } from "react"
import Link from "next/link"
import { ArrowUpRight, Search } from "lucide-react"
import { Input } from "@/components/ui/input"
import { OptionalBadge, ProjectMark, SolvedMark, useSolvedProblems } from "@/components/learn/solved-mark"
import type { Difficulty, LearnProblem, LearnProject } from "@/lib/learn/types"

const levels: { id: Difficulty; title: string; note: string }[] = [
  { id: "beginner", title: "Beginner", note: "Start with the essentials" },
  { id: "intermediate", title: "Intermediate", note: "Connect the concepts" },
  { id: "advanced", title: "Advanced", note: "Stretch your understanding" },
]

export function ProblemSheet({ problems, projects }: { problems: LearnProblem[]; projects: LearnProject[] }) {
  const [query, setQuery] = useState("")
  const [level, setLevel] = useState<Difficulty | "all">("all")
  const solved = useSolvedProblems()
  const filtered = useMemo(() => problems.filter((problem) => {
    if (level !== "all" && problem.difficulty !== level) return false
    const search = query.toLowerCase().trim()
    return !search || `${problem.id} ${problem.title} ${problem.tags.join(" ")}`.toLowerCase().includes(search)
  }), [problems, query, level])
  const shownProjects = useMemo(() => level === "all" ? projects.filter((project) => {
    const search = query.toLowerCase().trim()
    return !search || `${project.id} ${project.title} ${project.tags.join(" ")}`.toLowerCase().includes(search)
  }) : [], [projects, query, level])

  return <div className="mt-5">
    <div className="flex flex-wrap items-center gap-3">
      <div className="relative min-w-[230px] flex-1"><Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" /><Input value={query} onChange={(event) => setQuery(event.target.value)} aria-label="Search this problem sheet" placeholder="Search this sheet" className="h-10 rounded-md bg-card pl-10" /></div>
      <div className="flex flex-wrap gap-1" role="group" aria-label="Filter problems by difficulty">{(["all", "beginner", "intermediate", "advanced"] as const).map((item) => <button type="button" key={item} onClick={() => setLevel(item)} aria-pressed={level === item} className={`rounded-md px-3 py-2 text-xs font-medium capitalize transition-colors ${level === item ? "bg-muted text-foreground" : "text-muted-foreground hover:bg-muted/60 hover:text-foreground"}`}>{item}</button>)}</div>
    </div>
    {filtered.length || shownProjects.length ? <div className="mt-5 overflow-hidden rounded-lg border border-border/80 bg-card">{levels.map((item) => {
      const rows = filtered.filter((problem) => problem.difficulty === item.id)
      if (!rows.length) return null
      return <section key={item.id} aria-label={`${item.title} problems`} className="border-b border-border/70 last:border-b-0">
        <div className="flex items-center gap-3 border-b border-border/70 bg-muted/25 px-5 py-3"><h3 className="text-xs font-semibold">{item.title}</h3><span className="text-xs text-muted-foreground">{item.note}</span><span className="ml-auto text-xs tabular-nums text-muted-foreground">{rows.length} problems</span></div>
        {rows.map((problem) => <Link href={`/learn/problems/${problem.slug}`} key={problem.id} className="group flex min-h-[60px] items-center gap-4 border-b border-border/60 px-5 py-3 transition-colors last:border-b-0 hover:bg-muted/35"><SolvedMark solved={solved.has(problem.slug)} /><div className="min-w-0 flex-1"><p className="flex items-center gap-2 text-sm font-medium group-hover:text-primary">{problem.title}{problem.optional && <OptionalBadge />}</p><p className="mt-0.5 truncate text-[11px] text-muted-foreground">{problem.tags.slice(0, 3).join(" · ")}</p></div><ArrowUpRight className="h-4 w-4 text-muted-foreground group-hover:text-primary" /></Link>)}
      </section>
    })}{shownProjects.length > 0 && <section aria-label="Project ideas" className="border-b border-border/70 last:border-b-0">
        <div className="flex items-center gap-3 border-b border-border/70 bg-muted/25 px-5 py-3"><h3 className="text-xs font-semibold">Project ideas</h3><span className="text-xs text-muted-foreground">Ungraded briefs to build on your own</span><span className="ml-auto text-xs tabular-nums text-muted-foreground">{shownProjects.length} project ideas</span></div>
        {shownProjects.map((project) => <Link href={`/learn/projects/${project.slug}`} key={project.id} className="group flex min-h-[60px] items-center gap-4 border-b border-border/60 px-5 py-3 transition-colors last:border-b-0 hover:bg-muted/35"><ProjectMark /><div className="min-w-0 flex-1"><p className="text-sm font-medium group-hover:text-primary">{project.title}</p><p className="mt-0.5 truncate text-[11px] text-muted-foreground">Project idea{project.tags.length ? ` · ${project.tags.slice(0, 3).join(" · ")}` : ""}</p></div><ArrowUpRight className="h-4 w-4 text-muted-foreground group-hover:text-primary" /></Link>)}
      </section>}</div> : <div className="mt-5 rounded-lg border border-dashed bg-card p-8 text-center text-sm text-muted-foreground">No problems match this search. Try another term or level.</div>}
  </div>
}
