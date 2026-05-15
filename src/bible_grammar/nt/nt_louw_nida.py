"""
Louw-Nida sub-domain precision queries for the Greek NT.

The MACULA Greek NT dataset carries an `ln` column with sub-domain codes
in Louw-Nida format (e.g., '33.69', '31.35', '92.24').  The existing
`domain_search.py` module handles top-level domain queries (domain 33 =
Communication); this module exposes sub-domain granularity.

LN code format
──────────────
  '33.69'   — domain 33, sub-entry 69   (teach/instruct)
  '92.24'   — domain 92 (article ὁ)
  '93.169a' — proper noun variant

Multiple codes may be space-separated: '10.24 33.19'

Coverage: ~127,291 NT tokens with ln data (92.4% of all 137,779 NT tokens).
          6,941 unique sub-domain codes across 93 top-level domains.

Questions this answers
──────────────────────
  • What are the most frequent sub-domain codes in Romans?
  • Which lemmas fall in LN 31 (Hold a View, Believe, Trust)?
  • How does LN 33 (Communication) break down across its sub-domains?
  • Which books use the most Judgment/Punishment vocabulary (LN 38/56)?
  • Compare Paul's ethics vocabulary (LN 88) vs. John's?

Public API
──────────
nt_ln_data(subdomain=None, domain=None, book=None)   → DataFrame
nt_ln_subdomain_frequency(domain, book=None, top_n=20) → DataFrame
nt_ln_top_lemmas(subdomain, top_n=20, book=None)     → DataFrame
nt_ln_book_distribution(subdomain)                   → DataFrame
nt_ln_genre_profile(subdomain)                       → DataFrame
nt_ln_domain_breakdown(domain, book=None, top_n=20)  → DataFrame
nt_ln_comparison(books, domain, top_n=15)            → pivot DataFrame

print_nt_ln_overview()                               → None
print_nt_ln_subdomain_frequency(domain, ...)         → None
print_nt_ln_top_lemmas(subdomain, ...)               → None
print_nt_ln_book_distribution(subdomain)             → None
print_nt_ln_domain_breakdown(domain, ...)            → None
print_nt_ln_comparison(books, domain, ...)           → None

nt_ln_subdomain_chart(domain, ...)                   → Path | None
nt_ln_book_chart(subdomain, top_n=20)                → Path | None
nt_ln_genre_heatmap(domains, books)                  → Path | None

LN_DOMAIN_NAMES                                      → dict[int, str]
"""

from __future__ import annotations
import re
from pathlib import Path
from collections import Counter

import pandas as pd

from ..core._utils import ensure_chart_dir
from ..lexical.domain_search import DOMAIN_NAMES as LN_DOMAIN_NAMES  # re-export

_CHART_DIR = Path('output') / 'charts' / 'nt' / 'louw_nida'

NT_BOOK_GROUPS: dict[str, list[str]] = {
    'Gospels & Acts': ['Mat', 'Mrk', 'Luk', 'Jhn', 'Act'],
    'Pauline':        ['Rom', '1Co', '2Co', 'Gal', 'Eph', 'Php', 'Col',
                       '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm'],
    'General & Rev':  ['Heb', 'Jas', '1Pe', '2Pe', '1Jn', '2Jn', '3Jn',
                       'Jud', 'Rev'],
}
NT_BOOK_ORDER = (
    NT_BOOK_GROUPS['Gospels & Acts'] +
    NT_BOOK_GROUPS['Pauline'] +
    NT_BOOK_GROUPS['General & Rev']
)


# ── helpers ───────────────────────────────────────────────────────────────────

def _load_nt() -> pd.DataFrame:
    from ..core._utils import load_nt
    return load_nt()


def _parse_ln(ln_str: str) -> list[str]:
    """Split space-separated LN codes, stripping trailing letter suffixes."""
    if not ln_str or not isinstance(ln_str, str):
        return []
    codes = []
    for raw in ln_str.split():
        raw = raw.strip()
        if raw:
            codes.append(raw)
    return codes


def _ln_domain_of(code: str) -> int | None:
    """Return the top-level domain number for an LN code ('33.69' → 33)."""
    m = re.match(r'^(\d+)', code)
    return int(m.group(1)) if m else None


def _normalise_code(code: str) -> str:
    """Normalise an LN code for consistent matching (strip trailing alpha)."""
    return re.sub(r'[a-zA-Z]+$', '', code.strip())


# ── data access ───────────────────────────────────────────────────────────────

def nt_ln_data(
    subdomain: str | None = None,
    *,
    domain: int | None = None,
    book: str | list[str] | None = None,
) -> pd.DataFrame:
    """
    NT tokens with LN data, optionally filtered by sub-domain or top-level domain.

    Parameters
    ----------
    subdomain : exact LN code to match, e.g. '33.69', '31.35'
    domain    : top-level domain number to match (e.g. 33 matches all 33.x)
    book      : book abbreviation or list of abbreviations
    """
    df = _load_nt()
    if book is not None:
        if isinstance(book, str):
            book = [book]
        df = df[df['book'].isin(book)]

    df = df[df['ln'].notna() & (df['ln'] != '')].copy()

    if domain is not None:
        df = df[df['ln'].str.contains(re.escape(str(domain)) + r'\.', na=False)]

    if subdomain is not None:
        norm = _normalise_code(subdomain)
        df = df[df['ln'].apply(
            lambda x: any(_normalise_code(c) == norm for c in _parse_ln(x))
        )]

    return df.reset_index(drop=True)


def nt_ln_subdomain_frequency(
    domain: int,
    *,
    book: str | list[str] | None = None,
    top_n: int = 20,
) -> pd.DataFrame:
    """
    Frequency of sub-domain codes within a given top-level LN domain.

    Returns: subdomain, count, pct, top_lemma.
    """
    df = nt_ln_data(domain=domain, book=book)
    if df.empty:
        return pd.DataFrame(columns=['subdomain', 'count', 'pct', 'top_lemma'])

    code_rows: list[tuple[str, str]] = []
    for _, row in df.iterrows():
        for code in _parse_ln(row['ln']):
            if _ln_domain_of(code) == domain:
                code_rows.append((_normalise_code(code), row['lemma']))

    if not code_rows:
        return pd.DataFrame(columns=['subdomain', 'count', 'pct', 'top_lemma'])

    from collections import defaultdict
    code_lemmas: dict[str, Counter] = defaultdict(Counter)
    for code, lemma in code_rows:
        code_lemmas[code][lemma] += 1

    total = len(code_rows)
    rows = []
    for code, lemma_counts in code_lemmas.items():
        top = lemma_counts.most_common(1)[0][0]
        rows.append({'subdomain': code, 'count': sum(lemma_counts.values()), 'top_lemma': top})

    result = (
        pd.DataFrame(rows)
        .sort_values('count', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
    result['pct'] = (result['count'] / total * 100).round(1)
    return result[['subdomain', 'count', 'pct', 'top_lemma']]


def nt_ln_top_lemmas(
    subdomain: str,
    *,
    top_n: int = 20,
    book: str | list[str] | None = None,
) -> pd.DataFrame:
    """Most frequent lemmas tagged with a given LN sub-domain code."""
    df = nt_ln_data(subdomain=subdomain, book=book)
    if df.empty:
        return pd.DataFrame(columns=['lemma', 'strong_g', 'gloss', 'count'])

    result = (
        df.groupby(['lemma', 'strong_g', 'gloss'], dropna=False)
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
    return result


def nt_ln_book_distribution(
    subdomain: str,
) -> pd.DataFrame:
    """Book-by-book distribution of tokens in a given LN sub-domain."""
    df = nt_ln_data(subdomain=subdomain)
    if df.empty:
        return pd.DataFrame(columns=['book', 'count', 'pct'])

    total = len(df)
    counts = df['book'].value_counts().reset_index()
    counts.columns = ['book', 'count']
    counts['pct'] = (counts['count'] / total * 100).round(1)
    order = {b: i for i, b in enumerate(NT_BOOK_ORDER)}
    counts['_ord'] = counts['book'].map(order).fillna(999)
    return counts.sort_values('_ord').drop(columns='_ord').reset_index(drop=True)


def nt_ln_genre_profile(
    subdomain: str,
) -> pd.DataFrame:
    """Genre distribution for a given LN sub-domain."""
    df = nt_ln_data(subdomain=subdomain)
    if df.empty:
        return pd.DataFrame(columns=['genre', 'count', 'pct'])

    book_to_genre = {b: g for g, books in NT_BOOK_GROUPS.items() for b in books}
    df = df.copy()
    df['genre'] = df['book'].map(book_to_genre)
    counts = df['genre'].value_counts()
    pct = (counts / len(df) * 100).round(1)
    result = pd.DataFrame({'count': counts, 'pct': pct})
    order = list(NT_BOOK_GROUPS.keys())
    return result.reindex(order).reset_index().rename(columns={'index': 'genre'})


def nt_ln_domain_breakdown(
    domain: int,
    *,
    book: str | list[str] | None = None,
    top_n: int = 20,
) -> pd.DataFrame:
    """
    For a given top-level LN domain, show its sub-domain breakdown with
    the top lemma for each sub-domain.
    """
    return nt_ln_subdomain_frequency(domain, book=book, top_n=top_n)


def nt_ln_comparison(
    books: list[str],
    domain: int,
    *,
    top_n: int = 15,
) -> pd.DataFrame:
    """
    Compare LN sub-domain profiles across multiple NT books.

    Returns a pivot: rows=subdomain, cols=books, cells=% of book's domain tokens.
    """
    profiles: dict[str, pd.Series] = {}
    for book in books:
        df = nt_ln_subdomain_frequency(domain, book=book, top_n=100)
        if not df.empty:
            profiles[book] = df.set_index('subdomain')['pct']

    if not profiles:
        return pd.DataFrame()

    combined = pd.DataFrame(profiles).fillna(0).round(1)
    combined['_avg'] = combined.mean(axis=1)
    return combined.sort_values('_avg', ascending=False).drop(columns='_avg').head(top_n)


# ── print functions ───────────────────────────────────────────────────────────

def print_nt_ln_overview() -> None:
    df = _load_nt()
    has_ln = df[df['ln'].notna() & (df['ln'] != '')]
    # Count unique sub-domains
    all_codes: set[str] = set()
    for ln in has_ln['ln']:
        for c in _parse_ln(ln):
            all_codes.add(_normalise_code(c))
    w = 62
    print(f"\n{'═'*w}")
    print("  NT Louw-Nida Sub-Domain Coverage")
    print(f"{'═'*w}")
    print(f"  Total NT tokens      : {len(df):>9,}")
    print(f"  Tokens with LN code  : {len(has_ln):>9,} ({len(has_ln)/len(df)*100:.1f}%)")
    print(f"  Unique sub-domain codes: {len(all_codes):>7,}")
    print(f"  Top-level domains    : {len(LN_DOMAIN_NAMES):>9}")
    print()


def print_nt_ln_subdomain_frequency(
    domain: int,
    *,
    book: str | list[str] | None = None,
    top_n: int = 20,
) -> None:
    domain_name = LN_DOMAIN_NAMES.get(domain, str(domain))
    scope = f" ({book})" if isinstance(book, str) else ""
    df = nt_ln_subdomain_frequency(domain, book=book, top_n=top_n)
    w = 62
    print(f"\n{'═'*w}")
    print(f"  LN Domain {domain}: {domain_name}{scope}")
    print(f"  Sub-domain frequency (top {top_n})")
    print(f"{'═'*w}")
    if df.empty:
        print("  No results.")
        print()
        return
    print(f"  {'Sub-domain':<12} {'Count':>7} {'%':>6}  {'Top lemma'}")
    print(f"  {'-'*11} {'-'*7} {'-'*6}  {'-'*18}")
    for _, row in df.iterrows():
        print(f"  {row['subdomain']:<12} {row['count']:>7,} "
              f"{row['pct']:>5.1f}%  {row['top_lemma']}")
    print()


def print_nt_ln_top_lemmas(
    subdomain: str,
    *,
    top_n: int = 20,
    book: str | list[str] | None = None,
) -> None:
    scope = f" ({book})" if isinstance(book, str) else ""
    df = nt_ln_top_lemmas(subdomain, top_n=top_n, book=book)
    w = 66
    print(f"\n{'═'*w}")
    print(f"  LN {subdomain} — top lemmas{scope}")
    print(f"{'═'*w}")
    if df.empty:
        print("  No results.")
        print()
        return
    print(f"  {'Lemma':<14} {'Strong':<8} {'Gloss':<26} {'Count':>6}")
    print(f"  {'-'*13} {'-'*7} {'-'*25} {'-'*6}")
    for _, row in df.iterrows():
        print(f"  {str(row['lemma']):<14} {str(row['strong_g']):<8} "
              f"{str(row['gloss']):<26} {row['count']:>6,}")
    print()


def print_nt_ln_book_distribution(
    subdomain: str,
    *,
    top_n: int = 20,
) -> None:
    df = nt_ln_book_distribution(subdomain).head(top_n)
    print(f"\nLN {subdomain} — Book Distribution")
    print(f"  {'Book':<6} {'Count':>6} {'%':>6}")
    print('  ' + '-' * 22)
    for _, row in df.iterrows():
        print(f"  {row['book']:<6} {row['count']:>6,} {row['pct']:>5.1f}%")
    print()


def print_nt_ln_domain_breakdown(
    domain: int,
    *,
    book: str | list[str] | None = None,
    top_n: int = 20,
) -> None:
    print_nt_ln_subdomain_frequency(domain, book=book, top_n=top_n)


def print_nt_ln_comparison(
    books: list[str],
    domain: int,
    *,
    top_n: int = 15,
) -> None:
    domain_name = LN_DOMAIN_NAMES.get(domain, str(domain))
    df = nt_ln_comparison(books, domain, top_n=top_n)
    print(f"\nLN Domain {domain} ({domain_name}) — Book Comparison")
    print(f"  (% of each book's domain-{domain} tokens)")
    print()
    if df.empty:
        print("  No data.")
        return
    header = f"  {'Sub-domain':<12}" + ''.join(f" {b:>7}" for b in df.columns)
    print(header)
    print('  ' + '-' * (12 + 8 * len(df.columns)))
    for sd, row in df.iterrows():
        print(f"  {str(sd):<12}" + ''.join(f" {v:>6.1f}%" for v in row))
    print()


# ── chart functions ───────────────────────────────────────────────────────────

def nt_ln_subdomain_chart(
    domain: int,
    *,
    book: str | list[str] | None = None,
    top_n: int = 20,
) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_ln_subdomain_frequency(domain, book=book, top_n=top_n)
    if df.empty:
        return None

    domain_name = LN_DOMAIN_NAMES.get(domain, str(domain))
    ensure_chart_dir(_CHART_DIR)
    suffix = f"_{book}" if isinstance(book, str) else ""
    out = _CHART_DIR / f"ln{domain}_subdomains{suffix}.png"

    labels = [f"{row['subdomain']} ({row['top_lemma']})" for _, row in df.iterrows()]
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(labels[::-1], df['count'][::-1], color='steelblue')
    scope = f" ({book})" if isinstance(book, str) else ""
    ax.set_xlabel('Token count')
    ax.set_title(f'LN Domain {domain} ({domain_name}) — Sub-domain Breakdown{scope}')
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def nt_ln_book_chart(
    subdomain: str,
    *,
    top_n: int = 20,
) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_ln_book_distribution(subdomain).head(top_n)
    if df.empty:
        return None

    ensure_chart_dir(_CHART_DIR)
    out = _CHART_DIR / f"ln{subdomain.replace('.', '_')}_books.png"

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df['book'][::-1], df['count'][::-1], color='darkorange')
    ax.set_xlabel('Token count')
    ax.set_title(f'LN {subdomain} — Book Distribution')
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def nt_ln_genre_heatmap(
    domains: list[int],
    *,
    books: list[str] | None = None,
) -> Path | None:
    """
    Heatmap of top-level LN domain percentages across a set of NT books.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    if books is None:
        books = NT_BOOK_ORDER

    data_rows = []
    for domain in domains:
        domain_name = LN_DOMAIN_NAMES.get(domain, str(domain))
        row: dict = {'domain': f"{domain}: {domain_name}"}
        for book in books:
            df_b = nt_ln_data(domain=domain, book=book)
            total_book = len(_load_nt()[_load_nt()['book'] == book])
            row[book] = round(len(df_b) / max(total_book, 1) * 100, 2)
        data_rows.append(row)

    if not data_rows:
        return None

    pivot = pd.DataFrame(data_rows).set_index('domain')
    ensure_chart_dir(_CHART_DIR)
    out = _CHART_DIR / 'ln_domain_heatmap.png'

    fig, ax = plt.subplots(figsize=(max(10, len(books) * 0.9), max(5, len(domains) * 0.7)))
    im = ax.imshow(pivot.values.astype(float), aspect='auto', cmap='YlOrRd')
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, rotation=45, ha='right', fontsize=8)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=8)
    plt.colorbar(im, ax=ax, label='% of book tokens')
    ax.set_title('Louw-Nida Domain Profile by Book')
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out
