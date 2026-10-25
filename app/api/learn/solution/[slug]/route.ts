import { NextResponse } from "next/server"
import { packBySlug } from "@/lib/learn/pack"
import { markdownHtml } from "@/lib/learn/markdown"

export async function GET(_request: Request, { params }: { params: Promise<{ slug: string }> }) {
  const pack = packBySlug((await params).slug)
  if (!pack) return NextResponse.json({ error: "Unknown problem." }, { status: 404 })
  // The leading docstring repeats the explanation, which is returned separately as HTML.
  const solution = pack.solution.replace(/^r?"""[\s\S]*?"""\s*/, "")
  return NextResponse.json({ solution, explanationHtml: markdownHtml(pack.solutionExplanation) }, { headers: { "Cache-Control": "no-store" } })
}
