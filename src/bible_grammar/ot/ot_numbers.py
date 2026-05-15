"""
Hebrew OT number morphology profile.

Analyses the 6,881 number tokens (class_='num') in the MACULA Hebrew WLC dataset,
covering cardinal and ordinal numbers, gender polarity, construct chains, and
distribution across the OT corpus.

Key pedagogical point for BBH Ch11: the gender-polarity rule — cardinal numbers 3–10
take the *opposite* gender of the noun they count (masculine form counts feminine nouns
and vice versa). אֶחָד/שְׁנַיִם (1–2) agree normally; 11–19 use both; 20+ are invariable.

Public API
──────────
ot_number_data(book=None)               → DataFrame (all num-class tokens)
ot_number_frequency()                   → DataFrame (lemma frequency table)
ot_number_gender_profile(book=None)     → DataFrame (gender distribution)
ot_number_state_profile(book=None)      → DataFrame (state distribution)
ot_number_book_distribution()           → DataFrame (count + pct per OT book)
ot_number_genre_profile()               → DataFrame (count by genre group)
ot_number_polarity_table()              → DataFrame (gender × value for cardinals 1–10)
ot_top_number_lemmas(n=20)              → DataFrame (most frequent number lemmas)

print_ot_number_overview()              → None
print_ot_number_frequency(n=20)         → None
print_ot_number_gender(book=None)       → None
print_ot_number_state(book=None)        → None
print_ot_number_book_distribution()     → None
print_ot_number_genre_profile()         → None
print_ot_number_polarity()              → None

ot_number_frequency_chart()             → Path | None
ot_number_genre_chart()                 → Path | None
ot_number_book_chart()                  → Path | None
"""

from __future__ import annotations
from pathlib import Path

import pandas as pd

from ..core._utils import load_ot_data

GENDER_ORDER = ['masculine', 'feminine', 'both', 'common']
STATE_ORDER  = ['absolute', 'construct', 'determined']
NUMBER_ORDER = ['singular', 'plural', 'dual']

OT_BOOK_GROUPS = {
    'Torah':      ['Gen', 'Exo', 'Lev', 'Num', 'Deu'],
    'Historical': ['Jos', 'Jdg', 'Rut', '1Sa', '2Sa', '1Ki', '2Ki',
                   '1Ch', '2Ch', 'Ezr', 'Neh', 'Est'],
    'Wisdom':     ['Job', 'Psa', 'Pro', 'Ecc', 'Sng'],
    'Prophets':   ['Isa', 'Jer', 'Lam', 'Ezk', 'Dan', 'Hos', 'Jol',
                   'Amo', 'Oba', 'Jon', 'Mic', 'Nam', 'Hab', 'Zep',
                   'Hag', 'Zec', 'Mal'],
}

OT_BOOK_ORDER = (
    OT_BOOK_GROUPS['Torah'] + OT_BOOK_GROUPS['Historical'] +
    OT_BOOK_GROUPS['Wisdom'] + OT_BOOK_GROUPS['Prophets']
)

# Books that concentrate number usage (census, chronology, temple dimensions)
CENSUS_BOOKS = ['Num', '1Ch', '2Ch', 'Exo', 'Ezk', 'Ezr', 'Neh']

# Cardinal numbers 1–10 with their Hebrew lemmas and Strong's
CARDINALS_1_10 = {
    1:  {'lemma': 'אֶחָד',    'strong': 'H259',  'gloss': 'one'},
    2:  {'lemma': 'שְׁנַיִם', 'strong': 'H8147', 'gloss': 'two'},
    3:  {'lemma': 'שָׁלֹשׁ',  'strong': 'H7969', 'gloss': 'three'},
    4:  {'lemma': 'אַרְבַּע', 'strong': 'H702',  'gloss': 'four'},
    5:  {'lemma': 'חָמֵשׁ',   'strong': 'H2568', 'gloss': 'five'},
    6:  {'lemma': 'שֵׁשׁ',    'strong': 'H8337', 'gloss': 'six'},
    7:  {'lemma': 'שֶׁבַע',   'strong': 'H7651', 'gloss': 'seven'},
    8:  {'lemma': 'שְׁמֹנֶה', 'strong': 'H8083', 'gloss': 'eight'},
    9:  {'lemma': 'תֵּשַׁע',  'strong': 'H8672', 'gloss': 'nine'},
    10: {'lemma': 'עֶשֶׂר',   'strong': 'H6235', 'gloss': 'ten'},
}

_CHART_DIR = Path('output') / 'charts' / 'ot' / 'numbers'


# ── data access ──────────────────────────────────────────────────────────────

def ot_number_data(book: str | None = None) -> pd.DataFrame:
    """All Hebrew number tokens (class_='num', lang='H')."""
    df = load_ot_data()
    nums = df[(df['class_'] == 'num') & (df['lang'] == 'H')].copy()
    if book:
        nums = nums[nums['book'] == book]
    return nums


def ot_top_number_lemmas(n: int = 20) -> pd.DataFrame:
    """Most frequent number lemmas with gloss and Strong's."""
    df = ot_number_data()
    return (
        df.groupby(['lemma', 'strong_h', 'gloss'])
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
        .head(n)
        .reset_index(drop=True)
    )


def ot_number_frequency() -> pd.DataFrame:
    """Frequency table: lemma × count × pct, sorted by count."""
    df = ot_number_data()
    total = len(df)
    freq = (
        df.groupby(['lemma', 'strong_h', 'gloss'])
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
        .reset_index(drop=True)
    )
    freq['pct'] = (freq['count'] / total * 100).round(1)
    return freq


def ot_number_gender_profile(book: str | None = None) -> pd.DataFrame:
    """Gender distribution of number tokens."""
    df = ot_number_data(book)
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


def ot_number_state_profile(book: str | None = None) -> pd.DataFrame:
    """State distribution of number tokens."""
    df = ot_number_data(book)
    total = len(df)
    state = (
        df['state']
        .value_counts()
        .reindex([s for s in STATE_ORDER if s in df['state'].unique()])
        .reset_index()
    )
    state.columns = ['state', 'count']
    state['pct'] = (state['count'] / total * 100).round(1)
    return state


def ot_number_book_distribution() -> pd.DataFrame:
    """Count of number tokens per OT book in canonical order."""
    df = ot_number_data()
    total = len(df)
    counts = df['book'].value_counts().reset_index()
    counts.columns = ['book', 'count']
    counts['pct'] = (counts['count'] / total * 100).round(1)
    # Sort canonically
    order = {b: i for i, b in enumerate(OT_BOOK_ORDER)}
    counts['_ord'] = counts['book'].map(order)
    counts = counts.sort_values('_ord').drop(columns='_ord').reset_index(drop=True)
    return counts


def ot_number_genre_profile() -> pd.DataFrame:
    """Number token count and percentage per genre group."""
    df = ot_number_data()
    book_to_genre = {b: g for g, books in OT_BOOK_GROUPS.items() for b in books}
    df = df.copy()
    df['genre'] = df['book'].map(book_to_genre)
    genre_counts = df['genre'].value_counts()
    genre_pct = (genre_counts / len(df) * 100).round(1)
    result = pd.DataFrame({'count': genre_counts, 'pct': genre_pct})
    order = list(OT_BOOK_GROUPS.keys())
    return result.reindex(order).reset_index().rename(columns={'index': 'genre'})


def ot_number_polarity_table() -> pd.DataFrame:
    """
    Gender distribution for cardinals 1–10 illustrating the polarity rule.

    Numbers 3–10 show the reverse-gender pattern: the masculine form (no ה-)
    counts feminine nouns; the feminine form (-ה) counts masculine nouns.
    """
    df = ot_number_data()
    rows = []
    for val, info in CARDINALS_1_10.items():
        subset = df[df['strong_h'] == info['strong']]
        total = len(subset)
        if total == 0:
            continue
        gender_counts = subset['gender'].value_counts()
        rows.append({
            'value': val,
            'lemma': info['lemma'],
            'gloss': info['gloss'],
            'total': total,
            'masculine': gender_counts.get('masculine', 0),
            'feminine': gender_counts.get('feminine', 0),
            'both': gender_counts.get('both', 0),
            'masc_pct': round(gender_counts.get('masculine', 0) / total * 100, 1),
            'fem_pct': round(gender_counts.get('feminine', 0) / total * 100, 1),
        })
    return pd.DataFrame(rows)


# ── print functions ───────────────────────────────────────────────────────────

def print_ot_number_overview() -> None:
    df = ot_number_data()
    total = len(df)
    unique_lemmas = df['lemma'].nunique()
    books = df['book'].nunique()
    top_book = df['book'].value_counts().index[0]
    top_count = df['book'].value_counts().iloc[0]
    print("Hebrew Number Tokens (OT)")
    print(f"  Total tokens : {total:,}")
    print(f"  Unique lemmas: {unique_lemmas}")
    print(f"  Books covered: {books}")
    print(f"  Most numbers : {top_book} ({top_count:,} tokens, "
          f"{top_count/total*100:.1f}%)")


def print_ot_number_frequency(n: int = 20) -> None:
    df = ot_number_frequency().head(n)
    print(f"{'Lemma':<14} {'Strong':<8} {'Gloss':<18} {'Count':>6} {'%':>6}")
    print('-' * 58)
    for _, row in df.iterrows():
        print(f"{row['lemma']:<14} {row['strong_h']:<8} {str(row['gloss']):<18} "
              f"{row['count']:>6,} {row['pct']:>5.1f}%")


def print_ot_number_gender(book: str | None = None) -> None:
    df = ot_number_gender_profile(book)
    label = f" ({book})" if book else ""
    print(f"Number Gender Distribution{label}")
    print(f"  {'Gender':<14} {'Count':>7} {'%':>6}")
    print('  ' + '-' * 30)
    for _, row in df.iterrows():
        print(f"  {str(row['gender']):<14} {row['count']:>7,} {row['pct']:>5.1f}%")


def print_ot_number_state(book: str | None = None) -> None:
    df = ot_number_state_profile(book)
    label = f" ({book})" if book else ""
    print(f"Number State Distribution{label}")
    print(f"  {'State':<14} {'Count':>7} {'%':>6}")
    print('  ' + '-' * 30)
    for _, row in df.iterrows():
        print(f"  {str(row['state']):<14} {row['count']:>7,} {row['pct']:>5.1f}%")


def print_ot_number_book_distribution() -> None:
    df = ot_number_book_distribution()
    print("Number Tokens per OT Book")
    print(f"  {'Book':<6} {'Count':>6} {'%':>6}")
    print('  ' + '-' * 22)
    for _, row in df.iterrows():
        print(f"  {row['book']:<6} {row['count']:>6,} {row['pct']:>5.1f}%")


def print_ot_number_genre_profile() -> None:
    df = ot_number_genre_profile()
    print("Number Tokens by Genre")
    print(f"  {'Genre':<12} {'Count':>6} {'%':>6}")
    print('  ' + '-' * 28)
    for _, row in df.iterrows():
        print(f"  {str(row['genre']):<12} {row['count']:>6,} {row['pct']:>5.1f}%")


def print_ot_number_polarity() -> None:
    df = ot_number_polarity_table()
    print("Cardinal Numbers 1–10: Gender Distribution")
    print("(Numbers 3–10 show reverse-gender polarity in Hebrew)")
    print()
    print(f"  {'#':<3} {'Lemma':<12} {'Gloss':<8} {'Total':>6} "
          f"{'Masc':>6} {'M%':>5} {'Fem':>6} {'F%':>5}")
    print('  ' + '-' * 60)
    for _, row in df.iterrows():
        print(f"  {int(row['value']):<3} {row['lemma']:<12} {row['gloss']:<8} "
              f"{int(row['total']):>6,} {int(row['masculine']):>6,} {row['masc_pct']:>4.0f}% "
              f"{int(row['feminine']):>6,} {row['fem_pct']:>4.0f}%")


# ── chart functions ───────────────────────────────────────────────────────────

def ot_number_frequency_chart(n: int = 15) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = ot_top_number_lemmas(n)
    _CHART_DIR.mkdir(parents=True, exist_ok=True)
    out = _CHART_DIR / 'ot_number_frequency.png'

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df['lemma'][::-1], df['count'][::-1], color='steelblue')
    for i, (count, lemma) in enumerate(zip(df['count'][::-1], df['lemma'][::-1])):
        ax.text(count + 5, i, str(count), va='center', fontsize=8)
    ax.set_xlabel('Occurrences')
    ax.set_title(f'Top {n} Hebrew Number Lemmas (OT)')
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def ot_number_genre_chart() -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = ot_number_genre_profile()
    _CHART_DIR.mkdir(parents=True, exist_ok=True)
    out = _CHART_DIR / 'ot_number_genre.png'

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(df['genre'], df['count'], color='steelblue')
    ax.set_ylabel('Number tokens')
    ax.set_title('Hebrew Number Tokens by Genre (OT)')
    for i, (g, c) in enumerate(zip(df['genre'], df['count'])):
        ax.text(i, c + 10, str(c), ha='center', fontsize=9)
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def ot_number_book_chart(top_n: int = 20) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = ot_number_book_distribution().head(top_n)
    _CHART_DIR.mkdir(parents=True, exist_ok=True)
    out = _CHART_DIR / 'ot_number_books.png'

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df['book'][::-1], df['count'][::-1], color='steelblue')
    ax.set_xlabel('Number tokens')
    ax.set_title(f'Hebrew Number Tokens — Top {top_n} Books')
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out
