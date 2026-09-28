import { NextResponse } from "next/server"
import User from "@/models/User"
import { TeamAppointment, TeamPerson, TeamYear } from "@/models/Team"
import { initiativeActor } from "@/lib/initiatives/access"
import type { TeamGroupOption, TeamYearOption } from "@/components/initiatives/types"

export async function GET() {
  try {
    const actor = await initiativeActor()
    if (!actor) return NextResponse.json({ error: "Sign in required" }, { status: 401 })
    if (!actor.eligible) return NextResponse.json({ error: "Team membership required" }, { status: 403 })
    if (!actor.admin) return NextResponse.json({ error: "Admin access required" }, { status: 403 })
    const [users, years] = await Promise.all([
      User.find().select("name email image").sort({ name: 1 }).lean(),
      TeamYear.find().select("year published groups").sort({ year: -1 }).lean(),
    ])
    const yearIds = years.map(year => year._id)
    const appointments = await TeamAppointment.find({ yearId: { $in: yearIds } }).select("personId yearId groupId").lean()
    const personIds = [...new Set(appointments.map(appointment => String(appointment.personId)))]
    const teamPeople = await TeamPerson.find({ _id: { $in: personIds } }).select("+userId +email name").lean()
    const accountIds = new Set(users.map(user => String(user._id)))
    const accountsByEmail = new Map(users.map(user => [user.email.toLowerCase(), String(user._id)]))
    const teamPeopleById = new Map(teamPeople.map(person => [String(person._id), person]))
    const teamYears: TeamYearOption[] = years.map(year => ({
      _id: String(year._id),
      year: year.year,
      published: year.published,
      groups: year.groups.map((group: { id: string; name: string }): TeamGroupOption => {
        const members = appointments.filter(appointment => String(appointment.yearId) === String(year._id) && appointment.groupId === group.id)
        const userIds: string[] = []
        let unlinkedCount = 0
        for (const member of members) {
          const person = teamPeopleById.get(String(member.personId))
          const linkedId = person?.userId && accountIds.has(person.userId) ? person.userId : person?.email ? accountsByEmail.get(person.email.toLowerCase()) : undefined
          if (linkedId) userIds.push(linkedId)
          else unlinkedCount++
        }
        return { id: group.id, name: group.name, userIds: [...new Set(userIds)], unlinkedCount }
      }),
    }))
    return NextResponse.json({ people: users, teamYears }, { headers: { "Cache-Control": "private, no-store" } })
  } catch (error) {
    console.error("Initiative people error:", error)
    return NextResponse.json({ error: "Unable to load people" }, { status: 500 })
  }
}
