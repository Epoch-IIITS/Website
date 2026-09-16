import type { MediaPurpose } from "@/lib/cloudinary-media"

// Leave room for multipart overhead below the hosting request-body limit.
export const IMAGE_UPLOAD_MAX_BYTES = 4 * 1024 * 1024
export const IMAGE_UPLOAD_MAX_LABEL = "4 MB"
export const CONTENT_IMAGE_TYPES = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"]
export const TEAM_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"]
const TOO_LARGE = `Image is too large. Choose an image of ${IMAGE_UPLOAD_MAX_LABEL} or less, or compress it before uploading.`

export function validateImageUpload(
  file: Pick<Blob, "size" | "type">,
  kind: "content" | "team" = "content",
): { error: string; status: number } | null {
  if (file.size === 0) return { error: "This file is empty. Choose another image.", status: 400 }
  if (file.size > IMAGE_UPLOAD_MAX_BYTES) return { error: TOO_LARGE, status: 413 }
  const allowedTypes = kind === "team" ? TEAM_IMAGE_TYPES : CONTENT_IMAGE_TYPES
  if (!allowedTypes.includes(file.type)) {
    return {
      error: kind === "team" ? "Choose a JPG, PNG or WebP photo." : "Choose a JPEG, PNG, GIF or WebP image.",
      status: 415,
    }
  }
  return null
}

export function imageUploadErrorMessage(error: unknown): string {
  return error instanceof Error ? error.message : "Image upload failed. Please try again."
}

// Shared by content forms and the team crop dialog. Never expose a proxy's
// HTML/plain-text response or a JSON parsing exception as the user-facing error.
export async function uploadImage(file: Blob, purpose: MediaPurpose, filename?: string): Promise<{ url: string }> {
  const validation = validateImageUpload(file, purpose === "team" ? "team" : "content")
  if (validation) throw new Error(validation.error)

  const body = new FormData()
  if (filename) body.append("file", file, filename)
  else body.append("file", file)
  if (purpose !== "team") body.append("purpose", purpose)

  let response: Response
  try {
    response = await fetch(purpose === "team" ? "/api/team/upload" : "/api/upload", { method: "POST", body })
  } catch {
    throw new Error("Could not connect to the server. Check your connection and try again.")
  }

  if (response.status === 413) throw new Error(TOO_LARGE)
  if (response.status === 401) throw new Error("Your session has expired. Sign in again, then retry the upload.")
  if (response.status === 403) throw new Error("You do not have permission to upload images.")
  if (response.status === 408 || response.status === 504) {
    throw new Error("The upload timed out. Please try again.")
  }
  if (response.status === 429) throw new Error("Too many uploads. Wait a moment, then try again.")
  if (response.status >= 500) throw new Error("The upload service is temporarily unavailable. Please try again later.")

  const data: unknown = await response.json().catch(() => null)
  if (!response.ok) {
    const message = data && typeof data === "object" && "error" in data ? data.error : null
    throw new Error(
      typeof message === "string" && message.trim() && message.length <= 300
        ? message
        : "Image upload failed. Please try again.",
    )
  }

  if (data && typeof data === "object" && "url" in data && typeof data.url === "string") {
    try {
      const url = new URL(data.url)
      if (url.protocol === "https:" || url.protocol === "http:") return { url: url.href }
    } catch {
      // A malformed success response must not replace the currently saved image.
    }
  }
  throw new Error("The server returned an invalid upload response. Please try again.")
}
