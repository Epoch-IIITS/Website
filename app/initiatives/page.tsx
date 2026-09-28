"use client"

import { useCallback, useEffect, useState } from "react"
import Link from "next/link"
import { useSession } from "next-auth/react"
import { useRouter } from "next/navigation"
import { Archive, ArrowRight, Layers3, Plus, Search } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { ParticipantPicker } from "@/components/initiatives/participant-picker"
import type { InitiativeSummary, ParticipantDirectory, Person, TeamYearOption } from "@/components/initiatives/types"

export default function InitiativesPage() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const [items, setItems] = useState<InitiativeSummary[]>([])
  const [people, setPeople] = useState<Person[]>([])
  const [teamYears, setTeamYears] = useState<TeamYearOption[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [archive, setArchive] = useState(false)
  const [search, setSearch] = useState("")
  const [open, setOpen] = useState(false)
  const [saving, setSaving] = useState(false)
  const [title, setTitle] = useState("")
  const [participants, setParticipants] = useState<string[]>([])

  const load = useCallback(async () => {
    try {
      const response = await fetch("/api/initiatives", { cache: "no-store" })
      if (!response.ok) throw new Error("Unable to load initiatives")
      setItems(await response.json())
      setError("")
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Unable to load initiatives")
    } finally { setLoading(false) }
  }, [])

  useEffect(() => {
    if (status === "unauthenticated") router.replace("/auth/signin?callbackUrl=/initiatives")
    if (status === "authenticated") {
      load()
      if (session?.user?.role === "admin") {
        fetch("/api/initiatives/people").then(response => response.ok ? response.json() : { people: [], teamYears: [] }).then((directory: ParticipantDirectory) => { setPeople(directory.people); setTeamYears(directory.teamYears) }).catch(() => {})
      }
    }
  }, [status, session?.user?.role, router, load])

  async function create() {
    setSaving(true)
    try {
      const response = await fetch("/api/initiatives", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, participants }),
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.error || "Unable to create initiative")
      router.push(`/initiatives/${data._id}`)
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Unable to create initiative")
    } finally { setSaving(false) }
  }

  const visible = items.filter(item => item.status === (archive ? "completed" : "active") && item.title.toLowerCase().includes(search.toLowerCase()))

  return <div className="mx-auto max-w-7xl space-y-6 px-4 py-8 sm:px-6">
    <div className="flex flex-wrap items-end justify-between gap-4">
      <div><p className="text-xs font-semibold uppercase tracking-widest text-primary">Club workspace</p><h1 className="mt-2 text-3xl font-semibold">Initiatives</h1><p className="mt-2 text-muted-foreground">Keep every plan, task, idea, and conversation together.</p></div>
      {session?.user?.role === "admin" && <Dialog open={open} onOpenChange={value => { setOpen(value); if (value) setError("") }}><DialogTrigger asChild><Button><Plus className="mr-2 h-4 w-4" />New initiative</Button></DialogTrigger><DialogContent className="max-h-[90vh] overflow-y-auto"><DialogHeader><DialogTitle>New initiative</DialogTitle><DialogDescription>Give this workspace a name and invite collaborators.</DialogDescription></DialogHeader>
        <div className="space-y-4"><Input aria-label="Initiative name" placeholder="UG1 Recruitment" value={title} onChange={event => setTitle(event.target.value)} maxLength={120} />
          <div><p className="mb-2 text-sm font-medium">Participants</p><ParticipantPicker people={people} teamYears={teamYears} selected={participants} onSelectionChange={setParticipants} /></div>
          {error && <p role="alert" className="text-sm text-destructive">{error}</p>}
          <Button onClick={create} disabled={saving || !title.trim()} className="w-full">{saving ? "Creating…" : "Create initiative"}</Button>
        </div>
      </DialogContent></Dialog>}
    </div>
    <div className="flex flex-wrap items-center gap-3">
      <Button variant={archive ? "outline" : "default"} onClick={() => setArchive(false)}>Active</Button>
      <Button variant={archive ? "default" : "outline"} onClick={() => setArchive(true)}><Archive className="mr-2 h-4 w-4" />Archive</Button>
      <div className="relative ml-auto w-full sm:w-64"><Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" /><Input className="pl-9" placeholder="Find an initiative" value={search} onChange={event => setSearch(event.target.value)} /></div>
    </div>
    {error && <p role="alert" className="text-sm text-destructive">{error} <Button variant="link" onClick={load}>Retry</Button></p>}
    {loading || status === "loading" ? <p className="text-muted-foreground">Loading initiatives…</p> : visible.length === 0 ? <div className="rounded-xl border border-dashed p-10 text-center text-muted-foreground">{archive ? "No completed initiatives yet." : "No active initiatives found."}</div> : <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">{visible.map(item => <Link key={item._id} href={`/initiatives/${item._id}`} className="group"><Card className="h-full transition-colors group-hover:border-primary/50"><CardHeader><CardTitle className="flex items-center justify-between gap-2 text-lg"><span>{item.title}</span><ArrowRight className="h-4 w-4 shrink-0 text-muted-foreground" /></CardTitle></CardHeader><CardContent><div className="flex flex-wrap gap-2 text-xs"><span className="rounded-full bg-muted px-2 py-1">{item.pendingTasks} pending</span><span className="rounded-full bg-muted px-2 py-1">{item.overdueTasks} overdue</span><span className="rounded-full bg-muted px-2 py-1">{item.unansweredQuestions} open questions</span></div>{item.nextTasks.length > 0 && <div className="mt-4 border-t pt-3"><p className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">Next to do</p><ul className="space-y-1 text-sm">{item.nextTasks.map((task, index) => <li key={index} className="truncate">• {task.title}</li>)}</ul></div>}{item.firstOpenQuestion && <p className="mt-3 line-clamp-2 text-sm text-muted-foreground"><span className="font-medium text-foreground">Open question:</span> {item.firstOpenQuestion}</p>}<div className="mt-5 flex items-center gap-2 text-xs text-muted-foreground"><Layers3 className="h-4 w-4" />{item.participants.length} participants</div></CardContent></Card></Link>)}</div>}
  </div>
}
