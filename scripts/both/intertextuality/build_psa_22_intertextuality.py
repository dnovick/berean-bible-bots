"""Build Psalms 22 intertextuality network report and graph."""
from bible_grammar.intertextuality.intertextuality import intertextuality_report

report_path = intertextuality_report(
    'Psa', chapter=22, min_votes=20,
    output_dir='output/reports/both/intertextuality',
)
print(f"Report: {report_path}")
