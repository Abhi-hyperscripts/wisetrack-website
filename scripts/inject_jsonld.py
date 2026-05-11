"""Inject JSON-LD structured data into every HTML page.

What gets added:
  - Every page: Organization (shared @id) so it cascades across the site.
  - Homepage: + WebSite.
  - Marketing/legal/etc pages: + WebPage + BreadcrumbList.
  - Blog posts (post-*.html): + Article + BreadcrumbList.
  - contact.html: + ContactPage + FAQPage (matches the FAQ already on page).

Run from repo root:  python3 scripts/inject_jsonld.py
"""
from __future__ import annotations
import json, pathlib, re, html as html_mod

ROOT = pathlib.Path(__file__).resolve().parent.parent

ORG = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": "https://wisetrack.in/#organization",
    "name": "WiseTrack Technologies",
    "alternateName": "WiseTrack",
    "url": "https://wisetrack.in/",
    "logo": "https://wisetrack.in/assets/logo.png",
    "image": "https://wisetrack.in/assets/og-image.jpg",
    "description": "Custom applications, finance integrations with whatever the client runs, and Ragenaizer — a Business OS we license to clients.",
    "foundingDate": "2020",
    "email": "support@wisetrack.in",
    "telephone": "+91-120-4848000",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Sector 62",
        "addressLocality": "Noida",
        "addressRegion": "Uttar Pradesh",
        "postalCode": "201309",
        "addressCountry": "IN",
    },
    "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "customer service",
        "email": "support@wisetrack.in",
        "telephone": "+91-120-4848000",
        "areaServed": "Worldwide",
        "availableLanguage": ["English", "Hindi"],
    },
    "sameAs": [
        "https://hyperscripts.io/",
        "https://ragenaizer.com/",
    ],
    "subOrganization": [
        {"@type": "Organization", "name": "HyperScripts", "url": "https://hyperscripts.io/"},
        {"@type": "Organization", "name": "Ragenaizer", "url": "https://ragenaizer.com/"},
    ],
    "knowsAbout": [
        "C#", ".NET", "ASP.NET Core", "Blazor", "Razor",
        "Postgres", "SQL Server", "Docker", "Linux", "Kubernetes",
        "Custom software development",
        "Real-time dashboards", "Multi-tenant SaaS",
        "Business OS", "CRM", "HRMS", "Project management",
        "Accounting software", "LMS", "Video conferencing",
        "Team chat", "Cloud storage", "Unified inbox",
        "REST APIs", "Webhooks", "OAuth integrations",
    ],
}

WEBSITE = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": "https://wisetrack.in/#website",
    "url": "https://wisetrack.in/",
    "name": "WiseTrack Technologies",
    "description": "Custom applications and Ragenaizer Business OS — built in C# / .NET.",
    "publisher": {"@id": "https://wisetrack.in/#organization"},
    "inLanguage": "en",
}


# ----- per-page metadata -----------------------------------------------------
PAGE_META = {
    "index.html":        ("WiseTrack — Software that needs real engineering.", "Home"),
    "solutions.html":    ("Solutions — WiseTrack", "Solutions"),
    "portfolio.html":    ("Work — WiseTrack", "Work"),
    "methodology.html":  ("Method — WiseTrack", "Method"),
    "insights.html":     ("Journal — WiseTrack", "Journal"),
    "careers.html":      ("Careers — WiseTrack", "Careers"),
    "contact.html":      ("Contact — WiseTrack", "Contact"),
    "terms.html":        ("Terms & Conditions — WiseTrack", "Terms"),
    "privacy.html":      ("Privacy Policy — WiseTrack", "Privacy"),
    "cookies.html":      ("Cookie Policy — WiseTrack", "Cookies"),
    "dashboard.html":    ("Ragenaizer · Live demo — WiseTrack", "Ragenaizer Demo"),
    "client-portal.html":("Client Portal — WiseTrack", "Client Portal"),
    "build-hrms.html":      ("Custom HRMS — WiseTrack", "Custom HRMS"),
    "build-crm.html":       ("Custom CRM — WiseTrack", "Custom CRM"),
    "build-pms.html":       ("Custom PMS — WiseTrack", "Custom PMS"),
    "build-vision.html":    ("Custom video conferencing — WiseTrack", "Custom video"),
    "build-drive.html":     ("Custom cloud Drive — WiseTrack", "Custom Drive"),
    "build-accounts.html":  ("Custom accounting — WiseTrack", "Custom accounting"),
    "build-lms.html":       ("Custom LMS — WiseTrack", "Custom LMS"),
    "build-research.html":  ("Custom research platform — WiseTrack", "Custom research"),
    "build-email.html":     ("Custom unified inbox — WiseTrack", "Custom inbox"),
    "build-chat.html":      ("Custom team chat — WiseTrack", "Custom chat"),
}

# Blog posts: slug -> (title, summary, author, date_iso, tag/section)
POSTS = {
    "post-when-to-build-when-to-buy": ("When to build, when to buy.", "Most teams should buy off-the-shelf and move on. Some should build something custom. Here's how we help clients work out which side of the line their problem sits on.", "Anand", "2026-02-26", "Engineering"),
    "post-why-we-turn-down-half":     ("Why we turn down half our projects.", "Saying yes to the wrong project hurts everyone. We explain how we decide what to take on.", "Anand", "2026-02-24", "Method"),
    "post-real-cost-of-wrong-stack":  ("The real cost of the wrong stack.", "Tech choices made on day one show up in the bill two years later.", "Karthik", "2025-12-12", "Engineering"),
    "post-one-app-vs-seven":          ("One app vs. seven.", "A 200-person firm moved from seven tools to Ragenaizer. The interesting parts weren't technical.", "Sara", "2025-11-04", "Ragenaizer"),
    "post-postgres-is-enough":        ("Postgres is enough, until it isn't.", "A field guide to the moment you should stop reaching for a new database — and when to.", "Priya", "2025-09-22", "Engineering"),
    "post-two-week-demos":            ("Two-week demos beat documents.", "Why we never write a 60-page spec, and what we do instead.", "Anand", "2025-08-08", "Method"),
}

FAQ = [
    ("Do you take on small projects?",
     "If the engineering is interesting and the scope is honest, yes. We've shipped projects under ₹10L when they fit. We turn down poorly-scoped large ones much more often."),
    ("How long until you reply?",
     "Average is 7 hours during the working week. Worst case, one full working day."),
    ("Do you sign an NDA?",
     "Standard mutual NDA, yes. Send us yours or use ours. Either is fine."),
    ("Can you work with our internal team?",
     "Often. We work well as the engineering arm next to a product or design team. Pair-engineering with your folks is welcome."),
]


def webpage_node(url: str, title: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "url": url,
        "name": title,
        "isPartOf": {"@id": "https://wisetrack.in/#website"},
        "publisher": {"@id": "https://wisetrack.in/#organization"},
        "inLanguage": "en",
    }


def breadcrumb_node(items: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": url}
            for i, (name, url) in enumerate(items)
        ],
    }


def article_node(slug: str, title: str, summary: str, author: str, date_iso: str, section: str) -> dict:
    url = f"https://wisetrack.in/{slug}.html"
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title.rstrip("."),
        "description": summary,
        "image": "https://wisetrack.in/assets/og-image.jpg",
        "datePublished": date_iso,
        "dateModified": date_iso,
        "author": {"@type": "Person", "name": author, "worksFor": {"@id": "https://wisetrack.in/#organization"}},
        "publisher": {"@id": "https://wisetrack.in/#organization"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "articleSection": section,
        "inLanguage": "en",
        "url": url,
    }


def faq_node(items: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ],
    }


def render(nodes: list[dict]) -> str:
    out = []
    for n in nodes:
        out.append(
            '<script type="application/ld+json">' +
            json.dumps(n, separators=(",", ":"), ensure_ascii=False) +
            "</script>"
        )
    return "\n".join(out)


def inject(html: str, jsonld_block: str) -> str:
    # Strip any prior JSON-LD scripts to keep idempotent
    html = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", html, flags=re.DOTALL)
    # Insert just before </head>
    return html.replace("</head>", jsonld_block + "\n</head>", 1)


def url_for(name: str) -> str:
    if name == "index.html":
        return "https://wisetrack.in/"
    return f"https://wisetrack.in/{name}"


def process_static_page(name: str, title: str, label: str) -> None:
    p = ROOT / name
    text = p.read_text()
    url = url_for(name)
    nodes = [ORG]
    if name == "index.html":
        nodes.append(WEBSITE)
        nodes.append(webpage_node(url, title))
    else:
        nodes.append(webpage_node(url, title))
        # Breadcrumb: Home > Section
        nodes.append(breadcrumb_node([
            ("Home", "https://wisetrack.in/"),
            (label, url),
        ]))
    if name == "contact.html":
        nodes.append(faq_node(FAQ))
    block = render(nodes)
    p.write_text(inject(text, block))
    print(f"{name}: {len(nodes)} JSON-LD blocks")


def process_post(slug: str, title: str, summary: str, author: str, date_iso: str, section: str) -> None:
    name = f"{slug}.html"
    p = ROOT / name
    text = p.read_text()
    url = url_for(name)
    nodes = [
        ORG,
        article_node(slug, title, summary, author, date_iso, section),
        breadcrumb_node([
            ("Home", "https://wisetrack.in/"),
            ("Journal", "https://wisetrack.in/insights.html"),
            (title.rstrip("."), url),
        ]),
    ]
    block = render(nodes)
    p.write_text(inject(text, block))
    print(f"{name}: {len(nodes)} JSON-LD blocks (Article)")


def main():
    for name, (title, label) in PAGE_META.items():
        process_static_page(name, title, label)
    for slug, (title, summary, author, date_iso, section) in POSTS.items():
        process_post(slug, title, summary, author, date_iso, section)


if __name__ == "__main__":
    main()
