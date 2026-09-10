import { NextResponse } from "next/server"
import connectDB from "@/lib/mongodb"
import Blog from "@/models/Blog"
import Project from "@/models/Project"
import Event from "@/models/Event"
import RSVP from "@/models/RSVP"
import Gallery from "@/models/Gallery"
import User from "@/models/User"
import ContactQuery from "@/models/ContactQuery"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"

export async function GET() {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user || session.user.role !== "admin") {
      return NextResponse.json({ error: "Admin access required" }, { status: session ? 403 : 401 })
    }
    await connectDB()

    const [
      totalBlogs,
      publishedBlogs,
      totalProjects,
      totalEvents,
      upcomingEvents,
      totalRSVPs,
      totalGalleries,
      totalUsers,
      totalQueries,
    ] = await Promise.all([
      Blog.countDocuments(),
      Blog.countDocuments({ published: true }),
      Project.countDocuments(),
      Event.countDocuments(),
      Event.countDocuments({ date: { $gte: new Date() } }),
      RSVP.countDocuments(), // Count all RSVPs since they're all attending now
      Gallery.countDocuments(),
      User.countDocuments(),
      ContactQuery.countDocuments(),
    ])

    const stats = {
      queries: { total: totalQueries },
      blogs: {
        total: totalBlogs,
        published: publishedBlogs,
        draft: totalBlogs - publishedBlogs,
      },
      projects: {
        total: totalProjects,
      },
      events: {
        total: totalEvents,
        upcoming: upcomingEvents,
        past: totalEvents - upcomingEvents,
      },
      rsvps: {
        total: totalRSVPs,
      },
      galleries: {
        total: totalGalleries,
      },
      users: {
        total: totalUsers,
      },
    }

    return NextResponse.json(stats)
  } catch (error) {
    return NextResponse.json({ error: "Failed to fetch admin stats" }, { status: 500 })
  }
}
