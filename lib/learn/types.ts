export type Difficulty = "beginner" | "intermediate" | "advanced"

export type Resource = {
  id: string
  title: string
  url: string
  author: string
}

export type LearnTopic = {
  slug: string
  title: string
  prefix: string
  prerequisites: string[]
  outcome: string
  description: string
  // Required graded steps; optional deep dives and project ideas are counted separately.
  problemCount: number
  optionalCount: number
  projectCount: number
  difficultyCounts: Record<Difficulty, number>
  resources: Resource[]
}

export type LearnProblem = {
  id: string
  slug: string
  title: string
  topicSlug: string
  difficulty: Difficulty
  prerequisites: string[]
  tags: string[]
  entryPoint: string
  testCount: number
  // "script" steps are whole programs graded through stdin/stdout; "function" steps are imported.
  kind: "function" | "script"
  // Optional deep dives are graded but excluded from topic completion and progress bars.
  optional: boolean
}

// An ungraded brief shown on the path after the step it follows (`after`, null at a topic start).
export type LearnProject = {
  id: string
  slug: string
  title: string
  topicSlug: string
  after: string | null
  tags: string[]
}

export type ProjectPage = LearnProject & {
  uses: { slug: string; id: string; title: string }[]
  brief: string
  milestones: string[]
  stretch: string[]
  data: string
  setup: string
}

export type PathItem = { kind: "problem"; item: LearnProblem } | { kind: "project"; item: LearnProject }

export type ProblemPack = LearnProblem & {
  objectives: string[]
  allowedPackages: string[]
  // Libraries used only by optional comparison tests, which are skipped when unavailable.
  optionalPackages: string[]
  article: string
  statement: string
  starter: string
  solution: string
  solutionExplanation: string
  hints: string[]
  failureFeedback: { test: string; advice: string }[]
  // group: index of the TestCase class the test belongs to (into localClasses).
  visibleTests: { name: string; code: string; group?: number }[]
  // Test-module helpers the visible tests call, for the in-browser harness ("" when not local).
  localPrelude: string
  // Non-test members (setUp, helper methods) of each visible test's class, for the harness.
  localClasses: string[]
  resources: Resource[]
}

// Only this shape may cross the server-component/client boundary.
export type PublicProblemPack = Omit<ProblemPack, "solution" | "solutionExplanation"> & { localEligible: boolean }

export type LearnTestResult = { name: string; passed: boolean; message?: string }
export type LearnExecutionResult = {
  passed: number
  total: number
  status: "passed" | "failed"
  tests?: LearnTestResult[]
  output?: string
  // Submit only: names of the supplied tests that failed (their code stays private).
  failedTests?: string[]
}
