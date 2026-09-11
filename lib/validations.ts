import { z } from "zod"

function isHttpUrlValue(value: string) {
  try {
    const protocol = new URL(value).protocol
    return protocol === "http:" || protocol === "https:"
  } catch {
    return false
  }
}

function colorLuminance(hex: string) {
  const channels = [1, 3, 5].map(index => Number.parseInt(hex.slice(index, index + 2), 16) / 255)
  const [red, green, blue] = channels.map(channel => channel <= 0.03928 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4)
  return 0.2126 * red + 0.7152 * green + 0.0722 * blue
}

const httpUrl = z.string().url().refine(isHttpUrlValue, "URL must use http or https")

export const contactQuerySchema = z.object({
  firstName: z.string().trim().min(1, "First name is required").max(80),
  lastName: z.string().trim().min(1, "Last name is required").max(80),
  email: z.string().trim().email("Enter a valid email address").max(254).toLowerCase(),
  subject: z.string().trim().min(1, "Subject is required").max(200),
  message: z.string().trim().min(1, "Message is required").max(5000),
})

export const blogSchema = z.object({
  title: z.string().min(1, "Title is required"),
  content: z.string().min(1, "Content is required"),
  excerpt: z.string().min(1, "Excerpt is required"),
  slug: z.string().min(1, "Slug is required").optional(),
  status: z.enum(["draft", "published"]).default("draft"),
  tags: z.array(z.string()).default([]),
  featuredImage: httpUrl.optional().or(z.literal("")),
  published: z.boolean().default(false),
})

export const projectSchema = z.object({
  title: z.string().min(1, "Title is required"),
  description: z.string().min(1, "Description is required"),
  techStack: z.array(z.string()).default([]),
  githubUrl: httpUrl.optional().or(z.literal("")),
  liveUrl: httpUrl.optional().or(z.literal("")),
  image: httpUrl.optional().or(z.literal("")),
  featured: z.boolean().default(false),
})

export const eventSchema = z.object({
  title: z.string().min(1, "Title is required"),
  description: z.string().min(1, "Description is required"),
  date: z.string().min(1, "Date is required").refine((value) => !Number.isNaN(Date.parse(value)), "Invalid date"),
  venue: z.string().min(1, "Venue is required"),
  image: httpUrl.optional().or(z.literal("")),
  maxAttendees: z.number().int().positive().optional(),
  rsvpDeadline: z.string().optional().refine((value) => !value || !Number.isNaN(Date.parse(value)), "Invalid RSVP deadline"),
}).superRefine((value, context) => {
  if (value.rsvpDeadline && new Date(value.rsvpDeadline) > new Date(value.date)) {
    context.addIssue({
      code: z.ZodIssueCode.custom,
      path: ["rsvpDeadline"],
      message: "RSVP deadline cannot be after the event",
    })
  }
})

export const gallerySchema = z.object({
  eventName: z.string().min(1, "Event name is required"),
  eventDate: z.string().min(1, "Event date is required").refine((value) => !Number.isNaN(Date.parse(value)), "Invalid event date"),
  description: z.string().optional(),
  images: z
    .array(
      z.object({
        url: httpUrl,
        caption: z.string().optional(),
      }),
    )
    .min(1, "At least one image is required"),
})

export const rsvpSchema = z.object({
  eventId: z.string().min(1, "Event ID is required"),
})

export const qrCodeSchema = z.object({
  name: z.string().trim().min(1, "Name is required").max(100, "Name must be 100 characters or fewer"),
  content: z.string().trim().min(1, "Enter a URL or text").max(2000, "QR content must be 2,000 characters or fewer"),
  trackingEnabled: z.boolean().default(false),
  foregroundColor: z.string().regex(/^#[0-9a-f]{6}$/i, "Choose a valid foreground color"),
  backgroundColor: z.string().regex(/^#[0-9a-f]{6}$/i, "Choose a valid background color"),
  size: z.union([z.literal(256), z.literal(512), z.literal(1024)]),
  margin: z.number().int().min(0).max(8),
  errorCorrectionLevel: z.enum(["M", "H"]),
}).superRefine((value, context) => {
  if (value.trackingEnabled && !isHttpUrlValue(value.content)) {
    context.addIssue({
      code: z.ZodIssueCode.custom,
      path: ["trackingEnabled"],
      message: "Tracking is available only for http or https URLs",
    })
  }

  const foreground = colorLuminance(value.foregroundColor)
  const background = colorLuminance(value.backgroundColor)
  const contrast = (Math.max(foreground, background) + 0.05) / (Math.min(foreground, background) + 0.05)
  if (contrast < 3) {
    context.addIssue({
      code: z.ZodIssueCode.custom,
      path: ["backgroundColor"],
      message: "Choose foreground and background colors with more contrast",
    })
  }
})
