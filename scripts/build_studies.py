#!/usr/bin/env python3
"""Build the MkDocs source tree for all Studies.

Reads data/studies/ and writes generated output to mkdocs_src/studies/.
Updates the Studies block in mkdocs_nav.yml using sentinel markers
(# <STUDIES> / # </STUDIES>) so the script can be run standalone
without touching the rest of the nav.

Run before `mkdocs build` (or let the pre-commit hook do it automatically):
    python scripts/build_studies.py
"""

from __future__ import annotations

import re
import subprocess
import sys
import shutil
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
_DATA_STUDIES = _REPO / "data" / "studies"
_MKDOCS_STUDIES = _REPO / "mkdocs_src" / "studies"
_NAV_PATH = _REPO / "mkdocs_nav.yml"

NAV_START = "# <STUDIES>"
NAV_END = "# </STUDIES>"

# ── Psalm 119 stanzas ─────────────────────────────────────────────────────────

PSALM119_STANZAS = [
    (1,  "א", "Alef",  1,   8),
    (2,  "ב", "Bet",   9,  16),
    (3,  "ג", "Gimel", 17, 24),
    (4,  "ד", "Dalet", 25, 32),
    (5,  "ה", "He",    33, 40),
    (6,  "ו", "Waw",   41, 48),
    (7,  "ז", "Zayin", 49, 56),
    (8,  "ח", "Ḥet",   57, 64),
    (9,  "ט", "Tet",   65, 72),
    (10, "י", "Yod",   73, 80),
    (11, "כ", "Kaf",   81, 88),
    (12, "ל", "Lamed", 89, 96),
    (13, "מ", "Mem",   97, 104),
    (14, "נ", "Nun",  105, 112),
    (15, "ס", "Samek", 113, 120),
    (16, "ע", "Ayin", 121, 128),
    (17, "פ", "Pe",   129, 136),
    (18, "צ", "Tsade", 137, 144),
    (19, "ק", "Qof",  145, 152),
    (20, "ר", "Resh", 153, 160),
    (21, "שׁ", "Shin", 161, 168),
    (22, "ת", "Taw",  169, 176),
]


# ── Nav helpers ───────────────────────────────────────────────────────────────

def _update_nav(new_block: str) -> None:
    text = _NAV_PATH.read_text(encoding="utf-8")
    wrapped = f"{NAV_START}\n{new_block}{NAV_END}"

    if NAV_START in text:
        pattern = rf"{re.escape(NAV_START)}.*?{re.escape(NAV_END)}"
        updated = re.sub(pattern, wrapped, text, flags=re.DOTALL)
    else:
        # Sentinel absent (e.g. nav was just rewritten by build_mkdocs.py).
        # Insert before "- Study Helps:" or "- API Reference:", whichever
        # comes first; fall back to appending at the end.
        for anchor in ("- Study Helps:", "- API Reference:"):
            if anchor in text:
                updated = text.replace(anchor, wrapped + "\n" + anchor, 1)
                break
        else:
            updated = text.rstrip() + "\n" + wrapped + "\n"

    _NAV_PATH.write_text(updated, encoding="utf-8")


def _build_psalm119_nav() -> str:
    """Return the Studies nav block for Psalm 119."""
    mem_dir = _MKDOCS_STUDIES / "psalm-119" / "memorization"

    lines: list[str] = [
        "- Studies:",
        "  - Overview: studies/index.md",
        "  - Psalm 119:",
        "    - Overview: studies/psalm-119/index.md",
        "    - Analysis — Word Vocabulary & Themes: studies/psalm-119/analysis/psalm-119-report.md",
        "    - Flashcards: studies/psalm-119/flashcards/index.md",
        "    - Memorization Exercises:",
        "      - Overview: studies/psalm-119/memorization/index.md",
    ]

    for num, letter, name, v_start, v_end in PSALM119_STANZAS:
        import unicodedata as _ud
        _n = _ud.normalize("NFKD", name.lower())
        slug = f"{num:02d}-{re.sub(r'[^a-z]', '', _n)}"
        section_dir = mem_dir / slug
        if section_dir.exists():
            lines.append(
                f"      - {letter} {name} (vv. {v_start}–{v_end}): "
                f"studies/psalm-119/memorization/{slug}/index.md"
            )

    return "\n".join(lines) + "\n"


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    _MKDOCS_STUDIES.mkdir(parents=True, exist_ok=True)

    # Copy hand-authored index pages from data/studies/ if present;
    # otherwise leave the existing mkdocs_src/studies/ files in place.
    for src in (_DATA_STUDIES / "psalm-119").glob("*.md"):
        dst = _MKDOCS_STUDIES / "psalm-119" / src.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    # Generate per-section memorization exercises for Psalm 119.
    mem_script = _REPO / "scripts" / "build_psalm119_memorization.py"
    subprocess.run([sys.executable, str(mem_script)], check=True)

    nav_block = _build_psalm119_nav()
    _update_nav(nav_block)
    print("build_studies: Studies nav updated.")


if __name__ == "__main__":
    main()
