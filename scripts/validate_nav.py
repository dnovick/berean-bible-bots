#!/usr/bin/env python3
"""Validate that all files referenced in mkdocs_nav.yml exist in mkdocs_src/.

Missing files that are gitignored are treated as warnings (generated content
that build scripts produce but that is not committed to the repo).  Missing
files that are tracked (or unknown to git) are treated as errors.

Exit 0 if no errors (warnings are allowed), exit 1 on errors.

Usage:
    python scripts/validate_nav.py
    python scripts/validate_nav.py --strict   # warnings also fail
"""

from __future__ import annotations

import argparse
import subprocess
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


def _is_gitignored(path: Path) -> bool:
    """Return True if git considers this path gitignored."""
    result = subprocess.run(
        ["git", "check-ignore", "-q", str(path)],
        cwd=_REPO,
        capture_output=True,
    )
    return result.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true",
                        help="treat warnings (gitignored missing files) as errors")
    args = parser.parse_args()

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
    warnings: list[str] = []
    for ref in md_refs:
        target = _DOCS_DIR / ref
        if not target.exists():
            if _is_gitignored(target):
                warnings.append(
                    f"WARN   mkdocs_nav.yml  —  generated file not built: {ref}"
                )
            else:
                errors.append(
                    f"ERROR  mkdocs_nav.yml  —  referenced file not found: {ref}"
                )

    total = len(errors) + len(warnings)
    if total == 0:
        print(f"validate_nav: OK — {len(md_refs)} nav entries checked")
        return 0

    for line in sorted(warnings):
        print(line)
    for line in sorted(errors):
        print(line)
    print()
    if errors:
        print(f"validate_nav: FAILED — {len(errors)} error(s), {len(warnings)} warning(s)")
    else:
        msg = f"{len(warnings)} warning(s) — generated files not built (run build scripts locally)"
        print(f"validate_nav: {msg}")

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
