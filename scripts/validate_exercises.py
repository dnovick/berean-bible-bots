#!/usr/bin/env python3
"""Validate exercise directory structure and content rules.

Each check is a registered function — add new checks to _CHECKS to extend.

Current checks:
  - three-format: every exercise directory has <name>.md, <name>.html, <name>.pdf

Exit 0 if clean (or warnings only without --strict), exit 1 on errors.

Usage:
    python scripts/validate_exercises.py
    python scripts/validate_exercises.py --strict
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Callable

_REPO = Path(__file__).resolve().parent.parent
_LESSONS_DIR = _REPO / "data" / "lessons"

CheckFn = Callable[[Path, list[str], list[str]], None]
_CHECKS: list[tuple[str, CheckFn]] = []


def _register(name: str) -> Callable[[CheckFn], CheckFn]:
    def decorator(fn: CheckFn) -> CheckFn:
        _CHECKS.append((name, fn))
        return fn
    return decorator


def _err(errors: list[str], path: Path, msg: str) -> None:
    errors.append(f"ERROR  {path.relative_to(_REPO)}  —  {msg}")


def _warn(warnings: list[str], path: Path, msg: str) -> None:
    warnings.append(f"WARN   {path.relative_to(_REPO)}  —  {msg}")


# ── Registered checks ─────────────────────────────────────────────────────────

@_register("three-format")
def check_three_formats(ex_dir: Path, errors: list[str], warnings: list[str]) -> None:
    """Every exercise directory must have <name>.md, <name>.html, and <name>.pdf."""
    name = ex_dir.name
    for suffix in (".md", ".html", ".pdf"):
        candidate = ex_dir / f"{name}{suffix}"
        if suffix == ".md":
            # Accept any non-README .md as the exercise file
            has_md = any(
                f.suffix == ".md" and f.name != "README.md"
                for f in ex_dir.iterdir() if f.is_file()
            )
            if not has_md:
                _err(errors, ex_dir, f"missing exercise .md file (expected {name}.md)")
        elif not candidate.exists():
            _err(errors, ex_dir, f"missing {suffix} file (expected {candidate.name})")


# ── Main ──────────────────────────────────────────────────────────────────────

def _iter_exercise_dirs() -> list[Path]:
    return sorted(
        d for d in _LESSONS_DIR.rglob("exercises/*")
        if d.is_dir()
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true",
                        help="treat warnings as errors")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    exercise_dirs = _iter_exercise_dirs()
    for ex_dir in exercise_dirs:
        for _name, check_fn in _CHECKS:
            check_fn(ex_dir, errors, warnings)

    total = len(errors) + len(warnings)
    if total == 0:
        print(f"validate_exercises: OK — {len(exercise_dirs)} exercise directories checked "
              f"({len(_CHECKS)} check(s) each)")
        return 0

    for line in sorted(warnings):
        print(line)
    for line in sorted(errors):
        print(line)
    print()
    if errors:
        print(f"validate_exercises: FAILED — {len(errors)} error(s), {len(warnings)} warning(s)")
    else:
        print(f"validate_exercises: {len(warnings)} warning(s) (use --strict to fail on warnings)")

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
