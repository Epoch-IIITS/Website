import { NextRequest, NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import mongoose from "mongoose";
import { authOptions } from "@/lib/auth";
import connectDB from "@/lib/mongodb";
import {
  TeamAppointment,
  TeamPerson,
  TeamRequest,
  TeamSettings,
  TeamYear,
  ensureTeamStorage,
} from "@/models/Team";
import {
  appointmentSchema,
  defaultSettings,
  idSchema,
  profileSchema,
  settingsSchema,
  yearSchema,
} from "@/lib/team-validation";

export const dynamic = "force-dynamic";
class TeamInputError extends Error {}
async function authorize() {
  const session = await getServerSession(authOptions);
  return session?.user?.role === "admin" ? session : null;
}
export async function GET() {
  if (!(await authorize()))
    return NextResponse.json(
      { error: "Admin access required" },
      { status: 403 },
    );
  try {
    await connectDB();
    const [years, people, appointments, requests, settings] = await Promise.all(
      [
        TeamYear.find().sort({ year: -1 }).lean(),
        TeamPerson.find().sort({ name: 1 }).lean(),
        TeamAppointment.find().sort({ order: 1 }).lean(),
        TeamRequest.find().sort({ createdAt: -1 }).lean(),
        TeamSettings.findById("team").lean(),
      ],
    );
    return NextResponse.json(
      {
        years,
        people,
        appointments,
        requests,
        settings: { ...defaultSettings, ...settings },
      },
      { headers: { "Cache-Control": "no-store" } },
    );
  } catch {
    return NextResponse.json(
      { error: "Unable to load team workspace" },
      { status: 500 },
    );
  }
}
export async function POST(req: NextRequest) {
  const admin = await authorize();
  if (!admin)
    return NextResponse.json(
      { error: "Admin access required" },
      { status: 403 },
    );
  try {
    const body = await req.json();
    await connectDB();
    await ensureTeamStorage();
    if (body.id) idSchema.parse(body.id);
    // All related writes share a transaction, including publication and request approval.
    await mongoose.connection.transaction(async (session) => {
      const options = { session, runValidators: true };
      if (body.action === "year") {
        const value = yearSchema.parse(body.value);
        if (body.id) {
          const current = await TeamSettings.findById("team").session(session);
          if (!value.published && String(current?.currentYearId) === body.id)
            throw new TeamInputError(
              "Choose another current year before unpublishing this year",
            );
          if (
            await TeamAppointment.exists({
              yearId: body.id,
              groupId: { $nin: value.groups.map((g) => g.id) },
            }).session(session)
          )
            throw new TeamInputError(
              "Move members before removing their group",
            );
          if (!(await TeamYear.findByIdAndUpdate(body.id, value, options)))
            throw new TeamInputError("Year not found");
        } else await TeamYear.create([value], { session });
      } else if (body.action === "current") {
        const year = await TeamYear.findOne({
          _id: idSchema.parse(body.id),
          published: true,
        }).session(session);
        if (!year)
          throw new TeamInputError("Publish the year before making it current");
        await TeamSettings.updateOne(
          { _id: "team" },
          { $set: { currentYearId: year._id } },
          { ...options, upsert: true },
        );
      } else if (body.action === "person") {
        const value = profileSchema.parse(body.value);
        if (body.id) {
          if (!(await TeamPerson.findByIdAndUpdate(body.id, value, options)))
            throw new TeamInputError("Person not found");
        } else await TeamPerson.create([value], { session });
      } else if (body.action === "appointment") {
        const value = appointmentSchema.parse(body.value);
        const year = await TeamYear.findById(value.yearId).session(session);
        if (!year?.groups.some((g: any) => g.id === value.groupId))
          throw new TeamInputError("Select a group in this academic year");
        if (
          !(await TeamPerson.exists({ _id: value.personId }).session(session))
        )
          throw new TeamInputError("Person not found");
        if (body.id) {
          if (
            !(await TeamAppointment.findByIdAndUpdate(body.id, value, options))
          )
            throw new TeamInputError("Appointment not found");
        } else await TeamAppointment.create([value], { session });
      } else if (body.action === "remove-appointment") {
        await TeamAppointment.deleteOne(
          { _id: idSchema.parse(body.id) },
          { session },
        );
      } else if (body.action === "settings") {
        await TeamSettings.updateOne(
          { _id: "team" },
          { $set: settingsSchema.parse(body.value) },
          { ...options, upsert: true },
        );
      } else if (body.action === "review") {
        const request = await TeamRequest.findOne({
          _id: idSchema.parse(body.id),
          status: "pending",
        }).session(session);
        if (!request)
          throw new TeamInputError(
            "This request has already been reviewed or no longer exists",
          );
        if (body.decision === "reject") {
          const reason = String(body.reason || "").trim();
          if (!reason || reason.length > 1000)
            throw new TeamInputError(
              "Provide a rejection reason (up to 1,000 characters)",
            );
          request.status = "rejected";
          request.reason = reason;
        } else if (body.decision === "approve") {
          const profile = profileSchema.parse(body.profile);
          let personId = body.personId;
          if (personId) {
            idSchema.parse(personId);
            if (!(await TeamPerson.exists({ _id: personId }).session(session)))
              throw new TeamInputError("Person not found");
          } else
            personId = (
              await TeamPerson.create([profile], { session })
            )[0]._id.toString();
          const value = appointmentSchema.parse({
            ...body.appointment,
            personId,
          });
          const year = await TeamYear.findById(value.yearId).session(session);
          if (!year?.groups.some((g: any) => g.id === value.groupId))
            throw new TeamInputError("Select a valid academic year and group");
          const appointment = await TeamAppointment.findOneAndUpdate(
            { personId, yearId: value.yearId },
            { $set: value },
            { ...options, upsert: true, new: true },
          );
          request.status = "approved";
          request.appointmentId = appointment._id;
        } else throw new TeamInputError("Invalid review decision");
        request.reviewedBy = admin.user.id;
        request.reviewedAt = new Date();
        await request.save({ session });
      } else throw new TeamInputError("Unknown action");
    });
    return NextResponse.json({ success: true });
  } catch (error: any) {
    const message =
      error?.code === 11000
        ? "This year or person’s appointment already exists"
        : error?.issues?.[0]?.message ||
          (error instanceof TeamInputError
            ? error.message
            : "Unable to save changes. Please try again.");
    return NextResponse.json(
      { error: message },
      {
        status:
          error?.code === 11000 ||
          error?.issues ||
          error instanceof TeamInputError ||
          error instanceof SyntaxError
            ? 400
            : 500,
      },
    );
  }
}
