"""
LXX translation consistency: how uniformly does each LXX book/translator
render a given Hebrew root?

Uses IBM Model 1 word-level alignment to measure:
  - Overall consistency score (0–100): percentage of aligned tokens that
    use the most common LXX rendering for that book
  - Per-book rendering profile: which Greek lemma(s) each book uses and
    how often
  - Cross-book divergences: books whose primary rendering differs from the
    corpus-wide primary

High consistency (>90%) = the LXX translator treated this word uniformly.
Low consistency or cross-book divergence may indicate:
  - Different translation philosophy between books
  - Semantic range of the Hebrew root not captured by one Greek word
  - Textual / recensional differences between LXX traditions

Usage
-----
from bible_grammar.intertextuality.lxx_consistency import (
    lxx_consistency, print_lxx_consistency, consistency_heatmap
)

# Single root
lxx_consistency('H7307')   # רוּחַ spirit/wind

# Print formatted report
print_lxx_consistency('H7307')

# Multiple roots
print_lxx_consistency('H2617')  # חֶסֶד lovingkindness

# Heatmap of rendering choices across books
consistency_heatmap('H7307', output_path='output/charts/ruach-lxx-consistency.png')
"""

from __future__ import annotations
import re
import pandas as pd
from pathlib import Path
from ..core.reference import BOOKS

_BOOK_ORDER = {b[0]: b[3] for b in BOOKS}
_BOOK_NAME = {b[0]: b[1] for b in BOOKS}


def _norm_root(strongs: str) -> str:
    """Strip variant letter and leading zeros: H0001G → H1, H1697I → H1697."""
    m = re.match(r'^([HG])0*(\d+)[A-Z]?$', strongs.strip().upper())
    return f"{m.group(1)}{m.group(2)}" if m else strongs.strip().upper()


def lxx_consistency(
    heb_strongs: str,
    *,
    min_count: int = 3,
    min_book_count: int = 2,
) -> dict:
    """
    Measure per-book LXX translation consistency for a Hebrew root.

    Parameters
    ----------
    heb_strongs    : Hebrew Strong's number, e.g. 'H7307', 'H1697'
    min_count      : Minimum total aligned tokens in a book to include it
    min_book_count : Minimum books required for a meaningful analysis

    Returns a dict:
      strongs          : normalised strongs
      lemma            : Hebrew lemma (from lexicon)
      gloss            : English gloss
      total_aligned    : total word-level alignment tokens
      corpus_primary   : most common LXX lemma across all books
      corpus_primary_pct: percentage using corpus_primary
      overall_consistency: weighted average consistency across books
      books            : list of per-book dicts (sorted by book order):
        {
          book_id, book_name,
          total,           # aligned tokens in this book
          primary_lemma,   # most-used LXX lemma in this book
          primary_pct,     # % using primary_lemma
          consistency,     # same as primary_pct (0–100)
          diverges,        # True if primary_lemma != corpus_primary
          rendering_profile: dict {lxx_lemma: count}
        }
      divergent_books  : list of book_ids where primary != corpus_primary
    """
    from ..core.ibm_align import load_word_alignment
    from ..lexical.wordstudy import _lookup_lex

    df = load_word_alignment()
    lex = _lookup_lex(heb_strongs) or {}

    # Filter to this root (strip variant letters for root matching)
    target_root = _norm_root(heb_strongs)
    mask = df['heb_strongs'].apply(lambda s: _norm_root(str(s)) == target_root)
    hits = df[mask]

    if hits.empty:
        return {
            'strongs': heb_strongs, 'lemma': lex.get('lemma', ''),
            'gloss': lex.get('gloss', ''), 'total_aligned': 0,
            'corpus_primary': '', 'corpus_primary_pct': 0.0,
            'overall_consistency': 0.0, 'books': [], 'divergent_books': [],
        }

    # Corpus-wide primary rendering
    corpus_counts = hits['lxx_lemma'].value_counts()
    corpus_primary = corpus_counts.index[0]
    corpus_primary_pct = round(corpus_counts.iloc[0] / len(hits) * 100, 1)

    # Per-book analysis
    books_out = []
    for book_id, grp in hits.groupby('book_id'):
        if len(grp) < min_count:
            continue
        book_counts = grp['lxx_lemma'].value_counts()
        primary_lemma = book_counts.index[0]
        primary_pct = round(book_counts.iloc[0] / len(grp) * 100, 1)
        profile = book_counts.to_dict()
        books_out.append({
            'book_id':          book_id,
            'book_name':        _BOOK_NAME.get(book_id, book_id),
            'total':            len(grp),
            'primary_lemma':    primary_lemma,
            'primary_pct':      primary_pct,
            'consistency':      primary_pct,
            'diverges':         primary_lemma != corpus_primary,
            'rendering_profile': profile,
        })

    if len(books_out) < min_book_count:
        books_out = []

    # Sort by canonical book order
    books_out.sort(key=lambda b: _BOOK_ORDER.get(b['book_id'], 999))

    # Weighted average consistency
    if books_out:
        total_w = sum(b['total'] for b in books_out)
        overall = round(
            sum(b['consistency'] * b['total'] for b in books_out) / total_w, 1
        ) if total_w else 0.0
    else:
        overall = 0.0

    divergent = [b['book_id'] for b in books_out if b['diverges']]

    return {
        'strongs':             heb_strongs,
        'lemma':               lex.get('lemma', ''),
        'gloss':               lex.get('gloss', ''),
        'total_aligned':       len(hits),
        'corpus_primary':      corpus_primary,
        'corpus_primary_pct':  corpus_primary_pct,
        'overall_consistency': overall,
        'books':               books_out,
        'divergent_books':     divergent,
    }


def print_lxx_consistency(heb_strongs: str, *, min_count: int = 3) -> None:
    """Print a formatted LXX translation consistency report."""
    result = lxx_consistency(heb_strongs, min_count=min_count)

    print(f"\n{'═'*70}")
    print(f"  LXX Translation Consistency: {result['strongs']}")
    if result['lemma']:
        print(f"  Hebrew: {result['lemma']}  ({result['gloss']})")
    print(f"{'═'*70}\n")

    if result['total_aligned'] == 0:
        print("  No word-level alignment data found.\n")
        return

    print(f"  Total aligned tokens : {result['total_aligned']:,}")
    print(f"  Corpus-wide primary  : {result['corpus_primary']}  "
          f"({result['corpus_primary_pct']:.0f}%)")
    print(f"  Overall consistency  : {result['overall_consistency']:.0f}%")
    if result['divergent_books']:
        print(f"  Divergent books      : {', '.join(result['divergent_books'])}")
    print()

    if not result['books']:
        print("  Insufficient per-book data.\n")
        return

    # Column header
    print(f"  {'Book':<20} {'Tokens':>6}  {'Primary rendering':<18} {'Pct':>5}  {'Alt renderings'}")
    print(f"  {'-'*19} {'-'*6}  {'-'*17} {'-'*5}  {'-'*30}")

    for b in result['books']:
        # Build alt renderings string (exclude primary)
        alts = {k: v for k, v in b['rendering_profile'].items()
                if k != b['primary_lemma']}
        alt_str = '  '.join(
            f"{lemma}×{cnt}" for lemma, cnt in
            sorted(alts.items(), key=lambda x: -x[1])
        )[:35] if alts else ''

        diverge_mark = ' ←' if b['diverges'] else ''
        bar = '█' * min(int(b['consistency'] / 10), 10)
        print(f"  {b['book_name']:<20} {b['total']:>6}  "
              f"{b['primary_lemma']:<18} {b['consistency']:>5.0f}%  "
              f"{bar}  {alt_str}{diverge_mark}")

    if result['divergent_books']:
        print(f"\n  ← primary rendering differs from corpus-wide primary "
              f"({result['corpus_primary']})")
    print()


def consistency_heatmap(
    roots: str | list[str],
    *,
    min_count: int = 3,
    output_path: str | None = None,
    title: str | None = None,
) -> None:
    """
    Generate a heatmap of LXX rendering choices across books for one or more
    Hebrew roots.

    Rows = LXX lemmas, Columns = OT books, Cell value = % of tokens in that
    book using that rendering. Books/lemmas with no data are blank.

    Parameters
    ----------
    roots       : Single strongs string or list
    min_count   : Minimum tokens per book to include
    output_path : Save to PNG if provided; otherwise display inline
    title       : Chart title (auto-generated if None)
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from ..core.ibm_align import load_word_alignment

    if isinstance(roots, str):
        roots = [roots]

    df = load_word_alignment()

    # Collect all data
    all_rows = []
    root_labels = []
    for strongs in roots:
        target = _norm_root(strongs)
        hits = df[df['heb_strongs'].apply(lambda s: _norm_root(str(s)) == target)]
        if hits.empty:
            continue
        from ..lexical.wordstudy import _lookup_lex
        lex = _lookup_lex(strongs) or {}
        label = f"{lex.get('lemma', '')}\n({strongs})" if lex.get('lemma') else strongs
        root_labels.append(label)
        all_rows.append(hits)

    if not all_rows:
        print("No alignment data found.")
        return

    combined = pd.concat(all_rows)

    # Build pivot: lxx_lemma × book_id = pct
    book_totals = combined.groupby('book_id').size()
    valid_books = book_totals[book_totals >= min_count].index
    filtered = combined[combined['book_id'].isin(valid_books)]

    pivot = (filtered.groupby(['lxx_lemma', 'book_id'])
             .size()
             .unstack(fill_value=0))

    # Normalise to percentage per book
    pivot_pct = pivot.div(pivot.sum(axis=0), axis=1) * 100

    # Sort books by canonical order, lemmas by frequency
    book_cols = sorted(pivot_pct.columns,
                       key=lambda b: _BOOK_ORDER.get(b, 999))
    lemma_rows = pivot_pct.sum(axis=1).sort_values(ascending=False).index
    pivot_pct = pivot_pct.loc[lemma_rows, book_cols]

    # Replace book_id with short name
    pivot_pct.columns = [_BOOK_NAME.get(b, b) for b in book_cols]

    # Draw heatmap
    fig_w = max(10, len(pivot_pct.columns) * 0.55)
    fig_h = max(3,  len(pivot_pct.index) * 0.55 + 1.5)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    im = ax.imshow(pivot_pct.values, cmap='YlOrRd', vmin=0, vmax=100, aspect='auto')

    ax.set_xticks(range(len(pivot_pct.columns)))
    ax.set_xticklabels(pivot_pct.columns, rotation=45, ha='right', fontsize=8)
    ax.set_yticks(range(len(pivot_pct.index)))
    ax.set_yticklabels(pivot_pct.index, fontsize=9)

    # Annotate cells with percentage (only non-zero)
    for i, row in enumerate(pivot_pct.index):
        for j, col in enumerate(pivot_pct.columns):
            val = pivot_pct.loc[row, col]
            if val > 0:
                color = 'white' if val > 60 else 'black'
                ax.text(j, i, f"{val:.0f}%", ha='center', va='center',
                        fontsize=7, color=color)

    plt.colorbar(im, ax=ax, label='% of tokens', shrink=0.6)

    if title is None:
        strongs_str = ', '.join(roots)
        title = f"LXX Translation Consistency: {strongs_str}"
    ax.set_title(title, fontsize=11, pad=12)
    ax.set_xlabel('OT Book', fontsize=9)
    ax.set_ylabel('LXX Rendering', fontsize=9)

    plt.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"  Saved: {output_path}")
    else:
        plt.savefig('/tmp/consistency_heatmap.png', dpi=150, bbox_inches='tight')
        print("  Chart saved to /tmp/consistency_heatmap.png")

    plt.close()


def batch_consistency(
    roots: list[str],
    *,
    min_count: int = 3,
) -> pd.DataFrame:
    """
    Run lxx_consistency() for multiple roots; return a summary DataFrame.

    Columns: strongs, lemma, gloss, total_aligned, corpus_primary,
             corpus_primary_pct, overall_consistency, n_divergent_books
    """
    rows = []
    for r in roots:
        result = lxx_consistency(r, min_count=min_count)
        rows.append({
            'strongs':              result['strongs'],
            'lemma':                result['lemma'],
            'gloss':                result['gloss'],
            'total_aligned':        result['total_aligned'],
            'corpus_primary':       result['corpus_primary'],
            'corpus_primary_pct':   result['corpus_primary_pct'],
            'overall_consistency':  result['overall_consistency'],
            'n_divergent_books':    len(result['divergent_books']),
        })
    return pd.DataFrame(rows).sort_values('overall_consistency', ascending=False)
