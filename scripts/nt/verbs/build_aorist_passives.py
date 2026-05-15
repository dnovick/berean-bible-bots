"""Build Greek aorist passive verbs by NT book report."""
import matplotlib; matplotlib.use('Agg')  # noqa: E702
import matplotlib.pyplot as plt
from pathlib import Path
from bible_grammar.core.query import query

REPORT = Path('output/reports/nt/verbs/greek-aorist-passives-by-nt-book.md')
CHART = Path('output/charts/nt/verbs/nt_aorist_passive_by_book.png')
for p in [REPORT.parent, CHART.parent]:
    p.mkdir(parents=True, exist_ok=True)

df = query(testament='NT', part_of_speech='verb', tense='aorist', voice='passive')
book_counts = df.groupby('book').size().sort_values(ascending=False).reset_index(name='count')
total = len(df)

fig, ax = plt.subplots(figsize=(13, 6))
ax.bar(book_counts['book'], book_counts['count'], color='#d62728', edgecolor='white')
ax.set_title('Greek Aorist Passive Verbs by NT Book', fontsize=12, fontweight='bold')
ax.set_ylabel('Count')
plt.xticks(rotation=45, ha='right', fontsize=8)
fig.tight_layout()
fig.savefig(CHART, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"Chart: {CHART}")

lines = [
    '# Greek Aorist Passive Verbs by NT Book',
    '',
    '*Build script: [scripts/nt/verbs/build_aorist_passives.py]'
    '(../../../../scripts/nt/verbs/build_aorist_passives.py)*',
    '',
    '---',
    '',
    f'Total aorist passive tokens: **{total:,}**',
    '',
    '![NT aorist passives by book](../../../charts/nt/verbs/nt_aorist_passive_by_book.png)',
    '',
    '| Book | Count |',
    '|---|---|',
]
for _, r in book_counts.iterrows():
    lines.append(f"| {r['book']} | {r['count']} |")

REPORT.write_text('\n'.join(lines))
print(f"Report: {REPORT}")
