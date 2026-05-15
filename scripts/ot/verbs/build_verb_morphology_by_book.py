"""Build comprehensive verb morphology by book report (OT stems + NT tense/mood)."""
import matplotlib; matplotlib.use('Agg')  # noqa: E702
import matplotlib.pyplot as plt
from pathlib import Path
from bible_grammar.lexical.stats import verb_stems_by_book, greek_verb_forms

REPORT = Path('output/reports/ot/verbs/verb-morphology-by-book.md')
CHART_OT = Path('output/charts/ot/verbs/verb-stems-ot-by-book.png')
CHART_NT_TENSE = Path('output/charts/nt/verbs/verb-tenses-nt-by-book.png')
CHART_NT_MOOD = Path('output/charts/nt/verbs/verb-moods-nt-by-book.png')
for p in [REPORT.parent, CHART_OT.parent, CHART_NT_TENSE.parent]:
    p.mkdir(parents=True, exist_ok=True)

ot_df = verb_stems_by_book(testament='OT')
nt_df = greek_verb_forms()

STEMS = ['qal', 'niphal', 'piel', 'pual', 'hiphil', 'hophal', 'hithpael']
STEM_COLORS = ['#4292c6', '#2ca25f', '#fd8d3c', '#9e9ac8', '#d62728', '#a65628', '#e7298a']


def _grouped_bar(data, cats, colors, title, path, ylabel='Count'):
    cats_present = [c for c in cats if c in data.columns]
    x = range(len(data))
    width = 0.8 / len(cats_present)
    fig, ax = plt.subplots(figsize=(16, 6))
    for i, cat in enumerate(cats_present):
        offsets = [xi + (i - len(cats_present) / 2 + 0.5) * width for xi in x]
        ax.bar(offsets, data[cat], width=width, label=cat.capitalize(),
               color=colors[i % len(colors)], edgecolor='white', linewidth=0.2)
    ax.set_xticks(list(x))
    ax.set_xticklabels(data['book'].tolist(), rotation=45, ha='right', fontsize=7)
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.legend(loc='upper right', fontsize=7, ncol=2)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Chart: {path}")


_grouped_bar(ot_df, STEMS, STEM_COLORS,
             'OT Verb Stems by Book', CHART_OT)

NT_TENSES = ['present', 'imperfect', 'future', 'aorist', 'perfect', 'pluperfect']
NT_MOODS = ['indicative', 'subjunctive', 'imperative', 'infinitive', 'participle', 'optative']
NT_COLORS_T = ['#2b8cbe', '#7bccc4', '#f0a500', '#d62728', '#9467bd', '#bcbd22']
NT_COLORS_M = ['#4292c6', '#2ca25f', '#fd8d3c', '#9e9ac8', '#d62728', '#bcbd22']

_grouped_bar(nt_df, NT_TENSES, NT_COLORS_T,
             'NT Verb Tenses by Book', CHART_NT_TENSE)
_grouped_bar(nt_df, NT_MOODS, NT_COLORS_M,
             'NT Verb Moods by Book', CHART_NT_MOOD)

lines = [
    '# Verb Morphology by Book',
    '',
    '*Build script: [scripts/ot/verbs/build_verb_morphology_by_book.py]'
    '(../../../../scripts/ot/verbs/build_verb_morphology_by_book.py)*',
    '',
    '---',
    '',
    '## OT Hebrew Verb Stems by Book',
    '',
    '![OT verb stems by book](../../../charts/ot/verbs/verb-stems-ot-by-book.png)',
    '',
    '## NT Greek Verb Tenses by Book',
    '',
    '![NT verb tenses by book](../../../charts/nt/verbs/verb-tenses-nt-by-book.png)',
    '',
    '## NT Greek Verb Moods by Book',
    '',
    '![NT verb moods by book](../../../charts/nt/verbs/verb-moods-nt-by-book.png)',
]
REPORT.write_text('\n'.join(lines))
print(f"Report: {REPORT}")
