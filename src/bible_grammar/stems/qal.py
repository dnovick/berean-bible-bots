"""
Qal verb morphology analysis for Biblical Hebrew instruction.

The Qal (קַל) is the base stem of Biblical Hebrew — the simplest,
most common, and most semantically transparent verb form. It accounts
for roughly half of all OT verb tokens. Every other stem (Niphal,
Piel, Pual, Hiphil, Hophal, Hithpael) is derived from it.

Semantic range of the Qal:
  • Simple action (active): כָּתַב (wrote), אָכַל (ate), הָלַךְ (went)
  • Simple state (stative): יָדַע (knew), אָהַב (loved), כָּבֵד (was heavy)
  • Fientive (dynamic) vs. stative verbs behave differently in pointing

All functions use MACULA Hebrew WLC data (load_syntax_ot).

Public API
──────────
qal_data()                           → DataFrame (all Qal tokens)
qal_conjugation_profile(book=None)   → DataFrame (type_ distribution)
qal_top_roots(n=30, book=None)       → DataFrame (most frequent roots)
qal_root_conjugation(roots=None)     → DataFrame (root × conjugation crosstab)
qal_book_distribution()              → DataFrame (count + pct per book)
qal_stem_comparison(books=None)      → DataFrame (all stems % by book)
qal_dominant_roots(min_pct=70)       → DataFrame (roots >X% Qal)
qal_semantic_categories()            → DataFrame (semantic function counts)

print_qal_overview()                 → None
print_qal_conjugation(book=None)     → None
print_qal_top_roots(n=20, book=None) → None
print_qal_root_conjugation(roots=None) → None
print_qal_book_distribution()        → None
print_qal_dominant_roots()           → None
print_qal_semantic_categories()      → None

qal_conjugation_chart(book=None)     → Path | None
qal_book_chart()                     → Path | None
qal_stem_chart(books=None)           → Path | None
qal_root_heatmap(top_n=15)           → Path | None

qal_report(output_dir=None)          → Path   (full Markdown report)
"""

from __future__ import annotations
import functools
from pathlib import Path

from ._stem_analysis import StemAnalysis, StemConfig, _DEFAULT_CONJ_ORDER


# ── Conjugation order — Qal includes participle passive ───────────────────────

_QAL_CONJ_ORDER: list[str] = list(_DEFAULT_CONJ_ORDER) + ['participle passive']


# ── Semantic function classifier ──────────────────────────────────────────────

_STATIVE_KEYWORDS = (
    'was', 'were', 'is', 'be', 'been', 'being',
    'knew', 'know', 'loved', 'love', 'hated', 'hate',
    'feared', 'fear', 'trusted', 'trust',
    'heavy', 'small', 'great', 'strong', 'weak', 'full', 'empty',
    'good', 'evil', 'old', 'young', 'sick', 'hungry', 'thirsty',
    'remained', 'dwelt', 'dwell', 'sat', 'sit', 'stood', 'stand',
)

_MOTION_KEYWORDS = (
    'went', 'go', 'came', 'come', 'walked', 'walk', 'ran', 'run',
    'fled', 'flee', 'returned', 'return', 'ascended', 'ascend',
    'descended', 'descend', 'crossed', 'cross', 'entered', 'enter',
    'went out', 'came out', 'went up', 'came up', 'went down', 'came down',
)

_SPEECH_KEYWORDS = (
    'said', 'say', 'spoke', 'speak', 'called', 'call', 'cried', 'cry',
    'answered', 'answer', 'asked', 'ask', 'commanded', 'command',
    'declared', 'declare', 'proclaimed', 'proclaim',
)

_CREATION_WORSHIP_KEYWORDS = (
    'created', 'create', 'made', 'make', 'built', 'build', 'formed', 'form',
    'worshiped', 'worship', 'bowed', 'bow', 'praised', 'praise',
    'blessed', 'bless', 'prayed', 'pray', 'offered', 'offer',
    'sacrificed', 'sacrifice',
)


def _qal_semantic_fn(gloss: str) -> str:
    g = str(gloss).strip().lower()
    if any(w in g for w in _SPEECH_KEYWORDS):
        return 'speech / communication'
    if any(w in g for w in _MOTION_KEYWORDS):
        return 'motion / movement'
    if any(w in g for w in _CREATION_WORSHIP_KEYWORDS):
        return 'creation / worship'
    if any(w in g for w in _STATIVE_KEYWORDS):
        return 'stative / condition'
    return 'other action'


# ── Config + analysis engine ──────────────────────────────────────────────────

_CONFIG = StemConfig(
    name='qal',
    macula_value='qal',
    display='Qal (קַל)',
    conj_order=_QAL_CONJ_ORDER,
    chart_color='#5B9BD5',  # blue — the Qal color used in all stem comparison charts
)

_ANALYSIS = StemAnalysis(_CONFIG)


# ── Public API ────────────────────────────────────────────────────────────────

qal_data                    = _ANALYSIS.data
qal_conjugation_profile     = _ANALYSIS.conjugation_profile
qal_top_roots               = _ANALYSIS.top_roots
qal_root_conjugation        = _ANALYSIS.root_conjugation
qal_book_distribution       = _ANALYSIS.book_distribution
qal_stem_comparison         = _ANALYSIS.stem_comparison
qal_dominant_roots          = _ANALYSIS.dominant_roots

qal_semantic_categories       = functools.partial(_ANALYSIS.semantic_categories, _qal_semantic_fn)
print_qal_semantic_categories = functools.partial(_ANALYSIS.print_semantic_categories, _qal_semantic_fn)
qal_semantic_chart            = functools.partial(_ANALYSIS.semantic_chart, _qal_semantic_fn)

print_qal_overview          = _ANALYSIS.print_overview
print_qal_conjugation       = _ANALYSIS.print_conjugation
print_qal_top_roots         = _ANALYSIS.print_top_roots
print_qal_root_conjugation  = _ANALYSIS.print_root_conjugation
print_qal_book_distribution = _ANALYSIS.print_book_distribution
print_qal_dominant_roots    = _ANALYSIS.print_dominant_roots

qal_conjugation_chart       = _ANALYSIS.conjugation_chart
qal_book_chart              = _ANALYSIS.book_chart
qal_stem_chart              = _ANALYSIS.stem_comparison_chart
qal_root_heatmap            = _ANALYSIS.root_heatmap
qal_top_roots_chart         = _ANALYSIS.top_roots_chart


def qal_report(output_dir: str | None = None) -> Path:
    """Generate a complete Qal morphology report (Markdown + PNG charts)."""
    if output_dir is None:
        out_dir = Path('output') / 'reports' / 'ot' / 'verbs'
    else:
        out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Generating charts...")
    charts: dict[str, Path | None] = {
        'conjugation': qal_conjugation_chart(),
        'books':       qal_book_chart(),
        'stems':       qal_stem_chart(),
        'heatmap':     qal_root_heatmap(),
        'semantic':    qal_semantic_chart(),
        'top_roots':   qal_top_roots_chart(),
    }
    for k, p in charts.items():
        if p:
            print(f"  ✓ {k}: {p}")

    df_full = _ANALYSIS._load()
    h = _ANALYSIS._stem_df(df_full)
    total_tokens = len(h)
    total_verbs = len(df_full[df_full['class_'] == 'verb'])
    unique_roots = h['_lem'].nunique()

    conj_df     = qal_conjugation_profile()
    top_roots_df = qal_top_roots(20)
    dom_df      = qal_dominant_roots(min_pct=90, min_tokens=20).head(20)
    sem_df      = qal_semantic_categories()
    book_df     = qal_book_distribution().head(20)

    lines: list[str] = []
    lines.append('# Qal (קַל) Verb Morphology — Biblical Hebrew\n\n')
    lines.append('*Generated from MACULA Hebrew WLC data*\n\n---\n\n')

    lines.append('## 1. Overview\n\n')
    lines.append(
        'The **Qal** is the base stem of Biblical Hebrew — the simplest, most common, '
        'and most semantically transparent verb form. All derived stems (Niphal, Piel, '
        'Pual, Hiphil, Hophal, Hithpael) add morphological elements to the Qal root.\n\n'
    )
    lines.append('| Statistic | Value |\n|---|---|\n')
    lines.append(f'| Total Qal tokens (OT)   | {total_tokens:,} |\n')
    lines.append(f'| % of all OT verb tokens | {total_tokens/total_verbs*100:.1f}% |\n')
    lines.append(f'| Unique roots in Qal     | {unique_roots:,} |\n\n')

    lines.append('## 2. Conjugation Distribution\n\n')
    lines.append('| Conjugation | Count | % |\n|---|---|---|\n')
    for _, row in conj_df.iterrows():
        if row['count'] > 0:
            lines.append(f"| {row['form']} | {row['count']:,} | {row['pct']}% |\n")
    lines.append('\n')

    lines.append('## 3. Distribution Across Books (top 20)\n\n')
    lines.append('| Book | Count | % of OT Qal | % of book verbs |\n|---|---|---|---|\n')
    for _, row in book_df.iterrows():
        lines.append(
            f"| {row['book']} | {row['count']:,} | {row['pct']}% | {row['pct_of_book_verbs']}% |\n")
    lines.append('\n')

    lines.append('## 4. Most Frequent Qal Roots (top 20)\n\n')
    lines.append('| # | Root | Lemma | Count | % | Primary meaning |\n|---|---|---|---|---|---|\n')
    for i, row in top_roots_df.iterrows():
        lines.append(
            f"| {i+1} | {row['root']} | {row['lemma']} | {row['count']:,} | {row['pct']}% | {row['top_gloss']} |\n")
    lines.append('\n')

    lines.append('## 5. Qal-Dominant Roots (≥90%)\n\n')
    lines.append('| Root | Lemma | Qal | Total | % | Gloss |\n|---|---|---|---|---|---|\n')
    for _, row in dom_df.iterrows():
        lines.append(
            f"| {row['root']} | {row['lemma']} | {row['niphal_count']} | {row['total']} | {row['hif_pct']}% | {row['top_gloss']} |\n")
    lines.append('\n')

    lines.append('## 6. Semantic Function Categories\n\n')
    lines.append('| Category | Count | % |\n|---|---|---|\n')
    for _, row in sem_df.iterrows():
        lines.append(f"| {row['category']} | {row['count']:,} | {row['pct']}% |\n")
    lines.append('\n')

    report_path = out_dir / 'qal_report.md'
    report_path.write_text(''.join(lines), encoding='utf-8')
    print(f"\nReport saved: {report_path}")
    return report_path
