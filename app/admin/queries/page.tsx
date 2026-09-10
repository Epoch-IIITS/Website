"use client"

import { useEffect, useRef, useState } from "react"
import { Inbox, RefreshCw, ChevronLeft, ChevronRight, Mail, Trash2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { AlertDialog, AlertDialogContent, AlertDialogHeader, AlertDialogTitle, AlertDialogDescription, AlertDialogFooter, AlertDialogCancel, AlertDialogAction } from "@/components/ui/alert-dialog"
import { toast } from "sonner"
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
  const [deleteTarget, setDeleteTarget] = useState<ContactQuery | null>(null)
  const [deleting, setDeleting] = useState(false)
  const [deleteError, setDeleteError] = useState("")
  const inboxHeading = useRef<HTMLHeadingElement>(null)

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
        if (page > Math.max(1, result.pagination.pages)) {
          setPage(Math.max(1, result.pagination.pages))
          return
        }
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

  async function deleteQuery() {
    if (!deleteTarget || deleting) return
    setDeleting(true)
    setDeleteError("")
    try {
      const response = await fetch(`/api/admin/queries/${deleteTarget._id}`, { method: "DELETE" })
      if (!response.ok && response.status !== 404) {
        throw new Error(response.status === 401 || response.status === 403
          ? "Your admin session has expired or access was denied. Please sign in again."
          : "Unable to delete the query. Please try again.")
      }
      if (response.status === 404) toast.info("This query was already deleted.")
      else toast.success("Query deleted")
      setDeleteTarget(null)
      setRevision(value => value + 1)
    } catch (error) {
      setDeleteError(error instanceof Error ? error.message : "Unable to delete the query.")
    } finally {
      setDeleting(false)
    }
  }
  return (
    <div className="mx-auto max-w-7xl space-y-6 px-4 py-4 sm:px-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div><h1 ref={inboxHeading} tabIndex={-1} className="text-3xl font-semibold tracking-tight">Contact queries</h1><p className="mt-2 text-muted-foreground">Read questions and ideas submitted through Contact Us.</p></div>
        <Button variant="outline" disabled={loading || deleting} onClick={() => setRevision(value => value + 1)}><RefreshCw className={cn("mr-2 h-4 w-4", loading && "animate-spin")} />Refresh</Button>
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
                <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
                  <p className="text-xs font-medium uppercase tracking-widest text-muted-foreground">Contact submission</p>
                  <Button variant="outline" size="sm" className="text-destructive hover:bg-destructive/10 hover:text-destructive" onClick={() => { setDeleteTarget(selected); setDeleteError("") }}>
                    <Trash2 className="mr-2 h-4 w-4" />Delete query
                  </Button>
                </div>
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
      <AlertDialog open={deleteTarget !== null} onOpenChange={open => { if (!open && !deleting) setDeleteTarget(null) }}>
        <AlertDialogContent onEscapeKeyDown={event => { if (deleting) event.preventDefault() }} onCloseAutoFocus={event => { event.preventDefault(); inboxHeading.current?.focus({ preventScroll: true }) }}>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete this query?</AlertDialogTitle>
            <AlertDialogDescription className="break-words">This will permanently delete “{deleteTarget?.subject}” from {deleteTarget?.firstName} {deleteTarget?.lastName}. This action cannot be undone.</AlertDialogDescription>
          </AlertDialogHeader>
          {deleteError && <p role="alert" className="text-sm text-destructive">{deleteError}</p>}
          <AlertDialogFooter>
            <AlertDialogCancel disabled={deleting}>Cancel</AlertDialogCancel>
            <AlertDialogAction disabled={deleting} className="bg-destructive text-destructive-foreground hover:bg-destructive/90" onClick={event => { event.preventDefault(); deleteQuery() }}>{deleting ? "Deleting…" : "Delete query"}</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}
