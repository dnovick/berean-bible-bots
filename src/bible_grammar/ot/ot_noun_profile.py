"""
Hebrew OT noun morphology profile.

Provides state (absolute/construct/determined), gender, number, and article
usage statistics across the Hebrew Bible, backed by the MACULA Hebrew WLC dataset.
All functions filter to lang='H' (Hebrew) unless otherwise noted.

Public API
──────────
ot_noun_data(book=None)                   → DataFrame (all Hebrew noun tokens)
ot_adj_data(book=None)                    → DataFrame (all Hebrew adjective tokens)
ot_noun_gender_profile(book=None)         → DataFrame (gender distribution)
ot_noun_number_profile(book=None)         → DataFrame (number distribution)
ot_noun_state_profile(book=None)          → DataFrame (state distribution)
ot_noun_gender_state(book=None)           → DataFrame (gender × state crosstab)
ot_noun_top_lemmas(n=30, book=None)       → DataFrame (most frequent noun lemmas)
ot_noun_lemma_state(lemmas=None, top_n=15)→ DataFrame (lemma × state crosstab)
ot_noun_book_distribution()               → DataFrame (count + pct per OT book)
ot_noun_genre_profile()                   → DataFrame (state % by genre group)
ot_article_usage(book=None)               → DataFrame (article token stats)
ot_construct_top_lemmas(n=20, book=None)  → DataFrame (top construct-state nouns)

print_ot_noun_overview()                  → None
print_ot_noun_gender(book=None)           → None
print_ot_noun_state(book=None)            → None
print_ot_noun_top_lemmas(n=20, book=None) → None
print_ot_construct_top_lemmas(n=20, book=None) → None
print_ot_noun_genre_profile()             → None
print_ot_noun_book_distribution()         → None
print_ot_article_usage(book=None)         → None

ot_noun_state_chart(book=None)            → Path | None
ot_noun_gender_chart(book=None)           → Path | None
ot_noun_genre_heatmap()                   → Path | None
ot_noun_book_chart()                      → Path | None
"""

from __future__ import annotations
from pathlib import Path

import pandas as pd

from ..core._utils import load_ot_data

STATE_ORDER  = ['absolute', 'construct', 'determined']
GENDER_ORDER = ['masculine', 'feminine']
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

_CHART_DIR = Path('output') / 'charts' / 'ot' / 'nouns'


def _ensure_chart_dir() -> Path:
    _CHART_DIR.mkdir(parents=True, exist_ok=True)
    return _CHART_DIR


def _count_profile(series: pd.Series, order: list[str]) -> pd.DataFrame:
    vals = series[series.str.len() > 0]
    vc = vals.str.lower().value_counts()
    total = vc.sum()
    records = []
    for form in order:
        cnt = int(vc.get(form, 0))
        records.append({'form': form, 'count': cnt,
                        'pct': round(cnt / total * 100, 1) if total else 0.0})
    for form, cnt in vc.items():
        if str(form).lower() not in order and int(cnt) > 0:
            records.append({'form': str(form), 'count': int(cnt),
                            'pct': round(int(cnt) / total * 100, 1) if total else 0.0})
    return pd.DataFrame(records)


# ── Data loading ──────────────────────────────────────────────────────────────

def ot_noun_data(book: str | None = None) -> pd.DataFrame:
    """All Hebrew noun tokens (class_='noun', lang='H'), optionally filtered to one book."""
    df = load_ot_data()
    nouns = df[(df['class_'] == 'noun') & (df['lang'] == 'H')].copy()
    if book:
        nouns = nouns[nouns['book'] == book]
    return nouns


def ot_adj_data(book: str | None = None) -> pd.DataFrame:
    """All Hebrew adjective tokens (class_='adj', lang='H')."""
    df = load_ot_data()
    adjs = df[(df['class_'] == 'adj') & (df['lang'] == 'H')].copy()
    if book:
        adjs = adjs[adjs['book'] == book]
    return adjs


# ── Profile functions ─────────────────────────────────────────────────────────

def ot_noun_gender_profile(book: str | None = None) -> pd.DataFrame:
    """Gender distribution across Hebrew nouns. Returns DataFrame: form, count, pct."""
    n = ot_noun_data(book)
    return _count_profile(n['gender'].fillna(''), GENDER_ORDER)


def ot_noun_number_profile(book: str | None = None) -> pd.DataFrame:
    """Number distribution across Hebrew nouns. Returns DataFrame: form, count, pct."""
    n = ot_noun_data(book)
    return _count_profile(n['number'].fillna(''), NUMBER_ORDER)


def ot_noun_state_profile(book: str | None = None) -> pd.DataFrame:
    """State distribution (absolute/construct/determined). Returns DataFrame: form, count, pct."""
    n = ot_noun_data(book)
    return _count_profile(n['state'].fillna(''), STATE_ORDER)


def ot_noun_gender_state(book: str | None = None) -> pd.DataFrame:
    """Gender × state crosstab (counts)."""
    n = ot_noun_data(book)
    sub = n[n['gender'].notna() & n['state'].notna() &
            (n['gender'] != '') & (n['state'] != '')].copy()
    sub['gender'] = sub['gender'].str.lower()
    sub['state'] = sub['state'].str.lower()
    ct = pd.crosstab(sub['gender'], sub['state'])
    ct = ct.reindex(
        index=[g for g in GENDER_ORDER if g in ct.index],
        columns=[s for s in STATE_ORDER if s in ct.columns],
        fill_value=0,
    )
    return ct


def ot_noun_top_lemmas(n: int = 30, book: str | None = None) -> pd.DataFrame:
    """Top-n most frequent Hebrew noun lemmas. Columns: lemma, count, pct, top_gloss."""
    nouns = ot_noun_data(book)
    grp = nouns.groupby('lemma').agg(
        count=('lemma', 'size'),
        top_gloss=('english', lambda x: x.value_counts().index[0] if len(x) else ''),
        top_state=('state', lambda x: x.value_counts().index[0] if len(x) else ''),
    ).reset_index().sort_values('count', ascending=False).head(n)
    total = grp['count'].sum()
    grp['pct'] = (grp['count'] / total * 100).round(1)
    return grp.reset_index(drop=True)


def ot_noun_lemma_state(lemmas: list[str] | None = None,
                        top_n: int = 15) -> pd.DataFrame:
    """Lemma × state crosstab. Pass a lemma list or get top-n by frequency."""
    nouns = ot_noun_data()
    if lemmas is None:
        lemmas = nouns['lemma'].value_counts().head(top_n).index.tolist()
    sub = nouns[nouns['lemma'].isin(lemmas) &
                nouns['state'].notna() & (nouns['state'] != '')].copy()
    sub['state'] = sub['state'].str.lower()
    ct = pd.crosstab(sub['lemma'], sub['state'])
    present_states = [s for s in STATE_ORDER if s in ct.columns]
    ct = ct.reindex(index=lemmas, columns=present_states, fill_value=0)
    return ct


def ot_noun_book_distribution() -> pd.DataFrame:
    """Noun token count and % per OT book (Hebrew only). Includes % of book words."""
    df = load_ot_data()
    h_df = df[df['lang'] == 'H']
    nouns = h_df[h_df['class_'] == 'noun']

    book_counts = nouns['book'].value_counts().reset_index()
    book_counts.columns = ['book', 'count']
    total = book_counts['count'].sum()
    book_counts['pct'] = (book_counts['count'] / total * 100).round(1)

    all_words = h_df['book'].value_counts().reset_index()
    all_words.columns = ['book', 'total_words']
    book_counts = book_counts.merge(all_words, on='book', how='left')
    book_counts['pct_of_book_words'] = (
        book_counts['count'] / book_counts['total_words'] * 100
    ).round(1)

    order_map = {b: i for i, b in enumerate(OT_BOOK_ORDER)}
    book_counts['_ord'] = book_counts['book'].map(order_map).fillna(99)
    return book_counts.sort_values('_ord').drop(columns='_ord').reset_index(drop=True)


def ot_noun_genre_profile() -> pd.DataFrame:
    """State % breakdown by OT genre group. Rows=genre, cols=states."""
    df = load_ot_data()
    nouns = df[(df['class_'] == 'noun') & (df['lang'] == 'H')].copy()
    nouns['state'] = nouns['state'].fillna('').str.lower()
    rows = []
    for genre, books in OT_BOOK_GROUPS.items():
        sub = nouns[nouns['book'].isin(books) & (nouns['state'] != '')]
        total = len(sub)
        row: dict = {'genre': genre}
        for s in STATE_ORDER:
            cnt = (sub['state'] == s).sum()
            row[s] = round(cnt / total * 100, 1) if total else 0.0
        row['total'] = total
        rows.append(row)
    return pd.DataFrame(rows).set_index('genre')


def ot_article_usage(book: str | None = None) -> pd.DataFrame:
    """Article token (class_='art') counts vs. noun counts by genre or single book.

    In Hebrew the definite article ה attaches to the following word (noun, adj,
    participle). MACULA WLC represents it as a separate class_='art' token.
    Returns DataFrame: scope, nouns, articles, pct_articular.
    """
    df = load_ot_data()
    h_df = df[df['lang'] == 'H']

    if book:
        nouns_count = int((h_df[h_df['class_'] == 'noun']['book'] == book).sum())
        art_count   = int((h_df[h_df['class_'] == 'art']['book'] == book).sum())
        return pd.DataFrame([{
            'scope': book,
            'nouns': nouns_count,
            'articles': art_count,
            'pct_articular': round(art_count / nouns_count * 100, 1) if nouns_count else 0.0,
        }])

    rows = []
    for genre, books in OT_BOOK_GROUPS.items():
        sub = h_df[h_df['book'].isin(books)]
        nouns_count = int((sub['class_'] == 'noun').sum())
        art_count   = int((sub['class_'] == 'art').sum())
        rows.append({
            'scope': genre,
            'nouns': nouns_count,
            'articles': art_count,
            'pct_articular': round(art_count / nouns_count * 100, 1) if nouns_count else 0.0,
        })
    return pd.DataFrame(rows)


def ot_construct_top_lemmas(n: int = 20, book: str | None = None) -> pd.DataFrame:
    """Top-n noun lemmas that most frequently appear in the construct state."""
    nouns = ot_noun_data(book)
    constr = nouns[nouns['state'].str.lower() == 'construct']
    grp = constr.groupby('lemma').agg(
        construct_count=('lemma', 'size'),
        top_gloss=('english', lambda x: x.value_counts().index[0] if len(x) else ''),
    ).reset_index().sort_values('construct_count', ascending=False).head(n)
    # Also get total count for % in construct
    total_by_lemma = nouns.groupby('lemma').size().rename('total_count')
    grp = grp.merge(total_by_lemma, on='lemma', how='left')
    grp['pct_construct'] = (grp['construct_count'] / grp['total_count'] * 100).round(1)
    return grp.reset_index(drop=True)


# ── Print functions ───────────────────────────────────────────────────────────

def print_ot_noun_overview() -> None:
    """Print a statistical overview of Hebrew OT noun morphology."""
    df = load_ot_data()
    h_df = df[df['lang'] == 'H']
    nouns = h_df[h_df['class_'] == 'noun']
    total_words = len(h_df)
    total_nouns = len(nouns)
    unique_lemmas = nouns['lemma'].nunique()
    art_tokens = (h_df['class_'] == 'art').sum()

    print()
    print('╔' + '═' * 78 + '╗')
    print('║' + '  Hebrew OT Noun Morphology — Overview'.center(78) + '║')
    print('╚' + '═' * 78 + '╝')
    print()
    print(f"  Total Hebrew word tokens:   {total_words:>8,}")
    noun_pct = total_nouns / total_words * 100
    print(f"  Hebrew noun tokens:         {total_nouns:>8,}  ({noun_pct:.1f}% of words)")
    print(f"  Unique noun lemmas:         {unique_lemmas:>8,}")
    print(f"  Definite article tokens:    {art_tokens:>8,}")
    print()

    print("  State distribution (nouns):")
    for _, row in ot_noun_state_profile().iterrows():
        if row['count'] == 0:
            continue
        bar = '█' * int(row['pct'] / 2)
        print(f"    {row['form']:<14} {row['count']:>7,}  ({row['pct']:>5.1f}%)  {bar}")
    print()

    print("  Gender distribution (nouns):")
    for _, row in ot_noun_gender_profile().iterrows():
        if row['count'] == 0:
            continue
        bar = '█' * int(row['pct'] / 2)
        print(f"    {row['form']:<14} {row['count']:>7,}  ({row['pct']:>5.1f}%)  {bar}")
    print()

    print("  Number distribution (nouns):")
    for _, row in ot_noun_number_profile().iterrows():
        if row['count'] == 0:
            continue
        bar = '█' * int(row['pct'] / 2)
        print(f"    {row['form']:<14} {row['count']:>7,}  ({row['pct']:>5.1f}%)  {bar}")
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
        print(f"  {row['form']:<16} {row['count']:>7,}  {row['pct']:>5.1f}%  {bar}")
    print()


def print_ot_noun_gender(book: str | None = None) -> None:
    scope = book or 'Whole OT'
    _print_profile(f"Hebrew noun gender distribution — {scope}", ot_noun_gender_profile(book))


def print_ot_noun_state(book: str | None = None) -> None:
    scope = book or 'Whole OT'
    _print_profile(f"Hebrew noun state distribution — {scope}", ot_noun_state_profile(book))


def print_ot_noun_top_lemmas(n: int = 20, book: str | None = None) -> None:
    df = ot_noun_top_lemmas(n, book)
    scope = book or 'Whole OT'
    print()
    print('═' * 76)
    print(f"  Top {n} Hebrew noun lemmas — {scope}")
    print('─' * 76)
    print(f"  {'#':<4} {'Lemma':<22} {'Count':>7} {'%':>6}  {'Top state':<14} Gloss")
    print('  ' + '─' * 72)
    for i, row in df.iterrows():
        print(f"  {i+1:<4} {row['lemma']:<22} {row['count']:>7,} {row['pct']:>5.1f}%  "
              f"{row['top_state']:<14} {row['top_gloss']}")
    print()


def print_ot_construct_top_lemmas(n: int = 20, book: str | None = None) -> None:
    df = ot_construct_top_lemmas(n, book)
    scope = book or 'Whole OT'
    print()
    print('═' * 76)
    print(f"  Top {n} Hebrew nouns in construct state — {scope}")
    print('─' * 76)
    print(f"  {'#':<4} {'Lemma':<22} {'Construct':>10} {'Total':>8} {'% constr':>9}  Gloss")
    print('  ' + '─' * 72)
    for i, row in df.iterrows():
        print(f"  {i+1:<4} {row['lemma']:<22} {row['construct_count']:>10,} "
              f"{row['total_count']:>8,} {row['pct_construct']:>8.1f}%  {row['top_gloss']}")
    print()


def print_ot_noun_genre_profile() -> None:
    df = ot_noun_genre_profile()
    print()
    print('═' * 80)
    print("  Hebrew noun state % by OT genre group")
    print('─' * 80)
    header = f"  {'Genre':<14}" + ''.join(f"{s:>12}" for s in STATE_ORDER) + f"  {'Total':>8}"
    print(header)
    print('  ' + '─' * 76)
    for genre, row in df.iterrows():
        vals = ''.join(f"{row.get(s, 0.0):>11.1f}%" for s in STATE_ORDER)
        print(f"  {genre:<14}{vals}  {row['total']:>8,}")
    print()


def print_ot_noun_book_distribution() -> None:
    df = ot_noun_book_distribution()
    print()
    print('═' * 76)
    print("  Hebrew noun distribution across OT books")
    print('─' * 76)
    print(f"  {'Book':<8} {'Count':>7} {'% of OT':>9} {'% of book':>10}  Bar")
    print('  ' + '─' * 72)
    for _, row in df.iterrows():
        bar = '█' * int(row['pct'] * 1.5)
        print(f"  {row['book']:<8} {row['count']:>7,} {row['pct']:>8.1f}% "
              f"{row['pct_of_book_words']:>9.1f}%  {bar}")
    print()


def print_ot_article_usage(book: str | None = None) -> None:
    df = ot_article_usage(book)
    scope = book or 'OT by genre'
    print()
    print('═' * 72)
    print(f"  Hebrew definite article usage — {scope}")
    print('  (article tokens / noun tokens; article ה is a separate MACULA token)')
    print('─' * 72)
    print(f"  {'Scope':<14} {'Nouns':>8} {'Articles':>10} {'Art/Noun %':>12}")
    print('  ' + '─' * 68)
    for _, row in df.iterrows():
        print(f"  {row['scope']:<14} {row['nouns']:>8,} {row['articles']:>10,} "
              f"{row['pct_articular']:>11.1f}%")
    print()


# ── Chart functions ───────────────────────────────────────────────────────────

def ot_noun_state_chart(book: str | None = None) -> Path | None:
    """Horizontal bar chart of noun state distribution."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = ot_noun_state_profile(book)
    df = df[df['count'] > 0]
    scope = book or 'Whole OT'

    fig, ax = plt.subplots(figsize=(9, 4))
    colors = ['#1565C0', '#E65100', '#2E7D32'][:len(df)]
    bars = ax.barh(df['form'], df['pct'], color=colors)
    for bar, val in zip(bars, df['pct']):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va='center', fontsize=10)
    ax.set_title(f"Hebrew OT Noun State Distribution — {scope}", fontsize=13, fontweight='bold')
    ax.set_xlabel("% of noun tokens")
    ax.set_xlim(0, df['pct'].max() * 1.2)
    ax.xaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()

    out = _ensure_chart_dir() / f'ot_noun_state{"_"+book if book else ""}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def ot_noun_gender_chart(book: str | None = None) -> Path | None:
    """Bar chart of noun gender distribution."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = ot_noun_gender_profile(book)
    df = df[df['count'] > 0]
    scope = book or 'Whole OT'

    fig, ax = plt.subplots(figsize=(7, 3.5))
    colors = ['#1565C0', '#C62828']
    ax.bar(df['form'], df['pct'], color=colors[:len(df)])
    for i, (_, row) in enumerate(df.iterrows()):
        ax.text(i, row['pct'] + 0.5, f"{row['pct']:.1f}%", ha='center', fontsize=11)
    ax.set_title(f"Hebrew OT Noun Gender Distribution — {scope}", fontsize=13, fontweight='bold')
    ax.set_ylabel("% of noun tokens")
    ax.set_ylim(0, df['pct'].max() * 1.25)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()

    out = _ensure_chart_dir() / f'ot_noun_gender{"_"+book if book else ""}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def ot_noun_genre_heatmap() -> Path | None:
    """Heatmap of noun state % by OT genre group."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = ot_noun_genre_profile()
    states = [s for s in STATE_ORDER if s in df.columns]
    data = df[states].values.astype(float)

    fig, ax = plt.subplots(figsize=(8, 3.5))
    im = ax.imshow(data, cmap='YlOrRd', aspect='auto', vmin=0, vmax=data.max())
    ax.set_xticks(range(len(states)))
    ax.set_xticklabels(states, fontsize=12)
    ax.set_yticks(range(len(df.index)))
    ax.set_yticklabels(df.index.tolist(), fontsize=11)
    for i in range(len(df.index)):
        for j in range(len(states)):
            val = data[i, j]
            ax.text(j, i, f"{val:.1f}%", ha='center', va='center',
                    fontsize=11, color='black' if val < 25 else 'white')
    plt.colorbar(im, ax=ax, label='% of genre noun tokens')
    ax.set_title("Hebrew OT Noun State Distribution by Genre", fontsize=13, fontweight='bold')
    fig.tight_layout()

    out = _ensure_chart_dir() / 'ot_noun_genre_heatmap.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def ot_noun_book_chart() -> Path | None:
    """Bar + line chart of noun counts and % across OT books."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = ot_noun_book_distribution()
    fig, ax1 = plt.subplots(figsize=(16, 5))
    x = range(len(df))
    ax1.bar(x, df['count'], color='steelblue', alpha=0.8, label='noun count')
    ax1.set_ylabel('Noun token count', color='steelblue')
    ax1.tick_params(axis='y', labelcolor='steelblue')

    ax2 = ax1.twinx()
    ax2.plot(list(x), df['pct_of_book_words'].tolist(), 'o-', color='darkorange',
             linewidth=1.8, markersize=4, label='% of book words')
    ax2.set_ylabel('% of book words', color='darkorange')
    ax2.tick_params(axis='y', labelcolor='darkorange')

    ax1.set_xticks(list(x))
    ax1.set_xticklabels(df['book'].tolist(), rotation=45, ha='right', fontsize=8)
    ax1.set_title("Hebrew OT Noun Distribution Across Books", fontsize=13, fontweight='bold')
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    fig.tight_layout()

    out = _ensure_chart_dir() / 'ot_noun_books.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out
