# Project starting guide

## Overview

Epoch is a full-stack tech club website for sharing blogs, projects, events, and photo galleries. Members can sign in, manage their profile, register for events, and download PDF tickets with QR codes. A sidebar admin workspace manages content, users, event registrations, and contact queries.

The app is a single Next.js project: pages and API handlers live together in `app/`. There is no separate backend service in this repository.

## Stack

- Next.js 15.2.8 App Router, React 18, and TypeScript with strict mode.
- Tailwind CSS 3, shadcn/ui-style components backed by Radix UI, Lucide icons, and `next-themes`.
- MongoDB through Mongoose; Zod schemas for content validation.
- NextAuth v4 with Google OAuth and email/password credentials, using JWT sessions.
- Cloudinary for image uploads; PDFKit and QRCode for event tickets.
- The `@/*` import alias resolves from the repository root.

## Local setup

1. Install Node.js compatible with the pinned Next.js version. No Node version is pinned in the repository.
2. Run `npm install`. Both `package-lock.json` and `pnpm-lock.yaml` exist; the README uses npm. Avoid incidental lockfile changes or switching package managers during unrelated work.
3. Configure local environment variables in `.env.local` (Next.js also loads `.env`). Keep credentials out of source control and documentation; `.env*` files are ignored.
4. Run `npm run dev` and open `http://localhost:3000`.

For local admin access without Google, add an unused email to `ADMIN_EMAILS`, restart the dev server, and open `/auth/signin`. The development-only email/password form supports creating an account and signing in, then opens `/admin`. Use the exact configured email when creating the account. Existing Google-only accounts have no password; use a separate development account. This form uses the existing credentials provider and stored roles, and is hidden in production builds.

| Variable | Purpose |
| --- | --- |
| `MONGODB_URI` | MongoDB connection string; `lib/mongodb.ts` throws on import if missing. |
| `NEXTAUTH_URL` | App origin, normally `http://localhost:3000` locally. Also used by server pages to fetch this app's API, so it must match the running app. |
| `NEXTAUTH_SECRET` | NextAuth session secret. |
| `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | Google OAuth credentials; the callback route is `/api/auth/callback/google`. |
| `ADMIN_EMAILS` | Comma-separated emails assigned admin role when new accounts are created. Current parsing does not trim spaces. Changing this list does not update existing users' stored roles. |
| `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` | Required to use image uploads. |

## Where to start reading

| Path | Responsibility |
| --- | --- |
| `app/layout.tsx`, `app/page.tsx` | Root layout, metadata, providers, and homepage content fetching. |
| `app/blog/`, `app/projects/`, `app/events/`, `app/gallery/` | Public content pages. Blog detail URLs use slugs; event and gallery details use IDs. A gallery detail page uses `components/event-gallery.tsx` for its full-image viewer. |
| `app/team/`, `app/contact/`, `app/privacy/`, `app/terms/` | Team directory and informational pages. `/about` permanently redirects to `/team`. |
| `app/auth/`, `app/profile/`, `app/my-rsvps/` | Sign-in/error screens and member pages. |
| `app/admin/`, `components/admin-shell.tsx` | Sidebar workspace, overview, content CRUD, users, event RSVPs, and the contact queries inbox at `/admin/queries`. |
| `app/api/` | HTTP route handlers for content, auth, uploads, profiles, and RSVPs. |
| `models/` | Mongoose models: `User`, `Blog`, `Project`, `Event`, `Gallery`, `RSVP`, `ContactQuery`. |
| `lib/mongodb.ts` | Shared MongoDB connector with a cached connection/promise for reuse across reloads. |
| `lib/auth.ts`, `types/next-auth.d.ts` | Authentication callbacks and session/JWT types, including user ID and role. |
| `lib/validations.ts`, `lib/utils.ts` | Shared Zod schemas and helpers such as slug/ticket ID generation and class merging. |
| `lib/ticket-generator.ts`, `fonts/` | PDF ticket generation and local font assets. |
| `components/` | Shared site components, session/theme providers, layout, admin guard, upload UI, and the event gallery viewer. |
| `components/ui/`, `hooks/` | Reusable UI primitives and hooks. Some hook copies also exist under `components/ui/`; check imports before editing. |
| `app/globals.css`, `tailwind.config.ts`, `components.json` | Active global styles, theme tokens, Tailwind, and UI component configuration. `styles/globals.css` also exists; the root layout imports `app/globals.css`. |
| `public/` | Static assets. |

## Main flows and conventions

- Public pages often fetch `/api/...` from server components using `NEXTAUTH_URL` and `cache: "no-store"`. Some fetch failures produce empty content, so an empty page does not necessarily mean the database is empty.
- Content APIs live at `/api/blogs`, `/api/projects`, `/api/events`, and `/api/gallery`. The public blog page uses singular `/blog`. Check each handler's response shape: the blog list returns `{ blogs, pagination }`, while several other lists return arrays.
- API handlers connect through `connectDB()`, use Mongoose models, and generally return JSON with `NextResponse`. Extend shared Zod schemas alongside model, handler, and form changes where applicable.
- `middleware.ts` matches `/api/admin/:path*` and `/api/rsvp/:path*`. Admin pages use `AdminGuard`; content mutation handlers also perform server-side role checks. Preserve server-side authorization rather than relying on the UI guard. The upload handler currently has no session check.
- RSVP creation links an event and user, enforces the deadline/capacity checks in the handler, and generates a ticket ID. The model has a unique event/user index. Tickets at `/api/rsvp/[id]/ticket` are restricted to the owner or an admin.
- Contact Us requires sign-in to view the form and submit through `POST /api/contact`; signed-out visitors see a login prompt that returns them to `/contact` after authentication. The account email is read-only, and the API uses the server session email. Submissions are validated, stored in MongoDB, and shown newest first through admin-only `GET /api/admin/queries?page=1` (20 per page). The form reports success only after persistence. This stores messages for review; it does not send email. Earlier simulated submissions were never saved.
- The Blog, Projects, Events, Gallery, Team, and Contact listing pages use the shared `components/page-kicker.tsx` header. Each header contains only its one-line uppercase kicker; page titles and introductory descriptions are intentionally omitted.
- Gallery detail pages render thumbnails through `EventGallery`. Clicking a photo opens an uncropped full-image dialog; Previous/Next buttons and Left/Right Arrow keys wrap through the collection, while Escape closes the dialog and restores focus to the originating thumbnail. Preserve the dialog title, instructions, counter, captions, broken-image state, and keyboard behavior when changing this component.
- Prefer existing UI components, Tailwind theme tokens, and `@/` imports. Add `"use client"` where browser APIs, React state/effects, or client session hooks require it; keep database and secret-bearing code on the server.
- Admins can permanently delete a contact query through `DELETE /api/admin/queries/[id]`. The inbox requires confirmation, refreshes after deletion, and moves back to the last available page if necessary. The endpoint checks the session's admin role and validates the record ID.
- `Project` has no `createdBy` field. Project detail reads and updates must not populate or assign that relationship; doing so makes existing projects fail to load under Mongoose strict population. The project edit page distinguishes a real 404 from other load failures and offers retry for recoverable errors.
- Several files contain large commented-out earlier implementations. Read the active code before making changes.

## Team directory

- `/team` displays the configured current published academic year, falling back to the newest published year before a current year is selected. `/team?year=2025` links to an archive. Unpublished years and appointments are never returned publicly.
- The public Team page uses the `Epoch Community` kicker followed by a row with the selected AY on the left and the archive dropdown on the right. Group headings are centered, large, and italic. Photo cards show the name at the bottom center by default and reveal smaller left-aligned details over a transparent gradient on hover, keyboard focus, or tap. LinkedIn and share-card actions are right-aligned icon-only links, and per-card AY badges are omitted; dedicated share-card pages and images still identify the AY.
- `/admin/team` manages academic years, their ordered hierarchy groups, people, yearly appointments, requests, and public page text. Groups are year-specific; the group heading (e.g. Domain Leads) is separate from the person's POR (e.g. NLP Lead). Group IDs remain stable on rename/reorder. Members must be moved before removing a populated group.
- Academic year, profile, and appointment editors open in dialogs from their New/Edit actions; Copy hierarchy opens a prefilled new-year dialog. Dialogs close after a successful save, retain errors and entered values on failure, and prevent dismissal during saving or photo upload.
- People can be filtered by name; the appointment editor uses a searchable person combobox with keyboard selection and requires choosing an existing profile. Starting a new appointment while an AY filter is active preselects that academic year.
- POR is optional for appointments and listing requests. Blank or omitted POR values are stored as an empty string and hidden on public cards and share images; the academic year and hierarchy group still organize appointments.
- `models/Team.ts` contains `TeamYear`, `TeamPerson`, `TeamAppointment`, `TeamRequest`, and `TeamSettings`. Profiles hold current career details; appointments hold historical AY/POR/group/order. A person has at most one appointment per AY. The singleton settings record stores the current year, so only one can be current. Switch the current year before unpublishing it.
- Team writes use MongoDB transactions and require a replica set (MongoDB Atlas supports this). Unique indexes are initialized before accepting writes. Admin writes and approval are implemented in `/api/admin/team`; approval atomically creates/links a person, upserts their appointment, and records the review. An already-reviewed request cannot be approved again.
- Copy hierarchy prepares an unsaved year with the same group headings. Appointments are added individually.
- `/team/request` requires sign-in and publication consent. `/api/team/requests` records the session's identity, allows one pending request per applicant/year, and returns only that applicant's request status/feedback. Admins can approve or reject with feedback. Existing profiles are preserved when linking a request; edit their current details separately in People.
- `/api/team/upload` is an authenticated Cloudinary photo upload endpoint for JPG/PNG/WebP up to 5 MB. Team photos use the `epoch-team` folder. It is separate from the existing content upload endpoint.
- Profile photo selection opens a square crop dialog with drag, zoom, and keyboard-accessible position sliders. Only the confirmed crop is uploaded; cancelling keeps the previous photo. Adjust crop can reframe the selected source or existing Cloudinary photo. Profile previews, public cards, and share-card portraits use the same square framing.
- `/team/member/[id]` is the stable public URL for a published appointment. Its `/image` endpoint renders a 1200 × 1200 PNG with `next/og`, used for downloads and social previews. The image centers a compact dark community-profile card with the `public/epoch_logo_with_name.png` brand asset at top right, an infinity-color heatmap, photo or gradient initials, current career details, tagline, and newest-first chips for every appointment that is published under a published AY. A blank POR falls back to that year's hierarchy-group name. The selected appointment and year must also be published; images use no-store responses. Previously downloaded pictures and third-party social caches cannot be revoked. Set `NEXTAUTH_URL` to the public origin for social links.
- Run `node --test scripts/team.test.cjs` for validation, authorization, hierarchy/publication, approval/rejection, duplicate constraints, and real PNG rendering checks. Tests isolate database/session boundaries and do not write to the live database. Optionally set `TEAM_CARD_PREVIEW` to an absolute PNG output path to inspect the generated test card.

## Commands and verification

| Command | Purpose / limitation |
| --- | --- |
| `npm run dev` | Start the development server. |
| `npm run build` | Build for production. `next.config.mjs` skips ESLint and TypeScript build errors, so a successful build does not establish type correctness. |
| `npm start` | Run an existing production build. |
| `npx tsc --noEmit --incremental false` | Run TypeScript checking separately without writing incremental build metadata. |
| `npm run lint` | Invokes `next lint`. No ESLint configuration or direct ESLint dependency is present, so expect an initial setup prompt rather than a ready-to-run unattended check. |

Run `node --test scripts/*.test.cjs` for contact validation, authenticated submission behavior, inbox authorization/pagination/deletion, and project read/update regression tests using isolated database/session boundaries. Project tests use the real Mongoose schema and query handling with database I/O stubbed out. There is no package-level `test` script. `scripts/test-db.js` is a diagnostic script that imports `.js` paths for source files stored as `.ts`; it is not a ready-to-run test harness.

For application changes, run relevant available checks and manually exercise the affected pages/API flows. Check signed-out, member, and admin behavior when changing access control; check responsive layout and both themes for UI changes. Report existing failures separately from regressions. Documentation-only changes do not require an application build.

The README is useful background but has stale details: credentials authentication and Cloudinary uploads are implemented, and the RSVP model has no attendance-status field. Treat current source as authoritative. Keep this root `AGENTS.md` as the single project starting guide, and update it when setup or architecture changes.
