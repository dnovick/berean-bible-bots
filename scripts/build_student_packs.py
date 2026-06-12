"""Build student zip packages for BBH, BBG, and BBA.

Produces three self-contained zips under output/student-packs/:
  BBH.zip  — Hebrew lessons, exercises (HTML+PDF+MD), flashcard decks, OT charts
  BBG.zip  — Greek lessons, exercises (HTML+PDF+MD), flashcard decks, NT+Both charts
  BBA.zip  — Aramaic lessons, exercises (HTML+PDF+MD), flashcard decks

Each chapter folder contains:
  lesson.html         — rendered lesson (README.md → styled HTML)
  <paradigm>.html     — rendered paradigm/reference files (if any)
  exercises/          — HTML and PDF exercise files only
  flashcards/         — .txt and -fd.txt deck files + README

A clickable index.html at the course root links all chapters.
"""

import re
import zipfile
from pathlib import Path

import markdown

REPO = Path(__file__).resolve().parents[1]
LESSONS = REPO / "data" / "lessons"
CHARTS = REPO / "output" / "charts"
OUT = REPO / "output" / "student-packs"
OUT.mkdir(parents=True, exist_ok=True)

# ── HTML template ─────────────────────────────────────────────────────────────

_CSS = """
body {
  font-family: Georgia, 'Times New Roman', serif;
  max-width: 860px;
  margin: 40px auto;
  padding: 0 24px 60px;
  color: #222;
  line-height: 1.7;
}
h1 { font-size: 1.8em; border-bottom: 2px solid #c8a96e; padding-bottom: 8px; }
h2 { font-size: 1.35em; border-bottom: 1px solid #ddd; padding-bottom: 4px; margin-top: 2em; }
h3 { font-size: 1.1em; color: #444; margin-top: 1.6em; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 0.92em; }
th { background: #f5efe0; border: 1px solid #ccc; padding: 6px 10px; text-align: left; }
td { border: 1px solid #ddd; padding: 5px 10px; }
code, pre { background: #f8f4ec; border-radius: 3px; padding: 2px 5px;
            font-family: 'Courier New', monospace; font-size: 0.9em; }
pre { padding: 12px 16px; overflow-x: auto; }
blockquote { border-left: 4px solid #c8a96e; margin: 1em 0; padding: 4px 16px;
             color: #555; background: #fdf9f2; }
a { color: #7b3f00; }
hr { border: none; border-top: 1px solid #ddd; margin: 2em 0; }
.nav { font-size: 0.85em; margin-bottom: 1.5em; color: #888; }
.nav a { color: #7b3f00; margin-right: 8px; }
"""

_INDEX_CSS = """
body {
  font-family: Georgia, 'Times New Roman', serif;
  max-width: 780px;
  margin: 40px auto;
  padding: 0 24px 60px;
  color: #222;
  line-height: 1.7;
}
h1 { font-size: 2em; border-bottom: 2px solid #c8a96e; padding-bottom: 8px; }
h2 { font-size: 1.2em; color: #555; margin-top: 0; }
ul { list-style: none; padding: 0; }
li { padding: 4px 0; border-bottom: 1px solid #f0e8d8; }
li a { color: #7b3f00; font-size: 1em; text-decoration: none; }
li a:hover { text-decoration: underline; }
.subtitle { color: #888; font-size: 0.85em; margin-left: 6px; }
h3 { font-size: 1em; color: #999; letter-spacing: 0.05em; text-transform: uppercase;
     margin: 1.6em 0 0.3em; }
"""


def _html_page(title: str, body_html: str, nav_html: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{_CSS}</style>
</head>
<body>
{"<div class='nav'>" + nav_html + "</div>" if nav_html else ""}
{body_html}
</body>
</html>"""


def _md_to_html(md_path: Path, nav_html: str = "") -> str:
    """Convert a markdown file to a styled HTML page."""
    text = md_path.read_text(encoding="utf-8")
    # Extract title from first heading
    m = re.match(r'^#\s+(.+)', text)
    title = m.group(1) if m else md_path.stem
    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "nl2br"],
    )
    return _html_page(title, body, nav_html)


# ── Flashcard README ──────────────────────────────────────────────────────────

_FLASHCARD_README = """\
# Flashcard Decks — How to Use

## Anki (free — recommended)

1. Download Anki from https://apps.ankiweb.net
2. In Anki, go to  File → Import
3. Select the  .txt  file for this chapter (e.g. ch13-vocab-deck.txt)
4. Make sure  Fields separated by: Tab  is selected
5. Click Import

The  .txt  files use tab-separated values compatible with Anki's default import format.

## Flashcards Deluxe (iOS/Android — paid)

Use the  -fd.txt  files.  In Flashcards Deluxe, tap the  +  button and choose
"Import from File (Dropbox / Files)".

## Reading the decks as plain text

Open the  .txt  file in any text editor or spreadsheet application.
Each line is one card:  front [TAB] back
"""


# ── Course builder ────────────────────────────────────────────────────────────

def _chapter_title(readme: Path) -> str:
    """Extract the markdown h1 title from a chapter README."""
    text = readme.read_text(encoding="utf-8")
    m = re.match(r'^#\s+(.+)', text)
    return m.group(1) if m else readme.parent.name


def build_course(
    zip_name: str,
    source_lessons: Path,
    course_label: str,
    chapter_count: int,
    chart_dirs: list[Path],
) -> Path:
    """Build one student zip.

    Args:
        zip_name: e.g. "BBH"
        source_lessons: path to data/lessons/bbh  (or bbg, bba)
        course_label: display name, e.g. "Basics of Biblical Hebrew (BBH)"
        chapter_count: expected number of chapters (for the index)
        chart_dirs: list of chart source directories to bundle under Charts/
    """
    zip_path = OUT / f"{zip_name}.zip"
    print(f"\nBuilding {zip_path} ...")

    chapters: list[tuple[str, str, str]] = []  # (folder_name, title, chapter_dir_in_zip)

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:

        # ── Chapters ──────────────────────────────────────────────────────────
        for ch_num in range(1, chapter_count + 1):
            ch_dir = source_lessons / f"ch{ch_num}"
            if not ch_dir.exists():
                continue

            readme = ch_dir / "README.md"
            title = _chapter_title(readme) if readme.exists() else f"Chapter {ch_num}"
            # Folder name: ch01 — Hebrew Alphabet  (zero-padded for sort order)
            folder = f"ch{ch_num:02d} — {_topic(title)}"
            zip_ch = f"{zip_name}/{folder}"

            chapters.append((folder, title, zip_ch))

            # Lesson HTML
            if readme.exists():
                nav = '<a href="../index.html">↑ Course index</a>'
                zf.writestr(f"{zip_ch}/lesson.html", _md_to_html(readme, nav))

            # Paradigm / reference .md files (not deck files, not README)
            for md_file in sorted(ch_dir.glob("*.md")):
                if md_file.name == "README.md" or "deck" in md_file.name:
                    continue
                nav = '<a href="../index.html">↑ Course index</a> · <a href="lesson.html">Lesson</a>'
                html_name = md_file.stem + ".html"
                zf.writestr(f"{zip_ch}/{html_name}", _md_to_html(md_file, nav))

            # Exercises — HTML, PDF, and MD
            ex_root = ch_dir / "exercises"
            if ex_root.exists():
                for ex_dir in sorted(ex_root.iterdir()):
                    if not ex_dir.is_dir():
                        continue
                    for ext in ("*.html", "*.pdf", "*.md"):
                        for f in sorted(ex_dir.glob(ext)):
                            if f.name == "README.md":
                                continue
                            zf.write(f, f"{zip_ch}/exercises/{ex_dir.name}/{f.name}")

            # Flashcard decks (.txt and -fd.txt; skip .md versions)
            deck_files = [
                f for f in sorted(ch_dir.glob("*.txt"))
                if "deck" in f.name
            ]
            if deck_files:
                for f in deck_files:
                    zf.write(f, f"{zip_ch}/flashcards/{f.name}")
                zf.writestr(f"{zip_ch}/flashcards/HOW-TO-IMPORT.txt", _FLASHCARD_README)

        # ── Charts ────────────────────────────────────────────────────────────
        for chart_dir in chart_dirs:
            if not chart_dir.exists():
                continue
            # Preserve sub-structure: Charts/<category>/<subdir>/file.png
            rel_base = chart_dir.relative_to(CHARTS)
            for png in sorted(chart_dir.rglob("*.png")):
                rel = png.relative_to(chart_dir)
                zf.write(png, f"{zip_name}/Charts/{rel_base}/{rel}")

        # ── Course index ──────────────────────────────────────────────────────
        zf.writestr(f"{zip_name}/index.html", _build_index(zip_name, course_label, chapters))

    size_mb = zip_path.stat().st_size / 1_048_576
    print(f"  → {zip_path.name}  ({size_mb:.1f} MB,  {len(chapters)} chapters)")
    return zip_path


def _topic(full_title: str) -> str:
    """Extract topic portion from 'BBH Chapter N — Topic' → 'Topic'."""
    m = re.search(r'—\s*(.+)', full_title)
    return m.group(1).strip() if m else full_title


def _build_index(zip_name: str, course_label: str, chapters: list[tuple]) -> str:
    items = "\n".join(
        f'    <li><a href="{folder}/lesson.html">'
        f'Ch {i+1:02d} — {_topic(title)}</a></li>'
        for i, (folder, title, _) in enumerate(chapters)
    )
    body = f"""<h1>{course_label}</h1>
<h2>Student Lesson Package</h2>
<p>Click any chapter below to open the lesson. Each chapter folder also contains
interactive exercises (HTML), printable exercises (PDF), static reference copies (MD), plus flashcard files
for import into Anki or Flashcards Deluxe.</p>
<h3>Chapters</h3>
<ul>
{items}
</ul>
<p style="margin-top:3em; color:#aaa; font-size:0.8em;">
Generated by Berean Bible Bots · github.com/dnovick/berean-bible-bots</p>"""
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{course_label}</title>
<style>{_INDEX_CSS}</style>
</head>
<body>
{body}
</body>
</html>"""
    return page


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    build_course(
        zip_name="BBH",
        source_lessons=LESSONS / "bbh",
        course_label="Basics of Biblical Hebrew (BBH)",
        chapter_count=35,
        chart_dirs=[CHARTS / "ot"],
    )

    build_course(
        zip_name="BBG",
        source_lessons=LESSONS / "bbg",
        course_label="Basics of Biblical Greek (BBG)",
        chapter_count=36,
        chart_dirs=[CHARTS / "nt", CHARTS / "both"],
    )

    build_course(
        zip_name="BBA",
        source_lessons=LESSONS / "bba",
        course_label="Basics of Biblical Aramaic (BBA)",
        chapter_count=22,
        chart_dirs=[],
    )

    print("\nDone. Zips are in output/student-packs/")
