#!/usr/bin/env python3
"""Validate internal markdown links in lesson and site content files.

Checks that relative [text](path) links in .md files resolve to existing
files. Skips external URLs (http/https), anchor-only links (#heading),
site-absolute links (/path), and mailto: links.

All broken links are reported as WARN (non-blocking) by default because the
repo contains many planned/future content items (unwritten BBA/BBG chapters,
pending vocab decks) whose scaffold files link forward to content not yet
written.  Use --strict to promote warnings to errors and fail the run.

Scans:
  - data/lessons/**/*.md
  - mkdocs_src/**/*.md

Exit 0 always unless --strict and there are warnings, or an internal error.

Usage:
    python scripts/validate_links.py
    python scripts/validate_links.py --strict   # fail on any broken link
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
_SCAN_ROOTS = [
    _REPO / "data" / "lessons",
    _REPO / "mkdocs_src",
]

_LINK_RE = re.compile(r"\[(?:[^\]]*)\]\(([^)]+)\)")


def _is_skippable(target: str) -> bool:
    return (
        target.startswith(("http://", "https://", "mailto:"))
        or target.startswith("#")
        or target.startswith("/")   # site-absolute URL, not a filesystem path
    )


def _check_file(
    md_file: Path,
    errors: list[str],
    warnings: list[str],
) -> None:
    try:
        text = md_file.read_text(encoding="utf-8")
    except Exception as exc:
        warnings.append(f"WARN   {md_file.relative_to(_REPO)}  —  could not read: {exc}")
        return

    for match in _LINK_RE.finditer(text):
        target = match.group(1).strip()
        if _is_skippable(target):
            continue

        # Strip inline anchor
        path_part = target.split("#")[0]
        if not path_part:
            continue

        resolved = (md_file.parent / path_part).resolve()
        if resolved.exists():
            continue

        rel_source = md_file.relative_to(_REPO)
        warnings.append(
            f"WARN   {rel_source}  —  broken link: [{path_part}] → not found"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true",
                        help="treat warnings as errors")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    md_files: list[Path] = []
    for root in _SCAN_ROOTS:
        if root.exists():
            md_files.extend(sorted(root.rglob("*.md")))

    for md_file in md_files:
        _check_file(md_file, errors, warnings)

    total = len(errors) + len(warnings)
    if total == 0:
        print(f"validate_links: OK — {len(md_files)} files checked")
        return 0

    for line in sorted(warnings):
        print(line)
    for line in sorted(errors):
        print(line)
    print()
    if errors:
        print(f"validate_links: FAILED — {len(errors)} broken link(s), {len(warnings)} warning(s)")
    else:
        print(f"validate_links: {len(warnings)} warning(s) (use --strict to fail on warnings)")

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
