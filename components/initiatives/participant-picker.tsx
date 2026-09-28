"use client"

import { useState } from "react"
import { Plus, Search, Users } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import type { Person, TeamYearOption } from "./types"

type Props = {
  people: Person[]
  teamYears?: TeamYearOption[]
  selected: string[]
  onSelectionChange: (ids: string[]) => void
}

export function ParticipantPicker({ people, teamYears = [], selected, onSelectionChange }: Props) {
  const [query, setQuery] = useState("")
  const [yearId, setYearId] = useState("")
  const year = teamYears.find(item => item._id === yearId) || teamYears[0]
  const search = query.trim().toLocaleLowerCase()
  const matches = people.filter(person =>
    person.name.toLocaleLowerCase().includes(search)
    || person.email?.toLocaleLowerCase().includes(search),
  )

  return <div className="space-y-4">
    {year && <section className="space-y-2 rounded-md border p-3" aria-label="Add from Team">
      <div className="flex flex-wrap items-center justify-between gap-2"><div><h3 className="flex items-center gap-2 text-sm font-medium"><Users className="h-4 w-4" />Add from Team</h3><p className="text-xs text-muted-foreground">Select a committee to add its members with accounts.</p></div><select aria-label="Academic year" value={year._id} onChange={event => setYearId(event.target.value)} className="h-9 rounded-md border bg-background px-2 text-sm">{teamYears.map(item => <option key={item._id} value={item._id}>AY {item.year}{item.published ? "" : " (draft)"}</option>)}</select></div>
      <div className="max-h-44 space-y-1 overflow-y-auto">{year.groups.map(group => {
        const remaining = group.userIds.filter(id => !selected.includes(id))
        return <div key={group.id} className="flex items-center justify-between gap-2 rounded-md bg-muted/40 px-2 py-2"><div className="min-w-0"><p className="truncate text-sm font-medium">{group.name}</p><p className="text-xs text-muted-foreground">{group.userIds.length} with accounts{group.unlinkedCount ? ` · ${group.unlinkedCount} without accounts` : ""}</p></div><Button type="button" size="sm" variant="outline" disabled={remaining.length === 0} onClick={() => onSelectionChange([...new Set([...selected, ...group.userIds])])}><Plus className="mr-1 h-3.5 w-3.5" />{remaining.length ? `Add ${remaining.length}` : group.userIds.length ? "Added" : "No accounts"}</Button></div>
      })}{year.groups.length === 0 && <p className="text-sm text-muted-foreground">No committees in this academic year.</p>}</div>
    </section>}
    <div className="space-y-2"><p className="text-sm font-medium">Find an account</p>
    <div className="relative">
      <Search className="pointer-events-none absolute left-3 top-3 h-4 w-4 text-muted-foreground" aria-hidden="true" />
      <Input
        aria-label="Search participants by name or email"
        placeholder="Search by name or email"
        className="pl-9"
        value={query}
        onChange={event => setQuery(event.target.value)}
      />
    </div>
    <p className="text-xs text-muted-foreground" aria-live="polite">
      {matches.length} {matches.length === 1 ? "person" : "people"} found · {selected.length} selected
    </p>
    <div className="max-h-40 space-y-1 overflow-y-auto rounded-md border p-2">
      {matches.length ? matches.map(person => <label key={person._id} className="flex cursor-pointer items-center gap-2 rounded p-2 text-sm hover:bg-muted">
        <input
          type="checkbox"
          checked={selected.includes(person._id)}
          onChange={event => onSelectionChange(event.target.checked
            ? [...new Set([...selected, person._id])]
            : selected.filter(id => id !== person._id))}
        />
        <span>{person.name}{person.email && <span className="text-muted-foreground"> ({person.email})</span>}</span>
      </label>) : <p className="p-2 text-sm text-muted-foreground">No matching people.</p>}
    </div></div>
  </div>
}
