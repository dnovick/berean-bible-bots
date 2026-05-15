"""Build syntactic role analysis for YHWH/Elohim in the OT."""
from bible_grammar.names.role_search import role_report

# YHWH = H3068, Elohim = H430
report_path = role_report(
    subject_strongs=['H3068', 'H430'],
    corpus='OT',
    top_n=30,
    label='YHWH/Elohim',
    output_dir='output/reports/ot/names',
    include_cross_testament=True,
)
print(f"Report: {report_path}")
