"""Comprehensive SEO + AI-compatibility pass.

Idempotent — safe to re-run after content edits. Updates each HTML page so
search engines + LLM crawlers see consistent metadata.

What it does:
  1. Ensures every page has og:image:alt (defaults to canonical alt).
  2. Adds og:image:width/height + twitter:image to legal pages that lack them.
  3. Injects per-page Service JSON-LD for build-*.html + ai.html.
  4. Injects Blog/ItemList for insights.html, CollectionPage for portfolio.html,
     SoftwareApplication for dashboard.html, BreadcrumbList for index.html
     (and ai.html if missing).
  5. Adds an Organization "knowsAbout" boost on the AI page so LLMs index
     agentic capabilities correctly.
  6. Regenerates sitemap.xml with <lastmod> timestamps.
  7. Rewrites llms.txt with full inventory.
  8. Writes llms-full.txt — a richer, agent-grounding doc.

Run from repo root:  python3 scripts/seo_pass.py
"""
from __future__ import annotations
import pathlib, re, json, datetime as _dt

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://wisetrack.in"
TODAY = _dt.date.today().isoformat()
OG_IMG = f"{BASE}/assets/og-image.jpg"
OG_ALT = "WiseTrack Technologies — Software that needs real engineering."

# ───────── Page registry (single source of truth) ─────────
# Each entry: slug, title, summary, priority, changefreq
# "summary" is used for llms.txt + the description we synthesise where missing.
PAGES = [
    ("",                              "WiseTrack — Software that needs real engineering.",          "Custom applications, finance integrations, and Ragenaizer — a Business OS — plus production-grade agentic AI.", 1.00, "weekly"),
    ("solutions.html",                "Solutions — three ways we engage",                            "Three doors — custom build via HyperScripts, ready-made platforms, or licence Ragenaizer.", 0.92, "monthly"),
    ("ai.html",                       "AI & Agentic AI — engineered, not glued together",            "Production agent loops on Anthropic Claude — 90+ tools across 9 business modules, ClickHouse RAG, three-tier safety gates, full token + cost observability.", 0.95, "monthly"),
    ("portfolio.html",                "Work — selected engagements",                                  "Case studies: RBI (Burger King / Popeyes) QSR dashboard, Vivo Mobile, an elections counting platform feeding Hindustan Times / ABP / Times Internet / Google, Maldives resort ops, the Ragenaizer rollout.", 0.90, "monthly"),
    ("methodology.html",              "Method — how we run an engagement",                            "Four-phase process — listen, design, build (two-week demos), and stay around for what matters.", 0.80, "monthly"),
    ("insights.html",                 "Journal — field notes on engineering",                        "Writing on custom vs SaaS decisions, the cost of the wrong stack, agentic AI in production, the discipline of saying no.", 0.78, "weekly"),
    ("careers.html",                  "Careers — engineering hires",                                  "Open roles in engineering, platform, and design. A small team, deliberate hiring, work that ships.", 0.78, "weekly"),
    ("contact.html",                  "Contact — start a project",                                    "Tell us what you want to build. We reply within one working day.", 0.72, "monthly"),
    ("dashboard.html",                "Ragenaizer · live dashboard demo",                            "A live, interactive demo of a Ragenaizer dashboard — restaurant brands ops with revenue, orders, signal health.", 0.55, "monthly"),
    ("client-portal.html",            "Client portal",                                                "Sign-in for existing clients. Engagements, sprints, invoices, support.", 0.30, "yearly"),
    ("terms.html",                    "Terms & Conditions",                                           "Governing terms for use of wisetrack.in and our engagements.", 0.30, "yearly"),
    ("privacy.html",                  "Privacy Policy",                                               "How we handle data on wisetrack.in.", 0.30, "yearly"),
    ("cookies.html",                  "Cookie Policy",                                                "What cookies we set on wisetrack.in and why.", 0.30, "yearly"),
    # Blog posts
    ("post-when-to-build-when-to-buy.html","When to build, when to buy",                              "Decision framework for custom-vs-SaaS — five questions, one honest call.", 0.75, "monthly"),
    ("post-why-we-turn-down-half.html",   "Why we turn down half our projects",                       "Our five filters for inbound briefs — fit, urgency, technical interest, ownership, integrity.", 0.75, "monthly"),
    ("post-real-cost-of-wrong-stack.html","The real cost of the wrong stack",                         "Hiring risk, operational tax, observability cost — why default-to-.NET pays off in practice.", 0.75, "monthly"),
    ("post-one-app-vs-seven.html",        "One app vs. seven",                                        "A Ragenaizer rollout for a 200-person firm — replacing seven SaaS tools with a single platform.", 0.75, "monthly"),
    ("post-postgres-is-enough.html",      "Postgres is enough, until it isn't",                       "When to add a second data store, and when not to — engineering judgment, not cargo culting.", 0.75, "monthly"),
    ("post-two-week-demos.html",          "Two-week demos beat documents",                            "Why we replace long specs with demo-driven planning, and how that keeps engagements honest.", 0.75, "monthly"),
    # Build-* (custom-build service pages)
    ("build-hrms.html",     "Custom HRMS · multi-country payroll & attendance",                       "We've built a multi-country HRMS with transparent payroll, geofenced attendance, and a country-agnostic statutory engine. Custom build vs Ragenaizer license.", 0.85, "monthly"),
    ("build-crm.html",      "Custom CRM · pipeline & lead capture",                                   "We've shipped a sales CRM with visual pipeline, multi-channel capture, Facebook Lead Ads, and a shared customer record across finance and ops.", 0.85, "monthly"),
    ("build-pms.html",      "Custom PMS · projects + engineering bug tracker",                        "A project management system that's also an honest bug tracker — issue types, severity, SLA, time tracking, billing.", 0.85, "monthly"),
    ("build-vision.html",   "Custom video conferencing — meeting platform",                            "An HD video conferencing system — meeting lobby, live captions, AI transcription, auto-recording, guest access. Custom build vs Zoom/Meet.", 0.85, "monthly"),
    ("build-drive.html",    "Custom cloud Drive — file storage with audit",                            "A cloud storage product — 5GB resumable chunked uploads, password-protected shares, revocable links, audit logging, S3/Wasabi backends.", 0.85, "monthly"),
    ("build-accounts.html", "Custom accounting — double-entry, multi-currency, GST",                    "Double-entry accounting with multi-currency, bank reconciliation, GST returns, fixed-asset depreciation, subscriptions, period close.", 0.85, "monthly"),
    ("build-lms.html",      "Custom LMS · courses, live training, certificates",                       "Learning management with course builders, live training rooms, quizzes, public certificate verification, compliance reporting.", 0.85, "monthly"),
    ("build-research.html", "Custom research platform — cross-tabs, segmentation, FGD",                "Market research platform with cross-tabs, driver analysis, K-means segmentation, TURF, FGD transcription, auto-coding of open-ends.", 0.85, "monthly"),
    ("build-email.html",    "Custom unified inbox — Gmail/Outlook/IMAP bridge",                         "Unified inbox bridging Gmail / Outlook / Microsoft 365 / IMAP+SMTP. Shared team inboxes, email-to-deal/task in one click.", 0.85, "monthly"),
    ("build-chat.html",     "Custom team chat — real-time messaging",                                  "Real-time team messaging — direct + group + channels, attachments, read receipts, presence, audited edits, guest access.", 0.85, "monthly"),
]

# Build-* page → Service schema details
SERVICE_INFO = {
    "build-hrms.html":     ("Custom HRMS development",            "Human resources & payroll software",          "Multi-country HRMS, payroll, attendance, statutory engine"),
    "build-crm.html":      ("Custom CRM development",             "Sales & customer relationship software",      "Sales pipeline, lead capture, customer record"),
    "build-pms.html":      ("Custom PMS development",             "Project management software",                 "Project tracking, bug tracker, time tracking, billing"),
    "build-vision.html":   ("Custom video conferencing build",    "Video conferencing platform",                 "HD video, meeting lobby, transcription, recording"),
    "build-drive.html":    ("Custom cloud Drive build",           "Cloud storage platform",                       "File storage, sharing, audit logging, S3/Wasabi backends"),
    "build-accounts.html": ("Custom accounting software",         "Accounting & finance software",                "Double-entry, multi-currency, GST, depreciation, period close"),
    "build-lms.html":      ("Custom LMS development",             "Learning management software",                "Courses, live training, quizzes, certificates, compliance"),
    "build-research.html": ("Custom market-research platform",    "Market research & analytics platform",         "Cross-tabs, segmentation, TURF, FGD transcription, open-end coding"),
    "build-email.html":    ("Custom unified inbox build",         "Unified team inbox platform",                  "Gmail/Outlook bridge, shared inboxes, email-to-task"),
    "build-chat.html":     ("Custom team chat build",             "Real-time messaging platform",                 "Direct/group messaging, presence, attachments, audited edits"),
    "ai.html":             ("Agentic AI engineering",             "AI / LLM engineering services",                 "Custom agents, tool-use, RAG, multi-stage pipelines on Anthropic Claude"),
}

# ───────── Helpers ─────────

def upsert_meta_alt(text: str, alt: str) -> str:
    """Add og:image:alt + twitter:image:alt right after og:image:height if missing."""
    if 'og:image:alt' in text:
        return text
    # Insert after og:image:height OR after og:image
    repl = f'<meta property="og:image:alt" content="{alt}" />\n<meta name="twitter:image:alt" content="{alt}" />\n'
    if '<meta property="og:image:height"' in text:
        return re.sub(
            r'(<meta property="og:image:height"[^>]*/>\n)',
            r'\1' + repl, text, count=1)
    # Fallback: after og:image
    return re.sub(
        r'(<meta property="og:image" content="[^"]*"\s*/>\n)',
        r'\1' + repl, text, count=1)

def upsert_og_dimensions(text: str) -> str:
    """Add og:image:width/height + og:image:type if absent."""
    additions = []
    if 'og:image:type' not in text:
        additions.append('<meta property="og:image:type" content="image/jpeg" />')
    if 'og:image:secure_url' not in text:
        additions.append(f'<meta property="og:image:secure_url" content="{OG_IMG}" />')
    if 'og:image:width' not in text:
        additions.append('<meta property="og:image:width" content="1200" />')
    if 'og:image:height' not in text:
        additions.append('<meta property="og:image:height" content="630" />')
    if not additions:
        return text
    repl = '\n'.join(additions) + '\n'
    return re.sub(
        r'(<meta property="og:image" content="[^"]*"\s*/>\n)',
        r'\1' + repl, text, count=1)

def upsert_twitter_image(text: str) -> str:
    """Make sure twitter:image is set."""
    if 'twitter:image' in text:
        return text
    repl = f'<meta name="twitter:image" content="{OG_IMG}" />\n'
    if 'twitter:card' in text:
        return re.sub(
            r'(<meta name="twitter:card"[^>]*/>\n)',
            r'\1' + repl, text, count=1)
    return text

def remove_existing_jsonld(text: str, type_marker: str) -> str:
    """Remove any existing JSON-LD block containing the given @type marker.

    Used to ensure idempotency — drop the prior block before re-inserting."""
    pattern = re.compile(
        r'<script type="application/ld\+json">\{[^<]*?"@type":"'
        + re.escape(type_marker) +
        r'"[^<]*?\}</script>\n?', re.DOTALL)
    return pattern.sub('', text)

def inject_before_head_close(text: str, snippet: str) -> str:
    return text.replace('</head>', snippet + '</head>', 1)

# ───────── JSON-LD builders ─────────

def service_jsonld(slug: str) -> str:
    name, stype, desc_short = SERVICE_INFO[slug]
    url = f"{BASE}/{slug}"
    obj = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "serviceType": stype,
        "description": desc_short,
        "url": url,
        "provider": {"@id": f"{BASE}/#organization"},
        "areaServed": ["Worldwide"],
        "audience": {"@type": "Audience", "audienceType": "Business"},
        "category": "Custom software development",
    }
    return f'<script type="application/ld+json">{json.dumps(obj, separators=(",", ":"))}</script>\n'

def breadcrumb_jsonld(items: list[tuple[str,str]]) -> str:
    """items: list of (name, url) pairs."""
    obj = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i+1, "name": n, "item": u}
            for i, (n, u) in enumerate(items)
        ],
    }
    return f'<script type="application/ld+json">{json.dumps(obj, separators=(",", ":"))}</script>\n'

def blog_jsonld() -> str:
    posts = [(s, t) for s, t, _, _, _ in PAGES if s.startswith('post-')]
    obj = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "WiseTrack Journal",
        "url": f"{BASE}/insights.html",
        "publisher": {"@id": f"{BASE}/#organization"},
        "blogPost": [
            {"@type": "BlogPosting", "headline": title, "url": f"{BASE}/{slug}"}
            for slug, title in posts
        ],
    }
    return f'<script type="application/ld+json">{json.dumps(obj, separators=(",", ":"))}</script>\n'

def portfolio_jsonld() -> str:
    works = [
        ("RBI (Burger King + Popeyes) — QSR dashboard",   "Multi-country ops dashboard for Restaurant Brands International franchises."),
        ("Vivo Mobile — tech-ops dashboard",              "After-sales tech ops dashboard across India retail network."),
        ("Elections counting platform",                    "Real-time elections counting feed for Hindustan Times, ABP, Times Internet, Google."),
        ("Maldives resort operations",                     "Resort ops platform — bookings, housekeeping, F&B, F&B kitchen."),
        ("Ragenaizer rollout",                             "Internal-platform rollout of the Ragenaizer Business OS."),
    ]
    obj = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "WiseTrack — Work",
        "url": f"{BASE}/portfolio.html",
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": [
                {"@type": "ListItem", "position": i+1,
                 "item": {"@type": "CreativeWork", "name": n, "description": d, "creator": {"@id": f"{BASE}/#organization"}}}
                for i, (n, d) in enumerate(works)
            ],
        },
    }
    return f'<script type="application/ld+json">{json.dumps(obj, separators=(",", ":"))}</script>\n'

def software_app_jsonld() -> str:
    obj = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "Ragenaizer",
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "Web",
        "description": "Ragenaizer is a Business OS — HRMS, CRM, PMS, Mail, Chat, Drive, Accounts, LMS, Research, Vision — with agentic AI woven through every module.",
        "url": "https://ragenaizer.com/",
        "publisher": {"@id": f"{BASE}/#organization"},
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "INR", "availability": "https://schema.org/InStock"},
    }
    return f'<script type="application/ld+json">{json.dumps(obj, separators=(",", ":"))}</script>\n'

def careers_jsonld() -> str:
    obj = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Careers — WiseTrack Technologies",
        "url": f"{BASE}/careers.html",
        "about": {"@id": f"{BASE}/#organization"},
        "primaryImageOfPage": OG_IMG,
        "mainEntity": {
            "@type": "Organization",
            "@id": f"{BASE}/#organization",
            "hiringOrganization": True,
        },
    }
    return f'<script type="application/ld+json">{json.dumps(obj, separators=(",", ":"))}</script>\n'


# ───────── Per-page processing ─────────
def process_page(p: pathlib.Path) -> bool:
    text = p.read_text()
    orig = text

    # 1. OG image dimensions + secure_url + type
    text = upsert_og_dimensions(text)
    text = upsert_twitter_image(text)

    # 2. og:image:alt
    # Page-specific alts (better SEO)
    page_alt = OG_ALT
    if p.name.startswith('build-'):
        slug_name = p.name[len('build-'):].split('.')[0].upper()
        page_alt = f"WiseTrack — Custom {slug_name} build"
    elif p.name == 'ai.html':
        page_alt = "WiseTrack — AI & Agentic AI services"
    elif p.name == 'portfolio.html':
        page_alt = "WiseTrack — selected work"
    elif p.name == 'insights.html':
        page_alt = "WiseTrack Journal — field notes on engineering"
    text = upsert_meta_alt(text, page_alt)

    # 3. JSON-LD injections
    new_jsonld = []

    if p.name in SERVICE_INFO:
        text = remove_existing_jsonld(text, "Service")
        new_jsonld.append(service_jsonld(p.name))

    if p.name == 'index.html':
        text = remove_existing_jsonld(text, "BreadcrumbList")
        new_jsonld.append(breadcrumb_jsonld([("Home", f"{BASE}/")]))

    if p.name == 'insights.html':
        text = remove_existing_jsonld(text, "Blog")
        new_jsonld.append(blog_jsonld())

    if p.name == 'portfolio.html':
        text = remove_existing_jsonld(text, "CollectionPage")
        new_jsonld.append(portfolio_jsonld())

    if p.name == 'dashboard.html':
        text = remove_existing_jsonld(text, "SoftwareApplication")
        new_jsonld.append(software_app_jsonld())

    if new_jsonld:
        text = inject_before_head_close(text, ''.join(new_jsonld))

    if text != orig:
        p.write_text(text)
        return True
    return False


# ───────── Sitemap ─────────
def write_sitemap():
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for slug, _, _, prio, freq in PAGES:
        out.append('  <url>')
        out.append(f'    <loc>{BASE}/{slug}</loc>')
        out.append(f'    <lastmod>{TODAY}</lastmod>')
        out.append(f'    <changefreq>{freq}</changefreq>')
        out.append(f'    <priority>{prio:.2f}</priority>')
        out.append('  </url>')
    out.append('</urlset>')
    (ROOT / 'sitemap.xml').write_text('\n'.join(out) + '\n')


# ───────── llms.txt ─────────
def write_llms():
    lines = [
        "# WiseTrack Technologies",
        "",
        "> WiseTrack Technologies is a software company in Noida, India, founded 2020.",
        "> We build custom applications, ship production-grade agentic AI, and",
        "> license Ragenaizer — our Business OS. Working stack: C# / .NET /",
        "> ASP.NET Core, Postgres, ClickHouse (for vectors), Docker on Linux,",
        "> with Blazor / Razor on the front-end. Anthropic Claude for AI.",
        "> Small team, deliberate engagements, ~50% inbound rejection rate.",
        "",
        "## Brands",
        "- [HyperScripts](https://hyperscripts.io/): Custom software engagements. Web apps, mobile apps, finance integrations, multi-source dashboards, agentic AI.",
        "- [Ragenaizer](https://ragenaizer.com/): Our flagship product — one app to run a business, with agentic AI woven into every module.",
        "",
        "## Core pages",
    ]
    for slug, title, summary, _, _ in PAGES:
        if slug.startswith('post-') or slug.startswith('build-'):
            continue
        url = f"{BASE}/" if slug == "" else f"{BASE}/{slug}"
        lines.append(f"- [{title}]({url}): {summary}")
    lines.append("")
    lines.append("## Articles (Journal)")
    for slug, title, summary, _, _ in PAGES:
        if not slug.startswith('post-'):
            continue
        lines.append(f"- [{title}]({BASE}/{slug}): {summary}")
    lines.append("")
    lines.append("## Custom build pages — Ragenaizer as proof of capability")
    for slug, title, summary, _, _ in PAGES:
        if not slug.startswith('build-'):
            continue
        lines.append(f"- [{title}]({BASE}/{slug}): {summary}")
    lines.append("")
    lines.append("## Contact")
    lines.append(f"- Email: support@wisetrack.in")
    lines.append(f"- WhatsApp (sales & support): https://wa.me/919220474451")
    lines.append(f"- Office: Unit 314, Tower A, ATS Bouquet, Sector 132, Noida, Uttar Pradesh, India")
    lines.append("")
    lines.append("## Stack we work in")
    lines.append("- Languages: C#, .NET / ASP.NET Core, Blazor / Razor")
    lines.append("- Data: Postgres, ClickHouse (vectors), Redis (cache), S3-compatible object store")
    lines.append("- Infra: Docker, Linux, Kubernetes")
    lines.append("- AI: Anthropic Claude (Haiku 4.5, Sonnet 4.5), bge-small-en embeddings, custom agent loop with tool-use, prompt caching, three-tier safety gates, full token + cost observability")
    lines.append("")
    (ROOT / 'llms.txt').write_text('\n'.join(lines) + '\n')


# ───────── llms-full.txt — richer agent grounding ─────────
def write_llms_full():
    content = f"""# WiseTrack Technologies · Full Profile

## Identity
- Legal name: WiseTrack Technologies
- Founded: 2020
- Office: Unit 314, Tower A, ATS Bouquet, Sector 132, Noida, Uttar Pradesh, India
- Email: support@wisetrack.in
- WhatsApp: https://wa.me/919220474451
- Site: https://wisetrack.in/

## Brands
- **HyperScripts** (https://hyperscripts.io) — custom software engagements
- **Ragenaizer** (https://ragenaizer.com) — Business OS we license, ten modules

## What we sell
We sell custom software builds and a licensable Business OS:
1. Custom web platforms (Multi-tenant SaaS, internal tools, complex workflows)
2. Finance & integrations (custom finance/accounting apps tied to whatever ERP the client runs)
3. Native mobile apps (iOS + Android, real backend)
4. Real-time dashboards (multi-source, fast queries)
5. AI & Agentic AI engineering — see https://wisetrack.in/ai.html
6. Ragenaizer license (off-the-shelf, ten modules, fast time-to-deploy)
7. Custom builds of each Ragenaizer module — proof of capability already shipped

## Stack
- **Backend**: C#, .NET 9, ASP.NET Core
- **Frontend**: Blazor (Server + WASM), Razor components
- **Data**: Postgres (primary OLTP), ClickHouse (OLAP + vector store), Redis (cache + queue), S3-compatible objects
- **Infra**: Docker, Linux, Kubernetes (selectively)
- **AI**: Anthropic Claude (Haiku 4.5 default for tool loops, Sonnet 4.5 for hard reasoning), direct HTTP integration (no LangChain/Semantic Kernel), prompt caching via anthropic-beta, bge-small-en for embeddings, ClickHouse for vector storage

## AI / Agentic capabilities
- Real multi-turn agent loop (up to 40 tool rounds per run, 60 tools/min rate limit)
- 90+ tools exposed to the LLM across 9 production business modules
- Three-tier safety gates: Safe (GET / read) / Moderate (POST/PUT, user confirms) / Critical (DELETE / payroll / hard gate)
- ClickHouse-backed RAG with cosine similarity, top-K configurable, bge-small-en embeddings
- Streaming responses via SSE; gRPC bidirectional for research / FGD pipelines
- Token + cost observability via `ai_token_usage` audit table (async fire-and-forget)
- Auto-fallback Haiku → Sonnet on 529 overload
- Anthropic Batch API support for long-running research jobs (50% cost discount)
- Per-tenant API keys, never stored at rest
- Modules with deep AI integration: Accounts, HRMS, PMS, Procurement
- Moderate AI integration: CRM, LMS, Research (async pipelines), Vision (transcription)
- Light: Drive

## Engagement model
- Small team. Two slots per quarter usually.
- We turn down roughly half of inbound briefs — by design.
- Two-week demos rather than three-month specs.
- We tell clients "build custom" or "license Ragenaizer" honestly — sometimes the answer is "buy a SaaS we don't sell."

## Past work (selected)
- Restaurant Brands International (Burger King + Popeyes) — multi-country QSR ops dashboard
- Vivo Mobile — tech-ops dashboard across India retail
- Elections counting platform — feeding Hindustan Times, ABP, Times Internet, Google
- Maldives resort operations — bookings, housekeeping, F&B, kitchen
- Ragenaizer rollouts — multiple internal-platform consolidations replacing 5–10 SaaS tools

## Contact
- Sales / support: support@wisetrack.in
- WhatsApp Business: https://wa.me/919220474451
- Average reply time: 7 hours within working week, worst case one working day

## Page index
"""
    for slug, title, summary, _, _ in PAGES:
        url = f"{BASE}/" if slug == "" else f"{BASE}/{slug}"
        content += f"- {url} — {title} · {summary}\n"
    (ROOT / 'llms-full.txt').write_text(content)


# ───────── Main ─────────
def main():
    print("=== SEO + AI-compatibility pass ===\n")

    # Update each page
    changed = 0
    for slug, *_ in PAGES:
        if slug == "":
            path = ROOT / 'index.html'
        else:
            path = ROOT / slug
        if not path.exists():
            print(f"  (missing) {path.name}")
            continue
        if process_page(path):
            print(f"  updated  {path.name}")
            changed += 1
        else:
            print(f"  no-change {path.name}")
    print(f"\n{changed} pages updated.")

    write_sitemap()
    print("✓ sitemap.xml regenerated with lastmod")

    write_llms()
    print("✓ llms.txt rewritten with full inventory")

    write_llms_full()
    print("✓ llms-full.txt written for agent grounding")


if __name__ == "__main__":
    main()
