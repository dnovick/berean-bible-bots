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

# Content at or below this character count renders inline on the session page;
# anything larger is written as its own sub-page.
INLINE_THRESHOLD = 600

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

# Maps textbook short name (lowercase) → human-readable group label
_GROUP_LABELS: dict[str, str] = {
    "bbh": "Biblical Hebrew - Year 1",
    "bbg": "Biblical Greek",
    "bba": "Biblical Aramaic",
}


# ── Data loading ──────────────────────────────────────────────────────────────

def load_course(course_dir: Path) -> dict[str, Any]:
    """Load a course from course.yml + session-NN/session.yml subdirectories."""
    with open(course_dir / "course.yml") as f:
        data: dict[str, Any] = yaml.safe_load(f)
    data.setdefault("instructors", [])
    data.setdefault("description", "")
    data.setdefault("edition", "")
    data["_course_dir"] = course_dir  # preserve actual path for session file resolution

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
        # Derive number from directory name: session-01 → 1.
        # A 'number:' key in session.yml overrides the derived value.
        if "number" not in session:
            try:
                session["number"] = int(session_dir.name.split("-", 1)[1])
            except (IndexError, ValueError):
                session["number"] = len(sessions) + 1
        session["_dir"] = session_dir.name
        sessions.append(session)

    data["sessions"] = sessions
    return data


def load_all_courses() -> list[dict[str, Any]]:
    """Load all courses from data/courses/<group>/<id>/, sorted by group then id."""
    courses = []
    for entry in sorted(_COURSES_DATA_DIR.iterdir()):
        if not entry.is_dir():
            continue
        if (entry / "course.yml").exists():
            # Ungrouped legacy course directly under data/courses/
            courses.append(load_course(entry))
        else:
            # Group directory — scan one level deeper for course dirs
            for course_dir in sorted(entry.iterdir()):
                if course_dir.is_dir() and (course_dir / "course.yml").exists():
                    courses.append(load_course(course_dir))
    return courses


# ── Slug / anchor helpers ────────────────────────────────────────────────────

def course_group(course: dict[str, Any]) -> str:
    """Return the URL group prefix for a course (e.g. 'bbh', 'bbg', 'bba')."""
    tb = course.get("textbook", "")
    short = _TEXTBOOK_META.get(tb, {}).get("short", "")
    return short.lower() if short else "other"


def heading_anchor(heading: str) -> str:
    """Return a MkDocs-compatible anchor ID for a heading string."""
    slug = heading.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug.strip())
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def content_slug(section: dict[str, Any]) -> str:
    """Return a URL slug for a section's standalone sub-page."""
    if section.get("file"):
        return Path(section["file"]).stem
    return heading_anchor(section.get("heading", "section"))


def _strip_leading_h1(text: str) -> str:
    """Remove a leading '# …' H1 line when rendering content inline."""
    lines_list = text.splitlines()
    if lines_list and lines_list[0].startswith("# "):
        return "\n".join(lines_list[1:]).lstrip("\n")
    return text


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
    """Render mkdocs_src/courses/index.md — one entry per language group."""
    lines = [
        "# Courses",
        "",
        "Select a language to see its courses and resources.",
        "",
    ]

    seen_groups: list[str] = []
    for course in courses:
        group = course_group(course)
        if group not in seen_groups:
            seen_groups.append(group)

    for group in seen_groups:
        label = _GROUP_LABELS.get(group, group.upper())
        lines.append(f"- [{label}]({group}/index.md)")

    lines.append("")
    return "\n".join(lines)


def render_group_page(group: str, courses: list[dict[str, Any]]) -> str:
    """Render mkdocs_src/courses/<group>/index.md — group landing page."""
    label = _GROUP_LABELS.get(group, group.upper())
    lines = [
        f"# {label}",
        "",
        "## Resources",
        "",
        "- [Student Resources](common/student-resources.md) — "
        "Textbook acquisition and Bible software guide",
        "",
        "## Courses",
        "",
        "| Course | Instructor(s) | Sessions |",
        "|---|---|---|",
    ]
    for course in courses:
        cid = course["id"]
        instructors = ", ".join(course.get("instructors", []))
        count = len(course.get("sessions", []))
        link = f"[{cid}]({cid}/index.md)"
        lines.append(f"| {link} | {instructors} | {count} |")
    lines.append("")
    return "\n".join(lines)


def _copy_common_resources(group: str, common_out: Path) -> None:
    """Copy data/courses/<group>/common/*.md into mkdocs_src/courses/<group>/common/."""
    common_data = _COURSES_DATA_DIR / group / "common"
    if not common_data.is_dir():
        return
    for src in sorted(common_data.glob("*.md")):
        dst = common_out / src.name
        dst.write_text(src.read_text(encoding="utf-8"))
        print(f"  Wrote {dst.relative_to(_REPO_ROOT)}")


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
) -> tuple[str, dict[str, str]]:
    """Render mkdocs_src/courses/<id>/sessions/session-NN.md.

    Returns (page_markdown, subpages) where subpages maps filename → content
    for sections whose content exceeds INLINE_THRESHOLD.  The caller is
    responsible for writing those files under sessions/<session-slug>/.
    """
    cid = course["id"]
    name = course.get("name", cid)
    textbook = course.get("textbook", "")
    if course_dir is None:
        course_dir = _COURSES_DATA_DIR / cid
    sess_slug = session_slug(session)
    session_dir = course_dir / sess_slug

    num = session.get("number", "")
    focus = session.get("focus", "")
    date_str = format_date(session.get("date"))
    instructor = (session.get("instructor") or "").strip()
    chapter = session.get("chapter")
    agenda = session.get("agenda") or []
    sections = session.get("sections") or []
    notes = (session.get("notes") or "").strip()

    # ── First pass: classify each section, build heading → URL map ─────────────
    section_urls: dict[str, str] = {}
    subpages: dict[str, str] = {}

    for section in sections:
        heading = section.get("heading", "")
        body = _section_content(section, session_dir)
        if len(body) <= INLINE_THRESHOLD:
            anchor = heading_anchor(heading)
            if anchor:
                section_urls[heading] = f"#{anchor}"
        else:
            cslug = content_slug(section)
            section_urls[heading] = f"{sess_slug}/{cslug}.md"
            subpages[f"{cslug}.md"] = f"# {heading}\n\n{_strip_leading_h1(body)}\n"

    # ── Build page ──────────────────────────────────────────────────────────────
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
            # Explicit url: in YAML always wins; otherwise auto-match to section
            url = item.get("url", "") or section_urls.get(title, "")
            entry = f"[{title}]({url})" if url else title
            lines.append(f"1. {entry}")
        lines.append("")

    # Render only inline sections; subpages are written by the caller
    for section in sections:
        heading = section.get("heading", "")
        body = _section_content(section, session_dir)
        if len(body) <= INLINE_THRESHOLD:
            if heading:
                lines += [f"## {heading}", ""]
            inline_body = _strip_leading_h1(body)
            if inline_body:
                lines += [inline_body, ""]

    if notes:
        lines += ["## Notes", "", notes, ""]

    return "\n".join(lines), subpages


# ── Nav management ────────────────────────────────────────────────────────────

def _build_nav_block(courses: list[dict[str, Any]]) -> str:
    """Build the YAML nav fragment for the Courses section."""
    lines = [
        _NAV_START,
        "- Courses:",
        "  - Overview: courses/index.md",
    ]

    by_group: dict[str, list[dict[str, Any]]] = {}
    for course in courses:
        by_group.setdefault(course_group(course), []).append(course)

    for group, group_courses in by_group.items():
        label = _GROUP_LABELS.get(group, group.upper())
        lines.append(f"  - {label}:")
        lines.append(f"    - Overview: courses/{group}/index.md")
        lines.append(
            f"    - Student Resources: courses/{group}/common/student-resources.md"
        )
        for course in group_courses:
            cid = course["id"]
            lines.append(f"    - {cid}:")
            lines.append(f"      - Overview: courses/{group}/{cid}/index.md")
            sessions = course.get("sessions", [])
            if sessions:
                lines.append("      - Sessions:")
                for session in sessions:
                    title = session_title(session)
                    fname = session_filename(session)
                    lines.append(
                        f"        - '{title}': courses/{group}/{cid}/sessions/{fname}"
                    )

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
    import shutil

    courses = load_all_courses()
    print(f"Found {len(courses)} course(s): {[c['id'] for c in courses]}")

    # Wipe and recreate so stale files (old non-grouped paths) don't linger.
    if _COURSES_SITE_DIR.exists():
        shutil.rmtree(_COURSES_SITE_DIR)
    _COURSES_SITE_DIR.mkdir(parents=True)

    idx = _COURSES_SITE_DIR / "index.md"
    idx.write_text(render_courses_index(courses))
    print(f"  Wrote {idx.relative_to(_REPO_ROOT)}")

    # Group courses and generate group landing + common resource pages.
    by_group: dict[str, list[dict[str, Any]]] = {}
    for course in courses:
        by_group.setdefault(course_group(course), []).append(course)

    for group, group_courses in by_group.items():
        group_out = _COURSES_SITE_DIR / group
        common_out = group_out / "common"
        group_out.mkdir(parents=True, exist_ok=True)
        common_out.mkdir(parents=True, exist_ok=True)

        gp = group_out / "index.md"
        gp.write_text(render_group_page(group, group_courses))
        print(f"  Wrote {gp.relative_to(_REPO_ROOT)}")

        _copy_common_resources(group, common_out)

        for course in group_courses:
            cid = course["id"]
            course_out = group_out / cid
            sessions_out = course_out / "sessions"
            course_out.mkdir(parents=True, exist_ok=True)
            sessions_out.mkdir(parents=True, exist_ok=True)

            cp = course_out / "index.md"
            cp.write_text(render_course_page(course))
            print(f"  Wrote {cp.relative_to(_REPO_ROOT)}")

            course_dir = course.get("_course_dir") or _COURSES_DATA_DIR / cid
            for session in course.get("sessions", []):
                sp = sessions_out / session_filename(session)
                page_md, subpages = render_session_page(course, session, course_dir)
                sp.write_text(page_md)
                print(f"  Wrote {sp.relative_to(_REPO_ROOT)}")

                if subpages:
                    subpage_dir = sessions_out / session_slug(session)
                    subpage_dir.mkdir(parents=True, exist_ok=True)
                    for fname, content in subpages.items():
                        subpage_path = subpage_dir / fname
                        subpage_path.write_text(content)
                        print(f"  Wrote {subpage_path.relative_to(_REPO_ROOT)}")

    update_nav(courses)
    print("Done.")


if __name__ == "__main__":
    main()
