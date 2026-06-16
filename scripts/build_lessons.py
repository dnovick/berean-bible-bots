"""Build the MkDocs source tree for all lessons (BBH, BBG, BBA).

Reads data/lessons/{bbh,bbg,bba}/ and writes generated output to
mkdocs_src/lessons/{hebrew,greek,aramaic}/.  Updates the lessons block in
mkdocs_nav.yml using sentinel markers (# <LESSONS> / # </LESSONS>) so the
script can be run standalone without touching the rest of the nav.

Run before `mkdocs build` (or let the pre-commit hook do it automatically):
    python scripts/build_lessons.py
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Any

import yaml

_REPO = Path(__file__).resolve().parent.parent
_LESSONS = _REPO / "data" / "lessons"
_MKDOCS_SRC = _REPO / "mkdocs_src"
_NAV_PATH = _REPO / "mkdocs_nav.yml"

# Sentinel markers used to delimit the lessons block in mkdocs_nav.yml.
# build_mkdocs.py inserts these when writing the full nav; update_nav()
# uses them to patch just the lessons section on incremental rebuilds.
NAV_START = "# <LESSONS>"
NAV_END = "# </LESSONS>"

# ── Chapter title maps ────────────────────────────────────────────────────────

BBH_TITLES: dict[str, str] = {
    "ch1": "Hebrew Alphabet",
    "ch2": "Hebrew Vowels",
    "ch3": "Syllabification and Pronunciation",
    "ch4": "Hebrew Nouns",
    "ch5": "Definite Article and Conjunction ו",
    "ch6": "Hebrew Prepositions",
    "ch7": "Hebrew Adjectives",
    "ch8": "Hebrew Pronouns",
    "ch9": "Hebrew Pronominal Suffixes",
    "ch10": "Hebrew Construct Chain",
    "ch11": "Hebrew Numbers",
    "ch12": "Introduction to Hebrew Verbs",
    "ch13": "Qal Perfect Strong Verbs",
    "ch14": "Qal Perfect Weak Verbs",
    "ch15": "Qal Imperfect Strong Verbs",
    "ch16": "Qal Imperfect Weak Verbs",
    "ch17": "Waw-Consecutive",
    "ch18": "Qal Imperative",
    "ch19": "Qal Pronominal Suffixes on Verbs",
    "ch20": "Qal Infinitive Construct",
    "ch21": "Qal Infinitive Absolute",
    "ch22": "Qal Participle",
    "ch23": "Sentence Syntax",
    "ch24": "Niphal Strong",
    "ch25": "Niphal Weak",
    "ch26": "Hiphil Strong",
    "ch27": "Hiphil Weak",
    "ch28": "Hophal Strong",
    "ch29": "Hophal Weak",
    "ch30": "Piel Strong",
    "ch31": "Piel Weak",
    "ch32": "Pual Strong",
    "ch33": "Pual Weak",
    "ch34": "Hithpael Strong",
    "ch35": "Hithpael Weak",
}

BBG_TITLES: dict[str, str] = {
    "ch1": "The Greek Language",
    "ch2": "Learning Greek",
    "ch3": "The Alphabet and Pronunciation",
    "ch4": "Punctuation and Syllabification",
    "ch5": "Introduction to English Nouns",
    "ch6": "Nominative and Accusative; Article",
    "ch7": "Genitive and Dative",
    "ch8": "Prepositions and εἰμί",
    "ch9": "Adjectives",
    "ch10": "Third Declension",
    "ch11": "First and Second Person Personal Pronouns",
    "ch12": "αὐτός",
    "ch13": "Demonstrative Pronouns/Adjectives",
    "ch14": "Relative Pronoun",
    "ch15": "Introduction to Verbs",
    "ch16": "Present Active Indicative",
    "ch17": "Contract Verbs",
    "ch18": "Present Middle/Passive Indicative",
    "ch19": "Future Active and Middle Indicative",
    "ch20": "Verbal Roots (Patterns 2–4)",
    "ch21": "Imperfect Indicative",
    "ch22": "Second Aorist Active and Middle Indicative",
    "ch23": "First Aorist Active and Middle Indicative",
    "ch24": "Aorist and Future Passive Indicative",
    "ch25": "Perfect Indicative",
    "ch26": "Introduction to Participles",
    "ch27": "Imperfective (Present) Adverbial Participles",
    "ch28": "Perfective (Aorist) Adverbial Participles",
    "ch29": "Adjectival Participles",
    "ch30": "Combinative (Perfect) Participles and Genitive Absolutes",
    "ch31": "Subjunctive",
    "ch32": "Infinitive",
    "ch33": "Imperative",
    "ch34": "Indicative of δίδωμι",
    "ch35": "Nonindicative of δίδωμι and Conditional Sentences",
    "ch36": "ἵστημι, τίθημι, δείκνυμι and Odds 'n Ends",
}

BBA_TITLES: dict[str, str] = {
    "ch1": "Alphabet",
    "ch2": "Vowels",
    "ch3": "Syllabification",
    "ch4": "Nouns: Absolute State",
    "ch5": "Nouns: Determined State",
    "ch6": "Nouns: Construct State",
    "ch7": "Conjunctions and Prepositions",
    "ch8": "Pronominal Suffixes",
    "ch9": "Pronouns",
    "ch10": "Adjectives and Numbers",
    "ch11": "Adverbs and Particles",
    "ch12": "Introduction to Aramaic Verbs",
    "ch13": "Peal Perfect",
    "ch14": "Peal Imperfect",
    "ch15": "Peal Imperative",
    "ch16": "Peal Infinitive Construct",
    "ch17": "Peal Participle",
    "ch18": "The Peil, Hithpeel, and Ithpeel Stems",
    "ch19": "The Pael Stem",
    "ch20": "The Hithpaal and Ithpaal Stems",
    "ch21": "The Haphel Stem",
    "ch22": "The Aphel, Shaphel, and Hophal Stems",
}

# (lang, data-dir-name, nav-label, titles)
COURSES: list[tuple[str, str, str, dict[str, str]]] = [
    ("hebrew", "bbh", "Biblical Hebrew (BBH)", BBH_TITLES),
    ("greek",   "bbg", "Biblical Greek (BBG)",   BBG_TITLES),
    ("aramaic", "bba", "Biblical Aramaic (BBA)", BBA_TITLES),
]

_COURSE_META: dict[str, Any] = {
    "hebrew": {
        "heading": "Biblical Hebrew — BBH",
        "textbook": "*Basics of Biblical Hebrew*, Pratico & Van Pelt, 3rd Edition",
        "sections": None,
    },
    "greek": {
        "heading": "Biblical Greek — BBG",
        "textbook": "*Basics of Biblical Greek*, William D. Mounce, 4th Edition",
        "sections": None,
    },
    "aramaic": {
        "heading": "Biblical Aramaic — BBA",
        "textbook": "*Basics of Biblical Aramaic*",
        "sections": [
            ("Phonological System",        range(1, 4)),
            ("Nominal System",             range(4, 12)),
            ("Verbal System: Peal",        range(12, 18)),
            ("Verbal System: Derived Stems", range(18, 23)),
        ],
    },
}

# ── General helpers ───────────────────────────────────────────────────────────


def sorted_chapters(titles: dict[str, str]) -> list[str]:
    return sorted(titles.keys(), key=lambda x: int(x[2:]))


def slugify(name: str) -> str:
    """Convert exercise dir name to a readable title."""
    name = re.sub(r"^ch\d+-", "", name)
    return name.replace("-", " ").title()


def _md_title(path: Path) -> str:
    """Return the first # heading from a markdown file."""
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    except OSError:
        pass
    return path.stem.replace("-", " ").replace("_", " ").title()


def _read_chapter_yml(course: str, ch: str) -> dict[str, Any]:
    path = _LESSONS / course / ch / "chapter.yml"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _strip_tags(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


def _readme_description(readme_path: Path) -> str:
    if not readme_path.exists():
        return ""
    text = readme_path.read_text(encoding="utf-8")
    text = re.sub(r"^#[^#][^\n]*\n", "", text).strip()
    text = re.sub(r"^\*[^\n]*\*\n+", "", text).strip()
    text = re.sub(r"^---\n+", "", text).strip()
    text = re.sub(r"^## Description\n+", "", text, flags=re.IGNORECASE).strip()
    m = re.search(r"\n##|^---", text, re.MULTILINE)
    desc = text[: m.start()].strip() if m else text.strip()
    desc = re.sub(r"^#{1,3}[^\n]*\n", "", desc, flags=re.MULTILINE).strip()
    desc = re.sub(r"^\*\*\w[^*]*:\*\*[^\n]*\n?", "", desc, flags=re.MULTILINE).strip()
    return desc


def _readme_coverage_table(readme_path: Path) -> str:
    if not readme_path.exists():
        return ""
    table_lines: list[str] = []
    in_table = False
    for line in readme_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("|"):
            in_table = True
            table_lines.append(line)
        elif in_table:
            break
    return "\n".join(table_lines) if table_lines else ""


def _sample_qas(html_path: Path, n: int = 3) -> list[tuple[str, str]]:
    if not html_path.exists():
        return []
    text = html_path.read_text(encoding="utf-8")

    # JS items[] pattern (Greek parsing drills)
    items_m = re.search(r"const items\s*=\s*\[(.*?)\];", text, re.DOTALL)
    if items_m:
        pairs: list[tuple[str, str]] = []
        for obj in re.finditer(r"\{([^}]+)\}", items_m.group(1)):
            fields: dict[str, str] = {}
            for kv in re.finditer(r'(\w+)\s*:\s*"([^"]*)"', obj.group(1)):
                fields[kv.group(1)] = kv.group(2)
            if "form" not in fields:
                continue
            q = fields.get("form", "")
            a = " · ".join(
                fields[k] for k in
                ("tense", "voice", "mood", "person", "number", "aug", "lexical", "trans")
                if k in fields
            )
            if q and a:
                pairs.append((q, a))
            if len(pairs) >= n:
                break
        return pairs

    # Static HTML row pattern
    ans_pattern = re.compile(
        r'<tr[^>]*class="[^"]*(?:ans-row|answer-row)[^"]*"[^>]*>(.*?)</tr>',
        re.DOTALL | re.IGNORECASE,
    )
    parts = ans_pattern.split(text)
    static_pairs: list[tuple[str, str]] = []
    for i in range(1, len(parts), 2):
        q_rows = re.findall(r"<tr[^>]*>(.*?)</tr>", parts[i - 1], re.DOTALL)
        if not q_rows:
            continue
        q_text = re.sub(
            r"(▶ Answer|▼ Hide|כתוב\.\.\.|parse\.\.\.|—)", "",
            _strip_tags(q_rows[-1])
        ).strip()
        q_text = re.sub(r"\s+", " ", q_text).strip()
        a_text = re.sub(r"\s+", " ", _strip_tags(parts[i])).strip()
        if re.search(r"\d", q_text) and q_text and a_text:
            static_pairs.append((q_text, a_text))
        if len(static_pairs) >= n:
            break
    return static_pairs


# ── Deck helpers ──────────────────────────────────────────────────────────────


def _deck_short_title(stem: str) -> str:
    name = re.sub(r"^ch\d+-", "", stem)
    name = re.sub(r"-deck$", "", name)
    return name.replace("-", " ").title()


def _deck_description(deck_md: Path) -> str:
    if not deck_md.exists():
        return ""
    m = re.search(r"^\*([^*\n]+)\*",
                  deck_md.read_text(encoding="utf-8"), re.MULTILINE)
    return m.group(1).strip() if m else ""


def _prepend_deck_download_header(content: str, stem: str) -> str:
    h1_m = re.match(r"(# [^\n]+\n)", content)
    if not h1_m:
        return content
    dl_line = (
        f"\n**Download:** [Anki import (.txt)]({stem}.txt) · "
        f"[Flashcards Deluxe (-fd.txt)]({stem}-fd.txt)\n\n---\n\n"
    )
    rest = re.sub(r"^\s*---\s*\n+", "", content[h1_m.end():])
    return h1_m.group(0) + dl_line + rest


# ── Page generators ───────────────────────────────────────────────────────────


def _inject_lesson_header(
    content: str,
    focus: str,
    has_exercises: bool,
    has_decks: bool,
) -> str:
    h1_m = re.match(r"(# [^\n]+\n)", content)
    if not h1_m:
        return content
    lines: list[str] = [""]
    if focus:
        lines += [f"> {focus.strip()}", ""]
    if has_exercises or has_decks:
        lines += ["| Resource | Link |", "|---|---|"]
        if has_exercises:
            lines.append("| Exercises | [View exercises →](exercises.md) |")
        if has_decks:
            lines.append("| Flashcard Decks | [View decks →](flashcards.md) |")
        lines.append("")
    return h1_m.group(0) + "\n".join(lines) + content[h1_m.end():]


def _build_exercise_page(
    ex_src: Path,
    ex_title: str,
    ch_num: int,
    ch_title: str,
    html_name: str,
    md_name: str,
    pdf_name: str,
    has_md: bool,
    has_pdf: bool,
) -> str:
    btn_parts = [
        f"[Full Screen (Interactive)]({html_name}){{.md-button .md-button--primary}}"
    ]
    if has_pdf:
        btn_parts.append(f"[Print / PDF]({pdf_name}){{.md-button}}")
    if has_md:
        btn_parts.append(f"[Markdown]({md_name}){{.md-button}}")

    lines: list[str] = [
        f"# {ex_title}", "",
        f"*Chapter {ch_num} — {ch_title}*", "",
        "  ".join(btn_parts), "",
    ]
    desc = _readme_description(ex_src / "README.md")
    if desc:
        lines += [desc, ""]
    cov = _readme_coverage_table(ex_src / "README.md")
    if cov:
        lines += ["## Coverage", "", cov, ""]
    for i, (q, a) in enumerate(_sample_qas(ex_src / html_name, n=3), 1):
        if i == 1:
            lines += ["## Sample Questions", ""]
        lines += [f"**Q{i}.** {q}", f"> **A:** {a}", ""]
    return "\n".join(lines)


def _build_exercises_page(ch_num: int, ch_title: str, items: list[dict]) -> str:
    lines = [
        f"# Ch{ch_num} — {ch_title}: Exercises", "",
        "[← Back to lesson](index.md)", "",
    ]
    if not items:
        lines += ["*No exercises for this chapter.*", ""]
    else:
        lines += ["| Exercise | Description |", "|---|---|"]
        for item in items:
            lines.append(
                f"| [{item['title']}]({item['link']}) "
                f"| {item.get('desc', '').replace(chr(10), ' ')} |"
            )
        lines.append("")
    return "\n".join(lines)


def _build_flashcards_page(ch_num: int, ch_title: str, items: list[dict]) -> str:
    lines = [
        f"# Ch{ch_num} — {ch_title}: Flashcards", "",
        "[← Back to lesson](index.md)", "",
    ]
    if not items:
        lines += ["*No flashcard decks for this chapter.*", ""]
    else:
        lines += ["| Deck | Description |", "|---|---|"]
        for item in items:
            lines.append(
                f"| [{item['title']}]({item['md']}) "
                f"| {item.get('desc', '').replace(chr(10), ' ')} |"
            )
        lines.append("")
    return "\n".join(lines)


# ── Chapter builder ───────────────────────────────────────────────────────────


def build_chapter(
    lang: str,
    course: str,
    ch: str,
    title: str,
    ch_num: int,
) -> list[dict]:
    """Build output for one chapter. Returns nav entries."""
    src_dir = _LESSONS / course / ch
    dst_dir = _MKDOCS_SRC / "lessons" / lang / ch
    dst_dir.mkdir(parents=True, exist_ok=True)

    focus = (_read_chapter_yml(course, ch).get("focus") or "").strip()

    # ── Exercises ─────────────────────────────────────────────────────────────
    exercise_items: list[dict] = []
    exercises_src = src_dir / "exercises"
    if exercises_src.is_dir():
        for ex_dir in sorted(d for d in exercises_src.iterdir() if d.is_dir()):
            ex_name = ex_dir.name
            ex_dst = dst_dir / "exercises" / ex_name
            ex_dst.mkdir(parents=True, exist_ok=True)
            for ext in ("*.md", "*.html", "*.pdf"):
                for f in ex_dir.glob(ext):
                    shutil.copy(f, ex_dst / f.name)

            html_files = list(ex_dir.glob("*.html"))
            ex_desc = _readme_description(ex_dir / "README.md")
            if html_files:
                stem = html_files[0].stem
                html_name = html_files[0].name
                has_md = (ex_dir / f"{stem}.md").exists()
                has_pdf = (ex_dir / f"{stem}.pdf").exists()
                (ex_dst / "index.md").write_text(
                    _build_exercise_page(
                        ex_src=ex_dir,
                        ex_title=slugify(ex_name),
                        ch_num=ch_num,
                        ch_title=title,
                        html_name=html_name,
                        md_name=f"{stem}.md",
                        pdf_name=f"{stem}.pdf",
                        has_md=has_md,
                        has_pdf=has_pdf,
                    ),
                    encoding="utf-8",
                )
                ex_link = f"exercises/{ex_name}/index.md"
            elif (ex_dir / "README.md").exists():
                ex_link = f"exercises/{ex_name}/README.md"
            else:
                continue

            exercise_items.append(
                {"title": slugify(ex_name), "link": ex_link, "desc": ex_desc}
            )

    # ── Flashcard decks ───────────────────────────────────────────────────────
    deck_items: list[dict] = []
    for deck_md in sorted(src_dir.glob("*-deck.md")):
        content = _prepend_deck_download_header(
            deck_md.read_text(encoding="utf-8"), deck_md.stem
        )
        (dst_dir / deck_md.name).write_text(content, encoding="utf-8")
        deck_items.append({
            "title": _deck_short_title(deck_md.stem),
            "md": deck_md.name,
            "desc": _deck_description(deck_md),
        })
    for txt in src_dir.glob("*.txt"):
        shutil.copy(txt, dst_dir / txt.name)

    # Other .md files (paradigms, etc.)
    for md in src_dir.glob("*.md"):
        if md.name != "README.md" and not md.name.endswith("-deck.md"):
            shutil.copy(md, dst_dir / md.name)

    # ── Listing pages ─────────────────────────────────────────────────────────
    if exercise_items:
        (dst_dir / "exercises.md").write_text(
            _build_exercises_page(ch_num, title, exercise_items), encoding="utf-8"
        )
    if deck_items:
        (dst_dir / "flashcards.md").write_text(
            _build_flashcards_page(ch_num, title, deck_items), encoding="utf-8"
        )

    # ── index.md from README.md ───────────────────────────────────────────────
    readme = src_dir / "README.md"
    if readme.exists():
        content = readme.read_text(encoding="utf-8")
        content = re.sub(r"(exercises/[^)]+/)README\.md", r"\1index.md", content)
        content = re.sub(r"\((exercises/[^)]+/)\)", r"(\1index.md)", content)
        content = _inject_lesson_header(
            content, focus,
            has_exercises=bool(exercise_items),
            has_decks=bool(deck_items),
        )
        (dst_dir / "index.md").write_text(content, encoding="utf-8")

    # ── Nav ───────────────────────────────────────────────────────────────────
    ch_nav: list = [{"Lesson": f"lessons/{lang}/{ch}/index.md"}]
    if exercise_items:
        ch_nav.append({"Exercises": f"lessons/{lang}/{ch}/exercises.md"})
    if deck_items:
        ch_nav.append({"Flashcards": f"lessons/{lang}/{ch}/flashcards.md"})
    return [{f"Ch{ch_num} — {title}": ch_nav}]


# ── Additional resources (BBH) ────────────────────────────────────────────────


def build_additional_resources_nav() -> list:
    """Copy BBH additional-resources and return nav entries."""
    src = _LESSONS / "bbh" / "additional-resources"
    dst = _MKDOCS_SRC / "lessons" / "hebrew" / "additional-resources"
    if not src.exists():
        return []
    dst.mkdir(parents=True, exist_ok=True)

    nav_entries: list[dict] = []

    # Top-level index page
    top_index = src / "index.md"
    if top_index.exists():
        shutil.copy(top_index, dst / "index.md")
        nav_entries.append({"Overview": "lessons/hebrew/additional-resources/index.md"})

    # One subdir per resource; find primary .md for the nav link
    for sub in sorted(d for d in src.iterdir() if d.is_dir()):
        sub_dst = dst / sub.name
        sub_dst.mkdir(parents=True, exist_ok=True)
        for f in sub.iterdir():
            if f.is_file():
                shutil.copy(f, sub_dst / f.name)
        md_files = [f for f in sub.glob("*.md") if f.name.lower() != "readme.md"]
        if md_files:
            md = md_files[0]
            nav_entries.append(
                {_md_title(sub_dst / md.name):
                 f"lessons/hebrew/additional-resources/{sub.name}/{md.name}"}
            )

    return [{"Additional Resources": nav_entries}] if nav_entries else []


# ── Course builder ────────────────────────────────────────────────────────────


def build_course_overview(lang: str, titles: dict[str, str]) -> None:
    meta = _COURSE_META[lang]
    dst = _MKDOCS_SRC / "lessons" / lang
    dst.mkdir(parents=True, exist_ok=True)

    def _table(chs: list[str]) -> list[str]:
        rows = ["| Chapter | Topic |", "|---|---|"]
        for ch in chs:
            ch_num = int(ch[2:])
            rows.append(
                f"| [Ch{ch_num} — {titles[ch]}]({ch}/index.md) | {titles[ch]} |"
            )
        return rows

    lines = [f"# {meta['heading']}", "", meta["textbook"], "", "---", "", "## Syllabus", ""]
    all_chs = sorted_chapters(titles)
    if meta["sections"] is None:
        lines.extend(_table(all_chs))
    else:
        ch_by_num = {int(ch[2:]): ch for ch in all_chs}
        for section_title, ch_range in meta["sections"]:
            lines += [f"### {section_title}", ""]
            lines.extend(_table([ch_by_num[n] for n in ch_range if n in ch_by_num]))
            lines.append("")

    (dst / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_course(
    lang: str,
    course: str,
    label: str,
    titles: dict[str, str],
) -> list[dict]:
    """Build all chapters for one course. Returns nav entries for that course."""
    build_course_overview(lang, titles)
    nav_entries: list[dict] = [{"Overview": f"lessons/{lang}/index.md"}]
    for ch in sorted_chapters(titles):
        src = _LESSONS / course / ch
        if not src.is_dir():
            continue
        nav_entries.extend(build_chapter(lang, course, ch, titles[ch], int(ch[2:])))
    if lang == "hebrew" and course == "bbh":
        nav_entries.extend(build_additional_resources_nav())
    return [{label: nav_entries}]


# ── Build all ─────────────────────────────────────────────────────────────────


def build_all() -> list[dict]:
    """Build all lesson output. Returns the full lessons nav entries list."""
    # Clean stale chapter and additional-resources dirs
    for lang, _, _, titles in COURSES:
        lang_dir = _MKDOCS_SRC / "lessons" / lang
        for ch in sorted_chapters(titles):
            ch_dir = lang_dir / ch
            if ch_dir.exists():
                shutil.rmtree(ch_dir)
        ar = lang_dir / "additional-resources"
        if ar.exists():
            shutil.rmtree(ar)

    nav_entries: list[dict] = []
    total = 0
    for lang, course, label, titles in COURSES:
        nav_entries.extend(build_course(lang, course, label, titles))
        total += sum(
            1 for ch in sorted_chapters(titles)
            if (_LESSONS / course / ch).is_dir()
        )
    print(f"  Processed {total} chapters across {len(COURSES)} courses.")
    return nav_entries


# ── Nav update ────────────────────────────────────────────────────────────────


def _lesson_nav_block(lesson_entries: list[dict]) -> str:
    """Serialize lesson nav entries wrapped in sentinel markers."""
    block_yaml = yaml.dump(lesson_entries, allow_unicode=True, sort_keys=False).rstrip()
    return f"{NAV_START}\n{block_yaml}\n{NAV_END}"


def update_nav(lesson_entries: list[dict]) -> None:
    """Insert or replace the lessons block in mkdocs_nav.yml."""
    nav_text = _NAV_PATH.read_text(encoding="utf-8")
    new_block = _lesson_nav_block(lesson_entries)

    if NAV_START in nav_text:
        # Sentinels already present — replace between them
        nav_text = re.sub(
            rf"{re.escape(NAV_START)}.*?{re.escape(NAV_END)}",
            new_block,
            nav_text,
            flags=re.DOTALL,
        )
    else:
        # First run: lesson entries exist but have no sentinels yet.
        # They live between "- Home: ..." and the first non-lesson top-level entry.
        home_m = re.search(r"^- Home:.*\n", nav_text, re.MULTILINE)
        end_m = re.search(
            r"^(?:# <COURSES>|- Notebooks:|- Reports:|- API Reference:)",
            nav_text,
            re.MULTILINE,
        )
        if home_m and end_m and home_m.end() < end_m.start():
            nav_text = (
                nav_text[: home_m.end()]
                + new_block + "\n"
                + nav_text[end_m.start():]
            )
        else:
            nav_text = nav_text.rstrip() + "\n" + new_block + "\n"

    _NAV_PATH.write_text(nav_text, encoding="utf-8")
    print(f"  Updated {_NAV_PATH.name}")


# ── Main ──────────────────────────────────────────────────────────────────────


def main() -> None:
    print("Building mkdocs_src/lessons/ ...")
    (_MKDOCS_SRC / "lessons").mkdir(parents=True, exist_ok=True)
    lesson_entries = build_all()
    update_nav(lesson_entries)
    print("Done.")


if __name__ == "__main__":
    main()
