# Epoch administrator guide

This guide is for people who run the Epoch website. Use the admin workspace at `/admin` for public content, registrations, the Team directory, users, contact queries, QR codes, and activity logs. Use **Initiatives** from the signed-in avatar menu for private club work. Initiatives are separate from public Events and Projects.

## Quick navigation

| Goal | Where to go |
| --- | --- |
| Check site activity | **Admin → Overview** (`/admin`) |
| Publish writing or showcase work | **Admin → Content → Blogs / Projects / Gallery** |
| Create an event or review its registrations | **Admin → Events** (`/admin/events`) |
| Manage the public team roster | **Admin → People → Team** (`/admin/team`) |
| Review accounts and roles | **Admin → People → Users** (`/admin/users`) |
| Read contact submissions | **Admin → Inbox** (`/admin/queries`) |
| Review changes | **Admin → Tools → Logs** (`/admin/logs`) |
| Generate a QR code | **Admin → Tools → Utilities → QR Code Generator** |
| Coordinate a club initiative | Avatar menu → **Initiatives** (`/initiatives`) |

An administrator account is required for `/admin` and administrator actions. A normal signed-in account can use member features and collaborate only in initiatives to which it has been invited. The desktop sidebar groups Content, People, and Tools; on a narrow screen, open it with the navigation toggle.

The **Overview** page shows registered accounts, upcoming events and their registrations, published and draft blog counts, contact queries, and links to each content area. Its upcoming-registration figure counts registrations attached to upcoming events; it is different from the all-time RSVP total.

## Events and registrations

1. Open **Admin → Events → New Event**. Enter a title, description, date and time, and venue. You can also add an image, attendance limit, and RSVP deadline.
2. Save the event, then check its public page under `/events`. Use **Edit** in the Events list to correct details.
3. Use the event's **RSVPs** action to see attendees and export the list as CSV. Signed-in members register from the public event page and can download their own PDF ticket from their registrations.

The form displays event dates in India Standard Time. The application stores actual UTC instants and shows them in IST on event pages and tickets. An RSVP is accepted only while the event is in the future, before its optional deadline, and while an optional capacity has room. A user has at most one RSVP for an event. **Deleting an event also deletes its RSVP records**, so export anything needed first. An event's ticket QR is part of the ticket flow; it is not a QR created in Utilities and does not appear in the Utilities scan analytics.

## Blogs

1. Open **Content → Blogs → New Blog Post**. Enter a **title**, short **excerpt**, and **content**; all three are required. The content field supports Markdown.
2. Add optional tags and a featured image. Use the tag field's **Add** button or Enter to commit each tag before saving.
3. Select **Publish immediately** if the post is ready. The default is an unpublished draft, which does not appear as a public story.
4. Return to **Blogs** to search, open, edit, or delete a post. Use **Edit** to change its published state later. Check the result on `/blog`, and open its public detail page to review formatting and links.

The blog list distinguishes drafts and published posts. A blog detail URL uses a slug assigned when the post is created; editing its title does not automatically change that slug. Deleting a blog permanently removes the post; managed images no longer referenced elsewhere are queued for cleanup.

## Projects

1. Open **Content → Projects → New Project**. Enter a **title**, **description**, and at least one **Tech Stack** item. Add each technology with **Add** or Enter.
2. Optionally add a GitHub URL, live demo URL, and project image. Select **Featured Project** when the project should be highlighted where the site uses featured projects.
3. Save, then use **Projects** to search, open, edit, or delete it. Review its public page under `/projects`, including outbound links and the image.

Projects are public showcase records, separate from private Initiatives and public Events. They do not have an event RSVP flow. Deleting a project permanently removes it and queues cleanup for any unreferenced managed image.

## Gallery

1. Open **Content → Gallery → New Gallery**. Enter the **event name** and **event date**; a description is optional. A gallery is its own record and can be created without first creating a public Event.
2. Upload one or more photos by dropping files or choosing them. Add captions if useful. Select **Set as cover** on the photo that should represent the gallery on the public listing.
3. Save, then use **Gallery → Edit** to change details, captions, photos, or cover. Check `/gallery` and the gallery detail page. Visitors can open full images and browse with Previous/Next or keyboard arrows.

At least one valid image is required. The list shows galleries newest by event date. The selected cover must be one of that gallery's images; older galleries without an explicit cover use their first image. Changing the cover does not reorder the photos. If some uploads fail, successful uploads remain in the form and failed filenames are shown for retry. Deleting a gallery removes its record and queues cleanup for images no longer referenced elsewhere.

Content uploads accept JPEG, PNG, GIF, or WebP up to **4 MB per file**. Team photos accept JPG, PNG, or WebP up to 4 MB. Image uploads require the configured Cloudinary account; an image may upload before its content form is saved, so see [Image maintenance](#image-maintenance) for abandoned uploads.

## Team directory: adding members

The Team directory has three layers: an **academic year**, a reusable **person profile**, and that person's **appointment** in a year. A profile alone will not appear on `/team`.

1. In **People → Team → Academic years**, create the year and its ordered hierarchy groups, such as Executive Committee and Sub-Committee. **Copy hierarchy** starts a new unsaved year with the same headings.
2. In **People**, create or find the person's profile. Add their name, optional photo and career details. If they should edit their own shared profile later, set their private **Account email** to the email of their signed-in account.
3. In **Appointments**, select the existing profile, academic year, and hierarchy group. Add a position of responsibility (POR) if applicable; it can be blank. Publish the appointment when it is ready.
4. Publish the academic year and use **Make current** to select the year displayed by default on `/team`. Review the public directory. Published older years remain available in the archive.

Both the year **and** the appointment must be published for a person to appear publicly. One profile can have appointments in different years, but at most one per year. Profile details such as name, photo, current role, and organization are shared across years; the POR, group, order, and publication are year-specific. Move members to another group before removing a populated group. Switch to another current year before unpublishing the current one.

The **Requests** tab shows signed-in members asking to be listed. Review their submission, then approve or reject it with feedback. Approval links or creates a profile and adds the appointment. A linked member can later edit their shared profile from `/profile`; only admins can change appointments, hierarchy, or publication. Team profiles without a matching site account cannot be invited to an initiative until that person has an account.

## Users, contact inbox, and logs

- **Users** lists registered accounts. Search or filter by role, and change an account between User and Admin only when that person should have the corresponding access. `ADMIN_EMAILS` assigns the admin role when a *new* account is created; changing that environment setting does not change an existing account's stored role.
- **Inbox** shows contact form submissions newest first, 20 per page. The sender must be signed in to submit. The site stores the message for review; it does **not** send an email. You can permanently delete a query after confirmation.
- **Logs** lets admins search and filter recorded administrator changes and linked-member profile edits. Logs contain safe summaries, not full sensitive messages or QR contents. Recording starts when the logging feature is deployed; old actions are not backfilled. Entries are retained for six calendar months.

## QR codes: when tracking works

Open **Tools → Utilities → QR Code Generator**. Enter a name and either a URL or text, adjust the optional appearance settings, and create the code to save and download it. The preview updates before saving. If tracking is selected, its preview contains a **sample link**; distribute only the final downloaded code or tracked link after creation.

| QR content | Tracking available? | What scanning does |
| --- | --- | --- |
| `https://...` or `http://...` URL with tracking enabled | Yes | Opens an Epoch `/q/...` link, records a scan, then redirects to the saved URL. |
| HTTP(S) URL with tracking off | No | Opens the destination directly. |
| Plain text, email address, phone number, Wi-Fi data, or a non-HTTP(S) scheme | No | Shows or handles the encoded content without passing through Epoch. |
| A QR generated outside Utilities, including an event ticket QR | No Utilities analytics | It does not use that saved tracked redirect. |

Saved tracked codes show total scans and an **estimated** unique count in Analytics. The estimate uses a privacy-preserving fingerprint; raw IP addresses and user-agent strings are not stored. Analytics requires the Epoch redirect and database to be available. If analytics recording fails temporarily, the redirect is still attempted. The saved-code list shows the latest 100 codes. **Deleting a saved code permanently removes its scan aggregates and disables its tracked link**, so already printed tracked QR codes stop working. A direct, untracked QR cannot be converted into a tracked printed code after distribution; create and distribute a new tracked code.

## Initiatives: private coordination

Open **Initiatives** from your avatar menu. An admin creates an initiative with a name such as *UG1 Recruitment* or *Ganesh Chaturthi Event* and invites existing accounts. Participants can be selected individually or from an academic-year Team group; the group picker matches Team profiles to existing site accounts and reports profiles it cannot match. Initiatives do not create public Events, RSVPs, or Gallery entries.

The initiative list shows active work by default, with pending and overdue task counts and open questions. Use **Archive** to see completed initiatives. Inside each initiative:

- **To-Do:** Add tasks with a title, optional description, deadline, and multiple assignees. Click the circle on a task card to switch directly between **To do** and **Done**. Completed cards are gray and move to the bottom. Open a card for its full details and comments. Typing `@` in a comment offers initiative participants to mention. A task's creator or an admin can delete it; deletion also removes its comments.
- **Canvas:** Add shared notes, question boards, and image or link references. A question board asks one question, and suggestions stay as replies under it. Drag cards to organize them and resize them from their corner; positions and chosen dimensions persist. Legacy cards retain automatic height until resized. Cards can tag initiative participants. A card's creator or an admin can delete it.
- **Settings icon:** View or change participants, complete and archive the initiative, reopen it, or permanently delete it. Only admins can change participants, archive/reopen, or delete the entire initiative.

Archived initiatives are read-only until an admin reopens them. Initiative deletion is permanent and removes its tasks, comments, canvas cards, and question replies. Canvas images use the managed Cloudinary media workflow. There is no separate initiative chat; task discussions are comments, while question-board discussion stays with its question.

## Image maintenance

Managed images live in Cloudinary. When an admin replaces or removes an image or deletes content, the application queues a cleanup job and checks whether any other saved record still references that image before deleting it. Draft or unpublished content counts as a reference. New uploads that never become attached to saved content can be cleaned after 24 hours. **There is no scheduled cleanup**, so a maintainer must run the commands below when needed.

From the repository root, first confirm that `.env.local` or `.env` points to the intended MongoDB database and Cloudinary account:

```bash
npm run media:cleanup
```

This retries failed cleanup jobs and removes eligible unattached tracked uploads. To look for older or otherwise untracked orphan candidates in the managed Epoch folders, run a **read-only report**:

```bash
npm run media:orphans
```

Review the candidate list and its environment before applying it:

```bash
npm run media:orphans -- --apply
```

Apply mode can delete Cloudinary images. It repeats the database reference check before deletion, but a wrong environment or an image used outside this application's stored references still matters. The commands cover current `epoch/` media folders and the legacy `epoch-blogs/` and `epoch-team/` folders. They do not move legacy assets or act on another Cloudinary account. Attached assets and unresolved jobs remain recorded; resolved cleanup records expire after 30 days. See [dev.md](dev.md) for developer setup and the underlying media lifecycle.

## Things to remember

- Preview public content after saving, especially event times, Team publication, gallery cover photos, and QR destinations.
- Export data you need before deleting events, initiatives, contact queries, or tracked QR codes. These deletions are permanent in the product.
- Initiative membership is separate from an account's site-wide Admin/User role. Adding someone to Team does not automatically give them an Epoch account or initiative access.
- The admin and Team write paths use MongoDB transactions; the database must support transactions (for example, MongoDB Atlas). If a save fails, check the database connection before retrying.
- For technical setup, environment variables, and test commands, use [dev.md](dev.md). Never place real credentials or member data in this guide.
