/* Services — "Blueprint" (animation style 04), WebGL.
   Each service is built in front of you: a glowing scan plane sweeps up through the object,
   drawing its wireframe, and the solid, lit object materialises behind the scan (two clipping
   planes, the wire one running ahead). The previous object dematerialises top-down as the next
   one starts. A brief sketch, a laptop with a web portal, a phone, an agent network with pulses,
   a dashboard city, and the six-sprint staircase to launch. Same toolkit as the other pages:
   three r128, ACES, soft shadows, mirror floor, depth of field, bloom, grain. Colours are site
   tokens; the code panel types alongside. Scroll is in viewport heights, eased each frame. */
(function () {
  var sec = document.getElementById('blueprint'); if (!sec) return;
  var stage = sec.querySelector('.bp-stage'), canvas = sec.querySelector('canvas.bp-gl');
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
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = lowEnd ? THREE.PCFShadowMap : THREE.PCFSoftShadowMap;
  renderer.localClippingEnabled = true;

  // ---------- palette ----------
  var root = document.documentElement, C = {};
  function tok(n, fb) { return getComputedStyle(root).getPropertyValue(n).trim() || fb; }
  function readPalette() { C = { bg: tok('--bg', '#f8f3ec'), bg2: tok('--bg-2', '#f1e8dc'), surface: tok('--surface', '#fffdf9'), surface2: tok('--surface-2', '#f4ece0'), line: tok('--line', '#dccdbd'), text: tok('--text', '#3b0d14'), text2: tok('--text-2', '#4a2a2e'), muted: tok('--muted', '#7a4b4f'), a: tok('--violet', '#d8261c'), c: tok('--cyan', '#d9b26a'), m: tok('--mint', '#7fc08a'), dark: !root.classList.contains('light') }; }
  readPalette();
  function lin(hex) { return new THREE.Color(hex).convertSRGBToLinear(); }
  function hexOf(col) { return '#' + new THREE.Color(col).getHexString(); }
  function alpha(hex, a) { var c = new THREE.Color(hex); return 'rgba(' + Math.round(c.r * 255) + ',' + Math.round(c.g * 255) + ',' + Math.round(c.b * 255) + ',' + a + ')'; }

  // ---------- screen textures ----------
  var FONT = '"Inter Tight", ui-sans-serif, system-ui, sans-serif', MONO = '"JetBrains Mono", ui-monospace, monospace';
  function rr(x, c, X, Y, W, H, R) { x.beginPath(); x.moveTo(X + R, Y); x.arcTo(X + W, Y, X + W, Y + H, R); x.arcTo(X + W, Y + H, X, Y + H, R); x.arcTo(X, Y + H, X, Y, R); x.arcTo(X, Y, X + W, Y, R); x.closePath(); x.fillStyle = c; x.fill(); }
  function paintWeb(cv) {
    cv.width = 1280; cv.height = 800; var x = cv.getContext('2d'), A = hexOf(C.a), S = hexOf(C.surface), S2 = hexOf(C.surface2), T = hexOf(C.text), T2 = hexOf(C.text2), MU = hexOf(C.muted), L = hexOf(C.line), M = hexOf(C.m);
    x.fillStyle = S; x.fillRect(0, 0, 1280, 800);
    x.fillStyle = S2; x.fillRect(0, 0, 250, 800); x.fillStyle = L; x.fillRect(250, 0, 2, 800);
    x.fillStyle = T; x.font = '700 30px ' + FONT; x.fillText('Northline', 36, 62);
    ['Dashboard', 'Invoices', 'Customers', 'Stock', 'Reports', 'Settings'].forEach(function (n, i) { if (i === 1) rr(x, alpha(A, 0.15), 22, 106 + i * 56, 206, 44, 10); x.fillStyle = i === 1 ? A : T2; x.font = '500 22px ' + FONT; x.fillText(n, 40, 136 + i * 56); });
    [['Overdue', '₹ 4.8L', A], ['Due this week', '₹ 2.1L', T], ['Collected', '₹ 11.6L', M]].forEach(function (k, i) { var X = 290 + i * 320; rr(x, i === 0 ? alpha(A, 0.12) : S2, X, 50, 296, 130, 16); x.fillStyle = MU; x.font = '500 22px ' + FONT; x.fillText(k[0], X + 24, 96); x.fillStyle = k[2]; x.font = '700 40px ' + MONO; x.fillText(k[1], X + 24, 150); });
    x.fillStyle = MU; x.font = '600 18px ' + MONO; ['CUSTOMER', 'AMOUNT', 'STATUS'].forEach(function (h, i) { x.fillText(h, [290, 760, 1010][i], 240); });
    [['Kumar Enterprises', '₹ 1,24,000', 'Overdue'], ['Shah Traders', '₹ 86,500', 'Overdue'], ['Bluewave Retail', '₹ 2,10,000', 'Due'], ['Om Logistics', '₹ 48,200', 'Paid'], ['Raj Electricals', '₹ 72,900', 'Paid'], ['Greenleaf Foods', '₹ 1,05,000', 'Paid']].forEach(function (r, i) {
      var y = 300 + i * 78; x.fillStyle = L; x.fillRect(290, y - 44, 950, 2); x.fillStyle = T; x.font = '500 24px ' + FONT; x.fillText(r[0], 290, y); x.font = '600 24px ' + MONO; x.fillText(r[1], 760, y);
      var col = r[2] === 'Paid' ? M : A; rr(x, alpha(col, 0.18), 1010, y - 28, 120, 40, 20); x.fillStyle = col; x.font = '700 19px ' + FONT; x.textAlign = 'center'; x.fillText(r[2], 1070, y - 1); x.textAlign = 'left';
    });
  }
  function paintPhone(cv) {
    cv.width = 540; cv.height = 1100; var x = cv.getContext('2d'), A = hexOf(C.a), S = hexOf(C.surface), T = hexOf(C.text), T2 = hexOf(C.text2), MU = hexOf(C.muted), L = hexOf(C.line), Cc = hexOf(C.c), M = hexOf(C.m);
    x.fillStyle = S; x.fillRect(0, 0, 540, 1100);
    x.fillStyle = MU; x.font = '600 24px ' + MONO; x.fillText('9:41', 50, 80);
    rr(x, alpha(Cc, 0.18), 40, 120, 460, 330, 30);
    x.strokeStyle = A; x.lineWidth = 5; x.setLineDash([12, 10]); x.beginPath(); x.arc(270, 285, 115, 0, 7); x.stroke(); x.setLineDash([]);
    x.beginPath(); x.arc(270, 285, 14, 0, 7); x.fillStyle = A; x.fill(); x.fillStyle = T; x.font = '600 24px ' + MONO; x.fillText('150 m', 300, 190);
    rr(x, A, 40, 480, 460, 110, 26); x.fillStyle = '#fff'; x.font = '700 34px ' + FONT; x.textAlign = 'center'; x.fillText('Clock in · 09:02', 270, 548); x.textAlign = 'left';
    ['Approve leave · Priya', 'New lead · Kumar Ent.', 'Scan · GRN 2041'].forEach(function (t, i) { var y = 680 + i * 120; x.beginPath(); x.arc(76, y, 26, 0, 7); x.fillStyle = [A, Cc, M][i]; x.fill(); x.fillStyle = T2; x.font = '500 28px ' + FONT; x.fillText(t, 124, y + 10); x.fillStyle = L; x.fillRect(40, y + 56, 460, 2); });
  }

  // ---------- scene ----------
  var scene = new THREE.Scene(), bgCol = lin(C.bg);
  scene.background = bgCol; scene.fog = new THREE.FogExp2(bgCol.getHex(), 0.035);
  var camera = new THREE.PerspectiveCamera(36, 1, 0.1, 200);
  var hemi = new THREE.HemisphereLight(0xffffff, 0x444444, 0.5); scene.add(hemi);
  var key = new THREE.DirectionalLight(0xffffff, 1.3); key.position.set(5, 10, 6); key.castShadow = true;
  key.shadow.mapSize.set(lowEnd ? 1024 : 2048, lowEnd ? 1024 : 2048); var kc = key.shadow.camera; kc.left = -8; kc.right = 8; kc.top = 8; kc.bottom = -8; kc.far = 30; key.shadow.bias = -0.0004; key.shadow.radius = 4;
  scene.add(key);
  var rim = new THREE.PointLight(0xffffff, 1.6, 20, 2); rim.position.set(-5, 4, -4); scene.add(rim);
  var rim2 = new THREE.PointLight(0xffffff, 1.0, 20, 2); rim2.position.set(5, 2.5, -5); scene.add(rim2);

  var mirror = null;
  if (!lowEnd && THREE.Reflector) { mirror = new THREE.Reflector(new THREE.PlaneGeometry(80, 80), { textureWidth: Math.round(window.innerWidth * DPR * 0.5), textureHeight: Math.round(window.innerHeight * DPR * 0.5), color: 0x8a8a8a }); mirror.rotation.x = -Math.PI / 2; mirror.position.y = -0.002; scene.add(mirror); }
  var glaze = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.MeshStandardMaterial({ color: bgCol.clone(), roughness: 0.6, transparent: !!mirror, opacity: mirror ? 0.84 : 1 }));
  glaze.rotation.x = -Math.PI / 2; glaze.receiveShadow = true; scene.add(glaze);
  // the drafting disc: a turntable with a blueprint grid
  var disc = new THREE.Mesh(new THREE.CylinderGeometry(3.6, 3.75, 0.16, 96), new THREE.MeshPhysicalMaterial({ color: 0x111111, roughness: 0.35, metalness: 0.5, clearcoat: 1 }));
  disc.position.y = 0.08; disc.receiveShadow = true; disc.castShadow = true; scene.add(disc);
  var discRing = new THREE.Mesh(new THREE.TorusGeometry(3.62, 0.018, 8, 160), new THREE.MeshBasicMaterial({ color: 0xffffff })); discRing.rotation.x = Math.PI / 2; discRing.position.y = 0.165; scene.add(discRing);
  var discGrid = new THREE.PolarGridHelper(3.5, 24, 8, 96, 0xffffff, 0xffffff); discGrid.position.y = 0.168; discGrid.material.transparent = true; discGrid.material.opacity = 0.18; scene.add(discGrid);
  var floorGrid = new THREE.GridHelper(80, 80, 0x000000, 0x000000); floorGrid.position.y = 0.003; floorGrid.material.transparent = true; floorGrid.material.opacity = 0.05; scene.add(floorGrid);
  var turn = new THREE.Group(); turn.position.y = 0.16; scene.add(turn);

  // ---------- builder: every object is solids + their edge wireframes, both clipped ----------
  var wireMat = function () { return new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.95, clippingPlanes: [], depthWrite: false }); };
  function solidMat(o) { var m = new THREE.MeshPhysicalMaterial(Object.assign({ color: 0x1a1a1a, roughness: 0.35, metalness: 0.3, clearcoat: 0.6, clippingPlanes: [], clipShadows: true }, o || {})); return m; }
  var OBJ = {};
  function make(name) {
    var o = { name: name, g: new THREE.Group(), solids: [], wires: [], wireP: new THREE.Plane(new THREE.Vector3(0, -1, 0), 0), solidP: new THREE.Plane(new THREE.Vector3(0, -1, 0), 0), minY: 0, maxY: 2, extra: null, textures: [] };
    turn.add(o.g); OBJ[name] = o; return o;
  }
  function add(o, geo, mat, pos, rot, opts) {
    opts = opts || {};
    mat.clippingPlanes = [o.solidP];
    var mesh = new THREE.Mesh(geo, mat); if (pos) mesh.position.copy(pos); if (rot) mesh.rotation.set(rot.x || 0, rot.y || 0, rot.z || 0);
    mesh.castShadow = !opts.noShadow; mesh.receiveShadow = true; (opts.parent || o.g).add(mesh); o.solids.push(mesh);
    if (!opts.noWire) { var w = new THREE.LineSegments(new THREE.EdgesGeometry(geo, opts.edgeAngle || 20), wireMat()); w.material.clippingPlanes = [o.wireP]; mesh.add(w); o.wires.push(w); }
    return mesh;
  }
  function screen(o, cv, painter, w, h, pos, rot, parent) {
    painter(cv); var t = new THREE.CanvasTexture(cv); t.encoding = THREE.sRGBEncoding; t.anisotropy = 4; o.textures.push([t, cv, painter]);
    var m = new THREE.MeshStandardMaterial({ map: t, emissive: 0xffffff, emissiveMap: t, emissiveIntensity: 0.45, roughness: 0.3 });
    return add(o, new THREE.PlaneGeometry(w, h), m, pos, rot, { noWire: true, noShadow: true, parent: parent });
  }
  var V = function (x, y, z) { return new THREE.Vector3(x, y, z); };

  // 0 · the brief: three rough blocks on the disc, joined by struts
  (function () {
    var o = make('sheet'), mat = solidMat({ color: 0x222222, metalness: 0.1, roughness: 0.5 });
    add(o, new THREE.BoxGeometry(1.1, 0.8, 1.1), mat, V(-1.3, 0.4, 0.4)); add(o, new THREE.BoxGeometry(1.5, 1.5, 1.2), mat.clone(), V(0.6, 0.75, -0.4)); add(o, new THREE.BoxGeometry(0.9, 2.2, 0.9), mat.clone(), V(1.9, 1.1, 1.0));
    add(o, new THREE.CylinderGeometry(0.035, 0.035, 2.0, 8), mat.clone(), V(-0.35, 0.95, 0), { x: 0, y: 0.3, z: 1.2 });
    add(o, new THREE.TorusGeometry(0.55, 0.035, 8, 48), mat.clone(), V(0.6, 2.05, -0.4), { x: Math.PI / 2 });
    o.minY = 0; o.maxY = 2.4; o.accent = o.solids[1];
  })();
  // 1 · web: a laptop with the portal on screen
  (function () {
    var o = make('web'), alu = solidMat({ color: 0x9a9da3, metalness: 0.85, roughness: 0.28, clearcoat: 0.3 });
    add(o, new THREE.BoxGeometry(3.6, 0.12, 2.4), alu, V(0, 0.06, 0.4));
    add(o, new THREE.BoxGeometry(3.0, 0.02, 1.0), solidMat({ color: 0x1b1d22 }), V(0, 0.125, 0.15), null, { noShadow: true });
    var lid = new THREE.Group(); lid.position.set(0, 0.12, -0.8); lid.rotation.x = -0.28; o.g.add(lid);
    add(o, new THREE.BoxGeometry(3.6, 2.3, 0.08), alu.clone(), V(0, 1.15, 0), null, { parent: lid });
    add(o, new THREE.BoxGeometry(3.42, 2.12, 0.01), solidMat({ color: 0x050505, roughness: 0.2 }), V(0, 1.16, 0.045), null, { parent: lid, noShadow: true });
    screen(o, document.createElement('canvas'), paintWeb, 3.3, 2.06, V(0, 1.16, 0.052), null, lid);
    o.minY = 0; o.maxY = 2.5;
  })();
  // 2 · mobile: a phone, standing, slightly turned
  (function () {
    var o = make('mobile');
    var sh = new THREE.Shape(), w = 1.15, h = 2.35, r = 0.2; sh.moveTo(-w / 2 + r, -h / 2); sh.lineTo(w / 2 - r, -h / 2); sh.quadraticCurveTo(w / 2, -h / 2, w / 2, -h / 2 + r); sh.lineTo(w / 2, h / 2 - r); sh.quadraticCurveTo(w / 2, h / 2, w / 2 - r, h / 2); sh.lineTo(-w / 2 + r, h / 2); sh.quadraticCurveTo(-w / 2, h / 2, -w / 2, h / 2 - r); sh.lineTo(-w / 2, -h / 2 + r); sh.quadraticCurveTo(-w / 2, -h / 2, -w / 2 + r, -h / 2);
    var geo = new THREE.ExtrudeGeometry(sh, { depth: 0.11, bevelEnabled: true, bevelThickness: 0.02, bevelSize: 0.02, bevelSegments: 3, curveSegments: 10 }); geo.translate(0, 0, -0.055);
    var ph = new THREE.Group(); ph.position.set(0, 1.42, 0); ph.rotation.set(-0.08, -0.35, 0.04); o.g.add(ph);
    add(o, geo, solidMat({ color: 0x15171c, metalness: 0.6, roughness: 0.25, clearcoat: 1 }), null, null, { parent: ph, edgeAngle: 30 });
    screen(o, document.createElement('canvas'), paintPhone, 1.05, 2.14, V(0, 0, 0.082), null, ph);
    add(o, new THREE.CylinderGeometry(0.6, 0.7, 0.06, 48), solidMat({ color: 0x222222 }), V(0, 0.03, 0));
    o.minY = 0; o.maxY = 2.7;
  })();
  // 3 · AI: an agent network; pulses run the loop
  (function () {
    var o = make('ai'), pts = [V(-2.0, 0.9, 0.6), V(-0.8, 1.9, -0.2), V(0.5, 1.0, 0.5), V(1.6, 2.1, -0.4), V(2.2, 0.8, 0.7)];
    var nodeMat = solidMat({ color: 0x202226, metalness: 0.2, roughness: 0.3, clearcoat: 1 });
    o.nodes = pts.map(function (p, i) { return add(o, new THREE.IcosahedronGeometry(i === 2 ? 0.42 : 0.32, 1), nodeMat.clone(), p, null, { edgeAngle: 1 }); });
    var tools = [V(-0.3, 0.3, 1.4), V(0.5, 0.3, 1.6), V(1.3, 0.3, 1.4)];
    tools.forEach(function (p) { add(o, new THREE.BoxGeometry(0.55, 0.22, 0.32), nodeMat.clone(), p); add(o, new THREE.CylinderGeometry(0.02, 0.02, p.distanceTo(pts[2]), 6), nodeMat.clone(), p.clone().add(pts[2]).multiplyScalar(0.5), null, { noWire: true }).lookAt(pts[2]); });
    o.g.children.slice(-6).forEach(function (m, i) { if (i % 2) { m.rotateX(Math.PI / 2); } });
    var path = new THREE.CatmullRomCurve3(pts.concat([V(1.0, 2.9, -0.6), V(-0.8, 1.9, -0.2)]), false, 'centripetal');
    add(o, new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts, false, 'centripetal'), 120, 0.025, 6, false), nodeMat.clone(), null, null, { noWire: true });
    add(o, new THREE.TubeGeometry(new THREE.CatmullRomCurve3([pts[3], V(0.5, 3.0, -0.8), pts[1]], false, 'centripetal'), 60, 0.018, 6, false), nodeMat.clone(), null, null, { noWire: true });
    o.pulses = [0, 1, 2].map(function () { var p = new THREE.Mesh(new THREE.SphereGeometry(0.07, 16, 12), new THREE.MeshBasicMaterial({ color: 0xffffff })); o.g.add(p); return p; });
    o.curve = new THREE.CatmullRomCurve3(pts, false, 'centripetal');
    o.minY = 0; o.maxY = 3.1;
    o.extra = function (vis, time) { o.pulses.forEach(function (p, k) { var u = (time * 0.18 + k / 3) % 1; p.position.copy(o.curve.getPointAt(u)); p.visible = vis > 0.6; }); };
  })();
  // 4 · dashboards: a city of bars and a revenue ribbon
  (function () {
    var o = make('dash'), base = solidMat({ color: 0x1c1d21 });
    add(o, new THREE.BoxGeometry(4.6, 0.08, 3.0), base, V(0, 0.04, 0));
    o.bars = [];
    for (var cx = 0; cx < 7; cx++) for (var cz = 0; cz < 4; cz++) {
      var h = 0.35 + Math.abs(Math.sin(cx * 1.7 + cz * 2.3)) * 1.9 + (cx / 7) * 0.6, m = solidMat({ color: 0x2a2c31, metalness: 0.2 });
      o.bars.push([add(o, new THREE.BoxGeometry(0.42, h, 0.42), m, V(-1.85 + cx * 0.62, 0.08 + h / 2, -1.05 + cz * 0.7)), (cx + cz) % 3]);
    }
    var curve = new THREE.CatmullRomCurve3([V(-2.4, 1.0, 1.5), V(-1.2, 1.5, 1.5), V(0, 1.2, 1.5), V(1.1, 2.2, 1.5), V(2.4, 2.9, 1.5)], false, 'centripetal');
    o.ribbon = add(o, new THREE.TubeGeometry(curve, 100, 0.045, 8, false), solidMat({ color: 0x333333 }), null, null, { noWire: true });
    o.minY = 0; o.maxY = 3.1;
  })();
  // 5 · delivery: six sprint steps rising to launch
  (function () {
    var o = make('process'), m = solidMat({ color: 0x1d1e22 });
    o.steps = [];
    for (var k = 0; k < 6; k++) {
      var a = -2.2 + k * 0.62, R = 2.3, h = 0.25 + k * 0.42, x = Math.cos(a) * R, z = Math.sin(a) * R * 0.6;
      o.steps.push(add(o, new THREE.CylinderGeometry(0.42, 0.46, h, 32), m.clone(), V(x, h / 2, z)));
      add(o, new THREE.CylinderGeometry(0.012, 0.012, 0.7, 6), m.clone(), V(x, h + 0.35, z), null, { noWire: true });
      o.flag = add(o, new THREE.PlaneGeometry(0.42, 0.26), new THREE.MeshStandardMaterial({ color: 0xffffff, side: THREE.DoubleSide, emissive: 0xffffff, emissiveIntensity: 0.2 }), V(x + 0.22, h + 0.57, z), null, { noWire: true, noShadow: true });
      o.steps[k].flag = o.flag;
    }
    o.minY = 0; o.maxY = 3.3;
  })();

  // the scan plane: a glowing ring that rides the wire cut
  var scan = new THREE.Mesh(new THREE.RingGeometry(0.2, 2.75, 96, 1), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.0, side: THREE.DoubleSide, depthWrite: false, blending: THREE.AdditiveBlending }));
  scan.rotation.x = -Math.PI / 2; turn.add(scan);
  var scanEdge = new THREE.Mesh(new THREE.TorusGeometry(2.75, 0.01, 6, 160), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0 })); scanEdge.rotation.x = Math.PI / 2; turn.add(scanEdge);

  // dust
  var DN = lowEnd ? 500 : 1300, dg = new THREE.BufferGeometry(), dp = new Float32Array(DN * 3);
  for (var i = 0; i < DN; i++) { dp[i * 3] = (Math.random() - 0.5) * 22; dp[i * 3 + 1] = Math.random() * 8; dp[i * 3 + 2] = (Math.random() - 0.5) * 22; }
  dg.setAttribute('position', new THREE.BufferAttribute(dp, 3));
  var dust = new THREE.Points(dg, new THREE.PointsMaterial({ size: 0.03, transparent: true, opacity: 0.4, depthWrite: false })); scene.add(dust);

  // ---------- post ----------
  var composer = new THREE.EffectComposer(renderer);
  composer.addPass(new THREE.RenderPass(scene, camera));
  var bokeh = null;
  if (!lowEnd && THREE.BokehPass) { bokeh = new THREE.BokehPass(scene, camera, { focus: 9, aperture: 0.0022, maxblur: 0.006, width: 1, height: 1 }); composer.addPass(bokeh); }
  var bloom = new THREE.UnrealBloomPass(new THREE.Vector2(1, 1), 0.6, 0.5, 0.8); composer.addPass(bloom);
  var finalPass = new THREE.ShaderPass({
    uniforms: { tDiffuse: { value: null }, uTime: { value: 0 }, uVig: { value: new THREE.Color(0.8, 0.8, 0.8) } },
    vertexShader: 'varying vec2 vUv; void main(){ vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }',
    fragmentShader: 'uniform sampler2D tDiffuse; uniform float uTime; uniform vec3 uVig; varying vec2 vUv; void main(){ vec4 c=texture2D(tDiffuse,vUv); vec3 col=pow(max(c.rgb,0.0),vec3(1.0/2.2)); vec2 q=vUv-0.5; float v=smoothstep(1.0,0.32,length(q*vec2(1.0,0.85))*1.3); col=mix(col*uVig,col,v); float g=fract(sin(dot(gl_FragCoord.xy+mod(uTime*61.0,97.0),vec2(12.9898,78.233)))*43758.5453); col+=(g-0.5)*0.035; gl_FragColor=vec4(col,1.0); }'
  });
  composer.addPass(finalPass);

  var ACC = new THREE.Color(), SEC = new THREE.Color(), MIN = new THREE.Color();
  function applyPalette() {
    readPalette(); bgCol.copy(lin(C.bg)); scene.fog.color.copy(bgCol);
    glaze.material.color.copy(lin(C.dark ? C.bg : C.bg2)).multiplyScalar(C.dark ? 1 : 0.92);
    ACC.copy(lin(C.a)); SEC.copy(lin(C.c)); MIN.copy(lin(C.m));
    rim.color.copy(ACC); rim2.color.copy(SEC); rim.intensity = C.dark ? 1.6 : 0.55; rim2.intensity = C.dark ? 1.0 : 0.45; discRing.material.color.copy(ACC);
    discGrid.material.color.copy(C.dark ? new THREE.Color(1, 1, 1) : lin(C.text)); discGrid.material.opacity = C.dark ? 0.16 : 0.22;
    floorGrid.material.color.set(C.dark ? 0xffffff : 0x000000);
    scan.material.color.copy(ACC); scanEdge.material.color.copy(ACC);
    hemi.color.copy(lin(C.dark ? '#c9cfe0' : '#ffffff')); hemi.groundColor.copy(bgCol); hemi.intensity = C.dark ? 0.35 : 0.55;
    key.intensity = C.dark ? 1.0 : 1.5; renderer.toneMappingExposure = C.dark ? 1.05 : 0.98;
    disc.material.color.copy(lin(C.dark ? '#121418' : '#1b1719'));
    bloom.threshold = C.dark ? 0.72 : 0.9; bloom.strength = C.dark ? 0.55 : 0.32;
    dust.material.color.copy(lin(C.dark ? '#ffffff' : C.text)); dust.material.opacity = C.dark ? 0.4 : 0.2;
    Object.keys(OBJ).forEach(function (k) { OBJ[k].wires.forEach(function (w) { w.material.color.copy(ACC); }); OBJ[k].textures.forEach(function (t) { t[2](t[1]); t[0].needsUpdate = true; }); });
    // colour accents on the objects
    var sheet = OBJ.sheet; sheet.solids[1].material.color.copy(ACC); sheet.solids[1].material.metalness = 0.2;
    OBJ.ai.nodes[2].material.color.copy(ACC); OBJ.ai.nodes[2].material.emissive = ACC.clone(); OBJ.ai.nodes[2].material.emissiveIntensity = 0.5;
    OBJ.ai.pulses.forEach(function (p) { p.material.color.copy(ACC).lerp(new THREE.Color(1, 1, 1), 0.3); });
    OBJ.dash.bars.forEach(function (b) { var c = [ACC, SEC, MIN][b[1]]; b[0].material.color.copy(c); b[0].material.emissive = c.clone(); b[0].material.emissiveIntensity = 0.12; });
    OBJ.dash.ribbon.material.color.copy(ACC); OBJ.dash.ribbon.material.emissive = ACC.clone(); OBJ.dash.ribbon.material.emissiveIntensity = 0.6;
    OBJ.process.steps.forEach(function (s, k) { var c = k === 5 ? MIN : ACC; s.flag.material.color.copy(c); s.flag.material.emissive = c.clone(); s.flag.material.emissiveIntensity = 0.5; });
    var b = new THREE.Color(C.bg), sh = new THREE.Color(C.dark ? '#000000' : C.line);
    finalPass.uniforms.uVig.value.set(C.dark ? 0.6 : 0.5 + 0.5 * sh.r / Math.max(0.01, b.r), C.dark ? 0.6 : 0.5 + 0.5 * sh.g / Math.max(0.01, b.g), C.dark ? 0.6 : 0.5 + 0.5 * sh.b / Math.max(0.01, b.b));
  }
  applyPalette();
  new MutationObserver(applyPalette).observe(root, { attributes: true, attributeFilter: ['class', 'data-palette'] });

  // ---------- timeline + shots ----------
  var ORDER = ['sheet', 'web', 'mobile', 'ai', 'dash', 'process'];
  var RANGES = { sheet: [0, 1.0], web: [1.0, 2.65], mobile: [2.65, 4.3], ai: [4.3, 5.95], dash: [5.95, 7.6], process: [7.6, 9.2] };
  var END = 9.2;
  // camera orbit per chapter: [yaw, height, distance]
  var SHOT = { sheet: [0.55, 4.2, 11.5], web: [-0.35, 3.0, 9.0], mobile: [0.45, 2.6, 9.4], ai: [-0.2, 3.4, 10.0], dash: [0.75, 5.2, 10.5], process: [-0.6, 4.6, 11.5] };
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function fit(v, a, b) { return clamp((v - a) / (b - a), 0, 1); }
  function ease(t) { return t * t * (3 - 2 * t); }
  function easeIO(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }

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
  function resize() { vw = stage.clientWidth; vh = stage.clientHeight; mobile = vw < 760; renderer.setSize(vw, vh, false); composer.setSize(vw, vh); camera.aspect = vw / vh; camera.fov = mobile ? 52 : 36; camera.updateProjectionMatrix(); if (bokeh) bokeh.uniforms.aspect.value = vw / vh; }
  function shotFor(name) {
    var s = SHOT[name], d = s[2] * (mobile ? 1.25 : 1);
    var pos = V(Math.sin(s[0]) * d, s[1], Math.cos(s[0]) * d);
    var fwd = V(0, 1.2, 0).sub(pos).normalize(), right = new THREE.Vector3().crossVectors(fwd, V(0, 1, 0)).normalize();
    var tgt = V(0, mobile ? 2.2 : 1.25, 0).addScaledVector(right, mobile ? 0 : -2.4);
    return { pos: pos, tgt: tgt, focus: d };
  }

  function secTop() { return sec.getBoundingClientRect().top + window.scrollY; }
  var seekTo = null; sec.__seek = function (v) { seekTo = v; sCur = v; };
  function target() { return seekTo !== null ? seekTo : clamp((window.scrollY - secTop()) / vh, 0, END); }
  var sCur = 0, last = performance.now(), t0 = last, visible = true;
  new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }, { rootMargin: '200px 0px' }).observe(sec);

  function frame(now) {
    requestAnimationFrame(frame);
    var dt = Math.min(0.05, (now - last) / 1000); last = now;
    if (!visible) return;
    var tg = target(); sCur = reduced ? tg : sCur + (tg - sCur) * (1 - Math.exp(-dt * 5));
    var s = sCur, time = (now - t0) / 1000;
    var scanY = -1, scanVis = 0, activeName = 'sheet', activeT = 0;

    ORDER.forEach(function (name, idx) {
      var o = OBJ[name], r = RANGES[name], t = fit(s, r[0], r[1]), first = idx === 0, lastCh = idx === ORDER.length - 1;
      var build = first ? ease(fit(s, 0, 0.6)) : ease(fit(t, 0.02, 0.4));
      var solid = first ? ease(fit(s, 0.15, 0.75)) : ease(fit(t, 0.14, 0.55));
      var gone = lastCh ? 0 : ease(fit(t, 0.86, 1.0));
      if (!first && s < r[0]) { build = 0; solid = 0; }
      var span = o.maxY - o.minY + 0.3;
      var wireCut = o.minY - 0.05 + span * build * (1 - gone), solidCut = o.minY - 0.05 + span * solid * (1 - gone);
      o.wireP.constant = wireCut + turn.position.y; o.solidP.constant = solidCut + turn.position.y;
      o.g.visible = wireCut > o.minY - 0.04;
      o.wires.forEach(function (w) { w.material.opacity = (0.95 - 0.7 * solid) * (1 - gone * 0.3); });
      if (o.extra) o.extra(solid * (1 - gone), time);
      if (build > 0 && build < 1 && !gone) { scanY = wireCut; scanVis = Math.sin(build * Math.PI); }
      if (gone > 0 && gone < 1) { scanY = wireCut; scanVis = Math.max(scanVis, Math.sin(gone * Math.PI) * 0.6); }
      if (s >= r[0] && s < r[1]) { activeName = name; activeT = t; }
    });
    scan.position.y = scanEdge.position.y = Math.max(0.02, scanY);
    scan.material.opacity = (C.dark ? 0.16 : 0.07) * scanVis; scanEdge.material.opacity = (C.dark ? 0.9 : 0.55) * scanVis; scan.visible = scanEdge.visible = scanVis > 0.01;
    turn.rotation.y = reduced ? 0 : time * 0.06;

    // camera: glide between chapter shots
    var idxF = 0; ORDER.forEach(function (n, k) { if (s >= RANGES[n][0]) idxF = k + (k < ORDER.length - 1 ? ease(fit(s, RANGES[n][1] - 0.35, RANGES[n][1] + 0.1)) : 0); });
    var i0 = Math.floor(idxF), i1 = Math.min(ORDER.length - 1, i0 + 1), f = easeIO(idxF - i0);
    var A = shotFor(ORDER[i0]), B = shotFor(ORDER[i1]);
    // interpolate the orbit angle rather than the straight line, so the camera swings round
    var sa = SHOT[ORDER[i0]], sb = SHOT[ORDER[i1]], yaw = sa[0] + (sb[0] - sa[0]) * f, hgt = sa[1] + (sb[1] - sa[1]) * f, dist = (sa[2] + (sb[2] - sa[2]) * f) * (mobile ? 1.25 : 1);
    if (s < 0.9) { dist += (1 - ease(fit(s, 0, 0.9))) * 2.5; hgt += (1 - ease(fit(s, 0, 0.9))) * 1.2; }
    camera.position.set(Math.sin(yaw) * dist, hgt, Math.cos(yaw) * dist);
    camera.lookAt(A.tgt.clone().lerp(B.tgt, f));
    if (bokeh) bokeh.uniforms.focus.value = dist;

    // code panel
    var cd = CODE[activeName], co = cd ? ease(fit(activeT, 0.2, 0.32)) * (1 - ease(fit(activeT, 0.84, 0.96))) : 0;
    code.style.opacity = co.toFixed(3); code.style.transform = 'translateY(' + ((1 - co) * 12).toFixed(1) + 'px)';
    if (cd) { if (lastCode !== activeName) { lastCode = activeName; lastN = -1; lang.textContent = cd[0]; } var n = Math.round(plainLen(cd[1]) * fit(activeT, 0.26, 0.7)); if (n !== lastN) { lastN = n; pre.innerHTML = typed(cd[1], n) + '<span class="caret"></span>'; } }
    // copy
    copies.forEach(function (c) {
      var r = c.dataset.range.split(',').map(parseFloat), fade = 0.26;
      var o = r[0] <= 0 ? 1 - fit(s, r[1], r[1] + fade) : r[1] >= END ? fit(s, r[0] - fade, r[0]) : Math.min(fit(s, r[0] - fade, r[0]), 1 - fit(s, r[1], r[1] + fade));
      c.style.opacity = o.toFixed(3);
      c.style.transform = mobile ? 'translateY(' + ((1 - o) * 14).toFixed(1) + 'px)' : 'translateY(calc(-46% + ' + ((1 - o) * 14).toFixed(1) + 'px))';
      c.classList.toggle('on', o > 0.5);
    });
    var hint = sec.querySelector('.bp-hint'); if (hint) hint.style.opacity = 1 - fit(s, 0.05, 0.4);
    dust.rotation.y = time * 0.012;
    finalPass.uniforms.uTime.value = time;
    composer.render();
  }
  resize(); window.addEventListener('resize', resize);
  sCur = target();
  requestAnimationFrame(function (now) { last = now; requestAnimationFrame(frame); });
  sec.classList.add('gl');
})();
