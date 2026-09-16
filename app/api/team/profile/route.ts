import type { ClientSession } from "mongoose"
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
import {
  ensureTeamStorage,
  TeamAppointment,
  TeamPerson,
  TeamRequest,
} from "@/models/Team"

export const dynamic = "force-dynamic"

type MemberProfile = {
  person: any
}

function normalizeEmail(value: unknown) {
  return typeof value === "string" ? value.trim().toLowerCase() : ""
}

function withSession<T extends { session: (session: ClientSession) => T }>(
  query: T,
  session?: ClientSession,
) {
  return session ? query.session(session) : query
}

async function findMemberProfile(
  userId: string,
  email: string,
  session?: ClientSession,
): Promise<MemberProfile | null> {
  if (email) {
    const emailPersonQuery = TeamPerson.findOne({ email }).select("+userId +email")
    const emailPerson = await withSession(emailPersonQuery, session)
    if (emailPerson) {
      const membershipQuery = TeamAppointment.exists({ personId: emailPerson._id })
      if (await withSession(membershipQuery, session)) {
        return { person: emailPerson }
      }
    }
  }

  const ownedPersonQuery = TeamPerson.findOne({ userId }).select("+userId +email")
  const ownedPerson = await withSession(ownedPersonQuery, session)

  if (
    ownedPerson &&
    (!ownedPerson.email || normalizeEmail(ownedPerson.email) === email)
  ) {
    const membershipQuery = TeamAppointment.exists({ personId: ownedPerson._id })
    const hasMembership = await withSession(membershipQuery, session)
    if (hasMembership) {
      return { person: ownedPerson }
    }
  }

  // Requests approved before TeamPerson stored account ownership can still be
  // resolved safely through their saved appointment.
  const requestQuery = TeamRequest.findOne({
    status: "approved",
    appointmentId: { $ne: null },
    $or: [{ userId }, ...(email ? [{ email }] : [])],
  })
    .sort({ reviewedAt: -1, createdAt: -1 })
    .select("appointmentId")
  const approvedRequest = await withSession(requestQuery, session)
  if (!approvedRequest?.appointmentId) return null

  const appointmentQuery = TeamAppointment.findById(
    approvedRequest.appointmentId,
  ).select("personId")
  const appointment = await withSession(appointmentQuery, session)
  if (!appointment?.personId) return null

  const personQuery = TeamPerson.findById(appointment.personId).select(
    "+userId +email",
  )
  const person = await withSession(personQuery, session)
  if (!person) return null
  if (person.email && normalizeEmail(person.email) !== email) return null

  return { person }
}

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
      normalizeEmail(session.user.email),
    )
    const response = membership
      ? NextResponse.json({
          member: true,
          profile: serializeProfile(membership.person),
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
    const email = normalizeEmail(session.user.email)

    await runAuditedMutation(session, request, async (dbSession) => {
      const membership = await findMemberProfile(
        session.user.id,
        email,
        dbSession,
      )
      if (!membership) throw new TeamProfileAccessError()

      updatedPerson = await TeamPerson.findOneAndUpdate(
        { _id: membership.person._id },
        {
          $set: {
            ...value,
            userId: session.user.id,
            ...(email ? { email } : {}),
          },
        },
        { new: true, runValidators: true, session: dbSession },
      )
      if (!updatedPerson) throw new TeamProfileAccessError()

      const removedIds = await reconcileMediaUrls({
        beforeUrls: [membership.person.photo],
        afterUrls: [updatedPerson.photo],
        reason: `Updated by team member ${session.user.id}`,
        session: dbSession,
      })
      removedIds.forEach((publicId) => cleanupIds.add(publicId))

      const changes = diffAuditFields(membership.person, updatedPerson, [
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
