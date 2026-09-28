export type Person = { _id: string; name: string; email?: string; image?: string }
export type TeamGroupOption = { id: string; name: string; userIds: string[]; unlinkedCount: number }
export type TeamYearOption = { _id: string; year: number; published: boolean; groups: TeamGroupOption[] }
export type ParticipantDirectory = { people: Person[]; teamYears: TeamYearOption[] }
export type InitiativeSummary = {
  _id: string
  title: string
  status: "active" | "completed"
  participants: Person[]
  updatedAt: string
  completedAt?: string
  pendingTasks: number
  overdueTasks: number
  unansweredQuestions: number
  nextTasks: { title: string; dueAt?: string }[]
  firstOpenQuestion?: string
}
export type InitiativeTask = {
  _id: string
  createdBy: string
  title: string
  description: string
  dueAt?: string | null
  status: "todo" | "done"
  assignees: Person[]
}
export type InitiativeBlock = {
  _id: string
  createdBy: string
  type: "note" | "question" | "reference"
  title: string
  content: string
  url: string
  taggedUsers: Person[]
  x: number
  y: number
  width?: number
  height?: number
  version: number
}
export type InitiativeReply = {
  _id: string
  block: string
  body: string
  createdBy: Person
  createdAt: string
}
export type InitiativeTaskComment = {
  _id: string
  task: string
  body: string
  mentions: string[]
  createdBy: Person
  createdAt: string
}
export type InitiativeDetail = {
  initiative: Omit<InitiativeSummary, "pendingTasks" | "overdueTasks" | "unansweredQuestions">
  tasks: InitiativeTask[]
  blocks: InitiativeBlock[]
  replies: InitiativeReply[]
  comments: InitiativeTaskComment[]
  actor: { id: string; admin: boolean }
}
