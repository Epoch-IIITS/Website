'use client'

import { usePathname } from 'next/navigation'
import { useEffect, useState } from 'react'
import { InfinityLoader } from '@/components/infinity-loader'

export const PageLoader = () => {
  const pathname = usePathname()
  const [loading, setLoading] = useState(false)
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  useEffect(() => {
    setLoading(true)

    const timeout = setTimeout(() => {
      setLoading(false)
    }, 2000)

    return () => clearTimeout(timeout)
  }, [pathname])

  if (!loading || !mounted) return null

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-background">
      <InfinityLoader className="h-[120px] w-[220px]" />
    </div>
  )
}
