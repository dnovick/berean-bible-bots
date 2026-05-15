"""Build 2nd person feminine plural perfect verbs report."""
import matplotlib; matplotlib.use('Agg')  # noqa: E702
import matplotlib.pyplot as plt
from pathlib import Path
from bible_grammar.core.query import query

REPORT = Path('output/reports/ot/verbs/2fp-perfect-verbs.md')
CHART = Path('output/charts/ot/verbs/2fp-perfect-by-book-stem-v3.png')
for p in [REPORT.parent, CHART.parent]:
    p.mkdir(parents=True, exist_ok=True)

df = query(testament='OT', part_of_speech='verb', person='2', number='plural',
           gender='feminine', conjugation='perfect')

book_counts = df.groupby('book').size().sort_values(ascending=False).reset_index(name='count')
total = len(df)

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(book_counts['book'], book_counts['count'], color='#9e9ac8', edgecolor='white')
ax.set_title('2fp Perfect Verbs by OT Book', fontsize=12, fontweight='bold')
ax.set_ylabel('Count')
plt.xticks(rotation=45, ha='right')
fig.tight_layout()
fig.savefig(CHART, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"Chart: {CHART}")

lines = [
    '# 2nd Person Feminine Plural Perfect Verbs in the OT',
    '',
    '*Build script: [scripts/ot/verbs/build_2fp_perfect.py]'
    '(../../../../scripts/ot/verbs/build_2fp_perfect.py)*',
    '',
    '---',
    '',
    f'Total occurrences: **{total}**',
    '',
    '![2fp perfect by book](../../../charts/ot/verbs/2fp-perfect-by-book-stem-v3.png)',
    '',
    '| Book | Count |',
    '|---|---|',
]
for _, r in book_counts.iterrows():
    lines.append(f"| {r['book']} | {r['count']} |")

REPORT.write_text('\n'.join(lines))
print(f"Report: {REPORT}")
