"""Build semantic profile for H7965 שָׁלוֹם (shalom / peace, wholeness)."""
from bible_grammar.lexical.semantic_profile import save_semantic_profile

report_path = save_semantic_profile('H7965', output_dir='output/reports/ot/lexicon')
print(f"Report: {report_path}")
