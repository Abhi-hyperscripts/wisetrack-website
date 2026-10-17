"""Colour maths and the palette registry shared by tokenise-colours.py and build-palettes.py.

Every site colour literal belongs to one of four families, named after the Curd & Sindoor
originals: taupe (the maroon-tinted neutrals, paper and ink), sindoor (the accent), brass
(the secondary, gold) and leaf (the green used for positive states). A palette gives each
family a target: taupe takes a hue and a chroma, the others take one anchor colour. Every
token is then retinted by the same transform, so the relationships between tints, tones and
shades survive the change of palette.
"""
import json, math, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(ROOT, 'tools', 'palette_tokens.json')

# ---------------------------------------------------------------- sRGB <-> OKLCH
def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def _gam(c):
    c = max(0.0, min(1.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055

def hex_to_oklch(h):
    r, g, b = [_lin(int(h[i:i + 2], 16)) for i in (0, 2, 4)]
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = l ** (1 / 3), m ** (1 / 3), s ** (1 / 3)
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    bb = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return L, math.hypot(a, bb), (math.degrees(math.atan2(bb, a)) + 360) % 360

def _oklch_to_rgb_lin(L, C, H):
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)

def oklch_to_hex(L, C, H):
    """Clip to the sRGB gamut by lowering chroma, never by shifting hue or lightness."""
    L = max(0.0, min(1.0, L))
    lo, hi = 0.0, C
    rgb = _oklch_to_rgb_lin(L, C, H)
    if not all(-0.0005 <= v <= 1.0005 for v in rgb):
        for _ in range(24):
            mid = (lo + hi) / 2
            rgb = _oklch_to_rgb_lin(L, mid, H)
            if all(-0.0005 <= v <= 1.0005 for v in rgb): lo = mid
            else: hi = mid
        rgb = _oklch_to_rgb_lin(L, lo, H)
    return '#%02x%02x%02x' % tuple(round(_gam(v) * 255) for v in rgb)

def hex_to_rgb_triplet(h):
    return '%d %d %d' % tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))

# ---------------------------------------------------------------- families
# Leftovers from the previous (Aurora) theme and off-palette one-offs, folded onto their
# Curd & Sindoor equivalent before classification.
ALIASES = {
    '8b5cf6': 'd8261c', '818cf8': 'ff6a45', '1e1e6c': '6e0d12', 'f472b6': 'ff6a45',
    'c6c2d8': 'c9a9a9', 'bcbad0': 'c9a9a9', '1f2937': '3b0d14', '080912': '2a0810',
    '0f1018': '2a0810', 'f1f5f9': 'f8f3ec', 'eaeaf5': 'fffdf9', 'eef0ff': 'fffdf9',
    'bef264': '9fd3a6',
}
# Never retinted: pure black and white, and the WhatsApp greens on the chat button.
EXCLUDE = {'000000', 'ffffff', '25d366', '1fad53', '15803d'}

def family_of(h):
    L, C, H = hex_to_oklch(h)
    if 110 <= H < 200: return 'leaf'
    if (H >= 330 or H < 50) and C > 0.12: return 'sindoor'
    if 240 <= H < 330 and C > 0.10: return 'sindoor'
    if 50 <= H < 110 and C >= 0.03: return 'brass'
    return 'taupe'

# Source anchors (the Curd & Sindoor palette).
SRC = {
    'taupe': {'h': 12.0, 'c': 0.072},
    'sindoor': hex_to_oklch('d8261c'),
    'brass': hex_to_oklch('b8903f'),
    'leaf': hex_to_oklch('4f7a3a'),
}

PALETTES = [
    {'id': 'curd-sindoor', 'name': 'Curd & Sindoor', 'taupe': (12.0, 0.072), 'sindoor': 'd8261c', 'brass': 'b8903f', 'leaf': '4f7a3a'},
    {'id': 'curd-maroon', 'name': 'Curd & Maroon', 'taupe': (12.0, 0.072), 'sindoor': '7d1426', 'brass': 'b8903f', 'leaf': '4f7a3a'},
    {'id': 'saffron', 'name': 'Saffron', 'taupe': (40.0, 0.045), 'sindoor': 'c9560f', 'brass': '8a6a26', 'leaf': '4f7a3a'},
    {'id': 'emerald', 'name': 'Emerald', 'taupe': (160.0, 0.014), 'sindoor': '0f7d5a', 'brass': 'c9a55a', 'leaf': '3f6b34'},
    {'id': 'cobalt', 'name': 'Cobalt', 'taupe': (250.0, 0.022), 'sindoor': '1d4fb8', 'brass': 'd9a441', 'leaf': '2f8f5b'},
    {'id': 'aurora', 'name': 'Aurora', 'taupe': (265.0, 0.032), 'sindoor': '6366f1', 'brass': '22b8d4', 'leaf': '84cc16'},
    {'id': 'graphite', 'name': 'Graphite & Sky', 'taupe': (250.0, 0.006), 'sindoor': '0284c7', 'brass': 'e0a526', 'leaf': '2f9e5a'},
]

def retint(h, fam, pal):
    """Move one source colour into the palette's version of its family."""
    L, C, H = hex_to_oklch(h)
    if fam == 'taupe':
        th, tc = pal['taupe']
        return oklch_to_hex(L, C * (tc / SRC['taupe']['c']), H + (th - SRC['taupe']['h']))
    Ls, Cs, Hs = SRC[fam]
    Lt, Ct, Ht = hex_to_oklch(pal[fam])
    # lightness: anchor maps to anchor, 0 and 1 stay fixed
    L2 = L * Lt / Ls if L <= Ls else 1 - (1 - L) * (1 - Lt) / (1 - Ls)
    return oklch_to_hex(L2, C * (Ct / Cs), H + (Ht - Hs))

# ---------------------------------------------------------------- registry
def load_registry():
    with open(REGISTRY, encoding='utf-8') as f: return json.load(f)

def save_registry(reg):
    with open(REGISTRY, 'w', encoding='utf-8') as f: json.dump(reg, f, indent=1, sort_keys=True)

HEX_RE = re.compile(r'#([0-9a-fA-F]{6})\b')
RGBA_RE = re.compile(r'rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*(?:,\s*([0-9.]+%?)\s*)?\)')
