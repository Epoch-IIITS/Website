"use client"

import { useState, type FormEvent } from "react"
import { signIn } from "next-auth/react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export function DevSignIn() {
  const [action, setAction] = useState<"signin" | "signup">("signin")
  const [pending, setPending] = useState(false)
  const [error, setError] = useState("")

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const data = new FormData(event.currentTarget)
    setPending(true)
    setError("")

    try {
      const result = await signIn("credentials", {
        email: String(data.get("email")).trim(),
        password: String(data.get("password")),
        action,
        redirect: false,
        callbackUrl: "/admin",
      })
      if (!result?.ok || result.error) {
        setError(result?.error || "Sign-in failed. Please try again.")
        return
      }
      // Reload so the session provider and admin guard read the new session.
      window.location.assign("/admin")
    } catch {
      setError("Unable to sign in. Check your development server and database connection.")
    } finally {
      setPending(false)
    }
  }

  return (
    <form onSubmit={submit} className="space-y-4 rounded-lg border border-border p-4">
      <div>
        <h2 className="font-semibold">Development sign-in</h2>
        <p className="text-sm text-muted-foreground">
          Use an email/password account to access the dashboard without Google.
          For a new admin account, add its email to ADMIN_EMAILS and restart the server before creating it.
        </p>
      </div>
      <div className="space-y-2">
        <Label htmlFor="dev-email">Email</Label>
        <Input id="dev-email" name="email" type="email" autoComplete="username" required disabled={pending} />
      </div>
      <div className="space-y-2">
        <Label htmlFor="dev-password">Password</Label>
        <Input id="dev-password" name="password" type="password" autoComplete={action === "signup" ? "new-password" : "current-password"} required disabled={pending} />
      </div>
      {error && <p role="alert" className="text-sm text-destructive">{error}</p>}
      <Button type="submit" className="w-full" disabled={pending}>
        {pending ? "Please wait…" : action === "signup" ? "Create account and sign in" : "Sign in with password"}
      </Button>
      <Button type="button" variant="link" className="w-full" disabled={pending} onClick={() => {
        setAction(action === "signin" ? "signup" : "signin")
        setError("")
      }}>
        {action === "signin" ? "Create a development account" : "Use an existing account"}
      </Button>
    </form>
  )
}
