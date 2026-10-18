/* Services — "Blueprint" (animation style 04). See blueprint.css for the idea.
   Each chapter is a drawing: `wire` shapes draw in (pathLength=1, so every stroke is dashed by
   the same 0..1 amount), `fill` shapes and labels fade in once the lines are down, the code
   panel types, then the drawing undraws as the next one starts. Scroll is measured in viewport
   heights (s) and eased toward the target every frame. */
(function () {
  var sec = document.getElementById('blueprint'); if (!sec) return;
  var svg = sec.querySelector('svg.bp-sheet'), NS = 'http://www.w3.org/2000/svg';
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---------- drawing helpers ----------
  var cur = null; // the chapter group being built
  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    (parent || cur.g).appendChild(e); return e;
  }
  function wire(tag, attrs, cls) { attrs['class'] = 'w ' + (cls || ''); attrs.pathLength = 1; var e = el(tag, attrs); cur.wires.push(e); return e; }
  function fill(tag, attrs, cls, delay) { attrs['class'] = 'f ' + (cls || ''); var e = el(tag, attrs); e.style.opacity = 0; cur.fills.push([e, delay || 0]); return e; }
  function text(x, y, s, cls, anchor, delay) { var e = el('text', { x: x, y: y, 'class': cls || '', 'text-anchor': anchor || 'start' }); e.textContent = s; e.style.opacity = 0; cur.fills.push([e, delay || 0]); return e; }
  function line(x1, y1, x2, y2, cls) { return wire('line', { x1: x1, y1: y1, x2: x2, y2: y2 }, cls); }
  function rect(x, y, w, h, r, cls) { return wire('rect', { x: x, y: y, width: w, height: h, rx: r || 0 }, cls); }
  function frect(x, y, w, h, r, cls, d) { return fill('rect', { x: x, y: y, width: w, height: h, rx: r || 0 }, cls, d); }
  function circ(cx, cy, r, cls) { return wire('circle', { cx: cx, cy: cy, r: r }, cls); }
  function path(d, cls) { return wire('path', { d: d }, cls); }
  // a dimension line with end ticks and a label
  function dim(x1, y1, x2, y2, label) {
    var h = y1 === y2, e1 = el('line', { x1: x1, y1: y1, x2: x2, y2: y2, 'class': 'd', pathLength: 1 }); cur.wires.push(e1);
    [[x1, y1], [x2, y2]].forEach(function (p) {
      var t = el('line', h ? { x1: p[0], y1: p[1] - 6, x2: p[0], y2: p[1] + 6, 'class': 'd', pathLength: 1 } : { x1: p[0] - 6, y1: p[1], x2: p[0] + 6, y2: p[1], 'class': 'd', pathLength: 1 }); cur.wires.push(t);
    });
    if (h) text((x1 + x2) / 2, y1 - 9, label, '', 'middle'); else { var tx = text(x1 - 12, (y1 + y2) / 2, label, '', 'middle'); tx.setAttribute('transform', 'rotate(-90 ' + (x1 - 12) + ' ' + ((y1 + y2) / 2) + ')'); }
  }
  // an annotation: dashed leader from a point to a label
  function note(px, py, lx, ly, label) {
    var l = el('polyline', { points: px + ',' + py + ' ' + lx + ',' + ly + ' ' + (lx + (lx > px ? 14 : -14)) + ',' + ly, 'class': 'lead', pathLength: 1 });
    l.style.opacity = 0; cur.fills.push([l, 0.25]);
    el('circle', { cx: px, cy: py, r: 3, 'class': 'f a' }).style.opacity = 0; cur.fills.push([cur.g.lastChild, 0.25]);
    text(lx + (lx > px ? 20 : -20), ly + 4, label, 'lbl', lx > px ? 'start' : 'end', 0.3);
  }
  var chapters = [];
  function chapter(name, code, codeLang) {
    cur = { g: el('g', { 'class': 'ch-' + name }, svg), wires: [], fills: [], code: code || '', lang: codeLang || '', extra: null };
    chapters.push(cur); return cur;
  }

  // ---------- 0 · the sheet: border and title block (stays) ----------
  var sheet = chapter('sheet');
  rect(14, 14, 972, 672, 4, 'thin'); rect(24, 24, 952, 652, 2);
  var sheetRoot = sheet.g, tb = el('g', { 'class': 'tb' });
  cur.g = tb;
  rect(716, 596, 260, 80, 0); line(716, 622, 976, 622); line(716, 649, 976, 649); line(830, 596, 830, 676);
  text(726, 613, 'PROJECT'); text(840, 613, 'YOUR SOFTWARE', 'v');
  text(726, 640, 'DRAWN BY'); text(840, 640, 'WISETRACK · INDIA', 'v');
  text(726, 667, 'SHEET'); var sheetNo = text(840, 667, '1 OF 6 · BRIEF', 'v');
  cur.g = sheetRoot;
  // the brief: a rough sketch with a question mark, drawn on the open sheet
  path('M150 470 C 210 380, 300 520, 370 430 S 520 360, 600 440', 'thin');
  rect(170, 180, 190, 120, 10); rect(420, 150, 220, 160, 10, 'a'); rect(250, 360, 160, 90, 10);
  path('M360 240 L420 230', ''); path('M520 310 L410 380', '');
  text(265, 248, 'orders?', 'big', 'middle', .2); text(530, 238, 'one screen', 'big', 'middle', .25); text(330, 412, 'stock', 'big', 'middle', .3);
  text(660, 140, '← what you tell us', 'lbl', 'start', .4);

  // ---------- 1 · web portal ----------
  chapter('web', '<span class="k">app</span>.MapGet(<span class="s">"/api/invoices"</span>, <span class="k">async</span> (Db db) =>\n    <span class="k">await</span> db.Invoices\n        .Where(i => i.Status == <span class="s">"overdue"</span>)\n        .OrderBy(i => i.DueDate)\n        .ToListAsync());', 'C# · ASP.NET Core');
  rect(110, 90, 600, 420, 12); line(110, 128, 710, 128); circ(132, 109, 5); circ(150, 109, 5); circ(168, 109, 5);
  rect(200, 99, 300, 20, 6, 'thin'); rect(110, 128, 130, 382, 0);
  frect(111, 129, 128, 380, 0, 's2'); frect(201, 100, 298, 18, 5, 'ln');
  for (var i = 0; i < 6; i++) { line(130, 160 + i * 34, 200 + (i % 3) * 14, 160 + i * 34, 'thin'); }
  frect(124, 151, 102, 20, 5, 'at', .1); text(134, 165, 'Invoices', 'ui', 'start', .15);
  [0, 1, 2].forEach(function (k) { rect(260 + k * 148, 148, 132, 70, 8, k === 0 ? 'a' : ''); frect(261 + k * 148, 149, 130, 68, 7, k === 0 ? 'at' : 's', .05 * k); });
  text(274, 172, 'Overdue', 'ui', 'start', .2); text(274, 200, '₹ 4.8L', 'uib', 'start', .2);
  text(422, 172, 'Due this week', 'ui', 'start', .25); text(422, 200, '₹ 2.1L', 'uib', 'start', .25);
  text(570, 172, 'Collected', 'ui', 'start', .3); text(570, 200, '₹ 11.6L', 'uib', 'start', .3);
  rect(260, 236, 428, 254, 8);
  for (var r = 0; r < 6; r++) { line(260, 276 + r * 36, 688, 276 + r * 36, 'thin'); frect(278, 288 + r * 36, 110 - (r % 3) * 18, 9, 4, 'ln', .1 + r * .03); frect(560, 288 + r * 36, 46, 12, 6, r < 2 ? 'at' : 'mt', .12 + r * .03); }
  text(278, 260, 'CUSTOMER', '', 'start', .1); text(460, 260, 'AMOUNT', '', 'start', .1); text(560, 260, 'STATUS', '', 'start', .1);
  dim(110, 62, 710, 62, '1440 PX · RESPONSIVE');
  note(470, 380, 800, 330, 'Postgres · one query');
  note(330, 182, 800, 196, 'Redis · cached totals');
  note(175, 300, 800, 460, 'Your workflow, not a template');

  // ---------- 2 · mobile ----------
  chapter('mobile', '<span class="k">val</span> inside = location.distanceTo(office) < <span class="n">150f</span>\n<span class="k">if</span> (inside) attendance.clockIn(now(), location)\n<span class="k">else</span> ui.warn(<span class="s">"Outside the office geofence"</span>)\nsync.queueWhenOnline(attendance.pending())', 'Kotlin · Android');
  rect(330, 50, 250, 500, 38); rect(345, 64, 220, 472, 28, 'thin'); rect(420, 70, 70, 16, 8);
  frect(346, 65, 218, 470, 27, 's');
  text(368, 108, '9:41', 'ui', 'start', .1);
  rect(365, 130, 180, 150, 14, 'thin'); frect(366, 131, 178, 148, 13, 'ct', .1);
  circ(455, 205, 52, 'a'); circ(455, 205, 4, 'a'); path('M455 205 L493 170', 'thin');
  text(463, 186, '150 m', '', 'start', .2);
  rect(365, 300, 180, 50, 14, 'a'); frect(366, 301, 178, 48, 13, 'a', .15); text(455, 331, 'Clock in · 09:02', 'uib on', 'middle', .2);
  for (var m = 0; m < 3; m++) { circ(383, 386 + m * 46, 10, m === 0 ? 'a' : 'thin'); line(402, 382 + m * 46, 520, 382 + m * 46, 'thin'); line(402, 394 + m * 46, 480, 394 + m * 46, 'thin'); }
  text(402, 380, 'Approve leave · Priya', 'ui', 'start', .25); text(402, 426, 'New lead · Kumar Ent.', 'ui', 'start', .28); text(402, 472, 'Scan · GRN 2041', 'ui', 'start', .31);
  dim(300, 50, 300, 550, '390 PT');
  note(500, 205, 760, 170, 'Geofence · works offline');
  note(545, 325, 760, 330, 'SQLCipher · encrypted on device');
  note(560, 470, 760, 470, 'Syncs the moment it’s online');

  // ---------- 3 · AI agents ----------
  var ai = chapter('ai', '{\n  <span class="s">"tool"</span>: <span class="s">"accounts.search_invoices"</span>,\n  <span class="s">"input"</span>: { <span class="s">"status"</span>: <span class="s">"overdue"</span>, <span class="s">"limit"</span>: <span class="n">50</span> },\n  <span class="s">"guard"</span>: <span class="s">"read-only · tenant scoped"</span>,\n  <span class="s">"cost"</span>: <span class="s">"logged per call"</span>\n}', 'Agent tool call');
  var N = { q: [80, 280], plan: [270, 150], tools: [480, 280], check: [690, 150], ans: [800, 330] };
  function node(k, label, cls) { var p = N[k]; rect(p[0], p[1], 150, 64, 14, cls); frect(p[0] + 1, p[1] + 1, 148, 62, 13, cls === 'a' ? 'at' : cls === 'c' ? 'ct' : 's', .1); text(p[0] + 75, p[1] + 38, label, 'uib', 'middle', .15); }
  node('q', 'Your question'); node('plan', 'Plan', 'a'); node('tools', 'Use tools', 'c'); node('check', 'Check', 'a'); node('ans', 'Answer + action', 'm');
  var flowD = 'M230 312 C 250 250, 250 182, 270 182 M420 182 C 460 182, 460 312, 480 312 M630 312 C 660 312, 660 182, 690 182 M840 214 C 860 260, 870 300, 875 330';
  var flowP = path(flowD, 'a');
  path('M765 150 C 740 70, 380 70, 345 150', 'thin'); text(555, 78, 'self-correct', 'lbl', 'middle', .3);
  [['accounts.search', 0], ['crm.lookup', 1], ['drive.read', 2]].forEach(function (t) {
    var x = 420 + t[1] * 105, y = 430; path('M555 344 L' + (x + 45) + ' ' + y, 'thin'); rect(x, y, 96, 32, 8, 'c'); frect(x + 1, y + 1, 94, 30, 7, 'ct', .2); text(x + 48, y + 20, t[0], '', 'middle', .25);
  });
  note(345, 214, 160, 470, 'Guardrails on every step');
  note(875, 394, 870, 520, 'Token cost logged per call');
  ai.extra = function (t) { // a pulse running along the loop
    if (!ai.pulse) { ai.pulseH = el('circle', { r: 11, 'class': 'pulse-h' }, ai.g); ai.pulse = el('circle', { r: 5, 'class': 'pulse' }, ai.g); ai.len = flowP.getTotalLength ? null : 0; }
    var p = fitf(t, .45, .95), vis = t > .4 && t < .97 ? 1 : 0;
    var path0 = flowP, L = path0.getTotalLength(), pt = path0.getPointAtLength(L * p);
    ai.pulse.setAttribute('cx', pt.x); ai.pulse.setAttribute('cy', pt.y); ai.pulseH.setAttribute('cx', pt.x); ai.pulseH.setAttribute('cy', pt.y);
    ai.pulse.style.opacity = ai.pulseH.style.opacity = vis;
  };

  // ---------- 4 · dashboards ----------
  chapter('dash', 'socket.on(<span class="s">"metrics"</span>, m => {\n  revenue.push(m.revenue);\n  orders.set(m.orders);\n  chart.update({ series: [revenue] });\n});', 'WebSocket · live');
  rect(90, 70, 820, 470, 14);
  [0, 1, 2, 3].forEach(function (k) { rect(116 + k * 196, 96, 178, 76, 10, k === 0 ? 'a' : ''); frect(117 + k * 196, 97, 176, 74, 9, k === 0 ? 'at' : 's', .05 * k); });
  [['Revenue today', '₹ 6.4L'], ['Orders', '1,284'], ['Avg ticket', '₹ 498'], ['Live users', '312']].forEach(function (x, k) { text(132 + k * 196, 124, x[0], 'ui', 'start', .15 + k * .03); text(132 + k * 196, 154, x[1], 'uib', 'start', .15 + k * .03); });
  line(140, 470, 560, 470); line(140, 210, 140, 470);
  for (var g = 0; g < 4; g++) line(140, 250 + g * 55, 560, 250 + g * 55, 'thin');
  path('M140 430 C 190 410, 220 440, 270 380 S 360 330, 410 350 S 500 250, 560 240', 'a');
  fill('path', { d: 'M140 430 C 190 410, 220 440, 270 380 S 360 330, 410 350 S 500 250, 560 240 L560 470 L140 470 Z' }, 'at', .1);
  for (var bb = 0; bb < 7; bb++) { var hh = [90, 140, 110, 170, 130, 190, 160][bb]; rect(610 + bb * 40, 470 - hh, 26, hh, 4, bb % 2 ? 'c' : 'm'); frect(610 + bb * 40, 470 - hh, 26, hh, 4, bb % 2 ? 'c' : 'm', .1 + bb * .03); }
  line(600, 470, 890, 470);
  text(140, 500, 'REVENUE · 30 DAYS', '', 'start', .1); text(610, 500, 'ORDERS · BY BRANCH', '', 'start', .1);
  note(560, 240, 760, 600, 'Updates in under a second');
  note(200, 134, 60, 610, 'Every number traceable to a record');

  // ---------- 5 · process: two-week demos ----------
  chapter('process', '', '');
  line(110, 340, 890, 340, 'a');
  ['Week 2', 'Week 4', 'Week 6', 'Week 8', 'Week 10', 'Week 12'].forEach(function (w, k) {
    var x = 150 + k * 140; line(x, 326, x, 354); path('M' + x + ' 326 L' + x + ' 250 L' + (x + 70) + ' 262 L' + x + ' 274', k === 5 ? 'm' : 'a');
    fill('path', { d: 'M' + x + ' 250 L' + (x + 70) + ' 262 L' + x + ' 274 Z' }, k === 5 ? 'm' : 'a', .05 * k);
    text(x, 384, w.toUpperCase(), '', 'middle', .1 + k * .04);
    text(x, 408, k === 5 ? 'Launch' : 'Demo ' + (k + 1), 'uib', 'middle', .12 + k * .04);
  });
  dim(110, 470, 890, 470, 'FIXED PRICE · AGREED BEFORE WEEK 1');
  note(430, 262, 520, 160, 'You click a working build every fortnight');

  // ---------- timeline ----------
  var RANGES = { sheet: [0, 1.0], web: [1.0, 2.65], mobile: [2.65, 4.3], ai: [4.3, 5.95], dash: [5.95, 7.6], process: [7.6, 9.2] };
  var SHEET = { sheet: '1 OF 6 · BRIEF', web: '2 OF 6 · WEB', mobile: '3 OF 6 · MOBILE', ai: '4 OF 6 · AI', dash: '5 OF 6 · DASHBOARDS', process: '6 OF 6 · DELIVERY' };
  var END = 9.2;
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function fitf(v, a, b) { return clamp((v - a) / (b - a), 0, 1); }
  function ease(t) { return t * t * (3 - 2 * t); }

  var code = sec.querySelector('.bp-code'), pre = code.querySelector('pre'), lang = code.querySelector('header span');
  var copies = [].slice.call(sec.querySelectorAll('.bp-copy'));
  var lastCode = null, lastChars = -1;
  function typed(html, n) { // reveal n visible characters of an HTML string, keeping tags
    var out = '', count = 0, i = 0;
    while (i < html.length && count < n) {
      if (html[i] === '<') { var j = html.indexOf('>', i); out += html.slice(i, j + 1); i = j + 1; continue; }
      if (html[i] === '&') { var e2 = html.indexOf(';', i); out += html.slice(i, e2 + 1); i = e2 + 1; count++; continue; }
      out += html[i]; i++; count++;
    }
    var opens = (out.match(/<span/g) || []).length - (out.match(/<\/span>/g) || []).length;
    for (var q = 0; q < opens; q++) out += '</span>';
    return out;
  }
  function plainLen(html) { return html.replace(/<[^>]+>/g, '').replace(/&[a-z]+;/g, 'x').length; }

  function render(s) {
    var active = null, activeT = 0;
    chapters.forEach(function (c) {
      var name = c.g.getAttribute('class').slice(3), r = RANGES[name], t = fitf(s, r[0], r[1]);
      var isFirst = name === 'sheet', isLast = name === 'process';
      var draw = isFirst ? ease(fitf(s, 0, 0.55)) : ease(fitf(t, 0, .34));
      var out = isLast ? 0 : isFirst ? 0 : ease(fitf(t, .86, 1));
      if (s < r[0] && !isFirst) draw = 0;
      var frac = draw * (1 - out);
      c.wires.forEach(function (w) { w.style.strokeDasharray = '1 1'; w.style.strokeDashoffset = (1 - frac).toFixed(4); });
      c.fills.forEach(function (f) { var o = ease(fitf(isFirst ? s : t, (isFirst ? .35 : .3) + f[1] * .5, (isFirst ? .7 : .52) + f[1] * .5)) * (1 - out); f[0].style.opacity = o.toFixed(3); });
      if (c.extra) c.extra(t);
      if (!isFirst && s >= r[0] && s < r[1]) { active = c; activeT = t; }
    });
    // the brief sketch (not the border / title block) gives way to the first drawing
    var sk = fitf(s, 0.75, 1.15);
    [].forEach.call(sheet.g.children, function (n) { if (n !== tb) n.style.opacity = (1 - sk).toFixed(3); });
    var nm = 'sheet'; for (var k in RANGES) if (s >= RANGES[k][0]) nm = k; sheetNo.textContent = SHEET[nm];
    // code panel
    var co = active && active.code ? ease(fitf(activeT, .2, .32)) * (1 - ease(fitf(activeT, .84, .96))) : 0;
    code.style.opacity = co.toFixed(3); code.style.transform = 'translateY(' + ((1 - co) * 12).toFixed(1) + 'px)';
    if (active && active.code) {
      if (lastCode !== active) { lastCode = active; lastChars = -1; lang.textContent = active.lang; }
      var n = Math.round(plainLen(active.code) * fitf(activeT, .26, .7));
      if (n !== lastChars) { lastChars = n; pre.innerHTML = typed(active.code, n) + '<span class="caret"></span>'; }
    }
    // copy
    copies.forEach(function (c) {
      var r = c.dataset.range.split(',').map(parseFloat), fade = .26;
      var o = r[0] <= 0 ? 1 - fitf(s, r[1], r[1] + fade) : r[1] >= END ? fitf(s, r[0] - fade, r[0]) : Math.min(fitf(s, r[0] - fade, r[0]), 1 - fitf(s, r[1], r[1] + fade));
      c.style.opacity = o.toFixed(3);
      c.style.transform = mobile ? 'translateY(' + ((1 - o) * 14).toFixed(1) + 'px)' : 'translateY(calc(-46% + ' + ((1 - o) * 14).toFixed(1) + 'px))';
      c.classList.toggle('on', o > .5);
    });
    var hint = sec.querySelector('.bp-hint'); if (hint) hint.style.opacity = 1 - fitf(s, .05, .4);
  }

  var mobile = false, vh = 1;
  function measure() { mobile = window.innerWidth < 760; vh = sec.querySelector('.bp-stage').clientHeight || window.innerHeight; }
  function secTop() { return sec.getBoundingClientRect().top + window.scrollY; }
  function target() { return clamp((window.scrollY - secTop()) / vh, 0, END); }
  var sCur = 0, last = performance.now(), visible = true;
  new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }, { rootMargin: '200px 0px' }).observe(sec);
  function loop(now) {
    var dt = Math.min(0.05, (now - last) / 1000); last = now;
    if (visible) { var tg = target(); var ns = reduced ? tg : sCur + (tg - sCur) * (1 - Math.exp(-dt * 6)); if (Math.abs(ns - sCur) > 0.0004 || ns === tg) { sCur = ns; render(sCur); } }
    requestAnimationFrame(loop);
  }
  measure(); window.addEventListener('resize', measure);
  sCur = target(); render(sCur);
  requestAnimationFrame(function (now) { last = now; requestAnimationFrame(loop); });
})();
