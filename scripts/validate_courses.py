#!/usr/bin/env python3
"""Validate course and lesson content structure.

Checks:
  - course.yml has required fields (id, name, textbook)
  - Every session.yml has date: and focus: (non-empty)
  - date: is a valid YYYY-MM-DD string
  - chapter: (if present) is within the valid range for the textbook
  - Every file: reference in sections and files blocks points to a real file
  - Every exercise directory under data/lessons/ has all three formats
    (.html, .pdf, and at least one non-README .md)

Exit 0 if clean, exit 1 if any errors.  Warnings are printed but do not
cause a non-zero exit.

Usage:
    python scripts/validate_courses.py
    python scripts/validate_courses.py --strict   # warnings also count as errors
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

import yaml

_REPO = Path(__file__).resolve().parent.parent
_COURSES_DIR = _REPO / "data" / "courses"
_LESSONS_DIR = _REPO / "data" / "lessons"

# Maximum valid chapter number per textbook (short name → max chapter)
_CHAPTER_MAX: dict[str, int] = {
    "Basics of Biblical Hebrew": 35,
    "Basics of Biblical Greek": 36,
    "Basics of Biblical Aramaic": 22,
}

# ── Helpers ───────────────────────────────────────────────────────────────────


def _err(errors: list[str], path: Path, msg: str) -> None:
    errors.append(f"ERROR  {path.relative_to(_REPO)}  —  {msg}")


def _warn(warnings: list[str], path: Path, msg: str) -> None:
    warnings.append(f"WARN   {path.relative_to(_REPO)}  —  {msg}")


# ── Course-level checks ───────────────────────────────────────────────────────


def _check_course_yml(
    course_yml: Path,
    errors: list[str],
    warnings: list[str],
) -> dict:
    try:
        with open(course_yml) as f:
            data = yaml.safe_load(f) or {}
    except Exception as exc:
        _err(errors, course_yml, f"YAML parse error: {exc}")
        return {}

    for field in ("id", "name", "textbook"):
        if not data.get(field):
            _err(errors, course_yml, f"missing required field: {field!r}")

    return data


# ── Session-level checks ──────────────────────────────────────────────────────


def _check_session_yml(
    session_yml: Path,
    textbook: str,
    errors: list[str],
    warnings: list[str],
) -> None:
    try:
        with open(session_yml) as f:
            data = yaml.safe_load(f) or {}
    except Exception as exc:
        _err(errors, session_yml, f"YAML parse error: {exc}")
        return

    # Required fields
    for field in ("date", "focus"):
        if not data.get(field):
            _err(errors, session_yml, f"missing or empty required field: {field!r}")

    # Date format
    date_val = data.get("date")
    if date_val:
        try:
            datetime.strptime(str(date_val), "%Y-%m-%d")
        except ValueError:
            _err(errors, session_yml, f"date {date_val!r} is not YYYY-MM-DD")

    # Chapter range
    chapter = data.get("chapter")
    if chapter is not None:
        max_ch = _CHAPTER_MAX.get(textbook)
        if max_ch is None:
            _warn(warnings, session_yml, f"unknown textbook {textbook!r}; cannot validate chapter range")
        elif not isinstance(chapter, int) or not (1 <= chapter <= max_ch):
            _err(errors, session_yml, f"chapter {chapter!r} out of range 1–{max_ch} for {textbook!r}")

    session_dir = session_yml.parent

    # File references in sections — warn (file may be planned but not yet written)
    for section in data.get("sections") or []:
        if not isinstance(section, dict):
            continue
        ref = section.get("file")
        if ref and not (session_dir / ref).exists():
            _warn(warnings, session_yml, f"sections file not found: {ref!r}")

    # File references in downloads — error (committed downloads must exist)
    for dl in data.get("files") or []:
        if not isinstance(dl, dict):
            continue
        ref = dl.get("file")
        if ref and not (session_dir / ref).exists():
            _err(errors, session_yml, f"files download not found: {ref!r}")


# ── Exercise-level checks ─────────────────────────────────────────────────────


def _check_exercises(errors: list[str], warnings: list[str]) -> None:
    for ex_dir in sorted(_LESSONS_DIR.glob("*/*/exercises/*/")):
        if not ex_dir.is_dir():
            continue

        has_html = any(ex_dir.glob("*.html"))
        has_pdf = any(ex_dir.glob("*.pdf"))
        # A non-README .md counts; README.md alone does not
        md_files = [f for f in ex_dir.glob("*.md") if f.name.lower() != "readme.md"]
        has_md = bool(md_files)

        if not has_html:
            _err(errors, ex_dir, "missing .html exercise file")
        if not has_pdf:
            _err(errors, ex_dir, "missing .pdf exercise file")
        if not has_md:
            _warn(warnings, ex_dir, "missing standalone .md exercise file (only README.md found)")


# ── Main ──────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat warnings as errors (non-zero exit if any warnings)",
    )
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    # Walk all course directories
    for entry in sorted(_COURSES_DIR.iterdir()):
        if not entry.is_dir():
            continue
        if (entry / "course.yml").exists():
            course_dirs = [entry]
        else:
            course_dirs = [
                d for d in sorted(entry.iterdir())
                if d.is_dir() and (d / "course.yml").exists()
            ]

        for course_dir in course_dirs:
            course_data = _check_course_yml(course_dir / "course.yml", errors, warnings)
            textbook = course_data.get("textbook", "")

            for session_dir in sorted(
                d for d in course_dir.iterdir()
                if d.is_dir() and d.name.startswith("session-")
            ):
                session_yml = session_dir / "session.yml"
                if not session_yml.exists():
                    _warn(warnings, session_dir, "directory has no session.yml")
                    continue
                _check_session_yml(session_yml, textbook, errors, warnings)

    # Exercise format completeness
    _check_exercises(errors, warnings)

    # Report
    total_issues = len(errors) + len(warnings)
    if total_issues == 0:
        print(f"validate_courses: OK — {_count_sessions()} sessions, "
              f"{_count_exercises()} exercises checked")
        return 0

    for line in sorted(warnings):
        print(line)
    for line in sorted(errors):
        print(line)

    print()
    if errors:
        print(f"validate_courses: FAILED — {len(errors)} error(s), {len(warnings)} warning(s)")
    else:
        print(f"validate_courses: {len(warnings)} warning(s) (use --strict to fail on warnings)")

    if errors or (args.strict and warnings):
        return 1
    return 0


def _count_sessions() -> int:
    return sum(
        1
        for p in _COURSES_DIR.rglob("session.yml")
    )


def _count_exercises() -> int:
    return sum(
        1
        for p in _LESSONS_DIR.glob("*/*/exercises/*/")
        if p.is_dir()
    )


if __name__ == "__main__":
    sys.exit(main())
