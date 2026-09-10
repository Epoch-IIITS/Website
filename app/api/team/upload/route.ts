import { NextRequest, NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { v2 as cloudinary } from "cloudinary";

export async function POST(req: NextRequest) {
  const session = await getServerSession(authOptions);
  if (!session?.user?.id)
    return NextResponse.json(
      { error: "Please sign in to upload a photo" },
      { status: 401 },
    );
  try {
    const file = (await req.formData()).get("file");
    if (
      !(file instanceof File) ||
      file.size > 5 * 1024 * 1024 ||
      !["image/jpeg", "image/png", "image/webp"].includes(file.type)
    )
      return NextResponse.json(
        { error: "Use a JPG, PNG or WebP photo under 5 MB" },
        { status: 400 },
      );
    cloudinary.config({
      cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
      api_key: process.env.CLOUDINARY_API_KEY,
      api_secret: process.env.CLOUDINARY_API_SECRET,
    });
    const buffer = Buffer.from(await file.arrayBuffer());
    const result = await new Promise<any>((resolve, reject) => {
      cloudinary.uploader
        .upload_stream(
          {
            folder: "epoch-team",
            resource_type: "image",
            transformation: [{ width: 1200, height: 1200, crop: "limit" }],
            format: "jpg",
          },
          (error, value) => (error ? reject(error) : resolve(value)),
        )
        .end(buffer);
    });
    return NextResponse.json({ url: result.secure_url });
  } catch {
    return NextResponse.json(
      { error: "Photo upload failed. Please try again." },
      { status: 500 },
    );
  }
}
