import fs from "node:fs";
import path from "node:path";
import mongoose from "mongoose";
import { v2 as cloudinary } from "cloudinary";
import {
  MEDIA_CLEANUP_GRACE_MS,
  describeMediaCleanupGracePeriod,
  readMediaReferenceValues,
  selectOrphanCandidates,
} from "./media-maintenance-helpers.mjs";

const MANAGED_PREFIXES = [
  "epoch-blogs/",
  "epoch-team/",
  "epoch/blogs/",
  "epoch/projects/",
  "epoch/events/",
  "epoch/gallery/",
  "epoch/team/",
];
const CLOUDINARY_LIST_PREFIXES = ["epoch-blogs/", "epoch-team/", "epoch/"];
const RESOLVED_RETENTION_MS = 30 * 24 * 60 * 60 * 1000;

function loadEnvFile(filename) {
  const file = path.join(process.cwd(), filename);
  if (!fs.existsSync(file)) return;
  for (const line of fs.readFileSync(file, "utf8").split(/\r?\n/)) {
    const match = line.match(
      /^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$/,
    );
    if (!match || Object.prototype.hasOwnProperty.call(process.env, match[1]))
      continue;
    let value = match[2];
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    process.env[match[1]] = value;
  }
}

// Shell variables win; otherwise use the same local-over-base precedence as Next.js.
loadEnvFile(".env.local");
loadEnvFile(".env");

function requireConfiguration() {
  const required = [
    "MONGODB_URI",
    "CLOUDINARY_CLOUD_NAME",
    "CLOUDINARY_API_KEY",
    "CLOUDINARY_API_SECRET",
  ];
  const missing = required.filter((key) => !process.env[key]);
  if (missing.length)
    throw new Error(`Missing environment variables: ${missing.join(", ")}`);
  cloudinary.config({
    cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
    api_key: process.env.CLOUDINARY_API_KEY,
    api_secret: process.env.CLOUDINARY_API_SECRET,
  });
}

function isManagedPublicId(publicId) {
  return MANAGED_PREFIXES.some((prefix) => publicId.startsWith(prefix));
}

function parseManagedUrl(value) {
  if (typeof value !== "string" || !value) return null;
  try {
    const url = new URL(value);
    const parts = url.pathname
      .split("/")
      .filter(Boolean)
      .map(decodeURIComponent);
    if (
      url.protocol !== "https:" ||
      url.hostname !== "res.cloudinary.com" ||
      parts[0] !== process.env.CLOUDINARY_CLOUD_NAME ||
      parts[1] !== "image" ||
      parts[2] !== "upload"
    )
      return null;
    const versionIndex = parts.findIndex(
      (part, index) => index >= 3 && /^v\d+$/.test(part),
    );
    if (versionIndex < 0 || versionIndex === parts.length - 1) return null;
    const publicIdParts = parts.slice(versionIndex + 1);
    publicIdParts[publicIdParts.length - 1] = publicIdParts
      .at(-1)
      .replace(/\.[a-z0-9]+$/i, "");
    const publicId = publicIdParts.join("/");
    return isManagedPublicId(publicId) ? publicId : null;
  } catch {
    return null;
  }
}

function extractManagedUrls(value) {
  if (typeof value !== "string" || !value) return [];
  const candidates =
    value.match(/https:\/\/res\.cloudinary\.com\/[^\s"'<>()[\]]+/gi) || [];
  return [...new Set(candidates)]
    .map((candidate) => candidate.replace(/[.,;:!?]+$/, ""))
    .filter((candidate) => parseManagedUrl(candidate));
}

const MediaAssetSchema = new mongoose.Schema(
  {
    assetId: String,
    publicId: { type: String, required: true, unique: true },
    url: { type: String, required: true },
    resourceType: { type: String, default: "image" },
    folder: { type: String, required: true },
    purpose: String,
    status: { type: String, required: true },
    source: { type: String, required: true },
    uploadedBy: String,
    lastError: String,
    deletedAt: Date,
    expiresAt: Date,
  },
  { timestamps: true },
);
MediaAssetSchema.index({ status: 1, createdAt: 1 });
MediaAssetSchema.index({ expiresAt: 1 }, { expireAfterSeconds: 0 });

const CleanupJobSchema = new mongoose.Schema(
  {
    publicId: { type: String, required: true, unique: true },
    url: { type: String, required: true },
    resourceType: { type: String, default: "image" },
    reason: { type: String, required: true },
    status: { type: String, required: true },
    attempts: { type: Number, default: 0 },
    lastError: String,
    processingStartedAt: Date,
    completedAt: Date,
    expiresAt: Date,
  },
  { timestamps: true },
);
CleanupJobSchema.index({ status: 1, createdAt: 1 });
CleanupJobSchema.index({ expiresAt: 1 }, { expireAfterSeconds: 0 });

const MediaAsset =
  mongoose.models.MediaAsset || mongoose.model("MediaAsset", MediaAssetSchema);
const CleanupJob =
  mongoose.models.MediaCleanupJob ||
  mongoose.model("MediaCleanupJob", CleanupJobSchema);

async function referencedMedia() {
  const db = mongoose.connection.db;
  if (!db) throw new Error("MongoDB is not connected");
  const values = await readMediaReferenceValues(db);
  const urls = new Set(values.flatMap(extractManagedUrls));
  const publicIds = new Set([...urls].map(parseManagedUrl).filter(Boolean));
  return { urls, publicIds };
}

function resolvedExpiry() {
  return new Date(Date.now() + RESOLVED_RETENTION_MS);
}

async function ensureMaintenanceStorage() {
  await Promise.all([MediaAsset.init(), CleanupJob.init()]);
}

async function queueAsset(asset, reason) {
  const folder =
    asset.asset_folder ||
    asset.public_id.slice(0, asset.public_id.lastIndexOf("/"));
  await MediaAsset.findOneAndUpdate(
    { publicId: asset.public_id },
    {
      $set: {
        assetId: asset.asset_id,
        url: asset.secure_url,
        resourceType: "image",
        folder,
        status: "deletion_pending",
      },
      $setOnInsert: { source: "legacy" },
      $unset: { lastError: 1, deletedAt: 1, expiresAt: 1 },
    },
    { upsert: true, runValidators: true },
  );
  await CleanupJob.findOneAndUpdate(
    { publicId: asset.public_id },
    {
      $set: {
        url: asset.secure_url,
        resourceType: "image",
        reason,
        status: "pending",
      },
      $unset: {
        lastError: 1,
        processingStartedAt: 1,
        completedAt: 1,
        expiresAt: 1,
      },
    },
    { upsert: true, runValidators: true },
  );
}

async function processJobs(publicIds) {
  await CleanupJob.updateMany(
    {
      status: "processing",
      processingStartedAt: { $lt: new Date(Date.now() - 15 * 60 * 1000) },
    },
    {
      $set: {
        status: "failed",
        lastError: "Cleanup process stopped before completion",
      },
    },
  );
  const jobs = await CleanupJob.find({
    status: { $in: ["pending", "failed"] },
    ...(Array.isArray(publicIds) ? { publicId: { $in: publicIds } } : {}),
  })
    .sort({ createdAt: 1 })
    .lean();
  const referenced = await referencedMedia();
  const result = { completed: 0, cancelled: 0, failed: 0 };

  for (const job of jobs) {
    if (
      referenced.publicIds.has(job.publicId) ||
      referenced.urls.has(job.url)
    ) {
      await Promise.all([
        CleanupJob.updateOne(
          { _id: job._id },
          {
            $set: {
              status: "cancelled",
              completedAt: new Date(),
              expiresAt: resolvedExpiry(),
            },
            $unset: { lastError: 1, processingStartedAt: 1 },
          },
        ),
        MediaAsset.updateOne(
          { publicId: job.publicId },
          {
            $set: { status: "attached" },
            $unset: { lastError: 1, deletedAt: 1, expiresAt: 1 },
          },
        ),
      ]);
      result.cancelled++;
      continue;
    }

    const claimed = await CleanupJob.findOneAndUpdate(
      { _id: job._id, status: { $in: ["pending", "failed"] } },
      {
        $set: { status: "processing", processingStartedAt: new Date() },
        $inc: { attempts: 1 },
        $unset: { lastError: 1 },
      },
      { returnDocument: "after" },
    );
    if (!claimed) continue;

    try {
      const currentReferences = await referencedMedia();
      if (
        currentReferences.publicIds.has(job.publicId) ||
        currentReferences.urls.has(job.url)
      ) {
        await Promise.all([
          CleanupJob.updateOne(
            { _id: job._id },
            {
              $set: {
                status: "cancelled",
                completedAt: new Date(),
                expiresAt: resolvedExpiry(),
              },
              $unset: { lastError: 1, processingStartedAt: 1 },
            },
          ),
          MediaAsset.updateOne(
            { publicId: job.publicId },
            {
              $set: { status: "attached" },
              $unset: { lastError: 1, deletedAt: 1, expiresAt: 1 },
            },
          ),
        ]);
        result.cancelled++;
        continue;
      }
      if (!isManagedPublicId(job.publicId))
        throw new Error("Refusing to delete an unmanaged asset");
      await cloudinary.uploader.destroy(job.publicId, {
        resource_type: "image",
        type: "upload",
        invalidate: true,
      });
      const completedAt = new Date();
      await Promise.all([
        CleanupJob.updateOne(
          { _id: job._id },
          {
            $set: {
              status: "completed",
              completedAt,
              expiresAt: resolvedExpiry(),
            },
            $unset: { lastError: 1, processingStartedAt: 1 },
          },
        ),
        MediaAsset.updateOne(
          { publicId: job.publicId },
          {
            $set: {
              status: "deleted",
              deletedAt: completedAt,
              expiresAt: resolvedExpiry(),
            },
            $unset: { lastError: 1 },
          },
        ),
      ]);
      result.completed++;
    } catch (error) {
      const message = String(
        error instanceof Error ? error.message : error,
      ).slice(0, 500);
      await Promise.all([
        CleanupJob.updateOne(
          { _id: job._id },
          {
            $set: { status: "failed", lastError: message },
            $unset: { processingStartedAt: 1 },
          },
        ),
        MediaAsset.updateOne(
          { publicId: job.publicId },
          { $set: { status: "failed", lastError: message } },
        ),
      ]);
      result.failed++;
    }
  }
  return result;
}

async function listManagedResources() {
  const resources = new Map();
  for (const prefix of CLOUDINARY_LIST_PREFIXES) {
    let nextCursor;
    do {
      const page = await cloudinary.api.resources({
        resource_type: "image",
        type: "upload",
        prefix,
        max_results: 500,
        ...(nextCursor ? { next_cursor: nextCursor } : {}),
      });
      for (const asset of page.resources || []) {
        if (isManagedPublicId(asset.public_id))
          resources.set(asset.public_id, asset);
      }
      nextCursor = page.next_cursor;
    } while (nextCursor);
  }
  return [...resources.values()];
}

async function scanOrphans(apply) {
  const [assets, referenced] = await Promise.all([
    listManagedResources(),
    referencedMedia(),
  ]);
  const candidates = selectOrphanCandidates(assets, referenced);

  console.log(`Managed Cloudinary assets: ${assets.length}`);
  console.log(`Referenced managed assets: ${referenced.publicIds.size}`);
  console.log(
    `Orphan candidates older than ${describeMediaCleanupGracePeriod()}: ${candidates.length}`,
  );
  if (candidates.length) {
    console.table(
      candidates.map((asset) => ({
        publicId: asset.public_id,
        createdAt: asset.created_at,
        bytes: asset.bytes,
        previewUrl: asset.secure_url,
      })),
    );
  }

  if (!apply) {
    console.log(
      "Dry run only. Review the list, then rerun with --apply to queue and delete these candidates.",
    );
    return;
  }

  await ensureMaintenanceStorage();
  for (const asset of candidates)
    await queueAsset(asset, "Confirmed by manual orphan scan");
  const result = await processJobs(candidates.map((asset) => asset.public_id));
  console.log(
    `Cleanup complete: ${result.completed} deleted, ${result.cancelled} still referenced, ${result.failed} failed.`,
  );
}

async function cleanupQueuedAssets() {
  await ensureMaintenanceStorage();
  const cutoff = new Date(Date.now() - MEDIA_CLEANUP_GRACE_MS);
  const abandoned = await MediaAsset.find({
    status: "pending",
    createdAt: { $lt: cutoff },
  }).lean();
  for (const asset of abandoned) {
    await queueAsset(
      {
        public_id: asset.publicId,
        asset_id: asset.assetId,
        secure_url: asset.url,
        asset_folder: asset.folder,
      },
      `Uploaded image was not attached to saved content within ${describeMediaCleanupGracePeriod()}`,
    );
  }
  const result = await processJobs();
  console.log(
    `Queued cleanup complete: ${result.completed} deleted, ${result.cancelled} still referenced, ${result.failed} failed.`,
  );
}

async function main() {
  const mode = process.argv[2];
  if (!["orphans", "cleanup"].includes(mode)) {
    throw new Error("Use either 'orphans' or 'cleanup'");
  }
  requireConfiguration();
  await mongoose.connect(process.env.MONGODB_URI, { bufferCommands: false });
  if (mode === "orphans") await scanOrphans(process.argv.includes("--apply"));
  else await cleanupQueuedAssets();
}

try {
  await main();
} catch (error) {
  console.error(
    `Media maintenance failed: ${error instanceof Error ? error.message : error}`,
  );
  process.exitCode = 1;
} finally {
  await mongoose.disconnect();
}
