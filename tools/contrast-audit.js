#!/usr/bin/env node
/* Contrast audit: every page x every palette x light/dark.

     node tools/contrast-audit.js [baseUrl] [--pages a.html,b.html] [--min 3]

   For each visible element that owns text, take its text colour (alpha composited) and the
   background actually behind it: walk up the ancestors compositing background colours, and for
   gradient backgrounds test against every colour stop (worst case). Text painted with
   background-clip:text, and text over images, video or canvas, is skipped — it has no single
   background to measure. Findings are grouped by a selector signature so one shared component
   reads as one line, with the palettes/themes/pages it fails on. Exit code 1 when anything fails.
*/
const path = require('path');
const fs = require('fs');
let playwright;
for (const p of [process.env.PLAYWRIGHT_PATH, 'playwright'].filter(Boolean)) { try { playwright = require(p); break; } catch (e) {} }
if (!playwright) { console.error('playwright not found; set PLAYWRIGHT_PATH'); process.exit(2); }

const ROOT = path.join(__dirname, '..');
const args = process.argv.slice(2);
const base = (args.find(a => /^https?:/.test(a)) || 'http://localhost:5578/').replace(/\/?$/, '/');
const pagesArg = args.includes('--pages') ? args[args.indexOf('--pages') + 1].split(',') : null;
const MIN = args.includes('--min') ? parseFloat(args[args.indexOf('--min') + 1]) : 3;
const pages = pagesArg || fs.readdirSync(ROOT).filter(f => f.endsWith('.html') && !/^(google|index-1|og-image|yt-banner)/.test(f)).sort();
const palettes = (fs.readFileSync(path.join(ROOT, 'assets/palettes.css'), 'utf8').match(/--palette-list:\s*"([^"]+)"/) || [, 'signal'])[1].split(',');
const themes = ['light', 'dark'];

function probe(MIN) {
  const parse = s => { const m = s.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[\s,\/]+/).filter(Boolean).map(Number); return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1]; };
  const over = (top, under) => { const a = top[3]; return [0, 1, 2].map(i => top[i] * a + under[i] * (1 - a)).concat(1); };
  const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const stops = s => (s.match(/rgba?\([^)]+\)/g) || []).map(parse);
  const sig = el => { let s = el.tagName.toLowerCase(); const c = (el.getAttribute('class') || '').split(/\s+/).filter(x => x && !/^(hidden|md:|sm:|lg:|xl:|group|transition|duration|ease|hover:|focus:)/.test(x)).slice(0, 5); if (c.length) s += '.' + c.join('.'); const p = el.parentElement; if (p && p !== document.body) { const pc = (p.getAttribute('class') || '').split(/\s+/).filter(Boolean).slice(0, 2).join('.'); s = p.tagName.toLowerCase() + (pc ? '.' + pc : '') + ' > ' + s; } return s; };
  const out = [];
  const pageBg = parse(getComputedStyle(document.body).backgroundColor) || [255, 255, 255, 1];
  const rootBg = parse(getComputedStyle(document.documentElement).backgroundColor);
  const canvasBg = pageBg[3] > 0 ? over(pageBg, rootBg && rootBg[3] ? rootBg : [255, 255, 255, 1]) : (rootBg && rootBg[3] ? rootBg : [255, 255, 255, 1]);
  for (const el of document.querySelectorAll('body *')) {
    if (/^(SCRIPT|STYLE|NOSCRIPT|SVG|PATH|CANVAS|VIDEO|IMG|TEMPLATE|OPTION)$/i.test(el.tagName)) continue;
    let own = ''; for (const n of el.childNodes) if (n.nodeType === 3) own += n.textContent; own = own.trim();
    if (!own || own.length < 2) continue;
    const r = el.getBoundingClientRect(); if (r.width < 2 || r.height < 2) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility !== 'visible' || cs.display === 'none') continue;
    if (/text/.test(cs.webkitBackgroundClip || cs.backgroundClip || '')) continue;
    const fill = cs.webkitTextFillColor ? parse(cs.webkitTextFillColor) : null;
    if (fill && fill[3] === 0) continue;            // transparent fill = gradient-clipped text
    let fg = fill || parse(cs.color); if (!fg) continue;
    let opacity = 1, layers = [], skip = false, hidden = false;
    for (let a = el; a && a !== document.documentElement; a = a.parentElement) {
      const as = getComputedStyle(a);
      opacity *= parseFloat(as.opacity);
      if (as.display === 'none' || as.visibility === 'hidden') hidden = true;
      if (/url\(/.test(as.backgroundImage)) { skip = true; break; }
      if (/gradient/.test(as.backgroundImage)) { const st = stops(as.backgroundImage).filter(Boolean); if (st.length) { layers.push({ grad: st }); if (st.every(c => c[3] >= 0.95)) break; } }
      const bg = parse(as.backgroundColor); if (bg && bg[3] > 0) { layers.push({ col: bg }); if (bg[3] >= 0.95) break; }
      if (a.tagName === 'BODY') break;
    }
    if (skip || hidden || opacity < 0.35) continue;
    // a canvas/video sibling painted under this text means no single measurable background
    // (the home and how-we-build scenes); those are checked visually instead
    if (layers.length === 0 && document.querySelector('canvas#gl, #home canvas, #method canvas#gl')) continue;
    // composite background candidates bottom-up; a gradient layer fans out into its stops
    let cands = [canvasBg];
    for (let i = layers.length - 1; i >= 0; i--) {
      const L = layers[i];
      if (L.col) cands = cands.map(c => over(L.col, c));
      else { const n = []; for (const c of cands) for (const s of L.grad) n.push(over(s, c)); cands = n; }
    }
    const worst = Math.min(...cands.map(b => ratio(over(fg, b), b)));
    const px = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight) >= 600;
    const large = px >= 24 || (px >= 18.66 && bold);
    const need = large ? Math.min(MIN, 3) : MIN;
    if (worst < need) out.push({ sig: sig(el), text: own.slice(0, 40), ratio: Math.round(worst * 100) / 100, fg: cs.color, px });
  }
  return out;
}

(async () => {
  const browser = await playwright.chromium.launch();
  const jobs = [];
  for (const pal of palettes) for (const th of themes) jobs.push({ pal, th });
  const agg = new Map();
  let done = 0;
  await Promise.all(Array.from({ length: 4 }, async () => {
    while (jobs.length) {
      const { pal, th } = jobs.shift();
      const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
      await ctx.addInitScript(([p, t]) => { try { localStorage.setItem('palette', p); localStorage.setItem('theme', t); } catch (e) {} }, [pal, th]);
      const pg = await ctx.newPage();
      for (const url of pages) {
        try {
          await pg.goto(base + url, { waitUntil: 'load', timeout: 30000 });
          await pg.waitForTimeout(700);
          // reveal-on-scroll content: force everything visible so it is measured
          await pg.addStyleTag({ content: '[data-reveal],.reveal,.fade,.rise,[class*="opacity-0"]{opacity:1!important;transform:none!important}' });
          const found = await pg.evaluate(probe, MIN);
          for (const f of found) {
            const k = f.sig;
            if (!agg.has(k)) agg.set(k, { sig: k, text: f.text, min: f.ratio, combos: new Set(), pages: new Set(), fg: f.fg });
            const a = agg.get(k); a.combos.add(pal + '/' + th); a.pages.add(url); if (f.ratio < a.min) { a.min = f.ratio; a.text = f.text; a.fg = f.fg; }
          }
        } catch (e) { console.error('ERR', pal, th, url, e.message.split('\n')[0]); }
      }
      await ctx.close();
      done++; process.stderr.write(`  ${done}/${palettes.length * themes.length} ${pal}/${th}\n`);
    }
  }));
  await browser.close();
  const rows = [...agg.values()].sort((a, b) => b.combos.size * b.pages.size - a.combos.size * a.pages.size || a.min - b.min);
  const report = rows.map(r => ({ sig: r.sig, text: r.text, minRatio: r.min, fg: r.fg, combos: [...r.combos].sort(), pages: [...r.pages].sort() }));
  fs.writeFileSync(path.join(ROOT, 'tools', 'contrast-report.json'), JSON.stringify(report, null, 1));
  console.log(`${rows.length} failing components (min ${MIN}:1) across ${pages.length} pages x ${palettes.length} palettes x 2 themes`);
  for (const r of rows.slice(0, 80)) console.log(`${String(r.min).padEnd(5)} ${String(r.combos.size).padStart(2)} combos ${String(r.pages.size).padStart(2)} pages  ${r.sig.slice(0, 110)}  "${r.text}"`);
  process.exit(rows.length ? 1 : 0);
})();
