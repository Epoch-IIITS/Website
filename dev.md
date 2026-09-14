# Epoch developer guide

This guide covers local development, verification, and the operational details that contributors should understand before changing the application. The repository contains one full-stack Next.js application; there is no separate backend service.

## Prerequisites

- A Node.js version compatible with Next.js 15. Node.js 20 LTS or newer is recommended; the repository does not currently pin a version.
- npm for the documented workflow.
- A MongoDB Atlas account and cluster. Atlas provides the replica-set deployment required by the application's transactions.
- A Cloudinary account when testing uploads or media cleanup.
- Google OAuth credentials when testing the Google sign-in flow. Development also includes a local email/password provider.

Both `package-lock.json` and `pnpm-lock.yaml` currently exist. The documentation uses npm, while some deployment environments may select pnpm automatically. If dependencies change, keep both lockfiles synchronized until the project standardizes on one package manager.

## Initial setup

1. Clone the repository and enter it.

   ```bash
   git clone https://github.com/Epoch-IIITS/Website.git
   cd Website
   ```

2. Install dependencies.

   ```bash
   npm install
   ```

3. Copy the example environment file and replace its placeholders.

   ```bash
   cp .env.example .env.local
   ```

4. Start the development server.

   ```bash
   npm run dev
   ```

5. Open [http://localhost:3000](http://localhost:3000).

`NEXTAUTH_URL` must match the origin and port used by the development server. Server components use it when calling this application's own API routes.

## Environment variables

| Variable | Required | Purpose |
| --- | --- | --- |
| `MONGODB_URI` | Yes | MongoDB Atlas SRV connection string, including the database name. Audited and team writes use transactions. |
| `NEXTAUTH_URL` | Yes | Application origin, normally `http://localhost:3000` locally. |
| `NEXTAUTH_SECRET` | Yes | Secret used to sign and encrypt authentication data. Generate a unique value for every environment. |
| `GOOGLE_CLIENT_ID` | Production/Google testing | Google OAuth client ID. |
| `GOOGLE_CLIENT_SECRET` | Production/Google testing | Google OAuth client secret. |
| `ADMIN_EMAILS` | For admin setup | Comma-separated email addresses that receive the admin role when their account is first created. |
| `CLOUDINARY_CLOUD_NAME` | For media features | Cloudinary cloud name used for uploads, URL ownership checks, and cleanup. |
| `CLOUDINARY_API_KEY` | For media features | Cloudinary API key. |
| `CLOUDINARY_API_SECRET` | For media features | Cloudinary API secret; keep it server-side. |

There is no cron secret or scheduled cleanup task. Media maintenance is run manually.

### Google OAuth

Create a web OAuth client and add this local callback URL:

```text
http://localhost:3000/api/auth/callback/google
```

Use the deployed origin instead of `localhost:3000` for the production callback.

### Local admin access without Google

The email/password provider is registered only while `NODE_ENV=development`.

1. Add an unused development email to `ADMIN_EMAILS`.
2. Restart the development server.
3. Open `/auth/signin` and create an account with that email and a password of at least eight characters.
4. Continue to `/admin` after signing in.

Changing `ADMIN_EMAILS` does not update roles for accounts already stored in MongoDB. Google-only accounts do not have a password, so use a separate development account for local credential testing.

## MongoDB Atlas setup

Admin audit writes and compound team writes are committed in MongoDB transactions. Use a MongoDB Atlas cluster for development because Atlas supplies the replica-set deployment those transactions require; no local Docker database or manual `rs.initiate()` step is needed.

1. Create or select an Atlas project, then create a cluster suitable for development.
2. In Database Access, create a dedicated database user for this application. Grant it read/write access to the development database; do not reuse an Atlas account password or a production application user.
3. In Network Access, add your current public IP address so the local development server can connect. Add the deployment platform's outbound address separately for production. Avoid `0.0.0.0/0` unless it is a short-lived troubleshooting measure and you understand the exposure.
4. Open the cluster's Connect flow, choose Drivers and Node.js, and copy the SRV connection string.
5. Add the application database name to the URI and save it as `MONGODB_URI` in `.env.local`:

   ```env
   MONGODB_URI=mongodb+srv://<db-user>:<url-encoded-password>@<cluster-host>/epoch-development?retryWrites=true&w=majority
   ```

   Replace every placeholder. If the password contains reserved URI characters such as `@`, `:`, `/`, or `%`, URL-encode the password before placing it in the URI.

6. Start the application with `npm run dev`. A successful connection followed by an admin create, update, or delete verifies that both ordinary database access and transactional audit logging work.

Use a separate development database such as `epoch-development`. Never point local tests or media-maintenance commands at the production database unintentionally. Atlas database users are separate from the users who sign in to the Atlas website.

For current Atlas UI and connection details, see MongoDB's guides for [creating and connecting to a cluster](https://www.mongodb.com/docs/atlas/create-connect-deployments/) and [connecting with a driver](https://www.mongodb.com/docs/atlas/driver-connection/).

## Application map

| Path | Responsibility |
| --- | --- |
| `app/blog/`, `app/projects/`, `app/events/`, `app/gallery/` | Public content pages |
| `app/team/` | Current team, archives, requests, and share cards |
| `app/auth/`, `app/profile/`, `app/my-rsvps/` | Authentication and member experiences |
| `app/admin/` | Admin workspace and content management UI |
| `app/api/` | Content, account, RSVP, admin, upload, and utility handlers |
| `components/admin-shell.tsx` | Admin navigation and responsive shell |
| `lib/mongodb.ts` | Cached Mongoose connection |
| `lib/auth.ts` | NextAuth providers and role/session callbacks |
| `lib/audit-log.ts` | Atomic audit transaction wrapper and safe change summaries |
| `lib/media-assets.ts` | Managed-image registration, reference checks, and cleanup processing |
| `lib/event-dates.ts` | Legacy event correction and explicit IST formatting |
| `lib/ticket-generator.ts` | PDF event-ticket generation |

The `@/*` TypeScript alias resolves from the repository root.

## Authentication and authorization

- Admin pages use `AdminGuard`, but UI protection is not sufficient. Preserve authorization checks inside every protected route handler.
- Middleware covers `/api/admin/:path*` and `/api/rsvp/:path*`; content mutation handlers still perform their own admin checks.
- Sessions use JWTs, but role data is reread from MongoDB so role changes take effect without waiting for a new sign-in.
- Member-owned endpoints must derive identity and email from the server session, never from submitted request fields.

When changing access control, manually check signed-out, ordinary-member, and administrator behavior.

## Audit logging

- Successful administrator creates, updates, and deletes are written with their domain changes through `runAuditedMutation`.
- The domain write and audit entry share one MongoDB transaction, which is why a replica set is required.
- Logs start recording only after this feature is deployed; historical actions are not backfilled.
- Logs expire six calendar months after creation. The read API hides expired entries immediately, while MongoDB's TTL process removes them asynchronously.
- Audit data is allowlisted. Do not copy passwords, tokens, contact-message bodies, QR contents, or other sensitive payloads into logs.
- Large blog bodies and gallery image lists should remain summarized rather than duplicated into audit records.

The admin log viewer is available at `/admin/logs`.

## Cloudinary image lifecycle

New uploads are recorded in `MediaAsset`. Content creates attach those records, while replacements, removals, and entity deletions create durable `MediaCleanupJob` entries inside the same transaction as the content change. Cloudinary deletion happens only after the MongoDB transaction commits.

Before deleting an asset, cleanup checks blogs, projects, events, galleries, team profiles and requests, user images, and Cloudinary URLs embedded in blog content. If anything still references the asset, deletion is cancelled. External URLs, another Cloudinary account, and assets outside managed Epoch folders are ignored.

New uploads use these folders:

| Purpose | Folder |
| --- | --- |
| Blog | `epoch/blogs` |
| Project | `epoch/projects` |
| Event | `epoch/events` |
| Gallery | `epoch/gallery` |
| Team | `epoch/team` |

Existing assets in `epoch-blogs` and `epoch-team` are not moved, so previously published links continue to work.

### Manual cleanup

Retry failed cleanup jobs and delete tracked uploads that were never attached to saved content and are older than 24 hours:

```bash
npm run media:cleanup
```

Scan managed legacy and current folders for existing orphan candidates:

```bash
npm run media:orphans
```

That command is a dry run. Review every candidate before applying deletion:

```bash
npm run media:orphans -- --apply
```

The apply command is destructive. It repeats the database reference check, but you should still verify that the environment points to the intended MongoDB database and Cloudinary account. Draft or unpublished content is still a valid database reference and is not considered orphaned.

Deleted asset records and completed or cancelled cleanup jobs expire after 30 days. Attached assets and unresolved jobs remain available for reference protection and manual retry.

## Events, tickets, and dates

- Event times are stored as UTC instants and displayed in `Asia/Kolkata` through `lib/event-dates.ts`.
- Legacy events have a one-time response correction until they are edited. Do not apply an additional browser-local offset.
- An RSVP is unique per event/user, and capacity slots have a per-event unique index to protect against concurrent overbooking.
- Ticket PDFs use the tracked Inter files in `fonts/`.
- Keep `pdfkit` in `serverExternalPackages` in `next.config.mjs`; bundling it breaks runtime font metrics and color-profile paths.

## Team-directory rules

- Academic-year groups and appointments are year-specific.
- Only published appointments belonging to published years can appear publicly.
- One person can have at most one appointment per academic year.
- The current year must be changed before it can be unpublished.
- Members must be moved before a populated hierarchy group is removed.
- Team approval and admin changes are transactional and therefore also require the MongoDB replica set.

## API and UI conventions

- Connect through `connectDB()` and validate request data with the shared Zod schemas where applicable.
- Public list response shapes are not uniform: blogs return `{ blogs, pagination }`, while projects, events, and galleries return arrays.
- Server components commonly fetch this application's API using `NEXTAUTH_URL` and `cache: "no-store"`.
- Keep database code and credentials in server modules. Add `"use client"` only where browser APIs, state, effects, or client session hooks require it.
- Reuse components in `components/ui/`, Tailwind theme tokens, and the `@/` import alias.
- Event date formatting must remain timezone-explicit.
- Several source files contain large commented-out older implementations. Confirm which code is active before editing.

## Verification

Run all automated tests:

```bash
node --test scripts/*.test.cjs
```

Run strict TypeScript checking separately:

```bash
npx tsc --noEmit --incremental false
```

Build the production application:

```bash
npm run build
```

The production build skips ESLint but performs Next.js framework type validation. Keep the standalone TypeScript command in the workflow because it is an explicit, fast check independent of the build. `npm run lint` is not currently a ready-to-run unattended check because the repository has no ESLint configuration or direct ESLint dependency.

For UI changes, also inspect responsive layouts, light/dark themes, loading and empty states, and relevant keyboard behavior. For authorization changes, test every supported role.

## Deployment checklist

- Configure all production secrets in the hosting platform; never commit `.env.local`.
- Use a MongoDB Atlas cluster, restrict its network access to trusted application addresses, and verify the application database user can read, write, and create the required indexes.
- Set `NEXTAUTH_URL` to the public origin and configure the matching Google callback URL.
- Configure the three Cloudinary variables before enabling uploads.
- Run the tests, standalone type check, and production build.
- Verify admin access with a real account whose stored role is `admin`.
- Run the orphan scanner in dry-run mode before any cleanup against production.
- Remember that there is no scheduled media cleanup; run `npm run media:cleanup` manually when required.

## Things to remember

- Never commit secrets, production exports, generated tickets, or personal contact/member data.
- Do not remove handler-level authorization because a page guard or middleware also exists.
- Do not move or rename existing Cloudinary assets as part of cleanup; doing so changes delivery URLs.
- Do not delete an image merely because it is unpublished. Only an asset with no database reference is orphaned.
- Do not put Cloudinary calls inside MongoDB transactions. Queue the cleanup and perform it after commit.
- Keep audit entries small, allowlisted, and free of sensitive content.
- Keep both lockfiles synchronized after dependency changes.
- Preserve the event timezone and PDFKit configuration noted above.
