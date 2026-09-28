import mongoose from "mongoose"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import connectDB from "@/lib/mongodb"
import { Initiative } from "@/models/Initiative"
import User from "@/models/User"

export async function initiativeActor() {
  const session = await getServerSession(authOptions)
  if (!session?.user?.id || !mongoose.isValidObjectId(session.user.id)) return null
  await connectDB()
  const user = await User.findById(session.user.id).select("role").lean()
  if (!user) return null
  return { id: session.user.id, admin: user.role === "admin" }
}

export async function accessibleInitiative(id: string, actor: { id: string; admin: boolean }) {
  if (!mongoose.isValidObjectId(id)) return null
  const initiative = await Initiative.findById(id)
  if (!initiative) return null
  if (!actor.admin && !initiative.participants.some((person: mongoose.Types.ObjectId) => person.toString() === actor.id)) return null
  return initiative
}

export function participantIds(initiative: { participants: mongoose.Types.ObjectId[] }) {
  return initiative.participants.map(person => person.toString())
}
