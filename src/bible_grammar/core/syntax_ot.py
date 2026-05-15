"""
MACULA Hebrew syntax layer — general-purpose query API for the OT.

Wraps the WLC lowfat XML files from the macula-hebrew submodule and caches
a flattened DataFrame as Parquet for fast reloads.  Parallel to syntax.py
(MACULA Greek) so the same query patterns work for both testaments.

Schema (word-level columns)
───────────────────────────
  xml_id         : unique token ID  (e.g. o010010010011)
  ref            : "GEN 1:1!1" style reference
  book           : our canonical book_id (e.g. "Gen")
  chapter        : int
  verse          : int
  word_num       : int (1-based position in verse)
  text           : surface form with cantillation (unicode)
  lemma          : lexical headword
  transliteration: transliteration
  strongnumberx  : extended Strong's number (e.g. "7225")
  strong_h       : "H"-prefixed form compatible with rest of project (e.g. "H7225")
  stronglemma    : lemma of the Strong's entry
  morph          : morphology code (e.g. "Vqp3ms")
  pos            : part of speech (verb / noun / prep / conj / …)
  class_         : syntactic class (verb / noun / prep / …)
  type_          : qatal / wayyiqtol / common / proper / …
  lang           : H (Hebrew) or A (Aramaic)
  stem           : qal / niphal / piel / pual / hiphil / hophal / hithpael / …
  gender         : masculine / feminine / common
  number         : singular / plural / dual
  person         : first / second / third
  state          : absolute / construct / determined
  role           : s / v / o / io / p / adv / … (syntactic role in clause)
  gloss          : short English gloss
  english        : contextual English translation
  frame          : argument frame  (e.g. "A0:id; A1:id;")
  subjref        : xml_id of the subject referent
  participantref : xml_id of the antecedent for pronouns/suffixes
  greek          : LXX Greek word (inline OT↔LXX alignment)
  greekstrong    : LXX Strong's number (plain integer string, e.g. "4160")
  greek_g        : "G"-prefixed LXX Strong's (e.g. "G4160")
  lexdomain      : Louw-Nida style semantic domain
  coredomain     : core semantic domain
  sdbh           : SDBH semantic domain

Usage
─────
from bible_grammar.core.syntax_ot import (
    load_syntax_ot, query_syntax_ot, MACULA_OT_BOOK_MAP,
)

df = load_syntax_ot()                           # full 475k-row DataFrame
verbs = query_syntax_ot(strong_h='H1254')       # all בָּרָא tokens
niphal = query_syntax_ot(stem='niphal', book='Isa')
lxx_paieo = query_syntax_ot(greekstrong='4160') # OT words translated as ποιέω
"""

from __future__ import annotations
from pathlib import Path
from typing import Any
import pandas as pd

_REPO_ROOT = Path(__file__).resolve().parents[2]
_MACULA_OT_DIR = _REPO_ROOT / "macula-hebrew" / "WLC" / "lowfat"
_OT_PARQUET = _REPO_ROOT / "data" / "processed" / "macula_syntax_ot.parquet"

# MACULA all-caps → our title-case book_id
MACULA_OT_BOOK_MAP: dict[str, str] = {
    'GEN': 'Gen', 'EXO': 'Exo', 'LEV': 'Lev', 'NUM': 'Num', 'DEU': 'Deu',
    'JOS': 'Jos', 'JDG': 'Jdg', 'RUT': 'Rut', '1SA': '1Sa', '2SA': '2Sa',
    '1KI': '1Ki', '2KI': '2Ki', '1CH': '1Ch', '2CH': '2Ch', 'EZR': 'Ezr',
    'NEH': 'Neh', 'EST': 'Est', 'JOB': 'Job', 'PSA': 'Psa', 'PRO': 'Pro',
    'ECC': 'Ecc', 'SNG': 'Sng', 'ISA': 'Isa', 'JER': 'Jer', 'LAM': 'Lam',
    'EZK': 'Ezk', 'DAN': 'Dan', 'HOS': 'Hos', 'JOL': 'Jol', 'AMO': 'Amo',
    'OBA': 'Oba', 'JON': 'Jon', 'MIC': 'Mic', 'NAM': 'Nam', 'HAB': 'Hab',
    'ZEP': 'Zep', 'HAG': 'Hag', 'ZEC': 'Zec', 'MAL': 'Mal',
}
OUR_OT_BOOK_MAP: dict[str, str] = {v: k for k, v in MACULA_OT_BOOK_MAP.items()}

_cache: pd.DataFrame | None = None


def _parse_ref(ref: str) -> tuple[str, int, int, int]:
    """'GEN 1:1!2' → (book_id, chapter, verse, word_num)."""
    try:
        book_part, rest = ref.split(' ', 1)
        if '!' in rest:
            cv, wn = rest.split('!', 1)
        else:
            cv, wn = rest, '1'
        ch, vs = cv.split(':')
        return (
            MACULA_OT_BOOK_MAP.get(book_part, book_part),
            int(ch), int(vs), int(wn),
        )
    except Exception:
        return ('', 0, 0, 0)


def _xml_id(elem: Any) -> str:
    return (elem.get('{http://www.w3.org/XML/1998/namespace}id') or
            elem.get('xml:id') or '')


def _build_parquet() -> pd.DataFrame:
    if not _MACULA_OT_DIR.exists():
        raise FileNotFoundError(
            f"MACULA Hebrew lowfat XML not found at {_MACULA_OT_DIR}.\n"
            "Run: git submodule update --init macula-hebrew"
        )

    import xml.etree.ElementTree as ET
    import glob

    xml_files = sorted(glob.glob(str(_MACULA_OT_DIR / '*.xml')))
    rows = []

    for xml_file in xml_files:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for w in root.iter('w'):
            ref = w.get('ref', '')
            if not ref:
                continue
            book, ch, vs, wn = _parse_ref(ref)
            gstrong = w.get('greekstrong', '')
            rows.append({
                'xml_id':          _xml_id(w),
                'ref':             ref,
                'book':            book,
                'chapter':         ch,
                'verse':           vs,
                'word_num':        wn,
                'text':            w.get('unicode', w.text or ''),
                'lemma':           w.get('lemma', ''),
                'transliteration': w.get('transliteration', ''),
                'strongnumberx':   w.get('strongnumberx', ''),
                'strong_h':        ('H' + w.get('strongnumberx', '').lstrip('0')
                                    if w.get('strongnumberx') else ''),
                'stronglemma':     w.get('stronglemma', ''),
                'morph':           w.get('morph', ''),
                'pos':             w.get('pos', ''),
                'class_':          w.get('class', ''),
                'type_':           w.get('type', ''),
                'lang':            w.get('lang', 'H'),
                'stem':            w.get('stem', ''),
                'gender':          w.get('gender', ''),
                'number':          w.get('number', ''),
                'person':          w.get('person', ''),
                'state':           w.get('state', ''),
                'role':            w.get('role', ''),
                'gloss':           w.get('gloss', ''),
                'english':         w.get('english', ''),
                'frame':           w.get('frame', ''),
                'subjref':         w.get('subjref', '') or None,
                'participantref':  w.get('participantref', '') or None,
                'greek':           w.get('greek', ''),
                'greekstrong':     gstrong,
                'greek_g':         (f"G{int(gstrong):04d}" if gstrong.isdigit() else ''),
                'lexdomain':       w.get('lexdomain', ''),
                'coredomain':      w.get('coredomain', ''),
                'sdbh':            w.get('sdbh', ''),
                'sensenumber':     w.get('sensenumber', ''),
            })

    df = pd.DataFrame(rows)
    # Convert coordinate columns to compact integer types
    for col in ('chapter', 'verse', 'word_num'):
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int16')

    _OT_PARQUET.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(_OT_PARQUET, index=False)
    return df


def load_syntax_ot(force_rebuild: bool = False) -> pd.DataFrame:
    """
    Load MACULA Hebrew syntax DataFrame.

    On first call, parses all 930 lowfat XML files and caches as Parquet
    (~30–60 s depending on machine).  Subsequent calls load from Parquet
    (~0.5 s).  Pass force_rebuild=True to re-parse from XML.
    """
    global _cache
    if _cache is not None and not force_rebuild:
        return _cache

    if _OT_PARQUET.exists() and not force_rebuild:
        _cache = pd.read_parquet(_OT_PARQUET)
    else:
        print("Building MACULA Hebrew syntax Parquet cache (first run only)…")
        _cache = _build_parquet()
        print(f"  Cached {len(_cache):,} word tokens → {_OT_PARQUET}")

    return _cache


def query_syntax_ot(
    *,
    book: str | None = None,
    chapter: int | None = None,
    verse: int | None = None,
    strong_h: str | None = None,
    strongnumberx: str | None = None,
    lemma: str | None = None,
    role: str | None = None,
    stem: str | None = None,
    pos: str | None = None,
    lang: str | None = None,
    tense: str | None = None,
    person: str | None = None,
    gender: str | None = None,
    number: str | None = None,
    state: str | None = None,
    greekstrong: str | int | None = None,
    has_subjref: bool | None = None,
    has_participantref: bool | None = None,
) -> pd.DataFrame:
    """
    Filtered query over the MACULA Hebrew syntax table.

    strong_h accepts 'H7225', 'H7225A', or plain '7225'.
    greekstrong accepts G-prefixed ('G4160'), plain int (4160), or string ('4160').
    tense is matched against the type_ column (e.g. 'qatal', 'wayyiqtol').
    """
    df = load_syntax_ot()

    if book is not None:
        df = df[df['book'] == book]
    if chapter is not None:
        df = df[df['chapter'] == chapter]
    if verse is not None:
        df = df[df['verse'] == verse]

    if strong_h is not None:
        # Normalise: strip H prefix and leading zeros for comparison
        s = str(strong_h).upper().lstrip('H')
        df = df[df['strongnumberx'].str.upper().str.lstrip('0') == s.lstrip('0')]
    if strongnumberx is not None:
        df = df[df['strongnumberx'] == strongnumberx]
    if lemma is not None:
        df = df[df['lemma'] == lemma]
    if role is not None:
        df = df[df['role'] == role]
    if stem is not None:
        df = df[df['stem'].str.lower() == stem.lower()]
    if pos is not None:
        df = df[df['pos'].str.lower() == pos.lower()]
    if lang is not None:
        df = df[df['lang'] == lang.upper()]
    if tense is not None:
        df = df[df['type_'].str.lower() == tense.lower()]
    if person is not None:
        df = df[df['person'] == person]
    if gender is not None:
        df = df[df['gender'] == gender]
    if number is not None:
        df = df[df['number'] == number]
    if state is not None:
        df = df[df['state'] == state]

    if greekstrong is not None:
        gs = str(greekstrong).lstrip('Gg0') or '0'
        plain = str(int(gs)) if gs.isdigit() else gs
        df = df[df['greekstrong'] == plain]

    if has_subjref is True:
        df = df[df['subjref'].notna() & (df['subjref'] != '')]
    if has_subjref is False:
        df = df[df['subjref'].isna() | (df['subjref'] == '')]
    if has_participantref is True:
        df = df[df['participantref'].notna() & (df['participantref'] != '')]
    if has_participantref is False:
        df = df[df['participantref'].isna() | (df['participantref'] == '')]

    return df


def lxx_alignment(
    strong_h: str | None = None,
    *,
    book: str | None = None,
    min_count: int = 3,
    top_n: int = 10,
) -> pd.DataFrame:
    """
    Return the LXX word(s) most frequently used to translate a Hebrew lemma,
    derived from the inline greek/greekstrong columns in MACULA Hebrew.

    Returns a DataFrame: greek_g, greek_lemma, greekstrong, count, pct.
    This is a word-level OT↔LXX alignment from the syntax tree itself
    (as opposed to the IBM Model 1 alignment in ibm_align.py).
    """
    df = query_syntax_ot(strong_h=strong_h, book=book)
    df = df[df['greekstrong'].notna() & (df['greekstrong'] != '')]

    if df.empty:
        return pd.DataFrame(columns=['greek_g', 'greekstrong', 'count', 'pct'])

    counts = (
        df.groupby(['greekstrong', 'greek'])
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
        .head(top_n)
    )
    counts = counts[counts['count'] >= min_count].copy()
    total = counts['count'].sum()
    counts['pct'] = (counts['count'] / total * 100).round(1)
    counts['greek_g'] = counts['greekstrong'].apply(
        lambda s: f"G{int(s):04d}" if s.isdigit() else s
    )
    return counts[['greek_g', 'greekstrong', 'greek', 'count', 'pct']].reset_index(drop=True)


def clause_roles_ot(book: str | None = None, chapter: int | None = None,
                    verse: int | None = None) -> pd.DataFrame:
    """
    Return the syntactic role of each word in the given scope.
    Useful for subject-verb-object analysis per clause.
    """
    df = query_syntax_ot(book=book, chapter=chapter, verse=verse)
    return df[['book', 'chapter', 'verse', 'word_num',
               'text', 'lemma', 'strong_h', 'role', 'gloss',
               'stem', 'type_', 'greek', 'greek_g']].copy()
