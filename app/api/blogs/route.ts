import { type NextRequest, NextResponse } from "next/server"
import connectDB from "@/lib/mongodb"
import Blog from "@/models/Blog"
import User from "@/models/User"
import { blogSchema } from "@/lib/validations"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import { escapeRegex } from "@/lib/utils"
import sanitizeHtml from "sanitize-html"

// Helper function to generate slug from title
function generateSlug(title: string): string {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9 -]/g, "") // Remove special characters
    .replace(/\s+/g, "-") // Replace spaces with hyphens
    .replace(/-+/g, "-") // Replace multiple hyphens with single hyphen
    .trim()
}

export async function GET(request: NextRequest) {
  try {
    await connectDB()

    const { searchParams } = new URL(request.url)
    const published = searchParams.get("published")
    const search = searchParams.get("search")?.trim().slice(0, 100)
    const requestedPage = Number.parseInt(searchParams.get("page") || "1", 10)
    const requestedLimit = Number.parseInt(searchParams.get("limit") || "10", 10)
    const page = Number.isInteger(requestedPage) && requestedPage > 0 ? requestedPage : 1
    const limit = Number.isInteger(requestedLimit) ? Math.min(Math.max(requestedLimit, 1), 50) : 10
    const skip = (page - 1) * limit

    const session = published === "true" ? null : await getServerSession(authOptions)
    const filter: Record<string, unknown> = session?.user?.role === "admin" && published !== "true"
      ? {}
      : { published: true }
    if (search) {
      const pattern = new RegExp(escapeRegex(search), "i")
      filter.$or = [{ title: pattern }, { excerpt: pattern }, { tags: pattern }]
    }

    const blogs = await Blog.find(filter)
      .populate("author", session?.user?.role === "admin" ? "name email" : "name")
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(limit)

    const total = await Blog.countDocuments(filter)

    return NextResponse.json({
      blogs,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit),
      },
    })
  } catch (error) {
    console.error("Blog fetch error:", error)
    return NextResponse.json({ error: "Failed to fetch blogs" }, { status: 500 })
  }
}

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)

    if (!session?.user || session.user.role !== "admin") {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    const body = await request.json()

    // Generate slug if not provided
    if (!body.slug && body.title) {
      body.slug = generateSlug(body.title)
    }

    // Handle empty featuredImage
    if (body.featuredImage === "") {
      delete body.featuredImage
    }

    // Convert published boolean to status
    if (body.published !== undefined) {
      body.status = body.published ? "published" : "draft"
      delete body.published
    }

    const validatedData = blogSchema.parse(body)

    await connectDB()

    // Find the user to get the ObjectId
    const user = await User.findOne({ email: session.user.email })
    if (!user) {
      return NextResponse.json({ error: "User not found" }, { status: 404 })
    }

    // Check if slug already exists and make it unique
    let finalSlug = validatedData.slug || generateSlug(body.title)
    const existingBlog = await Blog.findOne({ slug: finalSlug })
    if (existingBlog) {
      finalSlug = `${finalSlug}-${Date.now()}`
    }

    const blog = await Blog.create({
      ...validatedData,
      content: sanitizeHtml(validatedData.content),
      slug: finalSlug,
      author: user._id,
      published: validatedData.status === "published",
    })

    const populatedBlog = await Blog.findById(blog._id).populate("author", "name")

    return NextResponse.json(populatedBlog, { status: 201 })
  } catch (error) {
    console.error("Blog creation error:", error)
    if (error instanceof Error && error.name === "ZodError") {
      return NextResponse.json(
        {
          error: "Validation failed",
          details: (error as any).errors,
        },
        { status: 400 },
      )
    }
    return NextResponse.json({ error: "Failed to create blog" }, { status: 500 })
  }
}
