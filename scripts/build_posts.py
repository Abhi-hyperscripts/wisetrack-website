"""Generate blog post HTML files.

Each post is built from a content dict using the same HUD-frame template.
Run from repo root:  python3 scripts/build_posts.py
"""
from __future__ import annotations
import pathlib, html, textwrap

ROOT = pathlib.Path(__file__).resolve().parent.parent


# --------------------------------------------------------------------------- #
# Content
# --------------------------------------------------------------------------- #
POSTS = [
    {
        "slug": "post-when-to-build-when-to-buy",
        "title": "When to build, when to buy.",
        "italic_word": "buy",
        "subtitle": "Most teams should buy off-the-shelf and move on. Some should build something custom. We've watched both calls go wrong.",
        "date_iso": "2026-02-26",
        "date_human": "26 Feb 2026",
        "author": "Anand",
        "read": "7 min read",
        "tag": "HyperScripts",
        "tag_color": "tag-violet",
        "summary": "Most teams should buy off-the-shelf and move on. Some should build something custom. Here's how we help clients work out which side of the line their problem sits on.",
        "toc": [
            ("default-is-buy", "01 · The default is buy"),
            ("when-custom-wins", "02 · When custom actually wins"),
            ("five-questions", "03 · Five questions before you build"),
            ("honest-test", "04 · The honest test"),
            ("what-we-say-no-to", "05 · What we say no to"),
        ],
        "sections": [
            ("default-is-buy", "01", "The default is buy.",
             [
                "If a category has three credible vendors competing for your business — accounting, CRM, helpdesk, payroll, conferencing — buy. Most teams ask us about building these things and we send them away with a shortlist of SaaS products instead. There is no engineering reward in re-implementing Stripe, Notion, or Zoho.",
                "The reasoning is brutal but consistent. A mature SaaS in a competitive category has burned a thousand engineer-years on edge cases you haven't thought of: timezones, currency, refunds, dunning, audit logs, GDPR exports, single-sign-on, regional tax. You can't out-engineer that with a six-month build. You'll arrive on day one with a product that has 60% of the obvious features and none of the unsexy ones.",
             ]),
            ("when-custom-wins", "02", "When custom actually wins.",
             [
                "Custom wins when your workflow is the moat. If the way your operations team approves a transaction is what makes you a better business than your competitor, an off-the-shelf approval tool will flatten that into a generic form. You'll either bend the SaaS to fit (expensive integrations) or bend your process to fit the SaaS (you lose the moat). Either way, you've paid to become average.",
                "We see this most often in three places. Resort operations: every property runs slightly differently and the local quirks matter. Finance with deep Zoho — the accounting platform you bought knows nothing about your specific inventory model. And real-time dashboards stitched from systems that were never meant to talk to each other.",
             ]),
            ("five-questions", "03", "Five questions before you build.",
             [
                "Before you sign an SOW with anyone (us included), answer these in writing. If three or more answers point toward buy, buy.",
                "<strong>1.</strong> Is there a SaaS in this category with more than 1,000 paying customers? If yes, what specifically is missing for you?",
                "<strong>2.</strong> Can your team articulate the workflow without using SaaS-product names? If you can only describe what you need in terms of \"a Salesforce-but-for-X\", you're describing a fork, not a product.",
                "<strong>3.</strong> What's the cost of being wrong on the first version? If you can throw away v1 after six months and start again, you're prototyping — buy and validate first.",
                "<strong>4.</strong> Will you own this codebase in five years? Or will the original engineers have left and the project be undermaintained? Custom software has a maintenance bill, and it shows up forever.",
                "<strong>5.</strong> Is the engineering interesting? If the answer is no — if you're just lining up CRUD forms over a database — there's almost certainly a SaaS that does this better than you will. Build when the engineering is actually hard.",
             ]),
            ("honest-test", "04", "The honest test.",
             [
                "Here is the cheapest version of the build-vs-buy decision: pay for the top three SaaS options for one quarter. Use them. If by the end of three months your team is still complaining about specific friction that costs real money — and you can name it — then build the custom thing that removes that friction. Not a clone of the SaaS. The specific thing.",
                "The teams who skip this step almost always regret it. They spend six months and ₹40 lakh building something only to discover the off-the-shelf tool would have worked fine with a tiny workflow change.",
             ]),
            ("what-we-say-no-to", "05", "What we say no to.",
             [
                "We turn down build engagements that look like clones of existing SaaS without a clear workflow moat. We turn down engagements where the client wants \"a custom CRM\" or \"our own Slack\". We will gently suggest the SaaS that does this and offer to help with the deep configuration / integration instead — that's where the real engineering lives.",
                "We say yes when the system has to talk to three internal sources nobody else knows about, when the workflow is the product, or when scale and reliability requirements rule out anything off-the-shelf. That's our zone.",
             ]),
        ],
    },
    {
        "slug": "post-why-we-turn-down-half",
        "title": "Why we turn down half our projects.",
        "italic_word": "turn down",
        "subtitle": "Saying yes to the wrong project hurts everyone. Here's how we decide what to take on, and why being picky is the most useful thing we do for our clients.",
        "date_iso": "2026-02-24",
        "date_human": "24 Feb 2026",
        "author": "Anand",
        "read": "5 min read",
        "tag": "HyperScripts",
        "tag_color": "tag-violet",
        "summary": "Saying yes to the wrong project hurts everyone. We explain how we decide what to take on, and why being picky is the most useful thing we do for our clients.",
        "toc": [
            ("saying-no-is-the-work", "01 · Saying no is the work"),
            ("five-filters", "02 · The five filters"),
            ("wrong-fit", "03 · What wrong fit looks like"),
            ("right-fit", "04 · What right fit looks like"),
        ],
        "sections": [
            ("saying-no-is-the-work", "01", "Saying no is the work.",
             [
                "A bad project takes the same calendar time as a good one. Both fill the team's working hours, both occupy the same project slot, both deny that slot to a different client. So a yes to a marginal project is also a no to a strong one we haven't met yet.",
                "The math is even worse than that. A bad project leaks. The engineering is annoying, motivation slumps, code quality drops by a half-grade, the deadlines slip, the other concurrent projects pick up the slack. Bad projects are expensive in ways the timesheet does not show.",
             ]),
            ("five-filters", "02", "The five filters.",
             [
                "Every inbound brief goes through five quick filters. Three fails and we say no. Two fails and we have a hard conversation.",
                "<strong>Engineering depth.</strong> Is there something here that genuinely needs us? If the answer is \"a WordPress site plus a contact form\", we recommend an agency.",
                "<strong>Decision maker.</strong> Is the person we're talking to the one who can say yes and pay invoices? Three layers of middlemen is a yellow flag; four is a red one.",
                "<strong>Honest scope.</strong> Does the brief describe what they want, not what they think they should ask for? If we ask \"why this feature?\" three times and don't get past surface answers, it's a no.",
                "<strong>Realistic timeline.</strong> Anyone who says \"we need it in six weeks\" for a six-month build is telling us something useful about how they'll manage the rest of the project.",
                "<strong>The room.</strong> If a client treats engineering as a cost centre to be squeezed — not as the thing that makes their product good — that relationship breaks under load. We pass.",
             ]),
            ("wrong-fit", "03", "What wrong fit looks like.",
             [
                "Wrong fit usually looks reasonable on paper. The budget is fine, the timeline is fine, the tech stack is fine, the client is polite. The tell is in the second conversation: they cannot answer questions about their users without consulting a deck, they describe the problem in solutions (\"we need a microservices architecture\"), and they are gently shocked when we suggest scope cuts.",
                "We have learned the hard way that fixing this in the SOW does not fix it. The way the relationship starts is the way it stays.",
             ]),
            ("right-fit", "04", "What right fit looks like.",
             [
                "Right fit is much rarer and easier to spot. The client has a specific operational problem that's costing them measurable money. They can describe their users in concrete detail. They have already tried the obvious solutions and can tell you exactly why they failed. They know what they don't know.",
                "Those engagements are a joy. The work is interesting, the client respects the trade-offs, the software gets used the day it ships, and a year later it's still running fine. We aim for ten of those a year — three or four concurrent at a time — and turn down everything else.",
             ]),
        ],
    },
    {
        "slug": "post-real-cost-of-wrong-stack",
        "title": "The real cost of the wrong stack.",
        "italic_word": "wrong",
        "subtitle": "Tech choices made on day one show up in the bill two years later. We unpack the trade-offs we wish more teams thought through before they started building.",
        "date_iso": "2025-12-12",
        "date_human": "12 Dec 2025",
        "author": "Karthik",
        "read": "8 min read",
        "tag": "HyperScripts",
        "tag_color": "tag-cyan",
        "summary": "Tech choices made on day one show up in the bill two years later. We unpack the trade-offs we wish more teams thought through before they started building.",
        "toc": [
            ("hidden-costs", "01 · The hidden costs"),
            ("hiring-risk", "02 · Hiring risk"),
            ("operational-tax", "03 · The operational tax"),
            ("three-questions", "04 · Three questions before you choose"),
            ("our-default", "05 · Our default stack — and why"),
        ],
        "sections": [
            ("hidden-costs", "01", "The hidden costs.",
             [
                "The framework you pick on day one is the framework you'll be running in five years. Migrations are theoretically possible, practically rare. So the decision matters more than it feels at the moment you make it.",
                "There are three families of hidden cost. The first is talent: how easy will it be to hire experienced engineers two years from now? The second is operational: how much sleep does this stack cost? The third is dependency: how exposed are you when a critical library author quits maintenance?",
             ]),
            ("hiring-risk", "02", "Hiring risk.",
             [
                "Pick a popular stack and you have a deep pool of senior engineers to hire from at a fair market rate. Pick a fashionable one and you compete with every well-funded startup for the same 200 people. Pick an exotic one and you become the senior engineer.",
                "We have watched teams choose a beautiful new framework, recruit one rockstar to lead, and then quietly suffer for the next four years when that rockstar moves on and no replacement exists. The framework was correct. The hiring calculus was not.",
             ]),
            ("operational-tax", "03", "The operational tax.",
             [
                "Every stack has an operational tax — the engineering hours you spend keeping it alive between feature work. Some are notoriously cheap: a boring Postgres + Linux setup will run for years without ceremony. Some are expensive: anything that requires bespoke clustering, brittle build pipelines, or constant security upgrades to non-LTS dependencies.",
                "We track this in our own work as a percentage of engineer time spent on \"maintenance vs ship\". Healthy projects sit at 15–20%. Over 35% and the stack is the bug.",
             ]),
            ("three-questions", "04", "Three questions before you choose.",
             [
                "<strong>1.</strong> If we are still running this in 2030, will the language still have an LTS release? If you can't answer with confidence, pick something else.",
                "<strong>2.</strong> Can a competent engineer read the codebase in two days and start contributing? Some stacks reward heroes; the good ones reward newcomers.",
                "<strong>3.</strong> Are you choosing this because it's right for the problem, or because it was in the last conference talk you watched? Boring tech wins more projects than novelty.",
             ]),
            ("our-default", "05", "Our default stack — and why.",
             [
                "Our default is C# on .NET, ASP.NET Core for web APIs, Postgres for data, Docker on Linux for deployment. We chose this for very specific reasons.",
                ".NET has long-term-support cadence we can plan around. C# is one of the most-hireable languages in our market and the engineers it attracts tend to take production seriously. ASP.NET Core is mature, fast, and unfashionable in exactly the right way.",
                "Postgres is the database we'd choose again every time. Docker on Linux is the boring deployment story that has not failed us yet. None of these will turn up in a Twitter thread next year, which is precisely why we use them.",
             ]),
        ],
    },
    {
        "slug": "post-one-app-vs-seven",
        "title": "One app vs. seven.",
        "italic_word": "seven",
        "subtitle": "A 200-person firm moved from seven tools to Ragenaizer. The interesting parts weren't technical.",
        "date_iso": "2025-11-04",
        "date_human": "04 Nov 2025",
        "author": "Sara",
        "read": "6 min read",
        "tag": "Ragenaizer",
        "tag_color": "tag-cyan",
        "summary": "A 200-person firm moved from seven tools to Ragenaizer. The interesting parts weren't technical.",
        "toc": [
            ("before", "01 · The before"),
            ("decision", "02 · The decision"),
            ("migration-week", "03 · Migration week"),
            ("what-broke", "04 · What broke"),
            ("surprised", "05 · What surprised everyone"),
        ],
        "sections": [
            ("before", "01", "The before.",
             [
                "Seven tools. CRM in one place, projects in another, time-tracking in a third, support tickets in a fourth, internal docs scattered between two more, and a finance dashboard nobody trusted in the seventh. The monthly SaaS bill was substantial; the time tax on the team was much larger.",
                "Sales would close a deal in the CRM. Project ops would manually mirror that into the project tool. Finance would reconcile against the accounting system. Anyone with a quick question would ask in three Slack channels because they couldn't remember which tool held the truth. The work everyone did to keep the tools in sync was a second, invisible business inside the business.",
             ]),
            ("decision", "02", "The decision.",
             [
                "The CFO did the spreadsheet. Annual SaaS cost across the seven tools, plus the estimated cost of the team time spent on reconciliation. The total was uncomfortable. Switching to a single platform — Ragenaizer in this case — wasn't going to be cheaper on the SaaS line alone, but it would erase the reconciliation cost almost entirely.",
                "We were in those rooms. The pushback wasn't about features (we had them). It was about change. Seven tools meant seven teams with seven workflows that everybody had memorised. One tool meant one workflow, and a transition.",
             ]),
            ("migration-week", "03", "Migration week.",
             [
                "We blocked off a full week and we did not pretend it would be smooth. The team's productivity was going to take a hit for ten working days; we built that into the plan and told everybody.",
                "Days one and two were data import. Days three and four were running parallel — old tools and Ragenaizer both live, with the team encouraged to break the new system on purpose. Days five through eight were single-system: old tools read-only, Ragenaizer authoritative. By day ten the old tools were archived and read-only access was retained for the few people who still needed historical records.",
             ]),
            ("what-broke", "04", "What broke.",
             [
                "Three things broke that we should have predicted, and one we didn't.",
                "Predictable: imported contacts had duplicate records across tools (CRM and support both knew \"Anand at Acme\" but with different email casing). The finance team's reporting needed views we hadn't built yet. And the sales team's pipeline stages didn't map cleanly to the default Ragenaizer stages.",
                "Unpredictable: nobody on the team had realised how much institutional knowledge was sitting inside their Slack search. Switching tools meant losing that searchable history. We spent a week building an import for the most-used channels' archives.",
             ]),
            ("surprised", "05", "What surprised everyone.",
             [
                "Three months in, the team's reaction split. About 70% loved the single-system experience. 20% missed specific features of the old tools. 10% were diplomatic.",
                "The CFO's surprise was the most interesting. The reconciliation savings were real but smaller than projected. The savings that actually moved the P&L came from somewhere we hadn't quantified at all: decisions made faster. When the entire team can see the same numbers without anyone exporting a spreadsheet, the speed of the company changes shape. We didn't have a way to model that on day one and now we do.",
             ]),
        ],
    },
    {
        "slug": "post-postgres-is-enough",
        "title": "Postgres is enough, until it isn't.",
        "italic_word": "isn't",
        "subtitle": "A field guide to the moment you should stop reaching for a new database — and when to.",
        "date_iso": "2025-09-22",
        "date_human": "22 Sep 2025",
        "author": "Priya",
        "read": "9 min read",
        "tag": "Engineering",
        "tag_color": "tag-cyan",
        "summary": "A field guide to the moment you should stop reaching for a new database — and when to.",
        "toc": [
            ("further-than-you-think", "01 · Postgres goes further than you think"),
            ("three-signals", "02 · Three signals to look for"),
            ("migration-cost", "03 · The real migration cost"),
            ("playbook", "04 · A practical playbook"),
        ],
        "sections": [
            ("further-than-you-think", "01", "Postgres goes further than you think.",
             [
                "Most teams reach for a specialised database too early. They read a blog post about how some unicorn company runs everything on a streaming system and assume their CRUD app needs the same. It does not.",
                "On the systems we run, Postgres comfortably handles single-instance setups well into the millions of rows with simple indexing, the high tens of millions with proper partitioning and a thoughtful schema, and into hundreds of millions when you accept the operational complexity of read replicas and connection pooling. None of that requires moving off Postgres.",
                "We have shipped real-time-feeling dashboards on raw Postgres with materialised views and a careful refresh strategy. We have run multi-tenant SaaS with row-level security and tenant-keyed partitioning. We have done event-sourced workflows with an append-only table and a few smart indexes. Postgres is, in our experience, very rarely the bottleneck.",
             ]),
            ("three-signals", "02", "Three signals to start considering alternatives.",
             [
                "There are three honest signals that you should consider adding (not replacing — adding) another data store. Each one needs to be reproducible, measurable, and not solvable by indexing.",
                "<strong>Signal 1 — Hot path latency you cannot index away.</strong> If a small set of queries serves the majority of traffic and they cannot be made fast through indexing, materialised views, or a query rewrite, a key-value cache in front of Postgres usually solves it. Redis. That's the answer.",
                "<strong>Signal 2 — Write throughput you cannot batch.</strong> If sustained writes outpace what a single Postgres primary can absorb and you cannot shard or batch your writes, then a purpose-built time-series or column store may help. We have used ClickHouse for analytics dashboards where the read pattern is OLAP-shaped. Postgres still owns the operational data.",
                "<strong>Signal 3 — Search beyond LIKE.</strong> If you need ranked full-text search across long documents with synonyms and stemming, Postgres's built-in full-text is good enough until it isn't, and at that point a dedicated search engine is the right call. Until then, do not.",
             ]),
            ("migration-cost", "03", "The real migration cost.",
             [
                "Moving primary data off Postgres is one of the most expensive things you can do. You pay it in three currencies. Engineering hours, because every query, ORM mapping, transaction boundary, and integrity constraint has to be re-thought. Operational complexity, because you now run two systems and the failure modes multiply. And cognitive load on every new engineer who joins, forever.",
                "We have seen teams pay all three of those costs to escape a problem they could have indexed away in an afternoon. We have also seen teams put it off too long and run into a real wall. The judgment call is what we get paid for.",
             ]),
            ("playbook", "04", "A practical playbook.",
             [
                "If you're feeling pain, do these in order and stop the moment the pain goes away.",
                "<strong>Step 1.</strong> Run <code>EXPLAIN ANALYZE</code> on the slow queries. Most of the time, there's an index that doesn't exist yet, or a join that's doing something dumb.",
                "<strong>Step 2.</strong> Look at <code>pg_stat_statements</code>. The hot queries are not always the ones you think.",
                "<strong>Step 3.</strong> Add Redis in front of the hot read path. Cache invalidation is hard, but cheaper than data-store migration.",
                "<strong>Step 4.</strong> Move read traffic to replicas if write contention is the issue, not raw query speed.",
                "<strong>Step 5.</strong> Partition the largest tables by tenant or by date.",
                "<strong>Step 6.</strong> Only after all of the above: introduce a second store for the specific workload that doesn't fit Postgres's shape.",
                "We have shipped many production systems and only reached step 6 a handful of times. It's a long way down the list for a reason.",
             ]),
        ],
    },
    {
        "slug": "post-two-week-demos",
        "title": "Two-week demos beat documents.",
        "italic_word": "beat",
        "subtitle": "Why we never write a 60-page spec, and what we do instead.",
        "date_iso": "2025-08-08",
        "date_human": "08 Aug 2025",
        "author": "Anand",
        "read": "4 min read",
        "tag": "Method",
        "tag_color": "tag-lime",
        "summary": "Why we never write a 60-page spec, and what we do instead.",
        "toc": [
            ("the-problem", "01 · The 60-page spec problem"),
            ("demo-driven", "02 · Demo-driven planning"),
            ("what-we-write", "03 · What we still put in writing"),
            ("what-we-show", "04 · What we put on screen"),
        ],
        "sections": [
            ("the-problem", "01", "The 60-page spec problem.",
             [
                "Every traditional consulting engagement starts with a discovery phase that produces a long document. The document looks impressive, costs a quarter of the engagement budget, and goes unread for the rest of the project. By the time the team is shipping, the document is wrong in at least three important places — but nobody updates it because the team is busy shipping.",
                "The cost of the spec was not the writing. It was the false confidence everybody borrowed against while it was being written.",
             ]),
            ("demo-driven", "02", "Demo-driven planning.",
             [
                "We replace the long spec with a two-week demo cycle. Every two weeks, we put working software in front of the client. Not screenshots, not Figma, not a Loom video — software you can click. At the end of each demo we agree, on the spot, what the next two weeks will produce.",
                "This forces three healthy behaviours. We can't punt hard decisions to a future document — the calendar makes us decide. The client gets to react to something concrete instead of approving abstract bullets. And the team gets to course-correct early and often, when the cost of changing direction is small.",
             ]),
            ("what-we-write", "03", "What we still put in writing.",
             [
                "Demos do not replace writing entirely. There are three things we always write down.",
                "<strong>Decisions.</strong> Every meaningful trade-off — \"we chose row-level security over a per-tenant database\" — gets a one-paragraph entry in a decision log. Future-us reads it more often than we expect.",
                "<strong>Contracts.</strong> Anything that crosses a system boundary (an API, a webhook, a CSV import, a data model another team depends on) gets a written contract. These are short and precise. They are also versioned.",
                "<strong>The next two weeks.</strong> A bullet list. Never longer than one page. Signed off by the client at the end of every demo.",
                "That's it. Nothing else gets written into the long-form documents the project would have produced with a traditional spec — because nothing else changes slowly enough for documents to be worth maintaining.",
             ]),
            ("what-we-show", "04", "What we put on screen.",
             [
                "The demo is the deliverable. We host the build on a staging URL the client can poke at any time, not just during the demo call. We seed it with real-looking data — sometimes anonymised production data, sometimes generated. We don't pre-bake demo flows; the client can wander wherever they want.",
                "After six years of running this way, we have one strong belief: the projects that ship well are the ones where the client sees the software early, often, and with the rough edges left in. Polish too soon and you can't have the right conversations.",
             ]),
        ],
    },
]


# --------------------------------------------------------------------------- #
# Templates
# --------------------------------------------------------------------------- #
NAV = """\\
<div class="fixed top-0 left-0 right-0 h-[2px] z-[80] origin-left scale-x-0 bg-gradient-to-r from-violet via-indigo to-cyan" data-progress></div>

<div class="fixed top-0 left-0 right-0 z-[70] bg-bg/85 backdrop-blur-xl border-b border-white/5">
  <div class="max-w-page mx-auto px-edge h-9 flex items-center justify-between text-[11px] mono tracking-wider text-muted">
    <div class="flex items-center gap-3"><span class="h-1.5 w-1.5 rounded-full bg-mint animate-pulse"></span><span class="hidden sm:inline">JOURNAL · {date_human} · {read}</span><span class="sm:hidden">JOURNAL</span></div>
    <div class="flex items-center gap-5"><span class="hidden md:inline">Noida, IN</span><span data-clock>--:--:-- IST</span></div>
  </div>
</div>

<header class="fixed top-9 left-0 right-0 z-[60] bg-bg/55 backdrop-blur-2xl border-b border-white/5 transition-all duration-300">
  <nav class="max-w-page mx-auto px-edge h-[80px] flex items-center justify-between">
    <a href="index.html" class="flex items-center gap-2.5 group">
      <img src="assets/logo/wt-mark.svg" alt="Wisetrack Logo" class="h-[24px] md:h-[29px] w-auto transition-transform group-hover:scale-105" />
      <span class="font-sans font-extrabold text-base md:text-lg tracking-tight text-text whitespace-nowrap">WISETRACK TECHNOLOGIES</span>
    </a>

    <!-- Desktop links -->
    <div class="hidden md:flex items-center gap-8 text-[13px] font-semibold text-text-2">
      <div class="relative group py-6">
        <a href="products.html" class="hover:text-text flex items-center gap-1 transition-colors">
          Products
          <svg class="w-3.5 h-3.5 opacity-60 transition-transform group-hover:rotate-180" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" /></svg>
        </a>
        <!-- Mega Dropdown -->
        <div class="absolute top-full left-1/2 -translate-x-1/2 w-[92vw] max-w-[850px] pt-3 opacity-0 pointer-events-none group-hover:opacity-100 group-hover:pointer-events-auto transition-all duration-300 z-50">
          <div class="bg-surface border border-white/10 rounded-2xl p-6 shadow-2xl backdrop-blur-2xl text-left">
            <div class="flex items-center justify-between mb-4 pb-3 border-b border-white/5">
              <div>
                <span class="font-display font-light text-xl text-text">Our Flagship Business OS: <b class="font-bold text-indigo">Ragenaizer</b></span>
                <p class="text-xs text-text-2/70 mt-1">One integrated database system replacing up to 7 separate B2B SaaS licenses.</p>
              </div>
              <a href="products.html" class="text-xs font-mono font-bold text-indigo hover:underline flex items-center gap-1">SEE ALL PRODUCTS &rarr;</a>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <a href="hrms-payroll.html" class="block p-4 bg-white/[0.01] border border-white/5 hover:border-violet/30 hover:bg-white/[0.02] rounded-xl transition-all duration-200 group/card">
                <div class="flex items-center gap-3.5 mb-2">
                  <span class="text-lg">👥</span>
                  <div class="text-sm font-bold text-text">HRMS & Payroll</div>
                </div>
                <p class="text-xs text-text-2/70 leading-relaxed mb-3">Statutory Indian payroll compliance, tax filing, geofenced attendance.</p>
                <span class="text-[10px] font-bold text-indigo tracking-wider font-mono">EXPLORE MODULE &rarr;</span>
              </a>
              <a href="crm-sales.html" class="block p-4 bg-white/[0.01] border border-white/5 hover:border-mint/30 hover:bg-white/[0.02] rounded-xl transition-all duration-200 group/card">
                <div class="flex items-center gap-3.5 mb-2">
                  <span class="text-lg">💼</span>
                  <div class="text-sm font-bold text-text">CRM & Sales</div>
                </div>
                <p class="text-xs text-text-2/70 leading-relaxed mb-3">Pipeline mapping, lead forms integration, client record sharing.</p>
                <span class="text-[10px] font-bold text-indigo tracking-wider font-mono">EXPLORE MODULE &rarr;</span>
              </a>
              <a href="build-pms.html" class="block p-4 bg-white/[0.01] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.02] rounded-xl transition-all duration-200 group/card">
                <div class="flex items-center gap-3.5 mb-2">
                  <span class="text-lg">🛠️</span>
                  <div class="text-sm font-bold text-text">PMS & Projects</div>
                </div>
                <p class="text-xs text-text-2/70 leading-relaxed mb-3">Milestone tracking, engineering bug manager, timesheets & billing.</p>
                <span class="text-[10px] font-bold text-indigo tracking-wider font-mono">EXPLORE MODULE &rarr;</span>
              </a>
              <a href="build-lms.html" class="block p-4 bg-white/[0.01] border border-white/5 hover:border-cyan/30 hover:bg-white/[0.02] rounded-xl transition-all duration-200 group/card">
                <div class="flex items-center gap-3.5 mb-2">
                  <span class="text-lg">🎓</span>
                  <div class="text-sm font-bold text-text">LMS & Training</div>
                </div>
                <p class="text-xs text-text-2/70 leading-relaxed mb-3">Structured employee training, compliance testing, digital certificates.</p>
                <span class="text-[10px] font-bold text-indigo tracking-wider font-mono">EXPLORE MODULE &rarr;</span>
              </a>
              <a href="build-accounts.html" class="block p-4 bg-white/[0.01] border border-white/5 hover:border-lime/30 hover:bg-white/[0.02] rounded-xl transition-all duration-200 group/card">
                <div class="flex items-center gap-3.5 mb-2">
                  <span class="text-lg">🧾</span>
                  <div class="text-sm font-bold text-text">Double-Entry Accounts</div>
                </div>
                <p class="text-xs text-text-2/70 leading-relaxed mb-3">Ledger sync, automated invoicing, expenses, cashflow analysis.</p>
                <span class="text-[10px] font-bold text-indigo tracking-wider font-mono">EXPLORE MODULE &rarr;</span>
              </a>
              <a href="build-chat.html" class="block p-4 bg-white/[0.01] border border-white/5 hover:border-sky/30 hover:bg-white/[0.02] rounded-xl transition-all duration-200 group/card">
                <div class="flex items-center gap-3.5 mb-2">
                  <span class="text-lg">💬</span>
                  <div class="text-sm font-bold text-text">Enterprise Chat</div>
                </div>
                <p class="text-xs text-text-2/70 leading-relaxed mb-3">Audit-logged messaging, file attachments, team channel controls.</p>
                <span class="text-[10px] font-bold text-indigo tracking-wider font-mono">EXPLORE MODULE &rarr;</span>
              </a>
            </div>
          </div>
        </div>
      </div>

      <div class="relative group py-6">
        <a href="custom-services.html" class="hover:text-text flex items-center gap-1 transition-colors">
          Services
          <svg class="w-3.5 h-3.5 opacity-60 transition-transform group-hover:rotate-180" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" /></svg>
        </a>
        <!-- Services Dropdown -->
        <div class="absolute top-full left-1/2 -translate-x-1/2 w-[92vw] max-w-[650px] pt-3 opacity-0 pointer-events-none group-hover:opacity-100 group-hover:pointer-events-auto transition-all duration-300 z-50">
          <div class="bg-surface border border-white/10 rounded-2xl p-6 shadow-2xl backdrop-blur-2xl text-left">
            <div class="flex items-center justify-between mb-4 pb-3 border-b border-white/5">
              <div>
                <span class="font-display font-light text-xl text-text">Software Development: <b class="font-bold text-indigo">HyperScripts</b></span>
                <p class="text-xs text-text-2/70 mt-1">High-performance custom engineering for web, mobile, and workflow systems.</p>
              </div>
              <a href="custom-services.html" class="text-xs font-mono font-bold text-indigo hover:underline flex items-center gap-1">SEE ALL SERVICES &rarr;</a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <a href="custom-services.html#custom-software" class="block p-4 bg-white/[0.01] border border-white/5 hover:border-violet/30 hover:bg-white/[0.02] rounded-xl transition-all duration-200 group/card">
                <div class="flex items-center gap-3.5 mb-2">
                  <span class="text-lg">💻</span>
                  <div class="text-sm font-bold text-text">Custom Web & OS Software</div>
                </div>
                <p class="text-xs text-text-2/70 leading-relaxed mb-1">C#, .NET Core, Blazor, Postgres. Scalable business architecture.</p>
              </a>
              <a href="custom-services.html#mobile-apps" class="block p-4 bg-white/[0.01] border border-white/5 hover:border-lime/30 hover:bg-white/[0.02] rounded-xl transition-all duration-200 group/card">
                <div class="flex items-center gap-3.5 mb-2">
                  <span class="text-lg">📱</span>
                  <div class="text-sm font-bold text-text">Mobile Applications</div>
                </div>
                <p class="text-xs text-text-2/70 leading-relaxed mb-1">Native iOS & Android apps mapped to central business databases.</p>
              </a>
              <a href="custom-services.html#ai-automation" class="block p-4 bg-white/[0.01] border border-white/5 hover:border-mint/30 hover:bg-white/[0.02] rounded-xl transition-all duration-200 group/card">
                <div class="flex items-center gap-3.5 mb-2">
                  <span class="text-lg">🤖</span>
                  <div class="text-sm font-bold text-text">Agentic AI Solutions</div>
                </div>
                <p class="text-xs text-text-2/70 leading-relaxed mb-1">Production agent loops using Claude 3.5, RAG, and ClickHouse.</p>
              </a>
              <a href="custom-services.html#dashboards" class="block p-4 bg-white/[0.01] border border-white/5 hover:border-sky/30 hover:bg-white/[0.02] rounded-xl transition-all duration-200 group/card">
                <div class="flex items-center gap-3.5 mb-2">
                  <span class="text-lg">📊</span>
                  <div class="text-sm font-bold text-text">Interactive Dashboards</div>
                </div>
                <p class="text-xs text-text-2/70 leading-relaxed mb-1">Consolidated metrics visualizer showing real-time operational status.</p>
              </a>
            </div>
          </div>
        </div>
      </div>

      <a href="ai.html" class="hover:text-text transition-colors">AI</a>
      <a href="portfolio.html" class="hover:text-text transition-colors">Work</a>
      <a href="methodology.html" class="hover:text-text transition-colors">Method</a>
      <a href="blog.html" class="hover:text-text transition-colors">Blog</a>
      <a href="careers.html" class="hover:text-text transition-colors">Careers</a>
    </div>

    <div class="flex items-center gap-3">
      <a href="contact.html" class="btn-primary flex items-center gap-2 text-xs font-semibold py-2 px-4 rounded-lg bg-indigo text-white hover:opacity-90 transition-all">
        Start a Project <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3 7h8M7 3l4 4-4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </a>
      <button class="md:hidden h-9 w-9 grid place-items-center rounded-full border border-white/10" data-menu-toggle aria-expanded="false" aria-label="Open menu">
        <span class="block w-4 h-[1.5px] bg-text mb-1"></span><span class="block w-4 h-[1.5px] bg-text"></span>
      </button>
    </div>
  </nav>

  <!-- Mobile Navigation -->
  <div data-menu class="md:hidden hidden bg-bg border-t border-white/5 [&.open]:block">
    <div class="px-edge py-6 flex flex-col gap-4 text-lg text-left">
      <a href="index.html" class="py-2 hover:text-text font-bold">Home</a>
      <details class="py-2 group">
        <summary class="flex items-center justify-between text-lg cursor-pointer list-none text-text font-semibold">
          <span>Products</span>
          <svg class="opacity-60 transition-transform group-open:rotate-180" width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3 5l4 4 4-4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </summary>
        <div class="mobile-build-list mt-3 pl-3 flex flex-col gap-2">
          <a class="py-2 px-3 block text-sm border-l border-white/5 text-text hover:text-text font-bold" href="products.html">All Products &rarr;</a>
          <a class="py-2 px-3 block text-sm border-l border-white/5 text-text-2 hover:text-text" href="hrms-payroll.html">HRMS & Payroll &rarr;</a>
          <a class="py-2 px-3 block text-sm border-l border-white/5 text-text-2 hover:text-text" href="crm-sales.html">CRM & Sales &rarr;</a>
          <a class="py-2 px-3 block text-sm border-l border-white/5 text-text-2 hover:text-text" href="build-pms.html">PMS</a>
          <a class="py-2 px-3 block text-sm border-l border-white/5 text-text-2 hover:text-text" href="build-lms.html">LMS</a>
          <a class="py-2 px-3 block text-sm border-l border-white/5 text-text-2 hover:text-text" href="build-accounts.html">Accounts</a>
          <a class="py-2 px-3 block text-sm border-l border-white/5 text-text-2 hover:text-text" href="build-chat.html">Chat & Video</a>
        </div>
      </details>
      <details class="py-2 group">
        <summary class="flex items-center justify-between text-lg cursor-pointer list-none text-text font-semibold">
          <span>Services</span>
          <svg class="opacity-60 transition-transform group-open:rotate-180" width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3 5l4 4 4-4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </summary>
        <div class="mobile-build-list mt-3 pl-3 flex flex-col gap-2">
          <a class="py-2 px-3 block text-sm border-l border-white/5 text-text hover:text-text font-bold" href="custom-services.html">All Services &rarr;</a>
          <a class="py-2 px-3 block text-sm border-l border-white/5 text-text-2 hover:text-text" href="custom-services.html#custom-software">Custom Web Development</a>
          <a class="py-2 px-3 block text-sm border-l border-white/5 text-text-2 hover:text-text" href="custom-services.html#mobile-apps">Mobile Applications</a>
          <a class="py-2 px-3 block text-sm border-l border-white/5 text-text-2 hover:text-text" href="custom-services.html#ai-automation">Agentic AI Loops</a>
          <a class="py-2 px-3 block text-sm border-l border-white/5 text-text-2 hover:text-text" href="custom-services.html#dashboards">Custom Dashboards</a>
        </div>
      </details>
      <a href="ai.html" class="py-2 hover:text-text">AI Solutions</a>
      <a href="portfolio.html" class="py-2 hover:text-text">Work</a>
      <a href="methodology.html" class="py-2 hover:text-text">Company</a>
      <a href="blog.html" class="py-2 hover:text-text font-bold">Blog</a>
      <a href="careers.html" class="py-2 hover:text-text">Careers</a>
      <a href="contact.html" class="btn-primary w-fit mt-2">Start a Project</a>
    </div>
  </div>
</header>
"""

FOOTER = """\
<footer class="relative border-t border-white/5">
  <div class="max-w-page mx-auto px-edge pt-20 pb-10">
    <div class="grid grid-cols-12 gap-gutter">
      <div class="col-span-12 lg:col-span-4">
        <a href="index.html" class="flex items-center gap-2.5"><span class="brand-wordmark text-[17px] md:text-[20px]">WISETRACK&nbsp;TECHNOLOGIES<span class="text-violet">.</span></span></a>
        <p class="mt-6 max-w-md text-text-2/80 leading-relaxed">Software company with two brands. <span class="text-text">HyperScripts</span> builds custom software. <span class="text-text">Ragenaizer</span> is our flagship product.</p>
        <div class="mt-6 flex items-center gap-3 text-muted text-sm"><span class="dot"></span><span>Open for new engagements · Q1–Q2 2026</span></div>
      </div>
      <div class="col-span-6 md:col-span-3 lg:col-span-2 lg:col-start-6"><div class="mono text-[11px] tracking-widest text-muted mb-5">EXPLORE</div><ul class="flex flex-col gap-3 text-text-2"><li><a href="solutions.html" class="hover:text-text">Solutions</a></li><li><a href="portfolio.html" class="hover:text-text">Work</a></li><li><a href="methodology.html" class="hover:text-text">Method</a></li><li><a href="blog.html" class="hover:text-text">Journal</a></li></ul></div>
      <div class="col-span-6 md:col-span-3 lg:col-span-2"><div class="mono text-[11px] tracking-widest text-muted mb-5">BRANDS</div><ul class="flex flex-col gap-3 text-text-2"><li><a href="solutions.html" class="hover:text-text">HyperScripts</a></li><li><a href="dashboard.html" class="hover:text-text">Ragenaizer</a></li><li><a href="careers.html" class="hover:text-text">Careers</a></li><li><a href="client-portal.html" class="hover:text-text">Client portal</a></li></ul></div>
      <div class="col-span-6 md:col-span-3 lg:col-span-2"><div class="mono text-[11px] tracking-widest text-muted mb-5">LEGAL</div><ul class="flex flex-col gap-3 text-text-2"><li><a href="terms.html" class="hover:text-text">Terms</a></li><li><a href="privacy.html" class="hover:text-text">Privacy</a></li><li><a href="cookies.html" class="hover:text-text">Cookies</a></li></ul></div>
      <div class="col-span-12 md:col-span-6 lg:col-span-2"><div class="mono text-[11px] tracking-widest text-muted mb-5">FIELD NOTES</div><p class="text-text-2/85 mb-3">Occasional writing on engineering, products, and the work.</p><form class="flex items-center gap-2"><input type="email" placeholder="you@company.com" class="field flex-1"/><button class="btn-primary magnetic" type="submit"><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3 7h8M7 3l4 4-4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></button></form></div>
    </div>
    <div class="mt-16 pt-8 border-t border-white/5 flex flex-col md:flex-row gap-6 justify-between items-start md:items-center"><p class="mono text-[11px] text-muted tracking-widest">© 2026 WISETRACK TECHNOLOGIES · HARD SOFTWARE, BUILT SELECTIVELY</p><div class="flex gap-6 text-sm text-muted"><a href="privacy.html" class="hover:text-text">Privacy</a><a href="terms.html" class="hover:text-text">Terms</a><a href="cookies.html" class="hover:text-text">Cookies</a><a href="contact.html" class="hover:text-text">Contact</a></div></div>
  </div>
</footer>
"""

TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<script>(function(){{try{{if(localStorage.getItem("theme")!=="dark"){{document.documentElement.classList.add("light");}}else{{document.documentElement.classList.remove("light");}}}}catch(e){{}}}})();</script>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title_plain} — WiseTrack Journal</title>
<meta name="description" content="{summary_safe}" />
<link rel="canonical" href="https://wisetrack.in/{slug}.html" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="WiseTrack" />
<meta property="og:title" content="{title_plain} — WiseTrack Journal" />
<meta property="og:description" content="{summary_safe}" />
<meta property="og:image" content="https://wisetrack.in/assets/og-image.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:url" content="https://wisetrack.in/{slug}.html" />
<meta property="article:published_time" content="{date_iso}" />
<meta property="article:author" content="{author}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title_plain} — WiseTrack Journal" />
<meta name="twitter:description" content="{summary_safe}" />
<meta name="twitter:image" content="https://wisetrack.in/assets/og-image.png" />
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,300..900,30..100,0..1;1,9..144,300..900,30..100,0..1&family=Inter+Tight:wght@300..700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<script src="assets/tailwind-config.js"></script>
<link href="assets/styles.css" rel="stylesheet" />
<script>document.documentElement.classList.add("js")</script>
<script src="assets/site.js" defer></script>
<style>
  .prose p {{ margin-top: 1rem; line-height: 1.75; color: rgba(198, 194, 216, 0.92); }}
  .prose code {{ font-family: "JetBrains Mono", monospace; font-size: 0.9em; background: rgba(255,255,255,0.05); padding: 0.1em 0.4em; border-radius: 4px; border: 1px solid rgba(255,255,255,0.06); }}
  .prose strong {{ color: var(--text); font-weight: 600; }}
</style>
</head>
<body class="bg-bg text-text font-sans antialiased overflow-x-hidden">

{nav}

<main class="relative pt-[120px]">

<!-- Article hero -->
<section class="relative overflow-hidden">
  <div class="absolute inset-0 -z-0 pointer-events-none">
    <div class="aurora animate-drift" style="top:-30%; left:-10%; opacity:.4"></div>
    <div class="absolute inset-0 bp-grid"></div>
    <div class="absolute inset-0 bg-gradient-to-b from-transparent to-bg"></div>
    <div class="grain"></div>
  </div>

  <div class="relative max-w-page mx-auto px-edge pt-12 md:pt-16 pb-16">
    <div class="relative hud hud-cyan p-6 md:p-10 lg:p-14 border border-white/8 rounded-2xl bg-white/[0.015]">
      <div class="absolute top-3 left-6 mono text-[10px] tracking-widest text-muted">FILE&nbsp;·&nbsp;wisetrack.in/{slug}</div>
      <div class="absolute top-3 right-6 mono text-[10px] tracking-widest text-cyan flex items-center gap-2"><span class="h-1.5 w-1.5 rounded-full bg-cyan"></span>JOURNAL&nbsp;/&nbsp;ARTICLE</div>
      <div class="absolute bottom-3 left-6 mono text-[10px] tracking-widest text-muted">{date_human}</div>
      <div class="absolute bottom-3 right-6 mono text-[10px] tracking-widest text-muted">{read}</div>

      <div class="mt-8">
        <a href="blog.html" class="inline-flex items-center gap-2 mono text-[11px] tracking-widest text-muted hover:text-text transition-colors">
          <svg width="12" height="12" viewBox="0 0 14 14" fill="none"><path d="M11 7H3M7 3L3 7l4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
          BACK&nbsp;TO&nbsp;JOURNAL
        </a>
      </div>

      <div class="mt-6 flex items-center gap-3 reveal">
        <span class="tag {tag_color}">{tag}</span>
        <span class="mono text-[11px] tracking-widest text-muted">{date_human}&nbsp;·&nbsp;{author}&nbsp;·&nbsp;{read}</span>
      </div>

      <h1 class="serif text-[clamp(2.4rem,5vw,5rem)] leading-[1] tracking-tight mt-5 reveal" data-delay="80">
        {title_html}
      </h1>

      <p class="mt-6 text-xl text-text-2/85 leading-relaxed max-w-prose reveal" data-delay="160">
        {summary_safe}
      </p>
    </div>
  </div>
</section>

<!-- Article body -->
<section class="relative">
  <div class="max-w-page mx-auto px-edge pb-24 grid grid-cols-12 gap-gutter">
    <aside class="col-span-12 lg:col-span-3 lg:sticky lg:top-36 lg:self-start reveal">
      <div class="mono text-[10px] tracking-widest text-muted mb-4">/CONTENTS</div>
      <ul class="flex flex-col gap-2 text-sm">
{toc_items}
      </ul>
      <div class="hairline-soft my-6"></div>
      <div class="mono text-[10px] tracking-widest text-muted mb-2">SHARE</div>
      <div class="flex gap-3 text-sm text-text-2">
        <a class="hover:text-text" href="https://twitter.com/intent/tweet?text={tweet_text}&url=https://wisetrack.in/{slug}.html" target="_blank" rel="noopener">𝕏</a>
        <a class="hover:text-text" href="https://www.linkedin.com/sharing/share-offsite/?url=https://wisetrack.in/{slug}.html" target="_blank" rel="noopener">LinkedIn</a>
        <a class="hover:text-text" href="mailto:?subject={subject}&body=https://wisetrack.in/{slug}.html">Email</a>
      </div>
    </aside>

    <article class="col-span-12 lg:col-span-9 flex flex-col gap-12 max-w-3xl prose reveal" data-delay="100">
{body}
    </article>
  </div>
</section>

<!-- Author / CTA strip -->
<section class="relative border-t border-white/5">
  <div class="max-w-page mx-auto px-edge py-16 grid grid-cols-12 gap-gutter items-center">
    <div class="col-span-12 md:col-span-7">
      <span class="slug">§ Continue reading</span>
      <h3 class="serif text-2xl md:text-3xl leading-tight tracking-tight mt-3">More from the <span class="serif-italic text-gradient">journal</span>.</h3>
      <p class="mt-3 text-text-2/85">Short pieces on engineering, products, and the work — written when we have something we'd want to read.</p>
    </div>
    <div class="col-span-12 md:col-span-5 md:text-right flex flex-col md:items-end gap-3">
      <a href="blog.html" class="btn-ghost w-fit">All articles <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3 7h8M7 3l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
      <a href="contact.html" class="btn-primary magnetic w-fit">Start a project <svg class="arr" width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3 7h8M7 3l4 4-4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
    </div>
  </div>
</section>

</main>

{footer}

</body>
</html>
"""


def build(post: dict) -> str:
    title_plain = post["title"].rstrip(".")
    iw = post["italic_word"]
    # Render the headline with the italic word highlighted via gradient sweep
    if iw in title_plain:
        title_html = title_plain.replace(
            iw,
            f'<span class="serif-italic text-gradient">{iw}</span>',
            1,
        ) + '<span class="text-violet">.</span>'
    else:
        title_html = title_plain + '<span class="text-violet">.</span>'

    summary_safe = html.escape(post["summary"])
    toc_items = "\n".join(
        f'        <li><a class="text-text-2 hover:text-text" href="#{slug}">{label}</a></li>'
        for slug, label in post["toc"]
    )
    body_parts = []
    for sec_id, num, head, paragraphs in post["sections"]:
        ps = "\n".join(f"        <p>{p}</p>" for p in paragraphs)
        body_parts.append(textwrap.dedent(f"""\
          <section id="{sec_id}">
            <span class="slug">§ {num}</span>
            <h2 class="serif text-3xl md:text-4xl leading-tight tracking-tight mt-2">{head}</h2>
        {ps}
          </section>
        """))
    body = "\n".join(body_parts)

    tweet_text = html.escape(title_plain).replace(" ", "%20")
    subject = html.escape(title_plain).replace(" ", "%20")

    out = TEMPLATE.format(
        title_plain=html.escape(title_plain),
        title_html=title_html,
        summary_safe=summary_safe,
        slug=post["slug"],
        date_iso=post["date_iso"],
        date_human=post["date_human"],
        author=post["author"],
        read=post["read"],
        tag=post["tag"],
        tag_color=post["tag_color"],
        toc_items=toc_items,
        body=body,
        tweet_text=tweet_text,
        subject=subject,
        nav=NAV.format(date_human=post["date_human"], read=post["read"]),
        footer=FOOTER,
    )
    return out


def main():
    for post in POSTS:
        out = build(post)
        path = ROOT / f"{post['slug']}.html"
        path.write_text(out, encoding="utf-8")
        print(f"wrote {path.name}")


if __name__ == "__main__":
    main()
