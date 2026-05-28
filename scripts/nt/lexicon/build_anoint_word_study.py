"""Build "Anoint / Anointing" cross-corpus word study.

Covers NT Greek, LXX Greek, and Biblical Hebrew, tracing the semantic
field across all three corpora.

Outputs:
  output/reports/nt/lexicon/anoint-word-study/anoint-word-study.md
  output/reports/nt/lexicon/anoint-word-study/anoint-nt-distribution.png
  output/reports/nt/lexicon/anoint-word-study/anoint-lxx-distribution.png
  output/reports/nt/lexicon/anoint-word-study/anoint-hebrew-distribution.png
  output/reports/nt/lexicon/anoint-word-study/anoint-word-study.csv
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

REPORT_DIR = Path('output/reports/nt/lexicon/anoint-word-study')
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ── NT Greek terms ────────────────────────────────────────────────────────────
NT_TERMS: list[tuple[str, str, str]] = [
    # (strongs, lemma, gloss)
    ('G0218', 'ἀλείφω',   'anoint (physical/ceremonial)'),
    ('G5548', 'χρίω',     'anoint (consecrate/commission)'),
    ('G2025', 'ἐπιχρίω',  'rub on / spread on'),
    ('G1472', 'ἐγχρίω',   'anoint (imperative sense)'),
    ('G3462', 'μυρίζω',   'anoint with myrrh/ointment'),
    ('G5545', 'χρῖσμα',   'anointing (noun — the gift/act)'),
    ('G5547', 'χριστός',  'Christ / Anointed One'),
    ('G3464', 'μύρον',    'myrrh / ointment / fragrant oil'),
]

# ── LXX Greek terms ───────────────────────────────────────────────────────────
LXX_TERMS: list[tuple[str, str, str]] = [
    ('G5548', 'χρίω',    'anoint (primary LXX word for mashach)'),
    ('G5547', 'χριστός', 'Anointed One (translate mashiach)'),
    ('G3464', 'μύρον',   'ointment / fragrant oil'),
]

# ── Hebrew terms ──────────────────────────────────────────────────────────────
HEB_TERMS: list[tuple[str, str, str, str]] = [
    # (root, transliteration, gloss, part_of_speech_hint)
    ('H4886', 'māšaḥ',   'to anoint (verb)',            'Verb'),
    ('H4888', 'mišḥāh',  'anointing / consecration (noun)', 'Noun'),
    ('H4899', 'māšîaḥ',  'anointed one / Messiah',      'Noun'),
    ('H5480', 'sûk',     'anoint oneself / rub with oil', 'Verb'),
]

# ── NT book order ─────────────────────────────────────────────────────────────
NT_BOOK_ORDER = [
    'Mat', 'Mrk', 'Luk', 'Jhn', 'Act',
    'Rom', '1Co', '2Co', 'Gal', 'Eph', 'Php', 'Col',
    '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm',
    'Heb', 'Jas', '1Pe', '2Pe', '1Jn', '2Jn', '3Jn', 'Jud', 'Rev',
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
    'Jon': 'Jonah', 'Mic': 'Micah', 'Nah': 'Nahum', 'Hab': 'Habakkuk',
    'Zep': 'Zephaniah', 'Hag': 'Haggai', 'Zec': 'Zechariah', 'Mal': 'Malachi',
}


def extract_root(s: str) -> str:
    if not isinstance(s, str):
        return ''
    m = re.search(r'\{(H\d+)[A-Z]?\}', s)
    return m.group(1) if m else ''


def verse_text(df: pd.DataFrame, book: str, ch: int, vs: int,
               source: str) -> str:
    rows = df[(df['book_id'] == book) & (df['chapter'] == ch) &
              (df['verse'] == vs) & (df['source'] == source)]
    return ' '.join(
        str(t).strip().rstrip('¶').strip()
        for t in rows['translation'].dropna()
        if str(t).strip()
    )


# ── Chart: NT distribution heatmap ───────────────────────────────────────────

def chart_nt_distribution(nt: pd.DataFrame) -> Path:
    """Heatmap of NT anoint terms by book."""
    terms = [(s, l) for s, l, _ in NT_TERMS]
    books_with_hits = set()
    data: dict[str, dict[str, int]] = {l: {} for _, l, _ in NT_TERMS}

    for strongs, lemma, _ in NT_TERMS:
        hits = nt[nt['strongs'] == strongs]
        for book, cnt in hits.groupby('book_id').size().items():
            data[lemma][book] = int(cnt)
            books_with_hits.add(book)

    books = [b for b in NT_BOOK_ORDER if b in books_with_hits]
    book_labels = [NT_BOOK_NAMES.get(b, b) for b in books]
    lemmas = [l for _, l in terms]

    mat = np.zeros((len(lemmas), len(books)), dtype=int)
    for i, (_, lemma) in enumerate(terms):
        for j, book in enumerate(books):
            mat[i, j] = data[lemma].get(book, 0)

    fig, ax = plt.subplots(figsize=(max(10, len(books) * 0.7 + 2), len(lemmas) * 0.55 + 2))
    im = ax.imshow(mat, aspect='auto', cmap='Blues', vmin=0)

    ax.set_xticks(range(len(books)))
    ax.set_xticklabels(book_labels, rotation=45, ha='right', fontsize=8.5)
    ax.set_yticks(range(len(lemmas)))
    ax.set_yticklabels(lemmas, fontsize=9)

    for i in range(len(lemmas)):
        for j in range(len(books)):
            v = mat[i, j]
            if v > 0:
                mx = mat[i].max() or 1
                color = 'white' if v / mx > 0.5 else '#333333'
                ax.text(j, i, str(v), ha='center', va='center',
                        fontsize=8, color=color, fontweight='bold')

    ax.set_title('NT "Anoint" Vocabulary — Occurrences by Book',
                 fontsize=11, fontweight='bold', pad=10)
    plt.colorbar(im, ax=ax, shrink=0.6, label='Occurrences')
    plt.tight_layout()
    out = REPORT_DIR / 'anoint-nt-distribution.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved {out}')
    return out


def chart_lxx_distribution(lxx: pd.DataFrame) -> Path:
    """Bar chart of χρίω occurrences across OT books in LXX."""
    chrio = lxx[(lxx['strongs'] == 'G5548') & (~lxx['is_deuterocanon'])]
    by_book = chrio.groupby('book_id').size().sort_values(ascending=False)

    labels = [OT_BOOK_NAMES.get(b, b) for b in by_book.index]
    colors = ['#4C72B0'] * len(labels)

    fig, ax = plt.subplots(figsize=(max(8, len(labels) * 0.6 + 1.5), 4.5))
    bars = ax.bar(range(len(labels)), by_book.values, color=colors, alpha=0.9)
    for bar, v in zip(bars, by_book.values):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.1, str(v),
                ha='center', va='bottom', fontsize=8)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=8.5)
    ax.set_ylabel('Occurrences')
    ax.set_title('χρίω in the LXX (Canonical OT) — Distribution by Book',
                 fontsize=11, fontweight='bold')
    plt.tight_layout()
    out = REPORT_DIR / 'anoint-lxx-distribution.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved {out}')
    return out


def chart_hebrew_distribution(heb: pd.DataFrame) -> Path:
    """Grouped bar chart of Hebrew anoint roots by book."""
    roots = [r for r, _, _, _ in HEB_TERMS]
    root_labels = {r: t for r, t, _, _ in HEB_TERMS}

    books_with_hits = set()
    data: dict[str, dict[str, int]] = {r: {} for r in roots}
    for root in roots:
        for book, cnt in heb[heb['root'] == root].groupby('book_id').size().items():
            data[root][book] = int(cnt)
            books_with_hits.add(book)

    ot_order = list(OT_BOOK_NAMES.keys())
    books = [b for b in ot_order if b in books_with_hits]
    book_labels = [OT_BOOK_NAMES.get(b, b) for b in books]

    n_roots = len(roots)
    x = np.arange(len(books))
    width = 0.8 / n_roots
    colors = ['#4C72B0', '#DD6B48', '#9B59B6', '#5BA85A']

    fig, ax = plt.subplots(figsize=(max(10, len(books) * 0.65 + 2), 5))
    for i, root in enumerate(roots):
        vals = [data[root].get(b, 0) for b in books]
        offset = (i - n_roots / 2 + 0.5) * width
        ax.bar(x + offset, vals, width=width * 0.9,
               color=colors[i], label=root_labels[root], alpha=0.9)

    ax.set_xticks(x)
    ax.set_xticklabels(book_labels, rotation=45, ha='right', fontsize=8.5)
    ax.set_ylabel('Occurrences')
    ax.set_title('Hebrew "Anoint" Roots — Distribution by Book',
                 fontsize=11, fontweight='bold')
    ax.legend(fontsize=8, ncol=2)
    plt.tight_layout()
    out = REPORT_DIR / 'anoint-hebrew-distribution.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved {out}')
    return out


# ── Report ────────────────────────────────────────────────────────────────────

def _kjv_ref(df: pd.DataFrame, book: str, ch: int, vs: int,
             source: str) -> str:
    text = verse_text(df, book, ch, vs, source)
    return text[:110] + '…' if len(text) > 110 else text


def build_report(df: pd.DataFrame, lxx: pd.DataFrame,
                 heb: pd.DataFrame) -> Path:
    nt = df[df['source'] == 'TAGNT']

    lines = [
        '# "Anoint / Anointing" — Cross-Corpus Word Study',
        '',
        '**Corpora:** NT Greek (TAGNT) · LXX Greek · Biblical Hebrew (TAHOT)  ',
        '**Translation:** KJV',
        '',
        '## Contents',
        '',
        '- [Overview](#overview)',
        '- [Key Observations](#key-observations)',
        '- [NT Greek Terms](#nt-greek-terms)',
        '- [LXX Greek Terms](#lxx-greek-terms)',
        '- [Biblical Hebrew Terms](#biblical-hebrew-terms)',
        '- [Cross-Corpus Connections](#cross-corpus-connections)',
        '- [Summary Table](#summary-table)',
        '',
        '---',
        '',
        '## Overview',
        '',
        'The English word "anoint" covers a rich semantic field in the biblical'
        ' languages. In the NT two distinct Greek verbs appear: **ἀλείφω**,'
        ' used for physical/everyday anointing (of the body, the sick, the dead),'
        ' and **χρίω**, used exclusively for the consecrating or commissioning'
        ' anointing associated with divine appointment. The noun **χριστός**'
        ' ("Anointed One") derives directly from χρίω and becomes the defining'
        ' title of Jesus. The LXX uses χρίω to translate the Hebrew **מָשַׁח**'
        ' (māšaḥ) throughout the OT, forging the terminological link between the'
        ' Hebrew "Messiah" (מָשִׁיחַ, māšîaḥ) and the Greek "Christ" (χριστός).',
        '',
        '---',
        '',
        '## Key Observations',
        '',
    ]

    # Dynamic observations
    aleipho_ct = len(nt[nt['strongs'] == 'G0218'])
    chrio_ct = len(nt[nt['strongs'] == 'G5548'])
    christos_nt = len(nt[nt['strongs'] == 'G5547'])
    chrisma_ct = len(nt[nt['strongs'] == 'G5545'])
    chrio_lxx = len(lxx[(lxx['strongs'] == 'G5548') & (~lxx['is_deuterocanon'])])
    mashach_ct = len(heb[heb['root'] == 'H4886'])
    mashiach_ct = len(heb[heb['root'] == 'H4899'])

    lines += [
        f'- **ἀλείφω vs. χρίω distinction:** In the NT, ἀλείφω ({aleipho_ct} occurrences)'
        ' is used for physical anointing — of the head (Matt 6:17), of the sick'
        ' (Mark 6:13; Jas 5:14), and of Jesus\' body for burial (Mark 16:1; John 12:3).'
        f' χρίω ({chrio_ct} occurrences) is reserved for divine commission: the Spirit'
        ' anointing Jesus at his baptism (Luke 4:18; Acts 10:38), and God anointing'
        ' believers (2 Cor 1:21).',
        '',
        '- **χρίω in the LXX:** The LXX translates Hebrew מָשַׁח (māšaḥ,'
        f' {mashach_ct} OT occurrences) with χρίω in {chrio_lxx} places across'
        ' the canonical OT, concentrated in Exodus–Numbers (priestly anointing),'
        ' Samuel–Kings (royal anointing), and Psalms.',
        '',
        f'- **χριστός:** In the NT χριστός appears {christos_nt:,} times as a title'
        f' for Jesus. In the LXX it translates מָשִׁיחַ (māšîaḥ, {mashiach_ct}'
        ' OT occurrences), the title borne by the anointed king or priest.'
        ' This LXX usage is the direct lexical bridge between "Messiah" and "Christ."',
        '',
        f'- **χρῖσμα ({chrisma_ct} NT occurrences, 1 John 2:20, 27):** John uses this'
        ' noun for the "anointing" believers receive from the Holy One. The term'
        ' is rare in the LXX and likely evokes the OT anointing oil (מִשְׁחָה,'
        ' mišḥāh) poured on priests and tabernacle furnishings.',
        '',
        '- **Two Hebrew verbs:** מָשַׁח (māšaḥ) is the primary cultic/royal'
        ' anointing verb; סוּךְ (sûk, 9 occurrences) is the everyday word'
        ' for rubbing/oiling the body (2 Sam 12:20; Dan 10:3; Ruth 3:3).'
        ' The LXX does not consistently render סוּךְ with χρίω.',
        '',
        '---',
        '',
        '## NT Greek Terms',
        '',
        '![NT anoint distribution](anoint-nt-distribution.png)',
        '',
    ]

    for strongs, lemma, gloss in NT_TERMS:
        hits = nt[nt['strongs'] == strongs]
        refs = hits[['book_id', 'chapter', 'verse']].drop_duplicates()
        count = len(hits)
        if count == 0:
            continue

        by_book = hits.groupby('book_id').size()
        book_summary = ', '.join(
            f'{NT_BOOK_NAMES.get(b, b)} ({c})'
            for b, c in by_book.sort_values(ascending=False).items()
        )

        lines += [
            f'### {lemma} ({strongs})',
            '',
            f'**Gloss:** {gloss}  ',
            f'**NT occurrences:** {count}  ',
            f'**Distribution:** {book_summary}',
            '',
            '| Reference | KJV text (excerpt) |',
            '|---|---|',
        ]
        for _, r in refs.sort_values(['book_id', 'chapter', 'verse']).iterrows():
            bname = NT_BOOK_NAMES.get(r['book_id'], r['book_id'])
            text = _kjv_ref(df, r['book_id'], int(r['chapter']), int(r['verse']), 'TAGNT')
            lines.append(f'| {bname} {r["chapter"]}:{r["verse"]} | {text} |')
        lines.append('')

    lines += [
        '---',
        '',
        '## LXX Greek Terms',
        '',
        'The LXX (Septuagint) is the primary Greek translation of the Hebrew OT'
        ' and is the version most NT authors cite when quoting scripture.'
        ' Its word choices directly shape NT vocabulary.',
        '',
        '![χρίω in LXX](anoint-lxx-distribution.png)',
        '',
        '### χρίω (G5548) in the LXX',
        '',
    ]

    chrio_lxx_df = lxx[(lxx['strongs'] == 'G5548') & (~lxx['is_deuterocanon'])]
    by_book_lxx = chrio_lxx_df.groupby('book_id').size().sort_values(ascending=False)
    lines += [
        f'**Canonical OT occurrences:** {len(chrio_lxx_df)}  ',
        f'**Books:** {len(by_book_lxx)}',
        '',
        '| Book | Count |',
        '|---|---:|',
    ]
    for book, cnt in by_book_lxx.items():
        lines.append(f'| {OT_BOOK_NAMES.get(book, book)} | {cnt} |')
    lines.append('')

    # χρῖσις in LXX
    chrisis = lxx[lxx['lemma'] == 'χρῖσις']
    if len(chrisis) > 0:
        by_book_chrisis = chrisis.groupby('book_id').size().sort_values(ascending=False)
        lines += [
            '### χρῖσις (anointing, noun) in the LXX',
            '',
            f'**Occurrences:** {len(chrisis)}  ',
            '**Distribution:** ' + ', '.join(
                f'{OT_BOOK_NAMES.get(b, b)} ({c})'
                for b, c in by_book_chrisis.items()
            ),
            '',
        ]

    # χρῖσμα in LXX
    chrisma_lxx = lxx[lxx['strongs'] == 'G5545']
    if len(chrisma_lxx) > 0:
        lines += [
            '### χρῖσμα (G5545) in the LXX',
            '',
            f'**Occurrences:** {len(chrisma_lxx)}  ',
            '**Distribution:** ' + ', '.join(
                f'{OT_BOOK_NAMES.get(b, b)} ({c})'
                for b, c in chrisma_lxx.groupby('book_id').size().items()
            ),
            '',
        ]

    # χριστός in LXX (including deuterocanon)
    christos_lxx = lxx[lxx['lemma'] == 'χριστός']
    if len(christos_lxx) > 0:
        lines += [
            '### χριστός (Anointed One) in the LXX',
            '',
            f'**Occurrences:** {len(christos_lxx)}  ',
            '**Distribution:** ' + ', '.join(
                f'{OT_BOOK_NAMES.get(b, b)} ({c})'
                for b, c in christos_lxx.groupby('book_id').size().items()
            ),
            '',
        ]

    lines += [
        '---',
        '',
        '## Biblical Hebrew Terms',
        '',
        '![Hebrew anoint roots](anoint-hebrew-distribution.png)',
        '',
    ]

    for root, translit, gloss, _ in HEB_TERMS:
        sub = heb[heb['root'] == root]
        count = len(sub)
        if count == 0:
            continue
        by_book = sub.groupby('book_id').size().sort_values(ascending=False)
        book_summary = ', '.join(
            f'{OT_BOOK_NAMES.get(b, b)} ({c})'
            for b, c in by_book.items()
        )

        # Sample word forms
        word_forms = sub['word'].value_counts().head(3)
        forms_str = ', '.join(
            f'{w} ({c}x)' for w, c in word_forms.items()
        )

        lines += [
            f'### {translit} ({root})',
            '',
            f'**Gloss:** {gloss}  ',
            f'**Occurrences:** {count}  ',
            f'**Distribution:** {book_summary}  ',
            f'**Common forms:** {forms_str}',
            '',
        ]

    lines += [
        '---',
        '',
        '## Cross-Corpus Connections',
        '',
        '| Hebrew (BH) | LXX Greek | NT Greek | Concept |',
        '|---|---|---|---|',
        '| מָשַׁח (māšaḥ, H4886) | χρίω (G5548) | χρίω (G5548) |'
        ' To anoint / consecrate for office |',
        '| מָשִׁיחַ (māšîaḥ, H4899) | χριστός (G5547) | χριστός (G5547) |'
        ' The Anointed One / Messiah / Christ |',
        '| מִשְׁחָה (mišḥāh, H4888) | χρῖσις / χρῖσμα | χρῖσμα (G5545) |'
        ' The anointing oil / act of anointing |',
        '| סוּךְ (sûk, H5480) | (no fixed equivalent) | ἀλείφω (G0218) |'
        ' Everyday anointing / rubbing with oil |',
        '| — | — | ἀλείφω (G0218) | Physical anointing (sick, burial, hospitality) |',
        '| — | — | ἐπιχρίω (G2025) | Spread / rub on (Jesus making clay, John 9) |',
        '| — | — | μυρίζω (G3462) | Anoint with myrrh/perfume |',
        '| — | — | ἐγχρίω (G1472) | Anoint (Rev 3:18 — counsel to Laodicea) |',
        '',
        '> **Theological note:** The LXX\'s consistent rendering of מָשַׁח with χρίω'
        ' meant that Greek-speaking Jews already associated χριστός with the'
        ' royal-priestly anointing of the OT. When the NT proclaims Jesus as'
        ' ὁ χριστός, it draws on this entire OT anointing tradition — priest,'
        ' king, and prophet (Luke 4:18, quoting Isa 61:1, itself a מָשַׁח'
        ' passage rendered by the LXX with χρίω).',
        '',
        '---',
        '',
        '## Summary Table',
        '',
        '| Term | Language | Strongs/Root | Occurrences | Primary Context |',
        '|---|---|---|---:|---|',
    ]

    # NT terms
    for strongs, lemma, gloss in NT_TERMS:
        ct = len(nt[nt['strongs'] == strongs])
        if ct == 0:
            continue
        lines.append(f'| {lemma} | NT Greek | {strongs} | {ct} | {gloss} |')

    # LXX χρίω
    lines.append(
        f'| χρίω | LXX Greek | G5548 | {len(chrio_lxx_df)}'
        ' | Translates māšaḥ throughout OT |'
    )

    # Hebrew terms
    for root, translit, gloss, _ in HEB_TERMS:
        ct = len(heb[heb['root'] == root])
        lines.append(f'| {translit} | Biblical Hebrew | {root} | {ct} | {gloss} |')

    lines += [
        '',
        '---',
        '',
        '*Greek NT data: TAGNT (Byzantine/Textus Receptus, STEPBible CC BY 4.0).*  ',
        '*LXX data: CenterBLC LXX (CC BY 4.0).*  ',
        '*Hebrew data: TAHOT (STEPBible CC BY 4.0, Tyndale House Cambridge).*  ',
        '*Generated by [scripts/nt/lexicon/build_anoint_word_study.py]'
        '(../../../../scripts/nt/lexicon/build_anoint_word_study.py).*',
    ]

    out = REPORT_DIR / 'anoint-word-study.md'
    out.write_text('\n'.join(lines), encoding='utf-8')
    print(f'  Saved {out}')
    return out


def build_csv(df: pd.DataFrame, lxx: pd.DataFrame,
              heb: pd.DataFrame) -> Path:
    nt = df[df['source'] == 'TAGNT']
    rows = []

    for strongs, lemma, gloss in NT_TERMS:
        hits = nt[nt['strongs'] == strongs]
        for _, r in hits[['book_id', 'chapter', 'verse']].drop_duplicates().iterrows():
            rows.append({
                'corpus': 'NT', 'term': lemma, 'strongs': strongs,
                'gloss': gloss,
                'book': r['book_id'], 'chapter': r['chapter'], 'verse': r['verse'],
            })

    chrio_lxx = lxx[(lxx['strongs'] == 'G5548') & (~lxx['is_deuterocanon'])]
    for _, r in chrio_lxx[['book_id', 'chapter', 'verse']].drop_duplicates().iterrows():
        rows.append({
            'corpus': 'LXX', 'term': 'χρίω', 'strongs': 'G5548',
            'gloss': 'anoint (LXX)',
            'book': r['book_id'], 'chapter': r['chapter'], 'verse': r['verse'],
        })

    for root, translit, gloss, _ in HEB_TERMS:
        for _, r in heb[heb['root'] == root][['book_id', 'chapter', 'verse']].drop_duplicates().iterrows():  # noqa: E501
            rows.append({
                'corpus': 'BH', 'term': translit, 'strongs': root,
                'gloss': gloss,
                'book': r['book_id'], 'chapter': r['chapter'], 'verse': r['verse'],
            })

    out_df = pd.DataFrame(rows)
    out = REPORT_DIR / 'anoint-word-study.csv'
    out_df.to_csv(out, index=False)
    print(f'  Saved {out}')
    return out


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('Loading data...')
    df = _db.load()
    lxx = _db.load_lxx()
    heb = df[df['source'] == 'TAHOT'].copy()
    heb['root'] = heb['strongs'].apply(extract_root)

    print('Building charts...')
    nt = df[df['source'] == 'TAGNT']
    chart_nt_distribution(nt)
    chart_lxx_distribution(lxx)
    chart_hebrew_distribution(heb)

    print('Building report...')
    build_report(df, lxx, heb)

    print('Building CSV...')
    build_csv(df, lxx, heb)

    print('Done.')
