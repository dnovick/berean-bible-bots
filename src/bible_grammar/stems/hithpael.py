"""
Hithpael verb morphology analysis for Biblical Hebrew instruction.

The Hithpael (הִתְפַּעֵל) is the reflexive-intensive stem of Biblical Hebrew.
It typically:
  • Expresses a reflexive of the Piel: הִתְקַדֵּשׁ (consecrated oneself) ← Piel קִדֵּשׁ
  • Expresses a reciprocal action: הִתְרָאוּ (saw one another)
  • Expresses an iterative/frequentative: הִתְהַלֵּךְ (walked about, walked continually)
  • Expresses a tolerative/reflexive: הִתְמַכֵּר (sold oneself)
  • Has a denominative sense for some roots: הִתְנַבֵּא (acted as a prophet)

All functions use MACULA Hebrew WLC data (load_syntax_ot).

Public API
──────────
hithpael_data()                           → DataFrame (all Hithpael tokens)
hithpael_conjugation_profile(book=None)   → DataFrame (type_ distribution)
hithpael_top_roots(n=30, book=None)       → DataFrame (most frequent roots)
hithpael_root_conjugation(roots=None)     → DataFrame (root × conjugation crosstab)
hithpael_book_distribution()              → DataFrame (count + pct per book)
hithpael_stem_comparison(books=None)      → DataFrame (all stems % by book)
hithpael_dominant_roots(min_pct=70)       → DataFrame (roots >X% Hithpael)
hithpael_semantic_categories()            → DataFrame (semantic function counts)

print_hithpael_overview()                 → None
print_hithpael_conjugation(book=None)     → None
print_hithpael_top_roots(n=20, book=None) → None
print_hithpael_root_conjugation(roots=None) → None
print_hithpael_book_distribution()        → None
print_hithpael_dominant_roots()           → None
print_hithpael_semantic_categories()      → None

hithpael_conjugation_chart(book=None)     → Path | None
hithpael_book_chart()                     → Path | None
hithpael_stem_chart(books=None)           → Path | None
hithpael_root_heatmap(top_n=15)           → Path | None

hithpael_report(output_dir=None)          → Path   (full Markdown report)
"""

from __future__ import annotations

import pandas as pd
import functools
from pathlib import Path

from ._stem_analysis import StemAnalysis, StemConfig


# ── Semantic function classifier ──────────────────────────────────────────────

_REFLEXIVE_KEYWORDS = (
    'himself', 'herself', 'themselves', 'oneself',
    'consecrated himself', 'purified himself', 'sanctified himself',
    'humbled himself', 'prostrated himself', 'bowed himself',
    'strengthened himself', 'encouraged himself',
    'presented himself', 'showed himself',
    'mourned', 'wept', 'lamented',
)

_RECIPROCAL_KEYWORDS = (
    'one another', 'each other', 'together', 'saw one another',
    'looked at each other', 'married one another',
)

_ITERATIVE_KEYWORDS = (
    'walked about', 'walked continually', 'went about', 'kept walking',
    'continually', 'again and again', 'repeatedly',
    'prayed', 'interceded', 'pleaded',
)

_DENOMINATIVE_KEYWORDS = (
    'acted as a prophet', 'prophesied', 'acted as priest',
    'played the harlot', 'played the fool', 'acted like',
    'pretended', 'feigned', 'disguised',
)


def _hithpael_semantic_fn(gloss: str) -> str:
    g = str(gloss).strip().lower()
    if any(w in g for w in _RECIPROCAL_KEYWORDS):
        return 'reciprocal'
    if any(w in g for w in _DENOMINATIVE_KEYWORDS):
        return 'denominative'
    if any(w in g for w in _ITERATIVE_KEYWORDS):
        return 'iterative'
    if any(w in g for w in _REFLEXIVE_KEYWORDS):
        return 'reflexive'
    return 'other'


# ── Config + analysis engine ──────────────────────────────────────────────────

_CONFIG = StemConfig(
    name='hithpael',
    macula_value='hithpael',
    display='Hithpael (הִתְפַּעֵל)',
    chart_color='#FFC000',  # amber
)

_ANALYSIS = StemAnalysis(_CONFIG)


# ── Public API ────────────────────────────────────────────────────────────────

hithpael_data                    = _ANALYSIS.data
hithpael_conjugation_profile     = _ANALYSIS.conjugation_profile
hithpael_top_roots               = _ANALYSIS.top_roots
hithpael_root_conjugation        = _ANALYSIS.root_conjugation
hithpael_book_distribution       = _ANALYSIS.book_distribution
hithpael_stem_comparison         = _ANALYSIS.stem_comparison


def hithpael_dominant_roots(min_pct: float = 70.0, min_tokens: int = 5) -> pd.DataFrame:
    """Roots where the Hithpael accounts for ≥ min_pct of all occurrences."""
    return _ANALYSIS.dominant_roots(min_pct, min_tokens)


hithpael_semantic_categories     = functools.partial(_ANALYSIS.semantic_categories, _hithpael_semantic_fn)
print_hithpael_semantic_categories = functools.partial(_ANALYSIS.print_semantic_categories, _hithpael_semantic_fn)
hithpael_semantic_chart          = functools.partial(_ANALYSIS.semantic_chart, _hithpael_semantic_fn)

print_hithpael_overview          = _ANALYSIS.print_overview
print_hithpael_conjugation       = _ANALYSIS.print_conjugation
print_hithpael_top_roots         = _ANALYSIS.print_top_roots
print_hithpael_root_conjugation  = _ANALYSIS.print_root_conjugation
print_hithpael_book_distribution = _ANALYSIS.print_book_distribution
print_hithpael_dominant_roots    = _ANALYSIS.print_dominant_roots

hithpael_conjugation_chart       = _ANALYSIS.conjugation_chart
hithpael_book_chart              = _ANALYSIS.book_chart
hithpael_stem_chart              = _ANALYSIS.stem_comparison_chart
hithpael_root_heatmap            = _ANALYSIS.root_heatmap
hithpael_top_roots_chart         = _ANALYSIS.top_roots_chart


def hithpael_report(output_dir: str | None = None) -> Path:
    """Generate a complete Hithpael morphology report (Markdown + PNG charts)."""
    if output_dir is None:
        out_dir = Path('output') / 'reports' / 'ot' / 'verbs'
    else:
        out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df_full = _ANALYSIS._load()
    h = _ANALYSIS._stem_df(df_full)
    total_tokens = len(h)
    total_verbs = len(df_full[df_full['class_'] == 'verb'])
    unique_roots = h['_lem'].nunique()

    conj_df = hithpael_conjugation_profile()
    top_roots_df = hithpael_top_roots(20)
    sem_df = hithpael_semantic_categories()
    book_df = hithpael_book_distribution().head(20)

    lines: list[str] = []
    lines.append('# Hithpael (הִתְפַּעֵל) Verb Morphology — Biblical Hebrew\n')
    lines.append('*Generated from MACULA Hebrew WLC data*\n\n')
    lines.append('---\n\n')
    lines.append('## 1. Overview\n\n')
    lines.append('| Statistic | Value |\n|---|---|\n')
    lines.append(f'| Total Hithpael tokens (OT) | {total_tokens:,} |\n')
    lines.append(f'| % of all OT verb tokens     | {total_tokens/total_verbs*100:.1f}% |\n')
    lines.append(f'| Unique roots in Hithpael    | {unique_roots} |\n\n')

    lines.append('## 2. Conjugation Distribution\n\n')
    lines.append('| Conjugation | Count | % |\n|---|---|---|\n')
    for _, row in conj_df.iterrows():
        if row['count'] > 0:
            lines.append(f"| {row['form']} | {row['count']:,} | {row['pct']}% |\n")
    lines.append('\n')

    lines.append('## 3. Distribution Across Books\n\n')
    lines.append('| Book | Count | % of OT Hithpael | % of book verbs |\n|---|---|---|---|\n')
    for _, row in book_df.iterrows():
        lines.append(
            f"| {row['book']} | {row['count']:,} | {row['pct']}% "
            f"| {row['pct_of_book_verbs']}% |\n")
    lines.append('\n')

    lines.append('## 4. Most Frequent Hithpael Roots\n\n')
    lines.append('| # | Root | Lemma | Count | % | Primary meaning |\n|---|---|---|---|---|---|\n')
    for i, row in top_roots_df.iterrows():
        lines.append(
            f"| {i+1} | {row['root']} | {row['lemma']} | {row['count']:,} "
            f"| {row['pct']}% | {row['top_gloss']} |\n")
    lines.append('\n')

    lines.append('## 5. Semantic Function Categories\n\n')
    lines.append('| Category | Count | % |\n|---|---|---|\n')
    for _, row in sem_df.iterrows():
        lines.append(f"| {row['category']} | {row['count']:,} | {row['pct']}% |\n")
    lines.append('\n')

    report_path = out_dir / 'hithpael_report.md'
    report_path.write_text(''.join(lines), encoding='utf-8')
    print(f"\nReport saved: {report_path}")
    return report_path
