const { test } = require("node:test")
const assert = require("node:assert/strict")
const fs = require("node:fs")
const path = require("node:path")
const vm = require("node:vm")
const ts = require("typescript")
const mongoose = require("mongoose")

function load(file, mocks = {}, globals = {}) {
  const source = fs.readFileSync(path.join(__dirname, "..", file), "utf8")
  const { outputText } = ts.transpileModule(source, {
    compilerOptions: {
      module: ts.ModuleKind.CommonJS,
      target: ts.ScriptTarget.ES2020,
      esModuleInterop: true,
    },
  })
  const context = {
    exports: {},
    require: (name) => (name in mocks ? mocks[name] : require(name)),
    Date,
    URL,
    RegExp,
    Set,
    Buffer,
    process,
    ...globals,
  }
  vm.runInNewContext(outputText, context, { filename: file })
  return context.exports
}

test("production auth exposes Google only, while development keeps the local credentials provider", () => {
  const providers = {
    "next-auth/providers/google": (options) => ({ id: "google", options }),
    "next-auth/providers/credentials": (options) => ({ id: "credentials", options }),
    bcryptjs: {},
    "@/models/User": {},
    "./mongodb": async () => {},
  }
  const original = process.env.NODE_ENV
  try {
    process.env.NODE_ENV = "production"
    assert.equal(load("lib/auth.ts", providers).authOptions.providers.map((provider) => provider.id).join(","), "google")
    process.env.NODE_ENV = "development"
    assert.equal(load("lib/auth.ts", providers).authOptions.providers.map((provider) => provider.id).join(","), "google,credentials")
  } finally {
    process.env.NODE_ENV = original
  }
})

test("legacy event timestamps are corrected once and normalized timestamps are unchanged", () => {
  const { eventDateForUse } = load("lib/event-dates.ts")
  const stored = "2026-09-11T18:00:00.000Z"
  assert.equal(eventDateForUse(stored, false).toISOString(), "2026-09-11T12:30:00.000Z")
  assert.equal(eventDateForUse(stored, true).toISOString(), stored)
})

test("blog save middleware works with Mongoose 9 and preserves a collision-safe slug", async () => {
  delete mongoose.models.Blog
  const Blog = load("models/Blog.ts").default
  const blog = new Blog({ title: "Repeated title", slug: "repeated-title-123" })
  await Blog.schema.s.hooks.execPre("save", blog, [])
  assert.equal(blog.slug, "repeated-title-123")
})

test("content validation rejects executable URL schemes", () => {
  const { projectSchema, gallerySchema } = load("lib/validations.ts")
  assert.equal(projectSchema.safeParse({
    title: "Unsafe",
    description: "Unsafe link",
    githubUrl: "javascript:alert(1)",
  }).success, false)
  assert.equal(gallerySchema.safeParse({
    eventName: "Gallery",
    eventDate: "2026-09-11",
    images: [{ url: "javascript:alert(1)" }],
  }).success, false)
})

test("the general upload and RSVP-admin APIs reject anonymous requests before storage access", async () => {
  const next = {
    NextResponse: {
      json: (body, options = {}) => ({ body, status: options.status || 200 }),
    },
  }
  const cloudinary = { config() {}, uploader: {} }
  const upload = load("app/api/upload/route.ts", {
    "next/server": next,
    cloudinary: { v2: cloudinary },
    "next-auth": { getServerSession: async () => null },
    "@/lib/auth": { authOptions: {} },
  })
  assert.equal((await upload.POST({ formData: async () => { throw new Error("must not parse") } })).status, 401)

  let connected = false
  const rsvps = load("app/api/admin/events/[id]/rsvps/route.ts", {
    "next/server": next,
    "next-auth": { getServerSession: async () => null },
    "@/lib/auth": { authOptions: {} },
    "@/lib/mongodb": async () => { connected = true },
    "@/models/RSVP": {},
  })
  const response = await rsvps.GET({}, { params: Promise.resolve({ id: "507f1f77bcf86cd799439011" }) })
  assert.equal(response.status, 401)
  assert.equal(connected, false)
})

test("RSVP capacity slots have a per-event unique index", () => {
  delete mongoose.models.RSVP
  const RSVP = load("models/RSVP.ts").default
  const capacityIndex = RSVP.schema.indexes().find(([fields]) => fields.event === 1 && fields.capacitySlot === 1)
  assert.ok(capacityIndex)
  assert.equal(capacityIndex[1].unique, true)
})

test("ticket generator creates a PDF using the project fonts", async () => {
  const { generateTicketPDF } = load("lib/ticket-generator.ts")
  const pdf = await generateTicketPDF({
    eventTitle: "Test Event",
    eventDate: new Date("2026-09-12T07:30:00.000Z"),
    eventVenue: "G04",
    attendeeName: "Epoch Member",
    attendeeEmail: "member@example.com",
    ticketId: "TKT-TEST-123",
  })

  assert.ok(pdf.length > 1_000)
  assert.equal(pdf.subarray(0, 5).toString(), "%PDF-")
})

test("QR validation restricts tracking to links and rejects low-contrast branding", () => {
  const { qrCodeSchema } = load("lib/validations.ts")
  const valid = {
    name: "Epoch website",
    content: "https://epoch.iiits.ac.in",
    trackingEnabled: true,
    foregroundColor: "#0f172a",
    backgroundColor: "#ffffff",
    size: 512,
    margin: 2,
    errorCorrectionLevel: "M",
  }

  assert.equal(qrCodeSchema.safeParse(valid).success, true)
  assert.equal(qrCodeSchema.safeParse({ ...valid, content: "plain text" }).success, false)
  assert.equal(qrCodeSchema.safeParse({ ...valid, foregroundColor: "#ffffff" }).success, false)
})

test("QR scans have one aggregate record per code and privacy fingerprint", () => {
  delete mongoose.models.QRCodeScan
  const QRCodeScan = load("models/QRCodeScan.ts").default
  const uniqueIndex = QRCodeScan.schema.indexes().find(([fields]) => fields.qrCode === 1 && fields.fingerprintHash === 1)
  assert.ok(uniqueIndex)
  assert.equal(uniqueIndex[1].unique, true)
})

test("QR admin APIs reject anonymous requests before database access", async () => {
  let connected = false
  const next = {
    NextResponse: {
      json: (body, options = {}) => ({ body, status: options.status || 200 }),
    },
  }
  const route = load("app/api/admin/qr-codes/route.ts", {
    "next/server": next,
    "next-auth": { getServerSession: async () => null },
    "@/lib/auth": { authOptions: {} },
    "@/lib/mongodb": async () => { connected = true },
    "@/lib/validations": {},
    "@/lib/qr-code": {},
    "@/models/GeneratedQRCode": {},
    "@/models/QRCodeScan": {},
  })

  assert.equal((await route.GET({})).status, 401)
  assert.equal((await route.POST({})).status, 401)
  assert.equal(connected, false)
})

test("QR deletion is admin-only and removes its scan aggregates", async () => {
  const next = {
    NextResponse: {
      json: (body, options = {}) => ({ body, status: options.status || 200 }),
    },
  }
  let connected = false
  const anonymousRoute = load("app/api/admin/qr-codes/[id]/route.ts", {
    "next/server": next,
    "next-auth": { getServerSession: async () => null },
    mongoose: {},
    "@/lib/auth": { authOptions: {} },
    "@/lib/mongodb": async () => { connected = true },
    "@/models/GeneratedQRCode": {},
    "@/models/QRCodeScan": {},
  })
  const params = { params: Promise.resolve({ id: "507f1f77bcf86cd799439011" }) }
  assert.equal((await anonymousRoute.DELETE({}, params)).status, 401)
  assert.equal(connected, false)

  let deletedScans = false
  const adminRoute = load("app/api/admin/qr-codes/[id]/route.ts", {
    "next/server": next,
    "next-auth": { getServerSession: async () => ({ user: { id: "admin", role: "admin" } }) },
    mongoose: {
      Types: { ObjectId: { isValid: () => true } },
      connection: { transaction: async callback => callback("transaction") },
    },
    "@/lib/auth": { authOptions: {} },
    "@/lib/mongodb": async () => {},
    "@/models/GeneratedQRCode": {
      findByIdAndDelete: async (id, options) => {
        assert.equal(id, "507f1f77bcf86cd799439011")
        assert.equal(options.session, "transaction")
        return { _id: id }
      },
    },
    "@/models/QRCodeScan": {
      deleteMany: async (filter, options) => {
        assert.equal(filter.qrCode, "507f1f77bcf86cd799439011")
        assert.equal(options.session, "transaction")
        deletedScans = true
      },
    },
  })
  assert.equal((await adminRoute.DELETE({}, params)).status, 200)
  assert.equal(deletedScans, true)
})
