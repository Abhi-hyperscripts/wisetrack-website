#!/usr/bin/env python3
"""Builds index.html from the site shell (header, footer, head) and the home-page concept.
   python3 tools/build-home.py
   Sources: assets/home/src/shell.html (a copy of the previous index.html, for its header/footer)
            assets/home/src/home.html  (the particle home page, self-contained)"""
import re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
home = open(f'{ROOT}/assets/home/src/home.html', encoding='utf-8').read()
site = open(f'{ROOT}/assets/home/src/shell.html', encoding='utf-8').read().split('\n')

css = home[home.index('<style>') + 7:home.index('</style>')]
css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
js = home[home.rindex('<script>') + 8:home.rindex('</script>')]
markup = home[home.index('<div class="bars"'):home.rindex('<footer>')]
markup = re.sub(r'<header class="nav">.*?</header>\n', '', markup, flags=re.S).replace('<div class="bars" id="bars"></div>\n', '')
b0 = home.index('<a class="brand"'); brand = home[b0:home.index('</a>', b0) + 4]
markup = '<div id="home">\n<div hidden aria-hidden="true">' + brand + '</div>\n' + markup + '</div>\n'

DROP = {':root', '*', 'html', 'body', '::selection', 'a'}
def prefix(sel):
    parts = []
    for s in sel.split(','):
        s = s.strip()
        parts.append('#home' + s if s.startswith(('.ready', '.dusk')) else '#home ' + s)
    return ', '.join(parts)
def namespace(block_css):
    out = []
    for b in re.split(r'(?<=\})', block_css):
        if not b.strip(): continue
        m = re.match(r'\s*([^{]+)\{', b, flags=re.S)
        sel = m.group(1).strip()
        if sel == ':root': out.append(b); continue
        if sel in DROP: continue
        out.append(b.replace(m.group(1), prefix(sel) + ' ', 1))
    return ''.join(out)
# split top-level @media / @keyframes blocks from plain rules
pos, ns = 0, ''
for m in re.finditer(r'@(media|keyframes)[^{]*\{', css):
    ns += namespace(css[pos:m.start()])
    depth, i = 1, m.end()
    while depth and i < len(css):
        depth += {'{': 1, '}': -1}.get(css[i], 0); i += 1
    inner = css[m.end():i - 1]
    ns += css[m.start():m.end()] + (inner if m.group(1) == 'keyframes' else namespace(inner)) + '}\n'
    pos = i
ns += namespace(css[pos:])
ns += '''
#home { position: relative; }
#home .ch { min-height: 100svh; }
#home h1, #home h2, #home h3 { font-variation-settings: "SOFT" 60, "WONK" 0; }
html.light body { background: #f8f3ec; }
'''
js = js.replace("var root = document.documentElement, bars = document.getElementById('bars');", "var root = document.getElementById('home'), bars = { classList: { add: function () {} } };")
js = js.replace("var rawS = 0; function onScroll() { rawS = window.scrollY / window.innerHeight; smT = Math.min(LAST, Math.max(0, rawS)); }",
                "var rawS = 0, storyEl = document.querySelector('#home .story'); function onScroll() { var top = storyEl.getBoundingClientRect().top + window.scrollY; rawS = (window.scrollY - top) / window.innerHeight; smT = Math.min(LAST, Math.max(0, rawS)); }")
js = js.replace("portraitImg.src = 'portrait.png';", "portraitImg.src = 'assets/home/portrait.png';").replace("load('screen_home_light.png'", "load('assets/home/screen_home_light.png'")
for must in ('assets/home/portrait.png', 'assets/home/screen_home_light.png', 'storyEl', "getElementById('home')"):
    assert must in js, must

main_i = next(i for i, l in enumerate(site) if l.strip().startswith('<main class="relative pt-[120px]">'))
foot_i = next(i for i, l in enumerate(site) if l.strip().startswith('<footer class="py-16'))
head = '\n'.join(site[:main_i])
head = re.sub(r'<link href="assets/styles.css\?v=[^"]*" rel="stylesheet" />', '<link href="assets/styles.css?v=20261018" rel="stylesheet" />\n  <style id="home-styles">' + ns.replace('\\', '\\\\') + '</style>', head)
head = re.sub(r'assets/tailwind-config.js\?v=[^"]*', 'assets/tailwind-config.js?v=20261018', head)
tail = '\n'.join(site[foot_i:]).replace('</body>', '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>\n<script>' + js + '</script>\n</body>')
page = head + '\n  <main class="relative pt-[120px]">\n' + markup + '  </main>\n' + tail
open(f'{ROOT}/index.html', 'w', encoding='utf-8').write(page)
print('index.html written:', len(page), 'bytes;', ns.count('#home'), 'namespaced selectors')
