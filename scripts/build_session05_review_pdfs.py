#!/usr/bin/env python3
"""Generate fillable PDFs for Session 5 review exercises.

Output path: data/courses/bbh/bbh-2026.1/session-05/exercises/<name>/<name>.pdf

Usage:
    python scripts/build_session05_review_pdfs.py
"""

from __future__ import annotations

import os
import sys
from typing import List, Tuple, Type

# Ensure src/ is on the path when run from repo root
_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO, 'src'))

from bible_grammar.exercise_pdf import ExercisePDF  # noqa: E402

_SESSION_DIR = os.path.join(
    _REPO, 'data', 'courses', 'bbh', 'bbh-2026.1', 'session-05', 'exercises'
)


# ---------------------------------------------------------------------------
# Exercise 1 — Letter Review (25 items)
# ---------------------------------------------------------------------------

LETTER_ROWS = [
    ['1',  'ף',  '', ''],
    ['2',  'כּ', '', ''],
    ['3',  'ד',  '', ''],
    ['4',  'ח',  '', ''],
    ['5',  'שׂ', '', ''],
    ['6',  'ץ',  '', ''],
    ['7',  'ת',  '', ''],
    ['8',  'ר',  '', ''],
    ['9',  'ע',  '', ''],
    ['10', 'פ',  '', ''],
    ['11', 'ן',  '', ''],
    ['12', 'ב',  '', ''],
    ['13', 'גּ', '', ''],
    ['14', 'ם',  '', ''],
    ['15', 'כ',  '', ''],
    ['16', 'א',  '', ''],
    ['17', 'שׁ', '', ''],
    ['18', 'ך',  '', ''],
    ['19', 'דּ', '', ''],
    ['20', 'תּ', '', ''],
    ['21', 'בּ', '', ''],
    ['22', 'ג',  '', ''],
    ['23', 'ה',  '', ''],
    ['24', 'פּ', '', ''],
    ['25', 'ט',  '', ''],
]

LETTER_ANSWERS = [
    ['1',  'ף',  'Pe Sofit',     'f as in "fan" — final form of פ; word-final only; always soft'],
    ['2',  'כּ', 'Kaf (hard)',   'k as in "king" — dagesh lene; hard form'],
    ['3',  'ד',  'Dalet (soft)', 'd / dh — soft form (no dagesh)'],
    ['4',  'ח',  'Ḥet',          'ch as in "Bach" — guttural; never takes dagesh forte'],
    ['5',  'שׂ', 'Sin',          's as in "sun" — left dot; same letter-shape as Shin'],
    ['6',  'ץ',  'Tsade Sofit',  'emphatic ts — final form of צ; word-final only'],
    ['7',  'ת',  'Taw (soft)',   't / th — soft form (no dagesh)'],
    ['8',  'ר',  'Resh',         'r (uvular) — resists dagesh forte'],
    ['9',  'ע',  'Ayin',         '(silent) — guttural; distinct from Alef'],
    ['10', 'פ',  'Pe (soft)',    'f as in "fan" — soft form (no dagesh)'],
    ['11', 'ן',  'Nun Sofit',    'n — final form of נ; word-final only'],
    ['12', 'ב',  'Bet (soft)',   'v as in "vine" — soft form (no dagesh)'],
    ['13', 'גּ', 'Gimel (hard)', 'g as in "go" — dagesh lene; hard form'],
    ['14', 'ם',  'Mem Sofit',    'm — final form of מ; word-final only'],
    ['15', 'כ',  'Kaf (soft)',   'kh as in "Bach" — soft form (no dagesh)'],
    ['16', 'א',  'Alef',         '(silent) — guttural; distinct from Ayin'],
    ['17', 'שׁ', 'Shin',         'sh as in "shoe" — right dot'],
    ['18', 'ך',  'Kaf Sofit',   'k / kh — final form of כ; word-final only'],
    ['19', 'דּ', 'Dalet (hard)', 'd as in "day" — dagesh lene; hard form'],
    ['20', 'תּ', 'Taw (hard)',   't as in "top" — dagesh lene; hard form'],
    ['21', 'בּ', 'Bet (hard)',   'b as in "boy" — dagesh lene; hard form'],
    ['22', 'ג',  'Gimel (soft)', 'g / gh — soft form (no dagesh)'],
    ['23', 'ה',  'He',           'h — guttural; often quiescent word-finally'],
    ['24', 'פּ', 'Pe (hard)',    'p as in "pan" — dagesh lene; hard form'],
    ['25', 'ט',  'Tet',          't as in "toy" — emphatic; NOT a Begadkephat letter'],
]


class LetterReviewPDF(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each Hebrew letter shown, identify: (1) Letter Name, (2) Sound. '
            'Focus on confusable pairs, sofit forms, and Begadkephat hard/soft variants.'
        )
        self.add_section_heading('Exercise — 25 items')
        self.add_generic_table(
            headers=['#', 'Letter', 'Name', 'Sound'],
            rows=LETTER_ROWS,
            col_ratios=[0.06, 0.10, 0.22, 0.62],
            heb_cols=[1],
            show_answers=False,
        )
        self.add_section_heading('Answer Key')
        self.add_generic_table(
            headers=['#', 'Letter', 'Name', 'Sound'],
            rows=LETTER_ANSWERS,
            col_ratios=[0.06, 0.10, 0.22, 0.62],
            heb_cols=[1],
            show_answers=True,
            answer_rows=LETTER_ANSWERS,
        )


# ---------------------------------------------------------------------------
# Exercise 2 — Vowel Review (20 items)
# ---------------------------------------------------------------------------

VOWEL_ROWS = [
    ['1',  'מָ',                      '', '', ''],
    ['2',  'מַ',                      '', '', ''],
    ['3',  'מֹ',                      '', '', ''],
    ['4',  'מִ',                      '', '', ''],
    ['5',  'מֵ',                      '', '', ''],
    ['6',  'מֶ',                      '', '', ''],
    ['7',  'מֻ',                      '', '', ''],
    ['8',  'מוּ',                     '', '', ''],
    ['9',  'מוֹ',                     '', '', ''],
    ['10', 'מִי',                     '', '', ''],
    ['11', 'מֵי',                     '', '', ''],
    ['12', 'מְ (word-initial)',        '', '', ''],
    ['13', 'מְ (word-final)',          '', '', ''],
    ['14', 'מָ (closed, unaccented)', '', '', ''],
    ['15', 'מֲ',                      '', '', ''],
    ['16', 'מֱ',                      '', '', ''],
    ['17', 'מֳ',                      '', '', ''],
    ['18', 'אָה',                     '', '', ''],
    ['19', 'אֹה',                     '', '', ''],
    ['20', 'אֵה',                     '', '', ''],
]

VOWEL_ANSWERS = [
    ['1',  'מָ',                      'Qamets',        'A',       'Long'],
    ['2',  'מַ',                      'Pathach',       'A',       'Short'],
    ['3',  'מֹ',                      'Holem',         'O',       'Long'],
    ['4',  'מִ',                      'Hireq',         'I',       'Short'],
    ['5',  'מֵ',                      'Tsere',         'E',       'Long'],
    ['6',  'מֶ',                      'Seghol',        'E',       'Short'],
    ['7',  'מֻ',                      'Qibbuts',       'U',       'Short'],
    ['8',  'מוּ',                     'Shureq',        'U',       'Long'],
    ['9',  'מוֹ',                     'Holem Waw',     'O',       'Long'],
    ['10', 'מִי',                     'Hireq Yod',     'I',       'Long'],
    ['11', 'מֵי',                     'Tsere Yod',     'E',       'Long'],
    ['12', 'מְ',                      'Vocal Shewa',   'Reduced', 'Reduced'],
    ['13', 'מְ',                      'Silent Shewa',  '—',       '—'],
    ['14', 'מָ',                      'Qamets Hatuf',  'O',       'Short'],
    ['15', 'מֲ',                      'Hateph Pathach','A',       'Reduced'],
    ['16', 'מֱ',                      'Hateph Seghol', 'E',       'Reduced'],
    ['17', 'מֳ',                      'Hateph Qamets', 'O',       'Reduced'],
    ['18', 'אָה',                     'Qamets He',     'A',       'Long'],
    ['19', 'אֹה',                     'Holem He',      'O',       'Long'],
    ['20', 'אֵה',                     'Tsere He',      'E',       'Long'],
]


class VowelReviewPDF(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each pointed Hebrew form shown, identify: (1) Vowel Name, '
            '(2) Vowel Class (A / E / I / O / U / Reduced), (3) Quantity (Long / Short / Reduced). '
            'The letter מ (Mem) is used as the carrier consonant for most items; '
            'א (Alef) for word-final ה forms.'
        )
        self.add_section_heading('Exercise — 20 items')
        self.add_generic_table(
            headers=['#', 'Form', 'Vowel Name', 'Class', 'Quantity'],
            rows=VOWEL_ROWS,
            col_ratios=[0.06, 0.22, 0.30, 0.18, 0.24],
            heb_cols=[1],
            show_answers=False,
        )
        self.add_section_heading('Answer Key')
        self.add_generic_table(
            headers=['#', 'Form', 'Vowel Name', 'Class', 'Quantity'],
            rows=VOWEL_ANSWERS,
            col_ratios=[0.06, 0.22, 0.30, 0.18, 0.24],
            heb_cols=[1],
            show_answers=True,
            answer_rows=VOWEL_ANSWERS,
        )


# ---------------------------------------------------------------------------
# Exercise 3 — Syllabification Review (15 words)
# ---------------------------------------------------------------------------

SYLL_ROWS = [
    ['1',  'אָב',   '', '', '', ''],
    ['2',  'בֵּן',  '', '', '', ''],
    ['3',  'בַּיִת','', '', '', ''],
    ['4',  'קוֹל', '', '', '', ''],
    ['5',  'יָד',   '', '', '', ''],
    ['6',  'מַיִם','', '', '', ''],
    ['7',  'שֶׁמֶשׁ','','', '', ''],
    ['8',  'אָדָם','', '', '', ''],
    ['9',  'פֶּה', '', '', '', ''],
    ['10', 'לֵב',  '', '', '', ''],
    ['11', 'עֵץ',  '', '', '', ''],
    ['12', 'אֱמֶת','', '', '', ''],
    ['13', 'נֶפֶשׁ','','', '', ''],
    ['14', 'מָוֶת','', '', '', ''],
    ['15', 'חֶרֶב','', '', '', ''],
]

SYLL_ANSWERS = [
    ['1',  'אָב',   'אָב',     'C',   'אָב*',   '—'],
    ['2',  'בֵּן',  'בֵּן',    'C',   'בֵּן*',  '—'],
    ['3',  'בַּיִת','בַּ-יִת', 'O-C', 'יִת*',   '—'],
    ['4',  'קוֹל', 'קוֹל',   'C',   'קוֹל*',  '—'],
    ['5',  'יָד',   'יָד',     'C',   'יָד*',   '—'],
    ['6',  'מַיִם','מַ-יִם',  'O-C', 'יִם*',   '—'],
    ['7',  'שֶׁמֶשׁ','שֶׁ-מֶשׁ','O-C','מֶשׁ*',  '—'],
    ['8',  'אָדָם','אָ-דָם',  'O-C', 'דָם*',   '—'],
    ['9',  'פֶּה', 'פֶּה',    'O',   'פֶּה*',  '—'],
    ['10', 'לֵב',  'לֵב',     'C',   'לֵב*',   '—'],
    ['11', 'עֵץ',  'עֵץ',     'C',   'עֵץ*',   '—'],
    ['12', 'אֱמֶת','אֱ-מֶת',  'O-C', 'מֶת*',   '—'],
    ['13', 'נֶפֶשׁ','נֶ-פֶשׁ', 'O-C', 'פֶשׁ*',  '—'],
    ['14', 'מָוֶת','מָ-וֶת',  'O-C', 'וֶת*',   '—'],
    ['15', 'חֶרֶב','חֶ-רֶב',  'O-C', 'רֶב*',   '—'],
]


class SyllabificationReviewPDF(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each Hebrew word: (1) divide into syllables with hyphens, '
            '(2) label each syllable O (open) or C (closed), '
            '(3) mark the stressed syllable with an asterisk (*), '
            '(4) note any Qamets Hatuf (write QH, or — if none). '
            'All words are from biblical Hebrew vocabulary in Ch1–3 or Genesis 1:1–5.'
        )
        self.add_section_heading('Exercise — 15 words')
        self.add_generic_table(
            headers=['#', 'Word', 'Division', 'Types', 'Stress', 'QH?'],
            rows=SYLL_ROWS,
            col_ratios=[0.05, 0.13, 0.22, 0.14, 0.22, 0.24],
            heb_cols=[1],
            show_answers=False,
        )
        self.add_section_heading('Answer Key')
        self.add_generic_table(
            headers=['#', 'Word', 'Division', 'Types', 'Stress', 'QH?'],
            rows=SYLL_ANSWERS,
            col_ratios=[0.05, 0.13, 0.22, 0.14, 0.22, 0.24],
            heb_cols=[1],
            show_answers=True,
            answer_rows=SYLL_ANSWERS,
            answer_heb_cols=[2, 4],
        )


# ---------------------------------------------------------------------------
# Exercise 4 — Dagesh: Forte vs. Lene (10 items)
# ---------------------------------------------------------------------------

DAGESH_ROWS = [
    ['1',  'הַשָּׁמַיִם', 'שּׁ', '', ''],
    ['2',  'בְּרֵאשִׁית', 'בּ',  '', ''],
    ['3',  'כִּי',         'כּ',  '', ''],
    ['4',  'הַמָּיִם',    'מּ',  '', ''],
    ['5',  'תּוֹרָה',     'תּ',  '', ''],
    ['6',  'מִשְׁפָּט',   'פּ',  '', ''],
    ['7',  'גּוֹי',        'גּ',  '', ''],
    ['8',  'וַיִּקְרָא', 'יּ',  '', ''],
    ['9',  'הַפָּנִים',   'פּ',  '', ''],
    ['10', 'דְּבַר',      'דּ',  '', ''],
]

DAGESH_ANSWERS = [
    ['1',  'הַשָּׁמַיִם', 'שּׁ', 'Forte', 'Shin is not Begadkephat → Forte; article assimilation'],
    ['2',  'בְּרֵאשִׁית', 'בּ',  'Lene',  'Begadkephat in word-initial position → Lene (hard b)'],
    ['3',  'כִּי',         'כּ',  'Lene',  'Begadkephat in word-initial position → Lene (hard k)'],
    ['4',  'הַמָּיִם',    'מּ',  'Forte', 'Mem is not Begadkephat → Forte; article assimilation'],
    ['5',  'תּוֹרָה',     'תּ',  'Lene',  'Begadkephat in word-initial position → Lene (hard t)'],
    ['6',  'מִשְׁפָּט',   'פּ',  'Forte', 'Begadkephat but follows closed syllable מִשׁ → Forte'],
    ['7',  'גּוֹי',        'גּ',  'Lene',  'Begadkephat in word-initial position → Lene (hard g)'],
    ['8',  'וַיִּקְרָא', 'יּ',  'Forte', 'Yod is not Begadkephat → Forte; Wayyiqtol prefix doubling'],
    ['9',  'הַפָּנִים',   'פּ',  'Forte', 'Begadkephat but follows article assimilation הַ → Forte'],
    ['10', 'דְּבַר',      'דּ',  'Lene',  'Begadkephat in stem-initial position → Lene (hard d)'],
]


class DageshReviewPDF(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each word, a target letter with a dagesh is shown. '
            'Identify whether the dagesh is Forte or Lene and state the reason. '
            'Key rule: if the letter is NOT a Begadkephat (bet gimel dalet kaf pe taw), '
            'any dagesh must be Forte.'
        )
        self.add_section_heading('Exercise — 10 items')
        self.add_generic_table(
            headers=['#', 'Word', 'Target', 'Forte or Lene?', 'Reason'],
            rows=DAGESH_ROWS,
            col_ratios=[0.05, 0.20, 0.10, 0.18, 0.47],
            heb_cols=[1, 2],
            show_answers=False,
        )
        self.add_section_heading('Answer Key')
        self.add_generic_table(
            headers=['#', 'Word', 'Target', 'Type', 'Reason'],
            rows=DAGESH_ANSWERS,
            col_ratios=[0.05, 0.20, 0.10, 0.14, 0.51],
            heb_cols=[1, 2],
            show_answers=True,
            answer_rows=DAGESH_ANSWERS,
        )


# ---------------------------------------------------------------------------
# Exercise 5 — Shewa: Vocal vs. Silent (10 items)
# ---------------------------------------------------------------------------

SHEWA_ROWS = [
    ['1',  'בְּרֵאשִׁית', 'בְּ (initial)',  '', ''],
    ['2',  'מֶלֶךְ',      'ךְ (final)',     '', ''],
    ['3',  'יְרוּשָׁלַיִם','יְ (initial)',   '', ''],
    ['4',  'מִשְׁפָּט',   'שְׁ (middle)',   '', ''],
    ['5',  'בְּרִית',     'בְּ (initial)',  '', ''],
    ['6',  'יִשְׂרָאֵל', 'שְׂ (middle)',   '', ''],
    ['7',  'כְּבוֹד',     'כְּ (initial)', '', ''],
    ['8',  'נִשְׁמַר',    'שְׁ (middle)',   '', ''],
    ['9',  'שְׁמַע',      'שְׁ (initial)', '', ''],
    ['10', 'יִשְׁלַח',    'שְׁ (middle)',  '', ''],
]

SHEWA_ANSWERS = [
    ['1',  'בְּרֵאשִׁית', 'בְּ',  'Vocal',  'Word-initial: every word begins with a vowel sound'],
    ['2',  'מֶלֶךְ',      'ךְ',   'Silent', 'Word-final: marks close of the last syllable; no sound'],
    ['3',  'יְרוּשָׁלַיִם','יְ',   'Vocal',  'Word-initial: Yod begins the word'],
    ['4',  'מִשְׁפָּט',   'שְׁ',  'Silent', 'Middle-of-word, not initial, no dagesh forte → closes syllable מִשׁ'],
    ['5',  'בְּרִית',     'בְּ',  'Vocal',  'Word-initial: Bet begins the word'],
    ['6',  'יִשְׂרָאֵל', 'שְׂ',  'Silent', 'Middle-of-word after short Hireq (יִ) → closes syllable יִשׂ'],
    ['7',  'כְּבוֹד',     'כְּ', 'Vocal',  'Word-initial: Kaf begins the word'],
    ['8',  'נִשְׁמַר',    'שְׁ',  'Silent', 'Middle-of-word after short Hireq (נִ) → closes syllable נִשׁ'],
    ['9',  'שְׁמַע',      'שְׁ',  'Vocal',  'Word-initial: Shin begins the word'],
    ['10', 'יִשְׁלַח',    'שְׁ',  'Silent', 'Middle-of-word after short Hireq (יִ) → closes syllable יִשׁ'],
]


class ShewaReviewPDF(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each word, a target letter bearing a shewa is identified. '
            'Determine whether the shewa is Vocal or Silent and state the rule. '
            'Vocal shewa: (1) word-initial, (2) after another shewa, (3) under dagesh forte. '
            'Silent shewa: (1) word-final, (2) all other positions.'
        )
        self.add_section_heading('Exercise — 10 items')
        self.add_generic_table(
            headers=['#', 'Word', 'Target', 'Vocal or Silent?', 'Rule'],
            rows=SHEWA_ROWS,
            col_ratios=[0.05, 0.22, 0.16, 0.18, 0.39],
            heb_cols=[1, 2],
            show_answers=False,
        )
        self.add_section_heading('Answer Key')
        self.add_generic_table(
            headers=['#', 'Word', 'Target', 'Type', 'Rule'],
            rows=SHEWA_ANSWERS,
            col_ratios=[0.05, 0.22, 0.10, 0.12, 0.51],
            heb_cols=[1, 2],
            show_answers=True,
            answer_rows=SHEWA_ANSWERS,
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def _out(name: str) -> str:
    d = os.path.join(_SESSION_DIR, name)
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, f'{name}.pdf')


def main() -> None:
    exercises: List[Tuple[Type[ExercisePDF], str, str, str]] = [
        (LetterReviewPDF,
         'Session 5 — Hebrew Letter Review',
         'BBH 2026.1 · Ch1–3 Review · 25 items',
         'session05-letter-review'),
        (VowelReviewPDF,
         'Session 5 — Hebrew Vowel Review',
         'BBH 2026.1 · Ch1–3 Review · 20 items',
         'session05-vowel-review'),
        (SyllabificationReviewPDF,
         'Session 5 — Syllabification Review',
         'BBH 2026.1 · Ch3 Review · 15 words',
         'session05-syllabification-review'),
        (DageshReviewPDF,
         'Session 5 — Dagesh: Forte vs. Lene',
         'BBH 2026.1 · Ch3 Review · 10 items',
         'session05-dagesh-review'),
        (ShewaReviewPDF,
         'Session 5 — Shewa: Vocal vs. Silent',
         'BBH 2026.1 · Ch3 Review · 10 items',
         'session05-shewa-review'),
    ]

    for klass, title, subtitle, name in exercises:
        path = _out(name)
        klass(title=title, subtitle=subtitle).save(path)
        print(f'  wrote {os.path.relpath(path, _REPO)}')

    print('Done.')


if __name__ == '__main__':
    main()
