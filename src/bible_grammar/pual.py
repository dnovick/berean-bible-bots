"""
Pual verb morphology analysis for Biblical Hebrew instruction.

The Pual (פֻּעַל) is the passive of the Piel stem.
It typically:
  • Expresses the passive of the Piel intensive: שֻׁבַּר (was shattered) ← Piel שִׁבֵּר
  • Expresses a passive factitive state: קֻדַּשׁ (was made holy / was consecrated)
  • Expresses a passive declarative: צֻדַּק (was declared righteous)
  • Is far less common than the Piel (~450 tokens vs. ~6,500)

All functions use MACULA Hebrew WLC data (load_syntax_ot).

Public API
──────────
pual_data()                           → DataFrame (all Pual tokens)
pual_conjugation_profile(book=None)   → DataFrame (type_ distribution)
pual_top_roots(n=30, book=None)       → DataFrame (most frequent roots)
pual_root_conjugation(roots=None)     → DataFrame (root × conjugation crosstab)
pual_book_distribution()              → DataFrame (count + pct per book)
pual_stem_comparison(books=None)      → DataFrame (all stems % by book)
pual_dominant_roots(min_pct=70)       → DataFrame (roots >X% Pual)
pual_semantic_categories()            → DataFrame (semantic function counts)

print_pual_overview()                 → None
print_pual_conjugation(book=None)     → None
print_pual_top_roots(n=20, book=None) → None
print_pual_root_conjugation(roots=None) → None
print_pual_book_distribution()        → None
print_pual_dominant_roots()           → None
print_pual_semantic_categories()      → None

pual_conjugation_chart(book=None)     → Path | None
pual_book_chart()                     → Path | None
pual_stem_chart(books=None)           → Path | None
pual_root_heatmap(top_n=15)           → Path | None

pual_report(output_dir=None)          → Path   (full Markdown report)
"""

from __future__ import annotations

import pandas as pd
import functools
from pathlib import Path

from ._stem_analysis import StemAnalysis, StemConfig


# ── Semantic function classifier ──────────────────────────────────────────────

_PASSIVE_INTENSIVE_KEYWORDS = (
    'was broken', 'was shattered', 'was crushed', 'was scattered',
    'was driven out', 'was cut down', 'was struck', 'was beaten',
    'was torn', 'was pursued',
)

_PASSIVE_FACTITIVE_KEYWORDS = (
    'was consecrated', 'was sanctified', 'was made holy', 'was purified',
    'was defiled', 'was honored', 'was glorified', 'was filled',
    'was strengthened', 'was magnified',
)

_PASSIVE_DECLARATIVE_KEYWORDS = (
    'was declared', 'was counted', 'was reckoned', 'was regarded',
    'was called', 'was named', 'was pronounced',
)

_BIRTH_KEYWORDS = (
    'was born', 'born',
)


def _pual_semantic_fn(gloss: str) -> str:
    g = str(gloss).strip().lower()
    if any(w in g for w in _BIRTH_KEYWORDS):
        return 'passive (birth)'
    if any(w in g for w in _PASSIVE_DECLARATIVE_KEYWORDS):
        return 'passive declarative'
    if any(w in g for w in _PASSIVE_FACTITIVE_KEYWORDS):
        return 'passive factitive'
    if any(w in g for w in _PASSIVE_INTENSIVE_KEYWORDS):
        return 'passive intensive'
    return 'passive (other)'


# ── Config + analysis engine ──────────────────────────────────────────────────

_CONFIG = StemConfig(
    name='pual',
    macula_value='pual',
    display='Pual (פֻּעַל)',
    chart_color='#A9D18E',  # green
)

_ANALYSIS = StemAnalysis(_CONFIG)


# ── Public API ────────────────────────────────────────────────────────────────

pual_data                    = _ANALYSIS.data
pual_conjugation_profile     = _ANALYSIS.conjugation_profile
pual_top_roots               = _ANALYSIS.top_roots
pual_root_conjugation        = _ANALYSIS.root_conjugation
pual_book_distribution       = _ANALYSIS.book_distribution
pual_stem_comparison         = _ANALYSIS.stem_comparison


def pual_dominant_roots(min_pct: float = 70.0, min_tokens: int = 5) -> pd.DataFrame:
    """Roots where the Pual accounts for ≥ min_pct of all occurrences."""
    return _ANALYSIS.dominant_roots(min_pct, min_tokens)


pual_semantic_categories     = functools.partial(_ANALYSIS.semantic_categories, _pual_semantic_fn)
print_pual_semantic_categories = functools.partial(_ANALYSIS.print_semantic_categories, _pual_semantic_fn)
pual_semantic_chart          = functools.partial(_ANALYSIS.semantic_chart, _pual_semantic_fn)

print_pual_overview          = _ANALYSIS.print_overview
print_pual_conjugation       = _ANALYSIS.print_conjugation
print_pual_top_roots         = _ANALYSIS.print_top_roots
print_pual_root_conjugation  = _ANALYSIS.print_root_conjugation
print_pual_book_distribution = _ANALYSIS.print_book_distribution
print_pual_dominant_roots    = _ANALYSIS.print_dominant_roots

pual_conjugation_chart       = _ANALYSIS.conjugation_chart
pual_book_chart              = _ANALYSIS.book_chart
pual_stem_chart              = _ANALYSIS.stem_comparison_chart
pual_root_heatmap            = _ANALYSIS.root_heatmap
pual_top_roots_chart         = _ANALYSIS.top_roots_chart


def pual_report(output_dir: str | None = None) -> Path:
    """Generate a complete Pual morphology report (Markdown + PNG charts)."""
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

    conj_df = pual_conjugation_profile()
    top_roots_df = pual_top_roots(20)
    sem_df = pual_semantic_categories()
    book_df = pual_book_distribution().head(20)

    lines: list[str] = []
    lines.append('# Pual (פֻּעַל) Verb Morphology — Biblical Hebrew\n')
    lines.append('*Generated from MACULA Hebrew WLC data*\n\n')
    lines.append('---\n\n')
    lines.append('## 1. Overview\n\n')
    lines.append('| Statistic | Value |\n|---|---|\n')
    lines.append(f'| Total Pual tokens (OT) | {total_tokens:,} |\n')
    lines.append(f'| % of all OT verb tokens  | {total_tokens/total_verbs*100:.1f}% |\n')
    lines.append(f'| Unique roots in Pual   | {unique_roots} |\n\n')

    lines.append('## 2. Conjugation Distribution\n\n')
    lines.append('| Conjugation | Count | % |\n|---|---|---|\n')
    for _, row in conj_df.iterrows():
        if row['count'] > 0:
            lines.append(f"| {row['form']} | {row['count']:,} | {row['pct']}% |\n")
    lines.append('\n')

    lines.append('## 3. Distribution Across Books\n\n')
    lines.append('| Book | Count | % of OT Pual | % of book verbs |\n|---|---|---|---|\n')
    for _, row in book_df.iterrows():
        lines.append(
            f"| {row['book']} | {row['count']:,} | {row['pct']}% "
            f"| {row['pct_of_book_verbs']}% |\n")
    lines.append('\n')

    lines.append('## 4. Most Frequent Pual Roots\n\n')
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

    report_path = out_dir / 'pual_report.md'
    report_path.write_text(''.join(lines), encoding='utf-8')
    print(f"\nReport saved: {report_path}")
    return report_path
