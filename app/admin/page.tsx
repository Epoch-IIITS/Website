"use client"

import { useState, useEffect, useCallback } from "react"
import Link from "next/link"
import { Calendar, Users, Inbox, FileText, ArrowRight, Plus, FolderOpen, ImageIcon } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

interface Stats {
  blogs: { total: number; published: number; draft: number }
  projects: { total: number }
  events: { total: number; upcoming: number }
  galleries: { total: number }
  users: { total: number }
  rsvps: { total: number }
  queries: { total: number }
}

export default function AdminDashboard() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const load = useCallback(async () => {
    setLoading(true)
    setError("")
    try {
      const response = await fetch("/api/admin/stats", { cache: "no-store" })
      if (!response.ok) throw new Error("Unable to load the overview. Please try again.")
      setStats(await response.json())
    } catch (error) {
      setError(error instanceof Error ? error.message : "Unable to load the overview.")
    } finally { setLoading(false) }
  }, [])
  useEffect(() => { load() }, [load])

  const metrics = stats ? [
    { label: "Community members", value: stats.users.total, detail: "Registered accounts", icon: Users, href: "/admin/users" },
    { label: "Upcoming events", value: stats.events.upcoming, detail: `${stats.rsvps.total} total registrations`, icon: Calendar, href: "/admin/events" },
    { label: "Published stories", value: stats.blogs.published, detail: `${stats.blogs.draft} drafts in progress`, icon: FileText, href: "/admin/blogs" },
    { label: "Contact queries", value: stats.queries.total, detail: "Messages from the community", icon: Inbox, href: "/admin/queries" },
  ] : []
  const content = stats ? [
    { title: "Blogs", detail: "Stories, updates, and ideas", count: stats.blogs.total, icon: FileText, href: "/admin/blogs" },
    { title: "Projects", detail: "What the community is building", count: stats.projects.total, icon: FolderOpen, href: "/admin/projects" },
    { title: "Events", detail: "Workshops, meetups, and registrations", count: stats.events.total, icon: Calendar, href: "/admin/events" },
    { title: "Gallery", detail: "Moments from your events", count: stats.galleries.total, icon: ImageIcon, href: "/admin/gallery" },
  ] : []

  return (
    <div className="mx-auto max-w-7xl space-y-8 px-4 py-4 sm:px-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div><p className="mb-2 text-xs font-semibold uppercase tracking-widest text-muted-foreground">Your club at a glance</p><h1 className="text-3xl font-semibold tracking-tight">Overview</h1><p className="mt-2 text-muted-foreground">Keep the community informed, connected, and heard.</p></div>
        <Button asChild><Link href="/admin/events/new"><Plus className="mr-2 h-4 w-4" />Create event</Link></Button>
      </div>
      {error ? <div role="alert" className="rounded-xl border bg-background p-6"><p className="mb-4 text-destructive">{error}</p><Button variant="outline" onClick={load}>Try again</Button></div> : loading ? (
        <div role="status" aria-label="Loading overview" className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">{[1, 2, 3, 4].map(n => <div key={n} className="h-40 animate-pulse rounded-xl border bg-muted" />)}</div>
      ) : stats && <>
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {metrics.map(({ label, value, detail, icon: Icon, href }) => <Link key={label} href={href} className="rounded-xl border bg-card p-5 transition-colors hover:border-primary/50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring">
            <div className="flex items-center justify-between gap-2 text-sm text-muted-foreground"><span>{label}</span><Icon className="h-4 w-4" /></div>
            <p className="my-3 text-4xl font-semibold tracking-tight">{value}</p><p className="text-xs text-muted-foreground">{detail}</p>
          </Link>)}
        </div>
        <div className="grid items-start gap-6 xl:grid-cols-3">
          <Card className="xl:col-span-2">
            <CardHeader><CardTitle className="text-lg">Content library</CardTitle><CardDescription>Manage everything your members see.</CardDescription></CardHeader>
            <CardContent className="divide-y">
              {content.map(({ title, detail, count, icon: Icon, href }) => <Link key={title} href={href} className="flex items-center gap-4 rounded-md py-5 transition-colors hover:bg-muted/50">
                <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-muted"><Icon className="h-5 w-5 text-muted-foreground" /></span>
                <div className="min-w-0 flex-1"><p className="font-medium">{title}</p><p className="text-sm text-muted-foreground">{detail}</p></div>
                <span className="text-sm tabular-nums text-muted-foreground">{count}</span><ArrowRight className="h-4 w-4 shrink-0 text-muted-foreground" />
              </Link>)}
            </CardContent>
          </Card>
          <Card className="border-primary/20 bg-primary/5">
            <CardHeader><Inbox className="mb-4 h-7 w-7 text-primary" /><CardTitle className="text-xl">Listen to your community</CardTitle><CardDescription>Questions, collaboration requests, and ideas sent through Contact Us arrive here.</CardDescription></CardHeader>
            <CardContent><p className="mb-6 text-sm"><span className="font-semibold">{stats.queries.total}</span> {stats.queries.total === 1 ? "message" : "messages"} received</p><Button asChild className="w-full justify-between"><Link href="/admin/queries">Open contact queries<ArrowRight className="h-4 w-4" /></Link></Button></CardContent>
          </Card>
        </div>
      </>}
    </div>
  )
}
