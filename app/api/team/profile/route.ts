import { getServerSession } from "next-auth"
import { NextRequest, NextResponse } from "next/server"
import { ZodError } from "zod"
import { authOptions } from "@/lib/auth"
import { diffAuditFields, runAuditedMutation } from "@/lib/audit-log"
import {
  attemptMediaCleanup,
  ensureMediaStorage,
  reconcileMediaUrls,
} from "@/lib/media-assets"
import connectDB from "@/lib/mongodb"
import { profileSchema } from "@/lib/team-validation"
import { findMemberProfile, normalizeTeamEmail } from "@/lib/team-membership"
import {
  ensureTeamStorage,
  TeamPerson,
} from "@/models/Team"

export const dynamic = "force-dynamic"

function serializeProfile(person: any) {
  return {
    name: person.name || "",
    linkedin: person.linkedin || "",
    currentRole: person.currentRole || "",
    organization: person.organization || "",
    photo: person.photo || "",
    tagline: person.tagline || "",
  }
}

export async function GET() {
  const session = await getServerSession(authOptions)
  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
  }

  try {
    await connectDB()
    const membership = await findMemberProfile(
      session.user.id,
      normalizeTeamEmail(session.user.email),
    )
    const response = membership
      ? NextResponse.json({
          member: true,
          profile: serializeProfile(membership),
        })
      : NextResponse.json({ member: false })

    response.headers.set("Cache-Control", "no-store")
    return response
  } catch (error) {
    console.error("Failed to load member team profile", error)
    return NextResponse.json(
      { error: "Unable to load your team profile" },
      { status: 500 },
    )
  }
}

export async function PUT(request: NextRequest) {
  const session = await getServerSession(authOptions)
  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
  }

  try {
    const value = profileSchema.parse(await request.json())
    await connectDB()
    await ensureTeamStorage()
    await ensureMediaStorage()

    let updatedPerson: any = null
    const cleanupIds = new Set<string>()
    const email = normalizeTeamEmail(session.user.email)

    await runAuditedMutation(session, request, async (dbSession) => {
      const membership = await findMemberProfile(
        session.user.id,
        email,
        dbSession,
      )
      if (!membership) throw new TeamProfileAccessError()

      updatedPerson = await TeamPerson.findOneAndUpdate(
        { _id: membership._id },
        {
          $set: {
            ...value,
            userId: session.user.id,
            ...(email ? { email } : {}),
          },
        },
        { returnDocument: "after", runValidators: true, session: dbSession },
      )
      if (!updatedPerson) throw new TeamProfileAccessError()

      const removedIds = await reconcileMediaUrls({
        beforeUrls: [membership.photo],
        afterUrls: [updatedPerson.photo],
        reason: `Updated by team member ${session.user.id}`,
        session: dbSession,
      })
      removedIds.forEach((publicId) => cleanupIds.add(publicId))

      const changes = diffAuditFields(membership, updatedPerson, [
        "name",
        "linkedin",
        "currentRole",
        "organization",
        "photo",
        "tagline",
      ])
      return {
        value: true,
        logs: changes.length
          ? [
              {
                action: "update" as const,
                entityType: "team-person",
                entityId: String(updatedPerson._id),
                entityLabel: updatedPerson.name,
                summary: `Updated own team profile “${updatedPerson.name}”`,
                changes,
                sideEffects: removedIds.length
                  ? { cloudinaryImagesQueued: removedIds.length }
                  : undefined,
              },
            ]
          : [],
      }
    })

    await attemptMediaCleanup([...cleanupIds])
    return NextResponse.json({
      member: true,
      profile: serializeProfile(updatedPerson),
    })
  } catch (error) {
    if (error instanceof ZodError) {
      return NextResponse.json(
        { error: error.issues[0]?.message || "Invalid profile details" },
        { status: 400 },
      )
    }
    if (error instanceof TeamProfileAccessError) {
      return NextResponse.json(
        { error: "No team profile is linked to this account" },
        { status: 403 },
      )
    }
    if (
      typeof error === "object" &&
      error !== null &&
      "code" in error &&
      error.code === 11000
    ) {
      return NextResponse.json(
        { error: "This account is already linked to another team profile" },
        { status: 409 },
      )
    }
    console.error("Failed to update member team profile", error)
    return NextResponse.json(
      { error: "Unable to update your team profile" },
      { status: 500 },
    )
  }
}

class TeamProfileAccessError extends Error {}
