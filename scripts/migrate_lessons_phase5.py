#!/usr/bin/env python3
"""One-time migration: Phase 5 of issue #319.

Moves flashcard deck files from the chapter root into flashcards/<slug>/
subdirectories and creates deck.yml in each, mirroring the exercises/<name>/
+ exercise.yml pattern.

chapter.yml flashcards: slug lists are unchanged — only the file locations move.
"""

import re
import shutil
from pathlib import Path

import yaml

_LESSONS = Path(__file__).parent.parent / "data" / "lessons"
_COURSES = ["bbh", "bbg", "bba"]


def _extract_deck_name(deck_md: Path) -> str:
    for line in deck_md.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return deck_md.stem.replace("-", " ").title()


def _extract_deck_description(deck_md: Path) -> str:
    for line in deck_md.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\*(.+)\*$", line.strip())
        if m:
            return m.group(1).strip()
    return ""


def migrate_chapter(ch_dir: Path) -> int:
    ch_num = ch_dir.name[2:]
    prefix = f"ch{ch_num}-"
    suffix = "-deck.md"

    slugs = [
        f.name[len(prefix):-len(suffix)]
        for f in sorted(ch_dir.iterdir())
        if f.is_file() and f.name.startswith(prefix) and f.name.endswith(suffix)
    ]

    if not slugs:
        return 0

    flashcards_dir = ch_dir / "flashcards"
    flashcards_dir.mkdir(exist_ok=True)

    for slug in slugs:
        slug_dir = flashcards_dir / slug
        slug_dir.mkdir(exist_ok=True)

        stem = f"ch{ch_num}-{slug}-deck"
        deck_md = ch_dir / f"{stem}.md"
        deck_txt = ch_dir / f"{stem}.txt"
        deck_fd = ch_dir / f"{stem}-fd.txt"

        # Create deck.yml before moving the .md (we still need to read it)
        deck_yml_path = slug_dir / "deck.yml"
        if not deck_yml_path.exists():
            name = _extract_deck_name(deck_md) if deck_md.exists() else slug.replace("-", " ").title()
            desc = _extract_deck_description(deck_md) if deck_md.exists() else ""
            content = yaml.dump(
                {"name": name, "description": desc},
                allow_unicode=True,
                sort_keys=False,
                default_flow_style=False,
                width=80,
            )
            deck_yml_path.write_text(content, encoding="utf-8")

        for src in (deck_md, deck_txt, deck_fd):
            if src.exists():
                shutil.move(str(src), slug_dir / src.name)

    return len(slugs)


def main() -> None:
    total_decks = 0
    total_chapters = 0

    for course in _COURSES:
        course_dir = _LESSONS / course
        if not course_dir.is_dir():
            continue
        for ch_dir in sorted(course_dir.iterdir()):
            if not ch_dir.is_dir() or not (ch_dir / "chapter.yml").exists():
                continue
            moved = migrate_chapter(ch_dir)
            if moved:
                total_chapters += 1
                total_decks += moved

    print(f"Migrated {total_decks} decks across {total_chapters} chapters.")


if __name__ == "__main__":
    main()
