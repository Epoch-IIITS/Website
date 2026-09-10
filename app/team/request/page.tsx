"use client";
import { useEffect, useState } from "react";
import { useSession } from "next-auth/react";
import Link from "next/link";
import { ProfileFields, emptyProfile } from "@/components/team/profile-fields";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

export default function RequestPage() {
  const { data: session, status } = useSession();
  const [profile, setProfile] = useState(emptyProfile);
  const [year, setYear] = useState(new Date().getFullYear());
  const [group, setGroup] = useState("");
  const [por, setPor] = useState("");
  const [notes, setNotes] = useState("");
  const [consent, setConsent] = useState(false);
  const [photoUploading, setPhotoUploading] = useState(false);
  const [requests, setRequests] = useState<any[]>([]);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  async function load() {
    try {
      const response = await fetch("/api/team/requests");
      const data = await response.json();
      if (!response.ok) throw new Error(data.error);
      setRequests(data.requests);
    } catch (e: any) {
      setError(e.message);
    }
  }
  useEffect(() => {
    if (status === "authenticated") void load();
  }, [status]);
  return (
    <div className="mx-auto max-w-3xl px-4 py-12">
      <Link href="/team" className="text-sm text-muted-foreground">
        ← Team directory
      </Link>
      <h1 className="mt-6 text-4xl font-semibold">
        Your place in the Epoch story.
      </h1>
      <p className="my-5 text-muted-foreground">
        Send your details for review. An admin will verify your academic year
        and position before adding you to the directory.
      </p>
      {status === "loading" ? (
        <p>Loading…</p>
      ) : !session ? (
        <Button asChild>
          <Link href="/auth/signin?callbackUrl=%2Fteam%2Frequest">
            Sign in to submit your details
          </Link>
        </Button>
      ) : (
        <>
          <form
            className="space-y-6 rounded-2xl border bg-card p-6"
            onSubmit={async (e) => {
              e.preventDefault();
              setBusy(true);
              setError("");
              setMessage("");
              try {
                const response = await fetch("/api/team/requests", {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({
                    ...profile,
                    year,
                    group,
                    por,
                    notes,
                    consent,
                  }),
                });
                const data = await response.json();
                if (!response.ok) throw new Error(data.error);
                setMessage(
                  "Your request has been saved and is awaiting review.",
                );
                setConsent(false);
                await load();
              } catch (e: any) {
                setError(e.message);
              } finally {
                setBusy(false);
              }
            }}
          >
            <fieldset disabled={busy || photoUploading} className="space-y-6">
              <p className="text-sm text-muted-foreground">
                Signed in as {session.user.email}. Your email is only visible to
                administrators.
              </p>
              <ProfileFields
                value={profile}
                onChange={setProfile}
                onUploadingChange={setPhotoUploading}
              />
              <div className="grid gap-4 sm:grid-cols-2">
                <Label>
                  Academic year
                  <Input
                    className="mt-2"
                    type="number"
                    min={2000}
                    max={2200}
                    required
                    value={year}
                    onChange={(e) => setYear(Number(e.target.value))}
                  />
                </Label>
                <Label>
                  Position of responsibility (POR, optional)
                  <Input
                    className="mt-2"
                    maxLength={100}
                    placeholder="e.g. NLP Lead"
                    value={por}
                    onChange={(e) => setPor(e.target.value)}
                  />
                </Label>
              </div>
              <Label className="block">
                Suggested hierarchy group
                <Input
                  className="mt-2"
                  maxLength={80}
                  placeholder="e.g. Domain Leads — leave blank if unsure"
                  value={group}
                  onChange={(e) => setGroup(e.target.value)}
                />
              </Label>
              <Label className="block">
                Notes for the admin
                <Textarea
                  className="mt-2"
                  maxLength={2000}
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                />
              </Label>
              <label className="flex items-start gap-3 text-sm">
                <input
                  className="mt-1"
                  type="checkbox"
                  required
                  checked={consent}
                  onChange={(e) => setConsent(e.target.checked)}
                />
                I consent to publishing these profile details and photo in the
                Team directory and downloadable share cards after approval.
              </label>
              <Button disabled={busy}>
                {busy ? "Submitting…" : "Submit for review"}
              </Button>
            </fieldset>
          </form>
          {error && (
            <p role="alert" className="mt-4 text-destructive">
              {error}
            </p>
          )}
          {message && (
            <p role="status" className="mt-4 text-primary">
              {message}
            </p>
          )}
          <section className="mt-10">
            <h2 className="mb-4 text-xl font-semibold">Your requests</h2>
            {!requests.length && (
              <p className="text-muted-foreground">No requests yet.</p>
            )}
            <div className="space-y-3">
              {requests.map((r) => (
                <article key={r._id} className="rounded-xl border p-4">
                  <div className="flex flex-wrap justify-between gap-3">
                    <h3 className="font-medium">
                      {[`AY ${r.year}`, r.por].filter(Boolean).join(" · ")}
                    </h3>
                    <span className="text-sm capitalize">{r.status}</span>
                  </div>
                  {r.reason && (
                    <p className="mt-2 text-sm text-muted-foreground">
                      Admin feedback: {r.reason}
                    </p>
                  )}
                </article>
              ))}
            </div>
          </section>
        </>
      )}
    </div>
  );
}
