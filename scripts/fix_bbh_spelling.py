#!/usr/bin/env python3
"""One-time cleanup: fix all bbh-spelling warnings in exercise files.

Applies the same substitution map used by validate_exercises.py's bbh-spelling
check to every <name>.html and <name>.md in data/lessons/.  Compound terms
(e.g. hateph-patach, hireq-yod) are applied before simple terms to prevent
partial matches from interfering.

Safe to re-run — already-correct files are unchanged.

Usage:
    python scripts/fix_bbh_spelling.py [--dry-run]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
_LESSONS_DIR = _REPO / "data" / "lessons"

# Applied in order: compound/longer patterns FIRST so that e.g.
# "hateph-patach" → "Hateph Pathach" before "\bpatach\b" → "Pathach" runs.
_SUBSTITUTIONS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bhateph-pathach\b"), "Hateph Pathach"),
    (re.compile(r"\bhateph-patach\b"),  "Hateph Pathach"),
    (re.compile(r"\bhatef\b"),           "Hateph"),
    (re.compile(r"\bhireq-yod\b"),       "Hireq-Yod"),
    (re.compile(r"\bholem[\s-]vav\b"),   "Holem Waw"),
    # vowel names (simple)
    (re.compile(r"\bpatach\b"),          "Pathach"),
    (re.compile(r"\bPatach\b"),          "Pathach"),
    (re.compile(r"\bpatakh\b"),          "Pathach"),
    (re.compile(r"\bPatakh\b"),          "Pathach"),
    (re.compile(r"\bpatah\b"),           "Pathach"),
    (re.compile(r"\bqamets\b"),          "Qamets"),
    (re.compile(r"\btsere\b"),           "Tsere"),
    (re.compile(r"\bseghol\b"),          "Seghol"),
    (re.compile(r"\bholem\b"),           "Holem"),
    (re.compile(r"\bhireq\b"),           "Hireq"),
    (re.compile(r"\bqibbuts\b"),         "Qibbuts"),
    (re.compile(r"\bshureq\b"),          "Shureq"),
    (re.compile(r"\bsheva\b"),           "Shewa"),
    (re.compile(r"\bshewa\b"),           "Shewa"),
    # consonant names
    (re.compile(r"\bAleph\b"),           "Alef"),
    (re.compile(r"\bBeth\b"),            "Bet"),
    (re.compile(r"\bChet\b"),            "Ḥet"),
    (re.compile(r"\bTeth\b"),            "Tet"),
    (re.compile(r"\bKaph\b"),            "Kaf"),
    (re.compile(r"\bSamekh\b"),          "Samek"),
    (re.compile(r"\bQoph\b"),            "Qof"),
    (re.compile(r"\bTav\b"),             "Taw"),
]


def fix_file(path: Path, dry_run: bool) -> int:
    """Apply substitutions; return number of replacements made."""
    text = path.read_text(encoding="utf-8", errors="replace")
    original = text
    for pattern, replacement in _SUBSTITUTIONS:
        text = pattern.sub(replacement, text)
    if text == original:
        return 0
    if not dry_run:
        path.write_text(text, encoding="utf-8")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true",
                        help="report what would change without writing files")
    args = parser.parse_args()

    changed: list[Path] = []
    for ex_dir in sorted(_LESSONS_DIR.rglob("*")):
        if not ex_dir.is_dir():
            continue
        name = ex_dir.name
        for suffix in (".html", ".md"):
            f = ex_dir / f"{name}{suffix}"
            if f.exists() and fix_file(f, args.dry_run):
                changed.append(f)

    action = "Would fix" if args.dry_run else "Fixed"
    for p in changed:
        print(f"  {action}: {p.relative_to(_REPO)}")
    print(f"\n{action} {len(changed)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
