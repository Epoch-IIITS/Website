import { type NextRequest, NextResponse } from "next/server"
import connectDB from "@/lib/mongodb"
import Blog from "@/models/Blog"
import sanitizeHtml from "sanitize-html"

export async function GET(request: NextRequest, { params }: { params: Promise<{ slug: string }> }) {
  try {
    const { slug } = await params
    await connectDB()

    const blog = await Blog.findOne({ slug, published: true }).populate("author", "name")

    if (!blog) {
      return NextResponse.json({ error: "Blog not found" }, { status: 404 })
    }

    const value = blog.toObject()
    value.content = sanitizeHtml(value.content)
    return NextResponse.json(value)
  } catch (error) {
    console.error("Blog fetch error:", error)
    return NextResponse.json({ error: "Failed to fetch blog" }, { status: 500 })
  }
}
