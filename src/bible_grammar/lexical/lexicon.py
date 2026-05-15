"""
Lexicon module — public API over the STEPBible TBESH (Hebrew) and
TBESG (Greek) brief lexicons that ship with the stepbible-data submodule.

Previously these were private helpers inside wordstudy.py.  Promoting them
here makes lexicon lookups available to any module and to notebook code.

Data model
──────────
Each entry is a dict:
  strongs      : canonical extended Strong's (e.g. "H1254A", "G4160")
  lemma        : Hebrew/Greek headword
  translit     : transliteration
  pos_code     : language:type-gender-extra (e.g. "H:V", "G:N-M")
  gloss        : short English gloss
  definition   : full definition (HTML stripped)

Usage
─────
from bible_grammar.lexical.lexicon import lookup, search_gloss, lex_entry

# Single lookup
entry = lookup('H1254')    # בָּרָא
entry = lookup('G4160')    # ποιέω
entry = lookup('G2424')    # Ἰησοῦς

# Fuzzy gloss search
results = search_gloss('create', lang='H')

# Print formatted entry
lex_entry('H7965')         # שָׁלוֹם

# Available after submodule init; gracefully returns {} if lexicon missing.
"""

from __future__ import annotations
import re
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_TBESH = _REPO_ROOT / "stepbible-data" / "Lexicons" / \
    "TBESH - Translators Brief lexicon of Extended Strongs for Hebrew - STEPBible.org CC BY.txt"
_TBESG = _REPO_ROOT / "stepbible-data" / "Lexicons" / \
    "TBESG - Translators Brief lexicon of Extended Strongs for Greek - STEPBible.org CC BY.txt"

_heb_cache: dict | None = None
_grk_cache: dict | None = None


# ── Internal helpers ──────────────────────────────────────────────────────────

def _clean_def(raw: str) -> str:
    text = re.sub(r'<[^>]+>', ' ', raw)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _parse_tbesh() -> dict[str, dict]:
    result: dict[str, dict] = {}
    if not _TBESH.exists():
        return result
    with open(_TBESH, encoding='utf-8') as fh:
        for line in fh:
            line = line.rstrip('\n')
            if not line or line.startswith('#') or line.startswith('='):
                continue
            parts = line.split('\t')
            if len(parts) < 7:
                continue
            ext_id = parts[2].strip()
            if not ext_id or not ext_id.startswith('H'):
                continue
            base = re.sub(r'[A-Z]$', '', ext_id)
            lemma = parts[3].strip()
            translit = parts[4].strip()
            pos_code = parts[5].strip()
            gloss = parts[6].strip()
            defn = _clean_def(parts[7]) if len(parts) > 7 else ''
            entry = {
                'strongs': ext_id, 'lemma': lemma,
                'translit': translit, 'pos_code': pos_code,
                'gloss': gloss, 'definition': defn,
            }
            for key in (base, ext_id):
                if key and key not in result:
                    result[key] = entry
    return result


def _parse_tbesg() -> dict[str, dict]:
    result: dict[str, dict] = {}
    if not _TBESG.exists():
        return result
    with open(_TBESG, encoding='utf-8') as fh:
        for line in fh:
            line = line.rstrip('\n')
            if not line or line.startswith('#') or line.startswith('='):
                continue
            parts = line.split('\t')
            if len(parts) < 7:
                continue
            ext_id = parts[2].strip()
            if not ext_id or not ext_id.startswith('G'):
                continue
            base = re.sub(r'[A-Z]$', '', ext_id)
            lemma = parts[3].strip()
            translit = parts[4].strip()
            pos_code = parts[5].strip()
            gloss = parts[6].strip()
            defn = _clean_def(parts[7]) if len(parts) > 7 else ''
            entry = {
                'strongs': ext_id, 'lemma': lemma,
                'translit': translit, 'pos_code': pos_code,
                'gloss': gloss, 'definition': defn,
            }
            for key in (base, ext_id):
                if key and key not in result:
                    result[key] = entry
    return result


def _heb() -> dict[str, dict]:
    global _heb_cache
    if _heb_cache is None:
        _heb_cache = _parse_tbesh()
    return _heb_cache


def _grk() -> dict[str, dict]:
    global _grk_cache
    if _grk_cache is None:
        _grk_cache = _parse_tbesg()
    return _grk_cache


# ── Public API ────────────────────────────────────────────────────────────────

def lookup(strongs: str) -> dict:
    """
    Return the lexicon entry for a Strong's number.

    Accepts any of: 'H1254', 'H1254A', 'G2424', 'G2424G'.
    Returns {} if not found or lexicon file missing.
    """
    s = strongs.strip()
    if s.startswith('H') or s.startswith('h'):
        s = s.upper()
        return _heb().get(s, {})
    if s.startswith('G') or s.startswith('g'):
        s = s.upper()
        return _grk().get(s, {})
    return {}


def search_gloss(
    query: str,
    *,
    lang: str | None = None,
    max_results: int = 20,
) -> list[dict]:
    """
    Search entries whose gloss or definition contains *query* (case-insensitive).

    lang : 'H' for Hebrew only, 'G' for Greek only, None for both.
    Returns a list of entry dicts (includes 'strongs' key).
    """
    q = query.lower()
    results = []
    if lang in (None, 'H'):
        for k, v in _heb().items():
            if re.sub(r'[A-Z]$', '', k) != k:
                continue  # skip extended duplicates
            if q in v.get('gloss', '').lower() or q in v.get('definition', '').lower():
                results.append(v)
    if lang in (None, 'G'):
        for k, v in _grk().items():
            if re.sub(r'[A-Z]$', '', k) != k:
                continue
            if q in v.get('gloss', '').lower() or q in v.get('definition', '').lower():
                results.append(v)
    return results[:max_results]


def lex_entry(strongs: str) -> None:
    """Print a formatted lexicon entry to stdout."""
    entry = lookup(strongs)
    if not entry:
        print(f"No entry found for {strongs!r}")
        return
    w = 72
    print(f"\n{'═' * w}")
    print(f"  {entry['strongs']}  {entry['lemma']}  ({entry['translit']})")
    print(f"  POS: {entry['pos_code']}   Gloss: {entry['gloss']}")
    print(f"{'─' * w}")
    defn = entry.get('definition', '')
    # Word-wrap definition at 68 chars
    words = defn.split()
    line = '  '
    for word in words:
        if len(line) + len(word) + 1 > 70:
            print(line)
            line = '  ' + word
        else:
            line += (' ' if line.strip() else '') + word
    if line.strip():
        print(line)
    print(f"{'═' * w}\n")


def lemma_index(lang: str) -> dict[str, str]:
    """
    Return a {lemma → strongs} reverse lookup for fast lemma-to-Strong's
    resolution.  lang='H' or 'G'.

    Normalises Greek lemmas to lowercase NFC.
    Used by resolve_strongs() and the word-study module.
    """
    import unicodedata
    result: dict[str, str] = {}
    src = _heb() if lang.upper() == 'H' else _grk()
    for k, v in src.items():
        # Only index base (not extended) numbers
        if re.sub(r'[A-Z]$', '', k) != k:
            continue
        lemma = v.get('lemma', '').strip()
        if not lemma:
            continue
        if lang.upper() == 'G':
            lemma = unicodedata.normalize('NFC', lemma.lower())
        else:
            lemma = unicodedata.normalize('NFC', lemma)
        if lemma not in result:
            result[lemma] = k
        # Also index stripped consonants for Hebrew
        if lang.upper() == 'H':
            consonants = re.sub(r'[֑-ׇ]', '', lemma)
            if consonants not in result:
                result[consonants] = k
    return result
