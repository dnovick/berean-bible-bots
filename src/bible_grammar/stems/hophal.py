"""
Hophal verb morphology analysis for Biblical Hebrew instruction.

The Hophal (הָפְעַל) is the passive of the Hiphil stem.
It typically:
  • Expresses the passive of the Hiphil causative: הוּבָא (was brought) ← Hiphil הֵבִיא
  • Expresses a causative-passive state: הוּמַת (was put to death) ← Hiphil הֵמִית
  • Expresses a causative-passive result: הֻגַּד (was told / reported) ← Hiphil הִגִּיד

It is the least common of the seven major stems (~480 tokens), largely
because the Niphal covers most simple passive needs and the Hophal is
restricted to roots where the Hiphil causative is already established.

All functions use MACULA Hebrew WLC data (load_syntax_ot).

Public API
──────────
hophal_data()                           → DataFrame (all Hophal tokens)
hophal_conjugation_profile(book=None)   → DataFrame (type_ distribution)
hophal_top_roots(n=30, book=None)       → DataFrame (most frequent roots)
hophal_root_conjugation(roots=None)     → DataFrame (root × conjugation crosstab)
hophal_book_distribution()              → DataFrame (count + pct per book)
hophal_stem_comparison(books=None)      → DataFrame (all stems % by book)
hophal_dominant_roots(min_pct=70)       → DataFrame (roots >X% Hophal)
hophal_semantic_categories()            → DataFrame (semantic function counts)

print_hophal_overview()                 → None
print_hophal_conjugation(book=None)     → None
print_hophal_top_roots(n=20, book=None) → None
print_hophal_root_conjugation(roots=None) → None
print_hophal_book_distribution()        → None
print_hophal_dominant_roots()           → None
print_hophal_semantic_categories()      → None

hophal_conjugation_chart(book=None)     → Path | None
hophal_book_chart()                     → Path | None
hophal_stem_chart(books=None)           → Path | None
hophal_root_heatmap(top_n=15)           → Path | None

hophal_report(output_dir=None)          → Path   (full Markdown report)
"""

from __future__ import annotations

import pandas as pd
import functools
from pathlib import Path

from ._stem_analysis import StemAnalysis, StemConfig


# ── Semantic function classifier ──────────────────────────────────────────────

_CAUSATIVE_PASSIVE_MOTION_KEYWORDS = (
    'was brought', 'was led', 'was carried', 'was taken',
    'was sent', 'was driven', 'was cast', 'was thrown',
    'was brought out', 'was brought up', 'was brought down',
    'was brought in', 'was led out', 'was led away',
)

_CAUSATIVE_PASSIVE_DEATH_KEYWORDS = (
    'was put to death', 'was killed', 'was slain', 'was struck down',
    'was executed', 'was destroyed',
)

_CAUSATIVE_PASSIVE_SPEECH_KEYWORDS = (
    'was told', 'was reported', 'was declared', 'was announced',
    'was commanded', 'was shown', 'was made known',
)

_CAUSATIVE_PASSIVE_STATE_KEYWORDS = (
    'was set', 'was placed', 'was appointed', 'was established',
    'was given', 'was returned', 'was restored', 'was saved',
    'was hidden', 'was removed',
)


def _hophal_semantic_fn(gloss: str) -> str:
    g = str(gloss).strip().lower()
    if any(w in g for w in _CAUSATIVE_PASSIVE_DEATH_KEYWORDS):
        return 'causative-passive (death/judgment)'
    if any(w in g for w in _CAUSATIVE_PASSIVE_MOTION_KEYWORDS):
        return 'causative-passive (motion/transfer)'
    if any(w in g for w in _CAUSATIVE_PASSIVE_SPEECH_KEYWORDS):
        return 'causative-passive (speech/report)'
    if any(w in g for w in _CAUSATIVE_PASSIVE_STATE_KEYWORDS):
        return 'causative-passive (placement/state)'
    return 'causative-passive (other)'


# ── Config + analysis engine ──────────────────────────────────────────────────

_CONFIG = StemConfig(
    name='hophal',
    macula_value='hophal',
    display='Hophal (הָפְעַל)',
    chart_color='#C9C9C9',  # grey — consistent with stem comparison colour scheme
)

_ANALYSIS = StemAnalysis(_CONFIG)


# ── Public API ────────────────────────────────────────────────────────────────

hophal_data                    = _ANALYSIS.data
hophal_conjugation_profile     = _ANALYSIS.conjugation_profile
hophal_top_roots               = _ANALYSIS.top_roots
hophal_root_conjugation        = _ANALYSIS.root_conjugation
hophal_book_distribution       = _ANALYSIS.book_distribution
hophal_stem_comparison         = _ANALYSIS.stem_comparison


def hophal_dominant_roots(min_pct: float = 70.0, min_tokens: int = 5) -> pd.DataFrame:
    """Roots where the Hophal accounts for ≥ min_pct of all occurrences."""
    return _ANALYSIS.dominant_roots(min_pct, min_tokens)


hophal_semantic_categories       = functools.partial(_ANALYSIS.semantic_categories, _hophal_semantic_fn)
print_hophal_semantic_categories = functools.partial(_ANALYSIS.print_semantic_categories, _hophal_semantic_fn)
hophal_semantic_chart            = functools.partial(_ANALYSIS.semantic_chart, _hophal_semantic_fn)

print_hophal_overview          = _ANALYSIS.print_overview
print_hophal_conjugation       = _ANALYSIS.print_conjugation
print_hophal_top_roots         = _ANALYSIS.print_top_roots
print_hophal_root_conjugation  = _ANALYSIS.print_root_conjugation
print_hophal_book_distribution = _ANALYSIS.print_book_distribution
print_hophal_dominant_roots    = _ANALYSIS.print_dominant_roots

hophal_conjugation_chart       = _ANALYSIS.conjugation_chart
hophal_book_chart              = _ANALYSIS.book_chart
hophal_stem_chart              = _ANALYSIS.stem_comparison_chart
hophal_root_heatmap            = _ANALYSIS.root_heatmap
hophal_top_roots_chart         = _ANALYSIS.top_roots_chart


def hophal_report(output_dir: str | None = None) -> Path:
    """Generate a complete Hophal morphology report (Markdown + PNG charts)."""
    if output_dir is None:
        out_dir = Path('output') / 'reports' / 'ot' / 'verbs'
    else:
        out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Generating charts...")
    charts: dict[str, Path | None] = {
        'conjugation': hophal_conjugation_chart(),
        'books':       hophal_book_chart(),
        'stems':       hophal_stem_chart(),
        'heatmap':     hophal_root_heatmap(),
        'semantic':    hophal_semantic_chart(),
        'top_roots':   hophal_top_roots_chart(),
    }
    for k, p in charts.items():
        if p:
            print(f"  ✓ {k}: {p}")

    df_full = _ANALYSIS._load()
    h = _ANALYSIS._stem_df(df_full)
    total_tokens = len(h)
    total_verbs = len(df_full[df_full['class_'] == 'verb'])
    unique_roots = h['_lem'].nunique()

    conj_df      = hophal_conjugation_profile()
    top_roots_df = hophal_top_roots(20)
    dom_df       = hophal_dominant_roots(min_pct=70, min_tokens=5).head(20)
    sem_df       = hophal_semantic_categories()
    book_df      = hophal_book_distribution().head(20)

    lines: list[str] = []
    lines.append('# Hophal (הָפְעַל) Verb Morphology — Biblical Hebrew\n\n')
    lines.append('*Generated from MACULA Hebrew WLC data*\n\n---\n\n')

    lines.append('## 1. Overview\n\n')
    lines.append(
        'The **Hophal** is the causative-passive stem — the passive counterpart of the Hiphil. '
        'It is the rarest of the seven major stems (~480 tokens), because most simple passive '
        'needs are covered by the Niphal. Hophal forms appear only where the Hiphil causative '
        'is already in use for that root.\n\n'
    )
    lines.append('| Statistic | Value |\n|---|---|\n')
    lines.append(f'| Total Hophal tokens (OT)  | {total_tokens:,} |\n')
    lines.append(f'| % of all OT verb tokens   | {total_tokens/total_verbs*100:.1f}% |\n')
    lines.append(f'| Unique roots in Hophal    | {unique_roots} |\n\n')

    lines.append('### Hophal vs. Hiphil — the causative pair\n\n')
    lines.append('| Hiphil (active) | Hophal (passive) | Root | Gloss |\n|---|---|---|---|\n')
    lines.append('| הֵבִיא (brought) | הוּבָא (was brought) | בוא | come/bring |\n')
    lines.append('| הֵמִית (put to death) | הוּמַת (was put to death) | מות | die |\n')
    lines.append('| הִגִּיד (told) | הֻגַּד (was told) | נגד | tell |\n')
    lines.append('| הוֹצִיא (brought out) | הוּצָא (was brought out) | יצא | go out |\n\n')

    lines.append('## 2. Conjugation Distribution\n\n')
    lines.append('| Conjugation | Count | % |\n|---|---|---|\n')
    for _, row in conj_df.iterrows():
        if row['count'] > 0:
            lines.append(f"| {row['form']} | {row['count']:,} | {row['pct']}% |\n")
    lines.append('\n')

    lines.append('## 3. Distribution Across Books (top 20)\n\n')
    lines.append('| Book | Count | % of OT Hophal | % of book verbs |\n|---|---|---|---|\n')
    for _, row in book_df.iterrows():
        lines.append(
            f"| {row['book']} | {row['count']:,} | {row['pct']}% | {row['pct_of_book_verbs']}% |\n")
    lines.append('\n')

    lines.append('## 4. Most Frequent Hophal Roots (top 20)\n\n')
    lines.append('| # | Root | Lemma | Count | % | Primary meaning |\n|---|---|---|---|---|---|\n')
    for i, row in top_roots_df.iterrows():
        lines.append(
            f"| {i+1} | {row['root']} | {row['lemma']} | {row['count']:,} | {row['pct']}% | {row['top_gloss']} |\n")
    lines.append('\n')

    lines.append('## 5. Hophal-Dominant Roots (≥70%)\n\n')
    lines.append('| Root | Lemma | Hophal | Total | % | Gloss |\n|---|---|---|---|---|---|\n')
    for _, row in dom_df.iterrows():
        lines.append(
            f"| {row['root']} | {row['lemma']} | {row['niphal_count']} | {row['total']} | {row['hif_pct']}% | {row['top_gloss']} |\n")
    lines.append('\n')

    lines.append('## 6. Semantic Function Categories\n\n')
    lines.append('| Category | Count | % |\n|---|---|---|\n')
    for _, row in sem_df.iterrows():
        lines.append(f"| {row['category']} | {row['count']:,} | {row['pct']}% |\n")
    lines.append('\n')

    report_path = out_dir / 'hophal_report.md'
    report_path.write_text(''.join(lines), encoding='utf-8')
    print(f"\nReport saved: {report_path}")
    return report_path
