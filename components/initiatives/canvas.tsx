"use client"

import { useEffect, useRef, useState, type PointerEvent } from "react"
import { Grip, Image as ImageIcon, Maximize2, MessageCircleQuestion, RefreshCw, StickyNote, ZoomIn, ZoomOut } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import type { InitiativeBlock, InitiativeReply, Person } from "./types"
import { validateImageUpload } from "@/lib/image-upload"

type Props = { initiativeId: string; blocks: InitiativeBlock[]; replies: InitiativeReply[]; participants: Person[]; actor: { id: string; admin: boolean }; readOnly: boolean; embedded?: boolean; onAction: (payload: object) => Promise<boolean>; onRefresh: () => Promise<void> }
type View = { x: number; y: number; zoom: number }
type Gesture = { kind: "pan"; x: number; y: number; originX: number; originY: number } | { kind: "card"; id: string; x: number; y: number; originX: number; originY: number } | { kind: "resize"; id: string; x: number; y: number; width: number; height: number }

function growTextarea(element: HTMLTextAreaElement) {
  element.style.height = "auto"
  element.style.height = `${Math.min(element.scrollHeight, Math.round(window.innerHeight * 0.45))}px`
}

export function InitiativeCanvas({ initiativeId, blocks, replies, participants, actor, readOnly, embedded = false, onAction, onRefresh }: Props) {
  const viewport = useRef<HTMLDivElement>(null)
  const editorInput = useRef<HTMLTextAreaElement>(null)
  const gesture = useRef<Gesture | null>(null)
  const [view, setView] = useState<View>({ x: 100, y: 80, zoom: 1 })
  const [positions, setPositions] = useState<Record<string, { x: number; y: number }>>({})
  const [sizes, setSizes] = useState<Record<string, { width: number; height: number }>>({})
  const [editorOpen, setEditorOpen] = useState(false)
  const [editing, setEditing] = useState<InitiativeBlock | null>(null)
  const [type, setType] = useState<InitiativeBlock["type"]>("note")
  const [title, setTitle] = useState("")
  const [content, setContent] = useState("")
  const [url, setUrl] = useState("")
  const [taggedUsers, setTaggedUsers] = useState<string[]>([])
  const [saving, setSaving] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [uploadError, setUploadError] = useState("")
  const [drafts, setDrafts] = useState<Record<string, string>>({})

  useEffect(() => {
    if (editorOpen && type === "question" && editorInput.current) growTextarea(editorInput.current)
  }, [editorOpen, type, content])

  function openEditor(kind: InitiativeBlock["type"], block: InitiativeBlock | null = null) {
    setEditing(block)
    setType(kind)
    setTitle(block?.title || "")
    setContent(block?.content || "")
    setUrl(block?.url || "")
    setTaggedUsers(block?.taggedUsers.map(person => person._id) || [])
    setUploadError("")
    setEditorOpen(true)
  }

  async function save() {
    setSaving(true)
    const rect = viewport.current?.getBoundingClientRect()
    const x = editing?.x ?? Math.round(((rect?.width || 800) / 2 - view.x) / view.zoom - 170 + blocks.length * 25)
    const y = editing?.y ?? Math.round(((rect?.height || 600) / 2 - view.y) / view.zoom - 100 + blocks.length * 25)
    const payload = editing
      ? { action: "block.update", id: editing._id, version: editing.version, title, content, url, taggedUsers, x: positions[editing._id]?.x ?? x, y: positions[editing._id]?.y ?? y }
      : { action: "block.create", type, title, content, url, taggedUsers, x, y }
    if (await onAction(payload)) setEditorOpen(false)
    setSaving(false)
  }
  async function remove() {
    if (!editing || !window.confirm(`Delete this ${editing.type} card and its replies?`)) return
    setSaving(true)
    if (await onAction({ action: "block.delete", id: editing._id })) setEditorOpen(false)
    setSaving(false)
  }

  async function upload(file: File) {
    const validation = validateImageUpload(file)
    if (validation) { setUploadError(validation.error); return }
    setUploading(true)
    setUploadError("")
    try {
      const form = new FormData()
      form.append("file", file)
      const response = await fetch(`/api/initiatives/${initiativeId}/upload`, { method: "POST", body: form })
      const result = await response.json().catch(() => null)
      if (!response.ok || typeof result?.url !== "string") throw new Error(result?.error || "Unable to upload image")
      setUrl(result.url)
    } catch (cause) {
      setUploadError(cause instanceof Error ? cause.message : "Unable to upload image")
    } finally { setUploading(false) }
  }

  function startPan(event: PointerEvent<HTMLDivElement>) {
    if (event.target !== event.currentTarget) return
    gesture.current = { kind: "pan", x: event.clientX, y: event.clientY, originX: view.x, originY: view.y }
    event.currentTarget.setPointerCapture(event.pointerId)
  }
  function movePan(event: PointerEvent<HTMLDivElement>) {
    const active = gesture.current
    if (active?.kind === "pan") setView(current => ({ ...current, x: active.originX + event.clientX - active.x, y: active.originY + event.clientY - active.y }))
  }
  function startCard(event: PointerEvent<HTMLDivElement>, block: InitiativeBlock) {
    if (readOnly) return
    const position = positions[block._id] || { x: block.x, y: block.y }
    gesture.current = { kind: "card", id: block._id, x: event.clientX, y: event.clientY, originX: position.x, originY: position.y }
    event.currentTarget.setPointerCapture(event.pointerId)
  }
  function moveCard(event: PointerEvent<HTMLDivElement>) {
    const active = gesture.current
    if (active?.kind === "card") setPositions(current => ({ ...current, [active.id]: { x: active.originX + (event.clientX - active.x) / view.zoom, y: active.originY + (event.clientY - active.y) / view.zoom } }))
  }
  async function endCard(event: PointerEvent<HTMLDivElement>, block: InitiativeBlock) {
    const active = gesture.current
    gesture.current = null
    if (active?.kind !== "card" || active.id !== block._id) return
    const nextX = Math.round(active.originX + (event.clientX - active.x) / view.zoom)
    const nextY = Math.round(active.originY + (event.clientY - active.y) / view.zoom)
    if (nextX === Math.round(active.originX) && nextY === Math.round(active.originY)) return
    const ok = await onAction({ action: "block.update", id: block._id, version: block.version, title: block.title, content: block.content, url: block.url, taggedUsers: block.taggedUsers.map(person => person._id), x: nextX, y: nextY })
    if (ok) setPositions(current => { const next = { ...current }; delete next[block._id]; return next })
  }
  function startResize(event: PointerEvent<HTMLButtonElement>, block: InitiativeBlock) {
    if (readOnly) return
    event.stopPropagation()
    const rect = event.currentTarget.parentElement?.getBoundingClientRect()
    const current = sizes[block._id]
    gesture.current = { kind: "resize", id: block._id, x: event.clientX, y: event.clientY, width: current?.width ?? block.width ?? Math.round((rect?.width || 340) / view.zoom), height: current?.height ?? block.height ?? Math.round((rect?.height || 190) / view.zoom) }
    event.currentTarget.setPointerCapture(event.pointerId)
  }
  function resizeDimensions(event: PointerEvent<HTMLButtonElement>, active: Extract<Gesture, { kind: "resize" }>) {
    return {
      width: Math.max(240, Math.min(900, Math.round(active.width + (event.clientX - active.x) / view.zoom))),
      height: Math.max(160, Math.min(800, Math.round(active.height + (event.clientY - active.y) / view.zoom))),
    }
  }
  function moveResize(event: PointerEvent<HTMLButtonElement>) {
    const active = gesture.current
    if (active?.kind === "resize") setSizes(current => ({ ...current, [active.id]: resizeDimensions(event, active) }))
  }
  async function endResize(event: PointerEvent<HTMLButtonElement>, block: InitiativeBlock) {
    const active = gesture.current
    gesture.current = null
    if (active?.kind !== "resize" || active.id !== block._id) return
    const nextSize = resizeDimensions(event, active)
    const clearPreview = () => setSizes(current => { const next = { ...current }; delete next[block._id]; return next })
    if (nextSize.width === active.width && nextSize.height === active.height) { clearPreview(); return }
    const position = positions[block._id] || { x: block.x, y: block.y }
    await onAction({ action: "block.update", id: block._id, version: block.version, title: block.title, content: block.content, url: block.url, taggedUsers: block.taggedUsers.map(person => person._id), x: position.x, y: position.y, ...nextSize })
    clearPreview()
  }
  function zoom(factor: number) {
    const rect = viewport.current?.getBoundingClientRect()
    const cx = (rect?.width || 800) / 2
    const cy = (rect?.height || 600) / 2
    setView(current => {
      const next = Math.min(2, Math.max(0.4, current.zoom * factor))
      return { zoom: next, x: cx - (cx - current.x) * next / current.zoom, y: cy - (cy - current.y) * next / current.zoom }
    })
  }

  return <div className={embedded ? "min-w-0 space-y-2" : "space-y-3 py-4"}>
    <div className="flex flex-wrap items-center justify-between gap-2"><div><h2 className={embedded ? "text-lg font-semibold" : "text-xl font-semibold"}>Canvas</h2>{!embedded && <p className="text-sm text-muted-foreground">Drag empty space to pan. Drag a card header to arrange ideas; drag its lower-right corner to resize it.</p>}</div><div className="flex flex-wrap items-center gap-2">{!readOnly && <><Button size="sm" variant="outline" onClick={() => openEditor("note")}><StickyNote className="mr-1 h-4 w-4" />Note</Button><Button size="sm" variant="outline" onClick={() => openEditor("question")}><MessageCircleQuestion className="mr-1 h-4 w-4" />Question board</Button><Button size="sm" variant="outline" onClick={() => openEditor("reference")}><ImageIcon className="mr-1 h-4 w-4" />Reference</Button></>}<Button size="icon" variant="outline" aria-label="Refresh canvas" onClick={async () => { setPositions({}); setSizes({}); await onRefresh() }}><RefreshCw className="h-4 w-4" /></Button></div></div>
    <div className="flex items-center gap-2"><Button size="icon" variant="outline" aria-label="Zoom out" onClick={() => zoom(0.8)}><ZoomOut className="h-4 w-4" /></Button><span className="w-14 text-center text-sm tabular-nums">{Math.round(view.zoom * 100)}%</span><Button size="icon" variant="outline" aria-label="Zoom in" onClick={() => zoom(1.25)}><ZoomIn className="h-4 w-4" /></Button><Button size="sm" variant="ghost" onClick={() => setView({ x: 100, y: 80, zoom: 1 })}><Maximize2 className="mr-1 h-4 w-4" />Reset view</Button></div>
    <div ref={viewport} onPointerDown={startPan} onPointerMove={movePan} onPointerUp={() => { if (gesture.current?.kind === "pan") gesture.current = null }} className={`relative min-h-[480px] overflow-hidden rounded-xl border bg-muted/20 touch-none ${embedded ? "h-[65vh] lg:h-[calc(100vh-240px)] lg:min-h-[520px]" : "h-[70vh]"}`} style={{ backgroundImage: "radial-gradient(circle, hsl(var(--muted-foreground) / .18) 1px, transparent 1px)", backgroundSize: "24px 24px" }}>
      <div className="absolute left-0 top-0" style={{ transform: `translate(${view.x}px, ${view.y}px) scale(${view.zoom})`, transformOrigin: "0 0" }}>
        {blocks.map(block => {
          const position = positions[block._id] || { x: block.x, y: block.y }
          const size = sizes[block._id]
          const height = size?.height ?? block.height
          const ownReplies = replies.filter(reply => reply.block === block._id)
          return <Card key={block._id} className="absolute flex flex-col shadow-md" style={{ left: position.x, top: position.y, width: size?.width ?? block.width ?? 340, height }}>
            <CardHeader onPointerDown={event => startCard(event, block)} onPointerMove={moveCard} onPointerUp={event => endCard(event, block)} onPointerCancel={() => { gesture.current = null }} className={`flex cursor-grab select-none flex-row items-start justify-between gap-2 space-y-0 border-b p-3 ${readOnly ? "cursor-default" : "active:cursor-grabbing"}`}><div className="flex items-center gap-2"><span className="rounded bg-muted p-1">{block.type === "note" ? <StickyNote className="h-4 w-4" /> : block.type === "question" ? <MessageCircleQuestion className="h-4 w-4" /> : <ImageIcon className="h-4 w-4" />}</span><CardTitle className="text-sm">{block.title || (block.type === "question" ? "Question board" : block.type === "note" ? "Note" : "Reference")}</CardTitle></div>{!readOnly && <Button size="sm" variant="ghost" onPointerDown={event => event.stopPropagation()} onClick={() => openEditor(block.type, block)}>Edit</Button>}</CardHeader>
            <CardContent className={`p-3 pb-7 ${height && block.type === "question" ? "flex min-h-0 flex-1 flex-col gap-3 overflow-y-auto" : height ? "min-h-0 flex-1 space-y-3 overflow-y-auto" : "space-y-3"}`}><p className="whitespace-pre-wrap break-words text-sm">{block.content}</p>{block.url && <><a href={block.url} target="_blank" rel="noopener noreferrer" className="block truncate text-sm text-primary underline">{block.url}</a>{/\.(png|jpe?g|webp|gif)(\?.*)?$/i.test(block.url) && <img src={block.url} alt={block.title || "Reference image"} className="max-h-40 w-full rounded-md object-contain" />}</>}
              {block.taggedUsers.length > 0 && <div className="flex flex-wrap gap-1">{block.taggedUsers.map(person => <span key={person._id} className="rounded-full bg-muted px-2 py-1 text-xs">@{person.name}</span>)}</div>}
              {block.type === "question" && <div className={`${height ? "flex min-h-0 flex-1 flex-col gap-2" : "space-y-2"} border-t pt-3`}><p className="shrink-0 text-xs font-semibold uppercase tracking-wide text-muted-foreground">Suggestions · {ownReplies.length}</p><div className={`${height ? "min-h-0 flex-1" : "max-h-40"} space-y-2 overflow-y-auto`}>{ownReplies.map(reply => <div key={reply._id} className="rounded-md bg-muted p-2 text-sm"><span className="font-medium">{reply.createdBy.name}: </span><span className="whitespace-pre-wrap break-words">{reply.body}</span></div>)}</div>{!readOnly && <form onSubmit={async event => { event.preventDefault(); const input = event.currentTarget.querySelector("textarea"); const body = drafts[block._id]?.trim(); if (body && await onAction({ action: "reply.create", blockId: block._id, body })) { setDrafts(current => ({ ...current, [block._id]: "" })); if (input) input.style.height = "auto" } }} className="flex shrink-0 flex-col gap-2"><Textarea aria-label={`Suggest an idea for ${block.title || "question"}`} placeholder="Add a suggestion…" value={drafts[block._id] || ""} onChange={event => setDrafts(current => ({ ...current, [block._id]: event.target.value }))} onInput={event => growTextarea(event.currentTarget)} maxLength={4000} rows={4} className="min-h-24 max-h-[45vh] resize-y" /><Button size="sm" className="self-end" disabled={!drafts[block._id]?.trim()}>Post suggestion</Button></form>}</div>}
            </CardContent>
            {!readOnly && <button type="button" aria-label={`Resize ${block.title || block.type} card`} onPointerDown={event => startResize(event, block)} onPointerMove={moveResize} onPointerUp={event => endResize(event, block)} onPointerCancel={() => { gesture.current = null; setSizes(current => { const next = { ...current }; delete next[block._id]; return next }) }} className="absolute bottom-1 right-1 flex h-7 w-7 touch-none items-center justify-center rounded text-muted-foreground hover:bg-muted hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring cursor-nwse-resize"><Grip className="h-4 w-4" /></button>}
          </Card>
        })}
      </div>
      {blocks.length === 0 && <div className="pointer-events-none absolute inset-0 flex items-center justify-center text-center text-sm text-muted-foreground">This canvas is empty. Add a note, question board, or reference to start.</div>}
    </div>
    <Dialog open={editorOpen} onOpenChange={setEditorOpen}><DialogContent className="max-h-[90vh] overflow-y-auto"><DialogHeader><DialogTitle>{editing ? "Edit" : "Add"} {type === "question" ? "question board" : type}</DialogTitle><DialogDescription>{type === "question" ? "Ask for ideas; participants can reply with suggestions on the canvas." : type === "reference" ? "Share a link or image reference and give it context." : "Share a note everyone can edit."}</DialogDescription></DialogHeader><div className="space-y-4"><Input aria-label="Card title" placeholder={type === "question" ? "Suggest ideas for the event" : "Title"} value={title} onChange={event => setTitle(event.target.value)} maxLength={160} /><Textarea ref={editorInput} aria-label={type === "question" ? "Question" : "Content"} placeholder={type === "question" ? "What would you like the team to suggest?" : "Add context…"} value={content} onChange={event => setContent(event.target.value)} maxLength={10000} className={type === "question" ? "min-h-40 max-h-[45vh] resize-y" : "min-h-28"} />{type === "reference" && <><Input type="url" aria-label="Reference URL" placeholder="https://…" value={url} onChange={event => setUrl(event.target.value)} /><label className="block text-sm font-medium">Or upload an image (4 MB max)<input type="file" accept="image/jpeg,image/png,image/gif,image/webp" className="mt-2 block w-full text-sm" disabled={uploading} onChange={event => { const file = event.target.files?.[0]; if (file) upload(file) }} /></label>{uploadError && <p role="alert" className="text-sm text-destructive">{uploadError}</p>}{url && /\.(png|jpe?g|webp|gif)(\?.*)?$/i.test(url) && <img src={url} alt="Reference preview" className="max-h-32 rounded object-contain" />}</>}
      {type === "reference" && <div><p className="mb-2 text-sm font-medium">Tag participants</p><div className="max-h-32 space-y-1 overflow-y-auto rounded-md border p-2">{participants.map(person => <label key={person._id} className="flex items-center gap-2 rounded p-1 text-sm"><input type="checkbox" checked={taggedUsers.includes(person._id)} onChange={event => setTaggedUsers(current => event.target.checked ? [...current, person._id] : current.filter(id => id !== person._id))} />{person.name}</label>)}</div></div>}
      <div className="flex gap-2">{editing && (actor.admin || editing.createdBy === actor.id) && <Button variant="destructive" onClick={remove} disabled={saving || uploading}>Delete</Button>}<Button onClick={save} disabled={saving || uploading || (type === "question" && !content.trim()) || (type === "reference" && !url.trim())} className="flex-1">{saving ? "Saving…" : "Save card"}</Button></div>
    </div></DialogContent></Dialog>
  </div>
}
