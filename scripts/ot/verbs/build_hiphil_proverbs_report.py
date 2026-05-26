"""Build Hiphil density report for the book of Proverbs.

Outputs:
  output/reports/ot/verbs/hiphil-proverbs/hiphil-proverbs-report.md
  output/reports/ot/verbs/hiphil-proverbs/hiphil-proverbs-chapter-density.csv
  output/reports/ot/verbs/hiphil-proverbs/hiphil-proverbs-top-roots.csv
  output/reports/ot/verbs/hiphil-proverbs/hiphil-proverbs-density-bar.png
  output/reports/ot/verbs/hiphil-proverbs/hiphil-proverbs-top-roots-bar.png
  output/reports/ot/verbs/hiphil-proverbs/hiphil-proverbs-density-heatmap.png
"""

from __future__ import annotations

import re
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker as mticker  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from bible_grammar import query  # noqa: E402

REPORT_DIR = Path('output/reports/ot/verbs/hiphil-proverbs')
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ── Load data ─────────────────────────────────────────────────────────────────

df = query(testament='ot')
all_pro = df[df['book_id'] == 'Pro'].copy()
pro_hiphil = all_pro[all_pro['stem'] == 'Hiphil'].copy()

BASELINE = len(pro_hiphil) / len(all_pro) * 100  # overall Proverbs Hiphil rate
N_CHAPTERS = all_pro['chapter'].nunique()


def extract_root_strongs(s: str) -> str:
    """Pull the H-number root from a MACULA strongs string like 'H9002/{H3034}'."""
    if pd.isna(s):
        return ''
    m = re.search(r'\{(H\d+[A-Z]?)\}', str(s))
    if m:
        return m.group(1)
    return re.sub(r'[{}]', '', str(s).split('/')[0])


pro_hiphil = pro_hiphil.copy()
pro_hiphil['root_strongs'] = pro_hiphil['strongs'].apply(extract_root_strongs)

# ── 1. Chapter-level density ──────────────────────────────────────────────────

word_counts = all_pro.groupby('chapter').size().rename('n_words')
verse_counts = all_pro.groupby('chapter')['verse'].nunique().rename('n_verses')
hiphil_counts = pro_hiphil.groupby('chapter').size().rename('n_hiphil')

ch_df = pd.concat([word_counts, verse_counts, hiphil_counts], axis=1).fillna(0)
ch_df['n_hiphil'] = ch_df['n_hiphil'].astype(int)
ch_df['hiphil_per_100w'] = (ch_df['n_hiphil'] / ch_df['n_words'] * 100).round(2)
ch_df['hiphil_per_verse'] = (ch_df['n_hiphil'] / ch_df['n_verses']).round(2)
ch_df.index.name = 'chapter'
ch_df = ch_df.reset_index()

# ── 2. Top roots ──────────────────────────────────────────────────────────────


def clean_gloss(series: pd.Series) -> str:
    for g in series.mode():
        g = re.sub(r'^(and|the|to|I|he|you|they|[a-z]{1,3})[/ ]+', '', str(g))
        if len(g) > 2:
            return g.lower()
    return str(series.iloc[0]).lower()


root_df = (
    pro_hiphil.groupby('root_strongs')
    .agg(
        count=('root_strongs', 'size'),
        gloss=('translation', clean_gloss),
    )
    .sort_values('count', ascending=False)
    .reset_index()
)
root_df = root_df[root_df['root_strongs'] != ''].copy()

# ── 3. Chart: density bar (all chapters sorted by density) ───────────────────


def build_density_bar() -> Path:
    top = ch_df.sort_values('hiphil_per_100w', ascending=False).head(31)
    x = np.arange(len(top))
    colors = ['#1565C0' if v >= BASELINE * 2 else '#42A5F5' for v in top['hiphil_per_100w']]

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.bar(x, top['hiphil_per_100w'], color=colors, width=0.7)
    ax.axhline(BASELINE, color='#E53935', linewidth=1.2, linestyle='--',
               label=f'Proverbs average ({BASELINE:.1f}%)')
    ax.set_xticks(x)
    ax.set_xticklabels([f'Pr {c}' for c in top['chapter']], rotation=45, ha='right', fontsize=8.5)
    ax.set_ylabel('Hiphil verbs per 100 words', fontsize=10)
    ax.set_title('Proverbs — Chapters by Hiphil Density\n(Hiphil verbs per 100 words)',
                 fontsize=11)
    ax.legend(fontsize=9)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=False))
    fig.tight_layout()
    out = REPORT_DIR / 'hiphil-proverbs-density-bar.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'Saved {out}')
    return out


# ── 4. Chart: top-roots horizontal bar ───────────────────────────────────────


def build_roots_bar() -> Path:
    top = root_df.head(20).copy()
    top = top.iloc[::-1]
    labels = [f'{row.root_strongs} — {row.gloss}' for _, row in top.iterrows()]

    fig, ax = plt.subplots(figsize=(10, 7))
    y = np.arange(len(top))
    ax.barh(y, top['count'], color='#1565C0', height=0.65)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel('Occurrences in Proverbs (Hiphil)', fontsize=10)
    ax.set_title('Proverbs — Top 20 Verb Roots in the Hiphil\n(by token count)', fontsize=11)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    fig.tight_layout()
    out = REPORT_DIR / 'hiphil-proverbs-top-roots-bar.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'Saved {out}')
    return out


# ── 5. Chart: chapter heatmap (all 31 chapters in a single row grid) ─────────


def build_density_heatmap() -> Path:
    """Heat strip showing density for every chapter."""
    n_cols = 11  # rows of ~11 give a compact 3-row grid for 31 chapters
    chapters = list(range(1, 32))
    density = {int(r.chapter): r.hiphil_per_100w for _, r in ch_df.iterrows()}

    # Pad to full grid
    n_rows = -(-len(chapters) // n_cols)  # ceiling division
    padded = chapters + [None] * (n_rows * n_cols - len(chapters))
    grid_vals = [density.get(c, 0.0) if c is not None else float('nan')
                 for c in padded]

    matrix = np.array(grid_vals, dtype=float).reshape(n_rows, n_cols)

    row_labels = [
        f'Pr {i * n_cols + 1}–{min((i + 1) * n_cols, 31)}'
        for i in range(n_rows)
    ]
    col_labels = [str(i + 1) for i in range(n_cols)]

    fig, ax = plt.subplots(figsize=(13, 3.5))
    vmax = max(10.0, float(np.nanmax(matrix)))
    im = ax.imshow(matrix, aspect='auto', cmap='Blues', vmin=0, vmax=vmax)

    ax.set_xticks(range(n_cols))
    ax.set_xticklabels(col_labels, fontsize=8)
    ax.set_yticks(range(n_rows))
    ax.set_yticklabels(row_labels, fontsize=9)

    for i in range(n_rows):
        for j in range(n_cols):
            v = matrix[i, j]
            c_idx = i * n_cols + j
            if c_idx >= len(chapters):
                ax.text(j, i, '', ha='center', va='center', fontsize=7)
            elif v > 0:
                color = 'white' if v > vmax * 0.6 else '#111'
                ax.text(j, i, f'{v:.1f}', ha='center', va='center',
                        fontsize=7, color=color)
            else:
                ax.text(j, i, '—', ha='center', va='center',
                        fontsize=7, color='#aaa')

    ax.set_title(
        'Proverbs — Hiphil Density Across All 31 Chapters\n'
        '(Hiphil verbs per 100 words; column = offset within group)',
        fontsize=10,
    )
    plt.colorbar(im, ax=ax, label='Hiphil per 100 words', fraction=0.025, pad=0.02)
    fig.tight_layout()
    out = REPORT_DIR / 'hiphil-proverbs-density-heatmap.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'Saved {out}')
    return out


# ── 6. Report ─────────────────────────────────────────────────────────────────

top5_density = ch_df.sort_values('hiphil_per_100w', ascending=False).head(5)
top5_roots = root_df.head(5)
zero_hiphil = sorted(ch_df[ch_df['n_hiphil'] == 0]['chapter'].tolist())
n_above_baseline = (ch_df['hiphil_per_100w'] > BASELINE).sum()


def _slug(heading: str) -> str:
    ascii_only = heading.encode('ascii', errors='ignore').decode()
    no_punct = re.sub(r'[^a-zA-Z0-9\s-]', '', ascii_only)
    slug = re.sub(r'\s+', '-', no_punct.lower())
    return re.sub(r'-{2,}', '-', slug).strip('-')


HEADINGS = [
    'Overview',
    'Chapter Density — All 31 Proverbs Chapters',
    'Full Density Map — All 31 Chapters',
    'Top Verb Roots in the Hiphil',
    'Detailed Chapter Table',
    'Grammar Note — The Hiphil Stem',
]


def build_report() -> Path:
    lines: list[str] = []

    lines += [
        '# Hiphil Verb Density in Proverbs',
        '',
        '**Corpus:** Hebrew Old Testament (MACULA/WLC)',
        '**Book:** Proverbs (31 chapters)',
        '**Focus:** Which chapters are most Hiphil-dense, and which verb roots'
        ' most commonly appear in the Hiphil',
        '',
        '---',
        '',
        '## Contents',
        '',
    ]
    for i, h in enumerate(HEADINGS, 1):
        lines.append(f'{i}. [{h}](#{_slug(h)})')
    lines += ['', '---', '']

    # ── Key Observations ──────────────────────────────────────────────────────
    lines += [
        '## Key Observations',
        '',
        f'- **Proverbs contains {len(pro_hiphil):,} Hiphil verb tokens** across'
        f' {(ch_df["n_hiphil"] > 0).sum()} of {N_CHAPTERS} chapters'
        f' ({len(zero_hiphil)} chapters have none).',
        f'- **Overall Proverbs Hiphil rate: {BASELINE:.1f} per 100 words.**'
        f' {n_above_baseline} chapters exceed this baseline.',
    ]
    top1 = top5_density.iloc[0]
    lines += [
        f'- **Most Hiphil-dense chapter: Proverbs {int(top1.chapter)}**'
        f' ({top1.hiphil_per_100w:.1f} per 100 words,'
        f' {int(top1.n_hiphil)} tokens in {int(top1.n_words)} words).',
        '- **Top 5 densest chapters:** ' +
        ', '.join(f'Pr {int(r.chapter)} ({r.hiphil_per_100w:.1f}%)'
                  for _, r in top5_density.iterrows()) + '.',
        f'- **Most common Hiphil root:** {top5_roots.iloc[0].root_strongs}'
        f' ("{top5_roots.iloc[0].gloss}") — {int(top5_roots.iloc[0]["count"])} tokens.',
        '- **Top 5 roots:** ' +
        ', '.join(
            f'{r.root_strongs} "{r.gloss}" ({int(r["count"])})'
            for _, r in top5_roots.iterrows()
        ) + '.',
        '- **Theologically notable:** the Hiphil of שָׂכַל (H7919A, "act wisely/prudently")'
        ' is the most frequent root — a causative frame deeply embedded in the'
        ' wisdom tradition: to make wise, to give insight, to cause understanding.',
        '',
        '---',
        '',
    ]

    # ── Section 1: Overview ───────────────────────────────────────────────────
    lines += [
        '## Overview',
        '',
        'The Hiphil is Hebrew\'s **causative stem**: it turns an intransitive root'
        ' into a transitive action, or expresses declarative and factitive meanings'
        ' (see the grammar note at the end of this report). In wisdom literature,'
        ' the Hiphil frequently appears in contexts of instruction and correction —'
        ' "cause to understand," "make wise," "bring to shame," "incline the heart."',
        '',
        'This report measures Hiphil density two ways:',
        '',
        '- **Per 100 words** — controls for chapter length; the most useful'
        ' cross-chapter comparison.',
        '- **Per verse** — useful for a feel of how Hiphil-saturated the'
        ' instruction is at the verse level.',
        '',
        f'The **Proverbs-wide baseline** is **{BASELINE:.1f} Hiphil verbs per 100 words**'
        f' ({len(pro_hiphil):,} tokens / {len(all_pro):,} total words).',
        '',
        '---',
        '',
    ]

    # ── Section 2: Density bar ────────────────────────────────────────────────
    lines += [
        '## Chapter Density — All 31 Proverbs Chapters',
        '',
        '![Hiphil density — Proverbs chapters](hiphil-proverbs-density-bar.png)',
        '',
        'Bars in **dark blue** exceed twice the Proverbs average.'
        ' The **red dashed line** marks the Proverbs-wide baseline'
        f' ({BASELINE:.1f} per 100 words).',
        '',
        '| Rank | Chapter | Hiphil tokens | Total words | Per 100 words | Per verse |',
        '|---|---|---|---|---|---|',
    ]
    for rank, (_, row) in enumerate(
        ch_df.sort_values('hiphil_per_100w', ascending=False).head(20).iterrows(), 1
    ):
        lines.append(
            f'| {rank} | Proverbs {int(row.chapter)} |'
            f' {int(row.n_hiphil)} | {int(row.n_words)} |'
            f' {row.hiphil_per_100w:.2f} | {row.hiphil_per_verse:.2f} |'
        )
    lines += ['', '---', '']

    # ── Section 3: Heatmap ────────────────────────────────────────────────────
    lines += [
        '## Full Density Map — All 31 Chapters',
        '',
        '![Hiphil density heatmap — Proverbs](hiphil-proverbs-density-heatmap.png)',
        '',
        'Each cell is one chapter. The number is Hiphil verbs per 100 words.'
        ' Darker = more Hiphil-dense. "—" = no Hiphil in that chapter.',
        '',
        f'**Chapters with no Hiphil verbs ({len(zero_hiphil)}):** ' +
        (', '.join(f'Pr {c}' for c in zero_hiphil) if zero_hiphil else 'none') + '.',
        '',
        '---',
        '',
    ]

    # ── Section 4: Top roots ──────────────────────────────────────────────────
    lines += [
        '## Top Verb Roots in the Hiphil',
        '',
        '![Top Hiphil roots in Proverbs](hiphil-proverbs-top-roots-bar.png)',
        '',
        '| Rank | Root (Strongs) | Gloss | Hiphil tokens |',
        '|---|---|---|---|',
    ]
    for rank, (_, row) in enumerate(root_df.head(25).iterrows(), 1):
        lines.append(
            f'| {rank} | {row.root_strongs} | {row.gloss} | {int(row["count"])} |'
        )
    lines += [
        '',
        '**Notes on the top roots:**',
        '',
        '- **H7919A (שָׂכַל, act wisely/prudently):** The Hiphil expresses the'
        ' causative of insight — to make someone wise, to instruct with'
        ' understanding. The signature verb of the wisdom tradition.',
        '- **H3254H (יָסַף, add/increase):** The Hiphil "cause to add" appears'
        ' repeatedly in Proverbs in contexts of gaining wisdom, words, and'
        ' days — "the wise will increase learning" (Pr 1:5).',
        '- **H0995 (בִּין, understand/discern):** The Hiphil expresses causing'
        ' someone to understand — the teacher\'s goal in wisdom instruction.',
        '- **H3198 (יָכַח, rebuke/reprove):** The Hiphil "cause to be reproved"'
        ' is the verb of correction, appearing in the famous Proverbs sayings'
        ' about accepting discipline and reproof.',
        '- **H5186 (נָטָה, incline):** Hiphil "incline (the heart/ear)" — a'
        ' common wisdom petition idiom, asking the student to attend to'
        ' instruction.',
        '',
        '---',
        '',
    ]

    # ── Section 5: Full chapter table ─────────────────────────────────────────
    lines += [
        '## Detailed Chapter Table',
        '',
        'All 31 chapters, sorted by chapter number.',
        '',
        '| Chapter | Hiphil tokens | Total words | Per 100 words | Per verse |',
        '|---|---|---|---|---|',
    ]
    for _, row in ch_df.sort_values('chapter').iterrows():
        marker = ' ✦' if row.hiphil_per_100w >= BASELINE * 2 else ''
        lines.append(
            f'| {int(row.chapter)} | {int(row.n_hiphil)} | {int(row.n_words)} |'
            f' {row.hiphil_per_100w:.2f}{marker} | {row.hiphil_per_verse:.2f} |'
        )
    lines += [
        '',
        f'✦ = more than twice the Proverbs average ({BASELINE:.1f} per 100 words)',
        '',
        '---',
        '',
    ]

    # ── Section 6: Grammar note ───────────────────────────────────────────────
    lines += [
        '## Grammar Note — The Hiphil Stem',
        '',
        'The **Hiphil** (הִפְעִיל) is one of the seven main Hebrew verb stems.'
        ' It is most often **causative**: it takes an action or state expressed'
        ' by the Qal and causes it to happen.',
        '',
        '| Qal | Hiphil | Meaning shift |',
        '|---|---|---|',
        '| בּוֹא — to come | הֵבִיא — to bring | cause to come |',
        '| יָצָא — to go out | הוֹצִיא — to bring out | cause to go out |',
        '| שָׁמַע — to hear | הִשְׁמִיעַ — to proclaim | cause to hear |',
        '| גָּדַל — to be great | הִגְדִּיל — to magnify | cause to be great |',
        '| יָשַׁע — to be saved | הוֹשִׁיעַ — to save | cause to be saved |',
        '',
        'In Proverbs, the Hiphil is especially prominent in wisdom and instruction'
        ' contexts:',
        '',
        '- **Wisdom verbs:** שִׂכֵּל (make wise), הֵבִין (cause to understand),'
        ' הוֹדִיעַ (make known)',
        '- **Correction verbs:** הוֹכִיחַ (rebuke), הֵשִׁיב (bring back/restore)',
        '- **Behavioral outcomes:** הֵבִישׁ (bring shame), הֵיטִיב (do good),'
        ' הִרְבָּה (increase)',
        '',
        'The relatively high Hiphil density in Proverbs compared with other'
        ' wisdom books reflects its didactic intent: Proverbs is a book of'
        ' causation — parents and teachers causing children to become wise,'
        ' and wisdom causing outcomes in those who embrace or reject it.',
        '',
        '---',
        '',
        '*Report generated by'
        ' [scripts/ot/verbs/build_hiphil_proverbs_report.py]'
        '(../../../../../scripts/ot/verbs/build_hiphil_proverbs_report.py).*'
        ' *Source: MACULA Hebrew (WLC morphology, CC BY 4.0).*',
    ]

    out = REPORT_DIR / 'hiphil-proverbs-report.md'
    out.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Saved {out}')
    return out


# ── 7. CSV exports ────────────────────────────────────────────────────────────

def build_csvs() -> None:
    ch_out = REPORT_DIR / 'hiphil-proverbs-chapter-density.csv'
    ch_df.to_csv(ch_out, index=False)
    print(f'Saved {ch_out}')

    root_out = REPORT_DIR / 'hiphil-proverbs-top-roots.csv'
    root_df.to_csv(root_out, index=False)
    print(f'Saved {root_out}')


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('Building charts...')
    build_density_bar()
    build_roots_bar()
    build_density_heatmap()

    print('Building report...')
    build_report()

    print('Building CSVs...')
    build_csvs()

    print('Done.')
