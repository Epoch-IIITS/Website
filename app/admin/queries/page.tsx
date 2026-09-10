"use client"

import { useEffect, useState } from "react"
import { Inbox, RefreshCw, ChevronLeft, ChevronRight, Mail } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface ContactQuery {
  _id: string
  firstName: string
  lastName: string
  email: string
  subject: string
  message: string
  createdAt: string
}
interface InboxData {
  queries: ContactQuery[]
  pagination: { page: number; total: number; pages: number }
}

export default function ContactQueriesPage() {
  const [data, setData] = useState<InboxData | null>(null)
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [page, setPage] = useState(1)
  const [revision, setRevision] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    const controller = new AbortController()
    setLoading(true)
    setError("")
    async function load() {
      try {
        const response = await fetch(`/api/admin/queries?page=${page}`, { signal: controller.signal, cache: "no-store" })
        if (!response.ok) throw new Error(response.status === 401 || response.status === 403 ? "Your admin session has expired or access was denied. Please sign in again." : "Unable to load messages. Please try again.")
        const result: InboxData = await response.json()
        if (controller.signal.aborted) return
        setData(result)
        setSelectedId(current => result.queries.some(query => query._id === current) ? current : result.queries[0]?._id || null)
      } catch (error) {
        if (!controller.signal.aborted) setError(error instanceof Error ? error.message : "Unable to load messages.")
      } finally {
        if (!controller.signal.aborted) setLoading(false)
      }
    }
    load()
    return () => controller.abort()
  }, [page, revision])

  const selected = data?.queries.find(query => query._id === selectedId)
  return (
    <div className="mx-auto max-w-7xl space-y-6 px-4 py-4 sm:px-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div><h1 className="text-3xl font-semibold tracking-tight">Contact queries</h1><p className="mt-2 text-muted-foreground">Read questions and ideas submitted through Contact Us.</p></div>
        <Button variant="outline" disabled={loading} onClick={() => setRevision(value => value + 1)}><RefreshCw className={cn("mr-2 h-4 w-4", loading && "animate-spin")} />Refresh</Button>
      </div>
      {error ? <div role="alert" className="rounded-xl border bg-card p-8"><p className="mb-4 text-destructive">{error}</p><Button variant="outline" onClick={() => setRevision(value => value + 1)}>Try again</Button></div> : loading ? (
        <div role="status" className="flex min-h-80 items-center justify-center rounded-xl border bg-card text-muted-foreground">Loading messages…</div>
      ) : !data?.queries.length ? (
        <div className="flex min-h-80 flex-col items-center justify-center rounded-xl border bg-card px-6 text-center"><Inbox className="mb-4 h-10 w-10 text-muted-foreground" /><h2 className="text-lg font-semibold">No messages yet</h2><p className="mt-2 max-w-sm text-sm text-muted-foreground">New submissions from the Contact Us page will appear here.</p></div>
      ) : (
        <div className="overflow-hidden rounded-xl border bg-card">
          <div className="flex items-center justify-between border-b px-5 py-4"><h2 className="text-sm font-semibold">Inbox <span className="ml-2 rounded-full bg-muted px-2 py-0.5 text-xs text-muted-foreground">{data.pagination.total}</span></h2><span className="text-xs text-muted-foreground">Newest first</span></div>
          <div className="grid lg:min-h-[540px] lg:grid-cols-[340px_minmax(0,1fr)]">
            <nav aria-label="Contact messages" className="max-h-72 divide-y overflow-y-auto border-b lg:max-h-[650px] lg:border-b-0 lg:border-r">
              {data.queries.map(query => <button key={query._id} onClick={() => setSelectedId(query._id)} aria-pressed={selectedId === query._id} aria-controls="query-detail" className={cn("block w-full border-l-2 p-5 text-left transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-ring", selectedId === query._id ? "border-l-primary bg-primary/5" : "border-l-transparent hover:bg-muted/50")}>
                <div className="mb-2 flex items-center justify-between gap-3"><p className="truncate text-sm font-semibold">{query.firstName} {query.lastName}</p><time dateTime={query.createdAt} className="shrink-0 text-[11px] text-muted-foreground">{new Date(query.createdAt).toLocaleDateString(undefined, { month: "short", day: "numeric" })}</time></div>
                <p className="truncate text-sm font-medium">{query.subject}</p><p className="mt-1 line-clamp-2 break-words text-xs leading-relaxed text-muted-foreground">{query.message}</p>
              </button>)}
            </nav>
            <article id="query-detail" aria-label="Selected message" className="min-w-0 p-6 sm:p-8" aria-live="polite">
              {selected && <>
                <p className="mb-3 text-xs font-medium uppercase tracking-widest text-muted-foreground">Contact submission</p>
                <h2 className="break-words text-2xl font-semibold tracking-tight">{selected.subject}</h2>
                <div className="my-6 flex flex-wrap items-start gap-3 border-b pb-6">
                  <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-muted text-sm font-semibold">{selected.firstName.charAt(0)}{selected.lastName.charAt(0)}</span>
                  <div className="min-w-0"><p className="break-words text-sm font-semibold">{selected.firstName} {selected.lastName}</p><p className="mt-1 flex items-start gap-2 break-all text-sm text-muted-foreground"><Mail className="mt-0.5 h-4 w-4 shrink-0" />{selected.email}</p><time dateTime={selected.createdAt} className="mt-2 block text-xs text-muted-foreground">{new Date(selected.createdAt).toLocaleString()}</time></div>
                </div>
                <p className="whitespace-pre-wrap break-words text-sm leading-7">{selected.message}</p>
              </>}
            </article>
          </div>
          <div className="flex items-center justify-between gap-3 border-t px-5 py-4">
            <p className="text-xs text-muted-foreground">Page {data.pagination.page} of {data.pagination.pages}</p>
            <div className="flex gap-2"><Button variant="outline" size="sm" disabled={page <= 1} onClick={() => setPage(value => value - 1)}><ChevronLeft className="mr-1 h-4 w-4" />Previous</Button><Button variant="outline" size="sm" disabled={page >= data.pagination.pages} onClick={() => setPage(value => value + 1)}>Next<ChevronRight className="ml-1 h-4 w-4" /></Button></div>
          </div>
        </div>
      )}
    </div>
  )
}
