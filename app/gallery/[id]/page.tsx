import { Images } from "lucide-react";
import Link from "next/link";
import { notFound } from "next/navigation";
import { EventGallery } from "@/components/event-gallery";
async function getGallery(id: string) {
  try {
    const response = await fetch(
      `${process.env.NEXTAUTH_URL}/api/gallery/${id}`,
      {
        cache: "no-store",
      },
    );
    if (!response.ok) {
      if (response.status === 404) return null;
      throw new Error("Failed to fetch gallery");
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching gallery:", error);
    return null;
  }
}

interface PageProps {
  params: Promise<{ id: string }>;
}

export default async function GalleryDetailPage({ params }: PageProps) {
  const { id } = await params;
  const gallery = await getGallery(id);

  if (!gallery) {
    notFound();
  }

  const photoCount = gallery.images?.length || 0;
  const date = new Date(gallery.eventDate).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });

  return (
    <div className="mx-auto max-w-[1200px] px-4 pb-[72px] sm:px-8">
      <section className="flex flex-col gap-5 pb-8 pt-12">
        <nav aria-label="Breadcrumb" className="flex min-w-0 gap-2 text-sm text-muted-foreground">
          <Link href="/gallery" className="hover:text-foreground">Gallery</Link>
          <span aria-hidden="true">/</span>
          <span className="truncate text-foreground" aria-current="page">{gallery.eventName}</span>
        </nav>
        <div className="flex max-w-[700px] flex-col gap-3">
          <h1 className="text-[36px] font-semibold leading-[1.05] tracking-[-0.03em] sm:text-[48px]">{gallery.eventName}</h1>
          {gallery.description && <p className="text-[17px] leading-relaxed text-muted-foreground">{gallery.description}</p>}
          <span className="font-mono text-xs uppercase text-muted-foreground">
            <time dateTime={gallery.eventDate}>{date}</time> · {photoCount} {photoCount === 1 ? "photo" : "photos"}
          </span>
        </div>
      </section>

      {photoCount > 0 ? (
        <section aria-label="Event photos" className="flex flex-col gap-4">
          <p className="text-sm text-muted-foreground">Click a photo to view it in full.</p>
          <EventGallery images={gallery.images} eventName={gallery.eventName} />
        </section>
      ) : (
        <div className="rounded-2xl border border-dashed border-input bg-card p-12 text-center">
          <Images className="mx-auto mb-4 h-12 w-12 text-muted-foreground" aria-hidden="true" />
          <h2 className="mb-2 text-lg font-semibold">No photos available</h2>
          <p className="text-muted-foreground">This gallery doesn&apos;t have any photos yet.</p>
        </div>
      )}
    </div>
  );
}
