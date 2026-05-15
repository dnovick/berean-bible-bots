"""
Divine name and christological term frequency analysis.

Tracks the major divine names and christological titles across the OT, LXX, and NT:

  OT Hebrew
  ─────────
  H3068G  יהוה  YHWH (the Tetragrammaton)
  H0430   אלהים  Elohim (God)
  H0136   אדני  Adonai (Lord)
  H3050   יה    Yah (short form of YHWH)
  H7706   שדי   El Shaddai (God Almighty)
  H0410   אל    El (God / Mighty One)

  LXX Greek
  ─────────
  G2962   κύριος  Kyrios (Lord — renders YHWH)
  G2316   θεός    Theos (God — renders Elohim)

  NT Greek
  ────────
  G2316   θεός    Theos (God)
  G2962   κύριος  Kyrios (Lord)
  G2424G  Ἰησοῦς  Iesous (Jesus)
  G5547   Χριστός Christos (Christ / Anointed)
  G3962   πατήρ   Pater (Father — in theological contexts)
  G4151   πνεῦμα  Pneuma (Spirit — in theological contexts)

Usage
-----
from bible_grammar.names.divine_names import divine_name_table, print_divine_names
from bible_grammar.names.divine_names import divine_names_chart, divine_names_report

# Overview tables
print_divine_names('OT')
print_divine_names('NT')

# Distribution chart
divine_names_chart('OT', output_path='output/charts/ot-divine-names.png')

# Full Markdown report
divine_names_report(output_dir='output/reports')
"""

from __future__ import annotations
import pandas as pd
from pathlib import Path

# ── Name registry ────────────────────────────────────────────────────────────

OT_DIVINE_NAMES: dict[str, dict] = {
    'H3068G': {'label': 'YHWH',       'hebrew': 'יהוה',  'gloss': 'the LORD (Tetragrammaton)'},
    'H0430':  {'label': 'Elohim',     'hebrew': 'אֱלֹהִים', 'gloss': 'God'},
    'H0136':  {'label': 'Adonai',     'hebrew': 'אֲדֹנָי', 'gloss': 'Lord (title)'},
    'H3050':  {'label': 'Yah',        'hebrew': 'יָהּ',   'gloss': 'Yah (short form of YHWH)'},
    'H7706':  {'label': 'Shaddai',    'hebrew': 'שַׁדַּי', 'gloss': 'Almighty'},
    'H0410':  {'label': 'El',         'hebrew': 'אֵל',    'gloss': 'God / Mighty One'},
}

NT_DIVINE_NAMES: dict[str, dict] = {
    'G2316':  {'label': 'Theos',      'greek': 'θεός',    'gloss': 'God'},
    'G2962':  {'label': 'Kyrios',     'greek': 'κύριος',  'gloss': 'Lord'},
    'G2424G': {'label': 'Iesous',     'greek': 'Ἰησοῦς', 'gloss': 'Jesus'},
    'G5547':  {'label': 'Christos',   'greek': 'Χριστός', 'gloss': 'Christ / Anointed'},
    'G3962':  {'label': 'Pater',      'greek': 'πατήρ',   'gloss': 'Father'},
    'G4151':  {'label': 'Pneuma',     'greek': 'πνεῦμα',  'gloss': 'Spirit'},
}

LXX_DIVINE_NAMES: dict[str, dict] = {
    'G2962':  {'label': 'Kyrios',  'greek': 'κύριος', 'gloss': 'Lord (renders YHWH)'},
    'G2316':  {'label': 'Theos',   'greek': 'θεός',   'gloss': 'God (renders Elohim)'},
}

# Canonical section groupings
OT_SECTIONS = {
    'Torah':      ['Gen', 'Exo', 'Lev', 'Num', 'Deu'],
    'Historical': ['Jos', 'Jdg', 'Rut', '1Sa', '2Sa', '1Ki', '2Ki', '1Ch', '2Ch', 'Ezr', 'Neh', 'Est'],  # noqa: E501
    'Wisdom':     ['Job', 'Psa', 'Pro', 'Ecc', 'Sng'],
    'Prophets':   ['Isa', 'Jer', 'Lam', 'Ezk', 'Dan', 'Hos', 'Jol', 'Amo', 'Oba', 'Jon', 'Mic',
                   'Nah', 'Hab', 'Zep', 'Hag', 'Zec', 'Mal'],
}

NT_SECTIONS = {
    'Gospels & Acts': ['Mat', 'Mrk', 'Luk', 'Jhn', 'Act'],
    'Pauline':        ['Rom', '1Co', '2Co', 'Gal', 'Eph', 'Php', 'Col', '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm'],  # noqa: E501
    'General & Rev':  ['Heb', 'Jas', '1Pe', '2Pe', '1Jn', '2Jn', '3Jn', 'Jud', 'Rev'],
}


# ── Core helpers ─────────────────────────────────────────────────────────────

def _load_corpus(corpus: str) -> pd.DataFrame:
    """Return the words DataFrame for 'OT', 'NT', or 'LXX'."""
    from ..core.query import query
    if corpus == 'LXX':
        df = pd.read_parquet('data/processed/lxx.parquet')
        df = df[~df['is_deuterocanon'].astype(bool)]   # canonical books only
        return df
    return query(testament=corpus)


def _count_by_book(df: pd.DataFrame, strongs_key: str) -> pd.Series:
    """Count rows matching strongs_key in each book, return Series indexed by book_id."""
    mask = df['strongs'].str.contains(strongs_key, na=False, regex=False)
    return df[mask].groupby('book_id').size()


def _book_name(book_id: str) -> str:
    from ..core.reference import book_info
    info = book_info(book_id)
    return info['name'] if info else book_id


def _book_order(book_id: str) -> int:
    from ..core.reference import book_info
    info = book_info(book_id)
    return info.get('canonical_order', 999) if info else 999


# ── Public API ────────────────────────────────────────────────────────────────

def divine_name_table(corpus: str = 'OT') -> 'pd.DataFrame':
    """
    Return a DataFrame with one row per book, one column per divine name.

    corpus: 'OT', 'NT', or 'LXX'
    """
    import pandas as pd

    df = _load_corpus(corpus)
    names = OT_DIVINE_NAMES if corpus == 'OT' else (
        LXX_DIVINE_NAMES if corpus == 'LXX' else NT_DIVINE_NAMES)

    # Build counts
    records = {}
    for strongs, meta in names.items():
        records[meta['label']] = _count_by_book(df, strongs)

    result = pd.DataFrame(records).fillna(0).astype(int)

    # Add book metadata
    result.index.name = 'book_id'
    result = result.reset_index()
    result['book_name'] = result['book_id'].apply(_book_name)
    result['canonical_order'] = result['book_id'].apply(_book_order)

    # Add Total column
    name_cols = list(names[k]['label'] for k in names)
    result['Total'] = result[name_cols].sum(axis=1)

    result = result.sort_values('canonical_order').reset_index(drop=True)
    return result


def divine_name_summary(corpus: str = 'OT') -> 'pd.DataFrame':
    """
    Return a summary DataFrame: one row per divine name with total count,
    percentage of all divine-name tokens, and top 3 books.
    """
    import pandas as pd

    df = _load_corpus(corpus)
    names = OT_DIVINE_NAMES if corpus == 'OT' else (
        LXX_DIVINE_NAMES if corpus == 'LXX' else NT_DIVINE_NAMES)

    rows = []
    for strongs, meta in names.items():
        mask = df['strongs'].str.contains(strongs, na=False, regex=False)
        total = int(mask.sum())
        by_book = df[mask].groupby('book_id').size().sort_values(ascending=False)
        top3 = ', '.join(f"{_book_name(b)} ({n})" for b, n in by_book.head(3).items())
        script = meta.get('hebrew', meta.get('greek', ''))
        rows.append({
            'strongs':  strongs,
            'label':    meta['label'],
            'script':   script,
            'gloss':    meta['gloss'],
            'total':    total,
            'top_books': top3,
        })

    summary = pd.DataFrame(rows)
    grand = summary['total'].sum()
    summary['pct'] = (summary['total'] / grand * 100).round(1) if grand > 0 else 0.0
    return summary.sort_values('total', ascending=False).reset_index(drop=True)


def divine_name_by_section(corpus: str = 'OT') -> 'pd.DataFrame':
    """
    Return a DataFrame: rows = divine names, columns = canonical sections,
    values = count per section.
    """
    import pandas as pd

    df = _load_corpus(corpus)
    names = OT_DIVINE_NAMES if corpus == 'OT' else (
        LXX_DIVINE_NAMES if corpus == 'LXX' else NT_DIVINE_NAMES)
    sections = OT_SECTIONS if corpus in ('OT', 'LXX') else NT_SECTIONS

    rows = []
    for strongs, meta in names.items():
        mask = df['strongs'].str.contains(strongs, na=False, regex=False)
        hits = df[mask]
        row = {'label': meta['label'], 'strongs': strongs}
        for sec_name, book_ids in sections.items():
            row[sec_name] = int(hits[hits['book_id'].isin(book_ids)].shape[0])
        row['Total'] = int(hits.shape[0])
        rows.append(row)

    return pd.DataFrame(rows).sort_values('Total', ascending=False).reset_index(drop=True)


def print_divine_names(corpus: str = 'OT') -> None:
    """Print a formatted summary report to stdout."""

    label = {'OT': 'Old Testament (Hebrew)', 'NT': 'New Testament (Greek)',
             'LXX': 'Septuagint (LXX)'}[corpus]
    summary = divine_name_summary(corpus)
    by_section = divine_name_by_section(corpus)

    w = 70
    print(f"\n{'═'*w}")
    print(f"  Divine Names Analysis — {label}")
    print(f"{'═'*w}\n")

    print("  Overview")
    print(f"  {'-'*w}")
    print(f"  {'Name':<14} {'Script':<12} {'Strongs':<10} {'Total':>7}  {'%':>6}  Top Books")
    print(f"  {'-'*13} {'-'*11} {'-'*9} {'-'*7}  {'-'*6}  {'-'*30}")
    for _, row in summary.iterrows():
        print(f"  {row['label']:<14} {row['script']:<12} {row['strongs']:<10} "
              f"{row['total']:>7,}  {row['pct']:>5.1f}%  {row['top_books']}")
    print()

    sections = OT_SECTIONS if corpus in ('OT', 'LXX') else NT_SECTIONS
    sec_names = list(sections.keys())
    print("  By Section")
    print(f"  {'-'*w}")
    header = f"  {'Name':<14} " + "".join(f"{s[:14]:<16}" for s in sec_names) + f"{'Total':>7}"
    print(header)
    print(f"  {'-'*13} " + "".join(f"{'-'*15} " for _ in sec_names) + f"{'-'*7}")
    for _, row in by_section.iterrows():
        line = f"  {row['label']:<14} "
        for s in sec_names:
            line += f"{row[s]:>8,}        "
        line += f"{row['Total']:>7,}"
        print(line)
    print()


def divine_names_chart(
    corpus: str = 'OT',
    *,
    output_path: str | None = None,
    top_n_books: int = 20,
    chart_type: str = 'stacked_bar',  # 'stacked_bar' | 'heatmap'
    figsize: tuple = (13, 6),
) -> str:
    """
    Generate and save a chart of divine name distribution.

    chart_type:
      'stacked_bar' — stacked bar chart, x=books, stacks=names (OT/LXX only makes sense)
      'heatmap'     — rows=divine names, cols=sections, cells=counts

    Returns path to saved PNG.
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np

    corpus_label = {'OT': 'Old Testament', 'NT': 'New Testament', 'LXX': 'LXX (Canonical)'}[corpus]
    names = OT_DIVINE_NAMES if corpus == 'OT' else (
        LXX_DIVINE_NAMES if corpus == 'LXX' else NT_DIVINE_NAMES)
    name_labels = [meta['label'] for meta in names.values()]

    if output_path is None:
        sub = 'ot' if corpus in ('OT', 'LXX') else 'nt'
        out_dir = Path('output') / 'charts' / sub / 'names'
        out_dir.mkdir(parents=True, exist_ok=True)
        suffix = 'bar' if chart_type == 'stacked_bar' else 'heatmap'
        output_path = str(out_dir / f"{corpus.lower()}-divine-names-{suffix}.png")

    if chart_type == 'stacked_bar':
        tbl = divine_name_table(corpus)
        # Pick top N books by total divine name count
        tbl_sorted = tbl.nlargest(top_n_books, 'Total')
        tbl_sorted = tbl_sorted.sort_values('canonical_order')

        fig, ax = plt.subplots(figsize=figsize)
        x = range(len(tbl_sorted))
        bottom = np.zeros(len(tbl_sorted))

        colors = [plt.get_cmap('tab10')(i) for i in range(10)]
        patches = []
        for i, lbl in enumerate(name_labels):
            if lbl not in tbl_sorted.columns:
                continue
            vals = tbl_sorted[lbl].values
            ax.bar(x, vals, bottom=bottom, color=colors[i % len(colors)],
                   label=lbl, edgecolor='white', linewidth=0.3)
            bottom += vals
            patches.append(mpatches.Patch(color=colors[i % len(colors)], label=lbl))

        ax.set_xticks(list(x))
        ax.set_xticklabels(tbl_sorted['book_name'], rotation=45, ha='right', fontsize=8)
        ax.set_ylabel('Occurrences', fontsize=9)
        ax.set_title(f'Divine Name Distribution — {corpus_label}\n(top {top_n_books} books by total)',  # noqa: E501
                     fontsize=11, fontweight='bold', pad=10)
        ax.yaxis.grid(True, linestyle='--', alpha=0.4)
        ax.set_axisbelow(True)
        ax.legend(handles=patches, loc='upper right', fontsize=8, framealpha=0.8)

    elif chart_type == 'heatmap':
        sec_df = divine_name_by_section(corpus)
        sections = OT_SECTIONS if corpus in ('OT', 'LXX') else NT_SECTIONS
        sec_cols = list(sections.keys())
        matrix = sec_df[sec_cols].values.astype(float)

        # Normalize per row (divine name) so heatmap shows relative emphasis
        row_max = matrix.max(axis=1, keepdims=True)
        row_max[row_max == 0] = 1
        matrix_norm = matrix / row_max

        fig, ax = plt.subplots(figsize=(max(8, len(sec_cols)*2), len(name_labels)+1))
        im = ax.imshow(matrix_norm, cmap='Blues', aspect='auto', vmin=0, vmax=1)

        ax.set_xticks(range(len(sec_cols)))
        ax.set_xticklabels(sec_cols, rotation=30, ha='right', fontsize=9)
        ax.set_yticks(range(len(sec_df)))
        ax.set_yticklabels(sec_df['label'].tolist(), fontsize=9)

        for i in range(len(sec_df)):
            for j in range(len(sec_cols)):
                raw = int(sec_df.iloc[i][sec_cols[j]])
                color = 'white' if matrix_norm[i, j] > 0.6 else 'black'
                ax.text(j, i, f'{raw:,}', ha='center', va='center', fontsize=8, color=color)

        plt.colorbar(im, ax=ax, label='Relative intensity (row-normalized)')
        ax.set_title(f'Divine Name Distribution by Section — {corpus_label}',
                     fontsize=11, fontweight='bold', pad=10)

    else:
        raise ValueError(f"Unknown chart_type: {chart_type!r}")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    return output_path


def divine_names_report(
    output_dir: str = 'output/reports/both/names',
    *,
    corpora: list[str] | None = None,
) -> str:
    """
    Generate a comprehensive Markdown report covering OT, LXX, and NT divine names.

    Returns the path to the saved Markdown file.
    """
    from pathlib import Path

    if corpora is None:
        corpora = ['OT', 'LXX', 'NT']

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / 'divine-names-report.md'

    lines = [
        "# Divine Names and Christological Titles",
        "",
        "Analysis of the major divine names across the Hebrew OT, Septuagint (LXX), "
        "and Greek NT, drawn from STEPBible TAHOT/TAGNT/TALXX morphological data.",
        "",
    ]

    corpus_labels = {
        'OT':  'Old Testament (Hebrew)',
        'LXX': 'Septuagint — canonical books only',
        'NT':  'New Testament (Greek)',
    }

    for corpus in corpora:
        # Generate chart
        chart_bar = divine_names_chart(corpus, chart_type='stacked_bar',
                                       output_path=str(out_dir / f'{corpus.lower()}-divine-names-bar.png'))  # noqa: E501
        chart_heat = divine_names_chart(corpus, chart_type='heatmap',
                                        output_path=str(out_dir / f'{corpus.lower()}-divine-names-heatmap.png'))  # noqa: E501

        summary = divine_name_summary(corpus)
        by_section = divine_name_by_section(corpus)
        by_book = divine_name_table(corpus)

        names = OT_DIVINE_NAMES if corpus == 'OT' else (
            LXX_DIVINE_NAMES if corpus == 'LXX' else NT_DIVINE_NAMES)
        sections = OT_SECTIONS if corpus in ('OT', 'LXX') else NT_SECTIONS
        sec_cols = list(sections.keys())
        name_labels = [meta['label'] for meta in names.values()]

        lines += [
            "---",
            "",
            f"## {corpus_labels[corpus]}",
            "",
        ]

        # Summary table
        lines += [
            "### Overview",
            "",
            "| Name | Script | Strongs | Total | % | Top Books |",
            "|---|---|---|---:|---:|---|",
        ]
        for _, row in summary.iterrows():
            lines.append(
                f"| {row['label']} | {row['script']} | {row['strongs']} "
                f"| {row['total']:,} | {row['pct']:.1f}% | {row['top_books']} |"
            )
        lines.append("")

        # By-section table
        lines += [
            "### Distribution by Section",
            "",
            "| Name | " + " | ".join(sec_cols) + " | Total |",
            "|---|" + "|".join(["---:" for _ in sec_cols]) + "|---:|",
        ]
        for _, row in by_section.iterrows():
            sec_vals = " | ".join(f"{row[s]:,}" for s in sec_cols)
            lines.append(f"| {row['label']} | {sec_vals} | {row['Total']:,} |")
        lines.append("")

        # Charts
        lines += [
            "### Charts",
            "",
            f"![{corpus} divine names distribution]({Path(chart_bar).name})",
            "",
            f"![{corpus} divine names heatmap]({Path(chart_heat).name})",
            "",
        ]

        # By-book table (all books)
        lines += [
            "### By Book",
            "",
            "| Book | " + " | ".join(name_labels) + " | Total |",
            "|---|" + "|".join(["---:" for _ in name_labels]) + "|---:|",
        ]
        for _, row in by_book.iterrows():
            vals = " | ".join(f"{row[lbl]:,}" for lbl in name_labels if lbl in row)
            lines.append(f"| {row['book_name']} | {vals} | {row['Total']:,} |")
        lines.append("")

    lines += [
        "---",
        "",
        "_Source: STEPBible TAHOT/TAGNT/TALXX (CC BY 4.0, Tyndale House Cambridge)._",
    ]

    md_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"  Saved: {md_path}")
    return str(md_path)
