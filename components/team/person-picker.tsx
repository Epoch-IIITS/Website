"use client";

import { useEffect, useId, useRef, useState } from "react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import type { TeamProfile } from "@/lib/team-validation";

export function PersonPicker({
  people,
  value,
  onChange,
}: {
  people: TeamProfile[];
  value: string;
  onChange: (id: string) => void;
}) {
  const id = useId();
  const input = useRef<HTMLInputElement>(null);
  const [query, setQuery] = useState(
    people.find((person) => person._id === value)?.name || "",
  );
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(0);
  const matches = people.filter((person) =>
    person.name.toLocaleLowerCase().includes(query.trim().toLocaleLowerCase()),
  );
  useEffect(() => {
    if (value)
      setQuery(people.find((person) => person._id === value)?.name || "");
  }, [value, people]);
  useEffect(() => {
    input.current?.setCustomValidity(
      value ? "" : "Select a person from the search results.",
    );
  }, [value]);
  useEffect(() => {
    if (open)
      document
        .getElementById(`${id}-option-${active}`)
        ?.scrollIntoView({ block: "nearest" });
  }, [active, open, id]);
  function select(person: TeamProfile) {
    onChange(person._id);
    setQuery(person.name);
    setOpen(false);
    input.current?.focus();
  }
  return (
    <div
      className="relative"
      onBlur={(event) => {
        if (!event.currentTarget.contains(event.relatedTarget)) setOpen(false);
      }}
    >
      <Label htmlFor={id}>Person</Label>
      <Input
        ref={input}
        id={id}
        className="mt-2"
        role="combobox"
        aria-autocomplete="list"
        aria-expanded={open}
        aria-controls={`${id}-options`}
        aria-activedescendant={
          open && matches[active] ? `${id}-option-${active}` : undefined
        }
        placeholder="Search people by name…"
        autoComplete="off"
        required
        value={query}
        onFocus={() => {
          setOpen(true);
          setActive(0);
        }}
        onChange={(event) => {
          setQuery(event.target.value);
          onChange("");
          setOpen(true);
          setActive(0);
        }}
        onKeyDown={(event) => {
          if (event.key === "ArrowDown" || event.key === "ArrowUp") {
            event.preventDefault();
            setOpen(true);
            setActive((index) =>
              Math.max(
                0,
                Math.min(
                  matches.length - 1,
                  index + (event.key === "ArrowDown" ? 1 : -1),
                ),
              ),
            );
          } else if (event.key === "Enter" && open) {
            event.preventDefault();
            if (matches[active]) select(matches[active]);
          } else if (event.key === "Escape" && open) {
            event.preventDefault();
            event.stopPropagation();
            setOpen(false);
          }
        }}
      />
      {open && (
        <div
          id={`${id}-options`}
          role="listbox"
          aria-label="Matching people"
          className="absolute z-50 mt-1 max-h-36 w-full overflow-y-auto rounded-xl border bg-popover p-1 text-popover-foreground shadow-lg"
        >
          {matches.length ? (
            matches.map((person, index) => (
              <div
                key={person._id}
                id={`${id}-option-${index}`}
                role="option"
                aria-selected={person._id === value}
                onPointerDown={(event) => event.preventDefault()}
                onClick={() => select(person)}
                onPointerMove={() => setActive(index)}
                className={`cursor-pointer rounded-lg px-3 py-1.5 ${index === active ? "bg-accent text-accent-foreground" : ""}`}
              >
                <p className="text-sm font-medium">{person.name}</p>
                <p className="text-xs text-muted-foreground">
                  {[person.currentRole, person.organization]
                    .filter(Boolean)
                    .join(" · ")}
                </p>
              </div>
            ))
          ) : (
            <p className="px-3 py-3 text-sm text-muted-foreground">
              {people.length
                ? "No people match this name."
                : "Create a profile in People first."}
            </p>
          )}
        </div>
      )}
    </div>
  );
}
