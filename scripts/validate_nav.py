#!/usr/bin/env python3
"""Validate that all files referenced in mkdocs_nav.yml exist in mkdocs_src/.

Exit 0 if all referenced files exist, exit 1 if any are missing.

Usage:
    python scripts/validate_nav.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

_REPO = Path(__file__).resolve().parent.parent
_NAV_FILE = _REPO / "mkdocs_nav.yml"
_DOCS_DIR = _REPO / "mkdocs_src"


def _collect_paths(node: object, found: list[str]) -> None:
    """Recursively collect all string leaf values from the nav tree."""
    if isinstance(node, str):
        found.append(node)
    elif isinstance(node, dict):
        for v in node.values():
            _collect_paths(v, found)
    elif isinstance(node, list):
        for item in node:
            _collect_paths(item, found)


def main() -> int:
    if not _NAV_FILE.exists():
        print(f"validate_nav: ERROR — {_NAV_FILE.relative_to(_REPO)} not found")
        return 1

    try:
        with open(_NAV_FILE) as f:
            nav_data = yaml.safe_load(f) or {}
    except Exception as exc:
        print(f"validate_nav: ERROR — YAML parse error: {exc}")
        return 1

    nav = nav_data if isinstance(nav_data, list) else nav_data.get("nav", [])

    refs: list[str] = []
    _collect_paths(nav, refs)

    # Keep only .md paths (skip external URLs and anchors)
    md_refs = [
        r for r in refs
        if r.endswith(".md") and not r.startswith("http")
    ]

    errors: list[str] = []
    for ref in md_refs:
        target = _DOCS_DIR / ref
        if not target.exists():
            errors.append(f"ERROR  mkdocs_nav.yml  —  referenced file not found: {ref}")

    if not errors:
        print(f"validate_nav: OK — {len(md_refs)} nav entries checked")
        return 0

    for line in sorted(errors):
        print(line)
    print()
    print(f"validate_nav: FAILED — {len(errors)} missing file(s)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
