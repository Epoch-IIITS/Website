# Epoch developer guide

This guide covers local development, verification, and the operational details that contributors should understand before changing the application. The website and its APIs are one Next.js application. Learn also has a separate Python execution service in `executor/`; Next.js still owns authentication, submissions, and database writes.

## Prerequisites

- A Node.js version compatible with Next.js 15. Node.js 20 LTS or newer is recommended; the repository does not currently pin a version.
- npm for the documented workflow.
- A MongoDB Atlas account and cluster. Atlas provides the replica-set deployment required by the application's transactions.
- A Cloudinary account when testing uploads or media cleanup.
- Google OAuth credentials when testing the Google sign-in flow. Development also includes a local email/password provider.
- Python 3.13 for rebuilding and validating all Learn question packs, with NumPy and pandas available in that Python environment. The app JSON generator itself uses only the Python standard library.
- Docker Engine or Docker Desktop when testing Learn's trusted executor. It is not needed for ordinary Next.js development or compatible browser-local Run actions.

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
| `LEARN_EXECUTOR_URL` | Learn Submit and fallback Run | Trusted `https://` origin of the separate executor, including a custom port if used. Next.js adds `/execute`. |
| `LEARN_EXECUTOR_TOKEN` | Learn Submit and fallback Run | Shared bearer token used only by the Next.js server and executor. |

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
| `app/initiatives/`, `app/api/initiatives/` | Private initiative workspaces and their authenticated API |
| `app/learn/`, `components/learn/`, `app/api/learn/` | Learn UI, authenticated submissions and progress APIs at `/learn` |
| `lib/learn/`, `models/LearnSubmission.ts` | Server-side curriculum, public payload split, executor client, and saved submissions |
| `executor/` | Separate VPS service for isolated Python execution and supplied tests |
| `app/api/` | Content, account, RSVP, admin, upload, and utility handlers |
| `components/admin-shell.tsx` | Admin navigation and responsive shell |
| `lib/mongodb.ts` | Cached Mongoose connection |
| `lib/auth.ts` | NextAuth providers and role/session callbacks |
| `lib/audit-log.ts` | Atomic audit transaction wrapper and safe change summaries |
| `lib/media-assets.ts` | Managed-image registration, reference checks, and cleanup processing |
| `lib/event-dates.ts` | Legacy event correction and explicit IST formatting |
| `lib/ticket-generator.ts` | PDF event-ticket generation |

The `@/*` TypeScript alias resolves from the repository root.

### Learn execution and progress

Learn uses the name and base route `/learn`. The source curriculum lives in `aimlgym/`; the app reads generated JSON files from `lib/learn/`. The current catalogue has 15 topics with 250 required problems, 41 optional deep dives and 31 project ideas, arranged as one path that starts from zero Python (Python → Mathematics → Statistics → NumPy → pandas → FastAPI → Machine Learning → Deep Learning → Computer Vision → NLP → LLMs → Explainable AI → Federated Learning → Reinforcement Learning → Agentic AI). The packs are authored content, not runtime configuration. `aimlgym/README.md` describes the pack layout and rebuild workflow, `aimlgym/curriculum.md` the learning sequence, `aimlgym/coverage-map.md` the prerequisite and coverage map, and `aimlgym/manifest.csv` lists every pack in path order.

For a full content rebuild, use two Python 3.13 virtual environments outside the published pack folders: one matching the executor image (`aimlgym/build/requirements-executor.txt`) and one with current versions of every library the packs use (`aimlgym/build/requirements-full.txt`), which catches version-specific behaviour. On Linux, install PyTorch from `https://download.pytorch.org/whl/cpu` first to avoid the CUDA wheels:

```bash
python3.13 -m venv ../epoch-learn-exec && ../epoch-learn-exec/bin/pip install -r aimlgym/build/requirements-executor.txt
python3.13 -m venv ../epoch-learn-full && ../epoch-learn-full/bin/pip install -r aimlgym/build/requirements-full.txt
```

#### Add or edit a question

1. Edit the step's dictionary in `aimlgym/build/topics/*.py` (each topic lists its modules in `aimlgym/build/path.py`). These modules are the authoring source; the six files in `aimlgym/topics/<topic>/<problem-slug>/` are rendered from them and overwritten by the builder.
2. For a new step, give it a globally unique slug and add the slug to the topic's list in `PATH` in `aimlgym/build/path.py` at the position where it should be learned. Do not write an ID: the builder numbers steps from `PATH`. Required fields: `slug`, `title`, `difficulty`, `prereqs` (slugs that come earlier in the path), `objectives`, `tags`, `packages`, `sources`, `entry`, `article` (starting with an H1, with a worked example and common mistakes), `statement`, `starter`, `hints` (exactly three), `solution`, `explanation`, `tests` (at least six), and `feedback` (pairs naming existing tests). Optional: `kind: "script"` for whole-program steps graded through stdin/stdout, and `library` (`text`, `tests`, `optional`) for a manual-versus-library comparison; comparisons for older packs live in `aimlgym/build/library_comparisons.py`. Refer to other steps as `[[slug]]`. Source IDs must exist in `aimlgym/sources.csv`.
3. The reference solution must pass every test and the starter must fail at least one. Put three short, self-contained visible cases first: `scripts/generate-learn-demo.py` publishes the first three `test_*` methods (at most 18 lines each) plus any test-module helpers they call. A pack runs in the browser only if its packages are ones Pyodide ships (NumPy, pandas, SciPy, scikit-learn, OpenCV) and its visible cases import only those and the standard-library modules the Pyodide harness allows (`LOCAL_PACKAGES` and `LOCAL_MODULES` in the generator); otherwise Run uses the executor.
4. Use only constructs and imports that earlier steps teach. `python3 aimlgym/build/audit.py` checks this against `FEATURE_INTRO`, `IMPORT_INTRO` and `LIBRARY_INTRO` in `path.py`, and also checks prerequisite order, cross-topic prerequisites and difficulty order.
5. Rebuild, validate and regenerate (from the repository root):

   ```bash
   python3 aimlgym/build/build.py
   ../epoch-learn-exec/bin/python aimlgym/build/validate.py --label executor-pins
   ../epoch-learn-full/bin/python aimlgym/build/validate.py --label full
   python3 aimlgym/build/audit.py
   python3 aimlgym/build/reports.py
   python3 scripts/generate-learn-demo.py
   ```

   `validate.py --only <topic-slug>` checks one topic during authoring without writing results; run both full validations before `reports.py`. Rerun one pack directly with `cd aimlgym/topics/<topic>/<slug> && python3 -B -m unittest tests -v` (prefix `AIMLGYM_TARGET=starter` to test the starter).

Library steps (for SciPy, scikit-learn, PyTorch, OpenCV, LangChain, LangGraph and Gymnasium) live in `aimlgym/build/topics/*_library.py`; each one is followed on the path by the from-scratch step it replaces, now an optional deep dive. Tests that train models use tiny seeded data, one thread and trend or tolerance checks so they pass in both validation environments; LLM and agent tests use LangChain's fake chat models. Register each library's first step in `IMPORT_INTRO`. Two other kinds of path entry share the same `PATH` lists. An **optional deep dive** is an ordinary step with `"optional": True`: it is graded as usual, shows an Optional badge, and is excluded from topic completion, progress bars and the problem counts. A **project idea** is a dictionary with `"kind": "project"` and the fields `slug`, `title`, `brief`, `uses` (slugs of earlier graded steps), `milestones` (four to six), `stretch`, `data` and `setup` (optionally `tags`). It is ungraded: the builder renders only `metadata.json` and `project.md`, numbers it separately (`PY-P1`, …) so graded IDs do not change, checks that every `uses` link is an earlier step, and validation and the audit skip it. The app lists it with a lightbulb after the step it follows, counts it as a project idea rather than a problem, and opens `/learn/projects/<slug>`, a reading page whose milestone ticks are stored only in the browser.

For a new topic, add its tuple to `TOPICS` and its step list to `PATH` in `aimlgym/build/path.py`, an introduction in `aimlgym/build/overviews.py`, and its modules under `aimlgym/build/topics/`. The app generator reads topics, order and outcomes from `path.py`, and catalogue counts are computed from the data; add the topic to a filter group in `components/learn/learn-catalogue.tsx`.

#### Rebuild the catalogue and grading data

The full pack build updates `aimlgym/topics/`, `aimlgym/build/results/`, `aimlgym/manifest.csv`, `aimlgym/coverage.md`, `aimlgym/coverage-map.md`, `aimlgym/curriculum.md`, `aimlgym/README.md` and the `supports` column of `aimlgym/sources.csv`. The app generator then writes these five JSON files:

| File | Used for |
| --- | --- |
| `lib/learn/catalogue.generated.json` | Topic, problem and project-idea summaries for `/learn` and topic pages. |
| `lib/learn/projects.generated.json` | Server-side project-idea pages (brief, linked steps, milestones, stretch goals, data and setup). |
| `lib/learn/packs.generated.json` | Server-side articles, statements, starter code, hints, visible snippets with the helper prelude they call, and worked solutions. |
| `lib/learn/local-compat.generated.json` | Static eligibility flags for browser-local Run. A local runtime failure still falls back to the executor. |
| `executor/tests.generated.json` | Full supplied test source for the executor; deploy this file to the VPS with the matching app release. |

Review and commit the changed source packs **and** generated files together. Keep `packs.generated.json` on the server side of the Next.js data flow. Never place `executor/tests.generated.json` in `public/` or return full tests to the browser. The problem page sends a public pack without the reference solution; the optional worked solution is fetched only when Reveal is pressed. A stale VPS test file can make grading results fail the app's expected test-count checks, so deploy app fixtures and executor tests as one content release.

#### Run, Submit, and saved progress

Monaco, KaTeX, Mermaid, and the Pyodide Web Worker load only on problem pages. Run checks the visible cases as local practice when a pack is eligible. For an eligible pack the Pyodide worker starts when the problem page opens and loads that pack's packages in the background (the editor header shows “Preparing Python…”); it stays alive across Runs, and each Run executes in a fresh namespace. A Run that takes longer than 45 s, or a worker error, replaces the worker and falls back to the executor. The worker maps `opencv-python-headless` to Pyodide's `opencv-python`, runs whole-program (`kind: "script"`) steps with each visible case's stdin, and executes the test-module helpers that the visible cases call. The harness also rebuilds each visible test's class with its `setUp` and helper methods (`localClasses` in the generated pack). Packs whose visible cases are not browser-compatible (for example PyTorch, FastAPI, LangChain, LangGraph or Gymnasium steps, or `asyncio.run`), and local runtime failures, fall back to the VPS executor when configured. Run never saves progress. Run on the executor (for problems that cannot run in the browser) and Submit both require a NextAuth session; signed-out learners see a sign-in note instead of a request being sent. Submit always uses the HTTPS executor for all supplied tests and returns the counts plus the names of any failed tests (never hidden test code); the workspace lists them with the matching advice from the pack's failure feedback. Next.js sends the executor an HMAC of the user id (keyed with `LEARN_EXECUTOR_TOKEN`), which the executor uses to allow each user 10 Runs and 5 Submits per minute with one request at a time; over the limit the routes return 429 with `Retry-After` and the workspace shows when to try again, and Submit saves nothing. If the executor is missing or unavailable, the app shows “Python execution is currently unavailable.” and records no submission.

Next.js writes trusted grading results to `LearnSubmission` under the session user ID. `/api/learn/submissions?slug=...` loads that user's latest saved code, `/api/learn/progress` and `/learn/progress` count distinct passed required problems (optional deep dives keep their solved marks but do not count), and `/api/learn/solution/[slug]` serves a worked solution when requested. The problem workspace has mouse-resizable learning/editor and editor/results splits. Its Run and Submit tooltips use the detected OS: Command plus apostrophe and Command plus Return on macOS, Control plus apostrophe and Control plus Enter on Windows/Linux. The learning UI shows a desktop-use notice on smaller screens.

#### Set up the executor for development or deployment

The current executor is **not Piston**. It is `executor/service.py`, which authenticates `POST /execute` and starts the Docker image built from `executor/Dockerfile` and `executor/runner.py`. The service reads `executor/tests.generated.json` locally; it has no MongoDB credentials or `/health` endpoint. The runner image installs every library the packs use, pinned in `executor/requirements.txt` and mirrored by `aimlgym/build/requirements-executor.txt`: NumPy 2.2.6, pandas 2.2.3, SciPy 1.14.1, scikit-learn 1.6.1, OpenCV headless 4.10.0.84, PyTorch 2.14.1 (CPU), FastAPI 0.162.0, httpx 0.28.1, LangChain Core 1.7.0, LangGraph 1.2.17 and Gymnasium 1.4.0. SciPy, scikit-learn and OpenCV match the versions Pyodide 0.27.7 ships. The service keeps two preloaded containers, runs at most two jobs and queues up to 30 requests (Submit first); see `executor/README.md` for the limits and the measurement script. To try the runner on a development machine, start Docker and run from the repository root:

```bash
docker info
docker build -t epoch-learn-runner:latest executor/
python3 -B -m unittest executor.test_service
node --test scripts/learn.test.cjs
```

To check a newly authored pack against the image's actual Python packages, change the slug below and send its reference solution and full tests into the container:

```bash
python3 - <<'PY' | docker run --rm -i epoch-learn-runner:latest
import json
from pathlib import Path

slug = "greeting-formatter"
pack = json.loads(Path("lib/learn/packs.generated.json").read_text())[slug]
tests = json.loads(Path("executor/tests.generated.json").read_text())[slug]
print(json.dumps({"mode": "submit", "code": pack["solution"], "tests": tests["tests"]}))
PY
```

The container first prints `READY` (its libraries are loaded), then one JSON line. Expect `"status": "passed"` and `passed == total == test_count` from that problem's metadata. The `full` validation environment uses newer NumPy/pandas and library versions than the image. Check package-sensitive questions in the Docker image before publishing, and update the image pins and rebuild it if a new pack requires different dependencies.

For a host-service smoke test, generate a token and start the loopback server in one terminal:

```bash
export LEARN_EXECUTOR_TOKEN="$(openssl rand -hex 32)"
python3 executor/service.py
```

From another terminal, `curl -i -X POST http://127.0.0.1:8765/execute` should return **401**, confirming the service is reachable and rejects requests without the token. The host process must be able to use Docker without `sudo`; `docker info` checks that access. This direct HTTP check is local to the machine. Next.js deliberately rejects an HTTP `LEARN_EXECUTOR_URL`, even on localhost, so end-to-end Run fallback and Submit need a trusted HTTPS frontend.

Set `LEARN_EXECUTOR_URL` to that HTTPS origin and `LEARN_EXECUTOR_TOKEN` to the same token used by the service in the **Next.js server** environment or `.env.local`, then restart Next.js. Never use a `NEXT_PUBLIC_` prefix. The [executor VPS guide](executor/README.md) gives the shared service setup and three HTTPS options: provider HTTPS proxy, private-IP machine through Tailscale Funnel, or shared public IP with a routed high port through DuckDNS and Caddy. It also documents systemd boot setup, certificate verification, firewall rules, and limits. After connecting it, sign in, Submit a known passing solution, and confirm `/learn/progress` updates only for that account.

## Authentication and authorization

- Admin pages use `AdminGuard`, but UI protection is not sufficient. Preserve authorization checks inside every protected route handler.
- Middleware covers `/api/admin/:path*` and `/api/rsvp/:path*`; content mutation handlers still perform their own admin checks.
- Sessions use JWTs, but role data is reread from MongoDB so role changes take effect without waiting for a new sign-in.
- Member-owned endpoints must derive identity and email from the server session, never from submitted request fields.
- Initiative workspaces are independent of public Events and Projects. Admins create, archive, and permanently delete them; invited accounts with a Team appointment in any year can collaborate. Admins bypass the Team membership requirement. The avatar menu uses the same historical Team membership lookup as the self-service profile editor, and every initiative API action checks that eligibility plus participant access. The participant picker can bulk add linked accounts from Team academic-year groups; Team profiles without matching accounts are shown as unavailable. The workspace shows To-Do beside Canvas on desktop, with tasks above the canvas on narrow screens. Tasks have comments with participant @mentions; the canvas holds notes, question boards, and references. Canvas card positions and optional dimensions persist through version checked updates.

When changing access control, manually check signed-out, ordinary-member, and administrator behavior.

## Audit logging

- Successful administrator creates, updates, and deletes, plus member-initiated updates to their linked team profile, are written with their domain changes through `runAuditedMutation`.
- The domain write and audit entry share one MongoDB transaction, which is why a replica set is required.
- Logs start recording only after this feature is deployed; historical actions are not backfilled.
- Logs expire six calendar months after creation. The read API hides expired entries immediately, while MongoDB's TTL process removes them asynchronously.
- Audit data is allowlisted. Do not copy passwords, tokens, contact-message bodies, QR contents, or other sensitive payloads into logs.
- Large blog bodies and gallery image lists should remain summarized rather than duplicated into audit records.

The admin-only log viewer is available at `/admin/logs`. Member profile entries use the signed-in member as the actor and include only changed public profile fields; the private account email and internal user link are excluded from change values.

## Cloudinary image lifecycle

Image uploads accept files up to 4 MB each. `lib/image-upload.ts` shares file validation between the forms and API handlers and handles upload responses without assuming errors are JSON. This leaves room for multipart overhead under the hosting request limit. Content images support JPEG, PNG, GIF, and WebP; team photos support JPG, PNG, and WebP, with validation before cropping and before sending the confirmed crop. Failed gallery uploads are listed by filename and reason; successful uploads are kept when retrying failed files. Run `node --test scripts/uploads.test.cjs` for upload validation, response handling, and API regression checks.

New uploads are recorded in `MediaAsset`. Content creates attach those records, while replacements, removals, and entity deletions create durable `MediaCleanupJob` entries inside the same transaction as the content change. Cloudinary deletion happens only after the MongoDB transaction commits.

Before deleting an asset, cleanup checks blogs, projects, events, initiative canvas references, galleries, team profiles and requests, user images, and Cloudinary URLs embedded in blog content. If anything still references the asset, deletion is cancelled. External URLs, another Cloudinary account, and assets outside managed Epoch folders are ignored.

New uploads use these folders:

| Purpose | Folder |
| --- | --- |
| Blog | `epoch/blogs` |
| Project | `epoch/projects` |
| Event | `epoch/events` |
| Gallery | `epoch/gallery` |
| Team | `epoch/team` |
| Initiative canvas | `epoch/initiatives` |

Existing assets in `epoch-blogs` and `epoch-team` are not moved, so previously published links continue to work.

Gallery records may store a `coverImage` URL selected from their own `images` array. Existing records without one use their first image. Changing the cover does not reorder event photos. Gallery list queries sort by `eventDate` descending, followed by creation time and ID for stable ordering.

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
- An approved listing request links the applicant's account email to one shared person profile. Linked members can edit that profile from `/profile`; academic years, groups, positions, order, and publication remain admin-managed.
- Older approved requests are resolved by user ID or normalized account email and acquire the direct account link on the member's first profile update. For manually created people, set the private Account email in the People editor to enable self-service editing.
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
- Deploy the matching Learn JSON fixtures and `executor/tests.generated.json`, expose the executor through trusted HTTPS, and set the server-only `LEARN_EXECUTOR_URL` and `LEARN_EXECUTOR_TOKEN`. Verify a signed-in Submit and per-user progress before opening Learn grading to users.
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
