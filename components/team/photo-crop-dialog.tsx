"use client";

import { useEffect, useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

const clamp = (value: number) => Math.max(0, Math.min(1, value));

export function PhotoCropDialog({
  source,
  open,
  onClose,
  onConfirm,
  returnFocusTo,
}: {
  source: string;
  open: boolean;
  onClose: () => void;
  onConfirm: (photo: Blob) => Promise<void>;
  returnFocusTo: HTMLElement | null;
}) {
  const image = useRef<HTMLImageElement>(null);
  const drag = useRef<{
    x: number;
    y: number;
    horizontal: number;
    vertical: number;
    width: number;
  } | null>(null);
  const [size, setSize] = useState({ width: 0, height: 0 });
  const [zoom, setZoom] = useState(1);
  const [horizontal, setHorizontal] = useState(0.5);
  const [vertical, setVertical] = useState(0.5);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  useEffect(() => {
    setSize({ width: 0, height: 0 });
    setZoom(1);
    setHorizontal(0.5);
    setVertical(0.5);
    setError("");
  }, [source]);
  const cropSize = Math.min(size.width, size.height) / zoom;
  const x = (size.width - cropSize) * horizontal;
  const y = (size.height - cropSize) * vertical;
  async function applyCrop() {
    if (!image.current || !cropSize || busy) return;
    setBusy(true);
    setError("");
    try {
      const canvas = document.createElement("canvas");
      canvas.width = canvas.height = Math.min(
        1200,
        Math.max(1, Math.round(cropSize)),
      );
      const context = canvas.getContext("2d");
      if (!context)
        throw new Error("This browser could not prepare the photo.");
      context.fillStyle = "#ffffff";
      context.fillRect(0, 0, canvas.width, canvas.height);
      context.drawImage(
        image.current,
        x,
        y,
        cropSize,
        cropSize,
        0,
        0,
        canvas.width,
        canvas.height,
      );
      const blob = await new Promise<Blob>((resolve, reject) =>
        canvas.toBlob(
          (value) =>
            value
              ? resolve(value)
              : reject(new Error("Could not prepare the cropped photo.")),
          "image/jpeg",
          0.92,
        ),
      );
      await onConfirm(blob);
    } catch (error: any) {
      setError(
        error.name === "SecurityError"
          ? "This photo cannot be cropped here. Select the original image from your device."
          : error.message || "Could not crop this photo. Please try again.",
      );
    } finally {
      setBusy(false);
    }
  }
  return (
    <Dialog
      open={open}
      onOpenChange={(value) => {
        if (!value && !busy) onClose();
      }}
    >
      <DialogContent
        className="flex max-h-[90dvh] w-[calc(100%_-_2rem)] max-w-lg flex-col overflow-y-auto rounded-xl"
        onInteractOutside={(event) => event.preventDefault()}
        onEscapeKeyDown={(event) => {
          if (busy) event.preventDefault();
        }}
        onCloseAutoFocus={(event) => {
          event.preventDefault();
          returnFocusTo?.focus();
        }}
      >
        <DialogHeader className="pr-6">
          <DialogTitle>Choose your photo’s frame</DialogTitle>
          <DialogDescription>
            Drag the photo and adjust the zoom. Everything inside the square
            will appear on your profile and share card.
          </DialogDescription>
        </DialogHeader>
        <div
          className="relative mx-auto aspect-square w-full max-w-[320px] shrink-0 touch-none select-none overflow-hidden rounded-xl bg-muted cursor-grab active:cursor-grabbing"
          onPointerDown={(event) => {
            if (!cropSize || busy) return;
            event.currentTarget.setPointerCapture(event.pointerId);
            drag.current = {
              x: event.clientX,
              y: event.clientY,
              horizontal,
              vertical,
              width: event.currentTarget.getBoundingClientRect().width,
            };
          }}
          onPointerMove={(event) => {
            const start = drag.current;
            if (!start || busy) return;
            if (size.width > cropSize)
              setHorizontal(
                clamp(
                  start.horizontal -
                    (((event.clientX - start.x) / start.width) * cropSize) /
                      (size.width - cropSize),
                ),
              );
            if (size.height > cropSize)
              setVertical(
                clamp(
                  start.vertical -
                    (((event.clientY - start.y) / start.width) * cropSize) /
                      (size.height - cropSize),
                ),
              );
          }}
          onPointerUp={() => {
            drag.current = null;
          }}
          onPointerCancel={() => {
            drag.current = null;
          }}
          onLostPointerCapture={() => {
            drag.current = null;
          }}
        >
          <img
            key={source}
            ref={image}
            src={source}
            crossOrigin="anonymous"
            alt="Selected photo crop"
            draggable={false}
            onLoad={(event) =>
              setSize({
                width: event.currentTarget.naturalWidth,
                height: event.currentTarget.naturalHeight,
              })
            }
            onError={() => {
              setSize({ width: 0, height: 0 });
              setError(
                "We couldn’t load this photo. Select a JPG, PNG or WebP image from your device.",
              );
            }}
            className="pointer-events-none absolute max-w-none"
            style={
              cropSize
                ? {
                    width: `${(size.width / cropSize) * 100}%`,
                    height: `${(size.height / cropSize) * 100}%`,
                    left: `${(-x / cropSize) * 100}%`,
                    top: `${(-y / cropSize) * 100}%`,
                  }
                : { visibility: "hidden" }
            }
          />
          {!cropSize && (
            <p className="absolute inset-0 flex items-center justify-center text-sm text-muted-foreground">
              {error ? "Photo unavailable" : "Loading photo…"}
            </p>
          )}
          <div
            aria-hidden="true"
            className="pointer-events-none absolute inset-0 grid grid-cols-3 grid-rows-3"
          >
            {Array.from({ length: 9 }, (_, i) => (
              <span key={i} className="border border-white/25" />
            ))}
          </div>
        </div>
        <fieldset disabled={busy || !cropSize} className="space-y-3">
          <label className="block text-sm font-medium">
            Zoom · {zoom.toFixed(1)}×
            <input
              type="range"
              min={1}
              max={4}
              step={0.01}
              value={zoom}
              onChange={(event) => setZoom(Number(event.target.value))}
              className="mt-2 block w-full accent-primary"
            />
          </label>
          <div className="grid grid-cols-2 gap-4">
            <label className="block text-sm">
              Horizontal position
              <input
                type="range"
                min={0}
                max={1}
                step={0.01}
                value={horizontal}
                disabled={size.width <= cropSize}
                onChange={(event) => setHorizontal(Number(event.target.value))}
                className="mt-2 block w-full accent-primary"
              />
            </label>
            <label className="block text-sm">
              Vertical position
              <input
                type="range"
                min={0}
                max={1}
                step={0.01}
                value={vertical}
                disabled={size.height <= cropSize}
                onChange={(event) => setVertical(Number(event.target.value))}
                className="mt-2 block w-full accent-primary"
              />
            </label>
          </div>
          <Button
            type="button"
            variant="ghost"
            onClick={() => {
              setZoom(1);
              setHorizontal(0.5);
              setVertical(0.5);
            }}
          >
            Reset frame
          </Button>
        </fieldset>
        {error && (
          <p role="alert" className="text-sm text-destructive">
            {error}
          </p>
        )}
        <div className="flex justify-end gap-3">
          <Button
            type="button"
            variant="outline"
            disabled={busy}
            onClick={onClose}
          >
            Cancel
          </Button>
          <Button
            type="button"
            disabled={busy || !cropSize}
            onClick={applyCrop}
          >
            {busy ? "Uploading…" : "Use this crop"}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
