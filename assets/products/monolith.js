/* Products — "Monoliths" (animation style 03).
   Twelve module screens stand as lit glass monoliths along an avenue on a reflective floor. The
   camera walks the avenue one module at a time, then the monoliths lift and lock into a single
   wall: one Ragenaizer screen. Light pulses carry one record across the modules, and the camera
   rises for the close. Same toolkit as How we build: three r128, ACES tone mapping, soft
   shadows, depth of field, bloom, grain and vignette. Every colour comes from the site tokens,
   so palettes and light/dark re-skin the scene and the screen textures. Scroll is measured in
   viewport heights (s) across the pinned section and eased toward the target each frame. */
(function () {
  var sec = document.getElementById('assembly'); if (!sec) return;
  var stage = sec.querySelector('.as-stage'), canvas = sec.querySelector('canvas.as-gl');
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!window.THREE || !canvas) { sec.classList.add('no-gl'); return; }
  var renderer;
  try { renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: false, alpha: false, powerPreference: 'high-performance' }); } catch (e) { renderer = null; }
  if (!renderer) { sec.classList.add('no-gl'); return; }

  var isMobile = Math.min(window.innerWidth, window.innerHeight) < 760;
  var cores = navigator.hardwareConcurrency || 4, mem = navigator.deviceMemory || 8;
  var lowEnd = isMobile || cores <= 4 || mem <= 4;
  var DPR = lowEnd ? 1 : Math.min(window.devicePixelRatio || 1, 1.5);
  renderer.setPixelRatio(DPR);
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.0;
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = lowEnd ? THREE.PCFShadowMap : THREE.PCFSoftShadowMap;

  // ---------- palette ----------
  var root = document.documentElement;
  function tok(name, fb) { var v = getComputedStyle(root).getPropertyValue(name).trim(); return v || fb; }
  function isDark() { return !root.classList.contains('light'); }
  var C = {};
  function readPalette() {
    C = { bg: tok('--bg', '#f8f3ec'), bg2: tok('--bg-2', '#f1e8dc'), surface: tok('--surface', '#fffdf9'), surface2: tok('--surface-2', '#f4ece0'),
      line: tok('--line', '#dccdbd'), text: tok('--text', '#3b0d14'), text2: tok('--text-2', '#4a2a2e'), muted: tok('--muted', '#7a4b4f'),
      a: tok('--violet', '#d8261c'), c: tok('--cyan', '#d9b26a'), m: tok('--mint', '#7fc08a'), inkA: tok('--ink-violet', '#be2313'), inkM: tok('--ink-mint', '#3c6d45'), dark: isDark() };
  }
  readPalette();
  // three r128 has no colour management: palette hex is sRGB, the renderer works in linear and
  // the final pass encodes, so every scene colour goes through lin()
  function lin(hex) { return new THREE.Color(hex).convertSRGBToLinear(); }

  // ---------- the twelve modules ----------
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
  var FLOW = [0, 2, 11, 1, 9];
  var FLOW_TAGS = ['Lead #2041 won', 'Invoice INV-0318', 'Stock −12 units', 'Incentive ₹4,200', 'In today’s report'];

  // ---------- screen textures: each module's UI painted on a canvas ----------
  var TW = 1024, TH = 640;
  function rr(x, c, X, Y, W, H, R) { x.beginPath(); x.moveTo(X + R, Y); x.arcTo(X + W, Y, X + W, Y + H, R); x.arcTo(X + W, Y + H, X, Y + H, R); x.arcTo(X, Y + H, X, Y, R); x.arcTo(X, Y, X + W, Y, R); x.closePath(); x.fillStyle = c; x.fill(); }
  function bar(x, c, X, Y, W, H) { rr(x, c, X, Y, W, H, H / 2); }
  function alpha(hex, a) { var h = hex.replace('#', ''); if (h.length === 3) h = h.split('').map(function (q) { return q + q; }).join(''); var n = parseInt(h, 16); return 'rgba(' + (n >> 16 & 255) + ',' + (n >> 8 & 255) + ',' + (n & 255) + ',' + a + ')'; }
  function hexOf(col) { var cc = new THREE.Color(col); return '#' + cc.getHexString(); }
  var FONT = '"Inter Tight", ui-sans-serif, system-ui, sans-serif', MONO = '"JetBrains Mono", ui-monospace, monospace';
  function paint(m, cv) {
    var tall = m.ui === 'phone', W = tall ? 420 : TW, H = tall ? 840 : TH;
    cv.width = W; cv.height = H;
    var x = cv.getContext('2d'), A = hexOf(C.a), Cc = hexOf(C.c), M = hexOf(C.m), T = hexOf(C.text), T2 = hexOf(C.text2), MU = hexOf(C.muted), S = hexOf(C.surface), S2 = hexOf(C.surface2), L = hexOf(C.line);
    x.fillStyle = S; x.fillRect(0, 0, W, H);
    // title bar
    x.fillStyle = S2; x.fillRect(0, 0, W, tall ? 64 : 76); x.fillStyle = L; x.fillRect(0, tall ? 63 : 75, W, 2);
    if (!tall) { [0, 1, 2].forEach(function (i) { x.beginPath(); x.arc(36 + i * 26, 38, 8, 0, 7); x.fillStyle = alpha(T, 0.18); x.fill(); }); }
    x.fillStyle = T; x.font = '600 30px ' + FONT; x.textBaseline = 'middle'; x.textAlign = tall ? 'center' : 'left';
    x.fillText(m.n, tall ? W / 2 : 128, tall ? 33 : 39);
    if (!tall) { x.textAlign = 'right'; x.font = '500 18px ' + MONO; x.fillStyle = MU; x.fillText('RAGENAIZER', W - 32, 39); }
    x.textAlign = 'left';
    var P = 34, top = (tall ? 64 : 76) + 30, cw = W - P * 2;
    var accents = [A, Cc, M];
    var people = [['AM', 'Aarav Mehta'], ['PN', 'Priya Nair'], ['VS', 'Vikram Singh'], ['NK', 'Neha Kapoor']];
    function row(y, avatar, name, val, pill, i) {
      if (avatar) { x.beginPath(); x.arc(P + 22, y, 20, 0, 7); x.fillStyle = accents[i % 3]; x.fill(); x.fillStyle = '#fff'; x.font = '700 15px ' + FONT; x.textAlign = 'center'; x.fillText(avatar, P + 22, y + 1); x.textAlign = 'left'; }
      x.fillStyle = T2; x.font = '500 24px ' + FONT; x.fillText(name, P + (avatar ? 60 : 0), y);
      if (val) { x.fillStyle = T; x.font = '600 23px ' + MONO; x.textAlign = 'right'; x.fillText(val, W - P - (pill ? 120 : 0), y); x.textAlign = 'left'; }
      if (pill) { rr(x, alpha(pill[1], 0.18), W - P - 100, y - 18, 100, 36, 18); x.fillStyle = pill[1]; x.font = '700 17px ' + FONT; x.textAlign = 'center'; x.fillText(pill[0], W - P - 50, y + 1); x.textAlign = 'left'; }
      x.fillStyle = L; x.fillRect(P, y + 36, cw, 2);
    }
    switch (m.ui) {
      case 'pipeline':
        [['NEW', 3], ['QUALIFIED', 2], ['PROPOSAL', 2], ['WON', 1]].forEach(function (c, i) {
          var cx = P + i * (cw / 4), w = cw / 4 - 16;
          rr(x, alpha(T, 0.04), cx, top, w, H - top - 30, 14);
          x.fillStyle = MU; x.font = '600 17px ' + MONO; x.fillText(c[0], cx + 16, top + 30);
          for (var k = 0; k < c[1]; k++) { var y = top + 58 + k * 128; rr(x, S, cx + 12, y, w - 24, 112, 10); bar(x, alpha(T, 0.14), cx + 28, y + 22, w - 90, 12); bar(x, alpha(T, 0.08), cx + 28, y + 44, w - 120, 10); x.fillStyle = A; x.font = '700 22px ' + MONO; x.fillText(['₹ 1.2L', '₹ 2.4L', '₹ 6.1L', '₹ 4.2L'][i], cx + 28, y + 84); }
        });
        break;
      case 'payroll':
        x.fillStyle = MU; x.font = '500 22px ' + FONT; x.fillText('Payroll · October', P, top + 8);
        x.fillStyle = T; x.font = '600 40px ' + MONO; x.textAlign = 'right'; x.fillText('₹ 18,42,000', W - P, top + 10); x.textAlign = 'left';
        people.forEach(function (p, i) { row(top + 90 + i * 98, p[0], p[1], ['₹ 62,400', '₹ 48,900', '₹ 71,250', '₹ 39,800'][i], [i === 3 ? 'Due' : 'Paid', i === 3 ? Cc : M], i); });
        break;
      case 'ledger':
        x.fillStyle = MU; x.font = '500 22px ' + FONT; x.fillText('Journal · 17 Oct', P, top + 8);
        x.fillStyle = M; x.font = '700 24px ' + FONT; x.textAlign = 'right'; x.fillText('Balanced ✓', W - P, top + 8); x.textAlign = 'left';
        [['Sales · GST 18%', '', '2,95,000'], ['Bank · HDFC', '2,95,000', ''], ['Stock in hand', '', '1,12,000'], ['Cost of goods', '1,12,000', '']].forEach(function (r, i) {
          var y = top + 90 + i * 98; x.fillStyle = T2; x.font = '500 24px ' + FONT; x.fillText(r[0], P, y);
          x.fillStyle = T; x.font = '600 23px ' + MONO; x.textAlign = 'right'; x.fillText(r[1], W - P - 210, y); x.fillText(r[2], W - P, y); x.textAlign = 'left'; x.fillStyle = L; x.fillRect(P, y + 36, cw, 2);
        });
        break;
      case 'gantt':
        [['Discovery', 0, .22], ['Design', .14, .3], ['Build · API', .3, .44], ['Build · UI', .4, .4], ['QA', .7, .2], ['Launch', .88, .1]].forEach(function (t, i) {
          var y = top + 20 + i * 76; x.fillStyle = T2; x.font = '500 23px ' + FONT; x.fillText(t[0], P, y + 12);
          var gx = P + 210, gw = cw - 210; bar(x, alpha(T, 0.06), gx, y, gw, 26); bar(x, accents[i % 3], gx + gw * t[1], y, gw * t[2], 26);
        });
        break;
      case 'courses':
        [['POSH compliance', 1], ['GST for sales teams', .64], ['Safety induction', .82], ['New CRM workflow', .3]].forEach(function (c, i) {
          var y = top + 30 + i * 112; x.fillStyle = T; x.font = '600 25px ' + FONT; x.fillText(c[0], P, y);
          bar(x, alpha(T, 0.08), P, y + 30, cw - 110, 16); bar(x, M, P, y + 30, (cw - 110) * c[1], 16);
          x.fillStyle = T2; x.font = '600 22px ' + MONO; x.textAlign = 'right'; x.fillText(Math.round(c[1] * 100) + '%', W - P, y + 38); x.textAlign = 'left';
        });
        break;
      case 'chat':
        [['Dashboard for Northline is up — can you check the totals?', 0], ['Looks right. Shipping it to the client.', 1], ['Great, I’ll start the invoice.', 0]].forEach(function (b, i) {
          x.font = '500 24px ' + FONT; var tw = Math.min(cw * 0.72, x.measureText(b[0]).width + 44), bx = b[1] ? W - P - tw : P, by = top + 10 + i * 140;
          rr(x, b[1] ? A : alpha(T, 0.07), bx, by, tw, 96, 22); x.fillStyle = b[1] ? '#fff' : T2;
          var words = b[0].split(' '), line = '', ly = by + 38; words.forEach(function (w) { if (x.measureText(line + w).width > tw - 44) { x.fillText(line, bx + 22, ly); line = ''; ly += 32; } line += w + ' '; }); x.fillText(line, bx + 22, ly);
        });
        break;
      case 'files':
        ['GST-Oct.pdf', 'Payroll.xlsx', 'Brief.docx', 'Logo.svg', 'Q3-deck.pdf', 'Stock.csv', 'Contract.pdf', 'Photos'].forEach(function (f, i) {
          var col = i % 4, r = Math.floor(i / 4), fw = cw / 4 - 18, fx = P + col * (cw / 4), fy = top + r * 230;
          rr(x, alpha(T, 0.04), fx, fy, fw, 200, 14); rr(x, alpha(accents[i % 3], 0.25), fx + fw / 2 - 40, fy + 30, 80, 100, 8); x.fillStyle = accents[i % 3]; x.fillRect(fx + fw / 2 - 40, fy + 30, 80, 16);
          x.fillStyle = T2; x.font = '500 21px ' + FONT; x.textAlign = 'center'; x.fillText(f, fx + fw / 2, fy + 168); x.textAlign = 'left';
        });
        break;
      case 'inbox':
        [['Northline Traders', 'Re: revised quotation', '10:42', 1], ['GST portal', 'Return filed for September', '09:15', 1], ['Priya Nair', 'Leave request · 2 days', 'Yest', 0], ['Razorpay', 'Payout settled ₹2.95L', 'Yest', 0]].forEach(function (r, i) {
          var y = top + 30 + i * 112; if (r[3]) { x.beginPath(); x.arc(P + 8, y, 8, 0, 7); x.fillStyle = A; x.fill(); }
          x.fillStyle = T; x.font = '700 25px ' + FONT; x.fillText(r[0], P + 32, y); x.fillStyle = T2; x.font = '500 22px ' + FONT; x.fillText(r[1], P + 32, y + 36);
          x.fillStyle = MU; x.font = '500 20px ' + MONO; x.textAlign = 'right'; x.fillText(r[2], W - P, y); x.textAlign = 'left'; x.fillStyle = L; x.fillRect(P, y + 62, cw, 2);
        });
        break;
      case 'bars':
        x.fillStyle = MU; x.font = '500 22px ' + FONT; x.fillText('Survey · 1,240 responses', P, top + 8);
        x.fillStyle = T; x.font = '600 36px ' + MONO; x.textAlign = 'right'; x.fillText('+18%', W - P, top + 10); x.textAlign = 'left';
        [44, 70, 52, 88, 61, 95, 73, 58].forEach(function (h, i) { var bw = cw / 8 - 18, bh = (H - top - 120) * h / 100; rr(x, accents[i % 3], P + i * (cw / 8), H - 50 - bh, bw, bh, 8); });
        x.fillStyle = L; x.fillRect(P, H - 48, cw, 2);
        break;
      case 'copilot':
        rr(x, alpha(T, 0.05), P, top, cw, 76, 16); x.fillStyle = T; x.font = '500 26px ' + FONT; x.fillText('Which invoices are overdue this week?', P + 26, top + 40);
        ['accounts.search_invoices', 'crm.lookup_customer'].forEach(function (c, i) { x.font = '600 18px ' + MONO; var w = x.measureText(c).width + 30; var cx = P + (i ? 360 : 0); rr(x, alpha(Cc, 0.2), cx, top + 104, w, 40, 8); x.fillStyle = Cc; x.fillText(c, cx + 15, top + 125); });
        [0.92, 0.8, 0.66].forEach(function (w, i) { bar(x, alpha(T, i ? 0.08 : 0.14), P, top + 184 + i * 40, cw * w, 16); });
        bar(x, A, P, top + 320, cw * 0.4, 16);
        break;
      case 'phone':
        x.fillStyle = MU; x.font = '600 18px ' + MONO; x.fillText('9:41', P, top - 6);
        rr(x, A, P, top + 20, cw, 170, 24); x.fillStyle = '#fff'; x.font = '500 22px ' + FONT; x.fillText('Clocked in · 09:02', P + 24, top + 70); x.font = '700 34px ' + MONO; x.fillText('Geofence OK', P + 24, top + 128);
        ['Approve leave · Priya', 'New lead · Kumar Ent.', 'Call back · Vikram'].forEach(function (t, i) {
          var y = top + 260 + i * 110; x.beginPath(); x.arc(P + 22, y, 20, 0, 7); x.fillStyle = accents[(i + 1) % 3]; x.fill();
          x.fillStyle = T2; x.font = '500 22px ' + FONT; x.fillText(t, P + 58, y + 2); x.fillStyle = L; x.fillRect(P, y + 46, cw, 2);
        });
        break;
      case 'shop':
        ['₹ 1,299', '₹ 849', '₹ 2,450', '₹ 599', '₹ 1,050', '₹ 3,200'].forEach(function (p, i) {
          var col = i % 3, r = Math.floor(i / 3), fw = cw / 3 - 18, fx = P + col * (cw / 3), fy = top + r * 245;
          var g = x.createLinearGradient(fx, fy, fx + fw, fy + 150); g.addColorStop(0, alpha(accents[i % 3], 0.35)); g.addColorStop(1, alpha(accents[(i + 1) % 3], 0.3));
          rr(x, g, fx, fy, fw, 150, 14); x.fillStyle = T; x.font = '700 26px ' + MONO; x.fillText(p, fx + 4, fy + 196);
        });
        break;
    }
  }

  // ---------- scene ----------
  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(isMobile ? 52 : 38, 1, 0.1, 200);
  var bgCol = lin(C.bg); scene.background = bgCol; scene.fog = new THREE.FogExp2(bgCol.getHex(), 0.028);
  var hemi = new THREE.HemisphereLight(0xffffff, 0x444444, 0.55); scene.add(hemi);
  var key = new THREE.DirectionalLight(0xffffff, 1.15); key.position.set(6, 12, 8); key.castShadow = true;
  key.shadow.mapSize.set(lowEnd ? 1024 : 2048, lowEnd ? 1024 : 2048);
  var sc = key.shadow.camera; sc.left = -18; sc.right = 18; sc.top = 18; sc.bottom = -18; sc.near = 1; sc.far = 50; key.shadow.bias = -0.0004;
  scene.add(key); key.target.position.set(0, 0, -8); scene.add(key.target);
  var rimA = new THREE.PointLight(0xffffff, 1.4, 26, 2); rimA.position.set(-7, 4, -6); scene.add(rimA);
  var rimB = new THREE.PointLight(0xffffff, 1.0, 26, 2); rimB.position.set(7, 3, -16); scene.add(rimB);

  // floor: a real mirror under a tinted glaze, so the reflection reads as polished stone
  var floorY = 0, mirror = null;
  if (!lowEnd && THREE.Reflector) {
    mirror = new THREE.Reflector(new THREE.PlaneGeometry(120, 120), { textureWidth: Math.round(window.innerWidth * DPR * 0.5), textureHeight: Math.round(window.innerHeight * DPR * 0.5), color: 0x8a8a8a });
    mirror.rotation.x = -Math.PI / 2; mirror.position.y = floorY - 0.002; scene.add(mirror);
  }
  var glaze = new THREE.Mesh(new THREE.PlaneGeometry(120, 120), new THREE.MeshStandardMaterial({ color: bgCol.clone(), roughness: 0.55, metalness: 0.0, transparent: !!mirror, opacity: mirror ? 0.82 : 1 }));
  glaze.rotation.x = -Math.PI / 2; glaze.position.y = floorY; glaze.receiveShadow = true; scene.add(glaze);
  // floor grid lines, faint
  var grid = new THREE.GridHelper(120, 60, 0x000000, 0x000000); grid.position.y = floorY + 0.003; grid.material.transparent = true; grid.material.opacity = 0.06; scene.add(grid);

  // the monoliths
  var SW = 3.0, SH = 1.875, D = 0.09;
  var bodyMat = new THREE.MeshPhysicalMaterial({ color: 0x111111, roughness: 0.25, metalness: 0.6, clearcoat: 1, clearcoatRoughness: 0.12 });
  var rimMat = new THREE.MeshStandardMaterial({ color: lin(C.a), emissive: lin(C.a), emissiveIntensity: 0.6, roughness: 0.4 });
  var slabs = MODS.map(function (m, i) {
    var tall = m.ui === 'phone', w = tall ? 0.95 : SW, h = tall ? 1.9 : SH;
    var g = new THREE.Group();
    var body = new THREE.Mesh(new THREE.BoxGeometry(w + 0.08, h + 0.08, D), bodyMat); body.castShadow = true; body.receiveShadow = true; g.add(body);
    var cv = document.createElement('canvas'); paint(m, cv);
    var tex = new THREE.CanvasTexture(cv); tex.encoding = THREE.sRGBEncoding; tex.anisotropy = 4;
    var scr = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshStandardMaterial({ map: tex, emissive: 0xffffff, emissiveMap: tex, emissiveIntensity: 0.55, roughness: 0.32, metalness: 0 }));
    scr.position.z = D / 2 + 0.002; g.add(scr);
    var rim = new THREE.Mesh(new THREE.BoxGeometry(w + 0.1, 0.018, D + 0.01), rimMat); rim.position.y = -(h / 2 + 0.05); g.add(rim);
    scene.add(g);
    return { g: g, m: m, cv: cv, tex: tex, scr: scr, w: w, h: h, glow: 0 };
  });
  function repaint() { slabs.forEach(function (s) { paint(s.m, s.cv); s.tex.needsUpdate = true; }); }

  // avenue: pairs facing the aisle, receding into the fog
  var AV = slabs.map(function (s, i) {
    var side = i % 2 ? 1 : -1;
    var pos = new THREE.Vector3(side * 2.1, s.h / 2 + 0.32, -i * 2.6 - 1.5);
    var q = new THREE.Quaternion().setFromEuler(new THREE.Euler(0, -side * 0.5, 0));
    return { pos: pos, q: q, side: side };
  });
  // wall: one 4x3 screen, high above the floor
  var WALL_C = new THREE.Vector3(0, 4.3, -11), GAP = 0.14;
  var WL = slabs.map(function (s, i) {
    var c = i % 4, r = Math.floor(i / 4);
    return { pos: new THREE.Vector3(WALL_C.x + (c - 1.5) * (SW + GAP), WALL_C.y + (1 - r) * (SH + GAP), WALL_C.z), q: new THREE.Quaternion() };
  });
  var bezel = new THREE.Mesh(new THREE.BoxGeometry(4 * SW + 3 * GAP + 0.5, 3 * SH + 2 * GAP + 0.5, 0.06), new THREE.MeshPhysicalMaterial({ color: 0x0b0b0b, roughness: 0.35, metalness: 0.5, clearcoat: 1 }));
  bezel.position.copy(WALL_C).add(new THREE.Vector3(0, 0, -0.09)); bezel.scale.set(0.001, 0.001, 1); bezel.castShadow = true; scene.add(bezel);

  // the record that travels across the wall
  var pulse = new THREE.Mesh(new THREE.SphereGeometry(0.09, 20, 16), new THREE.MeshBasicMaterial({ color: 0xffffff }));
  var pulseLight = new THREE.PointLight(0xffffff, 0, 6, 2); pulse.add(pulseLight); scene.add(pulse);
  var trailN = 40, trailGeo = new THREE.BufferGeometry(), trailPos = new Float32Array(trailN * 3);
  trailGeo.setAttribute('position', new THREE.BufferAttribute(trailPos, 3));
  var trail = new THREE.Line(trailGeo, new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.85 })); scene.add(trail);
  var flowPts = FLOW.map(function (i) { return WL[i].pos.clone().add(new THREE.Vector3(0, 0, 0.35)); });
  var flowCurve = new THREE.CatmullRomCurve3(flowPts, false, 'centripetal', 0.3);

  // dust in the air: catches the light, gives the space depth
  var DUSTN = lowEnd ? 600 : 1600, dg = new THREE.BufferGeometry(), dp = new Float32Array(DUSTN * 3);
  for (var i = 0; i < DUSTN; i++) { dp[i * 3] = (Math.random() - 0.5) * 26; dp[i * 3 + 1] = Math.random() * 9; dp[i * 3 + 2] = -Math.random() * 30 + 6; }
  dg.setAttribute('position', new THREE.BufferAttribute(dp, 3));
  var dust = new THREE.Points(dg, new THREE.PointsMaterial({ size: 0.035, transparent: true, opacity: 0.5, depthWrite: false })); scene.add(dust);

  // ---------- post: depth of field, bloom, grain + vignette ----------
  var composer = new THREE.EffectComposer(renderer);
  composer.addPass(new THREE.RenderPass(scene, camera));
  var bokeh = null;
  if (!lowEnd && THREE.BokehPass) { bokeh = new THREE.BokehPass(scene, camera, { focus: 6, aperture: 0.0026, maxblur: 0.0065, width: 1, height: 1 }); composer.addPass(bokeh); }
  var bloom = new THREE.UnrealBloomPass(new THREE.Vector2(1, 1), 0.5, 0.55, 0.82); composer.addPass(bloom);
  var finalPass = new THREE.ShaderPass({
    uniforms: { tDiffuse: { value: null }, uTime: { value: 0 }, uVig: { value: new THREE.Color(0.86, 0.86, 0.86) } },
    vertexShader: 'varying vec2 vUv; void main(){ vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }',
    fragmentShader: 'uniform sampler2D tDiffuse; uniform float uTime; uniform vec3 uVig; varying vec2 vUv; void main(){ vec4 c=texture2D(tDiffuse,vUv); vec3 col=pow(max(c.rgb,0.0),vec3(1.0/2.2)); vec2 q=vUv-0.5; float v=smoothstep(1.0,0.32,length(q*vec2(1.0,0.85))*1.3); col=mix(col*uVig,col,v); float g=fract(sin(dot(gl_FragCoord.xy+mod(uTime*61.0,97.0),vec2(12.9898,78.233)))*43758.5453); col+=(g-0.5)*0.035; gl_FragColor=vec4(col,1.0); }'
  });
  composer.addPass(finalPass);

  function applyPalette() {
    readPalette();
    bgCol.copy(lin(C.bg)); scene.fog.color.copy(bgCol); glaze.material.color.copy(lin(C.dark ? C.bg : C.bg2)).multiplyScalar(C.dark ? 1 : 0.92);
    var acc = lin(C.a), sec2 = lin(C.c);
    rimMat.color.copy(acc); rimMat.emissive.copy(acc);
    rimA.color.copy(acc); rimB.color.copy(sec2);
    pulse.material.color.copy(acc).lerp(new THREE.Color(1, 1, 1), 0.35); pulseLight.color.copy(acc); trail.material.color.copy(acc);
    hemi.color.copy(lin(C.dark ? '#c9cfe0' : '#ffffff')); hemi.groundColor.copy(bgCol); hemi.intensity = C.dark ? 0.35 : 0.55;
    key.intensity = C.dark ? 0.9 : 1.5; key.shadow.radius = 4;
    renderer.toneMappingExposure = C.dark ? 1.05 : 0.98;
    bodyMat.color.copy(lin(C.dark ? '#0d0f14' : '#1a1416'));
    slabs.forEach(function (s) { s.scr.material.emissiveIntensity = C.dark ? 0.42 : 0.3; });
    bloom.threshold = C.dark ? 0.78 : 0.92; bloom.strength = C.dark ? 0.45 : 0.3;
    grid.material.color.set(C.dark ? '#ffffff' : '#000000'); grid.material.opacity = C.dark ? 0.05 : 0.06;
    dust.material.color.copy(lin(C.dark ? '#ffffff' : C.text)); dust.material.opacity = C.dark ? 0.45 : 0.25;
    var b = new THREE.Color(C.bg), sh = new THREE.Color(C.dark ? '#000000' : C.line);
    var vr = C.dark ? 0.62 : 0.5 + 0.5 * sh.r / Math.max(0.01, b.r), vg = C.dark ? 0.62 : 0.5 + 0.5 * sh.g / Math.max(0.01, b.g), vb = C.dark ? 0.62 : 0.5 + 0.5 * sh.b / Math.max(0.01, b.b); finalPass.uniforms.uVig.value.set(vr, vg, vb);
    repaint();
  }
  applyPalette();
  new MutationObserver(function () { applyPalette(); }).observe(root, { attributes: true, attributeFilter: ['class', 'data-palette'] });

  // ---------- timeline ----------
  var T = { carIn: [0.9, 1.6], car: [1.6, 5.4], pull: [5.4, 5.85], dock: [5.75, 6.55], flow: [6.95, 8.0], end: 9.2 };
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function fit(v, r) { return clamp((v - r[0]) / (r[1] - r[0]), 0, 1); }
  function ease(t) { return t * t * (3 - 2 * t); }
  function easeIO(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }

  var vw = 1, vh = 1, mobile = isMobile;
  function resize() {
    vw = stage.clientWidth; vh = stage.clientHeight; mobile = vw < 760;
    renderer.setSize(vw, vh, false); composer.setSize(vw, vh); camera.aspect = vw / vh; camera.fov = mobile ? 58 : 38; camera.updateProjectionMatrix();
    if (bokeh) { bokeh.uniforms.aspect.value = vw / vh; }
  }

  // camera shots
  var tmpQ = new THREE.Quaternion(), tmpV = new THREE.Vector3(), up = new THREE.Vector3(0, 1, 0);
  function slabShot(i) { // close on module i, framed to the right of the copy
    var a = AV[i], n = new THREE.Vector3(0, 0, 1).applyQuaternion(a.q), r = new THREE.Vector3(1, 0, 0).applyQuaternion(a.q);
    var dist = mobile ? 6.0 : 5.6, pos = a.pos.clone().addScaledVector(n, dist).add(new THREE.Vector3(0, 0.25, 0));
    var tgt = a.pos.clone().addScaledVector(r, mobile ? 0 : -1.0).add(new THREE.Vector3(0, mobile ? -0.55 : 0, 0));
    return { pos: pos, tgt: tgt, focus: dist };
  }
  var HERO = { pos: new THREE.Vector3(-0.6, 0.75, 6.4), tgt: new THREE.Vector3(1.9, 1.5, -22), focus: 10 };
  function wallShot() { return { pos: new THREE.Vector3(mobile ? 0 : -2.2, WALL_C.y + 0.6, WALL_C.z + (mobile ? 21 : 19)), tgt: new THREE.Vector3(mobile ? 0 : -5.6, WALL_C.y - (mobile ? 1.6 : 0.1), WALL_C.z), focus: 15 }; }
  function tiltShot(t) { // the camera swings low and to the side, the wall towering above
    var a = -0.55 + 0.35 * t;
    return { pos: new THREE.Vector3(WALL_C.x + Math.sin(a) * 13, 1.4 + 0.6 * t, WALL_C.z + Math.cos(a) * 13), tgt: new THREE.Vector3(mobile ? 0 : -3.4, WALL_C.y + 0.2, WALL_C.z), focus: 13 };
  }
  function endShot() { return { pos: new THREE.Vector3(mobile ? 0 : 5.5, 9.5, WALL_C.z + 17), tgt: new THREE.Vector3(mobile ? 0 : -3.4, WALL_C.y - 1.2, WALL_C.z), focus: 19 }; }
  function lerpShot(a, b, t) { return { pos: a.pos.clone().lerp(b.pos, t), tgt: a.tgt.clone().lerp(b.tgt, t), focus: a.focus + (b.focus - a.focus) * t }; }

  // ---------- copy ----------
  var copies = [].slice.call(sec.querySelectorAll('.as-copy'));
  var modName = sec.querySelector('[data-mod-name]'), modDesc = sec.querySelector('[data-mod-desc]'), modNum = sec.querySelector('[data-mod-num]'), modLink = sec.querySelector('[data-mod-link]');
  var steps = [].slice.call(sec.querySelectorAll('.as-steps li')), tag = sec.querySelector('.as-tag');
  var shown = -1;
  function setMod(i) { if (i === shown) return; shown = i; var m = MODS[i]; modName.textContent = m.n; modDesc.textContent = m.d; modNum.textContent = String(i + 1).padStart(2, '0'); modLink.href = m.href; }

  // ---------- frame ----------
  function secTop() { return sec.getBoundingClientRect().top + window.scrollY; }
  var seekTo = null; sec.__seek = function (v) { seekTo = v; sCur = v; };
  function target() { return seekTo !== null ? seekTo : clamp((window.scrollY - secTop()) / vh, 0, T.end); }
  var sCur = 0, last = performance.now(), t0 = last, visible = true;
  new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }, { rootMargin: '200px 0px' }).observe(sec);
  var proj = new THREE.Vector3();

  function frame(now) {
    requestAnimationFrame(frame);
    var dt = Math.min(0.05, (now - last) / 1000); last = now;
    if (!visible) return;
    var tg = target(); sCur = reduced ? tg : sCur + (tg - sCur) * (1 - Math.exp(-dt * 5));
    var s = sCur, time = (now - t0) / 1000;
    var a = clamp(fit(s, T.car) * 11, 0, 11), ai = Math.round(a);
    var eIn = easeIO(fit(s, T.carIn)), eDock = fit(s, T.dock), flow = fit(s, T.flow);

    // slabs: avenue -> wall, each with its own delay and an arc through the air
    slabs.forEach(function (sl, i) {
      var lag = (i / 11) * 0.45, t = easeIO(clamp((eDock - lag) / 0.55, 0, 1));
      var p = AV[i].pos.clone().lerp(WL[i].pos, t); p.y += Math.sin(t * Math.PI) * 3.4; p.z -= Math.sin(t * Math.PI) * 2.5;
      var bob = (1 - t) * Math.sin(time * 0.7 + i) * 0.03; p.y += bob;
      sl.g.position.copy(p); sl.g.quaternion.copy(AV[i].q).slerp(WL[i].q, t);
      // the module on stage glows; on the wall the flow lights its stops
      var on = eDock < 0.02 && s > T.carIn[0] && i === ai ? 1 : 0;
      var lit = flow > 0 && FLOW.indexOf(i) >= 0 && FLOW.indexOf(i) <= Math.floor(flow * FLOW.length - 0.001) ? 1 : 0;
      sl.glow += ((on || lit) - sl.glow) * (1 - Math.exp(-dt * 6));
      sl.scr.material.emissiveIntensity = (C.dark ? 0.42 : 0.3) + sl.glow * (C.dark ? 0.3 : 0.25);
    });
    var bz = easeIO(fit(s, [T.dock[0] + 0.55, T.dock[1] + 0.1])); bezel.scale.set(Math.max(0.001, bz), Math.max(0.001, bz), 1);

    // camera: hero -> through the avenue -> back for the wall -> low and to the side -> high
    var shot;
    if (s < T.carIn[0]) shot = HERO;
    else if (s < T.car[0]) shot = lerpShot(HERO, slabShot(0), eIn);
    else if (s < T.pull[0]) { var i0 = Math.floor(a), i1 = Math.min(11, i0 + 1), f = easeIO(a - i0); shot = lerpShot(slabShot(i0), slabShot(i1), f); }
    else if (s < T.dock[1] + 0.3) shot = lerpShot(slabShot(11), wallShot(), easeIO(fit(s, [T.pull[0], T.pull[1]])));
    else if (s < T.flow[0]) shot = lerpShot(wallShot(), tiltShot(0), easeIO(fit(s, [T.dock[1] + 0.3, T.flow[0]])));
    else if (s < T.flow[1] + 0.3) shot = tiltShot(fit(s, [T.flow[0], T.flow[1] + 0.3]));
    else shot = lerpShot(tiltShot(1), endShot(), easeIO(fit(s, [T.flow[1] + 0.3, T.end - 0.2])));
    camera.position.copy(shot.pos); camera.lookAt(shot.tgt);
    if (!reduced) { camera.position.x += Math.sin(time * 0.21) * 0.06; camera.position.y += Math.sin(time * 0.17) * 0.04; }
    if (bokeh) { bokeh.uniforms.focus.value = shot.focus; }

    // pulse along the flow
    var fl = clamp(flow * 1.04, 0, 1), showP = flow > 0.01 && flow < 0.999 ? 1 : 0;
    var pt = flowCurve.getPointAt(fl); pulse.position.copy(pt); pulse.visible = !!showP || (flow >= 0.999 && s < T.flow[1] + 0.4);
    pulseLight.intensity = pulse.visible ? 2.2 : 0;
    for (var k = 0; k < trailN; k++) { var u = clamp(fl - k * 0.006, 0, 1), q = flowCurve.getPointAt(u); trailPos[k * 3] = q.x; trailPos[k * 3 + 1] = q.y; trailPos[k * 3 + 2] = q.z; }
    trailGeo.attributes.position.needsUpdate = true; trail.visible = pulse.visible;
    var stepI = Math.min(FLOW.length - 1, Math.floor(flow * FLOW.length));
    if (tag) {
      proj.copy(pt).project(camera);
      tag.style.transform = 'translate(' + ((proj.x * 0.5 + 0.5) * vw).toFixed(1) + 'px,' + ((-proj.y * 0.5 + 0.5) * vh - 26).toFixed(1) + 'px) translate(-50%,-100%)';
      tag.style.opacity = pulse.visible && flow > 0.02 ? 1 : 0; tag.textContent = FLOW_TAGS[stepI];
    }
    steps.forEach(function (li, j) { li.classList.toggle('on', flow > 0 && j <= stepI); });

    // dust drifts
    dust.rotation.y = time * 0.01;

    // copy
    copies.forEach(function (c) {
      var r = c.dataset.range.split(',').map(parseFloat), fade = 0.28;
      var o = r[0] <= 0 ? 1 - fit(s, [r[1], r[1] + fade]) : r[1] >= T.end ? fit(s, [r[0] - fade, r[0]]) : Math.min(fit(s, [r[0] - fade, r[0]]), 1 - fit(s, [r[1], r[1] + fade]));
      c.style.opacity = o.toFixed(3);
      c.style.transform = mobile ? 'translateY(' + ((1 - o) * 16).toFixed(1) + 'px)' : 'translateY(calc(-46% + ' + ((1 - o) * 16).toFixed(1) + 'px))';
      c.classList.toggle('on', o > 0.5);
    });
    setMod(ai);
    var hint = sec.querySelector('.as-hint'); if (hint) hint.style.opacity = 1 - fit(s, [0.05, 0.4]);

    finalPass.uniforms.uTime.value = time;
    composer.render();
  }

  resize(); window.addEventListener('resize', resize);
  sCur = target();
  requestAnimationFrame(function (now) { last = now; requestAnimationFrame(frame); });
  sec.classList.add('gl');
})();
