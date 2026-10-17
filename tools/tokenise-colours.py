#!/usr/bin/env python3
"""One-time migration: replace every site colour literal with a palette token.

    python3 tools/tokenise-colours.py

Scans the stylesheet, the Tailwind config, site.js, the home and method scene sources and
the <style> blocks / style="" attributes of every page; registers each distinct colour under
a family token (tools/palette_tokens.json) and rewrites the literal as var(--token) or, where
an alpha was present, rgb(var(--token-rgb) / a). Idempotent: already-tokenised files have no
literals left to match. Run build-palettes.py afterwards to regenerate assets/palettes.css.
"""
import glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from palette_lib import *

os.chdir(ROOT)
reg = load_registry() if os.path.exists(REGISTRY) else {}

def token_for(h, need_rgb):
    return register(reg, h, need_rgb)

def css_sub(text, alpha_value=False):
    """Rewrite literals in CSS text. alpha_value=True is the Tailwind-colour form."""
    def hx(m):
        t = token_for(m.group(1), alpha_value)
        if not t: return m.group(0)
        return 'rgb(var(--%s-rgb) / <alpha-value>)' % t if alpha_value else 'var(--%s)' % t
    def rg(m):
        h = '%02x%02x%02x' % tuple(int(m.group(i)) for i in (1, 2, 3))
        t = token_for(h, True)
        if not t: return m.group(0)
        return 'rgb(var(--%s-rgb) / %s)' % (t, m.group(4)) if m.group(4) is not None else 'rgb(var(--%s-rgb))' % t
    out, pos = [], 0
    # leave url(...) payloads alone (data URIs carry their own colours)
    for u in re.finditer(r'url\((?:[^()]|\([^()]*\))*\)', text):
        out.append(HEX_RE.sub(hx, RGBA_RE.sub(rg, text[pos:u.start()]))); out.append(u.group(0)); pos = u.end()
    out.append(HEX_RE.sub(hx, RGBA_RE.sub(rg, text[pos:])))
    return ''.join(out)

def html_sub(text):
    """Only <style> blocks and style="" attributes; SVG presentation attributes and meta tags stay."""
    text = re.sub(r'(<style[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + css_sub(m.group(2)) + m.group(3), text, flags=re.S)
    return re.sub(r'(\sstyle=")([^"]*)(")', lambda m: m.group(1) + css_sub(m.group(2)) + m.group(3), text)

def rewrite(path, fn):
    s = open(path, encoding='utf-8').read(); o = fn(s)
    if o != s: open(path, 'w', encoding='utf-8').write(o); return 1
    return 0

changed = 0
changed += rewrite('assets/styles.css', css_sub)
# Tailwind: whole-string hex colours become the <alpha-value> form; hex inside longer strings stays plain
def tw_sub(s):
    s = re.sub(r'"#([0-9a-fA-F]{6})"', lambda m: '"' + css_sub('#' + m.group(1), alpha_value=True) + '"', s)
    return css_sub(s)
changed += rewrite('assets/tailwind-config.js', tw_sub)
changed += rewrite('assets/site.js', css_sub)
for src in ('assets/home/src/home.html', 'assets/method/src/scene.html', 'assets/home/src/shell.html', 'assets/method/src/shell.html'):
    changed += rewrite(src, html_sub)
for page in sorted(glob.glob('*.html')):
    if page in ('index.html', 'methodology.html'): continue   # built from their sources
    changed += rewrite(page, html_sub)

save_registry(reg)
fams = {}
for v in reg.values(): fams[v['family']] = fams.get(v['family'], 0) + 1
print('files changed:', changed, '| tokens:', len(reg), fams, '| rgb forms:', sum(v['rgb'] for v in reg.values()))
