import { z } from "zod";

export const idSchema = z.string().regex(/^[a-f\d]{24}$/i, "Invalid record ID");
const text = (max: number) => z.string().trim().max(max);
export const profileSchema = z.object({
  name: text(100).min(1, "Name is required"),
  linkedin: text(300).refine((v) => {
    if (!v) return true;
    try {
      const url = new URL(v);
      return (
        url.protocol === "https:" &&
        ["linkedin.com", "www.linkedin.com"].includes(url.hostname) &&
        !url.username &&
        !url.password &&
        /^\/in\/[^/]+\/?$/.test(url.pathname)
      );
    } catch {
      return false;
    }
  }, "Use a LinkedIn profile URL, such as https://www.linkedin.com/in/name"),
  currentRole: text(120),
  organization: text(120),
  tagline: text(180),
  photo: text(500).refine(
    (v) => !v || /^https:\/\/res\.cloudinary\.com\/[^\s]+$/.test(v),
    "Upload a profile photo",
  ),
});
export const yearSchema = z
  .object({
    year: z.number().int().min(2000).max(2200),
    published: z.boolean(),
    groups: z
      .array(z.object({ id: z.string().min(1).max(80), name: text(80).min(1) }))
      .min(1)
      .max(30),
  })
  .refine(
    (v) => new Set(v.groups.map((g) => g.id)).size === v.groups.length,
    "Group IDs must be unique",
  )
  .refine(
    (v) =>
      new Set(v.groups.map((g) => g.name.toLowerCase())).size ===
      v.groups.length,
    "Group headings must be unique within an academic year",
  );
export const appointmentSchema = z.object({
  personId: idSchema,
  yearId: idSchema,
  groupId: z.string().min(1).max(80),
  por: text(100).default(""),
  order: z.number().int().min(0).max(10000),
  published: z.boolean(),
});
export const settingsSchema = z.object({
  title: text(100).min(1),
  introduction: text(1000),
  ctaTitle: text(100).min(1),
  ctaText: text(500),
});
export const requestSchema = profileSchema.extend({
  year: z.number().int().min(2000).max(2200),
  group: text(80),
  por: text(100).default(""),
  notes: text(2000),
  consent: z.literal(true),
});
export const defaultSettings = {
  title: "The People behind Epoch",
  introduction:
    "Builders, thinkers, and curious minds. Meet the people bringing our community to life, one academic year at a time.",
  ctaTitle: "Part of the Epoch story?",
  ctaText:
    "Current members and alumni: share your details and help us complete our team directory.",
};
export type TeamProfile = z.infer<typeof profileSchema> & { _id: string };
export type TeamYearData = z.infer<typeof yearSchema> & { _id: string };
export type TeamAppointmentData = z.infer<typeof appointmentSchema> & {
  _id: string;
};
