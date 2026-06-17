"""Build the MkDocs docs/ source tree.

Orchestrates the full site build:
  - Lessons (BBH/BBG/BBA) — delegated to scripts/build_lessons.py
  - Notebooks, Reports, Study Helps, API Reference — built here

Run before `mkdocs build`:
    python scripts/build_mkdocs.py
"""

import re
import shutil
from pathlib import Path

from build_lessons import (  # noqa: E402
    build_all as _build_all_lessons,
    NAV_START as _LESSONS_NAV_START,
    NAV_END as _LESSONS_NAV_END,
)

REPO = Path(__file__).parent.parent
MKDOCS_SRC = REPO / "mkdocs_src"


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
            # Promote single-entry subdirs to the parent level (avoids the
            # "expand → click" two-click pattern) — UNLESS the subdir has a
            # README.md, which signals it is a named category with its own
            # overview page and should always appear as a nav group.
            sub_has_readme = (sub / "README.md").exists()
            sole = (
                len(sub_entries) == 1 and
                isinstance(list(sub_entries[0].values())[0], str) and
                list(sub_entries[0].keys())[0] != "Overview" and
                not sub_has_readme
            )
            if sole:
                nav_entries.append(sub_entries[0])
            else:
                # Use README H1 title if available, else capitalise dir name
                if sub_has_readme:
                    sub_label = _md_title(sub_dst / "index.md") or \
                        sub.name.replace("-", " ").replace("_", " ").title()
                else:
                    sub_label = sub.name.replace("-", " ").replace("_", " ").title()
                nav_entries.append({sub_label: sub_entries})

    # Determine whether to add nav entries for .md files and/or an Overview.
    #
    # Case 1 — No README: add each .md file as its own nav entry.
    # Case 2 — README alone (no other .md, no sub-entries):
    #   The README index IS the single destination; link to it directly.
    # Case 3 — README + one or more .md files or subdirectory entries:
    #   Write README as index.md, add an Overview entry, and list each
    #   .md file so every report is reachable directly from the nav.
    is_readme_only = (
        readme.exists() and
        len(md_files) == 0 and
        not any(True for _ in nav_entries)
    )

    # Write README → index.md whenever README exists (Cases 2 & 3).
    if readme.exists():
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
    elif is_readme_only:
        # Case 2: README-only directory — the README index IS the single destination
        readme_title = _md_title(dst_dir / "index.md") or label
        rel = str((dst_dir / "index.md").relative_to(MKDOCS_SRC))
        nav_entries.append({readme_title: rel})
    else:
        # Case 3: README + one or more .md files and/or subdirectory entries.
        # Sub-dir entries are already in nav_entries. Also add each flat .md
        # file so every report is reachable directly from the nav (not just
        # via the Overview landing page).
        for md in md_files:
            title = _md_title(dst_dir / md.name)
            rel = str((dst_dir / md.name).relative_to(MKDOCS_SRC))
            nav_entries.append({title: rel})

    # Add index.md as first nav entry for Case 3 (README + content).
    if not is_readme_only and readme.exists():
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


def build_nav() -> list:
    nav: list = [{"Home": "index.md"}]
    nav.extend(_build_all_lessons())  # BBH / BBG / BBA (includes additional-resources)
    nav.extend(build_notebooks())
    nav.extend(build_reports())
    # Courses nav block is inserted by scripts/build_courses.py (update_nav)
    nav.extend(build_study_helps())
    nav.append({"API Reference": "reference/index.md"})
    return nav


def write_nav_yml(nav: list) -> None:
    """Serialize nav list to YAML and write mkdocs_nav.yml.

    Inserts # <LESSONS> / # </LESSONS> sentinel markers around the lesson
    entries so that build_lessons.py can patch just the lessons section on
    incremental rebuilds without touching the rest of the nav.
    """
    import yaml
    out = REPO / "mkdocs_nav.yml"
    yaml_str = yaml.dump({"nav": nav}, allow_unicode=True, sort_keys=False)

    # Insert sentinel markers around the lessons block.
    # Lessons always follow "- Home: index.md" and precede "- Notebooks:".
    first_lesson = "- Biblical Hebrew (BBH):"
    after_lessons = "- Notebooks:"
    if first_lesson in yaml_str:
        yaml_str = yaml_str.replace(
            first_lesson, _LESSONS_NAV_START + "\n" + first_lesson, 1
        )
    if after_lessons in yaml_str:
        yaml_str = yaml_str.replace(
            after_lessons, _LESSONS_NAV_END + "\n" + after_lessons, 1
        )

    out.write_text(yaml_str, encoding="utf-8")
    print(f"Wrote {out}")


def copy_static_assets() -> None:
    """Copy hand-authored static files from docs/ into mkdocs_src/.

    These files are committed under docs/ (not generated) and must be present
    in mkdocs_src/ for MkDocs to include them in the built site.  Covered:
      - assets/logo.png  (theme logo and favicon)
      - stylesheets/extra.css  (custom colour scheme)
      - javascripts/*.js  (sortable tables, nav toggle, home-link)
      - about-the-logo.md  (hand-authored page)
    """
    static_dirs = ["assets", "stylesheets", "javascripts"]
    for d in static_dirs:
        src = REPO / "docs" / d
        dst = MKDOCS_SRC / d
        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)

    for fname in ["about-the-logo.md"]:
        src = REPO / "docs" / fname
        if src.exists():
            shutil.copy2(src, MKDOCS_SRC / fname)


def build_api_reference() -> None:
    ref_dir = MKDOCS_SRC / "reference"
    ref_dir.mkdir(parents=True, exist_ok=True)

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

    # Clean generated reports and study-helps dirs
    for clean_dir in ("reports", "study-helps"):
        d = MKDOCS_SRC / clean_dir
        if d.exists():
            shutil.rmtree(d)

    # Ensure mkdocs_src/ exists (gitignored; absent on fresh CI checkout)
    MKDOCS_SRC.mkdir(parents=True, exist_ok=True)

    # Copy hand-authored static assets (logo, CSS, JS) from docs/ into mkdocs_src/
    copy_static_assets()

    # Write root index.md — hide nav and TOC so the full width is available
    (MKDOCS_SRC / "index.md").write_text(
        "---\ntemplate: home.html\nhide:\n  - navigation\n  - toc\n---\n",
        encoding="utf-8",
    )

    build_api_reference()
    nav = build_nav()  # calls _build_all_lessons() which handles lesson dir cleanup
    write_nav_yml(nav)
    print("Done. Run: mkdocs build")


if __name__ == "__main__":
    main()
