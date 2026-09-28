import { NextRequest, NextResponse } from "next/server"
import { accessibleInitiative, initiativeActor } from "@/lib/initiatives/access"
import { uploadManagedImage, destroyManagedImage } from "@/lib/cloudinary-media"
import { registerUploadedMedia } from "@/lib/media-assets"
import { validateImageUpload } from "@/lib/image-upload"

export async function POST(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const actor = await initiativeActor()
    if (!actor) return NextResponse.json({ error: "Sign in required" }, { status: 401 })
    const initiative = await accessibleInitiative((await params).id, actor)
    if (!initiative) return NextResponse.json({ error: "Initiative not found" }, { status: 404 })
    if (initiative.status === "completed") return NextResponse.json({ error: "Reopen this initiative before uploading" }, { status: 409 })
    let form: FormData
    try { form = await request.formData() } catch { return NextResponse.json({ error: "Could not read the upload" }, { status: 400 }) }
    const file = form.get("file")
    if (!(file instanceof File)) return NextResponse.json({ error: "Choose an image" }, { status: 400 })
    const validation = validateImageUpload(file)
    if (validation) return NextResponse.json({ error: validation.error }, { status: validation.status })
    const result = await uploadManagedImage(Buffer.from(await file.arrayBuffer()), "initiative")
    try {
      await registerUploadedMedia(result, "initiative", actor.id)
    } catch (error) {
      try { await destroyManagedImage(result.publicId) } catch (cleanupError) { console.error("Initiative upload rollback failed:", cleanupError) }
      throw error
    }
    return NextResponse.json({ url: result.url })
  } catch (error) {
    console.error("Initiative upload error:", error)
    return NextResponse.json({ error: "Image upload failed" }, { status: 500 })
  }
}
