"""
Verb-argument (governance) extraction from the MACULA Hebrew lowfat syntax trees.

The flattened word-level table built by ``syntax_ot.py`` (one row per token, in
document order) throws away the constituency tree — it cannot reliably tell
you whether a preposition immediately after a verb is that verb's governed
complement, an unrelated adjunct, or something else entirely.  The raw lowfat
XML (``macula-hebrew/WLC/lowfat/*.xml``) still has the tree: every clause is a
``<wg class="cl">`` node, and a verb's arguments — subject, direct object,
prepositional complement(s) — are its *sibling* children within that same
clause node, each tagged with a ``role`` attribute (``s``, ``v``, ``o``,
``o2``, ``pp``, ``adv``, …).

This module walks that tree directly (not the flattened table) to answer,
for every finite verb occurrence in the OT: what preposition (if any)
introduces its complement, or does it take a bare/marked direct object, or
neither?  One row per (verb occurrence × argument) is cached as Parquet —
mirroring the ``syntax_ot.py`` / ``syntax.py`` build-once-cache-forever
pattern — for the query layer in ``ot/verb_governance.py`` to consume.

Schema (one row per verb-occurrence × argument; a verb occurrence with no
qualifying argument gets a single ``arg_role='none'`` row)
────────────────────────────────────────────────────────────────────────────
  verb_xml_id       : xml:id of the verb token
  ref               : "JER 17:5!7" style reference (of the verb token)
  book, chapter, verse
  verb_lemma        : pointed lexical form, e.g. 'בָּטַח'
  verb_strongnumberx: extended Strong's number, e.g. '0982'
  verb_stem         : qal / niphal / piel / …
  verb_type         : qatal / yiqtol / wayyiqtol / imperative / participle / …
  verb_person, verb_gender, verb_number
  n_args            : how many qualifying arguments (pp/o/o2) this occurrence has
  arg_index         : 0-based position of this argument among the clause's
                       direct-child arguments, in document order
  arg_role          : 'pp' | 'o' | 'o2' | 'none'
  prep_lemma        : governing preposition's lemma (arg_role=='pp' only)
  prep_strongnumberx
  has_object_marker : True if the argument phrase contains אֵת (class='om')
                       (meaningful for arg_role in {'o','o2'} only)
  head_lemma        : best-effort head noun/pronoun of the argument phrase
  head_strongnumberx
  head_gloss
  arg_text          : concatenated surface text of the argument phrase
  arg_gloss         : concatenated glosses of the argument phrase

Usage
─────
from bible_grammar.core.verb_governance import load_verb_governance

df = load_verb_governance()                  # full DataFrame, all OT verbs
batach = df[df['verb_strongnumberx'] == '0982']
"""

from __future__ import annotations
from pathlib import Path
from typing import Any, Optional
import pandas as pd

from .syntax_ot import MACULA_OT_BOOK_MAP

_REPO_ROOT = Path(__file__).resolve().parents[3]
_MACULA_OT_DIR = _REPO_ROOT / "macula-hebrew" / "WLC" / "lowfat"
_GOVERNANCE_PARQUET = _REPO_ROOT / "data" / "processed" / "macula_verb_governance.parquet"

_cache: Optional[pd.DataFrame] = None

# Argument roles we treat as a verb's governed complements. Other role values
# on clause-siblings ('s' subject, 'adv' single-word adverbs, 'p' predicate)
# are not complements in the sense this module is built to answer.
_ARG_ROLES = {'pp', 'o', 'o2'}

# Word classes that count as a plausible "head" of an argument phrase, in
# priority order (first match wins).
_HEAD_CLASSES = ('noun', 'pron', 'adj')


def _parse_ref(ref: str) -> tuple[str, int, int]:
    """'JER 17:5!7' -> (book_id, chapter, verse). Reuses the same MACULA
    book-code map as syntax_ot.py so book IDs stay consistent project-wide."""
    try:
        book_part, rest = ref.split(' ', 1)
        cv = rest.split('!', 1)[0]
        ch, vs = cv.split(':')
        return (MACULA_OT_BOOK_MAP.get(book_part, book_part), int(ch), int(vs))
    except Exception:
        return ('', 0, 0)


def _word_text(w: Any) -> str:
    return w.get('unicode', w.text or '')


def _arg_phrase_info(wg_or_w: Any, *, is_pp: bool) -> dict:
    """Extract prep/head/text/gloss info from an argument constituent, which
    may be a single <w> (bare token argument) or a <wg> subtree (phrase)."""
    words = list(wg_or_w.iter('w')) if wg_or_w.tag == 'wg' else [wg_or_w]

    prep_lemma = ''
    prep_strongnumberx = ''
    has_object_marker = False
    head_lemma = ''
    head_strongnumberx = ''
    head_gloss = ''
    text_parts = []
    gloss_parts = []

    for w in words:
        cls = w.get('class', '')
        if cls == 'om':
            has_object_marker = True
        if is_pp and cls == 'prep' and not prep_lemma:
            prep_lemma = w.get('lemma', '')
            prep_strongnumberx = w.get('strongnumberx', '')
            continue  # don't fold the preposition itself into the "complement" text/head
        if not head_lemma and cls in _HEAD_CLASSES:
            head_lemma = w.get('lemma', '')
            head_strongnumberx = w.get('strongnumberx', '')
            head_gloss = w.get('gloss', '')
        text_parts.append(_word_text(w))
        gloss_parts.append(w.get('gloss', ''))

    return {
        'prep_lemma': prep_lemma,
        'prep_strongnumberx': prep_strongnumberx,
        'has_object_marker': has_object_marker,
        'head_lemma': head_lemma,
        'head_strongnumberx': head_strongnumberx,
        'head_gloss': head_gloss,
        'arg_text': ''.join(text_parts),
        'arg_gloss': ' '.join(g for g in gloss_parts if g),
    }


def _extract_file(xml_file: str, rows: list[dict]) -> None:
    import xml.etree.ElementTree as ET

    tree = ET.parse(xml_file)
    root = tree.getroot()

    parent_map = {child: parent for parent in root.iter() for child in parent}

    for v in root.iter('w'):
        if v.get('role') != 'v':
            continue
        ref = v.get('ref', '')
        if not ref:
            continue
        book, ch, vs = _parse_ref(ref)

        clause = parent_map.get(v)
        siblings = list(clause) if clause is not None else []

        args = []
        for sib in siblings:
            if sib is v:
                continue
            role = sib.get('role', '')
            if role not in _ARG_ROLES:
                continue
            info = _arg_phrase_info(sib, is_pp=(role == 'pp'))
            args.append({'arg_role': role, **info})

        base = {
            'verb_xml_id':        v.get('{http://www.w3.org/XML/1998/namespace}id') or v.get('xml:id', ''),
            'ref':                ref,
            'book':                book,
            'chapter':             ch,
            'verse':               vs,
            'verb_lemma':          v.get('lemma', ''),
            'verb_strongnumberx':  v.get('strongnumberx', ''),
            'verb_stem':           v.get('stem', ''),
            'verb_type':           v.get('type', ''),
            'verb_person':         v.get('person', ''),
            'verb_gender':         v.get('gender', ''),
            'verb_number':         v.get('number', ''),
            'n_args':              len(args),
        }

        if not args:
            rows.append({
                **base, 'arg_index': -1, 'arg_role': 'none',
                'prep_lemma': '', 'prep_strongnumberx': '',
                'has_object_marker': False,
                'head_lemma': '', 'head_strongnumberx': '', 'head_gloss': '',
                'arg_text': '', 'arg_gloss': '',
            })
        else:
            for i, arg in enumerate(args):
                rows.append({**base, 'arg_index': i, **arg})


def _build_parquet() -> pd.DataFrame:
    if not _MACULA_OT_DIR.exists():
        raise FileNotFoundError(
            f"MACULA Hebrew lowfat XML not found at {_MACULA_OT_DIR}.\n"
            "Run: git submodule update --init macula-hebrew"
        )

    import glob

    xml_files = sorted(glob.glob(str(_MACULA_OT_DIR / '*.xml')))
    rows: list[dict] = []
    for xml_file in xml_files:
        _extract_file(xml_file, rows)

    df = pd.DataFrame(rows)
    for col in ('chapter', 'verse', 'n_args', 'arg_index'):
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int16')
    df['has_object_marker'] = df['has_object_marker'].astype(bool)

    _GOVERNANCE_PARQUET.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(_GOVERNANCE_PARQUET, index=False)
    return df


def load_verb_governance(force_rebuild: bool = False) -> pd.DataFrame:
    """
    Load the verb-argument (governance) DataFrame.

    On first call, walks all 930 lowfat XML files' constituency trees and
    caches the result as Parquet (a couple of minutes — slower than
    syntax_ot.py's flat build since this does per-verb sibling extraction).
    Subsequent calls load from Parquet. Pass force_rebuild=True to re-parse.
    """
    global _cache
    if _cache is not None and not force_rebuild:
        return _cache

    if _GOVERNANCE_PARQUET.exists() and not force_rebuild:
        _cache = pd.read_parquet(_GOVERNANCE_PARQUET)
    else:
        print("Building verb-governance Parquet cache from MACULA lowfat trees "
              "(first run only)…")
        _cache = _build_parquet()
        print(f"  Cached {len(_cache):,} argument rows → {_GOVERNANCE_PARQUET}")

    return _cache
