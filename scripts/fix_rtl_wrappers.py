#!/usr/bin/env python3
"""Fix hebrew-no-rtl-wrapper warnings in exercise HTML files.

For each text node containing Hebrew characters that has no RTL-styled ancestor,
splits the text into Hebrew and non-Hebrew runs and wraps each Hebrew run in:
  <span style="direction:rtl;unicode-bidi:embed;">…</span>

Safe to re-run — files with no unprotected Hebrew are unchanged.

Usage:
    python scripts/fix_rtl_wrappers.py [chapter_dir ...]

    # Fix ch27 and ch29 (default):
    python scripts/fix_rtl_wrappers.py

    # Fix specific chapters:
    python scripts/fix_rtl_wrappers.py data/lessons/bbh/ch25 data/lessons/bbh/ch27
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, Comment, NavigableString

_REPO = Path(__file__).resolve().parent.parent
_LESSONS_DIR = _REPO / "data" / "lessons"

_DEFAULT_CHAPTERS = [
    _LESSONS_DIR / "bbh" / "ch27",
    _LESSONS_DIR / "bbh" / "ch29",
]

# Hebrew Unicode block: U+0590–U+05FF (includes vowel points, cantillation, letters)
_HEBREW_CHAR_RE = re.compile(r"[֐-׿]")
# Splits text into alternating non-Hebrew / Hebrew runs
_HEBREW_RUN_RE = re.compile(r"([֐-׿]+)")

_RTL_STYLE_RE = re.compile(r"direction\s*:\s*rtl", re.IGNORECASE)
_CSS_RULE_RE = re.compile(r"([^{}]+)\{([^{}]*)\}")
_CSS_CLASS_RE = re.compile(r"\.([\w-]+)")
_SKIP_TAGS = {"script", "style"}

RTL_STYLE = "direction:rtl;unicode-bidi:embed;"


def _build_rtl_classes(soup: BeautifulSoup) -> set[str]:
    classes: set[str] = set()
    for style_tag in soup.find_all("style"):
        for selector, body in _CSS_RULE_RE.findall(style_tag.get_text()):
            if _RTL_STYLE_RE.search(body):
                classes.update(_CSS_CLASS_RE.findall(selector))
    return classes


def _has_rtl_ancestor(el: object, rtl_classes: set[str]) -> bool:
    node = el
    while node is not None and getattr(node, "name", None) is not None:
        style = node.get("style", "") or ""  # type: ignore[attr-defined]
        if _RTL_STYLE_RE.search(style):
            return True
        classes = node.get("class", []) or []  # type: ignore[attr-defined]
        if isinstance(classes, str):
            classes = [classes]
        if rtl_classes.intersection(classes):
            return True
        node = node.parent  # type: ignore[attr-defined]
    return False


def _fix_html_file(html_path: Path) -> bool:
    """Wrap bare Hebrew runs in RTL spans. Returns True if the file was changed."""
    original = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(original, "html.parser")

    rtl_classes = _build_rtl_classes(soup)

    changed = False
    # Collect text nodes to fix (don't modify while iterating)
    to_fix: list[NavigableString] = []
    for text_node in soup.find_all(string=_HEBREW_CHAR_RE):
        if not isinstance(text_node, NavigableString):
            continue
        if isinstance(text_node, Comment):
            continue
        parent = text_node.parent
        if parent is None:
            continue
        if any(a.name in _SKIP_TAGS for a in parent.parents if getattr(a, "name", None)):
            continue
        if getattr(parent, "name", None) in _SKIP_TAGS:
            continue
        if not _has_rtl_ancestor(parent, rtl_classes):
            to_fix.append(text_node)

    for text_node in to_fix:
        text = str(text_node)
        parts = _HEBREW_RUN_RE.split(text)
        if len(parts) <= 1:
            continue  # no Hebrew found (shouldn't happen, but guard)

        # insert_before(text_node) accumulates nodes in insertion order before
        # text_node, so iterate parts in forward order to preserve original order.
        for part in parts:
            if not part:
                continue
            if _HEBREW_CHAR_RE.search(part):
                span = soup.new_tag("span", style=RTL_STYLE)
                span.string = part
                text_node.insert_before(span)
            else:
                text_node.insert_before(NavigableString(part))
        text_node.extract()
        changed = True

    if not changed:
        return False

    html_path.write_text(str(soup), encoding="utf-8")
    return True


def _chapter_html_files(chapter_dir: Path) -> list[Path]:
    exercises_dir = chapter_dir / "exercises"
    if not exercises_dir.is_dir():
        return []
    files = []
    for ex_dir in sorted(exercises_dir.iterdir()):
        if not ex_dir.is_dir():
            continue
        html = ex_dir / f"{ex_dir.name}.html"
        if html.exists():
            files.append(html)
    return files


def main() -> int:
    if len(sys.argv) > 1:
        chapters = [Path(a).resolve() for a in sys.argv[1:]]
    else:
        chapters = _DEFAULT_CHAPTERS

    total_fixed = 0
    for chapter in chapters:
        if not chapter.is_dir():
            print(f"  SKIP (not found): {chapter}")
            continue
        for html_path in _chapter_html_files(chapter):
            if _fix_html_file(html_path):
                print(f"  Fixed: {html_path.relative_to(_REPO)}")
                total_fixed += 1

    print(f"\nFixed {total_fixed} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
