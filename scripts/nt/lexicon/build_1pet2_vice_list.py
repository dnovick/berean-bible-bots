"""Build 1 Peter 2:1 — "Lay Aside" Vice List word study.

Five terms commanded to be put off in 1 Peter 2:1:
  κακία (G2549) — malice / evil
  δόλος (G1388) — deceit / guile
  ὑπόκρισις (G5272) — hypocrisy
  φθόνος (G5355) — envy
  καταλαλιά (G2636) — slander / evil speaking

Outputs:
  output/reports/nt/lexicon/1pet2-vice-list/1pet2-vice-list.md
  output/reports/nt/lexicon/1pet2-vice-list/1pet2-vice-list-nt-heatmap.png
  output/reports/nt/lexicon/1pet2-vice-list/1pet2-vice-list.csv
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, '.')
from src.bible_grammar.core import db as _db  # noqa: E402

REPORT_DIR = Path('output/reports/nt/lexicon/1pet2-vice-list')
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ── Terms ─────────────────────────────────────────────────────────────────────

TERMS: list[tuple[str, str, str, list[str], str, str]] = [
    # (strongs, lemma, gloss, heb_roots, etymology, theological_note)
    (
        'G2549', 'κακία', 'malice, evil, wickedness',
        ['H7451'],
        'From κακός (bad, evil). The most general term in the list — covers all moral evil, '
        'both as inner disposition and outward act.',
        'In the NT κακία spans the range from specific "malice" toward others (Eph 4:31) to '
        'general "wickedness" (Acts 8:22) and even "trouble" (Matt 6:34). The LXX uses it '
        '110× in canonical books to render Hebrew רַע / רָעָה — the broadest OT word for evil. '
        'Peter places it first, making it the root from which the other four grow.',
    ),
    (
        'G1388', 'δόλος', 'deceit, guile, treachery',
        ['H4820', 'H7423'],
        'From δέλω (to trap). Originally meant bait or lure; extended to any cunning trick '
        'or deception.',
        'The LXX uses δόλος 34× in canonical books for Hebrew מִרְמָה (deceit, treachery) '
        'and רְמִיָּה (laxness, slackness — often with the sense of deliberate negligence). '
        'Both Hebrew nouns carry the idea of calculated dishonesty. In the NT δόλος appears '
        'in vice lists (Rom 1:29; Mark 7:22) and is used for the plot to arrest Jesus '
        '(Matt 26:4; Mark 14:1). Notably, Jesus calls Nathanael a man "in whom is no δόλος" '
        '(John 1:47) — echoing Ps 32:2 ("in whose spirit there is no deceit"). '
        'Peter himself quotes Ps 34:13 ("let him refrain his lips from speaking δόλον") '
        'just two verses later at 1 Pet 2:22, applying it to Christ\'s sinlessness.',
    ),
    (
        'G5272', 'ὑπόκρισις', 'hypocrisy, dissimulation, play-acting',
        ['H2612'],
        'From ὑποκρίνομαι (to play a part on stage, to answer from under a mask). '
        'Classical Greek used it of actors; in the NT it denotes religious insincerity.',
        'The word appears in NT contexts of religious performance divorced from reality: '
        'Jesus\' seven woes against the scribes and Pharisees (Matt 23), the testing of Jesus '
        '(Mark 12:15), and Paul\'s rebuke of Peter\'s "dissimulation" (Gal 2:13). '
        'The Hebrew חֹנֶף (godlessness, profanity) is only a partial equivalent — the '
        'theatrical dimension of ὑπόκρισις is distinctly Greek. In the NT ὑπόκρισις '
        'names the specific sin of performing piety for human approval rather than before God. '
        'In 1 Tim 4:2 "lies in hypocrisy" (ἐν ὑποκρίσει) describes the conscience-seared '
        'false teacher.',
    ),
    (
        'G5355', 'φθόνος', 'envy, jealousy (malicious)',
        ['H7068', 'H7065'],
        'Root uncertain; possibly related to φθείρω (to corrupt). Unlike ζῆλος (which can '
        'be positive), φθόνος always has a negative force — pain at another\'s good fortune.',
        'φθόνος is consistently negative in the NT — it is the motive for which the chief '
        'priests delivered Jesus (Matt 27:18; Mark 15:10). It appears in Galatians as a '
        '"work of the flesh" (5:21) and in Titus 3:3 as a descriptor of pre-conversion life. '
        'The Hebrew קִנְאָה covers both positive zeal and negative envy; the LXX uses '
        'φθόνος only 4× and almost entirely restricts the negative sense to it. '
        'The distinction from ζῆλος is important: ζῆλος can be righteous (John 2:17; '
        'Rom 10:2) but φθόνος never is. Peter pairs it with ὑπόκρισις — both involve '
        'a false interior orientation toward others.',
    ),
    (
        'G2636', 'καταλαλιά', 'slander, evil speaking, defamation',
        [],
        'From κατά (against) + λαλέω (to speak). Literally "speaking against" someone.',
        'The rarest term in the list: only 2 NT occurrences (2 Cor 12:20; 1 Pet 2:1) and '
        '1 LXX occurrence (deuterocanonical). The related verb καταλαλέω appears 4× in '
        '1 Peter alone (2:12; 3:16 ×2; cf. Jas 4:11), making the καταλαλ- word-group '
        'particularly characteristic of the letter\'s concern with the community\'s reputation '
        'before outsiders. The compound structure (against + speak) emphasizes that this is '
        'directed, targeted speech — not mere gossip but speech designed to harm someone\'s '
        'standing. Peter returns to the theme at 2:12: "having your conversation honest among '
        'the Gentiles: that, whereas they speak against (καταλαλοῦσιν) you as evildoers, they '
        'may by your good works … glorify God."',
    ),
]

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
    '1Ch': '1 Chronicles', '2Ch': '2 Chronicles', 'Ezr': 'Ezra', 'Neh': 'Nehemiah',
    'Est': 'Esther', 'Job': 'Job', 'Psa': 'Psalms', 'Pro': 'Proverbs',
    'Ecc': 'Ecclesiastes', 'Sng': 'Song', 'Isa': 'Isaiah', 'Jer': 'Jeremiah',
    'Lam': 'Lamentations', 'Ezk': 'Ezekiel', 'Dan': 'Daniel', 'Hos': 'Hosea',
    'Jol': 'Joel', 'Amo': 'Amos', 'Oba': 'Obadiah', 'Jon': 'Jonah',
    'Mic': 'Micah', 'Nam': 'Nahum', 'Hab': 'Habakkuk', 'Zep': 'Zephaniah',
    'Hag': 'Haggai', 'Zec': 'Zechariah', 'Mal': 'Malachi',
}

HEB_ROOTS = {
    'H7451': 'רַע / רָעָה (evil, wickedness)',
    'H4820': 'מִרְמָה (deceit, fraud)',
    'H7423': 'רְמִיָּה (slackness, treachery)',
    'H2612': 'חֹנֶף (godlessness, profaneness)',
    'H7068': 'קִנְאָה (jealousy, envy — noun)',
    'H7065': 'קָנָא (be jealous/envious — verb)',
}


def get_root(s: str) -> str:
    if not isinstance(s, str):
        return ''
    m = re.search(r'\{(H\d+)[A-Z]?\}', s)
    return m.group(1) if m else ''


# ── Chart: heatmap of term × NT book ─────────────────────────────────────────

def chart_heatmap(nt: pd.DataFrame) -> Path:
    lemmas = [lem for _, lem, *_ in TERMS]

    books_hit: set[str] = set()
    data: dict[str, dict[str, int]] = {lem: {} for lem in lemmas}
    for s, lem, *_ in TERMS:
        for book, cnt in nt[nt['strongs'] == s].groupby('book_id').size().items():
            data[lem][book] = int(cnt)
            books_hit.add(book)

    books = [b for b in NT_BOOK_ORDER if b in books_hit]
    book_labels = [NT_BOOK_NAMES.get(b, b) for b in books]

    mat = np.zeros((len(lemmas), len(books)), dtype=int)
    for i, lem in enumerate(lemmas):
        for j, b in enumerate(books):
            mat[i, j] = data[lem].get(b, 0)

    fig, ax = plt.subplots(figsize=(max(10, len(books) * 0.8 + 2), len(lemmas) * 0.7 + 2))
    im = ax.imshow(mat, aspect='auto', cmap='YlOrRd', vmin=0)

    ax.set_xticks(range(len(books)))
    ax.set_xticklabels(book_labels, rotation=45, ha='right', fontsize=8.5)
    ax.set_yticks(range(len(lemmas)))
    ax.set_yticklabels(lemmas, fontsize=10)

    for i in range(len(lemmas)):
        for j in range(len(books)):
            v = mat[i, j]
            if v > 0:
                mx = mat[i].max() or 1
                color = 'white' if v / mx > 0.6 else '#333'
                ax.text(j, i, str(v), ha='center', va='center',
                        fontsize=9, color=color, fontweight='bold')

    ax.set_title('1 Peter 2:1 Vice List — NT Distribution',
                 fontsize=11, fontweight='bold', pad=10)
    plt.colorbar(im, ax=ax, shrink=0.6, label='Occurrences')
    plt.tight_layout()
    out = REPORT_DIR / '1pet2-vice-list-nt-heatmap.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved {out}')
    return out


# ── Report ────────────────────────────────────────────────────────────────────

def build_report(df: pd.DataFrame, lxx: pd.DataFrame) -> Path:
    nt = df[df['source'] == 'TAGNT']
    ot = df[df['source'] == 'TAHOT']

    kjv_trans = _db.load_translations()
    kjv = kjv_trans[kjv_trans['translation'] == 'KJV']

    def kjv_text(book: str, ch: int, vs: int) -> str:
        r = kjv[(kjv['book_id'] == book) & (kjv['chapter'] == ch) & (kjv['verse'] == vs)]
        t = r['text'].values[0] if len(r) else ''
        return (t[:120] + '…') if len(t) > 120 else t

    lines = [
        '# 1 Peter 2:1 — The "Lay Aside" Vice List',
        '',
        '**Anchor text:** 1 Peter 2:1 (KJV) — *"Wherefore laying aside all malice, '
        'and all guile, and hypocrisies, and envies, and all evil speakings"*',
        '',
        '**Corpora:** NT Greek (TAGNT) · LXX Greek · Biblical Hebrew (TAHOT)',
        '',
        '## Contents',
        '',
        '- [Overview](#overview)',
        '- [Key Observations](#key-observations)',
    ]
    for _, l, g, *_ in TERMS:
        anchor = l.lower().replace('/', '').replace(' ', '-')
        lines.append(f'- [{l} — {g.split(",")[0]}](#{anchor})')
    lines += [
        '- [Vice List Distribution Chart](#vice-list-distribution-chart)',
        '- [Summary Table](#summary-table)',
        '',
        '---',
        '',
        '## Overview',
        '',
        '1 Peter 2:1 opens with an aorist participle of command: **Ἀποθέμενοι** '
        '("having laid aside" / "putting off") — from ἀποτίθημι, the same verb used '
        'in Eph 4:22 ("put off the old man"), Col 3:8 ("put off all these"), '
        'and Jas 1:21 ("lay apart all filthiness"). The aorist participle '
        'signals a decisive, prior action that accompanies the positive command '
        'of v. 2 ("desire the sincere milk of the word"). You lay these things aside '
        '*in order to* grow.',
        '',
        'Five vices follow, structured as three pairs (κακία / δόλος; '
        'ὑπόκρισεις / φθόνους; then the closing καταλαλιάς). All five are nouns. '
        'The range is significant: they span inner disposition (κακία, φθόνος), '
        'deliberate deception (δόλος), performed religion (ὑπόκρισις), and '
        'destructive speech (καταλαλιά). Together they describe the social sins that '
        'fracture community — exactly the concern of a letter written to dispersed '
        'communities living under social pressure.',
        '',
        '---',
        '',
        '## Key Observations',
        '',
        '- **κακία heads the list** as the broadest term, functioning as the genus '
        'of which the others are species. All four subsequent vices are forms of '
        'κακία in concrete expression.',
        '',
        '- **δόλος reappears in Peter\'s Christology.** At 2:22 Peter quotes '
        'Isa 53:9 ("neither was any δόλος found in his mouth"), making Christ\'s '
        'freedom from guile the explicit model for the behavior commanded in 2:1.',
        '',
        '- **ὑπόκρισις and φθόνος concern the interior life toward others.** '
        'Hypocrisy wears a false face; envy harbors secret hostility. Both sins '
        'become especially toxic in close communities under external pressure — '
        'exactly the situation of 1 Peter\'s recipients.',
        '',
        '- **καταλαλιά is the rarest NT term** (only 2 occurrences), yet the '
        'related verb καταλαλέω recurs three times in 1 Peter itself, making '
        '"speaking against" a distinctive pastoral concern of the letter. '
        'The community\'s speech before outsiders is a recurring theme '
        '(2:12; 3:16).',
        '',
        '- **LXX background is uneven.** κακία (110× canonical LXX) and δόλος '
        '(34× canonical LXX) have deep OT roots; ὑπόκρισις, φθόνος, and '
        'καταλαλιά are essentially NT-era terms with minimal LXX presence.',
        '',
        '---',
        '',
    ]

    for strongs, lemma, gloss, heb_roots_list, etym, theological_note in TERMS:
        nt_hits = nt[nt['strongs'] == strongs]
        lxx_hits = lxx[lxx['strongs'] == strongs]
        lxx_canon = lxx_hits[~lxx_hits['is_deuterocanon']]

        anchor = lemma.lower().replace('/', '').replace(' ', '-')
        lines += [
            f'## {lemma}',
            '',
            f'**Strongs:** {strongs}  ',
            f'**Gloss:** {gloss}  ',
            f'**NT occurrences:** {len(nt_hits)}  ',
            f'**LXX occurrences (canonical):** {len(lxx_canon)}  ',
        ]
        if heb_roots_list:
            heb_str = '; '.join(
                f'{HEB_ROOTS.get(r, r)} ({len(ot[ot["strongs"].apply(get_root) == r])}×)'
                for r in heb_roots_list
            )
            lines.append(f'**Hebrew background:** {heb_str}')
        lines += [
            '',
            f'**Etymology:** {etym}',
            '',
            f'**Theological note:** {theological_note}',
            '',
        ]

        # NT distribution table
        by_book = nt_hits.groupby('book_id').size().sort_values(ascending=False)
        if len(by_book):
            lines += [
                '**NT distribution:**',
                '',
                '| Book | Count |',
                '|---|---:|',
            ]
            for b, c in by_book.items():
                lines.append(f'| {NT_BOOK_NAMES.get(b, b)} | {c} |')
            lines.append('')

        # Key NT verses
        refs = nt_hits[['book_id', 'chapter', 'verse']].drop_duplicates()
        refs_sorted = refs.sort_values(['book_id', 'chapter', 'verse'])
        lines += [
            '**NT occurrences (KJV):**',
            '',
            '| Reference | KJV text |',
            '|---|---|',
        ]
        for _, r in refs_sorted.iterrows():
            bname = NT_BOOK_NAMES.get(r['book_id'], r['book_id'])
            t = kjv_text(r['book_id'], int(r['chapter']), int(r['verse']))
            lines.append(f'| {bname} {r["chapter"]}:{r["verse"]} | {t} |')
        lines.append('')

        # LXX top books
        if len(lxx_canon) > 0:
            by_book_lxx = lxx_canon.groupby('book_id').size().sort_values(ascending=False)
            lines += [
                f'**LXX distribution (canonical, {len(lxx_canon)} total):**  ',
                ', '.join(
                    f'{OT_BOOK_NAMES.get(b, b)} ({c})'
                    for b, c in list(by_book_lxx.items())[:8]
                ),
                '',
            ]

        lines.append('---')
        lines.append('')

    lines += [
        '## Vice List Distribution Chart',
        '',
        '![NT Distribution Heatmap](1pet2-vice-list-nt-heatmap.png)',
        '',
        '---',
        '',
        '## Summary Table',
        '',
        '| Term | Strongs | NT | LXX (canonical) | Hebrew background | Gloss |',
        '|---|---|---:|---:|---|---|',
    ]
    for strongs, lemma, gloss, heb_roots_list, *_ in TERMS:
        nt_ct = len(nt[nt['strongs'] == strongs])
        lxx_ct = len(lxx[(lxx['strongs'] == strongs) & (~lxx['is_deuterocanon'])])
        heb = '; '.join(HEB_ROOTS.get(r, r) for r in heb_roots_list) if heb_roots_list else '—'
        lines.append(
            f'| {lemma} | {strongs} | {nt_ct} | {lxx_ct} | {heb} | {gloss} |'
        )
    lines += [
        '',
        '---',
        '',
        '*Greek NT data: TAGNT (Byzantine/Textus Receptus, STEPBible CC BY 4.0).*  ',
        '*LXX data: CenterBLC LXX (CC BY 4.0).*  ',
        '*Hebrew data: TAHOT (STEPBible CC BY 4.0).*  ',
        '*Generated by [scripts/nt/lexicon/build_1pet2_vice_list.py]'
        '(../../../../scripts/nt/lexicon/build_1pet2_vice_list.py).*',
    ]

    out = REPORT_DIR / '1pet2-vice-list.md'
    out.write_text('\n'.join(lines), encoding='utf-8')
    print(f'  Saved {out}')
    return out


def build_csv(df: pd.DataFrame) -> Path:
    nt = df[df['source'] == 'TAGNT']
    rows = []
    for strongs, lemma, gloss, *_ in TERMS:
        for _, r in nt[nt['strongs'] == strongs][['book_id', 'chapter', 'verse']]\
                .drop_duplicates().iterrows():
            rows.append({
                'lemma': lemma, 'strongs': strongs, 'gloss': gloss,
                'book': r['book_id'], 'chapter': r['chapter'], 'verse': r['verse'],
            })
    out = REPORT_DIR / '1pet2-vice-list.csv'
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f'  Saved {out}')
    return out


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('Loading data...')
    df = _db.load()
    lxx = _db.load_lxx()
    nt = df[df['source'] == 'TAGNT']

    print('Building chart...')
    chart_heatmap(nt)

    print('Building report...')
    build_report(df, lxx)

    print('Building CSV...')
    build_csv(df)

    print('Done.')
