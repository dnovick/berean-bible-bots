"""
Morphological distribution charts: visualise how a root's grammatical forms
distribute across books.

For Hebrew verbs: stem × conjugation breakdown per book (stacked bar).
For Greek verbs:  tense × voice per book (stacked bar).
For Greek nouns:  case distribution per book (stacked bar).

Usage
-----
from bible_grammar.lexical.morph_chart import morph_distribution, morph_chart

# Hebrew verb — stem breakdown across books
morph_distribution('H1696')          # דָבַר to speak
morph_chart('H1696', output_path='output/charts/dabar-stems.png')

# Greek verb — tense × voice across books
morph_distribution('G3004')          # λέγω to say
morph_chart('G3004', output_path='output/charts/lego-tense.png')

# Greek noun — case distribution
morph_distribution('G3056')          # λόγος word
morph_chart('G3056', output_path='output/charts/logos-case.png')
"""

from __future__ import annotations
import re
import pandas as pd
from pathlib import Path
from ..core.reference import BOOKS

_BOOK_ORDER = {b[0]: b[3] for b in BOOKS}
_BOOK_NAME = {b[0]: b[1] for b in BOOKS}

# Canonical sort orders for display
_STEM_ORDER = ['Qal', 'Niphal', 'Piel', 'Pual', 'Hithpael',
               'Hiphil', 'Hophal', 'Hithpolel', 'Polel', 'Polal']
_CONJ_ORDER = ['Perfect', 'Consecutive Perfect', 'Imperfect',
               'Consecutive Imperfect', 'Jussive', 'Imperative',
               'Infinitive construct', 'Infinitive absolute', 'Participle',
               'Participle passive']
_TENSE_ORDER = ['Present', 'Imperfect', 'Future', 'Aorist', 'Perfect',
                'Pluperfect', 'Second Aorist', 'Second Perfect']
_VOICE_ORDER = ['Active', 'Middle', 'Passive', 'Middle/Passive']
_CASE_ORDER = ['Nominative', 'Vocative', 'Accusative', 'Genitive', 'Dative']


def _norm_strongs(s: str) -> str:
    m = re.match(r'^([HG])0*(\d+)[A-Z]?$', str(s).strip().upper())
    return f"{m.group(1)}{m.group(2)}" if m else str(s).strip().upper()


def _get_hits(strongs: str) -> tuple[pd.DataFrame, bool]:
    """Return filtered DataFrame for this strongs and whether it is Hebrew."""
    from ..core import db as _db
    df_all = _db.load()
    clean = strongs.strip("{}").upper()
    is_hebrew = clean.startswith("H")
    source = "TAHOT" if is_hebrew else "TAGNT"
    corpus = df_all[df_all["source"] == source]

    m = re.match(r'^([HG])0*(\d+)([A-Z]?)$', clean)
    if m:
        pfx, num, suf = m.groups()
        pat = (rf'\{{{pfx}0*{num}[A-Z]?\}}' if is_hebrew
               else rf'\b{pfx}0*{num}[A-Z]?\b')
    else:
        pat = re.escape(clean)

    hits = corpus[corpus["strongs"].str.upper().str.contains(pat, regex=True, na=False)].copy()
    return hits, is_hebrew


def morph_distribution(strongs: str, *, min_book_count: int = 3) -> dict:
    """
    Compute per-book morphological distribution for a root.

    Returns a dict:
      strongs, lemma, gloss, is_hebrew, pos, dim1, dim2,
      pivot   : DataFrame (rows=books, cols=morph categories, values=count)
      pivot_pct: same but normalised to 100% per book
    """
    from .wordstudy import _lookup_lex

    hits, is_hebrew = _get_hits(strongs)
    lex = _lookup_lex(strongs) or {}

    if hits.empty:
        return {'strongs': strongs, 'lemma': '', 'gloss': '', 'pivot': pd.DataFrame()}

    pos_vals = hits['part_of_speech'].dropna().unique().tolist()
    pos = pos_vals[0] if pos_vals else ''

    # Choose dimensions based on language and POS
    if is_hebrew:
        if 'Verb' in pos_vals:
            hits = hits[hits['part_of_speech'] == 'Verb']
            dim1, dim2 = 'stem', 'conjugation'
            # Combined label: "Piel Perfect"
            hits = hits.copy()
            hits['_cat'] = (hits['stem'].fillna('').str.strip() + ' '
                            + hits['conjugation'].fillna('').str.strip()).str.strip()
        else:
            dim1, dim2 = 'state', 'part_of_speech'
            hits = hits.copy()
            hits['_cat'] = hits['part_of_speech'].fillna('').str.strip()
    else:
        if any('Verb' in str(p) for p in pos_vals):
            hits = hits[hits['part_of_speech'].str.contains('Verb', na=False)]
            hits = hits.copy()
            hits['_cat'] = (hits['tense'].fillna('').str.strip() + ' '
                            + hits['voice'].fillna('').str.strip()).str.strip()
            dim1, dim2 = 'tense', 'voice'
        elif any('Noun' in str(p) for p in pos_vals):
            hits = hits.copy()
            hits['_cat'] = hits['case_'].fillna('').str.strip()
            dim1, dim2 = 'case_', ''
        else:
            hits = hits.copy()
            hits['_cat'] = hits['part_of_speech'].fillna('').str.strip()
            dim1, dim2 = 'part_of_speech', ''

    # Remove empty categories
    hits = hits[hits['_cat'].str.len() > 0]

    # Filter books with enough tokens
    book_counts = hits.groupby('book_id').size()
    valid_books = book_counts[book_counts >= min_book_count].index
    hits = hits[hits['book_id'].isin(valid_books)]

    if hits.empty:
        return {'strongs': strongs, 'lemma': lex.get('lemma', ''),
                'gloss': lex.get('gloss', ''), 'pivot': pd.DataFrame()}

    # Build pivot
    pivot = (hits.groupby(['book_id', '_cat'])
             .size()
             .unstack(fill_value=0))

    # Sort books by canonical order
    pivot = pivot.loc[sorted(pivot.index, key=lambda b: _BOOK_ORDER.get(b, 999))]
    pivot.index = [_BOOK_NAME.get(b, b) for b in pivot.index]

    # Sort columns by canonical form order
    if is_hebrew and 'Verb' in pos_vals:
        def _stem_conj_key(c: str) -> tuple[int, int]:
            parts = c.split(' ', 1)
            stem = parts[0] if parts else ''
            conj = parts[1] if len(parts) > 1 else ''
            return (_STEM_ORDER.index(stem) if stem in _STEM_ORDER else 99,
                    _CONJ_ORDER.index(conj) if conj in _CONJ_ORDER else 99)
        cols = sorted(pivot.columns, key=_stem_conj_key)
    elif not is_hebrew and dim1 == 'case_':
        cols = [c for c in _CASE_ORDER if c in pivot.columns]
        cols += [c for c in pivot.columns if c not in cols]
    else:
        cols = pivot.columns.tolist()
    pivot = pivot[cols]

    # Percentage pivot
    row_totals = pivot.sum(axis=1)
    pivot_pct = pivot.div(row_totals, axis=0) * 100

    return {
        'strongs':    strongs,
        'lemma':      lex.get('lemma', ''),
        'gloss':      lex.get('gloss', ''),
        'is_hebrew':  is_hebrew,
        'pos':        pos,
        'dim1':       dim1,
        'dim2':       dim2,
        'pivot':      pivot,
        'pivot_pct':  pivot_pct,
    }


def print_morph_distribution(strongs: str, *, min_book_count: int = 3) -> None:
    """Print a formatted morphological distribution table."""
    result = morph_distribution(strongs, min_book_count=min_book_count)
    pivot = result.get('pivot')

    print(f"\n{'═'*70}")
    print(f"  Morphological Distribution: {result['strongs']}", end='')
    if result.get('lemma'):
        print(f"  —  {result['lemma']}  ({result['gloss']})", end='')
    print(f"\n{'═'*70}\n")

    if pivot is None or pivot.empty:
        print("  No data found.\n")
        return

    pivot_pct = result['pivot_pct']
    cols = pivot.columns.tolist()
    col_w = max(12, max(len(c) for c in cols) + 2)

    # Header
    header = f"  {'Book':<22}"
    for c in cols:
        header += f"  {c[:col_w-1]:>{col_w}}"
    print(header)
    print(f"  {'-'*22}" + f"  {'-'*(col_w)}" * len(cols))

    for book in pivot.index:
        row = f"  {book:<22}"
        total = pivot.loc[book].sum()
        for c in cols:
            cnt = pivot.loc[book, c]
            pct = pivot_pct.loc[book, c]
            if cnt > 0:
                row += f"  {cnt:>{col_w-5}d} {pct:>4.0f}%"
            else:
                row += f"  {'':>{col_w}}"
        row += f"   [{int(total)}]"
        print(row)
    print()


def morph_chart(
    strongs: str,
    *,
    chart_type: str = 'stacked_bar',
    min_book_count: int = 3,
    output_path: str | None = None,
    title: str | None = None,
    pct: bool = True,
) -> None:
    """
    Generate a morphological distribution chart for a root.

    Parameters
    ----------
    strongs        : Hebrew or Greek Strong's number
    chart_type     : 'stacked_bar' (default) or 'heatmap'
    min_book_count : Minimum tokens per book to include
    output_path    : Save to PNG if provided; otherwise /tmp/
    title          : Chart title (auto-generated if None)
    pct            : If True, normalise to 100% per book (stacked_bar only)
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    result = morph_distribution(strongs, min_book_count=min_book_count)
    pivot = result.get('pivot')
    pivot_pct = result.get('pivot_pct')

    if pivot is None or pivot.empty:
        print("  No data to chart.")
        return

    if pct and pivot_pct is None:
        print("  No percentage data to chart.")
        return

    data = pivot_pct if pct else pivot
    assert data is not None
    cols = data.columns.tolist()
    books = data.index.tolist()

    if title is None:
        lang = "Hebrew" if result.get('is_hebrew') else "Greek"
        title = (f"{result['lemma']} ({result['strongs']})  —  "
                 f"{lang} Morphological Distribution")

    # Colour palette
    cmap = plt.cm.get_cmap('tab20', len(cols))
    colors = [cmap(i) for i in range(len(cols))]

    if chart_type == 'heatmap':
        fig_w = max(8, len(books) * 0.55)
        fig_h = max(3, len(cols) * 0.5 + 1.5)
        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        im = ax.imshow(data.values.T, cmap='YlOrRd', vmin=0,
                       vmax=100 if pct else data.values.max(), aspect='auto')
        ax.set_xticks(range(len(books)))
        ax.set_xticklabels(books, rotation=45, ha='right', fontsize=7)
        ax.set_yticks(range(len(cols)))
        ax.set_yticklabels(cols, fontsize=8)
        for i, book in enumerate(books):
            for j, col in enumerate(cols):
                val = data.loc[book, col]
                if val > 0:
                    text_color = 'white' if val > (
                        50 if pct else data.values.max()*0.6) else 'black'
                    label = f"{val:.0f}%" if pct else str(int(val))
                    ax.text(i, j, label, ha='center', va='center',
                            fontsize=6, color=text_color)
        plt.colorbar(im, ax=ax, label='%' if pct else 'count', shrink=0.6)
    else:
        # Stacked bar
        fig_w = max(10, len(books) * 0.5)
        fig_h = 6
        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        bottom = [0.0] * len(books)
        x = range(len(books))
        for i, col in enumerate(cols):
            vals = [data.loc[b, col] for b in books]
            bars = ax.bar(x, vals, bottom=bottom, label=col,
                          color=colors[i], width=0.7)
            # Annotate segments that are wide enough
            for rect, val, bot in zip(bars, vals, bottom):
                if val >= (5 if pct else 1):
                    ax.text(rect.get_x() + rect.get_width() / 2,
                            bot + val / 2,
                            f"{val:.0f}%" if pct else str(int(val)),
                            ha='center', va='center', fontsize=6, color='white',
                            fontweight='bold')
            bottom = [b + v for b, v in zip(bottom, vals)]

        ax.set_xticks(list(x))
        ax.set_xticklabels(books, rotation=45, ha='right', fontsize=8)
        ax.set_ylabel('% of tokens per book' if pct else 'Token count', fontsize=9)
        ax.set_ylim(0, 105 if pct else None)
        ax.legend(loc='upper right', fontsize=7, ncol=max(1, len(cols)//8),
                  bbox_to_anchor=(1.0, 1.0))

    ax.set_title(title, fontsize=11, pad=12)
    plt.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"  Saved: {output_path}")
    else:
        out = '/tmp/morph_chart.png'
        plt.savefig(out, dpi=150, bbox_inches='tight')
        print(f"  Chart saved to {out}")
    plt.close()
