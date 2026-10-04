#!/usr/bin/env python3
"""Generate fillable PDFs for Session 136 review exercises.

Output paths:
  data/courses/bbh/bbh-2024.1/session-136/exercises/<name>/<name>.pdf

Usage:
    python scripts/build_session136_review_pdfs.py
"""

from __future__ import annotations

import os
import sys
from typing import List, Tuple, Type

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO, 'src'))

from bible_grammar.exercise_pdf import ExercisePDF  # noqa: E402

_SESSION_DIR = os.path.join(
    _REPO, 'data', 'courses', 'bbh', 'bbh-2024.1', 'session-136', 'exercises'
)

# ---------------------------------------------------------------------------
# Exercise 1 — Stem Identification Drill (25 items)
# ---------------------------------------------------------------------------

STEM_ID_ROWS = [
    ['1',  'יִשְׁמֹר',   '', '', '', ''],
    ['2',  'קִדֵּשׁ',    '', '', '', ''],
    ['3',  'הִקְדִּישׁ', '', '', '', ''],
    ['4',  'נִשְׁמַר',   '', '', '', ''],
    ['5',  'הִתְפַּלֵּל', '', '', '', ''],
    ['6',  'קֻדַּשׁ',    '', '', '', ''],
    ['7',  'יִכָּתֵב',   '', '', '', ''],
    ['8',  'כָּתַב',     '', '', '', ''],
    ['9',  'יְדַבֵּר',   '', '', '', ''],
    ['10', 'הֻשְׁלַךְ',  '', '', '', ''],
    ['11', 'מְדַבֵּר',   '', '', '', ''],
    ['12', 'יַגְדִּיל',  '', '', '', ''],
    ['13', 'שֹׁמֵר',     '', '', '', ''],
    ['14', 'נִכְתָּב',   '', '', '', ''],
    ['15', 'יִתְפַּלֵּל', '', '', '', ''],
    ['16', 'יְדֻבַּר',   '', '', '', ''],
    ['17', 'הִגְדִּיל',  '', '', '', ''],
    ['18', 'מַגְדִּיל',  '', '', '', ''],
    ['19', 'וַיִּכְתֹּב', '', '', '', ''],
    ['20', 'מִתְפַּלֵּל', '', '', '', ''],
    ['21', 'יֻשְׁלַךְ',  '', '', '', ''],
    ['22', 'נִקְדַּשׁ',  '', '', '', ''],
    ['23', 'מְדֻבָּר',   '', '', '', ''],
    ['24', 'מֻשְׁלָךְ',  '', '', '', ''],
    ['25', 'כָּתְבָה',   '', '', '', ''],
]

STEM_ID_ANSWERS = [
    ['1',  'יִשְׁמֹר',   'Qal',      'Imperfect', '3ms', 'שׁמר'],
    ['2',  'קִדֵּשׁ',    'Piel',     'Perfect',   '3ms', 'קדשׁ'],
    ['3',  'הִקְדִּישׁ', 'Hiphil',   'Perfect',   '3ms', 'קדשׁ'],
    ['4',  'נִשְׁמַר',   'Niphal',   'Perfect',   '3ms', 'שׁמר'],
    ['5',  'הִתְפַּלֵּל', 'Hithpael', 'Perfect',   '3ms', 'פלל'],
    ['6',  'קֻדַּשׁ',    'Pual',     'Perfect',   '3ms', 'קדשׁ'],
    ['7',  'יִכָּתֵב',   'Niphal',   'Imperfect', '3ms', 'כתב'],
    ['8',  'כָּתַב',     'Qal',      'Perfect',   '3ms', 'כתב'],
    ['9',  'יְדַבֵּר',   'Piel',     'Imperfect', '3ms', 'דבר'],
    ['10', 'הֻשְׁלַךְ',  'Hophal',   'Perfect',   '3ms', 'שׁלך'],
    ['11', 'מְדַבֵּר',   'Piel',     'Participle', 'ms', 'דבר'],
    ['12', 'יַגְדִּיל',  'Hiphil',   'Imperfect', '3ms', 'גדל'],
    ['13', 'שֹׁמֵר',     'Qal',      'Participle', 'ms', 'שׁמר'],
    ['14', 'נִכְתָּב',   'Niphal',   'Participle', 'ms', 'כתב'],
    ['15', 'יִתְפַּלֵּל', 'Hithpael', 'Imperfect', '3ms', 'פלל'],
    ['16', 'יְדֻבַּר',   'Pual',     'Imperfect', '3ms', 'דבר'],
    ['17', 'הִגְדִּיל',  'Hiphil',   'Perfect',   '3ms', 'גדל'],
    ['18', 'מַגְדִּיל',  'Hiphil',   'Participle', 'ms', 'גדל'],
    ['19', 'וַיִּכְתֹּב', 'Qal',      'Wayyiqtol', '3ms', 'כתב'],
    ['20', 'מִתְפַּלֵּל', 'Hithpael', 'Participle', 'ms', 'פלל'],
    ['21', 'יֻשְׁלַךְ',  'Hophal',   'Imperfect', '3ms', 'שׁלך'],
    ['22', 'נִקְדַּשׁ',  'Niphal',   'Perfect',   '3ms', 'קדשׁ'],
    ['23', 'מְדֻבָּר',   'Pual',     'Participle', 'ms', 'דבר'],
    ['24', 'מֻשְׁלָךְ',  'Hophal',   'Participle', 'ms', 'שׁלך'],
    ['25', 'כָּתְבָה',   'Qal',      'Perfect',   '3fs', 'כתב'],
]


class StemIdDrillPDF(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each Hebrew form, identify the stem, conjugation, PGN, and root. '
            'Forms are drawn from all seven stems learned in BBH Ch12–35.'
        )
        self.add_section_heading('Exercise — 25 items')
        self.add_generic_table(
            headers=['#', 'Hebrew', 'Stem', 'Conj.', 'PGN', 'Root'],
            rows=STEM_ID_ROWS,
            col_ratios=[0.05, 0.18, 0.13, 0.17, 0.10, 0.37],
            heb_cols=[1],
            show_answers=False,
        )
        self.add_section_heading('Answer Key')
        self.add_generic_table(
            headers=['#', 'Hebrew', 'Stem', 'Conj.', 'PGN', 'Root'],
            rows=STEM_ID_ANSWERS,
            col_ratios=[0.05, 0.18, 0.13, 0.17, 0.10, 0.37],
            heb_cols=[1],
            show_answers=True,
            answer_rows=STEM_ID_ANSWERS,
        )


# ---------------------------------------------------------------------------
# Exercise 2 — Full Parsing: Psalm 119 and Pentateuch (25 items)
# ---------------------------------------------------------------------------

FULL_PARSING_ROWS = [
    ['1',  'Num 19:12', 'יִתְחַטָּא', '', '', '', '', ''],
    ['2',  'Gen 1:4',   'וַיַּבְדֵּל', '', '', '', '', ''],
    ['3',  'Ps 119:11', 'צָפַנְתִּי', '', '', '', '', ''],
    ['4',  'Ex 3:2',    'וַיֵּרָא',   '', '', '', '', ''],
    ['5',  'Ps 119:25', 'חַיֵּנִי',   '', '', '', '', ''],
    ['6',  'Gen 4:26',  'יֻלַּד',     '', '', '', '', ''],
    ['7',  'Deut 6:4',  'שְׁמַע',     '', '', '', '', ''],
    ['8',  'Gen 2:3',   'וַיְקַדֵּשׁ', '', '', '', '', ''],
    ['9',  'Ps 119:27', 'הֲבִינֵנִי', '', '', '', '', ''],
    ['10', 'Gen 17:5',  'יִקָּרֵא',   '', '', '', '', ''],
    ['11', 'Lev 13:58', 'וְכֻבַּס',   '', '', '', '', ''],
    ['12', 'Ex 14:13',  'הִתְיַצְּבוּ', '', '', '', '', ''],
    ['13', 'Ps 119:29', 'הָסֵר',      '', '', '', '', ''],
    ['14', 'Gen 1:1',   'בָּרָא',     '', '', '', '', ''],
    ['15', 'Gen 18:7',  'וַיְמַהֵר',  '', '', '', '', ''],
    ['16', 'Gen 3:5',   'וְנִפְקְחוּ', '', '', '', '', ''],
    ['17', 'Gen 26:11', 'יוּמָת',     '', '', '', '', ''],
    ['18', 'Gen 1:3',   'וַיֹּאמֶר',  '', '', '', '', ''],
    ['19', 'Ps 119:28', 'קַיְּמֵנִי', '', '', '', '', ''],
    ['20', 'Gen 2:24',  'וְדָבַק',    '', '', '', '', ''],
    ['21', 'Num 26:55', 'יֵחָלֵק',    '', '', '', '', ''],
    ['22', 'Gen 40:15', 'גֻּנַּבְתִּי', '', '', '', '', ''],
    ['23', 'Gen 12:1',  'לֶךְ',       '', '', '', '', ''],
    ['24', 'Ps 119:32', 'תַרְחִיב',   '', '', '', '', ''],
    ['25', 'Ps 119:3',  'הָלָכוּ',    '', '', '', '', ''],
]

FULL_PARSING_ANSWERS = [
    ['1',  'Num 19:12', 'יִתְחַטָּא', 'Hithpael', 'Imperfect',  '3ms', 'חטא', 'purify himself'],
    ['2',  'Gen 1:4',   'וַיַּבְדֵּל', 'Hiphil',   'Wayyiqtol',  '3ms', 'בדל', 'separated'],
    ['3',  'Ps 119:11', 'צָפַנְתִּי', 'Qal',      'Perfect',    '1cs', 'צפן', 'I stored up'],
    ['4',  'Ex 3:2',    'וַיֵּרָא',   'Niphal',   'Wayyiqtol',  '3ms', 'ראה', 'appeared'],
    ['5',  'Ps 119:25', 'חַיֵּנִי',   'Piel',     'Imperative', '2ms', 'חיה', 'give me life'],
    ['6',  'Gen 4:26',  'יֻלַּד',     'Hophal',   'Perfect',    '3ms', 'ילד', 'was born'],
    ['7',  'Deut 6:4',  'שְׁמַע',     'Qal',      'Imperative', '2ms', 'שׁמע', 'hear!'],
    ['8',  'Gen 2:3',   'וַיְקַדֵּשׁ', 'Piel',     'Wayyiqtol',  '3ms', 'קדשׁ', 'sanctified'],
    ['9',  'Ps 119:27', 'הֲבִינֵנִי', 'Hiphil',   'Imperative', '2ms', 'בין', 'cause me to understand'],
    ['10', 'Gen 17:5',  'יִקָּרֵא',   'Niphal',   'Imperfect',  '3ms', 'קרא', 'be called'],
    ['11', 'Lev 13:58', 'וְכֻבַּס',   'Pual',     'Perfect',    '3ms', 'כבס', 'be washed'],
    ['12', 'Ex 14:13',  'הִתְיַצְּבוּ', 'Hithpael', 'Imperative', '2mp', 'יצב', 'station yourselves!'],
    ['13', 'Ps 119:29', 'הָסֵר',      'Hiphil',   'Imperative', '2ms', 'סור', 'remove!'],
    ['14', 'Gen 1:1',   'בָּרָא',     'Qal',      'Perfect',    '3ms', 'ברא', 'created'],
    ['15', 'Gen 18:7',  'וַיְמַהֵר',  'Piel',     'Wayyiqtol',  '3ms', 'מהר', 'hurried'],
    ['16', 'Gen 3:5',   'וְנִפְקְחוּ', 'Niphal',   'Perfect',    '3cp', 'פקח', 'will be opened'],
    ['17', 'Gen 26:11', 'יוּמָת',     'Hophal',   'Imperfect',  '3ms', 'מות', 'shall be put to death'],
    ['18', 'Gen 1:3',   'וַיֹּאמֶר',  'Qal',      'Wayyiqtol',  '3ms', 'אמר', 'said'],
    ['19', 'Ps 119:28', 'קַיְּמֵנִי', 'Piel',     'Imperative', '2ms', 'קום', 'establish me!'],
    ['20', 'Gen 2:24',  'וְדָבַק',    'Qal',      'Perfect',    '3ms', 'דבק', 'clings/shall cling'],
    ['21', 'Num 26:55', 'יֵחָלֵק',    'Niphal',   'Imperfect',  '3ms', 'חלק', 'be divided'],
    ['22', 'Gen 40:15', 'גֻּנַּבְתִּי', 'Pual',     'Perfect',    '1cs', 'גנב', 'I was stolen'],
    ['23', 'Gen 12:1',  'לֶךְ',       'Qal',      'Imperative', '2ms', 'הלך', 'go!'],
    ['24', 'Ps 119:32', 'תַרְחִיב',   'Hiphil',   'Imperfect',  '2ms', 'רחב', 'you enlarge'],
    ['25', 'Ps 119:3',  'הָלָכוּ',    'Qal',      'Perfect',    '3cp', 'הלך', 'they walked'],
]


class FullParsingPDF(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each verb, identify the stem, conjugation, PGN, root, and give a translation. '
            'Verses are from Psalm 119 and the Pentateuch.'
        )
        self.add_section_heading('Exercise — 25 items')
        self.add_generic_table(
            headers=['#', 'Ref', 'Hebrew', 'Stem', 'Conj.', 'PGN', 'Root', 'Translation'],
            rows=FULL_PARSING_ROWS,
            col_ratios=[0.04, 0.10, 0.14, 0.12, 0.16, 0.10, 0.12, 0.22],
            heb_cols=[2],
            show_answers=False,
        )
        self.add_section_heading('Answer Key')
        self.add_generic_table(
            headers=['#', 'Ref', 'Hebrew', 'Stem', 'Conj.', 'PGN', 'Root', 'Translation'],
            rows=FULL_PARSING_ANSWERS,
            col_ratios=[0.04, 0.10, 0.14, 0.12, 0.16, 0.10, 0.12, 0.22],
            heb_cols=[2],
            show_answers=True,
            answer_rows=FULL_PARSING_ANSWERS,
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
        (StemIdDrillPDF,
         'Session 136 — All-Stems Identification Drill',
         'BBH 2024.1 · Review · 25 items · All Seven Stems',
         'session136-stem-id-drill'),
        (FullParsingPDF,
         'Session 136 — Full Parsing: Psalm 119 and Pentateuch',
         'BBH 2024.1 · Review · 25 items · All Seven Stems',
         'session136-full-parsing'),
    ]

    for klass, title, subtitle, name in exercises:
        path = _out(name)
        klass(title=title, subtitle=subtitle).save(path)
        print(f'  wrote {os.path.relpath(path, _REPO)}')

    print('Done.')


if __name__ == '__main__':
    main()
