const { test } = require("node:test")
const assert = require("node:assert/strict")
const fs = require("node:fs")
const path = require("node:path")
const vm = require("node:vm")
const ts = require("typescript")

function load(file, mocks = {}) {
  const source = fs.readFileSync(path.join(__dirname, "..", file), "utf8")
  const { outputText } = ts.transpileModule(source, {
    compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020, esModuleInterop: true },
  })
  const context = { exports: {}, console, URL, require: name => name in mocks ? mocks[name] : require(name) }
  vm.runInNewContext(outputText, context, { filename: file })
  return context.exports
}

const validation = load("lib/initiatives/validation.ts")
const json = { NextResponse: { json: (body, options = {}) => ({ body: JSON.parse(JSON.stringify(body)), status: options.status || 200 }) } }
const id = "507f1f77bcf86cd799439011"
const other = "507f1f77bcf86cd799439012"
const outsider = "507f1f77bcf86cd799439013"
const request = body => ({ json: async () => body })
const params = { params: Promise.resolve({ id }) }

function detailRoute({ actor = { id, admin: false, eligible: true }, initiative = {
  _id: id, title: "UG1 Recruitment", status: "active", participants: [{ toString: () => id }, { toString: () => other }],
  createdBy: { toString: () => id },
}, models = {}, audit } = {}) {
  const calls = { writes: 0, logs: [] }
  const defaults = {
    Initiative: { findById: () => ({ session: async () => initiative }), updateOne: async () => { calls.writes++ } },
    InitiativeBlock: { exists: () => ({ session: async () => ({ _id: other }) }) },
    InitiativeReply: { create: async docs => { calls.writes++; return [{ _id: other, ...docs[0] }] } },
    InitiativeTask: { exists: () => ({ session: async () => ({ _id: other }) }) },
    InitiativeTaskComment: { create: async docs => { calls.writes++; return [{ _id: other, ...docs[0] }] } },
  }
  const route = load("app/api/initiatives/[id]/route.ts", {
    mongoose: { connection: { transaction: async mutation => mutation({}) }, Types: { ObjectId: class { constructor(value) { this.value = value } } } },
    "next/server": json,
    "next-auth": { getServerSession: async () => ({ user: { id, role: "admin" } }) },
    "@/lib/auth": { authOptions: {} },
    "@/lib/audit-log": { runAuditedMutation: async (_session, _request, mutation) => { const result = await mutation({}); calls.logs.push(...result.logs); return result.value } },
    "@/lib/media-assets": { ensureMediaStorage: async () => {}, attemptMediaCleanup: async () => {}, reconcileMediaUrls: async () => [] },
    "@/models/User": { countDocuments: async () => 2 },
    "@/models/Initiative": { ...defaults, ...models },
    "@/lib/initiatives/access": { initiativeActor: async () => actor, accessibleInitiative: async () => initiative, participantIds: item => item.participants.map(person => person.toString()) },
    "@/lib/initiatives/validation": validation,
  })
  return { route, calls }
}

test("initiative access rejects signed-out users and users outside a workspace", async () => {
  const signedOut = detailRoute({ actor: null })
  assert.equal((await signedOut.route.PATCH(request({ action: "task.comment.create", taskId: other, body: "Hello", mentions: [] }), params)).status, 401)
  const excluded = detailRoute({ initiative: null })
  assert.equal((await excluded.route.PATCH(request({ action: "task.comment.create", taskId: other, body: "Hello", mentions: [] }), params)).status, 404)
  assert.equal(signedOut.calls.writes + excluded.calls.writes, 0)
})

test("a signed-in nonmember cannot use an invited initiative through its API", async () => {
  const excluded = detailRoute({ actor: { id, admin: false, eligible: false } })
  const response = await excluded.route.PATCH(request({ action: "task.comment.create", taskId: other, body: "Hello", mentions: [] }), params)
  assert.equal(response.status, 403)
  assert.equal(response.body.error, "Team membership required")
  assert.equal(excluded.calls.writes, 0)
})

test("completed initiatives reject participant writes", async () => {
  const { route, calls } = detailRoute({ initiative: { _id: id, status: "completed", participants: [{ toString: () => id }] } })
  assert.equal((await route.PATCH(request({ action: "task.comment.create", taskId: other, body: "Hello", mentions: [] }), params)).status, 409)
  assert.equal(calls.writes, 0)
})

test("a mention must refer to an initiative participant", async () => {
  const { route, calls } = detailRoute()
  assert.equal((await route.PATCH(request({ action: "task.comment.create", taskId: other, body: "Hello", mentions: [outsider] }), params)).status, 400)
  assert.equal(calls.writes, 0)
})

test("comments attach to an existing task in the initiative", async () => {
  const { route, calls } = detailRoute()
  assert.equal((await route.PATCH(request({ action: "task.comment.create", taskId: other, body: "@Lokesh what is the update?", mentions: [id] }), params)).status, 200)
  assert.equal(calls.writes, 2)
  const missing = detailRoute({ models: { InitiativeTask: { exists: () => ({ session: async () => null }) } } })
  assert.equal((await missing.route.PATCH(request({ action: "task.comment.create", taskId: other, body: "Update?", mentions: [] }), params)).status, 404)
  assert.equal(missing.calls.writes, 0)
  assert.equal(validation.initiativeAction.safeParse({ action: "message.create", body: "Old chat", mentions: [] }).success, false)
})

test("task status can be changed with a status-only action", async () => {
  let update
  const { route, calls } = detailRoute({ models: {
    InitiativeTask: { findOneAndUpdate: async (_filter, change) => { update = change; calls.writes++; return { _id: other } } },
  } })
  assert.equal((await route.PATCH(request({ action: "task.status", id: other, status: "done" }), params)).status, 200)
  assert.equal(update.$set.status, "done")
  assert.deepEqual(Object.keys(update.$set), ["status"])
  assert.equal(calls.logs.length, 0)
  assert.equal(validation.initiativeAction.safeParse({ action: "task.status", id: other, status: "in_progress" }).success, false)
})

test("members cannot delete another person's task", async () => {
  const { route, calls } = detailRoute({ models: {
    InitiativeTask: {
      findOne: () => ({ session: async () => ({ createdBy: other }) }),
      deleteOne: async () => { calls.writes++ },
    },
  } })
  assert.equal((await route.PATCH(request({ action: "task.delete", id: other }), params)).status, 403)
  assert.equal(calls.writes, 0)
})

test("stale canvas edits return a conflict before changing the card", async () => {
  const { route, calls } = detailRoute({ models: {
    InitiativeBlock: {
      findOne: () => ({ session: async () => ({ url: "" }) }),
      findOneAndUpdate: async () => null,
    },
  } })
  const response = await route.PATCH(request({
    action: "block.update", id: other, version: 0, title: "Shared note", content: "New text",
    url: "", taggedUsers: [], x: 0, y: 0,
  }), params)
  assert.equal(response.status, 409)
  assert.equal(calls.writes, 0)
})

test("canvas card dimensions are validated and saved with the card update", async () => {
  let update
  const { route } = detailRoute({ models: {
    InitiativeBlock: {
      findOne: () => ({ session: async () => ({ url: "" }) }),
      findOneAndUpdate: async (_filter, change) => { update = change; return { _id: other } },
    },
  } })
  const change = { action: "block.update", id: other, version: 0, title: "Shared note", content: "Plan", url: "", taggedUsers: [], x: 10, y: 20, width: 520, height: 310 }
  assert.equal((await route.PATCH(request(change), params)).status, 200)
  assert.equal(update.$set.width, 520)
  assert.equal(update.$set.height, 310)
  assert.equal((await route.PATCH(request({ ...change, width: undefined, height: undefined }), params)).status, 200)
  assert.equal("width" in update.$set, false)
  assert.equal("height" in update.$set, false)
  assert.equal((await route.PATCH(request({ ...change, width: 100 }), params)).status, 400)
})

test("question replies stay attached to an existing question board", async () => {
  const { route, calls } = detailRoute()
  const result = await route.PATCH(request({ action: "reply.create", blockId: other, body: "Try a hands-on session" }), params)
  assert.equal(result.status, 200)
  assert.equal(calls.writes, 2)
  const missing = detailRoute({ models: { InitiativeBlock: { exists: () => ({ session: async () => null }) } } })
  assert.equal((await missing.route.PATCH(request({ action: "reply.create", blockId: other, body: "Idea" }), params)).status, 404)
  assert.equal(missing.calls.writes, 0)
})

test("only admins may archive and audited admin writes share the mutation", async () => {
  const initiative = {
    _id: id, title: "Intro Session", status: "active", completedAt: undefined,
    participants: [{ toString: () => id }], createdBy: { toString: () => id },
    $session: () => {}, save: async () => {},
  }
  const member = detailRoute({ initiative })
  assert.equal((await member.route.PATCH(request({ action: "status", status: "completed" }), params)).status, 403)
  const admin = detailRoute({ actor: { id, admin: true, eligible: true }, initiative })
  assert.equal((await admin.route.PATCH(request({ action: "status", status: "completed" }), params)).status, 200)
  assert.equal(initiative.status, "completed")
  assert.equal(admin.calls.logs[0].entityType, "initiative")
  assert.match(admin.calls.logs[0].summary, /Archived/)
})

test("only admins can delete an initiative and deletion cascades through its content", async () => {
  const removed = []
  const initiative = { _id: id, title: "Intro Session", status: "active", participants: [{ toString: () => id }] }
  const models = {
    Initiative: {
      findById: () => ({ session: async () => initiative }),
      deleteOne: async () => { removed.push("initiative") },
    },
    InitiativeTask: { deleteMany: async () => { removed.push("tasks"); return { deletedCount: 2 } } },
    InitiativeTaskComment: { deleteMany: async () => { removed.push("comments"); return { deletedCount: 3 } } },
    InitiativeBlock: {
      find: () => ({ select: () => ({ session: () => ({ lean: async () => [] }) }) }),
      deleteMany: async () => { removed.push("blocks"); return { deletedCount: 1 } },
    },
    InitiativeReply: { deleteMany: async () => { removed.push("replies"); return { deletedCount: 4 } } },
  }
  const member = detailRoute({ initiative, models })
  assert.equal((await member.route.DELETE(request({}), params)).status, 403)
  assert.equal(removed.length, 0)
  const admin = detailRoute({ actor: { id, admin: true, eligible: true }, initiative, models })
  assert.equal((await admin.route.DELETE(request({}), params)).status, 200)
  assert.deepEqual(removed, ["tasks", "comments", "blocks", "replies", "initiative"])
  assert.equal(admin.calls.logs[0].action, "delete")
  assert.match(admin.calls.logs[0].summary, /3 comments/)
})

test("initiative creation is restricted to admins", async () => {
  const route = load("app/api/initiatives/route.ts", {
    "next/server": json,
    "next-auth": { getServerSession: async () => null },
    "@/lib/auth": { authOptions: {} },
    "@/lib/audit-log": { runAuditedMutation: async () => { throw new Error("unexpected") } },
    "@/models/User": {},
    "@/models/Initiative": {},
    "@/lib/initiatives/access": { initiativeActor: async () => ({ id, admin: false, eligible: true }) },
    "@/lib/initiatives/validation": validation,
  })
  assert.equal((await route.POST(request({ title: "UG1 Recruitment" }))).status, 403)
})

test("the participant directory groups Team appointments by year and linked account", async () => {
  const yearId = "507f1f77bcf86cd799439014"
  const people = [
    { _id: id, name: "Lokesh", email: "lokesh@example.com" },
    { _id: other, name: "Khyati", email: "khyati@example.com" },
  ]
  const years = [{ _id: yearId, year: 2026, published: true, groups: [{ id: "executive", name: "Executive Committee" }] }]
  const appointments = [
    { personId: "person-1", yearId, groupId: "executive" },
    { personId: "person-2", yearId, groupId: "executive" },
    { personId: "person-3", yearId, groupId: "executive" },
  ]
  const teamPeople = [
    { _id: "person-1", userId: id, email: "" },
    { _id: "person-2", userId: "", email: "KHYATI@example.com" },
    { _id: "person-3", userId: "", email: "missing@example.com" },
  ]
  const sorted = value => ({ select: () => ({ sort: () => ({ lean: async () => value }) }) })
  const selected = value => ({ select: () => ({ lean: async () => value }) })
  let actor = { id, admin: false, eligible: true }
  const route = load("app/api/initiatives/people/route.ts", {
    "next/server": json,
    "@/models/User": { find: () => sorted(people) },
    "@/models/Team": {
      TeamYear: { find: () => sorted(years) },
      TeamAppointment: { find: () => selected(appointments) },
      TeamPerson: { find: () => selected(teamPeople) },
    },
    "@/lib/initiatives/access": { initiativeActor: async () => actor },
  })
  assert.equal((await route.GET()).status, 403)
  actor = { id, admin: true, eligible: true }
  const response = await route.GET()
  assert.equal(response.status, 200)
  assert.deepEqual(response.body.teamYears[0].groups[0].userIds, [id, other])
  assert.equal(response.body.teamYears[0].groups[0].unlinkedCount, 1)
})

test("a deleted account cannot retain initiative access through an old session", async () => {
  const access = load("lib/initiatives/access.ts", {
    mongoose: { isValidObjectId: () => true },
    "next-auth": { getServerSession: async () => ({ user: { id, role: "admin" } }) },
    "@/lib/auth": { authOptions: {} },
    "@/lib/mongodb": async () => {},
    "@/models/Initiative": { Initiative: {} },
    "@/models/User": { findById: () => ({ select: () => ({ lean: async () => null }) }) },
    "@/lib/team-membership": { findMemberProfile: async () => null, normalizeTeamEmail: email => email },
  })
  assert.equal(await access.initiativeActor(), null)
})

test("initiative eligibility follows historical team membership and admins bypass it", async () => {
  let memberProfile = { _id: other }
  let role = "user"
  const access = load("lib/initiatives/access.ts", {
    mongoose: { isValidObjectId: () => true },
    "next-auth": { getServerSession: async () => ({ user: { id } }) },
    "@/lib/auth": { authOptions: {} },
    "@/lib/mongodb": async () => {},
    "@/models/Initiative": { Initiative: {} },
    "@/models/User": { findById: () => ({ select: () => ({ lean: async () => ({ role, email: "member@example.com" }) }) }) },
    "@/lib/team-membership": { findMemberProfile: async () => memberProfile, normalizeTeamEmail: email => email },
  })
  assert.equal((await access.initiativeActor()).eligible, true)
  memberProfile = null
  assert.equal((await access.initiativeActor()).eligible, false)
  role = "admin"
  assert.equal((await access.initiativeActor()).eligible, true)
})
