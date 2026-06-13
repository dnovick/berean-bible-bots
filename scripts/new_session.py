#!/usr/bin/env python3
"""Scaffold a new session directory with a pre-filled session.yml.

Usage:
    python scripts/new_session.py <course-id> \\
        --date YYYY-MM-DD --focus "Session topic" \\
        [--session N] [--chapter N] [--instructor "Name"]

Arguments:
    course-id    Course identifier, e.g. bbh-2026.1 or bbh-2024.1.

Options:
    --date       Session date in YYYY-MM-DD format (required).
    --focus      Short description shown in the course session table (required).
    --session    Explicit session number. If omitted, uses the next number
                 after the highest existing session directory.
    --chapter    Textbook chapter number for this session (omit for
                 intro/review sessions with no primary chapter).
    --instructor Lead teacher name (omit to leave blank).

The script creates:
    data/courses/<group>/<course-id>/session-NN/session.yml

and prints the path of the created file.  It refuses to overwrite an
existing session directory.

Examples:
    # Next sequential session, no chapter:
    python scripts/new_session.py bbh-2026.1 \\
        --date 2026-09-17 --focus "Review — BBH Ch4–5"

    # Explicit session number with chapter and instructor:
    python scripts/new_session.py bbh-2026.1 \\
        --date 2026-10-01 --focus "Hebrew Nouns" --session 7 \\
        --chapter 4 --instructor "Preston Brown"
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
_COURSES_DIR = _REPO / "data" / "courses"

_SESSION_YML_TEMPLATE = """\
# Session schema
#
# date:     YYYY-MM-DD
# focus:    short description shown in the course session table
# chapter:  BBH chapter number (integer) — renders as a "Textbook Chapter" link
#           on the session page and is used in the course session table.
#           Omit for review/intro sessions with no primary chapter.
#
# agenda:   ordered list of session agenda items
#   - title:  item label (required)
#     url:    optional link (internal path or external URL)
#
# sections: freeform content blocks, each rendered as ## Heading + markdown body
#   - heading: section title
#     content: inline markdown text (use | for multi-line)
#     file:    .md filename in this session directory (e.g. "background.md")
#
# instructor: name of the lead teacher for this session (optional, omit if blank)
# recording:  URL to the session recording (optional, omit or leave blank if unavailable)
# notes:      plain-text instructor notes (not rendered on the page when blank)
#
# reading:  progressive reading exercise(s) for this session (rendered as ## Reading)
#   Each entry:
#   - name:        short label shown as the subsection heading and in the agenda (required)
#     description: goals or instructions for this reading activity (required)
#     passage:     Scripture reference displayed on the session page (required)
#     file:        HTML filename in this session directory (required)
#
# files:    downloadable resources attached to this session (rendered as ## Downloads)
#   - name: display label for the link (required)
#     file: filename in this session directory (e.g. "handout.pdf")

date: "{date}"
focus: "{focus}"{chapter_line}{instructor_line}

agenda:
sections:

notes: ""
"""


def _find_course_dir(course_id: str) -> Path:
    """Return the course directory for course_id, searching all group dirs."""
    for entry in sorted(_COURSES_DIR.iterdir()):
        if not entry.is_dir():
            continue
        # Direct course dir (ungrouped)
        if entry.name == course_id and (entry / "course.yml").exists():
            return entry
        # Group dir — search one level deeper
        candidate = entry / course_id
        if candidate.is_dir() and (candidate / "course.yml").exists():
            return candidate
    raise SystemExit(
        f"ERROR: course {course_id!r} not found under {_COURSES_DIR}.\n"
        f"Available courses: {_list_course_ids()}"
    )


def _list_course_ids() -> str:
    ids = []
    for entry in sorted(_COURSES_DIR.iterdir()):
        if not entry.is_dir():
            continue
        if (entry / "course.yml").exists():
            ids.append(entry.name)
        else:
            for sub in sorted(entry.iterdir()):
                if sub.is_dir() and (sub / "course.yml").exists():
                    ids.append(sub.name)
    return ", ".join(ids) if ids else "(none found)"


def _next_session_number(course_dir: Path) -> int:
    """Derive the next session number from existing session-NN directories."""
    nums = []
    for d in course_dir.iterdir():
        if d.is_dir() and d.name.startswith("session-"):
            try:
                nums.append(int(d.name.split("-", 1)[1]))
            except (IndexError, ValueError):
                pass
    return max(nums, default=0) + 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold a new session.yml in the given course.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("course_id", metavar="course-id",
                        help="Course ID, e.g. bbh-2026.1")
    parser.add_argument("--date", required=True,
                        help="Session date (YYYY-MM-DD)")
    parser.add_argument("--focus", required=True,
                        help="Short session description")
    parser.add_argument("--session", type=int, default=None,
                        help="Explicit session number (default: next sequential)")
    parser.add_argument("--chapter", type=int, default=None,
                        help="Textbook chapter number (omit for review/intro sessions)")
    parser.add_argument("--instructor", default=None,
                        help="Lead teacher name")
    args = parser.parse_args()

    # Validate date format
    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print(f"ERROR: --date must be YYYY-MM-DD, got {args.date!r}", file=sys.stderr)
        return 1

    course_dir = _find_course_dir(args.course_id)

    session_num = args.session if args.session is not None else _next_session_number(course_dir)
    session_dir_name = f"session-{session_num:02d}"
    session_dir = course_dir / session_dir_name

    if session_dir.exists():
        print(f"ERROR: {session_dir} already exists. "
              f"Use --session N to specify a different number.", file=sys.stderr)
        return 1

    chapter_line = f"\nchapter: {args.chapter}" if args.chapter is not None else ""
    instructor_line = f"\ninstructor: \"{args.instructor}\"" if args.instructor else ""

    content = _SESSION_YML_TEMPLATE.format(
        date=args.date,
        focus=args.focus,
        chapter_line=chapter_line,
        instructor_line=instructor_line,
    )

    session_dir.mkdir(parents=True)
    yml_path = session_dir / "session.yml"
    yml_path.write_text(content, encoding="utf-8")

    print(f"Created: {yml_path.relative_to(_REPO)}")
    print(f"  Course:  {args.course_id}  ({course_dir.relative_to(_REPO)})")
    print(f"  Session: {session_dir_name}  (number {session_num})")
    print(f"  Date:    {args.date}")
    print(f"  Focus:   {args.focus}")
    if args.chapter:
        print(f"  Chapter: {args.chapter}")
    if args.instructor:
        print(f"  Instructor: {args.instructor}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
