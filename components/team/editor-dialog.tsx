"use client";

import { useRef, type ReactNode } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

export function TeamEditorDialog({
  open,
  onClose,
  title,
  description,
  busy,
  error,
  returnFocusTo,
  focusTitleOnOpen = false,
  children,
}: {
  open: boolean;
  onClose: () => void;
  title: string;
  description: string;
  busy: boolean;
  error: string;
  returnFocusTo: HTMLElement | null;
  focusTitleOnOpen?: boolean;
  children: ReactNode;
}) {
  const titleRef = useRef<HTMLHeadingElement>(null);
  return (
    <Dialog
      open={open}
      onOpenChange={(value) => {
        if (!value && !busy) onClose();
      }}
    >
      <DialogContent
        className="flex max-h-[90dvh] w-[calc(100%_-_2rem)] max-w-2xl flex-col overflow-y-auto rounded-xl"
        onInteractOutside={(event) => event.preventDefault()}
        onOpenAutoFocus={(event) => {
          if (focusTitleOnOpen) {
            event.preventDefault();
            titleRef.current?.focus();
          }
        }}
        onEscapeKeyDown={(event) => {
          if (busy) event.preventDefault();
        }}
        onCloseAutoFocus={(event) => {
          event.preventDefault();
          returnFocusTo?.focus();
        }}
      >
        <DialogHeader className="pr-6">
          <DialogTitle
            ref={titleRef}
            tabIndex={focusTitleOnOpen ? -1 : undefined}
          >
            {title}
          </DialogTitle>
          <DialogDescription>{description}</DialogDescription>
        </DialogHeader>
        {error && (
          <p
            role="alert"
            className="rounded-lg border border-destructive/40 p-3 text-sm text-destructive"
          >
            {error}
          </p>
        )}
        <fieldset disabled={busy} className="min-w-0 shrink-0" aria-busy={busy}>
          {children}
        </fieldset>
        <Button
          type="button"
          variant="outline"
          disabled={busy}
          onClick={onClose}
          className="shrink-0 self-end"
        >
          Cancel
        </Button>
      </DialogContent>
    </Dialog>
  );
}
