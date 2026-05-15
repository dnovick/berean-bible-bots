"""Build semantic profile for H1285 בְּרִית (berith / covenant)."""
from bible_grammar.lexical.semantic_profile import save_semantic_profile

report_path = save_semantic_profile('H1285', output_dir='output/reports/ot/lexicon')
print(f"Report: {report_path}")
