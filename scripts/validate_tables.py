#!/usr/bin/env python3
"""Validate markdown table conventions across mkdocs_src/.

Current checks:
  - bold-summary-row: WARN when every cell in a data row is bold but the first
    cell does not contain the word "total". Such rows look like intended summary
    rows (pinned to bottom during column-sort) but will sort normally because the
    sortable-tables.js isSummaryRow() check requires the word "total" in the bold
    text. Use "**Total**", "**OT Total**", or "**NT Total**" for summary rows.

Exit 0 if clean (or warnings only without --strict), exit 1 on errors / warnings
under --strict.

Usage:
    python scripts/validate_tables.py
    python scripts/validate_tables.py --strict
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
_DOCS_DIR = _REPO / "mkdocs_src"

# Matches a markdown table data row: | cell | cell | ... |
# Excludes separator rows like |---|---|
_TABLE_ROW_RE = re.compile(r"^\|(.+)\|$")
_SEPARATOR_RE = re.compile(r"^\|[\s:|-]+\|$")

# A single markdown cell content is entirely bold if it matches **...**
# (allowing surrounding whitespace and optional nested formatting).
_ALL_BOLD_CELL_RE = re.compile(r"^\s*\*\*(.+?)\*\*\s*$")

_TOTAL_RE = re.compile(r"\btotal\b", re.IGNORECASE)


def _split_cells(row: str) -> list[str]:
    """Split a markdown table row into individual cell strings."""
    inner = row.strip().lstrip("|").rstrip("|")
    return [c.strip() for c in inner.split("|")]


def _is_separator(row: str) -> bool:
    return bool(_SEPARATOR_RE.match(row.strip()))


def _bold_text(cell: str) -> str | None:
    """Return the inner text if the cell is entirely bold, else None."""
    m = _ALL_BOLD_CELL_RE.match(cell)
    return m.group(1) if m else None


def check_file(path: Path, warnings: list[str]) -> None:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    header_seen = False

    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            header_seen = False
            continue

        if not _TABLE_ROW_RE.match(stripped):
            continue

        if _is_separator(stripped):
            header_seen = True
            continue

        if not header_seen:
            # This is the header row — skip
            continue

        # Data row
        cells = _split_cells(stripped)
        if not cells:
            continue

        bold_texts = [_bold_text(c) for c in cells]

        # All cells bold?
        if not all(t is not None for t in bold_texts):
            continue

        first_bold = bold_texts[0]
        if first_bold is None:
            continue

        if not _TOTAL_RE.search(first_bold):
            rel = path.relative_to(_REPO)
            warnings.append(
                f"WARN   {rel}:{lineno}  —  bold-summary-row: "
                f"all cells bold but first cell \"{first_bold}\" does not contain "
                f"\"total\"; row will sort normally (not pinned). "
                f"Use **Total** / **OT Total** if this is a summary row."
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true",
                        help="treat warnings as errors")
    args = parser.parse_args()

    warnings: list[str] = []
    # Lesson and exercise pages are excluded from column-sort by the JS
    # (any URL containing "/lessons/" is never sorted), so bold-row conventions
    # there are irrelevant to sorting.
    _EXCLUDED = {_DOCS_DIR / "lessons"}
    md_files = sorted(
        f for f in _DOCS_DIR.rglob("*.md")
        if not any(exc in f.parents for exc in _EXCLUDED)
    )
    for f in md_files:
        check_file(f, warnings)

    if not warnings:
        print(f"validate_tables: OK — {len(md_files)} files checked")
        return 0

    for w in warnings:
        print(w)
    print()
    print(f"validate_tables: {len(warnings)} warning(s)")
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
