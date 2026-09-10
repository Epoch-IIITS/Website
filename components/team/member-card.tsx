"use client";
import { useEffect, useId, useState } from "react";
import Link from "next/link";
import { Linkedin, Share2 } from "lucide-react";
import type { TeamProfile } from "@/lib/team-validation";

export function MemberCard({
  person,
  por,
  id,
}: {
  person: TeamProfile;
  por: string;
  id?: string;
}) {
  const [broken, setBroken] = useState(false);
  const [hovered, setHovered] = useState(false);
  const [expanded, setExpanded] = useState(false);
  const [focused, setFocused] = useState(false);
  const detailsId = useId();
  const visible = hovered || expanded || focused;
  useEffect(() => setBroken(false), [person.photo]);
  return (
    <article
      className="relative aspect-square overflow-hidden rounded-2xl bg-zinc-800 text-white shadow-sm"
      onPointerEnter={(event) => {
        if (event.pointerType === "mouse") setHovered(true);
      }}
      onPointerLeave={() => setHovered(false)}
      onFocusCapture={(event) => {
        if (event.target.matches(":focus-visible")) setFocused(true);
      }}
      onBlurCapture={(event) => {
        if (!event.currentTarget.contains(event.relatedTarget)) {
          setFocused(false);
          setExpanded(false);
        }
      }}
      onKeyDown={(event) => {
        if (event.key === "Escape") {
          setExpanded(false);
          setFocused(false);
          setHovered(false);
        }
      }}
    >
      {person.photo && !broken ? (
        <img
          src={person.photo}
          alt=""
          loading="lazy"
          className="absolute inset-0 h-full w-full object-cover"
          onError={() => setBroken(true)}
        />
      ) : (
        <div
          className="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-purple-950 to-slate-700 text-6xl font-semibold text-white/60"
          aria-label="No profile photo"
        >
          {person.name
            .split(" ")
            .map((name) => name[0])
            .slice(0, 2)
            .join("")}
        </div>
      )}
      <div
        aria-hidden="true"
        className={`pointer-events-none absolute inset-0 bg-gradient-to-t from-black/90 via-black/35 to-transparent transition-opacity duration-500 motion-reduce:transition-none ${visible ? "opacity-100" : "opacity-55"}`}
      />
      <button
        type="button"
        aria-label={`${visible ? "Hide" : "Show"} details for ${person.name}`}
        aria-expanded={visible}
        aria-controls={detailsId}
        onClick={() => {
          setExpanded(!expanded);
          setFocused(false);
        }}
        className="absolute inset-0 z-10 rounded-2xl focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-white"
      />
      <div className="pointer-events-none absolute inset-0 z-20 [text-shadow:0_1px_6px_rgb(0_0_0_/_45%)]">
        <h3
          aria-hidden={visible}
          className={`absolute inset-5 flex items-end justify-center break-words text-center text-2xl font-semibold leading-tight transition-[opacity,transform] duration-300 motion-reduce:transition-none ${visible ? "scale-95 opacity-0" : "scale-100 opacity-100"}`}
        >
          {person.name}
        </h3>
        <div
          id={detailsId}
          aria-hidden={!visible}
          className={`absolute inset-x-0 bottom-0 max-h-full p-5 text-left transition-[opacity,transform] duration-500 ease-out motion-reduce:transition-none ${visible ? "translate-y-0 opacity-100" : "pointer-events-none translate-y-4 opacity-0"}`}
        >
          <div
            className={`max-h-full overflow-y-auto overscroll-contain ${visible ? "pointer-events-auto" : "pointer-events-none"}`}
          >
            <div className="space-y-2">
              <h3 className="break-words text-xl font-semibold leading-tight">
                {person.name}
              </h3>
              {por && (
                <p className="break-words text-base font-medium italic">
                  {por}
                </p>
              )}
              <div className="grid grid-cols-[minmax(0,1fr)_auto] items-end gap-3">
                <div className="min-w-0 space-y-2">
                  {person.tagline && (
                    <p className="break-words text-xs leading-relaxed text-white/90">
                      {person.tagline}
                    </p>
                  )}
                  {(person.currentRole || person.organization) && (
                    <p className="break-words text-xs leading-relaxed text-white/90">
                      {[person.currentRole, person.organization]
                        .filter(Boolean)
                        .join(" · ")}
                    </p>
                  )}
                </div>
                <div className="flex items-center justify-end gap-1">
                  {person.linkedin && (
                    <a
                      href={person.linkedin}
                      target="_blank"
                      rel="noopener noreferrer"
                      tabIndex={visible ? 0 : -1}
                      title="LinkedIn"
                      className="inline-flex rounded-full p-1 text-white/90 transition-colors hover:bg-white/15 hover:text-white focus-visible:outline focus-visible:outline-2"
                      aria-label={`${person.name} on LinkedIn`}
                    >
                      <Linkedin className="h-5 w-5" />
                    </a>
                  )}
                  {id && (
                    <Link
                      href={`/team/member/${id}`}
                      tabIndex={visible ? 0 : -1}
                      title="Share card"
                      aria-label={`Share card for ${person.name}`}
                      className="inline-flex rounded-full p-1 text-white/90 transition-colors hover:bg-white/15 hover:text-white focus-visible:outline focus-visible:outline-2"
                    >
                      <Share2 className="h-5 w-5" />
                    </Link>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </article>
  );
}
