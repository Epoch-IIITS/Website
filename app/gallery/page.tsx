export const dynamic = "force-dynamic";

import { Images } from "lucide-react";
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

const formatDate = (value: string) =>
  new Date(value).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });

function Cover({ gallery, className, aspect }: { gallery: any; className?: string; aspect: string }) {
  const coverImage = gallery.coverImage || gallery.images?.[0]?.url;
  return coverImage ? (
    <GalleryImage src={coverImage} alt={`${gallery.eventName} cover`} aspect={aspect} className={className} />
  ) : (
    <div className={`flex items-center justify-center bg-secondary ${aspect} ${className ?? ""}`}>
      <Images className="h-8 w-8 text-muted-foreground" aria-hidden="true" />
    </div>
  );
}

export default async function GalleryPage({ searchParams }: { searchParams: Promise<{ year?: string }> }) {
  const galleries: any[] = await getGalleries();
  const { year } = await searchParams;
  const years = [...new Set(galleries.map((gallery) => String(new Date(gallery.eventDate).getFullYear())))];
  const selectedYear = year && years.includes(year) ? year : null;
  const shown = selectedYear ? galleries.filter((gallery) => String(new Date(gallery.eventDate).getFullYear()) === selectedYear) : galleries;
  const [featured, ...rest] = shown;
  const photoCount = (gallery: any) => gallery.images?.length || 0;

  return (
    <div className="mx-auto max-w-[1200px] px-4 pb-[72px] sm:px-8">
      <section className="flex flex-wrap items-end justify-between gap-8 pb-10 pt-16 sm:pt-20">
        <div className="flex max-w-[640px] flex-col gap-4">
          <PageKicker as="p" className="mb-0">Gallery · {galleries.length} {galleries.length === 1 ? "album" : "albums"}</PageKicker>
          <h1 className="text-[40px] font-semibold leading-[1.04] tracking-[-0.035em] sm:text-[56px]">Community moments</h1>
          <p className="text-[17px] leading-relaxed text-muted-foreground">Photos from every session, hackathon and showcase.</p>
        </div>
        {years.length > 1 && (
          <nav aria-label="Filter by year" className="flex flex-wrap gap-2">
            {[{ label: "All", value: null }, ...years.map((value) => ({ label: value, value }))].map((option) => {
              const active = option.value === selectedYear;
              return (
                <Link
                  key={option.label}
                  href={option.value ? `/gallery?year=${option.value}` : "/gallery"}
                  aria-current={active ? "page" : undefined}
                  className={`inline-flex h-9 items-center rounded-full border px-3.5 text-[13px] font-medium transition-colors ${active ? "border-primary bg-primary text-primary-foreground" : "border-input bg-card hover:bg-accent"}`}
                >
                  {option.label}
                </Link>
              );
            })}
          </nav>
        )}
      </section>

      {!featured ? (
        <div className="rounded-2xl border border-dashed border-input bg-card p-12 text-center">
          <Images className="mx-auto mb-4 h-12 w-12 text-muted-foreground" aria-hidden="true" />
          <h3 className="mb-2 text-lg font-semibold">No galleries yet</h3>
          <p className="text-muted-foreground">Check back later for photos from our events!</p>
        </div>
      ) : (
        <>
          <Link
            href={`/gallery/${featured._id}`}
            aria-label={`Open ${featured.eventName} gallery`}
            className="group grid overflow-hidden rounded-2xl border bg-card focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring md:grid-cols-3"
          >
            <Cover gallery={featured} aspect="aspect-[3/2] md:aspect-auto" className="md:col-span-2 md:h-full md:min-h-[360px]" />
            <div className="flex flex-col justify-between gap-6 p-6 sm:p-8">
              <div className="flex flex-col gap-3">
                <span className="self-start rounded-full bg-primary-soft px-2.5 py-1 text-xs font-medium text-primary">Latest album</span>
                <h3 className="text-[28px] font-semibold leading-tight tracking-tight">{featured.eventName}</h3>
                {featured.description && <p className="line-clamp-4 text-[15px] leading-relaxed text-muted-foreground">{featured.description}</p>}
              </div>
              <div className="flex justify-between border-t pt-4 font-mono text-xs uppercase text-muted-foreground">
                <time dateTime={featured.eventDate}>{formatDate(featured.eventDate)}</time>
                <span>{photoCount(featured)} {photoCount(featured) === 1 ? "photo" : "photos"}</span>
              </div>
            </div>
          </Link>

          {rest.length > 0 && (
            <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {rest.map((gallery) => (
                <Link
                  key={gallery._id}
                  href={`/gallery/${gallery._id}`}
                  aria-label={`Open ${gallery.eventName} gallery`}
                  className="group flex flex-col gap-3 rounded-xl focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                >
                  <div className="overflow-hidden rounded-xl"><Cover gallery={gallery} aspect="aspect-[3/2]" /></div>
                  <div className="flex items-baseline justify-between gap-3">
                    <h3 className="text-base font-semibold group-hover:text-primary">{gallery.eventName}</h3>
                    <span className="whitespace-nowrap font-mono text-xs text-muted-foreground" aria-label={`${photoCount(gallery)} photos`}>{photoCount(gallery)}</span>
                  </div>
                  <span className="-mt-1.5 line-clamp-1 text-sm text-muted-foreground">
                    {gallery.description ? `${gallery.description} · ` : ""}<time dateTime={gallery.eventDate}>{formatDate(gallery.eventDate)}</time>
                  </span>
                </Link>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}
