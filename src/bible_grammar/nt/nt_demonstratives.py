"""
Greek NT demonstrative pronoun/adjective profile.

Analyses the 1,709 demonstrative tokens (type_='demonstrative') in the MACULA
Greek Nestle1904 dataset. Covers οὗτος (this/these, 1,388 tokens) and ἐκεῖνος
(that/those, 244 tokens), plus τοιοῦτος (such a kind, 57) and τοσοῦτος (so great, 20).

Key pedagogical points for BBG Ch13:
- οὗτος (near) vs. ἐκεῖνος (far) — the two primary demonstratives
- Three uses: attributive (modifying a noun), substantival (standing alone as noun),
  predicate (with copula — "this is…")
- Attributive position: demonstrative FOLLOWS the article+noun (article-noun-dem)
  unlike ordinary adjectives

Public API
──────────
nt_demo_data(book=None)                    → DataFrame (all demonstrative tokens)
nt_demo_frequency()                        → DataFrame (lemma frequency table)
nt_demo_case_profile(lemma=None)           → DataFrame (case distribution)
nt_demo_gender_profile(lemma=None)         → DataFrame (gender distribution)
nt_demo_use_profile(lemma=None)            → DataFrame (attributive vs. substantival)
nt_demo_book_distribution()                → DataFrame (count + pct per NT book)
nt_demo_genre_profile()                    → DataFrame (count by genre group)
nt_demo_near_far_comparison()              → DataFrame (οὗτος vs. ἐκεῖνος by genre)
nt_demo_top_cooccurrences(lemma, n=15)     → DataFrame (most co-verse nouns)

print_nt_demo_overview()                   → None
print_nt_demo_frequency()                  → None
print_nt_demo_case(lemma=None)             → None
print_nt_demo_gender(lemma=None)           → None
print_nt_demo_use()                        → None
print_nt_demo_book_distribution()          → None
print_nt_demo_genre_profile()              → None
print_nt_demo_near_far()                   → None

nt_demo_frequency_chart()                  → Path | None
nt_demo_case_chart(lemma=None)             → Path | None
nt_demo_genre_heatmap()                    → Path | None
nt_demo_book_chart()                       → Path | None
"""

from __future__ import annotations
from pathlib import Path

import pandas as pd

from ..core.syntax import load_syntax as _load_nt_data

# Strong's numbers (no G prefix, no zero-padding — matches MACULA column)
OUTOS    = '3778'   # οὗτος — near demonstrative (this/these)
EKEINOS  = '1565'   # ἐκεῖνος — far demonstrative (that/those)
TOIOUTOS = '5108'   # τοιοῦτος — qualitative (such, of such a kind)
TOSOUTON = '5118'   # τοσοῦτος — quantitative (so great, so much)

DEMO_STRONGS = {OUTOS, EKEINOS, TOIOUTOS, TOSOUTON}

DEMO_LABELS = {
    OUTOS:    'οὗτος (this)',
    EKEINOS:  'ἐκεῖνος (that)',
    TOIOUTOS: 'τοιοῦτος (such)',
    TOSOUTON: 'τοσοῦτος (so great)',
}

CASE_ORDER   = ['nominative', 'accusative', 'genitive', 'dative']
GENDER_ORDER = ['masculine', 'feminine', 'neuter']
NUMBER_ORDER = ['singular', 'plural']

NT_GENRE = {
    'Gospels': ['Mat', 'Mrk', 'Luk', 'Jhn'],
    'Acts':    ['Act'],
    'Pauline': ['Rom', '1Co', '2Co', 'Gal', 'Eph', 'Php', 'Col',
                '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm'],
    'General': ['Heb', 'Jas', '1Pe', '2Pe', '1Jn', '2Jn', '3Jn', 'Jud', 'Rev'],
}

NT_BOOK_ORDER = (
    NT_GENRE['Gospels'] + NT_GENRE['Acts'] +
    NT_GENRE['Pauline'] + NT_GENRE['General']
)

_CHART_DIR = Path('output') / 'charts' / 'nt' / 'demonstratives'


# ── data access ───────────────────────────────────────────────────────────────

def nt_demo_data(book: str | None = None) -> pd.DataFrame:
    """All demonstrative pronoun/adjective tokens."""
    df = _load_nt_data()
    demos = df[df['strong'].isin(DEMO_STRONGS)].copy()
    if book:
        demos = demos[demos['book'] == book]
    # Classify use: tokens with a syntactic role are substantival;
    # tokens without a role are attributive/predicate modifiers
    demos['use'] = demos['role'].apply(
        lambda r: 'substantival' if pd.notna(r) and r in ('s', 'o', 'io', 'p', 'adv')
        else 'attributive/predicate'
    )
    return demos


def nt_demo_frequency() -> pd.DataFrame:
    """Lemma frequency table."""
    df = nt_demo_data()
    total = len(df)
    freq = (
        df.groupby(['strong', 'lemma'])
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
        .reset_index(drop=True)
    )
    freq['pct'] = (freq['count'] / total * 100).round(1)
    return freq


def nt_demo_case_profile(lemma: str | None = None) -> pd.DataFrame:
    """Case distribution, optionally filtered to one lemma ('οὗτος' or 'ἐκεῖνος')."""
    df = nt_demo_data()
    if lemma:
        df = df[df['lemma'] == lemma]
    total = len(df)
    case = (
        df['case_']
        .value_counts()
        .reindex([c for c in CASE_ORDER if c in df['case_'].unique()])
        .reset_index()
    )
    case.columns = ['case_', 'count']
    case['pct'] = (case['count'] / total * 100).round(1)
    return case


def nt_demo_gender_profile(lemma: str | None = None) -> pd.DataFrame:
    """Gender distribution, optionally filtered to one lemma."""
    df = nt_demo_data()
    if lemma:
        df = df[df['lemma'] == lemma]
    total = len(df)
    gender = (
        df['gender']
        .value_counts()
        .reindex([g for g in GENDER_ORDER if g in df['gender'].unique()])
        .reset_index()
    )
    gender.columns = ['gender', 'count']
    gender['pct'] = (gender['count'] / total * 100).round(1)
    return gender


def nt_demo_use_profile(lemma: str | None = None) -> pd.DataFrame:
    """Attributive/predicate vs. substantival use distribution."""
    df = nt_demo_data()
    if lemma:
        df = df[df['lemma'] == lemma]
    total = len(df)
    use = df['use'].value_counts().reset_index()
    use.columns = ['use', 'count']
    use['pct'] = (use['count'] / total * 100).round(1)
    return use


def nt_demo_book_distribution() -> pd.DataFrame:
    """Count of demonstrative tokens per NT book in canonical order."""
    df = nt_demo_data()
    total = len(df)
    counts = df['book'].value_counts().reset_index()
    counts.columns = ['book', 'count']
    counts['pct'] = (counts['count'] / total * 100).round(1)
    order = {b: i for i, b in enumerate(NT_BOOK_ORDER)}
    counts['_ord'] = counts['book'].map(order)
    counts = counts.sort_values('_ord').drop(columns='_ord').reset_index(drop=True)
    return counts


def nt_demo_genre_profile() -> pd.DataFrame:
    """Demonstrative count and percentage per NT genre group."""
    df = nt_demo_data()
    book_to_genre = {b: g for g, books in NT_GENRE.items() for b in books}
    df = df.copy()
    df['genre'] = df['book'].map(book_to_genre)
    genre_counts = df['genre'].value_counts()
    genre_pct = (genre_counts / len(df) * 100).round(1)
    result = pd.DataFrame({'count': genre_counts, 'pct': genre_pct})
    order = list(NT_GENRE.keys())
    return result.reindex(order).reset_index().rename(columns={'index': 'genre'})


def nt_demo_near_far_comparison() -> pd.DataFrame:
    """οὗτος vs. ἐκεῖνος count by NT genre — near/far contrast."""
    df = nt_demo_data()
    df = df[df['strong'].isin([OUTOS, EKEINOS])].copy()
    book_to_genre = {b: g for g, books in NT_GENRE.items() for b in books}
    df['genre'] = df['book'].map(book_to_genre)
    pivot = (
        df.groupby(['genre', 'lemma'])
        .size()
        .unstack(fill_value=0)
        .reindex(list(NT_GENRE.keys()))
    )
    return pivot


def nt_demo_top_cooccurrences(strong: str = OUTOS, n: int = 15) -> pd.DataFrame:
    """
    Nouns that appear in the same verse as the given demonstrative most often.
    Useful for seeing what things/persons οὗτος and ἐκεῖνος point to.
    """
    df_all = _load_nt_data()
    demos = df_all[df_all['strong'] == strong][['book', 'chapter', 'verse']].drop_duplicates()
    nouns_in_verse = df_all[
        (df_all['class_'] == 'noun') &
        df_all.set_index(['book', 'chapter', 'verse']).index.isin(
            demos.set_index(['book', 'chapter', 'verse']).index
        )
    ]
    return (
        nouns_in_verse.groupby(['lemma', 'strong'])
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
        .head(n)
        .reset_index(drop=True)
    )


# ── print functions ───────────────────────────────────────────────────────────

def print_nt_demo_overview() -> None:
    df = nt_demo_data()
    total = len(df)
    print("Greek NT Demonstrative Pronouns/Adjectives")
    print(f"  Total tokens : {total:,}")
    by_lemma = df['lemma'].value_counts()
    for lemma, count in by_lemma.items():
        print(f"    {lemma:<14} {count:>5,}  ({count/total*100:.1f}%)")
    print(f"  Books covered: {df['book'].nunique()}")


def print_nt_demo_frequency() -> None:
    df = nt_demo_frequency()
    print(f"{'Strong':<8} {'Lemma':<16} {'Count':>6} {'%':>6}")
    print('-' * 42)
    for _, row in df.iterrows():
        print(f"G{row['strong']:<7} {row['lemma']:<16} {row['count']:>6,} {row['pct']:>5.1f}%")


def print_nt_demo_case(lemma: str | None = None) -> None:
    df = nt_demo_case_profile(lemma)
    label = f" ({lemma})" if lemma else ""
    print(f"Case Distribution{label}")
    print(f"  {'Case':<14} {'Count':>6} {'%':>6}")
    print('  ' + '-' * 30)
    for _, row in df.iterrows():
        print(f"  {str(row['case_']):<14} {row['count']:>6,} {row['pct']:>5.1f}%")


def print_nt_demo_gender(lemma: str | None = None) -> None:
    df = nt_demo_gender_profile(lemma)
    label = f" ({lemma})" if lemma else ""
    print(f"Gender Distribution{label}")
    print(f"  {'Gender':<12} {'Count':>6} {'%':>6}")
    print('  ' + '-' * 28)
    for _, row in df.iterrows():
        print(f"  {str(row['gender']):<12} {row['count']:>6,} {row['pct']:>5.1f}%")


def print_nt_demo_use() -> None:
    print("Use Type: οὗτος vs. ἐκεῖνος")
    for lemma in ['οὗτος', 'ἐκεῖνος']:
        df = nt_demo_use_profile(lemma)
        print(f"\n  {lemma}:")
        for _, row in df.iterrows():
            print(f"    {str(row['use']):<26} {row['count']:>5,}  ({row['pct']:.1f}%)")


def print_nt_demo_book_distribution() -> None:
    df = nt_demo_book_distribution()
    print("Demonstrative Tokens per NT Book")
    print(f"  {'Book':<6} {'Count':>6} {'%':>6}")
    print('  ' + '-' * 22)
    for _, row in df.iterrows():
        print(f"  {row['book']:<6} {row['count']:>6,} {row['pct']:>5.1f}%")


def print_nt_demo_genre_profile() -> None:
    df = nt_demo_genre_profile()
    print("Demonstrative Tokens by NT Genre")
    print(f"  {'Genre':<10} {'Count':>6} {'%':>6}")
    print('  ' + '-' * 26)
    for _, row in df.iterrows():
        print(f"  {str(row['genre']):<10} {row['count']:>6,} {row['pct']:>5.1f}%")


def print_nt_demo_near_far() -> None:
    df = nt_demo_near_far_comparison()
    print("Near (οὗτος) vs. Far (ἐκεῖνος) by Genre")
    print(df.to_string())


# ── chart functions ───────────────────────────────────────────────────────────

def nt_demo_frequency_chart() -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_demo_frequency()
    _CHART_DIR.mkdir(parents=True, exist_ok=True)
    out = _CHART_DIR / 'nt_demo_frequency.png'

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(df['lemma'], df['count'], color='steelblue')
    ax.set_ylabel('Occurrences')
    ax.set_title('Greek NT Demonstrative Pronoun Frequency')
    for i, (lemma, count) in enumerate(zip(df['lemma'], df['count'])):
        ax.text(i, count + 5, str(count), ha='center', fontsize=9)
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def nt_demo_case_chart(lemma: str | None = None) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_demo_case_profile(lemma)
    _CHART_DIR.mkdir(parents=True, exist_ok=True)
    suffix = f'_{lemma}' if lemma else ''
    out = _CHART_DIR / f'nt_demo_case{suffix}.png'

    label = f' — {lemma}' if lemma else ''
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(df['case_'], df['count'], color='steelblue')
    ax.set_ylabel('Occurrences')
    ax.set_title(f'Demonstrative Case Distribution{label}')
    for i, (c, count) in enumerate(zip(df['case_'], df['count'])):
        ax.text(i, count + 2, str(count), ha='center', fontsize=9)
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def nt_demo_genre_heatmap() -> Path | None:
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ImportError:
        return None

    df = nt_demo_near_far_comparison()
    _CHART_DIR.mkdir(parents=True, exist_ok=True)
    out = _CHART_DIR / 'nt_demo_genre_heatmap.png'

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.heatmap(df, annot=True, fmt='d', cmap='Blues', ax=ax)
    ax.set_title('Demonstrative Pronouns by Genre (οὗτος vs. ἐκεῖνος)')
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def nt_demo_book_chart(top_n: int = 15) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_demo_book_distribution().head(top_n)
    _CHART_DIR.mkdir(parents=True, exist_ok=True)
    out = _CHART_DIR / 'nt_demo_books.png'

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df['book'][::-1], df['count'][::-1], color='steelblue')
    ax.set_xlabel('Demonstrative tokens')
    ax.set_title(f'Greek Demonstrative Pronouns — Top {top_n} NT Books')
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out
