"""
Biblical Aramaic verb morphology analysis.

Analyses the Aramaic verb stems (Peal, Pael, Haphel, Peil, Hithpeel, etc.)
from the Daniel and Ezra sections of the MACULA Hebrew WLC dataset.
All functions filter to tokens where lang='A'.

Public API
──────────
aramaic_data(book=None)                    → DataFrame (all Aramaic tokens)
aramaic_verb_data(book=None)               → DataFrame (Aramaic verbs only)
aramaic_stem_profile(book=None)            → DataFrame (stem distribution)
aramaic_conj_profile(book=None)            → DataFrame (conjugation distribution)
aramaic_stem_conj(stem=None)               → DataFrame (stem × conjugation crosstab)
aramaic_top_roots(n=30, book=None)         → DataFrame (most frequent roots)
aramaic_book_distribution()                → DataFrame (token count per book)
aramaic_stem_by_book()                     → DataFrame (stem counts per book)

print_aramaic_overview()                   → None
print_aramaic_stem_profile(book=None)      → None
print_aramaic_conj_profile(book=None)      → None
print_aramaic_stem_conj(stem=None)         → None
print_aramaic_top_roots(n=20, book=None)   → None
print_aramaic_book_distribution()          → None

aramaic_stem_chart(book=None)              → Path | None
aramaic_conj_chart(book=None)              → Path | None
aramaic_stem_book_chart()                  → Path | None
"""

from __future__ import annotations
from pathlib import Path

import pandas as pd

from ..core._utils import load_ot_data

STEM_ORDER = [
    'peal', 'haphel', 'pael', 'peil', 'hithpeel',
    'hithpaal', 'aphel', 'shaphel', 'hophal', 'ithpeel', 'ithpaal',
]

CONJ_ORDER = [
    'qatal', 'yiqtol', 'participle active', 'participle passive',
    'infinitive construct', 'imperative',
]

ARAMAIC_BOOKS = ['Dan', 'Ezr']

_CHART_DIR = Path('output') / 'charts' / 'ot' / 'aramaic'


def _ensure_chart_dir() -> Path:
    _CHART_DIR.mkdir(parents=True, exist_ok=True)
    return _CHART_DIR


# ── Data loading ──────────────────────────────────────────────────────────────

def aramaic_data(book: str | None = None) -> pd.DataFrame:
    """All Aramaic tokens (lang='A'), optionally filtered to one book."""
    df = load_ot_data()
    aram = df[df['lang'] == 'A'].copy()
    if book:
        aram = aram[aram['book'] == book]
    return aram


def aramaic_verb_data(book: str | None = None) -> pd.DataFrame:
    """Aramaic verb tokens (lang='A', class_='verb')."""
    df = load_ot_data()
    verbs = df[(df['lang'] == 'A') & (df['class_'] == 'verb')].copy()
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
        if cnt > 0:
            records.append({'form': form, 'count': cnt,
                            'pct': round(cnt / total * 100, 1) if total else 0.0})
    for form, cnt in vc.items():
        if str(form).lower() not in order and int(cnt) > 0:
            records.append({'form': str(form), 'count': int(cnt),
                            'pct': round(int(cnt) / total * 100, 1) if total else 0.0})
    return pd.DataFrame(records)


def aramaic_stem_profile(book: str | None = None) -> pd.DataFrame:
    """Stem distribution for Aramaic verbs. Returns DataFrame: form, count, pct."""
    v = aramaic_verb_data(book)
    return _count_profile(v['stem'].dropna(), STEM_ORDER)


def aramaic_conj_profile(book: str | None = None) -> pd.DataFrame:
    """Conjugation (type_) distribution for Aramaic verbs."""
    v = aramaic_verb_data(book)
    return _count_profile(v['type_'].dropna(), CONJ_ORDER)


def aramaic_stem_conj(stem: str | None = None) -> pd.DataFrame:
    """Stem × conjugation crosstab for Aramaic verbs.

    If stem is None, shows all stems; otherwise filters to that stem.
    """
    v = aramaic_verb_data()
    if stem:
        v = v[v['stem'].str.lower() == stem.lower()]
    sub = v[v['stem'].notna() & v['type_'].notna()].copy()
    sub['stem'] = sub['stem'].str.lower()
    sub['type_'] = sub['type_'].str.lower()
    ct = pd.crosstab(sub['stem'], sub['type_'])
    ct = ct.reindex(
        index=[s for s in STEM_ORDER if s in ct.index],
        columns=[c for c in CONJ_ORDER if c in ct.columns],
        fill_value=0,
    )
    return ct


def aramaic_top_roots(n: int = 30, book: str | None = None) -> pd.DataFrame:
    """Top-n most frequent Aramaic verb roots by lemma."""
    v = aramaic_verb_data(book)
    grp = v.groupby('lemma').agg(
        count=('lemma', 'size'),
        top_stem=('stem', lambda x: x.value_counts().index[0] if len(x) else ''),
        top_gloss=('english', lambda x: x.value_counts().index[0] if len(x) else ''),
    ).reset_index().sort_values('count', ascending=False).head(n)
    total = grp['count'].sum()
    grp['pct'] = (grp['count'] / total * 100).round(1)
    return grp.reset_index(drop=True)


def aramaic_book_distribution() -> pd.DataFrame:
    """Token count (all classes) per book. Columns: book, tokens, verbs, pct_verbs."""
    df = load_ot_data()
    aram = df[df['lang'] == 'A']
    books = aram['book'].value_counts().reset_index()
    books.columns = ['book', 'tokens']

    verbs = aram[aram['class_'] == 'verb']['book'].value_counts().reset_index()
    verbs.columns = ['book', 'verbs']
    out = books.merge(verbs, on='book', how='left').fillna(0)
    out['verbs'] = out['verbs'].astype(int)
    out['pct_verbs'] = (out['verbs'] / out['tokens'] * 100).round(1)
    return out.sort_values('tokens', ascending=False).reset_index(drop=True)


def aramaic_stem_by_book() -> pd.DataFrame:
    """Stem counts per book (Daniel and Ezra)."""
    v = aramaic_verb_data()
    ct = pd.crosstab(v['book'], v['stem'])
    ct = ct.reindex(
        index=[b for b in ARAMAIC_BOOKS if b in ct.index],
        columns=[s for s in STEM_ORDER if s in ct.columns],
        fill_value=0,
    )
    return ct


# ── Print functions ───────────────────────────────────────────────────────────

def print_aramaic_overview() -> None:
    """Print a statistical overview of Biblical Aramaic in the MACULA dataset."""
    df = load_ot_data()
    aram = df[df['lang'] == 'A']
    verbs = aram[aram['class_'] == 'verb']
    total_ot = len(df)
    total_aram = len(aram)
    total_verbs = len(verbs)

    print()
    print('╔' + '═' * 78 + '╗')
    print('║' + '  Biblical Aramaic — OT Overview'.center(78) + '║')
    print('╚' + '═' * 78 + '╝')
    print()
    print(f"  Total Aramaic tokens:       {total_aram:>7,}")
    print(f"  % of OT word tokens:        {total_aram/total_ot*100:>7.2f}%")
    print(f"  Aramaic verb tokens:        {total_verbs:>7,}")
    print()
    print("  Books with Aramaic text:")
    for _, row in aramaic_book_distribution().iterrows():
        print(f"    {row['book']:<8}  {row['tokens']:>5} tokens  "
              f"{row['verbs']:>4} verbs ({row['pct_verbs']:.1f}%)")
    print()

    print("  Stem distribution (verbs):")
    for _, row in aramaic_stem_profile().iterrows():
        bar = '█' * int(row['pct'] / 2)
        print(f"    {row['form']:<14} {row['count']:>4}  ({row['pct']:>5.1f}%)  {bar}")
    print()

    print("  Conjugation distribution (verbs):")
    for _, row in aramaic_conj_profile().iterrows():
        bar = '█' * int(row['pct'] / 2)
        print(f"    {row['form']:<22} {row['count']:>4}  ({row['pct']:>5.1f}%)  {bar}")
    print()


def print_aramaic_stem_profile(book: str | None = None) -> None:
    scope = book or 'Daniel + Ezra'
    df = aramaic_stem_profile(book)
    total = df['count'].sum()
    print()
    print('═' * 72)
    print(f"  Aramaic stem distribution — {scope}  (total: {total:,})")
    print('─' * 72)
    for _, row in df.iterrows():
        bar = '█' * int(row['pct'] / 2)
        print(f"  {row['form']:<16} {row['count']:>5}  {row['pct']:>5.1f}%  {bar}")
    print()


def print_aramaic_conj_profile(book: str | None = None) -> None:
    scope = book or 'Daniel + Ezra'
    df = aramaic_conj_profile(book)
    total = df['count'].sum()
    print()
    print('═' * 72)
    print(f"  Aramaic conjugation distribution — {scope}  (total: {total:,})")
    print('─' * 72)
    for _, row in df.iterrows():
        bar = '█' * int(row['pct'] / 2)
        print(f"  {row['form']:<24} {row['count']:>5}  {row['pct']:>5.1f}%  {bar}")
    print()


def print_aramaic_stem_conj(stem: str | None = None) -> None:
    ct = aramaic_stem_conj(stem)
    label = f"stem={stem}" if stem else "all stems"
    print()
    print('═' * 80)
    print(f"  Aramaic stem × conjugation — {label}")
    print('─' * 80)
    abbrev = {
        'qatal': 'qatal', 'yiqtol': 'yiqtol',
        'participle active': 'ptc.act', 'participle passive': 'ptc.pas',
        'infinitive construct': 'inf.c', 'imperative': 'impv',
    }
    cols = list(ct.columns)
    header = (f"  {'Stem':<14}"
              + ''.join(f"{abbrev.get(c, c[:7]):>9}" for c in cols)
              + f"  {'Total':>6}")
    print(header)
    print('  ' + '─' * 76)
    for s, row in ct.iterrows():
        total = row.sum()
        vals = ''.join(f"{v:>9}" for v in row)
        print(f"  {s:<14}{vals}  {total:>6}")
    print()


def print_aramaic_top_roots(n: int = 20, book: str | None = None) -> None:
    df = aramaic_top_roots(n, book)
    scope = book or 'Daniel + Ezra'
    print()
    print('═' * 76)
    print(f"  Top {n} Aramaic verb roots — {scope}")
    print('─' * 76)
    print(f"  {'#':<4} {'Lemma':<18} {'Count':>6} {'%':>6} {'Top stem':<14} Gloss")
    print('  ' + '─' * 72)
    for i, row in df.iterrows():
        print(f"  {i+1:<4} {row['lemma']:<18} {row['count']:>6} {row['pct']:>5.1f}% "
              f"{row['top_stem']:<14} {row['top_gloss']}")
    print()


def print_aramaic_book_distribution() -> None:
    df = aramaic_book_distribution()
    print()
    print('═' * 60)
    print("  Biblical Aramaic token distribution by book")
    print('─' * 60)
    for _, row in df.iterrows():
        print(f"  {row['book']:<8}  {row['tokens']:>5} tokens  "
              f"{row['verbs']:>4} verbs  ({row['pct_verbs']:.1f}% verbs)")
    print()


# ── Chart functions ───────────────────────────────────────────────────────────

def aramaic_stem_chart(book: str | None = None) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = aramaic_stem_profile(book)
    df = df[df['count'] > 0].sort_values('count')
    scope = book or 'Daniel + Ezra'

    fig, ax = plt.subplots(figsize=(9, 5))
    colors = plt.cm.copper([0.2 + 0.6 * i / max(len(df) - 1, 1) for i in range(len(df))])  # type: ignore[attr-defined]
    bars = ax.barh(df['form'], df['count'], color=colors)
    for bar, row in zip(bars, df.itertuples()):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                f"{row.count}  ({row.pct}%)", va='center', fontsize=9)
    ax.set_title(f"Biblical Aramaic Verb Stem Distribution — {scope}",
                 fontsize=13, fontweight='bold')
    ax.set_xlabel("Token count")
    ax.xaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()

    out = _ensure_chart_dir() / f'aramaic_stems{"_"+book if book else ""}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def aramaic_conj_chart(book: str | None = None) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = aramaic_conj_profile(book)
    df = df[df['count'] > 0].sort_values('pct')
    scope = book or 'Daniel + Ezra'

    fig, ax = plt.subplots(figsize=(9, 4))
    colors = plt.cm.YlOrBr([0.3 + 0.5 * i / max(len(df) - 1, 1) for i in range(len(df))])  # type: ignore[attr-defined]
    bars = ax.barh(df['form'], df['pct'], color=colors)
    for bar, val in zip(bars, df['pct']):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va='center', fontsize=9)
    ax.set_title(f"Biblical Aramaic Conjugation Distribution — {scope}",
                 fontsize=13, fontweight='bold')
    ax.set_xlabel("% of verb tokens")
    ax.set_xlim(0, df['pct'].max() * 1.2)
    ax.xaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()

    out = _ensure_chart_dir() / f'aramaic_conj{"_"+book if book else ""}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def aramaic_stem_book_chart() -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    ct = aramaic_stem_by_book()
    if ct.empty:
        return None

    # Normalize to % per book
    pct_ct = ct.div(ct.sum(axis=1), axis=0) * 100

    fig, ax = plt.subplots(figsize=(9, 5))
    bottom = [0.0] * len(pct_ct.index)
    colors = plt.cm.Set2(range(len(pct_ct.columns)))  # type: ignore[attr-defined]

    for j, stem in enumerate(pct_ct.columns):
        vals = pct_ct[stem].tolist()
        bars = ax.bar(pct_ct.index.tolist(), vals, bottom=bottom,
                      color=colors[j % len(colors)], label=stem, edgecolor='white', linewidth=0.5)
        for bar, val, bot in zip(bars, vals, bottom):
            if val >= 8:
                ax.text(bar.get_x() + bar.get_width() / 2, bot + val / 2,
                        f"{val:.0f}%", ha='center', va='center', fontsize=9)
        bottom = [b + v for b, v in zip(bottom, vals)]

    ax.set_ylim(0, 108)
    ax.set_ylabel('% of verb tokens')
    ax.set_title('Biblical Aramaic Verb Stem Distribution by Book',
                 fontsize=13, fontweight='bold')
    ax.legend(loc='upper right', fontsize=9, ncol=2)
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    fig.tight_layout()

    out = _ensure_chart_dir() / 'aramaic_stem_by_book.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out
