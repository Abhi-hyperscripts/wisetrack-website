"""Generate per-module 'Custom build' service pages.

Positioning: WiseTrack has already shipped each of these systems
inside Ragenaizer. When a client wants a *custom* build of one of
them, WiseTrack is the team that's been there. Ragenaizer becomes
proof-of-capability, not the offer.

Each page lives at build-<slug>.html and follows the same template.

Run from repo root:  python3 scripts/build_services.py
"""
from __future__ import annotations
import html, pathlib, textwrap

ROOT = pathlib.Path(__file__).resolve().parent.parent


# --------------------------------------------------------------------------- #
# Content — one entry per module
# --------------------------------------------------------------------------- #
SERVICES = [
    {
        "slug": "hrms",
        "code": "01",
        "module": "HRMS",
        "tagline": "Custom HRMS, built by people who've shipped one in production.",
        "italic": "production",
        "blurb": "We've already built a multi-country HRMS with transparent payroll, geofenced attendance, and a country-agnostic statutory engine — it ships inside Ragenaizer. If your team needs a custom HRMS instead, the hard problems are already solved.",
        "ragenaizer_url": "https://ragenaizer.com/pages/hrms.html",
        "capabilities": [
            ("Transparent payroll", "Every payslip line traceable back to its formula, inputs, and values. Audit-ready by default."),
            ("Country-agnostic engine", "Statutory rules (PF, ESI, PT, TDS, social security, regional tax) driven by JSON configs, not hard-coded. Adding a new country is a config change, not a rewrite."),
            ("Geofenced attendance", "GPS + NFC + selfie verification. Regularisation workflow with approval chain. Overtime + shift handling."),
            ("Salary structure versioning", "Mid-period revisions, retroactive corrections, and statutory ceiling changes handled in the same payroll run."),
            ("Bank file generation", "NEFT / RTGS / ACH / wire formats. Direct to bank or via approval queue."),
            ("Self-service portal", "Payslips, leave applications, expense claims, document requests. Mobile-first."),
            ("Compliance pack", "GST, TDS, PF, ESI return generation. Country-specific (India today; UK / UAE / US patterns ready)."),
            ("Payroll → finance bridge", "Payroll runs post journal entries straight into Accounts. No CSV round-tripping."),
        ],
        "hard_problems": [
            "Time-zone-correct attendance across a workforce distributed across regions, including DST edges.",
            "Retroactive salary revisions inside a closed period — without breaking statutory filings or audit trails.",
            "Per-component proration when an employee transfers mid-month between locations / cost centres / pay scales.",
            "Multi-currency CTC with home-currency payslip generation and accurate FX accounting on settlement.",
            "Statutory ceiling changes mid-year (the kind of thing the government does in March), applied without forcing a re-run on every closed period.",
        ],
        "stack": "ASP.NET Core services, Postgres, an event-sourced ledger for payroll, separate read models for reporting. Single tenant or multi-tenant, your call. Deploys on Docker / Linux.",
    },
    {
        "slug": "crm",
        "code": "02",
        "module": "CRM",
        "tagline": "Custom CRM, with the integrations you actually need.",
        "italic": "actually",
        "blurb": "We've built and shipped a sales CRM with a visual pipeline, multi-channel lead capture, Facebook Lead Ads integration, and a shared customer record across finance and operations. If you want yours instead of Salesforce — these are the gears.",
        "ragenaizer_url": "https://ragenaizer.com/pages/crm.html",
        "capabilities": [
            ("Visual pipeline", "Drag-to-stage Kanban. Per-pipeline stages, win/loss reasons, deal velocity, weighted forecasts."),
            ("Universal lead capture", "Webhook ingestion from any web form. Native connectors for Facebook Lead Ads and Google Ads."),
            ("AI lead enrichment", "Automatic enrichment from public profiles + scoring. Workable without becoming creepy."),
            ("Activities & tasks", "Threads on every deal. Reminders, follow-up cadences, owner reassignment."),
            ("Shared customer record", "One record across CRM, billing, projects. No duplicate-customer rabbit hole."),
            ("Conversion to deal / project / invoice", "Won deals can spawn projects, contracts, invoices — auto-numbered, owner-assigned, audit-trailed."),
            ("Reporting", "Pipeline health, conversion by stage, win rate by source, by rep, by segment. Embedded dashboards."),
            ("Email + WhatsApp threads", "Conversation history attached to the deal, not the rep."),
        ],
        "hard_problems": [
            "Deduplication when leads arrive from 4 channels in the same hour — same person, different casing, missing fields.",
            "Pipeline-state machine that allows custom stages per pipeline without losing reporting consistency.",
            "Permission model: a sales lead who can see their team but not their peers; a manager who can see all of one BU; an exec who sees aggregates only.",
            "Multi-currency forecasts with FX as of report-run time, not deal-creation time.",
            "Cross-module live data — when a deal's contract is signed, that customer record should appear in Accounts the same second.",
        ],
        "stack": "ASP.NET Core, Postgres with row-level security for tenant + role isolation, Redis for queue + cache, webhooks via a thin gateway service. Frontend in Blazor or your stack of choice.",
    },
    {
        "slug": "pms",
        "code": "03",
        "module": "PMS",
        "tagline": "Custom project &amp; issue tracking, with the seriousness of an engineering tracker.",
        "italic": "engineering",
        "blurb": "We've shipped a project management system that's also an honest engineering bug tracker — Bug / Feature / Task / Regression issue types, severity, priority, SLA stats, threaded comments, watchers, time-tracking, billing. If you want yours instead of Jira-plus-five-tools, here's what it takes.",
        "ragenaizer_url": "https://ragenaizer.com/pages/pms.html",
        "capabilities": [
            ("Project + issues, one system", "Projects with auto-numbered issue keys (PRJ-1234), threaded comments, attachments, status workflows."),
            ("Engineering-grade issues", "Bug / Feature / Task / Regression types. Severity, priority, reproducibility, environment, fixed-in-version."),
            ("SLA tracking", "Per-priority SLA timers. Breach alerts. Average resolution stats by type / owner / project."),
            ("Time tracking + timesheets", "Daily logs, weekly approval, per-member billing rates. Roll up to client invoices."),
            ("Kanban + Sprints", "Drag-to-status boards, sprint planning, burn-down. Configurable workflows."),
            ("Linked items", "Mark-as-duplicate, relates-to, blocks, blocked-by. Walk the graph in reports."),
            ("Watchers & subscriptions", "Granular notification rules per issue and per project."),
            ("Project meeting rooms", "Auto-created video rooms per project — no calendar dance."),
        ],
        "hard_problems": [
            "Permission model that handles client visibility (\"clients can see their tickets, not other clients'\") without making the staff UI miserable.",
            "Cross-project issue linking when projects live in different tenants of the same multi-tenant install.",
            "Time-tracking integrity — a developer's accidental 47-hour day should be caught and corrected without destroying their week.",
            "Workflow customisation per project without forking the data model.",
            "Roll-up reporting across hundreds of projects without query-of-doom dashboards.",
        ],
        "stack": "ASP.NET Core, Postgres, MeiliSearch / OpenSearch for issue search, a worker queue for notifications and SLA breaches. Optional Slack / Teams bridges.",
    },
    {
        "slug": "vision",
        "code": "04",
        "module": "Vision · video conferencing",
        "tagline": "Custom video conferencing, with the WebRTC engineering already understood.",
        "italic": "WebRTC",
        "blurb": "We've shipped a working HD video conferencing system — hosted meeting lobby, live captions, AI transcription, auto-recording to cloud storage, guest access. If you want a custom video product instead of paying per-seat for Zoom or Meet, here's how it's actually built.",
        "ragenaizer_url": "https://ragenaizer.com/pages/vision.html",
        "capabilities": [
            ("HD multi-party calls", "100+ participants, adaptive bitrate, network-aware quality. Selective Forwarding Unit (SFU) topology, not full-mesh."),
            ("Hosted meeting lobby", "Knock-to-enter with admit / reject. Per-meeting allowlists. Three modes: open, hosted, allowlist."),
            ("Live captions", "Real-time speech-to-text. Multilingual with code-switching for India English."),
            ("AI summaries + transcripts", "Auto-transcript with speaker diarisation. Post-meeting summary, action items, topic timeline."),
            ("Auto-record to Drive", "Server-side recording, post-processing, attached to the meeting record."),
            ("Guest access", "Browser-only join — no account, no app install. Sensible for enterprise clients."),
            ("Chat + reactions + screenshare", "Sidebar chat, emoji reactions, single + multi-screen share."),
            ("Per-room ops", "Mute-all, lock room, remove participant, host transfer."),
        ],
        "hard_problems": [
            "Signalling at scale — WebRTC peers join and leave constantly; the signal layer has to be horizontally scalable.",
            "Media routing — SFU clustering for big rooms, simulcast layers, bandwidth back-off when networks degrade.",
            "Recording pipeline — server-side composer, post-process, transcode, cold-store. Without dropping any of the streams.",
            "Captioning latency — sub-second is the bar, and the model needs to handle Indian accents and code-switching.",
            "Auth that works for both authenticated users AND guests, with the same media plane.",
        ],
        "stack": "LiveKit (open-source WebRTC SFU) or mediasoup; ASP.NET Core signalling; Postgres for room state; Redis for presence; a recording worker pool; an STT pipeline (Whisper / Deepgram). All on Linux containers.",
    },
    {
        "slug": "drive",
        "code": "05",
        "module": "Drive · cloud storage",
        "tagline": "Custom cloud storage, with the upload engineering already solved.",
        "italic": "upload",
        "blurb": "We've shipped a cloud-storage product with 5GB resumable chunked uploads, password-protected shares, revocable links, full audit logging, and S3 / Wasabi compatible backends. If you want a custom Drive — for compliance, sovereignty, or pricing reasons — these are the moving parts.",
        "ragenaizer_url": "https://ragenaizer.com/pages/drive.html",
        "capabilities": [
            ("Resumable chunked upload", "Multipart + chunk-resume so a 5GB file survives a flaky network. Network drops, you resume from the last chunk."),
            ("Encrypted at rest", "AES-256 server-side; envelope encryption with per-tenant keys. Hardware-backed KMS where available."),
            ("Revocable links", "Share, set expiry, set download cap, set password. Revoke or rotate after issuing — no need to delete the file."),
            ("Audit trail", "Who viewed, who downloaded, when, from which IP. Exportable. Required for HIPAA / SOC2 / DPDP audits."),
            ("Versioning", "Roll back to any prior version. Configurable retention windows."),
            ("S3 / Wasabi / MinIO compatible", "Bring-your-own object store. No vendor lock-in on the data plane."),
            ("Presigned URLs", "Direct browser-to-bucket uploads so files never traverse your application server."),
            ("Granular ACLs", "Per-file, per-folder, per-group. Inheritance with explicit overrides."),
        ],
        "hard_problems": [
            "Resumable upload protocol — the client side needs idempotent chunk identifiers, the server needs to garbage-collect orphaned chunks.",
            "Multi-tenant key management — each tenant's data encrypted with their own key, key material never crosses tenant boundaries.",
            "Quota accounting in near-real-time across hundreds of thousands of files per tenant.",
            "Antivirus / DLP on upload without blocking the user — async scanning with quarantine on bad hits.",
            "Cold-storage tiering when files haven't been accessed in 90+ days — without breaking share links.",
        ],
        "stack": "ASP.NET Core for the control plane, S3-compatible object storage for the data plane (Wasabi / MinIO / Backblaze B2 are all fine), Postgres for metadata, Redis for presigned URL minting. Optional virus-scan worker.",
    },
    {
        "slug": "accounts",
        "code": "06",
        "module": "Accounts · accounting",
        "tagline": "Custom accounting software, audit-ready by default.",
        "italic": "audit-ready",
        "blurb": "We've shipped a double-entry accounting system with multi-currency, bank reconciliation, GST returns, fixed-asset depreciation, subscriptions, period close. If your business is large enough that QuickBooks / Tally / Zoho start hurting, here's what the custom build actually involves.",
        "ragenaizer_url": "https://ragenaizer.com/pages/accounts.html",
        "capabilities": [
            ("Double-entry ledger", "Journal-first design — every transaction is balanced by construction. Reports derive from journals, never the other way around."),
            ("Multi-currency", "Transactions in any currency. FX rates at transaction time, FX revaluation at period close. Realised + unrealised gain/loss handled cleanly."),
            ("Bank reconciliation", "Statement import, auto-match, fuzzy match for slight differences, manual override with audit trail."),
            ("AR + AP", "Invoices, recurring invoices, credit notes, vendor bills, purchase orders, AR / AP aging."),
            ("Tax engine", "GST + TDS for India out of the box. Returns generation (GSTR-1, GSTR-3B). Extensible for other jurisdictions."),
            ("Fixed assets", "Depreciation methods (straight-line / WDV / units-of-production), batch run, disposal, gain/loss postings."),
            ("Subscriptions / recurring billing", "Plans, trials, metered usage, dunning. Webhooks from Stripe / Razorpay auto-post."),
            ("Period close & audit lock", "Soft close, hard close, year-end close with check-lists. Reopen-with-reason if you must."),
        ],
        "hard_problems": [
            "Audit trail that survives schema migrations — five years from now, the journal entry needs to be readable.",
            "Period locking that allows late adjustments via reversal-and-correction without rewriting history.",
            "Multi-entity / multi-book consolidation with intercompany eliminations.",
            "FX revaluation that posts correctly to realised / unrealised buckets at the right granularity.",
            "Number-sequence allocation in a multi-writer cluster without gaps — accountants notice.",
        ],
        "stack": "ASP.NET Core, Postgres (the relational integrity matters here — no NoSQL), a separate read-model service for reports, and a Hangfire / Quartz worker for end-of-period batch jobs. Audit log lives in an append-only event store.",
    },
    {
        "slug": "lms",
        "code": "07",
        "module": "LMS",
        "tagline": "Custom learning platforms — with live, self-paced, and verifiable.",
        "italic": "verifiable",
        "blurb": "We've shipped a learning management system with course builders, live training rooms, quizzes, certificates with public verification links, training rules, compliance reporting. If you need a custom LMS for your customers, your franchisees, your new hires — here are the moving parts.",
        "ragenaizer_url": "https://ragenaizer.com/pages/lms.html",
        "capabilities": [
            ("Course builder", "Modules, lessons, video, documents, SCORM-style content, prerequisites, gating."),
            ("Quizzes & assessments", "Multiple question types, randomisation, time limits, auto-grading + manual review."),
            ("Live training", "Sessions powered by the Vision module — attendance tracking, recordings auto-linked, transcripts."),
            ("Verifiable certificates", "Issued with a public verify-by-URL endpoint — recipients can prove completion outside the platform."),
            ("Learning paths", "Sequences across multiple courses with progression rules."),
            ("Training rules", "Auto-enrol new hires, role changes, compliance windows. The HR-grade automation most LMSes lack."),
            ("Discussions", "Per-course threads, mentions, instructor replies, moderation."),
            ("Analytics", "Per-learner, per-cohort, per-course. Pass rates, time-to-complete, drop-offs."),
        ],
        "hard_problems": [
            "Mixed-mode course delivery — live + self-paced + assignments — without making the UI a Christmas tree of buttons.",
            "Cohort vs. self-paced enrolment — same content, different progression models, same gradebook.",
            "Certificate verification that's tamper-evident without requiring a blockchain pitch deck.",
            "Compliance training reporting that an auditor can actually read.",
            "Scaling live sessions to 500+ attendees without losing chat or polls.",
        ],
        "stack": "ASP.NET Core, Postgres, S3 for content storage, a streaming layer for live (LiveKit), MeiliSearch / OpenSearch for course discovery. Notification worker for nudges.",
    },
    {
        "slug": "research",
        "code": "08",
        "module": "Research · analytics",
        "tagline": "Custom research and analytics platforms — survey to insights in minutes.",
        "italic": "minutes",
        "blurb": "We've shipped a market-research platform that runs cross-tabs, driver analysis, K-means segmentation, TURF, focus-group transcription, and auto-coding of open-ends — without anyone writing SPSS syntax. If you need yours, here's what's underneath.",
        "ragenaizer_url": "https://ragenaizer.com/pages/research.html",
        "capabilities": [
            ("Survey ingestion", "CSV / Excel / Decipher / Qualtrics imports. Variable mapping, label preservation, weighting."),
            ("Cross-tabs with significance", "Z-tests with letter notation, configurable confidence levels, weighted bases."),
            ("Driver analysis", "Multiple linear regression with shapley-style importance. Outputs publication-ready charts."),
            ("Segmentation", "K-means clustering with elbow / silhouette diagnostics, profiled segments."),
            ("TURF", "Reach / frequency portfolio optimisation across SKUs / features / message variants."),
            ("Open-end auto-coding", "LLM-assisted code-frame discovery, manual review, sentiment, theme tagging."),
            ("Focus-group transcription", "Speaker diarisation, time-coded transcript, theme extraction."),
            ("Embeddable dashboards", "Embed cross-tab + chart widgets in a client portal — under your domain, your branding."),
        ],
        "hard_problems": [
            "Statistical correctness — getting the Z-test to actually match what an SPSS user would expect, edge cases and all.",
            "Performance — cross-tabbing a 50K-row dataset with 200 banner variables in the time it takes to make tea.",
            "Open-end coding that's auditable — the LLM suggested this code, the analyst accepted / rejected, here's the diff.",
            "Multi-language survey responses with mixed scripts in the same column.",
            "Weighting + post-stratification that respects the survey design instead of pretending it's a simple random sample.",
        ],
        "stack": "ASP.NET Core for orchestration, Python workers (numpy / pandas / scikit-learn) for the heavy stats, Postgres for survey storage, ClickHouse for fast cross-tab queries on large datasets.",
    },
    {
        "slug": "email",
        "code": "09",
        "module": "Email · unified inbox",
        "tagline": "Custom unified inbox — bring your own provider, keep your data.",
        "italic": "your data",
        "blurb": "We've shipped a unified inbox that bridges Gmail / Outlook / Microsoft 365 / IMAP+SMTP, shows everything in one queue, supports shared team inboxes, and turns email threads into deals or tasks in one click. The data stays where you tell it to.",
        "ragenaizer_url": "https://ragenaizer.com/pages/email.html",
        "capabilities": [
            ("Multi-provider connect", "Gmail / Outlook OAuth, Microsoft 365 OAuth, generic IMAP+SMTP. Per-user multiple accounts."),
            ("Shared inboxes", "Sales@, support@, info@. Multi-assignee, internal notes, SLA timers, auto-responses."),
            ("Threading & search", "Conversation-level threading, full-text search across all connected mailboxes."),
            ("Turn email into work", "One click: thread → deal, thread → ticket, thread → task. Attached customer record."),
            ("Templates & snippets", "Per-team templates, variables, signatures."),
            ("Send-as", "Send as a shared inbox without exposing your personal address."),
            ("Filters & rules", "Inbox automations — labels, routing, auto-assign."),
            ("Self-host", "Optional on-prem deployment with bring-your-own SMTP — mail never leaves your infrastructure."),
        ],
        "hard_problems": [
            "OAuth flow + token refresh that survives Google's quarterly auth changes.",
            "IMAP sync at scale — hundreds of mailboxes, IDLE connections, partial-fetch logic, deduplication.",
            "Threading across providers — Gmail's conversation model, Outlook's, IMAP's RFC threading — all reconciled.",
            "Encrypted attachment storage with the same audit trail as the rest of the platform.",
            "Bounce / complaint feedback loop handling so you don't get your sender reputation tanked.",
        ],
        "stack": "ASP.NET Core, Postgres for metadata, S3-compatible storage for raw MIME, Redis for IDLE connection pool state, a worker fleet for sync. Optional SMTP relay (Postfix / Haraka) for self-host.",
    },
    {
        "slug": "chat",
        "code": "10",
        "module": "Chat · team messaging",
        "tagline": "Custom team chat — real-time, with unlimited history.",
        "italic": "unlimited",
        "blurb": "We've shipped a real-time team messaging system — direct + group + channels, file attachments, read receipts, presence, edits with audit, guest access. If you need yours without Slack pricing or retention limits, this is what it takes to build.",
        "ragenaizer_url": "https://ragenaizer.com/pages/chat.html",
        "capabilities": [
            ("Real-time over WebSocket", "Persistent connection per client, message fan-out via a pub/sub layer. Reconnect-and-catch-up logic baked in."),
            ("Channels, DMs, groups", "Public / private channels, multi-party DMs, threaded replies."),
            ("Unlimited history", "No 90-day deletion. Search across every message you've ever sent."),
            ("File attachments", "Auto-saved to Drive, with audit trail, with the same access controls."),
            ("Edits + deletes with audit", "Editable for a window, deletable, both leave audit-log entries."),
            ("Presence + receipts", "Online / Away / Busy / Offline, read-by receipts per channel."),
            ("Guest access", "Bring vendors / clients into a single channel without expanding their reach."),
            ("Video escalation", "Any chat → instant video call via Vision. No tool-switching."),
        ],
        "hard_problems": [
            "Fan-out at scale — a single message in a 10K-member channel needs to reach every connected client in &lt;200ms.",
            "Message ordering — multiple senders, multiple servers, monotonic ordering with conflict resolution.",
            "Search that handles emoji, code blocks, and 17 languages without tokenisation drama.",
            "Mobile push that arrives before the client opens the app, without draining batteries.",
            "GDPR / DPDP delete — a user requests deletion, every reference of theirs needs to actually go.",
        ],
        "stack": "ASP.NET Core + SignalR for WebSocket transport, Postgres for durable storage, Redis Pub/Sub for fan-out, MeiliSearch for full-text. Push via FCM / APNs.",
    },
]


# --------------------------------------------------------------------------- #
# Templates (nav + footer shared with the rest of the site)
# --------------------------------------------------------------------------- #
NAV = """\
<div class="fixed top-0 left-0 right-0 h-[2px] z-[80] origin-left scale-x-0 bg-gradient-to-r from-violet via-indigo to-cyan" data-progress></div>

<div class="fixed top-0 left-0 right-0 z-[70] bg-bg/85 backdrop-blur-xl border-b border-white/5">
  <div class="max-w-page mx-auto px-edge h-9 flex items-center justify-between text-[11px] mono tracking-wider text-muted">
    <div class="flex items-center gap-3"><span class="dot"></span><span class="hidden sm:inline">CAPABILITIES · CUSTOM BUILD</span><span class="sm:hidden">CAPABILITIES</span></div>
    <div class="flex items-center gap-5"><span class="hidden md:inline">Noida, IN</span><span data-clock>--:--:-- IST</span></div>
  </div>
</div>

<header class="fixed top-9 left-0 right-0 z-[60] bg-bg/55 backdrop-blur-2xl border-b border-white/5">
  <nav class="max-w-page mx-auto px-edge h-[80px] flex items-center justify-between">
    <a href="index.html" class="flex items-center gap-2.5"><span class="brand-wordmark text-[14px] md:text-[17px]">WISETRACK&nbsp;TECHNOLOGIES<span class="text-violet">.</span></span></a>
    <div class="hidden md:block">
      <div class="nav-links">
        <a href="solutions.html" class="is-active">Solutions</a>
        <a href="portfolio.html">Work</a>
        <a href="methodology.html">Method</a>
        <a href="insights.html">Journal</a>
        <a href="careers.html">Careers</a>
      </div>
    </div>
    <div class="flex items-center gap-3">
      <a href="contact.html" class="hidden sm:inline-flex magnetic btn-primary text-sm">Start a project <svg class="arr" width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3 7h8M7 3l4 4-4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
      <button class="md:hidden h-9 w-9 grid place-items-center rounded-full border border-white/10" data-menu-toggle aria-expanded="false"><span class="block w-4 h-[1.5px] bg-text mb-1"></span><span class="block w-4 h-[1.5px] bg-text"></span></button>
    </div>
  </nav>
  <div data-menu class="md:hidden hidden bg-bg border-t border-white/5 [&.open]:block">
    <div class="px-edge py-6 flex flex-col gap-4 text-lg">
      <a href="solutions.html" class="py-2 text-text">Solutions</a>
      <a href="portfolio.html" class="py-2">Work</a>
      <a href="methodology.html" class="py-2">Method</a>
      <a href="insights.html" class="py-2">Journal</a>
      <a href="careers.html" class="py-2">Careers</a>
      <a href="contact.html" class="btn-primary w-fit mt-2">Start a project</a>
    </div>
  </div>
</header>
"""

FOOTER = """\
<footer class="relative border-t border-white/5">
  <div class="max-w-page mx-auto px-edge pt-20 pb-10">
    <div class="grid grid-cols-12 gap-gutter">
<!-- WhatsApp footer strip -->
      <div class="col-span-12 mb-10">
        <div class="wa-strip">
          <div class="qr"><img src="assets/whatsapp_qr.png" alt="WhatsApp QR code for WiseTrack Technologies" /></div>
          <div class="copy">
            <div class="label">WHATSAPP · SALES &amp; SUPPORT</div>
            <div class="head">Quicker than email — <em>chat with us</em>.</div>
            <p>Scan the QR or tap the button to start a WhatsApp chat with our sales &amp; support team. We reply within working hours, IST.</p>
          </div>
          <a href="https://wa.me/919220474451" target="_blank" rel="noopener" class="cta">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19.05 4.91A10.09 10.09 0 0 0 11.93 2C6.5 2 2.07 6.43 2.07 11.85a9.81 9.81 0 0 0 1.41 5.06L2 22l5.25-1.37a9.93 9.93 0 0 0 4.68 1.19h.01c5.43 0 9.86-4.43 9.86-9.85a9.8 9.8 0 0 0-2.75-6.96Zm-7.12 15.16h-.01a8.16 8.16 0 0 1-4.16-1.14l-.3-.18-3.11.82.83-3.04-.2-.31a8.17 8.17 0 0 1-1.25-4.37c0-4.51 3.68-8.18 8.19-8.18a8.13 8.13 0 0 1 5.79 2.4 8.13 8.13 0 0 1 2.4 5.79c0 4.51-3.67 8.21-8.18 8.21Zm4.49-6.13c-.25-.12-1.47-.72-1.7-.81-.23-.08-.39-.12-.56.12-.16.25-.64.81-.78.97-.14.16-.29.18-.54.06-.25-.12-1.05-.39-1.99-1.23a7.5 7.5 0 0 1-1.38-1.72c-.14-.25-.02-.38.11-.5.11-.11.25-.29.37-.43.12-.14.16-.25.25-.41.08-.16.04-.31-.02-.43-.06-.12-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43h-.48a.93.93 0 0 0-.67.31c-.23.25-.88.86-.88 2.1 0 1.24.9 2.43 1.03 2.6.12.17 1.78 2.72 4.3 3.81.6.26 1.07.41 1.43.53.6.19 1.15.16 1.59.1.49-.07 1.47-.6 1.68-1.18.21-.58.21-1.08.15-1.18-.06-.1-.23-.16-.48-.28Z"/></svg>
            Chat on WhatsApp
          </a>
        </div>
      </div>
      <div class="col-span-12 lg:col-span-4">
        <a href="index.html" class="flex items-center gap-2.5"><span class="brand-wordmark text-[17px] md:text-[20px]">WISETRACK&nbsp;TECHNOLOGIES<span class="text-violet">.</span></span></a>
        <p class="mt-6 max-w-md text-text-2/80 leading-relaxed">Software company with two brands. <span class="text-text">HyperScripts</span> builds custom software. <span class="text-text">Ragenaizer</span> is our flagship product.</p>
        <div class="mt-6 flex items-center gap-3 text-muted text-sm"><span class="dot"></span><span>Open for new engagements · Q1–Q2 2026</span></div>
      </div>
      <div class="col-span-6 md:col-span-3 lg:col-span-2 lg:col-start-6"><div class="mono text-[11px] tracking-widest text-muted mb-5">EXPLORE</div><ul class="flex flex-col gap-3 text-text-2"><li><a href="solutions.html" class="hover:text-text">Solutions</a></li><li><a href="portfolio.html" class="hover:text-text">Work</a></li><li><a href="methodology.html" class="hover:text-text">Method</a></li><li><a href="insights.html" class="hover:text-text">Journal</a></li></ul></div>
      <div class="col-span-6 md:col-span-3 lg:col-span-2"><div class="mono text-[11px] tracking-widest text-muted mb-5">BRANDS</div><ul class="flex flex-col gap-3 text-text-2"><li><a href="https://hyperscripts.io/" target="_blank" rel="noopener" class="hover:text-text">HyperScripts</a></li><li><a href="https://ragenaizer.com/" target="_blank" rel="noopener" class="hover:text-text">Ragenaizer</a></li><li><a href="careers.html" class="hover:text-text">Careers</a></li><li><a href="client-portal.html" class="hover:text-text">Client portal</a></li></ul></div>
      <div class="col-span-6 md:col-span-3 lg:col-span-2"><div class="mono text-[11px] tracking-widest text-muted mb-5">LEGAL</div><ul class="flex flex-col gap-3 text-text-2"><li><a href="terms.html" class="hover:text-text">Terms</a></li><li><a href="privacy.html" class="hover:text-text">Privacy</a></li><li><a href="cookies.html" class="hover:text-text">Cookies</a></li></ul></div>
      <div class="col-span-12 md:col-span-6 lg:col-span-2"><div class="mono text-[11px] tracking-widest text-muted mb-5">FIELD NOTES</div><p class="text-text-2/85 mb-3">Occasional writing on engineering, products, and the work.</p><form class="flex items-center gap-2"><input type="email" placeholder="you@company.com" class="field flex-1"/><button class="btn-primary magnetic" type="submit"><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3 7h8M7 3l4 4-4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></button></form></div>
    </div>
    <div class="mt-16 pt-8 border-t border-white/5 flex flex-col md:flex-row gap-6 justify-between items-start md:items-center"><p class="mono text-[11px] text-muted tracking-widest">© 2026 WISETRACK TECHNOLOGIES · HARD SOFTWARE, BUILT SELECTIVELY</p><div class="flex gap-6 text-sm text-muted"><a href="privacy.html" class="hover:text-text">Privacy</a><a href="terms.html" class="hover:text-text">Terms</a><a href="cookies.html" class="hover:text-text">Cookies</a><a href="contact.html" class="hover:text-text">Contact</a></div></div>
  </div>
</footer>

<!-- WhatsApp chat FAB -->
<a href="https://wa.me/919220474451" target="_blank" rel="noopener" class="wa-fab" aria-label="Chat with WiseTrack on WhatsApp">
  <span class="wa-icon">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19.05 4.91A10.09 10.09 0 0 0 11.93 2C6.5 2 2.07 6.43 2.07 11.85a9.81 9.81 0 0 0 1.41 5.06L2 22l5.25-1.37a9.93 9.93 0 0 0 4.68 1.19h.01c5.43 0 9.86-4.43 9.86-9.85a9.8 9.8 0 0 0-2.75-6.96Zm-7.12 15.16h-.01a8.16 8.16 0 0 1-4.16-1.14l-.3-.18-3.11.82.83-3.04-.2-.31a8.17 8.17 0 0 1-1.25-4.37c0-4.51 3.68-8.18 8.19-8.18a8.13 8.13 0 0 1 5.79 2.4 8.13 8.13 0 0 1 2.4 5.79c0 4.51-3.67 8.21-8.18 8.21Zm4.49-6.13c-.25-.12-1.47-.72-1.7-.81-.23-.08-.39-.12-.56.12-.16.25-.64.81-.78.97-.14.16-.29.18-.54.06-.25-.12-1.05-.39-1.99-1.23a7.5 7.5 0 0 1-1.38-1.72c-.14-.25-.02-.38.11-.5.11-.11.25-.29.37-.43.12-.14.16-.25.25-.41.08-.16.04-.31-.02-.43-.06-.12-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43h-.48a.93.93 0 0 0-.67.31c-.23.25-.88.86-.88 2.1 0 1.24.9 2.43 1.03 2.6.12.17 1.78 2.72 4.3 3.81.6.26 1.07.41 1.43.53.6.19 1.15.16 1.59.1.49-.07 1.47-.6 1.68-1.18.21-.58.21-1.08.15-1.18-.06-.1-.23-.16-.48-.28Z"/></svg>
  </span>
  <span class="wa-label">Chat with us</span>
</a>
"""


TEMPLATE = """\
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<link rel="icon" type="image/png" href="assets/logo.png" />
<link rel="apple-touch-icon" href="assets/logo.png" />
<title>Custom {module_plain} · WiseTrack</title>
<meta name="description" content="{description}" />
<link rel="canonical" href="https://wisetrack.in/build-{slug}.html" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="WiseTrack" />
<meta property="og:title" content="Custom {module_plain} · WiseTrack" />
<meta property="og:description" content="{description}" />
<meta property="og:image" content="https://wisetrack.in/assets/og-image.jpg" />
<meta property="og:image:secure_url" content="https://wisetrack.in/assets/og-image.jpg" />
<meta property="og:image:type" content="image/jpeg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:url" content="https://wisetrack.in/build-{slug}.html" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Custom {module_plain} · WiseTrack" />
<meta name="twitter:description" content="{description}" />
<meta name="twitter:image" content="https://wisetrack.in/assets/og-image.jpg" />
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,300..900,30..100,0..1;1,9..144,300..900,30..100,0..1&family=Inter+Tight:wght@300..700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<script src="assets/tailwind-config.js"></script>
<link href="assets/styles.css" rel="stylesheet" />
<script>document.documentElement.classList.add("js")</script>
<script src="assets/site.js" defer></script>
</head>
<body class="bg-bg text-text font-sans antialiased overflow-x-hidden">

{nav}

<main class="relative pt-[120px]">

<!-- HERO -->
<section class="relative overflow-hidden">
  <div class="absolute inset-0 -z-0 pointer-events-none">
    <div class="aurora animate-drift" style="top:-30%; left:-10%; opacity:.4"></div>
    <div class="absolute inset-0 bp-grid"></div>
    <div class="absolute inset-0 bg-gradient-to-b from-transparent to-bg"></div>
    <div class="grain"></div>
  </div>

  <div class="relative max-w-page mx-auto px-edge pt-12 md:pt-16 pb-16">
    <div class="relative hud hud-cyan p-6 md:p-10 lg:p-14 border border-white/8 rounded-2xl bg-white/[0.015]">
      <div class="hidden md:block absolute top-3 left-6 mono text-[10px] tracking-widest text-muted">FILE&nbsp;·&nbsp;wisetrack.in/build-{slug}</div>
      <div class="hidden md:block absolute top-3 right-6 mono text-[10px] tracking-widest text-cyan flex items-center gap-2"><span class="h-1.5 w-1.5 rounded-full bg-cyan"></span>BUILD&nbsp;·&nbsp;{module_upper}</div>
      <div class="hidden md:block absolute bottom-3 left-6 mono text-[10px] tracking-widest text-muted">REF&nbsp;·&nbsp;RAGENAIZER</div>
      <div class="hidden md:block absolute bottom-3 right-6 mono text-[10px] tracking-widest text-muted">REV&nbsp;2026.05</div>

      <div class="grid grid-cols-12 gap-gutter mt-8">
        <div class="col-span-12 lg:col-span-8 reveal">
          <a href="solutions.html" class="inline-flex items-center gap-2 mono text-[11px] tracking-widest text-muted hover:text-text transition-colors">
            <svg width="12" height="12" viewBox="0 0 14 14" fill="none"><path d="M11 7H3M7 3L3 7l4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            BACK&nbsp;TO&nbsp;SOLUTIONS
          </a>
          <span class="slug block mt-6">§ {code} · CUSTOM&nbsp;{module_upper}</span>
          <h1 class="serif text-[clamp(2.2rem,5vw,4.6rem)] leading-[1] tracking-tight mt-4">
            {headline_html}
          </h1>
          <p class="mt-6 text-lg md:text-xl text-text-2/85 leading-relaxed max-w-prose">
            {blurb}
          </p>
          <div class="mt-8 flex flex-wrap gap-3">
            <a href="contact.html" class="btn-primary magnetic">Tell us about your build <svg class="arr" width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3 7h8M7 3l4 4-4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
            <a href="{ragenaizer_url}" target="_blank" rel="noopener" class="btn-ghost">See it shipped <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3 11L11 3M5 3h6v6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
          </div>
        </div>

        <div class="col-span-12 lg:col-span-4 reveal" data-delay="120">
          <div class="card p-6 hud hud-lime">
            <div class="mono text-[10px] tracking-widest text-muted">PROOF&nbsp;OF&nbsp;CAPABILITY</div>
            <div class="serif text-2xl mt-3 leading-tight">Ragenaizer · {module_short}</div>
            <p class="mt-3 text-sm text-text-2/85">A production-grade {module_lower} module already built and running. We ship a custom one for clients who need their own.</p>
            <a href="{ragenaizer_url}" target="_blank" rel="noopener" class="mt-4 inline-flex items-center gap-2 text-lime text-sm">
              ragenaizer.com / {module_lower}
              <svg width="12" height="12" viewBox="0 0 14 14" fill="none"><path d="M3 11L11 3M5 3h6v6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Capabilities -->
<section class="relative py-12 md:py-20">
  <div class="max-w-page mx-auto px-edge">
    <div class="grid grid-cols-12 gap-gutter mb-10">
      <div class="col-span-12 md:col-span-5 reveal">
        <span class="slug">§ Capabilities</span>
        <h2 class="serif text-[clamp(2rem,4vw,3rem)] leading-[1] tracking-tight mt-3">
          What goes inside a real <span class="serif-italic text-gradient">{module_lower}</span>.
        </h2>
      </div>
      <p class="col-span-12 md:col-span-6 md:col-start-7 self-end text-text-2/85 text-lg leading-relaxed reveal" data-delay="100">
        These are the moving parts we've shipped before. Your custom build picks a subset — and we tell you upfront which parts are worth re-implementing and which ones aren't.
      </p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-5">
{capability_cards}
    </div>
  </div>
</section>

<!-- Hard problems -->
<section class="relative bg-gradient-to-b from-transparent via-bg-2/40 to-transparent border-y border-white/5 py-16 md:py-24">
  <div class="max-w-page mx-auto px-edge">
    <div class="grid grid-cols-12 gap-gutter">
      <div class="col-span-12 md:col-span-5 reveal">
        <span class="slug">§ The hard bits</span>
        <h2 class="serif text-[clamp(2rem,4vw,3rem)] leading-[1] tracking-tight mt-3">
          The problems that <span class="serif-italic text-gradient-cool">don't</span> show up in the demo.
        </h2>
        <p class="mt-5 text-text-2/85 leading-relaxed">
          These are the ones that take a custom build from "works in a screenshot" to "works in production for three years." We've already learned them once.
        </p>
      </div>
      <div class="col-span-12 md:col-span-7 reveal" data-delay="120">
        <ol class="flex flex-col gap-5">
{hard_problems_list}
        </ol>
      </div>
    </div>
  </div>
</section>

<!-- Stack -->
<section class="relative py-16 md:py-24">
  <div class="max-w-page mx-auto px-edge">
    <div class="grid grid-cols-12 gap-gutter items-center">
      <div class="col-span-12 md:col-span-5 reveal">
        <span class="slug">§ Stack &amp; shape</span>
        <h2 class="serif text-[clamp(1.8rem,3.6vw,2.6rem)] leading-tight tracking-tight mt-3">
          How we'd put it together.
        </h2>
      </div>
      <div class="col-span-12 md:col-span-7 reveal" data-delay="100">
        <div class="card p-6 md:p-8 hud hud-cyan">
          <div class="mono text-[10px] tracking-widest text-muted">DEFAULT&nbsp;STACK&nbsp;·&nbsp;SUBSTITUTABLE</div>
          <p class="mt-4 text-text-2/90 leading-relaxed">{stack}</p>
          <div class="mt-6 flex flex-wrap gap-2">
            <span class="tag tag-violet">C# · .NET</span>
            <span class="tag tag-cyan">ASP.NET Core</span>
            <span class="tag tag-lime">Postgres</span>
            <span class="tag">Docker · Linux</span>
            <span class="tag tag-sky">gRPC where it earns its keep</span>
            <span class="tag">Multi-tenant by default</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- When build vs license -->
<section class="relative bg-gradient-to-b from-transparent via-bg-2/30 to-transparent border-y border-white/5 py-16 md:py-24">
  <div class="max-w-page mx-auto px-edge">
    <div class="grid grid-cols-12 gap-gutter mb-10">
      <div class="col-span-12 md:col-span-6 reveal">
        <span class="slug">§ Build vs. license</span>
        <h2 class="serif text-[clamp(2rem,4.2vw,3.4rem)] leading-[1] tracking-tight mt-3">
          We'll tell you when <span class="serif-italic text-gradient-warm">not</span> to build.
        </h2>
      </div>
      <p class="col-span-12 md:col-span-5 md:col-start-8 self-end text-text-2/85 text-lg leading-relaxed reveal" data-delay="100">
        Custom isn't always the right call. We've shipped Ragenaizer so we can say that honestly.
      </p>
    </div>
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
      <div class="card p-7 hud hud-cyan reveal">
        <div class="mono text-[10px] tracking-widest text-muted">BUILD&nbsp;CUSTOM&nbsp;WHEN</div>
        <ul class="mt-5 flex flex-col gap-3 text-text-2/90">
          <li class="flex gap-3"><span class="text-cyan">→</span><span>The {module_lower} <em>is</em> the moat — your competitor can't have the same one.</span></li>
          <li class="flex gap-3"><span class="text-cyan">→</span><span>You have compliance / sovereignty / data-residency requirements no SaaS will satisfy.</span></li>
          <li class="flex gap-3"><span class="text-cyan">→</span><span>You need to integrate at a level deeper than off-the-shelf vendors expose.</span></li>
          <li class="flex gap-3"><span class="text-cyan">→</span><span>Per-seat pricing across thousands of users makes the build cheaper inside 24 months.</span></li>
        </ul>
      </div>
      <div class="card p-7 hud hud-lime reveal" data-delay="120">
        <div class="mono text-[10px] tracking-widest text-muted">LICENSE&nbsp;RAGENAIZER&nbsp;INSTEAD&nbsp;WHEN</div>
        <ul class="mt-5 flex flex-col gap-3 text-text-2/90">
          <li class="flex gap-3"><span class="text-lime">→</span><span>The workflow is generic enough that a configurable platform will do.</span></li>
          <li class="flex gap-3"><span class="text-lime">→</span><span>You want it in weeks, not quarters.</span></li>
          <li class="flex gap-3"><span class="text-lime">→</span><span>You'd rather buy than own — let someone else maintain the {module_lower} forever.</span></li>
          <li class="flex gap-3"><span class="text-lime">→</span><span>Your engineering capacity should go to the parts of your product that no SaaS covers.</span></li>
        </ul>
        <a href="{ragenaizer_url}" target="_blank" rel="noopener" class="mt-6 inline-flex items-center gap-2 text-lime text-sm">
          Look at Ragenaizer first
          <svg width="12" height="12" viewBox="0 0 14 14" fill="none"><path d="M3 11L11 3M5 3h6v6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </a>
      </div>
    </div>
  </div>
</section>

<!-- CTA -->
<section class="relative py-16 md:py-24">
  <div class="max-w-page mx-auto px-edge">
    <div class="card p-10 md:p-16 relative overflow-hidden reveal">
      <div class="absolute -inset-1 pointer-events-none opacity-60"><div class="aurora animate-drift" style="left:-10%; top:-30%"></div></div>
      <div class="relative grid grid-cols-12 gap-gutter items-end">
        <div class="col-span-12 md:col-span-8">
          <span class="slug">§ Next step</span>
          <h2 class="serif text-[clamp(2rem,4.5vw,3.6rem)] leading-[1.02] tracking-tight mt-4">
            Custom {module_lower}? <span class="serif-italic text-gradient">Tell us what you need.</span>
          </h2>
          <p class="mt-5 max-w-prose text-text-2/85 text-lg">
            One conversation. We tell you whether it's a custom build, a Ragenaizer rollout, or something we shouldn't take on.
          </p>
        </div>
        <div class="col-span-12 md:col-span-4 md:text-right">
          <a href="contact.html" class="btn-primary magnetic w-fit">Start a project <svg class="arr" width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3 7h8M7 3l4 4-4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
        </div>
      </div>
    </div>
  </div>
</section>

</main>

{footer}

</body>
</html>
"""


def cap_card(idx: int, name: str, desc: str) -> str:
    accent = ["violet", "cyan", "lime", "sky"][idx % 4]
    return (
        f'      <div class="card p-6 hud hud-{accent} reveal" data-delay="{(idx % 4) * 60}">\n'
        f'        <div class="mono text-[10px] tracking-widest text-muted">/{idx+1:02d}</div>\n'
        f'        <h3 class="serif text-xl md:text-2xl mt-3 leading-tight">{name}</h3>\n'
        f'        <p class="mt-3 text-text-2/85 leading-relaxed">{desc}</p>\n'
        f'      </div>'
    )


def hard_item(idx: int, text: str) -> str:
    return (
        f'          <li class="flex gap-4">\n'
        f'            <span class="serif text-3xl text-gradient leading-none mt-1">{idx+1:02d}</span>\n'
        f'            <span class="text-text-2/90 leading-relaxed">{text}</span>\n'
        f'          </li>'
    )


def build(s: dict) -> str:
    module_plain = s["module"]
    module_short = module_plain.split(" · ")[0]
    module_upper = module_short.upper()
    module_lower = module_short.lower()
    italic = s["italic"]
    # Inject italic gradient on the chosen word in the tagline
    if italic in s["tagline"]:
        headline_html = s["tagline"].replace(
            italic, f'<span class="serif-italic text-gradient">{italic}</span>', 1
        )
    else:
        headline_html = s["tagline"]
    return TEMPLATE.format(
        slug=s["slug"],
        code=s["code"],
        module_plain=html.escape(module_plain),
        module_short=html.escape(module_short),
        module_upper=html.escape(module_upper),
        module_lower=html.escape(module_lower),
        headline_html=headline_html,
        blurb=html.escape(s["blurb"]),
        description=html.escape(s["blurb"]),
        ragenaizer_url=s["ragenaizer_url"],
        capability_cards="\n".join(cap_card(i, n, d) for i, (n, d) in enumerate(s["capabilities"])),
        hard_problems_list="\n".join(hard_item(i, t) for i, t in enumerate(s["hard_problems"])),
        stack=html.escape(s["stack"]),
        nav=NAV,
        footer=FOOTER,
    )


def main():
    for s in SERVICES:
        path = ROOT / f"build-{s['slug']}.html"
        path.write_text(build(s))
        print(f"wrote {path.name}")


if __name__ == "__main__":
    main()
