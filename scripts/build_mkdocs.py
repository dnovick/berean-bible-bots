"""Build the MkDocs docs/ source tree from data/lessons/.

Copies all lesson Markdown files into mkdocs_src/lessons/<lang>/<ch>/,
generates per-chapter index pages that inline the interactive HTML exercises
directly (no iframe), and writes the nav structure to mkdocs_nav.yml for
inclusion in mkdocs.yml.

Run before `mkdocs build`:
    python scripts/build_mkdocs.py
"""

import re
import shutil
from pathlib import Path

REPO = Path(__file__).parent.parent
LESSONS = REPO / "data" / "lessons"
MKDOCS_SRC = REPO / "mkdocs_src"


def _strip_tags(html: str) -> str:
    """Remove all HTML tags and collapse whitespace."""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


def _readme_description(readme_path: Path) -> str:
    """Extract the description paragraph(s) from an exercise README.md.

    Returns the text between the first heading and the first ## section,
    skipping the subtitle italic line and the --- rule.
    """
    if not readme_path.exists():
        return ""
    text = readme_path.read_text(encoding="utf-8")
    # Drop the h1 title line
    text = re.sub(r"^#[^#][^\n]*\n", "", text).strip()
    # Drop a leading italic subtitle (*…*)
    text = re.sub(r"^\*[^\n]*\*\n+", "", text).strip()
    # Drop a leading ---
    text = re.sub(r"^---\n+", "", text).strip()
    # Drop ## Description heading if present
    text = re.sub(r"^## Description\n+", "", text, flags=re.IGNORECASE).strip()
    # Take only up to the next ## section or ---
    m = re.search(r"\n##|^---", text, re.MULTILINE)
    desc = text[: m.start()].strip() if m else text.strip()
    # Drop any remaining markdown headings
    desc = re.sub(r"^#{1,3}[^\n]*\n", "", desc, flags=re.MULTILINE).strip()
    # Drop bold metadata lines like **Chapter:** … **Type:** … **Items:** …
    desc = re.sub(r"^\*\*\w[^*]*:\*\*[^\n]*\n?", "", desc, flags=re.MULTILINE).strip()
    return desc


def _readme_coverage_table(readme_path: Path) -> str:
    """Extract the first markdown table from the README as a fenced block."""
    if not readme_path.exists():
        return ""
    text = readme_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    table_lines: list[str] = []
    in_table = False
    for line in lines:
        if line.startswith("|"):
            in_table = True
            table_lines.append(line)
        elif in_table:
            break
    return "\n".join(table_lines) if table_lines else ""


def _sample_qas(html_path: Path, n: int = 3) -> list[tuple[str, str]]:
    """Extract up to n (question, answer) text pairs from an exercise HTML.

    Handles two patterns:
    - Static rows: pairs of a data row followed by an .ans-row / .answer-row
    - JS data array: const items = [ { form, tense, …, trans }, … ]
    """
    if not html_path.exists():
        return []
    text = html_path.read_text(encoding="utf-8")

    # ── JS items[] pattern (Greek parsing drills) ──────────────────────────
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
            answer_parts = []
            for k in ("tense", "voice", "mood", "person", "number",
                      "aug", "lexical", "trans"):
                if k in fields:
                    answer_parts.append(fields[k])
            a = " · ".join(answer_parts)
            if q and a:
                pairs.append((q, a))
            if len(pairs) >= n:
                break
        return pairs

    # ── Static HTML row pattern ─────────────────────────────────────────────
    # Find each question row that is immediately followed by an answer row.
    # Question rows contain an input/select (no answer text yet).
    # Answer rows have class ans-row or answer-row.
    ans_pattern = re.compile(
        r'<tr[^>]*class="[^"]*(?:ans-row|answer-row)[^"]*"[^>]*>(.*?)</tr>',
        re.DOTALL | re.IGNORECASE,
    )
    # Split on answer rows to find their preceding question rows
    parts = ans_pattern.split(text)
    # parts alternates: [pre_html, ans_content, pre_html, ans_content, …]
    pairs = []
    for i in range(1, len(parts), 2):
        ans_html = parts[i]
        pre_html = parts[i - 1]
        # The question row is the last <tr> before this answer row
        q_rows = re.findall(r"<tr[^>]*>(.*?)</tr>", pre_html, re.DOTALL)
        if not q_rows:
            continue
        q_text = _strip_tags(q_rows[-1])
        a_text = _strip_tags(ans_html)
        # Skip header rows (no digits in question)
        if not re.search(r"\d", q_text):
            continue
        # Clean up — remove placeholder text and button labels
        q_text = re.sub(
            r"(▶ Answer|▼ Hide|כתוב\.\.\.|parse\.\.\.|—)", "", q_text
        ).strip()
        q_text = re.sub(r"\s+", " ", q_text).strip()
        a_text = re.sub(r"\s+", " ", a_text).strip()
        if q_text and a_text:
            pairs.append((q_text, a_text))
        if len(pairs) >= n:
            break
    return pairs


def _build_exercise_page(
    ex_src: Path,
    ex_dst: Path,
    ex_title: str,
    ch_num: int,
    ch_title: str,
    html_name: str,
    md_name: str,
    pdf_name: str,
    has_md: bool,
    has_pdf: bool,
) -> str:
    """Build a clean exercise landing page: description, coverage table,
    sample Q&A, and download buttons.  Returns the page markdown string.
    """
    readme = ex_src / "README.md"
    html_path = ex_src / html_name

    description = _readme_description(readme)
    coverage = _readme_coverage_table(readme)
    samples = _sample_qas(html_path, n=3)

    # ── Download buttons ─────────────────────────────────────────────────────
    btn_parts = [f"[Full Screen (Interactive)]({html_name}){{.md-button .md-button--primary}}"]
    if has_pdf:
        btn_parts.append(f"[Print / PDF]({pdf_name}){{.md-button}}")
    if has_md:
        btn_parts.append(f"[Markdown]({md_name}){{.md-button}}")
    buttons_line = "  ".join(btn_parts)

    lines: list[str] = [
        f"# {ex_title}",
        "",
        f"*Chapter {ch_num} — {ch_title}*",
        "",
        buttons_line,
        "",
    ]

    # ── Description ─────────────────────────────────────────────────────────
    if description:
        lines += [description, ""]

    # ── Coverage table ───────────────────────────────────────────────────────
    if coverage:
        lines += ["## Coverage", "", coverage, ""]

    # ── Sample questions ─────────────────────────────────────────────────────
    if samples:
        lines += ["## Sample Questions", ""]
        for i, (q, a) in enumerate(samples, 1):
            lines.append(f"**Q{i}.** {q}")
            lines.append(f"> **A:** {a}")
            lines.append("")

    return "\n".join(lines)


BBH_TITLES = {
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

BBG_TITLES = {
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

BBA_TITLES = {
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

COURSES = [
    ("hebrew", "bbh", "Biblical Hebrew (BBH)", BBH_TITLES),
    ("greek", "bbg", "Biblical Greek (BBG)", BBG_TITLES),
    ("aramaic", "bba", "Biblical Aramaic (BBA)", BBA_TITLES),
]


def slugify(name: str) -> str:
    """Convert exercise dir name to a readable title."""
    # strip leading chN- prefix
    name = re.sub(r"^ch\d+-", "", name)
    return name.replace("-", " ").title()


def _read_chapter_yml(course: str, ch: str) -> dict:
    """Read data/lessons/{course}/{ch}/chapter.yml; return {} if missing."""
    import yaml as _yaml
    path = LESSONS / course / ch / "chapter.yml"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return _yaml.safe_load(f) or {}


def _deck_short_title(stem: str) -> str:
    """Convert deck file stem to display title.

    Examples: 'ch1-alphabet-deck' → 'Alphabet Deck'
              'ch13-morphology-deck' → 'Morphology Deck'
    """
    name = re.sub(r"^ch\d+-", "", stem)  # strip ch{N}- prefix
    name = re.sub(r"-deck$", "", name)   # strip -deck suffix
    return name.replace("-", " ").title()


def _deck_description(deck_md: Path) -> str:
    """Extract the first italic description line from a deck .md file."""
    if not deck_md.exists():
        return ""
    text = deck_md.read_text(encoding="utf-8")
    m = re.search(r"^\*([^*\n]+)\*", text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def _prepend_deck_download_header(content: str, stem: str) -> str:
    """Prepend Anki / Flashcards Deluxe download links to a deck .md file."""
    txt_name = f"{stem}.txt"
    fd_name = f"{stem}-fd.txt"
    h1_m = re.match(r"(# [^\n]+\n)", content)
    if not h1_m:
        return content
    dl_line = (
        f"\n**Download:** [Anki import (.txt)]({txt_name}) · "
        f"[Flashcards Deluxe (-fd.txt)]({fd_name})\n\n---\n\n"
    )
    # Skip the original --- separator that opens the deck content
    rest = content[h1_m.end():]
    rest = re.sub(r"^\s*---\s*\n+", "", rest)
    return h1_m.group(0) + dl_line + rest


def _inject_lesson_header(
    content: str,
    focus: str,
    has_exercises: bool,
    has_decks: bool,
) -> str:
    """Inject focus blockquote and resource nav table after the H1 heading."""
    h1_m = re.match(r"(# [^\n]+\n)", content)
    if not h1_m:
        return content

    lines: list[str] = [""]

    if focus:
        lines.append(f"> {focus.strip()}")
        lines.append("")

    if has_exercises or has_decks:
        lines += ["| Resource | Link |", "|---|---|"]
        if has_exercises:
            lines.append("| Exercises | [View exercises →](exercises.md) |")
        if has_decks:
            lines.append("| Flashcard Decks | [View decks →](flashcards.md) |")
        lines.append("")

    insert = "\n".join(lines)
    return h1_m.group(0) + insert + content[h1_m.end():]


def _build_exercises_page(
    ch_num: int,
    ch_title: str,
    items: list[dict],
) -> str:
    """Generate exercises.md listing page content."""
    lines = [
        f"# Ch{ch_num} — {ch_title}: Exercises",
        "",
        "[← Back to lesson](index.md)",
        "",
    ]
    if not items:
        lines += ["*No exercises for this chapter.*", ""]
    else:
        lines += ["| Exercise | Description |", "|---|---|"]
        for item in items:
            desc = item.get("desc", "").replace("\n", " ")
            lines.append(f"| [{item['title']}]({item['link']}) | {desc} |")
        lines.append("")
    return "\n".join(lines)


def _build_flashcards_page(
    ch_num: int,
    ch_title: str,
    items: list[dict],
) -> str:
    """Generate flashcards.md listing page content."""
    lines = [
        f"# Ch{ch_num} — {ch_title}: Flashcards",
        "",
        "[← Back to lesson](index.md)",
        "",
    ]
    if not items:
        lines += ["*No flashcard decks for this chapter.*", ""]
    else:
        lines += ["| Deck | Description |", "|---|---|"]
        for item in items:
            desc = item.get("desc", "").replace("\n", " ")
            lines.append(f"| [{item['title']}]({item['md']}) | {desc} |")
        lines.append("")
    return "\n".join(lines)


def sorted_chapters(titles: dict[str, str]) -> list[str]:
    return sorted(titles.keys(), key=lambda x: int(x[2:]))


def build_chapter(
    lang: str,
    course: str,
    ch: str,
    title: str,
    ch_num: int,
) -> list[dict]:
    """Build docs for one chapter. Returns nav entries for this chapter."""
    src_dir = LESSONS / course / ch
    dst_dir = MKDOCS_SRC / "lessons" / lang / ch
    dst_dir.mkdir(parents=True, exist_ok=True)

    # Read chapter.yml for focus description
    ch_meta = _read_chapter_yml(course, ch)
    focus = ch_meta.get("focus", "").strip()

    # ── Exercises ────────────────────────────────────────────────────────────
    exercises_src = src_dir / "exercises"
    exercises_dst = dst_dir / "exercises"
    exercise_items: list[dict] = []

    if exercises_src.is_dir():
        for ex_dir in sorted(exercises_src.iterdir()):
            if not ex_dir.is_dir():
                continue
            ex_name = ex_dir.name
            ex_dst = exercises_dst / ex_name
            ex_dst.mkdir(parents=True, exist_ok=True)

            for md in ex_dir.glob("*.md"):
                shutil.copy(md, ex_dst / md.name)
            for html in ex_dir.glob("*.html"):
                shutil.copy(html, ex_dst / html.name)
            for pdf in ex_dir.glob("*.pdf"):
                shutil.copy(pdf, ex_dst / pdf.name)

            html_files = list(ex_dir.glob("*.html"))
            ex_title = slugify(ex_name)
            ex_desc = _readme_description(ex_dir / "README.md")

            if html_files:
                html_name = html_files[0].name
                stem = html_files[0].stem
                md_name = f"{stem}.md"
                pdf_name = f"{stem}.pdf"
                has_md = (ex_dir / md_name).exists()
                has_pdf = (ex_dir / pdf_name).exists()

                page_content = _build_exercise_page(
                    ex_src=ex_dir,
                    ex_dst=ex_dst,
                    ex_title=ex_title,
                    ch_num=ch_num,
                    ch_title=title,
                    html_name=html_name,
                    md_name=md_name,
                    pdf_name=pdf_name,
                    has_md=has_md,
                    has_pdf=has_pdf,
                )
                (ex_dst / "index.md").write_text(page_content, encoding="utf-8")
                ex_link = f"exercises/{ex_name}/index.md"
            elif (ex_dir / "README.md").exists():
                ex_link = f"exercises/{ex_name}/README.md"
            else:
                continue

            exercise_items.append(
                {"title": ex_title, "link": ex_link, "desc": ex_desc}
            )

    # ── Flashcard decks ───────────────────────────────────────────────────────
    deck_items: list[dict] = []
    for deck_md in sorted(src_dir.glob("*-deck.md")):
        deck_title = _deck_short_title(deck_md.stem)
        deck_desc = _deck_description(deck_md)

        # Copy .md with download header prepended
        content = deck_md.read_text(encoding="utf-8")
        content = _prepend_deck_download_header(content, deck_md.stem)
        (dst_dir / deck_md.name).write_text(content, encoding="utf-8")

        deck_items.append(
            {"title": deck_title, "md": deck_md.name, "desc": deck_desc}
        )

    # Copy deck text files (Anki .txt and Flashcards Deluxe -fd.txt)
    for txt in src_dir.glob("*.txt"):
        shutil.copy(txt, dst_dir / txt.name)

    # Copy paradigm / other .md files (not README, not deck files)
    for md in src_dir.glob("*.md"):
        if md.name == "README.md" or md.name.endswith("-deck.md"):
            continue
        shutil.copy(md, dst_dir / md.name)

    # ── Generated listing pages ───────────────────────────────────────────────
    if exercise_items:
        ex_page = _build_exercises_page(ch_num, title, exercise_items)
        (dst_dir / "exercises.md").write_text(ex_page, encoding="utf-8")

    if deck_items:
        fl_page = _build_flashcards_page(ch_num, title, deck_items)
        (dst_dir / "flashcards.md").write_text(fl_page, encoding="utf-8")

    # ── index.md from README.md ───────────────────────────────────────────────
    readme = src_dir / "README.md"
    if readme.exists():
        content = readme.read_text(encoding="utf-8")
        content = re.sub(
            r"(exercises/[^)]+/)README\.md",
            r"\1index.md",
            content,
        )
        content = re.sub(
            r"\((exercises/[^)]+/)\)",
            r"(\1index.md)",
            content,
        )
        content = _inject_lesson_header(
            content, focus,
            has_exercises=bool(exercise_items),
            has_decks=bool(deck_items),
        )
        (dst_dir / "index.md").write_text(content, encoding="utf-8")

    # ── Nav (3 items: Lesson / Exercises / Flashcards) ────────────────────────
    ch_nav: list = [{"Lesson": f"lessons/{lang}/{ch}/index.md"}]
    if exercise_items:
        ch_nav.append({"Exercises": f"lessons/{lang}/{ch}/exercises.md"})
    if deck_items:
        ch_nav.append({"Flashcards": f"lessons/{lang}/{ch}/flashcards.md"})

    return [{f"Ch{ch_num} — {title}": ch_nav}]


NOTEBOOK_SECTIONS = [
    ("Getting Started", [
        ("Introduction", [
            ("tutorial/getting_started.ipynb", "Getting Started"),
        ]),
    ]),
    ("Old Testament (Hebrew)", [
        ("Verb Stems", [
            ("ot/verbs/stem_overview.ipynb", "Stem Overview"),
            ("ot/verbs/qal.ipynb", "Qal"),
            ("ot/verbs/niphal.ipynb", "Niphal"),
            ("ot/verbs/hiphil.ipynb", "Hiphil"),
            ("ot/verbs/hophal.ipynb", "Hophal"),
            ("ot/verbs/piel.ipynb", "Piel"),
            ("ot/verbs/pual.ipynb", "Pual"),
            ("ot/verbs/hithpael.ipynb", "Hithpael"),
        ]),
        ("Noun Morphology", [
            ("ot/nouns/ot_nouns.ipynb", "OT Nouns"),
            ("ot/numbers/ot_numbers.ipynb", "OT Numbers"),
        ]),
        ("Syntax & Verbal Analysis", [
            ("ot/syntax/verbal_syntax.ipynb", "Verbal Syntax"),
            ("ot/syntax/poetry.ipynb", "Poetry"),
            ("ot/syntax/predicate_argument.ipynb", "Predicate-Argument"),
            ("ot/syntax/discourse_structure.ipynb", "Discourse Structure"),
            ("ot/syntax/register_analysis.ipynb", "Register Analysis"),
            ("ot/syntax/information_structure.ipynb", "Information Structure"),
            ("ot/syntax/prepositions.ipynb", "Prepositions"),
        ]),
        ("Speaker & Role Analysis", [
            ("ot/speakers/speaker_attribution.ipynb", "Speaker Attribution"),
            ("ot/speakers/syntactic_roles_ot.ipynb", "Syntactic Roles"),
            ("ot/speakers/participant_tracking.ipynb", "Participant Tracking"),
            ("ot/speakers/speech_acts.ipynb", "Speech Acts"),
        ]),
        ("Lexicon", [
            ("ot/lexicon/hapax_legomena.ipynb", "Hapax Legomena"),
        ]),
        ("Semantic Domains", [
            ("ot/semantic_domains/ot_semantic_domains.ipynb", "Semantic Domains"),
        ]),
        ("Aramaic", [
            ("ot/aramaic/aramaic_overview.ipynb", "Aramaic Overview"),
            ("ot/aramaic/aramaic_nominal.ipynb", "Aramaic Nominal"),
        ]),
        ("Targumim", [
            ("ot/targumim/targumim_overview.ipynb", "Targumim Overview"),
        ]),
    ]),
    ("New Testament (Greek)", [
        ("Verb Morphology", [
            ("nt/verbs/nt_verbs.ipynb", "NT Verbs"),
        ]),
        ("Noun Morphology", [
            ("nt/nouns/nt_nouns.ipynb", "NT Nouns"),
        ]),
        ("Syntax & Roles", [
            ("nt/syntax/syntactic_roles_nt.ipynb", "Syntactic Roles"),
            ("nt/syntax/participles.ipynb", "Participles"),
            ("nt/syntax/mood_usage.ipynb", "Mood Usage"),
            ("nt/syntax/demonstratives.ipynb", "Demonstratives"),
            ("nt/syntax/coreference.ipynb", "Coreference"),
            ("nt/syntax/style_analysis.ipynb", "Style Analysis"),
            ("nt/syntax/information_structure.ipynb", "Information Structure"),
            ("nt/syntax/speech_acts.ipynb", "Speech Acts"),
            ("nt/syntax/louw_nida_domains.ipynb", "Louw-Nida Domains"),
            ("nt/syntax/prepositions.ipynb", "Prepositions"),
        ]),
        ("Discourse", [
            ("nt/discourse/discourse_particles.ipynb", "Discourse Particles"),
        ]),
        ("Peshitta NT (Syriac)", [
            ("nt/peshitta/peshitta_morphology.ipynb", "Peshitta Morphology"),
        ]),
    ]),
    ("Cross-Testament", [
        ("Survey", [
            ("both/survey/data_exploration.ipynb", "Data Exploration"),
            ("both/survey/book_profiles.ipynb", "Book Profiles"),
            ("both/survey/christological_titles.ipynb", "Christological Titles"),
            ("both/survey/divine_names.ipynb", "Divine Names"),
            ("both/survey/genre_compare.ipynb", "Genre Comparison"),
        ]),
        ("Lexicon", [
            ("both/lexicon/word_study.ipynb", "Word Study"),
            ("both/lexicon/concordance.ipynb", "Concordance"),
            ("both/lexicon/language_analysis.ipynb", "Language Analysis"),
            ("both/lexicon/morph_distribution.ipynb", "Morphological Distribution"),
            ("both/lexicon/collocation_and_phrase.ipynb", "Collocation & Phrase"),
            ("both/lexicon/formulaic_language.ipynb", "Formulaic Language"),
        ]),
        ("Intertextuality", [
            ("both/intertextuality/lxx_analysis.ipynb", "LXX Analysis"),
            ("both/intertextuality/theological_trajectories.ipynb", "Theological Trajectories"),
            ("both/intertextuality/nt_quotations.ipynb", "NT Quotations"),
            ("both/intertextuality/parallel_passage.ipynb", "Parallel Passages"),
        ]),
    ]),
    ("Developer / Infrastructure", [
        ("Reference", [
            ("dev/data_pipeline.ipynb", "Data Pipeline"),
            ("dev/export_and_profiles.ipynb", "Export & Profiles"),
            ("dev/morphology_codes.ipynb", "Morphology Codes"),
        ]),
    ]),
]


_NOTEBOOKS_INDEX = """\
# Notebooks

Interactive analysis notebooks covering the full `bible_grammar` toolkit \
— Hebrew OT, Greek NT, Septuagint, Peshitta, and Targumim.

Each notebook below is rendered statically with its outputs. \
Click the **Open in Colab** badge on any notebook page to run it interactively \
in Google Colab — no local installation required.

!!! tip "New to Jupyter or this project?"
    Start with the [**Getting Started**](tutorial/getting_started.ipynb) notebook —
    it walks through running cells, filtering the dataset, and generating charts,
    no prior Python experience needed.

## Running in Google Colab

Click the **Open in Colab** badge at the top of any notebook page. \
On first run, execute the **Colab setup** cell (cell 2), which will:

1. Clone the repository into `/content/berean-bible-bots`
2. Install Python dependencies from `notebook-setup/requirements.txt`
3. Download the processed data files (~295 MB) from `bereanbiblebots.com/data/`

Subsequent cells run normally once the setup cell completes \
(~2–3 minutes on first run; data is cached for the session).

## Running Locally

To execute notebooks on your own machine:

```bash
git clone https://github.com/dnovick/berean-bible-bots.git
cd berean-bible-bots
python -m venv .venv && source .venv/bin/activate
pip install -r notebook-setup/requirements.txt
# Download processed data (one-time, ~295 MB)
bash notebook-setup/postBuild
jupyter lab
```

Then open any notebook from the `notebooks/` directory.
"""


def build_notebooks() -> list:
    """Copy notebooks into mkdocs_src and return nav entries."""
    nb_src = REPO / "notebooks"
    nb_dst = MKDOCS_SRC / "notebooks"

    # Clean and recreate
    if nb_dst.exists():
        shutil.rmtree(nb_dst)
    nb_dst.mkdir(parents=True)

    (nb_dst / "index.md").write_text(_NOTEBOOKS_INDEX, encoding="utf-8")

    nav_entries: list = [{"Overview": "notebooks/index.md"}]

    for corpus_label, sections in NOTEBOOK_SECTIONS:
        corpus_entries: list = []
        for section_label, notebooks in sections:
            section_entries = []
            for nb_rel, nb_title in notebooks:
                src = nb_src / nb_rel
                if not src.exists():
                    continue
                dst_path = nb_dst / nb_rel
                dst_path.parent.mkdir(parents=True, exist_ok=True)

                shutil.copy(src, dst_path)
                section_entries.append(
                    {nb_title: f"notebooks/{nb_rel}"}
                )
            if section_entries:
                corpus_entries.append({section_label: section_entries})
        if corpus_entries:
            nav_entries.append({corpus_label: corpus_entries})

    return [{"Notebooks": nav_entries}]


# ── Reports ───────────────────────────────────────────────────────────────────

# Section labels and their output/reports/ subdirectory names.
# Each entry is (nav_label, subdir_under_reports).
REPORT_SECTIONS = [
    ("Old Testament (Hebrew)", "ot"),
    ("New Testament (Greek)", "nt"),
    ("Cross-Testament", "both"),
]


def _rewrite_chart_paths(content: str, depth: int) -> str:
    """Rewrite ../../../charts/... relative paths to MkDocs-relative paths.

    Reports reference charts as e.g. ../../../charts/nt/verbs/foo.png
    (relative from output/reports/nt/verbs/).  In mkdocs_src the charts
    live at reports/charts/nt/verbs/foo.png, so we replace the ../..
    prefix with the correct relative path based on how deep the file is.
    """
    # Replace any number of ../ followed by charts/ with the right prefix
    prefix = "../" * depth + "charts/"
    return re.sub(r"(?:\.\./)+charts/", prefix, content)


def _build_report_dir(
    src_dir: Path,
    dst_dir: Path,
    depth: int,
    nav_entries: list,
    label: str,
) -> None:
    """Recursively copy one reports subdirectory into mkdocs_src/reports/."""
    dst_dir.mkdir(parents=True, exist_ok=True)

    readme = src_dir / "README.md"

    # Copy individual .md reports (not README; skip index.md when README exists
    # since README will be written as index.md for multi-content dirs)
    _skip = {"README.md"} | ({"index.md"} if readme.exists() else set())
    md_files = sorted(f for f in src_dir.glob("*.md") if f.name not in _skip)
    for md in md_files:
        content = md.read_text(encoding="utf-8")
        content = _rewrite_chart_paths(content, depth)
        content = re.sub(r"\(([^)]+/)README\.md\)", r"(\1index.md)", content)
        (dst_dir / md.name).write_text(content, encoding="utf-8")

    # Copy non-md assets (.csv, .png, .pdf, etc.)
    for f in src_dir.iterdir():
        if f.is_file() and f.suffix not in (".md",):
            shutil.copy(f, dst_dir / f.name)

    # Recurse into subdirectories
    for sub in sorted(d for d in src_dir.iterdir() if d.is_dir()):
        sub_dst = dst_dir / sub.name
        sub_entries: list = []
        _build_report_dir(sub, sub_dst, depth + 1, sub_entries, sub.name)
        if sub_entries:
            # If the subdirectory produced exactly one direct link whose title
            # is NOT "Overview" (i.e. it's a real report link, not a landing-page
            # placeholder), promote it to the parent level without a wrapper group.
            # This avoids the "expand section → click link" two-click pattern.
            sole = (
                len(sub_entries) == 1 and
                isinstance(list(sub_entries[0].values())[0], str) and
                list(sub_entries[0].keys())[0] != "Overview"
            )
            if sole:
                nav_entries.append(sub_entries[0])
            else:
                # Use README H1 title if available, else capitalise dir name
                sub_readme = sub / "README.md"
                if sub_readme.exists():
                    sub_label = _md_title(sub_dst / "index.md") or \
                        sub.name.replace("-", " ").replace("_", " ").title()
                else:
                    sub_label = sub.name.replace("-", " ").replace("_", " ").title()
                nav_entries.append({sub_label: sub_entries})

    # Determine whether to add nav entries for .md files and/or an Overview.
    #
    # Case 1 — No README: add each .md file as its own nav entry.
    # Case 2 — README + exactly one report .md + no subdirectory entries:
    #   Skip the Overview entirely — no index.md is written for this dir.
    #   The report .md IS the sole page; its own H1 becomes the nav label.
    #   This prevents search engines from indexing a thin landing page.
    # Case 3 — README alone (no other .md, no sub-entries):
    #   The README index IS the single destination; link to it directly.
    # Case 4 — README + multiple .md files or subdirectory entries:
    #   Write README as index.md, add an Overview entry, suppress bare .md files
    #   (they are linked from the Overview page).
    index_src = src_dir / "index.md"
    is_single_file_report = (
        readme.exists() and
        len(md_files) == 1 and
        not any(True for _ in nav_entries)
    )
    is_readme_only = (
        readme.exists() and
        len(md_files) == 0 and
        not any(True for _ in nav_entries)
    )

    # Write README → index.md only for dirs that need a landing page (Cases 3 & 4).
    # Single-file report dirs (Case 2) get no index.md so no defunct page exists.
    if readme.exists() and not is_single_file_report:
        content = readme.read_text(encoding="utf-8")
        content = _rewrite_chart_paths(content, depth)
        content = re.sub(r"\(([^)]+/)README\.md\)", r"(\1index.md)", content)
        (dst_dir / "index.md").write_text(content, encoding="utf-8")

    if not readme.exists():
        # Case 1: no README — add all .md files directly
        for md in md_files:
            title = _md_title(dst_dir / md.name)
            rel = str((dst_dir / md.name).relative_to(MKDOCS_SRC))
            nav_entries.append({title: rel})
    elif is_single_file_report:
        # Case 2: README + single report .md — link report directly using its H1
        report_title = _md_title(dst_dir / md_files[0].name) or label
        rel = str((dst_dir / md_files[0].name).relative_to(MKDOCS_SRC))
        nav_entries.append({report_title: rel})
    elif is_readme_only:
        # Case 3: README-only directory — the README index IS the single destination
        readme_title = _md_title(dst_dir / "index.md") or label
        rel = str((dst_dir / "index.md").relative_to(MKDOCS_SRC))
        nav_entries.append({readme_title: rel})
    else:
        # Case 4: README + multiple .md files and/or subdirectory entries.
        # Sub-dir entries are already in nav_entries. Also add each flat .md
        # file so every report is reachable directly from the nav (not just
        # via the Overview landing page).
        for md in md_files:
            title = _md_title(dst_dir / md.name)
            rel = str((dst_dir / md.name).relative_to(MKDOCS_SRC))
            nav_entries.append({title: rel})

    # Add index.md as first nav entry for Case 4 only
    if not is_single_file_report and not is_readme_only and (
            readme.exists() or index_src.exists()):
        if not readme.exists() and index_src.exists():
            pass  # already copied above via md_files
        rel_index = str((dst_dir / "index.md").relative_to(MKDOCS_SRC))
        # Remove any existing "Overview" entry to avoid duplication, then insert
        nav_entries[:] = [e for e in nav_entries if list(e.keys())[0] != "Overview"
                          and list(e.values())[0] != rel_index]
        nav_entries.insert(0, {"Overview": rel_index})


def _md_title(path: Path) -> str:
    """Extract the first # heading from a markdown file as its nav title."""
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    except OSError:
        pass
    return path.stem.replace("-", " ").replace("_", " ").title()


def build_reports() -> list:
    """Copy output/reports/ into mkdocs_src/reports/ and return nav entries."""
    reports_src = REPO / "output" / "reports"
    charts_src = REPO / "output" / "charts"
    reports_dst = MKDOCS_SRC / "reports"

    # Clean and recreate
    if reports_dst.exists():
        shutil.rmtree(reports_dst)
    reports_dst.mkdir(parents=True)

    # Copy charts tree alongside reports so relative paths resolve correctly.
    # Remove any README.md files inside charts/ — they're not web pages.
    charts_dst = reports_dst / "charts"
    if charts_src.exists():
        shutil.copytree(charts_src, charts_dst)
        for readme in charts_dst.rglob("README.md"):
            readme.unlink()

    # Landing page = output/reports/README.md
    top_readme = reports_src / "README.md"
    if top_readme.exists():
        content = top_readme.read_text(encoding="utf-8")
        content = _rewrite_chart_paths(content, 1)
        content = re.sub(r"\(([^)]+/)README\.md\)", r"(\1index.md)", content)
        (reports_dst / "index.md").write_text(content, encoding="utf-8")

    nav_entries: list = [{"Overview": "reports/index.md"}]

    for section_label, subdir in REPORT_SECTIONS:
        src = reports_src / subdir
        if not src.is_dir():
            continue
        dst = reports_dst / subdir
        section_entries: list = []
        _build_report_dir(src, dst, depth=1, nav_entries=section_entries, label=subdir)
        if section_entries:
            nav_entries.append({section_label: section_entries})

    return [{"Reports": nav_entries}]


STUDY_HELPS_SECTIONS = [
    ("New Testament", "nt"),
]


def build_study_helps() -> list:
    """Copy output/study-helps/ into mkdocs_src/study-helps/ and return nav entries."""
    src_root = REPO / "output" / "study-helps"
    dst_root = MKDOCS_SRC / "study-helps"

    if dst_root.exists():
        shutil.rmtree(dst_root)
    dst_root.mkdir(parents=True)

    top_readme = src_root / "README.md"
    if top_readme.exists():
        content = top_readme.read_text(encoding="utf-8")
        content = re.sub(r"\(([^)]+/)README\.md\)", r"(\1index.md)", content)
        (dst_root / "index.md").write_text(content, encoding="utf-8")

    nav_entries: list = [{"Overview": "study-helps/index.md"}]

    for section_label, subdir in STUDY_HELPS_SECTIONS:
        src = src_root / subdir
        if not src.is_dir():
            continue
        dst = dst_root / subdir
        section_entries: list = []
        _build_report_dir(src, dst, depth=1, nav_entries=section_entries, label=subdir)
        if section_entries:
            nav_entries.append({section_label: section_entries})

    return [{"Study Helps": nav_entries}]


def build_additional_resources_nav() -> list:
    """Copy data/lessons/bbh/additional-resources/ into mkdocs_src
    and return nav entries for embedding inside the BBH course section."""
    src = LESSONS / "bbh" / "additional-resources"
    dst = MKDOCS_SRC / "lessons" / "hebrew" / "additional-resources"
    if not src.exists():
        return []

    dst.mkdir(parents=True, exist_ok=True)
    nav_entries: list = []
    _build_report_dir(src, dst, depth=3, nav_entries=nav_entries,
                      label="Additional Resources")
    return [{"Additional Resources": nav_entries}] if nav_entries else []


def build_course(lang: str, course: str, label: str, titles: dict[str, str]) -> list:
    """Build all chapters for a course. Returns nav entries."""
    nav_entries = []
    nav_entries.append({"Overview": f"lessons/{lang}/index.md"})
    for ch in sorted_chapters(titles):
        ch_num = int(ch[2:])
        title = titles[ch]
        src = LESSONS / course / ch
        if not src.is_dir():
            continue
        nav_entries.extend(build_chapter(lang, course, ch, title, ch_num))
    # Append Additional Resources at the end of BBH only
    if lang == "hebrew" and course == "bbh":
        nav_entries.extend(build_additional_resources_nav())
    return [{label: nav_entries}]


def build_courses_nav() -> list:
    """Read data/courses/ YAMLs and return nav entries for the Courses section."""
    import yaml as _yaml
    courses_data_dir = REPO / "data" / "courses"
    if not courses_data_dir.is_dir():
        return []

    textbook_short = {
        "Basics of Biblical Hebrew": "BBH",
        "Basics of Biblical Greek": "BBG",
        "Basics of Biblical Aramaic": "BBA",
    }

    def _load_course(course_dir: Path) -> dict:
        yml = course_dir / "course.yml"
        with open(yml) as f:
            data = _yaml.safe_load(f)
        sessions: list[dict] = []
        for session_dir in sorted(
            d for d in course_dir.iterdir()
            if d.is_dir() and d.name.startswith("session-")
        ):
            syml = session_dir / "session.yml"
            if not syml.exists():
                continue
            with open(syml) as f:
                session = _yaml.safe_load(f) or {}
            if "number" not in session:
                try:
                    session["number"] = int(session_dir.name.split("-", 1)[1])
                except (IndexError, ValueError):
                    session["number"] = len(sessions) + 1
            session["_dir"] = session_dir.name
            sessions.append(session)
        data["sessions"] = sessions
        return data

    courses = []
    for entry in sorted(courses_data_dir.iterdir()):
        if not entry.is_dir():
            continue
        if (entry / "course.yml").exists():
            courses.append(_load_course(entry))
        else:
            for course_dir in sorted(entry.iterdir()):
                if course_dir.is_dir() and (course_dir / "course.yml").exists():
                    courses.append(_load_course(course_dir))

    if not courses:
        return []

    group_labels = {
        "bbh": "Biblical Hebrew - Year 1",
        "bbg": "Biblical Greek",
        "bba": "Biblical Aramaic",
    }

    by_group: dict = {}
    for course in courses:
        tb = course.get("textbook", "Other")
        short = textbook_short.get(tb, "other").lower()
        by_group.setdefault(short, []).append(course)

    nav_entries: list = [{"Overview": "courses/index.md"}]
    for group, group_courses in by_group.items():
        label = group_labels.get(group, group.upper())
        group_entries: list = [
            {"Overview": f"courses/{group}/index.md"},
            {"Student Resources": f"courses/{group}/common/student-resources.md"},
        ]
        for course in group_courses:
            cid = course["id"]
            course_entries: list = [{"Overview": f"courses/{group}/{cid}/index.md"}]
            sessions = course.get("sessions", [])
            if sessions:
                session_entries = []
                for session in sessions:
                    num = session.get("number", "")
                    focus = session.get("focus", "")
                    fname = f"{session.get('_dir', f'session-{num:02d}')}.md"
                    session_entries.append(
                        {f"Session {num} — {focus}":
                         f"courses/{group}/{cid}/sessions/{fname}"}
                    )
                course_entries.append({"Sessions": session_entries})
            group_entries.append({cid: course_entries})
        nav_entries.append({label: group_entries})

    return [{"Courses": nav_entries}]


def build_nav() -> list:
    nav: list = [{"Home": "index.md"}]
    for lang, course, label, titles in COURSES:
        nav.extend(build_course(lang, course, label, titles))
    nav.extend(build_notebooks())
    nav.extend(build_reports())
    nav.extend(build_courses_nav())
    nav.extend(build_study_helps())
    nav.append({"API Reference": "reference/index.md"})
    return nav


def write_nav_yml(nav: list) -> None:
    """Serialize nav list to YAML and write mkdocs_nav.yml."""
    import yaml
    out = REPO / "mkdocs_nav.yml"
    out.write_text(yaml.dump({"nav": nav}, allow_unicode=True, sort_keys=False))
    print(f"Wrote {out}")


def build_api_reference() -> None:
    ref_dir = MKDOCS_SRC / "reference"
    ref_dir.mkdir(exist_ok=True)

    # Copy existing docs/features.md as the narrative API reference
    features = REPO / "docs" / "features.md"
    if features.exists():
        shutil.copy(features, ref_dir / "features.md")

    index = ref_dir / "index.md"
    index.write_text(
        "# API Reference\n\n"
        "## Query API — Narrative Guide\n\n"
        "See [Features & Code Examples](features.md) for the full query API "
        "with worked examples.\n\n"
        "## Module Reference\n\n"
        "::: bible_grammar\n"
        "    options:\n"
        "      show_root_heading: true\n"
        "      show_submodules: true\n",
        encoding="utf-8",
    )


def main() -> None:
    print("Building MkDocs source tree...")

    # Clean generated chapter dirs (not hand-authored index pages)
    for lang, _, _, titles in COURSES:
        lang_dir = MKDOCS_SRC / "lessons" / lang
        for ch in sorted_chapters(titles):
            ch_dir = lang_dir / ch
            if ch_dir.exists():
                shutil.rmtree(ch_dir)

    # Clean generated reports, study-helps, and additional-resources dirs
    for clean_dir in ("reports", "study-helps"):
        d = MKDOCS_SRC / clean_dir
        if d.exists():
            shutil.rmtree(d)
    # additional-resources now lives inside lessons/hebrew/ (part of BBH section)
    ar = MKDOCS_SRC / "lessons" / "hebrew" / "additional-resources"
    if ar.exists():
        shutil.rmtree(ar)
    # Clean old top-level location if it exists from previous build
    old_ar = MKDOCS_SRC / "lessons" / "additional-resources"
    if old_ar.exists():
        shutil.rmtree(old_ar)

    build_api_reference()
    nav = build_nav()
    write_nav_yml(nav)

    total = sum(
        1
        for lang, course, _, titles in COURSES
        for ch in sorted_chapters(titles)
        if (LESSONS / course / ch).is_dir()
    )
    print(f"Processed {total} chapters across {len(COURSES)} courses.")
    print("Done. Run: mkdocs build")


if __name__ == "__main__":
    main()
