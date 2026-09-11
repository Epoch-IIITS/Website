"use client"

import { FormEvent, useCallback, useEffect, useMemo, useState } from "react"
import Link from "next/link"
import { ArrowLeft, BarChart3, Copy, Download, Link2, Loader2, QrCode, RefreshCw, Trash2, Type } from "lucide-react"
import { toast } from "sonner"
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from "@/components/ui/alert-dialog"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Switch } from "@/components/ui/switch"
import { Textarea } from "@/components/ui/textarea"

interface GeneratedCode {
  _id: string
  name: string
  content: string
  contentType: "url" | "text"
  trackingEnabled: boolean
  foregroundColor: string
  backgroundColor: string
  size: 256 | 512 | 1024
  margin: number
  errorCorrectionLevel: "M" | "H"
  createdAt: string
  imageUrl: string
  trackedUrl: string | null
  analytics: {
    totalScans: number
    uniqueScans: number
    firstScannedAt: string | null
    lastScannedAt: string | null
  }
}

const initialForm = {
  name: "",
  content: "",
  trackingEnabled: false,
  foregroundColor: "#0f172a",
  backgroundColor: "#ffffff",
  size: 512 as 256 | 512 | 1024,
  margin: 2,
  errorCorrectionLevel: "M" as "M" | "H",
}

function isHttpUrl(value: string) {
  try {
    const url = new URL(value)
    return url.protocol === "http:" || url.protocol === "https:"
  } catch {
    return false
  }
}

function formatDate(value: string | null) {
  return value ? new Date(value).toLocaleString() : "Not scanned yet"
}

export default function QRCodeGeneratorPage() {
  const [form, setForm] = useState(initialForm)
  const [qrCodes, setQrCodes] = useState<GeneratedCode[]>([])
  const [latest, setLatest] = useState<GeneratedCode | null>(null)
  const [analyticsCode, setAnalyticsCode] = useState<GeneratedCode | null>(null)
  const [deleteTarget, setDeleteTarget] = useState<GeneratedCode | null>(null)
  const [deleting, setDeleting] = useState(false)
  const [deleteError, setDeleteError] = useState("")
  const [previewDataUrl, setPreviewDataUrl] = useState<string | null>(null)
  const [previewLoading, setPreviewLoading] = useState(false)
  const [previewError, setPreviewError] = useState("")
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState("")
  const contentIsUrl = useMemo(() => isHttpUrl(form.content.trim()), [form.content])
  const hasDraftPreview = form.content.trim().length > 0

  const loadCodes = useCallback(async () => {
    setLoading(true)
    setError("")
    try {
      const response = await fetch("/api/admin/qr-codes", { cache: "no-store" })
      const result = await response.json()
      if (!response.ok) throw new Error(result.error || "Unable to load QR codes")
      setQrCodes(result.qrCodes)
    } catch (error) {
      setError(error instanceof Error ? error.message : "Unable to load QR codes")
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { loadCodes() }, [loadCodes])

  useEffect(() => {
    const content = form.content.trim()
    if (!content) {
      setPreviewDataUrl(null)
      setPreviewError("")
      setPreviewLoading(false)
      return
    }

    let cancelled = false
    setPreviewLoading(true)
    setPreviewError("")
    const timer = window.setTimeout(async () => {
      try {
        const { default: QRCode } = await import("qrcode")
        const payload = form.trackingEnabled && contentIsUrl
          ? `${window.location.origin}/q/PREVIEW_ONLY`
          : content
        const dataUrl = await QRCode.toDataURL(payload, {
          width: Math.min(form.size, 512),
          margin: form.margin,
          errorCorrectionLevel: form.errorCorrectionLevel,
          color: { dark: form.foregroundColor, light: form.backgroundColor },
        })
        if (!cancelled) setPreviewDataUrl(dataUrl)
      } catch {
        if (!cancelled) {
          setPreviewDataUrl(null)
          setPreviewError("Choose valid colors and content to preview the QR code.")
        }
      } finally {
        if (!cancelled) setPreviewLoading(false)
      }
    }, 180)

    return () => {
      cancelled = true
      window.clearTimeout(timer)
    }
  }, [contentIsUrl, form.backgroundColor, form.content, form.errorCorrectionLevel, form.foregroundColor, form.margin, form.size, form.trackingEnabled])

  function updateContent(content: string) {
    setForm(current => ({
      ...current,
      content,
      trackingEnabled: isHttpUrl(content.trim()) ? current.trackingEnabled : false,
    }))
  }

  async function createQRCode(event: FormEvent) {
    event.preventDefault()
    if (saving) return
    setSaving(true)
    setError("")
    try {
      const response = await fetch("/api/admin/qr-codes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      })
      const result = await response.json()
      if (!response.ok) throw new Error(result.error || "Unable to create QR code")
      setQrCodes(current => [result.qrCode, ...current])
      setLatest(result.qrCode)
      setForm(current => ({ ...current, name: "", content: "", trackingEnabled: false }))
      toast.success("QR code created")
    } catch (error) {
      setError(error instanceof Error ? error.message : "Unable to create QR code")
    } finally {
      setSaving(false)
    }
  }

  async function copyTrackedUrl(url: string) {
    try {
      await navigator.clipboard.writeText(url)
      toast.success("Tracked link copied")
    } catch {
      toast.error("Unable to copy the link")
    }
  }

  async function deleteQRCode() {
    if (!deleteTarget || deleting) return
    setDeleting(true)
    setDeleteError("")
    try {
      const response = await fetch(`/api/admin/qr-codes/${deleteTarget._id}`, { method: "DELETE" })
      const result = await response.json()
      if (!response.ok && response.status !== 404) {
        throw new Error(result.error || "Unable to delete the QR code")
      }

      setQrCodes(current => current.filter(code => code._id !== deleteTarget._id))
      setLatest(current => current?._id === deleteTarget._id ? null : current)
      setAnalyticsCode(current => current?._id === deleteTarget._id ? null : current)
      setDeleteTarget(null)
      toast.success(response.status === 404 ? "QR code was already deleted" : "QR code deleted")
    } catch (error) {
      setDeleteError(error instanceof Error ? error.message : "Unable to delete the QR code")
    } finally {
      setDeleting(false)
    }
  }

  return (
    <div className="mx-auto max-w-7xl space-y-8 px-4 py-4 sm:px-6">
      <div>
        <Button variant="ghost" asChild className="mb-3 -ml-3"><Link href="/admin/utilities"><ArrowLeft className="mr-2 h-4 w-4" />Utilities</Link></Button>
        <h1 className="text-3xl font-semibold tracking-tight">QR Code Generator</h1>
        <p className="mt-2 text-muted-foreground">Create downloadable QR codes for links or text. Tracked links report total and estimated unique scans.</p>
      </div>

      <div className="grid items-start gap-6 xl:grid-cols-[minmax(0,1.35fr)_minmax(320px,0.65fr)]">
        <Card>
          <CardHeader><CardTitle>Create QR Code</CardTitle><CardDescription>Enter the content first, then choose optional branding and tracking.</CardDescription></CardHeader>
          <CardContent>
            <form className="space-y-6" onSubmit={createQRCode}>
              <div className="space-y-2">
                <Label htmlFor="qr-name">Name</Label>
                <Input id="qr-name" maxLength={100} required placeholder="Orientation registration" value={form.name} onChange={event => setForm(current => ({ ...current, name: event.target.value }))} />
              </div>
              <div className="space-y-2">
                <div className="flex items-center justify-between gap-3"><Label htmlFor="qr-content">URL or text</Label><Badge variant="outline">{contentIsUrl ? <><Link2 className="mr-1 h-3 w-3" />URL</> : <><Type className="mr-1 h-3 w-3" />Text</>}</Badge></div>
                <Textarea id="qr-content" rows={5} maxLength={2000} required placeholder="https://epoch.iiits.ac.in or any text" value={form.content} onChange={event => updateContent(event.target.value)} />
                <p className="text-xs text-muted-foreground">{form.content.length}/2,000 characters</p>
              </div>

              <div className="rounded-xl border p-4">
                <div className="flex items-start justify-between gap-4">
                  <div><Label htmlFor="qr-tracking" className="text-sm font-medium">Enable scan tracking</Label><p className="mt-1 text-xs leading-5 text-muted-foreground">Available for http and https links. The QR opens a short Epoch link before redirecting.</p></div>
                  <Switch id="qr-tracking" checked={form.trackingEnabled} disabled={!contentIsUrl} onCheckedChange={trackingEnabled => setForm(current => ({ ...current, trackingEnabled }))} aria-describedby="qr-tracking-note" />
                </div>
                <p id="qr-tracking-note" className="sr-only">Tracking records total scans and an estimated unique count without storing raw IP addresses.</p>
              </div>

              <fieldset className="space-y-4 rounded-xl border p-4">
                <legend className="px-2 text-sm font-semibold">Optional branding</legend>
                <div className="grid gap-4 sm:grid-cols-2">
                  <div className="space-y-2"><Label htmlFor="foreground">Foreground</Label><div className="flex gap-2"><Input id="foreground" type="color" className="w-14 shrink-0 p-1" value={form.foregroundColor} onChange={event => setForm(current => ({ ...current, foregroundColor: event.target.value }))} /><Input aria-label="Foreground hex color" value={form.foregroundColor} maxLength={7} onChange={event => setForm(current => ({ ...current, foregroundColor: event.target.value }))} /></div></div>
                  <div className="space-y-2"><Label htmlFor="background">Background</Label><div className="flex gap-2"><Input id="background" type="color" className="w-14 shrink-0 p-1" value={form.backgroundColor} onChange={event => setForm(current => ({ ...current, backgroundColor: event.target.value }))} /><Input aria-label="Background hex color" value={form.backgroundColor} maxLength={7} onChange={event => setForm(current => ({ ...current, backgroundColor: event.target.value }))} /></div></div>
                  <div className="space-y-2"><Label>Image size</Label><Select value={String(form.size)} onValueChange={value => setForm(current => ({ ...current, size: Number(value) as 256 | 512 | 1024 }))}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent><SelectItem value="256">256 × 256</SelectItem><SelectItem value="512">512 × 512</SelectItem><SelectItem value="1024">1024 × 1024</SelectItem></SelectContent></Select></div>
                  <div className="space-y-2"><Label>Error correction</Label><Select value={form.errorCorrectionLevel} onValueChange={(value: "M" | "H") => setForm(current => ({ ...current, errorCorrectionLevel: value }))}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent><SelectItem value="M">Standard</SelectItem><SelectItem value="H">High</SelectItem></SelectContent></Select></div>
                  <div className="space-y-2 sm:col-span-2"><Label htmlFor="margin">Quiet-zone margin: {form.margin}</Label><Input id="margin" type="range" min={0} max={8} value={form.margin} onChange={event => setForm(current => ({ ...current, margin: Number(event.target.value) }))} /></div>
                </div>
                <p className="text-xs text-muted-foreground">Use a dark foreground on a light background and test branded codes before printing.</p>
              </fieldset>

              {error && <p role="alert" className="text-sm text-destructive">{error}</p>}
              <Button type="submit" disabled={saving} className="w-full sm:w-auto">{saving ? <><Loader2 className="mr-2 h-4 w-4 animate-spin" />Creating…</> : <><QrCode className="mr-2 h-4 w-4" />Create QR Code</>}</Button>
            </form>
          </CardContent>
        </Card>

        <Card className="xl:sticky xl:top-24">
          <CardHeader><CardTitle>QR preview</CardTitle><CardDescription>{hasDraftPreview ? (form.name.trim() || "Unsaved preview") : latest ? latest.name : "Enter content to preview your QR code."}</CardDescription></CardHeader>
          <CardContent>
            {hasDraftPreview ? <div className="space-y-4">
              <div className="relative flex aspect-square items-center justify-center overflow-hidden rounded-xl border bg-white p-4">
                {previewDataUrl && <img src={previewDataUrl} alt="Live QR code preview" className="h-full w-full object-contain" />}
                {previewLoading && <div role="status" className="absolute inset-0 flex items-center justify-center bg-white/80 text-slate-600"><Loader2 className="mr-2 h-5 w-5 animate-spin" />Updating preview…</div>}
                {!previewLoading && previewError && <p role="alert" className="px-6 text-center text-sm text-red-600">{previewError}</p>}
              </div>
              <div className="rounded-lg bg-muted p-3 text-sm text-muted-foreground">
                {form.trackingEnabled && contentIsUrl ? "This preview uses a sample tracked link. The final link is assigned when you create the QR code." : "Preview only. Create the QR code to save and download it."}
              </div>
            </div> : latest ? <div className="space-y-4">
              <div className="flex aspect-square items-center justify-center overflow-hidden rounded-xl border bg-white p-4"><img src={latest.imageUrl} alt={`QR code for ${latest.name}`} className="h-full w-full object-contain" /></div>
              {latest.trackedUrl && <div className="rounded-lg bg-muted p-3"><p className="mb-1 text-xs font-medium text-muted-foreground">Tracked link</p><p className="break-all text-sm">{latest.trackedUrl}</p></div>}
              <div className="grid gap-2 sm:grid-cols-2 xl:grid-cols-1 2xl:grid-cols-2">
                <Button asChild><a href={`${latest.imageUrl}?download=1`}><Download className="mr-2 h-4 w-4" />Download PNG</a></Button>
                {latest.trackedUrl && <Button variant="outline" onClick={() => copyTrackedUrl(latest.trackedUrl!)}><Copy className="mr-2 h-4 w-4" />Copy link</Button>}
              </div>
            </div> : <div className="flex aspect-square flex-col items-center justify-center rounded-xl border border-dashed px-8 text-center text-muted-foreground"><QrCode className="mb-4 h-16 w-16 opacity-30" /><p className="text-sm">Start typing a URL or text to see the preview.</p></div>}
          </CardContent>
        </Card>
      </div>

      <section aria-labelledby="saved-codes-title" className="space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3"><div><h2 id="saved-codes-title" className="text-2xl font-semibold tracking-tight">Saved QR codes</h2><p className="mt-1 text-sm text-muted-foreground">The latest 100 codes are shown.</p></div><Button variant="outline" onClick={loadCodes} disabled={loading}><RefreshCw className={`mr-2 h-4 w-4 ${loading ? "animate-spin" : ""}`} />Refresh</Button></div>
        {loading ? <div role="status" className="flex min-h-40 items-center justify-center rounded-xl border bg-card text-muted-foreground">Loading QR codes…</div> : error && !qrCodes.length ? <div role="alert" className="rounded-xl border bg-card p-6 text-destructive">{error}</div> : !qrCodes.length ? <div className="flex min-h-40 items-center justify-center rounded-xl border bg-card text-muted-foreground">No QR codes created yet.</div> : (
          <div className="divide-y overflow-hidden rounded-xl border bg-card">
            {qrCodes.map(code => <article key={code._id} className="grid gap-4 p-5 md:grid-cols-[minmax(0,1fr)_auto] md:items-center">
              <div className="min-w-0"><div className="flex flex-wrap items-center gap-2"><h3 className="truncate font-semibold">{code.name}</h3><Badge variant="outline">{code.contentType === "url" ? "URL" : "Text"}</Badge>{code.trackingEnabled && <Badge>Tracked</Badge>}</div><p className="mt-2 truncate text-sm text-muted-foreground">{code.content}</p><p className="mt-2 text-xs text-muted-foreground">Created {new Date(code.createdAt).toLocaleString()}</p></div>
              <div className="flex flex-wrap items-center gap-2">
                {code.trackingEnabled && <div className="mr-2 flex gap-4 text-sm"><span><strong className="tabular-nums">{code.analytics.totalScans}</strong> total</span><span><strong className="tabular-nums">{code.analytics.uniqueScans}</strong> unique</span></div>}
                <Button variant="outline" size="sm" asChild><a href={`${code.imageUrl}?download=1`}><Download className="mr-2 h-4 w-4" />PNG</a></Button>
                <Button variant="outline" size="sm" disabled={!code.trackingEnabled} onClick={() => setAnalyticsCode(code)}><BarChart3 className="mr-2 h-4 w-4" />Analytics</Button>
                <Button variant="outline" size="sm" className="text-destructive hover:bg-destructive/10 hover:text-destructive" onClick={() => { setDeleteError(""); setDeleteTarget(code) }}><Trash2 className="mr-2 h-4 w-4" />Delete</Button>
              </div>
            </article>)}
          </div>
        )}
      </section>

      <Dialog open={analyticsCode !== null} onOpenChange={open => { if (!open) setAnalyticsCode(null) }}>
        <DialogContent>
          <DialogHeader><DialogTitle>{analyticsCode?.name}</DialogTitle><DialogDescription>Scan activity for this tracked QR code. Unique scans are privacy-preserving estimates.</DialogDescription></DialogHeader>
          {analyticsCode && <div className="space-y-5">
            <div className="grid grid-cols-3 gap-3"><div className="rounded-xl border p-4"><p className="text-xs text-muted-foreground">Total</p><p className="mt-2 text-2xl font-semibold tabular-nums">{analyticsCode.analytics.totalScans}</p></div><div className="rounded-xl border p-4"><p className="text-xs text-muted-foreground">Unique</p><p className="mt-2 text-2xl font-semibold tabular-nums">{analyticsCode.analytics.uniqueScans}</p></div><div className="rounded-xl border p-4"><p className="text-xs text-muted-foreground">Repeats</p><p className="mt-2 text-2xl font-semibold tabular-nums">{Math.max(0, analyticsCode.analytics.totalScans - analyticsCode.analytics.uniqueScans)}</p></div></div>
            <dl className="space-y-3 text-sm"><div className="flex items-start justify-between gap-4"><dt className="text-muted-foreground">First scan</dt><dd className="text-right">{formatDate(analyticsCode.analytics.firstScannedAt)}</dd></div><div className="flex items-start justify-between gap-4"><dt className="text-muted-foreground">Latest scan</dt><dd className="text-right">{formatDate(analyticsCode.analytics.lastScannedAt)}</dd></div></dl>
            {analyticsCode.trackedUrl && <Button variant="outline" className="w-full" onClick={() => copyTrackedUrl(analyticsCode.trackedUrl!)}><Copy className="mr-2 h-4 w-4" />Copy tracked link</Button>}
          </div>}
        </DialogContent>
      </Dialog>

      <AlertDialog open={deleteTarget !== null} onOpenChange={open => { if (!open && !deleting) setDeleteTarget(null) }}>
        <AlertDialogContent onEscapeKeyDown={event => { if (deleting) event.preventDefault() }}>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete this QR code?</AlertDialogTitle>
            <AlertDialogDescription>
              “{deleteTarget?.name}” and all of its scan analytics will be permanently deleted. Its tracked link will stop working immediately.
            </AlertDialogDescription>
          </AlertDialogHeader>
          {deleteError && <p role="alert" className="text-sm text-destructive">{deleteError}</p>}
          <AlertDialogFooter>
            <AlertDialogCancel disabled={deleting}>Cancel</AlertDialogCancel>
            <AlertDialogAction disabled={deleting} className="bg-destructive text-destructive-foreground hover:bg-destructive/90" onClick={event => { event.preventDefault(); deleteQRCode() }}>
              {deleting ? "Deleting…" : "Delete QR code"}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}
