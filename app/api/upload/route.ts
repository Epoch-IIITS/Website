import { type NextRequest, NextResponse } from "next/server"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import connectDB from "@/lib/mongodb"
import {
  destroyManagedImage,
  isMediaPurpose,
  uploadManagedImage,
} from "@/lib/cloudinary-media"
import { registerUploadedMedia } from "@/lib/media-assets"

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user || session.user.role !== "admin") {
      return NextResponse.json({ error: "Admin access required" }, { status: session ? 403 : 401 })
    }

    const formData = await request.formData()
    const file = formData.get("file") as File
    const requestedPurpose = formData.get("purpose")
    // Keep blog as the fallback so an already-open admin form remains compatible
    // while new forms explicitly select their resource-specific folder.
    const purpose = requestedPurpose === null ? "blog" : requestedPurpose

    if (!file) {
      return NextResponse.json({ error: "No file received" }, { status: 400 })
    }
    if (!isMediaPurpose(purpose) || purpose === "team") {
      return NextResponse.json({ error: "Invalid upload purpose" }, { status: 400 })
    }

    // Validate file type
    const allowedTypes = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"]
    if (!allowedTypes.includes(file.type)) {
      return NextResponse.json({ error: "Invalid file type. Only images are allowed." }, { status: 400 })
    }

    // Validate file size (5MB limit)
    const maxSize = 5 * 1024 * 1024
    if (file.size > maxSize) {
      return NextResponse.json({ error: "File too large. Maximum size is 5MB." }, { status: 400 })
    }

    const bytes = await file.arrayBuffer()
    const buffer = Buffer.from(bytes)

    const result = await uploadManagedImage(buffer, purpose)
    try {
      await connectDB()
      await registerUploadedMedia(result, purpose, String(session.user.id))
    } catch (storageError) {
      // Compensate for the Cloudinary write so a registry failure does not itself
      // create an untracked orphan.
      try {
        await destroyManagedImage(result.publicId)
      } catch (cleanupError) {
        console.error("Unable to roll back untracked Cloudinary upload:", cleanupError)
      }
      throw storageError
    }

    return NextResponse.json({
      url: result.url,
      publicId: result.publicId,
      assetId: result.assetId,
      resourceType: result.resourceType,
    }, { status: 200 })
  } catch (error) {
    console.error("Upload error:", error)
    return NextResponse.json({ error: "Upload failed" }, { status: 500 })
  }
}
