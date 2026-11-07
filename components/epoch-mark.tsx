import { cn } from "@/lib/utils"

/** The Epoch infinity logo (blue to pink gradient). Size it by height; width follows its 2.1:1 ratio. */
export function EpochMark({ className }: { className?: string }) {
  // eslint-disable-next-line @next/next/no-img-element
  return <img src="/epoch_mark.png" alt="" aria-hidden="true" width={223} height={106} className={cn("h-6 w-auto shrink-0 select-none", className)} draggable={false} />
}
