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
    Date,
    Error,
    URL,
    RegExp,
    crypto: { randomUUID: () => "operation-1" },
    require: (name) => name in mocks ? mocks[name] : require(name),
    ...globals,
  }
  vm.runInNewContext(outputText, context, { filename: file })
  return context.exports
}

test("audit logs have chronological filter indexes and expire automatically", () => {
  delete mongoose.models.AuditLog
  const AuditLog = load("models/AuditLog.ts").default
  const indexes = AuditLog.schema.indexes()

  const ttl = indexes.find(([fields]) => fields.expiresAt === 1)
  assert.ok(ttl)
  assert.equal(ttl[1].expireAfterSeconds, 0)
  assert.ok(indexes.some(([fields]) => fields.createdAt === -1 && fields._id === -1))
  assert.ok(indexes.some(([fields]) => fields.action === 1 && fields.createdAt === -1))
  assert.ok(indexes.some(([fields]) => fields.entityType === 1 && fields.createdAt === -1))
})

test("audit field diffs normalize values and summarize long content", () => {
  const helper = load("lib/audit-log.ts", {
    mongoose,
    "@/models/AuditLog": {},
  })
  const id = new mongoose.Types.ObjectId()
  const changes = helper.diffAuditFields(
    { title: "Before", owner: id, hidden: "secret" },
    { title: "After", owner: id, hidden: "changed" },
    ["title", "owner"],
  )
  assert.deepEqual(JSON.parse(JSON.stringify(changes)), [
    { field: "title", before: "Before", after: "After" },
  ])
  assert.deepEqual(JSON.parse(JSON.stringify(helper.textContentChange("content", "abc", "abcdef"))), [
    { field: "content", before: "3 characters", after: "6 characters" },
  ])
  assert.deepEqual(JSON.parse(JSON.stringify(helper.countChange("images", [{ url: "a" }], [{ url: "b" }]))), [
    { field: "images", before: "1 item", after: "1 item" },
  ])
})

test("domain and audit writes share one transaction and retain logs for six months", async () => {
  let initialized = false
  let transactionSession
  let inserted
  const AuditLog = {
    init: async () => { initialized = true },
    create: async (documents, options) => {
      inserted = documents
      assert.equal(options.session, transactionSession)
    },
  }
  const fakeMongoose = {
    Types: mongoose.Types,
    connection: {
      transaction: async (callback) => {
        transactionSession = { transaction: true }
        return callback(transactionSession)
      },
    },
  }
  const helper = load("lib/audit-log.ts", {
    mongoose: fakeMongoose,
    "@/models/AuditLog": AuditLog,
  })
  const session = { user: { id: "admin-1", name: "Admin", email: "admin@example.com", role: "admin" } }
  const request = { method: "POST", nextUrl: { pathname: "/api/projects" } }
  const value = await helper.runAuditedMutation(session, request, async (databaseSession) => {
    assert.equal(databaseSession, transactionSession)
    return {
      value: "saved",
      logs: [{
        action: "create",
        entityType: "project",
        entityId: "project-1",
        entityLabel: "Epoch",
        summary: "Created project",
      }],
    }
  })

  assert.equal(value, "saved")
  assert.equal(initialized, true)
  assert.equal(inserted.length, 1)
  assert.equal(inserted[0].operationId, "operation-1")
  assert.equal(inserted[0].actor.email, "admin@example.com")
  assert.equal(inserted[0].route, "/api/projects")
  const expectedExpiry = new Date(inserted[0].createdAt)
  expectedExpiry.setUTCMonth(expectedExpiry.getUTCMonth() + 6)
  assert.equal(inserted[0].expiresAt.toISOString(), expectedExpiry.toISOString())
})

test("an audit write failure rejects the enclosing mutation", async () => {
  const helper = load("lib/audit-log.ts", {
    mongoose: {
      Types: mongoose.Types,
      connection: { transaction: async (callback) => callback({}) },
    },
    "@/models/AuditLog": {
      init: async () => {},
      create: async () => { throw new Error("audit unavailable") },
    },
  })
  await assert.rejects(
    helper.runAuditedMutation(
      { user: { id: "admin", role: "admin" } },
      { method: "DELETE", nextUrl: { pathname: "/api/projects/1" } },
      async () => ({
        value: true,
        logs: [{ action: "delete", entityType: "project", entityId: "1", entityLabel: "One", summary: "Deleted" }],
      }),
    ),
    /audit unavailable/,
  )
})

const next = {
  NextResponse: {
    json: (body, options = {}) => ({
      body: JSON.parse(JSON.stringify(body)),
      status: options.status || 200,
      headers: options.headers,
    }),
  },
}

function logsRoute(session, model, connect = async () => {}) {
  return load("app/api/admin/logs/route.ts", {
    "next/server": next,
    "next-auth": { getServerSession: async () => session },
    "@/lib/auth": { authOptions: {} },
    "@/lib/mongodb": connect,
    "@/lib/utils": { escapeRegex: (value) => value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") },
    "@/models/AuditLog": model,
  })
}

function logRequest(query = "") {
  return { nextUrl: new URL(`http://localhost/api/admin/logs${query}`) }
}

test("activity logs are admin-only before database access", async () => {
  let connected = false
  for (const [session, status] of [[null, 401], [{ user: { role: "user" } }, 403]]) {
    const route = logsRoute(session, {}, async () => { connected = true })
    assert.equal((await route.GET(logRequest())).status, status)
  }
  assert.equal(connected, false)
})

test("activity log filters are validated before database access", async () => {
  let connected = false
  const route = logsRoute({ user: { role: "admin" } }, {}, async () => { connected = true })
  for (const query of ["?page=0", "?action=read", "?entityType=password", "?from=bad", "?from=2026-02-31", "?from=2026-09-02&to=2026-09-01"]) {
    assert.equal((await route.GET(logRequest(query))).status, 400)
  }
  assert.equal(connected, false)
})

test("activity logs use bounded private pagination and exclude expired entries", async () => {
  const calls = {}
  const chain = {
    select(value) { calls.select = value; return this },
    sort(value) { calls.sort = JSON.parse(JSON.stringify(value)); return this },
    skip(value) { calls.skip = value; return this },
    limit(value) { calls.limit = value; return this },
    async lean() { return [{ action: "create", summary: "Created project" }] },
  }
  const model = {
    find(filter) { calls.filter = filter; return chain },
    countDocuments: async () => 26,
  }
  const route = logsRoute({ user: { role: "admin" } }, model)
  const response = await route.GET(logRequest("?page=2&action=create&entityType=project&search=epoch"))
  assert.equal(response.status, 200)
  assert.equal(calls.filter.action, "create")
  assert.equal(calls.filter.entityType, "project")
  assert.ok(calls.filter.expiresAt.$gt instanceof Date)
  assert.equal(calls.skip, 25)
  assert.equal(calls.limit, 25)
  assert.deepEqual(calls.sort, { createdAt: -1, _id: -1 })
  assert.deepEqual(response.body.pagination, { page: 2, total: 26, pages: 2, limit: 25 })
  assert.equal(response.headers["Cache-Control"], "no-store")
})
