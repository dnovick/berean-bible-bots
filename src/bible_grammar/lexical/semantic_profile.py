"""
Semantic range explorer: unified full-profile report for any Hebrew or Greek root.

Combines:
  - Lexicon entry (lemma, gloss, definition, POS)
  - Corpus frequency and book distribution
  - Morphological form breakdown
  - LXX translation equivalents and consistency (Hebrew only)
  - OT → LXX → NT trajectory (Hebrew only)
  - Top collocates (statistically significant neighbors)
  - Example verses (KJV)

Produces either a formatted terminal report or a shareable Markdown file
with an embedded distribution chart.

Usage
-----
from bible_grammar.lexical.semantic_profile import semantic_profile, print_semantic_profile
from bible_grammar.lexical.semantic_profile import save_semantic_profile

# Terminal report
print_semantic_profile('H7965')   # שָׁלוֹם peace
print_semantic_profile('G3056')   # λόγος word

# Save as Markdown + PNG chart
save_semantic_profile('H7965', output_dir='output/reports')
save_semantic_profile('G3056', output_dir='output/reports')
"""

from __future__ import annotations
from pathlib import Path
from typing import Any


def semantic_profile(strongs: str, *, collocate_window: int = 5,
                     min_collocate_count: int = 3,
                     top_collocates: int = 10,
                     example_verses: int = 4) -> dict:
    """
    Build a complete semantic profile for a Hebrew or Greek root.

    Returns a dict combining all available analyses.
    """
    from .wordstudy import word_study
    from ..intertextuality.lxx_consistency import lxx_consistency
    from .collocation import collocations
    from .morph_chart import morph_distribution

    clean = strongs.strip('{}').upper()
    is_hebrew = clean.startswith('H')
    corpus = 'OT' if is_hebrew else 'NT'

    # 1. Word study (core)
    ws = word_study(clean, example_verses=example_verses)

    # 2. LXX consistency (Hebrew only)
    lxx_cons = {}
    if is_hebrew:
        lxx_cons = lxx_consistency(clean, min_count=3)

    # 3. Collocations
    co_df = collocations(clean, window=collocate_window, corpus=corpus,
                         min_count=min_collocate_count, top_n=top_collocates)

    # 4. Morphological distribution
    morph = morph_distribution(clean)

    return {
        'strongs':         clean,
        'is_hebrew':       is_hebrew,
        'corpus':          corpus,
        'word_study':      ws,
        'lxx_consistency': lxx_cons,
        'collocations':    co_df,
        'morph':           morph,
    }


def print_semantic_profile(strongs: str, **kwargs: Any) -> None:
    """Print a formatted semantic profile to stdout."""

    p = semantic_profile(strongs, **kwargs)
    ws = p['word_study']
    lc = p['lxx_consistency']
    co = p['collocations']
    morph = p['morph']
    is_heb = p['is_hebrew']

    w = 70
    print(f"\n{'═'*w}")
    lang = 'Hebrew' if is_heb else 'Greek'
    lemma_str = f"  {ws['lemma']}  /{ws['translit']}/" if ws.get('translit') else f"  {ws['lemma']}"
    print(f"  Semantic Profile: {p['strongs']}  —  {lang}")
    if ws.get('lemma'):
        print(lemma_str)
    if ws.get('gloss'):
        print(f"  Gloss: {ws['gloss']}")
    print(f"{'═'*w}\n")

    # Definition
    if ws.get('definition'):
        print("  Definition")
        print(f"  {'-'*w}")
        words = ws['definition'].split()
        line = []
        for word in words:
            line.append(word)
            if len(' '.join(line)) > 66:
                print(f"    {' '.join(line[:-1])}")
                line = [word]
        if line:
            print(f"    {' '.join(line)}")
        print()

    # Frequency
    print(f"  Frequency                                  {ws['total_occurrences']:,} occurrences")
    print(f"  {'-'*w}")
    bb = ws['by_book'].head(12)
    for _, row in bb.iterrows():
        bar = '█' * min(int(row['pct'] / 2), 20)
        print(f"    {row['book_name']:<22} {row['count']:>5}  ({row['pct']:>4.1f}%)  {bar}")
    if len(ws['by_book']) > 12:
        print(f"    … and {len(ws['by_book'])-12} more books")
    print()

    # Morphological forms
    pivot = morph.get('pivot')
    if pivot is not None and not pivot.empty:
        print("  Morphological Distribution")
        print(f"  {'-'*w}")
        cols = pivot.columns.tolist()
        morph['pivot_pct']
        # Show top 6 forms by total count
        col_totals = pivot.sum(axis=0).sort_values(ascending=False)
        top_cols = col_totals.head(6).index.tolist()
        for col in top_cols:
            total_col = int(col_totals[col])
            pct = total_col / ws['total_occurrences'] * 100
            bar = '█' * min(int(pct / 2), 25)
            print(f"    {col:<35} {total_col:>5}  ({pct:>4.1f}%)  {bar}")
        if len(cols) > 6:
            rest = int(col_totals.iloc[6:].sum())
            print(f"    {'Other forms':<35} {rest:>5}")
        print()

    # LXX equivalents + consistency (Hebrew only)
    if is_heb:
        te = ws.get('translation_equivalents')
        if te is not None and not te.empty:
            print("  LXX Translation Equivalents")
            print(f"  {'-'*w}")
            for _, row in te.head(6).iterrows():
                lemma = row.get('lxx_lemma', '')
                sg = row.get('lxx_strongs', '')
                cnt = int(row.get('count', 0))
                pct = float(row.get('pct', 0))
                bar = '█' * min(int(pct / 5), 20)
                print(f"    {lemma:<20} {sg:<10} {cnt:>5}  ({pct:>4.1f}%)  {bar}")
            print()

        if lc and lc.get('total_aligned', 0) > 0:
            print(f"  LXX Consistency: {lc['overall_consistency']:.0f}%  "
                  f"(primary: {lc['corpus_primary']}  {lc['corpus_primary_pct']:.0f}%)")
            if lc.get('divergent_books'):
                print(f"  Divergent books: {', '.join(lc['divergent_books'])}")
            print()

        # OT → LXX → NT trajectory
        traj = ws.get('nt_lxx_equiv', [])
        if traj:
            print("  OT → LXX → NT Trajectory")
            print(f"  {'-'*w}")
            for eq in traj[:3]:
                print(f"    {eq['lemma']:<20} ({eq['strongs']})  →  {eq['nt_total']:,} NT occurrences")  # noqa: E501
                for _, row in eq['nt_by_book'].head(6).iterrows():
                    print(f"      {row['book_id']:<12} {row['count']:>4}")
            print()

    # Collocations
    if co is not None and not co.empty:
        print(f"  Top Collocates  (window ±{p.get('collocate_window', 5)}, corpus {p['corpus']})")
        print(f"  {'-'*w}")
        print(f"    {'Lemma':<22} {'Gloss':<25} {'Obs':>5}  {'G²':>8}")
        print(f"    {'-'*21} {'-'*24} {'-'*5}  {'-'*8}")
        for _, row in co.head(10).iterrows():
            print(f"    {row['lemma']:<22} {str(row['gloss'])[:24]:<25} "
                  f"{row['co_count']:>5}  {row['log_likelihood']:>8.1f}")
        print()

    # Example verses
    examples = ws.get('examples', [])
    if examples:
        print("  Example Verses")
        print(f"  {'-'*w}")
        for ex in examples:
            print(f"    [{ex['reference']}]  {ex['word']}")
            if ex['context']:
                ctx = ex['context']
                if len(ctx) > 88:
                    ctx = ctx[:85] + '...'
                print(f"      {ctx}")
        print()


def save_semantic_profile(
    strongs: str,
    *,
    output_dir: str | None = None,
    collocate_window: int = 5,
    min_collocate_count: int = 3,
    top_collocates: int = 10,
    example_verses: int = 5,
) -> str:
    """
    Save a complete semantic profile as a Markdown report with embedded chart.

    Returns the path to the saved Markdown file.
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    p = semantic_profile(strongs,
                         collocate_window=collocate_window,
                         min_collocate_count=min_collocate_count,
                         top_collocates=top_collocates,
                         example_verses=example_verses)

    ws = p['word_study']
    lc = p['lxx_consistency']
    co = p['collocations']
    morph = p['morph']
    is_heb = p['is_hebrew']
    clean = p['strongs']

    if output_dir is None:
        sub = 'ot' if is_heb else 'nt'
        out_dir = Path('output') / 'reports' / sub / 'lexicon'
    else:
        out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = clean.lower()
    chart_path = out_dir / f"{slug}-distribution.png"
    md_path = out_dir / f"{slug}-semantic-profile.md"

    # ── Chart: book distribution bar ──────────────────────────────────────
    bb = ws['by_book'].head(20)
    fig, ax = plt.subplots(figsize=(10, 5))
    x = range(len(bb))
    bars = ax.bar(x, bb['count'],
                  color='#4C72B0', edgecolor='white', linewidth=0.5)
    ax.set_xticks(list(x))
    ax.set_xticklabels(bb['book_name'], rotation=45, ha='right', fontsize=8)
    ax.set_ylabel('Occurrences', fontsize=9)
    lang = 'Hebrew' if is_heb else 'Greek'
    title = (f"{ws['lemma']} ({clean})  —  \"{ws['gloss']}\"\n"
             f"{lang} · {ws['total_occurrences']:,} total occurrences")
    ax.set_title(title, fontsize=11, fontweight='bold', pad=10)
    ax.yaxis.grid(True, linestyle='--', alpha=0.4)
    ax.set_axisbelow(True)
    for bar in bars:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.3,
                    str(int(h)), ha='center', va='bottom', fontsize=7)
    plt.tight_layout()
    plt.savefig(chart_path, dpi=150, bbox_inches='tight')
    plt.close()

    # ── Markdown ──────────────────────────────────────────────────────────
    lang_label = 'Hebrew' if is_heb else 'Greek'
    lines = []

    lines += [
        f"# Semantic Profile: {clean} — {ws.get('lemma', '')}",
        "",
        f"**Language:** {lang_label}  ",
        f"**Lemma:** {ws.get('lemma', '')}  ",
        f"**Transliteration:** {ws.get('translit', '')}  ",
        f"**Gloss:** {ws.get('gloss', '')}  ",
        f"**POS:** {ws.get('pos_code', '')}  ",
        f"**Total occurrences:** {ws['total_occurrences']:,}  ",
        "",
    ]

    if ws.get('definition'):
        lines += [
            "## Definition",
            "",
            ws['definition'],
            "",
        ]

    lines += [
        "## Distribution by Book",
        "",
        f"![{ws.get('lemma', clean)} distribution]({chart_path.name})",
        "",
    ]

    # Full book table
    bb_full = ws['by_book']
    lines += ["| Book | Count | % |", "|---|---:|---:|"]
    for _, row in bb_full.iterrows():
        lines.append(f"| {row['book_name']} | {row['count']:,} | {row['pct']:.1f}% |")
    lines.append("")

    # Morphological forms
    pivot = morph.get('pivot')
    if pivot is not None and not pivot.empty:
        col_totals = pivot.sum(axis=0).sort_values(ascending=False)
        lines += [
            "## Morphological Forms",
            "",
            "| Form | Count | % |",
            "|---|---:|---:|",
        ]
        for col, cnt in col_totals.items():
            pct = cnt / ws['total_occurrences'] * 100
            lines.append(f"| {col} | {int(cnt):,} | {pct:.1f}% |")
        lines.append("")

    # LXX equivalents (Hebrew only)
    if is_heb:
        te = ws.get('translation_equivalents')
        if te is not None and not te.empty:
            lines += [
                "## LXX Translation Equivalents",
                "",
                "| Greek Lemma | Strongs | Count | % |",
                "|---|---|---:|---:|",
            ]
            for _, row in te.head(10).iterrows():
                lines.append(
                    f"| {row.get('lxx_lemma', '')} | {row.get('lxx_strongs', '')} "
                    f"| {int(row.get('count', 0)):,} | {float(row.get('pct', 0)):.1f}% |"
                )
            lines.append("")

        if lc and lc.get('total_aligned', 0) > 0:
            lines += [
                "## LXX Translation Consistency",
                "",
                f"**Overall consistency:** {lc['overall_consistency']:.0f}%  ",
                f"**Corpus-wide primary rendering:** {lc['corpus_primary']} "
                f"({lc['corpus_primary_pct']:.0f}%)  ",
            ]
            if lc.get('divergent_books'):
                lines.append(f"**Divergent books:** {', '.join(lc['divergent_books'])}  ")
            lines += [
                "",
                "| Book | Tokens | Primary Rendering | Consistency | Alt Renderings |",
                "|---|---:|---|---:|---|",
            ]
            for b in lc.get('books', []):
                alts = {k: v for k, v in b['rendering_profile'].items()
                        if k != b['primary_lemma']}
                alt_str = '  '.join(f"{k}×{v}" for k, v in
                                    sorted(alts.items(), key=lambda x: -x[1]))[:40]
                div = ' ←' if b['diverges'] else ''
                lines.append(
                    f"| {b['book_name']} | {b['total']} | {b['primary_lemma']} "
                    f"| {b['consistency']:.0f}%{div} | {alt_str} |"
                )
            lines.append("")

        # OT → LXX → NT trajectory
        traj = ws.get('nt_lxx_equiv', [])
        if traj:
            lines += ["## OT → LXX → NT Trajectory", ""]
            for eq in traj[:3]:
                lines += [
                    f"**{eq['lemma']}** ({eq['strongs']}) — {eq['nt_total']:,} NT occurrences",
                    "",
                    "| NT Book | Count |",
                    "|---|---:|",
                ]
                for _, row in eq['nt_by_book'].head(10).iterrows():
                    lines.append(f"| {row['book_id']} | {row['count']} |")
                lines.append("")

    # Collocations
    if co is not None and not co.empty:
        lines += [
            f"## Top Collocates  (window ±{collocate_window}, {p['corpus']})",
            "",
            "| Lemma | Strongs | Gloss | Observed | Expected | PMI | G² |",
            "|---|---|---|---:|---:|---:|---:|",
        ]
        for _, row in co.iterrows():
            lines.append(
                f"| {row['lemma']} | {row['strongs']} | {row['gloss']} "
                f"| {row['co_count']} | {row['expected']:.1f} "
                f"| {row['pmi']:.2f} | {row['log_likelihood']:.1f} |"
            )
        lines.append("")

    # Example verses
    examples = ws.get('examples', [])
    if examples:
        lines += ["## Example Verses", ""]
        for ex in examples:
            ctx = ex['context']
            if len(ctx) > 120:
                ctx = ctx[:117] + '...'
            lines += [
                f"**[{ex['reference']}]** _{ex['word']}_  ",
                f"> {ctx}",
                "",
            ]

    lines += [
        "---",
        "",
        "_Source: STEPBible TAHOT/TAGNT/TALXX (CC BY 4.0, Tyndale House Cambridge). "
        "IBM Model 1 word alignment. Collocations scored by log-likelihood (G²)._",
    ]

    md_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"  Saved: {md_path}")
    print(f"  Chart: {chart_path}")
    return str(md_path)
