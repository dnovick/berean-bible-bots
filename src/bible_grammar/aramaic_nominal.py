"""
Biblical Aramaic nominal morphology analysis.

Covers noun state/gender/number distribution, pronoun types, preposition
frequency, and adjective usage in the Aramaic sections of Daniel and Ezra.
All functions filter to lang='A'.

Public API
──────────
aramaic_noun_data(book=None)               → DataFrame (all Aramaic noun tokens)
aramaic_pron_data(book=None)               → DataFrame (all Aramaic pronoun tokens)
aramaic_prep_data(book=None)               → DataFrame (all Aramaic preposition tokens)
aramaic_adj_data(book=None)                → DataFrame (all Aramaic adjective tokens)

aramaic_noun_state_profile(book=None)      → DataFrame (absolute/construct/determined)
aramaic_noun_gender_profile(book=None)     → DataFrame (masculine/feminine)
aramaic_noun_number_profile(book=None)     → DataFrame (singular/plural/dual)
aramaic_noun_gender_state(book=None)       → DataFrame (gender × state crosstab)
aramaic_noun_top_lemmas(n=20, book=None)   → DataFrame (most frequent noun lemmas)
aramaic_noun_state_by_book()               → DataFrame (state counts per book)
aramaic_pron_type_profile(book=None)       → DataFrame (pronoun type distribution)
aramaic_prep_frequency(n=15, book=None)    → DataFrame (top prepositions by lemma)
aramaic_class_distribution(book=None)      → DataFrame (all word classes)

print_aramaic_nominal_overview()           → None
print_aramaic_noun_state(book=None)        → None
print_aramaic_noun_gender(book=None)       → None
print_aramaic_noun_top_lemmas(n=20, book=None) → None
print_aramaic_noun_state_by_book()         → None
print_aramaic_pron_profile(book=None)      → None
print_aramaic_prep_frequency(n=15, book=None) → None

aramaic_noun_state_chart(book=None)        → Path | None
aramaic_noun_state_book_chart()            → Path | None
aramaic_prep_chart(book=None)              → Path | None
"""

from __future__ import annotations
from pathlib import Path

import pandas as pd

from ._utils import load_ot_data

NOUN_STATE_ORDER  = ['absolute', 'construct', 'determined']
GENDER_ORDER      = ['masculine', 'feminine']
NUMBER_ORDER      = ['singular', 'plural', 'dual']
PRON_TYPE_ORDER   = ['pronominal', 'personal', 'demonstrative',
                     'interrogative', 'indefinite']

ARAMAIC_BOOKS = ['Dan', 'Ezr']

_CHART_DIR = Path('output') / 'charts' / 'ot' / 'aramaic'


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
        if cnt > 0:
            records.append({'form': form, 'count': cnt,
                            'pct': round(cnt / total * 100, 1) if total else 0.0})
    for form, cnt in vc.items():
        if str(form).lower() not in order and int(cnt) > 0:
            records.append({'form': str(form), 'count': int(cnt),
                            'pct': round(int(cnt) / total * 100, 1) if total else 0.0})
    return pd.DataFrame(records)


# ── Data loading ──────────────────────────────────────────────────────────────

def _aram(book: str | None = None) -> pd.DataFrame:
    df = load_ot_data()
    out = df[df['lang'] == 'A'].copy()
    if book:
        out = out[out['book'] == book]
    return out


def aramaic_noun_data(book: str | None = None) -> pd.DataFrame:
    """All Aramaic noun tokens (lang='A', class_='noun')."""
    return _aram(book).pipe(lambda df: df[df['class_'] == 'noun'].copy())


def aramaic_pron_data(book: str | None = None) -> pd.DataFrame:
    """All Aramaic pronoun tokens (lang='A', class_='pron')."""
    return _aram(book).pipe(lambda df: df[df['class_'] == 'pron'].copy())


def aramaic_prep_data(book: str | None = None) -> pd.DataFrame:
    """All Aramaic preposition tokens (lang='A', class_='prep')."""
    return _aram(book).pipe(lambda df: df[df['class_'] == 'prep'].copy())


def aramaic_adj_data(book: str | None = None) -> pd.DataFrame:
    """All Aramaic adjective tokens (lang='A', class_='adj')."""
    return _aram(book).pipe(lambda df: df[df['class_'] == 'adj'].copy())


# ── Profile functions ─────────────────────────────────────────────────────────

def aramaic_noun_state_profile(book: str | None = None) -> pd.DataFrame:
    """Noun state distribution (absolute/construct/determined)."""
    n = aramaic_noun_data(book)
    return _count_profile(n['state'].fillna(''), NOUN_STATE_ORDER)


def aramaic_noun_gender_profile(book: str | None = None) -> pd.DataFrame:
    """Noun gender distribution."""
    n = aramaic_noun_data(book)
    return _count_profile(n['gender'].fillna(''), GENDER_ORDER)


def aramaic_noun_number_profile(book: str | None = None) -> pd.DataFrame:
    """Noun number distribution."""
    n = aramaic_noun_data(book)
    return _count_profile(n['number'].fillna(''), NUMBER_ORDER)


def aramaic_noun_gender_state(book: str | None = None) -> pd.DataFrame:
    """Gender × state crosstab (counts)."""
    n = aramaic_noun_data(book)
    sub = n[n['gender'].notna() & n['state'].notna() &
            (n['gender'] != '') & (n['state'] != '')].copy()
    sub['gender'] = sub['gender'].str.lower()
    sub['state'] = sub['state'].str.lower()
    ct = pd.crosstab(sub['gender'], sub['state'])
    ct = ct.reindex(
        index=[g for g in GENDER_ORDER if g in ct.index],
        columns=[s for s in NOUN_STATE_ORDER if s in ct.columns],
        fill_value=0,
    )
    return ct


def aramaic_noun_top_lemmas(n: int = 20, book: str | None = None) -> pd.DataFrame:
    """Top-n most frequent Aramaic noun lemmas."""
    nouns = aramaic_noun_data(book)
    grp = nouns.groupby('lemma').agg(
        count=('lemma', 'size'),
        top_gloss=('english', lambda x: x.value_counts().index[0] if len(x) else ''),
        top_state=('state', lambda x: x.value_counts().index[0] if len(x) else ''),
    ).reset_index().sort_values('count', ascending=False).head(n)
    total = grp['count'].sum()
    grp['pct'] = (grp['count'] / total * 100).round(1)
    return grp.reset_index(drop=True)


def aramaic_noun_state_by_book() -> pd.DataFrame:
    """Noun state counts per book (Daniel and Ezra)."""
    nouns = aramaic_noun_data()
    sub = nouns[nouns['state'].notna() & (nouns['state'] != '')].copy()
    sub['state'] = sub['state'].str.lower()
    ct = pd.crosstab(sub['book'], sub['state'])
    ct = ct.reindex(
        index=[b for b in ARAMAIC_BOOKS if b in ct.index],
        columns=[s for s in NOUN_STATE_ORDER if s in ct.columns],
        fill_value=0,
    )
    return ct


def aramaic_pron_type_profile(book: str | None = None) -> pd.DataFrame:
    """Pronoun type distribution (pronominal/personal/demonstrative/etc.)."""
    p = aramaic_pron_data(book)
    return _count_profile(p['type_'].fillna(''), PRON_TYPE_ORDER)


def aramaic_prep_frequency(n: int = 15, book: str | None = None) -> pd.DataFrame:
    """Top-n Aramaic prepositions by frequency. Columns: lemma, count, pct, top_gloss."""
    preps = aramaic_prep_data(book)
    grp = preps.groupby('lemma').agg(
        count=('lemma', 'size'),
        top_gloss=('english', lambda x: x.value_counts().index[0] if len(x) else ''),
    ).reset_index().sort_values('count', ascending=False).head(n)
    total = grp['count'].sum()
    grp['pct'] = (grp['count'] / total * 100).round(1)
    return grp.reset_index(drop=True)


def aramaic_class_distribution(book: str | None = None) -> pd.DataFrame:
    """Distribution of all word classes in the Aramaic sections."""
    aram = _aram(book)
    vc = aram['class_'].value_counts().reset_index()
    vc.columns = ['class_', 'count']
    total = vc['count'].sum()
    vc['pct'] = (vc['count'] / total * 100).round(1)
    return vc.reset_index(drop=True)


# ── Print functions ───────────────────────────────────────────────────────────

def print_aramaic_nominal_overview() -> None:
    """Print a statistical overview of Biblical Aramaic nominal morphology."""
    df = load_ot_data()
    aram = df[df['lang'] == 'A']
    nouns = aram[aram['class_'] == 'noun']
    prons = aram[aram['class_'] == 'pron']
    preps = aram[aram['class_'] == 'prep']
    adjs  = aram[aram['class_'] == 'adj']
    arts  = aram[aram['class_'] == 'art']
    total = len(aram)

    print()
    print('╔' + '═' * 78 + '╗')
    print('║' + '  Biblical Aramaic Nominal System — Overview'.center(78) + '║')
    print('╚' + '═' * 78 + '╝')
    print()
    print(f"  Total Aramaic tokens:       {total:>7,}")
    print(f"  Nouns:                      {len(nouns):>7,}  ({len(nouns)/total*100:.1f}%)")
    print(f"  Pronouns:                   {len(prons):>7,}  ({len(prons)/total*100:.1f}%)")
    print(f"  Prepositions:               {len(preps):>7,}  ({len(preps)/total*100:.1f}%)")
    print(f"  Adjectives:                 {len(adjs):>7,}  ({len(adjs)/total*100:.1f}%)")
    print(f"  Articles (ה/א det. prefix): {len(arts):>7,}  ({len(arts)/total*100:.1f}%)")
    print()

    print("  Noun state distribution:")
    for _, row in aramaic_noun_state_profile().iterrows():
        bar = '█' * int(row['pct'] / 2)
        print(f"    {row['form']:<14} {row['count']:>4}  ({row['pct']:>5.1f}%)  {bar}")
    print()
    print("  Noun state — Daniel vs. Ezra:")
    ct = aramaic_noun_state_by_book()
    for bk, row in ct.iterrows():
        total_bk = row.sum()
        vals = '  '.join(
            f"{s}: {int(row.get(s, 0)):>3}" for s in NOUN_STATE_ORDER if s in row.index
        )
        print(f"    {bk}  |  {vals}  |  total: {total_bk}")
    print()


def _print_profile(label: str, df: pd.DataFrame) -> None:
    total = df['count'].sum()
    print()
    print('═' * 70)
    print(f"  {label}  (total: {total:,})")
    print('─' * 70)
    for _, row in df.iterrows():
        bar = '█' * int(row['pct'] / 2)
        print(f"  {row['form']:<20} {row['count']:>5}  {row['pct']:>5.1f}%  {bar}")
    print()


def print_aramaic_noun_state(book: str | None = None) -> None:
    scope = book or 'Daniel + Ezra'
    _print_profile(f"Aramaic noun state — {scope}", aramaic_noun_state_profile(book))


def print_aramaic_noun_gender(book: str | None = None) -> None:
    scope = book or 'Daniel + Ezra'
    _print_profile(f"Aramaic noun gender — {scope}", aramaic_noun_gender_profile(book))


def print_aramaic_noun_top_lemmas(n: int = 20, book: str | None = None) -> None:
    df = aramaic_noun_top_lemmas(n, book)
    scope = book or 'Daniel + Ezra'
    print()
    print('═' * 76)
    print(f"  Top {n} Aramaic noun lemmas — {scope}")
    print('─' * 76)
    print(f"  {'#':<4} {'Lemma':<22} {'Count':>6} {'%':>6}  {'Top state':<14} Gloss")
    print('  ' + '─' * 72)
    for i, row in df.iterrows():
        print(f"  {i+1:<4} {row['lemma']:<22} {row['count']:>6,} {row['pct']:>5.1f}%  "
              f"{row['top_state']:<14} {row['top_gloss']}")
    print()


def print_aramaic_noun_state_by_book() -> None:
    ct = aramaic_noun_state_by_book()
    print()
    print('═' * 70)
    print("  Aramaic noun state by book — Daniel vs. Ezra")
    print('─' * 70)
    states = list(ct.columns)
    header = f"  {'Book':<8}" + ''.join(f"{s:>14}" for s in states) + f"  {'Total':>6}"
    print(header)
    print('  ' + '─' * 66)
    for bk, row in ct.iterrows():
        total_bk = row.sum()
        vals = ''.join(f"{int(row.get(s, 0)):>14}" for s in states)
        print(f"  {bk:<8}{vals}  {total_bk:>6}")
    print()


def print_aramaic_pron_profile(book: str | None = None) -> None:
    scope = book or 'Daniel + Ezra'
    _print_profile(f"Aramaic pronoun type distribution — {scope}",
                   aramaic_pron_type_profile(book))


def print_aramaic_prep_frequency(n: int = 15, book: str | None = None) -> None:
    df = aramaic_prep_frequency(n, book)
    scope = book or 'Daniel + Ezra'
    print()
    print('═' * 68)
    print(f"  Top {n} Aramaic prepositions — {scope}")
    print('─' * 68)
    print(f"  {'#':<4} {'Lemma':<20} {'Count':>6} {'%':>6}  Gloss")
    print('  ' + '─' * 64)
    for i, row in df.iterrows():
        print(f"  {i+1:<4} {row['lemma']:<20} {row['count']:>6,} {row['pct']:>5.1f}%  "
              f"{row['top_gloss']}")
    print()


# ── Chart functions ───────────────────────────────────────────────────────────

def aramaic_noun_state_chart(book: str | None = None) -> Path | None:
    """Horizontal bar chart of Aramaic noun state distribution."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = aramaic_noun_state_profile(book)
    df = df[df['count'] > 0]
    scope = book or 'Daniel + Ezra'

    fig, ax = plt.subplots(figsize=(9, 3.5))
    colors = ['#1565C0', '#E65100', '#2E7D32'][:len(df)]
    bars = ax.barh(df['form'], df['count'], color=colors)
    for bar, row in zip(bars, df.itertuples()):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                f"{row.count}  ({row.pct}%)", va='center', fontsize=9)
    ax.set_title(f"Biblical Aramaic Noun State Distribution — {scope}",
                 fontsize=13, fontweight='bold')
    ax.set_xlabel("Token count")
    ax.xaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()

    out = _ensure_chart_dir() / f'aramaic_noun_state{"_"+book if book else ""}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def aramaic_noun_state_book_chart() -> Path | None:
    """Stacked bar chart of noun state % per book (Daniel vs. Ezra)."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    ct = aramaic_noun_state_by_book()
    if ct.empty:
        return None

    pct_ct = ct.div(ct.sum(axis=1), axis=0) * 100
    fig, ax = plt.subplots(figsize=(7, 4))
    bottom = [0.0] * len(pct_ct.index)
    colors = {'absolute': '#1565C0', 'construct': '#E65100', 'determined': '#2E7D32'}

    for state in pct_ct.columns:
        vals = pct_ct[state].tolist()
        bars = ax.bar(pct_ct.index.tolist(), vals, bottom=bottom,
                      color=colors.get(state, '#888888'), label=state,
                      edgecolor='white', linewidth=0.5)
        for bar, val, bot in zip(bars, vals, bottom):
            if val >= 8:
                ax.text(bar.get_x() + bar.get_width() / 2, bot + val / 2,
                        f"{val:.0f}%", ha='center', va='center', fontsize=10)
        bottom = [b + v for b, v in zip(bottom, vals)]

    ax.set_ylim(0, 110)
    ax.set_ylabel('% of noun tokens')
    ax.set_title('Aramaic Noun State by Book (Daniel vs. Ezra)',
                 fontsize=13, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    fig.tight_layout()

    out = _ensure_chart_dir() / 'aramaic_noun_state_by_book.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def aramaic_prep_chart(book: str | None = None) -> Path | None:
    """Horizontal bar chart of top Aramaic prepositions."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = aramaic_prep_frequency(12, book)
    if df.empty:
        return None
    scope = book or 'Daniel + Ezra'
    df = df.sort_values('count')

    fig, ax = plt.subplots(figsize=(9, 5))
    colors = plt.cm.copper([0.2 + 0.6 * i / max(len(df) - 1, 1) for i in range(len(df))])  # type: ignore[attr-defined]
    bars = ax.barh(df['lemma'], df['count'], color=colors)
    for bar, row in zip(bars, df.itertuples()):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                f"{row.count}  ({row.pct}%)", va='center', fontsize=9)
    ax.set_title(f"Top Aramaic Prepositions — {scope}", fontsize=13, fontweight='bold')
    ax.set_xlabel("Token count")
    ax.xaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()

    out = _ensure_chart_dir() / f'aramaic_preps{"_"+book if book else ""}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out
