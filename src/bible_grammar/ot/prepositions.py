"""
Preposition frequency and collocate analysis for Biblical Hebrew.

Data source: MACULA OT syntax data (syntax_ot), which provides clean
pointed lemmas and positional word_num fields for adjacency joins.

Primary functions:
  prep_frequency()        — frequency table of all prepositions
  prep_by_book()          — one preposition's distribution across books
  prep_distribution_table() — side-by-side comparison of major prepositions
  prep_collocates()       — top collocates for a given preposition
  prep_object_types()     — grammatical breakdown of what follows a prep
  compare_preps()         — side-by-side collocate comparison of two preps
  find_governing_prep()   — look backwards from a word position for a governing preposition
  inf_cst_by_prep()       — frequency table of infinitive constructs by governing preposition

Print wrappers:
  print_prep_frequency()
  print_prep_by_book()
  print_prep_distribution()
  print_prep_collocates()
  print_compare_preps()
  print_inf_cst_by_prep()
"""

import pandas as pd
from typing import Optional

from ..core._utils import nfc as _nfc, strip_diacritics as _strip_diacritics, load_ot_data


# Canonical book order
_CANON = [
    'Gen', 'Exo', 'Lev', 'Num', 'Deu',
    'Jos', 'Jdg', 'Rut', '1Sa', '2Sa', '1Ki', '2Ki',
    '1Ch', '2Ch', 'Ezr', 'Neh', 'Est',
    'Job', 'Psa', 'Pro', 'Ecc', 'Sng',
    'Isa', 'Jer', 'Lam', 'Ezk', 'Dan',
    'Hos', 'Jol', 'Amo', 'Oba', 'Jon', 'Mic', 'Nah', 'Hab', 'Zep', 'Hag', 'Zec', 'Mal',
]

BOOK_ORDER = {b: i for i, b in enumerate(_CANON)}

BOOK_GROUPS = {
    'Torah':            ['Gen', 'Exo', 'Lev', 'Num', 'Deu'],
    'Former Prophets':  ['Jos', 'Jdg', 'Rut', '1Sa', '2Sa', '1Ki', '2Ki'],
    'Writings':         ['1Ch', '2Ch', 'Ezr', 'Neh', 'Est', 'Job', 'Psa', 'Pro', 'Ecc', 'Sng', 'Lam'],  # noqa: E501
    'Latter Prophets':  ['Isa', 'Jer', 'Ezk', 'Dan', 'Hos', 'Jol', 'Amo', 'Oba', 'Jon', 'Mic', 'Nah', 'Hab', 'Zep', 'Hag', 'Zec', 'Mal'],  # noqa: E501
}

# Top 7 major prepositions (by OT frequency)
MAJOR_PREPS = ['לְ', 'בְּ', 'מִן', 'עַל', 'אֶל', 'כְּ', 'עַד']

# Human-readable gloss for common prepositions
PREP_GLOSS = {
    'לְ':     'lamed — to/for',
    'בְּ':    'bet — in/with',
    'מִן':    'min — from',
    'עַל':    'al — on/upon',
    'אֶל':    'el — to/toward',
    'כְּ':    'kaf — as/like',
    'עַד':    'ad — until/as far as',
    'עִם':    'im — with',
    'אֵת':    'et — with (accompaniment)',
    'אַחַר':  'achar — after',
    'תַּחַת': 'tachat — under/instead of',
    'בֵּין':  'beyn — between',
    'נֶגֶד':  'neged — before/opposite',
    'לְמַעַן': "lema'an — for the sake of",
    'בַּעַד':  "ba'ad — behind/through/for",
}


def _df() -> pd.DataFrame:
    return load_ot_data()


def _preps(book: Optional[str] = None,
           book_group: Optional[str] = None) -> pd.DataFrame:
    """Return prep-only slice, optionally filtered by book or group."""
    df = _df()
    mask = df['class_'] == 'prep'
    if book is not None:
        mask &= df['book'] == book
    if book_group is not None:
        books = BOOK_GROUPS.get(book_group, [])
        mask &= df['book'].isin(books)
    return df[mask].copy()


# ---------------------------------------------------------------------------
# Frequency tables
# ---------------------------------------------------------------------------

def prep_frequency(
    book: Optional[str] = None,
    book_group: Optional[str] = None,
    top_n: int = 20,
) -> pd.DataFrame:
    """
    Frequency table of all prepositions by lemma.

    Parameters
    ----------
    book : str, optional
        Single OT book abbreviation (e.g. 'Gen').
    book_group : str, optional
        One of 'Torah', 'Former Prophets', 'Writings', 'Latter Prophets'.
    top_n : int
        Number of rows to return (most frequent first).

    Returns
    -------
    DataFrame with columns: lemma, gloss, count, pct
    """
    preps = _preps(book=book, book_group=book_group)
    counts = preps['lemma'].value_counts().reset_index()
    counts.columns = ['lemma', 'count']
    counts['pct'] = (counts['count'] / counts['count'].sum() * 100).round(1)
    counts['gloss'] = counts['lemma'].map(PREP_GLOSS).fillna('')
    counts = counts[['lemma', 'gloss', 'count', 'pct']]
    return counts.head(top_n).reset_index(drop=True)


def prep_by_book(lemma: str) -> pd.DataFrame:
    """
    Distribution of a single preposition across all OT books.

    Parameters
    ----------
    lemma : str
        Pointed Hebrew lemma, e.g. 'לְ'.

    Returns
    -------
    DataFrame with columns: book, count, pct_of_lemma
    """
    lemma = _nfc(lemma)
    preps = _preps()
    subset = preps[preps['lemma'] == lemma]
    counts = subset['book'].value_counts().reset_index()
    counts.columns = ['book', 'count']
    counts['pct_of_lemma'] = (counts['count'] / counts['count'].sum() * 100).round(1)
    counts['book_order'] = counts['book'].map(BOOK_ORDER).fillna(99)
    counts = counts.sort_values('book_order').drop(columns='book_order')
    return counts.reset_index(drop=True)


def prep_distribution_table(
    lemmas: Optional[list[str]] = None,
) -> pd.DataFrame:
    """
    Side-by-side comparison of major prepositions by book group.

    Parameters
    ----------
    lemmas : list[str], optional
        Which prepositions to include. Defaults to MAJOR_PREPS (top 7).

    Returns
    -------
    DataFrame indexed by book group with one column per preposition.
    Includes a 'Total' row.
    """
    if lemmas is None:
        lemmas = MAJOR_PREPS
    preps = _preps()
    group_map = {}
    for g, books in BOOK_GROUPS.items():
        for b in books:
            group_map[b] = g

    preps_filtered = preps[preps['lemma'].isin(lemmas)].copy()
    preps_filtered['group'] = preps_filtered['book'].map(group_map).fillna('Other')

    pivot = (
        preps_filtered
        .groupby(['group', 'lemma'])
        .size()
        .unstack(fill_value=0)
    )
    # Ensure all requested lemmas appear even if count is zero
    for lem in lemmas:
        if lem not in pivot.columns:
            pivot[lem] = 0
    pivot = pivot[lemmas]

    group_order = ['Torah', 'Former Prophets', 'Writings', 'Latter Prophets']
    pivot = pivot.reindex([g for g in group_order if g in pivot.index])
    pivot.loc['Total'] = pivot.sum()
    return pivot


# ---------------------------------------------------------------------------
# Collocate analysis
# ---------------------------------------------------------------------------

def prep_collocates(
    lemma: str,
    pos: Optional[str] = None,
    top_n: int = 20,
    book: Optional[str] = None,
    book_group: Optional[str] = None,
) -> pd.DataFrame:
    """
    Top words immediately following a preposition (direct object / NN head).

    Uses word_num + 1 adjacency within the same verse. Skips conjunctions,
    particles, and other prepositions in the result unless pos is set.

    Parameters
    ----------
    lemma : str
        Pointed Hebrew lemma of the preposition, e.g. 'לְ'.
    pos : str, optional
        Filter the following word by part-of-speech substring, e.g. 'noun'.
    top_n : int
        Number of collocates to return.
    book : str, optional
    book_group : str, optional

    Returns
    -------
    DataFrame with columns: collocate, pos, gloss, count
    """
    lemma = _nfc(lemma)
    df = _df()
    preps = _preps(book=book, book_group=book_group)
    prep_subset = preps[preps['lemma'] == lemma][
        ['book', 'chapter', 'verse', 'word_num']
    ].copy()
    prep_subset['next_word_num'] = prep_subset['word_num'] + 1

    # Apply book filter to all-words table too
    all_words = df.copy()
    if book is not None:
        all_words = all_words[all_words['book'] == book]
    if book_group is not None:
        books = BOOK_GROUPS.get(book_group, [])
        all_words = all_words[all_words['book'].isin(books)]

    merged = prep_subset.merge(
        all_words[['book', 'chapter', 'verse', 'word_num', 'lemma', 'pos', 'gloss']],
        left_on=['book', 'chapter', 'verse', 'next_word_num'],
        right_on=['book', 'chapter', 'verse', 'word_num'],
        how='left',
    )

    # Optionally filter by POS of following word
    if pos is not None:
        merged = merged[merged['pos'].str.contains(pos, case=False, na=False)]

    counts = (
        merged.groupby(['lemma', 'pos', 'gloss'], dropna=False)
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
    )
    counts = counts.rename(columns={'lemma': 'collocate'})
    return counts.head(top_n).reset_index(drop=True)


def prep_object_types(
    lemma: str,
    book: Optional[str] = None,
    book_group: Optional[str] = None,
) -> pd.DataFrame:
    """
    Breakdown of the grammatical type of the word immediately following a preposition.

    Parameters
    ----------
    lemma : str
        Pointed Hebrew lemma of the preposition, e.g. 'בְּ'.

    Returns
    -------
    DataFrame with columns: pos, count, pct
    """
    lemma = _nfc(lemma)
    df = _df()
    preps = _preps(book=book, book_group=book_group)
    prep_subset = preps[preps['lemma'] == lemma][
        ['book', 'chapter', 'verse', 'word_num']
    ].copy()
    prep_subset['next_word_num'] = prep_subset['word_num'] + 1

    all_words = df.copy()
    if book is not None:
        all_words = all_words[all_words['book'] == book]
    if book_group is not None:
        books = BOOK_GROUPS.get(book_group, [])
        all_words = all_words[all_words['book'].isin(books)]

    merged = prep_subset.merge(
        all_words[['book', 'chapter', 'verse', 'word_num', 'pos']],
        left_on=['book', 'chapter', 'verse', 'next_word_num'],
        right_on=['book', 'chapter', 'verse', 'word_num'],
        how='left',
    )

    counts = merged['pos'].value_counts().reset_index()
    counts.columns = ['pos', 'count']
    counts['pct'] = (counts['count'] / counts['count'].sum() * 100).round(1)
    return counts.reset_index(drop=True)


def compare_preps(
    lemma1: str,
    lemma2: str,
    pos: Optional[str] = None,
    top_n: int = 20,
    book_group: Optional[str] = None,
) -> pd.DataFrame:
    """
    Side-by-side collocate comparison of two prepositions.

    Parameters
    ----------
    lemma1, lemma2 : str
        Pointed Hebrew lemmas, e.g. 'לְ' and 'בְּ'.
    pos : str, optional
        Filter following words by POS substring.
    top_n : int
        Number of top collocates per preposition.
    book_group : str, optional

    Returns
    -------
    DataFrame with columns: collocate, gloss, count_lemma1, count_lemma2
    Sorted by count_lemma1 descending.
    """
    c1 = prep_collocates(lemma1, pos=pos, top_n=top_n, book_group=book_group)[
        ['collocate', 'gloss', 'count']
    ].rename(columns={'count': f'count_{lemma1}', 'gloss': 'gloss'})

    c2 = prep_collocates(lemma2, pos=pos, top_n=top_n, book_group=book_group)[
        ['collocate', 'count']
    ].rename(columns={'count': f'count_{lemma2}'})

    merged = c1.merge(c2, on='collocate', how='outer').fillna(0)
    merged[f'count_{lemma1}'] = merged[f'count_{lemma1}'].astype(int)
    merged[f'count_{lemma2}'] = merged[f'count_{lemma2}'].astype(int)
    merged = merged.sort_values(f'count_{lemma1}', ascending=False)
    return merged.reset_index(drop=True)


# ---------------------------------------------------------------------------
# Infinitive construct / governing preposition helpers
# ---------------------------------------------------------------------------

def find_governing_prep(book_df: pd.DataFrame, pos: int) -> str:
    """
    Look back up to 3 positions from *pos* in *book_df* to find a governing
    preposition.  Stops early if a verb, noun, or adjective is encountered.

    Parameters
    ----------
    book_df : DataFrame
        A reset-indexed slice of the MACULA syntax table for a single book.
    pos : int
        Integer row position of the word whose governing prep is sought.

    Returns
    -------
    str
        Diacritics-stripped lemma of the governing preposition, or '(none)'.
    """
    for back in range(1, 4):
        if pos - back < 0:
            break
        prev = book_df.iloc[pos - back]
        if prev['class_'] == 'prep':
            return _strip_diacritics(str(prev.get('lemma', '')))
        if prev['class_'] in ('verb', 'noun', 'adj'):
            break
    return '(none)'


def inf_cst_by_prep(book: Optional[str] = None) -> pd.DataFrame:
    """
    Frequency table of infinitive constructs grouped by governing preposition.

    Parameters
    ----------
    book : str, optional
        OT book abbreviation (e.g. 'Gen').  If None, covers the entire OT.

    Returns
    -------
    DataFrame with columns: prep, count, pct
        Sorted by count descending.
    """
    df = _df()
    if book is not None:
        df = df[df['book'] == book].reset_index(drop=True)
    else:
        df = df.reset_index(drop=True)

    inf_rows = df[df['type_'] == 'infinitive construct']
    counts: dict[str, int] = {}
    for _, row in inf_rows.iterrows():
        pos = df.index.get_loc(row.name)
        prep = find_governing_prep(df, pos)
        counts[prep] = counts.get(prep, 0) + 1

    total = sum(counts.values()) or 1
    result = pd.DataFrame(
        [{'prep': p, 'count': c, 'pct': round(c / total * 100, 1)}
         for p, c in sorted(counts.items(), key=lambda x: -x[1])]
    )
    return result.reset_index(drop=True)


# ---------------------------------------------------------------------------
# Print helpers
# ---------------------------------------------------------------------------

def print_prep_frequency(
    book: Optional[str] = None,
    book_group: Optional[str] = None,
    top_n: int = 20,
) -> None:
    scope = book or book_group or 'OT-wide'
    print(f'\n=== Preposition Frequency ({scope}) ===')
    df = prep_frequency(book=book, book_group=book_group, top_n=top_n)
    print(df.to_string(index=False))


def print_prep_by_book(lemma: str) -> None:
    gloss = PREP_GLOSS.get(lemma, lemma)
    print(f'\n=== {lemma} ({gloss}) — Distribution by Book ===')
    df = prep_by_book(lemma)
    print(df.to_string(index=False))


def print_prep_distribution(lemmas: Optional[list[str]] = None) -> None:
    print('\n=== Major Preposition Distribution by Book Group ===')
    df = prep_distribution_table(lemmas=lemmas)
    print(df.to_string())


def print_prep_collocates(
    lemma: str,
    pos: Optional[str] = None,
    top_n: int = 20,
    book: Optional[str] = None,
    book_group: Optional[str] = None,
) -> None:
    gloss = PREP_GLOSS.get(lemma, lemma)
    scope = book or book_group or 'OT-wide'
    pos_note = f', pos={pos!r}' if pos else ''
    print(f'\n=== Top collocates of {lemma} ({gloss}){pos_note} [{scope}] ===')
    df = prep_collocates(lemma, pos=pos, top_n=top_n, book=book, book_group=book_group)
    print(df.to_string(index=False))


def print_compare_preps(
    lemma1: str,
    lemma2: str,
    pos: Optional[str] = None,
    top_n: int = 20,
    book_group: Optional[str] = None,
) -> None:
    g1 = PREP_GLOSS.get(lemma1, lemma1)
    g2 = PREP_GLOSS.get(lemma2, lemma2)
    print(f'\n=== Collocate comparison: {lemma1} ({g1}) vs. {lemma2} ({g2}) ===')
    df = compare_preps(lemma1, lemma2, pos=pos, top_n=top_n, book_group=book_group)
    print(df.to_string(index=False))


def print_inf_cst_by_prep(book: Optional[str] = None) -> None:
    scope = book or 'OT-wide'
    print(f'\n=== Infinitive Construct by Governing Preposition ({scope}) ===')
    df = inf_cst_by_prep(book=book)
    print(df.to_string(index=False))
