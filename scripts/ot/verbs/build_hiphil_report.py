"""Build Hiphil verb morphology report."""
from bible_grammar.stems.hiphil import hiphil_report

report_path = hiphil_report(output_dir='output/reports/ot/verbs')
print(f"Report: {report_path}")
