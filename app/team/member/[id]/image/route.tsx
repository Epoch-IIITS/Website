import { ImageResponse } from "next/og";
import { NextRequest } from "next/server";
import { publicMember } from "@/lib/team-data";
export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export async function GET(
  req: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  const member = await publicMember((await params).id);
  if (!member) return new Response("Member not found", { status: 404 });
  const p = member.person;
  let photo = "";
  if (p.photo && /^https:\/\/res\.cloudinary\.com\//.test(p.photo)) {
    try {
      const response = await fetch(p.photo, {
        signal: AbortSignal.timeout(5000),
        redirect: "error",
      });
      if (
        response.ok &&
        response.headers.get("content-type")?.startsWith("image/")
      ) {
        const bytes = await response.arrayBuffer();
        if (bytes.byteLength <= 8 * 1024 * 1024)
          photo = `data:${response.headers.get("content-type")};base64,${Buffer.from(bytes).toString("base64")}`;
      }
    } catch {
      /* Use initials if the photo is unavailable. */
    }
  }
  return new ImageResponse(
    <div
      style={{
        display: "flex",
        width: "100%",
        height: "100%",
        background: "#181122",
        color: "#f6f1fc",
        padding: 72,
        flexDirection: "column",
        fontFamily: "sans-serif",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          fontSize: 30,
          letterSpacing: 5,
        }}
      >
        <span>EPOCH</span>
        <span style={{ color: "#be95ed", letterSpacing: 1 }}>
          AY {member.year.year}
        </span>
      </div>
      <div
        style={{
          display: "flex",
          marginTop: 60,
          gap: 42,
          alignItems: "center",
        }}
      >
        {photo ? (
          <img
            src={photo}
            width={300}
            height={300}
            style={{ borderRadius: 36, objectFit: "cover" }}
          />
        ) : (
          <div
            style={{
              display: "flex",
              width: 300,
              height: 300,
              borderRadius: 36,
              background: "#3a2554",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 100,
            }}
          >
            {p.name
              .split(" ")
              .map((n: string) => n[0])
              .slice(0, 2)
              .join("")}
          </div>
        )}
        <div style={{ display: "flex", flex: 1, flexDirection: "column" }}>
          {member.por && <span style={{ color: "#be95ed", fontSize: 30, marginBottom: 18 }}>
            {member.por}
          </span>}
          <span
            style={{ fontSize: p.name.length > 40 ? 42 : 58, fontWeight: 700 }}
          >
            {p.name}
          </span>
        </div>
      </div>
      <div
        style={{
          display: "flex",
          marginTop: 52,
          fontSize: 34,
          lineHeight: 1.35,
        }}
      >
        {p.tagline}
      </div>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          marginTop: 36,
          color: "#ccc0dc",
          fontSize: 27,
          lineHeight: 1.4,
        }}
      >
        <span>{p.currentRole}</span>
        <span>{p.organization}</span>
      </div>
      <div
        style={{
          display: "flex",
          marginTop: "auto",
          borderTop: "1px solid #59436f",
          paddingTop: 26,
          justifyContent: "space-between",
          fontSize: 23,
          color: "#be95ed",
        }}
      >
        <span>THE PEOPLE BEHIND EPOCH</span>
        <span>Build. Learn. Belong.</span>
      </div>
    </div>,
    {
      width: 1200,
      height: 1200,
      headers: {
        "Cache-Control": "no-store",
        ...(req.nextUrl.searchParams.has("download")
          ? {
              "Content-Disposition": `attachment; filename="epoch-ay-${member.year.year}-${member._id}.png"`,
            }
          : {}),
      },
    },
  );
}
