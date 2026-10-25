"use client"

import { useEffect, useState } from "react"
import { GraduationCap, RefreshCw } from "lucide-react"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { cn } from "@/lib/utils"

interface Learner {
  id: string
  name: string
  email: string
  image: string | null
  batch: string | null
  completed: number
  lastSolvedAt: string
}
interface LearnersData {
  learners: Learner[]
  batches: string[]
  total: number
}

function initials(name: string) {
  return name.split(/\s+/).filter(Boolean).slice(0, 2).map(part => part.charAt(0).toUpperCase()).join("") || "?"
}

export default function LearnersPage() {
  const [batch, setBatch] = useState("all")
  const [data, setData] = useState<LearnersData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [revision, setRevision] = useState(0)

  useEffect(() => {
    const controller = new AbortController()
    setLoading(true)
    setError("")
    const query = batch === "all" ? "" : `?batch=${batch}`
    fetch(`/api/admin/learners${query}`, { signal: controller.signal, cache: "no-store" })
      .then(async response => {
        if (!response.ok) throw new Error(response.status === 401 ? "Your admin session has expired or access was denied. Please sign in again." : "Unable to load learners. Please try again.")
        return response.json() as Promise<LearnersData>
      })
      .then(result => { if (!controller.signal.aborted) setData(result) })
      .catch(caught => { if (!controller.signal.aborted) setError(caught instanceof Error ? caught.message : "Unable to load learners.") })
      .finally(() => { if (!controller.signal.aborted) setLoading(false) })
    return () => controller.abort()
  }, [batch, revision])

  return (
    <div className="mx-auto max-w-7xl space-y-6 px-4 py-4 sm:px-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight">Learners</h1>
          <p className="mt-2 text-muted-foreground">Members who have solved at least one Learn problem through Submit.</p>
        </div>
        <div className="flex items-center gap-2">
          <Select value={batch} onValueChange={setBatch}>
            <SelectTrigger className="w-44" aria-label="Filter by batch"><SelectValue /></SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All learners</SelectItem>
              {data?.batches.map(value => <SelectItem key={value} value={value}>Batch {value}</SelectItem>)}
              {batch !== "all" && !data?.batches.includes(batch) && <SelectItem value={batch}>Batch {batch}</SelectItem>}
            </SelectContent>
          </Select>
          <Button variant="outline" disabled={loading} onClick={() => setRevision(value => value + 1)}><RefreshCw className={cn("mr-2 h-4 w-4", loading && "animate-spin")} />Refresh</Button>
        </div>
      </div>

      {error ? (
        <div role="alert" className="rounded-xl border bg-card p-8"><p className="mb-4 text-destructive">{error}</p><Button variant="outline" onClick={() => setRevision(value => value + 1)}>Try again</Button></div>
      ) : loading && !data ? (
        <div role="status" className="flex min-h-80 items-center justify-center rounded-xl border bg-card text-muted-foreground">Loading learners…</div>
      ) : !data?.learners.length ? (
        <div className="flex min-h-80 flex-col items-center justify-center rounded-xl border bg-card px-6 text-center">
          <GraduationCap className="mb-4 h-10 w-10 text-muted-foreground" />
          <h2 className="text-lg font-semibold">{batch === "all" ? "No learners yet" : `No learners in batch ${batch}`}</h2>
          <p className="mt-2 max-w-sm text-sm text-muted-foreground">People appear here after their first passing submission on /learn.</p>
        </div>
      ) : (
        <div className="overflow-hidden rounded-xl border bg-card">
          <div className="flex items-center justify-between border-b px-5 py-4">
            <h2 className="text-sm font-semibold">{batch === "all" ? "All learners" : `Batch ${batch}`} <span className="ml-2 rounded-full bg-muted px-2 py-0.5 text-xs text-muted-foreground">{data.learners.length}</span></h2>
            <span className="text-xs text-muted-foreground">Most problems completed first{batch !== "all" && ` · ${data.total} learners in all batches`}</span>
          </div>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-14"><span className="sr-only">Avatar</span></TableHead>
                <TableHead>Name</TableHead>
                <TableHead>Email</TableHead>
                <TableHead className="text-right">Problems completed</TableHead>
                <TableHead className="hidden text-right md:table-cell">Last solved</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {data.learners.map(learner => (
                <TableRow key={learner.id}>
                  <TableCell>
                    <Avatar className="h-9 w-9">
                      {learner.image && <AvatarImage src={learner.image} alt="" referrerPolicy="no-referrer" />}
                      <AvatarFallback className="text-xs">{initials(learner.name)}</AvatarFallback>
                    </Avatar>
                  </TableCell>
                  <TableCell className="font-medium">{learner.name}</TableCell>
                  <TableCell className="break-all text-muted-foreground">{learner.email}</TableCell>
                  <TableCell className="text-right tabular-nums font-semibold">{learner.completed}</TableCell>
                  <TableCell className="hidden text-right text-muted-foreground md:table-cell"><time dateTime={learner.lastSolvedAt}>{new Date(learner.lastSolvedAt).toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" })}</time></TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  )
}
