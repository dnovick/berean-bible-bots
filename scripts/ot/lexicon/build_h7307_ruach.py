"""Build semantic profile for H7307 רוּחַ (ruach / spirit, wind, breath)."""
from bible_grammar.lexical.semantic_profile import save_semantic_profile

report_path = save_semantic_profile('H7307', output_dir='output/reports/ot/lexicon')
print(f"Report: {report_path}")
