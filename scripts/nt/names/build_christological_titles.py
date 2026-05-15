"""Build Christological titles report: Jesus's self-designations in the Gospels."""
from bible_grammar.names.christological_titles import title_report

report_path = title_report(
    output_dir='output/reports/nt/names',
    include_verses=True,
)
print(f"Report: {report_path}")
