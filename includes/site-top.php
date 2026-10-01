<?php
if (!defined('WISETRACK')) { http_response_code(403); exit; }
?>
<body class="bg-bg text-text font-sans antialiased overflow-x-hidden">
  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-P32QMPCK"
  height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <!-- End Google Tag Manager (noscript) -->

  <!-- Scroll progress -->
  <div class="fixed top-0 left-0 right-0 h-[2px] z-[80] origin-left scale-x-0 bg-gradient-to-r from-violet via-indigo to-cyan" data-progress></div>

  <!-- Top Announcement Bar -->
  <div class="fixed top-0 left-0 right-0 z-[70] bg-bg/85 backdrop-blur-xl border-b border-white/5">
    <div class="max-w-page mx-auto px-edge h-9 flex items-center justify-between text-[11px] mono tracking-wider text-muted">
      <div class="flex items-center gap-3">
        <span class="h-1.5 w-1.5 rounded-full bg-mint animate-pulse"></span>
        <span class="hidden sm:inline"><?= e($topbarDesktop ?? 'OPEN · accepting new engagements / Q1–Q2 2026') ?></span>
        <span class="sm:hidden"><?= e($topbarMobile ?? 'OPEN · Q1–Q2 2026') ?></span>
      </div>
      <div class="flex items-center gap-5">
        <span class="hidden md:inline">Noida, IN</span>
        <span data-clock>--:--:-- IST</span>
      </div>
    </div>
  <!-- Primary nav -->
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
                <a href="custom-web-os-software.html" class="block p-4 bg-white/[0.01] border border-white/5 hover:border-violet/30 hover:bg-white/[0.02] rounded-xl transition-all duration-200 group/card">
                  <div class="flex items-center gap-3.5 mb-2">
                    <svg class="w-5 h-5 text-violet group-hover/card:scale-110 transition-transform duration-200" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
                    <div class="text-sm font-bold text-text">Custom Web & OS Software</div>
                  </div>
                  <p class="text-xs text-text-2/70 leading-relaxed mb-1">C#, .NET Core, Blazor, Postgres. Scalable business architecture.</p>
                </a>
                <a href="mobile-app.html" class="block p-4 bg-white/[0.01] border border-white/5 hover:border-lime/30 hover:bg-white/[0.02] rounded-xl transition-all duration-200 group/card">
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

        <a href="portfolio.html" class="hover:text-text transition-colors">Work</a>
        <a href="blog.html" class="text-text hover:text-text transition-colors font-bold">Blog</a>
        <a href="careers.html" class="hover:text-text transition-colors">Careers</a>
        <a href="contact.html" class="hover:text-text transition-colors">Contact</a>
      </div>

      <div class="flex items-center gap-3">
        <a href="contact.html" class="btn-primary hidden sm:flex items-center gap-2 text-xs font-semibold py-2 px-4 rounded-lg bg-indigo text-white hover:opacity-90 transition-all">
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
            <a class="py-2 px-3 block text-sm border-l border-white/5 text-text-2 hover:text-text" href="custom-web-os-software.html">Custom Web Development</a>
            <a class="py-2 px-3 block text-sm border-l border-white/5 text-text-2 hover:text-text" href="mobile-app.html">Mobile Applications</a>
            <a class="py-2 px-3 block text-sm border-l border-white/5 text-text-2 hover:text-text" href="custom-services.html#ai-automation">Agentic AI Loops</a>
            <a class="py-2 px-3 block text-sm border-l border-white/5 text-text-2 hover:text-text" href="custom-services.html#dashboards">Custom Dashboards</a>
          </div>
        </details>
        <a href="portfolio.html" class="py-2 hover:text-text">Work</a>
        <a href="blog.html" class="py-2 hover:text-text font-bold">Blog</a>
        <a href="careers.html" class="py-2 hover:text-text">Careers</a>
        <a href="contact.html" class="py-2 hover:text-text">Contact</a>
        <a href="contact.html" class="btn-primary w-fit mt-2">Start a Project</a>
  </header>
