import Link from "next/link"
import { ArrowRight, MapPin } from "lucide-react"
import { eventDateParts } from "@/lib/event-dates"
import { requiredProblems, topics, projects as learnProjects } from "@/lib/learn/data"

async function getJson<T>(path: string, fallback: T): Promise<T> {
  try {
    const response = await fetch(`${process.env.NEXTAUTH_URL}${path}`, { cache: "no-store" })
    return response.ok ? await response.json() : fallback
  } catch {
    return fallback
  }
}

async function getLatestContent() {
  const [blogs, projects, events, galleries] = await Promise.all([
    getJson<{ blogs?: any[] }>("/api/blogs?published=true&limit=3", { blogs: [] }),
    getJson<any[]>("/api/projects", []),
    getJson<any[]>("/api/events", []),
    getJson<any[]>("/api/gallery", []),
  ])
  const list = <T,>(value: unknown): T[] => (Array.isArray(value) ? value : [])
  return { blogs: blogs.blogs || [], projects: list<any>(projects), events: list<any>(events), galleries: list<any>(galleries) }
}

function SectionHeading({ kicker, title, href, linkLabel }: { kicker: string; title: string; href: string; linkLabel: string }) {
  return (
    <div className="mb-8 flex flex-wrap items-end justify-between gap-6">
      <div className="flex flex-col gap-2">
        <span className="kicker">{kicker}</span>
        <h2 className="text-3xl font-semibold tracking-tight sm:text-4xl">{title}</h2>
      </div>
      <Link href={href} className="text-sm font-medium text-primary hover:underline">{linkLabel} →</Link>
    </div>
  )
}

const offerings = [
  { title: "Workshops & talks", body: "Intro sessions every semester, deep-dives on emerging domains, and hackathons with industry partners." },
  { title: "A practice track", body: "Concept notes and graded Python problems, from NumPy and Pandas to deep learning and LLMs." },
  { title: "Real projects", body: "Members build and deploy working tools — event platforms, prediction models, chatbots." },
  { title: "People to learn with", body: "Seniors, alumni and peers who have taken the same path and share what worked." },
]

export default async function HomePage() {
  const { blogs, projects, events, galleries } = await getLatestContent()
  const now = Date.now()
  const recentEvents = [...events].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()).slice(0, 5)
  const featuredProjects = (projects.some((project) => project.featured) ? projects.filter((project) => project.featured) : projects).slice(0, 3)
  const hero = galleries.find((gallery) => gallery.coverImage || gallery.images?.[0]?.url)
  const heroImage = hero ? hero.coverImage || hero.images[0].url : null

  const stats = [
    { value: topics.length, label: "Learn topics" },
    { value: requiredProblems.length, label: "practice problems" },
    { value: learnProjects.length, label: "guided project ideas" },
    { value: projects.length, label: "community projects shipped" },
  ]

  return (
    <div className="flex flex-col">
      <section className="mx-auto w-full max-w-[1200px] px-4 pb-16 pt-16 sm:px-8 sm:pb-[72px] sm:pt-[88px]">
        <div className="grid items-center gap-12 lg:grid-cols-2 lg:gap-16">
          <div className="flex flex-col gap-7">
            <div className="kicker flex items-center gap-2.5"><span className="h-2 w-2 rounded-full bg-primary" aria-hidden="true" />AI/ML Club · IIIT Sri City</div>
            <h1 className="text-[44px] font-semibold leading-[1.02] tracking-[-0.035em] sm:text-[64px]">Learn machine learning by building it.</h1>
            <p className="max-w-[500px] text-lg leading-relaxed text-muted-foreground">Epoch is the student AI/ML community at IIIT Sri City. Workshops, a hands-on practice track and member-built projects — from your first print() to federated learning.</p>
            <div className="flex flex-wrap gap-3">
              <Link href="/learn" className="inline-flex h-12 items-center gap-2 rounded-[10px] bg-primary px-[22px] text-[15px] font-medium text-primary-foreground transition-colors hover:bg-primary/90">Start learning <ArrowRight className="h-4 w-4" aria-hidden="true" /></Link>
              <Link href="/events" className="inline-flex h-12 items-center rounded-[10px] border border-input bg-card px-[22px] text-[15px] font-medium transition-colors hover:bg-accent">See events</Link>
            </div>
          </div>
          {heroImage && (
            <Link href={`/gallery/${hero._id}`} className="relative block">
              <img src={heroImage} alt={`${hero.eventName} photo`} className="block aspect-[4/3] w-full rounded-2xl object-cover" />
              <span className="absolute bottom-4 left-4 flex flex-col gap-0.5 rounded-[10px] bg-card px-3.5 py-2.5 text-[13px] shadow-lg">
                <span className="font-semibold">{hero.eventName}</span>
                <span className="font-mono text-xs uppercase text-muted-foreground">{new Date(hero.eventDate).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })} · {hero.images?.length || 0} photos</span>
              </span>
            </Link>
          )}
        </div>
        <dl className="mt-16 grid grid-cols-2 border-y lg:mt-[72px] lg:grid-cols-4">
          {stats.map((stat, index) => (
            <div key={stat.label} className={`flex flex-col-reverse gap-1 py-6 ${index % 2 ? "border-l pl-6" : ""} ${index === 2 ? "lg:border-l lg:pl-6" : ""} ${index > 1 ? "border-t lg:border-t-0" : ""}`}>
              <dt className="text-sm text-muted-foreground">{stat.label}</dt>
              <dd className="text-[32px] font-semibold tracking-tight">{stat.value}</dd>
            </div>
          ))}
        </dl>
      </section>

      <section className="mx-auto w-full max-w-[1200px] px-4 pb-24 pt-12 sm:px-8">
        <div className="grid gap-12 lg:grid-cols-3">
          <h2 className="text-[32px] font-semibold leading-tight tracking-tight">What happens at Epoch</h2>
          <div className="grid gap-x-12 gap-y-10 sm:grid-cols-2 lg:col-span-2">
            {offerings.map((item, index) => (
              <div key={item.title} className="flex flex-col gap-2">
                <span className="font-mono text-xs text-primary">{String(index + 1).padStart(2, "0")}</span>
                <h3 className="text-lg font-semibold">{item.title}</h3>
                <p className="text-[15px] leading-relaxed text-muted-foreground">{item.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {recentEvents.length > 0 && (
        <section className="border-y bg-card">
          <div className="mx-auto max-w-[1200px] px-4 py-[88px] sm:px-8">
            <SectionHeading kicker="Events" title="Recent sessions" href="/events" linkLabel="All events" />
            <div className="flex flex-col border-t">
              {recentEvents.map((event) => {
                const { day, month, year } = eventDateParts(event.date)
                const upcoming = new Date(event.date).getTime() >= now
                return (
                  <Link key={event._id} href={`/events/${event._id}`} className="group grid grid-cols-[72px_minmax(0,1fr)] items-center gap-x-6 border-b py-[22px] md:grid-cols-[96px_minmax(0,1fr)_200px] md:gap-x-12">
                    <span className="flex flex-col font-mono"><span className="text-[22px] font-medium">{day}</span><span className="text-xs text-muted-foreground">{month} {year}</span></span>
                    <span className="flex min-w-0 flex-col gap-1">
                      <span className="flex flex-wrap items-center gap-2"><span className="text-[17px] font-semibold group-hover:text-primary">{event.title}</span>{upcoming && <span className="rounded-full bg-primary-soft px-2.5 py-0.5 text-xs font-medium text-primary">Upcoming</span>}</span>
                      <span className="truncate text-sm text-muted-foreground">{event.description}</span>
                    </span>
                    <span className="hidden items-center gap-1.5 text-sm text-muted-foreground md:flex"><MapPin className="h-3.5 w-3.5 shrink-0" aria-hidden="true" /><span className="truncate">{event.venue}</span></span>
                  </Link>
                )
              })}
            </div>
          </div>
        </section>
      )}

      <section className="mx-auto w-full max-w-[1200px] px-4 py-24 sm:px-8">
        <div className="grid items-center gap-14 lg:grid-cols-2">
          <div className="flex flex-col gap-5">
            <span className="kicker">Epoch Learn</span>
            <h2 className="text-[32px] font-semibold leading-[1.1] tracking-[-0.025em] sm:text-[40px]">Read the concept. Write the code. Pass the tests.</h2>
            <p className="text-[17px] leading-relaxed text-muted-foreground">A browser-based practice track written by the club. Every problem pairs a short concept note with a Python editor and hidden tests, and your progress is saved to your account.</p>
            <Link href="/learn" className="mt-2 inline-flex h-11 items-center gap-2 self-start rounded-[10px] bg-primary px-[18px] text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90">Browse topics <ArrowRight className="h-4 w-4" aria-hidden="true" /></Link>
          </div>
          <div className="overflow-hidden rounded-2xl bg-panel text-panel-foreground shadow-2xl shadow-black/20" aria-hidden="true">
            <div className="flex items-center justify-between border-b border-white/10 px-[18px] py-3.5 font-mono text-xs text-[#A3A9B4]"><span>PY-01 · starter.py</span><span className="text-[#6EE7A0]">● 8 / 8 tests passed</span></div>
            <pre className="overflow-x-auto whitespace-pre-wrap px-[18px] py-[22px] font-mono text-sm leading-[1.8]"><span className="text-[#7C8494]"># Print six lines. The first one is done for you.</span>{"\n"}print(<span className="text-[#9FD7A8]">&quot;Hello, world!&quot;</span>){"\n"}print(<span className="text-[#9FD7A8]">&quot;Python&quot;</span>, <span className="text-[#9FD7A8]">&quot;is&quot;</span>, <span className="text-[#9FD7A8]">&quot;fun&quot;</span>){"\n"}print(<span className="text-[#9FD7A8]">&quot;2026&quot;</span>, <span className="text-[#9FD7A8]">&quot;10&quot;</span>, <span className="text-[#9FD7A8]">&quot;24&quot;</span>, sep=<span className="text-[#9FD7A8]">&quot;-&quot;</span>){"\n"}print(){"\n"}print(<span className="text-[#9FD7A8]">&quot;Loading&quot;</span>, end=<span className="text-[#9FD7A8]">&quot;...&quot;</span>){"\n"}print(<span className="text-[#9FD7A8]">&quot;done&quot;</span>)</pre>
            <div className="flex justify-end gap-2 border-t border-white/10 px-[18px] py-3.5 text-[13px]"><span className="rounded-lg border border-white/20 px-3.5 py-2">Run</span><span className="rounded-lg bg-primary px-3.5 py-2 font-medium text-primary-foreground">Submit</span></div>
          </div>
        </div>
      </section>

      {featuredProjects.length > 0 && (
        <section className="border-y bg-card">
          <div className="mx-auto max-w-[1200px] px-4 py-[88px] sm:px-8">
            <SectionHeading kicker="Projects" title="Built by members" href="/projects" linkLabel={`All ${projects.length} projects`} />
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {featuredProjects.map((project) => (
                <article key={project._id} className="flex flex-col overflow-hidden rounded-[14px] border bg-card transition-colors hover:border-input">
                  {project.image && <img src={project.image} alt={`${project.title} preview`} className="block aspect-video w-full border-b object-cover" />}
                  <div className="flex flex-1 flex-col gap-2.5 p-5">
                    <h3 className="text-lg font-semibold">{project.title}</h3>
                    <p className="line-clamp-3 flex-1 text-sm leading-relaxed text-muted-foreground">{project.description}</p>
                    {project.techStack?.length > 0 && <span className="font-mono text-xs text-muted-foreground">{project.techStack.slice(0, 3).join(" · ")}</span>}
                    {(project.githubUrl || project.liveUrl) && (
                      <div className="flex gap-4 border-t pt-3 text-sm font-medium">
                        {project.githubUrl && <a href={project.githubUrl} target="_blank" rel="noopener noreferrer" className="hover:text-primary">Code ↗</a>}
                        {project.liveUrl && <a href={project.liveUrl} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">Live demo ↗</a>}
                      </div>
                    )}
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>
      )}

      {blogs.length > 0 && (
        <section className="mx-auto w-full max-w-[1200px] px-4 py-24 sm:px-8">
          <SectionHeading kicker="Blog" title="Latest writing" href="/blog" linkLabel="All posts" />
          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {blogs.map((blog: any) => (
              <Link key={blog._id} href={`/blog/${blog.slug}`} className="group flex flex-col gap-3.5">
                {blog.featuredImage ? <img src={blog.featuredImage} alt="" className="block aspect-video w-full rounded-xl border object-cover" /> : <span className="block aspect-video w-full rounded-xl border bg-secondary" aria-hidden="true" />}
                <span className="font-mono text-xs uppercase text-muted-foreground">{new Date(blog.createdAt).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })}{blog.tags?.[0] ? ` · ${blog.tags[0]}` : ""}</span>
                <h3 className="text-[19px] font-semibold leading-snug group-hover:text-primary">{blog.title}</h3>
                {blog.author?.name && <span className="text-sm text-muted-foreground">{blog.author.name}</span>}
              </Link>
            ))}
          </div>
        </section>
      )}

    </div>
  )
}
