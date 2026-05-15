"""Build OT Hebrew vs. Aramaic word distribution report."""
import matplotlib; matplotlib.use('Agg')  # noqa: E702
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from bible_grammar.core.query import query

REPORT = Path('output/reports/ot/lexicon/ot-hebrew-aramaic-by-book.md')
CHART = Path('output/charts/ot/lexicon/ot-hebrew-aramaic-by-book.png')
for p in [REPORT.parent, CHART.parent]:
    p.mkdir(parents=True, exist_ok=True)

df = query(testament='OT')
lang_book = df.groupby(['book', 'language']).size().unstack(fill_value=0).reset_index()
lang_book['total'] = lang_book.get('Hebrew', 0) + lang_book.get('Aramaic', 0)
lang_book['aramaic_pct'] = (lang_book.get('Aramaic', 0) / lang_book['total'] * 100).round(1)
lang_book = lang_book[lang_book.get('Aramaic', pd.Series([0] * len(lang_book))).gt(0)]
lang_book = lang_book.sort_values('aramaic_pct', ascending=False)

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(lang_book['book'], lang_book['aramaic_pct'], color='#d62728', edgecolor='white')
ax.set_title('OT Aramaic Word % by Book', fontsize=12, fontweight='bold')
ax.set_ylabel('Aramaic %')
ax.set_xlabel('Book')
plt.xticks(rotation=45, ha='right')
fig.tight_layout()
fig.savefig(CHART, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"Chart: {CHART}")

lines = [
    '# Hebrew vs. Aramaic Word Distribution in the OT',
    '',
    '*Build script: [scripts/ot/lexicon/build_ot_hebrew_aramaic.py]'
    '(../../../../scripts/ot/lexicon/build_ot_hebrew_aramaic.py)*',
    '',
    '---',
    '',
    '![OT Hebrew vs Aramaic](../../../charts/ot/lexicon/ot-hebrew-aramaic-by-book.png)',
    '',
    '| Book | Hebrew | Aramaic | Aramaic % |',
    '|---|---|---|---|',
]
for _, r in lang_book.iterrows():
    heb = int(r.get('Hebrew', 0))
    ara = int(r.get('Aramaic', 0))
    lines.append(f"| {r['book']} | {heb:,} | {ara:,} | {r['aramaic_pct']}% |")

REPORT.write_text('\n'.join(lines))
print(f"Report: {REPORT}")
