"""
Collocation statistics: find words that co-occur with a target word
significantly more often than chance predicts.

Uses Pointwise Mutual Information (PMI) and log-likelihood ratio (G²) as
association measures. Words with high PMI appear near the target far more
often than their corpus frequency alone would predict.

Usage
-----
from bible_grammar.lexical.collocation import collocations, print_collocations

# What words appear near רוּחַ (spirit) in the OT?
print_collocations('H7307', window=5, corpus='OT')

# What words cluster around λόγος in the NT?
print_collocations('G3056', window=5, corpus='NT')

# Return raw DataFrame for notebook display
df = collocations('H7307', window=5, corpus='OT')
"""

from __future__ import annotations
import re
import math
import pandas as pd
from ..core import db as _db
from ..core.reference import BOOKS
from ..core._utils import norm_strongs as _norm_strongs

_BOOK_ORDER = {b[0]: b[3] for b in BOOKS}

# Strong's numbers that are function words / grammatical particles to exclude
# from collocation results (they co-occur with everything)
_STOP_PREFIXES = {'H9', 'H5', 'H1'}  # H9xxx = grammatical particles in TAHOT


def _extract_root(strongs_cell: str, is_hebrew: bool) -> str:
    """Extract the primary content strongs from a TAHOT strongs cell."""
    if not strongs_cell or pd.isna(strongs_cell):
        return ''
    s = str(strongs_cell)
    if is_hebrew:
        # Hebrew: find {H....} tokens, skip H9xxx grammatical particles
        braced = re.findall(r'\{([HG]\d+[A-Z]?)\}', s)
        for b in braced:
            if not re.match(r'H9\d+', b):
                return _norm_strongs(b)
        # fallback: bare token
        m = re.match(r'^([HG]\d+[A-Z]?)$', s.strip())
        return _norm_strongs(m.group(1)) if m else ''
    else:
        # Greek: plain strongs token
        m = re.match(r'^(G\d+[A-Z]?)\b', s.strip().upper())
        return _norm_strongs(m.group(1)) if m else _norm_strongs(s)


def _build_gpos(df: pd.DataFrame) -> pd.Series:
    """
    Assign a global sequential position index to each row, sorted by
    canonical book order → chapter → verse → word_num.
    """
    order = df['book_id'].map(_BOOK_ORDER).fillna(999)
    sort_key = (order * 1_000_000_000
                + df['chapter'] * 1_000_000
                + df['verse'] * 1_000
                + df['word_num'])
    return sort_key.rank(method='first').astype(int)


def collocations(
    target: str,
    *,
    window: int = 5,
    corpus: str = 'OT',
    book: str | None = None,
    book_group: str | None = None,
    min_count: int = 3,
    top_n: int = 30,
    exclude_particles: bool = True,
) -> pd.DataFrame:
    """
    Find words that significantly co-occur with a target Hebrew or Greek root.

    Parameters
    ----------
    target          : Strong's number, e.g. 'H7307', 'G3056'
    window          : Number of words either side to consider a co-occurrence
    corpus          : 'OT', 'NT', or 'LXX'
    book            : Restrict to a single book (e.g. 'Gen', 'Rom')
    book_group      : Restrict to a book group ('torah', 'pauline', etc.)
    min_count       : Minimum raw co-occurrence count to include a collocate
    top_n           : Return top N collocates by PMI
    exclude_particles: If True, skip Hebrew grammatical particles (H9xxx)

    Returns a DataFrame with columns:
      strongs, lemma, gloss, co_count, target_count, collocate_count,
      corpus_size, pmi, log_likelihood, expected
    Sorted by log_likelihood descending.
    """
    from .wordstudy import _lookup_lex

    source_map = {'OT': 'TAHOT', 'NT': 'TAGNT', 'LXX': 'TALXX'}
    source = source_map.get(corpus.upper(), 'TAHOT')
    is_hebrew = source == 'TAHOT'

    df_all = _db.load()
    df = df_all[df_all['source'] == source].copy()

    # Apply book / book_group filters
    if book:
        df = df[df['book_id'] == book]
    elif book_group:
        from ..core.reference import book_ids_for_group
        ids = book_ids_for_group(book_group)
        df = df[df['book_id'].isin(ids)]

    if df.empty:
        return pd.DataFrame()

    # Normalise target strongs
    target_norm = _norm_strongs(target)

    # Build root column
    df = df.copy()
    df['root'] = df['strongs'].apply(lambda s: _extract_root(s, is_hebrew))

    # Assign global position index
    df['_gpos'] = _build_gpos(df)
    df = df.sort_values('_gpos').reset_index(drop=True)

    # Find target positions
    target_mask = df['root'] == target_norm
    target_positions = df.index[target_mask].tolist()

    if not target_positions:
        return pd.DataFrame()

    N = len(df)                     # corpus size (tokens)
    f_target = len(target_positions)  # frequency of target

    # Collect all collocate tokens within window
    co_counts: dict[str, int] = {}
    for pos in target_positions:
        lo = max(0, pos - window)
        hi = min(N - 1, pos + window)
        window_roots = df.loc[lo:hi, 'root']
        for r in window_roots:
            if not r or r == target_norm:
                continue
            if exclude_particles and re.match(r'H9\d+', r):
                continue
            co_counts[r] = co_counts.get(r, 0) + 1

    if not co_counts:
        return pd.DataFrame()

    # Collocate frequencies in full corpus
    root_freq = df['root'].value_counts().to_dict()

    # Compute association measures
    rows = []
    for collocate, f_co in co_counts.items():
        if f_co < min_count:
            continue
        f_collocate = root_freq.get(collocate, 0)
        if f_collocate == 0:
            continue

        # Expected co-occurrence under independence
        # Using approximate: E = (f_target * f_collocate * window_size * 2) / N
        # More precisely: p(target) * p(collocate) * N_windows
        n_windows = f_target * window * 2
        expected = (f_collocate / N) * n_windows

        # PMI = log2( P(x,y) / (P(x)*P(y)) )
        # Observed joint prob ≈ f_co / N_windows
        p_co = f_co / max(n_windows, 1)
        p_col = f_collocate / N
        pmi = math.log2(p_co / p_col) if p_co > 0 and p_col > 0 else 0.0

        # Log-likelihood (G²) — more robust for rare words
        # G² = 2 * sum(O * ln(O/E))  over the 2×2 contingency table
        O11 = f_co
        O12 = f_target - f_co
        O21 = f_collocate - f_co
        O22 = N - f_target - f_collocate + f_co
        E11 = expected
        E12 = f_target - expected
        E21 = f_collocate - expected
        E22 = N - f_target - f_collocate + expected

        def _ll(o: float, e: float) -> float:
            return o * math.log(o / e) if o > 0 and e > 0 else 0.0

        g2 = 2 * (_ll(O11, E11) + _ll(O12, max(E12, 1e-10))
                  + _ll(O21, max(E21, 1e-10)) + _ll(O22, max(E22, 1e-10)))

        lex = _lookup_lex(collocate) or {}
        rows.append({
            'strongs':          collocate,
            'lemma':            lex.get('lemma', ''),
            'gloss':            lex.get('gloss', ''),
            'co_count':         f_co,
            'target_count':     f_target,
            'collocate_count':  f_collocate,
            'corpus_size':      N,
            'expected':         round(expected, 2),
            'pmi':              round(pmi, 2),
            'log_likelihood':   round(g2, 1),
        })

    if not rows:
        return pd.DataFrame()

    result = (pd.DataFrame(rows)
              .sort_values('log_likelihood', ascending=False)
              .head(top_n)
              .reset_index(drop=True))
    return result


def print_collocations(
    target: str,
    *,
    window: int = 5,
    corpus: str = 'OT',
    book: str | None = None,
    min_count: int = 3,
    top_n: int = 20,
) -> None:
    """Print a formatted collocation report for a target Hebrew/Greek root."""
    from .wordstudy import _lookup_lex

    lex = _lookup_lex(target) or {}
    label = f"{lex.get('lemma', '')}  ({target})" if lex.get('lemma') else target

    scope = book if book else corpus
    print(f"\n{'═'*70}")
    print(f"  Collocations: {label}")
    print(f"  Window: ±{window} words  |  Corpus: {scope}  |  Min count: {min_count}")
    print(f"{'═'*70}\n")

    df = collocations(target, window=window, corpus=corpus, book=book,
                      min_count=min_count, top_n=top_n)

    if df.empty:
        print("  No significant collocates found.\n")
        return

    target_count = df['target_count'].iloc[0]
    corpus_size = df['corpus_size'].iloc[0]
    print(f"  Target frequency : {target_count:,} / {corpus_size:,} tokens\n")

    print(f"  {'Strongs':<9} {'Lemma':<22} {'Gloss':<25} "
          f"{'Obs':>5} {'Exp':>6} {'PMI':>6}  {'G²':>8}")
    print(f"  {'-'*8} {'-'*21} {'-'*24} "
          f"{'-'*5} {'-'*6} {'-'*6}  {'-'*8}")

    for _, row in df.iterrows():
        bar = '█' * min(int(row['log_likelihood'] / 20), 12)
        print(f"  {row['strongs']:<9} {row['lemma']:<22} {str(row['gloss'])[:24]:<25} "
              f"{row['co_count']:>5} {row['expected']:>6.1f} {row['pmi']:>6.2f}  "
              f"{row['log_likelihood']:>8.1f}  {bar}")
    print()


def collocation_network(
    targets: str | list[str],
    *,
    window: int = 5,
    corpus: str = 'OT',
    min_count: int = 3,
    top_n: int = 15,
    output_path: str | None = None,
) -> None:
    """
    Generate a collocation network chart for one or more target roots.

    Rows = target roots, Cols = top collocates (by combined log-likelihood),
    Cells = observed co-occurrence count. Saved as PNG.
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from .wordstudy import _lookup_lex
    from pathlib import Path

    if isinstance(targets, str):
        targets = [targets]

    all_dfs = {}
    for t in targets:
        df = collocations(t, window=window, corpus=corpus, min_count=min_count,
                          top_n=top_n)
        if not df.empty:
            all_dfs[t] = df

    if not all_dfs:
        print("No collocation data found.")
        return

    # Union of all collocates
    all_collocates = []
    for df in all_dfs.values():
        all_collocates.extend(df['strongs'].tolist())
    # Rank by total log-likelihood across all targets
    col_ll: dict[str, float] = {}
    for df in all_dfs.values():
        for _, row in df.iterrows():
            col_ll[row['strongs']] = col_ll.get(row['strongs'], 0) + row['log_likelihood']
    top_cols = [k for k, _ in sorted(col_ll.items(), key=lambda x: -x[1])[:top_n]]

    # Build matrix: target × collocate → co_count
    matrix = {}
    for t, df in all_dfs.items():
        lex = _lookup_lex(t) or {}
        label = f"{lex.get('lemma', '')} ({t})" if lex.get('lemma') else t
        row_dict = dict(zip(df['strongs'], df['co_count']))
        matrix[label] = [row_dict.get(c, 0) for c in top_cols]

    col_labels = []
    for c in top_cols:
        lex = _lookup_lex(c) or {}
        col_labels.append(f"{lex.get('lemma', c)}\n({c})" if lex.get('lemma') else c)

    pivot = pd.DataFrame(matrix, index=col_labels).T

    fig_w = max(10, len(top_cols) * 0.7)
    fig_h = max(3, len(targets) * 0.6 + 1.5)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    im = ax.imshow(pivot.values, cmap='YlOrRd', aspect='auto')
    ax.set_xticks(range(len(col_labels)))
    ax.set_xticklabels(col_labels, rotation=45, ha='right', fontsize=7)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=9)

    for i in range(len(pivot.index)):
        for j in range(len(col_labels)):
            val = pivot.values[i, j]
            if val > 0:
                color = 'white' if val > pivot.values.max() * 0.6 else 'black'
                ax.text(j, i, str(int(val)), ha='center', va='center',
                        fontsize=7, color=color)

    plt.colorbar(im, ax=ax, label='co-occurrence count', shrink=0.6)
    ax.set_title(f"Collocation Network ({corpus}, window=±{window})", fontsize=11, pad=12)
    plt.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"  Saved: {output_path}")
    else:
        plt.savefig('/tmp/collocation_network.png', dpi=150, bbox_inches='tight')
        print("  Chart saved to /tmp/collocation_network.png")
    plt.close()
