"""
Formulaic language and fixed phrase detection for the Hebrew OT and Greek NT.

Biblical Hebrew and Greek contain hundreds of fixed expressions — prophetic
formulas, doxological phrases, oath/blessing/curse formulas, epistolary
greetings — that carry specialized theological or rhetorical functions.

This module provides:
  1. N-gram frequency extraction (verse-boundary-safe)
  2. Formula search by lemma sequence with optional '*' wildcard
  3. Curated HEBREW_FORMULAS and GREEK_FORMULAS reference dictionaries
  4. Book/chapter distribution analysis
  5. Whole-corpus formula profile (all curated formulas at once)

Notes on lemma matching
───────────────────────
  All pattern matching uses the MACULA Hebrew/Greek lemma column.
  Inflected forms (e.g. וַיְהִי) are matched via their root lemma (הָיָה).
  The special token '*' in a pattern matches any single lemma.
  Patterns must not cross verse boundaries (formulas are intra-verse).

Questions this answers
──────────────────────
  • How often does כֹּה אָמַר יְהוָה appear, and in which books?
  • Where does ἀμὴν λέγω ὑμῖν cluster in the Gospels?
  • What are the top-30 Hebrew bigrams in the Psalms?
  • Which books use the most prophetic formulas?

Public API
──────────
HEBREW_FORMULAS                              → dict of curated OT formulas
GREEK_FORMULAS                               → dict of curated NT formulas

ot_formula_frequency(n, min_count, book)     → DataFrame (ngram, count)
nt_formula_frequency(n, min_count, book)     → DataFrame (ngram, count)
ot_formula_search(pattern, book)             → DataFrame (ref, context)
nt_formula_search(pattern, book)             → DataFrame (ref, context)
formula_book_distribution(pattern, lang)     → DataFrame (book, count, pct)
ot_formula_profile()                         → DataFrame (all HEBREW_FORMULAS)
nt_formula_profile()                         → DataFrame (all GREEK_FORMULAS)

print_formula_concordance(pattern, lang)     → None
print_formula_book_distribution(pattern, lang) → None
print_ot_formula_profile()                   → None
print_nt_formula_profile()                   → None
print_ot_top_ngrams(n, min_count, top_n)     → None
print_nt_top_ngrams(n, min_count, top_n)     → None

formula_book_chart(pattern, lang)            → Path | None
formula_chapter_chart(book, formula_key, lang) → Path | None
"""

from __future__ import annotations
from collections import Counter
from pathlib import Path

import pandas as pd

from ..core._utils import ensure_chart_dir

_CHART_DIR = Path('output') / 'charts' / 'formulaic'

# ── curated formula registries ────────────────────────────────────────────────

HEBREW_FORMULAS: dict[str, dict] = {
    'ko_amar_yhwh': {
        'pattern': ['כֹּה', 'אָמַר', 'יְהוָה'],
        'gloss': 'Thus says YHWH',
        'transliteration': 'kō ʾāmar YHWH',
        'function': 'prophetic',
    },
    'neum_yhwh': {
        'pattern': ['נְאֻם', 'יְהוָה'],
        'gloss': "Oracle of YHWH",
        'transliteration': "neʾum YHWH",
        'function': 'prophetic',
    },
    'devar_yhwh': {
        'pattern': ['דָּבָר', 'יְהוָה'],
        'gloss': 'Word of YHWH',
        'transliteration': 'dəvar YHWH',
        'function': 'prophetic',
    },
    'wayehi_devar_yhwh': {
        'pattern': ['הָיָה', 'דָּבָר', 'יְהוָה'],
        'gloss': 'The word of YHWH came',
        'transliteration': 'wayhî dəvar YHWH',
        'function': 'prophetic-narrative',
    },
    'karat_berit': {
        'pattern': ['כָּרַת', 'בְּרִית'],
        'gloss': 'Cut a covenant',
        'transliteration': 'kārat bərît',
        'function': 'covenantal',
    },
    'barukh_yhwh': {
        'pattern': ['בָּרוּךְ', 'יְהוָה'],
        'gloss': 'Blessed be YHWH',
        'transliteration': 'bārûk YHWH',
        'function': 'doxological',
    },
    'hallelu_yah': {
        'pattern': ['הָלַל', 'יָהּ'],
        'gloss': 'Praise the LORD (Hallelu-Yah)',
        'transliteration': 'halləlû Yāh',
        'function': 'doxological',
    },
    'arur': {
        'pattern': ['אָרוּר'],
        'gloss': 'Cursed (curse formula)',
        'transliteration': 'ʾārûr',
        'function': 'malediction',
    },
    'tsivah_yhwh': {
        'pattern': ['צָוָה', 'יְהוָה'],
        'gloss': 'YHWH commanded',
        'transliteration': 'ṣiwwāh YHWH',
        'function': 'legal',
    },
    'hayah_yhwh_im': {
        'pattern': ['הָיָה', 'יְהוָה', 'עִם'],
        'gloss': 'YHWH was with (X)',
        'transliteration': 'hāyāh YHWH ʿim',
        'function': 'divine-presence',
    },
}

GREEK_FORMULAS: dict[str, dict] = {
    'amen_lego_hymin': {
        'pattern': ['ἀμήν', 'λέγω', 'σύ'],
        'gloss': 'Truly I say to you',
        'transliteration': 'amēn legō hymin',
        'function': 'dominical',
    },
    'amen_amen_lego_hymin': {
        'pattern': ['ἀμήν', 'ἀμήν', 'λέγω', 'σύ'],
        'gloss': 'Truly truly I say to you (Johannine double amen)',
        'transliteration': 'amēn amēn legō hymin',
        'function': 'dominical',
    },
    'gegraptai': {
        'pattern': ['γράφω'],
        'gloss': 'It is written',
        'transliteration': 'gegraptai',
        'function': 'citation',
        'note': 'lemma match — includes all forms of γράφω',
    },
    'charis_kai_eirene': {
        'pattern': ['χάρις', 'σύ', 'καί', 'εἰρήνη'],
        'gloss': 'Grace and peace to you',
        'transliteration': 'charis hymin kai eirēnē',
        'function': 'epistolary',
    },
    'eirene_hymin': {
        'pattern': ['εἰρήνη', 'σύ'],
        'gloss': 'Peace to you',
        'transliteration': 'eirēnē hymin',
        'function': 'greeting',
    },
    'echon_ota_akoueto': {
        'pattern': ['ἔχω', 'οὖς', 'ἀκούω'],
        'gloss': 'He who has ears, let him hear',
        'transliteration': 'ho echōn ōta akouetō',
        'function': 'dominical',
    },
    'en_arche_en': {
        'pattern': ['ἐν', 'ἀρχή', 'εἰμί'],
        'gloss': 'In the beginning was',
        'transliteration': 'en archē ēn',
        'function': 'prologue',
    },
}

# Canonical OT book order for display
_OT_BOOK_ORDER = [
    'Gen', 'Exo', 'Lev', 'Num', 'Deu', 'Jos', 'Jdg', 'Rut',
    '1Sa', '2Sa', '1Ki', '2Ki', '1Ch', '2Ch', 'Ezr', 'Neh', 'Est',
    'Job', 'Psa', 'Pro', 'Ecc', 'Sol', 'Isa', 'Jer', 'Lam',
    'Eze', 'Dan', 'Hos', 'Joe', 'Amo', 'Oba', 'Jon', 'Mic',
    'Nah', 'Hab', 'Zep', 'Hag', 'Zec', 'Mal',
]
_NT_BOOK_ORDER = [
    'Mat', 'Mrk', 'Luk', 'Jhn', 'Act',
    'Rom', '1Co', '2Co', 'Gal', 'Eph', 'Php', 'Col',
    '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm',
    'Heb', 'Jas', '1Pe', '2Pe', '1Jn', '2Jn', '3Jn', 'Jud', 'Rev',
]


# ── helpers ───────────────────────────────────────────────────────────────────

def _load_ot_h() -> pd.DataFrame:
    from ..core._utils import load_ot_h
    return load_ot_h()


def _load_nt() -> pd.DataFrame:
    from ..core._utils import load_nt
    return load_nt()


def _match_pattern(window: list[str], pattern: list[str]) -> bool:
    if len(window) != len(pattern):
        return False
    return all(p == '*' or w == p for w, p in zip(window, pattern))


def _ngram_search(df: pd.DataFrame, pattern: list[str], context_words: int) -> pd.DataFrame:
    """Core search: find lemma pattern in df grouped by (book, chapter, verse)."""
    n = len(pattern)
    rows = []
    for (bk, ch, vs), grp in df.groupby(['book', 'chapter', 'verse'], sort=False):
        grp = grp.reset_index(drop=True)
        lemmas = grp['lemma'].tolist()
        texts = grp['text'].tolist() if 'text' in grp.columns else lemmas
        ref_val = grp['ref'].iloc[0] if 'ref' in grp.columns else f'{bk} {ch}:{vs}'
        for i in range(len(lemmas) - n + 1):
            if _match_pattern(lemmas[i:i+n], pattern):
                ctx_s = max(0, i - context_words)
                ctx_e = min(len(texts), i + n + context_words)
                rows.append({
                    'ref': ref_val,
                    'book': bk,
                    'chapter': int(ch),
                    'verse': int(vs),
                    'match_text': ' '.join(texts[i:i+n]),
                    'context': ' '.join(texts[ctx_s:ctx_e]),
                })
    if not rows:
        return pd.DataFrame(columns=['ref', 'book', 'chapter', 'verse', 'match_text', 'context'])
    return pd.DataFrame(rows).reset_index(drop=True)


def _ngram_counter(df: pd.DataFrame, n: int) -> Counter:
    """Count verse-boundary-safe n-grams over lemma column."""
    counter: Counter = Counter()
    for _, grp in df.groupby(['book', 'chapter', 'verse'], sort=False):
        lemmas = grp['lemma'].tolist()
        for i in range(len(lemmas) - n + 1):
            counter[tuple(lemmas[i:i+n])] += 1
    return counter


def _parse_pattern(pattern: str | list[str]) -> list[str]:
    if isinstance(pattern, str):
        return pattern.split()
    return list(pattern)


# ── data functions ────────────────────────────────────────────────────────────

def ot_formula_frequency(
    n: int = 2,
    *,
    min_count: int = 5,
    book: str | None = None,
) -> pd.DataFrame:
    """
    Top Hebrew n-gram lemma sequences in the OT (verse-boundary-safe).

    Returns: ngram (space-joined lemmas), count.
    """
    df = _load_ot_h()
    if book:
        df = df[df['book'] == book]
    counter = _ngram_counter(df, n)
    rows = [
        {'ngram': ' '.join(ng), 'count': c}
        for ng, c in counter.most_common()
        if c >= min_count
    ]
    return pd.DataFrame(rows)


def nt_formula_frequency(
    n: int = 2,
    *,
    min_count: int = 5,
    book: str | None = None,
) -> pd.DataFrame:
    """
    Top Greek n-gram lemma sequences in the NT (verse-boundary-safe).

    Returns: ngram (space-joined lemmas), count.
    """
    df = _load_nt()
    if book:
        df = df[df['book'] == book]
    counter = _ngram_counter(df, n)
    rows = [
        {'ngram': ' '.join(ng), 'count': c}
        for ng, c in counter.most_common()
        if c >= min_count
    ]
    return pd.DataFrame(rows)


def ot_formula_search(
    pattern: str | list[str],
    *,
    book: str | list[str] | None = None,
    context_words: int = 3,
) -> pd.DataFrame:
    """
    Search for a lemma sequence in the Hebrew OT.

    pattern : list of lemmas or space-separated string. Use '*' as single-token wildcard.
    Returns: ref, book, chapter, verse, match_text, context.
    """
    pat = _parse_pattern(pattern)
    df = _load_ot_h()
    if book is not None:
        if isinstance(book, str):
            book = [book]
        df = df[df['book'].isin(book)]
    return _ngram_search(df, pat, context_words)


def nt_formula_search(
    pattern: str | list[str],
    *,
    book: str | list[str] | None = None,
    context_words: int = 3,
) -> pd.DataFrame:
    """
    Search for a lemma sequence in the Greek NT.

    pattern : list of lemmas or space-separated string. Use '*' as single-token wildcard.
    Returns: ref, book, chapter, verse, match_text, context.
    """
    pat = _parse_pattern(pattern)
    df = _load_nt()
    if book is not None:
        if isinstance(book, str):
            book = [book]
        df = df[df['book'].isin(book)]
    return _ngram_search(df, pat, context_words)


def formula_book_distribution(
    pattern: str | list[str],
    *,
    lang: str = 'H',
) -> pd.DataFrame:
    """
    Count occurrences of a lemma pattern per book.

    Returns: book, count, pct — ordered canonically.
    """
    pat = _parse_pattern(pattern)
    result = ot_formula_search(pat) if lang == 'H' else nt_formula_search(pat)
    if result.empty:
        return pd.DataFrame(columns=['book', 'count', 'pct'])
    total = len(result)
    counts = result['book'].value_counts().reset_index()
    counts.columns = ['book', 'count']
    counts['pct'] = (counts['count'] / total * 100).round(1)
    book_order = _OT_BOOK_ORDER if lang == 'H' else _NT_BOOK_ORDER
    order_map = {b: i for i, b in enumerate(book_order)}
    counts['_ord'] = counts['book'].map(order_map).fillna(999)
    return counts.sort_values('_ord').drop(columns='_ord').reset_index(drop=True)


def ot_formula_profile() -> pd.DataFrame:
    """
    Run all HEBREW_FORMULAS searches and return counts.

    Returns: key, gloss, function, pattern, count — sorted by count desc.
    """
    rows = []
    for key, meta in HEBREW_FORMULAS.items():
        pat = meta['pattern']
        result = ot_formula_search(pat)
        rows.append({
            'key': key,
            'gloss': meta['gloss'],
            'function': meta['function'],
            'pattern': ' '.join(pat),
            'count': len(result),
        })
    return (
        pd.DataFrame(rows)
        .sort_values('count', ascending=False)
        .reset_index(drop=True)
    )


def nt_formula_profile() -> pd.DataFrame:
    """
    Run all GREEK_FORMULAS searches and return counts.

    Returns: key, gloss, function, pattern, count — sorted by count desc.
    """
    rows = []
    for key, meta in GREEK_FORMULAS.items():
        pat = meta['pattern']
        result = nt_formula_search(pat)
        rows.append({
            'key': key,
            'gloss': meta['gloss'],
            'function': meta['function'],
            'pattern': ' '.join(pat),
            'count': len(result),
        })
    return (
        pd.DataFrame(rows)
        .sort_values('count', ascending=False)
        .reset_index(drop=True)
    )


# ── print functions ───────────────────────────────────────────────────────────

def print_formula_concordance(
    pattern: str | list[str],
    *,
    lang: str = 'H',
    max_rows: int = 30,
) -> None:
    pat = _parse_pattern(pattern)
    result = ot_formula_search(pat) if lang == 'H' else nt_formula_search(pat)
    pat_str = ' '.join(pat)
    w = 70
    print(f"\n{'═'*w}")
    print(f"  Formula: {pat_str}")
    print(f"  {len(result)} occurrence(s)")
    print(f"{'═'*w}")
    if result.empty:
        print("  No results.")
        print()
        return
    print(f"  {'Ref':<20}  Context")
    print('  ' + '-' * 67)
    for _, row in result.head(max_rows).iterrows():
        ctx = row['context'][:55] if len(row['context']) > 55 else row['context']
        print(f"  {str(row['ref']):<20}  {ctx}")
    if len(result) > max_rows:
        print(f"  ... ({len(result) - max_rows} more not shown)")
    print()


def print_formula_book_distribution(
    pattern: str | list[str],
    *,
    lang: str = 'H',
) -> None:
    pat = _parse_pattern(pattern)
    df = formula_book_distribution(pat, lang=lang)
    pat_str = ' '.join(pat)
    print(f"\nBook Distribution — {pat_str}")
    if df.empty:
        print("  No occurrences.")
        print()
        return
    print(f"  {'Book':<6} {'Count':>6} {'%':>6}  Bar")
    print('  ' + '-' * 40)
    for _, row in df.iterrows():
        bar = '█' * min(int(row['pct']), 40)
        print(f"  {row['book']:<6} {row['count']:>6} {row['pct']:>5.1f}%  {bar}")
    print()


def print_ot_formula_profile() -> None:
    df = ot_formula_profile()
    w = 70
    print(f"\n{'═'*w}")
    print("  Hebrew Formula Profile (HEBREW_FORMULAS)")
    print(f"{'═'*w}")
    print(f"  {'Formula (gloss)':<36} {'Function':<22} {'Count':>6}")
    print('  ' + '-' * 67)
    for _, row in df.iterrows():
        gloss = row['gloss'][:34] if len(row['gloss']) > 34 else row['gloss']
        func = row['function'][:20] if len(row['function']) > 20 else row['function']
        print(f"  {gloss:<36} {func:<22} {row['count']:>6,}")
    print()


def print_nt_formula_profile() -> None:
    df = nt_formula_profile()
    w = 70
    print(f"\n{'═'*w}")
    print("  Greek Formula Profile (GREEK_FORMULAS)")
    print(f"{'═'*w}")
    print(f"  {'Formula (gloss)':<40} {'Function':<16} {'Count':>6}")
    print('  ' + '-' * 65)
    for _, row in df.iterrows():
        gloss = row['gloss'][:38] if len(row['gloss']) > 38 else row['gloss']
        func = row['function'][:14] if len(row['function']) > 14 else row['function']
        print(f"  {gloss:<40} {func:<16} {row['count']:>6,}")
    print()


def print_ot_top_ngrams(
    n: int = 2,
    *,
    min_count: int = 10,
    top_n: int = 30,
    book: str | None = None,
) -> None:
    scope = f" ({book})" if book else " (full OT)"
    df = ot_formula_frequency(n, min_count=min_count, book=book).head(top_n)
    print(f"\nTop Hebrew {n}-gram lemma sequences{scope}")
    print(f"  {'#':>3}  {'N-gram':<50} {'Count':>7}")
    print('  ' + '-' * 65)
    for i, (_, row) in enumerate(df.iterrows(), 1):
        ng = row['ngram'][:48] if len(row['ngram']) > 48 else row['ngram']
        print(f"  {i:>3}  {ng:<50} {row['count']:>7,}")
    print()


def print_nt_top_ngrams(
    n: int = 2,
    *,
    min_count: int = 5,
    top_n: int = 30,
    book: str | None = None,
) -> None:
    scope = f" ({book})" if book else " (full NT)"
    df = nt_formula_frequency(n, min_count=min_count, book=book).head(top_n)
    print(f"\nTop Greek {n}-gram lemma sequences{scope}")
    print(f"  {'#':>3}  {'N-gram':<50} {'Count':>7}")
    print('  ' + '-' * 65)
    for i, (_, row) in enumerate(df.iterrows(), 1):
        ng = row['ngram'][:48] if len(row['ngram']) > 48 else row['ngram']
        print(f"  {i:>3}  {ng:<50} {row['count']:>7,}")
    print()


# ── chart functions ───────────────────────────────────────────────────────────

def formula_book_chart(
    pattern: str | list[str],
    *,
    lang: str = 'H',
) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    pat = _parse_pattern(pattern)
    df = formula_book_distribution(pat, lang=lang)
    if df.empty:
        return None

    ensure_chart_dir(_CHART_DIR)
    safe = '_'.join(p[:8] for p in pat).replace('/', '_')
    out = _CHART_DIR / f'formula_books_{safe}_{lang}.png'
    pat_str = ' '.join(pat)

    fig, ax = plt.subplots(figsize=(max(8, len(df) * 0.5), 5))
    ax.bar(df['book'], df['count'], color='steelblue')
    ax.set_xlabel('Book')
    ax.set_ylabel('Occurrences')
    ax.set_title(f'Formula: {pat_str}\nDistribution by Book')
    ax.tick_params(axis='x', rotation=45, labelsize=8)
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def formula_chapter_chart(
    book: str,
    formula_key: str,
    *,
    lang: str = 'H',
) -> Path | None:
    """Bar chart of formula occurrences per chapter within a single book."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    registry = HEBREW_FORMULAS if lang == 'H' else GREEK_FORMULAS
    if formula_key not in registry:
        return None

    pat = registry[formula_key]['pattern']
    result = ot_formula_search(pat, book=book) if lang == 'H' else nt_formula_search(pat, book=book)
    if result.empty:
        return None

    # Count per chapter
    ch_counts = result.groupby('chapter').size().reset_index(name='count')

    ensure_chart_dir(_CHART_DIR)
    out = _CHART_DIR / f'formula_{formula_key}_{book}.png'
    gloss = registry[formula_key]['gloss']

    fig, ax = plt.subplots(figsize=(max(6, len(ch_counts) * 0.5), 4))
    ax.bar(ch_counts['chapter'], ch_counts['count'], color='darkorange')
    ax.set_xlabel('Chapter')
    ax.set_ylabel('Occurrences')
    ax.set_title(f'"{gloss}" per chapter — {book}')
    ax.set_xticks(ch_counts['chapter'])
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out
