"""Build semantic profile for G3056 λόγος (logos / word, reason)."""
from bible_grammar.lexical.semantic_profile import save_semantic_profile

report_path = save_semantic_profile('G3056', output_dir='output/reports/nt/lexicon')
print(f"Report: {report_path}")
