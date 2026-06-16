#!/usr/bin/env python3
"""Validate course and lesson content structure.

Checks:
  - instance.yml has required fields (id, name, textbook)
  - course.yml (group-level), if present, has required field: name
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

File scope levels (used in session.yml file: entries):
    session  (default) — file lives in the session directory
    instance           — file lives in <instance>/common/  (e.g. bbh-2024.1/common/)
    course             — file lives in <group>/common/     (e.g. bbh/common/)
    global             — file lives in data/courses/common/
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
_GLOBAL_COMMON_DIR = _COURSES_DIR / "common"

# Maximum valid chapter number per textbook (short name → max chapter)
_CHAPTER_MAX: dict[str, int] = {
    "Basics of Biblical Hebrew": 35,
    "Basics of Biblical Greek": 36,
    "Basics of Biblical Aramaic": 22,
}

# ── Helpers ───────────────────────────────────────────────────────────────────


def _resolve_file(ref: str, scope: str, session_dir: Path, instance_dir: Path) -> Path:
    """Return the expected filesystem path for a file: reference given its scope.

    scope: session  (default) → session_dir / ref
    scope: instance           → instance_dir / "common" / ref
    scope: course             → instance_dir.parent / "common" / ref
    scope: global             → data/courses/common/ / ref
    """
    if scope == "instance":
        return instance_dir / "common" / ref
    if scope == "course":
        return instance_dir.parent / "common" / ref
    if scope == "global":
        return _GLOBAL_COMMON_DIR / ref
    return session_dir / ref


def _err(errors: list[str], path: Path, msg: str) -> None:
    errors.append(f"ERROR  {path.relative_to(_REPO)}  —  {msg}")


def _warn(warnings: list[str], path: Path, msg: str) -> None:
    warnings.append(f"WARN   {path.relative_to(_REPO)}  —  {msg}")


# ── Group-level checks ────────────────────────────────────────────────────────


def _check_course_yml(
    group_yml: Path,
    errors: list[str],
    warnings: list[str],
) -> dict:
    try:
        with open(group_yml) as f:
            data = yaml.safe_load(f) or {}
    except Exception as exc:
        _err(errors, group_yml, f"YAML parse error: {exc}")
        return {}

    if not data.get("name"):
        _err(errors, group_yml, "missing required field: 'name'")

    group_dir = group_yml.parent
    for res in data.get("resources") or []:
        if not isinstance(res, dict):
            continue
        ref = res.get("file") or ""
        scope = res.get("scope", "course")
        if not ref:
            continue
        resolved = _GLOBAL_COMMON_DIR / ref if scope == "global" else group_dir / "common" / ref
        if not resolved.exists():
            _err(errors, group_yml, f"resource file not found: {ref!r} (scope: {scope!r})")

    return data


# ── Instance-level checks ─────────────────────────────────────────────────────


def _check_instance_yml(
    instance_yml: Path,
    errors: list[str],
    warnings: list[str],
) -> dict:
    try:
        with open(instance_yml) as f:
            data = yaml.safe_load(f) or {}
    except Exception as exc:
        _err(errors, instance_yml, f"YAML parse error: {exc}")
        return {}

    for field in ("id", "name", "textbook"):
        if not data.get(field):
            _err(errors, instance_yml, f"missing required field: {field!r}")

    instance_dir = instance_yml.parent
    for res in data.get("resources") or []:
        if not isinstance(res, dict):
            continue
        ref = res.get("file") or ""
        scope = res.get("scope", "instance")
        if not ref:
            continue
        if scope == "instance":
            resolved = instance_dir / "common" / ref
        elif scope == "course":
            resolved = instance_dir.parent / "common" / ref
        elif scope == "global":
            resolved = _GLOBAL_COMMON_DIR / ref
        else:
            _err(errors, instance_yml, f"unknown scope {scope!r} for resource {ref!r}")
            continue
        if not resolved.exists():
            _err(errors, instance_yml, f"resource file not found: {ref!r} (scope: {scope!r})")

    return data


# ── Session-level checks ──────────────────────────────────────────────────────


def _check_session_yml(
    session_yml: Path,
    textbook: str,
    instance_dir: Path,
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

    # Lesson entry
    lesson = data.get("lesson") or {}
    if lesson:
        if not isinstance(lesson, dict):
            _err(errors, session_yml, "lesson must be a mapping with 'name' and 'url'")
        else:
            for field in ("name", "url"):
                if not lesson.get(field):
                    _err(errors, session_yml, f"lesson missing required field: {field!r}")

    # Reading entries
    readings_raw = data.get("reading") or []
    readings = [readings_raw] if isinstance(readings_raw, dict) else list(readings_raw)
    for reading in readings:
        if not isinstance(reading, dict):
            continue
        for field in ("name", "description", "passage"):
            if not reading.get(field):
                _err(errors, session_yml, f"reading entry missing required field: {field!r}")
        ref = reading.get("file")
        scope = reading.get("scope", "session")
        if not ref:
            _err(errors, session_yml, "reading entry missing required field: 'file'")
        elif not _resolve_file(ref, scope, session_dir, instance_dir).exists():
            _err(errors, session_yml, f"reading file not found: {ref!r} (scope: {scope!r})")

    # File references in sections — warn (file may be planned but not yet written)
    for section in data.get("sections") or []:
        if not isinstance(section, dict):
            continue
        ref = section.get("file")
        scope = section.get("scope", "session")
        if ref and not ref.startswith("http") and not _resolve_file(ref, scope, session_dir, instance_dir).exists():
            _warn(warnings, session_yml, f"sections file not found: {ref!r} (scope: {scope!r})")

    # File references in subpages — warn (file may be planned but not yet written)
    for sp in data.get("subpages") or []:
        if not isinstance(sp, dict):
            continue
        ref = sp.get("file")
        scope = sp.get("scope", "session")
        if ref and not _resolve_file(ref, scope, session_dir, instance_dir).exists():
            _warn(warnings, session_yml, f"subpages file not found: {ref!r} (scope: {scope!r})")

    # File references in downloads — error (committed downloads must exist)
    for dl in data.get("files") or []:
        if not isinstance(dl, dict):
            continue
        ref = dl.get("file")
        scope = dl.get("scope", "session")
        if ref and not _resolve_file(ref, scope, session_dir, instance_dir).exists():
            _err(errors, session_yml, f"files download not found: {ref!r} (scope: {scope!r})")


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

        if (entry / "instance.yml").exists():
            # Ungrouped legacy instance directly under data/courses/
            instance_dirs = [entry]
        else:
            # Group directory — validate group.yml if present, then scan instances
            group_yml = entry / "course.yml"
            if group_yml.exists():
                _check_course_yml(group_yml, errors, warnings)

            instance_dirs = [
                d for d in sorted(entry.iterdir())
                if d.is_dir() and (d / "instance.yml").exists()
            ]

        for instance_dir in instance_dirs:
            instance_data = _check_instance_yml(instance_dir / "instance.yml", errors, warnings)
            textbook = instance_data.get("textbook", "")

            for session_dir in sorted(
                d for d in instance_dir.iterdir()
                if d.is_dir() and d.name.startswith("session-")
            ):
                session_yml = session_dir / "session.yml"
                if not session_yml.exists():
                    _warn(warnings, session_dir, "directory has no session.yml")
                    continue
                _check_session_yml(session_yml, textbook, instance_dir, errors, warnings)

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
