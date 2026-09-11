import { type NextRequest, NextResponse } from "next/server"
import connectDB from "@/lib/mongodb"
import RSVP from "@/models/RSVP"
import Event from "@/models/Event"
import User from "@/models/User"
import { getServerSession } from "next-auth/next"
import { authOptions } from "@/lib/auth"
import { generateTicketId } from "@/lib/utils"
import { type Session } from "next-auth"
import mongoose from "mongoose"
import { rsvpSchema } from "@/lib/validations"
import { eventDateForUse } from "@/lib/event-dates"

async function createRsvp(
  eventId: string,
  userId: mongoose.Types.ObjectId,
  capacitySlot?: number,
) {
  for (let attempt = 0; attempt < 3; attempt += 1) {
    try {
      return await RSVP.create({
        event: eventId,
        user: userId,
        ticketId: generateTicketId(),
        capacitySlot,
      })
    } catch (error: any) {
      if (error?.code === 11000 && error?.keyPattern?.ticketId) continue
      throw error
    }
  }
  throw new Error("Unable to allocate a unique ticket ID")
}

export async function POST(request: NextRequest) {
  try {
    const session = (await getServerSession(authOptions)) as Session | null

    if (!session?.user?.email) {
      return NextResponse.json({ error: "Authentication required" }, { status: 401 })
    }

    const { eventId } = rsvpSchema.parse(await request.json())
    if (!mongoose.isValidObjectId(eventId)) {
      return NextResponse.json({ error: "Invalid event ID" }, { status: 400 })
    }

    await connectDB()

    // Find the user to get the ObjectId
    const user = await User.findOne({ email: session.user.email })
    if (!user) {
      return NextResponse.json({ error: "User not found" }, { status: 404 })
    }

    // Check if event exists and is still accepting RSVPs
    const event = await Event.findById(eventId)
    if (!event) {
      return NextResponse.json({ error: "Event not found" }, { status: 404 })
    }

    if (eventDateForUse(event.date, event.timezoneNormalized) < new Date()) {
      return NextResponse.json({ error: "This event has already ended" }, { status: 400 })
    }

    if (
      event.rsvpDeadline &&
      new Date() > eventDateForUse(event.rsvpDeadline, event.timezoneNormalized)
    ) {
      return NextResponse.json({ error: "RSVP deadline has passed" }, { status: 400 })
    }

    // Check if user already RSVP'd
    const existingRSVP = await RSVP.findOne({
      event: eventId,
      user: user._id,
    })

    if (existingRSVP) {
      return NextResponse.json(existingRSVP)
    }

    await RSVP.init()

    let rsvp
    if (event.maxAttendees) {
      const legacyCount = await RSVP.countDocuments({
        event: eventId,
        capacitySlot: { $exists: false },
      })
      if (legacyCount >= event.maxAttendees) {
        return NextResponse.json({ error: "Event is full" }, { status: 400 })
      }

      const occupiedSlots = new Set<number>(
        await RSVP.distinct("capacitySlot", {
          event: eventId,
          capacitySlot: { $exists: true },
        }),
      )
      for (let slot = legacyCount + 1; slot <= event.maxAttendees; slot += 1) {
        if (occupiedSlots.has(slot)) continue
        try {
          rsvp = await createRsvp(eventId, user._id, slot)
          break
        } catch (error: any) {
          if (error?.code !== 11000 || !error?.keyPattern?.capacitySlot) throw error
          const duplicate = await RSVP.findOne({ event: eventId, user: user._id })
          if (duplicate) return NextResponse.json(duplicate)
        }
      }
      if (!rsvp) {
        return NextResponse.json({ error: "Event is full" }, { status: 400 })
      }
    } else {
      rsvp = await createRsvp(eventId, user._id)
    }

    const populatedRSVP = await RSVP.findById(rsvp._id)
      .populate("event", "title date venue")
      .populate("user", "name email")

    return NextResponse.json(populatedRSVP, { status: 201 })
  } catch (error: any) {
    console.error("RSVP creation error:", error)
    if (error?.issues) {
      return NextResponse.json({ error: error.issues[0].message }, { status: 400 })
    }
    if (error?.code === 11000) {
      return NextResponse.json({ error: "You have already registered for this event" }, { status: 409 })
    }
    return NextResponse.json({ error: "Failed to create RSVP" }, { status: 500 })
  }
}

export async function GET(request: NextRequest) {
  try {
    const session = (await getServerSession(authOptions)) as Session | null

    if (!session?.user?.email) {
      return NextResponse.json({ error: "Authentication required" }, { status: 401 })
    }

    await connectDB()

    // Find the user to get the ObjectId
    const user = await User.findOne({ email: session.user.email })
    if (!user) {
      return NextResponse.json({ error: "User not found" }, { status: 404 })
    }

    const rsvps = await RSVP.find({ user: user._id })
      .populate("event", "title date venue image")
      .sort({ createdAt: -1 })

    // Filter out RSVPs where the event has been deleted
    const validRsvps = rsvps.filter(rsvp => rsvp.event !== null)

    return NextResponse.json(validRsvps)
  } catch (error) {
    console.error("RSVPs fetch error:", error)
    return NextResponse.json({ error: "Failed to fetch RSVPs" }, { status: 500 })
  }
}
