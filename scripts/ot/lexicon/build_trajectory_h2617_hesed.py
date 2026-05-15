"""Build cross-testament trajectory for H2617 חֶסֶד (hesed / lovingkindness)."""
from bible_grammar.lexical.trajectory import save_trajectory_report

report_path = save_trajectory_report('H2617', output_dir='output/reports/ot/lexicon')
print(f"Report: {report_path}")
