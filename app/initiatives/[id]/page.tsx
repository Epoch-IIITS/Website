"use client"

import { useCallback, useEffect, useState } from "react"
import Link from "next/link"
import { useParams, useRouter } from "next/navigation"
import { useSession } from "next-auth/react"
import { Archive, ArrowLeft, RotateCcw, Settings2, Trash2, Users } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { InitiativeTodo } from "@/components/initiatives/todo"
import { InitiativeCanvas } from "@/components/initiatives/canvas"
import { ParticipantPicker } from "@/components/initiatives/participant-picker"
import type { InitiativeDetail, ParticipantDirectory, Person, TeamYearOption } from "@/components/initiatives/types"

export default function InitiativePage() {
  const { id } = useParams<{ id: string }>()
  const router = useRouter()
  const { status } = useSession()
  const [data, setData] = useState<InitiativeDetail | null>(null)
  const [people, setPeople] = useState<Person[]>([])
  const [teamYears, setTeamYears] = useState<TeamYearOption[]>([])
  const [selected, setSelected] = useState<string[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [peopleOpen, setPeopleOpen] = useState(false)
  const [deleting, setDeleting] = useState(false)

  const load = useCallback(async () => {
    try {
      const response = await fetch(`/api/initiatives/${id}`, { cache: "no-store" })
      const result = await response.json()
      if (!response.ok) throw new Error(result.error || "Unable to load initiative")
      setData(result)
      setError("")
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Unable to load initiative")
    } finally { setLoading(false) }
  }, [id])

  useEffect(() => {
    if (status === "unauthenticated") router.replace(`/auth/signin?callbackUrl=/initiatives/${id}`)
    if (status === "authenticated") load()
  }, [status, router, id, load])

  useEffect(() => {
    if (status !== "authenticated") return
    const timer = window.setInterval(load, 15000)
    return () => window.clearInterval(timer)
  }, [status, load])

  useEffect(() => {
    if (peopleOpen && data?.actor.admin) {
      fetch("/api/initiatives/people").then(response => response.ok ? response.json() : { people: [], teamYears: [] }).then((directory: ParticipantDirectory) => { setPeople(directory.people); setTeamYears(directory.teamYears) }).catch(() => {})
    }
  }, [peopleOpen, data?.actor.admin])

  async function act(payload: object) {
    try {
      const response = await fetch(`/api/initiatives/${id}`, {
        method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload),
      })
      const result = await response.json()
      if (!response.ok) throw new Error(result.error || "Unable to save change")
      await load()
      return true
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Unable to save change")
      return false
    }
  }

  async function removeInitiative() {
    if (!data || !window.confirm(`Permanently delete “${data.initiative.title}” and all its tasks, comments, and canvas content?`)) return
    setDeleting(true)
    try {
      const response = await fetch(`/api/initiatives/${id}`, { method: "DELETE" })
      const result = await response.json()
      if (!response.ok) throw new Error(result.error || "Unable to delete initiative")
      router.push("/initiatives")
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Unable to delete initiative")
      setDeleting(false)
    }
  }

  if (loading || status === "loading") return <div className="mx-auto max-w-7xl px-4 py-10 text-muted-foreground">Loading initiative…</div>
  if (!data) return <div className="mx-auto max-w-7xl px-4 py-10"><p role="alert" className="mb-4 text-destructive">{error || "Initiative unavailable"}</p><Button asChild variant="outline"><Link href="/initiatives">Back to initiatives</Link></Button></div>
  const { initiative, tasks, comments, blocks, replies, actor } = data
  const readOnly = initiative.status === "completed"

  return <div className="mx-auto w-full max-w-[1920px] space-y-3 px-3 py-4 sm:px-5">
    <div className="flex flex-wrap items-center justify-between gap-3 border-b pb-3">
      <div><h1 className="sr-only">{initiative.title}</h1><Link href="/initiatives" className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground"><ArrowLeft className="h-4 w-4" />All initiatives</Link></div>
      <DropdownMenu>
        <DropdownMenuTrigger asChild><Button size="icon" variant="outline" aria-label="Initiative settings"><Settings2 className="h-4 w-4" /></Button></DropdownMenuTrigger>
        <DropdownMenuContent align="end" className="min-w-52">
          <DropdownMenuLabel>Initiative settings</DropdownMenuLabel>
          <DropdownMenuItem onSelect={() => { setSelected(initiative.participants.map(person => person._id)); setPeopleOpen(true) }}><Users className="mr-2 h-4 w-4" />People ({initiative.participants.length})</DropdownMenuItem>
          {actor.admin && <><DropdownMenuSeparator /><DropdownMenuItem onSelect={() => void act({ action: "status", status: readOnly ? "active" : "completed" })}>{readOnly ? <RotateCcw className="mr-2 h-4 w-4" /> : <Archive className="mr-2 h-4 w-4" />}{readOnly ? "Reopen" : "Complete & archive"}</DropdownMenuItem><DropdownMenuSeparator /><DropdownMenuItem disabled={deleting} className="text-destructive focus:text-destructive" onSelect={() => void removeInitiative()}><Trash2 className="mr-2 h-4 w-4" />{deleting ? "Deleting…" : "Delete initiative"}</DropdownMenuItem></>}
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
    <Dialog open={peopleOpen} onOpenChange={setPeopleOpen}><DialogContent className="max-h-[90vh] overflow-y-auto"><DialogHeader><DialogTitle>Participants</DialogTitle><DialogDescription>People who can open and contribute to this initiative.</DialogDescription></DialogHeader>
      {actor.admin && !readOnly ? <><ParticipantPicker people={people} teamYears={teamYears} selected={selected} onSelectionChange={setSelected} /><Button onClick={async () => { if (await act({ action: "participants", participants: selected })) setPeopleOpen(false) }}>Save participants</Button></> : <ul className="space-y-2 text-sm">{initiative.participants.map(person => <li key={person._id}>{person.name}</li>)}</ul>}
    </DialogContent></Dialog>
    {error && <div role="alert" className="flex items-center gap-3 rounded-md border border-destructive/40 bg-destructive/5 px-4 py-2 text-sm text-destructive"><span>{error}</span><Button variant="link" size="sm" onClick={load}>Reload</Button></div>}
    {readOnly && <div className="rounded-md border bg-muted px-4 py-3 text-sm text-muted-foreground">This initiative is archived and read only. An admin can reopen it.</div>}
    <div className="grid min-w-0 gap-4 lg:grid-cols-[minmax(280px,320px)_minmax(0,1fr)]">
      <aside aria-label="Initiative tasks" className="max-h-[42vh] min-w-0 overflow-y-auto rounded-xl border bg-card/50 p-3 lg:h-[calc(100vh-170px)] lg:max-h-none lg:min-h-[520px]"><InitiativeTodo compact tasks={tasks} comments={comments} participants={initiative.participants} actor={actor} readOnly={readOnly} onAction={act} /></aside>
      <main className="min-w-0"><InitiativeCanvas embedded initiativeId={id} blocks={blocks} replies={replies} participants={initiative.participants} actor={actor} readOnly={readOnly} onAction={act} onRefresh={load} /></main>
    </div>
  </div>
}
