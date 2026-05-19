"""Build the MkDocs docs/ source tree from output/lessons/.

Copies all lesson Markdown files into mkdocs_src/lessons/<lang>/<ch>/,
generates per-chapter index pages that embed the interactive HTML exercises
via iframes, and writes the nav structure to mkdocs_nav.yml for inclusion
in mkdocs.yml.

Run before `mkdocs build`:
    python scripts/build_mkdocs.py
"""

import re
import shutil
from pathlib import Path

REPO = Path(__file__).parent.parent
LESSONS = REPO / "output" / "lessons"
MKDOCS_SRC = REPO / "mkdocs_src"

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
    src_dir = LESSONS / lang / course / ch
    dst_dir = MKDOCS_SRC / "lessons" / lang / ch
    dst_dir.mkdir(parents=True, exist_ok=True)

    # Copy README.md → index.md, rewriting exercise links to point at index.md
    readme = src_dir / "README.md"
    if readme.exists():
        content = readme.read_text(encoding="utf-8")
        # Rewrite  exercises/<name>/README.md  →  exercises/<name>/index.md
        content = re.sub(
            r"(exercises/[^)]+/)README\.md",
            r"\1index.md",
            content,
        )
        # Rewrite bare  exercises/<name>/  →  exercises/<name>/index.md
        # (bare directory links with no explicit file)
        content = re.sub(
            r"\((exercises/[^)]+/)\)",
            r"(\1index.md)",
            content,
        )
        (dst_dir / "index.md").write_text(content, encoding="utf-8")

    # Copy paradigm / other .md files (not README, not deck files)
    for md in src_dir.glob("*.md"):
        if md.name == "README.md":
            continue
        if "-deck" in md.name:
            continue
        shutil.copy(md, dst_dir / md.name)

    # Copy exercises
    exercises_src = src_dir / "exercises"
    exercises_dst = dst_dir / "exercises"
    exercise_entries = []

    if exercises_src.is_dir():
        for ex_dir in sorted(exercises_src.iterdir()):
            if not ex_dir.is_dir():
                continue
            ex_name = ex_dir.name
            ex_dst = exercises_dst / ex_name
            ex_dst.mkdir(parents=True, exist_ok=True)

            # Copy .md, .html, and .pdf files
            for md in ex_dir.glob("*.md"):
                shutil.copy(md, ex_dst / md.name)
            for html in ex_dir.glob("*.html"):
                shutil.copy(html, ex_dst / html.name)
            for pdf in ex_dir.glob("*.pdf"):
                shutil.copy(pdf, ex_dst / pdf.name)

            # Build exercise page: embed HTML via iframe if .html exists,
            # else redirect to the .md
            html_files = list(ex_dir.glob("*.html"))
            md_file = ex_dst / "README.md"
            ex_title = slugify(ex_name)

            if html_files:
                html_name = html_files[0].name
                stem = html_files[0].stem  # e.g. ch26-function-sort
                md_name = f"{stem}.md"
                pdf_name = f"{stem}.pdf"
                has_md = (ex_dir / md_name).exists()
                has_pdf = (ex_dir / pdf_name).exists()

                # Build download links line (web-only — injected here, not in source)
                download_parts = [f"[Full screen]({html_name}){{.md-button}}"]
                if has_md:
                    download_parts.append(f"[Answer key (MD)]({md_name}){{.md-button}}")
                if has_pdf:
                    download_parts.append(f"[Print (PDF)]({pdf_name}){{.md-button}}")
                downloads_line = "  ".join(download_parts)

                iframe_md = ex_dst / "index.md"
                iframe_md.write_text(
                    f"# {ex_title}\n\n"
                    f"*Chapter {ch_num} — {title}*\n\n"
                    f"{downloads_line}\n\n"
                    f'<iframe src="{html_name}" '
                    f'style="width:100%;height:85vh;border:1px solid #ddd;'
                    f'border-radius:6px;" '
                    f'title="{ex_title}"></iframe>\n',
                    encoding="utf-8",
                )
                exercise_entries.append(
                    {ex_title: f"lessons/{lang}/{ch}/exercises/{ex_name}/index.md"}
                )
            elif md_file.exists():
                exercise_entries.append(
                    {ex_title: f"lessons/{lang}/{ch}/exercises/{ex_name}/README.md"}
                )

    # Build chapter nav entry
    ch_nav: list = [{"Lesson": f"lessons/{lang}/{ch}/index.md"}]
    if exercise_entries:
        ch_nav.append({"Exercises": exercise_entries})

    return [{f"Ch{ch_num} — {title}": ch_nav}]


def build_course(lang: str, course: str, label: str, titles: dict[str, str]) -> list:
    """Build all chapters for a course. Returns nav entries."""
    nav_entries = []
    nav_entries.append({"Overview": f"lessons/{lang}/index.md"})
    for ch in sorted_chapters(titles):
        ch_num = int(ch[2:])
        title = titles[ch]
        src = LESSONS / lang / course / ch
        if not src.is_dir():
            continue
        nav_entries.extend(build_chapter(lang, course, ch, title, ch_num))
    return [{label: nav_entries}]


def build_nav() -> list:
    nav: list = [{"Home": "index.md"}]
    for lang, course, label, titles in COURSES:
        nav.extend(build_course(lang, course, label, titles))
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

    build_api_reference()
    nav = build_nav()
    write_nav_yml(nav)

    total = sum(
        1
        for lang, course, _, titles in COURSES
        for ch in sorted_chapters(titles)
        if (LESSONS / lang / course / ch).is_dir()
    )
    print(f"Processed {total} chapters across {len(COURSES)} courses.")
    print("Done. Run: mkdocs build")


if __name__ == "__main__":
    main()
