"use client"

import { useEffect, useState } from "react"

// Milestone ticks are a personal convenience kept in this browser only; projects are ungraded.
export function ProjectMilestones({ slug, milestones }: { slug: string; milestones: string[] }) {
  const key = `learn-project-milestones:${slug}`
  const [done, setDone] = useState<boolean[]>(() => milestones.map(() => false))
  useEffect(() => {
    try {
      const saved = JSON.parse(localStorage.getItem(key) ?? "[]")
      if (Array.isArray(saved)) setDone(milestones.map((_, index) => saved[index] === true))
    } catch { /* Storage can be unavailable; the list still works for this visit. */ }
  }, [key, milestones])

  function toggle(index: number) {
    const next = done.map((value, position) => position === index ? !value : value)
    setDone(next)
    try { localStorage.setItem(key, JSON.stringify(next)) } catch { /* Keep the tick for this visit only. */ }
  }

  return <ol className="mt-3 space-y-2">{milestones.map((milestone, index) => <li key={index}>
    <label className="flex cursor-pointer items-start gap-3 rounded-md border border-border/70 bg-muted/20 px-3 py-2.5 text-sm leading-6 transition-colors hover:border-primary/40">
      <input type="checkbox" checked={done[index] ?? false} onChange={() => toggle(index)} className="mt-1 h-4 w-4 shrink-0 accent-[hsl(var(--primary))]" />
      <span className={done[index] ? "text-muted-foreground line-through" : ""}><span className="mr-2 tabular-nums text-primary">{String(index + 1).padStart(2, "0")}</span>{milestone}</span>
    </label>
  </li>)}</ol>
}
