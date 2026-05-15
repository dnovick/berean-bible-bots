"""Build genre comparison report: morphological patterns across literary sections."""
from bible_grammar.discourse.genre_compare import genre_report

report_path = genre_report(
    output_dir='output/reports/both/genre',
    ot_features=['verb_stem', 'verb_conjugation', 'part_of_speech'],
    nt_features=['verb_tense', 'verb_voice', 'verb_mood', 'part_of_speech'],
)
print(f"Report: {report_path}")
