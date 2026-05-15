"""
Cross-testament word trajectory: Hebrew OT → LXX → Greek NT.

For any Hebrew or Greek Strong's number, stitches together the full
lexical journey of a word across three corpora into a single pipeline
report and chart.

Questions this answers
──────────────────────
  • How does שָׁלוֹם (shalom) travel from Hebrew OT → LXX εἰρήνη → NT?
  • Is NT δικαιοσύνη (righteousness) using LXX vocabulary or fresh coinage?
  • How does the frequency and distribution of רוּחַ / πνεῦμα shift
    from OT to LXX to NT?
  • Which Greek NT authors use the most LXX-derived covenant vocabulary?

Pipeline stages
───────────────
  1. OT Hebrew   — word_study(): lemma, definition, total count, by-book,
                   morphological forms
  2. OT→LXX      — lxx_alignment(): which Greek words translate this Hebrew
                   root, with frequency and percentage
  3. LXX corpus  — lxx_by_book() / query_lxx(): how the LXX Greek word
                   is distributed across the Septuagint
  4. NT Greek    — TAGNT query: total count, by-book distribution
  5. Continuity  — compares LXX primary rendering with NT usage to assess
                   whether NT adopts LXX vocabulary (high continuity) or
                   diverges (new word choice)

Public API
──────────
word_trajectory(strongs, ...)          → dict with all pipeline stages
print_trajectory(strongs, ...)         → formatted terminal report
trajectory_chart(strongs, ...)         → 3-panel bar chart PNG
save_trajectory_report(strongs, ...)   → Markdown report + chart
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd


# ── Helpers ───────────────────────────────────────────────────────────────────

def _is_hebrew(strongs: str) -> bool:
    return strongs.upper().startswith('H')


def _nt_by_book(strongs: str) -> pd.DataFrame:
    """Per-book NT occurrence count from TAGNT Parquet (exact string match)."""
    df = pd.read_parquet('data/processed/words.parquet')
    nt = df[(df['source'] == 'TAGNT') & (df['strongs'] == strongs)]
    counts = nt.groupby('book_id').size().reset_index(name='count')
    return counts.sort_values('count', ascending=False).reset_index(drop=True)


def _nt_by_book_g(strongs_int: int) -> pd.DataFrame:
    """Per-book NT count for a Strong's number given as an int.

    Handles TAGNT's format quirks:
      - 4-digit zero-padded: 'G0040'
      - With variant suffix: 'G4151G', 'G4151H'
    Matches any row whose numeric Strong's prefix equals strongs_int.
    """
    import re as _re
    df = pd.read_parquet('data/processed/words.parquet')
    nt = df[df['source'] == 'TAGNT']
    # Extract numeric portion from strongs: 'G0040' → 40, 'G4151G' → 4151

    def _extract_num(s: str) -> int:
        if not s or not isinstance(s, str):
            return -1
        m = _re.match(r'[Gg](\d+)', s)
        return int(m.group(1)) if m else -1

    mask = nt['strongs'].map(_extract_num) == strongs_int
    counts = nt[mask].groupby('book_id').size().reset_index(name='count')
    return counts.sort_values('count', ascending=False).reset_index(drop=True)


_NT_BOOK_ORDER = [
    'Mat', 'Mrk', 'Luk', 'Jhn', 'Act',
    'Rom', '1Co', '2Co', 'Gal', 'Eph', 'Php', 'Col',
    '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm',
    'Heb', 'Jas', '1Pe', '2Pe', '1Jn', '2Jn', '3Jn', 'Jud', 'Rev',
]

_OT_BOOK_ORDER = [
    'Gen', 'Exo', 'Lev', 'Num', 'Deu', 'Jos', 'Jdg', 'Rut',
    '1Sa', '2Sa', '1Ki', '2Ki', '1Ch', '2Ch', 'Ezr', 'Neh',
    'Est', 'Job', 'Psa', 'Pro', 'Ecc', 'Sng', 'Isa', 'Jer',
    'Lam', 'Ezk', 'Dan', 'Hos', 'Jol', 'Amo', 'Oba', 'Jon',
    'Mic', 'Nah', 'Hab', 'Zep', 'Hag', 'Zec', 'Mal',
]


# ── Core pipeline ─────────────────────────────────────────────────────────────

def word_trajectory(
    strongs: str,
    *,
    top_lxx_forms: int = 3,
) -> dict:
    """
    Full cross-testament trajectory for a Hebrew or Greek Strong's number.

    Parameters
    ----------
    strongs       : Strong's number, e.g. 'H7965' or 'G1515'
    top_lxx_forms : how many LXX rendering forms to include

    Returns a dict with keys:
      strongs, lemma, translit, gloss, definition, is_hebrew,
      ot_total, ot_by_book,            # Hebrew/Aramaic OT (always present for H)
      morph_forms,                      # morphological breakdown
      lxx_primary, lxx_primary_g,       # top LXX Greek word + Strong's (for H words)
      lxx_alignment,                    # DataFrame: Greek renderings with %
      lxx_total, lxx_by_book,           # LXX corpus distribution
      lxx_consistency,                  # % of tokens using primary rendering
      nt_strongs, nt_lemma,             # NT counterpart Strong's and lemma
      nt_total, nt_by_book,             # NT distribution
      continuity,                       # 'high'|'medium'|'low'|'none'
      continuity_note,                  # plain-text explanation
    """
    from .wordstudy import word_study
    from ..core.syntax_ot import lxx_alignment as _lxx_align
    from ..core.lxx_query import lxx_by_book, query_lxx
    from ..intertextuality.lxx_consistency import lxx_consistency

    strongs = strongs.strip()
    is_heb = _is_hebrew(strongs)

    # ── Stage 1: lexicon + OT stats ───────────────────────────────────────────
    ws = word_study(strongs)

    result: dict = {
        'strongs':    strongs,
        'lemma':      ws.get('lemma', ''),
        'translit':   ws.get('translit', ''),
        'gloss':      ws.get('gloss', ''),
        'definition': ws.get('definition', ''),
        'is_hebrew':  is_heb,
        'ot_total':   ws.get('total_occurrences', 0) if is_heb else 0,
        'ot_by_book': ws.get('by_book', pd.DataFrame()) if is_heb else pd.DataFrame(),
        'morph_forms': ws.get('morphological_forms', pd.DataFrame()),
    }

    # ── Stage 2: Hebrew → LXX alignment ──────────────────────────────────────
    if is_heb:
        align_df = _lxx_align(strongs)
        result['lxx_alignment'] = align_df

        # Determine primary LXX Greek word
        if not align_df.empty:
            # Group by Strong's number to get total pct per lemma (rows are inflected forms)
            by_strongs = align_df.groupby('greek_g', as_index=False)['count'].sum()
            by_strongs = by_strongs.sort_values('count', ascending=False).reset_index(drop=True)
            total_count = by_strongs['count'].sum()
            by_strongs['pct'] = (by_strongs['count'] / total_count *
                                 100).round(1) if total_count else 0.0
            top_row = align_df.iloc[0]
            g_num = str(top_row.get('greekstrong', top_row.get('greek_g', '')))
            # Store as unpadded G# (matching LXX parquet format, e.g. 'G25' not 'G0025')
            if g_num and g_num.isdigit():
                result['lxx_primary_g'] = f"G{int(g_num)}"
            elif str(g_num).upper().startswith('G'):
                try:
                    result['lxx_primary_g'] = f"G{int(g_num[1:])}"
                except ValueError:
                    result['lxx_primary_g'] = g_num
            else:
                result['lxx_primary_g'] = ''
            result['lxx_primary'] = top_row.get('greek', '')
            # Consistency = % of tokens using the primary Strong's number
            primary_g = result['lxx_primary_g']
            # by_strongs uses greek_g which may be zero-padded; normalise for comparison

            def _norm_g(s: object) -> str:
                s = str(s).strip().upper()
                if s.startswith('G'):
                    try:
                        return f"G{int(s[1:])}"
                    except ValueError:
                        pass
                return s
            by_strongs['greek_g_norm'] = by_strongs['greek_g'].map(_norm_g)
            primary_rows = by_strongs[by_strongs['greek_g_norm'] == primary_g]
            result['lxx_consistency_pct'] = float(
                primary_rows.iloc[0]['pct']) if not primary_rows.empty else 0.0
        else:
            result['lxx_primary'] = ''
            result['lxx_primary_g'] = ''
            result['lxx_consistency_pct'] = 0.0

        # Full consistency profile
        try:
            lc = lxx_consistency(strongs)
            result['lxx_consistency'] = lc.get('overall_consistency', 0)
        except Exception:
            result['lxx_consistency'] = result['lxx_consistency_pct']

        lxx_g = result['lxx_primary_g']
    else:
        result['lxx_alignment'] = pd.DataFrame()
        result['lxx_primary'] = ''
        # Normalise to unpadded format for LXX parquet compatibility
        try:
            _g = strongs.strip().upper()
            lxx_g_norm = f"G{int(_g[1:])}" if _g.startswith('G') else strongs
        except ValueError:
            lxx_g_norm = strongs
        result['lxx_primary_g'] = lxx_g_norm
        result['lxx_consistency_pct'] = 0.0
        result['lxx_consistency'] = 0.0
        lxx_g = lxx_g_norm

    # ── Stage 3: LXX corpus distribution ─────────────────────────────────────
    if lxx_g:
        lxx_book_df = lxx_by_book(strongs=lxx_g)
        result['lxx_total'] = int(lxx_book_df['count'].sum()) if not lxx_book_df.empty else 0
        result['lxx_by_book'] = lxx_book_df
        # LXX lemma
        lxx_sample = query_lxx(strongs=lxx_g)
        result['lxx_lemma'] = lxx_sample.iloc[0]['lemma'] if not lxx_sample.empty else ''
    else:
        result['lxx_total'] = 0
        result['lxx_by_book'] = pd.DataFrame()
        result['lxx_lemma'] = ''

    # ── Stage 4: NT distribution ──────────────────────────────────────────────
    if not is_heb:
        # Greek input: NT usage is the word itself
        nt_df = _nt_by_book(strongs)
        result['nt_strongs'] = strongs
        result['nt_lemma'] = ws.get('lemma', '')
        result['nt_total'] = int(nt_df['count'].sum()) if not nt_df.empty else 0
        result['nt_by_book'] = nt_df
    else:
        # For Hebrew words: prefer the nt_lxx_equiv entry that matches the LXX primary word;
        # fall back to querying TAGNT directly using lxx_primary_g.
        nt_equivs = ws.get('nt_lxx_equiv', [])
        lxx_g_norm = result.get('lxx_primary_g', '')

        def _g_int(s: object) -> int:
            """Normalise G#### to int for comparison."""
            try:
                return int(str(s).strip().upper().lstrip('G'))
            except ValueError:
                return -1

        lxx_g_int = _g_int(lxx_g_norm)

        # Find the equiv whose Strong's matches the LXX primary G-number
        matched_equiv = None
        for eq in nt_equivs:
            if _g_int(eq.get('strongs', '')) == lxx_g_int and lxx_g_int > 0:
                matched_equiv = eq
                break
        if matched_equiv is None and nt_equivs:
            matched_equiv = nt_equivs[0]

        if lxx_g_int > 0:
            # Always prefer the LXX primary word's NT usage as the primary trajectory endpoint
            nt_df = _nt_by_book_g(lxx_g_int)
            lxx_lemma = result.get('lxx_lemma', '')
            result['nt_strongs'] = lxx_g_norm
            result['nt_lemma'] = lxx_lemma
            result['nt_total'] = int(nt_df['count'].sum()) if not nt_df.empty else 0
            result['nt_by_book'] = nt_df
        elif matched_equiv:
            result['nt_strongs'] = matched_equiv.get('strongs', '')
            result['nt_lemma'] = matched_equiv.get('lemma', '')
            result['nt_total'] = matched_equiv.get('nt_total', 0)
            nt_by_book = matched_equiv.get('nt_by_book', pd.DataFrame())
            result['nt_by_book'] = nt_by_book if isinstance(
                nt_by_book, pd.DataFrame) else pd.DataFrame()
        else:
            result['nt_strongs'] = ''
            result['nt_lemma'] = ''
            result['nt_total'] = 0
            result['nt_by_book'] = pd.DataFrame()

    # ── Stage 5: Continuity assessment ───────────────────────────────────────
    result['continuity'], result['continuity_note'] = _assess_continuity(result)

    return result


def _assess_continuity(r: dict) -> tuple[str, str]:
    """
    Compare LXX primary rendering with NT word choice.
    Returns (level, note) where level is 'high'|'medium'|'low'|'none'.
    """
    lxx_g = r.get('lxx_primary_g', '')
    nt_g = r.get('nt_strongs', '')
    lxx_pct = r.get('lxx_consistency_pct', 0.0)
    nt_total = r.get('nt_total', 0)

    if not lxx_g or not nt_g:
        return 'none', 'Insufficient data for continuity assessment.'

    # Normalise both to 'G<int>' (unpadded) for comparison
    def _norm(s: str) -> str:
        s = s.strip().upper()
        if s.startswith('G'):
            try:
                return f"G{int(s[1:])}"
            except ValueError:
                return s
        try:
            return f"G{int(s)}"
        except ValueError:
            return s

    lxx_norm = _norm(lxx_g)
    nt_norm = _norm(nt_g)

    if lxx_norm == nt_norm:
        if lxx_pct >= 80:
            return ('high',
                    f"NT adopts the dominant LXX word ({r.get('lxx_lemma', '')}, "
                    f"{lxx_pct:.0f}% consistent in LXX). Strong lexical continuity.")
        else:
            return ('medium',
                    f"NT uses the same Greek word as LXX ({r.get('lxx_lemma', '')}), "
                    f"but LXX rendering is only {lxx_pct:.0f}% consistent — "
                    f"multiple Greek words compete in the LXX.")
    else:
        if nt_total > 0:
            return ('low',
                    f"NT uses {r.get('nt_lemma', '')} ({nt_norm}) while the LXX "
                    f"primarily uses {r.get('lxx_lemma', '')} ({lxx_norm}). "
                    f"The NT draws on different vocabulary for this concept.")
        return ('none', 'No NT counterpart identified.')


# ── Terminal output ───────────────────────────────────────────────────────────

def print_trajectory(strongs: str, *, top_n: int = 10) -> None:
    """Print a formatted cross-testament trajectory to stdout."""
    t = word_trajectory(strongs)
    w = 72

    print(f"\n{'═'*w}")
    print(f"  Cross-Testament Trajectory: {t['strongs']}  {t['lemma']}  ({t['gloss']})")
    print(f"{'═'*w}")
    print(f"  {t['definition'][:w-2]}")
    print()

    if t['is_hebrew']:
        print("  ── OT Hebrew ──────────────────────────────────────────────────")
        print(f"  Total occurrences: {t['ot_total']:,}")
        ob = t['ot_by_book']
        if not ob.empty:
            top = ob.nlargest(top_n, 'count') if 'count' in ob.columns else ob.head(top_n)
            books_str = '  '.join(f"{r['book_id']}:{r['count']}" for _, r in top.iterrows())
            print(f"  Top books: {books_str}")
        print()

        print("  ── OT → LXX Alignment ─────────────────────────────────────────")
        align = t['lxx_alignment']
        if not align.empty:
            # Collapse inflected forms → by Strong's number for display
            by_g = align.groupby('greek_g', as_index=False)['count'].sum()
            total = by_g['count'].sum()
            by_g['pct'] = (by_g['count'] / total * 100).round(1) if total else 0.0
            by_g = by_g.sort_values('count', ascending=False)
            # Get a sample lemma (uninflected form, shortest) for each Strong's
            lemma_for = align.sort_values('greek').groupby('greek_g')['greek'].first().to_dict()
            for _, row in by_g.head(5).iterrows():
                g = row['greek_g']
                lemma = lemma_for.get(g, '')
                pct = row['pct']
                cnt = row['count']
                print(f"  {str(g):<10} {str(lemma):<20} {cnt:>5}×  {pct:>5.1f}%")
        else:
            print("  No alignment data available.")
        print(f"  LXX consistency: {t['lxx_consistency_pct']:.0f}%")
        print()

    print("  ── LXX Corpus ─────────────────────────────────────────────────")
    lxx_word = t.get('lxx_lemma', '') or t.get('lxx_primary', '')
    lxx_g = t.get('lxx_primary_g', '')
    print(f"  {lxx_g}  {lxx_word}  —  {t['lxx_total']:,} tokens in LXX")
    lb = t['lxx_by_book']
    if not lb.empty:
        top = lb.nlargest(top_n, 'count') if 'count' in lb.columns else lb.head(top_n)
        books_str = '  '.join(f"{r['book_id']}:{r['count']}" for _, r in top.iterrows())
        print(f"  Top books: {books_str}")
    print()

    print("  ── NT Greek ────────────────────────────────────────────────────")
    print(f"  {t['nt_strongs']}  {t['nt_lemma']}  —  {t['nt_total']:,} tokens in NT")
    nb = t['nt_by_book']
    if isinstance(nb, pd.DataFrame) and not nb.empty:
        col = 'count' if 'count' in nb.columns else nb.columns[-1]
        top = nb.nlargest(top_n, col)
        book_col = 'book_id' if 'book_id' in nb.columns else nb.columns[0]
        books_str = '  '.join(f"{r[book_col]}:{r[col]}" for _, r in top.iterrows())
        print(f"  Top books: {books_str}")
    print()

    cont_symbol = {'high': '✓✓', 'medium': '✓', 'low': '△', 'none': '—'}.get(t['continuity'], '—')
    print(
        f"  ── Continuity: {t['continuity'].upper()} {cont_symbol} ─────────────────────────────────")  # noqa: E501
    print(f"  {t['continuity_note']}")
    print()


# ── Chart ─────────────────────────────────────────────────────────────────────

def trajectory_chart(
    strongs: str,
    *,
    output_path: str | None = None,
    figsize: tuple = (15, 5),
) -> str:
    """
    Three-panel horizontal bar chart: OT by-book | LXX by-book | NT by-book.
    Returns path to saved PNG.
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    t = word_trajectory(strongs)

    slug = strongs.lower().replace(' ', '')
    if output_path is None:
        out_dir = Path('output') / 'charts' / 'ot' / 'lexicon'
        out_dir.mkdir(parents=True, exist_ok=True)
        output_path = str(out_dir / f'trajectory-{slug}.png')

    def _prep(df: pd.DataFrame | None, book_col: str, count_col: str,
              order: list[str], top_n: int = 15) -> tuple[list, list]:
        if df is None or (isinstance(df, pd.DataFrame) and df.empty):
            return [], []
        if not isinstance(df, pd.DataFrame):
            return [], []
        df = df.copy()
        df = df[df[count_col] > 0] if count_col in df.columns else df
        ord_map = {b: i for i, b in enumerate(order)}
        df['_ord'] = df[book_col].map(lambda b: ord_map.get(b, 999))
        df = df.sort_values('_ord').drop(columns='_ord')
        df = df.nlargest(top_n, count_col)
        return df[book_col].tolist(), df[count_col].tolist()

    # OT panel
    ot_df = t['ot_by_book']
    if isinstance(ot_df, pd.DataFrame) and not ot_df.empty:
        ob_col = 'book_id' if 'book_id' in ot_df.columns else ot_df.columns[0]
        ot_books, ot_counts = _prep(ot_df, ob_col, 'count', _OT_BOOK_ORDER)
    else:
        ot_books, ot_counts = [], []

    # LXX panel
    lb_df = t['lxx_by_book']
    if isinstance(lb_df, pd.DataFrame) and not lb_df.empty:
        lxx_books, lxx_counts = _prep(lb_df, 'book_id', 'count', _OT_BOOK_ORDER)
    else:
        lxx_books, lxx_counts = [], []

    # NT panel
    nt_df = t['nt_by_book']
    if isinstance(nt_df, pd.DataFrame) and not nt_df.empty:
        nb_col = 'book_id' if 'book_id' in nt_df.columns else nt_df.columns[0]
        cnt_col = 'count' if 'count' in nt_df.columns else nt_df.columns[-1]
        nt_books, nt_counts = _prep(nt_df, nb_col, cnt_col, _NT_BOOK_ORDER)
    else:
        nt_books, nt_counts = [], []

    fig, axes = plt.subplots(1, 3, figsize=figsize)
    panels = [
        (axes[0], ot_books,  ot_counts,  '#2c5f8a',
         f"OT Hebrew\n{t['strongs']} {t['lemma']} ({t['ot_total']:,} total)"),
        (axes[1], lxx_books, lxx_counts, '#5a8a2c',
         f"LXX Greek\n{t.get('lxx_primary_g', '')} {t.get('lxx_lemma', '')} ({t['lxx_total']:,} total)"),  # noqa: E501
        (axes[2], nt_books,  nt_counts,  '#8a2c2c',
         f"NT Greek\n{t.get('nt_strongs', '')} {t.get('nt_lemma', '')} ({t['nt_total']:,} total)"),
    ]

    for ax, books, counts, color, title in panels:
        if books:
            y = range(len(books))
            ax.barh(list(y), counts, color=color, alpha=0.85)
            ax.set_yticks(list(y))
            ax.set_yticklabels(books, fontsize=8)
            ax.invert_yaxis()
        ax.set_title(title, fontsize=9, fontweight='bold', pad=6)
        ax.xaxis.grid(True, linestyle='--', alpha=0.4)
        ax.set_axisbelow(True)
        if not books:
            ax.text(0.5, 0.5, 'No data', ha='center', va='center',
                    transform=ax.transAxes, color='gray', fontsize=9)

    cont = t['continuity'].upper()
    fig.suptitle(
        f"Cross-Testament Trajectory: {t['strongs']} {t['lemma']} \"{t['gloss']}\"\n"
        f"Continuity: {cont} — {t['continuity_note'][:80]}",
        fontsize=10, fontweight='bold', y=1.02,
    )
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    return output_path


# ── Markdown report ───────────────────────────────────────────────────────────

def save_trajectory_report(
    strongs: str,
    *,
    output_dir: str = 'output/reports/ot/lexicon',
    top_n: int = 15,
) -> str:
    """
    Generate a full Markdown + chart report for a word's cross-testament trajectory.
    Returns path to saved Markdown file.
    """
    t = word_trajectory(strongs)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    slug = strongs.lower().replace(' ', '')
    md_path = out_dir / f'trajectory-{slug}.md'
    chart_path = trajectory_chart(
        strongs,
        output_path=str(out_dir / f'trajectory-{slug}.png'),
    )

    lines = [
        f"# Cross-Testament Trajectory: {t['strongs']} {t['lemma']} \"{t['gloss']}\"",
        "",
        f"> **{t['lemma']}** ({t['translit']}) — {t['definition']}",
        "",
        f"![Trajectory chart]({Path(chart_path).name})",
        "",
        "| Corpus | Strong's | Lemma | Total |",
        "|---|---|---|---:|",
        f"| OT Hebrew | {t['strongs']} | {t['lemma']} | {t['ot_total']:,} |" if t['is_hebrew'] else "",  # noqa: E501
        f"| LXX Greek | {t.get('lxx_primary_g', '')} | {t.get('lxx_lemma', '')} "
        f"| {t['lxx_total']:,} |",
        f"| NT Greek  | {t.get('nt_strongs', '')} | {t.get('nt_lemma', '')} | {t['nt_total']:,} |",
        "",
    ]
    lines = [ln for ln in lines if ln is not None]

    # Continuity
    cont_emoji = {'high': '🟢', 'medium': '🟡', 'low': '🟠', 'none': '⚪'}.get(t['continuity'], '⚪')
    lines += [
        f"## Continuity Assessment: {t['continuity'].upper()} {cont_emoji}",
        "",
        t['continuity_note'],
        "",
    ]

    # OT section
    if t['is_hebrew']:
        lines += ["## OT Hebrew Distribution", ""]
        ob = t['ot_by_book']
        if isinstance(ob, pd.DataFrame) and not ob.empty:
            b_col = 'book_id' if 'book_id' in ob.columns else ob.columns[0]
            top_ot = ob.nlargest(top_n, 'count') if 'count' in ob.columns else ob.head(top_n)
            lines += ["| Book | Count |", "|---|---:|"]
            for _, r in top_ot.iterrows():
                lines.append(f"| {r[b_col]} | {r['count']} |")
        lines.append("")

        # Morphological forms
        mf = t.get('morph_forms')
        if isinstance(mf, pd.DataFrame) and not mf.empty:
            lines += ["### Morphological Forms", ""]
            col_str = ' | '.join(mf.columns)
            lines.append(f"| {col_str} |")
            lines.append("|" + "---|" * len(mf.columns))
            for _, r in mf.iterrows():
                lines.append("| " + " | ".join(str(v) for v in r) + " |")
            lines.append("")

    # LXX alignment
    align = t.get('lxx_alignment')
    if isinstance(align, pd.DataFrame) and not align.empty:
        lines += [
            "## OT → LXX Alignment",
            "",
            f"The LXX renders **{t['lemma']}** as follows "
            f"(consistency: {t['lxx_consistency_pct']:.0f}%):",
            "",
            "| LXX Strong's | LXX Lemma | Count | Pct |",
            "|---|---|---:|---:|",
        ]
        for _, r in align.head(8).iterrows():
            g = r.get('greek_g', '')
            lemma = r.get('greek', '')
            cnt = r.get('count', 0)
            pct = r.get('pct', 0)
            lines.append(f"| {g} | {lemma} | {cnt} | {pct:.1f}% |")
        lines.append("")

    # LXX distribution
    lb = t['lxx_by_book']
    if isinstance(lb, pd.DataFrame) and not lb.empty and t['lxx_total'] > 0:
        lines += ["## LXX Distribution", ""]
        top_lxx = lb[lb['count'] > 0].nlargest(top_n, 'count')
        lines += ["| Book | Count |", "|---|---:|"]
        for _, r in top_lxx.iterrows():
            lines.append(f"| {r['book_id']} | {r['count']} |")
        lines.append("")

    # NT distribution
    nb = t['nt_by_book']
    if isinstance(nb, pd.DataFrame) and not nb.empty:
        lines += ["## NT Distribution", ""]
        b_col = 'book_id' if 'book_id' in nb.columns else nb.columns[0]
        c_col = 'count' if 'count' in nb.columns else nb.columns[-1]
        top_nt = nb.nlargest(top_n, c_col)
        lines += ["| Book | Count |", "|---|---:|"]
        for _, r in top_nt.iterrows():
            lines.append(f"| {r[b_col]} | {r[c_col]} |")
        lines.append("")

    lines += [
        "---",
        "",
        "_Sources: TAHOT (STEPBible, CC BY 4.0), MACULA Hebrew WLC (Clear Bible, CC BY 4.0), "
        "CenterBLC LXX Rahlfs 1935, TAGNT (STEPBible, CC BY 4.0). "
        "Hebrew→LXX alignment via MACULA Hebrew inline greek/greekstrong columns._",
    ]

    md_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"  Saved: {md_path}")
    print(f"  Chart: {chart_path}")
    return str(md_path)


# ── Batch ─────────────────────────────────────────────────────────────────────

def batch_trajectories(
    strongs_list: list[str],
    *,
    output_dir: str = 'output/reports/ot/lexicon',
) -> list[str]:
    """
    Generate trajectory reports for a list of Strong's numbers.
    Returns list of Markdown file paths.
    """
    paths = []
    for s in strongs_list:
        try:
            path = save_trajectory_report(s, output_dir=output_dir)
            paths.append(path)
        except Exception as e:
            print(f"  Warning: {s} failed — {e}")
    return paths
