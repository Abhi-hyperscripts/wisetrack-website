/* WiseTrack — interaction layer v2.
   Cursor spotlight, scroll reveals, magnetic buttons, tilt cards,
   counters, parallax, word-reveal, spotlight nav, clock, typewriter,
   sticker float, scroll progress, mobile nav. */
(function () {
  "use strict";

  document.documentElement.classList.add("js");

  const reduceMotion =
    window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ───────── Cursor spotlight ───────── */
  function initCursor() {
    if (reduceMotion) return;
    if (window.matchMedia("(pointer: coarse)").matches) return;

    const dot = document.createElement("div");
    Object.assign(dot.style, {
      position: "fixed", pointerEvents: "none",
      width: "560px", height: "560px", left: "0", top: "0",
      transform: "translate(-50%, -50%)", borderRadius: "9999px",
      background: "radial-gradient(closest-side, rgba(139,92,246,0.38), rgba(34,211,238,0.14) 55%, transparent 75%)",
      filter: "blur(22px)", zIndex: "1", mixBlendMode: "screen",
      opacity: "0", transition: "opacity 600ms ease"
    });
    document.body.appendChild(dot);

    const ring = document.createElement("div");
    Object.assign(ring.style, {
      position: "fixed", pointerEvents: "none",
      width: "26px", height: "26px", left: "0", top: "0",
      transform: "translate(-50%, -50%) scale(1)", borderRadius: "9999px",
      border: "1px solid rgba(235, 233, 245, 0.55)",
      zIndex: "60",
      transition: "transform 200ms ease, opacity 300ms ease, background 200ms ease, border-color 200ms ease",
      opacity: "0"
    });
    document.body.appendChild(ring);

    let tx = 0, ty = 0, cx = 0, cy = 0, rx = 0, ry = 0;
    window.addEventListener("mousemove", (e) => {
      tx = e.clientX; ty = e.clientY;
      dot.style.opacity = "1"; ring.style.opacity = "1";
    });
    window.addEventListener("mouseleave", () => {
      dot.style.opacity = "0"; ring.style.opacity = "0";
    });

    function tick() {
      cx += (tx - cx) * 0.08; cy += (ty - cy) * 0.08;
      rx += (tx - rx) * 0.2;  ry += (ty - ry) * 0.2;
      dot.style.left = cx + "px"; dot.style.top = cy + "px";
      ring.style.left = rx + "px"; ring.style.top = ry + "px";
      requestAnimationFrame(tick);
    }
    tick();

    const sel = "a, button, .tilt, .magnetic, input, textarea, select, [data-cursor]";
    document.querySelectorAll(sel).forEach((el) => {
      el.addEventListener("mouseenter", () => {
        ring.style.transform = "translate(-50%, -50%) scale(1.7)";
        ring.style.background = "rgba(139,92,246,0.18)";
        ring.style.borderColor = "rgba(180,150,255,0.7)";
      });
      el.addEventListener("mouseleave", () => {
        ring.style.transform = "translate(-50%, -50%) scale(1)";
        ring.style.background = "transparent";
        ring.style.borderColor = "rgba(235, 233, 245, 0.55)";
      });
    });
  }

  /* ───────── Word splitter for `.words` ───────── */
  function splitWords() {
    document.querySelectorAll(".words").forEach((el) => {
      if (el.dataset.split === "1") return;
      const html = el.innerHTML;
      // split by space but keep tags intact: walk text nodes
      const walk = (node) => {
        if (node.nodeType === 3) {
          const text = node.nodeValue;
          if (!text.trim()) return;
          const frag = document.createDocumentFragment();
          const parts = text.split(/(\s+)/);
          parts.forEach((p) => {
            if (/^\s+$/.test(p)) frag.appendChild(document.createTextNode(p));
            else if (p.length) {
              const span = document.createElement("span");
              span.className = "word";
              span.textContent = p;
              frag.appendChild(span);
            }
          });
          node.parentNode.replaceChild(frag, node);
        } else if (node.nodeType === 1) {
          // skip script/style; recurse into children but preserve elements
          if (["SCRIPT", "STYLE"].includes(node.tagName)) return;
          // if element has class .word or .char already, skip
          if (node.classList.contains("word") || node.classList.contains("char")) return;
          Array.from(node.childNodes).forEach(walk);
        }
      };
      walk(el);
      // assign --i indices
      el.querySelectorAll(".word").forEach((w, i) => w.style.setProperty("--i", i));
      el.dataset.split = "1";
    });
    document.querySelectorAll(".chars").forEach((el) => {
      if (el.dataset.split === "1") return;
      const text = el.textContent;
      el.textContent = "";
      [...text].forEach((c, i) => {
        const span = document.createElement("span");
        span.className = "char";
        span.textContent = c === " " ? " " : c;
        span.style.setProperty("--i", i);
        el.appendChild(span);
      });
      el.dataset.split = "1";
    });
  }

  /* ───────── Scroll reveals ───────── */
  function initReveal() {
    splitWords();
    const items = document.querySelectorAll(".reveal, .words, .chars");
    if (!items.length) return;
    if (!("IntersectionObserver" in window)) {
      items.forEach((el) => el.classList.add("in"));
      return;
    }
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            const delay = parseInt(e.target.dataset.delay || "0", 10);
            setTimeout(() => e.target.classList.add("in"), delay);
            io.unobserve(e.target);
          }
        });
      },
      { rootMargin: "0px 0px -6% 0px", threshold: 0.06 }
    );
    items.forEach((el) => io.observe(el));
  }

  /* ───────── Counter animation ───────── */
  function initCounters() {
    const counters = document.querySelectorAll("[data-count]");
    if (!counters.length || !("IntersectionObserver" in window)) return;
    function fmt(n, suffix) {
      if (suffix && /M/.test(suffix)) return n.toFixed(n < 10 ? 1 : 0);
      if (suffix && /K/.test(suffix)) return Math.round(n);
      if (Number.isInteger(parseFloat(counters[0].dataset.count))) return Math.round(n).toLocaleString();
      return n.toFixed(n < 10 ? 1 : 0);
    }
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (!e.isIntersecting) return;
          const el = e.target;
          const target = parseFloat(el.dataset.count);
          const suffix = el.dataset.suffix || "";
          const dur = parseInt(el.dataset.dur || "1800", 10);
          const start = performance.now();
          function step(t) {
            const p = Math.min(1, (t - start) / dur);
            const eased = 1 - Math.pow(1 - p, 3);
            el.textContent = fmt(target * eased, suffix) + suffix;
            if (p < 1) requestAnimationFrame(step);
            else el.textContent = fmt(target, suffix) + suffix;
          }
          requestAnimationFrame(step);
          io.unobserve(el);
        });
      },
      { threshold: 0.4 }
    );
    counters.forEach((el) => io.observe(el));
  }

  /* ───────── Magnetic buttons ───────── */
  function initMagnetic() {
    if (reduceMotion) return;
    document.querySelectorAll(".magnetic").forEach((el) => {
      const strength = parseFloat(el.dataset.magnet || "0.35");
      el.addEventListener("mousemove", (ev) => {
        const r = el.getBoundingClientRect();
        const x = ev.clientX - (r.left + r.width / 2);
        const y = ev.clientY - (r.top + r.height / 2);
        el.style.transform = `translate(${x * strength}px, ${y * strength}px)`;
      });
      el.addEventListener("mouseleave", () => { el.style.transform = ""; });
    });
  }

  /* ───────── Tilt cards ───────── */
  function initTilt() {
    if (reduceMotion) return;
    document.querySelectorAll(".tilt").forEach((card) => {
      const max = parseFloat(card.dataset.tilt || "5");
      card.addEventListener("mousemove", (ev) => {
        const r = card.getBoundingClientRect();
        const px = (ev.clientX - r.left) / r.width;
        const py = (ev.clientY - r.top) / r.height;
        const rx = (py - 0.5) * -2 * max;
        const ry = (px - 0.5) * 2 * max;
        card.style.transform = `perspective(1000px) rotateX(${rx}deg) rotateY(${ry}deg)`;
        card.style.setProperty("--mx", px * 100 + "%");
        card.style.setProperty("--my", py * 100 + "%");
      });
      card.addEventListener("mouseleave", () => { card.style.transform = ""; });
    });
  }

  /* ───────── Parallax ───────── */
  function initParallax() {
    if (reduceMotion) return;
    const items = document.querySelectorAll("[data-parallax]");
    if (!items.length) return;
    function tick() {
      const y = window.scrollY;
      items.forEach((el) => {
        const s = parseFloat(el.dataset.parallax || "0.1");
        el.style.transform = `translate3d(0, ${y * s}px, 0)`;
      });
      requestAnimationFrame(tick);
    }
    tick();
  }

  /* ───────── Hero orb scale on scroll ───────── */
  function initOrbScroll() {
    if (reduceMotion) return;
    const orbs = document.querySelectorAll("[data-orb-scale]");
    if (!orbs.length) return;
    function tick() {
      const y = window.scrollY;
      orbs.forEach((el) => {
        const max = parseFloat(el.dataset.orbScale || "0.0008");
        const rot = y * 0.05;
        const s = 1 - Math.min(0.25, y * max);
        el.style.transform = `rotate(${rot}deg) scale(${s})`;
      });
      requestAnimationFrame(tick);
    }
    tick();
  }

  /* ───────── Live clock ───────── */
  function initClock() {
    const node = document.querySelector("[data-clock]");
    if (!node) return;
    const pad = (n) => String(n).padStart(2, "0");
    function set() {
      const d = new Date();
      node.textContent =
        pad(d.getHours()) + ":" + pad(d.getMinutes()) + ":" + pad(d.getSeconds()) + " IST";
    }
    set(); setInterval(set, 1000);
  }

  /* ───────── Typewriter ───────── */
  function initType() {
    document.querySelectorAll("[data-type]").forEach((el) => {
      const items = JSON.parse(el.dataset.type);
      let i = 0, j = 0, deleting = false;
      function loop() {
        const cur = items[i];
        el.textContent = cur.slice(0, j);
        if (!deleting && j < cur.length) { j++; setTimeout(loop, 55); }
        else if (!deleting && j === cur.length) { setTimeout(() => { deleting = true; loop(); }, 1700); }
        else if (deleting && j > 0) { j--; setTimeout(loop, 28); }
        else { deleting = false; i = (i + 1) % items.length; setTimeout(loop, 240); }
      }
      loop();
    });
  }

  /* ───────── Scroll progress bar ───────── */
  function initProgress() {
    const bar = document.querySelector("[data-progress]");
    if (!bar) return;
    function set() {
      const h = document.documentElement.scrollHeight - window.innerHeight;
      const p = h > 0 ? Math.min(1, window.scrollY / h) : 0;
      bar.style.transform = `scaleX(${p})`;
    }
    set(); window.addEventListener("scroll", set, { passive: true });
  }

  /* ───────── Spotlight nav ───────── */
  function initNavSpotlight() {
    document.querySelectorAll(".nav-links").forEach((nav) => {
      const pill = document.createElement("span");
      pill.className = "nav-pill";
      nav.appendChild(pill);
      const links = nav.querySelectorAll("a");
      function move(el) {
        const r = el.getBoundingClientRect();
        const p = nav.getBoundingClientRect();
        pill.style.transform = `translateX(${r.left - p.left - 1}px)`;
        pill.style.width = r.width + "px";
      }
      links.forEach((a) => {
        a.addEventListener("mouseenter", () => move(a));
        a.addEventListener("focus", () => move(a));
      });
      const active = nav.querySelector("a.is-active");
      if (active) {
        requestAnimationFrame(() => { move(active); pill.style.opacity = "0"; });
        nav.addEventListener("mouseleave", () => { pill.style.opacity = "0"; });
      } else {
        nav.addEventListener("mouseleave", () => { pill.style.opacity = "0"; });
      }
    });
  }

  /* ───────── Vertical section rail scroll-spy ───────── */
  function initSectionRail() {
    const rail = document.querySelector("[data-rail]");
    if (!rail) return;
    const links = Array.from(rail.querySelectorAll("a[href^='#']"));
    if (!links.length) return;
    const sections = links
      .map((a) => document.getElementById(a.getAttribute("href").slice(1)))
      .filter(Boolean);
    if (!sections.length) return;

    function activate(id) {
      links.forEach((a) => {
        a.classList.toggle("is-active", a.getAttribute("href") === "#" + id);
      });
    }

    if (!("IntersectionObserver" in window)) {
      activate(sections[0].id);
      return;
    }

    // Track which sections are in the central viewport band; pick the topmost.
    const visible = new Set();
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) visible.add(e.target);
          else visible.delete(e.target);
        });
        if (visible.size) {
          const top = [...visible].sort(
            (a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top
          )[0];
          activate(top.id);
        }
      },
      { rootMargin: "-40% 0px -50% 0px", threshold: 0 }
    );
    sections.forEach((s) => io.observe(s));
    activate(sections[0].id);
  }

  /* ───────── Mobile nav ───────── */
  function initMobileNav() {
    const btn = document.querySelector("[data-menu-toggle]");
    const panel = document.querySelector("[data-menu]");
    if (!btn || !panel) return;
    btn.addEventListener("click", () => {
      const open = panel.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      document.body.style.overflow = open ? "hidden" : "";
    });
    panel.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => {
        panel.classList.remove("open");
        document.body.style.overflow = "";
        btn.setAttribute("aria-expanded", "false");
      })
    );
  }

  /* ───────── Sticker floats with mouse ───────── */
  function initFloatStickers() {
    if (reduceMotion) return;
    const wraps = document.querySelectorAll("[data-stickers]");
    wraps.forEach((wrap) => {
      const items = wrap.querySelectorAll(".sticker.float");
      wrap.addEventListener("mousemove", (e) => {
        const r = wrap.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5;
        const y = (e.clientY - r.top) / r.height - 0.5;
        items.forEach((s, idx) => {
          const strength = (idx + 1) * 6;
          s.style.transform = `translate(${x * strength}px, ${y * strength}px)`;
        });
      });
      wrap.addEventListener("mouseleave", () => {
        items.forEach((s) => (s.style.transform = ""));
      });
    });
  }

  /* ───────── Tiny toast ───────── */
  function showToast(message, kind) {
    let t = document.getElementById("wt-toast");
    if (!t) {
      t = document.createElement("div");
      t.id = "wt-toast";
      Object.assign(t.style, {
        position: "fixed",
        bottom: "94px",
        right: "24px",
        zIndex: "85",
        maxWidth: "320px",
        padding: "12px 14px",
        borderRadius: "12px",
        background: "rgba(8, 9, 18, 0.94)",
        border: "1px solid rgba(190, 242, 100, 0.45)",
        color: "#EAEAF5",
        fontSize: "13.5px",
        lineHeight: "1.4",
        boxShadow: "0 16px 40px -10px rgba(0,0,0,0.55)",
        backdropFilter: "blur(14px)",
        opacity: "0",
        transform: "translateY(8px)",
        transition: "opacity 0.25s ease, transform 0.25s ease",
        pointerEvents: "none",
      });
      document.body.appendChild(t);
    }
    t.textContent = message;
    t.style.borderColor =
      kind === "error" ? "rgba(244, 114, 182, 0.6)" : "rgba(190, 242, 100, 0.45)";
    t.style.opacity = "1";
    t.style.transform = "translateY(0)";
    clearTimeout(t._timer);
    t._timer = setTimeout(() => {
      t.style.opacity = "0";
      t.style.transform = "translateY(8px)";
    }, 4200);
  }

  /* ───────── Form handlers ─────────
     Self-detect form shape and route the submit to a useful place
     (no backend required). Three shapes:
       a) Newsletter — exactly one email input → mailto signup.
       b) Contact brief — multiple fields incl. textarea → compose full
          brief email to support@wisetrack.in.
       c) Auth demo — has password input → toast 'demo mode'. */
  function initFormHandlers() {
    document.querySelectorAll("form").forEach((form) => {
      // Skip mobile menu / search forms that don't have inputs we recognise
      const emailEl = form.querySelector('input[type="email"]');
      const pwEl = form.querySelector('input[type="password"]');
      const textareaEl = form.querySelector("textarea");
      const textInputs = form.querySelectorAll('input[type="text"]');
      const selectEl = form.querySelector("select");
      const hasMultipleFields =
        textareaEl || textInputs.length || selectEl;
      const isNewsletter = !!emailEl && !pwEl && !hasMultipleFields;
      const isContactBrief =
        !!emailEl && !!textareaEl;
      const isAuth = !!pwEl;
      if (!isNewsletter && !isContactBrief && !isAuth) return;

      form.addEventListener("submit", (e) => {
        e.preventDefault();
        const enc = encodeURIComponent;

        if (isAuth) {
          showToast(
            "Demo only — auth isn't wired up yet. Email support@wisetrack.in for portal access.",
            "error"
          );
          return;
        }

        if (isContactBrief) {
          const name = form.querySelector('input[type="text"]')?.value.trim() || "";
          const email = emailEl.value.trim();
          const company = form.querySelectorAll('input[type="text"]')[1]?.value.trim() || "";
          const help = selectEl?.value || "";
          const message = textareaEl.value.trim();
          if (!email || !message) {
            showToast("Please add at least your email and a short brief.", "error");
            return;
          }
          const subject = `Project brief from ${name || email}`;
          const body =
            `Name: ${name}\nEmail: ${email}\nCompany: ${company}\nHelp with: ${help}\n\n` +
            `Brief:\n${message}\n\n— sent from wisetrack.in`;
          window.location.href = `mailto:support@wisetrack.in?subject=${enc(subject)}&body=${enc(body)}`;
          showToast("Mail draft opening — review and send. We reply within one working day.");
          return;
        }

        if (isNewsletter) {
          const email = emailEl.value.trim();
          if (!email) {
            showToast("Add your email to subscribe.", "error");
            return;
          }
          const body = `Please add ${email} to the WiseTrack field-notes list.`;
          window.location.href =
            `mailto:support@wisetrack.in?subject=${enc("Newsletter signup")}&body=${enc(body)}`;
          showToast("Mail draft opening — hit send and you're on the list.");
          form.reset();
        }
      });
    });
  }

  /* ───────── Theme toggle (dark ↔ light) ─────────
     Anti-FOUC inline <head> script already applied 'light' class if
     localStorage said so. Here we inject the nav button + handle clicks. */
  function initThemeToggle() {
    const SVG_MOON = '<svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
    const SVG_SUN  = '<svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>';

    function makeBtn() {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "theme-toggle";
      btn.setAttribute("data-theme-toggle", "");
      btn.setAttribute("aria-label", "Toggle light / dark theme");
      btn.innerHTML = SVG_MOON + SVG_SUN;
      btn.addEventListener("click", function () {
        const isLight = document.documentElement.classList.toggle("light");
        try { localStorage.setItem("theme", isLight ? "light" : "dark"); } catch (e) { /* private mode */ }
      });
      return btn;
    }

    // Mount once into the right-side nav cluster (next to "Start a project").
    // Cluster = the last flex container with .btn-primary inside <nav>.
    const nav = document.querySelector("header nav");
    if (!nav) return;
    const cluster = nav.querySelector(".flex.items-center.gap-3, .flex.items-center.gap-2");
    if (!cluster || cluster.querySelector("[data-theme-toggle]")) return;
    // Insert before "Start a project" so visual order = [toggle][CTA][hamburger]
    const cta = cluster.querySelector("a.btn-primary, .btn-primary");
    const btn = makeBtn();
    if (cta) cluster.insertBefore(btn, cta);
    else cluster.insertBefore(btn, cluster.firstChild);

    // Mobile menu — also expose the toggle inside the hamburger panel so
    // it's reachable when the desktop nav cluster is hidden.
    const mobileMenu = document.querySelector("[data-menu]");
    if (mobileMenu && !mobileMenu.querySelector("[data-theme-toggle-mobile]")) {
      const wrap = document.createElement("div");
      wrap.className = "px-edge pb-6 pt-2 flex items-center gap-3 text-sm text-muted";
      wrap.setAttribute("data-theme-toggle-mobile", "");
      const label = document.createElement("span");
      label.textContent = "Appearance";
      const mBtn = makeBtn();
      wrap.appendChild(label);
      wrap.appendChild(mBtn);
      mobileMenu.appendChild(wrap);
    }
  }

  function init() {
    initThemeToggle();
    initCursor();
    initReveal();
    initCounters();
    initMagnetic();
    initTilt();
    initParallax();
    initOrbScroll();
    initClock();
    initType();
    initProgress();
    initNavSpotlight();
    initSectionRail();
    initMobileNav();
    initFloatStickers();
    initFormHandlers();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
