"use client";

import { useTransition } from "react";
import { useRouter } from "next/navigation";
import type { TeamYearData } from "@/lib/team-validation";

export function YearSelector({
  years,
  selectedYear,
  currentYearId,
}: {
  years: TeamYearData[];
  selectedYear?: number;
  currentYearId?: string;
}) {
  const router = useRouter();
  const [pending, startTransition] = useTransition();
  return (
    <div>
      <label htmlFor="team-year" className="sr-only">
        Academic year
      </label>
      <select
        id="team-year"
        value={selectedYear || ""}
        disabled={pending || !years.length}
        aria-busy={pending}
        onChange={(event) => {
          const year = event.target.value;
          startTransition(() =>
            router.push(`/team?year=${year}`, { scroll: false }),
          );
        }}
        className="h-10 min-w-32 rounded-xl border border-input bg-background px-3 text-sm font-medium focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
      >
        {!selectedYear && (
          <option value="">
            {years.length ? "Choose a year" : "Coming soon"}
          </option>
        )}
        {years.map((year) => (
          <option key={year._id} value={year.year}>
            {year.year}
            {year._id === currentYearId ? " · Current" : ""}
          </option>
        ))}
      </select>
      <span role="status" className="sr-only">
        {pending ? "Loading team…" : ""}
      </span>
    </div>
  );
}
