import { v2 as cloudinary, type UploadApiOptions, type UploadApiResponse } from "cloudinary"

export const mediaPurposes = ["blog", "project", "event", "gallery", "team"] as const
export type MediaPurpose = (typeof mediaPurposes)[number]

const folders: Record<MediaPurpose, string> = {
  blog: "epoch/blogs",
  project: "epoch/projects",
  event: "epoch/events",
  gallery: "epoch/gallery",
  team: "epoch/team",
}

const managedFolderPrefixes = [
  "epoch-blogs/",
  "epoch-team/",
  "epoch/blogs/",
  "epoch/projects/",
  "epoch/events/",
  "epoch/gallery/",
  "epoch/team/",
] as const

export interface ManagedMediaIdentifier {
  publicId: string
  resourceType: "image"
  folder: string
  url: string
}

export interface UploadedMedia extends ManagedMediaIdentifier {
  assetId: string
  format: string
  bytes: number
}

function requiredCloudinaryConfig() {
  const cloudName = process.env.CLOUDINARY_CLOUD_NAME
  const apiKey = process.env.CLOUDINARY_API_KEY
  const apiSecret = process.env.CLOUDINARY_API_SECRET
  if (!cloudName || !apiKey || !apiSecret) {
    throw new Error("Cloudinary is not configured")
  }
  cloudinary.config({ cloud_name: cloudName, api_key: apiKey, api_secret: apiSecret })
  return cloudinary
}

export function isMediaPurpose(value: unknown): value is MediaPurpose {
  return typeof value === "string" && mediaPurposes.includes(value as MediaPurpose)
}

export function folderForMediaPurpose(purpose: MediaPurpose) {
  return folders[purpose]
}

export function isManagedPublicId(publicId: string) {
  return managedFolderPrefixes.some((prefix) => publicId.startsWith(prefix))
}

export function parseManagedCloudinaryUrl(
  value: unknown,
  cloudName = process.env.CLOUDINARY_CLOUD_NAME,
): ManagedMediaIdentifier | null {
  if (typeof value !== "string" || !value || !cloudName) return null

  try {
    const parsed = new URL(value)
    if (parsed.protocol !== "https:" || parsed.hostname !== "res.cloudinary.com") return null

    const parts = parsed.pathname.split("/").filter(Boolean).map(decodeURIComponent)
    if (parts[0] !== cloudName || parts[1] !== "image" || parts[2] !== "upload") return null

    const versionIndex = parts.findIndex((part, index) => index >= 3 && /^v\d+$/.test(part))
    if (versionIndex < 0 || versionIndex === parts.length - 1) return null

    const path = parts.slice(versionIndex + 1)
    const finalPart = path.at(-1)
    if (!finalPart) return null
    path[path.length - 1] = finalPart.replace(/\.[a-z0-9]+$/i, "")
    const publicId = path.join("/")
    if (!publicId || !isManagedPublicId(publicId)) return null

    return {
      publicId,
      resourceType: "image",
      folder: publicId.slice(0, publicId.lastIndexOf("/")),
      url: parsed.toString(),
    }
  } catch {
    return null
  }
}

export function extractManagedCloudinaryUrls(value: unknown, cloudName = process.env.CLOUDINARY_CLOUD_NAME) {
  if (typeof value !== "string" || !value) return []
  const candidates = value.match(/https:\/\/res\.cloudinary\.com\/[^\s"'<>()[\]]+/gi) || []
  return [...new Set(candidates)]
    .map((candidate) => parseManagedCloudinaryUrl(candidate.replace(/[.,;:!?]+$/, ""), cloudName)?.url)
    .filter((url): url is string => Boolean(url))
}

export async function uploadManagedImage(
  buffer: Buffer,
  purpose: MediaPurpose,
  options: Partial<Pick<UploadApiOptions, "format" | "transformation">> = {},
): Promise<UploadedMedia> {
  const client = requiredCloudinaryConfig()
  const result = await new Promise<UploadApiResponse>((resolve, reject) => {
    client.uploader
      .upload_stream(
        {
          folder: folderForMediaPurpose(purpose),
          resource_type: "image",
          ...options,
        },
        (error, value) => error || !value ? reject(error || new Error("Upload failed")) : resolve(value),
      )
      .end(buffer)
  })

  return {
    url: result.secure_url,
    publicId: result.public_id,
    assetId: result.asset_id,
    resourceType: "image",
    folder: folderForMediaPurpose(purpose),
    format: result.format,
    bytes: result.bytes,
  }
}

export async function destroyManagedImage(publicId: string) {
  if (!isManagedPublicId(publicId)) throw new Error("Refusing to delete an unmanaged Cloudinary asset")
  return requiredCloudinaryConfig().uploader.destroy(publicId, {
    resource_type: "image",
    type: "upload",
    invalidate: true,
  })
}
