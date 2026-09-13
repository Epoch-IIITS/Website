import { type NextRequest, NextResponse } from "next/server"
import connectDB from "@/lib/mongodb"
import Blog from "@/models/Blog"
import User from "@/models/User"
import { blogSchema } from "@/lib/validations"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import { diffAuditFields, runAuditedMutation, textContentChange } from "@/lib/audit-log"
import sanitizeHtml from "sanitize-html"

export async function GET(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params
    const session = await getServerSession(authOptions)
    if (!session?.user || session.user.role !== "admin") {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }
    await connectDB()

    const blog = await Blog.findById(id).populate("author", "name email")

    if (!blog) {
      return NextResponse.json({ error: "Blog not found" }, { status: 404 })
    }

    return NextResponse.json(blog)
  } catch (error) {
    return NextResponse.json({ error: "Failed to fetch blog" }, { status: 500 })
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
    const validatedData = blogSchema.partial().parse(body)

    await connectDB()

    // Find the user to get the ObjectId
    const user = await User.findOne({ email: session.user.email })
    if (!user) {
      return NextResponse.json({ error: "User not found" }, { status: 404 })
    }

    const blog = await runAuditedMutation(session, request, async (databaseSession) => {
      const before = await Blog.findById(id).session(databaseSession)
      if (!before) return { value: null, logs: [] }

      const update: Record<string, unknown> = { ...validatedData, author: user._id }
      if (validatedData.content !== undefined) update.content = sanitizeHtml(validatedData.content)
      if (validatedData.status !== undefined) update.published = validatedData.status === "published"
      delete update.status

      const updated = await Blog.findByIdAndUpdate(
        id,
        update,
        { new: true, runValidators: true, session: databaseSession },
      ).populate("author", "name email")
      const changes = [
        ...diffAuditFields(before, updated, ["title", "slug", "excerpt", "featuredImage", "published", "tags"]),
        ...textContentChange("content", before.content, updated?.content),
      ]
      return {
        value: updated,
        logs: changes.length ? [{
          action: "update",
          entityType: "blog",
          entityId: id,
          entityLabel: updated?.title || before.title,
          summary: `Updated blog “${updated?.title || before.title}”`,
          changes,
        }] : [],
      }
    })

    if (!blog) {
      return NextResponse.json({ error: "Blog not found" }, { status: 404 })
    }

    return NextResponse.json(blog)
  } catch (error) {
    if (error instanceof Error) {
      return NextResponse.json({ error: error.message }, { status: 400 })
    }
    return NextResponse.json({ error: "Failed to update blog" }, { status: 500 })
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

    const blog = await runAuditedMutation(session, request, async (databaseSession) => {
      const deleted = await Blog.findByIdAndDelete(id, { session: databaseSession })
      return {
        value: deleted,
        logs: deleted ? [{
          action: "delete",
          entityType: "blog",
          entityId: id,
          entityLabel: deleted.title,
          summary: `Deleted blog “${deleted.title}”`,
          changes: [
            ...diffAuditFields(deleted, {}, ["title", "slug", "excerpt", "featuredImage", "published", "tags"]),
            ...textContentChange("content", deleted.content, ""),
          ],
        }] : [],
      }
    })

    if (!blog) {
      return NextResponse.json({ error: "Blog not found" }, { status: 404 })
    }

    return NextResponse.json({ message: "Blog deleted successfully" })
  } catch (error) {
    return NextResponse.json({ error: "Failed to delete blog" }, { status: 500 })
  }
}
