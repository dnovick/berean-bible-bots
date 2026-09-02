#!/usr/bin/env python3
"""Validate exercise directory structure and content rules.

Each check is a registered function — add new checks to _CHECKS to extend.

Current checks:
  - three-format: every exercise directory has <name>.md, <name>.html, <name>.pdf
  - ans-row-no-inline-display: ans-row elements have no inline display style,
      answer buttons are not pre-labeled as open, inputs have no 'e.g.' placeholder,
      inputs with a small answer set do not use placeholder="A or B"
  - ans-row-no-colspan: ans-row <tr> elements must not contain colspan attributes
  - verse-ref-hebrew-same-node: verse references and Hebrew text must not share a
      short text node (RTL bidi reordering renders them in wrong order)
  - readme-chapter-number: README.md must mention the chapter number from the path

Exit 0 if clean (or warnings only without --strict), exit 1 on errors.

Usage:
    python scripts/validate_exercises.py
    python scripts/validate_exercises.py --strict
"""

from __future__ import annotations

import argparse
import re as _re
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

_ANS_ROW_INLINE_DISPLAY_RE = _re.compile(
    r'class=["\']ans-row["\'][^>]*style=["\'][^"\']*display\s*:', _re.IGNORECASE
)
_RBTN_PRE_OPEN_RE = _re.compile(r'class=["\']rbtn\s+on["\']', _re.IGNORECASE)
_PLACEHOLDER_EG_RE = _re.compile(r'placeholder=["\'][^"\']*e\.g\.', _re.IGNORECASE)
_PLACEHOLDER_OR_RE = _re.compile(
    r'<input\b[^>]*placeholder=["\'](?=[^"\']{1,25}["\'])[^"\']*\bor\b[^"\']*["\']',
    _re.IGNORECASE
)


@_register("ans-row-no-inline-display")
def check_ans_row_no_inline_display(
    ex_dir: Path, errors: list[str], warnings: list[str]
) -> None:
    """ans-row elements must not carry inline style="display:..." attributes,
    answer buttons must not be pre-labeled as open (class="rbtn on" / ▼ Hide),
    input placeholders must not use 'e.g.' (reveals the answer), and inputs
    must not use placeholder="A or B" (signals a small answer set — use select).
    colspan on ans-rows is checked separately by ans-row-no-colspan.
    """
    name = ex_dir.name
    html_file = ex_dir / f"{name}.html"
    if not html_file.exists():
        return
    text = html_file.read_text(encoding="utf-8", errors="replace")
    for lineno, line in enumerate(text.splitlines(), 1):
        if _ANS_ROW_INLINE_DISPLAY_RE.search(line):
            _err(
                errors, ex_dir,
                f"{html_file.name}:{lineno} — ans-row has inline display style"
                " (remove the style attribute; CSS handles visibility)"
            )
        if _RBTN_PRE_OPEN_RE.search(line):
            _err(
                errors, ex_dir,
                f"{html_file.name}:{lineno} — answer button pre-labeled as open"
                " (class=\"rbtn on\"); use class=\"rbtn\" and ▶ Answer on page load"
            )
        if _PLACEHOLDER_EG_RE.search(line):
            _err(
                errors, ex_dir,
                f"{html_file.name}:{lineno} — input has 'e.g.' placeholder"
                " (reveals the answer); use a generic label like 'division' or 'types'"
            )
        if _PLACEHOLDER_OR_RE.search(line):
            _err(
                errors, ex_dir,
                f"{html_file.name}:{lineno} — input placeholder enumerates choices with"
                " 'or' (e.g. 'QH or —'); fields with a small answer set must use"
                " <select> instead of <input>"
            )


_ANS_BLOCK_RE = _re.compile(
    r'<tr[^>]*class=["\'][^"\']*ans-row[^"\']*["\'][^>]*>.*?</tr>',
    _re.IGNORECASE | _re.DOTALL
)
_COLSPAN_RE = _re.compile(r'\bcolspan\b', _re.IGNORECASE)


@_register("ans-row-no-colspan")
def check_ans_row_no_colspan(
    ex_dir: Path, errors: list[str], warnings: list[str]
) -> None:
    """ans-row <tr> elements must not contain colspan attributes.
    Every <td> in an answer row must align cell-for-cell with the table headers.
    """
    name = ex_dir.name
    html_file = ex_dir / f"{name}.html"
    if not html_file.exists():
        return
    text = html_file.read_text(encoding="utf-8", errors="replace")
    reported: set[int] = set()
    for m in _ANS_BLOCK_RE.finditer(text):
        block = m.group(0)
        if _COLSPAN_RE.search(block):
            lineno = text[:m.start()].count('\n') + 1
            if lineno not in reported:
                reported.add(lineno)
                _err(
                    errors, ex_dir,
                    f"{html_file.name}:{lineno} — ans-row uses colspan;"
                    " every <td> must align cell-for-cell with column headers"
                    " (no colspan shortcuts)"
                )


_TEXT_NODE_RE = _re.compile(r'>([^<]+)<')
_HEBREW_CHARS_RE = _re.compile(r'[ְ-ת]')
_VERSE_REF_IN_NODE_RE = _re.compile(r'\b\d+:\d+')


@_register("verse-ref-hebrew-same-node")
def check_verse_ref_hebrew_same_node(
    ex_dir: Path, errors: list[str], warnings: list[str]
) -> None:
    """Short text nodes (<=80 chars) must not contain both Hebrew characters and
    a verse reference pattern (N:N). RTL bidi reordering renders them backwards.
    Put the reference on its own line or in a separate LTR element.
    """
    name = ex_dir.name
    html_file = ex_dir / f"{name}.html"
    if not html_file.exists():
        return
    text = html_file.read_text(encoding="utf-8", errors="replace")
    for lineno, line in enumerate(text.splitlines(), 1):
        if "<td" not in line.lower():
            continue
        for m in _TEXT_NODE_RE.finditer(line):
            node = m.group(1).strip()
            if (len(node) <= 80
                    and _HEBREW_CHARS_RE.search(node)
                    and _VERSE_REF_IN_NODE_RE.search(node)):
                _warn(
                    warnings, ex_dir,
                    f"{html_file.name}:{lineno} — verse reference and Hebrew text"
                    " in the same text node (RTL reordering renders it backwards);"
                    " put the reference on its own line or in a separate LTR element"
                )


_CH_DIR_RE = _re.compile(r'[\\/]ch(\d+)[\\/]exercises[\\/]')


@_register("readme-chapter-number")
def check_readme_chapter_number(
    ex_dir: Path, errors: list[str], warnings: list[str]
) -> None:
    """README.md must mention the chapter number matching the directory path."""
    readme = ex_dir / "README.md"
    if not readme.exists():
        return
    m = _CH_DIR_RE.search(str(ex_dir))
    if not m:
        return
    n = m.group(1)
    text = readme.read_text(encoding="utf-8", errors="replace").lower()
    if f"ch{n}" not in text and f"chapter {n}" not in text:
        _warn(
            warnings, ex_dir,
            f"README.md does not mention ch{n} — chapter number may be wrong"
        )


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
