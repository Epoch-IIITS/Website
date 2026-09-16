"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { useSession } from "next-auth/react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { ProfileFields, emptyProfile } from "@/components/team/profile-fields"
import { toast } from "sonner"
import { User, Mail, Shield, Calendar } from "lucide-react"

export default function ProfilePage() {
  const { data: session, status } = useSession()
  const [teamProfile, setTeamProfile] = useState(emptyProfile)
  const [isTeamMember, setIsTeamMember] = useState(false)
  const [teamProfileLoading, setTeamProfileLoading] = useState(true)
  const [teamProfileSaving, setTeamProfileSaving] = useState(false)
  const [teamPhotoUploading, setTeamPhotoUploading] = useState(false)
  const [teamProfileError, setTeamProfileError] = useState("")

  useEffect(() => {
    if (status !== "authenticated") return

    let cancelled = false
    const loadTeamProfile = async () => {
      setTeamProfileLoading(true)
      setTeamProfileError("")
      try {
        const response = await fetch("/api/team/profile", { cache: "no-store" })
        const result = await response.json().catch(() => ({}))
        if (!response.ok) {
          throw new Error(result.error || "Unable to load your team profile")
        }
        if (cancelled) return
        setIsTeamMember(Boolean(result.member))
        if (result.member && result.profile) setTeamProfile(result.profile)
      } catch (error) {
        if (!cancelled) {
          setTeamProfileError(
            error instanceof Error ? error.message : "Unable to load your team profile",
          )
        }
      } finally {
        if (!cancelled) setTeamProfileLoading(false)
      }
    }

    void loadTeamProfile()
    return () => {
      cancelled = true
    }
  }, [status])

  const handleUpdateTeamProfile = async (e: React.FormEvent) => {
    e.preventDefault()
    setTeamProfileSaving(true)
    setTeamProfileError("")

    try {
      const response = await fetch("/api/team/profile", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(teamProfile),
      })
      const result = await response.json().catch(() => ({}))
      if (!response.ok) {
        throw new Error(result.error || "Unable to update your team profile")
      }

      setTeamProfile(result.profile)
      toast.success("Team profile updated successfully!")
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Unable to update your team profile"
      setTeamProfileError(message)
      toast.error(message)
    } finally {
      setTeamProfileSaving(false)
    }
  }

  if (status === "loading") {
    return (
      <div className="container mx-auto px-4 py-8 max-w-2xl">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-muted rounded w-1/4"></div>
          <div className="h-64 bg-muted rounded"></div>
        </div>
      </div>
    )
  }

  if (!session) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-2xl">
        <div className="text-center">
          <h1 className="text-4xl font-bold mb-4">Profile</h1>
          <p className="text-muted-foreground mb-8">Please sign in to view your profile</p>
          <Button asChild>
            <a href="/auth/signin">Sign In</a>
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-3xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-4">Profile</h1>
        <p className="text-muted-foreground">Manage your account settings and preferences</p>
      </div>

      <div className="space-y-6">
        {/* Profile Overview */}
        <Card>
          <CardHeader>
            <CardTitle>Profile Overview</CardTitle>
            <CardDescription>Your account information and status</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center space-x-4 mb-6">
              <Avatar className="h-20 w-20">
                <AvatarImage src={session.user.image || ""} alt={session.user.name || ""} />
                <AvatarFallback className="text-lg">
                  {session.user.name?.charAt(0) || session.user.email?.charAt(0) || "U"}
                </AvatarFallback>
              </Avatar>
              <div className="space-y-2">
                <h3 className="text-xl font-semibold">{session.user.name || "User"}</h3>
                <div className="flex items-center gap-2">
                  <Badge variant={session.user.role === "admin" ? "default" : "secondary"}>
                    {session.user.role === "admin" ? "Admin" : "user"}
                  </Badge>
                  {session.user.role === "admin" && (
                    <Badge variant="outline">
                      <Shield className="mr-1 h-3 w-3" />
                      Admin Access
                    </Badge>
                  )}
                </div>
              </div>
            </div>

            <div className="grid gap-4">
              <div className="flex items-center gap-3 text-sm">
                <Mail className="h-4 w-4 text-muted-foreground" />
                <span>{session.user.email}</span>
              </div>
              <div className="flex items-center gap-3 text-sm">
                <User className="h-4 w-4 text-muted-foreground" />
                <span>Provider: {session.user.provider || "Google"}</span>
              </div>
              <div className="flex items-center gap-3 text-sm">
                <Calendar className="h-4 w-4 text-muted-foreground" />
                <span>
                  Member since: {session.user.createdAt ? new Date(session.user.createdAt).toLocaleDateString() : "Unavailable"}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>

        {teamProfileLoading && (
          <Card>
            <CardHeader>
              <CardTitle>Team directory profile</CardTitle>
              <CardDescription>Checking for a team listing linked to your account…</CardDescription>
            </CardHeader>
          </Card>
        )}

        {!teamProfileLoading && isTeamMember && (
          <Card>
            <CardHeader>
              <CardTitle>Team directory profile</CardTitle>
              <CardDescription>
                These shared details appear in every academic year where you are listed.
                Team years and positions remain managed by administrators.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleUpdateTeamProfile} className="space-y-6">
                <fieldset
                  disabled={teamProfileSaving || teamPhotoUploading}
                  className="space-y-6 disabled:opacity-70"
                >
                  <ProfileFields
                    value={teamProfile}
                    onChange={setTeamProfile}
                    onUploadingChange={setTeamPhotoUploading}
                  />
                  {teamProfileError && (
                    <p role="alert" className="text-sm text-destructive">
                      {teamProfileError}
                    </p>
                  )}
                  <Button type="submit">
                    {teamPhotoUploading
                      ? "Uploading photo…"
                      : teamProfileSaving
                        ? "Saving…"
                        : "Save team profile"}
                  </Button>
                </fieldset>
              </form>
            </CardContent>
          </Card>
        )}

        {!teamProfileLoading && !isTeamMember && (
          <Card>
            <CardHeader>
              <CardTitle>Team directory profile</CardTitle>
              <CardDescription>
                No team listing is linked to {session.user.email || "this account"}.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <p
                role={teamProfileError ? "alert" : "status"}
                className={teamProfileError ? "text-sm text-destructive" : "text-sm text-muted-foreground"}
              >
                {teamProfileError ||
                  "If you already appear on the Team page, an administrator needs to add this account email to your person profile."}
              </p>
              {session.user.role === "admin" && !teamProfileError && (
                <Button asChild variant="outline">
                  <a href="/admin/team">Open team administration</a>
                </Button>
              )}
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
