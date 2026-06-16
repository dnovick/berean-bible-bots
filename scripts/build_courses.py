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

# Maps textbook short name (lowercase) → human-readable group label
_GROUP_LABELS: dict[str, str] = {
    "bbh": "Biblical Hebrew - Year 1",
    "bbg": "Biblical Greek",
    "bba": "Biblical Aramaic",
}


# ── Data loading ──────────────────────────────────────────────────────────────

def load_course_data(group_dir: Path) -> dict[str, Any]:
    """Load data/courses/<group>/course.yml, or return {} if absent."""
    yml = group_dir / "course.yml"
    if not yml.exists():
        return {}
    with open(yml) as f:
        return yaml.safe_load(f) or {}


def load_instance(instance_dir: Path) -> dict[str, Any]:
    """Load a course instance from instance.yml + session-NN/session.yml subdirectories."""
    with open(instance_dir / "instance.yml") as f:
        data: dict[str, Any] = yaml.safe_load(f)
    data.setdefault("instructors", [])
    data.setdefault("description", "")
    data.setdefault("edition", "")
    data["_instance_dir"] = instance_dir  # preserve actual path for session file resolution

    sessions: list[dict[str, Any]] = []
    for session_dir in sorted(
        d for d in instance_dir.iterdir()
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


def load_all_instances() -> list[dict[str, Any]]:
    """Load all courses from data/courses/<group>/<id>/, sorted by group then id."""
    courses = []
    for entry in sorted(_COURSES_DATA_DIR.iterdir()):
        if not entry.is_dir():
            continue
        if (entry / "instance.yml").exists():
            # Ungrouped legacy instance directly under data/courses/
            courses.append(load_instance(entry))
        else:
            # Group directory — scan one level deeper for instance dirs
            for course_dir in sorted(entry.iterdir()):
                if course_dir.is_dir() and (course_dir / "instance.yml").exists():
                    courses.append(load_instance(course_dir))
    return courses


# ── Slug / anchor helpers ────────────────────────────────────────────────────

def instance_group(course: dict[str, Any]) -> str:
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
        group = instance_group(course)
        if group not in seen_groups:
            seen_groups.append(group)

    for group in seen_groups:
        label = _GROUP_LABELS.get(group, group.upper())
        lines.append(f"- [{label}]({group}/index.md)")

    lines.append("")
    return "\n".join(lines)


def render_course_page(
    group: str,
    courses: list[dict[str, Any]],
    group_data: dict[str, Any],
) -> str:
    """Render mkdocs_src/courses/<group>/index.md — group landing page.

    group_data comes from data/courses/<group>/course.yml; falls back to
    _GROUP_LABELS / hardcoded student-resources if the file is absent.
    """
    label = group_data.get("name") or _GROUP_LABELS.get(group, group.upper())
    description = (group_data.get("description") or "").strip()
    resources = group_data.get("resources") or []

    lines = [f"# {label}", ""]
    if description:
        lines += [description, ""]

    lines += ["## Resources", ""]
    if resources:
        for res in resources:
            name = res.get("name", "")
            rfile = res.get("file", "")
            scope = res.get("scope", "course")
            desc = (res.get("description") or "").strip()
            if rfile:
                url = f"../common/{rfile}" if scope == "global" else f"common/{rfile}"
            else:
                url = ""
            entry = f"[{name}]({url})" if url else name
            suffix = f" — {desc}" if desc else ""
            lines.append(f"- {entry}{suffix}")
    else:
        lines.append(
            "- [Student Resources](common/student-resources.md) — "
            "Textbook acquisition and Bible software guide"
        )
    lines += [
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


def _copy_course_resources(group: str, common_out: Path) -> None:
    """Copy data/courses/<group>/common/* into mkdocs_src/courses/<group>/common/."""
    common_data = _COURSES_DATA_DIR / group / "common"
    if not common_data.is_dir():
        return
    common_out.mkdir(parents=True, exist_ok=True)
    for src in sorted(common_data.iterdir()):
        if src.is_file():
            dst = common_out / src.name
            dst.write_bytes(src.read_bytes())
            print(f"  Wrote {dst.relative_to(_REPO_ROOT)}")


def _copy_global_resources(global_out: Path) -> None:
    """Copy data/courses/common/* into mkdocs_src/courses/common/."""
    global_data = _COURSES_DATA_DIR / "common"
    if not global_data.is_dir():
        return
    global_out.mkdir(parents=True, exist_ok=True)
    for src in sorted(global_data.iterdir()):
        if src.is_file():
            dst = global_out / src.name
            dst.write_bytes(src.read_bytes())
            print(f"  Wrote {dst.relative_to(_REPO_ROOT)}")


def _copy_instance_resources(instance_dir: Path, instance_out: Path) -> None:
    """Copy instance_dir/common/* into mkdocs_src/courses/<group>/<id>/common/."""
    common_data = instance_dir / "common"
    if not common_data.is_dir():
        return
    common_out = instance_out / "common"
    common_out.mkdir(parents=True, exist_ok=True)
    for src in sorted(common_data.iterdir()):
        if src.is_file():
            dst = common_out / src.name
            dst.write_bytes(src.read_bytes())
            print(f"  Wrote {dst.relative_to(_REPO_ROOT)}")


def render_instance_page(course: dict[str, Any]) -> str:
    """Render mkdocs_src/courses/<id>/index.md — session table for one course."""
    cid = course["id"]
    name = course.get("name", cid)
    textbook = course.get("textbook", "")
    edition = course.get("edition", "")
    instructors = course.get("instructors", [])
    sessions = course.get("sessions", [])
    session_groups = course.get("session_groups", [])
    resources = course.get("resources") or []

    lines = [f"# {name} — {cid}", ""]

    tb_display = textbook
    if edition:
        tb_display += f", {edition} ed."
    lines.append(f"**Textbook:** {tb_display}  ")

    if instructors:
        lines.append(f"**Instructor(s):** {', '.join(instructors)}  ")

    lines.append("")

    if resources:
        lines += ["## Resources", ""]
        for res in resources:
            rname = res.get("name", "")
            rfile = res.get("file", "")
            scope = res.get("scope", "instance")
            desc = (res.get("description") or "").strip()
            if rfile:
                if scope == "global":
                    url = f"../../common/{rfile}"
                elif scope == "course":
                    url = f"../common/{rfile}"
                else:
                    url = f"common/{rfile}"
            else:
                url = ""
            entry = f"[{rname}]({url})" if url else rname
            suffix = f" — {desc}" if desc else ""
            lines.append(f"- {entry}{suffix}")
        lines.append("")

    if not sessions:
        lines += ["*No sessions recorded yet.*", ""]
        return "\n".join(lines)

    def _sess_num(s: dict[str, Any]) -> int:
        try:
            return int(s.get("number", 0))
        except (ValueError, TypeError):
            return 0

    def _sess_row(session: dict[str, Any]) -> str:
        num = session.get("number", "")
        date_str = format_date(session.get("date"))
        focus = session.get("focus", "")
        recording = (session.get("recording") or "").strip()
        sess_link = f"[{num} — {focus}](sessions/{session_filename(session)})"
        rec_cell = f"[Watch]({recording})" if recording else ""
        return f"| {sess_link} | {date_str} | {rec_cell} |"

    _TABLE_HDR = ["| Session | Date | Recording |", "|---|---|---|"]

    lines += ["## Sessions", ""]

    if session_groups:
        assigned_nums: set[int] = set()
        for grp in session_groups:
            frm = int(grp.get("from", 1))
            to = int(grp.get("to", 9999))
            grp_heading = grp.get("heading", "Sessions")
            grp_sessions = [s for s in sessions if frm <= _sess_num(s) <= to]
            if not grp_sessions:
                continue
            assigned_nums.update(_sess_num(s) for s in grp_sessions)
            lines += [f"### {grp_heading}", ""] + _TABLE_HDR
            for session in grp_sessions:
                lines.append(_sess_row(session))
            lines.append("")

        unassigned = [s for s in sessions if _sess_num(s) not in assigned_nums]
        if unassigned:
            lines += ["### Other Sessions", ""] + _TABLE_HDR
            for session in unassigned:
                lines.append(_sess_row(session))
            lines.append("")
    else:
        lines += _TABLE_HDR
        for session in sessions:
            lines.append(_sess_row(session))
        lines.append("")

    return "\n".join(lines)


def _resolve_file_path(ref: str, scope: str, session_dir: Path, instance_dir: Path) -> Path:
    """Return the filesystem path for a file: reference given its scope.

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
        return _COURSES_DATA_DIR / "common" / ref
    return session_dir / ref


def _section_content(section: dict[str, Any], session_dir: Path, instance_dir: Path) -> str:
    """Return the body text for a section: inline content or file contents."""
    if section.get("file"):
        ref = section["file"]
        if ref.startswith("http"):
            return f"*(external link: `{ref}`)*"
        scope = section.get("scope", "session")
        file_path = _resolve_file_path(ref, scope, session_dir, instance_dir)
        if file_path.exists():
            return file_path.read_text(encoding="utf-8").strip()
        return f"*(file not found: `{ref}`)*"
    return (section.get("content") or "").strip()


def render_session_page(
    course: dict[str, Any],
    session: dict[str, Any],
    instance_dir: Path | None = None,
) -> tuple[str, dict[str, str]]:
    """Render mkdocs_src/courses/<id>/sessions/session-NN.md.

    Returns (page_markdown, subpages) where subpages maps filename → content.
    Every section is always written as its own sub-page; the caller is
    responsible for writing those files under sessions/<session-slug>/.
    """
    cid = course["id"]
    name = course.get("name", cid)
    if instance_dir is None:
        instance_dir = _COURSES_DATA_DIR / cid
    sess_slug = session_slug(session)
    session_dir = instance_dir / sess_slug

    num = session.get("number", "")
    focus = session.get("focus", "")
    date_str = format_date(session.get("date"))
    instructor = (session.get("instructor") or "").strip()
    recording = (session.get("recording") or "").strip()
    agenda = session.get("agenda") or []
    sections = session.get("sections") or []
    subpage_decls = session.get("subpages") or []
    notes = (session.get("notes") or "").strip()
    files = session.get("files") or []
    homework = session.get("homework") or []
    lesson = session.get("lesson") or {}
    readings_raw = session.get("reading") or []
    # Normalize: accept a single dict or a list
    readings: list[dict] = (
        [readings_raw] if isinstance(readings_raw, dict) else list(readings_raw)
    )

    # ── First pass: classify each section, build heading → URL map ─────────────
    section_urls: dict[str, str] = {}
    subpages: dict[str, str] = {}

    for section in sections:
        heading = section.get("heading", "")
        body = _section_content(section, session_dir, instance_dir)
        cslug = content_slug(section)
        section_urls[heading] = f"{sess_slug}/{cslug}.md"
        subpages[f"{cslug}.md"] = f"# {heading}\n\n{_strip_leading_h1(body)}\n"

    # subpages: declared sub-pages linked from section content; written to the
    # session subdirectory but never surfaced in the agenda or Additional Info.
    for sp_decl in subpage_decls:
        heading = sp_decl.get("heading", "")
        body = _section_content(sp_decl, session_dir, instance_dir)
        cslug = content_slug(sp_decl)
        subpages[f"{cslug}.md"] = f"# {heading}\n\n{_strip_leading_h1(body)}\n"

    # Add reading names to section_urls so agenda items can auto-link to them.
    # Register both the bare name ("Genesis 1:1–5") and the prefixed form
    # ("Reading: Genesis 1:1–5") so manual agenda entries with either title link.
    for reading in readings:
        rname = reading.get("name", "")
        rfile = reading.get("file", "")
        if rname and rfile:
            section_urls[rname] = f"{sess_slug}/{rfile}"
            section_urls[f"Reading: {rname}"] = f"{sess_slug}/{rfile}"

    # Add "Exercises" to section_urls if this session has an exercises: block.
    exercises = session.get("exercises") or []
    if exercises:
        section_urls["Exercises"] = f"{sess_slug}/exercises.md"

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
    if recording:
        lines.append(f"**Recording:** [Watch]({recording})  ")

    lines.append("")

    # Build combined agenda: explicit items, then lesson, then readings
    lesson_agenda = (
        [{
            "title": f"Lesson: {lesson.get('name', '')}",
            "url": lesson.get("url", ""),
            "duration": lesson.get("duration", ""),
        }]
        if lesson.get("name") and lesson.get("url")
        else []
    )
    # Only auto-append a reading agenda entry if that title isn't already in the
    # manual agenda (prevents duplicates when the author writes it explicitly).
    manual_titles = {item.get("title", "") for item in agenda}
    reading_agenda = [
        {
            "title": f"Reading: {r.get('name', '')}",
            "url": f"{sess_slug}/{r.get('file', '')}",
            "duration": r.get("duration", ""),
        }
        for r in readings
        if r.get("name") and r.get("file")
        and f"Reading: {r.get('name', '')}" not in manual_titles
    ]
    full_agenda = list(agenda) + lesson_agenda + reading_agenda

    if full_agenda:
        lines += ["## Agenda", ""]
        for item in full_agenda:
            title = item.get("title", "")
            # Explicit url: in YAML always wins; otherwise auto-match to section
            url = item.get("url", "") or section_urls.get(title, "")
            entry = f"[{title}]({url})" if url else title
            duration = (item.get("duration") or "").strip()
            if duration:
                entry += f" ({duration})"
            lines.append(f"1. {entry}")
        lines.append("")

    # Sections with no matching agenda title are orphaned — surface them in a
    # dedicated ## Additional Info table rather than leaving them unreachable.
    agenda_titles = {item.get("title", "") for item in full_agenda}
    orphaned = [
        s for s in sections
        if s.get("heading", "") not in agenda_titles
    ]
    if orphaned:
        lines += ["## Additional Info", ""]
        lines += ["| Topic |", "|---|"]
        for s in orphaned:
            heading = s.get("heading", "")
            url = section_urls.get(heading, "")
            entry = f"[{heading}]({url})" if url else heading
            lines.append(f"| {entry} |")
        lines.append("")

    if homework:
        lines += ["## Homework", ""]
        for item in homework:
            lines.append(f"- {item}")
        lines.append("")

    if files:
        lines += ["## Downloads", ""]
        for f in files:
            fname = f.get("file", "")
            label = f.get("name", "") or fname
            url = f"{sess_slug}/{fname}" if fname else ""
            entry = f"[{label}]({url})" if url else label
            lines.append(f"- {entry}")
        lines.append("")

    if notes:
        lines += ["## Notes", "", notes, ""]

    return "\n".join(lines), subpages


# ── Session exercises pages ───────────────────────────────────────────────────

def _render_session_exercises_page(
    session: dict[str, Any],
    exercises: list[dict[str, Any]],
) -> str:
    """Render sessions/{slug}/exercises.md — exercises listing for one session."""
    num = session.get("number", "")
    focus = session.get("focus", "")
    back = f"../{session_filename(session)}"
    lines = [
        f"# Session {num} — {focus}: Exercises",
        "",
        f"[← Back to session]({back})",
        "",
    ]
    if not exercises:
        lines += ["*No exercises for this session.*", ""]
    else:
        lines += ["| Exercise | Description |", "|---|---|"]
        for ex in exercises:
            name = ex.get("name", "")
            slug = ex.get("slug", "")
            desc = ex.get("desc", "")
            if slug:
                lines.append(f"| [{name}](exercises/{slug}/index.md) | {desc} |")
            else:
                lines.append(f"| {name} | {desc} |")
        lines.append("")
    return "\n".join(lines)


def _render_session_exercise_overview(
    session: dict[str, Any],
    ex: dict[str, Any],
    ex_src: Path,
) -> str:
    """Render sessions/{slug}/exercises/{ex-slug}/index.md — one exercise page."""
    num = session.get("number", "")
    focus = session.get("focus", "")
    name = ex.get("name", "")
    slug = ex.get("slug", "")
    desc = ex.get("desc", "")

    html_files = list(ex_src.glob("*.html"))
    stem = html_files[0].stem if html_files else slug
    html_name = html_files[0].name if html_files else ""
    pdf_name = f"{stem}.pdf"
    md_name = f"{stem}.md"
    has_pdf = (ex_src / pdf_name).exists()
    has_md = (ex_src / md_name).exists()

    btn_parts: list[str] = []
    if html_name:
        btn_parts.append(
            f"[Full Screen (Interactive)]({html_name}){{.md-button .md-button--primary}}"
        )
    if has_pdf:
        btn_parts.append(f"[Print / PDF]({pdf_name}){{.md-button}}")
    if has_md:
        btn_parts.append(f"[Markdown]({md_name}){{.md-button}}")
    buttons_line = "  ".join(btn_parts)

    lines: list[str] = [
        f"# {name}",
        "",
        f"*Session {num} — {focus}*",
        "",
        buttons_line,
        "",
    ]
    if desc:
        lines += [desc, ""]
    return "\n".join(lines)


# ── Nav management ────────────────────────────────────────────────────────────

def _build_nav_block(
    courses: list[dict[str, Any]],
    group_data_map: dict[str, dict[str, Any]],
) -> str:
    """Build the YAML nav fragment for the Courses section."""
    lines = [
        _NAV_START,
        "- Courses:",
        "  - Overview: courses/index.md",
    ]

    by_group: dict[str, list[dict[str, Any]]] = {}
    for course in courses:
        by_group.setdefault(instance_group(course), []).append(course)

    for group, group_instances in by_group.items():
        gdata = group_data_map.get(group, {})
        label = gdata.get("name") or _GROUP_LABELS.get(group, group.upper())
        resources = gdata.get("resources") or []

        lines.append(f"  - {label}:")
        lines.append(f"    - Overview: courses/{group}/index.md")

        if resources:
            for res in resources:
                rname = res.get("name", "")
                rfile = res.get("file", "")
                scope = res.get("scope", "course")
                if rname and rfile:
                    if scope == "global":
                        lines.append(f"    - {rname}: courses/common/{rfile}")
                    else:
                        lines.append(f"    - {rname}: courses/{group}/common/{rfile}")
        else:
            lines.append(
                f"    - Student Resources: courses/{group}/common/student-resources.md"
            )

        for course in group_instances:
            cid = course["id"]
            lines.append(f"    - {cid}:")
            lines.append(f"      - Overview: courses/{group}/{cid}/index.md")
            for res in course.get("resources") or []:
                rname = res.get("name", "")
                rfile = res.get("file", "")
                scope = res.get("scope", "instance")
                if rname and rfile:
                    if scope == "global":
                        lines.append(f"      - {rname}: courses/common/{rfile}")
                    elif scope == "course":
                        lines.append(f"      - {rname}: courses/{group}/common/{rfile}")
                    else:
                        lines.append(f"      - {rname}: courses/{group}/{cid}/common/{rfile}")
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


def update_nav(
    courses: list[dict[str, Any]],
    group_data_map: dict[str, dict[str, Any]],
) -> None:
    """Insert or replace the Courses block in mkdocs_nav.yml."""
    nav_text = _NAV_PATH.read_text()
    new_block = _build_nav_block(courses, group_data_map)

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

    courses = load_all_instances()
    print(f"Found {len(courses)} course(s): {[c['id'] for c in courses]}")

    # Wipe and recreate so stale files (old non-grouped paths) don't linger.
    if _COURSES_SITE_DIR.exists():
        shutil.rmtree(_COURSES_SITE_DIR)
    _COURSES_SITE_DIR.mkdir(parents=True)

    idx = _COURSES_SITE_DIR / "index.md"
    idx.write_text(render_courses_index(courses))
    print(f"  Wrote {idx.relative_to(_REPO_ROOT)}")

    # Copy global common resources (data/courses/common/ → mkdocs_src/courses/common/).
    _copy_global_resources(_COURSES_SITE_DIR / "common")

    # Group courses and generate group landing + common resource pages.
    by_group: dict[str, list[dict[str, Any]]] = {}
    for course in courses:
        by_group.setdefault(instance_group(course), []).append(course)

    # Load group-level course.yml for every group that has one.
    group_data_map: dict[str, dict[str, Any]] = {}
    for group in by_group:
        group_data_map[group] = load_course_data(_COURSES_DATA_DIR / group)

    for group, group_instances in by_group.items():
        group_out = _COURSES_SITE_DIR / group
        common_out = group_out / "common"
        group_out.mkdir(parents=True, exist_ok=True)
        common_out.mkdir(parents=True, exist_ok=True)

        gp = group_out / "index.md"
        gp.write_text(render_course_page(group, group_instances, group_data_map[group]))
        print(f"  Wrote {gp.relative_to(_REPO_ROOT)}")

        _copy_course_resources(group, common_out)

        for course in group_instances:
            cid = course["id"]
            course_out = group_out / cid
            sessions_out = course_out / "sessions"
            course_out.mkdir(parents=True, exist_ok=True)
            sessions_out.mkdir(parents=True, exist_ok=True)

            instance_dir = course.get("_instance_dir") or _COURSES_DATA_DIR / cid

            cp = course_out / "index.md"
            cp.write_text(render_instance_page(course))
            print(f"  Wrote {cp.relative_to(_REPO_ROOT)}")

            _copy_instance_resources(instance_dir, course_out)
            for session in course.get("sessions", []):
                sp = sessions_out / session_filename(session)
                page_md, subpages = render_session_page(course, session, instance_dir)
                sp.write_text(page_md)
                print(f"  Wrote {sp.relative_to(_REPO_ROOT)}")

                if subpages:
                    subpage_dir = sessions_out / session_slug(session)
                    subpage_dir.mkdir(parents=True, exist_ok=True)
                    for fname, content in subpages.items():
                        subpage_path = subpage_dir / fname
                        subpage_path.write_text(content)
                        print(f"  Wrote {subpage_path.relative_to(_REPO_ROOT)}")

                sess_data_dir = instance_dir / session_slug(session)
                files_out_dir = sessions_out / session_slug(session)

                # Collect all session-level files that need copying:
                # - files: download attachments
                # - reading: HTML exercise files
                sess_files = session.get("files") or []
                readings_raw = session.get("reading") or []
                reading_list = (
                    [readings_raw] if isinstance(readings_raw, dict)
                    else list(readings_raw)
                )
                reading_files = [
                    {"file": r.get("file", ""), "scope": r.get("scope", "session")}
                    for r in reading_list
                    if r.get("file")
                ]
                all_copy_files = sess_files + reading_files
                if all_copy_files:
                    files_out_dir.mkdir(parents=True, exist_ok=True)
                    for f in all_copy_files:
                        src_name = f.get("file", "")
                        if not src_name:
                            continue
                        scope = f.get("scope", "session")
                        src = _resolve_file_path(src_name, scope, sess_data_dir, instance_dir)
                        if src.exists():
                            dst = files_out_dir / src_name
                            dst.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(src, dst)
                            print(f"  Copied {dst.relative_to(_REPO_ROOT)}")
                        else:
                            print(f"  WARNING: session file not found: {src}")

                # Generate exercises listing page + per-exercise overview pages.
                sess_exercises = session.get("exercises") or []
                if sess_exercises:
                    sess_site_dir = sessions_out / session_slug(session)
                    sess_site_dir.mkdir(parents=True, exist_ok=True)

                    ex_list_path = sess_site_dir / "exercises.md"
                    ex_list_path.write_text(
                        _render_session_exercises_page(session, sess_exercises)
                    )
                    print(f"  Wrote {ex_list_path.relative_to(_REPO_ROOT)}")

                    for ex in sess_exercises:
                        ex_slug = ex.get("slug", "")
                        if not ex_slug:
                            continue
                        ex_data_dir = sess_data_dir / "exercises" / ex_slug
                        ex_site_dir = sess_site_dir / "exercises" / ex_slug
                        ex_site_dir.mkdir(parents=True, exist_ok=True)

                        # Copy exercise files (.html, .pdf, .md)
                        for pattern in ("*.html", "*.pdf", "*.md"):
                            for src_file in ex_data_dir.glob(pattern):
                                shutil.copy2(src_file, ex_site_dir / src_file.name)
                                print(f"  Copied {(ex_site_dir / src_file.name).relative_to(_REPO_ROOT)}")

                        # Generate index.md overview page
                        overview = _render_session_exercise_overview(
                            session, ex, ex_data_dir
                        )
                        (ex_site_dir / "index.md").write_text(overview)
                        print(f"  Wrote {(ex_site_dir / 'index.md').relative_to(_REPO_ROOT)}")

    update_nav(courses, group_data_map)
    print("Done.")


if __name__ == "__main__":
    main()
