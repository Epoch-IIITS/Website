import type { ClientSession } from "mongoose"
import Blog from "@/models/Blog"
import Event from "@/models/Event"
import Gallery from "@/models/Gallery"
import MediaAsset from "@/models/MediaAsset"
import MediaCleanupJob from "@/models/MediaCleanupJob"
import Project from "@/models/Project"
import { TeamPerson, TeamRequest } from "@/models/Team"
import User from "@/models/User"
import {
  destroyManagedImage,
  extractManagedCloudinaryUrls,
  parseManagedCloudinaryUrl,
  type MediaPurpose,
  type UploadedMedia,
} from "@/lib/cloudinary-media"

const RESOLVED_RECORD_RETENTION_MS = 30 * 24 * 60 * 60 * 1000

function expiryFromNow() {
  return new Date(Date.now() + RESOLVED_RECORD_RETENTION_MS)
}

function uniqueManagedAssets(urls: unknown[]) {
  const assets = new Map<string, NonNullable<ReturnType<typeof parseManagedCloudinaryUrl>>>()
  for (const value of urls) {
    for (const url of extractManagedCloudinaryUrls(value)) {
      const parsed = parseManagedCloudinaryUrl(url)
      if (parsed) assets.set(parsed.publicId, parsed)
    }
  }
  return assets
}

export async function ensureMediaStorage() {
  await Promise.all([MediaAsset.init(), MediaCleanupJob.init()])
}

export async function registerUploadedMedia(
  media: UploadedMedia,
  purpose: MediaPurpose,
  uploadedBy: string,
) {
  await ensureMediaStorage()
  await MediaAsset.findOneAndUpdate(
    { publicId: media.publicId },
    {
      $set: {
        assetId: media.assetId,
        url: media.url,
        resourceType: media.resourceType,
        folder: media.folder,
        purpose,
        status: "pending",
        source: "upload",
        uploadedBy,
      },
      $unset: { lastError: 1, deletedAt: 1, expiresAt: 1 },
    },
    { upsert: true, returnDocument: "after", runValidators: true },
  )
}

export async function attachMediaUrls(urls: unknown[], session?: ClientSession) {
  const assets = uniqueManagedAssets(urls)
  for (const asset of assets.values()) {
    await MediaAsset.findOneAndUpdate(
      { publicId: asset.publicId },
      {
        $set: {
          url: asset.url,
          resourceType: asset.resourceType,
          folder: asset.folder,
          status: "attached",
        },
        $setOnInsert: { source: "legacy" },
        $unset: { lastError: 1, deletedAt: 1, expiresAt: 1 },
      },
      {
        upsert: true,
        returnDocument: "after",
        runValidators: true,
        ...(session ? { session } : {}),
      },
    )
    await MediaCleanupJob.updateOne(
      { publicId: asset.publicId, status: { $in: ["pending", "failed"] } },
      {
        $set: { status: "cancelled", completedAt: new Date(), expiresAt: expiryFromNow() },
        $unset: { lastError: 1, processingStartedAt: 1 },
      },
      session ? { session } : {},
    )
  }
}

export async function reconcileMediaUrls({
  beforeUrls,
  afterUrls,
  reason,
  session,
}: {
  beforeUrls: unknown[]
  afterUrls: unknown[]
  reason: string
  session: ClientSession
}) {
  const before = uniqueManagedAssets(beforeUrls)
  const after = uniqueManagedAssets(afterUrls)
  await attachMediaUrls([...after.values()].map((asset) => asset.url), session)

  const removed = [...before.values()].filter((asset) => !after.has(asset.publicId))
  for (const asset of removed) {
    await MediaAsset.findOneAndUpdate(
      { publicId: asset.publicId },
      {
        $set: {
          url: asset.url,
          resourceType: asset.resourceType,
          folder: asset.folder,
          status: "deletion_pending",
        },
        $setOnInsert: { source: "legacy" },
        $unset: { lastError: 1, deletedAt: 1, expiresAt: 1 },
      },
      { upsert: true, returnDocument: "after", runValidators: true, session },
    )
    await MediaCleanupJob.findOneAndUpdate(
      { publicId: asset.publicId },
      {
        $set: {
          url: asset.url,
          resourceType: asset.resourceType,
          reason: reason.slice(0, 300),
          status: "pending",
        },
        $unset: {
          lastError: 1,
          processingStartedAt: 1,
          completedAt: 1,
          expiresAt: 1,
        },
      },
      { upsert: true, returnDocument: "after", runValidators: true, session },
    )
  }

  return removed.map((asset) => asset.publicId)
}

export async function collectReferencedMedia() {
  const values = await Promise.all([
    Blog.distinct("featuredImage", { featuredImage: { $type: "string", $ne: "" } }),
    Blog.distinct("content", { content: /res\.cloudinary\.com/i }),
    Project.distinct("image", { image: { $type: "string", $ne: "" } }),
    Event.distinct("image", { image: { $type: "string", $ne: "" } }),
    Gallery.distinct("images.url", { "images.url": { $type: "string", $ne: "" } }),
    TeamPerson.distinct("photo", { photo: { $type: "string", $ne: "" } }),
    TeamRequest.distinct("photo", { photo: { $type: "string", $ne: "" } }),
    User.distinct("image", { image: { $type: "string", $ne: "" } }),
  ])
  const urls = values
    .flat()
    .flatMap((value) => extractManagedCloudinaryUrls(value))
  return {
    urls: new Set(urls),
    publicIds: new Set(uniqueManagedAssets(urls).keys()),
  }
}

async function resolveReferencedJob(job: { _id: unknown; publicId: string }) {
  const completedAt = new Date()
  await Promise.all([
    MediaCleanupJob.updateOne(
      { _id: job._id },
      {
        $set: { status: "cancelled", completedAt, expiresAt: expiryFromNow() },
        $unset: { lastError: 1, processingStartedAt: 1 },
      },
    ),
    MediaAsset.updateOne(
      { publicId: job.publicId },
      { $set: { status: "attached" }, $unset: { lastError: 1, deletedAt: 1, expiresAt: 1 } },
    ),
  ])
}

export async function processMediaCleanupJobs({
  publicIds,
  includeFailed = false,
  limit = 25,
}: {
  publicIds?: string[]
  includeFailed?: boolean
  limit?: number
} = {}) {
  await ensureMediaStorage()

  const staleProcessing = new Date(Date.now() - 15 * 60 * 1000)
  await MediaCleanupJob.updateMany(
    { status: "processing", processingStartedAt: { $lt: staleProcessing } },
    { $set: { status: "failed", lastError: "Cleanup process stopped before completion" } },
  )

  const statuses = includeFailed ? ["pending", "failed"] : ["pending"]
  const jobs = await MediaCleanupJob.find({
    status: { $in: statuses },
    ...(publicIds?.length ? { publicId: { $in: publicIds } } : {}),
  })
    .sort({ createdAt: 1 })
    .limit(Math.min(Math.max(limit, 1), 100))
    .lean()

  const referenced = await collectReferencedMedia()
  const results = { completed: 0, cancelled: 0, failed: 0 }

  for (const job of jobs) {
    if (referenced.publicIds.has(job.publicId) || referenced.urls.has(job.url)) {
      await resolveReferencedJob(job)
      results.cancelled += 1
      continue
    }

    const claimed = await MediaCleanupJob.findOneAndUpdate(
      { _id: job._id, status: { $in: statuses } },
      {
        $set: { status: "processing", processingStartedAt: new Date() },
        $inc: { attempts: 1 },
        $unset: { lastError: 1 },
      },
      { returnDocument: "after" },
    )
    if (!claimed) continue

    try {
      // Confirm again after claiming so a reference saved while this batch was
      // being prepared still prevents deletion.
      const currentReferences = await collectReferencedMedia()
      if (currentReferences.publicIds.has(job.publicId) || currentReferences.urls.has(job.url)) {
        await resolveReferencedJob(job)
        results.cancelled += 1
        continue
      }
      await destroyManagedImage(job.publicId)
      const completedAt = new Date()
      await Promise.all([
        MediaCleanupJob.updateOne(
          { _id: job._id },
          {
            $set: { status: "completed", completedAt, expiresAt: expiryFromNow() },
            $unset: { lastError: 1, processingStartedAt: 1 },
          },
        ),
        MediaAsset.updateOne(
          { publicId: job.publicId },
          {
            $set: { status: "deleted", deletedAt: completedAt, expiresAt: expiryFromNow() },
            $unset: { lastError: 1 },
          },
        ),
      ])
      results.completed += 1
    } catch (error) {
      const message = (error instanceof Error ? error.message : "Cloudinary deletion failed").slice(0, 500)
      await Promise.all([
        MediaCleanupJob.updateOne(
          { _id: job._id },
          { $set: { status: "failed", lastError: message }, $unset: { processingStartedAt: 1 } },
        ),
        MediaAsset.updateOne(
          { publicId: job.publicId },
          { $set: { status: "failed", lastError: message } },
        ),
      ])
      results.failed += 1
    }
  }

  return results
}

export async function attemptMediaCleanup(publicIds: string[]) {
  if (!publicIds.length) return
  try {
    await processMediaCleanupJobs({ publicIds: [...new Set(publicIds)] })
  } catch (error) {
    console.error("Unable to process queued media cleanup:", error)
  }
}
