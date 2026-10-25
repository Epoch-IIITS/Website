import "server-only"
import projectPages from "@/lib/learn/projects.generated.json"
import type { ProjectPage } from "@/lib/learn/types"

const projectMap = projectPages as Record<string, ProjectPage>

export function projectPageBySlug(slug: string) {
  return Object.hasOwn(projectMap, slug) ? projectMap[slug] : undefined
}
