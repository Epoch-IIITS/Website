import { type NextRequest, NextResponse } from "next/server"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import connectDB from "@/lib/mongodb"
import { escapeRegex } from "@/lib/utils"
import AuditLog from "@/models/AuditLog"

const actions = new Set(["create", "update", "delete"])
const entityTypes = new Set([
  "blog",
  "project",
  "event",
  "gallery",
  "user",
  "contact-query",
  "qr-code",
  "team-year",
  "team-person",
  "team-appointment",
  "team-settings",
  "team-request",
])

function validDate(value: string | null, endOfDay = false) {
  if (!value) return null
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return undefined
  const [year, month, day] = value.split("-").map(Number)
  const daysInMonth = new Date(Date.UTC(year, month, 0)).getUTCDate()
  if (month < 1 || month > 12 || day < 1 || day > daysInMonth) return undefined
  const date = new Date(`${value}T${endOfDay ? "23:59:59.999" : "00:00:00.000"}+05:30`)
  return Number.isNaN(date.getTime()) ? undefined : date
}

export async function GET(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user || session.user.role !== "admin") {
      return NextResponse.json(
        { error: "Admin access required" },
        { status: session ? 403 : 401 },
      )
    }

    const pageValue = request.nextUrl.searchParams.get("page") || "1"
    const page = Number(pageValue)
    const action = request.nextUrl.searchParams.get("action") || ""
    const entityType = request.nextUrl.searchParams.get("entityType") || ""
    const search = request.nextUrl.searchParams.get("search")?.trim() || ""
    const from = validDate(request.nextUrl.searchParams.get("from"))
    const to = validDate(request.nextUrl.searchParams.get("to"), true)

    if (
      !Number.isSafeInteger(page)
      || page < 1
      || page > 100000
      || (action && !actions.has(action))
      || (entityType && !entityTypes.has(entityType))
      || search.length > 100
      || from === undefined
      || to === undefined
      || (from && to && from > to)
    ) {
      return NextResponse.json({ error: "Invalid log filters" }, { status: 400 })
    }

    const filter: Record<string, any> = { expiresAt: { $gt: new Date() } }
    if (action) filter.action = action
    if (entityType) filter.entityType = entityType
    if (from || to) {
      filter.createdAt = {
        ...(from ? { $gte: from } : {}),
        ...(to ? { $lte: to } : {}),
      }
    }
    if (search) {
      const pattern = new RegExp(escapeRegex(search), "i")
      filter.$or = [
        { entityLabel: pattern },
        { summary: pattern },
        { "actor.name": pattern },
        { "actor.email": pattern },
      ]
    }

    const limit = 25
    await connectDB()
    const [logs, total] = await Promise.all([
      AuditLog.find(filter)
        .select("-expiresAt")
        .sort({ createdAt: -1, _id: -1 })
        .skip((page - 1) * limit)
        .limit(limit)
        .lean(),
      AuditLog.countDocuments(filter),
    ])

    return NextResponse.json(
      {
        logs,
        pagination: {
          page,
          total,
          pages: Math.ceil(total / limit),
          limit,
        },
      },
      { headers: { "Cache-Control": "no-store" } },
    )
  } catch (error) {
    console.error("Audit log fetch error:", error)
    return NextResponse.json({ error: "Unable to load activity logs" }, { status: 500 })
  }
}
