import { type NextRequest, NextResponse } from "next/server"
import connectDB from "@/lib/mongodb"
import Gallery from "@/models/Gallery"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import { gallerySchema } from "@/lib/validations"
import { countChange, diffAuditFields, runAuditedMutation } from "@/lib/audit-log"
import {
  attemptMediaCleanup,
  ensureMediaStorage,
  reconcileMediaUrls,
} from "@/lib/media-assets"

interface RouteParams {
  params: Promise<{ id: string }>
}

export async function GET(request: NextRequest, { params }: RouteParams) {
  try {
    const { id } = await params
    console.log("Fetching gallery with ID:", id)

    await connectDB()

    const gallery = await Gallery.findById(id)
    if (!gallery) {
      console.log("Gallery not found for ID:", id)
      return NextResponse.json({ error: "Gallery not found" }, { status: 404 })
    }

    console.log("Gallery found:", gallery.eventName)
    return NextResponse.json(gallery)
  } catch (error) {
    console.error("Gallery fetch error:", error)
    return NextResponse.json({ error: "Failed to fetch gallery" }, { status: 500 })
  }
}

export async function PUT(request: NextRequest, { params }: RouteParams) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user || session.user.role !== "admin") {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    const { id } = await params
    const body = gallerySchema.parse(await request.json())

    await connectDB()
    await ensureMediaStorage()

    const cleanupPublicIds = new Set<string>()
    const gallery = await runAuditedMutation(session, request, async (databaseSession) => {
      const before = await Gallery.findById(id).session(databaseSession)
      if (!before) return { value: null, logs: [] }

      const updated = await Gallery.findByIdAndUpdate(
        id,
        { $set: { ...body, eventDate: new Date(body.eventDate) } },
        {
          returnDocument: "after",
          runValidators: true,
          session: databaseSession,
        },
      )
      const changes = [
        ...diffAuditFields(before, updated, ["eventName", "eventDate", "description"]),
        ...countChange("images", before.images, updated?.images || []),
      ]
      const queued = await reconcileMediaUrls({
        beforeUrls: before.images.map((image: { url: string }) => image.url),
        afterUrls: (updated?.images || []).map((image: { url: string }) => image.url),
        reason: `Image removed from gallery ${id}`,
        session: databaseSession,
      })
      queued.forEach((publicId) => cleanupPublicIds.add(publicId))
      return {
        value: updated,
        logs: changes.length ? [{
          action: "update",
          entityType: "gallery",
          entityId: id,
          entityLabel: updated?.eventName || before.eventName,
          summary: `Updated gallery “${updated?.eventName || before.eventName}”`,
          changes,
          sideEffects: queued.length ? { cloudinaryImagesQueued: queued.length } : undefined,
        }] : [],
      }
    })
    if (!gallery) {
      return NextResponse.json({ error: "Gallery not found" }, { status: 404 })
    }

    await attemptMediaCleanup([...cleanupPublicIds])
    return NextResponse.json(gallery)
  } catch (error: any) {
    console.error("Gallery update error:", error)
    if (error?.issues) {
      return NextResponse.json({ error: error.issues[0].message }, { status: 400 })
    }
    return NextResponse.json({ error: "Failed to update gallery" }, { status: 500 })
  }
}

export async function DELETE(request: NextRequest, { params }: RouteParams) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user || session.user.role !== "admin") {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    const { id } = await params
    await connectDB()
    await ensureMediaStorage()

    const cleanupPublicIds = new Set<string>()
    const gallery = await runAuditedMutation(session, request, async (databaseSession) => {
      const deleted = await Gallery.findByIdAndDelete(id, { session: databaseSession })
      const queued = deleted ? await reconcileMediaUrls({
        beforeUrls: deleted.images.map((image: { url: string }) => image.url),
        afterUrls: [],
        reason: `Deleted gallery ${id}`,
        session: databaseSession,
      }) : []
      queued.forEach((publicId) => cleanupPublicIds.add(publicId))
      return {
        value: deleted,
        logs: deleted ? [{
          action: "delete",
          entityType: "gallery",
          entityId: id,
          entityLabel: deleted.eventName,
          summary: `Deleted gallery “${deleted.eventName}”`,
          changes: [
            ...diffAuditFields(deleted, {}, ["eventName", "eventDate", "description"]),
            ...countChange("images", deleted.images, []),
          ],
          sideEffects: queued.length ? { cloudinaryImagesQueued: queued.length } : undefined,
        }] : [],
      }
    })
    if (!gallery) {
      return NextResponse.json({ error: "Gallery not found" }, { status: 404 })
    }

    await attemptMediaCleanup([...cleanupPublicIds])
    return NextResponse.json({ message: "Gallery deleted successfully" })
  } catch (error) {
    console.error("Gallery delete error:", error)
    return NextResponse.json({ error: "Failed to delete gallery" }, { status: 500 })
  }
}
