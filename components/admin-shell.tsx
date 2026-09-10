"use client"

import { type ReactNode } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { signOut, useSession } from "next-auth/react"
import { LayoutDashboard, FileText, FolderOpen, Calendar, ImageIcon, Users, Inbox, ArrowUpRight, LogOut, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { SheetTitle, SheetDescription } from "@/components/ui/sheet"
import { Sidebar, SidebarProvider, SidebarTrigger, useSidebar } from "@/components/ui/sidebar"
import { ThemeToggle } from "@/components/theme-toggle"
import { cn } from "@/lib/utils"

const navigation = [
  { label: "Overview", href: "/admin", icon: LayoutDashboard },
  { label: "Blogs", href: "/admin/blogs", icon: FileText },
  { label: "Projects", href: "/admin/projects", icon: FolderOpen },
  { label: "Events", href: "/admin/events", icon: Calendar },
  { label: "Gallery", href: "/admin/gallery", icon: ImageIcon },
  { label: "Users", href: "/admin/users", icon: Users },
  { label: "Contact queries", href: "/admin/queries", icon: Inbox },
]

export function AdminShell({ children }: { children: ReactNode }) {
  return <SidebarProvider><AdminWorkspace>{children}</AdminWorkspace></SidebarProvider>
}

function AdminWorkspace({ children }: { children: ReactNode }) {
  const pathname = usePathname()
  const { data: session } = useSession()
  const { setOpenMobile, isMobile } = useSidebar()
  const isActive = (href: string) => pathname === href || (href !== "/admin" && pathname.startsWith(`${href}/`))
  const current = navigation.find(item => isActive(item.href))

  function sidebar() {
    return (
      <div className="flex h-full flex-col">
        {isMobile && <><SheetTitle className="sr-only">Admin navigation</SheetTitle><SheetDescription className="sr-only">Navigate the Epoch admin workspace.</SheetDescription><Button variant="ghost" size="icon" className="absolute right-2 top-2" aria-label="Close admin navigation" onClick={() => setOpenMobile(false)}><X className="h-4 w-4" /></Button></>}
        <Link href="/admin" onClick={() => setOpenMobile(false)} className="flex items-center gap-3 px-6 py-7">
          <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary text-lg font-bold text-primary-foreground">E</span>
          <div><p className="text-lg font-semibold tracking-tight">Epoch</p><p className="text-xs text-muted-foreground">Admin workspace</p></div>
        </Link>
        <p className="px-6 pb-3 pt-3 text-[11px] font-semibold uppercase tracking-widest text-muted-foreground">Workspace</p>
        <nav aria-label="Admin navigation" className="flex-1 space-y-1 overflow-y-auto px-3">
          {navigation.map(({ label, href, icon: Icon }) => (
            <Link key={href} href={href} onClick={() => setOpenMobile(false)} aria-current={isActive(href) ? "page" : undefined}
              className={cn("flex items-center gap-3 rounded-lg px-3 py-3 text-sm font-medium transition-colors", isActive(href) ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:bg-muted hover:text-foreground")}>
              <Icon className="h-4 w-4" aria-hidden="true" />{label}
            </Link>
          ))}
        </nav>
        <div className="space-y-3 border-t p-4">
          <Button variant="outline" asChild className="w-full justify-between"><Link href="/">View website<ArrowUpRight className="h-4 w-4" /></Link></Button>
          <div className="flex items-center gap-3 px-1">
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-muted text-sm font-semibold">{session?.user?.name?.charAt(0)?.toUpperCase() || "A"}</div>
            <div className="min-w-0 flex-1"><p className="truncate text-sm font-medium">{session?.user?.name || "Administrator"}</p><p className="truncate text-xs text-muted-foreground">{session?.user?.email}</p></div>
            <Button variant="ghost" size="icon" aria-label="Sign out" onClick={() => signOut({ callbackUrl: "/" })}><LogOut className="h-4 w-4" /></Button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <>
      <Sidebar>{sidebar()}</Sidebar>
      <div className="min-h-screen min-w-0 flex-1 bg-muted/20">
        <header className="sticky top-0 z-30 flex h-16 items-center justify-between gap-4 border-b bg-background/95 px-4 backdrop-blur sm:px-8">
          <div className="flex items-center gap-3">
            <SidebarTrigger aria-label="Toggle admin navigation" />
            <span className="text-sm text-muted-foreground">Workspace</span><span className="text-muted-foreground/50">/</span><span className="text-sm font-medium">{current?.label || "Admin"}</span>
          </div>
          <ThemeToggle />
        </header>
        <div className="min-w-0 px-2 py-4 sm:px-4 sm:py-6">{children}</div>
      </div>
    </>
  )
}
