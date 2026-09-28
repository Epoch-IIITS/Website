"use client"

import { useRef, useState, type FormEvent, type KeyboardEvent } from "react"
import { Send } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import type { InitiativeTaskComment, Person } from "./types"

type Props = {
  taskId: string
  comments: InitiativeTaskComment[]
  participants: Person[]
  readOnly: boolean
  onAction: (payload: object) => Promise<boolean>
}

const timeFormat = new Intl.DateTimeFormat("en-IN", { dateStyle: "medium", timeStyle: "short", timeZone: "Asia/Kolkata" })

export function TaskComments({ taskId, comments, participants, readOnly, onAction }: Props) {
  const [body, setBody] = useState("")
  const [cursor, setCursor] = useState(0)
  const [selected, setSelected] = useState<string[]>([])
  const [active, setActive] = useState(0)
  const [sending, setSending] = useState(false)
  const input = useRef<HTMLTextAreaElement>(null)
  const beforeCursor = body.slice(0, cursor)
  const match = /(?:^|\s)@([\p{L}\p{N}._-]*)$/u.exec(beforeCursor)
  const query = match?.[1].toLocaleLowerCase() || ""
  const suggestions = match ? participants.filter(person => person.name.toLocaleLowerCase().includes(query)).slice(0, 8) : []

  function choose(person: Person) {
    if (!match) return
    const start = cursor - match[0].length + match[0].lastIndexOf("@")
    const replacement = `@${person.name} `
    const next = body.slice(0, start) + replacement + body.slice(cursor)
    const nextCursor = start + replacement.length
    setBody(next)
    setSelected(current => [...new Set([...current, person._id])])
    setCursor(nextCursor)
    setActive(0)
    requestAnimationFrame(() => {
      input.current?.focus()
      input.current?.setSelectionRange(nextCursor, nextCursor)
    })
  }

  function onKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (!suggestions.length) return
    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      event.preventDefault()
      setActive(current => (current + (event.key === "ArrowDown" ? 1 : -1) + suggestions.length) % suggestions.length)
    } else if (event.key === "Enter" || event.key === "Tab") {
      event.preventDefault()
      choose(suggestions[active] || suggestions[0])
    } else if (event.key === "Escape") {
      setCursor(-1)
    }
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!body.trim() || sending) return
    setSending(true)
    const mentions = selected.filter(id => {
      const person = participants.find(value => value._id === id)
      return person && body.includes(`@${person.name}`)
    })
    if (await onAction({ action: "task.comment.create", taskId, body, mentions })) {
      setBody("")
      setSelected([])
      setCursor(0)
    }
    setSending(false)
  }

  return <div className="space-y-3 border-t pt-3">
    <h4 className="text-sm font-medium">Comments {comments.length > 0 && <span className="text-muted-foreground">({comments.length})</span>}</h4>
    {comments.length === 0 && <p className="text-xs text-muted-foreground">No comments yet.</p>}
    <div className="space-y-3">{comments.map(comment => <div key={comment._id} className="rounded-md bg-muted/50 p-3 text-sm"><div className="flex flex-wrap items-baseline gap-2"><strong>{comment.createdBy.name}</strong><time className="text-xs text-muted-foreground">{timeFormat.format(new Date(comment.createdAt))}</time></div><p className="mt-1 whitespace-pre-wrap break-words">{comment.body}</p></div>)}</div>
    {!readOnly && <form onSubmit={submit} className="space-y-2">
      <div className="relative">
        {suggestions.length > 0 && <div role="listbox" aria-label="Mention a participant" className="absolute bottom-full z-20 mb-1 max-h-48 w-full overflow-y-auto rounded-md border bg-popover p-1 shadow-lg">{suggestions.map((person, index) => <button key={person._id} type="button" role="option" aria-selected={index === active} onMouseDown={event => event.preventDefault()} onClick={() => choose(person)} className={`block w-full rounded px-3 py-2 text-left text-sm ${index === active ? "bg-accent text-accent-foreground" : "hover:bg-accent"}`}>{person.name}</button>)}</div>}
        <Textarea ref={input} aria-label="Task comment" placeholder="Comment on this task… Type @ to mention someone" value={body} maxLength={4000} onChange={event => { setBody(event.target.value); setCursor(event.target.selectionStart); setActive(0) }} onClick={event => setCursor(event.currentTarget.selectionStart)} onKeyUp={event => { if (!["ArrowDown", "ArrowUp", "Enter", "Tab"].includes(event.key)) setCursor(event.currentTarget.selectionStart) }} onKeyDown={onKeyDown} className="min-h-20" />
      </div>
      <Button type="submit" size="sm" disabled={sending || !body.trim()}><Send className="mr-2 h-3.5 w-3.5" />{sending ? "Posting…" : "Post comment"}</Button>
    </form>}
  </div>
}
