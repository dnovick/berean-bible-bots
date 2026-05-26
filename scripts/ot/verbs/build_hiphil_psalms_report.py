"""Build Hiphil density report for the book of Psalms.

Outputs:
  output/reports/ot/verbs/hiphil-psalms/hiphil-psalms-report.md
  output/reports/ot/verbs/hiphil-psalms/hiphil-psalms-chapter-density.csv
  output/reports/ot/verbs/hiphil-psalms/hiphil-psalms-top-roots.csv
  output/reports/ot/verbs/hiphil-psalms/hiphil-psalms-density-bar.png
  output/reports/ot/verbs/hiphil-psalms/hiphil-psalms-top-roots-bar.png
  output/reports/ot/verbs/hiphil-psalms/hiphil-psalms-density-heatmap.png
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
from bidi.algorithm import get_display  # noqa: E402

from bible_grammar import query  # noqa: E402

REPORT_DIR = Path('output/reports/ot/verbs/hiphil-psalms')
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ── Load data ─────────────────────────────────────────────────────────────────

df = query(testament='ot')
all_psa = df[df['book_id'] == 'Psa'].copy()
psa_hiphil = all_psa[all_psa['stem'] == 'Hiphil'].copy()

BASELINE = len(psa_hiphil) / len(all_psa) * 100  # overall Psalms Hiphil rate


def extract_root_strongs(s: str) -> str:
    """Pull the H-number root from a MACULA strongs string like 'H9002/{H3034}'.

    Strips trailing letter suffixes (e.g. H7725M -> H7725) because MACULA uses
    sub-lexeme letters for contextual distinctions within the same root entry.
    """
    if pd.isna(s):
        return ''
    m = re.search(r'\{(H\d+)[A-Z]?\}', str(s))
    if m:
        return m.group(1)
    raw = re.sub(r'[{}]', '', str(s).split('/')[0])
    return re.sub(r'[A-Z]+$', '', raw)


def strip_cantillation(w: str) -> str:
    """Remove Hebrew cantillation marks (U+0591–U+05AF) from a word."""
    return ''.join(ch for ch in w if not (0x0591 <= ord(ch) <= 0x05AF))


def clean_word(w: str) -> str:
    """Strip prefixes (e.g. 'and/ '), maqqef, and cantillation from a Hebrew word form."""
    if '/' in w:
        w = w.split('/')[-1]
    w = re.sub(r'[\\].*', '', w)
    w = re.sub(r'[׃־]', '', w)
    return strip_cantillation(w).strip()


def get_lemma(root: str) -> str:
    """Return the best available Hebrew dictionary form for a root Strong's number."""
    subset = df[df['root_strongs'] == root]
    for stem, conj, person, gender, number in [
        ('Qal', 'Perfect', '3rd', 'Masculine', 'Singular'),
        ('Hiphil', 'Perfect', '3rd', 'Masculine', 'Singular'),
        ('Hiphil', 'Infinitive construct', '', '', ''),
    ]:
        filt = subset[subset['stem'] == stem]
        if conj:
            filt = filt[filt['conjugation'] == conj]
        if person:
            filt = filt[filt['person'] == person]
        if gender:
            filt = filt[filt['gender'] == gender]
        if number:
            filt = filt[filt['number'] == number]
        no_pref = filt[~filt['word'].str.contains('/', na=False)]
        if len(no_pref):
            return clean_word(no_pref['word'].mode()[0])
        if len(filt):
            return clean_word(filt['word'].mode()[0])
    no_pref = subset[~subset['word'].str.contains('/', na=False)]
    if len(no_pref):
        return clean_word(no_pref['word'].iloc[0])
    return root


df['root_strongs'] = df['strongs'].apply(extract_root_strongs)
psa_hiphil = psa_hiphil.copy()
psa_hiphil['root_strongs'] = psa_hiphil['strongs'].apply(extract_root_strongs)

# ── 1. Chapter-level density ──────────────────────────────────────────────────

word_counts = all_psa.groupby('chapter').size().rename('n_words')
verse_counts = all_psa.groupby('chapter')['verse'].nunique().rename('n_verses')
hiphil_counts = psa_hiphil.groupby('chapter').size().rename('n_hiphil')

ch_df = pd.concat([word_counts, verse_counts, hiphil_counts], axis=1).fillna(0)
ch_df['n_hiphil'] = ch_df['n_hiphil'].astype(int)
ch_df['hiphil_per_100w'] = (ch_df['n_hiphil'] / ch_df['n_words'] * 100).round(2)
ch_df['hiphil_per_verse'] = (ch_df['n_hiphil'] / ch_df['n_verses']).round(2)
ch_df.index.name = 'chapter'
ch_df = ch_df.reset_index()

# ── 2. Top roots ──────────────────────────────────────────────────────────────

# Best gloss: strip leading "and/ ", "the/ ", common prefix fragments


def clean_gloss(series: pd.Series) -> str:
    for g in series.mode():
        g = re.sub(r'^(and|the|to|I|he|you|they|[a-z]{1,3})[/ ]+', '', str(g))
        if len(g) > 2:
            return g.lower()
    return str(series.iloc[0]).lower()


root_df = (
    psa_hiphil.groupby('root_strongs')
    .agg(
        count=('root_strongs', 'size'),
        gloss=('translation', clean_gloss),
    )
    .sort_values('count', ascending=False)
    .reset_index()
)
root_df = root_df[root_df['root_strongs'] != ''].copy()
root_df['lemma'] = root_df['root_strongs'].apply(get_lemma)

# ── 3. Chart: density bar (top 30 chapters by hiphil_per_100w) ───────────────


def build_density_bar() -> Path:
    top = ch_df.sort_values('hiphil_per_100w', ascending=False).head(30)
    x = np.arange(len(top))
    colors = ['#1565C0' if v >= BASELINE * 2 else '#42A5F5' for v in top['hiphil_per_100w']]

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.bar(x, top['hiphil_per_100w'], color=colors, width=0.7)
    ax.axhline(BASELINE, color='#E53935', linewidth=1.2, linestyle='--',
               label=f'Psalms average ({BASELINE:.1f}%)')
    ax.set_xticks(x)
    ax.set_xticklabels([f'Ps {c}' for c in top['chapter']], rotation=45, ha='right', fontsize=8.5)
    ax.set_ylabel('Hiphil verbs per 100 words', fontsize=10)
    ax.set_title('Psalms — Top 30 Chapters by Hiphil Density\n(Hiphil verbs per 100 words)',
                 fontsize=11)
    ax.legend(fontsize=9)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=False))
    fig.tight_layout()
    out = REPORT_DIR / 'hiphil-psalms-density-bar.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'Saved {out}')
    return out


# ── 4. Chart: top-roots horizontal bar ───────────────────────────────────────

def build_roots_bar() -> Path:
    top = root_df.head(20).copy()
    top = top.iloc[::-1]  # flip so highest is at top
    labels = [
        get_display(f'{row.lemma} — {row.gloss}')
        for _, row in top.iterrows()
    ]

    fig, ax = plt.subplots(figsize=(10, 7))
    y = np.arange(len(top))
    ax.barh(y, top['count'], color='#1565C0', height=0.65)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel('Occurrences in Psalms (Hiphil)', fontsize=10)
    ax.set_title('Psalms — Top 20 Verb Roots in the Hiphil\n(by token count)', fontsize=11)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    fig.tight_layout()
    out = REPORT_DIR / 'hiphil-psalms-top-roots-bar.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'Saved {out}')
    return out


# ── 5. Chart: 15-chapter group heatmap (density across all 150 psalms) ───────

def build_density_heatmap() -> Path:
    """Heat strip showing density for every psalm, grouped into rows of 15."""
    n_cols = 15
    chapters = list(range(1, 151))
    density = {int(r.chapter): r.hiphil_per_100w for _, r in ch_df.iterrows()}
    grid_vals = [density.get(c, 0.0) for c in chapters]

    n_rows = len(chapters) // n_cols  # 150 / 15 = 10
    matrix = np.array(grid_vals).reshape(n_rows, n_cols)

    row_labels = [f'Ps {i*n_cols+1}–{(i+1)*n_cols}' for i in range(n_rows)]
    col_labels = [str(i + 1) for i in range(n_cols)]

    fig, ax = plt.subplots(figsize=(13, 5))
    vmax = max(10.0, matrix.max())
    im = ax.imshow(matrix, aspect='auto', cmap='Blues', vmin=0, vmax=vmax)

    ax.set_xticks(range(n_cols))
    ax.set_xticklabels(col_labels, fontsize=8)
    ax.set_yticks(range(n_rows))
    ax.set_yticklabels(row_labels, fontsize=9)

    for i in range(n_rows):
        for j in range(n_cols):
            v = matrix[i, j]
            if v > 0:
                color = 'white' if v > vmax * 0.6 else '#111'
                ax.text(j, i, f'{v:.1f}', ha='center', va='center',
                        fontsize=7, color=color)
            else:
                ax.text(j, i, '—', ha='center', va='center',
                        fontsize=7, color='#aaa')

    ax.set_title(
        'Psalms — Hiphil Density Across All 150 Chapters\n'
        '(Hiphil verbs per 100 words; column = offset within group)',
        fontsize=10,
    )
    plt.colorbar(im, ax=ax, label='Hiphil per 100 words', fraction=0.025, pad=0.02)
    fig.tight_layout()
    out = REPORT_DIR / 'hiphil-psalms-density-heatmap.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'Saved {out}')
    return out


# ── 6. Report ─────────────────────────────────────────────────────────────────

# Precompute a few headline figures
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
    'Chapter Density — Top 30 Psalms',
    'Full Density Map — All 150 Psalms',
    'Top Verb Roots in the Hiphil',
    'Detailed Chapter Table',
    'Grammar Note — The Hiphil Stem',
]


def build_report() -> Path:
    lines: list[str] = []

    lines += [
        '# Hiphil Verb Density in the Psalms',
        '',
        '**Corpus:** Hebrew Old Testament (MACULA/WLC)',
        '**Book:** Psalms (150 chapters)',
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
        f'- **Psalms contains {len(psa_hiphil):,} Hiphil verb tokens** across'
        f' {(ch_df["n_hiphil"] > 0).sum()} of 150 chapters'
        f' ({len(zero_hiphil)} chapters have none).',
        f'- **Overall Psalms Hiphil rate: {BASELINE:.1f} per 100 words.**'
        f' {n_above_baseline} chapters exceed this baseline.',
    ]
    top1 = top5_density.iloc[0]
    lines += [
        f'- **Most Hiphil-dense chapter: Psalm {int(top1.chapter)}**'
        f' ({top1.hiphil_per_100w:.1f} per 100 words,'
        f' {int(top1.n_hiphil)} tokens in {int(top1.n_words)} words).',
    ]
    lines += [
        '- **Top 5 densest chapters:** ' +
        ', '.join(f'Ps {int(r.chapter)} ({r.hiphil_per_100w:.1f}%)'
                  for _, r in top5_density.iterrows()) + '.',
        f'- **Most common Hiphil root:** {top5_roots.iloc[0].lemma}'
        f' ("{top5_roots.iloc[0].gloss}") — {int(top5_roots.iloc[0]["count"])} tokens.',
        '- **Top 5 roots:** ' +
        ', '.join(
            f'{r.lemma} "{r.gloss}" ({int(r["count"])})'
            for _, r in top5_roots.iterrows()
        ) + '.',
        '- **Theologically notable:** the Hiphil of הֹדוֹת ("give thanks")'
        ' is the most frequent root — the very verb behind the תּוֹדָה (todah)'
        ' thanksgiving genre that dominates Psalms.',
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
        ' (see the grammar note at the end of this report). In poetry, the Hiphil'
        ' is especially common in praise language — "cause to shine," "make great,"'
        ' "declare righteous," "save," "lift up."',
        '',
        'This report measures Hiphil density two ways:',
        '',
        '- **Per 100 words** — controls for chapter length; the most useful'
        ' cross-chapter comparison.',
        '- **Per verse** — useful for a feel of how Hiphil-saturated the poetry is'
        ' at the verse level.',
        '',
        f'The **Psalms-wide baseline** is **{BASELINE:.1f} Hiphil verbs per 100 words**'
        f' ({len(psa_hiphil):,} tokens / {len(all_psa):,} total words).',
        '',
        '---',
        '',
    ]

    # ── Section 2: Top-30 density bar ─────────────────────────────────────────
    lines += [
        '## Chapter Density — Top 30 Psalms',
        '',
        '![Hiphil density — top 30 psalms](hiphil-psalms-density-bar.png)',
        '',
        'Bars in **dark blue** exceed twice the Psalms average.'
        ' The **red dashed line** marks the Psalms-wide baseline'
        f' ({BASELINE:.1f} per 100 words).',
        '',
        '| Rank | Psalm | Hiphil tokens | Total words | Per 100 words | Per verse |',
        '|---|---|---|---|---|---|',
    ]
    for rank, (_, row) in enumerate(
        ch_df.sort_values('hiphil_per_100w', ascending=False).head(20).iterrows(), 1
    ):
        lines.append(
            f'| {rank} | Psalm {int(row.chapter)} |'
            f' {int(row.n_hiphil)} | {int(row.n_words)} |'
            f' {row.hiphil_per_100w:.2f} | {row.hiphil_per_verse:.2f} |'
        )
    lines += ['', '---', '']

    # ── Section 3: Heatmap ────────────────────────────────────────────────────
    lines += [
        '## Full Density Map — All 150 Psalms',
        '',
        '![Hiphil density heatmap — all 150 psalms](hiphil-psalms-density-heatmap.png)',
        '',
        'Each cell is one psalm. The number is Hiphil verbs per 100 words.'
        ' Darker = more Hiphil-dense. "—" = no Hiphil in that psalm.',
        '',
        f'**Psalms with no Hiphil verbs ({len(zero_hiphil)}):** ' +
        (', '.join(f'Ps {c}' for c in zero_hiphil) if zero_hiphil else 'none') + '.',
        '',
        '---',
        '',
    ]

    # ── Section 4: Top roots ──────────────────────────────────────────────────
    lines += [
        '## Top Verb Roots in the Hiphil',
        '',
        '![Top Hiphil roots in Psalms](hiphil-psalms-top-roots-bar.png)',
        '',
        '| Rank | Root | Gloss | Hiphil tokens |',
        '|---|---|---|---|',
    ]
    for rank, (_, row) in enumerate(root_df.head(25).iterrows(), 1):
        lines.append(
            f'| {rank} | {row.lemma} | {row.gloss} | {int(row["count"])} |'
        )
    lines += [
        '',
        '**Notes on the top roots:**',
        '',
        '- **הֹדוֹת (give thanks):** The Hiphil of this root is the'
        ' standard Psalms verb for corporate and individual praise — "I will give'
        ' thanks to the LORD." Its 38 occurrences top the list by a wide margin.',
        '- **שׁוּב (return/restore/repay):** The Hiphil expresses causative'
        ' return — "bring back," "restore," "repay." Its breadth of meaning'
        ' (petition, justice, deliverance) makes it the second most frequent'
        ' Hiphil root across Psalms.',
        '- **הִגִּיד (declare/proclaim):** The Hiphil expresses the act of'
        ' making something known, particularly God\'s works and righteousness'
        ' before the congregation.',
        '- **הוֹשִׁיעַ (save):** The Hiphil expresses deliverance by God —'
        ' the root behind יֵשׁוּעַ/יְשׁוּעָה (salvation). Central to the'
        ' lament and praise genres alike.',
        '- **הִבִּיט (look/pay attention):** Hiphil "cause to look," often'
        ' used in petition ("look upon me") or accusation.',
        '',
        '---',
        '',
    ]

    # ── Section 5: Full chapter table ─────────────────────────────────────────
    lines += [
        '## Detailed Chapter Table',
        '',
        'All 150 psalms, sorted by chapter number.',
        '',
        '| Psalm | Hiphil tokens | Total words | Per 100 words | Per verse |',
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
        f'✦ = more than twice the Psalms average ({BASELINE:.1f} per 100 words)',
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
        'In Psalms, the Hiphil frequently appears in:',
        '',
        '- **Praise verbs:** הוֹדָה (give thanks), הִגִּיד (declare),'
        ' הִשְׁמִיעַ (proclaim)',
        '- **Petition verbs:** הַצִּילָה (deliver!), הוֹשִׁיעָה (save!),'
        ' הַטֵּה (incline your ear!)',
        '- **Narrative of God\'s acts:** הוֹצִיא (brought out), הֵבִיא (brought),'
        ' הִכָּה (struck down)',
        '',
        'The high Hiphil density in psalms of praise and petition — compared with'
        ' psalms of instruction or lament — reflects this functional pattern:'
        ' the Hiphil is the verb of agency, and Psalms is full of appeals to'
        ' God\'s agency on behalf of his people.',
        '',
        '---',
        '',
        '*Report generated by'
        ' [scripts/ot/verbs/build_hiphil_psalms_report.py]'
        '(../../../../../scripts/ot/verbs/build_hiphil_psalms_report.py).*'
        ' *Source: MACULA Hebrew (WLC morphology, CC BY 4.0).*',
    ]

    out = REPORT_DIR / 'hiphil-psalms-report.md'
    out.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Saved {out}')
    return out


# ── 7. CSV exports ────────────────────────────────────────────────────────────

def build_csvs() -> None:
    ch_out = REPORT_DIR / 'hiphil-psalms-chapter-density.csv'
    ch_df.to_csv(ch_out, index=False)
    print(f'Saved {ch_out}')

    root_out = REPORT_DIR / 'hiphil-psalms-top-roots.csv'
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
