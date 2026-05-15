"""Build NT verb tense×voice heatmaps: full NT and Pauline corpus."""
import matplotlib; matplotlib.use('Agg')  # noqa: E702
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from bible_grammar.lexical.stats import greek_verb_forms

REPORT_NT = Path('output/reports/nt/verbs/greek-nt-tense-voice-heatmap.md')
REPORT_PAU = Path('output/reports/nt/verbs/greek-pauline-tense-voice-heatmap.md')
CHART_NT = Path('output/charts/nt/verbs/nt_tense_voice.png')
CHART_PAU = Path('output/charts/nt/verbs/pauline_tense_voice.png')
for p in [REPORT_NT.parent, CHART_NT.parent]:
    p.mkdir(parents=True, exist_ok=True)

PAULINE = ['Rom', '1Co', '2Co', 'Gal', 'Eph', 'Php', 'Col',
           '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm']

nt_df = greek_verb_forms()
pau_df = greek_verb_forms(book_group='pauline') if hasattr(greek_verb_forms, 'book_group') else \
    greek_verb_forms()[greek_verb_forms()['book'].isin(PAULINE)] if 'book' in greek_verb_forms().columns \
    else nt_df[nt_df.index.isin(PAULINE)]

TENSES = ['present', 'imperfect', 'future', 'aorist', 'perfect', 'pluperfect']
VOICES = ['active', 'middle', 'passive']


def _heatmap(pivot, title, path):
    fig, ax = plt.subplots(figsize=(10, 5))
    im = ax.imshow(pivot.values, aspect='auto', cmap='Blues')
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, fontsize=10)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=10)
    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            v = int(pivot.values[i, j])
            ax.text(j, i, f'{v:,}', ha='center', va='center', fontsize=9,
                    color='white' if v > pivot.values.max() * 0.5 else 'black')
    ax.set_title(title, fontsize=12, fontweight='bold')
    plt.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Chart: {path}")


def _pivot_tense_voice(df):
    tenses = [t for t in TENSES if t in df.columns]
    voices = [v for v in VOICES if v in df.columns]
    rows = []
    for t in tenses:
        row = {}
        for v in voices:
            if t in df.columns and v in df.columns:
                row[v] = df[t].sum()  # simplified; real impl uses crosstab
        rows.append(row)
    return pd.DataFrame(rows, index=tenses, columns=voices).fillna(0)


from bible_grammar.core.query import query as raw_query  # noqa: E402
nt_raw = raw_query(testament='NT', part_of_speech='verb')
pau_raw = raw_query(testament='NT', part_of_speech='verb',
                    book=PAULINE[0])  # placeholder

nt_crosstab = pd.crosstab(nt_raw['tense'], nt_raw['voice']).fillna(0)
nt_crosstab = nt_crosstab.reindex(
    [t for t in TENSES if t in nt_crosstab.index],
    columns=[v for v in VOICES if v in nt_crosstab.columns],
    fill_value=0)

pau_raw = nt_raw[nt_raw['book'].isin(PAULINE)]
pau_crosstab = pd.crosstab(pau_raw['tense'], pau_raw['voice']).fillna(0)
pau_crosstab = pau_crosstab.reindex(
    [t for t in TENSES if t in pau_crosstab.index],
    columns=[v for v in VOICES if v in pau_crosstab.columns],
    fill_value=0)

_heatmap(nt_crosstab, 'Greek NT Verb Tense × Voice', CHART_NT)
_heatmap(pau_crosstab, 'Greek Verb Tense × Voice — Pauline Letters', CHART_PAU)


def _report(title, chart_rel, report_path):
    lines = [
        f'# {title}',
        '',
        '*Build script: [scripts/nt/verbs/build_tense_voice_heatmaps.py]'
        '(../../../../scripts/nt/verbs/build_tense_voice_heatmaps.py)*',
        '',
        '---',
        '',
        f'![Tense-voice heatmap]({chart_rel})',
    ]
    Path(report_path).write_text('\n'.join(lines))
    print(f"Report: {report_path}")


_report('Greek NT Verb Tense × Voice Heatmap',
        '../../../charts/nt/verbs/nt_tense_voice.png',
        REPORT_NT)
_report('Greek Verb Tense × Voice in Pauline Letters',
        '../../../charts/nt/verbs/pauline_tense_voice.png',
        REPORT_PAU)
