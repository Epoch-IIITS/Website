import type { ClientSession } from "mongoose"
import { TeamAppointment, TeamPerson, TeamRequest } from "@/models/Team"

export function normalizeTeamEmail(value: unknown) {
  return typeof value === "string" ? value.trim().toLowerCase() : ""
}

function withSession<T extends { session: (session: ClientSession) => T }>(query: T, session?: ClientSession) {
  return session ? query.session(session) : query
}

export async function findMemberProfile(userId: string, email: string, session?: ClientSession) {
  if (email) {
    const emailPerson = await withSession(TeamPerson.findOne({ email }).select("+userId +email"), session)
    if (emailPerson && await withSession(TeamAppointment.exists({ personId: emailPerson._id }), session)) {
      return emailPerson
    }
  }

  const ownedPerson = await withSession(TeamPerson.findOne({ userId }).select("+userId +email"), session)
  if (ownedPerson && (!ownedPerson.email || normalizeTeamEmail(ownedPerson.email) === email)) {
    if (await withSession(TeamAppointment.exists({ personId: ownedPerson._id }), session)) return ownedPerson
  }

  // Older approved requests can still establish membership through their appointment.
  const approvedRequest = await withSession(TeamRequest.findOne({
    status: "approved",
    appointmentId: { $ne: null },
    $or: [{ userId }, ...(email ? [{ email }] : [])],
  }).sort({ reviewedAt: -1, createdAt: -1 }).select("appointmentId"), session)
  if (!approvedRequest?.appointmentId) return null

  const appointment = await withSession(TeamAppointment.findById(approvedRequest.appointmentId).select("personId"), session)
  if (!appointment?.personId) return null

  const person = await withSession(TeamPerson.findById(appointment.personId).select("+userId +email"), session)
  if (!person || (person.email && normalizeTeamEmail(person.email) !== email)) return null
  return person
}
