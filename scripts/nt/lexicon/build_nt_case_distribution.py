"""Build NT case distribution by book report."""
import matplotlib; matplotlib.use('Agg')  # noqa: E702
import matplotlib.pyplot as plt
from pathlib import Path
from bible_grammar.nt.nt_noun_profile import nt_noun_case_profile

REPORT = Path('output/reports/nt/lexicon/nt-case-distribution-by-book.md')
CHART = Path('output/charts/nt/lexicon/nt-case-distribution-by-book.png')
for p in [REPORT.parent, CHART.parent]:
    p.mkdir(parents=True, exist_ok=True)

path = CHART
case_df = nt_noun_case_profile()
CASES = ['nominative', 'genitive', 'dative', 'accusative', 'vocative']
CASE_COLORS = ['#4292c6', '#2ca25f', '#fd8d3c', '#d62728', '#9e9ac8']

cases_present = [c for c in CASES if c in case_df.columns]
x = range(len(case_df))
width = 0.8 / len(cases_present)
fig, ax = plt.subplots(figsize=(14, 6))
for i, case in enumerate(cases_present):
    offsets = [xi + (i - len(cases_present) / 2 + 0.5) * width for xi in x]
    ax.bar(offsets, case_df[case], width=width, label=case.capitalize(),
           color=CASE_COLORS[i % len(CASE_COLORS)], edgecolor='white', linewidth=0.2)
ax.set_xticks(list(x))
ax.set_xticklabels(case_df.get('book', case_df.index).tolist(),
                   rotation=45, ha='right', fontsize=8)
ax.set_ylabel('Noun count')
ax.set_title('Greek NT Case Distribution by Book', fontsize=12, fontweight='bold')
ax.legend(loc='upper right', fontsize=8)
fig.tight_layout()
fig.savefig(CHART, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"Chart: {CHART}")

lines = [
    '# Greek NT Case Distribution by Book',
    '',
    '*Build script: [scripts/nt/lexicon/build_nt_case_distribution.py]'
    '(../../../../scripts/nt/lexicon/build_nt_case_distribution.py)*',
    '',
    '---',
    '',
    '![NT case distribution](../../../charts/nt/lexicon/nt-case-distribution-by-book.png)',
]
REPORT.write_text('\n'.join(lines))
print(f"Report: {REPORT}")
