import { NextRequest, NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import connectDB from "@/lib/mongodb";
import { destroyManagedImage, uploadManagedImage } from "@/lib/cloudinary-media";
import { registerUploadedMedia } from "@/lib/media-assets";
import { validateImageUpload } from "@/lib/image-upload";

export async function POST(req: NextRequest) {
  const session = await getServerSession(authOptions);
  if (!session?.user?.id)
    return NextResponse.json(
      { error: "Please sign in to upload a photo" },
      { status: 401 },
    );
  try {
    let formData: FormData;
    try {
      formData = await req.formData();
    } catch {
      return NextResponse.json(
        { error: "Could not read the upload. Select a photo and try again." },
        { status: 400 },
      );
    }
    const file = formData.get("file");
    if (!(file instanceof File))
      return NextResponse.json({ error: "No photo received" }, { status: 400 });
    const validation = validateImageUpload(file, "team");
    if (validation)
      return NextResponse.json({ error: validation.error }, { status: validation.status });
    const buffer = Buffer.from(await file.arrayBuffer());
    const result = await uploadManagedImage(buffer, "team", {
      transformation: [{ width: 1200, height: 1200, crop: "limit" }],
      format: "jpg",
    });
    try {
      await connectDB();
      await registerUploadedMedia(result, "team", String(session.user.id));
    } catch (storageError) {
      try {
        await destroyManagedImage(result.publicId);
      } catch (cleanupError) {
        console.error("Unable to roll back untracked team upload:", cleanupError);
      }
      throw storageError;
    }
    return NextResponse.json({
      url: result.url,
      publicId: result.publicId,
      assetId: result.assetId,
      resourceType: result.resourceType,
    });
  } catch {
    return NextResponse.json(
      { error: "Photo upload failed. Please try again." },
      { status: 500 },
    );
  }
}
