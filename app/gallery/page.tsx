export const dynamic = "force-dynamic";

import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Calendar, Images } from "lucide-react";
import Link from "next/link";
import GalleryImage from "@/components/GalleryImage";
import { PageKicker } from "@/components/page-kicker";

async function getGalleries() {
  try {
    const response = await fetch(`${process.env.NEXTAUTH_URL}/api/gallery`);
    if (!response.ok) throw new Error("Failed to fetch galleries");
    return await response.json();
  } catch (error) {
    console.error("Error fetching galleries:", error);
    return [];
  }
}

export default async function GalleryPage() {
  const galleries = await getGalleries();

  return (
    // <AuthWrapper>
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-6xl mx-auto">
        <PageKicker>Community Moments</PageKicker>

        {galleries.length === 0 ? (
          <Card>
            <CardContent className="p-12 text-center">
              <Images className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">No galleries yet</h3>
              <p className="text-muted-foreground">
                Check back later for photos from our events!
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {galleries.map((gallery: any) => {
              const coverImage = gallery.coverImage || gallery.images?.[0]?.url;
              const photoCount = gallery.images?.length || 0;
              return (
                <Link
                  key={gallery._id}
                  href={`/gallery/${gallery._id}`}
                  aria-label={`Open ${gallery.eventName} gallery`}
                  className="rounded-xl focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                >
                  <Card className="group relative aspect-[4/3] overflow-hidden border-0 bg-muted shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-xl">
                    {coverImage ? (
                      <GalleryImage
                        src={coverImage}
                        alt={`${gallery.eventName} cover`}
                        aspect="aspect-[4/3]"
                        className="h-full"
                      />
                    ) : (
                      <div className="flex h-full items-center justify-center bg-muted">
                        <Images className="h-8 w-8 text-muted-foreground" />
                      </div>
                    )}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/95 via-black/35 to-transparent" />
                    <div className="absolute left-3 top-3 flex items-center gap-1.5 rounded-full border border-white/15 bg-black/55 px-2.5 py-1 text-xs text-white backdrop-blur-sm">
                      {/* <Calendar className="h-3.5 w-3.5" /> */}
                      <time dateTime={gallery.eventDate}>
                        {new Date(gallery.eventDate).toLocaleDateString(
                          "en-US",
                          {
                            month: "long",
                            day: "numeric",
                            year: "numeric",
                          },
                        )}
                      </time>
                    </div>
                    <Badge
                      aria-label={`${photoCount} ${photoCount === 1 ? "photo" : "photos"}`}
                      className="absolute right-3 top-3 border-white/15 bg-black/55 text-white backdrop-blur-sm hover:bg-black/55"
                    >
                      <Images className="mr-1.5 h-3.5 w-3.5" />
                      {photoCount}
                    </Badge>
                    <div className="absolute inset-x-0 bottom-0 p-3 text-white sm:p-4">
                      <h2 className="line-clamp-2 text-base font-semibold leading-tight drop-shadow-sm sm:text-lg">
                        {gallery.eventName}
                      </h2>
                      {gallery.description && (
                        <p className="mt-1 line-clamp-2 text-xs leading-snug text-white/80 sm:text-sm">
                          {gallery.description}
                        </p>
                      )}
                    </div>
                  </Card>
                </Link>
              );
            })}
          </div>
        )}
      </div>
    </div>
    // </AuthWrapper>
  );
}
