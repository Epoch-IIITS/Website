import "server-only"
import type { ProblemPack, PublicProblemPack } from "@/lib/learn/types"
import localCompatibility from "@/lib/learn/local-compat.generated.json"

export function publicProblemPack(pack: ProblemPack): PublicProblemPack {
  const { solution: _solution, solutionExplanation: _explanation, ...publicPack } = pack
  return { ...publicPack, localEligible: Boolean((localCompatibility as Record<string, boolean>)[pack.slug]) }
}
