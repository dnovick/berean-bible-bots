"""
HTML and CSV export utilities for berean-bible-bots analyses.

Provides two levels of export:

  1. Low-level helpers — convert any DataFrame or analysis result to CSV or
     an HTML fragment / standalone page.

  2. High-level exporters — one function per analysis type that collects all
     the relevant DataFrames, renders a styled standalone HTML report, and
     also writes companion CSV files.

Output directories
------------------
  output/exports/csv/   — raw CSV files (one per table)
  output/exports/html/  — self-contained HTML reports (inline CSS, embedded charts)

Usage
-----
from bible_grammar.reporting.export import (
    export_csv, export_html_page,
    export_word_study, export_semantic_profile,
    export_genre_compare, export_divine_names,
    export_all,
)

# Single DataFrame → CSV
export_csv(df, 'my-table')

# Full word study report
export_word_study('H7965')   # שָׁלוֹם
export_word_study('G3056')   # λόγος

# Genre comparison report
export_genre_compare('OT')
export_genre_compare('NT')

# Divine names report
export_divine_names()

# Everything at once
export_all()
"""

from __future__ import annotations
import pandas as pd
from pathlib import Path
from typing import Any
import base64
import re

# ── Directory constants ───────────────────────────────────────────────────────

CSV_DIR = Path('output/exports/csv')
HTML_DIR = Path('output/exports/html')

for _d in (CSV_DIR, HTML_DIR):
    _d.mkdir(parents=True, exist_ok=True)


# ── Shared CSS ────────────────────────────────────────────────────────────────

_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  font-size: 14px;
  color: #1a1a2e;
  background: #f8f9fa;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}
h1 { font-size: 1.8rem; margin-bottom: 0.25rem; color: #1a1a2e; }
h2 { font-size: 1.25rem; margin: 2rem 0 0.5rem; color: #16213e; border-bottom: 2px solid #0f3460; padding-bottom: 0.25rem; }  # noqa: E501
h3 { font-size: 1rem; margin: 1.5rem 0 0.4rem; color: #0f3460; }
p  { margin: 0.5rem 0; line-height: 1.6; color: #444; }
.meta { font-size: 0.85rem; color: #666; margin-bottom: 1.5rem; }
.badge {
  display: inline-block;
  background: #0f3460;
  color: white;
  font-size: 0.75rem;
  padding: 0.15rem 0.5rem;
  border-radius: 3px;
  margin-right: 0.4rem;
}
table {
  border-collapse: collapse;
  width: 100%;
  margin: 0.5rem 0 1.5rem;
  background: white;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}
thead tr { background: #0f3460; color: white; }
th { padding: 0.55rem 0.75rem; text-align: left; font-weight: 600; font-size: 0.82rem; letter-spacing: 0.03em; }  # noqa: E501
th.num { text-align: right; }
td { padding: 0.45rem 0.75rem; border-bottom: 1px solid #eef0f4; font-size: 0.85rem; }
td.num { text-align: right; font-variant-numeric: tabular-nums; }
tr:last-child td { border-bottom: none; }
tr:nth-child(even) { background: #f4f6fb; }
tr:hover { background: #e8eef8; }
.chart-wrap { text-align: center; margin: 1rem 0 1.5rem; }
.chart-wrap img { max-width: 100%; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.12); }
blockquote { border-left: 3px solid #0f3460; padding: 0.4rem 1rem; color: #444; background: #f0f4fa; border-radius: 0 4px 4px 0; margin: 0.5rem 0 1rem; font-style: italic; }  # noqa: E501
.note { font-size: 0.8rem; color: #777; margin-top: 2rem; border-top: 1px solid #ddd; padding-top: 0.75rem; }  # noqa: E501
.toc { background: white; border-radius: 6px; padding: 1rem 1.5rem; margin-bottom: 2rem; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }  # noqa: E501
.toc ul { list-style: disc; padding-left: 1.5rem; }
.toc li { margin: 0.2rem 0; }
.toc a { color: #0f3460; text-decoration: none; }
.toc a:hover { text-decoration: underline; }
"""


# ── Low-level helpers ─────────────────────────────────────────────────────────

def export_csv(df: 'pd.DataFrame', slug: str, *, subdir: str = '') -> Path:
    """
    Write a DataFrame to CSV.

    Parameters
    ----------
    df    : DataFrame to export
    slug  : filename stem (no extension)
    subdir: optional subdirectory under CSV_DIR

    Returns the Path to the saved file.
    """
    dest = CSV_DIR / subdir if subdir else CSV_DIR
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / f"{slug}.csv"
    df.to_csv(path, index=True)
    return path


def _df_to_html_table(df: 'pd.DataFrame', *, numeric_cols: list[str] | None = None,
                      pct_cols: list[str] | None = None, float_fmt: str = '.1f') -> str:
    """Render a DataFrame as a styled HTML table string."""
    import pandas as pd

    numeric_cols = numeric_cols or []
    pct_cols = pct_cols or []
    auto_num = {c for c in df.columns
                if pd.api.types.is_numeric_dtype(df[c]) and c not in pct_cols}
    num_set = set(numeric_cols) | auto_num

    rows_html = []
    for idx, row in df.iterrows():
        cells = []
        for col in df.columns:
            val = row[col]
            is_num = col in num_set
            is_pct = col in pct_cols
            if is_pct and isinstance(val, (int, float)):
                cell = f'<td class="num">{val:{float_fmt}}%</td>'
            elif is_num and isinstance(val, (int, float)):
                if isinstance(val, float):
                    cell = f'<td class="num">{val:{float_fmt}}</td>'
                else:
                    cell = f'<td class="num">{val:,}</td>'
            else:
                cell = f'<td>{val}</td>'
            cells.append(cell)
        rows_html.append(f'  <tr>{"".join(cells)}</tr>')

    header_cells = []
    for col in df.columns:
        is_num = col in num_set or col in (pct_cols or [])
        cls = ' class="num"' if is_num else ''
        header_cells.append(f'<th{cls}>{col}</th>')

    return (
        '<table>\n'
        f'  <thead><tr>{"".join(header_cells)}</tr></thead>\n'
        '  <tbody>\n' +
        '\n'.join(rows_html) +
        '\n  </tbody>\n</table>'
    )


def _img_to_data_uri(path: str | Path) -> str:
    """Return a data: URI for a PNG file (for inline embedding)."""
    data = Path(path).read_bytes()
    b64 = base64.b64encode(data).decode()
    return f'data:image/png;base64,{b64}'


def export_html_page(
    sections: list[dict],
    title: str,
    slug: str,
    *,
    subtitle: str = '',
    source_note: str = 'STEPBible TAHOT/TAGNT/TALXX (CC BY 4.0, Tyndale House Cambridge)',
) -> Path:
    """
    Build and save a standalone HTML report.

    Parameters
    ----------
    sections : list of dicts, each with keys:
        'heading'    : str  (h2 level)
        'subheading' : str  (optional h3)
        'text'       : str  (optional paragraph)
        'df'         : DataFrame to render as table (optional)
        'chart'      : path to PNG to embed inline (optional)
        'html'       : raw HTML fragment to insert verbatim (optional)
        'pct_cols'   : list of column names to format as % (optional)
    title    : page <title> and <h1>
    slug     : output filename stem
    subtitle : optional subtitle line
    source_note : footer attribution

    Returns the Path to the saved file.
    """
    import datetime

    toc_items = [s['heading'] for s in sections if s.get('heading')]
    toc_anchors = [re.sub(r'[^a-z0-9]+', '-', h.lower()).strip('-') for h in toc_items]

    toc_html = ''
    if len(toc_items) > 2:
        lis = '\n'.join(
            f'    <li><a href="#{a}">{h}</a></li>'
            for h, a in zip(toc_items, toc_anchors)
        )
        toc_html = f'<div class="toc"><strong>Contents</strong><ul>\n{lis}\n</ul></div>'

    body_parts = []
    anchor_idx = 0
    for sec in sections:
        heading = sec.get('heading', '')
        subheading = sec.get('subheading', '')
        text = sec.get('text', '')
        df = sec.get('df')
        chart = sec.get('chart')
        raw = sec.get('html', '')
        pct_cols = sec.get('pct_cols', [])

        if heading:
            anchor = toc_anchors[anchor_idx] if anchor_idx < len(toc_anchors) else ''
            anchor_idx += 1
            body_parts.append(f'<h2 id="{anchor}">{heading}</h2>')
        if subheading:
            body_parts.append(f'<h3>{subheading}</h3>')
        if text:
            body_parts.append(f'<p>{text}</p>')
        if chart and Path(chart).exists():
            uri = _img_to_data_uri(chart)
            body_parts.append(f'<div class="chart-wrap"><img src="{uri}" alt="{heading}"></div>')
        if df is not None and not df.empty:
            body_parts.append(_df_to_html_table(df, pct_cols=pct_cols))
        if raw:
            body_parts.append(raw)

    now = datetime.datetime.now().strftime('%Y-%m-%d')
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>{_CSS}</style>
</head>
<body>
  <h1>{title}</h1>
  {"<p class='meta'>" + subtitle + "</p>" if subtitle else ""}
  <p class="meta">Generated {now}</p>
  {toc_html}
  {"".join(body_parts)}
  <p class="note">Source: {source_note}.</p>
</body>
</html>"""

    path = HTML_DIR / f"{slug}.html"
    path.write_text(html, encoding='utf-8')
    return path


# ── Analysis exporters ────────────────────────────────────────────────────────

def export_word_study(strongs: str, *, example_verses: int = 5) -> dict[str, Path | None]:
    """
    Export a word study to CSV + HTML.

    Returns dict with keys 'html', 'csv_by_book', 'csv_morphology', 'csv_collocates'.
    """
    from ..lexical.wordstudy import word_study
    from ..lexical.collocation import collocations
    from ..lexical.morph_chart import morph_distribution
    import pandas as pd

    clean = strongs.strip('{}').upper()
    is_heb = clean.startswith('H')
    ws = word_study(clean, example_verses=example_verses)
    co = collocations(clean, corpus='OT' if is_heb else 'NT', min_count=3, top_n=15)
    morph = morph_distribution(clean)

    slug = clean.lower()

    # ── CSV exports ────────────────────────────────────────────────────────
    csv_by_book = export_csv(ws['by_book'], f'{slug}-by-book', subdir='word-studies')

    csv_morph = None
    pivot = morph.get('pivot')
    if pivot is not None and not pivot.empty:
        col_totals = pivot.sum(axis=0).sort_values(ascending=False).reset_index()
        col_totals.columns = ['form', 'count']
        col_totals['pct'] = (col_totals['count'] / ws['total_occurrences'] * 100).round(1)
        csv_morph = export_csv(col_totals, f'{slug}-morphology', subdir='word-studies')

    csv_co = None
    if co is not None and not co.empty:
        csv_co = export_csv(co, f'{slug}-collocates', subdir='word-studies')

    te = ws.get('translation_equivalents')
    if te is not None and not te.empty:
        export_csv(te, f'{slug}-lxx-equivalents', subdir='word-studies')

    # ── HTML report ────────────────────────────────────────────────────────
    lang = 'Hebrew' if is_heb else 'Greek'
    lemma = ws.get('lemma', clean)
    gloss = ws.get('gloss', '')
    translit = ws.get('translit', '')

    sections: list[dict[str, Any]] = []

    # Header meta as HTML fragment
    badges = (f'<span class="badge">{clean}</span>'
              f'<span class="badge">{lang}</span>'
              f'<span class="badge">{ws["total_occurrences"]:,} occurrences</span>')
    defn = ws.get('definition', '')
    meta_html = f'{badges}<br><br>'
    if translit:
        meta_html += f'<strong>{lemma}</strong> /{translit}/ — {gloss}<br>'
    else:
        meta_html += f'<strong>{lemma}</strong> — {gloss}<br>'
    if defn:
        meta_html += f'<br><blockquote>{defn}</blockquote>'
    sections.append({'heading': '', 'html': meta_html})

    # Distribution
    sections.append({
        'heading': 'Distribution by Book',
        'df': ws['by_book'].rename(columns={'book_name': 'Book', 'count': 'Count', 'pct': '%'}),
        'pct_cols': ['%'],
    })

    # Morphology
    if pivot is not None and not pivot.empty:
        col_totals2 = pivot.sum(axis=0).sort_values(ascending=False).reset_index()
        col_totals2.columns = ['Form', 'Count']
        col_totals2['%'] = (col_totals2['Count'] / ws['total_occurrences'] * 100).round(1)
        sections.append({'heading': 'Morphological Forms', 'df': col_totals2, 'pct_cols': ['%']})

    # LXX equivalents
    if is_heb and te is not None and not te.empty:
        te_disp = te.rename(columns={'lxx_lemma': 'Greek Lemma', 'lxx_strongs': 'Strongs',
                                     'count': 'Count', 'pct': '%'}).head(10)
        sections.append({'heading': 'LXX Translation Equivalents',
                        'df': te_disp, 'pct_cols': ['%']})

    # OT→LXX→NT trajectory
    traj = ws.get('nt_lxx_equiv', [])
    if traj:
        traj_rows = []
        for eq in traj[:5]:
            traj_rows.append({'Greek Lemma': eq['lemma'], 'Strongs': eq['strongs'],
                              'NT Occurrences': eq['nt_total']})
        sections.append({'heading': 'OT → LXX → NT Trajectory',
                         'df': pd.DataFrame(traj_rows)})

    # Collocations
    if co is not None and not co.empty:
        co_disp = co[['lemma', 'strongs', 'gloss', 'co_count',
                      'expected', 'pmi', 'log_likelihood']].copy()
        co_disp.columns = ['Lemma', 'Strongs', 'Gloss', 'Observed', 'Expected', 'PMI', 'G²']
        sections.append({'heading': 'Top Collocates', 'df': co_disp})

    # Example verses
    examples = ws.get('examples', [])
    if examples:
        ex_html = '<ul style="list-style:none;padding:0">'
        for ex in examples:
            ctx = ex['context']
            # Bold the target word in context
            re.sub(r'[֑-ׇ̀-ͯ]', '', ex['word'])
            highlighted = ctx.replace(ex['word'], f'<strong>{ex["word"]}</strong>', 1)
            ex_html += (f'<li style="margin:0.75rem 0">'
                        f'<strong>[{ex["reference"]}]</strong> '
                        f'<em>{ex["word"]}</em><br>'
                        f'<span style="color:#555">{highlighted}</span></li>')
        ex_html += '</ul>'
        sections.append({'heading': 'Example Verses', 'html': ex_html})

    html_path = export_html_page(
        sections,
        title=f'Word Study: {lemma} ({clean})',
        slug=f'{slug}-word-study',
        subtitle=f'{lang} · {gloss} · {ws["total_occurrences"]:,} occurrences',
    )

    print(f'  HTML: {html_path}')
    print(f'  CSV:  {csv_by_book}')
    return {'html': html_path, 'csv_by_book': csv_by_book,
            'csv_morphology': csv_morph, 'csv_collocates': csv_co}


def export_genre_compare(corpus: str = 'OT') -> dict[str, Path]:
    """Export genre comparison to CSV + HTML for all features."""
    from ..discourse.genre_compare import genre_compare, genre_heatmap, OT_GENRES, NT_GENRES
    import pandas as pd

    corpus_label = 'Old Testament Hebrew' if corpus == 'OT' else 'New Testament Greek'
    features = (['verb_stem', 'verb_conjugation', 'pos'] if corpus == 'OT'
                else ['verb_tense', 'verb_voice', 'verb_mood', 'pos'])

    FEATURE_TITLES = {
        'verb_stem':        'Verb Stem Distribution',
        'verb_conjugation': 'Verb Conjugation Distribution',
        'pos':              'Part-of-Speech Distribution',
        'verb_tense':       'Verb Tense Distribution',
        'verb_voice':       'Verb Voice Distribution',
        'verb_mood':        'Verb Mood Distribution',
    }
    FEATURE_NOTES = {
        'verb_stem': ('Hebrew verb stems (binyanim) encode voice and action intensity. '
                      'Qal is simple active; Piel intensifies; Hiphil is causative; Niphal is passive/reflexive.'),  # noqa: E501
        'verb_conjugation': ('Consecutive Perfect (wayyiqtol) drives OT narrative prose. '
                             'Imperfect and Participle dominate poetry and prophecy.'),
        'pos': ('The ratio of verbs to nouns shifts across genres: '
                'narrative prose is verb-heavy, poetry and law are noun-heavy.'),
        'verb_tense': ('Aorist (punctiliar past) dominates narrative; Present dominates epistolary writing. '  # noqa: E501
                       'Perfect marks completed action with ongoing relevance.'),
        'verb_voice': ('Passive constructions increase in epistolary literature, '
                       'reflecting theological passives.'),
        'verb_mood': ('Participles are proportionally highest in Revelation and General letters. '
                      'Subjunctive marks contingency and hortatory purpose clauses.'),
    }

    sections: list[dict[str, Any]] = []
    csv_paths = {}

    # Token count summary
    genres = OT_GENRES if corpus == 'OT' else NT_GENRES
    token_rows = []
    for g, books in genres.items():
        df_all = genre_compare(corpus, 'pos', normalize=False)
        token_rows.append({'Genre': g, 'Books': len(books),
                           'Total Tokens': int(df_all.loc[g, 'total'])})
    sections.append({'heading': 'Token Counts by Genre',
                     'df': pd.DataFrame(token_rows)})

    for feat in features:
        df_pct = genre_compare(corpus, feat, normalize=True)
        df_cnt = genre_compare(corpus, feat, normalize=False)

        # Save CSV (counts)
        csv_p = export_csv(df_cnt.reset_index(), f'{corpus.lower()}-genre-{feat}',
                           subdir='genre-compare')
        csv_paths[feat] = csv_p

        # Generate heatmap chart
        chart_p = genre_heatmap(corpus, feat,
                                output_path=str(HTML_DIR / f'{corpus.lower()}-genre-{feat}.png'))

        cats = [c for c in df_pct.columns if c != 'total']
        # Build display df for HTML (pct with genre as column)
        disp = df_pct[cats].copy().reset_index()
        disp.columns = ['Genre'] + cats
        pct_cols = cats

        title = FEATURE_TITLES.get(feat, feat)
        note = FEATURE_NOTES.get(feat, '')
        sections.append({
            'heading': title,
            'text': note,
            'chart': chart_p,
            'df': disp,
            'pct_cols': pct_cols,
        })

    html_path = export_html_page(
        sections,
        title=f'Genre Comparison — {corpus_label}',
        slug=f'{corpus.lower()}-genre-comparison',
        subtitle=f'Morphological patterns across canonical literary sections · {corpus_label}',
    )

    print(f'  HTML: {html_path}')
    return {'html': html_path, **csv_paths}


def export_divine_names(corpora: list[str] | None = None) -> dict[str, Path]:
    """Export divine names analysis to CSV + HTML."""
    from ..names.divine_names import (divine_name_summary, divine_name_by_section,
                               divine_name_table, divine_names_chart)

    if corpora is None:
        corpora = ['OT', 'LXX', 'NT']

    CORPUS_LABELS = {
        'OT':  'Old Testament Hebrew',
        'LXX': 'Septuagint (canonical books)',
        'NT':  'New Testament Greek',
    }

    sections: list[dict[str, Any]] = []
    csv_paths = {}

    for corpus in corpora:
        summary = divine_name_summary(corpus)
        by_section = divine_name_by_section(corpus)
        by_book = divine_name_table(corpus)

        # CSV
        export_csv(summary,    f'{corpus.lower()}-divine-names-summary',    subdir='divine-names')
        export_csv(by_section, f'{corpus.lower()}-divine-names-by-section', subdir='divine-names')
        csv_p = export_csv(by_book, f'{corpus.lower()}-divine-names-by-book', subdir='divine-names')
        csv_paths[corpus] = csv_p

        # Charts
        bar_p = divine_names_chart(corpus, chart_type='stacked_bar',
                                   output_path=str(HTML_DIR / f'{corpus.lower()}-divine-names-bar.png'))  # noqa: E501
        heat_p = divine_names_chart(corpus, chart_type='heatmap',
                                    output_path=str(HTML_DIR / f'{corpus.lower()}-divine-names-heatmap.png'))  # noqa: E501

        label = CORPUS_LABELS[corpus]
        sections += [
            {'heading': label},
            {'subheading': 'Overview',
             'df': summary[['label', 'script', 'strongs', 'total', 'pct', 'top_books']].rename(
                 columns={'label': 'Name', 'script': 'Script', 'strongs': 'Strongs',
                          'total': 'Total', 'pct': '%', 'top_books': 'Top Books'}),
             'pct_cols': ['%']},
            {'subheading': 'Distribution by Section',
             'df': by_section.drop(columns=['strongs'])},
            {'subheading': 'Distribution by Book (bar chart)', 'chart': bar_p},
            {'subheading': 'Distribution by Section (heatmap)', 'chart': heat_p},
        ]

    html_path = export_html_page(
        sections,
        title='Divine Names and Christological Titles',
        slug='divine-names',
        subtitle='Hebrew OT · Septuagint LXX · Greek NT',
    )

    print(f'  HTML: {html_path}')
    return {'html': html_path, **csv_paths}


def export_semantic_profile(strongs: str) -> dict[str, Path]:
    """Export a semantic profile to HTML + CSV."""
    from ..lexical.semantic_profile import semantic_profile
    import pandas as pd

    clean = strongs.strip('{}').upper()
    is_heb = clean.startswith('H')
    p = semantic_profile(clean, top_collocates=15, example_verses=6)
    ws = p['word_study']
    lc = p['lxx_consistency']
    co = p['collocations']
    morph = p['morph']

    slug = clean.lower()
    lemma = ws.get('lemma', clean)
    gloss = ws.get('gloss', '')
    lang = 'Hebrew' if is_heb else 'Greek'

    # Distribution chart (reuse existing generator)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    bb = ws['by_book'].head(20)
    fig, ax = plt.subplots(figsize=(10, 5))
    x = range(len(bb))
    ax.bar(x, bb['count'], color='#4C72B0', edgecolor='white', linewidth=0.5)
    ax.set_xticks(list(x))
    ax.set_xticklabels(bb['book_name'], rotation=45, ha='right', fontsize=8)
    ax.set_ylabel('Occurrences', fontsize=9)
    ax.set_title(f'{lemma} ({clean}) — "{gloss}" · {ws["total_occurrences"]:,} occurrences',
                 fontsize=11, fontweight='bold')
    ax.yaxis.grid(True, linestyle='--', alpha=0.4)
    ax.set_axisbelow(True)
    plt.tight_layout()
    chart_p = HTML_DIR / f'{slug}-distribution.png'
    plt.savefig(chart_p, dpi=150, bbox_inches='tight')
    plt.close()

    # CSV
    export_csv(ws['by_book'], f'{slug}-by-book', subdir='semantic-profiles')
    if co is not None and not co.empty:
        export_csv(co, f'{slug}-collocates', subdir='semantic-profiles')

    # Sections
    sections: list[dict[str, Any]] = []
    badges = (f'<span class="badge">{clean}</span>'
              f'<span class="badge">{lang}</span>'
              f'<span class="badge">{ws["total_occurrences"]:,} occurrences</span>')
    defn = ws.get('definition', '')
    meta_html = f'{badges}<br><br><strong>{lemma}</strong>'
    if ws.get('translit'):
        meta_html += f' /{ws["translit"]}/'
    meta_html += f' — {gloss}'
    if defn:
        meta_html += f'<br><br><blockquote>{defn}</blockquote>'
    sections.append({'heading': '', 'html': meta_html})

    sections.append({
        'heading': 'Distribution by Book', 'chart': str(chart_p),
        'df': ws['by_book'].rename(columns={'book_name': 'Book', 'count': 'Count', 'pct': '%'}),
        'pct_cols': ['%'],
    })

    pivot = morph.get('pivot')
    if pivot is not None and not pivot.empty:
        col_totals = pivot.sum(axis=0).sort_values(ascending=False).reset_index()
        col_totals.columns = ['Form', 'Count']
        col_totals['%'] = (col_totals['Count'] / ws['total_occurrences'] * 100).round(1)
        sections.append({'heading': 'Morphological Forms', 'df': col_totals, 'pct_cols': ['%']})

    if is_heb:
        te = ws.get('translation_equivalents')
        if te is not None and not te.empty:
            te_disp = te.rename(columns={'lxx_lemma': 'Greek Lemma', 'lxx_strongs': 'Strongs',
                                         'count': 'Count', 'pct': '%'}).head(10)
            sections.append({'heading': 'LXX Translation Equivalents',
                            'df': te_disp, 'pct_cols': ['%']})

        if lc and lc.get('total_aligned', 0) > 0:
            book_rows = []
            for b in lc.get('books', []):
                alts = {k: v for k, v in b['rendering_profile'].items() if k != b['primary_lemma']}
                alt_str = '  '.join(f"{k}×{v}" for k, v in sorted(
                    alts.items(), key=lambda x: -x[1]))[:40]
                book_rows.append({
                    'Book': b['book_name'], 'Tokens': b['total'],
                    'Primary': b['primary_lemma'], 'Consistency': b['consistency'],
                    'Alt Renderings': alt_str,
                })
            cons_html = (f'<p><strong>Overall consistency:</strong> {lc["overall_consistency"]:.0f}% &nbsp; '  # noqa: E501
                         f'<strong>Corpus-wide primary:</strong> {lc["corpus_primary"]} '
                         f'({lc["corpus_primary_pct"]:.0f}%)</p>')
            sections.append({'heading': 'LXX Translation Consistency', 'html': cons_html,
                             'df': pd.DataFrame(book_rows), 'pct_cols': ['Consistency']})

        traj = ws.get('nt_lxx_equiv', [])
        if traj:
            traj_rows = [{'Greek Lemma': eq['lemma'], 'Strongs': eq['strongs'],
                          'NT Occurrences': eq['nt_total']} for eq in traj[:5]]
            sections.append({'heading': 'OT → LXX → NT Trajectory',
                             'df': pd.DataFrame(traj_rows)})

    if co is not None and not co.empty:
        co_disp = co[['lemma', 'strongs', 'gloss', 'co_count',
                      'expected', 'pmi', 'log_likelihood']].copy()
        co_disp.columns = ['Lemma', 'Strongs', 'Gloss', 'Observed', 'Expected', 'PMI', 'G²']
        sections.append({'heading': 'Top Collocates', 'df': co_disp})

    examples = ws.get('examples', [])
    if examples:
        ex_html = '<ul style="list-style:none;padding:0">'
        for ex in examples:
            highlighted = ex['context'].replace(ex['word'], f'<strong>{ex["word"]}</strong>', 1)
            ex_html += (f'<li style="margin:0.75rem 0">'
                        f'<strong>[{ex["reference"]}]</strong> <em>{ex["word"]}</em><br>'
                        f'<span style="color:#555">{highlighted}</span></li>')
        ex_html += '</ul>'
        sections.append({'heading': 'Example Verses', 'html': ex_html})

    html_path = export_html_page(
        sections,
        title=f'Semantic Profile: {lemma} ({clean})',
        slug=f'{slug}-semantic-profile',
        subtitle=f'{lang} · {gloss} · {ws["total_occurrences"]:,} occurrences',
    )

    print(f'  HTML: {html_path}')
    return {'html': html_path}


def export_all(*, word_studies: list[str] | None = None) -> dict[str, list[Path]]:
    """
    Run all available exporters and return a dict of output paths.

    word_studies: list of Strongs numbers to export individually.
                  Defaults to the pre-generated semantic profiles.
    """
    if word_studies is None:
        word_studies = ['H7965', 'H1285', 'H7307', 'G3056', 'G26']

    results: dict[str, list[Path]] = {}

    print('Exporting divine names...')
    r = export_divine_names()
    results['divine_names'] = [r['html']]

    print('Exporting genre comparisons...')
    for corpus in ['OT', 'NT']:
        r = export_genre_compare(corpus)
        results.setdefault('genre_compare', []).append(r['html'])

    print('Exporting word studies / semantic profiles...')
    for s in word_studies:
        r = export_semantic_profile(s)
        results.setdefault('semantic_profiles', []).append(r['html'])

    print('\nAll exports written to:')
    print(f'  HTML → {HTML_DIR}')
    print(f'  CSV  → {CSV_DIR}')
    return results
