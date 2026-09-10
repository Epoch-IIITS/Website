"use client";
import { useEffect, useRef, useState } from "react";
import { TeamEditorDialog } from "@/components/team/editor-dialog";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { ProfileFields, emptyProfile } from "@/components/team/profile-fields";
import { PersonPicker } from "@/components/team/person-picker";
import { MemberCard } from "@/components/team/member-card";
import {
  defaultSettings,
  type TeamYearData,
  type TeamProfile,
  type TeamAppointmentData,
} from "@/lib/team-validation";

const selectClass =
  "mt-2 h-10 w-full rounded-md border bg-background px-3 text-sm";
const blankAppointment = {
  personId: "",
  yearId: "",
  groupId: "",
  por: "",
  order: 0,
  published: false,
};
type Workspace = {
  years: TeamYearData[];
  people: TeamProfile[];
  appointments: TeamAppointmentData[];
  requests: any[];
  settings: typeof defaultSettings & { currentYearId?: string };
};
export default function TeamAdmin() {
  const [data, setData] = useState<Workspace | null>(null);
  const [tab, setTab] = useState("years");
  const [editor, setEditor] = useState<
    "year" | "person" | "appointment" | null
  >(null);
  const editorTrigger = useRef<HTMLElement | null>(null);
  function openEditor(value: "year" | "person" | "appointment") {
    editorTrigger.current = document.activeElement as HTMLElement | null;
    setError("");
    setMessage("");
    setEditor(value);
  }
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [yearId, setYearId] = useState("");
  const [year, setYear] = useState({
    year: new Date().getFullYear(),
    published: false,
    groups: [
      { id: "executive", name: "Executive Committee" },
      { id: "subcommittee", name: "Sub-Committee Members" },
      { id: "learners", name: "Learners" },
    ],
  });
  const [personId, setPersonId] = useState("");
  const [profile, setProfile] = useState(emptyProfile);
  const [appointmentId, setAppointmentId] = useState("");
  const [appointment, setAppointment] = useState(blankAppointment);
  const [settings, setSettings] = useState(defaultSettings);
  const [request, setRequest] = useState<any>(null);
  const [reason, setReason] = useState("");
  const [reviewPerson, setReviewPerson] = useState("");
  const [photoUploading, setPhotoUploading] = useState(false);
  const [peopleSearch, setPeopleSearch] = useState("");
  const [filterYear, setFilterYear] = useState("");
  const [requestFilter, setRequestFilter] = useState("pending");
  const dialogProps = {
    onClose: () => {
      setEditor(null);
      setError("");
    },
    busy: busy || photoUploading,
    error,
    returnFocusTo: editorTrigger.current,
  };

  async function load() {
    const response = await fetch("/api/admin/team", { cache: "no-store" });
    const value = await response.json();
    if (!response.ok) throw new Error(value.error);
    setData(value);
    setSettings(value.settings);
  }
  useEffect(() => {
    load().catch((e) => setError(e.message));
  }, []);
  async function save(body: any) {
    setBusy(true);
    setError("");
    setMessage("");
    try {
      const response = await fetch("/api/admin/team", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const value = await response.json();
      if (!response.ok) throw new Error(value.error);
      await load();
      setMessage("Changes saved");
      return true;
    } catch (e: any) {
      setError(e.message);
      return false;
    } finally {
      setBusy(false);
    }
  }
  function editPerson(person?: TeamProfile) {
    setPersonId(person?._id || "");
    setProfile(person || emptyProfile);
  }
  function editAppointment(
    value?: TeamAppointmentData,
    defaultYearId = "",
  ) {
    setAppointmentId(value?._id || "");
    setAppointment(value || { ...blankAppointment, yearId: defaultYearId });
  }
  function appointmentFields() {
    const selected = data?.years.find((y) => y._id === appointment.yearId);
    return (
      <div className="grid gap-4 sm:grid-cols-2">
        <Label>
          Academic year
          <select
            className={selectClass}
            required
            value={appointment.yearId}
            onChange={(e) =>
              setAppointment({
                ...appointment,
                yearId: e.target.value,
                groupId: "",
              })
            }
          >
            <option value="">Select a year</option>
            {data?.years.map((y) => (
              <option key={y._id} value={y._id}>
                AY {y.year}
                {y.published ? "" : " (draft)"}
              </option>
            ))}
          </select>
        </Label>
        <Label>
          Hierarchy group
          <select
            className={selectClass}
            required
            value={appointment.groupId}
            onChange={(e) =>
              setAppointment({ ...appointment, groupId: e.target.value })
            }
          >
            <option value="">Select a group</option>
            {selected?.groups.map((g) => (
              <option key={g.id} value={g.id}>
                {g.name}
              </option>
            ))}
          </select>
        </Label>
        <Label>
          Position of responsibility (optional)
          <Input
            className="mt-2"
            maxLength={100}
            value={appointment.por}
            placeholder="e.g. NLP Lead"
            onChange={(e) =>
              setAppointment({ ...appointment, por: e.target.value })
            }
          />
        </Label>
        <Label>
          Display order (lowest first)
          <Input
            className="mt-2"
            type="number"
            min={0}
            max={10000}
            required
            value={appointment.order}
            onChange={(e) =>
              setAppointment({ ...appointment, order: Number(e.target.value) })
            }
          />
        </Label>
        <label className="flex items-center gap-2 text-sm sm:col-span-2">
          <input
            type="checkbox"
            checked={appointment.published}
            onChange={(e) =>
              setAppointment({ ...appointment, published: e.target.checked })
            }
          />
          Publish this appointment (visible only when its year is published)
        </label>
      </div>
    );
  }
  return (
    <div className="mx-auto max-w-6xl space-y-6 p-2 sm:p-4">
      <header className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-3xl font-semibold">Team</h1>
          <p className="mt-2 text-muted-foreground">
            Every year, every role, every person.
          </p>
        </div>
        <Button variant="outline" asChild>
          <Link href="/team">View directory ↗</Link>
        </Button>
      </header>
      <nav aria-label="Team administration" className="flex flex-wrap gap-2">
        {[
          ["years", "Academic years"],
          ["people", "People"],
          ["roster", "Appointments"],
          [
            "requests",
            `Requests${data ? ` (${data.requests.filter((r) => r.status === "pending").length})` : ""}`,
          ],
          ["settings", "Page settings"],
        ].map(([key, label]) => (
          <Button
            key={key}
            disabled={busy || photoUploading}
            variant={tab === key ? "default" : "outline"}
            onClick={() => {
              setTab(key);
              setMessage("");
              setRequest(null);
              editPerson();
              editAppointment();
            }}
            aria-pressed={tab === key}
          >
            {label}
          </Button>
        ))}
      </nav>
      {error && !editor && (
        <div
          role="alert"
          className="rounded-xl border border-destructive/40 p-4 text-destructive"
        >
          {error}
          {!data && (
            <Button
              className="ml-3"
              variant="outline"
              onClick={() => {
                setError("");
                load().catch((e) => setError(e.message));
              }}
            >
              Retry
            </Button>
          )}
        </div>
      )}
      {message && (
        <p role="status" className="rounded-xl border bg-primary/5 p-4">
          {message}
        </p>
      )}
      {!data ? (
        <p>Loading workspace…</p>
      ) : (
        <fieldset
          disabled={busy || photoUploading}
          className="min-w-0 space-y-6"
        >
          {tab === "years" && (
            <div className="space-y-6">
              <section className="space-y-3">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-semibold">Academic years</h2>
                  <Button
                    variant="outline"
                    onClick={() => {
                      openEditor("year");
                      setYearId("");
                      setYear({
                        year: new Date().getFullYear(),
                        published: false,
                        groups: [
                          {
                            id: crypto.randomUUID(),
                            name: "Executive Committee",
                          },
                        ],
                      });
                    }}
                  >
                    New academic year
                  </Button>
                </div>
                {!data.years.length && (
                  <p className="text-sm text-muted-foreground">
                    Create your first academic year to start building a roster.
                  </p>
                )}
                {data.years.map((y) => (
                  <article
                    key={y._id}
                    className="space-y-3 rounded-xl border bg-card p-4"
                  >
                    <div className="flex justify-between">
                      <h3 className="font-semibold">AY {y.year}</h3>
                      <span className="text-xs text-muted-foreground">
                        {data.settings.currentYearId === y._id
                          ? "Current"
                          : y.published
                            ? "Published"
                            : "Draft"}
                      </span>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      {y.groups.map((g) => g.name).join(" → ")}
                    </p>
                    <div className="flex flex-wrap gap-2">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => {
                          openEditor("year");
                          setYearId(y._id);
                          setYear({
                            year: y.year,
                            published: y.published,
                            groups: y.groups,
                          });
                        }}
                      >
                        Edit
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => {
                          openEditor("year");
                          setYearId("");
                          setYear({
                            year: y.year + 1,
                            published: false,
                            groups: y.groups.map((g) => ({
                              ...g,
                              id: crypto.randomUUID(),
                            })),
                          });
                        }}
                      >
                        Copy hierarchy
                      </Button>
                      {y.published && data.settings.currentYearId !== y._id && (
                        <Button
                          size="sm"
                          onClick={() => save({ action: "current", id: y._id })}
                        >
                          Make current
                        </Button>
                      )}
                    </div>
                  </article>
                ))}
              </section>
              <TeamEditorDialog
                {...dialogProps}
                open={editor === "year"}
                title={yearId ? "Edit academic year" : "New academic year"}
                description="Set the academic year and arrange its hierarchy groups."
              >
                <form
                  className="space-y-5"
                  onSubmit={async (e) => {
                    e.preventDefault();
                    if (
                      await save({
                        action: "year",
                        id: yearId || undefined,
                        value: year,
                      })
                    ) {
                      setEditor(null);
                      setYearId("");
                      setYear({
                        ...year,
                        year: year.year + 1,
                        published: false,
                      });
                    }
                  }}
                >
                  <Label className="block">
                    AY year
                    <Input
                      className="mt-2"
                      type="number"
                      required
                      min={2000}
                      max={2200}
                      value={year.year}
                      onChange={(e) =>
                        setYear({ ...year, year: Number(e.target.value) })
                      }
                    />
                  </Label>
                  <label className="flex items-center gap-2 text-sm">
                    <input
                      type="checkbox"
                      checked={year.published}
                      onChange={(e) =>
                        setYear({ ...year, published: e.target.checked })
                      }
                    />
                    Publish this academic year
                  </label>
                  <div>
                    <h3 className="font-medium">
                      Hierarchy, from top to bottom
                    </h3>
                    <p className="mt-1 text-xs text-muted-foreground">
                      Group headings are separate from each person’s POR. Move
                      members before removing their group.
                    </p>
                  </div>
                  <div className="space-y-3">
                    {year.groups.map((g, i) => (
                      <div key={g.id} className="flex items-center gap-1">
                        <Input
                          aria-label={`Group ${i + 1} name`}
                          required
                          maxLength={80}
                          value={g.name}
                          onChange={(e) =>
                            setYear({
                              ...year,
                              groups: year.groups.map((v, n) =>
                                n === i ? { ...v, name: e.target.value } : v,
                              ),
                            })
                          }
                        />
                        {[-1, 1].map((direction) => (
                          <Button
                            key={direction}
                            type="button"
                            variant="ghost"
                            size="icon"
                            disabled={
                              i + direction < 0 ||
                              i + direction >= year.groups.length
                            }
                            aria-label={`Move ${g.name} ${direction === -1 ? "up" : "down"}`}
                            onClick={() => {
                              const groups = [...year.groups];
                              [groups[i], groups[i + direction]] = [
                                groups[i + direction],
                                groups[i],
                              ];
                              setYear({ ...year, groups });
                            }}
                          >
                            {direction === -1 ? "↑" : "↓"}
                          </Button>
                        ))}
                        <Button
                          type="button"
                          size="icon"
                          variant="ghost"
                          aria-label={`Remove ${g.name}`}
                          disabled={year.groups.length === 1}
                          onClick={() =>
                            setYear({
                              ...year,
                              groups: year.groups.filter((v) => v.id !== g.id),
                            })
                          }
                        >
                          ×
                        </Button>
                      </div>
                    ))}
                  </div>
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() =>
                      setYear({
                        ...year,
                        groups: [
                          ...year.groups,
                          { id: crypto.randomUUID(), name: "" },
                        ],
                      })
                    }
                  >
                    Add group
                  </Button>
                  <div>
                    <Button>{busy ? "Saving…" : "Save academic year"}</Button>
                  </div>
                </form>
              </TeamEditorDialog>
            </div>
          )}
          {tab === "people" && (
            <div className="space-y-6">
              <section className="space-y-3">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-semibold">People</h2>
                  <Button
                    variant="outline"
                    onClick={() => {
                      editPerson();
                      openEditor("person");
                    }}
                  >
                    New profile
                  </Button>
                </div>
                {!data.people.length && (
                  <p className="text-sm text-muted-foreground">
                    Add profiles here, then assign them to an academic year.
                  </p>
                )}
                <Label className="block">
                  Find person by name
                  <Input
                    type="search"
                    className="mt-2"
                    placeholder="Search people…"
                    value={peopleSearch}
                    onChange={(event) => setPeopleSearch(event.target.value)}
                  />
                </Label>
                {data.people.length > 0 &&
                  !data.people.some((person) =>
                    person.name
                      .toLocaleLowerCase()
                      .includes(peopleSearch.trim().toLocaleLowerCase()),
                  ) && (
                    <p
                      role="status"
                      className="py-4 text-sm text-muted-foreground"
                    >
                      No people match this name.
                    </p>
                  )}
                {data.people
                  .filter((person) =>
                    person.name
                      .toLocaleLowerCase()
                      .includes(peopleSearch.trim().toLocaleLowerCase()),
                  )
                  .map((p) => (
                    <button
                      key={p._id}
                      className="block w-full rounded-xl border bg-card p-4 text-left hover:bg-muted"
                      onClick={() => {
                        editPerson(p);
                        openEditor("person");
                      }}
                    >
                      <span className="block font-medium">{p.name}</span>
                      <span className="text-xs text-muted-foreground">
                        {p.currentRole}{" "}
                        {p.organization && `· ${p.organization}`}
                      </span>
                    </button>
                  ))}
              </section>
              <TeamEditorDialog
                {...dialogProps}
                open={editor === "person"}
                title={personId ? "Edit profile" : "New profile"}
                description="Add a person’s details and profile photo. Assign their academic year in Appointments."
              >
                <form
                  className="space-y-5"
                  onSubmit={async (e) => {
                    e.preventDefault();
                    if (
                      await save({
                        action: "person",
                        id: personId || undefined,
                        value: profile,
                      })
                    ) {
                      setEditor(null);
                      editPerson();
                    }
                  }}
                >
                  <p className="text-sm text-muted-foreground">
                    Current career details update across all years. Yearly PORs
                    are managed in Appointments.
                  </p>
                  <ProfileFields
                    value={profile}
                    onChange={setProfile}
                    onUploadingChange={setPhotoUploading}
                  />
                  <Button>{busy ? "Saving…" : "Save profile"}</Button>
                  {profile.name && (
                    <div className="max-w-xs">
                      <p className="mb-3 text-sm text-muted-foreground">
                        Card preview
                      </p>
                      <MemberCard
                        person={{ ...profile, _id: personId }}
                        por="Position of responsibility"
                      />
                    </div>
                  )}
                </form>
              </TeamEditorDialog>
            </div>
          )}
          {tab === "roster" && (
            <div className="space-y-6">
              <section className="space-y-4">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-semibold">Appointments</h2>
                  <Button
                    variant="outline"
                    onClick={() => {
                      editAppointment(undefined, filterYear);
                      openEditor("appointment");
                    }}
                  >
                    New appointment
                  </Button>
                </div>
                <Label className="block">
                  Filter by academic year
                  <select
                    className={selectClass}
                    value={filterYear}
                    onChange={(e) => setFilterYear(e.target.value)}
                  >
                    <option value="">All years</option>
                    {data.years.map((y) => (
                      <option key={y._id} value={y._id}>
                        AY {y.year}
                      </option>
                    ))}
                  </select>
                </Label>
                {data.appointments
                  .filter((a) => !filterYear || a.yearId === filterYear)
                  .map((a) => {
                    const appointmentYear = data.years.find(
                      (year) => year._id === a.yearId,
                    );
                    const hierarchyGroup = appointmentYear?.groups.find(
                      (group) => group.id === a.groupId,
                    );
                    return (
                      <article
                        key={a._id}
                        className="space-y-3 rounded-xl border bg-card p-4"
                      >
                        <h3 className="font-medium">
                          {data.people.find((p) => p._id === a.personId)?.name}
                        </h3>
                        <p className="text-sm text-muted-foreground">
                          AY {appointmentYear?.year ?? "—"} ·{" "}
                          {hierarchyGroup?.name || "Unknown group"} ·{" "}
                          {a.por && `${a.por} · `}Order {a.order} ·{" "}
                          {a.published ? "Published" : "Draft"}
                        </p>
                        <div className="flex flex-wrap gap-2">
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => {
                              editAppointment(a);
                              openEditor("appointment");
                            }}
                          >
                            Edit
                          </Button>
                          {a.published &&
                            data.years.find((y) => y._id === a.yearId)
                              ?.published && (
                              <Button size="sm" variant="outline" asChild>
                                <Link href={`/team/member/${a._id}`}>
                                  View share card
                                </Link>
                              </Button>
                            )}
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => {
                              if (
                                window.confirm(
                                  "Remove this appointment? The person’s profile will remain available.",
                                )
                              )
                                void save({
                                  action: "remove-appointment",
                                  id: a._id,
                                });
                            }}
                          >
                            Remove
                          </Button>
                        </div>
                      </article>
                    );
                  })}
                {!data.appointments.length && (
                  <p className="text-sm text-muted-foreground">
                    No appointments yet.
                  </p>
                )}
              </section>
              <TeamEditorDialog
                {...dialogProps}
                open={editor === "appointment"}
                title={appointmentId ? "Edit appointment" : "New appointment"}
                description="Assign a person to an academic year and hierarchy group. POR is optional."
                focusTitleOnOpen
              >
                <form
                  className="space-y-5"
                  onSubmit={async (e) => {
                    e.preventDefault();
                    if (
                      await save({
                        action: "appointment",
                        id: appointmentId || undefined,
                        value: appointment,
                      })
                    ) {
                      setEditor(null);
                      editAppointment();
                    }
                  }}
                >
                  <PersonPicker
                    people={data.people}
                    value={appointment.personId}
                    onChange={(personId) =>
                      setAppointment({ ...appointment, personId })
                    }
                  />
                  {appointmentFields()}
                  <Button>{busy ? "Saving…" : "Save appointment"}</Button>
                  {appointment.personId && appointment.yearId && (
                    <div className="max-w-xs">
                      <MemberCard
                        person={data.people.find(
                          (p) => p._id === appointment.personId,
                        )!}
                        por={appointment.por}
                      />
                    </div>
                  )}
                </form>
              </TeamEditorDialog>
            </div>
          )}
          {tab === "requests" && (
            <div className="space-y-6">
              <Label className="block max-w-xs">
                Request status
                <select
                  className={selectClass}
                  value={requestFilter}
                  onChange={(e) => setRequestFilter(e.target.value)}
                >
                  {["pending", "approved", "rejected", "all"].map((s) => (
                    <option key={s} value={s}>
                      {s[0].toUpperCase() + s.slice(1)}
                    </option>
                  ))}
                </select>
              </Label>
              <div className="grid gap-4 md:grid-cols-2">
                {data.requests
                  .filter(
                    (r) =>
                      requestFilter === "all" || r.status === requestFilter,
                  )
                  .map((r) => (
                    <article
                      key={r._id}
                      className="space-y-3 rounded-xl border bg-card p-5"
                    >
                      <div className="flex justify-between gap-3">
                        <h2 className="font-semibold">{r.name}</h2>
                        <span className="text-sm capitalize">{r.status}</span>
                      </div>
                      <p className="text-sm">
                        {[`AY ${r.year}`, r.por, r.group]
                          .filter(Boolean)
                          .join(" · ")}
                      </p>
                      <p className="break-all text-xs text-muted-foreground">
                        {r.email} · {new Date(r.createdAt).toLocaleDateString()}
                      </p>
                      {r.notes && (
                        <p className="whitespace-pre-wrap text-sm">{r.notes}</p>
                      )}
                      {r.reason && (
                        <p className="text-sm">Feedback: {r.reason}</p>
                      )}
                      {r.status === "pending" && (
                        <Button
                          variant="outline"
                          onClick={() => {
                            setRequest(r);
                            setProfile(r);
                            setReason("");
                            setReviewPerson("");
                            setAppointment({
                              ...blankAppointment,
                              yearId:
                                data.years.find((y) => y.year === r.year)
                                  ?._id || "",
                              por: r.por || "",
                            });
                          }}
                        >
                          Review request
                        </Button>
                      )}
                    </article>
                  ))}
              </div>
              {!data.requests.some(
                (r) => requestFilter === "all" || r.status === requestFilter,
              ) && (
                <p className="text-muted-foreground">
                  No {requestFilter === "all" ? "" : requestFilter} requests.
                </p>
              )}
              {request && (
                <form
                  className="space-y-6 rounded-2xl border bg-card p-6"
                  onSubmit={async (e) => {
                    e.preventDefault();
                    if (
                      await save({
                        action: "review",
                        id: request._id,
                        decision: "approve",
                        personId: reviewPerson || undefined,
                        profile,
                        appointment,
                      })
                    )
                      setRequest(null);
                  }}
                >
                  <h2 className="text-xl font-semibold">
                    Review {request.name}
                  </h2>
                  <Label className="block">
                    Link to an existing person or create a profile
                    <select
                      className={selectClass}
                      value={reviewPerson}
                      onChange={(e) => setReviewPerson(e.target.value)}
                    >
                      <option value="">
                        Create a new profile from these details
                      </option>
                      {data.people.map((p) => (
                        <option key={p._id} value={p._id}>
                          {p.name}
                        </option>
                      ))}
                    </select>
                  </Label>
                  {reviewPerson ? (
                    <p className="text-sm text-muted-foreground">
                      The existing profile will be kept. Approval creates or
                      updates their appointment for the selected year. Edit
                      their profile in People if needed.
                    </p>
                  ) : (
                    <ProfileFields
                      value={profile}
                      onChange={setProfile}
                      onUploadingChange={setPhotoUploading}
                    />
                  )}
                  {appointmentFields()}
                  <div className="flex gap-3">
                    <Button>Approve request</Button>
                    <Button
                      type="button"
                      variant="outline"
                      onClick={() => setRequest(null)}
                    >
                      Cancel
                    </Button>
                  </div>
                  <div className="space-y-3 border-t pt-5">
                    <Label className="block">
                      Rejection feedback (visible to applicant)
                      <Textarea
                        className="mt-2"
                        maxLength={1000}
                        value={reason}
                        onChange={(e) => setReason(e.target.value)}
                      />
                    </Label>
                    <Button
                      type="button"
                      variant="destructive"
                      disabled={!reason.trim()}
                      onClick={async () => {
                        if (
                          await save({
                            action: "review",
                            id: request._id,
                            decision: "reject",
                            reason,
                          })
                        )
                          setRequest(null);
                      }}
                    >
                      Reject request
                    </Button>
                  </div>
                </form>
              )}
            </div>
          )}
          {tab === "settings" && (
            <form
              className="max-w-3xl space-y-5 rounded-2xl border bg-card p-6"
              onSubmit={(e) => {
                e.preventDefault();
                void save({ action: "settings", value: settings });
              }}
            >
              <h2 className="text-xl font-semibold">Public page content</h2>
              {(
                [
                  ["title", "Page heading", 100],

                  ["ctaTitle", "Request section heading", 100],
                  ["ctaText", "Request section description", 500],
                ] as const
              ).map(([key, label, max]) => (
                <Label key={key} className="block">
                  {label}
                  <Textarea
                    className="mt-2"
                    required={key === "title" || key === "ctaTitle"}
                    maxLength={max}
                    value={settings[key]}
                    onChange={(e) =>
                      setSettings({ ...settings, [key]: e.target.value })
                    }
                  />
                </Label>
              ))}
              <Button>Save page settings</Button>
            </form>
          )}
        </fieldset>
      )}
    </div>
  );
}
