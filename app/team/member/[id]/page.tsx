import { notFound } from "next/navigation";
import Link from "next/link";
import { publicMember } from "@/lib/team-data";
import { ShareActions } from "@/components/team/share-actions";
export const dynamic = "force-dynamic";
export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const member = await publicMember(id);
  if (!member) return { title: "Member unavailable — Epoch" };
  const origin = process.env.NEXTAUTH_URL || "http://localhost:3000";
  const title = [member.person.name, member.por, `AY ${member.year.year}`].filter(Boolean).join(" · ");
  const images = [
    {
      url: `${origin}/team/member/${id}/image`,
      width: 1200,
      height: 1200,
      alt: title,
    },
  ];
  return {
    title,
    description: member.person.tagline,
    openGraph: { title, images, url: `${origin}/team/member/${id}` },
    twitter: { card: "summary_large_image" as const, title, images },
  };
}
export default async function MemberPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const member = await publicMember(id);
  if (!member) notFound();
  return (
    <div className="mx-auto max-w-2xl space-y-8 px-4 py-12">
      <Link
        href={`/team?year=${member.year.year}`}
        className="text-sm text-muted-foreground hover:underline"
      >
        ← Back to AY {member.year.year}
      </Link>
      <h1 className="text-2xl font-semibold">
        {member.person.name}’s Epoch card
      </h1>
      <img
        src={`/team/member/${id}/image`}
        alt={[member.person.name, member.por, `AY ${member.year.year}`, member.person.tagline].filter(Boolean).join(", ")}
        width={1200}
        height={1200}
        className="w-full rounded-3xl border shadow-xl"
      />
      <ShareActions id={id} name={member.person.name} />
      {member.person.linkedin && (
        <p className="text-center">
          <a
            href={member.person.linkedin}
            target="_blank"
            rel="noopener noreferrer"
            className="text-primary hover:underline"
          >
            Connect on LinkedIn ↗
          </a>
        </p>
      )}
    </div>
  );
}
