"""
Build a `{WTT}` icon mark in the spirit of the existing `assets/logo.png` (a
`{S}` curly-brace + monogram), but with "WTT" replacing the S.

Design:
  - Heavy left curly brace `{`        (Helvetica Bold from the OS)
  - "WTT" in Corpta                   (the brand wordmark face)
  - Heavy right curly brace `}`
  - All glyphs in one fill color, tight crop, transparent BG.

Outputs (assets/logo/):
  - icon-wtt-dark.png         dark fill, transparent BG  (matches existing logo.png)
  - icon-wtt-light.png        light fill, transparent BG (for use on dark bg)
  - icon-wtt-light-on-dark.png  light fill on solid bg #07080F
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
CORPTA = ROOT / "assets" / "fonts" / "corpta-demo.otf"
HELVETICA = Path("/System/Library/Fonts/Helvetica.ttc")  # face=1 is Bold
OUT_DIR = ROOT / "assets" / "logo"

DARK = "#0A0A12"
LIGHT = "#EAEAF5"
BG_DARK = "#07080F"

SIZE = 800              # nominal em size; output is cropped to ink
GAP_EM = 0.18           # gap between brace and the inner WTT cluster
BRACE_SCALE = 1.55      # braces drawn taller than the letters
WTT_TRACKING_EM = 0.02  # mild positive tracking — letters breathe, stay readable
# Arcs that BRIDGE the two braces (top + bottom), like the reference {S} mark.
# They span the inner width between the braces; height is a flat dome.
ARC_VISIBLE_H_EM = 0.18 # visible curve height
ARC_STROKE_EM = 0.085   # arc stroke thickness ≈ brace stem
ARC_BRACE_OVERLAP_EM = 0.08  # arc endpoints tuck into the brace tips


def render(out_path: Path, *, color: str, bg: str | None) -> None:
    text_font = ImageFont.truetype(str(CORPTA), SIZE)
    brace_size = int(SIZE * BRACE_SCALE)
    brace_font = ImageFont.truetype(str(HELVETICA), brace_size, index=1)

    tracking_px = SIZE * WTT_TRACKING_EM
    gap_px = SIZE * GAP_EM

    # Measure WTT with per-glyph tracking.
    wtt = "WTT"
    wtt_w = 0.0
    for i, ch in enumerate(wtt):
        wtt_w += text_font.getlength(ch)
        if i < len(wtt) - 1:
            wtt_w += tracking_px

    # Generous scratch canvas; we crop afterwards.
    pad = SIZE
    text_asc, text_desc = text_font.getmetrics()
    brace_asc, brace_desc = brace_font.getmetrics()
    canvas_w = int(brace_font.getlength("{") + gap_px + wtt_w + gap_px + brace_font.getlength("}") + 2 * pad)
    canvas_h = max(text_asc + text_desc, brace_asc + brace_desc) + 2 * pad

    img = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Vertical baseline alignment: use the Corpta cap-height center as the
    # centerline, and center each brace on that same line via its em-box.
    text_y = pad
    text_baseline = text_y + text_asc
    cap_h = SIZE * 0.70  # Corpta cap ≈ 0.70 em (measured from prior render)
    text_cap_top = text_baseline - cap_h
    text_center_y = (text_cap_top + text_baseline) / 2

    # Brace placement: center its em-box vertically on text_center_y.
    brace_y = int(text_center_y - (brace_asc + brace_desc) / 2)
    brace_x = pad

    # Brace positions
    left_brace_x = brace_x
    left_brace_w = brace_font.getlength("{")
    right_brace_x = brace_x + left_brace_w + gap_px + wtt_w + gap_px
    right_brace_w = brace_font.getlength("}")

    draw.text((left_brace_x, brace_y), "{", font=brace_font, fill=color)
    pen = left_brace_x + left_brace_w + gap_px
    for i, ch in enumerate(wtt):
        draw.text((pen, text_y), ch, font=text_font, fill=color)
        pen += text_font.getlength(ch)
        if i < len(wtt) - 1:
            pen += tracking_px
    draw.text((right_brace_x, brace_y), "}", font=brace_font, fill=color)

    # Arcs that BRIDGE the two braces (top + bottom).
    # Endpoints tuck slightly INTO the inner side of each brace so the curves
    # appear to spring out of the brace tips.
    overlap = SIZE * ARC_BRACE_OVERLAP_EM
    arc_left = left_brace_x + left_brace_w - overlap
    arc_right = right_brace_x + overlap
    visible_h = SIZE * ARC_VISIBLE_H_EM
    box_h = visible_h * 2
    stroke = int(SIZE * ARC_STROKE_EM)

    # Top arc: dome sitting at the top of the brace span.
    # Endpoints (at midline of ellipse box) should land near the brace top tips.
    brace_top_tip_y = brace_y + brace_asc * 0.12  # Helvetica brace top tip drops ~12% from font top
    top_box_midline = brace_top_tip_y
    top_box_top = top_box_midline - visible_h
    draw.arc(
        (arc_left, top_box_top, arc_right, top_box_top + box_h),
        start=180, end=360, fill=color, width=stroke,
    )

    # Bottom arc: cup at the bottom of the brace span.
    brace_bot_tip_y = brace_y + (brace_asc + brace_desc) - brace_asc * 0.12
    bot_box_midline = brace_bot_tip_y
    bot_box_top = bot_box_midline - visible_h
    draw.arc(
        (arc_left, bot_box_top, arc_right, bot_box_top + box_h),
        start=0, end=180, fill=color, width=stroke,
    )

    bbox = img.getbbox()
    if bbox is None:
        raise RuntimeError("nothing rendered")
    ink = img.crop(bbox)

    if bg is None:
        ink.save(out_path, "PNG", optimize=True)
    else:
        out = Image.new("RGBA", ink.size, bg)
        out.alpha_composite(ink)
        out.save(out_path, "PNG", optimize=True)
    print(f"  wrote {out_path.relative_to(ROOT)}  ({ink.size[0]}x{ink.size[1]})")


def main() -> None:
    print("Rendering {WTT} icon variants:")
    render(OUT_DIR / "icon-wtt-dark.png", color=DARK, bg=None)
    render(OUT_DIR / "icon-wtt-light.png", color=LIGHT, bg=None)
    render(OUT_DIR / "icon-wtt-light-on-dark.png", color=LIGHT, bg=BG_DARK)


if __name__ == "__main__":
    main()
