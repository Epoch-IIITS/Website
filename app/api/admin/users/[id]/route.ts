import { type NextRequest, NextResponse } from "next/server"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import connectDB from "@/lib/mongodb"
import User from "@/models/User"
import { diffAuditFields, runAuditedMutation } from "@/lib/audit-log"

export async function PATCH(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params
    const session = await getServerSession(authOptions)

    if (!session?.user || session.user.role !== "admin") {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    const { role } = await request.json()

    if (!["admin", "user"].includes(role)) {
      return NextResponse.json({ error: "Invalid role" }, { status: 400 })
    }

    await connectDB()

    const user = await runAuditedMutation(session, request, async (databaseSession) => {
      const before = await User.findById(id)
        .select("name email role")
        .session(databaseSession)
      if (!before) return { value: null, logs: [] }

      const updated = await User.findByIdAndUpdate(
        id,
        { role },
        {
          returnDocument: "after",
          runValidators: true,
          session: databaseSession,
        },
      ).select("name email role")
      const changes = diffAuditFields(before, updated, ["role"])
      return {
        value: updated,
        logs: changes.length ? [{
          action: "update",
          entityType: "user",
          entityId: id,
          entityLabel: updated?.name || updated?.email || before.name,
          summary: `Changed ${updated?.email || before.email} to ${role}`,
          changes,
        }] : [],
      }
    })

    if (!user) {
      return NextResponse.json({ error: "User not found" }, { status: 404 })
    }

    return NextResponse.json(user)
  } catch (error) {
    console.error("User update error:", error)
    return NextResponse.json({ error: "Failed to update user" }, { status: 500 })
  }
}
