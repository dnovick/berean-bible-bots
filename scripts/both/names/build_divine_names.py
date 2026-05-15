"""Build divine names and Christological titles report (OT + LXX + NT)."""
from bible_grammar.names.divine_names import divine_names_report

report_path = divine_names_report(
    output_dir='output/reports/both/names',
    corpora=['OT', 'LXX', 'NT'],
)
print(f"Report: {report_path}")
