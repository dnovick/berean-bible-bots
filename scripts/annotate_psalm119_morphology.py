#!/usr/bin/env python3
"""Annotate Psalm 119 key_words with morphological data from words.parquet.

Run once (locally) whenever new key_words are added to psalm-119-text.yaml.
Requires data/processed/words.parquet (gitignored; not available in CI).

Output: updates psalm-119-text.yaml in-place, adding pos/lemma/stem/conj/pgn
fields to every key_word entry that can be matched.

Usage:
    python scripts/annotate_psalm119_morphology.py [--force]

Use --force to re-annotate entries that already have a 'pos' field.
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

import yaml

REPO = Path(__file__).resolve().parent.parent
YAML_PATH = REPO / "data" / "studies" / "psalm-119" / "psalm-119-text.yaml"
PARQUET_PATH = REPO / "data" / "processed" / "words.parquet"

FORCE = "--force" in sys.argv

# ---------------------------------------------------------------------------
# Word normalization
# ---------------------------------------------------------------------------


def _clean(word: str) -> str:
    """Strip cantillation marks and separators; keep vowel points and dagesh.

    Strips:  U+0591–U+05AF (tropes), U+05BD (meteg), U+05BE (maqqef),
             U+05C0 (paseq), U+05C3 (sof pasuq), U+05C6 (nun hafukha),
             literal backslash (TAHOT encoding artifact), slash prefix separator.
    Keeps:   U+05B0–U+05BC (shewa, vowel points, dagesh),
             U+05BF (rafe), U+05C1–U+05C2 (shin/sin dots).
    """
    buf: list[str] = []
    i = 0
    while i < len(word):
        ch = word[i]
        cp = ord(ch)
        if 0x0591 <= cp <= 0x05AF:   # cantillation marks
            i += 1
            continue
        if cp in (0x05BD, 0x05BE, 0x05C0, 0x05C3, 0x05C6):
            i += 1
            continue
        if ch == '\\':               # TAHOT backslash-marker: skip it and next char
            i += 2
            continue
        if ch == '/':                # prefix separator: join, don't emit
            i += 1
            continue
        buf.append(ch)
        i += 1
    return unicodedata.normalize('NFC', ''.join(buf))


# ---------------------------------------------------------------------------
# Morph-code parsing (TAHOT format)
# ---------------------------------------------------------------------------

# Primary word-type priority: verb beats noun beats adj beats pronoun beats particle/prep
_POS_PRIORITY = {'V': (0, 'verb'), 'N': (1, 'noun'), 'A': (2, 'adj'),
                 'P': (3, 'pronoun'), 'T': (4, 'particle'), 'R': (4, 'particle')}

_STEM = {
    'q': 'Qal', 'N': 'Niphal', 'p': 'Piel', 'u': 'Pual',
    'h': 'Hiphil', 'o': 'Hophal', 't': 'Hithpael',
    'D': 'Polel', 'E': 'Polal', 'F': 'Hithpolel', 'Q': 'Qal-pass',
}

_CONJ = {
    'p': 'Perf', 'i': 'Impf', 'v': 'Wqtl', 'j': 'Juss',
    'm': 'Impv', 'c': 'InfCstr', 'a': 'InfAbs',
    'r': 'Ptc.act', 's': 'Ptc.pass',
}

# Short codes for verb PGN: person+gender+number → e.g. '3ms', '2mp', '1cs'
_PER_V = {'1': '1', '2': '2', '3': '3', 'c': 'c'}
_GEN_V = {'m': 'm', 'f': 'f', 'b': 'c', 'c': 'c'}
_NUM_V = {'s': 's', 'p': 'p', 'd': 'd'}

# Descriptor codes for participle/noun/adj gender·number·state
_GEN_N = {'m': 'm', 'f': 'f', 'b': 'c', 'c': 'c'}
_NUM_N = {'s': 'sg', 'p': 'pl', 'd': 'du'}
_STATE_N = {'a': 'abs', 'c': 'cstr', 'd': 'det'}


def _parse_verb(seg: str) -> dict[str, str]:
    """Parse TAHOT verb code (after the 'V' byte)."""
    result: dict[str, str] = {}
    if not seg:
        return result
    result['stem'] = _STEM.get(seg[0], seg[0])
    cj = seg[1] if len(seg) > 1 else ''
    result['conj'] = _CONJ.get(cj, cj)
    tail = seg[2:]
    if cj in ('r', 's'):
        # Participle: tail = gender + number + state
        g = _GEN_N.get(tail[0], tail[0]) if len(tail) > 0 else ''
        n = _NUM_N.get(tail[1], tail[1]) if len(tail) > 1 else ''
        s = _STATE_N.get(tail[2], tail[2]) if len(tail) > 2 else ''
        result['pgn'] = '.'.join(x for x in [g, n, s] if x)
    elif cj in ('c', 'a'):
        result['pgn'] = ''
    else:
        per = _PER_V.get(tail[0], tail[0]) if len(tail) > 0 else ''
        gen = _GEN_V.get(tail[1], tail[1]) if len(tail) > 1 else ''
        num = _NUM_V.get(tail[2], tail[2]) if len(tail) > 2 else ''
        result['pgn'] = f"{per}{gen}{num}"
    return result


def _parse_noun(seg: str) -> dict[str, str]:
    """Parse TAHOT noun code (after the 'N' byte)."""
    result: dict[str, str] = {}
    # seg = type-byte(c/p) + gender + number + state
    tail = seg[1:] if seg and seg[0] in ('c', 'p') else seg
    if len(tail) > 0:
        result['gender'] = _GEN_N.get(tail[0], tail[0])
    if len(tail) > 1:
        result['number'] = _NUM_N.get(tail[1], tail[1])
    if len(tail) > 2:
        result['state'] = _STATE_N.get(tail[2], tail[2])
    return result


def _parse_adj(seg: str) -> dict[str, str]:
    """Parse TAHOT adjective code (after the 'A' byte). Same layout as noun."""
    result: dict[str, str] = {}
    tail = seg[1:] if seg and seg[0].islower() else seg
    if len(tail) > 0:
        result['gender'] = _GEN_N.get(tail[0], tail[0])
    if len(tail) > 1:
        result['number'] = _NUM_N.get(tail[1], tail[1])
    if len(tail) > 2:
        result['state'] = _STATE_N.get(tail[2], tail[2])
    return result


def _parse_suffix(seg: str) -> str:
    """Parse suffix segment 'Sp3ms' → '3ms'."""
    # seg starts with 'S' then type-char ('p'=pronominal) then person+gender+number
    tail = seg[2:] if len(seg) >= 2 else ''
    per = _PER_V.get(tail[0], '') if len(tail) > 0 else ''
    gen = _GEN_V.get(tail[1], '') if len(tail) > 1 else ''
    num = _NUM_V.get(tail[2], '') if len(tail) > 2 else ''
    return f"{per}{gen}{num}"


def _morph_from_code(morph_code: str) -> dict[str, Any]:
    """Derive morphological info by parsing a TAHOT morph_code string.

    Prefers the highest-priority word type when multiple segments are present
    (e.g., HTd/Vqrmpa → verb wins over particle prefix).
    """
    if not morph_code:
        return {}

    segs = morph_code.split('/')
    best_priority = 99
    primary: tuple[str, str] | None = None  # (pos_label, code_after_type_byte)
    suffix_seg: str | None = None

    for seg in segs:
        code = seg[1:] if seg.startswith('H') else seg
        if not code:
            continue
        first = code[0]
        if first == 'S':
            suffix_seg = code
            continue
        if first in _POS_PRIORITY:
            pri, label = _POS_PRIORITY[first]
            if pri < best_priority:
                best_priority = pri
                primary = (label, code[1:])

    if primary is None:
        return {}

    pos, rest = primary
    result: dict[str, Any] = {'pos': pos}

    if pos == 'verb':
        v = _parse_verb(rest)
        result.update(v)
    elif pos == 'noun':
        n = _parse_noun(rest)
        result.update(n)
    elif pos == 'adj':
        a = _parse_adj(rest)
        result.update(a)

    if suffix_seg:
        result['suffix'] = _parse_suffix(suffix_seg)

    return result


# ---------------------------------------------------------------------------
# Lemma lookup from Strong's numbers
# ---------------------------------------------------------------------------

def _extract_strongs(raw: str) -> str:
    """Extract the primary Strong's number (in curly braces) from a strongs field."""
    m = re.search(r'\{(H\d+[A-Z]?)\}', raw or '')
    return m.group(1) if m else ''


def build_lemma_map(df: Any) -> dict[str, str]:
    """Build Strong's number → canonical Hebrew lemma (pointed form).

    Filters to rows where the word has NO lexical prefix (article/prep)
    and NO pronominal suffix, then picks the most frequent absolute-state form.
    """
    heb = df[df['language'] == 'Hebrew'].copy()
    # Extract primary strongs key and clean word
    heb['strongs_key'] = heb['strongs'].apply(_extract_strongs)
    heb['word_clean'] = heb['word'].apply(_clean)

    # Keep only rows where morph_code starts directly with the primary word type
    # (no lexical prefix segment before the '/'). This excludes בְּ/תוֹרַת style rows.
    # A morph_code with a prefix segment looks like 'HR/...' or 'HTd/...' — it
    # contains '/' and starts with H[TR] or similar non-primary types.
    has_lex_prefix = heb['morph_code'].str.match(r'^H[TRd]', na=False)
    has_pron_suffix = heb['morph_code'].str.contains(r'/S', na=False)

    clean_heb = heb[~has_lex_prefix & ~has_pron_suffix]

    lemma_map: dict[str, str] = {}

    for key, grp in clean_heb.groupby('strongs_key'):
        if not key:
            continue
        pos_counts = grp['part_of_speech'].value_counts()
        primary_pos = pos_counts.index[0] if len(pos_counts) else ''

        candidate = ''
        if primary_pos == 'Verb':
            # Prefer Qal Perfect 3ms → otherwise any Perfect 3ms → InfCstr
            for filt in [
                (grp['stem'] == 'Qal') & (grp['conjugation'] == 'Perfect') &
                (grp['person'] == '3rd') & (grp['gender'] == 'Masculine') &
                (grp['number'] == 'Singular'),
                (grp['conjugation'] == 'Perfect') & (grp['person'] == '3rd') &
                (grp['gender'] == 'Masculine') & (grp['number'] == 'Singular'),
                (grp['conjugation'] == 'Infinitive construct'),
            ]:
                subset = grp[filt]
                if not subset.empty:
                    wc = subset['word_clean'].value_counts()
                    candidate = wc.index[0]
                    break

        elif primary_pos in ('Noun', 'Adjective'):
            # Prefer absolute singular; fallback to most common
            for filt in [
                (grp['state'] == 'Absolute') & (grp['number'] == 'Singular'),
                (grp['state'] == 'Absolute'),
                grp['word_clean'].notna(),
            ]:
                subset = grp[filt]
                if not subset.empty:
                    wc = subset['word_clean'].value_counts()
                    candidate = wc.index[0]
                    break

        else:
            wc = grp['word_clean'].value_counts()
            candidate = wc.index[0] if len(wc) else ''

        if candidate:
            lemma_map[key] = candidate

    return lemma_map


# ---------------------------------------------------------------------------
# Main annotation logic
# ---------------------------------------------------------------------------

def _annotate_kw(kw: dict[str, Any], verse_tokens: list[tuple[str, str, str]]) -> bool:
    """Annotate a single key_word dict in-place. Returns True if annotated."""
    word = unicodedata.normalize('NFC', kw.get('word', ''))
    match = next(
        ((mc, st) for cw, mc, st in verse_tokens
         if unicodedata.normalize('NFC', cw) == word),
        None
    )
    if not match:
        return False
    mc, strongs_raw = match
    morph = _morph_from_code(mc)
    if not morph:
        return False

    pos = morph.get('pos', '')
    kw['pos'] = pos
    if pos == 'verb':
        kw['stem'] = morph.get('stem', '')
        kw['conj'] = morph.get('conj', '')
        pgn = morph.get('pgn', '')
        if pgn:
            kw['pgn'] = pgn
        sfx = morph.get('suffix', '')
        if sfx:
            kw['suffix'] = sfx
    elif pos in ('noun', 'adj'):
        for field in ('gender', 'number', 'state'):
            val = morph.get(field, '')
            if val:
                kw[field] = val
        sfx = morph.get('suffix', '')
        if sfx:
            kw['suffix'] = sfx

    return True  # lemma assigned later by caller


def annotate() -> None:
    try:
        import pandas as pd
    except ImportError:
        print("ERROR: pandas not available. Run locally where words.parquet is accessible.")
        return

    if not PARQUET_PATH.exists():
        print(f"ERROR: {PARQUET_PATH} not found.")
        return

    import pandas as pd  # noqa: F811 — re-import for module-level visibility

    print("Loading words.parquet...")
    df = pd.read_parquet(PARQUET_PATH)

    print("Building lemma map from OT-wide data...")
    lemma_map = build_lemma_map(df)
    print(f"  {len(lemma_map)} Strong's → lemma entries")

    # Build Ps 119 verse lookup: verse → [(clean_word, morph_code, strongs_raw)]
    ps119 = df[(df['book_id'] == 'Psa') & (df['chapter'] == 119)].copy()
    verse_lookup: dict[int, list[tuple[str, str, str]]] = {}
    for _, row in ps119.iterrows():
        v = int(row['verse'])
        cw = _clean(str(row['word']))
        mc = str(row.get('morph_code', '') or '')
        st = str(row.get('strongs', '') or '')
        verse_lookup.setdefault(v, []).append((cw, mc, st))

    print(f"  Ps 119 word tokens: {sum(len(v) for v in verse_lookup.values())}")

    print(f"Loading {YAML_PATH}...")
    with open(YAML_PATH, encoding='utf-8') as f:
        data = yaml.safe_load(f)

    matched = missed = skipped = 0
    for stanza in data['stanzas']:
        for verse in stanza['verses']:
            vnum = int(verse['abs_num'])
            tokens = verse_lookup.get(vnum, [])
            for kw in (verse.get('key_words') or []) + (verse.get('line_endings') or []):
                if not isinstance(kw, dict):
                    continue
                if kw.get('pos') and not FORCE:
                    skipped += 1
                    continue
                if _annotate_kw(kw, tokens):
                    # Assign lemma
                    word = unicodedata.normalize('NFC', kw.get('word', ''))
                    strongs_raw = next(
                        (st for cw, mc, st in tokens
                         if unicodedata.normalize('NFC', cw) == word),
                        ''
                    )
                    sk = _extract_strongs(strongs_raw)
                    if sk and sk in lemma_map:
                        kw['lemma'] = lemma_map[sk]
                    matched += 1
                else:
                    missed += 1

    print(f"Annotation: matched={matched}, missed={missed}, skipped(already done)={skipped}")
    if missed:
        print("  Missed words (check normalization):")
        for stanza in data['stanzas']:
            for verse in stanza['verses']:
                vnum = int(verse['abs_num'])
                tokens = verse_lookup.get(vnum, [])
                for kw in (verse.get('key_words') or []) + (verse.get('line_endings') or []):
                    if isinstance(kw, dict) and not kw.get('pos'):
                        word = unicodedata.normalize('NFC', kw.get('word', ''))
                        clean_tokens = [cw for cw, _, _ in tokens]
                        print(f"    v{vnum}: {kw.get('word')} → closest: "
                              f"{[t for t in clean_tokens if any(ch in word for ch in t)][:3]}")

    with open(YAML_PATH, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False,
                  sort_keys=False, width=10000)
    print(f"Wrote {YAML_PATH}")


if __name__ == '__main__':
    annotate()
