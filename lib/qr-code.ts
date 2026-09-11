import { createHmac, randomBytes } from "crypto"

type QRCodeRecord = {
  content: string
  slug: string
  trackingEnabled: boolean
  contentType: "url" | "text"
}

export function isHttpUrl(value: string) {
  try {
    const url = new URL(value)
    return url.protocol === "http:" || url.protocol === "https:"
  } catch {
    return false
  }
}

export function createQRCodeSlug() {
  return randomBytes(9).toString("base64url")
}

export function getPublicOrigin(fallbackOrigin?: string) {
  const candidates = [process.env.NEXTAUTH_URL, fallbackOrigin]
  for (const candidate of candidates) {
    if (!candidate) continue
    try {
      const url = new URL(candidate)
      if (url.protocol === "http:" || url.protocol === "https:") return url.origin
    } catch {
      // Try the next trusted origin.
    }
  }
  throw new Error("A public application origin is required")
}

export function getQRCodePayload(qrCode: QRCodeRecord, fallbackOrigin?: string) {
  if (qrCode.trackingEnabled && qrCode.contentType === "url") {
    return `${getPublicOrigin(fallbackOrigin)}/q/${qrCode.slug}`
  }
  return qrCode.content
}

export function createScanFingerprint(headers: Headers) {
  const forwarded = headers.get("cf-connecting-ip")
    || headers.get("x-real-ip")
    || headers.get("x-forwarded-for")?.split(",")[0]?.trim()
    || "unknown"
  const userAgent = headers.get("user-agent")?.slice(0, 500) || "unknown"
  const secret = process.env.NEXTAUTH_SECRET
  if (!secret) throw new Error("NEXTAUTH_SECRET is required for scan tracking")

  return createHmac("sha256", secret)
    .update(`${forwarded}\0${userAgent}`)
    .digest("hex")
}
