"""Build Niphal perfect verb distribution reports (all books + top-20)."""
import matplotlib; matplotlib.use('Agg')  # noqa: E702
import matplotlib.pyplot as plt
from pathlib import Path
from bible_grammar.lexical.stats import niphal_perfects_by_book

REPORT_ALL = Path('output/reports/ot/verbs/niphal-perfects-by-book.md')
REPORT_TOP = Path('output/reports/ot/verbs/niphal-perfects-by-book-top20.md')
CHART_ALL = Path('output/charts/ot/verbs/niphal_perfects.png')
CHART_TOP = Path('output/charts/ot/verbs/niphal_perfects_by_book.png')
for p in [REPORT_ALL.parent, CHART_ALL.parent]:
    p.mkdir(parents=True, exist_ok=True)

df = niphal_perfects_by_book()
top20 = df.head(20)


def _bar(data, title, path):
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.bar(data['book'], data['count'], color='#2b8cbe', edgecolor='white')
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_ylabel('Niphal Perfect count')
    plt.xticks(rotation=45, ha='right', fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Chart: {path}")


_bar(df, 'Niphal Perfect Verbs by OT Book', CHART_ALL)
_bar(top20, 'Niphal Perfect Verbs — Top 20 Books', CHART_TOP)


def _report(data, title, report_path, chart_path):
    lines = [
        f'# {title}',
        '',
        '*Build script: [scripts/ot/verbs/build_niphal_reports.py]'
        '(../../../../scripts/ot/verbs/build_niphal_reports.py)*',
        '',
        '---',
        '',
        f'![Chart]({chart_path})',
        '',
        f'Total: **{data["count"].sum():,}**',
        '',
        '| Book | Count |',
        '|---|---|',
    ]
    for _, r in data.iterrows():
        lines.append(f"| {r['book']} | {r['count']} |")
    Path(report_path).write_text('\n'.join(lines))
    print(f"Report: {report_path}")


_report(df, 'Niphal Perfect Verbs by OT Book',
        REPORT_ALL, '../../../charts/ot/verbs/niphal_perfects.png')
_report(top20, 'Niphal Perfect Verbs by OT Book (Top 20)',
        REPORT_TOP, '../../../charts/ot/verbs/niphal_perfects_by_book.png')
