#!/usr/bin/env python3
"""Build Psalm 119 memorization exercises for all 22 acrostic sections.

Generated output goes to:
    mkdocs_src/studies/psalm-119/memorization/<slug>/

Generates per section:
    - Vocabulary Anki deck (.txt, -fd.txt, .md)
    - Verse-recitation Anki deck (.txt, -fd.txt, .md)
    - Cloze L1 exercise — key vocab blanked (.html, .md, .pdf)
    - Cloze L2 exercise — line endings blanked (.html, .md, .pdf)
    - Verse-ordering exercise (.html, .md, .pdf)
    - First-word-prompt exercise (.html, .md, .pdf)
    - Reference card PDF (Hebrew + KJV side-by-side)

Run standalone:
    python scripts/build_psalm119_memorization.py
"""

from __future__ import annotations

import re
import random
import html
from pathlib import Path
from typing import Any

import yaml
import pandas as pd

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas
from bidi.algorithm import get_display

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO = Path(__file__).resolve().parent.parent
DATA_YAML = REPO / "data" / "studies" / "psalm-119" / "psalm-119-text.yaml"
WORDS_PARQUET = REPO / "data" / "processed" / "words.parquet"
MKDOCS_OUT = REPO / "mkdocs_src" / "studies" / "psalm-119" / "memorization"

# ---------------------------------------------------------------------------
# Fonts (reportlab)
# ---------------------------------------------------------------------------
_FONTS_REGISTERED = False


def _register_fonts() -> None:
    global _FONTS_REGISTERED
    if _FONTS_REGISTERED:
        return
    try:
        pdfmetrics.registerFont(
            TTFont("ArialHebrew", "/System/Library/Fonts/ArialHB.ttc", subfontIndex=2)
        )
        pdfmetrics.registerFont(
            TTFont("ArialHebrewBold", "/System/Library/Fonts/ArialHB.ttc", subfontIndex=3)
        )
    except Exception:
        pass
    _FONTS_REGISTERED = True


def _heb(text: str) -> str:
    return get_display(text)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
_CANT = re.compile(r"[֑-ׇֽֿׁׂׅ֯ׄ‍]")
_MAQQUEF = "־"


def _strip_word(w: str) -> str:
    parts = str(w).split("/")
    joined = "".join(parts)
    clean = _CANT.sub("", joined)
    clean = clean.replace("\\", "").replace("׃", "").replace(_MAQQUEF, "")
    return clean


def load_stanzas() -> list[dict[str, Any]]:
    with open(DATA_YAML, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["stanzas"]


def build_word_lookup() -> dict[str, str]:
    """Return {clean_word -> gloss} for Psalm 119."""
    df = pd.read_parquet(WORDS_PARQUET)
    p119 = df[(df["book_id"] == "Psa") & (df["chapter"] == 119)].copy()
    p119["clean"] = p119["word"].apply(_strip_word)
    lookup: dict[str, str] = {}
    for _, row in p119.iterrows():
        clean = row["clean"]
        if clean and clean not in lookup:
            lookup[clean] = _clean_gloss(str(row.get("translation", "")))
    return lookup


def _clean_gloss(raw: str) -> str:
    t = re.sub(r"\s*\[.*?\]\s*", " ", raw)
    t = re.sub(r"\s*/\s*", " ", t)
    t = " ".join(t.split())
    return t.strip(" ;")


def lookup_gloss(key_word: str, word_lookup: dict[str, str]) -> str:
    clean = _strip_word(key_word)
    return word_lookup.get(clean, "")


# ---------------------------------------------------------------------------
# Slug helper
# ---------------------------------------------------------------------------
def make_slug(stanza: dict[str, Any]) -> str:
    import unicodedata
    name = stanza["name"].lower()
    # Decompose (e.g. Ḥet → h + combining dot + et), strip non-ASCII
    name = unicodedata.normalize("NFKD", name)
    name = re.sub(r"[^a-z]", "", name)
    return f"{stanza['num']:02d}-{name}"


# ---------------------------------------------------------------------------
# Verse text helpers
# ---------------------------------------------------------------------------
def blank_key_word(text: str, key_word: str) -> str:
    # Try direct match first
    if key_word in text:
        idx = text.index(key_word)
        after = text[idx + len(key_word):]
        # Absorb trailing maqquef + next token so the blank is clean
        m = re.match(r"[־-](\S+)", after)
        if m:
            return text[:idx] + "______" + after[m.end():]
        return text[:idx] + "______" + after
    return text


def blank_line_endings(text: str, endings: list[str]) -> str:
    for ending in endings:
        text = blank_key_word(text, ending)
    return text


def safe_html(s: str) -> str:
    return html.escape(s)


# ---------------------------------------------------------------------------
# Common HTML CSS/JS template
# ---------------------------------------------------------------------------
_EXERCISE_CSS = """\
  body { font-family: Georgia, serif; max-width: 1050px; margin: 2em auto; padding: 0 1.5em; color: #222; }
  h1 { font-size: 1.4em; border-bottom: 2px solid #444; padding-bottom: .4em; }
  h2 { font-size: 1.1em; margin-top: 1.5em; color: #444; }
  .subtitle { color: #666; font-style: italic; margin-top: -.3em; margin-bottom: 1em; }
  table { border-collapse: collapse; width: 100%; margin: 1em 0; }
  th { background: #2a4a6e; color: #fff; padding: .5em .7em; text-align: left; font-size: .85em; }
  td { border: 1px solid #ccc; padding: .45em .65em; font-size: .88em; vertical-align: top; }
  tr:nth-child(even):not(.answer-row) td { background: #f7f7f7; }
  .heb { font-size: 1.25em; direction: rtl; unicode-bidi: embed; display: block; }
  .heb-inline { font-size: 1.2em; direction: rtl; unicode-bidi: embed; }
  input.parse-field { width: 100%; box-sizing: border-box; font-size: .88em; padding: 3px 5px;
    border: 1px solid #aaa; border-radius: 3px; direction: rtl; }
  textarea.heb-area { width: 100%; box-sizing: border-box; font-size: 1.1em; padding: 4px 6px;
    border: 1px solid #aaa; border-radius: 3px; direction: rtl; min-height: 3em; }
  select.parse-field { width: 100%; box-sizing: border-box; font-size: .88em; padding: 3px 5px;
    border: 1px solid #aaa; border-radius: 3px; }
  .answer-row td { background: #e6f4ea !important; color: #1a5c1a; font-size: .85em; }
  .answer-row { display: none; }
  button.reveal-btn { font-size: .78em; padding: 2px 7px; cursor: pointer; border: 1px solid #888;
    border-radius: 3px; background: #fff; white-space: nowrap; }
  .controls { margin: 1em 0; display: flex; gap: .6em; flex-wrap: wrap; }
  .controls button { padding: .4em .9em; font-size: .9em; cursor: pointer; border: 1px solid #555;
    border-radius: 4px; background: #f0f0f0; }
  .controls button:hover { background: #ddd; }
  .tip { background: #fffbe6; border-left: 4px solid #d4a017; padding: .6em 1em; margin: 1em 0; font-size: .88em; }
  @media print {
    button, .controls { display: none !important; }
    input.parse-field, textarea.heb-area { border: none; border-bottom: 1px solid #000; background: transparent; }
    .answer-row { display: table-row !important; }
    select.parse-field { border: none; border-bottom: 1px solid #000; background: transparent; }
  }"""

_EXERCISE_JS = """\
  function toggle(id) {
    var r = document.getElementById(id);
    r.style.display = (r.style.display === 'none' || r.style.display === '') ? 'table-row' : 'none';
  }
  function showAll() { document.querySelectorAll('.answer-row').forEach(r => r.style.display='table-row'); }
  function hideAll() { document.querySelectorAll('.answer-row').forEach(r => r.style.display='none'); }
  function clearAll() {
    document.querySelectorAll('input.parse-field, textarea.heb-area').forEach(f => f.value='');
    document.querySelectorAll('select.parse-field').forEach(s => s.selectedIndex=0);
  }"""


def _html_doc(title: str, subtitle: str, body: str) -> str:
    return (
        f"<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
        f"<meta charset=\"UTF-8\">\n"
        f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
        f"<title>{safe_html(title)}</title>\n"
        f"<style>\n{_EXERCISE_CSS}\n</style>\n</head>\n<body>\n"
        f"<h1>{safe_html(title)}</h1>\n"
        f"<p class=\"subtitle\">{safe_html(subtitle)}</p>\n"
        f"{body}"
        f"<script>\n{_EXERCISE_JS}\n</script>\n</body>\n</html>\n"
    )


# ---------------------------------------------------------------------------
# Cloze L1 — key vocabulary words blanked
# ---------------------------------------------------------------------------
def build_cloze_l1_html(stanza: dict[str, Any], word_lookup: dict[str, str]) -> str:
    letter = stanza["letter"]
    name = stanza["name"]
    v_start = stanza["verses"][0]["abs_num"]
    v_end = stanza["verses"][-1]["abs_num"]
    title = f"Psalm 119 — {letter} {name} — Cloze Fill-in Level 1"
    subtitle = (
        f"Ps 119:{v_start}–{v_end} · Key vocabulary words blanked · "
        f"Type the missing Hebrew word, then click ▶ Answer"
    )

    tip = (
        '<div class="tip"><strong>Level 1:</strong> One or more key vocabulary words per verse '
        "are blanked. Type the missing Hebrew form exactly as it appears in the verse.</div>"
    )
    controls = (
        '<div class="controls">'
        '<button onclick="showAll()">Show All Answers</button>'
        '<button onclick="hideAll()">Hide All Answers</button>'
        '<button onclick="clearAll()">Clear All Inputs</button>'
        "</div>"
    )

    rows = []
    rows.append(
        "<tr><th>#</th><th>Verse — fill in the blanks</th>"
        "<th>Missing word(s)</th><th></th></tr>"
    )
    ans_rows = []

    for i, v in enumerate(stanza["verses"]):
        ref = f"119:{v['abs_num']}"
        blanked = v["hebrew"]
        key_words = v.get("key_words") or []
        # Blank each key_word
        for kw in key_words:
            blanked = blank_key_word(blanked, kw)

        inputs = "".join(
            f'<input class="parse-field" id="cl1_{i}_{j}" '
            f'placeholder="{safe_html(kw)[:1]}…" dir="rtl">'
            for j, kw in enumerate(key_words)
        )

        rows.append(
            f"<tr id='q-cl1-{i}'>"
            f"<td>{safe_html(ref)}</td>"
            f"<td><span class='heb'>{safe_html(blanked)}</span></td>"
            f"<td>{inputs}</td>"
            f"<td><button class='reveal-btn' onclick=\"toggle('a-cl1-{i}')\">▶ Answer</button></td>"
            f"</tr>"
        )

        answers = []
        for kw in key_words:
            gloss = lookup_gloss(kw, word_lookup)
            gloss_str = f" — {gloss}" if gloss else ""
            answers.append(f"<span class='heb-inline'>{safe_html(kw)}</span>{safe_html(gloss_str)}")
        ans_text = " &nbsp;|&nbsp; ".join(answers) if answers else "—"

        ans_rows.append(
            f"<tr class='answer-row' id='a-cl1-{i}'>"
            f"<td>✓ {safe_html(ref)}</td>"
            f"<td><span class='heb'>{safe_html(v['hebrew'])}</span></td>"
            f"<td>{ans_text}</td>"
            f"<td></td>"
            f"</tr>"
        )

    # Interleave question rows and answer rows
    body_rows = []
    for qr, ar in zip(rows[1:], ans_rows):
        body_rows.append(qr)
        body_rows.append(ar)

    body = (
        tip + controls
        + f"<table>\n{rows[0]}\n"
        + "\n".join(body_rows)
        + "\n</table>\n"
    )
    return _html_doc(title, subtitle, body)


def build_cloze_l1_md(stanza: dict[str, Any], word_lookup: dict[str, str]) -> str:
    letter = stanza["letter"]
    name = stanza["name"]
    v_start = stanza["verses"][0]["abs_num"]
    v_end = stanza["verses"][-1]["abs_num"]

    lines = [
        f"# Psalm 119 — {letter} {name} — Cloze Level 1",
        "",
        f"*Ps 119:{v_start}–{v_end} · Key vocabulary words blanked*",
        "",
        "| # | Verse (blanked) | Key Word(s) — Gloss |",
        "|---|---|---|",
    ]
    for v in stanza["verses"]:
        ref = f"119:{v['abs_num']}"
        blanked = v["hebrew"]
        key_words = v.get("key_words") or []
        for kw in key_words:
            blanked = blank_key_word(blanked, kw)
        answers = []
        for kw in key_words:
            gloss = lookup_gloss(kw, word_lookup)
            answers.append(f"{kw}" + (f" — {gloss}" if gloss else ""))
        ans_str = " | ".join(answers) if answers else "—"
        lines.append(f"| {ref} | {blanked} | {ans_str} |")

    lines += ["", "---", "", "## Answer Key", "", "| # | Full Hebrew Verse | Key Word(s) |", "|---|---|---|"]
    for v in stanza["verses"]:
        ref = f"119:{v['abs_num']}"
        key_words = v.get("key_words") or []
        kw_list = ", ".join(key_words) if key_words else "—"
        lines.append(f"| {ref} | {v['hebrew']} | {kw_list} |")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Cloze L2 — line endings blanked
# ---------------------------------------------------------------------------
def build_cloze_l2_html(stanza: dict[str, Any], word_lookup: dict[str, str]) -> str:
    letter = stanza["letter"]
    name = stanza["name"]
    v_start = stanza["verses"][0]["abs_num"]
    v_end = stanza["verses"][-1]["abs_num"]
    title = f"Psalm 119 — {letter} {name} — Cloze Fill-in Level 2"
    subtitle = (
        f"Ps 119:{v_start}–{v_end} · Line-ending words blanked · "
        f"Advanced recall of verse endings"
    )

    tip = (
        '<div class="tip"><strong>Level 2:</strong> The last word of each half-line is blanked. '
        "This is the hardest part of verse memorization — the cadence-word you must produce from memory.</div>"
    )
    controls = (
        '<div class="controls">'
        '<button onclick="showAll()">Show All Answers</button>'
        '<button onclick="hideAll()">Hide All Answers</button>'
        '<button onclick="clearAll()">Clear All Inputs</button>'
        "</div>"
    )

    rows = ["<tr><th>#</th><th>Verse — fill in the endings</th><th>Missing ending(s)</th><th></th></tr>"]
    ans_rows = []

    for i, v in enumerate(stanza["verses"]):
        ref = f"119:{v['abs_num']}"
        endings = v.get("line_endings") or []
        blanked = v["hebrew"]
        for ending in endings:
            blanked = blank_key_word(blanked, ending)

        inputs = "".join(
            f'<input class="parse-field" id="cl2_{i}_{j}" '
            f'placeholder="line ending" dir="rtl">'
            for j in range(len(endings) if endings else 1)
        )

        rows.append(
            f"<tr>"
            f"<td>{safe_html(ref)}</td>"
            f"<td><span class='heb'>{safe_html(blanked)}</span></td>"
            f"<td>{inputs}</td>"
            f"<td><button class='reveal-btn' onclick=\"toggle('a-cl2-{i}')\">▶ Answer</button></td>"
            f"</tr>"
        )

        answers = []
        for ending in endings:
            gloss = lookup_gloss(ending, word_lookup)
            answers.append(
                f"<span class='heb-inline'>{safe_html(ending)}</span>"
                + (f" — {safe_html(gloss)}" if gloss else "")
            )
        ans_text = " &nbsp;|&nbsp; ".join(answers) if answers else "—"

        ans_rows.append(
            f"<tr class='answer-row' id='a-cl2-{i}'>"
            f"<td>✓ {safe_html(ref)}</td>"
            f"<td><span class='heb'>{safe_html(v['hebrew'])}</span></td>"
            f"<td>{ans_text}</td>"
            f"<td></td>"
            f"</tr>"
        )

    body_rows = []
    for qr, ar in zip(rows[1:], ans_rows):
        body_rows.append(qr)
        body_rows.append(ar)

    body = (
        tip + controls
        + f"<table>\n{rows[0]}\n"
        + "\n".join(body_rows)
        + "\n</table>\n"
    )
    return _html_doc(title, subtitle, body)


def build_cloze_l2_md(stanza: dict[str, Any], word_lookup: dict[str, str]) -> str:
    letter = stanza["letter"]
    name = stanza["name"]
    v_start = stanza["verses"][0]["abs_num"]
    v_end = stanza["verses"][-1]["abs_num"]

    lines = [
        f"# Psalm 119 — {letter} {name} — Cloze Level 2",
        "",
        f"*Ps 119:{v_start}–{v_end} · Line-ending words blanked*",
        "",
        "| # | Verse (blanked) | Line Ending(s) — Gloss |",
        "|---|---|---|",
    ]
    for v in stanza["verses"]:
        ref = f"119:{v['abs_num']}"
        endings = v.get("line_endings") or []
        blanked = v["hebrew"]
        for e in endings:
            blanked = blank_key_word(blanked, e)
        answers = []
        for e in endings:
            gloss = lookup_gloss(e, word_lookup)
            answers.append(e + (f" — {gloss}" if gloss else ""))
        ans_str = " | ".join(answers) if answers else "—"
        lines.append(f"| {ref} | {blanked} | {ans_str} |")

    lines += ["", "---", "", "## Answer Key", "", "| # | Full Hebrew Verse | Line Ending(s) |", "|---|---|---|"]
    for v in stanza["verses"]:
        ref = f"119:{v['abs_num']}"
        endings = v.get("line_endings") or []
        lines.append(f"| {ref} | {v['hebrew']} | {', '.join(endings) if endings else '—'} |")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Verse ordering
# ---------------------------------------------------------------------------
def _shuffled_order(stanza: dict[str, Any]) -> list[int]:
    rng = random.Random(stanza["num"] * 7)
    order = list(range(8))
    rng.shuffle(order)
    return order


def build_verse_order_html(stanza: dict[str, Any]) -> str:
    letter = stanza["letter"]
    name = stanza["name"]
    v_start = stanza["verses"][0]["abs_num"]
    v_end = stanza["verses"][-1]["abs_num"]
    title = f"Psalm 119 — {letter} {name} — Verse Ordering"
    subtitle = (
        f"Ps 119:{v_start}–{v_end} · "
        f"Number each verse 1–8 in canonical order, then click ▶ Answer"
    )

    tip = (
        '<div class="tip"><strong>Verse ordering:</strong> The 8 verses are shown in scrambled order. '
        "Assign each verse its correct position (1–8) using the dropdown.</div>"
    )
    controls = (
        '<div class="controls">'
        '<button onclick="showAll()">Show All Answers</button>'
        '<button onclick="hideAll()">Hide All Answers</button>'
        '<button onclick="clearAll()">Clear All Inputs</button>'
        "</div>"
    )

    shuffled = _shuffled_order(stanza)
    verses = stanza["verses"]

    opts = "".join(
        f'<option value="{n}">{n}</option>'
        for n in range(1, 9)
    )
    select_tmpl = f'<select class="parse-field"><option value="">—</option>{opts}</select>'

    rows = ["<tr><th>Verse</th><th>Hebrew</th><th>Position (1–8)</th><th></th></tr>"]
    ans_rows = []
    for disp_idx, orig_idx in enumerate(shuffled):
        v = verses[orig_idx]
        correct_pos = orig_idx + 1
        ref = f"119:{v['abs_num']}"
        lbl = chr(65 + disp_idx)  # A, B, C ...

        rows.append(
            f"<tr>"
            f"<td><strong>{lbl}</strong></td>"
            f"<td><span class='heb'>{safe_html(v['hebrew'])}</span></td>"
            f"<td>{select_tmpl}</td>"
            f"<td><button class='reveal-btn' onclick=\"toggle('a-vo-{disp_idx}')\">▶ Answer</button></td>"
            f"</tr>"
        )
        ans_rows.append(
            f"<tr class='answer-row' id='a-vo-{disp_idx}'>"
            f"<td>✓ {lbl}</td>"
            f"<td><span class='heb'>{safe_html(v['hebrew'])}</span></td>"
            f"<td><strong>Position {correct_pos}</strong> ({safe_html(ref)}) — "
            f"starts: <span class='heb-inline'>{safe_html(v['first_word'])}</span></td>"
            f"<td></td>"
            f"</tr>"
        )

    body_rows = []
    for qr, ar in zip(rows[1:], ans_rows):
        body_rows.append(qr)
        body_rows.append(ar)

    body = (
        tip + controls
        + f"<table>\n{rows[0]}\n"
        + "\n".join(body_rows)
        + "\n</table>\n"
    )
    return _html_doc(title, subtitle, body)


def build_verse_order_md(stanza: dict[str, Any]) -> str:
    letter = stanza["letter"]
    name = stanza["name"]
    v_start = stanza["verses"][0]["abs_num"]
    v_end = stanza["verses"][-1]["abs_num"]
    shuffled = _shuffled_order(stanza)
    verses = stanza["verses"]

    lines = [
        f"# Psalm 119 — {letter} {name} — Verse Ordering",
        "",
        f"*Ps 119:{v_start}–{v_end} · Number each verse 1–8 in canonical order*",
        "",
        "| Label | Hebrew Verse | Your Order |",
        "|---|---|---|",
    ]
    for disp_idx, orig_idx in enumerate(shuffled):
        v = verses[orig_idx]
        lbl = chr(65 + disp_idx)
        lines.append(f"| {lbl} | {v['hebrew']} | ___ |")

    lines += ["", "---", "", "## Answer Key", "", "| Label | Correct Position | First Word |", "|---|---|---|"]
    for disp_idx, orig_idx in enumerate(shuffled):
        v = verses[orig_idx]
        lbl = chr(65 + disp_idx)
        lines.append(f"| {lbl} | {orig_idx + 1} | {v['first_word']} |")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# First-word prompt
# ---------------------------------------------------------------------------
def build_first_word_html(stanza: dict[str, Any]) -> str:
    letter = stanza["letter"]
    name = stanza["name"]
    v_start = stanza["verses"][0]["abs_num"]
    v_end = stanza["verses"][-1]["abs_num"]
    title = f"Psalm 119 — {letter} {name} — First-Word Prompt"
    subtitle = (
        f"Ps 119:{v_start}–{v_end} · Given the first word, recite the full verse from memory"
    )

    tip = (
        '<div class="tip"><strong>Advanced recall:</strong> Given the verse reference and first word, '
        "type the complete Hebrew verse from memory. Click ▶ Answer to check.</div>"
    )
    controls = (
        '<div class="controls">'
        '<button onclick="showAll()">Show All Answers</button>'
        '<button onclick="hideAll()">Hide All Answers</button>'
        '<button onclick="clearAll()">Clear All Inputs</button>'
        "</div>"
    )

    rows = [
        "<tr><th>#</th><th>First Word</th><th>Your full verse</th><th></th></tr>"
    ]
    ans_rows = []
    for i, v in enumerate(stanza["verses"]):
        ref = f"119:{v['abs_num']}"
        rows.append(
            f"<tr>"
            f"<td>{safe_html(ref)}</td>"
            f"<td><span class='heb-inline'>{safe_html(v['first_word'])}</span></td>"
            f"<td><textarea class='heb-area' id='fw_{i}' placeholder='type the full verse…'></textarea></td>"
            f"<td><button class='reveal-btn' onclick=\"toggle('a-fw-{i}')\">▶ Answer</button></td>"
            f"</tr>"
        )
        ans_rows.append(
            f"<tr class='answer-row' id='a-fw-{i}'>"
            f"<td>✓ {safe_html(ref)}</td>"
            f"<td></td>"
            f"<td><span class='heb'>{safe_html(v['hebrew'])}</span>"
            f"<em style='display:block;color:#555;font-size:.9em;margin-top:.3em'>{safe_html(v['kjv'])}</em></td>"
            f"<td></td>"
            f"</tr>"
        )

    body_rows = []
    for qr, ar in zip(rows[1:], ans_rows):
        body_rows.append(qr)
        body_rows.append(ar)

    body = (
        tip + controls
        + f"<table>\n{rows[0]}\n"
        + "\n".join(body_rows)
        + "\n</table>\n"
    )
    return _html_doc(title, subtitle, body)


def build_first_word_md(stanza: dict[str, Any]) -> str:
    letter = stanza["letter"]
    name = stanza["name"]
    v_start = stanza["verses"][0]["abs_num"]
    v_end = stanza["verses"][-1]["abs_num"]

    lines = [
        f"# Psalm 119 — {letter} {name} — First-Word Prompt",
        "",
        f"*Ps 119:{v_start}–{v_end} · Given the first word, recite the full verse*",
        "",
        "| # | First Word | Your Full Verse |",
        "|---|---|---|",
    ]
    for v in stanza["verses"]:
        lines.append(f"| 119:{v['abs_num']} | {v['first_word']} | |")

    lines += ["", "---", "", "## Answer Key", "", "| # | Full Hebrew Verse | KJV |", "|---|---|---|"]
    for v in stanza["verses"]:
        kjv_clean = v["kjv"].replace("|", "\\|")
        lines.append(f"| 119:{v['abs_num']} | {v['hebrew']} | {kjv_clean} |")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Anki decks
# ---------------------------------------------------------------------------
def build_vocab_deck(
    stanza: dict[str, Any], word_lookup: dict[str, str], slug: str
) -> dict[str, str]:
    letter = stanza["letter"]
    name = stanza["name"]
    deck_name = f"Psalm 119 — {letter} {name} — Vocabulary"
    tag = f"ps119 ps119-{slug} ps119-vocab"

    cards: list[tuple[str, str]] = []
    seen: set[str] = set()
    for v in stanza["verses"]:
        for kw in (v.get("key_words") or []):
            if kw in seen:
                continue
            seen.add(kw)
            gloss = lookup_gloss(kw, word_lookup)
            gloss_str = gloss if gloss else "(see verse)"
            ref = f"Ps 119:{v['abs_num']}"
            front = f"{kw} ({ref})"
            back = gloss_str
            cards.append((front, back))

    # .txt — Anki import format
    txt_lines = [
        "#separator:tab",
        "#html:false",
        "#notetype:Basic",
        f"#deck:{deck_name}",
        "#tags column:3",
    ]
    for front, back in cards:
        txt_lines.append(f"{front}\t{back}\t{tag}")

    # -fd.txt — FrontDoor format
    fd_lines = [f"{front}\t{back}\t{deck_name}" for front, back in cards]

    # .md — display
    md_lines = [
        f"# {deck_name}",
        "",
        f"*{len(cards)} key vocabulary words from Psalm 119:{stanza['verses'][0]['abs_num']}"
        f"–{stanza['verses'][-1]['abs_num']}.*",
        f"*Import `ps119-{slug}-vocab-deck.txt` into Anki (File → Import).*",
        "",
        "---",
        "",
        "## Card List",
        "",
        "| # | Hebrew Form | Gloss |",
        "|---|---|---|",
    ]
    for i, (front, back) in enumerate(cards, 1):
        heb = front.split(" (")[0]
        md_lines.append(f"| {i} | {heb} | {back} |")

    return {
        "txt": "\n".join(txt_lines) + "\n",
        "fd": "\n".join(fd_lines) + "\n",
        "md": "\n".join(md_lines) + "\n",
    }


def build_verse_deck(stanza: dict[str, Any], slug: str) -> dict[str, str]:
    letter = stanza["letter"]
    name = stanza["name"]
    deck_name = f"Psalm 119 — {letter} {name} — Verse Recitation"
    tag = f"ps119 ps119-{slug} ps119-verse"

    cards: list[tuple[str, str]] = []
    for v in stanza["verses"]:
        ref = f"Ps 119:{v['abs_num']}"
        # Type A: first word → full verse
        front_a = f"{letter} · {ref} · {v['first_word']}"
        back_a = v["hebrew"]
        cards.append((front_a, back_a))
        # Type B: English → full verse
        front_b = f"[{ref}] {v['kjv']}"
        back_b = v["hebrew"]
        cards.append((front_b, back_b))

    txt_lines = [
        "#separator:tab",
        "#html:false",
        "#notetype:Basic",
        f"#deck:{deck_name}",
        "#tags column:3",
    ]
    for front, back in cards:
        txt_lines.append(f"{front}\t{back}\t{tag}")

    fd_lines = [f"{front}\t{back}\t{deck_name}" for front, back in cards]

    md_lines = [
        f"# {deck_name}",
        "",
        f"*{len(cards)} cards ({len(stanza['verses'])} verses × 2 card types) for "
        f"Psalm 119:{stanza['verses'][0]['abs_num']}–{stanza['verses'][-1]['abs_num']}.*",
        f"*Import `ps119-{slug}-verse-deck.txt` into Anki (File → Import).*",
        "",
        "**Type A** — First-word prompt → full Hebrew verse",
        "",
        "**Type B** — English gloss → full Hebrew verse",
        "",
        "---",
        "",
        "## Card List",
        "",
        "| # | Type | Front | Back |",
        "|---|---|---|---|",
    ]
    for i, (front, back) in enumerate(cards, 1):
        card_type = "A" if i % 2 == 1 else "B"
        md_lines.append(f"| {i} | {card_type} | {front} | {back} |")

    return {
        "txt": "\n".join(txt_lines) + "\n",
        "fd": "\n".join(fd_lines) + "\n",
        "md": "\n".join(md_lines) + "\n",
    }


# ---------------------------------------------------------------------------
# Section index.md
# ---------------------------------------------------------------------------
def build_section_index(stanza: dict[str, Any], slug: str) -> str:
    letter = stanza["letter"]
    name = stanza["name"]
    v_start = stanza["verses"][0]["abs_num"]
    v_end = stanza["verses"][-1]["abs_num"]

    lines = [
        f"# Psalm 119 — {letter} {name} Section (vv. {v_start}–{v_end})",
        "",
        f"The **{letter} ({name})** stanza of Psalm 119 comprises verses {v_start}–{v_end}.",
        "Each of the 8 verses begins with the Hebrew letter "
        f"**{letter}**.",
        "",
        "---",
        "",
        "## Verses at a Glance",
        "",
        "| # | Hebrew | KJV |",
        "|---|---|---|",
    ]
    for v in stanza["verses"]:
        kjv_clean = v["kjv"].replace("|", "\\|")
        lines.append(f"| {v['abs_num']} | {v['hebrew']} | {kjv_clean} |")

    lines += [
        "",
        "---",
        "",
        "## Exercises",
        "",
        "| Exercise | Description | Formats |",
        "|---|---|---|",
        "| [Cloze Level 1](exercises/cloze-l1/cloze-l1.html) | Key vocabulary words blanked | "
        "[HTML](exercises/cloze-l1/cloze-l1.html) · [PDF](exercises/cloze-l1/cloze-l1.pdf) · "
        "[MD](exercises/cloze-l1/cloze-l1.md) |",
        "| [Cloze Level 2](exercises/cloze-l2/cloze-l2.html) | Line-ending words blanked | "
        "[HTML](exercises/cloze-l2/cloze-l2.html) · [PDF](exercises/cloze-l2/cloze-l2.pdf) · "
        "[MD](exercises/cloze-l2/cloze-l2.md) |",
        "| [Verse Ordering](exercises/verse-order/verse-order.html) | Restore canonical verse order | "
        "[HTML](exercises/verse-order/verse-order.html) · [PDF](exercises/verse-order/verse-order.pdf) · "
        "[MD](exercises/verse-order/verse-order.md) |",
        "| [First-Word Prompt](exercises/first-word/first-word.html) | Recall full verse from first word | "
        "[HTML](exercises/first-word/first-word.html) · [PDF](exercises/first-word/first-word.pdf) · "
        "[MD](exercises/first-word/first-word.md) |",
        "",
        "---",
        "",
        "## Anki Flashcard Decks",
        "",
        "| Deck | Description | Download |",
        "|---|---|---|",
        f"| Vocabulary | Key words from this section | "
        f"[.txt](anki/ps119-{slug}-vocab-deck.txt) · "
        f"[FrontDoor](anki/ps119-{slug}-vocab-deck-fd.txt) · "
        f"[Preview](anki/ps119-{slug}-vocab-deck.md) |",
        f"| Verse Recitation | First-word → verse + English → verse | "
        f"[.txt](anki/ps119-{slug}-verse-deck.txt) · "
        f"[FrontDoor](anki/ps119-{slug}-verse-deck-fd.txt) · "
        f"[Preview](anki/ps119-{slug}-verse-deck.md) |",
        "",
        "---",
        "",
        "## Reference Card",
        "",
        f"[Download PDF reference card](ps119-{slug}-reference.pdf) — "
        "Hebrew and KJV side-by-side, suitable for printing.",
    ]

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# PDF generation
# ---------------------------------------------------------------------------

def _setup_pdf_page(c: rl_canvas.Canvas, title: str, subtitle: str = "") -> float:
    """Draw title/subtitle, return starting y position for content."""
    _register_fonts()
    W, H = LETTER
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(HexColor("#2a4a6e"))
    c.drawString(0.75 * inch, H - 0.75 * inch, title)
    y = H - 1.0 * inch
    if subtitle:
        c.setFont("Helvetica", 9)
        c.setFillColor(HexColor("#555555"))
        c.drawString(0.75 * inch, y, subtitle)
        y -= 0.2 * inch
    c.setStrokeColor(HexColor("#cccccc"))
    c.line(0.75 * inch, y, W - 0.75 * inch, y)
    return y - 0.2 * inch


def _draw_heb(c: rl_canvas.Canvas, text: str, x: float, y: float, font_size: float = 11) -> None:
    try:
        c.setFont("ArialHebrew", font_size)
    except Exception:
        c.setFont("Helvetica", font_size)
    c.drawString(x, y, _heb(text))


def build_reference_card_pdf(stanza: dict[str, Any], out_path: Path) -> None:
    """Two-column reference card: Hebrew | KJV, 8 verses."""
    _register_fonts()
    letter = stanza["letter"]
    name = stanza["name"]
    v_start = stanza["verses"][0]["abs_num"]
    v_end = stanza["verses"][-1]["abs_num"]
    title = f"Psalm 119 — {letter} {name} — Reference Card"
    subtitle = f"Verses {v_start}–{v_end}"

    W, H = LETTER
    c = rl_canvas.Canvas(str(out_path), pagesize=LETTER)
    y = _setup_pdf_page(c, title, subtitle)

    row_h = 0.7 * inch
    col_heb = 0.75 * inch
    col_kjv = W / 2 + 0.1 * inch
    col_heb_w = W / 2 - 1.0 * inch
    col_kjv_w = W / 2 - 0.85 * inch

    # Header row
    c.setFillColor(HexColor("#2a4a6e"))
    c.rect(col_heb - 0.05 * inch, y - 0.25 * inch, col_heb_w, 0.25 * inch, fill=1, stroke=0)
    c.rect(col_kjv - 0.05 * inch, y - 0.25 * inch, col_kjv_w, 0.25 * inch, fill=1, stroke=0)
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(col_heb, y - 0.18 * inch, "Hebrew")
    c.drawString(col_kjv, y - 0.18 * inch, "KJV")
    y -= 0.3 * inch

    for v in stanza["verses"]:
        if y < 1.0 * inch:
            c.showPage()
            y = H - 0.75 * inch

        # Light alternating background
        row_bg = HexColor("#f0f6ff") if v["num"] % 2 == 0 else HexColor("#ffffff")
        c.setFillColor(row_bg)
        c.rect(col_heb - 0.05 * inch, y - row_h + 0.05 * inch, W - 1.45 * inch, row_h, fill=1, stroke=0)

        # Verse number
        c.setFillColor(HexColor("#888888"))
        c.setFont("Helvetica", 8)
        c.drawString(0.4 * inch, y - 0.2 * inch, str(v["abs_num"]))

        # Hebrew (RTL)
        c.setFillColor(black)
        _draw_heb(c, v["hebrew"], col_heb, y - 0.22 * inch, 10)

        # KJV (LTR, wrapped)
        c.setFont("Helvetica", 8.5)
        c.setFillColor(HexColor("#333333"))
        from reportlab.lib.utils import simpleSplit
        words_wrapped = simpleSplit(v["kjv"], "Helvetica", 8.5, col_kjv_w)
        ly = y - 0.18 * inch
        for line in words_wrapped[:3]:
            c.drawString(col_kjv, ly, line)
            ly -= 0.13 * inch

        # Rule below row
        c.setStrokeColor(HexColor("#dddddd"))
        c.line(col_heb - 0.05 * inch, y - row_h + 0.05 * inch,
               W - 0.7 * inch, y - row_h + 0.05 * inch)
        y -= row_h

    c.save()


def build_cloze_pdf(
    stanza: dict[str, Any],
    level: int,
    word_lookup: dict[str, str],
    out_path: Path,
) -> None:
    """Fillable cloze PDF with AcroForm text fields."""
    _register_fonts()
    letter = stanza["letter"]
    name = stanza["name"]
    v_start = stanza["verses"][0]["abs_num"]
    v_end = stanza["verses"][-1]["abs_num"]
    label = "Key Vocabulary" if level == 1 else "Line Endings"
    title = f"Psalm 119 — {letter} {name} — Cloze Level {level}"
    subtitle = f"Ps 119:{v_start}–{v_end} · {label} blanked"

    W, H = LETTER
    c = rl_canvas.Canvas(str(out_path), pagesize=LETTER)
    y = _setup_pdf_page(c, title, subtitle)

    row_h = 0.9 * inch
    for i, v in enumerate(stanza["verses"]):
        if y < 1.2 * inch:
            c.showPage()
            y = H - 0.75 * inch

        ref = f"119:{v['abs_num']}"
        if level == 1:
            words_to_blank = v.get("key_words") or []
            blanked = v["hebrew"]
            for kw in words_to_blank:
                blanked = blank_key_word(blanked, kw)
        else:
            words_to_blank = v.get("line_endings") or []
            blanked = v["hebrew"]
            for e in words_to_blank:
                blanked = blank_key_word(blanked, e)

        # Ref
        c.setFillColor(HexColor("#444444"))
        c.setFont("Helvetica-Bold", 9)
        c.drawString(0.75 * inch, y - 0.18 * inch, ref)

        # Hebrew with blanks
        _draw_heb(c, blanked, 1.5 * inch, y - 0.18 * inch, 10)

        # Input fields for blanks
        for j in range(len(words_to_blank) or 1):
            field_x = 0.75 * inch + j * 1.8 * inch
            field_y = y - 0.55 * inch
            c.acroForm.textfield(
                name=f"cloze{level}_v{i}_b{j}",
                x=field_x, y=field_y,
                width=1.6 * inch, height=0.25 * inch,
                fontSize=10,
                borderStyle="underlined",
                fieldFlags="",
            )

        c.setStrokeColor(HexColor("#dddddd"))
        c.line(0.75 * inch, y - row_h + 0.05 * inch, W - 0.75 * inch, y - row_h + 0.05 * inch)
        y -= row_h

    c.save()


def build_verse_order_pdf(stanza: dict[str, Any], out_path: Path) -> None:
    """Fillable verse-ordering PDF."""
    _register_fonts()
    letter = stanza["letter"]
    name = stanza["name"]
    v_start = stanza["verses"][0]["abs_num"]
    v_end = stanza["verses"][-1]["abs_num"]
    title = f"Psalm 119 — {letter} {name} — Verse Ordering"
    subtitle = f"Ps 119:{v_start}–{v_end} · Write the correct position (1–8) for each verse"

    W, H = LETTER
    c = rl_canvas.Canvas(str(out_path), pagesize=LETTER)
    y = _setup_pdf_page(c, title, subtitle)

    shuffled = _shuffled_order(stanza)
    verses = stanza["verses"]
    row_h = 0.8 * inch

    for disp_idx, orig_idx in enumerate(shuffled):
        if y < 1.2 * inch:
            c.showPage()
            y = H - 0.75 * inch
        v = verses[orig_idx]
        lbl = chr(65 + disp_idx)

        c.setFillColor(HexColor("#444444"))
        c.setFont("Helvetica-Bold", 10)
        c.drawString(0.75 * inch, y - 0.2 * inch, lbl)

        _draw_heb(c, v["hebrew"], 1.1 * inch, y - 0.2 * inch, 10)

        c.acroForm.textfield(
            name=f"vo_{disp_idx}",
            x=W - 1.3 * inch, y=y - 0.35 * inch,
            width=0.5 * inch, height=0.25 * inch,
            fontSize=12,
            borderStyle="underlined",
            tooltip=f"Position of verse {lbl}",
        )

        c.setStrokeColor(HexColor("#dddddd"))
        c.line(0.75 * inch, y - row_h + 0.05 * inch, W - 0.75 * inch, y - row_h + 0.05 * inch)
        y -= row_h

    c.save()


def build_first_word_pdf(stanza: dict[str, Any], out_path: Path) -> None:
    """Fillable first-word-prompt PDF."""
    _register_fonts()
    letter = stanza["letter"]
    name = stanza["name"]
    v_start = stanza["verses"][0]["abs_num"]
    v_end = stanza["verses"][-1]["abs_num"]
    title = f"Psalm 119 — {letter} {name} — First-Word Prompt"
    subtitle = f"Ps 119:{v_start}–{v_end} · Write the full verse from memory"

    W, H = LETTER
    c = rl_canvas.Canvas(str(out_path), pagesize=LETTER)
    y = _setup_pdf_page(c, title, subtitle)

    row_h = 1.0 * inch
    for i, v in enumerate(stanza["verses"]):
        if y < 1.3 * inch:
            c.showPage()
            y = H - 0.75 * inch

        ref = f"119:{v['abs_num']}"
        c.setFillColor(HexColor("#444444"))
        c.setFont("Helvetica-Bold", 9)
        c.drawString(0.75 * inch, y - 0.18 * inch, ref)

        _draw_heb(c, v["first_word"], 1.5 * inch, y - 0.18 * inch, 11)

        c.acroForm.textfield(
            name=f"fw_{i}",
            x=0.75 * inch, y=y - 0.65 * inch,
            width=W - 1.5 * inch, height=0.35 * inch,
            fontSize=10,
            borderStyle="underlined",
            tooltip=f"Full verse for {ref}",
        )

        c.setStrokeColor(HexColor("#dddddd"))
        c.line(0.75 * inch, y - row_h + 0.05 * inch, W - 0.75 * inch, y - row_h + 0.05 * inch)
        y -= row_h

    c.save()


# ---------------------------------------------------------------------------
# Per-section builder
# ---------------------------------------------------------------------------
def build_section(
    stanza: dict[str, Any], word_lookup: dict[str, str], out_base: Path
) -> None:
    slug = make_slug(stanza)
    out = out_base / slug
    out.mkdir(parents=True, exist_ok=True)

    # Section index
    (out / "index.md").write_text(build_section_index(stanza, slug), encoding="utf-8")

    # Anki decks
    anki_dir = out / "anki"
    anki_dir.mkdir(exist_ok=True)
    vocab = build_vocab_deck(stanza, word_lookup, slug)
    (anki_dir / f"ps119-{slug}-vocab-deck.txt").write_text(vocab["txt"], encoding="utf-8")
    (anki_dir / f"ps119-{slug}-vocab-deck-fd.txt").write_text(vocab["fd"], encoding="utf-8")
    (anki_dir / f"ps119-{slug}-vocab-deck.md").write_text(vocab["md"], encoding="utf-8")

    verse = build_verse_deck(stanza, slug)
    (anki_dir / f"ps119-{slug}-verse-deck.txt").write_text(verse["txt"], encoding="utf-8")
    (anki_dir / f"ps119-{slug}-verse-deck-fd.txt").write_text(verse["fd"], encoding="utf-8")
    (anki_dir / f"ps119-{slug}-verse-deck.md").write_text(verse["md"], encoding="utf-8")

    # Exercises
    ex_dir = out / "exercises"
    ex_dir.mkdir(exist_ok=True)

    # Cloze L1
    cl1_dir = ex_dir / "cloze-l1"
    cl1_dir.mkdir(exist_ok=True)
    (cl1_dir / "cloze-l1.html").write_text(build_cloze_l1_html(stanza, word_lookup), encoding="utf-8")
    (cl1_dir / "cloze-l1.md").write_text(build_cloze_l1_md(stanza, word_lookup), encoding="utf-8")
    build_cloze_pdf(stanza, 1, word_lookup, cl1_dir / "cloze-l1.pdf")

    # Cloze L2
    cl2_dir = ex_dir / "cloze-l2"
    cl2_dir.mkdir(exist_ok=True)
    (cl2_dir / "cloze-l2.html").write_text(build_cloze_l2_html(stanza, word_lookup), encoding="utf-8")
    (cl2_dir / "cloze-l2.md").write_text(build_cloze_l2_md(stanza, word_lookup), encoding="utf-8")
    build_cloze_pdf(stanza, 2, word_lookup, cl2_dir / "cloze-l2.pdf")

    # Verse ordering
    vo_dir = ex_dir / "verse-order"
    vo_dir.mkdir(exist_ok=True)
    (vo_dir / "verse-order.html").write_text(build_verse_order_html(stanza), encoding="utf-8")
    (vo_dir / "verse-order.md").write_text(build_verse_order_md(stanza), encoding="utf-8")
    build_verse_order_pdf(stanza, vo_dir / "verse-order.pdf")

    # First-word prompt
    fw_dir = ex_dir / "first-word"
    fw_dir.mkdir(exist_ok=True)
    (fw_dir / "first-word.html").write_text(build_first_word_html(stanza), encoding="utf-8")
    (fw_dir / "first-word.md").write_text(build_first_word_md(stanza), encoding="utf-8")
    build_first_word_pdf(stanza, fw_dir / "first-word.pdf")

    # Reference card
    build_reference_card_pdf(stanza, out / f"ps119-{slug}-reference.pdf")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    stanzas = load_stanzas()
    print("build_psalm119_memorization: loading word glosses...")
    word_lookup = build_word_lookup()
    print(f"  {len(word_lookup)} words indexed.")

    MKDOCS_OUT.mkdir(parents=True, exist_ok=True)

    for stanza in stanzas:
        slug = make_slug(stanza)
        print(f"  Building {slug}...", end=" ", flush=True)
        build_section(stanza, word_lookup, MKDOCS_OUT)
        print("done")

    print(f"build_psalm119_memorization: {len(stanzas)} sections written to {MKDOCS_OUT}")


if __name__ == "__main__":
    main()
