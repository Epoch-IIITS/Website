import { type NextRequest, NextResponse } from "next/server"
import connectDB from "@/lib/mongodb"
import Project from "@/models/Project"
import { projectSchema } from "@/lib/validations"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import { escapeRegex } from "@/lib/utils"

export async function GET(request: NextRequest) {
  try {
    await connectDB()

    const { searchParams } = new URL(request.url)
    const featured = searchParams.get("featured")
    const search = searchParams.get("search")?.trim().slice(0, 100)

    const filter: Record<string, unknown> = featured === "true" ? { featured: true } : {}
    if (search) {
      const pattern = new RegExp(escapeRegex(search), "i")
      filter.$or = [{ title: pattern }, { description: pattern }, { techStack: pattern }]
    }

    const projects = await Project.find(filter).sort({ createdAt: -1 })

    return NextResponse.json(projects)
  } catch (error) {
    return NextResponse.json({ error: "Failed to fetch projects" }, { status: 500 })
  }
}

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)

    if (!session?.user || session.user.role !== "admin") {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    const body = await request.json()
    const validatedData = projectSchema.parse(body)

    await connectDB()

    const project = await Project.create(validatedData)

    return NextResponse.json(project, { status: 201 })
  } catch (error) {
    if (error instanceof Error) {
      return NextResponse.json({ error: error.message }, { status: 400 })
    }
    return NextResponse.json({ error: "Failed to create project" }, { status: 500 })
  }
}
