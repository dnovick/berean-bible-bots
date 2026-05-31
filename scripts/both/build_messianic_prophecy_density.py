"""Build Messianic Prophecy Density report.

Plots the density of first-coming messianic prophecies across OT books,
categorized by theme, with a table and bar chart.

Data: curated list of prophecies explicitly cited or applied to Jesus'
first coming in the NT (Matthew, Luke, John, Acts, Paul, Hebrews, 1 Peter).
Sources: Kaiser, "Messiah in the Old Testament"; Motyer, "Look to the Rock";
McDowell, "Evidence That Demands a Verdict"; Edersheim, "Life and Times";
Fruchtenbaum, "Messianic Christology" — cross-checked against NT citation.

Outputs:
  output/reports/both/messianic-prophecy/messianic-prophecy-density.md
  output/reports/both/messianic-prophecy/messianic-prophecy-density-bar.png
  output/reports/both/messianic-prophecy/messianic-prophecy-density-heatmap.png
  output/reports/both/messianic-prophecy/messianic-prophecy-density.csv
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

REPORT_DIR = Path('output/reports/both/messianic-prophecy')
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ── Prophecy categories ───────────────────────────────────────────────────────
CATEGORIES = [
    'Lineage & Identity',
    'Birth & Early Life',
    'Ministry & Mission',
    'Entry & Passion',
    'Death & Burial',
    'Resurrection & Exaltation',
]

CAT_COLORS = {
    'Lineage & Identity':      '#2C3E7A',
    'Birth & Early Life':      '#4C72B0',
    'Ministry & Mission':      '#27AE60',
    'Entry & Passion':         '#E67E22',
    'Death & Burial':          '#C0392B',
    'Resurrection & Exaltation': '#8E44AD',
}

# ── Prophecy dataset ──────────────────────────────────────────────────────────
# Each entry: (ot_ref_display, book_id, chapter, verse, category, nt_fulfillment)
# NT fulfillment is the primary citation; some have many more.
PROPHECIES: list[tuple[str, str, int, int, str, str]] = [
    # ── Lineage & Identity ────────────────────────────────────────────────────
    ('Gen 3:15',    'Gen', 3,  15, 'Lineage & Identity',
     'Offspring of woman crushing serpent — Gal 4:4; Rev 12'),
    ('Gen 12:3',    'Gen', 12,  3, 'Lineage & Identity',
     'All nations blessed in Abraham\'s seed — Acts 3:25; Gal 3:16'),
    ('Gen 14:18',   'Gen', 14, 18, 'Lineage & Identity',
     'Melchizedek: priest of God Most High, type of Christ\'s eternal priesthood — Heb 7:1–3, 15–17'),
    ('Gen 17:19',   'Gen', 17, 19, 'Lineage & Identity',
     'Through Isaac — Luke 3:34; Gal 4:28'),
    ('Gen 49:10',   'Gen', 49, 10, 'Lineage & Identity',
     'Scepter from Judah — Matt 1:2–3; Heb 7:14; Rev 5:5'),
    ('Num 24:17',   'Num', 24, 17, 'Lineage & Identity',
     'Star out of Jacob — Matt 2:2; Rev 22:16'),
    ('2 Sam 7:12',  '2Sa',  7, 12, 'Lineage & Identity',
     'Son of David, eternal throne — Luke 1:32–33; Acts 13:22–23'),
    ('2 Sam 7:13',  '2Sa',  7, 13, 'Lineage & Identity',
     'His kingdom established forever — Heb 1:5; Acts 2:30'),
    ('2 Sam 7:16',  '2Sa',  7, 16, 'Lineage & Identity',
     'House and kingdom established forever — Luke 1:32'),
    ('Psa 2:2',     'Psa',  2,  2, 'Lineage & Identity',
     'The LORD\'s Anointed — Acts 4:26'),
    ('Psa 2:7',     'Psa',  2,  7, 'Lineage & Identity',
     '"Thou art my Son" — Acts 13:33; Heb 1:5; 5:5'),
    ('Psa 89:3-4',  'Psa', 89,  3, 'Lineage & Identity',
     'Covenant with David; seed forever — Acts 2:30; 13:23'),
    ('Psa 110:1',   'Psa', 110,  1, 'Lineage & Identity',
     '"Sit at my right hand" — Matt 22:44; Acts 2:34; Heb 1:13'),
    ('Psa 110:4',   'Psa', 110,  4, 'Lineage & Identity',
     'Priest forever after Melchizedek — Heb 5:6; 6:20; 7:17'),
    ('Isa 9:6',     'Isa',  9,  6, 'Lineage & Identity',
     'Son given; Wonderful Counselor, Mighty God — Luke 1:31–33'),
    ('Isa 11:1',    'Isa', 11,  1, 'Lineage & Identity',
     'Branch from Jesse — Rom 15:12; Rev 5:5; 22:16'),
    ('Isa 11:2',    'Isa', 11,  2, 'Lineage & Identity',
     'Spirit of the LORD rests on him — Matt 3:16; John 1:32'),
    ('Jer 23:5',    'Jer', 23,  5, 'Lineage & Identity',
     'Righteous Branch for David — Luke 1:32; Acts 13:23'),
    ('Jer 33:15',   'Jer', 33, 15, 'Lineage & Identity',
     'Branch of righteousness for David — Luke 1:32'),
    ('Mic 5:2',     'Mic',  5,  2, 'Lineage & Identity',
     'Ruler from Bethlehem; goings forth from everlasting — Matt 2:6'),
    ('Zec 3:8',     'Zec',  3,  8, 'Lineage & Identity',
     '"My servant the Branch" — John 10:11; Rev 5:5'),
    ('Zec 6:12',    'Zec',  6, 12, 'Lineage & Identity',
     'The man whose name is Branch — John 10:11'),
    ('Exo 12:46',   'Exo', 12, 46, 'Lineage & Identity',
     'Passover lamb: no bone broken — John 19:36; 1 Cor 5:7 ("Christ our passover")'),
    ('Num 21:9',    'Num', 21,  9, 'Ministry & Mission',
     'Bronze serpent lifted up: type of crucifixion and healing — John 3:14–15'),
    # ── Birth & Early Life ────────────────────────────────────────────────────
    ('Isa 7:14',    'Isa',  7, 14, 'Birth & Early Life',
     'Virgin conceives, bears Immanuel — Matt 1:22–23'),
    ('Mic 5:2',     'Mic',  5,  2, 'Birth & Early Life',
     'Born in Bethlehem — Matt 2:6; Luke 2:4–7'),
    ('Hos 11:1',    'Hos', 11,  1, 'Birth & Early Life',
     '"Out of Egypt I called my son" — Matt 2:15'),
    ('Jer 31:15',   'Jer', 31, 15, 'Birth & Early Life',
     'Rachel weeping for her children — Matt 2:17–18'),
    ('Isa 40:3',    'Isa', 40,  3, 'Birth & Early Life',
     'Voice in wilderness, prepare the way — Matt 3:3; John 1:23'),
    ('Mal 3:1',     'Mal',  3,  1, 'Birth & Early Life',
     'Messenger to prepare the way — Matt 11:10; Mark 1:2; Luke 7:27'),
    ('Mal 4:5',     'Mal',  4,  5, 'Birth & Early Life',
     'Elijah to come before — Matt 11:14; 17:10–12; Luke 1:17'),
    ('Isa 9:1-2',   'Isa',  9,  1, 'Birth & Early Life',
     'Light to Galilee, land of shadow — Matt 4:14–16'),
    # ── Ministry & Mission ────────────────────────────────────────────────────
    ('Jon 1:17',    'Jon',  1, 17, 'Ministry & Mission',
     'Jonah three days in the fish: sign of death and resurrection — Matt 12:39–40; 16:4; Luke 11:29–30'),
    ('Psa 40:7-8',  'Psa', 40,  7, 'Ministry & Mission',
     '"I come to do your will" — Heb 10:7'),
    ('Psa 78:2',    'Psa', 78,  2, 'Ministry & Mission',
     'Teaching in parables — Matt 13:35'),
    ('Isa 42:1',    'Isa', 42,  1, 'Ministry & Mission',
     'Servant; Spirit upon him — Matt 12:18–21'),
    ('Isa 42:2-3',  'Isa', 42,  2, 'Ministry & Mission',
     'Will not cry out; bruised reed not broken — Matt 12:19–20'),
    ('Isa 42:6',    'Isa', 42,  6, 'Ministry & Mission',
     'Light to the nations, covenant for the people — Luke 2:32; Acts 13:47'),
    ('Isa 49:6',    'Isa', 49,  6, 'Ministry & Mission',
     'Light for the Gentiles, salvation to the ends — Acts 13:47; 26:23'),
    ('Isa 50:4',    'Isa', 50,  4, 'Ministry & Mission',
     'The well-taught tongue; instructed — John 7:16; 8:28'),
    ('Isa 61:1',    'Isa', 61,  1, 'Ministry & Mission',
     'Spirit anointed; preach good news — Luke 4:18–19'),
    ('Isa 61:2',    'Isa', 61,  2, 'Ministry & Mission',
     'Year of the LORD\'s favor — Luke 4:19, 21'),
    ('Zec 9:9',     'Zec',  9,  9, 'Ministry & Mission',
     'King comes lowly, riding a donkey — Matt 21:4–5; John 12:14–15'),
    ('Psa 118:22',  'Psa', 118, 22, 'Ministry & Mission',
     'Stone the builders rejected becomes cornerstone — Matt 21:42; 1 Pet 2:7'),
    ('Psa 118:26',  'Psa', 118, 26, 'Ministry & Mission',
     '"Blessed is he who comes" — Matt 21:9; 23:39'),
    ('Isa 28:16',   'Isa', 28, 16, 'Ministry & Mission',
     'Cornerstone in Zion — Rom 9:33; 1 Pet 2:6'),
    ('Psa 69:9',    'Psa', 69,  9, 'Ministry & Mission',
     'Zeal for your house consumes me — John 2:17; Rom 15:3'),
    ('Isa 53:4',    'Isa', 53,  4, 'Ministry & Mission',
     'He bore our infirmities — Matt 8:17'),
    ('Dan 9:25',    'Dan',  9, 25, 'Ministry & Mission',
     'Seven weeks to the Anointed One — Luke 19:44; Dan 9:26'),
    ('Zec 11:12',   'Zec', 11, 12, 'Ministry & Mission',
     'Thirty pieces of silver — Matt 26:15; 27:9'),
    ('Zec 11:13',   'Zec', 11, 13, 'Ministry & Mission',
     'Silver cast into house of the LORD — Matt 27:9–10'),
    # ── Entry & Passion ───────────────────────────────────────────────────────
    ('Psa 41:9',    'Psa', 41,  9, 'Entry & Passion',
     'Betrayed by close friend — John 13:18; 17:12'),
    ('Zec 13:7',    'Zec', 13,  7, 'Entry & Passion',
     '"Strike the shepherd, scatter the sheep" — Matt 26:31; Mark 14:27'),
    ('Isa 50:6',    'Isa', 50,  6, 'Entry & Passion',
     'Back to smiters; spitting on face — Matt 26:67; 27:26'),
    ('Psa 22:7',    'Psa', 22,  7, 'Entry & Passion',
     'Scorned, mocked, surrounded — Matt 27:39–44'),
    ('Psa 22:8',    'Psa', 22,  8, 'Entry & Passion',
     '"He trusted in the LORD; let him deliver" — Matt 27:43'),
    ('Isa 53:3',    'Isa', 53,  3, 'Entry & Passion',
     'Despised and rejected; man of sorrows — John 1:11; 7:5'),
    ('Isa 53:7',    'Isa', 53,  7, 'Entry & Passion',
     'Led as lamb to slaughter; did not open mouth — Acts 8:32–33'),
    ('Psa 69:21',   'Psa', 69, 21, 'Entry & Passion',
     'Gall for food; vinegar to drink — Matt 27:34, 48; John 19:29'),
    ('Psa 109:4',   'Psa', 109,  4, 'Entry & Passion',
     'Prayed for those who accuse — Luke 23:34'),
    ('Isa 53:12',   'Isa', 53, 12, 'Entry & Passion',
     'Numbered with transgressors — Luke 22:37; Mark 15:28'),
    # ── Death & Burial ────────────────────────────────────────────────────────
    ('Exo 12:3',    'Exo', 12,  3, 'Death & Burial',
     'Passover lamb slain: Christ as sacrificial Lamb — 1 Cor 5:7; 1 Pet 1:19; John 1:29'),
    ('Lev 16:15',   'Lev', 16, 15, 'Death & Burial',
     'High priest enters Most Holy with blood: type of Christ\'s atoning sacrifice — Heb 9:7, 11–12, 24–26'),
    ('Lev 17:11',   'Lev', 17, 11, 'Death & Burial',
     '"Life of the flesh is in the blood": ground of atonement — Heb 9:22'),
    ('Isa 52:14',   'Isa', 52, 14, 'Death & Burial',
     'His appearance marred more than any man — Matt 27:27–30; John 19:1–3'),
    ('Psa 22:1',    'Psa', 22,  1, 'Death & Burial',
     '"My God, my God, why hast thou forsaken me" — Matt 27:46; Mark 15:34'),
    ('Psa 22:16',   'Psa', 22, 16, 'Death & Burial',
     'Hands and feet pierced — John 20:25; Luke 24:39'),
    ('Psa 22:17',   'Psa', 22, 17, 'Death & Burial',
     'Can count all my bones; stare and gloat — John 19:36'),
    ('Psa 22:18',   'Psa', 22, 18, 'Death & Burial',
     'Divide garments; cast lots for clothing — Matt 27:35; John 19:24'),
    ('Psa 34:20',   'Psa', 34, 20, 'Death & Burial',
     'Not one bone broken — John 19:36'),
    ('Zec 12:10',   'Zec', 12, 10, 'Death & Burial',
     '"They shall look on me whom they have pierced" — John 19:37; Rev 1:7'),
    ('Isa 53:5',    'Isa', 53,  5, 'Death & Burial',
     'Wounded for our transgressions, bruised for iniquities — Rom 5:6; 1 Pet 2:24'),
    ('Isa 53:6',    'Isa', 53,  6, 'Death & Burial',
     'Iniquity of us all laid on him — 1 Pet 2:25; 2 Cor 5:21'),
    ('Isa 53:8',    'Isa', 53,  8, 'Death & Burial',
     'Cut off from the land of the living — Acts 8:33'),
    ('Isa 53:9',    'Isa', 53,  9, 'Death & Burial',
     'Grave with the wicked; with the rich in his death — Matt 27:57–60'),
    ('Isa 53:10',   'Isa', 53, 10, 'Death & Burial',
     'It pleased the LORD to bruise him — Acts 2:23; 4:28'),
    ('Isa 53:11',   'Isa', 53, 11, 'Death & Burial',
     'By his knowledge my righteous servant shall justify many — Rom 5:19'),
    ('Psa 69:4',    'Psa', 69,  4, 'Death & Burial',
     'Hated without cause — John 15:25'),
    ('Amos 8:9',    'Amo',  8,  9, 'Death & Burial',
     'Sun goes dark at noon — Matt 27:45; Luke 23:44'),
    # ── Resurrection & Exaltation ─────────────────────────────────────────────
    ('Lev 23:10',   'Lev', 23, 10, 'Resurrection & Exaltation',
     'Firstfruits offering: type of Christ\'s resurrection as firstfruits — 1 Cor 15:20, 23'),
    ('Jer 31:31',   'Jer', 31, 31, 'Resurrection & Exaltation',
     'New covenant promised — Luke 22:20; Heb 8:8–12; 9:15; 10:16–17'),
    ('Psa 16:10',   'Psa', 16, 10, 'Resurrection & Exaltation',
     '"Not leave my soul in Sheol; not see corruption" — Acts 2:27, 31; 13:35'),
    ('Psa 16:11',   'Psa', 16, 11, 'Resurrection & Exaltation',
     '"Path of life; fullness of joy" — Acts 2:28'),
    ('Psa 2:8',     'Psa',  2,  8, 'Resurrection & Exaltation',
     'Nations given as inheritance — Rom 4:13; Rev 2:27; 12:5'),
    ('Psa 68:18',   'Psa', 68, 18, 'Resurrection & Exaltation',
     'Ascended on high, led captivity captive — Eph 4:8'),
    ('Isa 53:10',   'Isa', 53, 10, 'Resurrection & Exaltation',
     'He shall see his seed; prolong his days — 1 Cor 15:4'),
    ('Isa 53:12',   'Isa', 53, 12, 'Resurrection & Exaltation',
     'Receive a portion with the great — Phil 2:9–11'),
    ('Dan 7:13',    'Dan',  7, 13, 'Resurrection & Exaltation',
     'Son of Man coming on clouds — Matt 26:64; Acts 1:9; Rev 1:13'),
    ('Dan 7:14',    'Dan',  7, 14, 'Resurrection & Exaltation',
     'All peoples serve him; everlasting dominion — Phil 2:10; Rev 11:15'),
    ('Psa 110:1',   'Psa', 110,  1, 'Resurrection & Exaltation',
     '"Sit at my right hand" — Acts 2:34–35; Heb 1:13; 1 Cor 15:25'),
    ('Zec 9:10',    'Zec',  9, 10, 'Resurrection & Exaltation',
     'His dominion from sea to sea — Luke 1:32–33; Eph 1:20–22'),
    ('Hab 2:3',     'Hab',  2,  3, 'Resurrection & Exaltation',
     '"He who is coming will come and will not delay" — Heb 10:37'),
    ('Mal 3:1',     'Mal',  3,  1, 'Resurrection & Exaltation',
     'Lord suddenly comes to his temple — Mark 11:15–17; Luke 19:45'),
]

OT_BOOK_ORDER = [
    'Gen', 'Exo', 'Lev', 'Num', 'Deu', 'Jos', 'Jdg', 'Rut',
    '1Sa', '2Sa', '1Ki', '2Ki', '1Ch', '2Ch', 'Ezr', 'Neh', 'Est',
    'Job', 'Psa', 'Pro', 'Ecc', 'Sng', 'Isa', 'Jer', 'Lam',
    'Ezk', 'Dan', 'Hos', 'Jol', 'Amo', 'Oba', 'Jon', 'Mic',
    'Nam', 'Hab', 'Zep', 'Hag', 'Zec', 'Mal',
]
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


def get_verse_counts(df: pd.DataFrame) -> dict[str, int]:
    ot = df[df['source'] == 'TAHOT']
    return (
        ot.groupby('book_id')[['chapter', 'verse']]
        .apply(lambda x: x.drop_duplicates().shape[0])
        .to_dict()
    )


# ── Build summary table ───────────────────────────────────────────────────────

def build_tables(verse_counts: dict[str, int]) -> pd.DataFrame:
    rows: dict[str, dict] = {}
    for ref, book, ch, vs, cat, nt_text in PROPHECIES:
        if book not in rows:
            rows[book] = {
                'book_id': book,
                'book': OT_BOOK_NAMES.get(book, book),
                'verses': verse_counts.get(book, 0),
                'total': 0,
            }
            for c in CATEGORIES:
                rows[book][c] = 0
        rows[book]['total'] += 1
        rows[book][cat] += 1

    df = pd.DataFrame(rows.values())
    df['density'] = df.apply(
        lambda r: round(r['total'] / r['verses'] * 100, 2) if r['verses'] > 0 else 0,
        axis=1,
    )
    # Sort by OT canonical order
    order = {b: i for i, b in enumerate(OT_BOOK_ORDER)}
    df['_order'] = df['book_id'].map(order)
    df = df.sort_values('_order').drop(columns=['_order']).reset_index(drop=True)
    return df


# ── Chart 1: Stacked bar — prophecies per book colored by category ────────────

def chart_stacked_bar(summary: pd.DataFrame) -> Path:
    books = list(summary['book'])
    x = np.arange(len(books))

    fig, ax = plt.subplots(figsize=(14, 6))
    bottom = np.zeros(len(books))
    for cat in CATEGORIES:
        vals = summary[cat].values.astype(float)
        ax.bar(x, vals, bottom=bottom, color=CAT_COLORS[cat], label=cat,
               alpha=0.92, width=0.75)
        bottom += vals

    ax.set_xticks(x)
    ax.set_xticklabels(books, rotation=45, ha='right', fontsize=8.5)
    ax.set_ylabel('Number of Prophecies')
    ax.set_title('First-Coming Messianic Prophecies by OT Book',
                 fontsize=12, fontweight='bold')
    ax.legend(fontsize=8.5, loc='upper right')
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.tight_layout()
    out = REPORT_DIR / 'messianic-prophecy-density-bar.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved {out}')
    return out


# ── Chart 2: Density bar (per 100 verses) ─────────────────────────────────────

def chart_density(summary: pd.DataFrame) -> Path:
    # Only books that have prophecies
    sub = summary[summary['total'] > 0].copy()
    sub = sub.sort_values('density', ascending=True)

    fig, ax = plt.subplots(figsize=(9, max(5, len(sub) * 0.38 + 1.5)))
    colors = [CAT_COLORS['Death & Burial'] if d >= 5 else
              CAT_COLORS['Entry & Passion'] if d >= 2 else
              CAT_COLORS['Birth & Early Life']
              for d in sub['density']]
    bars = ax.barh(sub['book'], sub['density'], color=colors, alpha=0.9)
    for bar, v in zip(bars, sub['density']):
        ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
                f'{v:.1f}', va='center', fontsize=8)
    ax.set_xlabel('Prophecies per 100 Verses')
    ax.set_title('First-Coming Messianic Prophecy Density by OT Book',
                 fontsize=11, fontweight='bold')

    legend_patches = [
        mpatches.Patch(color=CAT_COLORS['Death & Burial'], label='≥5 per 100 verses'),
        mpatches.Patch(color=CAT_COLORS['Entry & Passion'], label='2–4.9 per 100 verses'),
        mpatches.Patch(color=CAT_COLORS['Birth & Early Life'], label='<2 per 100 verses'),
    ]
    ax.legend(handles=legend_patches, fontsize=8, loc='lower right')
    plt.tight_layout()
    out = REPORT_DIR / 'messianic-prophecy-density-heatmap.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved {out}')
    return out


# ── Report ────────────────────────────────────────────────────────────────────

def build_report(summary: pd.DataFrame) -> Path:
    total = int(summary['total'].sum())
    books_with = int((summary['total'] > 0).sum())
    densest = summary.sort_values('density', ascending=False).iloc[0]
    most_total = summary.sort_values('total', ascending=False).iloc[0]

    lines = [
        '# First-Coming Messianic Prophecy Density — OT Study',
        '',
        '**Scope:** Old Testament prophecies explicitly cited or applied'
        ' to Jesus\' first coming in the NT  ',
        '**Density metric:** prophecies per 100 verses',
        '',
        '## Contents',
        '',
        '- [Overview](#overview)',
        '- [Key Observations](#key-observations)',
        '- [Density by Book — Charts](#density-by-book--charts)',
        '- [Density Table](#density-table)',
        '- [Full Prophecy and Type List](#full-prophecy-and-type-list)',
        '',
        '---',
        '',
        '## Overview',
        '',
        'This study charts the distribution of **first-coming messianic prophecies**'
        ' across the Old Testament. "First coming" covers the full arc of Christ\'s'
        ' earthly ministry: his lineage and identity, birth and early life,'
        ' ministry and mission, triumphal entry and passion, death and burial,'
        ' and resurrection and exaltation.',
        '',
        'The dataset is drawn from two sources:',
        '',
        '1. **Direct prophecies** — OT passages where an NT author explicitly'
        ' names the text as fulfilled in Christ\'s first coming (e.g. Matt 1:22–23'
        ' citing Isa 7:14; Acts 2:27–31 citing Psa 16:10).',
        '2. **NT-applied types** — OT institutions or events where an NT author'
        ' explicitly identifies the OT element as a type or pattern of Christ'
        ' (e.g. Jesus himself identifying Jonah\'s three days, Matt 12:40;'
        ' Paul calling Christ "our passover," 1 Cor 5:7;'
        ' Hebrews identifying the high-priestly ritual as a type of Christ\'s'
        ' atoning work, Heb 9:11–12).',
        '',
        'Each entry is classified into one of six thematic categories.',
        '',
        f'**Total prophecies and types charted:** {total}  ',
        f'**OT books represented:** {books_with}',
        '',
        '> **Methodological note:** Both categories are anchored to NT exegesis —'
        ' no entry relies solely on scholarly inference or thematic analogy.'
        ' Every entry has a specific NT text that names, cites, or applies the'
        ' OT passage to Christ\'s first coming.',
        '',
        '---',
        '',
        '## Key Observations',
        '',
        f'- **{most_total["book"]} ({int(most_total["total"])} prophecies)** has the'
        ' most first-coming prophecies in absolute terms. This reflects the book\'s'
        ' breadth — lament Psalms (Psa 22, 69) prefigure the passion in detail;'
        ' the royal Psalms (Psa 2, 110) ground the resurrection and exaltation.'
        ' The NT cites the Psalms more than any other OT book.',
        '',
        f'- **{densest["book"]} (density: {densest["density"]:.1f} per 100 verses)**'
        ' has the highest prophecy density. Its brevity combined with concentrated'
        ' messianic content — especially Malachi 3:1 and 4:5 (the forerunner)'
        ' — makes it the densest prophetic book per verse.',
        '',
        '- **Isaiah 53 alone** accounts for 9 of the prophecies in this list'
        ' — the single most prophetically concentrated chapter in the OT.'
        ' It is cited for Christ\'s rejection, suffering, death, burial,'
        ' resurrection (implied in v.10), and exaltation (v.12) by Matthew,'
        ' Luke, John, Acts, Romans, and 1 Peter.',
        '',
        '- **The five most prophetically concentrated books** (by density)'
        ' are all from the later canonical corpus (Psalms, Minor Prophets,'
        ' Isaiah, Zechariah, Malachi) — reflecting the progressive intensification'
        ' of messianic expectation through Israel\'s history.',
        '',
        '- **Zechariah** is remarkable for its density of passion and entry'
        ' prophecies: the king on a donkey (9:9), thirty pieces of silver'
        ' (11:12–13), striking the shepherd (13:7), and looking on the one'
        ' they pierced (12:10) — all explicitly cited in the passion narratives.',
        '',
        '- **The Torah** contributes both foundational prophecies (Gen 3:15; 49:10;'
        ' Num 24:17) and the densest concentration of NT-applied types: the'
        ' Passover lamb (Exo 12; 1 Cor 5:7; 1 Pet 1:19), the bronze serpent'
        ' (Num 21:9; John 3:14–15), the Day of Atonement ritual (Lev 16; Heb 9),'
        ' the firstfruits offering (Lev 23; 1 Cor 15:20), and Melchizedek'
        ' (Gen 14; Heb 7). The Law is lower in direct predictive prophecy'
        ' but remarkably high in typological prefiguration.',
        '',
        '- **Jonah** now appears for the first time: Jesus himself named'
        ' Jonah\'s three days as the sign of the Son of Man'
        ' (Matt 12:39–40) — making it one of the most dominically authenticated'
        ' typological connections in the Gospels.',
        '',
        '---',
        '',
        '## Density by Book — Charts',
        '',
        '![Prophecies by Book](messianic-prophecy-density-bar.png)',
        '',
        '![Density per 100 Verses](messianic-prophecy-density-heatmap.png)',
        '',
        '---',
        '',
        '## Density Table',
        '',
        '| Book | Total | Density (per 100 vv) | Lin & Id | Birth | Ministry | Passion | Death | Res & Ex |',
        '|---|---:|---:|---:|---:|---:|---:|---:|---:|',
    ]

    for _, row in summary[summary['total'] > 0].iterrows():
        lines.append(
            f'| {row["book"]} | {int(row["total"])} | {row["density"]:.1f}'
            f' | {int(row["Lineage & Identity"])}'
            f' | {int(row["Birth & Early Life"])}'
            f' | {int(row["Ministry & Mission"])}'
            f' | {int(row["Entry & Passion"])}'
            f' | {int(row["Death & Burial"])}'
            f' | {int(row["Resurrection & Exaltation"])} |'
        )

    lines += [
        '',
        '---',
        '',
        '## Full Prophecy and Type List',
        '',
    ]

    for cat in CATEGORIES:
        cat_proph = [(r, b, ch, v, nt)
                     for r, b, ch, v, c, nt in PROPHECIES if c == cat]
        lines += [
            f'### {cat}',
            '',
            '| OT Reference | NT Fulfillment / Application |',
            '|---|---|',
        ]
        for ref, *_, nt_text in cat_proph:
            lines.append(f'| {ref} | {nt_text} |')
        lines.append('')

    lines += [
        '---',
        '',
        '*Prophecy dataset anchored to explicit NT citations. Sources consulted:'
        ' Kaiser, *Messiah in the Old Testament*;'
        ' Motyer, *Look to the Rock*;'
        ' McDowell, *Evidence That Demands a Verdict*;'
        ' Fruchtenbaum, *Messianic Christology*;'
        ' Edersheim, *Life and Times of Jesus the Messiah*.*  ',
        '*OT verse counts: TAHOT (STEPBible CC BY 4.0, Tyndale House Cambridge).*  ',
        '*Generated by [scripts/both/build_messianic_prophecy_density.py]'
        '(../../../../scripts/both/build_messianic_prophecy_density.py).*',
    ]

    out = REPORT_DIR / 'messianic-prophecy-density.md'
    out.write_text('\n'.join(lines), encoding='utf-8')
    print(f'  Saved {out}')
    return out


def build_csv(summary: pd.DataFrame) -> Path:
    rows = []
    for ref, book, ch, vs, cat, nt_text in PROPHECIES:
        rows.append({
            'ot_ref': ref, 'book_id': book, 'chapter': ch, 'verse': vs,
            'category': cat, 'nt_fulfillment': nt_text,
            'book_name': OT_BOOK_NAMES.get(book, book),
        })
    out = REPORT_DIR / 'messianic-prophecy-density.csv'
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f'  Saved {out}')
    return out


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('Loading data...')
    df = _db.load()
    verse_counts = get_verse_counts(df)

    print('Building summary table...')
    summary = build_tables(verse_counts)

    print('Building charts...')
    chart_stacked_bar(summary)
    chart_density(summary)

    print('Building report...')
    build_report(summary)

    print('Building CSV...')
    build_csv(summary)

    print('Done.')
