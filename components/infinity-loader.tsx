import { useId } from "react"
import { cn } from "@/lib/utils"

const PATH = "M50 25C40 11 31 5 21 5a20 20 0 0 0 0 40c10 0 19-6 29-20s19-20 29-20a20 20 0 0 1 0 40c-10 0-19-6-29-20z"

/** An infinity-shaped loader in the Epoch logo colors. */
export function InfinityLoader({ className, label = "Loading" }: { className?: string; label?: string }) {
  const gradient = `epoch-loader-${useId().replace(/:/g, "")}`
  return (
    <svg viewBox="-5 -5 110 60" role="status" aria-label={label} className={cn("h-[60px] w-[110px] overflow-visible", className)}>
      <defs>
        <linearGradient id={gradient} x1="0" y1="0" x2="100" y2="0" gradientUnits="userSpaceOnUse">
          <stop offset="0" stopColor="#1558C8" />
          <stop offset="0.55" stopColor="#C33764" />
          <stop offset="1" stopColor="#594BA1" />
        </linearGradient>
      </defs>
      <path d={PATH} fill="none" stroke="hsl(var(--border))" strokeWidth={6} />
      <path d={PATH} fill="none" stroke={`url(#${gradient})`} strokeWidth={6} strokeLinecap="round" pathLength={100} className="infinity-loader-trail" />
    </svg>
  )
}
