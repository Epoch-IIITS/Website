import { type NextRequest, NextResponse } from "next/server"
import connectDB from "@/lib/mongodb"
import Event from "@/models/Event"
import User from "@/models/User"
import { eventSchema } from "@/lib/validations"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import RSVP from "@/models/RSVP"
import { eventForResponse } from "@/lib/event-dates"
import mongoose from "mongoose"

export async function GET(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params
    await connectDB()

    const event = await Event.findById(id).populate("createdBy", "name")

    if (!event) {
      return NextResponse.json({ error: "Event not found" }, { status: 404 })
    }

    return NextResponse.json(eventForResponse(event))
  } catch (error) {
    return NextResponse.json({ error: "Failed to fetch event" }, { status: 500 })
  }
}

export async function PUT(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params
    const session = await getServerSession(authOptions)

    if (!session?.user || session.user.role !== "admin") {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    const body = await request.json()
    const validatedData = eventSchema.parse(body)

    await connectDB()

    // Find the user to get the ObjectId
    const user = await User.findOne({ email: session.user.email })
    if (!user) {
      return NextResponse.json({ error: "User not found" }, { status: 404 })
    }
    if (validatedData.maxAttendees) {
      const registrations = await RSVP.countDocuments({ event: id })
      if (validatedData.maxAttendees < registrations) {
        return NextResponse.json(
          { error: `Capacity cannot be lower than the ${registrations} existing registrations` },
          { status: 400 },
        )
      }
    }

    const eventUpdate: Record<string, unknown> = {
      ...validatedData,
      createdBy: user._id,
      date: new Date(validatedData.date),
      timezoneNormalized: true,
    }
    delete eventUpdate.rsvpDeadline
    if (validatedData.rsvpDeadline) {
      eventUpdate.rsvpDeadline = new Date(validatedData.rsvpDeadline)
    }
    if (validatedData.maxAttendees === undefined) delete eventUpdate.maxAttendees

    const unset: Record<string, 1> = {}
    if (!validatedData.rsvpDeadline) unset.rsvpDeadline = 1
    if (validatedData.maxAttendees === undefined) unset.maxAttendees = 1

    const event = await Event.findByIdAndUpdate(
      id,
      { $set: eventUpdate, ...(Object.keys(unset).length ? { $unset: unset } : {}) },
      { new: true, runValidators: true },
    ).populate("createdBy", "name")

    if (!event) {
      return NextResponse.json({ error: "Event not found" }, { status: 404 })
    }

    return NextResponse.json(eventForResponse(event))
  } catch (error) {
    if (error instanceof Error) {
      return NextResponse.json({ error: error.message }, { status: 400 })
    }
    return NextResponse.json({ error: "Failed to update event" }, { status: 500 })
  }
}

export async function DELETE(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params
    const session = await getServerSession(authOptions)

    if (!session?.user || session.user.role !== "admin") {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    await connectDB()

    let deleted = false
    await mongoose.connection.transaction(async (transaction) => {
      const event = await Event.findByIdAndDelete(id, { session: transaction })
      if (!event) return
      await RSVP.deleteMany({ event: id }, { session: transaction })
      deleted = true
    })

    if (!deleted) {
      return NextResponse.json({ error: "Event not found" }, { status: 404 })
    }

    return NextResponse.json({ message: "Event deleted successfully" })
  } catch (error) {
    return NextResponse.json({ error: "Failed to delete event" }, { status: 500 })
  }
}
