import mongoose from "mongoose";

const profileFields = {
  name: { type: String, required: true },
  linkedin: { type: String, default: "" },
  currentRole: { type: String, default: "" },
  organization: { type: String, default: "" },
  photo: { type: String, default: "" },
  tagline: { type: String, default: "" },
};
const year = new mongoose.Schema(
  {
    year: { type: Number, required: true, unique: true },
    published: { type: Boolean, default: false },
    groups: [{ _id: false, id: String, name: String }],
  },
  { timestamps: true },
);
const person = new mongoose.Schema(
  profileFields,
  { timestamps: true },
);
const appointment = new mongoose.Schema(
  {
    personId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "TeamPerson",
      required: true,
    },
    yearId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "TeamYear",
      required: true,
    },
    groupId: { type: String, required: true },
    por: { type: String, default: "" },
    order: { type: Number, default: 0 },
    published: { type: Boolean, default: false },
  },
  { timestamps: true },
);
appointment.index({ personId: 1, yearId: 1 }, { unique: true });
const settings = new mongoose.Schema(
  {
    _id: String,
    currentYearId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "TeamYear",
      default: null,
    },
    title: String,
    introduction: String,
    ctaTitle: String,
    ctaText: String,
  },
  { timestamps: true },
);
const request = new mongoose.Schema(
  {
    ...profileFields,
    year: Number,
    group: String,
    por: { type: String, default: "" },
    notes: String,
    consent: Boolean,
    userId: { type: String, required: true },
    email: { type: String, required: true },
    status: {
      type: String,
      enum: ["pending", "approved", "rejected"],
      default: "pending",
    },
    reason: { type: String, default: "" },
    reviewedBy: String,
    reviewedAt: Date,
    appointmentId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "TeamAppointment",
    },
  },
  { timestamps: true },
);
request.index(
  { userId: 1, year: 1 },
  { unique: true, partialFilterExpression: { status: "pending" } },
);
export const TeamYear =
  mongoose.models.TeamYear || mongoose.model("TeamYear", year);
export const TeamPerson =
  mongoose.models.TeamPerson || mongoose.model("TeamPerson", person);
export const TeamAppointment =
  mongoose.models.TeamAppointment ||
  mongoose.model("TeamAppointment", appointment);
export const TeamSettings =
  mongoose.models.TeamSettings || mongoose.model("TeamSettings", settings);
export const TeamRequest =
  mongoose.models.TeamRequest || mongoose.model("TeamRequest", request);

// Build unique indexes before accepting writes, including on a fresh database.
export async function ensureTeamStorage() {
  await Promise.all(
    [TeamYear, TeamPerson, TeamAppointment, TeamSettings, TeamRequest].map(
      (model) => model.init(),
    ),
  );
}
