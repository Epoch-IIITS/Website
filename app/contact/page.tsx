"use client"

import type React from "react"

import { useState } from "react"
import { useSession } from "next-auth/react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Check, Mail, MapPin, Instagram } from "lucide-react"
import { PageKicker } from "@/components/page-kicker"

export default function ContactPage() {
  const { data: session, status } = useSession()
  const accountEmail = session?.user?.email || ""
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitError, setSubmitError] = useState("")
  const [sent, setSent] = useState(false)

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const form = e.currentTarget
    const data = new FormData(form)
    setIsSubmitting(true)
    setSubmitError("")
    try {
      const response = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(Object.fromEntries(data.entries())),
      })
      const result = await response.json()
      if (!response.ok) throw new Error(result.error || "Unable to send your message")
      form.reset()
      setSent(true)
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : "Unable to send your message. Please try again.")
    } finally {
      setIsSubmitting(false)
    }
  }

  const field = "h-[46px] rounded-[10px] bg-card px-3.5 text-[15px]"
  const channels = [
    { icon: Mail, label: "Email", value: "aiml.club@iiits.in", href: "mailto:aiml.club@iiits.in" },
    { icon: Instagram, label: "Instagram", value: "@epoch.iiits", href: "https://www.instagram.com/epoch.iiits/" },
    { icon: MapPin, label: "Find us", value: "IIIT Sri City campus, Andhra Pradesh" },
  ]

  return (
    <div className="mx-auto max-w-[1200px] px-4 pb-24 pt-16 sm:px-8 sm:pt-20">
      <div className="grid items-start gap-12 lg:grid-cols-2 lg:gap-16">
        <div className="flex flex-col gap-10">
          <div className="flex flex-col gap-4">
            <PageKicker as="p" className="mb-0">Contact</PageKicker>
            <h1 className="text-[40px] font-semibold leading-[1.04] tracking-[-0.035em] sm:text-[56px]">Talk to the team</h1>
            <p className="text-[17px] leading-relaxed text-muted-foreground">Questions, collaboration ideas or a topic you want covered — send a message and a committee member will reply by email.</p>
          </div>

          <ul className="flex flex-col border-t">
            {channels.map(({ icon: Icon, label, value, href }) => {
              const body = (
                <>
                  <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-[10px] bg-secondary"><Icon className="h-[18px] w-[18px]" aria-hidden="true" /></span>
                  <span className="flex flex-col gap-0.5"><span className="text-[13px] text-muted-foreground">{label}</span><span className="text-base font-medium">{value}</span></span>
                </>
              )
              return (
                <li key={label} className="border-b">
                  {href ? (
                    <a href={href} target={href.startsWith("http") ? "_blank" : undefined} rel={href.startsWith("http") ? "noopener noreferrer" : undefined} className="flex items-center gap-4 py-[18px] hover:text-primary">{body}</a>
                  ) : (
                    <div className="flex items-center gap-4 py-[18px]">{body}</div>
                  )}
                </li>
              )
            })}
          </ul>

        </div>

        <div className="rounded-[20px] border bg-card p-6 shadow-[0_24px_48px_-32px_rgba(14,17,22,0.25)] sm:p-9">
          {status === "loading" ? (
            <p role="status" className="py-12 text-center text-sm text-muted-foreground">Checking your account…</p>
          ) : !accountEmail ? (
            <div className="flex min-h-[420px] flex-col items-center justify-center gap-4 text-center">
              <h2 className="text-[22px] font-semibold">Log in to see the contact form</h2>
              <p className="max-w-[340px] text-[15px] leading-relaxed text-muted-foreground">Use your Epoch account to send us a message.</p>
              <Button asChild className="h-11 rounded-[10px] px-[18px]"><Link href="/auth/signin?callbackUrl=%2Fcontact">Log in</Link></Button>
            </div>
          ) : sent ? (
            <div className="flex min-h-[520px] flex-col items-center justify-center gap-4 text-center" role="status">
              <span className="flex h-14 w-14 items-center justify-center rounded-full bg-success-soft text-success"><Check className="h-6 w-6" aria-hidden="true" /></span>
              <h2 className="text-2xl font-semibold">Message sent</h2>
              <p className="max-w-[340px] text-[15px] leading-relaxed text-muted-foreground">Thanks for reaching out. A committee member will reply to {accountEmail}.</p>
              <Button variant="outline" className="h-[42px] rounded-[10px]" onClick={() => setSent(false)}>Send another</Button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="flex flex-col gap-5">
              <div className="flex flex-col gap-1.5">
                <h2 className="text-[22px] font-semibold">Send a message</h2>
                <p className="text-sm text-muted-foreground">We usually reply within a few days.</p>
              </div>
              <div className="grid gap-4 sm:grid-cols-2">
                <div className="flex flex-col gap-2">
                  <Label htmlFor="firstName">First name</Label>
                  <Input id="firstName" name="firstName" required maxLength={80} disabled={isSubmitting} placeholder="John" className={field} />
                </div>
                <div className="flex flex-col gap-2">
                  <Label htmlFor="lastName">Last name</Label>
                  <Input id="lastName" name="lastName" required maxLength={80} disabled={isSubmitting} placeholder="Doe" className={field} />
                </div>
              </div>

              <div className="flex flex-col gap-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email" name="email" type="email" required maxLength={254}
                  value={accountEmail}
                  readOnly
                  className={`${field} cursor-not-allowed bg-muted text-muted-foreground`}
                  disabled={isSubmitting}
                  autoComplete="email"
                  aria-describedby="account-email-note"
                />
                <p id="account-email-note" className="text-xs text-subtle">Using the email from your signed-in account.</p>
              </div>

              <div className="flex flex-col gap-2">
                <Label htmlFor="subject">Topic</Label>
                <select id="subject" name="subject" required disabled={isSubmitting} defaultValue="General question" className={`${field} w-full border border-input outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50`}>
                  {["General question", "Collaboration or sponsorship", "Event or topic idea", "Join the team"].map((topic) => <option key={topic}>{topic}</option>)}
                </select>
              </div>

              <div className="flex flex-col gap-2">
                <Label htmlFor="message">Message</Label>
                <Textarea
                  id="message"
                  name="message"
                  required
                  maxLength={5000}
                  disabled={isSubmitting}
                  rows={6}
                  placeholder="Tell us more about your question or idea…"
                  className="rounded-[10px] bg-card px-3.5 py-3 text-[15px]"
                />
              </div>

              {submitError && <p role="alert" className="text-sm text-destructive">{submitError}</p>}
              <Button type="submit" disabled={isSubmitting} className="h-12 w-full rounded-[10px] text-[15px]">
                {isSubmitting ? "Sending…" : "Send message"}
              </Button>
            </form>
          )}
        </div>
      </div>

      {/* 
      <Card className="mt-8">
        <CardHeader>
          <CardTitle>Find Us</CardTitle>
          <CardDescription>Visit us at our office in the heart of San Francisco's Innovation District</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="aspect-video bg-muted rounded-lg flex items-center justify-center">
            <p className="text-muted-foreground">
              Interactive map would be embedded here
              <br />
              <span className="text-sm">(Google Maps, Mapbox, etc.)</span>
            </p>
          </div>
        </CardContent>
      </Card> */}
    </div>
  )
}
