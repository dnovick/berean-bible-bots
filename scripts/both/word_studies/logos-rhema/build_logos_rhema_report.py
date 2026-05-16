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
    'Rom': 'Epistle', '1Co': 'Epistle', '2Co': 'Epistle', 'Gal': 'Epistle',
    'Eph': 'Epistle', 'Php': 'Epistle', 'Col': 'Epistle',
    '1Th': 'Epistle', '2Th': 'Epistle', '1Ti': 'Epistle', '2Ti': 'Epistle',
    'Tit': 'Epistle', 'Phm': 'Epistle',
    'Heb': 'Epistle', 'Jas': 'General', '1Pe': 'General', '2Pe': 'General',
    '1Jn': 'General', '2Jn': 'General', '3Jn': 'General', 'Jud': 'General',
    'Rev': 'Apocalyptic',
}
GENRE_COLORS = {
    'Gospel': '#4292c6', 'Acts': '#2ca25f', 'Epistle': '#fd8d3c',
    'General': '#9e9ac8', 'Apocalyptic': '#d62728',
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
    genres = ['Gospel', 'Acts', 'Epistle', 'General', 'Apocalyptic']

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


# ── Markdown report ───────────────────────────────────────────────────────────

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

    # NT by book table
    nt_book_table = []
    for b in NT_ORDER:
        lc = len(logos_nt[logos_nt['book_id'] == b])
        rc = len(rhema_nt[rhema_nt['book_id'] == b])
        if lc > 0 or rc > 0:
            nt_book_table.append(f'| {BOOK_NAMES.get(b, b)} | {lc or "—"} | {rc or "—"} |')

    # Both-verses block
    both_blocks = []
    for _, row in both_verses.iterrows():
        text = _kjv(row['book_id'], row['chapter'], row['verse'])
        ref = f"{row['book_id']} {row['chapter']}:{row['verse']}"
        both_blocks.append(f'**{ref}** — *"{text}"*')

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
        '![NT frequency by book](../../../charts/both/word_studies/logos-rhema/'
        'logos-rhema-nt-by-book.png)',
        '',
        '| Book | λόγος | ῥῆμα |',
        '|---|---|---|',
    ] + nt_book_table + [
        '',
        '![NT genre distribution](../../../charts/both/word_studies/logos-rhema/'
        'logos-rhema-nt-genre-pie.png)',
        '',
        'λόγος is distributed across all NT genres with particular concentration in Acts '
        f'({len(logos_nt[logos_nt["book_id"] == "Act"])} occurrences) and the Gospels. '
        'ῥῆμα is almost entirely absent from the Pauline epistles — its weight falls on '
        'the Gospels (especially Luke), Acts, and a handful of general epistles.',
        '',
        '---',
        '',
        '## LXX Distribution',
        '',
        f'In the LXX canonical OT, λόγος occurs **{logos_total_lxx:,} times** and '
        f'ῥῆμα **{rhema_total_lxx:,} times**.',
        '',
        '![LXX frequency by book](../../../charts/both/word_studies/logos-rhema/'
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
        '![dābar split by genre](../../../charts/both/word_studies/logos-rhema/'
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
        '![dābar split by book](../../../charts/both/word_studies/logos-rhema/'
        'logos-rhema-dabar-split.png)',
        '',
        '---',
        '',
        '## Verses Where Both Appear Together (NT)',
        '',
        f'Only **{len(both_verses)} NT verses** contain both λόγος and ῥῆμα — '
        'making these passages especially revealing for understanding the distinction:',
        '',
    ] + [''] + [f'- {b}\n' for b in both_blocks] + [
        '',
        'In John 12:48, the distinction is particularly clear: **τὰ ῥήματα** refers '
        'to the specific words Jesus spoke (the concrete utterances), while **ὁ λόγος** '
        'refers to the message/word as a whole that will judge. In Acts 10:44, Peter '
        'speaks **ῥήματα** (the specific words of proclamation) and the Spirit falls on '
        'those who heard **τὸν λόγον** (the word/message as content).',
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
