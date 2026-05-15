"""
LXX (Septuagint) query module.

Wraps the CenterBLC/LXX Rahlfs 1935 data already loaded into
data/processed/lxx.parquet by lxx.py. Provides the same query API
style as query.py and syntax.py — a filtered DataFrame + convenience
helpers.

Columns in the parquet:
  source, book_id, lxx_book, chapter, verse, word_num,
  word, lemma, lemma_translit, transliteration, translation, strongs,
  morph_code, language, part_of_speech, tense, voice, mood, case_,
  number, gender, person, is_deuterocanon,
  stem, conjugation, state, noun_type, prefixes

Public API
──────────
load_lxx_data()       → full DataFrame (Parquet-cached)
query_lxx(...)        → filtered DataFrame
lxx_freq_table(...)   → frequency table of any column
lxx_concordance(...)  → concordance rows for a Strong's number
lxx_verb_stats(...)   → tense/voice/mood breakdown for a lemma or Strong's
print_lxx_query(...)  → formatted terminal summary
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd

_PARQUET = Path('data/processed/lxx.parquet')

# Canonical OT book order (matches reference.py)
LXX_BOOK_ORDER = [
    'Gen', 'Exo', 'Lev', 'Num', 'Deu', 'Jos', 'Jdg', 'Rut',
    '1Sa', '2Sa', '1Ki', '2Ki', '1Ch', '2Ch', 'Ezr', 'Neh',
    'Est', 'Job', 'Psa', 'Pro', 'Ecc', 'Sng', 'Isa', 'Jer',
    'Lam', 'Ezk', 'Dan', 'Hos', 'Jol', 'Amo', 'Oba', 'Jon',
    'Mic', 'Nah', 'Hab', 'Zep', 'Hag', 'Zec', 'Mal',
]

_BOOK_GROUP: dict[str, list[str]] = {
    'torah':     ['Gen', 'Exo', 'Lev', 'Num', 'Deu'],
    'historical': ['Jos', 'Jdg', 'Rut', '1Sa', '2Sa', '1Ki', '2Ki', '1Ch', '2Ch', 'Ezr', 'Neh', 'Est'],  # noqa: E501
    'wisdom':    ['Job', 'Psa', 'Pro', 'Ecc', 'Sng'],
    'prophets':  ['Isa', 'Jer', 'Lam', 'Ezk', 'Dan', 'Hos', 'Jol', 'Amo', 'Oba', 'Jon',
                  'Mic', 'Nah', 'Hab', 'Zep', 'Hag', 'Zec', 'Mal'],
}

_df_cache: pd.DataFrame | None = None


def load_lxx_data(force_rebuild: bool = False) -> pd.DataFrame:
    """Return the full LXX DataFrame from Parquet cache."""
    global _df_cache
    if _df_cache is not None and not force_rebuild:
        return _df_cache
    if not _PARQUET.exists():
        raise FileNotFoundError(
            f"{_PARQUET} not found. Run:\n"
            "  from bible_grammar.core.lxx import load_lxx\n"
            "  df = load_lxx()\n"
            "  df.to_parquet('data/processed/lxx.parquet', index=False)\n"
            "Or install TextFabric:  pip install 'text-fabric[github]'"
        )
    _df_cache = pd.read_parquet(_PARQUET)
    return _df_cache


def query_lxx(
    *,
    book: str | list[str] | None = None,
    book_group: str | None = None,
    chapter: int | None = None,
    verse: int | None = None,
    strongs: str | list[str] | None = None,
    lemma: str | None = None,
    part_of_speech: str | None = None,
    tense: str | None = None,
    voice: str | None = None,
    mood: str | None = None,
    case_: str | None = None,
    person: str | None = None,
    number: str | None = None,
    gender: str | None = None,
    include_deuterocanon: bool = False,
) -> pd.DataFrame:
    """
    Filtered query over the LXX corpus.

    Parameters
    ----------
    book            : book_id or list of book_ids  (e.g. 'Gen', ['Isa','Jer'])
    book_group      : 'torah'|'historical'|'wisdom'|'prophets'
    chapter         : chapter number
    verse           : verse number
    strongs         : Strong's G-number(s), e.g. 'G2316' or ['G2316','G2962']
    lemma           : Greek lemma string
    part_of_speech  : 'Verb'|'Noun'|'Adjective'|…
    tense           : 'Aorist'|'Present'|'Perfect'|'Imperfect'|'Future'|'Pluperfect'
    voice           : 'Active'|'Middle'|'Passive'
    mood            : 'Indicative'|'Subjunctive'|'Imperative'|'Infinitive'|'Participle'|'Optative'
    case_           : 'Nominative'|'Genitive'|'Accusative'|'Dative'|'Vocative'
    person          : '1st'|'2nd'|'3rd'
    number          : 'Singular'|'Plural'|'Dual'
    gender          : 'Masculine'|'Feminine'|'Neuter'
    include_deuterocanon : include deuterocanonical / Apocrypha books (default False)
    """
    df = load_lxx_data()

    if not include_deuterocanon:
        df = df[~df['is_deuterocanon']]

    if book_group:
        books = _BOOK_GROUP.get(book_group.lower(), [])
        df = df[df['book_id'].isin(books)]
    elif book is not None:
        if isinstance(book, str):
            book = [book]
        df = df[df['book_id'].isin(book)]

    if chapter is not None:
        df = df[df['chapter'] == chapter]
    if verse is not None:
        df = df[df['verse'] == verse]

    if strongs is not None:
        if isinstance(strongs, str):
            strongs = [strongs]
        # Normalise to the format used in the parquet: 'G' + unpadded int (e.g. 'G25', 'G1515')
        normed = []
        for s in strongs:
            s = s.strip().upper()
            if not s.startswith('G'):
                s = 'G' + s
            try:
                normed.append(f"G{int(s[1:])}")
            except ValueError:
                normed.append(s)
        df = df[df['strongs'].isin(normed)]

    if lemma is not None:
        df = df[df['lemma'] == lemma]
    if part_of_speech is not None:
        df = df[df['part_of_speech'].str.lower() == part_of_speech.lower()]
    if tense is not None:
        df = df[df['tense'].str.lower() == tense.lower()]
    if voice is not None:
        df = df[df['voice'].str.lower() == voice.lower()]
    if mood is not None:
        df = df[df['mood'].str.lower() == mood.lower()]
    if case_ is not None:
        df = df[df['case_'].str.lower() == case_.lower()]
    if person is not None:
        df = df[df['person'] == person]
    if number is not None:
        df = df[df['number'].str.lower() == number.lower()]
    if gender is not None:
        df = df[df['gender'].str.lower() == gender.lower()]

    return df.reset_index(drop=True)


def lxx_freq_table(
    group_by: str | list[str],
    *,
    book: str | list[str] | None = None,
    book_group: str | None = None,
    part_of_speech: str | None = None,
    include_deuterocanon: bool = False,
    top_n: int | None = None,
) -> pd.DataFrame:
    """
    Frequency table over the LXX grouped by one or more columns.

    Example
    -------
    lxx_freq_table('tense', part_of_speech='Verb', book_group='prophets')
    lxx_freq_table(['book_id', 'part_of_speech'])
    """
    df = query_lxx(book=book, book_group=book_group,
                   part_of_speech=part_of_speech,
                   include_deuterocanon=include_deuterocanon)
    result = (
        df.groupby(group_by)
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
    )
    if top_n:
        result = result.head(top_n)
    return result.reset_index(drop=True)


def lxx_concordance(
    strongs: str,
    *,
    book: str | list[str] | None = None,
    book_group: str | None = None,
    include_deuterocanon: bool = False,
    top_n: int | None = None,
) -> pd.DataFrame:
    """
    Return concordance rows for a Strong's number — one row per occurrence,
    with book, chapter, verse, word form, lemma, gloss, and morphology.
    """
    df = query_lxx(strongs=strongs, book=book, book_group=book_group,
                   include_deuterocanon=include_deuterocanon)
    cols = ['book_id', 'chapter', 'verse', 'word', 'lemma', 'translation',
            'part_of_speech', 'tense', 'voice', 'mood', 'case_']
    cols = [c for c in cols if c in df.columns]
    result = df[cols].copy()
    if top_n:
        result = result.head(top_n)
    return result.reset_index(drop=True)


def lxx_verb_stats(
    strongs: str | None = None,
    lemma: str | None = None,
    *,
    book: str | list[str] | None = None,
    book_group: str | None = None,
    include_deuterocanon: bool = False,
) -> pd.DataFrame:
    """
    Tense × Voice × Mood breakdown for a LXX verb lemma or Strong's number.
    """
    if strongs is None and lemma is None:
        raise ValueError("Provide strongs or lemma")
    df = query_lxx(strongs=strongs, lemma=lemma, part_of_speech='Verb',
                   book=book, book_group=book_group,
                   include_deuterocanon=include_deuterocanon)
    result = (
        df.groupby(['tense', 'voice', 'mood'])
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
    )
    return result.reset_index(drop=True)


def lxx_by_book(
    strongs: str | None = None,
    lemma: str | None = None,
    *,
    include_deuterocanon: bool = False,
) -> pd.DataFrame:
    """
    Per-book occurrence count for a Strong's number or lemma.
    Books are in canonical OT order.
    """
    df = query_lxx(strongs=strongs, lemma=lemma,
                   include_deuterocanon=include_deuterocanon)
    counts = df.groupby('book_id').size().reset_index(name='count')
    # Sort by canonical order
    order = {b: i for i, b in enumerate(LXX_BOOK_ORDER)}
    counts['_ord'] = counts['book_id'].map(lambda b: order.get(b, 999))
    return counts.sort_values('_ord').drop(columns='_ord').reset_index(drop=True)


def print_lxx_query(
    strongs: str | None = None,
    lemma: str | None = None,
    *,
    book: str | list[str] | None = None,
    book_group: str | None = None,
    top_n: int = 30,
    include_deuterocanon: bool = False,
) -> None:
    """
    Print a formatted summary for a LXX word: lexical info, total count,
    per-book distribution, and (for verbs) tense/voice/mood breakdown.
    """
    if strongs is None and lemma is None:
        print("  Provide strongs or lemma.")
        return

    df = query_lxx(strongs=strongs, lemma=lemma, book=book,
                   book_group=book_group,
                   include_deuterocanon=include_deuterocanon)

    if df.empty:
        print(f"  No results for strongs={strongs!r} lemma={lemma!r}")
        return

    sample = df.iloc[0]
    display_id = strongs or lemma
    w = 72
    print(f"\n{'═'*w}")
    print(f"  LXX: {display_id}  ({sample.get('lemma', '')})  "
          f"[{sample.get('translation', '')}]")
    print(f"  Total occurrences: {len(df):,}  "
          f"(canonical OT only: {len(df[~df['is_deuterocanon']]):,})")
    print(f"{'═'*w}")

    # By-book
    by_book = df.groupby('book_id').size().reset_index(name='count')
    order = {b: i for i, b in enumerate(LXX_BOOK_ORDER)}
    by_book['_ord'] = by_book['book_id'].map(lambda b: order.get(b, 999))
    by_book = by_book.sort_values('_ord').drop(columns='_ord')
    print(f"\n  {'Book':<8} Count")
    print(f"  {'-'*7} -----")
    for _, r in by_book.iterrows():
        print(f"  {r['book_id']:<8} {r['count']:>5}")

    # Verb breakdown
    verbs = df[df['part_of_speech'] == 'Verb']
    if not verbs.empty:
        print(f"\n  Verb forms ({len(verbs)} tokens):")
        print(f"  {'Tense':<14} {'Voice':<12} {'Mood':<14} Count")
        print(f"  {'-'*13} {'-'*11} {'-'*13} -----")
        breakdown = (verbs.groupby(['tense', 'voice', 'mood'])
                     .size().reset_index(name='count')
                     .sort_values('count', ascending=False)
                     .head(top_n))
        for _, r in breakdown.iterrows():
            print(f"  {str(r['tense']):<14} {str(r['voice']):<12} {str(r['mood']):<14} {r['count']:>5}")  # noqa: E501
    print()
