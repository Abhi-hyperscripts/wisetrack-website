"""
1. Insert the WT mark before the wordmark in the header nav of every HTML page.
2. Swap the favicon links to point at the new wt-mark.svg.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

# Pattern: an <img> for the wordmark inside a flex anchor. We capture the
# wordmark size classes so we can size the WT mark proportionally next to it.
WORDMARK_IMG_RE = re.compile(
    r'<img src="assets/logo/wordmark\.svg" alt="Wisetrack Technologies" '
    r'class="(h-\[(\d+)px\] md:h-\[(\d+)px\]) w-auto" />'
)


def wordmark_replacement(m: re.Match[str]) -> str:
    classes = m.group(1)        # e.g. "h-[14px] md:h-[17px]"
    small = int(m.group(2))     # e.g. 14
    large = int(m.group(3))     # e.g. 17
    # WT mark is taller than the wordmark for visual balance — ~1.6x cap-height
    mark_small = round(small * 1.7)
    mark_large = round(large * 1.7)
    return (
        f'<img src="assets/logo/wt-mark.svg" alt="" aria-hidden="true" '
        f'class="h-[{mark_small}px] md:h-[{mark_large}px] w-auto" />'
        f'<img src="assets/logo/wordmark.svg" alt="Wisetrack Technologies" '
        f'class="{classes} w-auto" />'
    )


# Favicon replacements (point at the vector mark)
FAVICON_OLD_PNG = re.compile(
    r'<link rel="icon" type="image/png" href="assets/logo\.png" />'
)
FAVICON_NEW_SVG = (
    '<link rel="icon" type="image/svg+xml" href="assets/logo/wt-mark.svg" />\n'
    '<link rel="alternate icon" type="image/png" href="assets/logo/wt-mark.png" />'
)

APPLE_TOUCH_OLD = re.compile(
    r'<link rel="apple-touch-icon" href="assets/logo\.png" />'
)
APPLE_TOUCH_NEW = '<link rel="apple-touch-icon" href="assets/logo/wt-mark.png" />'


total_wm = 0
total_fv = 0
total_at = 0
files_touched = 0
for path in sorted(ROOT.glob("*.html")):
    text = path.read_text(encoding="utf-8")
    orig = text
    text, n_wm = WORDMARK_IMG_RE.subn(wordmark_replacement, text)
    text, n_fv = FAVICON_OLD_PNG.subn(FAVICON_NEW_SVG, text)
    text, n_at = APPLE_TOUCH_OLD.subn(APPLE_TOUCH_NEW, text)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        files_touched += 1
        total_wm += n_wm
        total_fv += n_fv
        total_at += n_at
        print(f'  {path.name}: wordmarks={n_wm} favicon={n_fv} apple-touch={n_at}')

print(f'\nDone. {files_touched} files touched. '
      f'wordmark inserts={total_wm}  favicon swaps={total_fv}  apple-touch swaps={total_at}')
