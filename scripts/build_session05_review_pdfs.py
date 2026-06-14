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
# Exercise 1 — Letter Review (20 items — confusable pairs focus)
# ---------------------------------------------------------------------------

LETTER_ROWS = [
    ['1',  'ה',  '', ''],
    ['2',  'ח',  '', ''],
    ['3',  'ד',  '', ''],
    ['4',  'ר',  '', ''],
    ['5',  'ו',  '', ''],
    ['6',  'ז',  '', ''],
    ['7',  'שׁ', '', ''],
    ['8',  'שׂ', '', ''],
    ['9',  'ב',  '', ''],
    ['10', 'כ',  '', ''],
    ['11', 'כּ', '', ''],
    ['12', 'ק',  '', ''],
    ['13', 'מ',  '', ''],
    ['14', 'ס',  '', ''],
    ['15', 'ם',  '', ''],
    ['16', 'ן',  '', ''],
    ['17', 'ף',  '', ''],
    ['18', 'ץ',  '', ''],
    ['19', 'ך',  '', ''],
    ['20', 'א',  '', ''],
]

LETTER_ANSWERS = [
    ['1',  'ה',  'He',           'h — guttural; often quiescent at word-end'],
    ['2',  'ח',  'Ḥet',          'ch as in "Bach" — guttural; stronger throat sound than He'],
    ['3',  'ד',  'Dalet (soft)', 'd / dh — soft form; no dagesh'],
    ['4',  'ר',  'Resh',         'r (uvular) — never takes dagesh forte'],
    ['5',  'ו',  'Waw',          'w — also used as mater lectionis for O and U vowels'],
    ['6',  'ז',  'Zayin',        'z — one horizontal bar on top; contrast with Waw'],
    ['7',  'שׁ', 'Shin',         'sh as in "ship" — right dot; contrast with Sin'],
    ['8',  'שׂ', 'Sin',          's as in "sun" — left dot; contrast with Shin'],
    ['9',  'ב',  'Bet (soft)',   'v as in "vine" — soft form; no dagesh'],
    ['10', 'כ',  'Kaf (soft)',   'kh as in "Bach" — soft form; no dagesh'],
    ['11', 'כּ', 'Kaf (hard)',   'k as in "king" — dagesh lene; hard form'],
    ['12', 'ק',  'Qof',          'q (uvular k) — never a Begadkephat letter'],
    ['13', 'מ',  'Mem',          'm — open at bottom'],
    ['14', 'ס',  'Samek',        's — fully closed letter; contrast with Mem\'s open bottom'],
    ['15', 'ם',  'Mem Sofit',    'm — closed final form; word-final only'],
    ['16', 'ן',  'Nun Sofit',    'n — descending final form; word-final only'],
    ['17', 'ף',  'Pe Sofit',     'f — final form of Pe; word-final only'],
    ['18', 'ץ',  'Tsade Sofit',  'emphatic ts — final form of Tsade; word-final only'],
    ['19', 'ך',  'Kaf Sofit',   'kh — final form of Kaf; word-final only'],
    ['20', 'א',  'Alef',         '(silent) — guttural; contrast with Ayin'],
]


class LetterReviewPDF(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each Hebrew letter shown, identify: (1) Letter Name, (2) Sound. '
            'Items are grouped by confusable pairs — study them in contrast.'
        )
        self.add_section_heading('Exercise — 20 items')
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
# Exercise 2 — Vowel Review (15 items — confusable pairs focus)
# ---------------------------------------------------------------------------

VOWEL_ROWS = [
    ['1',  'בָּ (open, accented)',      '', '', ''],
    ['2',  'בַּ',                       '', '', ''],
    ['3',  'בָּ (closed, unaccented)',  '', '', ''],
    ['4',  'בֵּ',                       '', '', ''],
    ['5',  'בֶּ',                       '', '', ''],
    ['6',  'בִּ',                       '', '', ''],
    ['7',  'מִי',                       '', '', ''],
    ['8',  'מֵי',                       '', '', ''],
    ['9',  'בֹּ',                       '', '', ''],
    ['10', 'בּוֹ',                      '', '', ''],
    ['11', 'בּוּ',                      '', '', ''],
    ['12', 'בֻּ',                       '', '', ''],
    ['13', 'מְ (word-initial)',          '', '', ''],
    ['14', 'מֲ',                        '', '', ''],
    ['15', 'מֱ',                        '', '', ''],
]

VOWEL_ANSWERS = [
    ['1',  'בָּ',  'Qamets',         'A',       'Long'],
    ['2',  'בַּ',  'Pathach',        'A',       'Short'],
    ['3',  'בָּ',  'Qamets Hatuf',   'O',       'Short'],
    ['4',  'בֵּ',  'Tsere',          'E',       'Long'],
    ['5',  'בֶּ',  'Seghol',         'E',       'Short'],
    ['6',  'בִּ',  'Hireq',          'I',       'Short'],
    ['7',  'מִי',  'Hireq Yod',      'I',       'Long'],
    ['8',  'מֵי',  'Tsere Yod',      'E',       'Long'],
    ['9',  'בֹּ',  'Holem',          'O',       'Long'],
    ['10', 'בּוֹ', 'Holem Waw',      'O',       'Long'],
    ['11', 'בּוּ', 'Shureq',         'U',       'Long'],
    ['12', 'בֻּ',  'Qibbuts',        'U',       'Short'],
    ['13', 'מְ',   'Vocal Shewa',    'Reduced', 'Reduced'],
    ['14', 'מֲ',   'Hateph Pathach', 'A',       'Reduced'],
    ['15', 'מֱ',   'Hateph Seghol',  'E',       'Reduced'],
]


class VowelReviewPDF(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each pointed Hebrew form shown, identify: (1) Vowel Name, '
            '(2) Vowel Class (A / E / I / O / U / Reduced), (3) Quantity (Long / Short / Reduced). '
            'Items 1–3 test the critical Qamets / Pathach / Qamets Hatuf distinction.'
        )
        self.add_section_heading('Exercise — 15 items')
        self.add_generic_table(
            headers=['#', 'Form', 'Vowel Name', 'Class', 'Quantity'],
            rows=VOWEL_ROWS,
            col_ratios=[0.06, 0.26, 0.28, 0.16, 0.24],
            heb_cols=[1],
            show_answers=False,
        )
        self.add_section_heading('Answer Key')
        self.add_generic_table(
            headers=['#', 'Form', 'Vowel Name', 'Class', 'Quantity'],
            rows=VOWEL_ANSWERS,
            col_ratios=[0.06, 0.26, 0.28, 0.16, 0.24],
            heb_cols=[1],
            show_answers=True,
            answer_rows=VOWEL_ANSWERS,
        )


# ---------------------------------------------------------------------------
# Exercise 3 — Syllabification Review (15 words)
# ---------------------------------------------------------------------------

SYLL_ROWS = [
    ['1',  'בַּיִת', '', '', '', ''],
    ['2',  'מַיִם',  '', '', '', ''],
    ['3',  'שֶׁמֶשׁ','', '', '', ''],
    ['4',  'אָדָם',  '', '', '', ''],
    ['5',  'אֱמֶת',  '', '', '', ''],
    ['6',  'נֶפֶשׁ', '', '', '', ''],
    ['7',  'מָוֶת',  '', '', '', ''],
    ['8',  'חֶרֶב',  '', '', '', ''],
    ['9',  'אָמַר',  '', '', '', ''],
    ['10', 'בֹּקֶר', '', '', '', ''],
    ['11', 'עֶרֶב',  '', '', '', ''],
    ['12', 'פְּנֵי',  '', '', '', ''],
    ['13', 'מָקוֹם', '', '', '', ''],
    ['14', 'בְּרָכָה','','', '', ''],
    ['15', 'יְהוּדָה','','', '', ''],
]

SYLL_ANSWERS = [
    ['1',  'בַּיִת', 'בַּ-יִת',   'O-C',   'יִת*',   '—'],
    ['2',  'מַיִם',  'מַ-יִם',    'O-C',   'יִם*',   '—'],
    ['3',  'שֶׁמֶשׁ', 'שֶׁ-מֶשׁ', 'O-C',   'מֶשׁ*',  '—'],
    ['4',  'אָדָם',  'אָ-דָם',    'O-C',   'דָם*',   '—'],
    ['5',  'אֱמֶת',  'אֱ-מֶת',    'O-C',   'מֶת*',   '—'],
    ['6',  'נֶפֶשׁ', 'נֶ-פֶשׁ',   'O-C',   'פֶשׁ*',  '—'],
    ['7',  'מָוֶת',  'מָ-וֶת',    'O-C',   'וֶת*',   '—'],
    ['8',  'חֶרֶב',  'חֶ-רֶב',    'O-C',   'רֶב*',   '—'],
    ['9',  'אָמַר',  'אָ-מַר',    'O-C',   'מַר*',   '—'],
    ['10', 'בֹּקֶר', 'בֹּ-קֶר',   'O-C',   'קֶר*',   '—'],
    ['11', 'עֶרֶב',  'עֶ-רֶב',    'O-C',   'רֶב*',   '—'],
    ['12', 'פְּנֵי',  'פְּ-נֵי',   'O-O',   'נֵי*',   '—'],
    ['13', 'מָקוֹם', 'מָ-קוֹם',   'O-C',   'קוֹם*',  '—'],
    ['14', 'בְּרָכָה','בְּ-רָ-כָה','O-O-O', 'כָה*',   '—'],
    ['15', 'יְהוּדָה','יְ-הוּ-דָה','O-O-O', 'דָה*',   '—'],
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
