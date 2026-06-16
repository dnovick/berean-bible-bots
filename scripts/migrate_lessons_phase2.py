"""One-time migration script for lesson schema Phase 2.

Actions performed (idempotent — safe to re-run):

1. Delete stray directory data/lessons/bbh/README.md/ (a directory mistakenly
   named README.md).
2. Rename chapter README.md → lesson.md in every chapter dir (has chapter.yml).
3. For each exercise subdirectory, extract name + description from README.md,
   write exercise.yml, then delete README.md.
4. Delete chapter-level exercises/README.md listing files.
5. Append flashcards: and exercises: fields to each chapter.yml.

Run with:
    .venv/bin/python3 scripts/migrate_lessons_phase2.py
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Any

import yaml

_REPO = Path(__file__).resolve().parent.parent
_LESSONS = _REPO / "data" / "lessons"
_COURSES = ("bbh", "bbg", "bba")


# ── Text-extraction helpers ───────────────────────────────────────────────────


def _extract_name(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def _extract_description(text: str) -> str:
    text = re.sub(r"^# [^\n]+\n+", "", text.lstrip())          # remove H1
    text = re.sub(                                                # remove bold metadata
        r"^\*\*[^*]+\*\*[^\n]*\n", "", text, flags=re.MULTILINE
    )
    text = text.lstrip()
    m = re.search(r"^## Description[^\n]*\n", text, re.MULTILINE | re.IGNORECASE)
    if m:
        text = text[m.end():]
    end_m = re.search(r"^#{2,3} ", text, re.MULTILINE)
    if end_m:
        text = text[: end_m.start()]
    return text.strip()


# ── Flashcard slug discovery ──────────────────────────────────────────────────


def _discover_flashcard_slugs(ch_dir: Path, ch_num: int) -> list[str]:
    """Return sorted list of deck-type slugs from ch<N>-<slug>-deck.md files."""
    slugs: list[str] = []
    prefix = f"ch{ch_num}-"
    for f in ch_dir.glob("*-deck.md"):
        name = f.stem          # e.g. ch14-morphology-deck
        if not name.startswith(prefix):
            continue
        without_prefix = name[len(prefix):]   # morphology-deck
        if without_prefix.endswith("-deck"):
            slug = without_prefix[: -len("-deck")]   # morphology
            slugs.append(slug)
    return sorted(slugs)


# ── Chapter.yml appender ──────────────────────────────────────────────────────


def _yaml_list(items: list[str]) -> str:
    """Return inline YAML for a string list ([] or block)."""
    if not items:
        return "[]"
    return "\n" + "".join(f"  - {item}\n" for item in items)


def _append_chapter_yml(
    ch_yml: Path,
    flashcard_slugs: list[str],
    exercise_names: list[str],
) -> bool:
    """Append flashcards: and exercises: to chapter.yml if not already present.

    Returns True if the file was modified.
    """
    text = ch_yml.read_text(encoding="utf-8")
    if "flashcards:" in text and "exercises:" in text:
        return False   # already migrated

    additions: list[str] = []
    if "flashcards:" not in text:
        additions.append(f"flashcards: {_yaml_list(flashcard_slugs)}")
    if "exercises:" not in text:
        additions.append(f"exercises: {_yaml_list(exercise_names)}")

    if not additions:
        return False

    append_text = "\n" + "\n".join(additions)
    if not text.endswith("\n"):
        append_text = "\n" + append_text
    ch_yml.write_text(text + append_text, encoding="utf-8")
    return True


# ── Per-chapter migration ─────────────────────────────────────────────────────


def migrate_chapter(ch_dir: Path) -> dict[str, Any]:
    """Migrate a single chapter directory. Returns a stats dict."""
    stats: dict[str, Any] = {
        "readme_renamed": False,
        "exercises_yml_created": 0,
        "exercises_readme_deleted": 0,
        "chapter_yml_updated": False,
        "anomalies": [],
    }

    ch_yml = ch_dir / "chapter.yml"
    if not ch_yml.exists():
        return stats  # not a chapter dir

    # Parse chapter number from chapter.yml
    raw = yaml.safe_load(ch_yml.read_text(encoding="utf-8")) or {}
    ch_num: int = int(raw.get("chapter", 0))

    # ── 2. Rename README.md → lesson.md ──────────────────────────────────────
    readme = ch_dir / "README.md"
    lesson = ch_dir / "lesson.md"
    if readme.exists() and not lesson.exists():
        readme.rename(lesson)
        stats["readme_renamed"] = True
    elif lesson.exists() and not readme.exists():
        pass  # already migrated
    elif readme.exists() and lesson.exists():
        stats["anomalies"].append("Both README.md and lesson.md exist — README.md left in place")

    # ── 3. Exercise subdirectories ────────────────────────────────────────────
    exercises_dir = ch_dir / "exercises"
    exercise_names: list[str] = []

    if exercises_dir.is_dir():
        # Delete chapter-level exercises/README.md (the listing file)
        ex_listing = exercises_dir / "README.md"
        if ex_listing.exists():
            ex_listing.unlink()
            stats["exercises_readme_deleted"] += 1

        for ex_subdir in sorted(d for d in exercises_dir.iterdir() if d.is_dir()):
            exercise_names.append(ex_subdir.name)
            ex_readme = ex_subdir / "README.md"
            ex_yml = ex_subdir / "exercise.yml"

            if not ex_yml.exists():
                if ex_readme.exists():
                    text = ex_readme.read_text(encoding="utf-8")
                    name = _extract_name(text)
                    description = _extract_description(text)
                    data = {"name": name, "description": description}
                    ex_yml.write_text(
                        yaml.dump(
                            data,
                            allow_unicode=True,
                            sort_keys=False,
                            default_flow_style=False,
                            width=80,
                        ),
                        encoding="utf-8",
                    )
                    ex_readme.unlink()
                    stats["exercises_yml_created"] += 1
                else:
                    stats["anomalies"].append(
                        f"Exercise {ex_subdir.name}: no README.md and no exercise.yml"
                    )
            else:
                # exercise.yml already exists — delete README.md if still present
                if ex_readme.exists():
                    ex_readme.unlink()

            # Warn if no HTML file
            html_files = list(ex_subdir.glob("*.html"))
            if not html_files:
                stats["anomalies"].append(
                    f"Exercise {ex_subdir.name}: no HTML file found"
                )

    # ── 5. Append to chapter.yml ──────────────────────────────────────────────
    flashcard_slugs = _discover_flashcard_slugs(ch_dir, ch_num)
    modified = _append_chapter_yml(ch_yml, flashcard_slugs, exercise_names)
    stats["chapter_yml_updated"] = modified

    return stats


# ── Main ──────────────────────────────────────────────────────────────────────


def main() -> None:
    totals: dict[str, int] = {
        "readme_renamed": 0,
        "exercises_yml_created": 0,
        "exercises_readme_deleted": 0,
        "chapter_yml_updated": 0,
        "chapters_processed": 0,
    }
    all_anomalies: list[str] = []

    # ── 1. Delete stray directory data/lessons/bbh/README.md/ ─────────────────
    stray = _LESSONS / "bbh" / "README.md"
    if stray.is_dir():
        shutil.rmtree(stray)
        print(f"  Deleted stray directory: {stray}")
    else:
        print(f"  Stray directory not found (already clean): {stray}")

    for course in _COURSES:
        course_dir = _LESSONS / course
        if not course_dir.is_dir():
            continue
        for ch_dir in sorted(course_dir.iterdir()):
            if not ch_dir.is_dir():
                continue
            if ch_dir.name == "additional-resources":
                continue
            if not (ch_dir / "chapter.yml").exists():
                continue

            stats = migrate_chapter(ch_dir)
            totals["chapters_processed"] += 1
            totals["readme_renamed"] += int(stats["readme_renamed"])
            totals["exercises_yml_created"] += stats["exercises_yml_created"]
            totals["exercises_readme_deleted"] += stats["exercises_readme_deleted"]
            totals["chapter_yml_updated"] += int(stats["chapter_yml_updated"])

            if stats["anomalies"]:
                for a in stats["anomalies"]:
                    all_anomalies.append(f"  [{course}/{ch_dir.name}] {a}")

    print("\nMigration complete.")
    print(f"  Chapters processed:          {totals['chapters_processed']}")
    print(f"  README.md → lesson.md:       {totals['readme_renamed']}")
    print(f"  exercise.yml created:        {totals['exercises_yml_created']}")
    print(f"  exercises/README.md deleted: {totals['exercises_readme_deleted']}")
    print(f"  chapter.yml updated:         {totals['chapter_yml_updated']}")

    if all_anomalies:
        print(f"\nAnomalies ({len(all_anomalies)}):")
        for a in all_anomalies:
            print(a)
    else:
        print("\nNo anomalies detected.")


if __name__ == "__main__":
    main()
