"use client"

import { useState } from "react"
import Link from "next/link"
import { Calendar, MapPin } from "lucide-react"
import { cn } from "@/lib/utils"

export interface PastEvent {
  _id: string
  title: string
  description: string
  venue: string
  image?: string
  day: string
  month: string
  year: string
  when: string
}

/** Past events grouped by year, with the selected event's details beside the list on wide screens. */
export function PastEvents({ events }: { events: PastEvent[] }) {
  const [selectedId, setSelectedId] = useState(events[0]?._id)
  const current = events.find((event) => event._id === selectedId) ?? events[0]
  if (!current) return null

  return (
    <div className="grid items-start gap-8 md:grid-cols-2">
      <ul className="flex flex-col gap-2">
        {events.map((event, index) => {
          const showYear = index === 0 || events[index - 1].year !== event.year
          const selected = event._id === current._id
          const dateBox = (
            <span className="flex h-16 flex-col items-center justify-center rounded-[10px] border bg-background font-mono">
              <span className="text-xl font-medium">{event.day}</span>
              <span className="text-[11px] text-muted-foreground">{event.month}</span>
            </span>
          )
          const text = (
            <span className="flex min-w-0 flex-col gap-1">
              <span className="text-base font-semibold">{event.title}</span>
              <span className="truncate text-[13px] text-muted-foreground">{event.venue}</span>
            </span>
          )
          const row = "grid w-full grid-cols-[64px_minmax(0,1fr)] items-center gap-4 rounded-xl border p-4 text-left transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          return (
            <li key={event._id} className="flex flex-col">
              {showYear && <span className="px-1 pb-1 pt-4 font-mono text-xs text-muted-foreground">{event.year}</span>}
              <button
                type="button"
                onClick={() => setSelectedId(event._id)}
                aria-pressed={selected}
                className={cn(row, "hidden md:grid", selected ? "border-foreground bg-card" : "border-transparent hover:bg-card")}
              >
                {dateBox}{text}
              </button>
              <Link href={`/events/${event._id}`} className={cn(row, "border-transparent hover:bg-card md:hidden")}>
                {dateBox}{text}
              </Link>
            </li>
          )
        })}
      </ul>

      <aside aria-live="polite" className="sticky top-24 hidden overflow-hidden rounded-2xl border bg-card md:block">
        {current.image ? (
          <img src={current.image} alt={`Photo from ${current.title}`} className="block aspect-video w-full object-cover" />
        ) : (
          <div aria-hidden="true" className="flex aspect-video w-full flex-col items-center justify-center gap-1 bg-secondary font-mono text-muted-foreground">
            <span className="text-[56px] text-foreground">{current.day}</span>
            <span className="text-[13px]">{current.month} {current.year}</span>
          </div>
        )}
        <div className="flex flex-col gap-4 p-7">
          <span className="self-start rounded-full bg-secondary px-2.5 py-1 text-xs font-medium text-muted-foreground">Ended</span>
          <h3 className="text-[26px] font-semibold leading-tight tracking-tight">{current.title}</h3>
          <div className="flex flex-col gap-2 text-sm text-muted-foreground">
            <span className="flex items-center gap-2"><Calendar className="h-4 w-4 shrink-0" aria-hidden="true" />{current.when}</span>
            <span className="flex items-center gap-2"><MapPin className="h-4 w-4 shrink-0" aria-hidden="true" />{current.venue}</span>
          </div>
          <p className="line-clamp-[8] whitespace-pre-line text-[15px] leading-relaxed text-foreground/85">{current.description}</p>
          <Link href={`/events/${current._id}`} className="inline-flex h-[42px] items-center self-start rounded-[10px] bg-primary px-4 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90">Event details</Link>
        </div>
      </aside>
    </div>
  )
}
