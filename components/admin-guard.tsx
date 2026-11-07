"use client"

import { InfinityLoader } from "@/components/infinity-loader"
import type React from "react"

import { useSession } from "next-auth/react"
import { useRouter } from "next/navigation"
import { useEffect } from "react"

export function AdminGuard({ children }: { children: React.ReactNode }) {
  const { data: session, status } = useSession()
  const router = useRouter()

  useEffect(() => {
    if (status === "loading") return

    if (!session) {
      router.push("/api/auth/signin")
      return
    }

    if (session.user?.role !== "admin") {
      router.push("/")
      return
    }
  }, [session, status, router])

  if (status === "loading") {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <InfinityLoader className="h-[120px] w-[220px]" />
      </div>
    )
  }

  if (!session || session.user?.role !== "admin") {
    return null
  }

  return <>{children}</>
}
