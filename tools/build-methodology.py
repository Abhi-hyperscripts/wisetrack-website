#!/usr/bin/env python3
"""Builds methodology.html: the Vastu chakra scene (assets/method/src/scene.html) inside the site shell,
   with the copy rewritten for Wisetrack's build process.   python3 tools/build-methodology.py"""
import re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
scene = open(f'{ROOT}/assets/method/src/scene.html', encoding='utf-8').read()
shell = open(f'{ROOT}/methodology.html', encoding='utf-8').read() if not os.path.exists(f'{ROOT}/assets/method/src/shell.html') else open(f'{ROOT}/assets/method/src/shell.html', encoding='utf-8').read()
if not os.path.exists(f'{ROOT}/assets/method/src/shell.html'):
    open(f'{ROOT}/assets/method/src/shell.html', 'w', encoding='utf-8').write(shell)
home_src = open(f'{ROOT}/assets/home/src/home.html', encoding='utf-8').read()
mark_svg = re.search(r'<svg class="mk".*?</svg>', home_src, re.S).group(0).replace('class="mk" aria-hidden="true" focusable="false"', 'class="mark" aria-hidden="true"').replace('fill="currentColor"', '')

# ---------------------------------------------------------------- CSS, scoped under #method
css = scene[scene.index('<style>') + 7:scene.index('</style>')]
css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
def sel_map(sel):
    out = []
    for s in sel.split(','):
        s = s.strip()
        if s in ('html', 'a'): continue
        if s == 'body': s = '#method'
        elif s.startswith(':root'): s = '#method' + s[5:]
        elif s.startswith('.go') or s.startswith('.no-gl'): s = '#method' + s
        elif s.startswith('footer'): continue
        else: s = '#method ' + s
        out.append(s)
    return ', '.join(out)
def namespace(block_css):
    out = []
    for b in re.split(r'(?<=\})', block_css):
        if not b.strip(): continue
        m = re.match(r'\s*([^{]+)\{', b, flags=re.S)
        if not m: out.append(b); continue
        sel = m.group(1).strip()
        ns = sel_map(sel)
        if not ns: continue
        body = b[m.end():]
        if sel == 'body': body = body.replace('margin: 0;', '').replace('background: var(--bg);', '')
        out.append(ns + ' {' + body)
    return ''.join(out)
pos, ns = 0, ''
for m in re.finditer(r'@(media|keyframes)[^{]*\{', css):
    ns += namespace(css[pos:m.start()])
    depth, i = 1, m.end()
    while depth and i < len(css):
        depth += {'{': 1, '}': -1}.get(css[i], 0); i += 1
    inner = css[m.end():i - 1]
    ns += css[m.start():m.end()] + (inner if m.group(1) == 'keyframes' else namespace(inner)) + '}\n'
    pos = i
ns += namespace(css[pos:])
ns += '''
#method { position: relative; font-family: var(--body); font-size: 16px; line-height: 1.55; color: var(--fg); }
#method .sound-fab { position: fixed; left: 22px; bottom: 22px; z-index: 20; background: var(--card); backdrop-filter: blur(10px); opacity: 0; transition: opacity 1s ease 3.2s, border-color .3s, color .3s; }
#method.go .sound-fab { opacity: 1; }
#method .preloader-mark { width: 92px; height: 61px; fill: #7d1426; opacity: 0; animation: fadeUp 0.9s cubic-bezier(0.2, 0.8, 0.2, 1) 0.1s forwards; }
#method .pill.primary:hover { color: var(--btn-fg); }
#method .cta { display: flex; align-items: center; flex-wrap: wrap; gap: clamp(16px, 4vw, 64px); }
#method .cta .copy { flex: 0 1 34rem; }
#method .team { flex: 1 1 320px; min-width: 0; max-width: 720px; margin: 0 clamp(0px, 5vw, 96px) 0 0; padding: 22px 22px 16px; border-radius: 22px; background: var(--card); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid var(--line); box-shadow: 0 30px 80px rgba(110,30,35,0.10); transition: background-color .9s ease, border-color .9s ease; }
#method .team canvas { width: 100%; display: block; }
#method .team figcaption { margin-top: 12px; font-size: 10.5px; letter-spacing: 0.22em; text-transform: uppercase; color: var(--fg-2); text-align: right; }
@media (max-width: 760px) { #method .team { margin-right: 0; max-width: 100%; flex-basis: 100%; } #method .team figcaption { text-align: left; } }
'''

# ---------------------------------------------------------------- JS, retargeted
js = scene[scene.rindex('<script>') + 8:scene.rindex('</script>')]
def R(a, b, n=1):
    global js
    assert js.count(a) == n, (a[:70], js.count(a)); js = js.replace(a, b)
R("var root = document.documentElement;", "var root = document.getElementById('method'), siteRoot = document.documentElement;")
R("if (phaseNight) root.setAttribute('data-phase', 'night'); else root.removeAttribute('data-phase'); }",
  "if (phaseNight) root.setAttribute('data-phase', 'night'); else root.removeAttribute('data-phase'); siteRoot.classList.toggle('light', !phaseNight); }")
R("'apg.sound'", "'wt.sound'", js.count("'apg.sound'"))
R("var ELEMENT = ['water','water','water','air','air','air','fire','fire','fire','earth','earth','space','space','space','space','water'];",
  "var ELEMENT = ['data','data','data','web','web','web','mobile','mobile','mobile','AI','AI','ops','ops','ops','ops','data'];")
R("return AREAS[i] > HI ? 'Extended' : AREAS[i] < LO ? 'Cut' : 'Balanced';", "return AREAS[i] > HI ? 'Built from scratch' : AREAS[i] < LO ? 'Configured' : 'Standard';")
R("AREAS[idx].toFixed(1) + ' sq ft · '", "AREAS[idx].toFixed(1) + ' hrs · '")
R("[['Living', [-0.22, -0.26]], ['Kitchen', [0.22, -0.36]], ['Pooja', [0.22, -0.08]], ['Bedroom', [-0.27, 0.25]], ['Study', [0.04, 0.25]]]",
  "[['Sales', [-0.22, -0.26]], ['Accounts', [0.22, -0.36]], ['HR', [0.22, -0.08]], ['Stores', [-0.27, 0.25]], ['Projects', [0.04, 0.25]]]")
R("x.fillText('MAIN DOOR', q2[0], q2[1] + 10);", "x.fillText('ORDER ENTRY', q2[0], q2[1] + 10);")
R("page === 1 ? 'Vastu Chakra · Aira Hennur shop' : 'Zone balance · 16 zones'", "page === 1 ? 'Scope sheet · Northline Traders' : 'Effort balance · 16 workstreams'")
R("page === 1 ? 'DOOR READING 253°  ·  PLAN TOP FACES WSW  ·  16 OCT 2026' : 'SQ FT  ·  OUTSIDE FACE OF WALLS  ·  AVG 22.2'",
  "page === 1 ? 'KICKOFF 16 OCT 2026  ·  12 WEEKS  ·  FIXED PRICE' : 'HOURS PER FORTNIGHT  ·  SIXTEEN WORKSTREAMS  ·  AVG 22.2'")
R("x.fillText('N  253°', 36, 760); x.fillText('Acharya Pankit Goyal', 36, 790);", "x.fillText('SPRINT 1  ·  WEEK 1 OF 12', 36, 760); x.fillText('Wisetrack Technologies · Noida', 36, 790);")
R("x.fillText('16 zones · 32 entrances · indicative', 36, 816);", "x.fillText('16 workstreams · 32 milestones · indicative', 36, 816);")
R("AREAS[row].toFixed(1) + ' sq ft'", "AREAS[row].toFixed(1) + ' hrs'")
R("AREAS[row + 8].toFixed(1) + ' sq ft'", "AREAS[row + 8].toFixed(1) + ' hrs'")
R("x.fillText('Powered by Wisetrack Technologies', 584, 860);", "x.fillText('wisetrack.in  ·  how we build', 584, 860);")

team_js = r"""
  // ---------- the team, in particles: a 2D stipple of the photo that gathers as the last chapter arrives ----------
  (function () {
    var sec = document.getElementById('cta'), cv = document.getElementById('teamc'); if (!sec || !cv) return;
    var root = document.getElementById('method'), reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches, isMobile = Math.min(window.innerWidth, window.innerHeight) < 760;
    function fit(v, a, b) { return Math.min(1, Math.max(0, (v - a) / (b - a))); }
    var x = cv.getContext('2d'), img = new Image(), pts = [], W = 0, H = 0, dpr = 1, N = isMobile ? 11000 : 26000, prog = 0, tStart = performance.now();
    function size() { if (!img.naturalWidth) return; var r = cv.getBoundingClientRect(); dpr = Math.min(window.devicePixelRatio || 1, 2); W = r.width; H = W * img.naturalHeight / img.naturalWidth; cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); cv.style.height = H + 'px'; }
    img.onload = function () {
      var c = document.createElement('canvas'); c.width = img.naturalWidth; c.height = img.naturalHeight; var g = c.getContext('2d'); g.drawImage(img, 0, 0);
      var d = g.getImageData(0, 0, c.width, c.height).data, tries = 0;
      while (pts.length < N && tries < N * 60) { tries++; var px = Math.random() * c.width, py = Math.random() * c.height, v = d[((py | 0) * c.width + (px | 0)) * 4]; if (Math.random() * 255 > v) continue; pts.push({ u: px / c.width, v: py / c.height, w: v / 255, fx: Math.random(), fy: 0.9 + Math.random() * 0.6, s: Math.random(), ph: Math.random() * 6.283 }); }
      size(); requestAnimationFrame(draw);
    };
    img.src = 'assets/method/team.png';
    window.addEventListener('resize', size);
    function draw(now) {
      var r = sec.getBoundingClientRect(), target = fit((window.innerHeight * 0.92 - r.top) / (window.innerHeight * 0.7), 0, 1);
      prog += (target - prog) * (reduced ? 1 : 0.06);
      var time = (now - tStart) / 1000, night = root.getAttribute('data-phase') === 'night', ink = night ? '#f6efe3' : '#7d1426', gold = night ? '#d9b26a' : '#b8903f';
      x.setTransform(dpr, 0, 0, dpr, 0, 0); x.clearRect(0, 0, W, H);
      if (prog > 0.002) for (var i = 0; i < pts.length; i++) {
        var p = pts[i], st = fit((prog - p.s * 0.4) / 0.6, 0, 1); st = st * st * (3 - 2 * st); if (st <= 0) continue;
        var tx = p.u * W, ty = p.v * H, ex = tx + (p.fx * W - tx) * (1 - st), ey = ty + (p.fy * H - ty) * (1 - st);
        if (!reduced) { ex += Math.sin(time * 0.6 + p.ph) * 0.6; ey += Math.cos(time * 0.5 + p.ph) * 0.6; }
        var sz = 1.1 + 1.7 * p.w;
        x.globalAlpha = (0.3 + 0.7 * p.w) * st; x.fillStyle = p.s < 0.07 ? gold : ink; x.fillRect(ex, ey, sz, sz);
      }
      x.globalAlpha = 1;
      requestAnimationFrame(draw);
    }
  })();
"""
js = js + team_js
assert "teamc" in js

# ---------------------------------------------------------------- markup
def chapter(id_, key, cls, eyebrow, h2, lede, extra=''):
    return f'''  <section class="chapter long wrap" id="{id_}" data-key="{key}">
    <div class="copy scrim{cls}">
      <div class="eyebrow">{eyebrow}</div>
      <h2 data-split>{h2}</h2>
      <p class="lede">{lede}</p>{extra}
    </div>
  </section>
'''
def meta(*pairs): return '\n      <div class="meta">' + ''.join(f'<span>{k} <b>{v}</b></span>' if v else f'<span>{k}</span>' for k, v in pairs) + '</div>'
markup = f'''<div id="method">
<div id="preloader" aria-hidden="true">
  <div>
    {mark_svg.replace('class="mark"', 'class="preloader-mark"')}
    <div class="count" id="count">000</div>
    <div class="rule"><i></i></div>
    <div class="kicker">Finding your North</div>
  </div>
</div>
<canvas id="gl" aria-hidden="true"></canvas>
<div class="letterbox top" aria-hidden="true"></div><div class="letterbox bottom" aria-hidden="true"></div>
<div id="cursor" aria-hidden="true"></div>
<nav class="rail" aria-label="Chapters" id="rail">
  <a href="#brief" data-k="2"><i></i>I</a><a href="#core" data-k="3"><i></i>II</a><a href="#journey" data-k="4"><i></i>III</a><a href="#price" data-k="5"><i></i>IV</a><a href="#sprints" data-k="6"><i></i>V</a><a href="#quality" data-k="7"><i></i>VI</a><a href="#handover" data-k="9"><i></i>VII</a>
</nav>
<button class="pill sound-fab" id="sound" type="button" aria-pressed="false" aria-label="Sound"><i></i><span>Sound</span></button>
<div id="tip" aria-hidden="true"></div>

<main id="top">
  <section class="chapter hero wrap" data-key="0">
    <div class="copy">
      <div class="eyebrow fade">How we build · fixed price · twelve weeks</div>
      <h1>
        <span class="w"><span>Twelve</span></span>
        <span class="w"><span>weeks</span></span>
        <span class="w"><span>from</span></span>
        <span class="w"><span>brief</span></span><br>
        <span class="w"><span>to</span></span>
        <span class="w"><span><em>production</em></span></span>
      </h1>
      <p class="lede fade">Our method is an instrument. It measures what your company already does, finds the centre, fixes North, and builds outward in two-week sprints, at a price agreed before we start.</p>
      <div class="actions fade">
        <a class="pill primary" href="contact.html">Start a project</a>
        <a class="pill" href="crm-case-study.html">Read a case study</a>
      </div>
    </div>
    <div class="scroll-hint fade"><span>Scroll to explore</span><i></i></div>
  </section>

{chapter('instrument', 1, ' right', 'The instrument', 'A degree ring, <em>sixteen</em> workstreams, thirty-two milestones',
  'We plan a build the way a surveyor reads a site: a protractor marked every degree, sixteen workstreams of 22.5°, thirty-two milestones on the outer ring, and forty-five checks in the grid, laid over your own operation.',
  meta(('Ticks', '360'), ('Workstreams', '16'), ('Milestones', '32'), ('Checks', '45')))}
{chapter('brief', 2, '', '<span class="n">1</span> The brief', 'Your business, <em>to the outside face</em> of the walls',
  'Paid discovery, one to two weeks. We sit with every desk, open every sheet and group chat, trace the outline of how work actually moves, and measure each process the way you run it today.',
  meta(('Discovery', '1–2 weeks'), ('Interviews', '8–12'), ('Output', 'scope sheet')))}
{chapter('core', 3, ' right', '<span class="n">2</span> The core', 'Find the <em>centre</em>',
  'Every system has one point everything else is measured from: the record that must never be wrong. The order, the ledger, the employee file. We find it first and build outward from it.')}
{chapter('journey', 4, '', '<span class="n">3</span> The first journey', 'The door your team <em>enters</em> by',
  'One workflow, end to end, chosen with you: the one your team runs ten times a day. It is designed, built and signed off before anything else, and it sets the axis for the rest of the build.')}
{chapter('price', 5, '', '<span class="n">4</span> Fix the price', 'Scope agreed. <em>Price locked.</em>',
  'With the brief and the first journey agreed, the quote is fixed. Thirty percent to start, forty at design sign-off, thirty at launch. No day rates and no change-order surprises; new work is quoted the same way.',
  meta(('Quote', 'fixed'), ('Payment', '30 · 40 · 30'), ('Timeline', '12 weeks')))}
{chapter('sprints', 6, '', '<span class="n">5</span> Two-week sprints', 'Sixteen workstreams, <em>one</em> build',
  'Every fortnight, a demo of working software by the engineer who wrote it. Each workstream rises to the effort it needs: pale where we configure, deep maroon where we build from scratch. Milestones light up as they close.',
  '\n      <div class="actions"><a class="pill primary" href="#handover">See the handover</a></div>')}
{chapter('quality', 7, ' right', '<span class="n">6</span> Quality', 'Forty-five checks, <em>eighty-one</em> cases',
  'Automated tests over every workstream, and the grid above the centre is our release checklist: security, backups, performance, data migration. Nothing ships until the grid is complete.')}
  <section class="chapter graph wrap" data-key="8">
    <div class="panel">
      <header><h3>Effort balance</h3><span>Northline build · hours per fortnight · indicative</span></header>
      <svg id="bars" viewBox="0 0 640 230" role="img" aria-label="Bar graph of hours per fortnight across sixteen workstreams with max, average and min lines"></svg>
      <div class="legend"><span><b style="background:#e6cbc8"></b>Pale, configured</span><span><b style="background:#7d1426"></b>Deep, built from scratch</span><span>Lines: (avg + max) / 2 · average · (avg + min) / 2</span></div>
    </div>
  </section>
{chapter('handover', 9, '', '<span class="n">7</span> Launch and handover', 'Two pages, in <em>your</em> name',
  'Page one is the handover sheet: repositories, servers, credentials and the architecture inside the ring. Page two carries the support plan and the runbook. The code, the servers and the data are yours from day one.',
  meta(('Repositories · servers · data', ''), ('Support on', 'one monthly plan')))}
  <section class="chapter features wrap" id="features" data-key="10">
    <div>
      <div class="head">
        <div class="eyebrow">After launch</div>
        <h2 data-split>Then we keep it <em>running</em></h2>
        <p class="lede">Launch is the door. Behind it: hosting, monitoring, updates and a team you can call, on one fixed monthly plan.</p>
      </div>
      <div class="cards">
        <article class="card"><svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="3"/><path d="M7 15l3-4 3 3 4-6"/></svg><h4>Monitoring and backups</h4><p>Uptime checks, nightly backups and restore drills. You get the monthly report, we carry the pager.</p><span class="tag">Report every month</span></article>
        <article class="card"><svg viewBox="0 0 24 24"><path d="M12 3l8 4v6c0 5-3.5 7.5-8 8-4.5-.5-8-3-8-8V7z"/><path d="M9 12l2 2 4-4"/></svg><h4>Fixes within the plan</h4><p>Defects are fixed inside the plan, in the same week, not billed by the hour.</p><span class="tag">Same week</span></article>
        <article class="card"><svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h10M4 17h7"/><circle cx="18" cy="16" r="3"/></svg><h4>New work, quoted</h4><p>A new branch, a report, an integration: scoped and priced the same way as the first build.</p><span class="tag">Fixed price</span></article>
        <article class="card"><svg viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.5"/><circle cx="17" cy="9" r="2.5"/><path d="M2.5 20c1-4 3.5-6 6.5-6s5.5 2 6.5 6zM15 14.5c3 0 5.5 1.5 6.5 5.5H17"/></svg><h4>Training and handover</h4><p>Your team trained, your IT handed the keys. Leave us any time and take everything with you.</p><span class="tag">Yours from day one</span></article>
      </div>
    </div>
  </section>

  <section class="chapter cta wrap" id="cta" data-key="11">
    <div class="copy scrim">
      <div class="eyebrow">Begin</div>
      <h2 data-split>Ready to find <em>your</em> North?</h2>
      <p class="lede">Tell us what your team runs on today. The engineer who would build it calls you back, and you receive a fixed price within one working day of that call.</p>
      <div class="actions"><a class="pill primary" href="contact.html">Start a project</a><a class="pill" href="portfolio.html">See our work</a></div>
      <div class="meta"><span>Noida · remote across India</span><span>English · Hindi</span></div>
    </div>
    <figure class="team"><canvas id="teamc" aria-label="The Wisetrack team, drawn in particles"></canvas><figcaption>The Wisetrack team · Noida</figcaption></figure>
  </section>
</main>
</div>
'''

# ---------------------------------------------------------------- assemble into the methodology shell
lines = shell.split('\n')
main_i = next(i for i, l in enumerate(lines) if l.strip().startswith('<main'))
foot_i = next(i for i, l in enumerate(lines) if l.strip().startswith('<footer class="py-16'))
head = '\n'.join(lines[:main_i])
head = re.sub(r'<title>.*?</title>', '<title>How We Build — Fixed Price, Twelve Weeks to Production · Wisetrack</title>', head, flags=re.S)
head = re.sub(r'(<meta name="description"\s+content=")[^"]*(")', r'\1Our build method: paid discovery, the core record first, one journey end to end, a fixed price, two-week demos, a release checklist, and a handover with the code in your name. Twelve weeks from brief to production.\2', head, flags=re.S)
head = re.sub(r'(<meta property="og:title" content=")[^"]*(")', r'\1How We Build — Fixed Price, Twelve Weeks to Production · Wisetrack\2', head)
head = re.sub(r'(<meta property="og:description" content=")[^"]*(")', r'\1Discovery, the core, the first journey, a fixed price, two-week sprints, a release checklist and a handover in your name. Twelve weeks from brief to production.\2', head)
head = re.sub(r'<link href="assets/styles.css\?v=[^"]*" rel="stylesheet" />',
              '<link href="assets/styles.css?v=20261017" rel="stylesheet" />\n  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Inter:wght@400;500;600&display=swap">\n  <style id="method-styles">' + ns.replace('\\', '\\\\') + '</style>', head)
assert 'method-styles' in head
libs = '\n'.join(re.findall(r'<script src="https://cdn.jsdelivr.net/npm/three@0\.128\.0/[^"]+"></script>', scene))
tail = '\n'.join(lines[foot_i:]).replace('</body>', libs + '\n<script>' + js + '</script>\n</body>')
page = head + '\n<main class="relative pt-[120px]">\n' + markup + '</main>\n' + tail
open(f'{ROOT}/methodology.html', 'w', encoding='utf-8').write(page)
print('methodology.html written:', len(page), 'bytes;', ns.count('#method'), 'scoped selectors')
