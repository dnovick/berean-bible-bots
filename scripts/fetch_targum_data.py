"""
Download Targum verse texts from the Sefaria API and save to data/processed/targum.parquet.

Covers:
  Targum Onkelos — Torah (Gen, Exo, Lev, Num, Deu)
  Targum Jonathan — Former Prophets (Jos, Jdg)
                    Latter Prophets (Isa, Jer, Ezk, Hos, Amo, Mic, Nah, Hab, Zec)
  Targum to Psalms (Aramaic Targum to Psalms)

Each row: targum, book_id, chapter, verse, text

Run:
    python scripts/fetch_targum_data.py
"""
import json
import time
import urllib.request
from pathlib import Path

import pandas as pd

OUT = Path("data/processed/targum.parquet")

# (sefaria_ref_base, targum_name, book_id, num_chapters)
BOOKS = [
    # Targum Onkelos
    ("Onkelos_Genesis",      "Onkelos",  "Gen", 50),
    ("Onkelos_Exodus",       "Onkelos",  "Exo", 40),
    ("Onkelos_Leviticus",    "Onkelos",  "Lev", 27),
    ("Onkelos_Numbers",      "Onkelos",  "Num", 36),
    ("Onkelos_Deuteronomy",  "Onkelos",  "Deu", 34),
    # Targum Jonathan — Former Prophets
    ("Targum_Jonathan_on_Joshua",  "Jonathan", "Jos", 24),
    ("Targum_Jonathan_on_Judges",  "Jonathan", "Jdg", 21),
    # Targum Jonathan — Latter Prophets
    ("Targum_Jonathan_on_Isaiah",    "Jonathan", "Isa", 66),
    ("Targum_Jonathan_on_Jeremiah",  "Jonathan", "Jer", 52),
    ("Targum_Jonathan_on_Ezekiel",   "Jonathan", "Ezk", 48),
    ("Targum_Jonathan_on_Hosea",     "Jonathan", "Hos", 14),
    ("Targum_Jonathan_on_Amos",      "Jonathan", "Amo",  9),
    ("Targum_Jonathan_on_Micah",     "Jonathan", "Mic",  7),
    ("Targum_Jonathan_on_Nahum",     "Jonathan", "Nah",  3),
    ("Targum_Jonathan_on_Habakkuk",  "Jonathan", "Hab",  3),
    ("Targum_Jonathan_on_Zechariah", "Jonathan", "Zec", 14),
    # Targum to Psalms
    ("Aramaic_Targum_to_Psalms", "Psalms", "Psa", 150),
]

DELAY = 0.25  # seconds between requests — be polite to Sefaria


def fetch_chapter(ref_base: str, chapter: int) -> list[str]:
    """Return list of verse strings for one chapter (empty string for missing)."""
    url = f"https://www.sefaria.org/api/texts/{ref_base}.{chapter}?context=0&pad=0"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            data = json.loads(r.read())
        he = data.get("he", [])
        if isinstance(he, list):
            return [v if isinstance(v, str) else "" for v in he]
        return []
    except Exception as exc:
        print(f"    WARNING: {ref_base}.{chapter} — {exc}")
        return []


def main() -> None:
    rows: list[dict] = []
    for ref_base, targum, book_id, num_ch in BOOKS:
        print(f"{targum} {book_id}: fetching {num_ch} chapters …")
        for ch in range(1, num_ch + 1):
            verses = fetch_chapter(ref_base, ch)
            for vs_idx, text in enumerate(verses, start=1):
                if text.strip():
                    rows.append({
                        "targum": targum,
                        "book_id": book_id,
                        "chapter": ch,
                        "verse": vs_idx,
                        "text": text.strip(),
                    })
            time.sleep(DELAY)
        book_total = sum(1 for r in rows if r["book_id"] == book_id and r["targum"] == targum)
        print(f"  → {book_total} verses")

    df = pd.DataFrame(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    print(f"\nSaved {len(df):,} verses to {OUT}")


if __name__ == "__main__":
    main()
