"""Build NT Greek verb tense distribution report.

Analyses verb tense usage across every NT book and author, scaled by
verse count so books of different length are comparable.

Outputs:
  output/reports/nt/verbs/tense-distribution/nt-tense-distribution.md
  output/reports/nt/verbs/tense-distribution/nt-tense-distribution.csv
  output/reports/nt/verbs/tense-distribution/*.png  (multiple charts)
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
from src.bible_grammar.core.query import query  # noqa: E402

REPORT_DIR = Path('output/reports/nt/verbs/tense-distribution')
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ── Tense consolidation ───────────────────────────────────────────────────────
# TAGNT uses R/2R for Perfect, L/2L for Pluperfect, 2P for 2nd Perfect stem,
# Aorist/2nd Aorist for first/second aorist (different stem, same tense).
TENSE_MAP: dict[str, str] = {
    'Present':    'Present',
    'Imperfect':  'Imperfect',
    'Aorist':     'Aorist',
    '2nd Aorist': 'Aorist',
    'Future':     'Future',
    '2nd Future': 'Future',
    'R':          'Perfect',
    '2R':         'Perfect',
    '2P':         'Perfect',
    'L':          'Pluperfect',
    '2L':         'Pluperfect',
}

TENSES = ['Present', 'Imperfect', 'Aorist', 'Future', 'Perfect', 'Pluperfect']

TENSE_COLORS: dict[str, str] = {
    'Present':    '#4C72B0',
    'Imperfect':  '#64B5CD',
    'Aorist':     '#DD6B48',
    'Future':     '#5BA85A',
    'Perfect':    '#9B59B6',
    'Pluperfect': '#C0A040',
}

# ── Book metadata ─────────────────────────────────────────────────────────────
BOOK_ORDER = [
    'Mat', 'Mrk', 'Luk', 'Jhn', 'Act',
    'Rom', '1Co', '2Co', 'Gal', 'Eph', 'Php', 'Col',
    '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm',
    'Heb', 'Jas', '1Pe', '2Pe', '1Jn', '2Jn', '3Jn', 'Jud', 'Rev',
]

BOOK_NAMES: dict[str, str] = {
    'Mat': 'Matthew', 'Mrk': 'Mark', 'Luk': 'Luke', 'Jhn': 'John',
    'Act': 'Acts', 'Rom': 'Romans', '1Co': '1 Corinthians',
    '2Co': '2 Corinthians', 'Gal': 'Galatians', 'Eph': 'Ephesians',
    'Php': 'Philippians', 'Col': 'Colossians', '1Th': '1 Thessalonians',
    '2Th': '2 Thessalonians', '1Ti': '1 Timothy', '2Ti': '2 Timothy',
    'Tit': 'Titus', 'Phm': 'Philemon', 'Heb': 'Hebrews', 'Jas': 'James',
    '1Pe': '1 Peter', '2Pe': '2 Peter', '1Jn': '1 John', '2Jn': '2 John',
    '3Jn': '3 John', 'Jud': 'Jude', 'Rev': 'Revelation',
}

# Author groupings
AUTHORS: dict[str, list[str]] = {
    'Matthew':  ['Mat'],
    'Mark':     ['Mrk'],
    'Luke':     ['Luk', 'Act'],
    'John':     ['Jhn', '1Jn', '2Jn', '3Jn', 'Rev'],
    'Paul':     ['Rom', '1Co', '2Co', 'Gal', 'Eph', 'Php', 'Col',
                 '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm'],
    'Hebrews':  ['Heb'],
    'Catholic': ['Jas', '1Pe', '2Pe', 'Jud'],
}

# Genre groupings
GENRES: dict[str, list[str]] = {
    'Gospel':      ['Mat', 'Mrk', 'Luk', 'Jhn'],
    'Acts':        ['Act'],
    'Pauline Ep.': ['Rom', '1Co', '2Co', 'Gal', 'Eph', 'Php', 'Col',
                    '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm'],
    'Hebrews':     ['Heb'],
    'Catholic Ep.': ['Jas', '1Pe', '2Pe', '1Jn', '2Jn', '3Jn', 'Jud'],
    'Apocalyptic': ['Rev'],
}


# ── Data loading ──────────────────────────────────────────────────────────────

def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Return (verb_df, verse_counts, word_counts)."""
    df = query(testament='nt')

    verse_counts = (
        df.drop_duplicates(['book_id', 'chapter', 'verse'])
        .groupby('book_id').size()
        .rename('verses')
    )
    word_counts = df.groupby('book_id').size().rename('words')

    verbs = df[df['part_of_speech'] == 'Verb'].copy()
    verbs['tense_clean'] = verbs['tense'].map(TENSE_MAP)
    verbs = verbs[verbs['tense_clean'].notna()]

    return verbs, verse_counts, word_counts


def book_tense_table(verbs: pd.DataFrame,
                     verse_counts: pd.Series) -> pd.DataFrame:
    """Per-book tense counts and rates per 100 verses."""
    raw = (verbs.groupby(['book_id', 'tense_clean'])
           .size().unstack(fill_value=0))
    # Ensure all tenses present
    for t in TENSES:
        if t not in raw.columns:
            raw[t] = 0
    raw = raw[TENSES]
    raw = raw.reindex(BOOK_ORDER).fillna(0).astype(int)

    rates = raw.div(verse_counts.reindex(BOOK_ORDER), axis=0) * 100
    return raw, rates


def group_tense_table(verbs: pd.DataFrame,
                      groups: dict[str, list[str]],
                      verse_counts: pd.Series) -> pd.DataFrame:
    """Aggregate tense counts and rates for named groups."""
    rows_raw, rows_rate = [], []
    for group, books in groups.items():
        v_sub = verbs[verbs['book_id'].isin(books)]
        vc_sub = verse_counts.reindex(books).sum()
        counts = v_sub['tense_clean'].value_counts().reindex(TENSES, fill_value=0)
        rates = counts / vc_sub * 100
        rows_raw.append(pd.Series(counts, name=group))
        rows_rate.append(pd.Series(rates, name=group))
    return pd.DataFrame(rows_raw), pd.DataFrame(rows_rate)


# ── Charts ────────────────────────────────────────────────────────────────────

def chart_heatmap(rates: pd.DataFrame) -> Path:
    """Heatmap: books × tenses, colour = rate per 100 verses."""
    labels = [BOOK_NAMES.get(b, b) for b in rates.index]
    n_books = len(labels)
    fig, ax = plt.subplots(figsize=(11, n_books * 0.38 + 1.5))

    data = rates.values.T  # shape: (tenses, books)
    # Normalise column-wise so each tense's colour scale is independent
    col_max = data.max(axis=1, keepdims=True)
    col_max[col_max == 0] = 1
    normed = data / col_max

    im = ax.imshow(normed, aspect='auto', cmap='Blues', vmin=0, vmax=1)

    ax.set_xticks(range(n_books))
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=8)
    ax.set_yticks(range(len(TENSES)))
    ax.set_yticklabels(TENSES, fontsize=9)

    # Annotate cells with rate value
    for i, tense in enumerate(TENSES):
        for j in range(n_books):
            val = rates.values[j, i]
            ax.text(j, i, f'{val:.1f}', ha='center', va='center',
                    fontsize=6.5, color='white' if normed[i, j] > 0.55 else '#333333')

    ax.set_title('NT Verb Tense Frequency by Book\n(rate per 100 verses; '
                 'colour intensity relative to each tense\'s maximum)',
                 fontsize=10, fontweight='bold', pad=10)
    fig.colorbar(im, ax=ax, shrink=0.5, label='Relative intensity')
    plt.tight_layout()
    out = REPORT_DIR / 'nt-tense-heatmap.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved {out}')
    return out


def chart_stacked_bar_books(rates: pd.DataFrame) -> Path:
    """Stacked 100% bar chart: tense share per book."""
    labels = [BOOK_NAMES.get(b, b) for b in rates.index]
    totals = rates.sum(axis=1)
    totals[totals == 0] = 1
    pct = rates.div(totals, axis=0) * 100

    n = len(labels)
    fig, ax = plt.subplots(figsize=(14, 5))
    bottom = np.zeros(n)
    x = np.arange(n)
    for tense in TENSES:
        vals = pct[tense].values
        ax.bar(x, vals, bottom=bottom, color=TENSE_COLORS[tense],
               label=tense, width=0.75)
        # Label segments > 8%
        for i, (v, b) in enumerate(zip(vals, bottom)):
            if v >= 8:
                ax.text(i, b + v / 2, f'{v:.0f}%', ha='center', va='center',
                        fontsize=6, color='white', fontweight='bold')
        bottom += vals

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=8)
    ax.set_ylabel('% of all verb forms')
    ax.set_title('NT Verb Tense Distribution by Book (% share)',
                 fontsize=11, fontweight='bold')
    ax.legend(loc='upper right', fontsize=8, ncol=3)
    ax.set_ylim(0, 105)
    plt.tight_layout()
    out = REPORT_DIR / 'nt-tense-stacked-books.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved {out}')
    return out


def chart_author_grouped(rate_authors: pd.DataFrame) -> Path:
    """Grouped bar chart: tense rates per author."""
    authors = list(rate_authors.index)
    x = np.arange(len(TENSES))
    n_auth = len(authors)
    width = 0.8 / n_auth

    cmap = plt.get_cmap('tab10')
    auth_colors = {a: cmap(i / n_auth) for i, a in enumerate(authors)}

    fig, ax = plt.subplots(figsize=(12, 5))
    for i, author in enumerate(authors):
        vals = [rate_authors.loc[author, t] for t in TENSES]
        offset = (i - n_auth / 2 + 0.5) * width
        bars = ax.bar(x + offset, vals, width=width * 0.9,
                      color=auth_colors[author], label=author, alpha=0.9)
        for bar, v in zip(bars, vals):
            if v >= 2:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.3,
                        f'{v:.1f}', ha='center', va='bottom',
                        fontsize=5.5, color='#333333')

    ax.set_xticks(x)
    ax.set_xticklabels(TENSES, fontsize=10)
    ax.set_ylabel('Verb forms per 100 verses')
    ax.set_title('NT Verb Tense Rate by Author\n(per 100 verses)',
                 fontsize=11, fontweight='bold')
    ax.legend(fontsize=8, ncol=4)
    plt.tight_layout()
    out = REPORT_DIR / 'nt-tense-by-author.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved {out}')
    return out


def chart_genre_grouped(rate_genres: pd.DataFrame) -> Path:
    """Grouped bar chart: tense rates per genre."""
    genres = list(rate_genres.index)
    x = np.arange(len(TENSES))
    n_g = len(genres)
    width = 0.8 / n_g

    cmap = plt.get_cmap('Set2')
    genre_colors = {g: cmap(i / n_g) for i, g in enumerate(genres)}

    fig, ax = plt.subplots(figsize=(12, 5))
    for i, genre in enumerate(genres):
        vals = [rate_genres.loc[genre, t] for t in TENSES]
        offset = (i - n_g / 2 + 0.5) * width
        bars = ax.bar(x + offset, vals, width=width * 0.9,
                      color=genre_colors[genre], label=genre, alpha=0.9)
        for bar, v in zip(bars, vals):
            if v >= 2:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.3,
                        f'{v:.1f}', ha='center', va='bottom',
                        fontsize=5.5, color='#333333')

    ax.set_xticks(x)
    ax.set_xticklabels(TENSES, fontsize=10)
    ax.set_ylabel('Verb forms per 100 verses')
    ax.set_title('NT Verb Tense Rate by Genre\n(per 100 verses)',
                 fontsize=11, fontweight='bold')
    ax.legend(fontsize=8, ncol=3)
    plt.tight_layout()
    out = REPORT_DIR / 'nt-tense-by-genre.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved {out}')
    return out


def chart_present_aorist_ratio(rates: pd.DataFrame) -> Path:
    """Scatter plot: present vs aorist rate per book, coloured by genre."""
    genre_for_book: dict[str, str] = {}
    for genre, books in GENRES.items():
        for b in books:
            genre_for_book[b] = genre

    genre_order = list(GENRES.keys())
    cmap = plt.get_cmap('Set2')
    genre_colors = {g: cmap(i / len(genre_order)) for i, g in enumerate(genre_order)}

    fig, ax = plt.subplots(figsize=(9, 7))

    for book in BOOK_ORDER:
        if book not in rates.index:
            continue
        x_val = rates.loc[book, 'Present']
        y_val = rates.loc[book, 'Aorist']
        genre = genre_for_book.get(book, 'Other')
        color = genre_colors.get(genre, 'gray')
        ax.scatter(x_val, y_val, color=color, s=70, zorder=3)
        ax.annotate(BOOK_NAMES.get(book, book), (x_val, y_val),
                    fontsize=7.5, xytext=(4, 3), textcoords='offset points',
                    color='#333333')

    # Diagonal reference line (equal present and aorist)
    lim_max = max(rates['Present'].max(), rates['Aorist'].max()) * 1.1
    ax.plot([0, lim_max], [0, lim_max], 'k--', linewidth=0.8, alpha=0.4,
            label='Present = Aorist')
    ax.set_xlabel('Present forms per 100 verses', fontsize=10)
    ax.set_ylabel('Aorist forms per 100 verses', fontsize=10)
    ax.set_title('Present vs. Aorist Rate by Book\n(above diagonal = aorist-dominant; '
                 'below = present-dominant)',
                 fontsize=10, fontweight='bold')

    # Legend for genres
    handles = [mpatches.Patch(color=genre_colors[g], label=g) for g in genre_order]
    diag_line = plt.Line2D(
        [0], [0], linestyle='--', color='k', alpha=0.4, label='Present = Aorist'
    )
    handles.append(diag_line)
    ax.legend(handles=handles, fontsize=8, loc='upper left')
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    plt.tight_layout()
    out = REPORT_DIR / 'nt-present-vs-aorist.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved {out}')
    return out


def chart_perfect_by_author(rate_authors: pd.DataFrame) -> Path:
    """Horizontal bar chart: perfect tense rate by author."""
    authors = list(rate_authors.index)
    vals = [rate_authors.loc[a, 'Perfect'] for a in authors]
    y = np.arange(len(authors))
    cmap = plt.get_cmap('tab10')
    colors = [cmap(i / len(authors)) for i in range(len(authors))]

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.barh(y, vals, color=colors, alpha=0.9)
    for bar, v in zip(bars, vals):
        ax.text(v + 0.1, bar.get_y() + bar.get_height() / 2,
                f'{v:.1f}', va='center', fontsize=9)
    ax.set_yticks(y)
    ax.set_yticklabels(authors, fontsize=10)
    ax.set_xlabel('Perfect verb forms per 100 verses')
    ax.set_title('Perfect Tense Usage by Author\n(per 100 verses)',
                 fontsize=11, fontweight='bold')
    plt.tight_layout()
    out = REPORT_DIR / 'nt-perfect-by-author.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved {out}')
    return out


# ── Report markdown ───────────────────────────────────────────────────────────

def build_report(
    raw: pd.DataFrame,
    rates: pd.DataFrame,
    raw_auth: pd.DataFrame,
    rate_auth: pd.DataFrame,
    raw_genre: pd.DataFrame,
    rate_genre: pd.DataFrame,
    verse_counts: pd.Series,
) -> Path:
    total_verbs = raw.values.sum()
    lines = [
        '# NT Greek Verb Tense Distribution',
        '',
        '**Text:** TAGNT (Byzantine/Textus Receptus) · **Scope:** All 27 NT books',
        '',
        '## Contents',
        '',
        '- [About This Report](#about-this-report)',
        '- [Key Observations](#key-observations)',
        '- [Tense Frequency Heatmap](#tense-frequency-heatmap)',
        '- [Tense Share by Book](#tense-share-by-book)',
        '- [Present vs. Aorist Scatter](#present-vs-aorist-scatter)',
        '- [Tense Rate by Author](#tense-rate-by-author)',
        '- [Tense Rate by Genre](#tense-rate-by-genre)',
        '- [Perfect Tense by Author](#perfect-tense-by-author)',
        '- [Per-Book Summary Table](#per-book-summary-table)',
        '- [Per-Author Summary Table](#per-author-summary-table)',
        '- [Per-Genre Summary Table](#per-genre-summary-table)',
        '',
        '---',
        '',
        '## About This Report',
        '',
        'This report analyses the distribution of Greek verb tenses across every book'
        ' of the NT, scaled by verse count so that books of different length are'
        ' directly comparable. All verb forms are included — indicative, participle,'
        ' infinitive, subjunctive, imperative, and optative — because tense in Greek'
        ' carries aspect information in all moods and non-finite forms, not just the'
        ' indicative.',
        '',
        '**Tense consolidation** (TAGNT codes → display name):',
        '',
        '| TAGNT code(s) | Tense | Aspectual force |',
        '|---|---|---|',
        '| Present | Present | Imperfective — ongoing, repeated, or habitual action |',
        '| Imperfect | Imperfect | Imperfective in past time (indicative only) |',
        '| Aorist, 2nd Aorist | Aorist | Perfective — action viewed as a whole |',
        '| Future, 2nd Future | Future | Expectation of future completion |',
        '| R, 2R, 2P | Perfect | Stative — completed action with present relevance |',
        '| L, 2L | Pluperfect | State in past time; rarest tense in NT |',
        '',
        f'**Total verb forms analysed:** {total_verbs:,}  ',
        '**Books:** 27  ',
        '',
        '---',
        '',
        '## Key Observations',
        '',
    ]

    # Compute observations dynamically from the data
    # Present-dominant books (below diagonal: present > aorist)
    pres_dom = rates[rates['Present'] > rates['Aorist']].index.tolist()
    aor_dom = rates[rates['Aorist'] > rates['Present']].index.tolist()

    # Highest/lowest present rate
    top_pres = rates['Present'].idxmax()
    top_aor = rates['Aorist'].idxmax()
    top_perf = rates['Perfect'].idxmax()
    top_imperf = rates['Imperfect'].idxmax()

    # Author with highest rates
    top_auth_pres = rate_auth['Present'].idxmax()
    top_auth_aor = rate_auth['Aorist'].idxmax()
    top_auth_perf = rate_auth['Perfect'].idxmax()

    pres_dom_names = ', '.join(BOOK_NAMES.get(b, b) for b in pres_dom)
    aor_dom_names = ', '.join(BOOK_NAMES.get(b, b) for b in aor_dom)

    lines += [
        f'- **Present-dominant books** (present > aorist per verse):'
        f' {pres_dom_names}',
        f'- **Aorist-dominant books** (aorist > present per verse):'
        f' {aor_dom_names}',
        f'- **Highest present rate:** {BOOK_NAMES.get(top_pres, top_pres)}'
        f' ({rates.loc[top_pres, "Present"]:.1f} per 100 verses)',
        f'- **Highest aorist rate:** {BOOK_NAMES.get(top_aor, top_aor)}'
        f' ({rates.loc[top_aor, "Aorist"]:.1f} per 100 verses)',
        f'- **Highest imperfect rate:** {BOOK_NAMES.get(top_imperf, top_imperf)}'
        f' ({rates.loc[top_imperf, "Imperfect"]:.1f} per 100 verses)'
        f' — imperfect is primarily a narrative tense',
        f'- **Highest perfect rate:** {BOOK_NAMES.get(top_perf, top_perf)}'
        f' ({rates.loc[top_perf, "Perfect"]:.1f} per 100 verses)',
        f'- **Author with highest present rate:** {top_auth_pres}'
        f' ({rate_auth.loc[top_auth_pres, "Present"]:.1f} per 100 verses)',
        f'- **Author with highest aorist rate:** {top_auth_aor}'
        f' ({rate_auth.loc[top_auth_aor, "Aorist"]:.1f} per 100 verses)',
        f'- **Author with highest perfect rate:** {top_auth_perf}'
        f' ({rate_auth.loc[top_auth_perf, "Perfect"]:.1f} per 100 verses)'
        f' — the perfect signals completed action with present effect,'
        f' theologically significant in Hebrews and Paul',
        '',
        '---',
        '',
        '## Tense Frequency Heatmap',
        '',
        'Colour intensity for each tense is normalised relative to that'
        ' tense\'s own maximum across all books — so each row (tense) has'
        ' its own scale. Numbers show the raw rate per 100 verses.',
        '',
        '![NT tense heatmap](nt-tense-heatmap.png)',
        '',
        '---',
        '',
        '## Tense Share by Book',
        '',
        'Each bar is divided by tense share (% of all verb forms in that book).'
        ' This reveals whether a book\'s overall verbal style is'
        ' present-heavy, aorist-heavy, or balanced.',
        '',
        '![NT tense stacked bars](nt-tense-stacked-books.png)',
        '',
        '---',
        '',
        '## Present vs. Aorist Scatter',
        '',
        'Each point is a book. Points **above** the dashed diagonal are'
        ' aorist-dominant; points **below** are present-dominant.'
        ' Genre is colour-coded.',
        '',
        '![Present vs aorist scatter](nt-present-vs-aorist.png)',
        '',
        '---',
        '',
        '## Tense Rate by Author',
        '',
        'Rates are per 100 verses, pooling all books attributed to each author.'
        ' Author attributions follow the traditional/canonical view.',
        '',
        '![Tense rate by author](nt-tense-by-author.png)',
        '',
        '---',
        '',
        '## Tense Rate by Genre',
        '',
        'Rates are per 100 verses. Genre groupings:'
        ' Gospels (Matthew–John), Acts, Pauline Epistles, Hebrews,'
        ' Catholic Epistles (James, 1–2 Peter, 1–3 John, Jude),'
        ' Apocalyptic (Revelation).',
        '',
        '![Tense rate by genre](nt-tense-by-genre.png)',
        '',
        '---',
        '',
        '## Perfect Tense by Author',
        '',
        'The perfect is theologically loaded in the NT: it asserts that a past'
        ' action has abiding present consequence. Its distribution across authors'
        ' is more varied than the present or aorist.',
        '',
        '![Perfect tense by author](nt-perfect-by-author.png)',
        '',
        '---',
        '',
        '## Per-Book Summary Table',
        '',
        '> Rates are verb forms per 100 verses. "Verses" = verse count in TAGNT.',
        '',
        '| Book | Verses | Present | Imperfect | Aorist | Future |'
        ' Perfect | Pluperfect |',
        '|---|---:|---:|---:|---:|---:|---:|---:|',
    ]

    for book in BOOK_ORDER:
        if book not in rates.index:
            continue
        vc = int(verse_counts.get(book, 0))
        r = rates.loc[book]
        lines.append(
            f'| {BOOK_NAMES.get(book, book)} | {vc} '
            f'| {r["Present"]:.1f} | {r["Imperfect"]:.1f}'
            f' | {r["Aorist"]:.1f} | {r["Future"]:.1f}'
            f' | {r["Perfect"]:.1f} | {r["Pluperfect"]:.1f} |'
        )

    lines += [
        '',
        '---',
        '',
        '## Per-Author Summary Table',
        '',
        '| Author | Books | Verses | Present | Imperfect | Aorist |'
        ' Future | Perfect | Pluperfect |',
        '|---|---|---:|---:|---:|---:|---:|---:|---:|',
    ]

    for author, books in AUTHORS.items():
        vc = int(verse_counts.reindex(books).sum())
        r = rate_auth.loc[author]
        book_names = ', '.join(BOOK_NAMES.get(b, b) for b in books)
        lines.append(
            f'| {author} | {book_names} | {vc}'
            f' | {r["Present"]:.1f} | {r["Imperfect"]:.1f}'
            f' | {r["Aorist"]:.1f} | {r["Future"]:.1f}'
            f' | {r["Perfect"]:.1f} | {r["Pluperfect"]:.1f} |'
        )

    lines += [
        '',
        '---',
        '',
        '## Per-Genre Summary Table',
        '',
        '| Genre | Books | Verses | Present | Imperfect | Aorist |'
        ' Future | Perfect | Pluperfect |',
        '|---|---|---:|---:|---:|---:|---:|---:|---:|',
    ]

    for genre, books in GENRES.items():
        vc = int(verse_counts.reindex(books).sum())
        r = rate_genre.loc[genre]
        book_abbrevs = ', '.join(books)
        lines.append(
            f'| {genre} | {book_abbrevs} | {vc}'
            f' | {r["Present"]:.1f} | {r["Imperfect"]:.1f}'
            f' | {r["Aorist"]:.1f} | {r["Future"]:.1f}'
            f' | {r["Perfect"]:.1f} | {r["Pluperfect"]:.1f} |'
        )

    lines += [
        '',
        '---',
        '',
        '*Greek text: TAGNT (Byzantine/Textus Receptus tradition,'
        ' STEPBible CC BY 4.0, Tyndale House Cambridge).*',
        ' *Verb tense data covers all moods and non-finite forms.*',
        ' *Generated by'
        ' [scripts/nt/verbs/build_nt_tense_distribution.py]'
        '(../../../../scripts/nt/verbs/build_nt_tense_distribution.py).*',
    ]

    out = REPORT_DIR / 'nt-tense-distribution.md'
    out.write_text('\n'.join(lines), encoding='utf-8')
    print(f'  Saved {out}')
    return out


# ── CSV exports ───────────────────────────────────────────────────────────────

def build_csvs(raw: pd.DataFrame, rates: pd.DataFrame,
               rate_auth: pd.DataFrame, rate_genre: pd.DataFrame,
               verse_counts: pd.Series) -> None:
    # Per-book rates
    out = rates.copy()
    out.index = [BOOK_NAMES.get(b, b) for b in out.index]
    out.insert(0, 'verses', verse_counts.reindex(BOOK_ORDER).values)
    out.to_csv(REPORT_DIR / 'nt-tense-distribution.csv')
    print(f'  Saved {REPORT_DIR}/nt-tense-distribution.csv')

    # Per-author rates
    rate_auth.to_csv(REPORT_DIR / 'nt-tense-distribution-authors.csv')
    print(f'  Saved {REPORT_DIR}/nt-tense-distribution-authors.csv')

    # Per-genre rates
    rate_genre.to_csv(REPORT_DIR / 'nt-tense-distribution-genres.csv')
    print(f'  Saved {REPORT_DIR}/nt-tense-distribution-genres.csv')


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('Loading data...')
    verbs, verse_counts, word_counts = load_data()

    print('Computing tables...')
    raw, rates = book_tense_table(verbs, verse_counts)
    raw_auth, rate_auth = group_tense_table(verbs, AUTHORS, verse_counts)
    raw_genre, rate_genre = group_tense_table(verbs, GENRES, verse_counts)

    print('Building charts...')
    chart_heatmap(rates)
    chart_stacked_bar_books(rates)
    chart_present_aorist_ratio(rates)
    chart_author_grouped(rate_auth)
    chart_genre_grouped(rate_genre)
    chart_perfect_by_author(rate_auth)

    print('Building report...')
    build_report(raw, rates, raw_auth, rate_auth,
                 raw_genre, rate_genre, verse_counts)

    print('Building CSVs...')
    build_csvs(raw, rates, rate_auth, rate_genre, verse_counts)

    print('Done.')
