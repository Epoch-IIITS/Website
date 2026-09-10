"use client"

import { useRef, useState } from "react"
import Image from "next/image"
import { ChevronLeft, ChevronRight, ImageOff } from "lucide-react"
import GalleryImage from "@/components/GalleryImage"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogDescription, DialogTitle } from "@/components/ui/dialog"

interface EventPhoto {
  url: string
  caption?: string
}

function FullPhoto({ photo, alt }: { photo: EventPhoto; alt: string }) {
  const [failed, setFailed] = useState(false)
  return (
    <div className="relative min-h-0 flex-1 overflow-hidden rounded-md bg-black">
      {failed || !photo.url ? (
        <div role="status" className="flex h-full flex-col items-center justify-center gap-3 p-6 text-center text-white/70">
          <ImageOff className="h-8 w-8" />
          <p>This image couldn’t be loaded. You can still browse the other photos.</p>
        </div>
      ) : (
        <Image src={photo.url} alt={alt} fill sizes="96vw" className="object-contain" onError={() => setFailed(true)} unoptimized />
      )}
    </div>
  )
}

export function EventGallery({ images, eventName }: { images: EventPhoto[]; eventName: string }) {
  const [activeIndex, setActiveIndex] = useState<number | null>(null)
  const opener = useRef<HTMLButtonElement | null>(null)
  const activePhoto = activeIndex === null ? undefined : images[activeIndex]

  function move(direction: number) {
    if (images.length < 2) return
    setActiveIndex(index => index === null ? null : (index + direction + images.length) % images.length)
  }

  return (
    <>
      <div className="columns-1 gap-4 space-y-4 md:columns-2 lg:columns-3">
        {images.map((photo, index) => (
          <button
            key={`${photo.url}-${index}`}
            type="button"
            aria-label={`Open photo ${index + 1} of ${images.length}${photo.caption ? `: ${photo.caption}` : ""}`}
            aria-haspopup="dialog"
            className="group block w-full break-inside-avoid overflow-hidden rounded-lg border bg-card text-left transition-shadow hover:shadow-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            onClick={event => {
              opener.current = event.currentTarget
              setActiveIndex(index)
            }}
          >
            <GalleryImage src={photo.url || "/placeholder.svg"} alt={photo.caption || `${eventName} — photo ${index + 1}`} aspect="aspect-[4/3]" />
            {photo.caption && <span className="block p-4 text-sm leading-relaxed text-muted-foreground">{photo.caption}</span>}
          </button>
        ))}
      </div>

      <Dialog open={activePhoto !== undefined} onOpenChange={open => { if (!open) setActiveIndex(null) }}>
        <DialogContent
          className="flex h-[90dvh] w-[96vw] max-w-[1440px] flex-col gap-4 rounded-lg p-4 sm:p-6"
          onCloseAutoFocus={event => {
            event.preventDefault()
            opener.current?.focus({ preventScroll: true })
          }}
          onKeyDown={event => {
            if (event.altKey || event.ctrlKey || event.metaKey) return
            if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
              event.preventDefault()
              move(event.key === "ArrowLeft" ? -1 : 1)
            }
          }}
        >
          <div className="shrink-0 pr-8">
            <DialogTitle className="truncate leading-normal">{eventName}</DialogTitle>
            <DialogDescription className="mt-1 text-xs">Use the arrow buttons or ← → keys to browse. Press Escape to close.</DialogDescription>
          </div>
          {activePhoto && activeIndex !== null && (
            <>
              <FullPhoto key={`${activePhoto.url}-${activeIndex}`} photo={activePhoto} alt={activePhoto.caption || `${eventName} — photo ${activeIndex + 1}`} />
              <div className="shrink-0 space-y-3">
                {activePhoto.caption && <p className="max-h-20 overflow-y-auto break-words text-center text-sm">{activePhoto.caption}</p>}
                <div className="flex items-center justify-between gap-3">
                  <Button variant="outline" disabled={images.length < 2} onClick={() => move(-1)} aria-label="Previous image"><ChevronLeft className="h-4 w-4 sm:mr-2" /><span className="hidden sm:inline">Previous</span></Button>
                  <p aria-live="polite" aria-atomic="true" className="text-sm tabular-nums text-muted-foreground">Photo {activeIndex + 1} of {images.length}</p>
                  <Button variant="outline" disabled={images.length < 2} onClick={() => move(1)} aria-label="Next image"><span className="hidden sm:inline">Next</span><ChevronRight className="h-4 w-4 sm:ml-2" /></Button>
                </div>
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </>
  )
}
