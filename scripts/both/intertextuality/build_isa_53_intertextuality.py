"""Build Isaiah 53 intertextuality network report and graph."""
from bible_grammar.intertextuality.intertextuality import intertextuality_report

report_path = intertextuality_report(
    'Isa', chapter=53, min_votes=20,
    output_dir='output/reports/both/intertextuality',
)
print(f"Report: {report_path}")
