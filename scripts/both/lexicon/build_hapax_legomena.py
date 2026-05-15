"""Build hapax legomena by book report (OT + NT)."""
import matplotlib; matplotlib.use('Agg')  # noqa: E702
import matplotlib.pyplot as plt
from pathlib import Path
from bible_grammar.lexical.hapax import hapax_summary

REPORT = Path('output/reports/both/lexicon/hapax-legomena-by-book.md')
CHART_OT = Path('output/charts/ot/lexicon/hapax-ot-by-book.png')
CHART_NT = Path('output/charts/nt/lexicon/hapax-nt-by-book.png')
for p in [REPORT.parent, CHART_OT.parent, CHART_NT.parent]:
    p.mkdir(parents=True, exist_ok=True)

ot_df = hapax_summary(corpus='OT')
nt_df = hapax_summary(corpus='NT')


def _bar(df, title, path):
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.bar(df['book'], df['hapax_count'], color='#2b8cbe', edgecolor='white')
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_ylabel('Hapax legomena')
    ax.set_xlabel('Book')
    plt.xticks(rotation=45, ha='right', fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Chart: {path}")


_bar(ot_df, 'Hapax Legomena by OT Book', CHART_OT)
_bar(nt_df, 'Hapax Legomena by NT Book', CHART_NT)

ot_total = ot_df['hapax_count'].sum()
nt_total = nt_df['hapax_count'].sum()

lines = [
    '# Hapax Legomena by Biblical Book',
    '',
    '*Build script: [scripts/both/lexicon/build_hapax_legomena.py]'
    '(../../../../scripts/both/lexicon/build_hapax_legomena.py)*',
    '',
    '---',
    '',
    f'OT total: **{ot_total:,}** · NT total: **{nt_total:,}**',
    '',
    '## OT Hapax Legomena',
    '',
    '![OT hapax by book](../../../charts/ot/lexicon/hapax-ot-by-book.png)',
    '',
    '| Book | Hapax Count |',
    '|---|---|',
]
for _, r in ot_df.iterrows():
    lines.append(f"| {r['book']} | {r['hapax_count']} |")

lines += [
    '',
    '## NT Hapax Legomena',
    '',
    '![NT hapax by book](../../../charts/nt/lexicon/hapax-nt-by-book.png)',
    '',
    '| Book | Hapax Count |',
    '|---|---|',
]
for _, r in nt_df.iterrows():
    lines.append(f"| {r['book']} | {r['hapax_count']} |")

REPORT.write_text('\n'.join(lines))
print(f"Report: {REPORT}")
