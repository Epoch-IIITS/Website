import { NextRequest, NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import connectDB from "@/lib/mongodb";
import { TeamRequest, ensureTeamStorage } from "@/models/Team";
import { requestSchema } from "@/lib/team-validation";

export async function GET() {
  const session = await getServerSession(authOptions);
  if (!session?.user?.id)
    return NextResponse.json({ error: "Please sign in" }, { status: 401 });
  try {
    await connectDB();
    const requests = await TeamRequest.find({ userId: session.user.id })
      .select("name year por status reason createdAt")
      .sort({ createdAt: -1 })
      .lean();
    return NextResponse.json(
      { requests },
      { headers: { "Cache-Control": "no-store" } },
    );
  } catch {
    return NextResponse.json(
      { error: "Unable to load your requests" },
      { status: 500 },
    );
  }
}
export async function POST(req: NextRequest) {
  const session = await getServerSession(authOptions);
  if (!session?.user?.id || !session.user.email)
    return NextResponse.json({ error: "Please sign in" }, { status: 401 });
  try {
    const value = requestSchema.parse(await req.json());
    await connectDB();
    await ensureTeamStorage();
    await TeamRequest.create({
      ...value,
      userId: session.user.id,
      email: session.user.email,
    });
    return NextResponse.json({ success: true }, { status: 201 });
  } catch (error: any) {
    return NextResponse.json(
      {
        error:
          error.code === 11000
            ? "You already have a pending request for this year"
            : error.issues?.[0]?.message || "Unable to submit your request",
      },
      { status: 400 },
    );
  }
}
