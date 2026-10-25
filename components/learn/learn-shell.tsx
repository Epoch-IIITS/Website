"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { useTheme } from "next-themes"
import { ChartNoAxesCombined, House, Laptop2, LibraryBig, Moon, PanelLeftClose, PanelLeftOpen, Sun } from "lucide-react"

const links = [
  { href: "/learn", label: "Topics", icon: LibraryBig },
  { href: "/learn/progress", label: "Progress", icon: ChartNoAxesCombined },
]

export function LearnShell({ children, active }: { children: React.ReactNode; active: "explore" | "progress" | "problem" }) {
  const [collapsed, setCollapsed] = useState(active === "problem")
  const { resolvedTheme, setTheme } = useTheme()

  useEffect(() => setCollapsed(active === "problem"), [active])

  return <div className="learn-surface min-h-screen bg-background text-foreground">
    <div className="mx-auto max-w-lg px-7 py-20 text-center lg:hidden">
      <Laptop2 className="mx-auto h-9 w-9 text-foreground" />
      <p className="mt-7 text-xs font-semibold uppercase tracking-[0.2em] text-muted-foreground">Learn</p>
      <h1 className="mt-3 text-2xl font-semibold tracking-tight">Open this on a laptop or desktop</h1>
      <p className="mt-4 text-sm leading-6 text-muted-foreground">The reading and Python editor layout needs a larger screen. Come back when you are at your desk.</p>
      <Link href="/" className="mt-6 inline-flex text-sm font-medium underline underline-offset-4">Back to Epoch</Link>
    </div>
    <div className={`hidden min-h-screen lg:grid ${collapsed ? "lg:grid-cols-[64px_minmax(0,1fr)]" : "lg:grid-cols-[216px_minmax(0,1fr)]"}`}>
      <aside className="sticky top-0 flex h-screen flex-col overflow-hidden border-r border-border bg-card px-2 py-3">
        <div className={`flex gap-1 ${collapsed ? "flex-col items-center" : "items-center justify-between px-1"}`}>
          <Link href="/" aria-label="Epoch home" title="Epoch home" className={`flex h-10 items-center gap-3 rounded-md text-sm font-semibold hover:bg-muted ${collapsed ? "w-10 justify-center" : "min-w-0 flex-1 px-2"}`}><House className="h-4 w-4 shrink-0" />{!collapsed && <span>Epoch</span>}</Link>
          <button type="button" onClick={() => setCollapsed(!collapsed)} aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"} title={collapsed ? "Expand sidebar" : "Collapse sidebar"} className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md text-muted-foreground hover:bg-muted hover:text-foreground">{collapsed ? <PanelLeftOpen className="h-4 w-4" /> : <PanelLeftClose className="h-4 w-4" />}</button>
        </div>
        <div className="mt-5 border-t border-border pt-4">
          {!collapsed && <p className="px-3 text-[10px] font-semibold uppercase tracking-[0.16em] text-muted-foreground">Learn</p>}
          <nav aria-label="Learn" className="mt-2 space-y-1">{links.map(({ href, label, icon: Icon }) => {
            const selected = href === "/learn" ? active !== "progress" : active === "progress"
            return <Link key={href} href={href} aria-label={label} title={collapsed ? label : undefined} className={`flex h-10 items-center gap-3 rounded-md text-sm transition-colors ${collapsed ? "justify-center" : "px-3"} ${selected ? "bg-muted font-medium text-foreground" : "text-muted-foreground hover:bg-muted/70 hover:text-foreground"}`}><Icon className="h-4 w-4 shrink-0" />{!collapsed && <span>{label}</span>}</Link>
          })}</nav>
        </div>
        <div className="mt-auto border-t border-border pt-3">
          <button type="button" onClick={() => setTheme(resolvedTheme === "dark" ? "light" : "dark")} aria-label="Toggle theme" title="Toggle theme" className={`flex h-10 w-full items-center gap-3 rounded-md text-sm text-muted-foreground hover:bg-muted hover:text-foreground ${collapsed ? "justify-center" : "px-3"}`}><Sun className="hidden h-4 w-4 shrink-0 dark:block" /><Moon className="block h-4 w-4 shrink-0 dark:hidden" />{!collapsed && <span>Appearance</span>}</button>
        </div>
      </aside>
      <main className={`min-w-0 ${active === "problem" ? "h-screen min-h-0 overflow-hidden" : "min-h-screen"}`}>{children}</main>
    </div>
  </div>
}
