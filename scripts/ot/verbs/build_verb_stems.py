"""Build OT verb stem distribution reports: Genesis, OT total, Torah, and pie chart."""
import matplotlib; matplotlib.use('Agg')  # noqa: E702
import matplotlib.pyplot as plt
from pathlib import Path
from bible_grammar.lexical.stats import verb_stems_by_book

CHARTS = Path('output/charts/ot/verbs')
REPORTS = Path('output/reports/ot/verbs')
CHARTS.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

df_all = verb_stems_by_book(testament='OT')
STEMS = ['qal', 'niphal', 'piel', 'pual', 'hiphil', 'hophal', 'hithpael']
STEM_COLORS = {
    'qal': '#4292c6', 'niphal': '#2ca25f', 'piel': '#fd8d3c',
    'pual': '#9e9ac8', 'hiphil': '#d62728', 'hophal': '#a65628', 'hithpael': '#e7298a',
}


def _stacked_bar(data, title, path):
    books = data['book'].tolist()
    stems_present = [s for s in STEMS if s in data.columns]
    bottoms = [0.0] * len(books)
    fig, ax = plt.subplots(figsize=(13, 6))
    for stem in stems_present:
        vals = data[stem].tolist()
        ax.bar(books, vals, bottom=bottoms, label=stem.capitalize(),
               color=STEM_COLORS.get(stem, '#aaa'), edgecolor='white', linewidth=0.3)
        bottoms = [b + v for b, v in zip(bottoms, vals)]
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_ylabel('Verb count')
    ax.legend(loc='upper right', fontsize=8)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Chart: {path}")


# Genesis
gen = df_all[df_all['book'] == 'Gen']
_stacked_bar(gen, 'Hebrew Verb Stems — Genesis', CHARTS / 'genesis_verb_stems.png')

# Torah
torah = df_all[df_all['book'].isin(['Gen', 'Exo', 'Lev', 'Num', 'Deu'])]
_stacked_bar(torah, 'Hebrew Verb Stems in Torah Books', CHARTS / 'torah_verb_stems_grouped.png')

# OT total bar
ot_total_by_stem = df_all[[s for s in STEMS if s in df_all.columns]].sum()
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(ot_total_by_stem.index, ot_total_by_stem.values,
       color=[STEM_COLORS.get(s, '#aaa') for s in ot_total_by_stem.index], edgecolor='white')
ax.set_title('Hebrew Verb Stems — Entire Old Testament', fontsize=12, fontweight='bold')
ax.set_ylabel('Token count')
for bar, v in zip(ax.patches, ot_total_by_stem.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50,
            f'{int(v):,}', ha='center', fontsize=9)
fig.tight_layout()
fig.savefig(CHARTS / 'ot_verb_stems_total.png', dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"Chart: {CHARTS / 'ot_verb_stems_total.png'}")

# Pie
fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(ot_total_by_stem.values,
       labels=[s.capitalize() for s in ot_total_by_stem.index],
       autopct='%1.1f%%',
       colors=[STEM_COLORS.get(s, '#aaa') for s in ot_total_by_stem.index],
       startangle=140, explode=[0.03] * len(ot_total_by_stem))
ax.set_title('Hebrew Verb Stem Distribution — Old Testament', fontsize=12, fontweight='bold')
fig.tight_layout()
fig.savefig(CHARTS / 'ot-verb-stems-pie.png', dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"Chart: {CHARTS / 'ot-verb-stems-pie.png'}")


def _report(title, chart_rel, report_path, extra_lines=None):
    lines = [
        f'# {title}',
        '',
        '*Build script: [scripts/ot/verbs/build_verb_stems.py]'
        '(../../../../scripts/ot/verbs/build_verb_stems.py)*',
        '',
        '---',
        '',
        f'![Chart]({chart_rel})',
    ]
    if extra_lines:
        lines += extra_lines
    Path(report_path).write_text('\n'.join(lines))
    print(f"Report: {report_path}")


_report('Hebrew Verb Stems — Genesis',
        '../../../charts/ot/verbs/genesis_verb_stems.png',
        REPORTS / 'hebrew-verb-stems-genesis.md')
_report('Hebrew Verb Stems — Entire Old Testament',
        '../../../charts/ot/verbs/ot_verb_stems_total.png',
        REPORTS / 'hebrew-verb-stems-ot-total.md')
_report('Hebrew Verb Stems in Torah Books (Grouped)',
        '../../../charts/ot/verbs/torah_verb_stems_grouped.png',
        REPORTS / 'hebrew-verb-stems-torah-by-book.md')
_report('Hebrew Verb Stem Distribution — Old Testament',
        '../../../charts/ot/verbs/ot-verb-stems-pie.png',
        REPORTS / 'ot-verb-stems-pie.md')
