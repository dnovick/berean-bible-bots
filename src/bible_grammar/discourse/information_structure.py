"""
Information structure analysis — clause-linking, parataxis/hypotaxis ratios,
fronted elements, and postpositive particle profiles for Hebrew OT and Greek NT.

**Scope and limitations**
True topic/focus identification requires full syntactic annotation beyond what
MACULA provides. This module computes well-defined *approximations*:
  - Pre-verbal element counts from verb-form order analysis (OT)
  - Parataxis/hypotaxis ratios from connective inventory counts (OT + NT)
  - Explicit subject-pronoun frequency as a potential focus marker (NT)
  - Postpositive discourse particle density (NT)
These are labeled as proxies throughout; they are linguistic metrics, not
full discourse analyses.

Hebrew metrics
──────────────
  parataxis_ratio    — verses beginning with וְ/וַ (wayyiqtol or waw-qatal)
  hypotaxis_ratio    — subordinate clauses (כִּי, אֲשֶׁר, inf. construct, rel.)
  fronted_ratio      — non-verb-initial clauses (nominal, adverbial before verb)
  nominal_clause_pct — clauses with no verb (copula-free)

Greek metrics
─────────────
  de_density         — δέ per 1,000 tokens (topic shift / continuation)
  gar_density        — γάρ per 1,000 tokens (explanatory/given)
  oun_density        — οὖν per 1,000 tokens (inferential)
  men_density        — μέν per 1,000 tokens (correlative/contrast)
  asyndeton_pct      — verses with no clause-linking particle
  explicit_subj_pct  — finite verb clauses with explicit subject pronoun

Questions this answers
──────────────────────
  • Is Deuteronomy more hypotactic than Genesis? (law vs. narrative)
  • Which NT book uses the most γάρ? (Paul is dominant)
  • How does John's clause-linking compare to Mark's?
  • Which OT books have the highest fronted-element ratio?

Public API
──────────
ot_information_profile(book)             → dict
nt_information_profile(book)             → dict
ot_clause_linking_comparison(books)      → DataFrame
nt_clause_linking_comparison(books)      → DataFrame

print_ot_information_profile(book)       → None
print_nt_information_profile(book)       → None
print_ot_clause_linking_comparison(books) → None
print_nt_clause_linking_comparison(books) → None

nt_clause_linking_chart(books)           → Path | None
nt_information_heatmap(books)            → Path | None
ot_clause_linking_chart(books)           → Path | None
"""

from __future__ import annotations
from pathlib import Path

import pandas as pd

from ..core._utils import ensure_chart_dir

_CHART_DIR = Path('output') / 'charts' / 'information_structure'

# Hebrew connectives
_WAW_CONSECUTIVE_TYPES = {'wayyiqtol', 'waw+qatal', 'waw+yiqtol'}
_SUBORDINATING_LEMMAS = {'כִּי', 'אֲשֶׁר', 'פֶּן', 'לְמַעַן', 'אַחַר', 'בְּעַבוּר'}
_NON_VERB_INITIAL_TYPES = {'nominal', 'participle active', 'participle passive'}

# Greek postpositive particles (lemma)
_GK_POSTPOSITIVES = {
    'δέ': 'de',
    'γάρ': 'gar',
    'οὖν': 'oun',
    'μέν': 'men',
    'ἀλλά': 'alla',
    'καί': 'kai',
}
# Explicit subject pronouns (Greek first/second/third person)
_GK_SUBJ_PRONS = {'ἐγώ', 'σύ', 'αὐτός', 'ἡμεῖς', 'ὑμεῖς', 'αὐτοί'}


# ── helpers ───────────────────────────────────────────────────────────────────

def _load_ot_h() -> pd.DataFrame:
    from ..core._utils import load_ot_h
    return load_ot_h()


def _load_nt() -> pd.DataFrame:
    from ..core._utils import load_nt
    return load_nt()


def _book_df_h(book: str) -> pd.DataFrame:
    return _load_ot_h().pipe(lambda df: df[df['book'] == book])


def _book_df_g(book: str) -> pd.DataFrame:
    df = _load_nt()
    return df[df['book'] == book]


# ── data functions ────────────────────────────────────────────────────────────

def ot_information_profile(book: str) -> dict:
    """
    Clause-linking and information structure metrics for an OT Hebrew book.

    Returns a dict with: total_tokens, parataxis_ratio, hypotaxis_ratio,
    fronted_ratio, nominal_clause_pct, inf_construct_per1k.
    """
    df = _book_df_h(book)
    if df.empty:
        return {}

    total = len(df)
    # Verse-level analysis for clause-initial type
    verse_firsts = df.groupby(['book', 'chapter', 'verse']).first().reset_index()
    total_verses = len(verse_firsts)

    # Parataxis: verse starts with wayyiqtol or waw-prefix
    wayyiqtol_first = (verse_firsts['type_'] == 'wayyiqtol').sum()
    # Also count verses where first token lemma is וְ/וַ (waw conjunction)
    waw_lemmas = {'וְ', 'וּ', 'וַ'}
    waw_first = verse_firsts['lemma'].isin(waw_lemmas).sum()
    parataxis = int(wayyiqtol_first + waw_first)

    # Hypotaxis: subordinating lemmas appear in verse
    subordinating = df['lemma'].isin(_SUBORDINATING_LEMMAS).sum()

    # Fronted elements: non-verb-initial types
    fronted = int(verse_firsts['type_'].isin(_NON_VERB_INITIAL_TYPES).sum())

    # Nominal clause: verse with no verbal token
    verbal_types = {'wayyiqtol', 'qatal', 'yiqtol', 'imperative', 'cohortative',
                    'jussive', 'participle active', 'participle passive',
                    'infinitive construct', 'infinitive absolute'}
    verse_has_verb = df.groupby(['book', 'chapter', 'verse'])['type_'].apply(
        lambda s: s.isin(verbal_types).any()
    )
    nominal_verses = int((~verse_has_verb).sum())

    # Infinitive construct density
    inf_c = (df['type_'] == 'infinitive construct').sum() / total * 1000

    return {
        'book': book,
        'total_tokens': total,
        'total_verses': total_verses,
        'parataxis_count': parataxis,
        'parataxis_ratio': round(parataxis / max(total_verses, 1), 4),
        'hypotaxis_subordinators': int(subordinating),
        'hypotaxis_per1k': round(subordinating / total * 1000, 2),
        'fronted_elements': fronted,
        'fronted_ratio': round(fronted / max(total_verses, 1), 4),
        'nominal_clause_count': nominal_verses,
        'nominal_clause_pct': round(nominal_verses / max(total_verses, 1) * 100, 2),
        'inf_construct_per1k': round(inf_c, 2),
    }


def nt_information_profile(book: str) -> dict:
    """
    Clause-linking and information structure metrics for an NT Greek book.

    Returns a dict with: total_tokens, de_density, gar_density, oun_density,
    men_density, kai_density, explicit_subj_pct.
    """
    df = _book_df_g(book)
    if df.empty:
        return {}

    total = len(df)

    # Postpositive particle densities (per 1,000 tokens)
    densities = {}
    for lemma, key in _GK_POSTPOSITIVES.items():
        cnt = (df['lemma'] == lemma).sum()
        densities[f'{key}_per1k'] = round(cnt / total * 1000, 2)

    # Explicit subject pronoun frequency (as % of all tokens)
    subj_pron = df['lemma'].isin(_GK_SUBJ_PRONS).sum()
    explicit_subj_pct = round(subj_pron / total * 100, 2)

    # Asyndeton: verses with no connective particle
    conn_lemmas = set(_GK_POSTPOSITIVES.keys())
    total_verses = df.groupby(['book', 'chapter', 'verse']).ngroups
    verse_has_conn = df.groupby(['book', 'chapter', 'verse'])['lemma'].apply(
        lambda s: bool(s.isin(conn_lemmas).any())
    )
    asyndeton_count = int((~verse_has_conn).sum())

    return {
        'book': book,
        'total_tokens': total,
        'total_verses': total_verses,
        **densities,
        'explicit_subj_pct': explicit_subj_pct,
        'asyndeton_count': asyndeton_count,
        'asyndeton_pct': round(asyndeton_count / max(total_verses, 1) * 100, 2),
    }


def ot_clause_linking_comparison(books: list[str]) -> pd.DataFrame:
    """Side-by-side information structure metrics for OT books."""
    rows = [ot_information_profile(b) for b in books]
    rows = [r for r in rows if r]
    return pd.DataFrame(rows).set_index('book') if rows else pd.DataFrame()


def nt_clause_linking_comparison(books: list[str]) -> pd.DataFrame:
    """Side-by-side information structure metrics for NT books."""
    rows = [nt_information_profile(b) for b in books]
    rows = [r for r in rows if r]
    return pd.DataFrame(rows).set_index('book') if rows else pd.DataFrame()


# ── print functions ───────────────────────────────────────────────────────────

def print_ot_information_profile(book: str) -> None:
    p = ot_information_profile(book)
    if not p:
        print(f"No data for {book}.")
        return
    w = 58
    print(f"\n{'═'*w}")
    print(f"  Information Structure Profile — {book} (Hebrew)")
    print(f"{'═'*w}")
    print(f"  Total tokens           : {p['total_tokens']:>8,}")
    print(f"  Total verses           : {p['total_verses']:>8,}")
    print(f"  Parataxis ratio        : {p['parataxis_ratio']:>8.4f}  (wayyiqtol/waw-initial)")
    print(f"  Hypotaxis subordinators: {p['hypotaxis_subordinators']:>8,}"
          f"  ({p['hypotaxis_per1k']}/1k tokens)")
    print(f"  Fronted elements       : {p['fronted_elements']:>8,}  (non-verb-initial)")
    print(f"  Fronted ratio          : {p['fronted_ratio']:>8.4f}")
    print(f"  Nominal clauses        : {p['nominal_clause_count']:>8,}"
          f"  ({p['nominal_clause_pct']}% of verses)")
    print(f"  Inf. construct/1k      : {p['inf_construct_per1k']:>8.2f}")
    print()


def print_nt_information_profile(book: str) -> None:
    p = nt_information_profile(book)
    if not p:
        print(f"No data for {book}.")
        return
    w = 58
    print(f"\n{'═'*w}")
    print(f"  Information Structure Profile — {book} (Greek)")
    print(f"{'═'*w}")
    print(f"  Total tokens           : {p['total_tokens']:>8,}")
    print(f"  Total verses           : {p['total_verses']:>8,}")
    print(f"  δέ per 1k              : {p['de_per1k']:>8.2f}  (topic shift/continuation)")
    print(f"  γάρ per 1k             : {p['gar_per1k']:>8.2f}  (explanatory/given)")
    print(f"  οὖν per 1k             : {p['oun_per1k']:>8.2f}  (inferential)")
    print(f"  μέν per 1k             : {p['men_per1k']:>8.2f}  (correlative/contrast)")
    print(f"  καί per 1k             : {p['kai_per1k']:>8.2f}  (additive/parataxis)")
    print(f"  ἀλλά per 1k            : {p['alla_per1k']:>8.2f}  (adversative)")
    print(f"  Explicit subject %     : {p['explicit_subj_pct']:>8.2f}%")
    print(f"  Asyndeton %            : {p['asyndeton_pct']:>8.2f}%  (no connective in verse)")
    print()


def print_ot_clause_linking_comparison(books: list[str]) -> None:
    df = ot_clause_linking_comparison(books)
    if df.empty:
        return
    print("\nOT Clause-Linking Comparison")
    metrics = ['parataxis_ratio', 'hypotaxis_per1k', 'fronted_ratio',
               'nominal_clause_pct', 'inf_construct_per1k']
    labels = ['Paratx ratio', 'Hypotx/1k', 'Fronted ratio', 'Nominal %', 'InfC/1k']
    print(f"  {'Metric':<16}" + ''.join(f"  {b:>8}" for b in df.index))
    print('  ' + '-' * (16 + 10 * len(df)))
    for metric, label in zip(metrics, labels):
        if metric not in df.columns:
            continue
        line = f"  {label:<16}"
        for val in df[metric]:
            if isinstance(val, float):
                line += f"  {val:>8.3f}"
            else:
                line += f"  {val:>8}"
        print(line)
    print()


def print_nt_clause_linking_comparison(books: list[str]) -> None:
    df = nt_clause_linking_comparison(books)
    if df.empty:
        return
    print("\nNT Clause-Linking Comparison")
    metrics = ['de_per1k', 'gar_per1k', 'oun_per1k', 'kai_per1k',
               'alla_per1k', 'explicit_subj_pct', 'asyndeton_pct']
    labels = ['δέ/1k', 'γάρ/1k', 'οὖν/1k', 'καί/1k',
              'ἀλλά/1k', 'Expl.subj%', 'Asyndeton%']
    print(f"  {'Metric':<14}" + ''.join(f"  {b:>8}" for b in df.index))
    print('  ' + '-' * (14 + 10 * len(df)))
    for metric, label in zip(metrics, labels):
        if metric not in df.columns:
            continue
        line = f"  {label:<14}"
        for val in df[metric]:
            if isinstance(val, float):
                line += f"  {val:>8.2f}"
            else:
                line += f"  {val:>8}"
        print(line)
    print()


# ── chart functions ───────────────────────────────────────────────────────────

def nt_clause_linking_chart(
    books: list[str],
) -> Path | None:
    """Stacked bar chart of NT postpositive particle densities per book."""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        return None

    df = nt_clause_linking_comparison(books)
    if df.empty:
        return None

    ensure_chart_dir(_CHART_DIR)
    out = _CHART_DIR / f'nt_clause_linking_{"_".join(books[:6])}.png'

    metric_cols = ['de_per1k', 'gar_per1k', 'oun_per1k', 'men_per1k', 'alla_per1k']
    metric_labels = ['δέ', 'γάρ', 'οὖν', 'μέν', 'ἀλλά']
    colors = ['steelblue', 'darkorange', 'green', 'crimson', 'purple']

    x = np.arange(len(df.index))
    bottom = np.zeros(len(df.index))
    fig, ax = plt.subplots(figsize=(max(8, len(books) * 0.8), 5))
    for col, label, color in zip(metric_cols, metric_labels, colors):
        if col in df.columns:
            vals = df[col].fillna(0).values.astype(float)
            ax.bar(x, vals, bottom=bottom, label=label, color=color)
            bottom += vals

    ax.set_xticks(x)
    ax.set_xticklabels(df.index, rotation=45, ha='right', fontsize=9)
    ax.set_ylabel('Occurrences per 1,000 tokens')
    ax.set_title('NT Discourse Particle Density by Book')
    ax.legend(loc='upper right', fontsize=9)
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def nt_information_heatmap(
    books: list[str],
) -> Path | None:
    """Heatmap of NT information structure metrics across books."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_clause_linking_comparison(books)
    if df.empty:
        return None

    metrics = ['de_per1k', 'gar_per1k', 'oun_per1k', 'kai_per1k',
               'alla_per1k', 'explicit_subj_pct', 'asyndeton_pct']
    labels = ['δέ/1k', 'γάρ/1k', 'οὖν/1k', 'καί/1k',
              'ἀλλά/1k', 'Expl.subj%', 'Asyndeton%']
    metrics = [m for m in metrics if m in df.columns]
    labels = labels[:len(metrics)]

    mat = df[metrics].copy().astype(float)
    for col in mat.columns:
        std = mat[col].std()
        mat[col] = (mat[col] - mat[col].mean()) / std if std > 0 else 0.0

    ensure_chart_dir(_CHART_DIR)
    out = _CHART_DIR / f'nt_info_heatmap_{"_".join(books[:6])}.png'

    fig, ax = plt.subplots(figsize=(max(8, len(metrics) * 1.2), max(4, len(books) * 0.5)))
    im = ax.imshow(mat.values, aspect='auto', cmap='RdBu', vmin=-2, vmax=2)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=35, ha='right', fontsize=9)
    ax.set_yticks(range(len(mat.index)))
    ax.set_yticklabels(mat.index, fontsize=9)
    plt.colorbar(im, ax=ax, label='Z-score')
    ax.set_title('NT Information Structure Metrics (Z-normalised)')
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def ot_clause_linking_chart(
    books: list[str],
) -> Path | None:
    """Grouped bar chart of OT parataxis, hypotaxis, and fronted element ratios."""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        return None

    df = ot_clause_linking_comparison(books)
    if df.empty:
        return None

    ensure_chart_dir(_CHART_DIR)
    out = _CHART_DIR / f'ot_clause_linking_{"_".join(books[:6])}.png'

    metrics = ['parataxis_ratio', 'fronted_ratio', 'nominal_clause_pct']
    labels = ['Parataxis ratio', 'Fronted ratio', 'Nominal clause %']
    colors = ['steelblue', 'darkorange', 'green']

    x = np.arange(len(df.index))
    w = 0.25
    fig, ax = plt.subplots(figsize=(max(8, len(books) * 0.7), 5))
    for i, (metric, label, color) in enumerate(zip(metrics, labels, colors)):
        if metric in df.columns:
            vals = df[metric].fillna(0).values.astype(float)
            ax.bar(x + (i - 1) * w, vals, w, label=label, color=color)

    ax.set_xticks(x)
    ax.set_xticklabels(df.index, rotation=45, ha='right', fontsize=9)
    ax.set_ylabel('Ratio / %')
    ax.set_title('OT Clause-Linking Metrics by Book')
    ax.legend()
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out
