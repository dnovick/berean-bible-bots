"""Build NT Suffering word study report.

Covers the major Greek vocabulary of suffering, affliction, endurance,
and the Christ-pattern in the NT, with distribution charts and a
topical theological report.

Outputs:
  output/reports/nt/lexicon/suffering-word-study/suffering-word-study.md
  output/reports/nt/lexicon/suffering-word-study/suffering-nt-heatmap.png
  output/reports/nt/lexicon/suffering-word-study/suffering-by-author.png
  output/reports/nt/lexicon/suffering-word-study/suffering-word-study.csv
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.patches as mpatches  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, '.')
from src.bible_grammar.core import db as _db  # noqa: E402

REPORT_DIR = Path('output/reports/nt/lexicon/suffering-word-study')
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ── Core vocabulary ───────────────────────────────────────────────────────────
# (strongs, lemma, gloss, semantic_group)
TERMS: list[tuple[str, str, str, str]] = [
    # Suffering / affliction
    ('G2347', 'θλῖψις',        'tribulation, affliction, distress',        'Affliction'),
    ('G2346', 'θλίβω',         'to press, afflict, oppress',               'Affliction'),
    ('G3958', 'πάσχω',         'to suffer, experience',                    'Affliction'),
    ('G3804', 'πάθημα',        'suffering, passion (n)',                   'Affliction'),
    ('G3806', 'πάθος',         'passion, suffering (n)',                   'Affliction'),
    ('G4730', 'στενοχωρία',    'distress, anguish',                        'Affliction'),
    ('G2553', 'κακοπαθέω',     'to suffer hardship, endure evil',          'Affliction'),
    ('G2552', 'κακοπαθής',     'suffering hardship (adj)',                 'Affliction'),
    ('G4777', 'συγκακοπαθέω',  'to suffer together, share in hardship',    'Affliction'),
    ('G4841', 'συμπάσχω',      'to suffer together with',                  'Affliction'),
    # Persecution
    ('G1375', 'διωγμός',       'persecution',                              'Persecution'),
    ('G1377', 'διώκω',         'to persecute, pursue',                     'Persecution'),
    ('G2558', 'κακουχέω',      'to mistreat, torment',                     'Persecution'),
    # Endurance / patience
    ('G5278', 'ὑπομένω',       'to endure, remain under, persevere',       'Endurance'),
    ('G5281', 'ὑπομονή',       'endurance, steadfastness, patience',       'Endurance'),
    ('G3114', 'μακροθυμέω',    'to be patient, long-suffering',            'Endurance'),
    ('G3115', 'μακροθυμία',    'patience, long-suffering, forbearance',    'Endurance'),
    # Testing / proving
    ('G3986', 'πειρασμός',     'trial, temptation, testing',               'Testing'),
    ('G1382', 'δοκιμή',        'proven character, proof (from testing)',   'Testing'),
    ('G1383', 'δοκίμιον',      'testing, means of proof',                  'Testing'),
]

# ── NT book data ──────────────────────────────────────────────────────────────
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

# Book verse counts (approximate, for rate calculations)
VERSE_COUNTS = {
    'Mat': 1071, 'Mrk': 678, 'Luk': 1151, 'Jhn': 879, 'Act': 1007,
    'Rom': 433, '1Co': 437, '2Co': 257, 'Gal': 149, 'Eph': 155,
    'Php': 104, 'Col': 95, '1Th': 89, '2Th': 47, '1Ti': 113,
    '2Ti': 83, 'Tit': 46, 'Phm': 25, 'Heb': 303, 'Jas': 108,
    '1Pe': 105, '2Pe': 61, '1Jn': 105, '2Jn': 13, '3Jn': 14,
    'Jud': 25, 'Rev': 404,
}

AUTHORS = {
    'Paul':    ['Rom', '1Co', '2Co', 'Gal', 'Eph', 'Php', 'Col',
                '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm'],
    'Luke':    ['Luk', 'Act'],
    'John':    ['Jhn', '1Jn', '2Jn', '3Jn', 'Rev'],
    'Peter':   ['1Pe', '2Pe'],
    'Matthew': ['Mat'],
    'Mark':    ['Mrk'],
    'Hebrews': ['Heb'],
    'General': ['Jas', 'Jud'],
}

GROUP_COLORS = {
    'Affliction':  '#C0392B',
    'Persecution': '#E67E22',
    'Endurance':   '#2980B9',
    'Testing':     '#27AE60',
}


def verse_ref(book: str, ch: int, vs: int) -> str:
    return f'{NT_BOOK_NAMES.get(book, book)} {ch}:{vs}'


def kjv_text(df: pd.DataFrame, book: str, ch: int, vs: int) -> str:
    rows = df[(df['book_id'] == book) & (df['chapter'] == ch) &
              (df['verse'] == vs) & (df['source'] == 'TAGNT')]
    text = ' '.join(
        str(t).strip().rstrip('¶').strip()
        for t in rows['translation'].dropna()
        if str(t).strip()
    )
    return (text[:120] + '…') if len(text) > 120 else text


# ── Chart 1: Heatmap — top terms × books ─────────────────────────────────────

def chart_heatmap(nt: pd.DataFrame) -> Path:
    """Heatmap of suffering vocabulary occurrences per book."""
    # Use only terms with meaningful NT occurrence counts (≥5)
    active = [(s, l, g, grp) for s, l, g, grp in TERMS
              if len(nt[nt['strongs'] == s]) >= 4]

    books_with_hits: set[str] = set()
    data: dict[str, dict[str, int]] = {}
    for s, l, _, _ in active:
        data[l] = {}
        for book, cnt in nt[nt['strongs'] == s].groupby('book_id').size().items():
            data[l][book] = int(cnt)
            books_with_hits.add(book)

    books = [b for b in NT_BOOK_ORDER if b in books_with_hits]
    book_labels = [NT_BOOK_NAMES.get(b, b) for b in books]
    lemmas = [l for _, l, _, _ in active]
    groups = [grp for _, _, _, grp in active]

    mat = np.zeros((len(lemmas), len(books)), dtype=int)
    for i, (_, lemma, _, _) in enumerate(active):
        for j, book in enumerate(books):
            mat[i, j] = data[lemma].get(book, 0)

    fig, ax = plt.subplots(figsize=(max(12, len(books) * 0.65 + 2),
                                    len(lemmas) * 0.55 + 2.5))
    im = ax.imshow(mat, aspect='auto', cmap='Reds', vmin=0)

    ax.set_xticks(range(len(books)))
    ax.set_xticklabels(book_labels, rotation=45, ha='right', fontsize=8)
    ax.set_yticks(range(len(lemmas)))
    ax.set_yticklabels(lemmas, fontsize=9)

    # Color ytick labels by semantic group
    for tick, grp in zip(ax.get_yticklabels(), groups):
        tick.set_color(GROUP_COLORS.get(grp, '#333333'))

    for i in range(len(lemmas)):
        for j in range(len(books)):
            v = mat[i, j]
            if v > 0:
                mx = mat[i].max() or 1
                color = 'white' if v / mx > 0.55 else '#333333'
                ax.text(j, i, str(v), ha='center', va='center',
                        fontsize=7.5, color=color, fontweight='bold')

    legend_patches = [mpatches.Patch(color=c, label=g)
                      for g, c in GROUP_COLORS.items()]
    ax.legend(handles=legend_patches, loc='upper right',
              fontsize=8, framealpha=0.85)

    ax.set_title('NT Suffering Vocabulary — Occurrences by Book',
                 fontsize=11, fontweight='bold', pad=10)
    plt.colorbar(im, ax=ax, shrink=0.5, label='Occurrences')
    plt.tight_layout()
    out = REPORT_DIR / 'suffering-nt-heatmap.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved {out}')
    return out


# ── Chart 2: Grouped bar — by author group ────────────────────────────────────

def chart_by_author(nt: pd.DataFrame) -> Path:
    """Grouped bar: suffering vocabulary density per 100 verses by author."""
    groups = ['Affliction', 'Persecution', 'Endurance', 'Testing']
    author_order = ['Paul', 'Hebrews', '1 Peter', 'James/Jude',
                    'Luke/Acts', 'John', 'Matthew', 'Mark']

    # Map author label → books
    author_books = {
        'Paul':       AUTHORS['Paul'],
        'Hebrews':    ['Heb'],
        '1 Peter':    ['1Pe'],
        'James/Jude': ['Jas', 'Jud'],
        'Luke/Acts':  AUTHORS['Luke'],
        'John':       AUTHORS['John'],
        'Matthew':    ['Mat'],
        'Mark':       ['Mrk'],
    }

    # Collect group totals per author
    group_strongs: dict[str, list[str]] = {g: [] for g in groups}
    for s, _, _, grp in TERMS:
        if grp in group_strongs:
            group_strongs[grp].append(s)

    rates: dict[str, dict[str, float]] = {}
    for author, books in author_books.items():
        total_verses = sum(VERSE_COUNTS.get(b, 0) for b in books)
        rates[author] = {}
        for grp in groups:
            ct = sum(
                len(nt[(nt['strongs'] == s) & (nt['book_id'].isin(books))])
                for s in group_strongs[grp]
            )
            rates[author][grp] = (ct / total_verses * 100) if total_verses else 0

    x = np.arange(len(author_order))
    n_grp = len(groups)
    width = 0.8 / n_grp

    fig, ax = plt.subplots(figsize=(12, 5))
    for i, grp in enumerate(groups):
        vals = [rates[a][grp] for a in author_order]
        offset = (i - n_grp / 2 + 0.5) * width
        ax.bar(x + offset, vals, width=width * 0.9,
               color=GROUP_COLORS[grp], label=grp, alpha=0.9)

    ax.set_xticks(x)
    ax.set_xticklabels(author_order, fontsize=9)
    ax.set_ylabel('Occurrences per 100 verses')
    ax.set_title('NT Suffering Vocabulary — Density by Author Group',
                 fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    plt.tight_layout()
    out = REPORT_DIR / 'suffering-by-author.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved {out}')
    return out


# ── Report ────────────────────────────────────────────────────────────────────

def build_report(df: pd.DataFrame) -> Path:
    nt = df[df['source'] == 'TAGNT']

    # Pre-compute counts
    counts = {s: len(nt[nt['strongs'] == s]) for s, _, _, _ in TERMS}
    thlipsis = counts['G2347']
    pascho = counts['G3958']
    pathema = counts['G3804']
    hypomone = counts['G5281']
    hupomeno = counts['G5278']
    diogmos = counts['G1375']
    peirasmos = counts['G3986']
    dokime = counts['G1382']

    lines = [
        '# Suffering in the Life of the Believer — NT Word Study',
        '',
        '**Corpus:** Greek NT (TAGNT, Byzantine/Textus Receptus)  ',
        '**Translation:** KJV',
        '',
        '## Contents',
        '',
        '- [Overview](#overview)',
        '- [Key Observations](#key-observations)',
        '- [Vocabulary of Suffering](#vocabulary-of-suffering)',
        '  - [θλῖψις — Tribulation and Affliction](#θλῖψις--tribulation-and-affliction)',
        '  - [πάσχω / πάθημα — To Suffer / Suffering](#πάσχω--πάθημα--to-suffer--suffering)',
        '  - [διωγμός / διώκω — Persecution](#διωγμός--διώκω--persecution)',
        '  - [ὑπομονή / ὑπομένω — Endurance](#ὑπομονή--ὑπομένω--endurance)',
        '  - [πειρασμός / δοκιμή — Trial and Proven Character](#πειρασμός--δοκιμή--trial-and-proven-character)',
        '- [Christ as the Pattern and Ground of Suffering](#christ-as-the-pattern-and-ground-of-suffering)',
        '- [Suffering as Participation in Christ](#suffering-as-participation-in-christ)',
        '- [The Purpose of Suffering in the NT](#the-purpose-of-suffering-in-the-nt)',
        '- [Key Passages by Author](#key-passages-by-author)',
        '- [Distribution Charts](#distribution-charts)',
        '- [Summary Table](#summary-table)',
        '',
        '---',
        '',
        '## Overview',
        '',
        'The NT does not treat suffering as an anomaly in the Christian life but as'
        ' an expected, even appointed, feature of it. Four interlocking themes'
        ' organize the NT\'s teaching:',
        '',
        '1. **Christ\'s own sufferings were divinely ordained** — the servant of'
        ' Isa 53 who was "bruised for our iniquities," the Son who "learned obedience'
        ' by the things which he suffered" (Heb 5:8).',
        '2. **Believers are called into a pattern of suffering that mirrors Christ\'s'
        ' own** — "if we suffer with him, that we may be also glorified together"'
        ' (Rom 8:17).',
        '3. **Suffering is purposive, not punitive** — it produces endurance,'
        ' proven character, and hope (Rom 5:3–4); it conforms believers to Christ'
        ' (Phil 3:10); it glorifies God (1 Pet 4:16).',
        '4. **The suffering of the present age stands in deliberate contrast to the'
        ' coming glory** — "the sufferings of this present time are not worth'
        ' comparing with the glory which shall be revealed" (Rom 8:18).',
        '',
        '---',
        '',
        '## Key Observations',
        '',
        f'- **θλῖψις ({thlipsis} NT occurrences)** is the dominant noun for'
        ' affliction. It literally means "pressure" or "crushing." The term'
        ' covers external opposition (persecution, hardship) and internal distress.'
        ' Jesus himself predicts it as the normal lot of his disciples'
        ' (John 16:33: "In the world ye shall have tribulation").',
        '',
        f'- **πάσχω ({pascho} occurrences)** is distributed almost equally between'
        ' Christ\'s own sufferings and those of believers — a deliberate lexical'
        ' link. In 1 Peter πάσχω appears 12 times, more than any other NT book,'
        ' and almost always Christ\'s suffering serves as the explicit ground or'
        ' pattern for the believer\'s.',
        '',
        f'- **πάθημα ({pathema} occurrences)** appears in two key Pauline texts'
        ' that explicitly connect the believer\'s sufferings with Christ\'s:'
        ' Rom 8:18 ("the sufferings of this present time") and 2 Cor 1:5'
        ' ("as the sufferings of Christ abound in us").',
        '',
        f'- **ὑπομονή ({hypomone} occurrences)** is the characteristic NT response'
        ' to suffering — active, purposeful endurance rather than passive resignation.'
        ' It appears in every major author who addresses suffering: Paul, James,'
        ' Peter, Hebrews, and Revelation.',
        '',
        '- **The suffering–glory axis** (e.g. Rom 8:17–18; 1 Pet 5:10; 2 Cor 4:17;'
        ' Rev 7:14) is the most consistent structural feature of NT suffering'
        ' theology. The same pattern appears in Christ himself:'
        ' "the sufferings of Christ and the glory that should follow" (1 Pet 1:11).',
        '',
        '- **1 Peter and 2 Corinthians** are the two densest loci of NT suffering'
        ' theology. 1 Peter addresses communities under social ostracism and'
        ' possible state persecution; 2 Corinthians is Paul\'s most autobiographical'
        ' account of apostolic suffering as evidence of divine power.',
        '',
        '---',
        '',
        '## Vocabulary of Suffering',
        '',
        '### θλῖψις — Tribulation and Affliction',
        '',
        f'**G2347 θλῖψις, -εως, ἡ** | {thlipsis} NT occurrences',
        '',
        'The root meaning is physical pressure or constriction (from θλίβω, to press).'
        ' In the NT it is the primary word for the affliction that characterizes life'
        ' in a fallen age. It is never accidental — Jesus promises it (John 16:33),'
        ' Paul says "we must through much tribulation enter into the kingdom of God"'
        ' (Acts 14:22), and the Thessalonian letters treat it as the appointed lot'
        ' of the called (1 Thess 3:3–4).',
        '',
        '**Distribution by book:**',
        '',
    ]

    thlipsis_df = nt[nt['strongs'] == 'G2347']
    by_book = thlipsis_df.groupby('book_id').size().sort_values(ascending=False)
    lines.append('| Book | Count |')
    lines.append('|---|---:|')
    for bk, ct in by_book.items():
        lines.append(f'| {NT_BOOK_NAMES.get(bk, bk)} | {ct} |')
    lines.append('')

    lines += [
        '**Key texts:**',
        '',
        '| Reference | KJV |',
        '|---|---|',
    ]
    key_refs_thlipsis = [
        ('Jhn', 16, 33), ('Act', 14, 22), ('Rom', 5, 3),
        ('Rom', 8, 35), ('2Co', 1, 4), ('1Th', 3, 3), ('Rev', 7, 14),
    ]
    for bk, ch, vs in key_refs_thlipsis:
        lines.append(f'| {verse_ref(bk, ch, vs)} | {kjv_text(df, bk, ch, vs)} |')
    lines.append('')

    lines += [
        '---',
        '',
        '### πάσχω / πάθημα — To Suffer / Suffering',
        '',
        f'**G3958 πάσχω** (verb) | {pascho} NT occurrences  ',
        f'**G3804 πάθημα, -ατος, τό** (noun) | {pathema} NT occurrences',
        '',
        'πάσχω means to experience or undergo something — usually painful. What'
        ' is theologically significant is how the NT **distributes** its usage:'
        ' roughly half the occurrences refer to Christ\'s own sufferings,'
        ' and half to believers\'. This is not coincidental. Peter explicitly'
        ' structures his argument on the pattern: Christ suffered → you will suffer'
        ' → suffer as he suffered (1 Pet 2:21–23; 3:17–18; 4:1).',
        '',
        'πάθημα (the noun) is especially important in Paul. In 2 Cor 1:5 he speaks'
        ' of "the sufferings of Christ" (παθήματα τοῦ Χριστοῦ) overflowing into'
        ' the apostle — a sharing in the ongoing significance of Christ\'s'
        ' suffering-pattern, not a supplement to the atonement.',
        '',
        '**Key texts:**',
        '',
        '| Reference | KJV |',
        '|---|---|',
    ]
    key_refs_pascho = [
        ('Luk', 24, 26), ('Act', 17, 3), ('Rom', 8, 17),
        ('2Co', 1, 5), ('Php', 1, 29), ('Php', 3, 10),
        ('1Pe', 2, 21), ('1Pe', 4, 1), ('Heb', 5, 8),
    ]
    for bk, ch, vs in key_refs_pascho:
        lines.append(f'| {verse_ref(bk, ch, vs)} | {kjv_text(df, bk, ch, vs)} |')
    lines.append('')

    lines += [
        '---',
        '',
        '### διωγμός / διώκω — Persecution',
        '',
        f'**G1375 διωγμός, -οῦ, ὁ** | {diogmos} NT occurrences  ',
        f'**G1377 διώκω** | {counts["G1377"]} NT occurrences',
        '',
        'διωγμός refers specifically to active, hostile pursuit — persecution by'
        ' opponents. Jesus lists it alongside θλῖψις in the parable of the sower'
        ' (Matt 13:21) as the pressure that causes the word to be abandoned. Paul'
        ' catalogues his own persecutions in 2 Cor 12:10 and 2 Tim 3:11, and in'
        ' 2 Tim 3:12 states the broadest principle: "All that will live godly in'
        ' Christ Jesus shall suffer persecution."',
        '',
        '**Key texts:**',
        '',
        '| Reference | KJV |',
        '|---|---|',
    ]
    key_refs_diogmos = [
        ('Mat', 5, 10), ('Mat', 13, 21), ('Rom', 8, 35),
        ('2Co', 12, 10), ('2Ti', 3, 12), ('Heb', 10, 33),
    ]
    for bk, ch, vs in key_refs_diogmos:
        lines.append(f'| {verse_ref(bk, ch, vs)} | {kjv_text(df, bk, ch, vs)} |')
    lines.append('')

    lines += [
        '---',
        '',
        '### ὑπομονή / ὑπομένω — Endurance',
        '',
        f'**G5281 ὑπομονή, -ῆς, ἡ** | {hypomone} NT occurrences  ',
        f'**G5278 ὑπομένω** | {hupomeno} NT occurrences',
        '',
        'ὑπομονή is often translated "patience" in the KJV, but the word carries'
        ' the force of **active perseverance under pressure** — staying under a'
        ' load, not running from it. It is distinct from μακροθυμία (patience'
        ' toward people) and always has a forward, hopeful orientation:'
        ' "tribulation worketh patience; and patience, experience; and experience,'
        ' hope" (Rom 5:3–4). The letter of James opens with this logic'
        ' (Jas 1:3–4), as does Hebrews (Heb 12:1).',
        '',
        '| Reference | KJV |',
        '|---|---|',
    ]
    key_refs_hypomone = [
        ('Rom', 5, 3), ('Rom', 5, 4), ('Heb', 10, 36),
        ('Heb', 12, 1), ('Jas', 1, 3), ('Rev', 13, 10),
    ]
    for bk, ch, vs in key_refs_hypomone:
        lines.append(f'| {verse_ref(bk, ch, vs)} | {kjv_text(df, bk, ch, vs)} |')
    lines.append('')

    lines += [
        '---',
        '',
        '### πειρασμός / δοκιμή — Trial and Proven Character',
        '',
        f'**G3986 πειρασμός, -οῦ, ὁ** | {peirasmos} NT occurrences  ',
        f'**G1382 δοκιμή, -ῆς, ἡ** | {dokime} NT occurrences',
        '',
        'πειρασμός covers both temptation (internal moral solicitation) and external'
        ' trial or testing. In contexts of suffering the focus is the latter: the'
        ' fire that tests the gold (1 Pet 1:7). The result of endured trial is'
        ' δοκιμή — proven, tested character. The word is used in metallurgy for'
        ' metal that has passed the refiner\'s test. Paul\'s chain in Rom 5:3–4'
        ' (tribulation → endurance → proven character → hope) and James\'s parallel'
        ' in Jas 1:3–4 both move from suffering through testing to a productive end.',
        '',
        '| Reference | KJV |',
        '|---|---|',
    ]
    key_refs_peirasmos = [
        ('Jas', 1, 2), ('Jas', 1, 12), ('1Pe', 1, 6),
        ('1Pe', 1, 7), ('Rom', 5, 4), ('2Co', 8, 2),
    ]
    for bk, ch, vs in key_refs_peirasmos:
        lines.append(f'| {verse_ref(bk, ch, vs)} | {kjv_text(df, bk, ch, vs)} |')
    lines.append('')

    lines += [
        '---',
        '',
        '## Christ as the Pattern and Ground of Suffering',
        '',
        'The NT is unanimous that Christ\'s sufferings were not merely biographical'
        ' events but **divinely ordained** and **theologically constitutive**'
        ' for what follows. Several texts establish this:',
        '',
        '**The necessity of Christ\'s suffering (ἔδει):**',
        '',
        '| Reference | KJV |',
        '|---|---|',
    ]
    key_refs_christ = [
        ('Luk', 24, 26), ('Luk', 24, 46), ('Act', 17, 3),
        ('Act', 3, 18), ('Heb', 2, 10), ('Heb', 5, 8),
        ('1Pe', 1, 11), ('1Pe', 2, 21),
    ]
    for bk, ch, vs in key_refs_christ:
        lines.append(f'| {verse_ref(bk, ch, vs)} | {kjv_text(df, bk, ch, vs)} |')
    lines += [
        '',
        '> **Note:** Luke 24:26 ("Ought not Christ to have suffered these things,'
        ' and to enter into his glory?") uses ἔδει — the imperfect of necessity.'
        ' This is not regret but divine necessity: the suffering was the appointed'
        ' path to the glory. The identical structure (suffering → glory) is then'
        ' applied to believers in Rom 8:17, 1 Pet 5:10, and Rev 7:14.',
        '',
        'Hebrews 5:8 makes a remarkable claim: "though he were a Son, yet learned'
        ' he obedience by the things which he suffered." The sinless Son did not'
        ' need moral correction; he underwent suffering as the instrument by which'
        ' full human obedience — the costly, tested kind — was exercised and'
        ' completed. This establishes why suffering is the path for believers too:'
        ' it is the same path the Son himself walked.',
        '',
        '---',
        '',
        '## Suffering as Participation in Christ',
        '',
        'Perhaps the NT\'s most distinctive contribution is the concept of'
        ' **solidarity in suffering** — the believer\'s suffering as participation'
        ' in Christ\'s own:',
        '',
        '| Text | Theme |',
        '|---|---|',
        '| Rom 8:17 | "If we suffer with him (συμπάσχομεν), that we may be also glorified together" |',
        '| 2 Cor 1:5 | "The sufferings of Christ abound in us" (παθήματα τοῦ Χριστοῦ) |',
        '| Phil 3:10 | "The fellowship of his sufferings" (κοινωνία παθημάτων αὐτοῦ) |',
        '| Col 1:24 | "Fill up what is lacking in the afflictions of Christ in my flesh" |',
        '| 1 Pet 4:13 | "Partakers of Christ\'s sufferings" (κοινωνεῖτε τοῖς τοῦ Χριστοῦ παθήμασιν) |',
        '| Heb 13:13 | "Let us go forth to him outside the camp, bearing his reproach" |',
        '',
        '> **Note on Col 1:24:** This is the most frequently misread suffering text.'
        ' Paul does not say the atonement is incomplete. The "afflictions of Christ"'
        ' (θλίψεων τοῦ Χριστοῦ) is a distinct phrase from "the sufferings of Christ"'
        ' in 1 Pet 1:11. Paul\'s point is that the messianic community\'s appointed'
        ' share of eschatological tribulation is something Paul, as apostle to the'
        ' Gentiles, is filling up on their behalf — a representative role, not a'
        ' soteriological supplement.',
        '',
        '---',
        '',
        '## The Purpose of Suffering in the NT',
        '',
        'The NT is explicit that God\'s purposes in the suffering of believers'
        ' are productive, not merely permissive:',
        '',
        '| Purpose | Key Text |',
        '|---|---|',
        '| Produces endurance and proven character | Rom 5:3–4; Jas 1:3–4 |',
        '| Conforms believers to Christ | Rom 8:29; Phil 3:10 |',
        '| Manifests divine power in weakness | 2 Cor 12:9–10; 4:7–12 |',
        '| Trains in holiness | Heb 12:10–11 |',
        '| Prepares eternal weight of glory | 2 Cor 4:17 |',
        '| Glorifies God, causes praise | 1 Pet 4:16; 2 Thess 1:4–5 |',
        '| Witnesses to the truth of the gospel | Phil 1:29; Acts 5:41 |',
        '| Leads to final vindication and glory | 1 Pet 5:10; Rev 7:14–17 |',
        '',
        '**The suffering–glory contrast** is the NT\'s controlling framework:'
        ' "our light and momentary troubles are achieving for us an eternal glory'
        ' that far outweighs them all" (2 Cor 4:17, NIV). The KJV\'s "exceeding'
        ' and eternal weight of glory" renders βάρος αἰώνιον — an eschatological'
        ' heaviness that dwarfs the πρόσκαιρον (momentary) affliction.',
        '',
        '---',
        '',
        '## Key Passages by Author',
        '',
        '### Paul',
        '',
        '| Reference | KJV |',
        '|---|---|',
    ]
    paul_refs = [
        ('Rom', 5, 3), ('Rom', 8, 17), ('Rom', 8, 18),
        ('2Co', 1, 5), ('2Co', 4, 17), ('2Co', 12, 9),
        ('Php', 1, 29), ('Php', 3, 10), ('Col', 1, 24),
        ('2Ti', 3, 12),
    ]
    for bk, ch, vs in paul_refs:
        lines.append(f'| {verse_ref(bk, ch, vs)} | {kjv_text(df, bk, ch, vs)} |')
    lines += ['', '### Hebrews', '', '| Reference | KJV |', '|---|---|']
    heb_refs = [
        ('Heb', 2, 10), ('Heb', 5, 8), ('Heb', 10, 36),
        ('Heb', 12, 1), ('Heb', 12, 10), ('Heb', 12, 11),
    ]
    for bk, ch, vs in heb_refs:
        lines.append(f'| {verse_ref(bk, ch, vs)} | {kjv_text(df, bk, ch, vs)} |')
    lines += ['', '### 1 Peter', '', '| Reference | KJV |', '|---|---|']
    pet_refs = [
        ('1Pe', 1, 6), ('1Pe', 1, 7), ('1Pe', 2, 21),
        ('1Pe', 3, 17), ('1Pe', 4, 1), ('1Pe', 4, 13),
        ('1Pe', 4, 16), ('1Pe', 5, 10),
    ]
    for bk, ch, vs in pet_refs:
        lines.append(f'| {verse_ref(bk, ch, vs)} | {kjv_text(df, bk, ch, vs)} |')
    lines += ['', '### James', '', '| Reference | KJV |', '|---|---|']
    jas_refs = [('Jas', 1, 2), ('Jas', 1, 3), ('Jas', 1, 4), ('Jas', 1, 12)]
    for bk, ch, vs in jas_refs:
        lines.append(f'| {verse_ref(bk, ch, vs)} | {kjv_text(df, bk, ch, vs)} |')
    lines += [
        '',
        '---',
        '',
        '## Distribution Charts',
        '',
        '![NT Suffering Vocabulary — Heatmap](suffering-nt-heatmap.png)',
        '',
        '![NT Suffering Vocabulary — By Author](suffering-by-author.png)',
        '',
        '---',
        '',
        '## Summary Table',
        '',
        '| Term | Strongs | Occurrences | Gloss | Group |',
        '|---|---|---:|---|---|',
    ]
    for s, l, g, grp in TERMS:
        ct = counts[s]
        if ct > 0:
            lines.append(f'| {l} | {s} | {ct} | {g} | {grp} |')

    lines += [
        '',
        '---',
        '',
        '*Greek NT data: TAGNT (Byzantine/Textus Receptus, STEPBible CC BY 4.0).*  ',
        '*Generated by [scripts/nt/lexicon/build_suffering_word_study.py]'
        '(../../../../scripts/nt/lexicon/build_suffering_word_study.py).*',
    ]

    out = REPORT_DIR / 'suffering-word-study.md'
    out.write_text('\n'.join(lines), encoding='utf-8')
    print(f'  Saved {out}')
    return out


def build_csv(df: pd.DataFrame) -> Path:
    nt = df[df['source'] == 'TAGNT']
    rows = []
    for s, lemma, gloss, grp in TERMS:
        hits = nt[nt['strongs'] == s]
        for _, r in hits[['book_id', 'chapter', 'verse']].drop_duplicates().iterrows():
            rows.append({
                'group': grp, 'lemma': lemma, 'strongs': s, 'gloss': gloss,
                'book': r['book_id'], 'chapter': r['chapter'], 'verse': r['verse'],
            })
    out = REPORT_DIR / 'suffering-word-study.csv'
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f'  Saved {out}')
    return out


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('Loading data...')
    df = _db.load()
    nt = df[df['source'] == 'TAGNT']

    print('Building charts...')
    chart_heatmap(nt)
    chart_by_author(nt)

    print('Building report...')
    build_report(df)

    print('Building CSV...')
    build_csv(df)

    print('Done.')
