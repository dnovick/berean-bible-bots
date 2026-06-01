"""Word study: the vice/virtue list of 2 Timothy 3:1-5.

Generates:
  output/reports/nt/lexicon/2tim3-vice-list/
    index.md                      — main page: passage, summary table, obs.
    <slug>/README.md              — one page per term (22 terms)
  output/charts/nt/lexicon/2tim3-vice-list/
    <slug>-nt.png                 — NT distribution (terms with ≥3 NT occ)
    <slug>-lxx.png                — LXX distribution (terms with ≥5 LXX occ)
"""
import matplotlib; matplotlib.use('Agg')  # noqa: E702
import matplotlib.pyplot as plt
from pathlib import Path

from bible_grammar.core import db as _db
from bible_grammar.core.reference import BOOKS

# ── Paths ─────────────────────────────────────────────────────────────────────

REPORT_DIR = Path('output/reports/nt/lexicon/2tim3-vice-list')
CHART_DIR = Path('output/charts/nt/lexicon/2tim3-vice-list')
REPORT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────────────

words = _db.load()
lxx_df = _db.load_lxx()
trans = _db.load_translations()
kjv = trans[trans['translation'] == 'KJV'].copy()

nt = words[words['source'] == 'TAGNT'].copy()

NT_ORDER = [b[0] for b in BOOKS if b[2] == 'NT']
OT_ORDER = [b[0] for b in BOOKS if b[2] == 'OT']
BOOK_NAMES = {b[0]: b[1] for b in BOOKS}

ACCENT_COLOR = '#2166ac'
LXX_COLOR = '#4dac26'


def _kjv(book: str, ch: int, vs: int) -> str:
    row = kjv[(kjv['book_id'] == book) & (kjv['chapter'] == ch) & (kjv['verse'] == vs)]
    return row['text'].values[0] if len(row) else ''


# ── Term catalogue ─────────────────────────────────────────────────────────────
#
# Each entry:
#   strongs, greek, transliteration, gloss, verse, kjv_render,
#   etymology, semantic_note, ot_concept, theological_note
#
# verse = which verse in 2 Tim 3 it appears in
# slug  = derived from greek (set below)

TERMS = [
    {
        'strongs': 'G5467',
        'greek': 'χαλεπός',
        'translit': 'chalepos',
        'gloss': 'harsh, fierce, dangerous',
        'verse': 1,
        'kjv_render': 'perilous',
        'etymology': 'Origin uncertain; used in classical Greek of difficult terrain, '
                     'dangerous situations, and harsh persons.',
        'semantic_note': 'The only two NT uses are 2 Tim 3:1 and Matt 8:28 (the '
                         'Gadarene demoniacs, described as "exceeding fierce"). '
                         'The pairing with violent demoniacs illuminates what '
                         'Paul intends: the last-days moral climate will be '
                         'as dangerous and untameable as men possessed.',
        'ot_concept': 'The LXX uses χαλεπός 11× across 5 books, rendering terms '
                      'for fierce enemies, harsh burdens (Exo 1:14 of Egyptian '
                      'slavery), and dangerous beasts (Deu 32:24).',
        'theological_note': 'The term frames the entire list: Paul is not merely '
                            'describing moral failure but warning of a period of '
                            'social danger — people who are actively harmful.',
    },
    {
        'strongs': 'G5367',
        'greek': 'φίλαυτος',
        'translit': 'philautos',
        'gloss': 'self-loving',
        'verse': 2,
        'kjv_render': 'lovers of their own selves',
        'etymology': 'Compound: φίλος (loving) + αὐτός (self). NT hapax legomenon. '
                     'Aristotle used the cognate φιλαυτία as the root of all vice '
                     '(Eth. Nic. IX.8).',
        'semantic_note': 'Placed first in the list, φίλαυτος appears to anchor the '
                         'catalogue: all the vices that follow are in some sense '
                         'expressions of disordered self-love. The Aristotelian '
                         'background (self-love as the mother of vices) may be '
                         'deliberate.',
        'ot_concept': 'No LXX occurrences. The Hebrew Bible addresses '
                      'self-centredness through concepts like pride (גָּאוֹן) and '
                      'the hardened heart (קְשֵׁה-לֵב), rather than a single term.',
        'theological_note': 'Its position at the head of the list and its '
                            'Aristotelian resonance suggest Paul is offering a '
                            'diagnosis: the last-days vices are symptoms of a '
                            'fundamental inversion — love of self displacing '
                            'love of God (contrast φιλόθεος at the end, v.4).',
    },
    {
        'strongs': 'G5366',
        'greek': 'φιλάργυρος',
        'translit': 'philargyros',
        'gloss': 'money-loving, covetous',
        'verse': 2,
        'kjv_render': 'covetous',
        'etymology': 'Compound: φίλος + ἄργυρος (silver, money). '
                     'The cognate noun φιλαργυρία appears at 1 Tim 6:10 '
                     '("the love of money is a root of all evil").',
        'semantic_note': 'Appears twice in NT (Luk 16:14, where the Pharisees are '
                         'called φιλάργυροι, and here). Luke\'s usage connects '
                         'greed directly to opposition to Jesus\' teaching on '
                         'wealth. The LXX has one instance (Sir 10:8).',
        'ot_concept': 'The OT addresses covetousness through the tenth commandment '
                      '(חָמַד, Exo 20:17) and the prophets\' condemnation of '
                      'dishonest gain (בֶּצַע, Jer 6:13; Eze 22:27).',
        'theological_note': 'Placed immediately after φίλαυτος: love of money is '
                            'the first external symptom of disordered self-love.',
    },
    {
        'strongs': 'G0213',
        'greek': 'ἀλαζών',
        'translit': 'alazon',
        'gloss': 'boastful, swaggering braggart',
        'verse': 2,
        'kjv_render': 'boasters',
        'etymology': 'Classical term for the stock character of the braggart who '
                     'claims more than he possesses. Appears in Rom 1:30 alongside '
                     'ὑπερήφανος, forming the same pair as here.',
        'semantic_note': 'NT uses: Rom 1:30 and 2 Tim 3:2 only. The LXX has no '
                         'occurrences but the cognate ἀλαζονεία (boasting, '
                         'arrogance) appears in Wisdom and Maccabees.',
        'ot_concept': 'Corresponds broadly to Hebrew גָּאָה (to be haughty) and '
                      'רָהַב (to be proud/boastful; Psa 40:4). The prophets '
                      'frequently condemn national and individual boasting '
                      '(Isa 13:11; Jer 48:29).',
        'theological_note': 'ἀλαζών (claiming more than you have) and ὑπερήφανος '
                            '(thinking yourself above others) form a pair: the '
                            'first is the outward display, the second the inward '
                            'disposition.',
    },
    {
        'strongs': 'G5244',
        'greek': 'ὑπερήφανος',
        'translit': 'hyperephanos',
        'gloss': 'proud, arrogant, showing oneself above others',
        'verse': 2,
        'kjv_render': 'proud',
        'etymology': 'Compound: ὑπέρ (over/above) + φαίνομαι (to appear, show '
                     'oneself). Literally "one who shows himself above others."',
        'semantic_note': 'Five NT occurrences across five books; 40 LXX occurrences '
                         'across 12 books — one of the richer terms in the list. '
                         'Consistently listed among the gravest sins: Rom 1:30 '
                         '(alongside ἀλαζών), Luk 1:51 (God scatters the proud), '
                         'Jas 4:6 / 1Pe 5:5 (God opposes the proud — quoting '
                         'Pro 3:34 LXX, where ὑπερηφάνοις renders גֵּאִים).',
        'ot_concept': 'Primary Hebrew equivalents: גָּאֶה / גָּאוֹן (pride, '
                      'haughtiness; Psa 10:2; Pro 8:13; Isa 2:12), and זֵד '
                      '(presumptuous, arrogant; Psa 119:21,51,69). '
                      'Pride is one of the seven things the LORD hates (Pro 6:17).',
        'theological_note': 'The LXX depth (40 occurrences) makes this one of the '
                            'theologically weightiest terms in the list. The '
                            'Magnificat (Luk 1:51) and the Proverbs quotation '
                            '(Jas 4:6) frame ὑπερήφανος as the characteristic '
                            'sin that draws divine opposition.',
    },
    {
        'strongs': 'G0989',
        'greek': 'βλάσφημος',
        'translit': 'blasphemos',
        'gloss': 'blasphemous, slanderous, abusive in speech',
        'verse': 2,
        'kjv_render': 'blasphemers',
        'etymology': 'Compound: βλάπτω (to harm) + φήμη (speech, reputation). '
                     'Denotes speech that damages — whether against God '
                     '(blasphemy in the strict sense) or against people '
                     '(slander, abuse).',
        'semantic_note': 'Five NT occurrences across four books. No LXX occurrences '
                         '(the LXX uses βλασφημέω as a verb but not this '
                         'adjective). In the Pastorals the term spans both '
                         'senses: 1 Tim 1:13 (Paul was a βλάσφημος — a '
                         'blasphemer against God); Tit 2:5 (young women whose '
                         'conduct might cause the word of God to be "blasphemed" '
                         '— i.e., slandered before outsiders).',
        'ot_concept': 'Corresponds to Hebrew גִּדֵּף (to blaspheme, revile; '
                      'Num 15:30; 2Ki 19:6) and חָרַף (to taunt, reproach; '
                      'Psa 44:16; Isa 37:23).',
        'theological_note': 'The ambiguity between "blasphemer" and "slanderer" '
                            'is deliberate: the person who speaks abusively of '
                            'other people is engaged in the same fundamental act '
                            'as the person who blasphemes God — both treat '
                            'the image-bearer as contemptible.',
    },
    {
        'strongs': 'G0545',
        'greek': 'ἀπειθής',
        'translit': 'apeithes',
        'gloss': 'disobedient, unpersuadable',
        'verse': 2,
        'kjv_render': 'disobedient to parents',
        'etymology': 'Alpha-privative + πείθομαι (to be persuaded, to obey). '
                     'Denotes someone who refuses to be persuaded — resistant '
                     'to both argument and authority.',
        'semantic_note': 'Six NT occurrences across five books — the most widely '
                         'distributed alpha-privative in the list. Appears in '
                         'Rom 1:30 (same vice catalogue), Tit 1:16 and 3:3, '
                         'Luk 1:17 (John to turn the disobedient to the wisdom '
                         'of the just), and Act 26:19. No LXX occurrences.',
        'ot_concept': 'Corresponds to Hebrew מֶרִי (rebellion, defiance; Num 17:25; '
                      'Isa 30:9) and סָרַר (stubborn, rebellious; Deu 21:18,20 '
                      'of the rebellious son — the exact context of the '
                      '"disobedient to parents" charge).',
        'theological_note': 'The phrase "disobedient to parents" (γονεῦσιν '
                            'ἀπειθεῖς) echoes the fifth commandment and Deu '
                            '21:18-21. Disobedience to parents was a capital '
                            'offence in the Mosaic law; Paul treats it as a '
                            'mark of the last-days moral collapse.',
    },
    {
        'strongs': 'G0884',
        'greek': 'ἀχάριστος',
        'translit': 'acharistos',
        'gloss': 'ungrateful, unthankful',
        'verse': 2,
        'kjv_render': 'unthankful',
        'etymology': 'Alpha-privative + χάρις (grace, favour, thankfulness). '
                     'NT hapax legomenon (here and Luk 6:35 only).',
        'semantic_note': 'Luk 6:35 uses ἀχάριστος of those to whom God shows '
                         'kindness despite their ingratitude — setting up the '
                         'contrast that Paul exploits: God lavishes grace; '
                         'the last-days person refuses to acknowledge it.',
        'ot_concept': 'No LXX occurrences. The Hebrew Bible addresses ingratitude '
                      'narratively (Israel\'s repeated forgetfulness of God\'s '
                      'acts, Psa 106) rather than through a single term.',
        'theological_note': 'Ingratitude in Paul\'s theology is close to the root '
                            'of pagan sin: Rom 1:21 names failure to give thanks '
                            '(εὐχαρίστησαν) as one of the first steps in moral '
                            'decline. ἀχάριστος names the settled character of '
                            'one who never gives thanks.',
    },
    {
        'strongs': 'G0462',
        'greek': 'ἀνόσιος',
        'translit': 'anosios',
        'gloss': 'unholy, impious',
        'verse': 2,
        'kjv_render': 'unholy',
        'etymology': 'Alpha-privative + ὅσιος (holy, pious, devout). '
                     'NT: only 2 Tim 3:2 and 1 Tim 1:9.',
        'semantic_note': 'In 1 Tim 1:9 ἀνόσιος appears in a list of lawbreakers '
                         'for whom the law was given — paired there with ἀσεβής '
                         '(ungodly). The two Pastoral occurrences frame '
                         'impiety as a characteristic of those outside covenant '
                         'faithfulness. No LXX occurrences.',
        'ot_concept': 'Hebrew חָנֵף (profane, godless; Psa 106:38; Isa 9:17; '
                      'Job 8:13) and רָשָׁע (wicked, ungodly) cover similar '
                      'semantic space.',
        'theological_note': 'Placed at the end of verse 2, ἀνόσιος and ἀχάριστος '
                            'together describe the failure of both vertical '
                            'dimensions: no thankfulness to God, no holiness '
                            'before God.',
    },
    {
        'strongs': 'G0794',
        'greek': 'ἄστοργος',
        'translit': 'astorgos',
        'gloss': 'without natural affection, unloving',
        'verse': 3,
        'kjv_render': 'without natural affection',
        'etymology': 'Alpha-privative + στοργή (natural familial love, '
                     'especially between parents and children). '
                     'Appears in NT only here and Rom 1:31.',
        'semantic_note': 'στοργή (the base term) does not itself appear in the '
                         'NT but is common in classical Greek for the instinctive '
                         'love of family members. Its absence — ἄστοργος — '
                         'describes those in whom even this most basic bond '
                         'has dissolved.',
        'ot_concept': 'No LXX occurrences. The Hebrew Bible speaks of parental '
                      'love through terms like רַחֲמִים (compassion, womb-love; '
                      'Psa 103:13) and the image of a nursing mother '
                      '(Isa 49:15).',
        'theological_note': 'Rom 1:31 places ἄστοργος at the nadir of the '
                            'pagan moral descent — the point where even '
                            'nature\'s own bonds break down. Paul returns '
                            'to it here as a mark of the last-days apostasy '
                            'within the church community.',
    },
    {
        'strongs': 'G0786',
        'greek': 'ἄσπονδος',
        'translit': 'aspondos',
        'gloss': 'irreconcilable, implacable',
        'verse': 3,
        'kjv_render': 'trucebreakers',
        'etymology': 'Alpha-privative + σπονδή (libation, treaty, truce). '
                     'A σπονδή was the drink offering that sealed a treaty; '
                     'ἄσπονδος is one who refuses to enter into any truce '
                     'or cannot be reconciled.',
        'semantic_note': 'NT: only 2 Tim 3:3 and Rom 1:31. The KJV "trucebreaker" '
                         'slightly mistranslates: the term does not mean one who '
                         'breaks an existing truce but one who is unwilling to '
                         'make peace at all — implacable, perpetually at odds.',
        'ot_concept': 'No LXX occurrences. Hebrew שָׁלוֹם (peace, wholeness) '
                      'provides the conceptual background: the ἄσπονδος '
                      'is the one incapable of שָׁלוֹם with others.',
        'theological_note': 'The KJV translation "trucebreaker" has shaped '
                            'much English preaching on this verse, but the '
                            'underlying sense is more radical: not treachery '
                            'toward an existing agreement, but refusal to '
                            'seek peace at all.',
    },
    {
        'strongs': 'G1228',
        'greek': 'διάβολος',
        'translit': 'diabolos',
        'gloss': 'slanderer; the Devil',
        'verse': 3,
        'kjv_render': 'false accusers',
        'etymology': 'Compound: διά (through, across) + βάλλω (to throw). '
                     'Literally "one who throws accusations across." In the '
                     'LXX it translates שָׂטָן (adversary, accuser). In the '
                     'NT it is both a common noun (slanderer) and the proper '
                     'name of the Devil.',
        'semantic_note': '38 NT occurrences across 14 books — the most '
                         'distributed term in the list by far. The majority '
                         'of occurrences are the proper noun (Satan/the Devil); '
                         'the common-noun use (slanderer) appears in 1 Tim 3:11 '
                         '(deaconesses not to be slanderers), Tit 2:3 '
                         '(older women likewise), and here. The LXX has '
                         '22 occurrences, mostly translating שָׂטָן in Job '
                         'and Zechariah.',
        'ot_concept': 'Hebrew שָׂטָן (H7854): adversary, accuser. The three '
                      'main OT passages are Job 1–2 (the heavenly accuser), '
                      'Zec 3:1–2 (accusing Joshua the high priest), and '
                      '1Ch 21:1 (inciting David). The LXX transliterates '
                      'as Σατάν or translates as διάβολος.',
        'theological_note': 'The use of διάβολος as a common noun ("slanderers") '
                            'is not incidental: Paul names the character of the '
                            'Devil (the Accuser) as a human trait of the last '
                            'days. Those who engage in slander take on the '
                            'character of the Adversary.',
    },
    {
        'strongs': 'G0193',
        'greek': 'ἀκρατής',
        'translit': 'akrates',
        'gloss': 'without self-control, intemperate',
        'verse': 3,
        'kjv_render': 'incontinent',
        'etymology': 'Alpha-privative + κράτος (strength, power, control). '
                     'NT hapax legomenon. Aristotle\'s term for the person '
                     'who knows what is right but cannot control themselves '
                     'enough to do it (Eth. Nic. VII).',
        'semantic_note': 'No LXX occurrences. The cognate ἐγκράτεια '
                         '(self-control) is a fruit of the Spirit (Gal 5:23) '
                         'and a virtue the Pastorals commend for elders '
                         '(Tit 1:8). ἀκρατής is its direct opposite.',
        'ot_concept': 'Hebrew חֲסַר לֵב (lacking sense/heart, Pro 6:32; 7:7) '
                      'and פָּרַע (unrestrained, Exo 32:25 of Israel at the '
                      'golden calf) cover similar ground.',
        'theological_note': 'The Aristotelian background is worth noting: '
                            'classical virtue ethics considered ἀκρασία '
                            '(incontinence) a fundamental character defect. '
                            'Paul adopts the term but locates its remedy '
                            'not in philosophical discipline but in the '
                            'Spirit\'s fruit of ἐγκράτεια.',
    },
    {
        'strongs': 'G0434',
        'greek': 'ἀνήμερος',
        'translit': 'anemeros',
        'gloss': 'savage, fierce, untamed',
        'verse': 3,
        'kjv_render': 'fierce',
        'etymology': 'Alpha-privative + ἥμερος (tame, gentle, civilised). '
                     'NT hapax legomenon. Used in classical Greek of wild '
                     'animals and uncivilised peoples.',
        'semantic_note': 'No LXX occurrences. The contrast with ἥμερος '
                         '(tame/gentle) is vivid: the term pictures people '
                         'who have reverted to the condition of undomesticated '
                         'animals — the opposite of the civil and peaceable '
                         'community Paul commends.',
        'ot_concept': 'Hebrew פֶּרֶא (wild donkey, a symbol of untamed '
                      'independence; Gen 16:12 of Ishmael; Job 39:5) '
                      'shares the imagery of untamed wildness.',
        'theological_note': 'The sequence ἀκρατεῖς, ἀνήμεροι, ἀφιλάγαθοι '
                            'traces a descent: losing self-control leads to '
                            'savagery, which leads to hostility to everything '
                            'good.',
    },
    {
        'strongs': 'G0865',
        'greek': 'ἀφιλάγαθος',
        'translit': 'aphilagathos',
        'gloss': 'not loving good, hostile to goodness',
        'verse': 3,
        'kjv_render': 'despisers of those that are good',
        'etymology': 'Alpha-privative + φίλος (loving) + ἀγαθός (good). '
                     'NT hapax legomenon. Its positive counterpart '
                     'φιλάγαθος (lover of good) appears in Tit 1:8 as '
                     'a required quality for overseers.',
        'semantic_note': 'No LXX occurrences. The KJV "despisers of those '
                         'that are good" over-translates: the term simply '
                         'means "not loving what is good" — the absence '
                         'of love for goodness itself, not necessarily '
                         'active hatred.',
        'ot_concept': 'Hebrew שֹׂנֵא טוֹב (hating good; Mic 3:2) and '
                      'מָאַס (to reject, despise; Amo 5:10 "they hate '
                      'the one who reproves") cover similar ground.',
        'theological_note': 'Standing at the mirror image of φιλάγαθος '
                            '(Tit 1:8), this term marks the final inversion: '
                            'the elder is to love goodness; the last-days '
                            'person is constitutionally indifferent or '
                            'hostile to it.',
    },
    {
        'strongs': 'G4273',
        'greek': 'προδότης',
        'translit': 'prodotes',
        'gloss': 'traitor, betrayer',
        'verse': 4,
        'kjv_render': 'traitors',
        'etymology': 'From προδίδωμι (to hand over, betray): πρό (before/forth) '
                     '+ δίδωμι (to give). The one who "gives someone over" '
                     'to their enemies.',
        'semantic_note': 'Three NT occurrences: Luk 6:16 (Judas called προδότης '
                         '— the only NT individual named a traitor), Act 7:52 '
                         '(those who betrayed and killed the prophets), and '
                         'here. Four LXX occurrences across 2 books.',
        'ot_concept': 'Hebrew בֹּגֵד (treacherous one, traitor; Psa 119:158; '
                      'Isa 24:16; Hab 1:13) — from בָּגַד (to act '
                      'treacherously, to cover/wrap, hence to hide one\'s '
                      'true intentions).',
        'theological_note': 'The only named NT traitor is Judas (Luk 6:16). '
                            'Paul\'s use here connects the church\'s '
                            'last-days experience to the betrayal of the '
                            'prophets (Act 7:52): a pattern of those inside '
                            'the covenant community handing over the faithful.',
    },
    {
        'strongs': 'G4312',
        'greek': 'προπετής',
        'translit': 'propetes',
        'gloss': 'rash, reckless, headlong',
        'verse': 4,
        'kjv_render': 'heady',
        'etymology': 'Compound: πρό (forward) + πίπτω (to fall). '
                     'Literally "falling forward" — the one who rushes ahead '
                     'without thinking.',
        'semantic_note': 'Two NT occurrences: Act 19:36 (the Ephesian town clerk '
                         'warns the crowd not to act προπετῶς — rashly) and '
                         'here. Three LXX occurrences.',
        'ot_concept': 'Hebrew פָּזַז (to act rashly, to leap; 2Sa 6:16 of '
                      'David\'s dancing; Gen 49:4 of Reuben\'s rashness) '
                      'and מִבְהָל (hasty, rash; Pro 29:20).',
        'theological_note': 'The KJV "heady" (headstrong, wilful) captures '
                            'the volitional aspect. προπετής is recklessness '
                            'in action — the behavioural complement of '
                            'τετυφωμένοι (inflated in mind).',
    },
    {
        'strongs': 'G5187',
        'greek': 'τυφόω',
        'translit': 'typhoo',
        'gloss': 'to be puffed up with conceit, to be blinded by pride',
        'verse': 4,
        'kjv_render': 'highminded',
        'etymology': 'From τῦφος (smoke, mist; hence, delusion, conceit). '
                     'The perfect passive participle here (τετυφωμένοι) '
                     'describes those who have been — and remain — inflated '
                     'with pride.',
        'semantic_note': 'Three NT occurrences, all Pauline: 1 Tim 3:6 '
                         '(a new elder must not be τυφωθῇ, "puffed up"), '
                         '1 Tim 6:4 (false teachers are τετύφωται), and here. '
                         'No LXX occurrences.',
        'ot_concept': 'Hebrew גָּבַהּ (to be high, exalted; in moral sense, '
                      'to be haughty; Pro 16:5; Eze 28:2,5) and זָדוֹן '
                      '(presumptuousness, arrogance; Pro 21:24).',
        'theological_note': 'The smoke/mist imagery of τῦφος is apt: the '
                            'conceited person\'s self-assessment is a cloud '
                            'that obscures reality. Paul uses the word '
                            'consistently of those in leadership positions '
                            'whose pride disqualifies them.',
    },
    {
        'strongs': 'G5369',
        'greek': 'φιλήδονος',
        'translit': 'philedonos',
        'gloss': 'pleasure-loving',
        'verse': 4,
        'kjv_render': 'lovers of pleasures',
        'etymology': 'Compound: φίλος + ἡδονή (pleasure, enjoyment). '
                     'NT hapax legomenon.',
        'semantic_note': 'No LXX occurrences. The cognate ἡδονή appears '
                         'in Jas 4:1,3 (pleasures that war in the members) '
                         'and 2Pe 2:13 (pleasure in daylight carousing). '
                         'φιλήδονος stands in direct antithesis to '
                         'φιλόθεος in the same verse — the '
                         'two loves are mutually exclusive.',
        'ot_concept': 'Hebrew תַּאֲוָה (desire, craving; Num 11:4 of the '
                      'people\'s craving in the desert; Pro 21:25,26) '
                      'and עֶדְנָה (luxury, pleasure; Gen 18:12).',
        'theological_note': 'The phrase "lovers of pleasure rather than lovers '
                            'of God" is the sharpest antithesis in the list — '
                            'two compound adjectives placed side by side with '
                            'μᾶλλον ἢ (more than). It crystallises the entire '
                            'catalogue: self-love (v.2) has displaced '
                            'God-love (v.4).',
    },
    {
        'strongs': 'G5377',
        'greek': 'φιλόθεος',
        'translit': 'philotheos',
        'gloss': 'God-loving',
        'verse': 4,
        'kjv_render': 'lovers of God',
        'etymology': 'Compound: φίλος + θεός (God). NT hapax legomenon. '
                     'Appears in the phrase φιλήδονοι μᾶλλον ἢ φιλόθεοι '
                     '(lovers of pleasure more than lovers of God).',
        'semantic_note': 'The single NT occurrence makes this technically '
                         'a hapax but it functions as the pivot of the entire '
                         'list: by naming what is absent (love of God), '
                         'Paul reveals the theological diagnosis of all '
                         'the preceding vices. No LXX occurrences.',
        'ot_concept': 'The command to love God (אָהַב + יְהוָה) is central '
                      'to the Shema (Deu 6:5) and the summary of the law. '
                      'φιλόθεος frames the 2 Tim 3 vices as failures of '
                      'this primary commandment.',
        'theological_note': 'φιλόθεος answers φίλαυτος (v.2): the list opens '
                            'with self-love and closes with its antithesis, '
                            'God-love. The entire catalogue is framed as the '
                            'consequence of inverting the great commandment.',
    },
    {
        'strongs': 'G3446',
        'greek': 'μόρφωσις',
        'translit': 'morphosis',
        'gloss': 'outward form, semblance, shape',
        'verse': 5,
        'kjv_render': 'form',
        'etymology': 'From μορφόω (to form, shape) — related to μορφή '
                     '(form, appearance). μόρφωσις denotes the external '
                     'shape or outward appearance, with no implication of '
                     'inner reality.',
        'semantic_note': 'Two NT occurrences: 2 Tim 3:5 and Rom 2:20 '
                         '(the Jew who has "the form of knowledge and truth '
                         'in the law"). In both cases μόρφωσις is the '
                         'external form without the inner substance.',
        'ot_concept': 'No LXX occurrences. The Hebrew Bible uses '
                      'צֶלֶם (image, form; Gen 1:26–27) and תָּאַר '
                      '(outward appearance; 1Sa 16:7 — "man looks on the '
                      'outward appearance").',
        'theological_note': '"Having the form of godliness but denying its '
                            'power" (v.5) is the culminating charge: all the '
                            'preceding vices are not from obviously secular '
                            'people but from those who maintain a religious '
                            'veneer. This verse is the key to why Paul has '
                            'listed these vices — they describe people inside '
                            'the church community, not outside it.',
    },
    {
        'strongs': 'G2150',
        'greek': 'εὐσέβεια',
        'translit': 'eusebeia',
        'gloss': 'godliness, piety, reverence',
        'verse': 5,
        'kjv_render': 'godliness',
        'etymology': 'Compound: εὖ (well, rightly) + σέβομαι (to revere, '
                     'worship). Denotes the whole orientation of life toward '
                     'God — comprehensive practical piety.',
        'semantic_note': '15 NT occurrences across 5 books — the richest '
                         'positive term in the list. Concentrated heavily '
                         'in the Pastorals (1 Tim: 8×, 2 Tim: 1×, Tit: 1×) '
                         'and 2 Peter (4×). 57 LXX occurrences across 8 books. '
                         'The cognate εὐσεβής (pious, godly) and verb '
                         'εὐσεβέω add further occurrences.',
        'ot_concept': 'Hebrew יִרְאַת יְהוָה (fear of the LORD — the '
                      'comprehensive term for covenant faithfulness and '
                      'practical holiness; Pro 1:7; 9:10; Psa 111:10). '
                      'The LXX frequently renders יִרְאָה with εὐσέβεια, '
                      'especially in wisdom literature.',
        'theological_note': 'εὐσέβεια is the Pastorals\' signature virtue — '
                            'the word that sums up what the false teachers '
                            'lack (1 Tim 6:5) and what Timothy is to pursue '
                            '(1 Tim 6:11). Its appearance here in μόρφωσιν '
                            'εὐσεβείας ("form of godliness") is devastating: '
                            'the very word Paul uses for genuine Christian '
                            'character is reduced to an empty shell.',
    },
]

# Derive slugs from transliteration
for t in TERMS:
    t['slug'] = str(t['translit']).lower().replace('ō', 'o').replace('ē', 'e')


# ── Chart helpers ──────────────────────────────────────────────────────────────

def _chart_nt(term: dict) -> Path | None:
    """Bar chart of NT occurrences by book. Returns path or None if too few."""
    hits = nt[nt['strongs'].str.contains(term['strongs'], na=False)]
    if len(hits) < 3:
        return None
    cnt = hits.groupby('book_id').size().reindex(NT_ORDER, fill_value=0)
    books = [b for b in NT_ORDER if cnt[b] > 0]
    vals = [cnt[b] for b in books]

    fig, ax = plt.subplots(figsize=(max(5, len(books) * 0.9), 4))
    ax.bar(range(len(books)), vals, color=ACCENT_COLOR, edgecolor='white', linewidth=0.4)
    ax.set_xticks(range(len(books)))
    ax.set_xticklabels(books, rotation=45, ha='right', fontsize=9)
    ax.set_ylabel('Occurrences')
    ax.set_title(
        f'{term["greek"]} ({term["strongs"]}) — NT Distribution',
        fontsize=11, fontweight='bold',
    )
    for i, v in enumerate(vals):
        ax.text(i, v + 0.05, str(v), ha='center', fontsize=8)
    fig.tight_layout()
    path = CHART_DIR / f'{term["slug"]}-nt.png'
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Chart: {path}')
    return path


def _chart_lxx(term: dict) -> Path | None:
    """Bar chart of LXX occurrences by OT book. Returns path or None if too few."""
    hits = lxx_df[(lxx_df['strongs'] == term['strongs']) & (~lxx_df['is_deuterocanon'])]
    if len(hits) < 5:
        return None
    cnt = hits.groupby('book_id').size().reindex(OT_ORDER, fill_value=0)
    books = [b for b in OT_ORDER if cnt[b] > 0]
    vals = [cnt[b] for b in books]

    fig, ax = plt.subplots(figsize=(max(5, len(books) * 0.9), 4))
    ax.bar(range(len(books)), vals, color=LXX_COLOR, edgecolor='white', linewidth=0.4)
    ax.set_xticks(range(len(books)))
    ax.set_xticklabels(books, rotation=45, ha='right', fontsize=9)
    ax.set_ylabel('Occurrences')
    ax.set_title(
        f'{term["greek"]} ({term["strongs"]}) — LXX Distribution (Canonical OT)',
        fontsize=11, fontweight='bold',
    )
    for i, v in enumerate(vals):
        ax.text(i, v + 0.05, str(v), ha='center', fontsize=8)
    fig.tight_layout()
    path = CHART_DIR / f'{term["slug"]}-lxx.png'
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Chart: {path}')
    return path


# ── NT occurrence table helper ─────────────────────────────────────────────────

def _nt_occurrence_table(term: dict) -> list:
    """Return markdown table lines for all NT occurrences with KJV text."""
    hits = nt[nt['strongs'].str.contains(term['strongs'], na=False)].copy()
    if len(hits) == 0:
        return ['*No NT occurrences outside 2 Tim 3.*']
    lines = ['| Reference | Greek form | KJV text |', '|---|---|---|']
    for _, r in hits.sort_values(['book_id', 'chapter', 'verse'],
                                 key=lambda s: s.map(
                                     lambda v: NT_ORDER.index(v)
                                     if v in NT_ORDER else 99
                                 ) if s.name == 'book_id' else s).iterrows():
        ref = f'{r["book_id"]} {r["chapter"]}:{r["verse"]}'
        kjv_text = _kjv(r['book_id'], r['chapter'], r['verse'])
        kjv_short = kjv_text[:110] + ('…' if len(kjv_text) > 110 else '')
        lines.append(f'| {ref} | {r["word"]} | {kjv_short} |')
    return lines


def _lxx_occurrence_table(term: dict) -> list:
    """Return markdown table lines for LXX occurrences (canonical only)."""
    hits = lxx_df[(lxx_df['strongs'] == term['strongs'])
                  & (~lxx_df['is_deuterocanon'])].copy()
    if len(hits) == 0:
        return ['*No canonical LXX occurrences.*']
    lines = ['| Reference | LXX form |', '|---|---|']
    for _, r in hits.sort_values(['book_id', 'chapter', 'verse'],
                                 key=lambda s: s.map(
                                     lambda v: OT_ORDER.index(v)
                                     if v in OT_ORDER else 99
                                 ) if s.name == 'book_id' else s).iterrows():
        ref = f'{r["book_id"]} {r["chapter"]}:{r["verse"]}'
        lines.append(f'| {ref} | {r["word"]} |')
    return lines


# ── Per-term page ──────────────────────────────────────────────────────────────

def _build_term_page(term: dict, nt_chart: Path | None, lxx_chart: Path | None) -> None:
    """Write output/reports/nt/lexicon/2tim3-vice-list/<slug>/README.md."""
    slug = term['slug']
    term_dir = REPORT_DIR / slug
    term_dir.mkdir(exist_ok=True)

    hits_nt = nt[nt['strongs'].str.contains(term['strongs'], na=False)]
    hits_lxx = lxx_df[(lxx_df['strongs'] == term['strongs'])
                      & (~lxx_df['is_deuterocanon'])]
    nt_occ = len(hits_nt)
    nt_bks = hits_nt['book_id'].nunique()
    lxx_occ = len(hits_lxx)

    # Relative path from term subdir back to charts
    chart_rel = '../../../../../../charts/nt/lexicon/2tim3-vice-list'

    lines = [
        f'# {term["greek"]} ({term["strongs"]}) — {term["gloss"]}',
        '',
        '*Part of the [2 Timothy 3:1–5 Vice List study](../index.md)*',
        '',
        '---',
        '',
        '## Contents',
        '',
        '- [Overview](#overview)',
        '- [Etymology and Semantic Range](#etymology-and-semantic-range)',
        '- [OT / LXX Background](#ot--lxx-background)',
        '- [NT Distribution](#nt-distribution)',
        '- [Theological Note](#theological-note)',
        '- [NT Occurrences](#nt-occurrences)',
    ]
    if lxx_occ > 0:
        lines.append('- [LXX Occurrences (Canonical)](#lxx-occurrences-canonical)')
    lines += [
        '',
        '---',
        '',
        '## Overview',
        '',
        '| Field | Value |',
        '|---|---|',
        f'| Strong\'s | {term["strongs"]} |',
        f'| Greek | {term["greek"]} |',
        f'| Transliteration | {term["translit"]} |',
        f'| Gloss | {term["gloss"]} |',
        f'| 2 Tim 3 verse | 3:{term["verse"]} |',
        f'| KJV rendering | "{term["kjv_render"]}" |',
        f'| NT occurrences | {nt_occ} ({nt_bks} book{"s" if nt_bks != 1 else ""}) |',
        f'| LXX occurrences (canonical) | {lxx_occ} |',
        '',
        '---',
        '',
        '## Etymology and Semantic Range',
        '',
        term['etymology'],
        '',
        term['semantic_note'],
        '',
        '---',
        '',
        '## OT / LXX Background',
        '',
        term['ot_concept'],
        '',
    ]

    if lxx_occ > 0:
        if lxx_chart:
            lines += [
                f'![LXX distribution]({chart_rel}/{slug}-lxx.png)',
                '',
            ]
        lines += _lxx_occurrence_table(term) + ['']

    lines += [
        '---',
        '',
        '## NT Distribution',
        '',
    ]
    if nt_chart:
        lines += [
            f'![NT distribution]({chart_rel}/{slug}-nt.png)',
            '',
        ]
    lines += [
        '---',
        '',
        '## Theological Note',
        '',
        term['theological_note'],
        '',
        '---',
        '',
        '## NT Occurrences',
        '',
    ] + _nt_occurrence_table(term) + ['']

    path = term_dir / 'README.md'
    path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'  Page: {path}')


# ── Main index page ────────────────────────────────────────────────────────────

def _build_index() -> None:
    """Write output/reports/nt/lexicon/2tim3-vice-list/index.md."""

    # Summary table rows
    table_rows = []
    for t in TERMS:
        hits_nt = nt[nt['strongs'].str.contains(t['strongs'], na=False)]
        hits_lxx = lxx_df[(lxx_df['strongs'] == t['strongs'])
                          & (~lxx_df['is_deuterocanon'])]
        nt_occ = len(hits_nt)
        lxx_occ = len(hits_lxx)
        hapax = ' ★' if nt_occ == 1 else ''
        table_rows.append(
            f'| 3:{t["verse"]} | [{t["greek"]}]({t["slug"]}/README.md) '
            f'| {t["strongs"]} | {t["gloss"]} '
            f'| {nt_occ}{hapax} | {lxx_occ or "—"} |'
        )

    lines = [
        '# 2 Timothy 3:1–5 — Vice List Word Study',
        '',
        '*Build script: [scripts/nt/lexicon/2tim3-vice-list/'
        'build_2tim3_vice_list.py]'
        '(../../../../../scripts/nt/lexicon/2tim3-vice-list/'
        'build_2tim3_vice_list.py)*',
        '',
        '---',
        '',
        '## Contents',
        '',
        '- [The Passage](#the-passage)',
        '- [Key Observations](#key-observations)',
        '- [Term Catalogue](#term-catalogue)',
        '- [Structural Analysis](#structural-analysis)',
        '',
        '---',
        '',
        '## The Passage',
        '',
        '> *"This know also, that in the last days perilous times shall come.*',
        '> *For men shall be lovers of their own selves, covetous, boasters, proud,*',
        '> *blasphemers, disobedient to parents, unthankful, unholy,*',
        '> *Without natural affection, trucebreakers, false accusers, incontinent,*',
        '> *fierce, despisers of those that are good,*',
        '> *Traitors, heady, highminded, lovers of pleasures more than lovers of God;*',
        '> *Having a form of godliness, but denying the power thereof:*',
        '> *from such turn away."* — 2 Timothy 3:1–5 (KJV)',
        '',
        '---',
        '',
        '## Key Observations',
        '',
        '### 1. The list is a diagnosis, not merely a description',
        '',
        'Paul does not present these as the vices of pagans outside the church. '
        'Verse 5 ("having a form of godliness") makes explicit that he is '
        'describing people who maintain a religious appearance — those inside '
        'the community of faith. The list is a warning about internal corruption, '
        'not external threat.',
        '',
        '### 2. φίλαυτος and φιλόθεος form a deliberate frame',
        '',
        'The list opens with φίλαυτος (self-loving, v.2) and closes with '
        'φιλήδονοι μᾶλλον ἢ φιλόθεοι (lovers of pleasure more than lovers of '
        'God, v.4). The bookends are two compound "φίλ-" adjectives on opposite '
        'sides of the great commandment. All 18 vices between them are '
        'expressions of disordered love — love of self where love of God '
        'should be.',
        '',
        '### 3. Nine of the 22 terms are NT hapax legomena',
        '',
        'φίλαυτος, ἀκρατής, ἀνήμερος, ἀφιλάγαθος, φιλήδονος, φιλόθεος, '
        'and several others appear nowhere else in the NT. The concentration '
        'of rare vocabulary in a single passage suggests Paul may be drawing '
        'on a traditional vice catalogue — a form well-attested in Hellenistic '
        'moral philosophy and in Jewish literature (1QS, Didache) — and '
        'adapting it for the Pastorals.',
        '',
        '### 4. The alpha-privative terms cluster together',
        '',
        'Six consecutive terms in vv.2–3 begin with alpha-privative (ἀ-): '
        'ἀχάριστοι, ἀνόσιοι, ἄστοργοι, ἄσπονδοι, ἀκρατεῖς, ἀνήμεροι. '
        'This is a rhetorical device: each term names the absence of a virtue '
        '(gratitude, holiness, family love, peaceability, self-control, '
        'civilised behaviour). The string of negations describes people '
        'defined by what they lack.',
        '',
        '### 5. διάβολος (v.3) is theologically charged',
        '',
        'Translated "false accusers" (KJV), διάβολος is the standard NT term '
        'for the Devil. Paul\'s use of it as a common noun for slanderers '
        '(as also in 1 Tim 3:11 and Tit 2:3) implies that slanderous humans '
        'take on the characteristic work of the Accuser. The last-days community '
        'produces people who, in their speech, act as the Devil acts.',
        '',
        '### 6. The LXX depth varies dramatically across the list',
        '',
        'εὐσέβεια (57 LXX occ), ὑπερήφανος (40), and χαλεπός (11) have '
        'significant LXX presence and rich Hebrew OT backgrounds. '
        'Most of the alpha-privative terms and the φίλ- compounds have '
        'no LXX presence at all — they are Greek coinages addressing vices '
        'that the Hebrew vocabulary tended to handle differently '
        '(through narrative, law, or wisdom literature rather than '
        'compound adjectives).',
        '',
        '### 7. εὐσέβεια reduced to μόρφωσις is the rhetorical climax',
        '',
        'εὐσέβεια is the Pastorals\' signature positive term (15 NT occurrences, '
        '8 in 1 Timothy alone). Its appearance here in the phrase '
        '"form of εὐσέβεια" is the sharpest irony in the letter: the very '
        'word Paul uses throughout the Pastorals for genuine godliness '
        'is here drained of content, reduced to a shell. The catalogue '
        'culminates not in outright atheism but in pious fraud.',
        '',
        '---',
        '',
        '## Term Catalogue',
        '',
        '★ = NT hapax legomenon',
        '',
        '| Verse | Term | Strongs | Gloss | NT occ | LXX occ |',
        '|---|---|---|---|---|---|',
    ] + table_rows + [
        '',
        '---',
        '',
        '## Structural Analysis',
        '',
        'The 22 terms (including χαλεπός in v.1 and εὐσέβεια/μόρφωσις in v.5) '
        'can be grouped by grammatical form and rhetorical function:',
        '',
        '**φίλ- compounds** (disordered love):',
        'φίλαυτος · φιλάργυρος · φιλήδονος · φιλόθεος',
        '',
        '**Alpha-privative negations** (absence of virtue):',
        'ἀχάριστος · ἀνόσιος · ἄστοργος · ἄσπονδος · ἀκρατής · ἀνήμερος · ἀφιλάγαθος',
        '',
        '**Pride / self-elevation**:',
        'ἀλαζών · ὑπερήφανος · τετυφωμένοι',
        '',
        '**Speech sins**:',
        'βλάσφημος · διάβολος',
        '',
        '**Action / relational sins**:',
        'ἀπειθής · προδότης · προπετής',
        '',
        '**The framing terms** (v.1 and v.5):',
        'χαλεπός (sets the tone) · μόρφωσις εὐσεβείας (the devastating conclusion)',
        '',
        '---',
        '',
    ]

    path = REPORT_DIR / 'index.md'
    path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Index: {path}')


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    for term in TERMS:
        print(f'\n{term["greek"]} ({term["strongs"]})')
        nt_chart = _chart_nt(term)
        lxx_chart = _chart_lxx(term)
        _build_term_page(term, nt_chart, lxx_chart)
    _build_index()
    print('\nDone.')
