#!/usr/bin/env python3
"""
Generate MkDocs course pages from data/courses/.

Usage
-----
    python scripts/build_courses.py

Directory layout
----------------
    data/courses/<id>/
        course.yml          # course metadata only (name, textbook, instructors, …)
        session-01/
            session.yml     # date, focus, chapter, agenda, sections, notes
            <content>.md    # optional freeform .md files referenced by sections
        session-02/
            session.yml
        …

Running this script regenerates all pages under mkdocs_src/courses/ and
updates the Courses block in mkdocs_nav.yml.
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[1]
_COURSES_DATA_DIR = _REPO_ROOT / "data" / "courses"
_COURSES_SITE_DIR = _REPO_ROOT / "mkdocs_src" / "courses"
_NAV_PATH = _REPO_ROOT / "mkdocs_nav.yml"

_NAV_START = "# <COURSES>"
_NAV_END = "# </COURSES>"

# ── Textbook metadata ─────────────────────────────────────────────────────────

_BBH_CHAPTERS: dict[int, str] = {
    1: "Hebrew Alphabet",
    2: "Hebrew Vowels",
    3: "Syllabification and Pronunciation",
    4: "Hebrew Nouns",
    5: "Definite Article and Conjunction Vav",
    6: "Hebrew Prepositions",
    7: "Hebrew Adjectives",
    8: "Hebrew Pronouns",
    9: "Hebrew Pronominal Suffixes",
    10: "Hebrew Construct Chain",
    11: "Hebrew Numbers",
    12: "Introduction to Hebrew Verbs",
    13: "Qal Perfect Strong Verbs",
    14: "Qal Perfect Weak Verbs",
    15: "Qal Imperfect Strong Verbs",
    16: "Qal Imperfect Weak Verbs",
    17: "Waw-Consecutive",
    18: "Qal Imperative",
    19: "Qal Pronominal Suffixes on Verbs",
    20: "Qal Infinitive Construct",
    21: "Qal Infinitive Absolute",
    22: "Qal Participle",
    23: "Sentence Syntax",
    24: "Niphal Strong",
    25: "Niphal Weak",
    26: "Hiphil Strong",
    27: "Hiphil Weak",
    28: "Hophal Strong",
    29: "Hophal Weak",
    30: "Piel Strong",
    31: "Piel Weak",
    32: "Pual Strong",
    33: "Pual Weak",
    34: "Hithpael Strong",
    35: "Hithpael Weak",
}

_TEXTBOOK_META: dict[str, dict[str, Any]] = {
    "Basics of Biblical Hebrew": {
        "short": "BBH",
        "url_prefix": "lessons/hebrew/",
        "chapters": _BBH_CHAPTERS,
    },
    "Basics of Biblical Greek": {
        "short": "BBG",
        "url_prefix": "lessons/greek/",
        "chapters": {},
    },
    "Basics of Biblical Aramaic": {
        "short": "BBA",
        "url_prefix": "lessons/aramaic/",
        "chapters": {},
    },
}


# ── Data loading ──────────────────────────────────────────────────────────────

def load_course(course_dir: Path) -> dict[str, Any]:
    """Load a course from course.yml + session-NN/session.yml subdirectories."""
    with open(course_dir / "course.yml") as f:
        data: dict[str, Any] = yaml.safe_load(f)
    data.setdefault("instructors", [])
    data.setdefault("description", "")
    data.setdefault("edition", "")

    sessions: list[dict[str, Any]] = []
    for session_dir in sorted(
        d for d in course_dir.iterdir()
        if d.is_dir() and d.name.startswith("session-")
    ):
        yml = session_dir / "session.yml"
        if not yml.exists():
            continue
        with open(yml) as f:
            session: dict[str, Any] = yaml.safe_load(f) or {}
        # Derive number from directory name: session-01 → 1
        try:
            session["number"] = int(session_dir.name.split("-", 1)[1])
        except (IndexError, ValueError):
            session["number"] = len(sessions) + 1
        session["_dir"] = session_dir.name
        sessions.append(session)

    data["sessions"] = sessions
    return data


def load_all_courses() -> list[dict[str, Any]]:
    """Load all courses from data/courses/, sorted by id."""
    courses = []
    for course_dir in sorted(_COURSES_DATA_DIR.iterdir()):
        if course_dir.is_dir() and (course_dir / "course.yml").exists():
            courses.append(load_course(course_dir))
    return courses


# ── Formatting helpers ────────────────────────────────────────────────────────

def format_date(date_val: Any) -> str:
    """Format a date value as 'Mon D, YYYY'. Returns '' if blank."""
    if not date_val:
        return ""
    if hasattr(date_val, "strftime"):
        dt: datetime = date_val
        return dt.strftime("%b %-d, %Y")
    try:
        return datetime.strptime(str(date_val), "%Y-%m-%d").strftime("%b %-d, %Y")
    except ValueError:
        return str(date_val)


def chapter_url(textbook: str, chapter_num: int) -> str:
    """Return the absolute URL for a textbook chapter page."""
    prefix = _TEXTBOOK_META.get(textbook, {}).get("url_prefix", "")
    return f"/{prefix}ch{chapter_num}/"


def chapter_label(textbook: str, chapter_num: int) -> str:
    """Return a label like 'BBH Ch28 — Hophal Strong'."""
    meta = _TEXTBOOK_META.get(textbook, {})
    short = meta.get("short", textbook)
    title = meta.get("chapters", {}).get(chapter_num, "")
    label = f"{short} Ch{chapter_num}"
    if title:
        label += f" — {title}"
    return label


def chapter_link_md(textbook: str, chapter_num: int) -> str:
    """Return a Markdown link for a chapter, or '' if chapter_num is falsy."""
    if not chapter_num:
        return ""
    return f"[{chapter_label(textbook, chapter_num)}]({chapter_url(textbook, chapter_num)})"


def session_slug(session: dict[str, Any]) -> str:
    return session.get("_dir") or f"session-{session['number']:02d}"


def session_filename(session: dict[str, Any]) -> str:
    return f"{session_slug(session)}.md"


def session_title(session: dict[str, Any]) -> str:
    return f"Session {session['number']} — {session.get('focus', '')}"


# ── Page renderers ────────────────────────────────────────────────────────────

def render_courses_index(courses: list[dict[str, Any]]) -> str:
    """Render mkdocs_src/courses/index.md — overview table of all courses."""
    lines = [
        "# Courses",
        "",
        "Syllabi for Biblical Hebrew, Greek, and Aramaic classes.",
        "",
    ]

    by_textbook: dict[str, list[dict[str, Any]]] = {}
    for course in courses:
        tb = course.get("textbook", "Other")
        by_textbook.setdefault(tb, []).append(course)

    for textbook, tb_courses in by_textbook.items():
        lines += [f"## {textbook}", ""]
        lines += [
            "| Course | Description | Instructor(s) | Sessions |",
            "|---|---|---|---|",
        ]
        for course in tb_courses:
            cid = course["id"]
            desc = course.get("description", "")
            instructors = ", ".join(course.get("instructors", []))
            count = len(course.get("sessions", []))
            link = f"[{cid}]({cid}/index.md)"
            lines.append(f"| {link} | {desc} | {instructors} | {count} |")
        lines.append("")

    return "\n".join(lines)


def render_course_page(course: dict[str, Any]) -> str:
    """Render mkdocs_src/courses/<id>/index.md — session table for one course."""
    cid = course["id"]
    name = course.get("name", cid)
    textbook = course.get("textbook", "")
    edition = course.get("edition", "")
    instructors = course.get("instructors", [])
    description = course.get("description", "")
    sessions = course.get("sessions", [])

    lines = [f"# {name} — {cid}", ""]

    if description:
        lines += [description, ""]

    tb_display = textbook
    if edition:
        tb_display += f", {edition} ed."
    lines.append(f"**Textbook:** {tb_display}  ")

    if instructors:
        lines.append(f"**Instructor(s):** {', '.join(instructors)}  ")

    lines.append("")

    if not sessions:
        lines += ["*No sessions recorded yet.*", ""]
        return "\n".join(lines)

    lines += [
        "## Sessions",
        "",
        "| Session | Date |",
        "|---|---|",
    ]

    for session in sessions:
        num = session.get("number", "")
        date_str = format_date(session.get("date"))
        focus = session.get("focus", "")
        sess_link = f"[{num} — {focus}](sessions/{session_filename(session)})"
        lines.append(f"| {sess_link} | {date_str} |")

    lines.append("")
    return "\n".join(lines)


def _section_content(section: dict[str, Any], session_dir: Path) -> str:
    """Return the body text for a section: inline content or file contents.

    File paths are relative to the per-session data directory
    (e.g. data/courses/bbh-2026.1/session-01/).
    """
    if section.get("file"):
        file_path = session_dir / section["file"]
        if file_path.exists():
            return file_path.read_text(encoding="utf-8").strip()
        return f"*(file not found: `{section['file']}`)*"
    return (section.get("content") or "").strip()


def render_session_page(
    course: dict[str, Any],
    session: dict[str, Any],
    course_dir: Path | None = None,
) -> str:
    """Render mkdocs_src/courses/<id>/sessions/session-NN.md."""
    cid = course["id"]
    name = course.get("name", cid)
    textbook = course.get("textbook", "")
    if course_dir is None:
        course_dir = _COURSES_DATA_DIR / cid
    session_dir = course_dir / session_slug(session)

    num = session.get("number", "")
    focus = session.get("focus", "")
    date_str = format_date(session.get("date"))
    instructor = (session.get("instructor") or "").strip()
    chapter = session.get("chapter")
    agenda = session.get("agenda") or []
    sections = session.get("sections") or []
    notes = (session.get("notes") or "").strip()

    lines = [
        f"# Session {num} — {focus}",
        "",
        f"**Course:** [{name} — {cid}](../index.md)  ",
    ]

    if date_str:
        lines.append(f"**Date:** {date_str}  ")
    if instructor:
        lines.append(f"**Instructor:** {instructor}  ")

    lines.append("")

    if chapter:
        lines += ["## Textbook Chapter", "", chapter_link_md(textbook, chapter), ""]

    if agenda:
        lines += ["## Agenda", ""]
        for item in agenda:
            title = item.get("title", "")
            url = item.get("url", "")
            entry = f"[{title}]({url})" if url else title
            lines.append(f"1. {entry}")
        lines.append("")

    for section in sections:
        heading = section.get("heading", "")
        body = _section_content(section, session_dir)
        if heading:
            lines += [f"## {heading}", ""]
        if body:
            lines += [body, ""]

    if notes:
        lines += ["## Notes", "", notes, ""]

    return "\n".join(lines)


# ── Nav management ────────────────────────────────────────────────────────────

def _build_nav_block(courses: list[dict[str, Any]]) -> str:
    """Build the YAML nav fragment for the Courses section."""
    lines = [
        _NAV_START,
        "- Courses:",
        "  - Overview: courses/index.md",
    ]

    by_short: dict[str, list[dict[str, Any]]] = {}
    for course in courses:
        tb = course.get("textbook", "Other")
        short = _TEXTBOOK_META.get(tb, {}).get("short", tb)
        by_short.setdefault(short, []).append(course)

    for tb_courses in by_short.values():
        for course in tb_courses:
            cid = course["id"]
            lines.append(f"  - {cid}:")
            lines.append(f"    - Overview: courses/{cid}/index.md")
            sessions = course.get("sessions", [])
            if sessions:
                lines.append("    - Sessions:")
                for session in sessions:
                    title = session_title(session)
                    fname = session_filename(session)
                    lines.append(f"      - '{title}': courses/{cid}/sessions/{fname}")

    lines.append(_NAV_END)
    return "\n".join(lines)


def update_nav(courses: list[dict[str, Any]]) -> None:
    """Insert or replace the Courses block in mkdocs_nav.yml."""
    nav_text = _NAV_PATH.read_text()
    new_block = _build_nav_block(courses)

    if _NAV_START in nav_text:
        pattern = re.compile(
            rf"{re.escape(_NAV_START)}.*?{re.escape(_NAV_END)}",
            re.DOTALL,
        )
        nav_text = pattern.sub(new_block, nav_text)
    else:
        # Insert before "- Study Helps:" or append
        for anchor in ("- Study Helps:", "- API Reference:"):
            if anchor in nav_text:
                nav_text = nav_text.replace(anchor, new_block + "\n" + anchor, 1)
                break
        else:
            nav_text = nav_text.rstrip() + "\n" + new_block + "\n"

    _NAV_PATH.write_text(nav_text)
    print(f"  Updated {_NAV_PATH.name}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    courses = load_all_courses()
    print(f"Found {len(courses)} course(s): {[c['id'] for c in courses]}")

    _COURSES_SITE_DIR.mkdir(parents=True, exist_ok=True)

    idx = _COURSES_SITE_DIR / "index.md"
    idx.write_text(render_courses_index(courses))
    print(f"  Wrote {idx.relative_to(_REPO_ROOT)}")

    for course in courses:
        cid = course["id"]
        course_out = _COURSES_SITE_DIR / cid
        sessions_out = course_out / "sessions"
        course_out.mkdir(parents=True, exist_ok=True)
        sessions_out.mkdir(parents=True, exist_ok=True)

        cp = course_out / "index.md"
        cp.write_text(render_course_page(course))
        print(f"  Wrote {cp.relative_to(_REPO_ROOT)}")

        course_dir = _COURSES_DATA_DIR / cid
        for session in course.get("sessions", []):
            sp = sessions_out / session_filename(session)
            sp.write_text(render_session_page(course, session, course_dir))
            print(f"  Wrote {sp.relative_to(_REPO_ROOT)}")

    update_nav(courses)
    print("Done.")


if __name__ == "__main__":
    main()
