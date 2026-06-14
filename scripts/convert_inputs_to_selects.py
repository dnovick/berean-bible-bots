#!/usr/bin/env python3
"""
Convert <input class="parse-field"> elements in BBH HTML exercise files
to <select> dropdowns for columns with fixed option sets.

Usage: python3 scripts/convert_inputs_to_selects.py
"""

from pathlib import Path
from bs4 import BeautifulSoup, Tag

# ---------------------------------------------------------------------------
# Column → options map
# Keys are normalised lowercase column header text.
# Each value is a list of option strings (blank first option is always added).
# ---------------------------------------------------------------------------

BASE_DIR = Path("/Users/dnovick/gitrepos/projects/bible/berean-bible-bots")

FILES = [
    # Session review exercises — Ch1–3 (session05)
    # These exercises use class="f" inputs; qualifying columns are converted to selects.
    "data/courses/bbh/bbh-2026.1/session-05/exercises/session05-letter-review/session05-letter-review.html",
    "data/courses/bbh/bbh-2026.1/session-05/exercises/session05-vowel-review/session05-vowel-review.html",
    "data/courses/bbh/bbh-2026.1/session-05/exercises/"
    "session05-syllabification-review/session05-syllabification-review.html",
    "data/courses/bbh/bbh-2026.1/session-05/exercises/session05-dagesh-review/session05-dagesh-review.html",
    "data/courses/bbh/bbh-2026.1/session-05/exercises/session05-shewa-review/session05-shewa-review.html",
    # Lesson exercises — Ch4+
    "data/lessons/bbh/ch4/exercises/ch4-noun-parsing/ch4-noun-parsing.html",
    "data/lessons/bbh/ch7/exercises/ch7-adjective-usage/ch7-adjective-usage.html",
    "data/lessons/bbh/ch12/exercises/ch12-verb-overview/ch12-verb-overview.html",
    "data/lessons/bbh/ch13/exercises/ch13-parsing-drill/ch13-parsing-drill.html",
    "data/lessons/bbh/ch13/exercises/ch13-passage-exercise/ch13-passage-exercise.html",
    "data/lessons/bbh/ch13/exercises/ch13-qal-perfect-paradigm-drill/ch13-qal-perfect-paradigm-drill.html",
    "data/lessons/bbh/ch15/exercises/ch15-parsing-drill/ch15-parsing-drill.html",
    "data/lessons/bbh/ch15/exercises/ch15-qal-imperfect-paradigm-drill/ch15-qal-imperfect-paradigm-drill.html",
    "data/lessons/bbh/ch17/exercises/ch17-wayyiqtol-paradigm-drill/ch17-wayyiqtol-paradigm-drill.html",
    "data/lessons/bbh/ch18/exercises/ch18-qal-imperative-paradigm-drill/ch18-qal-imperative-paradigm-drill.html",
    "data/lessons/bbh/ch24/exercises/ch24-niphal-paradigm-drill/ch24-niphal-paradigm-drill.html",
    "data/lessons/bbh/ch26/exercises/ch26-hiphil-paradigm-drill/ch26-hiphil-paradigm-drill.html",
    "data/lessons/bbh/ch26/exercises/ch26-stem-id-drill/ch26-stem-id-drill.html",
    "data/lessons/bbh/ch27/exercises/ch27-function-sort/ch27-function-sort.html",
    "data/lessons/bbh/ch27/exercises/ch27-passage-exercise/ch27-passage-exercise.html",
    "data/lessons/bbh/ch27/exercises/ch27-qal-hiphil-contrast/ch27-qal-hiphil-contrast.html",
    "data/lessons/bbh/ch27/exercises/ch27-stem-id-drill/ch27-stem-id-drill.html",
    "data/lessons/bbh/ch28/exercises/ch28-hophal-paradigm-drill/ch28-hophal-paradigm-drill.html",
    "data/lessons/bbh/ch29/exercises/ch29-hophal-weak-paradigm-drill/ch29-hophal-weak-paradigm-drill.html",
    "data/lessons/bbh/ch30/exercises/ch30-piel-paradigm-drill/ch30-piel-paradigm-drill.html",
    "data/lessons/bbh/ch31/exercises/ch31-piel-weak-paradigm-drill/ch31-piel-weak-paradigm-drill.html",
    "data/lessons/bbh/ch32/exercises/ch32-pual-paradigm-drill/ch32-pual-paradigm-drill.html",
    "data/lessons/bbh/ch33/exercises/ch33-pual-weak-paradigm-drill/ch33-pual-weak-paradigm-drill.html",
    "data/lessons/bbh/ch34/exercises/ch34-hithpael-paradigm-drill/ch34-hithpael-paradigm-drill.html",
    "data/lessons/bbh/ch35/exercises/ch35-hithpael-weak-paradigm-drill/ch35-hithpael-weak-paradigm-drill.html",
]

# ---------------------------------------------------------------------------
# Helper: detect style (with-dot vs without-dot) from existing answer cells
# ---------------------------------------------------------------------------


def detect_style_from_answers(soup: BeautifulSoup) -> dict:
    """
    Scan answer rows for values to detect whether files use
    dotted (m./f./s./pl./du.) or bare (m/f/s/p) abbreviations.
    Returns dict with keys 'gender_dot' and 'number_dot'.
    """
    all_td_text = []
    for row in soup.find_all("tr"):
        cls = list(row.get("class") or [])
        # Answer rows have class containing "ans-row", "answer-row", etc.
        is_ans = any("ans" in c for c in cls) or any("answer" in c for c in cls)
        if is_ans:
            for td in row.find_all("td"):
                txt = td.get_text(strip=True)
                if txt:
                    all_td_text.append(txt)

    # Check for dotted patterns
    gender_dot = any(t in ("m.", "f.", "c.") for t in all_td_text)
    number_dot = any(t in ("s.", "pl.", "du.") for t in all_td_text)
    # Detect Dagesh and Shewa type answer styles
    has_forte_lene = any(t in ("Forte", "Lene") for t in all_td_text)
    has_vocal_silent = any(t in ("Vocal", "Silent") for t in all_td_text)

    return {
        "gender_dot": gender_dot,
        "number_dot": number_dot,
        "has_forte_lene": has_forte_lene,
        "has_vocal_silent": has_vocal_silent,
    }


def get_column_options(header_text: str, style: dict) -> list | None:
    """
    Return a list of option strings for a given column header,
    or None if the column should be left as free text.
    """
    h = header_text.strip().lower()

    # Exact / close matches for column headers
    if h == "person":
        return ["1", "2", "3"]

    if h == "number":
        if style.get("number_dot"):
            return ["s.", "pl.", "du."]
        else:
            return ["s", "p", "du"]

    if h == "gender":
        if style.get("gender_dot"):
            return ["m.", "f.", "c."]
        else:
            return ["m", "f", "c"]

    if h == "state":
        return ["abs.", "cstr.", "abs. or cstr."]

    if h == "stem":
        return ["Qal", "Niphal", "Piel", "Pual", "Hiphil", "Hophal", "Hithpael"]

    if h == "pgn":
        return [
            "1cs", "2ms", "2fs", "3ms", "3fs",
            "1cp", "2mp", "2fp", "3mp", "3fp",
            "ms", "fs", "mp", "fp",
        ]

    if h == "use":
        return [
            "Attributive (def.)",
            "Attributive (indef.)",
            "Predicate",
            "Substantival",
            "Comparative",
            "Superlative",
        ]

    if h == "function":
        return ["Causative", "Simple Action"]

    if h in ("conjugation", "conj"):
        return [
            "Perfect",
            "Imperfect",
            "Wayyiqtol",
            "Imperative",
            "Inf. Construct",
            "Inf. Absolute",
            "Participle",
        ]

    # ── Session review exercise column types ─────────────────────────────────

    # Letter name (all BBH letter names including sofit and hard/soft variants)
    if h == "name":
        return [
            "Alef", "Ayin", "Bet", "Bet (hard)", "Bet (soft)",
            "Dalet", "Dalet (hard)", "Dalet (soft)",
            "Gimel", "Gimel (hard)", "Gimel (soft)",
            "He", "Ḥet", "Kaf", "Kaf (hard)", "Kaf (soft)", "Kaf Sofit",
            "Lamed", "Mem", "Mem Sofit", "Nun", "Nun Sofit",
            "Pe", "Pe (hard)", "Pe (soft)", "Pe Sofit",
            "Qof", "Resh", "Samek", "Shin", "Sin",
            "Taw", "Taw (hard)", "Taw (soft)", "Tet",
            "Tsade", "Tsade Sofit", "Waw", "Yod", "Zayin",
        ]

    # Vowel name (BBH vowel names)
    if h == "vowel name":
        return [
            "Qamets", "Pathach", "Qamets Hatuf", "Tsere", "Seghol",
            "Hireq", "Hireq Yod", "Tsere Yod", "Holem", "Holem Waw",
            "Shureq", "Qibbuts", "Qamets He", "Holem He", "Tsere He",
            "Seghol He", "Vocal Shewa", "Silent Shewa",
            "Hateph Pathach", "Hateph Seghol", "Hateph Qamets",
        ]

    # Vowel class (A/E/I/O/U/Reduced)
    if h == "class":
        return ["A", "E", "I", "O", "U", "Reduced", "—"]

    # Vowel quantity (Long/Short/Reduced)
    if h == "quantity":
        return ["Long", "Short", "Reduced", "—"]

    # Syllable type pattern (O/C combinations)
    if h in ("types (o/c)", "types"):
        return ["O", "C", "O-C", "C-O", "O-O", "C-C", "O-O-C", "C-O-C", "O-O-O", "O-C-C"]

    # Qamets Hatuf indicator
    if h in ("qamets hatuf?", "qh?"):
        return ["—", "Yes", "No"]

    # Dagesh type (Forte/Lene) — detected from answer rows
    if h in ("forte or lene?", "type") and style.get("has_forte_lene"):
        return ["Forte", "Lene"]

    # Shewa type (Vocal/Silent) — detected from answer rows
    if h == "type" and style.get("has_vocal_silent"):
        return ["Vocal", "Silent"]

    return None  # free-text column; leave as input


# ---------------------------------------------------------------------------
# CSS snippet to inject
# ---------------------------------------------------------------------------
SELECT_CSS = (
    "select.parse-field { font-size: .9em; padding: 2px 4px; "
    "border: 1px solid #aaa; border-radius: 3px; min-width: 80px; }"
)
# CSS for session exercises that use class="f" (already injected at file creation;
# this constant is kept for reference — inject_select_css checks for both).
SELECT_CSS_F = (
    "select.f { width: 100%; box-sizing: border-box; border: 1px solid #bbb; "
    "border-radius: 3px; padding: .22rem .3rem; font-family: Georgia, serif; "
    "font-size: .87rem; background: #fafff8; }"
)


def build_select(options: list, original_input: Tag, soup: BeautifulSoup) -> Tag:
    """
    Create a <select class="parse-field"> tag to replace original_input.
    Preserve id, name, and data-* attributes from the original input.
    """
    sel = soup.new_tag("select")
    # Preserve the original class (parse-field or f) so CSS rules match
    orig_classes = list(original_input.get("class") or ["parse-field"])
    sel["class"] = orig_classes  # type: ignore[assignment]  # BS4 accepts list at runtime
    # Preserve id if present
    if original_input.get("id"):
        sel["id"] = original_input["id"]
    if original_input.get("name"):
        sel["name"] = original_input["name"]
    # Copy any data-* attributes
    for attr, val in original_input.attrs.items():
        if attr.startswith("data-"):
            sel[attr] = val

    # Blank first option
    blank = soup.new_tag("option", value="")
    blank.string = "—"
    sel.append(blank)

    for opt_text in options:
        opt = soup.new_tag("option", value=opt_text)
        opt.string = opt_text
        sel.append(opt)

    return sel


def is_answer_row(tr: Tag) -> bool:
    """Return True if this <tr> is an answer/reveal row (should not be modified)."""
    cls = list(tr.get("class") or [])
    row_id = str(tr.get("id") or "")
    return (
        any("ans" in c for c in cls)
        or any("answer" in c for c in cls)
        or row_id.startswith("ans-")
    )


def fix_clear_all(html_str: str) -> str:
    """
    Update clearAll() JS to use querySelectorAll('.parse-field') so it clears
    both <input> and <select> elements.
    Patterns handled:
      querySelectorAll('input.parse-field')
      querySelectorAll("input.parse-field")
      querySelectorAll('input.f')        -- older files use class="f" wrongly; also fix
      querySelectorAll("input.f")
    """
    patterns = [
        ("querySelectorAll('input.parse-field')", "querySelectorAll('.parse-field')"),
        ('querySelectorAll("input.parse-field")', "querySelectorAll('.parse-field')"),
        ("querySelectorAll('input.f')", "querySelectorAll('.parse-field')"),
        ('querySelectorAll("input.f")', "querySelectorAll('.parse-field')"),
    ]
    for old, new in patterns:
        html_str = html_str.replace(old, new)
    return html_str


def inject_select_css(soup: BeautifulSoup) -> bool:
    """
    Add SELECT_CSS to the <style> block if not already present.
    Handles both parse-field (lesson exercises) and f (session exercises) classes.
    Returns True if injected, False if already there.
    """
    style_tag = soup.find("style")
    if style_tag is None:
        return False
    existing = style_tag.string or ""
    # For session exercises (class="f"), select.f CSS is already written at creation time
    if "select.f" in existing:
        return False
    if "select.parse-field" in existing:
        return False
    # Append at end of style block
    style_tag.string = existing.rstrip() + "\n  " + SELECT_CSS + "\n"
    return True


def process_file(rel_path: str) -> dict:
    """
    Process a single HTML file: replace qualifying inputs with selects.
    Returns a report dict.
    """
    path = BASE_DIR / rel_path
    if not path.exists():
        return {"file": rel_path, "error": "FILE NOT FOUND"}

    raw = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")

    style = detect_style_from_answers(soup)
    converted_columns = set()
    total_selects = 0

    # Process every <table> in the document
    for table in soup.find_all("table"):
        # Get headers and their column indices
        # Use the first row that has <th> elements
        headers = {}  # col_index -> header_text
        header_row = None
        for tr in table.find_all("tr"):
            ths = tr.find_all("th")
            if ths:
                header_row = tr
                for idx, th in enumerate(ths):
                    headers[idx] = th.get_text(strip=True)
                break

        if not headers:
            continue

        # Determine which col indices should become selects
        col_options = {}  # col_index -> [options]
        for idx, hdr_text in headers.items():
            opts = get_column_options(hdr_text, style)
            if opts is not None:
                col_options[idx] = opts

        if not col_options:
            continue

        # Walk every data row (not header row, not answer row)
        for tr in table.find_all("tr"):
            if tr is header_row:
                continue
            if is_answer_row(tr):
                continue

            tds = tr.find_all("td")
            for col_idx, options in col_options.items():
                if col_idx >= len(tds):
                    continue
                td = tds[col_idx]
                # Find input.parse-field or input.f (session exercises use .f)
                inp = td.find("input", class_="parse-field")
                if inp is None:
                    inp = td.find("input", class_="f")
                if inp is None:
                    continue
                classes = list(inp.get("class") or [])
                if "wide" in classes:
                    continue
                # Build and substitute the select (preserving original class)
                sel = build_select(options, inp, soup)
                inp.replace_with(sel)
                total_selects += 1
                hdr = headers[col_idx]
                converted_columns.add(hdr)

    if total_selects == 0:
        return {
            "file": rel_path,
            "converted_columns": [],
            "selects_created": 0,
            "note": "No qualifying inputs found",
        }

    # Inject CSS
    inject_select_css(soup)

    # Serialise back to string
    result_html = str(soup)

    # Fix clearAll() JS
    result_html = fix_clear_all(result_html)

    # Write back
    path.write_text(result_html, encoding="utf-8")

    return {
        "file": rel_path,
        "converted_columns": sorted(converted_columns),
        "selects_created": total_selects,
        "style": f"gender_dot={style['gender_dot']}, number_dot={style['number_dot']}",
    }


def main() -> None:
    print("=" * 70)
    print("Converting <input class='parse-field'> → <select> in BBH exercises")
    print("=" * 70)
    total_selects_all = 0
    for rel_path in FILES:
        result = process_file(rel_path)
        fname = Path(rel_path).name
        if "error" in result:
            print(f"\n  ERROR  {fname}: {result['error']}")
        elif result["selects_created"] == 0:
            print(f"\n  SKIP   {fname}: {result.get('note', 'no qualifying inputs')}")
        else:
            print(f"\n  OK     {fname}")
            print(f"         Columns converted: {', '.join(result['converted_columns'])}")
            print(f"         Selects created:   {result['selects_created']}")
            if "style" in result:
                print(f"         Style detected:    {result['style']}")
            total_selects_all += result["selects_created"]
    print()
    print("=" * 70)
    print(f"Done. Total selects created across all files: {total_selects_all}")
    print("=" * 70)


if __name__ == "__main__":
    main()
