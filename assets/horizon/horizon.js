/* Event Horizon (animation style 05): a black hole ray-traced in real time.
   Every pixel shoots a light ray and integrates its path through Schwarzschild gravity
   (units of the event-horizon radius, rs = 1; acceleration -1.5 h^2 x / r^5). Rays that cross
   the disk plane pick up the accretion disk (temperature falls with radius, Keplerian swirl,
   Doppler beaming), rays inside r = 1 are swallowed, and rays that escape read a lensed
   starfield. The far side of the disk is bent over the top and under the bottom of the shadow,
   which is the halo. Post: bloom, an anamorphic streak, ACES tone mapping, grain, vignette.
   A scroll-driven camera tours six shots; resolution adapts to keep the frame rate up. */
(function () {
  var sec = document.getElementById('horizon'); if (!sec) return;
  var stage = sec.querySelector('.hz-stage'), canvas = sec.querySelector('canvas.hz-gl');
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!window.THREE || !canvas) { sec.classList.add('no-gl'); return; }
  document.documentElement.classList.remove('light');
  new MutationObserver(function () { if (document.documentElement.classList.contains('light')) document.documentElement.classList.remove('light'); }).observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
  var renderer;
  try { renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: false, alpha: false, powerPreference: 'high-performance' }); } catch (e) { renderer = null; }
  if (!renderer) { sec.classList.add('no-gl'); return; }
  var isMobile = Math.min(window.innerWidth, window.innerHeight) < 760;
  var cores = navigator.hardwareConcurrency || 4, mem = navigator.deviceMemory || 8;
  var lowEnd = isMobile || cores <= 4 || mem <= 4;
  var STEPS = lowEnd ? 150 : 260;
  var Q = lowEnd ? 0.5 : Math.min(window.devicePixelRatio || 1, 1.25) * 0.85;   // render scale, adapted at runtime
  renderer.setPixelRatio(Q);

  // ---------- the ray tracer ----------
  var frag = [
    'precision highp float;',
    '#define STEPS ' + STEPS,
    'uniform vec2 uRes; uniform float uTime; uniform vec3 uCam; uniform mat3 uRot; uniform float uFov;',
    'uniform float uIn, uOut, uDop, uHeat;',
    'float hash(vec3 p){ p = fract(p * 0.3183099 + 0.1); p *= 17.0; return fract(p.x * p.y * p.z * (p.x + p.y + p.z)); }',
    'float noise(vec3 x){ vec3 i = floor(x), f = fract(x); f = f * f * (3.0 - 2.0 * f);',
    '  return mix(mix(mix(hash(i), hash(i + vec3(1,0,0)), f.x), mix(hash(i + vec3(0,1,0)), hash(i + vec3(1,1,0)), f.x), f.y),',
    '             mix(mix(hash(i + vec3(0,0,1)), hash(i + vec3(1,0,1)), f.x), mix(hash(i + vec3(0,1,1)), hash(i + vec3(1,1,1)), f.x), f.y), f.z); }',
    'float fbm(vec3 p){ float a = 0.5, s = 0.0; for (int i = 0; i < 5; i++){ s += a * noise(p); p = p * 2.03 + 1.7; a *= 0.5; } return s; }',
    // background: three layers of stars and a faint galactic band, read in the bent ray direction
    'vec3 sky(vec3 d){',
    '  vec3 col = vec3(0.0);',
    '  for (int l = 0; l < 3; l++){',
    '    float sc = 70.0 + float(l) * 110.0; vec3 p = d * sc, c = floor(p); float h = hash(c + float(l) * 17.3);',
    '    if (h > 0.982){ vec3 sp = c + 0.5 + 0.3 * (vec3(hash(c + 1.3), hash(c + 2.7), hash(c + 5.1)) - 0.5); float dd = length(p - sp);',
    '      float b = smoothstep(0.38, 0.0, dd) * (h - 0.982) * 30.0 / (1.0 + float(l)); vec3 tint = mix(vec3(1.0, 0.82, 0.62), vec3(0.7, 0.82, 1.0), hash(c + 9.0)); col += tint * b; }',
    '  }',
    '  float band = exp(-pow(dot(d, normalize(vec3(0.25, 1.0, 0.35))) * 2.6, 2.0));',
    '  col += vec3(0.32, 0.26, 0.36) * band * (0.2 + 0.8 * fbm(d * 7.0)) * 0.22;',
    '  return col;',
    '}',
    // the accretion disk at a point in its plane: colour and opacity
    'vec4 disk(vec3 p, vec3 rd, float r){',
    '  float t = (r - uIn) / (uOut - uIn);',
    '  float ang = atan(p.z, p.x), om = 1.0 / pow(r, 1.5);',
    '  float sw = ang - uTime * om * 2.2;',
    '  vec2 pc = vec2(cos(sw), sin(sw)) * r;',
    '  vec2 cs = vec2(cos(sw), sin(sw));',
    // stretched along the orbit: slow change with angle, fast change with radius -> fine streaks
    '  float n = fbm(vec3(cs * 1.4, r * 2.2 + uTime * 0.015));',
    '  float fil = fbm(vec3(cs * 3.2, r * 9.0));',
    '  float lanes = 0.82 + 0.18 * sin(r * 4.1 + n * 6.0);',
    '  float dens = smoothstep(0.0, 0.05, t) * pow(1.0 - t, 2.0) * (0.3 + 0.95 * n) * mix(0.55, 1.25, fil) * lanes;',
    '  float temp = pow(uIn / r, 0.9);',
    '  vec3 hot = vec3(1.0, 0.96, 0.88), warm = vec3(1.0, 0.58, 0.2), cool = vec3(0.55, 0.16, 0.04);',
    '  vec3 c = mix(cool, warm, smoothstep(0.15, 0.55, temp)); c = mix(c, hot, smoothstep(0.6, 1.0, temp));',
    '  vec3 vel = normalize(vec3(-p.z, 0.0, p.x)) * sqrt(0.5 / r);',
    '  float dop = clamp(1.0 + uDop * dot(vel, -rd) * 2.2, 0.35, 2.4);',
    '  c *= pow(dop, 3.0) * mix(0.6, 1.6, temp) * uHeat;',
    '  return vec4(c * dens * 1.7, clamp(dens * 1.5, 0.0, 1.0));',
    '}',
    'void main(){',
    '  vec2 uv = (gl_FragCoord.xy - 0.5 * uRes) / uRes.y;',
    '  vec3 rd = normalize(uRot * normalize(vec3(uv * uFov, -1.0)));',
    '  vec3 pos = uCam, vel = rd, col = vec3(0.0); float alpha = 0.0; bool swallowed = false;',
    '  vec3 hv = cross(pos, vel); float h2 = dot(hv, hv);',
    '  for (int i = 0; i < STEPS; i++){',
    '    float r = length(pos);',
    '    float dt = clamp(0.06 + 0.1 * r, 0.04, 1.6) * (r < 6.0 ? 0.55 : 1.0);',
    '    vec3 acc = -1.5 * h2 * pos / pow(r, 5.0);',
    '    vec3 np = pos + vel * dt; vel = normalize(vel + acc * dt);',
    '    if (pos.y * np.y < 0.0){',
    '      vec3 cp = mix(pos, np, pos.y / (pos.y - np.y)); float cr = length(cp);',
    '      if (cr > uIn && cr < uOut && alpha < 0.995){ vec4 d = disk(cp, vel, cr); col += (1.0 - alpha) * d.rgb; alpha += (1.0 - alpha) * d.a; }',
    '    }',
    '    pos = np;',
    '    float nr = length(pos);',
    '    if (nr < 1.0){ swallowed = true; break; }',
    '    if (nr > 80.0) break;',
    '  }',
    // a thin glow just outside the shadow: light skimming the photon sphere
    '  if (!swallowed) col += (1.0 - alpha) * sky(normalize(vel));',
    '  gl_FragColor = vec4(col, 1.0);',
    '}'
  ].join('\n');

  var quadScene = new THREE.Scene(), quadCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  var U = {
    uRes: { value: new THREE.Vector2(1, 1) }, uTime: { value: 0 }, uCam: { value: new THREE.Vector3(0, 2, 40) },
    uRot: { value: new THREE.Matrix3() }, uFov: { value: Math.tan(0.6) }, uIn: { value: 3.0 }, uOut: { value: 14.0 }, uDop: { value: 0.55 }, uHeat: { value: 1.0 }
  };
  quadScene.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), new THREE.ShaderMaterial({ uniforms: U, vertexShader: 'void main(){ gl_Position = vec4(position, 1.0); }', fragmentShader: frag, depthTest: false, depthWrite: false })));

  // ---------- post ----------
  var rt = new THREE.WebGLRenderTarget(1, 1, { type: THREE.HalfFloatType, format: THREE.RGBAFormat });
  var composer = new THREE.EffectComposer(renderer, rt);
  composer.addPass(new THREE.RenderPass(quadScene, quadCam));
  var bloom = new THREE.UnrealBloomPass(new THREE.Vector2(1, 1), 0.55, 0.35, 0.92); composer.addPass(bloom);
  var finalPass = new THREE.ShaderPass({
    uniforms: { tDiffuse: { value: null }, uTime: { value: 0 }, uTexel: { value: new THREE.Vector2(1, 1) }, uStreak: { value: 0.6 }, uExpo: { value: 1.0 } },
    vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: [
      'uniform sampler2D tDiffuse; uniform float uTime, uStreak, uExpo; uniform vec2 uTexel; varying vec2 vUv;',
      'vec3 aces(vec3 x){ return clamp((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14), 0.0, 1.0); }',
      'void main(){',
      '  vec3 c = texture2D(tDiffuse, vUv).rgb;',
      // anamorphic streak: a wide horizontal smear of only the brightest light, cooled slightly
      '  vec3 s = vec3(0.0); float w = 0.0;',
      '  for (int i = -12; i <= 12; i++){ float fi = float(i); float k = exp(-abs(fi) * 0.16); vec3 t = texture2D(tDiffuse, vUv + vec2(fi * uTexel.x * 9.0, 0.0)).rgb; s += max(t - 2.2, 0.0) * k; w += k; }',
      '  c += s / w * vec3(0.55, 0.7, 1.0) * uStreak * 1.6;',
      '  c = aces(c * uExpo);',
      '  vec2 q = vUv - 0.5; c *= mix(0.55, 1.0, smoothstep(0.95, 0.3, length(q * vec2(1.0, 0.8)) * 1.25));',
      '  float g = fract(sin(dot(gl_FragCoord.xy + mod(uTime * 61.0, 97.0), vec2(12.9898, 78.233))) * 43758.5453); float lum = dot(c, vec3(0.299, 0.587, 0.114)); c += (g - 0.5) * 0.04 * smoothstep(0.02, 0.25, lum);',
      '  c = pow(max(c, 0.0), vec3(1.0 / 2.2));',
      '  gl_FragColor = vec4(c, 1.0);',
      '}'
    ].join('\n')
  });
  composer.addPass(finalPass);

  // ---------- camera tour ----------
  // each key: position, look-at, roll (radians), field of view (degrees), disk heat
  var V = function (x, y, z) { return new THREE.Vector3(x, y, z); };
  var KEYS = [
    { s: 0.0, p: V(6, 3.2, 62), l: V(0, 0, 0), roll: -0.06, fov: 34, heat: 0.85 },   // approach from deep space
    { s: 1.4, p: V(2, 1.6, 30), l: V(0, 0.2, 0), roll: -0.03, fov: 40, heat: 1.0 },   // closing in
    { s: 2.6, p: V(0, 0.95, 21), l: V(0, 0.35, 0), roll: 0.0, fov: 46, heat: 1.0 },   // the iconic edge-on view, halo over the top
    { s: 3.9, p: V(-9, 14, 9), l: V(0, 0, 0), roll: 0.25, fov: 48, heat: 1.05 },      // swinging up
    { s: 4.9, p: V(0.01, 27, 0.4), l: V(0, 0, 0), roll: 0.0, fov: 50, heat: 1.1 },    // straight down onto the rings
    { s: 6.0, p: V(12, 0.55, 6), l: V(-4, 0.2, -10), roll: -0.12, fov: 64, heat: 1.15 }, // dropping to the disk plane
    { s: 6.9, p: V(3, 0.42, 9.5), l: V(-9, 0.0, -2), roll: -0.18, fov: 70, heat: 1.2 },  // skimming the road of light
    { s: 7.8, p: V(-4.6, 1.3, 3.2), l: V(0, 0, 0), roll: 0.1, fov: 62, heat: 1.25 },    // near the photon sphere
    { s: 8.6, p: V(-20, 6, 26), l: V(0, 0, 0), roll: -0.05, fov: 38, heat: 1.0 },       // pulling back
    { s: 9.4, p: V(-12, 3, 44), l: V(0, 0.4, 0), roll: -0.04, fov: 30, heat: 0.95 }     // the close
  ];
  var END = 9.4;
  var posCurve = new THREE.CatmullRomCurve3(KEYS.map(function (k) { return k.p; }), false, 'centripetal', 0.5);
  var lookCurve = new THREE.CatmullRomCurve3(KEYS.map(function (k) { return k.l; }), false, 'centripetal', 0.5);
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function fit(v, a, b) { return clamp((v - a) / (b - a), 0, 1); }
  function ease(t) { return t * t * (3 - 2 * t); }
  // scroll position -> curve parameter, piecewise so each key is reached at its scroll mark
  function curveT(s) {
    for (var i = 0; i < KEYS.length - 1; i++) {
      var a = KEYS[i], b = KEYS[i + 1];
      if (s <= b.s) { var f = ease(fit(s, a.s, b.s)); return { u: (i + f) / (KEYS.length - 1), a: a, b: b, f: f }; }
    }
    var n = KEYS.length - 1; return { u: 1, a: KEYS[n], b: KEYS[n], f: 1 };
  }
  var camObj = new THREE.PerspectiveCamera(), m4 = new THREE.Matrix4();

  // ---------- copy + letterbox ----------
  var copies = [].slice.call(sec.querySelectorAll('.hz-copy')), bars = sec.querySelectorAll('.hz-bar');

  var vw = 1, vh = 1, mobile = isMobile;
  function resize() {
    vw = stage.clientWidth; vh = stage.clientHeight; mobile = vw < 760;
    renderer.setSize(vw, vh, false); composer.setSize(vw, vh);
    U.uRes.value.set(vw * Q, vh * Q); finalPass.uniforms.uTexel.value.set(1 / (vw * Q), 1 / (vh * Q));
  }
  function setQuality(q) { Q = q; renderer.setPixelRatio(Q); composer.setPixelRatio(Q); resize(); }
  function secTop() { return sec.getBoundingClientRect().top + window.scrollY; }
  var seekTo = null; sec.__seek = function (v) { seekTo = v; sCur = v; };
  function target() { return seekTo !== null ? seekTo : clamp((window.scrollY - secTop()) / vh, 0, END); }
  var sCur = 0, last = performance.now(), t0 = last, visible = true, slow = 0, fast = 0;
  new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }, { rootMargin: '200px 0px' }).observe(sec);

  function frame(now) {
    requestAnimationFrame(frame);
    var dtRaw = (now - last) / 1000, dt = Math.min(0.05, dtRaw); last = now;
    if (!visible) return;
    // keep it fluid: step the render scale down when frames run long, back up when there is room
    if (dtRaw > 0.026) { slow++; fast = 0; } else if (dtRaw < 0.014) { fast++; slow = 0; }
    if (slow > 20 && Q > 0.4) { slow = 0; setQuality(Math.max(0.4, Q - 0.1)); }
    if (fast > 240 && Q < (lowEnd ? 0.6 : 1.0)) { fast = 0; setQuality(Q + 0.05); }

    var tg = target(); sCur = reduced ? tg : sCur + (tg - sCur) * (1 - Math.exp(-dt * 3.2));
    var s = sCur, time = (now - t0) / 1000;
    // the opening drifts in by itself before any scroll
    var intro = reduced ? 1 : ease(fit(time, 0.0, 7.0));
    var c = curveT(s);
    var p = posCurve.getPointAt(Math.min(1, c.u)), l = lookCurve.getPointAt(Math.min(1, c.u));
    if (s < 0.05) p = p.clone().multiplyScalar(1 + (1 - intro) * 0.35);
    var roll = c.a.roll + (c.b.roll - c.a.roll) * c.f, fov = c.a.fov + (c.b.fov - c.a.fov) * c.f, heat = c.a.heat + (c.b.heat - c.a.heat) * c.f;
    if (!reduced) { p.x += Math.sin(time * 0.13) * 0.18; p.y += Math.sin(time * 0.11) * 0.08; roll += Math.sin(time * 0.09) * 0.012; }
    if (mobile) fov *= 1.25;
    camObj.position.copy(p); camObj.up.set(Math.sin(roll), Math.cos(roll), 0); camObj.lookAt(l);
    camObj.updateMatrixWorld(true); m4.extractRotation(camObj.matrixWorld);
    U.uRot.value.setFromMatrix4(m4); U.uCam.value.copy(p);
    U.uFov.value = Math.tan(fov * Math.PI / 360) * 1.0; U.uTime.value = time; U.uHeat.value = heat;
    finalPass.uniforms.uTime.value = time; finalPass.uniforms.uExpo.value = 0.82;

    // copy + letterbox (bars close in for the dramatic shots)
    copies.forEach(function (el) {
      var r = el.dataset.range.split(',').map(parseFloat), fade = 0.3;
      var o = r[0] <= 0 ? 1 - fit(s, r[1], r[1] + fade) : r[1] >= END ? fit(s, r[0] - fade, r[0]) : Math.min(fit(s, r[0] - fade, r[0]), 1 - fit(s, r[1], r[1] + fade));
      el.style.opacity = o.toFixed(3); el.style.transform = 'translateY(' + ((1 - o) * 16).toFixed(1) + 'px)'; el.classList.toggle('on', o > 0.5);
    });
    var lb = Math.max(ease(fit(s, 2.0, 2.6)) * (1 - ease(fit(s, 3.6, 4.1))), ease(fit(s, 5.7, 6.2)) * (1 - ease(fit(s, 8.2, 8.7))));
    for (var b = 0; b < bars.length; b++) bars[b].style.transform = 'scaleY(' + lb.toFixed(3) + ')';
    var hint = sec.querySelector('.hz-hint'); if (hint) hint.style.opacity = 1 - fit(s, 0.05, 0.4);

    composer.render();
  }
  resize(); window.addEventListener('resize', resize);
  sCur = target();
  requestAnimationFrame(function (now) { last = now; requestAnimationFrame(frame); });
  sec.classList.add('gl');
})();
