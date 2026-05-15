"""
Greek NT noun/case morphology profile.

Provides case distribution, declension pattern frequency, gender breakdown,
and article co-occurrence statistics across the GNT, backed by the MACULA
Greek syntax layer.

Public API
──────────
nt_noun_data(book=None)                  → DataFrame (all GNT noun tokens)
nt_noun_case_profile(book=None)          → DataFrame (case distribution)
nt_noun_gender_profile(book=None)        → DataFrame (gender distribution)
nt_noun_number_profile(book=None)        → DataFrame (number distribution)
nt_noun_case_gender(book=None)           → DataFrame (case × gender crosstab)
nt_noun_top_lemmas(n=30, book=None)      → DataFrame (most frequent noun lemmas)
nt_noun_lemma_case(lemmas=None)          → DataFrame (lemma × case crosstab)
nt_noun_book_distribution()              → DataFrame (count + pct per NT book)
nt_noun_genre_profile()                  → DataFrame (case % by genre group)
nt_article_stats(book=None)              → DataFrame (article vs anarthrous counts)

print_nt_noun_overview()                 → None
print_nt_noun_case(book=None)            → None
print_nt_noun_gender(book=None)          → None
print_nt_noun_case_gender(book=None)     → None
print_nt_noun_top_lemmas(n=20)           → None
print_nt_noun_genre_profile()            → None
print_nt_noun_book_distribution()        → None
print_nt_article_stats(book=None)        → None

nt_noun_case_chart(book=None)            → Path | None
nt_noun_gender_chart(book=None)          → Path | None
nt_noun_genre_heatmap()                  → Path | None
nt_noun_case_gender_heatmap(book=None)   → Path | None
nt_noun_book_chart()                     → Path | None
"""

from __future__ import annotations
from pathlib import Path

import pandas as pd

from ..core.syntax import load_syntax
from .nt_verb_profile import NT_BOOK_GROUPS, NT_BOOK_ORDER

CASE_ORDER   = ['nominative', 'accusative', 'genitive', 'dative', 'vocative']
GENDER_ORDER = ['masculine', 'feminine', 'neuter']
NUMBER_ORDER = ['singular', 'plural']

_CHART_DIR = Path('output') / 'charts' / 'nt' / 'nouns'


def _ensure_chart_dir() -> Path:
    _CHART_DIR.mkdir(parents=True, exist_ok=True)
    return _CHART_DIR


# ── Data loading ──────────────────────────────────────────────────────────────

def nt_noun_data(book: str | None = None) -> pd.DataFrame:
    """All GNT noun tokens (class_='noun'), optionally filtered to one book."""
    df = load_syntax()
    nouns = df[df['class_'] == 'noun'].copy()
    if book:
        nouns = nouns[nouns['book'] == book]
    return nouns


# ── Profile helpers ───────────────────────────────────────────────────────────

def _count_profile(series: pd.Series, order: list[str]) -> pd.DataFrame:
    vc = series.str.lower().value_counts()
    total = vc.sum()
    records = []
    for form in order:
        cnt = int(vc.get(form, 0))
        records.append({'form': form, 'count': cnt,
                        'pct': round(cnt / total * 100, 1) if total else 0.0})
    for form, cnt in vc.items():
        if str(form).lower() not in order:
            records.append({'form': str(form), 'count': int(cnt),
                            'pct': round(int(cnt) / total * 100, 1) if total else 0.0})
    return pd.DataFrame(records)


# ── Profile functions ─────────────────────────────────────────────────────────

def nt_noun_case_profile(book: str | None = None) -> pd.DataFrame:
    """Case distribution across GNT nouns. Returns DataFrame: form, count, pct."""
    n = nt_noun_data(book)
    return _count_profile(n['case_'].dropna(), CASE_ORDER)


def nt_noun_gender_profile(book: str | None = None) -> pd.DataFrame:
    """Gender distribution across GNT nouns. Returns DataFrame: form, count, pct."""
    n = nt_noun_data(book)
    return _count_profile(n['gender'].dropna(), GENDER_ORDER)


def nt_noun_number_profile(book: str | None = None) -> pd.DataFrame:
    """Number distribution across GNT nouns. Returns DataFrame: form, count, pct."""
    n = nt_noun_data(book)
    return _count_profile(n['number'].dropna(), NUMBER_ORDER)


def nt_noun_case_gender(book: str | None = None) -> pd.DataFrame:
    """Case × gender crosstab (counts)."""
    n = nt_noun_data(book)
    sub = n[n['case_'].notna() & n['gender'].notna()].copy()
    sub['case_'] = sub['case_'].str.lower()
    sub['gender'] = sub['gender'].str.lower()
    ct = pd.crosstab(sub['case_'], sub['gender'])
    ct = ct.reindex(
        index=[c for c in CASE_ORDER if c in ct.index],
        columns=[g for g in GENDER_ORDER if g in ct.columns],
        fill_value=0,
    )
    return ct


def nt_noun_top_lemmas(n: int = 30, book: str | None = None) -> pd.DataFrame:
    """Top-n most frequent noun lemmas. Columns: lemma, strong_g, count, pct, top_gloss."""
    nouns = nt_noun_data(book)
    grp = nouns.groupby(['lemma', 'strong_g']).agg(
        count=('lemma', 'size'),
        top_gloss=('gloss', lambda x: x.value_counts().index[0] if len(x) else ''),
    ).reset_index().sort_values('count', ascending=False).head(n)
    total = grp['count'].sum()
    grp['pct'] = (grp['count'] / total * 100).round(1)
    return grp.reset_index(drop=True)


def nt_noun_lemma_case(lemmas: list[str] | None = None, top_n: int = 15) -> pd.DataFrame:
    """Lemma × case crosstab (counts). Pass a lemma list or get top-n by frequency."""
    nouns = nt_noun_data()
    if lemmas is None:
        lemmas = nouns['lemma'].value_counts().head(top_n).index.tolist()
    sub = nouns[nouns['lemma'].isin(lemmas) & nouns['case_'].notna()].copy()
    sub['case_'] = sub['case_'].str.lower()
    ct = pd.crosstab(sub['lemma'], sub['case_'])
    ct = ct.reindex(
        index=lemmas,
        columns=[c for c in CASE_ORDER if c in ct.columns],
        fill_value=0,
    )
    return ct


def nt_noun_book_distribution() -> pd.DataFrame:
    """Noun token count and % per NT book. Columns: book, count, pct, pct_of_book_words."""
    df = load_syntax()
    nouns = df[df['class_'] == 'noun']
    book_counts = nouns['book'].value_counts().reset_index()
    book_counts.columns = ['book', 'count']
    total = book_counts['count'].sum()
    book_counts['pct'] = (book_counts['count'] / total * 100).round(1)

    all_words = df['book'].value_counts().reset_index()
    all_words.columns = ['book', 'total_words']
    book_counts = book_counts.merge(all_words, on='book', how='left')
    book_counts['pct_of_book_words'] = (
        book_counts['count'] / book_counts['total_words'] * 100
    ).round(1)

    order_map = {b: i for i, b in enumerate(NT_BOOK_ORDER)}
    book_counts['_ord'] = book_counts['book'].map(order_map).fillna(99)
    return book_counts.sort_values('_ord').drop(columns='_ord').reset_index(drop=True)


def nt_noun_genre_profile() -> pd.DataFrame:
    """Case % breakdown by NT genre group. Rows=genre, cols=cases."""
    df = load_syntax()
    nouns = df[df['class_'] == 'noun'].copy()
    nouns['case_'] = nouns['case_'].str.lower()
    rows = []
    for genre, books in NT_BOOK_GROUPS.items():
        sub = nouns[nouns['book'].isin(books) & nouns['case_'].notna()]
        total = len(sub)
        row: dict = {'genre': genre}
        for c in CASE_ORDER:
            cnt = (sub['case_'] == c).sum()
            row[c] = round(cnt / total * 100, 1) if total else 0.0
        row['total'] = total
        rows.append(row)
    return pd.DataFrame(rows).set_index('genre')


def nt_article_stats(book: str | None = None) -> pd.DataFrame:
    """Article (ὁ/ἡ/τό) vs anarthrous count per case.
    Returns DataFrame: case, with_article, without_article, pct_articular."""
    df = load_syntax()
    if book:
        df = df[df['book'] == book]
    nouns = df[df['class_'] == 'noun'].copy()
    nouns['case_'] = nouns['case_'].str.lower()

    # Build a set of token positions that immediately follow an article
    # The definite article in MACULA has strong G3588
    articles = df[df['strong'] == '3588'][['book', 'chapter', 'verse', 'word_num']].copy()
    art_positions = set(
        zip(articles['book'], articles['chapter'], articles['verse'], articles['word_num'])
    )

    nouns['prev_pos'] = list(zip(
        nouns['book'], nouns['chapter'], nouns['verse'], nouns['word_num'] - 1
    ))
    nouns['has_article'] = nouns['prev_pos'].isin(art_positions)

    rows = []
    for case in CASE_ORDER:
        sub = nouns[nouns['case_'] == case]
        total = len(sub)
        with_art = sub['has_article'].sum()
        without_art = total - with_art
        rows.append({
            'case': case,
            'with_article': int(with_art),
            'without_article': int(without_art),
            'total': total,
            'pct_articular': round(with_art / total * 100, 1) if total else 0.0,
        })
    return pd.DataFrame(rows)


# ── Print functions ───────────────────────────────────────────────────────────

def print_nt_noun_overview() -> None:
    """Print a statistical overview of GNT noun morphology."""
    df = load_syntax()
    nouns = df[df['class_'] == 'noun']
    total = len(nouns)
    total_words = len(df)
    unique_lemmas = nouns['lemma'].nunique()

    print()
    print('╔' + '═' * 78 + '╗')
    print('║' + '  Greek NT Noun Morphology — Overview'.center(78) + '║')
    print('╚' + '═' * 78 + '╝')
    print()
    print(f"  Total GNT noun tokens:      {total:>7,}")
    print(f"  % of all GNT words:         {total/total_words*100:>7.1f}%")
    print(f"  Unique noun lemmas:         {unique_lemmas:>7,}")
    print()

    print("  Case distribution:")
    for _, row in nt_noun_case_profile().iterrows():
        if row['count'] > 0:
            bar = '█' * int(row['pct'] / 2)
            print(f"    {row['form']:<12} {row['count']:>6,}  ({row['pct']:>5.1f}%)  {bar}")
    print()
    print("  Gender distribution:")
    for _, row in nt_noun_gender_profile().iterrows():
        if row['count'] > 0:
            bar = '█' * int(row['pct'] / 2)
            print(f"    {row['form']:<12} {row['count']:>6,}  ({row['pct']:>5.1f}%)  {bar}")
    print()


def _print_profile(label: str, df: pd.DataFrame) -> None:
    total = df['count'].sum()
    print()
    print('═' * 72)
    print(f"  {label}  (total: {total:,})")
    print('─' * 72)
    for _, row in df.iterrows():
        if row['count'] == 0:
            continue
        bar = '█' * int(row['pct'] / 2)
        print(f"  {row['form']:<14} {row['count']:>6,}  {row['pct']:>5.1f}%  {bar}")
    print()


def print_nt_noun_case(book: str | None = None) -> None:
    scope = book or 'Whole GNT'
    _print_profile(f"GNT noun case distribution — {scope}", nt_noun_case_profile(book))


def print_nt_noun_gender(book: str | None = None) -> None:
    scope = book or 'Whole GNT'
    _print_profile(f"GNT noun gender distribution — {scope}", nt_noun_gender_profile(book))


def print_nt_noun_case_gender(book: str | None = None) -> None:
    ct = nt_noun_case_gender(book)
    scope = book or 'Whole GNT'
    print()
    print('═' * 60)
    print(f"  Noun case × gender — {scope}")
    print('─' * 60)
    header = f"  {'Case':<14}" + ''.join(f"{g:>12}" for g in ct.columns)
    print(header)
    print('  ' + '─' * 56)
    for case, row in ct.iterrows():
        vals = ''.join(f"{v:>12,}" for v in row)
        print(f"  {case:<14}{vals}")
    print()


def print_nt_noun_top_lemmas(n: int = 20, book: str | None = None) -> None:
    df = nt_noun_top_lemmas(n, book)
    scope = book or 'Whole GNT'
    print()
    print('═' * 76)
    print(f"  Top {n} GNT noun lemmas — {scope}")
    print('─' * 76)
    print(f"  {'#':<4} {'Lemma':<20} {'Strong':>7} {'Count':>7} {'%':>6}  Gloss")
    print('  ' + '─' * 72)
    for i, row in df.iterrows():
        print(f"  {i+1:<4} {row['lemma']:<20} {row['strong_g']:>7} {row['count']:>7,} "
              f"{row['pct']:>5.1f}%  {row['top_gloss']}")
    print()


def print_nt_noun_genre_profile() -> None:
    df = nt_noun_genre_profile()
    print()
    print('═' * 80)
    print("  GNT noun case % by genre group")
    print('─' * 80)
    header = f"  {'Genre':<20}" + ''.join(f"{c:>12}" for c in CASE_ORDER) + f"  {'Total':>8}"
    print(header)
    print('  ' + '─' * 76)
    for genre, row in df.iterrows():
        vals = ''.join(f"{row[c]:>11.1f}%" for c in CASE_ORDER if c in row.index)
        print(f"  {genre:<20}{vals}  {row['total']:>8,}")
    print()


def print_nt_noun_book_distribution() -> None:
    df = nt_noun_book_distribution()
    print()
    print('═' * 76)
    print("  GNT noun distribution across NT books")
    print('─' * 76)
    print(f"  {'Book':<8} {'Count':>7} {'% of GNT':>10} {'% of book':>10}  Bar")
    print('  ' + '─' * 72)
    for _, row in df.iterrows():
        bar = '█' * int(row['pct'] * 2)
        print(f"  {row['book']:<8} {row['count']:>7,} {row['pct']:>9.1f}% "
              f"{row['pct_of_book_words']:>9.1f}%  {bar}")
    print()


def print_nt_article_stats(book: str | None = None) -> None:
    df = nt_article_stats(book)
    scope = book or 'Whole GNT'
    print()
    print('═' * 72)
    print(f"  Article vs. anarthrous nouns by case — {scope}")
    print('─' * 72)
    print(f"  {'Case':<14} {'Articular':>10} {'Anarthrous':>12} {'Total':>8} {'% Articular':>13}")
    print('  ' + '─' * 68)
    for _, row in df.iterrows():
        print(f"  {row['case']:<14} {row['with_article']:>10,} {row['without_article']:>12,} "
              f"{row['total']:>8,} {row['pct_articular']:>12.1f}%")
    print()


# ── Chart functions ───────────────────────────────────────────────────────────

def nt_noun_case_chart(book: str | None = None) -> Path | None:
    """Horizontal bar chart of case distribution."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_noun_case_profile(book)
    df = df[df['count'] > 0].sort_values('pct')
    scope = book or 'Whole GNT'

    fig, ax = plt.subplots(figsize=(9, 4))
    colors = plt.cm.Oranges([0.4 + 0.5 * i / max(len(df) - 1, 1) for i in range(len(df))])  # type: ignore[attr-defined]
    bars = ax.barh(df['form'], df['pct'], color=colors)
    for bar, val in zip(bars, df['pct']):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va='center', fontsize=9)
    ax.set_title(f"GNT Noun Case Distribution — {scope}", fontsize=13, fontweight='bold')
    ax.set_xlabel("% of noun tokens")
    ax.set_xlim(0, df['pct'].max() * 1.2)
    ax.xaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()

    out = _ensure_chart_dir() / f'nt_noun_case{"_"+book if book else ""}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def nt_noun_gender_chart(book: str | None = None) -> Path | None:
    """Bar chart of gender distribution."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_noun_gender_profile(book)
    df = df[df['count'] > 0]
    scope = book or 'Whole GNT'

    fig, ax = plt.subplots(figsize=(7, 3.5))
    colors = ['#1565C0', '#C62828', '#558B2F']
    ax.bar(df['form'], df['pct'], color=colors[:len(df)])
    for i, (_, row) in enumerate(df.iterrows()):
        ax.text(i, row['pct'] + 0.5, f"{row['pct']:.1f}%", ha='center', fontsize=10)
    ax.set_title(f"GNT Noun Gender Distribution — {scope}", fontsize=13, fontweight='bold')
    ax.set_ylabel("% of noun tokens")
    ax.set_ylim(0, df['pct'].max() * 1.2)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()

    out = _ensure_chart_dir() / f'nt_noun_gender{"_"+book if book else ""}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def nt_noun_genre_heatmap() -> Path | None:
    """Heatmap of case % by NT genre group."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_noun_genre_profile()
    cases = [c for c in CASE_ORDER if c in df.columns]
    data = df[cases].values.astype(float)

    fig, ax = plt.subplots(figsize=(9, 3.5))
    im = ax.imshow(data, cmap='YlOrRd', aspect='auto', vmin=0, vmax=data.max())
    ax.set_xticks(range(len(cases)))
    ax.set_xticklabels(cases, fontsize=11)
    ax.set_yticks(range(len(df.index)))
    ax.set_yticklabels(df.index.tolist(), fontsize=11)
    for i in range(len(df.index)):
        for j in range(len(cases)):
            val = data[i, j]
            ax.text(j, i, f"{val:.1f}%", ha='center', va='center',
                    fontsize=10, color='black' if val < 25 else 'white')
    plt.colorbar(im, ax=ax, label='% of genre noun tokens')
    ax.set_title("GNT Noun Case Distribution by Genre", fontsize=13, fontweight='bold')
    fig.tight_layout()

    out = _ensure_chart_dir() / 'nt_noun_genre_heatmap.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def nt_noun_case_gender_heatmap(book: str | None = None) -> Path | None:
    """Heatmap of case × gender (counts)."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    ct = nt_noun_case_gender(book)
    scope = book or 'Whole GNT'

    fig, ax = plt.subplots(figsize=(7, 4))
    im = ax.imshow(ct.values.astype(float), cmap='Blues', aspect='auto')
    ax.set_xticks(range(len(ct.columns)))
    ax.set_xticklabels(ct.columns.tolist(), fontsize=12)
    ax.set_yticks(range(len(ct.index)))
    ax.set_yticklabels(ct.index.tolist(), fontsize=11)
    for i in range(len(ct.index)):
        for j in range(len(ct.columns)):
            val = ct.values[i, j]
            if val > 0:
                ax.text(j, i, f"{val:,}", ha='center', va='center',
                        fontsize=9, color='black' if val < ct.values.max() * 0.6 else 'white')
    plt.colorbar(im, ax=ax, label='token count')
    ax.set_title(f"GNT Noun Case × Gender — {scope}", fontsize=12, fontweight='bold')
    fig.tight_layout()

    out = _ensure_chart_dir() / f'nt_noun_case_gender{"_"+book if book else ""}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def nt_noun_book_chart() -> Path | None:
    """Bar chart of noun counts across NT books."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_noun_book_distribution()
    fig, ax1 = plt.subplots(figsize=(14, 5))
    x = range(len(df))
    ax1.bar(x, df['count'], color='darkorange', alpha=0.8, label='noun count')
    ax1.set_ylabel('Noun token count', color='darkorange')
    ax1.tick_params(axis='y', labelcolor='darkorange')

    ax2 = ax1.twinx()
    ax2.plot(x, df['pct_of_book_words'], 'o-', color='steelblue',
             linewidth=1.8, markersize=5, label='% of book words')
    ax2.set_ylabel('% of book words', color='steelblue')
    ax2.tick_params(axis='y', labelcolor='steelblue')

    ax1.set_xticks(list(x))
    ax1.set_xticklabels(df['book'].tolist(), rotation=40, ha='right', fontsize=9)
    ax1.set_title("GNT Noun Distribution Across NT Books", fontsize=13, fontweight='bold')
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    fig.tight_layout()

    out = _ensure_chart_dir() / 'nt_noun_books.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out
