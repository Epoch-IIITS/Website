import { type NextRequest, NextResponse } from "next/server";
import connectDB from "@/lib/mongodb";
import RSVP from "@/models/RSVP";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";

export async function GET(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const session = await getServerSession(authOptions);
    if (!session?.user || session.user.role !== "admin") {
      return NextResponse.json(
        { error: "Admin access required" },
        { status: session ? 403 : 401 },
      );
    }
    const { id } = await params; // Await the params Promise
    await connectDB();

    const rsvps = await RSVP.find({ event: id })
      .populate("user", "name email image")
      .populate("event", "title date venue")
      .sort({ createdAt: -1 });

    // Filter out RSVPs where event might be deleted
    const validRsvps = rsvps.filter(rsvp => rsvp.event !== null);

    const stats = {
      attending: validRsvps.length, // All RSVPs are attending since RSVPs are binary now
      notAttending: 0, // No longer applicable
      maybe: 0, // No longer applicable
      total: validRsvps.length,
    };

    return NextResponse.json({
      rsvps: validRsvps,
      stats,
    });
  } catch (error) {
    return NextResponse.json({ error: "Failed to fetch event RSVPs" }, { status: 500 });
  }
}
