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
        "tagline": "Custom HRMS Software, Built Around Your Business",
        "italic": "Your Business",
        "blurb": "Every company manages people differently. Instead of forcing your team to adapt to generic HR software, we build a custom HRMS tailored to your workflows, policies, and payroll requirements.\n\nPowered by the production-tested HRMS engine inside Ragenaizer, our solution helps you launch faster while avoiding the complexity of building everything from scratch.",
        "ragenaizer_url": "https://ragenaizer.com/pages/hrms.html",
        "hero_right_card_html": """<div class="col-span-12 lg:col-span-4 reveal" data-delay="120">
          <div class="card p-6 hud hud-lime">
            <div class="mono text-[10px] tracking-widest text-muted">KEY STRENGTHS</div>
            <ul class="mt-4 flex flex-col gap-3.5 text-sm text-text-2/95">
              <li class="flex items-start gap-2.5">
                <span class="text-lime text-base leading-none">✔</span>
                <span>Custom Development</span>
              </li>
              <li class="flex items-start gap-2.5">
                <span class="text-lime text-base leading-none">✔</span>
                <span>Payroll &amp; Compliance Ready</span>
              </li>
              <li class="flex items-start gap-2.5">
                <span class="text-lime text-base leading-none">✔</span>
                <span>Cloud-Based &amp; Scalable</span>
              </li>
              <li class="flex items-start gap-2.5">
                <span class="text-lime text-base leading-none">✔</span>
                <span>Built for Indian &amp; Global Businesses</span>
              </li>
            </ul>
            <a href="contact.html" class="mt-6 inline-flex items-center gap-2 text-lime text-sm hover:underline">
              Book a Free Consultation
              <svg width="12" height="12" viewBox="0 0 14 14" fill="none"><path d="M3 11L11 3M5 3h6v6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </a>
          </div>
        </div>""",
        "capabilities": [
            ("Payroll That Finance Can Trust", "Transparent salary calculations, multiple salary structures, payroll revisions &amp; arrears, bank file generation, statutory deductions, and payroll audit trails.<br/><br/><strong>Result:</strong> Faster payroll cycles with fewer manual errors."),
            ("Attendance That Works Everywhere", "GPS attendance, geofencing, selfie verification, NFC, biometric integration, shift management, overtime tracking, and attendance corrections.<br/><br/><strong>Result:</strong> Accurate attendance without manual follow-ups."),
            ("Leave &amp; Employee Management", "Employees can apply for leave, view payslips, submit expense claims, update personal information, download HR documents, and track approvals.<br/><br/><strong>Result:</strong> Better employee experience with less work for HR."),
            ("Built-In Compliance", "PF, ESI, Professional Tax, TDS, custom statutory rules, and multi-country configurations. Resulting in less compliance risk and easier reporting."),
            ("Built for Growing Businesses", "Multiple branches, departments, cost centres, employee transfers, salary revisions, multi-company operations, and multi-currency payroll. No rebuilding required."),
        ],
        "extra_section_html": """
<!-- Modular Architecture Blueprint Section -->
<section class="relative py-16 md:py-24 bg-gradient-to-b from-transparent via-bg-2/30 to-transparent border-t border-white/5">
  <div class="max-w-page mx-auto px-edge">
    <div class="grid grid-cols-12 gap-gutter mb-12">
      <div class="col-span-12 lg:col-span-6 reveal">
        <span class="slug">§ The Architecture Blueprint</span>
        <h2 class="serif text-[clamp(2.2rem,4.5vw,3.6rem)] leading-[1.05] tracking-tight mt-3">
          16 Core Modules. <span class="serif-italic text-gradient">Fully Customizable.</span>
        </h2>
      </div>
      <p class="col-span-12 lg:col-span-5 lg:col-start-8 self-end text-text-2/85 text-lg leading-relaxed reveal" data-delay="100">
        Every capability, structured for your organization. Choose the exact features your enterprise needs. We adapt every module to your operational rules, without vendor lock-in.
      </p>
    </div>
    
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 reveal">
      <!-- Card 1 -->
      <div class="flex flex-col items-start p-6 bg-white/[0.015] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.03] rounded-2xl transition-all duration-300 group">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo/10 to-violet/10 border border-white/10 shadow-lg flex items-center justify-center text-indigo mb-4 transition-transform group-hover:scale-110">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"/><line x1="9" y1="22" x2="9" y2="16"/><line x1="15" y1="22" x2="15" y2="16"/><line x1="9" y1="16" x2="15" y2="16"/><path d="M16 8h-8V6h8v2zm0 5h-8v-2h8v2z"/></svg>
        </div>
        <h4 class="font-sans font-bold text-base text-text">Payroll</h4>
        <p class="text-xs text-text-2/70 mt-1.5 leading-relaxed">26 states, full statutory</p>
      </div>

      <!-- Card 2 -->
      <div class="flex flex-col items-start p-6 bg-white/[0.015] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.03] rounded-2xl transition-all duration-300 group">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo/10 to-violet/10 border border-white/10 shadow-lg flex items-center justify-center text-indigo mb-4 transition-transform group-hover:scale-110">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="11" r="2.5"/><path d="M3 18c0-3 3-4 6-4s6 1 6 4"/><line x1="15" y1="8" x2="19" y2="8"/><line x1="15" y1="12" x2="19" y2="12"/></svg>
        </div>
        <h4 class="font-sans font-bold text-base text-text">Employee Management</h4>
        <p class="text-xs text-text-2/70 mt-1.5 leading-relaxed">Centralised records</p>
      </div>

      <!-- Card 3 -->
      <div class="flex flex-col items-start p-6 bg-white/[0.015] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.03] rounded-2xl transition-all duration-300 group">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo/10 to-violet/10 border border-white/10 shadow-lg flex items-center justify-center text-indigo mb-4 transition-transform group-hover:scale-110">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22a7 7 0 0 0 7-7c0-4.3-3-7-7-7s-7 2.7-7 7a7 7 0 0 0 7 7zm-3-7a3 3 0 0 1 6 0m-4.5-3.5a1.5 1.5 0 0 1 3 0"/></svg>
        </div>
        <h4 class="font-sans font-bold text-base text-text">Attendance</h4>
        <p class="text-xs text-text-2/70 mt-1.5 leading-relaxed">Biometric, mobile, WFH</p>
      </div>

      <!-- Card 4 -->
      <div class="flex flex-col items-start p-6 bg-white/[0.015] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.03] rounded-2xl transition-all duration-300 group">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo/10 to-violet/10 border border-white/10 shadow-lg flex items-center justify-center text-indigo mb-4 transition-transform group-hover:scale-110">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
        </div>
        <h4 class="font-sans font-bold text-base text-text">Leave Management</h4>
        <p class="text-xs text-text-2/70 mt-1.5 leading-relaxed">Policy-based, multi-tier</p>
      </div>

      <!-- Card 5 -->
      <div class="flex flex-col items-start p-6 bg-white/[0.015] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.03] rounded-2xl transition-all duration-300 group">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo/10 to-violet/10 border border-white/10 shadow-lg flex items-center justify-center text-indigo mb-4 transition-transform group-hover:scale-110">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
        </div>
        <h4 class="font-sans font-bold text-base text-text">Employee Self-Service</h4>
        <p class="text-xs text-text-2/70 mt-1.5 leading-relaxed">Mobile app for teams</p>
      </div>

      <!-- Card 6 -->
      <div class="flex flex-col items-start p-6 bg-white/[0.015] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.03] rounded-2xl transition-all duration-300 group">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo/10 to-violet/10 border border-white/10 shadow-lg flex items-center justify-center text-indigo mb-4 transition-transform group-hover:scale-110">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        </div>
        <h4 class="font-sans font-bold text-base text-text">Applicant Tracking</h4>
        <p class="text-xs text-text-2/70 mt-1.5 leading-relaxed">ATS + digital onboarding</p>
      </div>

      <!-- Card 7 -->
      <div class="flex flex-col items-start p-6 bg-white/[0.015] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.03] rounded-2xl transition-all duration-300 group">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo/10 to-violet/10 border border-white/10 shadow-lg flex items-center justify-center text-indigo mb-4 transition-transform group-hover:scale-110">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        </div>
        <h4 class="font-sans font-bold text-base text-text">Performance Management</h4>
        <p class="text-xs text-text-2/70 mt-1.5 leading-relaxed">KPIs, appraisals, 360°</p>
      </div>

      <!-- Card 8 -->
      <div class="flex flex-col items-start p-6 bg-white/[0.015] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.03] rounded-2xl transition-all duration-300 group">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo/10 to-violet/10 border border-white/10 shadow-lg flex items-center justify-center text-indigo mb-4 transition-transform group-hover:scale-110">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        </div>
        <h4 class="font-sans font-bold text-base text-text">Timesheet</h4>
        <p class="text-xs text-text-2/70 mt-1.5 leading-relaxed">Project &amp; billing hours</p>
      </div>

      <!-- Card 9 -->
      <div class="flex flex-col items-start p-6 bg-white/[0.015] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.03] rounded-2xl transition-all duration-300 group">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo/10 to-violet/10 border border-white/10 shadow-lg flex items-center justify-center text-indigo mb-4 transition-transform group-hover:scale-110">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
        </div>
        <h4 class="font-sans font-bold text-base text-text">HR Policies</h4>
        <p class="text-xs text-text-2/70 mt-1.5 leading-relaxed">Digital policy management</p>
      </div>

      <!-- Card 10 -->
      <div class="flex flex-col items-start p-6 bg-white/[0.015] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.03] rounded-2xl transition-all duration-300 group">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo/10 to-violet/10 border border-white/10 shadow-lg flex items-center justify-center text-indigo mb-4 transition-transform group-hover:scale-110">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1-2-1Z"/><path d="M16 8H8m8 4H8m6 4H8"/></svg>
        </div>
        <h4 class="font-sans font-bold text-base text-text">Expense Management</h4>
        <p class="text-xs text-text-2/70 mt-1.5 leading-relaxed">Claims &amp; reimbursements</p>
      </div>

      <!-- Card 11 -->
      <div class="flex flex-col items-start p-6 bg-white/[0.015] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.03] rounded-2xl transition-all duration-300 group">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo/10 to-violet/10 border border-white/10 shadow-lg flex items-center justify-center text-indigo mb-4 transition-transform group-hover:scale-110">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
        </div>
        <h4 class="font-sans font-bold text-base text-text">Asset Management</h4>
        <p class="text-xs text-text-2/70 mt-1.5 leading-relaxed">Track &amp; assign assets</p>
      </div>

      <!-- Card 12 -->
      <div class="flex flex-col items-start p-6 bg-white/[0.015] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.03] rounded-2xl transition-all duration-300 group">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo/10 to-violet/10 border border-white/10 shadow-lg flex items-center justify-center text-indigo mb-4 transition-transform group-hover:scale-110">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="m16 11 2 2 4-4"/></svg>
        </div>
        <h4 class="font-sans font-bold text-base text-text">Visitor Management</h4>
        <p class="text-xs text-text-2/70 mt-1.5 leading-relaxed">Digital visitor register</p>
      </div>

      <!-- Card 13 -->
      <div class="flex flex-col items-start p-6 bg-white/[0.015] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.03] rounded-2xl transition-all duration-300 group">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo/10 to-violet/10 border border-white/10 shadow-lg flex items-center justify-center text-indigo mb-4 transition-transform group-hover:scale-110">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c0 2 2.7 3.5 6 3.5s6-1.5 6-3.5v-5"/></svg>
        </div>
        <h4 class="font-sans font-bold text-base text-text">Training &amp; Development</h4>
        <p class="text-xs text-text-2/70 mt-1.5 leading-relaxed">Structured learning paths</p>
      </div>

      <!-- Card 14 -->
      <div class="flex flex-col items-start p-6 bg-white/[0.015] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.03] rounded-2xl transition-all duration-300 group">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo/10 to-violet/10 border border-white/10 shadow-lg flex items-center justify-center text-indigo mb-4 transition-transform group-hover:scale-110">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
        </div>
        <h4 class="font-sans font-bold text-base text-text">HR Reports</h4>
        <p class="text-xs text-text-2/70 mt-1.5 leading-relaxed">Real-time analytics</p>
      </div>

      <!-- Card 15 -->
      <div class="flex flex-col items-start p-6 bg-white/[0.015] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.03] rounded-2xl transition-all duration-300 group">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo/10 to-violet/10 border border-white/10 shadow-lg flex items-center justify-center text-indigo mb-4 transition-transform group-hover:scale-110">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18.36 6.64a9 9 0 0 1 0 12.72M6.34 17.66a9 9 0 0 1 0-12.72M2 12h3m14 0h3m-10-7v3m0 8v3"/></svg>
        </div>
        <h4 class="font-sans font-bold text-base text-text">Integrations</h4>
        <p class="text-xs text-text-2/70 mt-1.5 leading-relaxed">Biometric, ERP &amp; more</p>
      </div>

      <!-- Card 16 -->
      <div class="flex flex-col items-start p-6 bg-white/[0.015] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.03] rounded-2xl transition-all duration-300 group">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo/10 to-violet/10 border border-white/10 shadow-lg flex items-center justify-center text-indigo mb-4 transition-transform group-hover:scale-110">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        </div>
        <h4 class="font-sans font-bold text-base text-text">Survey Software</h4>
        <p class="text-xs text-text-2/70 mt-1.5 leading-relaxed">Employee feedback surveys</p>
      </div>
    </div>
  </div>
</section>

<!-- Why Companies Choose Wisetrack Section -->
<section class="relative py-16 md:py-24 bg-gradient-to-b from-transparent via-bg-2/20 to-transparent border-t border-white/5">
  <div class="max-w-page mx-auto px-edge">
    <div class="grid grid-cols-12 gap-gutter items-start">
      <!-- Left Column -->
      <div class="col-span-12 lg:col-span-5 reveal">
        <span class="slug">§ WHY WISETRACK</span>
        <h2 class="serif text-[clamp(2.2rem,4.5vw,3.6rem)] leading-[1.05] tracking-tight mt-3">
          Why Companies Choose <span class="serif-italic text-gradient">Wisetrack</span>
        </h2>
        <p class="mt-6 text-text-2/85 text-base leading-relaxed">
          We don't start from scratch. Your HRMS is built on <strong>Ragenaizer</strong>, our production-tested enterprise platform that already powers complex payroll, HR, and workflow systems.
        </p>
        <p class="mt-4 text-text-2/85 text-base leading-relaxed">
          This gives you faster delivery, lower risk, and software built specifically around your business.
        </p>
        
        <!-- Powered By Card -->
        <div class="mt-8 p-4 bg-white/[0.02] border border-white/5 rounded-xl flex items-center gap-4 max-w-sm">
          <div class="w-12 h-12 rounded-xl bg-violet/10 border border-violet/20 flex items-center justify-center text-violet font-bold text-xl shadow-inner flex-shrink-0">
            R
          </div>
          <div>
            <div class="mono text-[9px] tracking-widest text-muted">POWERED BY</div>
            <div class="font-sans font-bold text-sm text-text">Ragenaizer</div>
            <div class="text-xs text-text-2/70 mt-0.5">Our enterprise platform for HR, Payroll &amp; Workflow automation.</div>
          </div>
        </div>
        
        <!-- Action Button -->
        <div class="mt-8">
          <a href="methodology.html" class="btn-primary magnetic w-fit flex items-center gap-2">
            See How We Build
            <svg class="arr" width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3 7h8M7 3l4 4-4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </a>
        </div>
      </div>
      
      <!-- Right Column (Grid of 6 Cards) -->
      <div class="col-span-12 lg:col-span-7 reveal lg:pl-6 mt-12 lg:mt-0">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
          <!-- Card 1: 40-60% Faster Delivery -->
          <div class="flex flex-col items-start p-6 bg-white/[0.015] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.03] rounded-2xl transition-all duration-300 group">
            <div class="w-12 h-12 rounded-xl bg-indigo/5 border border-indigo/10 flex items-center justify-center text-indigo mb-4 transition-transform group-hover:scale-110">
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2.5 3.19-2.5 5.5h20c0-2.31-1-4.24-2.5-5.5M12 2C7.58 2 4 5.58 4 10c0 4.42 3.58 8 8 8s8-3.58 8-8c0-4.42-3.58-8-8-8z"/><path d="M12 6v8M9 9h6"/></svg>
            </div>
            <h4 class="font-sans font-bold text-sm text-text">40–60% Faster Delivery</h4>
            <p class="text-xs text-text-2/70 mt-1.5 leading-relaxed">Production-ready foundation instead of building everything from scratch.</p>
          </div>
          
          <!-- Card 2: Lower Project Risk -->
          <div class="flex flex-col items-start p-6 bg-white/[0.015] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.03] rounded-2xl transition-all duration-300 group">
            <div class="w-12 h-12 rounded-xl bg-indigo/5 border border-indigo/10 flex items-center justify-center text-indigo mb-4 transition-transform group-hover:scale-110">
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 11 2 2 4-4"/></svg>
            </div>
            <h4 class="font-sans font-bold text-sm text-text">Lower Project Risk</h4>
            <p class="text-xs text-text-2/70 mt-1.5 leading-relaxed">Core HR, payroll and workflow engines are already tested in production.</p>
          </div>
          
          <!-- Card 3: Built Around Your Business -->
          <div class="flex flex-col items-start p-6 bg-white/[0.015] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.03] rounded-2xl transition-all duration-300 group">
            <div class="w-12 h-12 rounded-xl bg-indigo/5 border border-indigo/10 flex items-center justify-center text-indigo mb-4 transition-transform group-hover:scale-110">
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/></svg>
            </div>
            <h4 class="font-sans font-bold text-sm text-text">Built Around Your Business</h4>
            <p class="text-xs text-text-2/70 mt-1.5 leading-relaxed">Your approvals, payroll rules, attendance policies and workflows — your way.</p>
          </div>
          
          <!-- Card 4: Enterprise Integrations -->
          <div class="flex flex-col items-start p-6 bg-white/[0.015] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.03] rounded-2xl transition-all duration-300 group">
            <div class="w-12 h-12 rounded-xl bg-indigo/5 border border-indigo/10 flex items-center justify-center text-indigo mb-4 transition-transform group-hover:scale-110">
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22v-4h3a2 2 0 0 0 2-2v-3h4v-3H17v-3a2 2 0 0 0-2-2h-3V1H9v4H6a2 2 0 0 0-2 2v3H1v3h3v3a2 2 0 0 0 2 2h3v4h3Z"/></svg>
            </div>
            <h4 class="font-sans font-bold text-sm text-text">Enterprise Integrations</h4>
            <p class="text-xs text-text-2/70 mt-1.5 leading-relaxed">Seamless integration with ERP, biometric devices, accounting software and third-party APIs.</p>
          </div>
          
          <!-- Card 5: Scales With Your Growth -->
          <div class="flex flex-col items-start p-6 bg-white/[0.015] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.03] rounded-2xl transition-all duration-300 group">
            <div class="w-12 h-12 rounded-xl bg-indigo/5 border border-indigo/10 flex items-center justify-center text-indigo mb-4 transition-transform group-hover:scale-110">
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
            </div>
            <h4 class="font-sans font-bold text-sm text-text">Scales With Your Growth</h4>
            <p class="text-xs text-text-2/70 mt-1.5 leading-relaxed">From 100 employees to 10,000+, the platform grows with your organization.</p>
          </div>
          
          <!-- Card 6: You Own The Software -->
          <div class="flex flex-col items-start p-6 bg-white/[0.015] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.03] rounded-2xl transition-all duration-300 group">
            <div class="w-12 h-12 rounded-xl bg-indigo/5 border border-indigo/10 flex items-center justify-center text-indigo mb-4 transition-transform group-hover:scale-110">
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
            </div>
            <h4 class="font-sans font-bold text-sm text-text">You Own The Software</h4>
            <p class="text-xs text-text-2/70 mt-1.5 leading-relaxed">Full ownership of source code with no vendor lock-in or monthly SaaS limitations.</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Bottom Strip -->
    <div class="mt-12 p-6 bg-white/[0.01] border border-white/5 rounded-2xl flex flex-col lg:flex-row justify-between items-center gap-6 reveal">
      <div class="flex items-center gap-4 flex-1">
        <div class="w-12 h-12 rounded-full bg-violet/10 flex items-center justify-center text-violet flex-shrink-0">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        </div>
        <div>
          <p class="text-xs text-text-2/70 leading-relaxed">Most software companies spend months rebuilding standard HR features.</p>
          <p class="text-sm font-bold text-violet mt-0.5">We start with a production-tested foundation and customize only what makes your business unique.</p>
        </div>
      </div>
      
      <div class="h-[1px] w-full lg:h-12 lg:w-[1px] bg-white/5"></div>
      
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-6 flex-shrink-0 w-full lg:w-auto">
        <div class="flex items-center gap-2.5">
          <svg class="w-4 h-4 text-cyan" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          <div>
            <div class="text-[10px] font-bold text-text">Faster</div>
            <div class="text-[9px] text-muted tracking-wide">Time to Value</div>
          </div>
        </div>
        <div class="flex items-center gap-2.5">
          <svg class="w-4 h-4 text-lime" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 11 2 2 4-4"/></svg>
          <div>
            <div class="text-[10px] font-bold text-text">Lower</div>
            <div class="text-[9px] text-muted tracking-wide">Risk</div>
          </div>
        </div>
        <div class="flex items-center gap-2.5">
          <div class="text-xs font-bold text-violet w-4 h-4 flex items-center justify-center bg-violet/10 rounded-full">₹</div>
          <div>
            <div class="text-[10px] font-bold text-text">Better</div>
            <div class="text-[9px] text-muted tracking-wide">ROI</div>
          </div>
        </div>
        <div class="flex items-center gap-2.5">
          <svg class="w-4 h-4 text-cyan" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/></svg>
          <div>
            <div class="text-[10px] font-bold text-text">Proven</div>
            <div class="text-[9px] text-muted tracking-wide">Results</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
""",
        "hard_problems": [
            "Time-zone-correct attendance across a workforce distributed across regions, including DST edges.",
            "Retroactive salary revisions inside a closed period — without breaking statutory filings or audit trails.",
            "Per-component proration when an employee transfers mid-month between locations / cost centres / pay scales.",
            "Multi-currency CTC with home-currency payslip generation and accurate FX accounting on settlement.",
            "Statutory ceiling changes mid-year (the kind of thing the government does in March), applied without forcing a re-run on every closed period.",
        ],
        "stack": "ASP.NET Core services, Postgres, an event-sourced ledger for payroll, separate read models for reporting. Single tenant or multi-tenant, your call. Deploys on Docker / Linux.",
        "cta_slug": "Get Started",
        "cta_headline_html": "Ready to Build an HRMS That <span class=\"serif-italic text-gradient\">Fits Your Business</span>?",
        "cta_blurb": "Whether you're replacing spreadsheets, upgrading legacy software, or building a custom HR platform from scratch, we'll help you design a solution that matches your workflows, payroll policies, and business goals.<br/><br/><strong>Let's build your HRMS together.</strong>",
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
    <div class="flex items-center gap-3"><span class="h-1.5 w-1.5 rounded-full bg-mint animate-pulse"></span><span class="hidden sm:inline">CAPABILITIES · CUSTOM BUILD</span><span class="sm:hidden">CAPABILITIES</span></div>
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
                  <svg class="w-5 h-5 text-violet group-hover/card:scale-110 transition-transform duration-200" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
                  <div class="text-sm font-bold text-text">HRMS & Payroll</div>
                </div>
                <p class="text-xs text-text-2/70 leading-relaxed mb-3">Statutory Indian payroll compliance, tax filing, geofenced attendance.</p>
                <span class="text-[10px] font-bold text-indigo tracking-wider font-mono">EXPLORE MODULE &rarr;</span>
              </a>
              <a href="crm-sales.html" class="block p-4 bg-white/[0.01] border border-white/5 hover:border-mint/30 hover:bg-white/[0.02] rounded-xl transition-all duration-200 group/card">
                <div class="flex items-center gap-3.5 mb-2">
                  <svg class="w-5 h-5 text-mint group-hover/card:scale-110 transition-transform duration-200" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>
                  <div class="text-sm font-bold text-text">CRM & Sales</div>
                </div>
                <p class="text-xs text-text-2/70 leading-relaxed mb-3">Pipeline mapping, lead forms integration, client record sharing.</p>
                <span class="text-[10px] font-bold text-indigo tracking-wider font-mono">EXPLORE MODULE &rarr;</span>
              </a>
              <a href="build-pms.html" class="block p-4 bg-white/[0.01] border border-white/5 hover:border-indigo/30 hover:bg-white/[0.02] rounded-xl transition-all duration-200 group/card">
                <div class="flex items-center gap-3.5 mb-2">
                  <svg class="w-5 h-5 text-indigo group-hover/card:scale-110 transition-transform duration-200" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path></svg>
                  <div class="text-sm font-bold text-text">PMS & Projects</div>
                </div>
                <p class="text-xs text-text-2/70 leading-relaxed mb-3">Milestone tracking, engineering bug manager, timesheets & billing.</p>
                <span class="text-[10px] font-bold text-indigo tracking-wider font-mono">EXPLORE MODULE &rarr;</span>
              </a>
              <a href="build-lms.html" class="block p-4 bg-white/[0.01] border border-white/5 hover:border-cyan/30 hover:bg-white/[0.02] rounded-xl transition-all duration-200 group/card">
                <div class="flex items-center gap-3.5 mb-2">
                  <svg class="w-5 h-5 text-cyan group-hover/card:scale-110 transition-transform duration-200" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M22 10v6M2 10l10-5 10 5-10 5z"></path><path d="M6 12v5c0 2 2 3 6 3s6-1 6-3v-5"></path></svg>
                  <div class="text-sm font-bold text-text">LMS & Training</div>
                </div>
                <p class="text-xs text-text-2/70 leading-relaxed mb-3">Structured employee training, compliance testing, digital certificates.</p>
                <span class="text-[10px] font-bold text-indigo tracking-wider font-mono">EXPLORE MODULE &rarr;</span>
              </a>
              <a href="build-accounts.html" class="block p-4 bg-white/[0.01] border border-white/5 hover:border-lime/30 hover:bg-white/[0.02] rounded-xl transition-all duration-200 group/card">
                <div class="flex items-center gap-3.5 mb-2">
                  <svg class="w-5 h-5 text-lime group-hover/card:scale-110 transition-transform duration-200" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1-2-1z"></path><path d="M16 8H8m8 4H8m6 4H8"></path></svg>
                  <div class="text-sm font-bold text-text">Double-Entry Accounts</div>
                </div>
                <p class="text-xs text-text-2/70 leading-relaxed mb-3">Ledger sync, automated invoicing, expenses, cashflow analysis.</p>
                <span class="text-[10px] font-bold text-indigo tracking-wider font-mono">EXPLORE MODULE &rarr;</span>
              </a>
              <a href="build-chat.html" class="block p-4 bg-white/[0.01] border border-white/5 hover:border-sky/30 hover:bg-white/[0.02] rounded-xl transition-all duration-200 group/card">
                <div class="flex items-center gap-3.5 mb-2">
                  <svg class="w-5 h-5 text-sky group-hover/card:scale-110 transition-transform duration-200" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
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
                  <svg class="w-5 h-5 text-violet group-hover/card:scale-110 transition-transform duration-200" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
                  <div class="text-sm font-bold text-text">Custom Web & OS Software</div>
                </div>
                <p class="text-xs text-text-2/70 leading-relaxed mb-1">C#, .NET Core, Blazor, Postgres. Scalable business architecture.</p>
              </a>
              <a href="custom-services.html#mobile-apps" class="block p-4 bg-white/[0.01] border border-white/5 hover:border-lime/30 hover:bg-white/[0.02] rounded-xl transition-all duration-200 group/card">
                <div class="flex items-center gap-3.5 mb-2">
                  <svg class="w-5 h-5 text-lime group-hover/card:scale-110 transition-transform duration-200" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"></rect><line x1="12" y1="18" x2="12.01" y2="18"></line></svg>
                  <div class="text-sm font-bold text-text">Mobile Applications</div>
                </div>
                <p class="text-xs text-text-2/70 leading-relaxed mb-1">Native iOS & Android apps mapped to central business databases.</p>
              </a>
              <a href="custom-services.html#ai-automation" class="block p-4 bg-white/[0.01] border border-white/5 hover:border-mint/30 hover:bg-white/[0.02] rounded-xl transition-all duration-200 group/card">
                <div class="flex items-center gap-3.5 mb-2">
                  <svg class="w-5 h-5 text-mint group-hover/card:scale-110 transition-transform duration-200" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="10" rx="2"></rect><circle cx="12" cy="5" r="2"></circle><path d="M12 7v4m-4 5h8M8 12V9a4 4 0 0 1 8 0v3"></path></svg>
                  <div class="text-sm font-bold text-text">Agentic AI Solutions</div>
                </div>
                <p class="text-xs text-text-2/70 leading-relaxed mb-1">Production agent loops using Claude 3.5, RAG, and ClickHouse.</p>
              </a>
              <a href="custom-services.html#dashboards" class="block p-4 bg-white/[0.01] border border-white/5 hover:border-sky/30 hover:bg-white/[0.02] rounded-xl transition-all duration-200 group/card">
                <div class="flex items-center gap-3.5 mb-2">
                  <svg class="w-5 h-5 text-sky group-hover/card:scale-110 transition-transform duration-200" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
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
      <div class="col-span-6 md:col-span-3 lg:col-span-2 lg:col-start-6"><div class="mono text-[11px] tracking-widest text-muted mb-5">EXPLORE</div><ul class="flex flex-col gap-3 text-text-2"><li><a href="solutions.html" class="hover:text-text">Solutions</a></li><li><a href="portfolio.html" class="hover:text-text">Work</a></li><li><a href="methodology.html" class="hover:text-text">Method</a></li><li><a href="blog.html" class="hover:text-text">Journal</a></li></ul></div>
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
<html lang="en">
<head>
<script>(function(){{try{{if(localStorage.getItem("theme")!=="dark"){{document.documentElement.classList.add("light");}}else{{document.documentElement.classList.remove("light");}}}}catch(e){{}}}})();</script>
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
            {case_study_btn}
            <a href="{ragenaizer_url}" target="_blank" rel="noopener" class="btn-ghost">See it shipped <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3 11L11 3M5 3h6v6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
          </div>
        </div>

        {hero_right_card_html}
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

{extra_section_html}

<!-- Hard problems -->
<section class="relative bg-gradient-to-b from-transparent via-bg-2/40 to-transparent border-y border-white/5 py-16 md:py-24">
  <div class="max-w-page mx-auto px-edge">
    <div class="grid grid-cols-12 gap-gutter">
      <div class="col-span-12 md:col-span-5 reveal">
        <span class="slug">§ {hard_slug}</span>
        <h2 class="serif text-[clamp(2rem,4vw,3rem)] leading-[1] tracking-tight mt-3">
          {hard_headline_html}
        </h2>
        <p class="mt-5 text-text-2/85 leading-relaxed">
          {hard_blurb}
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
          <span class="slug">§ {cta_slug}</span>
          <h2 class="serif text-[clamp(2rem,4.5vw,3.6rem)] leading-[1.02] tracking-tight mt-4">
            {cta_headline_html}
          </h2>
          <p class="mt-5 max-w-prose text-text-2/85 text-lg">
            {cta_blurb}
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

    # Hero Right Card
    hero_right_card_html = s.get("hero_right_card_html")
    if not hero_right_card_html:
        hero_right_card_html = f"""<div class="col-span-12 lg:col-span-4 reveal" data-delay="120">
          <div class="card p-6 hud hud-lime">
            <div class="mono text-[10px] tracking-widest text-muted">PROOF&nbsp;OF&nbsp;CAPABILITY</div>
            <div class="serif text-2xl mt-3 leading-tight">Ragenaizer · {html.escape(module_short)}</div>
            <p class="mt-3 text-sm text-text-2/85">A production-grade {html.escape(module_lower)} module already built and running. We ship a custom one for clients who need their own.</p>
            <a href="{s['ragenaizer_url']}" target="_blank" rel="noopener" class="mt-4 inline-flex items-center gap-2 text-lime text-sm">
              ragenaizer.com / {html.escape(module_lower)}
              <svg width="12" height="12" viewBox="0 0 14 14" fill="none"><path d="M3 11L11 3M5 3h6v6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
            </a>
          </div>
        </div>"""

    # Hard Problems
    hard_slug = s.get("hard_slug", "The hard bits")
    hard_headline_html = s.get("hard_headline_html")
    if not hard_headline_html:
        hard_title = s.get("hard_title", "The problems that [don't] show up in the demo.")
        hard_italic = s.get("hard_italic", "don't")
        if hard_italic in hard_title:
            hard_headline_html = hard_title.replace(
                hard_italic, f'<span class="serif-italic text-gradient-cool">{hard_italic}</span>', 1
            ).replace("[", "").replace("]", "")
        else:
            hard_headline_html = hard_title
    
    hard_blurb = s.get("hard_blurb", "These are the ones that take a custom build from \"works in a screenshot\" to \"works in production for three years.\" We've already learned them once.")

    # CTA
    cta_slug = s.get("cta_slug", "Next step")
    cta_headline_html = s.get("cta_headline_html")
    if not cta_headline_html:
        cta_title = f"Custom {module_lower}? [Tell us what you need.]"
        cta_italic = "Tell us what you need."
        cta_headline_html = cta_title.replace(
            cta_italic, f'<span class="serif-italic text-gradient">{cta_italic}</span>', 1
        ).replace("[", "").replace("]", "")
    
    cta_blurb = s.get("cta_blurb", "One conversation. We tell you whether it's a custom build, a Ragenaizer rollout, or something we shouldn't take on.")

    # Escaping blurbs for safety
    blurb_escaped = html.escape(s["blurb"]).replace("\n", "<br/>")

    case_study_btn = ""
    if s["slug"] in ["crm", "hrms", "pms"]:
        case_study_btn = f'<a href="{s["slug"]}-case-study.html" class="btn-ghost">Case Study &rarr;</a>'

    return TEMPLATE.format(
        slug=s["slug"],
        code=s["code"],
        module_plain=html.escape(module_plain),
        module_short=html.escape(module_short),
        module_upper=html.escape(module_upper),
        module_lower=html.escape(module_lower),
        headline_html=headline_html,
        blurb=blurb_escaped,
        description=html.escape(s["blurb"].split("\n")[0]),
        ragenaizer_url=s["ragenaizer_url"],
        hero_right_card_html=hero_right_card_html,
        capability_cards="\n".join(cap_card(i, n, d) for i, (n, d) in enumerate(s["capabilities"])),
        hard_slug=html.escape(hard_slug),
        hard_headline_html=hard_headline_html,
        hard_blurb=hard_blurb,
        hard_problems_list="\n".join(hard_item(i, t) for i, t in enumerate(s["hard_problems"])),
        stack=html.escape(s["stack"]),
        cta_slug=html.escape(cta_slug),
        cta_headline_html=cta_headline_html,
        cta_blurb=cta_blurb,
        extra_section_html=s.get("extra_section_html", ""),
        case_study_btn=case_study_btn,
        nav=NAV,
        footer=FOOTER,
    )


def main():
    for s in SERVICES:
        path = ROOT / f"build-{s['slug']}.html"
        path.write_text(build(s), encoding="utf-8")
        print(f"wrote {path.name}")


if __name__ == "__main__":
    main()
