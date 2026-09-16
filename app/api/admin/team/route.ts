import { NextRequest, NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import connectDB from "@/lib/mongodb";
import {
  diffAuditFields,
  runAuditedMutation,
  type AuditDraft,
} from "@/lib/audit-log";
import {
  attemptMediaCleanup,
  ensureMediaStorage,
  reconcileMediaUrls,
} from "@/lib/media-assets";
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
  personSchema,
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
        TeamPerson.find().select("+email").sort({ name: 1 }).lean(),
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
    await ensureMediaStorage();
    if (body.id) idSchema.parse(body.id);
    // All related writes share a transaction, including their audit records.
    const cleanupPublicIds = new Set<string>();
    await runAuditedMutation(admin, req, async (session) => {
      const options = { session, runValidators: true };
      const logs: AuditDraft[] = [];
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
          const before = await TeamYear.findById(body.id).session(session);
          if (!before)
            throw new TeamInputError("Year not found");
          const updated = await TeamYear.findByIdAndUpdate(
            body.id,
            value,
            { ...options, returnDocument: "after" },
          );
          const changes = diffAuditFields(before, updated, [
            "year",
            "published",
            "groups",
          ]);
          if (changes.length)
            logs.push({
              action: "update",
              entityType: "team-year",
              entityId: body.id,
              entityLabel: `AY ${updated?.year || before.year}`,
              summary: `Updated academic year ${updated?.year || before.year}`,
              changes,
            });
        } else {
          const created = (await TeamYear.create([value], { session }))[0];
          logs.push({
            action: "create",
            entityType: "team-year",
            entityId: created._id.toString(),
            entityLabel: `AY ${created.year}`,
            summary: `Created academic year ${created.year}`,
            changes: diffAuditFields({}, created, ["year", "published", "groups"]),
          });
        }
      } else if (body.action === "current") {
        const year = await TeamYear.findOne({
          _id: idSchema.parse(body.id),
          published: true,
        }).session(session);
        if (!year)
          throw new TeamInputError("Publish the year before making it current");
        const before = await TeamSettings.findById("team").session(session);
        const updated = await TeamSettings.findOneAndUpdate(
          { _id: "team" },
          { $set: { currentYearId: year._id } },
          { ...options, upsert: true, returnDocument: "after" },
        );
        const changes = diffAuditFields(before, updated, ["currentYearId"]);
        if (changes.length)
          logs.push({
            action: before ? "update" : "create",
            entityType: "team-settings",
            entityId: "team",
            entityLabel: "Team settings",
            summary: `Made AY ${year.year} the current academic year`,
            changes,
          });
      } else if (body.action === "person") {
        const value = personSchema.parse(body.value);
        const { email, ...profile } = value;
        if (body.id) {
          const before = await TeamPerson.findById(body.id)
            .select("+email +userId")
            .session(session);
          if (!before)
            throw new TeamInputError("Person not found");
          const emailChanged = (before.email || "") !== email;
          const updated = await TeamPerson.findByIdAndUpdate(
            body.id,
            {
              $set: { ...profile, ...(email ? { email } : {}) },
              ...(emailChanged || !email
                ? { $unset: { userId: 1, ...(!email ? { email: 1 } : {}) } }
                : {}),
            },
            { ...options, returnDocument: "after" },
          );
          const queued = await reconcileMediaUrls({
            beforeUrls: [before.photo],
            afterUrls: [updated?.photo],
            reason: `Photo removed from team profile ${body.id}`,
            session,
          });
          queued.forEach((publicId) => cleanupPublicIds.add(publicId));
          const changes = diffAuditFields(before, updated, [
            "name",
            "linkedin",
            "currentRole",
            "organization",
            "photo",
            "tagline",
          ]);
          if (emailChanged)
            changes.push({
              field: "accountLink",
              before: before.email ? "linked" : null,
              after: email ? "linked" : null,
            });
          if (changes.length)
            logs.push({
              action: "update",
              entityType: "team-person",
              entityId: body.id,
              entityLabel: updated?.name || before.name,
              summary: `Updated team profile “${updated?.name || before.name}”`,
              changes,
              sideEffects: queued.length
                ? { cloudinaryImagesQueued: queued.length }
                : undefined,
            });
        } else {
          const created = (
            await TeamPerson.create(
              [{ ...profile, ...(email ? { email } : {}) }],
              { session },
            )
          )[0];
          await reconcileMediaUrls({
            beforeUrls: [],
            afterUrls: [created.photo],
            reason: `Attached to team profile ${created._id}`,
            session,
          });
          logs.push({
            action: "create",
            entityType: "team-person",
            entityId: created._id.toString(),
            entityLabel: created.name,
            summary: `Created team profile “${created.name}”`,
            changes: diffAuditFields({}, created, [
              "name",
              "linkedin",
              "currentRole",
              "organization",
              "photo",
              "tagline",
            ]).concat(
              email
                ? [{ field: "accountLink", before: null, after: "linked" }]
                : [],
            ),
          });
        }
      } else if (body.action === "appointment") {
        const value = appointmentSchema.parse(body.value);
        const year = await TeamYear.findById(value.yearId).session(session);
        if (!year?.groups.some((g: any) => g.id === value.groupId))
          throw new TeamInputError("Select a group in this academic year");
        if (
          !(await TeamPerson.exists({ _id: value.personId }).session(session))
        )
          throw new TeamInputError("Person not found");
        const person = await TeamPerson.findById(value.personId).session(session);
        const label = `${person?.name || "Team member"}, AY ${year.year}`;
        if (body.id) {
          const before = await TeamAppointment.findById(body.id).session(session);
          if (!before)
            throw new TeamInputError("Appointment not found");
          const updated = await TeamAppointment.findByIdAndUpdate(
            body.id,
            value,
            { ...options, returnDocument: "after" },
          );
          const changes = diffAuditFields(before, updated, [
            "personId",
            "yearId",
            "groupId",
            "por",
            "order",
            "published",
          ]);
          if (changes.length)
            logs.push({
              action: "update",
              entityType: "team-appointment",
              entityId: body.id,
              entityLabel: label,
              summary: `Updated appointment for ${label}`,
              changes,
            });
        } else {
          const created = (
            await TeamAppointment.create([value], { session })
          )[0];
          logs.push({
            action: "create",
            entityType: "team-appointment",
            entityId: created._id.toString(),
            entityLabel: label,
            summary: `Created appointment for ${label}`,
            changes: diffAuditFields({}, created, [
              "personId",
              "yearId",
              "groupId",
              "por",
              "order",
              "published",
            ]),
          });
        }
      } else if (body.action === "remove-appointment") {
        const id = idSchema.parse(body.id);
        const deleted = await TeamAppointment.findByIdAndDelete(id, { session });
        if (!deleted) throw new TeamInputError("Appointment not found");
        const person = await TeamPerson.findById(deleted.personId).session(session);
        const year = await TeamYear.findById(deleted.yearId).session(session);
        const label = `${person?.name || "Team member"}, AY ${year?.year || "unknown"}`;
        logs.push({
          action: "delete",
          entityType: "team-appointment",
          entityId: id,
          entityLabel: label,
          summary: `Removed appointment for ${label}`,
          changes: diffAuditFields(deleted, {}, [
            "personId",
            "yearId",
            "groupId",
            "por",
            "order",
            "published",
          ]),
        });
      } else if (body.action === "settings") {
        const before = await TeamSettings.findById("team").session(session);
        const updated = await TeamSettings.findOneAndUpdate(
          { _id: "team" },
          { $set: settingsSchema.parse(body.value) },
          { ...options, upsert: true, returnDocument: "after" },
        );
        const changes = diffAuditFields(before, updated, [
          "title",
          "introduction",
          "ctaTitle",
          "ctaText",
        ]);
        if (changes.length)
          logs.push({
            action: before ? "update" : "create",
            entityType: "team-settings",
            entityId: "team",
            entityLabel: "Team page settings",
            summary: `${before ? "Updated" : "Created"} team page settings`,
            changes,
          });
      } else if (body.action === "review") {
        const request = await TeamRequest.findOne({
          _id: idSchema.parse(body.id),
          status: "pending",
        }).session(session);
        if (!request)
          throw new TeamInputError(
            "This request has already been reviewed or no longer exists",
          );
        const requestBefore = request.toObject();
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
          const requestEmail = String(request.email || "").trim().toLowerCase();
          const accountPerson = await TeamPerson.findOne({
            $or: [{ userId: request.userId }, { email: requestEmail }],
          })
            .select("_id")
            .session(session);
          if (
            accountPerson &&
            body.personId &&
            accountPerson._id.toString() !== body.personId
          )
            throw new TeamInputError(
              "This account is already linked to another team profile",
            );
          let personId = accountPerson?._id.toString() || body.personId;
          if (personId) {
            idSchema.parse(personId);
            const linkedPerson = await TeamPerson.findOneAndUpdate(
              {
                _id: personId,
                $or: [
                  { userId: request.userId },
                  { email: requestEmail },
                  { userId: { $exists: false } },
                  { userId: "" },
                ],
              },
              { $set: { userId: request.userId, email: requestEmail } },
              { new: true, runValidators: true, session },
            );
            if (!linkedPerson) {
              if (!(await TeamPerson.exists({ _id: personId }).session(session)))
                throw new TeamInputError("Person not found");
              throw new TeamInputError(
                "Person is already linked to another account",
              );
            }
          } else {
            const createdPerson = (
              await TeamPerson.create(
                [
                  {
                    ...profile,
                    userId: request.userId,
                    email: requestEmail,
                  },
                ],
                { session },
              )
            )[0];
            await reconcileMediaUrls({
              beforeUrls: [],
              afterUrls: [createdPerson.photo],
              reason: `Attached while approving team request ${request._id}`,
              session,
            });
            personId = createdPerson._id.toString();
            logs.push({
              action: "create",
              entityType: "team-person",
              entityId: personId,
              entityLabel: createdPerson.name,
              summary: `Created team profile “${createdPerson.name}” while approving a request`,
              changes: diffAuditFields({}, createdPerson, [
                "name",
                "linkedin",
                "currentRole",
                "organization",
                "photo",
                "tagline",
              ]),
            });
          }
          const value = appointmentSchema.parse({
            ...body.appointment,
            personId,
          });
          const year = await TeamYear.findById(value.yearId).session(session);
          if (!year?.groups.some((g: any) => g.id === value.groupId))
            throw new TeamInputError("Select a valid academic year and group");
          const appointmentBefore = await TeamAppointment.findOne({
            personId,
            yearId: value.yearId,
          }).session(session);
          const appointment = await TeamAppointment.findOneAndUpdate(
            { personId, yearId: value.yearId },
            { $set: value },
            { ...options, upsert: true, returnDocument: "after" },
          );
          request.status = "approved";
          request.appointmentId = appointment._id;
          const person = await TeamPerson.findById(personId).session(session);
          const appointmentChanges = diffAuditFields(
            appointmentBefore,
            appointment,
            ["personId", "yearId", "groupId", "por", "order", "published"],
          );
          if (appointmentChanges.length)
            logs.push({
              action: appointmentBefore ? "update" : "create",
              entityType: "team-appointment",
              entityId: appointment._id.toString(),
              entityLabel: `${person?.name || request.name}, AY ${year.year}`,
              summary: `${appointmentBefore ? "Updated" : "Created"} an appointment while approving ${request.name}’s request`,
              changes: appointmentChanges,
            });
        } else throw new TeamInputError("Invalid review decision");
        request.reviewedBy = admin.user.id;
        request.reviewedAt = new Date();
        await request.save({ session });
        logs.push({
          action: "update",
          entityType: "team-request",
          entityId: request._id.toString(),
          entityLabel: request.name,
          summary: `${body.decision === "approve" ? "Approved" : "Rejected"} team request from ${request.name}`,
          changes: diffAuditFields(requestBefore, request, [
            "status",
            "reason",
            "appointmentId",
          ]),
        });
      } else throw new TeamInputError("Unknown action");
      return { value: true, logs };
    });
    await attemptMediaCleanup([...cleanupPublicIds]);
    return NextResponse.json({ success: true });
  } catch (error: any) {
    const duplicateAccountLink =
      error?.code === 11000 &&
      (error?.keyPattern?.email || error?.keyPattern?.userId);
    const message =
      duplicateAccountLink
        ? "This account email is already linked to another team profile"
        : error?.code === 11000
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
