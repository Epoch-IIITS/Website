import "server-only"
import packs from "@/lib/learn/packs.generated.json"
import type { ProblemPack } from "@/lib/learn/types"

const packMap = packs as Record<string, ProblemPack>

export function packBySlug(slug: string) {
  return Object.hasOwn(packMap, slug) ? packMap[slug] : undefined
}
