"""
Intertextuality network: OT verse / chapter / book → NT quotations.

Given any OT anchor (verse, chapter, or whole book), finds all NT verses
that quote or allude to it via the scrollmapper cross-reference data
(OpenBible.info, CC-BY), scored by community vote confidence.

Three query modes
-----------------
  verse   — single OT verse → all NT citations  (e.g. Isa 53:5)
  chapter — OT chapter → NT citation network    (e.g. Psa 22)
  book    — whole OT book → NT network overview (e.g. Isaiah)

Output
------
  • Terminal table (reference, NT verse, votes, KJV text)
  • NetworkX graph with matplotlib layout saved as PNG
  • Standalone HTML report (table + embedded graph + KJV snippets)
  • CSV of all edges

Usage
-----
from bible_grammar.intertextuality.intertextuality import (
    intertextuality, print_intertextuality,
    intertextuality_graph, intertextuality_report,
)

# Terminal output
print_intertextuality('Isa', chapter=53)
print_intertextuality('Psa', chapter=22)
print_intertextuality('Isa', chapter=53, verse=5)

# Network graph PNG
intertextuality_graph('Isa', chapter=53,
                      output_path='output/charts/isa53-network.png')

# Full HTML + CSV report
intertextuality_report('Isa', chapter=53, output_dir='output/reports')
"""

from __future__ import annotations
import pandas as pd
from pathlib import Path


# ── Reference helpers ─────────────────────────────────────────────────────────

def _ref_str(book: str, chapter: int | None = None, verse: int | None = None) -> str:
    if chapter and verse:
        return f"{book} {chapter}:{verse}"
    if chapter:
        return f"{book} {chapter}"
    return book


def _book_name(book_id: str) -> str:
    from ..core.reference import book_info
    info = book_info(book_id)
    return info['name'] if info else book_id


def _nt_book_order(book_id: str) -> int:
    from ..core.reference import book_info
    info = book_info(book_id)
    return info.get('canonical_order', 999) if info else 999


def _get_kjv_verse(book_id: str, chapter: int, verse: int) -> str:
    """Fetch a KJV verse text, returning empty string if unavailable."""
    try:
        from ..core import db as _db
        df = _db.load()
        rows = df[(df['book_id'] == book_id) & (df['chapter'] == chapter) &
                  (df['verse'] == verse) & (df['source'].isin({'TAHOT', 'TAGNT'}))]
        if rows.empty:
            return ''
        trans = rows['translation'].dropna()
        return ' '.join(str(t).strip().rstrip('¶').strip() for t in trans if str(t).strip())
    except Exception:
        return ''


# ── Core data function ────────────────────────────────────────────────────────

def intertextuality(
    ot_book: str,
    *,
    chapter: int | None = None,
    verse: int | None = None,
    min_votes: int = 20,
    include_kjv: bool = True,
) -> 'pd.DataFrame':
    """
    Return a DataFrame of OT→NT quotation links.

    Parameters
    ----------
    ot_book   : OT book ID (e.g. 'Isa', 'Psa', 'Gen')
    chapter   : OT chapter (None = all chapters in the book)
    verse     : OT verse   (None = all verses in the chapter)
    min_votes : minimum community-vote score for inclusion
    include_kjv: fetch KJV text snippets for each NT verse

    Returns
    -------
    DataFrame with columns:
      ot_ref, ot_book, ot_chapter, ot_verse,
      nt_ref, nt_book, nt_chapter, nt_verse,
      votes, ot_text, nt_text
    """
    import pandas as pd
    from .quotations import nt_quotations

    df = nt_quotations()
    q = df[df['ot_book'] == ot_book]
    if chapter is not None:
        q = q[q['ot_chapter'] == chapter]
    if verse is not None:
        q = q[q['ot_verse'] == verse]
    q = q[q['votes'] >= min_votes].copy()

    if q.empty:
        return pd.DataFrame(columns=['ot_ref', 'ot_book', 'ot_chapter', 'ot_verse',
                                     'nt_ref', 'nt_book', 'nt_chapter', 'nt_verse',
                                     'votes', 'ot_text', 'nt_text'])

    q = q.sort_values('votes', ascending=False).reset_index(drop=True)

    q['ot_ref'] = q.apply(
        lambda r: f"{_book_name(r['ot_book'])} {r['ot_chapter']}:{r['ot_verse']}", axis=1)
    q['nt_ref'] = q.apply(
        lambda r: f"{_book_name(r['nt_book'])} {r['nt_chapter']}:{r['nt_verse']}", axis=1)

    if include_kjv:
        q['ot_text'] = q.apply(
            lambda r: _get_kjv_verse(r['ot_book'], int(r['ot_chapter']), int(r['ot_verse'])), axis=1)  # noqa: E501
        q['nt_text'] = q.apply(
            lambda r: _get_kjv_verse(r['nt_book'], int(r['nt_chapter']), int(r['nt_verse'])), axis=1)  # noqa: E501
    else:
        q['ot_text'] = ''
        q['nt_text'] = ''

    return q[['ot_ref', 'ot_book', 'ot_chapter', 'ot_verse',
              'nt_ref', 'nt_book', 'nt_chapter', 'nt_verse',
              'votes', 'ot_text', 'nt_text']]


# ── Terminal output ───────────────────────────────────────────────────────────

def print_intertextuality(
    ot_book: str,
    *,
    chapter: int | None = None,
    verse: int | None = None,
    min_votes: int = 20,
) -> None:
    """Print a formatted intertextuality table to stdout."""

    df = intertextuality(ot_book, chapter=chapter, verse=verse,
                         min_votes=min_votes, include_kjv=True)

    _ref_str(ot_book, chapter, verse)
    full_anchor = _ref_str(_book_name(ot_book), chapter, verse)
    w = 72

    print(f"\n{'═'*w}")
    print(f"  Intertextuality Network: {full_anchor}")
    print(f"  {len(df)} NT citations  (min votes: {min_votes})")
    print(f"{'═'*w}\n")

    if df.empty:
        print(f"  No citations found at votes >= {min_votes}.")
        print("  Try lowering min_votes (e.g. min_votes=10).\n")
        return

    # Summary: NT book coverage
    nt_counts = df.groupby('nt_book').size().sort_values(ascending=False)
    print(f"  NT Books  ({nt_counts.shape[0]} books)")
    print(f"  {'-'*w}")
    for bk, cnt in nt_counts.items():
        bar = '█' * min(cnt, 20)
        print(f"    {_book_name(bk):<22} {cnt:>3} citation{'s' if cnt > 1 else ''}  {bar}")
    print()

    # Per-OT-verse grouping (useful when chapter or book scope)
    if verse is None:
        ot_verses = df['ot_ref'].unique()
        print("  Citations by OT Verse")
        print(f"  {'-'*w}")
        for ov in ot_verses:
            sub = df[df['ot_ref'] == ov]
            ot_txt = sub.iloc[0]['ot_text']
            if len(ot_txt) > 70:
                ot_txt = ot_txt[:67] + '...'
            print(f"\n  [{ov}]")
            if ot_txt:
                print(f"    \"{ot_txt}\"")
            for _, row in sub.iterrows():
                nt_txt = row['nt_text']
                if len(nt_txt) > 66:
                    nt_txt = nt_txt[:63] + '...'
                print(f"    → {row['nt_ref']:<25} votes={row['votes']:>4}  \"{nt_txt}\"")
    else:
        # Single verse: flat list
        ot_txt = df.iloc[0]['ot_text'] if not df.empty else ''
        if ot_txt:
            print(f"  OT: \"{ot_txt[:88]}\"")
            print()
        print(f"  {'NT Reference':<26} {'Votes':>6}  NT Text")
        print(f"  {'-'*25} {'-'*6}  {'-'*34}")
        for _, row in df.iterrows():
            nt_txt = row['nt_text']
            if len(nt_txt) > 55:
                nt_txt = nt_txt[:52] + '...'
            print(f"  {row['nt_ref']:<26} {row['votes']:>6}  \"{nt_txt}\"")
    print()


# ── Network graph ─────────────────────────────────────────────────────────────

def intertextuality_graph(
    ot_book: str,
    *,
    chapter: int | None = None,
    verse: int | None = None,
    min_votes: int = 20,
    output_path: str | None = None,
    figsize: tuple = (14, 9),
    layout: str = 'spring',   # 'spring' | 'bipartite' | 'shell'
) -> str:
    """
    Render the OT→NT quotation network as a PNG.

    Node types:
      • OT verses  — square markers, blue
      • NT books   — circle markers, coral (book-level aggregation)
      • NT verses  — circle markers, orange (if verse/chapter scope)

    Edge weight proportional to vote score.

    Returns the path to the saved PNG.
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import networkx as nx

    df = intertextuality(ot_book, chapter=chapter, verse=verse,
                         min_votes=min_votes, include_kjv=False)

    if output_path is None:
        out_dir = Path('output') / 'charts' / 'both' / 'intertextuality'
        out_dir.mkdir(parents=True, exist_ok=True)
        slug_parts = [ot_book.lower()]
        if chapter:
            slug_parts.append(str(chapter))
        if verse:
            slug_parts.append(str(verse))
        output_path = str(out_dir / ('-'.join(slug_parts) + '-network.png'))

    anchor_label = _ref_str(_book_name(ot_book), chapter, verse)

    if df.empty:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, f'No citations found for {anchor_label}\nat min_votes={min_votes}',
                ha='center', va='center', fontsize=12, transform=ax.transAxes)
        ax.axis('off')
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        return output_path

    G = nx.DiGraph()

    # Decide granularity: verse-level nodes for chapter/verse scope,
    # chapter-level for book scope
    book_scope = (chapter is None and verse is None)
    (chapter is not None and verse is None)

    df['votes'].max()

    for _, row in df.iterrows():
        ot_node = row['ot_ref']
        # NT node: book for full-book scope, verse otherwise
        if book_scope:
            nt_node = _book_name(row['nt_book'])
        else:
            nt_node = row['nt_ref']

        if not G.has_node(ot_node):
            G.add_node(ot_node, kind='ot',
                       chapter=int(row['ot_chapter']), verse=int(row['ot_verse']))
        if not G.has_node(nt_node):
            G.add_node(nt_node, kind='nt')

        # Accumulate weight for multi-verse book-scope
        if G.has_edge(ot_node, nt_node):
            G[ot_node][nt_node]['weight'] += row['votes']
            G[ot_node][nt_node]['count'] += 1
        else:
            G.add_edge(ot_node, nt_node, weight=row['votes'], count=1)

    # Layout
    ot_nodes = [n for n, d in G.nodes(data=True) if d.get('kind') == 'ot']
    nt_nodes = [n for n, d in G.nodes(data=True) if d.get('kind') == 'nt']

    if layout == 'bipartite' or True:  # bipartite always looks cleanest
        pos = {}
        ot_sorted = sorted(ot_nodes, key=lambda n: (
            G.nodes[n].get('chapter', 0), G.nodes[n].get('verse', 0)))
        nt_sorted = sorted(nt_nodes, key=lambda n: _nt_book_order(
            # recover book_id from display name
            next((row['nt_book'] for _, row in df.iterrows()
                  if _book_name(row['nt_book']) == n or row['nt_ref'] == n), n)
        ))
        for i, n in enumerate(ot_sorted):
            pos[n] = (0, -i * (10 / max(len(ot_sorted), 1)))
        for i, n in enumerate(nt_sorted):
            pos[n] = (2, -i * (10 / max(len(nt_sorted), 1)))

    fig, ax = plt.subplots(figsize=figsize)

    # Edge widths and colours
    edges = list(G.edges(data=True))
    weights = [d['weight'] for _, _, d in edges]
    max_w = max(weights) if weights else 1
    edge_widths = [0.5 + 3.5 * (w / max_w) for w in weights]
    edge_alpha = [0.3 + 0.5 * (w / max_w) for w in weights]

    for (u, v, d), lw, alpha in zip(edges, edge_widths, edge_alpha):
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], ax=ax,
                               width=lw, alpha=alpha,
                               edge_color='#0f3460', arrows=True,
                               arrowstyle='->', arrowsize=12,
                               connectionstyle='arc3,rad=0.05',
                               node_size=800)

    # OT nodes
    ot_sizes = []
    for n in ot_nodes:
        out_w = sum(d['weight'] for _, _, d in G.out_edges(n, data=True))
        ot_sizes.append(200 + min(out_w * 2, 1200))

    nx.draw_networkx_nodes(G, pos, nodelist=ot_nodes, ax=ax,
                           node_color='#4C72B0', node_size=ot_sizes,
                           node_shape='s', alpha=0.9)

    # NT nodes
    nt_sizes = []
    for n in nt_nodes:
        in_w = sum(d['weight'] for _, _, d in G.in_edges(n, data=True))
        nt_sizes.append(300 + min(in_w * 2, 1400))

    nx.draw_networkx_nodes(G, pos, nodelist=nt_nodes, ax=ax,
                           node_color='#DD6B48', node_size=nt_sizes,
                           node_shape='o', alpha=0.9)

    # Labels
    label_dict = {n: n for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=label_dict, ax=ax,
                            font_size=7.5, font_color='white', font_weight='bold')

    # Legend
    ot_patch = mpatches.Patch(color='#4C72B0', label='OT verse (■)')
    nt_patch = mpatches.Patch(color='#DD6B48', label='NT ' +
                              ('book' if book_scope else 'verse') + ' (●)')
    ax.legend(handles=[ot_patch, nt_patch], loc='lower right', fontsize=9)

    total_links = len(df)
    ax.set_title(
        f'Intertextuality Network: {anchor_label}\n'
        f'{total_links} citation{"s" if total_links != 1 else ""}  ·  '
        f'{len(ot_nodes)} OT verse{"s" if len(ot_nodes) != 1 else ""}  →  '
        f'{len(nt_nodes)} NT {"books" if book_scope else "verses"}  '
        f'(min votes: {min_votes})',
        fontsize=10, fontweight='bold', pad=12,
    )
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    return output_path


# ── HTML + CSV report ─────────────────────────────────────────────────────────

def intertextuality_report(
    ot_book: str,
    *,
    chapter: int | None = None,
    verse: int | None = None,
    min_votes: int = 20,
    output_dir: str = 'output/reports/both/intertextuality',
) -> str:
    """
    Generate an HTML + CSV report for an OT→NT intertextuality network.

    Returns path to the saved Markdown (HTML) file.
    """
    from pathlib import Path

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    slug_parts = [ot_book.lower()]
    if chapter:
        slug_parts.append(str(chapter))
    if verse:
        slug_parts.append(str(verse))
    slug = '-'.join(slug_parts) + '-intertextuality'

    anchor_full = _ref_str(_book_name(ot_book), chapter, verse)

    df = intertextuality(ot_book, chapter=chapter, verse=verse,
                         min_votes=min_votes, include_kjv=True)

    # Network graph
    chart_path = intertextuality_graph(
        ot_book, chapter=chapter, verse=verse, min_votes=min_votes,
        output_path=str(out_dir / f'{slug}-graph.png'),
    )

    # CSV
    csv_path = out_dir / f'{slug}.csv'
    if not df.empty:
        df[['ot_ref', 'nt_ref', 'votes', 'ot_text', 'nt_text']].to_csv(csv_path, index=False)
        print(f'  CSV:  {csv_path}')

    # Markdown report
    lines = [
        f"# Intertextuality Network: {anchor_full}",
        "",
        f"**OT anchor:** {anchor_full}  ",
        f"**NT citations:** {len(df):,}  ",
        f"**Min confidence votes:** {min_votes}  ",
        f"**NT books covered:** {df['nt_book'].nunique() if not df.empty else 0}  ",
        "",
    ]

    if df.empty:
        lines += [
            f"> No citations found at min_votes={min_votes}. "
            f"Try a lower threshold.",
            "",
        ]
    else:
        # Graph embed
        lines += [
            "## Network Graph",
            "",
            f"![{anchor_full} intertextuality network]({Path(chart_path).name})",
            "",
        ]

        # NT book summary
        nt_counts = (df.groupby('nt_book')
                       .agg(citations=('votes', 'count'), total_votes=('votes', 'sum'))
                       .sort_values('total_votes', ascending=False)
                       .reset_index())
        nt_counts['nt_book_name'] = nt_counts['nt_book'].apply(_book_name)

        lines += [
            "## NT Book Coverage",
            "",
            "| NT Book | Citations | Total Vote Score |",
            "|---|---:|---:|",
        ]
        for _, row in nt_counts.iterrows():
            lines.append(f"| {row['nt_book_name']} | {row['citations']} | {row['total_votes']:,} |")
        lines.append("")

        # Full citation table
        lines += [
            "## All Citations",
            "",
            "| OT Verse | NT Verse | Votes | OT Text | NT Text |",
            "|---|---|---:|---|---|",
        ]
        for _, row in df.iterrows():
            ot_txt = (row['ot_text'][:80] + '...') if len(row['ot_text']) > 80 else row['ot_text']
            nt_txt = (row['nt_text'][:80] + '...') if len(row['nt_text']) > 80 else row['nt_text']
            lines.append(
                f"| {row['ot_ref']} | {row['nt_ref']} | {row['votes']} "
                f"| {ot_txt} | {nt_txt} |"
            )
        lines.append("")

        # Per-verse detail (for verse/chapter scope only)
        if chapter is not None:
            lines += ["## Verse-by-Verse Detail", ""]
            for ot_ref in df['ot_ref'].unique():
                sub = df[df['ot_ref'] == ot_ref]
                ot_txt = sub.iloc[0]['ot_text']
                lines += [
                    f"### {ot_ref}",
                    "",
                    f"> {ot_txt}" if ot_txt else "",
                    "",
                ]
                for _, row in sub.iterrows():
                    nt_txt = row['nt_text']
                    lines += [
                        f"**[{row['nt_ref']}]** (votes: {row['votes']})  ",
                        f"> {nt_txt}" if nt_txt else "",
                        "",
                    ]

    lines += [
        "---",
        "",
        "_Cross-reference data: scrollmapper / OpenBible.info (CC-BY). "
        "Vote scores reflect community confidence in each link. "
        "Text: KJV (STEPBible TAHOT/TAGNT CC BY 4.0, Tyndale House Cambridge)._",
    ]

    md_path = out_dir / f'{slug}.md'
    md_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'  Saved: {md_path}')
    return str(md_path)
