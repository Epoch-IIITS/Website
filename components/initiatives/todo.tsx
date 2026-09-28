"use client"

import { useState } from "react"
import { CalendarDays, CheckCircle2, Circle, MessageCircle, Plus, Trash2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import type { InitiativeTask, InitiativeTaskComment, Person } from "./types"
import { TaskComments } from "./task-comments"

type Props = { tasks: InitiativeTask[]; comments: InitiativeTaskComment[]; participants: Person[]; actor: { id: string; admin: boolean }; readOnly: boolean; compact?: boolean; onAction: (payload: object) => Promise<boolean> }
const timeFormat = new Intl.DateTimeFormat("en-IN", { dateStyle: "medium", timeStyle: "short", timeZone: "Asia/Kolkata" })

export function InitiativeTodo({ tasks, comments, participants, actor, readOnly, compact = false, onAction }: Props) {
  const [viewingId, setViewingId] = useState<string | null>(null)
  const [editing, setEditing] = useState<InitiativeTask | null>(null)
  const [open, setOpen] = useState(false)
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [dueAt, setDueAt] = useState("")
  const [assignees, setAssignees] = useState<string[]>([])
  const [saving, setSaving] = useState(false)
  const [togglingId, setTogglingId] = useState<string | null>(null)

  function edit(task: InitiativeTask | null) {
    setViewingId(null)
    setEditing(task)
    setTitle(task?.title || "")
    setDescription(task?.description || "")
    setDueAt(task?.dueAt ? new Date(new Date(task.dueAt).getTime() + 330 * 60000).toISOString().slice(0, 16) : "")
    setAssignees(task?.assignees.map(person => person._id) || [])
    setOpen(true)
  }

  async function save() {
    setSaving(true)
    const payload = { action: editing ? "task.update" : "task.create", ...(editing ? { id: editing._id } : {}), title, description, dueAt: dueAt ? new Date(`${dueAt}:00+05:30`).toISOString() : null, assignees }
    if (await onAction(payload)) setOpen(false)
    setSaving(false)
  }

  async function remove(task: InitiativeTask) {
    if (readOnly || saving || !window.confirm(`Permanently delete task “${task.title}” and its comments?`)) return
    setSaving(true)
    if (await onAction({ action: "task.delete", id: task._id })) {
      setViewingId(null)
      setOpen(false)
    }
    setSaving(false)
  }

  async function toggleStatus(task: InitiativeTask) {
    if (readOnly || togglingId) return
    setTogglingId(task._id)
    await onAction({ action: "task.status", id: task._id, status: task.status === "done" ? "todo" : "done" })
    setTogglingId(null)
  }

  const pending = tasks.filter(task => task.status !== "done")
  const done = tasks.filter(task => task.status === "done")
  const viewingTask = tasks.find(task => task._id === viewingId)
  const taskComments = viewingTask ? comments.filter(comment => comment.task === viewingTask._id) : []

  return <div className={compact ? "space-y-3" : "space-y-6 py-4"}>
    <div className="flex flex-wrap items-center justify-between gap-2"><div><h2 className={compact ? "text-lg font-semibold" : "text-xl font-semibold"}>To-Do</h2><p className="text-xs text-muted-foreground">{pending.length} pending · {done.length} completed</p></div>{!readOnly && <Button size={compact ? "sm" : "default"} onClick={() => edit(null)}><Plus className="mr-1 h-4 w-4" />Add task</Button>}</div>
    <section className={compact ? "space-y-2" : "mx-auto max-w-4xl space-y-3"} aria-label="Tasks">
      {tasks.length === 0 && <p className="rounded-lg border border-dashed p-6 text-sm text-muted-foreground">No tasks here.</p>}
      {pending.map(task => <TaskCard key={task._id} task={task} compact={compact} readOnly={readOnly} toggling={Boolean(togglingId)} commentCount={comments.filter(comment => comment.task === task._id).length} onOpen={setViewingId} onToggle={toggleStatus} />)}
      {done.length > 0 && <h3 className="border-t pt-5 text-sm font-semibold uppercase tracking-wide text-muted-foreground">Completed <span className="ml-1 rounded-full bg-muted px-2 py-1">{done.length}</span></h3>}
      {done.map(task => <TaskCard key={task._id} task={task} compact={compact} readOnly={readOnly} toggling={Boolean(togglingId)} commentCount={comments.filter(comment => comment.task === task._id).length} onOpen={setViewingId} onToggle={toggleStatus} />)}
    </section>

    <Dialog open={Boolean(viewingTask)} onOpenChange={value => { if (!value) setViewingId(null) }}>
      <DialogContent className="max-h-[90vh] overflow-y-auto sm:max-w-2xl">
        {viewingTask && <>
          <DialogHeader><DialogTitle className="pr-6">{viewingTask.title}</DialogTitle></DialogHeader>
          <div className="space-y-5">
            <div className="flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
              <span className="rounded-full bg-muted px-2 py-1">{viewingTask.status === "done" ? "Done" : "To do"}</span>
              {viewingTask.dueAt && <span className="inline-flex items-center gap-1 rounded-full bg-muted px-2 py-1"><CalendarDays className="h-3.5 w-3.5" />{timeFormat.format(new Date(viewingTask.dueAt))}</span>}
            </div>
            {viewingTask.description && <div><h3 className="mb-1 text-sm font-medium">Description</h3><p className="whitespace-pre-wrap break-words text-sm text-muted-foreground">{viewingTask.description}</p></div>}
            <div><h3 className="mb-2 text-sm font-medium">Assignees</h3><div className="flex flex-wrap gap-2 text-sm">{viewingTask.assignees.length ? viewingTask.assignees.map(person => <span key={person._id} className="rounded-full bg-muted px-2 py-1">{person.name}</span>) : <span className="text-muted-foreground">Unassigned</span>}</div></div>
            {!readOnly && <div className="flex flex-wrap items-center gap-2"><Button variant="outline" size="sm" disabled={saving} onClick={() => edit(viewingTask)}>Edit task</Button>{(actor.admin || viewingTask.createdBy === actor.id) && <Button variant="destructive" size="sm" disabled={saving} onClick={() => void remove(viewingTask)}><Trash2 className="mr-1 h-4 w-4" />{saving ? "Deleting…" : "Delete task"}</Button>}</div>}
            <TaskComments taskId={viewingTask._id} comments={taskComments} participants={participants} readOnly={readOnly} onAction={onAction} />
          </div>
        </>}
      </DialogContent>
    </Dialog>

    <Dialog open={open} onOpenChange={setOpen}><DialogContent className="max-h-[90vh] overflow-y-auto"><DialogHeader><DialogTitle>{editing ? "Edit task" : "New task"}</DialogTitle></DialogHeader><div className="space-y-4">
      <Input aria-label="Task title" placeholder="What needs to be done?" value={title} maxLength={160} onChange={event => setTitle(event.target.value)} />
      <Textarea aria-label="Task description" placeholder="Add details, links, or context" value={description} onChange={event => setDescription(event.target.value)} maxLength={4000} />
      <label className="block space-y-1 text-sm font-medium">Deadline (IST)<input type="datetime-local" value={dueAt} onChange={event => setDueAt(event.target.value)} className="flex h-10 w-full rounded-md border bg-background px-3 text-sm" /></label>
      <div><p className="mb-2 text-sm font-medium">Assignees</p><div className="max-h-40 space-y-1 overflow-y-auto rounded-md border p-2">{participants.map(person => <label key={person._id} className="flex items-center gap-2 rounded p-2 text-sm hover:bg-muted"><input type="checkbox" checked={assignees.includes(person._id)} onChange={event => setAssignees(current => event.target.checked ? [...current, person._id] : current.filter(id => id !== person._id))} />{person.name}</label>)}</div></div>
      <div className="flex gap-2">{editing && (actor.admin || editing.createdBy === actor.id) && !readOnly && <Button variant="destructive" onClick={() => void remove(editing)} disabled={saving}>Delete task</Button>}<Button onClick={save} disabled={saving || !title.trim()} className="flex-1">{saving ? "Saving…" : "Save task"}</Button></div>
    </div></DialogContent></Dialog>
  </div>
}

function TaskCard({ task, commentCount, compact, readOnly, toggling, onOpen, onToggle }: { task: InitiativeTask; commentCount: number; compact: boolean; readOnly: boolean; toggling: boolean; onOpen: (id: string) => void; onToggle: (task: InitiativeTask) => void }) {
  return <Card className={`flex items-start transition-colors ${task.status === "done" ? "border-muted-foreground/20 bg-muted/70 text-muted-foreground shadow-none hover:bg-muted/90" : "hover:border-primary/50"}`}><button type="button" disabled={readOnly || toggling} onClick={() => onToggle(task)} aria-label={`${task.status === "done" ? "Mark as to do" : "Mark as done"}: ${task.title}`} className="ml-1 mt-1 flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-muted-foreground hover:text-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50">{task.status === "done" ? <CheckCircle2 className="h-5 w-5" /> : <Circle className="h-5 w-5" />}</button><button type="button" onClick={() => onOpen(task._id)} aria-label={`Open task ${task.title}`} className={`min-w-0 flex-1 rounded-lg text-left focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring ${compact ? "p-3 pl-2" : "p-4 pl-2"}`}>
      <div className="flex items-start justify-between gap-3"><span className="min-w-0 font-medium">{task.title}</span><span className={`shrink-0 rounded-full px-2 py-1 text-xs text-muted-foreground ${task.status === "done" ? "bg-background/70" : "bg-muted"}`}>{task.status === "done" ? "Done" : "To do"}</span></div>
      <div className="mt-2 flex flex-wrap items-center gap-x-6 gap-y-2 text-xs text-muted-foreground">{task.dueAt && <span className="inline-flex items-center gap-1"><CalendarDays className="h-3.5 w-3.5" />{timeFormat.format(new Date(task.dueAt))}</span>}{task.assignees.length > 0 && <span className="min-w-0 truncate">{task.assignees.map(person => person.name).join(", ")}</span>}{commentCount > 0 && <span className="inline-flex items-center gap-1"><MessageCircle className="h-3.5 w-3.5" />{commentCount}</span>}</div>
    </button></Card>
}
