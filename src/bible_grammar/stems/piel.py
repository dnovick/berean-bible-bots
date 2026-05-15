"""
Piel verb morphology analysis for Biblical Hebrew instruction.

The Piel (פִּעֵל) is the intensive-active stem of Biblical Hebrew.
It typically:
  • Expresses an intensive action: שִׁבֵּר (shattered) ← Qal שָׁבַר (broke)
  • Expresses a factitive (makes state into action): קִדֵּשׁ (made holy) ← קָדוֹשׁ (holy)
  • Expresses a declarative: הִצְדִּיק → Piel צִדֵּק (declared righteous)
  • Expresses a denominative (verb from noun): דִּבֵּר (spoke) ← דָּבָר (word)
  • Has a simple active sense for some roots that rarely appear in Qal

All functions use MACULA Hebrew WLC data (load_syntax_ot).

Public API
──────────
piel_data()                           → DataFrame (all Piel tokens)
piel_conjugation_profile(book=None)   → DataFrame (type_ distribution)
piel_top_roots(n=30, book=None)       → DataFrame (most frequent roots)
piel_root_conjugation(roots=None)     → DataFrame (root × conjugation crosstab)
piel_book_distribution()              → DataFrame (count + pct per book)
piel_stem_comparison(books=None)      → DataFrame (all stems % by book)
piel_dominant_roots(min_pct=70)       → DataFrame (roots >X% Piel)
piel_semantic_categories()            → DataFrame (semantic function counts)

print_piel_overview()                 → None
print_piel_conjugation(book=None)     → None
print_piel_top_roots(n=20, book=None) → None
print_piel_root_conjugation(roots=None) → None
print_piel_book_distribution()        → None
print_piel_dominant_roots()           → None
print_piel_semantic_categories()      → None

piel_conjugation_chart(book=None)     → Path | None
piel_book_chart()                     → Path | None
piel_stem_chart(books=None)           → Path | None
piel_root_heatmap(top_n=15)           → Path | None

piel_report(output_dir=None)          → Path   (full Markdown report)
"""

from __future__ import annotations
import functools
from pathlib import Path

from ._stem_analysis import StemAnalysis, StemConfig


# ── Semantic function classifier ──────────────────────────────────────────────

_INTENSIVE_KEYWORDS = (
    'shattered', 'broke in pieces', 'smashed', 'destroyed', 'tore',
    'scattered', 'drove out', 'pursued', 'chased', 'crushed',
    'bless', 'blessed', 'curse', 'cursed', 'praise', 'praised',
    'seek', 'sought', 'inquire', 'inquired',
)

_FACTITIVE_KEYWORDS = (
    'made holy', 'consecrated', 'sanctified', 'purified', 'made clean',
    'defiled', 'made unclean', 'honored', 'glorified', 'justified',
    'made righteous', 'made great', 'magnified', 'made numerous',
    'made strong', 'strengthened', 'made full', 'filled',
)

_DECLARATIVE_KEYWORDS = (
    'declared', 'declared righteous', 'declared guilty', 'declared clean',
    'declared unclean', 'counted', 'regarded as', 'reckoned',
    'pronounced', 'called', 'named',
)

_DENOMINATIVE_KEYWORDS = (
    'spoke', 'speak', 'told', 'commanded', 'prophesied', 'prophesy',
    'prayed', 'pray', 'ministered', 'minister', 'served as priest',
    'acted as priest', 'played', 'sang', 'sang praise',
)


def _piel_semantic_fn(gloss: str) -> str:
    g = str(gloss).strip().lower()
    if any(w in g for w in _DECLARATIVE_KEYWORDS):
        return 'declarative'
    if any(w in g for w in _FACTITIVE_KEYWORDS):
        return 'factitive'
    if any(w in g for w in _DENOMINATIVE_KEYWORDS):
        return 'denominative'
    if any(w in g for w in _INTENSIVE_KEYWORDS):
        return 'intensive'
    return 'other'


# ── Config + analysis engine ──────────────────────────────────────────────────

_CONFIG = StemConfig(
    name='piel',
    macula_value='piel',
    display='Piel (פִּעֵל)',
    chart_color='#5B9BD5',  # blue
)

_ANALYSIS = StemAnalysis(_CONFIG)


# ── Public API ────────────────────────────────────────────────────────────────

piel_data                    = _ANALYSIS.data
piel_conjugation_profile     = _ANALYSIS.conjugation_profile
piel_top_roots               = _ANALYSIS.top_roots
piel_root_conjugation        = _ANALYSIS.root_conjugation
piel_book_distribution       = _ANALYSIS.book_distribution
piel_stem_comparison         = _ANALYSIS.stem_comparison
piel_dominant_roots          = _ANALYSIS.dominant_roots

piel_semantic_categories     = functools.partial(_ANALYSIS.semantic_categories, _piel_semantic_fn)
print_piel_semantic_categories = functools.partial(_ANALYSIS.print_semantic_categories, _piel_semantic_fn)
piel_semantic_chart          = functools.partial(_ANALYSIS.semantic_chart, _piel_semantic_fn)

print_piel_overview          = _ANALYSIS.print_overview
print_piel_conjugation       = _ANALYSIS.print_conjugation
print_piel_top_roots         = _ANALYSIS.print_top_roots
print_piel_root_conjugation  = _ANALYSIS.print_root_conjugation
print_piel_book_distribution = _ANALYSIS.print_book_distribution
print_piel_dominant_roots    = _ANALYSIS.print_dominant_roots

piel_conjugation_chart       = _ANALYSIS.conjugation_chart
piel_book_chart              = _ANALYSIS.book_chart
piel_stem_chart              = _ANALYSIS.stem_comparison_chart
piel_root_heatmap            = _ANALYSIS.root_heatmap
piel_top_roots_chart         = _ANALYSIS.top_roots_chart


def piel_report(output_dir: str | None = None) -> Path:
    """Generate a complete Piel morphology report (Markdown + PNG charts)."""
    if output_dir is None:
        out_dir = Path('output') / 'reports' / 'ot' / 'verbs'
    else:
        out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Generating charts...")
    charts: dict[str, Path | None] = {
        'conjugation': piel_conjugation_chart(),
        'books':       piel_book_chart(),
        'stems':       piel_stem_chart(),
        'heatmap':     piel_root_heatmap(),
        'semantic':    piel_semantic_chart(),
        'top_roots':   piel_top_roots_chart(),
    }
    for k, p in charts.items():
        if p:
            print(f"  ✓ {k}: {p}")

    df_full = _ANALYSIS._load()
    h = _ANALYSIS._stem_df(df_full)
    total_tokens = len(h)
    total_verbs = len(df_full[df_full['class_'] == 'verb'])
    unique_roots = h['_lem'].nunique()

    conj_df = piel_conjugation_profile()
    top_roots_df = piel_top_roots(20)
    dom_df = piel_dominant_roots(min_pct=80, min_tokens=10).head(20)
    sem_df = piel_semantic_categories()
    book_df = piel_book_distribution().head(20)

    lines: list[str] = []
    lines.append('# Piel (פִּעֵל) Verb Morphology — Biblical Hebrew\n')
    lines.append('*Generated from MACULA Hebrew WLC data*\n\n')
    lines.append('---\n\n')

    lines.append('## 1. Overview\n\n')
    lines.append(
        'The **Piel** stem is the primary intensive-active stem of Biblical Hebrew. '
        'It is formed with a **Dagesh Forte in the middle root consonant (R2)** '
        'and a characteristic Tsere or Patach vowel pattern.\n\n'
    )
    lines.append('| Statistic | Value |\n|---|---|\n')
    lines.append(f'| Total Piel tokens (OT) | {total_tokens:,} |\n')
    lines.append(f'| % of all OT verb tokens  | {total_tokens/total_verbs*100:.1f}% |\n')
    lines.append(f'| Unique roots in Piel   | {unique_roots} |\n')

    lines.append('## 2. Conjugation Distribution\n\n')
    lines.append('| Conjugation | Count | % |\n|---|---|---|\n')
    for _, row in conj_df.iterrows():
        if row['count'] > 0:
            lines.append(f"| {row['form']} | {row['count']:,} | {row['pct']}% |\n")
    lines.append('\n')

    lines.append('## 3. Distribution Across Books\n\n')
    lines.append('| Book | Count | % of OT Piel | % of book verbs |\n|---|---|---|---|\n')
    for _, row in book_df.iterrows():
        lines.append(
            f"| {row['book']} | {row['count']:,} | {row['pct']}% "
            f"| {row['pct_of_book_verbs']}% |\n")
    lines.append('\n')

    lines.append('## 4. Most Frequent Piel Roots\n\n')
    lines.append('| # | Root | Lemma | Count | % | Primary meaning |\n|---|---|---|---|---|---|\n')
    for i, row in top_roots_df.iterrows():
        lines.append(
            f"| {i+1} | {row['root']} | {row['lemma']} | {row['count']:,} "
            f"| {row['pct']}% | {row['top_gloss']} |\n")
    lines.append('\n')

    lines.append('## 5. Piel-Dominant Roots (≥80%)\n\n')
    lines.append('| Root | Lemma | Piel | Total | % | Gloss |\n|---|---|---|---|---|---|\n')
    for _, row in dom_df.iterrows():
        lines.append(
            f"| {row['root']} | {row['lemma']} | {row['piel_count']} "
            f"| {row['total']} | {row['hif_pct']}% | {row['top_gloss']} |\n")
    lines.append('\n')

    lines.append('## 6. Semantic Function Categories\n\n')
    lines.append('| Category | Count | % |\n|---|---|---|\n')
    for _, row in sem_df.iterrows():
        lines.append(f"| {row['category']} | {row['count']:,} | {row['pct']}% |\n")
    lines.append('\n')

    report_path = out_dir / 'piel_report.md'
    report_path.write_text(''.join(lines), encoding='utf-8')
    print(f"\nReport saved: {report_path}")
    return report_path
