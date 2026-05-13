"""
One-shot: replace every CSS-rendered `brand-wordmark` span with an <img> tag
pointing to assets/logo/wordmark.svg.

The site has three size patterns:
  - 14/17px (header)
  - 17/20px (footer)
  - 30/34px (og-image template only)

Each becomes:
  <img src="assets/logo/wordmark.svg"
       alt="Wisetrack Technologies"
       class="h-[{small}px] md:h-[{large}px] w-auto" />
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

SPAN_RE = re.compile(
    r'<span class="brand-wordmark text-\[(\d+)px\] md:text-\[(\d+)px\]">'
    r'WISETRACK&nbsp;TECHNOLOGIES'
    r'<span class="text-violet">\.</span>'
    r'</span>'
)


def replacement(m: re.Match[str]) -> str:
    small, large = m.group(1), m.group(2)
    return (
        f'<img src="assets/logo/wordmark.svg" '
        f'alt="Wisetrack Technologies" '
        f'class="h-[{small}px] md:h-[{large}px] w-auto" />'
    )


total = 0
files_touched = 0
for path in sorted(ROOT.glob("*.html")):
    text = path.read_text(encoding="utf-8")
    new_text, n = SPAN_RE.subn(replacement, text)
    if n:
        path.write_text(new_text, encoding="utf-8")
        total += n
        files_touched += 1
        print(f"  {path.name}: {n}")

print(f"\nDone. {total} replacements across {files_touched} files.")
