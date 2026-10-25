import type { Metadata } from "next"
import { LearnShell } from "@/components/learn/learn-shell"
import { LearnCatalogue } from "@/components/learn/learn-catalogue"
import { requiredProblems, topics } from "@/lib/learn/data"

export const metadata: Metadata = {
  title: "Learn | Epoch",
  description: `Learn Python from zero, then explore ${topics.length - 1} AI, machine learning and API topics with ${requiredProblems.length} guided Python problems.`,
}

export default function LearnPage() {
  return <LearnShell active="explore"><LearnCatalogue /></LearnShell>
}
