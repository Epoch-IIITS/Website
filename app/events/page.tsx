import Link from "next/link"
import { Calendar, MapPin, Users } from "lucide-react"
import { PageKicker } from "@/components/page-kicker"
import { PastEvents, type PastEvent } from "@/components/events/past-events"
import { eventDateParts, formatEventDate, formatEventTime } from "@/lib/event-dates"

async function getEvents() {
  try {
    const response = await fetch(`${process.env.NEXTAUTH_URL}/api/events`, {
      cache: "no-store",
    })
    if (!response.ok) throw new Error("Failed to fetch events")
    return await response.json()
  } catch (error) {
    return []
  }
}

export const metadata = {
  title: "Events - Epoch",
  description: "Join our upcoming tech events, workshops, and networking sessions",
}

export default async function EventsPage() {
  const events = await getEvents()

  const upcomingEvents = events.filter((event: any) => new Date(event.date) >= new Date())
  const pastEvents: PastEvent[] = events
    .filter((event: any) => new Date(event.date) < new Date())
    .sort((a: any, b: any) => new Date(b.date).getTime() - new Date(a.date).getTime())
    .map((event: any) => {
      const { day, month, year } = eventDateParts(event.date)
      return {
        _id: event._id,
        title: event.title,
        description: event.description,
        venue: event.venue,
        image: event.image || undefined,
        day,
        month,
        year,
        when: `${formatEventDate(event.date)} · ${formatEventTime(event.date)}`,
      }
    })

  return (
    <div className="mx-auto max-w-[1200px] px-4 pb-24 sm:px-8">
      <section className="flex max-w-[660px] flex-col gap-4 pb-10 pt-16 sm:pt-20">
        <PageKicker as="p" className="mb-0">Events</PageKicker>
        <h1 className="text-[40px] font-semibold leading-[1.04] tracking-[-0.035em] sm:text-[56px]">Workshops, talks and hackathons</h1>
        <p className="text-[17px] leading-relaxed text-muted-foreground">Every session Epoch has run — and where to find the next one.</p>
      </section>

      <section className="pb-14" aria-labelledby="upcoming-heading">
        {upcomingEvents.length > 0 ? (
          <div className="flex flex-col gap-6">
            <div className="flex items-baseline justify-between gap-4">
              <h2 id="upcoming-heading" className="text-[32px] font-semibold tracking-tight">Upcoming</h2>
              <span className="font-mono text-xs text-muted-foreground">{upcomingEvents.length} {upcomingEvents.length === 1 ? "EVENT" : "EVENTS"}</span>
            </div>
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {upcomingEvents.map((event: any) => (
                <article key={event._id} className="flex flex-col overflow-hidden rounded-2xl border bg-card">
                  {event.image && <img src={event.image} alt={event.title} className="block aspect-video w-full object-cover" />}
                  <div className="flex flex-1 flex-col gap-4 p-6">
                    <span className="self-start rounded-full bg-primary-soft px-2.5 py-1 text-xs font-medium text-primary">Upcoming</span>
                    <h3 className="line-clamp-2 text-xl font-semibold leading-snug">{event.title}</h3>
                    <p className="line-clamp-3 text-sm leading-relaxed text-muted-foreground">{event.description}</p>
                    <div className="mt-auto flex flex-col gap-2 text-sm text-muted-foreground">
                      <span className="flex items-center gap-2"><Calendar className="h-4 w-4 shrink-0" aria-hidden="true" />{formatEventDate(event.date)} at {formatEventTime(event.date)}</span>
                      <span className="flex items-center gap-2"><MapPin className="h-4 w-4 shrink-0" aria-hidden="true" />{event.venue}</span>
                      {event.maxAttendees && <span className="flex items-center gap-2"><Users className="h-4 w-4 shrink-0" aria-hidden="true" />Max {event.maxAttendees} attendees</span>}
                    </div>
                    <Link href={`/events/${event._id}`} className="inline-flex h-11 items-center justify-center rounded-[10px] bg-primary px-[18px] text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90">View details &amp; RSVP</Link>
                  </div>
                </article>
              ))}
            </div>
          </div>
        ) : (
          <div className="flex flex-wrap items-center justify-between gap-6 rounded-2xl border border-dashed border-input bg-card p-6 sm:p-8">
            <div className="flex items-start gap-[18px]">
              <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-primary-soft text-primary"><Calendar className="h-4 w-4" aria-hidden="true" /></span>
              <div className="flex max-w-[560px] flex-col gap-1.5">
                <span className="font-mono text-xs tracking-[0.06em] text-muted-foreground">UPCOMING · 0</span>
                <h2 id="upcoming-heading" className="text-[22px] font-semibold">The next session is being planned</h2>
                <p className="text-[15px] leading-relaxed text-muted-foreground">Follow @epoch.iiits on Instagram to hear when registration opens.</p>
              </div>
            </div>
            <div className="flex flex-wrap gap-2.5">
              <a href="https://www.instagram.com/epoch.iiits/" target="_blank" rel="noopener noreferrer" className="inline-flex h-11 items-center rounded-[10px] bg-primary px-[18px] text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90">Follow on Instagram</a>
              <Link href="/contact" className="inline-flex h-11 items-center rounded-[10px] border border-input bg-card px-[18px] text-sm font-medium transition-colors hover:bg-accent">Suggest a topic</Link>
            </div>
          </div>
        )}
      </section>

      {pastEvents.length > 0 && (
        <section className="flex flex-col gap-6" aria-labelledby="past-heading">
          <div className="flex flex-wrap items-baseline justify-between gap-4">
            <h2 id="past-heading" className="text-[32px] font-semibold tracking-tight">Past events</h2>
            <span className="font-mono text-xs text-muted-foreground">{pastEvents.length} {pastEvents.length === 1 ? "EVENT" : "EVENTS"}<span className="hidden md:inline"> · SELECT ONE FOR DETAILS</span></span>
          </div>
          <PastEvents events={pastEvents} />
        </section>
      )}
    </div>
  )
}
