"use client"

import type React from "react"

import { useState } from "react"
import { useSession } from "next-auth/react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { toast } from "sonner"
import { Mail, MapPin, Phone, Clock, Instagram } from "lucide-react"

export default function ContactPage() {
  const { data: session, status } = useSession()
  const accountEmail = session?.user?.email || ""
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitError, setSubmitError] = useState("")

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
      toast.success("Message received! Our team will review your query.")
      form.reset()
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : "Unable to send your message. Please try again.")
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4">Contact Us</h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Have questions about our events, want to collaborate, or just want to say hello? We'd love to hear from you!
        </p>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Contact Information */}
        <div className="lg:col-span-1">
          <Card>
            <CardHeader>
              <CardTitle>Get in Touch</CardTitle>
              <CardDescription>Reach out to us through any of these channels</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-start space-x-3">
                <Mail className="h-5 w-5 text-primary mt-1" />
                <div>
                  <p className="font-medium">Email</p>
                  <p className="text-sm text-muted-foreground">aiml.club@iiits.in</p>
                </div>
              </div>

              <div className="flex items-start space-x-3">
                <Instagram className="h-5 w-5 text-primary mt-1" />
                <div>
                  <p className="font-medium">Instagram</p>
                  <p className="text-sm text-muted-foreground">epoch.iiits</p>
                </div>
              </div>

              {/* <div className="flex items-start space-x-3">
                <MapPin className="h-5 w-5 text-primary mt-1" />
                <div>
                  <p className="font-medium">Address</p>
                  <p className="text-sm text-muted-foreground">
                    123 Tech Street
                    <br />
                    Innovation District
                    <br />
                    San Francisco, CA 94105
                  </p>
                </div>
              </div> */}

              {/* <div className="flex items-start space-x-3">
                <Clock className="h-5 w-5 text-primary mt-1" />
                <div>
                  <p className="font-medium">Office Hours</p>
                  <p className="text-sm text-muted-foreground">
                    Monday - Friday: 9:00 AM - 6:00 PM
                    <br />
                    Saturday: 10:00 AM - 4:00 PM
                    <br />
                    Sunday: Closed
                  </p>
                </div>
              </div> */}
            </CardContent>
          </Card>

          {/* FAQ */}
          <Card className="mt-6">
            <CardHeader>
              <CardTitle>Quick Questions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <p className="font-medium text-sm">How do I join TechClub?</p>
                <p className="text-sm text-muted-foreground">
                  Simply sign up with your Google account and start attending our events!
                </p>
              </div>
              <div>
                <p className="font-medium text-sm">Are events free?</p>
                <p className="text-sm text-muted-foreground">
                  Most of our events are free for members. Some special workshops may have a small fee.
                </p>
              </div>
              <div>
                <p className="font-medium text-sm">Can I suggest an event topic?</p>
                <p className="text-sm text-muted-foreground">
                  We love member suggestions. Use the contact form to share your ideas.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Contact Form */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Send us a Message</CardTitle>
              <CardDescription>Send your questions and ideas to the Epoch team.</CardDescription>
            </CardHeader>
            <CardContent>
              {status === "loading" ? (
                <p role="status" className="py-12 text-center text-sm text-muted-foreground">Checking your account…</p>
              ) : !accountEmail ? (
                <div className="space-y-4 rounded-lg border border-dashed bg-muted/30 px-6 py-12 text-center">
                  <h2 className="text-lg font-semibold">Log in to see the contact form</h2>
                  <p className="text-sm text-muted-foreground">Use your Epoch account to send us a message.</p>
                  <Button asChild><Link href="/auth/signin?callbackUrl=%2Fcontact">Log in</Link></Button>
                </div>
              ) : <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="firstName">First Name</Label>
                    <Input id="firstName" name="firstName" required maxLength={80} disabled={isSubmitting} placeholder="John" />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="lastName">Last Name</Label>
                    <Input id="lastName" name="lastName" required maxLength={80} disabled={isSubmitting} placeholder="Doe" />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email" name="email" type="email" required maxLength={254}
                    value={accountEmail}
                    readOnly
                    className="cursor-not-allowed bg-muted text-muted-foreground"
                    disabled={isSubmitting}
                    autoComplete="email"
                    aria-describedby="account-email-note"
                  />
                  <p id="account-email-note" className="text-xs text-muted-foreground">Using the email from your signed-in account.</p>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="subject">Subject</Label>
                  <Input id="subject" name="subject" required maxLength={200} disabled={isSubmitting} placeholder="What's this about?" />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="message">Message</Label>
                  <Textarea
                    id="message"
                    name="message"
                    required
                    maxLength={5000}
                    disabled={isSubmitting}
                    rows={6}
                    placeholder="Tell us more about your inquiry..."
                  />
                </div>

                {submitError && <p role="alert" className="text-sm text-destructive">{submitError}</p>}
                <Button type="submit" disabled={isSubmitting} className="w-full">
                  {isSubmitting ? "Sending..." : "Send Message"}
                </Button>
              </form>}
            </CardContent>
          </Card>
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
