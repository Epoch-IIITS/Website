"use client"

import { type ReactNode, useEffect, useState } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { signOut, useSession } from "next-auth/react"
import { LayoutDashboard, FileText, FolderOpen, Calendar, ImageIcon, Users, Inbox, LogOut, X, Wrench, ScrollText, GraduationCap } from "lucide-react"
import { Button } from "@/components/ui/button"
import { SheetTitle, SheetDescription } from "@/components/ui/sheet"
import { Sidebar, SidebarProvider, SidebarTrigger, useSidebar } from "@/components/ui/sidebar"
import { ThemeToggle } from "@/components/theme-toggle"
import { cn } from "@/lib/utils"
import { EpochMark } from "@/components/epoch-mark"

type CountKey = "blogs" | "projects" | "events" | "galleries"
type NavItem = { label: string; href: string; icon: typeof LayoutDashboard; count?: CountKey }

const overview: NavItem = { label: "Overview", href: "/admin", icon: LayoutDashboard }
const sections: { label: string; items: NavItem[] }[] = [
  { label: "Content", items: [
    { label: "Blog posts", href: "/admin/blogs", icon: FileText, count: "blogs" },
    { label: "Projects", href: "/admin/projects", icon: FolderOpen, count: "projects" },
    { label: "Events", href: "/admin/events", icon: Calendar, count: "events" },
    { label: "Gallery", href: "/admin/gallery", icon: ImageIcon, count: "galleries" },
  ] },
  { label: "People", items: [
    { label: "Team", href: "/admin/team", icon: Users },
    { label: "Users", href: "/admin/users", icon: Users },
    { label: "Learners", href: "/admin/learners", icon: GraduationCap },
    { label: "Inbox", href: "/admin/queries", icon: Inbox },
  ] },
  { label: "Tools", items: [
    { label: "Activity log", href: "/admin/logs", icon: ScrollText },
    { label: "Utilities", href: "/admin/utilities", icon: Wrench },
  ] },
]
const allItems = [overview, ...sections.flatMap(section => section.items)]

export function AdminShell({ children }: { children: ReactNode }) {
  return <SidebarProvider><AdminWorkspace>{children}</AdminWorkspace></SidebarProvider>
}

function AdminWorkspace({ children }: { children: ReactNode }) {
  const pathname = usePathname()
  const { data: session } = useSession()
  const { setOpenMobile, isMobile } = useSidebar()
  const [counts, setCounts] = useState<Partial<Record<CountKey, number>>>({})
  useEffect(() => {
    let cancelled = false
    fetch("/api/admin/stats", { cache: "no-store" }).then(response => response.ok ? response.json() : null).then(stats => {
      if (cancelled || !stats) return
      setCounts({ blogs: stats.blogs?.total, projects: stats.projects?.total, events: stats.events?.total, galleries: stats.galleries?.total })
    }).catch(() => {})
    return () => { cancelled = true }
  }, [])
  const isActive = (href: string) => pathname === href || (href !== "/admin" && pathname.startsWith(`${href}/`))
  const current = allItems.find(item => isActive(item.href))

  function navLink({ label, href, count }: NavItem) {
    const value = count ? counts[count] : undefined
    return <Link key={href} href={href} onClick={() => setOpenMobile(false)} aria-current={isActive(href) ? "page" : undefined}
      className={cn("flex h-9 items-center justify-between gap-3 rounded-lg px-2.5 text-sm transition-colors", isActive(href) ? "bg-secondary font-medium text-foreground" : "text-muted-foreground hover:bg-secondary hover:text-foreground")}>
      <span className="truncate">{label}</span>{value !== undefined && <span className="text-xs tabular-nums text-subtle">{value}</span>}
    </Link>
  }

  function sidebar() {
    return (
      <div className="flex h-full flex-col gap-5 bg-card px-3.5 py-[18px]">
        {isMobile && <><SheetTitle className="sr-only">Admin navigation</SheetTitle><SheetDescription className="sr-only">Navigate the Epoch admin workspace.</SheetDescription><Button variant="ghost" size="icon" className="absolute right-2 top-2" aria-label="Close admin navigation" onClick={() => setOpenMobile(false)}><X className="h-4 w-4" /></Button></>}
        <Link href="/admin" onClick={() => setOpenMobile(false)} className="flex items-center gap-2.5 px-1.5 py-1">
          <EpochMark className="h-5" />
          <span className="flex flex-col leading-tight"><span className="text-sm font-semibold">Epoch</span><span className="text-xs text-muted-foreground">Admin workspace</span></span>
        </Link>
        <nav aria-label="Admin navigation" className="-mx-1 flex flex-1 flex-col gap-0.5 overflow-y-auto px-1">
          {navLink(overview)}
          {sections.map(section => <div key={section.label} className="flex flex-col gap-0.5">
            <p className="px-2.5 pb-1.5 pt-3.5 font-mono text-[11px] uppercase tracking-[0.06em] text-subtle">{section.label}</p>
            {section.items.map(item => navLink(item))}
          </div>)}
        </nav>
        <div className="flex flex-col gap-3 border-t border-border/60 pt-3">
          <div className="flex items-center gap-2.5 px-1.5">
            <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-secondary text-[13px] font-semibold">{session?.user?.name?.charAt(0)?.toUpperCase() || "A"}</span>
            <div className="min-w-0 flex-1"><p className="truncate text-sm font-medium">{session?.user?.name || "Administrator"}</p><p className="truncate text-xs text-muted-foreground">{session?.user?.email}</p></div>
            <Button variant="ghost" size="icon" className="h-8 w-8 shrink-0 text-muted-foreground" aria-label="Sign out" title="Sign out" onClick={() => signOut({ callbackUrl: "/" })}><LogOut className="h-4 w-4" /></Button>
          </div>
          <div className="flex items-center justify-between px-1.5 text-sm text-muted-foreground"><span>Appearance</span><ThemeToggle /></div>
        </div>
      </div>
    )
  }

  return (
    <>
      <Sidebar>{sidebar()}</Sidebar>
      <div className="min-h-screen min-w-0 flex-1 bg-sunken">
        <header className="sticky top-0 z-30 flex h-14 items-center gap-3 border-b bg-background/95 px-4 backdrop-blur md:hidden">
          <SidebarTrigger aria-label="Open admin navigation" />
          <span className="text-sm text-muted-foreground">Admin</span><span className="text-muted-foreground/50">/</span><span className="truncate text-sm font-medium">{current?.label || "Workspace"}</span>
        </header>
        <div className="hidden md:block"><SidebarTrigger aria-label="Toggle admin navigation" className="m-3 mb-0 text-muted-foreground" /></div>
        <div className="min-w-0 px-2 pb-14 pt-4 sm:px-6 md:pt-1 lg:px-8">{children}</div>
      </div>
    </>
  )
}
