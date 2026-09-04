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
_MKDOCS_SRC = _REPO / "mkdocs_src"
# output/reports/ is the committed source for reports; mkdocs_src/reports/ is
# gitignored and regenerated from it, so scan the tracked source instead.
_SCAN_ROOTS = [
    _REPO / "data" / "lessons",
    _REPO / "output" / "reports",
    _MKDOCS_SRC / "courses",
    _MKDOCS_SRC / "standards",
    _MKDOCS_SRC / "policies",
    _MKDOCS_SRC / "studies",
]

# Match navigation links only; exclude image links (![alt](src)) — broken images
# affect display but not site navigation, so they're out of scope here.
_LINK_RE = re.compile(r"(?<!!)\[(?:[^\]]*)\]\(([^)]+)\)")


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

        # mkdocs promotes foo/bar.md → foo/bar/index.html (directory URLs),
        # so a link like ../x.txt in bar.md resolves to foo/x.txt on the
        # published site even though the filesystem check above uses
        # foo/ as the base. For non-index mkdocs_src files, also accept a
        # link that resolves correctly from the directory-URL base
        # (foo/bar/ → one level deeper than the .md file's directory).
        if (md_file.is_relative_to(_MKDOCS_SRC)
                and md_file.name not in ("index.md", "README.md")):
            dir_url_resolved = (md_file.parent / md_file.stem / path_part).resolve()
            if dir_url_resolved.exists():
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
