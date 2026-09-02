#!/usr/bin/env python3
"""Validate lesson content structure for BBH, BBG, and BBA.

Checks:
  - chapter.yml has required fields (chapter, course, title, focus)
  - lesson.md is present in every chapter directory
  - Every slug in flashcards: resolves to all three deck files
    (ch<N>-<slug>-deck.md, ch<N>-<slug>-deck.txt, ch<N>-<slug>-deck-fd.txt)
  - Flashcard directories with real deck content not listed in flashcards:
    are flagged as undeclared (build_lessons.py silently skips them —
    this is how the ch34/ch35 morphology decks went unbuilt)
  - Every name in exercises: has a corresponding directory
  - Every exercise directory has exercise.yml with name and description
  - Every exercise directory has all three formats (.md, .html, .pdf)
  - Exercise directories not listed in exercises: are flagged as undeclared

Exit 0 if clean, exit 1 if any errors.  Warnings are printed but do not
cause a non-zero exit.

Usage:
    python scripts/validate_lessons.py
    python scripts/validate_lessons.py --strict   # warnings also count as errors
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

_REPO = Path(__file__).resolve().parent.parent
_LESSONS = _REPO / "data" / "lessons"


# ── Helpers ───────────────────────────────────────────────────────────────────


def _err(errors: list[str], path: Path, msg: str) -> None:
    errors.append(f"ERROR  {path.relative_to(_REPO)}  —  {msg}")


def _warn(warnings: list[str], path: Path, msg: str) -> None:
    warnings.append(f"WARN   {path.relative_to(_REPO)}  —  {msg}")


# ── Exercise-level checks ─────────────────────────────────────────────────────


def _check_exercise(
    ex_dir: Path,
    errors: list[str],
    warnings: list[str],
) -> None:
    ex_yml_path = ex_dir / "exercise.yml"
    if not ex_yml_path.exists():
        _err(errors, ex_dir, "missing exercise.yml")
    else:
        try:
            with open(ex_yml_path, encoding="utf-8") as f:
                ex_data: dict[str, Any] = yaml.safe_load(f) or {}
        except Exception as exc:
            _err(errors, ex_yml_path, f"YAML parse error: {exc}")
            ex_data = {}

        for field in ("name", "description"):
            if not ex_data.get(field):
                _err(errors, ex_yml_path, f"missing required field: {field!r}")

    if not any(ex_dir.glob("*.html")):
        _err(errors, ex_dir, "missing .html exercise file")
    if not any(ex_dir.glob("*.pdf")):
        _err(errors, ex_dir, "missing .pdf exercise file")
    if not any(ex_dir.glob("*.md")):
        _err(errors, ex_dir, "missing .md exercise file")


# ── Chapter-level checks ──────────────────────────────────────────────────────


def _check_chapter(
    ch_dir: Path,
    errors: list[str],
    warnings: list[str],
) -> None:
    ch_yml_path = ch_dir / "chapter.yml"

    try:
        with open(ch_yml_path, encoding="utf-8") as f:
            data: dict[str, Any] = yaml.safe_load(f) or {}
    except Exception as exc:
        _err(errors, ch_yml_path, f"YAML parse error: {exc}")
        return

    for field in ("chapter", "course", "title", "focus"):
        if not data.get(field):
            _err(errors, ch_yml_path, f"missing required field: {field!r}")

    # lesson.md must exist
    if not (ch_dir / "lesson.md").exists():
        _err(errors, ch_dir, "missing lesson.md")

    ch_num = str(data.get("chapter", ""))

    # ── Flashcards ────────────────────────────────────────────────────────────
    # flashcards: [] (explicit empty list) = intentionally no decks — no warning.
    # Missing flashcards: key = possibly forgotten — warn.
    if "flashcards" not in data:
        _warn(warnings, ch_yml_path, "flashcards: field missing from chapter.yml")
    flashcard_slugs: list[str] = data.get("flashcards") or []
    if flashcard_slugs:
        flashcards_dir = ch_dir / "flashcards"
        for slug in flashcard_slugs:
            slug_dir = flashcards_dir / slug
            stem = f"ch{ch_num}-{slug}-deck"

            if not slug_dir.is_dir():
                _err(errors, ch_yml_path,
                     f"flashcard slug {slug!r}: directory flashcards/{slug}/ not found")
                continue

            if not (slug_dir / "deck.yml").exists():
                _err(errors, slug_dir, "missing deck.yml")

            for filename in (f"{stem}.md", f"{stem}.txt", f"{stem}-fd.txt"):
                if not (slug_dir / filename).exists():
                    _err(errors, ch_yml_path,
                         f"flashcard slug {slug!r}: missing {filename}")

    # Undeclared flashcard directories: a deck.yml + ch<N>-<slug>-deck.md
    # sitting in flashcards/<slug>/ but never listed in flashcards: is silently
    # skipped by build_lessons.py (declared-slugs mode ignores auto-discovery)
    # — this is exactly how the ch34/ch35 morphology decks went unbuilt.
    flashcards_dir = ch_dir / "flashcards"
    if flashcards_dir.is_dir():
        declared_slugs: set[str] = set(flashcard_slugs)
        for slug_dir in sorted(d for d in flashcards_dir.iterdir() if d.is_dir()):
            slug = slug_dir.name
            if slug in declared_slugs:
                continue
            stem = f"ch{ch_num}-{slug}-deck"
            if (slug_dir / f"{stem}.md").exists():
                _warn(warnings, ch_yml_path,
                      f"flashcard directory {slug!r} exists with deck content but is"
                      " not listed in flashcards: — it will not appear on the built site")

    # ── Exercises ─────────────────────────────────────────────────────────────
    exercises_dir = ch_dir / "exercises"
    # exercises: [] (explicit empty list) = intentionally no exercises — no warning.
    # Missing exercises: key = possibly forgotten — warn.
    if "exercises" not in data:
        _warn(warnings, ch_yml_path, "exercises: field missing from chapter.yml")
    exercise_list: list[str] = data.get("exercises") or []
    declared: set[str] = set(exercise_list)

    # Declared exercises must exist and be valid
    for ex_name in exercise_list:
        ex_dir = exercises_dir / ex_name
        if not ex_dir.is_dir():
            _err(errors, ch_yml_path,
                 f"exercise {ex_name!r}: directory not found")
            continue
        _check_exercise(ex_dir, errors, warnings)

    # Undeclared exercise directories: warn and still validate their formats
    if exercises_dir.is_dir():
        for ex_dir in sorted(d for d in exercises_dir.iterdir() if d.is_dir()):
            if ex_dir.name not in declared:
                _warn(warnings, ch_yml_path,
                      f"exercise directory {ex_dir.name!r} exists but is not listed in exercises:")
                _check_exercise(ex_dir, errors, warnings)


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
    chapter_count = 0
    exercise_count = 0

    for course_dir in sorted(_LESSONS.iterdir()):
        if not course_dir.is_dir():
            continue
        for ch_dir in sorted(course_dir.iterdir()):
            if not ch_dir.is_dir() or not (ch_dir / "chapter.yml").exists():
                continue
            _check_chapter(ch_dir, errors, warnings)
            chapter_count += 1
            ex_root = ch_dir / "exercises"
            if ex_root.is_dir():
                exercise_count += sum(1 for d in ex_root.iterdir() if d.is_dir())

    total_issues = len(errors) + len(warnings)
    if total_issues == 0:
        print(
            f"validate_lessons: OK — "
            f"{chapter_count} chapters, {exercise_count} exercises checked"
        )
        return 0

    for line in sorted(warnings):
        print(line)
    for line in sorted(errors):
        print(line)

    print()
    if errors:
        print(
            f"validate_lessons: FAILED — "
            f"{len(errors)} error(s), {len(warnings)} warning(s)"
        )
    else:
        print(
            f"validate_lessons: {len(warnings)} warning(s) "
            f"(use --strict to fail on warnings)"
        )

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
