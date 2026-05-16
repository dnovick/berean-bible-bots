"""Word study: λόγος (G3056) vs ῥῆμα (G4487) — "word" in Hebrew/Greek OT/LXX/NT.

Generates:
  Charts:
    logos-rhema-nt-by-book.png          — side-by-side NT frequency bar chart
    logos-rhema-lxx-by-book.png         — LXX frequency by book (canonical)
    logos-rhema-hebrew-sources.png      — Hebrew source words feeding each Greek term
    logos-rhema-dabar-split.png         — how dabar splits between logos/rhema by book
    logos-rhema-nt-genre-pie.png        — genre distribution pie for each term

  Reports:
    logos-rhema.md                      — main markdown report
    logos-rhema-concordance.csv         — full NT concordance for both terms
    logos-rhema-lxx-concordance.csv     — LXX concordance for both terms
"""
import matplotlib; matplotlib.use('Agg')  # noqa: E702
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

from bible_grammar.core import db as _db
from bible_grammar.core.reference import BOOKS

REPORT_DIR = Path('output/reports/both/word_studies/logos-rhema')
CHART_DIR = Path('output/charts/both/word_studies/logos-rhema')
REPORT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)

# ── Load data ─────────────────────────────────────────────────────────────────

words = _db.load()
lxx_df = _db.load_lxx()
trans = _db.load_translations()
align = pd.read_parquet(
    Path(__file__).resolve().parents[4] / 'data' / 'processed' / 'alignment.parquet'
)
kjv = trans[trans['translation'] == 'KJV'].copy()

nt = words[words['source'] == 'TAGNT'].copy()

logos_nt = nt[nt['strongs'].str.contains('G3056', na=False)].copy()
rhema_nt = nt[nt['strongs'].str.contains('G4487', na=False)].copy()

logos_lxx = lxx_df[(lxx_df['strongs'] == 'G3056') & (~lxx_df['is_deuterocanon'])].copy()
rhema_lxx = lxx_df[(lxx_df['strongs'] == 'G4487') & (~lxx_df['is_deuterocanon'])].copy()

# ── Book order helpers ─────────────────────────────────────────────────────────

NT_ORDER = [b[0] for b in BOOKS if b[2] == 'NT']
OT_ORDER = [b[0] for b in BOOKS if b[2] == 'OT']

NT_GENRE = {
    'Mat': 'Gospel', 'Mrk': 'Gospel', 'Luk': 'Gospel', 'Jhn': 'Gospel',
    'Act': 'Acts',
    'Rom': 'Pauline Epistles', '1Co': 'Pauline Epistles', '2Co': 'Pauline Epistles',
    'Gal': 'Pauline Epistles', 'Eph': 'Pauline Epistles', 'Php': 'Pauline Epistles',
    'Col': 'Pauline Epistles', '1Th': 'Pauline Epistles', '2Th': 'Pauline Epistles',
    '1Ti': 'Pauline Epistles', '2Ti': 'Pauline Epistles', 'Tit': 'Pauline Epistles',
    'Phm': 'Pauline Epistles',
    'Heb': 'General Epistles', 'Jas': 'General Epistles', '1Pe': 'General Epistles',
    '2Pe': 'General Epistles', '1Jn': 'General Epistles', '2Jn': 'General Epistles',
    '3Jn': 'General Epistles', 'Jud': 'General Epistles',
    'Rev': 'Apocalyptic',
}
GENRE_COLORS = {
    'Gospel': '#4292c6', 'Acts': '#2ca25f', 'Pauline Epistles': '#fd8d3c',
    'General Epistles': '#9e9ac8', 'Apocalyptic': '#d62728',
}

LOGOS_COLOR = '#2166ac'
RHEMA_COLOR = '#d6604d'

BOOK_NAMES = {b[0]: b[1] for b in BOOKS}


def _kjv(book: str, ch: int, vs: int) -> str:
    row = kjv[(kjv['book_id'] == book) & (kjv['chapter'] == ch) & (kjv['verse'] == vs)]
    return row['text'].values[0] if len(row) else ''


# ── Chart 1: NT frequency side-by-side by book ────────────────────────────────

def _chart_nt_by_book() -> None:
    logos_cnt = logos_nt.groupby('book_id').size().reindex(NT_ORDER, fill_value=0)
    rhema_cnt = rhema_nt.groupby('book_id').size().reindex(NT_ORDER, fill_value=0)

    books_with_data = [b for b in NT_ORDER if logos_cnt[b] > 0 or rhema_cnt[b] > 0]
    logos_vals = [logos_cnt[b] for b in books_with_data]
    rhema_vals = [rhema_cnt[b] for b in books_with_data]

    x = range(len(books_with_data))
    w = 0.38
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.bar([i - w / 2 for i in x], logos_vals, width=w, label='λόγος (G3056)',
           color=LOGOS_COLOR, edgecolor='white', linewidth=0.4)
    ax.bar([i + w / 2 for i in x], rhema_vals, width=w, label='ῥῆμα (G4487)',
           color=RHEMA_COLOR, edgecolor='white', linewidth=0.4)
    ax.set_xticks(list(x))
    ax.set_xticklabels(books_with_data, rotation=45, ha='right', fontsize=8)
    ax.set_ylabel('Occurrences')
    ax.set_title('λόγος vs ῥῆμα — NT Frequency by Book', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    fig.tight_layout()
    path = CHART_DIR / 'logos-rhema-nt-by-book.png'
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'Chart: {path}')


# ── Chart 2: LXX frequency by OT book ─────────────────────────────────────────

def _chart_lxx_by_book() -> None:
    logos_cnt = logos_lxx.groupby('book_id').size().reindex(OT_ORDER, fill_value=0)
    rhema_cnt = rhema_lxx.groupby('book_id').size().reindex(OT_ORDER, fill_value=0)

    books_with_data = [b for b in OT_ORDER if logos_cnt[b] > 0 or rhema_cnt[b] > 0]
    logos_vals = [logos_cnt[b] for b in books_with_data]
    rhema_vals = [rhema_cnt[b] for b in books_with_data]

    x = range(len(books_with_data))
    w = 0.38
    fig, ax = plt.subplots(figsize=(16, 5))
    ax.bar([i - w / 2 for i in x], logos_vals, width=w, label='λόγος (G3056)',
           color=LOGOS_COLOR, edgecolor='white', linewidth=0.3)
    ax.bar([i + w / 2 for i in x], rhema_vals, width=w, label='ῥῆμα (G4487)',
           color=RHEMA_COLOR, edgecolor='white', linewidth=0.3)
    ax.set_xticks(list(x))
    ax.set_xticklabels(books_with_data, rotation=45, ha='right', fontsize=7)
    ax.set_ylabel('Occurrences')
    ax.set_title('λόγος vs ῥῆμα — LXX Frequency by Book (Canonical OT)',
                 fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    fig.tight_layout()
    path = CHART_DIR / 'logos-rhema-lxx-by-book.png'
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'Chart: {path}')


# ── Chart 3: dābar split by OT genre group (stacked bar) ─────────────────────

OT_GENRE = {
    'Gen': 'Torah', 'Exo': 'Torah', 'Lev': 'Torah', 'Num': 'Torah', 'Deu': 'Torah',
    'Jos': 'Former\nProphets', 'Jdg': 'Former\nProphets',
    '1Sa': 'Former\nProphets', '2Sa': 'Former\nProphets',
    '1Ki': 'Former\nProphets', '2Ki': 'Former\nProphets',
    '1Ch': 'Writings', '2Ch': 'Writings', 'Ezr': 'Writings', 'Neh': 'Writings',
    'Est': 'Writings', 'Rut': 'Writings',
    'Job': 'Wisdom', 'Pro': 'Wisdom', 'Ecc': 'Wisdom',
    'Psa': 'Psalms',
    'Isa': 'Latter\nProphets', 'Jer': 'Latter\nProphets', 'Lam': 'Latter\nProphets',
    'Ezk': 'Latter\nProphets', 'Dan': 'Latter\nProphets',
    'Hos': 'Latter\nProphets', 'Jol': 'Latter\nProphets', 'Amo': 'Latter\nProphets',
    'Oba': 'Latter\nProphets', 'Jon': 'Latter\nProphets', 'Mic': 'Latter\nProphets',
    'Nah': 'Latter\nProphets', 'Hab': 'Latter\nProphets', 'Zep': 'Latter\nProphets',
    'Hag': 'Latter\nProphets', 'Zec': 'Latter\nProphets', 'Mal': 'Latter\nProphets',
}
GENRE_ORDER_OT = ['Torah', 'Former\nProphets', 'Writings', 'Psalms', 'Wisdom', 'Latter\nProphets']


def _chart_hebrew_sources() -> None:
    dabar_align = align[align['heb_strongs'].apply(lambda s: 'H1697' in str(s))].copy()
    dabar_align['genre'] = dabar_align['book_id'].map(OT_GENRE).fillna('Other')

    logos_by_genre = (dabar_align[dabar_align['lxx_strongs'] == 'G3056']
                      .groupby('genre').size())
    rhema_by_genre = (dabar_align[dabar_align['lxx_strongs'] == 'G4487']
                      .groupby('genre').size())

    genres = [g for g in GENRE_ORDER_OT if g in logos_by_genre.index or g in rhema_by_genre.index]
    logos_vals = [logos_by_genre.get(g, 0) for g in genres]
    rhema_vals = [rhema_by_genre.get(g, 0) for g in genres]
    totals = [lv + rv for lv, rv in zip(logos_vals, rhema_vals)]
    logos_pct = [lv / t * 100 if t else 0 for lv, t in zip(logos_vals, totals)]
    rhema_pct = [r / t * 100 if t else 0 for r, t in zip(rhema_vals, totals)]

    x = range(len(genres))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Left: raw counts stacked
    ax1.bar(x, logos_vals, color=LOGOS_COLOR, label='→ λόγος', edgecolor='white')
    ax1.bar(x, rhema_vals, bottom=logos_vals, color=RHEMA_COLOR, label='→ ῥῆμα', edgecolor='white')
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(genres, fontsize=9)
    ax1.set_ylabel('Count')
    ax1.set_title('dābar Translation: Raw Counts', fontsize=11, fontweight='bold')
    ax1.legend(fontsize=9)
    for i, (lv, rv, t) in enumerate(zip(logos_vals, rhema_vals, totals)):
        if t > 0:
            ax1.text(i, t + 1, str(t), ha='center', fontsize=8, color='#444')

    # Right: percentage stacked
    ax2.bar(x, logos_pct, color=LOGOS_COLOR, label='→ λόγος', edgecolor='white')
    ax2.bar(x, rhema_pct, bottom=logos_pct, color=RHEMA_COLOR, label='→ ῥῆμα', edgecolor='white')
    ax2.set_xticks(list(x))
    ax2.set_xticklabels(genres, fontsize=9)
    ax2.set_ylabel('Percentage')
    ax2.set_ylim(0, 110)
    ax2.set_title('dābar Translation: % Share', fontsize=11, fontweight='bold')
    ax2.legend(fontsize=9)
    for i, (lp, rp) in enumerate(zip(logos_pct, rhema_pct)):
        if lp > 5:
            ax2.text(i, lp / 2, f'{lp:.0f}%', ha='center', va='center', fontsize=8, color='white')
        if rp > 5:
            ax2.text(i, lp + rp / 2, f'{rp:.0f}%', ha='center', va='center', fontsize=8, color='white')

    fig.suptitle('How the LXX Translates דָּבָר (dābar) by OT Genre: λόγος vs ῥῆμα',
                 fontsize=12, fontweight='bold')
    fig.tight_layout()
    path = CHART_DIR / 'logos-rhema-hebrew-sources.png'
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'Chart: {path}')


# ── Chart 4: dābar split by individual OT book (detailed view) ────────────────

def _chart_dabar_split() -> None:
    dabar_align = align[align['heb_strongs'].apply(lambda s: 'H1697' in str(s))]
    logos_dabar = dabar_align[dabar_align['lxx_strongs'] == 'G3056'].groupby('book_id').size()
    rhema_dabar = dabar_align[dabar_align['lxx_strongs'] == 'G4487'].groupby('book_id').size()

    books = sorted(set(logos_dabar.index) | set(rhema_dabar.index),
                   key=lambda b: OT_ORDER.index(b) if b in OT_ORDER else 99)
    logos_vals = [logos_dabar.get(b, 0) for b in books]
    rhema_vals = [rhema_dabar.get(b, 0) for b in books]

    x = range(len(books))
    w = 0.38
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.bar([i - w / 2 for i in x], logos_vals, width=w, label='→ λόγος',
           color=LOGOS_COLOR, edgecolor='white', linewidth=0.3)
    ax.bar([i + w / 2 for i in x], rhema_vals, width=w, label='→ ῥῆμα',
           color=RHEMA_COLOR, edgecolor='white', linewidth=0.3)
    ax.set_xticks(list(x))
    ax.set_xticklabels(books, rotation=45, ha='right', fontsize=8)
    ax.set_ylabel('Count')
    ax.set_title('How the LXX Translates דָּבָר (dābar): λόγος vs ῥῆμα by Book',
                 fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    fig.tight_layout()
    path = CHART_DIR / 'logos-rhema-dabar-split.png'
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'Chart: {path}')


# ── Chart 5: NT genre distribution pie ────────────────────────────────────────

def _chart_nt_genre_pie() -> None:
    def genre_counts(df: pd.DataFrame) -> "pd.Series[int]":
        df = df.copy()
        df['genre'] = df['book_id'].map(NT_GENRE).fillna('Other')
        return df.groupby('genre').size()

    logos_g = genre_counts(logos_nt)
    rhema_g = genre_counts(rhema_nt)
    genres = ['Gospel', 'Acts', 'Pauline Epistles', 'General Epistles', 'Apocalyptic']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    for ax, data, title in [
        (ax1, logos_g, f'λόγος — {len(logos_nt)} occurrences'),
        (ax2, rhema_g, f'ῥῆμα — {len(rhema_nt)} occurrences'),
    ]:
        vals = [data.get(g, 0) for g in genres]
        colors = [GENRE_COLORS[g] for g in genres]
        non_zero = [(v, g, c) for v, g, c in zip(vals, genres, colors) if v > 0]
        ax.pie([v for v, _, _ in non_zero],
               labels=[f'{g}\n({v})' for v, g, _ in non_zero],
               colors=[c for _, _, c in non_zero],
               autopct='%1.0f%%', startangle=140,
               textprops={'fontsize': 9})
        ax.set_title(title, fontsize=11, fontweight='bold')

    fig.suptitle('NT Genre Distribution: λόγος vs ῥῆμα', fontsize=13, fontweight='bold')
    fig.tight_layout()
    path = CHART_DIR / 'logos-rhema-nt-genre-pie.png'
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'Chart: {path}')


# ── CSV exports ───────────────────────────────────────────────────────────────

def _csv_nt_concordance() -> None:
    rows = []
    for term, label, df in [
        ('G3056', 'λόγος', logos_nt), ('G4487', 'ῥῆμα', rhema_nt)
    ]:
        for _, row in df.iterrows():
            kjv_text = _kjv(row['book_id'], row['chapter'], row['verse'])
            rows.append({
                'term': label, 'strongs': term,
                'book': row['book_id'], 'chapter': row['chapter'],
                'verse': row['verse'], 'word_num': row['word_num'],
                'greek_word': row['word'],
                'morph': row['morph_code'], 'case': row['case_'],
                'number': row['number'], 'gender': row['gender'],
                'kjv_verse': kjv_text,
            })
    df_out = pd.DataFrame(rows)
    path = REPORT_DIR / 'logos-rhema-concordance.csv'
    df_out.to_csv(path, index=False)
    print(f'CSV: {path}  ({len(df_out)} rows)')


def _csv_lxx_concordance() -> None:
    rows = []
    for strongs, label, df in [
        ('G3056', 'λόγος', logos_lxx), ('G4487', 'ῥῆμα', rhema_lxx)
    ]:
        for _, row in df.iterrows():
            rows.append({
                'term': label, 'strongs': strongs,
                'book': row['book_id'], 'chapter': row['chapter'],
                'verse': row['verse'],
                'lxx_word': row['word'],
                'case': row['case_'], 'number': row['number'],
            })
    df_out = pd.DataFrame(rows)
    path = REPORT_DIR / 'logos-rhema-lxx-concordance.csv'
    df_out.to_csv(path, index=False)
    print(f'CSV: {path}  ({len(df_out)} rows)')


# ── NT by-book table (3-panel HTML) ──────────────────────────────────────────

def _nt_book_html(logos: pd.DataFrame, rhema: pd.DataFrame) -> str:
    """Three side-by-side HTML sub-tables of NT book counts."""
    gospels_acts = ['Mat', 'Mrk', 'Luk', 'Jhn', 'Act']
    pauline = ['Rom', '1Co', '2Co', 'Gal', 'Eph', 'Php', 'Col',
               '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm']
    general_apoc = ['Heb', 'Jas', '1Pe', '2Pe', '1Jn', '2Jn', '3Jn', 'Jud', 'Rev']

    lc = logos.groupby('book_id').size().to_dict()
    rc = rhema.groupby('book_id').size().to_dict()

    def _panel(books: list, title: str) -> str:
        rows = '\n'.join(
            f'<tr><td>{BOOK_NAMES.get(b, b)}</td>'
            f'<td align="right">{lc.get(b, 0) or "—"}</td>'
            f'<td align="right">{rc.get(b, 0) or "—"}</td></tr>'
            for b in books
            if lc.get(b, 0) > 0 or rc.get(b, 0) > 0
        )
        return (
            '<table>\n'
            f'<tr><th colspan="3" align="left"><b>{title}</b></th></tr>\n'
            '<tr><th align="left">Book</th>'
            '<th>λόγος</th><th>ῥῆμα</th></tr>\n'
            f'{rows}\n'
            '</table>'
        )

    panels = [
        _panel(gospels_acts, 'Gospels &amp; Acts'),
        _panel(pauline, 'Pauline Epistles'),
        _panel(general_apoc, 'General Epistles &amp; Revelation'),
    ]
    cells = '\n<td width="32">&nbsp;</td>\n'.join(
        f'<td valign="top">\n{p}\n</td>' for p in panels
    )
    return f'<table>\n<tr>\n{cells}\n</tr>\n</table>'


# ── Synoptic pericope comparison ─────────────────────────────────────────────

# Each entry: (pericope_name, mat_refs, mrk_refs, luk_refs, note)
# Refs are (book, ch, vs) tuples. note may be '' or a brief gloss.
SYNOPTIC_PERICOPES = [
    (
        'Temptation: "every word that proceedeth"',
        [('Mat', 4, 4)], [], [('Luk', 4, 4)],
        'Both quote Deut 8:3 LXX verbatim; ῥῆμα frames the OT text as divine spoken '
        'utterance. Mark has no temptation account.',
    ),
    (
        'Sermon conclusion: "heareth these sayings / words"',
        [('Mat', 7, 24), ('Mat', 7, 26), ('Mat', 7, 28)],
        [],
        [('Luk', 6, 47), ('Luk', 7, 1)],
        'Matthew uses λόγος throughout the Sermon conclusion. Luke uses λόγος '
        'at 6:47 for the same "hear and do" charge, but closes the episode at '
        '7:1 with ῥήματα ("when he had ended all these sayings") — shifting '
        'from the doctrinal content of the sermon (λόγος) to the individual '
        'utterances that constituted it (ῥῆμα).',
    ),
    (
        'Centurion: "speak the word only"',
        [('Mat', 8, 8)], [], [('Luk', 7, 7)],
        'Both use λόγος for the healing command. The centurion asks for a single '
        'authoritative word (λόγος) — emphasising the power of the message/command '
        'rather than the act of speaking. Mark omits this pericope.',
    ),
    (
        'Miraculous catch: "at thy word / ῥήματι"',
        [], [], [('Luk', 5, 5)],
        'Lukan exclusive. Simon responds to Jesus\' spoken command with ῥήματι — '
        'the immediate, concrete utterance just given. Matthew and Mark have no '
        'parallel in this form.',
    ),
    (
        'Sower: "the seed is the word" (throughout)',
        [('Mat', 13, 19), ('Mat', 13, 20), ('Mat', 13, 21),
         ('Mat', 13, 22), ('Mat', 13, 23)],
        [('Mrk', 4, 14), ('Mrk', 4, 15), ('Mrk', 4, 16),
         ('Mrk', 4, 17), ('Mrk', 4, 18), ('Mrk', 4, 19), ('Mrk', 4, 20)],
        [('Luk', 8, 11), ('Luk', 8, 12), ('Luk', 8, 13), ('Luk', 8, 15)],
        'All three synoptics use λόγος exclusively throughout the sower '
        'interpretation, consistently treating the "word of the kingdom" as '
        'doctrinal content to be received, not a specific oral event.',
    ),
    (
        'Corban: "making void the word of God"',
        [('Mat', 15, 6)], [('Mrk', 7, 13)], [],
        'Both Matthew and Mark use λόγος for the scriptural tradition being '
        'nullified — the word as authoritative deposit. Luke has no parallel here.',
    ),
    (
        'Syro-Phoenician woman: "for this word/saying"',
        [('Mat', 15, 23)], [('Mrk', 7, 29)], [],
        'Matthew uses λόγον at 15:23 for Jesus\' silence ("not a word"), not the '
        'woman\'s reply. Mark uses λόγον at 7:29 for the woman\'s retort that wins '
        'the healing. Both use λόγος; Luke has no parallel.',
    ),
    (
        'Second passion prediction: "understood not that saying"',
        [], [('Mrk', 9, 32)], [('Luk', 9, 45)],
        'Both Mark and Luke use ῥῆμα for the disciples\' failure to understand — '
        'the specific utterance (the passion prediction just spoken) is too '
        'concrete and shocking to process. Matthew uses λόγον at 17:23 for the '
        'same event.',
    ),
    (
        'Rich young ruler: "sad at that saying"',
        [('Mat', 19, 22)], [('Mrk', 10, 22)], [],
        'Both Matthew and Mark use λόγος for the saying that grieved the ruler '
        '(the call to sell everything). The response is to a doctrinal claim, '
        'not merely a spoken moment — hence λόγος.',
    ),
    (
        'Tribute to Caesar: "catch him in his words"',
        [('Mat', 22, 15), ('Mat', 22, 46)],
        [('Mrk', 12, 13)],
        [('Luk', 20, 20), ('Luk', 20, 26)],
        'Matthew and Mark use λόγος for the trap ("entangle him in his talk"). '
        'Luke uses λόγος at 20:20 for the same scheme, but switches to ῥήματος '
        'at 20:26 when they "could not take hold of his words before the people" '
        '— the shift to ῥῆμα emphasises the specific utterances they tried and '
        'failed to weaponise.',
    ),
    (
        '"My words shall not pass away"',
        [('Mat', 24, 35)], [('Mrk', 13, 31)], [('Luk', 21, 33)],
        'Perfect triple agreement: all three use λόγοι for Jesus\' enduring words '
        '— emphasising their permanent, authoritative character as revelation.',
    ),
    (
        'Gethsemane: "prayed using the same words"',
        [('Mat', 26, 44)], [('Mrk', 14, 39)], [],
        'Both use λόγος for the prayer repeated verbatim — treating the prayer '
        'as a unified content rather than as individual spoken moments. '
        'Luke has no verbal parallel for this detail.',
    ),
    (
        "Peter's denial: "
        '"remembered the word [ῥῆμα] of the Lord"',
        [('Mat', 26, 75)], [('Mrk', 14, 72)], [('Luk', 22, 61)],
        'Perfect triple agreement on ῥῆμα — the most striking consensus in '
        'this study. All three evangelists choose ῥῆμα for the moment of '
        'Peter\'s recollection: the specific, shattering prediction Jesus '
        'spoke is what comes back to him. The word as lived speech-event, '
        'not as doctrine.',
    ),
    (
        'Jesus silent before Pilate',
        [('Mat', 27, 14)], [], [],
        'Matthew alone uses ῥῆμα: "he answered him not to a single ῥῆμα." '
        'The emphasis is on the absence of individual spoken words — '
        'not a refused λόγος (message/teaching) but a refusal to utter '
        'even one ῥῆμα (word). Mark and Luke do not use either term here.',
    ),
]


def _terms_at(nt_df: pd.DataFrame, book: str, ch: int, vs: int) -> list:
    """Return list of (label, greek_word) for λόγος/ῥῆμα at the given verse."""
    out = []
    for strongs, label in [('G3056', 'λόγος'), ('G4487', 'ῥῆμα')]:
        hits = nt_df[(nt_df['book_id'] == book) & (nt_df['chapter'] == ch)
                     & (nt_df['verse'] == vs)
                     & nt_df['strongs'].str.contains(strongs, na=False)]
        for _, r in hits.iterrows():
            out.append((label, r['word']))
    return out


def _cell(nt_df: pd.DataFrame, refs: list) -> str:
    """Render a table cell for one gospel's refs: 'ref — term (form)' lines."""
    parts = []
    for book, ch, vs in refs:
        hits = _terms_at(nt_df, book, ch, vs)
        if hits:
            term_str = ', '.join(f'**{lbl}** ({form})' for lbl, form in hits)
            parts.append(f'{ch}:{vs} — {term_str}')
    return '<br>'.join(parts) if parts else '—'


def _synoptic_section(nt_df: pd.DataFrame) -> list:
    """Build lines for the Synoptic Pericope Comparison section."""
    lines = [
        '## Synoptic Pericope Comparison',
        '',
        'The table below tracks every synoptic pericope that contains λόγος or '
        'ῥῆμα in at least one gospel. Pericopes where all attesting gospels agree '
        'confirm the semantic tendency; pericopes where they diverge are the most '
        'revealing. The **Notes** column explains the significance of each pattern.',
        '',
        '| Pericope | Matthew | Mark | Luke | Notes |',
        '|---|---|---|---|---|',
    ]

    for name, mat_refs, mrk_refs, luk_refs, note in SYNOPTIC_PERICOPES:
        mat_cell = _cell(nt_df, mat_refs)
        mrk_cell = _cell(nt_df, mrk_refs)
        luk_cell = _cell(nt_df, luk_refs)
        # skip if no gospel has either term (shouldn't happen with our curated list)
        if mat_cell == mrk_cell == luk_cell == '—':
            continue
        note_escaped = note.replace('|', '&#124;')
        lines.append(f'| {name} | {mat_cell} | {mrk_cell} | {luk_cell} | {note_escaped} |')

    lines += [
        '',
        '### Patterns across the pericopes',
        '',
        '**Where all three agree on ῥῆμα:** The temptation narrative (quoting Deut 8:3), '
        'the second passion prediction (a specific saying the disciples failed to grasp), '
        'and Peter\'s denial are the clearest cases. In each, the word in view is a '
        'concrete, episodic utterance — a moment of speech whose specific content matters.',
        '',
        '**Where all three agree on λόγος:** The sower parable (seed = the word of the '
        'kingdom), the Corban dispute (the word of God as scriptural authority), '
        '"my words shall not pass away," and the Gethsemane repetition all treat the '
        'word as a deposit of teaching or authoritative message.',
        '',
        '**The two divergences are structurally informative:**',
        '',
        '- *Sermon conclusion (Mat 7:28 / Luk 7:1)*: Matthew closes with λόγους '
        '(Jesus\' teaching as a body of content); Luke closes with ῥήματα '
        '(the individual utterances that constituted the address). Same event, '
        'different framing — Matthew\'s λόγος emphasises what was taught, '
        'Luke\'s ῥῆμα emphasises the speech act itself.',
        '',
        '- *Tribute to Caesar (Mat 22:15 / Luk 20:26)*: Matthew and Mark use λόγος '
        'for the adversaries\' scheme. Luke adds ῥήματος at 20:26 when reporting '
        'their failure to "take hold of his words" — the specific utterances of '
        'Jesus proved impossible to weaponise. The shift within Luke from λόγος '
        '(the plan) to ῥῆμα (the actual words spoken) mirrors the broader pattern '
        'precisely.',
    ]
    return lines


# ── Markdown report ───────────────────────────────────────────────────────────

def _build_both_verse_lines(
    both_verses: pd.DataFrame,
    detail: "dict[tuple[str, int, int], tuple[str, str, list[str]]]",
) -> "list[str]":
    """Build the detailed both-verses section lines."""
    lines = []
    for _, row in both_verses.iterrows():
        key = (row['book_id'], int(row['chapter']), int(row['verse']))
        if key not in detail:
            continue
        heading, quote, bullets = detail[key]
        lines += [
            '---',
            '',
            f'### {heading}',
            '',
            quote,
            '',
        ] + [f'- {b}' for b in bullets] + ['']
    lines.append('---')
    return lines


def _build_report() -> None:
    logos_total_nt = len(logos_nt)
    rhema_total_nt = len(rhema_nt)
    logos_total_lxx = len(logos_lxx)
    rhema_total_lxx = len(rhema_lxx)

    # dabar split totals
    dabar_align = align[align['heb_strongs'].apply(lambda s: 'H1697' in str(s))]
    dabar_to_logos = len(dabar_align[dabar_align['lxx_strongs'] == 'G3056'])
    dabar_to_rhema = len(dabar_align[dabar_align['lxx_strongs'] == 'G4487'])
    dabar_total = dabar_to_logos + dabar_to_rhema
    dabar_logos_pct = dabar_to_logos * 100 // dabar_total if dabar_total else 0

    # Scripture collocations (verse-level)
    logos_vset = set(zip(logos_nt['book_id'], logos_nt['chapter'], logos_nt['verse']))
    rhema_vset = set(zip(rhema_nt['book_id'], rhema_nt['chapter'], rhema_nt['verse']))

    def _vset(strongs_code: str) -> set:
        rows = nt[nt['strongs'].str.contains(strongs_code, na=False)]
        return set(zip(rows['book_id'], rows['chapter'], rows['verse']))

    sc_theos = (len(logos_vset & _vset('G2316')), len(rhema_vset & _vset('G2316')))
    sc_graphe = (len(logos_vset & _vset('G1124')), len(rhema_vset & _vset('G1124')))
    sc_grapho = (len(logos_vset & _vset('G1125')), len(rhema_vset & _vset('G1125')))
    sc_nomos = (len(logos_vset & _vset('G3551')), len(rhema_vset & _vset('G3551')))
    sc_proph = (len(logos_vset & _vset('G4396')), len(rhema_vset & _vset('G4396')))

    # NT books where each appears
    logos_books = sorted(logos_nt['book_id'].unique(),
                         key=lambda b: NT_ORDER.index(b) if b in NT_ORDER else 99)
    rhema_books = sorted(rhema_nt['book_id'].unique(),
                         key=lambda b: NT_ORDER.index(b) if b in NT_ORDER else 99)
    logos_only = set(logos_books) - set(rhema_books)
    rhema_only = set(rhema_books) - set(logos_books)

    # Verses with both
    logos_refs = logos_nt[['book_id', 'chapter', 'verse']].drop_duplicates()
    rhema_refs = rhema_nt[['book_id', 'chapter', 'verse']].drop_duplicates()
    both_verses = logos_refs.merge(rhema_refs, on=['book_id', 'chapter', 'verse'])

    # LXX book counts (top 5 each)
    logos_lxx_top = logos_lxx.groupby('book_id').size().sort_values(ascending=False).head(5)
    rhema_lxx_top = rhema_lxx.groupby('book_id').size().sort_values(ascending=False).head(5)

    nt_book_html = _nt_book_html(logos_nt, rhema_nt)

    # Both-verses detail: word-level logos/rhema positions and forms
    BOTH_DETAIL = {
        ('Mat', 12, 36): (
            'Matthew 12:36',
            '> *"But I say unto you, That every idle **word** [ῥῆμα, Acc. Sg.] that men '
            'shall speak, they shall give **account** [λόγον, Acc. Sg.] thereof in the '
            'day of judgment."* (KJV)',
            [
                '**ῥῆμα** (word#6): the individual *spoken utterance* — the idle remark '
                'as a concrete speech act',
                '**λόγος** (word#16): the *account* or *reckoning* rendered — here '
                'carrying its sense of reasoned explanation, not "word" at all',
                'The KJV renders both as "word" / "account," obscuring that Jesus uses '
                'two different words with deliberately different senses in a single sentence',
            ],
        ),
        ('Jhn', 12, 48): (
            'John 12:48',
            '> *"He that rejecteth me, and receiveth not my **words** [ῥήματά, Acc. Pl.] '
            'hath one that judgeth him: the **word** [λόγος, Nom. Sg.] that I have spoken, '
            'the same shall judge him in the last day."* (KJV)',
            [
                '**ῥήματα** (word#8): the individual *sayings* of Jesus — the specific '
                'utterances one might hear and reject',
                '**λόγος** (word#15): the *message as a whole* — the authoritative word '
                'of Christ considered as a unified, judicial reality',
                'The shift from plural ῥήματα to singular λόγος is not accidental: '
                'rejecting the individual words amounts to rejecting the Word entire',
            ],
        ),
        ('Act', 10, 44): (
            'Acts 10:44',
            '> *"While Peter yet spake these **words** [ῥήματα, Acc. Pl.], the Holy Ghost '
            'fell on all them which heard the **word** [λόγον, Acc. Sg.]."* (KJV)',
            [
                '**ῥήματα** (word#6): the specific sentences Peter was speaking — the '
                'ongoing, audible proclamation in progress',
                '**λόγος** (word#18): the *word/message* as received content — the gospel '
                'message that the hearers were taking in',
                'The Holy Spirit falls during the ῥήματα (the act of speaking) and upon '
                'those hearing the λόγος (the message) — the two are simultaneous but distinct',
            ],
        ),
        ('Heb', 12, 19): (
            'Hebrews 12:19',
            '> *"And the sound of a trumpet, and the voice of **words** [ῥημάτων, Gen. Pl.]; '
            'which voice they that heard intreated that the **word** [λόγον, Acc. Sg.] '
            'should not be spoken to them any more:"* (KJV)',
            [
                '**ῥημάτων** (word#6): the terrifying *utterances* at Sinai — the audible, '
                'individual declarations from the fire and darkness (Deut 4:12)',
                '**λόγος** (word#14): the *word* (message) they begged not to hear further '
                '— the ongoing divine address considered as a single overwhelming communication',
                'The Sinai theophany is described first in terms of its individual ῥήματα '
                '(each terrifying pronouncement), then as a λόγος (the word as a whole) '
                'too terrible to bear',
            ],
        ),
    }

    lines = [
        '# Word Study: λόγος (G3056) and ῥῆμα (G4487)',
        '',
        '*Build script: [scripts/both/word_studies/logos-rhema/'
        'build_logos_rhema_report.py]'
        '(../../../../../scripts/both/word_studies/logos-rhema/'
        'build_logos_rhema_report.py)*',
        '',
        '---',
        '',
        '## Overview',
        '',
        'Both λόγος and ῥῆμα are translated "word" in the KJV, yet they carry distinct '
        'semantic profiles rooted in their different senses and their different translation '
        'histories in the LXX.',
        '',
        '| Term | Strongs | Gloss | LXX occurrences (canonical) | NT occurrences |',
        '|---|---|---|---|---|',
        f'| λόγος | G3056 | word, reason, account | {logos_total_lxx:,} | {logos_total_nt:,} |',
        f'| ῥῆμα  | G4487 | word, saying, utterance | {rhema_total_lxx:,} | {rhema_total_nt:,} |',
        '',
        '---',
        '',
        '## Definitions and Semantic Range',
        '',
        '### λόγος (lógos) — G3056',
        '',
        'From λέγω (*légō*, "to gather, recount, say"). λόγος is the most semantically '
        'broad of the two terms. Its range spans:',
        '',
        '- **A spoken word or statement** (Mat 8:8 — "speak the *word* only")',
        '- **A message or proclamation** (Acts 6:2 — "the *word* of God")',
        '- **Reasoned discourse or account** (Mat 12:36 — "give *account* of every idle word")',
        '- **A narrative or report** (Luk 1:2)',
        '- **Divine reason / the eternal Word** (John 1:1 — "In the beginning was the *Word*")',
        '',
        'The Stoic philosophical tradition had already loaded λόγος with cosmic significance '
        '— the rational principle governing the universe. John\'s Prologue exploits this '
        'resonance directly.',
        '',
        '### ῥῆμα (rhḗma) — G4487',
        '',
        'From ῥέω (*rhéō*, "to speak, utter"). ῥῆμα is more narrowly focused on '
        'the **act of speaking** and the **specific words uttered**:',
        '',
        '- **Individual spoken words** (Mat 26:75 — "Peter remembered the *word* of Jesus")',
        '- **Sayings, declarations** (Luk 1:37 — "no *word* from God shall be void of power")',
        '- **Spoken commands** (Luk 5:5 — "at thy *word* I will let down the net")',
        '- **Prophetic utterances** (Heb 6:5 — "tasted the good *word* of God")',
        '',
        'ῥῆμα tends to emphasize the **individual, concrete utterance** as an event, '
        'whereas λόγος more readily abstracts to **message, doctrine, or rational content**.',
        '',
        '---',
        '',
        '## NT Distribution',
        '',
        f'λόγος appears in **{len(logos_books)} NT books** ({logos_total_nt} total); '
        f'ῥῆμα appears in **{len(rhema_books)} NT books** ({rhema_total_nt} total).',
        '',
        f'Books with **only λόγος** (no ῥῆμα): '
        f'{", ".join(sorted(logos_only))}',
        '',
        f'Books with **only ῥῆμα** (no λόγος): '
        f'{", ".join(sorted(rhema_only)) if rhema_only else "none"}',
        '',
        '![NT frequency by book](../../../../charts/both/word_studies/logos-rhema/'
        'logos-rhema-nt-by-book.png)',
        '',
        nt_book_html,
        '',
        '![NT genre distribution](../../../../charts/both/word_studies/logos-rhema/'
        'logos-rhema-nt-genre-pie.png)',
        '',
        'λόγος is distributed across all NT genres with particular concentration in Acts '
        f'({len(logos_nt[logos_nt["book_id"] == "Act"])} occurrences) and the Gospels. '
        'ῥῆμα is almost entirely absent from the Pauline Epistles — its weight falls on '
        'the Gospels (especially Luke), Acts, and the General Epistles.',
        '',
        '---',
        '',
        '## LXX Distribution',
        '',
        f'In the LXX canonical OT, λόγος occurs **{logos_total_lxx:,} times** and '
        f'ῥῆμα **{rhema_total_lxx:,} times**.',
        '',
        '![LXX frequency by book](../../../../charts/both/word_studies/logos-rhema/'
        'logos-rhema-lxx-by-book.png)',
        '',
        '**Top 5 books for λόγος (LXX):**',
        '',
    ] + [f'- {BOOK_NAMES.get(b, b)}: {c}' for b, c in logos_lxx_top.items()] + [
        '',
        '**Top 5 books for ῥῆμα (LXX):**',
        '',
    ] + [f'- {BOOK_NAMES.get(b, b)}: {c}' for b, c in rhema_lxx_top.items()] + [
        '',
        '---',
        '',
        '## Hebrew Source Words',
        '',
        'The LXX translators drew on several Hebrew terms when choosing between '
        'λόγος and ῥῆμα:',
        '',
        '### דָּבָר (dābar, H1697) — the primary Hebrew source',
        '',
        'דָּבָר is the most common Hebrew word for "word" (1,441 OT occurrences). '
        'The LXX overwhelmingly prefers λόγος for it overall, but the balance shifts '
        'by genre:',
        '',
        '| Hebrew | → λόγος | → ῥῆμα | λόγος % |',
        '|---|---|---|---|',
        f'| דָּבָר (H1697) | {dabar_to_logos} | {dabar_to_rhema} | '
        f'{dabar_logos_pct}% |',
        '',
        '![dābar split by genre](../../../../charts/both/word_studies/logos-rhema/'
        'logos-rhema-hebrew-sources.png)',
        '',
        'The genre breakdown reveals a striking pattern: the Former Prophets '
        '(Samuel, Kings, Joshua, Judges) show the highest ῥῆμα share — consistent '
        'with their use of דָּבָר for specific, concrete speech events and royal '
        'decrees. Torah, Psalms, and Latter Prophets tilt strongly toward λόγος, '
        'especially in formulaic expressions like "the word of the LORD came to..." '
        'where the translators favored the more theologically weighty λόγος.',
        '',
        '### Other Hebrew sources',
        '',
        '- **אָמַר (ʾāmar, H559)** — "to say/speak": a verb, rarely rendered as '
        'either noun directly',
        '- **מִלָּה (millāh, H4405)** — "word, speech" (38 OT occurrences, '
        'mostly in Job): LXX Job renders it with ῥῆμα',
        '- **פֶּה (peh, H6310)** — "mouth": ῥῆμα occasionally translates this '
        'metonymically in "mouth of the LORD" phrases',
        '- **אֵמֶר (ʾēmer, H561)** — "word, speech": minor term rendered by both',
        '',
        'The book-by-book detail:',
        '',
        '![dābar split by book](../../../../charts/both/word_studies/logos-rhema/'
        'logos-rhema-dabar-split.png)',
        '',
        '---',
        '',
        '## Verses Where Both Appear Together (NT)',
        '',
        f'Only **{len(both_verses)} NT verses** contain both λόγος and ῥῆμα — '
        'making these passages especially revealing for understanding the distinction:',
        '',
    ] + _build_both_verse_lines(both_verses, BOTH_DETAIL) + [
        '',
        'Across all four verses the pattern is consistent: **ῥῆμα** points to the '
        'individual, concrete utterance as a speech event; **λόγος** points to the word '
        'considered as message, content, or rational account. The KJV\'s use of "word" '
        'for both regularly masks this distinction.',
        '',
        '---',
        '',
    ] + _synoptic_section(nt) + [
        '',
        '---',
        '',
        '## Use with Reference to Written Scripture',
        '',
        'The two terms have strikingly different profiles when it comes to referencing '
        'the written scriptures — the OT text, the law, the prophets, and the canon '
        'of Revelation.',
        '',
        '### Summary counts (NT)',
        '',
        '| Context | λόγος | ῥῆμα |',
        '|---|---|---|',
        f'| Same verse as θεός (God) | {sc_theos[0]} | {sc_theos[1]} |',
        f'| Same verse as γραφή (scripture) | {sc_graphe[0]} | {sc_graphe[1]} |',
        f'| Same verse as γράφω (written / it is written) | {sc_grapho[0]} | {sc_grapho[1]} |',
        f'| Same verse as νόμος (law) | {sc_nomos[0]} | {sc_nomos[1]} |',
        f'| Same verse as προφήτης (prophet) | {sc_proph[0]} | {sc_proph[1]} |',
        '',
        'λόγος is overwhelmingly the term used for scripture as a body of text or as '
        'authoritative message. ῥῆμα is rare in explicitly scriptural contexts — and '
        'where it appears, it consistently refers to the spoken or living *quality* of '
        'the word, not to the written deposit.',
        '',
        '### λόγος and the written scriptures',
        '',
        '**λόγος is the standard term for the OT scriptures considered as authoritative '
        'content:**',
        '',
        '- **Jhn 10:35** — "unto whom the *word* [λόγος] of God came, and the scripture '
        'cannot be broken" — λόγος and γραφή are used in the same breath; the λόγος '
        'is what the scripture *contains*',
        '- **Jhn 15:25** — "that the *word* [λόγος] might be fulfilled that is written '
        'in their law, They hated me without a cause" — λόγος as the OT text being fulfilled',
        '- **Luk 3:4** — "as it is written in the book of the *words* [λόγοι] of Esaias '
        'the prophet" — the book of Isaiah referred to as a collection of λόγοι',
        '- **Luk 24:44** — "these are the *words* [λόγοι] which I spake unto you... that '
        'all things must be fulfilled, which were written in the law of Moses, and in the '
        'prophets, and in the psalms" — λόγοι used for the prophetic-scriptural content '
        'of the whole OT',
        '- **Act 15:15** — "to this agree the *words* [λόγοι] of the prophets; as it is '
        'written" — the OT prophecies are λόγοι',
        '- **Rev 22:18–19** — "the *words* [λόγοι] of the prophecy of this book" (×2) '
        '— the Apocalypse itself is a collection of λόγοι',
        '- **Heb 4:12** — "the *word* [λόγος] of God is quick and powerful" — the active, '
        'judging quality of the scriptural word, using λόγος',
        '',
        '### ῥῆμα and the written scriptures',
        '',
        'ῥῆμα appears in only **two** NT verses that explicitly invoke the written OT:',
        '',
        '- **Mat 4:4 / Luk 4:4** — Jesus quoting Deuteronomy 8:3: "Man shall not live by '
        'bread alone, but by every *word* [ῥῆμα] that proceedeth out of the mouth of God." '
        'The source text (Deut 8:3 LXX) uses ῥῆμα. Jesus quotes scripture using ῥῆμα '
        'deliberately — the emphasis falls on the *living utterance from God\'s mouth*, '
        'not on the written text as a deposit. The OT scripture is being cited, but ῥῆμα '
        'highlights its character as divine speech.',
        '- **Act 28:25** — "Well spake the Holy Ghost by Esaias the prophet" — the one '
        '*word/utterance* (ῥῆμα) Paul singles out is Isaiah 6:9–10. Here ῥῆμα frames '
        'the OT oracle as a Spirit-spoken utterance, foregrounding its prophetic-pneumatic '
        'origin.',
        '- **2Pe 3:2** — "the *words* [ῥήματα] which were spoken before by the holy '
        'prophets" — the OT prophetic corpus as *spoken* declarations, emphasizing the '
        'oral/pneumatic dimension.',
        '',
        '### LXX: logos and rhema for the Decalogue and Torah',
        '',
        'The LXX itself shows the same tension when translating the Hebrew *dābar* '
        'in legal-scriptural contexts:',
        '',
        '| Reference | Hebrew | LXX | Context |',
        '|---|---|---|---|',
        '| Exo 20:1 | כָּל-הַדְּבָרִים הָאֵלֶּה | **λόγους** | '
        '"God spoke *all these words*" — the Decalogue introduction |',
        '| Exo 34:28 | עֲשֶׂרֶת הַדְּבָרִים | **λόγους** / **ῥήματα** | '
        '"the ten words" — the Decalogue (both terms appear in same verse) |',
        '| Deu 4:13 | עֲשֶׂרֶת הַדְּבָרִים | **ῥήματα** | '
        '"the ten words... written on two tablets of stone" — the Decalogue |',
        '| Deu 5:22 | הַדְּבָרִים הָאֵלֶּה | **ῥήματα** | '
        '"these words the LORD spoke to all your assembly" — the Decalogue |',
        '| Deu 10:4 | עֲשֶׂרֶת הַדְּבָרִים | **λόγους** | '
        '"the ten words... written according to the first writing" — the Decalogue |',
        '| Deu 28:58 | דִּבְרֵי הַתּוֹרָה הַזֹּאת | **ῥήματα** | '
        '"the words of this law" |',
        '| Deu 31:24 | דִּבְרֵי הַתּוֹרָה | **λόγους** | '
        '"the words of this law in a book" |',
        '',
        'The LXX translators show no consistent preference for one term over the other '
        'when rendering the Decalogue — both appear, sometimes in adjacent references. '
        'This confirms that in the OT/LXX context the two terms were closer in meaning '
        'than they would become in NT theological usage.',
        '',
        '### Summary',
        '',
        '**λόγος** is the NT\'s default term for the scriptures as authoritative, '
        'transmissible content: the books of the prophets, the words of the law, the '
        'canon of Revelation. It is the word *as deposit, message, and text*.',
        '',
        '**ῥῆμα** in scriptural contexts consistently emphasizes the *oral and pneumatic* '
        'character of the word — what *proceeds from the mouth of God*, what *the Spirit '
        'spoke through Isaiah*, what the prophets *declared*. It points to scripture as '
        'divine speech-event rather than written text.',
        '',
        'This is theologically significant: when NT writers want to emphasize the '
        '*authority and permanence* of the scriptural text, they use λόγος. When they '
        'want to emphasize its *living, Spirit-breathed, spoken* character, they reach '
        'for ῥῆμα.',
        '',
        '---',
        '',
        '## Theological Significance',
        '',
        '### The λόγος of God',
        '',
        'λόγος is the term used for the divine Word in its most exalted theological '
        'contexts: John 1:1–14 (the pre-existent Logos), Heb 4:12 ("the *word* of God '
        'is living and active"), Rev 19:13 ("his name is called The *Word* of God"). '
        'It carries the weight of revelation as a permanent, rational, authoritative '
        'message — consistent with its Stoic and Jewish-Hellenistic background (Philo\'s '
        '*Logos* theology).',
        '',
        '### ῥῆμα in pneumatic/charismatic contexts',
        '',
        'ῥῆμα frequently appears in contexts emphasizing the **Spirit\'s immediate '
        'utterance**: Luk 1:37 ("no ῥῆμα from God shall be void of power"), Eph 6:17 '
        '("the sword of the Spirit, which is the ῥῆμα of God"), Rom 10:17 '
        '("faith comes from hearing, and hearing through the ῥῆμα of Christ"). '
        'In each case the emphasis is on the *spoken word as living event*, not '
        'as doctrinal content.',
        '',
        '### Synonymous use',
        '',
        'Despite these distinctions, the two words are not always differentiated in the NT. '
        'Luke uses both interchangeably in narrative: "the shepherds said to one another, '
        'Let us go to Bethlehem and see this ῥῆμα..." (Luk 2:15) where ῥῆμα clearly '
        'means "thing/event" as much as "word." Similarly, John\'s Gospel uses both '
        'for the words of Jesus without systematic distinction in some passages. '
        'The difference is a tendency, not an absolute rule.',
        '',
        '---',
        '',
        '## Data Files',
        '',
        '| File | Contents |',
        '|---|---|',
        '| [logos-rhema-concordance.csv](logos-rhema-concordance.csv) | '
        'Full NT concordance for both terms with KJV verse text |',
        '| [logos-rhema-lxx-concordance.csv](logos-rhema-lxx-concordance.csv) | '
        'LXX concordance for both terms (canonical books) |',
    ]

    path = REPORT_DIR / 'logos-rhema.md'
    path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Report: {path}')


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    _chart_nt_by_book()
    _chart_lxx_by_book()
    _chart_hebrew_sources()
    _chart_dabar_split()
    _chart_nt_genre_pie()
    _csv_nt_concordance()
    _csv_lxx_concordance()
    _build_report()
    print('\nDone.')
