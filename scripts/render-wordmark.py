"""
Render the WISETRACK TECHNOLOGIES. wordmark to PNG (3 color variants) and SVG.

CSS source (assets/styles.css `.brand-wordmark`):
  font-family: Corpta
  font-weight: 400
  text-transform: uppercase
  letter-spacing: 0.04em   -> applied per-glyph as advance offset
Text:   "WISETRACK TECHNOLOGIES" + "." (in violet)
Colors: text #EAEAF5  /  dark #07080F  /  violet period #7C3AED  /  bg #07080F

Outputs go to assets/.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen

ROOT = Path(__file__).resolve().parent.parent
FONT_PATH = ROOT / "assets" / "fonts" / "corpta-demo.otf"
OUT_DIR = ROOT / "assets" / "logo"

TEXT_BASE = "WISETRACK TECHNOLOGIES"   # NBSP between words, matches markup

TEXT_LIGHT = "#EAEAF5"
TEXT_DARK = "#07080F"
BG_DARK = "#07080F"

# Render size — generous so downscaling stays crisp.
FONT_SIZE = 480
LETTER_SPACING_EM = 0.04
PAD_X = 120
PAD_Y = 80


def measure(font: ImageFont.FreeTypeFont, text: str, tracking_px: float) -> tuple[int, int, int]:
    """Return (width, ascent_from_baseline, descent_from_baseline) for a tracked run."""
    ascent, descent = font.getmetrics()
    width = 0
    for i, ch in enumerate(text):
        bbox = font.getbbox(ch)
        advance = font.getlength(ch)
        width += advance
        if i < len(text) - 1:
            width += tracking_px
    return int(round(width)), ascent, descent


def draw_tracked(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str,
                 font: ImageFont.FreeTypeFont, fill: str, tracking_px: float) -> float:
    """Draw `text` at `xy` (top-left baseline-aware) with per-glyph tracking.
    Returns the x advance (pen position after the last glyph including its advance).
    """
    x, y = xy
    pen = float(x)
    for i, ch in enumerate(text):
        draw.text((pen, y), ch, font=font, fill=fill)
        pen += font.getlength(ch)
        if i < len(text) - 1:
            pen += tracking_px
    return pen


def render_png(out_path: Path, *, text_color: str, bg: str | None) -> None:
    font = ImageFont.truetype(str(FONT_PATH), FONT_SIZE)
    tracking_px = FONT_SIZE * LETTER_SPACING_EM

    base_w, ascent, descent = measure(font, TEXT_BASE, tracking_px)
    # Generous scratch canvas; we crop to ink afterwards.
    scratch_w = base_w + 2 * PAD_X
    scratch_h = ascent + descent + 2 * PAD_Y
    scratch = Image.new("RGBA", (scratch_w, scratch_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(scratch)
    draw_tracked(draw, (PAD_X, PAD_Y), TEXT_BASE, font, text_color, tracking_px)

    bbox = scratch.getbbox()  # tight bounds of non-transparent pixels
    if bbox is None:
        raise RuntimeError("nothing rendered")
    ink = scratch.crop(bbox)

    if bg is None:
        ink.save(out_path, "PNG", optimize=True)
    else:
        out = Image.new("RGBA", ink.size, bg)
        out.alpha_composite(ink)
        out.save(out_path, "PNG", optimize=True)

    print(f"  wrote {out_path.relative_to(ROOT)}  ({ink.size[0]}x{ink.size[1]})")


def render_svg(out_path: Path) -> None:
    """Render the wordmark as an SVG with glyphs converted to <path> outlines
    (no font dependency at view time)."""
    tt = TTFont(str(FONT_PATH))
    cmap = tt.getBestCmap()
    glyph_set = tt.getGlyphSet()
    units_per_em = tt["head"].unitsPerEm

    # Use font-size 1000 worth of em units for cleaner numbers in the SVG.
    em = 1000
    scale = em / units_per_em
    tracking_em = LETTER_SPACING_EM * em  # in our em coordinate

    def glyph_for(ch: str):
        gname = cmap.get(ord(ch))
        if gname is None:
            return None, None
        return glyph_set[gname], gname

    # Fallback width for missing-glyph chars (space/NBSP). The demo font omits
    # spaces; use 0.35em which matches how PIL rendered the PNG variants.
    SPACE_ADVANCE = 0.35 * em

    # Build paths and compute layout. Track ink bbox across glyphs (in glyph
    # coords, y-up). x is in em units (post-scale).
    paths: list[str] = []
    x = 0.0
    ink_xmin = float("inf")
    ink_ymin = float("inf")
    ink_xmax = float("-inf")
    ink_ymax = float("-inf")

    base = TEXT_BASE.replace("\xa0", " ")
    for i, ch in enumerate(base):
        glyph, gname = glyph_for(ch)
        if glyph is None:
            advance = SPACE_ADVANCE
        else:
            pen = SVGPathPen(glyph_set)
            glyph.draw(pen)
            d = pen.getCommands()
            advance = tt["hmtx"].metrics[gname][0] * scale

            bp = BoundsPen(glyph_set)
            glyph.draw(bp)
            if bp.bounds is not None:
                gxmin, gymin, gxmax, gymax = bp.bounds
                gxmin *= scale; gxmax *= scale
                gymin *= scale; gymax *= scale
                ink_xmin = min(ink_xmin, x + gxmin)
                ink_xmax = max(ink_xmax, x + gxmax)
                ink_ymin = min(ink_ymin, gymin)
                ink_ymax = max(ink_ymax, gymax)

            if d:
                paths.append(
                    f'<g transform="translate({x:.2f},0) scale({scale:.6f},{-scale:.6f})" '
                    f'fill="{TEXT_LIGHT}"><path d="{d}"/></g>'
                )
        x += advance
        if i < len(base) - 1:
            x += tracking_em

    # Tight viewBox: shift so ink_xmin/ink_ymax map to (0,0) in SVG space.
    # SVG y-axis is flipped relative to font y-up, so the top of the ink in
    # SVG corresponds to ink_ymax in font coords.
    vb_w = ink_xmax - ink_xmin
    vb_h = ink_ymax - ink_ymin
    # Glyph paths live in a coordinate where y=0 is the baseline (post flip).
    # After our outer translate, glyph(x=x0) sits at SVG x=tx + x0, and the
    # top of the glyph (ymax in font coords) sits at SVG y=ty - ymax.
    inner_tx = -ink_xmin
    inner_ty = ink_ymax

    body = "\n  ".join(paths)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w:.2f} {vb_h:.2f}" '
        f'role="img" aria-label="WISETRACK TECHNOLOGIES">\n'
        f'  <title>WISETRACK TECHNOLOGIES</title>\n'
        f'  <g transform="translate({inner_tx:.2f},{inner_ty:.2f})">\n  {body}\n  </g>\n'
        f'</svg>\n'
    )
    out_path.write_text(svg, encoding="utf-8")
    print(f"  wrote {out_path.relative_to(ROOT)}  (viewBox {vb_w:.0f}x{vb_h:.0f})")


def main() -> None:
    print("Rendering wordmark variants:")
    render_png(OUT_DIR / "wordmark-white-transparent.png", text_color=TEXT_LIGHT, bg=None)
    render_png(OUT_DIR / "wordmark-dark-transparent.png", text_color=TEXT_DARK, bg=None)
    render_png(OUT_DIR / "wordmark-white-on-dark.png", text_color=TEXT_LIGHT, bg=BG_DARK)
    render_svg(OUT_DIR / "wordmark.svg")


if __name__ == "__main__":
    main()
