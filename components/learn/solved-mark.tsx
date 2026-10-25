"use client"

import { useEffect, useState } from "react"
import { Check, Lightbulb } from "lucide-react"

// Read-only checkbox showing whether the signed-in member has passed a problem through Submit.
export function SolvedMark({ solved }: { solved: boolean }) {
  return <span role="img" aria-label={solved ? "Solved" : "Not solved"} className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-[4px] border ${solved ? "border-primary bg-primary text-primary-foreground" : "border-muted-foreground/40"}`}>
    {solved && <Check className="h-3 w-3" strokeWidth={3} />}
  </span>
}

// Shown in place of a solved mark for ungraded project ideas.
export function ProjectMark() {
  return <span role="img" aria-label="Project idea" className="flex h-4 w-4 shrink-0 items-center justify-center text-primary"><Lightbulb className="h-4 w-4" /></span>
}

// Optional deep dives are graded but do not count towards topic completion.
export function OptionalBadge() {
  return <span className="shrink-0 rounded-full border border-border px-1.5 py-px text-[10px] font-medium text-muted-foreground">Optional</span>
}

// Slugs the signed-in member has passed; empty when signed out or progress cannot be loaded.
export function useSolvedProblems() {
  const [solved, setSolved] = useState<Set<string>>(() => new Set())
  useEffect(() => {
    let cancelled = false
    fetch("/api/learn/progress", { cache: "no-store" }).then((response) => response.ok ? response.json() : null).then((data) => {
      if (cancelled || !Array.isArray(data?.completedSlugs)) return
      setSolved(new Set(data.completedSlugs.filter((slug: unknown): slug is string => typeof slug === "string")))
    }).catch(() => {})
    return () => { cancelled = true }
  }, [])
  return solved
}
