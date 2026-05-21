from typing import Optional
from ._base import (
    ExercisePDF, PassageExercise,
    VerbEntry, PassageBlock, ContrastEntry, NHEntry, BGEntry, SortEntry,
    _build_exercise_pdf,
    _heb, _mixed_font,
    C_RULE, C_ANSWER_BG, C_ANSWER_FG, C_HEADER_BG,
)
from reportlab.lib.units import inch
from reportlab.lib.colors import black
from reportlab.lib.utils import simpleSplit

# ---------------------------------------------------------------------------
# Chapter 26 exercise
# ---------------------------------------------------------------------------


class Ch26Exercise(PassageExercise):
    _instructions = (
        'Most highlighted verbs are Hiphil forms. For each one, first answer '
        'Is it Hiphil? (Yes / No). If Yes: fill in Conjugation, PGN, Root, and Function. '
        'If No: identify the correct stem and parse fully. '
        'Three verbs in this exercise are not Hiphil — drawn from Qal and Niphal already studied. '
        'The answer key begins on the page marked "Answer Key".'
    )

    def _render_passages(self, show_answers: bool) -> None:
        """Render all passages and verb tables; called twice (questions-only, then with answers)."""

        # ── Passage A ────────────────────────────────────────────────────────
        self.add_section_heading('Passage A — Genesis 6:12–20')

        self.add_passage(PassageBlock(
            '6:12',
            'וַיַּרְא אֱלֹהִים אֶת־הָאָרֶץ וְהִנֵּה נִשְׁחָתָה כִּי־הִשְׁחִית כָּל־בָּשָׂר אֶת־דַּרְכּוֹ עַל־הָאָרֶץ',
            '"And God saw the earth, and behold, it [1] ____; for all flesh had [2] ____ its way upon the earth."'))
        self.add_verb_table([
            VerbEntry('1', 'נִשְׁחָתָה', 'Weqatal', '3fs', 'שָׁחַת', 'NOT Hiphil — Niphal passive: it was corrupt; נִ- prefix = Niphal, not הִ- Hiphil'),
            VerbEntry('2', 'הִשְׁחִית', 'Perfect (qatal)', '3ms', 'שָׁחַת', 'Causative — had corrupted'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock(
            '6:13',
            'הִנְנִי מַשְׁחִיתָם עִם־הָאָרֶץ',
            '"Behold, I am [3] ____ them with the earth."'))
        self.add_verb_table([VerbEntry('3', 'מַשְׁחִיתָם', 'Participle + 3mp suffix', 'ms', 'שָׁחַת', 'Causative — destroying them')], show_answers=show_answers)

        self.add_passage(PassageBlock(
            '6:17',
            'וַאֲנִי הִנְנִי מֵבִיא אֶת־הַמַּבּוּל מַיִם עַל־הָאָרֶץ',
            '"As for me, behold, I am [4] ____ the flood of waters upon the earth."'))
        self.add_verb_table([VerbEntry('4', 'מֵבִיא', 'Participle', 'ms', 'בּוֹא', 'Causative — bringing')], show_answers=show_answers)

        self.add_passage(PassageBlock(
            '6:18',
            'וַהֲקִמֹתִי אֶת־בְּרִיתִי אִתָּךְ',
            '"But I will [5] ____ my covenant with you."'))
        self.add_verb_table([VerbEntry('5', 'וַהֲקִמֹתִי', 'Weqatal', '1cs', 'קוּם', 'Factitive — I will establish')], show_answers=show_answers)

        self.add_passage(PassageBlock(
            '6:19',
            'מִכָּל־בָּשָׂר שְׁנַיִם מִכֹּל תָּבִיא אֶל־הַתֵּבָה',
            '"Of every living thing you shall [6] ____ two of every kind into the ark."'))
        self.add_verb_table([VerbEntry('6', 'תָּבִיא', 'Imperfect', '2ms', 'בּוֹא', 'Causative — you shall bring')], show_answers=show_answers)

        self.add_passage(PassageBlock(
            '6:19–20',
            'לְהַחֲיֹת אִתָּךְ … לְהַחֲיוֹת',
            '"to [7] ____ them alive with you … to [8] ____ them"'))
        self.add_verb_table([
            VerbEntry('7', 'לְהַחֲיֹת', 'Inf. Construct', '—', 'חָיָה', 'Causative — to keep alive'),
            VerbEntry('8', 'לְהַחֲיוֹת', 'Inf. Construct', '—', 'חָיָה', 'Causative — to keep alive'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B ────────────────────────────────────────────────────────
        self.add_section_heading('Passage B — Genesis 7:4')

        self.add_passage(PassageBlock(
            '7:4',
            'כִּי לְיָמִים עוֹד שִׁבְעָה אָנֹכִי מַמְטִיר עַל־הָאָרֶץ אַרְבָּעִים יוֹם',
            '"For in seven days I will [9] ____ rain on the earth forty days."'))
        self.add_verb_table([VerbEntry('9', 'מַמְטִיר', 'Participle', 'ms', 'מָטַר', 'Causative/Denominative — causing rain')], show_answers=show_answers)

        self.add_section_break()

        # ── Passage C ────────────────────────────────────────────────────────
        self.add_section_heading('Passage C — Genesis 8:1–21')

        self.add_passage(PassageBlock('8:1', 'וַיַּעֲבֵר אֱלֹהִים רוּחַ עַל־הָאָרֶץ',
            '"And God [10] ____ a wind over the earth."'))
        self.add_verb_table([VerbEntry('10', 'וַיַּעֲבֵר', 'Wayyiqtol', '3ms', 'עָבַר', 'Causative — caused to pass over')], show_answers=show_answers)

        self.add_passage(PassageBlock('8:9', 'וַיָּבֵא אֹתָהּ אֵלָיו אֶל־הַתֵּבָה',
            '"And he [11] ____ her back to him into the ark."'))
        self.add_verb_table([VerbEntry('11', 'וַיָּבֵא', 'Wayyiqtol', '3ms', 'בּוֹא', 'Causative — brought')], show_answers=show_answers)

        self.add_passage(PassageBlock('8:13', 'וַיָּסַר נֹחַ אֶת־מִכְסֵה הַתֵּבָה',
            '"And Noah [12] ____ the covering of the ark."'))
        self.add_verb_table([VerbEntry('12', 'וַיָּסַר', 'Wayyiqtol', '3ms', 'סוּר', 'Causative — removed')], show_answers=show_answers)

        self.add_passage(PassageBlock('8:17', 'הַיְצֵא אִתָּךְ כָּל־הַחַיָּה',
            '"[13] ____ with you every living thing."'))
        self.add_verb_table([VerbEntry('13', 'הַיְצֵא', 'Imperative', '2ms', 'יָצָא', 'Causative — bring out!')], show_answers=show_answers)

        self.add_passage(PassageBlock('8:20', 'וַיַּעַל עֹלֹת בַּמִּזְבֵּחַ',
            '"And he [14] ____ burnt offerings on the altar."'))
        self.add_verb_table([VerbEntry('14', 'וַיַּעַל', 'Wayyiqtol', '3ms', 'עָלָה', 'Causative — offered up')], show_answers=show_answers)

        self.add_passage(PassageBlock('8:21', 'לֹא־אֹסִף לְהַכֹּת אֶת־כָּל־חַי',
            '"I will never again [15] ____ every living thing."'))
        self.add_verb_table([VerbEntry('15', 'לְהַכֹּת', 'Inf. Construct', '—', 'נָכָה', 'Causative — to strike down')], show_answers=show_answers)

        self.add_section_break()

        # ── Passage D ────────────────────────────────────────────────────────
        self.add_section_heading('Passage D — Genesis 22:17  (Infinitive Absolute)')

        self.add_passage(PassageBlock(
            '22:17',
            'כִּי בָרֵךְ אֲבָרֶכְךָ וְהַרְבָּה אַרְבֶּה אֶת־זַרְעֲךָ כְּכוֹכְבֵי הַשָּׁמַיִם',
            '"For I will surely bless you, and I will [16] ____ [17] ____ your offspring as the stars of heaven."',
            watchout='Watch out: בָּרֵךְ and אֲבָרֶכְךָ are Piel forms of בָּרַךְ ("to bless") — not Hiphil. Parse only verbs 16–17.'))
        self.add_verb_table([
            VerbEntry('16', 'וְהַרְבָּה', 'Inf. Absolute', '—', 'רָבָה', 'Causative — emphatic modifier (surely/multiplying)'),
            VerbEntry('17', 'אַרְבֶּה',  'Imperfect',   '1cs', 'רָבָה', 'Causative — I will multiply'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage E ────────────────────────────────────────────────────────
        self.add_section_heading('Passage E — Deuteronomy 7:2  (Weqatal + Emphatic Pair)')

        self.add_passage(PassageBlock(
            '7:2',
            'וּנְתָנָם יְהוָה אֱלֹהֶיךָ לְפָנֶיךָ וְהִכִּיתָם הַכֵּה תַכֶּה לֹא־תִכְרֹת לָהֶם בְּרִית',
            '"When the LORD your God [18] ____ them over, you shall [19] ____ them — [20] ____ [21] ____ them — [22] ____ no covenant with them."'))
        self.add_verb_table([
            VerbEntry('18', 'וּנְתָנָם', 'Weqatal',      '3ms', 'נָתַן', 'NOT Hiphil — Qal: and he gives/gives over; וּ + Qal perfect/weqatal; no הִ- prefix'),
            VerbEntry('19', 'וְהִכִּיתָם', 'Weqatal',    '2ms', 'נָכָה', 'Causative — and you shall strike them'),
            VerbEntry('20', 'הַכֵּה',    'Inf. Absolute', '—', 'נָכָה', 'Causative — emphatic modifier (certainly)'),
            VerbEntry('21', 'תַכֶּה',    'Imperfect',    '2ms', 'נָכָה', 'Causative — you shall strike'),
            VerbEntry('22', 'תִכְרֹת',  'Imperfect',    '2ms', 'כָּרַת', 'NOT Hiphil — Qal: you shall cut (covenant); plain Qal imperfect; no הַ- Hiphil prefix'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Bonus ─────────────────────────────────────────────────────────────
        self.add_section_heading('Bonus — Genesis 6:1, 6:10')

        self.add_passage(PassageBlock('6:1', 'כִּי־הֵחֵל הָאָדָם לָרֹב', '"When man began to multiply…"'))
        self.add_passage(PassageBlock('6:10', 'וַיּוֹלֶד נֹחַ שְׁלֹשָׁה בָנִים', '"And Noah fathered three sons."'))
        self.add_verb_table([
            VerbEntry('B1', 'הֵחֵל',    'Perfect (qatal)', '3ms', 'חָלַל', 'Causative — began (Hiphil of חָלַל = to begin)'),
            VerbEntry('B2', 'וַיּוֹלֶד', 'Wayyiqtol',      '3ms', 'יָלַד', 'Causative — fathered / begat'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Notes + Score ─────────────────────────────────────────────────────
        self.add_note(
            'Note: #2 (הִשְׁחִית) and B1 (הֵחֵל) are Perfect (qatal), not Weqatal — both follow כִּי '
            'with no waw prefix. #16–17 and #20–21 illustrate the emphatic inf. absolute + imperfect '
            'construction: the inf. absolute intensifies the finite verb ("shall certainly strike"). '
            '#1 (נִשְׁחָתָה) is Niphal of the same root as #2 — compare: Niphal נִ- vs. Hiphil הִ-.'
        )
        self.add_score(
            'Score: 19 Hiphil + 3 non-Hiphil + 2 bonus = 24 total.  '
            '21–24 = excellent  |  16–20 = review the paradigm  |  below 16 = revisit §26.3–26.13'
        )

        # ── Coverage table ────────────────────────────────────────────────────
        self.add_section_heading('Conjugation Coverage')
        self.add_coverage_table([
            ('Wayyiqtol (5)',          '#10, #11, #12, #14, B2'),
            ('Inf. Construct (3)',     '#7, #8, #15'),
            ('Participle (3)',         '#3, #4, #9'),
            ('Imperfect (3)',          '#6, #17, #21'),
            ('Perfect / qatal (2)',    '#2, B1'),
            ('Weqatal (2)',            '#5, #19'),
            ('Inf. Absolute (2)',      '#16, #20'),
            ('Imperative (1)',         '#13'),
            ('Non-Hiphil (3)',         '#1 (Niphal Weqatal 3fs), #18 (Qal Weqatal 3ms), #22 (Qal Imperfect 2ms)'),
        ])

        # ── Reflection (only on question pages, not repeated in key) ──────────
        if not show_answers:
            self.add_reflection([
                'Wayyiqtol dominates in Gen 6–8 but is absent from Passages D and E. What does this tell '
                'you about how genre — narrative vs. divine oracle (Gen 22) vs. legal instruction (Deut 7) '
                '— shapes conjugation choice in the Hiphil?',
                'Both Passage D (Gen 22:17) and Passage E (Deut 7:2) use the emphatic inf. absolute + '
                'imperfect pattern. What does the inf. absolute add beyond a plain imperfect? Are the two '
                'contexts — promise and command — using the emphasis for the same rhetorical purpose?',
                'In Gen 6–8, God is the subject of nearly every Hiphil; Noah appears as subject only at '
                '#11 and #13. What does this distribution of agency tell you about the theological '
                'architecture of the flood narrative?',
            ])


# ---------------------------------------------------------------------------
# Chapter 26 — Qal–Hiphil Contrast Drill
# ---------------------------------------------------------------------------


class Ch26ContrastExercise(ExercisePDF):

    _ENTRIES_A = [
        ContrastEntry('1', 'בּוֹא', 'to go in, come',   'יָּבֵא',      'Wayyiqtol 3ms', 'Gen 2:19',  'he brought (them)',          'Causative',      'God caused the animals to come to Adam'),
        ContrastEntry('2', 'יָצָא', 'to go out',        'תּוֹצֵא',     'Wayyiqtol 3fs', 'Gen 1:12',  'it brought forth',           'Causative',      'Earth caused vegetation to come out'),
        ContrastEntry('3', 'שׁוּב', 'to return',        'הֵשִׁיב',     'Weqatal 3ms',   'Gen 14:16', 'he brought back',            'Causative',      'Abraham caused Lot to return'),
        ContrastEntry('4', 'עָלָה', 'to go up',         'הַעֲלֵה',     'Imperative 2ms', 'Gen 22:2',  'offer up! / bring up!',      'Causative',      'Cause Isaac to go up as an offering'),
        ContrastEntry('5', 'יָרַד', 'to go down',       'תֹּרֶד',      'Wayyiqtol 3fs', 'Gen 24:18', 'she lowered (her jar)',       'Causative',      'Rebekah caused the jar to go down'),
        ContrastEntry('6', 'מוּת',  'to die',           'הָמִית',      'Inf. Constr.',  'Gen 18:25', 'to put to death / to kill',  'Causative',      'Causing someone to die'),
        ContrastEntry('7', 'יָלַד', 'to give birth',    'יּוֹלֶד',     'Wayyiqtol 3ms', 'Gen 5:3',   'he fathered / begat',        'Causative',      'Adam caused a son to be born'),
        ContrastEntry('8', 'שָׁקָה', 'to drink',        'הִשְׁקָה',    'Perfect 3ms',   'Gen 2:6',   'it watered',                 'Causative',      'Mist caused the ground to receive water'),
    ]
    _ENTRIES_B = [
        ContrastEntry('9',  'כָּבֵד', 'to be heavy/honored', 'יַּכְבֵּד',   'Wayyiqtol 3ms', 'Exo 8:28', 'he hardened (his heart)',         'Factitive',   'Caused heart to be in state of stubbornness'),
        ContrastEntry('10', 'גָּדַל', 'to be great',         'תַּגְדֵּל',   'Wayyiqtol 2ms', 'Gen 19:19', 'you have made great (your mercy)', 'Factitive',   'Caused kindness to be great'),
        ContrastEntry('11', 'רָשָׁע', 'to be wicked',        'הִרְשִׁיעוּ', 'Perfect 3cp',    'Deu 25:1', 'they condemned as guilty',         'Declarative', 'Legal verdict: declaring guilty party as guilty'),
    ]
    _ENTRIES_C = [
        ContrastEntry('12', 'נָכָה', 'no Qal in BH', 'הַכּוֹת',      'Inf. Construct', 'Gen 4:15',  'to strike / smite',  'Simple Action', 'Hiphil is primary form; no causative layer'),
        ContrastEntry('13', 'שָׁמַד', 'no Qal in BH', 'הִשְׁמַדְתִּי', 'Perfect 1cs',    'Lev 26:30', 'I will destroy',      'Simple Action', 'Niphal of same root = "to be destroyed"'),
        ContrastEntry('14', 'נָגַד', 'rare Qal',      'יַּגֵּד',      'Wayyiqtol 3ms', 'Gen 9:22',  'he told / reported', 'Simple Action', 'Root idea = place before someone'),
    ]

    def _build(self) -> None:
        self.add_instructions(
            'For each item: (1) write an English translation of the Hiphil form in the Translation '
            'column; (2) write the semantic function (Causative / Factitive / Declarative / Simple '
            'Action) in the Function column. Answer key is on the last page.'
        )

        self.add_section_heading('Part A — Motion Verbs (Causative)')
        self.add_note('These roots describe motion in the Qal. The Hiphil makes someone else do the moving.')
        self.add_contrast_table(self._ENTRIES_A, show_answers=False)

        self.add_section_heading('Part B — Stative Verbs (Factitive and Declarative)')
        self.add_note(
            'Factitive: the Hiphil causes an object to be in a state (make heavy, make great). '
            'Declarative: the Hiphil declares/treats something as being in that state (declare guilty).'
        )
        self.add_contrast_table(self._ENTRIES_B, show_answers=False)

        self.add_section_heading('Part C — Verbs with No Common Qal')
        self.add_note('Hiphil is the standard/primary form of these roots. No Qal "base" to compare against.')
        self.add_contrast_table(self._ENTRIES_C, show_answers=False)

        self.add_reflection([
            'For the motion verbs in Part A, describe the pattern in one sentence: what does the '
            'Hiphil consistently do to the Qal meaning?',
            'Which of Part B\'s three verbs is Factitive and which is Declarative? How did you decide?',
            'Does the lack of a Qal counterpart (Part C) affect how you translate the Hiphil? Why or why not?',
        ])

        self.add_answer_key_contrast(self._ENTRIES_A + self._ENTRIES_B + self._ENTRIES_C)


def build_ch26_contrast_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch26ContrastExercise,
        'Chapter 26 — Qal–Hiphil Contrast Drill',
        'BBH Chapter 26 · Hiphil Strong Verbs',
        ['hebrew', 'bbh', 'ch26', 'exercises', 'ch26-qal-hiphil-contrast'],
        'ch26-qal-hiphil-contrast.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 26 — Semantic Function Sorting
# ---------------------------------------------------------------------------


class Ch26FunctionSortExercise(ExercisePDF):

    _ENTRIES = [
        SortEntry('1',  'וַיָּבֵא',       'Wayyiqtol 3ms',  'Gen 2:19',  '"he brought them to the man"',                     'C',  'בּוֹא',  'Qal = to come; Hiphil = cause to come'),
        SortEntry('2',  'וַתּוֹצֵא',     'Wayyiqtol 3fs',  'Gen 1:12',  '"the earth brought forth vegetation"',              'C',  'יָצָא',  'Qal = to go out; Hiphil = cause to come out'),
        SortEntry('3',  'וַיָּשֶׁב',     'Wayyiqtol 3ms',  'Gen 14:16', '"he brought back his brother Lot"',                 'C',  'שׁוּב',  'Qal = to return; Hiphil = cause to return'),
        SortEntry('4',  'הִשְׁקָה',      'Perfect 3ms',    'Gen 2:6',   '"a mist watered the whole surface"',                'C',  'שָׁקָה', 'Qal = to drink; Hiphil = cause to drink/water'),
        SortEntry('5',  'וַיּוֹלֶד',     'Wayyiqtol 3ms',  'Gen 5:3',   '"Adam fathered a son"',                            'C',  'יָלַד',  'Qal = to give birth; Hiphil = cause to be born'),
        SortEntry('6',  'הַעֲלֵה',       'Imperative 2ms', 'Gen 22:2',  '"offer him as a burnt offering"',                   'C',  'עָלָה',  'Qal = to go up; Hiphil = cause to go up/offer'),
        SortEntry('7',  'וַתֹּרֶד',      'Wayyiqtol 3fs',  'Gen 24:18', '"she lowered her jar to give him a drink"',         'C',  'יָרַד',  'Qal = to go down; Hiphil = cause to go down'),
        SortEntry('8',  'וַיָּסַר',      'Wayyiqtol 3ms',  'Gen 30:35', '"he removed the streaked goats"',                   'C',  'סוּר',   'Qal = to turn aside; Hiphil = cause to depart'),
        SortEntry('9',  'וַיַּגֵּד',     'Wayyiqtol 3ms',  'Gen 9:22',  '"Ham told his two brothers"',                      'SA', 'נָגַד',  'Rare Qal; Hiphil is operative form: to tell'),
        SortEntry('10', 'הִגִּיד',       'Weqatal 3ms',    'Gen 3:11',  '"who told you that you were naked?"',               'SA', 'נָגַד',  'Same root as #9; Hiphil = standard form'),
        SortEntry('11', 'וַתַּשְׁלֵךְ',  'Wayyiqtol 3fs',  'Gen 21:15', '"she threw the child under a bush"',                'SA', 'שָׁלַךְ', 'No common Qal; Hiphil = to throw/cast'),
        SortEntry('12', 'הִזְכַּרְתָּ', 'Perfect 2ms',    'Gen 40:14', '"mention me to Pharaoh"',                           'C',  'זָכַר',  'Qal = to remember; Hiphil = cause to remember'),
        SortEntry('13', 'מַזְכִּיר',    'Participle ms',  'Gen 41:9',  '"I am bringing my faults to mind"',                 'C',  'זָכַר',  'Causing something to be remembered'),
        SortEntry('14', 'הָמִית',        'Inf. Constr.',   'Gen 18:25', '"far be it from you to put…to death"',              'C',  'מוּת',   'Qal = to die; Hiphil = cause to die'),
        SortEntry('15', 'הַכּוֹת',       'Inf. Constr.',   'Gen 4:15',  '"lest anyone who found him strike him"',            'SA', 'נָכָה',  'No Qal; Hiphil = primary form: to strike'),
        SortEntry('16', 'הִשְׁמַדְתִּי', 'Perfect 1cs',   'Lev 26:30', '"I will destroy your high places"',                 'SA', 'שָׁמַד', 'No Qal; Niphal = "be destroyed"'),
        SortEntry('17', 'תַּשְׁמִידוּ', 'Imperfect 2mp',  'Num 33:52', '"you shall demolish their figured stones"',          'SA', 'שָׁמַד', 'Same root as #16; conquest context'),
        SortEntry('18', 'וַיַּכְבֵּד',   'Wayyiqtol 3ms',  'Exo 8:32',  '"Pharaoh hardened his heart this time also"',        'F',  'כָּבֵד', 'Qal = be heavy; Hiphil = make/cause heaviness'),
        SortEntry('19', 'וְהַכְבֵּד',   'Inf. Absolute',  'Exo 8:15',  '"he made his heart stubborn" (intensified)',         'F',  'כָּבֵד', 'Inf. Abs. intensifies the factitive action'),
        SortEntry('20', 'וַתַּגְדֵּל',  'Wayyiqtol 2ms',  'Gen 19:19', '"you have shown great kindness to me"',             'F',  'גָּדַל', 'Qal = be great; Hiphil = cause greatness'),
        SortEntry('21', 'הִרְשִׁיעוּ', 'Perfect 3cp',    'Deu 25:1',  '"acquit the innocent and condemn the guilty"',       'D',  'רָשָׁע', 'Legal verdict; declaring — not causing — guilt'),
        SortEntry('22', 'יַרְשִׁיעֻ',  'Imperfect 3mp',  'Exo 22:8',  '"the judges shall declare him guilty"',              'D',  'רָשָׁע', 'Same root; judicial pronouncement'),
        SortEntry('23', 'וַיַּעַל',      'Wayyiqtol 3ms',  'Gen 8:20',  '"Noah offered burnt offerings on the altar"',        'C',  'עָלָה',  'Qal = go up; Hiphil = cause to go up/offer'),
        SortEntry('24', 'הָמִית',        'Inf. Constr.',   'Gen 37:18', '"they conspired against him to kill him"',           'C',  'מוּת',   'Same form as #14; different context'),
        SortEntry('25', 'מַמְטִיר',    'Participle ms',  'Gen 7:4',   '"I am about to send rain on the earth"',             'DN', 'מָטַר',  'Noun: מָטָר (rain); Hiphil = to cause rain / send rain'),
        SortEntry('26', 'וַיַּשְׁכֵּם', 'Wayyiqtol 3ms',  'Gen 22:3',  '"Abraham rose early in the morning"',               'DN', 'שָׁכַם', 'Noun: שְׁכֶם (shoulder); to shoulder up = rise early'),
        SortEntry('27', 'הַאְזִינוּ', 'Imperative 2mp', 'Deu 32:1',  '"give ear, O heavens, and I will speak"',           'DN', 'אָזַן',  'Noun: אֹזֶן (ear); to ear = give ear / listen'),
    ]

    def _build(self) -> None:
        self.add_instructions(
            'Classify each Hiphil verb as C (Causative), F (Factitive), D (Declarative), '
            'SA (Simple Action), or DN (Denominative). Write your answer in the Function column. '
            'Answer key is on the last page.'
        )

        self.add_note(
            'C = Causative (subject causes another to act/experience)  |  '
            'F = Factitive (subject causes object to be in a state)  |  '
            'D = Declarative (subject declares something as being in a state)  |  '
            'SA = Simple Action (Hiphil is the standard form; no common Qal)  |  '
            'DN = Denominative (Hiphil derived from a noun; not in BBH)'
        )

        self.add_sort_table(self._ENTRIES, show_answers=False)

        self.add_reflection([
            'Items 18–19 both come from the root for "be heavy" (Exo 8). How does the Hiphil meaning '
            'connect to the Qal? Is this Factitive or Causative — and why?',
            'Items 21–22 are both Declarative (not Factitive), even though רָשָׁע has a clear stative '
            'Qal. What is the difference between making someone wicked and declaring someone wicked? '
            'What makes Deu 25:1 and Exo 22:8 clearly Declarative?',
            'Items 12–13 (זָכַר, "to remember") are classified as Causative. How does "mention me to '
            'Pharaoh" (Gen 40:14) fit the Causative definition? Does that reading change the translation?',
        ])

        self.add_answer_key_sort(self._ENTRIES)


def build_ch26_function_sort_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch26FunctionSortExercise,
        'Chapter 26 — Semantic Function Sorting',
        'BBH Chapter 26 · Hiphil Strong Verbs',
        ['hebrew', 'bbh', 'ch26', 'exercises', 'ch26-function-sort'],
        'ch26-function-sort.pdf',
        out_dir,
    )


def build_ch26_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch26Exercise,
        'Chapter 26 — "Spot the Hiphil" Passage Exercise',
        'Genesis 6–8  ·  Genesis 22  ·  Deuteronomy 7',
        ['hebrew', 'bbh', 'ch26', 'exercises', 'ch26-passage-exercise'],
        'ch26-passage-exercise.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 26 — Qal / Niphal / Hiphil Stem Identification Drill (Strong Roots)
# ---------------------------------------------------------------------------
_CH26_STEM_ROWS = [
    ['1',  'קָטַל',      '',  '',            '',    ''],
    ['2',  'הִקְטִיל',   '',  '',            '',    ''],
    ['3',  'נִקְטַל',    '',  '',            '',    ''],
    ['4',  'שָׁמַר',     '',  '',            '',    ''],
    ['5',  'הִשְׁמִיד',  '',  '',            '',    ''],
    ['6',  'נִשְׁמַר',   '',  '',            '',    ''],
    ['7',  'כָּתַב',     '',  '',            '',    ''],
    ['8',  'הִכְבִּיד',  '',  '',            '',    ''],
    ['9',  'נִכְתַּב',   '',  '',            '',    ''],
    ['10', 'יִשְׁמֹר',   '',  '',            '',    ''],
    ['11', 'יַכְבִּיד',  '',  '',            '',    ''],
    ['12', 'יִשָּׁמֵר',  '',  '',            '',    ''],
    ['13', 'וַיִּשְׁמֹר', '', '',           '',    ''],
    ['14', 'וַיַּכְבֵּד', '', '',           '',    ''],
    ['15', 'וַיִּשָּׁמֵר', '', '',          '',    ''],
    ['16', 'שְׁמֹר',     '',  '',            '',    ''],
    ['17', 'הַכְבֵּד',   '',  '',            '',    ''],
    ['18', 'הִשָּׁמֵר',  '',  '',            '',    ''],
    ['19', 'שָׁמוֹר',    '',  '',            '',    ''],
    ['20', 'הַכְבֵּד',   '',  '',            '',    ''],
    ['21', 'הִשָּׁמֵר',  '',  '',            '',    ''],
    ['22', 'שֹׁמֵר',     '',  '',            '',    ''],
    ['23', 'מַכְבִּיד',  '',  '',            '',    ''],
    ['24', 'נִשְׁמָר',   '',  '',            '',    ''],
]
_CH26_STEM_ANS = [
    ['1',  'קָטַל',      'Qal',    'Perfect',      '3ms', 'קטל'],
    ['2',  'הִקְטִיל',   'Hiphil', 'Perfect',      '3ms', 'קטל'],
    ['3',  'נִקְטַל',    'Niphal', 'Perfect',      '3ms', 'קטל'],
    ['4',  'שָׁמַר',     'Qal',    'Perfect',      '3ms', 'שׁמר'],
    ['5',  'הִשְׁמִיד',  'Hiphil', 'Perfect',      '3ms', 'שׁמד'],
    ['6',  'נִשְׁמַר',   'Niphal', 'Perfect',      '3ms', 'שׁמר'],
    ['7',  'כָּתַב',     'Qal',    'Perfect',      '3ms', 'כתב'],
    ['8',  'הִכְבִּיד',  'Hiphil', 'Perfect',      '3ms', 'כבד'],
    ['9',  'נִכְתַּב',   'Niphal', 'Perfect',      '3ms', 'כתב'],
    ['10', 'יִשְׁמֹר',   'Qal',    'Imperfect',    '3ms', 'שׁמר'],
    ['11', 'יַכְבִּיד',  'Hiphil', 'Imperfect',    '3ms', 'כבד'],
    ['12', 'יִשָּׁמֵר',  'Niphal', 'Imperfect',    '3ms', 'שׁמר'],
    ['13', 'וַיִּשְׁמֹר', 'Qal',   'Wayyiqtol',   '3ms', 'שׁמר'],
    ['14', 'וַיַּכְבֵּד', 'Hiphil','Wayyiqtol',   '3ms', 'כבד'],
    ['15', 'וַיִּשָּׁמֵר', 'Niphal','Wayyiqtol',  '3ms', 'שׁמר'],
    ['16', 'שְׁמֹר',     'Qal',    'Imperative',   '2ms', 'שׁמר'],
    ['17', 'הַכְבֵּד',   'Hiphil', 'Imperative',   '2ms', 'כבד'],
    ['18', 'הִשָּׁמֵר',  'Niphal', 'Imperative',   '2ms', 'שׁמר'],
    ['19', 'שָׁמוֹר',    'Qal',    'Inf. Absolute', '—',  'שׁמר'],
    ['20', 'הַכְבֵּד',   'Hiphil', 'Inf. Absolute', '—',  'כבד'],
    ['21', 'הִשָּׁמֵר',  'Niphal', 'Inf. Absolute', '—',  'שׁמר'],
    ['22', 'שֹׁמֵר',     'Qal',    'Participle',   'ms',  'שׁמר'],
    ['23', 'מַכְבִּיד',  'Hiphil', 'Participle',   'ms',  'כבד'],
    ['24', 'נִשְׁמָר',   'Niphal', 'Participle',   'ms',  'שׁמר'],
]


class Ch26StemIdDrill(ExercisePDF):
    _instructions = (
        'For each verb form, identify the stem (Qal / Niphal / Hiphil), '
        'then fill in the conjugation, PGN (person–gender–number), and root. '
        'All 24 forms are from strong roots. '
        'Non-finite forms (Inf. Absolute, Participle): enter — in PGN, or note gender for participles.'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'Hebrew Form', 'Stem', 'Conjugation', 'PGN', 'Root']
        cr   = [0.05, 0.18, 0.15, 0.22, 0.15, 0.25]
        self.add_drill_with_answer_key(
            hdrs, _CH26_STEM_ROWS, _CH26_STEM_ANS,
            col_ratios=cr,
            heb_cols=[1],
            answer_heb_cols=[5],
            section_title='Qal / Niphal / Hiphil — Strong Roots',
        )


def build_ch26_stem_id_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch26StemIdDrill,
        'Chapter 26 — Qal / Niphal / Hiphil Stem Identification Drill',
        'BBH Chapter 26 · Hiphil Strong Verbs',
        ['hebrew', 'bbh', 'ch26', 'exercises', 'ch26-stem-id-drill'],
        'ch26-stem-id-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 25 — "Spot the Niphal" Passage Exercise
# ---------------------------------------------------------------------------


class Ch25Exercise(PassageExercise):
    _instructions = (
        'Most highlighted verbs are Niphal forms. For each one, first answer '
        'Is it Niphal? (Yes / No). If Yes: parse conjugation, PGN, and root, '
        'then state the semantic function (Passive / Reflexive / Middle / Simple Action). '
        'If No: identify the correct stem and parse fully. '
        'Three verbs in this exercise are not Niphal — drawn from Qal already studied. '
        'Answer key begins on the page marked "Answer Key".'
    )

    def _render_passages(self, show_answers: bool) -> None:

        # ── Passage A ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage A — Genesis 3:5–10')

        self.add_passage(PassageBlock('3:5',
            'וִֽהְיִיתֶם֙ כֵּֽאלֹהִ֔ים יֹדְעֵ֖י טוֹב וָרָ֑ע כִּ֣י יֹדֵ֔עַ אֱלֹהִ֕ים כִּ֗י בְּיֹ֛ום אֲכָלְכֶ֥ם מִמֶּ֖נּוּ וְנִפְקְח֖וּ עֵינֵיכֶ֑ם',
            '"…for God knows that in the day you eat of it your eyes will [1] ____."'))
        self.add_verb_table([VerbEntry('1', 'וְנִפְקְחוּ', 'Weqatal', '3cp', 'פָּקַח', 'Middle — will be opened')], show_answers=show_answers)

        self.add_passage(PassageBlock('3:6',
            'וַתֵּרֶא הָאִשָּׁה כִּי טוֹב הָעֵץ … וְנֶחְמָ֤ד הָעֵץ֙ לְהַשְׂכִּ֔יל',
            '"So when the woman [2] ____ that the tree was good … and the tree was [3] ____ to make one wise."'))
        self.add_verb_table([
            VerbEntry('2', 'וַתֵּרֶא', 'Wayyiqtol', '3fs', 'רָאָה', 'NOT Niphal — Qal: and she saw; III-ה Qal wayyiqtol; no נ-/תִ- Niphal marker'),
            VerbEntry('3', 'וְנֶחְמָד', 'Participle ms', 'ms', 'חָמַד', 'Passive — desirable (substantival ptc.)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('3:7',
            'וַתִּפָּקַ֙חְנָה֙ עֵינֵ֣י שְׁנֵיהֶ֔ם',
            '"Then the eyes of both of them [4] ____."'))
        self.add_verb_table([VerbEntry('4', 'וַתִּפָּקַחְנָה', 'Wayyiqtol', '3fp', 'פָּקַח', 'Middle — they were opened')], show_answers=show_answers)

        self.add_passage(PassageBlock('3:10',
            'וָאִירָ֛א כִּֽי־עֵירֹ֥ם אָנֹ֖כִי וָאֵחָבֵֽא',
            '"I was afraid, because I was naked, and [5] ____."'))
        self.add_verb_table([VerbEntry('5', 'וָאֵחָבֵא', 'Wayyiqtol', '1cs', 'חָבָא', 'Reflexive — I hid myself')], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage B — Genesis 6:6–12')

        self.add_passage(PassageBlock('6:6',
            'וַיִּנָּ֣חֶם יְהוָ֔ה כִּֽי־עָשָׂ֥ה אֶת־הָאָדָ֖ם בָּאָ֑רֶץ',
            '"And the LORD [6] ____ that he [7] ____ man on the earth."'))
        self.add_verb_table([
            VerbEntry('6', 'וַיִּנָּחֶם', 'Wayyiqtol', '3ms', 'נָחַם', 'Simple Action (Niphal-only) — relented'),
            VerbEntry('7', 'עָשָׂה', 'Perfect', '3ms', 'עָשָׂה', 'NOT Niphal — Qal: he made/did; III-ה Qal perfect; contrast Niphal וַיִּנָּחֶם earlier in the verse'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('6:7',
            'נִחַ֖מְתִּי כִּ֥י עֲשִׂיתִֽם',
            '"I [8] ____ that I made them."'))
        self.add_verb_table([VerbEntry('8', 'נִחַמְתִּי', 'Weqatal', '1cs', 'נָחַם', 'Simple Action (Niphal-only) — I regret')], show_answers=show_answers)

        self.add_passage(PassageBlock('6:11',
            'וַתִּשָּׁחֵ֥ת הָאָ֖רֶץ … וַתִּמָּלֵ֥א הָאָ֖רֶץ חָמָֽס',
            '"The earth [9] ____ … and the earth [10] ____ with violence."'))
        self.add_verb_table([
            VerbEntry('9', 'וַתִּשָּׁחֵת', 'Wayyiqtol', '3fs', 'שָׁחַת', 'Passive — it was corrupted'),
            VerbEntry('10', 'וַתִּמָּלֵא', 'Wayyiqtol', '3fs', 'מָלֵא', 'Passive — it was filled'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('6:12',
            'וְהִנֵּ֥ה נִשְׁחָ֑תָה כִּֽי־הִשְׁחִ֧ית כָּל־בָּשָׂ֛ר',
            '"and behold, it [11] ____, for all flesh had corrupted its way."'))
        self.add_verb_table([VerbEntry('11', 'נִשְׁחָתָה', 'Weqatal', '3fs', 'שָׁחַת', 'Passive — it was corrupt')], show_answers=show_answers)

        self.add_passage(PassageBlock('6:21',
            'וְהָיָ֥ה לְךָ֖ וְלָהֶ֥ם לְאָכְלָֽה יֵֽאָכֵ֔ל',
            '"it shall be food for you and for them — it shall [12] ____."'))
        self.add_verb_table([VerbEntry('12', 'יֵאָכֵל', 'Imperfect', '3ms', 'אָכַל', 'Passive — it shall be eaten')], show_answers=show_answers)

        self.add_section_break()

        # ── Passage C ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage C — Genesis 21:23–31')

        self.add_passage(PassageBlock('21:23',
            'הִשָּׁ֨בְעָ֜ה לִּ֗י בֵּאלֹהִ֛ים הֵ֖נָּה',
            '"[13] ____ to me by God here."'))
        self.add_verb_table([VerbEntry('13', 'הִשָּׁבְעָה', 'Imperative', '2ms', 'שָׁבַע', 'Reflexive — Swear! (bind yourself by oath)')], show_answers=show_answers)

        self.add_passage(PassageBlock('21:24',
            'וַיֹּ֙אמֶר֙ אַבְרָהָ֔ם אָנֹכִ֖י אִשָּׁבֵֽעַ',
            '"And Abraham said, \'I [14] ____.\'"'))
        self.add_verb_table([VerbEntry('14', 'אִשָּׁבֵעַ', 'Imperfect', '1cs', 'שָׁבַע', 'Reflexive — I will swear')], show_answers=show_answers)

        self.add_passage(PassageBlock('21:31',
            'כִּ֛י שָׁ֥ם נִשְׁבְּע֖וּ שְׁנֵיהֶֽם',
            '"For there [15] ____ both of them."'))
        self.add_verb_table([VerbEntry('15', 'נִשְׁבְּעוּ', 'Weqatal', '3mp', 'שָׁבַע', 'Reflexive — they swore (bound themselves by oath)')], show_answers=show_answers)

        self.add_section_break()

        # ── Bonus ─────────────────────────────────────────────────────────────
        self.add_section_heading('Bonus — Genesis 21:3, 21:8')

        self.add_passage(PassageBlock('21:3', 'אֲשֶׁר־נּֽוֹלַד־לֹ֛ו', '"who had been born to him"'))
        self.add_passage(PassageBlock('21:8', 'וַיִּגְדַּ֤ל הַיֶּ֙לֶד֙ וַיִּגָּמַ֑ל', '"And the child [16] ____ and was weaned."'))
        self.add_verb_table([
            VerbEntry('B1', 'נּוֹלַד',  'Weqatal',   '3ms', 'יָלַד', 'Passive — who had been born'),
            VerbEntry('16', 'וַיִּגְדַּל', 'Wayyiqtol', '3ms', 'גָּדַל', 'NOT Niphal — Qal: and he grew; plain Qal wayyiqtol; contrast Niphal וַיִּגָּמַל in same verse'),
            VerbEntry('B2', 'וַיִּגָּמַל', 'Wayyiqtol', '3ms', 'גָּמַל', 'Passive — was weaned'),
        ], show_answers=show_answers)

        self.add_section_break()

        self.add_note(
            'Items 6–8 (וַיִּנָּחֶם / נִחַמְתִּי) are both from נָחַם, a verb that occurs almost exclusively '
            'in the Niphal. Items 13–15 all parse as Reflexive from שָׁבַע — '
            'notice how Imperative, Imperfect, and Weqatal all express the same oath-swearing action.'
        )
        self.add_score(
            'Score: 13 Niphal + 3 non-Niphal + 2 bonus = 18 total.  '
            '15–18 = excellent  |  11–14 = review the paradigm  |  below 11 = revisit §23.3–23.13'
        )

        self.add_section_heading('Conjugation Coverage')
        self.add_coverage_table([
            ('Wayyiqtol (6)',   '#4, #5, #6, #9, #10, B2'),
            ('Weqatal (5)',     '#1, #8, #11, #15, B1'),
            ('Imperfect (2)',   '#12, #14'),
            ('Participle (1)',  '#3'),
            ('Imperative (1)',  '#13'),
            ('Non-Niphal (3)',  '#2 (Qal Wayyiqtol 3fs), #7 (Qal Perfect 3ms), #16 (Qal Wayyiqtol 3ms)'),
        ])

        if not show_answers:
            self.add_reflection([
                'Every Niphal in Passage A (Gen 3) involves eyes, hiding, or desire. What does the '
                'Niphal contribute to the theological message of the Fall narrative?',
                'In Gen 6:6–7, God is the subject of a Niphal-only verb (נָחַם). What does this choice '
                'tell us about how the narrator portrays God\'s emotional response?',
                'Compare Gen 3:5 (וְנִפְקְחוּ — "will be opened," Middle/Tolerative) with Gen 3:7 '
                '(וַתִּפָּקַחְנָה — "were opened," Middle). Is the function identical in both? '
                'What difference in nuance, if any, does the shift from weqatal to wayyiqtol suggest?',
            ])


def build_ch25_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch25Exercise,
        'Chapter 25 — "Spot the Niphal" Passage Exercise',
        'Genesis 3, 6, and 21  ·  The Garden, the Flood Prelude, and Beersheba',
        ['hebrew', 'bbh', 'ch25', 'exercises', 'ch25-passage-exercise'],
        'ch25-passage-exercise.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 24 — "Spot the Niphal" Passage Exercise
# ---------------------------------------------------------------------------


class Ch24Exercise(PassageExercise):
    _instructions = (
        'Most highlighted verbs are Niphal forms. For each one, first answer '
        'Is it Niphal? (Yes / No). If Yes: parse conjugation, PGN, and root, '
        'then state the semantic function (Passive / Reflexive / Simple Action). '
        'If No: identify the correct stem and parse fully. '
        'Three verbs in this exercise are not Niphal — drawn from Qal already studied. '
        'Answer key begins on the page marked "Answer Key".'
    )

    def _render_passages(self, show_answers: bool) -> None:

        # ── Passage A ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage A — Genesis 37:7, 36')

        self.add_passage(PassageBlock('37:7',
            'וְהִנֵּה קָמָה אֲלֻמָּתִי וְגַם נִצָּבָה',
            '"and behold, my sheaf [1] ____ and [2] ____."'))
        self.add_verb_table([
            VerbEntry('1', 'קָמָה', 'Perfect', '3fs', 'קוּם', 'NOT Niphal — Qal: she/it arose (no נ- prefix; plain Qal of hollow verb)'),
            VerbEntry('2', 'נִצָּבָה', 'Perfect', '3fs', 'נָצַב', 'Reflexive — it stood upright (stationed itself)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('37:36',
            'וְהַמְּדָנִים מָכְרוּ אֹתוֹ … וַיִּמָּכֵר יוֹסֵף אֶל־מִצְרָיִם',
            '"Now the Midianites [3] ____ him … and Joseph [4] ____ into Egypt."'))
        self.add_verb_table([
            VerbEntry('3', 'מָכְרוּ', 'Perfect', '3cp', 'מָכַר', 'NOT Niphal — Qal: they sold; no נִ- prefix; contrast with Niphal וַיִּמָּכֵר in same verse'),
            VerbEntry('4', 'וַיִּמָּכֵר', 'Wayyiqtol', '3ms', 'מָכַר', 'Passive — he was sold'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage B — Genesis 44:9–20')

        self.add_passage(PassageBlock('44:9',
            'אֲשֶׁר יִמָּצֵא אִתּוֹ מֵעֲבָדֶיךָ וָמֵת',
            '"With whichever of your servants [5] ____ [the cup] shall die."'))
        self.add_verb_table([VerbEntry('5', 'יִמָּצֵא', 'Imperfect', '3ms', 'מָצָא', 'Passive — is found')], show_answers=show_answers)

        self.add_passage(PassageBlock('44:12',
            'וַיִּמָּצֵא הַגָּבִיעַ בְּאַמְתַּחַת בִּנְיָמִן',
            '"And the cup [6] ____ in Benjamin\'s sack."'))
        self.add_verb_table([VerbEntry('6', 'וַיִּמָּצֵא', 'Wayyiqtol', '3ms', 'מָצָא', 'Passive — was found')], show_answers=show_answers)

        self.add_passage(PassageBlock('44:20',
            'יֶשׁ לָנוּ אָב זָקֵן וְיֶלֶד זְקֻנִים קָטָן וְאָחִיו מֵת וַיִּוָּתֵר הוּא',
            '"We have an aged father … his brother is dead, and he alone [7] ____."'))
        self.add_verb_table([VerbEntry('7', 'וַיִּוָּתֵר', 'Wayyiqtol', '3ms', 'יָתַר', 'Passive/Middle — was left, remained')], show_answers=show_answers)

        self.add_section_break()

        # ── Passage C ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage C — Genesis 45:1, 16')

        self.add_passage(PassageBlock('45:1',
            'וְלֹא־יָכֹל יוֹסֵף לְהִתְאַפֵּק לְכֹל הַנִּצָּבִים עָלָיו',
            '"Joseph [8] ____ no longer control himself before all those [9] ____ near him."'))
        self.add_verb_table([
            VerbEntry('8', 'יָכֹל', 'Perfect', '3ms', 'יָכֹל', 'NOT Niphal — Qal: he was able; Qal-only verb; לֹא יָכֹל = could not'),
            VerbEntry('9', 'הַנִּצָּבִים', 'Participle', 'mp', 'נָצַב', 'Reflexive — those standing (stationed themselves)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('45:16',
            'וְהַקֹּל נִשְׁמַע בֵּית פַּרְעֹה לֵאמֹר בָּאוּ אֲחֵי־יוֹסֵף',
            '"And the report [10] ____ in Pharaoh\'s household, \'Joseph\'s brothers have come.\'"'))
        self.add_verb_table([VerbEntry('10', 'נִשְׁמַע', 'Perfect', '3ms', 'שָׁמַע', 'Passive — was heard')], show_answers=show_answers)

        self.add_section_break()

        # ── Passage D ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage D — Genesis 47:14, 31')

        self.add_passage(PassageBlock('47:14',
            'וַיְלַקֵּט יוֹסֵף אֶת־כָּל־הַכֶּסֶף הַנִּמְצָא בְאֶרֶץ־מִצְרַיִם',
            '"And Joseph collected all the silver [11] ____ in the land of Egypt."'))
        self.add_verb_table([VerbEntry('11', 'הַנִּמְצָא', 'Participle', 'ms', 'מָצָא', 'Passive — that was found')], show_answers=show_answers)

        self.add_passage(PassageBlock('47:31',
            'הִשָּׁבְעָה לִי וַיִּשָּׁבַע לוֹ',
            '"[12] ____ to me." And he [13] ____ to him."'))
        self.add_verb_table([
            VerbEntry('12', 'הִשָּׁבְעָה', 'Imperative', '2ms', 'שָׁבַע', 'Reflexive — swear! (bind yourself by oath)'),
            VerbEntry('13', 'וַיִּשָּׁבַע', 'Wayyiqtol', '3ms', 'שָׁבַע', 'Reflexive — he swore (bound himself by oath)'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage E ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage E — Genesis 49:1, 29, 33')

        self.add_passage(PassageBlock('49:1',
            'הֵאָסְפוּ וְאַגִּידָה לָכֶם',
            '"[14] ____ and I will tell you."'))
        self.add_verb_table([VerbEntry('14', 'הֵאָסְפוּ', 'Imperative', '2mp', 'אָסַף', 'Passive — gather yourselves!')], show_answers=show_answers)

        self.add_passage(PassageBlock('49:29',
            'אֲנִי נֶאֱסָף אֶל־עַמִּי',
            '"I am [15] ____ to my people."'))
        self.add_verb_table([VerbEntry('15', 'נֶאֱסָף', 'Participle', 'ms', 'אָסַף', 'Passive — am about to be gathered (die)')], show_answers=show_answers)

        self.add_passage(PassageBlock('49:33',
            'וַיֵּאָסֶף אֶל־עַמָּיו',
            '"and he was [16] ____ to his people."'))
        self.add_verb_table([VerbEntry('16', 'וַיֵּאָסֶף', 'Wayyiqtol', '3ms', 'אָסַף', 'Passive — was gathered (died)')], show_answers=show_answers)

        self.add_section_break()

        # ── Bonus ─────────────────────────────────────────────────────────────
        self.add_section_heading('Bonus — Exodus 19:12')

        self.add_passage(PassageBlock('19:12',
            'וְהִשָּׁמַרְתֶּם … הִשָּׁמְרוּ לָכֶם',
            '"And you shall [B1] ____ … [B2] ____ for yourselves."'))
        self.add_verb_table([
            VerbEntry('B1', 'וְהִשָּׁמַרְתֶּם', 'Weqatal',   '2mp', 'שָׁמַר', 'Reflexive — take heed for yourselves'),
            VerbEntry('B2', 'הִשָּׁמְרוּ',      'Imperative', '2mp', 'שָׁמַר', 'Reflexive — take heed! (guard yourselves)'),
        ], show_answers=show_answers)

        self.add_section_break()

        self.add_note(
            'Items 15–16 (נֶאֱסָף / וַיֵּאָסֶף) are both from אָסַף — the euphemism "gathered to '
            'one\'s people" means death. Items 12–13 both parse as Reflexive from שָׁבַע — '
            'notice Imperative followed by Wayyiqtol in the same verse (Gen 47:31).'
        )
        self.add_score(
            'Score: 13 Niphal + 3 non-Niphal + 2 bonus = 18 total.  '
            '15–18 = excellent  |  11–14 = review the paradigm  |  below 11 = revisit §24.3–24.13'
        )

        self.add_section_heading('Conjugation Coverage')
        self.add_coverage_table([
            ('Wayyiqtol (5)',   '#4, #6, #7, #13, #16'),
            ('Participle (3)',  '#9, #11, #15'),
            ('Imperfect (1)',   '#5'),
            ('Perfect (2)',     '#2, #10'),
            ('Imperative (3)',  '#12, #14, B2'),
            ('Weqatal (1)',     'B1'),
            ('Non-Niphal (3)',  '#1 (Qal Perf 3fs), #3 (Qal Perf 3cp), #8 (Qal Perf 3ms)'),
        ])

        if not show_answers:
            self.add_reflection([
                'Several Niphal forms of אָסַף in this passage describe Jacob\'s death (Gen 49:29, 33). '
                'What does the passive "to be gathered to one\'s people" suggest about ancient Israelite '
                'views of death?',
                'In Gen 47:31, both הִשָּׁ֣בְעָה (imperative) and וַיִּשָּׁבַע (wayyiqtol) appear together. '
                'How does the narrative sequence reinforce the solemnity of Jacob\'s deathbed request?',
                'Compare נִצָּבָה in Gen 37:7 (Reflexive — sheaf stands itself upright) with הַנִּצָּבִים '
                'in Gen 45:1 (Reflexive participle — servants stationed before Joseph). Is the reflexive '
                'force the same in both? What does each communicate about agency?',
            ])


def build_ch24_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch24Exercise,
        'Chapter 24 — "Spot the Niphal" Passage Exercise',
        'Genesis 37, 44, 45, 47, 49  ·  The Joseph Narrative',
        ['hebrew', 'bbh', 'ch24', 'exercises', 'ch24-passage-exercise'],
        'ch24-passage-exercise.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 24 — Qal–Niphal Contrast Drill
# ---------------------------------------------------------------------------


class Ch24ContrastExercise(ExercisePDF):

    _ENTRIES_A = [
        ContrastEntry('1',  'מָכַר', 'to sell',            'וַיִּמָּכֵר',      'Wayyiqtol 3ms',  'Gen 37:36', 'he was sold into Egypt',         'Passive',       'The object of selling (Joseph) becomes the subject'),
        ContrastEntry('2',  'מָצָא', 'to find',            'יִמָּצֵא',         'Imperfect 3ms',  'Gen 44:9',  'is found (with the cup)',         'Passive',       'The thing found becomes the subject; finder absent'),
        ContrastEntry('3',  'שָׁמַע', 'to hear',           'נִשְׁמַע',         'Perfect 3ms',    'Gen 45:16', 'was heard (in Pharaoh\'s house)', 'Passive',       'The report receives the hearing — it becomes audible'),
        ContrastEntry('4',  'אָסַף', 'to gather',          'וַיֵּאָסֶף',       'Wayyiqtol 3ms',  'Gen 49:33', 'was gathered to his people',      'Passive',       'Jacob receives the action of being gathered in (die)'),
        ContrastEntry('5',  'כָּרַת', 'to cut off',        'וְנִכְרְתָה',      'Weqatal 3fs',    'Exo 12:15', 'will be cut off from Israel',     'Passive',       'The person receives covenant-exclusion penalty'),
        ContrastEntry('6',  'נָתַן', 'to give',            'נִתְּנוּ',         'Perfect 3mp',    'Gen 9:2',   'they are given into your hand',   'Passive',       'Animals receive the action of being given/placed'),
        ContrastEntry('7',  'אָכַל', 'to eat',             'יֵאָכֵל',          'Imperfect 3ms',  'Exo 12:46', 'it shall be eaten',               'Passive',       'Passover lamb receives the action of eating'),
        ContrastEntry('8',  'שָׁמַר', 'to keep / guard',  'הִשָּׁמְרוּ',      'Imperative 2mp', 'Exo 19:12', 'take heed for yourselves!',       'Reflexive',     'Guard yourself — subject directs action back on itself'),
    ]
    _ENTRIES_B = [
        ContrastEntry('9',  'נָצַב', 'to be stationed',    'נִצָּבָה',         'Perfect 3fs',    'Gen 37:7',  'it stood upright',                'Reflexive',     'The sheaf stations itself in the standing position'),
        ContrastEntry('10', 'יָתַר', 'to remain',          'וַיִּוָּתֵר',      'Wayyiqtol 3ms',  'Gen 44:20', 'he alone was left',               'Passive/Middle', 'State of being-left fell upon him; middle nuance'),
        ContrastEntry('11', 'שָׁאַר', 'to remain',         'נִשְׁאַר',         'Perfect 3ms',    'Exo 14:28', 'not one of them remained',        'Middle',        'Soldiers were in the state of having been left'),
    ]
    _ENTRIES_C = [
        ContrastEntry('12', 'לָחַם', 'no standard Qal',    'הִלָּחֵם',         'Imperative 2ms', 'Exo 17:9',  'fight against Amalek!',           'Simple action', 'Niphal is the base form; no causative layer'),
        ContrastEntry('13', 'נָחַם', 'no standard Qal',    'וַיִּנָּחֶם',      'Wayyiqtol 3ms',  'Gen 6:6',   'the LORD regretted / relented',   'Simple action', 'Niphal is the base form; to regret/relent/be comforted'),
        ContrastEntry('14', 'שָׁבַע', 'to seven/complete', 'הִשָּׁבְעָה',      'Imperative 2ms', 'Gen 47:31', 'swear to me!',                    'Reflexive',     'Bind yourself by oath; reflexive oath-taking'),
    ]

    def _build(self) -> None:
        self.add_instructions(
            'For each item: (1) write an English translation of the Niphal form in the Translation '
            'column; (2) write the semantic function (Passive / Reflexive / Simple Action) in the '
            'Function column. Answer key is on the last page.'
        )

        self.add_section_heading('Part A — Transitive Roots (Qal acts on an object)')
        self.add_note('These roots take a direct object in the Qal. The Niphal turns the object into the subject — the classic passive pattern.')
        self.add_contrast_table(self._ENTRIES_A, show_answers=False)

        self.add_section_heading('Part B — Stative / Intransitive Roots')
        self.add_note('These roots describe states. Their Niphal expresses the subject coming into or remaining in a state.')
        self.add_contrast_table(self._ENTRIES_B, show_answers=False)

        self.add_section_heading('Part C — Roots with No Standard Qal')
        self.add_note('These roots occur almost exclusively in the Niphal. The Niphal form is the standard lexical entry.')
        self.add_contrast_table(self._ENTRIES_C, show_answers=False)

        self.add_reflection([
            'For the transitive roots in Part A, describe the pattern in one sentence: what does the '
            'Niphal consistently do to the Qal meaning?',
            'Items 9–11 all involve verbs of position or remaining (נָצַב, יָתַר, שָׁאַר). How does '
            '"reflexive" vs. "middle" vs. "passive" help explain the subtle difference in agency?',
            'לָחַם (item 12) and נָחַם (item 13) are both "lexical Niphal" roots. How does a student '
            'recognize this? What should they look for in a dictionary entry?',
        ])

        self.add_answer_key_contrast(self._ENTRIES_A + self._ENTRIES_B + self._ENTRIES_C)


def build_ch24_contrast_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch24ContrastExercise,
        'Chapter 24 — Qal–Niphal Contrast Drill',
        'BBH Chapter 24 · Niphal Strong Verbs',
        ['hebrew', 'bbh', 'ch24', 'exercises', 'ch24-qal-niphal-contrast'],
        'ch24-qal-niphal-contrast.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 24 — Semantic Function Sorting
# ---------------------------------------------------------------------------


class Ch24FunctionSortExercise(ExercisePDF):

    _ENTRIES = [
        SortEntry('1',  'וַיִּמָּכֵר',      'Wayyiqtol 3ms',  'Gen 37:36', '"and Joseph was sold into Egypt"',              'P',  'מָכַר',  'Joseph receives the action of being sold'),
        SortEntry('2',  'נִצָּבָה',         'Perfect 3fs',    'Gen 37:7',  '"my sheaf stood upright"',                      'R',  'נָצַב',  'Sheaf stations itself (acts on itself)'),
        SortEntry('3',  'וַיִּנָּחֶם',      'Wayyiqtol 3ms',  'Gen 6:6',   '"the LORD regretted"',                          'SA', 'נָחַם',  'Niphal-only: no standard Qal; to regret/relent'),
        SortEntry('4',  'יֵאָכֵל',          'Imperfect 3ms',  'Exo 12:46', '"it shall be eaten"',                           'P',  'אָכַל',  'Passover lamb receives the action of eating'),
        SortEntry('5',  'הִשָּׁמְרוּ',      'Imperative 2mp', 'Exo 19:12', '"take heed for yourselves!"',                   'R',  'שָׁמַר', 'Guard yourself — subject directs action back on self'),
        SortEntry('6',  'נִשְׁמַע',         'Perfect 3ms',    'Gen 45:16', '"the report was heard"',                        'P',  'שָׁמַע', 'Report receives the hearing — it becomes audible'),
        SortEntry('7',  'הִשָּׁבְעָה',      'Imperative 2ms', 'Gen 47:31', '"swear to me!"',                                'R',  'שָׁבַע', 'Bind yourself by oath (reflexive oath-taking)'),
        SortEntry('8',  'הַנִּמְצָא',       'Participle ms',  'Gen 47:14', '"the silver that was found"',                   'P',  'מָצָא',  'Silver was discovered (received the finding action)'),
        SortEntry('9',  'וְנִכְרְתָה',      'Weqatal 3fs',    'Exo 12:15', '"that person will be cut off"',                 'P',  'כָּרַת', 'Person receives covenant-exclusion penalty'),
        SortEntry('10', 'נִצָּבִים',        'Participle mp',  'Exo 5:20',  '"standing before Pharaoh"',                     'R',  'נָצַב',  'Overseers have stationed themselves before Pharaoh'),
        SortEntry('11', 'אִוָּעֵד',         'Imperfect 1cs',  'Exo 29:42', '"I will meet with you there"',                  'RC', 'יָעַד',  'God and Israel meet one another at the tent'),
        SortEntry('12', 'וַיִּשָּׁבַע',     'Wayyiqtol 3ms',  'Gen 47:31', '"and he swore to him"',                         'R',  'שָׁבַע', 'Jacob binds himself by oath at Joseph\'s request'),
        SortEntry('13', 'וַיֵּאָסֶף',       'Wayyiqtol 3ms',  'Gen 49:33', '"and he was gathered to his people"',           'P',  'אָסַף',  'Jacob is gathered in (brought to ancestors — die)'),
        SortEntry('14', 'יִלָּחֵם',         'Imperfect 3ms',  'Exo 14:14', '"the LORD will fight for you"',                 'SA', 'לָחַם',  'Niphal-only: to fight is the base meaning'),
        SortEntry('15', 'נִשְׁבְּעוּ',      'Weqatal 3mp',    'Gen 21:31', '"both of them swore"',                          'R',  'שָׁבַע', 'Each binds himself individually — reflexive, not reciprocal'),
        SortEntry('16', 'תִּכָּרֵת',        'Imperfect 3fs',  'Gen 41:36', '"the land will not be cut off"',                'P',  'כָּרַת', 'Land receives the action of being cut off (depleted)'),
        SortEntry('17', 'נִלְחָם',          'Participle ms',  'Exo 14:25', '"the LORD is fighting for them"',               'SA', 'לָחַם',  'Niphal-only: the LORD fights (no Qal to contrast)'),
        SortEntry('18', 'הֵאָסְפוּ',        'Imperative 2mp', 'Gen 49:1',  '"gather yourselves!"',                          'P',  'אָסַף',  'Passive imperative: be gathered (assemble)'),
        SortEntry('19', 'וְנוֹעֲדוּ',       'Weqatal 3mp',    'Num 10:3',  '"all the congregation shall assemble"',         'RC', 'יָעַד',  'Congregation assembles mutually together'),
        SortEntry('20', 'נִחַמְתִּי',       'Weqatal 1cs',    'Gen 6:7',   '"I regret that I made them"',                   'SA', 'נָחַם',  'Niphal-only: I regret is the base meaning'),
        SortEntry('21', 'נְמַלְתֶּם',       'Weqatal 2mp',    'Gen 17:11', '"you shall be circumcised"',                    'P',  'מוּל',   'Males receive the action of circumcision'),
        SortEntry('22', 'נִצַּבְתָּ',       'Perfect 2ms',    'Exo 7:15',  '"station yourself to meet him"',                'R',  'נָצַב',  'Moses positions himself at the Nile'),
        SortEntry('23', 'לְהִלָּחֵם',       'Inf. Construct', 'Exo 17:10', '"to fight against Amalek"',                     'SA', 'לָחַם',  'Niphal-only: to fight — the inf. construct form'),
        SortEntry('24', 'יִמָּצֵא',         'Imperfect 3ms',  'Gen 44:9',  '"whoever is found [with the cup]"',             'P',  'מָצָא',  'Person discovered with cup — receives the finding'),
        SortEntry('25', 'הִמָּצֵא יִמָּצֵא', 'Inf. Abs. + Impl', 'Exo 22:3', '"if it is actually found in his possession"',  'P',  'מָצָא',  'Emphatic passive; doubling stresses the discovery'),
    ]

    def _build(self) -> None:
        self.add_instructions(
            'Classify each Niphal verb as P (Passive), R (Reflexive), RC (Reciprocal), '
            'or SA (Simple Action). Write your answer in the Function column. '
            'Answer key is on the last page.'
        )

        self.add_note(
            'P = Passive (subject receives the action)  |  '
            'R = Reflexive (subject acts on/for itself)  |  '
            'RC = Reciprocal (subjects act on one another)  |  '
            'SA = Simple Action (Niphal-only root; no distinct Qal meaning)'
        )

        self.add_sort_table(self._ENTRIES, show_answers=False)

        self.add_reflection([
            'Items 3, 14, 17, 20, and 23 are all Simple Action (לָחַם and נָחַם). What is the practical '
            'difference between a Niphal-only root and a root that simply lacks a Qal in the OT corpus?',
            'Compare items 7 and 12 (both שָׁבַע). The imperative and wayyiqtol appear in the same verse '
            '(Gen 47:31). How does the sequential narrative create a scene of formal oath-taking?',
            'Item 18 (הֵאָסְפוּ) is Passive, yet it is an imperative. Explain how a Niphal imperative '
            'can be both a command and passive in force.',
        ])

        self.add_answer_key_sort(self._ENTRIES)


def build_ch24_function_sort_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch24FunctionSortExercise,
        'Chapter 24 — Semantic Function Sorting',
        'BBH Chapter 24 · Niphal Strong Verbs',
        ['hebrew', 'bbh', 'ch24', 'exercises', 'ch24-function-sort'],
        'ch24-function-sort.pdf',
        out_dir,
    )


class Ch25WeakFormIdExercise(ExercisePDF):
    """Weak-Form Identification Drill — 52 items across 8 weak classes."""

    # (num, hebrew, conjugation, pgn, ref, gloss, class_label, root, note)
    _PART_A = [
        # Group 1 — III-א
        SortEntry('1',  'נִמְצָא',          'Perfect',          'Gen 44:12', '"it was found"',                         'III-א', 'מָצָא', 'Perfect 3ms — silent final א'),
        SortEntry('2',  'יִמָּצֵא',         'Imperfect',        'Gen 44:10', '"let it be found"',                      'III-א', 'מָצָא', 'Imperfect 3ms — tsere + silent א'),
        SortEntry('3',  'וַיִּמָּצֵא',      'Wayyiqtol',        'Gen 44:12', '"and it was found"',                     'III-א', 'מָצָא', 'Wayyiqtol 3ms — dagesh + final silent א'),
        SortEntry('4',  'הִמָּצֵא',         'Inf. Abs.',        'Exo 22:3',  '"actually found" (emph.)',               'III-א', 'מָצָא', 'Inf. Absolute (= inf. construct form)'),
        SortEntry('5',  'הַנִּמְצָא',       'Participle ms',    'Gen 47:14', '"that which was found"',                 'III-א', 'מָצָא', 'Participle ms — article + נִ + silent final א'),
        # Group 2 — III-ה
        SortEntry('6',  'נִגְלָה',          'Perfect',          'Isa 40:5',  '"it was revealed"',                      'III-ה', 'גָּלָה', 'Perfect 3ms — final ָה'),
        SortEntry('7',  'יִגָּלֶה',         'Imperfect',        'Isa 53:1',  '"it will be revealed"',                  'III-ה', 'גָּלָה', 'Imperfect 3ms — final ֶה (not tsere)'),
        SortEntry('8',  'וַיִּגָּל',        'Wayyiqtol',        'Num 24:4',  '"whose eyes are unveiled"',              'III-ה', 'גָּלָה', 'Wayyiqtol 3ms — apocopated (ה dropped)'),
        SortEntry('9',  'לְהִגָּלוֹת',      'Inf. Construct',   'Isa 49:9',  '"to show themselves"',                   'III-ה', 'גָּלָה', 'Inf. Construct — וֹת suffix'),
        SortEntry('10', 'וַיֵּרָא',         'Wayyiqtol',        'Gen 12:7',  '"and the LORD appeared"',               'III-ה', 'רָאָה', 'Wayyiqtol 3ms — apocopated + ר compensatory tsere'),
        # Group 3 — I-guttural
        SortEntry('11', 'נֶאֱמַר',          'Perfect',          'Exo 5:13',  '"it was said"',                          'I-guttural', 'אָמַר', 'Perfect 3ms — נֶ prefix + composite shewa'),
        SortEntry('12', 'יֵאָמֵר',          'Imperfect',        'Num 21:14', '"it is said"',                           'I-guttural', 'אָמַר', 'Imperfect 3ms — יֵ prefix; no dagesh in א'),
        SortEntry('13', 'וַיֵּאָמֵר',       'Wayyiqtol',        'Gen 10:9',  '"and it was said of him"',              'I-guttural', 'אָמַר', 'Wayyiqtol 3ms — וַיֵּ (not וַיִּ)'),
        SortEntry('14', 'הֵעָמֵד',          'Inf. Construct',   'Exo 9:16',  '"for this purpose I let you stand"',    'I-guttural', 'עָמַד', 'Inf. Construct — הֵ prefix; no dagesh in ע'),
        SortEntry('15', 'נֶאֱמָן',          'Participle ms',    'Deu 7:9',   '"faithful, trustworthy"',               'I-guttural', 'אָמַן', 'Participle ms — נֶ prefix + qamets under R2'),
        # Group 4 — I-נ
        SortEntry('16', 'נִגַּשׁ',          'Perfect',          'Gen 44:18', '"he drew near"',                         'I-נ', 'נָגַשׁ', 'Perfect 3ms — dagesh forte in ג (R2)'),
        SortEntry('17', 'וַיִּגַּשׁ',       'Wayyiqtol',        'Gen 44:18', '"and he drew near"',                     'I-נ', 'נָגַשׁ', 'Wayyiqtol 3ms — dagesh in ג (R2)'),
        SortEntry('18', 'נִצַּלְתֶּם',      'Perfect',          'Exo 12:27', '"you were delivered"',                   'I-נ', 'נָצַל', 'Perfect 2mp — dagesh in צ (R2)'),
        SortEntry('19', 'הִנָּצֵל',         'Imperative',       'Prov 6:3',  '"deliver yourself!"',                    'I-נ', 'נָצַל', 'Imperative 2ms — dagesh in נּ (R2)'),
        SortEntry('20', 'וַיִּנָּצֵל',      'Wayyiqtol',        'Gen 32:31', '"and Jacob was delivered"',              'I-נ', 'נָצַל', 'Wayyiqtol 3ms — dagesh in נּ (R2)'),
        # Group 5 — I-י
        SortEntry('21', 'נוֹלַד',           'Perfect',          'Gen 21:3',  '"he was born"',                          'I-י', 'יָלַד', 'Perfect 3ms — נוֹ prefix + patach under R2'),
        SortEntry('22', 'וַיִּוָּלֵד',      'Wayyiqtol',        'Gen 4:18',  '"and he was born"',                      'I-י', 'יָלַד', 'Wayyiqtol 3ms — וַיִּוָּ cluster'),
        SortEntry('23', 'יִוָּלֵד',         'Imperfect',        'Gen 17:17', '"shall a child be born?"',               'I-י', 'יָלַד', 'Imperfect 3ms — יִוָּ cluster + tsere'),
        SortEntry('24', 'בְּהִוָּלֶד',      'Inf. Construct',   'Gen 21:5',  '"when he was born"',                     'I-י', 'יָלַד', 'Inf. Construct — הִוָּ prefix + בְּ'),
        SortEntry('25', 'נוֹלָד',           'Participle ms',    '1 Kgs 13:2', '"one who will be born"',                 'I-י', 'יָלַד', 'Participle ms — נוֹ prefix + qamets (vs. patach in perfect)'),
        # Group 6 — III-ח/ע
        SortEntry('26', 'נִשְׁמַע',         'Perfect',          'Est 1:20',  '"it was heard"',                         'III-ch/ayin', 'שָׁמַע', 'Perfect 3ms — patach furtive before final ע'),
        SortEntry('27', 'יִשָּׁמַע',        'Imperfect',        'Exo 28:35', '"it shall be heard"',                    'III-ch/ayin', 'שָׁמַע', 'Imperfect 3ms — patach (not tsere) before ע; dagesh in R1'),
        SortEntry('28', 'וַיִּשָּׁמַע',     'Wayyiqtol',        'Gen 45:2',  '"and it was heard"',                     'III-ch/ayin', 'שָׁמַע', 'Wayyiqtol 3ms — patach before ע; no furtive'),
        SortEntry('29', 'הִשָּׁמַע',        'Inf. Construct',   'Deu 4:32',  '"to be heard"',                          'III-ch/ayin', 'שָׁמַע', 'Inf. Construct (= Imperative form) — patach before ע'),
        SortEntry('30', 'נִשְׁמָע',         'Participle ms',    'Ecc 12:13', '"that which is heard"',                  'III-ch/ayin', 'שָׁמַע', 'Participle ms — qamets + patach furtive before ע'),
        # Group 7 — Biconsonantal
        SortEntry('31', 'נָכוֹן',           'Perfect',          'Gen 41:32', '"it is established"',                    'Biconsonantal', 'כּוּן', 'Perfect 3ms — נָ prefix (qamets) + medial וֹ'),
        SortEntry('32', 'יִכּוֹן',          'Imperfect',        'Psa 93:2',  '"it is established"',                    'Biconsonantal', 'כּוּן', 'Imperfect 3ms — dagesh in R1 (Niphal assimilation) + contracted root'),
        SortEntry('33', 'נָכוֹן',           'Participle ms',    'Psa 57:8',  '"steadfast, firm"',                      'Biconsonantal', 'כּוּן', 'Participle ms — נָ prefix + vocalic structure = identical to perfect'),
        SortEntry('34', 'וַיִּקּוֹם',       'Wayyiqtol',        '(expected)', '"and it was established"',              'Biconsonantal', 'קוּם', 'Wayyiqtol 3ms — וַיִּ + dagesh in R1 + contracted root'),
        SortEntry('35', 'הִקּוֹם',          'Imperative',       '(expected)', '"be established!"',                     'Biconsonantal', 'קוּם', 'Imperative 2ms — הִ + dagesh in R1 + contracted root'),
        # Group 8 — Geminate
        SortEntry('36', 'נָסַב',            'Perfect',          'Josh 15:3', '"it went around"',                       'Geminate', 'סָבַב', 'Perfect 3ms — נָ prefix (qamets), same as Biconsonantal; root ס-ב-ב has R2=R3'),
        SortEntry('37', 'וַיִּסֹּב',        'Wayyiqtol',        '1 Sam 7:16', '"and he went on circuit"',               'Geminate', 'סָבַב', 'Wayyiqtol 3ms — dagesh forte in ב (R2=R3 doubled)'),
        SortEntry('38', 'יִסֹּב',           'Imperfect',        'Josh 19:34', '"it turns around"',                      'Geminate', 'סָבַב', 'Imperfect 3ms — dagesh forte in ב; holem in contracted root'),
        SortEntry('39', 'הִסֹּב',           'Imperative',       '2 Sam 18:30', '"turn aside!"',                         'Geminate', 'סָבַב', 'Imperative 2ms — הִ + dagesh forte in ב'),
        SortEntry('40', 'נָסַב',            'Participle ms',    'Psa 26:6',  '"going around" (participial)',            'Geminate', 'סָבַב', 'Participle ms — נָ prefix, identical to perfect 3ms; context determines'),
    ]

    _PART_B = [
        SortEntry('41', 'תֵרָאֶה',          'Imperfect/Jussive', 'Gen 1:9',   '"let it appear"',                        'III-ה',         'רָאָה', '3fs — ר compensatory + final ֶה'),
        SortEntry('42', 'וַיִּוָּדַע',      'Wayyiqtol',        'Est 2:22',  '"the matter became known"',             'I-י',           'יָדַע', '3ms — וַיִּוָּ; patach under R2 (יָדַע class)'),
        SortEntry('43', 'נֶעֱמַד',          'Perfect',          '1 Sam 17:16', '"he took his stand"',                  'I-guttural',    'עָמַד', '3ms — נֶ prefix + composite shewa under ע'),
        SortEntry('44', 'וַיִּמָּצְאוּ',    'Wayyiqtol',        'Gen 47:14', '"all the silver was gathered"',          'III-א',         'מָצָא', '3mp — dagesh + 3mp ending + silent א'),
        SortEntry('45', 'נוֹדַע',           'Perfect',          'Gen 41:21', '"it was not known"',                     'I-י',           'יָדַע', '3ms — נוֹ prefix + patach (perfect, not participle)'),
        SortEntry('46', 'וַיִּגַּשׁ',       'Wayyiqtol',        'Gen 44:18', '"Judah drew near"',                      'I-נ',           'נָגַשׁ', '3ms — dagesh in ג (R2); root נ invisible'),
        SortEntry('47', 'הֵרָאֵה',          'Imperative',       '1 Kgs 18:1', '"show yourself!"',                       'III-ה',         'רָאָה', '2ms — הֵ compensatory + final ֵה (imperative)'),
        SortEntry('48', 'נִשְׁלַח',         'Perfect',          'Est 3:13',  '"letters were sent"',                    'III-ch/ayin',   'שָׁלַח', '3ms — patach furtive before final ח'),
        SortEntry('49', 'נָכוֹן',           'Perfect/Participle', 'Exo 34:2', '"be ready"',                             'Biconsonantal', 'כּוּן', 'נָ prefix (qamets) is the biconsonantal Niphal marker'),
        SortEntry('50', 'וַיִּסֹּב',        'Wayyiqtol',        '2 Sam 5:23', '"and he circled behind them"',          'Geminate',      'סָבַב', '3ms — וַיִּ + dagesh forte in ב (R2=R3); root ס-ב-ב is Geminate, not hollow'),
        SortEntry('51', 'נִמְצְאוּ',        'Perfect',          'Exo 12:19', '"whoever is found"',                     'III-א',         'מָצָא', '3cp — 3cp ending + final silent א'),
        SortEntry('52', 'יֵעָמְדוּ',        'Imperfect',        'Num 27:22', '"they shall stand before"',              'I-guttural',    'עָמַד', '3mp — יֵ prefix; no dagesh in ע; 3mp ending'),
    ]

    def _build(self) -> None:
        self.add_instructions(
            'Part A (1–40): forms are grouped by weak class. Identify class, parse conjugation + PGN, '
            'and give the root. '
            'Part B (41–52): mixed classes — identify the class first, then parse. '
            'Answer key is on the last page.'
        )

        self.add_note(
            'Classes: III-א (silent final א)  |  III-ה (final ָה / ֶה / וֹת / apocopated)  |  '
            'III-ch/ayin (patach furtive before ח/ע; patach in short forms)  |  '
            'I-guttural (נֶ / יֵ / הֵ prefix; no dagesh in R1)  |  '
            'I-נ (dagesh forte in R2; root נ invisible)  |  '
            'I-י (נוֹ prefix in perfect/ptc; יִוָּ / הִוָּ in impf/wayyiqtol/imv/inf)  |  '
            'Biconsonantal (נָ prefix in perfect/ptc; dagesh in R1 elsewhere)  |  '
            'Geminate (נָ prefix in perfect/ptc — same as Biconsonantal!; dagesh forte in R2/R3 elsewhere; R2=R3 is the class marker)'
        )

        self.add_section_heading('Part A — By Class')
        self.add_sort_table(self._PART_A, show_answers=False)

        self.add_section_heading('Part B — Mixed')
        self.add_sort_table(self._PART_B, show_answers=False)

        self.add_reflection([
            'Items 1 and 5 (III-א) are both pointed נִמְצָא — perfect 3ms and participle ms are identical. '
            'What contextual or syntactic clues allow you to distinguish them in a real text?',
            'Compare items 8 (וַיִּגָּל, III-ה) and 17 (וַיִּגַּשׁ, I-נ). Both show a short form after '
            'וַיִּ with a dagesh. How do you tell them apart?',
            'Items 10 (וַיֵּרָא) and 13 (וַיֵּאָמֵר) both use the prefix וַיֵּ instead of the expected '
            'וַיִּ. Is this the same phonological rule in both cases?',
            'Items 21 (נוֹלַד) and 25 (נוֹלָד) differ only in the vowel under R2. Which is the perfect '
            'and which is the participle, and how would each behave differently in a clause?',
            'Items 26 (נִשְׁמַע, III-ח/ע) and item 1 (נִמְצָא, III-א) both begin with נִ. What '
            'distinguishes them visually, and why does the patach furtive appear before שָׁמַע but not מָצָא?',
            'Items 31 and 33 both show נָכוֹן (Biconsonantal). How does this perfect/participle ambiguity '
            'parallel the III-א problem in question 1, and what does it reveal about the general challenge '
            'of Niphal weak forms?',
            'Items 36 and 40 (Geminate) are both pointed נָסַב — perfect 3ms and participle ms are '
            'identical in the Geminate class, just like the Biconsonantal class (items 31/33). '
            'Given a form like נָסַב, how do you even know whether the root is Geminate (ס-ב-ב) '
            'or Biconsonantal (a hollow root)? What information outside the vocalization must you use?',
        ])

        self.add_answer_key_sort(self._PART_A + self._PART_B)


def build_ch25_weak_form_id_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch25WeakFormIdExercise,
        'Chapter 25 — Niphal Weak-Form Identification Drill',
        'BBH Chapter 25 · Niphal Weak Verbs',
        ['hebrew', 'bbh', 'ch25', 'exercises', 'ch25-weak-form-id'],
        'ch25-weak-form-id.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 27 — Hiphil Weak Verbs
# ---------------------------------------------------------------------------


class Ch27Exercise(ExercisePDF):
    """Passage exercise — 18 Hiphil weak verbs from Gen, Exo, Num, Deu."""

    def _render_passages(self, show_answers: bool) -> None:

        self.add_section_heading('Part A — Genesis and Exodus (items 1–10)')

        self.add_passage(PassageBlock('Gen 1:5',
            'וַיִּקְרָא אֱלֹהִים לָאוֹר יוֹם וַיַּקְרֵא לַחֹשֶׁךְ לָיְלָה',
            '"and he [1] ____ the darkness Night"'))
        self.add_verb_table([VerbEntry('1', 'וַיַּקְרֵא', 'Wayyiqtol', '3ms', 'קָרָא', 'III-א — he called / proclaimed')], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 6:18',
            'וַהֲקִמֹתִי אֶת־בְּרִיתִי אִתְּךָ',
            '"but I [2] ____ my covenant with you"'))
        self.add_verb_table([VerbEntry('2', 'וַהֲקִמֹתִי', 'Weqatal', '1cs', 'קוּם', 'Biconsonantal — I will establish')], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 8:20',
            'הֶעֱלָה נֹחַ עֹלֹת עַל הַמִּזְבֵּחַ',
            '"Noah [3] ____ burnt offerings on the altar"'))
        self.add_verb_table([VerbEntry('3', 'הֶעֱלָה', 'Perfect', '3ms', 'עָלָה', 'III-ה + I-guttural — he offered up')], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 15:7',
            'אֲנִי יְהוָה אֲשֶׁר הוֹצֵאתִיךָ מֵאוּר כַּשְׂדִּים',
            '"I am the LORD who [4] ____ from Ur of the Chaldeans"'))
        self.add_verb_table([VerbEntry('4', 'הוֹצֵאתִיךָ', 'Perfect', '1cs + 2ms', 'יָצָא', 'I-י — I brought you out')], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 22:2',
            'וַיַּעַל שָׁם עֹלָה',
            '"and he [5] ____ a burnt offering there"'))
        self.add_verb_table([VerbEntry('5', 'וַיַּעַל', 'Wayyiqtol', '3ms', 'עָלָה', 'III-ה — he offered up (apocopated)')], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 2:21',
            'וַיַּפֵּל יְהוָה אֱלֹהִים תַּרְדֵּמָה עַל הָאָדָם',
            '"the LORD God [6] ____ a deep sleep upon the man"'))
        self.add_verb_table([VerbEntry('6', 'וַיַּפֵּל', 'Wayyiqtol', '3ms', 'נָפַל', 'I-נ — he caused to fall / cast')], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 9:16',
            'וְאוּלָם בַּעֲבוּר זֹאת הֶעֱמַדְתִּיךָ',
            '"but for this purpose I [7] ____ you"'))
        self.add_verb_table([VerbEntry('7', 'הֶעֱמַדְתִּיךָ', 'Perfect', '1cs + 2ms', 'עָמַד', 'I-guttural — I raised you up / stationed you')], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 20:2',
            'אָנֹכִי יְהוָה אֱלֹהֶיךָ אֲשֶׁר הוֹצֵאתִיךָ מֵאֶרֶץ מִצְרַיִם',
            '"I am the LORD your God, who [8] ____ of the land of Egypt"'))
        self.add_verb_table([VerbEntry('8', 'הוֹצֵאתִיךָ', 'Perfect', '1cs + 2ms', 'יָצָא', 'I-י — I brought you out')], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 33:18',
            'וַיֹּאמַר הַרְאֵנִי נָא אֶת־כְּבֹדֶךָ',
            '"and he said, [9] ____ your glory, please"'))
        self.add_verb_table([VerbEntry('9', 'הַרְאֵנִי', 'Imperative', '2ms + 1cs', 'רָאָה', 'III-ה — show me')], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 40:2',
            'הָקֵם אֶת־מִשְׁכַּן אֹהֶל מוֹעֵד',
            '"[10] ____ the tabernacle of the tent of meeting"'))
        self.add_verb_table([VerbEntry('10', 'הָקֵם', 'Imperative', '2ms', 'קוּם', 'Biconsonantal — set up / erect')], show_answers=show_answers)

        self.add_section_break()
        self.add_section_heading('Part B — Numbers and Deuteronomy (items 11–18)')

        self.add_passage(PassageBlock('Num 27:19',
            'הַעֲמֵד אֹתוֹ לִפְנֵי אֶלְעָזָר הַכֹּהֵן',
            '"[11] ____ him before Eleazar the priest"'))
        self.add_verb_table([VerbEntry('11', 'הַעֲמֵד', 'Imperative', '2ms', 'עָמַד', 'I-guttural — set him / station him')], show_answers=show_answers)

        self.add_passage(PassageBlock('Deu 18:15',
            'נָבִיא מִקִּרְבְּךָ יָקִים לְךָ יְהוָה אֱלֹהֶיךָ',
            '"a prophet like me the LORD [12] ____ for you"'))
        self.add_verb_table([VerbEntry('12', 'יָקִים', 'Imperfect', '3ms', 'קוּם', 'Biconsonantal — will raise up')], show_answers=show_answers)

        self.add_passage(PassageBlock('Deu 4:10',
            'הַשְׁמַע אֶת־הָעָם אֶת־דִּבְרֵי',
            '"[13] ____ the people these words"'))
        self.add_verb_table([VerbEntry('13', 'הַשְׁמַע', 'Imperative', '2ms', 'שָׁמַע', 'III-ח/ע — make them hear')], show_answers=show_answers)

        self.add_passage(PassageBlock('Deu 8:14',
            'אֲשֶׁר הוֹצִיאֲךָ מֵאֶרֶץ מִצְרַיִם',
            '"who [14] ____ of the land of Egypt"'))
        self.add_verb_table([VerbEntry('14', 'הוֹצִיאֲךָ', 'Perfect', '3ms + 2ms', 'יָצָא', 'I-י — he brought you out')], show_answers=show_answers)

        self.add_passage(PassageBlock('Deu 8:14',
            'הַמּוֹצִיאֲךָ מֵאֶרֶץ מִצְרַיִם',
            '"[15] ____ of the land of Egypt (substantival participle)"'))
        self.add_verb_table([VerbEntry('15', 'הַמּוֹצִיאֲךָ', 'Participle', 'ms', 'יָצָא', 'I-י — the one who brought you out')], show_answers=show_answers)

        self.add_passage(PassageBlock('Num 1:51',
            'וְהֵקִים אֶת־הַמִּשְׁכָּן',
            '"and [16] ____ the tabernacle"'))
        self.add_verb_table([VerbEntry('16', 'וְהֵקִים', 'Weqatal', '3ms', 'קוּם', 'Biconsonantal — he shall set up')], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 3:17',
            'לְהַעֲלוֹת אֶתְכֶם מֵעֳנִי מִצְרַיִם',
            '"[17] ____ you out of the affliction of Egypt"'))
        self.add_verb_table([VerbEntry('17', 'לְהַעֲלוֹת', 'Inf. Construct', '—', 'עָלָה', 'III-ה + I-guttural — to bring up')], show_answers=show_answers)

        self.add_passage(PassageBlock('Isa 48:6',
            'מֵעַתָּה אַשְׁמִיעֲכֶם חֲדָשׁוֹת',
            '"from now on [18] ____ new things"'))
        self.add_verb_table([VerbEntry('18', 'אַשְׁמִיעֲכֶם', 'Imperfect', '1cs + 2mp', 'שָׁמַע', 'III-ח/ע — I announce to you')], show_answers=show_answers)

        self.add_section_break()
        self.add_section_heading('Part C — Distractor Check')
        self.add_note(
            'These three verbs are drawn from the same corpus. None are Hiphil. '
            'Answer "No" for Hiphil? and complete the full parse.'
        )

        self.add_passage(PassageBlock('Gen 22:3',
            'וַיַּשְׁכֵּם אַבְרָהָם בַּבֹּקֶר וַיֵּלֶךְ אֶל הַמָּקוֹם',
            '"And Abraham rose early in the morning and [19] ____ to the place."'))
        self.add_verb_table([VerbEntry('19', 'וַיֵּלֶךְ', 'Wayyiqtol', '3ms', 'הָלַךְ', 'NOT Hiphil — Qal: and he went; no הִ/הַ prefix; plain Qal of הָלַךְ')], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 21:3',
            'וַיִּקְרָא אַבְרָהָם אֶת שֶׁם בְּנוֹ אֲשֶׁר נוֹלַד לוֹ',
            '"And Abraham called the name of his son who [20] ____ to him."'))
        self.add_verb_table([VerbEntry('20', 'נוֹלַד', 'Perfect', '3ms', 'יָלַד', 'NOT Hiphil — Niphal passive: was born; נוֹ- prefix = Niphal of I-י root')], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 2:17',
            'כִּי בְּיוֹם אֲכָלְךָ מִמֶּנּוּ מוֹת תָּמוּת',
            '"for in the day you eat of it you shall surely [21] ____."'))
        self.add_verb_table([VerbEntry('21', 'תָּמוּת', 'Imperfect', '2ms', 'מוּת', 'NOT Hiphil — Qal: you will die; תָּ- prefix = Qal imperfect 2ms; no הַ- Hiphil prefix')], show_answers=show_answers)

    def _build(self) -> None:
        self.add_instructions(
            'Most highlighted verbs are Hiphil forms. For each: (1) Is it Hiphil? (Yes / No); '
            '(2) parse — conjugation, person-gender-number, root; '
            '(3) state the weak class '
            '(I-guttural / III-ch/ayin / III-aleph / III-he / Pe-Nun / Pe-Yod / Biconsonantal); '
            '(4) give a brief causative gloss in context. '
            'Three verbs in Part C are not Hiphil. Answer "No" and parse fully.'
        )
        self._render_passages(show_answers=False)
        self.add_section_heading('Answer Key')
        self._render_passages(show_answers=True)


def build_ch27_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch27Exercise,
        'Chapter 27 — "Spot the Hiphil" Passage Exercise',
        'BBH Chapter 27 · Hiphil Weak Verbs',
        ['hebrew', 'bbh', 'ch27', 'exercises', 'ch27-passage-exercise'],
        'ch27-passage-exercise.pdf',
        out_dir,
    )


class Ch27WeakFormIdExercise(ExercisePDF):
    """Weak-Form Identification Drill — 50 items across 8 weak classes."""

    _PART_A = [
        # Group 1 — I-guttural
        SortEntry('1',  'הֶעֱמִיד',      'Perfect',      '1 Kgs 7:21', '"he set up"',              'I-guttural',    'עָמַד', 'seghol under הֶ + hateph-seghol under ע'),
        SortEntry('2',  'וַיַּעֲמֵד',    'Wayyiqtol',    '2 Chr 4:4',  '"and he set it"',           'I-guttural',    'עָמַד', 'patach prefix + composite shewa under ע'),
        SortEntry('3',  'יַעֲמִיד',      'Imperfect',    'Psa 107:29', '"he causes to stand"',      'I-guttural',    'עָמַד', 'patach prefix + composite shewa; no dagesh'),
        SortEntry('4',  'הַעֲמֵד',       'Imperative',   'Num 27:19',  '"set him before"',          'I-guttural',    'עָמַד', 'הַ + composite shewa under ע + tsere'),
        SortEntry('5',  'מַעֲמִיד',      'Participle',   'Neh 4:7',    '"one who stations"',        'I-guttural',    'עָמַד', 'מַ + composite shewa under ע + chiriq'),
        # Group 2 — III-ח/ע
        SortEntry('6',  'הִשְׁמִיעַ',    'Perfect',      'Isa 48:6',   '"he caused to hear"',       'III-ch/ayin',   'שָׁמַע', 'patach furtive before final ע in 3ms'),
        SortEntry('7',  'וַיַּשְׁלַח',   'Wayyiqtol',    'Gen 3:23',   '"and he sent out"',         'III-ch/ayin',   'שָׁלַח', 'patach (not tsere) before final ח'),
        SortEntry('8',  'יַשְׁמִיעַ',    'Imperfect',    'Isa 42:2',   '"he will cause to hear"',   'III-ch/ayin',   'שָׁמַע', 'patach furtive before final ע'),
        SortEntry('9',  'הַשְׁמַע',      'Imperative',   'Deu 4:10',   '"make them hear"',          'III-ch/ayin',   'שָׁמַע', 'patach before final ע (not tsere)'),
        SortEntry('10', 'מַשְׁמִיעַ',    'Participle',   'Isa 41:26',  '"one who announces"',       'III-ch/ayin',   'שָׁמַע', 'מַ + chiriq-yod + patach furtive before ע'),
        # Group 3 — III-א
        SortEntry('11', 'הִמְצִיא',      'Perfect',      'Neh 9:15',   '"he provided"',             'III-aleph',     'מָצָא', 'chiriq-yod + silent final א'),
        SortEntry('12', 'וַיַּמְצֵא',    'Wayyiqtol',    '2 Chr 2:13', '"and he provided"',         'III-aleph',     'מָצָא', 'tsere + silent final א'),
        SortEntry('13', 'יַמְצִיא',      'Imperfect',    'Pro 8:35',   '"he will cause to find"',   'III-aleph',     'מָצָא', 'chiriq-yod + silent final א'),
        SortEntry('14', 'וַיַּקְרֵא',    'Wayyiqtol',    'Gen 1:5',    '"and he called"',           'III-aleph',     'קָרָא', 'tsere + silent final א'),
        SortEntry('15', 'מַקְרִיא',      'Participle',   'Neh 8:3',    '"one who reads aloud"',     'III-aleph',     'קָרָא', 'מַ + chiriq-yod + silent final א'),
        # Group 4 — III-ה
        SortEntry('16', 'הֶעֱלָה',       'Perfect',      'Gen 8:20',   '"he offered up"',           'III-he',        'עָלָה', 'qamets + ה ending; seghol under הֶ'),
        SortEntry('17', 'וַיַּעַל',      'Wayyiqtol',    'Gen 22:2',   '"and he went up"',          'III-he',        'עָלָה', 'apocopated — ה dropped; short patach under R2'),
        SortEntry('18', 'יַעֲלֶה',       'Imperfect',    'Lev 14:20',  '"he shall offer up"',       'III-he',        'עָלָה', 'seghol + ה ending'),
        SortEntry('19', 'הַרְאֵה',       'Imperative',   'Exo 33:18',  '"show me"',                 'III-he',        'רָאָה', 'tsere + ה retained (not apocopated)'),
        SortEntry('20', 'לְהַעֲלוֹת',   'Inf. Construct', 'Exo 3:17',  '"to bring up"',             'III-he',        'עָלָה', 'ends in וֹת — strong III-ה marker'),
        # Group 5 — I-נ
        SortEntry('21', 'הִפִּיל',       'Perfect',      'Gen 2:21',   '"he caused to fall"',       'I-nun',         'נָפַל', 'dagesh forte in R2 (פ); נ assimilated'),
        SortEntry('22', 'וַיַּפֵּל',     'Wayyiqtol',    'Gen 2:21',   '"and he cast"',             'I-nun',         'נָפַל', 'patach prefix + dagesh in R2 + tsere'),
        SortEntry('23', 'יַפִּיל',       'Imperfect',    'Pro 19:15',  '"causes to fall"',          'I-nun',         'נָפַל', 'patach prefix + dagesh in R2 + chiriq'),
        SortEntry('24', 'הַגֵּשׁ',       'Imperative',   'Gen 27:25',  '"bring near"',              'I-nun',         'נָגַשׁ', 'הַ + dagesh forte in R2 (ג) + tsere'),
        SortEntry('25', 'מַגִּישׁ',      'Participle',   'Mal 1:7',    '"one who brings near"',     'I-nun',         'נָגַשׁ', 'מַ + dagesh in R2 + chiriq'),
        # Group 6 — I-י
        SortEntry('26', 'הוֹצִיא',       'Perfect',      'Gen 15:7',   '"he brought out"',          'I-yod',         'יָצָא', 'הוֹ prefix (holem-vav) — I-yod/vav signature'),
        SortEntry('27', 'וַיּוֹצֵא',     'Wayyiqtol',    'Gen 1:12',   '"and it brought forth"',    'I-yod',         'יָצָא', 'וַיּוֹ prefix — dagesh in יּ + holem-vav'),
        SortEntry('28', 'יוֹרִיד',       'Imperfect',    '1 Sam 2:6',  '"he brings down"',          'I-yod',         'יָרַד', 'יוֹ prefix (holem-vav)'),
        SortEntry('29', 'הוֹרֵד',        'Imperative',   'Gen 42:38',  '"bring down"',              'I-yod',         'יָרַד', 'הוֹ prefix (not הַ) + tsere'),
        SortEntry('30', 'מוֹצִיא',       'Participle',   'Deu 8:14',   '"the one who brings out"',  'I-yod',         'יָצָא', 'מוֹ prefix (holem-vav) — not מַ'),
        # Group 7 — Biconsonantal
        SortEntry('31', 'הֵקִים',        'Perfect',      'Gen 6:18',   '"he established"',          'Biconsonantal', 'קוּם', 'הֵ prefix (tsere) — not הִ (hiriq)'),
        SortEntry('32', 'וַיָּקֶם',      'Wayyiqtol',    'Gen 23:20',  '"and it was confirmed"',    'Biconsonantal', 'קוּם', 'qamets prefix + apocopated seghol final'),
        SortEntry('33', 'יָקִים',        'Imperfect',    'Deu 18:15',  '"he will raise up"',        'Biconsonantal', 'קוּם', 'qamets under prefix consonant (יָ)'),
        SortEntry('34', 'הָקֵם',         'Imperative',   'Exo 40:2',   '"set up"',                  'Biconsonantal', 'קוּם', 'הָ prefix (qamets) + tsere'),
        SortEntry('35', 'מֵקִים',        'Participle',   '1 Sam 2:8',  '"one who raises up"',       'Biconsonantal', 'קוּם', 'מֵ prefix (tsere) — not מַ'),
        # Group 8 — Geminate
        SortEntry('36', 'הֵסֵב',         'Perfect',      '1 Kgs 21:4', '"he turned his face"',      'Geminate', 'סָבַב', 'הֵ prefix (tsere) — same as Biconsonantal הֵקִים; root ס-ב-ב has R2=R3'),
        SortEntry('37', 'וַיָּסֶב',      'Wayyiqtol',    'Josh 6:14',  '"and they marched around"', 'Geminate', 'סָבַב', 'qamets prefix + apocopated seghol — same pattern as Biconsonantal וַיָּקֶם'),
        SortEntry('38', 'יָסֵב',         'Imperfect',    'Isa 44:20',  '"it leads astray"',         'Geminate', 'סָבַב', 'qamets under prefix (יָ) — same as Biconsonantal יָקִים; root knowledge required'),
        SortEntry('39', 'הָסֵב',         'Imperative',   '2 Sam 2:22', '"turn aside!"',             'Geminate', 'סָבַב', 'הָ prefix (qamets) — same as Biconsonantal הָקֵם; only root distinguishes'),
        SortEntry('40', 'מֵסֵב',         'Participle',   '(expected)', '"one who surrounds"',       'Geminate', 'סָבַב', 'מֵ prefix (tsere) — same as Biconsonantal מֵקִים; Geminate class requires root knowledge'),
    ]

    _PART_B = [
        SortEntry('41', 'וַיַּשְׁמַע',   'Wayyiqtol',    '1 Sam 15:14', '"and he made heard"',       'III-ch/ayin',   'שָׁמַע', 'patach before final ע (not tsere) — guttural forces lowering'),
        SortEntry('42', 'הֵשִׂים',        'Perfect',       'Gen 45:9',    '"he made / placed"',        'Biconsonantal', 'שִׂים',  'הֵ prefix (tsere); root שׂ-י-מ contains medial hireq-yod vowel letter = Biconsonantal'),
        SortEntry('43', 'וַיַּעַל',       'Wayyiqtol',     'Gen 22:2',    '"and he went up"',          'III-he',        'עָלָה', 'apocopated: ה dropped'),
        SortEntry('44', 'הִגִּישׁ',       'Perfect',       'Amos 9:13',   '"he brought near"',         'I-nun',         'נָגַשׁ', 'dagesh forte in R2 (ג)'),
        SortEntry('45', 'הָסֵב',          'Imperative',    '2 Sam 5:23',  '"circle around behind them"', 'Geminate',     'סָבַב', 'הָ prefix (qamets) — looks exactly like Biconsonantal הָקֵם; root ס-ב-ב has R2=R3 = Geminate'),
        SortEntry('46', 'הֶרְאָה',        'Perfect',       'Exo 25:9',    '"he showed"',               'III-he',        'רָאָה', 'qamets + ה ending; seghol under הֶ'),
        SortEntry('47', 'וַיּוֹרֶד',      'Wayyiqtol',     'Gen 42:38',   '"and he brought down"',     'I-yod',         'יָרַד', 'וַיּוֹ prefix uniquely identifies I-yod Hiphil'),
        SortEntry('48', 'מַעֲמִידִים',    'Participle mp', 'Neh 4:7',     '"those who station"',       'I-guttural',    'עָמַד', 'מַ + composite shewa under ע + chiriq + ים'),
        SortEntry('49', 'הַמְצֵא',        'Imperative',    '(expected)',  '"cause to find"',           'III-aleph',     'מָצָא', 'tsere + silent final א; הַ prefix (patach)'),
        SortEntry('50', 'וָאָקִים',       'Wayyiqtol',     'Exo 6:4',     '"and I established"',       'Biconsonantal', 'קוּם', 'וָאָ (1cs wayyiqtol) + qamets + chiriq-yod medial vowel letter = Biconsonantal'),
    ]

    def _build(self) -> None:
        self.add_instructions(
            'Part A (1–40): forms are grouped by weak class (5 per class). '
            'Identify conjugation + PGN, and give the root. '
            'Part B (41–50): mixed classes — identify the class first, then parse. '
            'Answer key is on the last page.'
        )

        self.add_note(
            'Classes: I-guttural (he prefix seghol; composite shewa under R1)  |  '
            'III-ch/ayin (patach furtive before final guttural)  |  '
            'III-aleph (silent final aleph; chiriq-yod or tsere before it)  |  '
            'III-he (qamets+he perfect; seghol+he impf/ptc; apocopated wayyiqtol; vot inf.cstr)  |  '
            'I-nun (dagesh forte in R2 throughout)  |  '
            'I-yod (ho/yo/mo prefix pattern)  |  '
            'Biconsonantal (he+tsere perfect; qamets impf/wayyiqtol; ha+qamets imv/inf; me+tsere ptc)  |  '
            'Geminate (same prefixes as Biconsonantal! R2=R3 is the only distinguishing feature; requires root knowledge)'
        )

        self.add_section_heading('Part A — By Class')
        self.add_sort_table(self._PART_A, show_answers=False)

        self.add_section_heading('Part B — Mixed')
        self.add_sort_table(self._PART_B, show_answers=False)

        self.add_reflection([
            'Compare הִמְצִיא (III-aleph perfect 3ms) and הַמְצֵא (III-aleph imperative 2ms). '
            'Both end with silent final aleph. How do you distinguish them? '
            'What is the key difference in the prefix vowel?',
            'הַשְׁמַע (III-ch/ayin imperative) and הַעֲמֵד (I-guttural imperative) both begin '
            'with the ha- prefix. How does the vowel under R1 differ? What does that tell you about the class?',
            'וַיַּשְׁלַח (III-ch/ayin wayyiqtol) and וַיַּקְרֵא (III-aleph wayyiqtol) both have '
            'patach under the wayyiqtol prefix. The difference is in the final vowel. '
            'Explain what happens to the Hiphil tsere in each case and why.',
            'Compare הוֹרֵד (I-yod imperative 2ms) and הָקֵם (Biconsonantal imperative 2ms). '
            'Both have a long prefix vowel rather than the patach of the strong Hiphil imperative. '
            'What prefix vowel does each use, and how can you tell them apart?',
            'Items 36-40 (Geminate) and items 31-35 (Biconsonantal) share nearly identical vowel '
            'patterns in every conjugation: he+tsere perfect, qamets imperfect/wayyiqtol, '
            'ha+qamets imperative, me+tsere participle. What is the only reliable way to determine '
            'whether a Hiphil form belongs to the Geminate class or the Biconsonantal class? '
            'Why can the vocalization alone not always resolve this question?',
        ])

        self.add_answer_key_sort(self._PART_A + self._PART_B)


def build_ch27_weak_form_id_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch27WeakFormIdExercise,
        'Chapter 27 — Hiphil Weak-Form Identification Drill',
        'BBH Chapter 27 · Hiphil Weak Verbs',
        ['hebrew', 'bbh', 'ch27', 'exercises', 'ch27-weak-form-id'],
        'ch27-weak-form-id.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 27 — Niphal–Hiphil Contrast Drill
# ---------------------------------------------------------------------------


class Ch27NHContrastExercise(ExercisePDF):
    """Niphal–Hiphil Contrast Drill — 20 items across both stems."""

    _PART_A = [
        NHEntry('1',  'נִשְׁמַע',     'Est 1:20',  '"the decree ___ throughout the kingdom"',   'Niphal', 'Perfect',    '3ms', 'שָׁמַע · III-ח/ע',         'was heard',              'נִ prefix + patach furtive before ע = Niphal III-ח/ע perfect'),
        NHEntry('2',  'הִשְׁמִיעַ',   'Isa 48:6',  '"I ___ you new things"',                    'Hiphil', 'Perfect',    '3ms', 'שָׁמַע · III-ח/ע',         'caused to hear / announced', 'הִ + chiriq-yod + patach furtive before ע = Hiphil III-ח/ע perfect'),
        NHEntry('3',  'יִמָּצֵא',     'Gen 44:10', '"he with whom it is ___ shall be my servant"', 'Niphal', 'Imperfect', '3ms', 'מָצָא · III-א',            'is found',               'יִמָּ (dagesh in מ = Niphal assimilation) + tsere + silent א'),
        NHEntry('4',  'הִמְצִיא',     'Neh 9:15',  '"You ___ them bread from heaven"',           'Hiphil', 'Perfect',    '3ms', 'מָצָא · III-א',            'provided / caused to find', 'הִ + chiriq-yod + silent final א = Hiphil III-א perfect'),
        NHEntry('5',  'נִגְלָה',      'Isa 40:5',  '"the glory of the LORD shall ___"',          'Niphal', 'Perfect',    '3ms', 'גָּלָה · III-ה',           'was revealed',           'נִ prefix + final ָה = Niphal III-ה perfect'),
        NHEntry('6',  'הֶעֱלָה',      'Gen 8:20',  '"Noah ___ burnt offerings on the altar"',    'Hiphil', 'Perfect',    '3ms', 'עָלָה · III-ה + I-gutt.', 'offered up',             'הֶ prefix + hateph-seghol under ע + qamets + ה = Hiphil III-ה perfect'),
        NHEntry('7',  'וַיִּגַּשׁ',   'Gen 44:18', '"Judah ___ him and said"',                  'Niphal', 'Wayyiqtol',  '3ms', 'נָגַשׁ · I-נ',             'drew near (reflexive)',   'וַיִּ + dagesh in ג (Niphal I-נ assimilation) without הִ prefix'),
        NHEntry('8',  'הִגִּישׁ',     'Amos 9:13', '"the one who ___ grain offering"',           'Hiphil', 'Perfect',    '3ms', 'נָגַשׁ · I-נ',             'brought near',           'הִ prefix + dagesh in ג (R2); contrast Niphal וַיִּגַּשׁ'),
    ]

    _PART_B = [
        NHEntry('9',  'נוֹלַד',       'Gen 21:3',  '"a son ___ to Abraham"',                    'Niphal', 'Perfect',    '3ms', 'יָלַד · I-י',              'was born',               'נוֹ prefix = Niphal I-י perfect; patach under R2 (not qamets of participle)'),
        NHEntry('10', 'יּוֹלֶד',      'Gen 5:3',   '"Adam ___ a son in his own likeness"',      'Hiphil', 'Wayyiqtol',  '3ms', 'יָלַד · I-י',              'fathered / begat',       'וַיּוֹ prefix (dagesh in יּ + holem-vav) = Hiphil I-י wayyiqtol'),
        NHEntry('11', 'יִוָּלֵד',     'Gen 17:17', '"shall a child ___ to a man of 100 years?"', 'Niphal', 'Imperfect',  '3ms', 'יָלַד · I-י',              'shall be born',          'יִוָּ cluster (dagesh in ו) = Niphal I-י imperfect; contrast Hiphil יוֹ'),
        NHEntry('12', 'יוֹרִיד',      '1 Sam 2:6', '"the LORD ___ to Sheol and raises up"',     'Hiphil', 'Imperfect',  '3ms', 'יָרַד · I-י',              'brings down',            'יוֹ prefix (holem-vav, no dagesh in ו) = Hiphil I-י imperfect'),
        NHEntry('13', 'וַיִּוָּדַע',  'Est 2:22',  '"the matter ___ to Mordecai"',              'Niphal', 'Wayyiqtol',  '3ms', 'יָדַע · I-י',              'became known',           'וַיִּוָּ cluster = Niphal I-י wayyiqtol'),
        NHEntry('14', 'הֵקִים',       'Gen 6:18',  '"I will ___ my covenant with you"',         'Hiphil', 'Perfect',    '3ms', 'קוּם · Biconsonantal',     'established',            'הֵ prefix (tsere) = Hiphil Biconsonantal perfect; contrast Niphal נָ (qamets)'),
        NHEntry('15', 'נָכוֹן',       'Gen 41:32', '"the thing is ___ by God"',                 'Niphal', 'Perfect',    '3ms', 'כּוּן · Biconsonantal',    'is established / firm',  'נָ prefix (qamets) = Niphal Biconsonantal perfect; context confirms passive sense'),
    ]

    _PART_C = [
        NHEntry('16', 'וַיַּעַל',     'Gen 22:2',  '"and he ___ him as a burnt offering"',      'Hiphil', 'Wayyiqtol',  '3ms', 'עָלָה · III-ה + I-gutt.', 'offered up (apocopated)', 'patach prefix (יַ) + composite shewa + apocopated = Hiphil; contrast Niphal וַיֵּ'),
        NHEntry('17', 'וַיִּגָּל',    'Num 24:4',  '"who sees the vision, ___ eyes"',           'Niphal', 'Wayyiqtol',  '3ms', 'גָּלָה · III-ה',           'were uncovered (apocopated)', 'וַיִּ + dagesh in ג (Niphal assimilation) + apocopated = Niphal'),
        NHEntry('18', 'הָסֵב',        '2 Sam 2:22', '"___ from following me"',                   'Hiphil', 'Imperative', '2ms', 'סָבַב · Geminate',         'turn aside!',            'הָ prefix (qamets) = Hiphil Biconsonantal/Geminate imperative; root R2=R3'),
        NHEntry('19', 'מַעֲמִידִים',  'Neh 4:7',   '"we who were ___ guard over them"',         'Hiphil', 'Participle', 'mp',  'עָמַד · I-guttural',       'stationing / standing guard', 'מַ + composite shewa under ע = Hiphil I-guttural participle; contrast Niphal נֶ'),
        NHEntry('20', 'הֵרָאֵה',      '1 Kgs 18:1', '"Go, ___ yourself to Ahab"',                'Niphal', 'Imperative', '2ms', 'רָאָה · III-ה',            'show yourself!',         'הֵ prefix (ר compensatory) + final ֵה retained = Niphal III-ה imperative'),
    ]

    def _build(self) -> None:
        self.add_instructions(
            'For each form: (1) identify the stem (Niphal or Hiphil); (2) parse — conjugation, PGN; '
            '(3) give the root and weak class; (4) translate in context. '
            'Answer key is on the last page.'
        )

        self.add_note(
            'Niphal markers: נִ prefix (perfect/participle); יִמָּ / וַיִּמָּ (imperfect/wayyiqtol — assimilation); '
            'נוֹ (I-י perfect/ptc); יִוָּ (I-י imperfect); נָ (Biconsonantal perfect/ptc).  '
            'Hiphil markers: הִ prefix (perfect); יַ (imperfect); הַ (imperative/inf.); מַ (participle) — '
            'modified for weak classes: הֶ (I-gutt.), הוֹ / יוֹ / מוֹ (I-י), הֵ / יָ / הָ / מֵ (Biconsonantal/Geminate).'
        )

        self.add_section_heading('Part A — Contrasting Niphal and Hiphil (same root)')
        self.add_note('Niphal = passive/reflexive. Hiphil = causative. Same root, opposite semantic direction.')
        self.add_nh_table(self._PART_A, show_answers=False)

        self.add_section_heading('Part B — Weak-Class Focus (I-י and Biconsonantal)')
        self.add_note(
            'I-י: Niphal perfect/ptc = נוֹ; imperfect = יִוָּ (dagesh in ו). '
            'Hiphil perfect = הוֹ; imperfect = יוֹ (no dagesh in ו). '
            'Biconsonantal: Niphal perfect/ptc = נָ (qamets); Hiphil perfect = הֵ (tsere).'
        )
        self.add_nh_table(self._PART_B, show_answers=False)

        self.add_section_heading('Part C — Mixed Review')
        self.add_nh_table(self._PART_C, show_answers=False)

        self.add_reflection([
            'Items 1–2 (שָׁמַע) and 3–4 (מָצָא): pick one pair and explain in one sentence '
            'what the Niphal adds and what the Hiphil adds to the basic Qal meaning.',
            'Items 9–11 are all from יָלַד (I-י). Both stems use a holem-vav cluster. '
            'What is the precise difference between Niphal perfect נוֹלַד and Hiphil wayyiqtol וַיּוֹלֶד?',
            'Items 16 and 17 are both apocopated III-ה wayyiqtol forms. '
            'What vowel under the prefix consonant is decisive in distinguishing Niphal from Hiphil?',
            'Items 18 (הָסֵב, Hiphil Geminate imperative) and 20 (הֵרָאֵה, Niphal III-ה imperative) '
            'both have a long prefix vowel rather than the expected strong הַ/הִ. '
            'Explain the phonological reason for the long vowel in each case.',
        ])

        self.add_answer_key_nh(self._PART_A + self._PART_B + self._PART_C)

    def add_answer_key_nh(self, entries: list) -> None:
        self.add_section_heading('Answer Key')
        c = self._canvas
        w = self._usable_w()
        ratios = [0.04, 0.10, 0.10, 0.76]
        cw = [r * w for r in ratios]
        headers = ['#', 'Form', 'Stem', 'Answer']

        self._check_space(self.HEADER_H + len(entries) * self.ANSWER_H + 0.1*inch)
        y = self._y
        x0 = self.MARGIN_L

        c.setFillColor(C_HEADER_BG)
        c.setStrokeColor(C_RULE)
        c.setLineWidth(0.4)
        c.rect(x0, y - self.HEADER_H, sum(cw), self.HEADER_H, fill=1, stroke=1)
        cx = x0
        c.setFont('Helvetica-Bold', self.LABEL_SIZE)
        c.setFillColor(black)
        for hdr, col_w in zip(headers, cw):
            c.drawString(cx + 3, y - self.HEADER_H + 5, hdr)
            cx += col_w
        y -= self.HEADER_H

        for e in entries:
            self._check_space(self.ANSWER_H)
            c.setFillColor(C_ANSWER_BG)
            c.setStrokeColor(C_RULE)
            c.setLineWidth(0.4)
            c.rect(x0, y - self.ANSWER_H, sum(cw), self.ANSWER_H, fill=1, stroke=1)
            cx = x0
            c.setFont('Helvetica-Bold', self.LABEL_SIZE)
            c.setFillColor(C_ANSWER_FG)
            c.drawCentredString(cx + cw[0]/2, y - self.ANSWER_H + 6, e.num)
            cx += cw[0]
            c.setFont('ArialHebrew', self.LABEL_SIZE)
            c.drawRightString(cx + cw[1] - 3, y - self.ANSWER_H + 6, _heb(e.heb))
            cx += cw[1]
            c.setFont('Helvetica-Bold', self.LABEL_SIZE)
            c.drawString(cx + 3, y - self.ANSWER_H + 6, e.stem)
            cx += cw[2]
            c.setFont(_mixed_font(), self.LABEL_SIZE)
            answer = f'{e.conj} · {e.pgn} · {e.root_class} — "{e.translation}" — {e.note}'
            lines = simpleSplit(answer, _mixed_font(), self.LABEL_SIZE, cw[3] - 6)
            c.drawString(cx + 3, y - self.ANSWER_H + 6, lines[0] if lines else answer)
            y -= self.ANSWER_H

        self._y = y - 0.08 * inch


def build_ch27_nh_contrast_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch27NHContrastExercise,
        'Chapter 27 — Niphal–Hiphil Contrast Drill',
        'BBH Chapters 25 & 27 · Niphal and Hiphil Weak Verbs',
        ['hebrew', 'bbh', 'ch27', 'exercises', 'ch27-niphal-hiphil-contrast'],
        'ch27-niphal-hiphil-contrast.pdf',
        out_dir,
    )


class Ch27BGDrillExercise(ExercisePDF):
    """Biconsonantal / Geminate Disambiguation Drill — 24 items in Niphal and Hiphil."""

    _PART_A = [
        BGEntry('1',  'נָכוֹן',    'Gen 41:32',  '"the thing is ___ by God"',                    'Niphal', 'Perfect/Ptc', '3ms/ms', 'Biconsonantal', 'כּוּן',  'is established / firm',       'נָ prefix (qamets); medial ו vowel letter = Biconsonantal'),
        BGEntry('2',  'נָסַב',     '1 Kgs 7:24', '"the gourds ___ it, ten to a cubit"',          'Niphal', 'Perfect',     '3ms',    'Geminate',      'סָבַב',  'encircled / went around',     'נָ prefix (qamets); R2=R3=ב = Geminate; no medial vowel letter'),
        BGEntry('3',  'יִכּוֹן',   'Psa 93:2',   '"your throne ___ from of old"',                'Niphal', 'Imperfect',   '3ms',    'Biconsonantal', 'כּוּן',  'is established',              'יִ + dagesh in כּ + holem-vav = Niphal Biconsonantal imperfect'),
        BGEntry('4',  'יִסֹּב',    'Num 21:4',   '"they traveled ___ Mount Edom"',               'Niphal', 'Imperfect',   '3ms',    'Geminate',      'סָבַב',  'went around',                 'יִ + dagesh in סּ (R2=R3 doubled) + holem = Niphal Geminate imperfect'),
        BGEntry('5',  'הֵכּוֹן',   'Psa 57:8',   '"my heart is ___, O God"',                     'Niphal', 'Perfect',     '3ms',    'Biconsonantal', 'כּוּן',  'is ready / prepared',         'הֵ + dagesh + holem-vav = Niphal Biconsonantal; context confirms passive sense'),
        BGEntry('6',  'הֵסֹּב',    'Num 34:4',   '"your border ___ from the south"',             'Niphal', 'Perfect',     '3ms',    'Geminate',      'סָבַב',  'turned / went around',        'הֵ + dagesh in סּ (R2=R3) + holem = Niphal Geminate perfect'),
        BGEntry('7',  'נָשׁוּב',   'Lam 3:40',   '"let us examine and ___ to the LORD"',         'Niphal', 'Cohortative', '1cp',    'Biconsonantal', 'שׁוּב',  'let us return',               'נָ prefix + medial ו = Niphal Biconsonantal; cohortative force from context'),
        BGEntry('8',  'נָתֹם',     '1 Sam 3:12', '"when I ___ what I have spoken"',              'Niphal', 'Inf. Const.', '—',      'Geminate',      'תָּמַם', 'to be completed / finished',  'נָ prefix + holem = Niphal Geminate inf. construct; root R2=R3=מ'),
    ]

    _PART_B = [
        BGEntry('9',  'הֵקִים',    'Gen 6:18',   '"I will ___ my covenant with you"',            'Hiphil', 'Perfect',     '3ms',    'Biconsonantal', 'קוּם',  'established / raised up',     'הֵ prefix (tsere) = Hiphil; medial ו vowel letter = Biconsonantal'),
        BGEntry('10', 'הֵסֵב',     '2 Sam 2:22', '"___ from following me"',                      'Hiphil', 'Perfect',     '3ms',    'Geminate',      'סָבַב', 'turned aside',                'הֵ prefix (tsere) = Hiphil; no medial vowel letter, R2=R3=ב = Geminate'),
        BGEntry('11', 'יָקִים',    'Deut 18:15', '"the LORD will ___ a prophet"',                'Hiphil', 'Imperfect',   '3ms',    'Biconsonantal', 'קוּם',  'will raise up',               'יָ prefix (qamets) = Hiphil Biconsonantal imperfect; medial ו retained'),
        BGEntry('12', 'יָסֵב',     'Eccl 1:6',   '"the wind ___ to the south"',                  'Hiphil', 'Imperfect',   '3ms',    'Geminate',      'סָבַב', 'causes to go around / turns', 'יָ prefix (qamets) = Hiphil; no medial vowel letter = Geminate'),
        BGEntry('13', 'הָקֵם',     'Deut 27:26', '"\'___ the words of this law\'"',              'Hiphil', 'Imperative',  '2ms',    'Biconsonantal', 'קוּם',  'raise up! / confirm!',        'הָ prefix (qamets) = Hiphil imperative; Biconsonantal: no R2=R3 doubling'),
        BGEntry('14', 'הָסֵב',     '2 Sam 2:22', '"___ from following me"',                      'Hiphil', 'Imperative',  '2ms',    'Geminate',      'סָבַב', 'turn aside!',                 'הָ prefix (qamets) = Hiphil imperative; same vowels as Biconsonantal; root R2=R3=ב'),
        BGEntry('15', 'מֵקִים',    '1 Sam 2:8',  '"He ___ the poor from the dust"',              'Hiphil', 'Participle',  'ms',     'Biconsonantal', 'קוּם',  'one who raises up',           'מֵ prefix (tsere) = Hiphil participle; medial ו retained = Biconsonantal'),
        BGEntry('16', 'מֵסֵב',     'Ezek 41:7',  '"the structure ___ upward"',                   'Hiphil', 'Participle',  'ms',     'Geminate',      'סָבַב', 'going around / surrounding',  'מֵ prefix (tsere) = Hiphil participle; no medial vowel letter = Geminate'),
    ]

    _PART_C = [
        BGEntry('17', 'נָמֹוג',    'Isa 14:31',  '"all Philistia ___"',                          'Niphal', 'Perfect',     '3ms',    'Biconsonantal', 'מוּג',  'melted / dissolved',          'נָ prefix + medial ו = Niphal Biconsonantal; root מוּג = to melt'),
        BGEntry('18', 'הֵמַס',     'Josh 2:11',  '"the LORD ___ our hearts"',                    'Hiphil', 'Perfect',     '3ms',    'Geminate',      'מסס',   'caused to melt',              'הֵ prefix (tsere) = Hiphil; R2=R3=ס = Geminate; patach under contracted stem'),
        BGEntry('19', 'יָרֻם',     'Isa 52:13',  '"my servant shall be high and ___ up"',        'Niphal', 'Imperfect',   '3ms',    'Biconsonantal', 'רוּם',  'will be exalted / lifted up', 'יָ prefix + qibbutz under R2 (passive) = Niphal Biconsonantal; contrast Hiphil יָרִים'),
        BGEntry('20', 'יָרֹם',     'Psa 99:2',   '"great is the LORD, ___ above all peoples"',   'Niphal', 'Imperfect',   '3ms',    'Biconsonantal', 'רוּם',  'is exalted / high',           'יָ prefix + holem under R2 = Niphal Biconsonantal; compare Hiphil יָרִים (chiriq)'),
        BGEntry('21', 'הֵרִים',    'Gen 14:22',  '"I have ___ my hand to the LORD"',             'Hiphil', 'Perfect',     '3ms',    'Biconsonantal', 'רוּם',  'lifted up / swore an oath',   'הֵ prefix (tsere) + chiriq-yod = Hiphil Biconsonantal perfect; causative sense'),
        BGEntry('22', 'הוּרַם',    'Lev 4:10',   '"just as it is ___ from the peace offerings"', 'Hophal', 'Perfect',     '3ms',    'Biconsonantal', 'רוּם',  'was lifted off / removed',    'הוּ prefix (holem-vav) = Hophal (passive of Hiphil), not Niphal or Hiphil'),
        BGEntry('23', 'יָשׁוּב',   'Hos 14:8',   '"they ___ in the shade"',                      'Qal',    'Imperfect',   '3ms',    'Biconsonantal', 'שׁוּב', 'will dwell / return',         'Qal Biconsonantal — no Niphal נ or Hiphil הֵ/מֵ marker; medial ו retained'),
        BGEntry('24', 'יָשֹׁב',    'Lam 1:11',   '"all her people ___ to find bread"',           'Qal',    'Imperfect',   '3ms',    'Biconsonantal', 'שׁוּב', 'returned / went around',      'Qal Biconsonantal; holem vowel grade vs. shureq in יָשׁוּב — both Qal, not Niphal/Hiphil'),
    ]

    def _build(self) -> None:
        self.add_instructions(
            'For each form: (1) identify the stem (Niphal or Hiphil); (2) parse — conjugation, PGN; '
            '(3) identify the weak class (Biconsonantal or Geminate); (4) give the root and translate. '
            'Biconsonantal and Geminate forms are vocally identical — root knowledge is required. '
            'Answer key is on the last page.'
        )

        self.add_note(
            'Biconsonantal (II-י/ו): medial vowel letter ו or י retained in stem (e.g. קוּם, שׁוּב, כּוּן). '
            'Geminate (R2=R3): same consonant at R2 and R3; no medial vowel letter (e.g. סָבַב, תָּמַם). '
            'Both classes share: Niphal perfect נָ (qamets); Hiphil perfect הֵ (tsere); '
            'Hiphil imperfect יָ (qamets); Hiphil imperative הָ (qamets); Hiphil participle מֵ (tsere).'
        )

        self.add_section_heading('Part A — Niphal: Biconsonantal vs. Geminate')
        self.add_note(
            'All forms are Niphal. Identify whether each is Biconsonantal (medial ו/י) or Geminate (R2=R3). '
            'The prefix vowel pattern (נָ in perfect; יִ in imperfect) is identical for both classes.'
        )
        self.add_bg_table(self._PART_A, show_answers=False)

        self.add_section_heading('Part B — Hiphil: Biconsonantal vs. Geminate')
        self.add_note(
            'All forms are Hiphil. Hiphil prefix patterns: הֵ (perfect) · יָ (imperfect) · הָ (imperative) · מֵ (participle). '
            'These are identical for Biconsonantal and Geminate — root knowledge is the only distinguisher.'
        )
        self.add_bg_table(self._PART_B, show_answers=False)

        self.add_section_heading('Part C — Mixed: Stem and Class Both Unknown')
        self.add_note(
            'Identify both the stem (Niphal/Hiphil/Qal/Hophal) and the class. '
            'Part C includes Qal and Hophal forms as distractors — not every Biconsonantal form is Niphal or Hiphil.'
        )
        self.add_bg_table(self._PART_C, show_answers=False)

        self.add_reflection([
            'Items 1 (נָכוֹן) and 2 (נָסַב) have the same נָ prefix. What is the only reliable way '
            'to identify נָכוֹן as Biconsonantal (root כּוּן) and נָסַב as Geminate (root סָבַב)?',
            'Items 9 (הֵקִים) and 10 (הֵסֵב) both have הֵ prefix (tsere). One retains a medial vowel '
            'letter; the other shows a contracted stem. Describe precisely what the medial position '
            'of each form looks like and how that reflects the root structure.',
            'Items 11 (יָקִים) and 12 (יָסֵב) are both Hiphil imperfect 3ms. You encounter an unknown '
            'form יָדֵל. What question must you ask to determine if it is Biconsonantal or Geminate?',
            'Items 19 (יָרֻם) and 21 (הֵרִים) come from the same root (רוּם) but differ in stem. '
            'What vowel under R2 distinguishes the Niphal imperfect from the Hiphil perfect?',
            'Item 22 (הוּרַם) was classified as Hophal. How does the Hophal Biconsonantal prefix (הוּ) '
            'differ from Niphal (נָ) and Hiphil (הֵ), and what does it tell you about the semantics?',
        ])

        self.add_answer_key_bg(self._PART_A + self._PART_B + self._PART_C)

    def add_answer_key_bg(self, entries: list) -> None:
        self.add_section_heading('Answer Key')
        c = self._canvas
        w = self._usable_w()
        ratios = [0.04, 0.10, 0.10, 0.76]
        cw = [r * w for r in ratios]
        headers = ['#', 'Form', 'Stem', 'Answer']

        self._check_space(self.HEADER_H + len(entries) * self.ANSWER_H + 0.1*inch)
        y = self._y
        x0 = self.MARGIN_L

        c.setFillColor(C_HEADER_BG)
        c.setStrokeColor(C_RULE)
        c.setLineWidth(0.4)
        c.rect(x0, y - self.HEADER_H, sum(cw), self.HEADER_H, fill=1, stroke=1)
        cx = x0
        c.setFont('Helvetica-Bold', self.LABEL_SIZE)
        c.setFillColor(black)
        for hdr, col_w in zip(headers, cw):
            c.drawString(cx + 3, y - self.HEADER_H + 5, hdr)
            cx += col_w
        y -= self.HEADER_H

        for e in entries:
            self._check_space(self.ANSWER_H)
            c.setFillColor(C_ANSWER_BG)
            c.setStrokeColor(C_RULE)
            c.setLineWidth(0.4)
            c.rect(x0, y - self.ANSWER_H, sum(cw), self.ANSWER_H, fill=1, stroke=1)
            cx = x0
            c.setFont('Helvetica-Bold', self.LABEL_SIZE)
            c.setFillColor(C_ANSWER_FG)
            c.drawCentredString(cx + cw[0]/2, y - self.ANSWER_H + 6, e.num)
            cx += cw[0]
            c.setFont('ArialHebrew', self.LABEL_SIZE)
            c.drawRightString(cx + cw[1] - 3, y - self.ANSWER_H + 6, _heb(e.heb))
            cx += cw[1]
            c.setFont('Helvetica-Bold', self.LABEL_SIZE)
            c.drawString(cx + 3, y - self.ANSWER_H + 6, e.stem)
            cx += cw[2]
            c.setFont(_mixed_font(), self.LABEL_SIZE)
            answer = f'{e.conj} · {e.pgn} · {e.bg_class} · {e.root} — "{e.translation}" — {e.note}'
            lines = simpleSplit(answer, _mixed_font(), self.LABEL_SIZE, cw[3] - 6)
            c.drawString(cx + 3, y - self.ANSWER_H + 6, lines[0] if lines else answer)
            y -= self.ANSWER_H

        self._y = y - 0.08 * inch


def build_ch27_bg_drill_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch27BGDrillExercise,
        'Chapter 27 — Biconsonantal / Geminate Disambiguation Drill',
        'BBH Chapters 25 & 27 · Niphal and Hiphil Weak Verbs',
        ['hebrew', 'bbh', 'ch27', 'exercises', 'ch27-biconsig-drill'],
        'ch27-biconsig-drill.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 27 — Qal–Hiphil Contrast Drill (Weak Verbs)
# ---------------------------------------------------------------------------


class Ch27ContrastExercise(ExercisePDF):

    _ENTRIES_A = [
        ContrastEntry('1',  'יָדַע', 'to know',        'הוֹדִיעַ', 'Perfect 3ms',    'Deu 4:9',   'he made known / declared',       'Causative',      'Causing others to know; Qal = to know'),
        ContrastEntry('2',  'יָצָא', 'to go out',       'הוֹצִיא', 'Perfect 3ms',    'Gen 15:7',  'he brought out',                 'Causative',      'God caused Abram to exit Ur; Qal = go out'),
        ContrastEntry('3',  'יָשַׁב', 'to sit, dwell',  'הוֹשִׁיב', 'Wayyiqtol 3ms', 'Gen 47:11', 'he settled them (in the land)',  'Causative',      'Joseph caused his family to dwell; Qal = sit/dwell'),
        ContrastEntry('4',  'נָפַל', 'to fall',         'הִפִּיל', 'Wayyiqtol 3ms',  'Gen 2:21',  'he caused to fall / cast down',  'Causative',      'God caused deep sleep to fall on Adam; Qal = fall'),
        ContrastEntry('5',  'נָגַשׁ', 'to draw near',   'הִגִּישׁ', 'Wayyiqtol 3ms', 'Gen 43:31', 'he set before them / brought near', 'Causative',   'Joseph caused food to be set before them; Qal = draw near'),
    ]
    _ENTRIES_B = [
        ContrastEntry('6',  'בּוֹא', 'to come, go in',  'הֵבִיא', 'Perfect 3ms',    'Gen 43:17', 'he brought',                    'Causative',      'Brothers caused to come to Joseph\'s house; Qal = come'),
        ContrastEntry('7',  'שׁוּב', 'to return',        'הֵשִׁיב', 'Wayyiqtol 3ms', 'Gen 42:25', 'he gave back / returned it',    'Causative',      'Joseph caused the silver to be returned; Qal = return'),
        ContrastEntry('8',  'קוּם', 'to rise, stand',   'הֵקִים', 'Wayyiqtol 3ms',  'Gen 6:18',  'he established / confirmed',    'Causative',      'God caused the covenant to stand; Qal = rise/stand'),
        ContrastEntry('9',  'מוּת', 'to die',            'יָמִית', 'Imperfect 3ms',  'Deu 17:12', 'he will put to death',          'Causative',      'Causing death; Qal = die'),
        ContrastEntry('10', 'שִׂים', 'to set, put',      'יָשִׂים', 'Imperfect 3ms', 'Gen 24:2',  'he will put / place',           'Simple Action',  'Hiphil = primary usage for placing; Qal rare in same sense'),
    ]
    _ENTRIES_C = [
        ContrastEntry('11', 'עָלָה', 'to go up',        'הֶעֱלָה', 'Perfect 3ms',    'Gen 46:4',   'he brought up',          'Causative',      'God caused Jacob to go up to Egypt; Qal = go up'),
        ContrastEntry('12', 'רָאָה', 'to see',           'הֶרְאָה', 'Perfect 3ms',    'Deu 34:1',   'he showed',              'Causative',      'LORD caused Moses to see the land; Qal = see'),
        ContrastEntry('13', 'נָטָה', 'to stretch out',   'הִטָּה',  'Wayyiqtol 3ms', 'Exo 10:13',  'he stretched out',       'Causative',      'Moses stretched out his staff; Qal = extend/stretch'),
        ContrastEntry('14', 'גָּלָה', 'to go into exile', 'הִגְלָה', 'Perfect 3ms',   '2 Kgs 17:6', 'he exiled / sent into exile', 'Causative', 'King caused Israel to go into exile; Qal = go into exile'),
        ContrastEntry('15', 'הָיָה', 'to be',            'יֶהְיֶה', 'Imperfect 3ms', '—',          'it will be / come about', 'Simple Action', 'III-ה root; Hiphil rare in this sense; Qal = be/become'),
    ]

    def _build(self) -> None:
        self.add_instructions(
            'For each item: (1) write an English translation of the Hiphil form in the Translation '
            'column; (2) write the semantic function (Causative / Factitive / Declarative / Simple '
            'Action) in the Function column. Answer key is on the last page.'
        )

        self.add_section_heading('Part A — I-י / I-נ Weak Roots')
        self.add_note('These roots lose or assimilate their first consonant in the Hiphil. The causative relationship with the Qal is preserved.')
        self.add_contrast_table(self._ENTRIES_A, show_answers=False)

        self.add_section_heading('Part B — Hollow Roots (I/II-ו/י)')
        self.add_note(
            'Hollow roots contract the middle vowel-letter in Hiphil. '
            'Identify the two outer consonants, then apply the causative logic.'
        )
        self.add_contrast_table(self._ENTRIES_B, show_answers=False)

        self.add_section_heading('Part C — III-ה Weak Roots')
        self.add_note('III-ה roots add a ה in Hiphil Perfect (הֶ prefix + ָה suffix) and drop the ה in prefix conjugations.')
        self.add_contrast_table(self._ENTRIES_C, show_answers=False)

        self.add_reflection([
            'In Part A, the I-י roots (יָדַע, יָצָא, יָשַׁב) all use הוֹ– as the Hiphil prefix. '
            'What happens to the initial י? Describe the contraction in one sentence.',
            'Items 8 (קוּם) and 9 (מוּת) are both hollow roots classified as Causative. '
            'Can a hollow root ever produce a Factitive or Declarative Hiphil? Give a reason for your answer.',
            'Compare עָלָה in Ch26\'s exercise and item 11 here. Both use the same root, but item 11 '
            'is a Perfect rather than Imperative. Does the weak-root form change your ability to recognize it as Hiphil?',
        ])

        self.add_answer_key_contrast(self._ENTRIES_A + self._ENTRIES_B + self._ENTRIES_C)


def build_ch27_contrast_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch27ContrastExercise,
        'Chapter 27 — Qal–Hiphil Contrast Drill (Weak Verbs)',
        'BBH Chapter 27 · Hiphil Weak Verbs',
        ['hebrew', 'bbh', 'ch27', 'exercises', 'ch27-qal-hiphil-contrast'],
        'ch27-qal-hiphil-contrast.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 27 — Semantic Function Sorting (Weak Roots)
# ---------------------------------------------------------------------------


class Ch27FunctionSortExercise(ExercisePDF):

    _ENTRIES = [
        SortEntry('1',  'הוֹצִיא',   'Perfect 3ms',    'Gen 15:7',   '"I am the LORD who brought you out of Ur"',                       'C',  'יָצָא',  'Qal = go out; Hiphil = cause to go out / bring out'),
        SortEntry('2',  'הוֹשִׁיב',  'Wayyiqtol 3ms',  'Gen 47:11',  '"Joseph settled his father and brothers in Egypt"',               'C',  'יָשַׁב', 'Qal = sit/dwell; Hiphil = cause to dwell / settle'),
        SortEntry('3',  'הוֹדִיעַ',  'Perfect 3ms',    'Deu 4:9',    '"make them known to your children and grandchildren"',            'C',  'יָדַע',  'Qal = know; Hiphil = cause to know / make known'),
        SortEntry('4',  'הֵבִיא',    'Perfect 3ms',    'Gen 43:17',  '"the man brought Joseph\'s brothers into Joseph\'s house"',        'C',  'בּוֹא',  'Qal = come; Hiphil = cause to come / bring'),
        SortEntry('5',  'הֵשִׁיב',   'Wayyiqtol 3ms',  'Gen 42:25',  '"Joseph commanded that each man\'s money be returned"',           'C',  'שׁוּב',  'Qal = return; Hiphil = cause to return / give back'),
        SortEntry('6',  'הֵקִים',    'Wayyiqtol 3ms',  'Gen 6:18',   '"I will establish my covenant with you"',                         'C',  'קוּם',  'Qal = rise/stand; Hiphil = cause to stand / establish'),
        SortEntry('7',  'יָמִית',    'Imperfect 3ms',  'Deu 17:12',  '"that man shall be put to death"',                               'C',  'מוּת',  'Qal = die; Hiphil = cause to die / put to death'),
        SortEntry('8',  'הִפִּיל',   'Wayyiqtol 3ms',  'Gen 2:21',   '"the LORD caused a deep sleep to fall on the man"',               'C',  'נָפַל',  'Qal = fall; Hiphil = cause to fall / cast down'),
        SortEntry('9',  'הִגִּישׁ',  'Wayyiqtol 3ms',  'Gen 43:31',  '"Joseph set the meal before them"',                              'C',  'נָגַשׁ', 'Qal = draw near; Hiphil = cause to draw near / set before'),
        SortEntry('10', 'הֶעֱלָה',   'Perfect 3ms',    'Gen 46:4',   '"I will also bring you up again"',                               'C',  'עָלָה',  'Qal = go up; Hiphil = cause to go up / bring up'),
        SortEntry('11', 'הֶרְאָה',   'Perfect 3ms',    'Deu 34:1',   '"the LORD showed him all the land"',                             'C',  'רָאָה',  'Qal = see; Hiphil = cause to see / show'),
        SortEntry('12', 'הִטָּה',    'Wayyiqtol 3ms',  'Exo 10:13',  '"Moses stretched out his staff over Egypt"',                     'C',  'נָטָה',  'Qal = extend/stretch; Hiphil = cause to extend / stretch out'),
        SortEntry('13', 'הִגְלָה',   'Perfect 3ms',    '2 Kgs 17:6', '"the king of Assyria exiled Israel to Assyria"',                 'C',  'גָּלָה', 'Qal = go into exile; Hiphil = cause to go into exile / exile'),
        SortEntry('14', 'הֵרַע',     'Perfect 3ms',    'Gen 19:9',   '"now we will deal worse with you than with them"',               'F',  'רָעַע',  'Qal = be bad; Hiphil = make worse / treat badly'),
        SortEntry('15', 'הֶחֱיָה',   'Wayyiqtol 3ms',  'Gen 47:25',  '"you have saved our lives!"',                                    'C',  'חָיָה',  'Qal = live; Hiphil = cause to live / save alive'),
        SortEntry('16', 'הִשְׁחִית', 'Wayyiqtol 3ms',  'Gen 6:12',   '"for all flesh had corrupted its way on earth"',                 'SA', 'שָׁחַת', 'Hiphil = destroy/corrupt; Niphal = be destroyed; Hiphil is primary usage'),
        SortEntry('17', 'הֵרִים',    'Wayyiqtol 3ms',  'Gen 22:10',  '"Abraham reached out his hand and lifted the knife"',            'C',  'רוּם',   'Qal = be high/rise; Hiphil = cause to rise / lift up'),
        SortEntry('18', 'הֵשִׁיב',   'Perfect 3ms',    'Num 23:20',  '"I have received a command to bless"',                           'C',  'שׁוּב',  'Qal = return; Hiphil = receive back / cause to return (blessing)'),
        SortEntry('19', 'הֵמִיר',    'Perfect 3ms',    'Lev 27:10',  '"he shall not exchange it or substitute it"',                    'SA', 'מוּר',   'To exchange/substitute; Hiphil is primary form for this meaning'),
        SortEntry('20', 'יַשְׁמִיעַ', 'Imperfect 3ms', 'Deu 4:36',   '"from heaven he made you hear his voice"',                       'C',  'שָׁמַע', 'Qal = hear; Hiphil = cause to hear / proclaim'),
        SortEntry('21', 'הֵבִין',    'Perfect 3ms',    'Neh 8:8',    '"they gave the sense so that the people understood"',            'C',  'בִּין',   'Qal = understand; Hiphil = cause to understand / give understanding'),
        SortEntry('22', 'הִרְבָּה',  'Perfect 3ms',    'Gen 22:17',  '"I will greatly multiply your offspring"',                       'C',  'רָבָה',  'Qal = be many; Hiphil = cause to be many / multiply'),
        SortEntry('23', 'הִגְדִּיל', 'Perfect 3ms',    'Joel 2:21',  '"for the LORD has done great things"',                           'F',  'גָּדַל', 'Qal = be great; Hiphil = cause greatness / do great things'),
        SortEntry('24', 'הִכְשִׁיל', 'Perfect 3ms',    'Lam 1:14',   '"he made my strength fail / he caused me to stumble"',          'C',  'כָּשַׁל', 'Qal = stumble; Hiphil = cause to stumble / make strength fail'),
    ]

    def _build(self) -> None:
        self.add_instructions(
            'Classify each Hiphil verb as C (Causative), F (Factitive), D (Declarative), '
            'SA (Simple Action), or DN (Denominative). Write your answer in the Function column. '
            'All roots are weak roots from Ch27 weak classes. Answer key is on the last page.'
        )

        self.add_note(
            'C = Causative (subject causes another to act/experience)  |  '
            'F = Factitive (subject causes object to be in a state)  |  '
            'D = Declarative (subject declares something as being in a state)  |  '
            'SA = Simple Action (Hiphil is the standard form; no common Qal)  |  '
            'DN = Denominative (Hiphil derived from a noun)'
        )

        self.add_sort_table(self._ENTRIES, show_answers=False)

        self.add_reflection([
            'Items 1, 2, 4, 8, 10, 12, 13 are all Causative. What do the underlying Qal roots have '
            'in common — motion, state, or position — that makes the Causative reading natural?',
            'Item 6 (קוּם, "to rise / stand") is Causative: God caused the covenant to stand. '
            'How is this different from Factitive? (Hint: what is the "object" being caused — a state or an action?)',
            'Items 21 (הֵבִין, "to understand") and 22 (הִרְבָּה, "to multiply") are both Causative. '
            'Identify the Qal meaning for each root and explain how the Hiphil extends it.',
        ])

        self.add_answer_key_sort(self._ENTRIES)


def build_ch27_function_sort_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch27FunctionSortExercise,
        'Chapter 27 — Semantic Function Sorting (Weak Roots)',
        'BBH Chapter 27 · Hiphil Weak Verbs',
        ['hebrew', 'bbh', 'ch27', 'exercises', 'ch27-function-sort'],
        'ch27-function-sort.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 27 — Qal / Niphal / Hiphil Stem Identification Drill (Weak Roots)
# ---------------------------------------------------------------------------
_CH27_STEM_ROWS = [
    ['1',  'יָלַד',       '',  '',              '',    ''],
    ['2',  'הוֹלִיד',     '',  '',              '',    ''],
    ['3',  'נוֹלַד',      '',  '',              '',    ''],
    ['4',  'שָׁב',        '',  '',              '',    ''],
    ['5',  'הֵשִׁיב',     '',  '',              '',    ''],
    ['6',  'נָשׁוּב',     '',  '',              '',    ''],
    ['7',  'עָלָה',       '',  '',              '',    ''],
    ['8',  'הֶעֱלָה',     '',  '',              '',    ''],
    ['9',  'נַעֲלָה',     '',  '',              '',    ''],
    ['10', 'יָשׁוּב',     '',  '',              '',    ''],
    ['11', 'יָשִׁיב',     '',  '',              '',    ''],
    ['12', 'יִוָּלֵד',    '',  '',              '',    ''],
    ['13', 'וַיָּשָׁב',   '',  '',              '',    ''],
    ['14', 'וַיָּשֶׁב',   '',  '',              '',    ''],
    ['15', 'וַיִּוָּלֵד', '',  '',              '',    ''],
    ['16', 'שׁוּב',       '',  '',              '',    ''],
    ['17', 'הָשֵׁב',      '',  '',              '',    ''],
    ['18', 'עֲלֵה',       '',  '',              '',    ''],
    ['19', 'עָלֹה',       '',  '',              '',    ''],
    ['20', 'הַעֲלֵה',     '',  '',              '',    ''],
    ['21', 'הֵעָלוֹת',    '',  '',              '',    ''],
    ['22', 'שָׁב',        '',  '',              '',    ''],
    ['23', 'מֵשִׁיב',     '',  '',              '',    ''],
    ['24', 'נוֹלָד',      '',  '',              '',    ''],
]
_CH27_STEM_ANS = [
    ['1',  'יָלַד',       'Qal',    'Perfect',         '3ms', 'ילד'],
    ['2',  'הוֹלִיד',     'Hiphil', 'Perfect',         '3ms', 'ילד'],
    ['3',  'נוֹלַד',      'Niphal', 'Perfect',         '3ms', 'ילד'],
    ['4',  'שָׁב',        'Qal',    'Perfect',         '3ms', 'שׁוב'],
    ['5',  'הֵשִׁיב',     'Hiphil', 'Perfect',         '3ms', 'שׁוב'],
    ['6',  'נָשׁוּב',     'Niphal', 'Perfect',         '3ms', 'שׁוב'],
    ['7',  'עָלָה',       'Qal',    'Perfect',         '3ms', 'עלה'],
    ['8',  'הֶעֱלָה',     'Hiphil', 'Perfect',         '3ms', 'עלה'],
    ['9',  'נַעֲלָה',     'Niphal', 'Perfect',         '3ms', 'עלה'],
    ['10', 'יָשׁוּב',     'Qal',    'Imperfect',       '3ms', 'שׁוב'],
    ['11', 'יָשִׁיב',     'Hiphil', 'Imperfect',       '3ms', 'שׁוב'],
    ['12', 'יִוָּלֵד',    'Niphal', 'Imperfect',       '3ms', 'ילד'],
    ['13', 'וַיָּשָׁב',   'Qal',    'Wayyiqtol',      '3ms', 'שׁוב'],
    ['14', 'וַיָּשֶׁב',   'Hiphil', 'Wayyiqtol',      '3ms', 'שׁוב'],
    ['15', 'וַיִּוָּלֵד', 'Niphal', 'Wayyiqtol',      '3ms', 'ילד'],
    ['16', 'שׁוּב',       'Qal',    'Imperative',      '2ms', 'שׁוב'],
    ['17', 'הָשֵׁב',      'Hiphil', 'Imperative',      '2ms', 'שׁוב'],
    ['18', 'עֲלֵה',       'Qal',    'Imperative',      '2ms', 'עלה'],
    ['19', 'עָלֹה',       'Qal',    'Inf. Absolute',   '—',   'עלה'],
    ['20', 'הַעֲלֵה',     'Hiphil', 'Imperative',      '2ms', 'עלה'],
    ['21', 'הֵעָלוֹת',    'Niphal', 'Inf. Construct',  '—',   'עלה'],
    ['22', 'שָׁב',        'Qal',    'Participle',      'ms',  'שׁוב'],
    ['23', 'מֵשִׁיב',     'Hiphil', 'Participle',      'ms',  'שׁוב'],
    ['24', 'נוֹלָד',      'Niphal', 'Participle',      'ms',  'ילד'],
]


class Ch27StemIdDrill(ExercisePDF):
    _instructions = (
        'For each verb form, identify the stem (Qal / Niphal / Hiphil), '
        'then fill in the conjugation, PGN (person–gender–number), and root. '
        'All 24 forms come from weak roots: I-י (ילד), Hollow (שׁוב), and III-ה (עלה). '
        'Notice that the same root appears in multiple stems — the vowel patterns and prefixes distinguish them. '
        'Non-finite forms: enter — in PGN, or note gender for participles.'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'Hebrew Form', 'Stem', 'Conjugation', 'PGN', 'Root']
        cr   = [0.05, 0.18, 0.15, 0.22, 0.15, 0.25]
        self.add_drill_with_answer_key(
            hdrs, _CH27_STEM_ROWS, _CH27_STEM_ANS,
            col_ratios=cr,
            heb_cols=[1],
            answer_heb_cols=[5],
            section_title='Qal / Niphal / Hiphil — Weak Roots',
        )


def build_ch27_stem_id_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch27StemIdDrill,
        'Chapter 27 — Qal / Niphal / Hiphil Stem Identification Drill (Weak Roots)',
        'BBH Chapter 27 · Hiphil Weak Verbs',
        ['hebrew', 'bbh', 'ch27', 'exercises', 'ch27-stem-id-drill'],
        'ch27-stem-id-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 30 — "Spot the Piel" Passage Exercise (Piel Strong)
# ---------------------------------------------------------------------------


class Ch30PielExercise(PassageExercise):
    _instructions = (
        'Each numbered verb belongs to one of the stems you have already studied '
        '(Qal, Niphal, Hiphil, Hophal, or Piel). '
        'For each one, fill in: Piel? (Yes/No), Conjugation, PGN, Root, and Stem/Function. '
        'The answer key begins on the page marked "Answer Key".'
    )

    def _render_passages(self, show_answers: bool) -> None:

        # ── Passage A ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage A — Genesis 1:22, 28')

        self.add_passage(PassageBlock('1:22',
            'וַיְבָ֧רֶךְ אֹתָ֛ם אֱלֹהִ֖ים לֵאמֹ֑ר פְּר֥וּ וּרְב֛וּ',
            '"And God blessed them, saying, \'Be fruitful and multiply…\'"'))
        self.add_verb_table([
            VerbEntry('1', 'וַיְבָרֶךְ', 'Wayyiqtol', '3ms', 'בָּרַךְ', 'Intensive — God\'s blessing; Piel Wayyiqtol וַיְ prefix'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('1:28',
            'וַיְבָ֣רֶךְ אֹתָ֖ם אֱלֹהִ֑ים',
            '"And God blessed them."'))
        self.add_verb_table([
            VerbEntry('2', 'וַיְבָרֶךְ', 'Wayyiqtol', '3ms', 'בָּרַךְ', 'Intensive — same form; R2=ר rejects dagesh; Piel marked by vowel pattern'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage B — Exodus 19:10–14')

        self.add_passage(PassageBlock('19:10',
            'וְקִדַּשְׁתָּ֥ אֹתָ֛ם הַיּ֥וֹם וּמָחָ֑ר וְכִבְּס֖וּ שִׂמְלֹתָֽם',
            '"…consecrate them today and tomorrow, and let them wash their garments."'))
        self.add_verb_table([
            VerbEntry('3', 'וְקִדַּשְׁתָּ', 'Weqatal', '2ms', 'קָדַשׁ', 'Factitive — cause to become holy; Weqatal = consequential command'),
            VerbEntry('4', 'וְכִבְּסוּ', 'Weqatal', '3cp', 'כָּבַס', 'Intensive — wash/launder; roots almost exclusively Piel OT-wide'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('19:14',
            'וַיְקַדֵּ֖שׁ אֶת־הָעָ֑ם וַיְכַבְּס֖וּ שִׂמְלֹתָֽם',
            '"…and he consecrated the people, and they washed their garments."'))
        self.add_verb_table([
            VerbEntry('5', 'וַיְקַדֵּשׁ', 'Wayyiqtol', '3ms', 'קָדַשׁ', 'Factitive — narrative fulfillment of command (v.10); same root'),
            VerbEntry('6', 'וַיְכַבְּסוּ', 'Wayyiqtol', '3mp', 'כָּבַס', 'Intensive — Wayyiqtol 3mp; contrast with Weqatal 3cp above'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('19:25',
            'וַיְדַבֵּ֥ר מֹשֶׁ֖ה אֶל־הָעָ֑ם',
            '"And Moses spoke to the people."'))
        self.add_verb_table([
            VerbEntry('7', 'וַיְדַבֵּר', 'Wayyiqtol', '3ms', 'דָּבַר', 'Denominative — from דָּבָר (word); 1,090x in OT; Piel is the standard form'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B insert — Exo 19:13 (Hophal distractor) ─────────────────
        self.add_passage(PassageBlock('19:13',
            'סָקוֹל יִסָּקֵל אוֹ יָרֹה יִיָּרֶה אִם בְּהֵמָה אִם אִישׁ לֹא יִחְיֶה',
            '"Whether beast or man, he shall not live — he shall be stoned or shot."'))
        self.add_verb_table([
            VerbEntry('8', 'יִסָּקֵל', 'Niphal Impf.', '3ms', 'סָקַל', 'NOT Piel — Niphal passive: "shall be stoned"; נִ-prefix contracts to יִ + dagesh; passive of Qal'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage C ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage C — Numbers 22:6–8, 17 (with Qal/Hophal distractors)')

        self.add_passage(PassageBlock('22:6',
            'לְכָה נָּא אָרָה לִּי אֶת הָעָם הַזֶּה כִּי יָדַעְתִּי אֵת אֲשֶׁר תְּבָרֵךְ מְבֹרָךְ [not numbered — Ch32] וַאֲשֶׁר תָּאֹר יוּאָר',
            '"Come now, curse this people for me… he whom you bless is blessed [Ch32 Pual — not numbered], and he whom you curse is cursed."'))
        self.add_verb_table([
            VerbEntry('9',  'אָרָה',     'Qal Jussive',  '1cs', 'אָרַר', 'NOT Piel — Qal jussive (curse); no dagesh in R2'),
            VerbEntry('10', 'תְּבָרֵךְ', 'Imperfect',    '2ms', 'בָּרַךְ', 'Intensive (Piel) — תְּ prefix + patach + tsere; R2=ר rejects dagesh'),
            VerbEntry('11', 'יוּאָר',   'Hophal Impf.', '3ms', 'אָרַר', 'NOT Piel — Hophal (shall be cursed); יוּ prefix = u-class vowel under prefix = Hophal marker'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('22:8',
            'יְדַבֵּר יְהוָה אֵלָי וְדִבַּרְתִּי אֲלֵיכֶם',
            '"The LORD will speak to me, and I will speak to you."'))
        self.add_verb_table([
            VerbEntry('12', 'יְדַבֵּר',    'Imperfect', '3ms', 'דָּבַר', 'Denominative — יְ prefix + dagesh in בּ; standard Piel Imperfect'),
            VerbEntry('13', 'וְדִבַּרְתִּי', 'Weqatal',   '1cs', 'דָּבַר', 'Denominative — Weqatal; Hireq under R1 + dagesh + 1cs suffix תִּי'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('22:17',
            'כִּי כַבֵּד אֲכַבֶּדְךָ מְאֹד וּלְכָה נָּא קָבָה לִי אֶת הָעָם הַזֶּה',
            '"For I will surely honor you greatly; come now, curse this people for me."'))
        self.add_verb_table([
            VerbEntry('14', 'כַּבֵּד',    'Inf. Absolute', '—',  'כָּבֵד', 'Intensive (Piel Inf.Abs.) — cognate construction כַּבֵּד אֲכַבֶּד'),
            VerbEntry('15', 'אֲכַבֶּדְךָ', 'Imperfect',    '1cs', 'כָּבֵד', 'Factitive — אֲ prefix + dagesh in בּ; Piel of "heavy" = to honor'),
            VerbEntry('16', 'קָבָה',      'Qal Impv.',    '2ms', 'קָבַב',  'NOT Piel — Qal imperative (curse geminate root); no dagesh in R2'),
        ], show_answers=show_answers)


def build_ch30_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch30PielExercise,
        'Chapter 30 — "Spot the Piel" Passage Exercise',
        'Gen 1  ·  Exo 19  ·  Num 22',
        ['hebrew', 'bbh', 'ch30', 'exercises', 'ch30-passage-exercise'],
        'ch30-passage-exercise.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 28 — "Spot the Hophal" Passage Exercise (correct: Hophal Strong)
# ---------------------------------------------------------------------------


class Ch28HophalExercise(PassageExercise):
    _instructions = (
        'Each numbered verb belongs to one of the stems you have already studied '
        '(Qal, Niphal, Hiphil, or Hophal). '
        'For each one, fill in: Hophal? (Yes/No), Conjugation, PGN, Root, and Stem/Function. '
        'The answer key begins on the page marked "Answer Key".'
    )

    def _render_passages(self, show_answers: bool) -> None:

        # ── Passage A ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage A — Genesis 22:20')

        self.add_passage(PassageBlock('22:20',
            'וַיְהִ֗י אַֽחֲרֵי֙ הַדְּבָרִ֣ים הָאֵ֔לֶּה וַיֻּגַּ֥ד לְאַבְרָהָ֖ם לֵאמֹֽר',
            '"Now after these things it was told to Abraham, saying…"'))
        self.add_verb_table([
            VerbEntry('1', 'וַיֻּגַּד', 'Wayyiqtol', '3ms', 'נָגַד', 'Hiphil הִגִּיד = to tell/declare → Hophal = it was reported'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage B — Exodus 5:14–16 (with Niphal distractor)')

        self.add_passage(PassageBlock('5:14',
            'וַיֻּכּ֗וּ שֹׁטְרֵי֙ בְּנֵ֣י יִשְׂרָאֵ֔ל אֲשֶׁר־שָׂ֣מוּ עֲלֵהֶ֔ם נֹגְשֵׂ֥י פַרְעֹ֖ה',
            '"And the overseers of the people of Israel were beaten…"'))
        self.add_verb_table([
            VerbEntry('2', 'וַיֻּכּוּ', 'Wayyiqtol', '3mp', 'נָכָה', 'Hiphil הִכָּה = to strike/kill → Hophal = were beaten'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('5:16',
            'תֶּ֗בֶן אֵ֤ין נִתָּן֙ לַעֲבָדֶ֔יךָ וְהִנֵּ֧ה עֲבָדֶ֛יךָ מֻכִּ֖ים',
            '"No straw is given to your servants, and behold, your servants are being beaten…"'))
        self.add_verb_table([
            VerbEntry('3', 'נִתָּן', 'Niphal Ptc.', 'ms', 'נָתַן', 'NOT Hophal — Niphal passive of Qal נָתַן (given); נ prefix'),
            VerbEntry('4', 'מֻכִּים', 'Participle', 'mp', 'נָכָה', 'Hophal — מֻ prefix (Qibbuts) = u-class vowel; passive of Hiphil הִכָּה'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage C ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage C — Numbers 35:16–18, 30–31 (Qal distractors)')

        self.add_passage(PassageBlock('35:16',
            'וְאִם בִּכְלִי בַרְזֶל הִכָּהוּ וַיָּמֹת מוֹת־יוּמַת הָרֹצֵֽחַ',
            '"If he struck him with iron and he died — the murderer shall surely be put to death."'))
        self.add_verb_table([
            VerbEntry('5', 'יוּמַת', 'Imperfect', '3ms', 'מוּת', 'Hophal — יוּ prefix (Shureq); Hiphil הֵמִית = to put to death'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('35:17',
            'וְאִם בְּאֶבֶן יָד אֲשֶׁר־יָמוּת בָּהּ הִכָּהוּ וַיָּמֹת מוֹת־יוּמַת הָרֹצֵֽחַ',
            '"If with a stone that could kill he struck him and he died — the murderer shall be put to death."'))
        self.add_verb_table([
            VerbEntry('6', 'יָמוּת', 'Qal Impf.', '3ms', 'מוּת', 'NOT Hophal — Qal intransitive "to die"; יָ prefix (Patach) ≠ Hophal'),
            VerbEntry('7', 'יוּמַת', 'Imperfect', '3ms', 'מוּת', 'Hophal — יוּ prefix (Shureq); same formula as verb 5'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('35:30–31',
            'עַל־פִּי עֵדִים יֵרָצֵחַ הָרֹצֵחַ … כִּי־מוֹת יוּמָת',
            '"On the testimony of witnesses the murderer shall be put to death… for he shall surely be put to death."'))
        self.add_verb_table([
            VerbEntry('8', 'יֵרָצֵחַ', 'Niphal Impf.', '3ms', 'רָצַח', 'NOT Hophal — Niphal (passive of Qal murder); יֵ prefix, no u-vowel'),
            VerbEntry('9', 'יוּמַת', 'Imperfect', '3ms', 'מוּת', 'Hophal — יוּ prefix (Shureq); death penalty formula'),
        ], show_answers=show_answers)


def build_ch28_hophal_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch28HophalExercise,
        'Chapter 28 — "Spot the Hophal" Passage Exercise',
        'Genesis 22  ·  Exodus 5  ·  Numbers 35',
        ['hebrew', 'bbh', 'ch28', 'exercises', 'ch28-passage-exercise'],
        'ch28-passage-exercise.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 34 — "Spot the Hithpael" Passage Exercise (Strong Verbs)
# ---------------------------------------------------------------------------


class Ch34HithpaelExercise(PassageExercise):
    _instructions = (
        'Each numbered verb belongs to one of the stems you have already studied '
        '(Qal, Niphal, Hiphil, Hophal, Piel, Pual, or Hithpael). '
        'Focus: strong roots in the Hithpael stem. '
        'For each one, fill in: Hithpael? (Yes/No), Conjugation, PGN, Root, and Stem/Function. '
        'The answer key begins on the page marked "Answer Key".'
    )

    def _render_passages(self, show_answers: bool) -> None:

        # ── Passage A ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage A — 1 Kings 8:28–30 · Genesis 20:7')

        self.add_passage(PassageBlock('8:28',
            'וְאֶל־הַתְּפִלָּה אֲשֶׁר עַבְדְּךָ מִתְפַּלֵּל לְפָנֶיךָ הַיּוֹם',
            '"…and to the prayer that your servant is praying before you today."'))
        self.add_verb_table([
            VerbEntry('1', 'מִתְפַּלֵּל', 'Participle', 'ms', 'פלל',
                      'Denominative — "praying"; מִתְ- prefix marks Hithpael participle; root פלל has no Qal in OT'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('8:30',
            'אֲשֶׁר יִתְפַּלְּלוּ אֶל הַמָּקוֹם הַזֶּה',
            '"…when they pray toward this place."'))
        self.add_verb_table([
            VerbEntry('2', 'יִתְפַּלְּלוּ', 'Imperfect', '3mp', 'פלל',
                      'Denominative — "they pray"; יִתְ- prefix + dagesh forte in doubled ל ל (geminate root)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('20:7',
            'כִּי נָבִיא הוּא וְיִתְפַּלֵּל בַּעַדְךָ',
            '"…for he is a prophet, and he will pray for you."'))
        self.add_verb_table([
            VerbEntry('3', 'יִתְפַּלֵּל', 'Imperfect', '3ms', 'פלל',
                      'Denominative — "he will pray"; יִתְ- prefix + patach under R1 + dagesh forte in ל ל'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('20:7',
            'הִתְפַּלֵּל אֶל יְהוָה',
            '"Pray to the LORD."'))
        self.add_verb_table([
            VerbEntry('4', 'הִתְפַּלֵּל', 'Imperative', '2ms', 'פלל',
                      'Denominative — "Pray!"; הִתְ- prefix + patach under R1 + tsere + ל ל; same form as perfect 3ms in isolation'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 29:36',
            'וְטִהֲרוֹ לְכַפֵּר עָלָיו',
            '"…and purify it to make atonement for it." [Piel distractor — no הִתְ prefix]'))
        self.add_verb_table([
            VerbEntry('5', 'וְטִהֲרוֹ', 'Weqatal', '3ms', 'טהר',
                      'NOT Hithpael — Piel: Factitive "shall purify it"; Hireq under R1 + guttural ה (rejects dagesh); no הִתְ prefix'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage B — Joshua 3:5 · Exodus 19:22')

        self.add_passage(PassageBlock('Jos 3:5',
            'הִתְקַדְּשׁוּ כִּי מָחָר יַעֲשֶׂה יְהוָה בְּקִרְבְּכֶם נִפְלָאוֹת',
            '"Consecrate yourselves, for tomorrow the LORD will do wonders among you."'))
        self.add_verb_table([
            VerbEntry('6', 'הִתְקַדְּשׁוּ', 'Imperative', '2mp', 'קדש',
                      'Reflexive — "consecrate yourselves!"; הִתְ- prefix + patach + dagesh forte in R2 (דּ) + 2mp suffix וּ'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 19:22',
            'וְגַם הַכֹּהֲנִים הַנִּגָּשִׁים אֶל יְהוָה יִתְקַדָּשׁוּ פֶּן יִפְרֹץ בָּהֶם',
            '"And also let the priests who come near to the LORD consecrate themselves, lest the LORD break out against them."'))
        self.add_verb_table([
            VerbEntry('7', 'יִתְקַדָּשׁוּ', 'Imperfect', '3mp', 'קדש',
                      'Reflexive — "let them consecrate themselves"; יִתְ- prefix + patach + lengthened R2 vowel (qamets) + 3mp suffix וּ'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Lev 8:15',
            'קֻדַּשׁ הַמִּזְבֵּחַ',
            '"The altar was consecrated." [Pual distractor — u-class vowel under R1]'))
        self.add_verb_table([
            VerbEntry('8', 'קֻדַּשׁ', 'Perfect', '3ms', 'קדש',
                      'NOT Hithpael — Pual Passive: "was consecrated"; Qibbuts (u-class) under R1 (קֻ) = Pual marker; no הִתְ prefix'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage C ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage C — Genesis 22:17–18 · 2 Samuel 10:12')

        self.add_passage(PassageBlock('Gen 22:18',
            'וְהִתְבָּרֲכוּ בְזַרְעֲךָ כֹּל גּוֹיֵי הָאָרֶץ',
            '"…and in your offspring all the nations of the earth shall bless themselves."'))
        self.add_verb_table([
            VerbEntry('9', 'וְהִתְבָּרֲכוּ', 'Weqatal', '3cp', 'ברך',
                      'Reflexive/Estimative — "shall bless themselves"; הִתְ- + R2=ר rejects dagesh (compensatory lengthening); 3cp suffix וּ'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('2 Sam 10:12',
            'חֲזַק וְנִתְחַזְּקָה בְּעַד עַמֵּנוּ',
            '"Be strong, and let us be courageous for our people."'))
        self.add_verb_table([
            VerbEntry('10', 'וְנִתְחַזְּקָה', 'Cohortative', '1cp', 'חזק',
                      'Reflexive — "let us strengthen ourselves"; נִתְ- (cohortative Hithpael 1cp) + dagesh forte in R2 (זּ) + ה cohortative'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Prov 17:15',
            'הִצְדִּיק אֶת הָרָשָׁע',
            '"He declared the wicked righteous." [Hiphil distractor — הִ- with no תְ]'))
        self.add_verb_table([
            VerbEntry('11', 'הִצְדִּיק', 'Perfect', '3ms', 'צדק',
                      'NOT Hithpael — Hiphil Declarative: "declared righteous"; הִ- prefix (no תְ) + Hireq-Yod under R2 = Hiphil pattern'),
        ], show_answers=show_answers)


def build_ch34_hithpael_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch34HithpaelExercise,
        'Chapter 34 — "Spot the Hithpael" Passage Exercise',
        '(Strong Verbs)  ·  1 Kgs 8  ·  Gen 20  ·  Jos 3  ·  Exo 19  ·  Gen 22  ·  2 Sam 10',
        ['hebrew', 'bbh', 'ch34', 'exercises', 'ch34-passage-exercise'],
        'ch34-passage-exercise.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 35 — "Spot the Hithpael" Passage Exercise (Weak Verbs)
# ---------------------------------------------------------------------------


class Ch35HithpaelWeakExercise(PassageExercise):
    _instructions = (
        'Each numbered verb belongs to one of the stems you have already studied '
        '(Qal, Niphal, Hiphil, Hophal, Piel, Pual, or Hithpael). '
        'Focus: weak roots in the Hithpael stem — watch for metathesis (I-צ/ז/שׁ) and III-ה forms. '
        'For each one, fill in: Hithpael? (Yes/No), Conjugation, PGN, Root, and Stem/Function. '
        'The answer key begins on the page marked "Answer Key".'
    )

    def _render_passages(self, show_answers: bool) -> None:

        # ── Passage A ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage A — Gen 22:5 · Gen 18:2 · Exo 20:5 · Psa 95:6')

        self.add_passage(PassageBlock('Gen 24:26',
            'וַיִּשְׁתַּחוּ לַיהוָה',
            '"And he bowed down before the LORD."'))
        self.add_verb_table([
            VerbEntry('1', 'וַיִּשְׁתַּחוּ', 'Wayyiqtol', '3ms', 'שחה',
                      'Reflexive — "and he bowed down"; I-שׁ metathesis: הִתְ+שׁ → הִשְׁתַּ; III-ה short form (וּ ending in Wayyiqtol 3ms)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 22:5',
            'וְנִשְׁתַּחֲוֶה וְנָשׁוּבָה אֲלֵיכֶם',
            '"…and we will worship and we will come back to you."'))
        self.add_verb_table([
            VerbEntry('2', 'וְנִשְׁתַּחֲוֶה', 'Cohortative', '1cp', 'שחה',
                      'Reflexive — "let us worship"; I-שׁ metathesis: הִתְ+שׁ → הִשְׁתַּ; cohortative prefix נ; III-ה ending ֶה'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 18:2',
            'וַיִּשְׁתַּחוּ אָרְצָה',
            '"And he bowed down to the ground."'))
        self.add_verb_table([
            VerbEntry('3', 'וַיִּשְׁתַּחוּ', 'Wayyiqtol', '3ms', 'שחה',
                      'Reflexive — "and he bowed down"; Wayyiqtol: וַיִּ + שְׁתַּחוּ; I-שׁ metathesis; III-ה short form (וּ ending in Wayyiqtol 3ms)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 20:5',
            'לֹא תִשְׁתַּחְוֶה לָהֶם',
            '"You shall not bow down to them."'))
        self.add_verb_table([
            VerbEntry('4', 'תִשְׁתַּחְוֶה', 'Imperfect', '2ms', 'שחה',
                      'Reflexive — "you shall not bow down"; תִ- (2ms prefix) + שְׁתַּחְוֶה; I-שׁ metathesis; III-ה imperfect ending ֶה'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Psa 95:6',
            'בֹּאוּ נִשְׁתַּחֲוֶה וְנִכְרָעָה נִבְרְכָה לִפְנֵי יְהוָה עֹשֵׂנוּ',
            '"Come, let us bow down and kneel; let us kneel before the LORD our maker." [Qal distractor — נִבְרְכָה]'))
        self.add_verb_table([
            VerbEntry('5', 'נִבְרְכָה', 'Cohortative', '1cp', 'ברך',
                      'NOT Hithpael — Qal: "let us kneel/bless"; נ = 1cp cohortative prefix (not הִתְ); no dagesh forte in R2'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage B — Genesis 35:7 · 1 Samuel 10:6, 11')

        self.add_passage(PassageBlock('Gen 35:7',
            'כִּי שָׁם נִגְלוּ אֵלָיו הָאֱלֹהִים',
            '"…because there God had revealed himself to him." [Niphal distractor]'))
        self.add_verb_table([
            VerbEntry('6', 'נִגְלוּ', 'Perfect', '3cp', 'גלה',
                      'NOT Hithpael — Niphal: "revealed themselves / were revealed"; נִ- prefix = Niphal; III-ה Niphal perfect 3cp (ה drops before וּ)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('1 Sam 10:6',
            'וְהִתְנַבִּיתָ עִמָּם וְנֶהְפַּכְתָּ לְאִישׁ אַחֵר',
            '"…and you will prophesy with them and be turned into another man."'))
        self.add_verb_table([
            VerbEntry('7', 'וְהִתְנַבִּיתָ', 'Weqatal', '2ms', 'נבא',
                      'Denominative/Iterative — "you will prophesy"; I-נ (no assimilation in Hithpael); הִתְ- + נַ + בִּי + 2ms suffix תָ; III-א'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('1 Sam 10:11',
            'וַיִּתְנַבְּאוּ עַד בּוֹא הַמִּנְחָה',
            '"And they prophesied until the offering of the evening sacrifice."'))
        self.add_verb_table([
            VerbEntry('8', 'וַיִּתְנַבְּאוּ', 'Wayyiqtol', '3mp', 'נבא',
                      'Denominative/Iterative — "and they prophesied"; יִתְ- prefix; I-נ (no assimilation); III-א with 3mp suffix אוּ'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage C ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage C — Genesis 44:16 · 2 Kings 8:29')

        self.add_passage(PassageBlock('Gen 44:16',
            'מַה נֹּאמַר לַאדֹנִי מַה נְּדַבֵּר וּמַה נִּצְטַדָּק',
            '"What shall we say? What shall we speak? How can we justify ourselves?"'))
        self.add_verb_table([
            VerbEntry('9', 'נִצְטַדָּק', 'Imperfect', '1cp', 'צדק',
                      'Reflexive/Estimative — "how can we justify ourselves?"; I-צ metathesis: הִתְצ → הִצְטַ (ת voices to ט); 1cp prefix נ'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('2 Kgs 8:29',
            'וַיָּשָׁב יוֹרָם הַמֶּלֶךְ לְהִתְרַפֵּא בְיִזְרְעֶאל',
            '"And King Joram returned to be healed in Jezreel."'))
        self.add_verb_table([
            VerbEntry('10', 'לְהִתְרַפֵּא', 'Inf. Construct', '—', 'רפא',
                      'Reflexive — "to be healed / to seek healing"; הִתְ- prefix; III-א root; לְ-preposition marks infinitive construct'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('2 Kgs 8:29',
            'כִּי הוּשַׁב הַמֶּלֶךְ',
            '"…that the king had returned." [Hophal distractor — הוּ- prefix]'))
        self.add_verb_table([
            VerbEntry('11', 'הוּשַׁב', 'Perfect', '3ms', 'שוב',
                      'NOT Hithpael — Hophal Passive: "was returned"; הוּ- prefix (u-class = Hophal); biconsonantal root שׁוּב; no הִתְ infix'),
        ], show_answers=show_answers)


def build_ch35_hithpael_weak_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch35HithpaelWeakExercise,
        'Chapter 35 — "Spot the Hithpael" Passage Exercise',
        '(Weak Verbs)  ·  Gen 22/18  ·  Exo 20  ·  Psa 95  ·  Gen 35/44  ·  1 Sam 10  ·  2 Kgs 8',
        ['hebrew', 'bbh', 'ch35', 'exercises', 'ch35-passage-exercise'],
        'ch35-passage-exercise.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 29 — "Spot the Hophal Weak" Passage Exercise
# ---------------------------------------------------------------------------


class Ch29HophalWeakExercise(PassageExercise):
    _instructions = (
        'Each numbered verb belongs to one of the stems you have already studied '
        '(Qal, Niphal, Hiphil, or Hophal). '
        'Focus: weak roots in the Hophal stem. '
        'For each one, fill in: Hophal? (Yes/No), Conjugation, PGN, Root, and Stem/Function. '
        'Key diagnostic: Hophal prefix vowel is always u-class (hu- Perfect, yu-/qu- Imperfect, mu- Participle). '
        'Four verbs in this exercise are not Hophal — drawn from Qal and Hiphil already studied. '
        'The answer key begins on the page marked "Answer Key".'
    )

    def _render_passages(self, show_answers: bool) -> None:

        # ── Passage A ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage A — Genesis 39:1 + 43:18 (Joseph narrative)')

        self.add_passage(PassageBlock('Gen 39:1a',
            'הוּרַד יוֹסֵף מִצְרָיְמָה וַיִּקְנֵהוּ פּוֹטִיפַר',
            '"Now Joseph had been brought down to Egypt, and Potiphar bought him."'))
        self.add_verb_table([
            VerbEntry('1', 'הוּרַד', 'Perfect', '3ms', 'יָרַד',
                      'Hophal — was brought down (I-yod; Hiphil horid = to bring down)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 39:1b',
            'הוּבָא יוֹסֵף מִצְרָיְמָה',
            '"Joseph was brought to Egypt."'))
        self.add_verb_table([
            VerbEntry('2', 'הוּבָא', 'Perfect', '3ms', 'בּוֹא',
                      'Hophal — was brought (I-yod; Hiphil hebi = to bring)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 43:18a',
            'עַל דְּבַר הַכֶּסֶף הַשָּׁב בְּאַמְתְּחֹתֵינוּ אֲנַחְנוּ מוּבָאִים',
            '"because of the silver that was returned in our sacks, we are being brought in."'))
        self.add_verb_table([
            VerbEntry('3', 'הַשָּׁב', 'Participle', 'ms', 'שׁוּב',
                      'Hophal Ptc. — (money) that was returned (biconsonantal; Hiphil heshiv)'),
            VerbEntry('4', 'מוּבָאִים', 'Participle', 'mp', 'בּוֹא',
                      'Hophal Ptc. mp — being brought in (mu- prefix; same root as #2)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 43:18b',
            'כִּי יוּבָא אִתָּנוּ אֶל בֵּיתוֹ',
            '"because we are being brought into his house."'))
        self.add_verb_table([
            VerbEntry('5', 'יוּבָא', 'Imperfect', '3ms', 'בּוֹא',
                      'Hophal — will be brought (yu- prefix = Hophal Impf.; I-yod)'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage B — Exodus 40:17 + Numbers 9:15-17 (Tabernacle)')

        self.add_passage(PassageBlock('Exo 40:17',
            'וַיְהִי בַּחֹדֶשׁ הָרִאשׁוֹן בַּשָּׁנָה הַשֵּׁנִית הוּקַם הַמִּשְׁכָּן',
            '"In the first month of the second year — the tabernacle was set up."'))
        self.add_verb_table([
            VerbEntry('6', 'הוּקַם', 'Perfect', '3ms', 'קוּם',
                      'Hophal — was set up (biconsonantal; Hiphil heqim = to set up/establish)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Num 9:15',
            'וּבְיוֹם הָקִים אֶת הַמִּשְׁכָּן כִּסָּה הֶעָנָן אֶת הַמִּשְׁכָּן',
            '"And on the day he set up the tabernacle, the cloud covered the tabernacle."'))
        self.add_verb_table([
            VerbEntry('7', 'הָקִים', 'Perfect', '3ms', 'קוּם',
                      'NOT Hophal — Hiphil active: "he set up" (ha- prefix, i-class; contrast huqam)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Num 9:17',
            'בְּהֵעָלֹת הֶעָנָן מֵעַל הַמִּשְׁכָּן יִסְעוּ בְּנֵי יִשְׂרָאֵל',
            '"Whenever the cloud lifted, the people of Israel set out."'))
        self.add_verb_table([
            VerbEntry('8', 'יִסְעוּ', 'Qal Impf.', '3mp', 'נָסַע',
                      'NOT Hophal — Qal Impf. 3mp (I-nun assimilation; yi- prefix, not yu-)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Num 9:15 context',
            'וְאִם לֹא יֻקַּם הַמִּשְׁכָּן',
            '"And if the tabernacle was not set up…"'))
        self.add_verb_table([
            VerbEntry('9', 'יֻקַּם', 'Imperfect', '3ms', 'קוּם',
                      'Hophal — will be set up (Qibbuts yu variant; biconsonantal; same root as #6)'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage C ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage C — Genesis 43:12 + 38:25 + Exodus 14:5')

        self.add_passage(PassageBlock('Gen 43:12',
            'וְאֶת הַכֶּסֶף הַמּוּשָׁב בְּפִי אַמְתְּחֹתֵיכֶם הוּשַׁב תָּשִׁיבוּ',
            '"and the money that was returned in the mouth of your sacks — bring it back."'))
        self.add_verb_table([
            VerbEntry('10', 'הוּשַׁב', 'Perfect', '3ms', 'שׁוּב',
                      'Hophal — was returned/brought back (biconsonantal; Hiphil heshiv)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 38:25',
            'הִוא מוּצֵאת וְהִיא שָׁלְחָה אֶל חָמִיהָ לֵאמֹר',
            '"She was being brought out, and she sent word to her father-in-law, saying…"'))
        self.add_verb_table([
            VerbEntry('11', 'מוּצֵאת', 'Participle', 'fs', 'יָצָא',
                      'Hophal Ptc. fs — being brought out (I-yod; mu- prefix; Hiphil hotzi)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 38:20',
            'וַיִּשְׁלַח יְהוּדָה אֶת גְּדִי הָעִזִּים וְלֹא מְצָאָהּ',
            '"And Judah sent the young goat, but he did not find her."'))
        self.add_verb_table([
            VerbEntry('12', 'מְצָאָהּ', 'Qal Pf.', '3ms + 3fs', 'מָצָא',
                      'NOT Hophal — Qal Pf. 3ms + 3fs obj. suffix (me = Qal, not Hophal mu-)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 5 context',
            'הוּצָא הַחוֹמֶר מֵהֶם',
            '"The straw was taken away from them."'))
        self.add_verb_table([
            VerbEntry('13', 'הוּצָא', 'Perfect', '3ms', 'יָצָא',
                      'Hophal — was brought out (I-yod; hu- prefix; Hiphil hotzi = to bring out)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 14:5',
            'הֻגַּד לְמֶלֶךְ מִצְרַיִם כִּי בָרַח הָעָם',
            '"It was told to the king of Egypt that the people had fled."'))
        self.add_verb_table([
            VerbEntry('14', 'הֻגַּד', 'Perfect', '3ms', 'נָגַד',
                      'Hophal — it was told (I-nun assimilation + Qibbuts; Hiphil higgid = to tell)'),
        ], show_answers=show_answers)


def build_ch29_hophal_weak_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch29HophalWeakExercise,
        'Chapter 29 — "Spot the Hophal Weak" Passage Exercise',
        'Genesis 39-43  /  Exodus 40 + Numbers 9  /  Genesis 38 + Exodus 14',
        ['hebrew', 'bbh', 'ch29', 'exercises', 'ch29-passage-exercise'],
        'ch29-passage-exercise.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 31 — "Spot the Piel Weak" Passage Exercise
# ---------------------------------------------------------------------------


class Ch31PielWeakExercise(PassageExercise):
    _instructions = (
        'Each numbered verb belongs to one of the stems you have already studied '
        '(Qal, Niphal, Hiphil, Hophal, or Piel). '
        'Focus: weak roots in the Piel stem, especially III-he roots. '
        'For each one, fill in: Piel? (Yes/No), Conjugation, PGN, Root, and Stem/Function. '
        'Three verbs in this exercise are not Piel — drawn from Hiphil and Hophal already studied. '
        'The answer key begins on the page marked "Answer Key".'
    )

    def _render_passages(self, show_answers: bool) -> None:

        # ── Passage A ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage A — Genesis 2:16; 3:11, 17 (Garden commands)')

        self.add_passage(PassageBlock('Gen 2:16',
            'וַיְצַו יְהוָה אֱלֹהִים עַל הָאָדָם לֵאמֹר',
            '"And the LORD God commanded the man, saying…"'))
        self.add_verb_table([
            VerbEntry('1', 'וַיְצַו', 'Wayyiqtol', '3ms', 'צָוָה',
                      'Denominative — "commanded"; III-he apocopated in Wayyiqtol: vayyetsav'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 3:11',
            'הֲמִן הָעֵץ אֲשֶׁר צִוִּיתִיךָ לְבִלְתִּי אֲכָל מִמֶּנּוּ',
            '"Have you eaten from the tree of which I commanded you not to eat?"'))
        self.add_verb_table([
            VerbEntry('2', 'צִוִּיתִיךָ', 'Perfect', '1cs + 2ms', 'צָוָה',
                      'Denominative — "I commanded you"; Hireq + dagesh in R2 + 1cs + 2ms obj.'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 3:17',
            'כִּי שָׁמַעְתָּ לְקוֹל אִשְׁתֶּךָ אֲשֶׁר צִוִּיתִיךָ לֵאמֹר',
            '"because you listened to your wife about the tree which I commanded you…"'))
        self.add_verb_table([
            VerbEntry('3', 'צִוִּיתִיךָ', 'Perfect', '1cs + 2ms', 'צָוָה',
                      'Denominative — same form as #2; God repeats in verdict speech'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage B — Genesis 6:18-20 + 18:19 + Exodus 1:17')

        self.add_passage(PassageBlock('Gen 6:18-19',
            'וַהֲקִמֹתִי אֶת בְּרִיתִי אִתָּךְ לְהַחֲיוֹת אִתָּךְ',
            '"and I will establish my covenant with you, to keep alive with you…"'))
        self.add_verb_table([
            VerbEntry('4', 'לְהַחֲיוֹת', 'Hiphil Inf.Const.', '—', 'חָיָה',
                      'NOT Piel — Hiphil Inf. Const. (leha- prefix); "to keep alive" (causative)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 6:19',
            'חִיָּה אֶת אֲשֶׁר בָּאָרֶץ',
            '"Keep alive what is on the earth."'))
        self.add_verb_table([
            VerbEntry('5', 'חִיָּה', 'Perfect', '3ms', 'חָיָה',
                      'Factitive — "kept alive"; III-he: Hireq + dagesh in R2 + qamets-he'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 18:19',
            'לְמַעַן אֲשֶׁר יְצַוֶּה אֶת בָּנָיו וְאֶת בֵּיתוֹ אַחֲרָיו',
            '"so that he will command his sons and his household after him…"'))
        self.add_verb_table([
            VerbEntry('6', 'יְצַוֶּה', 'Imperfect', '3ms', 'צָוָה',
                      'Denominative — III-he Impf. 3ms: ye- prefix + patach + dagesh in R2 + tsere-he'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 1:17',
            'וַיְחַיּוּ אֶת יַלְדֵי הַנָּשִׁים הָעִבְרִיּוֹת',
            '"and they kept alive the male children of the Hebrew women." (the midwives)'))
        self.add_verb_table([
            VerbEntry('7', 'וַיְחַיּוּ', 'Wayyiqtol', '3mp', 'חָיָה',
                      'Factitive — III-he Wayyiqtol 3mp: vayyeh + cha + yod (dagesh in yod) + u suffix'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage C ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage C — Genesis 16:6 + Deuteronomy 8:2-3 (Humbling)')

        self.add_passage(PassageBlock('Gen 16:6',
            'עִנָּה אֹתָהּ שָׂרַי',
            '"Sarai afflicted / humbled her."'))
        self.add_verb_table([
            VerbEntry('8', 'עִנָּה', 'Perfect', '3ms', 'עָנָה',
                      'Factitive — "she afflicted/humbled"; III-he: Hireq + dagesh in R2 + qamets-he'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Deu 8:2',
            'לְמַעַן עַנֹּתְךָ לְנַסֹּתְךָ',
            '"to humble you and to test you…"'))
        self.add_verb_table([
            VerbEntry('9', 'עַנֹּתְךָ', 'Inf. Construct', '— + 2ms', 'עָנָה',
                      'Factitive — III-he Inf. Const. + 2ms suffix: patach + dagesh in nun + tav'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Deu 8:3',
            'לְמַעַן הוֹדִיעֲךָ כִּי לֹא עַל הַלֶּחֶם לְבַדּוֹ יִחְיֶה הָאָדָם',
            '"in order to make you know that man does not live by bread alone."'))
        self.add_verb_table([
            VerbEntry('10', 'הוֹדִיעֲךָ', 'Hiphil Inf.Const.', '— + 2ms', 'יָדַע',
                      'NOT Piel — Hiphil Inf. Const. of I-yod root yada (ho- prefix); "to make known"'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Deu 8:2 parallel',
            'יְעַנֶּה יְהוָה אֱלֹהֶיךָ אֹתְךָ בַּמִּדְבָּר',
            '"The LORD your God will humble you in the wilderness."'))
        self.add_verb_table([
            VerbEntry('11', 'יְעַנֶּה', 'Imperfect', '3ms', 'עָנָה',
                      'Factitive — III-he Impf. 3ms: ye- + patach + dagesh in nun + tsere-he ending'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage D ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage D — Amos 3:7 + Genesis 50:16 + Deuteronomy 8:1')

        self.add_passage(PassageBlock('Amos 3:7',
            'כִּי לֹא יַעֲשֶׂה אֲדֹנָי יְהוִה דָּבָר כִּי אִם גִּלָּה סוֹדוֹ אֶל עֲבָדָיו הַנְּבִיאִים',
            '"For the Lord GOD does nothing without revealing his secret to his servants the prophets."'))
        self.add_verb_table([
            VerbEntry('12', 'גִּלָּה', 'Perfect', '3ms', 'גָּלָה',
                      'Declarative/Intensive — "revealed"; III-he: Hireq + dagesh in lamed + qamets-he'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 50:16',
            'וַיְצַוּוּ אֶל יוֹסֵף לֵאמֹר אָבִיךָ צִוָּה לִפְנֵי מוֹתוֹ',
            '"They sent a command to Joseph, saying, Your father gave orders before his death…"'))
        self.add_verb_table([
            VerbEntry('13', 'וַיְצַוּוּ', 'Wayyiqtol', '3mp', 'צָוָה',
                      'Denominative — Wayyiqtol 3mp of tsavah III-he; "they commanded"'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Deu 8:1',
            'כָּל הַמִּצְוָה אֲשֶׁר אָנֹכִי מְצַוְּךָ הַיּוֹם תִּשְׁמְרוּן לַעֲשׂוֹת',
            '"All the commandment that I am commanding you today, you shall be careful to do."'))
        self.add_verb_table([
            VerbEntry('14', 'מְצַוְּךָ', 'Participle', 'ms + 2ms', 'צָוָה',
                      'Denominative — Piel Ptc. ms + 2ms suffix: me- + patach + dagesh in R2'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 39:1 (review)',
            'הוּבָא יוֹסֵף מִצְרָיְמָה',
            '"Joseph was brought to Egypt." (Cross-stem review — compare Ch29)'))
        self.add_verb_table([
            VerbEntry('15', 'הוּבָא', 'Hophal Pf.', '3ms', 'בּוֹא',
                      'NOT Piel — Hophal Pf. 3ms (hu- prefix = u-class = Hophal passive); "was brought"'),
        ], show_answers=show_answers)


def build_ch31_piel_weak_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch31PielWeakExercise,
        'Chapter 31 — "Spot the Piel Weak" Passage Exercise',
        'Gen 2-3, 6, 16, 18  /  Exo 1  /  Deu 8  /  Amos 3  /  Gen 50',
        ['hebrew', 'bbh', 'ch31', 'exercises', 'ch31-passage-exercise'],
        'ch31-passage-exercise.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 32 — "Spot the Pual" Passage Exercise (Pual Strong)
# ---------------------------------------------------------------------------


class Ch32PualExercise(PassageExercise):
    _instructions = (
        'Each numbered verb belongs to one of the stems you have already studied '
        '(Qal, Niphal, Hiphil, Hophal, or Piel/Pual). '
        'For each one, fill in: Pual? (Yes/No), Conjugation, PGN, Root, and Stem/Function. '
        'The answer key begins on the page marked "Answer Key".'
    )

    def _render_passages(self, show_answers: bool) -> None:

        # ── Passage A ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage A — Numbers 22:6, 12; 23:8, 20 (Balaam cycle)')

        self.add_passage(PassageBlock('22:6',
            'כִּי יָדַעְתִּי אֵת אֲשֶׁר תְּבָרֵךְ מְבֹרָךְ וַאֲשֶׁר תָּאֹר יוּאָר',
            '"…for I know that he whom you bless is blessed, and he whom you curse is cursed."'))
        self.add_verb_table([
            VerbEntry('1', 'תְּבָרֵךְ', 'Imperfect',  '2ms', 'בָּרַךְ', 'NOT Pual — Piel Intensive: "you bless"; tsere under R2 = Piel active'),
            VerbEntry('2', 'מְבֹרָךְ',  'Participle', 'ms',  'בָּרַךְ', 'Passive — Pual Ptc. ms; Qamets under R1 (compensatory for ר rejecting dagesh)'),
            VerbEntry('3', 'יוּאָר',    'Imperfect',  '3ms', 'אָרַר',   'NOT Pual — Hophal: "shall be cursed"; יוּ prefix = u-class on preformative = Hophal Impf. marker'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('22:12',
            'לֹא תֵלֵךְ עִמָּהֶם לֹא תָאֹר אֶת הָעָם כִּי בָרוּךְ הוּא',
            '"You shall not go with them. You shall not curse the people, for they are blessed."'))
        self.add_verb_table([
            VerbEntry('4', 'תָאֹר',   'Imperfect', '2ms', 'אָרַר', 'NOT Pual — Qal: "you shall curse"; no u-class vowel under R1 with Dagesh in R2'),
            VerbEntry('5', 'בָּרוּךְ', 'Participle', 'ms', 'בָּרַךְ', 'Passive — Pual Ptc. ms (substantival: "blessed one"); Qamets = compensatory for ר'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('23:8',
            'מַה אֶקֹּב לֹא קַבֹּה אֵל וּמַה אֶזְעֹם לֹא זָעַם יְהוָה',
            '"How shall I curse what God has not cursed, and how shall I denounce what the LORD has not denounced?"'))
        self.add_verb_table([
            VerbEntry('6', 'קַבֹּה', 'Qal Inf.Abs.', '—',  'קָבַב', 'NOT Pual — Qal Inf. Abs.; geminate root; no Qibbuts + R2 dagesh'),
            VerbEntry('7', 'זָעַם',  'Perfect',      '3ms', 'זָעַם', 'NOT Pual — Qal Perf. 3ms; Qamets-Patach = Qal pattern; no u-class under R1'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('23:20',
            'הִנֵּה בָרֵךְ לָקָחְתִּי וּבֵרַךְ וְלֹא אֲשִׁיבֶנָּה',
            '"Behold, I have received a command to bless; he has blessed, and I cannot revoke it."'))
        self.add_verb_table([
            VerbEntry('8', 'בָרֵךְ', 'Inf. Absolute', '—', 'בָּרַךְ', 'NOT Pual — Piel Inf. Abs.: "to bless"; tsere under R2 = Piel active'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage B — Exodus 29:36–37 (Consecration of the Altar)')

        self.add_passage(PassageBlock('29:36',
            'וּמָשַׁחְתָּ אֹתוֹ לְקַדְּשׁוֹ',
            '"…and you shall anoint it to consecrate it."'))
        self.add_verb_table([
            VerbEntry('9', 'וּמָשַׁחְתָּ', 'Weqatal', '2ms', 'מָשַׁח', 'NOT Pual — Qal Weqatal: "and you shall anoint"; no u-class under R1'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('29:37',
            'שִׁבְעַת יָמִים תְּכַפֵּר עַל הַמִּזְבֵּחַ וְקִדַּשְׁתָּ אֹתוֹ וְהָיָה הַמִּזְבֵּחַ קֹדֶשׁ קָדָשִׁים כָּל הַנֹּגֵעַ בַּמִּזְבֵּחַ יִקְדָּשׁ',
            '"Seven days you shall make atonement for the altar and consecrate it, and the altar shall be most holy; whatever touches the altar shall be consecrated."'))
        self.add_verb_table([
            VerbEntry('10', 'וְקִדַּשְׁתָּ', 'Weqatal',     '2ms', 'קָדַשׁ', 'NOT Pual — Piel Factitive: "and you shall consecrate"; Hireq under R1 (קִ) = Piel'),
            VerbEntry('11', 'וְהָיָה',       'Weqatal',     '3ms', 'הָיָה',  'NOT Pual — Qal Weqatal: "and it shall be"; III-ה Qal'),
            VerbEntry('12', 'יִקְדָּשׁ',      'Niphal Impf.', '3ms', 'קָדַשׁ', 'NOT Pual — Niphal passive/reflexive: "shall be consecrated"; יִ + dagesh in R1 = Niphal; compare Pual: יְקֻדַּשׁ'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage C ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage C — Exodus 14:4; Isaiah 43:23; Exodus 40:17 (Pual of כבד + Hophal distractor)')

        self.add_passage(PassageBlock('Exo 14:4',
            'וְכָבַדְתִּי בְּפַרְעֹה וּבְכָל חֵילוֹ',
            '"And I will get glory through Pharaoh and all his host."'))
        self.add_verb_table([
            VerbEntry('13', 'וְכָבַדְתִּי', 'Weqatal', '1cs', 'כָּבֵד', 'NOT Pual — Niphal reflexive: "I will be glorified / get glory"; contracted Niphal prefix; no Qibbuts under R1'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Isa 43:23',
            'לֹא כֻבַּדְתַּנִי בְּקָרְבָּנֶיךָ',
            '"You have not honored me with your offerings."'))
        self.add_verb_table([
            VerbEntry('14', 'כֻּבַּדְתַּנִי', 'Perfect', '2ms', 'כָּבֵד', 'Passive — Pual: "you have not honored me"; Qibbuts under R1 (כֻ) + Dagesh in R2 (בּ) = Pual diagnostic'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 40:17',
            'הוּקַם הַמִּשְׁכָּן בְּיוֹם הַחֹדֶשׁ הָרִאשׁוֹן',
            '"The tabernacle was set up on the first day of the first month."'))
        self.add_verb_table([
            VerbEntry('15', 'הוּקַם', 'Perfect', '3ms', 'קוּם', 'NOT Pual — Hophal: "was set up/raised"; הוּ prefix = Hophal Perf. marker; hollow root has no R2 for dagesh; contrast Pual: קֻטַּל pattern'),
        ], show_answers=show_answers)

        if not show_answers:
            self.add_reflection([
                'In Passage A, verbs 1 (Piel) and 2 (Pual) come from the same root ברך. The root has R2=ר, '
                'which rejects Dagesh Forte. How does the Pual compensate for the missing dagesh, and why does '
                'this make the Pual and Piel of ברך harder to distinguish than strong-root counterparts?',
                'Verb 3 (יוּאָר, Hophal) and verb 14 (כֻּבַּדְתַּנִי, Pual) both express passive meaning. '
                'What is the key visual feature that distinguishes a Hophal from a Pual? '
                'What does each stem tell you about the corresponding active stem?',
                'Verbs 10 (Piel Weqatal) and 12 (Niphal Impf.) from Exo 29:37 use the same root קדש. '
                'The priest actively consecrates (Piel); then whatever touches becomes holy (Niphal). '
                'How does this passage illustrate the Piel-as-cause / Niphal-as-resulting-state distinction?',
            ])


def build_ch32_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch32PualExercise,
        'Chapter 32 — "Spot the Pual" Passage Exercise',
        'Num 22–23  ·  Exo 29  ·  Isa 43',
        ['hebrew', 'bbh', 'ch32', 'exercises', 'ch32-passage-exercise'],
        'ch32-passage-exercise.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 33 — "Spot the Pual" Passage Exercise (Pual Weak)
# ---------------------------------------------------------------------------


class Ch33PualWeakExercise(PassageExercise):
    _instructions = (
        'Each numbered verb belongs to one of the stems you have already studied '
        '(Qal, Niphal, Hiphil, Hophal, Piel, or Pual). '
        'For each one, fill in: Pual? (Yes/No), Conjugation, PGN, Root, and Stem/Function. '
        'For each Pual form, also identify the weak-root type (I-י, I-נ, III-ה, or R2=ר). '
        'The answer key begins on the page marked "Answer Key".'
    )

    def _render_passages(self, show_answers: bool) -> None:

        # ── Passage A ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage A — Genesis Genealogies (Gen 4:18; 4:26; 46:22; 6:1)')

        self.add_passage(PassageBlock('4:18',
            'וְעִירָד יָלַד אֶת מְחוּיָאֵל',
            '"And Irad fathered Mehujael."'))
        self.add_verb_table([
            VerbEntry('1', 'יָלַד', 'Perfect', '3ms', 'יָלַד', 'NOT Pual — Qal: "fathered/begat" (active); Qal Perf 3ms vowel pattern; no Qibbuts under R1'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('4:26',
            'אָז הוּחַל לִקְרֹא בְּשֵׁם יְהוָה',
            '"At that time people began to call upon the name of the LORD."'))
        self.add_verb_table([
            VerbEntry('2', 'הוּחַל', 'Perfect', '3ms', 'חָלַל', 'NOT Pual — Hophal: "was begun"; הוּ prefix = Hophal Perf. marker; geminate root; no Qibbuts under R1'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('46:22',
            'אֵלֶּה בְּנֵי רָחֵל אֲשֶׁר יֻלַּד לְיַעֲקֹב',
            '"These are the sons of Rachel who were born to Jacob."'))
        self.add_verb_table([
            VerbEntry('3', 'יֻלַּד', 'Perfect', '3ms', 'יָלַד', 'Passive — Pual; I-י root: "was born/begotten"; Qibbuts under R1 (יֻ) + Dagesh in R2 (לּ); Piel = "to beget" → Pual = "to be born"'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('6:1',
            'וַיִּוָּלְדוּ לָהֶם בָנִים',
            '"And sons were born to them."'))
        self.add_verb_table([
            VerbEntry('4', 'וַיִּוָּלְדוּ', 'Wayyiqtol', '3mp', 'יָלַד', 'NOT Pual — Niphal Wayyiqtol 3mp: "were born"; יִוָּ = Niphal with I-י (yod assimilates with dagesh); compare Pual יֻלַּד: Qibbuts vs. Niphal יִ'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage B — Leviticus 7:36; Numbers 3:9 (I-נ root נתן)')

        self.add_note('I-נ Pual: unlike Qal Imperfect where נ assimilates (יִתֵּן), '
                      'in the Pual the נ stays as R1 and takes Qibbuts. '
                      'Dagesh Forte falls on R2 (ת), not on an assimilated consonant.')

        self.add_passage(PassageBlock('Lev 7:36',
            'אֲשֶׁר צִוָּה יְהוָה לָתֵת לָהֶם',
            '"…which the LORD commanded to give to them."'))
        self.add_verb_table([
            VerbEntry('5', 'צִוָּה', 'Perfect', '3ms', 'צָוָה', 'NOT Pual — Piel active: "commanded"; Hireq under R1 (צִ) = Piel i-class; Pual passive would be צֻוָּה'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Num 3:9',
            'וְנָתַתָּ אֶת הַלְוִיִּם לְאַהֲרֹן וּלְבָנָיו נְתֻנִים נְתֻנִים הֵמָּה',
            '"And you shall give the Levites to Aaron and his sons; they are given, given."'))
        self.add_verb_table([
            VerbEntry('6', 'וְנָתַתָּ',  'Weqatal',   '2ms', 'נָתַן', 'NOT Pual — Qal Weqatal: "and you shall give"; no u-class under R1'),
            VerbEntry('7', 'נְתֻנִים',   'Participle', 'mp',  'נָתַן', 'Passive — Pual Ptc. mp; I-נ root: "given" (substantival); Qibbuts under תֻ; נ retained as R1 (does not assimilate in Pual)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Num 3:9b',
            'נֻתְּנוּ לִי הֵמָּה מִתּוֹךְ בְּנֵי יִשְׂרָאֵל',
            '"They were given to me from among the people of Israel."'))
        self.add_verb_table([
            VerbEntry('8', 'נֻתְּנוּ', 'Perfect', '3cp', 'נָתַן', 'Passive — Pual; I-נ root: "were given"; Qibbuts under R1 (נֻ) + Dagesh in R2 (תּ) + 3cp suffix וּ'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage C ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage C — Leviticus 8:35; Numbers 22:6; Psalm 72:17 (III-ה and R2=ר)')

        self.add_passage(PassageBlock('Lev 8:35',
            'כַּאֲשֶׁר צֻוֵּיתִי אֲנִי כֵּן צֻוֵּיתֶם',
            '"As I was commanded, so you were commanded."'))
        self.add_verb_table([
            VerbEntry('9',  'צֻוֵּיתִי', 'Perfect', '1cs', 'צָוָה', 'Passive — Pual; III-ה root: "I was commanded"; Qibbuts under R1 (צֻ) + Dagesh in R2 (וּ) + III-ה Perfect 1cs suffix יתִי'),
            VerbEntry('10', 'צֻוֵּיתֶם', 'Perfect', '2mp', 'צָוָה', 'Passive — Pual; III-ה root: "you were commanded"; same Pual diagnostic; 2mp suffix יתֶם'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Num 22:6',
            'כִּי יָדַעְתִּי אֵת אֲשֶׁר תְּבָרֵךְ מְבֹרָךְ וַאֲשֶׁר תָּאֹר יוּאָר',
            '"…for I know that he whom you bless is blessed, and he whom you curse is cursed."'))
        self.add_verb_table([
            VerbEntry('11', 'תְּבָרֵךְ', 'Imperfect',  '2ms', 'בָּרַךְ', 'NOT Pual — Piel Intensive: "you bless" (active); tsere under R2; R2=ר rejects dagesh but this is Piel'),
            VerbEntry('12', 'מְבֹרָךְ',  'Participle', 'ms',  'בָּרַךְ', 'Passive — Pual Ptc. ms; R2=ר (weak): Qamets under R1 (compensatory for ר rejecting dagesh)'),
            VerbEntry('13', 'יוּאָר',    'Imperfect',  '3ms', 'אָרַר',   'NOT Pual — Hophal: "shall be cursed"; יוּ prefix = u-class on preformative = Hophal Impf. marker'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Psa 72:17',
            'יְבֹרַךְ שְׁמוֹ לְעוֹלָם יִתְנַהֵל לִפְנֵי שֶׁמֶשׁ שְׁמוֹ',
            '"May his name be blessed forever; may his name endure before the sun."'))
        self.add_verb_table([
            VerbEntry('14', 'יְבֹרַךְ',   'Imperfect', '3ms', 'בָּרַךְ', 'Passive — Pual Impf.: "may his name be blessed"; R2=ר; Qamets under R1 (compensatory); jussive expressing prayer'),
            VerbEntry('15', 'יִתְנַהֵל', 'Imperfect', '3ms', 'נָהַל',  'NOT Pual — Hithpael: "may endure/continue"; יִתְ prefix = Hithpael marker; no Qibbuts under R1'),
        ], show_answers=show_answers)

        if not show_answers:
            self.add_reflection([
                'Verb 3 (יֻלַּד, I-י Pual Perfect) and verb 4 (וַיִּוָּלְדוּ, Niphal Wayyiqtol) '
                'both come from ילד and both express passive meaning. What visual feature most '
                'immediately distinguishes the Pual from the Niphal in these I-י forms?',
                'Verbs 7–8 (נְתֻנִים / נֻתְּנוּ, I-נ Pual) show that in the Pual, נ stays as R1 '
                'and takes Qibbuts rather than assimilating as in the Qal Imperfect (יִתֵּן). '
                'What grammatical principle causes the different behavior between stems?',
                'Verbs 9–10 (צֻוֵּיתִי / צֻוֵּיתֶם, III-ה Pual) parallel verb 5 (צִוָּה, Piel active). '
                'What single vowel under R1 most quickly identifies Piel vs. Pual? '
                'How does this i/u distinction work in the strong paradigm (קִטֵּל vs. קֻטַּל)?',
            ])


def build_ch33_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch33PualWeakExercise,
        'Chapter 33 — "Spot the Pual" Passage Exercise (Weak Roots)',
        'Gen 4  ·  Lev 7–8  ·  Num 3, 22  ·  Psa 72',
        ['hebrew', 'bbh', 'ch33', 'exercises', 'ch33-passage-exercise'],
        'ch33-passage-exercise.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Ch1–Ch6 builders
# ---------------------------------------------------------------------------


class Ch1LetterRecognitionExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each Hebrew letter shown, provide: (1) Letter Name, '
            '(2) Transliteration, (3) Sound, (4) Any special category '
            '(guttural / begadkephat / sofit form / normal).\n'
            'Items 1–22 cover all standard letters in canonical order. '
            'Items 23–27 cover the five sofit (final) forms. '
            'Items 28–30 show three begadkephat letters with dagesh lene.'
        )
        self.add_section_heading('Part A — Standard Letters (1–22)')
        rows_a = [
            ['1', 'א', '', '', '', ''],
            ['2', 'ב', '', '', '', ''],
            ['3', 'ג', '', '', '', ''],
            ['4', 'ד', '', '', '', ''],
            ['5', 'ה', '', '', '', ''],
            ['6', 'ו', '', '', '', ''],
            ['7', 'ז', '', '', '', ''],
            ['8', 'ח', '', '', '', ''],
            ['9', 'ט', '', '', '', ''],
            ['10', 'י', '', '', '', ''],
            ['11', 'כ', '', '', '', ''],
            ['12', 'ל', '', '', '', ''],
            ['13', 'מ', '', '', '', ''],
            ['14', 'נ', '', '', '', ''],
            ['15', 'ס', '', '', '', ''],
            ['16', 'ע', '', '', '', ''],
            ['17', 'פ', '', '', '', ''],
            ['18', 'צ', '', '', '', ''],
            ['19', 'ק', '', '', '', ''],
            ['20', 'ר', '', '', '', ''],
            ['21', 'שׁ', '', '', '', ''],
            ['22', 'ת', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'א', 'Aleph', 'ʾ', 'Silent/glottal stop', 'Guttural; quiescent'],
            ['2', 'ב', 'Beth', 'b / v', 'b (hard) or v (soft)', 'Begadkephat'],
            ['3', 'ג', 'Gimel', 'g / gh', 'g (hard) or gh (soft)', 'Begadkephat'],
            ['4', 'ד', 'Dalet', 'd / dh', 'd (hard) or dh (soft)', 'Begadkephat'],
            ['5', 'ה', 'He', 'h', 'h', 'Guttural; quiescent word-finally'],
            ['6', 'ו', 'Waw', 'w', 'w (consonantal)', 'Also mater lectionis'],
            ['7', 'ז', 'Zayin', 'z', 'z', 'Normal'],
            ['8', 'ח', 'Cheth', 'ḥ', 'ch as in German Bach', 'Guttural'],
            ['9', 'ט', 'Teth', 'ṭ', 'emphatic t', 'Normal (emphatic)'],
            ['10', 'י', 'Yod', 'y', 'y (consonantal)', 'Also mater lectionis'],
            ['11', 'כ', 'Kaph', 'k / kh', 'k (hard) or kh (soft)', 'Begadkephat; has sofit form'],
            ['12', 'ל', 'Lamed', 'l', 'l', 'Normal'],
            ['13', 'מ', 'Mem', 'm', 'm', 'Normal; has sofit form'],
            ['14', 'נ', 'Nun', 'n', 'n', 'Normal; has sofit form'],
            ['15', 'ס', 'Samech', 's', 's', 'Normal'],
            ['16', 'ע', 'Ayin', 'ʿ', 'Silent/pharyngeal', 'Guttural'],
            ['17', 'פ', 'Pe', 'p / f', 'p (hard) or f (soft)', 'Begadkephat; has sofit form'],
            ['18', 'צ', 'Tsade', 'ṣ', 'emphatic ts', 'Normal (emphatic); has sofit form'],
            ['19', 'ק', 'Qoph', 'q', 'q (uvular k)', 'Normal'],
            ['20', 'ר', 'Resh', 'r', 'r (uvular)', 'Behaves like guttural in some contexts'],
            ['21', 'שׁ', 'Shin', 'š', 'sh as in sheep', 'Normal (shin dot on right)'],
            ['22', 'ת', 'Taw', 't / th', 't (hard) or th (soft)', 'Begadkephat'],
        ]
        self.add_generic_table(
            headers=['#', 'Letter', 'Name', 'Transliteration', 'Sound', 'Special Category'],
            rows=rows_a,
            col_ratios=[0.05, 0.08, 0.12, 0.12, 0.14, 0.49],
            heb_cols=[1],
            show_answers=True,
            answer_rows=ans_a,
        )
        self.add_section_heading('Part B — Final (Sofit) Forms (23–27)')
        rows_b = [
            ['23', 'ך', '', '', '', ''],
            ['24', 'ם', '', '', '', ''],
            ['25', 'ן', '', '', '', ''],
            ['26', 'ף', '', '', '', ''],
            ['27', 'ץ', '', '', '', ''],
        ]
        ans_b = [
            ['23', 'ך', 'Kaph sofit', 'k / kh', 'k (hard) or kh (soft)', 'Sofit form of כ; occurs word-finally only'],
            ['24', 'ם', 'Mem sofit', 'm', 'm', 'Sofit form of מ; occurs word-finally only'],
            ['25', 'ן', 'Nun sofit', 'n', 'n', 'Sofit form of נ; occurs word-finally only'],
            ['26', 'ף', 'Pe sofit', 'p / f', 'p (hard) or f (soft)', 'Sofit form of פ; occurs word-finally only'],
            ['27', 'ץ', 'Tsade sofit', 'ṣ', 'emphatic ts', 'Sofit form of צ; occurs word-finally only'],
        ]
        self.add_generic_table(
            headers=['#', 'Letter', 'Name', 'Transliteration', 'Sound', 'Special Category'],
            rows=rows_b,
            col_ratios=[0.05, 0.08, 0.12, 0.12, 0.14, 0.49],
            heb_cols=[1],
            show_answers=True,
            answer_rows=ans_b,
        )
        self.add_section_heading('Part C — Begadkephat with Dagesh Lene (28–30)')
        rows_c = [
            ['28', 'בּ', '', '', '', ''],
            ['29', 'כּ', '', '', '', ''],
            ['30', 'פּ', '', '', '', ''],
        ]
        ans_c = [
            ['28', 'בּ', 'Beth (dagesh lene)', 'b', 'b as in boy — hard stop', 'Begadkephat — hard pronunciation'],
            ['29', 'כּ', 'Kaph (dagesh lene)', 'k', 'k as in king — hard stop', 'Begadkephat — hard pronunciation'],
            ['30', 'פּ', 'Pe (dagesh lene)', 'p', 'p as in pan — hard stop', 'Begadkephat — hard pronunciation'],
        ]
        self.add_generic_table(
            headers=['#', 'Letter', 'Name', 'Transliteration', 'Sound', 'Special Category'],
            rows=rows_c,
            col_ratios=[0.05, 0.08, 0.12, 0.12, 0.14, 0.49],
            heb_cols=[1],
            show_answers=True,
            answer_rows=ans_c,
        )


def build_ch1_letter_recognition(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch1LetterRecognitionExercise,
        'Chapter 1 — Hebrew Letter Recognition Exercise',
        'Hebrew Alphabet — Letter Identification',
        ['hebrew', 'bbh', 'ch1', 'exercises', 'ch1-letter-recognition'],
        'ch1-letter-recognition.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------


class Ch2VowelIdentificationExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each Hebrew form shown, identify: (1) Vowel Name, '
            '(2) Vowel Class (A / E / I / O / U / Reduced), '
            '(3) Quantity (Long / Short / Reduced), '
            '(4) Notes (e.g., mater lectionis present, composite sheva, dagesh forte). '
            'The letter מ (mem) serves as the carrier consonant for most items.'
        )
        rows = [
            ['1',  'מָ', '', '', '', ''],
            ['2',  'מֵ', '', '', '', ''],
            ['3',  'מִ', '', '', '', ''],
            ['4',  'מֹ', '', '', '', ''],
            ['5',  'מֻ', '', '', '', ''],
            ['6',  'מְ (word-initial)', '', '', '', ''],
            ['7',  'מַ', '', '', '', ''],
            ['8',  'מֶ', '', '', '', ''],
            ['9',  'מִי', '', '', '', ''],
            ['10', 'מוֹ', '', '', '', ''],
            ['11', 'מוּ', '', '', '', ''],
            ['12', 'מְ (word-final)', '', '', '', ''],
            ['13', 'מָ (closed, unaccented)', '', '', '', ''],
            ['14', 'מֵי', '', '', '', ''],
            ['15', 'כִּי', '', '', '', ''],
            ['16', 'מָ (= Qamets Hatuf)', '', '', '', ''],
            ['17', 'מֲ', '', '', '', ''],
            ['18', 'מֱ', '', '', '', ''],
            ['19', 'מֳ', '', '', '', ''],
            ['20', 'הֲ', '', '', '', ''],
            ['21', 'הֱ', '', '', '', ''],
            ['22', 'הֳ', '', '', '', ''],
            ['23', 'דָּבָר', '', '', '', ''],
            ['24', 'בֵּן', '', '', '', ''],
            ['25', 'מַּ (dagesh forte + patah)', '', '', '', ''],
        ]
        ans = [
            ['1',  'מָ', 'Qamets', 'A', 'Long', 'Standard long A; T-bar shape below consonant'],
            ['2',  'מֵ', 'Tsere', 'E', 'Long', 'Standard long E; two dots horizontally below consonant'],
            ['3',  'מִ', 'Hireq', 'I', 'Short', 'Standard short I; single dot below consonant'],
            ['4',  'מֹ', 'Holem', 'O', 'Long', 'Long O; single dot above the letter to the upper left'],
            ['5',  'מֻ', 'Qibbuts', 'U', 'Short', 'Short U; three diagonal dots below consonant'],
            ['6',  'מְ (word-initial)', 'Vocal Sheva', 'Reduced', 'Reduced', 'Vocal — word must begin with a vowel sound; /ə/'],
            ['7',  'מַ', 'Patah', 'A', 'Short', 'Standard short A; horizontal bar below consonant'],
            ['8',  'מֶ', 'Seghol', 'E', 'Short', 'Standard short E; three dots (inverted triangle)'],
            ['9',  'מִי', 'Hireq Yod', 'I', 'Long', 'Hireq with yod mater lectionis; yod is quiescent'],
            ['10', 'מוֹ', 'Holem Vav', 'O', 'Long', 'Holem with vav mater lectionis; vav is quiescent'],
            ['11', 'מוּ', 'Shureq', 'U', 'Long', 'Long U; vav with a dot in its center; vav is mater'],
            ['12', 'מְ (word-final)', 'Silent Sheva', '—', '—', 'Silent — marks the close of the final syllable'],
            ['13', 'מָ (closed, unaccented)', 'Qamets Hatuf', 'O', 'Short', 'Same shape as Qamets; O-class in closed unaccented syllable'],
            ['14', 'מֵי', 'Tsere Yod', 'E', 'Long', 'Tsere with yod mater lectionis; yod is quiescent'],
            ['15', 'כִּי', 'Hireq Yod', 'I', 'Long', 'Long I with yod mater; dagesh lene in kaph; word = because/that'],
            ['16', 'מָ (= Qamets Hatuf)', 'Qamets Hatuf', 'O', 'Short', 'O-class, short; same glyph as Qamets; closed unaccented syllable'],
            ['17', 'מֲ', 'Hatef Patah', 'A', 'Reduced', 'Composite sheva; A-class; used under gutturals'],
            ['18', 'מֱ', 'Hatef Seghol', 'E', 'Reduced', 'Composite sheva; E-class; used under gutturals'],
            ['19', 'מֳ', 'Hatef Qamets', 'O', 'Reduced', 'Composite sheva; O-class; least common hatef sheva'],
            ['20', 'הֲ', 'Hatef Patah', 'A', 'Reduced', 'Composite sheva; most common hatef; under gutturals'],
            ['21', 'הֱ', 'Hatef Seghol', 'E', 'Reduced', 'Composite sheva; E-class; less common than Hatef Patah'],
            ['22', 'הֳ', 'Hatef Qamets', 'O', 'Reduced', 'Composite sheva; O-class; least common of the three'],
            ['23', 'דָּבָר', 'Qamets \xd7 2', 'A', 'Long', 'Both vowels Qamets (long A); Dagesh Forte in dalet'],
            ['24', 'בֵּן', 'Tsere', 'E', 'Long', 'Long E under bet; dagesh lene in bet; word = son'],
            ['25', 'מַּ (dagesh forte + patah)', 'Patah', 'A', 'Short', 'Patah under mem; dot inside mem is Dagesh Forte'],
        ]
        self.add_generic_table(
            headers=['#', 'Form', 'Vowel Name', 'Class', 'Quantity', 'Notes'],
            rows=rows,
            col_ratios=[0.05, 0.10, 0.14, 0.08, 0.10, 0.53],
            heb_cols=[1],
            show_answers=True,
            answer_rows=ans,
        )


def build_ch2_vowel_identification(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch2VowelIdentificationExercise,
        'Chapter 2 — Vowel Identification Exercise',
        'Hebrew Vowels — Identification and Classification',
        ['hebrew', 'bbh', 'ch2', 'exercises', 'ch2-vowel-identification'],
        'ch2-vowel-identification.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------


class Ch3SyllableDivisionExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each word: (1) divide into syllables using hyphens, '
            '(2) label each syllable O (open) or C (closed), '
            '(3) mark the stressed syllable with an asterisk (*), '
            '(4) note any Qamets Hatuf (write QH in that column, or — if none).'
        )
        rows = [
            ['1', 'אֱלֹהִים', '', '', '', ''],
            ['2', 'בְּרֵאשִׁית', '', '', '', ''],
            ['3', 'הָאָרֶץ', '', '', '', ''],
            ['4', 'שָׁמַיִם', '', '', '', ''],
            ['5', 'יְרוּשָׁלַיִם', '', '', '', ''],
            ['6', 'דָּבָר', '', '', '', ''],
            ['7', 'מֶלֶךְ', '', '', '', ''],
            ['8', 'בְּרִית', '', '', '', ''],
            ['9', 'שָׁבַת', '', '', '', ''],
            ['10', 'נָבִיא', '', '', '', ''],
            ['11', 'אֲדֹנָי', '', '', '', ''],
            ['12', 'יִשְׂרָאֵל', '', '', '', ''],
            ['13', 'כֹּהֵן', '', '', '', ''],
            ['14', 'מִשְׁפָּט', '', '', '', ''],
            ['15', 'תּוֹרָה', '', '', '', ''],
            ['16', 'שָׁלוֹם', '', '', '', ''],
            ['17', 'חֶסֶד', '', '', '', ''],
            ['18', 'קֹדֶשׁ', '', '', '', ''],
            ['19', 'אֶרֶץ', '', '', '', ''],
            ['20', 'עַם', '', '', '', ''],
        ]
        ans = [
            ['1', 'אֱלֹהִים', 'אֱ-לֹ-הִים', 'O-O-C', 'הִים*', '—'],
            ['2', 'בְּרֵאשִׁית', 'בְּ-רֵא-שִׁית', 'O-O-C', 'שִׁית*', '—'],
            ['3', 'הָאָרֶץ', 'הָ-אָ-רֶץ', 'O-O-C', 'רֶץ*', '—'],
            ['4', 'שָׁמַיִם', 'שָׁ-מַ-יִם', 'O-O-C', 'יִם*', '—'],
            ['5', 'יְרוּשָׁלַיִם', 'יְ-רוּ-שָׁ-לַ-יִם', 'O-O-O-O-C', 'יִם*', '—'],
            ['6', 'דָּבָר', 'דָּ-בָר', 'O-O', 'בָר*', '—'],
            ['7', 'מֶלֶךְ', 'מֶ-לֶךְ', 'O-C', 'לֶךְ*', '—'],
            ['8', 'בְּרִית', 'בְּ-רִית', 'O-C', 'רִית*', '—'],
            ['9', 'שָׁבַת', 'שָׁ-בַת', 'O-C', 'בַת*', '—'],
            ['10', 'נָבִיא', 'נָ-בִיא', 'O-O', 'בִיא*', '—'],
            ['11', 'אֲדֹנָי', 'אֲ-דֹ-נָי', 'O-O-O', 'נָי*', '—'],
            ['12', 'יִשְׂרָאֵל', 'יִשׂ-רָ-אֵל', 'C-O-C', 'אֵל*', '—'],
            ['13', 'כֹּהֵן', 'כֹּ-הֵן', 'O-C', 'הֵן*', '—'],
            ['14', 'מִשְׁפָּט', 'מִשׁ-פָּט', 'C-C', 'פָּט*', '—'],
            ['15', 'תּוֹרָה', 'תּוֹ-רָה', 'O-O', 'רָה*', '—'],
            ['16', 'שָׁלוֹם', 'שָׁ-לוֹם', 'O-C', 'לוֹם*', '—'],
            ['17', 'חֶסֶד', 'חֶ-סֶד', 'O-C', 'סֶד*', '—'],
            ['18', 'קֹדֶשׁ', 'קֹ-דֶשׁ', 'O-C', 'דֶשׁ*', '—'],
            ['19', 'אֶרֶץ', 'אֶ-רֶץ', 'O-C', 'רֶץ*', '—'],
            ['20', 'עַם', 'עַם', 'C', 'עַם*', '—'],
        ]
        self.add_generic_table(
            headers=['#', 'Word', 'Syllable Division', 'Types (O/C)', 'Stress', 'Qamets Hatuf?'],
            rows=rows,
            col_ratios=[0.05, 0.12, 0.20, 0.14, 0.10, 0.39],
            heb_cols=[1],
            show_answers=True,
            answer_rows=ans,
        )


def build_ch3_syllable_division(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch3SyllableDivisionExercise,
        'Chapter 3 — Syllable Division Exercise',
        'Hebrew Syllables — Open, Closed, Stress, Qamets Hatuf',
        ['hebrew', 'bbh', 'ch3', 'exercises', 'ch3-syllable-division'],
        'ch3-syllable-division.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------


class Ch4NounParsingExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each form, give: (1) Gender (m./f.), (2) Number (s./pl./du.), '
            '(3) State (abs./cstr.), (4) Lexical Form (dictionary form), (5) Gloss.'
        )
        rows = [
            ['1', 'מֶלֶךְ', '', '', '', '', ''],
            ['2', 'מְלָכִים', '', '', '', '', ''],
            ['3', 'מַלְכֵי', '', '', '', '', ''],
            ['4', 'תּוֹרָה', '', '', '', '', ''],
            ['5', 'תּוֹרוֹת', '', '', '', '', ''],
            ['6', 'דְּבָרִים', '', '', '', '', ''],
            ['7', 'דִּבְרֵי', '', '', '', '', ''],
            ['8', 'בָּנִים', '', '', '', '', ''],
            ['9', 'בָּנוֹת', '', '', '', '', ''],
            ['10', 'אֲנָשִׁים', '', '', '', '', ''],
            ['11', 'נָשִׁים', '', '', '', '', ''],
            ['12', 'יָדַיִם', '', '', '', '', ''],
            ['13', 'עֵינַיִם', '', '', '', '', ''],
            ['14', 'עָרִים', '', '', '', '', ''],
            ['15', 'בָּתִּים', '', '', '', '', ''],
            ['16', 'יָמִים', '', '', '', '', ''],
            ['17', 'נֶפֶשׁ', '', '', '', '', ''],
            ['18', 'נְפָשׁוֹת', '', '', '', '', ''],
            ['19', 'סְפָרִים', '', '', '', '', ''],
            ['20', 'שָׁנָה', '', '', '', '', ''],
            ['21', 'שָׁנָתַיִם', '', '', '', '', ''],
            ['22', 'אֲרָצוֹת', '', '', '', '', ''],
            ['23', 'בְּנֵי', '', '', '', '', ''],
            ['24', 'מַלְכַּת', '', '', '', '', ''],
            ['25', 'שְׁנַת', '', '', '', '', ''],
        ]
        ans = [
            ['1', 'מֶלֶךְ', 'm.', 's.', 'abs.', 'מֶלֶךְ', 'king'],
            ['2', 'מְלָכִים', 'm.', 'pl.', 'abs.', 'מֶלֶךְ', 'kings'],
            ['3', 'מַלְכֵי', 'm.', 'pl.', 'cstr.', 'מֶלֶךְ', 'kings of'],
            ['4', 'תּוֹרָה', 'f.', 's.', 'abs.', 'תּוֹרָה', 'law, instruction'],
            ['5', 'תּוֹרוֹת', 'f.', 'pl.', 'abs./cstr.', 'תּוֹרָה', 'laws'],
            ['6', 'דְּבָרִים', 'm.', 'pl.', 'abs.', 'דָּבָר', 'words, things'],
            ['7', 'דִּבְרֵי', 'm.', 'pl.', 'cstr.', 'דָּבָר', 'words of'],
            ['8', 'בָּנִים', 'm.', 'pl.', 'abs.', 'בֵּן', 'sons'],
            ['9', 'בָּנוֹת', 'f.', 'pl.', 'abs.', 'בַּת', 'daughters'],
            ['10', 'אֲנָשִׁים', 'm.', 'pl.', 'abs.', 'אִישׁ', 'men'],
            ['11', 'נָשִׁים', 'f.', 'pl.', 'abs.', 'אִשָּׁה', 'women'],
            ['12', 'יָדַיִם', 'f.', 'du.', 'abs.', 'יָד', 'two hands'],
            ['13', 'עֵינַיִם', 'f.', 'du.', 'abs.', 'עַיִן', 'two eyes'],
            ['14', 'עָרִים', 'f.', 'pl.', 'abs.', 'עִיר', 'cities'],
            ['15', 'בָּתִּים', 'm.', 'pl.', 'abs.', 'בַּיִת', 'houses'],
            ['16', 'יָמִים', 'm.', 'pl.', 'abs.', 'יוֹם', 'days'],
            ['17', 'נֶפֶשׁ', 'f.', 's.', 'abs.', 'נֶפֶשׁ', 'soul, life'],
            ['18', 'נְפָשׁוֹת', 'f.', 'pl.', 'abs.', 'נֶפֶשׁ', 'souls'],
            ['19', 'סְפָרִים', 'm.', 'pl.', 'abs.', 'סֵפֶר', 'books'],
            ['20', 'שָׁנָה', 'f.', 's.', 'abs.', 'שָׁנָה', 'year'],
            ['21', 'שָׁנָתַיִם', 'f.', 'du.', 'abs.', 'שָׁנָה', 'two years'],
            ['22', 'אֲרָצוֹת', 'f.', 'pl.', 'abs.', 'אֶרֶץ', 'lands, earth'],
            ['23', 'בְּנֵי', 'm.', 'pl.', 'cstr.', 'בֵּן', 'sons of'],
            ['24', 'מַלְכַּת', 'f.', 's.', 'cstr.', 'מַלְכָּה', 'queen of'],
            ['25', 'שְׁנַת', 'f.', 's.', 'cstr.', 'שָׁנָה', 'year of'],
        ]
        self.add_generic_table(
            headers=['#', 'Form', 'Gender', 'Number', 'State', 'Lexical Form', 'Gloss'],
            rows=rows,
            col_ratios=[0.05, 0.13, 0.08, 0.08, 0.08, 0.14, 0.44],
            heb_cols=[1, 5],
            show_answers=True,
            answer_rows=ans,
        )


def build_ch4_noun_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch4NounParsingExercise,
        'Chapter 4 — Noun Parsing Drill',
        'Hebrew Nouns — Gender, Number, State, Lexical Form',
        ['hebrew', 'bbh', 'ch4', 'exercises', 'ch4-noun-parsing'],
        'ch4-noun-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------


class Ch5ArticleAndVavExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each Hebrew word or phrase: '
            '(1) Article? — Yes/No; '
            '(2) Article Form — if yes, what form? '
            '(3) Conj. ו? — Yes/No; '
            '(4) Conj. Form — if yes, what form? '
            '(5) Translation.'
        )
        hdrs = ['#', 'Hebrew', 'Article?', 'Article Form', 'Conj. ו?', 'Conj. Form', 'Translation']
        cr = [0.05, 0.12, 0.08, 0.16, 0.10, 0.12, 0.37]
        hc = [1]

        self.add_section_heading('Part A — Article Before Normal Consonants (1–8)')
        rows_a = [
            ['1', 'הַמֶּלֶךְ', '', '', '', '', ''],
            ['2', 'הַבַּיִת', '', '', '', '', ''],
            ['3', 'הַיּוֹם', '', '', '', '', ''],
            ['4', 'הַדָּבָר', '', '', '', '', ''],
            ['5', 'הַלַּיְלָה', '', '', '', '', ''],
            ['6', 'הַבֵּן', '', '', '', '', ''],
            ['7', 'הַסֵּפֶר', '', '', '', '', ''],
            ['8', 'הַנָּבִיא', '', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'הַמֶּלֶךְ', 'Yes', 'הַ + dagesh forte', 'No', '—', 'the king'],
            ['2', 'הַבַּיִת', 'Yes', 'הַ + dagesh forte', 'No', '—', 'the house'],
            ['3', 'הַיּוֹם', 'Yes', 'הַ + dagesh forte', 'No', '—', 'the day'],
            ['4', 'הַדָּבָר', 'Yes', 'הַ + dagesh forte', 'No', '—', 'the word / the thing'],
            ['5', 'הַלַּיְלָה', 'Yes', 'הַ + dagesh forte', 'No', '—', 'the night'],
            ['6', 'הַבֵּן', 'Yes', 'הַ + dagesh forte', 'No', '—', 'the son'],
            ['7', 'הַסֵּפֶר', 'Yes', 'הַ + dagesh forte', 'No', '—', 'the book / the scroll'],
            ['8', 'הַנָּבִיא', 'Yes', 'הַ + dagesh forte', 'No', '—', 'the prophet'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_a, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Part B — Article Before Gutturals (9–13)')
        rows_b = [
            ['9', 'הָאִישׁ', '', '', '', '', ''],
            ['10', 'הָאָרֶץ', '', '', '', '', ''],
            ['11', 'הֶעָם', '', '', '', '', ''],
            ['12', 'הָהָר', '', '', '', '', ''],
            ['13', 'הָרוּחַ', '', '', '', '', ''],
        ]
        ans_b = [
            ['9', 'הָאִישׁ', 'Yes', 'הָ (qamets; no dagesh)', 'No', '—', 'the man'],
            ['10', 'הָאָרֶץ', 'Yes', 'הָ (qamets; no dagesh)', 'No', '—', 'the land / the earth'],
            ['11', 'הֶעָם', 'Yes', 'הֶ (segol; no dagesh)', 'No', '—', 'the people'],
            ['12', 'הָהָר', 'Yes', 'הָ (qamets; no dagesh)', 'No', '—', 'the mountain'],
            ['13', 'הָרוּחַ', 'Yes', 'הָ (qamets; no dagesh)', 'No', '—', 'the spirit / the wind'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Part C — Conjunction Only (14–18)')
        rows_c = [
            ['14', 'וְדָבָר', '', '', '', '', ''],
            ['15', 'וּמֶלֶךְ', '', '', '', '', ''],
            ['16', 'וּבֵן', '', '', '', '', ''],
            ['17', 'וְאִישׁ', '', '', '', '', ''],
            ['18', 'וָאֹמַר', '', '', '', '', ''],
        ]
        ans_c = [
            ['14', 'וְדָבָר', 'No', '—', 'Yes', 'וְ (sheva)', 'and a word'],
            ['15', 'וּמֶלֶךְ', 'No', '—', 'Yes', 'וּ (shureq)', 'and a king'],
            ['16', 'וּבֵן', 'No', '—', 'Yes', 'וּ (shureq)', 'and a son'],
            ['17', 'וְאִישׁ', 'No', '—', 'Yes', 'וְ (sheva)', 'and a man'],
            ['18', 'וָאֹמַר', 'No', '—', 'Yes', 'וָ (qamets)', 'and I said / then I said'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_c, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_c)

        self.add_section_heading('Part D — Both Article and Conjunction (19–23)')
        rows_d = [
            ['19', 'וְהַמֶּלֶךְ', '', '', '', '', ''],
            ['20', 'וְהָאָרֶץ', '', '', '', '', ''],
            ['21', 'וְהָאִישׁ', '', '', '', '', ''],
            ['22', 'וְהַיּוֹם', '', '', '', '', ''],
            ['23', 'וְהֶעָם', '', '', '', '', ''],
        ]
        ans_d = [
            ['19', 'וְהַמֶּלֶךְ', 'Yes', 'הַ + dagesh forte', 'Yes', 'וְ (sheva)', 'and the king'],
            ['20', 'וְהָאָרֶץ', 'Yes', 'הָ (qamets; no dagesh)', 'Yes', 'וְ (sheva)', 'and the land / and the earth'],
            ['21', 'וְהָאִישׁ', 'Yes', 'הָ (qamets; no dagesh)', 'Yes', 'וְ (sheva)', 'and the man'],
            ['22', 'וְהַיּוֹם', 'Yes', 'הַ + dagesh forte', 'Yes', 'וְ (sheva)', 'and the day'],
            ['23', 'וְהֶעָם', 'Yes', 'הֶ (segol; no dagesh)', 'Yes', 'וְ (sheva)', 'and the people'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_d, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_d)

        self.add_section_heading('Part E — Neither (24–25)')
        rows_e = [
            ['24', 'מֶלֶךְ', '', '', '', '', ''],
            ['25', 'דָּבָר', '', '', '', '', ''],
        ]
        ans_e = [
            ['24', 'מֶלֶךְ', 'No', '—', 'No', '—', 'a king'],
            ['25', 'דָּבָר', 'No', '—', 'No', '—', 'a word / a thing'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_e, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_e)


def build_ch5_article_and_vav(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch5ArticleAndVavExercise,
        'Chapter 5 — Definite Article and Conjunction ו',
        'BBH Chapter 5 · 25 items',
        ['hebrew', 'bbh', 'ch5', 'exercises', 'ch5-article-and-vav'],
        'ch5-article-and-vav.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------


class Ch6PrepositionParsingExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each Hebrew prepositional phrase: '
            '(1) identify the preposition as it appears, '
            '(2) give the base (dictionary) form of the preposition, '
            '(3) describe any vowel change and explain why it occurred, '
            '(4) identify the object noun, '
            '(5) translate the phrase.'
        )
        hdrs = ['#', 'Hebrew', 'Preposition', 'Base Form', 'Change / Reason', 'Object', 'Translation']
        cr = [0.05, 0.12, 0.10, 0.08, 0.22, 0.10, 0.33]
        hc = [1]

        self.add_section_heading('Part A — Inseparable Prepositions: Standard/Sheva Rules (1–8)')
        rows_a = [
            ['1', 'בְּדָבָר', '', '', '', '', ''],
            ['2', 'לְמֶלֶךְ', '', '', '', '', ''],
            ['3', 'כְּאִישׁ', '', '', '', '', ''],
            ['4', 'בִּשְׁמוּאֵל', '', '', '', '', ''],
            ['5', 'לִשְׁלֹמֹה', '', '', '', '', ''],
            ['6', 'בֶּאֱמֶת', '', '', '', '', ''],
            ['7', 'לֵאלֹהִים', '', '', '', '', ''],
            ['8', 'כֶּחָכְמָה', '', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'בְּדָבָר', 'בְּ', 'בְּ', 'None — default sheva', 'דָּבָר', 'in a word'],
            ['2', 'לְמֶלֶךְ', 'לְ', 'לְ', 'None — default sheva', 'מֶלֶךְ', 'to a king / for a king'],
            ['3', 'כְּאִישׁ', 'כְּ', 'כְּ', 'None — default sheva', 'אִישׁ', 'like a man'],
            ['4', 'בִּשְׁמוּאֵל', 'בִּ', 'בְּ', 'Sheva → hireq: two consecutive shevas', 'שְׁמוּאֵל', 'in/with Samuel'],
            ['5', 'לִשְׁלֹמֹה', 'לִ', 'לְ', 'Sheva → hireq: two consecutive shevas', 'שְׁלֹמֹה', 'to Solomon'],
            ['6', 'בֶּאֱמֶת', 'בֶּ', 'בְּ', 'Composite sheva: אֱ (hateph seghol) → prep takes seghol', 'אֱמֶת', 'in truth'],
            ['7', 'לֵאלֹהִים', 'לֵ', 'לְ', 'Composite sheva matching + lengthening before א to tsere', 'אֱלֹהִים', 'to God'],
            ['8', 'כֶּחָכְמָה', 'כֶּ', 'כְּ', 'Composite sheva matching; prep takes seghol by assimilation', 'חָכְמָה', 'like wisdom'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_a, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Part B — Inseparable Prepositions Fused with Article (9–16)')
        rows_b = [
            ['9', 'בַּמֶּלֶךְ', '', '', '', '', ''],
            ['10', 'לַשָּׁמַיִם', '', '', '', '', ''],
            ['11', 'כַּיּוֹם', '', '', '', '', ''],
            ['12', 'בַּבַּיִת', '', '', '', '', ''],
            ['13', 'לָהָר', '', '', '', '', ''],
            ['14', 'בָּאָרֶץ', '', '', '', '', ''],
            ['15', 'לָעָם', '', '', '', '', ''],
            ['16', 'כָּהָאִישׁ', '', '', '', '', ''],
        ]
        ans_b = [
            ['9', 'בַּמֶּלֶךְ', 'בַּ', 'בְּ', 'Article fusion: הַ drops; patach transfers; dagesh forte in מ', 'מֶלֶךְ', 'in the king'],
            ['10', 'לַשָּׁמַיִם', 'לַ', 'לְ', 'Article fusion: הַ drops; patach transfers; dagesh forte in שׁ', 'שָּׁמַיִם', 'to the heavens'],
            ['11', 'כַּיּוֹם', 'כַּ', 'כְּ', 'Article fusion: הַ drops; patach transfers; dagesh forte in י', 'יּוֹם', 'like the day'],
            ['12', 'בַּבַּיִת', 'בַּ', 'בְּ', 'Article fusion: הַ drops; patach transfers; dagesh forte in ב', 'בַּיִת', 'in the house'],
            ['13', 'לָהָר', 'לָ', 'לְ', 'Article fusion (guttural): ה rejects dagesh; patach lengthens → qamets', 'הָר', 'to the mountain'],
            ['14', 'בָּאָרֶץ', 'בָּ', 'בְּ', 'Article fusion (guttural): א rejects dagesh; patach → qamets', 'אָרֶץ', 'in the earth / in the land'],
            ['15', 'לָעָם', 'לָ', 'לְ', 'Article fusion (guttural): ע rejects dagesh; patach → qamets', 'עָם', 'to the people'],
            ['16', 'כָּהָאִישׁ', 'כָּ', 'כְּ', 'Article fusion (guttural): א rejects dagesh; qamets under כָּ', 'אִישׁ', 'like the man'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Part C — מִן: Independent, Prefixed, and Compensatory (17–21)')
        rows_c = [
            ['17', 'מִן הַמֶּלֶךְ', '', '', '', '', ''],
            ['18', 'מִמֶּלֶךְ', '', '', '', '', ''],
            ['19', 'מִיַּד', '', '', '', '', ''],
            ['20', 'מֵהָאָרֶץ', '', '', '', '', ''],
            ['21', 'מֵאֱלֹהִים', '', '', '', '', ''],
        ]
        ans_c = [
            ['17', 'מִן הַמֶּלֶךְ', 'מִן', 'מִן', 'No change — independent before article', 'הַמֶּלֶךְ', 'from the king'],
            ['18', 'מִמֶּלֶךְ', 'מִ', 'מִן', 'Nun assimilates; dagesh forte in מ', 'מֶלֶךְ', 'from a king'],
            ['19', 'מִיַּד', 'מִ', 'מִן', 'Nun assimilates; dagesh forte in י', 'יָד', 'from the hand'],
            ['20', 'מֵהָאָרֶץ', 'מֵ', 'מִן', 'Compensatory: ה (guttural) rejects dagesh; hireq → tsere', 'הָאָרֶץ', 'from the earth'],
            ['21', 'מֵאֱלֹהִים', 'מֵ', 'מִן', 'Compensatory: א (guttural) rejects dagesh; hireq → tsere', 'אֱלֹהִים', 'from God'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_c, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_c)

        self.add_section_heading('Part D — Independent Prepositions (22–25)')
        rows_d = [
            ['22', 'אֶל הָעִיר', '', '', '', '', ''],
            ['23', 'עַל הַשָּׁמַיִם', '', '', '', '', ''],
            ['24', 'עִם הָעַם', '', '', '', '', ''],
            ['25', 'אֵת הַמֶּלֶךְ', '', '', '', '', ''],
        ]
        ans_d = [
            ['22', 'אֶל הָעִיר', 'אֶל', 'אֶל', 'None — independent preposition', 'הָעִיר', 'to the city'],
            ['23', 'עַל הַשָּׁמַיִם', 'עַל', 'עַל', 'None — independent preposition', 'הַשָּׁמַיִם', 'upon the heavens'],
            ['24', 'עִם הָעַם', 'עִם', 'עִם', 'None — independent preposition', 'הָעַם', 'with the people'],
            ['25', 'אֵת הַמֶּלֶךְ', 'אֵת (DOM)', 'אֵת', 'None — direct object marker', 'הַמֶּלֶךְ', '[marks the king as definite direct object]'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_d, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_d)


def build_ch6_preposition_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch6PrepositionParsingExercise,
        'Chapter 6 — Preposition Parsing Drill',
        'Hebrew Prepositions — Inseparable, Article Fusion, מִן, Independent',
        ['hebrew', 'bbh', 'ch6', 'exercises', 'ch6-preposition-parsing'],
        'ch6-preposition-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Ch7–Ch12 builders
# ---------------------------------------------------------------------------


class Ch7AdjectiveUsageExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each Hebrew phrase: '
            '(1) Use — Identify: Attributive (Def./Indef.) / Predicate / Substantival / Comparative / Superlative; '
            '(2) Adjective — give the adjective form shown; '
            '(3) Agreement — gender and number (ms/fs/mp/fp) and note whether it agrees; '
            '(4) Translation.'
        )
        hdrs = ['#', 'Hebrew', 'Use', 'Adjective', 'Agreement', 'Translation']
        cr = [0.05, 0.17, 0.15, 0.15, 0.22, 0.26]
        hc = [1, 3]

        self.add_section_heading('Part A — Attributive Adjectives (Definite) (1–5)')
        rows_a = [
            ['1', 'הַמֶּלֶךְ הַגָּדוֹל', '', '', '', ''],
            ['2', 'הָאִשָּׁה הַטּוֹבָה', '', '', '', ''],
            ['3', 'הָעִיר הַגְּדוֹלָה', '', '', '', ''],
            ['4', 'הָאֲנָשִׁים הַגִּבּוֹרִים', '', '', '', ''],
            ['5', 'הַדְּבָרִים הַטּוֹבִים', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'הַמֶּלֶךְ הַגָּדוֹל', 'Attributive (def.)', 'הַגָּדוֹל', 'ms; agrees with מֶלֶךְ (ms)', 'the great king'],
            ['2', 'הָאִשָּׁה הַטּוֹבָה', 'Attributive (def.)', 'הַטּוֹבָה', 'fs; agrees with אִשָּׁה (fs)', 'the good woman'],
            ['3', 'הָעִיר הַגְּדוֹלָה', 'Attributive (def.)', 'הַגְּדוֹלָה', 'fs; agrees with עִיר (fs)', 'the great city'],
            ['4', 'הָאֲנָשִׁים הַגִּבּוֹרִים', 'Attributive (def.)', 'הַגִּבּוֹרִים', 'mp; agrees with אֲנָשִׁים (mp)', 'the mighty men'],
            ['5', 'הַדְּבָרִים הַטּוֹבִים', 'Attributive (def.)', 'הַטּוֹבִים', 'mp; agrees with דְּבָרִים (mp)', 'the good words/things'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_a, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Part B — Attributive Adjectives (Indefinite) (6–10)')
        rows_b = [
            ['6', 'מֶלֶךְ גָּדוֹל', '', '', '', ''],
            ['7', 'אִשָּׁה טוֹבָה', '', '', '', ''],
            ['8', 'אֶרֶץ גְּדוֹלָה', '', '', '', ''],
            ['9', 'עַם קָדוֹשׁ', '', '', '', ''],
            ['10', 'דָּבָר חָדָשׁ', '', '', '', ''],
        ]
        ans_b = [
            ['6', 'מֶלֶךְ גָּדוֹל', 'Attributive (indef.)', 'גָּדוֹל', 'ms; agrees with מֶלֶךְ (ms)', 'a great king'],
            ['7', 'אִשָּׁה טוֹבָה', 'Attributive (indef.)', 'טוֹבָה', 'fs; agrees with אִשָּׁה (fs)', 'a good woman'],
            ['8', 'אֶרֶץ גְּדוֹלָה', 'Attributive (indef.)', 'גְּדוֹלָה', 'fs; agrees with אֶרֶץ (fs)', 'a great land'],
            ['9', 'עַם קָדוֹשׁ', 'Attributive (indef.)', 'קָדוֹשׁ', 'ms; agrees with עַם (ms)', 'a holy people'],
            ['10', 'דָּבָר חָדָשׁ', 'Attributive (indef.)', 'חָדָשׁ', 'ms; agrees with דָּבָר (ms)', 'a new word/thing'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Part C — Predicate Adjectives (11–18)')
        rows_c = [
            ['11', 'הַמֶּלֶךְ גָּדוֹל', '', '', '', ''],
            ['12', 'גָּדוֹל הַמֶּלֶךְ', '', '', '', ''],
            ['13', 'הָאִשָּׁה טוֹבָה', '', '', '', ''],
            ['14', 'טוֹב הַדָּבָר', '', '', '', ''],
            ['15', 'הָאָרֶץ טוֹבָה', '', '', '', ''],
            ['16', 'הַגִּבּוֹרִים חֲזָקִים', '', '', '', ''],
            ['17', 'יָשָׁר הַדֶּרֶךְ', '', '', '', ''],
            ['18', 'כָּבֵד הַדָּבָר', '', '', '', ''],
        ]
        ans_c = [
            ['11', 'הַמֶּלֶךְ גָּדוֹל', 'Predicate', 'גָּדוֹל', 'ms; agrees with מֶלֶךְ; no article', 'The king is great'],
            ['12', 'גָּדוֹל הַמֶּלֶךְ', 'Predicate', 'גָּדוֹל', 'ms; adj-first word order; no article', 'The king is great'],
            ['13', 'הָאִשָּׁה טוֹבָה', 'Predicate', 'טוֹבָה', 'fs; agrees with אִשָּׁה; no article', 'The woman is good'],
            ['14', 'טוֹב הַדָּבָר', 'Predicate', 'טוֹב', 'ms; adj-first; no article', 'The word/matter is good'],
            ['15', 'הָאָרֶץ טוֹבָה', 'Predicate', 'טוֹבָה', 'fs; agrees with אֶרֶץ; no article', 'The land is good'],
            ['16', 'הַגִּבּוֹרִים חֲזָקִים', 'Predicate', 'חֲזָקִים', 'mp; agrees with גִּבּוֹרִים; no article', 'The warriors are strong'],
            ['17', 'יָשָׁר הַדֶּרֶךְ', 'Predicate', 'יָשָׁר', 'ms; adj-first; no article', 'The way is straight/upright'],
            ['18', 'כָּבֵד הַדָּבָר', 'Predicate', 'כָּבֵד', 'ms; adj-first (stative pattern); no article', 'The matter is heavy/serious'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_c, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_c)

        self.add_section_heading('Part D — Substantival Adjectives (19–22)')
        rows_d = [
            ['19', 'הַטּוֹב', '', '', '', ''],
            ['20', 'הָרָע', '', '', '', ''],
            ['21', 'הַקְּדֹשִׁים', '', '', '', ''],
            ['22', 'רַבִּים', '', '', '', ''],
        ]
        ans_d = [
            ['19', 'הַטּוֹב', 'Substantival', 'הַטּוֹב', 'ms with article', 'the good (one/thing)'],
            ['20', 'הָרָע', 'Substantival', 'הָרָע', 'ms with article', 'the evil (one/thing)'],
            ['21', 'הַקְּדֹשִׁים', 'Substantival', 'הַקְּדֹשִׁים', 'mp with article', 'the holy ones; the saints'],
            ['22', 'רַבִּים', 'Substantival', 'רַבִּים', 'mp without article', 'many (people); a multitude'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_d, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_d)

        self.add_section_heading('Part E — Comparative and Superlative (23–25)')
        rows_e = [
            ['23', 'טוֹב מִדְּבַשׁ', '', '', '', ''],
            ['24', 'הַקָּטֹן', '', '', '', ''],
            ['25', 'עָרוּם מִכֹּל חַיַּת הַשָּׂדֶה', '', '', '', ''],
        ]
        ans_e = [
            ['23', 'טוֹב מִדְּבַשׁ', 'Comparative', 'טוֹב', 'ms; compared via מִן', 'better than honey'],
            ['24', 'הַקָּטֹן', 'Superlative', 'הַקָּטֹן', 'ms with article; no head noun', 'the youngest; the smallest'],
            ['25', 'עָרוּם מִכֹּל חַיַּת הַשָּׂדֶה', 'Comparative (superlative in context)', 'עָרוּם', 'ms; compared via מִכֹּל', 'more crafty than any beast of the field'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_e, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_e)


def build_ch7_adjective_usage(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch7AdjectiveUsageExercise,
        'Chapter 7 — Adjective Usage Drill',
        'Hebrew Adjectives — Attributive, Predicate, and Substantival Uses',
        ['hebrew', 'bbh', 'ch7', 'exercises', 'ch7-adjective-usage'],
        'ch7-adjective-usage.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------


class Ch8PronounIdentificationExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each item: (1) Identify the pronoun type '
            '(Personal / Demonstrative / Relative / Interrogative), '
            '(2) Isolate the pronoun, '
            '(3) Parse it — give Person, Gender, Number (PGN) where applicable; '
            'for Relative and Interrogative write "indecl.", '
            '(4) Translate the full phrase.'
        )
        rows = [
            ['1', 'אֲנִי יְהוָה אֱלֹהֵיכֶם', '', '', '', ''],
            ['2', 'אַתָּה עַבְדִּי', '', '', '', ''],
            ['3', 'הוּא הַכֹּהֵן', '', '', '', ''],
            ['4', 'הִיא הַמַּלְכָּה', '', '', '', ''],
            ['5', 'אֲנַחְנוּ עֲבָדֶיךָ', '', '', '', ''],
            ['6', 'אַתֶּם עֵדַי', '', '', '', ''],
            ['7', 'אָנֹכִי הָאִישׁ', '', '', '', ''],
            ['8', 'הֵם הַכֹּהֲנִים', '', '', '', ''],
            ['9', 'הָאִישׁ הַזֶּה', '', '', '', ''],
            ['10', 'הָאִשָּׁה הַזֹּאת', '', '', '', ''],
            ['11', 'הַדְּבָרִים הָאֵלֶּה', '', '', '', ''],
            ['12', 'זֶה הָאִישׁ', '', '', '', ''],
            ['13', 'זֹאת הָאָרֶץ', '', '', '', ''],
            ['14', 'בַּיּוֹם הַהוּא', '', '', '', ''],
            ['15', 'בָּעֵת הַהִיא', '', '', '', ''],
            ['16', 'הָאִישׁ אֲשֶׁר בָּא', '', '', '', ''],
            ['17', 'הָאִשָּׁה אֲשֶׁר רָאִיתִי', '', '', '', ''],
            ['18', 'הָאָרֶץ אֲשֶׁר נָתַן יְהוָה לָנוּ', '', '', '', ''],
            ['19', 'הָאִישׁ אֲשֶׁר עָבַד אֶת יְהוָה', '', '', '', ''],
            ['20', 'הַמִּצְוָה אֲשֶׁר צִוִּיתִיךָ', '', '', '', ''],
            ['21', 'הַדָּבָר אֲשֶׁר שָׁמַעְתָּ', '', '', '', ''],
            ['22', 'מִי אַתָּה', '', '', '', ''],
            ['23', 'מַה זֶּה', '', '', '', ''],
            ['24', 'מִי הָאִישׁ הַזֶּה', '', '', '', ''],
            ['25', 'מַה עָשִׂיתָ', '', '', '', ''],
        ]
        ans = [
            ['1', 'אֲנִי יְהוָה אֱלֹהֵיכֶם', 'Personal', 'אֲנִי', '1cs', 'I am the LORD your God'],
            ['2', 'אַתָּה עַבְדִּי', 'Personal', 'אַתָּה', '2ms', 'You are my servant'],
            ['3', 'הוּא הַכֹּהֵן', 'Personal', 'הוּא', '3ms', 'He is the priest'],
            ['4', 'הִיא הַמַּלְכָּה', 'Personal', 'הִיא', '3fs', 'She is the queen'],
            ['5', 'אֲנַחְנוּ עֲבָדֶיךָ', 'Personal', 'אֲנַחְנוּ', '1cp', 'We are your servants'],
            ['6', 'אַתֶּם עֵדַי', 'Personal', 'אַתֶּם', '2mp', 'You are my witnesses'],
            ['7', 'אָנֹכִי הָאִישׁ', 'Personal', 'אָנֹכִי', '1cs', 'I am the man'],
            ['8', 'הֵם הַכֹּהֲנִים', 'Personal', 'הֵם', '3mp', 'They are the priests'],
            ['9', 'הָאִישׁ הַזֶּה', 'Demonstrative', 'הַזֶּה', 'ms (near)', 'this man'],
            ['10', 'הָאִשָּׁה הַזֹּאת', 'Demonstrative', 'הַזֹּאת', 'fs (near)', 'this woman'],
            ['11', 'הַדְּבָרִים הָאֵלֶּה', 'Demonstrative', 'הָאֵלֶּה', 'cp (near)', 'these words/things'],
            ['12', 'זֶה הָאִישׁ', 'Demonstrative', 'זֶה', 'ms (near)', 'This is the man'],
            ['13', 'זֹאת הָאָרֶץ', 'Demonstrative', 'זֹאת', 'fs (near)', 'This is the land'],
            ['14', 'בַּיּוֹם הַהוּא', 'Demonstrative', 'הַהוּא', 'ms (far)', 'on that day'],
            ['15', 'בָּעֵת הַהִיא', 'Demonstrative', 'הַהִיא', 'fs (far)', 'at that time'],
            ['16', 'הָאִישׁ אֲשֶׁר בָּא', 'Relative', 'אֲשֶׁר', 'indecl.', 'the man who came'],
            ['17', 'הָאִשָּׁה אֲשֶׁר רָאִיתִי', 'Relative', 'אֲשֶׁר', 'indecl.', 'the woman whom I saw'],
            ['18', 'הָאָרֶץ אֲשֶׁר נָתַן יְהוָה לָנוּ', 'Relative', 'אֲשֶׁר', 'indecl.', 'the land that the LORD gave to us'],
            ['19', 'הָאִישׁ אֲשֶׁר עָבַד אֶת יְהוָה', 'Relative', 'אֲשֶׁר', 'indecl.', 'the man who served the LORD'],
            ['20', 'הַמִּצְוָה אֲשֶׁר צִוִּיתִיךָ', 'Relative', 'אֲשֶׁר', 'indecl.', 'the commandment that I commanded you'],
            ['21', 'הַדָּבָר אֲשֶׁר שָׁמַעְתָּ', 'Relative', 'אֲשֶׁר', 'indecl.', 'the word/thing that you heard'],
            ['22', 'מִי אַתָּה', 'Interrogative', 'מִי', 'indecl.', 'Who are you?'],
            ['23', 'מַה זֶּה', 'Interrogative', 'מַה', 'indecl.', 'What is this?'],
            ['24', 'מִי הָאִישׁ הַזֶּה', 'Interrogative', 'מִי', 'indecl.', 'Who is this man?'],
            ['25', 'מַה עָשִׂיתָ', 'Interrogative', 'מַה', 'indecl.', 'What have you done?'],
        ]
        self.add_generic_table(
            headers=['#', 'Hebrew', 'Pronoun Type', 'Pronoun', 'Parse (PGN)', 'Translation'],
            rows=rows,
            col_ratios=[0.05, 0.22, 0.14, 0.12, 0.10, 0.37],
            heb_cols=[1],
            show_answers=True,
            answer_rows=ans,
        )


def build_ch8_pronoun_identification(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch8PronounIdentificationExercise,
        'Chapter 8 — Pronoun Identification Drill',
        'Personal, Demonstrative, Relative, and Interrogative Pronouns',
        ['hebrew', 'bbh', 'ch8', 'exercises', 'ch8-pronoun-identification'],
        'ch8-pronoun-identification.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------


class Ch9SuffixParsingExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each Hebrew form below: '
            '(1) Base Word — identify the underlying noun, preposition, or particle; '
            '(2) Suffix — write the suffix element only; '
            '(3) Parse (PGN) — Person-Gender-Number of the suffix; '
            '(4) Translation — full translation of the suffixed form.'
        )
        rows = [
            ['1', 'סוּסוֹ', '', '', '', ''],
            ['2', 'דְּבָרִי', '', '', '', ''],
            ['3', 'מַלְכְּכֶם', '', '', '', ''],
            ['4', 'אָחִיהָ', '', '', '', ''],
            ['5', 'בֵּיתְךָ', '', '', '', ''],
            ['6', 'עַמֵּנוּ', '', '', '', ''],
            ['7', 'אֲדֹנֵיכֶם', '', '', '', ''],
            ['8', 'בְּנָהּ', '', '', '', ''],
            ['9', 'שְׁמֵיהֶם', '', '', '', ''],
            ['10', 'אַרְצָם', '', '', '', ''],
            ['11', 'לִי', '', '', '', ''],
            ['12', 'לְךָ', '', '', '', ''],
            ['13', 'לָהּ', '', '', '', ''],
            ['14', 'לָנוּ', '', '', '', ''],
            ['15', 'לָכֶם', '', '', '', ''],
            ['16', 'בָּהּ', '', '', '', ''],
            ['17', 'בָּם', '', '', '', ''],
            ['18', 'עִמִּי', '', '', '', ''],
            ['19', 'אֵלֶיךָ', '', '', '', ''],
            ['20', 'עָלָיו', '', '', '', ''],
            ['21', 'אֹתִי', '', '', '', ''],
            ['22', 'אֹתוֹ', '', '', '', ''],
            ['23', 'אֹתָהּ', '', '', '', ''],
            ['24', 'אֹתָנוּ', '', '', '', ''],
            ['25', 'אֹתָם', '', '', '', ''],
        ]
        ans = [
            ['1', 'סוּסוֹ', 'סוּס (horse)', 'וֹ', '3ms', 'his horse'],
            ['2', 'דְּבָרִי', 'דָּבָר (word)', 'ִי', '1cs', 'my word'],
            ['3', 'מַלְכְּכֶם', 'מֶלֶךְ (king)', 'כֶם', '2mp', 'your (mp) king'],
            ['4', 'אָחִיהָ', 'אָח (brother)', 'הָ', '3fs', 'her brother'],
            ['5', 'בֵּיתְךָ', 'בַּיִת (house)', 'ְךָ', '2ms', 'your (ms) house'],
            ['6', 'עַמֵּנוּ', 'עַם (people)', 'ֵנוּ', '1cp', 'our people'],
            ['7', 'אֲדֹנֵיכֶם', 'אָדוֹן (lord/master)', 'ֵיכֶם', '2mp', 'your (mp) lord/masters'],
            ['8', 'בְּנָהּ', 'בֵּן (son)', 'הָ', '3fs', 'her son'],
            ['9', 'שְׁמֵיהֶם', 'שָׁמַיִם (heavens)', 'ֵיהֶם', '3mp', 'their (m) heavens'],
            ['10', 'אַרְצָם', 'אֶרֶץ (land/earth)', 'ָם', '3mp', 'their (m) land'],
            ['11', 'לִי', 'לְ (to/for)', 'ִי', '1cs', 'to/for me'],
            ['12', 'לְךָ', 'לְ (to/for)', 'ְךָ', '2ms', 'to/for you (ms)'],
            ['13', 'לָהּ', 'לְ (to/for)', 'הָ', '3fs', 'to/for her'],
            ['14', 'לָנוּ', 'לְ (to/for)', 'ֵנוּ', '1cp', 'to/for us'],
            ['15', 'לָכֶם', 'לְ (to/for)', 'כֶם', '2mp', 'to/for you (mp)'],
            ['16', 'בָּהּ', 'בְּ (in/with)', 'הָ', '3fs', 'in/with her'],
            ['17', 'בָּם', 'בְּ (in/with)', 'ָם', '3mp', 'in/with them (m)'],
            ['18', 'עִמִּי', 'עִם (with)', 'ִי', '1cs', 'with me'],
            ['19', 'אֵלֶיךָ', 'אֶל (to/toward)', 'ְךָ', '2ms', 'to/toward you (ms)'],
            ['20', 'עָלָיו', 'עַל (upon/over)', 'ָיו', '3ms', 'upon/over him'],
            ['21', 'אֹתִי', 'אֵת (DOM)', 'ִי', '1cs', 'me (direct object)'],
            ['22', 'אֹתוֹ', 'אֵת (DOM)', 'וֹ', '3ms', 'him (direct object)'],
            ['23', 'אֹתָהּ', 'אֵת (DOM)', 'הָ', '3fs', 'her (direct object)'],
            ['24', 'אֹתָנוּ', 'אֵת (DOM)', 'ֵנוּ', '1cp', 'us (direct object)'],
            ['25', 'אֹתָם', 'אֵת (DOM)', 'ָם', '3mp', 'them (m, direct object)'],
        ]
        self.add_generic_table(
            headers=['#', 'Hebrew', 'Base Word', 'Suffix', 'Parse (PGN)', 'Translation'],
            rows=rows,
            col_ratios=[0.05, 0.12, 0.18, 0.10, 0.10, 0.45],
            heb_cols=[1],
            show_answers=True,
            answer_rows=ans,
        )


def build_ch9_suffix_parsing(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch9SuffixParsingExercise,
        'Chapter 9 — Hebrew Pronominal Suffix Parsing Drill',
        'Pronominal Suffixes on Nouns, Prepositions, and the DOM',
        ['hebrew', 'bbh', 'ch9', 'exercises', 'ch9-suffix-parsing'],
        'ch9-suffix-parsing.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------


class Ch10ConstructChainExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each item: (1) identify the construct noun (nomen regens) and its form type, '
            '(2) identify the absolute noun (nomen rectum), '
            '(3) state whether the chain is definite or indefinite, '
            '(4) translate into natural English.'
        )
        hdrs = ['#', 'Hebrew', 'Construct Noun', 'Absolute Noun', 'Definite?', 'Translation']
        cr = [0.05, 0.20, 0.22, 0.18, 0.08, 0.27]
        hc = [1]

        self.add_section_heading('Part A — Simple 2-Link Chains (Indefinite) (1–8)')
        rows_a = [
            ['1', 'דְּבַר מֶלֶךְ', '', '', '', ''],
            ['2', 'בֵּית אִישׁ', '', '', '', ''],
            ['3', 'כְּבוֹד עָם', '', '', '', ''],
            ['4', 'עֶבֶד מֶלֶךְ', '', '', '', ''],
            ['5', 'בְּנֵי אָדָם', '', '', '', ''],
            ['6', 'סֵפֶר תּוֹרָה', '', '', '', ''],
            ['7', 'כֹּהֵן אֱלֹהִים', '', '', '', ''],
            ['8', 'רוּחַ אָדָם', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'דְּבַר מֶלֶךְ', 'דְּבַר (ms cstr of דָּבָר)', 'מֶלֶךְ', 'No', 'a word of a king'],
            ['2', 'בֵּית אִישׁ', 'בֵּית (ms cstr of בַּיִת)', 'אִישׁ', 'No', "a man's house"],
            ['3', 'כְּבוֹד עָם', 'כְּבוֹד (ms cstr of כָּבוֹד)', 'עָם', 'No', 'glory of a people'],
            ['4', 'עֶבֶד מֶלֶךְ', 'עֶבֶד (ms cstr; segolate, unchanged)', 'מֶלֶךְ', 'No', 'a servant of a king'],
            ['5', 'בְּנֵי אָדָם', 'בְּנֵי (mp cstr of בֵּן; ִים → ֵי)', 'אָדָם', 'No', 'sons of man / humankind'],
            ['6', 'סֵפֶר תּוֹרָה', 'סֵפֶר (ms cstr; segolate, unchanged)', 'תּוֹרָה', 'No', 'a book of the law'],
            ['7', 'כֹּהֵן אֱלֹהִים', 'כֹּהֵן (ms cstr; unchanged)', 'אֱלֹהִים', 'No', 'a priest of God'],
            ['8', 'רוּחַ אָדָם', 'רוּחַ (fs cstr of רוּחַ; unchanged)', 'אָדָם', 'No', 'the spirit of man'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_a, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Part B — Simple 2-Link Chains (Definite) (9–16)')
        rows_b = [
            ['9', 'דְּבַר יְהוָה', '', '', '', ''],
            ['10', 'בֵּית יְהוָה', '', '', '', ''],
            ['11', 'כְּבוֹד יְהוָה', '', '', '', ''],
            ['12', 'שֵׁם יְהוָה', '', '', '', ''],
            ['13', 'בֵּית הַמֶּלֶךְ', '', '', '', ''],
            ['14', 'מֶלֶךְ יִשְׂרָאֵל', '', '', '', ''],
            ['15', 'עִיר דָּוִד', '', '', '', ''],
            ['16', 'בְּנֵי יִשְׂרָאֵל', '', '', '', ''],
        ]
        ans_b = [
            ['9', 'דְּבַר יְהוָה', 'דְּבַר (ms cstr; propretonic reduction)', 'יְהוָה (proper)', 'Yes', 'the word of the LORD'],
            ['10', 'בֵּית יְהוָה', 'בֵּית (ms cstr of בַּיִת)', 'יְהוָה (proper)', 'Yes', 'the house of the LORD'],
            ['11', 'כְּבוֹד יְהוָה', 'כְּבוֹד (ms cstr of כָּבוֹד)', 'יְהוָה (proper)', 'Yes', 'the glory of the LORD'],
            ['12', 'שֵׁם יְהוָה', 'שֵׁם (ms cstr; unchanged)', 'יְהוָה (proper)', 'Yes', 'the name of the LORD'],
            ['13', 'בֵּית הַמֶּלֶךְ', 'בֵּית (ms cstr)', 'הַמֶּלֶךְ (definite art.)', 'Yes', "the king's house"],
            ['14', 'מֶלֶךְ יִשְׂרָאֵל', 'מֶלֶךְ (ms cstr; segolate, unchanged)', 'יִשְׂרָאֵל (proper)', 'Yes', 'the king of Israel'],
            ['15', 'עִיר דָּוִד', 'עִיר (fs cstr; unchanged)', 'דָּוִד (proper)', 'Yes', 'the city of David'],
            ['16', 'בְּנֵי יִשְׂרָאֵל', 'בְּנֵי (mp cstr; ִים → ֵי)', 'יִשְׂרָאֵל (proper)', 'Yes', 'the sons/children of Israel'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Part C — Extended 3-Link Chains (17–21)')
        rows_c = [
            ['17', 'דְּבַר תּוֹרַת יְהוָה', '', '', '', ''],
            ['18', 'בֵּית אֱלֹהֵי יִשְׂרָאֵל', '', '', '', ''],
            ['19', 'מֶלֶךְ מַלְכֵי הַמְּלָכִים', '', '', '', ''],
            ['20', 'שֵׁם יְהוָה אֱלֹהֵינוּ', '', '', '', ''],
            ['21', 'עֶבֶד עַבְדֵי הַמֶּלֶךְ', '', '', '', ''],
        ]
        ans_c = [
            ['17', 'דְּבַר תּוֹרַת יְהוָה', 'דְּבַר, תּוֹרַת (both construct)', 'יְהוָה (proper)', 'Yes', 'the word of the law of the LORD'],
            ['18', 'בֵּית אֱלֹהֵי יִשְׂרָאֵל', 'בֵּית, אֱלֹהֵי (both construct)', 'יִשְׂרָאֵל (proper)', 'Yes', 'the house of the God of Israel'],
            ['19', 'מֶלֶךְ מַלְכֵי הַמְּלָכִים', 'מֶלֶךְ, מַלְכֵי (both construct)', 'הַמְּלָכִים (def. art.)', 'Yes', 'the king of kings of the kings'],
            ['20', 'שֵׁם יְהוָה אֱלֹהֵינוּ', 'שֵׁם (construct)', 'יְהוָה אֱלֹהֵינוּ (proper + appositive)', 'Yes', 'the name of the LORD our God'],
            ['21', 'עֶבֶד עַבְדֵי הַמֶּלֶךְ', 'עֶבֶד, עַבְדֵי (both construct)', 'הַמֶּלֶךְ (def. art.)', 'Yes', 'servant of the servants of the king'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_c, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_c)

        self.add_section_heading('Part D — Feminine Construct Nouns (22–25)')
        rows_d = [
            ['22', 'תּוֹרַת מֹשֶׁה', '', '', '', ''],
            ['23', 'תּוֹרַת יְהוָה', '', '', '', ''],
            ['24', 'מַלְכַּת שְׁבָא', '', '', '', ''],
            ['25', 'בִּרְכַּת יְהוָה', '', '', '', ''],
        ]
        ans_d = [
            ['22', 'תּוֹרַת מֹשֶׁה', 'תּוֹרַת (fs cstr; תּוֹרָה → תּוֹרַת)', 'מֹשֶׁה (proper)', 'Yes', 'the law/Torah of Moses'],
            ['23', 'תּוֹרַת יְהוָה', 'תּוֹרַת (fs cstr)', 'יְהוָה (proper)', 'Yes', 'the law/Torah of the LORD'],
            ['24', 'מַלְכַּת שְׁבָא', 'מַלְכַּת (fs cstr; מַלְכָּה → מַלְכַּת)', 'שְׁבָא (proper)', 'Yes', 'the queen of Sheba'],
            ['25', 'בִּרְכַּת יְהוָה', 'בִּרְכַּת (fs cstr; בְּרָכָה → בִּרְכַּת)', 'יְהוָה (proper)', 'Yes', 'the blessing of the LORD'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_d, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_d)


def build_ch10_construct_chain(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch10ConstructChainExercise,
        'Chapter 10 — Construct Chain Drill',
        'BBH Chapter 10 — Hebrew Construct Chain',
        ['hebrew', 'bbh', 'ch10', 'exercises', 'ch10-construct-chain'],
        'ch10-construct-chain.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------


class Ch11NumberIdentificationExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each Hebrew number-noun phrase: '
            '(1) identify the number word, '
            '(2) give its numeric value, '
            '(3) note the gender polarity situation (if applicable), '
            '(4) provide a translation.\n'
            'Gender Polarity: write "Yes — [noun gender] noun + [form used]" where polarity applies; '
            '"N/A (tens)" for multiples of ten; "N/A (1–2)" for ones and twos; '
            '"N/A (ordinal)" for ordinals.'
        )
        rows = [
            ['1', 'שִׁבְעָה יָמִים', '', '', '', ''],
            ['2', 'שָׁלֹשׁ נָשִׁים', '', '', '', ''],
            ['3', 'אַרְבָּעִים שָׁנָה', '', '', '', ''],
            ['4', 'שְׁנֵי אֲנָשִׁים', '', '', '', ''],
            ['5', 'עֶשֶׂר עָרִים', '', '', '', ''],
            ['6', 'חֲמִשָּׁה שְׁבָטִים', '', '', '', ''],
            ['7', 'שְׁתַּיִם עֶשְׂרֵה שָׁנָה', '', '', '', ''],
            ['8', 'שִׁשָּׁה בָּנִים', '', '', '', ''],
            ['9', 'שְׁלֹשִׁים אִישׁ', '', '', '', ''],
            ['10', 'תִּשְׁעָה אֲנָשִׁים', '', '', '', ''],
            ['11', 'שְׁנֵים עָשָׂר שֵׁבֶט', '', '', '', ''],
            ['12', 'אַרְבַּע בָּנוֹת', '', '', '', ''],
            ['13', 'חֲמִשָּׁה עָשָׂר אִישׁ', '', '', '', ''],
            ['14', 'שִׁבְעִים זָקֵן', '', '', '', ''],
            ['15', 'שֵׁשׁ שָׁנִים', '', '', '', ''],
            ['16', 'שְׁלֹשׁ עֶשְׂרֵה עִיר', '', '', '', ''],
            ['17', 'בַּיּוֹם הַשְּׁבִיעִי', '', '', '', ''],
            ['18', 'בַּחֹדֶשׁ הָרִאשׁוֹן', '', '', '', ''],
            ['19', 'הַשַּׁעַר הַשֵּׁנִי', '', '', '', ''],
            ['20', 'הַיּוֹם הָעֲשִׂירִי', '', '', '', ''],
        ]
        ans = [
            ['1', 'שִׁבְעָה יָמִים', 'שִׁבְעָה', '7', 'Yes — masc. noun + ה-form', 'seven days'],
            ['2', 'שָׁלֹשׁ נָשִׁים', 'שָׁלֹשׁ', '3', 'Yes — fem. noun + non-ה-form', 'three women'],
            ['3', 'אַרְבָּעִים שָׁנָה', 'אַרְבָּעִים', '40', 'N/A (tens — no polarity)', 'forty years'],
            ['4', 'שְׁנֵי אֲנָשִׁים', 'שְׁנֵי', '2', 'N/A (1–2 agree normally)', 'two men'],
            ['5', 'עֶשֶׂר עָרִים', 'עֶשֶׂר', '10', 'Yes — fem. noun + non-ה-form', 'ten cities'],
            ['6', 'חֲמִשָּׁה שְׁבָטִים', 'חֲמִשָּׁה', '5', 'Yes — masc. noun + ה-form', 'five tribes'],
            ['7', 'שְׁתַּיִם עֶשְׂרֵה שָׁנָה', 'שְׁתַּיִם עֶשְׂרֵה', '12', 'N/A (teens — 12 uses dual form)', 'twelve years'],
            ['8', 'שִׁשָּׁה בָּנִים', 'שִׁשָּׁה', '6', 'Yes — masc. noun + ה-form', 'six sons'],
            ['9', 'שְׁלֹשִׁים אִישׁ', 'שְׁלֹשִׁים', '30', 'N/A (tens — invariable)', 'thirty men'],
            ['10', 'תִּשְׁעָה אֲנָשִׁים', 'תִּשְׁעָה', '9', 'Yes — masc. noun + ה-form', 'nine men'],
            ['11', 'שְׁנֵים עָשָׂר שֵׁבֶט', 'שְׁנֵים עָשָׂר', '12', 'N/A (teens with masc. noun)', 'twelve tribes'],
            ['12', 'אַרְבַּע בָּנוֹת', 'אַרְבַּע', '4', 'Yes — fem. noun + non-ה-form', 'four daughters'],
            ['13', 'חֲמִשָּׁה עָשָׂר אִישׁ', 'חֲמִשָּׁה עָשָׂר', '15', 'Yes (unit) — masc. noun + ה-form unit', 'fifteen men'],
            ['14', 'שִׁבְעִים זָקֵן', 'שִׁבְעִים', '70', 'N/A (tens — invariable)', 'seventy elders'],
            ['15', 'שֵׁשׁ שָׁנִים', 'שֵׁשׁ', '6', 'Yes — fem. noun + non-ה-form', 'six years'],
            ['16', 'שְׁלֹשׁ עֶשְׂרֵה עִיר', 'שְׁלֹשׁ עֶשְׂרֵה', '13', 'Yes (unit) — fem. noun + non-ה-form unit', 'thirteen cities'],
            ['17', 'בַּיּוֹם הַשְּׁבִיעִי', 'הַשְּׁבִיעִי', '7th', 'N/A (ordinal; agrees as adj.)', 'on the seventh day'],
            ['18', 'בַּחֹדֶשׁ הָרִאשׁוֹן', 'הָרִאשׁוֹן', '1st', 'N/A (ordinal; agrees as adj.)', 'in the first month'],
            ['19', 'הַשַּׁעַר הַשֵּׁנִי', 'הַשֵּׁנִי', '2nd', 'N/A (ordinal; agrees as adj.)', 'the second gate'],
            ['20', 'הַיּוֹם הָעֲשִׂירִי', 'הָעֲשִׂירִי', '10th', 'N/A (ordinal; agrees as adj.)', 'the tenth day'],
        ]
        self.add_generic_table(
            headers=['#', 'Hebrew Phrase', 'Number Word', 'Value', 'Gender Polarity?', 'Translation'],
            rows=rows,
            col_ratios=[0.05, 0.22, 0.16, 0.07, 0.18, 0.32],
            heb_cols=[1],
            show_answers=True,
            answer_rows=ans,
        )


def build_ch11_number_identification(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch11NumberIdentificationExercise,
        'Chapter 11 — Number Identification Drill',
        'Hebrew Numbers — Cardinals, Teens, Tens, and Ordinals',
        ['hebrew', 'bbh', 'ch11', 'exercises', 'ch11-number-identification'],
        'ch11-number-identification.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------


class Ch12VerbOverviewExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Part A: For each Hebrew verb form and its gloss, identify: '
            '(1) the stem, (2) whether it expresses Active, Passive, or Reflexive meaning, '
            '(3) the three-letter root.\n'
            'Part B: For each English description of an action, identify which stem would be '
            'used in Hebrew and explain briefly why.\n'
            'Note: You do not need to parse conjugation or PGN yet.'
        )
        self.add_section_heading('Part A — Stem Identification (1–12)')
        rows_a = [
            ['1', 'שָׁמַר', '"he guarded"', '', '', ''],
            ['2', 'כָּתַב', '"he wrote"', '', '', ''],
            ['3', 'נָתַן', '"he gave"', '', '', ''],
            ['4', 'הָלַךְ', '"he walked"', '', '', ''],
            ['5', 'נִשְׁמַר', '"he was guarded / he kept himself"', '', '', ''],
            ['6', 'נִכְתַּב', '"it was written"', '', '', ''],
            ['7', 'הִשְׁמִיר', '"he caused to guard"', '', '', ''],
            ['8', 'הוֹלִיךְ', '"he caused to walk / he led"', '', '', ''],
            ['9', 'כִּתֵּב', '"he wrote (intensively / repeatedly)"', '', '', ''],
            ['10', 'שִׁמֵּר', '"he kept carefully / he tended"', '', '', ''],
            ['11', 'כֻּתַּב', '"it was written (intensive passive)"', '', '', ''],
            ['12', 'הִתְהַלֵּךְ', '"he walked about / he walked to and fro"', '', '', ''],
        ]
        ans_a = [
            ['1', 'שָׁמַר', '"he guarded"', 'Qal', 'Active', 'שמר'],
            ['2', 'כָּתַב', '"he wrote"', 'Qal', 'Active', 'כתב'],
            ['3', 'נָתַן', '"he gave"', 'Qal', 'Active', 'נתן'],
            ['4', 'הָלַךְ', '"he walked"', 'Qal', 'Active', 'הלך'],
            ['5', 'נִשְׁמַר', '"he was guarded / he kept himself"', 'Niphal', 'Passive/Reflexive', 'שמר'],
            ['6', 'נִכְתַּב', '"it was written"', 'Niphal', 'Passive', 'כתב'],
            ['7', 'הִשְׁמִיר', '"he caused to guard"', 'Hiphil', 'Active (causative)', 'שמר'],
            ['8', 'הוֹלִיךְ', '"he caused to walk / he led"', 'Hiphil', 'Active (causative)', 'הלך'],
            ['9', 'כִּתֵּב', '"he wrote (intensively)"', 'Piel', 'Active (intensive)', 'כתב'],
            ['10', 'שִׁמֵּר', '"he kept carefully"', 'Piel', 'Active (intensive)', 'שמר'],
            ['11', 'כֻּתַּב', '"it was written (intensive passive)"', 'Pual', 'Passive', 'כתב'],
            ['12', 'הִתְהַלֵּךְ', '"he walked about / to and fro"', 'Hithpael', 'Reflexive', 'הלך'],
        ]
        self.add_generic_table(
            headers=['#', 'Verb', 'Gloss', 'Stem', 'Active/Passive/Reflexive', 'Root'],
            rows=rows_a,
            col_ratios=[0.05, 0.12, 0.24, 0.12, 0.20, 0.27],
            heb_cols=[1],
            show_answers=True,
            answer_rows=ans_a,
        )
        self.add_section_heading('Part B — Meaning to Stem (1–8)')
        rows_b = [
            ['1', 'God caused Abraham to go out from Ur', '', ''],
            ['2', 'The letter was written by the scribe (simple passive)', '', ''],
            ['3', 'David walked around in his palace repeatedly', '', ''],
            ['4', 'The king was caused to reign (someone put him on the throne)', '', ''],
            ['5', 'She kept/guarded herself (simple reflexive)', '', ''],
            ['6', 'He wrote intensively / inscribed over and over (intensive passive)', '', ''],
            ['7', 'He killed himself thoroughly / destroyed himself (reflexive intensive)', '', ''],
            ['8', 'Moses guarded (base meaning, simple active)', '', ''],
        ]
        ans_b = [
            ['1', 'God caused Abraham to go out from Ur', 'Hiphil', 'Hiphil is causative active — subject causes another to perform the action.'],
            ['2', 'The letter was written (simple passive)', 'Niphal', 'Niphal is the simple passive (and reflexive) of the Qal.'],
            ['3', 'David walked around repeatedly', 'Hithpael', 'Hithpael is reflexive-intensive; הִתְהַלֵּךְ = "walk about/to and fro."'],
            ['4', 'The king was caused to reign', 'Hophal', 'Hophal is the causative passive — passive counterpart of the Hiphil.'],
            ['5', 'She kept/guarded herself (simple reflexive)', 'Niphal', 'Niphal doubles as reflexive for simple actions.'],
            ['6', 'He wrote intensively / inscribed over and over (intensive passive)', 'Pual', 'Pual is the passive counterpart of the Piel (intensive passive).'],
            ['7', 'He killed himself thoroughly (reflexive intensive)', 'Hithpael', 'Hithpael is reflexive and intensive — combines thoroughness with self-direction.'],
            ['8', 'Moses guarded (simple active)', 'Qal', 'Qal is the base, simple active stem.'],
        ]
        self.add_generic_table(
            headers=['#', 'Description', 'Stem', 'Explanation'],
            rows=rows_b,
            col_ratios=[0.05, 0.30, 0.12, 0.53],
            heb_cols=[],
            show_answers=True,
            answer_rows=ans_b,
        )


def build_ch12_verb_overview(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch12VerbOverviewExercise,
        'Chapter 12 — Verb Overview Exercise',
        'BBH Chapter 12 · 20 items',
        ['hebrew', 'bbh', 'ch12', 'exercises', 'ch12-verb-overview'],
        'ch12-verb-overview.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Ch13–Ch15 builders
# ---------------------------------------------------------------------------


class Ch13ParsingDrillExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each form, give: (a) Person, (b) Number, (c) Gender, '
            '(d) Root (3ms lexical form).\n'
            'Part C only: also identify the stative type '
            '(B = tsere, C = holem).'
        )
        hdrs_ab = ['#', 'Form', 'Person', 'Number', 'Gender', 'Root']
        cr_ab = [0.05, 0.16, 0.10, 0.10, 0.10, 0.49]
        hc = [1]

        self.add_section_heading('Part A — Clear Suffix Pattern (1–10)')
        rows_a = [
            ['1', 'שָׁמַרְתָּ', '', '', '', ''],
            ['2', 'כָּתַבְתִּי', '', '', '', ''],
            ['3', 'שָׁמְרוּ', '', '', '', ''],
            ['4', 'פָּקַדְנוּ', '', '', '', ''],
            ['5', 'מָשַׁלְתְּ', '', '', '', ''],
            ['6', 'בָּחַרְתֶּם', '', '', '', ''],
            ['7', 'זָכַרְתִּי', '', '', '', ''],
            ['8', 'לָמַד', '', '', '', ''],
            ['9', 'שָׁמַרְתֶּן', '', '', '', ''],
            ['10', 'חָפַרְתָּ', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'שָׁמַרְתָּ', '2', 's', 'm', 'שמר'],
            ['2', 'כָּתַבְתִּי', '1', 's', 'c', 'כתב'],
            ['3', 'שָׁמְרוּ', '3', 'p', 'c', 'שמר'],
            ['4', 'פָּקַדְנוּ', '1', 'p', 'c', 'פקד'],
            ['5', 'מָשַׁלְתְּ', '2', 's', 'f', 'משל'],
            ['6', 'בָּחַרְתֶּם', '2', 'p', 'm', 'בחר'],
            ['7', 'זָכַרְתִּי', '1', 's', 'c', 'זכר'],
            ['8', 'לָמַד', '3', 's', 'm', 'למד'],
            ['9', 'שָׁמַרְתֶּן', '2', 'p', 'f', 'שמר'],
            ['10', 'חָפַרְתָּ', '2', 's', 'm', 'חפר'],
        ]
        self.add_generic_table(headers=hdrs_ab, rows=rows_a, col_ratios=cr_ab, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Part B — Vowel Reduction Forms (11–20)')
        rows_b = [
            ['11', 'כָּתְבוּ', '', '', '', ''],
            ['12', 'שְׁמַרְתֶּם', '', '', '', ''],
            ['13', 'פָּקְדָה', '', '', '', ''],
            ['14', 'בָּחְרוּ', '', '', '', ''],
            ['15', 'מְשַׁלְתֶּן', '', '', '', ''],
            ['16', 'זָכַר', '', '', '', ''],
            ['17', 'חָפְרָה', '', '', '', ''],
            ['18', 'לָמְדוּ', '', '', '', ''],
            ['19', 'שְׁמַרְתֶּן', '', '', '', ''],
            ['20', 'פָּקַדְתְּ', '', '', '', ''],
        ]
        ans_b = [
            ['11', 'כָּתְבוּ', '3', 'p', 'c', 'כתב'],
            ['12', 'שְׁמַרְתֶּם', '2', 'p', 'm', 'שמר'],
            ['13', 'פָּקְדָה', '3', 's', 'f', 'פקד'],
            ['14', 'בָּחְרוּ', '3', 'p', 'c', 'בחר'],
            ['15', 'מְשַׁלְתֶּן', '2', 'p', 'f', 'משל'],
            ['16', 'זָכַר', '3', 's', 'm', 'זכר'],
            ['17', 'חָפְרָה', '3', 's', 'f', 'חפר'],
            ['18', 'לָמְדוּ', '3', 'p', 'c', 'למד'],
            ['19', 'שְׁמַרְתֶּן', '2', 'p', 'f', 'שמר'],
            ['20', 'פָּקַדְתְּ', '2', 's', 'f', 'פקד'],
        ]
        self.add_generic_table(headers=hdrs_ab, rows=rows_b, col_ratios=cr_ab, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Part C — Stative Roots (21–25)')
        rows_c = [
            ['21', 'כָּבַדְתָּ', '', '', '', '', ''],
            ['22', 'גָּדְלָה', '', '', '', '', ''],
            ['23', 'יָכֹלְתִּי', '', '', '', '', ''],
            ['24', 'זָקַנְתֶּם', '', '', '', '', ''],
            ['25', 'מָלְאָה', '', '', '', '', ''],
        ]
        ans_c = [
            ['21', 'כָּבַדְתָּ', '2', 's', 'm', 'כָּבֵד', 'B (tsere)'],
            ['22', 'גָּדְלָה', '3', 's', 'f', 'גָּדֵל', 'B (tsere)'],
            ['23', 'יָכֹלְתִּי', '1', 's', 'c', 'יָכֹל', 'C (holem)'],
            ['24', 'זָקַנְתֶּם', '2', 'p', 'm', 'זָקֵן', 'B (tsere)'],
            ['25', 'מָלְאָה', '3', 's', 'f', 'מָלֵא', 'B (tsere) / III-א'],
        ]
        self.add_generic_table(
            headers=['#', 'Form', 'Person', 'Number', 'Gender', 'Root (3ms)', 'Stative Type'],
            rows=rows_c,
            col_ratios=[0.05, 0.14, 0.09, 0.09, 0.09, 0.20, 0.34],
            heb_cols=hc,
            show_answers=True,
            answer_rows=ans_c,
        )


def build_ch13_parsing_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch13ParsingDrillExercise,
        'Chapter 13 — Parsing Drill: Qal Perfect Strong Verbs',
        'BBH Chapter 13',
        ['hebrew', 'bbh', 'ch13', 'exercises', 'ch13-parsing-drill'],
        'ch13-parsing-drill.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------


class Ch13PassageExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Parse each Qal Perfect verb. Give: '
            '(a) Person, (b) Number, (c) Gender, (d) Root (3ms lexical form), '
            '(e) Usage Type (Simple Past / Perfect of Experience / Stative / Prophetic Perfect).'
        )
        hdrs = ['#', 'Form', 'Person', 'Number', 'Gender', 'Root', 'Usage Type']
        cr = [0.05, 0.16, 0.09, 0.09, 0.09, 0.14, 0.38]
        hc = [1]

        self.add_section_heading('Passage A — Genesis 1:1–5 (1–2)')
        rows_a = [['1', 'בָּרָא', '', '', '', '', ''], ['2', 'הָיְתָה', '', '', '', '', '']]
        ans_a = [
            ['1', 'בָּרָא', '3', 's', 'm', 'ברא', 'Simple Past'],
            ['2', 'הָיְתָה', '3', 's', 'f', 'היה', 'Simple Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_a, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Passage B — Genesis 2:15–17 (3–4)')
        rows_b = [['3', 'אָכֹל', '', '', '', '', ''], ['4', 'אֲכָלְךָ', '', '', '', '', '']]
        ans_b = [
            ['3', 'אָכֹל', 'Inf. Abs.', '—', '—', 'אכל', 'Not a Perfect — Inf. Abs.'],
            ['4', 'אֲכָלְךָ', '2', 's', 'm', 'אכל', 'Simple Past + 2ms suffix'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Passage C — Genesis 3:6–13 (5–7)')
        rows_c = [
            ['5', 'נָתַתָּה', '', '', '', '', ''],
            ['6', 'נָתְנָה', '', '', '', '', ''],
            ['7', 'עָשִׂית', '', '', '', '', ''],
        ]
        ans_c = [
            ['5', 'נָתַתָּה', '2', 's', 'm', 'נתן', 'Simple Past'],
            ['6', 'נָתְנָה', '3', 's', 'f', 'נתן', 'Simple Past'],
            ['7', 'עָשִׂית', '2', 's', 'f', 'עשה', 'Simple Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_c, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_c)

        self.add_section_heading('Passage D — Genesis 4:1–10 (8–9)')
        rows_d = [['8', 'יָדַע', '', '', '', '', ''], ['9', 'יָדַעְתִּי', '', '', '', '', '']]
        ans_d = [
            ['8', 'יָדַע', '3', 's', 'm', 'ידע', 'Simple Past'],
            ['9', 'יָדַעְתִּי', '1', 's', 'c', 'ידע', 'Perfect of Experience'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_d, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_d)

        self.add_section_heading('Passage E — Additional Forms (10–15)')
        rows_e = [
            ['10', 'כָּבֵד', '', '', '', '', ''],
            ['11', 'שָׁמַעְנוּ', '', '', '', '', ''],
            ['12', 'קָטַלְתֶּם', '', '', '', '', ''],
            ['13', 'בָּרַכְתָּ', '', '', '', '', ''],
            ['14', 'יָשַׁבְנוּ', '', '', '', '', ''],
            ['15', 'קָרְאָה', '', '', '', '', ''],
        ]
        ans_e = [
            ['10', 'כָּבֵד', '3', 's', 'm', 'כבד', 'Stative'],
            ['11', 'שָׁמַעְנוּ', '1', 'p', 'c', 'שמע', 'Simple Past'],
            ['12', 'קָטַלְתֶּם', '2', 'p', 'm', 'קטל', 'Simple Past'],
            ['13', 'בָּרַכְתָּ', '2', 's', 'm', 'ברך', 'Simple Past'],
            ['14', 'יָשַׁבְנוּ', '1', 'p', 'c', 'ישב', 'Simple Past'],
            ['15', 'קָרְאָה', '3', 's', 'f', 'קרא', 'Simple Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_e, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_e)


def build_ch13_passage_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch13PassageExercise,
        'Chapter 13 — Passage Exercise: Qal Perfect Strong Verbs',
        'BBH Chapter 13',
        ['hebrew', 'bbh', 'ch13', 'exercises', 'ch13-passage-exercise'],
        'ch13-passage-exercise.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------


class Ch14PassageExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Parse each highlighted Qal Perfect form. Give: '
            '(a) Person, (b) Number, (c) Gender, (d) Root (3ms lexical form), '
            '(e) Weak Class, (f) Usage Type.'
        )
        hdrs = ['#', 'Form', 'Person', 'Number', 'Gender', 'Root', 'Weak Class', 'Usage Type']
        cr = [0.05, 0.13, 0.08, 0.08, 0.08, 0.12, 0.14, 0.32]
        hc = [1]

        self.add_section_heading('Passage A — Genesis 3:1–13 (1–4)')
        rows_a = [
            ['1', 'הָיָה', '', '', '', '', '', ''],
            ['2', 'אָמַר', '', '', '', '', '', ''],
            ['3', 'אָכַלְנוּ', '', '', '', '', '', ''],
            ['4', 'עָשִׂית', '', '', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'הָיָה', '3', 's', 'm', 'היה', 'III-ה', 'Stative'],
            ['2', 'אָמַר', '3', 's', 'm', 'אמר', 'I-gutt.', 'Simple Past'],
            ['3', 'אָכַלְנוּ', '1', 'p', 'c', 'אכל', 'I-gutt.', 'Simple Past'],
            ['4', 'עָשִׂית', '2', 's', 'f', 'עשה', 'III-ה', 'Simple Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_a, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Passage B — Genesis 6:9–22 (5–8)')
        rows_b = [
            ['5', 'הָיָה', '', '', '', '', '', ''],
            ['6', 'בָּא', '', '', '', '', '', ''],
            ['7', 'מָלְאָה', '', '', '', '', '', ''],
            ['8', 'צִוָּה', '', '', '', '', '', ''],
        ]
        ans_b = [
            ['5', 'הָיָה', '3', 's', 'm', 'היה', 'III-ה', 'Stative'],
            ['6', 'בָּא', '3', 's', 'm', 'בוא', 'Biconsonantal', 'Simple Past'],
            ['7', 'מָלְאָה', '3', 's', 'f', 'מלא', 'III-א', 'Simple Past'],
            ['8', 'צִוָּה', '3', 's', 'm', 'צוה', 'III-ה', 'Simple Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Passage C — Genesis 22:1–12 (9–12)')
        rows_c = [
            ['9', 'נִסָּה', '', '', '', '', '', ''],
            ['10', 'אָהַבְתָּ', '', '', '', '', '', ''],
            ['11', 'יָדַעְתִּי', '', '', '', '', '', ''],
            ['12', 'חָשַׂכְתָּ', '', '', '', '', '', ''],
        ]
        ans_c = [
            ['9', 'נִסָּה', '3', 's', 'm', 'נסה', 'III-ה', 'Simple Past'],
            ['10', 'אָהַבְתָּ', '2', 's', 'm', 'אהב', 'I-gutt.', 'Perf. of Experience'],
            ['11', 'יָדַעְתִּי', '1', 's', 'c', 'ידע', 'I-י', 'Perf. of Experience'],
            ['12', 'חָשַׂכְתָּ', '2', 's', 'm', 'חשך', 'III-gutt.', 'Simple Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_c, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_c)

        self.add_section_heading('Passage D — Exodus 1:17–21 (13–14)')
        rows_d = [
            ['13', 'עָשׂוּ', '', '', '', '', '', ''],
            ['14', 'עֲשִׂיתֶן', '', '', '', '', '', ''],
        ]
        ans_d = [
            ['13', 'עָשׂוּ', '3', 'p', 'c', 'עשה', 'III-ה', 'Simple Past'],
            ['14', 'עֲשִׂיתֶן', '2', 'p', 'f', 'עשה', 'III-ה', 'Simple Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_d, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_d)

        self.add_section_heading('Passage E — Additional Forms (15–20)')
        rows_e = [
            ['15', 'שָׁמַעְנוּ', '', '', '', '', '', ''],
            ['16', 'בָּאוּ', '', '', '', '', '', ''],
            ['17', 'קָמָה', '', '', '', '', '', ''],
            ['18', 'יָלְדוּ', '', '', '', '', '', ''],
            ['19', 'נָתְנָה', '', '', '', '', '', ''],
            ['20', 'תַּמּוּ', '', '', '', '', '', ''],
        ]
        ans_e = [
            ['15', 'שָׁמַעְנוּ', '1', 'p', 'c', 'שמע', 'III-gutt.', 'Simple Past'],
            ['16', 'בָּאוּ', '3', 'p', 'c', 'בוא', 'Biconsonantal', 'Simple Past'],
            ['17', 'קָמָה', '3', 's', 'f', 'קום', 'Biconsonantal', 'Simple Past'],
            ['18', 'יָלְדוּ', '3', 'p', 'c', 'ילד', 'I-י', 'Simple Past'],
            ['19', 'נָתְנָה', '3', 's', 'f', 'נתן', 'I-נ', 'Simple Past'],
            ['20', 'תַּמּוּ', '3', 'p', 'c', 'תמם', 'Geminate', 'Simple Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_e, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_e)


def build_ch14_passage_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch14PassageExercise,
        'Chapter 14 — Passage Exercise: Qal Perfect Weak Verbs',
        'BBH Chapter 14',
        ['hebrew', 'bbh', 'ch14', 'exercises', 'ch14-passage-exercise'],
        'ch14-passage-exercise.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------


class Ch14WeakFormIdExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each form, give: (a) Weak Class, (b) Person, (c) Number, '
            '(d) Gender, (e) Root (3ms lexical form).'
        )
        hdrs = ['#', 'Form', 'Weak Class', 'Person', 'Number', 'Gender', 'Root']
        cr = [0.05, 0.14, 0.15, 0.09, 0.09, 0.09, 0.39]
        hc = [1]
        groups = [
            ('Group 1: III-ה (1–5)', [
                ['1', 'עָשָׂה', '', '', '', '', ''],
                ['2', 'רָאִיתָ', '', '', '', '', ''],
                ['3', 'גָּלְתָה', '', '', '', '', ''],
                ['4', 'עָשׂוּ', '', '', '', '', ''],
                ['5', 'עֲלִיתֶם', '', '', '', '', ''],
            ], [
                ['1', 'עָשָׂה', 'III-ה', '3', 's', 'm', 'עשה'],
                ['2', 'רָאִיתָ', 'III-ה', '2', 's', 'm', 'ראה'],
                ['3', 'גָּלְתָה', 'III-ה', '3', 's', 'f', 'גלה'],
                ['4', 'עָשׂוּ', 'III-ה', '3', 'p', 'c', 'עשה'],
                ['5', 'עֲלִיתֶם', 'III-ה', '2', 'p', 'm', 'עלה'],
            ]),
            ('Group 2: III-א (6–10)', [
                ['6', 'מָצָא', '', '', '', '', ''],
                ['7', 'קָרְאָה', '', '', '', '', ''],
                ['8', 'חָטָאתִי', '', '', '', '', ''],
                ['9', 'מָצְאוּ', '', '', '', '', ''],
                ['10', 'מְצָאתֶם', '', '', '', '', ''],
            ], [
                ['6', 'מָצָא', 'III-א', '3', 's', 'm', 'מצא'],
                ['7', 'קָרְאָה', 'III-א', '3', 's', 'f', 'קרא'],
                ['8', 'חָטָאתִי', 'III-א', '1', 's', 'c', 'חטא'],
                ['9', 'מָצְאוּ', 'III-א', '3', 'p', 'c', 'מצא'],
                ['10', 'מְצָאתֶם', 'III-א', '2', 'p', 'm', 'מצא'],
            ]),
            ('Group 3: III-gutt. Lamed-Guttural (11–15)', [
                ['11', 'שָׁמַע', '', '', '', '', ''],
                ['12', 'שָׁלַח', '', '', '', '', ''],
                ['13', 'שָׁמַעְתִּי', '', '', '', '', ''],
                ['14', 'שָׁמְעוּ', '', '', '', '', ''],
                ['15', 'שְׁלַחְתֶּם', '', '', '', '', ''],
            ], [
                ['11', 'שָׁמַע', 'III-gutt.', '3', 's', 'm', 'שמע'],
                ['12', 'שָׁלַח', 'III-gutt.', '3', 's', 'm', 'שלח'],
                ['13', 'שָׁמַעְתִּי', 'III-gutt.', '1', 's', 'c', 'שמע'],
                ['14', 'שָׁמְעוּ', 'III-gutt.', '3', 'p', 'c', 'שמע'],
                ['15', 'שְׁלַחְתֶּם', 'III-gutt.', '2', 'p', 'm', 'שלח'],
            ]),
            ('Group 4: I-guttural / Pe-Guttural (16–20)', [
                ['16', 'אָמַר', '', '', '', '', ''],
                ['17', 'עָמַדְתָּ', '', '', '', '', ''],
                ['18', 'אָמַרְתִּי', '', '', '', '', ''],
                ['19', 'אֲמַרְתֶּם', '', '', '', '', ''],
                ['20', 'עָמְדוּ', '', '', '', '', ''],
            ], [
                ['16', 'אָמַר', 'I-gutt.', '3', 's', 'm', 'אמר'],
                ['17', 'עָמַדְתָּ', 'I-gutt.', '2', 's', 'm', 'עמד'],
                ['18', 'אָמַרְתִּי', 'I-gutt.', '1', 's', 'c', 'אמר'],
                ['19', 'אֲמַרְתֶּם', 'I-gutt.', '2', 'p', 'm', 'אמר'],
                ['20', 'עָמְדוּ', 'I-gutt.', '3', 'p', 'c', 'עמד'],
            ]),
            ('Group 5: I-נ and I-י (21–25)', [
                ['21', 'נָתַן', '', '', '', '', ''],
                ['22', 'נָתְנָה', '', '', '', '', ''],
                ['23', 'יָלַדְתָּ', '', '', '', '', ''],
                ['24', 'יָלְדוּ', '', '', '', '', ''],
                ['25', 'יָדַעְתִּי', '', '', '', '', ''],
            ], [
                ['21', 'נָתַן', 'I-נ', '3', 's', 'm', 'נתן'],
                ['22', 'נָתְנָה', 'I-נ', '3', 's', 'f', 'נתן'],
                ['23', 'יָלַדְתָּ', 'I-י', '2', 's', 'm', 'ילד'],
                ['24', 'יָלְדוּ', 'I-י', '3', 'p', 'c', 'ילד'],
                ['25', 'יָדַעְתִּי', 'I-י', '1', 's', 'c', 'ידע'],
            ]),
            ('Group 6: Biconsonantal (26–30)', [
                ['26', 'קָם', '', '', '', '', ''],
                ['27', 'שָׁבָה', '', '', '', '', ''],
                ['28', 'בָּאתָ', '', '', '', '', ''],
                ['29', 'קָמוּ', '', '', '', '', ''],
                ['30', 'שַׁבְתֶּם', '', '', '', '', ''],
            ], [
                ['26', 'קָם', 'Biconsonantal', '3', 's', 'm', 'קום'],
                ['27', 'שָׁבָה', 'Biconsonantal', '3', 's', 'f', 'שוב'],
                ['28', 'בָּאתָ', 'Biconsonantal', '2', 's', 'm', 'בוא'],
                ['29', 'קָמוּ', 'Biconsonantal', '3', 'p', 'c', 'קום'],
                ['30', 'שַׁבְתֶּם', 'Biconsonantal', '2', 'p', 'm', 'שוב'],
            ]),
            ('Group 7: Geminate (31–35)', [
                ['31', 'סָבַב', '', '', '', '', ''],
                ['32', 'תַּמּוּ', '', '', '', '', ''],
                ['33', 'סַבֹּתָ', '', '', '', '', ''],
                ['34', 'תָּם', '', '', '', '', ''],
                ['35', 'סָבָּה', '', '', '', '', ''],
            ], [
                ['31', 'סָבַב', 'Geminate', '3', 's', 'm', 'סבב'],
                ['32', 'תַּמּוּ', 'Geminate', '3', 'p', 'c', 'תמם'],
                ['33', 'סַבֹּתָ', 'Geminate', '2', 's', 'm', 'סבב'],
                ['34', 'תָּם', 'Geminate', '3', 's', 'm', 'תמם'],
                ['35', 'סָבָּה', 'Geminate', '3', 's', 'f', 'סבב'],
            ]),
        ]
        for heading, rows, ans in groups:
            self.add_section_heading(heading)
            self.add_generic_table(headers=hdrs, rows=rows, col_ratios=cr, heb_cols=hc,
                                   show_answers=True, answer_rows=ans)

        self.add_section_heading('Part B — Mixed (36–40)')
        rows_b = [
            ['36', 'הָיִיתִי', '', '', '', '', ''],
            ['37', 'נָפְלָה', '', '', '', '', ''],
            ['38', 'מָת', '', '', '', '', ''],
            ['39', 'בָּאנוּ', '', '', '', '', ''],
            ['40', 'שָׁמְעָה', '', '', '', '', ''],
        ]
        ans_b = [
            ['36', 'הָיִיתִי', 'III-ה', '1', 's', 'c', 'היה'],
            ['37', 'נָפְלָה', 'I-נ', '3', 's', 'f', 'נפל'],
            ['38', 'מָת', 'Biconsonantal', '3', 's', 'm', 'מות'],
            ['39', 'בָּאנוּ', 'Biconsonantal', '1', 'p', 'c', 'בוא'],
            ['40', 'שָׁמְעָה', 'III-gutt.', '3', 's', 'f', 'שמע'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)


def build_ch14_weak_form_id(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch14WeakFormIdExercise,
        'Chapter 14 — Weak-Form Identification Drill: Qal Perfect Weak Verbs',
        'BBH Chapter 14',
        ['hebrew', 'bbh', 'ch14', 'exercises', 'ch14-weak-form-id'],
        'ch14-weak-form-id.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------


class Ch15ParsingDrillExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each form, give: (a) Person, (b) Number, (c) Gender, '
            '(d) Root (3ms lexical form).\n'
            'Part C: also identify whether the form is a Jussive or Cohortative.'
        )
        hdrs_ab = ['#', 'Form', 'Person', 'Number', 'Gender', 'Root']
        cr_ab = [0.05, 0.16, 0.10, 0.10, 0.10, 0.49]
        hc = [1]

        self.add_section_heading('Part A — A-Class (Holem): Clear Prefix Pattern (1–10)')
        rows_a = [
            ['1', 'יִשְׁמֹר', '', '', '', ''],
            ['2', 'תִּכְתְּבוּ', '', '', '', ''],
            ['3', 'נִפְקֹד', '', '', '', ''],
            ['4', 'תִּלְמְדִי', '', '', '', ''],
            ['5', 'יִזְכְּרוּ', '', '', '', ''],
            ['6', 'אֶשְׁמֹר', '', '', '', ''],
            ['7', 'תִּמְשֹׁל', '', '', '', ''],
            ['8', 'יִכְתְּבוּ', '', '', '', ''],
            ['9', 'תִּשְׁמֹרְנָה', '', '', '', ''],
            ['10', 'אֶבְחַר', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'יִשְׁמֹר', '3', 's', 'm', 'שמר'],
            ['2', 'תִּכְתְּבוּ', '2', 'p', 'm', 'כתב'],
            ['3', 'נִפְקֹד', '1', 'p', 'c', 'פקד'],
            ['4', 'תִּלְמְדִי', '2', 's', 'f', 'למד'],
            ['5', 'יִזְכְּרוּ', '3', 'p', 'm', 'זכר'],
            ['6', 'אֶשְׁמֹר', '1', 's', 'c', 'שמר'],
            ['7', 'תִּמְשֹׁל', '3/2', 's', 'f/m', 'משל'],
            ['8', 'יִכְתְּבוּ', '3', 'p', 'm', 'כתב'],
            ['9', 'תִּשְׁמֹרְנָה', '3/2', 'p', 'f', 'שמר'],
            ['10', 'אֶבְחַר', '1', 's', 'c', 'בחר'],
        ]
        self.add_generic_table(headers=hdrs_ab, rows=rows_a, col_ratios=cr_ab, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Part B — B-Class (Patach) and Disambiguation (11–20)')
        rows_b = [
            ['11', 'יִשְׁמַע', '', '', '', ''],
            ['12', 'תִּשְׁמַע', '', '', '', ''],
            ['13', 'תִּשְׁמְעִי', '', '', '', ''],
            ['14', 'יִכְבַּד', '', '', '', ''],
            ['15', 'תִּגְדַּל', '', '', '', ''],
            ['16', 'יִכְבְּדוּ', '', '', '', ''],
            ['17', 'תִּשְׁמַעְנָה', '', '', '', ''],
            ['18', 'אֶשְׁמַע', '', '', '', ''],
            ['19', 'נִשְׁמַע', '', '', '', ''],
            ['20', 'יִגְדַּל', '', '', '', ''],
        ]
        ans_b = [
            ['11', 'יִשְׁמַע', '3', 's', 'm', 'שמע'],
            ['12', 'תִּשְׁמַע', '3/2', 's', 'f/m', 'שמע'],
            ['13', 'תִּשְׁמְעִי', '2', 's', 'f', 'שמע'],
            ['14', 'יִכְבַּד', '3', 's', 'm', 'כבד'],
            ['15', 'תִּגְדַּל', '3/2', 's', 'f/m', 'גדל'],
            ['16', 'יִכְבְּדוּ', '3', 'p', 'm', 'כבד'],
            ['17', 'תִּשְׁמַעְנָה', '3/2', 'p', 'f', 'שמע'],
            ['18', 'אֶשְׁמַע', '1', 's', 'c', 'שמע'],
            ['19', 'נִשְׁמַע', '1', 'p', 'c', 'שמע'],
            ['20', 'יִגְדַּל', '3', 's', 'm', 'גדל'],
        ]
        self.add_generic_table(
            headers=['#', 'Form', 'Person', 'Number', 'Gender', 'Root', 'Notes'],
            rows=[[r[0], r[1], r[2], r[3], r[4], r[5], ''] for r in rows_b],
            col_ratios=[0.05, 0.14, 0.09, 0.09, 0.09, 0.16, 0.38],
            heb_cols=hc,
            show_answers=True,
            answer_rows=[[r[0], r[1], r[2], r[3], r[4], r[5], ''] for r in ans_b],
        )

        self.add_section_heading('Part C — Jussive and Cohortative Forms (21–25)')
        rows_c = [
            ['21', 'יִשְׁמְרָה', '', '', '', '', ''],
            ['22', 'נִשְׁמְרָה', '', '', '', '', ''],
            ['23', 'יִשְׁמֹר', '', '', '', '', ''],
            ['24', 'תִּשְׁמֹר', '', '', '', '', ''],
            ['25', 'אֶשְׁמְרָה', '', '', '', '', ''],
        ]
        ans_c = [
            ['21', 'יִשְׁמְרָה', '3', 's', 'm', 'שמר', 'Jussive/Energic'],
            ['22', 'נִשְׁמְרָה', '1', 'p', 'c', 'שמר', 'Cohortative'],
            ['23', 'יִשְׁמֹר', '3', 's', 'm', 'שמר', 'Jussive (= Imperfect for strong)'],
            ['24', 'תִּשְׁמֹר', '3/2', 's', 'f/m', 'שמר', 'Jussive (= Imperfect for strong)'],
            ['25', 'אֶשְׁמְרָה', '1', 's', 'c', 'שמר', 'Cohortative'],
        ]
        self.add_generic_table(
            headers=['#', 'Form', 'Person', 'Number', 'Gender', 'Root', 'Form Type'],
            rows=rows_c,
            col_ratios=[0.05, 0.14, 0.09, 0.09, 0.09, 0.14, 0.40],
            heb_cols=hc,
            show_answers=True,
            answer_rows=ans_c,
        )


def build_ch15_parsing_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch15ParsingDrillExercise,
        'Chapter 15 — Parsing Drill: Qal Imperfect Strong Verbs',
        'BBH Chapter 15',
        ['hebrew', 'bbh', 'ch15', 'exercises', 'ch15-parsing-drill'],
        'ch15-parsing-drill.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------


class Ch15PassageExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Parse each highlighted Qal Imperfect form. Give: '
            '(a) Person, (b) Number, (c) Gender, (d) Root (3ms lexical form), '
            '(e) Usage Type.'
        )
        hdrs = ['#', 'Form', 'Person', 'Number', 'Gender', 'Root', 'Usage Type']
        cr = [0.05, 0.16, 0.09, 0.09, 0.09, 0.14, 0.38]
        hc = [1]

        self.add_section_heading('Passage A — Exodus 3:1–12 (1–4)')
        rows_a = [
            ['1', 'אֵלֵךְ', '', '', '', '', ''],
            ['2', 'אֶרְאֶה', '', '', '', '', ''],
            ['3', 'תִקְרַב', '', '', '', '', ''],
            ['4', 'אֶהְיֶה', '', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'אֵלֵךְ', '1', 's', 'c', 'הלך', 'Cohortative'],
            ['2', 'אֶרְאֶה', '1', 's', 'c', 'ראה', 'Cohortative'],
            ['3', 'תִקְרַב', '2', 's', 'm', 'קרב', 'Prohibition'],
            ['4', 'אֶהְיֶה', '1', 's', 'c', 'היה', 'Simple Future'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_a, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Passage B — Exodus 3:13–20 (5–8)')
        rows_b = [
            ['5', 'אֵלֵךְ', '', '', '', '', ''],
            ['6', 'אוֹצִיא', '', '', '', '', ''],
            ['7', 'אֶשְׁלַח', '', '', '', '', ''],
            ['8', 'יִשְׁמְעוּ', '', '', '', '', ''],
        ]
        ans_b = [
            ['5', 'אֵלֵךְ', '1', 's', 'c', 'הלך', 'Modal'],
            ['6', 'אוֹצִיא', '1', 's', 'c', 'יצא', 'Modal/Future (Hiphil)'],
            ['7', 'אֶשְׁלַח', '1', 's', 'c', 'שלח', 'Simple Future'],
            ['8', 'יִשְׁמְעוּ', '3', 'p', 'm', 'שמע', 'Simple Future'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Passage C — Exodus 20:13–17, Decalogue (9–13)')
        rows_c = [
            ['9', 'תִּרְצָח', '', '', '', '', ''],
            ['10', 'תִנְאָף', '', '', '', '', ''],
            ['11', 'תִּגְנֹב', '', '', '', '', ''],
            ['12', 'תַעֲנֶה', '', '', '', '', ''],
            ['13', 'תַחְמֹד', '', '', '', '', ''],
        ]
        ans_c = [
            ['9', 'תִּרְצָח', '2', 's', 'm', 'רצח', 'Prohibition (לֹא)'],
            ['10', 'תִנְאָף', '2', 's', 'm', 'נאף', 'Prohibition (לֹא)'],
            ['11', 'תִּגְנֹב', '2', 's', 'm', 'גנב', 'Prohibition (לֹא)'],
            ['12', 'תַעֲנֶה', '2', 's', 'm', 'ענה', 'Prohibition (לֹא)'],
            ['13', 'תַחְמֹד', '2', 's', 'm', 'חמד', 'Prohibition (לֹא)'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_c, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_c)

        self.add_section_heading('Passage D — Genesis 1:3, 9, 11 (14–15)')
        rows_d = [
            ['14', 'יְהִי', '', '', '', '', ''],
            ['15', 'יִקָּווּ', '', '', '', '', ''],
        ]
        ans_d = [
            ['14', 'יְהִי', '3', 's', 'm', 'היה', 'Jussive'],
            ['15', 'יִקָּווּ', '3', 'p', 'm', 'קוה', 'Jussive/Command (Niphal)'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_d, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_d)


def build_ch15_passage_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch15PassageExercise,
        'Chapter 15 — Passage Exercise: Qal Imperfect Strong Verbs',
        'BBH Chapter 15',
        ['hebrew', 'bbh', 'ch15', 'exercises', 'ch15-passage-exercise'],
        'ch15-passage-exercise.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Ch16–Ch18 builders
# ---------------------------------------------------------------------------


class Ch16PassageExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'Parse each highlighted verb. Give: '
            '(a) Person, (b) Number, (c) Gender, (d) Root (3ms lexical form), '
            '(e) Weak Class, (f) Form Type (Imperfect / Wayyiqtol / Jussive), '
            '(g) Usage Type.'
        )
        hdrs = ['#', 'Form', 'Person', 'Number', 'Gender', 'Root', 'Weak Class', 'Form Type', 'Usage Type']
        cr = [0.05, 0.12, 0.07, 0.07, 0.07, 0.11, 0.12, 0.10, 0.29]
        hc = [1]

        self.add_section_heading('Passage A — III-ה and III-א (Gen 1:3–11; Gen 3:1) (1–4)')
        rows_a = [
            ['1', 'יְהִי', '', '', '', '', '', '', ''],
            ['2', 'יַעֲשֶׂה', '', '', '', '', '', '', ''],
            ['3', 'יִהְיוּ', '', '', '', '', '', '', ''],
            ['4', 'תֹּאכְלוּ', '', '', '', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'יְהִי', '3', 's', 'm', 'היה', 'III-ה', 'Jussive', 'Volitional'],
            ['2', 'יַעֲשֶׂה', '3', 's', 'm', 'עשה', 'III-ה + I-gutt.', 'Jussive', 'Volitional'],
            ['3', 'יִהְיוּ', '3', 'p', 'm', 'היה', 'III-ה', 'Imperfect', 'Jussive/Volitional'],
            ['4', 'תֹּאכְלוּ', '2', 'p', 'm', 'אכל', 'I-gutt. (א)', 'Imperfect', 'Prohibition (לֹא)'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_a, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Passage B — III-Guttural and I-Guttural (Gen 3–4; Exo 20) (5–8)')
        rows_b = [
            ['5', 'יֹאמַר', '', '', '', '', '', '', ''],
            ['6', 'וַיִּשְׁמַע', '', '', '', '', '', '', ''],
            ['7', 'תַּחְמֹד', '', '', '', '', '', '', ''],
            ['8', 'וַיַּעֲמֹד', '', '', '', '', '', '', ''],
        ]
        ans_b = [
            ['5', 'יֹאמַר', '3', 's', 'm', 'אמר', 'I-gutt. (א)', 'Imperfect', 'Simple Future'],
            ['6', 'וַיִּשְׁמַע', '3', 's', 'm', 'שמע', 'III-gutt. (ע)', 'Wayyiqtol', 'Sequential Past'],
            ['7', 'תַּחְמֹד', '2', 's', 'm', 'חמד', 'I-gutt. (ח)', 'Imperfect', 'Prohibition (לֹא)'],
            ['8', 'וַיַּעֲמֹד', '3', 's', 'm', 'עמד', 'I-gutt. (ע)', 'Wayyiqtol', 'Sequential Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Passage C — I-נ and I-י (Gen 3–4; 9; Num 10) (9–12)')
        rows_c = [
            ['9', 'וַיִּתֵּן', '', '', '', '', '', '', ''],
            ['10', 'וַיֵּדַע', '', '', '', '', '', '', ''],
            ['11', 'יִתֵּן', '', '', '', '', '', '', ''],
            ['12', 'וַיֵּצֵא', '', '', '', '', '', '', ''],
        ]
        ans_c = [
            ['9', 'וַיִּתֵּן', '3', 's', 'm', 'נתן', 'I-נ', 'Wayyiqtol', 'Sequential Past'],
            ['10', 'וַיֵּדַע', '3', 's', 'm', 'ידע', 'I-י', 'Wayyiqtol', 'Sequential Past'],
            ['11', 'יִתֵּן', '3', 's', 'm', 'נתן', 'I-נ', 'Imperfect', 'Simple Future'],
            ['12', 'וַיֵּצֵא', '3', 's', 'm', 'יצא', 'I-י', 'Wayyiqtol', 'Sequential Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_c, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_c)

        self.add_section_heading('Passage D — Biconsonantal and Geminate (Gen 19–22) (13–16)')
        rows_d = [
            ['13', 'וַיָּבֹאוּ', '', '', '', '', '', '', ''],
            ['14', 'וַיָּקׇם', '', '', '', '', '', '', ''],
            ['15', 'יָשׁוּב', '', '', '', '', '', '', ''],
            ['16', 'וַיָּסׇּב', '', '', '', '', '', '', ''],
        ]
        ans_d = [
            ['13', 'וַיָּבֹאוּ', '3', 'p', 'm', 'בוא', 'Biconsonantal', 'Wayyiqtol', 'Sequential Past'],
            ['14', 'וַיָּקׇם', '3', 's', 'm', 'קום', 'Biconsonantal', 'Wayyiqtol', 'Sequential Past'],
            ['15', 'יָשׁוּב', '3', 's', 'm', 'שוב', 'Biconsonantal', 'Imperfect', 'Simple Future'],
            ['16', 'וַיָּסׇּב', '3', 's', 'm', 'סבב', 'Geminate', 'Wayyiqtol', 'Sequential Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_d, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_d)


def build_ch16_passage_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch16PassageExercise,
        'Chapter 16 — Passage Exercise: Qal Imperfect Weak Verbs',
        'BBH Chapter 16',
        ['hebrew', 'bbh', 'ch16', 'exercises', 'ch16-passage-exercise'],
        'ch16-passage-exercise.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------


class Ch16WeakFormIdExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each form, identify: (a) Weak Class, (b) Person, (c) Number, '
            '(d) Gender, (e) Root.\n'
            'Part A: forms are grouped by class. Part B: forms are mixed — identify the class first.'
        )
        hdrs = ['#', 'Form', 'Weak Class', 'Person', 'Number', 'Gender', 'Root']
        cr = [0.05, 0.14, 0.15, 0.09, 0.09, 0.09, 0.39]
        hc = [1]
        groups = [
            ('Group 1: III-ה (Lamed-He) (1–5)', [
                ['1', 'יִבְנֶה', '', '', '', '', ''],
                ['2', 'תַּעֲשֶׂה', '', '', '', '', ''],
                ['3', 'יִהְיֶה', '', '', '', '', ''],
                ['4', 'תִּרְאֶה', '', '', '', '', ''],
                ['5', 'יִבֶּן', '', '', '', '', ''],
            ], [
                ['1', 'יִבְנֶה', 'III-ה', '3', 's', 'm', 'בנה'],
                ['2', 'תַּעֲשֶׂה', 'III-ה', '3/2', 's', 'f/m', 'עשה'],
                ['3', 'יִהְיֶה', 'III-ה', '3', 's', 'm', 'היה'],
                ['4', 'תִּרְאֶה', 'III-ה', '3/2', 's', 'f/m', 'ראה'],
                ['5', 'יִבֶּן', 'III-ה', '3', 's', 'm', 'בנה'],
            ]),
            ('Group 2: III-א (Lamed-Aleph) (6–10)', [
                ['6', 'יִמְצָא', '', '', '', '', ''],
                ['7', 'תִּקְרָא', '', '', '', '', ''],
                ['8', 'אֶמְצָא', '', '', '', '', ''],
                ['9', 'יִמְצְאוּ', '', '', '', '', ''],
                ['10', 'נִקְרָא', '', '', '', '', ''],
            ], [
                ['6', 'יִמְצָא', 'III-א', '3', 's', 'm', 'מצא'],
                ['7', 'תִּקְרָא', 'III-א', '3/2', 's', 'f/m', 'קרא'],
                ['8', 'אֶמְצָא', 'III-א', '1', 's', 'c', 'מצא'],
                ['9', 'יִמְצְאוּ', 'III-א', '3', 'p', 'm', 'מצא'],
                ['10', 'נִקְרָא', 'III-א', '1', 'p', 'c', 'קרא'],
            ]),
            ('Group 3: III-gutt. Lamed-Guttural (11–15)', [
                ['11', 'יִשְׁלַח', '', '', '', '', ''],
                ['12', 'תִּשְׁמַע', '', '', '', '', ''],
                ['13', 'וַיִּשְׁמַע', '', '', '', '', ''],
                ['14', 'יִשְׁלְחוּ', '', '', '', '', ''],
                ['15', 'אֶשְׁמַע', '', '', '', '', ''],
            ], [
                ['11', 'יִשְׁלַח', 'III-gutt.', '3', 's', 'm', 'שלח'],
                ['12', 'תִּשְׁמַע', 'III-gutt.', '3/2', 's', 'f/m', 'שמע'],
                ['13', 'וַיִּשְׁמַע', 'III-gutt.', '3', 's', 'm', 'שמע'],
                ['14', 'יִשְׁלְחוּ', 'III-gutt.', '3', 'p', 'm', 'שלח'],
                ['15', 'אֶשְׁמַע', 'III-gutt.', '1', 's', 'c', 'שמע'],
            ]),
            ('Group 4: I-Guttural (Pe-Guttural) (16–20)', [
                ['16', 'יַעֲמֹד', '', '', '', '', ''],
                ['17', 'תַּחֲלֹם', '', '', '', '', ''],
                ['18', 'יֹאמַר', '', '', '', '', ''],
                ['19', 'תַּעַמְדוּ', '', '', '', '', ''],
                ['20', 'נַעֲמֹד', '', '', '', '', ''],
            ], [
                ['16', 'יַעֲמֹד', 'I-gutt.', '3', 's', 'm', 'עמד'],
                ['17', 'תַּחֲלֹם', 'I-gutt.', '3/2', 's', 'f/m', 'חלם'],
                ['18', 'יֹאמַר', 'I-gutt. (א)', '3', 's', 'm', 'אמר'],
                ['19', 'תַּעַמְדוּ', 'I-gutt.', '2', 'p', 'm', 'עמד'],
                ['20', 'נַעֲמֹד', 'I-gutt.', '1', 'p', 'c', 'עמד'],
            ]),
            ('Group 5: I-נ (Pe-Nun) (21–25)', [
                ['21', 'יִתֵּן', '', '', '', '', ''],
                ['22', 'תִּתֵּן', '', '', '', '', ''],
                ['23', 'וַיִּתֵּן', '', '', '', '', ''],
                ['24', 'יִפֹּל', '', '', '', '', ''],
                ['25', 'תִּתְּנוּ', '', '', '', '', ''],
            ], [
                ['21', 'יִתֵּן', 'I-נ', '3', 's', 'm', 'נתן'],
                ['22', 'תִּתֵּן', 'I-נ', '3/2', 's', 'f/m', 'נתן'],
                ['23', 'וַיִּתֵּן', 'I-נ', '3', 's', 'm', 'נתן'],
                ['24', 'יִפֹּל', 'I-נ', '3', 's', 'm', 'נפל'],
                ['25', 'תִּתְּנוּ', 'I-נ', '2', 'p', 'm', 'נתן'],
            ]),
            ('Group 6: I-י (Pe-Yod) (26–30)', [
                ['26', 'יֵדַע', '', '', '', '', ''],
                ['27', 'תֵּשֵׁב', '', '', '', '', ''],
                ['28', 'וַיֵּלֶד', '', '', '', '', ''],
                ['29', 'יֵצֵא', '', '', '', '', ''],
                ['30', 'אֵלֵד', '', '', '', '', ''],
            ], [
                ['26', 'יֵדַע', 'I-י', '3', 's', 'm', 'ידע'],
                ['27', 'תֵּשֵׁב', 'I-י', '3/2', 's', 'f/m', 'ישב'],
                ['28', 'וַיֵּלֶד', 'I-י', '3', 's', 'm', 'ילד'],
                ['29', 'יֵצֵא', 'I-י', '3', 's', 'm', 'יצא'],
                ['30', 'אֵלֵד', 'I-י', '1', 's', 'c', 'ילד'],
            ]),
            ('Group 7: Biconsonantal (II-י/ו) (31–35)', [
                ['31', 'יָקוּם', '', '', '', '', ''],
                ['32', 'תָּבוֹא', '', '', '', '', ''],
                ['33', 'וַיָּבֹא', '', '', '', '', ''],
                ['34', 'יָמוּת', '', '', '', '', ''],
                ['35', 'וַיָּקׇם', '', '', '', '', ''],
            ], [
                ['31', 'יָקוּם', 'Biconsonantal', '3', 's', 'm', 'קום'],
                ['32', 'תָּבוֹא', 'Biconsonantal', '3/2', 's', 'f/m', 'בוא'],
                ['33', 'וַיָּבֹא', 'Biconsonantal', '3', 's', 'm', 'בוא'],
                ['34', 'יָמוּת', 'Biconsonantal', '3', 's', 'm', 'מות'],
                ['35', 'וַיָּקׇם', 'Biconsonantal', '3', 's', 'm', 'קום'],
            ]),
            ('Group 8: Geminate (Ayin-Doubled) (36–40)', [
                ['36', 'יָסֹב', '', '', '', '', ''],
                ['37', 'יִסֹּב', '', '', '', '', ''],
                ['38', 'וַיָּסׇּב', '', '', '', '', ''],
                ['39', 'תָּסֹב', '', '', '', '', ''],
                ['40', 'יִסֹּבּוּ', '', '', '', '', ''],
            ], [
                ['36', 'יָסֹב', 'Geminate', '3', 's', 'm', 'סבב'],
                ['37', 'יִסֹּב', 'Geminate', '3', 's', 'm', 'סבב'],
                ['38', 'וַיָּסׇּב', 'Geminate', '3', 's', 'm', 'סבב'],
                ['39', 'תָּסֹב', 'Geminate', '3/2', 's', 'f/m', 'סבב'],
                ['40', 'יִסֹּבּוּ', 'Geminate', '3', 'p', 'm', 'סבב'],
            ]),
        ]
        for heading, rows, ans in groups:
            self.add_section_heading(heading)
            self.add_generic_table(headers=hdrs, rows=rows, col_ratios=cr, heb_cols=hc,
                                   show_answers=True, answer_rows=ans)

        self.add_section_heading('Part B — Mixed Forms (41–50)')
        rows_b = [
            ['41', 'וַיָּקׇם', '', '', '', '', ''],
            ['42', 'יִבְנֶה', '', '', '', '', ''],
            ['43', 'יִתֵּן', '', '', '', '', ''],
            ['44', 'יַעֲשֶׂה', '', '', '', '', ''],
            ['45', 'תֵּדַע', '', '', '', '', ''],
            ['46', 'וַיִּשְׁמַע', '', '', '', '', ''],
            ['47', 'יִמְצָא', '', '', '', '', ''],
            ['48', 'וַיָּבֹאוּ', '', '', '', '', ''],
            ['49', 'תִּתֵּן', '', '', '', '', ''],
            ['50', 'יֵצֵא', '', '', '', '', ''],
        ]
        ans_b = [
            ['41', 'וַיָּקׇם', 'Biconsonantal', '3', 's', 'm', 'קום'],
            ['42', 'יִבְנֶה', 'III-ה', '3', 's', 'm', 'בנה'],
            ['43', 'יִתֵּן', 'I-נ', '3', 's', 'm', 'נתן'],
            ['44', 'יַעֲשֶׂה', 'III-ה', '3', 's', 'm', 'עשה'],
            ['45', 'תֵּדַע', 'I-י', '3/2', 's', 'f/m', 'ידע'],
            ['46', 'וַיִּשְׁמַע', 'III-gutt.', '3', 's', 'm', 'שמע'],
            ['47', 'יִמְצָא', 'III-א', '3', 's', 'm', 'מצא'],
            ['48', 'וַיָּבֹאוּ', 'Biconsonantal', '3', 'p', 'm', 'בוא'],
            ['49', 'תִּתֵּן', 'I-נ', '3/2', 's', 'f/m', 'נתן'],
            ['50', 'יֵצֵא', 'I-י', '3', 's', 'm', 'יצא'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)


def build_ch16_weak_form_id(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch16WeakFormIdExercise,
        'Chapter 16 — Weak Form ID Drill: Qal Imperfect Weak Verbs',
        'BBH Chapter 16',
        ['hebrew', 'bbh', 'ch16', 'exercises', 'ch16-weak-form-id'],
        'ch16-weak-form-id.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------


class Ch17ParsingDrillExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each form, give: (a) Form Type (Wayyiqtol / Weqatal / Imperfect / Perfect), '
            '(b) Person, (c) Number, (d) Gender, (e) Root (3ms lexical form).'
        )
        hdrs_a = ['#', 'Form', 'Form Type', 'Person', 'Number', 'Gender', 'Root']
        cr_a = [0.05, 0.14, 0.14, 0.09, 0.09, 0.09, 0.40]
        hdrs_b = ['#', 'Form', 'Form Type', 'Person', 'Number', 'Gender', 'Root', 'Weak Class']
        cr_b = [0.05, 0.13, 0.12, 0.08, 0.08, 0.08, 0.14, 0.32]
        hc = [1]

        self.add_section_heading('Part A — Wayyiqtol: Strong and Common Weak Roots (1–10)')
        rows_a = [
            ['1', 'וַיֹּאמֶר', '', '', '', '', ''],
            ['2', 'וַתֹּאמֶר', '', '', '', '', ''],
            ['3', 'וַיֵּלֶךְ', '', '', '', '', ''],
            ['4', 'וַיִּקְטֹל', '', '', '', '', ''],
            ['5', 'וַיִּכְתְּבוּ', '', '', '', '', ''],
            ['6', 'וַתִּשְׁמֹרְנָה', '', '', '', '', ''],
            ['7', 'וָאֶקְטֹל', '', '', '', '', ''],
            ['8', 'וַנִּקְטֹל', '', '', '', '', ''],
            ['9', 'וַיִּתֵּן', '', '', '', '', ''],
            ['10', 'וַיָּבֹא', '', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'וַיֹּאמֶר', 'Wayyiqtol', '3', 's', 'm', 'אמר'],
            ['2', 'וַתֹּאמֶר', 'Wayyiqtol', '3', 's', 'f', 'אמר'],
            ['3', 'וַיֵּלֶךְ', 'Wayyiqtol', '3', 's', 'm', 'הלך'],
            ['4', 'וַיִּקְטֹל', 'Wayyiqtol', '3', 's', 'm', 'קטל'],
            ['5', 'וַיִּכְתְּבוּ', 'Wayyiqtol', '3', 'p', 'm', 'כתב'],
            ['6', 'וַתִּשְׁמֹרְנָה', 'Wayyiqtol', '3/2', 'p', 'f', 'שמר'],
            ['7', 'וָאֶקְטֹל', 'Wayyiqtol', '1', 's', 'c', 'קטל'],
            ['8', 'וַנִּקְטֹל', 'Wayyiqtol', '1', 'p', 'c', 'קטל'],
            ['9', 'וַיִּתֵּן', 'Wayyiqtol', '3', 's', 'm', 'נתן'],
            ['10', 'וַיָּבֹא', 'Wayyiqtol', '3', 's', 'm', 'בוא'],
        ]
        self.add_generic_table(headers=hdrs_a, rows=rows_a, col_ratios=cr_a, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Part B — Wayyiqtol: Weak Roots (11–20)')
        rows_b = [
            ['11', 'וַיַּרְא', '', '', '', '', '', ''],
            ['12', 'וַיְהִי', '', '', '', '', '', ''],
            ['13', 'וַיַּעַשׂ', '', '', '', '', '', ''],
            ['14', 'וַיָּקׇם', '', '', '', '', '', ''],
            ['15', 'וַיָּבֹאוּ', '', '', '', '', '', ''],
            ['16', 'וַיָּסׇּב', '', '', '', '', '', ''],
            ['17', 'וַיֵּדַע', '', '', '', '', '', ''],
            ['18', 'וַיֵּצֵא', '', '', '', '', '', ''],
            ['19', 'וַיִּבֶן', '', '', '', '', '', ''],
            ['20', 'וַיָּשׇׁב', '', '', '', '', '', ''],
        ]
        ans_b = [
            ['11', 'וַיַּרְא', 'Wayyiqtol', '3', 's', 'm', 'ראה', 'III-ה'],
            ['12', 'וַיְהִי', 'Wayyiqtol', '3', 's', 'm', 'היה', 'III-ה'],
            ['13', 'וַיַּעַשׂ', 'Wayyiqtol', '3', 's', 'm', 'עשה', 'III-ה + I-gutt.'],
            ['14', 'וַיָּקׇם', 'Wayyiqtol', '3', 's', 'm', 'קום', 'Biconsonantal'],
            ['15', 'וַיָּבֹאוּ', 'Wayyiqtol', '3', 'p', 'm', 'בוא', 'Biconsonantal'],
            ['16', 'וַיָּסׇּב', 'Wayyiqtol', '3', 's', 'm', 'סבב', 'Geminate'],
            ['17', 'וַיֵּדַע', 'Wayyiqtol', '3', 's', 'm', 'ידע', 'I-י'],
            ['18', 'וַיֵּצֵא', 'Wayyiqtol', '3', 's', 'm', 'יצא', 'I-י + III-א'],
            ['19', 'וַיִּבֶן', 'Wayyiqtol', '3', 's', 'm', 'בנה', 'III-ה'],
            ['20', 'וַיָּשׇׁב', 'Wayyiqtol', '3', 's', 'm', 'שוב', 'Biconsonantal'],
        ]
        self.add_generic_table(headers=hdrs_b, rows=rows_b, col_ratios=cr_b, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Part C — Weqatal and Disambiguation (21–30)')
        rows_c = [
            ['21', 'וְשָׁמַרְתָּ', '', '', '', '', ''],
            ['22', 'וְאָהַבְתָּ', '', '', '', '', ''],
            ['23', 'שָׁמַרְתָּ', '', '', '', '', ''],
            ['24', 'וּשְׁמַרְתֶּם', '', '', '', '', ''],
            ['25', 'וְנָתַתָּ', '', '', '', '', ''],
            ['26', 'יִשְׁמֹר', '', '', '', '', ''],
            ['27', 'וְשָׁמְרוּ', '', '', '', '', ''],
            ['28', 'שָׁמְרוּ', '', '', '', '', ''],
            ['29', 'וְעָשִׂיתָ', '', '', '', '', ''],
            ['30', 'וָאֹמַר', '', '', '', '', ''],
        ]
        ans_c = [
            ['21', 'וְשָׁמַרְתָּ', 'Weqatal', '2', 's', 'm', 'שמר'],
            ['22', 'וְאָהַבְתָּ', 'Weqatal', '2', 's', 'm', 'אהב'],
            ['23', 'שָׁמַרְתָּ', 'Perfect', '2', 's', 'm', 'שמר'],
            ['24', 'וּשְׁמַרְתֶּם', 'Weqatal', '2', 'p', 'm', 'שמר'],
            ['25', 'וְנָתַתָּ', 'Weqatal', '2', 's', 'm', 'נתן'],
            ['26', 'יִשְׁמֹר', 'Imperfect', '3', 's', 'm', 'שמר'],
            ['27', 'וְשָׁמְרוּ', 'Weqatal', '3', 'p', 'c', 'שמר'],
            ['28', 'שָׁמְרוּ', 'Perfect', '3', 'p', 'c', 'שמר'],
            ['29', 'וְעָשִׂיתָ', 'Weqatal', '2', 's', 'm', 'עשה'],
            ['30', 'וָאֹמַר', 'Wayyiqtol', '1', 's', 'c', 'אמר'],
        ]
        self.add_generic_table(headers=hdrs_a, rows=rows_c, col_ratios=cr_a, heb_cols=hc,
                               show_answers=True, answer_rows=ans_c)


def build_ch17_parsing_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch17ParsingDrillExercise,
        'Chapter 17 — Parsing Drill: Wayyiqtol and Weqatal',
        'BBH Chapter 17',
        ['hebrew', 'bbh', 'ch17', 'exercises', 'ch17-parsing-drill'],
        'ch17-parsing-drill.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------


class Ch17PassageExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each highlighted form, give: '
            '(a) Form Type (Wayyiqtol / Weqatal / Imperfect / Perfect), '
            '(b) Person, (c) Number, (d) Gender, (e) Root (3ms lexical form), '
            '(f) Usage Note.'
        )
        hdrs = ['#', 'Form', 'Form Type', 'Person', 'Number', 'Gender', 'Root', 'Usage Note']
        cr = [0.05, 0.14, 0.11, 0.08, 0.08, 0.08, 0.12, 0.34]
        hc = [1]

        self.add_section_heading('Passage A — Genesis 1:1–5 (Creation Narrative) (1–4)')
        rows_a = [
            ['1', 'בָּרָא', '', '', '', '', '', ''],
            ['2', 'וַיְהִי', '', '', '', '', '', ''],
            ['3', 'וַיַּרְא', '', '', '', '', '', ''],
            ['4', 'וַיִּקְרָא', '', '', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'בָּרָא', 'Perfect', '3', 's', 'm', 'ברא', 'Simple Past'],
            ['2', 'וַיְהִי', 'Wayyiqtol', '3', 's', 'm', 'היה', 'Sequential Past'],
            ['3', 'וַיַּרְא', 'Wayyiqtol', '3', 's', 'm', 'ראה', 'Sequential Past'],
            ['4', 'וַיִּקְרָא', 'Wayyiqtol', '3', 's', 'm', 'קרא', 'Sequential Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_a, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Passage B — Genesis 22:1–4 (Binding of Isaac) (5–8)')
        rows_b = [
            ['5', 'וַיְהִי', '', '', '', '', '', ''],
            ['6', 'וַיַּשְׁכֵּם', '', '', '', '', '', ''],
            ['7', 'וַיָּקׇם', '', '', '', '', '', ''],
            ['8', 'וַיַּרְא', '', '', '', '', '', ''],
        ]
        ans_b = [
            ['5', 'וַיְהִי', 'Wayyiqtol', '3', 's', 'm', 'היה', 'Sequential Past'],
            ['6', 'וַיַּשְׁכֵּם', 'Wayyiqtol', '3', 's', 'm', 'שכם', 'Sequential Past'],
            ['7', 'וַיָּקׇם', 'Wayyiqtol', '3', 's', 'm', 'קום', 'Sequential Past'],
            ['8', 'וַיַּרְא', 'Wayyiqtol', '3', 's', 'm', 'ראה', 'Sequential Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Passage C — Deuteronomy 6:4–7 (The Shema) (9–11)')
        rows_c = [
            ['9', 'וְאָהַבְתָּ', '', '', '', '', '', ''],
            ['10', 'וְשִׁנַּנְתָּם', '', '', '', '', '', ''],
            ['11', 'וְדִבַּרְתָּ', '', '', '', '', '', ''],
        ]
        ans_c = [
            ['9', 'וְאָהַבְתָּ', 'Weqatal', '2', 's', 'm', 'אהב', 'Sequential Future'],
            ['10', 'וְשִׁנַּנְתָּם', 'Weqatal', '2', 's', 'm', 'שנן', 'Sequential Future'],
            ['11', 'וְדִבַּרְתָּ', 'Weqatal', '2', 's', 'm', 'דבר', 'Sequential Future'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_c, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_c)

        self.add_section_heading('Passage D — Exodus 3:1–6 (Burning Bush) (12–16)')
        rows_d = [
            ['12', 'וַיֵּלֶךְ', '', '', '', '', '', ''],
            ['13', 'וַיַּרְא', '', '', '', '', '', ''],
            ['14', 'וַיֵּפֶן', '', '', '', '', '', ''],
            ['15', 'וַיִּקְרָא', '', '', '', '', '', ''],
            ['16', 'וַיֹּאמֶר', '', '', '', '', '', ''],
        ]
        ans_d = [
            ['12', 'וַיֵּלֶךְ', 'Wayyiqtol', '3', 's', 'm', 'הלך', 'Sequential Past'],
            ['13', 'וַיַּרְא', 'Wayyiqtol', '3', 's', 'm', 'ראה', 'Sequential Past'],
            ['14', 'וַיֵּפֶן', 'Wayyiqtol', '3', 's', 'm', 'פנה', 'Sequential Past'],
            ['15', 'וַיִּקְרָא', 'Wayyiqtol', '3', 's', 'm', 'קרא', 'Sequential Past'],
            ['16', 'וַיֹּאמֶר', 'Wayyiqtol', '3', 's', 'm', 'אמר', 'Sequential Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_d, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_d)


def build_ch17_passage_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch17PassageExercise,
        'Chapter 17 — Passage Exercise: Wayyiqtol and Weqatal in Context',
        'BBH Chapter 17',
        ['hebrew', 'bbh', 'ch17', 'exercises', 'ch17-passage-exercise'],
        'ch17-passage-exercise.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------


class Ch18ParsingDrillExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each form, give: (a) Conjugation (Imperative / Imperfect / Jussive / Cohortative), '
            '(b) Person, (c) Number, (d) Gender, (e) Root (lexical form).'
        )
        hdrs_a = ['#', 'Form', 'Conjugation', 'Person', 'Number', 'Gender', 'Root']
        cr_a = [0.05, 0.11, 0.14, 0.09, 0.09, 0.09, 0.43]
        hdrs_b = ['#', 'Form', 'Conjugation', 'Person', 'Number', 'Gender', 'Root', 'Weak Class']
        cr_b = [0.05, 0.10, 0.12, 0.08, 0.08, 0.08, 0.13, 0.36]
        hc = [1]

        self.add_section_heading('Part A — Strong and Common Roots (1–10)')
        rows_a = [
            ['1', 'שְׁמֹר', '', '', '', '', ''],
            ['2', 'שִׁמְרִי', '', '', '', '', ''],
            ['3', 'שִׁמְרוּ', '', '', '', '', ''],
            ['4', 'שְׁמֹרְנָה', '', '', '', '', ''],
            ['5', 'שְׁמַע', '', '', '', '', ''],
            ['6', 'שִׁמְעוּ', '', '', '', '', ''],
            ['7', 'זְכֹר', '', '', '', '', ''],
            ['8', 'חֲזַק', '', '', '', '', ''],
            ['9', 'כְּתֹב', '', '', '', '', ''],
            ['10', 'קְרָא', '', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'שְׁמֹר', 'Imperative', '2nd', 's', 'm', 'שמר'],
            ['2', 'שִׁמְרִי', 'Imperative', '2nd', 's', 'f', 'שמר'],
            ['3', 'שִׁמְרוּ', 'Imperative', '2nd', 'p', 'm', 'שמר'],
            ['4', 'שְׁמֹרְנָה', 'Imperative', '2nd', 'p', 'f', 'שמר'],
            ['5', 'שְׁמַע', 'Imperative', '2nd', 's', 'm', 'שמע'],
            ['6', 'שִׁמְעוּ', 'Imperative', '2nd', 'p', 'm', 'שמע'],
            ['7', 'זְכֹר', 'Imperative', '2nd', 's', 'm', 'זכר'],
            ['8', 'חֲזַק', 'Imperative', '2nd', 's', 'm', 'חזק'],
            ['9', 'כְּתֹב', 'Imperative', '2nd', 's', 'm', 'כתב'],
            ['10', 'קְרָא', 'Imperative', '2nd', 's', 'm', 'קרא'],
        ]
        self.add_generic_table(headers=hdrs_a, rows=rows_a, col_ratios=cr_a, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Part B — Weak Root Imperatives (11–25)')
        rows_b = [
            ['11', 'לֵךְ', '', '', '', '', '', ''],
            ['12', 'לְכוּ', '', '', '', '', '', ''],
            ['13', 'עֲשֵׂה', '', '', '', '', '', ''],
            ['14', 'עֲשׂוּ', '', '', '', '', '', ''],
            ['15', 'רְאֵה', '', '', '', '', '', ''],
            ['16', 'קוּם', '', '', '', '', '', ''],
            ['17', 'קוּמִי', '', '', '', '', '', ''],
            ['18', 'בֹּא', '', '', '', '', '', ''],
            ['19', 'שׁוּב', '', '', '', '', '', ''],
            ['20', 'שֵׁב', '', '', '', '', '', ''],
            ['21', 'צֵא', '', '', '', '', '', ''],
            ['22', 'תֵּן', '', '', '', '', '', ''],
            ['23', 'תְּנוּ', '', '', '', '', '', ''],
            ['24', 'אֱמֹר', '', '', '', '', '', ''],
            ['25', 'קַח', '', '', '', '', '', ''],
        ]
        ans_b = [
            ['11', 'לֵךְ', 'Imperative', '2nd', 's', 'm', 'הלך', 'I-י'],
            ['12', 'לְכוּ', 'Imperative', '2nd', 'p', 'm', 'הלך', 'I-י'],
            ['13', 'עֲשֵׂה', 'Imperative', '2nd', 's', 'm', 'עשה', 'III-ה + I-gutt.'],
            ['14', 'עֲשׂוּ', 'Imperative', '2nd', 'p', 'm', 'עשה', 'III-ה + I-gutt.'],
            ['15', 'רְאֵה', 'Imperative', '2nd', 's', 'm', 'ראה', 'III-ה'],
            ['16', 'קוּם', 'Imperative', '2nd', 's', 'm', 'קום', 'Biconsonantal'],
            ['17', 'קוּמִי', 'Imperative', '2nd', 's', 'f', 'קום', 'Biconsonantal'],
            ['18', 'בֹּא', 'Imperative', '2nd', 's', 'm', 'בוא', 'Biconsonantal'],
            ['19', 'שׁוּב', 'Imperative', '2nd', 's', 'm', 'שוב', 'Biconsonantal'],
            ['20', 'שֵׁב', 'Imperative', '2nd', 's', 'm', 'ישב', 'I-י'],
            ['21', 'צֵא', 'Imperative', '2nd', 's', 'm', 'יצא', 'I-י + III-א'],
            ['22', 'תֵּן', 'Imperative', '2nd', 's', 'm', 'נתן', 'I-נ'],
            ['23', 'תְּנוּ', 'Imperative', '2nd', 'p', 'm', 'נתן', 'I-נ'],
            ['24', 'אֱמֹר', 'Imperative', '2nd', 's', 'm', 'אמר', 'I-gutt. (א)'],
            ['25', 'קַח', 'Imperative', '2nd', 's', 'm', 'לקח', 'I-י'],
        ]
        self.add_generic_table(headers=hdrs_b, rows=rows_b, col_ratios=cr_b, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Part C — Disambiguation: Imperative, Imperfect, or Jussive? (26–35)')
        rows_c = [
            ['26', 'שְׁמֹר', '', '', '', '', ''],
            ['27', 'יִשְׁמֹר', '', '', '', '', ''],
            ['28', 'אַל־יִשְׁמֹר', '', '', '', '', ''],
            ['29', 'לְכוּ', '', '', '', '', ''],
            ['30', 'יֵלְכוּ', '', '', '', '', ''],
            ['31', 'עֲשֵׂה', '', '', '', '', ''],
            ['32', 'יַעַשׂ', '', '', '', '', ''],
            ['33', 'אַל־תַּעַשׂ', '', '', '', '', ''],
            ['34', 'בֹּא', '', '', '', '', ''],
            ['35', 'יָבֹא', '', '', '', '', ''],
        ]
        ans_c = [
            ['26', 'שְׁמֹר', 'Imperative', '2nd', 's', 'm', 'שמר'],
            ['27', 'יִשְׁמֹר', 'Imperfect', '3rd', 's', 'm', 'שמר'],
            ['28', 'אַל־יִשְׁמֹר', 'Jussive', '3rd', 's', 'm', 'שמר'],
            ['29', 'לְכוּ', 'Imperative', '2nd', 'p', 'm', 'הלך'],
            ['30', 'יֵלְכוּ', 'Imperfect', '3rd', 'p', 'm', 'הלך'],
            ['31', 'עֲשֵׂה', 'Imperative', '2nd', 's', 'm', 'עשה'],
            ['32', 'יַעַשׂ', 'Jussive', '3rd', 's', 'm', 'עשה'],
            ['33', 'אַל־תַּעַשׂ', 'Jussive', '2nd', 's', 'm', 'עשה'],
            ['34', 'בֹּא', 'Imperative', '2nd', 's', 'm', 'בוא'],
            ['35', 'יָבֹא', 'Imperfect', '3rd', 's', 'm', 'בוא'],
        ]
        self.add_generic_table(
            headers=['#', 'Form', 'Form Type', 'Person', 'Number', 'Gender', 'Root'],
            rows=rows_c,
            col_ratios=[0.05, 0.14, 0.14, 0.09, 0.09, 0.09, 0.40],
            heb_cols=hc,
            show_answers=True,
            answer_rows=ans_c,
        )


def build_ch18_parsing_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch18ParsingDrillExercise,
        'Chapter 18 — Parsing Drill: Qal Imperative',
        'BBH Chapter 18',
        ['hebrew', 'bbh', 'ch18', 'exercises', 'ch18-parsing-drill'],
        'ch18-parsing-drill.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------


class Ch18PassageExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each highlighted form, give: '
            '(a) Form Type (Imperative / Imperfect / Jussive / Weqatal), '
            '(b) Person, (c) Number, (d) Gender, (e) Root (lexical form), '
            '(f) Usage Note.'
        )
        hdrs = ['#', 'Form', 'Form Type', 'Person', 'Number', 'Gender', 'Root', 'Usage Note']
        cr = [0.05, 0.12, 0.11, 0.08, 0.08, 0.08, 0.13, 0.35]
        hc = [1]

        self.add_section_heading('Passage A — Genesis 12:1–3 (Call of Abraham) (1–3)')
        rows_a = [
            ['1', 'לֶךְ', '', '', '', '', '', ''],
            ['2', 'עֲזֹב', '', '', '', '', '', ''],
            ['3', 'וֶהְיֵה', '', '', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'לֶךְ', 'Imperative', '2nd', 's', 'm', 'הלך', 'Direct Command'],
            ['2', 'עֲזֹב', 'Imperative', '2nd', 's', 'm', 'עזב', 'Direct Command'],
            ['3', 'וֶהְיֵה', 'Imperative', '2nd', 's', 'm', 'היה', 'Direct Command'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_a, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Passage B — Genesis 22:1–2 (Binding of Isaac) (4–6)')
        rows_b = [
            ['4', 'קַח', '', '', '', '', '', ''],
            ['5', 'וְלֶךְ', '', '', '', '', '', ''],
            ['6', 'וְהַעֲלֵהוּ', '', '', '', '', '', ''],
        ]
        ans_b = [
            ['4', 'קַח', 'Imperative', '2nd', 's', 'm', 'לקח', 'Direct Command'],
            ['5', 'וְלֶךְ', 'Imperative', '2nd', 's', 'm', 'הלך', 'Command Chain'],
            ['6', 'וְהַעֲלֵהוּ', 'Imperative', '2nd', 's', 'm', 'עלה', 'Direct Command (Hiphil)'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Passage C — Deuteronomy 6:4–9 (The Shema) (7–10)')
        rows_c = [
            ['7', 'שְׁמַע', '', '', '', '', '', ''],
            ['8', 'וְאָהַבְתָּ', '', '', '', '', '', ''],
            ['9', 'וְשִׁנַּנְתָּם', '', '', '', '', '', ''],
            ['10', 'וְדִבַּרְתָּ', '', '', '', '', '', ''],
        ]
        ans_c = [
            ['7', 'שְׁמַע', 'Imperative', '2nd', 's', 'm', 'שמע', 'Direct Command'],
            ['8', 'וְאָהַבְתָּ', 'Weqatal', '2nd', 's', 'm', 'אהב', 'Command Chain'],
            ['9', 'וְשִׁנַּנְתָּם', 'Weqatal', '2nd', 's', 'm', 'שנן', 'Command Chain'],
            ['10', 'וְדִבַּרְתָּ', 'Weqatal', '2nd', 's', 'm', 'דבר', 'Command Chain'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_c, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_c)

        self.add_section_heading('Passage D — Genesis 1:28 + Exodus 3:4–5 (Divine Commands) (11–15)')
        rows_d = [
            ['11', 'פְּרוּ', '', '', '', '', '', ''],
            ['12', 'רְבוּ', '', '', '', '', '', ''],
            ['13', 'מִלְאוּ', '', '', '', '', '', ''],
            ['14', 'אַל־תִּקְרַב', '', '', '', '', '', ''],
            ['15', 'שַׁל נְעָלֶיךָ', '', '', '', '', '', ''],
        ]
        ans_d = [
            ['11', 'פְּרוּ', 'Imperative', '2nd', 'p', 'm', 'פרה', 'Direct Command'],
            ['12', 'רְבוּ', 'Imperative', '2nd', 'p', 'm', 'רבה', 'Direct Command'],
            ['13', 'מִלְאוּ', 'Imperative', '2nd', 'p', 'm', 'מלא', 'Direct Command'],
            ['14', 'אַל־תִּקְרַב', 'Jussive', '2nd', 's', 'm', 'קרב', 'Prohibition'],
            ['15', 'שַׁל נְעָלֶיךָ', 'Imperative', '2nd', 's', 'm', 'שלף/של', 'Direct Command'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_d, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_d)

        self.add_section_heading('Passage E — Numbers 13:17–18 (Scouting Canaan) (16)')
        rows_e = [['16', 'עֲלוּ', '', '', '', '', '', '']]
        ans_e = [['16', 'עֲלוּ', 'Imperative', '2nd', 'p', 'm', 'עלה', 'Direct Command']]
        self.add_generic_table(headers=hdrs, rows=rows_e, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_e)


def build_ch18_passage_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch18PassageExercise,
        'Chapter 18 — Passage Exercise: Qal Imperative in Context',
        'BBH Chapter 18',
        ['hebrew', 'bbh', 'ch18', 'exercises', 'ch18-passage-exercise'],
        'ch18-passage-exercise.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Ch19 — Pronominal Suffixes on Verbs
# ---------------------------------------------------------------------------


class Ch19ParsingDrillExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each form, give: (a) Base Verb — conjugation and PGN, '
            '(b) Root, (c) Suffix PGN, (d) Full Gloss.'
        )

        # Part A — Perfect + Suffix (1–8)
        hdrA = ['#', 'Form', 'Base Conjugation', 'Base PGN', 'Root',
                'Suffix PGN', 'Full Gloss']
        crA  = [0.05, 0.13, 0.14, 0.09, 0.10, 0.09, 0.40]
        rowsA = [
            ['1', 'שְׁמָרַ֥נִי', '', '', '', '', ''],
            ['2', 'שְׁמָרוֹ',   '', '', '', '', ''],
            ['3', 'שְׁמָרָ֥נוּ', '', '', '', '', ''],
            ['4', 'שְׁמַרְתַּ֥נִי', '', '', '', '', ''],
            ['5', 'שְׁמַרְתִּ֥יהוּ', '', '', '', '', ''],
            ['6', 'שְׁלָחַ֥נִי', '', '', '', '', ''],
            ['7', 'נְתָנַ֥נִי',  '', '', '', '', ''],
            ['8', 'עֲזָבַ֥נִי',  '', '', '', '', ''],
        ]
        ansA = [
            ['1', 'שְׁמָרַ֥נִי',  'Qal Perfect', '3ms', 'שמר', '1cs', 'he kept me'],
            ['2', 'שְׁמָרוֹ',    'Qal Perfect', '3ms', 'שמר', '3ms', 'he kept him'],
            ['3', 'שְׁמָרָ֥נוּ',  'Qal Perfect', '3ms', 'שמר', '1cp', 'he kept us'],
            ['4', 'שְׁמַרְתַּ֥נִי','Qal Perfect', '2ms', 'שמר', '1cs', 'you kept me'],
            ['5', 'שְׁמַרְתִּ֥יהוּ','Qal Perfect','1cs', 'שמר', '3ms', 'I kept him'],
            ['6', 'שְׁלָחַ֥נִי',  'Qal Perfect', '3ms', 'שלח', '1cs', 'he sent me'],
            ['7', 'נְתָנַ֥נִי',   'Qal Perfect', '3ms', 'נתן', '1cs', 'he gave me'],
            ['8', 'עֲזָבַ֥נִי',   'Qal Perfect', '3ms', 'עזב', '1cs', 'he forsook me'],
        ]
        self.add_section_heading('Part A — Perfect + Suffix (1–8)')
        self.add_generic_table(hdrA, rowsA, crA, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part B — Imperfect + Suffix (Energic Nun) (9–15)
        hdrB = ['#', 'Form', 'Base Conjugation', 'Base PGN', 'Root',
                'Suffix PGN', 'Energic Nun?', 'Full Gloss']
        crB  = [0.05, 0.12, 0.12, 0.09, 0.09, 0.09, 0.09, 0.35]
        rowsB = [
            ['9',  'יִשְׁמְרֵ֥נִי', '', '', '', '', '', ''],
            ['10', 'יִשְׁמְרֶ֥נּוּ', '', '', '', '', '', ''],
            ['11', 'יִשְׁמְרֵ֥נוּ', '', '', '', '', '', ''],
            ['12', 'תִּשְׁמְרֵ֥נִי', '', '', '', '', '', ''],
            ['13', 'יִמְצָאֵ֥נִי', '', '', '', '', '', ''],
            ['14', 'יִשְׁלָחֶ֥נּוּ', '', '', '', '', '', ''],
            ['15', 'יִרְאֶ֥נּוּ',   '', '', '', '', '', ''],
        ]
        ansB = [
            ['9',  'יִשְׁמְרֵ֥נִי', 'Qal Imperfect', '3ms', 'שמר', '1cs', 'No',  'he will keep me'],
            ['10', 'יִשְׁמְרֶ֥נּוּ', 'Qal Imperfect', '3ms', 'שמר', '3ms', 'Yes', 'he will keep him'],
            ['11', 'יִשְׁמְרֵ֥נוּ', 'Qal Imperfect', '3ms', 'שמר', '1cp', 'No',  'he will keep us'],
            ['12', 'תִּשְׁמְרֵ֥נִי', 'Qal Imperfect', '2ms/3fs', 'שמר', '1cs', 'No', 'you/she will keep me'],
            ['13', 'יִמְצָאֵ֥נִי', 'Qal Imperfect', '3ms', 'מצא', '1cs', 'No',  'he will find me'],
            ['14', 'יִשְׁלָחֶ֥נּוּ', 'Qal Imperfect', '3ms', 'שלח', '3ms', 'Yes', 'he will send him'],
            ['15', 'יִרְאֶ֥נּוּ',   'Qal Imperfect', '3ms', 'ראה', '3ms', 'Yes', 'he will see him'],
        ]
        self.add_section_heading('Part B — Imperfect + Suffix / Energic Nun (9–15)')
        self.add_generic_table(hdrB, rowsB, crB, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part C — Imperative and Wayyiqtol + Suffix (16–20)
        hdrC = ['#', 'Form', 'Base Conjugation', 'Base PGN', 'Root',
                'Suffix PGN', 'Full Gloss']
        rowsC = [
            ['16', 'שָׁמְרֵ֥נִי',   '', '', '', '', ''],
            ['17', 'וַיִּשְׁמְרֵ֥הוּ', '', '', '', '', ''],
            ['18', 'וַיִּשְׁלָחֵ֥הוּ', '', '', '', '', ''],
            ['19', 'וַיַּרְאֵ֥הוּ',  '', '', '', '', ''],
            ['20', 'שַׁלְּחֵ֥נִי',   '', '', '', '', ''],
        ]
        ansC = [
            ['16', 'שָׁמְרֵ֥נִי',   'Qal Imperative', '2ms', 'שמר', '1cs', 'Keep me!'],
            ['17', 'וַיִּשְׁמְרֵ֥הוּ', 'Qal Wayyiqtol', '3ms', 'שמר', '3ms', 'and he kept him'],
            ['18', 'וַיִּשְׁלָחֵ֥הוּ', 'Qal Wayyiqtol', '3ms', 'שלח', '3ms', 'and he sent him'],
            ['19', 'וַיַּרְאֵ֥הוּ',  'Qal Wayyiqtol', '3ms', 'ראה', '3ms', 'and he showed/saw him'],
            ['20', 'שַׁלְּחֵ֥נִי',   'Piel Imperative', '2ms', 'שלח', '1cs', 'Send me!'],
        ]
        self.add_section_heading('Part C — Imperative and Wayyiqtol + Suffix (16–20)')
        self.add_generic_table(hdrC, rowsC, crA, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part D — Infinitive Construct + Suffix (21–25)
        hdrD = ['#', 'Form', 'Base Conjugation', 'Root',
                'Suffix PGN', 'Suffix Role', 'Full Gloss']
        crD  = [0.05, 0.13, 0.14, 0.10, 0.09, 0.12, 0.37]
        rowsD = [
            ['21', 'בְּ/שָׁמְר/וֹ',   '', '', '', '', ''],
            ['22', 'כִּ/שְׁמֹ֣עַ/וֹ', '', '', '', '', ''],
            ['23', 'בְּ/רֹאֹת/וֹ',   '', '', '', '', ''],
            ['24', 'לְ/אָהֳבָ֥/הּ',  '', '', '', '', ''],
            ['25', 'כְּ/צֵאת/וֹ',    '', '', '', '', ''],
        ]
        ansD = [
            ['21', 'בְּ/שָׁמְר/וֹ',   'Qal Inf.Const.', 'שמר', '3ms', 'Subject', 'when he kept / in his keeping'],
            ['22', 'כִּ/שְׁמֹ֣עַ/וֹ', 'Qal Inf.Const.', 'שמע', '3ms', 'Subject', 'when he heard'],
            ['23', 'בְּ/רֹאֹת/וֹ',   'Qal Inf.Const.', 'ראה', '3ms', 'Subject', 'when he saw'],
            ['24', 'לְ/אָהֳבָ֥/הּ',  'Qal Inf.Const.', 'אהב', '3fs', 'Subject/Object', 'to love her'],
            ['25', 'כְּ/צֵאת/וֹ',    'Qal Inf.Const.', 'יצא', '3ms', 'Subject', 'when he went out'],
        ]
        self.add_section_heading('Part D — Infinitive Construct + Suffix (21–25)')
        self.add_generic_table(hdrD, rowsD, crD, heb_cols=[1],
                               show_answers=False)

        # Answer key
        self.add_section_break()
        self.add_section_heading('Answer Key — Part A')
        self.add_generic_table(hdrA, rowsA, crA, heb_cols=[1],
                               show_answers=True, answer_rows=ansA)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part B')
        self.add_generic_table(hdrB, rowsB, crB, heb_cols=[1],
                               show_answers=True, answer_rows=ansB)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part C')
        self.add_generic_table(hdrC, rowsC, crA, heb_cols=[1],
                               show_answers=True, answer_rows=ansC)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part D')
        self.add_generic_table(hdrD, rowsD, crD, heb_cols=[1],
                               show_answers=True, answer_rows=ansD)


def build_ch19_parsing_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch19ParsingDrillExercise,
        'Chapter 19 — Parsing Drill: Pronominal Suffixes on Verbs',
        'BBH Chapter 19',
        ['hebrew', 'bbh', 'ch19', 'exercises', 'ch19-parsing-drill'],
        'ch19-parsing-drill.pdf',
        out_dir,
    )


class Ch19PassageExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each highlighted form: (a) Base Verb — conjugation and root, '
            '(b) Suffix PGN, (c) Suffix Role (Object / Subject on Inf.Const.), '
            '(d) Full Gloss.'
        )
        hdr = ['#', 'Form', 'Base Conj.', 'Root',
               'Suffix PGN', 'Suffix Role', 'Full Gloss']
        cr  = [0.05, 0.14, 0.14, 0.09, 0.09, 0.10, 0.39]

        passages = [
            ('Passage A — Genesis 28:13–15 (God\'s Promise to Jacob)', [
                ['1', 'וּשְׁמַרְתִּיךָ',  '', '', '', '', ''],
                ['2', 'וַהֲשִׁבֹתִיךָ',  '', '', '', '', ''],
                ['3', 'אֶעֱזָבְךָ',      '', '', '', '', ''],
            ], [
                ['1', 'וּשְׁמַרְתִּיךָ',  'Qal Weqatal 1cs', 'שמר', '2ms', 'Object', 'and I will keep you'],
                ['2', 'וַהֲשִׁבֹתִיךָ',  'Hiphil Weqatal 1cs', 'שוב', '2ms', 'Object', 'and I will bring you back'],
                ['3', 'אֶעֱזָבְךָ',      'Qal Imperfect 1cs', 'עזב', '2ms', 'Object', 'I will forsake you'],
            ]),
            ('Passage B — Genesis 45:4–8 (Joseph Reveals Himself)', [
                ['4', 'שְׁלָחַ֥נִי (first)', '', '', '', '', ''],
                ['5', 'וַיִּשְׁלָחֵ֥נִי',   '', '', '', '', ''],
                ['6', 'מְכַרְתֶּ֥ם אֹתִי',  '', '', '', '', ''],
            ], [
                ['4', 'שְׁלָחַ֥נִי',        'Qal Perfect 3ms', 'שלח', '1cs', 'Object', 'God sent me'],
                ['5', 'וַיִּשְׁלָחֵ֥נִי',   'Qal Wayyiqtol 3ms', 'שלח', '1cs', 'Object', 'and God sent me'],
                ['6', 'מְכַרְתֶּ֥ם אֹתִי',  'Qal Perfect 2mp', 'מכר', '—', '—', 'you sold me (אֹתִי separate)'],
            ]),
            ('Passage C — Psalm 23:1–4 (The LORD My Shepherd)', [
                ['7',  'יַרְבִּיצֵ֑נִי', '', '', '', '', ''],
                ['8',  'יְנַהֲלֵ֥נִי',  '', '', '', '', ''],
                ['9',  'יַנְחֵ֥נִי',    '', '', '', '', ''],
                ['10', 'יְנַחֲמֻ֑נִי',  '', '', '', '', ''],
            ], [
                ['7',  'יַרְבִּיצֵ֑נִי', 'Hiphil Imperfect 3ms', 'רבץ', '1cs', 'Object', 'he makes me lie down'],
                ['8',  'יְנַהֲלֵ֥נִי',  'Piel Imperfect 3ms',   'נהל', '1cs', 'Object', 'he leads me'],
                ['9',  'יַנְחֵ֥נִי',    'Hiphil Imperfect 3ms', 'נחה', '1cs', 'Object', 'he guides me'],
                ['10', 'יְנַחֲמֻ֑נִי',  'Piel Imperfect 3mp',   'נחם', '1cs', 'Object', 'they comfort me'],
            ]),
            ('Passage D — Genesis 39:12–20 (Infinitive Construct + Suffix)', [
                ['11', 'כִּשְׁמֹ֣עַ אֲדֹנָ֗יו', '', '', '', '', ''],
                ['12', 'כְּרְאֹת/וֹ',            '', '', '', '', ''],
                ['13', 'עָזַ֤ב בִּגְד/וֹ',        '', '', '', '', ''],
                ['14', 'בִּהְיוֹת/וֹ',            '', '', '', '', ''],
            ], [
                ['11', 'כִּשְׁמֹ֣עַ',  'Qal Inf.Const.', 'שמע', '3ms (noun)', 'Subject', 'when his master heard'],
                ['12', 'כְּרְאֹת/וֹ', 'Qal Inf.Const.', 'ראה', '3ms', 'Subject', 'when he saw'],
                ['13', 'בִּגְד/וֹ',   'noun suffix',    'בֶּגֶד', '3ms', 'Possessive', 'his garment'],
                ['14', 'בִּהְיוֹת/וֹ', 'Qal Inf.Const.', 'היה', '3ms', 'Subject', 'while he was there'],
            ]),
            ('Passage E — Psalm 16:1 + Deuteronomy 31:6', [
                ['15', 'שָׁמְרֵ֥נִי',    '', '', '', '', ''],
                ['16', 'יַעַזְבֶ֔/ךָּ', '', '', '', '', ''],
            ], [
                ['15', 'שָׁמְרֵ֥נִי',    'Qal Imperative 2ms', 'שמר', '1cs', 'Object', 'Keep me!'],
                ['16', 'יַעַזְבֶ֔/ךָּ', 'Qal Imperfect 3ms',  'עזב', '2ms', 'Object', 'he will forsake you'],
            ]),
        ]

        for title, rows, ans in passages:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=False)
            self.add_section_break()

        self.add_section_heading('Answer Key')
        for title, rows, ans in passages:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=True, answer_rows=ans)
            self.add_section_break()


def build_ch19_passage_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch19PassageExercise,
        'Chapter 19 — Passage Exercise: Pronominal Suffixes on Verbs in Context',
        'BBH Chapter 19',
        ['hebrew', 'bbh', 'ch19', 'exercises', 'ch19-passage-exercise'],
        'ch19-passage-exercise.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Ch20 — Qal Infinitive Construct
# ---------------------------------------------------------------------------


class Ch20ParsingDrillExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each form: (a) Identify as IC or another form (Imperative / '
            'Imperfect / Perfect), (b) Root, (c) Root class, '
            '(d) Preposition (if any), (e) Function (Purpose / Temporal / '
            'Complementary / Quotative / From / Until).'
        )

        # Part A — Strong and B-class Roots (1–8)
        hdrA = ['#', 'Form', 'IC or other?', 'Root', 'Root Class', 'Prep', 'Function']
        crA  = [0.05, 0.13, 0.12, 0.10, 0.12, 0.08, 0.40]
        rowsA = [
            ['1', 'לִ/שְׁמֹר',  '', '', '', '', ''],
            ['2', 'לִ/שְׁמֹ֣עַ', '', '', '', '', ''],
            ['3', 'כִּ/שְׁמֹ֣עַ', '', '', '', '', ''],
            ['4', 'בִּ/זְכֹר',   '', '', '', '', ''],
            ['5', 'לִ/כְתֹב',   '', '', '', '', ''],
            ['6', 'לֵ/אמֹר',    '', '', '', '', ''],
            ['7', 'לֶ/אֱכֹל',   '', '', '', '', ''],
            ['8', 'מֵ/עֲשׂוֹת', '', '', '', '', ''],
        ]
        ansA = [
            ['1', 'לִ/שְׁמֹר',  'IC', 'שמר', 'Strong A',          'לְ', 'Purpose/Complementary'],
            ['2', 'לִ/שְׁמֹ֣עַ', 'IC', 'שמע', 'Strong B (gutt.)', 'לְ', 'Purpose/Complementary'],
            ['3', 'כִּ/שְׁמֹ֣עַ', 'IC', 'שמע', 'Strong B (gutt.)', 'כְּ', 'Temporal (when/as)'],
            ['4', 'בִּ/זְכֹר',   'IC', 'זכר', 'Strong A',          'בְּ', 'Temporal (when)'],
            ['5', 'לִ/כְתֹב',   'IC', 'כתב', 'Strong A',          'לְ', 'Purpose'],
            ['6', 'לֵ/אמֹר',    'IC', 'אמר', 'I-aleph',           'לְ', 'Quotative'],
            ['7', 'לֶ/אֱכֹל',   'IC', 'אכל', 'I-aleph',           'לְ', 'Purpose/Complementary'],
            ['8', 'מֵ/עֲשׂוֹת', 'IC', 'עשה', 'III-ה + I-gutt.',   'מִן', 'From/cessation'],
        ]
        self.add_section_heading('Part A — Strong and B-class Roots (1–8)')
        self.add_generic_table(hdrA, rowsA, crA, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part B — III-ה and Biconsonantal (9–15): no "IC or other?" column
        hdrB = ['#', 'Form', 'Root', 'Root Class', 'Prep', 'Function']
        crB  = [0.05, 0.14, 0.10, 0.12, 0.08, 0.51]
        rowsB = [
            ['9',  'לִ/רְאוֹת', '', '', '', ''],
            ['10', 'לַ/עֲשׂוֹת', '', '', '', ''],
            ['11', 'הֱיוֹת',     '', '', '', ''],
            ['12', 'לָ/בֹא',     '', '', '', ''],
            ['13', 'לָ/שׁוּב',   '', '', '', ''],
            ['14', 'לָ/מוּת',    '', '', '', ''],
            ['15', 'בְּ/בֹא',    '', '', '', ''],
        ]
        ansB = [
            ['9',  'לִ/רְאוֹת', 'ראה', 'III-ה',           'לְ', 'Purpose'],
            ['10', 'לַ/עֲשׂוֹת', 'עשה', 'III-ה + I-gutt.', 'לְ', 'Purpose/Complementary'],
            ['11', 'הֱיוֹת',     'היה', 'III-ה',           '—',  'Verbal noun/Complementary'],
            ['12', 'לָ/בֹא',     'בוא', 'Biconsonantal',   'לְ', 'Purpose/Complementary'],
            ['13', 'לָ/שׁוּב',   'שוב', 'Biconsonantal',   'לְ', 'Purpose/Complementary'],
            ['14', 'לָ/מוּת',    'מות', 'Biconsonantal',   'לְ', 'Purpose'],
            ['15', 'בְּ/בֹא',    'בוא', 'Biconsonantal',   'בְּ', 'Temporal (when)'],
        ]
        self.add_section_heading('Part B — III-ה and Biconsonantal (9–15)')
        self.add_generic_table(hdrB, rowsB, crB, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part C — I-י, I-נ, and Disambiguation (16–25)
        hdrC = ['#', 'Form', 'IC or other?', 'Root', 'Root Class', 'Notes']
        crC  = [0.05, 0.13, 0.12, 0.10, 0.12, 0.48]
        rowsC = [
            ['16', 'לֶ/כֶת',  '', '', '', ''],
            ['17', 'לָ/שֶׁ/בֶת', '', '', '', ''],
            ['18', 'צֵאת',    '', '', '', ''],
            ['19', 'תֵּת',    '', '', '', ''],
            ['20', 'לָ/דַ/עַת', '', '', '', ''],
            ['21', 'שְׁמֹר',  '', '', '', ''],
            ['22', 'שְׁמֹ֣עַ', '', '', '', ''],
            ['23', 'לֶ/כֶת',  '', '', '', ''],
            ['24', 'יִשְׁמֹר', '', '', '', ''],
            ['25', 'שָׁמַר',  '', '', '', ''],
        ]
        ansC = [
            ['16', 'לֶ/כֶת',  'IC', 'הלך', 'I-י', '"to go"; contracted form'],
            ['17', 'לָ/שֶׁ/בֶת', 'IC', 'ישב', 'I-י', '"to dwell/sit"; yod drops'],
            ['18', 'צֵאת',    'IC', 'יצא', 'I-י + III-א', '"going out"; bare IC with taw'],
            ['19', 'תֵּת',    'IC', 'נתן', 'I-נ', '"to give"; both nuns drop'],
            ['20', 'לָ/דַ/עַת', 'IC', 'ידע', 'I-י', '"to know"'],
            ['21', 'שְׁמֹר',  'IC or Imper.', 'שמר', 'Strong A', 'Ambiguous — context determines'],
            ['22', 'שְׁמֹ֣עַ', 'IC or Imper.', 'שמע', 'Strong B', 'Ambiguous — context determines'],
            ['23', 'לֶ/כֶת',  'IC', 'הלך', 'I-י', 'Cannot be Imperative (which is לֵךְ)'],
            ['24', 'יִשְׁמֹר', 'Imperfect', 'שמר', 'Strong A', 'יִ– prefix = Imperfect'],
            ['25', 'שָׁמַר',  'Perfect', 'שמר', 'Strong A', 'Qamets + patach = Perfect 3ms'],
        ]
        self.add_section_heading('Part C — I-י, I-נ, and Disambiguation (16–25)')
        self.add_generic_table(hdrC, rowsC, crC, heb_cols=[1],
                               show_answers=False)

        # Answer key
        self.add_section_break()
        self.add_section_heading('Answer Key — Part A')
        self.add_generic_table(hdrA, rowsA, crA, heb_cols=[1],
                               show_answers=True, answer_rows=ansA)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part B')
        self.add_generic_table(hdrB, rowsB, crB, heb_cols=[1],
                               show_answers=True, answer_rows=ansB)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part C')
        self.add_generic_table(hdrC, rowsC, crC, heb_cols=[1],
                               show_answers=True, answer_rows=ansC)


def build_ch20_parsing_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch20ParsingDrillExercise,
        'Chapter 20 — Parsing Drill: Qal Infinitive Construct',
        'BBH Chapter 20',
        ['hebrew', 'bbh', 'ch20', 'exercises', 'ch20-parsing-drill'],
        'ch20-parsing-drill.pdf',
        out_dir,
    )


class Ch20PassageExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each highlighted IC form: (a) Root, (b) Root class, '
            '(c) Preposition, (d) Function (Purpose / Temporal / '
            'Complementary / Quotative / From / Epexegetical), (e) Gloss.'
        )
        hdr = ['#', 'Form', 'Root', 'Root Class', 'Prep', 'Function', 'Gloss']
        cr  = [0.05, 0.14, 0.10, 0.12, 0.08, 0.14, 0.37]

        passages = [
            ('Passage 1 — Genesis 2:16–17 (The Garden Command)', [
                ['1', 'לֵאמֹ֑ר', '', '', '', '', ''],
            ], [
                ['1', 'לֵאמֹ֑ר', 'אמר', 'I-aleph', 'לְ', 'Quotative', 'saying'],
            ]),
            ('Passage 2 — Genesis 11:5 (Babel)', [
                ['2', 'לִרְאֹ֥ת', '', '', '', '', ''],
            ], [
                ['2', 'לִרְאֹ֥ת', 'ראה', 'III-ה', 'לְ', 'Purpose', 'to see'],
            ]),
            ('Passage 3 — Genesis 19:22 (Sodom)', [
                ['3', 'לַעֲשׂ֣וֹת', '', '', '', '', ''],
            ], [
                ['3', 'לַעֲשׂ֣וֹת', 'עשה', 'III-ה + I-gutt.', 'לְ', 'Complementary', 'to do'],
            ]),
            ('Passage 4 — Genesis 37:18 (Joseph\'s Brothers)', [
                ['4', 'לַהֲמִית֖וֹ', '', '', '', '', ''],
            ], [
                ['4', 'לַהֲמִית֖וֹ', 'מות', 'Biconsonantal (Hiphil IC)', 'לְ', 'Purpose', 'to kill him'],
            ]),
            ('Passage 5 — Genesis 39:18–19 (Potiphar\'s Wife)', [
                ['5', 'כְשָׁמְע֣וֹ',  '', '', '', '', ''],
                ['6', 'כִשְׁמֹ֨עַ',  '', '', '', '', ''],
            ], [
                ['5', 'כְשָׁמְע֣וֹ',  'שמע', 'Strong B (gutt.)', 'כְּ', 'Temporal (as/when)', 'as/when he heard'],
                ['6', 'כִשְׁמֹ֨עַ',  'שמע', 'Strong B (gutt.)', 'כְּ', 'Temporal (when)', 'when he heard'],
            ]),
            ('Passage 6 — Exodus 3:8 (The Burning Bush)', [
                ['7', 'לְהַצִּיל֣וֹ', '', '', '', '', ''],
                ['8', 'לְהַעֲלֹת֤וֹ', '', '', '', '', ''],
            ], [
                ['7', 'לְהַצִּיל֣וֹ', 'נצל', 'Hiphil (I-gutt.)', 'לְ', 'Purpose', 'to deliver him'],
                ['8', 'לְהַעֲלֹת֤וֹ', 'עלה', 'Hiphil (III-ה)',   'לְ', 'Purpose', 'to bring him up'],
            ]),
            ('Passage 7 — Exodus 19:1 (Arrival at Sinai)', [
                ['9', 'לְצֵ֥את', '', '', '', '', ''],
            ], [
                ['9', 'לְצֵ֥את', 'יצא', 'I-י + III-א', 'לְ', 'Epexegetical/Temporal', 'after the going out of'],
            ]),
            ('Passage 8 — Deuteronomy 6:18 (Land Possession)', [
                ['10', 'לְמַ֣עַן + יִיטַב', '', '', '', '', ''],
            ], [
                ['10', 'לְמַ֣עַן + יִיטַב', '—', '—', 'לְמַעַן', 'Purpose', 'NOT IC — purpose particle + finite verb'],
            ]),
            ('Passage 9 — Ecclesiastes 3:1–2 (A Time for Everything)', [
                ['11', 'לָלֶ֖דֶת',  '', '', '', '', ''],
                ['12', 'לָמ֑וּת',   '', '', '', '', ''],
                ['13', 'לִנְטֹ֙עַ֙', '', '', '', '', ''],
                ['14', 'לַעֲק֔וֹר', '', '', '', '', ''],
            ], [
                ['11', 'לָלֶ֖דֶת',  'ילד', 'I-י',               'לְ', 'Epexegetical', 'to be born'],
                ['12', 'לָמ֑וּת',   'מות', 'Biconsonantal',      'לְ', 'Epexegetical', 'to die'],
                ['13', 'לִנְטֹ֙עַ֙', 'נטע', 'Strong B (gutt. R3)','לְ', 'Epexegetical', 'to plant'],
                ['14', 'לַעֲק֔וֹר', 'עקר', 'I-gutt.',            'לְ', 'Epexegetical', 'to uproot'],
            ]),
            ('Passage 10 — Genesis 45:4–5 (Joseph Reveals Himself)', [
                ['15', 'לְמָכְרֵ֥נִי', '', '', '', '', ''],
                ['16', 'לְמִחְיָ֔ה',  '', '', '', '', ''],
            ], [
                ['15', 'לְמָכְרֵ֥נִי', 'מכר', 'Strong A', 'לְ', 'Purpose', 'to sell me'],
                ['16', 'לְמִחְיָ֔ה',  'חיה', 'III-ה',    'לְ', 'Purpose', 'for preservation of life'],
            ]),
        ]

        for title, rows, ans in passages:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=False)
            self.add_section_break()

        self.add_section_heading('Answer Key')
        for title, rows, ans in passages:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=True, answer_rows=ans)
            self.add_section_break()


def build_ch20_passage_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch20PassageExercise,
        'Chapter 20 — Passage Exercise: Qal Infinitive Construct in Context',
        'BBH Chapter 20',
        ['hebrew', 'bbh', 'ch20', 'exercises', 'ch20-passage-exercise'],
        'ch20-passage-exercise.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Ch21 — Qal Infinitive Absolute
# ---------------------------------------------------------------------------


class Ch21ParsingDrillExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each form: (a) Identify as IA, IC, Imperative, Imperfect, or '
            'Perfect — briefly explain how you know; (b) Root; (c) Root class; '
            '(d) Function if IA (Emphatic / Imperatival / Manner / Progressive).'
        )

        # Part A — Emphatic Pairs (1–8)
        hdrA = ['#', 'Form Pair', 'Which is IA?', 'Root', 'Root Class',
                'Function', 'Gloss']
        crA  = [0.05, 0.20, 0.12, 0.09, 0.12, 0.12, 0.30]
        rowsA = [
            ['1', 'מ֥וֹת — תָּמוּת',         '', '', '', '', ''],
            ['2', 'אָכֹ֥ל — תֹּאכֵֽל',       '', '', '', '', ''],
            ['3', 'שָׁמ֣וֹעַ — תִּשְׁמָע',   '', '', '', '', ''],
            ['4', 'שָׁמ֣וֹר — תִּשְׁמְרוּן', '', '', '', '', ''],
            ['5', 'רָאֹ֣ה — רָאִ֛יתִי',      '', '', '', '', ''],
            ['6', 'טָרֹ֥ף — טֹרַ֖ף',         '', '', '', '', ''],
            ['7', 'נָת֤וֹן — יִנָּתֵן',       '', '', '', '', ''],
            ['8', 'אָבֹ֖ד — תֹּאבֵדוּן',     '', '', '', '', ''],
        ]
        ansA = [
            ['1', 'מ֥וֹת — תָּמוּת',         'מ֥וֹת', 'מות', 'Biconsonantal', 'Emphatic', 'you shall surely die'],
            ['2', 'אָכֹ֥ל — תֹּאכֵֽל',       'אָכֹ֥ל', 'אכל', 'I-aleph',     'Emphatic', 'you may freely eat'],
            ['3', 'שָׁמ֣וֹעַ — תִּשְׁמָע',   'שָׁמ֣וֹעַ', 'שמע', 'Strong B (gutt.)', 'Emphatic', 'hear attentively'],
            ['4', 'שָׁמ֣וֹר — תִּשְׁמְרוּן', 'שָׁמ֣וֹר', 'שמר', 'Strong A',   'Emphatic', 'carefully keep'],
            ['5', 'רָאֹ֣ה — רָאִ֛יתִי',      'רָאֹ֣ה', 'ראה', 'III-ה',       'Emphatic', 'I have surely seen'],
            ['6', 'טָרֹ֥ף — טֹרַ֖ף',         'טָרֹ֥ף', 'טרף', 'Strong A',    'Emphatic', 'he has surely been torn'],
            ['7', 'נָת֤וֹן — יִנָּתֵן',       'נָת֤וֹן', 'נתן', 'I-נ',        'Emphatic', 'it shall certainly be given'],
            ['8', 'אָבֹ֖ד — תֹּאבֵדוּן',     'אָבֹ֖ד', 'אבד', 'Strong A',    'Emphatic', 'you shall utterly perish'],
        ]
        self.add_section_heading('Part A — Emphatic Pairs: IA + Finite Verb (1–8)')
        self.add_generic_table(hdrA, rowsA, crA, heb_cols=[1, 2],
                               show_answers=False)
        self.add_section_break()

        # Part B — Standalone IA Forms (9–14)
        hdrB = ['#', 'Form', 'IA or other?', 'Root', 'Root Class', 'Function']
        crB  = [0.05, 0.13, 0.13, 0.09, 0.12, 0.48]
        rowsB = [
            ['9',  'זָכ֕וֹר', '', '', '', ''],
            ['10', 'שָׁמ֗וֹר', '', '', '', ''],
            ['11', 'הָל֣וֹךְ', '', '', '', ''],
            ['12', 'יָצוֹא֙', '', '', '', ''],
            ['13', 'הָי֧וֹ',  '', '', '', ''],
            ['14', 'גָּאֹ֖ל', '', '', '', ''],
        ]
        ansB = [
            ['9',  'זָכ֕וֹר', 'IA', 'זכר', 'Strong A',    'Imperatival'],
            ['10', 'שָׁמ֗וֹר', 'IA', 'שמר', 'Strong A',    'Imperatival'],
            ['11', 'הָל֣וֹךְ', 'IA', 'הלך', 'I-י',         'Manner/Progressive'],
            ['12', 'יָצוֹא֙', 'IA', 'יצא', 'I-י + III-א', 'Emphatic/Manner'],
            ['13', 'הָי֧וֹ',  'IA', 'היה', 'III-ה',        'Emphatic/Verbal noun'],
            ['14', 'גָּאֹ֖ל', 'IA', 'גאל', 'Strong A',     'Emphatic'],
        ]
        self.add_section_heading('Part B — Standalone IA Forms (9–14)')
        self.add_generic_table(hdrB, rowsB, crB, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part C — Discrimination (15–25)
        hdrC = ['#', 'Form', 'Context given?', 'Identification', 'Root', 'Notes']
        crC  = [0.05, 0.11, 0.18, 0.16, 0.09, 0.41]
        rowsC = [
            ['15', 'מ֥וֹת',    'preceded by לָ',          '', '', ''],
            ['16', 'מ֥וֹת',    'followed by תָּמוּת',     '', '', ''],
            ['17', 'שָׁמ֣וֹר', 'no context',               '', '', ''],
            ['18', 'שְׁמֹר',   'no context',               '', '', ''],
            ['19', 'שָׁמַ֣ר',  'no context',               '', '', ''],
            ['20', 'יִשְׁמֹ֣ר', 'no context',              '', '', ''],
            ['21', 'זָכ֕וֹר',  'imperatival context',      '', '', ''],
            ['22', 'לִ/זְכֹר', 'preceded by כִּי',        '', '', ''],
            ['23', 'לֶ/כֶת',   'no context',               '', '', ''],
            ['24', 'הָל֣וֹךְ', 'followed by וָ/שׁ֑וֹב',  '', '', ''],
            ['25', 'הָלַ֥ךְ',  'no context',               '', '', ''],
        ]
        ansC = [
            ['15', 'מ֥וֹת',    'preceded by לָ',         'IC', 'מות', 'Preposition לָ marks IC; not IA'],
            ['16', 'מ֥וֹת',    'followed by תָּמוּת',    'IA', 'מות', 'No prep; paired with finite verb = emphatic IA'],
            ['17', 'שָׁמ֣וֹר', 'no context',              'IA', 'שמר', 'Qamets under R1 = IA; IC/Imper. would have shewa'],
            ['18', 'שְׁמֹר',   'no context',              'IC or Imper.', 'שמר', 'Shewa under R1 = IC or Imperative 2ms; ambiguous'],
            ['19', 'שָׁמַ֣ר',  'no context',              'Perfect 3ms', 'שמר', 'Qamets + patach = Qal Perfect 3ms'],
            ['20', 'יִשְׁמֹ֣ר', 'no context',             'Imperfect 3ms', 'שמר', 'יִ prefix = Imperfect'],
            ['21', 'זָכ֕וֹר',  'imperatival context',     'Imperatival IA', 'זכר', 'Qamets + holem-waw; stands alone as command'],
            ['22', 'לִ/זְכֹר', 'preceded by כִּי',       'IC', 'זכר', 'לִ prefix = IC; shewa under ז'],
            ['23', 'לֶ/כֶת',   'no context',              'IC', 'הלך', 'I-י contracted IC; IA would be הָל֣וֹךְ'],
            ['24', 'הָל֣וֹךְ', 'followed by וָ/שׁ֑וֹב', 'IA (Manner)', 'הלך', 'Paired IAs describe progressive action'],
            ['25', 'הָלַ֥ךְ',  'no context',              'Perfect 3ms', 'הלך', 'Qamets + patach; IA is הָל֣וֹךְ (holem-waw)'],
        ]
        self.add_section_heading('Part C — Discrimination: IA, IC, Imperative, Imperfect, or Perfect (15–25)')
        self.add_generic_table(hdrC, rowsC, crC, heb_cols=[1],
                               show_answers=False)

        # Answer key
        self.add_section_break()
        self.add_section_heading('Answer Key — Part A')
        self.add_generic_table(hdrA, rowsA, crA, heb_cols=[1, 2],
                               show_answers=True, answer_rows=ansA)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part B')
        self.add_generic_table(hdrB, rowsB, crB, heb_cols=[1],
                               show_answers=True, answer_rows=ansB)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part C')
        self.add_generic_table(hdrC, rowsC, crC, heb_cols=[1],
                               show_answers=True, answer_rows=ansC)


def build_ch21_parsing_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch21ParsingDrillExercise,
        'Chapter 21 — Parsing Drill: Qal Infinitive Absolute',
        'BBH Chapter 21',
        ['hebrew', 'bbh', 'ch21', 'exercises', 'ch21-parsing-drill'],
        'ch21-parsing-drill.pdf',
        out_dir,
    )


class Ch21PassageExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each highlighted IA form: (a) Root, (b) Root class, '
            '(c) Function (Emphatic / Imperatival / Manner / Progressive), '
            '(d) Full gloss of the construction.'
        )
        hdr = ['#', 'Form', 'Root', 'Root Class', 'Function', 'Gloss']
        cr  = [0.05, 0.16, 0.09, 0.12, 0.14, 0.44]

        passages = [
            ('Passage 1 — Genesis 2:16–17 (Permission and Prohibition)', [
                ['1', 'אָכֹ֥ל (in אָכֹ֥ל תֹּאכֵֽל)',  '', '', '', ''],
                ['2', 'מ֥וֹת (in מ֥וֹת תָּמוּת)',       '', '', '', ''],
            ], [
                ['1', 'אָכֹ֥ל', 'אכל', 'I-aleph',     'Emphatic', 'you may freely eat'],
                ['2', 'מ֥וֹת',  'מות', 'Biconsonantal', 'Emphatic', 'you shall surely die'],
            ]),
            ('Passage 2 — Exodus 3:7 (The Burning Bush)', [
                ['3', 'רָאֹ֣ה (in רָאֹ֣ה רָאִ֛יתִי)', '', '', '', ''],
            ], [
                ['3', 'רָאֹ֣ה', 'ראה', 'III-ה', 'Emphatic', 'I have surely seen'],
            ]),
            ('Passage 3 — Exodus 20:8 and Deuteronomy 5:12 (Sabbath)', [
                ['4', 'זָכ֕וֹר', '', '', '', ''],
                ['5', 'שָׁמ֗וֹר', '', '', '', ''],
            ], [
                ['4', 'זָכ֕וֹר', 'זכר', 'Strong A', 'Imperatival', 'Remember!'],
                ['5', 'שָׁמ֗וֹר', 'שמר', 'Strong A', 'Imperatival', 'Keep/Observe!'],
            ]),
            ('Passage 4 — Genesis 8:3, 5 (Flood Waters Recede)', [
                ['6', 'הָל֣וֹךְ (Gen 8:3)',  '', '', '', ''],
                ['7', 'וָ/שׁ֑וֹב',          '', '', '', ''],
                ['8', 'הָל֣וֹךְ (Gen 8:5)',  '', '', '', ''],
                ['9', 'וְ/חָס֔וֹר',         '', '', '', ''],
            ], [
                ['6', 'הָל֣וֹךְ', 'הלך', 'I-י',     'Manner/Progressive', 'going'],
                ['7', 'וָ/שׁ֑וֹב', 'שוב', 'Biconsonantal', 'Manner',          'returning'],
                ['8', 'הָל֣וֹךְ', 'הלך', 'I-י',     'Progressive',       'going'],
                ['9', 'וְ/חָס֔וֹר', 'חסר', 'Strong A',    'Progressive',       'decreasing'],
            ]),
            ('Passage 5 — Genesis 26:13 (Isaac\'s Prosperity)', [
                ['10', 'הָלוֹךְ֙',   '', '', '', ''],
                ['11', 'וְ/גָדֵ֔ל', '', '', '', ''],
            ], [
                ['10', 'הָלוֹךְ֙',   'הלך', 'I-י',     'Progressive', 'going/growing'],
                ['11', 'וְ/גָדֵ֔ל', 'גדל', 'Strong A', 'Progressive', 'growing greater'],
            ]),
            ('Passage 6 — Genesis 44:28 (Jacob on Joseph)', [
                ['12', 'טָרֹ֥ף (in טָרֹ֥ף טֹרַ֖ף)', '', '', '', ''],
            ], [
                ['12', 'טָרֹ֥ף', 'טרף', 'Strong A', 'Emphatic', 'he has surely been torn'],
            ]),
            ('Passage 7 — Deuteronomy 6:17 (Covenant Obedience)', [
                ['13', 'שָׁמ֣וֹר (in שָׁמ֣וֹר תִּשְׁמְר֗וּן)', '', '', '', ''],
            ], [
                ['13', 'שָׁמ֣וֹר', 'שמר', 'Strong A', 'Emphatic', 'diligently keep'],
            ]),
            ('Passage 8 — Deuteronomy 8:19 (Warning)', [
                ['14', 'שָׁכֹ֤חַ (in שָׁכֹ֤חַ תִּשְׁכַּח֙)', '', '', '', ''],
            ], [
                ['14', 'שָׁכֹ֤חַ', 'שכח', 'Strong B (gutt. R3)', 'Emphatic', 'ever forget'],
            ]),
            ('Passage 9 — Numbers 15:35 (Death Penalty Formula)', [
                ['15', 'מ֥וֹת (in מ֥וֹת יוּמַ֖ת)', '', '', '', ''],
            ], [
                ['15', 'מ֥וֹת', 'מות', 'Biconsonantal', 'Emphatic', 'shall surely be put to death'],
            ]),
        ]

        for title, rows, ans in passages:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=False)
            self.add_section_break()

        self.add_section_heading('Answer Key')
        for title, rows, ans in passages:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=True, answer_rows=ans)
            self.add_section_break()


def build_ch21_passage_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch21PassageExercise,
        'Chapter 21 — Passage Exercise: Qal Infinitive Absolute in Context',
        'BBH Chapter 21',
        ['hebrew', 'bbh', 'ch21', 'exercises', 'ch21-passage-exercise'],
        'ch21-passage-exercise.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Ch22 — Qal Participle (Active and Passive)
# ---------------------------------------------------------------------------


class Ch22ParsingDrillExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each form: (a) Active or Passive participle (or other form), '
            '(b) Root, (c) Root class, (d) Gender and Number, '
            '(e) Function (Attributive / Predicate / Substantive / '
            'Progressive / Occupational / Resultant state).'
        )

        # Part A — Active Participle, Strong Roots (1–8)
        hdrAC = ['#', 'Form', 'Act. or Pass.?', 'Root', 'Root Class',
                 'Gender/Number', 'Function']
        crAC  = [0.05, 0.14, 0.12, 0.09, 0.12, 0.12, 0.36]
        rowsA = [
            ['1', 'שֹׁמֵ֖ר',    '', '', '', '', ''],
            ['2', 'שֹׁמֶ֫רֶת',  '', '', '', '', ''],
            ['3', 'שֹׁמְרִ֖ים', '', '', '', '', ''],
            ['4', 'הַ/שֹּׁמֵ֖ר', '', '', '', '', ''],
            ['5', 'שֹׁמֵ֣עַ',   '', '', '', '', ''],
            ['6', 'שֹׁמְעִ֖ים', '', '', '', '', ''],
            ['7', 'עֹמֵ֖ד',     '', '', '', '', ''],
            ['8', 'עֹבֵ֖ר',     '', '', '', '', ''],
        ]
        ansA = [
            ['1', 'שֹׁמֵ֖ר',    'Active', 'שמר', 'Strong A',     'ms', 'Substantive/Predicate'],
            ['2', 'שֹׁמֶ֫רֶת',  'Active', 'שמר', 'Strong A',     'fs', 'Attributive or Substantive'],
            ['3', 'שֹׁמְרִ֖ים', 'Active', 'שמר', 'Strong A',     'mp', 'Substantive/Attributive'],
            ['4', 'הַ/שֹּׁמֵ֖ר', 'Active', 'שמר', 'Strong A',    'ms', 'Substantive with def. article'],
            ['5', 'שֹׁמֵ֣עַ',   'Active', 'שמע', 'Strong B (gutt.)', 'ms', 'Substantive/Predicate'],
            ['6', 'שֹׁמְעִ֖ים', 'Active', 'שמע', 'Strong B',    'mp', 'Attributive/Substantive'],
            ['7', 'עֹמֵ֖ד',     'Active', 'עמד', 'I-gutt.',      'ms', 'Predicate/Substantive'],
            ['8', 'עֹבֵ֖ר',     'Active', 'עבר', 'Strong A',     'ms', 'Substantive'],
        ]
        self.add_section_heading('Part A — Active Participle, Strong Roots (1–8)')
        self.add_generic_table(hdrAC, rowsA, crAC, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part B — Active Participle, Weak Roots (9–16): no Act./Pass. col
        hdrB = ['#', 'Form', 'Root', 'Root Class', 'Gender/Number', 'Function']
        crB  = [0.05, 0.14, 0.09, 0.14, 0.12, 0.46]
        rowsB = [
            ['9',  'עֹשֶׂ֖ה',   '', '', '', ''],
            ['10', 'עֹשִׂ֖ים',  '', '', '', ''],
            ['11', 'יוֹשֵׁ֖ב', '', '', '', ''],
            ['12', 'בָ֖א',      '', '', '', ''],
            ['13', 'מֵ֖ת',      '', '', '', ''],
            ['14', 'נֹתֵ֥ן',    '', '', '', ''],
            ['15', 'הוֹלֵ֣ךְ', '', '', '', ''],
            ['16', 'גֹּאֵ֣ל',  '', '', '', ''],
        ]
        ansB = [
            ['9',  'עֹשֶׂ֖ה',   'עשה', 'III-ה',    'ms', 'Substantive'],
            ['10', 'עֹשִׂ֖ים',  'עשה', 'III-ה',    'mp', 'Substantive/Attributive'],
            ['11', 'יוֹשֵׁ֖ב', 'ישב', 'I-י',       'ms', 'Occupational/Predicate'],
            ['12', 'בָ֖א',      'בוא', 'Biconsonantal', 'ms', 'Substantive/Predicate'],
            ['13', 'מֵ֖ת',      'מות', 'Biconsonantal', 'ms', 'Predicate/Substantive'],
            ['14', 'נֹתֵ֥ן',    'נתן', 'I-נ',       'ms', 'Substantive'],
            ['15', 'הוֹלֵ֣ךְ', 'הלך', 'I-י',       'ms', 'Predicate/Progressive'],
            ['16', 'גֹּאֵ֣ל',  'גאל', 'Strong A',  'ms', 'Substantive'],
        ]
        self.add_section_heading('Part B — Active Participle, Weak Roots (9–16)')
        self.add_generic_table(hdrB, rowsB, crB, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part C — Passive Participle (17–23)
        rowsC = [
            ['17', 'בָּר֥וּךְ',   '', '', '', '', ''],
            ['18', 'אָר֕וּר',    '', '', '', '', ''],
            ['19', 'כָּת֥וּב',   '', '', '', '', ''],
            ['20', 'בְּרוּכָ֥ה', '', '', '', '', ''],
            ['21', 'כְּתוּבִ֥ים', '', '', '', '', ''],
            ['22', 'נְטוּיָ֖ה',  '', '', '', '', ''],
            ['23', 'בְּלוּלָ֥ה', '', '', '', '', ''],
        ]
        ansC = [
            ['17', 'בָּר֥וּךְ',   'Passive', 'ברך', 'Strong A', 'ms', 'Predicate'],
            ['18', 'אָר֕וּר',    'Passive', 'ארר', 'Geminate',  'ms', 'Predicate'],
            ['19', 'כָּת֥וּב',   'Passive', 'כתב', 'Strong A', 'ms', 'Predicate/Attributive'],
            ['20', 'בְּרוּכָ֥ה', 'Passive', 'ברך', 'Strong A', 'fs', 'Predicate/Attributive'],
            ['21', 'כְּתוּבִ֥ים', 'Passive', 'כתב', 'Strong A', 'mp', 'Attributive'],
            ['22', 'נְטוּיָ֖ה',  'Passive', 'נטה', 'III-ה',    'fs', 'Attributive'],
            ['23', 'בְּלוּלָ֥ה', 'Passive', 'בלל', 'Geminate',  'fs', 'Attributive'],
        ]
        self.add_section_heading('Part C — Passive Participle (17–23)')
        self.add_generic_table(hdrAC, rowsC, crAC, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part D — Discrimination (24–32)
        hdrD = ['#', 'Form', 'Identification', 'Root', 'Notes']
        crD  = [0.05, 0.12, 0.22, 0.09, 0.52]
        rowsD = [
            ['24', 'שֹׁמֵ֖ר',  '', '', ''],
            ['25', 'שָׁמַ֣ר',  '', '', ''],
            ['26', 'יִשְׁמֹ֣ר', '', '', ''],
            ['27', 'שָׁמ֥וּר',  '', '', ''],
            ['28', 'שְׁמֹר',   '', '', ''],
            ['29', 'שָׁמ֣וֹר', '', '', ''],
            ['30', 'בָ֖א',     '', '', ''],
            ['31', 'לָ/בֹא',   '', '', ''],
            ['32', 'יִ/יְשֵׁ֣ב', '', '', ''],
        ]
        ansD = [
            ['24', 'שֹׁמֵ֖ר',  'Qal Active Ptc. ms',         'שמר', 'Holem-waw + tsere'],
            ['25', 'שָׁמַ֣ר',  'Qal Perfect 3ms',             'שמר', 'Qamets + patach'],
            ['26', 'יִשְׁמֹ֣ר', 'Qal Imperfect 3ms',          'שמר', 'יִ prefix'],
            ['27', 'שָׁמ֥וּר',  'Qal Passive Ptc. ms',        'שמר', 'Qamets + shureq (qatûl)'],
            ['28', 'שְׁמֹר',   'Qal IC or Imper. 2ms',        'שמר', 'Shewa + holem; ambiguous'],
            ['29', 'שָׁמ֣וֹר', 'Qal IA',                      'שמר', 'Qamets + holem-waw'],
            ['30', 'בָ֖א',     'Active Ptc. ms or Perfect 3ms','בוא', 'Biconsonantal; context decides'],
            ['31', 'לָ/בֹא',   'Qal IC',                      'בוא', 'לָ prefix = IC'],
            ['32', 'יִ/יְשֵׁ֣ב', 'Qal Imperfect 3ms',         'ישב', 'יִ prefix; ptc. would be יוֹשֵׁ֖ב'],
        ]
        self.add_section_heading('Part D — Discrimination (24–32)')
        self.add_generic_table(hdrD, rowsD, crD, heb_cols=[1],
                               show_answers=False)

        # Answer key
        self.add_section_break()
        self.add_section_heading('Answer Key — Part A')
        self.add_generic_table(hdrAC, rowsA, crAC, heb_cols=[1],
                               show_answers=True, answer_rows=ansA)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part B')
        self.add_generic_table(hdrB, rowsB, crB, heb_cols=[1],
                               show_answers=True, answer_rows=ansB)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part C')
        self.add_generic_table(hdrAC, rowsC, crAC, heb_cols=[1],
                               show_answers=True, answer_rows=ansC)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part D')
        self.add_generic_table(hdrD, rowsD, crD, heb_cols=[1],
                               show_answers=True, answer_rows=ansD)


def build_ch22_parsing_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch22ParsingDrillExercise,
        'Chapter 22 — Parsing Drill: Qal Participle (Active and Passive)',
        'BBH Chapter 22',
        ['hebrew', 'bbh', 'ch22', 'exercises', 'ch22-parsing-drill'],
        'ch22-parsing-drill.pdf',
        out_dir,
    )


class Ch22PassageExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each highlighted participle: (a) Active or Passive, '
            '(b) Root, (c) Root class, (d) Gender/Number, '
            '(e) Syntactic function (Attributive / Predicate / Substantive / '
            'Progressive / Occupational / Resultant state), (f) Gloss.'
        )
        hdr = ['#', 'Form', 'Act./Pass.', 'Root', 'Root Class',
               'G/N', 'Function', 'Gloss']
        cr  = [0.05, 0.13, 0.09, 0.08, 0.11, 0.06, 0.13, 0.35]

        passages = [
            ('Passage 1 — Genesis 3:14 and 4:11 (Curse Formulas)', [
                ['1', 'אָר֤וּר (Gen 3:14)', '', '', '', '', '', ''],
                ['2', 'אָר֤וּר (Gen 4:11)', '', '', '', '', '', ''],
            ], [
                ['1', 'אָר֤וּר', 'Passive', 'ארר', 'Geminate', 'ms', 'Predicate', 'you are cursed'],
                ['2', 'אָר֤וּר', 'Passive', 'ארר', 'Geminate', 'ms', 'Predicate', 'cursed are you'],
            ]),
            ('Passage 2 — Genesis 14:19 and 24:27 (Blessing Formulas)', [
                ['3', 'בָּר֤וּךְ (Gen 14:19)', '', '', '', '', '', ''],
                ['4', 'בָּר֤וּךְ (Gen 24:27)', '', '', '', '', '', ''],
            ], [
                ['3', 'בָּר֤וּךְ', 'Passive', 'ברך', 'Strong A', 'ms', 'Predicate', 'blessed is Abram'],
                ['4', 'בָּר֤וּךְ', 'Passive', 'ברך', 'Strong A', 'ms', 'Predicate', 'blessed is the LORD'],
            ]),
            ('Passage 3 — Genesis 18:1 (Abraham at the Tent)', [
                ['5', 'יֹשֵׁ֤ב', '', '', '', '', '', ''],
            ], [
                ['5', 'יֹשֵׁ֤ב', 'Active', 'ישב', 'I-י', 'ms', 'Predicate (circumstantial)', 'sitting'],
            ]),
            ('Passage 4 — Genesis 4:9 (Am I My Brother\'s Keeper?)', [
                ['6', 'שֹׁמֵ֥ר', '', '', '', '', '', ''],
            ], [
                ['6', 'שֹׁמֵ֥ר', 'Active', 'שמר', 'Strong A', 'ms', 'Substantive', 'keeper'],
            ]),
            ('Passage 5 — Exodus 3:2 (The Burning Bush)', [
                ['7', 'בֹּעֵ֣ר', '', '', '', '', '', ''],
            ], [
                ['7', 'בֹּעֵ֣ר', 'Active', 'בער', 'Strong A', 'ms', 'Predicate (attributive)', 'burning'],
            ]),
            ('Passage 6 — Exodus 6:6 (Outstretched Arm)', [
                ['8', 'נְטוּיָ֖ה', '', '', '', '', '', ''],
            ], [
                ['8', 'נְטוּיָ֖ה', 'Passive', 'נטה', 'III-ה', 'fs', 'Attributive', 'outstretched'],
            ]),
            ('Passage 7 — Deuteronomy 9:10 (Tablets Written by God)', [
                ['9', 'כְּתֻבִ֣ים', '', '', '', '', '', ''],
            ], [
                ['9', 'כְּתֻבִ֣ים', 'Passive', 'כתב', 'Strong A', 'mp', 'Attributive', 'written'],
            ]),
            ('Passage 9 — Leviticus 2:4–5 (Grain Offering)', [
                ['10', 'בְּלוּלֹ֥ת', '', '', '', '', '', ''],
            ], [
                ['10', 'בְּלוּלֹ֥ת', 'Passive', 'בלל', 'Geminate', 'fp', 'Attributive', 'mixed with oil'],
            ]),
            ('Passage 10 — Genesis 37:2 and Numbers 27:17 (Shepherd)', [
                ['11', 'רֹעֶ֩ה (Gen 37:2)',  '', '', '', '', '', ''],
                ['12', 'רֹעֶ֖ה (Num 27:17)', '', '', '', '', '', ''],
            ], [
                ['11', 'רֹעֶ֩ה', 'Active', 'רעה', 'III-ה', 'ms', 'Predicate (progressive)', 'was shepherding'],
                ['12', 'רֹעֶ֖ה', 'Active', 'רעה', 'III-ה', 'ms', 'Substantive',             'shepherd'],
            ]),
            ('Passage 11 — Leviticus 25:25 (Kinsman-Redeemer)', [
                ['13', 'גֹאֲל֔וֹ', '', '', '', '', '', ''],
            ], [
                ['13', 'גֹאֲל֔וֹ', 'Active', 'גאל', 'Strong A', 'ms + 3ms sfx', 'Substantive', 'his redeemer'],
            ]),
            ('Passage 12 — Numbers 14:14 (The LORD Among His People)', [
                ['14', 'עֹמֵ֣ד', '', '', '', '', '', ''],
            ], [
                ['14', 'עֹמֵ֣ד', 'Active', 'עמד', 'Strong A', 'ms', 'Predicate', 'standing'],
            ]),
            ('Standalone Forms', [
                ['15', 'נֹתֵ֥ן',    '', '', '', '', '', ''],
                ['16', 'יוֹשְׁבֵ֣י', '', '', '', '', '', ''],
            ], [
                ['15', 'נֹתֵ֥ן',    'Active', 'נתן', 'I-נ', 'ms',        'Substantive', 'giver / one who gives'],
                ['16', 'יוֹשְׁבֵ֣י', 'Active', 'ישב', 'I-י', 'mp const.', 'Attributive/Substantive', 'inhabitants of'],
            ]),
        ]

        for title, rows, ans in passages:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=False)
            self.add_section_break()

        self.add_section_heading('Answer Key')
        for title, rows, ans in passages:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=True, answer_rows=ans)
            self.add_section_break()


def build_ch22_passage_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch22PassageExercise,
        'Chapter 22 — Passage Exercise: Qal Participle (Active and Passive) in Context',
        'BBH Chapter 22',
        ['hebrew', 'bbh', 'ch22', 'exercises', 'ch22-passage-exercise'],
        'ch22-passage-exercise.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Ch23 — Clause Analysis / Reading the Clause
# ---------------------------------------------------------------------------


class Ch23ClauseAnalysisExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each clause: (a) Clause type (Verbal VSO / Verbal — fronted / '
            'Verbless / Waw-disjunctive / Circumstantial), '
            '(b) Main verb and conjugation (if any), '
            '(c) Fronted element (if any) and why, '
            '(d) Full English gloss.'
        )

        # Part A — VSO Verbal Clauses (1–4)
        hdrA = ['#', 'Hebrew', 'Clause Type', 'Verb & Conjugation',
                'Subject', 'Object/Predicate', 'Gloss']
        crA  = [0.05, 0.22, 0.12, 0.15, 0.10, 0.14, 0.22]
        rowsA = [
            ['1', 'וַיִּבְרָ֨א אֱלֹהִ֤ים אֶת‑הָ/אָדָ֙ם֙ (Gen 1:27)', '', '', '', '', ''],
            ['2', 'וַיֹּ֤אמֶר יְהוָ֔ה אֶל‑מֹשֶׁ֖ה (Exo 3:7)',        '', '', '', '', ''],
            ['3', 'שָׁמְע֖וּ בְּנֵ֣י יִשְׂרָאֵ֑ל (Deu 6:4)',              '', '', '', '', ''],
            ['4', 'וַיַּ֥רְא אֱלֹהִ֖ים אֶת‑הָ/אוֹר֑ (Gen 1:4)',      '', '', '', '', ''],
        ]
        ansA = [
            ['1', 'וַיִּבְרָ֨א אֱלֹהִ֤ים …', 'Verbal VSO', 'וַיִּבְרָ֨א (Wayyiqtol Qal 3ms)', 'אֱלֹהִ֤ים', 'אֶת‑הָ/אָדָ֙ם֙', 'And God created man'],
            ['2', 'וַיֹּ֤אמֶר יְהוָ֔ה …',     'Verbal VSO', 'וַיֹּ֤אמֶר (Wayyiqtol Qal 3ms)', 'יְהוָ֔ה',    'אֶל‑מֹשֶׁ֖ה (PP)', 'And the LORD said to Moses'],
            ['3', 'שָׁמְע֖וּ בְּנֵ֣י יִשְׂרָאֵ֑ל', 'Verbal VSO', 'שָׁמְע֖וּ (Qal Imper. 2mp)', '— (addressed)', '—', 'Hear, O Israel'],
            ['4', 'וַיַּ֥רְא אֱלֹהִ֖ים …',    'Verbal VSO', 'וַיַּ֥רְא (Wayyiqtol Qal 3ms)',  'אֱלֹהִ֖ים', 'אֶת‑הָ/אוֹר֑', 'And God saw the light'],
        ]
        self.add_section_heading('Part A — Verbal Clauses: Default VSO (1–4)')
        self.add_generic_table(hdrA, rowsA, crA, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part B — Fronted Elements (5–8)
        hdrB = ['#', 'Hebrew', 'What is fronted?', 'Type of element',
                'Why fronted?', 'Gloss']
        crB  = [0.05, 0.22, 0.14, 0.12, 0.22, 0.25]
        rowsB = [
            ['5', 'הַ/יּ֖וֹם יָלַ֥דְתִּי (Psa 2:7)',                   '', '', '', ''],
            ['6', 'וְאֶל‑קַ֥יִן … לֹ֥א שָׁעָֽה (Gen 4:5)',          '', '', '', ''],
            ['7', 'אֶת‑הָ/אָ֖רֶץ הַ/זֹּ֑את אֶתֵּ֥ן … (Gen 12:7)', '', '', '', ''],
            ['8', 'בְּ/צֶ֥לֶם אֱלֹהִ֖ים בָּרָ֣א אֹת֑וֹ (Gen 1:27b)',  '', '', '', ''],
        ]
        ansB = [
            ['5', 'הַ/יּ֖וֹם יָלַ֥דְתִּי',          'הַ/יּ֖וֹם',     'Temporal adverb', 'Emphatic: Today (not another day)', 'Today I have begotten you'],
            ['6', 'וְאֶל‑קַ֥יִן … לֹ֥א שָׁעָֽה', 'אֶל‑קַ֥יִן', 'Prepositional phrase', 'Contrast: to Cain (vs. Abel)', 'But to Cain he did not pay attention'],
            ['7', 'אֶת‑הָ/אָ֖רֶץ … אֶתֵּ֥ן',  'אֶת‑הָ/אָ֖רֶץ', 'Object', 'Emphasis on object: *This land* I will give', 'This land I will give to your offspring'],
            ['8', 'בְּ/צֶ֥לֶם אֱלֹהִ֖ים …',        'בְּ/צֶ֥לֶם אֱלֹהִ֖ים', 'Prepositional phrase', 'Chiastic emphasis: the image is central', 'In the image of God he created him'],
        ]
        self.add_section_heading('Part B — Fronted Elements (5–8)')
        self.add_generic_table(hdrB, rowsB, crB, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part C — Verbless Clauses (9–12)
        hdrC = ['#', 'Hebrew', 'Subject', 'Predicate', 'Implied Copula', 'Gloss']
        crC  = [0.05, 0.26, 0.12, 0.14, 0.12, 0.31]
        rowsC = [
            ['9',  'יְהוָ֥ה אֱלֹהֵ֖ינוּ יְהוָ֥ה אֶחָֽד (Deu 6:4b)', '', '', '', ''],
            ['10', 'טוֹב֙ הָ/אוֹר֑ (Gen 1:4)',                         '', '', '', ''],
            ['11', 'אָנֹכִ֖י יְהוָ֣ה אֱלֹהֶ֑יךָ (Exo 20:2)',          '', '', '', ''],
            ['12', 'הֲ/שֹׁמֵ֥ר אָחִ֖י אָנֹֽכִי (Gen 4:9)',            '', '', '', ''],
        ]
        ansC = [
            ['9',  'יְהוָ֥ה אֱלֹהֵ֖ינוּ …', 'יְהוָ֥ה', 'אֱלֹהֵ֖ינוּ / אֶחָֽד', 'is', 'The LORD is our God; the LORD is one'],
            ['10', 'טוֹב֙ הָ/אוֹר֑',         'הָ/אוֹר',  'טוֹב (pred. adj.)',   'was', 'The light was good'],
            ['11', 'אָנֹכִ֖י יְהוָ֣ה …',     'אָנֹכִ֖י', 'יְהוָ֣ה אֱלֹהֶ֑יךָ', 'am',  'I am the LORD your God'],
            ['12', 'הֲ/שֹׁמֵ֥ר אָחִ֖י אָנֹֽכִי', 'אָנֹכִי', 'שֹׁמֵ֥ר (pred. ptc.)', 'am', 'Am I my brother\'s keeper?'],
        ]
        self.add_section_heading('Part C — Verbless Clauses (9–12)')
        self.add_generic_table(hdrC, rowsC, crC, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part D — Waw-Disjunctive and Circumstantial (13–16)
        hdrD = ['#', 'Hebrew', 'First element after וְ', 'Function',
                'Relation to main narrative', 'Gloss']
        crD  = [0.05, 0.24, 0.12, 0.11, 0.22, 0.26]
        rowsD = [
            ['13', 'וְהָ/אָ֗רֶץ הָיְתָ֥ה תֹ֙הוּ֙ (Gen 1:2)',           '', '', '', ''],
            ['14', 'וְה֗וּא יֹשֵׁ֤ב פֶּֽתַח (Gen 18:1)',                '', '', '', ''],
            ['15', 'וְהַ/נָּחָשׁ֙ הָיָ֣ה עָר֔וּם (Gen 3:1)',            '', '', '', ''],
            ['16', 'וְהוּא֙ לֹ֣א יָדַ֔ע כִּ֥י יְהוָ֖ה עָזְבֽוֹ (Jdg 16:20)', '', '', '', ''],
        ]
        ansD = [
            ['13', 'וְהָ/אָ֗רֶץ הָיְתָ֥ה …', 'הָ/אָ֗רֶץ (noun)', 'Background', 'Off-narrative; sets scene before creation', 'Now the earth was formless and empty'],
            ['14', 'וְה֗וּא יֹשֵׁ֤ב …',       'הוּא + ptc.',        'Simultaneous circumstance', 'What Abraham was doing when LORD appeared', 'while he was sitting at the entrance'],
            ['15', 'וְהַ/נָּחָשׁ֙ …',         'הַ/נָּחָשׁ (noun)', 'Background', 'Introduces serpent before dialogue', 'Now the serpent was more crafty'],
            ['16', 'וְהוּא֙ לֹ֣א יָדַ֔ע …',   'הוּא (pronoun)',     'Contrast/irony', 'Contrasts Samson\'s action with his ignorance', 'but he did not know the LORD had left him'],
        ]
        self.add_section_heading('Part D — Waw-Disjunctive and Circumstantial (13–16)')
        self.add_generic_table(hdrD, rowsD, crD, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part E — Mixed Analysis (17–20)
        hdrE = ['#', 'Hebrew', 'Clause Type', 'Special Feature', 'Gloss']
        crE  = [0.05, 0.28, 0.14, 0.26, 0.27]
        rowsE = [
            ['17', 'בְּ/רֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים … (Gen 1:1)',     '', '', ''],
            ['18', 'הִנֵּ֥ה אָנֹכִ֖י שֹׁלֵ֥חַ מַלְאָ֖ךְ (Exo 23:20)', '', '', ''],
            ['19', 'וְאָהַבְתָּ֙ אֵ֣ת יְהוָ֣ה אֱלֹהֶ֔יךָ (Deu 6:5)',  '', '', ''],
            ['20', 'כִּ֣י אֵ֤ין אֱלֹהִים֙ זוּלָ֣תִי (Deu 32:39)',     '', '', ''],
        ]
        ansE = [
            ['17', 'בְּ/רֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים …', 'Verbal — PP fronted', 'Temporal PP בְּ/רֵאשִׁ֖ית fronted; VSO follows', 'In the beginning God created the heavens and the earth'],
            ['18', 'הִנֵּ֥ה אָנֹכִ֖י שֹׁלֵ֥חַ …',       'Verbless / Presentative', 'הִנֵּה + pronoun + participle = vivid present', 'Behold, I am sending an angel before you'],
            ['19', 'וְאָהַבְתָּ֙ אֵ֣ת יְהוָ֣ה …',       'Verbal — Weqatal',       'Weqatal continues imperatival chain from שְׁמַ֖ע', 'And you shall love the LORD your God'],
            ['20', 'כִּ֣י אֵ֤ין אֱלֹהִים֙ …',            'Verbless / Existence',   'אֵין = non-existence particle; כִּי = emphatic', 'For there is no God besides me'],
        ]
        self.add_section_heading('Part E — Mixed Analysis (17–20)')
        self.add_generic_table(hdrE, rowsE, crE, heb_cols=[1],
                               show_answers=False)

        # Answer key
        self.add_section_break()
        self.add_section_heading('Answer Key — Part A')
        self.add_generic_table(hdrA, rowsA, crA, heb_cols=[1],
                               show_answers=True, answer_rows=ansA)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part B')
        self.add_generic_table(hdrB, rowsB, crB, heb_cols=[1],
                               show_answers=True, answer_rows=ansB)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part C')
        self.add_generic_table(hdrC, rowsC, crC, heb_cols=[1],
                               show_answers=True, answer_rows=ansC)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part D')
        self.add_generic_table(hdrD, rowsD, crD, heb_cols=[1],
                               show_answers=True, answer_rows=ansD)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part E')
        self.add_generic_table(hdrE, rowsE, crE, heb_cols=[1],
                               show_answers=True, answer_rows=ansE)


def build_ch23_clause_analysis(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch23ClauseAnalysisExercise,
        'Chapter 23 — Clause Analysis Drill',
        'BBH Chapter 23',
        ['hebrew', 'bbh', 'ch23', 'exercises', 'ch23-clause-analysis'],
        'ch23-clause-analysis.pdf',
        out_dir,
    )


class Ch23PassageExercise(ExercisePDF):
    def _build(self) -> None:
        self.add_instructions(
            'For each highlighted clause: (a) identify the clause type, '
            '(b) identify any fronted element and its rhetorical function, '
            '(c) state the verb and its conjugation (if any), '
            '(d) supply the English gloss.'
        )
        hdr = ['#', 'Clause', 'Clause Type', 'Fronted Element (if any)',
               'Verb & Conjugation', 'Gloss']
        cr  = [0.05, 0.24, 0.14, 0.18, 0.16, 0.23]

        passages = [
            ('Passage 1 — Genesis 1:1–4 (Creation Account)', [
                ['1', 'בְּ/רֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים … (Gen 1:1)', '', '', '', ''],
                ['2', 'וְהָ/אָ֗רֶץ הָיְתָ֥ה תֹ֙הוּ֙ וָ/בֹ֔הוּ (Gen 1:2a)', '', '', '', ''],
                ['3', 'וַיֹּ֤אמֶר אֱלֹהִ֙ים֙ (Gen 1:3)',                   '', '', '', ''],
                ['4', 'כִּי‑טוֹב (Gen 1:4b)',                           '', '', '', ''],
            ], [
                ['1', 'בְּ/רֵאשִׁ֖ית בָּרָ֣א …',   'Verbal — PP fronted',         'בְּ/רֵאשִׁ֖ית (temporal PP)', 'בָּרָ֣א — Qal Perfect 3ms', 'In the beginning God created the heavens and the earth'],
                ['2', 'וְהָ/אָ֗רֶץ הָיְתָ֥ה …',    'Waw-disjunctive (Background)', 'הָ/אָ֗רֶץ (noun)',          'הָיְתָ֥ה — Qal Perfect 3fs', 'Now the earth was formless and empty'],
                ['3', 'וַיֹּ֤אמֶר אֱלֹהִ֙ים֙',    'Verbal VSO',                   'None',                        'וַיֹּ֤אמֶר — Wayyiqtol Qal 3ms', 'And God said'],
                ['4', 'כִּי‑טוֹב',              'Verbless (כִּי embedded)',     'None',                        'None', 'that it was good'],
            ]),
            ('Passage 2 — Genesis 3:1–5 (The Serpent and Eve)', [
                ['5', 'וְהַ/נָּחָשׁ֙ הָיָ֣ה עָר֔וּם (Gen 3:1a)', '', '', '', ''],
                ['6', 'וַיֹּ֙אמֶר֙ אֶל‑הָ/אִשָּׁ֔ה (Gen 3:1b)', '', '', '', ''],
                ['7', 'לֹ֥א מ֖וֹת תְּמֻתֽוּן (Gen 3:4)',           '', '', '', ''],
            ], [
                ['5', 'וְהַ/נָּחָשׁ֙ הָיָ֣ה …',    'Waw-disjunctive (Background)', 'הַ/נָּחָשׁ (noun)',         'הָיָ֣ה — Qal Perfect 3ms', 'Now the serpent was more crafty'],
                ['6', 'וַיֹּ֙אמֶר֙ אֶל‑הָ/אִשָּׁ֔ה', 'Verbal VSO',            'None',                       'וַיֹּ֙אמֶר֙ — Wayyiqtol Qal 3ms', 'And he said to the woman'],
                ['7', 'לֹ֥א מ֖וֹת תְּמֻתֽוּן',    'Verbal — IA fronted',          'מ֖וֹת (Inf. Absolute)',      'תְּמֻתֽוּן — Qal Imperfect 2mp', 'You will not surely die'],
            ]),
            ('Passage 3 — Deuteronomy 6:4–5 (The Shema)', [
                ['8',  'שְׁמַ֖ע יִשְׂרָאֵ֑ל (Deu 6:4a)',                            '', '', '', ''],
                ['9',  'יְהוָ֥ה אֱלֹהֵ֖ינוּ יְהוָ֥ה אֶחָֽד (Deu 6:4b)',           '', '', '', ''],
                ['10', 'וְאָהַבְתָּ֙ אֵ֣ת יְהוָ֣ה אֱלֹהֶ֔יךָ (Deu 6:5)',         '', '', '', ''],
            ], [
                ['8',  'שְׁמַ֖ע יִשְׂרָאֵ֑ל',       'Verbal VSO',                  'None', 'שְׁמַ֖ע — Qal Imperative 2ms', 'Hear, O Israel'],
                ['9',  'יְהוָ֥ה אֱלֹהֵ֖ינוּ …',     'Verbless (×2)',               'None', 'None', 'The LORD is our God; the LORD is one'],
                ['10', 'וְאָהַבְתָּ֙ …',             'Verbal — Weqatal',            'None', 'וְאָהַבְתָּ֙ — Weqatal Qal 2ms', 'And you shall love the LORD your God'],
            ]),
            ('Passage 4 — Genesis 22:1–2 (The Binding of Isaac)', [
                ['11', 'וְאַבְרָהָ֖ם זָקֵ֑ן',                           '', '', '', ''],
                ['12', 'אֶת‑יִצְחָ֖ק אֲשֶׁ֣ר אָהַ֑בְתָּ (Gen 22:2b)', '', '', '', ''],
            ], [
                ['11', 'וְאַבְרָהָ֖ם זָקֵ֑ן',           'Waw-disjunctive (Background)', 'אַבְרָהָ֖ם (noun)', 'None (verbless)', 'Now Abraham was old'],
                ['12', 'אֶת‑יִצְחָ֖ק אֲשֶׁ֣ר …', 'Verbal — Object fronted',       'אֶת‑יִצְחָ֖ק (direct obj.)', 'אָהַ֑בְתָּ — Qal Perfect 2ms', 'Isaac, whom you love'],
            ]),
            ('Passage 5 — Judges 16:20 / Genesis 4:9 / Exodus 20:2 (Mixed)', [
                ['13', 'וְהוּא֙ לֹ֣א יָדַ֔ע … (Jdg 16:20)',     '', '', '', ''],
                ['14', 'הֲ/שֹׁמֵ֥ר אָחִ֖י אָנֹֽכִי (Gen 4:9b)', '', '', '', ''],
                ['15', 'אָנֹכִ֖י יְהוָ֣ה אֱלֹהֶ֑יךָ (Exo 20:2)', '', '', '', ''],
            ], [
                ['13', 'וְהוּא֙ לֹ֣א יָדַ֔ע …',     'Waw-disjunctive (Contrast)',   'הוּא (pronoun)',             'יָדַ֔ע — Qal Perfect 3ms', 'but he did not know the LORD had left him'],
                ['14', 'הֲ/שֹׁמֵ֥ר אָחִ֖י אָנֹֽכִי', 'Verbless (interrogative)',    'שֹׁמֵ֥ר (pred. ptc.) + ה interrogative', 'None (verbless)', 'Am I my brother\'s keeper?'],
                ['15', 'אָנֹכִ֖י יְהוָ֣ה אֱלֹהֶ֑יךָ', 'Verbless (identity)',        'None', 'None', 'I am the LORD your God'],
            ]),
        ]

        for title, rows, ans in passages:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=False)
            self.add_section_break()

        self.add_section_heading('Answer Key')
        for title, rows, ans in passages:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=True, answer_rows=ans)
            self.add_section_break()


def build_ch23_passage_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch23PassageExercise,
        'Chapter 23 — Passage Exercise: Reading the Clause in Context',
        'BBH Chapter 23',
        ['hebrew', 'bbh', 'ch23', 'exercises', 'ch23-passage-exercise'],
        'ch23-passage-exercise.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 28 — Hophal Semantic Function Sorting
# ---------------------------------------------------------------------------


class Ch28FunctionSortExercise(ExercisePDF):
    _ENTRIES = [
        SortEntry('1',  'יֻּגַּד',   'Wayyiqtol 3ms',       'Gen 22:20',  '"it was told to Abraham"',                              'SR', 'נָגַד', 'Hophal of Hiphil "to tell"; information was reported'),
        SortEntry('2',  'יּוּשַׂם',  'Wayyiqtol 3ms',       'Gen 24:33',  '"food was set before him"',                             'SC', 'שִׂים',  'Caused to be placed/set; resulting state prominent'),
        SortEntry('3',  'הוּרַד',    'Qatal 3ms',            'Gen 39:1',   '"he had been brought down to Egypt"',                   'PT', 'יָרַד', 'Joseph physically moved; Hiphil = to bring down'),
        SortEntry('4',  'הֻבָּאת',   'Qatal 3fs',            'Gen 33:11',  '"it was brought to him"',                               'PT', 'בּוֹא', 'The gift was physically carried to Jacob'),
        SortEntry('5',  'הוּשַׁב',   'Qatal 3ms',            'Gen 42:28',  '"it has been returned into my sack"',                   'SC', 'שׁוּב', 'Silver caused to return; state of being-back prominent'),
        SortEntry('6',  'הוּבְאוּ',  'Qatal 3cp',            'Gen 43:18',  '"we were brought in (to Joseph\'s house)"',             'PT', 'בּוֹא', 'Brothers physically moved into the house'),
        SortEntry('7',  'יֻּגַּד',   'Wayyiqtol 3ms',       'Gen 38:13',  '"it was told to Tamar"',                                'SR', 'נָגַד', 'News of Judah\'s widowhood reported'),
        SortEntry('8',  'יֻּגַּד',   'Wayyiqtol 3ms',       'Gen 38:24',  '"it was told to Judah"',                                'SR', 'נָגַד', 'News of Tamar\'s pregnancy reported'),
        SortEntry('9',  'יֻּגַּד',   'Wayyiqtol 3ms',       'Gen 27:42',  '"it was told to Rebekah"',                              'SR', 'נָגַד', 'Esau\'s threat reported to Rebekah'),
        SortEntry('10', 'יוּמַת',    'Yiqtol 3ms',          'Gen 26:11',  '"he shall be put to death"',                            'LF', 'מוּת',  'Capital penalty formula; Hophal of Hiphil "to kill"'),
        SortEntry('11', 'יוּמַת',    'Yiqtol 3ms',          'Exo 19:12',  '"he shall be put to death"',                            'LF', 'מוּת',  'Sinai boundary violation penalty formula'),
        SortEntry('12', 'יוּמַת',    'Yiqtol 3ms',          'Exo 21:12',  '"he must be put to death"',                             'LF', 'מוּת',  'Murder law capital formula (Exo 21:12)'),
        SortEntry('13', 'יוּמַת',    'Yiqtol 3ms',          'Exo 21:15',  '"he must be put to death"',                             'LF', 'מוּת',  'Violence-against-parents capital formula'),
        SortEntry('14', 'יֻּכּוּ',   'Wayyiqtol 3mp',       'Exo 5:14',   '"the Israelite overseers were beaten"',                 'SA', 'נָכָה', 'Root נָכָה has no functional Qal; Hiphil is standard form'),
        SortEntry('15', 'מֻכִּים',   'Participle mp',       'Exo 5:16',   '"your servants are being beaten"',                      'SA', 'נָכָה', 'Participle of same SA root; ongoing state of being struck'),
        SortEntry('16', 'יוּסַר',    'Yiqtol 3ms',          'Lev 4:35',   '"it is to be removed"',                                 'SC', 'סוּר',  'Fat portions prescribed to enter state of removal'),
        SortEntry('17', 'הוּסַר',    'Qatal 3ms',           'Lev 4:31',   '"it was removed"',                                      'SC', 'סוּר',  'Fat portions caused to depart from offering'),
        SortEntry('18', 'הוּבָא',    'Weqatal 3ms',         'Lev 14:2',   '"he will be brought to the priest"',                    'PT', 'בּוֹא', 'The healed leper physically brought to priest'),
        SortEntry('19', 'יוּמַת',    'Yiqtol 3ms',          'Num 18:7',   '"he shall be put to death"',                            'LF', 'מוּת',  'Tabernacle-service intrusion penalty formula'),
        SortEntry('20', 'יֻּגַּד',   'Wayyiqtol 3ms',       'Exo 14:5',   '"it was told to the king of Egypt"',                    'SR', 'נָגַד', 'Israel\'s flight reported to Pharaoh'),
        SortEntry('21', 'הוּקַם',    'Qatal 3ms',           'Exo 40:17',  '"the tabernacle was set up"',                           'SC', 'קוּם',  'Caused to stand/erect; state of being established'),
        SortEntry('22', 'יוּשַׁב',   'Wayyiqtol 3ms',       'Exo 10:8',   '"Moses and Aaron were brought back"',                   'SC', 'שׁוּב', 'Caused to return to Pharaoh; state of return prominent'),
        SortEntry('23', 'הוּחַל',    'Qatal 3ms',           'Gen 4:26',   '"it was begun (to call on the LORD\'s name)"',          'SC', 'חָלַל', 'Worship practice caused to enter state of being begun'),
        SortEntry('24', 'הוּגַּד',   'Qatal 3ms',           'Exo 26:30',  '"you were shown the pattern of the tabernacle"',        'SR', 'נָגַד', 'The heavenly pattern was reported/revealed to Moses'),
        SortEntry('25', 'מוּמָת',    'Inf. Construct',      'Num 35:16',  '"the murderer must be put to death"',                   'LF', 'מוּת',  'Hophal infinitive in the capital penalty nominal clause'),
    ]

    def _build(self) -> None:
        self.add_instructions(
            'Classify each Hophal verb by semantic function: PT (Physical Transfer), LF (Legal Formula), '
            'SR (Speech Reporting), SC (State Change), or SA (Simple Action). '
            'Write your code in the Function column. Answer key is on the last page.'
        )
        self.add_note(
            'PT = Physical Transfer (subject was moved/brought/taken)  |  '
            'LF = Legal Formula (capital penalty: יוּמַת "shall be put to death")  |  '
            'SR = Speech Reporting (information was told/reported/shown)  |  '
            'SC = State Change (subject entered a new state: set up, returned, begun)  |  '
            'SA = Simple Action (no functional Qal; Hiphil is standard form)'
        )
        self.add_sort_table(self._ENTRIES, show_answers=False)
        self.add_reflection([
            'The יוּמַת formula (items 10–13, 19) appears in five different legal contexts. '
            'What does the repetition signal about the Hophal\'s role in Mosaic law?',
            'Items 1, 7–9, 20, 24 all use root נָגַד. Why is this root almost always in the Hophal '
            'for "was told"? (Hint: the Hiphil means "to tell/report.")',
            'Items 16–17 are both from סוּר in Lev 4. One is Qatal, one is Yiqtol. '
            'What does the conjugation difference signal about time or prescription?',
        ])
        self.add_answer_key_sort(self._ENTRIES)


def build_ch28_function_sort_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch28FunctionSortExercise,
        'Chapter 28 — Hophal Semantic Function Sorting',
        'BBH Chapter 28 · Hophal Strong Verbs',
        ['hebrew', 'bbh', 'ch28', 'exercises', 'ch28-function-sort'],
        'ch28-function-sort.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 28 — Hiphil–Hophal Contrast Drill
# ---------------------------------------------------------------------------


class Ch28HophalHiphilContrastExercise(ExercisePDF):

    def _build(self) -> None:
        self.add_instructions(
            'Part A: 8 Hophal forms — translate and name the corresponding Hiphil meaning. '
            'Part B: 4 מוּת pairs — identify Hiphil vs. Hophal and translate. '
            'Answer key is on the last page.'
        )
        self.add_note(
            'Hophal prefix vowel: קֻּ (strong/I-gutt); וּ (I-yod/Biconsonantal). '
            'Hiphil prefix vowel: הִ (perfect); הַ (imperative); מַ (participle). '
            'Biconsonantal: Hiphil perfect הֵ / Hophal perfect הוּ — one vowel distinguishes them.'
        )

        hdr_a = ['#', 'Form', 'Conjugation', 'Ref', 'Gloss (blank)', 'Translation', 'Stem']
        cr_a  = [0.05, 0.13, 0.14, 0.09, 0.28, 0.18, 0.13]
        rows_a = [
            ['1', 'הוּבְאוּ',  'Qatal 3cp',       'Gen 43:18', '"we were ___"',                 '', ''],
            ['2', 'הוּרַד',    'Qatal 3ms',        'Gen 39:1',  '"he had been ___ to Egypt"',    '', ''],
            ['3', 'הוּשַׁב',   'Qatal 3ms',        'Gen 42:28', '"it has been ___"',             '', ''],
            ['4', 'הוּקַם',    'Qatal 3ms',        'Exo 40:17', '"the tabernacle was ___"',      '', ''],
            ['5', 'יֻּגַּד',   'Wayyiqtol 3ms',   'Gen 22:20', '"it was ___"',                  '', ''],
            ['6', 'יּוּשַׂם',  'Wayyiqtol 3ms',   'Gen 24:33', '"food was ___"',                '', ''],
            ['7', 'הוּסַר',    'Qatal 3ms',        'Lev 4:31',  '"it was ___"',                  '', ''],
            ['8', 'יוּשַׁב',   'Wayyiqtol 3ms',   'Exo 10:8',  '"Moses was ___"',               '', ''],
        ]
        ans_a = [
            ['1', 'הוּבְאוּ',  'Qatal 3cp',       'Gen 43:18', '"we were brought in"',         'they were brought',  'Hophal (בּוֹא)'],
            ['2', 'הוּרַד',    'Qatal 3ms',        'Gen 39:1',  '"he had been brought down"',   'was brought down',   'Hophal (יָרַד)'],
            ['3', 'הוּשַׁב',   'Qatal 3ms',        'Gen 42:28', '"it has been returned"',       'was returned',       'Hophal (שׁוּב)'],
            ['4', 'הוּקַם',    'Qatal 3ms',        'Exo 40:17', '"the tabernacle was set up"',  'was set up',         'Hophal (קוּם)'],
            ['5', 'יֻּגַּד',   'Wayyiqtol 3ms',   'Gen 22:20', '"it was told"',                'it was told',        'Hophal (נָגַד)'],
            ['6', 'יּוּשַׂם',  'Wayyiqtol 3ms',   'Gen 24:33', '"food was set before him"',    'it was set/placed',  'Hophal (שִׂים)'],
            ['7', 'הוּסַר',    'Qatal 3ms',        'Lev 4:31',  '"it was removed"',             'was removed',        'Hophal (סוּר)'],
            ['8', 'יוּשַׁב',   'Wayyiqtol 3ms',   'Exo 10:8',  '"Moses was brought back"',     'was brought back',   'Hophal (שׁוּב)'],
        ]
        self.add_section_heading('Part A — Motion and Transfer Roots')
        self.add_generic_table(hdr_a, rows_a, cr_a, heb_cols=[1], show_answers=False)
        self.add_section_break()

        hdr_b = ['#', 'Form', 'Stem', 'Conj.', 'Ref', 'Translation']
        cr_b  = [0.05, 0.16, 0.12, 0.16, 0.14, 0.37]
        rows_b = [
            ['9',  'הֵמִית',   '', 'Inf. Construct', 'Gen 18:25', ''],
            ['10', 'יוּמַת',   '', 'Yiqtol 3ms',     'Gen 26:11', ''],
            ['11', 'הָמִית',   '', 'Qatal 3ms',       '2 Sam 12:9', ''],
            ['12', 'הוּמַת',   '', 'Qatal 3ms',       '2 Sam 21:9', ''],
        ]
        ans_b = [
            ['9',  'הֵמִית',   'Hiphil', 'Inf. Construct', 'Gen 18:25',   'to put to death; הֵ prefix = Hiphil Bicons.'],
            ['10', 'יוּמַת',   'Hophal', 'Yiqtol 3ms',     'Gen 26:11',  'shall be put to death; וּ prefix = Hophal'],
            ['11', 'הָמִית',   'Hiphil', 'Qatal 3ms',       '2 Sam 12:9', 'he killed; הֵ → הָ (alternate vocalization)'],
            ['12', 'הוּמַת',   'Hophal', 'Qatal 3ms',       '2 Sam 21:9', 'he was put to death; הוּ = Hophal perfect'],
        ]
        self.add_section_heading('Part B — מוּת: Hiphil / Hophal Pairs')
        self.add_generic_table(hdr_b, rows_b, cr_b, heb_cols=[1], show_answers=False)
        self.add_section_break()

        self.add_reflection([
            'In Part A, every Hophal form uses a וּ (shureq) prefix vowel. Explain why '
            'I-yod and Biconsonantal roots take shureq instead of the usual qibbuts.',
            'Items 9–12 are all from מוּת. Write the prefix vowel pattern that '
            'distinguishes Hiphil perfect (הֵמִית) from Hophal qatal (הוּמַת). '
            'What is the one vowel that differs?',
        ])

        self.add_section_heading('Answer Key — Part A')
        self.add_generic_table(hdr_a, rows_a, cr_a, heb_cols=[1],
                               show_answers=True, answer_rows=ans_a)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part B')
        self.add_generic_table(hdr_b, rows_b, cr_b, heb_cols=[1],
                               show_answers=True, answer_rows=ans_b)


def build_ch28_hophal_hiphil_contrast_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch28HophalHiphilContrastExercise,
        'Chapter 28 — Hiphil–Hophal Contrast Drill',
        'BBH Chapter 28 · Hophal Strong Verbs',
        ['hebrew', 'bbh', 'ch28', 'exercises', 'ch28-hophal-hiphil-contrast'],
        'ch28-hophal-hiphil-contrast.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 29 — Hophal Weak-Form Identification Drill
# ---------------------------------------------------------------------------


class Ch29WeakFormIdExercise(ExercisePDF):

    def _build(self) -> None:
        self.add_instructions(
            'Part A: identify conjugation, PGN, and root for each form (grouped by weak class). '
            'Part B: identify the weak class first, then conjugation, PGN, and root. '
            'Answer key is on the last page.'
        )
        self.add_note(
            'I-yod/Biconsonantal Hophal: uses וּ (shureq) not קֻּ.  '
            'I-nun: dagesh forte in R2 (nun assimilated).  '
            'III-he: ending ָה (qatal 3ms) or וּ (3cp).  '
            'I-guttural: hateph vowel under R1 instead of simple shewa.'
        )

        hdr = ['#', 'Form', 'Reference', 'Conjugation', 'PGN', 'Root']
        cr  = [0.05, 0.16, 0.14, 0.20, 0.10, 0.35]

        groups = [
            ('Group 1: I-yod / I-vav', [
                ['1', 'הוּרַד',    'Gen 39:1',  '', '', ''],
                ['2', 'הוּבָא',    'Lev 14:2',  '', '', ''],
                ['3', 'מוּבָאִים', 'Gen 43:18', '', '', ''],
                ['4', 'הוּבְאוּ',  'Gen 43:18', '', '', ''],
                ['5', 'מוּצֵאת',   'Gen 38:25', '', '', ''],
            ], [
                ['1', 'הוּרַד',    'Gen 39:1',  'Qatal',     '3ms', 'יָרַד · holem-vav prefix = I-yod Hophal'],
                ['2', 'הוּבָא',    'Lev 14:2',  'Weqatal',   '3ms', 'בּוֹא · holem-vav prefix = I-yod/Hollow'],
                ['3', 'מוּבָאִים', 'Gen 43:18', 'Participle', 'mp', 'בּוֹא · מוּ prefix (not מַ) = I-yod Hophal ptc'],
                ['4', 'הוּבְאוּ',  'Gen 43:18', 'Qatal',     '3cp', 'בּוֹא · holem-vav + plural וּ ending'],
                ['5', 'מוּצֵאת',   'Gen 38:25', 'Participle', 'fs', 'יָצָא · מוּ prefix + fs ת ending'],
            ]),
            ('Group 2: Biconsonantal (Hollow)', [
                ['6',  'הוּקַם',  'Exo 40:17', '', '', ''],
                ['7',  'יוּמַת',  'Gen 26:11', '', '', ''],
                ['8',  'הוּסַר',  'Lev 4:31',  '', '', ''],
                ['9',  'הוּשַׁב', 'Gen 42:28', '', '', ''],
                ['10', 'יּוּשַׂם', 'Gen 24:33', '', '', ''],
            ], [
                ['6',  'הוּקַם',  'Exo 40:17', 'Qatal',      '3ms', 'קוּם · הוּ prefix = Hophal Bicons. perfect'],
                ['7',  'יוּמַת',  'Gen 26:11', 'Yiqtol',     '3ms', 'מוּת · יוּ prefix = Hophal Bicons. imperfect'],
                ['8',  'הוּסַר',  'Lev 4:31',  'Qatal',      '3ms', 'סוּר · הוּ prefix; root סוּר'],
                ['9',  'הוּשַׁב', 'Gen 42:28', 'Qatal',      '3ms', 'שׁוּב · הוּ prefix; root שׁוּב'],
                ['10', 'יּוּשַׂם', 'Gen 24:33', 'Wayyiqtol',  '3ms', 'שִׂים · וַיּוּ prefix (dagesh in יּ) = Wayyiqtol'],
            ]),
            ('Group 3: I-nun', [
                ['11', 'יֻּגַּד',  'Gen 22:20', '', '', ''],
                ['12', 'יֻּגַּד',  'Gen 38:13', '', '', ''],
                ['13', 'יֻּכּוּ',  'Exo 5:14',  '', '', ''],
                ['14', 'מֻכִּים', 'Exo 5:16',  '', '', ''],
                ['15', 'יֻקָּם',  'Gen 4:15',  '', '', ''],
            ], [
                ['11', 'יֻּגַּד',  'Gen 22:20', 'Wayyiqtol', '3ms', 'נָגַד · nun assimilated; dagesh in ג'],
                ['12', 'יֻּגַּד',  'Gen 38:13', 'Wayyiqtol', '3ms', 'נָגַד · same form/root; different context'],
                ['13', 'יֻּכּוּ',  'Exo 5:14',  'Wayyiqtol', '3mp', 'נָכָה · I-nun + III-he; dagesh in כּ; plural וּ'],
                ['14', 'מֻכִּים', 'Exo 5:16',  'Participle', 'mp', 'נָכָה · qibbuts under מ + dagesh in כּ = Hophal ptc I-nun/III-he'],
                ['15', 'יֻקָּם',  'Gen 4:15',  'Yiqtol',    '3ms', 'נָקַם · nun assimilated; dagesh in ק'],
            ]),
            ('Group 4: III-he', [
                ['16', 'הֻגְלוּ',   'Jer 29:1',  '', '', ''],
                ['17', 'הֻלֶּדֶת', 'Gen 40:20', '', '', ''],
                ['18', 'מוּכָּה',  'Deu 28:27', '', '', ''],
                ['19', 'הֻבָּאת',  'Gen 33:11', '', '', ''],
                ['20', 'יֻּכֶּה',   'Exo 22:1',  '', '', ''],
            ], [
                ['16', 'הֻגְלוּ',   'Jer 29:1',  'Qatal',      '3cp', 'גָּלָה · III-he qibbuts; וּ ending 3cp'],
                ['17', 'הֻלֶּדֶת', 'Gen 40:20', 'Inf. Construct', '—', 'יָלַד · I-nun + III-he; inf. constr. ת ending'],
                ['18', 'מוּכָּה',  'Deu 28:27', 'Participle', 'fs', 'נָכָה · מוּ + dagesh + III-he ָה ptc fs = Hophal'],
                ['19', 'הֻבָּאת',  'Gen 33:11', 'Qatal',      '3fs', 'בּוֹא · I-yod + qibbuts; 3fs ת ending'],
                ['20', 'יֻּכֶּה',   'Exo 22:1',  'Yiqtol',    '3ms', 'נָכָה · I-nun + III-he; seghol + ה = III-he yiqtol'],
            ]),
        ]

        for title, rows, ans in groups:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1], show_answers=False)
            self.add_section_break()

        hdr_b = ['#', 'Form', 'Reference', 'Weak Class', 'Conjugation', 'PGN', 'Root']
        cr_b  = [0.04, 0.14, 0.12, 0.18, 0.17, 0.09, 0.26]
        rows_b = [
            ['21', 'יֻּגַּד',   'Gen 38:24', '', '', '', ''],
            ['22', 'הוּסַר',    'Lev 4:35',  '', '', '', ''],
            ['23', 'יוּמַת',    'Exo 21:12', '', '', '', ''],
            ['24', 'מוּבָאִים', 'Gen 43:18', '', '', '', ''],
            ['25', 'הוּבָא',    'Lev 14:2',  '', '', '', ''],
            ['26', 'הוּחַל',    'Gen 4:26',  '', '', '', ''],
            ['27', 'יֻּכּוּ',   'Exo 5:14',  '', '', '', ''],
            ['28', 'הוּקַם',    'Exo 40:17', '', '', '', ''],
            ['29', 'הֻגְלוּ',   'Jer 29:1',  '', '', '', ''],
            ['30', 'יֻקָּם',    'Gen 4:15',  '', '', '', ''],
        ]
        ans_b = [
            ['21', 'יֻּגַּד',   'Gen 38:24', 'I-nun',          'Wayyiqtol',  '3ms', 'נָגַד'],
            ['22', 'הוּסַר',    'Lev 4:35',  'Biconsonantal',  'Yiqtol',     '3ms', 'סוּר'],
            ['23', 'יוּמַת',    'Exo 21:12', 'Biconsonantal',  'Yiqtol',     '3ms', 'מוּת'],
            ['24', 'מוּבָאִים', 'Gen 43:18', 'I-yod',          'Participle', 'mp',  'בּוֹא'],
            ['25', 'הוּבָא',    'Lev 14:2',  'I-yod',          'Weqatal',    '3ms', 'בּוֹא'],
            ['26', 'הוּחַל',    'Gen 4:26',  'I-guttural',     'Qatal',      '3ms', 'חָלַל'],
            ['27', 'יֻּכּוּ',   'Exo 5:14',  'I-nun + III-he', 'Wayyiqtol',  '3mp', 'נָכָה'],
            ['28', 'הוּקַם',    'Exo 40:17', 'Biconsonantal',  'Qatal',      '3ms', 'קוּם'],
            ['29', 'הֻגְלוּ',   'Jer 29:1',  'III-he',         'Qatal',      '3cp', 'גָּלָה'],
            ['30', 'יֻקָּם',    'Gen 4:15',  'I-nun',          'Yiqtol',     '3ms', 'נָקַם'],
        ]

        self.add_section_heading('Part B — Mixed Forms')
        self.add_generic_table(hdr_b, rows_b, cr_b, heb_cols=[1], show_answers=False)
        self.add_section_break()

        self.add_reflection([
            'I-yod and Biconsonantal Hophal forms both use וּ (shureq). What phonological '
            'rule explains this? Compare the Hiphil of the same classes (I-yod uses הוֹ; '
            'Biconsonantal uses הֵ).',
            'I-nun forms (items 11–15) have dagesh forte in R2. What happened to the נ? '
            'Is this the same assimilation as in the Qal/Hiphil of I-nun roots?',
            'Items 13 and 20 are both from נָכָה (I-nun + III-he). One is wayyiqtol 3mp, '
            'the other yiqtol 3ms. Compare their endings. Where did the III-he ה go in item 13?',
        ])

        self.add_section_heading('Answer Key — Part A')
        for title, rows, ans in groups:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=True, answer_rows=ans)
            self.add_section_break()

        self.add_section_heading('Answer Key — Part B')
        self.add_generic_table(hdr_b, rows_b, cr_b, heb_cols=[1],
                               show_answers=True, answer_rows=ans_b)


def build_ch29_weak_form_id_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch29WeakFormIdExercise,
        'Chapter 29 — Hophal Weak-Form Identification Drill',
        'BBH Chapter 29 · Hophal Weak Verbs',
        ['hebrew', 'bbh', 'ch29', 'exercises', 'ch29-weak-form-id'],
        'ch29-weak-form-id.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 30 — Piel Semantic Function Sorting
# ---------------------------------------------------------------------------


class Ch30FunctionSortExercise(ExercisePDF):
    _ENTRIES = [
        SortEntry('1',  'יְבָרֶךְ',     'Wayyiqtol 3ms',    'Gen 1:22',  '"God blessed them"',                              'SA', 'בָּרַךְ', 'Piel is the primary form; no intensified Qal counterpart'),
        SortEntry('2',  'יְקַדֵּשׁ',    'Wayyiqtol 3ms',    'Gen 2:3',   '"he set it apart as holy"',                       'F',  'קָדַשׁ', 'Qal = be holy; Piel = cause to be holy (factitive)'),
        SortEntry('3',  'יְכַל',         'Wayyiqtol 3ms',    'Gen 2:2',   '"he finished"',                                   'I',  'כָּלָה', 'Thorough completion; Qal = be complete'),
        SortEntry('4',  'שַׁחֵת',        'Inf. Construct',   'Gen 6:17',  '"to destroy utterly"',                            'I',  'שָׁחַת', 'Total/thorough destruction; intensive force'),
        SortEntry('5',  'יְצַו',         'Wayyiqtol 3ms',    'Gen 2:16',  '"he commanded"',                                  'SA', 'צָוָה',  'Piel is the standard form; Qal is marginal'),
        SortEntry('6',  'יְגָרֶשׁ',     'Wayyiqtol 3ms',    'Gen 3:24',  '"he drove out forcibly"',                         'I',  'גָּרַשׁ', 'Forcible expulsion; more intensive than basic Qal'),
        SortEntry('7',  'חַיּוֹת',       'Inf. Construct',   'Gen 7:3',   '"to preserve alive"',                             'F',  'חָיָה',  'Qal = live; Piel = cause to be alive (factitive)'),
        SortEntry('8',  'יְשַׁלַּח',    'Wayyiqtol 3ms',    'Gen 8:7',   '"he sent out / released"',                        'I',  'שָׁלַח', 'Release/send away with force; Qal = send'),
        SortEntry('9',  'יְכַסּוּ',     'Wayyiqtol 3mp',    'Gen 9:23',  '"they thoroughly covered"',                       'I',  'כָּסָה', 'Thorough covering; Qal = cover'),
        SortEntry('10', 'יְדַבֵּר',     'Wayyiqtol 3ms',    'Gen 8:15',  '"he spoke"',                                      'SA', 'דָּבַר', 'Piel is standard form for "to speak"; Qal is rare'),
        SortEntry('11', 'יְשָׁרֶת',     'Wayyiqtol 3ms',    'Gen 39:4',  '"he served"',                                     'SA', 'שָׁרַת', 'Piel is primary form; denominative from שֵׁרוּת'),
        SortEntry('12', 'אֲגַדְּלָה',   'Yiqtol 1cs',       'Gen 12:2',  '"I will make great"',                             'F',  'גָּדַל', 'Qal = be great; Piel = cause to be great (factitive)'),
        SortEntry('13', 'מְקַלֵּל',     'Participle ms',    'Gen 12:3',  '"one who curses"',                                'D',  'קָלַל',  'Qal = be light/small; Piel = declare accursed'),
        SortEntry('14', 'יְנַגַּע',     'Wayyiqtol 3ms',    'Gen 12:17', '"he struck / afflicted"',                         'I',  'נָגַע',  'Intensive striking/affliction; more severe than Qal'),
        SortEntry('15', 'וְקִדַּשְׁתָּ', 'Weqatal 2ms',     'Exo 19:10', '"you shall consecrate them"',                     'F',  'קָדַשׁ', 'Cause the people to be in a holy state'),
        SortEntry('16', 'וְכִבְּסוּ',   'Weqatal 3cp',      'Exo 19:10', '"and they shall wash their garments"',            'I',  'כָּבַס', 'Thorough washing; Qal of כָּבַס is rare'),
        SortEntry('17', 'יְהַלֲלוּ',   'Wayyiqtol 3mp',    'Gen 12:15', '"they praised her"',                              'SA', 'הָלַל',  'Piel is standard form for "to praise"'),
        SortEntry('18', 'יְבַקֵּשׁ',    'Wayyiqtol 3ms',    'Gen 37:15', '"he sought"',                                     'I',  'בָּקַשׁ', 'Diligent/intensive seeking'),
        SortEntry('19', 'לְנַחֵם',      'Inf. Construct',   'Gen 37:35', '"to comfort him"',                                'I',  'נָחַם',  'Active comforting; Niphal = be comforted'),
        SortEntry('20', 'צִוָּה',        'Perfect 3ms',      'Gen 6:22',  '"he commanded"',                                  'SA', 'צָוָה',  'Same root as #5; Piel is the operative form'),
        SortEntry('21', 'לְכַפֵּר',     'Inf. Construct',   'Lev 4:20',  '"to make atonement"',                             'DN', 'כָּפַר', 'From כֹּפֶר "ransom/covering"; denominative function'),
        SortEntry('22', 'יְחַלֵּל',     'Wayyiqtol 3ms',    'Lev 21:12', '"he would profane"',                              'F',  'חָלַל',  'Qal = be profane; Piel = cause to be profane'),
        SortEntry('23', 'בִּקֵּשׁ',     'Perfect 3ms',      'Gen 43:30', '"he sought"',                                     'I',  'בָּקַשׁ', 'Same root as #18; intensive seeking'),
        SortEntry('24', 'יְנַחֵם',      'Yiqtol 3ms',       'Gen 5:29',  '"he will comfort us"',                            'SA', 'נָחַם',  'Active sense; Niphal = relent/be comforted; Piel = comfort'),
        SortEntry('25', 'לְהַלֵּל',     'Inf. Construct',   'Psa 113:1', '"to praise"',                                     'SA', 'הָלַל',  'Standard form for praise; same root as #17'),
    ]

    def _build(self) -> None:
        self.add_instructions(
            'Classify each Piel verb: I (Intensive), F (Factitive), D (Declarative), '
            'DN (Denominative), or SA (Simple Action). '
            'Answer key is on the last page.'
        )
        self.add_note(
            'I = Intensive (more forceful/thorough than Qal)  |  '
            'F = Factitive (causes object to be in a state; from stative root)  |  '
            'D = Declarative (declares/treats something as being in a state)  |  '
            'DN = Denominative (derived from a noun; performs noun\'s action)  |  '
            'SA = Simple Action (Piel is primary form; no productive Qal)'
        )
        self.add_sort_table(self._ENTRIES, show_answers=False)
        self.add_reflection([
            'Items 1, 5, 10, 17, 20, 24 are all SA. What do these roots share? '
            'Why does "intensification of the Qal" not work for them?',
            'Items 2, 7, 12, 15, 22 are all Factitive. For each root, name the '
            'Qal stative meaning and explain how the Piel "causes" that state.',
            'Item 21 (לְכַפֵּר): if this is Denominative, what noun is it from? '
            'How does knowing that noun illuminate its meaning in Lev 4:20?',
        ])
        self.add_answer_key_sort(self._ENTRIES)


def build_ch30_function_sort_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch30FunctionSortExercise,
        'Chapter 30 — Piel Semantic Function Sorting',
        'BBH Chapter 30 · Piel Strong Verbs',
        ['hebrew', 'bbh', 'ch30', 'exercises', 'ch30-function-sort'],
        'ch30-function-sort.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 30 — Qal–Piel Contrast Drill
# ---------------------------------------------------------------------------


class Ch30QalPielContrastExercise(ExercisePDF):

    def _build(self) -> None:
        self.add_instructions(
            'Part A: Intensive Piel forms — translate and name the function. '
            'Part B: Factitive Piel forms from stative roots. '
            'Part C: Declarative / Denominative / SA. '
            'Answer key is on the last page.'
        )
        self.add_note(
            'Test for Intensive: does the subject do the action more forcefully/thoroughly? '
            'Test for Factitive: does the subject cause an object to enter a state? '
            'Test for Declarative: does the subject pronounce/treat something as X?'
        )

        hdr = ['#', 'Root', 'Qal Meaning', 'Piel Form', 'Ref', 'Translation', 'Function']
        cr  = [0.04, 0.09, 0.16, 0.14, 0.09, 0.25, 0.23]

        rows_a = [
            ['1',  'שָׁבַר', 'to break',      'שִׁבֵּר (Perfect 3ms)',    'Exo 32:19', '', ''],
            ['2',  'כָּסָה', 'to cover',      'יְכַסּוּ (Wayy. 3mp)',     'Gen 9:23',  '', ''],
            ['3',  'שָׁלַח', 'to send',       'יְשַׁלַּח (Wayy. 3ms)',    'Gen 8:7',   '', ''],
            ['4',  'גָּרַשׁ', 'to drive out', 'יְגָרֶשׁ (Wayy. 3ms)',     'Gen 3:24',  '', ''],
            ['5',  'שָׁחַת', 'to corrupt',    'שַׁחֵת (Inf. Constr.)',     'Gen 6:17',  '', ''],
            ['6',  'כָּבַס', '(Qal rare)',    'וְכִבְּסוּ (Weq. 3cp)',    'Exo 19:10', '', ''],
            ['7',  'בָּקַשׁ', '(Qal rare)',   'יְבַקֵּשׁ (Wayy. 3ms)',    'Gen 37:15', '', ''],
        ]
        ans_a = [
            ['1',  'שָׁבַר', 'to break',      'שִׁבֵּר (Perfect 3ms)',    'Exo 32:19', 'smashed to pieces',        'I — thorough breaking'],
            ['2',  'כָּסָה', 'to cover',      'יְכַסּוּ (Wayy. 3mp)',     'Gen 9:23',  'they thoroughly covered',   'I — complete coverage'],
            ['3',  'שָׁלַח', 'to send',       'יְשַׁלַּח (Wayy. 3ms)',    'Gen 8:7',   'he sent out (released)',    'I — release/send away'],
            ['4',  'גָּרַשׁ', 'to drive out', 'יְגָרֶשׁ (Wayy. 3ms)',     'Gen 3:24',  'he drove out forcibly',     'I — forcible expulsion'],
            ['5',  'שָׁחַת', 'to corrupt',    'שַׁחֵת (Inf. Constr.)',     'Gen 6:17',  'to destroy utterly',        'I — total destruction'],
            ['6',  'כָּבַס', '(Qal rare)',    'וְכִבְּסוּ (Weq. 3cp)',    'Exo 19:10', 'they shall wash',           'I — thorough washing; SA also acceptable'],
            ['7',  'בָּקַשׁ', '(Qal rare)',   'יְבַקֵּשׁ (Wayy. 3ms)',    'Gen 37:15', 'he sought diligently',      'I — intensive searching'],
        ]

        rows_b = [
            ['8',  'קָדַשׁ', 'to be holy',    'יְקַדֵּשׁ (Wayy. 3ms)',    'Gen 2:3',   '', ''],
            ['9',  'גָּדַל', 'to be great',   'אֲגַדְּלָה (Yiqtol 1cs)',  'Gen 12:2',  '', ''],
            ['10', 'חָיָה', 'to live',        'חַיּוֹת (Inf. Constr.)',    'Gen 7:3',   '', ''],
            ['11', 'חָלַל', 'to be profane',  'יְחַלֵּל (Wayy. 3ms)',     'Lev 21:12', '', ''],
            ['12', 'כָּלָה', 'to be complete','יְכַל (Wayy. 3ms)',         'Gen 2:2',   '', ''],
        ]
        ans_b = [
            ['8',  'קָדַשׁ', 'to be holy',    'יְקַדֵּשׁ (Wayy. 3ms)',    'Gen 2:3',   'he sanctified',             'F — caused to be holy'],
            ['9',  'גָּדַל', 'to be great',   'אֲגַדְּלָה (Yiqtol 1cs)',  'Gen 12:2',  'I will make great',         'F — cause to be great'],
            ['10', 'חָיָה', 'to live',        'חַיּוֹת (Inf. Constr.)',    'Gen 7:3',   'to preserve alive',         'F — cause to be alive'],
            ['11', 'חָלַל', 'to be profane',  'יְחַלֵּל (Wayy. 3ms)',     'Lev 21:12', 'he would profane',          'F — cause to be profane'],
            ['12', 'כָּלָה', 'to be complete','יְכַל (Wayy. 3ms)',         'Gen 2:2',   'he completed/finished',     'F or I — cause completion'],
        ]

        rows_c = [
            ['13', 'קָלַל', 'to be small',  'מְקַלֵּל (Part. ms)',      'Gen 12:3',  '', ''],
            ['14', 'כָּפַר', '(to cover)',  'לְכַפֵּר (Inf. Constr.)',  'Lev 4:20',  '', ''],
            ['15', 'שָׁרַת', '(Qal rare)', 'יְשָׁרֶת (Wayy. 3ms)',     'Gen 39:4',  '', ''],
        ]
        ans_c = [
            ['13', 'קָלַל', 'to be small',  'מְקַלֵּל (Part. ms)',      'Gen 12:3',  'one who curses',             'D — declare accursed'],
            ['14', 'כָּפַר', '(to cover)',  'לְכַפֵּר (Inf. Constr.)',  'Lev 4:20',  'to make atonement',          'DN — from כֹּפֶר (ransom)'],
            ['15', 'שָׁרַת', '(Qal rare)', 'יְשָׁרֶת (Wayy. 3ms)',     'Gen 39:4',  'he served',                  'SA / DN — primary Piel form'],
        ]

        self.add_section_heading('Part A — Intensive Roots')
        self.add_generic_table(hdr, rows_a, cr, heb_cols=[3], show_answers=False)
        self.add_section_break()
        self.add_section_heading('Part B — Factitive Roots (Stative Qal)')
        self.add_generic_table(hdr, rows_b, cr, heb_cols=[3], show_answers=False)
        self.add_section_break()
        self.add_section_heading('Part C — Declarative / Denominative / SA')
        self.add_generic_table(hdr, rows_c, cr, heb_cols=[3], show_answers=False)
        self.add_section_break()

        self.add_reflection([
            'For Part A items 1–5, describe the pattern in one sentence: what does "Intensive" '
            'add to the Qal meaning?',
            'Part B: for items 8–12, write the stative Qal meaning and the Piel "factitive" meaning. '
            'What grammatical *object* does the Piel require that the Qal stative does not?',
            'Items 13–15: for each, explain in one sentence why "Intensive" does not fit.',
        ])

        self.add_section_heading('Answer Key — Part A')
        self.add_generic_table(hdr, rows_a, cr, heb_cols=[3],
                               show_answers=True, answer_rows=ans_a)
        self.add_section_heading('Answer Key — Part B')
        self.add_generic_table(hdr, rows_b, cr, heb_cols=[3],
                               show_answers=True, answer_rows=ans_b)
        self.add_section_heading('Answer Key — Part C')
        self.add_generic_table(hdr, rows_c, cr, heb_cols=[3],
                               show_answers=True, answer_rows=ans_c)


def build_ch30_qal_piel_contrast_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch30QalPielContrastExercise,
        'Chapter 30 — Qal–Piel Contrast Drill',
        'BBH Chapter 30 · Piel Strong Verbs',
        ['hebrew', 'bbh', 'ch30', 'exercises', 'ch30-qal-piel-contrast'],
        'ch30-qal-piel-contrast.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 31 — Piel Weak-Form Identification Drill
# ---------------------------------------------------------------------------


class Ch31WeakFormIdExercise(ExercisePDF):

    def _build(self) -> None:
        self.add_instructions(
            'Part A: identify conjugation, PGN, and root (forms grouped by weak class). '
            'Part B: identify weak class first, then conjugation, PGN, and root. '
            'Answer key is on the last page.'
        )
        self.add_note(
            'Piel diagnostic: Dagesh Forte in R2 (or compensatory lengthening when R2 = ר/ע/ח/ה/א). '
            'III-he: final ה drops in wayyiqtol/jussive (apocopation). '
            'I-nun: nun is RETAINED in the Piel (not assimilated). '
            'Geminate: Dagesh in doubled R2 is the Piel marker.'
        )

        hdr = ['#', 'Form', 'Reference', 'Conjugation', 'PGN', 'Root']
        cr  = [0.05, 0.18, 0.14, 0.22, 0.10, 0.31]

        groups = [
            ('Group 1: III-he', [
                ['1', 'יְכַל',       'Gen 2:2',   '', '', ''],
                ['2', 'יְצַו',       'Gen 2:16',  '', '', ''],
                ['3', 'צִוִּיתִי',   'Gen 3:11',  '', '', ''],
                ['4', 'יְחַיּוּ',   'Gen 12:12', '', '', ''],
                ['5', 'כִּלָּה',     'Gen 17:22', '', '', ''],
            ], [
                ['1', 'יְכַל',       'Gen 2:2',   'Wayyiqtol', '3ms', 'כָּלָה · apocopated (ה dropped); seghol'],
                ['2', 'יְצַו',       'Gen 2:16',  'Wayyiqtol', '3ms', 'צָוָה · apocopated; tsere under ו'],
                ['3', 'צִוִּיתִי',   'Gen 3:11',  'Qatal',     '1cs', 'צָוָה · qatal 1cs ending; chiriq-yod retained'],
                ['4', 'יְחַיּוּ',   'Gen 12:12', 'Yiqtol',    '3mp', 'חָיָה · yiqtol 3mp; ה replaced by וּ + dagesh'],
                ['5', 'כִּלָּה',     'Gen 17:22', 'Qatal',     '3ms', 'כָּלָה · qatal 3ms; qamets + ָה ending retained'],
            ]),
            ('Group 2: I-guttural', [
                ['6',  'עִנּוּ',      'Gen 15:13', '', '', ''],
                ['7',  'יְעַנֶּה',   'Exo 22:21', '', '', ''],
                ['8',  'עַנּוֹת',    'Exo 10:3',  '', '', ''],
                ['9',  'מְחַיֶּה',   'Neh 9:6',   '', '', ''],
                ['10', 'וַיְעַנּוּ', 'Exo 1:11',  '', '', ''],
            ], [
                ['6',  'עִנּוּ',      'Gen 15:13', 'Qatal',      '3cp', 'עָנָה · I-gutt (ע); composite shewa → simple; dagesh in נּ'],
                ['7',  'יְעַנֶּה',   'Exo 22:21', 'Yiqtol',     '3ms', 'עָנָה · I-gutt; hateph under ע; seghol + ה (III-he)'],
                ['8',  'עַנּוֹת',    'Exo 10:3',  'Inf. Constr.', '—', 'עָנָה · I-gutt; inf. construct ending וֹת'],
                ['9',  'מְחַיֶּה',   'Neh 9:6',   'Participle', 'ms', 'חָיָה · I-gutt (ח) + III-he; seghol + ה ptc ending'],
                ['10', 'וַיְעַנּוּ', 'Exo 1:11',  'Wayyiqtol',  '3mp', 'עָנָה · I-gutt + III-he; dual: gutt shewa + III-he 3mp'],
            ]),
            ('Group 3: Geminate', [
                ['11', 'יְהַלֲלוּ',  'Gen 12:15', '', '', ''],
                ['12', 'הַלְלוּ',    'Ps 113:1',  '', '', ''],
                ['13', 'הִלֵּל',     'Isa 14:12', '', '', ''],
                ['14', 'מְהַלֵּל',   'Ps 18:4',   '', '', ''],
                ['15', 'יְהַלֵּל',   'Prov 27:2', '', '', ''],
            ], [
                ['11', 'יְהַלֲלוּ',  'Gen 12:15', 'Wayyiqtol', '3mp', 'הָלַל · Geminate; dagesh in doubled ל; patach in prefix'],
                ['12', 'הַלְלוּ',    'Ps 113:1',  'Imperative', '2mp', 'הָלַל · Geminate; imperative 2mp; dagesh in ל'],
                ['13', 'הִלֵּל',     'Isa 14:12', 'Qatal',     '3ms', 'הָלַל · Geminate; chiriq under הִ in Piel perfect 3ms'],
                ['14', 'מְהַלֵּל',   'Ps 18:4',   'Participle', 'ms', 'הָלַל · Geminate; מְ prefix + tsere + dagesh in ל'],
                ['15', 'יְהַלֵּל',   'Prov 27:2', 'Yiqtol',    '3ms', 'הָלַל · Geminate; patach prefix + tsere + doubled ל'],
            ]),
            ('Group 4: I-nun', [
                ['16', 'יְנַחֵם',    'Gen 5:29',  '', '', ''],
                ['17', 'יְנַחֲמוּ', 'Gen 37:35', '', '', ''],
                ['18', 'יְנַגַּע',   'Gen 12:17', '', '', ''],
                ['19', 'נִסָּה',     'Gen 22:1',  '', '', ''],
                ['20', 'יְנַסֶּה',   'Deu 8:16',  '', '', ''],
            ], [
                ['16', 'יְנַחֵם',    'Gen 5:29',  'Yiqtol',    '3ms', 'נָחַם · I-nun retained (not assimilated in Piel); tsere'],
                ['17', 'יְנַחֲמוּ', 'Gen 37:35', 'Yiqtol',    '3mp', 'נָחַם · same root; 3mp ending; nun retained'],
                ['18', 'יְנַגַּע',   'Gen 12:17', 'Wayyiqtol', '3ms', 'נָגַע · I-nun retained; dagesh in ג (R2 Piel marker)'],
                ['19', 'נִסָּה',     'Gen 22:1',  'Qatal',     '3ms', 'נָסָה · I-nun + III-he; Piel perfect 3ms; qamets + ָה'],
                ['20', 'יְנַסֶּה',   'Deu 8:16',  'Yiqtol',    '3ms', 'נָסָה · I-nun + III-he; yiqtol; seghol + ה'],
            ]),
        ]

        for title, rows, ans in groups:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1], show_answers=False)
            self.add_section_break()

        hdr_b = ['#', 'Form', 'Reference', 'Weak Class', 'Conjugation', 'PGN', 'Root']
        cr_b  = [0.04, 0.15, 0.12, 0.17, 0.18, 0.09, 0.25]
        rows_b = [
            ['21', 'יְכַסֶּה',    'Gen 37:26',  '', '', '', ''],
            ['22', 'כִּסָּה',     'Gen 9:23',   '', '', '', ''],
            ['23', 'יְחַיּוּ',   'Exo 1:17',   '', '', '', ''],
            ['24', 'יְהַלֲלוּ',  'Ps 22:24',   '', '', '', ''],
            ['25', 'הִלֵּל',     'Isa 14:12',  '', '', '', ''],
            ['26', 'צִוָּה',      'Gen 7:9',    '', '', '', ''],
            ['27', 'יְנַגַּע',   'Gen 12:17',  '', '', '', ''],
            ['28', 'מְנַחֵם',    'Isa 51:12',  '', '', '', ''],
            ['29', 'עִנָּה',      'Exo 22:22',  '', '', '', ''],
            ['30', 'נִסָּה',     'Gen 22:1',   '', '', '', ''],
        ]
        ans_b = [
            ['21', 'יְכַסֶּה',    'Gen 37:26',  'III-he',       'Yiqtol',    '3ms', 'כָּסָה'],
            ['22', 'כִּסָּה',     'Gen 9:23',   'III-he',       'Qatal',     '3ms', 'כָּסָה'],
            ['23', 'יְחַיּוּ',   'Exo 1:17',   'I-gutt + III-he', 'Yiqtol', '3mp', 'חָיָה'],
            ['24', 'יְהַלֲלוּ',  'Ps 22:24',   'Geminate',     'Yiqtol',    '3mp', 'הָלַל'],
            ['25', 'הִלֵּל',     'Isa 14:12',  'Geminate',     'Qatal',     '3ms', 'הָלַל'],
            ['26', 'צִוָּה',      'Gen 7:9',    'III-he',       'Qatal',     '3ms', 'צָוָה'],
            ['27', 'יְנַגַּע',   'Gen 12:17',  'I-nun',        'Wayyiqtol', '3ms', 'נָגַע'],
            ['28', 'מְנַחֵם',    'Isa 51:12',  'I-nun',        'Participle','ms',  'נָחַם'],
            ['29', 'עִנָּה',      'Exo 22:22',  'I-gutt',       'Qatal',     '3ms', 'עָנָה'],
            ['30', 'נִסָּה',     'Gen 22:1',   'I-nun + III-he','Qatal',    '3ms', 'נָסָה'],
        ]

        self.add_section_heading('Part B — Mixed Forms')
        self.add_generic_table(hdr_b, rows_b, cr_b, heb_cols=[1], show_answers=False)
        self.add_section_break()

        self.add_reflection([
            'III-he: wayyiqtol יְכַל and יְצַו are apocopated. What happened to the ה? '
            'How does the qatal כִּלָּה differ — is the ה retained?',
            'I-nun Piel (items 16–20): unlike the Qal/Hiphil, the nun is NOT assimilated. '
            'Why? (Hint: dagesh forte in R2 is already the Piel stem marker.)',
            'Geminate items 11–15: what is the tell-tale vowel pattern for Piel Geminate '
            'perfect (item 13) vs. Piel Geminate yiqtol (items 11, 15)?',
        ])

        self.add_section_heading('Answer Key — Part A')
        for title, rows, ans in groups:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=True, answer_rows=ans)
            self.add_section_break()
        self.add_section_heading('Answer Key — Part B')
        self.add_generic_table(hdr_b, rows_b, cr_b, heb_cols=[1],
                               show_answers=True, answer_rows=ans_b)


def build_ch31_weak_form_id_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch31WeakFormIdExercise,
        'Chapter 31 — Piel Weak-Form Identification Drill',
        'BBH Chapter 31 · Piel Weak Verbs',
        ['hebrew', 'bbh', 'ch31', 'exercises', 'ch31-weak-form-id'],
        'ch31-weak-form-id.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 32 — Piel–Pual Contrast Drill
# ---------------------------------------------------------------------------


class Ch32PielPualContrastExercise(ExercisePDF):

    def _build(self) -> None:
        self.add_instructions(
            'Part A: active/passive pairs from the same root — identify stem and translate. '
            'Part B: 15 mixed forms (Piel / Pual / Hiphil / Hophal) — identify stem, '
            'conjugation, PGN, and root. Answer key is on the last page.'
        )
        self.add_note(
            'Piel diagnostic: Hireq / tsere under prefix + Dagesh Forte in R2.  '
            'Pual diagnostic: Qibbuts under R1 + Dagesh Forte in R2 '
            '(ר rejects dagesh → compensatory lengthening to qamets: מְבֹרָךְ).  '
            'Hophal: qibbuts under prefix consonant OR shureq for I-yod/Biconsonantal.  '
            'Hiphil: Hireq under הִ (perfect); patach under prefix (yiqtol/wayyiqtol).'
        )

        hdr_a = ['#', 'Root', 'Form A', 'Stem A', 'Form B', 'Stem B', 'Translation A / B']
        cr_a  = [0.04, 0.09, 0.14, 0.09, 0.14, 0.09, 0.41]
        rows_a = [
            ['1', 'בָּרַךְ', 'תְּבָרֵךְ (Yiqtol 2ms)',  '', 'מְבֹרָךְ (Part. ms)', '', ''],
            ['2', 'אָרַר',  'תָּאֹר (Yiqtol 2ms)',      '', 'יוּאָר (Yiqtol 3ms)',  '', ''],
            ['3', 'קָדַשׁ', 'וְקִדַּשְׁתָּ (Weq. 2ms)', '', 'יְקֻדַּשׁ (Yiqtol 3ms)', '', ''],
            ['4', 'יָלַד',  'יּוֹלֶד (Wayy. 3ms)',       '', 'יֻלַּד (Qatal 3ms)',  '', ''],
            ['5', 'כָּסָה', 'יְכַסֶּה (Yiqtol 3ms)',    '', 'יְכֻסּוּ (Wayy. 3mp)', '', ''],
        ]
        ans_a = [
            ['1', 'בָּרַךְ', 'תְּבָרֵךְ (Yiqtol 2ms)',  'Piel', 'מְבֹרָךְ (Part. ms)', 'Pual', 'you bless / is blessed (ר → qamets)'],
            ['2', 'אָרַר',  'תָּאֹר (Yiqtol 2ms)',      'Piel', 'יוּאָר (Yiqtol 3ms)',  'Pual', 'you curse / is cursed'],
            ['3', 'קָדַשׁ', 'וְקִדַּשְׁתָּ (Weq. 2ms)', 'Piel', 'יְקֻדַּשׁ (Yiqtol 3ms)', 'Pual', 'you consecrate / will be consecrated'],
            ['4', 'יָלַד',  'יּוֹלֶד (Wayy. 3ms)',       'Hiphil', 'יֻלַּד (Qatal 3ms)', 'Pual', 'he fathered / was born'],
            ['5', 'כָּסָה', 'יְכַסֶּה (Yiqtol 3ms)',    'Piel', 'יְכֻסּוּ (Wayy. 3mp)', 'Pual', 'he covers / they were covered'],
        ]

        hdr_b = ['#', 'Form', 'Stem', 'Conjugation', 'PGN', 'Root']
        cr_b  = [0.04, 0.18, 0.12, 0.20, 0.10, 0.36]
        rows_b = [
            ['6',  'מְבֹרָךְ',    '', '', '', ''],
            ['7',  'תְּבָרֵךְ',  '', '', '', ''],
            ['8',  'יֻלַּד',      '', '', '', ''],
            ['9',  'יְכֻלּוּ',   '', '', '', ''],
            ['10', 'יְכַסֶּה',   '', '', '', ''],
            ['11', 'יְכֻסּוּ',   '', '', '', ''],
            ['12', 'יְבָרֶךְ',   '', '', '', ''],
            ['13', 'יֻּגַּד',    '', '', '', ''],
            ['14', 'וַיְקַדֵּשׁ','', '', '', ''],
            ['15', 'יְקֻדַּשׁ',  '', '', '', ''],
            ['16', 'שִׁנֵּן',    '', '', '', ''],
            ['17', 'קֻדַּשׁ',    '', '', '', ''],
            ['18', 'הוּקַם',     '', '', '', ''],
            ['19', 'הִקְדִּישׁ', '', '', '', ''],
            ['20', 'יֻאַר',      '', '', '', ''],
        ]
        ans_b = [
            ['6',  'מְבֹרָךְ',    'Pual',   'Participle', 'ms',  'בָּרַךְ · qamets (compensatory; ר rejects dagesh)'],
            ['7',  'תְּבָרֵךְ',  'Piel',   'Yiqtol',     '2ms', 'בָּרַךְ · tsere under prefix = Piel'],
            ['8',  'יֻלַּד',      'Pual',   'Qatal',      '3ms', 'יָלַד · qibbuts + dagesh in ל = Pual'],
            ['9',  'יְכֻלּוּ',   'Pual',   'Wayyiqtol',  '3mp', 'כָּלָה · qibbuts + dagesh in כּ; III-he 3mp'],
            ['10', 'יְכַסֶּה',   'Piel',   'Yiqtol',     '3ms', 'כָּסָה · tsere (patach) prefix = Piel'],
            ['11', 'יְכֻסּוּ',   'Pual',   'Wayyiqtol',  '3mp', 'כָּסָה · qibbuts + dagesh in כּ = Pual'],
            ['12', 'יְבָרֶךְ',   'Piel',   'Wayyiqtol',  '3ms', 'בָּרַךְ · patach prefix + tsere = Piel'],
            ['13', 'יֻּגַּד',    'Hophal', 'Wayyiqtol',  '3ms', 'נָגַד · qibbuts under ו + dagesh = Hophal I-nun'],
            ['14', 'וַיְקַדֵּשׁ', 'Piel',  'Wayyiqtol',  '3ms', 'קָדַשׁ · patach-tsere pattern = Piel'],
            ['15', 'יְקֻדַּשׁ',  'Pual',   'Yiqtol',     '3ms', 'קָדַשׁ · qibbuts + dagesh = Pual'],
            ['16', 'שִׁנֵּן',    'Piel',   'Perfect',    '3ms', 'שָׁנַן · chiriq + tsere + dagesh in נּ = Piel'],
            ['17', 'קֻדַּשׁ',    'Pual',   'Perfect',    '3ms', 'קָדַשׁ · qibbuts + dagesh = Pual perfect'],
            ['18', 'הוּקַם',     'Hophal', 'Perfect',    '3ms', 'קוּם · shureq prefix = Hophal Biconsonantal'],
            ['19', 'הִקְדִּישׁ', 'Hiphil', 'Perfect',    '3ms', 'קָדַשׁ · chiriq prefix = Hiphil perfect'],
            ['20', 'יֻאַר',      'Pual',   'Yiqtol',     '3ms', 'אָרַר · qibbuts + I-aleph (rejects dagesh)'],
        ]

        self.add_section_heading('Part A — Active / Passive Pairs')
        self.add_generic_table(hdr_a, rows_a, cr_a, heb_cols=[2, 4], show_answers=False)
        self.add_section_break()
        self.add_section_heading('Part B — Mixed Forms: Piel / Pual / Hiphil / Hophal')
        self.add_generic_table(hdr_b, rows_b, cr_b, heb_cols=[1], show_answers=False)
        self.add_section_break()

        self.add_reflection([
            'The Pual diagnostic is "qibbuts under R1 + dagesh in R2." Item 6 (מְבֹרָךְ) has '
            'qamets, not qibbuts, under ר. What phonological rule explains this? '
            'Compare item 20 (יֻאַר) where the aleph also rejects dagesh.',
            'Items 13 (Hophal יֻּגַּד) and 8 (Pual יֻלַּד) both start with qibbuts. '
            'How do you distinguish a Hophal from a Pual when both use qibbuts?',
            'Item 4: יּוֹלֶד is Hiphil, not Piel, even though both are active. '
            'What features identify it as Hiphil rather than Piel?',
        ])

        self.add_section_heading('Answer Key — Part A')
        self.add_generic_table(hdr_a, rows_a, cr_a, heb_cols=[2, 4],
                               show_answers=True, answer_rows=ans_a)
        self.add_section_heading('Answer Key — Part B')
        self.add_generic_table(hdr_b, rows_b, cr_b, heb_cols=[1],
                               show_answers=True, answer_rows=ans_b)


def build_ch32_piel_pual_contrast_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch32PielPualContrastExercise,
        'Chapter 32 — Piel–Pual Contrast Drill',
        'BBH Chapter 32 · Pual Strong Verbs',
        ['hebrew', 'bbh', 'ch32', 'exercises', 'ch32-piel-pual-contrast'],
        'ch32-piel-pual-contrast.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 33 — Pual Weak-Form Identification Drill
# ---------------------------------------------------------------------------


class Ch33WeakFormIdExercise(ExercisePDF):

    def _build(self) -> None:
        self.add_instructions(
            'Part A: identify conjugation, PGN, and root (forms grouped by weak class). '
            'Part B: identify weak class first, then conjugation, PGN, and root. '
            'Answer key is on the last page.'
        )
        self.add_note(
            'Pual: Qibbuts under R1 + Dagesh Forte in R2. '
            'III-he Pual: ends in וּ (3cp) or ָה (3ms). '
            'I-nun Pual: nun assimilates into R2 dagesh (unlike Piel, where nun is retained). '
            'I-guttural/aleph + ר reject dagesh → compensatory lengthening.'
        )

        hdr = ['#', 'Form', 'Reference', 'Conjugation', 'PGN', 'Root']
        cr  = [0.05, 0.18, 0.14, 0.22, 0.10, 0.31]

        groups = [
            ('Group 1: III-he', [
                ['1', 'יְכֻלּוּ',   'Gen 2:1',   '', '', ''],
                ['2', 'יְכֻסּוּ',   'Gen 7:19',  '', '', ''],
                ['3', 'צֻוֵּיתָ',  'Gen 45:19', '', '', ''],
                ['4', 'כֻּלּוּ',   'Ezk 22:31', '', '', ''],
                ['5', 'צֻוֵּיתִי', 'Gen 45:19', '', '', ''],
            ], [
                ['1', 'יְכֻלּוּ',   'Gen 2:1',   'Wayyiqtol', '3mp', 'כָּלָה · qibbuts + dagesh + III-he 3mp'],
                ['2', 'יְכֻסּוּ',   'Gen 7:19',  'Wayyiqtol', '3mp', 'כָּסָה · qibbuts + dagesh in סּ; III-he 3mp'],
                ['3', 'צֻוֵּיתָ',  'Gen 45:19', 'Qatal',     '2ms', 'צָוָה · Pual qatal 2ms; III-he chiriq-yod ending'],
                ['4', 'כֻּלּוּ',   'Ezk 22:31', 'Qatal',     '3cp', 'כָּלָה · qibbuts + dagesh + 3cp וּ ending'],
                ['5', 'צֻוֵּיתִי', 'Gen 45:19', 'Qatal',     '1cs', 'צָוָה · Pual qatal 1cs; III-he chiriq-yod + י'],
            ]),
            ('Group 2: I-nun', [
                ['6',  'נֻכָּה',  'Exo 9:31',  '', '', ''],
                ['7',  'נֻכּוּ',  'Exo 9:32',  '', '', ''],
                ['8',  'נֻתַּץ',  'Jdg 6:28',  '', '', ''],
                ['9',  'נֻגָּף',  'Num 14:42', '', '', ''],
                ['10', 'נֻקָּה',  'Num 5:28',  '', '', ''],
            ], [
                ['6',  'נֻכָּה',  'Exo 9:31',  'Qatal',     '3fs', 'נָכָה · I-nun assimilates; qibbuts + dagesh in כּ'],
                ['7',  'נֻכּוּ',  'Exo 9:32',  'Qatal',     '3cp', 'נָכָה · same root; 3cp ending; note contrast with Piel'],
                ['8',  'נֻתַּץ',  'Jdg 6:28',  'Qatal',     '3ms', 'נָתַץ · I-nun assimilates into dagesh in תּ'],
                ['9',  'נֻגָּף',  'Num 14:42', 'Yiqtol',    '3mp', 'נָגַף · I-nun assimilates; qibbuts + dagesh'],
                ['10', 'נֻקָּה',  'Num 5:28',  'Yiqtol',    '3fs', 'נָקָה · I-nun assimilates; III-he feminine ending'],
            ]),
            ('Group 3: I-guttural / I-aleph', [
                ['11', 'אֹרָשָׂה',  'Exo 22:15', '', '', ''],
                ['12', 'עֻנָּה',    'Isa 51:21', '', '', ''],
                ['13', 'יֻאַר',     'Num 22:6',  '', '', ''],
                ['14', 'יְאָרֵר',   'Gen 12:3',  '', '', ''],
            ], [
                ['11', 'אֹרָשָׂה',  'Exo 22:15', 'Qatal',     '3fs', 'אָרַשׂ · I-aleph; holem (compensatory; ר rejects dagesh) + 3fs'],
                ['12', 'עֻנָּה',    'Isa 51:21', 'Qatal',     '3fs', 'עָנָה · I-gutt (ע) + III-he; qibbuts + dagesh in נּ'],
                ['13', 'יֻאַר',     'Num 22:6',  'Yiqtol',    '3ms', 'אָרַר · I-aleph; aleph rejects dagesh → qibbuts remains'],
                ['14', 'יְאָרֵר',   'Gen 12:3',  'Yiqtol',    '3ms', 'אָרַר · Piel (not Pual): patach prefix + tsere + dagesh'],
            ]),
        ]

        for title, rows, ans in groups:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1], show_answers=False)
            self.add_section_break()

        hdr_b = ['#', 'Form', 'Reference', 'Weak Class', 'Conjugation', 'PGN', 'Root']
        cr_b  = [0.04, 0.14, 0.12, 0.18, 0.18, 0.09, 0.25]
        rows_b = [
            ['15', 'יְכֻלּוּ',  'Gen 2:1',   '', '', '', ''],
            ['16', 'נֻכָּה',    'Exo 9:31',  '', '', '', ''],
            ['17', 'מְבֹרָךְ',  'Num 22:6',  '', '', '', ''],
            ['18', 'צֻוֵּיתָ', 'Gen 45:19', '', '', '', ''],
            ['19', 'נֻגָּף',    'Num 14:42', '', '', '', ''],
            ['20', 'אֹרָשָׂה', 'Exo 22:15', '', '', '', ''],
        ]
        ans_b = [
            ['15', 'יְכֻלּוּ',  'Gen 2:1',   'III-he',       'Wayyiqtol', '3mp', 'כָּלָה'],
            ['16', 'נֻכָּה',    'Exo 9:31',  'I-nun + III-he', 'Qatal',   '3fs', 'נָכָה'],
            ['17', 'מְבֹרָךְ',  'Num 22:6',  'Geminate (ר)',  'Participle','ms',  'בָּרַךְ'],
            ['18', 'צֻוֵּיתָ', 'Gen 45:19', 'III-he',        'Qatal',    '2ms', 'צָוָה'],
            ['19', 'נֻגָּף',    'Num 14:42', 'I-nun',         'Yiqtol',   '3mp', 'נָגַף'],
            ['20', 'אֹרָשָׂה', 'Exo 22:15', 'I-aleph + ר',   'Qatal',    '3fs', 'אָרַשׂ'],
        ]

        self.add_section_heading('Part B — Mixed Forms')
        self.add_generic_table(hdr_b, rows_b, cr_b, heb_cols=[1], show_answers=False)
        self.add_section_break()

        self.add_reflection([
            'III-he Pual (items 1–2): wayyiqtol 3mp ends in וּ. How does this compare '
            'to the Piel wayyiqtol 3mp of the same III-he roots?',
            'I-nun Pual (items 6–10) vs. I-nun Piel (Ch31 items 16–20): '
            'the nun assimilates in the Pual but is retained in the Piel. Why the difference?',
            'Item 14 (יְאָרֵר) is Piel, not Pual. What features identify it as Piel? '
            'Compare to item 13 (יֻאַר, Pual). Write the diagnostic for each.',
        ])

        self.add_section_heading('Answer Key — Part A')
        for title, rows, ans in groups:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=True, answer_rows=ans)
            self.add_section_break()
        self.add_section_heading('Answer Key — Part B')
        self.add_generic_table(hdr_b, rows_b, cr_b, heb_cols=[1],
                               show_answers=True, answer_rows=ans_b)


def build_ch33_weak_form_id_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch33WeakFormIdExercise,
        'Chapter 33 — Pual Weak-Form Identification Drill',
        'BBH Chapter 33 · Pual Weak Verbs',
        ['hebrew', 'bbh', 'ch33', 'exercises', 'ch33-weak-form-id'],
        'ch33-weak-form-id.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 34 — Hithpael Semantic Function Sorting
# ---------------------------------------------------------------------------


class Ch34FunctionSortExercise(ExercisePDF):
    _ENTRIES = [
        SortEntry('1',  'מִתְהַלֵּךְ',    'Participle ms',   'Gen 3:8',   '"walking about (in the garden)"',              'IT', 'הָלַךְ', 'Back-and-forth movement; not a single walk'),
        SortEntry('2',  'יִּתְחַבֵּא',    'Wayyiqtol 3ms',   'Gen 3:8',   '"he hid himself"',                             'R',  'חָבָא',  'Subject acts on itself; concealment'),
        SortEntry('3',  'יִּתְהַלֵּךְ',   'Wayyiqtol 3ms',   'Gen 5:22',  '"Enoch walked about (with God)"',              'IT', 'הָלַךְ', 'Habitual/continuous walking; same root as #1'),
        SortEntry('4',  'יִּתְעַצֵּב',    'Wayyiqtol 3ms',   'Gen 6:6',   '"he was grieved (to his heart)"',              'R',  'עָצַב',  'Inward grief; the LORD\'s heart acts on itself'),
        SortEntry('5',  'יִּתְגַּל',      'Wayyiqtol 3ms',   'Gen 9:21',  '"he uncovered himself"',                       'R',  'גָּלָה', 'Reflexive uncovering; subject = object'),
        SortEntry('6',  'הִתְהַלֵּךְ',   'Imperative 2ms',  'Gen 13:17', '"walk about (through the land)!"',              'IT', 'הָלַךְ', 'Command to traverse repeatedly; same root'),
        SortEntry('7',  'הִתְעַנִּי',     'Imperative 2fs',  'Gen 16:9',  '"humble yourself!"',                           'R',  'עָנָה',  'Reflexive self-humbling; subject acts on itself'),
        SortEntry('8',  'הִתְהַלֵּךְ',   'Imperative 2ms',  'Gen 17:1',  '"walk about before me!"',                      'IT', 'הָלַךְ', 'Continuous conduct before YHWH'),
        SortEntry('9',  'יִּשְׁתַּחוּ',  'Wayyiqtol 3ms',   'Gen 18:2',  '"he prostrated himself"',                      'R',  'שָׁחָה', 'Reflexive prostration; III-he Hithpael'),
        SortEntry('10', 'יִּשְׁתַּחוּ',  'Wayyiqtol 3ms',   'Gen 19:1',  '"Lot bowed down"',                             'R',  'שָׁחָה', 'Same form; Lot prostrates himself before the angels'),
        SortEntry('11', 'יִּתְפַּלֵּל',  'Wayyiqtol 3ms',   'Gen 20:17', '"he prayed"',                                  'DN', 'פָּלַל', 'From פֶּלֶל "mediation/judgment"; to mediate/intercede'),
        SortEntry('12', 'הִתְבָּרֲכוּ',  'Weqatal 3cp',     'Gen 22:18', '"they will bless themselves / be blessed"',    'R',  'בָּרַךְ', 'Reflexive blessing; can also be read as passive-like'),
        SortEntry('13', 'הִתְהַלַּכְתִּי', 'Qatal 1cs',     'Gen 24:40', '"I have walked about (before the LORD)"',      'IT', 'הָלַךְ', 'Continuous habitual conduct'),
        SortEntry('14', 'יִּשְׁתַּחוּ',  'Wayyiqtol 3ms',   'Gen 24:26', '"he bowed down and worshiped"',                'R',  'שָׁחָה', 'Same form; servant prostrates himself'),
        SortEntry('15', 'הִתְעַשְּׂקוּ', 'Qatal 3cp',       'Gen 26:20', '"they quarreled"',                             'RC', 'עָשַׂק',  'Mutual quarreling; the herdsmen act on one another'),
        SortEntry('16', 'מִתְנַחֵם',     'Participle ms',   'Gen 27:42', '"is comforting himself"',                      'R',  'נָחַם',  'Esau comforting himself with the thought of revenge'),
        SortEntry('17', 'יִּתְנַכְּלוּ', 'Wayyiqtol 3mp',   'Gen 37:18', '"they plotted against him"',                  'RC', 'נָכַל',  'Collective/mutual scheming against Joseph'),
        SortEntry('18', 'וַיִּתְאַבֵּל', 'Wayyiqtol 3ms',   'Gen 37:34', '"he mourned"',                                 'R',  'אָבַל',  'Inward grief expressed outwardly; reflexive mourning'),
        SortEntry('19', 'תִּתְכַּסֶּה',  'Wayyiqtol 3fs',   'Gen 24:65', '"she covered herself"',                        'R',  'כָּסָה', 'Rebekah covered herself with her veil'),
        SortEntry('20', 'יִּשְׁתַּחֲווּ', 'Wayyiqtol 3mp',  'Gen 33:7',  '"they bowed down"',                            'R',  'שָׁחָה', 'Jacob\'s wives and children prostrate themselves'),
        SortEntry('21', 'אֶתְנַהֲלָה',  'Cohortative 1cs', 'Gen 33:14', '"I will journey on slowly"',                   'IT', 'נָהַל',  'Iterative/continuous slow travel; guiding the flocks'),
        SortEntry('22', 'הִתְקַדְּשׁוּ', 'Imperative 2mp',  'Exo 19:22', '"consecrate yourselves!"',                    'R',  'קָדַשׁ', 'The priests prepare themselves for the theophany'),
        SortEntry('23', 'וַיִּתְחַזֵּק', 'Wayyiqtol 3ms',   'Exo 7:13',  '"and his heart was strengthened"',            'R',  'חָזַק',  'The heart strengthened itself / became stubborn'),
        SortEntry('24', 'יִּתְהַלְּלוּ', 'Wayyiqtol 3mp',  'Ps 97:7',   '"they glory in idols"',                        'ES', 'הָלַל',  'Present themselves as glorious; boast in idols'),
        SortEntry('25', 'הִתְחַזְּקוּ',  'Imperative 2mp',  'Jos 1:6',   '"be strong!"',                                 'ES', 'חָזַק',  'Present/conduct yourselves as strong; estimative force'),
    ]

    def _build(self) -> None:
        self.add_instructions(
            'Classify each Hithpael verb: R (Reflexive), RC (Reciprocal), '
            'IT (Iterative/Frequentative), ES (Estimative/Declarative), or DN (Denominative). '
            'Answer key is on the last page.'
        )
        self.add_note(
            'R = Reflexive (subject acts on itself)  |  '
            'RC = Reciprocal (subjects act on one another)  |  '
            'IT = Iterative/Frequentative (repeated or habitual action)  |  '
            'ES = Estimative (subject presents itself as being in a state)  |  '
            'DN = Denominative (derived from a noun)'
        )
        self.add_sort_table(self._ENTRIES, show_answers=False)
        self.add_reflection([
            'הָלַךְ appears 5 times (items 1, 3, 6, 8, 13). Why is this Iterative rather than Reflexive? '
            'What does "walking about" add that a single-step Qal walk does not?',
            'Item 12 (הִתְבָּרֲכוּ, Gen 22:18) can be translated "bless themselves" (R) '
            'or "be blessed" (passive). What would change if you read this as passive?',
            'Items 24–25 are Estimative. What does the Hithpael add to הָלַל and חָזַק '
            'that the Qal of the same root would not express?',
        ])
        self.add_answer_key_sort(self._ENTRIES)


def build_ch34_function_sort_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch34FunctionSortExercise,
        'Chapter 34 — Hithpael Semantic Function Sorting',
        'BBH Chapter 34 · Hithpael Strong Verbs',
        ['hebrew', 'bbh', 'ch34', 'exercises', 'ch34-function-sort'],
        'ch34-function-sort.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Chapter 35 — Hithpael Weak-Form Identification Drill
# ---------------------------------------------------------------------------


class Ch35WeakFormIdExercise(ExercisePDF):

    def _build(self) -> None:
        self.add_instructions(
            'Part A: identify conjugation, PGN, and root (forms grouped by weak class). '
            'Part B: mixed forms — identify weak class first, then conjugation, PGN, and root. '
            'Answer key is on the last page.'
        )
        self.add_note(
            'Sibilant Metathesis: when R1 = שׁ/שׂ/ס/צ, the Hithpael ת swaps with R1 '
            '(and ת → ט before צ). E.g., שָׁחָה → הִשְׁתַּחֲוָה; שָׁמַר → הִשְׁתַּמֵּר. '
            'I-guttural: composite shewa under R1 (e.g., הִתְהַלֵּךְ). '
            'III-he: apocopation in wayyiqtol (ה drops: יִּתְגַּל from גָּלָה).'
        )

        hdr = ['#', 'Form', 'Reference', 'Conjugation', 'PGN', 'Root']
        cr  = [0.05, 0.20, 0.14, 0.22, 0.10, 0.29]

        groups = [
            ('Group 1: III-he', [
                ['1', 'יִּתְגַּל',      'Gen 9:21',  '', '', ''],
                ['2', 'יִּשְׁתַּחוּ',  'Gen 18:2',  '', '', ''],
                ['3', 'הִשְׁתַּחֲוָה', 'Gen 22:5',  '', '', ''],
                ['4', 'תִּתְכַּסֶּה',  'Gen 24:65', '', '', ''],
                ['5', 'יִּשְׁתַּחֲווּ', 'Gen 33:7', '', '', ''],
            ], [
                ['1', 'יִּתְגַּל',      'Gen 9:21',  'Wayyiqtol', '3ms', 'גָּלָה · III-he apocopated; ה dropped'],
                ['2', 'יִּשְׁתַּחוּ',  'Gen 18:2',  'Wayyiqtol', '3ms', 'שָׁחָה · metathesis (שׁ + ת swap) + III-he apocopated'],
                ['3', 'הִשְׁתַּחֲוָה', 'Gen 22:5',  'Qatal',     '3ms', 'שָׁחָה · metathesis + III-he; qamets + ָה retained in qatal'],
                ['4', 'תִּתְכַּסֶּה',  'Gen 24:65', 'Wayyiqtol', '3fs', 'כָּסָה · strong R1; III-he seghol + ה retained in yiqtol'],
                ['5', 'יִּשְׁתַּחֲווּ', 'Gen 33:7', 'Wayyiqtol', '3mp', 'שָׁחָה · metathesis + III-he; 3mp וּ ending'],
            ]),
            ('Group 2: I-guttural', [
                ['6',  'מִתְהַלֵּךְ',  'Gen 3:8',   '', '', ''],
                ['7',  'יִּתְהַלֵּךְ', 'Gen 5:22',  '', '', ''],
                ['8',  'יִּתְחַבֵּא',  'Gen 3:8',   '', '', ''],
                ['9',  'הִתְעַנִּי',   'Gen 16:9',  '', '', ''],
                ['10', 'וַיִּתְחַזֵּק', 'Exo 7:13', '', '', ''],
            ], [
                ['6',  'מִתְהַלֵּךְ',  'Gen 3:8',   'Participle',  'ms', 'הָלַךְ · I-gutt (ה); hateph-patach under ה'],
                ['7',  'יִּתְהַלֵּךְ', 'Gen 5:22',  'Wayyiqtol',   '3ms', 'הָלַךְ · same root; hateph-patach + tsere'],
                ['8',  'יִּתְחַבֵּא',  'Gen 3:8',   'Wayyiqtol',   '3ms', 'חָבָא · I-gutt (ח) + III-aleph; hateph under ח'],
                ['9',  'הִתְעַנִּי',   'Gen 16:9',  'Imperative',  '2fs', 'עָנָה · I-gutt (ע) + III-he; hateph under ע'],
                ['10', 'וַיִּתְחַזֵּק', 'Exo 7:13', 'Wayyiqtol',   '3ms', 'חָזַק · I-gutt (ח); hateph-patach; dagesh in ז'],
            ]),
            ('Group 3: Sibilant Metathesis (R1 = שׁ/שׂ/ס/צ)', [
                ['11', 'יִּשְׁתַּחוּ',  'Gen 19:1',  '', '', ''],
                ['12', 'הִשְׁתַּחֲוָה', 'Gen 23:7',  '', '', ''],
                ['13', 'יִּשְׁתַּחֲווּ', 'Gen 33:7', '', '', ''],
                ['14', 'הִשְׁתַּמֵּר',  'Deu 4:9',   '', '', ''],
                ['15', 'וַיִּשְׁתֹּמֵם', 'Dan 4:16', '', '', ''],
            ], [
                ['11', 'יִּשְׁתַּחוּ',  'Gen 19:1',  'Wayyiqtol', '3ms', 'שָׁחָה · metathesis: ת + שׁ → שׁ + תּ; III-he apocopated'],
                ['12', 'הִשְׁתַּחֲוָה', 'Gen 23:7',  'Qatal',     '3ms', 'שָׁחָה · metathesis + III-he qatal; ָה retained'],
                ['13', 'יִּשְׁתַּחֲווּ', 'Gen 33:7', 'Wayyiqtol', '3mp', 'שָׁחָה · same as #11; 3mp וּ ending'],
                ['14', 'הִשְׁתַּמֵּר',  'Deu 4:9',   'Imperative', '2ms', 'שָׁמַר · metathesis: הִשְׁ instead of הִתְשׁ'],
                ['15', 'וַיִּשְׁתֹּמֵם', 'Dan 4:16', 'Wayyiqtol', '3ms', 'שָׁמֵם · metathesis; Geminate root'],
            ]),
            ('Group 4: I-nun', [
                ['16', 'מִתְנַחֵם',    'Gen 27:42', '', '', ''],
                ['17', 'יִּתְנַחֲמוּ', 'Gen 37:35', '', '', ''],
                ['18', 'יִּתְנַכְּלוּ', 'Gen 37:18', '', '', ''],
                ['19', 'אֶתְנַהֲלָה',  'Gen 33:14', '', '', ''],
                ['20', 'מִתְנַדְּבִים', 'Ezr 1:6',  '', '', ''],
            ], [
                ['16', 'מִתְנַחֵם',    'Gen 27:42', 'Participle', 'ms', 'נָחַם · I-nun RETAINED (not assimilated) in Hithpael'],
                ['17', 'יִּתְנַחֲמוּ', 'Gen 37:35', 'Wayyiqtol', '3mp', 'נָחַם · same root; 3mp ending; nun retained'],
                ['18', 'יִּתְנַכְּלוּ', 'Gen 37:18', 'Wayyiqtol', '3mp', 'נָכַל · I-nun retained; dagesh in כּ = Piel-pattern R2'],
                ['19', 'אֶתְנַהֲלָה',  'Gen 33:14', 'Cohortative', '1cs', 'נָהַל · I-nun retained; hateph-patach under ה (I-gutt?)'],
                ['20', 'מִתְנַדְּבִים', 'Ezr 1:6',  'Participle', 'mp', 'נָדַב · I-nun retained; plural מִתְנַ + dagesh in ד'],
            ]),
        ]

        for title, rows, ans in groups:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1], show_answers=False)
            self.add_section_break()

        hdr_b = ['#', 'Form', 'Reference', 'Weak Class', 'Conjugation', 'PGN', 'Root']
        cr_b  = [0.04, 0.18, 0.12, 0.17, 0.18, 0.09, 0.22]
        rows_b = [
            ['21', 'וַיִּשְׁתַּחוּ',  'Gen 24:26', '', '', '', ''],
            ['22', 'וַיִּתְאַבֵּל', 'Gen 37:34', '', '', '', ''],
            ['23', 'הִתְקַדְּשׁוּ',  'Exo 19:22', '', '', '', ''],
            ['24', 'וַיִּתְפַּלֵּל', 'Gen 20:17', '', '', '', ''],
            ['25', 'הִתְהַלֵּל',    'Jer 9:22',  '', '', '', ''],
            ['26', 'הִשְׁתַּמֵּר',  'Gen 31:24', '', '', '', ''],
            ['27', 'מִתְחַזְּקִים',  'Neh 3:20',  '', '', '', ''],
            ['28', 'יִּתְגַּלְגַּל', 'Ruth 3:8',  '', '', '', ''],
            ['29', 'הִתְרוֹמֵם',    'Ps 46:11',  '', '', '', ''],
            ['30', 'הִשְׁתּוֹלֵל',  'Isa 51:7',  '', '', '', ''],
        ]
        ans_b = [
            ['21', 'וַיִּשְׁתַּחוּ',  'Gen 24:26', 'Sibilant metathesis + III-he', 'Wayyiqtol',  '3ms', 'שָׁחָה'],
            ['22', 'וַיִּתְאַבֵּל', 'Gen 37:34', 'Strong',       'Wayyiqtol',  '3ms', 'אָבַל'],
            ['23', 'הִתְקַדְּשׁוּ',  'Exo 19:22', 'Strong',       'Imperative', '2mp', 'קָדַשׁ'],
            ['24', 'וַיִּתְפַּלֵּל', 'Gen 20:17', 'Strong',       'Wayyiqtol',  '3ms', 'פָּלַל'],
            ['25', 'הִתְהַלֵּל',    'Jer 9:22',  'I-gutt (ה) + Geminate', 'Imperative', '2ms', 'הָלַל'],
            ['26', 'הִשְׁתַּמֵּר',  'Gen 31:24', 'Sibilant metathesis',    'Imperative', '2ms', 'שָׁמַר'],
            ['27', 'מִתְחַזְּקִים',  'Neh 3:20',  'I-gutt (ח)',  'Participle', 'mp',  'חָזַק'],
            ['28', 'יִּתְגַּלְגַּל', 'Ruth 3:8',  'Geminate',    'Wayyiqtol',  '3ms', 'גָּלַל'],
            ['29', 'הִתְרוֹמֵם',    'Ps 46:11',  'Biconsonantal/Geminate', 'Imperative', '2ms', 'רוּם'],
            ['30', 'הִשְׁתּוֹלֵל',  'Isa 51:7',  'Sibilant metathesis',    'Qatal',      '3ms', 'שָׁלַל'],
        ]

        self.add_section_heading('Part B — Mixed Forms')
        self.add_generic_table(hdr_b, rows_b, cr_b, heb_cols=[1], show_answers=False)
        self.add_section_break()

        self.add_reflection([
            'Sibilant metathesis (items 11–15, Part B items 21, 26, 30): write the '
            'expected (pre-metathesis) form of הִשְׁתַּחֲוָה. Then identify which letters swapped.',
            'I-guttural Hithpael (items 6–10): how would you distinguish a Hithpael I-guttural '
            'form (e.g., מִתְהַלֵּךְ) from a Piel I-guttural form (e.g., מְהַלֵּל)?',
            'III-he apocopation: items 1, 2, 5 (wayyiqtol) drop the final ה. '
            'Item 3 (qatal 3ms) retains it. Why does the qatal retain the ה but the wayyiqtol does not?',
        ])

        self.add_section_heading('Answer Key — Part A')
        for title, rows, ans in groups:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=True, answer_rows=ans)
            self.add_section_break()
        self.add_section_heading('Answer Key — Part B')
        self.add_generic_table(hdr_b, rows_b, cr_b, heb_cols=[1],
                               show_answers=True, answer_rows=ans_b)


def build_ch35_weak_form_id_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch35WeakFormIdExercise,
        'Chapter 35 — Hithpael Weak-Form Identification Drill',
        'BBH Chapter 35 · Hithpael Weak Verbs',
        ['hebrew', 'bbh', 'ch35', 'exercises', 'ch35-weak-form-id'],
        'ch35-weak-form-id.pdf',
        out_dir,
    )


# ===========================================================================
# Paradigm Completion Exercises — BBH Ch13–Ch35
# ===========================================================================

# ---------------------------------------------------------------------------
# Ch13 — Qal Perfect Paradigm Drill
# ---------------------------------------------------------------------------


class Ch13QalPerfectParadigmDrill(ExercisePDF):
    _instructions = (
        'Write the correct Qal Perfect form for each PGN cell. '
        'Root: קטל (Type-A fientive). All cells are blank — fill from memory.'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'PGN', 'Form (קטל)']
        cr   = [0.06, 0.20, 0.74]
        rows = [
            ['1', '3ms', ''], ['2', '3fs', ''], ['3', '2ms', ''], ['4', '2fs', ''],
            ['5', '1cs', ''], ['6', '3cp', ''], ['7', '2mp', ''], ['8', '2fp', ''],
            ['9', '1cp', ''],
        ]
        ans = [
            ['1', '3ms', 'קָטַל'], ['2', '3fs', 'קָטְלָה'], ['3', '2ms', 'קָטַלְתָּ'],
            ['4', '2fs', 'קָטַלְתְּ'], ['5', '1cs', 'קָטַלְתִּי'], ['6', '3cp', 'קָטְלוּ'],
            ['7', '2mp', 'קְטַלְתֶּם'], ['8', '2fp', 'קְטַלְתֶּן'], ['9', '1cp', 'קָטַלְנוּ'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr,
                                       answer_heb_cols=[2],
                                       section_title='Qal Perfect — קטל')


def build_ch13_qal_perfect_paradigm_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch13QalPerfectParadigmDrill,
        'Chapter 13 — Qal Perfect Paradigm Drill',
        'BBH Chapter 13 · Qal Perfect Strong Verbs',
        ['hebrew', 'bbh', 'ch13', 'exercises', 'ch13-qal-perfect-paradigm-drill'],
        'ch13-qal-perfect-paradigm-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch15 — Qal Imperfect Paradigm Drill
# ---------------------------------------------------------------------------


class Ch15QalImperfectParadigmDrill(ExercisePDF):
    _instructions = (
        'Write the correct Qal Imperfect (yiqtol) form for each PGN. '
        'Root: שמר → יִשְׁמֹר (A-class, holem theme). All cells blank — fill from memory.'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'PGN', 'Form (שמר)']
        cr   = [0.06, 0.20, 0.74]
        rows = [['%d' % i, pgn, ''] for i, pgn in enumerate([
            '3ms','3fs','2ms','2fs','1cs','3mp','3fp','2mp','2fp','1cp'], 1)]
        ans = [
            ['1','3ms','יִשְׁמֹר'], ['2','3fs','תִּשְׁמֹר'], ['3','2ms','תִּשְׁמֹר'],
            ['4','2fs','תִּשְׁמְרִי'], ['5','1cs','אֶשְׁמֹר'], ['6','3mp','יִשְׁמְרוּ'],
            ['7','3fp','תִּשְׁמֹרְנָה'], ['8','2mp','תִּשְׁמְרוּ'], ['9','2fp','תִּשְׁמֹרְנָה'],
            ['10','1cp','נִשְׁמֹר'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr,
                                       answer_heb_cols=[2],
                                       section_title='Qal Imperfect — שמר')


def build_ch15_qal_imperfect_paradigm_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch15QalImperfectParadigmDrill,
        'Chapter 15 — Qal Imperfect Paradigm Drill',
        'BBH Chapter 15 · Qal Imperfect Strong Verbs',
        ['hebrew', 'bbh', 'ch15', 'exercises', 'ch15-qal-imperfect-paradigm-drill'],
        'ch15-qal-imperfect-paradigm-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch17 — Wayyiqtol Paradigm Drill
# ---------------------------------------------------------------------------


class Ch17WayyiqtolParadigmDrill(ExercisePDF):
    _instructions = (
        'Write the Wayyiqtol (waw-consecutive imperfect) form for each PGN. '
        'Root: קטל. Note: 1cs prefix waw takes qamets (וָ) before aleph.'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'PGN', 'Wayyiqtol form (קטל)']
        cr   = [0.06, 0.20, 0.74]
        rows = [['%d' % i, pgn, ''] for i, pgn in enumerate([
            '3ms','3fs','2ms','2fs','1cs','3mp','3fp','2mp','2fp','1cp'], 1)]
        ans = [
            ['1','3ms','וַיִּקְטֹל'], ['2','3fs','וַתִּקְטֹל'], ['3','2ms','וַתִּקְטֹל'],
            ['4','2fs','וַתִּקְטְלִי'], ['5','1cs','וָאֶקְטֹל'], ['6','3mp','וַיִּקְטְלוּ'],
            ['7','3fp','וַתִּקְטֹלְנָה'], ['8','2mp','וַתִּקְטְלוּ'], ['9','2fp','וַתִּקְטֹלְנָה'],
            ['10','1cp','וַנִּקְטֹל'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr,
                                       answer_heb_cols=[2],
                                       section_title='Wayyiqtol — קטל')


def build_ch17_wayyiqtol_paradigm_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch17WayyiqtolParadigmDrill,
        'Chapter 17 — Wayyiqtol Paradigm Drill',
        'BBH Chapter 17 · Waw-Consecutive',
        ['hebrew', 'bbh', 'ch17', 'exercises', 'ch17-wayyiqtol-paradigm-drill'],
        'ch17-wayyiqtol-paradigm-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch18 — Qal Imperative Paradigm Drill
# ---------------------------------------------------------------------------


class Ch18QalImperativeParadigmDrill(ExercisePDF):
    _instructions = (
        'Write the Qal Imperative form for each PGN. '
        'Root: שמר (A-class). Note: Imperative has only 2nd-person forms.'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'PGN', 'Imperative form (שמר)']
        cr   = [0.06, 0.20, 0.74]
        rows = [['%d' % i, pgn, ''] for i, pgn in enumerate(['2ms','2fs','2mp','2fp'], 1)]
        ans  = [
            ['1','2ms','שְׁמֹר'], ['2','2fs','שִׁמְרִי'],
            ['3','2mp','שִׁמְרוּ'], ['4','2fp','שְׁמֹרְנָה'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr,
                                       answer_heb_cols=[2],
                                       section_title='Qal Imperative — שמר')


def build_ch18_qal_imperative_paradigm_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch18QalImperativeParadigmDrill,
        'Chapter 18 — Qal Imperative Paradigm Drill',
        'BBH Chapter 18 · Qal Imperative',
        ['hebrew', 'bbh', 'ch18', 'exercises', 'ch18-qal-imperative-paradigm-drill'],
        'ch18-qal-imperative-paradigm-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch19 — Verb + Pronominal Suffix Paradigm Drill
# ---------------------------------------------------------------------------


class Ch19VerbSuffixParadigmDrill(ExercisePDF):
    _instructions = (
        'Part A: Supply the Qal Perfect 3ms (שָׁמַר) with the given object suffix. '
        'Part B: Supply the Qal Imperfect 3ms (יִשְׁמֹר) with the given object suffix. '
        'Note the energic nun before 3ms suffix in Part B.'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'Suffix (person)', 'Form']
        cr   = [0.06, 0.30, 0.64]

        rows_a = [
            ['1', '+1cs (me)', ''], ['2', '+2ms (you m.)', ''], ['3', '+3ms (him)', ''],
            ['4', '+3fs (her)', ''], ['5', '+1cp (us)', ''], ['6', '+3mp (them)', ''],
        ]
        ans_a = [
            ['1', '+1cs (me)', 'שְׁמָרַנִי'], ['2', '+2ms (you m.)', 'שְׁמָרְךָ'],
            ['3', '+3ms (him)', 'שְׁמָרוֹ'], ['4', '+3fs (her)', 'שְׁמָרָהּ'],
            ['5', '+1cp (us)', 'שְׁמָרָנוּ'], ['6', '+3mp (them)', 'שְׁמָרָם'],
        ]
        rows_b = [
            ['7', '+1cs (me)', ''], ['8', '+3ms (him)', ''], ['9', '+1cp (us)', ''],
        ]
        ans_b = [
            ['7', '+1cs (me)', 'יִשְׁמְרֵנִי'],
            ['8', '+3ms (him)', 'יִשְׁמְרֶנּוּ'],
            ['9', '+1cp (us)', 'יִשְׁמְרֵנוּ'],
        ]
        self.add_drill_with_answer_key(hdrs, rows_a, ans_a, col_ratios=cr,
                                       answer_heb_cols=[2],
                                       section_title='Part A — Qal Perfect 3ms + Suffix (שָׁמַר)',
                                       answer_title='Part A — Answer Key')
        self.add_drill_with_answer_key(hdrs, rows_b, ans_b, col_ratios=cr,
                                       answer_heb_cols=[2],
                                       section_title='Part B — Qal Imperfect 3ms + Suffix (יִשְׁמֹר)',
                                       answer_title='Part B — Answer Key')


def build_ch19_verb_suffix_paradigm_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch19VerbSuffixParadigmDrill,
        'Chapter 19 — Verb + Pronominal Suffix Paradigm Drill',
        'BBH Chapter 19 · Qal Pronominal Suffixes on Verbs',
        ['hebrew', 'bbh', 'ch19', 'exercises', 'ch19-verb-suffix-paradigm-drill'],
        'ch19-verb-suffix-paradigm-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch20 — Qal Infinitive Construct Paradigm Drill
# ---------------------------------------------------------------------------


class Ch20QalICParadigmDrill(ExercisePDF):
    _instructions = (
        'Give the bare Infinitive Construct and the form with לְ for each root class.'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'Root class', 'Bare IC', '+ לְ prefix']
        cr   = [0.05, 0.25, 0.35, 0.35]

        rows = [
            ['1', 'Strong A  (שמר)', '', ''],
            ['2', 'III-ה  (ראה)', '', ''],
            ['3', 'Biconsonantal  (שוב)', '', ''],
            ['4', 'I-י  (ישב)', '', ''],
            ['5', 'I-נ  (נתן)', '', ''],
            ['6', 'I-aleph  (אמר)', '', ''],
        ]
        ans = [
            ['1', 'Strong A  (שמר)', 'שְׁמֹר', 'לִשְׁמֹר'],
            ['2', 'III-ה  (ראה)', 'רְאוֹת', 'לִרְאוֹת'],
            ['3', 'Biconsonantal  (שוב)', 'שׁוּב', 'לָשׁוּב'],
            ['4', 'I-י  (ישב)', 'שֶׁבֶת', 'לָשֶׁבֶת'],
            ['5', 'I-נ  (נתן)', 'תֵּת', 'לָתֵת'],
            ['6', 'I-aleph  (אמר)', 'אֱמֹר', 'לֵאמֹר'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr,
                                       answer_heb_cols=[2, 3],
                                       section_title='Qal Infinitive Construct — Root Classes')


def build_ch20_qal_ic_paradigm_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch20QalICParadigmDrill,
        'Chapter 20 — Qal Infinitive Construct Paradigm Drill',
        'BBH Chapter 20 · Qal Infinitive Construct',
        ['hebrew', 'bbh', 'ch20', 'exercises', 'ch20-qal-ic-paradigm-drill'],
        'ch20-qal-ic-paradigm-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch21 — Qal Infinitive Absolute Paradigm Drill
# ---------------------------------------------------------------------------


class Ch21QalIAParadigmDrill(ExercisePDF):
    _instructions = (
        'Give the Qal Infinitive Absolute for each root class. '
        'Compare with the IC form — the vowel under R1 is the key distinction.'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'Root class', 'IC form (shown)', 'IA form']
        cr   = [0.05, 0.25, 0.30, 0.40]

        rows = [
            ['1', 'Strong A  (שמר)', 'שְׁמֹר', ''],
            ['2', 'III-ה  (ראה)', 'רְאוֹת', ''],
            ['3', 'Biconsonantal  (מות)', 'מוּת', ''],
            ['4', 'I-י  (הלך)', 'לֶכֶת', ''],
            ['5', 'I-נ  (נתן)', 'תֵּת', ''],
            ['6', 'I-aleph  (אכל)', 'אֱכֹל', ''],
        ]
        ans = [
            ['1', 'Strong A  (שמר)', 'שְׁמֹר', 'שָׁמוֹר'],
            ['2', 'III-ה  (ראה)', 'רְאוֹת', 'רָאֹה'],
            ['3', 'Biconsonantal  (מות)', 'מוּת', 'מוֹת'],
            ['4', 'I-י  (הלך)', 'לֶכֶת', 'הָלוֹךְ'],
            ['5', 'I-נ  (נתן)', 'תֵּת', 'נָתוֹן'],
            ['6', 'I-aleph  (אכל)', 'אֱכֹל', 'אָכוֹל'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr,
                                       heb_cols=[2], answer_heb_cols=[3],
                                       section_title='Qal Infinitive Absolute — Root Classes')


def build_ch21_qal_ia_paradigm_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch21QalIAParadigmDrill,
        'Chapter 21 — Qal Infinitive Absolute Paradigm Drill',
        'BBH Chapter 21 · Qal Infinitive Absolute',
        ['hebrew', 'bbh', 'ch21', 'exercises', 'ch21-qal-ia-paradigm-drill'],
        'ch21-qal-ia-paradigm-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch22 — Qal Participle Paradigm Drill
# ---------------------------------------------------------------------------


class Ch22QalParticipleParadigmDrill(ExercisePDF):
    _instructions = (
        'Part A: Write the Qal Active Participle for the root שמר (4 forms). '
        'Part B: Write the Qal Passive Participle (qatûl pattern) for the root שמר (4 forms).'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'Form', 'Active (שמר)']
        cr   = [0.06, 0.20, 0.74]

        rows_a = [['1','ms',''],['2','fs',''],['3','mp',''],['4','fp','']]
        ans_a  = [
            ['1','ms','שֹׁמֵר'], ['2','fs','שֹׁמֶרֶת'],
            ['3','mp','שֹׁמְרִים'], ['4','fp','שֹׁמְרוֹת'],
        ]
        rows_b = [['5','ms',''],['6','fs',''],['7','mp',''],['8','fp','']]
        ans_b  = [
            ['5','ms','שָׁמוּר'], ['6','fs','שְׁמוּרָה'],
            ['7','mp','שְׁמוּרִים'], ['8','fp','שְׁמוּרוֹת'],
        ]
        self.add_drill_with_answer_key(hdrs, rows_a, ans_a, col_ratios=cr,
                                       answer_heb_cols=[2],
                                       section_title='Part A — Qal Active Participle (שמר)',
                                       answer_title='Part A — Answer Key')
        hdrs_b = ['#', 'Form', 'Passive (שמר)']
        self.add_drill_with_answer_key(hdrs_b, rows_b, ans_b, col_ratios=cr,
                                       answer_heb_cols=[2],
                                       section_title='Part B — Qal Passive Participle / Qatûl (שמר)',
                                       answer_title='Part B — Answer Key')


def build_ch22_qal_participle_paradigm_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch22QalParticipleParadigmDrill,
        'Chapter 22 — Qal Participle Paradigm Drill',
        'BBH Chapter 22 · Qal Participle',
        ['hebrew', 'bbh', 'ch22', 'exercises', 'ch22-qal-participle-paradigm-drill'],
        'ch22-qal-participle-paradigm-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch24 — Niphal Paradigm Drill
# ---------------------------------------------------------------------------


class Ch24NiphalParadigmDrill(ExercisePDF):
    _instructions = (
        'Write the complete Niphal paradigm for the root קטל. '
        'Work conjugation by conjugation from memory. '
        'Key: נִ prefix in Perfect; dagesh forte in R1 + tsere in Imperfect.'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'PGN', 'Niphal form (קטל)']
        cr   = [0.06, 0.18, 0.76]
        # Perfect
        rows_pf = [['%d'%i,p,''] for i,p in enumerate(['3ms','3fs','2ms','2fs','1cs','3cp','2mp','2fp','1cp'],1)]
        ans_pf  = [
            ['1','3ms','נִקְטַל'],['2','3fs','נִקְטְלָה'],['3','2ms','נִקְטַלְתָּ'],
            ['4','2fs','נִקְטַלְתְּ'],['5','1cs','נִקְטַלְתִּי'],['6','3cp','נִקְטְלוּ'],
            ['7','2mp','נִקְטַלְתֶּם'],['8','2fp','נִקְטַלְתֶּן'],['9','1cp','נִקְטַלְנוּ'],
        ]
        # Imperfect
        rows_imp = [['%d'%(i+9),p,''] for i,p in enumerate(['3ms','3fs','2ms','2fs','1cs','3mp','3fp','2mp','2fp','1cp'],1)]
        ans_imp  = [
            ['10','3ms','יִקָּטֵל'],['11','3fs','תִּקָּטֵל'],['12','2ms','תִּקָּטֵל'],
            ['13','2fs','תִּקָּטְלִי'],['14','1cs','אֶקָּטֵל'],['15','3mp','יִקָּטְלוּ'],
            ['16','3fp','תִּקָּטַלְנָה'],['17','2mp','תִּקָּטְלוּ'],['18','2fp','תִּקָּטַלְנָה'],
            ['19','1cp','נִקָּטֵל'],
        ]
        # Imperative
        rows_imper = [['%d'%(i+19),p,''] for i,p in enumerate(['2ms','2fs','2mp','2fp'],1)]
        ans_imper  = [
            ['20','2ms','הִקָּטֵל'],['21','2fs','הִקָּטְלִי'],
            ['22','2mp','הִקָּטְלוּ'],['23','2fp','הִקָּטַלְנָה'],
        ]
        # IC + IA + Ptc
        hdrs_misc = ['#', 'Form', 'Niphal (קטל)']
        rows_misc = [
            ['24','Inf. Construct (bare)',''], ['25','Inf. Construct +לְ',''],
            ['26','Inf. Absolute',''],
            ['27','Participle ms',''], ['28','Participle fs',''],
            ['29','Participle mp',''], ['30','Participle fp',''],
        ]
        ans_misc  = [
            ['24','Inf. Construct (bare)','הִקָּטֵל'], ['25','Inf. Construct +לְ','לְהִקָּטֵל'],
            ['26','Inf. Absolute','נִקְטֹל'],
            ['27','Participle ms','נִקְטָל'], ['28','Participle fs','נִקְטֶלֶת'],
            ['29','Participle mp','נִקְטָלִים'], ['30','Participle fp','נִקְטָלוֹת'],
        ]

        for title_q, rows_q, ans_q in [
            ('Niphal Perfect', rows_pf, ans_pf),
            ('Niphal Imperfect', rows_imp, ans_imp),
            ('Niphal Imperative', rows_imper, ans_imper),
        ]:
            self.add_drill_with_answer_key(hdrs, rows_q, ans_q, col_ratios=cr,
                                           answer_heb_cols=[2],
                                           section_title=title_q,
                                           answer_title=f'{title_q} — Answer Key')
        self.add_drill_with_answer_key(hdrs_misc, rows_misc, ans_misc, col_ratios=cr,
                                       answer_heb_cols=[2],
                                       section_title='Niphal — Inf. Construct · Inf. Absolute · Participle',
                                       answer_title='Inf./Participle — Answer Key')


def build_ch24_niphal_paradigm_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch24NiphalParadigmDrill,
        'Chapter 24 — Niphal Paradigm Drill',
        'BBH Chapter 24 · Niphal Strong',
        ['hebrew', 'bbh', 'ch24', 'exercises', 'ch24-niphal-paradigm-drill'],
        'ch24-niphal-paradigm-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch26 — Hiphil Paradigm Drill
# ---------------------------------------------------------------------------


class Ch26HiphilParadigmDrill(ExercisePDF):
    _instructions = (
        'Write the complete Hiphil paradigm for the root קטל. '
        'Key: הִ prefix + chiriq in Perfect; patach under prefix in Imperfect; '
        'מַ prefix in Participle.'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'PGN', 'Hiphil form (קטל)']
        cr   = [0.06, 0.18, 0.76]
        rows_pf = [['%d'%i,p,''] for i,p in enumerate(['3ms','3fs','2ms','2fs','1cs','3cp','2mp','2fp','1cp'],1)]
        ans_pf  = [
            ['1','3ms','הִקְטִיל'],['2','3fs','הִקְטִילָה'],['3','2ms','הִקְטַלְתָּ'],
            ['4','2fs','הִקְטַלְתְּ'],['5','1cs','הִקְטַלְתִּי'],['6','3cp','הִקְטִילוּ'],
            ['7','2mp','הִקְטַלְתֶּם'],['8','2fp','הִקְטַלְתֶּן'],['9','1cp','הִקְטַלְנוּ'],
        ]
        rows_imp = [['%d'%(i+9),p,''] for i,p in enumerate(['3ms','3fs','2ms','2fs','1cs','3mp','3fp','2mp','2fp','1cp'],1)]
        ans_imp  = [
            ['10','3ms','יַקְטִיל'],['11','3fs','תַּקְטִיל'],['12','2ms','תַּקְטִיל'],
            ['13','2fs','תַּקְטִילִי'],['14','1cs','אַקְטִיל'],['15','3mp','יַקְטִילוּ'],
            ['16','3fp','תַּקְטֵלְנָה'],['17','2mp','תַּקְטִילוּ'],['18','2fp','תַּקְטֵלְנָה'],
            ['19','1cp','נַקְטִיל'],
        ]
        rows_imper = [['%d'%(i+19),p,''] for i,p in enumerate(['2ms','2fs','2mp','2fp'],1)]
        ans_imper  = [
            ['20','2ms','הַקְטֵל'],['21','2fs','הַקְטִילִי'],
            ['22','2mp','הַקְטִילוּ'],['23','2fp','הַקְטֵלְנָה'],
        ]
        hdrs_misc = ['#', 'Form', 'Hiphil (קטל)']
        rows_misc = [
            ['24','Inf. Construct (bare)',''], ['25','Inf. Construct +לְ',''],
            ['26','Inf. Absolute',''],
            ['27','Participle ms',''], ['28','Participle fs',''],
            ['29','Participle mp',''], ['30','Participle fp',''],
        ]
        ans_misc  = [
            ['24','Inf. Construct (bare)','הַקְטִיל'], ['25','Inf. Construct +לְ','לְהַקְטִיל'],
            ['26','Inf. Absolute','הַקְטֵל'],
            ['27','Participle ms','מַקְטִיל'], ['28','Participle fs','מַקְטֶלֶת'],
            ['29','Participle mp','מַקְטִילִים'], ['30','Participle fp','מַקְטִילוֹת'],
        ]
        for title_q, rows_q, ans_q in [
            ('Hiphil Perfect', rows_pf, ans_pf),
            ('Hiphil Imperfect', rows_imp, ans_imp),
            ('Hiphil Imperative', rows_imper, ans_imper),
        ]:
            self.add_drill_with_answer_key(hdrs, rows_q, ans_q, col_ratios=cr,
                                           answer_heb_cols=[2],
                                           section_title=title_q,
                                           answer_title=f'{title_q} — Answer Key')
        self.add_drill_with_answer_key(hdrs_misc, rows_misc, ans_misc, col_ratios=cr,
                                       answer_heb_cols=[2],
                                       section_title='Hiphil — Inf. Construct · Inf. Absolute · Participle',
                                       answer_title='Inf./Participle — Answer Key')


def build_ch26_hiphil_paradigm_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch26HiphilParadigmDrill,
        'Chapter 26 — Hiphil Paradigm Drill',
        'BBH Chapter 26 · Hiphil Strong',
        ['hebrew', 'bbh', 'ch26', 'exercises', 'ch26-hiphil-paradigm-drill'],
        'ch26-hiphil-paradigm-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch28 — Hophal Paradigm Drill
# ---------------------------------------------------------------------------


class Ch28HophalParadigmDrill(ExercisePDF):
    _instructions = (
        'Write the Hophal paradigm for the root מות. '
        'Note: there is NO Hophal Imperative — passives cannot be commanded. '
        'Key marker: שׁוּ/הוּ prefix (shureq) in Perfect/Imperfect; מוּ in Participle.'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'PGN', 'Hophal form (מות)']
        cr   = [0.06, 0.18, 0.76]
        rows_pf = [['%d'%i,p,''] for i,p in enumerate(['3ms','3fs','2ms','2fs','1cs','3cp','2mp','2fp','1cp'],1)]
        ans_pf  = [
            ['1','3ms','הוּמַת'],['2','3fs','הוּמְתָה'],['3','2ms','הוּמַתָּ'],
            ['4','2fs','הוּמַתְּ'],['5','1cs','הוּמַתִּי'],['6','3cp','הוּמְתוּ'],
            ['7','2mp','הוּמַתֶּם'],['8','2fp','הוּמַתֶּן'],['9','1cp','הוּמַתְנוּ'],
        ]
        rows_imp = [['%d'%(i+9),p,''] for i,p in enumerate(['3ms','3fs','2ms','2fs','1cs','3mp','3fp','2mp','2fp','1cp'],1)]
        ans_imp  = [
            ['10','3ms','יוּמַת'],['11','3fs','תּוּמַת'],['12','2ms','תּוּמַת'],
            ['13','2fs','תּוּמְתִי'],['14','1cs','אוּמַת'],['15','3mp','יוּמְתוּ'],
            ['16','3fp','תּוּמַתְנָה'],['17','2mp','תּוּמְתוּ'],['18','2fp','תּוּמַתְנָה'],
            ['19','1cp','נוּמַת'],
        ]
        hdrs_misc = ['#', 'Form', 'Hophal (מות)']
        rows_misc = [
            ['20','Inf. Construct (bare)',''], ['21','Inf. Construct +לְ',''],
            ['22','Inf. Absolute',''],
            ['23','Participle ms',''], ['24','Participle fs',''],
            ['25','Participle mp',''], ['26','Participle fp',''],
        ]
        ans_misc  = [
            ['20','Inf. Construct (bare)','הוּמַת'], ['21','Inf. Construct +לְ','לְהוּמַת'],
            ['22','Inf. Absolute','הוּמֵת'],
            ['23','Participle ms','מוּמָת'], ['24','Participle fs','מוּמָתֶת'],
            ['25','Participle mp','מוּמָתִים'], ['26','Participle fp','מוּמָתוֹת'],
        ]
        for title_q, rows_q, ans_q in [
            ('Hophal Perfect', rows_pf, ans_pf),
            ('Hophal Imperfect', rows_imp, ans_imp),
        ]:
            self.add_drill_with_answer_key(hdrs, rows_q, ans_q, col_ratios=cr,
                                           answer_heb_cols=[2],
                                           section_title=title_q,
                                           answer_title=f'{title_q} — Answer Key')
        self.add_drill_with_answer_key(hdrs_misc, rows_misc, ans_misc, col_ratios=cr,
                                       answer_heb_cols=[2],
                                       section_title='Hophal — Inf. Construct · Inf. Absolute · Participle',
                                       answer_title='Inf./Participle — Answer Key')


def build_ch28_hophal_paradigm_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch28HophalParadigmDrill,
        'Chapter 28 — Hophal Paradigm Drill',
        'BBH Chapter 28 · Hophal Strong',
        ['hebrew', 'bbh', 'ch28', 'exercises', 'ch28-hophal-paradigm-drill'],
        'ch28-hophal-paradigm-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch29 — Hophal Weak Paradigm Drill
# ---------------------------------------------------------------------------


class Ch29HophalWeakParadigmDrill(ExercisePDF):
    _instructions = (
        'Write the Hophal Weak forms. '
        'Part A uses נגד (I-נ root, qibbuts pattern — ֻ under prefix). '
        'Part B uses בוא (biconsonantal, shureq pattern). '
        'The qibbuts vs. shureq distinction is the key diagnostic.'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'PGN / Form', 'Hophal form']
        cr   = [0.06, 0.28, 0.66]

        rows_a = [
            ['1','Perfect 3ms',''], ['2','Perfect 3fs',''], ['3','Perfect 2ms',''],
            ['4','Perfect 1cs',''], ['5','Imperfect 3ms',''], ['6','Imperfect 3fs',''],
            ['7','Imperfect 3mp',''], ['8','Imperfect 1cp',''],
            ['9','Participle ms',''], ['10','Participle mp',''],
        ]
        ans_a = [
            ['1','Perfect 3ms','הֻגַּד'], ['2','Perfect 3fs','הֻגְּדָה'],
            ['3','Perfect 2ms','הֻגַּדְתָּ'], ['4','Perfect 1cs','הֻגַּדְתִּי'],
            ['5','Imperfect 3ms','יֻגַּד'], ['6','Imperfect 3fs','תֻּגַּד'],
            ['7','Imperfect 3mp','יֻגְּדוּ'], ['8','Imperfect 1cp','נֻגַּד'],
            ['9','Participle ms','מֻגָּד'], ['10','Participle mp','מֻגָּדִים'],
        ]
        rows_b = [
            ['11','Imperfect 3ms (בוא)',''], ['12','Participle ms (בוא)',''],
        ]
        ans_b = [
            ['11','Imperfect 3ms (בוא)','יוּבָא'], ['12','Participle ms (בוא)','מוּבָא'],
        ]
        self.add_drill_with_answer_key(hdrs, rows_a, ans_a, col_ratios=cr,
                                       answer_heb_cols=[2],
                                       section_title='Part A — Hophal Weak: נגד (I-נ, qibbuts)',
                                       answer_title='Part A — Answer Key')
        self.add_drill_with_answer_key(hdrs, rows_b, ans_b, col_ratios=cr,
                                       answer_heb_cols=[2],
                                       section_title='Part B — Hophal Weak: בוא (biconsonantal, shureq)',
                                       answer_title='Part B — Answer Key')


def build_ch29_hophal_weak_paradigm_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch29HophalWeakParadigmDrill,
        'Chapter 29 — Hophal Weak Paradigm Drill',
        'BBH Chapter 29 · Hophal Weak',
        ['hebrew', 'bbh', 'ch29', 'exercises', 'ch29-hophal-weak-paradigm-drill'],
        'ch29-hophal-weak-paradigm-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch30 — Piel Paradigm Drill
# ---------------------------------------------------------------------------


class Ch30PielParadigmDrill(ExercisePDF):
    _instructions = (
        'Write the complete Piel paradigm for the root דבר. '
        'Key marker: dagesh forte in R2 throughout all conjugations.'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'PGN', 'Piel form (דבר)']
        cr   = [0.06, 0.18, 0.76]
        rows_pf = [['%d'%i,p,''] for i,p in enumerate(['3ms','3fs','2ms','2fs','1cs','3cp','2mp','2fp','1cp'],1)]
        ans_pf  = [
            ['1','3ms','דִּבֵּר'],['2','3fs','דִּבְּרָה'],['3','2ms','דִּבַּרְתָּ'],
            ['4','2fs','דִּבַּרְתְּ'],['5','1cs','דִּבַּרְתִּי'],['6','3cp','דִּבְּרוּ'],
            ['7','2mp','דִּבַּרְתֶּם'],['8','2fp','דִּבַּרְתֶּן'],['9','1cp','דִּבַּרְנוּ'],
        ]
        rows_imp = [['%d'%(i+9),p,''] for i,p in enumerate(['3ms','3fs','2ms','2fs','1cs','3mp','3fp','2mp','2fp','1cp'],1)]
        ans_imp  = [
            ['10','3ms','יְדַבֵּר'],['11','3fs','תְּדַבֵּר'],['12','2ms','תְּדַבֵּר'],
            ['13','2fs','תְּדַבְּרִי'],['14','1cs','אֲדַבֵּר'],['15','3mp','יְדַבְּרוּ'],
            ['16','3fp','תְּדַבֵּרְנָה'],['17','2mp','תְּדַבְּרוּ'],['18','2fp','תְּדַבֵּרְנָה'],
            ['19','1cp','נְדַבֵּר'],
        ]
        rows_imper = [['%d'%(i+19),p,''] for i,p in enumerate(['2ms','2fs','2mp','2fp'],1)]
        ans_imper  = [
            ['20','2ms','דַּבֵּר'],['21','2fs','דַּבְּרִי'],
            ['22','2mp','דַּבְּרוּ'],['23','2fp','דַּבֵּרְנָה'],
        ]
        hdrs_misc = ['#', 'Form', 'Piel (דבר)']
        rows_misc = [
            ['24','Inf. Construct (bare)',''], ['25','Inf. Construct +לְ',''],
            ['26','Inf. Absolute',''],
            ['27','Participle ms',''], ['28','Participle fs',''],
            ['29','Participle mp',''], ['30','Participle fp',''],
        ]
        ans_misc  = [
            ['24','Inf. Construct (bare)','דַּבֵּר'], ['25','Inf. Construct +לְ','לְדַבֵּר'],
            ['26','Inf. Absolute','דַּבֵּר'],
            ['27','Participle ms','מְדַבֵּר'], ['28','Participle fs','מְדַבֶּרֶת'],
            ['29','Participle mp','מְדַבְּרִים'], ['30','Participle fp','מְדַבְּרוֹת'],
        ]
        for title_q, rows_q, ans_q in [
            ('Piel Perfect', rows_pf, ans_pf),
            ('Piel Imperfect', rows_imp, ans_imp),
            ('Piel Imperative', rows_imper, ans_imper),
        ]:
            self.add_drill_with_answer_key(hdrs, rows_q, ans_q, col_ratios=cr,
                                           answer_heb_cols=[2],
                                           section_title=title_q,
                                           answer_title=f'{title_q} — Answer Key')
        self.add_drill_with_answer_key(hdrs_misc, rows_misc, ans_misc, col_ratios=cr,
                                       answer_heb_cols=[2],
                                       section_title='Piel — Inf. Construct · Inf. Absolute · Participle',
                                       answer_title='Inf./Participle — Answer Key')


def build_ch30_piel_paradigm_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch30PielParadigmDrill,
        'Chapter 30 — Piel Paradigm Drill',
        'BBH Chapter 30 · Piel Strong',
        ['hebrew', 'bbh', 'ch30', 'exercises', 'ch30-piel-paradigm-drill'],
        'ch30-piel-paradigm-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch31 — Piel Weak Paradigm Drill (III-ה: גלה)
# ---------------------------------------------------------------------------


class Ch31PielWeakParadigmDrill(ExercisePDF):
    _instructions = (
        'Write the Piel Weak paradigm for the root גלה (III-ה: uncover/reveal). '
        'Note: final ה is retained in the 3ms Perfect; it drops before vowel suffixes.'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'PGN / Form', 'Piel form (גלה)']
        cr   = [0.06, 0.24, 0.70]

        rows_pf = [['%d'%i,p,''] for i,p in enumerate(['3ms','3fs','2ms','1cs','3cp'],1)]
        ans_pf  = [
            ['1','3ms','גִּלָּה'], ['2','3fs','גִּלְּתָה'], ['3','2ms','גִּלִּיתָ'],
            ['4','1cs','גִּלִּיתִי'], ['5','3cp','גִּלּוּ'],
        ]
        rows_imp = [['%d'%(i+5),p,''] for i,p in enumerate(['3ms','3fs','2ms','3mp','1cp'],1)]
        ans_imp  = [
            ['6','3ms','יְגַלֶּה'], ['7','3fs','תְּגַלֶּה'], ['8','2ms','תְּגַלֶּה'],
            ['9','3mp','יְגַלּוּ'], ['10','1cp','נְגַלֶּה'],
        ]
        rows_imper = [['%d'%(i+10),p,''] for i,p in enumerate(['2ms','2fs','2mp'],1)]
        ans_imper  = [
            ['11','2ms','גַּלֵּה'], ['12','2fs','גַּלִּי'], ['13','2mp','גַּלּוּ'],
        ]
        rows_ptc = [['14','Participle ms','']]
        ans_ptc  = [['14','Participle ms','מְגַלֶּה']]

        for title_q, rows_q, ans_q in [
            ('Piel Weak Perfect (גלה)', rows_pf, ans_pf),
            ('Piel Weak Imperfect (גלה)', rows_imp, ans_imp),
            ('Piel Weak Imperative (גלה)', rows_imper, ans_imper),
            ('Piel Weak Participle (גלה)', rows_ptc, ans_ptc),
        ]:
            self.add_drill_with_answer_key(hdrs, rows_q, ans_q, col_ratios=cr,
                                           answer_heb_cols=[2],
                                           section_title=title_q,
                                           answer_title=f'{title_q} — Answer Key')


def build_ch31_piel_weak_paradigm_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch31PielWeakParadigmDrill,
        'Chapter 31 — Piel Weak Paradigm Drill',
        'BBH Chapter 31 · Piel Weak',
        ['hebrew', 'bbh', 'ch31', 'exercises', 'ch31-piel-weak-paradigm-drill'],
        'ch31-piel-weak-paradigm-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch32 — Pual Paradigm Drill
# ---------------------------------------------------------------------------


class Ch32PualParadigmDrill(ExercisePDF):
    _instructions = (
        'Write the Pual (passive of Piel) paradigm for the root קטל. '
        'Key: qibbuts (ֻ) under R1 + dagesh forte in R2.'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'PGN / Form', 'Pual form (קטל)']
        cr   = [0.06, 0.24, 0.70]

        rows_pf = [['%d'%i,p,''] for i,p in enumerate(['3ms','3fs','2ms','3cp','1cs'],1)]
        ans_pf  = [
            ['1','3ms','קֻטַּל'], ['2','3fs','קֻטְּלָה'], ['3','2ms','קֻטַּלְתָּ'],
            ['4','3cp','קֻטְּלוּ'], ['5','1cs','קֻטַּלְתִּי'],
        ]
        rows_imp = [['%d'%(i+5),p,''] for i,p in enumerate(['3ms','3fs','2ms','3mp','1cp'],1)]
        ans_imp  = [
            ['6','3ms','יְקֻטַּל'], ['7','3fs','תְּקֻטַּל'], ['8','2ms','תְּקֻטַּל'],
            ['9','3mp','יְקֻטְּלוּ'], ['10','1cp','נְקֻטַּל'],
        ]
        rows_ptc = [['11','Participle ms',''],['12','Participle fs',''],
                    ['13','Participle mp',''],['14','Participle fp','']]
        ans_ptc  = [
            ['11','Participle ms','מְקֻטָּל'], ['12','Participle fs','מְקֻטֶּלֶת'],
            ['13','Participle mp','מְקֻטָּלִים'], ['14','Participle fp','מְקֻטָּלוֹת'],
        ]
        for title_q, rows_q, ans_q in [
            ('Pual Perfect (קטל)', rows_pf, ans_pf),
            ('Pual Imperfect (קטל)', rows_imp, ans_imp),
            ('Pual Participle (קטל)', rows_ptc, ans_ptc),
        ]:
            self.add_drill_with_answer_key(hdrs, rows_q, ans_q, col_ratios=cr,
                                           answer_heb_cols=[2],
                                           section_title=title_q,
                                           answer_title=f'{title_q} — Answer Key')


def build_ch32_pual_paradigm_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch32PualParadigmDrill,
        'Chapter 32 — Pual Paradigm Drill',
        'BBH Chapter 32 · Pual Strong',
        ['hebrew', 'bbh', 'ch32', 'exercises', 'ch32-pual-paradigm-drill'],
        'ch32-pual-paradigm-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch33 — Pual Weak Paradigm Drill (III-ה: בנה)
# ---------------------------------------------------------------------------


class Ch33PualWeakParadigmDrill(ExercisePDF):
    _instructions = (
        'Write the Pual Weak forms. '
        'Part A uses בנה (III-ה). '
        'Part B uses שאל (strong Pual — for comparison).'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'PGN / Form', 'Pual form']
        cr   = [0.06, 0.24, 0.70]

        rows_a = [['%d'%i,p,''] for i,p in enumerate([
            'Perfect 3ms (בנה)','Perfect 3fs (בנה)','Perfect 3cp (בנה)',
            'Imperfect 3ms (בנה)','Imperfect 3fs (בנה)','Imperfect 3mp (בנה)',
            'Participle ms (בנה)','Participle mp (בנה)',
        ],1)]
        ans_a = [
            ['1','Perfect 3ms (בנה)','בֻּנָּה'], ['2','Perfect 3fs (בנה)','בֻּנְּתָה'],
            ['3','Perfect 3cp (בנה)','בֻּנּוּ'], ['4','Imperfect 3ms (בנה)','יְבֻנֶּה'],
            ['5','Imperfect 3fs (בנה)','תְּבֻנֶּה'], ['6','Imperfect 3mp (בנה)','יְבֻנּוּ'],
            ['7','Participle ms (בנה)','מְבֻנֶּה'], ['8','Participle mp (בנה)','מְבֻנִּים'],
        ]
        rows_b = [
            ['9','Perfect 3ms (שאל)',''], ['10','Imperfect 3ms (שאל)',''],
        ]
        ans_b = [
            ['9','Perfect 3ms (שאל)','שֻׁאַל'], ['10','Imperfect 3ms (שאל)','יְשֻׁאַל'],
        ]
        self.add_drill_with_answer_key(hdrs, rows_a, ans_a, col_ratios=cr,
                                       answer_heb_cols=[2],
                                       section_title='Part A — Pual Weak: בנה (III-ה)',
                                       answer_title='Part A — Answer Key')
        self.add_drill_with_answer_key(hdrs, rows_b, ans_b, col_ratios=cr,
                                       answer_heb_cols=[2],
                                       section_title='Part B — Pual Strong: שאל (comparison)',
                                       answer_title='Part B — Answer Key')


def build_ch33_pual_weak_paradigm_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch33PualWeakParadigmDrill,
        'Chapter 33 — Pual Weak Paradigm Drill',
        'BBH Chapter 33 · Pual Weak',
        ['hebrew', 'bbh', 'ch33', 'exercises', 'ch33-pual-weak-paradigm-drill'],
        'ch33-pual-weak-paradigm-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch32 — Pual Function Sort (Strong Roots)
# ---------------------------------------------------------------------------


class Ch32FunctionSortExercise(ExercisePDF):

    def _build(self) -> None:
        self.add_instructions(
            'The Pual is always the passive of the Piel. '
            'For each of the 20 Pual forms below: '
            '(1) give the Piel active meaning; (2) translate the Pual passive form. '
            'Answer key is on the last page.'
        )
        self.add_note(
            'Pual diagnostic: Qibbuts (u-dot) under R1 + Dagesh Forte in R2. '
            'When R2 is a guttural (r, kh, etc.), dagesh is rejected and the '
            'preceding vowel lengthens: qibbuts -> holem (e.g., borakh not burrakk).'
        )
        hdr = ['#', 'Form', 'Root', 'Conjugation', 'Piel Active Meaning', 'Pual Passive Translation']
        cr  = [0.04, 0.14, 0.09, 0.18, 0.27, 0.28]
        rows = [
            ['1',  'קֻטַּל',   'קטל',  'Perfect 3ms',   '', ''],
            ['2',  'כֻּבַּד',   'כבד',  'Perfect 3ms',   '', ''],
            ['3',  'בֹּרַךְ',   'ברך',  'Perfect 3ms',   '', ''],
            ['4',  'שֻׁלַּח',   'שׁלח', 'Perfect 3ms',   '', ''],
            ['5',  'דֻּבַּר',   'דבר',  'Perfect 3ms',   '', ''],
            ['6',  'שֻׁמַּר',   'שׁמר', 'Perfect 3ms',   '', ''],
            ['7',  'גֹּרַשׁ',   'גרשׁ', 'Perfect 3ms',   '', ''],
            ['8',  'סֻפַּר',    'ספר',  'Perfect 3ms',   '', ''],
            ['9',  'כֻּסָּה',   'כסה',  'Perfect 3ms',   '', ''],
            ['10', 'יְקֻטַּל',  'קטל',  'Imperfect 3ms', '', ''],
            ['11', 'יְבֹרַךְ',  'ברך',  'Imperfect 3ms', '', ''],
            ['12', 'יְשֻׁלַּח', 'שׁלח', 'Imperfect 3ms', '', ''],
            ['13', 'יְכֻבַּד',  'כבד',  'Imperfect 3ms', '', ''],
            ['14', 'יְסֻפַּר',  'ספר',  'Imperfect 3ms', '', ''],
            ['15', 'יְגֹרַשׁ',  'גרשׁ', 'Imperfect 3ms', '', ''],
            ['16', 'מְקֻטָּל',  'קטל',  'Participle ms', '', ''],
            ['17', 'מְבֹרָךְ',  'ברך',  'Participle ms', '', ''],
            ['18', 'מְשֻׁלָּח', 'שׁלח', 'Participle ms', '', ''],
            ['19', 'כֻּבְּדוּ', 'כבד',  'Perfect 3cp',   '', ''],
            ['20', 'שֻׁלְּחוּ', 'שׁלח', 'Perfect 3cp',   '', ''],
        ]
        ans = [
            ['1',  'קֻטַּל',   'קטל',  'Perfect 3ms',   'to kill (intensively)', 'he was killed'],
            ['2',  'כֻּבַּד',   'כבד',  'Perfect 3ms',   'to honor',              'he was honored'],
            ['3',  'בֹּרַךְ',   'ברך',  'Perfect 3ms',   'to bless',              'he was blessed'],
            ['4',  'שֻׁלַּח',   'שׁלח', 'Perfect 3ms',   'to send away / release','he was sent away'],
            ['5',  'דֻּבַּר',   'דבר',  'Perfect 3ms',   'to speak',              'it was spoken'],
            ['6',  'שֻׁמַּר',   'שׁמר', 'Perfect 3ms',   'to guard / watch',      'he was guarded'],
            ['7',  'גֹּרַשׁ',   'גרשׁ', 'Perfect 3ms',   'to drive out / expel',  'he was driven out'],
            ['8',  'סֻפַּר',    'ספר',  'Perfect 3ms',   'to recount / tell',     'it was told / recounted'],
            ['9',  'כֻּסָּה',   'כסה',  'Perfect 3ms',   'to cover',              'it was covered'],
            ['10', 'יְקֻטַּל',  'קטל',  'Imperfect 3ms', 'to kill',               'he will be killed'],
            ['11', 'יְבֹרַךְ',  'ברך',  'Imperfect 3ms', 'to bless',              'he will be blessed'],
            ['12', 'יְשֻׁלַּח', 'שׁלח', 'Imperfect 3ms', 'to send / release',     'he will be sent'],
            ['13', 'יְכֻבַּד',  'כבד',  'Imperfect 3ms', 'to honor',              'he will be honored'],
            ['14', 'יְסֻפַּר',  'ספר',  'Imperfect 3ms', 'to recount / tell',     'it will be told'],
            ['15', 'יְגֹרַשׁ',  'גרשׁ', 'Imperfect 3ms', 'to drive out',          'he will be driven out'],
            ['16', 'מְקֻטָּל',  'קטל',  'Participle ms', 'to kill',               'one being killed'],
            ['17', 'מְבֹרָךְ',  'ברך',  'Participle ms', 'to bless',              'one being blessed'],
            ['18', 'מְשֻׁלָּח', 'שׁלח', 'Participle ms', 'to send / release',     'one being sent'],
            ['19', 'כֻּבְּדוּ', 'כבד',  'Perfect 3cp',   'to honor',              'they were honored'],
            ['20', 'שֻׁלְּחוּ', 'שׁלח', 'Perfect 3cp',   'to send away',          'they were sent away'],
        ]
        self.add_drill_with_answer_key(
            hdr, rows, ans,
            col_ratios=cr,
            heb_cols=[1, 2],
            answer_heb_cols=[1, 2],
            section_title='Pual Function Sort — 20 Strong-Root Forms',
            answer_title='Answer Key',
        )


def build_ch32_function_sort_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch32FunctionSortExercise,
        'Chapter 32 — Pual Function Sort',
        'BBH Chapter 32 · Pual Strong Verbs',
        ['hebrew', 'bbh', 'ch32', 'exercises', 'ch32-function-sort'],
        'ch32-function-sort.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Ch32 — Qal–Piel–Pual Contrast Drill (Strong Roots)
# ---------------------------------------------------------------------------


class Ch32QalPielPualContrastExercise(ExercisePDF):

    def _build(self) -> None:
        self.add_instructions(
            'Each triplet shows the same root in Qal, Piel, and Pual (Perfect 3ms). '
            'For each form: (1) identify the stem, (2) parse fully, (3) translate. '
            'Focus on the R1 vowel: variable (Qal), hiriq/tsere (Piel), qibbuts/holem (Pual). '
            'Answer key is on the last page.'
        )
        self.add_note(
            'Stem contrast (Perfect 3ms): Qal = qamets or tsere under R1, no dagesh in R2.  '
            'Piel = hiriq or tsere under R1 + dagesh forte in R2.  '
            'Pual = qibbuts under R1 + dagesh forte in R2 '
            '(holem when R2 is guttural and rejects dagesh).'
        )
        hdr = ['#', 'Form', 'Stem', 'Conjugation', 'PGN', 'Translation']
        cr  = [0.04, 0.16, 0.12, 0.20, 0.10, 0.38]

        triplets = [
            ('Triplet 1 — Root: brk (bless)', [
                ['1', 'בָּרַךְ', '', 'Perfect', '3ms', ''],
                ['2', 'בֵּרַךְ', '', 'Perfect', '3ms', ''],
                ['3', 'בֹּרַךְ', '', 'Perfect', '3ms', ''],
            ], [
                ['1', 'בָּרַךְ', 'Qal',  'Perfect', '3ms', 'he knelt'],
                ['2', 'בֵּרַךְ', 'Piel', 'Perfect', '3ms', 'he blessed'],
                ['3', 'בֹּרַךְ', 'Pual', 'Perfect', '3ms', 'he was blessed'],
            ]),
            ('Triplet 2 — Root: shlkh (send)', [
                ['4', 'שָׁלַח', '', 'Perfect', '3ms', ''],
                ['5', 'שִׁלַּח', '', 'Perfect', '3ms', ''],
                ['6', 'שֻׁלַּח', '', 'Perfect', '3ms', ''],
            ], [
                ['4', 'שָׁלַח', 'Qal',  'Perfect', '3ms', 'he sent'],
                ['5', 'שִׁלַּח', 'Piel', 'Perfect', '3ms', 'he sent away / released'],
                ['6', 'שֻׁלַּח', 'Pual', 'Perfect', '3ms', 'he was sent away'],
            ]),
            ('Triplet 3 — Root: dbr (speak)', [
                ['7',  'דָּבַר', '', 'Perfect', '3ms', ''],
                ['8',  'דִּבֶּר', '', 'Perfect', '3ms', ''],
                ['9',  'דֻּבַּר', '', 'Perfect', '3ms', ''],
            ], [
                ['7',  'דָּבַר', 'Qal',  'Perfect', '3ms', 'he spoke (rare)'],
                ['8',  'דִּבֶּר', 'Piel', 'Perfect', '3ms', 'he spoke'],
                ['9',  'דֻּבַּר', 'Pual', 'Perfect', '3ms', 'it was spoken'],
            ]),
            ('Triplet 4 — Root: kbd (honor)', [
                ['10', 'כָּבֵד', '', 'Perfect', '3ms', ''],
                ['11', 'כִּבֵּד', '', 'Perfect', '3ms', ''],
                ['12', 'כֻּבַּד', '', 'Perfect', '3ms', ''],
            ], [
                ['10', 'כָּבֵד', 'Qal',  'Perfect', '3ms', 'he was heavy / honored (stative)'],
                ['11', 'כִּבֵּד', 'Piel', 'Perfect', '3ms', 'he honored'],
                ['12', 'כֻּבַּד', 'Pual', 'Perfect', '3ms', 'he was honored'],
            ]),
            ('Triplet 5 — Root: spr (count / tell)', [
                ['13', 'סָפַר', '', 'Perfect', '3ms', ''],
                ['14', 'סִפֵּר', '', 'Perfect', '3ms', ''],
                ['15', 'סֻפַּר', '', 'Perfect', '3ms', ''],
            ], [
                ['13', 'סָפַר', 'Qal',  'Perfect', '3ms', 'he counted'],
                ['14', 'סִפֵּר', 'Piel', 'Perfect', '3ms', 'he recounted / told'],
                ['15', 'סֻפַּר', 'Pual', 'Perfect', '3ms', 'it was told / recounted'],
            ]),
        ]

        for title, rows, ans in triplets:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1], show_answers=False)
            self.add_section_break()

        self.add_reflection([
            'Across all five triplets, the R1 vowel follows a pattern: qamets or tsere (Qal), '
            'hiriq or tsere (Piel), qibbuts (Pual). Write this as a three-step diagnostic rule.',
            'Root brk (triplets 1, 3): the resh (r) rejects dagesh forte in R2. '
            'How does this affect the Piel vowel (tsere under b instead of hiriq)? '
            'And the Pual vowel (holem instead of qibbuts)?',
            'Root kbd (triplet 4): the Qal is stative (he was heavy). '
            'What does the Piel add to make it factitive? '
            'What grammatical role does the human recipient play in Piel vs. Pual?',
        ])

        self.add_section_heading('Answer Key')
        for title, rows, ans in triplets:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=True, answer_rows=ans)


def build_ch32_qal_piel_pual_contrast_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch32QalPielPualContrastExercise,
        'Chapter 32 — Qal–Piel–Pual Contrast Drill (Strong Roots)',
        'BBH Chapter 32 · Pual Strong Verbs',
        ['hebrew', 'bbh', 'ch32', 'exercises', 'ch32-qal-piel-pual-contrast'],
        'ch32-qal-piel-pual-contrast.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Ch32 — Stem-ID Drill (Strong Roots)
# ---------------------------------------------------------------------------


class Ch32StemIdDrill(ExercisePDF):
    _instructions = (
        'For each of the 24 verb forms, identify the stem (Qal / Piel / Pual), '
        'then parse fully (conjugation, PGN) and translate. '
        'All forms are from strong roots. Answer key is on the last page.'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        self.add_note(
            'Quick test: R1 has qibbuts (u-dot) or holem where guttural R2 blocks dagesh? -> Pual.  '
            'R1 has hiriq/tsere with dagesh forte in R2? -> Piel.  '
            'Plain vowel, no dagesh forte in R2? -> Qal.'
        )
        hdrs = ['#', 'Hebrew Form', 'Stem', 'Conjugation', 'PGN', 'Root', 'Translation']
        cr   = [0.04, 0.16, 0.11, 0.18, 0.10, 0.09, 0.32]
        rows = [
            ['1',  'דָּבַר',     '', '', '', 'דבר', ''],
            ['2',  'דִּבֶּר',    '', '', '', 'דבר', ''],
            ['3',  'דֻּבַּר',    '', '', '', 'דבר', ''],
            ['4',  'שָׁלַח',     '', '', '', 'שׁלח', ''],
            ['5',  'שִׁלַּח',    '', '', '', 'שׁלח', ''],
            ['6',  'שֻׁלַּח',    '', '', '', 'שׁלח', ''],
            ['7',  'כָּבֵד',     '', '', '', 'כבד', ''],
            ['8',  'כִּבֵּד',    '', '', '', 'כבד', ''],
            ['9',  'כֻּבַּד',    '', '', '', 'כבד', ''],
            ['10', 'יְדַבֵּר',   '', '', '', 'דבר', ''],
            ['11', 'יִדְבַּר',   '', '', '', 'דבר', ''],
            ['12', 'יְדֻבַּר',   '', '', '', 'דבר', ''],
            ['13', 'יְשַׁלַּח',  '', '', '', 'שׁלח', ''],
            ['14', 'יִשְׁלַח',   '', '', '', 'שׁלח', ''],
            ['15', 'יְשֻׁלַּח',  '', '', '', 'שׁלח', ''],
            ['16', 'וַיְדַבֵּר', '', '', '', 'דבר', ''],
            ['17', 'וַיִּדְבַּר','', '', '', 'דבר', ''],
            ['18', 'וַיְדֻבַּר', '', '', '', 'דבר', ''],
            ['19', 'דַּבֵּר',    '', '', '', 'דבר', ''],
            ['20', 'דְּבַר',     '', '', '', 'דבר', ''],
            ['21', 'מְדַבֵּר',   '', '', '', 'דבר', ''],
            ['22', 'דֹּבֵר',     '', '', '', 'דבר', ''],
            ['23', 'מְדֻבָּר',   '', '', '', 'דבר', ''],
            ['24', 'סֻפַּר',     '', '', '', 'ספר', ''],
        ]
        ans = [
            ['1',  'דָּבַר',     'Qal',  'Perfect',    '3ms', 'דבר', 'he spoke (rare)'],
            ['2',  'דִּבֶּר',    'Piel', 'Perfect',    '3ms', 'דבר', 'he spoke'],
            ['3',  'דֻּבַּר',    'Pual', 'Perfect',    '3ms', 'דבר', 'it was spoken'],
            ['4',  'שָׁלַח',     'Qal',  'Perfect',    '3ms', 'שׁלח', 'he sent'],
            ['5',  'שִׁלַּח',    'Piel', 'Perfect',    '3ms', 'שׁלח', 'he sent away / released'],
            ['6',  'שֻׁלַּח',    'Pual', 'Perfect',    '3ms', 'שׁלח', 'he was sent away'],
            ['7',  'כָּבֵד',     'Qal',  'Perfect',    '3ms', 'כבד', 'he was heavy / honored (stative)'],
            ['8',  'כִּבֵּד',    'Piel', 'Perfect',    '3ms', 'כבד', 'he honored'],
            ['9',  'כֻּבַּד',    'Pual', 'Perfect',    '3ms', 'כבד', 'he was honored'],
            ['10', 'יְדַבֵּר',   'Piel', 'Imperfect',  '3ms', 'דבר', 'he will speak'],
            ['11', 'יִדְבַּר',   'Qal',  'Imperfect',  '3ms', 'דבר', 'he will speak (rare)'],
            ['12', 'יְדֻבַּר',   'Pual', 'Imperfect',  '3ms', 'דבר', 'it will be spoken'],
            ['13', 'יְשַׁלַּח',  'Piel', 'Imperfect',  '3ms', 'שׁלח', 'he will send away'],
            ['14', 'יִשְׁלַח',   'Qal',  'Imperfect',  '3ms', 'שׁלח', 'he will send'],
            ['15', 'יְשֻׁלַּח',  'Pual', 'Imperfect',  '3ms', 'שׁלח', 'he will be sent'],
            ['16', 'וַיְדַבֵּר', 'Piel', 'Wayyiqtol',  '3ms', 'דבר', 'and he spoke'],
            ['17', 'וַיִּדְבַּר','Qal',  'Wayyiqtol',  '3ms', 'דבר', 'and he spoke (rare)'],
            ['18', 'וַיְדֻבַּר', 'Pual', 'Wayyiqtol',  '3ms', 'דבר', 'and it was spoken'],
            ['19', 'דַּבֵּר',    'Piel', 'Imperative', '2ms', 'דבר', 'speak!'],
            ['20', 'דְּבַר',     'Qal',  'Imperative', '2ms', 'דבר', 'speak! (rare)'],
            ['21', 'מְדַבֵּר',   'Piel', 'Participle', 'ms',  'דבר', 'speaking / one who speaks'],
            ['22', 'דֹּבֵר',     'Qal',  'Participle', 'ms',  'דבר', 'speaking / one who speaks'],
            ['23', 'מְדֻבָּר',   'Pual', 'Participle', 'ms',  'דבר', 'being spoken'],
            ['24', 'סֻפַּר',     'Pual', 'Perfect',    '3ms', 'ספר', 'it was told / recounted'],
        ]
        self.add_drill_with_answer_key(
            hdrs, rows, ans,
            col_ratios=cr,
            heb_cols=[1, 5],
            answer_heb_cols=[1, 5],
            section_title='Qal / Piel / Pual — Strong Roots (24 forms)',
            answer_title='Answer Key',
        )


def build_ch32_stem_id_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch32StemIdDrill,
        'Chapter 32 — Qal / Piel / Pual Stem-ID Drill (Strong Roots)',
        'BBH Chapter 32 · Pual Strong Verbs',
        ['hebrew', 'bbh', 'ch32', 'exercises', 'ch32-stem-id-drill'],
        'ch32-stem-id-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch33 — Qal–Piel–Pual Contrast Drill (Weak Roots)
# ---------------------------------------------------------------------------


class Ch33QalPielPualContrastExercise(ExercisePDF):

    def _build(self) -> None:
        self.add_instructions(
            'Each triplet shows the same weak root in Qal, Piel, and Pual (Perfect 3ms). '
            'For each form: (1) identify the stem, (2) parse fully, (3) translate. '
            'Watch for III-he endings and guttural compensatory lengthening. '
            'Answer key is on the last page.'
        )
        self.add_note(
            'III-he Pual Perfect 3ms: qibbuts under R1 + dagesh in R2 + final qamets-heh.  '
            'R2=r rejects dagesh: qibbuts lengthens to holem (borakh not burrakk).  '
            'I-guttural R1: guttural takes qibbuts (Pual) or hiriq (Piel) but does not '
            'change the stem vowel identity.'
        )
        hdr = ['#', 'Form', 'Stem', 'Conjugation', 'PGN', 'Translation']
        cr  = [0.04, 0.16, 0.12, 0.20, 0.10, 0.38]

        triplets = [
            ('Triplet 1 — Root: glh (III-he)', [
                ['1', 'גָּלָה', '', 'Perfect', '3ms', ''],
                ['2', 'גִּלָּה', '', 'Perfect', '3ms', ''],
                ['3', 'גֻּלָּה', '', 'Perfect', '3ms', ''],
            ], [
                ['1', 'גָּלָה', 'Qal',  'Perfect', '3ms', 'he went into exile / uncovered'],
                ['2', 'גִּלָּה', 'Piel', 'Perfect', '3ms', 'he revealed / uncovered'],
                ['3', 'גֻּלָּה', 'Pual', 'Perfect', '3ms', 'he was revealed / uncovered'],
            ]),
            ('Triplet 2 — Root: klh (III-he)', [
                ['4', 'כָּלָה', '', 'Perfect', '3ms', ''],
                ['5', 'כִּלָּה', '', 'Perfect', '3ms', ''],
                ['6', 'כֻּלָּה', '', 'Perfect', '3ms', ''],
            ], [
                ['4', 'כָּלָה', 'Qal',  'Perfect', '3ms', 'he finished / ceased'],
                ['5', 'כִּלָּה', 'Piel', 'Perfect', '3ms', 'he completed / finished off'],
                ['6', 'כֻּלָּה', 'Pual', 'Perfect', '3ms', 'he was finished / consumed'],
            ]),
            ('Triplet 3 — Root: brk (R2=r)', [
                ['7',  'בָּרַךְ', '', 'Perfect', '3ms', ''],
                ['8',  'בֵּרַךְ', '', 'Perfect', '3ms', ''],
                ['9',  'בֹּרַךְ', '', 'Perfect', '3ms', ''],
            ], [
                ['7',  'בָּרַךְ', 'Qal',  'Perfect', '3ms', 'he knelt'],
                ['8',  'בֵּרַךְ', 'Piel', 'Perfect', '3ms', 'he blessed'],
                ['9',  'בֹּרַךְ', 'Pual', 'Perfect', '3ms', 'he was blessed'],
            ]),
            ('Triplet 4 — Root: anh (III-he, I-guttural)', [
                ['10', 'עָנָה', '', 'Perfect', '3ms', ''],
                ['11', 'עִנָּה', '', 'Perfect', '3ms', ''],
                ['12', 'עֻנָּה', '', 'Perfect', '3ms', ''],
            ], [
                ['10', 'עָנָה', 'Qal',  'Perfect', '3ms', 'he answered'],
                ['11', 'עִנָּה', 'Piel', 'Perfect', '3ms', 'he afflicted / humbled'],
                ['12', 'עֻנָּה', 'Pual', 'Perfect', '3ms', 'he was afflicted'],
            ]),
            ('Triplet 5 — Root: khyh (III-he)', [
                ['13', 'חָיָה', '', 'Perfect', '3ms', ''],
                ['14', 'חִיָּה', '', 'Perfect', '3ms', ''],
                ['15', 'חֻיָּה', '', 'Perfect', '3ms', ''],
            ], [
                ['13', 'חָיָה', 'Qal',  'Perfect', '3ms', 'he lived'],
                ['14', 'חִיָּה', 'Piel', 'Perfect', '3ms', 'he kept alive'],
                ['15', 'חֻיָּה', 'Pual', 'Perfect', '3ms', 'he was kept alive'],
            ]),
        ]

        for title, rows, ans in triplets:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1], show_answers=False)
            self.add_section_break()

        self.add_reflection([
            'Compare Triplet 1 (glh, III-he) and Triplet 3 (brk, R2=r). '
            'Both are "weak" but in different ways. Describe the weak-root change '
            'in each and how it affects the Pual form specifically.',
            'Triplets 1, 2, 4, 5 all end in qamets-heh in the Pual Perfect 3ms. '
            'What marks the difference between the Piel and Pual in these III-he forms '
            'when R1 is not distinctive? (Hint: look at both R1 vowel and R2 dagesh.)',
            'Root anh (triplet 4) is both III-he and I-guttural. '
            'Did the I-guttural status change anything about the Pual form? '
            'Why or why not?',
        ])

        self.add_section_heading('Answer Key')
        for title, rows, ans in triplets:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=True, answer_rows=ans)


def build_ch33_qal_piel_pual_contrast_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch33QalPielPualContrastExercise,
        'Chapter 33 — Qal–Piel–Pual Contrast Drill (Weak Roots)',
        'BBH Chapter 33 · Pual Weak Verbs',
        ['hebrew', 'bbh', 'ch33', 'exercises', 'ch33-qal-piel-pual-contrast'],
        'ch33-qal-piel-pual-contrast.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Ch33 — Pual Function Sort (Weak Roots)
# ---------------------------------------------------------------------------


class Ch33FunctionSortExercise(ExercisePDF):

    def _build(self) -> None:
        self.add_instructions(
            'The Pual is always the passive of the Piel. '
            'For each of the 18 weak-root Pual forms below: '
            '(1) give the Piel active meaning; (2) translate the Pual passive form. '
            'Answer key is on the last page.'
        )
        self.add_note(
            'III-he endings: Perfect 3ms ends in qamets-heh; Imperfect 3ms and Participle ms '
            'end in tsere-heh.  '
            'R2=r: qibbuts lengthens to holem (borakh, yevorakh, mevorakk).  '
            'Perfect 3fs: qibbuts-R1 + shewa-R2 + tah suffix.  '
            'Perfect 3cp: qibbuts-R1 + dagesh-R2 + vav suffix.'
        )
        hdr = ['#', 'Form', 'Root', 'Weak Type', 'Conjugation', 'Piel Active', 'Pual Passive']
        cr  = [0.04, 0.13, 0.08, 0.13, 0.17, 0.22, 0.23]
        rows = [
            ['1',  'גֻּלָּה',   'גלה', 'III-he',       'Perfect 3ms',   '', ''],
            ['2',  'כֻּלָּה',   'כלה', 'III-he',       'Perfect 3ms',   '', ''],
            ['3',  'בֹּרַךְ',   'ברך', 'R2=r',         'Perfect 3ms',   '', ''],
            ['4',  'עֻנָּה',    'ענה', 'III-he, I-gutt','Perfect 3ms',  '', ''],
            ['5',  'חֻיָּה',    'חיה', 'III-he',       'Perfect 3ms',   '', ''],
            ['6',  'יְגֻלֶּה',  'גלה', 'III-he',       'Imperfect 3ms', '', ''],
            ['7',  'יְכֻלֶּה',  'כלה', 'III-he',       'Imperfect 3ms', '', ''],
            ['8',  'יְבֹרַךְ',  'ברך', 'R2=r',         'Imperfect 3ms', '', ''],
            ['9',  'יְעֻנֶּה',  'ענה', 'III-he, I-gutt','Imperfect 3ms','', ''],
            ['10', 'יְחֻיֶּה',  'חיה', 'III-he',       'Imperfect 3ms', '', ''],
            ['11', 'מְגֻלֶּה',  'גלה', 'III-he',       'Participle ms', '', ''],
            ['12', 'מְכֻלֶּה',  'כלה', 'III-he',       'Participle ms', '', ''],
            ['13', 'מְבֹרָךְ',  'ברך', 'R2=r',         'Participle ms', '', ''],
            ['14', 'גֻּלְתָּה', 'גלה', 'III-he',       'Perfect 3fs',   '', ''],
            ['15', 'בֹּרֲכוּ', 'ברך', 'R2=r',         'Perfect 3cp',   '', ''],
            ['16', 'כֻּלּוּ',   'כלה', 'III-he',       'Perfect 3cp',   '', ''],
            ['17', 'צֻוָּה',    'צוה', 'III-he',       'Perfect 3ms',   '', ''],
            ['18', 'שֻׁנָּה',   'שׁנה', 'III-he',       'Perfect 3ms',   '', ''],
        ]
        ans = [
            ['1',  'גֻּלָּה',   'גלה', 'III-he',       'Perfect 3ms',   'to reveal / uncover', 'it was revealed'],
            ['2',  'כֻּלָּה',   'כלה', 'III-he',       'Perfect 3ms',   'to complete / destroy','it was finished / consumed'],
            ['3',  'בֹּרַךְ',   'ברך', 'R2=r',         'Perfect 3ms',   'to bless',             'he was blessed'],
            ['4',  'עֻנָּה',    'ענה', 'III-he, I-gutt','Perfect 3ms',  'to afflict / humble',  'he was afflicted'],
            ['5',  'חֻיָּה',    'חיה', 'III-he',       'Perfect 3ms',   'to keep alive',        'he was kept alive'],
            ['6',  'יְגֻלֶּה',  'גלה', 'III-he',       'Imperfect 3ms', 'to reveal',            'it will be revealed'],
            ['7',  'יְכֻלֶּה',  'כלה', 'III-he',       'Imperfect 3ms', 'to complete / destroy','it will be finished'],
            ['8',  'יְבֹרַךְ',  'ברך', 'R2=r',         'Imperfect 3ms', 'to bless',             'he will be blessed'],
            ['9',  'יְעֻנֶּה',  'ענה', 'III-he, I-gutt','Imperfect 3ms','to afflict',           'he will be afflicted'],
            ['10', 'יְחֻיֶּה',  'חיה', 'III-he',       'Imperfect 3ms', 'to keep alive',        'he will be kept alive'],
            ['11', 'מְגֻלֶּה',  'גלה', 'III-he',       'Participle ms', 'to reveal',            'one being revealed'],
            ['12', 'מְכֻלֶּה',  'כלה', 'III-he',       'Participle ms', 'to complete / destroy','one being consumed'],
            ['13', 'מְבֹרָךְ',  'ברך', 'R2=r',         'Participle ms', 'to bless',             'one being blessed'],
            ['14', 'גֻּלְתָּה', 'גלה', 'III-he',       'Perfect 3fs',   'to reveal',            'it was revealed (3fs)'],
            ['15', 'בֹּרֲכוּ', 'ברך', 'R2=r',         'Perfect 3cp',   'to bless',             'they were blessed'],
            ['16', 'כֻּלּוּ',   'כלה', 'III-he',       'Perfect 3cp',   'to complete / destroy','they were consumed / finished'],
            ['17', 'צֻוָּה',    'צוה', 'III-he',       'Perfect 3ms',   'to command',           'he was commanded'],
            ['18', 'שֻׁנָּה',   'שׁנה', 'III-he',       'Perfect 3ms',   'to change',            'it was changed'],
        ]
        self.add_drill_with_answer_key(
            hdr, rows, ans,
            col_ratios=cr,
            heb_cols=[1, 2],
            answer_heb_cols=[1, 2],
            section_title='Pual Function Sort — 18 Weak-Root Forms',
            answer_title='Answer Key',
        )


def build_ch33_function_sort_exercise(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch33FunctionSortExercise,
        'Chapter 33 — Pual Function Sort (Weak Roots)',
        'BBH Chapter 33 · Pual Weak Verbs',
        ['hebrew', 'bbh', 'ch33', 'exercises', 'ch33-function-sort'],
        'ch33-function-sort.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# Ch33 — Stem-ID Drill (Weak Roots)
# ---------------------------------------------------------------------------


class Ch33StemIdDrill(ExercisePDF):
    _instructions = (
        'For each of the 24 verb forms, identify the stem (Qal / Piel / Pual), '
        'then parse fully (conjugation, PGN) and translate. '
        'All roots are weak (III-he or guttural). Answer key is on the last page.'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        self.add_note(
            'III-he Pual Perfect 3ms: qibbuts-R1 + dagesh-R2 + qamets-heh.  '
            'III-he Pual Imperfect 3ms: yeh prefix + qibbuts-R1 + dagesh-R2 + tsere-heh.  '
            'III-he Pual Participle ms: mem prefix + qibbuts-R1 + dagesh-R2 + tsere-heh.  '
            'R2=r: Piel -> tsere under R1; Pual -> holem under R1 (both without dagesh in r).'
        )
        hdrs = ['#', 'Hebrew Form', 'Stem', 'Conjugation', 'PGN', 'Root', 'Translation']
        cr   = [0.04, 0.16, 0.11, 0.18, 0.10, 0.09, 0.32]
        rows = [
            ['1',  'גָּלָה',    '', '', '',   'גלה', ''],
            ['2',  'גִּלָּה',   '', '', '',   'גלה', ''],
            ['3',  'גֻּלָּה',   '', '', '',   'גלה', ''],
            ['4',  'בָּרַךְ',   '', '', '',   'ברך', ''],
            ['5',  'בֵּרַךְ',   '', '', '',   'ברך', ''],
            ['6',  'בֹּרַךְ',   '', '', '',   'ברך', ''],
            ['7',  'כָּלָה',    '', '', '',   'כלה', ''],
            ['8',  'כִּלָּה',   '', '', '',   'כלה', ''],
            ['9',  'כֻּלָּה',   '', '', '',   'כלה', ''],
            ['10', 'יְגַלֶּה',  '', '', '',   'גלה', ''],
            ['11', 'יִגְלֶה',   '', '', '',   'גלה', ''],
            ['12', 'יְגֻלֶּה',  '', '', '',   'גלה', ''],
            ['13', 'יְבָרֵךְ',  '', '', '',   'ברך', ''],
            ['14', 'יְבֹרַךְ',  '', '', '',   'ברך', ''],
            ['15', 'יְכַלֶּה',  '', '', '',   'כלה', ''],
            ['16', 'וַיְגַל',   '', '', '',   'גלה', ''],
            ['17', 'וַיִּגֶּל', '', '', '',   'גלה', ''],
            ['18', 'וַיְצַו',   '', '', '',   'צוה', ''],
            ['19', 'גַּלֵּה',   '', '', '',   'גלה', ''],
            ['20', 'גְּלֵה',    '', '', '',   'גלה', ''],
            ['21', 'מְגַלֶּה',  '', '', '',   'גלה', ''],
            ['22', 'גֹּלֶה',    '', '', '',   'גלה', ''],
            ['23', 'מְגֻלֶּה',  '', '', '',   'גלה', ''],
            ['24', 'צֻוָּה',    '', '', '',   'צוה', ''],
        ]
        ans = [
            ['1',  'גָּלָה',    'Qal',  'Perfect',    '3ms', 'גלה', 'he went into exile / uncovered'],
            ['2',  'גִּלָּה',   'Piel', 'Perfect',    '3ms', 'גלה', 'he revealed / uncovered'],
            ['3',  'גֻּלָּה',   'Pual', 'Perfect',    '3ms', 'גלה', 'he was revealed / uncovered'],
            ['4',  'בָּרַךְ',   'Qal',  'Perfect',    '3ms', 'ברך', 'he knelt'],
            ['5',  'בֵּרַךְ',   'Piel', 'Perfect',    '3ms', 'ברך', 'he blessed'],
            ['6',  'בֹּרַךְ',   'Pual', 'Perfect',    '3ms', 'ברך', 'he was blessed'],
            ['7',  'כָּלָה',    'Qal',  'Perfect',    '3ms', 'כלה', 'he finished / ceased'],
            ['8',  'כִּלָּה',   'Piel', 'Perfect',    '3ms', 'כלה', 'he completed / finished off'],
            ['9',  'כֻּלָּה',   'Pual', 'Perfect',    '3ms', 'כלה', 'he was finished / consumed'],
            ['10', 'יְגַלֶּה',  'Piel', 'Imperfect',  '3ms', 'גלה', 'he will reveal'],
            ['11', 'יִגְלֶה',   'Qal',  'Imperfect',  '3ms', 'גלה', 'he will go into exile / uncover'],
            ['12', 'יְגֻלֶּה',  'Pual', 'Imperfect',  '3ms', 'גלה', 'it will be revealed'],
            ['13', 'יְבָרֵךְ',  'Piel', 'Imperfect',  '3ms', 'ברך', 'he will bless'],
            ['14', 'יְבֹרַךְ',  'Pual', 'Imperfect',  '3ms', 'ברך', 'he will be blessed'],
            ['15', 'יְכַלֶּה',  'Piel', 'Imperfect',  '3ms', 'כלה', 'he will complete / destroy'],
            ['16', 'וַיְגַל',   'Piel', 'Wayyiqtol',  '3ms', 'גלה', 'and he revealed'],
            ['17', 'וַיִּגֶּל', 'Qal',  'Wayyiqtol',  '3ms', 'גלה', 'and he went into exile'],
            ['18', 'וַיְצַו',   'Piel', 'Wayyiqtol',  '3ms', 'צוה', 'and he commanded'],
            ['19', 'גַּלֵּה',   'Piel', 'Imperative', '2ms', 'גלה', 'reveal!'],
            ['20', 'גְּלֵה',    'Qal',  'Imperative', '2ms', 'גלה', 'go into exile! / uncover!'],
            ['21', 'מְגַלֶּה',  'Piel', 'Participle', 'ms',  'גלה', 'revealing / one who reveals'],
            ['22', 'גֹּלֶה',    'Qal',  'Participle', 'ms',  'גלה', 'going into exile / one who uncovers'],
            ['23', 'מְגֻלֶּה',  'Pual', 'Participle', 'ms',  'גלה', 'being revealed / what is revealed'],
            ['24', 'צֻוָּה',    'Pual', 'Perfect',    '3ms', 'צוה', 'he was commanded'],
        ]
        self.add_drill_with_answer_key(
            hdrs, rows, ans,
            col_ratios=cr,
            heb_cols=[1, 5],
            answer_heb_cols=[1, 5],
            section_title='Qal / Piel / Pual — Weak Roots (24 forms)',
            answer_title='Answer Key',
        )


def build_ch33_stem_id_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch33StemIdDrill,
        'Chapter 33 — Qal / Piel / Pual Stem-ID Drill (Weak Roots)',
        'BBH Chapter 33 · Pual Weak Verbs',
        ['hebrew', 'bbh', 'ch33', 'exercises', 'ch33-stem-id-drill'],
        'ch33-stem-id-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch34 — Hithpael Paradigm Drill
# ---------------------------------------------------------------------------


class Ch34HithpaelParadigmDrill(ExercisePDF):
    _instructions = (
        'Write the complete Hithpael paradigm for the root קדשׁ. '
        'Key: הִתְ prefix in Perfect/Imperative/IC; יִתְ in Imperfect; מִתְ in Participle.'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'PGN', 'Hithpael form (קדשׁ)']
        cr   = [0.06, 0.18, 0.76]
        rows_pf = [['%d'%i,p,''] for i,p in enumerate(['3ms','3fs','2ms','2fs','1cs','3cp','2mp','2fp','1cp'],1)]
        ans_pf  = [
            ['1','3ms','הִתְקַדֵּשׁ'],['2','3fs','הִתְקַדְּשָׁה'],['3','2ms','הִתְקַדַּשְׁתָּ'],
            ['4','2fs','הִתְקַדַּשְׁתְּ'],['5','1cs','הִתְקַדַּשְׁתִּי'],['6','3cp','הִתְקַדְּשׁוּ'],
            ['7','2mp','הִתְקַדַּשְׁתֶּם'],['8','2fp','הִתְקַדַּשְׁתֶּן'],['9','1cp','הִתְקַדַּשְׁנוּ'],
        ]
        rows_imp = [['%d'%(i+9),p,''] for i,p in enumerate(['3ms','3fs','2ms','2fs','1cs','3mp','3fp','2mp','2fp','1cp'],1)]
        ans_imp  = [
            ['10','3ms','יִתְקַדֵּשׁ'],['11','3fs','תִּתְקַדֵּשׁ'],['12','2ms','תִּתְקַדֵּשׁ'],
            ['13','2fs','תִּתְקַדְּשִׁי'],['14','1cs','אֶתְקַדֵּשׁ'],['15','3mp','יִתְקַדְּשׁוּ'],
            ['16','3fp','תִּתְקַדֵּשְׁנָה'],['17','2mp','תִּתְקַדְּשׁוּ'],['18','2fp','תִּתְקַדֵּשְׁנָה'],
            ['19','1cp','נִתְקַדֵּשׁ'],
        ]
        rows_imper = [['%d'%(i+19),p,''] for i,p in enumerate(['2ms','2fs','2mp','2fp'],1)]
        ans_imper  = [
            ['20','2ms','הִתְקַדֵּשׁ'],['21','2fs','הִתְקַדְּשִׁי'],
            ['22','2mp','הִתְקַדְּשׁוּ'],['23','2fp','הִתְקַדֵּשְׁנָה'],
        ]
        hdrs_misc = ['#', 'Form', 'Hithpael (קדשׁ)']
        rows_misc = [
            ['24','Inf. Construct (bare)',''], ['25','Inf. Construct +לְ',''],
            ['26','Participle ms',''], ['27','Participle fs',''],
            ['28','Participle mp',''], ['29','Participle fp',''],
        ]
        ans_misc  = [
            ['24','Inf. Construct (bare)','הִתְקַדֵּשׁ'], ['25','Inf. Construct +לְ','לְהִתְקַדֵּשׁ'],
            ['26','Participle ms','מִתְקַדֵּשׁ'], ['27','Participle fs','מִתְקַדֶּשֶׁת'],
            ['28','Participle mp','מִתְקַדְּשִׁים'], ['29','Participle fp','מִתְקַדְּשׁוֹת'],
        ]
        for title_q, rows_q, ans_q in [
            ('Hithpael Perfect', rows_pf, ans_pf),
            ('Hithpael Imperfect', rows_imp, ans_imp),
            ('Hithpael Imperative', rows_imper, ans_imper),
        ]:
            self.add_drill_with_answer_key(hdrs, rows_q, ans_q, col_ratios=cr,
                                           answer_heb_cols=[2],
                                           section_title=title_q,
                                           answer_title=f'{title_q} — Answer Key')
        self.add_drill_with_answer_key(hdrs_misc, rows_misc, ans_misc, col_ratios=cr,
                                       answer_heb_cols=[2],
                                       section_title='Hithpael — Inf. Construct · Participle',
                                       answer_title='Inf./Participle — Answer Key')


def build_ch34_hithpael_paradigm_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch34HithpaelParadigmDrill,
        'Chapter 34 — Hithpael Paradigm Drill',
        'BBH Chapter 34 · Hithpael Strong',
        ['hebrew', 'bbh', 'ch34', 'exercises', 'ch34-hithpael-paradigm-drill'],
        'ch34-hithpael-paradigm-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch35 — Hithpael Weak Paradigm Drill (III-ה: גלה)
# ---------------------------------------------------------------------------


class Ch35HithpaelWeakParadigmDrill(ExercisePDF):
    _instructions = (
        'Write the Hithpael Weak forms. '
        'Part A uses גלה (III-ה). '
        'Part B shows metathesis: when R1 is a sibilant (ז, צ, שׁ, שׂ), '
        'the ת of הִתְ swaps with R1 (e.g., הִצְטַדֵּק from root צדק).'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'PGN / Form', 'Hithpael form']
        cr   = [0.06, 0.28, 0.66]

        rows_a = [
            ['1','Perfect 3ms (גלה)',''], ['2','Perfect 3fs (גלה)',''],
            ['3','Perfect 2ms (גלה)',''], ['4','Perfect 1cs (גלה)',''],
            ['5','Perfect 3cp (גלה)',''], ['6','Imperfect 3ms (גלה)',''],
            ['7','Imperfect 2ms (גלה)',''], ['8','Imperfect 3mp (גלה)',''],
            ['9','Imperfect 1cp (גלה)',''], ['10','Imperative 2ms (גלה)',''],
            ['11','Imperative 2fs (גלה)',''], ['12','Imperative 2mp (גלה)',''],
            ['13','Participle ms (גלה)',''], ['14','Participle mp (גלה)',''],
        ]
        ans_a = [
            ['1','Perfect 3ms (גלה)','הִתְגַּלָּה'], ['2','Perfect 3fs (גלה)','הִתְגַּלְּתָה'],
            ['3','Perfect 2ms (גלה)','הִתְגַּלִּיתָ'], ['4','Perfect 1cs (גלה)','הִתְגַּלִּיתִי'],
            ['5','Perfect 3cp (גלה)','הִתְגַּלּוּ'], ['6','Imperfect 3ms (גלה)','יִתְגַּלֶּה'],
            ['7','Imperfect 2ms (גלה)','תִּתְגַּלֶּה'], ['8','Imperfect 3mp (גלה)','יִתְגַּלּוּ'],
            ['9','Imperfect 1cp (גלה)','נִתְגַּלֶּה'], ['10','Imperative 2ms (גלה)','הִתְגַּלֵּה'],
            ['11','Imperative 2fs (גלה)','הִתְגַּלִּי'], ['12','Imperative 2mp (גלה)','הִתְגַּלּוּ'],
            ['13','Participle ms (גלה)','מִתְגַּלֶּה'], ['14','Participle mp (גלה)','מִתְגַּלִּים'],
        ]
        rows_b = [['15','Perfect 3ms (צדק — metathesis)',''], ['16','Imperfect 3ms (שמר — metathesis)',''],]
        ans_b  = [['15','Perfect 3ms (צדק — metathesis)','הִצְטַדֵּק'], ['16','Imperfect 3ms (שמר — metathesis)','יִשְׁתַּמֵּר'],]

        self.add_drill_with_answer_key(hdrs, rows_a, ans_a, col_ratios=cr,
                                       answer_heb_cols=[2],
                                       section_title='Part A — Hithpael Weak: גלה (III-ה)',
                                       answer_title='Part A — Answer Key')
        self.add_drill_with_answer_key(hdrs, rows_b, ans_b, col_ratios=cr,
                                       answer_heb_cols=[2],
                                       section_title='Part B — Hithpael Metathesis Examples',
                                       answer_title='Part B — Answer Key')


def build_ch35_hithpael_weak_paradigm_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch35HithpaelWeakParadigmDrill,
        'Chapter 35 — Hithpael Weak Paradigm Drill',
        'BBH Chapter 35 · Hithpael Weak',
        ['hebrew', 'bbh', 'ch35', 'exercises', 'ch35-hithpael-weak-paradigm-drill'],
        'ch35-hithpael-weak-paradigm-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch24 — Stem-ID Drill (Strong Roots)
# ---------------------------------------------------------------------------


class Ch24StemIdDrill(ExercisePDF):
    _instructions = (
        'For each Hebrew form, identify the stem (Qal or Niphal), '
        'conjugation, PGN, and root. '
        'Note: items 18 and 20 are הִשָּׁמֵר — Niphal Imperative 2ms and Niphal '
        'Infinitive Absolute are identical in strong roots; both parsings are accepted.'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'Hebrew Form', 'Stem', 'Conjugation', 'PGN', 'Root']
        cr   = [0.05, 0.18, 0.12, 0.22, 0.12, 0.31]
        rows = [
            ['1',  'קָטַל',       '', '', '',    ''],
            ['2',  'נִקְטַל',     '', '', '',    ''],
            ['3',  'שָׁמַר',      '', '', '',    ''],
            ['4',  'נִשְׁמַר',    '', '', '',    ''],
            ['5',  'מָכַר',       '', '', '',    ''],
            ['6',  'נִמְכַּר',    '', '', '',    ''],
            ['7',  'כָּרַת',      '', '', '',    ''],
            ['8',  'נִכְרַת',     '', '', '',    ''],
            ['9',  'יִשְׁמֹר',    '', '', '',    ''],
            ['10', 'יִשָּׁמֵר',   '', '', '',    ''],
            ['11', 'יִמָּכֵר',    '', '', '',    ''],
            ['12', 'יִמְכֹּר',    '', '', '',    ''],
            ['13', 'וַיִּשְׁמֹר', '', '', '',    ''],
            ['14', 'וַיִּשָּׁמֵר','', '', '',    ''],
            ['15', 'וַיִּמָּכֵר', '', '', '',    ''],
            ['16', 'וַיִּמְכֹּר', '', '', '',    ''],
            ['17', 'שְׁמֹר',      '', '', '',    ''],
            ['18', 'הִשָּׁמֵר',   '', '', '',    ''],
            ['19', 'שָׁמוֹר',     '', '', '',    ''],
            ['20', 'הִשָּׁמֵר',   '', '', '',    ''],
            ['21', 'הִנָּתֵן',    '', '', '',    ''],
            ['22', 'נָתוֹן',      '', '', '',    ''],
            ['23', 'שֹׁמֵר',      '', '', '',    ''],
            ['24', 'נִשְׁמָר',    '', '', '',    ''],
        ]
        ans = [
            ['1',  'קָטַל',       'Qal',    'Perfect',               '3ms', 'קטל'],
            ['2',  'נִקְטַל',     'Niphal', 'Perfect',               '3ms', 'קטל'],
            ['3',  'שָׁמַר',      'Qal',    'Perfect',               '3ms', 'שׁמר'],
            ['4',  'נִשְׁמַר',    'Niphal', 'Perfect',               '3ms', 'שׁמר'],
            ['5',  'מָכַר',       'Qal',    'Perfect',               '3ms', 'מכר'],
            ['6',  'נִמְכַּר',    'Niphal', 'Perfect',               '3ms', 'מכר'],
            ['7',  'כָּרַת',      'Qal',    'Perfect',               '3ms', 'כרת'],
            ['8',  'נִכְרַת',     'Niphal', 'Perfect',               '3ms', 'כרת'],
            ['9',  'יִשְׁמֹר',    'Qal',    'Imperfect',             '3ms', 'שׁמר'],
            ['10', 'יִשָּׁמֵר',   'Niphal', 'Imperfect',             '3ms', 'שׁמר'],
            ['11', 'יִמָּכֵר',    'Niphal', 'Imperfect',             '3ms', 'מכר'],
            ['12', 'יִמְכֹּר',    'Qal',    'Imperfect',             '3ms', 'מכר'],
            ['13', 'וַיִּשְׁמֹר', 'Qal',    'Wayyiqtol',             '3ms', 'שׁמר'],
            ['14', 'וַיִּשָּׁמֵר','Niphal', 'Wayyiqtol',             '3ms', 'שׁמר'],
            ['15', 'וַיִּמָּכֵר', 'Niphal', 'Wayyiqtol',             '3ms', 'מכר'],
            ['16', 'וַיִּמְכֹּר', 'Qal',    'Wayyiqtol',             '3ms', 'מכר'],
            ['17', 'שְׁמֹר',      'Qal',    'Imperative',            '2ms', 'שׁמר'],
            ['18', 'הִשָּׁמֵר',   'Niphal', 'Imperative / Inf. Abs.','2ms / —', 'שׁמר'],
            ['19', 'שָׁמוֹר',     'Qal',    'Inf. Absolute',         '—',   'שׁמר'],
            ['20', 'הִשָּׁמֵר',   'Niphal', 'Inf. Abs. / Imperative','— / 2ms', 'שׁמר'],
            ['21', 'הִנָּתֵן',    'Niphal', 'Inf. Absolute',         '—',   'נתן'],
            ['22', 'נָתוֹן',      'Qal',    'Inf. Absolute',         '—',   'נתן'],
            ['23', 'שֹׁמֵר',      'Qal',    'Participle',            'ms',  'שׁמר'],
            ['24', 'נִשְׁמָר',    'Niphal', 'Participle',            'ms',  'שׁמר'],
        ]
        self.add_drill_with_answer_key(
            hdrs, rows, ans,
            col_ratios=cr,
            heb_cols=[1],
            answer_heb_cols=[1, 5],
            section_title='Qal / Niphal — Strong Roots (24 forms)',
            answer_title='Answer Key',
        )


def build_ch24_stem_id_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch24StemIdDrill,
        'Chapter 24 — Qal / Niphal Stem-ID Drill (Strong Roots)',
        'BBH Chapter 24 · Niphal Strong Verbs',
        ['hebrew', 'bbh', 'ch24', 'exercises', 'ch24-stem-id-drill'],
        'ch24-stem-id-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch25 — Niphal Weak Paradigm Drill (III-ה: גלה; I-נ: נפל)
# ---------------------------------------------------------------------------


class Ch25NiphalWeakParadigmDrill(ExercisePDF):
    _instructions = (
        'Write the correct Niphal form for each entry. '
        'Section A uses גלה (III-ה); Section B uses נפל (I-נ). '
        'III-ה tip: watch for the ֶה endings in imperfect and participle. '
        'I-נ tip: nun assimilates into dagesh forte in the Niphal imperfect (יִפָּל).'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'PGN / Form', 'Niphal form']
        cr   = [0.06, 0.34, 0.60]

        rows_a = [
            ['1',  'Perfect 3ms (גלה)',    ''],
            ['2',  'Perfect 3fs (גלה)',    ''],
            ['3',  'Perfect 3cp (גלה)',    ''],
            ['4',  'Perfect 1cs (גלה)',    ''],
            ['5',  'Imperfect 3ms (גלה)',  ''],
            ['6',  'Imperfect 3fs (גלה)',  ''],
            ['7',  'Imperfect 3mp (גלה)',  ''],
            ['8',  'Imperfect 1cs (גלה)',  ''],
            ['9',  'Imperative 2ms (גלה)', ''],
            ['10', 'Inf. Construct (גלה)', ''],
            ['11', 'Inf. Absolute (גלה)',  ''],
            ['12', 'Participle ms (גלה)',  ''],
            ['13', 'Participle fs (גלה)',  ''],
        ]
        ans_a = [
            ['1',  'Perfect 3ms (גלה)',    'נִגְלָה'],
            ['2',  'Perfect 3fs (גלה)',    'נִגְלְתָה'],
            ['3',  'Perfect 3cp (גלה)',    'נִגְלוּ'],
            ['4',  'Perfect 1cs (גלה)',    'נִגְלֵיתִי'],
            ['5',  'Imperfect 3ms (גלה)',  'יִגָּלֶה'],
            ['6',  'Imperfect 3fs (גלה)',  'תִּגָּלֶה'],
            ['7',  'Imperfect 3mp (גלה)',  'יִגָּלוּ'],
            ['8',  'Imperfect 1cs (גלה)',  'אֶגָּלֶה'],
            ['9',  'Imperative 2ms (גלה)', 'הִגָּלֵה'],
            ['10', 'Inf. Construct (גלה)', 'הִגָּלוֹת'],
            ['11', 'Inf. Absolute (גלה)',  'הִגָּלֹה'],
            ['12', 'Participle ms (גלה)',  'נִגְלֶה'],
            ['13', 'Participle fs (גלה)',  'נִגְלֵית'],
        ]
        rows_b = [
            ['14', 'Perfect 3ms (נפל)',    ''],
            ['15', 'Perfect 3fs (נפל)',    ''],
            ['16', 'Perfect 3cp (נפל)',    ''],
            ['17', 'Imperfect 3ms (נפל)',  ''],
            ['18', 'Imperfect 3fs (נפל)',  ''],
            ['19', 'Imperfect 3mp (נפל)',  ''],
            ['20', 'Imperative 2ms (נפל)', ''],
            ['21', 'Participle ms (נפל)',  ''],
        ]
        ans_b = [
            ['14', 'Perfect 3ms (נפל)',    'נִפַּל'],
            ['15', 'Perfect 3fs (נפל)',    'נִפְּלָה'],
            ['16', 'Perfect 3cp (נפל)',    'נִפְּלוּ'],
            ['17', 'Imperfect 3ms (נפל)',  'יִפָּל'],
            ['18', 'Imperfect 3fs (נפל)',  'תִּפָּל'],
            ['19', 'Imperfect 3mp (נפל)',  'יִפְּלוּ'],
            ['20', 'Imperative 2ms (נפל)', 'הִפָּלֵל'],
            ['21', 'Participle ms (נפל)',  'נֹפֵל'],
        ]
        self.add_drill_with_answer_key(hdrs, rows_a, ans_a, col_ratios=cr,
                                       answer_heb_cols=[2],
                                       section_title='Section A — גלה (III-ה) Niphal',
                                       answer_title='Section A — Answer Key')
        self.add_drill_with_answer_key(hdrs, rows_b, ans_b, col_ratios=cr,
                                       answer_heb_cols=[2],
                                       section_title='Section B — נפל (I-נ) Niphal',
                                       answer_title='Section B — Answer Key')


def build_ch25_niphal_weak_paradigm_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch25NiphalWeakParadigmDrill,
        'Chapter 25 — Niphal Weak Paradigm Drill',
        'BBH Chapter 25 · Niphal Weak Verbs',
        ['hebrew', 'bbh', 'ch25', 'exercises', 'ch25-niphal-weak-paradigm-drill'],
        'ch25-niphal-weak-paradigm-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch25 — Qal–Niphal Contrast Drill (Weak Roots)
# ---------------------------------------------------------------------------


class Ch25QalNiphalContrastExercise(ExercisePDF):

    def _build(self) -> None:
        self.add_instructions(
            'Each item gives a weak root with its Qal meaning, a Niphal form, '
            'conjugation, and reference. '
            'For each: (1) translate the Niphal form; '
            '(2) name the semantic function: Passive / Reflexive / Simple Action / Stative. '
            '(3) explain in one sentence how the Niphal meaning follows from the Qal. '
            'Answer key at the bottom.'
        )

        hdr_a = ['#', 'Root', 'Qal Meaning', 'Niphal Form', 'Conj', 'Ref']
        cr_a  = [0.04, 0.08, 0.18, 0.14, 0.22, 0.34]
        rows_a = [
            ['1', 'נפל', 'to fall',           'יִפָּל',    'Imperfect 3ms', 'Gen 14:10'],
            ['2', 'נגש', 'to approach',        'נִגַּשׁ',  'Perfect 3ms',   '—'],
            ['3', 'נגד', 'to tell',            'הִגָּד',   'Inf. Absolute', '—'],
            ['4', 'נגע', 'to touch',           'נִגַּע',   'Perfect 3ms',   '—'],
            ['5', 'נכה', 'to strike',          'יִנָּכֶה', 'Imperfect 3ms', 'Exo 21:20'],
        ]
        rows_b = [
            ['6',  'גלה', 'to uncover, reveal', 'נִגְלָה', 'Perfect 3ms',   'Gen 35:7'],
            ['7',  'עלה', 'to go up, ascend',   'נַעֲלָה', 'Perfect 3ms',   '—'],
            ['8',  'ראה', 'to see',             'נִרְאָה', 'Perfect 3ms',   'Gen 12:7'],
            ['9',  'בנה', 'to build',           'יִבָּנֶה','Imperfect 3ms', '—'],
            ['10', 'עשׂה', 'to do, make',       'נַעֲשָׂה','Perfect 3ms',   'Gen 20:9'],
        ]
        rows_c = [
            ['11', 'קום', 'to rise, stand up',  'נָקוֹם',  'Perfect 3ms',   '—'],
            ['12', 'כון', 'to be firm',          'נָכוֹן',  'Perfect 3ms',   'Psa 103:19'],
            ['13', 'שׁים', 'to place, set',      'יִשָּׂם', 'Imperfect 3ms', '—'],
            ['14', 'בוא', 'to come, go in',     'נָבוֹא',  'Perfect 1cp',   'Num 32:9'],
            ['15', 'שׁוב', 'to return',          'נָשׁוּב', 'Perfect 3ms',   '—'],
        ]

        ans_a = [
            ['1', 'Root', 'Qal Meaning', 'Niphal Form', 'Conj', 'he fell — Simple Action | I-נ Niphal imperfect: root nun assimilates → dagesh in פּ'],
            ['2', '', '', '', '', 'he approached — Simple Action | Niphal of נגש carries the simple intransitive sense'],
            ['3', '', '', '', '', 'to be told — Passive | הִגָּד is Niphal inf. absolute of נגד; הִ + dagesh in גּ'],
            ['4', '', '', '', '', 'he was touched — Passive | subject receives the touch'],
            ['5', '', '', '', '', 'he shall be struck — Passive | Exo 21:20 legal context; dagesh in כּ (assimilated nun)'],
        ]
        ans_b = [
            ['6',  '', '', '', '', 'it was revealed — Passive or Reflexive | Gen 35:7: "God was revealed / revealed himself"'],
            ['7',  '', '', '', '', 'he went up — Simple Action | Niphal of עלה overlaps with Qal; note patach-furtive'],
            ['8',  '', '', '', '', 'he appeared — Passive/Reflexive | Gen 12:7: "the LORD appeared to Abram"'],
            ['9',  '', '', '', '', 'it will be built — Passive | dagesh forte in בּ + ֶה ending'],
            ['10', '', '', '', '', 'what has been done — Passive | Gen 20:9; patach-furtive before ה'],
        ]
        ans_c = [
            ['11', '', '', '', '', 'it was established — Passive | Niphal of קום; hollow root preserves ō vowel'],
            ['12', '', '', '', '', 'it is firm — Stative Niphal | Psa 103:19: "his throne is established"'],
            ['13', '', '', '', '', 'it will be placed — Passive | Niphal imperfect of שׁים; dagesh in שּׂ'],
            ['14', '', '', '', '', 'we went / came — Simple Action | Num 32:9; Niphal of בוא as simple intransitive'],
            ['15', '', '', '', '', 'it was brought back — Passive or SA | Niphal of שׁוב; context determines'],
        ]

        self.add_section_heading('Part A — I-נ Roots')
        self.add_generic_table(hdr_a, rows_a, cr_a, heb_cols=[3], show_answers=False)
        self.add_section_break()
        self.add_section_heading('Part B — III-ה Roots')
        self.add_generic_table(hdr_a, rows_b, cr_a, heb_cols=[3], show_answers=False)
        self.add_section_break()
        self.add_section_heading('Part C — Hollow Roots')
        self.add_generic_table(hdr_a, rows_c, cr_a, heb_cols=[3], show_answers=False)
        self.add_section_break()

        self.add_section_heading('Answer Key — Part A')
        self.add_generic_table(hdr_a, rows_a, cr_a, heb_cols=[3],
                               show_answers=True, answer_rows=ans_a)
        self.add_section_heading('Answer Key — Part B')
        self.add_generic_table(hdr_a, rows_b, cr_a, heb_cols=[3],
                               show_answers=True, answer_rows=ans_b)
        self.add_section_heading('Answer Key — Part C')
        self.add_generic_table(hdr_a, rows_c, cr_a, heb_cols=[3],
                               show_answers=True, answer_rows=ans_c)


def build_ch25_qal_niphal_contrast(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch25QalNiphalContrastExercise,
        'Chapter 25 — Qal–Niphal Contrast Drill (Weak Roots)',
        'BBH Chapter 25 · Niphal Weak Verbs',
        ['hebrew', 'bbh', 'ch25', 'exercises', 'ch25-qal-niphal-contrast'],
        'ch25-qal-niphal-contrast.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch25 — Function Sort (Weak Roots)
# ---------------------------------------------------------------------------


class Ch25FunctionSortExercise(ExercisePDF):

    def _build(self) -> None:
        self.add_instructions(
            'For each weak-root Niphal form, classify the semantic function: '
            'P = Passive, R = Reflexive/Reciprocal, SA = Simple Action. '
            'The gloss and reference provide context. Answer key at the bottom.'
        )
        hdrs = ['#', 'Hebrew', 'Conj', 'Ref', 'Gloss', 'Function (P/R/SA)']
        cr   = [0.04, 0.13, 0.18, 0.12, 0.35, 0.18]
        rows = [
            ['1',  'נִגְלָה',       'Perfect 3ms',    'Gen 35:7',   '"God was revealed to him"',                       ''],
            ['2',  'יִפָּל',        'Imperfect 3ms',  'Gen 14:10',  '"the kings fell into the tar pits"',              ''],
            ['3',  'נִרְאָה',       'Perfect 3ms',    'Gen 12:7',   '"the LORD appeared to Abram"',                    ''],
            ['4',  'יִבָּנֶה',      'Imperfect 3ms',  '—',          '"it will be built"',                              ''],
            ['5',  'וַיִּגָּלֶה',   'Wayyiqtol 3ms',  '1 Sam 3:21', '"the LORD revealed himself again at Shiloh"',    ''],
            ['6',  'נַעֲשָׂה',      'Perfect 3ms',    'Gen 20:9',   '"what has been done to me"',                      ''],
            ['7',  'נָכוֹן',        'Perfect 3ms',    'Psa 103:19', '"his throne is established"',                     ''],
            ['8',  'יִשָּׂם',       'Imperfect 3ms',  '—',          '"it will be placed"',                             ''],
            ['9',  'יִגָּלֶה',      'Imperfect 3ms',  '—',          '"it will be revealed"',                           ''],
            ['10', 'נִגַּשׁ',       'Perfect 3ms',    'Gen 44:18',  '"Judah drew near to him"',                        ''],
            ['11', 'נַעֲלָה',       'Perfect 3ms',    '—',          '"he went up / ascended"',                         ''],
            ['12', 'וַיִּנָּפֶל',   'Wayyiqtol 3ms',  '—',          '"he fell"',                                       ''],
            ['13', 'הִגָּלוֹת',     'Inf. Construct', '—',          '"to be revealed"',                                ''],
            ['14', 'נִגְלֵיתִי',    'Perfect 1cs',    '1 Sam 2:27', '"Did I not reveal myself?"',                      ''],
            ['15', 'יִנָּכֶה',      'Imperfect 3ms',  'Exo 21:20',  '"he shall be struck / beaten"',                  ''],
            ['16', 'נָשׁוּב',       'Perfect 3ms',    '—',          '"he/it returned / was brought back"',             ''],
            ['17', 'תִּגָּלֶה',     'Imperfect 3fs',  'Isa 40:5',   '"the glory of the LORD will be revealed"',       ''],
            ['18', 'נִגְלֶה',       'Participle ms',  '—',          '"being revealed / one who reveals himself"',     ''],
            ['19', 'הִנָּגֵשׁ',     'Inf. Absolute',  '—',          '"to approach"',                                   ''],
            ['20', 'נִרְאוּ',       'Perfect 3cp',    'Gen 1:9',    '"let the dry ground appear"',                     ''],
        ]
        ans = [
            ['1',  'נִגְלָה',       'Perfect 3ms',    'Gen 35:7',   '"God was revealed to him"',       'P (or R)'],
            ['2',  'יִפָּל',        'Imperfect 3ms',  'Gen 14:10',  '"the kings fell into the tar pits"', 'SA'],
            ['3',  'נִרְאָה',       'Perfect 3ms',    'Gen 12:7',   '"the LORD appeared to Abram"',    'R (or P)'],
            ['4',  'יִבָּנֶה',      'Imperfect 3ms',  '—',          '"it will be built"',              'P'],
            ['5',  'וַיִּגָּלֶה',   'Wayyiqtol 3ms',  '1 Sam 3:21', '"the LORD revealed himself again"', 'R'],
            ['6',  'נַעֲשָׂה',      'Perfect 3ms',    'Gen 20:9',   '"what has been done to me"',      'P'],
            ['7',  'נָכוֹן',        'Perfect 3ms',    'Psa 103:19', '"his throne is established"',     'SA'],
            ['8',  'יִשָּׂם',       'Imperfect 3ms',  '—',          '"it will be placed / set"',       'P'],
            ['9',  'יִגָּלֶה',      'Imperfect 3ms',  '—',          '"it will be revealed"',           'P'],
            ['10', 'נִגַּשׁ',       'Perfect 3ms',    'Gen 44:18',  '"Judah drew near to him"',        'SA'],
            ['11', 'נַעֲלָה',       'Perfect 3ms',    '—',          '"went up / ascended"',            'SA'],
            ['12', 'וַיִּנָּפֶל',   'Wayyiqtol 3ms',  '—',          '"he fell"',                       'SA'],
            ['13', 'הִגָּלוֹת',     'Inf. Construct', '—',          '"to be revealed"',                'P'],
            ['14', 'נִגְלֵיתִי',    'Perfect 1cs',    '1 Sam 2:27', '"Did I not reveal myself?"',      'R'],
            ['15', 'יִנָּכֶה',      'Imperfect 3ms',  'Exo 21:20',  '"he shall be struck"',            'P'],
            ['16', 'נָשׁוּב',       'Perfect 3ms',    '—',          '"he returned / was brought back"','SA or P'],
            ['17', 'תִּגָּלֶה',     'Imperfect 3fs',  'Isa 40:5',   '"will be revealed"',              'P'],
            ['18', 'נִגְלֶה',       'Participle ms',  '—',          '"being revealed / revealing himself"', 'R'],
            ['19', 'הִנָּגֵשׁ',     'Inf. Absolute',  '—',          '"to approach"',                   'SA'],
            ['20', 'נִרְאוּ',       'Perfect 3cp',    'Gen 1:9',    '"let the dry ground appear"',     'SA or R'],
        ]
        self.add_drill_with_answer_key(
            hdrs, rows, ans,
            col_ratios=cr,
            heb_cols=[1],
            answer_heb_cols=[1],
            section_title='Niphal Function Sort — 20 Weak-Root Forms',
            answer_title='Answer Key',
        )


def build_ch25_function_sort(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch25FunctionSortExercise,
        'Chapter 25 — Niphal Function Sort (Weak Roots)',
        'BBH Chapter 25 · Niphal Weak Verbs',
        ['hebrew', 'bbh', 'ch25', 'exercises', 'ch25-function-sort'],
        'ch25-function-sort.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch25 — Stem-ID Drill (Weak Roots)
# ---------------------------------------------------------------------------


class Ch25StemIdDrill(ExercisePDF):
    _instructions = (
        'For each Hebrew form, identify the stem (Qal or Niphal), '
        'conjugation, PGN, and root. '
        'Roots used: גלה (III-ה), נפל (I-נ), שׁוב (hollow), ראה (III-ה guttural).'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'Hebrew Form', 'Stem', 'Conjugation', 'PGN', 'Root']
        cr   = [0.05, 0.18, 0.12, 0.22, 0.12, 0.31]
        rows = [
            ['1',  'גָּלָה',      '', '', '', ''],
            ['2',  'נִגְלָה',     '', '', '', ''],
            ['3',  'נָפַל',       '', '', '', ''],
            ['4',  'נִפַּל',      '', '', '', ''],
            ['5',  'שָׁב',        '', '', '', ''],
            ['6',  'נָשׁוּב',     '', '', '', ''],
            ['7',  'רָאָה',       '', '', '', ''],
            ['8',  'נִרְאָה',     '', '', '', ''],
            ['9',  'יִגָּלֶה',    '', '', '', ''],
            ['10', 'יִגְלֶה',     '', '', '', ''],
            ['11', 'יִפֹּל',      '', '', '', ''],
            ['12', 'יִפָּל',      '', '', '', ''],
            ['13', 'יָשׁוּב',     '', '', '', ''],
            ['14', 'יִשָּׁב',     '', '', '', ''],
            ['15', 'וַיִּגֶּל',   '', '', '', ''],
            ['16', 'וַיִּגָּל',   '', '', '', ''],
            ['17', 'וַיִּפֹּל',   '', '', '', ''],
            ['18', 'וַיִּפָּל',   '', '', '', ''],
            ['19', 'גְּלֵה',      '', '', '', ''],
            ['20', 'הִגָּלֵה',    '', '', '', ''],
            ['21', 'גָּלֹה',      '', '', '', ''],
            ['22', 'הִגָּלֹה',    '', '', '', ''],
            ['23', 'גֹּלֶה',      '', '', '', ''],
            ['24', 'נִגְלֶה',     '', '', '', ''],
        ]
        ans = [
            ['1',  'גָּלָה',      'Qal',    'Perfect',     '3ms', 'גלה'],
            ['2',  'נִגְלָה',     'Niphal', 'Perfect',     '3ms', 'גלה'],
            ['3',  'נָפַל',       'Qal',    'Perfect',     '3ms', 'נפל'],
            ['4',  'נִפַּל',      'Niphal', 'Perfect',     '3ms', 'נפל'],
            ['5',  'שָׁב',        'Qal',    'Perfect',     '3ms', 'שׁוב'],
            ['6',  'נָשׁוּב',     'Niphal', 'Perfect',     '3ms', 'שׁוב'],
            ['7',  'רָאָה',       'Qal',    'Perfect',     '3ms', 'ראה'],
            ['8',  'נִרְאָה',     'Niphal', 'Perfect',     '3ms', 'ראה'],
            ['9',  'יִגָּלֶה',    'Niphal', 'Imperfect',   '3ms', 'גלה'],
            ['10', 'יִגְלֶה',     'Qal',    'Imperfect',   '3ms', 'גלה'],
            ['11', 'יִפֹּל',      'Qal',    'Imperfect',   '3ms', 'נפל'],
            ['12', 'יִפָּל',      'Niphal', 'Imperfect',   '3ms', 'נפל'],
            ['13', 'יָשׁוּב',     'Qal',    'Imperfect',   '3ms', 'שׁוב'],
            ['14', 'יִשָּׁב',     'Niphal', 'Imperfect',   '3ms', 'שׁוב'],
            ['15', 'וַיִּגֶּל',   'Qal',    'Wayyiqtol',   '3ms', 'גלה'],
            ['16', 'וַיִּגָּל',   'Niphal', 'Wayyiqtol',   '3ms', 'גלה'],
            ['17', 'וַיִּפֹּל',   'Qal',    'Wayyiqtol',   '3ms', 'נפל'],
            ['18', 'וַיִּפָּל',   'Niphal', 'Wayyiqtol',   '3ms', 'נפל'],
            ['19', 'גְּלֵה',      'Qal',    'Imperative',  '2ms', 'גלה'],
            ['20', 'הִגָּלֵה',    'Niphal', 'Imperative',  '2ms', 'גלה'],
            ['21', 'גָּלֹה',      'Qal',    'Inf. Absolute','—',  'גלה'],
            ['22', 'הִגָּלֹה',    'Niphal', 'Inf. Absolute','—',  'גלה'],
            ['23', 'גֹּלֶה',      'Qal',    'Participle',  'ms',  'גלה'],
            ['24', 'נִגְלֶה',     'Niphal', 'Participle',  'ms',  'גלה'],
        ]
        self.add_drill_with_answer_key(
            hdrs, rows, ans,
            col_ratios=cr,
            heb_cols=[1],
            answer_heb_cols=[1, 5],
            section_title='Qal / Niphal — Weak Roots (24 forms)',
            answer_title='Answer Key',
        )


def build_ch25_stem_id_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch25StemIdDrill,
        'Chapter 25 — Qal / Niphal Stem-ID Drill (Weak Roots)',
        'BBH Chapter 25 · Niphal Weak Verbs',
        ['hebrew', 'bbh', 'ch25', 'exercises', 'ch25-stem-id-drill'],
        'ch25-stem-id-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch28 — Stem-ID Drill (Strong Roots)
# ---------------------------------------------------------------------------


class Ch28StemIdDrill(ExercisePDF):
    _instructions = (
        'This drill mixes 24 forms of strong roots (Qal, Niphal, Hiphil, Hophal). '
        'For each item: (1) identify the stem, (2) parse conjugation and PGN, '
        '(3) translate the form. '
        'Roots used: קטל (paradigm), שׁמר (keep/guard), כבד (heavy/honored), שׁמד (destroy).'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        self.add_note(
            'Hophal Perfect: הָ prefix (qamets-hatuf = o-class).  '
            'Hophal Imperfect: יָ prefix.  '
            'Hophal Participle: הָ/הָשׁ prefix with qamets.  '
            'Hiphil: הִ prefix in Perfect; patach under prefix in Imperfect.'
        )
        hdrs = ['#', 'Hebrew Form', 'Stem', 'Conjugation', 'PGN', 'Root', 'Translation']
        cr   = [0.04, 0.16, 0.11, 0.18, 0.10, 0.09, 0.32]
        rows = [
            ['1',  'קָטַל',        '', '', '', 'קטל',  ''],
            ['2',  'הִקְטִיל',     '', '', '', 'קטל',  ''],
            ['3',  'נִקְטַל',      '', '', '', 'קטל',  ''],
            ['4',  'הָקְטַל',      '', '', '', 'קטל',  ''],
            ['5',  'שָׁמַר',       '', '', '', 'שׁמר', ''],
            ['6',  'נִשְׁמַר',     '', '', '', 'שׁמר', ''],
            ['7',  'יִשְׁמֹר',     '', '', '', 'שׁמר', ''],
            ['8',  'יַשְׁמִיר',    '', '', '', 'שׁמר', ''],
            ['9',  'יִשָּׁמֵר',    '', '', '', 'שׁמר', ''],
            ['10', 'יָשְׁמַר',     '', '', '', 'שׁמר', ''],
            ['11', 'וַיִּשְׁמֹר',  '', '', '', 'שׁמר', ''],
            ['12', 'וַיַּשְׁמֵר',  '', '', '', 'שׁמר', ''],
            ['13', 'וַיִּשָּׁמֵר', '', '', '', 'שׁמר', ''],
            ['14', 'וַיָּשְׁמַר',  '', '', '', 'שׁמר', ''],
            ['15', 'שְׁמֹר',       '', '', '', 'שׁמר', ''],
            ['16', 'הַשְׁמֵר',     '', '', '', 'שׁמר', ''],
            ['17', 'הִשָּׁמֵר',    '', '', '', 'שׁמר', ''],
            ['18', 'הָשְׁמֵר',     '', '', '', 'שׁמר', ''],
            ['19', 'שָׁמוֹר',      '', '', '', 'שׁמר', ''],
            ['20', 'הַשְׁמֵר',     '', '', '', 'שׁמר', ''],
            ['21', 'הִשָּׁמֵר',    '', '', '', 'שׁמר', ''],
            ['22', 'שֹׁמֵר',       '', '', '', 'שׁמר', ''],
            ['23', 'מַשְׁמִיר',    '', '', '', 'שׁמר', ''],
            ['24', 'הָשְׁמָר',     '', '', '', 'שׁמר', ''],
        ]
        ans = [
            ['1',  'קָטַל',        'Qal',    'Perfect',         '3ms', 'קטל',  'he killed'],
            ['2',  'הִקְטִיל',     'Hiphil', 'Perfect',         '3ms', 'קטל',  'he caused to kill'],
            ['3',  'נִקְטַל',      'Niphal', 'Perfect',         '3ms', 'קטל',  'he was killed'],
            ['4',  'הָקְטַל',      'Hophal', 'Perfect',         '3ms', 'קטל',  'he was caused to be killed'],
            ['5',  'שָׁמַר',       'Qal',    'Perfect',         '3ms', 'שׁמר', 'he kept / guarded'],
            ['6',  'נִשְׁמַר',     'Niphal', 'Perfect',         '3ms', 'שׁמר', 'he was kept / guarded'],
            ['7',  'יִשְׁמֹר',     'Qal',    'Imperfect',       '3ms', 'שׁמר', 'he will keep / guards'],
            ['8',  'יַשְׁמִיר',    'Hiphil', 'Imperfect',       '3ms', 'שׁמר', 'he will cause to keep'],
            ['9',  'יִשָּׁמֵר',    'Niphal', 'Imperfect',       '3ms', 'שׁמר', 'he will be kept / guards himself'],
            ['10', 'יָשְׁמַר',     'Hophal', 'Imperfect',       '3ms', 'שׁמר', 'he will be made to keep'],
            ['11', 'וַיִּשְׁמֹר',  'Qal',    'Wayyiqtol',       '3ms', 'שׁמר', 'and he kept / guarded'],
            ['12', 'וַיַּשְׁמֵר',  'Hiphil', 'Wayyiqtol',       '3ms', 'שׁמר', 'and he caused to keep'],
            ['13', 'וַיִּשָּׁמֵר', 'Niphal', 'Wayyiqtol',       '3ms', 'שׁמר', 'and he was kept / kept himself'],
            ['14', 'וַיָּשְׁמַר',  'Hophal', 'Wayyiqtol',       '3ms', 'שׁמר', 'and he was made to keep'],
            ['15', 'שְׁמֹר',       'Qal',    'Imperative',      '2ms', 'שׁמר', 'Keep! / Guard!'],
            ['16', 'הַשְׁמֵר',     'Hiphil', 'Imperative',      '2ms', 'שׁמר', 'Cause to keep! (same as #20)'],
            ['17', 'הִשָּׁמֵר',    'Niphal', 'Imperative',      '2ms', 'שׁמר', 'Guard yourself!'],
            ['18', 'הָשְׁמֵר',     'Hophal', 'Inf. Construct',  '—',   'שׁמר', 'to be made to keep / to be guarded'],
            ['19', 'שָׁמוֹר',      'Qal',    'Inf. Absolute',   '—',   'שׁמר', 'keeping / indeed keeping'],
            ['20', 'הַשְׁמֵר',     'Hiphil', 'Inf. Absolute',   '—',   'שׁמר', 'causing to keep (same as #16)'],
            ['21', 'הִשָּׁמֵר',    'Niphal', 'Inf. Absolute',   '—',   'שׁמר', 'being kept / indeed guarding oneself'],
            ['22', 'שֹׁמֵר',       'Qal',    'Participle',      'ms',  'שׁמר', 'one who keeps / guardian'],
            ['23', 'מַשְׁמִיר',    'Hiphil', 'Participle',      'ms',  'שׁמר', 'one who causes to keep'],
            ['24', 'הָשְׁמָר',     'Hophal', 'Participle',      'ms',  'שׁמר', 'one who is being kept / guarded'],
        ]
        self.add_drill_with_answer_key(
            hdrs, rows, ans,
            col_ratios=cr,
            heb_cols=[1, 5],
            answer_heb_cols=[1, 5],
            section_title='Qal / Niphal / Hiphil / Hophal — Strong Roots (24 forms)',
            answer_title='Answer Key',
        )


def build_ch28_stem_id_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch28StemIdDrill,
        'Chapter 28 — Four-Stem ID Drill (Strong Roots)',
        'BBH Chapter 28 · Hophal Strong Verbs',
        ['hebrew', 'bbh', 'ch28', 'exercises', 'ch28-stem-id-drill'],
        'ch28-stem-id-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch29 — Function Sort (Hophal Weak: Hiphil meaning + Hophal translation)
# ---------------------------------------------------------------------------


class Ch29FunctionSortExercise(ExercisePDF):

    def _build(self) -> None:
        self.add_instructions(
            'The Hophal is always the passive of the Hiphil. '
            'For each weak-root Hophal form: '
            '(1) identify the Hiphil active meaning (what the Hiphil of this root means); '
            '(2) translate the Hophal passive form in context. '
            'Answer key at the bottom.'
        )
        self.add_note(
            'I-י/Hollow Hophal: הוּ/יוּ prefix with shureq vowel (שׁוּרֶק) is the key marker.  '
            'I-י: Hiphil uses הוֹ– prefix; Hophal uses הוּ– prefix.  '
            'Hollow: Hiphil uses הֵ– + chiriq-yod; Hophal uses הוּ– + contracted stem.  '
            'III-ה Hophal: הוּ prefix + ָה ending in Perfect 3ms.'
        )
        hdr = ['#', 'Hophal Form', 'Root', 'Weak Class', 'Conjugation', 'Hiphil Active Meaning', 'Hophal Translation']
        cr  = [0.04, 0.12, 0.07, 0.10, 0.15, 0.26, 0.26]
        rows = [
            ['1',  'הוּבַל',    'יבל', 'I-י',    'Perfect 3ms',    '', ''],
            ['2',  'הוּבְאוּ',  'בוא', 'Hollow', 'Perfect 3cp',    '', ''],
            ['3',  'הוּרַד',    'ירד', 'I-י',    'Perfect 3ms',    '', ''],
            ['4',  'הוּקַם',    'קום', 'Hollow', 'Perfect 3ms',    '', ''],
            ['5',  'הוּשַׁב',   'שׁוב','Hollow', 'Perfect 3ms',    '', ''],
            ['6',  'יוּבַל',    'יבל', 'I-י',    'Imperfect 3ms',  '', ''],
            ['7',  'יוּבָא',    'בוא', 'Hollow', 'Imperfect 3ms',  '', ''],
            ['8',  'יוּרַד',    'ירד', 'I-י',    'Imperfect 3ms',  '', ''],
            ['9',  'יוּקַם',    'קום', 'Hollow', 'Imperfect 3ms',  '', ''],
            ['10', 'יוּשַׁב',   'שׁוב','Hollow', 'Imperfect 3ms',  '', ''],
            ['11', 'וַיּוּבַל', 'יבל', 'I-י',    'Wayyiqtol 3ms',  '', ''],
            ['12', 'וַיּוּבָא', 'בוא', 'Hollow', 'Wayyiqtol 3ms',  '', ''],
            ['13', 'וַיּוּרַד', 'ירד', 'I-י',    'Wayyiqtol 3ms',  '', ''],
            ['14', 'הוּלַד',    'ילד', 'I-י',    'Perfect 3ms',    '', ''],
            ['15', 'יוּלַד',    'ילד', 'I-י',    'Imperfect 3ms',  '', ''],
            ['16', 'מוּבָא',    'בוא', 'Hollow', 'Participle ms',  '', ''],
            ['17', 'מוּרָד',    'ירד', 'I-י',    'Participle ms',  '', ''],
            ['18', 'הוּגְלָה',  'גלה', 'III-ה',  'Perfect 3ms',    '', ''],
        ]
        ans = [
            ['1',  'הוּבַל',    'יבל', 'I-י',    'Perfect 3ms',    'Hiphil יָבַל: to lead/bring/carry',          'he was led / brought'],
            ['2',  'הוּבְאוּ',  'בוא', 'Hollow', 'Perfect 3cp',    'Hiphil הֵבִיא: to bring (cause to come)',     'they were brought'],
            ['3',  'הוּרַד',    'ירד', 'I-י',    'Perfect 3ms',    'Hiphil הוֹרִיד: to bring down (cause to descend)', 'he was brought down'],
            ['4',  'הוּקַם',    'קום', 'Hollow', 'Perfect 3ms',    'Hiphil הֵקִים: to raise up / establish',     'the tabernacle was erected'],
            ['5',  'הוּשַׁב',   'שׁוב','Hollow', 'Perfect 3ms',    'Hiphil הֵשִׁיב: to bring back / restore',    'the money was brought back'],
            ['6',  'יוּבַל',    'יבל', 'I-י',    'Imperfect 3ms',  'Hiphil יָבַל: to lead/bring/carry',          'he will be led / brought'],
            ['7',  'יוּבָא',    'בוא', 'Hollow', 'Imperfect 3ms',  'Hiphil הֵבִיא: to bring',                    'he will be brought'],
            ['8',  'יוּרַד',    'ירד', 'I-י',    'Imperfect 3ms',  'Hiphil הוֹרִיד: to bring down',              'he will be brought down'],
            ['9',  'יוּקַם',    'קום', 'Hollow', 'Imperfect 3ms',  'Hiphil הֵקִים: to raise up / establish',     'it will be raised up'],
            ['10', 'יוּשַׁב',   'שׁוב','Hollow', 'Imperfect 3ms',  'Hiphil הֵשִׁיב: to bring back / restore',    'he will be brought back'],
            ['11', 'וַיּוּבַל', 'יבל', 'I-י',    'Wayyiqtol 3ms',  'Hiphil יָבַל: to lead/bring',               'and he was led'],
            ['12', 'וַיּוּבָא', 'בוא', 'Hollow', 'Wayyiqtol 3ms',  'Hiphil הֵבִיא: to bring',                    'and he was brought (Gen 39:1)'],
            ['13', 'וַיּוּרַד', 'ירד', 'I-י',    'Wayyiqtol 3ms',  'Hiphil הוֹרִיד: to bring down',              'and he was brought down'],
            ['14', 'הוּלַד',    'ילד', 'I-י',    'Perfect 3ms',    'Hiphil הוֹלִיד: to beget / cause to be born', 'he was born'],
            ['15', 'יוּלַד',    'ילד', 'I-י',    'Imperfect 3ms',  'Hiphil הוֹלִיד: to beget / cause to be born', 'he will be born'],
            ['16', 'מוּבָא',    'בוא', 'Hollow', 'Participle ms',  'Hiphil הֵבִיא: to bring',                    '(one) being brought in'],
            ['17', 'מוּרָד',    'ירד', 'I-י',    'Participle ms',  'Hiphil הוֹרִיד: to bring down',              '(one) being brought down'],
            ['18', 'הוּגְלָה',  'גלה', 'III-ה',  'Perfect 3ms',    'Hiphil הִגְלָה: to exile (cause to go into exile)', 'he/Israel was carried into exile'],
        ]
        self.add_drill_with_answer_key(
            hdr, rows, ans,
            col_ratios=cr,
            heb_cols=[1, 2],
            answer_heb_cols=[1, 2],
            section_title='Hophal Weak-Root Function Sort (18 forms)',
            answer_title='Answer Key',
        )


def build_ch29_function_sort(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch29FunctionSortExercise,
        'Chapter 29 — Hophal Weak-Root Function Sort',
        'BBH Chapter 29 · Hophal Weak Verbs',
        ['hebrew', 'bbh', 'ch29', 'exercises', 'ch29-function-sort'],
        'ch29-function-sort.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch29 — Qal–Hiphil–Hophal Contrast Drill (Weak Roots)
# ---------------------------------------------------------------------------


class Ch29QalHiphilHophalContrastExercise(ExercisePDF):

    def _build(self) -> None:
        self.add_instructions(
            'Five root triplets — each root in Qal, Hiphil, and Hophal Perfect 3ms. '
            'For each form: (1) identify the stem, (2) parse conjugation and PGN, '
            '(3) translate, observing how the meaning shifts. '
            'Answer key at the bottom.'
        )

        hdr = ['#', 'Hebrew Form', 'Stem', 'Conjugation', 'PGN', 'Translation']
        cr  = [0.04, 0.16, 0.12, 0.20, 0.10, 0.38]

        triplets = [
            ('Part A — Root: בוא (Hollow: "to come / bring / be brought")', [
                ['1', 'בָּא',     '', 'Perfect', '3ms', ''],
                ['2', 'הֵבִיא',   '', 'Perfect', '3ms', ''],
                ['3', 'הוּבָא',   '', 'Perfect', '3ms', ''],
            ], [
                ['1', 'בָּא',     'Qal',    'Perfect', '3ms', 'he came'],
                ['2', 'הֵבִיא',   'Hiphil', 'Perfect', '3ms', 'he brought'],
                ['3', 'הוּבָא',   'Hophal', 'Perfect', '3ms', 'he was brought'],
            ]),
            ('Part B — Root: ירד (I-י: "to go down / bring down / be brought down")', [
                ['4', 'יָרַד',    '', 'Perfect', '3ms', ''],
                ['5', 'הוֹרִיד',  '', 'Perfect', '3ms', ''],
                ['6', 'הוּרַד',   '', 'Perfect', '3ms', ''],
            ], [
                ['4', 'יָרַד',    'Qal',    'Perfect', '3ms', 'he went down'],
                ['5', 'הוֹרִיד',  'Hiphil', 'Perfect', '3ms', 'he brought down'],
                ['6', 'הוּרַד',   'Hophal', 'Perfect', '3ms', 'he was brought down'],
            ]),
            ('Part C — Root: שׁוב (Hollow: "to return / bring back / be brought back")', [
                ['7', 'שָׁב',     '', 'Perfect', '3ms', ''],
                ['8', 'הֵשִׁיב',  '', 'Perfect', '3ms', ''],
                ['9', 'הוּשַׁב',  '', 'Perfect', '3ms', ''],
            ], [
                ['7', 'שָׁב',     'Qal',    'Perfect', '3ms', 'he returned'],
                ['8', 'הֵשִׁיב',  'Hiphil', 'Perfect', '3ms', 'he returned (it) / brought back'],
                ['9', 'הוּשַׁב',  'Hophal', 'Perfect', '3ms', 'he was brought back'],
            ]),
            ('Part D — Root: קום (Hollow: "to arise / raise up / be raised up")', [
                ['10', 'קָם',     '', 'Perfect', '3ms', ''],
                ['11', 'הֵקִים',  '', 'Perfect', '3ms', ''],
                ['12', 'הוּקַם',  '', 'Perfect', '3ms', ''],
            ], [
                ['10', 'קָם',     'Qal',    'Perfect', '3ms', 'he arose'],
                ['11', 'הֵקִים',  'Hiphil', 'Perfect', '3ms', 'he established / raised up'],
                ['12', 'הוּקַם',  'Hophal', 'Perfect', '3ms', 'he was raised up / established'],
            ]),
            ('Part E — Root: ילד (I-י: "to bear/father / beget / be born")', [
                ['13', 'יָלַד',   '', 'Perfect', '3ms', ''],
                ['14', 'הוֹלִיד', '', 'Perfect', '3ms', ''],
                ['15', 'הוּלַד',  '', 'Perfect', '3ms', ''],
            ], [
                ['13', 'יָלַד',   'Qal',    'Perfect', '3ms', 'he fathered / bore'],
                ['14', 'הוֹלִיד', 'Hiphil', 'Perfect', '3ms', 'he begat / caused to be born'],
                ['15', 'הוּלַד',  'Hophal', 'Perfect', '3ms', 'he was born'],
            ]),
        ]

        for title, rows, ans in triplets:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1], show_answers=False)
            self.add_section_break()

        self.add_section_heading('Answer Key')
        for title, rows, ans in triplets:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=True, answer_rows=ans)


def build_ch29_qal_hiphil_hophal_contrast(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch29QalHiphilHophalContrastExercise,
        'Chapter 29 — Qal–Hiphil–Hophal Contrast Drill (Weak Roots)',
        'BBH Chapter 29 · Hophal Weak Verbs',
        ['hebrew', 'bbh', 'ch29', 'exercises', 'ch29-qal-hiphil-hophal-contrast'],
        'ch29-qal-hiphil-hophal-contrast.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch29 — Stem-ID Drill (Weak Roots)
# ---------------------------------------------------------------------------


class Ch29StemIdDrill(ExercisePDF):
    _instructions = (
        'This drill mixes 24 forms of weak roots (hollow and I-י), '
        'from the four stems learned through Ch29: Qal, Niphal, Hiphil, Hophal. '
        'For each item: (1) identify the stem, (2) parse conjugation and PGN, '
        '(3) translate the form. '
        'Roots: בוא (hollow), שׁוב (hollow), קום (hollow), ירד (I-י), ילד (I-י).'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        self.add_note(
            'Key rule: In weak Hophal (hollow and I-י), '
            'the characteristic vowel is שׁוּרֶק (וּ) in the prefix slot — '
            'הוּ (Perfect/Inf.), יוּ (Imperfect), וַיּוּ (Wayyiqtol), מוּ (Participle). '
            'Note on item 11: Niphal Imperfect 3ms of בוא → יִוָּבֵא.'
        )
        hdrs = ['#', 'Hebrew Form', 'Stem', 'Conjugation', 'PGN', 'Root', 'Translation']
        cr   = [0.04, 0.16, 0.11, 0.18, 0.10, 0.09, 0.32]
        rows = [
            ['1',  'בָּא',       '', '', '', 'בוא', ''],
            ['2',  'הֵבִיא',     '', '', '', 'בוא', ''],
            ['3',  'נָבוֹא',     '', '', '', 'בוא', ''],
            ['4',  'הוּבָא',     '', '', '', 'בוא', ''],
            ['5',  'שָׁב',       '', '', '', 'שׁוב', ''],
            ['6',  'הֵשִׁיב',    '', '', '', 'שׁוב', ''],
            ['7',  'יָרַד',      '', '', '', 'ירד', ''],
            ['8',  'הוֹרִיד',    '', '', '', 'ירד', ''],
            ['9',  'יָבוֹא',     '', '', '', 'בוא', ''],
            ['10', 'יָבִיא',     '', '', '', 'בוא', ''],
            ['11', 'יִוָּבֵא',   '', '', '', 'בוא', ''],
            ['12', 'יוּבָא',     '', '', '', 'בוא', ''],
            ['13', 'יָשׁוּב',    '', '', '', 'שׁוב', ''],
            ['14', 'יָשִׁיב',    '', '', '', 'שׁוב', ''],
            ['15', 'יוּשַׁב',    '', '', '', 'שׁוב', ''],
            ['16', 'וַיָּבֹא',   '', '', '', 'בוא', ''],
            ['17', 'וַיָּבֵא',   '', '', '', 'בוא', ''],
            ['18', 'וַיּוּבָא',  '', '', '', 'בוא', ''],
            ['19', 'קָם',        '', '', '', 'קום', ''],
            ['20', 'הֵקִים',     '', '', '', 'קום', ''],
            ['21', 'הוּקַם',     '', '', '', 'קום', ''],
            ['22', 'יָלַד',      '', '', '', 'ילד', ''],
            ['23', 'הוֹלִיד',    '', '', '', 'ילד', ''],
            ['24', 'הוּלַד',     '', '', '', 'ילד', ''],
        ]
        ans = [
            ['1',  'בָּא',       'Qal',    'Perfect',   '3ms', 'בוא', 'he came'],
            ['2',  'הֵבִיא',     'Hiphil', 'Perfect',   '3ms', 'בוא', 'he brought'],
            ['3',  'נָבוֹא',     'Niphal', 'Perfect',   '3ms', 'בוא', 'he came in / entered'],
            ['4',  'הוּבָא',     'Hophal', 'Perfect',   '3ms', 'בוא', 'he was brought'],
            ['5',  'שָׁב',       'Qal',    'Perfect',   '3ms', 'שׁוב', 'he returned'],
            ['6',  'הֵשִׁיב',    'Hiphil', 'Perfect',   '3ms', 'שׁוב', 'he returned (it) / brought back'],
            ['7',  'יָרַד',      'Qal',    'Perfect',   '3ms', 'ירד', 'he went down'],
            ['8',  'הוֹרִיד',    'Hiphil', 'Perfect',   '3ms', 'ירד', 'he brought down'],
            ['9',  'יָבוֹא',     'Qal',    'Imperfect', '3ms', 'בוא', 'he will come'],
            ['10', 'יָבִיא',     'Hiphil', 'Imperfect', '3ms', 'בוא', 'he will bring'],
            ['11', 'יִוָּבֵא',   'Niphal', 'Imperfect', '3ms', 'בוא', 'he will come in / be brought in'],
            ['12', 'יוּבָא',     'Hophal', 'Imperfect', '3ms', 'בוא', 'he will be brought'],
            ['13', 'יָשׁוּב',    'Qal',    'Imperfect', '3ms', 'שׁוב', 'he will return'],
            ['14', 'יָשִׁיב',    'Hiphil', 'Imperfect', '3ms', 'שׁוב', 'he will bring back / restore'],
            ['15', 'יוּשַׁב',    'Hophal', 'Imperfect', '3ms', 'שׁוב', 'he will be brought back'],
            ['16', 'וַיָּבֹא',   'Qal',    'Wayyiqtol', '3ms', 'בוא', 'and he came'],
            ['17', 'וַיָּבֵא',   'Hiphil', 'Wayyiqtol', '3ms', 'בוא', 'and he brought'],
            ['18', 'וַיּוּבָא',  'Hophal', 'Wayyiqtol', '3ms', 'בוא', 'and he was brought'],
            ['19', 'קָם',        'Qal',    'Perfect',   '3ms', 'קום', 'he arose'],
            ['20', 'הֵקִים',     'Hiphil', 'Perfect',   '3ms', 'קום', 'he established / raised up'],
            ['21', 'הוּקַם',     'Hophal', 'Perfect',   '3ms', 'קום', 'he was raised up / established'],
            ['22', 'יָלַד',      'Qal',    'Perfect',   '3ms', 'ילד', 'he fathered / bore'],
            ['23', 'הוֹלִיד',    'Hiphil', 'Perfect',   '3ms', 'ילד', 'he begat / caused to be born'],
            ['24', 'הוּלַד',     'Hophal', 'Perfect',   '3ms', 'ילד', 'he was born'],
        ]
        self.add_drill_with_answer_key(
            hdrs, rows, ans,
            col_ratios=cr,
            heb_cols=[1, 5],
            answer_heb_cols=[1, 5],
            section_title='Qal / Niphal / Hiphil / Hophal — Weak Roots (24 forms)',
            answer_title='Answer Key',
        )


def build_ch29_stem_id_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch29StemIdDrill,
        'Chapter 29 — Four-Stem ID Drill (Weak Roots)',
        'BBH Chapter 29 · Hophal Weak Verbs',
        ['hebrew', 'bbh', 'ch29', 'exercises', 'ch29-stem-id-drill'],
        'ch29-stem-id-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch30 — Stem-ID Drill (Strong Roots)
# ---------------------------------------------------------------------------


class Ch30StemIdDrill(ExercisePDF):
    _instructions = (
        'Below are 24 Hebrew verb forms from strong roots (קטל, דבר, שׁמר, כבד). '
        'For each form, identify: (1) Stem (Qal / Niphal / Hiphil / Hophal / Piel), '
        '(2) Conjugation, (3) PGN, (4) Root. '
        'Answer key at the bottom.'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        self.add_note(
            'Piel: Dagesh forte in R2 + hiriq/tsere under prefix (shewa in imperfect).  '
            'Qal: no prefix, basic vowel pattern.  '
            'Niphal: נִ prefix in perfect; assimilated dagesh in imperfect.  '
            'Hiphil: הִ/הַ prefix.  Hophal: הָ/הֻ prefix (o/u class).'
        )
        hdrs = ['#', 'Hebrew Form', 'Stem', 'Conjugation', 'PGN', 'Root']
        cr   = [0.05, 0.18, 0.12, 0.22, 0.12, 0.31]
        rows = [
            ['1',  'קָטַל',        '', '', '', ''],
            ['2',  'קִטֵּל',       '', '', '', ''],
            ['3',  'הִקְטִיל',     '', '', '', ''],
            ['4',  'נִקְטַל',      '', '', '', ''],
            ['5',  'דִּבֶּר',      '', '', '', ''],
            ['6',  'דָּבַר',       '', '', '', ''],
            ['7',  'יְדַבֵּר',     '', '', '', ''],
            ['8',  'יִדְבַּר',     '', '', '', ''],
            ['9',  'יַדְבִּיר',    '', '', '', ''],
            ['10', 'יִדָּבֵר',     '', '', '', ''],
            ['11', 'וַיְדַבֵּר',   '', '', '', ''],
            ['12', 'וַיִּדְבַּר',  '', '', '', ''],
            ['13', 'וַיַּדְבֵּר',  '', '', '', ''],
            ['14', 'וַיִּדָּבֵר',  '', '', '', ''],
            ['15', 'דַּבֵּר',      '', '', '', ''],
            ['16', 'דְּבַר',       '', '', '', ''],
            ['17', 'הַדְבֵּר',     '', '', '', ''],
            ['18', 'הִדָּבֵר',     '', '', '', ''],
            ['19', 'דַּבֵּר',      '', '', '', ''],
            ['20', 'דָּבוֹר',      '', '', '', ''],
            ['21', 'מְדַבֵּר',     '', '', '', ''],
            ['22', 'דֹּבֵר',       '', '', '', ''],
            ['23', 'מַדְבִּיר',    '', '', '', ''],
            ['24', 'נִדְבָּר',     '', '', '', ''],
        ]
        ans = [
            ['1',  'קָטַל',        'Qal',    'Perfect',     '3ms', 'קטל'],
            ['2',  'קִטֵּל',       'Piel',   'Perfect',     '3ms', 'קטל'],
            ['3',  'הִקְטִיל',     'Hiphil', 'Perfect',     '3ms', 'קטל'],
            ['4',  'נִקְטַל',      'Niphal', 'Perfect',     '3ms', 'קטל'],
            ['5',  'דִּבֶּר',      'Piel',   'Perfect',     '3ms', 'דבר'],
            ['6',  'דָּבַר',       'Qal',    'Perfect',     '3ms', 'דבר'],
            ['7',  'יְדַבֵּר',     'Piel',   'Imperfect',   '3ms', 'דבר'],
            ['8',  'יִדְבַּר',     'Qal',    'Imperfect',   '3ms', 'דבר'],
            ['9',  'יַדְבִּיר',    'Hiphil', 'Imperfect',   '3ms', 'דבר'],
            ['10', 'יִדָּבֵר',     'Niphal', 'Imperfect',   '3ms', 'דבר'],
            ['11', 'וַיְדַבֵּר',   'Piel',   'Wayyiqtol',   '3ms', 'דבר'],
            ['12', 'וַיִּדְבַּר',  'Qal',    'Wayyiqtol',   '3ms', 'דבר'],
            ['13', 'וַיַּדְבֵּר',  'Hiphil', 'Wayyiqtol',   '3ms', 'דבר'],
            ['14', 'וַיִּדָּבֵר',  'Niphal', 'Wayyiqtol',   '3ms', 'דבר'],
            ['15', 'דַּבֵּר',      'Piel',   'Imperative',  '2ms', 'דבר'],
            ['16', 'דְּבַר',       'Qal',    'Imperative',  '2ms', 'דבר'],
            ['17', 'הַדְבֵּר',     'Hiphil', 'Imperative',  '2ms', 'דבר'],
            ['18', 'הִדָּבֵר',     'Niphal', 'Imperative',  '2ms', 'דבר'],
            ['19', 'דַּבֵּר',      'Piel',   'Inf. Absolute','—',  'דבר'],
            ['20', 'דָּבוֹר',      'Qal',    'Inf. Absolute','—',  'דבר'],
            ['21', 'מְדַבֵּר',     'Piel',   'Participle',  'ms',  'דבר'],
            ['22', 'דֹּבֵר',       'Qal',    'Participle',  'ms',  'דבר'],
            ['23', 'מַדְבִּיר',    'Hiphil', 'Participle',  'ms',  'דבר'],
            ['24', 'נִדְבָּר',     'Niphal', 'Participle',  'ms',  'דבר'],
        ]
        self.add_drill_with_answer_key(
            hdrs, rows, ans,
            col_ratios=cr,
            heb_cols=[1],
            answer_heb_cols=[1, 5],
            section_title='Qal / Niphal / Hiphil / Piel — Strong Roots (24 forms)',
            answer_title='Answer Key',
        )


def build_ch30_stem_id_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch30StemIdDrill,
        'Chapter 30 — Five-Stem ID Drill (Strong Roots)',
        'BBH Chapter 30 · Piel Strong Verbs',
        ['hebrew', 'bbh', 'ch30', 'exercises', 'ch30-stem-id-drill'],
        'ch30-stem-id-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch31 — Qal–Piel Contrast Drill (Weak Roots)
# ---------------------------------------------------------------------------


class Ch31QalPielContrastExercise(ExercisePDF):

    def _build(self) -> None:
        self.add_instructions(
            'Below are 15 weak-root Piel forms in three parts by weak class. '
            'For each: (1) translate the Piel form; '
            '(2) name the semantic function: I (Intensive), F (Factitive), '
            'D (Declarative), SA (Simple Action), or DN (Denominative); '
            '(3) compare with the Qal gloss to see what the Piel adds. '
            'Answer key at the bottom.'
        )
        self.add_note(
            'I-Guttural: gutturals reject dagesh; Piel shows compensatory lengthening.  '
            'III-ה: perfect 3ms ends in ָּה (qamets + dagesh-he) in Piel.  '
            'I-י / Hollow: the first root consonant may assimilate or contract.'
        )

        hdr = ['#', 'Hebrew', 'Root', 'Qal Gloss', 'Conjugation', 'Ref', 'Translation', 'Function']
        cr  = [0.04, 0.10, 0.08, 0.14, 0.14, 0.10, 0.22, 0.18]

        rows_a = [
            ['1',  'בֵּרַךְ', 'ברך', 'to kneel/bless',   'Perfect 3ms', 'Gen 1:28', '', ''],
            ['2',  'אֵהֵב',   'אהב', 'to love',           'Perfect 3ms', '—',        '', ''],
            ['3',  'חִזֵּק',  'חזק', 'to be strong',      'Perfect 3ms', 'Exo 4:21', '', ''],
            ['4',  'עִזֵּב',  'עזב', 'to forsake',        'Perfect 3ms', '—',        '', ''],
            ['5',  'עִנָּה',  'ענה', 'to answer/respond', 'Perfect 3ms', '—',        '', ''],
        ]
        rows_b = [
            ['6',  'גִּלָּה', 'גלה', 'to uncover/exile',  'Perfect 3ms', 'Gen 35:7', '', ''],
            ['7',  'בִּנָּה', 'בנה', 'to build',          'Perfect 3ms', '1 Kgs 6:2','', ''],
            ['8',  'צִוָּה', 'צוה', '(no common Qal)',    'Perfect 3ms', 'Gen 2:16', '', ''],
            ['9',  'קִנָּה', 'קנה', 'to acquire/buy',     'Perfect 3ms', '—',        '', ''],
            ['10', 'כִּלָּה', 'כלה', 'to be finished',    'Perfect 3ms', 'Gen 2:2',  '', ''],
        ]
        rows_c = [
            ['11', 'יִדֵּעַ', 'ידע', 'to know',           'Perfect 3ms', '—',        '', ''],
            ['12', 'חִיָּה',  'חיה', 'to live/be alive',  'Perfect 3ms', 'Gen 47:25','', ''],
            ['13', 'שִׁנָּה', 'שׁנה', 'to change/repeat', 'Perfect 3ms', '—',        '', ''],
            ['14', 'שִׁלֵּם', 'שׁלם', 'to be complete',   'Perfect 3ms', 'Exo 22:2', '', ''],
            ['15', 'כִּנָּה', 'כנה', '(noun: title)',      'Perfect 3ms', 'Isa 45:4', '', ''],
        ]

        ans_a = [
            ['1',  'בֵּרַךְ', 'ברך', 'to kneel/bless',   'Perfect 3ms', 'Gen 1:28', 'he blessed',                        'I'],
            ['2',  'אֵהֵב',   'אהב', 'to love',           'Perfect 3ms', '—',        'he loved intensively',              'I'],
            ['3',  'חִזֵּק',  'חזק', 'to be strong',      'Perfect 3ms', 'Exo 4:21', 'he hardened / made strong',         'F'],
            ['4',  'עִזֵּב',  'עזב', 'to forsake',        'Perfect 3ms', '—',        'he utterly forsook',                'I'],
            ['5',  'עִנָּה',  'ענה', 'to answer/respond', 'Perfect 3ms', '—',        'he afflicted / humbled',            'F'],
        ]
        ans_b = [
            ['6',  'גִּלָּה', 'גלה', 'to uncover/exile',  'Perfect 3ms', 'Gen 35:7', 'he revealed',                       'I'],
            ['7',  'בִּנָּה', 'בנה', 'to build',          'Perfect 3ms', '1 Kgs 6:2','he built thoroughly',               'I'],
            ['8',  'צִוָּה', 'צוה', '(no common Qal)',    'Perfect 3ms', 'Gen 2:16', 'he commanded',                      'SA'],
            ['9',  'קִנָּה', 'קנה', 'to acquire/buy',     'Perfect 3ms', '—',        'he acquired thoroughly',            'I'],
            ['10', 'כִּלָּה', 'כלה', 'to be finished',    'Perfect 3ms', 'Gen 2:2',  'he finished / completed',           'I or F'],
        ]
        ans_c = [
            ['11', 'יִדֵּעַ', 'ידע', 'to know',           'Perfect 3ms', '—',        'he made known / declared',          'D or I'],
            ['12', 'חִיָּה',  'חיה', 'to live/be alive',  'Perfect 3ms', 'Gen 47:25','he kept alive / preserved',         'F'],
            ['13', 'שִׁנָּה', 'שׁנה', 'to change/repeat', 'Perfect 3ms', '—',        'he changed / altered',              'I'],
            ['14', 'שִׁלֵּם', 'שׁלם', 'to be complete',   'Perfect 3ms', 'Exo 22:2', 'he made restitution / paid fully',  'I or F'],
            ['15', 'כִּנָּה', 'כנה', '(noun: title)',      'Perfect 3ms', 'Isa 45:4', 'he gave a title / assigned a name', 'DN'],
        ]

        self.add_section_heading('Part A — I-Guttural Roots')
        self.add_generic_table(hdr, rows_a, cr, heb_cols=[1, 2], show_answers=False)
        self.add_section_break()
        self.add_section_heading('Part B — III-ה Roots')
        self.add_generic_table(hdr, rows_b, cr, heb_cols=[1, 2], show_answers=False)
        self.add_section_break()
        self.add_section_heading('Part C — I-י / Hollow Roots')
        self.add_generic_table(hdr, rows_c, cr, heb_cols=[1, 2], show_answers=False)
        self.add_section_break()

        self.add_section_heading('Answer Key — Part A')
        self.add_generic_table(hdr, rows_a, cr, heb_cols=[1, 2],
                               show_answers=True, answer_rows=ans_a)
        self.add_section_heading('Answer Key — Part B')
        self.add_generic_table(hdr, rows_b, cr, heb_cols=[1, 2],
                               show_answers=True, answer_rows=ans_b)
        self.add_section_heading('Answer Key — Part C')
        self.add_generic_table(hdr, rows_c, cr, heb_cols=[1, 2],
                               show_answers=True, answer_rows=ans_c)


def build_ch31_qal_piel_contrast(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch31QalPielContrastExercise,
        'Chapter 31 — Qal–Piel Contrast Drill (Weak Roots)',
        'BBH Chapter 31 · Piel Weak Verbs',
        ['hebrew', 'bbh', 'ch31', 'exercises', 'ch31-qal-piel-contrast'],
        'ch31-qal-piel-contrast.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch31 — Piel Function Sort (Weak Roots)
# ---------------------------------------------------------------------------


class Ch31FunctionSortExercise(ExercisePDF):

    def _build(self) -> None:
        self.add_instructions(
            'For each Piel form below, classify the semantic function: '
            'I (Intensive), F (Factitive), D (Declarative), DN (Denominative), SA (Simple Action). '
            'Each item gives the Hebrew form, conjugation, root, reference, and contextual gloss. '
            'Answer key at the bottom.'
        )
        hdrs = ['#', 'Hebrew Form', 'Conjugation', 'Root', 'Ref', 'Gloss', 'Function']
        cr   = [0.04, 0.12, 0.16, 0.08, 0.10, 0.36, 0.14]
        rows = [
            ['1',  'בֵּרַךְ',    'Perfect 3ms',   'ברך',  'Gen 1:28',  '"God blessed them"',                      ''],
            ['2',  'גִּלָּה',    'Perfect 3ms',   'גלה',  'Gen 35:7',  '"God revealed himself to him"',           ''],
            ['3',  'חִזֵּק',     'Perfect 3ms',   'חזק',  'Exo 4:21',  '"I will harden his heart"',               ''],
            ['4',  'כִּלָּה',    'Perfect 3ms',   'כלה',  'Gen 2:2',   '"God finished his work"',                 ''],
            ['5',  'צִוָּה',     'Perfect 3ms',   'צוה',  'Gen 2:16',  '"the LORD commanded the man"',            ''],
            ['6',  'בֵּרֲכוּ',   'Perfect 3cp',   'ברך',  '—',         '"they blessed"',                          ''],
            ['7',  'יְבָרֵךְ',   'Imperfect 3ms', 'ברך',  'Psa 115:12','"the LORD will bless"',                   ''],
            ['8',  'יְצַוֶּה',   'Imperfect 3ms', 'צוה',  '—',         '"he will command"',                       ''],
            ['9',  'וַיְבָרֶךְ', 'Wayyiqtol 3ms', 'ברך',  'Gen 1:22',  '"God blessed them"',                      ''],
            ['10', 'וַיְצַו',    'Wayyiqtol 3ms', 'צוה',  'Gen 3:11',  '"which I commanded you"',                 ''],
            ['11', 'חִיָּה',     'Perfect 3ms',   'חיה',  'Gen 47:25', '"you have kept us alive"',                ''],
            ['12', 'שִׁלֵּם',    'Perfect 3ms',   'שׁלם', 'Exo 22:2',  '"he shall make full restitution"',        ''],
            ['13', 'עִנָּה',     'Perfect 3ms',   'ענה',  'Gen 15:13', '"they will afflict them"',                ''],
            ['14', 'כִּנָּה',    'Perfect 3ms',   'כנה',  'Isa 45:4',  '"I gave you a title"',                    ''],
            ['15', 'בִּקֵּשׁ',   'Perfect 3ms',   'בקש',  'Gen 37:15', '"what are you seeking?"',                 ''],
            ['16', 'יְבַקֵּשׁ',  'Imperfect 3ms', 'בקש',  '—',         '"he will seek"',                          ''],
            ['17', 'גִּלָּה',    'Perfect 3ms',   'גלה',  'Amo 3:7',   '"he reveals his secret to his servants"', ''],
            ['18', 'שִׁנָּה',    'Perfect 3ms',   'שׁנה', '—',          '"he changed / altered"',                  ''],
            ['19', 'חִזְּקוּ',   'Perfect 3cp',   'חזק',  '—',         '"they strengthened / encouraged"',        ''],
            ['20', 'בִּנָּה',    'Perfect 3ms',   'בנה',  '1 Kgs 6:2', '"Solomon built the house"',               ''],
        ]
        ans = [
            ['1',  'בֵּרַךְ',    'Perfect 3ms',   'ברך',  'Gen 1:28',   '"God blessed them"',                      'I'],
            ['2',  'גִּלָּה',    'Perfect 3ms',   'גלה',  'Gen 35:7',   '"God revealed himself to him"',           'I'],
            ['3',  'חִזֵּק',     'Perfect 3ms',   'חזק',  'Exo 4:21',   '"I will harden his heart"',               'F'],
            ['4',  'כִּלָּה',    'Perfect 3ms',   'כלה',  'Gen 2:2',    '"God finished his work"',                 'I or F'],
            ['5',  'צִוָּה',     'Perfect 3ms',   'צוה',  'Gen 2:16',   '"the LORD commanded the man"',            'SA'],
            ['6',  'בֵּרֲכוּ',   'Perfect 3cp',   'ברך',  '—',          '"they blessed"',                          'I'],
            ['7',  'יְבָרֵךְ',   'Imperfect 3ms', 'ברך',  'Psa 115:12', '"the LORD will bless"',                   'I'],
            ['8',  'יְצַוֶּה',   'Imperfect 3ms', 'צוה',  '—',          '"he will command"',                       'SA'],
            ['9',  'וַיְבָרֶךְ', 'Wayyiqtol 3ms', 'ברך',  'Gen 1:22',   '"God blessed them"',                      'I'],
            ['10', 'וַיְצַו',    'Wayyiqtol 3ms', 'צוה',  'Gen 3:11',   '"which I commanded you"',                 'SA'],
            ['11', 'חִיָּה',     'Perfect 3ms',   'חיה',  'Gen 47:25',  '"you have kept us alive"',                'F'],
            ['12', 'שִׁלֵּם',    'Perfect 3ms',   'שׁלם', 'Exo 22:2',   '"he shall make full restitution"',        'I or F'],
            ['13', 'עִנָּה',     'Perfect 3ms',   'ענה',  'Gen 15:13',  '"they will afflict them"',                'F'],
            ['14', 'כִּנָּה',    'Perfect 3ms',   'כנה',  'Isa 45:4',   '"I gave you a title"',                    'DN'],
            ['15', 'בִּקֵּשׁ',   'Perfect 3ms',   'בקש',  'Gen 37:15',  '"what are you seeking?"',                 'SA'],
            ['16', 'יְבַקֵּשׁ',  'Imperfect 3ms', 'בקש',  '—',          '"he will seek"',                          'SA'],
            ['17', 'גִּלָּה',    'Perfect 3ms',   'גלה',  'Amo 3:7',    '"he reveals his secret to his servants"', 'I'],
            ['18', 'שִׁנָּה',    'Perfect 3ms',   'שׁנה', '—',           '"he changed / altered"',                  'I'],
            ['19', 'חִזְּקוּ',   'Perfect 3cp',   'חזק',  '—',          '"they strengthened / encouraged"',        'F'],
            ['20', 'בִּנָּה',    'Perfect 3ms',   'בנה',  '1 Kgs 6:2',  '"Solomon built the house"',               'I'],
        ]
        self.add_drill_with_answer_key(
            hdrs, rows, ans,
            col_ratios=cr,
            heb_cols=[1, 3],
            answer_heb_cols=[1, 3],
            section_title='Piel Semantic Function Sort — 20 Weak-Root Forms',
            answer_title='Answer Key',
        )


def build_ch31_function_sort(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch31FunctionSortExercise,
        'Chapter 31 — Piel Function Sort (Weak Roots)',
        'BBH Chapter 31 · Piel Weak Verbs',
        ['hebrew', 'bbh', 'ch31', 'exercises', 'ch31-function-sort'],
        'ch31-function-sort.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch31 — Stem-ID Drill (Weak Roots)
# ---------------------------------------------------------------------------


class Ch31StemIdDrill(ExercisePDF):
    _instructions = (
        'Below are 24 Hebrew verb forms from weak roots (ברך, גלה, צוה, חזק). '
        'For each form, identify: (1) Stem (Qal / Niphal / Hiphil / Piel), '
        '(2) Conjugation, (3) PGN, (4) Root. '
        'Answer key at the bottom.'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        self.add_note(
            'I-Guttural Piel (ברך, חזק): guttural R1 cannot take dagesh; '
            'watch for virtual doubling (longer vowel before R2).  '
            'III-ה Piel (גלה, צוה): perfect 3ms ends in ָּה (qamets + dagesh-he).  '
            'Qal III-ה perfect 3ms ends in ָה (no dagesh in ה).'
        )
        hdrs = ['#', 'Hebrew Form', 'Stem', 'Conjugation', 'PGN', 'Root']
        cr   = [0.05, 0.18, 0.12, 0.22, 0.12, 0.31]
        rows = [
            ['1',  'בֵּרַךְ',    '', '', '', ''],
            ['2',  'בָּרַךְ',    '', '', '', ''],
            ['3',  'גִּלָּה',    '', '', '', ''],
            ['4',  'גָּלָה',     '', '', '', ''],
            ['5',  'נִגְלָה',    '', '', '', ''],
            ['6',  'הִגְלָה',    '', '', '', ''],
            ['7',  'צִוָּה',     '', '', '', ''],
            ['8',  'חִזֵּק',     '', '', '', ''],
            ['9',  'חָזַק',      '', '', '', ''],
            ['10', 'יְבָרֵךְ',   '', '', '', ''],
            ['11', 'יְצַוֶּה',   '', '', '', ''],
            ['12', 'יִגְלֶה',    '', '', '', ''],
            ['13', 'יִגָּלֶה',   '', '', '', ''],
            ['14', 'יְגַלֶּה',   '', '', '', ''],
            ['15', 'יַגְלֶה',    '', '', '', ''],
            ['16', 'וַיְבָרֶךְ', '', '', '', ''],
            ['17', 'וַיְצַו',    '', '', '', ''],
            ['18', 'וַיִּגֶּל',  '', '', '', ''],
            ['19', 'בָּרֵךְ',    '', '', '', ''],
            ['20', 'גַּל',       '', '', '', ''],
            ['21', 'גַּלֵּה',    '', '', '', ''],
            ['22', 'מְבָרֵךְ',   '', '', '', ''],
            ['23', 'מְגַלֶּה',   '', '', '', ''],
            ['24', 'גֹּלֶה',     '', '', '', ''],
        ]
        ans = [
            ['1',  'בֵּרַךְ',    'Piel',   'Perfect',     '3ms', 'ברך'],
            ['2',  'בָּרַךְ',    'Qal',    'Perfect',     '3ms', 'ברך'],
            ['3',  'גִּלָּה',    'Piel',   'Perfect',     '3ms', 'גלה'],
            ['4',  'גָּלָה',     'Qal',    'Perfect',     '3ms', 'גלה'],
            ['5',  'נִגְלָה',    'Niphal', 'Perfect',     '3ms', 'גלה'],
            ['6',  'הִגְלָה',    'Hiphil', 'Perfect',     '3ms', 'גלה'],
            ['7',  'צִוָּה',     'Piel',   'Perfect',     '3ms', 'צוה'],
            ['8',  'חִזֵּק',     'Piel',   'Perfect',     '3ms', 'חזק'],
            ['9',  'חָזַק',      'Qal',    'Perfect',     '3ms', 'חזק'],
            ['10', 'יְבָרֵךְ',   'Piel',   'Imperfect',   '3ms', 'ברך'],
            ['11', 'יְצַוֶּה',   'Piel',   'Imperfect',   '3ms', 'צוה'],
            ['12', 'יִגְלֶה',    'Qal',    'Imperfect',   '3ms', 'גלה'],
            ['13', 'יִגָּלֶה',   'Niphal', 'Imperfect',   '3ms', 'גלה'],
            ['14', 'יְגַלֶּה',   'Piel',   'Imperfect',   '3ms', 'גלה'],
            ['15', 'יַגְלֶה',    'Hiphil', 'Imperfect',   '3ms', 'גלה'],
            ['16', 'וַיְבָרֶךְ', 'Piel',   'Wayyiqtol',   '3ms', 'ברך'],
            ['17', 'וַיְצַו',    'Piel',   'Wayyiqtol',   '3ms', 'צוה'],
            ['18', 'וַיִּגֶּל',  'Qal',    'Wayyiqtol',   '3ms', 'גלה'],
            ['19', 'בָּרֵךְ',    'Piel',   'Imperative',  '2ms', 'ברך'],
            ['20', 'גַּל',       'Qal',    'Imperative',  '2ms', 'גלה'],
            ['21', 'גַּלֵּה',    'Piel',   'Imperative',  '2ms', 'גלה'],
            ['22', 'מְבָרֵךְ',   'Piel',   'Participle',  'ms',  'ברך'],
            ['23', 'מְגַלֶּה',   'Piel',   'Participle',  'ms',  'גלה'],
            ['24', 'גֹּלֶה',     'Qal',    'Participle',  'ms',  'גלה'],
        ]
        self.add_drill_with_answer_key(
            hdrs, rows, ans,
            col_ratios=cr,
            heb_cols=[1],
            answer_heb_cols=[1, 5],
            section_title='Qal / Niphal / Hiphil / Piel — Weak Roots (24 forms)',
            answer_title='Answer Key',
        )


def build_ch31_stem_id_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch31StemIdDrill,
        'Chapter 31 — Stem-ID Drill (Weak Roots)',
        'BBH Chapter 31 · Piel Weak Verbs',
        ['hebrew', 'bbh', 'ch31', 'exercises', 'ch31-stem-id-drill'],
        'ch31-stem-id-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch34 — Qal–Piel–Hithpael Contrast Drill (Strong Roots)
# ---------------------------------------------------------------------------


class Ch34QalPielHithpaelContrastExercise(ExercisePDF):

    def _build(self) -> None:
        self.add_instructions(
            'Five groups of three forms — each group shares a root in Qal, Piel, '
            'and Hithpael Perfect 3ms. '
            'For each: (1) identify the stem, (2) state the semantic function added, '
            '(3) translate. '
            'Note Group 3: root שׁמר has sibilant metathesis in the Hithpael '
            '(הִתְ + שׁ → הִשְׁתְּ). '
            'Answer key at the bottom.'
        )
        self.add_note(
            'Hithpael: הִתְ prefix + Dagesh Forte in R2. '
            'Piel: Dagesh Forte in R2, no prefix. '
            'Qal: neither prefix nor dagesh in R2. '
            'Sibilant metathesis: when R1 = שׁ/שׂ/ס/צ/ז, the ת of הִתְ swaps with R1.'
        )

        hdr = ['#', 'Hebrew', 'Stem', 'Function', 'Translation']
        cr  = [0.05, 0.18, 0.14, 0.22, 0.41]

        triplets = [
            ('Group 1 — Root: קדשׁ (to be holy)', [
                ['1', 'קָדַשׁ',      '', '', ''],
                ['2', 'קִדֵּשׁ',     '', '', ''],
                ['3', 'הִתְקַדֵּשׁ', '', '', ''],
            ], [
                ['1', 'קָדַשׁ',      'Qal',      'Basic / stative',   'he was holy / became holy'],
                ['2', 'קִדֵּשׁ',     'Piel',     'Factitive',          'he consecrated / made holy'],
                ['3', 'הִתְקַדֵּשׁ', 'Hithpael', 'Reflexive',          'he consecrated himself / made himself holy'],
            ]),
            ('Group 2 — Root: כבד (to be heavy/honored)', [
                ['4', 'כָּבֵד',      '', '', ''],
                ['5', 'כִּבֵּד',     '', '', ''],
                ['6', 'הִתְכַּבֵּד', '', '', ''],
            ], [
                ['4', 'כָּבֵד',      'Qal',      'Basic / stative',   'he was heavy / honored'],
                ['5', 'כִּבֵּד',     'Piel',     'Factitive',          'he honored'],
                ['6', 'הִתְכַּבֵּד', 'Hithpael', 'Reflexive',          'he honored himself / gloried'],
            ]),
            ('Group 3 — Root: שׁמר (sibilant metathesis)', [
                ['7', 'שָׁמַר',      '', '', ''],
                ['8', 'שִׁמֵּר',     '', '', ''],
                ['9', 'הִשְׁתַּמֵּר','', '', ''],
            ], [
                ['7', 'שָׁמַר',      'Qal',      'Basic',              'he kept / guarded'],
                ['8', 'שִׁמֵּר',     'Piel',     'Intensive',          'he kept carefully / watched over'],
                ['9', 'הִשְׁתַּמֵּר','Hithpael', 'Reflexive',          'he kept himself / was on guard (הִתְ + שׁ → הִשְׁתְּ)'],
            ]),
            ('Group 4 — Root: פלל (to judge/intervene)', [
                ['10', 'פָּלַל',      '', '', ''],
                ['11', 'פִּלֵּל',     '', '', ''],
                ['12', 'הִתְפַּלֵּל', '', '', ''],
            ], [
                ['10', 'פָּלַל',      'Qal',      'Basic',              'he judged / intervened'],
                ['11', 'פִּלֵּל',     'Piel',     'Intensive',          'he actively interceded'],
                ['12', 'הִתְפַּלֵּל', 'Hithpael', 'Reflexive/Denom.',   'he prayed (pleaded his own case before God)'],
            ]),
            ('Group 5 — Root: ברך (to kneel/bless)', [
                ['13', 'בָּרַךְ',     '', '', ''],
                ['14', 'בֵּרַךְ',     '', '', ''],
                ['15', 'הִתְבָּרֵךְ', '', '', ''],
            ], [
                ['13', 'בָּרַךְ',     'Qal',      'Basic',              'he knelt'],
                ['14', 'בֵּרַךְ',     'Piel',     'Factitive',          'he blessed'],
                ['15', 'הִתְבָּרֵךְ', 'Hithpael', 'Reflexive',          'he blessed himself / was blessed'],
            ]),
        ]

        for title, rows, ans in triplets:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1], show_answers=False)
            self.add_section_break()

        self.add_section_heading('Answer Key')
        for title, rows, ans in triplets:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=True, answer_rows=ans)


def build_ch34_qal_piel_hithpael_contrast(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch34QalPielHithpaelContrastExercise,
        'Chapter 34 — Qal / Piel / Hithpael Contrast Drill (Strong Roots)',
        'BBH Chapter 34 · Hithpael Strong Verbs',
        ['hebrew', 'bbh', 'ch34', 'exercises', 'ch34-qal-piel-hithpael-contrast'],
        'ch34-qal-piel-hithpael-contrast.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch34 — Stem-ID Drill (Strong Roots)
# ---------------------------------------------------------------------------


class Ch34StemIdDrill(ExercisePDF):
    _instructions = (
        'Identify the stem, conjugation, PGN, and root of each form below. '
        'Roots used: קדשׁ and דבר. '
        'Stems covered: Qal, Niphal, Piel, Pual, Hiphil, Hithpael. '
        'Note: items 3 and 20 share the same written form הִתְקַדֵּשׁ — '
        'context determines whether it is Hithpael Perfect 3ms or Imperative 2ms.'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'Hebrew Form', 'Stem', 'Conjugation', 'PGN', 'Root']
        cr   = [0.05, 0.18, 0.14, 0.22, 0.12, 0.29]
        rows = [
            ['1',  'קָדַשׁ',      '', '', '', ''],
            ['2',  'קִדֵּשׁ',     '', '', '', ''],
            ['3',  'הִתְקַדֵּשׁ', '', '', '', ''],
            ['4',  'נִקְדַּשׁ',   '', '', '', ''],
            ['5',  'הִקְדִּישׁ',  '', '', '', ''],
            ['6',  'קֻדַּשׁ',     '', '', '', ''],
            ['7',  'דִּבֶּר',     '', '', '', ''],
            ['8',  'דָּבַר',      '', '', '', ''],
            ['9',  'הִתְדַּבֵּר', '', '', '', ''],
            ['10', 'יְקַדֵּשׁ',   '', '', '', ''],
            ['11', 'יִקְדַּשׁ',   '', '', '', ''],
            ['12', 'יִתְקַדֵּשׁ', '', '', '', ''],
            ['13', 'יִקָּדֵשׁ',   '', '', '', ''],
            ['14', 'יַקְדִּישׁ',  '', '', '', ''],
            ['15', 'יְקֻדַּשׁ',   '', '', '', ''],
            ['16', 'וַיְקַדֵּשׁ', '', '', '', ''],
            ['17', 'וַיִּקְדַּשׁ','', '', '', ''],
            ['18', 'וַיִּתְקַדֵּשׁ','','', '', ''],
            ['19', 'קַדֵּשׁ',     '', '', '', ''],
            ['20', 'הִתְקַדֵּשׁ', '', '', '', ''],
            ['21', 'הִקָּדֵשׁ',   '', '', '', ''],
            ['22', 'מְקַדֵּשׁ',   '', '', '', ''],
            ['23', 'מִתְקַדֵּשׁ', '', '', '', ''],
            ['24', 'מַקְדִּישׁ',  '', '', '', ''],
        ]
        ans = [
            ['1',  'קָדַשׁ',      'Qal',     'Perfect',    '3ms', 'קדשׁ'],
            ['2',  'קִדֵּשׁ',     'Piel',    'Perfect',    '3ms', 'קדשׁ'],
            ['3',  'הִתְקַדֵּשׁ', 'Hithpael','Perfect',    '3ms', 'קדשׁ'],
            ['4',  'נִקְדַּשׁ',   'Niphal',  'Perfect',    '3ms', 'קדשׁ'],
            ['5',  'הִקְדִּישׁ',  'Hiphil',  'Perfect',    '3ms', 'קדשׁ'],
            ['6',  'קֻדַּשׁ',     'Pual',    'Perfect',    '3ms', 'קדשׁ'],
            ['7',  'דִּבֶּר',     'Piel',    'Perfect',    '3ms', 'דבר'],
            ['8',  'דָּבַר',      'Qal',     'Perfect',    '3ms', 'דבר'],
            ['9',  'הִתְדַּבֵּר', 'Hithpael','Perfect',    '3ms', 'דבר'],
            ['10', 'יְקַדֵּשׁ',   'Piel',    'Imperfect',  '3ms', 'קדשׁ'],
            ['11', 'יִקְדַּשׁ',   'Qal',     'Imperfect',  '3ms', 'קדשׁ'],
            ['12', 'יִתְקַדֵּשׁ', 'Hithpael','Imperfect',  '3ms', 'קדשׁ'],
            ['13', 'יִקָּדֵשׁ',   'Niphal',  'Imperfect',  '3ms', 'קדשׁ'],
            ['14', 'יַקְדִּישׁ',  'Hiphil',  'Imperfect',  '3ms', 'קדשׁ'],
            ['15', 'יְקֻדַּשׁ',   'Pual',    'Imperfect',  '3ms', 'קדשׁ'],
            ['16', 'וַיְקַדֵּשׁ', 'Piel',    'Wayyiqtol',  '3ms', 'קדשׁ'],
            ['17', 'וַיִּקְדַּשׁ','Qal',     'Wayyiqtol',  '3ms', 'קדשׁ'],
            ['18', 'וַיִּתְקַדֵּשׁ','Hithpael','Wayyiqtol', '3ms', 'קדשׁ'],
            ['19', 'קַדֵּשׁ',     'Piel',    'Imperative', '2ms', 'קדשׁ'],
            ['20', 'הִתְקַדֵּשׁ', 'Hithpael','Imperative', '2ms', 'קדשׁ'],
            ['21', 'הִקָּדֵשׁ',   'Niphal',  'Imperative', '2ms', 'קדשׁ'],
            ['22', 'מְקַדֵּשׁ',   'Piel',    'Participle', 'ms',  'קדשׁ'],
            ['23', 'מִתְקַדֵּשׁ', 'Hithpael','Participle', 'ms',  'קדשׁ'],
            ['24', 'מַקְדִּישׁ',  'Hiphil',  'Participle', 'ms',  'קדשׁ'],
        ]
        self.add_drill_with_answer_key(
            hdrs, rows, ans,
            col_ratios=cr,
            heb_cols=[1],
            answer_heb_cols=[1, 5],
            section_title='All Major Stems — Strong Roots: קדשׁ / דבר (24 forms)',
            answer_title='Answer Key',
        )


def build_ch34_stem_id_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch34StemIdDrill,
        'Chapter 34 — Stem-ID Drill (Strong Roots)',
        'BBH Chapter 34 · Hithpael Strong Verbs',
        ['hebrew', 'bbh', 'ch34', 'exercises', 'ch34-stem-id-drill'],
        'ch34-stem-id-drill.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch35 — Qal–Piel–Hithpael Contrast Drill (Weak Roots)
# ---------------------------------------------------------------------------


class Ch35QalPielHithpaelContrastExercise(ExercisePDF):

    def _build(self) -> None:
        self.add_instructions(
            'Five groups of three forms — each group shows a weak root in '
            'Qal, Piel, and Hithpael Perfect 3ms. '
            'For each: (1) identify the stem, (2) identify the weak class, '
            '(3) state how the weakness affects the form, (4) translate. '
            'Answer key at the bottom.'
        )
        self.add_note(
            'III-ה: perfect 3ms ends in ָ–ה; wayyiqtol apocopates (ה dropped).  '
            'Sibilant (שׁ/שׂ/ס): הִתְ + שׁ → הִשְׁתְּ (ת and שׁ swap).  '
            'Sibilant (צ): הִתְ + צ → ת assimilates to ט and swaps → הִצְטְ.  '
            'Geminate (R2=R3): Dagesh Forte in R2/R3; compensatory lengthening.'
        )

        hdr = ['#', 'Hebrew', 'Stem', 'Weak Class', 'Weakness Effect', 'Translation']
        cr  = [0.04, 0.16, 0.12, 0.14, 0.28, 0.26]

        groups = [
            ('Group 1 — Root: גלה (III-ה)', [
                ['1', 'גָּלָה',       '', '', '', ''],
                ['2', 'גִּלָּה',      '', '', '', ''],
                ['3', 'הִתְגַּלָּה',  '', '', '', ''],
            ], [
                ['1', 'גָּלָה',       'Qal',      'III-ה', 'Perfect 3ms ends in ָ–ה; ה = weak R3',                         'he went into exile / uncovered'],
                ['2', 'גִּלָּה',      'Piel',     'III-ה', 'Dagesh in R2 (לּ); R3-ה contracts to ָה',                      'he revealed'],
                ['3', 'הִתְגַּלָּה',  'Hithpael', 'III-ה', 'הִתְ prefix + dagesh in R2 + ָה ending (R3-ה preserved)',        'he revealed himself'],
            ]),
            ('Group 2 — Root: שׁמר (sibilant metathesis)', [
                ['4', 'שָׁמַר',       '', '', '', ''],
                ['5', 'שִׁמֵּר',      '', '', '', ''],
                ['6', 'הִשְׁתַּמֵּר', '', '', '', ''],
            ], [
                ['4', 'שָׁמַר',       'Qal',      'sibilant (R1=שׁ)', 'No effect in Qal; sibilant only affects Hithpael prefix', 'he kept / guarded'],
                ['5', 'שִׁמֵּר',      'Piel',     'sibilant (R1=שׁ)', 'No effect in Piel',                                       'he kept carefully / watched over'],
                ['6', 'הִשְׁתַּמֵּר', 'Hithpael', 'sibilant metathesis', 'הִתְ + שׁ → הִשְׁתְּ (ת and שׁ swap); dagesh in R2',   'he kept himself / was on guard'],
            ]),
            ('Group 3 — Root: צדק (sibilant צ with assimilation)', [
                ['7', 'צָדַק',        '', '', '', ''],
                ['8', 'צִדֵּק',       '', '', '', ''],
                ['9', 'הִצְטַדֵּק',   '', '', '', ''],
            ], [
                ['7', 'צָדַק',        'Qal',      'sibilant (R1=צ)', 'No effect in Qal',                                              'he was righteous'],
                ['8', 'צִדֵּק',       'Piel',     'sibilant (R1=צ)', 'No effect in Piel',                                             'he declared righteous / justified'],
                ['9', 'הִצְטַדֵּק',   'Hithpael', 'sibilant metathesis + assimilation', 'הִתְ + צ → ת→ט + swaps with צ → הִצְטְ',   'he justified himself'],
            ]),
            ('Group 4 — Root: הלל (geminate: R2=R3=ל)', [
                ['10', 'הָלַל',        '', '', '', ''],
                ['11', 'הִלֵּל',       '', '', '', ''],
                ['12', 'הִתְהַלֵּל',   '', '', '', ''],
            ], [
                ['10', 'הָלַל',        'Qal',      'geminate', 'Both ל radicals appear; no contraction in Qal perf. 3ms',        'he shone / praised'],
                ['11', 'הִלֵּל',       'Piel',     'geminate', 'Dagesh Forte in R2=R3 (לּ); Tsere under R1',                     'he praised'],
                ['12', 'הִתְהַלֵּל',   'Hithpael', 'geminate', 'הִתְ prefix + Dagesh Forte in R2/R3 (לּ)',                       'he boasted / praised himself'],
            ]),
            ('Group 5 — Root: ענה (III-ה: to answer/afflict)', [
                ['13', 'עָנָה',         '', '', '', ''],
                ['14', 'עִנָּה',        '', '', '', ''],
                ['15', 'הִתְעַנָּה',    '', '', '', ''],
            ], [
                ['13', 'עָנָה',         'Qal',      'III-ה', 'Perfect 3ms ends in ָ–ה',                                          'he answered'],
                ['14', 'עִנָּה',        'Piel',     'III-ה', 'Dagesh in R2 (נּ) + ָה ending',                                    'he afflicted'],
                ['15', 'הִתְעַנָּה',    'Hithpael', 'III-ה', 'הִתְ prefix + dagesh in R2 + ָה ending (R3-ה preserved)',          'he afflicted himself / fasted'],
            ]),
        ]

        for title, rows, ans in groups:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1], show_answers=False)
            self.add_section_break()

        self.add_section_heading('Answer Key')
        for title, rows, ans in groups:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=True, answer_rows=ans)


def build_ch35_qal_piel_hithpael_contrast(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch35QalPielHithpaelContrastExercise,
        'Chapter 35 — Qal / Piel / Hithpael Contrast Drill (Weak Roots)',
        'BBH Chapter 35 · Hithpael Weak Verbs',
        ['hebrew', 'bbh', 'ch35', 'exercises', 'ch35-qal-piel-hithpael-contrast'],
        'ch35-qal-piel-hithpael-contrast.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch35 — Hithpael Function Sort (Weak Roots)
# ---------------------------------------------------------------------------


class Ch35FunctionSortExercise(ExercisePDF):

    def _build(self) -> None:
        self.add_instructions(
            'For each weak-root Hithpael form, classify the semantic function: '
            'R (Reflexive), Re (Reciprocal), I (Intensive/Iterative), SA (Simple Action). '
            'Each item gives the Hebrew form, conjugation, root, reference, and gloss. '
            'Answer key at the bottom.'
        )
        hdrs = ['#', 'Hebrew', 'Conjugation', 'Root', 'Ref', 'Gloss', 'Function']
        cr   = [0.04, 0.14, 0.16, 0.08, 0.10, 0.34, 0.14]
        rows = [
            ['1',  'הִתְגַּלָּה',    'Perfect 3ms',   'גלה', 'Gen 35:7',   '"God revealed himself"',                     ''],
            ['2',  'הִשְׁתַּחֲוָה',  'Perfect 3ms',   'שׁחה','Gen 22:5',   '"we will worship / bow down"',                ''],
            ['3',  'הִתְהַלֵּל',    'Perfect 3ms',   'הלל', 'Jer 9:23',   '"let him not boast"',                         ''],
            ['4',  'הִתְפַּלֵּל',   'Perfect 3ms',   'פלל', 'Gen 20:7',   '"he prayed"',                                 ''],
            ['5',  'הִתְעַנָּה',    'Perfect 3ms',   'ענה', 'Ezr 8:21',   '"we afflicted ourselves / fasted"',           ''],
            ['6',  'יִתְגַּלֶּה',   'Imperfect 3ms', 'גלה', '—',          '"he will reveal himself"',                    ''],
            ['7',  'יִשְׁתַּחֲוֶה', 'Imperfect 3ms', 'שׁחה','—',          '"he will bow down"',                          ''],
            ['8',  'יִתְהַלֵּל',   'Imperfect 3ms', 'הלל', 'Jer 9:23',   '"let him boast"',                             ''],
            ['9',  'יִתְפַּלֵּל',  'Imperfect 3ms', 'פלל', '—',          '"he will pray"',                              ''],
            ['10', 'וַיִּתְגַּל',   'Wayyiqtol 3ms', 'גלה', 'Gen 9:21',   '"he uncovered himself"',                      ''],
            ['11', 'וַיִּשְׁתַּחוּ','Wayyiqtol 3ms', 'שׁחה','Gen 22:5',   '"and he bowed down"',                         ''],
            ['12', 'וַיִּתְפַּלֵּל','Wayyiqtol 3ms', 'פלל', 'Gen 20:17',  '"Abraham prayed"',                            ''],
            ['13', 'הִתְנַבֵּא',   'Perfect 3ms',   'נבא', '1 Sam 10:10','"he prophesied"',                             ''],
            ['14', 'הִתְחַזֵּק',   'Perfect 3ms',   'חזק', '2 Sam 10:12','"take courage! / be strong!"',               ''],
            ['15', 'הִתְנַחֵם',    'Perfect 3ms',   'נחם', 'Gen 24:67',  '"Isaac was comforted"',                       ''],
            ['16', 'הִתְבָּרֵךְ',  'Perfect 3ms',   'ברך', 'Gen 22:18',  '"all nations will bless themselves"',         ''],
            ['17', 'הִצְטַדֵּק',   'Perfect 3ms',   'צדק', '—',          '"he justified himself"',                      ''],
            ['18', 'הִתְרַגֵּז',   'Perfect 3ms',   'רגז', '—',          '"he trembled / was agitated"',                ''],
            ['19', 'הִתְחַנֵּן',   'Perfect 3ms',   'חנן', '—',          '"he pleaded for mercy / implored"',           ''],
            ['20', 'הִתְנַהֵג',    'Perfect 3ms',   'נהג', '—',          '"he conducted himself / behaved"',            ''],
        ]
        ans = [
            ['1',  'הִתְגַּלָּה',    'Perfect 3ms',   'גלה', 'Gen 35:7',    '"God revealed himself"',                     'R'],
            ['2',  'הִשְׁתַּחֲוָה',  'Perfect 3ms',   'שׁחה','Gen 22:5',    '"we will worship / bow down"',                'R'],
            ['3',  'הִתְהַלֵּל',    'Perfect 3ms',   'הלל', 'Jer 9:23',    '"let him not boast"',                         'R'],
            ['4',  'הִתְפַּלֵּל',   'Perfect 3ms',   'פלל', 'Gen 20:7',    '"he prayed"',                                 'SA'],
            ['5',  'הִתְעַנָּה',    'Perfect 3ms',   'ענה', 'Ezr 8:21',    '"we afflicted ourselves / fasted"',           'R'],
            ['6',  'יִתְגַּלֶּה',   'Imperfect 3ms', 'גלה', '—',           '"he will reveal himself"',                    'R'],
            ['7',  'יִשְׁתַּחֲוֶה', 'Imperfect 3ms', 'שׁחה','—',           '"he will bow down"',                          'R'],
            ['8',  'יִתְהַלֵּל',   'Imperfect 3ms', 'הלל', 'Jer 9:23',    '"let him boast"',                             'R'],
            ['9',  'יִתְפַּלֵּל',  'Imperfect 3ms', 'פלל', '—',           '"he will pray"',                              'SA'],
            ['10', 'וַיִּתְגַּל',   'Wayyiqtol 3ms', 'גלה', 'Gen 9:21',    '"he uncovered himself"',                      'R'],
            ['11', 'וַיִּשְׁתַּחוּ','Wayyiqtol 3ms', 'שׁחה','Gen 22:5',    '"and he bowed down"',                         'R'],
            ['12', 'וַיִּתְפַּלֵּל','Wayyiqtol 3ms', 'פלל', 'Gen 20:17',   '"Abraham prayed"',                            'SA'],
            ['13', 'הִתְנַבֵּא',   'Perfect 3ms',   'נבא', '1 Sam 10:10', '"he prophesied"',                             'SA'],
            ['14', 'הִתְחַזֵּק',   'Perfect 3ms',   'חזק', '2 Sam 10:12', '"take courage! / be strong!"',               'R'],
            ['15', 'הִתְנַחֵם',    'Perfect 3ms',   'נחם', 'Gen 24:67',   '"Isaac was comforted"',                       'R'],
            ['16', 'הִתְבָּרֵךְ',  'Perfect 3ms',   'ברך', 'Gen 22:18',   '"all nations will bless themselves"',         'R'],
            ['17', 'הִצְטַדֵּק',   'Perfect 3ms',   'צדק', '—',           '"he justified himself"',                      'R'],
            ['18', 'הִתְרַגֵּז',   'Perfect 3ms',   'רגז', '—',           '"he trembled / was agitated"',                'I'],
            ['19', 'הִתְחַנֵּן',   'Perfect 3ms',   'חנן', '—',           '"he pleaded for mercy / implored"',           'I'],
            ['20', 'הִתְנַהֵג',    'Perfect 3ms',   'נהג', '—',           '"he conducted himself / behaved"',            'R'],
        ]
        self.add_drill_with_answer_key(
            hdrs, rows, ans,
            col_ratios=cr,
            heb_cols=[1, 3],
            answer_heb_cols=[1, 3],
            section_title='Hithpael Semantic Function Sort — 20 Weak-Root Forms',
            answer_title='Answer Key',
        )


def build_ch35_function_sort(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch35FunctionSortExercise,
        'Chapter 35 — Hithpael Function Sort (Weak Roots)',
        'BBH Chapter 35 · Hithpael Weak Verbs',
        ['hebrew', 'bbh', 'ch35', 'exercises', 'ch35-function-sort'],
        'ch35-function-sort.pdf', out_dir,
    )


# ---------------------------------------------------------------------------
# Ch35 — Stem-ID Drill (Weak Roots)
# ---------------------------------------------------------------------------


class Ch35StemIdDrill(ExercisePDF):
    _instructions = (
        'Identify the stem, conjugation, PGN, and root of each form below. '
        'Weak roots used: גלה (III-ה), הלל (geminate), ענה (III-ה). '
        'Stems covered: Qal, Piel, Hithpael (8 items each, 24 total). '
        'Key challenge: in wayyiqtol, the III-ה ending is dropped (apocopation).'
    )

    def _build(self) -> None:
        self.add_instructions(self._instructions)
        hdrs = ['#', 'Hebrew Form', 'Stem', 'Conjugation', 'PGN', 'Root']
        cr   = [0.05, 0.20, 0.14, 0.22, 0.12, 0.27]
        rows = [
            ['1',  'גָּלָה',        '', '', '', ''],
            ['2',  'גִּלָּה',       '', '', '', ''],
            ['3',  'הִתְגַּלָּה',   '', '', '', ''],
            ['4',  'הָלַל',         '', '', '', ''],
            ['5',  'הִלֵּל',        '', '', '', ''],
            ['6',  'הִתְהַלֵּל',    '', '', '', ''],
            ['7',  'עָנָה',         '', '', '', ''],
            ['8',  'עִנָּה',        '', '', '', ''],
            ['9',  'הִתְעַנָּה',    '', '', '', ''],
            ['10', 'יְגַלֶּה',      '', '', '', ''],
            ['11', 'יִגְלֶה',       '', '', '', ''],
            ['12', 'יִתְגַּלֶּה',   '', '', '', ''],
            ['13', 'יְהַלֵּל',      '', '', '', ''],
            ['14', 'יִתְהַלֵּל',    '', '', '', ''],
            ['15', 'יְעַנֶּה',      '', '', '', ''],
            ['16', 'וַיְגַל',       '', '', '', ''],
            ['17', 'וַיִּגֶּל',     '', '', '', ''],
            ['18', 'וַיִּתְגַּל',   '', '', '', ''],
            ['19', 'גַּלֵּה',       '', '', '', ''],
            ['20', 'גְּלֵה',        '', '', '', ''],
            ['21', 'הִתְגַּלֵּה',   '', '', '', ''],
            ['22', 'מְגַלֶּה',      '', '', '', ''],
            ['23', 'גֹּלֶה',        '', '', '', ''],
            ['24', 'מִתְגַּלֶּה',   '', '', '', ''],
        ]
        ans = [
            ['1',  'גָּלָה',        'Qal',     'Perfect',    '3ms', 'גלה'],
            ['2',  'גִּלָּה',       'Piel',    'Perfect',    '3ms', 'גלה'],
            ['3',  'הִתְגַּלָּה',   'Hithpael','Perfect',    '3ms', 'גלה'],
            ['4',  'הָלַל',         'Qal',     'Perfect',    '3ms', 'הלל'],
            ['5',  'הִלֵּל',        'Piel',    'Perfect',    '3ms', 'הלל'],
            ['6',  'הִתְהַלֵּל',    'Hithpael','Perfect',    '3ms', 'הלל'],
            ['7',  'עָנָה',         'Qal',     'Perfect',    '3ms', 'ענה'],
            ['8',  'עִנָּה',        'Piel',    'Perfect',    '3ms', 'ענה'],
            ['9',  'הִתְעַנָּה',    'Hithpael','Perfect',    '3ms', 'ענה'],
            ['10', 'יְגַלֶּה',      'Piel',    'Imperfect',  '3ms', 'גלה'],
            ['11', 'יִגְלֶה',       'Qal',     'Imperfect',  '3ms', 'גלה'],
            ['12', 'יִתְגַּלֶּה',   'Hithpael','Imperfect',  '3ms', 'גלה'],
            ['13', 'יְהַלֵּל',      'Piel',    'Imperfect',  '3ms', 'הלל'],
            ['14', 'יִתְהַלֵּל',    'Hithpael','Imperfect',  '3ms', 'הלל'],
            ['15', 'יְעַנֶּה',      'Piel',    'Imperfect',  '3ms', 'ענה'],
            ['16', 'וַיְגַל',       'Piel',    'Wayyiqtol',  '3ms', 'גלה'],
            ['17', 'וַיִּגֶּל',     'Qal',     'Wayyiqtol',  '3ms', 'גלה'],
            ['18', 'וַיִּתְגַּל',   'Hithpael','Wayyiqtol',  '3ms', 'גלה'],
            ['19', 'גַּלֵּה',       'Piel',    'Imperative', '2ms', 'גלה'],
            ['20', 'גְּלֵה',        'Qal',     'Imperative', '2ms', 'גלה'],
            ['21', 'הִתְגַּלֵּה',   'Hithpael','Imperative', '2ms', 'גלה'],
            ['22', 'מְגַלֶּה',      'Piel',    'Participle', 'ms',  'גלה'],
            ['23', 'גֹּלֶה',        'Qal',     'Participle', 'ms',  'גלה'],
            ['24', 'מִתְגַּלֶּה',   'Hithpael','Participle', 'ms',  'גלה'],
        ]
        self.add_drill_with_answer_key(
            hdrs, rows, ans,
            col_ratios=cr,
            heb_cols=[1],
            answer_heb_cols=[1, 5],
            section_title='Qal / Piel / Hithpael — Weak Roots (24 forms)',
            answer_title='Answer Key',
        )


def build_ch35_stem_id_drill(out_dir: Optional[str] = None) -> str:
    return _build_exercise_pdf(
        Ch35StemIdDrill,
        'Chapter 35 — Stem-ID Drill (Weak Roots)',
        'BBH Chapter 35 · Hithpael Weak Verbs',
        ['hebrew', 'bbh', 'ch35', 'exercises', 'ch35-stem-id-drill'],
        'ch35-stem-id-drill.pdf', out_dir,
    )
