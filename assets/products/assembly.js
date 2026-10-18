/* Products — "Assembly" (animation style 03). See assembly.css for the idea.
   Scroll is measured in viewport heights (s) across the pinned section; each chapter owns a
   range of s. Every window has a pose per chapter (scatter, carousel, dock) and the current pose
   is a blend, eased toward the scroll target each frame so a single wheel tick moves smoothly. */
(function () {
  var sec = document.getElementById('assembly'); if (!sec) return;
  var stage = sec.querySelector('.as-stage'), rig = sec.querySelector('.as-rig'), frame = sec.querySelector('.as-frame');
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var MODS = [
    { n: 'CRM and Sales', d: 'Leads from web forms, Facebook and WhatsApp land in one pipeline; a won deal becomes an invoice in one click.', ui: 'pipeline', href: 'crm-sales.html' },
    { n: 'HRMS and Payroll', d: 'Onboarding to exit: statutory EPF, ESI and TDS, geofenced attendance and bank payout files.', ui: 'payroll', href: 'hrms-payroll.html' },
    { n: 'Accounts', d: 'Double-entry ledgers, GST invoicing and e-invoicing, expenses and cashflow, balanced on every entry.', ui: 'ledger', href: 'build-accounts.html' },
    { n: 'Projects', d: 'Milestones, timesheets, bug tickets with SLAs and a portal your client can log in to.', ui: 'gantt', href: 'build-pms.html' },
    { n: 'Learning', d: 'Courses, compliance videos, assessments and digital certificates for every team.', ui: 'courses', href: 'build-lms.html' },
    { n: 'Chat and Video', d: 'Audit-logged team chat, channels and video meetings with live captions.', ui: 'chat', href: 'build-chat.html' },
    { n: 'Drive', d: 'Company file storage with sharing, an audit trail and your own bucket.', ui: 'files', href: 'build-drive.html' },
    { n: 'Mail', d: 'One inbox for every account, with the customer record a click away.', ui: 'inbox', href: 'build-email.html' },
    { n: 'Research', d: 'Market research and surveys, analysed on your own data.', ui: 'bars', href: 'build-research.html' },
    { n: 'Copilot', d: 'Ninety-plus tools across the modules: ask a question, or ask it to do the work.', ui: 'copilot', href: 'products.html#modules' },
    { n: 'Mobile app', d: 'Android and iPhone: attendance, leads, approvals, chat and calls in the field.', ui: 'phone', href: 'mobile-app.html' },
    { n: 'Storefront', d: 'Your own online shop, with stock, GST billing and payments on the same ledger.', ui: 'shop', href: 'products.html#modules' }
  ];
  // the record that travels in the flow chapter: CRM -> Accounts -> Storefront -> HRMS -> Copilot
  var FLOW = [0, 2, 11, 1, 9];
  var FLOW_TAGS = ['Lead #2041 won', 'Invoice INV-0318', 'Stock −12 units', 'Incentive ₹4,200', 'In today’s report'];

  // ---------- mini UIs ----------
  function b(w, c) { return '<i class="b' + (c ? ' ' + c : '') + '" style="width:' + w + '%"></i>'; }
  function bs(w) { return '<i class="b s" style="width:' + w + '%"></i>'; }
  var PEOPLE = [['AM', 'Aarav Mehta'], ['PN', 'Priya Nair'], ['VS', 'Vikram Singh'], ['NK', 'Neha Kapoor'], ['RD', 'Rohan Das']];
  var UI = {
    pipeline: function () {
      var cols = [['New', ['₹ 1.2L', '₹ 80K', '₹ 3.4L']], ['Qualified', ['₹ 2.4L', '₹ 95K']], ['Proposal', ['₹ 6.1L', '₹ 1.8L']], ['Won', ['₹ 4.2L']]];
      return '<div class="cols">' + cols.map(function (c) {
        return '<div class="col"><span>' + c[0] + '</span>' + c[1].map(function (v, i) { return '<div class="card">' + b(70 + i * 9) + bs(45) + '<em>' + v + '</em></div>'; }).join('') + '</div>';
      }).join('') + '</div>';
    },
    payroll: function () {
      return '<div class="kv"><span>Payroll · October</span><strong>₹ 18,42,000</strong></div>' + PEOPLE.slice(0, 4).map(function (p, i) {
        return '<div class="row"><span class="av ' + ['', 'c', 'm', ''][i] + '">' + p[0] + '</span><span class="nm">' + p[1] + '</span><span class="amt">₹ ' + ['62,400', '48,900', '71,250', '39,800'][i] + '</span><span class="pill">' + (i === 3 ? 'Due' : 'Paid') + '</span></div>';
      }).join('');
    },
    ledger: function () {
      var r = [['Sales · GST 18%', '', '2,95,000'], ['Bank · HDFC', '2,95,000', ''], ['Stock in hand', '', '1,12,000'], ['Cost of goods', '1,12,000', '']];
      return '<div class="kv"><span>Journal · 17 Oct</span><strong style="font-size:10px;color:var(--ink-mint)">Balanced ✓</strong></div>' + r.map(function (x) {
        return '<div class="row"><span class="nm">' + x[0] + '</span><span class="amt" style="width:52px;text-align:right">' + x[1] + '</span><span class="amt" style="width:52px;text-align:right">' + x[2] + '</span></div>';
      }).join('');
    },
    gantt: function () {
      var t = [['Discovery', 0, 22], ['Design', 14, 30], ['Build · API', 30, 44], ['Build · UI', 40, 40], ['QA', 70, 20], ['Launch', 88, 10]];
      return '<div class="gantt">' + t.map(function (x, i) { return '<div class="row"><span class="lbl">' + x[0] + '</span><span class="trk"><i style="left:' + x[1] + '%;width:' + x[2] + '%;' + (i % 3 === 1 ? 'background:var(--cyan)' : i % 3 === 2 ? 'background:var(--mint)' : '') + '"></i></span></div>'; }).join('') + '</div>';
    },
    courses: function () {
      return [['POSH compliance', 100], ['GST for sales teams', 64], ['Safety induction', 82], ['New CRM workflow', 30]].map(function (c) {
        return '<div class="row"><span class="nm">' + c[0] + '</span><span class="prog"><i style="width:' + c[1] + '%"></i></span><span class="amt" style="width:30px;text-align:right">' + c[1] + '%</span></div>';
      }).join('');
    },
    chat: function () {
      return '<div class="bub">Dashboard for Northline is up, can you check the totals?</div><div class="bub me">Looks right. Shipping it to the client.</div><div class="bub">Great — I’ll start the invoice.</div>';
    },
    files: function () {
      var f = [['GST-Oct.pdf', ''], ['Payroll.xlsx', 'm'], ['Brief.docx', 'c'], ['Logo.svg', ''], ['Q3-deck.pdf', 'c'], ['Stock.csv', 'm'], ['Contract.pdf', ''], ['Photos', 'c']];
      return '<div class="files">' + f.map(function (x) { return '<div class="file ' + x[1] + '"><i></i>' + x[0] + '</div>'; }).join('') + '</div>';
    },
    inbox: function () {
      return [['Northline Traders', 'Re: revised quotation', '10:42', 1], ['GST portal', 'Return filed for September', '09:15', 1], ['Priya Nair', 'Leave request · 2 days', 'Yest', 0], ['Razorpay', 'Payout settled ₹2.95L', 'Yest', 0]].map(function (m) {
        return '<div class="row"><span class="dot' + (m[3] ? '' : ' o') + '"></span><span class="nm"><b style="color:var(--text)">' + m[0] + '</b> · ' + m[1] + '</span><span class="amt" style="font-size:8px;color:var(--muted)">' + m[2] + '</span></div>';
      }).join('');
    },
    bars: function () {
      return '<div class="kv"><span>Survey · 1,240 responses</span><strong>+18%</strong></div><div class="bars">' + [44, 70, 52, 88, 61, 95, 73, 58].map(function (h) { return '<i style="height:' + h + '%"></i>'; }).join('') + '</div>';
    },
    copilot: function () {
      return '<div class="ask">Which invoices are overdue this week?</div><div class="chips"><span>accounts.search_invoices</span><span>crm.lookup_customer</span></div>' + b(92) + bs(80) + bs(66) + '<div style="margin-top:8px">' + b(40, 'a') + '</div>';
    },
    phone: function () {
      return '<div class="phone-top"><span>9:41</span><span>●●●</span></div><div class="tile-big">Clocked in · 09:02<strong>Geofence OK</strong></div>' + ['Approve leave · Priya', 'New lead · Kumar Ent.', 'Call back · Vikram'].map(function (x, i) { return '<div class="row"><span class="av ' + ['c', '', 'm'][i] + '">' + x.split('· ')[1].slice(0, 1) + '</span><span class="nm">' + x + '</span></div>'; }).join('');
    },
    shop: function () {
      return '<div class="shop">' + ['₹ 1,299', '₹ 849', '₹ 2,450', '₹ 599', '₹ 1,050', '₹ 3,200'].map(function (p) { return '<div class="prod"><i></i><span>' + p + '</span></div>'; }).join('') + '</div>';
    }
  };

  // ---------- build the windows ----------
  var wins = MODS.map(function (m, i) {
    var el = document.createElement('div');
    el.className = 'as-win' + (m.ui === 'phone' ? ' tall' : '');
    el.setAttribute('aria-hidden', 'true');
    el.innerHTML = '<div class="as-bar"><i></i><i></i><i></i><b>' + m.n + '</b><em>Ragenaizer</em></div><div class="as-body">' + UI[m.ui]() + '</div>';
    rig.appendChild(el);
    return { el: el, m: m, w: m.ui === 'phone' ? 156 : 320, h: m.ui === 'phone' ? 280 : 210, cur: null };
  });
  var side = frame.querySelector('.as-side ol');
  side.innerHTML = MODS.map(function (m) { return '<li><i></i>' + m.n + '</li>'; }).join('');
  var sideItems = side.querySelectorAll('li');

  // seeded scatter so every visit looks the same
  var seed = 7; function R() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }
  var rnd = wins.map(function () { return [R(), R(), R(), R(), R(), R(), R()]; });

  // ---------- geometry ----------
  var vw = 0, vh = 0, mobile = false, k = 1, F = {};
  function measure() {
    vw = stage.clientWidth; vh = stage.clientHeight; mobile = vw < 760;
    k = Math.max(0.5, Math.min(1.12, vw / 1440));
    var fw = mobile ? vw * 0.94 : Math.min(1000, vw * 0.55), fh = fw * (mobile ? 0.78 : 0.6);
    F = { w: fw, h: fh, x: mobile ? 0 : vw * 0.2, y: mobile ? -vh * 0.16 : vh * 0.02, side: fw * (mobile ? 0.0 : 0.19), top: Math.max(30, fh * 0.075) };
    frame.style.width = fw + 'px'; frame.style.height = fh + 'px';
    var sd = frame.querySelector('.as-side'); sd.style.width = F.side + 'px'; sd.style.display = mobile ? 'none' : '';
    var tp = frame.querySelector('.as-top'); tp.style.left = F.side + 'px'; tp.style.height = F.top + 'px';
    var cols = mobile ? 3 : 4, rows = mobile ? 4 : 3, pad = fw * 0.022, g = fw * 0.016;
    var cw = fw - F.side - pad * 2, ch = fh - F.top - pad * 2;
    F.cols = cols; F.tw = (cw - g * (cols - 1)) / cols; F.th = (ch - g * (rows - 1)) / rows;
    F.cells = wins.map(function (w, i) {
      var c = i % cols, r = Math.floor(i / cols);
      // tile centre relative to the frame centre
      return { x: -fw / 2 + F.side + pad + c * (F.tw + g) + F.tw / 2, y: -fh / 2 + F.top + pad + r * (F.th + g) + F.th / 2 };
    });
    var svg = frame.querySelector('.as-flow'); svg.setAttribute('width', fw); svg.setAttribute('height', fh); svg.setAttribute('viewBox', '0 0 ' + fw + ' ' + fh);
    var pts = FLOW.map(function (i) { return [F.cells[i].x + fw / 2, F.cells[i].y + fh / 2]; });
    var d = 'M' + pts.map(function (p) { return p[0].toFixed(1) + ' ' + p[1].toFixed(1); }).join(' L');
    svg.querySelectorAll('path').forEach(function (p) { p.setAttribute('d', d); });
    flowLen = svg.querySelector('path.live').getTotalLength();
  }
  var flowLen = 1;

  // ---------- timeline (in viewport heights) ----------
  var T = mobileT();
  function mobileT() { return { carIn: [1.0, 1.7], car: [1.7, 5.5], dock: [5.5, 6.4], tiltIn: [6.5, 6.95], flow: [6.95, 7.95], tiltOut: [8.0, 8.5], end: 9.2 }; }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function fit(v, r) { return clamp((v - r[0]) / (r[1] - r[0]), 0, 1); }
  function ease(t) { return t * t * (3 - 2 * t); }
  function mix(a, b, t) { var o = {}; for (var key in a) o[key] = a[key] + (b[key] - a[key]) * t; return o; }

  function scatterPose(i, time) {
    var r = rnd[i], spreadX = mobile ? 0.62 : 0.78, spreadY = mobile ? 0.36 : 0.42;
    return {
      x: (r[0] - 0.5) * 2 * vw * spreadX + Math.sin(time * 0.31 + r[6] * 6) * 14,
      y: (r[1] - 0.5) * 2 * vh * spreadY + Math.cos(time * 0.27 + r[6] * 5) * 12 - (mobile ? vh * 0.12 : 0),
      z: -260 - r[2] * 1350, rx: (r[3] - 0.5) * 26, ry: (r[4] - 0.5) * 56, rz: (r[5] - 0.5) * 12,
      s: k * (mobile ? 0.8 : 1), o: 1
    };
  }
  function carouselPose(i, a) {
    var d = i - a, th = d * 0.4, R = (mobile ? 560 : 1000) * k, ad = Math.abs(d);
    return {
      x: (mobile ? 0 : vw * 0.2) + Math.sin(th) * R * 0.95, y: mobile ? -vh * 0.17 : 0,
      z: (Math.cos(th) - 1) * R - ad * 30, rx: 0, ry: -th * 57.3 * 0.85, rz: 0,
      s: k * (mobile ? 0.82 : 1) * (1 + 0.42 * Math.max(0, 1 - ad)), o: d < 0 ? clamp(1 + (d + 0.6) * 0.9, 0, 1) : clamp(1.15 - Math.max(0, ad - 2.6) * 0.55, 0, 1)
    };
  }
  function dockPose(i) {
    var w = wins[i], c = F.cells[i], sc = Math.min(F.tw / w.w, F.th / w.h) * 0.98;
    return { x: F.x + c.x, y: F.y + c.y, z: 2, rx: 0, ry: 0, rz: 0, s: sc, o: 1 };
  }

  // ---------- copy + rail ----------
  var copies = [].slice.call(sec.querySelectorAll('.as-copy'));
  var railLinks = [].slice.call(sec.querySelectorAll('.as-rail a'));
  var modName = sec.querySelector('[data-mod-name]'), modDesc = sec.querySelector('[data-mod-desc]'), modNum = sec.querySelector('[data-mod-num]'), modLink = sec.querySelector('[data-mod-link]');
  var steps = [].slice.call(sec.querySelectorAll('.as-steps li'));
  var shownMod = -1;
  function setMod(i) {
    if (i === shownMod) return; shownMod = i;
    var m = MODS[i]; modName.textContent = m.n; modDesc.textContent = m.d; modNum.textContent = String(i + 1).padStart(2, '0'); modLink.href = m.href;
  }
  railLinks.forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      window.scrollTo({ top: secTop() + parseFloat(a.dataset.s) * vh, behavior: reduced ? 'auto' : 'smooth' });
    });
  });

  // ---------- frame loop ----------
  function secTop() { return sec.getBoundingClientRect().top + window.scrollY; }
  var sCur = 0, last = performance.now(), t0 = last;
  function target() { return clamp((window.scrollY - secTop()) / vh, 0, T.end); }
  function tick(now) {
    var dt = Math.min(0.05, (now - last) / 1000); last = now;
    var tgt = target();
    sCur = reduced ? tgt : sCur + (tgt - sCur) * (1 - Math.exp(-dt * 7));
    var s = sCur, time = (now - t0) / 1000;
    var eCar = ease(fit(s, T.carIn)), eDock = ease(fit(s, T.dock));
    var a = clamp(fit(s, T.car) * 11, 0, 11);
    var tilt = ease(fit(s, T.tiltIn)) * (1 - ease(fit(s, T.tiltOut)));
    var flow = fit(s, T.flow);

    // rig: tilts the docked screen flat for the flow chapter
    rig.style.transform = 'translate3d(' + (F.x * tilt * 0.0) + 'px,' + (mobile ? 0 : vh * 0.04 * tilt) + 'px,0) rotateX(' + (46 * tilt) + 'deg) rotateZ(' + (-24 * tilt) + 'deg) scale(' + (1 - 0.1 * tilt) + ')';
    // frame
    var fo = ease(fit(s, [T.dock[0] + 0.15, T.dock[1]]));
    frame.style.opacity = fo;
    frame.style.transform = 'translate3d(' + (F.x - F.w / 2) + 'px,' + (F.y - F.h / 2) + 'px,' + (-40 + 40 * fo) + 'px) scale(' + (0.94 + 0.06 * fo) + ')';

    wins.forEach(function (w, i) {
      var p = mix(scatterPose(i, time), carouselPose(i, a), eCar);
      if (eDock > 0) p = mix(p, dockPose(i), eDock);
      var lit = flow > 0 && tilt > 0.5 && FLOW.indexOf(i) >= 0 && FLOW.indexOf(i) <= Math.floor(flow * FLOW.length - 0.001);
      if (lit) p.z += 34 * tilt;
      w.el.classList.toggle('lit', !!lit);
      w.el.style.transform = 'translate3d(' + p.x.toFixed(1) + 'px,' + p.y.toFixed(1) + 'px,' + p.z.toFixed(1) + 'px) rotateX(' + p.rx.toFixed(2) + 'deg) rotateY(' + p.ry.toFixed(2) + 'deg) rotateZ(' + p.rz.toFixed(2) + 'deg) scale(' + p.s.toFixed(4) + ')';
      w.el.style.opacity = p.o.toFixed(3);
    });

    // the travelling record
    var svg = frame.querySelector('.as-flow'), live = svg.querySelector('path.live'), dot = svg.querySelector('circle.dot'), halo = svg.querySelector('circle.halo'), tag = frame.querySelector('.as-tag');
    var fl = clamp(flow * 1.05, 0, 1), L = flowLen * fl;
    live.style.strokeDashoffset = 0; live.style.opacity = tilt > 0.3 ? 1 : 0;
    live.setAttribute('stroke-dasharray', L.toFixed(1) + ' ' + flowLen.toFixed(1));
    svg.querySelector('path.trail').style.opacity = tilt * 0.28;
    var pt = live.getPointAtLength(Math.max(0.01, L));
    dot.setAttribute('cx', pt.x); dot.setAttribute('cy', pt.y); halo.setAttribute('cx', pt.x); halo.setAttribute('cy', pt.y);
    halo.setAttribute('r', 10 + Math.sin(time * 4) * 3);
    dot.style.opacity = halo.style.opacity = tilt > 0.3 && flow > 0 ? 1 : 0;
    var stepI = Math.min(FLOW.length - 1, Math.floor(flow * FLOW.length));
    tag.textContent = FLOW_TAGS[stepI];
    tag.style.left = pt.x + 'px'; tag.style.top = pt.y + 'px'; tag.style.opacity = tilt > 0.5 && flow > 0.02 ? 1 : 0;
    steps.forEach(function (li, j) { li.classList.toggle('on', flow > 0 && j <= stepI); });

    // sidebar highlights the module on stage (carousel) or the flow step
    var onIdx = s < T.dock[1] ? Math.round(a) : (flow > 0 ? FLOW[stepI] : -1);
    sideItems.forEach(function (li, j) { li.classList.toggle('on', j === onIdx); });

    // copy
    copies.forEach(function (c) {
      var r = c.dataset.range.split(',').map(parseFloat), fade = 0.28;
      var o = Math.min(fit(s, [r[0] - fade, r[0]]), 1 - fit(s, [r[1], r[1] + fade]));
      if (r[0] <= 0) o = 1 - fit(s, [r[1], r[1] + fade]);
      if (r[1] >= T.end) o = fit(s, [r[0] - fade, r[0]]);
      c.style.opacity = o.toFixed(3);
      c.style.transform = (mobile ? 'translateY(' : 'translateY(calc(-46% + ') + ((1 - o) * 18).toFixed(1) + 'px' + (mobile ? ')' : '))');
      c.classList.toggle('on', o > 0.5);
    });
    setMod(Math.round(a));
    var hint = sec.querySelector('.as-hint'); if (hint) hint.style.opacity = 1 - fit(s, [0.05, 0.4]);
    railLinks.forEach(function (l) { var r = l.dataset.range.split(',').map(parseFloat); l.classList.toggle('on', s >= r[0] && s < r[1]); });

  }
  function loop(now) { if (visible) tick(now); else last = now; requestAnimationFrame(loop); }
  // only animate while the section is on screen
  var visible = true;
  new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }, { rootMargin: '200px 0px' }).observe(sec);
  measure();
  window.addEventListener('resize', measure);
  sCur = target();
  requestAnimationFrame(function (now) { last = now; requestAnimationFrame(loop); });
})();
