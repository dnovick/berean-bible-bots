"""
Greek NT participle usage analysis.

Provides adverbial vs. adjectival participle classification, tense × voice
profiles, genitive absolute counts, perfect participle statistics, and
genre comparison for all participial tokens in the GNT.

Public API
──────────
nt_participle_data(book=None)             → DataFrame (all GNT participle tokens)
nt_participle_tense_profile(book=None)    → DataFrame (tense distribution)
nt_participle_voice_profile(book=None)    → DataFrame (voice distribution)
nt_participle_tense_voice(book=None)      → DataFrame (tense × voice crosstab)
nt_participle_role_profile(book=None)     → DataFrame (syntactic role counts)
nt_participle_top_lemmas(n=20, book=None) → DataFrame (most frequent ptc lemmas)
nt_participle_book_distribution()         → DataFrame (count + pct per NT book)
nt_participle_genre_profile()             → DataFrame (tense % by genre)
nt_genitive_absolutes(book=None)          → DataFrame (genitive absolute tokens)
nt_perfect_participles(book=None)         → DataFrame (perfect participle tokens)

print_nt_participle_overview()            → None
print_nt_participle_tense(book=None)      → None
print_nt_participle_voice(book=None)      → None
print_nt_participle_tense_voice(book=None)→ None
print_nt_participle_role(book=None)       → None
print_nt_participle_top_lemmas(n=20)      → None
print_nt_participle_genre_profile()       → None
print_nt_genitive_absolutes(book=None)    → None
print_nt_perfect_participles(n=20)        → None
print_nt_participle_book_distribution()   → None

nt_participle_tense_chart(book=None)      → Path | None
nt_participle_genre_heatmap()             → Path | None
nt_participle_book_chart()                → Path | None
"""

from __future__ import annotations
from pathlib import Path

import pandas as pd

from .syntax import load_syntax
from .nt_verb_profile import NT_BOOK_GROUPS, NT_BOOK_ORDER, TENSE_ORDER, VOICE_ORDER

_CHART_DIR = Path('output') / 'charts' / 'nt' / 'participles'


def _ensure_chart_dir() -> Path:
    _CHART_DIR.mkdir(parents=True, exist_ok=True)
    return _CHART_DIR


# ── Data loading ──────────────────────────────────────────────────────────────

def nt_participle_data(book: str | None = None) -> pd.DataFrame:
    """All GNT participle tokens (mood='participle'), optionally filtered to one book."""
    df = load_syntax()
    ptc = df[df['mood'].str.lower() == 'participle'].copy()
    if book:
        ptc = ptc[ptc['book'] == book]
    return ptc


# ── Profile functions ─────────────────────────────────────────────────────────

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


def nt_participle_tense_profile(book: str | None = None) -> pd.DataFrame:
    """Tense distribution for participles. Returns DataFrame: form, count, pct."""
    p = nt_participle_data(book)
    return _count_profile(p['tense'].dropna(), TENSE_ORDER)


def nt_participle_voice_profile(book: str | None = None) -> pd.DataFrame:
    """Voice distribution for participles. Returns DataFrame: form, count, pct."""
    p = nt_participle_data(book)
    return _count_profile(p['voice'].dropna(), VOICE_ORDER)


def nt_participle_tense_voice(book: str | None = None) -> pd.DataFrame:
    """Tense × voice crosstab for participles (counts)."""
    p = nt_participle_data(book)
    sub = p[p['tense'].notna() & p['voice'].notna()].copy()
    sub['tense'] = sub['tense'].str.lower()
    sub['voice'] = sub['voice'].str.lower()
    ct = pd.crosstab(sub['tense'], sub['voice'])
    ct = ct.reindex(
        index=[t for t in TENSE_ORDER if t in ct.index],
        columns=[v for v in VOICE_ORDER if v in ct.columns],
        fill_value=0,
    )
    return ct


def nt_participle_role_profile(book: str | None = None) -> pd.DataFrame:
    """Syntactic role distribution for participles.

    Roles from MACULA: 's' (subject), 'v' (verb/predicate), 'o' (object),
    'adv' (adverbial), 'p' (predicate), 'io' (indirect object), etc.
    Adverbial participles have role 'adv'; adjectival have role 'p' or attributive.
    """
    p = nt_participle_data(book)
    role_labels = {
        'adv':  'adverbial',
        'p':    'predicate / attributive',
        's':    'subject (substantival)',
        'o':    'object (substantival)',
        'v':    'main verb position',
        'io':   'indirect object',
        'vc':   'verb complement',
    }
    p2 = p.copy()
    p2['role_label'] = p2['role'].map(role_labels).fillna(p2['role'].fillna('unknown'))
    vc = p2['role_label'].value_counts().reset_index()
    vc.columns = ['role', 'count']
    total = vc['count'].sum()
    vc['pct'] = (vc['count'] / total * 100).round(1)
    return vc.sort_values('count', ascending=False).reset_index(drop=True)


def nt_participle_top_lemmas(n: int = 20, book: str | None = None) -> pd.DataFrame:
    """Top-n most frequent participle lemmas."""
    p = nt_participle_data(book)
    grp = p.groupby(['lemma', 'strong_g']).agg(
        count=('lemma', 'size'),
        top_tense=('tense', lambda x: x.value_counts().index[0] if len(x) else ''),
        top_gloss=('gloss', lambda x: x.value_counts().index[0] if len(x) else ''),
    ).reset_index().sort_values('count', ascending=False).head(n)
    total = grp['count'].sum()
    grp['pct'] = (grp['count'] / total * 100).round(1)
    return grp.reset_index(drop=True)


def nt_participle_book_distribution() -> pd.DataFrame:
    """Participle token count and % per NT book."""
    df = load_syntax()
    ptc = df[df['mood'].str.lower() == 'participle']
    book_counts = ptc['book'].value_counts().reset_index()
    book_counts.columns = ['book', 'count']
    total = book_counts['count'].sum()
    book_counts['pct'] = (book_counts['count'] / total * 100).round(1)

    all_verbs = df[df['class_'] == 'verb']['book'].value_counts().reset_index()
    all_verbs.columns = ['book', 'total_verbs']
    book_counts = book_counts.merge(all_verbs, on='book', how='left')
    book_counts['pct_of_book_verbs'] = (
        book_counts['count'] / book_counts['total_verbs'] * 100
    ).round(1)

    order_map = {b: i for i, b in enumerate(NT_BOOK_ORDER)}
    book_counts['_ord'] = book_counts['book'].map(order_map).fillna(99)
    return book_counts.sort_values('_ord').drop(columns='_ord').reset_index(drop=True)


def nt_participle_genre_profile() -> pd.DataFrame:
    """Tense % breakdown for participles by NT genre group."""
    df = load_syntax()
    ptc = df[df['mood'].str.lower() == 'participle'].copy()
    ptc['tense'] = ptc['tense'].str.lower()
    rows = []
    for genre, books in NT_BOOK_GROUPS.items():
        sub = ptc[ptc['book'].isin(books) & ptc['tense'].notna()]
        total = len(sub)
        row: dict = {'genre': genre}
        for t in TENSE_ORDER:
            cnt = (sub['tense'] == t).sum()
            row[t] = round(cnt / total * 100, 1) if total else 0.0
        row['total'] = total
        rows.append(row)
    return pd.DataFrame(rows).set_index('genre')


def nt_genitive_absolutes(book: str | None = None) -> pd.DataFrame:
    """Genitive absolute participle tokens.

    A genitive absolute has a participle in the genitive case whose subject
    is different from the main clause subject. Identified by: mood=participle,
    case_=genitive. Returns sample token rows with reference and gloss.
    """
    p = nt_participle_data(book)
    gas = p[p['case_'].str.lower() == 'genitive'].copy()
    cols = ['book', 'chapter', 'verse', 'word_num', 'text', 'lemma', 'tense', 'voice', 'gloss']
    available = [c for c in cols if c in gas.columns]
    return gas[available].reset_index(drop=True)


def nt_perfect_participles(book: str | None = None) -> pd.DataFrame:
    """Perfect participle tokens with reference, lemma, and gloss."""
    p = nt_participle_data(book)
    perf = p[p['tense'].str.lower() == 'perfect'].copy()
    cols = ['book', 'chapter', 'verse', 'text', 'lemma', 'strong_g', 'voice', 'case_', 'gloss']
    available = [c for c in cols if c in perf.columns]
    return perf[available].reset_index(drop=True)


# ── Print functions ───────────────────────────────────────────────────────────

def print_nt_participle_overview() -> None:
    """Print a statistical overview of GNT participle morphology."""
    df = load_syntax()
    ptc = df[df['mood'].str.lower() == 'participle']
    total_verbs = len(df[df['class_'] == 'verb'])
    total_ptc = len(ptc)
    unique_lemmas = ptc['lemma'].nunique()

    print()
    print('╔' + '═' * 78 + '╗')
    print('║' + '  Greek NT Participles — Overview'.center(78) + '║')
    print('╚' + '═' * 78 + '╝')
    print()
    print(f"  Total GNT participle tokens:  {total_ptc:>7,}")
    print(f"  % of all GNT verb tokens:     {total_ptc/total_verbs*100:>7.1f}%")
    print(f"  Unique participle lemmas:      {unique_lemmas:>7,}")
    print()

    print("  Tense distribution:")
    for _, row in nt_participle_tense_profile().iterrows():
        if row['count'] > 0:
            bar = '█' * int(row['pct'] / 2)
            print(f"    {row['form']:<12} {row['count']:>6,}  ({row['pct']:>5.1f}%)  {bar}")
    print()
    print("  Voice distribution:")
    for _, row in nt_participle_voice_profile().iterrows():
        if row['count'] > 0:
            bar = '█' * int(row['pct'] / 2)
            print(f"    {row['form']:<12} {row['count']:>6,}  ({row['pct']:>5.1f}%)  {bar}")
    print()


def print_nt_participle_tense(book: str | None = None) -> None:
    scope = book or 'Whole GNT'
    df = nt_participle_tense_profile(book)
    total = df['count'].sum()
    print()
    print('═' * 72)
    print(f"  Participle tense distribution — {scope}  (total: {total:,})")
    print('─' * 72)
    for _, row in df.iterrows():
        if row['count'] == 0:
            continue
        bar = '█' * int(row['pct'] / 2)
        print(f"  {row['form']:<14} {row['count']:>6,}  {row['pct']:>5.1f}%  {bar}")
    print()


def print_nt_participle_voice(book: str | None = None) -> None:
    scope = book or 'Whole GNT'
    df = nt_participle_voice_profile(book)
    total = df['count'].sum()
    print()
    print('═' * 72)
    print(f"  Participle voice distribution — {scope}  (total: {total:,})")
    print('─' * 72)
    for _, row in df.iterrows():
        if row['count'] == 0:
            continue
        bar = '█' * int(row['pct'] / 2)
        print(f"  {row['form']:<14} {row['count']:>6,}  {row['pct']:>5.1f}%  {bar}")
    print()


def print_nt_participle_tense_voice(book: str | None = None) -> None:
    ct = nt_participle_tense_voice(book)
    scope = book or 'Whole GNT'
    print()
    print('═' * 72)
    print(f"  Participle tense × voice — {scope}")
    print('─' * 72)
    header = f"  {'Tense':<14}" + ''.join(f"{v:>10}" for v in ct.columns)
    print(header)
    print('  ' + '─' * 68)
    for tense, row in ct.iterrows():
        total = row.sum()
        vals = ''.join(f"{v:>10,}" for v in row)
        print(f"  {tense:<14}{vals}  ({total:,})")
    print()


def print_nt_participle_role(book: str | None = None) -> None:
    scope = book or 'Whole GNT'
    df = nt_participle_role_profile(book)
    total = df['count'].sum()
    print()
    print('═' * 76)
    print(f"  Participle syntactic role distribution — {scope}  (total: {total:,})")
    print('  (role is a proxy for adverbial vs. adjectival/substantival function)')
    print('─' * 76)
    for _, row in df.iterrows():
        bar = '█' * int(row['pct'] / 2)
        print(f"  {row['role']:<32} {row['count']:>6,}  {row['pct']:>5.1f}%  {bar}")
    print()


def print_nt_participle_top_lemmas(n: int = 20, book: str | None = None) -> None:
    df = nt_participle_top_lemmas(n, book)
    scope = book or 'Whole GNT'
    print()
    print('═' * 76)
    print(f"  Top {n} GNT participle lemmas — {scope}")
    print('─' * 76)
    print(f"  {'#':<4} {'Lemma':<20} {'Strong':>7} {'Count':>7} {'%':>6} {'Top tense':<14} Gloss")
    print('  ' + '─' * 72)
    for i, row in df.iterrows():
        print(f"  {i+1:<4} {row['lemma']:<20} {row['strong_g']:>7} {row['count']:>7,} "
              f"{row['pct']:>5.1f}% {row['top_tense']:<14} {row['top_gloss']}")
    print()


def print_nt_participle_genre_profile() -> None:
    df = nt_participle_genre_profile()
    print()
    print('═' * 80)
    print("  Participle tense % by genre group")
    print('─' * 80)
    tenses = [t for t in TENSE_ORDER if t in df.columns]
    header = f"  {'Genre':<20}" + ''.join(f"{t:>10}" for t in tenses) + f"  {'Total':>8}"
    print(header)
    print('  ' + '─' * 76)
    for genre, row in df.iterrows():
        vals = ''.join(f"{row.get(t, 0.0):>9.1f}%" for t in tenses)
        print(f"  {genre:<20}{vals}  {row['total']:>8,}")
    print()


def print_nt_genitive_absolutes(book: str | None = None, n: int = 20) -> None:
    df = nt_genitive_absolutes(book)
    scope = book or 'Whole GNT'
    print()
    print('═' * 76)
    print(f"  Genitive absolute participles — {scope}  ({len(df)} tokens)")
    print('─' * 76)
    if df.empty:
        print("  None found.")
        print()
        return
    for _, row in df.head(n).iterrows():
        ref = f"{row.get('book', '')} {row.get('chapter', '')}:{row.get('verse', '')}"
        tense = str(row.get('tense', '')).lower()
        voice = str(row.get('voice', '')).lower()
        gloss = row.get('gloss', '')
        print(f"  {ref:<12}  {row.get('text', ''):<20}  {tense} {voice:<10}  {gloss}")
    if len(df) > n:
        print(f"  … ({len(df) - n} more — use nt_genitive_absolutes() for full DataFrame)")
    print()


def print_nt_perfect_participles(n: int = 25) -> None:
    df = nt_perfect_participles()
    print()
    print('═' * 76)
    print(f"  Perfect participles in the GNT  ({len(df)} total tokens)")
    print('  These carry a completed action with ongoing relevance')
    print('─' * 76)
    top = df.groupby(['lemma', 'strong_g', 'voice']).size().reset_index(name='count')
    top = top.sort_values('count', ascending=False).head(n)
    print(f"  {'Lemma':<20} {'Strong':>7} {'Voice':<10} {'Count':>7}")
    print('  ' + '─' * 48)
    for _, row in top.iterrows():
        print(f"  {row['lemma']:<20} {row['strong_g']:>7} {row['voice']:<10} {row['count']:>7,}")
    print()


def print_nt_participle_book_distribution() -> None:
    df = nt_participle_book_distribution()
    print()
    print('═' * 76)
    print("  Participle distribution across NT books")
    print('─' * 76)
    print(f"  {'Book':<8} {'Count':>7} {'% of GNT ptc':>14} {'% of book verbs':>16}  Bar")
    print('  ' + '─' * 72)
    for _, row in df.iterrows():
        bar = '█' * int(row['pct'] * 2)
        print(f"  {row['book']:<8} {row['count']:>7,} {row['pct']:>13.1f}% "
              f"{row['pct_of_book_verbs']:>15.1f}%  {bar}")
    print()


# ── Chart functions ───────────────────────────────────────────────────────────

def nt_participle_tense_chart(book: str | None = None) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_participle_tense_profile(book)
    df = df[df['count'] > 0].sort_values('pct')
    scope = book or 'Whole GNT'

    fig, ax = plt.subplots(figsize=(9, 4))
    colors = plt.cm.Greens([0.4 + 0.5 * i / max(len(df) - 1, 1) for i in range(len(df))])  # type: ignore[attr-defined]
    bars = ax.barh(df['form'], df['pct'], color=colors)
    for bar, val in zip(bars, df['pct']):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va='center', fontsize=9)
    ax.set_title(f"GNT Participle Tense Distribution — {scope}", fontsize=13, fontweight='bold')
    ax.set_xlabel("% of participle tokens")
    ax.set_xlim(0, df['pct'].max() * 1.2)
    ax.xaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()

    out = _ensure_chart_dir() / f'nt_participle_tense{"_"+book if book else ""}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def nt_participle_genre_heatmap() -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_participle_genre_profile()
    tenses = [t for t in TENSE_ORDER if t in df.columns]
    data = df[tenses].values.astype(float)

    fig, ax = plt.subplots(figsize=(10, 3.5))
    im = ax.imshow(data, cmap='YlGn', aspect='auto', vmin=0, vmax=data.max())
    ax.set_xticks(range(len(tenses)))
    ax.set_xticklabels(tenses, fontsize=11)
    ax.set_yticks(range(len(df.index)))
    ax.set_yticklabels(df.index.tolist(), fontsize=11)
    for i in range(len(df.index)):
        for j in range(len(tenses)):
            val = data[i, j]
            ax.text(j, i, f"{val:.1f}%", ha='center', va='center',
                    fontsize=10, color='black' if val < 35 else 'white')
    plt.colorbar(im, ax=ax, label='% of genre participle tokens')
    ax.set_title("GNT Participle Tense by Genre", fontsize=13, fontweight='bold')
    fig.tight_layout()

    out = _ensure_chart_dir() / 'nt_participle_genre_heatmap.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def nt_participle_book_chart() -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_participle_book_distribution()
    fig, ax1 = plt.subplots(figsize=(14, 5))
    x = range(len(df))
    ax1.bar(x, df['count'], color='forestgreen', alpha=0.75, label='ptc count')
    ax1.set_ylabel('Participle token count', color='forestgreen')
    ax1.tick_params(axis='y', labelcolor='forestgreen')

    ax2 = ax1.twinx()
    ax2.plot(x, df['pct_of_book_verbs'], 'o-', color='darkorange',
             linewidth=1.8, markersize=5, label='% of book verbs')
    ax2.set_ylabel('% of book verbs', color='darkorange')
    ax2.tick_params(axis='y', labelcolor='darkorange')

    ax1.set_xticks(list(x))
    ax1.set_xticklabels(df['book'].tolist(), rotation=40, ha='right', fontsize=9)
    ax1.set_title("GNT Participle Distribution Across NT Books", fontsize=13, fontweight='bold')
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    fig.tight_layout()

    out = _ensure_chart_dir() / 'nt_participle_books.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out
