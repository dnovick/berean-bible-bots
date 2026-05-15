"""
Greek NT verb morphology profile.

Provides tense × voice × mood statistics across the GNT, paralleling the
Hebrew stem notebooks (qal.py, niphal.py, etc.) but operating on the MACULA
Greek syntax layer instead of the OT data.

Public API
──────────
nt_verb_data()                          → DataFrame (all GNT verb tokens)
nt_verb_tense_profile(book=None)        → DataFrame (tense distribution)
nt_verb_voice_profile(book=None)        → DataFrame (voice distribution)
nt_verb_mood_profile(book=None)         → DataFrame (mood distribution)
nt_verb_tense_voice(book=None)          → DataFrame (tense × voice crosstab)
nt_verb_tense_mood(book=None)           → DataFrame (tense × mood crosstab)
nt_verb_top_lemmas(n=30, book=None)     → DataFrame (most frequent verb lemmas)
nt_verb_lemma_tense(lemmas=None)        → DataFrame (lemma × tense crosstab)
nt_verb_book_distribution()             → DataFrame (count + pct per NT book)
nt_verb_genre_profile()                 → DataFrame (tense % by genre group)

print_nt_verb_overview()                → None
print_nt_verb_tense(book=None)          → None
print_nt_verb_voice(book=None)          → None
print_nt_verb_mood(book=None)           → None
print_nt_verb_tense_voice(book=None)    → None
print_nt_verb_top_lemmas(n=20)          → None
print_nt_verb_genre_profile()           → None
print_nt_verb_book_distribution()       → None

nt_verb_tense_chart(book=None)          → Path | None
nt_verb_voice_chart(book=None)          → Path | None
nt_verb_mood_chart(book=None)           → Path | None
nt_verb_genre_heatmap()                 → Path | None
nt_verb_book_chart()                    → Path | None
nt_verb_tense_voice_heatmap(book=None)  → Path | None
"""

from __future__ import annotations
from pathlib import Path

import pandas as pd

from ..core.syntax import load_syntax

# ── Book groups ───────────────────────────────────────────────────────────────

NT_BOOK_GROUPS: dict[str, list[str]] = {
    'Gospels & Acts': ['Mat', 'Mrk', 'Luk', 'Jhn', 'Act'],
    'Pauline':        ['Rom', '1Co', '2Co', 'Gal', 'Eph', 'Php', 'Col',
                       '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm'],
    'General & Rev':  ['Heb', 'Jas', '1Pe', '2Pe', '1Jn', '2Jn', '3Jn', 'Jud', 'Rev'],
}

NT_BOOK_ORDER: list[str] = [
    'Mat', 'Mrk', 'Luk', 'Jhn', 'Act',
    'Rom', '1Co', '2Co', 'Gal', 'Eph', 'Php', 'Col', '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm',
    'Heb', 'Jas', '1Pe', '2Pe', '1Jn', '2Jn', '3Jn', 'Jud', 'Rev',
]

TENSE_ORDER = ['present', 'imperfect', 'future', 'aorist', 'perfect', 'pluperfect']
VOICE_ORDER = ['active', 'middle', 'passive']
MOOD_ORDER  = ['indicative', 'subjunctive', 'optative', 'imperative', 'infinitive', 'participle']

_CHART_DIR = Path('output') / 'charts' / 'nt' / 'verbs'

# ── Data loading ──────────────────────────────────────────────────────────────


def nt_verb_data(book: str | None = None) -> pd.DataFrame:
    """All GNT verb tokens with morphological columns, optionally filtered to one book."""
    df = load_syntax()
    verbs = df[df['class_'] == 'verb'].copy()
    if book:
        verbs = verbs[verbs['book'] == book]
    return verbs


# ── Profile functions ─────────────────────────────────────────────────────────

def _count_profile(series: pd.Series, order: list[str]) -> pd.DataFrame:
    vc = series.str.lower().value_counts()
    total = vc.sum()
    records = []
    for form in order:
        cnt = int(vc.get(form, 0))
        records.append({'form': form, 'count': cnt,
                        'pct': round(cnt / total * 100, 1) if total else 0.0})
    # include any values not in our order list
    for form, cnt in vc.items():
        if str(form).lower() not in order:
            records.append({'form': str(form), 'count': int(cnt),
                            'pct': round(int(cnt) / total * 100, 1) if total else 0.0})
    return pd.DataFrame(records)


def nt_verb_tense_profile(book: str | None = None) -> pd.DataFrame:
    """Count verb tokens by tense. Returns DataFrame: form, count, pct."""
    v = nt_verb_data(book)
    return _count_profile(v['tense'].dropna(), TENSE_ORDER)


def nt_verb_voice_profile(book: str | None = None) -> pd.DataFrame:
    """Count verb tokens by voice. Returns DataFrame: form, count, pct."""
    v = nt_verb_data(book)
    return _count_profile(v['voice'].dropna(), VOICE_ORDER)


def nt_verb_mood_profile(book: str | None = None) -> pd.DataFrame:
    """Count verb tokens by mood. Returns DataFrame: form, count, pct."""
    v = nt_verb_data(book)
    return _count_profile(v['mood'].dropna(), MOOD_ORDER)


def nt_verb_tense_voice(book: str | None = None) -> pd.DataFrame:
    """Tense × voice crosstab (counts)."""
    v = nt_verb_data(book)
    sub = v[v['tense'].notna() & v['voice'].notna()].copy()
    sub['tense'] = sub['tense'].str.lower()
    sub['voice'] = sub['voice'].str.lower()
    ct = pd.crosstab(sub['tense'], sub['voice'])
    ct = ct.reindex(index=[t for t in TENSE_ORDER if t in ct.index],
                    columns=[c for c in VOICE_ORDER if c in ct.columns], fill_value=0)
    return ct


def nt_verb_tense_mood(book: str | None = None) -> pd.DataFrame:
    """Tense × mood crosstab (counts)."""
    v = nt_verb_data(book)
    sub = v[v['tense'].notna() & v['mood'].notna()].copy()
    sub['tense'] = sub['tense'].str.lower()
    sub['mood'] = sub['mood'].str.lower()
    ct = pd.crosstab(sub['tense'], sub['mood'])
    ct = ct.reindex(index=[t for t in TENSE_ORDER if t in ct.index],
                    columns=[m for m in MOOD_ORDER if m in ct.columns], fill_value=0)
    return ct


def nt_verb_top_lemmas(n: int = 30, book: str | None = None) -> pd.DataFrame:
    """Top-n most frequent verb lemmas. Columns: lemma, strong_g, count, pct, top_gloss."""
    v = nt_verb_data(book)
    grp = v.groupby(['lemma', 'strong_g']).agg(
        count=('lemma', 'size'),
        top_gloss=('gloss', lambda x: x.value_counts().index[0] if len(x) else ''),
    ).reset_index().sort_values('count', ascending=False).head(n)
    total = grp['count'].sum()
    grp['pct'] = (grp['count'] / total * 100).round(1)
    return grp.reset_index(drop=True)


def nt_verb_lemma_tense(lemmas: list[str] | None = None, top_n: int = 15) -> pd.DataFrame:
    """Lemma × tense crosstab (counts). Pass a lemma list or get top-n by frequency."""
    v = nt_verb_data()
    if lemmas is None:
        lemmas = v['lemma'].value_counts().head(top_n).index.tolist()
    sub = v[v['lemma'].isin(lemmas) & v['tense'].notna()].copy()
    sub['tense'] = sub['tense'].str.lower()
    ct = pd.crosstab(sub['lemma'], sub['tense'])
    ct = ct.reindex(index=lemmas,
                    columns=[t for t in TENSE_ORDER if t in ct.columns], fill_value=0)
    return ct


def nt_verb_book_distribution() -> pd.DataFrame:
    """Token count and % per NT book. Columns: book, count, pct, pct_of_book_words."""
    df = load_syntax()
    v = df[df['class_'] == 'verb']
    book_counts = v['book'].value_counts().reset_index()
    book_counts.columns = ['book', 'count']
    total = book_counts['count'].sum()
    book_counts['pct'] = (book_counts['count'] / total * 100).round(1)

    all_words = df['book'].value_counts().reset_index()
    all_words.columns = ['book', 'total_words']
    book_counts = book_counts.merge(all_words, on='book', how='left')
    book_counts['pct_of_book_words'] = (
        book_counts['count'] / book_counts['total_words'] * 100
    ).round(1)

    # Sort by canonical NT order
    order_map = {b: i for i, b in enumerate(NT_BOOK_ORDER)}
    book_counts['_ord'] = book_counts['book'].map(order_map).fillna(99)
    return book_counts.sort_values('_ord').drop(columns='_ord').reset_index(drop=True)


def nt_verb_genre_profile() -> pd.DataFrame:
    """Tense % breakdown by NT genre group. Rows=genre, cols=tenses."""
    df = load_syntax()
    v = df[df['class_'] == 'verb'].copy()
    v['tense'] = v['tense'].str.lower()
    rows = []
    for genre, books in NT_BOOK_GROUPS.items():
        sub = v[v['book'].isin(books) & v['tense'].notna()]
        total = len(sub)
        row: dict = {'genre': genre}
        for t in TENSE_ORDER:
            cnt = (sub['tense'] == t).sum()
            row[t] = round(cnt / total * 100, 1) if total else 0.0
        row['total'] = total
        rows.append(row)
    return pd.DataFrame(rows).set_index('genre')


# ── Print functions ───────────────────────────────────────────────────────────

def print_nt_verb_overview() -> None:
    """Print a quick statistical overview of GNT verb morphology."""
    df = load_syntax()
    v = df[df['class_'] == 'verb']
    total = len(v)
    total_words = len(df)
    unique_lemmas = v['lemma'].nunique()
    books_with = v['book'].nunique()

    print()
    print('╔' + '═' * 78 + '╗')
    print('║' + '  Greek NT Verb Morphology — Overview'.center(78) + '║')
    print('╚' + '═' * 78 + '╝')
    print()
    print(f"  Total GNT verb tokens:      {total:>7,}")
    print(f"  % of all GNT words:         {total/total_words*100:>7.1f}%")
    print(f"  Unique verb lemmas:         {unique_lemmas:>7,}")
    print(f"  Books containing verbs:     {books_with:>7,} of 27")
    print()

    print("  Tense distribution:")
    for _, row in nt_verb_tense_profile().iterrows():
        if row['count'] > 0:
            bar = '█' * int(row['pct'] / 2)
            print(f"    {row['form']:<12} {row['count']:>6,}  ({row['pct']:>5.1f}%)  {bar}")
    print()
    print("  Voice distribution:")
    for _, row in nt_verb_voice_profile().iterrows():
        if row['count'] > 0:
            bar = '█' * int(row['pct'] / 2)
            print(f"    {row['form']:<12} {row['count']:>6,}  ({row['pct']:>5.1f}%)  {bar}")
    print()
    print("  Mood distribution:")
    for _, row in nt_verb_mood_profile().iterrows():
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


def print_nt_verb_tense(book: str | None = None) -> None:
    scope = book or 'Whole GNT'
    _print_profile(f"Greek NT verb tense distribution — {scope}", nt_verb_tense_profile(book))


def print_nt_verb_voice(book: str | None = None) -> None:
    scope = book or 'Whole GNT'
    _print_profile(f"Greek NT verb voice distribution — {scope}", nt_verb_voice_profile(book))


def print_nt_verb_mood(book: str | None = None) -> None:
    scope = book or 'Whole GNT'
    _print_profile(f"Greek NT verb mood distribution — {scope}", nt_verb_mood_profile(book))


def print_nt_verb_tense_voice(book: str | None = None) -> None:
    ct = nt_verb_tense_voice(book)
    scope = book or 'Whole GNT'
    print()
    print('═' * 72)
    print(f"  Tense × Voice crosstab — {scope}")
    print('─' * 72)
    header = f"  {'Tense':<14}" + ''.join(f"{v:>10}" for v in ct.columns)
    print(header)
    print('  ' + '─' * 68)
    for tense, row in ct.iterrows():
        row_total = row.sum()
        vals = ''.join(f"{v:>10,}" for v in row)
        print(f"  {tense:<14}{vals}  ({row_total:,})")
    print()


def print_nt_verb_top_lemmas(n: int = 20, book: str | None = None) -> None:
    df = nt_verb_top_lemmas(n, book)
    scope = book or 'Whole GNT'
    print()
    print('═' * 76)
    print(f"  Top {n} GNT verb lemmas — {scope}")
    print('─' * 76)
    print(f"  {'#':<4} {'Lemma':<20} {'Strong':>7} {'Count':>7} {'%':>6}  Gloss")
    print('  ' + '─' * 72)
    for i, row in df.iterrows():
        print(f"  {i+1:<4} {row['lemma']:<20} {row['strong_g']:>7} {row['count']:>7,} "
              f"{row['pct']:>5.1f}%  {row['top_gloss']}")
    print()


def print_nt_verb_genre_profile() -> None:
    df = nt_verb_genre_profile()
    print()
    print('═' * 80)
    print("  GNT verb tense % by genre group")
    print('─' * 80)
    header = f"  {'Genre':<20}" + ''.join(f"{t:>10}" for t in TENSE_ORDER) + f"  {'Total':>8}"
    print(header)
    print('  ' + '─' * 76)
    for genre, row in df.iterrows():
        vals = ''.join(f"{row[t]:>9.1f}%" for t in TENSE_ORDER if t in row.index)
        print(f"  {genre:<20}{vals}  {row['total']:>8,}")
    print()


def print_nt_verb_book_distribution() -> None:
    df = nt_verb_book_distribution()
    print()
    print('═' * 76)
    print("  GNT verb distribution across NT books")
    print('─' * 76)
    print(f"  {'Book':<8} {'Count':>7} {'% of GNT':>10} {'% of book':>10}  Bar")
    print('  ' + '─' * 72)
    for _, row in df.iterrows():
        bar = '█' * int(row['pct'] * 2)
        print(f"  {row['book']:<8} {row['count']:>7,} {row['pct']:>9.1f}% "
              f"{row['pct_of_book_words']:>9.1f}%  {bar}")
    print()


# ── Chart functions ───────────────────────────────────────────────────────────

def _ensure_chart_dir() -> Path:
    _CHART_DIR.mkdir(parents=True, exist_ok=True)
    return _CHART_DIR


def nt_verb_tense_chart(book: str | None = None) -> Path | None:
    """Horizontal bar chart of tense distribution."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_verb_tense_profile(book)
    df = df[df['count'] > 0].sort_values('pct')
    scope = book or 'Whole GNT'

    fig, ax = plt.subplots(figsize=(9, 4))
    colors = plt.cm.Blues([0.4 + 0.5 * i / max(len(df) - 1, 1) for i in range(len(df))])  # type: ignore[attr-defined]
    bars = ax.barh(df['form'], df['pct'], color=colors)
    for bar, val in zip(bars, df['pct']):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va='center', fontsize=9)
    ax.set_title(f"GNT Verb Tense Distribution — {scope}", fontsize=13, fontweight='bold')
    ax.set_xlabel("% of verb tokens")
    ax.set_xlim(0, df['pct'].max() * 1.2)
    ax.xaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()

    out = _ensure_chart_dir() / f'nt_verb_tense{"_"+book if book else ""}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def nt_verb_voice_chart(book: str | None = None) -> Path | None:
    """Bar chart of voice distribution."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_verb_voice_profile(book)
    df = df[df['count'] > 0]
    scope = book or 'Whole GNT'

    fig, ax = plt.subplots(figsize=(7, 3.5))
    colors = ['#1565C0', '#E65100', '#2E7D32']
    ax.bar(df['form'], df['pct'], color=colors[:len(df)])
    for i, (_, row) in enumerate(df.iterrows()):
        ax.text(i, row['pct'] + 0.5, f"{row['pct']:.1f}%", ha='center', fontsize=10)
    ax.set_title(f"GNT Verb Voice Distribution — {scope}", fontsize=13, fontweight='bold')
    ax.set_ylabel("% of verb tokens")
    ax.set_ylim(0, df['pct'].max() * 1.2)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()

    out = _ensure_chart_dir() / f'nt_verb_voice{"_"+book if book else ""}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def nt_verb_mood_chart(book: str | None = None) -> Path | None:
    """Horizontal bar chart of mood distribution."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_verb_mood_profile(book)
    df = df[df['count'] > 0].sort_values('pct')
    scope = book or 'Whole GNT'

    fig, ax = plt.subplots(figsize=(9, 4))
    colors = plt.cm.Greens([0.35 + 0.5 * i / max(len(df) - 1, 1) for i in range(len(df))])  # type: ignore[attr-defined]
    bars = ax.barh(df['form'], df['pct'], color=colors)
    for bar, val in zip(bars, df['pct']):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va='center', fontsize=9)
    ax.set_title(f"GNT Verb Mood Distribution — {scope}", fontsize=13, fontweight='bold')
    ax.set_xlabel("% of verb tokens")
    ax.set_xlim(0, df['pct'].max() * 1.2)
    ax.xaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()

    out = _ensure_chart_dir() / f'nt_verb_mood{"_"+book if book else ""}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def nt_verb_genre_heatmap() -> Path | None:
    """Heatmap of tense % by NT genre group."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_verb_genre_profile()
    tenses = [t for t in TENSE_ORDER if t in df.columns]
    data = df[tenses].values.astype(float)

    fig, ax = plt.subplots(figsize=(10, 3.5))
    im = ax.imshow(data, cmap='YlOrRd', aspect='auto', vmin=0, vmax=data.max())
    ax.set_xticks(range(len(tenses)))
    ax.set_xticklabels(tenses, fontsize=11)
    ax.set_yticks(range(len(df.index)))
    ax.set_yticklabels(df.index.tolist(), fontsize=11)
    for i in range(len(df.index)):
        for j in range(len(tenses)):
            val = data[i, j]
            ax.text(j, i, f"{val:.1f}%", ha='center', va='center',
                    fontsize=10, color='black' if val < 25 else 'white')
    plt.colorbar(im, ax=ax, label='% of genre verb tokens')
    ax.set_title("GNT Verb Tense Distribution by Genre", fontsize=13, fontweight='bold')
    fig.tight_layout()

    out = _ensure_chart_dir() / 'nt_verb_genre_heatmap.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def nt_verb_book_chart() -> Path | None:
    """Bar chart of verb counts across NT books."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_verb_book_distribution()
    fig, ax1 = plt.subplots(figsize=(14, 5))
    x = range(len(df))
    ax1.bar(x, df['count'], color='steelblue', alpha=0.8, label='verb count')
    ax1.set_ylabel('Verb token count', color='steelblue')
    ax1.tick_params(axis='y', labelcolor='steelblue')

    ax2 = ax1.twinx()
    ax2.plot(x, df['pct_of_book_words'], 'o-', color='darkorange',
             linewidth=1.8, markersize=5, label='% of book words')
    ax2.set_ylabel('% of book words', color='darkorange')
    ax2.tick_params(axis='y', labelcolor='darkorange')

    ax1.set_xticks(list(x))
    ax1.set_xticklabels(df['book'].tolist(), rotation=40, ha='right', fontsize=9)
    ax1.set_title("GNT Verb Distribution Across NT Books", fontsize=13, fontweight='bold')
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    fig.tight_layout()

    out = _ensure_chart_dir() / 'nt_verb_books.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def nt_verb_tense_voice_heatmap(book: str | None = None) -> Path | None:
    """Heatmap of tense × voice (counts)."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    ct = nt_verb_tense_voice(book)
    scope = book or 'Whole GNT'

    fig, ax = plt.subplots(figsize=(7, 5))
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
    ax.set_title(f"GNT Verb Tense × Voice — {scope}", fontsize=12, fontweight='bold')
    fig.tight_layout()

    out = _ensure_chart_dir() / f'nt_verb_tense_voice{"_"+book if book else ""}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out
