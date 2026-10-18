/* Services — "Draughtsman" (animation style 04).
   A brass pantograph arm draws each service in ink on a drafting sheet: the brief, a web
   portal, a phone, an agent network, a dashboard, the sprint timeline. Each sheet gets a soft
   wash and a hand-lettered note, then slides onto a stack beside the board as the next sheet
   drops in. Same instrument vocabulary as How we build: brass, lacquer, ivory, a warm studio
   capture for reflections, soft shadows on a paper floor. Paper, ink and metals come from the
   site tokens, so palettes and light/dark re-skin it (dark mode reads as blueprint paper).
   Scroll is in viewport heights (s), eased each frame; the opening sheet draws itself on load. */
(function () {
  var sec = document.getElementById('blueprint'); if (!sec) return;
  var stage = sec.querySelector('.bp-stage'), canvas = sec.querySelector('canvas.bp-gl');
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!window.THREE || !window.SceneKit || !canvas) { sec.classList.add('no-gl'); return; }
  var dev = SceneKit.device(), isMobile = dev.isMobile, lowEnd = dev.lowEnd;
  var renderer = SceneKit.renderer(canvas, dev);
  if (!renderer) { sec.classList.add('no-gl'); return; }
  var ANISO = SceneKit.maxAniso(renderer);

  // ---------- palette ----------
  var root = document.documentElement, C = {};
  function tok(n, fb) { return getComputedStyle(root).getPropertyValue(n).trim() || fb; }
  function readPalette() {
    C = { bg: tok('--bg', '#f8f3ec'), paper: tok('--surface', '#fffdf9'), paper2: tok('--surface-2', '#f4ece0'), ink: tok('--text', '#3b0d14'), ink2: tok('--text-2', '#4a2a2e'), muted: tok('--muted', '#7a4b4f'),
      line: tok('--line', '#dccdbd'), a: tok('--violet', '#d8261c'), inkA: tok('--ink-violet', '#be2313'), brass: tok('--brass-78', '#d9b26a'), brassD: tok('--brass-68', '#b8903f'), lacq: tok('--sindoor-39', '#7d1426'),
      board: tok('--taupe-20', '#2a0810'), dark: !root.classList.contains('light') };
  }
  readPalette();
  function lin(hex) { return new THREE.Color(hex).convertSRGBToLinear(); }
  function rgba(hex, a) { var c = new THREE.Color(hex); return 'rgba(' + Math.round(c.r * 255) + ',' + Math.round(c.g * 255) + ',' + Math.round(c.b * 255) + ',' + a + ')'; }

  // ---------- scene ----------
  var scene = new THREE.Scene(), bgCol = lin(C.bg);
  scene.background = bgCol; scene.fog = new THREE.FogExp2(bgCol.getHex(), 0.045);
  var camera = new THREE.PerspectiveCamera(30, 1, 0.05, 60);
  var hemi = new THREE.HemisphereLight(0xffffff, 0x444444, 0.7); scene.add(hemi);
  var key = new THREE.DirectionalLight(0xffffff, 1.3); key.position.set(3.2, 5.2, 2.6); key.castShadow = true;
  key.shadow.mapSize.set(lowEnd ? 2048 : 4096, lowEnd ? 2048 : 4096); var kc = key.shadow.camera; kc.near = 1; kc.far = 16; kc.left = kc.bottom = -4.6; kc.right = kc.top = 4.6;
  key.shadow.bias = -0.0005; key.shadow.normalBias = 0.02; key.shadow.radius = 5; scene.add(key);
  var fill = new THREE.DirectionalLight(0xffffff, 0.35); fill.position.set(-4, 2.5, -3); scene.add(fill);

  // a warm studio, captured once into a mip-mapped cube (the How we build recipe)
  (function makeEnv() {
    var env = new THREE.Scene();
    env.add(new THREE.Mesh(new THREE.SphereGeometry(20, 32, 16), new THREE.ShaderMaterial({ side: THREE.BackSide,
      uniforms: { uTop: { value: lin('#fff8ee') }, uMid: { value: lin('#e9d7c3') }, uBot: { value: lin('#2a1a1c') } },
      vertexShader: 'varying vec3 vP; void main(){ vP=normalize(position); gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }',
      fragmentShader: 'uniform vec3 uTop,uMid,uBot; varying vec3 vP; void main(){ float h=clamp(vP.y,-1.0,1.0); vec3 c=mix(mix(uMid,uBot,pow(max(-h,0.0),0.8)),uTop,pow(max(h,0.0),0.6)); gl_FragColor=vec4(c,1.0); }' })));
    function box(x, y, z, w, h, i) { var m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: new THREE.Color(i, i, i), side: THREE.DoubleSide })); m.position.set(x, y, z); m.lookAt(0, 0, 0); env.add(m); }
    box(4, 6, 3, 5, 3, 4); box(-6, 3, -4, 6, 2, 2.5); box(0, 2, 8, 8, 1.2, 2);
    var rt = new THREE.WebGLCubeRenderTarget(256, { generateMipmaps: true, minFilter: THREE.LinearMipmapLinearFilter, magFilter: THREE.LinearFilter });
    new THREE.CubeCamera(0.1, 60, rt).update(renderer, env); scene.environment = rt.texture;
  })();

  // floor: catches shadows only; the paper-coloured clear colour is the room
  var ground = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.ShadowMaterial({ opacity: 0.2 }));
  ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);

  // materials (colours set in applyPalette)
  var brass = new THREE.MeshStandardMaterial({ roughness: 0.24, metalness: 1.0, envMapIntensity: 1.4 });
  var brassDark = new THREE.MeshStandardMaterial({ roughness: 0.35, metalness: 1.0, envMapIntensity: 1.2 });
  var lacquer = new THREE.MeshPhysicalMaterial({ roughness: 0.22, metalness: 0.0, clearcoat: 1, clearcoatRoughness: 0.08, envMapIntensity: 1.2 });
  var boardMat = new THREE.MeshPhysicalMaterial({ roughness: 0.35, metalness: 0.0, clearcoat: 1, clearcoatRoughness: 0.12, envMapIntensity: 0.9 });
  var steel = new THREE.MeshStandardMaterial({ color: lin('#c9ccd1'), roughness: 0.28, metalness: 1.0, envMapIntensity: 1.3 });
  var nibMat = new THREE.MeshStandardMaterial({ color: lin('#1a1a1a'), roughness: 0.3, metalness: 0.8 });

  // the drafting board
  var BW = 4.7, BD = 3.25;
  var board = new THREE.Mesh(SceneKit.rbox(BW, BD, 0.09, 0.12, 0.03), boardMat); board.rotation.x = -Math.PI / 2; board.position.y = 0.045; board.castShadow = board.receiveShadow = true; scene.add(board);
  var boardEdge = new THREE.Mesh(new THREE.BoxGeometry(BW - 0.3, 0.012, 0.012), brass); boardEdge.position.set(0, 0.092, BD / 2 - 0.08); scene.add(boardEdge);
  var TOP = 0.092; // board surface height

  // engraved instrument textures: a steel rule and a brass protractor
  function engraveTex(w, h, draw) { var c = document.createElement('canvas'); c.width = w; c.height = h; var x = c.getContext('2d'); draw(x, w, h); var t = new THREE.CanvasTexture(c); t.encoding = THREE.sRGBEncoding; t.anisotropy = ANISO; return t; }
  var ruleTex = engraveTex(2048, 128, function (x, w, h) { x.fillStyle = '#c9ccd1'; x.fillRect(0, 0, w, h); x.strokeStyle = 'rgba(20,20,24,0.85)'; x.fillStyle = 'rgba(20,20,24,0.85)'; x.font = '600 26px "JetBrains Mono", monospace';
    for (var i = 0; i <= 300; i++) { var X = 24 + i * (w - 48) / 300, L = i % 10 === 0 ? 56 : i % 5 === 0 ? 38 : 22; x.lineWidth = i % 10 === 0 ? 3 : 1.6; x.beginPath(); x.moveTo(X, 0); x.lineTo(X, L); x.stroke(); if (i % 10 === 0) x.fillText(String(i / 10), X + 5, 92); } });
  ruleTex.repeat.set(1 / 3.2, 1 / 0.2); ruleTex.offset.set(0.5, 0.5); // extrude caps carry raw xy as uv
  var rule = new THREE.Mesh(SceneKit.rbox(3.2, 0.2, 0.018, 0.02, 0.006), [new THREE.MeshStandardMaterial({ map: ruleTex, roughness: 0.3, metalness: 0.9, envMapIntensity: 1.3 }), steel]);
  rule.rotation.x = -Math.PI / 2; rule.position.set(0.1, TOP + 0.009, BD / 2 - 0.26); rule.castShadow = rule.receiveShadow = true; scene.add(rule);
  var protTex = engraveTex(1024, 1024, function (x, w, h) { x.fillStyle = '#d9b45e'; x.fillRect(0, 0, w, h); x.translate(w / 2, h / 2); x.strokeStyle = 'rgba(40,24,6,0.85)'; x.fillStyle = 'rgba(40,24,6,0.85)'; x.font = '600 30px "JetBrains Mono", monospace'; x.textAlign = 'center';
    for (var d = 0; d <= 180; d++) { var a = Math.PI + d * Math.PI / 180, r1 = 470, r0 = d % 10 === 0 ? 410 : d % 5 === 0 ? 432 : 450; x.lineWidth = d % 10 === 0 ? 3 : 1.5; x.beginPath(); x.moveTo(Math.cos(a) * r0, Math.sin(a) * r0); x.lineTo(Math.cos(a) * r1, Math.sin(a) * r1); x.stroke(); if (d % 30 === 0) x.fillText(String(d), Math.cos(a) * 365, Math.sin(a) * 365 + 10); }
    x.lineWidth = 2; x.beginPath(); x.arc(0, 0, 300, Math.PI, 2 * Math.PI); x.stroke(); });
  var protractor = new THREE.Mesh(new THREE.CircleGeometry(0.62, 128, 0, Math.PI), new THREE.MeshStandardMaterial({ map: protTex, roughness: 0.28, metalness: 1, envMapIntensity: 1.3, side: THREE.DoubleSide }));
  protTex.offset.set(0, 0); protractor.rotation.x = -Math.PI / 2; protractor.rotation.z = -0.25; protractor.position.set(-1.72, TOP + 0.004, 1.02); protractor.receiveShadow = true; scene.add(protractor);
  var protEdge = new THREE.Mesh(new THREE.TorusGeometry(0.62, 0.006, 8, 160, Math.PI), brassDark); protEdge.rotation.copy(protractor.rotation); protEdge.position.copy(protractor.position); protEdge.position.y += 0.004; scene.add(protEdge);

  // ---------- drafting sheets ----------
  var SW = 3.6, SH = 2.4, PX = 1800, PY = 1200, K = SW / PX;   // world units per sheet pixel
  function toWorld(px, py, y) { return new THREE.Vector3((px / PX - 0.5) * SW, y, (py / PY - 0.5) * SH); }

  // stroke builders, in sheet pixels
  function rect(x, y, w, h, r) { r = r || 0; var p = [], k; function arc(cx, cy, a0) { for (k = 0; k <= 8; k++) { var a = a0 + k * Math.PI / 16; p.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]); } }
    if (!r) return [[x, y], [x + w, y], [x + w, y + h], [x, y + h], [x, y]];
    p.push([x + r, y]); p.push([x + w - r, y]); arc(x + w - r, y + r, -Math.PI / 2); p.push([x + w, y + h - r]); arc(x + w - r, y + h - r, 0); p.push([x + r, y + h]); arc(x + r, y + h - r, Math.PI / 2); p.push([x, y + r]); arc(x + r, y + r, Math.PI); return p; }
  function circ(cx, cy, r, a0, a1) { var p = [], n = 64; a0 = a0 || 0; a1 = a1 == null ? Math.PI * 2 : a1; for (var k = 0; k <= n; k++) { var a = a0 + (a1 - a0) * k / n; p.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]); } return p; }
  function curve(a, c, b) { var p = []; for (var k = 0; k <= 32; k++) { var t = k / 32, u = 1 - t; p.push([u * u * a[0] + 2 * u * t * c[0] + t * t * b[0], u * u * a[1] + 2 * u * t * c[1] + t * t * b[1]]); } return p; }
  function S(pts, o) { o = o || {}; return { type: 'stroke', pts: pts, w: o.w || 3.2, col: o.col || 'ink', dash: o.dash || null }; }
  function W(shape, o) { o = o || {}; return { type: 'wash', shape: shape, col: o.col || 'a', a: o.a || 0.14 }; }
  function Tx(x, y, str, o) { o = o || {}; return { type: 'text', x: x, y: y, str: str, size: o.size || 46, col: o.col || 'ink', italic: o.italic !== false, align: o.align || 'left', mono: !!o.mono }; }
  function arrow(x1, y1, x2, y2) { var a = Math.atan2(y2 - y1, x2 - x1), h = 22; return [S([[x1, y1], [x2, y2]], { w: 2.4 }), S([[x2 - Math.cos(a - 0.4) * h, y2 - Math.sin(a - 0.4) * h], [x2, y2], [x2 - Math.cos(a + 0.4) * h, y2 - Math.sin(a + 0.4) * h]], { w: 2.4 })]; }
  function dim(x1, y, x2, label) { return [S([[x1, y], [x2, y]], { w: 1.6, col: 'muted' }), S([[x1, y - 14], [x1, y + 14]], { w: 1.6, col: 'muted' }), S([[x2, y - 14], [x2, y + 14]], { w: 1.6, col: 'muted' }), Tx((x1 + x2) / 2, y - 20, label, { size: 24, col: 'muted', mono: true, italic: false, align: 'center' })]; }
  function flat(a) { return [].concat.apply([], a.map(function (x) { return Array.isArray(x) ? x : [x]; })); }

  var DRAW = {
    sheet: flat([
      S(circ(470, 520, 170)), Tx(470, 535, 'orders?', { align: 'center' }),
      S(rect(780, 330, 420, 280, 18), { col: 'a' }), Tx(990, 485, 'one screen', { align: 'center', col: 'a' }),
      S(circ(1390, 700, 150)), Tx(1390, 715, 'stock', { align: 'center' }),
      arrow(640, 470, 770, 440), arrow(1250, 640, 1205, 560),
      W(rect(780, 330, 420, 280, 18)),
      S(curve([380, 860], [800, 980], [1280, 900]), { w: 2.4, dash: [10, 12] }), Tx(820, 1010, 'what you tell us', { size: 34, col: 'muted', align: 'center' })
    ]),
    web: flat([
      S(rect(240, 170, 1320, 840, 26)), S([[240, 250], [1560, 250]], { w: 2.4 }),
      S(circ(290, 210, 10)), S(circ(325, 210, 10)), S(circ(360, 210, 10)), S(rect(450, 196, 520, 30, 15), { w: 2 }),
      S([[520, 250], [520, 1010]], { w: 2.4 }),
      S([[280, 320], [460, 320]], { w: 2 }), S([[280, 380], [430, 380]], { w: 2 }), S([[280, 440], [450, 440]], { w: 2 }), S([[280, 500], [410, 500]], { w: 2 }),
      S(rect(570, 300, 300, 150, 14), { col: 'a' }), S(rect(900, 300, 300, 150, 14)), S(rect(1230, 300, 290, 150, 14)),
      W(rect(570, 300, 300, 150, 14)),
      Tx(600, 360, 'Overdue', { size: 30, italic: false, col: 'muted' }), Tx(600, 420, '₹ 4.8L', { size: 44, italic: false, col: 'a', mono: true }),
      S(rect(570, 490, 950, 470, 12), { w: 2.4 }),
      S([[570, 560], [1520, 560]], { w: 1.6 }), S([[570, 640], [1520, 640]], { w: 1.6 }), S([[570, 720], [1520, 720]], { w: 1.6 }), S([[570, 800], [1520, 800]], { w: 1.6 }), S([[570, 880], [1520, 880]], { w: 1.6 }),
      dim(240, 120, 1560, '1440 PX · RESPONSIVE'), Tx(1150, 1080, 'Invoices — one query, one screen', { size: 40, align: 'center' })
    ]),
    mobile: flat([
      S(rect(690, 110, 420, 940, 64)), S(rect(840, 140, 120, 26, 13), { w: 2 }),
      S(circ(900, 380, 120), { col: 'a', dash: [14, 12] }), S(circ(900, 380, 9), { col: 'a' }), S([[900, 380], [985, 295]], { w: 1.6, col: 'muted' }),
      Tx(1000, 300, '150 m', { size: 30, italic: false, col: 'muted', mono: true }),
      S(rect(740, 560, 320, 90, 30), { col: 'a' }), W(rect(740, 560, 320, 90, 30), { a: 0.85 }), Tx(900, 616, 'Clock in · 09:02', { size: 32, italic: false, col: 'paper', align: 'center' }),
      S(circ(770, 720, 16)), S([[805, 712], [1020, 712]], { w: 2 }), S([[805, 735], [960, 735]], { w: 1.6 }),
      S(circ(770, 800, 16)), S([[805, 792], [1030, 792]], { w: 2 }), S([[805, 815], [940, 815]], { w: 1.6 }),
      S(circ(770, 880, 16)), S([[805, 872], [1000, 872]], { w: 2 }), S([[805, 895], [950, 895]], { w: 1.6 }),
      S([[640, 110], [640, 1050]], { w: 1.6, col: 'muted' }), Tx(620, 590, '390 pt', { size: 24, italic: false, col: 'muted', mono: true, align: 'right' }),
      Tx(1180, 420, 'works offline,', { size: 40 }), Tx(1180, 475, 'syncs when back', { size: 40 })
    ]),
    ai: (function () {
      var N = [[300, 640], [620, 380], [900, 700], [1200, 400], [1480, 640]], out = [];
      for (var i = 0; i < N.length - 1; i++) out.push(S(curve(N[i], [(N[i][0] + N[i + 1][0]) / 2, (N[i][1] + N[i + 1][1]) / 2 - 120], N[i + 1]), { w: 2.4 }));
      N.forEach(function (n, i) { out.push(S(circ(n[0], n[1], i === 2 ? 70 : 54), { col: i === 2 ? 'a' : 'ink' })); });
      out.push(W(circ(900, 700, 70), { a: 0.18 }));
      out.push(S(curve([1200, 340], [910, 140], [620, 320]), { w: 2, dash: [10, 10], col: 'muted' })); out.push(Tx(910, 205, 'checks itself', { size: 34, col: 'muted', align: 'center' }));
      [[760, 920], [900, 960], [1040, 920]].forEach(function (t) { out.push(S([[900, 770], [t[0], t[1] - 30]], { w: 1.6 })); out.push(S(rect(t[0] - 70, t[1] - 30, 140, 56, 10), { w: 2 })); });
      ['Question', 'Plan', 'Tools', 'Check', 'Answer'].forEach(function (l, i) { out.push(Tx(N[i][0], N[i][1] + (i === 2 ? 115 : 100), l, { size: 32, italic: false, col: 'muted', align: 'center' })); });
      out.push(Tx(900, 1080, 'plans · uses your systems · checks · acts', { size: 40, align: 'center' }));
      return out;
    })(),
    dash: flat([
      S([[300, 980], [1500, 980]]), S([[300, 280], [300, 980]]),
      S([[300, 805], [1500, 805]], { w: 1.2, col: 'muted', dash: [8, 10] }), S([[300, 630], [1500, 630]], { w: 1.2, col: 'muted', dash: [8, 10] }), S([[300, 455], [1500, 455]], { w: 1.2, col: 'muted', dash: [8, 10] }),
      (function () { var p = [], k; for (k = 0; k <= 60; k++) { var t = k / 60, x = 300 + t * 1200, y = 880 - t * 420 - Math.sin(t * 9) * 60 - Math.sin(t * 3.2) * 40; p.push([x, y]); } return [S(p, { col: 'a', w: 4 }), W(p.concat([[1500, 980], [300, 980]]), { a: 0.12 })]; })(),
      [0, 1, 2, 3, 4, 5, 6].map(function (i) { var h = [160, 240, 200, 300, 260, 360, 320][i], x = 360 + i * 160; return S(rect(x, 980 - h, 70, h, 4), { w: 2 }); }),
      Tx(330, 250, 'Revenue · live', { size: 40 }), Tx(1500, 250, 'updates in under a second', { size: 34, col: 'muted', align: 'right' })
    ]),
    process: (function () {
      var out = [S([[200, 640], [1600, 640]], { w: 3.6 })];
      for (var i = 0; i < 6; i++) { var x = 300 + i * 240; out.push(S([[x, 640], [x, 430]], { w: 2.4 })); out.push(S([[x, 430], [x + 110, 465], [x, 500]], { col: i === 5 ? 'a' : 'ink' })); if (i === 5) out.push(W([[x, 430], [x + 110, 465], [x, 500]], { a: 0.75 }));
        out.push(Tx(x, 700, 'WEEK ' + (i + 1) * 2, { size: 24, italic: false, col: 'muted', mono: true, align: 'center' })); out.push(Tx(x, 760, i === 5 ? 'Launch' : 'Demo ' + (i + 1), { size: 40, align: 'center', col: i === 5 ? 'a' : 'ink' })); }
      out.push(Tx(900, 940, 'a working build in your hands every fortnight', { size: 42, align: 'center' }));
      return out.concat(dim(200, 1040, 1600, 'FIXED PRICE · AGREED BEFORE WEEK 1'));
    })()
  };
  var ORDER = ['sheet', 'web', 'mobile', 'ai', 'dash', 'process'];
  var TITLE = { sheet: 'BRIEF', web: 'WEB PORTAL', mobile: 'MOBILE', ai: 'AI AGENTS', dash: 'DASHBOARDS', process: 'DELIVERY' };

  // timeline per sheet: strokes cost their length, the pen travels (lifted) between them, washes and lettering take a beat
  function plan(items) {
    var t = 0, last = null;
    items.forEach(function (it) {
      if (it.type === 'stroke') {
        var len = 0; for (var i = 1; i < it.pts.length; i++) len += Math.hypot(it.pts[i][0] - it.pts[i - 1][0], it.pts[i][1] - it.pts[i - 1][1]);
        var start = it.pts[0], travel = last ? Math.hypot(start[0] - last[0], start[1] - last[1]) * 0.45 : 0;
        it.t0 = t; it.tr = travel; t += travel; it.d0 = t; it.len = len; t += len; it.t1 = t; it.from = last; last = it.pts[it.pts.length - 1];
      } else { it.t0 = t; t += 260; it.t1 = t; it.at = last; }
    });
    return t;
  }
  var SHEETS = ORDER.map(function (name, idx) {
    var items = DRAW[name], total = plan(items);
    var cv = document.createElement('canvas'); cv.width = PX; cv.height = PY;
    var base = document.createElement('canvas'); base.width = PX; base.height = PY;
    var tex = new THREE.CanvasTexture(cv); tex.encoding = THREE.sRGBEncoding; tex.anisotropy = ANISO;
    var mesh = new THREE.Mesh(new THREE.PlaneGeometry(SW, SH), new THREE.MeshStandardMaterial({ map: tex, roughness: 0.92, metalness: 0, envMapIntensity: 0.4, transparent: true }));
    mesh.rotation.x = -Math.PI / 2; mesh.receiveShadow = true; scene.add(mesh);
    return { name: name, idx: idx, items: items, total: total, cv: cv, base: base, tex: tex, mesh: mesh, drawn: -1 };
  });

  function colOf(c) { return c === 'a' ? C.inkA : c === 'muted' ? C.muted : c === 'paper' ? C.paper : C.ink; }
  function paintBase(sh) {
    var x = sh.base.getContext('2d');
    x.fillStyle = C.paper; x.fillRect(0, 0, PX, PY);
    // fine grid, then the printed border and title block
    for (var gx = 0; gx <= PX; gx += 30) { x.fillStyle = rgba(C.ink, gx % 150 === 0 ? 0.07 : 0.03); x.fillRect(gx, 0, 1.4, PY); }
    for (var gy = 0; gy <= PY; gy += 30) { x.fillStyle = rgba(C.ink, gy % 150 === 0 ? 0.07 : 0.03); x.fillRect(0, gy, PX, 1.4); }
    x.strokeStyle = rgba(C.ink, 0.75); x.lineWidth = 3; x.strokeRect(50, 50, PX - 100, PY - 100); x.lineWidth = 1.2; x.strokeRect(62, 62, PX - 124, PY - 124);
    x.lineWidth = 1.6; x.strokeRect(PX - 520, PY - 150, 458, 88); x.beginPath(); x.moveTo(PX - 360, PY - 150); x.lineTo(PX - 360, PY - 62); x.stroke();
    x.fillStyle = rgba(C.ink, 0.8); x.font = '600 20px "JetBrains Mono", monospace'; x.fillText('WISETRACK', PX - 500, PY - 112); x.fillText('INDIA', PX - 500, PY - 82);
    x.fillText('SHEET ' + (sh.idx + 1) + ' OF 6', PX - 340, PY - 112); x.fillText(TITLE[sh.name], PX - 340, PY - 82);
  }
  function strokePart(x, it, len) {
    x.strokeStyle = colOf(it.col); x.lineWidth = it.w; x.lineCap = 'round'; x.lineJoin = 'round'; x.setLineDash(it.dash || []);
    x.beginPath(); x.moveTo(it.pts[0][0], it.pts[0][1]); var acc = 0, end = it.pts[0];
    for (var i = 1; i < it.pts.length; i++) { var a = it.pts[i - 1], b = it.pts[i], d = Math.hypot(b[0] - a[0], b[1] - a[1]);
      if (acc + d >= len) { var f = (len - acc) / Math.max(d, 0.001); end = [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f]; x.lineTo(end[0], end[1]); break; }
      x.lineTo(b[0], b[1]); acc += d; end = b; }
    x.stroke(); x.setLineDash([]); return end;
  }
  function shapePath(x, pts) { x.beginPath(); x.moveTo(pts[0][0], pts[0][1]); for (var i = 1; i < pts.length; i++) x.lineTo(pts[i][0], pts[i][1]); x.closePath(); }
  // draw a sheet up to timeline position L; returns the pen (sheet px) and whether it touches the paper
  function render(sh, L) {
    var q = Math.round(L);
    var pen = null;
    if (q !== sh.drawn) {
      var x = sh.cv.getContext('2d'); x.drawImage(sh.base, 0, 0);
      sh.items.forEach(function (it) {
        if (L <= it.t0) return;
        if (it.type === 'stroke') { if (L > it.d0) strokePart(x, it, Math.min(it.len, L - it.d0)); }
        else if (it.type === 'wash') { x.fillStyle = rgba(colOf(it.col), it.a * Math.min(1, (L - it.t0) / (it.t1 - it.t0))); shapePath(x, it.shape); x.fill(); }
        else { var a = Math.min(1, (L - it.t0) / (it.t1 - it.t0)); x.fillStyle = rgba(colOf(it.col), 0.92 * a); x.textAlign = it.align; x.textBaseline = 'middle';
          x.font = (it.mono ? '600 ' : it.italic ? 'italic 500 ' : '500 ') + it.size + 'px ' + (it.mono ? '"JetBrains Mono", monospace' : '"Fraunces", Georgia, serif'); x.fillText(it.str, it.x, it.y); }
      });
      sh.drawn = q; sh.tex.needsUpdate = true;
    }
    // pen position
    for (var i = 0; i < sh.items.length; i++) { var it = sh.items[i];
      if (L < it.t0 || L > it.t1) continue;
      if (it.type === 'stroke') {
        if (L < it.d0) { var f = it.tr ? (L - it.t0) / it.tr : 1, a0 = it.from || it.pts[0], b0 = it.pts[0]; return { x: a0[0] + (b0[0] - a0[0]) * f, y: a0[1] + (b0[1] - a0[1]) * f, down: false }; }
        var x2 = sh.cv.getContext('2d'), l = L - it.d0, acc = 0;
        for (var j = 1; j < it.pts.length; j++) { var p = it.pts[j - 1], n = it.pts[j], d = Math.hypot(n[0] - p[0], n[1] - p[1]); if (acc + d >= l) { var ff = (l - acc) / Math.max(d, 0.001); return { x: p[0] + (n[0] - p[0]) * ff, y: p[1] + (n[1] - p[1]) * ff, down: true }; } acc += d; }
      } else if (it.at) return { x: it.at[0], y: it.at[1], down: false };
    }
    return null;
  }
  function repaintAll() { SHEETS.forEach(function (sh) { paintBase(sh); sh.drawn = -1; }); }

  // ---------- the pantograph arm ----------
  var SH0 = new THREE.Vector3(-2.75, 0, -1.75), ARM_Y = 0.42, L1 = 2.75, L2 = 2.75;
  var arm = new THREE.Group(); scene.add(arm);
  var tower = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.22, ARM_Y - 0.02, 48), brass); tower.position.set(SH0.x, (ARM_Y - 0.02) / 2, SH0.z); tower.castShadow = true; arm.add(tower);
  var towerBase = new THREE.Mesh(new THREE.CylinderGeometry(0.34, 0.37, 0.06, 64), lacquer); towerBase.position.set(SH0.x, 0.03, SH0.z); towerBase.castShadow = towerBase.receiveShadow = true; arm.add(towerBase);
  var towerRing = new THREE.Mesh(new THREE.TorusGeometry(0.2, 0.012, 12, 64), brass); towerRing.rotation.x = Math.PI / 2; towerRing.position.set(SH0.x, ARM_Y * 0.55, SH0.z); arm.add(towerRing);
  function rod(r) { var g = new THREE.CylinderGeometry(r, r, 1, 24); g.rotateX(Math.PI / 2); var m = new THREE.Mesh(g, brass); m.castShadow = true; arm.add(m); return m; }
  function joint(r, h) { var g = new THREE.Group(); var cap = new THREE.Mesh(new THREE.CylinderGeometry(r, r, h, 48), lacquer); cap.castShadow = true; g.add(cap); var ring = new THREE.Mesh(new THREE.TorusGeometry(r, 0.008, 10, 48), brass); ring.rotation.x = Math.PI / 2; ring.position.y = h / 2; g.add(ring); var pin = new THREE.Mesh(new THREE.CylinderGeometry(r * 0.35, r * 0.35, h + 0.02, 24), brass); g.add(pin); arm.add(g); return g; }
  var upper = rod(0.03), upper2 = rod(0.016), fore = rod(0.026), fore2 = rod(0.014);
  var jS = joint(0.11, 0.07), jE = joint(0.09, 0.06), jW = joint(0.075, 0.05);
  var counter = new THREE.Mesh(new THREE.SphereGeometry(0.13, 48, 32), brassDark); counter.castShadow = true; arm.add(counter);
  var counterRod = rod(0.02);
  var penG = new THREE.Group(); arm.add(penG);
  var barrel = new THREE.Mesh(new THREE.CylinderGeometry(0.032, 0.032, 0.28, 32), brass); barrel.position.y = 0.2; barrel.castShadow = true; penG.add(barrel);
  var collar = new THREE.Mesh(new THREE.CylinderGeometry(0.026, 0.034, 0.05, 32), brassDark); collar.position.y = 0.36; penG.add(collar);
  var band = new THREE.Mesh(new THREE.TorusGeometry(0.033, 0.006, 10, 40), lacquer); band.rotation.x = Math.PI / 2; band.position.y = 0.3; penG.add(band);
  var nib = new THREE.Mesh(new THREE.ConeGeometry(0.03, 0.09, 32), nibMat); nib.rotation.x = Math.PI; nib.position.y = 0.045; nib.castShadow = true; penG.add(nib);
  var inkDot = new THREE.PointLight(0xffffff, 0, 0.6, 2); inkDot.position.y = 0.05; penG.add(inkDot);
  function placeRod(m, A, B) { m.position.copy(A).add(B).multiplyScalar(0.5); m.scale.set(1, 1, A.distanceTo(B)); m.lookAt(B); }
  var penPos = new THREE.Vector3(1.4, 0, 1.0), penLift = 0.08;
  function poseArm() {
    var S0 = new THREE.Vector3(SH0.x, ARM_Y, SH0.z), dx = penPos.x - S0.x, dz = penPos.z - S0.z;
    var d = Math.min(L1 + L2 - 0.002, Math.max(0.05, Math.hypot(dx, dz))), a = Math.atan2(dz, dx), b = Math.acos(Math.min(1, (L1 * L1 + d * d - L2 * L2) / (2 * L1 * d)));
    var e1 = new THREE.Vector3(S0.x + Math.cos(a - b) * L1, ARM_Y, S0.z + Math.sin(a - b) * L1), e2 = new THREE.Vector3(S0.x + Math.cos(a + b) * L1, ARM_Y, S0.z + Math.sin(a + b) * L1);
    var E = e1.z < e2.z ? e1 : e2, Wp = new THREE.Vector3(penPos.x, ARM_Y, penPos.z);
    placeRod(upper, S0, E); placeRod(upper2, S0.clone().add(new THREE.Vector3(0, -0.07, 0)), E.clone().add(new THREE.Vector3(0, -0.07, 0)));
    placeRod(fore, E, Wp); placeRod(fore2, E.clone().add(new THREE.Vector3(0, -0.06, 0)), Wp.clone().add(new THREE.Vector3(0, -0.06, 0)));
    var back = S0.clone().sub(E).normalize().multiplyScalar(0.55).add(S0); counter.position.copy(back); placeRod(counterRod, S0, back);
    jS.position.copy(S0); jE.position.copy(E); jW.position.copy(Wp);
    penG.position.set(penPos.x, TOP + 0.001 + penLift, penPos.z);
  }

  // ---------- post ----------
  var P = SceneKit.post(renderer, scene, camera, dev), composer = P.composer, bloom = P.bloom, finalPass = P.finalPass;

  function applyPalette() {
    readPalette(); bgCol.copy(lin(C.bg)); scene.fog.color.copy(bgCol);
    brass.color.copy(lin(C.brass)); brassDark.color.copy(lin(C.brassD)); lacquer.color.copy(lin(C.lacq));
    boardMat.color.copy(lin(C.dark ? '#141418' : C.board)); boardEdge.material = brass;
    hemi.color.copy(lin(C.dark ? '#c9cfe0' : '#fff6e8')); hemi.groundColor.copy(lin(C.lacq)); hemi.intensity = C.dark ? 0.45 : 0.75;
    key.intensity = C.dark ? 1.0 : 1.3; renderer.toneMappingExposure = C.dark ? 1.05 : 1.0;
    ground.material.opacity = C.dark ? 0.35 : 0.2; inkDot.color.copy(lin(C.a));
    bloom.threshold = C.dark ? 0.8 : 0.95; bloom.strength = C.dark ? 0.35 : 0.18;
    var b = new THREE.Color(C.bg), sh = new THREE.Color(C.dark ? '#000000' : C.line);
    finalPass.uniforms.uVig.value.set(C.dark ? 0.6 : 0.55 + 0.45 * sh.r / Math.max(0.01, b.r), C.dark ? 0.6 : 0.55 + 0.45 * sh.g / Math.max(0.01, b.g), C.dark ? 0.6 : 0.55 + 0.45 * sh.b / Math.max(0.01, b.b));
    repaintAll();
  }
  applyPalette();
  new MutationObserver(applyPalette).observe(root, { attributes: true, attributeFilter: ['class', 'data-palette'] });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { repaintAll(); });

  // ---------- timeline ----------
  var RANGES = { sheet: [0, 1.0], web: [1.0, 2.65], mobile: [2.65, 4.3], ai: [4.3, 5.95], dash: [5.95, 7.6], process: [7.6, 9.2] }, END = 9.2;
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function fit(v, a, b) { return clamp((v - a) / (b - a), 0, 1); }
  function ease(t) { return t * t * (3 - 2 * t); }
  function easeIO(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }

  // where each finished sheet rests: a stack on the table to the right of the board
  function stackPose(i) { return { p: new THREE.Vector3(3.85 + (i % 2) * 0.05, 0.004 + i * 0.006, 0.15 - i * 0.04), r: 0.05 * (i % 3 - 1) - 0.1 }; }

  // camera: each chapter is a moving shot around a look point, [yaw, elevation, distance] at start and end
  var SHOTS = {
    sheet:   { a: [1.05, 0.2, 2.6, 'pen'], b: [0.45, 0.82, 7.2, 'board'] },     // macro on the nib, then up and back
    web:     { a: [-0.35, 1.05, 6.6, 'board'], b: [-0.08, 1.38, 5.8, 'board'] }, // high, settling to overhead
    mobile:  { a: [1.35, 0.2, 2.4, 'pen'], b: [0.75, 0.95, 6.2, 'board'] },     // low along the paper, rising
    ai:      { a: [-1.15, 0.62, 6.8, 'board'], b: [0.45, 0.88, 6.4, 'board'] }, // a slow orbit
    dash:    { a: [0.05, 1.45, 6.9, 'board'], b: [0.7, 0.58, 6.0, 'board'] },   // overhead, tilting down
    process: { a: [-0.85, 0.42, 7.8, 'wide'], b: [-0.3, 1.0, 9.6, 'wide'] }     // wide, the stack of sheets in frame
  };
  var LOOK = { board: new THREE.Vector3(0, TOP, 0.1), wide: new THREE.Vector3(1.0, TOP, 0.1) };
  var penSmooth = new THREE.Vector3(1.4, TOP, 1.0);
  function shotPos(p) {
    var look = p[3] === 'pen' ? penSmooth.clone() : LOOK[p[3]].clone();
    var yaw = p[0], el = mobile ? Math.max(p[1], 1.0) : p[1], d = p[2] * (mobile ? (p[3] === 'pen' ? 2.6 : 1.55) : 1);
    if (mobile && p[3] === 'pen') { look = LOOK.board.clone(); }
    var pos = new THREE.Vector3(look.x + Math.sin(yaw) * Math.cos(el) * d, look.y + Math.sin(el) * d, look.z + Math.cos(yaw) * Math.cos(el) * d);
    var fwd = look.clone().sub(pos).normalize(), right = new THREE.Vector3().crossVectors(fwd, new THREE.Vector3(0, 1, 0)).normalize();
    var tgt = look.addScaledVector(right, mobile ? 0 : -0.2 * d); if (mobile) { tgt.y -= 0.16 * d; tgt.z += 0.05 * d; }
    return { pos: pos, tgt: tgt };
  }
  function blendShot(A, B, t) { return { pos: A.pos.clone().lerp(B.pos, t), tgt: A.tgt.clone().lerp(B.tgt, t) }; }

  // ---------- copy + code (unchanged behaviour from the previous scene) ----------
  var code = sec.querySelector('.bp-code'), pre = code.querySelector('pre'), lang = code.querySelector('header span');
  var CODE = {
    web: ['C# · ASP.NET Core', '<span class="k">app</span>.MapGet(<span class="s">"/api/invoices"</span>, <span class="k">async</span> (Db db) =>\n    <span class="k">await</span> db.Invoices\n        .Where(i => i.Status == <span class="s">"overdue"</span>)\n        .OrderBy(i => i.DueDate)\n        .ToListAsync());'],
    mobile: ['Kotlin · Android', '<span class="k">val</span> inside = location.distanceTo(office) < <span class="n">150f</span>\n<span class="k">if</span> (inside) attendance.clockIn(now(), location)\n<span class="k">else</span> ui.warn(<span class="s">"Outside the office geofence"</span>)\nsync.queueWhenOnline(attendance.pending())'],
    ai: ['Agent tool call', '{\n  <span class="s">"tool"</span>: <span class="s">"accounts.search_invoices"</span>,\n  <span class="s">"input"</span>: { <span class="s">"status"</span>: <span class="s">"overdue"</span>, <span class="s">"limit"</span>: <span class="n">50</span> },\n  <span class="s">"guard"</span>: <span class="s">"read-only · tenant scoped"</span>,\n  <span class="s">"cost"</span>: <span class="s">"logged per call"</span>\n}'],
    dash: ['WebSocket · live', 'socket.on(<span class="s">"metrics"</span>, m => {\n  revenue.push(m.revenue);\n  orders.set(m.orders);\n  chart.update({ series: [revenue] });\n});']
  };
  function typed(html, n) { var out = '', count = 0, i = 0; while (i < html.length && count < n) { if (html[i] === '<') { var j = html.indexOf('>', i); out += html.slice(i, j + 1); i = j + 1; continue; } out += html[i]; i++; count++; } var opens = (out.match(/<span/g) || []).length - (out.match(/<\/span>/g) || []).length; for (var q = 0; q < opens; q++) out += '</span>'; return out; }
  function plainLen(html) { return html.replace(/<[^>]+>/g, '').length; }
  var copies = [].slice.call(sec.querySelectorAll('.bp-copy')), lastCode = null, lastN = -1;

  var vw = 1, vh = 1, mobile = isMobile;
  function resize() { vw = stage.clientWidth; vh = stage.clientHeight; mobile = vw < 760; renderer.setSize(vw, vh, false); P.setSize(vw, vh); camera.aspect = vw / vh; camera.fov = mobile ? 42 : 30; camera.updateProjectionMatrix(); }
  function secTop() { return sec.getBoundingClientRect().top + window.scrollY; }
  var seekTo = null; sec.__seek = function (v) { seekTo = v; sCur = v; };
  function target() { return seekTo !== null ? seekTo : clamp((window.scrollY - secTop()) / vh, 0, END); }
  var sCur = 0, last = performance.now(), t0 = last, visible = true, cam = { pos: new THREE.Vector3(), tgt: new THREE.Vector3(), init: false };
  new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }, { rootMargin: '200px 0px' }).observe(sec);
  var PARK = { x: 1650, y: 1120 };

  function frame(now) {
    requestAnimationFrame(frame);
    var dt = Math.min(0.05, (now - last) / 1000); last = now;
    if (!visible) return;
    var tg = target(); sCur = reduced ? tg : sCur + (tg - sCur) * (1 - Math.exp(-dt * 5));
    var s = sCur, time = (now - t0) / 1000;
    var cur = 0; ORDER.forEach(function (n, k) { if (s >= RANGES[n][0]) cur = k; });
    var penTarget = null;

    SHEETS.forEach(function (sh, i) {
      var r = RANGES[sh.name], t = fit(s, r[0], r[1]);
      // drawing progress: the opening sheet also draws itself after load
      var prog = i === 0 ? Math.max(reduced ? 1 : ease(fit(time, 0.6, 6.0)), fit(s, 0, 0.75)) : ease(fit(t, 0.04, 0.78));
      if (i > 0 && s < r[0] - 0.3) prog = 0;
      var pen = render(sh, prog * sh.total);
      if (i === cur && pen && prog < 1) penTarget = pen;
      // placement: drop in before its chapter, lie on the board, slide onto the stack after it
      var dropIn = i === 0 ? 1 : easeIO(fit(s, r[0] - 0.32, r[0] + 0.02));
      var out = i === ORDER.length - 1 ? 0 : easeIO(fit(s, r[1] - 0.22, r[1] + 0.12));
      var onBoard = new THREE.Vector3(0, TOP + 0.002 + i * 0.0004, 0.05), st = stackPose(i);
      var p = onBoard.clone(); p.y += (1 - dropIn) * 0.9; p.x -= (1 - dropIn) * 0.6;
      p.lerp(st.p, out); p.y += Math.sin(out * Math.PI) * 0.35;
      sh.mesh.position.copy(p);
      sh.mesh.rotation.set(-Math.PI / 2 + (1 - dropIn) * 0.25, 0, (1 - dropIn) * 0.18 + st.r * out);
      sh.mesh.material.opacity = Math.min(1, dropIn * 1.4); sh.mesh.visible = dropIn > 0.01;
    });

    // pen: follows the drawing, lifts between strokes, parks when the sheet is done
    var px = penTarget || PARK, down = penTarget && penTarget.down;
    var wp = toWorld(px.x, px.y, TOP);
    var kk = reduced ? 1 : 1 - Math.exp(-dt * (penTarget ? 18 : 3));
    penPos.lerp(wp, kk); penLift += ((down ? 0 : (penTarget ? 0.07 : 0.18)) - penLift) * (1 - Math.exp(-dt * 14));
    poseArm(); inkDot.intensity = down ? 0.35 : 0;
    penSmooth.lerp(new THREE.Vector3(penPos.x, TOP, penPos.z), 1 - Math.exp(-dt * 3));

    // camera
    var nm = ORDER[cur], rr = RANGES[nm], tt = easeIO(fit(s, rr[0], rr[1]));
    if (nm === 'sheet' && !reduced) tt = Math.max(tt, easeIO(fit(time, 1.0, 8.0)) * 0.85);
    var shot = blendShot(shotPos(SHOTS[nm].a), shotPos(SHOTS[nm].b), tt);
    if (cur < ORDER.length - 1) { var bl = ease(fit(s, rr[1] - 0.25, rr[1] + 0.15)); if (bl > 0) shot = blendShot(shot, shotPos(SHOTS[ORDER[cur + 1]].a), bl); }
    if (!cam.init) { cam.pos.copy(shot.pos); cam.tgt.copy(shot.tgt); cam.init = true; }
    var kc2 = reduced ? 1 : 1 - Math.exp(-dt * 4); cam.pos.lerp(shot.pos, kc2); cam.tgt.lerp(shot.tgt, kc2);
    camera.position.copy(cam.pos); camera.lookAt(cam.tgt);
    if (!reduced) { camera.position.x += Math.sin(time * 0.21) * 0.02; camera.position.y += Math.sin(time * 0.17) * 0.015; }

    // code panel
    var activeT = fit(s, rr[0], rr[1]), cd = CODE[nm], co = cd ? ease(fit(activeT, 0.2, 0.32)) * (1 - ease(fit(activeT, 0.84, 0.96))) : 0;
    code.style.opacity = co.toFixed(3); code.style.transform = 'translateY(' + ((1 - co) * 12).toFixed(1) + 'px)';
    if (cd) { if (lastCode !== nm) { lastCode = nm; lastN = -1; lang.textContent = cd[0]; } var n = Math.round(plainLen(cd[1]) * fit(activeT, 0.26, 0.7)); if (n !== lastN) { lastN = n; pre.innerHTML = typed(cd[1], n) + '<span class="caret"></span>'; } }
    // copy
    copies.forEach(function (c) {
      var r = c.dataset.range.split(',').map(parseFloat), fade = 0.26;
      var o = r[0] <= 0 ? 1 - fit(s, r[1], r[1] + fade) : r[1] >= END ? fit(s, r[0] - fade, r[0]) : Math.min(fit(s, r[0] - fade, r[0]), 1 - fit(s, r[1], r[1] + fade));
      c.style.opacity = o.toFixed(3);
      c.style.transform = mobile ? 'translateY(' + ((1 - o) * 14).toFixed(1) + 'px)' : 'translateY(calc(-46% + ' + ((1 - o) * 14).toFixed(1) + 'px))';
      c.classList.toggle('on', o > 0.5);
    });
    var hint = sec.querySelector('.bp-hint'); if (hint) hint.style.opacity = 1 - fit(s, 0.05, 0.4);
    finalPass.uniforms.uTime.value = time;
    composer.render();
  }
  resize(); window.addEventListener('resize', resize);
  sCur = target(); poseArm();
  requestAnimationFrame(function (now) { last = now; requestAnimationFrame(frame); });
  sec.classList.add('gl');
})();
