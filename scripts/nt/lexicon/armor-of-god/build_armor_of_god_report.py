"""Build the Armor of God report for Ephesians 6:10-18.

Generates:
  output/reports/nt/lexicon/armor-of-god/armor-of-god-report.md
  output/reports/nt/lexicon/armor-of-god/armor-of-god-heatmap.png
"""

import re
import matplotlib
matplotlib.use('Agg')  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from pathlib import Path  # noqa: E402

from bible_grammar import query  # noqa: E402

REPO = Path(__file__).resolve().parents[4]
REPORT_DIR = REPO / 'output' / 'reports' / 'nt' / 'lexicon' / 'armor-of-god'
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def _slug(heading: str) -> str:
    """Replicate MkDocs Material's heading anchor generation.

    Strip non-ASCII, remove punctuation other than hyphens, lowercase,
    collapse whitespace/hyphens to a single hyphen, strip leading/trailing.
    """
    ascii_only = heading.encode('ascii', errors='ignore').decode()
    no_punct = re.sub(r'[^a-zA-Z0-9\s-]', '', ascii_only)
    slug = re.sub(r'\s+', '-', no_punct.lower())
    return re.sub(r'-{2,}', '-', slug).strip('-')


# ── Data ──────────────────────────────────────────────────────────────────────

df = query(testament='nt')
eph = df[df['book_id'] == 'Eph'].copy()

# Armor items defined in 6:14-18 with their primary Strong's prefix
# Each entry: (piece, Greek term, Strong's prefix, ESV label, verse in ch6)
ARMOR = [
    ('Belt',       'ἀλήθεια',     'G0225',  'truth',        14),
    ('Breastplate', 'δικαιοσύνη', 'G1343', 'righteousness', 14),
    ('Shoes',      'εὐαγγέλιον',  'G2098',  'gospel',        15),
    ('Shoes',      'εἰρήνη',      'G1515',  'peace',         15),
    ('Shield',     'πίστις',      'G4102',  'faith',         16),
    ('Helmet',     'σωτηρία',     'G4991',  'salvation',     17),
    ('Sword',      'ῥῆμα θεοῦ',  'G4487',  'word of God',   17),
    ('Prayer',     'προσευχή',    'G4335',  'prayer',        18),
]

# Group the two shoes terms together for the chart
PIECES = [
    ('Belt of Truth',                  ['G0225'],         14),
    ('Breastplate of Righteousness',   ['G1343'],         14),
    ('Shoes — Gospel of Peace',        ['G2098', 'G1515'], 15),
    ('Shield of Faith',                ['G4102'],         16),
    ('Helmet of Salvation',            ['G4991'],         17),
    ('Sword — Word of God (ῥῆμα)',    ['G4487'],         17),
    ('Prayer',                         ['G4335'],         18),
]

EPH_CHAPTERS = list(range(1, 7))


def hits_in_eph(strongs_prefixes: list, exclude_ch6: bool = True) -> pd.DataFrame:
    """Return all Ephesians rows matching any of the given Strong's prefixes."""
    mask = eph['strongs'].fillna('').apply(
        lambda s: any(s.startswith(p) for p in strongs_prefixes)
    )
    rows = eph[mask].copy()
    if exclude_ch6:
        rows = rows[rows['chapter'] != 6]
    return rows


def ref_list(rows: pd.DataFrame) -> list:
    """Return sorted list of 'N:N' reference strings."""
    refs = rows[['chapter', 'verse']].drop_duplicates().sort_values(['chapter', 'verse'])
    return [f"{r.chapter}:{r.verse}" for r in refs.itertuples()]


# ── Chart: heatmap — which armor words appear in which chapters ───────────────

def build_heatmap() -> Path:
    piece_labels = [p[0] for p in PIECES]
    ch_labels = [f'Ch {c}' for c in EPH_CHAPTERS[:-1]]  # ch1–5 (exclude ch6)

    data = np.zeros((len(PIECES), len(EPH_CHAPTERS) - 1), dtype=int)
    for i, (piece, prefixes, _) in enumerate(PIECES):
        for j, ch in enumerate(EPH_CHAPTERS[:-1]):
            mask = eph['strongs'].fillna('').apply(
                lambda s: any(s.startswith(p) for p in prefixes)
            )
            data[i, j] = eph[mask & (eph['chapter'] == ch)].shape[0]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    cmap = plt.get_cmap('Blues')
    im = ax.imshow(data, aspect='auto', cmap=cmap, vmin=0, vmax=data.max() or 1)

    ax.set_xticks(range(len(ch_labels)))
    ax.set_xticklabels(ch_labels, fontsize=10)
    ax.set_yticks(range(len(piece_labels)))
    ax.set_yticklabels(piece_labels, fontsize=9.5)

    for i in range(len(PIECES)):
        for j in range(len(EPH_CHAPTERS) - 1):
            val = data[i, j]
            if val > 0:
                color = 'white' if val >= data.max() * 0.6 else '#222'
                ax.text(j, i, str(val), ha='center', va='center',
                        fontsize=10, fontweight='bold', color=color)

    ax.set_title(
        'Armor of God — Key Terms in Ephesians 1–5\n(word-count occurrences per chapter)',
        fontsize=11, pad=10,
    )
    fig.colorbar(im, ax=ax, shrink=0.6, label='Occurrences')
    plt.tight_layout()
    out = REPORT_DIR / 'armor-of-god-heatmap.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'Saved {out}')
    return out


# ── Report ────────────────────────────────────────────────────────────────────

EPH_6_PASSAGE = {
    10: ("Τοῦ λοιποῦ, ἀδελφοί μου, ἐνδυναμοῦσθε ἐν κυρίῳ καὶ ἐν τῷ κράτει τῆς ἰσχύος αὐτοῦ.",
         "Finally, my brethren, be strong in the Lord, and in the power of his might."),
    11: ("ἐνδύσασθε τὴν πανοπλίαν τοῦ θεοῦ πρὸς τὸ δύνασθαι ὑμᾶς στῆναι πρὸς τὰς μεθοδείας τοῦ διαβόλου·",
         "Put on the whole armour of God, that ye may be able to stand against the wiles of the devil."),
    12: (
        "ὅτι οὐκ ἔστιν ἡμῖν ἡ πάλη πρὸς αἷμα καὶ σάρκα ἀλλὰ πρὸς τὰς ἀρχάς, πρὸς τὰς ἐξουσίας, πρὸς τοὺς κοσμοκράτορας τοῦ σκότους τοῦ αἰῶνος τούτου, πρὸς τὰ πνευματικὰ τῆς πονηρίας ἐν τοῖς ἐπουρανίοις.",  # noqa: E501
        "For we wrestle not against flesh and blood, but against principalities, against powers, against the rulers of the darkness of this world, against spiritual wickedness in high places.",  # noqa: E501
    ),
    13: (
        "διὰ τοῦτο ἀναλάβετε τὴν πανοπλίαν τοῦ θεοῦ, ἵνα δυνηθῆτε ἀντιστῆναι ἐν τῇ ἡμέρᾳ τῇ πονηρᾷ καὶ ἅπαντα κατεργασάμενοι στῆναι.",  # noqa: E501
        "Wherefore take unto you the whole armour of God, that ye may be able to withstand in the evil day, and having done all, to stand.",
    ),
    14: (
        "στῆτε οὖν περιζωσάμενοι τὴν ὀσφὺν ὑμῶν ἐν ἀληθείᾳ καὶ ἐνδυσάμενοι τὸν θώρακα τῆς δικαιοσύνης",
        "Stand therefore, having your loins girt about with truth, and having on the breastplate of righteousness;",
    ),
    15: (
        "καὶ ὑποδησάμενοι τοὺς πόδας ἐν ἑτοιμασίᾳ τοῦ εὐαγγελίου τῆς εἰρήνης·",
        "And your feet shod with the preparation of the gospel of peace;",
    ),
    16: (
        "ἐν πᾶσιν ἀναλαβόντες τὸν θυρεὸν τῆς πίστεως, ἐν ᾧ δυνήσεσθε πάντα τὰ βέλη τοῦ πονηροῦ τὰ πεπυρωμένα σβέσαι·",  # noqa: E501
        "Above all, taking the shield of faith, wherewith ye shall be able to quench all the fiery darts of the wicked.",
    ),
    17: (
        "καὶ τὴν περικεφαλαίαν τοῦ σωτηρίου δέξασθε καὶ τὴν μάχαιραν τοῦ πνεύματος, ὅ ἐστιν ῥῆμα θεοῦ·",
        "And take the helmet of salvation, and the sword of the Spirit, which is the word of God:",
    ),
    18: (
        "διὰ πάσης προσευχῆς καὶ δεήσεως προσευχόμενοι ἐν παντὶ καιρῷ ἐν πνεύματι, καὶ εἰς αὐτὸ τοῦτο ἀγρυπνοῦντες ἐν πάσῃ προσκαρτερήσει καὶ δεήσει περὶ πάντων τῶν ἁγίων",  # noqa: E501
        "Praying always with all prayer and supplication in the Spirit, and watching thereunto with all perseverance and supplication for all saints;",  # noqa: E501
    ),
}

# Detailed earlier-in-Ephesians references with contextual quotes for the report
# Structure: strongs_prefix → list of (ref, greek_snippet, translation_snippet, significance)
EARLIER_REFS = {
    'G0225': [  # truth
        ('1:13', 'τὸν λόγον τῆς ἀληθείας', 'the word of truth',
         'Truth is the very substance of the gospel by which believers were sealed'),
        ('4:21', 'καθώς ἐστιν ἀλήθεια ἐν τῷ Ἰησοῦ', 'as the truth is in Jesus',
         'Christ himself is the embodiment of truth — the foundation of the belt'),
        ('4:24', 'τὴν κατὰ θεὸν κτισθέντα ἐν δικαιοσύνῃ καὶ ὁσιότητι τῆς ἀληθείας',
         'created in righteousness and true holiness',
         'Truth and righteousness appear together — the same pairing as in 6:14'),
        ('4:25', 'λαλεῖτε ἀλήθειαν', 'speak every man truth with his neighbour',
         'Believers are called to live out the truth they have girded on'),
        ('5:9', 'ἐν … ἀληθείᾳ', 'in all goodness and righteousness and truth',
         'The fruit of light includes truth — a quality of the new life in Christ'),
    ],
    'G1343': [  # righteousness
        ('4:24', 'ἐν δικαιοσύνῃ καὶ ὁσιότητι τῆς ἀληθείας',
         'in righteousness and true holiness',
         'The new self is created in righteousness — what the breastplate protects'),
        ('5:9', 'ἐν … δικαιοσύνῃ', 'in … righteousness and truth',
         'Righteousness is a characteristic of walking as children of light'),
    ],
    'G2098': [  # gospel
        ('1:13', 'τὸν λόγον τῆς ἀληθείας, τὸ εὐαγγέλιον τῆς σωτηρίας ὑμῶν',
         'the word of truth, the gospel of your salvation',
         'The gospel is the instrument of salvation and sealing with the Spirit'),
        ('3:6', 'συγκληρονόμα … διὰ τοῦ εὐαγγελίου',
         'fellowheirs … by the gospel',
         'The gospel unites Jew and Gentile — the peace the shoes proclaim'),
    ],
    'G1515': [  # peace
        ('1:2', 'χάρις ὑμῖν καὶ εἰρήνη', 'Grace be to you, and peace',
         'Peace is Paul\'s opening benediction for the whole letter'),
        ('2:14', 'αὐτὸς γάρ ἐστιν ἡ εἰρήνη ἡμῶν', 'he is our peace',
         'Christ IS peace — the profoundest grounding of the shoes of peace'),
        ('2:15', 'ἵνα τοὺς δύο κτίσῃ ἐν αὑτῷ εἰς ἕνα καινὸν ἄνθρωπον, ποιῶν εἰρήνην',
         'to make in himself of twain one new man, so making peace',
         'Christ made peace between Jew and Gentile through the cross'),
        ('2:17', 'εὐηγγελίσατο εἰρήνην … καὶ εἰρήνην',
         'came and preached peace … and peace',
         'The gospel IS the preaching of peace — shoes and gospel belong together'),
        ('4:3', 'τὸν σύνδεσμον τῆς εἰρήνης', 'the bond of peace',
         'Peace must be maintained among believers — a calling before a weapon'),
    ],
    'G4102': [  # faith
        ('1:15', 'τὴν καθ᾽ ὑμᾶς πίστιν', 'your faith in the Lord Jesus',
         'Paul gives thanks for the Ephesians\' faith — the shield that already works'),
        ('2:8', 'διὰ πίστεως … σεσῳσμένοι', 'by grace are ye saved through faith',
         'The most famous faith verse in Ephesians — salvation itself came by this shield'),
        ('3:12', 'διὰ τῆς πίστεως αὐτοῦ', 'by the faith of him',
         'Access to God comes through faith — the same shield used in prayer (6:18)'),
        ('3:17', 'κατοικῆσαι τὸν Χριστὸν διὰ τῆς πίστεως',
         'that Christ may dwell in your hearts by faith',
         "Faith is the ground of Christ's indwelling — the shield is not external armor only"),
        ('4:5', 'μία πίστις', 'one faith',
         'One faith belongs to the whole body — the shield is shared'),
        ('4:13', 'εἰς τὴν ἑνότητα τῆς πίστεως', 'in the unity of the faith',
         'The goal of maturity is unified faith — the fully-equipped body'),
    ],
    'G4991': [  # salvation
        ('1:13', 'τὸ εὐαγγέλιον τῆς σωτηρίας ὑμῶν', 'the gospel of your salvation',
         'Salvation is the content of the gospel — what the helmet announces'),
    ],
    'G4487': [  # rhēma
        ('5:26', 'ἐν ῥήματι', 'by the word',
         'Christ sanctifies the church through the word (ῥῆμα) — the same term as the sword'),
    ],
    'G4335': [  # prayer
        ('1:16', 'μνείαν ποιούμενος ἐπὶ τῶν προσευχῶν μου',
         'making mention of you in my prayers',
         'Paul himself models the unceasing prayer he calls for in 6:18'),
    ],
}


def piece_section(piece_label: str, strongs_prefixes: list, ch6_verse: int) -> str:
    """Generate the report section for one armor piece."""
    lines = [f'### {piece_label}', '']

    # Gather earlier refs
    all_refs: list[tuple] = []
    for prefix in strongs_prefixes:
        for ref_data in EARLIER_REFS.get(prefix, []):
            all_refs.append((prefix, ref_data))

    if not all_refs:
        lines.append('*No earlier occurrences found in Ephesians.*')
        lines.append('')
        return '\n'.join(lines)

    lines.append(f'Earlier in Ephesians, before it becomes a piece of armor in {ch6_verse}:')
    lines.append('')

    for prefix, (ref, greek, trans, sig) in all_refs:
        lines.append(f'**Eph {ref}**')
        lines.append(f'> {greek}')
        lines.append('>')
        lines.append(f'> *"{trans}"*')
        lines.append('')
        lines.append(sig)
        lines.append('')

    return '\n'.join(lines)


def build_report(heatmap_path: Path) -> Path:
    sections = []

    # ── Header ────────────────────────────────────────────────────────────────
    PIECE_HEADINGS = [
        'Belt of Truth (ἀλήθεια, G0225)',
        'Breastplate of Righteousness (δικαιοσύνη, G1343)',
        'Shoes — Gospel of Peace (εὐαγγέλιον G2098 + εἰρήνη G1515)',
        'Shield of Faith (πίστις, G4102)',
        'Helmet of Salvation (σωτηρία, G4991)',
        'Sword — Word of God (ῥῆμα θεοῦ, G4487)',
        'Prayer (προσευχή, G4335)',
    ]
    # Short display labels for the TOC sub-links
    PIECE_LABELS = [
        'Belt of Truth', 'Breastplate of Righteousness',
        'Shoes — Gospel of Peace', 'Shield of Faith',
        'Helmet of Salvation', 'Sword — Word of God', 'Prayer',
    ]

    h_obs = 'The Exegetical Observation'
    h_text = 'Ephesians 6:10–18 — Text and Translation'
    h_armor = 'The Armor Pieces and Their Earlier Occurrences'
    h_heatmap = 'Frequency Heatmap'
    h_summary = 'Summary Table'

    toc_piece_lines = '\n'.join(
        f'   - [{label}](#{_slug(heading)})'
        for label, heading in zip(PIECE_LABELS, PIECE_HEADINGS)
    )

    sections.append(f'''\
# The Armor of God — Ephesians 6:10–18 in Its Letter Context

**Focus passage:** Ephesians 6:10–18
**Corpus:** New Testament (TAGNT)
**Topic:** Each piece of the armor of God introduced in Eph 6:14–18 recapitulates a theme Paul has already developed earlier in Ephesians.
<!-- Build script: scripts/nt/lexicon/armor-of-god/build_armor_of_god_report.py (repo link omitted from web) -->

---

## Contents

1. [The Exegetical Observation](#{_slug(h_obs)})
2. [Ephesians 6:10–18 — Text and Translation](#{_slug(h_text)})
3. [The Armor Pieces and Their Earlier Occurrences](#{_slug(h_armor)})
{toc_piece_lines}
4. [Frequency Heatmap](#{_slug(h_heatmap)})
5. [Summary Table](#{_slug(h_summary)})

---

## The Exegetical Observation

Ephesians 6:10–18 is one of the most recognized passages in Paul's letters, but its rhetorical power is deeper than a standalone metaphor. Every piece of armor Paul names in verses 14–18 is a word or concept he has already introduced and developed in the preceding five chapters.

Paul is not mixing theological metaphors on the fly. He is *recapitulating the letter*. By the time a reader reaches 6:14, each armor term carries the weight of everything Paul has already said about it:

- **Truth** has been defined as the content of the gospel and the character of Christ (1:13; 4:21)
- **Righteousness** is the quality of the new creation in Christ (4:24)
- **Peace** is not a disposition but a person — Christ himself (2:14)
- **Faith** is how sinners are saved (2:8) and how Christ dwells in the heart (3:17)
- **Salvation** is the gospel's content, received through hearing and believing (1:13)
- **The word (ῥῆμα)** is the instrument by which Christ sanctifies the church (5:26)
- **Prayer** is Paul's own practice throughout the letter (1:16; 3:14–21)

The armor passage is therefore not an appendix. It is a call to *wear* what Paul has been teaching. The image transforms doctrinal exposition into lived readiness.

---

## Ephesians 6:10–18 — Text and Translation

''')

    # Passage text
    for v in range(10, 19):
        greek, trans = EPH_6_PASSAGE[v]
        armor_note = {
            14: ' *(belt of truth; breastplate of righteousness)*',
            15: ' *(shoes of the gospel of peace)*',
            16: ' *(shield of faith)*',
            17: ' *(helmet of salvation; sword of the Spirit)*',
            18: ' *(prayer)*',
        }.get(v, '')
        sections.append(f'**v. {v}**{armor_note}')
        sections.append(f'> {greek}')
        sections.append('>')
        sections.append(f'> *{trans}*')
        sections.append('')

    sections.append('---')
    sections.append('')

    # ── Armor sections ────────────────────────────────────────────────────────
    sections.append('## The Armor Pieces and Their Earlier Occurrences')
    sections.append('')
    sections.append(
        'For each piece of armor, the key Greek term is identified along with '
        'every earlier occurrence in Ephesians and the exegetical connection to 6:14–18.'
    )
    sections.append('')

    PIECE_DETAILS = list(zip(
        PIECE_HEADINGS,
        [['G0225'], ['G1343'], ['G2098', 'G1515'], ['G4102'], ['G4991'], ['G4487'], ['G4335']],
        [14, 14, 15, 16, 17, 17, 18],
    ))

    for piece_label, prefixes, ch6_v in PIECE_DETAILS:
        sections.append(piece_section(piece_label, prefixes, ch6_v))

    sections.append('---')
    sections.append('')

    # ── Heatmap ───────────────────────────────────────────────────────────────
    sections.append('## Frequency Heatmap')
    sections.append('')
    sections.append(
        'The chart below shows the word-count occurrences of each armor term '
        'across Ephesians chapters 1–5 (chapter 6 excluded). '
        'Chapters with higher counts reflect where Paul most developed that theme.'
    )
    sections.append('')
    sections.append('![Armor of God key terms across Ephesians 1–5](armor-of-god-heatmap.png)')
    sections.append('')
    sections.append('---')
    sections.append('')

    # ── Summary table ─────────────────────────────────────────────────────────
    sections.append('## Summary Table')
    sections.append('')
    sections.append(
        '| Armor Piece | Greek Term | Strong\'s | Earlier in Ephesians |'
    )
    sections.append(
        '|-------------|-----------|----------|---------------------|'
    )

    TABLE_ROWS = [
        ('Belt of Truth',              'ἀλήθεια',    'G0225', ['G0225']),
        ('Breastplate of Righteousness', 'δικαιοσύνη', 'G1343', ['G1343']),
        ('Shoes — Gospel',             'εὐαγγέλιον', 'G2098', ['G2098']),
        ('Shoes — Peace',              'εἰρήνη',     'G1515', ['G1515']),
        ('Shield of Faith',            'πίστις',     'G4102', ['G4102']),
        ('Helmet of Salvation',        'σωτηρία',    'G4991', ['G4991']),
        ('Sword — Word (ῥῆμα)',       'ῥῆμα θεοῦ', 'G4487', ['G4487']),
        ('Prayer',                     'προσευχή',   'G4335', ['G4335']),
    ]

    for piece, greek, strongs, prefixes in TABLE_ROWS:
        rows = hits_in_eph(prefixes)
        refs = ref_list(rows)
        refs_str = ', '.join(f'Eph {r}' for r in refs) if refs else '—'
        sections.append(f'| {piece} | {greek} | {strongs} | {refs_str} |')

    sections.append('')
    sections.append('---')
    sections.append('')
    sections.append(
        '*The armor passage of Ephesians 6 is not a self-contained metaphor dropped '
        'into a letter. Every piece of armor names a reality Paul has already '
        'expounded: who Christ is, what he accomplished, and how believers are '
        'to walk. The call to "put on the whole armor" is a call to live in what '
        'has already been given.*'
    )
    sections.append('')

    out = REPORT_DIR / 'armor-of-god-report.md'
    out.write_text('\n'.join(sections), encoding='utf-8')
    print(f'Saved {out}')
    return out


def build_csv() -> Path:
    """Export a CSV of all armor-term occurrences in Ephesians 1–5."""
    rows = []
    for piece_label, prefixes, ch6_verse in [
        ('Belt of Truth',                 ['G0225'],          14),
        ('Breastplate of Righteousness',  ['G1343'],          14),
        ('Shoes — Gospel of Peace',       ['G2098', 'G1515'], 15),
        ('Shield of Faith',               ['G4102'],          16),
        ('Helmet of Salvation',           ['G4991'],          17),
        ('Sword — Word of God',           ['G4487'],          17),
        ('Prayer',                        ['G4335'],          18),
    ]:
        for prefix in prefixes:
            hits = hits_in_eph([prefix])
            for _, row in hits.iterrows():
                rows.append({
                    'armor_piece': piece_label,
                    'strongs': prefix,
                    'reference': f"Eph {row['chapter']}:{row['verse']}",
                    'chapter': row['chapter'],
                    'verse': row['verse'],
                    'greek_word': row['word'],
                    'translation': row['translation'],
                    'introduced_in_ch6_v': ch6_verse,
                })
    csv_out = REPORT_DIR / 'armor-of-god-data.csv'
    pd.DataFrame(rows).sort_values(['armor_piece', 'chapter', 'verse']).to_csv(
        csv_out, index=False, encoding='utf-8'
    )
    print(f'Saved {csv_out}')
    return csv_out


if __name__ == '__main__':
    heatmap = build_heatmap()
    report = build_report(heatmap)
    csv_path = build_csv()
    print('Done.')
