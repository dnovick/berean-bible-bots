"""Build Greek 'obey' word study: NT + LXX occurrences of obedience vocabulary."""
from pathlib import Path
from bible_grammar.lexical.wordstudy import word_study
from bible_grammar.core.lxx_query import query_lxx

REPORT = Path('output/reports/nt/lexicon/obey-greek-word-study.md')
REPORT.parent.mkdir(parents=True, exist_ok=True)

# Key obedience words: G5219 ὑπακούω, G3982 πείθω, G3980 πειθαρχέω,
#                      G5293 ὑποτάσσω, G5255 ὑπήκοος
WORDS = [
    ('G5219', 'ὑπακούω', 'obey (hear under)'),
    ('G3982', 'πείθω', 'persuade / obey'),
    ('G3980', 'πειθαρχέω', 'obey authority'),
    ('G5293', 'ὑποτάσσω', 'submit / be subject'),
    ('G5255', 'ὑπήκοος', 'obedient'),
]

lines = [
    '# Greek Words for "Obey" — NT and LXX Word Study',
    '',
    '*Build script: [scripts/nt/lexicon/build_obey_word_study.py]'
    '(../../../../scripts/nt/lexicon/build_obey_word_study.py)*',
    '',
    '---',
    '',
    '| Strongs | Greek | Gloss | NT Count | LXX Count |',
    '|---|---|---|---|---|',
]

for strongs, greek, gloss in WORDS:
    study = word_study(strongs)
    nt_count = study.get('total_occurrences', 0)
    lxx = query_lxx(include_deuterocanon=False)
    lxx_count = len(lxx[lxx['dstrongs'].str.contains(strongs.lstrip('G'), na=False)])
    lines.append(f'| {strongs} | {greek} | {gloss} | {nt_count} | {lxx_count} |')

lines += [
    '',
    '## Detailed Profiles',
    '',
]
for strongs, greek, gloss in WORDS:
    study = word_study(strongs)
    lines += [
        f'### {greek} ({strongs}) — {gloss}',
        '',
        f'Total NT occurrences: **{study.get("total_occurrences", 0)}**',
        '',
    ]
    by_book = study.get('by_book', {})
    if by_book:
        lines += ['| Book | Count |', '|---|---|']
        for book, cnt in sorted(by_book.items(), key=lambda x: -x[1])[:10]:
            lines.append(f'| {book} | {cnt} |')
        lines.append('')

REPORT.write_text('\n'.join(lines))
print(f"Report: {REPORT}")
