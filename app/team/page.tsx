import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { publicRoster, publicTeam } from "@/lib/team-data";
import { YearSelector } from "@/components/team/year-selector";
import { MemberCard } from "@/components/team/member-card";
import { PageKicker } from "@/components/page-kicker";
import type { TeamYearData } from "@/lib/team-validation";

export const dynamic = "force-dynamic";
export const metadata = {
  title: "Team — Epoch",
  description:
    "Meet the people behind Epoch and explore our teams through the years.",
};
export default async function TeamPage({
  searchParams,
}: {
  searchParams: Promise<{ year?: string }>;
}) {
  const { year } = await searchParams;
  const { years, settings } = await publicTeam();
  const selected: TeamYearData | undefined = year
    ? years.find((y: TeamYearData) => String(y.year) === year)
    : years.find((y: TeamYearData) => y._id === settings.currentYearId) ||
      years[0];
  const currentYear =
    years.find((y: TeamYearData) => y._id === settings.currentYearId) ||
    years[0];
  const roster = selected ? await publicRoster(selected._id) : [];
  return (
    <div className="mx-auto max-w-7xl px-4 py-12 sm:px-8 sm:py-20">
      <PageKicker className="mb-8">Epoch Community</PageKicker>
      <div className="mb-16 flex items-center justify-between gap-4 border-t pt-6">
        <p className="text-xl font-semibold sm:text-2xl">
          AY {selected?.year || currentYear?.year || "—"}
        </p>
        <YearSelector
          years={years}
          selectedYear={selected?.year}
          currentYearId={currentYear?._id}
        />
      </div>
      {!selected ? (
        <div className="rounded-2xl border border-dashed p-12 text-center">
          <h2 className="text-xl font-semibold">
            {year
              ? "This team is not available yet"
              : "Our next chapter is taking shape"}
          </h2>
          <p className="mt-2 text-muted-foreground">
            {year
              ? "Choose an available academic year above."
              : "The team directory will appear here once a roster is published."}
          </p>
        </div>
      ) : (
        <>
          {selected.groups.map((group) => {
            const members = roster.filter((a: any) => a.groupId === group.id);
            return members.length ? (
              <section key={group.id} className="mb-14">
                <h2 className="mb-8 text-center text-3xl font-medium italic tracking-tight sm:text-4xl">
                  {group.name}
                </h2>
                <div
                  className={`grid gap-6 ${
                    members.length === 1
                      ? "mx-auto w-full max-w-xs"
                      : members.length === 2
                        ? "mx-auto w-full max-w-2xl sm:grid-cols-2"
                        : "sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
                  }`}
                >
                  {members.map((a: any) => (
                    <MemberCard
                      key={a._id}
                      person={a.person}
                      por={a.por}
                      id={a._id}
                    />
                  ))}
                </div>
              </section>
            ) : null;
          })}
          {!roster.length && (
            <p className="py-10 text-muted-foreground">
              This roster is being prepared. Check back soon.
            </p>
          )}
        </>
      )}
      <section className="mt-20 rounded-3xl border bg-primary/5 p-8 sm:p-12">
        <p className="text-xs font-semibold uppercase tracking-widest text-primary">
          Keep the story growing
        </p>
        <h2 className="mt-3 text-3xl font-semibold">{settings.ctaTitle}</h2>
        <p className="mt-4 max-w-2xl whitespace-pre-line text-muted-foreground">
          {settings.ctaText}
        </p>
        <Link
          href="/team/request"
          className="mt-6 inline-flex items-center gap-2 rounded-full bg-primary px-6 py-3 text-sm font-medium text-primary-foreground"
        >
          Request to be listed
          <ArrowUpRight className="h-4 w-4" />
        </Link>
      </section>
    </div>
  );
}
