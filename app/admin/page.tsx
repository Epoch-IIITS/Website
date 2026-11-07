"use client"

import { useCallback, useEffect, useState } from "react"
import Link from "next/link"
import { ArrowRight, ArrowUpRight, MoreHorizontal, Plus } from "lucide-react"
import { Button } from "@/components/ui/button"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { eventDateParts } from "@/lib/event-dates"
import { cn } from "@/lib/utils"

interface Stats {
  blogs: { total: number; published: number; draft: number }
  projects: { total: number }
  events: { total: number; upcoming: number }
  galleries: { total: number }
  users: { total: number; admins: number }
  rsvps: { total: number; upcoming: number }
  queries: { total: number }
}

interface EventRow { _id: string; title: string; date: string; venue: string }
interface LogRow { _id: string; action: "create" | "update" | "delete"; summary: string; createdAt: string; actor: { name: string } }
interface LearnerRow { id: string; name: string; completed: number }

const today = new Intl.DateTimeFormat("en-IN", { timeZone: "Asia/Kolkata", weekday: "long", day: "numeric", month: "long", year: "numeric" })
const logTime = new Intl.DateTimeFormat("en-IN", { timeZone: "Asia/Kolkata", day: "numeric", month: "short", hour: "numeric", minute: "2-digit", hour12: true })
const actionDot = { create: "bg-success", update: "bg-primary", delete: "bg-orange-600 dark:bg-orange-400" }

async function getJson<T>(url: string): Promise<T> {
  const response = await fetch(url, { cache: "no-store" })
  if (!response.ok) throw new Error(url)
  return response.json()
}

function Panel({ title, action, children, className }: { title: string; action?: React.ReactNode; children: React.ReactNode; className?: string }) {
  return (
    <section className={cn("overflow-hidden rounded-xl border bg-card", className)}>
      <div className="flex items-center justify-between gap-3 border-b border-border/60 px-5 py-4">
        <h2 className="text-base font-semibold">{title}</h2>
        {action}
      </div>
      {children}
    </section>
  )
}

function PanelLink({ href, children }: { href: string; children: React.ReactNode }) {
  return <Link href={href} className="inline-flex items-center gap-1 text-[13px] font-medium text-primary hover:underline">{children}<ArrowRight className="h-3.5 w-3.5" aria-hidden="true" /></Link>
}

function Muted({ children }: { children: React.ReactNode }) {
  return <p className="px-5 py-4 text-sm text-muted-foreground">{children}</p>
}

export default function AdminDashboard() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [events, setEvents] = useState<EventRow[] | null>(null)
  const [logs, setLogs] = useState<LogRow[] | null>(null)
  const [learners, setLearners] = useState<{ learners: LearnerRow[]; total: number } | null>(null)
  const [failed, setFailed] = useState<Set<string>>(new Set())
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    setLoading(true)
    const errors = new Set<string>()
    const settle = <T,>(key: string, promise: Promise<T>, set: (value: T) => void) =>
      promise.then(set).catch(() => { errors.add(key) })
    await Promise.all([
      settle("stats", getJson<Stats>("/api/admin/stats"), setStats),
      settle("events", getJson<EventRow[]>("/api/events"), (rows) => setEvents([...rows].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()))),
      settle("logs", getJson<{ logs: LogRow[] }>("/api/admin/logs?page=1"), (data) => setLogs(data.logs.slice(0, 4))),
      settle("learners", getJson<{ learners: LearnerRow[]; total: number }>("/api/admin/learners"), setLearners),
    ])
    setFailed(errors)
    setLoading(false)
  }, [])
  useEffect(() => { load() }, [load])

  const now = Date.now()
  const upcomingCount = events?.filter((event) => new Date(event.date).getTime() >= now).length ?? 0
  const metrics = [
    { label: "Community members", value: stats?.users.total, detail: stats ? `${stats.users.admins} admins · ${stats.users.total - stats.users.admins} members` : "", href: "/admin/users" },
    { label: "Upcoming events", value: stats?.events.upcoming, detail: stats ? `${stats.rsvps.upcoming} ${stats.rsvps.upcoming === 1 ? "registration" : "registrations"}` : "", href: "/admin/events" },
    { label: "Published stories", value: stats?.blogs.published, detail: stats ? `${stats.blogs.draft} ${stats.blogs.draft === 1 ? "draft" : "drafts"}` : "", href: "/admin/blogs" },
    { label: "Active learners", value: learners?.total, detail: "solved at least one problem", href: "/admin/learners" },
  ]

  return (
    <div className="mx-auto flex max-w-[1280px] flex-col gap-7 px-2 py-2 sm:px-4 lg:py-4">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div className="flex flex-col gap-1.5">
          <h1 className="text-[28px] font-semibold tracking-tight">Overview</h1>
          <span className="text-sm text-muted-foreground">{today.format(new Date())}</span>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" asChild><Link href="/" target="_blank">View site<ArrowUpRight className="h-4 w-4" /></Link></Button>
          <Button asChild><Link href="/admin/events/new"><Plus className="h-4 w-4" />New event</Link></Button>
        </div>
      </div>

      {failed.size > 0 && !loading && (
        <div role="alert" className="flex flex-wrap items-center justify-between gap-3 rounded-xl border bg-card px-5 py-4 text-sm">
          <span className="text-destructive">Some sections could not be loaded.</span>
          <Button variant="outline" size="sm" onClick={load}>Try again</Button>
        </div>
      )}

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {metrics.map(({ label, value, detail, href }) => (
          <Link key={label} href={href} className="flex flex-col gap-1.5 rounded-xl border bg-card px-5 py-[18px] transition-colors hover:border-input focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring">
            <span className="text-[13px] text-muted-foreground">{label}</span>
            {loading ? <span className="my-1 h-8 w-16 animate-pulse rounded bg-muted" /> : <span className="text-[30px] font-semibold leading-tight tracking-tight">{value ?? "—"}</span>}
            <span className="min-h-4 text-xs text-subtle">{detail}</span>
          </Link>
        ))}
      </div>

      <div className="grid items-start gap-4 xl:grid-cols-3">
        <Panel title="Events" action={<PanelLink href="/admin/events">Manage</PanelLink>} className="xl:col-span-2">
          {loading ? <Muted>Loading events…</Muted> : !events ? <Muted>Events could not be loaded.</Muted> : events.length === 0 ? <Muted>No events yet.</Muted> : (
            <div className="overflow-x-auto">
              <table className="w-full min-w-[620px] border-collapse text-sm">
                <thead>
                  <tr className="text-left text-xs text-subtle">
                    <th className="px-5 py-2.5 font-medium">Title</th>
                    <th className="px-3 py-2.5 font-medium">Date</th>
                    <th className="px-3 py-2.5 font-medium">Venue</th>
                    <th className="px-3 py-2.5 font-medium">Status</th>
                    <th className="px-5 py-2.5"><span className="sr-only">Actions</span></th>
                  </tr>
                </thead>
                <tbody>
                  {events.slice(0, 5).map((event) => {
                    const { day, month, year } = eventDateParts(event.date)
                    const upcoming = new Date(event.date).getTime() >= now
                    return (
                      <tr key={event._id} className="border-t border-border/60">
                        <td className="px-5 py-3.5 font-medium">{event.title}</td>
                        <td className="whitespace-nowrap px-3 py-3.5 font-mono text-xs text-muted-foreground">{day} {month} {year}</td>
                        <td className="px-3 py-3.5 text-muted-foreground">{event.venue}</td>
                        <td className="px-3 py-3.5"><span className={cn("rounded-full px-2.5 py-0.5 text-xs font-medium", upcoming ? "bg-primary-soft text-primary" : "bg-secondary text-muted-foreground")}>{upcoming ? "Upcoming" : "Past"}</span></td>
                        <td className="px-5 py-3.5 text-right">
                          <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                              <Button variant="outline" size="icon" className="h-8 w-8" aria-label={`More actions for ${event.title}`}><MoreHorizontal className="h-4 w-4" /></Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end">
                              <DropdownMenuItem asChild><Link href={`/admin/events/${event._id}/edit`}>Edit event</Link></DropdownMenuItem>
                              <DropdownMenuItem asChild><Link href={`/admin/events/${event._id}/rsvps`}>View registrations</Link></DropdownMenuItem>
                              <DropdownMenuItem asChild><Link href={`/events/${event._id}`} target="_blank">Open public page</Link></DropdownMenuItem>
                            </DropdownMenuContent>
                          </DropdownMenu>
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          )}
          {events && (
            <div className="flex flex-wrap items-center justify-between gap-3 border-t border-border/60 bg-muted/40 px-5 py-3.5 text-[13px] text-muted-foreground">
              <span>{upcomingCount === 0 ? "No upcoming events scheduled." : `${upcomingCount} upcoming ${upcomingCount === 1 ? "event" : "events"}.`}</span>
              <Button variant="outline" size="sm" asChild className="h-8"><Link href="/admin/events/new">Schedule one</Link></Button>
            </div>
          )}
        </Panel>

        <div className="flex flex-col gap-4">
          <section className="flex flex-col gap-3 rounded-xl border bg-card px-5 py-4">
            <div className="flex items-center justify-between">
              <h2 className="text-base font-semibold"><Link href="/admin/queries" className="hover:text-primary">Inbox</Link></h2>
              <span className="text-xs text-subtle">{stats ? `${stats.queries.total} ${stats.queries.total === 1 ? "message" : "messages"}` : ""}</span>
            </div>
            <p className="text-sm leading-relaxed text-muted-foreground">Messages sent through the Contact page land here.</p>
          </section>

          <Panel title="Recent activity" action={<PanelLink href="/admin/logs">Log</PanelLink>}>
            {loading ? <Muted>Loading activity…</Muted> : !logs ? <Muted>Activity could not be loaded.</Muted> : logs.length === 0 ? <Muted>No recent activity.</Muted> : (
              <ul>
                {logs.map((log) => (
                  <li key={log._id} className="flex items-start gap-3 border-b border-border/60 px-5 py-3 last:border-b-0">
                    <span className={cn("mt-1.5 h-2 w-2 shrink-0 rounded-full", actionDot[log.action])} aria-hidden="true" />
                    <div className="flex min-w-0 flex-col gap-0.5">
                      <span className="text-sm leading-snug"><strong className="font-semibold">{log.actor.name}</strong> {log.summary.charAt(0).toLowerCase() + log.summary.slice(1)}</span>
                      <span className="text-xs text-subtle">{logTime.format(new Date(log.createdAt))}</span>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </Panel>

          <Panel title="Top learners" action={<PanelLink href="/admin/learners">All</PanelLink>}>
            {loading ? <Muted>Loading learners…</Muted> : !learners ? <Muted>Learners could not be loaded.</Muted> : learners.learners.length === 0 ? <Muted>No passing submissions yet.</Muted> : (
              <ol className="flex flex-col gap-2.5 px-5 py-4">
                {learners.learners.slice(0, 3).map((learner) => (
                  <li key={learner.id} className="flex justify-between gap-3 text-sm">
                    <span className="truncate">{learner.name}</span>
                    <span className="shrink-0 font-mono text-xs text-muted-foreground">{learner.completed} solved</span>
                  </li>
                ))}
              </ol>
            )}
          </Panel>
        </div>
      </div>
    </div>
  )
}
