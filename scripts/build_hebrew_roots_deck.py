#!/usr/bin/env python3
"""Build Hebrew root flashcard deck.

Parses OpenScriptures HebrewStrong.xml to group Strong's codes by their
root entry, cross-references with words.parquet for OT frequencies and
attested verbal stems, then emits:

  data/lessons/bbh/additional-resources/hebrew-root-deck/
    hebrew-root-deck.txt         Anki (Hebrew Root notetype, 3 fields)
    hebrew-root-deck-fd-all.txt  Flashcards Deluxe, all 1000 roots
    hebrew-root-deck-fd-100.txt  Flashcards Deluxe, freq >= 100
    hebrew-root-deck-fd-50.txt   Flashcards Deluxe, freq 50-99
    hebrew-root-deck-fd-10.txt   Flashcards Deluxe, freq 10-49
    hebrew-root-deck.md          Summary report
    README.md
"""

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import xml.etree.ElementTree as ET
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
XML_PATH = ROOT_DIR / "openscriptures-lexicon" / "HebrewStrong.xml"
PARQUET_PATH = ROOT_DIR / "data" / "processed" / "words.parquet"
OUT_DIR = ROOT_DIR / "data" / "lessons" / "bbh" / "additional-resources" / "hebrew-root-deck"
NS = "http://openscriptures.github.com/morphhb/namespace"

STEM_ORDER = ["Qal", "Niphal", "Hiphil", "Hophal", "Piel", "Pual", "Hithpael"]
FREQ_BANDS = [
    ("100plus", 100, 999999),
    ("50to99", 50, 99),
    ("10to49", 10, 49),
    ("1to9", 1, 9),
]
TOP_N = 1000


@dataclass
class Entry:
    entry_id: str          # normalized 4-digit, e.g. "H0006"
    pos: str               # e.g. "v", "n-m", "n-pr-m"
    word_form: str         # with vowel points
    consonants: str        # stripped of vowel points
    gloss: str
    parent_id: Optional[str]   # normalized, or None
    xml_lang: str          # "heb" or "arc"


@dataclass
class RootCard:
    root_id: str
    consonants: str
    word_form: str
    gloss: str
    frequency: int
    verb_stems: List[Tuple[str, int]] = field(default_factory=list)
    nominals: List[Tuple[str, str, int]] = field(default_factory=list)
    has_verb: bool = False
    has_nominal: bool = False
    tags: List[str] = field(default_factory=list)


def nid(raw: str) -> str:
    """Normalize Strong's ID to 4-digit form: 'H6' → 'H0006', 'H0430G' → 'H0430'."""
    m = re.match(r"H(\d+)", raw)
    if not m:
        return raw
    return f"H{int(m.group(1)):04d}"


def strip_vowels(text: str) -> str:
    """Keep only Hebrew consonant codepoints U+05D0–U+05EA (and shin/sin dots U+05C1–U+05C2)."""
    return "".join(c for c in text if "א" <= c <= "ת")


def extract_gloss(entry: ET.Element) -> str:
    """Extract primary gloss from <meaning><def>…</def></meaning> or fallback."""
    meaning = entry.find(f"{{{NS}}}meaning")
    if meaning is not None:
        def_el = meaning.find(f"{{{NS}}}def")
        if def_el is not None and def_el.text:
            return def_el.text.strip()
        full = "".join(meaning.itertext()).strip()
        if full:
            return full[:80]
    usage = entry.find(f"{{{NS}}}usage")
    if usage is not None:
        txt = "".join(usage.itertext()).strip()
        if txt:
            return txt[:80]
    return ""


def parse_xml(xml_path: Path) -> Dict[str, Entry]:
    """Parse HebrewStrong.xml and return normalized_id → Entry."""
    tree = ET.parse(str(xml_path))
    root_el = tree.getroot()
    entries: Dict[str, Entry] = {}

    for e in root_el.findall(f"{{{NS}}}entry"):
        raw_id = e.get("id", "")
        if not raw_id.startswith("H"):
            continue
        norm = nid(raw_id)

        w_el = e.find(f"{{{NS}}}w")
        if w_el is None:
            continue
        pos = w_el.get("pos", "")
        word_form = (w_el.text or "").strip()
        consonants = strip_vowels(word_form)
        xml_lang = w_el.get("xml:lang", "heb")
        gloss = extract_gloss(e)

        # Find first source reference
        parent_id: Optional[str] = None
        src_el = e.find(f"{{{NS}}}source")
        if src_el is not None:
            w_src = src_el.find(f"{{{NS}}}w")
            if w_src is not None:
                ref = w_src.get("src", "")
                if ref:
                    parent_id = nid(ref)

        entries[norm] = Entry(
            entry_id=norm,
            pos=pos,
            word_form=word_form,
            consonants=consonants,
            gloss=gloss,
            parent_id=parent_id,
            xml_lang=xml_lang,
        )

    return entries


def find_ultimate_root(
    entry_id: str,
    entries: Dict[str, Entry],
    cache: Dict[str, str],
    visiting: Optional[set] = None,
) -> str:
    """Walk parent chain to find ultimate root, with cycle detection."""
    if entry_id in cache:
        return cache[entry_id]
    if visiting is None:
        visiting = set()
    if entry_id in visiting:
        cache[entry_id] = entry_id
        return entry_id
    visiting.add(entry_id)
    e = entries.get(entry_id)
    if e is None or e.parent_id is None or e.parent_id == entry_id:
        cache[entry_id] = entry_id
        return entry_id
    # Follow parent
    root = find_ultimate_root(e.parent_id, entries, cache, visiting)
    cache[entry_id] = root
    return root


def build_root_groups(entries: Dict[str, Entry]) -> Dict[str, List[str]]:
    """Return root_id → [all member entry IDs including the root itself]."""
    cache: Dict[str, str] = {}
    groups: Dict[str, List[str]] = {}
    for eid in entries:
        root = find_ultimate_root(eid, entries, cache)
        groups.setdefault(root, []).append(eid)
    return groups


def load_frequencies(parquet_path: Path) -> Tuple[Dict[str, int], Dict[str, Dict[str, int]]]:
    """Load OT Hebrew frequencies from parquet.

    Returns:
        lemma_freq: normalized_id → total count
        stem_freq: normalized_id → {stem_name → count}
    """
    df = pd.read_parquet(str(parquet_path))
    heb = df[df["language"] == "Hebrew"].copy()

    def extract_codes(s: object) -> List[str]:
        if not isinstance(s, str):
            return []
        return [nid(m) for m in re.findall(r"\{(H\d+[A-Z]?)\}", s)]

    # Explode each row's Strong's codes
    heb = heb.copy()
    heb["codes"] = heb["strongs"].apply(extract_codes)
    exploded = heb.explode("codes").dropna(subset=["codes"])

    # Filter out H9xxx grammatical markers
    exploded = exploded[~exploded["codes"].str.startswith("H9")]

    lemma_freq: Dict[str, int] = exploded.groupby("codes").size().to_dict()

    # Stem frequencies (only for verbs)
    verb_rows = exploded[
        (exploded["part_of_speech"] == "Verb") &
        (exploded["stem"].notna()) &
        (exploded["stem"].str.strip() != "")
    ]
    stem_groups = verb_rows.groupby(["codes", "stem"]).size()
    stem_freq: Dict[str, Dict[str, int]] = {}
    for (code, stem_name), count in stem_groups.items():
        stem_freq.setdefault(code, {})[stem_name] = int(count)

    return lemma_freq, stem_freq


def is_proper_name(pos: str) -> bool:
    return pos.startswith("n-pr")


def pos_label(pos: str) -> str:
    """Map XML pos to a readable label."""
    if pos.startswith("v"):
        return "Verb"
    if pos.startswith("n-m"):
        return "Noun (m)"
    if pos.startswith("n-f"):
        return "Noun (f)"
    if pos.startswith("n"):
        return "Noun"
    if pos.startswith("a"):
        return "Adj"
    if pos in ("adv",):
        return "Adv"
    if pos in ("prep",):
        return "Prep"
    if pos in ("conj",):
        return "Conj"
    if pos in ("prt",):
        return "Particle"
    return pos


def build_cards(
    root_groups: Dict[str, List[str]],
    entries: Dict[str, Entry],
    lemma_freq: Dict[str, int],
    stem_freq: Dict[str, Dict[str, int]],
) -> List[RootCard]:
    """Build one RootCard per root, sorted by combined frequency."""
    cards: List[RootCard] = []

    for root_id, member_ids in root_groups.items():
        root_entry = entries.get(root_id)
        if root_entry is None:
            continue

        # Skip proper names as root entries
        if is_proper_name(root_entry.pos):
            continue

        # Skip Aramaic-only roots
        all_heb = [entries[m].xml_lang == "heb" for m in member_ids if m in entries]
        if not any(all_heb):
            continue

        # Compute combined frequency
        total_freq = sum(lemma_freq.get(mid, 0) for mid in member_ids)
        if total_freq == 0:
            continue

        # Collect verb stems across all verb members
        verb_stem_totals: Dict[str, int] = {}
        for mid in member_ids:
            e = entries.get(mid)
            if e is None:
                continue
            if e.pos.startswith("v") and mid in stem_freq:
                for sname, cnt in stem_freq[mid].items():
                    verb_stem_totals[sname] = verb_stem_totals.get(sname, 0) + cnt

        # Order stems by STEM_ORDER then alphabetical
        ordered_stems: List[Tuple[str, int]] = []
        for sname in STEM_ORDER:
            if sname in verb_stem_totals:
                ordered_stems.append((sname, verb_stem_totals[sname]))
        for sname, cnt in sorted(verb_stem_totals.items()):
            if sname not in STEM_ORDER:
                ordered_stems.append((sname, cnt))

        # Collect nominals (non-verb, non-proper-name, Hebrew, with gloss)
        nominals: List[Tuple[str, str, int]] = []
        for mid in member_ids:
            e = entries.get(mid)
            if e is None or mid == root_id:
                continue
            if e.pos.startswith("v") or is_proper_name(e.pos):
                continue
            if e.xml_lang != "heb":
                continue
            freq = lemma_freq.get(mid, 0)
            if freq == 0:
                continue
            gloss = e.gloss or root_entry.gloss
            nominals.append((e.word_form, gloss, freq))

        nominals.sort(key=lambda x: -x[2])
        nominals = nominals[:8]  # cap at 8 per card for readability

        # Build tags
        tags: List[str] = ["Hebrew:Root"]
        if ordered_stems:
            tags.append("Hebrew:POS:Verb")
            for sname, _ in ordered_stems:
                tags.append(f"Hebrew:Stem:{sname}")
        if nominals:
            tags.append("Hebrew:POS:Nominal")
        # Frequency band tag
        if total_freq >= 100:
            tags.append("Hebrew:Freq:100plus")
        elif total_freq >= 50:
            tags.append("Hebrew:Freq:50to99")
        elif total_freq >= 10:
            tags.append("Hebrew:Freq:10to49")
        else:
            tags.append("Hebrew:Freq:1to9")

        cards.append(RootCard(
            root_id=root_id,
            consonants=root_entry.consonants,
            word_form=root_entry.word_form,
            gloss=root_entry.gloss,
            frequency=total_freq,
            verb_stems=ordered_stems,
            nominals=nominals,
            has_verb=bool(ordered_stems),
            has_nominal=bool(nominals),
            tags=tags,
        ))

    cards.sort(key=lambda c: -c.frequency)
    return cards[:TOP_N]


def render_anki_back(card: RootCard) -> str:
    """Render HTML for the Anki card back field."""
    parts: List[str] = []
    # Root form with vowels
    parts.append(
        f'<div style="font-size:1.5em;direction:rtl;margin-bottom:4px">'
        f'{card.word_form}</div>'
    )
    # Gloss
    if card.gloss:
        parts.append(f'<div style="font-style:italic;margin-bottom:8px">{card.gloss}</div>')

    # Verb stems table
    if card.verb_stems:
        rows = "".join(
            f"<tr><td>{s}</td><td style='text-align:right'>{c}</td></tr>"
            for s, c in card.verb_stems
        )
        parts.append(
            '<table style="border-collapse:collapse;margin-bottom:8px">'
            '<tr><th style="padding:2px 8px">Stem</th>'
            '<th style="padding:2px 8px;text-align:right">N</th></tr>'
            f"{rows}</table>"
        )

    # Nominals table
    if card.nominals:
        rows = "".join(
            f'<tr><td style="direction:rtl;padding:2px 8px">{wf}</td>'
            f'<td style="padding:2px 8px;font-style:italic">{gl}</td>'
            f'<td style="text-align:right;padding:2px 8px">{fr}</td></tr>'
            for wf, gl, fr in card.nominals
        )
        parts.append(
            '<table style="border-collapse:collapse">'
            '<tr><th style="padding:2px 8px">Form</th>'
            '<th style="padding:2px 8px">Gloss</th>'
            '<th style="padding:2px 8px;text-align:right">N</th></tr>'
            f"{rows}</table>"
        )

    return "".join(parts)


def render_fd_back(card: RootCard) -> str:
    """Render plain-text back for Flashcards Deluxe."""
    parts: List[str] = []
    if card.gloss:
        parts.append(card.gloss)
    if card.verb_stems:
        stem_str = ", ".join(f"{s} ({c})" for s, c in card.verb_stems)
        parts.append(f"Stems: {stem_str}")
    if card.nominals:
        nom_str = "; ".join(f"{wf} {gl}" for wf, gl, _ in card.nominals[:4])
        parts.append(f"Nouns: {nom_str}")
    return " | ".join(parts)


def write_anki(cards: List[RootCard], out_path: Path) -> None:
    """Write Anki import file (tab-separated, Hebrew Root notetype)."""
    lines = [
        "#separator:tab",
        "#html:true",
        "#notetype:Hebrew Root",
        "#deck:Biblical Hebrew::Root Deck",
        "#columns:Front\tBack\tFrequency\tTags",
        "#tags column:4",
    ]
    for card in cards:
        front = card.consonants
        back = render_anki_back(card)
        freq = str(card.frequency)
        tags = " ".join(card.tags)
        lines.append(f"{front}\t{back}\t{freq}\t{tags}")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Wrote {len(cards)} cards → {out_path.name}")


def write_fd(cards: List[RootCard], out_path: Path, min_freq: int, max_freq: int) -> None:
    """Write Flashcards Deluxe import file."""
    band_cards = [c for c in cards if min_freq <= c.frequency <= max_freq]
    lines = [
        "Text 1\tText 2\tCategory",
    ]
    for card in band_cards:
        front = card.consonants
        back = render_fd_back(card)
        # Determine category from primary tag
        if card.frequency >= 100:
            cat = "Freq100plus"
        elif card.frequency >= 50:
            cat = "Freq50to99"
        elif card.frequency >= 10:
            cat = "Freq10to49"
        else:
            cat = "Freq1to9"
        lines.append(f"{front}\t{back}\t{cat}")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Wrote {len(band_cards)} cards → {out_path.name}")


def write_summary_md(cards: List[RootCard], out_path: Path) -> None:
    """Write summary markdown report."""
    total = len(cards)
    has_verb = sum(1 for c in cards if c.has_verb)
    has_nominal = sum(1 for c in cards if c.has_nominal)
    freq_100 = sum(1 for c in cards if c.frequency >= 100)
    freq_50 = sum(1 for c in cards if 50 <= c.frequency < 100)
    freq_10 = sum(1 for c in cards if 10 <= c.frequency < 50)
    freq_low = sum(1 for c in cards if c.frequency < 10)
    min_freq = min(c.frequency for c in cards) if cards else 0
    max_freq = max(c.frequency for c in cards) if cards else 0

    rows = "".join(
        f"| {i+1} | {c.consonants} | {c.word_form} | {c.gloss[:50]} | {c.frequency} |"
        f" {', '.join(s for s, _ in c.verb_stems) or '—'} |\n"
        for i, c in enumerate(cards[:50])
    )

    content = f"""# Hebrew Root Flashcard Deck

## Summary

| Metric | Value |
|---|---|
| Total roots | {total} |
| Roots with verbal stems | {has_verb} |
| Roots with derived nominals | {has_nominal} |
| Freq ≥ 100 | {freq_100} |
| Freq 50–99 | {freq_50} |
| Freq 10–49 | {freq_10} |
| Freq 1–9 | {freq_low} |
| Frequency range | {min_freq}–{max_freq} |

## Files

| File | Description |
|---|---|
| `hebrew-root-deck.txt` | Anki import (Hebrew Root notetype, 3 fields) |
| `hebrew-root-deck-fd-all.txt` | Flashcards Deluxe — all {total} roots |
| `hebrew-root-deck-fd-100.txt` | Flashcards Deluxe — freq ≥ 100 ({freq_100} roots) |
| `hebrew-root-deck-fd-50.txt` | Flashcards Deluxe — freq 50–99 ({freq_50} roots) |
| `hebrew-root-deck-fd-10.txt` | Flashcards Deluxe — freq 10–49 ({freq_10} roots) |

## Top 50 Roots

| # | Root | Form | Gloss | Freq | Stems |
|---|---|---|---|---|---|
{rows}
"""
    out_path.write_text(content, encoding="utf-8")
    print(f"  Wrote summary → {out_path.name}")


def write_readme(cards: List[RootCard], out_path: Path) -> None:
    """Write README.md for the deck directory."""
    total = len(cards)
    content = f"""# Hebrew Root Deck

← [Back to Additional Resources](../index.md)

A flashcard deck for the top {total} Hebrew roots by OT frequency.
Each card front shows the consonantal root; the back shows the gloss, attested verbal stems, and derived nominals.

## Card Design

- **Front:** Consonantal root (e.g., אבד)
- **Back:** Vowel-pointed form, gloss, verbal stem frequencies, derived nominals
- **Frequency field:** Combined OT occurrence count (sum of all lemmata in the root family)

## Files

| File | Purpose |
|---|---|
| `hebrew-root-deck.txt` | Anki import — requires **Hebrew Root** notetype (3 fields: Front, Back, Frequency) |
| `hebrew-root-deck-fd-all.txt` | Flashcards Deluxe — all {total} roots |
| `hebrew-root-deck-fd-100.txt` | Flashcards Deluxe — freq ≥ 100 |
| `hebrew-root-deck-fd-50.txt` | Flashcards Deluxe — freq 50–99 |
| `hebrew-root-deck-fd-10.txt` | Flashcards Deluxe — freq 10–49 |
| `hebrew-root-deck.md` | Summary report with top-50 table |

## Anki Setup

Before importing `hebrew-root-deck.txt`, create a note type named **Hebrew Root** with three fields in order:
1. **Front** — the question (consonantal root)
2. **Back** — the answer (HTML)
3. **Frequency** — numeric OT frequency (used for filtered decks, e.g., `Frequency:>100`)

## Filtering in Flashcards Deluxe

Use the band files to study by frequency tier:
- `fd-100.txt` — most common roots (≥ 100 occurrences)
- `fd-50.txt` — moderately common (50–99)
- `fd-10.txt` — less common (10–49)
- `fd-all.txt` — complete deck

## Data Sources

- **Root groupings:** OpenScriptures HebrewLexicon (HebrewStrong.xml)
- **Frequencies:** OSHB morphologically-tagged OT (words.parquet)
- **Top {total} roots** ranked by combined root-family frequency
"""
    out_path.write_text(content, encoding="utf-8")
    print(f"  Wrote README → {out_path.name}")


def main() -> None:
    print("Parsing HebrewStrong.xml…")
    entries = parse_xml(XML_PATH)
    print(f"  Loaded {len(entries)} entries")

    print("Building root groups…")
    root_groups = build_root_groups(entries)
    print(f"  Found {len(root_groups)} root groups")

    print("Loading OT frequencies from parquet…")
    lemma_freq, stem_freq = load_frequencies(PARQUET_PATH)
    print(f"  Loaded frequencies for {len(lemma_freq)} codes")

    print(f"Building top-{TOP_N} root cards…")
    cards = build_cards(root_groups, entries, lemma_freq, stem_freq)
    print(f"  Built {len(cards)} cards (freq range {cards[-1].frequency}–{cards[0].frequency})")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Writing output files…")

    write_anki(cards, OUT_DIR / "hebrew-root-deck.txt")
    write_fd(cards, OUT_DIR / "hebrew-root-deck-fd-all.txt", 1, 999999)
    write_fd(cards, OUT_DIR / "hebrew-root-deck-fd-100.txt", 100, 999999)
    write_fd(cards, OUT_DIR / "hebrew-root-deck-fd-50.txt", 50, 99)
    write_fd(cards, OUT_DIR / "hebrew-root-deck-fd-10.txt", 10, 49)
    write_summary_md(cards, OUT_DIR / "hebrew-root-deck.md")
    write_readme(cards, OUT_DIR / "README.md")

    print("Done.")


if __name__ == "__main__":
    main()
    sys.exit(0)
