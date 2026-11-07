"use client";
import { useEffect, useRef, useState } from "react";
import { TeamEditorDialog } from "@/components/team/editor-dialog";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { ArrowUpRight, ChevronDown, ChevronUp, Copy, Pencil, Plus, Search, Share2, Trash2, X } from "lucide-react";
import { cn } from "@/lib/utils";
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
  "mt-2 h-10 w-full rounded-lg border border-input bg-card px-3 text-sm font-normal focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring";
const inlineSelectClass =
  "h-9 rounded-lg border border-input bg-card px-3 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring";

function Badge({ tone, children }: { tone: "current" | "published" | "draft" | "rejected"; children: React.ReactNode }) {
  const tones = {
    current: "bg-primary-soft text-primary",
    published: "bg-success-soft text-success",
    draft: "bg-secondary text-muted-foreground",
    rejected: "bg-destructive/10 text-destructive",
  };
  return <span className={cn("inline-flex shrink-0 items-center rounded-full px-2.5 py-0.5 text-xs font-medium", tones[tone])}>{children}</span>;
}

function Avatar({ name, photo }: { name: string; photo?: string }) {
  const initials = name.split(/\s+/).filter(Boolean).slice(0, 2).map((word) => word[0]?.toUpperCase()).join("");
  return photo ? (
    // eslint-disable-next-line @next/next/no-img-element
    <img src={photo} alt="" className="h-9 w-9 shrink-0 rounded-full object-cover" />
  ) : (
    <span aria-hidden="true" className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-secondary text-xs font-semibold text-muted-foreground">{initials || "?"}</span>
  );
}

function SectionHeader({ title, description, children }: { title: string; description: string; children?: React.ReactNode }) {
  return (
    <div className="flex flex-wrap items-end justify-between gap-3">
      <div className="flex flex-col gap-1">
        <h2 className="text-lg font-semibold">{title}</h2>
        <p className="text-sm text-muted-foreground">{description}</p>
      </div>
      {children && <div className="flex flex-wrap items-center gap-2">{children}</div>}
    </div>
  );
}

function Empty({ children }: { children: React.ReactNode }) {
  return <p className="rounded-xl border border-dashed border-input bg-card px-5 py-10 text-center text-sm text-muted-foreground">{children}</p>;
}
const blankAppointment = {
  personId: "",
  yearId: "",
  groupId: "",
  por: "",
  order: 0,
  published: false,
};
const emptyPersonProfile = { ...emptyProfile, email: "" };
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
  const [profile, setProfile] = useState(emptyPersonProfile);
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
    setProfile(person ? { ...emptyPersonProfile, ...person } : emptyPersonProfile);
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
        <label className="flex items-center gap-2.5 rounded-lg border bg-muted/30 px-3 py-2.5 text-sm sm:col-span-2">
          <input
            type="checkbox"
            className="h-4 w-4 accent-[hsl(var(--primary))]"
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
  const pendingCount = data ? data.requests.filter((r) => r.status === "pending").length : 0;
  const tabs = [
    { key: "years", label: "Academic years", count: data?.years.length },
    { key: "people", label: "People", count: data?.people.length },
    { key: "roster", label: "Appointments", count: data?.appointments.length },
    { key: "requests", label: "Requests", count: pendingCount || undefined, highlight: pendingCount > 0 },
    { key: "settings", label: "Page settings" },
  ];
  const search = peopleSearch.trim().toLocaleLowerCase();
  const shownPeople = data ? data.people.filter((person) => person.name.toLocaleLowerCase().includes(search)) : [];
  const appointmentsByPerson = new Map<string, number>();
  data?.appointments.forEach((a) => appointmentsByPerson.set(a.personId, (appointmentsByPerson.get(a.personId) ?? 0) + 1));
  const shownAppointments = data
    ? data.appointments
        .filter((a) => !filterYear || a.yearId === filterYear)
        .map((a) => {
          const appointmentYear = data.years.find((y) => y._id === a.yearId);
          return {
            appointment: a,
            person: data.people.find((p) => p._id === a.personId),
            year: appointmentYear,
            group: appointmentYear?.groups.find((g) => g.id === a.groupId),
          };
        })
        .sort((x, y) => (y.year?.year ?? 0) - (x.year?.year ?? 0) || (x.year?.groups.findIndex((g) => g.id === x.appointment.groupId) ?? 0) - (y.year?.groups.findIndex((g) => g.id === y.appointment.groupId) ?? 0) || x.appointment.order - y.appointment.order)
    : [];
  const shownRequests = data ? data.requests.filter((r) => requestFilter === "all" || r.status === requestFilter) : [];

  return (
    <div className="mx-auto flex max-w-[1280px] flex-col gap-6 px-2 py-2 sm:px-4 lg:py-4">
      <header className="flex flex-wrap items-end justify-between gap-4">
        <div className="flex flex-col gap-1.5">
          <h1 className="text-[28px] font-semibold tracking-tight">Team</h1>
          <p className="text-sm text-muted-foreground">Academic years, people and their appointments for the public Team page.</p>
        </div>
        <Button variant="outline" asChild>
          <Link href="/team" target="_blank">View directory<ArrowUpRight className="h-4 w-4" /></Link>
        </Button>
      </header>

      <nav aria-label="Team administration" className="-mx-2 overflow-x-auto border-b px-2">
        <div className="flex min-w-max gap-6">
          {tabs.map(({ key, label, count, highlight }) => (
            <button
              key={key}
              type="button"
              disabled={busy || photoUploading}
              onClick={() => {
                setTab(key);
                setMessage("");
                setRequest(null);
                editPerson();
                editAppointment();
              }}
              aria-pressed={tab === key}
              className={cn(
                "-mb-px flex h-11 items-center gap-2 border-b-2 text-sm font-medium transition-colors disabled:opacity-50",
                tab === key ? "border-foreground text-foreground" : "border-transparent text-muted-foreground hover:text-foreground",
              )}
            >
              {label}
              {count !== undefined && (
                <span className={cn("rounded-full px-1.5 py-px text-[11px] tabular-nums", highlight ? "bg-primary text-primary-foreground" : "bg-secondary text-muted-foreground")}>{count}</span>
              )}
            </button>
          ))}
        </div>
      </nav>

      {error && !editor && !request && (
        <div role="alert" className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-destructive/40 bg-card px-4 py-3 text-sm text-destructive">
          <span>{error}</span>
          {!data && (
            <Button
              variant="outline"
              size="sm"
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
        <div role="status" className="flex items-center justify-between gap-3 rounded-xl border border-success/30 bg-success-soft px-4 py-3 text-sm text-success">
          <span>{message}</span>
          <button type="button" aria-label="Dismiss" className="rounded p-0.5 hover:bg-black/5" onClick={() => setMessage("")}><X className="h-4 w-4" /></button>
        </div>
      )}

      {!data ? (
        <div role="status" aria-label="Loading workspace" className="flex flex-col gap-3">
          {[1, 2, 3].map((n) => <div key={n} className="h-16 animate-pulse rounded-xl border bg-muted" />)}
        </div>
      ) : (
        <fieldset disabled={busy || photoUploading} className="min-w-0 space-y-5">
          {tab === "years" && (
            <>
              <SectionHeader title="Academic years" description="Each year has its own ordered hierarchy groups. Only one published year is current.">
                <Button
                  onClick={() => {
                    openEditor("year");
                    setYearId("");
                    setYear({
                      year: new Date().getFullYear(),
                      published: false,
                      groups: [{ id: crypto.randomUUID(), name: "Executive Committee" }],
                    });
                  }}
                >
                  <Plus className="h-4 w-4" />New academic year
                </Button>
              </SectionHeader>
              {!data.years.length ? (
                <Empty>Create your first academic year to start building a roster.</Empty>
              ) : (
                <ul className="overflow-hidden rounded-xl border bg-card">
                  {[...data.years].sort((a, b) => b.year - a.year).map((y) => {
                    const isCurrent = data.settings.currentYearId === y._id;
                    const members = data.appointments.filter((a) => a.yearId === y._id).length;
                    return (
                      <li key={y._id} className="flex flex-col gap-3 border-b px-5 py-4 last:border-b-0 lg:flex-row lg:items-center lg:gap-6">
                        <div className="flex min-w-[180px] items-center gap-3">
                          <h3 className="text-base font-semibold">AY {y.year}</h3>
                          <Badge tone={isCurrent ? "current" : y.published ? "published" : "draft"}>{isCurrent ? "Current" : y.published ? "Published" : "Draft"}</Badge>
                        </div>
                        <div className="flex min-w-0 flex-1 flex-col gap-1.5">
                          <ol aria-label={`AY ${y.year} hierarchy`} className="flex flex-wrap gap-1.5">
                            {y.groups.map((g, index) => (
                              <li key={g.id} className="inline-flex items-center gap-1.5 rounded-md border bg-background px-2 py-0.5 text-xs">
                                <span className="font-mono text-[10px] text-subtle">{index + 1}</span>{g.name}
                              </li>
                            ))}
                          </ol>
                          <span className="text-xs text-subtle">{members} {members === 1 ? "appointment" : "appointments"}</span>
                        </div>
                        <div className="flex flex-wrap gap-2">
                          {y.published && !isCurrent && (
                            <Button size="sm" variant="outline" onClick={() => save({ action: "current", id: y._id })}>Make current</Button>
                          )}
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => {
                              openEditor("year");
                              setYearId("");
                              setYear({
                                year: y.year + 1,
                                published: false,
                                groups: y.groups.map((g) => ({ ...g, id: crypto.randomUUID() })),
                              });
                            }}
                          >
                            <Copy className="h-4 w-4" />Copy hierarchy
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => {
                              openEditor("year");
                              setYearId(y._id);
                              setYear({ year: y.year, published: y.published, groups: y.groups });
                            }}
                          >
                            <Pencil className="h-4 w-4" />Edit
                          </Button>
                        </div>
                      </li>
                    );
                  })}
                </ul>
              )}
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
                    if (await save({ action: "year", id: yearId || undefined, value: year })) {
                      setEditor(null);
                      setYearId("");
                      setYear({ ...year, year: year.year + 1, published: false });
                    }
                  }}
                >
                  <div className="grid gap-4 sm:grid-cols-2">
                    <Label className="block">
                      AY year
                      <Input
                        className="mt-2"
                        type="number"
                        required
                        min={2000}
                        max={2200}
                        value={year.year}
                        onChange={(e) => setYear({ ...year, year: Number(e.target.value) })}
                      />
                    </Label>
                    <label className="flex items-center gap-2.5 self-end rounded-lg border bg-muted/30 px-3 py-2.5 text-sm">
                      <input
                        type="checkbox"
                        className="h-4 w-4 accent-[hsl(var(--primary))]"
                        checked={year.published}
                        onChange={(e) => setYear({ ...year, published: e.target.checked })}
                      />
                      Publish this academic year
                    </label>
                  </div>
                  <div className="space-y-3">
                    <div>
                      <h3 className="text-sm font-medium">Hierarchy, from top to bottom</h3>
                      <p className="mt-1 text-xs text-muted-foreground">Group headings are separate from each person’s POR. Move members before removing their group.</p>
                    </div>
                    <ol className="space-y-2">
                      {year.groups.map((g, i) => (
                        <li key={g.id} className="flex items-center gap-1 rounded-lg border bg-card p-1 pl-3">
                          <span className="w-5 shrink-0 font-mono text-xs text-subtle">{i + 1}</span>
                          <Input
                            aria-label={`Group ${i + 1} name`}
                            required
                            maxLength={80}
                            value={g.name}
                            className="h-9 border-0 bg-transparent shadow-none focus-visible:ring-1"
                            onChange={(e) =>
                              setYear({
                                ...year,
                                groups: year.groups.map((v, n) => (n === i ? { ...v, name: e.target.value } : v)),
                              })
                            }
                          />
                          {[-1, 1].map((direction) => (
                            <Button
                              key={direction}
                              type="button"
                              variant="ghost"
                              size="icon"
                              className="h-9 w-9 shrink-0"
                              disabled={i + direction < 0 || i + direction >= year.groups.length}
                              aria-label={`Move ${g.name} ${direction === -1 ? "up" : "down"}`}
                              onClick={() => {
                                const groups = [...year.groups];
                                [groups[i], groups[i + direction]] = [groups[i + direction], groups[i]];
                                setYear({ ...year, groups });
                              }}
                            >
                              {direction === -1 ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                            </Button>
                          ))}
                          <Button
                            type="button"
                            size="icon"
                            variant="ghost"
                            className="h-9 w-9 shrink-0 text-muted-foreground hover:text-destructive"
                            aria-label={`Remove ${g.name}`}
                            disabled={year.groups.length === 1}
                            onClick={() => setYear({ ...year, groups: year.groups.filter((v) => v.id !== g.id) })}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </li>
                      ))}
                    </ol>
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={() => setYear({ ...year, groups: [...year.groups, { id: crypto.randomUUID(), name: "" }] })}
                    >
                      <Plus className="h-4 w-4" />Add group
                    </Button>
                  </div>
                  <div className="border-t pt-4">
                    <Button>{busy ? "Saving…" : "Save academic year"}</Button>
                  </div>
                </form>
              </TeamEditorDialog>
            </>
          )}

          {tab === "people" && (
            <>
              <SectionHeader title="People" description="Profiles hold current career details shared across every year.">
                <Button
                  onClick={() => {
                    editPerson();
                    openEditor("person");
                  }}
                >
                  <Plus className="h-4 w-4" />New profile
                </Button>
              </SectionHeader>
              <div className="relative max-w-sm">
                <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-subtle" aria-hidden="true" />
                <Input
                  type="search"
                  aria-label="Find person by name"
                  className="pl-9"
                  placeholder="Search people…"
                  value={peopleSearch}
                  onChange={(event) => setPeopleSearch(event.target.value)}
                />
              </div>
              {!data.people.length ? (
                <Empty>Add profiles here, then assign them to an academic year.</Empty>
              ) : !shownPeople.length ? (
                <p role="status" className="py-4 text-sm text-muted-foreground">No people match this name.</p>
              ) : (
                <ul className="overflow-hidden rounded-xl border bg-card">
                  {shownPeople.map((p) => {
                    const count = appointmentsByPerson.get(p._id) ?? 0;
                    return (
                      <li key={p._id} className="border-b last:border-b-0">
                        <button
                          type="button"
                          className="flex w-full items-center gap-3 px-5 py-3 text-left transition-colors hover:bg-muted/40"
                          onClick={() => {
                            editPerson(p);
                            openEditor("person");
                          }}
                        >
                          <Avatar name={p.name} photo={p.photo} />
                          <span className="flex min-w-0 flex-1 flex-col">
                            <span className="truncate text-sm font-medium">{p.name}</span>
                            <span className="truncate text-xs text-muted-foreground">{[p.currentRole, p.organization].filter(Boolean).join(" · ") || "No career details"}</span>
                          </span>
                          {p.email && <span className="hidden truncate text-xs text-subtle md:block">{p.email}</span>}
                          <span className="w-28 shrink-0 text-right text-xs text-subtle">{count} {count === 1 ? "appointment" : "appointments"}</span>
                          <Pencil className="h-4 w-4 shrink-0 text-subtle" aria-hidden="true" />
                        </button>
                      </li>
                    );
                  })}
                </ul>
              )}
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
                    if (await save({ action: "person", id: personId || undefined, value: profile })) {
                      setEditor(null);
                      editPerson();
                    }
                  }}
                >
                  <p className="text-sm text-muted-foreground">Current career details update across all years. Yearly PORs are managed in Appointments.</p>
                  <ProfileFields
                    value={profile}
                    onChange={(value) => setProfile((current) => ({ ...current, ...value }))}
                    onUploadingChange={setPhotoUploading}
                    beforeTagline={
                      <Label className="block">
                        Account email
                        <Input
                          className="mt-2"
                          type="email"
                          maxLength={320}
                          value={profile.email}
                          onChange={(event) => setProfile({ ...profile, email: event.target.value })}
                          placeholder="member@example.com"
                        />
                        <span className="mt-2 block text-xs font-normal text-muted-foreground">Used privately to show this member the profile editor after sign-in.</span>
                      </Label>
                    }
                  />
                  {profile.name && (
                    <div className="space-y-3 border-t pt-4">
                      <p className="kicker">Card preview</p>
                      <div className="max-w-xs"><MemberCard person={{ ...profile, _id: personId }} por="Position of responsibility" /></div>
                    </div>
                  )}
                  <div className="border-t pt-4">
                    <Button>{busy ? "Saving…" : "Save profile"}</Button>
                  </div>
                </form>
              </TeamEditorDialog>
            </>
          )}

          {tab === "roster" && (
            <>
              <SectionHeader title="Appointments" description="Who held which position in each academic year.">
                <select aria-label="Filter by academic year" className={inlineSelectClass} value={filterYear} onChange={(e) => setFilterYear(e.target.value)}>
                  <option value="">All years</option>
                  {data.years.map((y) => <option key={y._id} value={y._id}>AY {y.year}</option>)}
                </select>
                <Button
                  onClick={() => {
                    editAppointment(undefined, filterYear);
                    openEditor("appointment");
                  }}
                >
                  <Plus className="h-4 w-4" />New appointment
                </Button>
              </SectionHeader>
              {!shownAppointments.length ? (
                <Empty>{data.appointments.length ? "No appointments in this academic year." : "No appointments yet."}</Empty>
              ) : (
                <div className="overflow-x-auto rounded-xl border bg-card">
                  <table className="w-full min-w-[760px] border-collapse text-sm">
                    <thead>
                      <tr className="border-b text-left text-xs text-subtle">
                        <th className="px-5 py-2.5 font-medium">Person</th>
                        <th className="px-3 py-2.5 font-medium">Year</th>
                        <th className="px-3 py-2.5 font-medium">Group</th>
                        <th className="px-3 py-2.5 font-medium">POR</th>
                        <th className="px-3 py-2.5 text-right font-medium">Order</th>
                        <th className="px-3 py-2.5 font-medium">Status</th>
                        <th className="px-5 py-2.5"><span className="sr-only">Actions</span></th>
                      </tr>
                    </thead>
                    <tbody>
                      {shownAppointments.map(({ appointment: a, person, year: appointmentYear, group }) => (
                        <tr key={a._id} className="border-b last:border-b-0">
                          <td className="px-5 py-3">
                            <span className="flex items-center gap-3"><Avatar name={person?.name || "?"} photo={person?.photo} /><span className="font-medium">{person?.name || "Unknown person"}</span></span>
                          </td>
                          <td className="whitespace-nowrap px-3 py-3 font-mono text-xs text-muted-foreground">AY {appointmentYear?.year ?? "—"}</td>
                          <td className="px-3 py-3 text-muted-foreground">{group?.name || "Unknown group"}</td>
                          <td className="px-3 py-3">{a.por || <span className="text-subtle">—</span>}</td>
                          <td className="px-3 py-3 text-right font-mono text-xs tabular-nums text-muted-foreground">{a.order}</td>
                          <td className="px-3 py-3"><Badge tone={a.published ? "published" : "draft"}>{a.published ? "Published" : "Draft"}</Badge></td>
                          <td className="px-5 py-3">
                            <div className="flex justify-end gap-1">
                              {a.published && appointmentYear?.published && (
                                <Button size="icon" variant="ghost" className="h-8 w-8" asChild>
                                  <Link href={`/team/member/${a._id}`} aria-label={`View share card for ${person?.name}`} title="View share card"><Share2 className="h-4 w-4" /></Link>
                                </Button>
                              )}
                              <Button
                                size="icon"
                                variant="ghost"
                                className="h-8 w-8"
                                aria-label={`Edit ${person?.name}'s appointment`}
                                title="Edit"
                                onClick={() => {
                                  editAppointment(a);
                                  openEditor("appointment");
                                }}
                              >
                                <Pencil className="h-4 w-4" />
                              </Button>
                              <Button
                                size="icon"
                                variant="ghost"
                                className="h-8 w-8 text-muted-foreground hover:text-destructive"
                                aria-label={`Remove ${person?.name}'s appointment`}
                                title="Remove"
                                onClick={() => {
                                  if (window.confirm("Remove this appointment? The person’s profile will remain available."))
                                    void save({ action: "remove-appointment", id: a._id });
                                }}
                              >
                                <Trash2 className="h-4 w-4" />
                              </Button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
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
                    if (await save({ action: "appointment", id: appointmentId || undefined, value: appointment })) {
                      setEditor(null);
                      editAppointment();
                    }
                  }}
                >
                  <PersonPicker people={data.people} value={appointment.personId} onChange={(personId) => setAppointment({ ...appointment, personId })} />
                  {appointmentFields()}
                  {appointment.personId && appointment.yearId && (
                    <div className="space-y-3 border-t pt-4">
                      <p className="kicker">Card preview</p>
                      <div className="max-w-xs"><MemberCard person={data.people.find((p) => p._id === appointment.personId)!} por={appointment.por} /></div>
                    </div>
                  )}
                  <div className="border-t pt-4">
                    <Button>{busy ? "Saving…" : "Save appointment"}</Button>
                  </div>
                </form>
              </TeamEditorDialog>
            </>
          )}

          {tab === "requests" && (
            <>
              <SectionHeader title="Listing requests" description="Members ask to be listed from the public Team page.">
                <div role="group" aria-label="Request status" className="flex gap-0.5 rounded-lg bg-secondary p-0.5">
                  {["pending", "approved", "rejected", "all"].map((s) => (
                    <button
                      key={s}
                      type="button"
                      aria-pressed={requestFilter === s}
                      onClick={() => setRequestFilter(s)}
                      className={cn("h-8 rounded-md px-3 text-[13px] font-medium capitalize transition-colors", requestFilter === s ? "bg-card text-foreground shadow-sm" : "text-muted-foreground hover:text-foreground")}
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </SectionHeader>
              {!shownRequests.length ? (
                <Empty>No {requestFilter === "all" ? "" : requestFilter} requests.</Empty>
              ) : (
                <ul className="overflow-hidden rounded-xl border bg-card">
                  {shownRequests.map((r) => (
                    <li key={r._id} className="flex flex-col gap-3 border-b px-5 py-4 last:border-b-0 md:flex-row md:items-start md:gap-6">
                      <div className="flex min-w-0 flex-1 gap-3">
                        <Avatar name={r.name} photo={r.photo} />
                        <div className="flex min-w-0 flex-col gap-1">
                          <div className="flex flex-wrap items-center gap-2">
                            <h3 className="text-sm font-semibold">{r.name}</h3>
                            <Badge tone={r.status === "approved" ? "published" : r.status === "rejected" ? "rejected" : "draft"}>{r.status[0].toUpperCase() + r.status.slice(1)}</Badge>
                          </div>
                          <p className="text-sm text-muted-foreground">{[`AY ${r.year}`, r.por, r.group].filter(Boolean).join(" · ")}</p>
                          <p className="break-all text-xs text-subtle">{r.email} · {new Date(r.createdAt).toLocaleDateString()}</p>
                          {r.notes && <p className="mt-1 whitespace-pre-wrap text-sm">{r.notes}</p>}
                          {r.reason && <p className="mt-1 text-sm"><span className="text-muted-foreground">Feedback:</span> {r.reason}</p>}
                        </div>
                      </div>
                      {r.status === "pending" && (
                        <Button
                          size="sm"
                          onClick={() => {
                            editorTrigger.current = document.activeElement as HTMLElement | null;
                            setError("");
                            setRequest(r);
                            setProfile(r);
                            setReason("");
                            setReviewPerson("");
                            setAppointment({
                              ...blankAppointment,
                              yearId: data.years.find((y) => y.year === r.year)?._id || "",
                              por: r.por || "",
                            });
                          }}
                        >
                          Review
                        </Button>
                      )}
                    </li>
                  ))}
                </ul>
              )}
              <TeamEditorDialog
                {...dialogProps}
                onClose={() => {
                  setRequest(null);
                  setError("");
                }}
                open={Boolean(request)}
                title={request ? `Review ${request.name}` : "Review request"}
                description="Approve to add them to the directory, or reject with feedback the applicant can see."
              >
                {request && (
                  <form
                    className="space-y-5"
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
                    <Label className="block">
                      Link to an existing person or create a profile
                      <select className={selectClass} value={reviewPerson} onChange={(e) => setReviewPerson(e.target.value)}>
                        <option value="">Create a new profile from these details</option>
                        {data.people.map((p) => <option key={p._id} value={p._id}>{p.name}</option>)}
                      </select>
                    </Label>
                    {reviewPerson ? (
                      <p className="text-sm text-muted-foreground">The existing profile will be kept. Approval creates or updates their appointment for the selected year. Edit their profile in People if needed.</p>
                    ) : (
                      <ProfileFields value={profile} onChange={(value) => setProfile((current) => ({ ...current, ...value }))} onUploadingChange={setPhotoUploading} />
                    )}
                    {appointmentFields()}
                    <div className="border-t pt-4">
                      <Button>Approve request</Button>
                    </div>
                    <div className="space-y-3 rounded-lg border border-destructive/30 p-4">
                      <Label className="block">
                        Rejection feedback (visible to applicant)
                        <Textarea className="mt-2" maxLength={1000} value={reason} onChange={(e) => setReason(e.target.value)} />
                      </Label>
                      <Button
                        type="button"
                        variant="destructive"
                        disabled={!reason.trim()}
                        onClick={async () => {
                          if (await save({ action: "review", id: request._id, decision: "reject", reason })) setRequest(null);
                        }}
                      >
                        Reject request
                      </Button>
                    </div>
                  </form>
                )}
              </TeamEditorDialog>
            </>
          )}

          {tab === "settings" && (
            <>
              <SectionHeader title="Page settings" description="Text shown on the public Team page." />
              <form
                className="max-w-3xl space-y-5 rounded-xl border bg-card p-5 sm:p-6"
                onSubmit={(e) => {
                  e.preventDefault();
                  void save({ action: "settings", value: settings });
                }}
              >
                {(
                  [
                    ["title", "Page heading", 100],
                    ["ctaTitle", "Request section heading", 100],
                    ["ctaText", "Request section description", 500],
                  ] as const
                ).map(([key, label, max]) => (
                  <Label key={key} className="block">
                    {label}
                    {key === "ctaText" ? (
                      <Textarea className="mt-2" maxLength={max} value={settings[key]} onChange={(e) => setSettings({ ...settings, [key]: e.target.value })} />
                    ) : (
                      <Input className="mt-2" required maxLength={max} value={settings[key]} onChange={(e) => setSettings({ ...settings, [key]: e.target.value })} />
                    )}
                  </Label>
                ))}
                <div className="border-t pt-4">
                  <Button>Save page settings</Button>
                </div>
              </form>
            </>
          )}
        </fieldset>
      )}
    </div>
  );
}
