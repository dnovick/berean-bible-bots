"""Build nouns-by-gender-by-book report (OT + NT)."""
import matplotlib; matplotlib.use('Agg')  # noqa: E702
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from bible_grammar.ot.ot_noun_profile import ot_noun_gender_profile
from bible_grammar.nt.nt_noun_profile import nt_noun_gender_profile

REPORT = Path('output/reports/both/lexicon/nouns-by-gender-by-book.md')
CHART_OT = Path('output/charts/ot/lexicon/nouns-by-gender-ot.png')
CHART_NT = Path('output/charts/nt/lexicon/nouns-by-gender-nt.png')
for p in [REPORT.parent, CHART_OT.parent, CHART_NT.parent]:
    p.mkdir(parents=True, exist_ok=True)

ot_gender = ot_noun_gender_profile()
nt_gender = nt_noun_gender_profile()


def _stacked(df, title, path, colors):
    fig, ax = plt.subplots(figsize=(13, 6))
    df_pct = df.set_index('book').div(df.set_index('book').sum(axis=1), axis=0) * 100
    bottom = pd.Series([0.0] * len(df_pct), index=df_pct.index)
    for i, col in enumerate(df_pct.columns):
        ax.bar(df_pct.index, df_pct[col], bottom=bottom, label=col,
               color=colors[i % len(colors)], edgecolor='white', linewidth=0.3)
        bottom += df_pct[col]
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_ylabel('% of nouns')
    ax.legend(loc='upper right', fontsize=8)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Chart: {path}")


_stacked(ot_gender, 'OT Hebrew Nouns by Gender per Book',
         CHART_OT, ['#4292c6', '#d62728', '#41ab5d'])
_stacked(nt_gender, 'NT Greek Nouns by Gender per Book',
         CHART_NT, ['#4292c6', '#d62728', '#41ab5d'])

lines = [
    '# Nouns by Gender, Per Book',
    '',
    '*Build script: [scripts/both/lexicon/build_nouns_by_gender.py]'
    '(../../../../scripts/both/lexicon/build_nouns_by_gender.py)*',
    '',
    '---',
    '',
    '## OT Hebrew Nouns by Gender',
    '',
    '![OT nouns by gender](../../../charts/ot/lexicon/nouns-by-gender-ot.png)',
    '',
    '## NT Greek Nouns by Gender',
    '',
    '![NT nouns by gender](../../../charts/nt/lexicon/nouns-by-gender-nt.png)',
]
REPORT.write_text('\n'.join(lines))
print(f"Report: {REPORT}")
