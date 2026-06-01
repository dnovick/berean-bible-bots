"""Build 1 Peter 2:1 — "Lay Aside" Vice List word study.

Five terms commanded to be put off in 1 Peter 2:1:
  κακία (G2549) — malice / evil
  δόλος (G1388) — deceit / guile
  ὑπόκρισις (G5272) — hypocrisy
  φθόνος (G5355) — envy
  καταλαλιά (G2636) — slander / evil speaking

Generates:
  output/reports/nt/lexicon/1pet2-vice-list/
    index.md              — main page: passage, key observations, term catalogue
    <slug>/README.md      — one page per term (5 terms)
  output/charts/nt/lexicon/1pet2-vice-list/
    <slug>-nt.png         — NT distribution bar chart (where sufficient data)
  output/reports/nt/lexicon/1pet2-vice-list/
    1pet2-vice-list.csv   — raw occurrence data
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, '.')
from src.bible_grammar.core import db as _db  # noqa: E402

REPORT_DIR = Path('output/reports/nt/lexicon/1pet2-vice-list')
CHART_DIR = Path('output/charts/nt/lexicon/1pet2-vice-list')
REPORT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────────────

_words = _db.load()
_lxx_df = _db.load_lxx()
_trans = _db.load_translations()
_kjv = _trans[_trans['translation'] == 'KJV'].copy()

nt = _words[_words['source'] == 'TAGNT'].copy()
ot = _words[_words['source'] == 'TAHOT'].copy()

NT_BOOK_ORDER = [
    'Mat', 'Mrk', 'Luk', 'Jhn', 'Act', 'Rom', '1Co', '2Co', 'Gal', 'Eph',
    'Php', 'Col', '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm', 'Heb',
    'Jas', '1Pe', '2Pe', '1Jn', '2Jn', '3Jn', 'Jud', 'Rev',
]
NT_BOOK_NAMES = {
    'Mat': 'Matthew', 'Mrk': 'Mark', 'Luk': 'Luke', 'Jhn': 'John',
    'Act': 'Acts', 'Rom': 'Romans', '1Co': '1 Cor', '2Co': '2 Cor',
    'Gal': 'Galatians', 'Eph': 'Ephesians', 'Php': 'Philippians',
    'Col': 'Colossians', '1Th': '1 Thess', '2Th': '2 Thess',
    '1Ti': '1 Tim', '2Ti': '2 Tim', 'Tit': 'Titus', 'Phm': 'Philemon',
    'Heb': 'Hebrews', 'Jas': 'James', '1Pe': '1 Peter', '2Pe': '2 Peter',
    '1Jn': '1 John', '2Jn': '2 John', '3Jn': '3 John', 'Jud': 'Jude',
    'Rev': 'Revelation',
}
OT_BOOK_NAMES = {
    'Gen': 'Genesis', 'Exo': 'Exodus', 'Lev': 'Leviticus', 'Num': 'Numbers',
    'Deu': 'Deuteronomy', 'Jos': 'Joshua', 'Jdg': 'Judges', 'Rut': 'Ruth',
    '1Sa': '1 Samuel', '2Sa': '2 Samuel', '1Ki': '1 Kings', '2Ki': '2 Kings',
    '1Ch': '1 Chronicles', '2Ch': '2 Chronicles', 'Ezr': 'Ezra',
    'Neh': 'Nehemiah', 'Est': 'Esther', 'Job': 'Job', 'Psa': 'Psalms',
    'Pro': 'Proverbs', 'Ecc': 'Ecclesiastes', 'Sng': 'Song', 'Isa': 'Isaiah',
    'Jer': 'Jeremiah', 'Lam': 'Lamentations', 'Ezk': 'Ezekiel', 'Dan': 'Daniel',
    'Hos': 'Hosea', 'Jol': 'Joel', 'Amo': 'Amos', 'Oba': 'Obadiah',
    'Jon': 'Jonah', 'Mic': 'Micah', 'Nam': 'Nahum', 'Hab': 'Habakkuk',
    'Zep': 'Zephaniah', 'Hag': 'Haggai', 'Zec': 'Zechariah', 'Mal': 'Malachi',
}


def _kjv_verse(book: str, ch: int, vs: int) -> str:
    row = _kjv[
        (_kjv['book_id'] == book) & (_kjv['chapter'] == ch) & (_kjv['verse'] == vs)
    ]
    t = row['text'].values[0] if len(row) else ''
    return (t[:120] + '…') if len(t) > 120 else t


def _get_heb_root(s: str) -> str:
    if not isinstance(s, str):
        return ''
    m = re.search(r'\{(H\d+)[A-Z]?\}', s)
    return m.group(1) if m else ''


# ── Term catalogue ─────────────────────────────────────────────────────────────

TERMS = [
    {
        'strongs': 'G2549',
        'greek': 'κακία',
        'translit': 'kakia',
        'gloss': 'malice, evil, wickedness',
        'kjv_render': 'malice',
        'heb_roots': ['H7451'],
        'etymology': (
            'From κακός (bad, evil). The most general term in the list, covering '
            'the full spectrum of moral evil — both as inner disposition and outward act. '
            'The underlying κακ- root is one of the oldest and most productive in Greek.'
        ),
        'semantic_note': (
            'The NT deploys κακία across a wide range: from specific "malice" or '
            'ill-will toward others (Eph 4:31; Col 3:8) to general "wickedness" '
            '(Acts 8:22; Rom 1:29) and even "trouble / misfortune" (Matt 6:34, '
            '"sufficient unto the day is the evil thereof"). This breadth makes it '
            'the natural head of Peter\'s list: κακία is the root disposition from '
            'which the other four vices spring.'
        ),
        'ot_concept': (
            'The LXX uses κακία 110× in canonical books — the second-most common '
            'rendering of Hebrew רַע / רָעָה (H7451, 662× in OT), the broadest '
            'Hebrew term for evil in all its forms. The LXX concentration is '
            'heaviest in narrative books (1 Sam 15×, 1 Kgs 10×, Judges 8×) '
            'where κακία describes the evil of apostasy, idolatry, and moral '
            'failure. The Hebrew root carries both the sense of moral evil and '
            'the consequent harm it produces — a fusion the Greek κακία '
            'preserves.'
        ),
        'theological_note': (
            'Peter places κακία first, making it the genus from which the other '
            'four vices grow. Its position mirrors its function: malice is not '
            'one vice among equals but the soil in which all the others take root. '
            'The command to "lay aside" (ἀποθέμενοι) κακία is echoed verbatim in '
            'Eph 4:31, Col 3:8, and Jas 1:21 — a shared early-church baptismal '
            'formula for the moral break from the old life.'
        ),
    },
    {
        'strongs': 'G1388',
        'greek': 'δόλος',
        'translit': 'dolos',
        'gloss': 'deceit, guile, treachery',
        'kjv_render': 'guile',
        'heb_roots': ['H4820', 'H7423'],
        'etymology': (
            'From δέλω (to trap or snare). Originally denoted a lure or bait used '
            'to trap animals; extended to any cunning trick or calculated deception. '
            'The image is of concealed intent — the predator\'s bait hidden beneath '
            'an innocent appearance.'
        ),
        'semantic_note': (
            'δόλος appears in NT vice lists (Rom 1:29; Mark 7:22) and describes '
            'the plot to arrest Jesus (Matt 26:4; Mark 14:1, "take Jesus by δόλῳ"). '
            'Jesus calls Nathanael "an Israelite in whom is no δόλος" (John 1:47), '
            'consciously echoing Ps 32:2 LXX ("in whose spirit there is no δόλος"). '
            'The term thus spans the full range from interpersonal deception to '
            'explicit conspiracy.'
        ),
        'ot_concept': (
            'The LXX uses δόλος 34× in canonical books, primarily rendering Hebrew '
            'מִרְמָה (H4820, deceit / fraud, 39× OT) and רְמִיָּה (H7423, treachery / '
            'slackness, 15× OT). Both Hebrew nouns carry the sense of calculated '
            'dishonesty — deliberately misleading another. The Psalms and Proverbs '
            'are the main OT loci (8 and 7 LXX occurrences respectively). '
            'Notably, Ps 34:13 LXX — "keep your tongue from evil and your lips '
            'from speaking δόλον" — is directly quoted by Peter at 3:10.'
        ),
        'theological_note': (
            'δόλος is the most exegetically rich term in 1 Pet 2:1 because Peter '
            'returns to it two verses later. At 2:22 he quotes Isa 53:9 LXX: '
            '"neither was any δόλος found in his mouth" — applied to Christ\'s '
            'sinlessness. This makes Christ\'s freedom from guile the explicit '
            'model for the community\'s behavior commanded in 2:1. The '
            'juxtaposition is striking: the readers are to lay aside δόλος (2:1) '
            'because their Lord never had it (2:22). The Suffering Servant\'s '
            'guileless mouth becomes the paradigm for the new community\'s speech.'
        ),
    },
    {
        'strongs': 'G5272',
        'greek': 'ὑπόκρισις',
        'translit': 'hypokrisis',
        'gloss': 'hypocrisy, dissimulation, play-acting',
        'kjv_render': 'hypocrisies',
        'heb_roots': ['H2612'],
        'etymology': (
            'From ὑποκρίνομαι (to play a part on stage, to answer from under a mask). '
            'In classical Greek usage, ὑποκρίσις was entirely neutral — it described '
            'the craft of acting. The NT hardens it into a moral negative: the '
            'deliberate performance of piety that contradicts one\'s actual condition.'
        ),
        'semantic_note': (
            'Jesus deploys ὑπόκρισις against the scribes and Pharisees in his seven '
            'woes (Matt 23), where the indictment is precisely the gap between '
            'outward religious performance and inward reality. Mark 12:15 records '
            'Jesus perceiving their ὑπόκρισιν when they attempt to trap him. '
            'Paul uses it for Peter\'s behaviour at Antioch (Gal 2:13): '
            '"the other Jews dissembled (συνυπεκρίθησαν) likewise … insomuch '
            'that Barnabas also was carried away with their hypocrisy (ὑποκρίσει)." '
            'In 1 Tim 4:2 "lies spoken in hypocrisy (ὑποκρίσει)" describes the '
            'false teacher whose conscience has been seared.'
        ),
        'ot_concept': (
            'The LXX uses ὑπόκρισις only in deuterocanonical books (0× canonical OT), '
            'reflecting the fact that the theatrical dimension of the term is distinctly '
            'Greek. The closest Hebrew equivalent is חֹנֶף (H2612, godlessness / '
            'profaneness), which occurs only once in the OT (Job 34:30). The Hebrew '
            'Bible addresses the gap between appearance and reality through narrative '
            '(e.g., Ananias and Sapphira\'s story is anticipated in Achan\'s, '
            'Josh 7) rather than a single lexeme. The concept Peter names here '
            'is shaped more by Hellenistic Jewish moral discourse than by OT Hebrew.'
        ),
        'theological_note': (
            'The plural ὑποκρίσεις (KJV "hypocrisies") is notable — it suggests not '
            'a single act but a habitual pattern of performances. In the context of '
            '1 Peter\'s scattered and pressured communities, ὑπόκρισις would describe '
            'social self-presentation crafted for group approval rather than integrity '
            'before God. It pairs naturally with φθόνος: both are sins of the interior '
            'life directed against others — one through false face, one through hidden '
            'resentment.'
        ),
    },
    {
        'strongs': 'G5355',
        'greek': 'φθόνος',
        'translit': 'phthonos',
        'gloss': 'envy, jealousy (malicious)',
        'kjv_render': 'envies',
        'heb_roots': ['H7068', 'H7065'],
        'etymology': (
            'Root uncertain; possibly related to φθείρω (to corrupt, destroy). '
            'Unlike ζῆλος, which can denote positive zeal or ardent desire, '
            'φθόνος is uniformly negative in Greek moral vocabulary — it names '
            'the pain felt at another\'s good fortune, combined with the desire '
            'to diminish it.'
        ),
        'semantic_note': (
            'In the NT φθόνος is always negative: it is the explicit motive for '
            'which the chief priests delivered Jesus to Pilate (Matt 27:18; '
            'Mark 15:10 — two independent witnesses to this). It appears as a '
            '"work of the flesh" in Gal 5:21, alongside murders; in Titus 3:3 '
            'as a descriptor of the pre-conversion life ("living in malice and '
            'φθόνῳ, hateful and hating one another"); and at Phil 1:15 as the '
            'motive of some who preach Christ. The contrast with ζῆλος is '
            'theologically significant: ζῆλος can be righteous (John 2:17; '
            'Rom 10:2) but φθόνος never is.'
        ),
        'ot_concept': (
            'The LXX uses φθόνος only 4× and all occurrences are deuterocanonical '
            '(0× canonical OT). The Hebrew vocabulary does not draw the same sharp '
            'distinction: קִנְאָה (H7068, jealousy/zeal, 43× OT) and the verb '
            'קָנָא (H7065, 34× OT) cover both positive zeal (Num 25:11, Phinehas; '
            'Zech 1:14, God\'s jealousy for Jerusalem) and negative envy '
            '(Gen 37:11, Joseph\'s brothers). The LXX\'s minimal use of φθόνος '
            'reflects the Greek coinage\'s restriction to the purely malicious sense, '
            'which Hebrew expresses through context rather than lexeme.'
        ),
        'theological_note': (
            'The plural φθόνους (KJV "envies") suggests recurrent occurrences of '
            'the disposition. In a community letter written to dispersed believers '
            'under social pressure, envy describes the corrosive comparison between '
            'members — resentment of another\'s gifts, standing, or apparent '
            'security. Peter\'s answer in v. 2 is the exact antidote: desire the '
            '"sincere milk of the word" and *grow* — when all are oriented toward '
            'the same source of nourishment, competitive envy loses its footing.'
        ),
    },
    {
        'strongs': 'G2636',
        'greek': 'καταλαλιά',
        'translit': 'katalalia',
        'gloss': 'slander, evil speaking, defamation',
        'kjv_render': 'evil speakings',
        'heb_roots': [],
        'etymology': (
            'From κατά (against, down) + λαλέω (to speak). Literally "speaking '
            'against" someone. The compound structure — πρεπόν prefix with '
            'directional force — distinguishes this from mere loose talk: '
            'καταλαλιά is directed, targeted speech aimed at harming another\'s '
            'reputation or standing.'
        ),
        'semantic_note': (
            'NT hapax in the noun form: the only two occurrences are 2 Cor 12:20 '
            '(where Paul fears finding "strifes, envyings, wraths, strifes, '
            'backbitings (καταλαλιαί), whisperings…" at Corinth) and here. '
            'The related verb καταλαλέω, however, appears 4× in 1 Peter alone: '
            '2:12 ("whereas they speak against (καταλαλοῦσιν) you as evildoers"); '
            '3:16 ×2 ("they may be ashamed that falsely accuse your good '
            'conversation in Christ"). This concentration makes the καταλαλ- '
            'word-group a distinctive pastoral concern of the letter.'
        ),
        'ot_concept': (
            'No canonical LXX occurrences; one deuterocanonical occurrence. '
            'No single Hebrew equivalent. The OT addresses malicious speech through '
            'terms like רָכִיל (H7400, talebearer/slanderer, 6×) and דִּבָּה '
            '(H1681, evil report/defamation, 9×). The ninth commandment\'s '
            'prohibition of "false witness" (עֵד שֶׁקֶר, Exo 20:16) covers '
            'the legal dimension; the Psalms address the social reality (Ps 15:3, '
            '"He that backbiteth not with his tongue").'
        ),
        'theological_note': (
            'Though the rarest term in the list, καταλαλιά frames the entire '
            'letter\'s concern with the community\'s witness before outsiders. '
            'The irony Peter develops is pointed: the pagans speak against '
            '(καταλαλοῦσιν) the believers (2:12; 3:16), yet the believers are '
            'commanded to stop doing the same thing to one another (2:1). '
            'The community that lays aside καταλαλιά internally becomes '
            'the community that can endure καταλαλιά externally. '
            'The Ps 34 quotation at 3:10 — "let him refrain his lips from '
            'evil, and his tongue from speaking guile (δόλον)" — ties '
            'the speech-ethics of 2:1 (δόλος + καταλαλιά) to the letter\'s '
            'broader call to Christlike endurance.'
        ),
    },
]

# Derive slugs
for _t in TERMS:
    _t['slug'] = _t['translit'].lower()


# ── Charts ────────────────────────────────────────────────────────────────────

def _build_nt_chart(term: dict) -> bool:
    """Bar chart of NT occurrences by book. Returns True if chart was saved."""
    hits = nt[nt['strongs'] == term['strongs']]
    if len(hits) < 3:
        return False
    by_book = hits.groupby('book_id').size()
    books_ord = [b for b in NT_BOOK_ORDER if b in by_book.index]
    counts = [by_book[b] for b in books_ord]
    labels = [NT_BOOK_NAMES.get(b, b) for b in books_ord]

    fig, ax = plt.subplots(figsize=(max(5, len(books_ord) * 0.8 + 1.5), 3.5))
    bars = ax.bar(range(len(labels)), counts, color='#2166ac', alpha=0.9)
    for bar, v in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.05, str(v),
                ha='center', va='bottom', fontsize=9)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=8.5)
    ax.set_ylabel('Occurrences')
    ax.set_title(f'{term["greek"]} — NT Distribution', fontsize=10, fontweight='bold')
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.tight_layout()
    path = CHART_DIR / f'{term["slug"]}-nt.png'
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Chart: {path}')
    return True


def _build_lxx_chart(term: dict) -> bool:
    """Bar chart of LXX canonical occurrences by book."""
    hits = _lxx_df[
        (_lxx_df['strongs'] == term['strongs']) & (~_lxx_df['is_deuterocanon'])
    ]
    if len(hits) < 5:
        return False
    by_book = hits.groupby('book_id').size().sort_values(ascending=False).head(12)
    labels = [OT_BOOK_NAMES.get(b, b) for b in by_book.index]

    fig, ax = plt.subplots(figsize=(max(6, len(labels) * 0.7 + 1.5), 3.5))
    bars = ax.bar(range(len(labels)), by_book.values, color='#4dac26', alpha=0.9)
    for bar, v in zip(bars, by_book.values):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.05, str(v),
                ha='center', va='bottom', fontsize=9)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=8.5)
    ax.set_ylabel('Occurrences')
    ax.set_title(f'{term["greek"]} — LXX Distribution (canonical)', fontsize=10,
                 fontweight='bold')
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.tight_layout()
    path = CHART_DIR / f'{term["slug"]}-lxx.png'
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Chart: {path}')
    return True


# ── Per-term page ─────────────────────────────────────────────────────────────

def _nt_occurrence_table(term: dict) -> list[str]:
    hits = nt[nt['strongs'] == term['strongs']]
    refs = hits[['book_id', 'chapter', 'verse', 'word']].drop_duplicates(
        subset=['book_id', 'chapter', 'verse']
    ).sort_values(['book_id', 'chapter', 'verse'])
    if refs.empty:
        return ['*No NT occurrences.*']
    lines = ['| Reference | Greek form | KJV text |', '|---|---|---|']
    for _, r in refs.iterrows():
        bname = NT_BOOK_NAMES.get(r['book_id'], r['book_id'])
        t = _kjv_verse(r['book_id'], int(r['chapter']), int(r['verse']))
        lines.append(f'| {bname} {r["chapter"]}:{r["verse"]} | {r["word"]} | {t} |')
    return lines


def _lxx_occurrence_table(term: dict) -> list[str]:
    hits = _lxx_df[
        (_lxx_df['strongs'] == term['strongs']) & (~_lxx_df['is_deuterocanon'])
    ]
    if hits.empty:
        return []
    by_book = hits.groupby('book_id').size().sort_values(ascending=False)
    lines = [
        f'**Canonical LXX: {len(hits)} occurrences across {len(by_book)} book(s)**',
        '',
        '| Book | Count |',
        '|---|---:|',
    ]
    for b, c in by_book.items():
        lines.append(f'| {OT_BOOK_NAMES.get(b, b)} | {c} |')
    return lines


def build_term_page(term: dict, nt_chart: bool, lxx_chart: bool) -> None:
    slug = term['slug']
    term_dir = REPORT_DIR / slug
    term_dir.mkdir(exist_ok=True)

    hits_nt = nt[nt['strongs'] == term['strongs']]
    hits_lxx = _lxx_df[
        (_lxx_df['strongs'] == term['strongs']) & (~_lxx_df['is_deuterocanon'])
    ]
    nt_occ = len(hits_nt)
    nt_bks = hits_nt['book_id'].nunique()
    lxx_occ = len(hits_lxx)

    # Relative path from term subdir to charts
    chart_rel = '../../../../../../charts/nt/lexicon/1pet2-vice-list'

    heb_str = ''
    if term['heb_roots']:
        heb_labels = {
            'H7451': 'רַע / רָעָה (evil)',
            'H4820': 'מִרְמָה (deceit)',
            'H7423': 'רְמִיָּה (treachery)',
            'H2612': 'חֹנֶף (godlessness)',
            'H7068': 'קִנְאָה (envy/zeal — noun)',
            'H7065': 'קָנָא (envy/be jealous — verb)',
        }
        heb_str = '; '.join(
            f'{heb_labels.get(r, r)} ({len(ot[ot["strongs"].apply(_get_heb_root) == r])}× OT)'
            for r in term['heb_roots']
        )

    lines = [
        f'# {term["greek"]} ({term["strongs"]}) — {term["gloss"]}',
        '',
        '*Part of the [1 Peter 2:1 Vice List study](../index.md)*',
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
        f'| 1 Pet 2:1 KJV | "{term["kjv_render"]}" |',
        f'| NT occurrences | {nt_occ} ({nt_bks} book{"s" if nt_bks != 1 else ""}) |',
        f'| LXX occurrences (canonical) | {lxx_occ} |',
    ]
    if heb_str:
        lines.append(f'| Hebrew background | {heb_str} |')
    lines += [
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
    if lxx_chart:
        lines += [
            f'![LXX distribution]({chart_rel}/{slug}-lxx.png)',
            '',
        ]
    if lxx_occ > 0:
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


# ── Main index page ───────────────────────────────────────────────────────────

def build_index() -> None:
    lines = [
        '# 1 Peter 2:1 — The "Lay Aside" Vice List',
        '',
        '*Build script: [scripts/nt/lexicon/build_1pet2_vice_list.py]'
        '(../../../../scripts/nt/lexicon/build_1pet2_vice_list.py)*',
        '',
        '---',
        '',
        '## Contents',
        '',
        '- [The Passage](#the-passage)',
        '- [Key Observations](#key-observations)',
        '- [Term Catalogue](#term-catalogue)',
        '',
        '---',
        '',
        '## The Passage',
        '',
        '> *"Wherefore laying aside all malice, and all guile, and hypocrisies, '
        'and envies, and all evil speakings,*',
        '> *As newborn babes, desire the sincere milk of the word, that ye may grow '
        'thereby."* — 1 Peter 2:1–2 (KJV)',
        '',
        '**Greek text (1 Pet 2:1):**',
        '> Ἀποθέμενοι οὖν πᾶσαν κακίαν καὶ πάντα δόλον καὶ ὑποκρίσεις καὶ '
        'φθόνους καὶ πάσας καταλαλιάς',
        '',
        '---',
        '',
        '## Key Observations',
        '',
        '### 1. The aorist participle of command',
        '',
        '**Ἀποθέμενοι** ("having laid aside / putting off") is an aorist participle '
        'of ἀποτίθημι. The aorist signals a decisive prior act that accompanies '
        'the positive command of v. 2 ("desire the sincere milk of the word"). '
        'The same verb and construction appear in Eph 4:22–25, Col 3:8, Heb 12:1, '
        'and Jas 1:21 — a shared early-church baptismal formula for the ethical '
        'break from the old life.',
        '',
        '### 2. κακία as the root, the others as branches',
        '',
        'The five vices are not a random list. κακία (malice/evil) heads the '
        'series as the broadest term — the inner disposition from which the other '
        'four are specific expressions. δόλος and καταλαλιά both concern speech; '
        'ὑπόκρισις and φθόνος concern the interior life before others. Together '
        'they describe the social sins that fracture community.',
        '',
        '### 3. δόλος reappears in Peter\'s Christology',
        '',
        'At 2:22 Peter quotes Isa 53:9 LXX: *"neither was any δόλος found in his '
        'mouth"* — applied to Christ\'s sinlessness. This makes Christ\'s freedom '
        'from guile the explicit model for the behavior commanded in 2:1. The '
        'readers are to lay aside δόλος *because* their Lord never had it.',
        '',
        '### 4. The LXX depth varies dramatically',
        '',
        'κακία (110× canonical LXX) and δόλος (34× canonical LXX) have deep OT '
        'roots in Hebrew. ὑπόκρισις, φθόνος, and καταλαλιά have 0 canonical LXX '
        'occurrences — they are essentially NT-era moral vocabulary, shaped more by '
        'Hellenistic Jewish discourse than by Hebrew OT categories.',
        '',
        '### 5. καταλαλιά and the letter\'s concern with speech before outsiders',
        '',
        'Though the rarest term (2 NT occurrences), the καταλαλ- word-group '
        'appears 3× more in 1 Peter itself (2:12; 3:16 ×2). The communities '
        'Peter writes to were subject to slander from outsiders; his command '
        'is that they not do the same thing to one another.',
        '',
        '---',
        '',
        '## Term Catalogue',
        '',
        '| Term | Strongs | Gloss | NT occ | LXX occ (canonical) |',
        '|---|---|---|---|---|',
    ]

    for term in TERMS:
        nt_ct = len(nt[nt['strongs'] == term['strongs']])
        lxx_ct = len(_lxx_df[
            (_lxx_df['strongs'] == term['strongs']) & (~_lxx_df['is_deuterocanon'])
        ])
        slug = term['slug']
        lines.append(
            f'| [{term["greek"]}]({slug}/README.md) '
            f'| {term["strongs"]} '
            f'| {term["gloss"]} '
            f'| {nt_ct} '
            f'| {lxx_ct} |'
        )

    lines += [
        '',
        '---',
        '',
        '*Greek NT data: TAGNT (Byzantine/Textus Receptus, STEPBible CC BY 4.0).*  ',
        '*LXX data: CenterBLC LXX (CC BY 4.0).*  ',
        '*Hebrew data: TAHOT (STEPBible CC BY 4.0).*',
    ]

    path = REPORT_DIR / 'index.md'
    path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'  Index: {path}')


# ── CSV ───────────────────────────────────────────────────────────────────────

def build_csv() -> None:
    rows = []
    for term in TERMS:
        for _, r in nt[nt['strongs'] == term['strongs']][
            ['book_id', 'chapter', 'verse']
        ].drop_duplicates().iterrows():
            rows.append({
                'lemma': term['greek'], 'strongs': term['strongs'],
                'gloss': term['gloss'],
                'book': r['book_id'], 'chapter': r['chapter'], 'verse': r['verse'],
            })
    out = REPORT_DIR / '1pet2-vice-list.csv'
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f'  CSV: {out}')


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('Building charts...')
    nt_charts = {}
    lxx_charts = {}
    for term in TERMS:
        nt_charts[term['slug']] = _build_nt_chart(term)
        lxx_charts[term['slug']] = _build_lxx_chart(term)

    print('Building term pages...')
    for term in TERMS:
        build_term_page(term, nt_charts[term['slug']], lxx_charts[term['slug']])

    print('Building index...')
    build_index()

    print('Building CSV...')
    build_csv()

    print('Done.')
