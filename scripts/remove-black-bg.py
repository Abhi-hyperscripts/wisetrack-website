"""
Convert the dark background of a logo PNG to transparent.

Uses pixel brightness (max RGB channel) as the alpha source:
  - brightness ≤ T0 → fully transparent
  - brightness ≥ T1 → fully opaque
  - in between     → linear ramp (smooth anti-aliased edges)
"""
from pathlib import Path
import sys
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

SRC = Path("/Users/abhishekanand/.claude/image-cache/3635a1d3-623b-404f-a78e-29662559ba9b/2.png")
DEST = ROOT / "assets" / "logo" / "wisetrack-circular.png"

T0 = 18    # below this brightness → transparent
T1 = 70    # above this → opaque


def main() -> None:
    img = Image.open(SRC).convert("RGBA")
    arr = np.array(img).astype(np.int32)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    brightness = np.maximum(np.maximum(r, g), b)
    alpha = np.clip(((brightness - T0) * 255) / (T1 - T0), 0, 255).astype(np.uint8)
    arr[:, :, 3] = alpha
    out = Image.fromarray(arr.astype(np.uint8), "RGBA")
    out.save(DEST, "PNG", optimize=True)
    print(f"wrote {DEST.relative_to(ROOT)}  ({out.size[0]}x{out.size[1]})")


if __name__ == "__main__":
    main()
