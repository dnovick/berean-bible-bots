from ._base import ExercisePDF, _build_exercise_pdf
import os

# ---------------------------------------------------------------------------
# BBA Ch1 — Aramaic Letter Recognition
# ---------------------------------------------------------------------------

class BbaCh1LetterRecognitionPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each Aramaic letter: (1) Letter Name, (2) Transliteration, '
            '(3) Sound, (4) Special Category (Guttural/Emphatic/Bgdkpt/Normal), '
            '(5) Corresponding Hebrew letter.'
        )
        hdrs = ['#', 'Letter', 'Name', 'Translit.', 'Sound', 'Category', 'Heb. Equiv.']
        cr = [0.04, 0.07, 0.11, 0.10, 0.14, 0.15, 0.39]
        hc = [1]
        tc = [3]   # transliteration column
        rows = [
            ['1',  'א', '', '', '', '', ''], ['2',  'ב', '', '', '', '', ''],
            ['3',  'ג', '', '', '', '', ''], ['4',  'ד', '', '', '', '', ''],
            ['5',  'ה', '', '', '', '', ''], ['6',  'ו', '', '', '', '', ''],
            ['7',  'ז', '', '', '', '', ''], ['8',  'ח', '', '', '', '', ''],
            ['9',  'ט', '', '', '', '', ''], ['10', 'י', '', '', '', '', ''],
            ['11', 'כ', '', '', '', '', ''], ['12', 'ל', '', '', '', '', ''],
            ['13', 'מ', '', '', '', '', ''], ['14', 'נ', '', '', '', '', ''],
            ['15', 'ס', '', '', '', '', ''], ['16', 'ע', '', '', '', '', ''],
            ['17', 'פ', '', '', '', '', ''], ['18', 'צ', '', '', '', '', ''],
            ['19', 'ק', '', '', '', '', ''], ['20', 'ר', '', '', '', '', ''],
            ['21', 'שׁ','', '', '', '', ''], ['22', 'ת', '', '', '', '', ''],
        ]
        ans = [
            ['1',  'א', 'Aleph',  'ʾ',     'Silent (glottal)',       'Guttural',              'Same'],
            ['2',  'ב', 'Beth',   'b / v', 'b (hard) / v (soft)',    'Bgdkpt',                'Same'],
            ['3',  'ג', 'Gimel',  'g',     'g',                      'Bgdkpt',                'Same'],
            ['4',  'ד', 'Dalet',  'd/dh',  'd (hard) / dh',          'Bgdkpt',                'Same'],
            ['5',  'ה', 'He',     'h',     'h',                      'Guttural',              'Same (often quiescent)'],
            ['6',  'ו', 'Waw',    'w',     'w',                      'Normal / vowel letter', 'Same'],
            ['7',  'ז', 'Zayin',  'z',     'z',                      'Normal',                'Same'],
            ['8',  'ח', 'Cheth',  'ḥ',     'ch (guttural)',           'Guttural',              'Same'],
            ['9',  'ט', 'Teth',   'ṭ',     't (emphatic)',            'Emphatic',              'Same'],
            ['10', 'י', 'Yod',    'y',     'y',                      'Normal / vowel letter', 'Same'],
            ['11', 'כ', 'Kaph',   'k/kh',  'k (hard) / kh',          'Bgdkpt',                'Same'],
            ['12', 'ל', 'Lamed',  'l',     'l',                      'Normal',                'Same'],
            ['13', 'מ', 'Mem',    'm',     'm',                      'Normal',                'Same'],
            ['14', 'נ', 'Nun',    'n',     'n',                      'Normal',                'Same'],
            ['15', 'ס', 'Samech', 's',     's',                      'Normal',                'Same'],
            ['16', 'ע', 'Ayin',   'ʿ',     'Silent (pharyngeal)',     'Guttural',              'Same'],
            ['17', 'פ', 'Pe',     'p / f', 'p (hard) / f',           'Bgdkpt',                'Same'],
            ['18', 'צ', 'Tsade',  'ṣ',     'ts (emphatic)',           'Emphatic',              'Same'],
            ['19', 'ק', 'Qoph',   'q',     'q (uvular)',              'Emphatic',              'Same'],
            ['20', 'ר', 'Resh',   'r',     'r',                      'Normal (resists Dagesh)', 'Same'],
            ['21', 'שׁ','Shin',   'š',     'sh',                     'Normal',                'Same (Heb. שׁ often = Aram. תּ)'],
            ['22', 'ת', 'Taw',    't',     't / th',                 'Bgdkpt',                'Same'],
        ]
        self.add_section_heading('All 22 Aramaic Letters')
        self.add_generic_table(hdrs, rows, col_ratios=cr, heb_cols=hc, translit_cols=tc, show_answers=False)
        self.add_section_heading('Answer Key')
        self.add_generic_table(hdrs, rows, col_ratios=cr, heb_cols=hc, translit_cols=tc, show_answers=True, answer_rows=ans)



def build_bba_ch1_letter_recognition(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh1LetterRecognitionPDF,
        'BBA Chapter 1 — Aramaic Letter Recognition',
        'All 22 Letters · Gutturals · Emphatics · Bgdkpt · Hebrew Comparison',
        ['aramaic', 'bba', 'ch1', 'exercises', 'ch1-letter-recognition'],
        'ch1-letter-recognition.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBA Ch2 — Aramaic Vowel Identification
# ---------------------------------------------------------------------------

class BbaCh2VowelIdentificationPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each vowel form: (1) Vowel Name, (2) Class (Long/Short/Reduced), '
            '(3) Transliteration, (4) Mater Lectionis? (Yes/No), (5) Notes.'
        )
        hc = [1]
        hdrs_abc = ['#', 'Form', 'Vowel Name', 'Class', 'Translit.', 'Mater?', 'Notes']
        cr_abc = [0.04, 0.10, 0.14, 0.10, 0.08, 0.08, 0.46]
        hdrs_c = ['#', 'Form', 'Vowel Name', 'Class', 'Translit.', 'Notes']
        cr_c = [0.04, 0.10, 0.16, 0.10, 0.08, 0.52]
        hdrs_d = ['#', 'Form', 'Mater Letter', 'Vowel', 'Notes']
        cr_d = [0.04, 0.14, 0.14, 0.10, 0.58]
        self.add_multi_part_drill([
            {
                'title': 'Part A — Long Vowels (1–5)',
                'headers': hdrs_abc,
                'rows': [
                    ['1','בָּ','','','','',''], ['2','בֵּ','','','','',''],
                    ['3','בִּי','','','','',''], ['4','בּוֹ','','','','',''],
                    ['5','בּוּ','','','','',''],
                ],
                'answers': [
                    ['1','בָּ', 'Qamets',     'Long',    'ā', 'No',        'Most common long vowel'],
                    ['2','בֵּ', 'Tsere',      'Long',    'ē', 'No (plain)','Often has Yod mater'],
                    ['3','בִּי','Hireq Gadol','Long',    'ī', 'Yes — Yod', 'Yod is the mater'],
                    ['4','בּוֹ','Holem',      'Long',    'ō', 'Yes — Waw', 'Waw above-right of consonant'],
                    ['5','בּוּ','Shuruq',     'Long',    'ū', 'Yes — Waw', 'Dot in middle of Waw'],
                ],
                'col_ratios': cr_abc,
                'translit_cols': [4],
            },
            {
                'title': 'Part B — Short Vowels (6–10)',
                'headers': hdrs_abc,
                'rows': [
                    ['6', 'בַּ','','','','',''], ['7','בֶּ','','','','',''],
                    ['8', 'בִּ','','','','',''], ['9','בָּ (closed unstr.)','','','','',''],
                    ['10','בֻּ','','','','',''],
                ],
                'answers': [
                    ['6', 'בַּ', 'Patach',       'Short',   'a', 'No', 'Most common short vowel'],
                    ['7', 'בֶּ', 'Seghol',       'Short',   'e', 'No', 'Triangle of three dots'],
                    ['8', 'בִּ', 'Hireq Qatan',  'Short',   'i', 'No', 'No Yod mater'],
                    ['9', 'בָּ', 'Qamets Hatuph','Short',   'o', 'No', 'Same sign as Qamets; context determines'],
                    ['10','בֻּ', 'Qibbuts',      'Short',   'u', 'No', 'Three diagonal dots'],
                ],
                'col_ratios': cr_abc,
                'translit_cols': [4],
            },
            {
                'title': 'Part C — Reduced Vowels (11–15)',
                'headers': hdrs_c,
                'rows': [
                    ['11','בְּ (vocal)','','','',''], ['12','בְּ (silent)','','','',''],
                    ['13','אֲ','','','',''],          ['14','אֱ','','','',''],
                    ['15','אֳ','','','',''],
                ],
                'answers': [
                    ['11','בְּ','Vocal Sheva',   'Reduced','ə', 'Brief neutral vowel; opens syllable'],
                    ['12','בְּ','Silent Sheva',  '—',      '—', 'Closes syllable; not pronounced'],
                    ['13','אֲ', 'Hateph Patach', 'Reduced','ă', 'Under gutturals; very brief "ah"'],
                    ['14','אֱ', 'Hateph Seghol', 'Reduced','ĕ', 'Under gutturals; very brief "eh"'],
                    ['15','אֳ', 'Hateph Qamets', 'Reduced','ŏ', 'Under gutturals; rare; very brief "oh"'],
                ],
                'col_ratios': cr_c,
                'translit_cols': [4],
            },
            {
                'title': 'Part D — Matres Lectionis (16–20)',
                'headers': hdrs_d,
                'rows': [
                    ['16','מַלְכָּא','','',''], ['17','כְּתִיב','','',''],
                    ['18','שְׁלוֹ','','',''],  ['19','בּוּ','','',''],
                    ['20','אֱלָהָא','','',''],
                ],
                'answers': [
                    ['16','מַלְכָּא','א (Aleph)','ā (final)','Determined state suffix; Aleph is mater'],
                    ['17','כְּתִיב', 'י (Yod)',  'ī',        'Yod after Hireq = long ī'],
                    ['18','שְׁלוֹ',  'ו (Waw)',  'ō',        'Waw after Holem dot = long ō'],
                    ['19','בּוּ',    'ו (Waw)',  'ū',        'Shuruq — dot in middle of Waw'],
                    ['20','אֱלָהָא','א (Aleph)','ā (final)','Determined state suffix again'],
                ],
                'col_ratios': cr_d,
                'translit_cols': [3],
            },
        ], heb_cols=hc)


def build_bba_ch2_vowel_identification(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh2VowelIdentificationPDF,
        'BBA Chapter 2 — Aramaic Vowel Identification',
        'Long · Short · Reduced Vowels · Matres Lectionis',
        ['aramaic', 'bba', 'ch2', 'exercises', 'ch2-vowel-identification'],
        'ch2-vowel-identification.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBA Ch3 — Aramaic Syllabification Drill
# ---------------------------------------------------------------------------

class BbaCh3SyllabificationDrillPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each word: (1) divide into syllables using |, '
            '(2) label each syllable O (open) or C (closed), '
            '(3) mark stressed syllable with ′, '
            '(4) note any special features (Dagesh Forte, quiescence, etc.).'
        )
        hdrs = ['#', 'Word', 'Translit.', 'Division', 'Types', 'Stress', 'Special Features']
        cr = [0.04, 0.12, 0.14, 0.16, 0.10, 0.14, 0.30]
        hc = [1]
        tc = [2]
        self.add_multi_part_drill([
            {
                'title': 'Part A — Basic Division (1–8)',
                'headers': hdrs,
                'rows': [
                    ['1', 'מַלְכָּא',  'malkāʾ',        '', '', '', ''],
                    ['2', 'אֱלָהָא',   'ʾĕlāhāʾ',       '', '', '', ''],
                    ['3', 'בֵּית',     'bêt',            '', '', '', ''],
                    ['4', 'מַלְכִין',  'malkîn',         '', '', '', ''],
                    ['5', 'כְּתַב',    'kətab',          '', '', '', ''],
                    ['6', 'אֲבוּהִי',  'ʾăbûhî',         '', '', '', ''],
                    ['7', 'יְהוּד',    'yəhûd',          '', '', '', ''],
                    ['8', 'שְׁמַיָּא', 'šəmayyāʾ',       '', '', '', ''],
                ],
                'answers': [
                    ['1', 'מַלְכָּא',  'malkāʾ',   'מַל | כָּא',          'C · C',        '′כָּא',   'Final א quiescent (det. state)'],
                    ['2', 'אֱלָהָא',   'ʾĕlāhāʾ',  'אֱ | לָ | הָא',        'O · O · C',    '′הָא',    'Hateph seghol; final א quiescent'],
                    ['3', 'בֵּית',     'bêt',       'בֵּית',                'C (monosyll.)', '′בֵּית',  'Waw is mater for Tsere'],
                    ['4', 'מַלְכִין',  'malkîn',    'מַל | כִין',           'C · C',        '′כִין',   'Yod is mater for Hireq Gadol'],
                    ['5', 'כְּתַב',    'kətab',     'כְּ | תַב',            'O · C',        '′תַב',    'Opening sheva = vocal'],
                    ['6', 'אֲבוּהִי',  'ʾăbûhî',    'אֲ | בוּ | הִי',       'O · O · O',    '′הִי',    'Hateph Patach; Waw = Shuruq; Yod = mater'],
                    ['7', 'יְהוּד',    'yəhûd',     'יְ | הוּד',            'O · C',        '′הוּד',   'Opening sheva = vocal; Waw = Shuruq'],
                    ['8', 'שְׁמַיָּא', 'šəmayyāʾ',  'שְׁ | מַי | יָא',      'O · C · C',    '′יָא',    'Dagesh Forte in Yod = doubled'],
                ],
                'col_ratios': cr,
                'translit_cols': tc,
            },
            {
                'title': 'Part B — Dagesh Forte Doubling (9–12)',
                'headers': hdrs,
                'rows': [
                    ['9',  'שַׁבַּת',    'šabbat',   '', '', '', ''],
                    ['10', 'כַּסְּדִים', 'kaśśədîm', '', '', '', ''],
                    ['11', 'הַדַּבְרִין','haddabrîn', '', '', '', ''],
                    ['12', 'מִנַּי',     'minnay',   '', '', '', ''],
                ],
                'answers': [
                    ['9',  'שַׁבַּת',    'šabbat',   'שַׁב | בַּת',       'C · C',     '′בַּת', 'Dagesh Forte in Beth'],
                    ['10', 'כַּסְּדִים', 'kaśśədîm', 'כַּסּ | דִים',      'C · C',     '′דִים', 'Dagesh Forte in Samech'],
                    ['11', 'הַדַּבְרִין','haddabrîn', 'הַד | דַבְ | רִין', 'C · C · C', '′רִין', 'Dagesh Forte in Dalet'],
                    ['12', 'מִנַּי',     'minnay',   'מִנ | נַי',         'C · O',     '′נַי', 'Dagesh Forte in Nun (assimilation)'],
                ],
                'col_ratios': cr,
                'translit_cols': tc,
            },
            {
                'title': 'Part C — Guttural and Quiescence Features (13–16)',
                'headers': hdrs,
                'rows': [
                    ['13', 'אָמַר',   'ʾāmar',  '', '', '', ''],
                    ['14', 'חַכִּים', 'ḥakkîm', '', '', '', ''],
                    ['15', 'עִם',     'ʿim',    '', '', '', ''],
                    ['16', 'מַלְאַךְ','malʾak', '', '', '', ''],
                ],
                'answers': [
                    ['13', 'אָמַר',   'ʾāmar',  'אָ | מַר',    'O · C',        '′מַר',  'Long Qamets in open syllable; Aleph opens word'],
                    ['14', 'חַכִּים', 'ḥakkîm', 'חַכּ | כִים', 'C · C',        '′כִים', 'Dagesh Forte in Kaph; Cheth = guttural'],
                    ['15', 'עִם',     'ʿim',    'עִם',          'C (monosyll.)', '′עִם',  'Ayin = guttural; short Hireq in closed syllable'],
                    ['16', 'מַלְאַךְ','malʾak', 'מַל | אַךְ',  'C · C',        '′אַךְ', 'Aleph in second syllable; takes Patach'],
                ],
                'col_ratios': cr,
                'translit_cols': tc,
            },
            {
                'title': 'Part D — Accent and Vowel Reduction (17–20)',
                'headers': hdrs,
                'rows': [
                    ['17', 'נְבוּכַדְנֶצַּר', 'nəbûḵadneṣṣar', '', '', '', ''],
                    ['18', 'מַלְכוּתָא',       'malkûtāʾ',       '', '', '', ''],
                    ['19', 'בְּיוֹם',          'bəyôm',          '', '', '', ''],
                    ['20', 'לְמַלְכָּא',       'ləmalkāʾ',       '', '', '', ''],
                ],
                'answers': [
                    ['17', 'נְבוּכַדְנֶצַּר', 'nəbûḵadneṣṣar', 'נְ·בוּ·כַד·נֶצּ·צַר', 'O·O·C·C·C', '′צַר', 'Opening vocal sheva; Dagesh Forte in Tsade; propretonic reduction'],
                    ['18', 'מַלְכוּתָא',       'malkûtāʾ',       'מַל·כוּ·תָא',         'C·O·C',     '′תָא', 'Waw = Shuruq; final א quiescent'],
                    ['19', 'בְּיוֹם',          'bəyôm',          'בְּ·יוֹם',            'O·C',       '′יוֹם','Prefix בְּ = vocal sheva; Waw = Holem mater'],
                    ['20', 'לְמַלְכָּא',       'ləmalkāʾ',       'לְ·מַל·כָּא',         'O·C·C',     '′כָּא', 'Prefix לְ = vocal sheva; propretonic מַ stays short'],
                ],
                'col_ratios': cr,
                'translit_cols': tc,
            },
        ], heb_cols=hc)


def build_bba_ch3_syllabification_drill(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh3SyllabificationDrillPDF,
        'BBA Chapter 3 — Aramaic Syllabification Drill',
        'Open/Closed Syllables · Dagesh Forte · Guttural Quiescence · Accent',
        ['aramaic', 'bba', 'ch3', 'exercises', 'ch3-syllabification-drill'],
        'ch3-syllabification-drill.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBA Ch4 — Noun Identification Drill
# ---------------------------------------------------------------------------

class BbaCh4NounIdentificationPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each Aramaic noun form: (1) Gender — m. or f., '
            '(2) Number — s., pl., or du., '
            '(3) State — abs., det., or cstr., '
            '(4) Root / Lexical Form. All forms are in the absolute state.'
        )
        hdrs = ['#', 'Form', 'Gender', 'Number', 'State', 'Root / Lexical Form']
        cr = [0.04, 0.14, 0.10, 0.10, 0.10, 0.52]
        hc = [1]
        rows = [
            ['1',  'נוּר',       '', '', '', ''],
            ['2',  'חֵיוָה',    '', '', '', ''],
            ['3',  'רָזִין',     '', '', '', ''],
            ['4',  'עִדָּן',     '', '', '', ''],
            ['5',  'פְּשַׁר',    '', '', '', ''],
            ['6',  'חֵיוָן',    '', '', '', ''],
            ['7',  'זְמָן',      '', '', '', ''],
            ['8',  'טְעֵמִין',   '', '', '', ''],
            ['9',  'אַתּוּן',    '', '', '', ''],
            ['10', 'שָׁלְטָן',   '', '', '', ''],
            ['11', 'עִדָּנִין',  '', '', '', ''],
            ['12', 'גֹּב',       '', '', '', ''],
            ['13', 'פְּשָׁרִין', '', '', '', ''],
            ['14', 'חֲסַף',      '', '', '', ''],
            ['15', 'זְמָנִין',   '', '', '', ''],
            ['16', 'רָז',         '', '', '', ''],
            ['17', 'גּוֹא',       '', '', '', ''],
            ['18', 'שָׁלְטָנִין','', '', '', ''],
            ['19', 'טְעֵם',       '', '', '', ''],
            ['20', 'נוּרִין',     '', '', '', ''],
        ]
        ans = [
            ['1',  'נוּר',       'm.', 's.',  'abs.', 'נוּר — fire'],
            ['2',  'חֵיוָה',    'f.', 's.',  'abs.', 'חֵיוָה — animal, beast'],
            ['3',  'רָזִין',     'm.', 'pl.', 'abs.', 'רָז — secrets, mysteries'],
            ['4',  'עִדָּן',     'm.', 's.',  'abs.', 'עִדָּן — time, moment'],
            ['5',  'פְּשַׁר',    'm.', 's.',  'abs.', 'פְּשַׁר — interpretation'],
            ['6',  'חֵיוָן',    'f.', 'pl.', 'abs.', 'חֵיוָה — animals, beasts'],
            ['7',  'זְמָן',      'm.', 's.',  'abs.', 'זְמָן — time, a fixed time'],
            ['8',  'טְעֵמִין',   'm.', 'pl.', 'abs.', 'טְעֵם — commands, decrees'],
            ['9',  'אַתּוּן',    'm.', 's.',  'abs.', 'אַתּוּן — furnace'],
            ['10', 'שָׁלְטָן',   'm.', 's.',  'abs.', 'שָׁלְטָן — dominion'],
            ['11', 'עִדָּנִין',  'm.', 'pl.', 'abs.', 'עִדָּן — times, moments'],
            ['12', 'גֹּב',       'm.', 's.',  'abs.', 'גֹּב — pit, den'],
            ['13', 'פְּשָׁרִין', 'm.', 'pl.', 'abs.', 'פְּשַׁר — interpretations'],
            ['14', 'חֲסַף',      'm.', 's.',  'abs.', 'חֲסַף — clay, pottery'],
            ['15', 'זְמָנִין',   'm.', 'pl.', 'abs.', 'זְמָן — times'],
            ['16', 'רָז',         'm.', 's.',  'abs.', 'רָז — secret, mystery'],
            ['17', 'גּוֹא',       'm.', 's.',  'abs.', 'גּוֹא — midst, middle'],
            ['18', 'שָׁלְטָנִין','m.', 'pl.', 'abs.', 'שָׁלְטָן — dominions, powers'],
            ['19', 'טְעֵם',       'm.', 's.',  'abs.', 'טְעֵם — understanding, command'],
            ['20', 'נוּרִין',     'm.', 'pl.', 'abs.', 'נוּר — fires'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc)


def build_bba_ch4_noun_identification(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh4NounIdentificationPDF,
        'BBA Chapter 4 — Noun Identification Drill',
        'Absolute State · Gender · Number · Root Form',
        ['aramaic', 'bba', 'ch4', 'exercises', 'ch4-noun-identification'],
        'ch4-noun-identification.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBA Ch5 — Determined State Forms Drill
# ---------------------------------------------------------------------------

class BbaCh5DeterminedStateDrillPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'Each item gives a noun in one state (absolute or determined). '
            'Write it in the other state in the blank column. '
            'Direction is shown in the Notes column. '
            'Endings: ms ָא- · fs ָה-/ָתָא- · mp ִין-/ַיָּא- · fp ָן-/ָתָא-'
        )
        # Columns: #, Absolute Form, Determined Form, Gender/Number, Notes
        # heb_cols = [1, 2]; col 1 or 2 may be blank (input field) depending on direction
        # We'll use two separate tables split by direction, or just a single table
        # treating both Hebrew cols as display-only when pre-filled, input when blank.
        # Simpler: use separate rows, pre-fill given col via answer_rows mechanism.
        hdrs = ['#', 'Absolute Form', 'Determined Form', 'Gender/Number', 'Notes']
        cr = [0.04, 0.20, 0.20, 0.12, 0.44]
        hc = [1, 2]

        # For this exercise the "given" cell is pre-filled and "blank" cell is the input.
        # We encode: rows have the given value in its col, blank in the other.
        # answer_rows have both filled.
        rows = [
            ['1',  'אִילָן',    '',            'ms.', 'abs. → det.'],
            ['2',  '',           'נוּרָא',      'ms.', 'det. → abs.'],
            ['3',  'אֻמָּה',    '',            'fs.', 'abs. → det.'],
            ['4',  '',           'חֵיוְתָא',   'fs.', 'det. → abs.'],
            ['5',  'רָזִין',    '',            'mp.', 'abs. → det.'],
            ['6',  '',           'עִדָּנָא',   'ms.', 'det. → abs.'],
            ['7',  'מָאן',       '',            'ms.', 'abs. → det.'],
            ['8',  '',           'אֻמְּמָתָא', 'fp.', 'det. → abs.'],
            ['9',  'זְמָר',      '',            'ms.', 'abs. → det.'],
            ['10', '',           'רָזַיָּא',   'mp.', 'det. → abs.'],
            ['11', 'חֲמַר',     '',            'ms.', 'abs. → det.'],
            ['12', '',           'אִילָנַיָּא','mp.', 'det. → abs.'],
            ['13', 'חֵיוָן',   '',            'fp.', 'abs. → det.'],
            ['14', '',           'אֱסָרָא',    'ms.', 'det. → abs.'],
            ['15', 'יְקָר',      '',            'ms.', 'abs. → det.'],
            ['16', '',           'מָאנַיָּא',  'mp.', 'det. → abs.'],
            ['17', 'אֲתַר',     '',            'ms.', 'abs. → det.'],
            ['18', '',           'גִּשְׁמָא',  'ms.', 'det. → abs.'],
            ['19', 'זְמָנִין',  '',            'mp.', 'abs. → det.'],
            ['20', '',           'זְמָרַיָּא', 'mp.', 'det. → abs.'],
        ]
        ans = [
            ['1',  'אִילָן',    'אִילָנָא',    'ms.', 'Add ָא- — tree / the tree'],
            ['2',  'נוּר',       'נוּרָא',      'ms.', 'Remove ָא- — fire (Ch4)'],
            ['3',  'אֻמָּה',    'אֻמְּתָא',   'fs.', 'Replace ָה- with ָתָא-'],
            ['4',  'חֵיוָה',   'חֵיוְתָא',   'fs.', 'Remove ָתָא-, restore ָה- (Ch4)'],
            ['5',  'רָזִין',    'רָזַיָּא',    'mp.', 'Replace ִין- with ַיָּא- (Ch4)'],
            ['6',  'עִדָּן',    'עִדָּנָא',   'ms.', 'Remove ָא- (Ch4)'],
            ['7',  'מָאן',       'מָאנָא',      'ms.', 'Add ָא-'],
            ['8',  'אֻמְּמָן',  'אֻמְּמָתָא', 'fp.', 'Remove ָתָא-, restore ָן-'],
            ['9',  'זְמָר',      'זְמָרָא',     'ms.', 'Add ָא-'],
            ['10', 'רָזִין',    'רָזַיָּא',    'mp.', 'Remove ַיָּא-, restore ִין- (Ch4)'],
            ['11', 'חֲמַר',     'חַמְרָא',     'ms.', 'Add ָא-; vowel shift'],
            ['12', 'אִילָנִין', 'אִילָנַיָּא', 'mp.', 'Remove ַיָּא-, restore ִין-'],
            ['13', 'חֵיוָן',   'חֵיוָתָא',   'fp.', 'Replace ָן- with ָתָא- (Ch4)'],
            ['14', 'אֱסָר',     'אֱסָרָא',     'ms.', 'Remove ָא-'],
            ['15', 'יְקָר',      'יְקָרָא',     'ms.', 'Add ָא-'],
            ['16', 'מָאנִין',   'מָאנַיָּא',   'mp.', 'Remove ַיָּא-, restore ִין-'],
            ['17', 'אֲתַר',     'אֲתַרָא',     'ms.', 'Add ָא-'],
            ['18', 'גְּשֵׁם',   'גִּשְׁמָא',  'ms.', 'Remove ָא-; vowel shift'],
            ['19', 'זְמָנִין',  'זְמָנַיָּא',  'mp.', 'Replace ִין- with ַיָּא- (Ch4)'],
            ['20', 'זְמָרִין',  'זְמָרַיָּא',  'mp.', 'Remove ַיָּא-, restore ִין-'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc)


def build_bba_ch5_determined_state_drill(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh5DeterminedStateDrillPDF,
        'BBA Chapter 5 — Determined State Forms Drill',
        'Absolute ↔ Determined · All Four Gender/Number Patterns',
        ['aramaic', 'bba', 'ch5', 'exercises', 'ch5-determined-state-drill'],
        'ch5-determined-state-drill.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBA Ch6 — Construct Chain Drill
# ---------------------------------------------------------------------------

class BbaCh6ConstructChainDrillPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each item, write the construct form of the first noun and '
            'give the English translation of the complete construct chain. '
            'ms cstr. = abs. (unchanged) · fs: ָה- → ַת- · mp: ִין- → ֵי- · fp: ָן- → ָת-'
        )
        hdrs = ['#', 'Absolute Form', 'Construct Form', 'Genitive Noun', 'Translation']
        cr = [0.04, 0.18, 0.18, 0.18, 0.42]
        hc = [1, 2, 3]
        rows = [
            ['1',  'שָׁעָה (fs)',   '',  'חַד',          ''],
            ['2',  'מָרֵא (ms)',    '',  'מַלְכִין',     ''],
            ['3',  'פֻּם (ms)',     '',  'גֻּבָּא',      ''],
            ['4',  'רוּם (ms)',     '',  'שְׁמַיָּא',    ''],
            ['5',  'מַלְכָּה (fs)', '',  'מְדִינְתָא',   ''],
            ['6',  'מְדוֹר (ms)',   '',  'חֵיוְתָא',    ''],
            ['7',  'עֲנַף (ms)',    '',  'אִילָנָא',     ''],
            ['8',  'רָזִין (mp)',   '',  'אֱלָהָא',      ''],
            ['9',  'סוֹף (ms)',     '',  'כָּל־אַרְעָא', ''],
            ['10', 'חֵיוָה (fs)',   '',  'בְּרָא',       ''],
            ['11', 'פִּתְגָם (ms)', '',  'מַלְכָּא',     ''],
            ['12', 'מְלָכִין (mp)', '',  'אַרְעָא',      ''],
            ['13', 'רַעְיוֹן (ms)', '',  'לִבְבָהּ',     ''],
            ['14', 'שָׁלוּ (fs)',   '',  'מַלְכָּא',     ''],
            ['15', 'מְדִינָן (fp)', '',  'מַלְכוּתָא',   ''],
            ['16', 'נוּר (ms)',     '',  'אַתּוּנָא',    ''],
            ['17', 'אֻמָּה (fs)',   '',  'אַרְעָא',      ''],
            ['18', 'רָז (ms)',      '',  'מַלְכָּא',     ''],
            ['19', 'מְדוֹר (ms)',   '',  'שְׁמַיָּא',    ''],
            ['20', 'שָׁעָן (fp)',   '',  'יוֹמָא',       ''],
        ]
        ans = [
            ['1',  'שָׁעָה (fs)',   'שַׁעַת',   'חַד',          'one moment — fs ָה- → ַת-'],
            ['2',  'מָרֵא (ms)',    'מָרֵא',    'מַלְכִין',     'Lord of kings — ms cstr. = abs.'],
            ['3',  'פֻּם (ms)',     'פֻּם',     'גֻּבָּא',      'mouth of the den — ms cstr. = abs.'],
            ['4',  'רוּם (ms)',     'רוּם',     'שְׁמַיָּא',    'height of the heavens'],
            ['5',  'מַלְכָּה (fs)', 'מַלְכַּת', 'מְדִינְתָא',   'queen of the province — fs ָה- → ַת-'],
            ['6',  'מְדוֹר (ms)',   'מְדוֹר',   'חֵיוְתָא',    'dwelling of the beast'],
            ['7',  'עֲנַף (ms)',    'עֲנַף',    'אִילָנָא',     'branch of the tree'],
            ['8',  'רָזִין (mp)',   'רָזֵי',    'אֱלָהָא',      'secrets of God — mp ִין- → ֵי-'],
            ['9',  'סוֹף (ms)',     'סוֹף',     'כָּל־אַרְעָא', 'end of all the earth'],
            ['10', 'חֵיוָה (fs)',   'חֵיוַת',   'בְּרָא',       'beast of the field — fs ָה- → ַת-'],
            ['11', 'פִּתְגָם (ms)', 'פִּתְגָם', 'מַלְכָּא',     'decree of the king'],
            ['12', 'מְלָכִין (mp)', 'מַלְכֵי',  'אַרְעָא',      'kings of the earth — mp ִין- → ֵי-'],
            ['13', 'רַעְיוֹן (ms)', 'רַעְיוֹן', 'לִבְבָהּ',     'thought of her heart'],
            ['14', 'שָׁלוּ (fs)',   'שָׁלוּ',   'מַלְכָּא',     "king's negligence — lamed-waw: cstr. = abs."],
            ['15', 'מְדִינָן (fp)', 'מְדִינָת', 'מַלְכוּתָא',   'provinces of the kingdom — fp ָן- → ָת-'],
            ['16', 'נוּר (ms)',     'נוּר',     'אַתּוּנָא',    'fire of the furnace'],
            ['17', 'אֻמָּה (fs)',   'אֻמַּת',   'אַרְעָא',      'nation of the earth — fs ָה- → ַת-'],
            ['18', 'רָז (ms)',      'רָז',      'מַלְכָּא',     'secret of the king'],
            ['19', 'מְדוֹר (ms)',   'מְדוֹר',   'שְׁמַיָּא',    'dwelling of the heavens'],
            ['20', 'שָׁעָן (fp)',   'שָׁעָת',   'יוֹמָא',       'hours of the day — fp ָן- → ָת-'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc)


def build_bba_ch6_construct_chain_drill(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh6ConstructChainDrillPDF,
        'BBA Chapter 6 — Construct Chain Drill',
        'Construct State · All Four Gender/Number Patterns · Genitive Chains',
        ['aramaic', 'bba', 'ch6', 'exercises', 'ch6-construct-chain-drill'],
        'ch6-construct-chain-drill.pdf',
        out_dir,
    )


class BbaCh7PrepositionDrillPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each Aramaic phrase, identify the preposition or conjunction, give its gloss, '
            'identify the noun state, and translate the phrase.'
        )
        hdrs = ['#', 'Aramaic Phrase', 'Prep / Conj', 'Gloss', 'Noun State', 'Translation']
        cr = [0.04, 0.22, 0.14, 0.16, 0.14, 0.30]
        hc = [1]
        rows = [
            [1,  'קֳדָם מַלְכָּא',   '', '', '', ''],
            [2,  'מִן שְׁמַיָּא',    '', '', '', ''],
            [3,  'לְאַרְעָא',        '', '', '', ''],
            [4,  'בְּמַלְכוּתָא',   '', '', '', ''],
            [5,  'עַד עָלְמָא',      '', '', '', ''],
            [6,  'עַל אַנְפּוֹהִי', '', '', '', ''],
            [7,  'כְּאַבְנָא',       '', '', '', ''],
            [8,  'לָהֵן מַלְכָּא',  '', '', '', ''],
            [9,  'הֵן אִיתֵיכוֹן',  '', '', '', ''],
            [10, 'אַחֲרֵי דְנָה',   '', '', '', ''],
            [11, 'מִן גֻּבָּא',      '', '', '', ''],
            [12, 'בְּאַרְעָא',       '', '', '', ''],
            [13, 'כָּל-קֳבֵל דִּי', '', '', '', ''],
            [14, 'אַף אֲנָה',        '', '', '', ''],
            [15, 'עִם חַכִּימֵי',   '', '', '', ''],
            [16, 'לְמַלְכָּא',       '', '', '', ''],
            [17, 'עַד דִּי עָל',     '', '', '', ''],
            [18, 'אֲרוּ צְלֵם',      '', '', '', ''],
            [19, 'מִבָּבֶל',         '', '', '', ''],
            [20, 'בְּמַלְכוּ',       '', '', '', ''],
        ]
        ans = [
            [1,  'קֳדָם מַלְכָּא',   'קֳדָם',            'before, in the presence of', 'det. ms.',               'before the king'],
            [2,  'מִן שְׁמַיָּא',    'מִן',              'from',                       'det. mp.',               'from the heavens'],
            [3,  'לְאַרְעָא',        'לְ-',              'to, for',                    'det. fs.',               'to the earth'],
            [4,  'בְּמַלְכוּתָא',   'בְּ-',             'in, with, by',               'det. fs.',               'in the kingdom'],
            [5,  'עַד עָלְמָא',      'עַד',              'until, unto',                'det. ms.',               'unto eternity / forever'],
            [6,  'עַל אַנְפּוֹהִי', 'עַל',              'upon, on',                   'det. + 3ms suffix',      'upon his face'],
            [7,  'כְּאַבְנָא',       'כְּ-',             'as, like',                   'abs. ms.',               'like a stone'],
            [8,  'לָהֵן מַלְכָּא',  'לָהֵן',            'therefore, but',             '— (introduces address)', 'therefore, O king'],
            [9,  'הֵן אִיתֵיכוֹן',  'הֵן',              'if, whether',                '— (introduces clause)',  'if you are (ready)'],
            [10, 'אַחֲרֵי דְנָה',   'אַחֲרֵי',          'after, behind',              'dem. pronoun',           'after this'],
            [11, 'מִן גֻּבָּא',      'מִן',              'from, out of',               'det. ms.',               'out of the pit'],
            [12, 'בְּאַרְעָא',       'בְּ-',             'in, on',                     'det. fs.',               'in/on the earth'],
            [13, 'כָּל-קֳבֵל דִּי', 'כָּל-קֳבֵל דִּי',  'because, inasmuch as',       '— (introduces clause)',  'because / inasmuch as'],
            [14, 'אַף אֲנָה',        'אַף',              'also, even',                 '— (pronoun)',            'even I / I also'],
            [15, 'עִם חַכִּימֵי',   'עִם',              'with',                       'mp. cstr.',              'with the wise men of...'],
            [16, 'לְמַלְכָּא',       'לְ-',              'to, for',                    'det. ms.',               'to the king'],
            [17, 'עַד דִּי עָל',     'עַד דִּי',         'until (that)',               '— (introduces clause)',  'until he entered'],
            [18, 'אֲרוּ צְלֵם',      'אֲרוּ',            'behold, lo',                 'abs. ms.',               'behold, a statue'],
            [19, 'מִבָּבֶל',         'מִ- (מִן prefixed)', 'from',                     'proper noun',            'from Babylon'],
            [20, 'בְּמַלְכוּ',       'בְּ-',             'in',                         'abs. fs.',               'in a kingdom'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc)


def build_bba_ch7_preposition_drill(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh7PrepositionDrillPDF,
        'BBA Chapter 7 — Preposition Drill',
        'Conjunctions and Prepositions · Identification and Translation',
        ['aramaic', 'bba', 'ch7', 'exercises', 'ch7-preposition-drill'],
        'ch7-preposition-drill.pdf',
        out_dir,
    )


class BbaCh8SuffixDrillPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each form, identify the base form (noun or preposition), '
            'the pronominal suffix (person, gender, number), and give the English translation.'
        )
        hdrs = ['#', 'Form', 'Base Form', 'Suffix (PGN)', 'Translation']
        cr = [0.04, 0.18, 0.26, 0.16, 0.36]
        hc = [1]
        rows = [
            [1,  'מַלְכִּי',      '', '', ''],
            [2,  'אֱלָהֲנָא',    '', '', ''],
            [3,  'אַבוּהִי',      '', '', ''],
            [4,  'עַלַיְכוֹן',   '', '', ''],
            [5,  'בֵּיתֵהּ',      '', '', ''],
            [6,  'לְמַלְכָּה',   '', '', ''],
            [7,  'מִנִּי',        '', '', ''],
            [8,  'עַבְדֵיהוֹן',  '', '', ''],
            [9,  'אַנְפּוֹהִי',  '', '', ''],
            [10, 'יְדֵהּ',        '', '', ''],
            [11, 'עֲלֵיהוֹן',    '', '', ''],
            [12, 'לְהוֹן',        '', '', ''],
            [13, 'אֱלָהֵהּ',      '', '', ''],
            [14, 'מַלְכוּתִי',   '', '', ''],
            [15, 'עִמֵּהּ',        '', '', ''],
            [16, 'רֵאשֵׁהּ',      '', '', ''],
            [17, 'קֳדָמַי',       '', '', ''],
            [18, 'שְׁמֵהּ',        '', '', ''],
            [19, 'בָּנַיְכוֹן',  '', '', ''],
            [20, 'מִנְּהוֹן',     '', '', ''],
        ]
        ans = [
            [1,  'מַלְכִּי',      'מֶלֶךְ (king, ms)',          '1cs',  'my king'],
            [2,  'אֱלָהֲנָא',    'אֱלָה (God, ms)',             '1cp',  'our God'],
            [3,  'אַבוּהִי',      'אַב (father, ms)',             '3ms',  'his father'],
            [4,  'עַלַיְכוֹן',   'עַל (upon, prep)',             '2mp',  'upon you (mp)'],
            [5,  'בֵּיתֵהּ',      'בַּיִת (house, ms)',           '3ms',  'his house'],
            [6,  'לְמַלְכָּה',   'לְ- (to/for, prep)',           '3fs',  'to/for her'],
            [7,  'מִנִּי',        'מִן (from, prep)',             '1cs',  'from me'],
            [8,  'עַבְדֵיהוֹן',  'עֶבֶד (servant, ms pl)',       '3mp',  'their servants'],
            [9,  'אַנְפּוֹהִי',  'אַנְפִּין (face, mp)',         '3ms',  'his face'],
            [10, 'יְדֵהּ',        'יַד (hand, fs)',               '3ms',  'his hand'],
            [11, 'עֲלֵיהוֹן',    'עַל (upon, prep)',             '3mp',  'upon them'],
            [12, 'לְהוֹן',        'לְ- (to/for, prep)',           '3mp',  'to/for them'],
            [13, 'אֱלָהֵהּ',      'אֱלָה (God, ms)',             '3ms',  'his God'],
            [14, 'מַלְכוּתִי',   'מַלְכוּ (kingdom, fs)',        '1cs',  'my kingdom'],
            [15, 'עִמֵּהּ',        'עִם (with, prep)',            '3ms',  'with him'],
            [16, 'רֵאשֵׁהּ',      'רֵאשׁ (head, ms)',            '3ms',  'his head'],
            [17, 'קֳדָמַי',       'קֳדָם (before, prep)',         '1cs',  'before me'],
            [18, 'שְׁמֵהּ',        'שֵׁם (name, ms)',             '3ms',  'his name'],
            [19, 'בָּנַיְכוֹן',  'בַּר (son, pl. בָּנִין)',      '2mp',  'your (mp) sons'],
            [20, 'מִנְּהוֹן',     'מִן (from, prep)',             '3mp',  'from them'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc)


def build_bba_ch8_suffix_drill(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh8SuffixDrillPDF,
        'BBA Chapter 8 — Suffix Drill',
        'Pronominal Suffixes on Nouns and Prepositions',
        ['aramaic', 'bba', 'ch8', 'exercises', 'ch8-suffix-drill'],
        'ch8-suffix-drill.pdf',
        out_dir,
    )


class BbaCh9PronounDrillPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each form, identify the pronoun type, give the PGN where applicable, '
            'and give the English gloss or translation.'
        )
        hdrs = ['#', 'Form', 'Type', 'PGN', 'Gloss / Translation']
        cr = [0.04, 0.18, 0.26, 0.12, 0.40]
        hc = [1]
        rows = [
            [1,  'אֲנָה',       '', '', ''],
            [2,  'דְּנָה',      '', '', ''],
            [3,  'אִיתַי',      '', '', ''],
            [4,  'מַן',         '', '', ''],
            [5,  'הוּא',        '', '', ''],
            [6,  'כֹּל-אַרְעָא','', '', ''],
            [7,  'לֵית',        '', '', ''],
            [8,  'אִלֵּין',     '', '', ''],
            [9,  'מָה',         '', '', ''],
            [10, 'הִמּוֹ',       '', '', ''],
            [11, 'דָּא',         '', '', ''],
            [12, 'אֲנַחְנָה',   '', '', ''],
            [13, 'הָדֵין',      '', '', ''],
            [14, 'מִנְדַּעַם', '', '', ''],
            [15, 'הִיא',        '', '', ''],
            [16, 'אַנְתְּ',     '', '', ''],
            [17, 'כִּדְנָה',    '', '', ''],
            [18, 'מַן דִּי',    '', '', ''],
            [19, 'אִיתַיְכוֹן','', '', ''],
            [20, 'הָדָא',       '', '', ''],
        ]
        ans = [
            [1,  'אֲנָה',       'personal',                       '1cs',  'I'],
            [2,  'דְּנָה',      'demonstrative (near)',           'ms',   'this'],
            [3,  'אִיתַי',      'existential',                    '—',    'there is / there are'],
            [4,  'מַן',         'interrogative',                  '—',    'who?'],
            [5,  'הוּא',        'personal',                       '3ms',  'he, it'],
            [6,  'כֹּל-אַרְעָא','indefinite (כֹּל)',             '—',    'all the earth'],
            [7,  'לֵית',        'existential (negative)',         '—',    'there is not'],
            [8,  'אִלֵּין',     'demonstrative (near)',           'pl.',  'these'],
            [9,  'מָה',         'interrogative',                  '—',    'what?'],
            [10, 'הִמּוֹ',       'personal',                       '3mp',  'they'],
            [11, 'דָּא',         'demonstrative (near)',           'fs',   'this'],
            [12, 'אֲנַחְנָה',   'personal',                       '1cp',  'we'],
            [13, 'הָדֵין',      'demonstrative (near/far)',       'ms',   'this / that'],
            [14, 'מִנְדַּעַם', 'indefinite',                     '—',    'something, anything'],
            [15, 'הִיא',        'personal',                       '3fs',  'she, it'],
            [16, 'אַנְתְּ',     'personal',                       '2ms',  'you'],
            [17, 'כִּדְנָה',    'demonstrative idiom',            '—',    'thus, in this way'],
            [18, 'מַן דִּי',    'relative/interrogative compound','—',    'whoever, the one who'],
            [19, 'אִיתַיְכוֹן','existential + 2mp suffix',       '2mp',  'you are (there are you)'],
            [20, 'הָדָא',       'demonstrative (near/far)',       'fs',   'this / that'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc)


def build_bba_ch9_pronoun_drill(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh9PronounDrillPDF,
        'BBA Chapter 9 — Pronoun Drill',
        'Personal, Demonstrative, Interrogative, Existential, Indefinite',
        ['aramaic', 'bba', 'ch9', 'exercises', 'ch9-pronoun-drill'],
        'ch9-pronoun-drill.pdf',
        out_dir,
    )


class BbaCh10AdjectiveNumberDrillPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each form, identify whether it is an adjective or number, '
            'give the state/value and gender/number, and translate.'
        )
        hdrs = ['#', 'Form', 'Adj / Num', 'State / Value', 'G/N', 'Translation']
        cr = [0.04, 0.22, 0.14, 0.16, 0.10, 0.34]
        hc = [1]
        rows = [
            [1,  'רַב',                   '', '', '', ''],
            [2,  'שִׁבְעָה יוֹמִין',      '', '', '', ''],
            [3,  'חֵיוָה אָחֳרִי',        '', '', '', ''],
            [4,  'צְלֵם חַד',             '', '', '', ''],
            [5,  'מַלְכָּא רַבָּא',       '', '', '', ''],
            [6,  'קַדְמָיָא',             '', '', '', ''],
            [7,  'תְּרֵין שָׁנִין',       '', '', '', ''],
            [8,  'חַכִּימִין רַבְרְבִין', '', '', '', ''],
            [9,  'תְּלִיתַי',             '', '', '', ''],
            [10, 'אֱלָהּ קַדִּישׁ',       '', '', '', ''],
            [11, 'אַרְבְּעָה חֵיוָן',     '', '', '', ''],
            [12, 'שַׂגִּיאָה',            '', '', '', ''],
            [13, 'חֲמֵשׁ מְדִינָן',       '', '', '', ''],
            [14, 'מַלְכוּ אָחֳרִי',       '', '', '', ''],
            [15, 'שִׁבְעָה עִדָּנִין',    '', '', '', ''],
            [16, 'יְקַר עִלָּאָה',        '', '', '', ''],
            [17, 'תִּנְיָן',              '', '', '', ''],
            [18, 'תְּמָנֵה גֻּבְרִין',    '', '', '', ''],
            [19, 'אֱלָה שְׁמַיָּא חַיָּא','', '', '', ''],
            [20, 'חַד מִן',              '', '', '', ''],
        ]
        ans = [
            [1,  'רַב',                   'adjective',           'absolute',             'ms',      'great, large'],
            [2,  'שִׁבְעָה יוֹמִין',      'number',              'cardinal 7',           'ms noun', 'seven days'],
            [3,  'חֵיוָה אָחֳרִי',        'adjective',           'absolute',             'fs',      'another beast'],
            [4,  'צְלֵם חַד',             'number / indef. art.','cardinal 1',           'ms',      'one statue / a statue'],
            [5,  'מַלְכָּא רַבָּא',       'adjective',           'determined',           'ms',      'the great king'],
            [6,  'קַדְמָיָא',             'adjective (ordinal)', 'determined',           'ms',      'the first'],
            [7,  'תְּרֵין שָׁנִין',       'number',              'cardinal 2',           'fp noun', 'two years'],
            [8,  'חַכִּימִין רַבְרְבִין', 'adjective',           'absolute',             'mp',      'great/mighty wise men'],
            [9,  'תְּלִיתַי',             'adjective (ordinal)', 'absolute',             'ms',      'third'],
            [10, 'אֱלָהּ קַדִּישׁ',       'adjective',           'absolute',             'ms',      'a holy God'],
            [11, 'אַרְבְּעָה חֵיוָן',     'number',              'cardinal 4',           'fp noun', 'four beasts'],
            [12, 'שַׂגִּיאָה',            'adjective',           'determined',           'fs',      'the great/much (one)'],
            [13, 'חֲמֵשׁ מְדִינָן',       'number',              'cardinal 5',           'fp noun', 'five provinces'],
            [14, 'מַלְכוּ אָחֳרִי',       'adjective',           'absolute',             'fs',      'another kingdom'],
            [15, 'שִׁבְעָה עִדָּנִין',    'number',              'cardinal 7',           'mp noun', 'seven times / periods'],
            [16, 'יְקַר עִלָּאָה',        'adjective',           'determined',           'ms',      'the highest honor'],
            [17, 'תִּנְיָן',              'adjective (ordinal)', 'absolute',             'ms',      'second'],
            [18, 'תְּמָנֵה גֻּבְרִין',    'number',              'cardinal 8',           'mp noun', 'eight men'],
            [19, 'אֱלָה שְׁמַיָּא חַיָּא','adjective',           'absolute',             'ms',      'the living God of heaven'],
            [20, 'חַד מִן',              'number',              'cardinal 1 (partitive)','—',       'one of...'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc)


def build_bba_ch10_adjective_number_drill(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh10AdjectiveNumberDrillPDF,
        'BBA Chapter 10 — Adjective and Number Drill',
        'Adjective States and Agreement · Cardinal and Ordinal Numbers',
        ['aramaic', 'bba', 'ch10', 'exercises', 'ch10-adjective-number-drill'],
        'ch10-adjective-number-drill.pdf',
        out_dir,
    )


class BbaCh11ParticleDrillPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each phrase, identify the adverb or particle, give its category '
            '(time, place, manner, negation, discourse, causal/purpose), '
            'and give the English gloss or translation.'
        )
        hdrs = ['#', 'Aramaic Phrase', 'Adverb / Particle', 'Category', 'Gloss / Translation']
        cr = [0.04, 0.22, 0.16, 0.20, 0.38]
        hc = [1]
        rows = [
            [1,  'אֱדַיִן מַלְכָּא', '', '', ''],
            [2,  'לָא יָכְלִין',     '', '', ''],
            [3,  'כְּעַן אֱלָהּ',    '', '', ''],
            [4,  'תַּמָּה מֶלֶךְ',   '', '', ''],
            [5,  'יַתִּיר מִן',      '', '', ''],
            [6,  'כֵּן אֲמַר',       '', '', ''],
            [7,  'עֲדַיִן לָא',      '', '', ''],
            [8,  'הָכָא קָיְמִין',   '', '', ''],
            [9,  'לָהֵן מַלְכָּא',  '', '', ''],
            [10, 'אַף אֲנָה',        '', '', ''],
            [11, 'הֵן אִיתַי',       '', '', ''],
            [12, 'אֱדַיִן בֵּאדַיִן','', '', ''],
            [13, 'בְּדִיל דִּי',     '', '', ''],
            [14, 'אַל תִּדְחַל',     '', '', ''],
            [15, 'שַׂגִּיא טָב',     '', '', ''],
            [16, 'לָא עֲדַיִן',      '', '', ''],
            [17, 'אֲרוּ חֵיוָה',     '', '', ''],
            [18, 'כִּדְנָה אֲמַר',   '', '', ''],
            [19, 'כָּל-קֳבֵל דִּי', '', '', ''],
            [20, 'הֵן...הֵן',        '', '', ''],
        ]
        ans = [
            [1,  'אֱדַיִן מַלְכָּא', 'אֱדַיִן',          'time / discourse marker',       "then; at that time — 'then the king...'"],
            [2,  'לָא יָכְלִין',     'לָא',              'negation',                      "not — 'they are not able'"],
            [3,  'כְּעַן אֱלָהּ',    'כְּעַן',           'time (present)',                "now — 'now, O God...'"],
            [4,  'תַּמָּה מֶלֶךְ',   'תַּמָּה',          'place',                         "there — 'there (was) a king'"],
            [5,  'יַתִּיר מִן',      'יַתִּיר',          'manner',                        'exceedingly, more than'],
            [6,  'כֵּן אֲמַר',       'כֵּן',             'manner',                        "thus, so — 'thus he said'"],
            [7,  'עֲדַיִן לָא',      'עֲדַיִן',          'time (continuity)',             "still, yet — 'not yet'"],
            [8,  'הָכָא קָיְמִין',   'הָכָא',            'place',                         "here — 'standing here'"],
            [9,  'לָהֵן מַלְכָּא',  'לָהֵן',            'discourse (consequence/contrast)',"therefore / but — 'therefore, O king'"],
            [10, 'אַף אֲנָה',        'אַף',              'assertive',                     "also, even — 'even I / I also'"],
            [11, 'הֵן אִיתַי',       'הֵן',              'conditional/assertive',         "if; behold — 'if there is'"],
            [12, 'אֱדַיִן בֵּאדַיִן','אֱדַיִן',          'time / discourse marker',       'then — sequential / narrative marker'],
            [13, 'בְּדִיל דִּי',     'בְּדִיל דִּי',      'causal/purpose',                'in order that, for the sake of, because'],
            [14, 'אַל תִּדְחַל',     'אַל',              'negation (prohibitive)',        "do not — 'do not fear'"],
            [15, 'שַׂגִּיא טָב',     'שַׂגִּיא',         'manner (adverb from adj.)',     "greatly, very — 'very good'"],
            [16, 'לָא עֲדַיִן',      'לָא + עֲדַיִן',    'negation + time (idiom)',       'not yet'],
            [17, 'אֲרוּ חֵיוָה',     'אֲרוּ',            'discourse (presentative)',      "behold, lo — 'behold, a beast'"],
            [18, 'כִּדְנָה אֲמַר',   'כִּדְנָה',         'manner',                        "thus, in this manner — 'thus he said'"],
            [19, 'כָּל-קֳבֵל דִּי', 'כָּל-קֳבֵל דִּי',  'causal',                        'because, inasmuch as, therefore'],
            [20, 'הֵן...הֵן',        'הֵן...הֵן',         'conditional (correlative)',     'whether...or; if...then'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc)


def build_bba_ch11_particle_drill(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh11ParticleDrillPDF,
        'BBA Chapter 11 — Particle Drill',
        'Adverbs and Particles · Time, Place, Manner, Negation, Discourse',
        ['aramaic', 'bba', 'ch11', 'exercises', 'ch11-particle-drill'],
        'ch11-particle-drill.pdf',
        out_dir,
    )


# BBA Ch12 — Stem Identification Drill
class BbaCh12VerbIntroDrillPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each underlined verb from Daniel or Ezra, identify the stem '
            '(Peal, Peil, Ithpeel, Pael, Ithpaal, Haphel, Hophal, Shaph\'el, or Ithhaph\'al), '
            'isolate the three-letter root (3ms Peal perfect form), '
            'and give an English gloss of the verb as it appears in the verse.'
        )
        hdrs = ['#', 'Aramaic Clause', 'Ref', 'Stem', 'Root', 'Gloss']
        cr = [0.04, 0.30, 0.09, 0.17, 0.10, 0.30]
        hc = [1]
        rows = [
            [1,  'אֱדַיִן דָּנִיֵּאל לְבֵיתֵהּ אֲזַל',              'Dan 2:17', '', '', ''],
            [2,  'וּמִלְּתָא כְּתַב מַלְכָּא',                                                        'Dan 6:26', '', '', ''],
            [3,  'אֱדַיִן נְבוּכַדְנֶצַּר נְפַל עַל-אַנְפּוֹהִי',  'Dan 2:46', '', '', ''],
            [4,  'אֱדַיִן אֲמַר מַלְכָּא לְאַרְיוֹךְ',            'Dan 2:24', '', '', ''],
            [5,  'כְדִי הֲוָה דָנִיֵּאל מִתְחַנַּן',                      'Dan 6:12', '', '', ''],
            [6,  'וּמַלְכָּא שְׁלַח כְנֵמָא',                                                          'Ezra 5:17', '', '', ''],
            [7,  'יְהַבְתְּ לִי חָכְמְתָא וּגְבוּרְתָא',  'Dan 2:23', '', '', ''],
            [8,  'דִי כָל-עַמְמַיָּא ... יִפְּלוּן',                                        'Dan 3:7',  '', '', ''],
            [9,  'וְדָנִיֵּאל עֲבַד קַרְצֵי לְשַׁדְרַךְ',  'Dan 3:12', '', '', ''],
            [10, 'מַלְכוּתָא עֲלָךְ קָמַת',                                                                      'Dan 4:33', '', '', ''],
            [11, 'כְעַן הוֹדַעְתַּנִי דִי בְעֵינָא מִנָּךְ',  'Dan 2:23', '', '', ''],
            [12, 'דִי-יְהַב מַלְכָּא הֲקִים',                                                              'Dan 3:2',  '', '', ''],
            [13, 'בַּיְתָה דְנָה הִתְבְנִי',                                                              'Ezra 5:16', '', '', ''],
            [14, 'כָל-חֲבוּל לָא הִשְׁתְְּכַח בֵּהּ',                   'Dan 6:23', '', '', ''],
        ]
        ans = [
            [1,  'אֱדַיִן דָּנִיֵּאל לְבֵיתֵהּ אֲזַל',              'Dan 2:17', 'Peal',         'אזל', 'he went'],
            [2,  'וּמִלְּתָא כְּתַב מַלְכָּא',                                                        'Dan 6:26', 'Peal',         'כתב', 'the king wrote'],
            [3,  'אֱדַיִן נְבוּכַדְנֶצַּר נְפַל עַל-אַנְפּוֹהִי',  'Dan 2:46', 'Peal',         'נפל', 'he fell'],
            [4,  'אֱדַיִן אֲמַר מַלְכָּא לְאַרְיוֹךְ',            'Dan 2:24', 'Peal',         'אמר', 'the king said'],
            [5,  'כְדִי הֲוָה דָנִיֵּאל מִתְחַנַּן',                      'Dan 6:12', 'Peal',         'הוה', 'when Daniel was (praying)'],
            [6,  'וּמַלְכָּא שְׁלַח כְנֵמָא',                                                          'Ezra 5:17', 'Peal',        'שׁלח', 'the king sent'],
            [7,  'יְהַבְתְּ לִי חָכְמְתָא וּגְבוּרְתָא',  'Dan 2:23', 'Peal (2ms pf)', 'יהב', 'you gave'],
            [8,  'דִי כָל-עַמְמַיָּא ... יִפְּלוּן',                                        'Dan 3:7',  'Peal (3mp ipf)', 'נפל', 'they will fall'],
            [9,  'וְדָנִיֵּאל עֲבַד קַרְצֵי לְשַׁדְרַךְ',  'Dan 3:12', 'Peal',         'עבד', 'Daniel did / made'],
            [10, 'מַלְכוּתָא עֲלָךְ קָמַת',                                                                      'Dan 4:33', 'Peal (3fs pf)', 'קום', 'the kingdom stood / was restored'],
            [11, 'כְעַן הוֹדַעְתַּנִי דִי בְעֵינָא מִנָּךְ',  'Dan 2:23', 'Haphel (2ms+suf)', 'ידע', 'you made known to me'],
            [12, 'דִי-יְהַב מַלְכָּא הֲקִים',                                                              'Dan 3:2',  'Haphel (3ms pf)', 'קום', 'he/king set up, erected'],
            [13, 'בַּיְתָה דְנָה הִתְבְנִי',                                                              'Ezra 5:16', 'Ithpeel (3ms pf)', 'בנה', 'this house was built'],
            [14, 'כָל-חֲבוּל לָא הִשְׁתְְּכַח בֵּהּ',                   'Dan 6:23', 'Ithpeel (3ms pf)', 'שׁכח', 'no harm was found on him'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc,
                                        section_title='Verb Identification — Items 1–14')


def build_bba_ch12_verb_intro_drill(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh12VerbIntroDrillPDF,
        'BBA Chapter 12 — Stem Identification Drill',
        'Introduction to Aramaic Verbs · Peal · Haphel · Ithpeel',
        ['aramaic', 'bba', 'ch12', 'exercises', 'ch12-verb-intro-drill'],
        'ch12-verb-intro-drill.pdf',
        out_dir,
    )


class BbaCh13PealPerfectDrillPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each numbered Peal perfect form drawn from Daniel or Ezra, '
            'identify the Root (three root consonants), '
            'the PGN (person, gender, number), '
            'and provide an English translation. '
            'All forms are Peal (G stem) perfect. '
            'Verb types include strong roots and the major weak classes: '
            'I-aleph, I-nun, hollow (II-waw), III-he, III-aleph, and I-yod.'
        )
        hdrs = ['#', 'Form', 'Root', 'PGN', 'Translation']
        cr = [0.04, 0.16, 0.18, 0.18, 0.44]
        hc = [1]
        rows = [
            [1,  'אֲמַר',       '', '', ''],
            [2,  'כְּתַבוּ',     '', '', ''],
            [3,  'שְׁלַחְתְּ',   '', '', ''],
            [4,  'יְהַבְנָא',    '', '', ''],
            [5,  'עֲבַד',        '', '', ''],
            [6,  'שְׁמַעְתִּי',  '', '', ''],
            [7,  'נְפַלַת',     '', '', ''],
            [8,  'קָם',          '', '', ''],
            [9,  'הֲוָת',        '', '', ''],
            [10, 'זְכַרְתְּ',    '', '', ''],
            [11, 'שְׁנֵא',       '', '', ''],
            [12, 'סְגִדוּ',      '', '', ''],
            [13, 'בְּנָה',       '', '', ''],
            [14, 'אֲמַרוּ',      '', '', ''],
            [15, 'כְּתָבֵת',     '', '', ''],
            [16, 'יְהַבְתְּ',    '', '', ''],
            [17, 'הֲוֵינָא',     '', '', ''],
            [18, 'עֲבַדְתּוּן',  '', '', ''],
            [19, 'קָמַת',        '', '', ''],
            [20, 'בְּנַיְנָא',   '', '', ''],
        ]
        ans = [
            [1,  'אֲמַר',       'אמר',  '3ms',  'he said'],
            [2,  'כְּתַבוּ',     'כתב',  '3mp',  'they (m) wrote'],
            [3,  'שְׁלַחְתְּ',   'שׁלח', '2ms',  'you (ms) sent'],
            [4,  'יְהַבְנָא',    'יהב',  '1cp',  'we gave'],
            [5,  'עֲבַד',        'עבד',  '3ms',  'he did / made'],
            [6,  'שְׁמַעְתִּי',  'שׁמע', '2fs',  'you (fs) heard'],
            [7,  'נְפַלַת',     'נפל',  '3fs',  'she/it fell'],
            [8,  'קָם',          'קום',  '3ms',  'he arose / stood up'],
            [9,  'הֲוָת',        'הוה',  '3fs',  'she/it was'],
            [10, 'זְכַרְתְּ',    'זכר',  '2ms',  'you (ms) remembered'],
            [11, 'שְׁנֵא',       'שׁנא', '3ms',  'it changed / was different'],
            [12, 'סְגִדוּ',      'סגד',  '3mp',  'they (m) bowed down'],
            [13, 'בְּנָה',       'בנה',  '3ms',  'he built'],
            [14, 'אֲמַרוּ',      'אמר',  '3mp',  'they (m) said'],
            [15, 'כְּתָבֵת',     'כתב',  '1cs',  'I wrote'],
            [16, 'יְהַבְתְּ',    'יהב',  '2ms',  'you (ms) gave'],
            [17, 'הֲוֵינָא',     'הוה',  '1cp',  'we were'],
            [18, 'עֲבַדְתּוּן',  'עבד',  '2mp',  'you (mp) did / made'],
            [19, 'קָמַת',        'קום',  '3fs',  'she/it arose'],
            [20, 'בְּנַיְנָא',   'בנה',  '1cp',  'we built'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc,
                                        section_title='Peal Perfect Parsing — Items 1–20')


def build_bba_ch13_peal_perfect_drill(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh13PealPerfectDrillPDF,
        'BBA Chapter 13 — Peal Perfect Parsing Drill',
        'Peal Perfect · Strong and Weak Roots · Daniel and Ezra',
        ['aramaic', 'bba', 'ch13', 'exercises', 'ch13-peal-perfect-drill'],
        'ch13-peal-perfect-drill.pdf',
        out_dir,
    )


class BbaCh14PealImperfectDrillPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each numbered Peal imperfect form drawn from Daniel or Ezra, '
            'identify the Root (three root consonants, Peal perfect 3ms form), '
            'the PGN (person, gender, number), '
            'and provide an English translation. '
            'All forms are Peal (G stem) imperfect. '
            'Verb types include strong roots and the major weak classes: '
            'I-aleph, I-nun, hollow (II-waw), III-he, and the suppletive imperfect of יהב.'
        )
        hdrs = ['#', 'Form', 'Root', 'PGN', 'Translation']
        cr = [0.04, 0.16, 0.18, 0.18, 0.44]
        hc = [1]
        rows = [
            [1,  'יִכְתֻּב',      '', '', ''],
            [2,  'יֵאמַר',        '', '', ''],
            [3,  'יְקוּם',         '', '', ''],
            [4,  'יִפַּל',         '', '', ''],
            [5,  'יֶהֱוֵא',        '', '', ''],
            [6,  'יִשְׁלַח',       '', '', ''],
            [7,  'תִּקְטֻל',       '', '', ''],
            [8,  'יַעְבְּדוּן',    '', '', ''],
            [9,  'תִּבְנֵא',       '', '', ''],
            [10, 'יִסְגְּדוּן',    '', '', ''],
            [11, 'נִזְכֻּר',       '', '', ''],
            [12, 'יִנְתֵּן',       '', '', ''],
            [13, 'יִקְטֻל',        '', '', ''],
            [14, 'יִשְׁמַע',       '', '', ''],
            [15, 'אֶכְתֻּב',       '', '', ''],
            [16, 'תִּכְתְּבוּן',   '', '', ''],
            [17, 'תִּכְתְּבִין',   '', '', ''],
            [18, 'יִכְתְּבָן',     '', '', ''],
            [19, 'תֵּאמְרוּן',     '', '', ''],
            [20, 'נֶהֱוֵא',        '', '', ''],
        ]
        ans = [
            [1,  'יִכְתֻּב',      'כתב',  '3ms',      'he will write'],
            [2,  'יֵאמַר',        'אמר',  '3ms',      'he will say'],
            [3,  'יְקוּם',         'קום',  '3ms',      'he will arise'],
            [4,  'יִפַּל',         'נפל',  '3ms',      'he will fall'],
            [5,  'יֶהֱוֵא',        'הוה',  '3ms',      'it will be'],
            [6,  'יִשְׁלַח',       'שׁלח', '3ms',      'he will send'],
            [7,  'תִּקְטֻל',       'קטל',  '3fs / 2ms', 'she will kill / you (ms) will kill'],
            [8,  'יַעְבְּדוּן',    'עבד',  '3mp',      'they (m) will serve / do'],
            [9,  'תִּבְנֵא',       'בנה',  '3fs / 2ms', 'she/it will build / you (ms) will build'],
            [10, 'יִסְגְּדוּן',    'סגד',  '3mp',      'they (m) will bow down'],
            [11, 'נִזְכֻּר',       'זכר',  '1cp',      'we will remember'],
            [12, 'יִנְתֵּן',       'יהב',  '3ms',      'he will give (suppletive)'],
            [13, 'יִקְטֻל',        'קטל',  '3ms',      'he will kill'],
            [14, 'יִשְׁמַע',       'שׁמע', '3ms',      'he will hear'],
            [15, 'אֶכְתֻּב',       'כתב',  '1cs',      'I will write'],
            [16, 'תִּכְתְּבוּן',   'כתב',  '2mp',      'you (mp) will write'],
            [17, 'תִּכְתְּבִין',   'כתב',  '2fs',      'you (fs) will write'],
            [18, 'יִכְתְּבָן',     'כתב',  '3fp',      'they (f) will write'],
            [19, 'תֵּאמְרוּן',     'אמר',  '2mp',      'you (mp) will say'],
            [20, 'נֶהֱוֵא',        'הוה',  '1cp',      'we will be'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc,
                                        section_title='Peal Imperfect Parsing — Items 1–20')


def build_bba_ch14_peal_imperfect_drill(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh14PealImperfectDrillPDF,
        'BBA Chapter 14 — Peal Imperfect Parsing Drill',
        'Peal Imperfect · Strong and Weak Roots · Daniel and Ezra',
        ['aramaic', 'bba', 'ch14', 'exercises', 'ch14-peal-imperfect-drill'],
        'ch14-peal-imperfect-drill.pdf',
        out_dir,
    )


class BbaCh15PealImperativeDrillPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each numbered Peal imperative form drawn from Daniel or Ezra, '
            'identify the Root (three root consonants, Peal perfect 3ms form), '
            'the PGN (person, gender, number), '
            'and provide an English translation as a command ("Do X!"). '
            'All forms are Peal (G stem) imperative (2nd person only). '
            'Verb types include strong roots and the major weak classes: '
            'I-aleph, I-ayin, hollow (II-waw), III-he, and I-yod. '
            'Items 17-20 are negative imperative constructions (al + jussive; la + imperfect).'
        )
        hdrs = ['#', 'Form', 'Root', 'PGN', 'Translation']
        cr = [0.04, 0.18, 0.16, 0.18, 0.44]
        hc = [1]
        rows = [
            [1,  'קוּם',              '', '', ''],
            [2,  'אֱמַר',              '', '', ''],
            [3,  'כְּתֻב',             '', '', ''],
            [4,  'שְׁלַח',             '', '', ''],
            [5,  'עֲבֵד',              '', '', ''],
            [6,  'שְׁמַע',             '', '', ''],
            [7,  'הַב',                '', '', ''],
            [8,  'פְּרֻק',             '', '', ''],
            [9,  'בְּנוֹ',             '', '', ''],
            [10, 'הָבוּ',              '', '', ''],
            [11, 'אֱמַרוּ',            '', '', ''],
            [12, 'שְׁמַעוּ',           '', '', ''],
            [13, 'כְּתֻבִי',           '', '', ''],
            [14, 'שִׁלְחוּ',           '', '', ''],
            [15, 'קוּמוּ',             '', '', ''],
            [16, 'עֲבֵדוּ',            '', '', ''],
            [17, 'אַל תִּסְגֻּד',      '', '', ''],
            [18, 'לָא תִּכְתֻּב',      '', '', ''],
            [19, 'אַל תֵּאמְרוּן',     '', '', ''],
            [20, 'לָא תִּסְגְּדוּן',   '', '', ''],
        ]
        ans = [
            [1,  'קוּם',              'קום',   '2ms',      'Arise! / Stand up!'],
            [2,  'אֱמַר',              'אמר',   '2ms',      'Say! / Tell!'],
            [3,  'כְּתֻב',             'כתב',   '2ms',      'Write!'],
            [4,  'שְׁלַח',             'שׁלח',  '2ms',      'Send!'],
            [5,  'עֲבֵד',              'עבד',   '2ms',      'Do! / Serve! / Make!'],
            [6,  'שְׁמַע',             'שׁמע',  '2ms',      'Hear! / Listen!'],
            [7,  'הַב',                'יהב',   '2ms',      'Give!'],
            [8,  'פְּרֻק',             'פרק',   '2ms',      'Deliver! / Atone!'],
            [9,  'בְּנוֹ',             'בנה',   '2mp',      'Build! (to men)'],
            [10, 'הָבוּ',              'יהב',   '2mp',      'Give! (to men)'],
            [11, 'אֱמַרוּ',            'אמר',   '2mp',      'Say! (to men)'],
            [12, 'שְׁמַעוּ',           'שׁמע',  '2mp',      'Hear! (to men)'],
            [13, 'כְּתֻבִי',           'כתב',   '2fs',      'Write! (to a woman)'],
            [14, 'שִׁלְחוּ',           'שׁלח',  '2mp',      'Send! (to men)'],
            [15, 'קוּמוּ',             'קום',   '2mp',      'Arise! (to men)'],
            [16, 'עֲבֵדוּ',            'עבד',   '2mp',      'Do! / Serve! (to men)'],
            [17, 'אַל תִּסְגֻּד',      'סגד',   '2ms neg',  'Do not bow down! (urgent)'],
            [18, 'לָא תִּכְתֻּב',      'כתב',   '2ms neg',  'You shall not write (general)'],
            [19, 'אַל תֵּאמְרוּן',     'אמר',   '2mp neg',  'Do not say! (urgent, to men)'],
            [20, 'לָא תִּסְגְּדוּן',   'סגד',   '2mp neg',  'You shall not bow down (general)'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc,
                                        section_title='Peal Imperative Parsing — Items 1–20')


def build_bba_ch15_peal_imperative_drill(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh15PealImperativeDrillPDF,
        'BBA Chapter 15 — Peal Imperative Parsing Drill',
        'Peal Imperative · Strong and Weak Roots · Daniel and Ezra',
        ['aramaic', 'bba', 'ch15', 'exercises', 'ch15-peal-imperative-drill'],
        'ch15-peal-imperative-drill.pdf',
        out_dir,
    )


# BBA Ch16 — Peal Infinitive Construct Drill
class BbaCh16PealInfinitiveDrillPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each numbered infinitive construct form drawn from Daniel or Ezra, '
            'identify the Root (three root consonants, Peal perfect 3ms form), '
            'the Prefix and its meaning '
            '(le = purpose/complement "to"; ke = temporal "when/upon"; none = bare verbal noun), '
            'and provide an English translation of the full infinitive phrase. '
            'Forms cover strong roots, I-nun (nun retained), I-aleph (tsere prefix), '
            'hollow II-waw (tsere + yod prefix), III-he (aleph-tsere ending), '
            'and I-ayin (seghol prefix). '
            'Items 18-20 are Haphel infinitives (le-ha- prefix) — a preview of Ch21.'
        )
        hdrs = ['#', 'Form', 'Root', 'Prefix', 'Translation']
        cr = [0.04, 0.17, 0.14, 0.28, 0.37]
        hc = [1]
        rows = [
            [1,  'לְמִכְתַּב',    '', '', ''],
            [2,  'לְמֵאמַר',     '', '', ''],
            [3,  'לְמֵיקַם',     '', '', ''],
            [4,  'לְמִנְפַּל',    '', '', ''],
            [5,  'כְּמִשְׁמַע',   '', '', ''],
            [6,  'לְמֶעְבַּד',    '', '', ''],
            [7,  'לְמִנְתַּן',    '', '', ''],
            [8,  'לְמִבְנֵא',     '', '', ''],
            [9,  'כְּמֵיקַם',     '', '', ''],
            [10, 'לְמִסְגַּד',    '', '', ''],
            [11, 'לְמִקְרַב',     '', '', ''],
            [12, 'מִשְׁמַע',     '', '', ''],
            [13, 'מִכְתַּב',     '', '', ''],
            [14, 'לְמִשְׁלַח',    '', '', ''],
            [15, 'כְּמִכְתַּב',   '', '', ''],
            [16, 'לְמִנְפַּל',    '', '', ''],
            [17, 'מֶעְבַּד',      '', '', ''],
            [18, 'לְהַחֲוָיָה',   '', '', ''],
            [19, 'לְהַשְׁנָיָה',  '', '', ''],
            [20, 'לְהוֹדָעָה',   '', '', ''],
        ]
        ans = [
            [1,  'לְמִכְתַּב',    'כתב',  'לְ — purpose/complement',         'to write / in order to write'],
            [2,  'לְמֵאמַר',     'אמר',  'לְ — purpose; מֵ = I-aleph',       'to say / in order to say'],
            [3,  'לְמֵיקַם',     'קום',  'לְ — purpose; מֵי = hollow',        'to arise / to stand up'],
            [4,  'לְמִנְפַּל',    'נפל',  'לְ — purpose; nun retained (I-nun)', 'to fall (down)'],
            [5,  'כְּמִשְׁמַע',   'שׁמע', 'כְּ — temporal ("when/upon")',       'when hearing / upon hearing'],
            [6,  'לְמֶעְבַּד',    'עבד',  'לְ — purpose; מֶ = seghol (I-ayin)', 'to do / to make / to serve'],
            [7,  'לְמִנְתַּן',    'נתן',  'לְ — purpose; nun retained (I-nun)', 'to give'],
            [8,  'לְמִבְנֵא',     'בנה',  'לְ — purpose; ֵא ending = III-he',  'to build'],
            [9,  'כְּמֵיקַם',     'קום',  'כְּ — temporal; מֵי = hollow',       'when arising / upon standing'],
            [10, 'לְמִסְגַּד',    'סגד',  'לְ — purpose/complement',           'to bow down / to worship'],
            [11, 'לְמִקְרַב',     'קרב',  'לְ — purpose/complement',           'to approach / to draw near'],
            [12, 'מִשְׁמַע',     'שׁמע', 'none — bare infinitive',             'hearing / the act of hearing'],
            [13, 'מִכְתַּב',     'כתב',  'none — bare infinitive',             'writing / the act of writing'],
            [14, 'לְמִשְׁלַח',    'שׁלח', 'לְ — purpose/complement',           'to send'],
            [15, 'כְּמִכְתַּב',   'כתב',  'כְּ — temporal ("when/upon")',       'when writing / upon writing'],
            [16, 'לְמִנְפַּל',    'נפל',  'לְ — purpose; nun retained (I-nun)', 'to fall (down)'],
            [17, 'מֶעְבַּד',      'עבד',  'none — bare; מֶ = seghol (I-ayin)', 'doing / making / the act of serving'],
            [18, 'לְהַחֲוָיָה',   'חוה',  'לְהַ — Haphel inf. ("to show")',    'to show / to declare (Haphel)'],
            [19, 'לְהַשְׁנָיָה',  'שׁנה', 'לְהַ — Haphel inf. ("to change")', 'to change / to alter (Haphel)'],
            [20, 'לְהוֹדָעָה',   'ידע',  'לְהוֹ — Haphel inf. ("to inform")', 'to make known / to inform (Haphel)'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc,
                                        section_title='Peal Infinitive Construct Drill — Items 1–20')


def build_bba_ch16_peal_infinitive_drill(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh16PealInfinitiveDrillPDF,
        'BBA Chapter 16 — Peal Infinitive Construct Drill',
        'Peal Infinitive Construct · Strong and Weak Roots · Daniel and Ezra',
        ['aramaic', 'bba', 'ch16', 'exercises', 'ch16-peal-infinitive-drill'],
        'ch16-peal-infinitive-drill.pdf',
        out_dir,
    )


class BbaCh17PealParticipleDrillPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each numbered Peal participle form drawn from Daniel or Ezra, '
            'identify whether it is Active (qatal pattern: qamets on R1, tsere on R2) '
            'or Passive (qtil pattern: vocal shewa on R1, hireq-yod on R2), '
            'give the Root (three root consonants, Peal perfect 3ms form), '
            'the G/N (gender and number: ms / fs / mp / fp), '
            'and provide an English translation. '
            'Forms cover strong roots and the major weak classes: '
            'hollow II-waw (qaam pattern), III-he (final he/aleph mater), '
            'I-nun (nun retained), and I-aleph/guttural. '
            'Both absolute and determined state forms are included.'
        )
        hdrs = ['#', 'Form', 'Act/Pass', 'Root', 'G/N', 'Translation']
        cr = [0.04, 0.15, 0.12, 0.12, 0.08, 0.49]
        hc = [1]
        rows = [
            [1,  'כָּתֵב',       '', '', '', ''],
            [2,  'כְּתִיב',      '', '', '', ''],
            [3,  'כָּתְבִין',    '', '', '', ''],
            [4,  'כְּתִיבִין',   '', '', '', ''],
            [5,  'קָאֵם',        '', '', '', ''],
            [6,  'שְׁלִיח',      '', '', '', ''],
            [7,  'כָּתְבָן',     '', '', '', ''],
            [8,  'אֲסִיר',       '', '', '', ''],
            [9,  'חָזֵה',        '', '', '', ''],
            [10, 'רְשִׁים',      '', '', '', ''],
            [11, 'כָּתְבָה',     '', '', '', ''],
            [12, 'כְּתִיבָא',    '', '', '', ''],
            [13, 'שָׁמֵעַ',      '', '', '', ''],
            [14, 'שְׁלִיחִין',   '', '', '', ''],
            [15, 'עָבְדִין',     '', '', '', ''],
            [16, 'נָפֵל',        '', '', '', ''],
            [17, 'אֲסִירָא',     '', '', '', ''],
            [18, 'כָּתְבַיָּא',  '', '', '', ''],
            [19, 'בָּנֵא',       '', '', '', ''],
            [20, 'יְהִיב',       '', '', '', ''],
        ]
        ans = [
            [1,  'כָּתֵב',       'Active',  'כתב',  'ms', 'writing / one who writes'],
            [2,  'כְּתִיב',      'Passive', 'כתב',  'ms', 'written / it is written'],
            [3,  'כָּתְבִין',    'Active',  'כתב',  'mp', 'writing (mp) / ones who write'],
            [4,  'כְּתִיבִין',   'Passive', 'כתב',  'mp', 'written (mp) / those who are written'],
            [5,  'קָאֵם',        'Active',  'קום',  'ms', 'standing / one who stands (hollow)'],
            [6,  'שְׁלִיח',      'Passive', 'שׁלח', 'ms', 'sent / one who has been sent'],
            [7,  'כָּתְבָן',     'Active',  'כתב',  'fp', 'writing (fp) / those (f) who write'],
            [8,  'אֲסִיר',       'Passive', 'אסר',  'ms', 'bound / imprisoned'],
            [9,  'חָזֵה',        'Active',  'חזה',  'ms', 'seeing / one who sees (III-he)'],
            [10, 'רְשִׁים',      'Passive', 'רשׁם', 'ms', 'inscribed / signed / registered'],
            [11, 'כָּתְבָה',     'Active',  'כתב',  'fs', 'writing (fs) / one (f) who writes'],
            [12, 'כְּתִיבָא',    'Passive', 'כתב',  'ms', 'the written one (ms det.)'],
            [13, 'שָׁמֵעַ',      'Active',  'שׁמע', 'ms', 'hearing / one who hears'],
            [14, 'שְׁלִיחִין',   'Passive', 'שׁלח', 'mp', 'sent ones (mp) / envoys'],
            [15, 'עָבְדִין',     'Active',  'עבד',  'mp', 'doing / serving (mp)'],
            [16, 'נָפֵל',        'Active',  'נפל',  'ms', 'falling / one who falls (I-nun)'],
            [17, 'אֲסִירָא',     'Passive', 'אסר',  'ms', 'the prisoner (ms det.)'],
            [18, 'כָּתְבַיָּא',  'Active',  'כתב',  'mp', 'the writers (mp det.)'],
            [19, 'בָּנֵא',       'Active',  'בנה',  'ms', 'building / one who builds (III-he)'],
            [20, 'יְהִיב',       'Passive', 'יהב',  'ms', 'given / that which is given'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc,
                                        section_title='Peal Participle Drill — Items 1–20')


def build_bba_ch17_peal_participle_drill(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh17PealParticipleDrillPDF,
        'BBA Chapter 17 — Peal Participle Drill',
        'Peal Active and Passive Participles · Strong and Weak Roots · Daniel and Ezra',
        ['aramaic', 'bba', 'ch17', 'exercises', 'ch17-peal-participle-drill'],
        'ch17-peal-participle-drill.pdf',
        out_dir,
    )


# BBA Ch18 — Peil and Ithpeel Stem Drill


class BbaCh18PassiveStemsDrillPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each numbered verb form drawn from Daniel or Ezra, '
            'identify the Stem (Peil = simple passive of Peal, or Ithpeel = reflexive/passive of Peal), '
            'the Conjugation (Perfect / Imperfect / Participle), '
            'the Root (three root consonants, Peal perfect 3ms form), '
            'and provide an English translation. '
            'Peil perfect: hireq-yod on R2 (qetil pattern). '
            'Ithpeel perfect: hit- or it- prefix. '
            'Ithpeel imperfect: yit- before R1. '
            'Ithpeel participle: mit- prefix. '
            'Metathesis: sibilant R1 switches with taw (histt- / yisht-).'
        )
        hdrs = ['#', 'Form', 'Stem', 'Conjugation', 'Root', 'Translation']
        cr = [0.04, 0.14, 0.10, 0.16, 0.10, 0.46]
        hc = [1]
        rows = [
            [1,  'רְמִי',             '', '', '', ''],
            [2,  'אִתְכְּנִישׁ',      '', '', '', ''],
            [3,  'יִתְנְסַח',         '', '', '', ''],
            [4,  'שְׁבִיק',           '', '', '', ''],
            [5,  'הִשְׁתְּכַח',       '', '', '', ''],
            [6,  'כְּתִיב',           '', '', '', ''],
            [7,  'יִתְבְּנֵא',        '', '', '', ''],
            [8,  'חֲבִיל',            '', '', '', ''],
            [9,  'הִשְׁתַּנִּי',      '', '', '', ''],
            [10, 'אִתְמְלִי',         '', '', '', ''],
            [11, 'יִשְׁתַּנֵּא',      '', '', '', ''],
            [12, 'סְגִיד',            '', '', '', ''],
            [13, 'מִתְכַּנְּשִׁין',   '', '', '', ''],
            [14, 'יִתְמְחֵא',         '', '', '', ''],
            [15, 'קְטִילוּ',          '', '', '', ''],
            [16, 'אִתְקְטִלְנָא',     '', '', '', ''],
            [17, 'יִתְּבְנֵא',        '', '', '', ''],
            [18, 'הִתְחַסְּנַת',      '', '', '', ''],
            [19, 'יִתְחַסְּנוּן',     '', '', '', ''],
            [20, 'הִשְׁתְּכַחַת',     '', '', '', ''],
        ]
        ans = [
            [1,  'רְמִי',             'Peil',     'Perfect 3ms',    'רמה',  'he was thrown / was cast (III-he)'],
            [2,  'אִתְכְּנִישׁ',      'Ithpeel',  'Perfect 3ms',    'כנשׁ', 'he was gathered / gathered together'],
            [3,  'יִתְנְסַח',         'Ithpeel',  'Imperfect 3ms',  'נסח',  'it will be torn out / uprooted'],
            [4,  'שְׁבִיק',           'Peil',     'Perfect 3ms',    'שׁבק', 'it was left / abandoned'],
            [5,  'הִשְׁתְּכַח',       'Hithpeel', 'Perfect 3ms',    'שׁכח', 'it was found (metathesis: shin+taw swap)'],
            [6,  'כְּתִיב',           'Peil',     'Perf 3ms / ptcp', 'כתב', 'it is written / was written'],
            [7,  'יִתְבְּנֵא',        'Ithpeel',  'Imperfect 3ms',  'בנה',  'it will be built (III-he: -ea ending)'],
            [8,  'חֲבִיל',            'Peil',     'Perfect 3ms',    'חבל',  'it was destroyed / ruined (guttural R1)'],
            [9,  'הִשְׁתַּנִּי',      'Hithpeel', 'Perfect 3ms',    'שׁנה', 'it was changed (metathesis + III-he)'],
            [10, 'אִתְמְלִי',         'Ithpeel',  'Perfect 3ms',    'מלא',  'it was filled (III-aleph root)'],
            [11, 'יִשְׁתַּנֵּא',      'Ithpeel',  'Imperfect 3ms',  'שׁנה', 'it will be changed (metathesis)'],
            [12, 'סְגִיד',            'Peil',     'Perfect 3ms',    'סגד',  'he was worshiped / bowed down to'],
            [13, 'מִתְכַּנְּשִׁין',   'Ithpeel',  'Participle mp',  'כנשׁ', 'being gathered / gathering (mp)'],
            [14, 'יִתְמְחֵא',         'Ithpeel',  'Imperfect 3ms',  'מחא',  'it will be struck / smitten'],
            [15, 'קְטִילוּ',          'Peil',     'Perfect 3mp',    'קטל',  'they were killed'],
            [16, 'אִתְקְטִלְנָא',     'Ithpeel',  'Perfect 1cp',    'קטל',  'we were killed / killed ourselves'],
            [17, 'יִתְּבְנֵא',        'Ithpeel',  'Imperfect 3ms',  'בנה',  'it will be built (variant spelling)'],
            [18, 'הִתְחַסְּנַת',      'Hithpeel', 'Perfect 3fs',    'חסן',  'she/it was strengthened / prevailed'],
            [19, 'יִתְחַסְּנוּן',     'Ithpeel',  'Imperfect 3mp',  'חסן',  'they will be strengthened / prevail'],
            [20, 'הִשְׁתְּכַחַת',     'Hithpeel', 'Perfect 2ms',    'שׁכח', 'you were found deficient (Dan. 5:27)'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc,
                                        section_title='Peil and Ithpeel Stem Drill — Items 1–20')


def build_bba_ch18_passive_stems_drill(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh18PassiveStemsDrillPDF,
        'BBA Chapter 18 — Peil and Ithpeel Stem Drill',
        'Peil (Simple Passive) and Hithpeel/Ithpeel (Reflexive/Passive) · Daniel and Ezra',
        ['aramaic', 'bba', 'ch18', 'exercises', 'ch18-passive-stems-drill'],
        'ch18-passive-stems-drill.pdf',
        out_dir,
    )


class BbaCh19PaelStemDrillPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each numbered Pael verb form drawn from Daniel or Ezra, '
            'identify the Conjugation (Perfect / Imperfect / Imperative / Infinitive / Participle), '
            'the Root (three root consonants, Peal perfect 3ms form), '
            'the PGN (Person-Gender-Number; N/A for infinitive; active/passive for participle), '
            'and provide an English translation. '
            'Pael marker (all forms): dagesh forte in R2. '
            'Perfect: patach + dagesh-tsere in R2; 3ms = qattel pattern. '
            'Imperfect: ye- prefix (shewa, NOT hireq; contrast Peal yi-). '
            'Infinitive: le- prefix + dagesh + qamets in R2 + -ah suffix. '
            'Active participle: me- prefix + dagesh-tsere in R2. '
            'Passive participle: me- prefix + dagesh-patach in R2. '
            'III-he imperfect: ends in -ea; III-he participle: ends in -eh.'
        )
        hdrs = ['#', 'Form', 'Conjugation', 'Root', 'PGN', 'Translation']
        cr = [0.04, 0.14, 0.17, 0.10, 0.12, 0.43]
        hc = [1]
        rows = [
            [1,  'שַבַּח',             '', '', '', ''],
            [2,  'יְשַבַּח', '', '', '', ''],
            [3,  'מְשַבַּח', '', '', '', ''],
            [4,  'שַבְּחֵת', '', '', '', ''],
            [5,  'שַבַּחוּ', '', '', '', ''],
            [6,  'בָּרֵךְ',        '', '', '', ''],
            [7,  'יְבָרֵךְ',  '', '', '', ''],
            [8,  'מְבָרֵךְ',  '', '', '', ''],
            [9,  'חַוִּי',              '', '', '', ''],
            [10, 'יְחַוֵּא',  '', '', '', ''],
            [11, 'מְחַוֶּה',  '', '', '', ''],
            [12, 'נְחַוֵּא',  '', '', '', ''],
            [13, 'שַבַּחְנָא', '', '', '', ''],
            [14, 'לְשַבָּחָה', '', '', '', ''],
            [15, 'תְּשַבַּח', '', '', '', ''],
            [16, 'קַבֵּל',               '', '', '', ''],
            [17, 'יְקַבְּלוּן', '', '', '', ''],
            [18, 'שַלַּח',               '', '', '', ''],
            [19, 'מְקַטַּל',   '', '', '', ''],
            [20, 'יְרַבֵּא',   '', '', '', ''],
        ]
        ans = [
            [1,  'שַבַּח',             'Perfect',              'שבח', '3ms',          'he praised'],
            [2,  'יְשַבַּח', 'Imperfect',            'שבח', '3ms',          'he will praise'],
            [3,  'מְשַבַּח', 'Participle (active)',  'שבח', 'ms',           'praising'],
            [4,  'שַבְּחֵת', 'Perfect',              'שבח', '1cs',          'I praised'],
            [5,  'שַבַּחוּ', 'Perfect',              'שבח', '3mp',          'they praised'],
            [6,  'בָּרֵךְ',        'Perfect',              'ברך', '3ms',          'he blessed'],
            [7,  'יְבָרֵךְ',  'Imperfect',            'ברך', '3ms',          'he will bless'],
            [8,  'מְבָרֵךְ',  'Participle (active)',  'ברך', 'ms',           'blessing'],
            [9,  'חַוִּי',              'Perfect',              'חוה', '3ms (III-he)', 'he showed / declared'],
            [10, 'יְחַוֵּא',  'Imperfect',            'חוה', '3ms (III-he)', 'he will declare / show'],
            [11, 'מְחַוֶּה',  'Participle (active)',  'חוה', 'ms (III-he)',  'declaring / showing'],
            [12, 'נְחַוֵּא',  'Imperfect',            'חוה', '1cp',          'we will declare / show'],
            [13, 'שַבַּחְנָא', 'Perfect',   'שבח', '1cp',          'we praised'],
            [14, 'לְשַבָּחָה', 'Infinitive', 'שבח', 'N/A',          'to praise'],
            [15, 'תְּשַבַּח', 'Imperfect',       'שבח', '3fs / 2ms',    'she/you will praise'],
            [16, 'קַבֵּל',               'Perfect',              'קבל', '3ms',          'he received / accepted'],
            [17, 'יְקַבְּלוּן', 'Imperfect', 'קבל', '3mp', 'they will receive'],
            [18, 'שַלַּח',               'Perfect',              'שלח', '3ms',          'he sent / dispatched'],
            [19, 'מְקַטַּל',   'Participle (passive)', 'קטל', 'ms',           'being killed / the one killed'],
            [20, 'יְרַבֵּא',   'Imperfect',            'רבה', '3ms (III-he)', 'he will make great / exalt'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc,
                                        section_title='Pael Stem Drill — Items 1–20')


def build_bba_ch19_pael_stem_drill(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh19PaelStemDrillPDF,
        'BBA Chapter 19 — Pael Stem Drill',
        'Pael (D Stem — Intensive/Causative) · Daniel and Ezra',
        ['aramaic', 'bba', 'ch19', 'exercises', 'ch19-pael-stem-drill'],
        'ch19-pael-stem-drill.pdf',
        out_dir,
    )


# BBA Ch20 — Hithpaal / Ithpaal Stem Drill


class BbaCh20HithpaalDrillPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each numbered Hithpaal/Ithpaal verb form drawn from Daniel or Ezra, '
            'identify the Stem (Hithpaal — note metathesis if present), '
            'the Conjugation (Perfect / Imperfect / Imperative / Infinitive / Participle), '
            'the Root (three root consonants, Peal perfect 3ms form), '
            'the PGN (Person-Gender-Number; N/A for infinitive), '
            'and provide an English translation. '
            'Hithpaal marker: it-/hit- prefix AND dagesh forte in R2 — both features together. '
            'Metathesis: sibilant R1 (shin, sin, samekh) swaps with taw; prefix becomes hist-/isht-. '
            'Perfect 3ms: it-qattal pattern — it- prefix + patach + dagesh-patach in R2 (contrast Pael: tsere in R2). '
            'Imperfect 3ms: yit-qattal; prefix yit- (yod + hireq + taw + shewa). '
            'Participle: mit-qattal; prefix mit- (mem + hireq + taw + shewa). '
            'Distinguish from Ithpeel: same prefix but Ithpeel has NO dagesh in R2.'
        )
        hdrs = ['#', 'Form', 'Stem', 'Conjugation', 'Root', 'PGN', 'Translation']
        cr = [0.04, 0.13, 0.13, 0.14, 0.10, 0.10, 0.36]
        hc = [1]
        rows = [
            [1,  'הִשְׁתַּכַּח',      '', '', '', '', ''],
            [2,  'אִתְחַשַּׁב',       '', '', '', '', ''],
            [3,  'יִתְחַבַּל',        '', '', '', '', ''],
            [4,  'הִשְׁתַּכַּחוּ',    '', '', '', '', ''],
            [5,  'מִשְׁתַּכַּח',      '', '', '', '', ''],
            [6,  'הִתְנַדַּב',        '', '', '', '', ''],
            [7,  'הִתְמְלִּי',        '', '', '', '', ''],
            [8,  'יִתְרוֹמַם',        '', '', '', '', ''],
            [9,  'אִתְקַטַּל',        '', '', '', '', ''],
            [10, 'הִשְׁתַּוִּי',      '', '', '', '', ''],
            [11, 'מִתְנַדְּבִין',     '', '', '', '', ''],
            [12, 'תִּתְחַשַּׁב',     '', '', '', '', ''],
            [13, 'אִתְקַטַּלוּ',      '', '', '', '', ''],
            [14, 'מִתְקַטַּל',        '', '', '', '', ''],
            [15, 'הִשְׁתַּכַּחַת',    '', '', '', '', ''],
            [16, 'יִתְקַטְּלוּן',     '', '', '', '', ''],
            [17, 'אִתְנַדַּבְנָא',    '', '', '', '', ''],
            [18, 'לְהִתְקַטָּלָה',    '', '', '', '', ''],
            [19, 'אֶתְחַשַּׁב',       '', '', '', '', ''],
            [20, 'מִשְׁתַּכְּחָן',    '', '', '', '', ''],
        ]
        ans = [
            [1,  'הִשְׁתַּכַּח',      'Hithpaal (metath.)', 'Perfect',    'שׁכח',     '3ms',        'it/he was found'],
            [2,  'אִתְחַשַּׁב',       'Hithpaal',          'Perfect',    'חשׁב',     '3ms',        'it was reckoned / considered'],
            [3,  'יִתְחַבַּל',        'Hithpaal',          'Imperfect',  'חבל',      '3ms',        'it will be destroyed / harmed'],
            [4,  'הִשְׁתַּכַּחוּ',    'Hithpaal (metath.)', 'Perfect',   'שׁכח',     '3mp',        'they were found'],
            [5,  'מִשְׁתַּכַּח',      'Hithpaal (metath.)', 'Participle', 'שׁכח',    'ms',         'being found / was found'],
            [6,  'הִתְנַדַּב',        'Hithpaal',          'Perfect',    'נדב',      '3ms',        'he volunteered / gave freely'],
            [7,  'הִתְמְלִּי',        'Hithpaal',          'Perfect',    'מלא/מלי',  '3ms (III-he)', 'he was filled'],
            [8,  'יִתְרוֹמַם',        'Hithpaal',          'Imperfect',  'רמם/רום',  '3ms',        'he will exalt himself'],
            [9,  'אִתְקַטַּל',        'Hithpaal',          'Perfect',    'קטל',      '3ms',        'he was killed (model)'],
            [10, 'הִשְׁתַּוִּי',      'Hithpaal (metath.)', 'Perfect',   'שׁוה',    '3ms (III-he)', 'he became equal / was made like'],
            [11, 'מִתְנַדְּבִין',     'Hithpaal',          'Participle', 'נדב',      'mp',         'volunteering / those who volunteer'],
            [12, 'תִּתְחַשַּׁב',     'Hithpaal',          'Imperfect',  'חשׁב',     '3fs / 2ms',  'she/it will be reckoned / you will consider'],
            [13, 'אִתְקַטַּלוּ',      'Hithpaal',          'Perfect',    'קטל',      '3mp',        'they were killed (model)'],
            [14, 'מִתְקַטַּל',        'Hithpaal',          'Participle', 'קטל',      'ms',         'being killed (model)'],
            [15, 'הִשְׁתַּכַּחַת',    'Hithpaal (metath.)', 'Perfect',   'שׁכח',    '3fs',        'she/it was found'],
            [16, 'יִתְקַטְּלוּן',     'Hithpaal',          'Imperfect',  'קטל',      '3mp',        'they will be killed (model)'],
            [17, 'אִתְנַדַּבְנָא',    'Hithpaal',          'Perfect',    'נדב',      '1cp',        'we volunteered / gave freely'],
            [18, 'לְהִתְקַטָּלָה',    'Hithpaal',          'Infinitive', 'קטל',      'N/A',        'to be killed / to kill oneself (model)'],
            [19, 'אֶתְחַשַּׁב',       'Hithpaal',          'Imperfect',  'חשׁב',     '1cs',        'I will be reckoned / will consider'],
            [20, 'מִשְׁתַּכְּחָן',    'Hithpaal (metath.)', 'Participle', 'שׁכח',   'fp',         'being found (fp) / those (f) being found'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc,
                                        section_title='Hithpaal / Ithpaal Stem Drill — Items 1–20')


def build_bba_ch20_hithpaal_drill(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh20HithpaalDrillPDF,
        'BBA Chapter 20 — Hithpaal / Ithpaal Stem Drill',
        'Hithpaal / Ithpaal (Dt Stem — Reflexive/Passive of Pael) · Daniel and Ezra',
        ['aramaic', 'bba', 'ch20', 'exercises', 'ch20-hithpaal-drill'],
        'ch20-hithpaal-drill.pdf',
        out_dir,
    )


class BbaCh21HaphelStemDrillPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each numbered Haphel verb form drawn from Daniel or Ezra, '
            'identify the Conjugation (Perfect / Imperfect / Imperative / Infinitive / Participle), '
            'the Root (three root consonants, Peal perfect 3ms form), '
            'the PGN (Person-Gender-Number; N/A for infinitive; ms/mp/fs for participle), '
            'and provide an English translation. '
            'All forms are Haphel (H stem — causative). '
            'Haphel perfect: ha- prefix before R1; tsere in R2; no R2 dagesh. '
            'Haphel imperfect: yeh- prefix letter + ha- visible in stem (yeha-); tsere in R2. '
            'Haphel infinitive: leha- + qamets in R2 + -ah ending. '
            'Haphel participle: meha- prefix; tsere in R2; no R2 dagesh (contrast Pael: R2 dagesh). '
            'I-yod roots (yadac): ha + yeh- contracts to ho- (holem-waw). '
            'Hollow roots (qum): haqim pattern (compensatory dagesh in R3, not D-stem doubling). '
            '"Bring" root (yty/ath): fixed stem hethi (Haphel perfect 3ms).'
        )
        hdrs = ['#', 'Form', 'Conjugation', 'Root', 'PGN', 'Translation']
        cr = [0.04, 0.14, 0.16, 0.11, 0.13, 0.42]
        hc = [1]
        rows = [
            [1,  'הוֹדַע',         '', '', '', ''],
            [2,  'הַקִּים',         '', '', '', ''],
            [3,  'הֵיתִיוּ',        '', '', '', ''],
            [4,  'יְהוֹדַע',        '', '', '', ''],
            [5,  'לְהוֹדָעָה',      '', '', '', ''],
            [6,  'מְהוֹדֵעַ',       '', '', '', ''],
            [7,  'הַשְׁלְטָךְ',     '', '', '', ''],
            [8,  'מְהַעְדֵּה',      '', '', '', ''],
            [9,  'מְהַשְׁנֵא',      '', '', '', ''],
            [10, 'הַקִּימוּ',        '', '', '', ''],
            [11, 'לְהַשְׁלָטָה',    '', '', '', ''],
            [12, 'יְהַשְׁלַח',      '', '', '', ''],
            [13, 'הֵיתִי',          '', '', '', ''],
            [14, 'הוֹדַעְתְּ',      '', '', '', ''],
            [15, 'מְהָקֵם',         '', '', '', ''],
            [16, 'הַקְטֵל',         '', '', '', ''],
            [17, 'יְהֵיתוּן',       '', '', '', ''],
            [18, 'הַשְׁלֵט',        '', '', '', ''],
            [19, 'לְהַקְטָלָה',     '', '', '', ''],
            [20, 'מְהַקְטֵל',       '', '', '', ''],
        ]
        ans = [
            [1,  'הוֹדַע',         'Perfect',              'ידע',      '3ms',              'he made known / revealed'],
            [2,  'הַקִּים',         'Perfect',              'קום',      '3ms',              'he set up / established'],
            [3,  'הֵיתִיוּ',        'Perfect',              'יתי/אתה',  '3mp',              'they brought'],
            [4,  'יְהוֹדַע',        'Imperfect',            'ידע',      '3ms',              'he will make known / reveal'],
            [5,  'לְהוֹדָעָה',      'Infinitive',           'ידע',      'N/A',              'to make known / to declare'],
            [6,  'מְהוֹדֵעַ',       'Participle',           'ידע',      'ms',               'making known / revealing'],
            [7,  'הַשְׁלְטָךְ',     'Perfect',              'שׁלט',    '3ms + 2ms obj.',   'he made you ruler over'],
            [8,  'מְהַעְדֵּה',      'Participle',           'עדה',      'ms',               'removing / deposing'],
            [9,  'מְהַשְׁנֵא',      'Participle',           'שׁנה',    'ms',               'changing / altering'],
            [10, 'הַקִּימוּ',        'Perfect',              'קום',      '3mp',              'they set up / established'],
            [11, 'לְהַשְׁלָטָה',    'Infinitive',           'שׁלט',    'N/A',              'to give rule / to make ruler'],
            [12, 'יְהַשְׁלַח',      'Imperfect',            'שׁלח',    '3ms',              'he will send out / throw'],
            [13, 'הֵיתִי',          'Perfect',              'יתי/אתה',  '3ms',              'he brought'],
            [14, 'הוֹדַעְתְּ',      'Perfect',              'ידע',      '2ms',              'you made known / revealed'],
            [15, 'מְהָקֵם',         'Participle',           'קום',      'ms',               'setting up / establishing'],
            [16, 'הַקְטֵל',         'Perfect / Imperative', 'קטל',      '3ms / 2ms',        'he caused to kill / cause to kill! (model)'],
            [17, 'יְהֵיתוּן',       'Imperfect',            'יתי/אתה',  '3mp',              'they will bring'],
            [18, 'הַשְׁלֵט',        'Perfect',              'שׁלט',    '3ms',              'he made [him] ruler / gave dominion'],
            [19, 'לְהַקְטָלָה',     'Infinitive',           'קטל',      'N/A',              'to cause to kill (model)'],
            [20, 'מְהַקְטֵל',       'Participle',           'קטל',      'ms',               'causing to kill (model)'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc,
                                        section_title='Haphel Stem Drill — Items 1–20')


def build_bba_ch21_haphel_stem_drill(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh21HaphelStemDrillPDF,
        'BBA Chapter 21 — Haphel Stem Drill',
        'Haphel (H Stem — Causative) · Daniel and Ezra',
        ['aramaic', 'bba', 'ch21', 'exercises', 'ch21-haphel-stem-drill'],
        'ch21-haphel-stem-drill.pdf',
        out_dir,
    )


class BbaCh22CausativePassiveDrillPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'Capstone review covering all nine Aramaic stems (BBA Ch12-22). '
            'For each numbered verb form from Daniel or Ezra, identify: '
            'Stem (Peal / Peil / Ithpeel / Pael / Ithpaal / Haphel / Aphel / Shaphel / Hophal), '
            'Conjugation (Perfect / Imperfect / Imperative / Infinitive / Participle), '
            'Root (three root consonants), '
            'PGN (Person-Gender-Number; N/A for infinitive; ms/mp/fs for participle), '
            'and Translation. '
            'Diagnostics — Peal: no prefix, no R2 dagesh; '
            'Peil: qetil vowel pattern; '
            'Ithpeel: it/hit- prefix, no R2 dagesh; '
            'Pael: R2 dagesh forte (no prefix); '
            'Ithpaal: it/hit- prefix + R2 dagesh; '
            'Haphel: ha- (perf) / yeha- (imperf) / meha- (ptcp); '
            'Aphel: a- prefix, tsere in R2; '
            'Shaphel: sha-/she- prefix; '
            'Hophal: hu- (heh + qibbuts u-vowel).'
        )
        hdrs = ['#', 'Form', 'Stem', 'Conjugation', 'Root', 'PGN', 'Translation']
        cr = [0.04, 0.13, 0.12, 0.13, 0.09, 0.10, 0.39]
        hc = [1]
        rows = [
            [1,  'שֵׁיזִב',              '', '', '', '', ''],
            [2,  'הֻנְעַל',              '', '', '', '', ''],
            [3,  'אַחֲוִי',              '', '', '', '', ''],
            [4,  'יְשֵׁיזְבִנְּכוֹן',   '', '', '', '', ''],
            [5,  'לְשֵׁיזָבָה',          '', '', '', '', ''],
            [6,  'אַסְגִּי',             '', '', '', '', ''],
            [7,  'הֻרְמִי',              '', '', '', '', ''],
            [8,  'שֵׁיזְבָךְ',           '', '', '', '', ''],
            [9,  'כְּתַב',               '', '', '', '', ''],
            [10, 'כְּתִיב',              '', '', '', '', ''],
            [11, 'אִתְכְּתִב',           '', '', '', '', ''],
            [12, 'קַטֵּל',               '', '', '', '', ''],
            [13, 'אִתְקַטַּל',           '', '', '', '', ''],
            [14, 'הוֹדַע',               '', '', '', '', ''],
            [15, 'מְהַקְטֵל',            '', '', '', '', ''],
            [16, 'יְהַקְטֵל',            '', '', '', '', ''],
            [17, 'מְהוֹדֵעַ',            '', '', '', '', ''],
            [18, 'הַקִּים',              '', '', '', '', ''],
            [19, 'מְקַטֵּל',             '', '', '', '', ''],
            [20, 'יְשֵׁיזִב',            '', '', '', '', ''],
        ]
        ans = [
            [1,  'שֵׁיזִב',              'Shaphel',   'Perfect',    'יזב',      '3ms',               'he delivered / rescued'],
            [2,  'הֻנְעַל',              'Hophal',    'Perfect',    'עלל',      '3ms',               'was brought in'],
            [3,  'אַחֲוִי',              'Aphel',     'Perfect',    'חזה',      '3ms',               'he showed / declared'],
            [4,  'יְשֵׁיזְבִנְּכוֹן',   'Shaphel',   'Imperfect',  'יזב',      '3ms + 2mp obj.',    'will deliver you (pl.)'],
            [5,  'לְשֵׁיזָבָה',          'Shaphel',   'Infinitive', 'יזב',      'N/A',               'to deliver / rescue'],
            [6,  'אַסְגִּי',             'Aphel',     'Perfect',    'סגא/סגה',  '3ms',               'he made great / magnified'],
            [7,  'הֻרְמִי',              'Hophal',    'Perfect',    'רמה',      '3ms',               'was cast / thrown'],
            [8,  'שֵׁיזְבָךְ',           'Shaphel',   'Perfect',    'יזב',      '3ms + 2ms obj.',    'he delivered you'],
            [9,  'כְּתַב',               'Peal',      'Perfect',    'כתב',      '3ms',               'he wrote'],
            [10, 'כְּתִיב',              'Peil',      'Participle', 'כתב',      'ms',                'written / it is written'],
            [11, 'אִתְכְּתִב',           'Ithpeel',   'Perfect',    'כתב',      '3ms',               'it was written / recorded'],
            [12, 'קַטֵּל',               'Pael',      'Perfect',    'קטל',      '3ms',               'he killed / slaughtered'],
            [13, 'אִתְקַטַּל',           'Ithpaal',   'Perfect',    'קטל',      '3ms',               'he was killed'],
            [14, 'הוֹדַע',               'Haphel',    'Perfect',    'ידע',      '3ms',               'he made known / revealed'],
            [15, 'מְהַקְטֵל',            'Haphel',    'Participle', 'קטל',      'ms',                'causing to kill (model)'],
            [16, 'יְהַקְטֵל',            'Haphel',    'Imperfect',  'קטל',      '3ms',               'he will cause to kill (model)'],
            [17, 'מְהוֹדֵעַ',            'Haphel',    'Participle', 'ידע',      'ms',                'making known / revealing'],
            [18, 'הַקִּים',              'Haphel',    'Perfect',    'קום',      '3ms',               'he set up / established'],
            [19, 'מְקַטֵּל',             'Pael',      'Participle', 'קטל',      'ms',                'killing intensively (model)'],
            [20, 'יְשֵׁיזִב',            'Shaphel',   'Imperfect',  'יזב',      '3ms',               'he will deliver / rescue'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc,
                                        section_title='Capstone Review Drill — All Nine Stems — Items 1–20')


def build_bba_ch22_causative_passive_drill(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh22CausativePassiveDrillPDF,
        'BBA Chapter 22 — Causative & Passive Stems: Capstone Review',
        'All Nine Aramaic Stems · Daniel and Ezra · Capstone Drill',
        ['aramaic', 'bba', 'ch22', 'exercises', 'ch22-causative-passive-drill'],
        'ch22-causative-passive-drill.pdf',
        out_dir,
    )




# ---------------------------------------------------------------------------
# BBA Ch13 — Peal Perfect vs. Peal Imperfect Contrast Drill
# ---------------------------------------------------------------------------

class BbaCh13PealContrastPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each form, classify as Peal Perfect or Peal Imperfect, '
            'then give Person, Gender, Number, Root (three root consonants), and Translation. '
            'Key diagnostic: Imperfect has a preformative prefix (y/t/n/aleph + vowel); '
            'Perfect has no preformative.'
        )
        hdrs = ['#', 'Form', 'Conj (Pf/Impf)', 'Person', 'Gender', 'Number', 'Root', 'Translation']
        cr = [0.04, 0.12, 0.10, 0.07, 0.07, 0.07, 0.10, 0.43]
        hc = [1]
        rows = [
            ['1',  'כְּתַב',      '', '', '', '', '', ''],
            ['2',  'יִכְתֻּב',    '', '', '', '', '', ''],
            ['3',  'אֲמַר',       '', '', '', '', '', ''],
            ['4',  'תֵּאמַר',     '', '', '', '', '', ''],
            ['5',  'קְטַלַת',     '', '', '', '', '', ''],
            ['6',  'יִקְטֻל',     '', '', '', '', '', ''],
            ['7',  'שְׁמַעְנָא',  '', '', '', '', '', ''],
            ['8',  'נִשְׁמַע',    '', '', '', '', '', ''],
            ['9',  'עֲבַד',       '', '', '', '', '', ''],
            ['10', 'יַעְבֵּד',    '', '', '', '', '', ''],
            ['11', 'קְטַלוּ',     '', '', '', '', '', ''],
            ['12', 'יִקְטְלוּן',  '', '', '', '', '', ''],
            ['13', 'יְדַעְתְּ',   '', '', '', '', '', ''],
            ['14', 'תִּנְדַּע',   '', '', '', '', '', ''],
            ['15', 'נְפַל',       '', '', '', '', '', ''],
            ['16', 'יִּנְפֵּל',   '', '', '', '', '', ''],
            ['17', 'שָׁלַחְנָא',  '', '', '', '', '', ''],
            ['18', 'יִשְׁלַח',    '', '', '', '', '', ''],
            ['19', 'קְרָא',       '', '', '', '', '', ''],
            ['20', 'יִקְרֵא',     '', '', '', '', '', ''],
        ]
        ans = [
            ['1',  'כְּתַב',     'Perfect',    '3', 'm', 's',  'כתב', 'he wrote'],
            ['2',  'יִכְתֻּב',   'Imperfect',  '3', 'm', 's',  'כתב', 'he will write'],
            ['3',  'אֲמַר',      'Perfect',    '3', 'm', 's',  'אמר', 'he said'],
            ['4',  'תֵּאמַר',    'Imperfect',  '2/3','f','s',  'אמר', 'you (f.s.) will say / she will say'],
            ['5',  'קְטַלַת',    'Perfect',    '3', 'f', 's',  'קטל', 'she killed'],
            ['6',  'יִקְטֻל',    'Imperfect',  '3', 'm', 's',  'קטל', 'he will kill'],
            ['7',  'שְׁמַעְנָא', 'Perfect',    '1', 'c', 'pl', 'שׁמע','we heard'],
            ['8',  'נִשְׁמַע',   'Imperfect',  '1', 'c', 'pl', 'שׁמע','we will hear'],
            ['9',  'עֲבַד',      'Perfect',    '3', 'm', 's',  'עבד', 'he made / did'],
            ['10', 'יַעְבֵּד',   'Imperfect',  '3', 'm', 's',  'עבד', 'he will make / do'],
            ['11', 'קְטַלוּ',    'Perfect',    '3', 'm', 'pl', 'קטל', 'they killed'],
            ['12', 'יִקְטְלוּן', 'Imperfect',  '3', 'm', 'pl', 'קטל', 'they will kill'],
            ['13', 'יְדַעְתְּ',  'Perfect',    '2', 'm', 's',  'ידע', 'you knew'],
            ['14', 'תִּנְדַּע',  'Imperfect',  '2', 'm', 's',  'ידע', 'you will know'],
            ['15', 'נְפַל',      'Perfect',    '3', 'm', 's',  'נפל', 'he fell'],
            ['16', 'יִּנְפֵּל',  'Imperfect',  '3', 'm', 's',  'נפל', 'he will fall'],
            ['17', 'שָׁלַחְנָא', 'Perfect',    '1', 'c', 'pl', 'שׁלח','we sent'],
            ['18', 'יִשְׁלַח',   'Imperfect',  '3', 'm', 's',  'שׁלח','he will send'],
            ['19', 'קְרָא',      'Perfect',    '3', 'm', 's',  'קרא', 'he called / read'],
            ['20', 'יִקְרֵא',    'Imperfect',  '3', 'm', 's',  'קרא', 'he will call / read'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc,
                                        section_title='Peal Perfect vs. Imperfect Contrast — Items 1–20')


def build_bba_ch13_peal_contrast(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh13PealContrastPDF,
        'BBA Chapter 13 — Peal Perfect vs. Peal Imperfect Contrast Drill',
        'Peal Perfect and Imperfect · Daniel and Ezra · Contrast and Parse',
        ['aramaic', 'bba', 'ch13', 'exercises', 'ch13-peal-contrast'],
        'ch13-peal-contrast.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBA Ch18 — Peil vs. Ithpeel Stem Identification Drill
# ---------------------------------------------------------------------------

class BbaCh18StemContrastPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each form, identify the stem (Peil or Ithpeel), '
            'then give Conjugation, PGN, Root, and Translation. '
            'Peil diagnostic: internal vowel pattern CvCīC (long i under R2), no prefix. '
            'Ithpeel diagnostic: אִתְ prefix (perfect) or יִתְ prefix (imperfect).'
        )
        hdrs = ['#', 'Form', 'Stem (Peil/Ithpeel)', 'Conjugation', 'PGN', 'Root', 'Translation']
        cr = [0.04, 0.14, 0.12, 0.12, 0.10, 0.12, 0.36]
        hc = [1]
        rows = [
            ['1',  'כְּתִיב',      '', '', '', '', ''],
            ['2',  'הִתְכְּתִיב',  '', '', '', '', ''],
            ['3',  'קְטִיל',       '', '', '', '', ''],
            ['4',  'אִתְקְטֵל',    '', '', '', '', ''],
            ['5',  'שִׂים',        '', '', '', '', ''],
            ['6',  'יִתְבְּנֵא',   '', '', '', '', ''],
            ['7',  'יִתְכְּתִב',   '', '', '', '', ''],
            ['8',  'שְׂכִיר',      '', '', '', '', ''],
            ['9',  'אִתְעֲבִיד',   '', '', '', '', ''],
            ['10', 'נְתִין',       '', '', '', '', ''],
            ['11', 'יִתְיְהִב',    '', '', '', '', ''],
            ['12', 'קְרִי',        '', '', '', '', ''],
            ['13', 'אִתְאֲמַר',    '', '', '', '', ''],
            ['14', 'נְבִיא',       '', '', '', '', ''],
            ['15', 'יִתְנְסַח',    '', '', '', '', ''],
            ['16', 'כְּפִית',      '', '', '', '', ''],
            ['17', 'אִתְחֲזֵה',    '', '', '', '', ''],
            ['18', 'עֲבִיד',       '', '', '', '', ''],
            ['19', 'יִתְקְרֵא',    '', '', '', '', ''],
            ['20', 'שְׁלִים',      '', '', '', '', ''],
        ]
        ans = [
            ['1',  'כְּתִיב',     'Peil',    'Perfect',     '3ms', 'כתב', 'it was written'],
            ['2',  'הִתְכְּתִיב', 'Ithpeel', 'Perfect',     '3ms', 'כתב', 'it was inscribed / registered itself'],
            ['3',  'קְטִיל',      'Peil',    'Perfect',     '3ms', 'קטל', 'he was killed'],
            ['4',  'אִתְקְטֵל',   'Ithpeel', 'Perfect',     '3ms', 'קטל', 'he was killed (reflexive nuance)'],
            ['5',  'שִׂים',       'Peil',    'Perfect',     '3ms', 'שׂים', 'it was placed / set'],
            ['6',  'יִתְבְּנֵא',  'Ithpeel', 'Imperfect',   '3ms', 'בנה', 'it will be built'],
            ['7',  'יִתְכְּתִב',  'Ithpeel', 'Imperfect',   '3ms', 'כתב', 'it will be written'],
            ['8',  'שְׂכִיר',     'Peil',    'Perfect',     '3ms', 'שׂכר', 'he was hired'],
            ['9',  'אִתְעֲבִיד',  'Ithpeel', 'Perfect',     '3ms', 'עבד', 'it was done / made'],
            ['10', 'נְתִין',      'Peil',    'Perfect',     '3ms', 'נתן', 'it was given'],
            ['11', 'יִתְיְהִב',   'Ithpeel', 'Imperfect',   '3ms', 'יהב', 'it will be given'],
            ['12', 'קְרִי',       'Peil',    'Perfect',     '3ms', 'קרא', 'it was called / read'],
            ['13', 'אִתְאֲמַר',   'Ithpeel', 'Perfect',     '3ms', 'אמר', 'it was said'],
            ['14', 'נְבִיא',      'Peil',    'Perfect',     '3ms', 'נבא', 'he was prophesied / he is a prophet'],
            ['15', 'יִתְנְסַח',   'Ithpeel', 'Imperfect',   '3ms', 'נסח', 'it will be pulled out / uprooted'],
            ['16', 'כְּפִית',     'Peil',    'Perfect',     '3ms', 'כפת', 'he was bound'],
            ['17', 'אִתְחֲזֵה',   'Ithpeel', 'Perfect',     '3ms', 'חזה', 'it was seen / it appeared'],
            ['18', 'עֲבִיד',      'Peil',    'Perfect',     '3ms', 'עבד', 'it was made / done'],
            ['19', 'יִתְקְרֵא',   'Ithpeel', 'Imperfect',   '3ms', 'קרא', 'it will be called'],
            ['20', 'שְׁלִים',     'Peil',    'Perfect',     '3ms', 'שׁלם','it was completed / finished'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc,
                                        section_title='Peil vs. Ithpeel Identification Drill — Items 1–20')


def build_bba_ch18_stem_contrast(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh18StemContrastPDF,
        'BBA Chapter 18 — Peil vs. Ithpeel Stem Identification Drill',
        'Passive Peil vs. Reflexive/Passive Ithpeel · Daniel and Ezra',
        ['aramaic', 'bba', 'ch18', 'exercises', 'ch18-stem-contrast'],
        'ch18-stem-contrast.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBA Ch19 — Peal vs. Pael Contrast Drill
# ---------------------------------------------------------------------------

class BbaCh19PaelPealContrastPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each form, identify the stem (Peal or Pael), '
            'then give Conjugation, PGN, Root, and Translation. '
            'Pael diagnostic: dagesh forte in R2 (doubling of the second root consonant). '
            'Peal has no dagesh forte in R2.'
        )
        hdrs = ['#', 'Form', 'Stem (Peal/Pael)', 'Conjugation', 'PGN', 'Root', 'Translation']
        cr = [0.04, 0.13, 0.11, 0.12, 0.10, 0.12, 0.38]
        hc = [1]
        rows = [
            ['1',  'כְּתַב',      '', '', '', '', ''],
            ['2',  'כַּתֵּב',     '', '', '', '', ''],
            ['3',  'אֲמַר',       '', '', '', '', ''],
            ['4',  'חַוִּי',      '', '', '', '', ''],
            ['5',  'עֲבַד',       '', '', '', '', ''],
            ['6',  'בַּטִּיל',    '', '', '', '', ''],
            ['7',  'קְרָא',       '', '', '', '', ''],
            ['8',  'קַדֵּשׁ',     '', '', '', '', ''],
            ['9',  'יְדַע',       '', '', '', '', ''],
            ['10', 'שַׁוִּי',     '', '', '', '', ''],
            ['11', 'שְׁמַע',      '', '', '', '', ''],
            ['12', 'רַבִּי',      '', '', '', '', ''],
            ['13', 'נְפַל',       '', '', '', '', ''],
            ['14', 'כַּבֵּד',     '', '', '', '', ''],
            ['15', 'יִקְטֻל',     '', '', '', '', ''],
            ['16', 'יְבַטֵּל',    '', '', '', '', ''],
            ['17', 'אֲמַרְנָא',   '', '', '', '', ''],
            ['18', 'מְשַׁבַּח',   '', '', '', '', ''],
            ['19', 'שְׁלַח',      '', '', '', '', ''],
            ['20', 'שַׁלַּח',     '', '', '', '', ''],
        ]
        ans = [
            ['1',  'כְּתַב',     'Peal', 'Perfect',    '3ms', 'כתב', 'he wrote'],
            ['2',  'כַּתֵּב',    'Pael', 'Perfect',    '3ms', 'כתב', 'he wrote (intensively) / he recorded'],
            ['3',  'אֲמַר',      'Peal', 'Perfect',    '3ms', 'אמר', 'he said'],
            ['4',  'חַוִּי',     'Pael', 'Perfect',    '3ms', 'חוה', 'he declared / he showed'],
            ['5',  'עֲבַד',      'Peal', 'Perfect',    '3ms', 'עבד', 'he made / did'],
            ['6',  'בַּטִּיל',   'Pael', 'Perfect',    '3ms', 'בטל', 'he caused to cease / he stopped'],
            ['7',  'קְרָא',      'Peal', 'Perfect',    '3ms', 'קרא', 'he called / read'],
            ['8',  'קַדֵּשׁ',    'Pael', 'Perfect',    '3ms', 'קדשׁ','he sanctified / hallowed'],
            ['9',  'יְדַע',      'Peal', 'Perfect',    '3ms', 'ידע', 'he knew'],
            ['10', 'שַׁוִּי',    'Pael', 'Perfect',    '3ms', 'שׁוה','he made equal / he set'],
            ['11', 'שְׁמַע',     'Peal', 'Perfect',    '3ms', 'שׁמע','he heard'],
            ['12', 'רַבִּי',     'Pael', 'Perfect',    '3ms', 'רבה', 'he made great / he magnified'],
            ['13', 'נְפַל',      'Peal', 'Perfect',    '3ms', 'נפל', 'he fell'],
            ['14', 'כַּבֵּד',    'Pael', 'Perfect',    '3ms', 'כבד', 'he honored'],
            ['15', 'יִקְטֻל',    'Peal', 'Imperfect',  '3ms', 'קטל', 'he will kill'],
            ['16', 'יְבַטֵּל',   'Pael', 'Imperfect',  '3ms', 'בטל', 'he will cause to cease'],
            ['17', 'אֲמַרְנָא',  'Peal', 'Perfect',    '1cp', 'אמר', 'we said'],
            ['18', 'מְשַׁבַּח',  'Pael', 'Participle', 'ms',  'שׁבח','praising / who praises'],
            ['19', 'שְׁלַח',     'Peal', 'Perfect',    '3ms', 'שׁלח','he sent'],
            ['20', 'שַׁלַּח',    'Pael', 'Perfect',    '3ms', 'שׁלח','he sent away / he let go'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc,
                                        section_title='Peal vs. Pael Contrast Drill — Items 1–20')


def build_bba_ch19_pael_peal_contrast(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh19PaelPealContrastPDF,
        'BBA Chapter 19 — Peal vs. Pael Contrast Drill',
        'Simple Peal vs. Intensive/Factitive Pael · Daniel and Ezra',
        ['aramaic', 'bba', 'ch19', 'exercises', 'ch19-pael-qal-contrast'],
        'ch19-pael-qal-contrast.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBA Ch20 — Hithpaal Semantic Function Sorting
# ---------------------------------------------------------------------------

class BbaCh20HithpaalFunctionSortPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each Hithpaal/Ithpaal form, classify the semantic function: '
            'RF (Reflexive), RC (Reciprocal), IT (Iterative/Frequentative), ES (Estimative). '
            'Then give Conjugation, PGN, Root, and Translation.'
        )
        hdrs = ['#', 'Form', 'Function (RF/RC/IT/ES)', 'Conjugation', 'PGN', 'Root', 'Translation']
        cr = [0.04, 0.14, 0.12, 0.12, 0.09, 0.12, 0.37]
        hc = [1]
        rows = [
            ['1',  'הִשְׁתַּחֲוִי',    '', '', '', '', ''],
            ['2',  'יִשְׁתַּחֲווּן',   '', '', '', '', ''],
            ['3',  'מִתְכַּנְּשִׁין',  '', '', '', '', ''],
            ['4',  'הִתְחַשַּׁב',     '', '', '', '', ''],
            ['5',  'יִתְחַבַּר',      '', '', '', '', ''],
            ['6',  'מִתְנַדְּבִין',   '', '', '', '', ''],
            ['7',  'אִשְׁתַּדַּל',    '', '', '', '', ''],
            ['8',  'הִתְגְּזֵרַת',   '', '', '', '', ''],
            ['9',  'יִתְרָחֵץ',      '', '', '', '', ''],
            ['10', 'מִתְבַּהֲלִין',   '', '', '', '', ''],
            ['11', 'הִתְקְטַל',      '', '', '', '', ''],
            ['12', 'יִשְׁתַּנּוּן',   '', '', '', '', ''],
            ['13', 'מִתְנַסּוֹ',     '', '', '', '', ''],
            ['14', 'אִתְחַשַּׁב',    '', '', '', '', ''],
            ['15', 'הִתְבַּהֲלוּ',   '', '', '', '', ''],
            ['16', 'מִתְכַּנְּשִׁין', '', '', '', '', ''],
            ['17', 'יִשְׁתַּחֲוֵה',   '', '', '', '', ''],
            ['18', 'הִשְׁתַּכַּח',   '', '', '', '', ''],
            ['19', 'מִתְחַזֵּא',     '', '', '', '', ''],
            ['20', 'יִתְכַּנְּשׁוּן', '', '', '', '', ''],
        ]
        ans = [
            ['1',  'הִשְׁתַּחֲוִי',   'RF', 'Perfect',    '3ms', 'שׁחה', 'he bowed himself down'],
            ['2',  'יִשְׁתַּחֲווּן',  'RF', 'Imperfect',  '3mp', 'שׁחה', 'they will bow themselves down'],
            ['3',  'מִתְכַּנְּשִׁין', 'IT', 'Participle', 'mp',  'כנשׁ', 'gathering repeatedly / assembling'],
            ['4',  'הִתְחַשַּׁב',    'ES', 'Perfect',    '3ms', 'חשׁב', 'he was reckoned / counted himself'],
            ['5',  'יִתְחַבַּר',     'RF', 'Imperfect',  '3ms', 'חבר', 'he will join himself / ally himself'],
            ['6',  'מִתְנַדְּבִין',  'IT', 'Participle', 'mp',  'נדב', 'volunteering (repeatedly)'],
            ['7',  'אִשְׁתַּדַּל',   'RF', 'Perfect',    '3ms', 'שׁדל', 'he exerted himself'],
            ['8',  'הִתְגְּזֵרַת',  'RF', 'Perfect',    '3fs', 'גזר', 'it was decreed / cut off from itself'],
            ['9',  'יִתְרָחֵץ',     'RF', 'Imperfect',  '3ms', 'רחץ', 'he will wash himself'],
            ['10', 'מִתְבַּהֲלִין',  'IT', 'Participle', 'mp',  'בהל', 'being continually troubled / terrified'],
            ['11', 'הִתְקְטַל',     'RF', 'Perfect',    '3ms', 'קטל', 'he was slain (reflexive pass.)'],
            ['12', 'יִשְׁתַּנּוּן',  'RF', 'Imperfect',  '3mp', 'שׁנה', 'they will change themselves'],
            ['13', 'מִתְנַסּוֹ',    'IT', 'Participle', 'ms',  'נסה', 'testing repeatedly'],
            ['14', 'אִתְחַשַּׁב',   'ES', 'Perfect',    '3ms', 'חשׁב', 'it was reckoned as / counted'],
            ['15', 'הִתְבַּהֲלוּ',  'RF', 'Perfect',    '3mp', 'בהל', 'they were terrified'],
            ['16', 'מִתְכַּנְּשִׁין','IT', 'Participle', 'mp',  'כנשׁ', 'repeatedly assembling / coming together'],
            ['17', 'יִשְׁתַּחֲוֵה',  'RF', 'Imperfect',  '3ms', 'שׁחה', 'he will bow himself down'],
            ['18', 'הִשְׁתַּכַּח',  'RF', 'Perfect',    '3ms', 'שׁכח', 'he was found (reflexive passive)'],
            ['19', 'מִתְחַזֵּא',    'RF', 'Participle', 'ms',  'חזה', 'appearing / seeming'],
            ['20', 'יִתְכַּנְּשׁוּן','IT', 'Imperfect',  '3mp', 'כנשׁ', 'they will assemble (repeatedly)'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc,
                                        section_title='Hithpaal Function Sort — Items 1–20')


def build_bba_ch20_hithpaal_function_sort(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh20HithpaalFunctionSortPDF,
        'BBA Chapter 20 — Hithpaal Semantic Function Sorting',
        'Reflexive · Iterative · Estimative · Daniel and Ezra',
        ['aramaic', 'bba', 'ch20', 'exercises', 'ch20-hithpaal-function-sort'],
        'ch20-hithpaal-function-sort.pdf',
        out_dir,
    )


# ---------------------------------------------------------------------------
# BBA Ch21 — Haphel vs. Peal Contrast Drill
# ---------------------------------------------------------------------------

class BbaCh21HaphelPealContrastPDF(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each form, identify the stem (Peal or Haphel), '
            'then give Conjugation, PGN, Root, and Translation. '
            'Haphel diagnostic: הַ prefix (perfect); הוֹ prefix for I-yod/hollow roots; '
            'יְהַ prefix (imperfect). Peal has no causative prefix.'
        )
        hdrs = ['#', 'Form', 'Stem (Peal/Haphel)', 'Conjugation', 'PGN', 'Root', 'Translation']
        cr = [0.04, 0.13, 0.11, 0.12, 0.10, 0.12, 0.38]
        hc = [1]
        rows = [
            ['1',  'עֲבַד',         '', '', '', '', ''],
            ['2',  'הַעְבֵּד',      '', '', '', '', ''],
            ['3',  'עָל',           '', '', '', '', ''],
            ['4',  'הֵעַל',         '', '', '', '', ''],
            ['5',  'נְפַל',         '', '', '', '', ''],
            ['6',  'הַפֵּל',        '', '', '', '', ''],
            ['7',  'יְדַע',         '', '', '', '', ''],
            ['8',  'הוֹדַע',        '', '', '', '', ''],
            ['9',  'קוּם',          '', '', '', '', ''],
            ['10', 'הֲקֵים',        '', '', '', '', ''],
            ['11', 'אֲזַל',         '', '', '', '', ''],
            ['12', 'הַנְפֵּק',      '', '', '', '', ''],
            ['13', 'שְׁלַח',        '', '', '', '', ''],
            ['14', 'הַשְׁלֵט',      '', '', '', '', ''],
            ['15', 'קְרָא',         '', '', '', '', ''],
            ['16', 'יְהַחֲוֵה',     '', '', '', '', ''],
            ['17', 'אֲמַר',         '', '', '', '', ''],
            ['18', 'הֲקֵימוּ',      '', '', '', '', ''],
            ['19', 'נְפַקְנָא',     '', '', '', '', ''],
            ['20', 'הוֹדַעְנָּא',   '', '', '', '', ''],
        ]
        ans = [
            ['1',  'עֲבַד',        'Peal',   'Perfect',   '3ms', 'עבד', 'he did / made'],
            ['2',  'הַעְבֵּד',     'Haphel', 'Perfect',   '3ms', 'עבד', 'he caused to do / he made (someone) do'],
            ['3',  'עָל',          'Peal',   'Perfect',   '3ms', 'עלל', 'he entered'],
            ['4',  'הֵעַל',        'Haphel', 'Perfect',   '3ms', 'עלל', 'he brought in / he made (someone) enter'],
            ['5',  'נְפַל',        'Peal',   'Perfect',   '3ms', 'נפל', 'he fell'],
            ['6',  'הַפֵּל',       'Haphel', 'Perfect',   '3ms', 'נפל', 'he caused to fall / he felled'],
            ['7',  'יְדַע',        'Peal',   'Perfect',   '3ms', 'ידע', 'he knew'],
            ['8',  'הוֹדַע',       'Haphel', 'Perfect',   '3ms', 'ידע', 'he made known / he informed'],
            ['9',  'קוּם',         'Peal',   'Perfect',   '3ms', 'קום', 'he arose / stood'],
            ['10', 'הֲקֵים',       'Haphel', 'Perfect',   '3ms', 'קום', 'he caused to stand / he set up'],
            ['11', 'אֲזַל',        'Peal',   'Perfect',   '3ms', 'אזל', 'he went'],
            ['12', 'הַנְפֵּק',     'Haphel', 'Perfect',   '3ms', 'נפק', 'he brought out / he caused to go out'],
            ['13', 'שְׁלַח',       'Peal',   'Perfect',   '3ms', 'שׁלח','he sent'],
            ['14', 'הַשְׁלֵט',     'Haphel', 'Perfect',   '3ms', 'שׁלט','he gave authority / he made to rule'],
            ['15', 'קְרָא',        'Peal',   'Perfect',   '3ms', 'קרא', 'he called / read'],
            ['16', 'יְהַחֲוֵה',    'Haphel', 'Imperfect', '3ms', 'חוה', 'he will declare / he will show'],
            ['17', 'אֲמַר',        'Peal',   'Perfect',   '3ms', 'אמר', 'he said'],
            ['18', 'הֲקֵימוּ',     'Haphel', 'Perfect',   '3mp', 'קום', 'they set up / they caused to stand'],
            ['19', 'נְפַקְנָא',    'Peal',   'Perfect',   '1cp', 'נפק', 'we went out'],
            ['20', 'הוֹדַעְנָּא',  'Haphel', 'Perfect',   '1cp', 'ידע', 'we made known / we informed'],
        ]
        self.add_drill_with_answer_key(hdrs, rows, ans, col_ratios=cr, heb_cols=hc,
                                        section_title='Haphel vs. Peal Contrast Drill — Items 1–20')


def build_bba_ch21_haphel_peal_contrast(out_dir: str = None) -> str:
    return _build_exercise_pdf(
        BbaCh21HaphelPealContrastPDF,
        'BBA Chapter 21 — Haphel vs. Peal Contrast Drill',
        'Causative Haphel vs. Simple Peal · Daniel and Ezra',
        ['aramaic', 'bba', 'ch21', 'exercises', 'ch21-haphel-peal-contrast'],
        'ch21-haphel-peal-contrast.pdf',
        out_dir,
    )
