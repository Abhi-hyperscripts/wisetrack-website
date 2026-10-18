/* SceneKit — what the WebGL animation styles share so they render like product shots, not like
   a game: an anti-aliased renderer, an MSAA post chain (bloom, then gamma + vignette + grain),
   a studio light environment for reflections, and rounded, bevelled boxes instead of hard ones.
   three r128 (UMD). Used by assets/products/monolith.js and assets/services/hologram.js. */
(function () {
  if (!window.THREE) return;
  var T = window.THREE;

  function device() {
    var isMobile = Math.min(window.innerWidth, window.innerHeight) < 760;
    var cores = navigator.hardwareConcurrency || 4, mem = navigator.deviceMemory || 8;
    var lowEnd = isMobile || cores <= 4 || mem <= 4;
    return { isMobile: isMobile, lowEnd: lowEnd, dpr: Math.min(window.devicePixelRatio || 1, lowEnd ? 1.5 : 2) };
  }

  function renderer(canvas, dev) {
    var r;
    try { r = new T.WebGLRenderer({ canvas: canvas, antialias: true, alpha: false, powerPreference: 'high-performance' }); } catch (e) { return null; }
    r.setPixelRatio(dev.dpr);
    r.toneMapping = T.ACESFilmicToneMapping;
    r.shadowMap.enabled = true; r.shadowMap.type = T.PCFSoftShadowMap;
    return r;
  }

  // a dark studio with soft boxes: reflections on metal, lacquer and glass are what make an
  // object read as real
  function studioEnv(r) {
    var s = new T.Scene();
    s.add(new T.Mesh(new T.BoxGeometry(30, 14, 30), new T.MeshBasicMaterial({ color: new T.Color(0.05, 0.05, 0.06), side: T.BackSide })));
    function box(w, h, x, y, z, rx, ry, k) {
      var m = new T.Mesh(new T.PlaneGeometry(w, h), new T.MeshBasicMaterial({ color: new T.Color(k, k, k), side: T.DoubleSide }));
      m.position.set(x, y, z); m.rotation.set(rx, ry, 0); s.add(m);
    }
    box(12, 3.2, 0, 6.9, 0, Math.PI / 2, 0, 4.2);      // overhead strip
    box(7, 7, -14.9, 4.5, 3, 0, Math.PI / 2, 3.2);      // key softbox, left
    box(4, 9, 14.9, 4, -5, 0, -Math.PI / 2, 2.2);       // fill, right
    box(16, 1.6, 0, 2.6, -14.9, 0, 0, 1.6);             // rim strip behind
    box(16, 1.2, 0, 1.2, 14.9, 0, Math.PI, 0.9);        // low front bounce
    var pm = new T.PMREMGenerator(r), tex = pm.fromScene(s, 0.035).texture; pm.dispose();
    return tex;
  }

  // composer on a multisampled target (WebGL2), so edges stay clean through bloom and grain;
  // FXAA as the fallback on WebGL1
  function post(r, scene, camera, dev, opts) {
    opts = opts || {};
    var w = Math.max(1, window.innerWidth), h = Math.max(1, window.innerHeight), rt = null;
    if (r.capabilities.isWebGL2 && T.WebGLMultisampleRenderTarget) {
      rt = new T.WebGLMultisampleRenderTarget(w * dev.dpr, h * dev.dpr, { format: T.RGBAFormat, type: T.HalfFloatType });
      rt.samples = dev.lowEnd ? 2 : 4;
    }
    var composer = new T.EffectComposer(r, rt || undefined);
    composer.addPass(new T.RenderPass(scene, camera));
    var bloom = new T.UnrealBloomPass(new T.Vector2(w, h), opts.bloom || 0.4, 0.5, 0.85); composer.addPass(bloom);
    var fin = new T.ShaderPass({
      uniforms: { tDiffuse: { value: null }, uTime: { value: 0 }, uVig: { value: new T.Color(0.8, 0.8, 0.8) }, uGrain: { value: 0.022 } },
      vertexShader: 'varying vec2 vUv; void main(){ vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }',
      fragmentShader: 'uniform sampler2D tDiffuse; uniform float uTime, uGrain; uniform vec3 uVig; varying vec2 vUv; void main(){ vec4 c=texture2D(tDiffuse,vUv); vec3 col=pow(max(c.rgb,0.0),vec3(1.0/2.2)); vec2 q=vUv-0.5; float v=smoothstep(1.0,0.32,length(q*vec2(1.0,0.85))*1.3); col=mix(col*uVig,col,v); float g=fract(sin(dot(gl_FragCoord.xy+mod(uTime*61.0,97.0),vec2(12.9898,78.233)))*43758.5453); col+=(g-0.5)*uGrain; gl_FragColor=vec4(col,1.0); }'
    });
    composer.addPass(fin);
    var fxaa = null;
    if (!rt && T.FXAAShader) { fxaa = new T.ShaderPass(T.FXAAShader); composer.addPass(fxaa); }
    function setSize(w2, h2) {
      composer.setSize(w2, h2);
      if (fxaa) fxaa.uniforms.resolution.value.set(1 / (w2 * dev.dpr), 1 / (h2 * dev.dpr));
    }
    return { composer: composer, bloom: bloom, finalPass: fin, setSize: setSize };
  }

  // a box with rounded corners and bevelled edges, centred on the origin
  function rbox(w, h, d, r, bevel) {
    r = Math.min(r, w / 2 - 0.001, h / 2 - 0.001);
    var b = bevel != null ? bevel : Math.min(r * 0.5, d * 0.3);
    var x = -w / 2 + b, y = -h / 2 + b, W = w - 2 * b, H = h - 2 * b, R = Math.max(0.001, r - b);
    var s = new T.Shape();
    s.moveTo(x + R, y); s.lineTo(x + W - R, y); s.quadraticCurveTo(x + W, y, x + W, y + R);
    s.lineTo(x + W, y + H - R); s.quadraticCurveTo(x + W, y + H, x + W - R, y + H);
    s.lineTo(x + R, y + H); s.quadraticCurveTo(x, y + H, x, y + H - R);
    s.lineTo(x, y + R); s.quadraticCurveTo(x, y, x + R, y);
    var depth = Math.max(0.001, d - 2 * b);
    var g = new T.ExtrudeGeometry(s, { depth: depth, bevelEnabled: b > 0, bevelThickness: b, bevelSize: b, bevelSegments: 5, curveSegments: 10 });
    g.translate(0, 0, -depth / 2); g.computeVertexNormals();
    return g;
  }

  // a soft round dot, so point particles are specks of light rather than square pixels
  var dotTex = null;
  function softDot() {
    if (dotTex) return dotTex;
    var c = document.createElement('canvas'); c.width = c.height = 64; var x = c.getContext('2d');
    var g = x.createRadialGradient(32, 32, 0, 32, 32, 32); g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(0.35, 'rgba(255,255,255,0.55)'); g.addColorStop(1, 'rgba(255,255,255,0)');
    x.fillStyle = g; x.fillRect(0, 0, 64, 64); dotTex = new T.CanvasTexture(c); return dotTex;
  }

  function maxAniso(r) { return r.capabilities.getMaxAnisotropy ? r.capabilities.getMaxAnisotropy() : 4; }

  window.SceneKit = { softDot: softDot, device: device, renderer: renderer, studioEnv: studioEnv, post: post, rbox: rbox, maxAniso: maxAniso };
})();
