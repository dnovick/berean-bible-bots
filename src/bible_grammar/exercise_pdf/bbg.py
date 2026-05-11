from typing import Optional
from ._greek import GreekExercisePDF
from ._base import _build_exercise_pdf


class BbgCh3AlphabetDrillPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each Greek letter form shown, write: (a) the letter name and '
            '(b) its sound/pronunciation. '
            'Item 19 tests the final sigma form (ς). '
            'Part B tests uppercase recognition.'
        )
        hdrs = ['#', 'Form', 'Name', 'Sound / Pronunciation']
        cr = [0.06, 0.10, 0.22, 0.62]
        gk = [1]

        rows_a = [
            ['1',  'α', '', ''], ['2',  'β', '', ''], ['3',  'γ', '', ''],
            ['4',  'δ', '', ''], ['5',  'ε', '', ''], ['6',  'ζ', '', ''],
            ['7',  'η', '', ''], ['8',  'θ', '', ''], ['9',  'ι', '', ''],
            ['10', 'κ', '', ''], ['11', 'λ', '', ''], ['12', 'μ', '', ''],
            ['13', 'ν', '', ''], ['14', 'ξ', '', ''], ['15', 'ο', '', ''],
            ['16', 'π', '', ''], ['17', 'ρ', '', ''], ['18', 'σ', '', ''],
            ['19', 'ς', '', ''], ['20', 'τ', '', ''], ['21', 'υ', '', ''],
            ['22', 'φ', '', ''], ['23', 'χ', '', ''], ['24', 'ψ', '', ''],
            ['25', 'ω', '', ''],
        ]
        ans_a = [
            ['1',  'α', 'Alpha',   '"father" (long) / "along" (short)'],
            ['2',  'β', 'Beta',    '"b" as in "Bible"'],
            ['3',  'γ', 'Gamma',   '"g" as in "gone"; "ng" before γ κ χ ξ'],
            ['4',  'δ', 'Delta',   '"d" as in "dog"'],
            ['5',  'ε', 'Epsilon', 'short "e" as in "met" — always short'],
            ['6',  'ζ', 'Zeta',    '"z" as in "daze"'],
            ['7',  'η', 'Eta',     'long "e" as in "they" — always long'],
            ['8',  'θ', 'Theta',   '"th" as in "thin"'],
            ['9',  'ι', 'Iota',    '"ee" (long) / short "i" as in "in"'],
            ['10', 'κ', 'Kappa',   '"k" as in "kitchen"'],
            ['11', 'λ', 'Lambda',  '"l" as in "law"'],
            ['12', 'μ', 'Mu',      '"m" as in "mother"'],
            ['13', 'ν', 'Nu',      '"n" as in "new"'],
            ['14', 'ξ', 'Xi',      '"ks" as in "axiom" (double consonant)'],
            ['15', 'ο', 'Omicron', 'short "o" as in "off" — always short'],
            ['16', 'π', 'Pi',      '"p" as in "peach"'],
            ['17', 'ρ', 'Rho',     '"r" as in "rod"; initial rho = rough breathing'],
            ['18', 'σ', 'Sigma',   '"s" — medial form (beginning/middle of word)'],
            ['19', 'ς', 'Sigma',   '"s" — final form (end of word only)'],
            ['20', 'τ', 'Tau',     '"t" as in "talk"'],
            ['21', 'υ', 'Upsilon', 'French "tu" or German "uber"'],
            ['22', 'φ', 'Phi',     '"ph" as in "phone"'],
            ['23', 'χ', 'Chi',     'breathy "ch" as in German "Bach"'],
            ['24', 'ψ', 'Psi',     '"ps" as in "lips" (double consonant)'],
            ['25', 'ω', 'Omega',   'long "o" as in "tone" — always long'],
        ]

        self.add_section_heading('Part A — The 24 Letters (+ Final Sigma)')
        self.add_greek_table(hdrs, rows_a, cr, greek_cols=gk,
                             show_answers=False)

        self.add_section_heading('Answer Key')
        self.add_greek_table(hdrs, rows_a, cr, greek_cols=gk,
                             show_answers=True, answer_rows=ans_a)

        # Part B — Uppercase
        hdrs_b = ['#', 'Uppercase', 'Lowercase', 'Name']
        cr_b = [0.06, 0.12, 0.12, 0.70]
        rows_b = [
            ['B1', 'Α', '', ''], ['B2', 'Γ', '', ''], ['B3', 'Δ', '', ''],
            ['B4', 'Λ', '', ''], ['B5', 'Ξ', '', ''], ['B6', 'Π', '', ''],
            ['B7', 'Σ', '', ''], ['B8', 'Φ', '', ''], ['B9', 'Χ', '', ''],
            ['B10', 'Ψ', '', ''], ['B11', 'Ω', '', ''],
        ]
        ans_b = [
            ['B1', 'Α', 'α', 'Alpha'], ['B2', 'Γ', 'γ', 'Gamma'],
            ['B3', 'Δ', 'δ', 'Delta'], ['B4', 'Λ', 'λ', 'Lambda'],
            ['B5', 'Ξ', 'ξ', 'Xi'], ['B6', 'Π', 'π', 'Pi'],
            ['B7', 'Σ', 'σ/ς', 'Sigma'], ['B8', 'Φ', 'φ', 'Phi'],
            ['B9', 'Χ', 'χ', 'Chi'], ['B10', 'Ψ', 'ψ', 'Psi'],
            ['B11', 'Ω', 'ω', 'Omega'],
        ]
        self.add_section_heading('Part B — Uppercase Recognition')
        self.add_greek_table(hdrs_b, rows_b, cr_b, greek_cols=[1],
                             show_answers=False)
        self.add_section_heading('Answer Key — Part B')
        self.add_greek_table(hdrs_b, rows_b, cr_b, greek_cols=[1],
                             show_answers=True, answer_rows=ans_b)


def build_bbg_ch3_alphabet_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh3AlphabetDrillPDF,
        'BBG Chapter 3 — Greek Alphabet Drill',
        'Letter Identification: Name and Sound',
        ['greek', 'bbg', 'ch3', 'exercises', 'ch3-alphabet-drill'],
        'ch3-alphabet-drill.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch4 — Syllabification Drill PDF
# ---------------------------------------------------------------------------

class BbgCh4SyllableDrillPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each Greek word: (a) divide into syllables using hyphens, '
            '(b) name the accented syllable position (ultima / penult / antepenult), '
            '(c) name the accent type (acute / grave / circumflex).'
        )
        hdrs = ['#', 'Word', 'Syllable Division', 'Accent Position', 'Accent Type']
        cr = [0.05, 0.18, 0.28, 0.27, 0.22]
        gk = [1]

        rows_a = [
            ['1',  'θεός',      '', '', ''], ['2',  'λόγος',    '', '', ''],
            ['3',  'κύριος',    '', '', ''], ['4',  'πνεῦμα',   '', '', ''],
            ['5',  'σάρξ',      '', '', ''], ['6',  'νόμος',    '', '', ''],
            ['7',  'ἀγάπη',     '', '', ''], ['8',  'ζωή',      '', '', ''],
            ['9',  'πίστις',    '', '', ''], ['10', 'εἰρήνη',   '', '', ''],
        ]
        ans_a = [
            ['1',  'θεός',    'θε-ός',          'Ultima',      'Acute'],
            ['2',  'λόγος',   'λό-γος',         'Penult',      'Acute'],
            ['3',  'κύριος',  'κύ-ρι-ος',       'Antepenult',  'Acute'],
            ['4',  'πνεῦμα',  'πνεῦ-μα',        'Penult',      'Circumflex'],
            ['5',  'σάρξ',    'σάρξ (1 syl.)',   'Ultima',      'Acute'],
            ['6',  'νόμος',   'νό-μος',         'Penult',      'Acute'],
            ['7',  'ἀγάπη',   'ἀ-γά-πη',        'Penult',      'Acute'],
            ['8',  'ζωή',     'ζω-ή',           'Ultima',      'Acute'],
            ['9',  'πίστις',  'πίσ-τις',        'Penult',      'Acute'],
            ['10', 'εἰρήνη',  'εἰ-ρή-νη',       'Penult',      'Circumflex'],
        ]

        rows_b = [
            ['11', 'ἄνθρωπος',    '', '', ''], ['12', 'ἀπόστολος',  '', '', ''],
            ['13', 'εὐαγγέλιον',  '', '', ''], ['14', 'βασιλεία',   '', '', ''],
            ['15', 'ἁμαρτία',     '', '', ''], ['16', 'ἐκκλησία',   '', '', ''],
            ['17', 'ἀδελφός',     '', '', ''], ['18', 'προφήτης',   '', '', ''],
            ['19', 'παραβολή',    '', '', ''], ['20', 'ἀποκάλυψις', '', '', ''],
        ]
        ans_b = [
            ['11', 'ἄνθρωπος',   'ἄν-θρω-πος',      'Antepenult', 'Acute'],
            ['12', 'ἀπόστολος',  'ἀ-πόσ-το-λος',    'Penult',     'Acute'],
            ['13', 'εὐαγγέλιον', 'εὐ-αγ-γέ-λι-ον',  'Antepenult', 'Acute'],
            ['14', 'βασιλεία',   'βα-σι-λεί-α',      'Penult',     'Circumflex'],
            ['15', 'ἁμαρτία',    'ἁ-μαρ-τί-α',       'Penult',     'Acute'],
            ['16', 'ἐκκλησία',   'ἐκ-κλη-σί-α',      'Penult',     'Acute'],
            ['17', 'ἀδελφός',    'ἀ-δελ-φός',        'Ultima',     'Acute'],
            ['18', 'προφήτης',   'προ-φή-της',       'Penult',     'Circumflex'],
            ['19', 'παραβολή',   'πα-ρα-βο-λή',      'Ultima',     'Acute'],
            ['20', 'ἀποκάλυψις', 'ἀ-πο-κά-λυ-ψις',  'Antepenult', 'Acute'],
        ]

        self.add_section_heading('Part A — Two and Three Syllable Words')
        self.add_greek_table(hdrs, rows_a, cr, greek_cols=gk, show_answers=False)
        self.add_section_heading('Part B — Three to Five Syllable Words')
        self.add_greek_table(hdrs, rows_b, cr, greek_cols=gk, show_answers=False)

        self.add_section_heading('Answer Key — Part A')
        self.add_greek_table(hdrs, rows_a, cr, greek_cols=gk,
                             show_answers=True, answer_rows=ans_a)
        self.add_section_heading('Answer Key — Part B')
        self.add_greek_table(hdrs, rows_b, cr, greek_cols=gk,
                             show_answers=True, answer_rows=ans_b)


def build_bbg_ch4_syllable_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh4SyllableDrillPDF,
        'BBG Chapter 4 — Syllabification Drill',
        'Syllable Division, Accent Position, and Accent Type',
        ['greek', 'bbg', 'ch4', 'exercises', 'ch4-syllable-drill'],
        'ch4-syllable-drill.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch6 — Nominative/Accusative Parsing Drill PDF
# ---------------------------------------------------------------------------

class BbgCh6NomAccParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each form, give: (a) Case, (b) Number, (c) Gender, '
            '(d) Lexical form (nom. sg.), (e) Function in a sentence '
            '(subject / direct object / predicate nominative / article). '
            'All forms are 2nd-declension nominative or accusative.'
        )
        hdrs = ['#', 'Form', 'Case', 'Number', 'Gender', 'Lexical Form', 'Function']
        cr = [0.04, 0.14, 0.12, 0.10, 0.10, 0.14, 0.36]
        gk = [1]

        rows_a = [
            ['1',  'λόγος',       '', '', '', '', ''],
            ['2',  'λόγον',       '', '', '', '', ''],
            ['3',  'λόγοι',       '', '', '', '', ''],
            ['4',  'λόγους',      '', '', '', '', ''],
            ['5',  'ὁ',           '', '', '', '', ''],
            ['6',  'τόν',         '', '', '', '', ''],
            ['7',  'οἱ',          '', '', '', '', ''],
            ['8',  'τούς',        '', '', '', '', ''],
            ['9',  'κύριον',      '', '', '', '', ''],
            ['10', 'κύριοι',      '', '', '', '', ''],
        ]
        ans_a = [
            ['1',  'λόγος',  'Nom.',  'Sg.', 'Masc.', 'λόγος', 'Subject / pred. nom.'],
            ['2',  'λόγον',  'Acc.',  'Sg.', 'Masc.', 'λόγος', 'Direct object'],
            ['3',  'λόγοι',  'Nom.',  'Pl.', 'Masc.', 'λόγος', 'Subject'],
            ['4',  'λόγους', 'Acc.',  'Pl.', 'Masc.', 'λόγος', 'Direct object'],
            ['5',  'ὁ',      'Nom.',  'Sg.', 'Masc.', 'ὁ (art.)', 'Article — masc. sg. nom.'],
            ['6',  'τόν',    'Acc.',  'Sg.', 'Masc.', 'ὁ (art.)', 'Article — masc. sg. acc.'],
            ['7',  'οἱ',     'Nom.',  'Pl.', 'Masc.', 'ὁ (art.)', 'Article — masc. pl. nom.'],
            ['8',  'τούς',   'Acc.',  'Pl.', 'Masc.', 'ὁ (art.)', 'Article — masc. pl. acc.'],
            ['9',  'κύριον', 'Acc.',  'Sg.', 'Masc.', 'κύριος', 'Direct object'],
            ['10', 'κύριοι', 'Nom.',  'Pl.', 'Masc.', 'κύριος', 'Subject'],
        ]

        rows_b = [
            ['11', 'ἔργον',        '', '', '', '', ''],
            ['12', 'ἔργα',         '', '', '', '', ''],
            ['13', 'τό',           '', '', '', '', ''],
            ['14', 'τά',           '', '', '', '', ''],
            ['15', 'εὐαγγέλιον',   '', '', '', '', ''],
            ['16', 'εὐαγγέλια',    '', '', '', '', ''],
            ['17', 'θεός',         '', '', '', '', ''],
            ['18', 'θεόν',         '', '', '', '', ''],
            ['19', 'κόσμοι',       '', '', '', '', ''],
            ['20', 'ἔργα',         '', '', '', '', ''],
        ]
        ans_b = [
            ['11', 'ἔργον',       'Nom./Acc.', 'Sg.', 'Neut.', 'ἔργον',       'Subj. or dir. obj. (neuter rule)'],
            ['12', 'ἔργα',        'Nom./Acc.', 'Pl.', 'Neut.', 'ἔργον',       'Subj. or dir. obj.'],
            ['13', 'τό',          'Nom./Acc.', 'Sg.', 'Neut.', 'ὁ (art.)',    'Article — neut. sg.'],
            ['14', 'τά',          'Nom./Acc.', 'Pl.', 'Neut.', 'ὁ (art.)',    'Article — neut. pl.'],
            ['15', 'εὐαγγέλιον',  'Nom./Acc.', 'Sg.', 'Neut.', 'εὐαγγέλιον', 'Subj. or dir. obj.'],
            ['16', 'εὐαγγέλια',   'Nom./Acc.', 'Pl.', 'Neut.', 'εὐαγγέλιον', 'Subj. or dir. obj.'],
            ['17', 'θεός',        'Nom.',      'Sg.', 'Masc.', 'θεός',        'Subject / pred. nom.'],
            ['18', 'θεόν',        'Acc.',      'Sg.', 'Masc.', 'θεός',        'Direct object'],
            ['19', 'κόσμοι',      'Nom.',      'Pl.', 'Masc.', 'κόσμος',      'Subject'],
            ['20', 'ἔργα',        'Nom./Acc.', 'Pl.', 'Neut.', 'ἔργον',       'Subj. or dir. obj.'],
        ]

        self.add_section_heading('Part A — Masculine Nouns and Article')
        self.add_greek_table(hdrs, rows_a, cr, greek_cols=gk, show_answers=False)
        self.add_section_heading('Part B — Neuter Nouns, Article, and Mixed')
        self.add_greek_table(hdrs, rows_b, cr, greek_cols=gk, show_answers=False)

        self.add_section_heading('Answer Key — Part A')
        self.add_greek_table(hdrs, rows_a, cr, greek_cols=gk,
                             show_answers=True, answer_rows=ans_a)
        self.add_section_heading('Answer Key — Part B')
        self.add_greek_table(hdrs, rows_b, cr, greek_cols=gk,
                             show_answers=True, answer_rows=ans_b)


def build_bbg_ch6_nom_acc_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh6NomAccParsingPDF,
        'BBG Chapter 6 — Nominative and Accusative Parsing Drill',
        '2nd Declension Nouns and Definite Article',
        ['greek', 'bbg', 'ch6', 'exercises', 'ch6-nom-acc-parsing'],
        'ch6-nom-acc-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch7 — Genitive and Dative Parsing Drill
# ---------------------------------------------------------------------------

class BbgCh7GenDatParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each form, give: Case (G/D), Number (S/P), Gender (M/N), '
            'Lexical Form (nom. sg.), and a Translation Note. '
            'All forms are 2nd-declension genitive or dative.'
        )
        hdrs = ['#', 'Greek Form', 'Case', 'Number', 'Gender', 'Lexical Form', 'Translation Note']
        cr = [0.04, 0.18, 0.07, 0.08, 0.08, 0.14, 0.41]
        gk = [1]
        rows = [
            ['1',  'τοῦ θεοῦ',       '', '', '', '', ''],
            ['2',  'τῷ κυρίῳ',        '', '', '', '', ''],
            ['3',  'λόγων',           '', '', '', '', ''],
            ['4',  'τοῖς δούλοις',    '', '', '', '', ''],
            ['5',  'τοῦ ἔργου',       '', '', '', '', ''],
            ['6',  'τῷ νόμῳ',         '', '', '', '', ''],
            ['7',  'ἀδελφῶν',         '', '', '', '', ''],
            ['8',  'τοῖς ἔργοις',     '', '', '', '', ''],
            ['9',  'τοῦ υἱοῦ',        '', '', '', '', ''],
            ['10', 'τῷ οἴκῳ',         '', '', '', '', ''],
            ['11', 'εὐαγγελίων',      '', '', '', '', ''],
            ['12', 'τοῖς λόγοις',     '', '', '', '', ''],
            ['13', 'τοῦ ἀνθρώπου',    '', '', '', '', ''],
            ['14', 'τῷ ἀποστόλῳ',     '', '', '', '', ''],
            ['15', 'δούλου',          '', '', '', '', ''],
            ['16', 'τῶν τέκνων',      '', '', '', '', ''],
            ['17', 'τῷ εὐαγγελίῳ',   '', '', '', '', ''],
            ['18', 'κυρίων',          '', '', '', '', ''],
            ['19', 'τοῦ ἱεροῦ',       '', '', '', '', ''],
            ['20', 'τοῖς ἀδελφοῖς',   '', '', '', '', ''],
        ]
        ans = [
            ['1',  'τοῦ θεοῦ',      'G', 'S', 'M', 'θεός',         '"of God" / "God\'s"'],
            ['2',  'τῷ κυρίῳ',       'D', 'S', 'M', 'κύριος',       '"to/for the Lord"'],
            ['3',  'λόγων',          'G', 'P', 'M', 'λόγος',        '"of words"'],
            ['4',  'τοῖς δούλοις',   'D', 'P', 'M', 'δοῦλος',       '"to/for the slaves"'],
            ['5',  'τοῦ ἔργου',      'G', 'S', 'N', 'ἔργον',        '"of the work"'],
            ['6',  'τῷ νόμῳ',        'D', 'S', 'M', 'νόμος',        '"in/by the law"'],
            ['7',  'ἀδελφῶν',        'G', 'P', 'M', 'ἀδελφός',      '"of brothers"'],
            ['8',  'τοῖς ἔργοις',    'D', 'P', 'N', 'ἔργον',        '"by/with the works"'],
            ['9',  'τοῦ υἱοῦ',       'G', 'S', 'M', 'υἱός',         '"of the Son"'],
            ['10', 'τῷ οἴκῳ',        'D', 'S', 'M', 'οἶκος',        '"in/to the house"'],
            ['11', 'εὐαγγελίων',     'G', 'P', 'N', 'εὐαγγέλιον',   '"of gospels"'],
            ['12', 'τοῖς λόγοις',    'D', 'P', 'M', 'λόγος',        '"in/with the words"'],
            ['13', 'τοῦ ἀνθρώπου',   'G', 'S', 'M', 'ἄνθρωπος',     '"of the man"'],
            ['14', 'τῷ ἀποστόλῳ',    'D', 'S', 'M', 'ἀπόστολος',    '"to/for the apostle"'],
            ['15', 'δούλου',         'G', 'S', 'M', 'δοῦλος',       '"of a slave"'],
            ['16', 'τῶν τέκνων',     'G', 'P', 'N', 'τέκνον',       '"of the children"'],
            ['17', 'τῷ εὐαγγελίῳ',  'D', 'S', 'N', 'εὐαγγέλιον',   '"in/by the gospel"'],
            ['18', 'κυρίων',         'G', 'P', 'M', 'κύριος',       '"of lords"'],
            ['19', 'τοῦ ἱεροῦ',      'G', 'S', 'N', 'ἱερόν',        '"of the temple"'],
            ['20', 'τοῖς ἀδελφοῖς',  'D', 'P', 'M', 'ἀδελφός',      '"to/for the brothers"'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Parsing Table', use_greek=True)


def build_bbg_ch7_gen_dat_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh7GenDatParsingPDF,
        'BBG Chapter 7 — Genitive and Dative Parsing Drill',
        '2nd Declension Genitive and Dative Forms',
        ['greek', 'bbg', 'ch7', 'exercises', 'ch7-gen-dat-parsing'],
        'ch7-gen-dat-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch8 — Preposition Parsing Drill
# ---------------------------------------------------------------------------

class BbgCh8PrepositionParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each prepositional phrase: (1) name the preposition, '
            '(2) identify the case it governs (Gen / Dat / Acc), '
            '(3) give a contextual English translation.'
        )
        hdrs = ['#', 'Greek Phrase', 'Preposition', 'Case', 'Translation']
        cr = [0.04, 0.22, 0.12, 0.09, 0.53]
        gk = [1]
        rows = [
            ['1',  'ἐν τῷ κόσμῳ',          '', '', ''],
            ['2',  'εἰς τὴν βασιλείαν',     '', '', ''],
            ['3',  'ἐκ τοῦ οὐρανοῦ',        '', '', ''],
            ['4',  'ἀπὸ θεοῦ',              '', '', ''],
            ['5',  'πρὸς τὸν πατέρα',       '', '', ''],
            ['6',  'διὰ τοῦ νόμου',         '', '', ''],
            ['7',  'διὰ τοῦτο',             '', '', ''],
            ['8',  'κατὰ σάρκα',            '', '', ''],
            ['9',  'κατὰ τῶν ἐχθρῶν',      '', '', ''],
            ['10', 'μετὰ τῶν μαθητῶν',     '', '', ''],
            ['11', 'μετὰ ταῦτα',            '', '', ''],
            ['12', 'ἐπὶ τῆς γῆς',          '', '', ''],
            ['13', 'ἐπὶ τὴν θάλασσαν',     '', '', ''],
            ['14', 'παρὰ τοῦ πατρός',       '', '', ''],
            ['15', 'παρὰ τῷ κυρίῳ',        '', '', ''],
            ['16', 'περὶ τῆς ἁμαρτίας',    '', '', ''],
            ['17', 'ὑπὸ τοῦ θεοῦ',         '', '', ''],
            ['18', 'σὺν αὐτῷ',             '', '', ''],
            ['19', 'ἀντὶ πολλῶν',          '', '', ''],
            ['20', 'ἐν ἀρχῇ',              '', '', ''],
        ]
        ans = [
            ['1',  'ἐν τῷ κόσμῳ',         'ἐν',   'Dat', '"in the world"'],
            ['2',  'εἰς τὴν βασιλείαν',    'εἰς',  'Acc', '"into the kingdom"'],
            ['3',  'ἐκ τοῦ οὐρανοῦ',       'ἐκ',   'Gen', '"out of heaven"'],
            ['4',  'ἀπὸ θεοῦ',             'ἀπό',  'Gen', '"from God"'],
            ['5',  'πρὸς τὸν πατέρα',      'πρός', 'Acc', '"toward/to the Father"'],
            ['6',  'διὰ τοῦ νόμου',        'διά',  'Gen', '"through the law"'],
            ['7',  'διὰ τοῦτο',            'διά',  'Acc', '"because of this / therefore"'],
            ['8',  'κατὰ σάρκα',           'κατά', 'Acc', '"according to the flesh"'],
            ['9',  'κατὰ τῶν ἐχθρῶν',     'κατά', 'Gen', '"against the enemies"'],
            ['10', 'μετὰ τῶν μαθητῶν',    'μετά', 'Gen', '"with the disciples"'],
            ['11', 'μετὰ ταῦτα',           'μετά', 'Acc', '"after these things"'],
            ['12', 'ἐπὶ τῆς γῆς',         'ἐπί',  'Gen', '"on the earth"'],
            ['13', 'ἐπὶ τὴν θάλασσαν',    'ἐπί',  'Acc', '"onto/toward the sea"'],
            ['14', 'παρὰ τοῦ πατρός',      'παρά', 'Gen', '"from the Father"'],
            ['15', 'παρὰ τῷ κυρίῳ',       'παρά', 'Dat', '"beside/with the Lord"'],
            ['16', 'περὶ τῆς ἁμαρτίας',   'περί', 'Gen', '"concerning sin"'],
            ['17', 'ὑπὸ τοῦ θεοῦ',        'ὑπό',  'Gen', '"by God" (agent of passive)'],
            ['18', 'σὺν αὐτῷ',            'σύν',  'Dat', '"together with him"'],
            ['19', 'ἀντὶ πολλῶν',         'ἀντί', 'Gen', '"in place of / for many"'],
            ['20', 'ἐν ἀρχῇ',             'ἐν',   'Dat', '"in [the] beginning"'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Drill Table', use_greek=True)


def build_bbg_ch8_preposition_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh8PrepositionParsingPDF,
        'BBG Chapter 8 — Preposition Parsing Drill',
        'Prepositions and εἰμί',
        ['greek', 'bbg', 'ch8', 'exercises', 'ch8-preposition-parsing'],
        'ch8-preposition-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch9 — Adjective Parsing Drill
# ---------------------------------------------------------------------------

class BbgCh9AdjectiveParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each phrase, parse the adjective: Case (N/G/D/A), Number (S/P), '
            'Gender (M/F/N), and Position (Attributive / Predicate / Substantival).'
        )
        hdrs = ['#', 'Greek Phrase', 'Case', 'Number', 'Gender', 'Position']
        cr = [0.04, 0.28, 0.10, 0.10, 0.10, 0.38]
        gk = [1]
        rows = [
            ['1',  'ὁ ἀγαθὸς δοῦλος',       '', '', '', ''],
            ['2',  'ὁ δοῦλος ἀγαθός',        '', '', '', ''],
            ['3',  'οἱ ἀγαθοί',              '', '', '', ''],
            ['4',  'τὸν πιστὸν λόγον',       '', '', '', ''],
            ['5',  'ὁ λόγος πιστός',         '', '', '', ''],
            ['6',  'τῆς καλῆς ὁδοῦ',         '', '', '', ''],
            ['7',  'ἡ ὁδὸς καλή',            '', '', '', ''],
            ['8',  'τὰ ἀγαθά',               '', '', '', ''],
            ['9',  'τοῖς πιστοῖς δούλοις',   '', '', '', ''],
            ['10', 'ἡ πιστή',                '', '', '', ''],
            ['11', 'τοῦ ἀγαθοῦ ἔργου',       '', '', '', ''],
            ['12', 'τὸ ἔργον ἀγαθόν',        '', '', '', ''],
            ['13', 'ὁ πονηρὸς ἄνθρωπος',     '', '', '', ''],
            ['14', 'οἱ πιστοὶ ἀπόστολοι',    '', '', '', ''],
            ['15', 'τοὺς δικαίους',          '', '', '', ''],
            ['16', 'ἀγαθὴ ἡ ὁδός',           '', '', '', ''],
            ['17', 'τῷ ἀγαθῷ νόμῳ',          '', '', '', ''],
            ['18', 'τὸ πονηρόν',             '', '', '', ''],
            ['19', 'τῶν πιστῶν ἔργων',       '', '', '', ''],
            ['20', 'ὁ νόμος ἅγιος',          '', '', '', ''],
        ]
        ans = [
            ['1',  'ὁ ἀγαθὸς δοῦλος',      'N', 'S', 'M', 'Attributive (art-adj-noun)'],
            ['2',  'ὁ δοῦλος ἀγαθός',       'N', 'S', 'M', 'Predicate (adj no article)'],
            ['3',  'οἱ ἀγαθοί',             'N', 'P', 'M', 'Substantival ("the good people")'],
            ['4',  'τὸν πιστὸν λόγον',      'A', 'S', 'M', 'Attributive'],
            ['5',  'ὁ λόγος πιστός',        'N', 'S', 'M', 'Predicate'],
            ['6',  'τῆς καλῆς ὁδοῦ',        'G', 'S', 'F', 'Attributive'],
            ['7',  'ἡ ὁδὸς καλή',           'N', 'S', 'F', 'Predicate'],
            ['8',  'τὰ ἀγαθά',              'N', 'P', 'N', 'Substantival ("the good things")'],
            ['9',  'τοῖς πιστοῖς δούλοις',  'D', 'P', 'M', 'Attributive'],
            ['10', 'ἡ πιστή',               'N', 'S', 'F', 'Substantival ("the faithful woman")'],
            ['11', 'τοῦ ἀγαθοῦ ἔργου',      'G', 'S', 'N', 'Attributive'],
            ['12', 'τὸ ἔργον ἀγαθόν',       'N', 'S', 'N', 'Predicate'],
            ['13', 'ὁ πονηρὸς ἄνθρωπος',    'N', 'S', 'M', 'Attributive ("the evil man")'],
            ['14', 'οἱ πιστοὶ ἀπόστολοι',   'N', 'P', 'M', 'Attributive'],
            ['15', 'τοὺς δικαίους',         'A', 'P', 'M', 'Substantival ("the righteous ones")'],
            ['16', 'ἀγαθὴ ἡ ὁδός',          'N', 'S', 'F', 'Predicate (adj before art-noun)'],
            ['17', 'τῷ ἀγαθῷ νόμῳ',         'D', 'S', 'M', 'Attributive'],
            ['18', 'τὸ πονηρόν',            'N', 'S', 'N', 'Substantival ("the evil thing")'],
            ['19', 'τῶν πιστῶν ἔργων',      'G', 'P', 'N', 'Attributive'],
            ['20', 'ὁ νόμος ἅγιος',         'N', 'S', 'M', 'Predicate ("the law is holy")'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Drill Table', use_greek=True)


def build_bbg_ch9_adjective_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh9AdjectiveParsingPDF,
        'BBG Chapter 9 — Adjective Parsing Drill',
        'Attributive, Predicate, and Substantival Positions',
        ['greek', 'bbg', 'ch9', 'exercises', 'ch9-adjective-parsing'],
        'ch9-adjective-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch10 — Third Declension Parsing Drill
# ---------------------------------------------------------------------------

class BbgCh10ThirdDeclParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Parse each form: Case (N/G/D/A), Number (S/P), Gender (M/F/N), '
            'Lexical Form, and Translation.'
        )
        hdrs = ['#', 'Greek Form', 'Case', 'Number', 'Gender', 'Lexical Form', 'Translation']
        cr = [0.04, 0.18, 0.08, 0.08, 0.08, 0.14, 0.40]
        gk = [1]
        rows = [
            ['1',  'τοῦ πνεύματος',  '', '', '', '', ''],
            ['2',  'τῇ χάριτι',      '', '', '', '', ''],
            ['3',  'σώματα',         '', '', '', '', ''],
            ['4',  'τοὺς αἰῶνας',   '', '', '', '', ''],
            ['5',  'τῆς σαρκός',     '', '', '', '', ''],
            ['6',  'τῷ ὀνόματι',     '', '', '', '', ''],
            ['7',  'πνεύματα',       '', '', '', '', ''],
            ['8',  'αἰῶσιν',         '', '', '', '', ''],
            ['9',  'τὴν πόλιν',      '', '', '', '', ''],
            ['10', 'χαρίτων',        '', '', '', '', ''],
            ['11', 'τοῦ σώματος',    '', '', '', '', ''],
            ['12', 'ταῖς σαρξίν',    '', '', '', '', ''],
            ['13', 'τὰ ὀνόματα',     '', '', '', '', ''],
            ['14', 'τῆς πόλεως',     '', '', '', '', ''],
            ['15', 'χάριτα',         '', '', '', '', ''],
            ['16', 'τῶν πνευμάτων',  '', '', '', '', ''],
            ['17', 'αἰών',           '', '', '', '', ''],
            ['18', 'τοῖς σώμασιν',   '', '', '', '', ''],
            ['19', 'πόλεις',         '', '', '', '', ''],
            ['20', 'τὴν χάριτα',     '', '', '', '', ''],
        ]
        ans = [
            ['1',  'τοῦ πνεύματος', 'G',     'S', 'N', 'πνεῦμα', '"of the spirit"'],
            ['2',  'τῇ χάριτι',     'D',     'S', 'F', 'χάρις',  '"to/by grace"'],
            ['3',  'σώματα',        'N/A',   'P', 'N', 'σῶμα',   '"bodies"'],
            ['4',  'τοὺς αἰῶνας',  'A',     'P', 'M', 'αἰών',   '"the ages"'],
            ['5',  'τῆς σαρκός',    'G',     'S', 'F', 'σάρξ',   '"of the flesh"'],
            ['6',  'τῷ ὀνόματι',    'D',     'S', 'N', 'ὄνομα',  '"in/by the name"'],
            ['7',  'πνεύματα',      'N/A',   'P', 'N', 'πνεῦμα', '"spirits"'],
            ['8',  'αἰῶσιν',        'D',     'P', 'M', 'αἰών',   '"to/in the ages"'],
            ['9',  'τὴν πόλιν',     'A',     'S', 'F', 'πόλις',  '"the city"'],
            ['10', 'χαρίτων',       'G',     'P', 'F', 'χάρις',  '"of graces"'],
            ['11', 'τοῦ σώματος',   'G',     'S', 'N', 'σῶμα',   '"of the body"'],
            ['12', 'ταῖς σαρξίν',   'D',     'P', 'F', 'σάρξ',   '"in/to the flesh"'],
            ['13', 'τὰ ὀνόματα',    'N/A',   'P', 'N', 'ὄνομα',  '"the names"'],
            ['14', 'τῆς πόλεως',    'G',     'S', 'F', 'πόλις',  '"of the city"'],
            ['15', 'χάριτα',        'A',     'S', 'F', 'χάρις',  '"grace" (direct object)'],
            ['16', 'τῶν πνευμάτων', 'G',     'P', 'N', 'πνεῦμα', '"of the spirits"'],
            ['17', 'αἰών',          'N',     'S', 'M', 'αἰών',   '"age / eternity"'],
            ['18', 'τοῖς σώμασιν',  'D',     'P', 'N', 'σῶμα',   '"in/to the bodies"'],
            ['19', 'πόλεις',        'N/A',   'P', 'F', 'πόλις',  '"cities"'],
            ['20', 'τὴν χάριτα',    'A',     'S', 'F', 'χάρις',  '"grace" (direct object)'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Drill Table', use_greek=True)


def build_bbg_ch10_third_decl_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh10ThirdDeclParsingPDF,
        'BBG Chapter 10 — Third Declension Parsing Drill',
        'Consonant and Vowel Stem Nouns',
        ['greek', 'bbg', 'ch10', 'exercises', 'ch10-third-decl-parsing'],
        'ch10-third-decl-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch11 — Personal Pronoun Parsing Drill
# ---------------------------------------------------------------------------

class BbgCh11PronounParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Parse each pronoun: Person (1st/2nd), Case (Nom/Gen/Dat/Acc), '
            'Number (Sg/Pl), and Translation.'
        )
        hdrs = ['#', 'Form', 'Person', 'Case', 'Number', 'Translation']
        cr = [0.05, 0.12, 0.12, 0.12, 0.12, 0.47]
        gk = [1]
        rows = [
            ['1',  'ἐγώ',    '', '', '', ''], ['2',  'μου',    '', '', '', ''],
            ['3',  'σύ',     '', '', '', ''], ['4',  'ἡμεῖς', '', '', '', ''],
            ['5',  'ὑμῶν',   '', '', '', ''], ['6',  'μοι',    '', '', '', ''],
            ['7',  'σοί',    '', '', '', ''], ['8',  'ἡμᾶς',  '', '', '', ''],
            ['9',  'σε',     '', '', '', ''], ['10', 'ἐμέ',    '', '', '', ''],
            ['11', 'ὑμεῖς', '', '', '', ''], ['12', 'ἡμῖν',  '', '', '', ''],
            ['13', 'σου',    '', '', '', ''], ['14', 'ὑμᾶς',  '', '', '', ''],
            ['15', 'ἐμοῦ',  '', '', '', ''], ['16', 'ὑμῖν',  '', '', '', ''],
            ['17', 'με',     '', '', '', ''], ['18', 'σοῦ',    '', '', '', ''],
            ['19', 'ἡμῶν',  '', '', '', ''], ['20', 'ἐμοί',  '', '', '', ''],
        ]
        ans = [
            ['1',  'ἐγώ',   '1st', 'Nom', 'Sg', '"I" (emphatic subject)'],
            ['2',  'μου',   '1st', 'Gen', 'Sg', '"my / of me" (enclitic)'],
            ['3',  'σύ',    '2nd', 'Nom', 'Sg', '"you" (emphatic subject)'],
            ['4',  'ἡμεῖς','1st', 'Nom', 'Pl', '"we"'],
            ['5',  'ὑμῶν', '2nd', 'Gen', 'Pl', '"your (pl.) / of you"'],
            ['6',  'μοι',   '1st', 'Dat', 'Sg', '"to/for me" (enclitic)'],
            ['7',  'σοί',   '2nd', 'Dat', 'Sg', '"to/for you" (emphatic)'],
            ['8',  'ἡμᾶς', '1st', 'Acc', 'Pl', '"us"'],
            ['9',  'σε',    '2nd', 'Acc', 'Sg', '"you" (enclitic)'],
            ['10', 'ἐμέ',   '1st', 'Acc', 'Sg', '"me" (emphatic)'],
            ['11', 'ὑμεῖς','2nd', 'Nom', 'Pl', '"you (pl.)"'],
            ['12', 'ἡμῖν', '1st', 'Dat', 'Pl', '"to/for us"'],
            ['13', 'σου',   '2nd', 'Gen', 'Sg', '"your / of you" (enclitic)'],
            ['14', 'ὑμᾶς', '2nd', 'Acc', 'Pl', '"you (pl.)"'],
            ['15', 'ἐμοῦ', '1st', 'Gen', 'Sg', '"my / of me" (emphatic)'],
            ['16', 'ὑμῖν', '2nd', 'Dat', 'Pl', '"to/for you (pl.)"'],
            ['17', 'με',    '1st', 'Acc', 'Sg', '"me" (enclitic)'],
            ['18', 'σοῦ',   '2nd', 'Gen', 'Sg', '"your / of you" (emphatic)'],
            ['19', 'ἡμῶν', '1st', 'Gen', 'Pl', '"our / of us"'],
            ['20', 'ἐμοί', '1st', 'Dat', 'Sg', '"to/for me" (emphatic)'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Drill Table', use_greek=True)


def build_bbg_ch11_pronoun_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh11PronounParsingPDF,
        'BBG Chapter 11 — Personal Pronoun Parsing Drill',
        'First and Second Person Pronouns',
        ['greek', 'bbg', 'ch11', 'exercises', 'ch11-pronoun-parsing'],
        'ch11-pronoun-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch12 — αὐτός Parsing and Use Identification
# ---------------------------------------------------------------------------

class BbgCh12AutosParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each item: (1) Case (N/G/D/A), (2) Number (S/P), (3) Gender (M/F/N), '
            '(4) Use — PP = Personal Pronoun, INT = Intensive Adjective (predicate position), '
            'SAME = Identical Adjective (attributive position, article before αὐτός).'
        )
        hdrs = ['#', 'Greek Phrase', 'Case', 'Number', 'Gender', 'Use']
        cr = [0.04, 0.28, 0.10, 0.10, 0.10, 0.38]
        gk = [1]
        rows = [
            ['1',  'λέγει αὐτῷ',              '', '', '', ''],
            ['2',  'αὐτὸς ὁ κύριος',          '', '', '', ''],
            ['3',  'ὁ αὐτὸς λόγος',           '', '', '', ''],
            ['4',  'βλέπω αὐτόν',             '', '', '', ''],
            ['5',  'αὐτὴ ἡ γυνή',             '', '', '', ''],
            ['6',  'ἐν τῷ αὐτῷ τόπῳ',        '', '', '', ''],
            ['7',  'ἔδωκεν αὐτοῖς',           '', '', '', ''],
            ['8',  'αὐτοὶ οἱ μαθηταί',        '', '', '', ''],
            ['9',  'τὸ αὐτὸ πνεῦμα',          '', '', '', ''],
            ['10', 'ἤκουσαν αὐτῆς',           '', '', '', ''],
            ['11', 'αὐτὸς Ἰησοῦς',            '', '', '', ''],
            ['12', 'ἡ αὐτὴ ἐντολή',           '', '', '', ''],
            ['13', 'ἀπέστειλεν αὐτούς',       '', '', '', ''],
            ['14', 'ὁ λόγος αὐτοῦ',           '', '', '', ''],
            ['15', 'αὐτὴ εἶπεν',              '', '', '', ''],
            ['16', 'τῆς αὐτῆς χάριτος',       '', '', '', ''],
            ['17', 'εἶδεν αὐτά',              '', '', '', ''],
            ['18', 'αὐτοὶ ἐλάλησαν',          '', '', '', ''],
            ['19', 'τοῖς αὐτοῖς ἀδελφοῖς',    '', '', '', ''],
            ['20', 'πιστεύει εἰς αὐτήν',       '', '', '', ''],
        ]
        ans = [
            ['1',  'λέγει αὐτῷ',             'D', 'S', 'M', 'PP — "he says to him"'],
            ['2',  'αὐτὸς ὁ κύριος',         'N', 'S', 'M', 'INT — "the Lord himself"'],
            ['3',  'ὁ αὐτὸς λόγος',          'N', 'S', 'M', 'SAME — "the same word"'],
            ['4',  'βλέπω αὐτόν',            'A', 'S', 'M', 'PP — "I see him"'],
            ['5',  'αὐτὴ ἡ γυνή',            'N', 'S', 'F', 'INT — "the woman herself"'],
            ['6',  'ἐν τῷ αὐτῷ τόπῳ',       'D', 'S', 'M', 'SAME — "in the same place"'],
            ['7',  'ἔδωκεν αὐτοῖς',          'D', 'P', 'M', 'PP — "he gave to them"'],
            ['8',  'αὐτοὶ οἱ μαθηταί',       'N', 'P', 'M', 'INT — "the disciples themselves"'],
            ['9',  'τὸ αὐτὸ πνεῦμα',         'N', 'S', 'N', 'SAME — "the same spirit"'],
            ['10', 'ἤκουσαν αὐτῆς',          'G', 'S', 'F', 'PP — "they heard her"'],
            ['11', 'αὐτὸς Ἰησοῦς',           'N', 'S', 'M', 'INT — "Jesus himself"'],
            ['12', 'ἡ αὐτὴ ἐντολή',          'N', 'S', 'F', 'SAME — "the same commandment"'],
            ['13', 'ἀπέστειλεν αὐτούς',      'A', 'P', 'M', 'PP — "he sent them"'],
            ['14', 'ὁ λόγος αὐτοῦ',          'G', 'S', 'M', 'PP — "his word"'],
            ['15', 'αὐτὴ εἶπεν',             'N', 'S', 'F', 'INT — "she herself said"'],
            ['16', 'τῆς αὐτῆς χάριτος',      'G', 'S', 'F', 'SAME — "of the same grace"'],
            ['17', 'εἶδεν αὐτά',             'A', 'P', 'N', 'PP — "he saw them"'],
            ['18', 'αὐτοὶ ἐλάλησαν',         'N', 'P', 'M', 'INT — "they themselves spoke"'],
            ['19', 'τοῖς αὐτοῖς ἀδελφοῖς',   'D', 'P', 'M', 'SAME — "to the same brothers"'],
            ['20', 'πιστεύει εἰς αὐτήν',      'A', 'S', 'F', 'PP — "he believes in her/it"'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Drill Table', use_greek=True)


def build_bbg_ch12_autos_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh12AutosParsingPDF,
        'BBG Chapter 12 — αὐτός Parsing and Use Identification',
        'Personal Pronoun · Intensive · Identical Adjective',
        ['greek', 'bbg', 'ch12', 'exercises', 'ch12-autos-parsing'],
        'ch12-autos-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch13 — Demonstrative Parsing Drill
# ---------------------------------------------------------------------------

class BbgCh13DemonstrativeParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each item: (1) parse the demonstrative — Gender, Case, Number, Lexical form; '
            '(2) identify use as Adjective (A) or Pronoun (P).'
        )
        hdrs = ['#', 'Form', 'Context phrase', 'Gender', 'Case', 'Number', 'Lexical', 'Use']
        cr = [0.04, 0.11, 0.27, 0.08, 0.08, 0.08, 0.11, 0.23]
        gk = [1, 2]
        rows = [
            ['1',  'οὗτος',   'οὗτος ὁ ἄνθρωπος',      '', '', '', '', ''],
            ['2',  'τοῦτο',   'λέγω ὑμῖν τοῦτο',        '', '', '', '', ''],
            ['3',  'ταύτης',  'ἐκ τῆς γενεᾶς ταύτης',   '', '', '', '', ''],
            ['4',  'τούτους', 'τοὺς νόμους τούτους',     '', '', '', '', ''],
            ['5',  'αὕτη',    'αὕτη ἐστὶν ἡ ἐντολή',    '', '', '', '', ''],
            ['6',  'ταῦτα',   'ταῦτα εἶπεν Ἰησοῦς',     '', '', '', '', ''],
            ['7',  'τούτῳ',   'ἐν τούτῳ τῷ τόπῳ',       '', '', '', '', ''],
            ['8',  'τούτων',  'ἡ ἀρχὴ τούτων',          '', '', '', '', ''],
            ['9',  'αὗται',   'αὗται αἱ γυναῖκες',       '', '', '', '', ''],
            ['10', 'τοῦτον',  'τοῦτον τὸν ἄνδρα εἶδον', '', '', '', '', ''],
            ['11', 'ἐκεῖνος', 'ἐκεῖνος ὑμᾶς διδάξει',   '', '', '', '', ''],
            ['12', 'ἐκείνην', 'τοῦτον τὸν ἄνδρα εἶδον', '', '', '', '', ''],
            ['13', 'ἐκεῖνο',  'ἐκεῖνο τὸ ἔργον ἦν καλόν','', '', '', '', ''],
            ['14', 'ἐκείνης', 'ἡ βασιλεία ἐκείνης',     '', '', '', '', ''],
            ['15', 'ἐκεῖνοι', 'ἐκεῖνοι οἱ μαθηταί',     '', '', '', '', ''],
            ['16', 'ἐκείνων', 'ἀπὸ τῶν ἡμερῶν ἐκείνων', '', '', '', '', ''],
            ['17', 'ἐκεῖνα',  'ἐκεῖνα ἤκουσαν',         '', '', '', '', ''],
            ['18', 'ἐκείνῃ',  'ἐν ἐκείνῃ τῇ ἡμέρᾳ',    '', '', '', '', ''],
            ['19', 'τούτοις', 'τοῖς νόμοις τούτοις',    '', '', '', '', ''],
            ['20', 'ἐκείνοις','ἐκείνοις τοῖς ἀνθρώποις','', '', '', '', ''],
        ]
        ans = [
            ['1',  'οὗτος',   'οὗτος ὁ ἄνθρωπος',       'M', 'N', 'S', 'οὗτος',   'A'],
            ['2',  'τοῦτο',   'λέγω ὑμῖν τοῦτο',         'N', 'A', 'S', 'οὗτος',   'P'],
            ['3',  'ταύτης',  'ἐκ τῆς γενεᾶς ταύτης',    'F', 'G', 'S', 'οὗτος',   'A'],
            ['4',  'τούτους', 'τοὺς νόμους τούτους',      'M', 'A', 'P', 'οὗτος',   'A'],
            ['5',  'αὕτη',    'αὕτη ἐστὶν ἡ ἐντολή',     'F', 'N', 'S', 'οὗτος',   'P'],
            ['6',  'ταῦτα',   'ταῦτα εἶπεν Ἰησοῦς',      'N', 'A', 'P', 'οὗτος',   'P'],
            ['7',  'τούτῳ',   'ἐν τούτῳ τῷ τόπῳ',        'M', 'D', 'S', 'οὗτος',   'A'],
            ['8',  'τούτων',  'ἡ ἀρχὴ τούτων',           'M/N','G','P', 'οὗτος',   'P'],
            ['9',  'αὗται',   'αὗται αἱ γυναῖκες',        'F', 'N', 'P', 'οὗτος',   'A'],
            ['10', 'τοῦτον',  'τοῦτον τὸν ἄνδρα εἶδον',  'M', 'A', 'S', 'οὗτος',   'A'],
            ['11', 'ἐκεῖνος', 'ἐκεῖνος ὑμᾶς διδάξει',    'M', 'N', 'S', 'ἐκεῖνος', 'P'],
            ['12', 'ἐκείνην', 'ἐν ἐκείνῃ τῇ ὥρᾳ',        'F', 'A', 'S', 'ἐκεῖνος', 'A'],
            ['13', 'ἐκεῖνο',  'ἐκεῖνο τὸ ἔργον ἦν καλόν','N', 'N', 'S', 'ἐκεῖνος', 'A'],
            ['14', 'ἐκείνης', 'ἡ βασιλεία ἐκείνης',      'F', 'G', 'S', 'ἐκεῖνος', 'A'],
            ['15', 'ἐκεῖνοι', 'ἐκεῖνοι οἱ μαθηταί',      'M', 'N', 'P', 'ἐκεῖνος', 'A'],
            ['16', 'ἐκείνων', 'ἀπὸ τῶν ἡμερῶν ἐκείνων',  'M/N','G','P', 'ἐκεῖνος', 'A'],
            ['17', 'ἐκεῖνα',  'ἐκεῖνα ἤκουσαν',          'N', 'A', 'P', 'ἐκεῖνος', 'P'],
            ['18', 'ἐκείνῃ',  'ἐν ἐκείνῃ τῇ ἡμέρᾳ',      'F', 'D', 'S', 'ἐκεῖνος', 'A'],
            ['19', 'τούτοις', 'τοῖς νόμοις τούτοις',     'M/N','D','P', 'οὗτος',   'A'],
            ['20', 'ἐκείνοις','ἐκείνοις τοῖς ἀνθρώποις', 'M/N','D','P', 'ἐκεῖνος', 'A'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Drill Table', use_greek=True)


def build_bbg_ch13_demonstrative_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh13DemonstrativeParsingPDF,
        'BBG Chapter 13 — Demonstrative Parsing Drill',
        'οὗτος and ἐκεῖνος — Adjective vs. Pronoun Use',
        ['greek', 'bbg', 'ch13', 'exercises', 'ch13-demonstrative-parsing'],
        'ch13-demonstrative-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch14 — Relative Pronoun Parsing Drill
# ---------------------------------------------------------------------------

class BbgCh14RelativeParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each item: (1) Gender, (2) Case, (3) Number of the relative pronoun; '
            '(4) identify its Antecedent; (5) translate the clause. '
            'Remember: gender/number from antecedent; case from function in relative clause.'
        )
        hdrs = ['#', 'Phrase/Clause', 'Gender', 'Case', 'Number', 'Antecedent', 'Translation']
        cr = [0.04, 0.26, 0.08, 0.07, 0.08, 0.14, 0.33]
        gk = [1]
        rows = [
            ['1',  'ὁ ἄνθρωπος ὃν εἶδον',           '', '', '', '', ''],
            ['2',  'ἡ γυνή ἣν ἀγαπᾷς',              '', '', '', '', ''],
            ['3',  'τὸ τέκνον ὃ εἶχεν',              '', '', '', '', ''],
            ['4',  'οἱ μαθηταί οἳ ἤκουσαν',         '', '', '', '', ''],
            ['5',  'ἡ ὥρα ἐν ᾗ ἀκούσουσιν',         '', '', '', '', ''],
            ['6',  'ὁ λόγος οὗ ἤκουσας',             '', '', '', '', ''],
            ['7',  'τὰ ἔργα ἃ ποιεῖ',               '', '', '', '', ''],
            ['8',  'ὁ ἄγγελος ᾧ ἐλάλησεν',          '', '', '', '', ''],
            ['9',  'αἱ γυναῖκες αἷς εἶπεν',         '', '', '', '', ''],
            ['10', 'ὁ πατήρ οὗ ὁ υἱός ἐστιν',       '', '', '', '', ''],
            ['11', 'τὸ ῥῆμα ὃ εἶπεν αὐτοῖς',        '', '', '', '', ''],
            ['12', 'πᾶς ὃς πιστεύει εἰς αὐτόν',     '', '', '', '', ''],
            ['13', 'ἡ βασιλεία ἧς οὐκ ἔσται τέλος', '', '', '', '', ''],
            ['14', 'οἱ νόμοι οἷς πιστεύετε',        '', '', '', '', ''],
            ['15', 'τὰ τέκνα ὧν ὁ πατήρ ἐστιν',     '', '', '', '', ''],
            ['16', 'ὁ τόπος εἰς ὃν πορεύεται',      '', '', '', '', ''],
            ['17', 'ἡ ἡμέρα ἐν ᾗ ἦλθεν',            '', '', '', '', ''],
            ['18', 'οἱ ἄνθρωποι οὓς ἀπέστειλεν',    '', '', '', '', ''],
            ['19', 'ὃ ποιεῖς, ποίησον τάχιον',       '', '', '', '', ''],
            ['20', 'ἡ ἀλήθεια ἣν ἀκούετε',          '', '', '', '', ''],
        ]
        ans = [
            ['1',  'ὁ ἄνθρωπος ὃν εἶδον',          'M', 'A', 'S', 'ὁ ἄνθρωπος', '"the man whom I saw"'],
            ['2',  'ἡ γυνή ἣν ἀγαπᾷς',             'F', 'A', 'S', 'ἡ γυνή',     '"the woman whom you love"'],
            ['3',  'τὸ τέκνον ὃ εἶχεν',             'N', 'A', 'S', 'τὸ τέκνον',  '"the child that he had"'],
            ['4',  'οἱ μαθηταί οἳ ἤκουσαν',        'M', 'N', 'P', 'οἱ μαθηταί', '"the disciples who heard"'],
            ['5',  'ἡ ὥρα ἐν ᾗ ἀκούσουσιν',        'F', 'D', 'S', 'ἡ ὥρα',      '"the hour in which they will hear"'],
            ['6',  'ὁ λόγος οὗ ἤκουσας',            'M', 'G', 'S', 'ὁ λόγος',    '"the word of which you heard"'],
            ['7',  'τὰ ἔργα ἃ ποιεῖ',              'N', 'A', 'P', 'τὰ ἔργα',    '"the works that he does"'],
            ['8',  'ὁ ἄγγελος ᾧ ἐλάλησεν',         'M', 'D', 'S', 'ὁ ἄγγελος',  '"the angel to whom he spoke"'],
            ['9',  'αἱ γυναῖκες αἷς εἶπεν',        'F', 'D', 'P', 'αἱ γυναῖκες','"the women to whom he said"'],
            ['10', 'ὁ πατήρ οὗ ὁ υἱός ἐστιν',      'M', 'G', 'S', 'ὁ πατήρ',    '"the father whose son he is"'],
            ['11', 'τὸ ῥῆμα ὃ εἶπεν αὐτοῖς',       'N', 'A', 'S', 'τὸ ῥῆμα',    '"the word that he said to them"'],
            ['12', 'πᾶς ὃς πιστεύει εἰς αὐτόν',    'M', 'N', 'S', 'πᾶς',        '"everyone who believes in him"'],
            ['13', 'ἡ βασιλεία ἧς οὐκ ἔσται τέλος','F', 'G', 'S', 'ἡ βασιλεία', '"the kingdom of which there is no end"'],
            ['14', 'οἱ νόμοι οἷς πιστεύετε',       'M', 'D', 'P', 'οἱ νόμοι',   '"the laws in which you believe"'],
            ['15', 'τὰ τέκνα ὧν ὁ πατήρ ἐστιν',    'N', 'G', 'P', 'τὰ τέκνα',   '"the children whose father he is"'],
            ['16', 'ὁ τόπος εἰς ὃν πορεύεται',     'M', 'A', 'S', 'ὁ τόπος',    '"the place to which he is going"'],
            ['17', 'ἡ ἡμέρα ἐν ᾗ ἦλθεν',           'F', 'D', 'S', 'ἡ ἡμέρα',    '"the day on which he came"'],
            ['18', 'οἱ ἄνθρωποι οὓς ἀπέστειλεν',   'M', 'A', 'P', 'οἱ ἄνθρωποι','"the men whom he sent"'],
            ['19', 'ὃ ποιεῖς, ποίησον τάχιον',      'N', 'A', 'S', '(none)',      '"What you do, do quickly" (John 13:27)'],
            ['20', 'ἡ ἀλήθεια ἣν ἀκούετε',         'F', 'A', 'S', 'ἡ ἀλήθεια',  '"the truth that you hear"'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Drill Table', use_greek=True)


def build_bbg_ch14_relative_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh14RelativeParsingPDF,
        'BBG Chapter 14 — Relative Pronoun Parsing Drill',
        'ὅς, ἥ, ὅ — Gender/Number from Antecedent; Case from Clause Function',
        ['greek', 'bbg', 'ch14', 'exercises', 'ch14-relative-parsing'],
        'ch14-relative-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch16 — Present Active Indicative Parsing Drill
# ---------------------------------------------------------------------------

class BbgCh16PresentActiveParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'All verbs are Present Active Indicative. '
            'Provide: Person · Number · Lexical Form · Translation.'
        )
        hdrs = ['#', 'Form', 'Person', 'Number', 'Lexical Form', 'Translation']
        cr = [0.04, 0.16, 0.10, 0.10, 0.16, 0.44]
        gk = [1]
        rows = [
            ['1',  'λύω',         '', '', '', ''], ['2',  'λύεις',       '', '', '', ''],
            ['3',  'λύει',        '', '', '', ''], ['4',  'λύομεν',      '', '', '', ''],
            ['5',  'λύετε',       '', '', '', ''], ['6',  'λύουσιν',     '', '', '', ''],
            ['7',  'πιστεύω',     '', '', '', ''], ['8',  'γινώσκεις',   '', '', '', ''],
            ['9',  'ἀκούει',      '', '', '', ''], ['10', 'βλέπομεν',    '', '', '', ''],
            ['11', 'λέγετε',      '', '', '', ''], ['12', 'γράφουσιν',   '', '', '', ''],
            ['13', 'ἔχω',         '', '', '', ''], ['14', 'εὑρίσκεις',   '', '', '', ''],
            ['15', 'λαμβάνει',    '', '', '', ''], ['16', 'διδάσκομεν',  '', '', '', ''],
            ['17', 'κρίνετε',     '', '', '', ''], ['18', 'ἄγουσιν',     '', '', '', ''],
            ['19', 'πέμπω',       '', '', '', ''], ['20', 'σῴζει',       '', '', '', ''],
        ]
        ans = [
            ['1',  'λύω',        '1st', 'Sg', 'λύω',       'I am loosing / I loose'],
            ['2',  'λύεις',      '2nd', 'Sg', 'λύω',       'You are loosing'],
            ['3',  'λύει',       '3rd', 'Sg', 'λύω',       'He/she/it is loosing'],
            ['4',  'λύομεν',     '1st', 'Pl', 'λύω',       'We are loosing'],
            ['5',  'λύετε',      '2nd', 'Pl', 'λύω',       'You (pl.) are loosing'],
            ['6',  'λύουσιν',    '3rd', 'Pl', 'λύω',       'They are loosing'],
            ['7',  'πιστεύω',    '1st', 'Sg', 'πιστεύω',   'I believe'],
            ['8',  'γινώσκεις',  '2nd', 'Sg', 'γινώσκω',   'You know'],
            ['9',  'ἀκούει',     '3rd', 'Sg', 'ἀκούω',     'He/she hears'],
            ['10', 'βλέπομεν',   '1st', 'Pl', 'βλέπω',     'We see'],
            ['11', 'λέγετε',     '2nd', 'Pl', 'λέγω',      'You (pl.) are saying'],
            ['12', 'γράφουσιν',  '3rd', 'Pl', 'γράφω',     'They are writing'],
            ['13', 'ἔχω',        '1st', 'Sg', 'ἔχω',       'I have'],
            ['14', 'εὑρίσκεις',  '2nd', 'Sg', 'εὑρίσκω',   'You are finding'],
            ['15', 'λαμβάνει',   '3rd', 'Sg', 'λαμβάνω',   'He/she takes'],
            ['16', 'διδάσκομεν', '1st', 'Pl', 'διδάσκω',   'We are teaching'],
            ['17', 'κρίνετε',    '2nd', 'Pl', 'κρίνω',     'You (pl.) are judging'],
            ['18', 'ἄγουσιν',    '3rd', 'Pl', 'ἄγω',       'They are leading'],
            ['19', 'πέμπω',      '1st', 'Sg', 'πέμπω',     'I am sending'],
            ['20', 'σῴζει',      '3rd', 'Sg', 'σῴζω',      'He/she saves'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Parsing Table', use_greek=True)


def build_bbg_ch16_present_active_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh16PresentActiveParsingPDF,
        'BBG Chapter 16 — Present Active Indicative Parsing Drill',
        'λύω Paradigm and Common Verbs',
        ['greek', 'bbg', 'ch16', 'exercises', 'ch16-present-active-parsing'],
        'ch16-present-active-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch17 — Contract Verb Parsing Drill
# ---------------------------------------------------------------------------

class BbgCh17ContractVerbParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each contracted form: (1) Person, (2) Number, (3) Lexical form, '
            '(4) the two vowels that contracted (stem vowel + C.V.), (5) Translation.'
        )
        hdrs = ['#', 'Contracted form', 'Person', 'Number', 'Lexical form', 'Contraction', 'Translation']
        cr = [0.04, 0.16, 0.09, 0.09, 0.14, 0.16, 0.32]
        gk = [1]
        rows = [
            ['1',  'ἀγαπῶ',      '', '', '', '', ''], ['2',  'ἀγαπᾷς',    '', '', '', '', ''],
            ['3',  'ἀγαπᾷ',      '', '', '', '', ''], ['4',  'ἀγαπῶμεν',  '', '', '', '', ''],
            ['5',  'ἀγαπᾶτε',    '', '', '', '', ''], ['6',  'ἀγαπῶσιν',  '', '', '', '', ''],
            ['7',  'ποιῶ',       '', '', '', '', ''], ['8',  'ποιεῖς',    '', '', '', '', ''],
            ['9',  'ποιεῖ',      '', '', '', '', ''], ['10', 'ποιοῦμεν',  '', '', '', '', ''],
            ['11', 'ποιεῖτε',    '', '', '', '', ''], ['12', 'ποιοῦσιν',  '', '', '', '', ''],
            ['13', 'πληρῶ',      '', '', '', '', ''], ['14', 'πληροῖς',   '', '', '', '', ''],
            ['15', 'πληροῖ',     '', '', '', '', ''], ['16', 'πληροῦμεν', '', '', '', '', ''],
            ['17', 'πληροῦτε',   '', '', '', '', ''], ['18', 'λαλεῖς',    '', '', '', '', ''],
            ['19', 'ζητεῖτε',    '', '', '', '', ''], ['20', 'τιμῶ',      '', '', '', '', ''],
        ]
        ans = [
            ['1',  'ἀγαπῶ',     '1st', 'Sg', 'ἀγαπάω', 'α+ω→ω',  'I love'],
            ['2',  'ἀγαπᾷς',    '2nd', 'Sg', 'ἀγαπάω', 'α+ει→ᾳ', 'You love'],
            ['3',  'ἀγαπᾷ',     '3rd', 'Sg', 'ἀγαπάω', 'α+ει→ᾳ', 'He/she loves'],
            ['4',  'ἀγαπῶμεν',  '1st', 'Pl', 'ἀγαπάω', 'α+ο→ω',  'We love'],
            ['5',  'ἀγαπᾶτε',   '2nd', 'Pl', 'ἀγαπάω', 'α+ε→ᾱ',  'You (pl.) love'],
            ['6',  'ἀγαπῶσιν',  '3rd', 'Pl', 'ἀγαπάω', 'α+ου→ω', 'They love'],
            ['7',  'ποιῶ',      '1st', 'Sg', 'ποιέω',  'ε+ω→ω',  'I do/make'],
            ['8',  'ποιεῖς',    '2nd', 'Sg', 'ποιέω',  'ε+ε→ει', 'You do/make'],
            ['9',  'ποιεῖ',     '3rd', 'Sg', 'ποιέω',  'ε+ει→ει','He/she does/makes'],
            ['10', 'ποιοῦμεν',  '1st', 'Pl', 'ποιέω',  'ε+ο→ου', 'We do/make'],
            ['11', 'ποιεῖτε',   '2nd', 'Pl', 'ποιέω',  'ε+ε→ει', 'You (pl.) do/make'],
            ['12', 'ποιοῦσιν',  '3rd', 'Pl', 'ποιέω',  'ε+ου→ου','They do/make'],
            ['13', 'πληρῶ',     '1st', 'Sg', 'πληρόω', 'ο+ω→ω',  'I fill/fulfill'],
            ['14', 'πληροῖς',   '2nd', 'Sg', 'πληρόω', 'ο+ει→οι','You fill'],
            ['15', 'πληροῖ',    '3rd', 'Sg', 'πληρόω', 'ο+ει→οι','He/she fills'],
            ['16', 'πληροῦμεν', '1st', 'Pl', 'πληρόω', 'ο+ο→ου', 'We fill'],
            ['17', 'πληροῦτε',  '2nd', 'Pl', 'πληρόω', 'ο+ε→ου', 'You (pl.) fill'],
            ['18', 'λαλεῖς',    '2nd', 'Sg', 'λαλέω',  'ε+ε→ει', 'You speak'],
            ['19', 'ζητεῖτε',   '2nd', 'Pl', 'ζητέω',  'ε+ε→ει', 'You (pl.) seek'],
            ['20', 'τιμῶ',      '1st', 'Sg', 'τιμάω',  'α+ω→ω',  'I honor'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Parsing Table', use_greek=True)


def build_bbg_ch17_contract_verb_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh17ContractVerbParsingPDF,
        'BBG Chapter 17 — Contract Verb Parsing Drill',
        'α-, ε-, ο-Contract Verbs',
        ['greek', 'bbg', 'ch17', 'exercises', 'ch17-contract-verb-parsing'],
        'ch17-contract-verb-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch18 — Present Middle/Passive Indicative
# ---------------------------------------------------------------------------

class BbgCh18MiddlePassiveParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each verb: (1) Person, (2) Number, (3) Lexical form, '
            '(4) Voice — Middle / Passive / Deponent, (5) Translation.'
        )
        hdrs = ['#', 'Form', 'Context', 'Person', 'Number', 'Lexical form', 'Voice', 'Translation']
        cr = [0.04, 0.13, 0.15, 0.07, 0.07, 0.13, 0.11, 0.30]
        rows = [
            ['1',  'λύομαι',       '(no context)',            '', '', '', '', ''],
            ['2',  'λύῃ',          '(no context)',            '', '', '', '', ''],
            ['3',  'λύεται',       'ὑπὸ τοῦ κυρίου',         '', '', '', '', ''],
            ['4',  'λυόμεθα',      '(no context)',            '', '', '', '', ''],
            ['5',  'λύεσθε',       '(no context)',            '', '', '', '', ''],
            ['6',  'λύονται',      'ὑπὸ αὐτοῦ',              '', '', '', '', ''],
            ['7',  'ἔρχεται',      'πρὸς τὸν Ἰησοῦν',        '', '', '', '', ''],
            ['8',  'ἔρχομαι',      '(speaker going)',         '', '', '', '', ''],
            ['9',  'γίνεται',      'σάρξ',                   '', '', '', '', ''],
            ['10', 'πορεύεσθε',    '(command context)',       '', '', '', '', ''],
            ['11', 'ἀποκρίνεται',  'ὁ Ἰησοῦς',               '', '', '', '', ''],
            ['12', 'προσεύχεσθε',  '(2nd pl)',                '', '', '', '', ''],
            ['13', 'δέχονται',     'τοὺς ἀγγέλους',          '', '', '', '', ''],
            ['14', 'βαπτίζεται',   'ὑπὸ Ἰωάννου',            '', '', '', '', ''],
            ['15', 'βούλομαι',     "(speaker's will)",        '', '', '', '', ''],
            ['16', 'ἐρχόμεθα',     '(we are going)',          '', '', '', '', ''],
            ['17', 'πορεύῃ',       '(you go)',                '', '', '', '', ''],
            ['18', 'γίνεσθε',      '(become!)',               '', '', '', '', ''],
            ['19', 'λύεται',       '(no agent)',              '', '', '', '', ''],
            ['20', 'ἀσπάζονται',   '(they greet)',            '', '', '', '', ''],
        ]
        ans = [
            ['1',  'λύομαι',      '(no context)',       '1st', 'Sg', 'λύω',          'Mid/Pass', 'I am loosing/being loosed'],
            ['2',  'λύῃ',         '(no context)',       '2nd', 'Sg', 'λύω',          'Mid/Pass', 'You are loosing/being loosed'],
            ['3',  'λύεται',      'ὑπὸ τοῦ κυρίου',    '3rd', 'Sg', 'λύω',          'Passive',  'He/she is being loosed'],
            ['4',  'λυόμεθα',     '(no context)',       '1st', 'Pl', 'λύω',          'Mid/Pass', 'We are loosing/being loosed'],
            ['5',  'λύεσθε',      '(no context)',       '2nd', 'Pl', 'λύω',          'Mid/Pass', 'You (pl.) are being loosed'],
            ['6',  'λύονται',     'ὑπὸ αὐτοῦ',         '3rd', 'Pl', 'λύω',          'Passive',  'They are being loosed'],
            ['7',  'ἔρχεται',     'πρὸς τὸν Ἰησοῦν',  '3rd', 'Sg', 'ἔρχομαι',      'Deponent', 'He/she comes'],
            ['8',  'ἔρχομαι',     '(speaker going)',   '1st', 'Sg', 'ἔρχομαι',      'Deponent', 'I am coming'],
            ['9',  'γίνεται',     'σάρξ',              '3rd', 'Sg', 'γίνομαι',      'Deponent', 'He/she/it becomes'],
            ['10', 'πορεύεσθε',   '(command)',         '2nd', 'Pl', 'πορεύομαι',    'Deponent', 'Go! / You go'],
            ['11', 'ἀποκρίνεται', 'ὁ Ἰησοῦς',         '3rd', 'Sg', 'ἀποκρίνομαι',  'Deponent', 'He/she answers'],
            ['12', 'προσεύχεσθε', '(2nd pl)',          '2nd', 'Pl', 'προσεύχομαι',  'Deponent', 'You (pl.) pray'],
            ['13', 'δέχονται',    'τοὺς ἀγγέλους',    '3rd', 'Pl', 'δέχομαι',      'Deponent', 'They receive'],
            ['14', 'βαπτίζεται',  'ὑπὸ Ἰωάννου',      '3rd', 'Sg', 'βαπτίζω',      'Passive',  'He/she is being baptized'],
            ['15', 'βούλομαι',    "(speaker's will)",  '1st', 'Sg', 'βούλομαι',     'Deponent', 'I want / I wish'],
            ['16', 'ἐρχόμεθα',    '(we are going)',    '1st', 'Pl', 'ἔρχομαι',      'Deponent', 'We are coming'],
            ['17', 'πορεύῃ',      '(you go)',          '2nd', 'Sg', 'πορεύομαι',    'Deponent', 'You are going'],
            ['18', 'γίνεσθε',     '(become!)',         '2nd', 'Pl', 'γίνομαι',      'Deponent', 'Become! / you become'],
            ['19', 'λύεται',      '(no agent)',        '3rd', 'Sg', 'λύω',          'Mid/Pass', 'He loosens/is being loosed'],
            ['20', 'ἀσπάζονται',  '(they greet)',      '3rd', 'Pl', 'ἀσπάζομαι',    'Deponent', 'They greet'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=[1, 2],
                                       section_title='Parsing Table', use_greek=True)


def build_bbg_ch18_middle_passive_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh18MiddlePassiveParsingPDF,
        'BBG Chapter 18 — Present Middle/Passive Indicative Parsing Drill',
        'Middle, Passive, and Deponent Verbs',
        ['greek', 'bbg', 'ch18', 'exercises', 'ch18-middle-passive-parsing'],
        'ch18-middle-passive-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch19 — Future Active/Middle Parsing Drill
# ---------------------------------------------------------------------------

class BbgCh19FutureParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Provide: Tense · Voice · Person · Number · Lexical Form · Translation. '
            'Items 17–20 are future middle or deponent — identify voice correctly.'
        )
        hdrs = ['#', 'Form', 'Tense', 'Voice', 'Person', 'Number', 'Lexical Form', 'Translation']
        cr = [0.04, 0.14, 0.10, 0.09, 0.08, 0.08, 0.14, 0.33]
        gk = [1]
        rows = [
            ['1',  'λύσω',         '', '', '', '', '', ''], ['2',  'λύσεις',      '', '', '', '', '', ''],
            ['3',  'λύσει',        '', '', '', '', '', ''], ['4',  'λύσομεν',     '', '', '', '', '', ''],
            ['5',  'λύσετε',       '', '', '', '', '', ''], ['6',  'λύσουσιν',    '', '', '', '', '', ''],
            ['7',  'γράψω',        '', '', '', '', '', ''], ['8',  'ἄξει',        '', '', '', '', '', ''],
            ['9',  'πείσομεν',     '', '', '', '', '', ''], ['10', 'βλέψετε',     '', '', '', '', '', ''],
            ['11', 'ἀγαπήσω',      '', '', '', '', '', ''], ['12', 'ποιήσει',     '', '', '', '', '', ''],
            ['13', 'πληρώσομεν',   '', '', '', '', '', ''], ['14', 'μενῶ',        '', '', '', '', '', ''],
            ['15', 'μενεῖς',       '', '', '', '', '', ''], ['16', 'ἐγερεῖ',      '', '', '', '', '', ''],
            ['17', 'λύσομαι',      '', '', '', '', '', ''], ['18', 'λύσεται',     '', '', '', '', '', ''],
            ['19', 'λύσονται',     '', '', '', '', '', ''], ['20', 'ὄψομαι',      '', '', '', '', '', ''],
        ]
        ans = [
            ['1',  'λύσω',       'Fut', 'Act', '1st', 'Sg', 'λύω',      'I will loose'],
            ['2',  'λύσεις',     'Fut', 'Act', '2nd', 'Sg', 'λύω',      'You will loose'],
            ['3',  'λύσει',      'Fut', 'Act', '3rd', 'Sg', 'λύω',      'He/she will loose'],
            ['4',  'λύσομεν',    'Fut', 'Act', '1st', 'Pl', 'λύω',      'We will loose'],
            ['5',  'λύσετε',     'Fut', 'Act', '2nd', 'Pl', 'λύω',      'You (pl) will loose'],
            ['6',  'λύσουσιν',   'Fut', 'Act', '3rd', 'Pl', 'λύω',      'They will loose'],
            ['7',  'γράψω',      'Fut', 'Act', '1st', 'Sg', 'γράφω',    'I will write'],
            ['8',  'ἄξει',       'Fut', 'Act', '3rd', 'Sg', 'ἄγω',      'He/she will lead'],
            ['9',  'πείσομεν',   'Fut', 'Act', '1st', 'Pl', 'πείθω',    'We will persuade'],
            ['10', 'βλέψετε',    'Fut', 'Act', '2nd', 'Pl', 'βλέπω',    'You (pl) will see'],
            ['11', 'ἀγαπήσω',    'Fut', 'Act', '1st', 'Sg', 'ἀγαπάω',   'I will love'],
            ['12', 'ποιήσει',    'Fut', 'Act', '3rd', 'Sg', 'ποιέω',    'He/she will do/make'],
            ['13', 'πληρώσομεν', 'Fut', 'Act', '1st', 'Pl', 'πληρόω',   'We will fulfill'],
            ['14', 'μενῶ',       'Fut', 'Act', '1st', 'Sg', 'μένω',     'I will remain'],
            ['15', 'μενεῖς',     'Fut', 'Act', '2nd', 'Sg', 'μένω',     'You will remain'],
            ['16', 'ἐγερεῖ',     'Fut', 'Act', '3rd', 'Sg', 'ἐγείρω',   'He/she will raise'],
            ['17', 'λύσομαι',    'Fut', 'Mid', '1st', 'Sg', 'λύω',      'I will loose (for myself)'],
            ['18', 'λύσεται',    'Fut', 'Mid', '3rd', 'Sg', 'λύω',      'He/she will loose (for himself)'],
            ['19', 'λύσονται',   'Fut', 'Mid', '3rd', 'Pl', 'λύω',      'They will loose (for themselves)'],
            ['20', 'ὄψομαι',     'Fut', 'Mid', '1st', 'Sg', 'ὁράω',     'I will see (deponent)'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Parsing Table', use_greek=True)


def build_bbg_ch19_future_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh19FutureParsingPDF,
        'BBG Chapter 19 — Future Active and Middle Parsing Drill',
        'Sigma Tense Formant and Liquid Futures',
        ['greek', 'bbg', 'ch19', 'exercises', 'ch19-future-parsing'],
        'ch19-future-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch20 — Stem Change Drill
# ---------------------------------------------------------------------------

class BbgCh20StemChangeDrillPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each verb, provide: Verbal Root · Pattern (2/3/4) · Pattern Subtype · Future Form.'
        )
        hdrs = ['#', 'Present Form', 'Verbal Root', 'Pattern', 'Subtype', 'Future Form']
        cr = [0.04, 0.14, 0.13, 0.10, 0.35, 0.24]
        gk = [1, 5]
        rows = [
            ['1',  'γράφω',    '', '', '', ''], ['2',  'βλέπω',    '', '', '', ''],
            ['3',  'πέμπω',    '', '', '', ''], ['4',  'λείπω',    '', '', '', ''],
            ['5',  'ἄγω',      '', '', '', ''], ['6',  'ἄρχω',     '', '', '', ''],
            ['7',  'διώκω',    '', '', '', ''], ['8',  'κηρύσσω',  '', '', '', ''],
            ['9',  'πείθω',    '', '', '', ''], ['10', 'σῴζω',     '', '', '', ''],
            ['11', 'βαπτίζω',  '', '', '', ''], ['12', 'λαμβάνω',  '', '', '', ''],
            ['13', 'μανθάνω',  '', '', '', ''], ['14', 'ἁμαρτάνω', '', '', '', ''],
            ['15', 'τυγχάνω',  '', '', '', ''], ['16', 'λανθάνω',  '', '', '', ''],
            ['17', 'ὁράω',     '', '', '', ''], ['18', 'ἔρχομαι',  '', '', '', ''],
            ['19', 'φέρω',     '', '', '', ''], ['20', 'λέγω',     '', '', '', ''],
        ]
        ans = [
            ['1',  'γράφω',   'γραφ-',          '2', 'Labial stop (φ+σ→ψ)',        'γράψω'],
            ['2',  'βλέπω',   'βλεπ-',          '2', 'Labial stop (π+σ→ψ)',        'βλέψω'],
            ['3',  'πέμπω',   'πεμπ-',          '2', 'Labial stop (π+σ→ψ)',        'πέμψω'],
            ['4',  'λείπω',   'λειπ-',          '2', 'Labial stop (2nd aorist)',    'λείψω'],
            ['5',  'ἄγω',     'ἀγ-',            '2', 'Velar stop (γ+σ→ξ)',         'ἄξω'],
            ['6',  'ἄρχω',    'ἀρχ-',           '2', 'Velar stop (χ+σ→ξ)',         'ἄρξω'],
            ['7',  'διώκω',   'διωκ-',          '2', 'Velar stop (κ+σ→ξ)',         'διώξω'],
            ['8',  'κηρύσσω', 'κηρυκ-',         '2', 'Velar stop (κ+σ→ξ)',         'κηρύξω'],
            ['9',  'πείθω',   'πειθ-',          '2', 'Dental stop (θ+σ→σ)',        'πείσω'],
            ['10', 'σῴζω',    'σῳδ-',           '2', 'Dental stop (δ+σ→σ)',        'σώσω'],
            ['11', 'βαπτίζω', 'βαπτιδ-',        '2', 'Dental stop (δ+σ→σ)',        'βαπτίσω'],
            ['12', 'λαμβάνω', 'λαβ-',           '3', 'Nasal infix (αμβ in pres.)', 'λήμψομαι'],
            ['13', 'μανθάνω', 'μαθ-',           '3', 'Nasal infix (αν in pres.)',  '(no future attested)'],
            ['14', 'ἁμαρτάνω','ἁμαρτ-',         '3', 'Nasal infix (αν in pres.)',  'ἁμαρτήσω'],
            ['15', 'τυγχάνω', 'τυχ-',           '3', 'Nasal infix (αν in pres.)',  'τεύξομαι'],
            ['16', 'λανθάνω', 'λαθ-',           '3', 'Nasal infix (αν in pres.)',  'λήσω'],
            ['17', 'ὁράω',    'ὁρ-/ὀπ-/ἰδ-',    '4', 'Suppletive',                 'ὄψομαι (dep.)'],
            ['18', 'ἔρχομαι', 'ἐρχ-/ἐλευθ-/ἐλθ-','4','Suppletive',                'ἐλεύσομαι (dep.)'],
            ['19', 'φέρω',    'φερ-/οἰ-/ἐνεγκ-', '4', 'Suppletive',               'οἴσω'],
            ['20', 'λέγω',    'λεγ-/ἐρ-/εἰπ-',  '4', 'Suppletive',                'ἐρῶ (liquid fut.)'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Drill Table', use_greek=True)


def build_bbg_ch20_stem_change_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh20StemChangeDrillPDF,
        'BBG Chapter 20 — Verbal Root and Stem Change Drill',
        'Patterns 2–4: Stop Mutation, Nasal Infix, Suppletive',
        ['greek', 'bbg', 'ch20', 'exercises', 'ch20-stem-change-drill'],
        'ch20-stem-change-drill.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch21 — Imperfect Parsing Drill
# ---------------------------------------------------------------------------

class BbgCh21ImperfectParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Provide: Tense · Voice · Person · Number · Augment Type · Lexical Form · Translation.'
        )
        hdrs = ['#', 'Form', 'Voice', 'Person', 'Number', 'Augment', 'Lexical Form', 'Translation']
        cr = [0.04, 0.14, 0.09, 0.08, 0.08, 0.15, 0.14, 0.28]
        gk = [1]
        rows = [
            ['1',  'ἔλυον',        '', '', '', '', '', ''], ['2',  'ἔλυες',       '', '', '', '', '', ''],
            ['3',  'ἔλυεν',        '', '', '', '', '', ''], ['4',  'ἐλύομεν',     '', '', '', '', '', ''],
            ['5',  'ἐλύετε',       '', '', '', '', '', ''], ['6',  'ἔγραφον',     '', '', '', '', '', ''],
            ['7',  'ἐπίστευον',    '', '', '', '', '', ''], ['8',  'ἐδίδασκεν',   '', '', '', '', '', ''],
            ['9',  'ἤκουον',       '', '', '', '', '', ''], ['10', 'ἤλπιζον',     '', '', '', '', '', ''],
            ['11', 'ηὔξανον',      '', '', '', '', '', ''], ['12', 'ἠγάπων',      '', '', '', '', '', ''],
            ['13', 'ἐλυόμην',      '', '', '', '', '', ''], ['14', 'ἐλύου',       '', '', '', '', '', ''],
            ['15', 'ἐλύετο',       '', '', '', '', '', ''], ['16', 'ἐλύοντο',     '', '', '', '', '', ''],
            ['17', 'ἦν',           '', '', '', '', '', ''], ['18', 'ἦσαν',        '', '', '', '', '', ''],
            ['19', 'ἐξέβαλλον',    '', '', '', '', '', ''], ['20', 'προσήρχοντο', '', '', '', '', '', ''],
        ]
        ans = [
            ['1',  'ἔλυον',       'Act',      '1/3rd','Sg/Pl','Syllabic (ε-)',  'λύω',          'I was loosing / they were loosing'],
            ['2',  'ἔλυες',       'Act',      '2nd',  'Sg',  'Syllabic (ε-)',  'λύω',          'You were loosing'],
            ['3',  'ἔλυεν',       'Act',      '3rd',  'Sg',  'Syllabic (ε-)',  'λύω',          'He/she was loosing'],
            ['4',  'ἐλύομεν',     'Act',      '1st',  'Pl',  'Syllabic (ε-)',  'λύω',          'We were loosing'],
            ['5',  'ἐλύετε',      'Act',      '2nd',  'Pl',  'Syllabic (ε-)',  'λύω',          'You (pl.) were loosing'],
            ['6',  'ἔγραφον',     'Act',      '1/3rd','Sg/Pl','Syllabic (ε-)', 'γράφω',        'I/they was/were writing'],
            ['7',  'ἐπίστευον',   'Act',      '1/3rd','Sg/Pl','Syllabic (ε-)', 'πιστεύω',      'I/they was/were believing'],
            ['8',  'ἐδίδασκεν',   'Act',      '3rd',  'Sg',  'Syllabic (ε-)',  'διδάσκω',      'He/she was teaching'],
            ['9',  'ἤκουον',      'Act',      '1/3rd','Sg/Pl','Temporal (α→η)','ἀκούω',        'I/they was/were hearing'],
            ['10', 'ἤλπιζον',     'Act',      '1/3rd','Sg/Pl','Temporal (ε→η)','ἐλπίζω',       'They were hoping'],
            ['11', 'ηὔξανον',     'Act',      '1/3rd','Sg/Pl','Temporal (αυ→ηυ)','αὐξάνω',     'They were growing'],
            ['12', 'ἠγάπων',      'Act',      '1/3rd','Sg/Pl','Temporal (α→η)','ἀγαπάω',       'They were loving'],
            ['13', 'ἐλυόμην',     'Mid/Pass', '1st',  'Sg',  'Syllabic (ε-)',  'λύω',          'I was loosing for myself'],
            ['14', 'ἐλύου',       'Mid/Pass', '2nd',  'Sg',  'Syllabic (ε-)',  'λύω',          'You were loosing for yourself'],
            ['15', 'ἐλύετο',      'Mid/Pass', '3rd',  'Sg',  'Syllabic (ε-)',  'λύω',          'He/she was loosing for himself'],
            ['16', 'ἐλύοντο',     'Mid/Pass', '3rd',  'Pl',  'Syllabic (ε-)',  'λύω',          'They were loosing for themselves'],
            ['17', 'ἦν',          'Act',      '3rd',  'Sg',  'Temporal (εἰμί)','εἰμί',         'He/she/it was'],
            ['18', 'ἦσαν',        'Act',      '3rd',  'Pl',  'Temporal (εἰμί)','εἰμί',         'They were'],
            ['19', 'ἐξέβαλλον',   'Act',      '1/3rd','Sg/Pl','Syllabic (after ἐκ-)','ἐκβάλλω','They were casting out'],
            ['20', 'προσήρχοντο', 'Mid/Pass', '3rd',  'Pl',  'Temporal (after πρός-)','προσέρχομαι','They were coming to'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Parsing Table', use_greek=True)


def build_bbg_ch21_imperfect_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh21ImperfectParsingPDF,
        'BBG Chapter 21 — Imperfect Indicative Parsing Drill',
        'Augment · Secondary Active and Middle/Passive Endings',
        ['greek', 'bbg', 'ch21', 'exercises', 'ch21-imperfect-parsing'],
        'ch21-imperfect-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch22 — Second Aorist Parsing Drill
# ---------------------------------------------------------------------------

class BbgCh22SecondAoristParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Provide: Tense (Aor 2nd or Impf) · Voice · Person · Number · Lexical Form · Translation. '
            'Items 11 and 18 are imperfect distractors — identify them correctly!'
        )
        hdrs = ['#', 'Form', 'Tense', 'Voice', 'Person', 'Number', 'Lexical Form', 'Translation']
        cr = [0.04, 0.14, 0.12, 0.09, 0.08, 0.08, 0.14, 0.31]
        gk = [1]
        rows = [
            ['1',  'ἔλαβον',     '', '', '', '', '', ''], ['2',  'ἔλαβες',     '', '', '', '', '', ''],
            ['3',  'ἔλαβεν',     '', '', '', '', '', ''], ['4',  'ἐλάβομεν',   '', '', '', '', '', ''],
            ['5',  'ἦλθον',      '', '', '', '', '', ''], ['6',  'ἦλθεν',      '', '', '', '', '', ''],
            ['7',  'εἶπον',      '', '', '', '', '', ''], ['8',  'εἶπεν',      '', '', '', '', '', ''],
            ['9',  'εἶδον',      '', '', '', '', '', ''], ['10', 'εἶδεν',      '', '', '', '', '', ''],
            ['11', 'ἐλάμβανον',  '', '', '', '', '', ''], ['12', 'ἔβαλον',     '', '', '', '', '', ''],
            ['13', 'εὗρον',      '', '', '', '', '', ''], ['14', 'ἀπέθανον',   '', '', '', '', '', ''],
            ['15', 'ἐγενόμην',   '', '', '', '', '', ''], ['16', 'ἐγένετο',    '', '', '', '', '', ''],
            ['17', 'ἐγένοντο',   '', '', '', '', '', ''], ['18', 'ἤρχοντο',    '', '', '', '', '', ''],
            ['19', 'ἔσχον',      '', '', '', '', '', ''], ['20', 'ἔπιον',      '', '', '', '', '', ''],
        ]
        ans = [
            ['1',  'ἔλαβον',    'Aor 2nd', 'Act', '1st',   'Sg', 'λαμβάνω',    'I took/received'],
            ['2',  'ἔλαβες',    'Aor 2nd', 'Act', '2nd',   'Sg', 'λαμβάνω',    'You took/received'],
            ['3',  'ἔλαβεν',    'Aor 2nd', 'Act', '3rd',   'Sg', 'λαμβάνω',    'He/she took/received'],
            ['4',  'ἐλάβομεν',  'Aor 2nd', 'Act', '1st',   'Pl', 'λαμβάνω',    'We took/received'],
            ['5',  'ἦλθον',     'Aor 2nd', 'Act', '1/3rd', 'Sg/Pl','ἔρχομαι',  'I came / They came'],
            ['6',  'ἦλθεν',     'Aor 2nd', 'Act', '3rd',   'Sg', 'ἔρχομαι',    'He/she came'],
            ['7',  'εἶπον',     'Aor 2nd', 'Act', '1/3rd', 'Sg/Pl','λέγω',     'I said / They said'],
            ['8',  'εἶπεν',     'Aor 2nd', 'Act', '3rd',   'Sg', 'λέγω',       'He/she said'],
            ['9',  'εἶδον',     'Aor 2nd', 'Act', '1/3rd', 'Sg/Pl','ὁράω',     'I saw / They saw'],
            ['10', 'εἶδεν',     'Aor 2nd', 'Act', '3rd',   'Sg', 'ὁράω',       'He/she saw'],
            ['11', 'ἐλάμβανον', 'IMPF',    'Act', '1/3rd', 'Sg/Pl','λαμβάνω',  'DISTRACTOR — they were taking'],
            ['12', 'ἔβαλον',    'Aor 2nd', 'Act', '1/3rd', 'Sg/Pl','βάλλω',    'They threw (single λ)'],
            ['13', 'εὗρον',     'Aor 2nd', 'Act', '1/3rd', 'Sg/Pl','εὑρίσκω',  'They found'],
            ['14', 'ἀπέθανον',  'Aor 2nd', 'Act', '1/3rd', 'Sg/Pl','ἀποθνῄσκω','They died'],
            ['15', 'ἐγενόμην',  'Aor 2nd', 'Mid', '1st',   'Sg', 'γίνομαι',    'I became'],
            ['16', 'ἐγένετο',   'Aor 2nd', 'Mid', '3rd',   'Sg', 'γίνομαι',    'It happened / He became'],
            ['17', 'ἐγένοντο',  'Aor 2nd', 'Mid', '3rd',   'Pl', 'γίνομαι',    'They became'],
            ['18', 'ἤρχοντο',   'IMPF',    'Mid', '3rd',   'Pl', 'ἔρχομαι',    'DISTRACTOR — they were coming'],
            ['19', 'ἔσχον',     'Aor 2nd', 'Act', '1/3rd', 'Sg/Pl','ἔχω',      'They had'],
            ['20', 'ἔπιον',     'Aor 2nd', 'Act', '1/3rd', 'Sg/Pl','πίνω',     'They drank'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Parsing Table', use_greek=True)


def build_bbg_ch22_second_aorist_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh22SecondAoristParsingPDF,
        'BBG Chapter 22 — Second Aorist Parsing Drill',
        'Second Aorist Active and Middle Indicative',
        ['greek', 'bbg', 'ch22', 'exercises', 'ch22-second-aorist-parsing'],
        'ch22-second-aorist-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch23 — First Aorist Parsing Drill
# ---------------------------------------------------------------------------

class BbgCh23FirstAoristParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Provide: Tense (1st Aor / 2nd Aor) · Voice · Person · Number · Lexical Form · Translation. '
            'Items 11 and 20 are second aorist distractors.'
        )
        hdrs = ['#', 'Form', 'Tense', 'Voice', 'Person', 'Number', 'Lexical Form', 'Translation']
        cr = [0.04, 0.14, 0.12, 0.09, 0.08, 0.08, 0.14, 0.31]
        gk = [1]
        rows = [
            ['1',  'ἔλυσα',        '', '', '', '', '', ''], ['2',  'ἔλυσας',      '', '', '', '', '', ''],
            ['3',  'ἔλυσεν',       '', '', '', '', '', ''], ['4',  'ἐλύσαμεν',    '', '', '', '', '', ''],
            ['5',  'ἐλύσατε',      '', '', '', '', '', ''], ['6',  'ἔλυσαν',      '', '', '', '', '', ''],
            ['7',  'ἐπίστευσεν',   '', '', '', '', '', ''], ['8',  'ἔγραψα',      '', '', '', '', '', ''],
            ['9',  'ἐκήρυξεν',     '', '', '', '', '', ''], ['10', 'ἔσωσεν',      '', '', '', '', '', ''],
            ['11', 'ἔβαλεν',       '', '', '', '', '', ''], ['12', 'ἔμεινα',      '', '', '', '', '', ''],
            ['13', 'ἤγειρεν',      '', '', '', '', '', ''], ['14', 'ἀπέστειλεν',  '', '', '', '', '', ''],
            ['15', 'ἠγάπησεν',     '', '', '', '', '', ''], ['16', 'ἐποίησεν',    '', '', '', '', '', ''],
            ['17', 'ἐπλήρωσεν',    '', '', '', '', '', ''], ['18', 'ἐλυσάμην',    '', '', '', '', '', ''],
            ['19', 'ἐλύσατο',      '', '', '', '', '', ''], ['20', 'ἦλθεν',       '', '', '', '', '', ''],
        ]
        ans = [
            ['1',  'ἔλυσα',       'Aor 1st', 'Act', '1st', 'Sg', 'λύω',         'I loosed'],
            ['2',  'ἔλυσας',      'Aor 1st', 'Act', '2nd', 'Sg', 'λύω',         'You loosed'],
            ['3',  'ἔλυσεν',      'Aor 1st', 'Act', '3rd', 'Sg', 'λύω',         'He/she loosed'],
            ['4',  'ἐλύσαμεν',    'Aor 1st', 'Act', '1st', 'Pl', 'λύω',         'We loosed'],
            ['5',  'ἐλύσατε',     'Aor 1st', 'Act', '2nd', 'Pl', 'λύω',         'You (pl) loosed'],
            ['6',  'ἔλυσαν',      'Aor 1st', 'Act', '3rd', 'Pl', 'λύω',         'They loosed'],
            ['7',  'ἐπίστευσεν',  'Aor 1st', 'Act', '3rd', 'Sg', 'πιστεύω',     'He/she believed'],
            ['8',  'ἔγραψα',      'Aor 1st', 'Act', '1st', 'Sg', 'γράφω',       'I wrote (φ+σ→ψ)'],
            ['9',  'ἐκήρυξεν',    'Aor 1st', 'Act', '3rd', 'Sg', 'κηρύσσω',     'He proclaimed (κ+σ→ξ)'],
            ['10', 'ἔσωσεν',      'Aor 1st', 'Act', '3rd', 'Sg', 'σῴζω',        'He saved (δ+σ→σ)'],
            ['11', 'ἔβαλεν',      'Aor 2nd', 'Act', '3rd', 'Sg', 'βάλλω',       'DISTRACTOR — 2nd aorist (no σ)'],
            ['12', 'ἔμεινα',      'Aor 1st', 'Act', '1st', 'Sg', 'μένω',        'I remained (liquid: ε→ει)'],
            ['13', 'ἤγειρεν',     'Aor 1st', 'Act', '3rd', 'Sg', 'ἐγείρω',      'He raised (liquid aorist)'],
            ['14', 'ἀπέστειλεν',  'Aor 1st', 'Act', '3rd', 'Sg', 'ἀποστέλλω',   'He sent (liquid: λλ→λ)'],
            ['15', 'ἠγάπησεν',    'Aor 1st', 'Act', '3rd', 'Sg', 'ἀγαπάω',      'He loved (contract α→η)'],
            ['16', 'ἐποίησεν',    'Aor 1st', 'Act', '3rd', 'Sg', 'ποιέω',       'He did/made (contract ε→η)'],
            ['17', 'ἐπλήρωσεν',   'Aor 1st', 'Act', '3rd', 'Sg', 'πληρόω',      'He fulfilled (contract ο→ω)'],
            ['18', 'ἐλυσάμην',    'Aor 1st', 'Mid', '1st', 'Sg', 'λύω',         'I loosed for myself'],
            ['19', 'ἐλύσατο',     'Aor 1st', 'Mid', '3rd', 'Sg', 'λύω',         'He loosed for himself'],
            ['20', 'ἦλθεν',       'Aor 2nd', 'Act', '3rd', 'Sg', 'ἔρχομαι',     'DISTRACTOR — suppletive 2nd aorist'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Parsing Table', use_greek=True)


def build_bbg_ch23_first_aorist_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh23FirstAoristParsingPDF,
        'BBG Chapter 23 — First Aorist Parsing Drill',
        'First Aorist Active and Middle Indicative',
        ['greek', 'bbg', 'ch23', 'exercises', 'ch23-first-aorist-parsing'],
        'ch23-first-aorist-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch24 — Aorist and Future Passive Parsing Drill
# ---------------------------------------------------------------------------

class BbgCh24AoristFuturePassiveParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Provide: Tense · Voice · Person · Number · Lexical Form · Translation. '
            'Items 19–20 are active/middle distractors — identify them correctly!'
        )
        hdrs = ['#', 'Form', 'Tense', 'Voice', 'Person', 'Number', 'Lexical Form', 'Translation']
        cr = [0.04, 0.16, 0.09, 0.09, 0.08, 0.08, 0.14, 0.32]
        gk = [1]
        rows = [
            ['1',  'ἐλύθην',       '', '', '', '', '', ''], ['2',  'ἐλύθης',      '', '', '', '', '', ''],
            ['3',  'ἐλύθη',        '', '', '', '', '', ''], ['4',  'ἐλύθημεν',    '', '', '', '', '', ''],
            ['5',  'ἐλύθητε',      '', '', '', '', '', ''], ['6',  'ἐλύθησαν',    '', '', '', '', '', ''],
            ['7',  'ἐβαπτίσθη',    '', '', '', '', '', ''], ['8',  'ἐσώθη',       '', '', '', '', '', ''],
            ['9',  'ἠγέρθη',       '', '', '', '', '', ''], ['10', 'ἐγράφη',      '', '', '', '', '', ''],
            ['11', 'ἐστράφη',      '', '', '', '', '', ''], ['12', 'ἐβλήθη',      '', '', '', '', '', ''],
            ['13', 'ἀπεκρίθη',     '', '', '', '', '', ''], ['14', 'ἐπορεύθη',    '', '', '', '', '', ''],
            ['15', 'λυθήσομαι',    '', '', '', '', '', ''], ['16', 'λυθήσεται',   '', '', '', '', '', ''],
            ['17', 'σωθήσεται',    '', '', '', '', '', ''], ['18', 'ἐγερθήσεται', '', '', '', '', '', ''],
            ['19', 'ἔλυσεν',       '', '', '', '', '', ''], ['20', 'ἐλύσατο',     '', '', '', '', '', ''],
        ]
        ans = [
            ['1',  'ἐλύθην',      'Aor', 'Pass', '1st', 'Sg', 'λύω',          'I was loosed'],
            ['2',  'ἐλύθης',      'Aor', 'Pass', '2nd', 'Sg', 'λύω',          'You were loosed'],
            ['3',  'ἐλύθη',       'Aor', 'Pass', '3rd', 'Sg', 'λύω',          'He/she was loosed'],
            ['4',  'ἐλύθημεν',    'Aor', 'Pass', '1st', 'Pl', 'λύω',          'We were loosed'],
            ['5',  'ἐλύθητε',     'Aor', 'Pass', '2nd', 'Pl', 'λύω',          'You (pl) were loosed'],
            ['6',  'ἐλύθησαν',    'Aor', 'Pass', '3rd', 'Pl', 'λύω',          'They were loosed'],
            ['7',  'ἐβαπτίσθη',   'Aor', 'Pass', '3rd', 'Sg', 'βαπτίζω',      'He/she was baptized'],
            ['8',  'ἐσώθη',       'Aor', 'Pass', '3rd', 'Sg', 'σῴζω',         'He/she was saved'],
            ['9',  'ἠγέρθη',      'Aor', 'Pass', '3rd', 'Sg', 'ἐγείρω',       'He/she was raised'],
            ['10', 'ἐγράφη',      'Aor', 'Pass', '3rd', 'Sg', 'γράφω',        'It was written (η variant)'],
            ['11', 'ἐστράφη',     'Aor', 'Pass', '3rd', 'Sg', 'στρέφω',       'He was turned (η variant)'],
            ['12', 'ἐβλήθη',      'Aor', 'Pass', '3rd', 'Sg', 'βάλλω',        'He/it was thrown'],
            ['13', 'ἀπεκρίθη',    'Aor', 'Pass', '3rd', 'Sg', 'ἀποκρίνομαι',  'He answered (deponent)'],
            ['14', 'ἐπορεύθη',    'Aor', 'Pass', '3rd', 'Sg', 'πορεύομαι',    'He went (deponent)'],
            ['15', 'λυθήσομαι',   'Fut', 'Pass', '1st', 'Sg', 'λύω',          'I will be loosed'],
            ['16', 'λυθήσεται',   'Fut', 'Pass', '3rd', 'Sg', 'λύω',          'He/she will be loosed'],
            ['17', 'σωθήσεται',   'Fut', 'Pass', '3rd', 'Sg', 'σῴζω',         'He/she will be saved'],
            ['18', 'ἐγερθήσεται', 'Fut', 'Pass', '3rd', 'Sg', 'ἐγείρω',       'He/she will be raised'],
            ['19', 'ἔλυσεν',      'Aor', 'Act',  '3rd', 'Sg', 'λύω',          'DISTRACTOR — 1st aorist active'],
            ['20', 'ἐλύσατο',     'Aor', 'Mid',  '3rd', 'Sg', 'λύω',          'DISTRACTOR — 1st aorist middle'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Parsing Table', use_greek=True)


def build_bbg_ch24_aorist_future_passive_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh24AoristFuturePassiveParsingPDF,
        'BBG Chapter 24 — Aorist and Future Passive Parsing Drill',
        'Theta Tense Formant and Passive Personal Endings',
        ['greek', 'bbg', 'ch24', 'exercises', 'ch24-aorist-future-passive-parsing'],
        'ch24-aorist-future-passive-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch25 — Perfect Indicative Parsing Drill
# ---------------------------------------------------------------------------

class BbgCh25PerfectParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Provide: Tense · Voice · Person · Number · Reduplication type · Lexical Form · Translation. '
            'Items 19–20 are aorist distractors — identify them correctly!'
        )
        hdrs = ['#', 'Form', 'Tense', 'Voice', 'Person', 'Number', 'Redup.', 'Lexical Form', 'Translation']
        cr = [0.04, 0.14, 0.09, 0.09, 0.07, 0.07, 0.11, 0.13, 0.26]
        gk = [1]
        rows = [
            ['1',  'λέλυκα',     '', '', '', '', '', '', ''], ['2',  'λέλυκας',    '', '', '', '', '', '', ''],
            ['3',  'λέλυκεν',    '', '', '', '', '', '', ''], ['4',  'λελύκαμεν',  '', '', '', '', '', '', ''],
            ['5',  'λελύκατε',   '', '', '', '', '', '', ''], ['6',  'λελύκασιν',  '', '', '', '', '', '', ''],
            ['7',  'πεπίστευκα', '', '', '', '', '', '', ''], ['8',  'πεποίηκεν',  '', '', '', '', '', '', ''],
            ['9',  'ἀκήκοεν',    '', '', '', '', '', '', ''], ['10', 'γέγραφεν',   '', '', '', '', '', '', ''],
            ['11', 'γέγονεν',    '', '', '', '', '', '', ''], ['12', 'ἐγήγερται',  '', '', '', '', '', '', ''],
            ['13', 'γέγραπται',  '', '', '', '', '', '', ''], ['14', 'τετέλεσται', '', '', '', '', '', '', ''],
            ['15', 'λέλυμαι',    '', '', '', '', '', '', ''], ['16', 'λέλυται',    '', '', '', '', '', '', ''],
            ['17', 'λελύμεθα',   '', '', '', '', '', '', ''], ['18', 'λέλυνται',   '', '', '', '', '', '', ''],
            ['19', 'ἔλυσεν',     '', '', '', '', '', '', ''], ['20', 'ἔγραψεν',    '', '', '', '', '', '', ''],
        ]
        ans = [
            ['1',  'λέλυκα',    'Perf', 'Act',      '1st', 'Sg', 'λ+ε (cons.)',   'λύω',     'I have loosed'],
            ['2',  'λέλυκας',   'Perf', 'Act',      '2nd', 'Sg', 'λ+ε (cons.)',   'λύω',     'You have loosed'],
            ['3',  'λέλυκεν',   'Perf', 'Act',      '3rd', 'Sg', 'λ+ε (cons.)',   'λύω',     'He/she has loosed'],
            ['4',  'λελύκαμεν', 'Perf', 'Act',      '1st', 'Pl', 'λ+ε (cons.)',   'λύω',     'We have loosed'],
            ['5',  'λελύκατε',  'Perf', 'Act',      '2nd', 'Pl', 'λ+ε (cons.)',   'λύω',     'You (pl) have loosed'],
            ['6',  'λελύκασιν', 'Perf', 'Act',      '3rd', 'Pl', 'λ+ε (cons.)',   'λύω',     'They have loosed'],
            ['7',  'πεπίστευκα','Perf', 'Act',      '1st', 'Sg', 'π+ε (cons.)',   'πιστεύω', 'I have believed'],
            ['8',  'πεποίηκεν', 'Perf', 'Act',      '3rd', 'Sg', 'π+ε (cons.)',   'ποιέω',   'He/she has done/made'],
            ['9',  'ἀκήκοεν',   'Perf', 'Act',      '3rd', 'Sg', 'ἀκ+η (vowel)', 'ἀκούω',   'He/she has heard'],
            ['10', 'γέγραφεν',  'Perf', 'Act',      '3rd', 'Sg', 'γ+ε (2nd pf)', 'γράφω',   'He/she has written'],
            ['11', 'γέγονεν',   'Perf', 'Act',      '3rd', 'Sg', 'γ+ε (2nd pf)', 'γίνομαι', 'It has become'],
            ['12', 'ἐγήγερται', 'Perf', 'Mid/Pass', '3rd', 'Sg', 'ε+γ (cluster)','ἐγείρω',  'He/she has been raised'],
            ['13', 'γέγραπται', 'Perf', 'Mid/Pass', '3rd', 'Sg', 'γ+ε (cons.)',  'γράφω',   'It has been written'],
            ['14', 'τετέλεσται','Perf', 'Mid/Pass', '3rd', 'Sg', 'τ+ε (cons.)',  'τελέω',   'It is finished / completed'],
            ['15', 'λέλυμαι',   'Perf', 'Mid/Pass', '1st', 'Sg', 'λ+ε (cons.)',  'λύω',     'I have been loosed'],
            ['16', 'λέλυται',   'Perf', 'Mid/Pass', '3rd', 'Sg', 'λ+ε (cons.)',  'λύω',     'He/she has been loosed'],
            ['17', 'λελύμεθα',  'Perf', 'Mid/Pass', '1st', 'Pl', 'λ+ε (cons.)',  'λύω',     'We have been loosed'],
            ['18', 'λέλυνται',  'Perf', 'Mid/Pass', '3rd', 'Pl', 'λ+ε (cons.)',  'λύω',     'They have been loosed'],
            ['19', 'ἔλυσεν',    'Aor',  'Act',      '3rd', 'Sg', 'ε- (augment)', 'λύω',     'DISTRACTOR — aorist, not perfect'],
            ['20', 'ἔγραψεν',   'Aor',  'Act',      '3rd', 'Sg', 'ε- (augment)', 'γράφω',   'DISTRACTOR — aorist, not perfect'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Parsing Table', use_greek=True)


def build_bbg_ch25_perfect_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh25PerfectParsingPDF,
        'BBG Chapter 25 — Perfect Indicative Parsing Drill',
        'Reduplication · Kappa Tense Formant · Perfect Active and Passive',
        ['greek', 'bbg', 'ch25', 'exercises', 'ch25-perfect-parsing'],
        'ch25-perfect-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch27 — Present Participle Parsing Drill
# ---------------------------------------------------------------------------

class BbgCh27PresentParticipleParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Parse the bolded participle (Tense · Voice · Case · Number · Gender · Lexical Form). '
            'Then identify the Use (Adverbial / Adjectival / Substantival) and provide a Translation.'
        )
        hdrs = ['#', 'Form', 'Tense', 'Voice', 'Case', 'Number', 'Gender', 'Lexical', 'Use', 'Translation']
        cr = [0.03, 0.14, 0.07, 0.07, 0.07, 0.07, 0.07, 0.11, 0.10, 0.27]
        gk = [1]
        rows = [
            ['1',  'λύων',          '', '', '', '', '', '', '', ''],
            ['2',  'ἀκούων',        '', '', '', '', '', '', '', ''],
            ['3',  'πορευόμενοι',   '', '', '', '', '', '', '', ''],
            ['4',  'προσευχόμενος', '', '', '', '', '', '', '', ''],
            ['5',  'ἀγαπῶν',        '', '', '', '', '', '', '', ''],
            ['6',  'βλέπων',        '', '', '', '', '', '', '', ''],
            ['7',  'ἐρχόμενος',     '', '', '', '', '', '', '', ''],
            ['8',  'λεγόμενος',     '', '', '', '', '', '', '', ''],
            ['9',  'λαλοῦντος',     '', '', '', '', '', '', '', ''],
            ['10', 'πιστεύων',      '', '', '', '', '', '', '', ''],
            ['11', 'ἐρχομένους',    '', '', '', '', '', '', '', ''],
            ['12', 'λεγομένῳ',      '', '', '', '', '', '', '', ''],
            ['13', 'πιστεύων',      '', '', '', '', '', '', '', ''],
            ['14', 'ἀγαπῶντες',     '', '', '', '', '', '', '', ''],
            ['15', 'ὤν',            '', '', '', '', '', '', '', ''],
        ]
        ans = [
            ['1',  'λύων',          'Pres', 'Act',      'Nom', 'Sg', 'Masc', 'λύω',         'Adverbial',   'While loosing the slaves, he said to them.'],
            ['2',  'ἀκούων',        'Pres', 'Act',      'Nom', 'Sg', 'Masc', 'ἀκούω',       'Adverbial',   'But Jesus, hearing [this], answered them.'],
            ['3',  'πορευόμενοι',   'Pres', 'Mid',      'Nom', 'Pl', 'Masc', 'πορεύομαι',   'Adverbial',   'As you go, preach saying the kingdom is near.'],
            ['4',  'προσευχόμενος', 'Pres', 'Mid',      'Nom', 'Sg', 'Masc', 'προσεύχομαι', 'Adverbial',   'When praying, do not babble.'],
            ['5',  'ἀγαπῶν',        'Pres', 'Act',      'Nom', 'Sg', 'Masc', 'ἀγαπάω',      'Adverbial',   'The one who loves God can do all things.'],
            ['6',  'βλέπων',        'Pres', 'Act',      'Nom', 'Sg', 'Masc', 'βλέπω',       'Adverbial',   'Seeing the crowds, he was moved with compassion.'],
            ['7',  'ἐρχόμενος',     'Pres', 'Mid',      'Nom', 'Sg', 'Masc', 'ἔρχομαι',     'Adverbial',   'Peter, coming to him, said:'],
            ['8',  'λεγόμενος',     'Pres', 'Mid/Pass', 'Nom', 'Sg', 'Masc', 'λέγω',        'Adjectival',  'The one called Christ — he is the Son of God.'],
            ['9',  'λαλοῦντος',     'Pres', 'Act',      'Gen', 'Sg', 'Masc', 'λαλέω',       'Adv — Gen. Abs.', 'While he was saying these things, many believed.'],
            ['10', 'πιστεύων',      'Pres', 'Act',      'Nom', 'Sg', 'Masc', 'πιστεύω',     'Adjectival',  'The believing man is being saved.'],
            ['11', 'ἐρχομένους',    'Pres', 'Mid',      'Acc', 'Pl', 'Masc', 'ἔρχομαι',     'Adjectival',  'He saw the brothers, the ones coming to him.'],
            ['12', 'λεγομένῳ',      'Pres', 'Mid/Pass', 'Dat', 'Sg', 'Masc', 'λέγω',        'Adjectival',  'In the house called Bethesda.'],
            ['13', 'πιστεύων',      'Pres', 'Act',      'Nom', 'Sg', 'Masc', 'πιστεύω',     'Substantival', 'The one who believes in him is not judged.'],
            ['14', 'ἀγαπῶντες',     'Pres', 'Act',      'Nom', 'Pl', 'Masc', 'ἀγαπάω',      'Substantival', 'Blessed are those who love the Lord.'],
            ['15', 'ὤν',            'Pres', 'Act',      'Nom', 'Sg', 'Masc', 'εἰμί',        'Substantival', 'The one in the bosom of the Father has explained him.'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Parsing Table', use_greek=True)


def build_bbg_ch27_present_participle_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh27PresentParticipleParsingPDF,
        'BBG Chapter 27 — Present Participle Parsing Drill',
        'Imperfective (Present) Adverbial · Adjectival · Substantival Participles',
        ['greek', 'bbg', 'ch27', 'exercises', 'ch27-present-participle-parsing'],
        'ch27-present-participle-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch28 — Aorist Participle Parsing Drill
# ---------------------------------------------------------------------------

class BbgCh28AoristParticipleParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Parse the bolded participle (Tense · Voice · Case · Number · Gender · Lexical Form). '
            'Identify 1st or 2nd Aorist, the Use (Adverbial / Adjectival / Substantival), and provide a Translation.'
        )
        hdrs = ['#', 'Form', 'Tense', 'Voice', 'Case', 'Number', 'Gender', 'Lexical', '1st/2nd', 'Use', 'Translation']
        cr = [0.03, 0.13, 0.06, 0.06, 0.06, 0.06, 0.06, 0.11, 0.07, 0.09, 0.27]
        gk = [1]
        rows = [
            ['1',  'λύσας',          '', '', '', '', '', '', '', '', ''],
            ['2',  'ἀκούσας',        '', '', '', '', '', '', '', '', ''],
            ['3',  'πιστεύσαντες',   '', '', '', '', '', '', '', '', ''],
            ['4',  'προσκαλεσάμενος','', '', '', '', '', '', '', '', ''],
            ['5',  'ἐλθών',          '', '', '', '', '', '', '', '', ''],
            ['6',  'λαβών',          '', '', '', '', '', '', '', '', ''],
            ['7',  'ἰδών',           '', '', '', '', '', '', '', '', ''],
            ['8',  'ἀποκριθείς',     '', '', '', '', '', '', '', '', ''],
            ['9',  'βαπτισθείς',     '', '', '', '', '', '', '', '', ''],
            ['10', 'πιστεύσασιν',    '', '', '', '', '', '', '', '', ''],
            ['11', 'σπαρείς',        '', '', '', '', '', '', '', '', ''],
            ['12', 'ἐλθόντα',        '', '', '', '', '', '', '', '', ''],
            ['13', 'πιστεύσαντες',   '', '', '', '', '', '', '', '', ''],
            ['14', 'βαπτισθεῖσιν',   '', '', '', '', '', '', '', '', ''],
            ['15', 'λαβόντες',       '', '', '', '', '', '', '', '', ''],
        ]
        ans = [
            ['1',  'λύσας',          'Aor', 'Act',  'Nom', 'Sg', 'Masc', 'λύω',           '1st', 'Adverbial',   'After loosing the slaves, he entered the house.'],
            ['2',  'ἀκούσας',        'Aor', 'Act',  'Nom', 'Sg', 'Masc', 'ἀκούω',         '1st', 'Adverbial',   'But the king, having heard, was troubled.'],
            ['3',  'πιστεύσαντες',   'Aor', 'Act',  'Nom', 'Pl', 'Masc', 'πιστεύω',       '1st', 'Adverbial',   'Having believed in the Lord, they were baptized.'],
            ['4',  'προσκαλεσάμενος','Aor', 'Mid',  'Nom', 'Sg', 'Masc', 'προσκαλέομαι',  '1st', 'Adverbial',   'Having summoned his disciples, he said to them:'],
            ['5',  'ἐλθών',          'Aor', 'Act',  'Nom', 'Sg', 'Masc', 'ἔρχομαι',       '2nd', 'Adverbial',   'Coming to him, the centurion was appealing to him.'],
            ['6',  'λαβών',          'Aor', 'Act',  'Nom', 'Sg', 'Masc', 'λαμβάνω',       '2nd', 'Adverbial',   'Taking the five loaves, he blessed them.'],
            ['7',  'ἰδών',           'Aor', 'Act',  'Nom', 'Sg', 'Masc', 'ὁράω',          '2nd', 'Adverbial',   'But seeing the crowds, he went up the mountain.'],
            ['8',  'ἀποκριθείς',     'Aor', 'Pass', 'Nom', 'Sg', 'Masc', 'ἀποκρίνομαι',   '1st', 'Adverbial',   'And Peter, answering, said to him:'],
            ['9',  'βαπτισθείς',     'Aor', 'Pass', 'Nom', 'Sg', 'Masc', 'βαπτίζω',       '1st', 'Adverbial',   'Jesus, having been baptized, came up from the water.'],
            ['10', 'πιστεύσασιν',    'Aor', 'Act',  'Dat', 'Pl', 'Masc', 'πιστεύω',       '1st', 'Adjectival',  'He said to the disciples who had believed in him:'],
            ['11', 'σπαρείς',        'Aor', 'Pass', 'Nom', 'Sg', 'Masc', 'σπείρω',        '1st', 'Adjectival',  'The word that was sown — this is the word.'],
            ['12', 'ἐλθόντα',        'Aor', 'Act',  'Acc', 'Sg', 'Masc', 'ἔρχομαι',       '2nd', 'Adjectival',  'There he saw a man, the one who had come from Judea.'],
            ['13', 'πιστεύσαντες',   'Aor', 'Act',  'Nom', 'Pl', 'Masc', 'πιστεύω',       '1st', 'Substantival', 'Blessed are those who have believed and not seen.'],
            ['14', 'βαπτισθεῖσιν',   'Aor', 'Pass', 'Dat', 'Pl', 'Masc', 'βαπτίζω',       '1st', 'Substantival', 'Joy was given to those who had been baptized.'],
            ['15', 'λαβόντες',       'Aor', 'Act',  'Nom', 'Pl', 'Masc', 'λαμβάνω',       '2nd', 'Substantival', 'All those who had taken the authority rejoiced.'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Parsing Table', use_greek=True)


def build_bbg_ch28_aorist_participle_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh28AoristParticipleParsingPDF,
        'BBG Chapter 28 — Aorist Participle Parsing Drill',
        'Perfective (Aorist) Adverbial · Adjectival · Substantival Participles',
        ['greek', 'bbg', 'ch28', 'exercises', 'ch28-aorist-participle-parsing'],
        'ch28-aorist-participle-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch29 — Adjectival Participle Parsing Drill
# ---------------------------------------------------------------------------

class BbgCh29AdjectivalParticipleParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Parse the underlined participle (Tense · Voice · Case · Number · Gender · Lexical Form). '
            'Identify the Use (Attributive / Substantival). If attributive, note the Position (1st or 2nd). '
            'Provide a Translation.'
        )
        hdrs = ['#', 'Form', 'Tense', 'Voice', 'Case', 'Number', 'Gender', 'Lexical', 'Use', 'Notes', 'Translation']
        cr = [0.03, 0.13, 0.06, 0.06, 0.06, 0.06, 0.06, 0.11, 0.09, 0.09, 0.25]
        gk = [1]
        rows = [
            ['1',  'πιστεύων',    '', '', '', '', '', '', '', '', ''],
            ['2',  'ἀγαπῶντας',   '', '', '', '', '', '', '', '', ''],
            ['3',  'κλαίουσαν',   '', '', '', '', '', '', '', '', ''],
            ['4',  'ἐρχομένῳ',    '', '', '', '', '', '', '', '', ''],
            ['5',  'πιστεύσαντος','', '', '', '', '', '', '', '', ''],
            ['6',  'λύων',        '', '', '', '', '', '', '', '', ''],
            ['7',  'κεκλημένῳ',   '', '', '', '', '', '', '', '', ''],
            ['8',  'γεγραμμένοις','', '', '', '', '', '', '', '', ''],
            ['9',  'πιστεύων',    '', '', '', '', '', '', '', '', ''],
            ['10', 'κλαίοντες',   '', '', '', '', '', '', '', '', ''],
            ['11', 'νικῶν',       '', '', '', '', '', '', '', '', ''],
            ['12', 'ἀγαπῶντες',   '', '', '', '', '', '', '', '', ''],
            ['13', 'πιστεύουσιν', '', '', '', '', '', '', '', '', ''],
            ['14', 'ἐρχόμενον',   '', '', '', '', '', '', '', '', ''],
            ['15', 'σῳζομένοις',  '', '', '', '', '', '', '', '', ''],
        ]
        ans = [
            ['1',  'πιστεύων',    'Pres', 'Act',      'Nom', 'Sg', 'Masc', 'πιστεύω', 'Attributive', '1st pos.', 'The believing man is being saved.'],
            ['2',  'ἀγαπῶντας',   'Pres', 'Act',      'Acc', 'Pl', 'Masc', 'ἀγαπάω',  'Attributive', '1st pos.', 'Let us love the brothers who love us.'],
            ['3',  'κλαίουσαν',   'Pres', 'Act',      'Acc', 'Sg', 'Fem',  'κλαίω',   'Attributive', '1st pos.', 'He saw the weeping woman.'],
            ['4',  'ἐρχομένῳ',    'Pres', 'Mid',      'Dat', 'Sg', 'Masc', 'ἔρχομαι', 'Attributive', '1st pos.', 'In the coming age.'],
            ['5',  'πιστεύσαντος','Aor',  'Act',      'Gen', 'Sg', 'Masc', 'πιστεύω', 'Attributive', '1st pos.', 'He spoke about the crowd that had believed.'],
            ['6',  'λύων',        'Pres', 'Act',      'Nom', 'Sg', 'Masc', 'λύω',     'Attributive', '2nd pos.', 'The man who is loosing the slaves.'],
            ['7',  'κεκλημένῳ',   'Perf', 'Pass',     'Dat', 'Sg', 'Neut', 'καλέω',   'Attributive', '2nd pos.', 'To the child called Jesus.'],
            ['8',  'γεγραμμένοις','Perf', 'Pass',     'Dat', 'Pl', 'Masc', 'γράφω',   'Attributive', '2nd pos.', 'They believed the words that were written.'],
            ['9',  'πιστεύων',    'Pres', 'Act',      'Nom', 'Sg', 'Masc', 'πιστεύω', 'Substantival', '—', 'The one who believes in him is not judged.'],
            ['10', 'κλαίοντες',   'Pres', 'Act',      'Nom', 'Pl', 'Masc', 'κλαίω',   'Substantival', '—', 'Blessed are the poor — also blessed are those who weep.'],
            ['11', 'νικῶν',       'Pres', 'Act',      'Nom', 'Sg', 'Masc', 'νικάω',   'Substantival', '—', 'The one who conquers will inherit these things.'],
            ['12', 'ἀγαπῶντες',   'Pres', 'Act',      'Nom', 'Pl', 'Masc', 'ἀγαπάω',  'Substantival', '—', 'For those who love God all things work for good.'],
            ['13', 'πιστεύουσιν', 'Pres', 'Act',      'Dat', 'Pl', 'Masc', 'πιστεύω', 'Substantival', '—', 'He says to those who believe in him.'],
            ['14', 'ἐρχόμενον',   'Pres', 'Mid',      'Acc', 'Sg', 'Masc', 'ἔρχομαι', 'Substantival', '—', 'He saw the one coming to him.'],
            ['15', 'σῳζομένοις',  'Pres', 'Mid/Pass', 'Dat', 'Pl', 'Masc', 'σῴζω',    'Substantival', '—', 'I send this one to those who are being saved.'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Parsing Table', use_greek=True)


def build_bbg_ch29_adjectival_participle_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh29AdjectivalParticipleParsingPDF,
        'BBG Chapter 29 — Adjectival Participle Parsing Drill',
        'Attributive (1st & 2nd Position) and Substantival Participle Uses',
        ['greek', 'bbg', 'ch29', 'exercises', 'ch29-adjectival-participle-parsing'],
        'ch29-adjectival-participle-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch30 — Perfect Participles and Genitive Absolutes
# ---------------------------------------------------------------------------

class BbgCh30PerfectParticipleGenAbsPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Part A (1–8): Parse the perfect participle (Tense · Voice · Case · Number · Gender · Lexical) '
            'and translate. Part B (9–15): Identify the genitive absolute noun and participle, parse the '
            'participle, and translate the full sentence.'
        )
        # Part A
        hdrs_a = ['#', 'Form', 'Tense', 'Voice', 'Case', 'Number', 'Gender', 'Lexical', 'Translation']
        cr_a = [0.03, 0.14, 0.07, 0.09, 0.07, 0.07, 0.07, 0.12, 0.34]
        gk_a = [1]
        rows_a = [
            ['1', 'λελυκώς',     '', '', '', '', '', '', ''],
            ['2', 'πεπιστευκότας','', '', '', '', '', '', ''],
            ['3', 'γεγραφυῖα',   '', '', '', '', '', '', ''],
            ['4', 'τεθνηκώς',    '', '', '', '', '', '', ''],
            ['5', 'γεγραμμένος', '', '', '', '', '', '', ''],
            ['6', 'λελυμένον',   '', '', '', '', '', '', ''],
            ['7', 'πεπιστευμένοις','','', '', '', '', '', ''],
            ['8', 'γεγραμμέναι', '', '', '', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'λελυκώς',      'Perf', 'Active',    'Nom', 'Sg', 'Masc', 'λύω',     'The one who has loosed the slaves departed.'],
            ['2', 'πεπιστευκότας','Perf', 'Active',    'Acc', 'Pl', 'Masc', 'πιστεύω', 'He saw those who had believed in God.'],
            ['3', 'γεγραφυῖα',    'Perf', 'Active',    'Nom', 'Sg', 'Fem',  'γράφω',   'The woman who had written in the book.'],
            ['4', 'τεθνηκώς',     'Perf', 'Active',    'Nom', 'Sg', 'Masc', 'θνῄσκω',  'The man who had died — this was said.'],
            ['5', 'γεγραμμένος',  'Perf', 'Mid/Pass',  'Nom', 'Sg', 'Masc', 'γράφω',   'The word that was written in the book.'],
            ['6', 'λελυμένον',    'Perf', 'Mid/Pass',  'Acc', 'Sg', 'Masc', 'λύω',     'They saw the man who had been loosed.'],
            ['7', 'πεπιστευμένοις','Perf','Mid/Pass',  'Dat', 'Pl', 'Masc', 'πιστεύω', 'To those who have been entrusted with the truth.'],
            ['8', 'γεγραμμέναι',  'Perf', 'Mid/Pass',  'Nom', 'Pl', 'Fem',  'γράφω',   'The commandments that were written.'],
        ]
        # Part B
        hdrs_b = ['#', 'Gen. Noun', 'Gen. Ptc.', 'Ptc Tense', 'Voice', 'Case', 'Num', 'Lexical', 'Translation']
        cr_b = [0.03, 0.11, 0.13, 0.08, 0.07, 0.05, 0.05, 0.13, 0.35]
        gk_b = [1, 2]
        rows_b = [
            ['9',  'αὐτοῦ', 'λαλοῦντος',    '', '', '', '', '', ''],
            ['10', 'αὐτοῦ', 'ἐκπορευομένου','', '', '', '', '', ''],
            ['11', 'αὐτοῦ', 'καθημένου',    '', '', '', '', '', ''],
            ['12', 'αὐτοῦ', 'λέγοντος',     '', '', '', '', '', ''],
            ['13', 'αὐτοῦ', 'ἀπελθόντος',   '', '', '', '', '', ''],
            ['14', 'Ἡρῴδου','τεθνηκότος',   '', '', '', '', '', ''],
            ['15', 'αὐτοῦ', 'ὄντος',        '', '', '', '', '', ''],
        ]
        ans_b = [
            ['9',  'αὐτοῦ', 'λαλοῦντος',    'Pres', 'Act', 'Gen', 'Sg', 'λαλέω',        'While he was speaking to the crowds, his mother was outside.'],
            ['10', 'αὐτοῦ', 'ἐκπορευομένου','Pres', 'Mid', 'Gen', 'Sg', 'ἐκπορεύομαι',  'As he was going out of the temple, the disciples said to him.'],
            ['11', 'αὐτοῦ', 'καθημένου',    'Pres', 'Mid', 'Gen', 'Sg', 'κάθημαι',      'While he was sitting on the mountain, the disciples came to him.'],
            ['12', 'αὐτοῦ', 'λέγοντος',     'Pres', 'Act', 'Gen', 'Sg', 'λέγω',         'While he was saying these things, many believed in him.'],
            ['13', 'αὐτοῦ', 'ἀπελθόντος',   'Aor',  'Act', 'Gen', 'Sg', 'ἀπέρχομαι',    'After he had departed into the wilderness, the people came.'],
            ['14', 'Ἡρῴδου','τεθνηκότος',   'Perf', 'Act', 'Gen', 'Sg', 'θνῄσκω',       'After Herod had died, an angel appeared in a dream to Joseph.'],
            ['15', 'αὐτοῦ', 'ὄντος',        'Pres', 'Act', 'Gen', 'Sg', 'εἰμί',         'While he was in Bethlehem, Magi came from the east.'],
        ]
        self.add_multi_part_drill([
            {'title': 'Part A — Perfect Participles',  'headers': hdrs_a, 'rows': rows_a, 'answers': ans_a, 'col_ratios': cr_a, 'greek_cols': gk_a},
            {'title': 'Part B — Genitive Absolutes',   'headers': hdrs_b, 'rows': rows_b, 'answers': ans_b, 'col_ratios': cr_b, 'greek_cols': gk_b},
        ], use_greek=True)


def build_bbg_ch30_perfect_participle_genabs(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh30PerfectParticipleGenAbsPDF,
        'BBG Chapter 30 — Perfect Participles and Genitive Absolutes',
        'Combinative (Perfect) Participles · Genitive Absolute Construction',
        ['greek', 'bbg', 'ch30', 'exercises', 'ch30-perfect-participle-genabs'],
        'ch30-perfect-participle-genabs.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch31 — Subjunctive Parsing Drill
# ---------------------------------------------------------------------------

class BbgCh31SubjunctiveParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Parse the underlined form (Tense · Voice · Person · Number · Mood · Lexical Form). '
            'Identify the Use (Purpose/ἵνα · 3rd class/ἐάν · Hortatory · Prohibition · Indefinite · Emphatic denial). '
            'Provide a Translation.'
        )
        hdrs = ['#', 'Form', 'Tense', 'Voice', 'Person', 'Number', 'Mood', 'Lexical', 'Use', 'Translation']
        cr = [0.03, 0.14, 0.06, 0.06, 0.06, 0.06, 0.06, 0.11, 0.11, 0.31]
        gk = [1]
        rows = [
            ['1',  'σώσῃ',         '', '', '', '', '', '', '', ''],
            ['2',  'παρακαλέσῃ',   '', '', '', '', '', '', '', ''],
            ['3',  'πιστεύητε',    '', '', '', '', '', '', '', ''],
            ['4',  'κρίνω',        '', '', '', '', '', '', '', ''],
            ['5',  'ἀποκτείνωσιν', '', '', '', '', '', '', '', ''],
            ['6',  'πληρωθῇ',      '', '', '', '', '', '', '', ''],
            ['7',  'ὁμολογῶμεν',   '', '', '', '', '', '', '', ''],
            ['8',  'εἴπωμεν',      '', '', '', '', '', '', '', ''],
            ['9',  'ἁμάρτῃ',       '', '', '', '', '', '', '', ''],
            ['10', 'πιστεύσῃς',    '', '', '', '', '', '', '', ''],
            ['11', 'ἀγαπῶμεν',     '', '', '', '', '', '', '', ''],
            ['12', 'προσέλθωμεν',  '', '', '', '', '', '', '', ''],
            ['13', 'χαίρωμεν',     '', '', '', '', '', '', '', ''],
            ['14', 'νομίσητε',     '', '', '', '', '', '', '', ''],
            ['15', 'φοβηθῇς',      '', '', '', '', '', '', '', ''],
            ['16', 'κρίνητε',      '', '', '', '', '', '', '', ''],
            ['17', 'θέλῃ',         '', '', '', '', '', '', '', ''],
            ['18', 'ἔλθῃ',         '', '', '', '', '', '', '', ''],
            ['19', 'εἰσέλθητε',    '', '', '', '', '', '', '', ''],
            ['20', 'παρέλθῃ',      '', '', '', '', '', '', '', ''],
        ]
        ans = [
            ['1',  'σώσῃ',        'Aor', 'Act',  '3rd', 'Sg', 'Subj', 'σῴζω',        'Purpose (ἵνα)',         'He came in order to save the world.'],
            ['2',  'παρακαλέσῃ',  'Aor', 'Act',  '3rd', 'Sg', 'Subj', 'παρακαλέω',   'Purpose (ἵνα)',         'I will send him to you so that he might encourage you.'],
            ['3',  'πιστεύητε',   'Pres', 'Act',  '2nd', 'Pl', 'Subj', 'πιστεύω',    'Purpose (ἵνα)',         'These things were written so that you may believe Jesus is the Christ.'],
            ['4',  'κρίνω',       'Pres', 'Act',  '1st', 'Sg', 'Subj', 'κρίνω',      'Purpose (ἵνα)',         'I did not come in order to judge the world.'],
            ['5',  'ἀποκτείνωσιν','Aor', 'Act',  '3rd', 'Pl', 'Subj', 'ἀποκτείνω',  'Purpose (ἵνα) — neg.', 'It was given to them so that they might not kill them.'],
            ['6',  'πληρωθῇ',     'Aor', 'Pass', '3rd', 'Sg', 'Subj', 'πληρόω',      'Purpose (ἵνα)',         'I say this so that your joy may be filled.'],
            ['7',  'ὁμολογῶμεν',  'Pres', 'Act', '1st', 'Pl', 'Subj', 'ὁμολογέω',   '3rd class (ἐάν)',      'If we confess our sins, he is faithful.'],
            ['8',  'εἴπωμεν',     'Aor', 'Act',  '1st', 'Pl', 'Subj', 'λέγω',        '3rd class (ἐάν)',      'If we say that we have no sin, we deceive ourselves.'],
            ['9',  'ἁμάρτῃ',      'Aor', 'Act',  '3rd', 'Sg', 'Subj', 'ἁμαρτάνω',   '3rd class (ἐάν)',      'If anyone should sin, we have an advocate with the Father.'],
            ['10', 'πιστεύσῃς',   'Aor', 'Act',  '2nd', 'Sg', 'Subj', 'πιστεύω',    '3rd class (ἐάν)',      'If you believe, you will see the glory of God.'],
            ['11', 'ἀγαπῶμεν',    'Pres', 'Act', '1st', 'Pl', 'Subj', 'ἀγαπάω',     'Hortatory',            'Let us love one another, for love is from God.'],
            ['12', 'προσέλθωμεν', 'Aor', 'Act',  '1st', 'Pl', 'Subj', 'προσέρχομαι','Hortatory',            'Let us approach the throne of grace with boldness.'],
            ['13', 'χαίρωμεν',    'Pres', 'Act', '1st', 'Pl', 'Subj', 'χαίρω',      'Hortatory',            'Let us rejoice and exult and give glory to him.'],
            ['14', 'νομίσητε',    'Aor', 'Act',  '2nd', 'Pl', 'Subj', 'νομίζω',     'Prohibition (μή+aor)', 'Do not think that I came to abolish the Law.'],
            ['15', 'φοβηθῇς',     'Aor', 'Pass', '2nd', 'Sg', 'Subj', 'φοβέομαι',   'Prohibition (μή+aor)', 'Do not be afraid, Mary; you have found favor with God.'],
            ['16', 'κρίνητε',     'Pres', 'Act', '2nd', 'Pl', 'Subj', 'κρίνω',      'Prohibition (μή+pres)','Do not judge, so that you may not be judged.'],
            ['17', 'θέλῃ',        'Pres', 'Act', '3rd', 'Sg', 'Subj', 'θέλω',       'Indefinite (ὃς ἄν)',   'Whoever wishes to be great among you shall be your servant.'],
            ['18', 'ἔλθῃ',        'Aor', 'Act',  '3rd', 'Sg', 'Subj', 'ἔρχομαι',    'Indefinite (ὅταν)',     'When the Son of Man comes, will he find faith on the earth?'],
            ['19', 'εἰσέλθητε',   'Aor', 'Act',  '2nd', 'Pl', 'Subj', 'εἰσέρχομαι', 'Emphatic denial (οὐ μή)','You will certainly not enter the kingdom of heaven.'],
            ['20', 'παρέλθῃ',     'Aor', 'Act',  '3rd', 'Sg', 'Subj', 'παρέρχομαι', 'Emphatic denial (οὐ μή)','This generation will absolutely not pass away.'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Parsing Table', use_greek=True)


def build_bbg_ch31_subjunctive_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh31SubjunctiveParsingPDF,
        'BBG Chapter 31 — Subjunctive Parsing Drill',
        'Purpose · Conditional · Hortatory · Prohibition · Indefinite · Emphatic Denial',
        ['greek', 'bbg', 'ch31', 'exercises', 'ch31-subjunctive-parsing'],
        'ch31-subjunctive-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch32 — Infinitive Parsing Drill
# ---------------------------------------------------------------------------

class BbgCh32InfinitiveParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Parse the bolded infinitive (Tense · Voice · Lexical Form). '
            'Identify the Use (Complementary · Articular/subject · Purpose · Result · Indirect discourse · Temporal). '
            'Provide a Translation.'
        )
        hdrs = ['#', 'Form', 'Tense', 'Voice', 'Lexical', 'Use', 'Translation']
        cr = [0.03, 0.15, 0.07, 0.07, 0.14, 0.18, 0.36]
        gk = [1]
        rows = [
            ['1',  'λύειν',        '', '', '', '', ''],
            ['2',  'λῦσαι',        '', '', '', '', ''],
            ['3',  'διδάσκειν',    '', '', '', '', ''],
            ['4',  'ποιεῖν',       '', '', '', '', ''],
            ['5',  'ζητεῖν',       '', '', '', '', ''],
            ['6',  'ζῆν',          '', '', '', '', ''],
            ['7',  'σπεῖραι',      '', '', '', '', ''],
            ['8',  'εἶναι',        '', '', '', '', ''],
            ['9',  'σπεῖραι',      '', '', '', '', ''],
            ['10', 'θεαθῆναι',     '', '', '', '', ''],
            ['11', 'βαπτισθῆναι',  '', '', '', '', ''],
            ['12', 'γνῶναι',       '', '', '', '', ''],
            ['13', 'θαυμάζειν',    '', '', '', '', ''],
            ['14', 'εἰσελθεῖν',    '', '', '', '', ''],
            ['15', 'καλύπτεσθαι',  '', '', '', '', ''],
            ['16', 'εἶναι',        '', '', '', '', ''],
            ['17', 'ἐγηγέρθαι',    '', '', '', '', ''],
            ['18', 'ἀποθανεῖν',    '', '', '', '', ''],
            ['19', 'σπείρειν',     '', '', '', '', ''],
            ['20', 'κατεβαίνειν',  '', '', '', '', ''],
        ]
        ans = [
            ['1',  'λύειν',       'Pres', 'Act',  'λύω',          'Complementary',             'I want to loose the slaves.'],
            ['2',  'λῦσαι',       'Aor',  'Act',  'λύω',          'Complementary',             'I am not worthy to loose the strap of his sandal.'],
            ['3',  'διδάσκειν',   'Pres', 'Act',  'διδάσκω',      'Complementary',             'He began to teach them many things.'],
            ['4',  'ποιεῖν',      'Pres', 'Act',  'ποιέω',        'Complementary',             'Are you able to do this?'],
            ['5',  'ζητεῖν',      'Pres', 'Act',  'ζητέω',        'Complementary',             'Herod is about to seek the child to destroy him.'],
            ['6',  'ζῆν',         'Pres', 'Act',  'ζάω',          'Articular (subject)',        'For me to live is Christ and to die is gain.'],
            ['7',  'σπεῖραι',     'Aor',  'Act',  'σπείρω',       'Articular — purpose (τοῦ)', 'The sower went out to sow.'],
            ['8',  'εἶναι',       'Pres', 'Act',  'εἰμί',         'Articular — temporal (ἐν τῷ)', 'While he was in a certain place.'],
            ['9',  'σπεῖραι',     'Aor',  'Act',  'σπείρω',       'Purpose (εἰς τό)',           'He went in to sow the word.'],
            ['10', 'θεαθῆναι',    'Aor',  'Pass', 'θεάομαι',      'Purpose (πρός τό)',          'So as to be seen by them.'],
            ['11', 'βαπτισθῆναι', 'Aor',  'Pass', 'βαπτίζω',      'Purpose (εἰς τό)',           'He came to be baptized by him.'],
            ['12', 'γνῶναι',      'Aor',  'Act',  'γινώσκω',      'Purpose (τοῦ)',              'To know him and the power of his resurrection.'],
            ['13', 'θαυμάζειν',   'Pres', 'Act',  'θαυμάζω',      'Result (ὥστε)',              'So that the crowds marveled.'],
            ['14', 'εἰσελθεῖν',   'Aor',  'Act',  'εἰσέρχομαι',   'Result',                    'So that he was no longer able to enter a city.'],
            ['15', 'καλύπτεσθαι', 'Pres', 'Pass', 'καλύπτω',      'Result (ὥστε)',              'So that the boat was being covered by the waves.'],
            ['16', 'εἶναι',       'Pres', 'Act',  'εἰμί',         'Indirect discourse',         'They suppose him to be in the traveling company.'],
            ['17', 'ἐγηγέρθαι',   'Perf', 'Pass', 'ἐγείρω',       'Indirect discourse',         'They say that he has been raised from the dead.'],
            ['18', 'ἀποθανεῖν',   'Aor',  'Act',  'ἀποθνῄσκω',    'Indirect discourse',         'We believe that Jesus died and rose again.'],
            ['19', 'σπείρειν',    'Pres', 'Act',  'σπείρω',       'Temporal (ἐν τῷ)',           'While he was sowing, some seed fell along the path.'],
            ['20', 'κατεβαίνειν', 'Pres', 'Act',  'καταβαίνω',    'Temporal (ἐν τῷ)',           'As he was going down to Jericho, blind men were sitting there.'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Parsing Table', use_greek=True)


def build_bbg_ch32_infinitive_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh32InfinitiveParsingPDF,
        'BBG Chapter 32 — Infinitive Parsing Drill',
        'Complementary · Articular · Purpose · Result · Indirect Discourse · Temporal',
        ['greek', 'bbg', 'ch32', 'exercises', 'ch32-infinitive-parsing'],
        'ch32-infinitive-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch33 — Imperative Parsing Drill
# ---------------------------------------------------------------------------

class BbgCh33ImperativeParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Parse the bolded imperative (Tense · Voice · Person · Number · Lexical Form). '
            'Identify the Aspect (Ongoing / Simple / Stop). '
            'Provide a Translation.'
        )
        hdrs = ['#', 'Form', 'Tense', 'Voice', 'Person', 'Number', 'Lexical', 'Aspect', 'Translation']
        cr = [0.03, 0.14, 0.07, 0.07, 0.06, 0.06, 0.13, 0.09, 0.35]
        gk = [1]
        rows = [
            ['1',  'ἀγαπᾶτε',      '', '', '', '', '', '', ''],
            ['2',  'μετανοεῖτε',    '', '', '', '', '', '', ''],
            ['3',  'χαίρετε',       '', '', '', '', '', '', ''],
            ['4',  'πρόσεχε',       '', '', '', '', '', '', ''],
            ['5',  'αἴρετε',        '', '', '', '', '', '', ''],
            ['6',  'κλαίου',        '', '', '', '', '', '', ''],
            ['7',  'προσεύχεσθε',   '', '', '', '', '', '', ''],
            ['8',  'ἔρχου',         '', '', '', '', '', '', ''],
            ['9',  'πορεύθητε',     '', '', '', '', '', '', ''],
            ['10', 'μαθητεύσατε',   '', '', '', '', '', '', ''],
            ['11', 'ὑπόστρεψον',    '', '', '', '', '', '', ''],
            ['12', 'πίστευσον',     '', '', '', '', '', '', ''],
            ['13', 'ἐλθέ',          '', '', '', '', '', '', ''],
            ['14', 'λάβε',          '', '', '', '', '', '', ''],
            ['15', 'εἰπέ',          '', '', '', '', '', '', ''],
            ['16', 'λύθητι',        '', '', '', '', '', '', ''],
            ['17', 'φοβήθητε',      '', '', '', '', '', '', ''],
            ['18', 'ἀκουέτω',       '', '', '', '', '', '', ''],
            ['19', 'ἔστω',          '', '', '', '', '', '', ''],
            ['20', 'ἴσθι',          '', '', '', '', '', '', ''],
        ]
        ans = [
            ['1',  'ἀγαπᾶτε',    'Pres', 'Act',  '2nd', 'Pl', 'ἀγαπάω',    'Ongoing', 'Love your enemies.'],
            ['2',  'μετανοεῖτε',  'Pres', 'Act',  '2nd', 'Pl', 'μετανοέω',  'Ongoing', 'Repent and believe in the gospel.'],
            ['3',  'χαίρετε',     'Pres', 'Act',  '2nd', 'Pl', 'χαίρω',     'Ongoing', 'Rejoice in the Lord always.'],
            ['4',  'πρόσεχε',     'Pres', 'Act',  '2nd', 'Sg', 'προσέχω',   'Ongoing', 'Pay attention to yourself and to the teaching.'],
            ['5',  'αἴρετε',      'Pres', 'Act',  '2nd', 'Pl', 'αἴρω',      'Ongoing', 'Take my yoke upon you.'],
            ['6',  'κλαίου',      'Pres', 'Mid',  '2nd', 'Sg', 'κλαίω',     'Stop (ongoing prohib.)', 'Stop weeping! Behold, the Lion of Judah has conquered.'],
            ['7',  'προσεύχεσθε', 'Pres', 'Mid',  '2nd', 'Pl', 'προσεύχομαι','Ongoing', 'Pray without ceasing.'],
            ['8',  'ἔρχου',       'Pres', 'Mid',  '2nd', 'Sg', 'ἔρχομαι',   'Ongoing', 'Come and see.'],
            ['9',  'πορεύθητε',   'Aor',  'Pass', '2nd', 'Pl', 'πορεύομαι', 'Simple', 'Go therefore and make disciples of all nations.'],
            ['10', 'μαθητεύσατε', 'Aor',  'Act',  '2nd', 'Pl', 'μαθητεύω',  'Simple', 'Make disciples of all nations.'],
            ['11', 'ὑπόστρεψον',  'Aor',  'Act',  '2nd', 'Sg', 'ὑποστρέφω', 'Simple', 'Return to your house.'],
            ['12', 'πίστευσον',   'Aor',  'Act',  '2nd', 'Sg', 'πιστεύω',   'Simple', 'Believe on the Lord Jesus.'],
            ['13', 'ἐλθέ',        'Aor',  'Act',  '2nd', 'Sg', 'ἔρχομαι',   'Simple', 'Come and see.'],
            ['14', 'λάβε',        'Aor',  'Act',  '2nd', 'Sg', 'λαμβάνω',   'Simple', 'Take the child and his mother.'],
            ['15', 'εἰπέ',        'Aor',  'Act',  '2nd', 'Sg', 'λέγω',      'Simple', 'Tell me by what authority you do these things.'],
            ['16', 'λύθητι',      'Aor',  'Pass', '2nd', 'Sg', 'λύω',       'Simple', 'Be loosed from this bond.'],
            ['17', 'φοβήθητε',    'Aor',  'Pass', '2nd', 'Pl', 'φοβέομαι',  'Simple (prohib.)', 'Do not fear those who kill the body.'],
            ['18', 'ἀκουέτω',     'Pres', 'Act',  '3rd', 'Sg', 'ἀκούω',     'Ongoing', 'The one who has ears, let him hear.'],
            ['19', 'ἔστω',        'Pres', 'Act',  '3rd', 'Sg', 'εἰμί',      'Ongoing', 'But let your yes be yes.'],
            ['20', 'ἴσθι',        'Pres', 'Act',  '2nd', 'Sg', 'εἰμί',      'Ongoing', 'Be strengthened in grace.'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Parsing Table', use_greek=True)


def build_bbg_ch33_imperative_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh33ImperativeParsingPDF,
        'BBG Chapter 33 — Imperative Parsing Drill',
        'Commands and Prohibitions · Present vs. Aorist Aspect',
        ['greek', 'bbg', 'ch33', 'exercises', 'ch33-imperative-parsing'],
        'ch33-imperative-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch34 — δίδωμι Parsing Drill
# ---------------------------------------------------------------------------

class BbgCh34DidomiParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Parse the bolded form (Tense · Voice · Person · Number · Lexical Form). '
            'Provide a Translation. Watch for compound forms (παραδίδωμι, ἀποδίδωμι).'
        )
        hdrs = ['#', 'Form', 'Tense', 'Voice', 'Person', 'Number', 'Lexical', 'Translation']
        cr = [0.03, 0.15, 0.07, 0.07, 0.07, 0.07, 0.14, 0.40]
        gk = [1]
        rows = [
            ['1',  'ἔδωκεν',      '', '', '', '', '', ''],
            ['2',  'δίδωμι',      '', '', '', '', '', ''],
            ['3',  'δίδωσίν',     '', '', '', '', '', ''],
            ['4',  'δίδομεν',     '', '', '', '', '', ''],
            ['5',  'παραδίδωσιν', '', '', '', '', '', ''],
            ['6',  'ἐδίδου',      '', '', '', '', '', ''],
            ['7',  'παρεδίδου',   '', '', '', '', '', ''],
            ['8',  'ἐδίδοτε',     '', '', '', '', '', ''],
            ['9',  'ἔδωκεν',      '', '', '', '', '', ''],
            ['10', 'ἔδωκας',      '', '', '', '', '', ''],
            ['11', 'παρεδίδετο',  '', '', '', '', '', ''],
            ['12', 'παρέδωκεν',   '', '', '', '', '', ''],
            ['13', 'ἀπέδωκεν',    '', '', '', '', '', ''],
            ['14', 'ἐδόθη',       '', '', '', '', '', ''],
            ['15', 'ἐδόθησαν',    '', '', '', '', '', ''],
            ['16', 'ἐδόθη',       '', '', '', '', '', ''],
            ['17', 'παρεδόθη',    '', '', '', '', '', ''],
            ['18', 'παρεδίδετο',  '', '', '', '', '', ''],
            ['19', 'δίδοταί',     '', '', '', '', '', ''],
            ['20', 'παραδίδοται', '', '', '', '', '', ''],
        ]
        ans = [
            ['1',  'ἔδωκεν',     'Aor',  'Act',  '3rd', 'Sg', 'δίδωμι',      'God so loved the world that he gave his only Son.'],
            ['2',  'δίδωμι',     'Pres', 'Act',  '1st', 'Sg', 'δίδωμι',      'I give them eternal life.'],
            ['3',  'δίδωσίν',    'Pres', 'Act',  '3rd', 'Sg', 'δίδωμι',      'My Father gives you the bread from heaven.'],
            ['4',  'δίδομεν',    'Pres', 'Act',  '1st', 'Pl', 'δίδωμι',      'We give glory to God.'],
            ['5',  'παραδίδωσιν','Pres', 'Act',  '3rd', 'Sg', 'παραδίδωμι',  'The Son of Man is being handed over into the hands of men.'],
            ['6',  'ἐδίδου',     'Impf', 'Act',  '3rd', 'Sg', 'δίδωμι',      'He was giving them authority over unclean spirits.'],
            ['7',  'παρεδίδου',  'Impf', 'Act',  '3rd', 'Sg', 'παραδίδωμι',  'Judas was handing him over to the chief priests.'],
            ['8',  'ἐδίδοτε',    'Impf', 'Act',  '2nd', 'Pl', 'δίδωμι',      'And you were giving us bread daily.'],
            ['9',  'ἔδωκεν',     'Aor',  'Act',  '3rd', 'Sg', 'δίδωμι',      'God so loved the world that he gave his only Son.'],
            ['10', 'ἔδωκας',     'Aor',  'Act',  '2nd', 'Sg', 'δίδωμι',      'You gave him authority over all flesh.'],
            ['11', 'παρεδίδετο', 'Impf', 'Pass', '3rd', 'Sg', 'παραδίδωμι',  'On the night in which he was being betrayed, he took bread.'],
            ['12', 'παρέδωκεν',  'Aor',  'Act',  '3rd', 'Sg', 'παραδίδωμι',  'The Lord handed them over into the hands of the nations.'],
            ['13', 'ἀπέδωκεν',   'Aor',  'Act',  '3rd', 'Sg', 'ἀποδίδωμι',   'But God, whom he gave back to them.'],
            ['14', 'ἐδόθη',      'Aor',  'Pass', '3rd', 'Sg', 'δίδωμι',      'Authority to judge was given to him.'],
            ['15', 'ἐδόθησαν',   'Aor',  'Pass', '3rd', 'Pl', 'δίδωμι',      'Two wings of the great eagle were given to her.'],
            ['16', 'ἐδόθη',      'Aor',  'Pass', '3rd', 'Sg', 'δίδωμι',      'All authority in heaven and on earth was given to me.'],
            ['17', 'παρεδόθη',   'Aor',  'Pass', '3rd', 'Sg', 'παραδίδωμι',  'The word of God that was handed over to us.'],
            ['18', 'παρεδίδετο', 'Impf', 'Pass', '3rd', 'Sg', 'παραδίδωμι',  'On the night in which he was being betrayed, he took bread.'],
            ['19', 'δίδοταί',    'Pres', 'Pass', '3rd', 'Sg', 'δίδωμι',      'Everything that is given to me by my Father.'],
            ['20', 'παραδίδοται','Pres', 'Pass', '3rd', 'Sg', 'παραδίδωμι',  'What is being handed over to you? What authority do you have?'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Parsing Table', use_greek=True)


def build_bbg_ch34_didomi_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh34DidomiParsingPDF,
        'BBG Chapter 34 — δίδωμι Parsing Drill',
        'Present · Imperfect · Aorist · Passive forms of δίδωμι and compounds',
        ['greek', 'bbg', 'ch34', 'exercises', 'ch34-didomi-parsing'],
        'ch34-didomi-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch35 — Conditionals and δίδωμι Non-Indicative Drill
# ---------------------------------------------------------------------------

class BbgCh35ConditionalsdrillPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Part A (1–16): Identify the Conditional Class (1/2/3/4) and parse the protasis verb '
            '(Tense · Voice · Mood · Person · Number · Lexical Form). Provide a Translation. '
            'Part B (17–20): Parse the δίδωμι non-indicative form and translate.'
        )
        # Part A
        hdrs_a = ['#', 'Protasis Verb', 'Class', 'Tense', 'Voice', 'Mood', 'Person', 'Number', 'Lexical', 'Translation']
        cr_a = [0.03, 0.14, 0.06, 0.06, 0.06, 0.07, 0.06, 0.06, 0.11, 0.35]
        gk_a = [1]
        rows_a = [
            ['1',  'εἶ',          '', '', '', '', '', '', '', ''],
            ['2',  'ἐκβάλλω',     '', '', '', '', '', '', '', ''],
            ['3',  'ἐστίν',       '', '', '', '', '', '', '', ''],
            ['4',  'ἀγαπᾶτε',     '', '', '', '', '', '', '', ''],
            ['5',  'πιστεύετε',   '', '', '', '', '', '', '', ''],
            ['6',  'ἦτε',         '', '', '', '', '', '', '', ''],
            ['7',  'ἐγνώκειτε',   '', '', '', '', '', '', '', ''],
            ['8',  'ἦτε',         '', '', '', '', '', '', '', ''],
            ['9',  'ἦλθον',       '', '', '', '', '', '', '', ''],
            ['10', 'ἦν',          '', '', '', '', '', '', '', ''],
            ['11', 'ὁμολογῶμεν',  '', '', '', '', '', '', '', ''],
            ['12', 'εἴπωμεν',     '', '', '', '', '', '', '', ''],
            ['13', 'πιστεύσῃς',   '', '', '', '', '', '', '', ''],
            ['14', 'ἁμάρτῃ',      '', '', '', '', '', '', '', ''],
            ['15', 'πάσχοιτε',    '', '', '', '', '', '', '', ''],
            ['16', 'γένησθε',     '', '', '', '', '', '', '', ''],
        ]
        ans_a = [
            ['1',  'εἶ',         '1', 'Pres', 'Act', 'Ind', '2sg', '—',  'εἰμί',      'If you are the Son of God, tell these stones to become bread.'],
            ['2',  'ἐκβάλλω',    '1', 'Pres', 'Act', 'Ind', '1sg', '—',  'ἐκβάλλω',   'If I by the finger of God cast out demons, the kingdom has come.'],
            ['3',  'ἐστίν',      '1', 'Pres', 'Act', 'Ind', '3sg', '—',  'εἰμί',      'If God is righteous, he will judge the world.'],
            ['4',  'ἀγαπᾶτε',    '1', 'Pres', 'Act', 'Ind', '2pl', '—',  'ἀγαπάω',    'If you love me, you will keep my commandments.'],
            ['5',  'πιστεύετε',  '2', 'Pres', 'Act', 'Ind', '2pl', '—',  'πιστεύω',   'If you believed Moses, you would believe me (mixed).'],
            ['6',  'ἦτε',        '2', 'Impf', 'Act', 'Ind', '2pl', '—',  'εἰμί',      'If you were children of Abraham, you would be doing his works.'],
            ['7',  'ἐγνώκειτε',  '2', 'Plpf', 'Act', 'Ind', '2pl', '—', 'γινώσκω',   'If you had known me, you would have also known my Father.'],
            ['8',  'ἦτε',        '2', 'Impf', 'Act', 'Ind', '2pl', '—',  'εἰμί',      'If you were of the world, the world would love its own.'],
            ['9',  'ἦλθον',      '2', 'Aor',  'Act', 'Ind', '1sg', '—',  'ἔρχομαι',   'If I had not come and spoken to them, they would not have sin.'],
            ['10', 'ἦν',         '2', 'Impf', 'Act', 'Ind', '3sg', '—',  'εἰμί',      'If my kingdom were of this world, my servants would be fighting.'],
            ['11', 'ὁμολογῶμεν', '3', 'Pres', 'Act', 'Subj','1pl', '—',  'ὁμολογέω',  'If we confess our sins, he is faithful and just.'],
            ['12', 'εἴπωμεν',    '3', 'Aor',  'Act', 'Subj','1pl', '—',  'λέγω',      'If we say that we have no sin, we deceive ourselves.'],
            ['13', 'πιστεύσῃς',  '3', 'Aor',  'Act', 'Subj','2sg', '—',  'πιστεύω',   'If you believe, you will see the glory of God.'],
            ['14', 'ἁμάρτῃ',     '3', 'Aor',  'Act', 'Subj','3sg', '—',  'ἁμαρτάνω',  'If anyone should sin, we have an advocate with the Father.'],
            ['15', 'πάσχοιτε',   '4', 'Pres', 'Act', 'Opt', '2pl', '—',  'πάσχω',     'But even if you should suffer for righteousness, you are blessed.'],
            ['16', 'γένησθε',    '3', 'Aor',  'Mid', 'Subj','2pl', '—',  'γίνομαι',   'Who will harm you if you are zealous for what is good?'],
        ]
        # Part B
        hdrs_b = ['#', 'Form', 'Tense', 'Voice', 'Person/Case', 'Number/Gender', 'Mood/Type', 'Lexical', 'Translation']
        cr_b = [0.03, 0.10, 0.07, 0.07, 0.10, 0.12, 0.10, 0.11, 0.30]
        gk_b = [1]
        rows_b = [
            ['17', 'δότε',   '', '', '', '', '', '', ''],
            ['18', 'δῷ',     '', '', '', '', '', '', ''],
            ['19', 'διδόναι','', '', '', '', '', '', ''],
            ['20', 'δούς',   '', '', '', '', '', '', ''],
        ]
        ans_b = [
            ['17', 'δότε',    'Aor', 'Act', '2nd', 'Pl', 'Imperative', 'δίδωμι', 'He said: you give them something to eat.'],
            ['18', 'δῷ',      'Aor', 'Act', '3rd', 'Sg', 'Subjunctive','δίδωμι', 'So that he might give them eternal life.'],
            ['19', 'διδόναι', 'Pres','Act', '—',   '—',  'Infinitive', 'δίδωμι', 'God has authority to give it.'],
            ['20', 'δούς',    'Aor', 'Act', 'Nom', 'Sg Masc','Participle','δίδωμι','The one who gave authority to the people.'],
        ]
        self.add_multi_part_drill([
            {'title': 'Part A — Conditional Sentences',    'headers': hdrs_a, 'rows': rows_a, 'answers': ans_a, 'col_ratios': cr_a, 'greek_cols': gk_a},
            {'title': 'Part B — δίδωμι Non-Indicative',   'headers': hdrs_b, 'rows': rows_b, 'answers': ans_b, 'col_ratios': cr_b, 'greek_cols': gk_b},
        ], use_greek=True)


def build_bbg_ch35_conditionals_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh35ConditionalsdrillPDF,
        'BBG Chapter 35 — Conditionals and δίδωμι Non-Indicative',
        'Four Conditional Classes · Subjunctive · Infinitive · Imperative · Participle of δίδωμι',
        ['greek', 'bbg', 'ch35', 'exercises', 'ch35-conditionals-drill'],
        'ch35-conditionals-drill.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch36 — μι-Verbs Parsing Drill
# ---------------------------------------------------------------------------

class BbgCh36MiVerbsParsingPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Parse the bolded form (Tense · Voice · Person · Number · Mood · Lexical Form). '
            'For ἵστημι forms, note Transitive (T) or Intransitive (I). '
            'Provide a Translation.'
        )
        hdrs = ['#', 'Form', 'Tense', 'Voice', 'Person', 'Number', 'Mood', 'Lexical', 'T/I', 'Translation']
        cr = [0.03, 0.12, 0.07, 0.07, 0.06, 0.06, 0.07, 0.11, 0.05, 0.36]
        gk = [1]
        rows = [
            ['1',  'ἔστησεν',    '', '', '', '', '', '', '', ''],
            ['2',  'ἔστη',       '', '', '', '', '', '', '', ''],
            ['3',  'ἕστηκεν',    '', '', '', '', '', '', '', ''],
            ['4',  'ἵστησιν',    '', '', '', '', '', '', '', ''],
            ['5',  'στῆθι',      '', '', '', '', '', '', '', ''],
            ['6',  'ἑστήκατε',   '', '', '', '', '', '', '', ''],
            ['7',  'τίθησιν',    '', '', '', '', '', '', '', ''],
            ['8',  'τίθημι',     '', '', '', '', '', '', '', ''],
            ['9',  'ἔθηκαν',     '', '', '', '', '', '', '', ''],
            ['10', 'θές',        '', '', '', '', '', '', '', ''],
            ['11', 'δεῖξον',     '', '', '', '', '', '', '', ''],
            ['12', 'δείξω',      '', '', '', '', '', '', '', ''],
            ['13', 'δεικνύουσιν','', '', '', '', '', '', '', ''],
            ['14', 'ἀφίεμεν',    '', '', '', '', '', '', '', ''],
            ['15', 'ἀφιέναι',    '', '', '', '', '', '', '', ''],
            ['16', 'ἄφες',       '', '', '', '', '', '', '', ''],
            ['17', 'ἀπολλύμεθα', '', '', '', '', '', '', '', ''],
            ['18', 'ἀπολωλός',   '', '', '', '', '', '', '', ''],
            ['19', 'οἶδα',       '', '', '', '', '', '', '', ''],
            ['20', 'οἴδαμεν',    '', '', '', '', '', '', '', ''],
        ]
        ans = [
            ['1',  'ἔστησεν',    'Aor 1st','Act',  '3rd', 'Sg', 'Ind',  'ἵστημι',   'T', 'He set a child in their midst.'],
            ['2',  'ἔστη',       'Aor 2nd','Act',  '3rd', 'Sg', 'Ind',  'ἵστημι',   'I', 'Jesus stood in their midst and said: Peace to you.'],
            ['3',  'ἕστηκεν',    'Perf',   'Act',  '3rd', 'Sg', 'Ind',  'ἵστημι',   'I', 'The abomination of desolation is standing in the holy place.'],
            ['4',  'ἵστησιν',    'Pres',   'Act',  '3rd', 'Sg', 'Ind',  'ἵστημι',   'T', 'God sets them before his throne.'],
            ['5',  'στῆθι',      'Aor 2nd','Act',  '2nd', 'Sg', 'Imper','ἵστημι',   'I', 'Stand still and do not move.'],
            ['6',  'ἑστήκατε',   'Perf',   'Act',  '2nd', 'Pl', 'Ind',  'ἵστημι',   'I', 'Why are you standing looking into heaven?'],
            ['7',  'τίθησιν',    'Pres',   'Act',  '3rd', 'Sg', 'Ind',  'τίθημι',   '—', 'He puts it on the lampstand.'],
            ['8',  'τίθημι',     'Pres',   'Act',  '1st', 'Sg', 'Ind',  'τίθημι',   '—', 'I lay down my life for the sheep.'],
            ['9',  'ἔθηκαν',     'Aor',    'Act',  '3rd', 'Pl', 'Ind',  'τίθημι',   '—', 'Where they had placed him.'],
            ['10', 'θές',        'Aor',    'Act',  '2nd', 'Sg', 'Imper','τίθημι',   '—', 'Put your hand on her.'],
            ['11', 'δεῖξον',     'Aor',    'Act',  '2nd', 'Sg', 'Imper','δείκνυμι', '—', 'Show me your faith apart from your works.'],
            ['12', 'δείξω',      'Fut',    'Act',  '1st', 'Sg', 'Ind',  'δείκνυμι', '—', 'All these things I will show you.'],
            ['13', 'δεικνύουσιν','Pres',   'Act',  '3rd', 'Pl', 'Ind',  'δείκνυμι', '—', 'They showed him the coin of the poll tax.'],
            ['14', 'ἀφίεμεν',    'Pres',   'Act',  '1st', 'Pl', 'Ind',  'ἀφίημι',   '—', 'We forgive our debtors.'],
            ['15', 'ἀφιέναι',    'Pres',   'Act',  '—',   '—',  'Inf',  'ἀφίημι',   '—', 'Who is able to forgive sins except God alone?'],
            ['16', 'ἄφες',       'Aor',    'Act',  '2nd', 'Sg', 'Imper','ἀφίημι',   '—', 'Forgive us our debts.'],
            ['17', 'ἀπολλύμεθα', 'Pres',   'Mid',  '1st', 'Pl', 'Ind',  'ἀπόλλυμι', '—', 'We are perishing! Do you not care?'],
            ['18', 'ἀπολωλός',   'Perf',   'Act',  'Acc', 'Sg Neut','Ptc','ἀπόλλυμι','—', 'To seek the lost (the thing that has perished).'],
            ['19', 'οἶδα',       'Perf',   'Act',  '1st', 'Sg', 'Ind',  'οἶδα',     '—', 'I know that the Messiah is coming.'],
            ['20', 'οἴδαμεν',    'Perf',   'Act',  '1st', 'Pl', 'Ind',  'οἶδα',     '—', 'We know that the Son of God has come.'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Parsing Table', use_greek=True)


def build_bbg_ch36_mi_verbs_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh36MiVerbsParsingPDF,
        'BBG Chapter 36 — μι-Verb Parsing Drill',
        'ἵστημι · τίθημι · δείκνυμι · ἀφίημι · ἀπόλλυμι · οἶδα',
        ['greek', 'bbg', 'ch36', 'exercises', 'ch36-mi-verbs-parsing'],
        'ch36-mi-verbs-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch22 — First vs. Second Aorist Contrast Drill
# ---------------------------------------------------------------------------

class BbgCh22AoristContrastPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each aorist form: (1) classify as 1st or 2nd aorist, '
            '(2) give Person, (3) Number, (4) Lexical form, (5) Translation.'
        )
        hdrs = ['#', 'Form', 'Type (1st/2nd)', 'Person', 'Number', 'Lexical Form', 'Translation']
        cr = [0.04, 0.14, 0.11, 0.08, 0.09, 0.13, 0.41]
        gk = [1]
        rows = [
            ['1',  'ἔλυσα',        '', '', '', '', ''],
            ['2',  'εἶπον',        '', '', '', '', ''],
            ['3',  'ἦλθεν',        '', '', '', '', ''],
            ['4',  'εἶδον',        '', '', '', '', ''],
            ['5',  'ἐπίστευσας',   '', '', '', '', ''],
            ['6',  'ἔλαβεν',       '', '', '', '', ''],
            ['7',  'ἐδίδαξεν',     '', '', '', '', ''],
            ['8',  'ἔβαλεν',       '', '', '', '', ''],
            ['9',  'ἠκούσαμεν',    '', '', '', '', ''],
            ['10', 'ἔγνω',         '', '', '', '', ''],
            ['11', 'ἐκηρύξατε',    '', '', '', '', ''],
            ['12', 'ἔφαγεν',       '', '', '', '', ''],
            ['13', 'ἔσωσεν',       '', '', '', '', ''],
            ['14', 'ἀπέθανεν',     '', '', '', '', ''],
            ['15', 'ἐδόξασαν',     '', '', '', '', ''],
            ['16', 'ἐγένετο',      '', '', '', '', ''],
            ['17', 'ἐπίστευσαν',   '', '', '', '', ''],
            ['18', 'εὗρον',        '', '', '', '', ''],
            ['19', 'ἀπήγγειλαν',   '', '', '', '', ''],
            ['20', 'ἤγαγεν',       '', '', '', '', ''],
        ]
        ans = [
            ['1',  'ἔλυσα',       '1st', '1st', 'Sg', 'λύω',          'I loosed / I released'],
            ['2',  'εἶπον',       '2nd', '1st', 'Sg', 'λέγω',         'I said'],
            ['3',  'ἦλθεν',       '2nd', '3rd', 'Sg', 'ἔρχομαι',      'He came'],
            ['4',  'εἶδον',       '2nd', '1st', 'Sg', 'ὁράω',         'I saw'],
            ['5',  'ἐπίστευσας',  '1st', '2nd', 'Sg', 'πιστεύω',      'You believed'],
            ['6',  'ἔλαβεν',      '2nd', '3rd', 'Sg', 'λαμβάνω',      'He took'],
            ['7',  'ἐδίδαξεν',    '1st', '3rd', 'Sg', 'διδάσκω',      'He taught'],
            ['8',  'ἔβαλεν',      '2nd', '3rd', 'Sg', 'βάλλω',        'He threw / cast'],
            ['9',  'ἠκούσαμεν',   '1st', '1st', 'Pl', 'ἀκούω',        'We heard'],
            ['10', 'ἔγνω',        '2nd', '3rd', 'Sg', 'γινώσκω',      'He knew'],
            ['11', 'ἐκηρύξατε',   '1st', '2nd', 'Pl', 'κηρύσσω',      'You (pl.) preached'],
            ['12', 'ἔφαγεν',      '2nd', '3rd', 'Sg', 'ἐσθίω',        'He ate'],
            ['13', 'ἔσωσεν',      '1st', '3rd', 'Sg', 'σῴζω',         'He saved'],
            ['14', 'ἀπέθανεν',    '2nd', '3rd', 'Sg', 'ἀποθνῄσκω',    'He died'],
            ['15', 'ἐδόξασαν',    '1st', '3rd', 'Pl', 'δοξάζω',       'They glorified'],
            ['16', 'ἐγένετο',     '2nd', '3rd', 'Sg', 'γίνομαι',      'It came to pass / He became'],
            ['17', 'ἐπίστευσαν',  '1st', '3rd', 'Pl', 'πιστεύω',      'They believed'],
            ['18', 'εὗρον',       '2nd', '3rd', 'Pl', 'εὑρίσκω',      'They found'],
            ['19', 'ἀπήγγειλαν',  '1st', '3rd', 'Pl', 'ἀπαγγέλλω',    'They reported / announced'],
            ['20', 'ἤγαγεν',      '2nd', '3rd', 'Sg', 'ἄγω',          'He led / brought'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Parsing Table', use_greek=True)


def build_bbg_ch22_aorist_contrast(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh22AoristContrastPDF,
        'BBG Chapter 22 — First vs. Second Aorist Contrast Drill',
        'Second Aorist Active and Middle Indicative',
        ['greek', 'bbg', 'ch22', 'exercises', 'ch22-aorist-contrast'],
        'ch22-aorist-contrast.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch24 — Aorist and Future Passive Formation Drill
# ---------------------------------------------------------------------------

class BbgCh24PassiveFormationPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each passive form: (1) classify as Aorist Passive or Future Passive, '
            '(2) give Person, (3) Number, (4) Lexical form, (5) Translation.'
        )
        hdrs = ['#', 'Form', 'Tense (Aor/Fut)', 'Person', 'Number', 'Lexical Form', 'Translation']
        cr = [0.04, 0.16, 0.13, 0.08, 0.09, 0.14, 0.36]
        gk = [1]
        rows = [
            ['1',  'ἐλύθην',           '', '', '', '', ''],
            ['2',  'λυθήσομαι',        '', '', '', '', ''],
            ['3',  'ἐβλήθη',           '', '', '', '', ''],
            ['4',  'σωθήσεται',        '', '', '', '', ''],
            ['5',  'ἐβαπτίσθην',       '', '', '', '', ''],
            ['6',  'γραφήσεται',       '', '', '', '', ''],
            ['7',  'ἐδιδάχθητε',       '', '', '', '', ''],
            ['8',  'ἀκουσθήσεται',     '', '', '', '', ''],
            ['9',  'ἐγερθήσονται',     '', '', '', '', ''],
            ['10', 'ἠγέρθη',           '', '', '', '', ''],
            ['11', 'ἐπιστεύθη',        '', '', '', '', ''],
            ['12', 'δοξασθήσεται',     '', '', '', '', ''],
            ['13', 'ἐκρίθησαν',        '', '', '', '', ''],
            ['14', 'κριθήσονται',      '', '', '', '', ''],
            ['15', 'ἐλήμφθη',          '', '', '', '', ''],
            ['16', 'λημφθήσονται',     '', '', '', '', ''],
            ['17', 'ἀπεστάλην',        '', '', '', '', ''],
            ['18', 'ἀποσταλήσεται',    '', '', '', '', ''],
            ['19', 'εὑρέθη',           '', '', '', '', ''],
            ['20', 'εὑρεθήσεται',      '', '', '', '', ''],
        ]
        ans = [
            ['1',  'ἐλύθην',          'Aorist', '1st', 'Sg', 'λύω',          'I was loosed'],
            ['2',  'λυθήσομαι',       'Future', '1st', 'Sg', 'λύω',          'I will be loosed'],
            ['3',  'ἐβλήθη',          'Aorist', '3rd', 'Sg', 'βάλλω',        'He / it was thrown'],
            ['4',  'σωθήσεται',       'Future', '3rd', 'Sg', 'σῴζω',         'He will be saved'],
            ['5',  'ἐβαπτίσθην',      'Aorist', '1st', 'Sg', 'βαπτίζω',      'I was baptized'],
            ['6',  'γραφήσεται',      'Future', '3rd', 'Sg', 'γράφω',        'It will be written'],
            ['7',  'ἐδιδάχθητε',      'Aorist', '2nd', 'Pl', 'διδάσκω',      'You (pl.) were taught'],
            ['8',  'ἀκουσθήσεται',    'Future', '3rd', 'Sg', 'ἀκούω',        'It will be heard'],
            ['9',  'ἐγερθήσονται',    'Future', '3rd', 'Pl', 'ἐγείρω',       'They will be raised'],
            ['10', 'ἠγέρθη',          'Aorist', '3rd', 'Sg', 'ἐγείρω',       'He was raised'],
            ['11', 'ἐπιστεύθη',       'Aorist', '3rd', 'Sg', 'πιστεύω',      'It was believed'],
            ['12', 'δοξασθήσεται',    'Future', '3rd', 'Sg', 'δοξάζω',       'He / it will be glorified'],
            ['13', 'ἐκρίθησαν',       'Aorist', '3rd', 'Pl', 'κρίνω',        'They were judged'],
            ['14', 'κριθήσονται',     'Future', '3rd', 'Pl', 'κρίνω',        'They will be judged'],
            ['15', 'ἐλήμφθη',         'Aorist', '3rd', 'Sg', 'λαμβάνω',      'He / it was taken'],
            ['16', 'λημφθήσονται',    'Future', '3rd', 'Pl', 'λαμβάνω',      'They will be taken'],
            ['17', 'ἀπεστάλην',       'Aorist', '1st', 'Sg', 'ἀποστέλλω',    'I was sent'],
            ['18', 'ἀποσταλήσεται',   'Future', '3rd', 'Sg', 'ἀποστέλλω',    'He will be sent'],
            ['19', 'εὑρέθη',          'Aorist', '3rd', 'Sg', 'εὑρίσκω',      'He / it was found'],
            ['20', 'εὑρεθήσεται',     'Future', '3rd', 'Sg', 'εὑρίσκω',      'He / it will be found'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Parsing Table', use_greek=True)


def build_bbg_ch24_passive_formation(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh24PassiveFormationPDF,
        'BBG Chapter 24 — Aorist and Future Passive Formation Drill',
        'θη-Aorist Passive vs. θησ-Future Passive',
        ['greek', 'bbg', 'ch24', 'exercises', 'ch24-passive-formation'],
        'ch24-passive-formation.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch27 — Participle Use Classification Drill
# ---------------------------------------------------------------------------

class BbgCh27ParticipleUseSortPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each participle phrase, classify the use as ADV (adverbial), '
            'ADJ (adjectival), or SUB (substantival). '
            'Then identify the Key Signal (articular/anarthrous, presence of antecedent noun, etc.) '
            'and provide a Translation.'
        )
        hdrs = ['#', 'Greek Phrase', 'Use (ADV/ADJ/SUB)', 'Key Signal', 'Translation']
        cr = [0.04, 0.32, 0.11, 0.20, 0.33]
        gk = [1]
        rows = [
            ['1',  'ἀκούων ταῦτα ἐξῆλθεν',                     '', '', ''],
            ['2',  'ὁ πιστεύων εἰς αὐτόν',                      '', '', ''],
            ['3',  'ὁ λόγος ὁ λαλούμενος',                      '', '', ''],
            ['4',  'βλέπων τοὺς ὄχλους ἐσπλαγχνίσθη',           '', '', ''],
            ['5',  'οἱ πιστεύοντες σῴζονται',                    '', '', ''],
            ['6',  'εἶδεν τοὺς ἀδελφοὺς τοὺς ἐρχομένους',       '', '', ''],
            ['7',  'πορευόμενος εἶπεν αὐτοῖς',                   '', '', ''],
            ['8',  'ὁ ἀγαπῶν τὸν θεόν',                         '', '', ''],
            ['9',  'ἀνὴρ ὁ πιστεύων',                           '', '', ''],
            ['10', 'ἀπεκρίθη λέγων',                            '', '', ''],
            ['11', 'τοὺς ἔχοντας νόσους',                        '', '', ''],
            ['12', 'γυνὴ ἡ ἀσθενοῦσα',                          '', '', ''],
            ['13', 'ἀκούσαντες δὲ ἐχάρησαν',                    '', '', ''],
            ['14', 'οἱ ζητοῦντες τὴν ψυχήν',                    '', '', ''],
            ['15', 'λόγον τὸν ῥηθέντα',                         '', '', ''],
            ['16', 'ταῦτα εἰπὼν ἀπῆλθεν',                       '', '', ''],
            ['17', 'τὸ γεγεννημένον',                            '', '', ''],
            ['18', 'διδάσκων ἐν τῇ συναγωγῇ',                    '', '', ''],
            ['19', 'πᾶς ὁ πιστεύων',                            '', '', ''],
            ['20', 'ἡ γυνὴ ἡ λεγομένη',                         '', '', ''],
        ]
        ans = [
            ['1',  'ἀκούων ταῦτα ἐξῆλθεν',                    'ADV', 'Anarthrous, nom., modifies main verb action',    'Hearing these things, he went out'],
            ['2',  'ὁ πιστεύων εἰς αὐτόν',                     'SUB', 'Articular (ὁ), no antecedent noun',              'The one who believes in him'],
            ['3',  'ὁ λόγος ὁ λαλούμενος',                     'ADJ', 'Articular, modifies λόγος',                      'The word that was spoken'],
            ['4',  'βλέπων τοὺς ὄχλους ἐσπλαγχνίσθη',          'ADV', 'Anarthrous, nom., temporal',                     'Seeing the crowds, he had compassion'],
            ['5',  'οἱ πιστεύοντες σῴζονται',                   'SUB', 'Articular (οἱ), no antecedent noun',             'Those who believe are being saved'],
            ['6',  'εἶδεν τοὺς ἀδελφοὺς τοὺς ἐρχομένους',      'ADJ', 'Articular, agrees with ἀδελφούς',               'He saw the brothers, the ones coming'],
            ['7',  'πορευόμενος εἶπεν αὐτοῖς',                  'ADV', 'Anarthrous, nom., modal / temporal',             'While going, he said to them'],
            ['8',  'ὁ ἀγαπῶν τὸν θεόν',                        'SUB', 'Articular (ὁ), standalone phrase',               'The one who loves God'],
            ['9',  'ἀνὴρ ὁ πιστεύων',                          'ADJ', 'Articular, agrees with ἀνήρ',                   'A believing man (lit. a man, the one who believes)'],
            ['10', 'ἀπεκρίθη λέγων',                           'ADV', 'Anarthrous, modal (manner)',                     'He answered, saying'],
            ['11', 'τοὺς ἔχοντας νόσους',                       'SUB', 'Articular (τοὺς), no antecedent noun',           'Those who had diseases'],
            ['12', 'γυνὴ ἡ ἀσθενοῦσα',                         'ADJ', 'Articular, agrees with γυνή',                   'A sick woman (lit. a woman, the one who was sick)'],
            ['13', 'ἀκούσαντες δὲ ἐχάρησαν',                   'ADV', 'Anarthrous, nom., temporal (aorist = antecedent)','When they heard, they rejoiced'],
            ['14', 'οἱ ζητοῦντες τὴν ψυχήν',                   'SUB', 'Articular (οἱ), standalone',                    'Those who are seeking his life'],
            ['15', 'λόγον τὸν ῥηθέντα',                        'ADJ', 'Articular, agrees with λόγον',                  'The word that was spoken'],
            ['16', 'ταῦτα εἰπὼν ἀπῆλθεν',                      'ADV', 'Anarthrous, nom., temporal (aorist ptc.)',        'Having said these things, he departed'],
            ['17', 'τὸ γεγεννημένον',                           'SUB', 'Articular neuter, no antecedent',               'That which has been born'],
            ['18', 'διδάσκων ἐν τῇ συναγωγῇ',                   'ADV', 'Anarthrous, nom., circumstantial',              'While teaching in the synagogue'],
            ['19', 'πᾶς ὁ πιστεύων',                           'SUB', 'Articular (ὁ) with πᾶς',                        'Everyone who believes'],
            ['20', 'ἡ γυνὴ ἡ λεγομένη',                        'ADJ', 'Articular, agrees with γυνή',                   'The woman who is called'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Classification Table', use_greek=True)


def build_bbg_ch27_participle_use_sort(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh27ParticipleUseSortPDF,
        'BBG Chapter 27 — Participle Use Classification Drill',
        'Adverbial · Adjectival · Substantival Participles',
        ['greek', 'bbg', 'ch27', 'exercises', 'ch27-participle-use-sort'],
        'ch27-participle-use-sort.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch28 — Present vs. Aorist Adverbial Participle Contrast
# ---------------------------------------------------------------------------

class BbgCh28ParticipleTenseContrastPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each adverbial participle clause, classify the temporal relation as '
            'CONTEMP (present participle = same time as main verb) or '
            'ANTEC (aorist participle = prior to main verb). '
            'Then give Tense, Voice, Lexical form, and Translation.'
        )
        hdrs = ['#', 'Participle Clause', 'Relation', 'Tense', 'Voice', 'Lexical Form', 'Translation']
        cr = [0.04, 0.28, 0.08, 0.07, 0.07, 0.13, 0.33]
        gk = [1]
        rows = [
            ['1',  'ταῦτα εἰπὼν ἀπῆλθεν',                          '', '', '', '', ''],
            ['2',  'πορευόμενος κηρύσσει',                           '', '', '', '', ''],
            ['3',  'ἀκούσαντες ἐχάρησαν',                           '', '', '', '', ''],
            ['4',  'βλέπων τοὺς ὄχλους ἐσπλαγχνίσθη',               '', '', '', '', ''],
            ['5',  'ἐλθόντες εἶδον',                                 '', '', '', '', ''],
            ['6',  'προσευχόμενος μὴ βατταλογήσητε',                 '', '', '', '', ''],
            ['7',  'εἰσελθὼν εἰς τὴν συναγωγήν',                    '', '', '', '', ''],
            ['8',  'λαλῶν ταῦτα εἶπεν',                             '', '', '', '', ''],
            ['9',  'πιστεύσαντες ἐβαπτίσθησαν',                     '', '', '', '', ''],
            ['10', 'ἀποκριθεὶς εἶπεν',                               '', '', '', '', ''],
            ['11', 'διδάσκων ἐν τῇ συναγωγῇ ἐξεπλήσσοντο',          '', '', '', '', ''],
            ['12', 'ἐγερθεὶς παρέλαβεν τὸ παιδίον',                 '', '', '', '', ''],
            ['13', 'ἀναβλέψας εἰς τὸν οὐρανὸν εὐλόγησεν',           '', '', '', '', ''],
            ['14', 'κλαίων ἐξῆλθεν ἔξω',                            '', '', '', '', ''],
            ['15', 'εὑρόντες αὐτόν',                                 '', '', '', '', ''],
            ['16', 'ἐρχόμενος πρὸς αὐτόν',                          '', '', '', '', ''],
            ['17', 'λαβὼν τοὺς πέντε ἄρτους ηὐλόγησεν',             '', '', '', '', ''],
            ['18', 'ἐσθίων μετ᾽ αὐτῶν παρήγγειλεν',                 '', '', '', '', ''],
            ['19', 'ἀναστὰς ἐπορεύθη',                               '', '', '', '', ''],
            ['20', 'χαίροντες ὑπέστρεψαν',                           '', '', '', '', ''],
        ]
        ans = [
            ['1',  'ταῦτα εἰπὼν ἀπῆλθεν',                         'ANTEC',   'Aorist', 'Active',       'λέγω',          'Having said these things, he departed'],
            ['2',  'πορευόμενος κηρύσσει',                          'CONTEMP', 'Pres',  'Middle',        'πορεύομαι',     'While going, he preaches'],
            ['3',  'ἀκούσαντες ἐχάρησαν',                          'ANTEC',   'Aorist', 'Active',       'ἀκούω',         'When they heard, they rejoiced'],
            ['4',  'βλέπων τοὺς ὄχλους ἐσπλαγχνίσθη',              'CONTEMP', 'Pres',  'Active',        'βλέπω',         'While seeing the crowds, he had compassion'],
            ['5',  'ἐλθόντες εἶδον',                                'ANTEC',   'Aorist', 'Active',       'ἔρχομαι',       'After coming, they saw'],
            ['6',  'προσευχόμενος μὴ βατταλογήσητε',                'CONTEMP', 'Pres',  'Middle',        'προσεύχομαι',   'While praying, do not babble'],
            ['7',  'εἰσελθὼν εἰς τὴν συναγωγήν',                   'ANTEC',   'Aorist', 'Active',       'εἰσέρχομαι',    'After entering the synagogue'],
            ['8',  'λαλῶν ταῦτα εἶπεν',                            'CONTEMP', 'Pres',  'Active',        'λαλέω',         'While saying these things, he said (more)'],
            ['9',  'πιστεύσαντες ἐβαπτίσθησαν',                    'ANTEC',   'Aorist', 'Active',       'πιστεύω',       'When they believed, they were baptized'],
            ['10', 'ἀποκριθεὶς εἶπεν',                              'ANTEC',   'Aorist', 'Pass (dep.)',  'ἀποκρίνομαι',   'Having answered, he said'],
            ['11', 'διδάσκων ἐν τῇ συναγωγῇ ἐξεπλήσσοντο',         'CONTEMP', 'Pres',  'Active',        'διδάσκω',       'While he was teaching, they were amazed'],
            ['12', 'ἐγερθεὶς παρέλαβεν τὸ παιδίον',                'ANTEC',   'Aorist', 'Pass (dep.)',  'ἐγείρω',        'Having gotten up, he took the child'],
            ['13', 'ἀναβλέψας εἰς τὸν οὐρανὸν εὐλόγησεν',          'ANTEC',   'Aorist', 'Active',       'ἀναβλέπω',      'Having looked up to heaven, he blessed'],
            ['14', 'κλαίων ἐξῆλθεν ἔξω',                           'CONTEMP', 'Pres',  'Active',        'κλαίω',         'Weeping, he went outside'],
            ['15', 'εὑρόντες αὐτόν',                                'ANTEC',   'Aorist', 'Active',       'εὑρίσκω',       'After / when they found him'],
            ['16', 'ἐρχόμενος πρὸς αὐτόν',                         'CONTEMP', 'Pres',  'Middle',        'ἔρχομαι',       'While coming to him'],
            ['17', 'λαβὼν τοὺς πέντε ἄρτους ηὐλόγησεν',            'ANTEC',   'Aorist', 'Active',       'λαμβάνω',       'Having taken the five loaves, he blessed'],
            ['18', 'ἐσθίων μετ᾽ αὐτῶν παρήγγειλεν',                'CONTEMP', 'Pres',  'Active',        'ἐσθίω',         'While eating with them, he commanded'],
            ['19', 'ἀναστὰς ἐπορεύθη',                              'ANTEC',   'Aorist', 'Active',       'ἀνίστημι',      'Having risen, he went'],
            ['20', 'χαίροντες ὑπέστρεψαν',                          'CONTEMP', 'Pres',  'Active',        'χαίρω',         'Rejoicing, they returned'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Classification Table', use_greek=True)


def build_bbg_ch28_participle_tense_contrast(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh28ParticipleTenseContrastPDF,
        'BBG Chapter 28 — Present vs. Aorist Adverbial Participle Contrast',
        'Contemporaneous vs. Antecedent Action',
        ['greek', 'bbg', 'ch28', 'exercises', 'ch28-participle-tense-contrast'],
        'ch28-participle-tense-contrast.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch31 — Subjunctive Use Classification Drill
# ---------------------------------------------------------------------------

class BbgCh31SubjunctiveUseSortPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Classify each subjunctive clause by use code: '
            'HO (Hortatory), PU (Purpose), CO (3rd-class Conditional), '
            'IN (Indefinite Relative), DE (Deliberative), FS (Fear Statement). '
            'Then give Person, Number, Lexical form, and Translation.'
        )
        hdrs = ['#', 'Greek Clause', 'Use Code', 'Person', 'Number', 'Lexical Form', 'Translation']
        cr = [0.04, 0.30, 0.07, 0.07, 0.08, 0.12, 0.32]
        gk = [1]
        rows = [
            ['1',  'ἀγαπῶμεν ἀλλήλους',            '', '', '', '', ''],
            ['2',  'ἵνα πιστεύσητε',                '', '', '', '', ''],
            ['3',  'ἐὰν εἴπω ὑμῖν',                '', '', '', '', ''],
            ['4',  'ὅς ἐὰν ἀκούσῃ',                '', '', '', '', ''],
            ['5',  'τί ποιήσωμεν',                  '', '', '', '', ''],
            ['6',  'ἵνα σωθῶσιν',                   '', '', '', '', ''],
            ['7',  'μὴ φοβηθῶμεν',                  '', '', '', '', ''],
            ['8',  'ἐὰν ὁμολογήσῃ',                 '', '', '', '', ''],
            ['9',  'ὅπου ἐὰν εἰσέλθῃ',              '', '', '', '', ''],
            ['10', 'ποῦ ὑπάγω',                     '', '', '', '', ''],
            ['11', 'ἵνα γνῶτε',                     '', '', '', '', ''],
            ['12', 'εἰσέλθωμεν εἰς τὴν κατάπαυσιν','', '', '', '', ''],
            ['13', 'ἐὰν μὴ φάγητε',                 '', '', '', '', ''],
            ['14', 'ὃς ἐὰν ποιήσῃ τὸ θέλημα',       '', '', '', '', ''],
            ['15', 'ἵνα πλησθῶσιν',                 '', '', '', '', ''],
            ['16', 'πῶς σωθῶμεν',                   '', '', '', '', ''],
            ['17', 'φοβοῦμαι μὴ πλανηθῆτε',         '', '', '', '', ''],
            ['18', 'ἵνα ζήσωσιν',                   '', '', '', '', ''],
            ['19', 'ἐὰν ᾖ ἀγαθός',                  '', '', '', '', ''],
            ['20', 'ἄγωμεν ἐκεῖθεν',                '', '', '', '', ''],
        ]
        ans = [
            ['1',  'ἀγαπῶμεν ἀλλήλους',            'HO', '1st', 'Pl', 'ἀγαπάω',     'Let us love one another'],
            ['2',  'ἵνα πιστεύσητε',                'PU', '2nd', 'Pl', 'πιστεύω',    'In order that you may believe'],
            ['3',  'ἐὰν εἴπω ὑμῖν',                'CO', '1st', 'Sg', 'λέγω',       'If I say to you'],
            ['4',  'ὅς ἐὰν ἀκούσῃ',                'IN', '3rd', 'Sg', 'ἀκούω',      'Whoever hears'],
            ['5',  'τί ποιήσωμεν',                  'DE', '1st', 'Pl', 'ποιέω',      'What should we do?'],
            ['6',  'ἵνα σωθῶσιν',                   'PU', '3rd', 'Pl', 'σῴζω',       'In order that they might be saved'],
            ['7',  'μὴ φοβηθῶμεν',                  'HO', '1st', 'Pl', 'φοβέομαι',   'Let us not fear'],
            ['8',  'ἐὰν ὁμολογήσῃ',                 'CO', '3rd', 'Sg', 'ὁμολογέω',   'If he confesses'],
            ['9',  'ὅπου ἐὰν εἰσέλθῃ',              'IN', '3rd', 'Sg', 'εἰσέρχομαι', 'Wherever he enters'],
            ['10', 'ποῦ ὑπάγω',                     'DE', '1st', 'Sg', 'ὑπάγω',      'Where am I going? / Where should I go?'],
            ['11', 'ἵνα γνῶτε',                     'PU', '2nd', 'Pl', 'γινώσκω',    'In order that you may know'],
            ['12', 'εἰσέλθωμεν εἰς τὴν κατάπαυσιν','HO', '1st', 'Pl', 'εἰσέρχομαι', 'Let us enter into the rest'],
            ['13', 'ἐὰν μὴ φάγητε',                 'CO', '2nd', 'Pl', 'ἐσθίω',      'Unless you eat'],
            ['14', 'ὃς ἐὰν ποιήσῃ τὸ θέλημα',       'IN', '3rd', 'Sg', 'ποιέω',      'Whoever does the will'],
            ['15', 'ἵνα πλησθῶσιν',                 'PU', '3rd', 'Pl', 'πληρόω',     'In order that they might be filled'],
            ['16', 'πῶς σωθῶμεν',                   'DE', '1st', 'Pl', 'σῴζω',       'How can we be saved?'],
            ['17', 'φοβοῦμαι μὴ πλανηθῆτε',         'FS', '2nd', 'Pl', 'πλανάω',     'I fear that you may be led astray'],
            ['18', 'ἵνα ζήσωσιν',                   'PU', '3rd', 'Pl', 'ζάω',        'In order that they might live'],
            ['19', 'ἐὰν ᾖ ἀγαθός',                  'CO', '3rd', 'Sg', 'εἰμί',       'If he is good'],
            ['20', 'ἄγωμεν ἐκεῖθεν',                'HO', '1st', 'Pl', 'ἄγω',        'Let us go from there'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Classification Table', use_greek=True)


def build_bbg_ch31_subjunctive_use_sort(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh31SubjunctiveUseSortPDF,
        'BBG Chapter 31 — Subjunctive Use Classification Drill',
        'Hortatory · Purpose · Conditional · Indefinite · Deliberative · Fear Statement',
        ['greek', 'bbg', 'ch31', 'exercises', 'ch31-subjunctive-use-sort'],
        'ch31-subjunctive-use-sort.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBG Ch33 — Prohibition Pattern Drill
# ---------------------------------------------------------------------------

class BbgCh33ProhibitionDrillPDF(GreekExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each prohibition, classify the pattern as '
            'STOP (μή + present imperative = stop an ongoing action) or '
            'DONT (μή + aorist subjunctive = do not begin an action). '
            'Then give Tense, Mood, Lexical form, and Translation.'
        )
        hdrs = ['#', 'Greek Sentence', 'Pattern (STOP/DONT)', 'Tense', 'Mood', 'Lexical Form', 'Translation']
        cr = [0.04, 0.30, 0.10, 0.07, 0.08, 0.12, 0.29]
        gk = [1]
        rows = [
            ['1',  'μὴ κλαίετε',                           '', '', '', '', ''],
            ['2',  'μὴ φοβηθῇς',                           '', '', '', '', ''],
            ['3',  'μὴ νομίζετε ὅτι ἦλθον',               '', '', '', '', ''],
            ['4',  'μὴ εἰσέλθῃς εἰς πειρασμόν',           '', '', '', '', ''],
            ['5',  'μὴ μεριμνᾶτε',                         '', '', '', '', ''],
            ['6',  'μὴ λαλήσῃς κακόν',                    '', '', '', '', ''],
            ['7',  'μὴ θαυμάζετε',                         '', '', '', '', ''],
            ['8',  'μὴ πορευθῇς',                          '', '', '', '', ''],
            ['9',  'μὴ λέγε τοῦτο',                        '', '', '', '', ''],
            ['10', 'μὴ ἅψῃ',                               '', '', '', '', ''],
            ['11', 'μὴ φοβεῖσθε',                          '', '', '', '', ''],
            ['12', 'μὴ ἀποκτείνῃς',                        '', '', '', '', ''],
            ['13', 'μὴ κρίνετε',                           '', '', '', '', ''],
            ['14', 'μὴ ἁμάρτῃς',                           '', '', '', '', ''],
            ['15', 'μὴ κατεσθίετε τοὺς πτωχούς',          '', '', '', '', ''],
            ['16', 'μὴ ἄρῃς τὸ σκεῦος',                   '', '', '', '', ''],
            ['17', 'μὴ ἐπιθυμεῖτε',                        '', '', '', '', ''],
            ['18', 'μὴ πιστεύσῃς',                         '', '', '', '', ''],
            ['19', 'μὴ δίδοτε τὸ ἅγιον τοῖς κυσίν',       '', '', '', '', ''],
            ['20', 'μὴ ποιήσῃς τοῦτο',                    '', '', '', '', ''],
        ]
        ans = [
            ['1',  'μὴ κλαίετε',                          'STOP', 'Pres', 'Imperative',  'κλαίω',        'Stop weeping'],
            ['2',  'μὴ φοβηθῇς',                          'DONT', 'Aor',  'Subjunctive', 'φοβέομαι',     'Do not be afraid'],
            ['3',  'μὴ νομίζετε ὅτι ἦλθον',              'STOP', 'Pres', 'Imperative',  'νομίζω',       'Stop thinking that I came'],
            ['4',  'μὴ εἰσέλθῃς εἰς πειρασμόν',          'DONT', 'Aor',  'Subjunctive', 'εἰσέρχομαι',   'Do not enter into temptation'],
            ['5',  'μὴ μεριμνᾶτε',                        'STOP', 'Pres', 'Imperative',  'μεριμνάω',     'Stop worrying'],
            ['6',  'μὴ λαλήσῃς κακόν',                   'DONT', 'Aor',  'Subjunctive', 'λαλέω',        'Do not speak evil'],
            ['7',  'μὴ θαυμάζετε',                        'STOP', 'Pres', 'Imperative',  'θαυμάζω',      'Stop marveling'],
            ['8',  'μὴ πορευθῇς',                         'DONT', 'Aor',  'Subjunctive', 'πορεύομαι',    'Do not go'],
            ['9',  'μὴ λέγε τοῦτο',                       'STOP', 'Pres', 'Imperative',  'λέγω',         'Stop saying this'],
            ['10', 'μὴ ἅψῃ',                              'DONT', 'Aor',  'Subjunctive', 'ἅπτω',         'Do not touch'],
            ['11', 'μὴ φοβεῖσθε',                         'STOP', 'Pres', 'Imperative',  'φοβέομαι',     'Stop being afraid'],
            ['12', 'μὴ ἀποκτείνῃς',                       'DONT', 'Aor',  'Subjunctive', 'ἀποκτείνω',    'Do not kill'],
            ['13', 'μὴ κρίνετε',                          'STOP', 'Pres', 'Imperative',  'κρίνω',        'Do not judge (stop judging)'],
            ['14', 'μὴ ἁμάρτῃς',                          'DONT', 'Aor',  'Subjunctive', 'ἁμαρτάνω',     'Do not sin'],
            ['15', 'μὴ κατεσθίετε τοὺς πτωχούς',         'STOP', 'Pres', 'Imperative',  'κατεσθίω',     'Stop devouring the poor'],
            ['16', 'μὴ ἄρῃς τὸ σκεῦος',                  'DONT', 'Aor',  'Subjunctive', 'αἴρω',         'Do not take the vessel'],
            ['17', 'μὴ ἐπιθυμεῖτε',                       'STOP', 'Pres', 'Imperative',  'ἐπιθυμέω',     'Stop desiring / do not covet'],
            ['18', 'μὴ πιστεύσῃς',                        'DONT', 'Aor',  'Subjunctive', 'πιστεύω',      'Do not believe'],
            ['19', 'μὴ δίδοτε τὸ ἅγιον τοῖς κυσίν',      'STOP', 'Pres', 'Imperative',  'δίδωμι',       'Do not give what is holy to dogs'],
            ['20', 'μὴ ποιήσῃς τοῦτο',                   'DONT', 'Aor',  'Subjunctive', 'ποιέω',        'Do not do this'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, greek_cols=gk,
                                       section_title='Classification Table', use_greek=True)


def build_bbg_ch33_prohibition_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        BbgCh33ProhibitionDrillPDF,
        'BBG Chapter 33 — Prohibition Pattern Drill',
        'μή + Present Imperative (STOP) vs. μή + Aorist Subjunctive (DONT)',
        ['greek', 'bbg', 'ch33', 'exercises', 'ch33-prohibition-drill'],
        'ch33-prohibition-drill.pdf',
        out_dir,
    )
