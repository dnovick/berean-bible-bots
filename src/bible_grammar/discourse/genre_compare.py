"""
Genre comparison: morphological pattern heatmaps across canonical sections.

Compares how grammatical features distribute differently across the literary
genres of the Hebrew OT and Greek NT:

  OT comparisons
  ──────────────
  • Verb stem distribution     (Qal / Niphal / Piel / Hiphil / …)
  • Verb conjugation           (Perfect / Imperfect / Wayyiqtol / Participle / …)
  • Part-of-speech mix         (Noun / Verb / Adjective / Particle / …)
  • Noun state                 (Absolute / Construct)

  NT comparisons
  ──────────────
  • Verb tense                 (Aorist / Present / Perfect / Imperfect / Future)
  • Verb voice                 (Active / Middle / Passive / Deponent)
  • Verb mood                  (Indicative / Participle / Infinitive / Subjunctive / Imperative)
  • Part-of-speech mix

Usage
-----
from bible_grammar.discourse.genre_compare import genre_compare, print_genre_compare
from bible_grammar.discourse.genre_compare import genre_heatmap, genre_report

# Terminal tables
print_genre_compare('OT', feature='verb_stem')
print_genre_compare('NT', feature='verb_tense')

# Heatmap chart
genre_heatmap('OT', feature='verb_conjugation',
              output_path='output/charts/ot-genre-conjugation.png')

# Full Markdown report
genre_report(output_dir='output/reports')
"""

from __future__ import annotations
import pandas as pd
from pathlib import Path

# ── Genre / section definitions ──────────────────────────────────────────────

OT_GENRES: dict[str, list[str]] = {
    'Torah':      ['Gen', 'Exo', 'Lev', 'Num', 'Deu'],
    'Historical': ['Jos', 'Jdg', 'Rut', '1Sa', '2Sa', '1Ki', '2Ki', '1Ch', '2Ch', 'Ezr', 'Neh', 'Est'],  # noqa: E501
    'Wisdom':     ['Job', 'Psa', 'Pro', 'Ecc', 'Sng'],
    'Prophets':   ['Isa', 'Jer', 'Lam', 'Ezk', 'Dan', 'Hos', 'Jol', 'Amo', 'Oba', 'Jon', 'Mic',
                   'Nah', 'Hab', 'Zep', 'Hag', 'Zec', 'Mal'],
}

NT_GENRES: dict[str, list[str]] = {
    'Gospels & Acts': ['Mat', 'Mrk', 'Luk', 'Jhn', 'Act'],
    'Pauline':        ['Rom', '1Co', '2Co', 'Gal', 'Eph', 'Php', 'Col', '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm'],  # noqa: E501
    'General & Rev':  ['Heb', 'Jas', '1Pe', '2Pe', '1Jn', '2Jn', '3Jn', 'Jud', 'Rev'],
}

# ── Normalization maps ────────────────────────────────────────────────────────

_TENSE_NORM = {
    'Present':    'Present',
    'Imperfect':  'Imperfect',
    'Future':     'Future',
    'Aorist':     'Aorist',
    '2nd Aorist': 'Aorist',
    'R':          'Perfect',
    '2R':         'Perfect',
    'L':          'Pluperfect',
    '2L':         'Pluperfect',
    '2P':         'Aorist',
    '2nd Future': 'Future',
}

_VOICE_NORM = {
    'Active':           'Active',
    'Middle':           'Middle',
    'Passive':          'Passive',
    'Deponent':         'Deponent',
    'Middle Deponent':  'Deponent',
    'Middle or Passive': 'Middle',
    'N':                'Other',
}

# Display order for each feature
_ORDERS = {
    'verb_stem':        ['Qal', 'Niphal', 'Piel', 'Pual', 'Hithpael', 'Hiphil', 'Hophal'],
    'verb_conjugation': ['Perfect', 'Consecutive Perfect', 'Imperfect', 'Consecutive Imperfect',
                         'Imperative', 'Infinitive construct', 'Infinitive absolute',
                         'Participle', 'Participle passive', 'Jussive'],
    'pos':              ['Noun', 'Verb', 'Adjective', 'Pronoun', 'Preposition', 'Adverb', 'Particle'],  # noqa: E501
    'noun_state':       ['Absolute', 'Construct'],
    'verb_tense':       ['Present', 'Imperfect', 'Future', 'Aorist', 'Perfect', 'Pluperfect'],
    'verb_voice':       ['Active', 'Middle', 'Passive', 'Deponent'],
    'verb_mood':        ['Indicative', 'Participle', 'Infinitive', 'Subjunctive', 'Imperative', 'Optative'],  # noqa: E501
}


# ── Core data loading ─────────────────────────────────────────────────────────

def _load_ot() -> 'pd.DataFrame':
    from ..core import db as _db
    df = _db.load()
    return df[df['source'] == 'TAHOT'].copy()


def _load_nt() -> 'pd.DataFrame':
    from ..core import db as _db
    df = _db.load()
    return df[df['source'] == 'TAGNT'].copy()


# ── Core computation ──────────────────────────────────────────────────────────

def genre_compare(
    corpus: str = 'OT',
    feature: str = 'verb_stem',
    *,
    normalize: bool = True,
) -> 'pd.DataFrame':
    """
    Build a genre×feature count (or percentage) matrix.

    Parameters
    ----------
    corpus  : 'OT' or 'NT'
    feature : one of
                OT: 'verb_stem', 'verb_conjugation', 'pos', 'noun_state'
                NT: 'verb_tense', 'verb_voice', 'verb_mood', 'pos'
    normalize: if True, values are % of tokens in each genre (row %)

    Returns
    -------
    DataFrame with genres as rows and feature categories as columns.
    Includes a 'Total' column with the absolute token count.
    """
    import pandas as pd

    genres = OT_GENRES if corpus == 'OT' else NT_GENRES
    df = _load_ot() if corpus == 'OT' else _load_nt()

    order = _ORDERS.get(feature, [])

    rows = []
    for genre, books in genres.items():
        g = df[df['book_id'].isin(books)]

        if feature == 'verb_stem':
            sub = g[g['part_of_speech'] == 'Verb']
            col = 'stem'
        elif feature == 'verb_conjugation':
            sub = g[g['part_of_speech'] == 'Verb']
            col = 'conjugation'
        elif feature == 'noun_state':
            sub = g[(g['part_of_speech'] == 'Noun') & (g['noun_type'] == 'Common')]
            col = 'state'
        elif feature == 'pos':
            sub = g
            col = 'part_of_speech'
        elif feature == 'verb_tense':
            sub = g[g['part_of_speech'] == 'Verb'].copy()
            sub['_norm'] = sub['tense'].map(_TENSE_NORM).fillna(sub['tense'])
            col = '_norm'
        elif feature == 'verb_voice':
            sub = g[g['part_of_speech'] == 'Verb'].copy()
            sub['_norm'] = sub['voice'].map(_VOICE_NORM).fillna(sub['voice'])
            col = '_norm'
        elif feature == 'verb_mood':
            sub = g[g['part_of_speech'] == 'Verb']
            col = 'mood'
        else:
            raise ValueError(f"Unknown feature: {feature!r}")

        total = len(sub)
        counts = sub[col].value_counts()
        row = {'genre': genre, 'total': total}
        for cat in order:
            row[cat] = int(counts.get(cat, 0))
        # Include any categories not in the order list
        for cat, cnt in counts.items():
            if cat not in row:
                row[cat] = int(cnt)
        rows.append(row)

    result = pd.DataFrame(rows).set_index('genre')
    # Keep only ordered categories (drop noise / empty)
    keep_cols = [c for c in order if c in result.columns]
    result = result[['total'] + keep_cols]

    if normalize:
        for col in keep_cols:
            result[col] = (result[col] / result['total'] * 100).round(1)

    return result


# ── Terminal output ───────────────────────────────────────────────────────────

def print_genre_compare(
    corpus: str = 'OT',
    feature: str = 'verb_stem',
) -> None:
    """Print a formatted genre comparison table to stdout."""

    FEATURE_LABELS = {
        'verb_stem':        'Hebrew Verb Stem Distribution by Genre',
        'verb_conjugation': 'Hebrew Verb Conjugation Distribution by Genre',
        'pos':              'Part-of-Speech Distribution by Genre',
        'noun_state':       'Hebrew Noun State Distribution by Genre',
        'verb_tense':       'Greek Verb Tense Distribution by Genre',
        'verb_voice':       'Greek Verb Voice Distribution by Genre',
        'verb_mood':        'Greek Verb Mood Distribution by Genre',
    }
    corpus_label = 'Old Testament' if corpus == 'OT' else 'New Testament'
    title = FEATURE_LABELS.get(feature, f'{feature} by Genre')

    df_pct = genre_compare(corpus, feature, normalize=True)
    df_cnt = genre_compare(corpus, feature, normalize=False)
    cats = [c for c in df_pct.columns if c != 'total']

    w = 70
    print(f"\n{'═'*w}")
    print(f"  {title}")
    print(f"  {corpus_label}")
    print(f"{'═'*w}\n")

    # Header
    col_w = max(16, max(len(c) for c in cats) + 2)
    header = f"  {'Genre':<14} {'Tokens':>8}  "
    header += "".join(f"{c[:col_w-1]:<{col_w}}" for c in cats)
    print(header)
    print(f"  {'-'*13} {'-'*8}  " + "".join(f"{'-'*(col_w-1)} " for _ in cats))

    for genre in df_pct.index:
        total = int(df_cnt.loc[genre, 'total'])
        line = f"  {genre:<14} {total:>8,}  "
        for cat in cats:
            pct = df_pct.loc[genre, cat]
            bar = '█' * min(int(pct / 5), 12)
            line += f"{pct:>4.1f}%  {bar:<12} "
        print(line.rstrip())
    print()


# ── Heatmap chart ─────────────────────────────────────────────────────────────

def genre_heatmap(
    corpus: str = 'OT',
    feature: str = 'verb_stem',
    *,
    output_path: str | None = None,
    pct: bool = True,
    figsize: tuple | None = None,
    title: str | None = None,
) -> str:
    """
    Produce and save a heatmap: rows=genres, cols=feature categories.

    Returns the path to the saved PNG.
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    df = genre_compare(corpus, feature, normalize=pct)
    cats = [c for c in df.columns if c != 'total']
    matrix = df[cats].values.astype(float)

    TITLES = {
        ('OT', 'verb_stem'):        'Hebrew Verb Stem Distribution by Genre',
        ('OT', 'verb_conjugation'): 'Hebrew Verb Conjugation Distribution by Genre',
        ('OT', 'pos'):              'OT Part-of-Speech Distribution by Genre',
        ('OT', 'noun_state'):       'Hebrew Noun State (Absolute / Construct) by Genre',
        ('NT', 'verb_tense'):       'Greek Verb Tense Distribution by Genre',
        ('NT', 'verb_voice'):       'Greek Verb Voice Distribution by Genre',
        ('NT', 'verb_mood'):        'Greek Verb Mood Distribution by Genre',
        ('NT', 'pos'):              'NT Part-of-Speech Distribution by Genre',
    }

    chart_title = title or TITLES.get((corpus, feature), f'{corpus} {feature} by Genre')
    value_fmt = '{:.1f}%' if pct else '{:,.0f}'

    if output_path is None:
        out_dir = Path('output') / 'charts' / 'both' / 'genre'
        out_dir.mkdir(parents=True, exist_ok=True)
        output_path = str(out_dir / f"{corpus.lower()}-genre-{feature.replace('_', '-')}.png")

    n_genres, n_cats = matrix.shape
    fw = max(10, n_cats * 1.6)
    fh = max(4,  n_genres * 1.2)
    if figsize:
        fw, fh = figsize

    fig, ax = plt.subplots(figsize=(fw, fh))
    # Row-normalize for colour intensity so rare categories still show contrast
    row_max = matrix.max(axis=1, keepdims=True)
    row_max[row_max == 0] = 1
    norm_matrix = matrix / row_max

    im = ax.imshow(norm_matrix, cmap='YlOrRd', aspect='auto', vmin=0, vmax=1)

    ax.set_xticks(range(n_cats))
    ax.set_xticklabels(cats, rotation=35, ha='right', fontsize=9)
    ax.set_yticks(range(n_genres))
    row_labels = [f"{g}  (n={int(df.loc[g, 'total']):,})" for g in df.index]
    ax.set_yticklabels(row_labels, fontsize=9)

    # Annotate cells
    for i in range(n_genres):
        for j in range(n_cats):
            val = matrix[i, j]
            color = 'white' if norm_matrix[i, j] > 0.65 else 'black'
            ax.text(j, i, value_fmt.format(val),
                    ha='center', va='center', fontsize=8, color=color, fontweight='bold')

    ax.set_title(chart_title, fontsize=11, fontweight='bold', pad=12)
    plt.colorbar(im, ax=ax, label='Relative intensity (row-normalised)', shrink=0.8)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    return output_path


# ── Full Markdown report ──────────────────────────────────────────────────────

def genre_report(
    output_dir: str = 'output/reports/both/genre',
    *,
    ot_features: list[str] | None = None,
    nt_features: list[str] | None = None,
) -> str:
    """
    Generate a comprehensive Markdown genre comparison report.

    Returns path to the saved Markdown file.
    """
    from pathlib import Path

    if ot_features is None:
        ot_features = ['verb_stem', 'verb_conjugation', 'pos']
    if nt_features is None:
        nt_features = ['verb_tense', 'verb_voice', 'verb_mood', 'pos']

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / 'genre-comparison-report.md'

    FEATURE_TITLES = {
        'verb_stem':        'Verb Stem Distribution',
        'verb_conjugation': 'Verb Conjugation Distribution',
        'pos':              'Part-of-Speech Distribution',
        'noun_state':       'Noun State (Absolute / Construct)',
        'verb_tense':       'Verb Tense Distribution',
        'verb_voice':       'Verb Voice Distribution',
        'verb_mood':        'Verb Mood Distribution',
    }
    FEATURE_NOTES = {
        'verb_stem': (
            "Hebrew verb stems (binyanim) encode voice and degree of action intensity. "
            "Qal is the simple active stem; Piel intensifies or factitives; "
            "Hiphil makes causative; Niphal is passive/reflexive."
        ),
        'verb_conjugation': (
            "Consecutive Perfect (wayyiqtol) drives OT narrative prose. "
            "Imperfect and Participle dominate poetry and prophecy, "
            "reflecting ongoing or vivid-present discourse."
        ),
        'pos': (
            "The ratio of verbs to nouns shifts across genres: "
            "narrative prose is verb-heavy (action), poetry and law are noun-heavy (description)."
        ),
        'noun_state': (
            "Construct state (smichut) marks genitive relationships. "
            "Higher construct ratios indicate denser noun chains — "
            "characteristic of legal and priestly literature."
        ),
        'verb_tense': (
            "Aorist (punctiliar past) dominates narrative sections; "
            "Present dominates epistolary and didactic writing. "
            "Perfect (R-form) marks completed action with ongoing relevance."
        ),
        'verb_voice': (
            "Passive constructions increase in epistolary literature, "
            "reflecting theological passives (divine action without naming God). "
            "Deponent verbs are grammatically active but semantically middle."
        ),
        'verb_mood': (
            "Participles are proportionally highest in Revelation and General letters, "
            "reflecting their dense predicative and attributive use. "
            "Subjunctive marks contingency and hortatory purpose clauses."
        ),
    }

    lines = [
        "# Genre Comparison: Morphological Patterns Across Literary Sections",
        "",
        "Analysis of how grammatical features distribute differently across "
        "the literary genres of the Hebrew OT and Greek NT, using STEPBible "
        "TAHOT/TAGNT morphological data.",
        "",
        "Values shown as percentage of the relevant token class within each genre.",
        "",
    ]

    # ── OT ────────────────────────────────────────────────────────────────────
    lines += ["---", "", "## Old Testament Hebrew", ""]

    ot_genre_tokens = {}
    for genre, books in OT_GENRES.items():
        df_all = _load_ot()
        ot_genre_tokens[genre] = int(df_all[df_all['book_id'].isin(books)].shape[0])

    lines += [
        "### Token Counts by Genre",
        "",
        "| Genre | Books | Total Tokens |",
        "|---|---:|---:|",
    ]
    for genre, books in OT_GENRES.items():
        lines.append(f"| {genre} | {len(books)} | {ot_genre_tokens[genre]:,} |")
    lines.append("")

    for feature in ot_features:
        chart_path = genre_heatmap('OT', feature,
                                   output_path=str(out_dir / f'ot-genre-{feature.replace("_", "-")}.png'))  # noqa: E501
        df_pct = genre_compare('OT', feature, normalize=True)
        df_cnt = genre_compare('OT', feature, normalize=False)
        cats = [c for c in df_pct.columns if c != 'total']

        title = FEATURE_TITLES.get(feature, feature)
        note = FEATURE_NOTES.get(feature, '')
        lines += [f"### {title}", ""]
        if note:
            lines += [f"_{note}_", ""]

        lines += [f"![OT {title}]({Path(chart_path).name})", ""]

        # Table: rows=genres, cols=categories
        lines += [
            "| Genre | Tokens | " + " | ".join(cats) + " |",
            "|---|---:|" + "|".join(["---:" for _ in cats]) + "|",
        ]
        for genre in df_pct.index:
            total = int(df_cnt.loc[genre, 'total'])
            vals = " | ".join(f"{df_pct.loc[genre, c]:.1f}%" for c in cats)
            lines.append(f"| {genre} | {total:,} | {vals} |")
        lines.append("")

    # ── NT ────────────────────────────────────────────────────────────────────
    lines += ["---", "", "## New Testament Greek", ""]

    nt_genre_tokens = {}
    for genre, books in NT_GENRES.items():
        df_all = _load_nt()
        nt_genre_tokens[genre] = int(df_all[df_all['book_id'].isin(books)].shape[0])

    lines += [
        "### Token Counts by Genre",
        "",
        "| Genre | Books | Total Tokens |",
        "|---|---:|---:|",
    ]
    for genre, books in NT_GENRES.items():
        lines.append(f"| {genre} | {len(books)} | {nt_genre_tokens[genre]:,} |")
    lines.append("")

    for feature in nt_features:
        chart_path = genre_heatmap('NT', feature,
                                   output_path=str(out_dir / f'nt-genre-{feature.replace("_", "-")}.png'))  # noqa: E501
        df_pct = genre_compare('NT', feature, normalize=True)
        df_cnt = genre_compare('NT', feature, normalize=False)
        cats = [c for c in df_pct.columns if c != 'total']

        title = FEATURE_TITLES.get(feature, feature)
        note = FEATURE_NOTES.get(feature, '')
        lines += [f"### {title}", ""]
        if note:
            lines += [f"_{note}_", ""]

        lines += [f"![NT {title}]({Path(chart_path).name})", ""]

        lines += [
            "| Genre | Tokens | " + " | ".join(cats) + " |",
            "|---|---:|" + "|".join(["---:" for _ in cats]) + "|",
        ]
        for genre in df_pct.index:
            total = int(df_cnt.loc[genre, 'total'])
            vals = " | ".join(f"{df_pct.loc[genre, c]:.1f}%" for c in cats)
            lines.append(f"| {genre} | {total:,} | {vals} |")
        lines.append("")

    lines += [
        "---",
        "",
        "_Source: STEPBible TAHOT/TAGNT (CC BY 4.0, Tyndale House Cambridge). "
        "Values are percentages of the relevant token class within each genre._",
    ]

    md_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"  Saved: {md_path}")
    return str(md_path)
