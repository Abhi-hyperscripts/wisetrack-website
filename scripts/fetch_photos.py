"""Download a curated set of Unsplash photos for the site.

Unsplash license is permissive for commercial use; no attribution
required. Photo IDs are hand-picked to match dark/tech/cinematic
aesthetics. If any photo fails, falls back to Lorem Picsum
(picsum.photos) with the same seed so we still get a usable file.

Run from repo root: python3 scripts/fetch_photos.py
"""
from __future__ import annotations
import pathlib, urllib.request, urllib.error, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEST = ROOT / "assets" / "photos"
DEST.mkdir(parents=True, exist_ok=True)


# (slug, unsplash photo id, picsum fallback seed, w, h)
# Mixed pool of dark/tech/cinematic Unsplash photos.
# IDs are real Unsplash photo IDs (verified to exist as of writing).
PHOTOS = [
    # ---- Portfolio case studies (5) ----
    ("portfolio-rbi",        "1517248135467-4c7edcad34c4", "qsr-kitchen",  1600, 900),  # kitchen / food prep dark
    ("portfolio-vivo",       "1512941937669-90a1b58e7e9c", "mobile-tech",  1600, 900),  # phone / device
    ("portfolio-elections",  "1518770660439-4636190af475", "data-vis",     1600, 900),  # dark laptop / data
    ("portfolio-maldives",   "1573843981267-be1999ff37cd", "ocean-night",  1600, 900),  # tropical / villa
    ("portfolio-ragenaizer", "1573164713988-8665fc963095", "office-team",  1600, 900),  # team / office

    # ---- Blog post hero images (6) ----
    ("post-build-vs-buy",        "1454165804606-c3d57bc86b40", "fork-road",     1600, 900),
    ("post-turn-down-half",      "1494438639946-1ebd1d20bf85", "stop-sign",     1600, 900),
    ("post-wrong-stack",         "1517694712202-14dd9538aa97", "code-mess",     1600, 900),
    ("post-one-app-vs-seven",    "1542744094-3a31f272c490",   "desk-clean",    1600, 900),
    ("post-postgres-enough",     "1558494949-ef010cbdcc31",   "server-racks",  1600, 900),
    ("post-two-week-demos",      "1506784983877-45594efa4cbe","calendar-plan", 1600, 900),

    # ---- Module images (10): used on homepage 'Inside Ragenaizer'
    #      AND on the corresponding build-* page Proof-of-capability card.
    ("module-vision",   "1517245386807-bb43f82c33c4", "video-meeting",  1200, 800),
    ("module-chat",     "1611162617474-5b21e879e113", "chat-bubbles",   1200, 800),
    ("module-email",    "1526554850534-7c78330d5f90", "inbox-envelope", 1200, 800),
    ("module-drive",    "1545987796-200677ee1011",    "cloud-storage",  1200, 800),
    ("module-hrms",     "1556761175-5973dc0f32e7",    "hr-team",        1200, 800),
    ("module-research", "1551288049-bebda4e38f71",    "analytics",      1200, 800),
    ("module-crm",      "1552664730-d307ca884978",    "sales-pipeline", 1200, 800),
    ("module-pms",      "1542626991-cbc4e32524cc",    "kanban-planning",1200, 800),
    ("module-accounts", "1554224155-6726b3ff858f",    "ledger-money",   1200, 800),
    ("module-lms",      "1503676260728-1c00da094a0b", "learning",       1200, 800),
]


def unsplash_url(photo_id: str, w: int, h: int) -> str:
    # The images.unsplash.com endpoint supports on-the-fly cropping + format
    return (
        f"https://images.unsplash.com/photo-{photo_id}"
        f"?auto=format&fit=crop&w={w}&h={h}&q=78&fm=jpg"
    )


def picsum_url(seed: str, w: int, h: int) -> str:
    return f"https://picsum.photos/seed/{seed}/{w}/{h}"


def fetch(url: str, dest: pathlib.Path) -> bool:
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                          " AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/124.0 Safari/537.36"
        })
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
            if len(data) < 5_000:
                return False  # too small to be a real photo
            dest.write_bytes(data)
            return True
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
        return False


def main() -> int:
    total = len(PHOTOS)
    ok = 0
    for slug, photo_id, seed, w, h in PHOTOS:
        dest = DEST / f"{slug}.jpg"
        if dest.exists() and dest.stat().st_size > 30_000:
            print(f"skip {slug}.jpg (already present)")
            ok += 1
            continue
        # Try Unsplash first.
        if fetch(unsplash_url(photo_id, w, h), dest):
            print(f"unsplash → {slug}.jpg  ({dest.stat().st_size//1024} KB)")
            ok += 1
            continue
        # Fall back to Picsum.
        if fetch(picsum_url(seed, w, h), dest):
            print(f"picsum   → {slug}.jpg  ({dest.stat().st_size//1024} KB)")
            ok += 1
            continue
        print(f"FAIL     → {slug}.jpg")
    print(f"\n{ok}/{total} photos downloaded.")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
