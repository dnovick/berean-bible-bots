"""Build NT quotations of the OT overview report."""
from pathlib import Path
from bible_grammar.intertextuality.quotations import quotation_summary, nt_quotations

OUT = Path('output/reports/both/intertextuality')
OUT.mkdir(parents=True, exist_ok=True)

summary = quotation_summary(min_votes=25)
all_refs = nt_quotations(min_votes=10)

lines = [
    '# NT Quotations of the OT — Overview',
    '',
    '*Build script: [scripts/both/intertextuality/build_nt_quotations_overview.py]'
    '(../../../../scripts/both/intertextuality/build_nt_quotations_overview.py)*',
    '',
    '---',
    '',
    f'Total cross-references (min 10 votes): **{len(all_refs):,}**',
    '',
    '## Quotation Density by NT Book',
    '',
]

lines.append('| NT Book | Citations |')
lines.append('|---|---|')
for _, row in summary.sort_values('citations', ascending=False).iterrows():
    lines.append(f"| {row['nt_book']} | {row['citations']} |")

report_path = OUT / 'nt_quotations_overview.md'
report_path.write_text('\n'.join(lines))
print(f"Report: {report_path}")
