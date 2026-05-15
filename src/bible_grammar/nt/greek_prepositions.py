"""
Greek preposition frequency, case-binding, and collocate analysis.

Supports both the Greek NT (MACULA Nestle1904 via syntax.py) and the
Septuagint/LXX (CenterBLC via lxx.py).

Case binding is determined by adjacency join: the case_ of the word at
word_num+1 after the preposition. Preposition tokens themselves carry no
case in either source.

Case values are normalized to Title case: Accusative, Genitive, Dative,
Nominative (Nominative is rare and typically signals a set phrase or error).

Primary functions:
  greek_prep_frequency()        — frequency table of all prepositions
  greek_prep_by_book()          — one preposition across all books
  greek_prep_distribution_table() — major preps by book group
  greek_prep_cases()            — case-binding profile for one prep
  greek_prep_collocates()       — top collocates, optionally filtered by case
  compare_greek_preps()         — side-by-side collocate comparison
  nt_lxx_compare()              — case profile comparison: NT vs. LXX

Print wrappers:
  print_greek_prep_frequency()
  print_greek_prep_by_book()
  print_greek_prep_distribution()
  print_greek_prep_cases()
  print_greek_prep_collocates()
  print_compare_greek_preps()
  print_nt_lxx_compare()
"""

import pandas as pd
from typing import Optional, Literal

from ..core._utils import nfc as _nfc


Corpus = Literal['nt', 'lxx', 'both']

# ---------------------------------------------------------------------------
# Canonical book orders and groupings
# ---------------------------------------------------------------------------

_NT_CANON = [
    'Mat', 'Mrk', 'Luk', 'Jhn', 'Act',
    'Rom', '1Co', '2Co', 'Gal', 'Eph', 'Php', 'Col',
    '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm',
    'Heb', 'Jas', '1Pe', '2Pe', '1Jn', '2Jn', '3Jn', 'Jud', 'Rev',
]

_LXX_CANON = [
    'Gen', 'Exo', 'Lev', 'Num', 'Deu',
    'Jos', 'Jdg', 'Rut', '1Sa', '2Sa', '1Ki', '2Ki',
    '1Ch', '2Ch', 'Ezr', 'Neh', 'Est',
    'Job', 'Psa', 'Pro', 'Ecc', 'Sng',
    'Isa', 'Jer', 'Lam', 'Ezk', 'Dan',
    'Hos', 'Jol', 'Amo', 'Oba', 'Jon', 'Mic', 'Nah', 'Hab', 'Zep', 'Hag', 'Zec', 'Mal',
    # Deuterocanon
    'Tob', 'Jdt', '1Ma', '2Ma', 'Wis', 'Sir', 'Bar',
]

NT_BOOK_ORDER = {b: i for i, b in enumerate(_NT_CANON)}
LXX_BOOK_ORDER = {b: i for i, b in enumerate(_LXX_CANON)}

NT_BOOK_GROUPS = {
    'Gospels':          ['Mat', 'Mrk', 'Luk', 'Jhn'],
    'Acts':             ['Act'],
    'Pauline':          ['Rom', '1Co', '2Co', 'Gal', 'Eph', 'Php', 'Col',
                         '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm'],
    'General Epistles': ['Heb', 'Jas', '1Pe', '2Pe', '1Jn', '2Jn', '3Jn', 'Jud'],
    'Revelation':       ['Rev'],
}

LXX_BOOK_GROUPS = {
    'Torah':          ['Gen', 'Exo', 'Lev', 'Num', 'Deu'],
    'Historical':     ['Jos', 'Jdg', 'Rut', '1Sa', '2Sa', '1Ki', '2Ki',
                       '1Ch', '2Ch', 'Ezr', 'Neh', 'Est'],
    'Wisdom':         ['Job', 'Psa', 'Pro', 'Ecc', 'Sng'],
    'Major Prophets': ['Isa', 'Jer', 'Lam', 'Ezk', 'Dan'],
    'Minor Prophets': ['Hos', 'Jol', 'Amo', 'Oba', 'Jon', 'Mic',
                       'Nah', 'Hab', 'Zep', 'Hag', 'Zec', 'Mal'],
    'Deuterocanon':   ['Tob', 'Jdt', '1Ma', '2Ma', 'Wis', 'Sir', 'Bar'],
}

# Major prepositions by corpus
NT_MAJOR_PREPS = [_nfc(x) for x in
                  ['ἐν', 'εἰς', 'ἐκ', 'ἐπί', 'πρός', 'διά', 'ἀπό', 'κατά', 'μετά', 'περί']]
LXX_MAJOR_PREPS = [_nfc(x) for x in
                   ['ἐν', 'εἰς', 'ἐπί', 'πρός', 'ἀπό', 'ἐκ', 'μετά', 'κατά', 'διά', 'ἕως']]

PREP_GLOSS = {_nfc(k): v for k, v in {
    'ἐν':         'en — in/among',
    'εἰς':        'eis — into/for',
    'ἐκ':         'ek — out of/from',
    'ἐπί':        'epi — on/over/at',
    'πρός':       'pros — to/toward',
    'διά':        'dia — through/because of',
    'ἀπό':        'apo — from/away from',
    'κατά':       'kata — according to/against',
    'μετά':       'meta — with/after',
    'περί':       'peri — concerning/around',
    'ὑπό':        'hypo — by/under',
    'παρά':       'para — beside/from',
    'ὑπέρ':       'hyper — on behalf of/above',
    'σύν':        'syn — with/together',
    'ἕως':        'heos — until/as far as',
    'ἐνώπιον':    'enopion — before/in the presence of',
    'πρό':        'pro — before',
    'ἄχρι':       'achri — until/as far as',
    'ἔμπροσθεν':  'emprosthen — before/in front of',
    'χωρίς':      'choris — apart from/without',
    'ἐνώπιος':    'enopios — before (LXX variant)',
    'ἐναντίον':   'enantion — before/in the sight of',
    'ἐναντίας':   'enantias — against',
    'ἀνά':        'ana — up/each',
}.items()}

CASES = ['Accusative', 'Genitive', 'Dative', 'Nominative']

# ---------------------------------------------------------------------------
# Lazy-loaded DataFrames with case-enriched preposition rows
# ---------------------------------------------------------------------------

_nt_cache:  Optional[pd.DataFrame] = None   # prep tokens with case_binding
_lxx_cache: Optional[pd.DataFrame] = None


def _build_nt() -> pd.DataFrame:
    """NT prep DataFrame enriched with case of following word."""
    from ..core.syntax import load_syntax
    raw = load_syntax()
    df = raw.copy()
    df['lemma'] = df['lemma'].apply(lambda x: _nfc(str(x)) if pd.notna(x) else x)

    preps = df[df['class_'] == 'prep'][
        ['book', 'chapter', 'verse', 'word_num', 'lemma', 'gloss']
    ].copy()
    preps['next_wn'] = preps['word_num'] + 1

    next_words = df[['book', 'chapter', 'verse', 'word_num', 'case_', 'class_', 'lemma']].rename(
        columns={'lemma': 'obj_lemma', 'class_': 'obj_class', 'case_': 'raw_case'}
    )

    merged = preps.merge(
        next_words,
        left_on=['book', 'chapter', 'verse', 'next_wn'],
        right_on=['book', 'chapter', 'verse', 'word_num'],
        how='left',
    ).drop(columns=['next_wn', 'word_num_y'], errors='ignore')

    # Normalize to Title case (NT syntax has lowercase)
    merged['case_binding'] = merged['raw_case'].apply(
        lambda x: x.title() if isinstance(x, str) and x else None
    )
    merged['corpus'] = 'NT'
    merged = merged.rename(columns={'word_num_x': 'word_num'})
    return merged


def _build_lxx() -> pd.DataFrame:
    """LXX prep DataFrame enriched with case of following word."""
    from ..core.lxx import load_lxx
    raw = load_lxx()
    df = raw.copy()
    df['lemma'] = df['lemma'].apply(lambda x: _nfc(str(x)) if pd.notna(x) else x)

    preps = df[df['part_of_speech'].str.contains('Prep', case=False, na=False)][
        ['book_id', 'chapter', 'verse', 'word_num', 'lemma']
    ].copy().rename(columns={'book_id': 'book'})
    preps['next_wn'] = preps['word_num'] + 1

    next_words = df[['book_id', 'chapter', 'verse', 'word_num', 'case_', 'part_of_speech', 'lemma']].rename(  # noqa: E501
        columns={'book_id': 'book', 'lemma': 'obj_lemma',
                 'part_of_speech': 'obj_class', 'case_': 'raw_case'}
    )

    merged = preps.merge(
        next_words,
        left_on=['book', 'chapter', 'verse', 'next_wn'],
        right_on=['book', 'chapter', 'verse', 'word_num'],
        how='left',
    ).drop(columns=['next_wn', 'word_num_y'], errors='ignore')

    # LXX case values already Title case; normalize empties to None
    merged['case_binding'] = merged['raw_case'].apply(
        lambda x: x.title() if isinstance(x, str) and x.strip() else None
    )
    merged['corpus'] = 'LXX'
    merged = merged.rename(columns={'word_num_x': 'word_num'})
    return merged


def _nt_df() -> pd.DataFrame:
    global _nt_cache
    if _nt_cache is None:
        _nt_cache = _build_nt()
    return _nt_cache


def _lxx_df() -> pd.DataFrame:
    global _lxx_cache
    if _lxx_cache is None:
        _lxx_cache = _build_lxx()
    return _lxx_cache


def _get_df(corpus: Corpus) -> pd.DataFrame:
    if corpus == 'nt':
        return _nt_df()
    if corpus == 'lxx':
        return _lxx_df()
    return pd.concat([_nt_df(), _lxx_df()], ignore_index=True)


def _book_order(corpus: Corpus) -> dict:
    if corpus == 'nt':
        return NT_BOOK_ORDER
    if corpus == 'lxx':
        return LXX_BOOK_ORDER
    merged = {**LXX_BOOK_ORDER, **{k: v + len(LXX_BOOK_ORDER) for k, v in NT_BOOK_ORDER.items()}}
    return merged


def _book_groups(corpus: Corpus) -> dict:
    if corpus == 'nt':
        return NT_BOOK_GROUPS
    if corpus == 'lxx':
        return LXX_BOOK_GROUPS
    return {**LXX_BOOK_GROUPS, **NT_BOOK_GROUPS}


def _major_preps(corpus: Corpus) -> list[str]:
    if corpus == 'lxx':
        return LXX_MAJOR_PREPS
    return NT_MAJOR_PREPS


def _filter(df: pd.DataFrame, book: Optional[str], book_group: Optional[str],
            corpus: Corpus) -> pd.DataFrame:
    if book:
        df = df[df['book'] == book]
    if book_group:
        books = _book_groups(corpus).get(book_group, [])
        df = df[df['book'].isin(books)]
    return df


# ---------------------------------------------------------------------------
# Analysis functions
# ---------------------------------------------------------------------------

def greek_prep_frequency(
    corpus: Corpus = 'nt',
    book: Optional[str] = None,
    book_group: Optional[str] = None,
    top_n: int = 20,
) -> pd.DataFrame:
    """
    Frequency table of Greek prepositions.

    Parameters
    ----------
    corpus : 'nt', 'lxx', or 'both'
    book   : e.g. 'Mat', 'Gen'
    book_group : e.g. 'Gospels', 'Torah'
    top_n  : rows to return

    Returns
    -------
    DataFrame: lemma, gloss, count, pct
    """
    df = _filter(_get_df(corpus), book, book_group, corpus)
    counts = df['lemma'].value_counts().reset_index()
    counts.columns = ['lemma', 'count']
    counts['pct'] = (counts['count'] / counts['count'].sum() * 100).round(1)
    counts['gloss'] = counts['lemma'].map(PREP_GLOSS).fillna('')
    return counts[['lemma', 'gloss', 'count', 'pct']].head(top_n).reset_index(drop=True)


def greek_prep_by_book(
    lemma: str,
    corpus: Corpus = 'nt',
) -> pd.DataFrame:
    """
    Distribution of a single preposition across all books in the corpus.

    Returns
    -------
    DataFrame: book, count, pct_of_lemma  (canonical book order)
    """
    lemma = _nfc(lemma)
    df = _get_df(corpus)
    subset = df[df['lemma'] == lemma]
    counts = subset['book'].value_counts().reset_index()
    counts.columns = ['book', 'count']
    counts['pct_of_lemma'] = (counts['count'] / counts['count'].sum() * 100).round(1)
    order = _book_order(corpus)
    counts['sort_key'] = counts['book'].map(order).fillna(999)
    return counts.sort_values('sort_key').drop(columns='sort_key').reset_index(drop=True)


def greek_prep_distribution_table(
    corpus: Corpus = 'nt',
    lemmas: Optional[list[str]] = None,
) -> pd.DataFrame:
    """
    Side-by-side count of major prepositions by book group.

    Returns
    -------
    DataFrame indexed by book group, one column per preposition.
    Includes a 'Total' row.
    """
    if lemmas is None:
        lemmas = _major_preps(corpus)

    df = _get_df(corpus)
    groups = _book_groups(corpus)
    group_map = {b: g for g, books in groups.items() for b in books}

    subset = df[df['lemma'].isin(lemmas)].copy()
    subset['group'] = subset['book'].map(group_map).fillna('Other')

    pivot = subset.groupby(['group', 'lemma']).size().unstack(fill_value=0)
    for lem in lemmas:
        if lem not in pivot.columns:
            pivot[lem] = 0
    pivot = pivot[lemmas]

    group_order = list(groups.keys())
    pivot = pivot.reindex([g for g in group_order if g in pivot.index])
    pivot.loc['Total'] = pivot.sum()
    return pivot


def greek_prep_cases(
    lemma: str,
    corpus: Corpus = 'nt',
    book: Optional[str] = None,
    book_group: Optional[str] = None,
) -> pd.DataFrame:
    """
    Case-binding profile for a single preposition.

    Returns
    -------
    DataFrame: case_binding, count, pct
    """
    lemma = _nfc(lemma)
    df = _filter(_get_df(corpus), book, book_group, corpus)
    subset = df[df['lemma'] == lemma]
    counts = subset['case_binding'].value_counts(dropna=False).reset_index()
    counts.columns = ['case_binding', 'count']
    counts['case_binding'] = counts['case_binding'].fillna('(none / unclear)')
    counts['pct'] = (counts['count'] / counts['count'].sum() * 100).round(1)
    return counts.reset_index(drop=True)


def greek_prep_collocates(
    lemma: str,
    corpus: Corpus = 'nt',
    case: Optional[str] = None,
    obj_pos: Optional[str] = None,
    top_n: int = 20,
    book: Optional[str] = None,
    book_group: Optional[str] = None,
) -> pd.DataFrame:
    """
    Top words immediately following the preposition.

    Parameters
    ----------
    lemma     : Greek prep lemma, e.g. 'ἐν'
    corpus    : 'nt', 'lxx', or 'both'
    case      : filter by case binding, e.g. 'Dative', 'Accusative', 'Genitive'
    obj_pos   : filter the following word by POS substring, e.g. 'noun'
    top_n     : rows to return
    book / book_group : scope

    Returns
    -------
    DataFrame: collocate, obj_class, count
    """
    lemma = _nfc(lemma)
    df = _filter(_get_df(corpus), book, book_group, corpus)
    subset = df[df['lemma'] == lemma].copy()

    if case:
        subset = subset[subset['case_binding'].str.lower() == case.lower()]

    if obj_pos:
        subset = subset[subset['obj_class'].str.contains(obj_pos, case=False, na=False)]

    counts = (
        subset.groupby(['obj_lemma', 'obj_class', 'case_binding'], dropna=False)
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
    )
    counts = counts.rename(columns={'obj_lemma': 'collocate'})
    return counts.head(top_n).reset_index(drop=True)


def compare_greek_preps(
    lemma1: str,
    lemma2: str,
    corpus: Corpus = 'nt',
    case: Optional[str] = None,
    top_n: int = 20,
    book_group: Optional[str] = None,
) -> pd.DataFrame:
    """
    Side-by-side collocate comparison of two prepositions.

    Returns
    -------
    DataFrame: collocate, count_<lemma1>, count_<lemma2>  (sorted by lemma1)
    """
    c1 = greek_prep_collocates(lemma1, corpus=corpus, case=case, top_n=top_n,
                               book_group=book_group)[['collocate', 'count']].rename(
        columns={'count': f'count_{lemma1}'})
    c2 = greek_prep_collocates(lemma2, corpus=corpus, case=case, top_n=top_n,
                               book_group=book_group)[['collocate', 'count']].rename(
        columns={'count': f'count_{lemma2}'})

    merged = c1.merge(c2, on='collocate', how='outer').fillna(0)
    merged[f'count_{lemma1}'] = merged[f'count_{lemma1}'].astype(int)
    merged[f'count_{lemma2}'] = merged[f'count_{lemma2}'].astype(int)
    return merged.sort_values(f'count_{lemma1}', ascending=False).reset_index(drop=True)


def nt_lxx_compare(lemma: str) -> pd.DataFrame:
    """
    Compare the case-binding profile of a preposition between NT and LXX.

    Returns
    -------
    DataFrame: case_binding, count_nt, pct_nt, count_lxx, pct_lxx
    """
    nt = greek_prep_cases(lemma, corpus='nt').rename(
        columns={'count': 'count_nt', 'pct': 'pct_nt'})
    lxx = greek_prep_cases(lemma, corpus='lxx').rename(
        columns={'count': 'count_lxx', 'pct': 'pct_lxx'})
    merged = nt.merge(lxx, on='case_binding', how='outer').fillna(0)
    merged['count_nt'] = merged['count_nt'].astype(int)
    merged['count_lxx'] = merged['count_lxx'].astype(int)
    return merged.sort_values('count_nt', ascending=False).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Print helpers
# ---------------------------------------------------------------------------

def print_greek_prep_frequency(
    corpus: Corpus = 'nt',
    book: Optional[str] = None,
    book_group: Optional[str] = None,
    top_n: int = 20,
) -> None:
    scope = book or book_group or corpus.upper()
    print(f'\n=== Greek Preposition Frequency ({scope}) ===')
    print(greek_prep_frequency(corpus=corpus, book=book,
          book_group=book_group, top_n=top_n).to_string(index=False))


def print_greek_prep_by_book(lemma: str, corpus: Corpus = 'nt') -> None:
    gloss = PREP_GLOSS.get(lemma, lemma)
    print(f'\n=== {lemma} ({gloss}) — Distribution by Book [{corpus.upper()}] ===')
    print(greek_prep_by_book(lemma, corpus=corpus).to_string(index=False))


def print_greek_prep_distribution(corpus: Corpus = 'nt', lemmas: Optional[list[str]] = None) -> None:  # noqa: E501
    print(f'\n=== Major Preposition Distribution by Book Group [{corpus.upper()}] ===')
    print(greek_prep_distribution_table(corpus=corpus, lemmas=lemmas).to_string())


def print_greek_prep_cases(
    lemma: str,
    corpus: Corpus = 'nt',
    book: Optional[str] = None,
    book_group: Optional[str] = None,
) -> None:
    gloss = PREP_GLOSS.get(lemma, lemma)
    scope = book or book_group or corpus.upper()
    print(f'\n=== Case bindings of {lemma} ({gloss}) [{scope}] ===')
    print(greek_prep_cases(lemma, corpus=corpus, book=book,
          book_group=book_group).to_string(index=False))


def print_greek_prep_collocates(
    lemma: str,
    corpus: Corpus = 'nt',
    case: Optional[str] = None,
    obj_pos: Optional[str] = None,
    top_n: int = 20,
    book: Optional[str] = None,
    book_group: Optional[str] = None,
) -> None:
    gloss = PREP_GLOSS.get(lemma, lemma)
    scope = book or book_group or corpus.upper()
    case_note = f', case={case}' if case else ''
    pos_note = f', pos={obj_pos!r}' if obj_pos else ''
    print(f'\n=== Collocates of {lemma} ({gloss}){case_note}{pos_note} [{scope}] ===')
    print(greek_prep_collocates(lemma, corpus=corpus, case=case, obj_pos=obj_pos,
                                top_n=top_n, book=book, book_group=book_group).to_string(index=False))  # noqa: E501


def print_compare_greek_preps(
    lemma1: str,
    lemma2: str,
    corpus: Corpus = 'nt',
    case: Optional[str] = None,
    top_n: int = 20,
    book_group: Optional[str] = None,
) -> None:
    g1 = PREP_GLOSS.get(lemma1, lemma1)
    g2 = PREP_GLOSS.get(lemma2, lemma2)
    print(f'\n=== Collocate comparison: {lemma1} ({g1}) vs. {lemma2} ({g2}) [{corpus.upper()}] ===')
    print(compare_greek_preps(lemma1, lemma2, corpus=corpus, case=case,
                              top_n=top_n, book_group=book_group).to_string(index=False))


def print_nt_lxx_compare(lemma: str) -> None:
    gloss = PREP_GLOSS.get(lemma, lemma)
    print(f'\n=== NT vs. LXX case-binding comparison: {lemma} ({gloss}) ===')
    print(nt_lxx_compare(lemma).to_string(index=False))
