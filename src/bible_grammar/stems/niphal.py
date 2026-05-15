"""
Niphal verb morphology analysis for Biblical Hebrew instruction.

The Niphal (נִפְעַל) is the reflexive-passive stem of Biblical Hebrew.
It typically:
  • Expresses the passive of the Qal: נִשְׁמַר (was kept) ← Qal שָׁמַר (kept)
  • Expresses a reflexive action: נִלְחַם (fought) ← idea of fighting for oneself
  • Expresses a reciprocal action: נוֹעֲדוּ (met each other) ← idea of mutual meeting
  • Expresses a tolerative: נִמְכַּר (allowed himself to be sold)
  • Has a middle / stative sense: נִכְלַם (felt ashamed)

All functions use MACULA Hebrew WLC data (load_syntax_ot).

Public API
──────────
niphal_data()                           → DataFrame (all Niphal tokens)
niphal_conjugation_profile(book=None)   → DataFrame (type_ distribution)
niphal_top_roots(n=30, book=None)       → DataFrame (most frequent roots)
niphal_root_conjugation(roots=None)     → DataFrame (root × conjugation crosstab)
niphal_book_distribution()              → DataFrame (count + pct per book)
niphal_stem_comparison(books=None)      → DataFrame (all stems % by book)
niphal_dominant_roots(min_pct=70)       → DataFrame (roots >X% Niphal)
niphal_semantic_categories()            → DataFrame (semantic function counts)

print_niphal_overview()                 → None
print_niphal_conjugation(book=None)     → None
print_niphal_top_roots(n=20, book=None) → None
print_niphal_root_conjugation(roots=None) → None
print_niphal_book_distribution()        → None
print_niphal_dominant_roots()           → None
print_niphal_semantic_categories()      → None

niphal_conjugation_chart(book=None)     → Path | None
niphal_book_chart()                     → Path | None
niphal_stem_chart(books=None)           → Path | None
niphal_root_heatmap(top_n=15)           → Path | None

niphal_report(output_dir=None)          → Path   (full Markdown report)
"""

from __future__ import annotations
import functools
from pathlib import Path

from ._stem_analysis import StemAnalysis, StemConfig


# ── Semantic function classifier ──────────────────────────────────────────────

_PASSIVE_KEYWORDS = (
    'was', 'were', 'be', 'been', 'being',
    'is born', 'was born', 'is called', 'was called', 'is written', 'was written',
    'is commanded', 'was commanded', 'is given', 'was given',
    'is cut off', 'was cut off', 'is gathered', 'was gathered',
    'is told', 'was told', 'is seen', 'was seen',
)

_REFLEXIVE_KEYWORDS = (
    'himself', 'herself', 'themselves', 'oneself',
    'present oneself', 'show himself', 'hide himself', 'hide herself',
    'strengthen himself', 'strengthened himself',
    'defile himself', 'purify himself', 'sanctify himself',
    'mourned', 'mourn', 'washed himself',
)

_RECIPROCAL_KEYWORDS = (
    'each other', 'one another', 'together', 'met', 'meet',
    'assembled', 'assemble', 'gathered together', 'consulted',
)

_MIDDLE_STATIVE_KEYWORDS = (
    'ashamed', 'afraid', 'sorry', 'glad', 'troubled', 'grieved',
    'remained', 'stood', 'stayed', 'turned', 'repented',
    'was established', 'was sure', 'was firm',
)


def _niphal_semantic_fn(gloss: str) -> str:
    g = str(gloss).strip().lower()
    if any(w in g for w in _RECIPROCAL_KEYWORDS):
        return 'reciprocal'
    if any(w in g for w in _REFLEXIVE_KEYWORDS):
        return 'reflexive'
    if any(w in g for w in _MIDDLE_STATIVE_KEYWORDS):
        return 'middle / stative'
    if any(w in g for w in _PASSIVE_KEYWORDS):
        return 'passive'
    return 'other'


# ── Config + analysis engine ──────────────────────────────────────────────────

_CONFIG = StemConfig(
    name='niphal',
    macula_value='niphal',
    display='Niphal (נִפְעַל)',
    chart_color='#ED7D31',  # orange — consistent with stem comparison colour scheme
)

_ANALYSIS = StemAnalysis(_CONFIG)


# ── Public API ────────────────────────────────────────────────────────────────

niphal_data                    = _ANALYSIS.data
niphal_conjugation_profile     = _ANALYSIS.conjugation_profile
niphal_top_roots               = _ANALYSIS.top_roots
niphal_root_conjugation        = _ANALYSIS.root_conjugation
niphal_book_distribution       = _ANALYSIS.book_distribution
niphal_stem_comparison         = _ANALYSIS.stem_comparison
niphal_dominant_roots          = _ANALYSIS.dominant_roots

niphal_semantic_categories     = functools.partial(_ANALYSIS.semantic_categories, _niphal_semantic_fn)
print_niphal_semantic_categories = functools.partial(_ANALYSIS.print_semantic_categories, _niphal_semantic_fn)
niphal_semantic_chart          = functools.partial(_ANALYSIS.semantic_chart, _niphal_semantic_fn)

print_niphal_overview          = _ANALYSIS.print_overview
print_niphal_conjugation       = _ANALYSIS.print_conjugation
print_niphal_top_roots         = _ANALYSIS.print_top_roots
print_niphal_root_conjugation  = _ANALYSIS.print_root_conjugation
print_niphal_book_distribution = _ANALYSIS.print_book_distribution
print_niphal_dominant_roots    = _ANALYSIS.print_dominant_roots

niphal_conjugation_chart       = _ANALYSIS.conjugation_chart
niphal_book_chart              = _ANALYSIS.book_chart
niphal_stem_chart              = _ANALYSIS.stem_comparison_chart
niphal_root_heatmap            = _ANALYSIS.root_heatmap
niphal_top_roots_chart         = _ANALYSIS.top_roots_chart


def niphal_report(output_dir: str | None = None) -> Path:
    """
    Generate a complete Niphal morphology report (Markdown + PNG charts).

    Returns path to the Markdown report.
    """
    if output_dir is None:
        out_dir = Path('output') / 'reports' / 'ot' / 'verbs'
    else:
        out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Generating charts...")
    charts: dict[str, Path | None] = {
        'conjugation': niphal_conjugation_chart(),
        'books':       niphal_book_chart(),
        'stems':       niphal_stem_chart(),
        'heatmap':     niphal_root_heatmap(),
        'semantic':    niphal_semantic_chart(),
        'top_roots':   niphal_top_roots_chart(),
    }
    for k, p in charts.items():
        if p:
            print(f"  ✓ {k}: {p}")

    df_full = _ANALYSIS._load()
    h = _ANALYSIS._stem_df(df_full)
    total_tokens = len(h)
    total_verbs = len(df_full[df_full['class_'] == 'verb'])
    unique_roots = h['_lem'].nunique()

    conj_df = niphal_conjugation_profile()
    top_roots_df = niphal_top_roots(20)
    dom_df = niphal_dominant_roots(min_pct=80, min_tokens=10).head(20)
    sem_df = niphal_semantic_categories()
    book_df = niphal_book_distribution().head(20)

    lines: list[str] = []
    lines.append('# Niphal (נִפְעַל) Verb Morphology — Biblical Hebrew\n')
    lines.append('*Generated from MACULA Hebrew WLC data*\n\n')
    lines.append('---\n\n')

    lines.append('## 1. Overview\n\n')
    lines.append(
        'The **Niphal** stem is the primary reflexive/passive stem of Biblical Hebrew. '
        'It is formed with a נ (nun) prefix in the perfect and a נִ vowel pattern, '
        'but the nun assimilates in the imperfect, producing a doubled middle consonant '
        '(e.g. יִשָּׁמֵר). The Niphal is the **most common** derived stem after the Qal.\n\n'
    )
    lines.append('| Statistic | Value |\n|---|---|\n')
    lines.append(f'| Total Niphal tokens (OT) | {total_tokens:,} |\n')
    lines.append(f'| % of all OT verb tokens  | {total_tokens/total_verbs*100:.1f}% |\n')
    lines.append(f'| Unique roots in Niphal   | {unique_roots} |\n')

    lines.append('### Semantic functions of the Niphal\n\n')
    lines.append('| Function | Description | Example |\n|---|---|---|\n')
    lines.append('| **Passive** | Passive of Qal | נִשְׁמַר "was kept" (← שָׁמַר "kept") |\n')
    lines.append('| **Reflexive** | Action on/for oneself | נִסְתַּר "hid himself" |\n')
    lines.append('| **Reciprocal** | Mutual action | נוֹעֲדוּ "met each other" |\n')
    lines.append('| **Middle/Stative** | Inner state | נִכְלַם "felt ashamed" |\n')
    lines.append('| **Tolerative** | Allowed to happen | נִמְכַּר "sold himself" |\n\n')

    lines.append('## 2. Conjugation Distribution\n\n')
    if charts['conjugation']:
        rel = Path('../..') / 'charts' / 'ot' / 'verbs' / charts['conjugation'].name
        lines.append(f'![Niphal conjugation chart]({rel})\n\n')
    lines.append('| Conjugation | Count | % |\n|---|---|---|\n')
    for _, row in conj_df.iterrows():
        if row['count'] > 0:
            lines.append(f"| {row['form']} | {row['count']:,} | {row['pct']}% |\n")
    lines.append('\n')

    lines.append('## 3. Distribution Across Books\n\n')
    if charts['books']:
        rel = Path('../..') / 'charts' / 'ot' / 'verbs' / charts['books'].name
        lines.append(f'![Niphal book distribution]({rel})\n\n')
    lines.append('| Book | Count | % of OT Niphal | % of book verbs |\n|---|---|---|---|\n')
    for _, row in book_df.iterrows():
        lines.append(
            f"| {row['book']} | {row['count']:,} | {row['pct']}% | {row['pct_of_book_verbs']}% |\n")
    lines.append('\n')

    lines.append('## 4. Most Frequent Niphal Roots\n\n')
    if charts['top_roots']:
        rel = Path('../..') / 'charts' / 'ot' / 'verbs' / charts['top_roots'].name
        lines.append(f'![Top roots chart]({rel})\n\n')
    lines.append('| # | Root | Lemma | Count | % | Primary meaning |\n|---|---|---|---|---|---|\n')
    for i, row in top_roots_df.iterrows():
        lines.append(
            f"| {i+1} | {row['root']} | {row['lemma']} | {row['count']:,} | {row['pct']}% | {row['top_gloss']} |\n")  # noqa: E501
    lines.append('\n')

    lines.append('## 5. Niphal-Dominant Roots (≥80% of occurrences)\n\n')
    lines.append(
        'These roots rarely or never occur in the Qal — the Niphal IS their base meaning.\n\n'
    )
    lines.append('| Root | Lemma | Niphal | Total | % | Gloss |\n|---|---|---|---|---|---|\n')
    for _, row in dom_df.iterrows():
        lines.append(
            f"| {row['root']} | {row['lemma']} | {row['niphal_count']} | {row['total']} | {row['hif_pct']}% | {row['top_gloss']} |\n")  # noqa: E501
    lines.append('\n')

    lines.append('## 6. Semantic Function Categories\n\n')
    if charts['semantic']:
        rel = Path('../..') / 'charts' / 'ot' / 'verbs' / charts['semantic'].name
        lines.append(f'![Semantic categories pie chart]({rel})\n\n')
    lines.append('| Category | Count | % |\n|---|---|---|\n')
    for _, row in sem_df.iterrows():
        lines.append(f"| {row['category']} | {row['count']:,} | {row['pct']}% |\n")
    lines.append('\n')

    lines.append('## 7. Key Morphological Markers\n\n')
    lines.append('| Form | Diagnostic marker | Example |\n|---|---|---|\n')
    lines.append('| Perfect (qatal) 3ms | נִ- prefix | נִשְׁמַר |\n')
    lines.append('| Imperfect (yiqtol) 3ms | יִ- + doubling | יִשָּׁמֵר |\n')
    lines.append('| Wayyiqtol 3ms | וַיִּ- + doubling | וַיִּשָּׁמֵר |\n')
    lines.append('| Imperative ms | הִ- + doubling | הִשָּׁמֵר |\n')
    lines.append('| Inf. Construct | הִ- + doubling | הִשָּׁמֵר |\n')
    lines.append('| Inf. Absolute | נִ-..וֹ | נִשְׁמוֹר |\n')
    lines.append('| Participle ms | נִ-..אֶל | נִשְׁמָר |\n\n')

    report_path = out_dir / 'niphal_report.md'
    report_path.write_text(''.join(lines), encoding='utf-8')
    print(f"\nReport saved: {report_path}")
    return report_path
