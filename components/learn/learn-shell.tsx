"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { useTheme } from "next-themes"
import { ChartNoAxesCombined, House, LibraryBig, Moon, PanelLeftClose, PanelLeftOpen, Sun } from "lucide-react"

const links = [
  { href: "/learn", label: "Topics", icon: LibraryBig },
  { href: "/learn/progress", label: "Progress", icon: ChartNoAxesCombined },
]

export function LearnShell({ children, active }: { children: React.ReactNode; active: "explore" | "progress" | "problem" }) {
  const [collapsed, setCollapsed] = useState(active === "problem")
  const { resolvedTheme, setTheme } = useTheme()

  useEffect(() => setCollapsed(active === "problem"), [active])

  return <div className="learn-surface min-h-dvh bg-background text-foreground">
    {active !== "problem" && <header className="sticky top-0 z-40 flex h-14 items-center gap-1 border-b border-border bg-card px-2 lg:hidden">
      <Link href="/" aria-label="Epoch home" className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md hover:bg-muted"><House className="h-4 w-4" /></Link>
      <nav aria-label="Learn" className="flex min-w-0 flex-1 items-center gap-1">{links.map(({ href, label, icon: Icon }) => {
        const selected = href === "/learn" ? active !== "progress" : active === "progress"
        return <Link key={href} href={href} aria-current={selected ? "page" : undefined} className={`flex h-10 items-center gap-2 rounded-md px-3 text-sm ${selected ? "bg-muted font-medium text-foreground" : "text-muted-foreground"}`}><Icon className="h-4 w-4 shrink-0" />{label}</Link>
      })}</nav>
      <button type="button" onClick={() => setTheme(resolvedTheme === "dark" ? "light" : "dark")} aria-label="Toggle theme" className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md text-muted-foreground hover:bg-muted"><Sun className="hidden h-4 w-4 dark:block" /><Moon className="block h-4 w-4 dark:hidden" /></button>
    </header>}
    <div className={`min-h-dvh lg:grid ${collapsed ? "lg:grid-cols-[64px_minmax(0,1fr)]" : "lg:grid-cols-[216px_minmax(0,1fr)]"}`}>
      <aside className="sticky top-0 hidden h-screen lg:flex flex-col overflow-hidden border-r border-border bg-card px-2 py-3">
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
      <main className={`min-w-0 ${active === "problem" ? "h-dvh min-h-0 overflow-hidden lg:h-screen" : "lg:min-h-screen"}`}>{children}</main>
    </div>
  </div>
}
