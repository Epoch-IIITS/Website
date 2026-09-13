import { type NextRequest, NextResponse } from "next/server"
import connectDB from "@/lib/mongodb"
import Project from "@/models/Project"
import { projectSchema } from "@/lib/validations"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import { diffAuditFields, runAuditedMutation } from "@/lib/audit-log"

export async function GET(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params
    await connectDB()

    const project = await Project.findById(id)

    if (!project) {
      return NextResponse.json({ error: "Project not found" }, { status: 404 })
    }

    return NextResponse.json(project)
  } catch (error) {
    return NextResponse.json({ error: "Failed to fetch project" }, { status: 500 })
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
    const validatedData = projectSchema.parse(body)

    await connectDB()

    const project = await runAuditedMutation(session, request, async (databaseSession) => {
      const before = await Project.findById(id).session(databaseSession)
      if (!before) return { value: null, logs: [] }

      const updated = await Project.findByIdAndUpdate(
        id,
        { $set: validatedData },
        { returnDocument: "after", runValidators: true, session: databaseSession },
      )
      const changes = diffAuditFields(before, updated, ["title", "description", "techStack", "githubUrl", "liveUrl", "image", "featured"])
      return {
        value: updated,
        logs: changes.length ? [{
          action: "update",
          entityType: "project",
          entityId: id,
          entityLabel: updated?.title || before.title,
          summary: `Updated project “${updated?.title || before.title}”`,
          changes,
        }] : [],
      }
    })

    if (!project) {
      return NextResponse.json({ error: "Project not found" }, { status: 404 })
    }

    return NextResponse.json(project)
  } catch (error) {
    if (error instanceof Error) {
      return NextResponse.json({ error: error.message }, { status: 400 })
    }
    return NextResponse.json({ error: "Failed to update project" }, { status: 500 })
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

    const project = await runAuditedMutation(session, request, async (databaseSession) => {
      const deleted = await Project.findByIdAndDelete(id, { session: databaseSession })
      return {
        value: deleted,
        logs: deleted ? [{
          action: "delete",
          entityType: "project",
          entityId: id,
          entityLabel: deleted.title,
          summary: `Deleted project “${deleted.title}”`,
          changes: diffAuditFields(deleted, {}, ["title", "description", "techStack", "githubUrl", "liveUrl", "image", "featured"]),
        }] : [],
      }
    })

    if (!project) {
      return NextResponse.json({ error: "Project not found" }, { status: 404 })
    }

    return NextResponse.json({ message: "Project deleted successfully" })
  } catch (error) {
    return NextResponse.json({ error: "Failed to delete project" }, { status: 500 })
  }
}
