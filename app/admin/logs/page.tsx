"use client"

import { useDeferredValue, useEffect, useState } from "react"
import { ChevronLeft, ChevronRight, RefreshCw, ScrollText, Search } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { cn } from "@/lib/utils"

type AuditValue = string | number | boolean | null
interface AuditLogEntry {
  _id: string
  operationId: string
  action: "create" | "update" | "delete"
  entityType: string
  entityId: string
  entityLabel: string
  actor: { id: string; name: string; email: string; role: string }
  summary: string
  changes: { field: string; before: AuditValue; after: AuditValue }[]
  sideEffects?: Record<string, string | number | boolean>
  route: string
  method: string
  createdAt: string
}
interface LogsResponse {
  logs: AuditLogEntry[]
  pagination: { page: number; total: number; pages: number; limit: number }
}

const entityOptions = [
  ["blog", "Blogs"],
  ["project", "Projects"],
  ["event", "Events"],
  ["gallery", "Gallery"],
  ["user", "Users"],
  ["contact-query", "Contact queries"],
  ["qr-code", "QR codes"],
  ["team-year", "Team years"],
  ["team-person", "Team people"],
  ["team-appointment", "Team appointments"],
  ["team-settings", "Team settings"],
  ["team-request", "Team requests"],
] as const

const fieldLabels: Record<string, string> = {
  currentYearId: "Current academic year",
  currentRole: "Current role",
  featuredImage: "Featured image",
  cloudinaryImagesQueued: "Cloudinary images queued",
  githubUrl: "GitHub URL",
  liveUrl: "Live URL",
  maxAttendees: "Maximum attendees",
  rsvpDeadline: "RSVP deadline",
  personId: "Person",
  yearId: "Academic year",
  groupId: "Hierarchy group",
  por: "Position of responsibility",
  ctaTitle: "CTA title",
  ctaText: "CTA text",
  contentType: "Content type",
  trackingEnabled: "Tracking enabled",
  foregroundColor: "Foreground colour",
  backgroundColor: "Background colour",
  errorCorrectionLevel: "Error correction",
}

function displayTime(value: string) {
  return new Intl.DateTimeFormat("en-IN", {
    timeZone: "Asia/Kolkata",
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value))
}

function displayValue(value: AuditValue) {
  if (value === null) return "—"
  if (typeof value === "boolean") return value ? "Yes" : "No"
  return String(value)
}

export default function ActivityLogsPage() {
  const [data, setData] = useState<LogsResponse | null>(null)
  const [page, setPage] = useState(1)
  const [action, setAction] = useState("all")
  const [entityType, setEntityType] = useState("all")
  const [search, setSearch] = useState("")
  const deferredSearch = useDeferredValue(search.trim())
  const [from, setFrom] = useState("")
  const [to, setTo] = useState("")
  const [revision, setRevision] = useState(0)
  const [selected, setSelected] = useState<AuditLogEntry | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    const controller = new AbortController()
    async function load() {
      setLoading(true)
      setError("")
      try {
        const params = new URLSearchParams({ page: String(page) })
        if (action !== "all") params.set("action", action)
        if (entityType !== "all") params.set("entityType", entityType)
        if (deferredSearch) params.set("search", deferredSearch)
        if (from) params.set("from", from)
        if (to) params.set("to", to)
        const response = await fetch(`/api/admin/logs?${params}`, {
          cache: "no-store",
          signal: controller.signal,
        })
        const value = await response.json()
        if (!response.ok) {
          throw new Error(
            response.status === 401 || response.status === 403
              ? "Your admin session has expired or access was denied."
              : value.error || "Unable to load activity logs.",
          )
        }
        if (page > Math.max(1, value.pagination.pages)) {
          setPage(Math.max(1, value.pagination.pages))
          return
        }
        setData(value)
      } catch (loadError) {
        if (!controller.signal.aborted) {
          setError(loadError instanceof Error ? loadError.message : "Unable to load activity logs.")
        }
      } finally {
        if (!controller.signal.aborted) setLoading(false)
      }
    }
    load()
    return () => controller.abort()
  }, [action, deferredSearch, entityType, from, page, revision, to])

  function resetFilters() {
    setAction("all")
    setEntityType("all")
    setSearch("")
    setFrom("")
    setTo("")
    setPage(1)
  }

  return (
    <div className="mx-auto max-w-7xl space-y-6 px-4 py-4 sm:px-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight">Activity logs</h1>
          <p className="mt-2 text-muted-foreground">Review administrator changes from the last six months.</p>
        </div>
        <Button variant="outline" disabled={loading} onClick={() => setRevision(value => value + 1)}>
          <RefreshCw className={cn("mr-2 h-4 w-4", loading && "animate-spin")} />Refresh
        </Button>
      </div>

      <section aria-label="Log filters" className="flex flex-wrap items-end gap-4 rounded-xl border bg-card p-4">
        <Label className="min-w-0 flex-[2_1_22rem]">
          Search
          <span className="relative mt-2 block">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input value={search} maxLength={100} onChange={(event) => { setSearch(event.target.value); setPage(1) }} placeholder="Administrator or resource" className="pl-9" />
          </span>
        </Label>
        <Label className="min-w-[13rem] flex-1">
          Action
          <Select value={action} onValueChange={(value) => { setAction(value); setPage(1) }}>
            <SelectTrigger className="mt-2"><SelectValue /></SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All actions</SelectItem>
              <SelectItem value="create">Created</SelectItem>
              <SelectItem value="update">Updated</SelectItem>
              <SelectItem value="delete">Deleted</SelectItem>
            </SelectContent>
          </Select>
        </Label>
        <Label className="min-w-[15rem] flex-1">
          Resource
          <Select value={entityType} onValueChange={(value) => { setEntityType(value); setPage(1) }}>
            <SelectTrigger className="mt-2"><SelectValue /></SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All resources</SelectItem>
              {entityOptions.map(([value, label]) => <SelectItem key={value} value={value}>{label}</SelectItem>)}
            </SelectContent>
          </Select>
        </Label>
        <Label className="min-w-[13rem] flex-1">From<Input className="mt-2 w-full" type="date" value={from} onChange={(event) => { setFrom(event.target.value); setPage(1) }} /></Label>
        <Label className="min-w-[13rem] flex-1">To<Input className="mt-2 w-full" type="date" value={to} onChange={(event) => { setTo(event.target.value); setPage(1) }} /></Label>
        <div className="basis-full"><Button variant="ghost" size="sm" onClick={resetFilters}>Clear filters</Button></div>
      </section>

      {error ? (
        <div role="alert" className="rounded-xl border bg-card p-8"><p className="mb-4 text-destructive">{error}</p><Button variant="outline" onClick={() => setRevision(value => value + 1)}>Try again</Button></div>
      ) : loading ? (
        <div role="status" className="flex min-h-80 items-center justify-center rounded-xl border bg-card text-muted-foreground">Loading activity…</div>
      ) : !data?.logs.length ? (
        <div className="flex min-h-80 flex-col items-center justify-center rounded-xl border bg-card px-6 text-center"><ScrollText className="mb-4 h-10 w-10 text-muted-foreground" /><h2 className="text-lg font-semibold">No matching activity</h2><p className="mt-2 text-sm text-muted-foreground">New administrator changes will appear here.</p></div>
      ) : (
        <div className="overflow-hidden rounded-xl border bg-card">
          <div className="overflow-x-auto">
            <Table>
              <TableHeader><TableRow><TableHead>When</TableHead><TableHead>Action</TableHead><TableHead>Resource</TableHead><TableHead>Administrator</TableHead><TableHead className="text-right">Details</TableHead></TableRow></TableHeader>
              <TableBody>
                {data.logs.map((log) => (
                  <TableRow key={log._id}>
                    <TableCell className="whitespace-nowrap text-sm text-muted-foreground"><time dateTime={log.createdAt}>{displayTime(log.createdAt)}</time></TableCell>
                    <TableCell><Badge variant={log.action === "delete" ? "destructive" : log.action === "create" ? "default" : "secondary"} className="capitalize">{log.action}</Badge></TableCell>
                    <TableCell><p className="font-medium">{log.entityLabel}</p><p className="mt-1 max-w-md text-xs text-muted-foreground">{log.summary}</p></TableCell>
                    <TableCell><p className="text-sm">{log.actor.name}</p><p className="text-xs text-muted-foreground">{log.actor.email}</p></TableCell>
                    <TableCell className="text-right"><Button variant="outline" size="sm" onClick={() => setSelected(log)}>View</Button></TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
          <div className="flex items-center justify-between gap-3 border-t px-5 py-4">
            <p className="text-xs text-muted-foreground">{data.pagination.total} entries · Page {data.pagination.page} of {Math.max(1, data.pagination.pages)}</p>
            <div className="flex gap-2"><Button variant="outline" size="sm" disabled={page <= 1} onClick={() => setPage(value => value - 1)}><ChevronLeft className="mr-1 h-4 w-4" />Previous</Button><Button variant="outline" size="sm" disabled={page >= data.pagination.pages} onClick={() => setPage(value => value + 1)}>Next<ChevronRight className="ml-1 h-4 w-4" /></Button></div>
          </div>
        </div>
      )}

      <Dialog open={selected !== null} onOpenChange={(open) => { if (!open) setSelected(null) }}>
        <DialogContent className="max-h-[85vh] max-w-2xl overflow-y-auto">
          <DialogHeader><DialogTitle>{selected?.summary}</DialogTitle><DialogDescription>{selected && `${displayTime(selected.createdAt)} · ${selected.actor.name} (${selected.actor.email})`}</DialogDescription></DialogHeader>
          {selected && <div className="space-y-5">
            <dl className="grid gap-3 rounded-lg bg-muted/50 p-4 text-sm sm:grid-cols-2"><div><dt className="text-muted-foreground">Resource type</dt><dd className="mt-1">{entityOptions.find(([value]) => value === selected.entityType)?.[1] || selected.entityType}</dd></div><div><dt className="text-muted-foreground">Resource ID</dt><dd className="mt-1 break-all font-mono text-xs">{selected.entityId}</dd></div><div><dt className="text-muted-foreground">Request</dt><dd className="mt-1 font-mono text-xs">{selected.method} {selected.route}</dd></div><div><dt className="text-muted-foreground">Operation ID</dt><dd className="mt-1 break-all font-mono text-xs">{selected.operationId}</dd></div></dl>
            <section><h3 className="mb-3 font-medium">Changes</h3>{selected.changes.length ? <div className="space-y-3">{selected.changes.map((change) => <div key={change.field} className="rounded-lg border p-3"><p className="mb-2 text-sm font-medium">{fieldLabels[change.field] || change.field}</p><div className="grid gap-2 text-xs sm:grid-cols-2"><div><p className="text-muted-foreground">Before</p><p className="mt-1 break-words">{displayValue(change.before)}</p></div><div><p className="text-muted-foreground">After</p><p className="mt-1 break-words">{displayValue(change.after)}</p></div></div></div>)}</div> : <p className="text-sm text-muted-foreground">No field-level details were recorded.</p>}</section>
            {selected.sideEffects && <section><h3 className="mb-3 font-medium">Related changes</h3><dl className="space-y-2 rounded-lg border p-3 text-sm">{Object.entries(selected.sideEffects).map(([key, value]) => <div key={key} className="flex justify-between gap-4"><dt className="text-muted-foreground">{fieldLabels[key] || key}</dt><dd>{String(value)}</dd></div>)}</dl></section>}
          </div>}
        </DialogContent>
      </Dialog>
    </div>
  )
}
