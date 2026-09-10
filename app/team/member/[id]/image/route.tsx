import { ImageResponse } from "next/og";
import { NextRequest } from "next/server";
import { readFile } from "node:fs/promises";
import { join } from "node:path";
import { publicMember } from "@/lib/team-data";
export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const heatmap = [
  [
    "#12184a",
    "#1a1f5a",
    "#232869",
    "#2b3079",
    "#333a89",
    "#3b4498",
    "#454ea6",
    "#4f57ae",
  ],
  [
    "#5a5cb2",
    "#655fb0",
    "#7061ac",
    "#7c63a8",
    "#8765a4",
    "#93679f",
    "#9e6a99",
    "#aa6e93",
  ],
  [
    "#b5728c",
    "#c07685",
    "#ca7b7d",
    "#d38076",
    "#db866f",
    "#e28c68",
    "#e79262",
    "#ea985d",
  ],
  [
    "#ec9f5a",
    "#eba659",
    "#e9ad5b",
    "#e5b45f",
    "#dfba65",
    "#d8c06d",
    "#cfc476",
    "#c5c880",
  ],
  [
    "#c5c880",
    "#cfc476",
    "#d8c06d",
    "#dfba65",
    "#e5b45f",
    "#e9ad5b",
    "#eba659",
    "#ec9f5a",
  ],
  [
    "#ea985d",
    "#e79262",
    "#e28c68",
    "#db866f",
    "#d38076",
    "#ca7b7d",
    "#c07685",
    "#b5728c",
  ],
  [
    "#aa6e93",
    "#9e6a99",
    "#93679f",
    "#8765a4",
    "#7c63a8",
    "#7061ac",
    "#655fb0",
    "#5a5cb2",
  ],
  [
    "#4f57ae",
    "#454ea6",
    "#3b4498",
    "#333a89",
    "#2b3079",
    "#232869",
    "#1a1f5a",
    "#12184a",
  ],
];

export async function GET(
  req: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  const member = await publicMember((await params).id);
  if (!member) return new Response("Member not found", { status: 404 });
  const p = member.person;
  let logo = "";
  try {
    const bytes = await readFile(
      join(process.cwd(), "public", "epoch_logo_with_name.png"),
    );
    logo = `data:image/png;base64,${bytes.toString("base64")}`;
  } catch {
    /* Keep the card usable if the brand asset is unavailable. */
  }
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
  const career = [p.currentRole, p.organization].filter(Boolean).join(" · ");
  const chips = member.positions.map(
    (position: { por: string; group: string; year: number }) =>
      `${position.por || position.group || "Member"} · AY ${position.year}`,
  );
  const taglineLines = Math.max(1, Math.ceil((p.tagline?.length || 0) / 60));
  const cardHeight = Math.min(
    1000,
    560 +
      Math.max(0, taglineLines - 1) * 40 +
      Math.max(0, chips.length - 3) * 55,
  );
  return new ImageResponse(
    <div
      style={{
        display: "flex",
        width: "100%",
        height: "100%",
        alignItems: "center",
        justifyContent: "center",
        background: "#060608",
        color: "#f0eefc",
        padding: 64,
        fontFamily: "sans-serif",
      }}
    >
      <div
        style={{
          display: "flex",
          position: "relative",
          width: "100%",
          height: cardHeight,
          overflow: "hidden",
          flexDirection: "column",
          border: "2px solid #1c1c26",
          borderRadius: 34,
          background: "#0a0a10",
          padding: 52,
        }}
      >
        <div
          style={{
            display: "flex",
            position: "absolute",
            top: 0,
            right: 0,
            width: 360,
            height: 360,
            flexDirection: "column",
            opacity: 0.3,
          }}
        >
          {heatmap.map((row, rowIndex) => (
            <div
              key={rowIndex}
              style={{ display: "flex", width: "100%", flex: 1 }}
            >
              {row.map((color, columnIndex) => (
                <div
                  key={`${rowIndex}-${columnIndex}`}
                  style={{ display: "flex", flex: 1, background: color }}
                />
              ))}
            </div>
          ))}
        </div>
        {logo && (
          <img
            src={logo}
            width={180}
            height={180}
            style={{
              position: "absolute",
              top: -20,
              right: -20,
              objectFit: "contain",
            }}
          />
        )}
        <div
          style={{
            display: "flex",
            position: "relative",
            height: "100%",
            flexDirection: "column",
          }}
        >
          <div
            style={{
              display: "flex",
              color: "#7d7fe0",
              fontSize: 20,
              fontWeight: 600,
              letterSpacing: 2.5,
            }}
          >
            EPOCH.AIML // COMMUNITY PROFILE
          </div>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 30,
              marginTop: 36,
            }}
          >
            {photo ? (
              <img
                src={photo}
                width={180}
                height={180}
                style={{
                  border: "2px solid #2b2938",
                  borderRadius: 24,
                  objectFit: "cover",
                }}
              />
            ) : (
              <div
                style={{
                  display: "flex",
                  width: 180,
                  height: 180,
                  flexShrink: 0,
                  alignItems: "center",
                  justifyContent: "center",
                  borderRadius: 24,
                  background:
                    "linear-gradient(135deg, #3355e0 0%, #7c4fc9 35%, #d6407a 65%, #8a2438 100%)",
                  color: "#ffffff",
                  fontSize: 58,
                  fontWeight: 700,
                }}
              >
                {p.name
                  .split(" ")
                  .map((n: string) => n[0])
                  .slice(0, 2)
                  .join("")}
              </div>
            )}
            <div
              style={{
                display: "flex",
                minWidth: 0,
                flex: 1,
                flexDirection: "column",
              }}
            >
              <span
                style={{
                  fontSize:
                    p.name.length > 40 ? 34 : p.name.length > 26 ? 40 : 46,
                  fontWeight: 700,
                  lineHeight: 1.08,
                }}
              >
                {p.name}
              </span>
              {career && (
                <span
                  style={{
                    marginTop: 14,
                    color: "#9a97c4",
                    fontSize: career.length > 70 ? 19 : 23,
                    lineHeight: 1.35,
                  }}
                >
                  {career}
                </span>
              )}
            </div>
          </div>
          {p.tagline && (
            <div
              style={{
                display: "flex",
                marginTop: 30,
                color: "#d8d3f0",
                fontSize: p.tagline.length > 100 ? 24 : 30,
                lineHeight: 1.35,
              }}
            >
              “{p.tagline}”
            </div>
          )}
          <div
            style={{
              display: "flex",
              marginTop: 30,
              flexDirection: "column",
            }}
          >
            <div
              style={{
                display: "flex",
                marginBottom: 14,
                color: "#6b6890",
                fontSize: 18,
                fontWeight: 600,
                letterSpacing: 2.5,
              }}
            >
              POSITIONS HELD
            </div>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 12 }}>
              {chips.map((chip: string) => (
                <span
                  key={chip}
                  style={{
                    display: "flex",
                    maxWidth: "100%",
                    borderRadius: 14,
                    background: "#3a2650",
                    color: "#f0eefc",
                    fontSize: chips.length > 4 ? 18 : 21,
                    padding: "12px 20px",
                  }}
                >
                  {chip}
                </span>
              ))}
            </div>
          </div>
        </div>
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
