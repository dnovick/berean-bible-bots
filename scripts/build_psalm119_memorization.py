#!/usr/bin/env python3
"""Build Psalm 119 memorization exercises for all 22 acrostic sections.

HTML/MD/Anki content is generated from psalm-119-text.yaml (pyyaml only — no
heavy dependencies, works in CI).

PDFs are generated locally using reportlab + ArialHebrew font and stored in
data/studies/psalm-119/memorization/<slug>/ so CI can copy them to mkdocs_src/
without needing reportlab or macOS fonts.

Run standalone:
    python scripts/build_psalm119_memorization.py
"""

from __future__ import annotations

import re
import random
import html
import shutil
from pathlib import Path
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# Optional PDF dependencies (reportlab + bidi — only available locally)
# ---------------------------------------------------------------------------
try:
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, black
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas as rl_canvas
    from bidi.algorithm import get_display as _bidi_get_display
    _PDF_AVAILABLE = True
except ImportError:
    _PDF_AVAILABLE = False

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO = Path(__file__).resolve().parent.parent
DATA_YAML = REPO / "data" / "studies" / "psalm-119" / "psalm-119-text.yaml"
DATA_MEM = REPO / "data" / "studies" / "psalm-119" / "memorization"
MKDOCS_OUT = REPO / "mkdocs_src" / "studies" / "psalm-119" / "memorization"

# ---------------------------------------------------------------------------
# Data loading  (glosses embedded in YAML — no parquet/pandas needed)
# ---------------------------------------------------------------------------


def load_stanzas() -> list[dict[str, Any]]:
    with open(DATA_YAML, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["stanzas"]


def _kw_pairs(entries: list[Any]) -> list[tuple[str, str]]:
    """Return (word, gloss) pairs from key_words / line_endings entries.

    Entries may be plain strings (old format) or {word, gloss} dicts (new).
    """
    pairs: list[tuple[str, str]] = []
    for e in (entries or []):
        if isinstance(e, dict):
            pairs.append((e.get("word", ""), e.get("gloss", "")))
        else:
            pairs.append((str(e), ""))
    return pairs


# ---------------------------------------------------------------------------
# Slug helper
# ---------------------------------------------------------------------------

def make_slug(stanza: dict[str, Any]) -> str:
    import unicodedata
    name = stanza["name"].lower()
    name = unicodedata.normalize("NFKD", name)
    name = re.sub(r"[^a-z]", "", name)
    return f"{stanza['num']:02d}-{name}"


# ---------------------------------------------------------------------------
# Verse text helpers
# ---------------------------------------------------------------------------

def _sort_by_position(pairs: list[tuple[str, str]], text: str) -> list[tuple[str, str]]:
    """Return pairs sorted by position in text (ascending = rightmost in RTL display = first read)."""
    def _pos(wg: tuple[str, str]) -> int:
        try:
            return text.index(wg[0])
        except ValueError:
            return len(text)
    return sorted(pairs, key=_pos)


def blank_key_word(text: str, key_word: str) -> str:
    if key_word in text:
        idx = text.index(key_word)
        after = text[idx + len(key_word):]
        m = re.match(r"[־-](\S+)", after)
        if m:
            return text[:idx] + "______" + after[m.end():]
        return text[:idx] + "______" + after
    return text


def safe_html(s: str) -> str:
    return html.escape(s)


# ---------------------------------------------------------------------------
# Common HTML CSS/JS
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
# Cloze L1
# ---------------------------------------------------------------------------

def build_cloze_l1_html(stanza: dict[str, Any]) -> str:
    letter = stanza["letter"]
    name = stanza["name"]
    v_start = stanza["verses"][0]["abs_num"]
    v_end = stanza["verses"][-1]["abs_num"]
    title = f"Psalm 119 — {letter} {name} — Cloze Fill-in Level 1"
    subtitle = (
        f"Ps 119:{v_start}–{v_end} · Key vocabulary words blanked · "
        "Type the missing Hebrew word, then click ▶ Answer"
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
    header = "<tr><th>#</th><th>Verse — fill in the blanks</th><th>Missing word(s)</th><th></th></tr>"
    body_rows: list[str] = []
    for i, v in enumerate(stanza["verses"]):
        ref = f"119:{v['abs_num']}"
        pairs = _kw_pairs(v.get("key_words") or [])
        blanked = v["hebrew"]
        for word, _ in pairs:
            blanked = blank_key_word(blanked, word)
        ordered = _sort_by_position(pairs, v["hebrew"])
        inputs = "".join(
            f'<input class="parse-field" id="cl1_{i}_{j}" placeholder="{safe_html(w)[:1]}…" dir="rtl">'
            for j, (w, _) in enumerate(ordered)
        )
        body_rows.append(
            f"<tr>"
            f"<td>{safe_html(ref)}</td>"
            f"<td><span class='heb'>{safe_html(blanked)}</span></td>"
            f"<td>{inputs}</td>"
            f"<td><button class='reveal-btn' onclick=\"toggle('a-cl1-{i}')\">▶ Answer</button></td>"
            f"</tr>"
        )
        ans_parts = []
        for word, gloss in ordered:
            gs = f" — {safe_html(gloss)}" if gloss else ""
            ans_parts.append(f"<span class='heb-inline'>{safe_html(word)}</span>{gs}")
        ans_text = " &nbsp;|&nbsp; ".join(ans_parts) if ans_parts else "—"
        body_rows.append(
            f"<tr class='answer-row' id='a-cl1-{i}'>"
            f"<td>✓ {safe_html(ref)}</td>"
            f"<td><span class='heb'>{safe_html(v['hebrew'])}</span></td>"
            f"<td>{ans_text}</td><td></td></tr>"
        )
    body = tip + controls + f"<table>\n{header}\n" + "\n".join(body_rows) + "\n</table>\n"
    return _html_doc(title, subtitle, body)


def build_cloze_l1_md(stanza: dict[str, Any]) -> str:
    letter, name = stanza["letter"], stanza["name"]
    v_start, v_end = stanza["verses"][0]["abs_num"], stanza["verses"][-1]["abs_num"]
    lines = [
        f"# Psalm 119 — {letter} {name} — Cloze Level 1",
        "", f"*Ps 119:{v_start}–{v_end} · Key vocabulary words blanked*", "",
        "| # | Verse (blanked) | Key Word(s) — Gloss |", "|---|---|---|",
    ]
    for v in stanza["verses"]:
        pairs = _kw_pairs(v.get("key_words") or [])
        blanked = v["hebrew"]
        for word, _ in pairs:
            blanked = blank_key_word(blanked, word)
        ordered = _sort_by_position(pairs, v["hebrew"])
        ans = " | ".join((f"{w} — {g}" if g else w) for w, g in ordered) or "—"
        lines.append(f"| 119:{v['abs_num']} | {blanked} | {ans} |")
    lines += ["", "---", "", "## Answer Key", "", "| # | Full Verse | Key Word(s) |", "|---|---|---|"]
    for v in stanza["verses"]:
        pairs = _kw_pairs(v.get("key_words") or [])
        kw = ", ".join(w for w, _ in _sort_by_position(pairs, v["hebrew"])) or "—"
        lines.append(f"| 119:{v['abs_num']} | {v['hebrew']} | {kw} |")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Cloze L2
# ---------------------------------------------------------------------------

def build_cloze_l2_html(stanza: dict[str, Any]) -> str:
    letter, name = stanza["letter"], stanza["name"]
    v_start, v_end = stanza["verses"][0]["abs_num"], stanza["verses"][-1]["abs_num"]
    title = f"Psalm 119 — {letter} {name} — Cloze Fill-in Level 2"
    subtitle = f"Ps 119:{v_start}–{v_end} · Line-ending words blanked · Advanced recall"
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
    header = "<tr><th>#</th><th>Verse — fill in the endings</th><th>Missing ending(s)</th><th></th></tr>"
    body_rows: list[str] = []
    for i, v in enumerate(stanza["verses"]):
        ref = f"119:{v['abs_num']}"
        pairs = _kw_pairs(v.get("line_endings") or [])
        blanked = v["hebrew"]
        for word, _ in pairs:
            blanked = blank_key_word(blanked, word)
        ordered = _sort_by_position(pairs, v["hebrew"])
        n = len(ordered) or 1
        inputs = "".join(
            f'<input class="parse-field" id="cl2_{i}_{j}" placeholder="line ending" dir="rtl">'
            for j in range(n)
        )
        body_rows.append(
            f"<tr>"
            f"<td>{safe_html(ref)}</td>"
            f"<td><span class='heb'>{safe_html(blanked)}</span></td>"
            f"<td>{inputs}</td>"
            f"<td><button class='reveal-btn' onclick=\"toggle('a-cl2-{i}')\">▶ Answer</button></td>"
            f"</tr>"
        )
        ans_parts = []
        for word, gloss in ordered:
            gs = f" — {safe_html(gloss)}" if gloss else ""
            ans_parts.append(f"<span class='heb-inline'>{safe_html(word)}</span>{gs}")
        ans_text = " &nbsp;|&nbsp; ".join(ans_parts) if ans_parts else "—"
        body_rows.append(
            f"<tr class='answer-row' id='a-cl2-{i}'>"
            f"<td>✓ {safe_html(ref)}</td>"
            f"<td><span class='heb'>{safe_html(v['hebrew'])}</span></td>"
            f"<td>{ans_text}</td><td></td></tr>"
        )
    body = tip + controls + f"<table>\n{header}\n" + "\n".join(body_rows) + "\n</table>\n"
    return _html_doc(title, subtitle, body)


def build_cloze_l2_md(stanza: dict[str, Any]) -> str:
    letter, name = stanza["letter"], stanza["name"]
    v_start, v_end = stanza["verses"][0]["abs_num"], stanza["verses"][-1]["abs_num"]
    lines = [
        f"# Psalm 119 — {letter} {name} — Cloze Level 2",
        "", f"*Ps 119:{v_start}–{v_end} · Line-ending words blanked*", "",
        "| # | Verse (blanked) | Line Ending(s) — Gloss |", "|---|---|---|",
    ]
    for v in stanza["verses"]:
        pairs = _kw_pairs(v.get("line_endings") or [])
        blanked = v["hebrew"]
        for word, _ in pairs:
            blanked = blank_key_word(blanked, word)
        ordered = _sort_by_position(pairs, v["hebrew"])
        ans = " | ".join((f"{w} — {g}" if g else w) for w, g in ordered) or "—"
        lines.append(f"| 119:{v['abs_num']} | {blanked} | {ans} |")
    lines += ["", "---", "", "## Answer Key", "", "| # | Full Verse | Line Ending(s) |", "|---|---|---|"]
    for v in stanza["verses"]:
        pairs = _kw_pairs(v.get("line_endings") or [])
        ordered = _sort_by_position(pairs, v["hebrew"])
        lines.append(f"| 119:{v['abs_num']} | {v['hebrew']} | {', '.join(w for w, _ in ordered) or '—'} |")
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
    letter, name = stanza["letter"], stanza["name"]
    v_start, v_end = stanza["verses"][0]["abs_num"], stanza["verses"][-1]["abs_num"]
    title = f"Psalm 119 — {letter} {name} — Verse Ordering"
    subtitle = f"Ps 119:{v_start}–{v_end} · Number each verse 1–8 in canonical order, then click ▶ Answer"
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
    opts = "".join(f'<option value="{n}">{n}</option>' for n in range(1, 9))
    select_tmpl = f'<select class="parse-field"><option value="">—</option>{opts}</select>'
    header = "<tr><th>Verse</th><th>Hebrew</th><th>Position (1–8)</th><th></th></tr>"
    body_rows: list[str] = []
    for disp_idx, orig_idx in enumerate(_shuffled_order(stanza)):
        v = stanza["verses"][orig_idx]
        lbl = chr(65 + disp_idx)
        body_rows.append(
            f"<tr>"
            f"<td><strong>{lbl}</strong></td>"
            f"<td><span class='heb'>{safe_html(v['hebrew'])}</span></td>"
            f"<td>{select_tmpl}</td>"
            f"<td><button class='reveal-btn' onclick=\"toggle('a-vo-{disp_idx}')\">▶ Answer</button></td>"
            f"</tr>"
        )
        body_rows.append(
            f"<tr class='answer-row' id='a-vo-{disp_idx}'>"
            f"<td>✓ {lbl}</td>"
            f"<td><span class='heb'>{safe_html(v['hebrew'])}</span></td>"
            f"<td><strong>Position {orig_idx + 1}</strong> (119:{v['abs_num']}) — "
            f"starts: <span class='heb-inline'>{safe_html(v['first_word'])}</span></td>"
            f"<td></td></tr>"
        )
    body = tip + controls + f"<table>\n{header}\n" + "\n".join(body_rows) + "\n</table>\n"
    return _html_doc(title, subtitle, body)


def build_verse_order_md(stanza: dict[str, Any]) -> str:
    letter, name = stanza["letter"], stanza["name"]
    v_start, v_end = stanza["verses"][0]["abs_num"], stanza["verses"][-1]["abs_num"]
    lines = [
        f"# Psalm 119 — {letter} {name} — Verse Ordering",
        "", f"*Ps 119:{v_start}–{v_end} · Number each verse 1–8 in canonical order*", "",
        "| Label | Hebrew Verse | Your Order |", "|---|---|---|",
    ]
    for disp_idx, orig_idx in enumerate(_shuffled_order(stanza)):
        v = stanza["verses"][orig_idx]
        lines.append(f"| {chr(65+disp_idx)} | {v['hebrew']} | ___ |")
    lines += ["", "---", "", "## Answer Key", "", "| Label | Correct Position | First Word |", "|---|---|---|"]
    for disp_idx, orig_idx in enumerate(_shuffled_order(stanza)):
        v = stanza["verses"][orig_idx]
        lines.append(f"| {chr(65+disp_idx)} | {orig_idx + 1} | {v['first_word']} |")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# First-word prompt
# ---------------------------------------------------------------------------

def build_first_word_html(stanza: dict[str, Any]) -> str:
    letter, name = stanza["letter"], stanza["name"]
    v_start, v_end = stanza["verses"][0]["abs_num"], stanza["verses"][-1]["abs_num"]
    title = f"Psalm 119 — {letter} {name} — First-Word Prompt"
    subtitle = f"Ps 119:{v_start}–{v_end} · Given the first word, recite the full verse from memory"
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
    header = "<tr><th>#</th><th>First Word</th><th>Your full verse</th><th></th></tr>"
    body_rows: list[str] = []
    for i, v in enumerate(stanza["verses"]):
        ref = f"119:{v['abs_num']}"
        body_rows.append(
            f"<tr>"
            f"<td>{safe_html(ref)}</td>"
            f"<td><span class='heb-inline'>{safe_html(v['first_word'])}</span></td>"
            f"<td><textarea class='heb-area' id='fw_{i}' placeholder='type the full verse…'></textarea></td>"
            f"<td><button class='reveal-btn' onclick=\"toggle('a-fw-{i}')\">▶ Answer</button></td>"
            f"</tr>"
        )
        body_rows.append(
            f"<tr class='answer-row' id='a-fw-{i}'>"
            f"<td>✓ {safe_html(ref)}</td><td></td>"
            f"<td><span class='heb'>{safe_html(v['hebrew'])}</span>"
            f"<em style='display:block;color:#555;font-size:.9em;margin-top:.3em'>{safe_html(v['kjv'])}</em></td>"
            f"<td></td></tr>"
        )
    body = tip + controls + f"<table>\n{header}\n" + "\n".join(body_rows) + "\n</table>\n"
    return _html_doc(title, subtitle, body)


def build_first_word_md(stanza: dict[str, Any]) -> str:
    letter, name = stanza["letter"], stanza["name"]
    v_start, v_end = stanza["verses"][0]["abs_num"], stanza["verses"][-1]["abs_num"]
    lines = [
        f"# Psalm 119 — {letter} {name} — First-Word Prompt",
        "", f"*Ps 119:{v_start}–{v_end} · Given the first word, recite the full verse*", "",
        "| # | First Word | Your Full Verse |", "|---|---|---|",
    ]
    for v in stanza["verses"]:
        lines.append(f"| 119:{v['abs_num']} | {v['first_word']} | |")
    lines += ["", "---", "", "## Answer Key", "", "| # | Full Verse | KJV |", "|---|---|---|"]
    for v in stanza["verses"]:
        lines.append(f"| 119:{v['abs_num']} | {v['hebrew']} | {v['kjv'].replace('|', chr(92)+'|')} |")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Anki decks
# ---------------------------------------------------------------------------

_STEM_TAG = {
    "Qal": "qal", "Niphal": "niphal", "Piel": "piel", "Pual": "pual",
    "Hiphil": "hiphil", "Hophal": "hophal", "Hithpael": "hithpael",
    "Polel": "polel", "Polal": "polal", "Hithpolel": "hithpolel",
    "Qal-pass": "qal-pass",
}

_CONJ_TAG = {
    "Perf": "perfect", "Impf": "imperfect", "Wqtl": "wayyiqtol",
    "Juss": "jussive", "Impv": "imperative",
    "InfCstr": "inf-cstr", "InfAbs": "inf-abs",
    "Ptc.act": "participle", "Ptc.pass": "ptc-pass",
}


def _kw_back(kw: dict[str, Any]) -> str:
    """Build the back-of-card string from a key_word dict with morphological fields."""
    pos = kw.get("pos", "")
    gloss = kw.get("gloss", "") or "(see verse)"
    lemma = kw.get("lemma", "")
    suffix = kw.get("suffix", "")
    sfx_str = f" + {suffix} sfx" if suffix else ""

    if pos == "verb":
        stem = kw.get("stem", "")
        conj = kw.get("conj", "")
        pgn = kw.get("pgn", "")
        morph = " ".join(x for x in [stem, conj, pgn] if x)
        root_str = f" — root: {lemma}" if lemma else ""
        return f"verb — {morph}{sfx_str}{root_str} — {gloss}"

    if pos == "noun":
        gen = kw.get("gender", "")
        num = kw.get("number", "")
        state = kw.get("state", "")
        morph = ".".join(x for x in [gen, num, state] if x)
        lem_str = f" — lemma: {lemma}" if lemma else ""
        return f"noun {morph}{sfx_str}{lem_str} — {gloss}"

    if pos == "adj":
        gen = kw.get("gender", "")
        num = kw.get("number", "")
        state = kw.get("state", "")
        morph = ".".join(x for x in [gen, num, state] if x)
        lem_str = f" — lemma: {lemma}" if lemma else ""
        return f"adj {morph}{sfx_str}{lem_str} — {gloss}"

    if pos in ("pronoun", "particle"):
        lem_str = f" — lemma: {lemma}" if lemma else ""
        return f"{pos}{lem_str} — {gloss}"

    # Fallback: plain gloss
    return gloss


def _kw_tags(kw: dict[str, Any], base_tags: str) -> str:
    """Build the Anki tag string for a vocab card."""
    tags = [base_tags]
    pos = kw.get("pos", "")
    if pos:
        tags.append(f"ps119-{pos}")
    if pos == "verb":
        stem = _STEM_TAG.get(kw.get("stem", ""), "")
        if stem:
            tags.append(f"ps119-{stem}")
        conj_tag = _CONJ_TAG.get(kw.get("conj", ""), "")
        if conj_tag:
            tags.append(f"ps119-{conj_tag}")
    return " ".join(tags)


def _kw_parse_str(kw: dict[str, Any]) -> str:
    """Return a compact parse descriptor for the preview table."""
    pos = kw.get("pos", "")
    suffix = kw.get("suffix", "")
    sfx = f" + {suffix} sfx" if suffix else ""
    if pos == "verb":
        stem = kw.get("stem", "")
        conj = kw.get("conj", "")
        pgn = kw.get("pgn", "")
        return " ".join(x for x in [stem, conj, pgn] if x) + sfx
    if pos in ("noun", "adj"):
        g = kw.get("gender", "")
        n = kw.get("number", "")
        s = kw.get("state", "")
        return ".".join(x for x in [g, n, s] if x) + sfx
    return ""


def build_vocab_deck(stanza: dict[str, Any], slug: str) -> dict[str, str]:
    num = stanza["num"]
    name = stanza["name"]
    deck_name = f"Psalm 119::{num:02d} {name} — Vocabulary"
    base_tags = f"ps119-vocab ps119-{slug}"
    # cards: (front, back, tags, kw_dict)
    cards: list[tuple[str, str, str, dict[str, Any]]] = []
    seen: set[str] = set()
    for v in stanza["verses"]:
        for kw in (v.get("key_words") or []):
            if not isinstance(kw, dict):
                continue
            word = kw.get("word", "")
            if word in seen:
                continue
            seen.add(word)
            ref = f"Ps 119:{v['abs_num']}"
            cards.append((f"{word} ({ref})", _kw_back(kw), _kw_tags(kw, base_tags), kw))
    txt = "\n".join([
        "#separator:tab", "#html:false", "#notetype:Basic",
        f"#deck:{deck_name}", "#tags column:3",
        *[f"{f}\t{b}\t{t}" for f, b, t, _ in cards],
    ]) + "\n"
    fd = "\n".join(f"{f}\t{b}\t{deck_name}" for f, b, t, _ in cards) + "\n"
    md_lines = [
        f"# Psalm 119 — {stanza['letter']} {name} — Vocabulary", "",
        f"**Download:** [Anki import (.txt)](ps119-{slug}-vocab-deck.txt) · "
        f"[Flashcard Deluxe (-fd.txt)](ps119-{slug}-vocab-deck-fd.txt)",
        "",
        f"*{len(cards)} key vocabulary words from "
        f"Psalm 119:{stanza['verses'][0]['abs_num']}–{stanza['verses'][-1]['abs_num']}.*",
        f"*Import `ps119-{slug}-vocab-deck.txt` into Anki (File → Import).*",
        "", "---", "", "## Card List", "",
        "| # | Hebrew Form | POS | Parse / Morphology | Lemma | Gloss |",
        "|---|---|---|---|---|---|",
    ]
    for i, (f, _b, _t, kw) in enumerate(cards, 1):
        word = f.split(" (")[0]
        pos = kw.get("pos", "")
        parse = _kw_parse_str(kw)
        lemma = kw.get("lemma", "")
        gloss = kw.get("gloss", "")
        md_lines.append(f"| {i} | {word} | {pos} | {parse} | {lemma} | {gloss} |")
    return {"txt": txt, "fd": fd, "md": "\n".join(md_lines) + "\n"}


def build_verse_deck(stanza: dict[str, Any], slug: str) -> dict[str, str]:
    letter, name = stanza["letter"], stanza["name"]
    deck_name = f"Psalm 119::{stanza['num']:02d} {name} — Verse Recitation"
    tag = f"ps119-verse ps119-{slug}"
    cards: list[tuple[str, str]] = []
    for v in stanza["verses"]:
        ref = f"Ps 119:{v['abs_num']}"
        cards.append((f"{letter} · {ref} · {v['first_word']}", v["hebrew"]))
        cards.append((f"[{ref}] {v['kjv']}", v["hebrew"]))
    txt = "\n".join([
        "#separator:tab", "#html:false", "#notetype:Basic",
        f"#deck:{deck_name}", "#tags column:3",
        *[f"{f}\t{b}\t{tag}" for f, b in cards],
    ]) + "\n"
    fd = "\n".join(f"{f}\t{b}\t{deck_name}" for f, b in cards) + "\n"
    md_lines = [
        f"# {deck_name}", "",
        f"**Download:** [Anki import (.txt)](ps119-{slug}-verse-deck.txt) · "
        f"[Flashcard Deluxe (-fd.txt)](ps119-{slug}-verse-deck-fd.txt)",
        "",
        f"*{len(cards)} cards ({len(stanza['verses'])} verses × 2 card types).*",
        f"*Import `ps119-{slug}-verse-deck.txt` into Anki (File → Import).*",
        "", "**Type A** — First-word prompt → full Hebrew verse",
        "", "**Type B** — English gloss → full Hebrew verse",
        "", "---", "", "## Card List", "", "| # | Type | Front | Back |", "|---|---|---|---|",
        *[f"| {i} | {'A' if i % 2 == 1 else 'B'} | {f} | {b} |" for i, (f, b) in enumerate(cards, 1)],
    ]
    return {"txt": txt, "fd": fd, "md": "\n".join(md_lines) + "\n"}


# ---------------------------------------------------------------------------
# Section index
# ---------------------------------------------------------------------------

def build_section_index(stanza: dict[str, Any], slug: str) -> str:
    letter, name = stanza["letter"], stanza["name"]
    v_start, v_end = stanza["verses"][0]["abs_num"], stanza["verses"][-1]["abs_num"]
    lines = [
        f"# Psalm 119 — {letter} {name} Section (vv. {v_start}–{v_end})",
        "", f"The **{letter} ({name})** stanza comprises verses {v_start}–{v_end}; "
        f"each verse begins with **{letter}**.", "",
        "---", "", "## Verses at a Glance", "", "| # | Hebrew | KJV |", "|---|---|---|",
        *[f"| {v['abs_num']} | {v['hebrew']} | {v['kjv'].replace('|', chr(92)+'|')} |"
          for v in stanza["verses"]],
        "", "---", "", "## Exercises", "",
        "| Exercise | Description | Formats |", "|---|---|---|",
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
        "", "---", "", "## Anki Flashcard Decks", "",
        "| Deck | Download |", "|---|---|",
        f"| Vocabulary | [Anki (.txt)](anki/ps119-{slug}-vocab-deck.txt) · "
        f"[Flashcard Deluxe (-fd.txt)](anki/ps119-{slug}-vocab-deck-fd.txt) · "
        f"[Preview](anki/ps119-{slug}-vocab-deck.md) |",
        f"| Verse Recitation | [Anki (.txt)](anki/ps119-{slug}-verse-deck.txt) · "
        f"[Flashcard Deluxe (-fd.txt)](anki/ps119-{slug}-verse-deck-fd.txt) · "
        f"[Preview](anki/ps119-{slug}-verse-deck.md) |",
        "", "---", "", "## Reference Card", "",
        f"[Download PDF reference card](ps119-{slug}-reference.pdf) — Hebrew and KJV side-by-side.",
    ]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# PDF generation (local only — requires reportlab + ArialHebrew font)
# ---------------------------------------------------------------------------

def _heb(text: str) -> str:
    if _PDF_AVAILABLE:
        return _bidi_get_display(text)
    return text


def _register_fonts() -> None:
    if not _PDF_AVAILABLE:
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


def _setup_pdf_page(c: Any, title: str, subtitle: str = "") -> float:
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


def _draw_heb(c: Any, text: str, x: float, y: float, font_size: float = 11) -> None:
    try:
        c.setFont("ArialHebrew", font_size)
    except Exception:
        c.setFont("Helvetica", font_size)
    c.drawString(x, y, _heb(text))


def build_reference_card_pdf(stanza: dict[str, Any], out_path: Path) -> None:
    if not _PDF_AVAILABLE:
        return
    _register_fonts()
    letter, name = stanza["letter"], stanza["name"]
    v_start, v_end = stanza["verses"][0]["abs_num"], stanza["verses"][-1]["abs_num"]
    title = f"Psalm 119 — {letter} {name} — Reference Card"
    W, H = LETTER
    c = rl_canvas.Canvas(str(out_path), pagesize=LETTER, invariant=1)
    y = _setup_pdf_page(c, title, f"Verses {v_start}–{v_end}")
    row_h = 0.7 * inch
    col_heb = 0.75 * inch
    col_kjv = W / 2 + 0.1 * inch
    col_heb_w = W / 2 - 1.0 * inch
    col_kjv_w = W / 2 - 0.85 * inch
    c.setFillColor(HexColor("#2a4a6e"))
    c.rect(col_heb - 0.05 * inch, y - 0.25 * inch, col_heb_w, 0.25 * inch,
           fill=1, stroke=0)
    c.rect(col_kjv - 0.05 * inch, y - 0.25 * inch, col_kjv_w, 0.25 * inch,
           fill=1, stroke=0)
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(col_heb, y - 0.18 * inch, "Hebrew")
    c.drawString(col_kjv, y - 0.18 * inch, "KJV")
    y -= 0.3 * inch
    from reportlab.lib.utils import simpleSplit
    for v in stanza["verses"]:
        if y < 1.0 * inch:
            c.showPage()
            y = H - 0.75 * inch
        bg = HexColor("#f0f6ff") if v["num"] % 2 == 0 else HexColor("#ffffff")
        c.setFillColor(bg)
        c.rect(col_heb - 0.05 * inch, y - row_h + 0.05 * inch,
               W - 1.45 * inch, row_h, fill=1, stroke=0)
        c.setFillColor(HexColor("#888888"))
        c.setFont("Helvetica", 8)
        c.drawString(0.4 * inch, y - 0.2 * inch, str(v["abs_num"]))
        c.setFillColor(black)
        _draw_heb(c, v["hebrew"], col_heb, y - 0.22 * inch, 10)
        c.setFont("Helvetica", 8.5)
        c.setFillColor(HexColor("#333333"))
        wrapped = simpleSplit(v["kjv"], "Helvetica", 8.5, col_kjv_w)
        ly = y - 0.18 * inch
        for line in wrapped[:3]:
            c.drawString(col_kjv, ly, line)
            ly -= 0.13 * inch
        c.setStrokeColor(HexColor("#dddddd"))
        c.line(col_heb - 0.05 * inch, y - row_h + 0.05 * inch,
               W - 0.7 * inch, y - row_h + 0.05 * inch)
        y -= row_h
    c.save()


def build_cloze_pdf(stanza: dict[str, Any], level: int, out_path: Path) -> None:
    if not _PDF_AVAILABLE:
        return
    _register_fonts()
    letter, name = stanza["letter"], stanza["name"]
    v_start, v_end = stanza["verses"][0]["abs_num"], stanza["verses"][-1]["abs_num"]
    label = "Key Vocabulary" if level == 1 else "Line Endings"
    title = f"Psalm 119 — {letter} {name} — Cloze Level {level}"
    W, H = LETTER
    c = rl_canvas.Canvas(str(out_path), pagesize=LETTER, invariant=1)
    y = _setup_pdf_page(c, title, f"Ps 119:{v_start}–{v_end} · {label} blanked")
    row_h = 0.9 * inch
    for i, v in enumerate(stanza["verses"]):
        if y < 1.2 * inch:
            c.showPage()
            y = H - 0.75 * inch
        if level == 1:
            pairs = _kw_pairs(v.get("key_words") or [])
        else:
            pairs = _kw_pairs(v.get("line_endings") or [])
        blanked = v["hebrew"]
        for word, _ in pairs:
            blanked = blank_key_word(blanked, word)
        c.setFillColor(HexColor("#444444"))
        c.setFont("Helvetica-Bold", 9)
        c.drawString(0.75 * inch, y - 0.18 * inch, f"119:{v['abs_num']}")
        _draw_heb(c, blanked, 1.5 * inch, y - 0.18 * inch, 10)
        for j in range(len(pairs) or 1):
            c.acroForm.textfield(
                name=f"cloze{level}_v{i}_b{j}",
                x=0.75 * inch + j * 1.8 * inch,
                y=y - 0.55 * inch,
                width=1.6 * inch, height=0.25 * inch,
                fontSize=10, borderStyle="underlined",
            )
        c.setStrokeColor(HexColor("#dddddd"))
        c.line(0.75 * inch, y - row_h + 0.05 * inch,
               W - 0.75 * inch, y - row_h + 0.05 * inch)
        y -= row_h
    c.save()


def build_verse_order_pdf(stanza: dict[str, Any], out_path: Path) -> None:
    if not _PDF_AVAILABLE:
        return
    _register_fonts()
    letter, name = stanza["letter"], stanza["name"]
    v_start, v_end = stanza["verses"][0]["abs_num"], stanza["verses"][-1]["abs_num"]
    W, H = LETTER
    c = rl_canvas.Canvas(str(out_path), pagesize=LETTER, invariant=1)
    y = _setup_pdf_page(c, f"Psalm 119 — {letter} {name} — Verse Ordering",
                        f"Ps 119:{v_start}–{v_end} · Write the correct position (1–8)")
    row_h = 0.8 * inch
    for disp_idx, orig_idx in enumerate(_shuffled_order(stanza)):
        if y < 1.2 * inch:
            c.showPage()
            y = H - 0.75 * inch
        v = stanza["verses"][orig_idx]
        c.setFillColor(HexColor("#444444"))
        c.setFont("Helvetica-Bold", 10)
        c.drawString(0.75 * inch, y - 0.2 * inch, chr(65 + disp_idx))
        _draw_heb(c, v["hebrew"], 1.1 * inch, y - 0.2 * inch, 10)
        c.acroForm.textfield(
            name=f"vo_{disp_idx}",
            x=W - 1.3 * inch, y=y - 0.35 * inch,
            width=0.5 * inch, height=0.25 * inch,
            fontSize=12, borderStyle="underlined",
        )
        c.setStrokeColor(HexColor("#dddddd"))
        c.line(0.75 * inch, y - row_h + 0.05 * inch,
               W - 0.75 * inch, y - row_h + 0.05 * inch)
        y -= row_h
    c.save()


def build_first_word_pdf(stanza: dict[str, Any], out_path: Path) -> None:
    if not _PDF_AVAILABLE:
        return
    _register_fonts()
    letter, name = stanza["letter"], stanza["name"]
    v_start, v_end = stanza["verses"][0]["abs_num"], stanza["verses"][-1]["abs_num"]
    W, H = LETTER
    c = rl_canvas.Canvas(str(out_path), pagesize=LETTER, invariant=1)
    y = _setup_pdf_page(c, f"Psalm 119 — {letter} {name} — First-Word Prompt",
                        f"Ps 119:{v_start}–{v_end} · Write the full verse from memory")
    row_h = 1.0 * inch
    for i, v in enumerate(stanza["verses"]):
        if y < 1.3 * inch:
            c.showPage()
            y = H - 0.75 * inch
        c.setFillColor(HexColor("#444444"))
        c.setFont("Helvetica-Bold", 9)
        c.drawString(0.75 * inch, y - 0.18 * inch, f"119:{v['abs_num']}")
        _draw_heb(c, v["first_word"], 1.5 * inch, y - 0.18 * inch, 11)
        c.acroForm.textfield(
            name=f"fw_{i}",
            x=0.75 * inch, y=y - 0.65 * inch,
            width=W - 1.5 * inch, height=0.35 * inch,
            fontSize=10, borderStyle="underlined",
        )
        c.setStrokeColor(HexColor("#dddddd"))
        c.line(0.75 * inch, y - row_h + 0.05 * inch,
               W - 0.75 * inch, y - row_h + 0.05 * inch)
        y -= row_h
    c.save()


# ---------------------------------------------------------------------------
# Per-section builder
# ---------------------------------------------------------------------------

def build_section(stanza: dict[str, Any], mkdocs_out: Path, data_out: Path) -> None:
    slug = make_slug(stanza)
    out = mkdocs_out / slug
    out.mkdir(parents=True, exist_ok=True)
    data_slug = data_out / slug
    data_slug.mkdir(parents=True, exist_ok=True)

    (out / "index.md").write_text(build_section_index(stanza, slug), encoding="utf-8")

    anki_dir = out / "anki"
    anki_dir.mkdir(exist_ok=True)
    vocab = build_vocab_deck(stanza, slug)
    (anki_dir / f"ps119-{slug}-vocab-deck.txt").write_text(vocab["txt"], encoding="utf-8")
    (anki_dir / f"ps119-{slug}-vocab-deck-fd.txt").write_text(vocab["fd"], encoding="utf-8")
    (anki_dir / f"ps119-{slug}-vocab-deck.md").write_text(vocab["md"], encoding="utf-8")
    verse = build_verse_deck(stanza, slug)
    (anki_dir / f"ps119-{slug}-verse-deck.txt").write_text(verse["txt"], encoding="utf-8")
    (anki_dir / f"ps119-{slug}-verse-deck-fd.txt").write_text(verse["fd"], encoding="utf-8")
    (anki_dir / f"ps119-{slug}-verse-deck.md").write_text(verse["md"], encoding="utf-8")

    ex_dir = out / "exercises"
    ex_dir.mkdir(exist_ok=True)

    cl1_dir = ex_dir / "cloze-l1"
    cl1_dir.mkdir(exist_ok=True)
    (cl1_dir / "cloze-l1.html").write_text(build_cloze_l1_html(stanza), encoding="utf-8")
    (cl1_dir / "cloze-l1.md").write_text(build_cloze_l1_md(stanza), encoding="utf-8")
    _copy_or_build_pdf(data_slug / "exercises" / "cloze-l1" / "cloze-l1.pdf",
                       cl1_dir / "cloze-l1.pdf",
                       lambda p: build_cloze_pdf(stanza, 1, p))

    cl2_dir = ex_dir / "cloze-l2"
    cl2_dir.mkdir(exist_ok=True)
    (cl2_dir / "cloze-l2.html").write_text(build_cloze_l2_html(stanza), encoding="utf-8")
    (cl2_dir / "cloze-l2.md").write_text(build_cloze_l2_md(stanza), encoding="utf-8")
    _copy_or_build_pdf(data_slug / "exercises" / "cloze-l2" / "cloze-l2.pdf",
                       cl2_dir / "cloze-l2.pdf",
                       lambda p: build_cloze_pdf(stanza, 2, p))

    vo_dir = ex_dir / "verse-order"
    vo_dir.mkdir(exist_ok=True)
    (vo_dir / "verse-order.html").write_text(build_verse_order_html(stanza), encoding="utf-8")
    (vo_dir / "verse-order.md").write_text(build_verse_order_md(stanza), encoding="utf-8")
    _copy_or_build_pdf(data_slug / "exercises" / "verse-order" / "verse-order.pdf",
                       vo_dir / "verse-order.pdf",
                       lambda p: build_verse_order_pdf(stanza, p))

    fw_dir = ex_dir / "first-word"
    fw_dir.mkdir(exist_ok=True)
    (fw_dir / "first-word.html").write_text(build_first_word_html(stanza), encoding="utf-8")
    (fw_dir / "first-word.md").write_text(build_first_word_md(stanza), encoding="utf-8")
    _copy_or_build_pdf(data_slug / "exercises" / "first-word" / "first-word.pdf",
                       fw_dir / "first-word.pdf",
                       lambda p: build_first_word_pdf(stanza, p))

    _copy_or_build_pdf(data_slug / f"ps119-{slug}-reference.pdf",
                       out / f"ps119-{slug}-reference.pdf",
                       lambda p: build_reference_card_pdf(stanza, p))


def _copy_or_build_pdf(data_src: Path, mkdocs_dst: Path, builder: Any) -> None:
    """Copy pre-built PDF from data/ to mkdocs_src/, or build it if available."""
    if _PDF_AVAILABLE:
        data_src.parent.mkdir(parents=True, exist_ok=True)
        builder(data_src)
        shutil.copy2(data_src, mkdocs_dst)
    elif data_src.exists():
        shutil.copy2(data_src, mkdocs_dst)
    # else: PDF simply absent in CI with no pre-built copy yet — not an error


# ---------------------------------------------------------------------------
# Master flashcards index
# ---------------------------------------------------------------------------

def build_flashcards_index(stanzas: list[dict[str, Any]]) -> str:
    lines = [
        "# Psalm 119 — Flashcard Decks",
        "",
        "Download flashcard decks for all 22 stanzas. Each stanza has a **Vocabulary** deck "
        "(key Hebrew words with glosses) and a **Verse Recitation** deck "
        "(first-word and KJV prompts).",
        "",
        "Import `.txt` files into [Anki](https://apps.ankiweb.net) (File → Import). "
        "Use `-fd.txt` files with Flashcard Deluxe.",
        "",
        "---", "",
        "| Stanza | Vocabulary Deck | Verse Recitation Deck |",
        "|---|---|---|",
    ]
    for stanza in stanzas:
        slug = make_slug(stanza)
        letter, name = stanza["letter"], stanza["name"]
        v_start = stanza["verses"][0]["abs_num"]
        v_end = stanza["verses"][-1]["abs_num"]
        base = f"../memorization/{slug}/anki/ps119-{slug}"
        lines.append(
            f"| [{letter} {name} (vv. {v_start}–{v_end})](../memorization/{slug}/) |"
            f" [Anki (.txt)]({base}-vocab-deck.txt)"
            f" \xb7 [Flashcard Deluxe (-fd.txt)]({base}-vocab-deck-fd.txt)"
            f" \xb7 [Preview]({base}-vocab-deck.md) |"
            f" [Anki (.txt)]({base}-verse-deck.txt)"
            f" \xb7 [Flashcard Deluxe (-fd.txt)]({base}-verse-deck-fd.txt)"
            f" \xb7 [Preview]({base}-verse-deck.md) |"
        )
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    stanzas = load_stanzas()
    pdf_note = " (+ PDFs)" if _PDF_AVAILABLE else " (HTML/MD only — PDFs copied from data/)"
    print(f"build_psalm119_memorization: building {len(stanzas)} sections{pdf_note}...")
    MKDOCS_OUT.mkdir(parents=True, exist_ok=True)
    DATA_MEM.mkdir(parents=True, exist_ok=True)
    for stanza in stanzas:
        slug = make_slug(stanza)
        print(f"  {slug}...", end=" ", flush=True)
        build_section(stanza, MKDOCS_OUT, DATA_MEM)
        print("done")
    fc_dir = MKDOCS_OUT.parent / "flashcards"
    fc_dir.mkdir(parents=True, exist_ok=True)
    (fc_dir / "index.md").write_text(build_flashcards_index(stanzas), encoding="utf-8")
    print(f"build_psalm119_memorization: complete → {MKDOCS_OUT}")
    print(f"build_psalm119_memorization: flashcards index → {fc_dir / 'index.md'}")


if __name__ == "__main__":
    main()
