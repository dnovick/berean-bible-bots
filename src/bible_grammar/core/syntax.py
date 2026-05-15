"""
MACULA Greek syntax layer — general-purpose query API.

Wraps the Nestle1904 TSV from the macula-greek submodule and caches it as
Parquet for fast reloads.  All downstream modules (speaker, syntactic studies,
discourse analysis) import from here rather than reading the TSV directly.

Schema (column subset that matters)
─────────────────────────────────────
  xml_id    : unique word token ID (e.g. n40001001001)
  ref       : "MAT 1:1!1" style reference
  book      : our canonical book_id (e.g. "Mat")
  chapter   : int
  verse     : int
  word_num  : int (1-based position in verse)
  text      : surface form
  lemma     : dictionary headword
  strong    : Strong's number as plain integer string (e.g. "2424")
  strong_g  : "G"-prefixed form compatible with rest of project (e.g. "G2424")
  morph     : morph code (e.g. "N-NSF")
  class_    : noun / verb / adj / prep / conj / det / ptcl / adv
  type_     : common / proper / personal / relative / …
  role      : s / v / o / io / p / vc / adv / aux / o2
  gloss     : English word gloss
  person    : first / second / third
  number    : singular / plural
  gender    : masculine / feminine / neuter
  case_     : nominative / genitive / dative / accusative / vocative
  tense     : aorist / present / perfect / future / imperfect / pluperfect
  voice     : active / passive / middle
  mood      : indicative / subjunctive / infinitive / participle / imperative / optative
  subjref   : xml_id of the subject referent (links subject nouns/pronouns to clauses)
  referent  : xml_id this word refers to (coreferential chain)
  domain    : Louw-Nida semantic domain code(s)

Usage
─────
from bible_grammar.core.syntax import (
    load_syntax, query_syntax, speech_verbs, referent_chain,
    MACULA_BOOK_MAP,
)

df = load_syntax()                          # full 137k-row DataFrame
verbs = query_syntax(strong='2424')         # all Jesus tokens
speech = speech_verbs(book='Mat')           # speech-introducing verbs in Matthew
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd

_REPO_ROOT = Path(__file__).resolve().parents[2]
_MACULA_TSV = (_REPO_ROOT / "macula-greek" / "Nestle1904" / "tsv"
               / "macula-greek-Nestle1904.tsv")
_SYNTAX_PARQUET = _REPO_ROOT / "data" / "processed" / "macula_syntax.parquet"

# MACULA all-caps → our title-case book_id
MACULA_BOOK_MAP: dict[str, str] = {
    'MAT': 'Mat', 'MRK': 'Mrk', 'LUK': 'Luk', 'JHN': 'Jhn',
    'ACT': 'Act', 'ROM': 'Rom', '1CO': '1Co', '2CO': '2Co',
    'GAL': 'Gal', 'EPH': 'Eph', 'PHP': 'Php', 'COL': 'Col',
    '1TH': '1Th', '2TH': '2Th', '1TI': '1Ti', '2TI': '2Ti',
    'TIT': 'Tit', 'PHM': 'Phm', 'HEB': 'Heb', 'JAS': 'Jas',
    '1PE': '1Pe', '2PE': '2Pe', '1JN': '1Jn', '2JN': '2Jn',
    '3JN': '3Jn', 'JUD': 'Jud', 'REV': 'Rev',
}
# Reverse map: our book_id → MACULA
OUR_BOOK_MAP: dict[str, str] = {v: k for k, v in MACULA_BOOK_MAP.items()}

# Greek speech-introducing verbs (Strong's numbers as plain strings)
SPEECH_VERB_STRONGS: set[str] = {'3004', '5346', '2980', '611', '2036', '1941', '3670'}

_cache: pd.DataFrame | None = None


def _parse_ref(ref_series: pd.Series) -> pd.DataFrame:
    """Split 'MAT 1:1!1' into book/chapter/verse/word_num columns."""
    split1 = ref_series.str.split(' ', n=1, expand=True)
    macula_book = split1[0]
    rest = split1[1]  # "1:1!1"
    cv_wn = rest.str.split('[!:]', expand=True)
    return pd.DataFrame({
        'book':     macula_book.map(MACULA_BOOK_MAP).fillna(macula_book),
        'chapter':  cv_wn[0].astype('Int16'),
        'verse':    cv_wn[1].astype('Int16'),
        'word_num': cv_wn[2].astype('Int16'),
    })


def _build_parquet() -> pd.DataFrame:
    if not _MACULA_TSV.exists():
        raise FileNotFoundError(
            f"MACULA Greek TSV not found at {_MACULA_TSV}.\n"
            "Run: git submodule update --init macula-greek"
        )
    raw = pd.read_csv(_MACULA_TSV, sep='\t', dtype=str, low_memory=False)

    # Rename columns that clash with Python builtins or our schema
    raw = raw.rename(columns={
        'xml:id':  'xml_id',
        'class':   'class_',
        'type':    'type_',
        'case':    'case_',
    })

    coords = _parse_ref(raw['ref'])
    df = pd.concat([raw, coords], axis=1)

    def _to_strong_g(s: object) -> str | None:
        if not pd.notna(s) or not str(s).strip():
            return None
        # Some entries are compound like '1537+4053' — use the first number
        first = str(s).split('+')[0].strip()
        try:
            return f"G{int(float(first)):04d}"
        except ValueError:
            return None

    df['strong_g'] = df['strong'].apply(_to_strong_g)

    # Select and order columns we care about
    keep = [
        'xml_id', 'ref', 'book', 'chapter', 'verse', 'word_num',
        'text', 'lemma', 'strong', 'strong_g', 'morph',
        'class_', 'type_', 'role', 'gloss',
        'person', 'number', 'gender', 'case_',
        'tense', 'voice', 'mood',
        'subjref', 'referent', 'domain', 'ln',
        'english',
    ]
    keep = [c for c in keep if c in df.columns]
    df = df[keep].copy()

    _SYNTAX_PARQUET.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(_SYNTAX_PARQUET, index=False)
    return df


def load_syntax(force_rebuild: bool = False) -> pd.DataFrame:
    """
    Load MACULA Greek syntax DataFrame.

    On first call, parses the TSV and caches as Parquet (~4 s).
    Subsequent calls load the Parquet (~0.3 s).
    Pass force_rebuild=True to re-parse the TSV.
    """
    global _cache
    if _cache is not None and not force_rebuild:
        return _cache

    if _SYNTAX_PARQUET.exists() and not force_rebuild:
        _cache = pd.read_parquet(_SYNTAX_PARQUET)
    else:
        print("Building MACULA syntax Parquet cache (first run only)…")
        _cache = _build_parquet()
        print(f"  Cached {len(_cache):,} word tokens → {_SYNTAX_PARQUET}")

    return _cache


def query_syntax(
    *,
    book: str | None = None,
    chapter: int | None = None,
    verse: int | None = None,
    strong: str | int | None = None,
    lemma: str | None = None,
    role: str | None = None,
    class_: str | None = None,
    tense: str | None = None,
    voice: str | None = None,
    mood: str | None = None,
    case_: str | None = None,
    has_subjref: bool | None = None,
    has_referent: bool | None = None,
) -> pd.DataFrame:
    """
    Filtered query over the MACULA syntax table.

    strong can be given as plain integer ('2424'), G-prefixed ('G2424'),
    or int (2424) — all three forms are accepted.
    """
    df = load_syntax()

    if book is not None:
        df = df[df['book'] == book]
    if chapter is not None:
        df = df[df['chapter'] == chapter]
    if verse is not None:
        df = df[df['verse'] == verse]
    if strong is not None:
        s = str(strong).lstrip('Gg0').lstrip('0') or '0'
        # Normalise to no-prefix integer string for comparison
        plain = str(int(s))
        df = df[df['strong'] == plain]
    if lemma is not None:
        df = df[df['lemma'] == lemma]
    if role is not None:
        df = df[df['role'] == role]
    if class_ is not None:
        df = df[df['class_'] == class_]
    if tense is not None:
        df = df[df['tense'] == tense]
    if voice is not None:
        df = df[df['voice'] == voice]
    if mood is not None:
        df = df[df['mood'] == mood]
    if case_ is not None:
        df = df[df['case_'] == case_]
    if has_subjref is True:
        df = df[df['subjref'].notna()]
    if has_subjref is False:
        df = df[df['subjref'].isna()]
    if has_referent is True:
        df = df[df['referent'].notna()]
    if has_referent is False:
        df = df[df['referent'].isna()]

    return df


def speech_verbs(
    book: str | None = None,
    *,
    subject_strong: str | int | None = None,
) -> pd.DataFrame:
    """
    Return rows for speech-introducing verbs (λέγω, φημί, etc.).

    If subject_strong is given (e.g. 2424 for Jesus), further restrict to
    verbs whose subjref points to a token with that Strong's number.

    Returns a DataFrame with one row per speech-introducing verb token,
    with an added 'speaker_strong' column.
    """
    df = load_syntax()
    mask = df['strong'].isin(SPEECH_VERB_STRONGS)
    if book is not None:
        mask &= df['book'] == book
    sv = df[mask].copy()

    if subject_strong is not None:
        s = str(subject_strong).lstrip('Gg0') or '0'
        plain = str(int(s))
        id_to_strong = df.set_index('xml_id')['strong']
        sv = sv[sv['subjref'].map(lambda x: id_to_strong.get(x, '') == plain
                                  if pd.notna(x) else False)]

    return sv


def referent_chain(xml_id: str) -> pd.DataFrame:
    """
    Return all tokens whose 'referent' field points to xml_id —
    i.e., all tokens in the same co-reference chain.
    """
    df = load_syntax()
    return df[df['referent'] == xml_id]


def clause_roles(book: str | None = None, chapter: int | None = None,
                 verse: int | None = None) -> pd.DataFrame:
    """
    Return the syntactic role of each word in the given scope.
    Useful for building subject-verb-object triples per verse.
    """
    df = query_syntax(book=book, chapter=chapter, verse=verse)
    return df[['book', 'chapter', 'verse', 'word_num',
               'text', 'lemma', 'strong_g', 'role', 'gloss']].copy()


def jesus_speaking_verses(books: list[str] | None = None) -> set[tuple[str, int, int]]:
    """
    Return a set of (book, chapter, verse) tuples where a speech verb
    has Jesus (Strong 2424) as its subject via subjref.

    This is the core of speaker attribution for christological titles.
    """
    df = load_syntax()
    df.set_index('xml_id')['strong'].to_dict()

    gospel_books = {'Mat', 'Mrk', 'Luk', 'Jhn'}
    target_books = set(books) if books else gospel_books

    sv = df[
        df['strong'].isin(SPEECH_VERB_STRONGS) &
        df['book'].isin(target_books) &
        df['subjref'].notna()
    ]

    jesus_ids = set(df[df['strong'] == '2424']['xml_id'])
    jesus_sv = sv[sv['subjref'].isin(jesus_ids)]

    return {
        (row.book, int(row.chapter), int(row.verse))
        for row in jesus_sv.itertuples()
    }
