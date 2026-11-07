"use client"

import { Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"
import { cn } from "@/lib/utils"

export function ThemeToggle({ className }: { className?: string }) {
  const { setTheme, resolvedTheme } = useTheme()

  return (
    <button
      type="button"
      onClick={() => setTheme(resolvedTheme === "dark" ? "light" : "dark")}
      aria-label="Switch between light and dark mode"
      className={cn("flex h-10 w-10 shrink-0 items-center justify-center rounded-lg border bg-card text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring", className)}
    >
      <Moon className="h-4 w-4 dark:hidden" aria-hidden="true" />
      <Sun className="hidden h-4 w-4 dark:block" aria-hidden="true" />
    </button>
  )
}
