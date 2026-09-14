const { test } = require("node:test")
const assert = require("node:assert/strict")
const fs = require("node:fs")
const path = require("node:path")
const { pathToFileURL } = require("node:url")
const vm = require("node:vm")
const ts = require("typescript")
const mongoose = require("mongoose")

function load(file, mocks = {}) {
  const source = fs.readFileSync(path.join(__dirname, "..", file), "utf8")
  const { outputText } = ts.transpileModule(source, {
    compilerOptions: {
      module: ts.ModuleKind.CommonJS,
      target: ts.ScriptTarget.ES2022,
      esModuleInterop: true,
    },
  })
  const context = {
    exports: {},
    URL,
    Buffer,
    Date,
    Error,
    Map,
    Set,
    process,
    console,
    require: (name) => name in mocks ? mocks[name] : require(name),
  }
  vm.runInNewContext(outputText, context, { filename: file })
  return context.exports
}

async function loadMaintenanceHelpers() {
  const file = path.join(__dirname, "media-maintenance-helpers.mjs")
  return import(`${pathToFileURL(file).href}?test=${Date.now()}`)
}

test("managed Cloudinary URLs preserve legacy IDs and reject unrelated assets", () => {
  const helper = load("lib/cloudinary-media.ts", {
    cloudinary: { v2: { config() {}, uploader: {} } },
  })
  const legacy = helper.parseManagedCloudinaryUrl(
    "https://res.cloudinary.com/epoch-cloud/image/upload/v1700000000/epoch-blogs/legacy.jpg",
    "epoch-cloud",
  )
  assert.equal(legacy.publicId, "epoch-blogs/legacy")
  assert.equal(legacy.folder, "epoch-blogs")
  assert.equal(
    helper.parseManagedCloudinaryUrl(
      "https://res.cloudinary.com/epoch-cloud/image/upload/v1700000000/epoch/gallery/new.webp",
      "epoch-cloud",
    ).publicId,
    "epoch/gallery/new",
  )
  assert.equal(
    helper.parseManagedCloudinaryUrl(
      "https://res.cloudinary.com/another-cloud/image/upload/v1700000000/epoch/gallery/new.webp",
      "epoch-cloud",
    ),
    null,
  )
  assert.equal(
    helper.parseManagedCloudinaryUrl(
      "https://res.cloudinary.com/epoch-cloud/image/upload/v1700000000/unrelated/photo.webp",
      "epoch-cloud",
    ),
    null,
  )
  assert.deepEqual(
    Array.from(helper.extractManagedCloudinaryUrls(
      "Markdown ![photo](https://res.cloudinary.com/epoch-cloud/image/upload/v1700000000/epoch-blogs/inline.jpg)",
      "epoch-cloud",
    )),
    ["https://res.cloudinary.com/epoch-cloud/image/upload/v1700000000/epoch-blogs/inline.jpg"],
  )
})

test("new uploads use resource-specific folders", () => {
  const helper = load("lib/cloudinary-media.ts", {
    cloudinary: { v2: { config() {}, uploader: {} } },
  })
  assert.equal(helper.folderForMediaPurpose("blog"), "epoch/blogs")
  assert.equal(helper.folderForMediaPurpose("project"), "epoch/projects")
  assert.equal(helper.folderForMediaPurpose("event"), "epoch/events")
  assert.equal(helper.folderForMediaPurpose("gallery"), "epoch/gallery")
  assert.equal(helper.folderForMediaPurpose("team"), "epoch/team")
})

test("orphan scans read archived team profile photos from the Mongoose collection", async () => {
  const { readMediaReferenceValues } = await loadMaintenanceHelpers()
  const teamPhoto =
    "https://res.cloudinary.com/epoch-cloud/image/upload/v1700000000/epoch-team/member.jpg"
  const calls = []
  const db = {
    collection(collection) {
      return {
        async distinct(field) {
          calls.push([collection, field])
          return collection === "teampeople" && field === "photo" ? [teamPhoto] : []
        },
      }
    },
  }

  const values = await readMediaReferenceValues(db)

  assert.ok(calls.some(([collection, field]) => collection === "teampeople" && field === "photo"))
  assert.ok(!calls.some(([collection]) => collection === "teampersons"))
  assert.deepEqual(values, [teamPhoto])
})

test("orphan scans enforce and describe the configured cleanup grace period", async () => {
  const {
    MEDIA_CLEANUP_GRACE_MS,
    describeMediaCleanupGracePeriod,
    selectOrphanCandidates,
  } = await loadMaintenanceHelpers()
  const now = Date.parse("2026-09-14T12:00:00.000Z")
  const asset = (publicId, age) => ({
    public_id: publicId,
    secure_url: `https://res.cloudinary.com/epoch-cloud/image/upload/${publicId}.jpg`,
    created_at: new Date(now - age).toISOString(),
  })
  const twentyThreeHoursOld = asset("epoch-team/twenty-three-hours", 23 * 60 * 60 * 1000)
  const twentyFiveHoursOld = asset("epoch-team/twenty-five-hours", 25 * 60 * 60 * 1000)
  const referenced = asset("epoch-team/referenced", 25 * 60 * 60 * 1000)

  const candidates = selectOrphanCandidates(
    [twentyThreeHoursOld, twentyFiveHoursOld, referenced],
    {
      publicIds: new Set([referenced.public_id]),
      urls: new Set([referenced.secure_url]),
    },
    now,
  )

  assert.equal(MEDIA_CLEANUP_GRACE_MS, 24 * 60 * 60 * 1000)
  assert.equal(describeMediaCleanupGracePeriod(), "24 hours")
  assert.deepEqual(candidates.map(({ public_id }) => public_id), [
    twentyFiveHoursOld.public_id,
  ])
})

test("media registry and resolved cleanup records expire automatically", () => {
  delete mongoose.models.MediaAsset
  delete mongoose.models.MediaCleanupJob
  const MediaAsset = load("models/MediaAsset.ts").default
  const CleanupJob = load("models/MediaCleanupJob.ts").default

  for (const model of [MediaAsset, CleanupJob]) {
    const ttl = model.schema.indexes().find(([fields]) => fields.expiresAt === 1)
    assert.ok(ttl)
    assert.equal(ttl[1].expireAfterSeconds, 0)
    assert.ok(model.schema.indexes().some(([fields]) => fields.status === 1 && fields.createdAt === 1))
  }
})

test("reconciliation queues only removed managed assets in the MongoDB session", async () => {
  const assetUpdates = []
  const jobUpdates = []
  const mediaModel = {
    init: async () => {},
    findOneAndUpdate: async (...args) => { assetUpdates.push(args) },
    updateOne: async () => {},
  }
  const jobModel = {
    init: async () => {},
    findOneAndUpdate: async (...args) => { jobUpdates.push(args) },
    updateOne: async () => {},
  }
  const emptyReferenceModel = { distinct: async () => [] }
  const helper = load("lib/media-assets.ts", {
    "@/models/Blog": emptyReferenceModel,
    "@/models/Event": emptyReferenceModel,
    "@/models/Gallery": emptyReferenceModel,
    "@/models/MediaAsset": mediaModel,
    "@/models/MediaCleanupJob": jobModel,
    "@/models/Project": emptyReferenceModel,
    "@/models/Team": { TeamPerson: emptyReferenceModel, TeamRequest: emptyReferenceModel },
    "@/models/User": emptyReferenceModel,
    "@/lib/cloudinary-media": {
      extractManagedCloudinaryUrls: (value) =>
        typeof value === "string" && value.startsWith("managed:") ? [value] : [],
      parseManagedCloudinaryUrl: (url) =>
        typeof url === "string" && url.startsWith("managed:")
          ? { publicId: url.slice(8), resourceType: "image", folder: "epoch/gallery", url }
          : null,
      destroyManagedImage: async () => {},
    },
  })
  const session = { transaction: true }
  const removed = await helper.reconcileMediaUrls({
    beforeUrls: ["managed:old", "https://external.example/image.jpg"],
    afterUrls: ["managed:new"],
    reason: "Gallery update",
    session,
  })

  assert.deepEqual(Array.from(removed), ["old"])
  assert.equal(jobUpdates.length, 1)
  assert.equal(jobUpdates[0][0].publicId, "old")
  assert.equal(jobUpdates[0][2].session, session)
  assert.ok(assetUpdates.some(([filter]) => filter.publicId === "new"))
  assert.ok(assetUpdates.some(([filter]) => filter.publicId === "old"))
})

test("cleanup cancels deletion when another document still references the asset", async () => {
  let destroyed = false
  const updates = []
  const job = { _id: "job-1", publicId: "shared", url: "managed:shared", status: "pending" }
  const jobs = {
    init: async () => {},
    updateMany: async () => {},
    updateOne: async (...args) => { updates.push(args) },
    find: () => ({
      sort() { return this },
      limit() { return this },
      lean: async () => [job],
    }),
    findOneAndUpdate: async () => { throw new Error("referenced assets must not be claimed") },
  }
  const assets = { init: async () => {}, updateOne: async () => {} }
  const referencedModel = { distinct: async () => ["managed:shared"] }
  const emptyModel = { distinct: async () => [] }
  const helper = load("lib/media-assets.ts", {
    "@/models/Blog": referencedModel,
    "@/models/Event": emptyModel,
    "@/models/Gallery": emptyModel,
    "@/models/MediaAsset": assets,
    "@/models/MediaCleanupJob": jobs,
    "@/models/Project": emptyModel,
    "@/models/Team": { TeamPerson: emptyModel, TeamRequest: emptyModel },
    "@/models/User": emptyModel,
    "@/lib/cloudinary-media": {
      extractManagedCloudinaryUrls: (value) =>
        typeof value === "string" && value.startsWith("managed:") ? [value] : [],
      parseManagedCloudinaryUrl: (url) => ({
        publicId: url.slice(8),
        resourceType: "image",
        folder: "epoch/gallery",
        url,
      }),
      destroyManagedImage: async () => { destroyed = true },
    },
  })

  const result = await helper.processMediaCleanupJobs()
  assert.equal(result.cancelled, 1)
  assert.equal(result.completed, 0)
  assert.equal(destroyed, false)
  assert.equal(updates[0][1].$set.status, "cancelled")
})
