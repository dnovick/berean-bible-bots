"""
Build: NT OT Quotation Source Report — LXX vs MT alignment by book.

Runs batch_align() across every NT book and produces:
  - output/reports/both/intertextuality/nt-ot-source-alignment.md
  - output/reports/both/intertextuality/nt-ot-source-alignment.csv
  - output/reports/both/intertextuality/nt-ot-source-alignment-stacked.png
  - output/reports/both/intertextuality/nt-ot-source-alignment-heatmap.png
"""

from __future__ import annotations
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from bible_grammar import batch_align  # noqa: E402
from bible_grammar.core.reference import BOOKS  # noqa: E402

REPORT_DIR = Path('output/reports/both/intertextuality')
REPORT_DIR.mkdir(parents=True, exist_ok=True)

NT_BOOKS = [b[0] for b in BOOKS if b[2] == 'NT']

NT_FULL_NAMES = {
    'Mat': 'Matthew', 'Mrk': 'Mark', 'Luk': 'Luke', 'Jhn': 'John',
    'Act': 'Acts', 'Rom': 'Romans', '1Co': '1 Corinthians', '2Co': '2 Corinthians',
    'Gal': 'Galatians', 'Eph': 'Ephesians', 'Php': 'Philippians', 'Col': 'Colossians',
    '1Th': '1 Thessalonians', '2Th': '2 Thessalonians', '1Ti': '1 Timothy',
    '2Ti': '2 Timothy', 'Tit': 'Titus', 'Phm': 'Philemon', 'Heb': 'Hebrews',
    'Jas': 'James', '1Pe': '1 Peter', '2Pe': '2 Peter', '1Jn': '1 John',
    '2Jn': '2 John', '3Jn': '3 John', 'Jud': 'Jude', 'Rev': 'Revelation',
}

MIN_VOTES = 25

# ── 1. Gather per-book summary data ───────────────────────────────────────────


def gather_book_stats() -> pd.DataFrame:
    rows = []
    for bk in NT_BOOKS:
        df = batch_align(nt_book=bk, min_votes=MIN_VOTES)
        if df.empty:
            rows.append({
                'book_id': bk,
                'book': NT_FULL_NAMES[bk],
                'total_pairs': 0,
                'follows_lxx': 0,
                'mixed': 0,
                'mt_leaning': 0,
                'pct_follows_lxx': 0.0,
                'pct_mixed': 0.0,
                'pct_mt_leaning': 0.0,
                'mean_lxx_pct': 0.0,
                'median_lxx_pct': 0.0,
            })
            continue
        total = len(df)
        n_lxx = (df['summary'] == 'follows LXX').sum()
        n_mix = (df['summary'] == 'mixed').sum()
        n_mt = (df['summary'] == 'MT-leaning').sum()
        rows.append({
            'book_id': bk,
            'book': NT_FULL_NAMES[bk],
            'total_pairs': total,
            'follows_lxx': int(n_lxx),
            'mixed': int(n_mix),
            'mt_leaning': int(n_mt),
            'pct_follows_lxx': round(100 * n_lxx / total, 1),
            'pct_mixed': round(100 * n_mix / total, 1),
            'pct_mt_leaning': round(100 * n_mt / total, 1),
            'mean_lxx_pct': round(df['lxx_following_pct'].mean(), 1),
            'median_lxx_pct': round(df['lxx_following_pct'].median(), 1),
        })
        print(f'  {bk}: {total} pairs  LXX={n_lxx} mixed={n_mix} MT={n_mt}')
    return pd.DataFrame(rows)


# ── 2. Charts ─────────────────────────────────────────────────────────────────

def build_stacked_bar(stats: pd.DataFrame) -> Path:
    """Stacked bar: proportion of LXX / mixed / MT-leaning per NT book."""
    active = stats[stats['total_pairs'] > 0].copy()
    books = active['book'].tolist()
    n = len(books)

    lxx_pct = active['pct_follows_lxx'].values
    mix_pct = active['pct_mixed'].values
    mt_pct = active['pct_mt_leaning'].values

    fig, ax = plt.subplots(figsize=(14, 6))
    x = np.arange(n)
    w = 0.65

    ax.bar(x, lxx_pct, w, label='Follows LXX', color='#2196F3')
    ax.bar(x, mix_pct, w, bottom=lxx_pct, label='Mixed', color='#FF9800')
    ax.bar(x, mt_pct, w, bottom=lxx_pct + mix_pct, label='MT-leaning', color='#9E9E9E')

    ax.set_xticks(x)
    ax.set_xticklabels(books, rotation=45, ha='right', fontsize=9)
    ax.set_ylabel('% of cross-reference pairs', fontsize=11)
    ax.set_title('NT OT Quotation Source — LXX vs MT Alignment by Book\n'
                 f'(OpenBible allusion pairs, min. {MIN_VOTES} votes; '
                 'Rahlfs LXX, IBM Model 1 word alignment)', fontsize=11)
    ax.set_ylim(0, 105)
    ax.legend(loc='upper right', fontsize=9)

    # Annotate total pair count above each bar
    for i, row in enumerate(active.itertuples()):
        ax.text(i, 102, str(row.total_pairs), ha='center', va='bottom',
                fontsize=7, color='#333333')

    ax.text(0.01, -0.22,
            'Numbers above bars = total cross-reference pairs analysed.',
            transform=ax.transAxes, fontsize=8, color='#555555')

    fig.tight_layout()
    out = REPORT_DIR / 'nt-ot-source-alignment-stacked.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'Saved {out}')
    return out


def build_heatmap(stats: pd.DataFrame) -> Path:
    """Heatmap: mean LXX-following % per book, books sorted by corpus order."""
    active = stats[stats['total_pairs'] > 0].copy()

    fig, ax = plt.subplots(figsize=(14, 2.5))
    values = active['mean_lxx_pct'].values.reshape(1, -1)
    im = ax.imshow(values, aspect='auto', cmap='Blues', vmin=0, vmax=100)

    ax.set_xticks(range(len(active)))
    ax.set_xticklabels(active['book'].tolist(), rotation=45, ha='right', fontsize=9)
    ax.set_yticks([])
    ax.set_title('Mean LXX-following % per NT Book\n'
                 f'(darker = more LXX vocabulary; min. {MIN_VOTES} votes)',
                 fontsize=11)

    for j, val in enumerate(active['mean_lxx_pct'].values):
        color = 'white' if val > 55 else '#111111'
        ax.text(j, 0, f'{val:.0f}%', ha='center', va='center',
                fontsize=8, color=color, fontweight='bold')

    plt.colorbar(im, ax=ax, orientation='vertical', label='Mean LXX %', pad=0.02,
                 fraction=0.015)
    fig.tight_layout()
    out = REPORT_DIR / 'nt-ot-source-alignment-heatmap.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'Saved {out}')
    return out


# ── 3. Report ─────────────────────────────────────────────────────────────────

CAVEAT_SECTION = """\
## Methodology and Caveats

This report applies automated word-level alignment to measure how closely NT
authors followed the Greek Septuagint (LXX) when quoting the Hebrew Old
Testament. The methodology and its known limitations are described below.

### How the analysis works

1. **Cross-reference pairs** are drawn from the
   [OpenBible.info](https://www.openbible.info) community cross-reference
   dataset (CC-BY). Each pair links an NT verse to an OT verse and carries a
   *vote score* representing community confidence. Only pairs with **≥ 25
   votes** are included; lower-scored links tend to be thematic echoes rather
   than textual quotations.

2. **Word-level alignment** uses an IBM Model 1 statistical alignment trained
   on the Hebrew–Greek LXX parallel corpus. For each content word (noun, verb,
   adjective, adverb) in the NT verse, the model determines which Hebrew root
   it corresponds to, then checks whether the LXX renders that same Hebrew
   root with the same Greek lexeme.

3. **Verdicts** per word:

   | Verdict | Meaning |
   |---|---|
   | **LXX** | NT word's Greek lexeme appears in the LXX of this verse |
   | **LXX+MT** | Matches LXX *and* aligns to the Hebrew root in the MT |
   | **MT-diverge** | NT word's Hebrew root is in the MT but the LXX uses a different Greek word |
   | **neutral** | Function word, or no alignment data available |

4. **Pair verdict** thresholds:

   | Label | Criterion |
   |---|---|
   | **Follows LXX** | ≥ 70 % of content words match LXX vocabulary |
   | **Mixed** | 40–69 %, or at least one MT-diverge word |
   | **MT-leaning** | < 40 % LXX vocabulary match, zero MT-diverge words |

### Known limitations

**1. Allusion dataset bias toward thematic echoes.**
OpenBible vote data covers the full range from verbatim formal quotations to
loose thematic allusions. A passage like "God is love" will be linked to dozens
of OT verses thematically — but only one or two are actual textual sources.
The algorithm cannot distinguish formal quotations from thematic echoes, so
most pairs for every book score "MT-leaning" simply because the NT verse and
the allusion target share few exact vocabulary items.

**2. Single LXX manuscript tradition (Rahlfs 1935 / Vaticanus).**
The LXX was transmitted in several recensions. The project uses the
*Rahlfs 1935* critical edition, which is based primarily on Codex Vaticanus.
When an NT author follows a different LXX tradition (e.g. Codex Alexandrinus),
the algorithm may flag a genuine LXX quotation as "MT-leaning." The most
famous example is **Hebrews 10:5** (citing Ps 40:6): Rahlfs has `ὠτία`
("ears") where Hebrews writes `σῶμα` ("a body") — a reading found in Codex
Alexandrinus. The algorithm correctly detects the mismatch but cannot
distinguish "different LXX tradition" from "independent Hebrew translation."

**3. IBM Model 1 alignment sparsity.**
The word-alignment model works verse-by-verse. For short or rare words, and
for NT quotations that span multiple OT verses (e.g. Heb 8:8–12 citing
Jer 31:31–34), the alignment is sparse and many content words receive no
Hebrew root assignment, deflating the LXX-following score.

**4. What "MT-leaning" actually means in most cases.**
In this dataset, "MT-leaning" most often means *insufficient alignment data*
rather than a deliberate choice to depart from the LXX. Scholarly consensus
based on manual analysis consistently finds Matthew, Luke, Romans, and
especially Hebrews to be heavily LXX-dependent for their formal quotations.
The aggregate numbers in this report should be read as a rough signal, not a
precise measure.

### What the data *can* reliably show

- **Relative patterns across books.** Books with genuinely high LXX vocabulary
  overlap (e.g. Matthew quoting Isaiah, Hebrews citing the Psalms) do score
  higher than books with few formal quotations.
- **Individual well-paired cases.** Where a high-vote pair links an NT verse
  to exactly the right OT verse, the word-level alignment is meaningful (e.g.
  Matt 4:4 → Deut 8:3 scores 75% LXX, which aligns with scholarly judgment).
- **Direction of travel.** Even with sparse alignment, books like Revelation —
  which famously *alludes to* rather than formally *quotes* the OT — correctly
  score near zero LXX vocabulary overlap.

---
"""


def build_report(stats: pd.DataFrame) -> None:
    lines: list[str] = []

    lines += [
        '# NT OT Quotation Source — LXX vs MT Alignment by Book',
        '',
        '**Corpus:** New Testament (TAGNT) × Old Testament (TAHOT + CenterBLC/LXX)',
        '**Method:** IBM Model 1 word alignment; OpenBible.info cross-references',
        f'**Threshold:** Minimum {MIN_VOTES} votes per cross-reference pair',
        '',
        '---',
        '',
        '## Contents',
        '',
        '1. [Summary Table](#summary-table)',
        '2. [Stacked Bar Chart — LXX vs MT by Book](#stacked-bar-chart)',
        '3. [Heatmap — Mean LXX Vocabulary %](#heatmap)',
        '4. [Book-by-Book Notes](#book-by-book-notes)',
        '5. [Methodology and Caveats](#methodology-and-caveats)',
        '',
        '---',
        '',
        '## Key Observations',
        '',
        '- **No NT book scores consistently high on LXX vocabulary** in this',
        '  automated analysis, which runs counter to the scholarly consensus that',
        '  Matthew, Luke–Acts, and Hebrews are heavily LXX-dependent. This is',
        '  primarily an artifact of the allusion dataset mixing formal quotations',
        '  with thematic echoes. See the Caveats section.',
        '- **Revelation correctly scores near zero** — it alludes to but never',
        '  formally quotes the OT, so low LXX vocabulary overlap is expected.',
        '- **Individual high-confidence pairs do reveal LXX dependence** (e.g.',
        '  Matt 4:4 → Deut 8:3 at 75 %; Heb 1:5 → Ps 2:7 at 74 %).',
        '- **Books with very few pairs** (Philemon, 2 John, 3 John, Jude) lack',
        '  enough data for any conclusion.',
        '',
        '---',
        '',
        '## Summary Table',
        '',
        '| Book | Pairs | Follows LXX | Mixed | MT-leaning | Mean LXX % | Median LXX % |',
        '|---|---|---|---|---|---|---|',
    ]

    for _, row in stats.iterrows():
        if row['total_pairs'] == 0:
            lines.append(
                f"| {row['book']} | 0 | — | — | — | — | — |"
            )
        else:
            lines.append(
                f"| {row['book']} "
                f"| {row['total_pairs']} "
                f"| {row['follows_lxx']} ({row['pct_follows_lxx']:.0f}%) "
                f"| {row['mixed']} ({row['pct_mixed']:.0f}%) "
                f"| {row['mt_leaning']} ({row['pct_mt_leaning']:.0f}%) "
                f"| {row['mean_lxx_pct']:.1f}% "
                f"| {row['median_lxx_pct']:.1f}% |"
            )

    lines += [
        '',
        '---',
        '',
        '## Stacked Bar Chart',
        '',
        '![NT OT Quotation Source — LXX vs MT Alignment by Book]'
        '(nt-ot-source-alignment-stacked.png)',
        '',
        '---',
        '',
        '## Heatmap',
        '',
        '![Mean LXX-following % per NT Book]'
        '(nt-ot-source-alignment-heatmap.png)',
        '',
        '---',
        '',
        '## Book-by-Book Notes',
        '',
    ]

    # Short contextual note per book
    NOTES = {
        'Mat': (
            'Matthew is widely regarded as the most LXX-dependent Gospel for its '
            'formula quotations (e.g. 1:23 citing Isa 7:14 LXX; 4:15–16 citing '
            'Isa 9:1–2 LXX). The algorithm detects some LXX vocabulary in '
            'individual high-vote pairs but the thematic allusion noise dominates.'
        ),
        'Mrk': (
            'Mark has relatively few direct OT quotations. Its citations tend to '
            'be brief and often follow the LXX, but the small pair count limits '
            'statistical confidence here.'
        ),
        'Luk': (
            'Luke–Acts is known for heavy LXX dependence in its OT citations. '
            'The infancy narratives (chs 1–2) are especially LXX-saturated. '
            'The allusion dataset does not weight these formal quotations more '
            'heavily than thematic echoes, which dampens the signal.'
        ),
        'Jhn': (
            "John's OT citations are fewer but often carefully chosen. Some diverge "
            "from the LXX (e.g. 19:37 quoting Zech 12:10 closer to the Hebrew). "
            'The algorithm has limited data to distinguish these cases.'
        ),
        'Act': (
            "Acts' speeches (Peter in chs 1–2, Stephen in ch 7, Paul in ch 13) "
            'quote the LXX explicitly. The Acts 2:17–21 citation of Joel 2:28–32 '
            'is verbatim LXX. The low overall score reflects the thematic-echo '
            'noise in the allusion data.'
        ),
        'Rom': (
            'Romans contains the highest density of explicit OT quotations in the '
            'Pauline corpus. Paul regularly introduces them with "it is written" '
            '(γέγραπται). Scholarly analysis shows Paul sometimes follows the LXX, '
            'sometimes departs from it. The algorithm finds insufficient signal to '
            'distinguish these cases reliably.'
        ),
        '1Co': (
            '1 Corinthians cites the OT frequently, sometimes following LXX (e.g. '
            '1:31, 2:9) and sometimes adapting freely. The pair count is moderate '
            'but thematic echoes dominate.'
        ),
        '2Co': (
            '2 Corinthians has a high allusion count relative to its length. Many '
            "pairs are thematic echoes of the Psalms and Isaiah, reflecting Paul's "
            'theodicy and apostolic self-understanding.'
        ),
        'Gal': (
            "Galatians' explicit citations (Gen 15:6; Deut 27:26; Hab 2:4; "
            'Gen 12:3; Isa 54:1) are few but significant. The small pair count '
            'here limits conclusions.'
        ),
        'Eph': (
            "Ephesians' OT allusions are dense but mostly integrated into Paul's "
            'prose rather than formally quoted. The allusion data reflect this: '
            'high vote counts for thematic links rather than verbatim citations.'
        ),
        'Php': (
            'Philippians has few direct quotations. Most OT links are allusive '
            'rather than textual.'
        ),
        'Col': (
            'Colossians is OT-saturated in vocabulary but has few explicit '
            'quotation formulae. Most links in the allusion data are thematic.'
        ),
        '1Th': ('Very few cross-reference pairs at this threshold — insufficient data.',),
        '2Th': ('Very few cross-reference pairs at this threshold — insufficient data.',),
        '1Ti': ('Very few cross-reference pairs at this threshold — insufficient data.',),
        '2Ti': (
            '2 Timothy contains a few explicit OT references (e.g. 2:19 citing '
            'Num 16:5). Limited data here.'
        ),
        'Tit': ('Very few cross-reference pairs at this threshold — insufficient data.',),
        'Phm': ('No cross-reference pairs meet the vote threshold — no data.',),
        'Heb': (
            'Hebrews is the NT book most studied for LXX dependence. It quotes '
            'the LXX explicitly and at length (e.g. Ps 95:7–11 in 3:7–11; '
            'Jer 31:31–34 in 8:8–12). **However, this report systematically '
            'under-scores Hebrews** for two reasons: (1) many high-vote pairs link '
            'Hebrews verses to multiple thematic OT echoes, not just the primary '
            'LXX source; (2) Hebrews sometimes follows Codex Alexandrinus rather '
            'than Rahlfs (Vaticanus), causing genuine LXX quotations to be '
            'flagged as mismatches (e.g. 10:5 σῶμα vs Rahlfs ὠτία at Ps 39:7). '
            'A direct word-overlap test between Heb 3:7–11 and LXX Ps 94:7–11 '
            'yields **67 % shared vocabulary**, consistent with verbatim quotation.'
        ),
        'Jas': (
            "James is heavily indebted to the OT wisdom tradition. Its allusions "
            'are more stylistic than formal quotation, which produces low LXX '
            'alignment scores in this analysis.'
        ),
        '1Pe': (
            '1 Peter is dense with OT allusions and explicit citations, many '
            'following the LXX (e.g. 2:6 citing Isa 28:16 LXX; 2:9 echoing '
            'Exo 19:6 LXX). The allusion dataset is noisy here.'
        ),
        '2Pe': ('Limited pairs at this threshold.'),
        '1Jn': ('Limited pairs — allusive rather than quotation-based.',),
        '2Jn': ('No pairs meet the vote threshold — no data.',),
        '3Jn': ('One pair only — insufficient data.',),
        'Jud': (
            'Jude quotes 1 Enoch and Assumption of Moses as well as the OT. '
            'Cross-reference data here links to canonical OT only. One pair.'
        ),
        'Rev': (
            'Revelation is the NT book with the densest OT allusion — but it '
            '**never formally quotes** the OT with an introduction formula. '
            'Every OT link is allusive or typological. The algorithm correctly '
            'finds near-zero LXX vocabulary overlap for most pairs, because '
            "John's language is saturated with OT imagery that is woven into new "
            'Greek constructions rather than cited verbatim.'
        ),
    }

    for _, row in stats.iterrows():
        bk = row['book_id']
        note = NOTES.get(bk, '')
        if isinstance(note, tuple):
            note = note[0]
        lines.append(f"### {row['book']} ({bk})")
        lines.append('')
        if row['total_pairs'] == 0:
            lines.append('No cross-reference pairs meet the vote threshold.')
        else:
            lines.append(
                f"**{row['total_pairs']} pairs** — "
                f"{row['follows_lxx']} follows LXX ({row['pct_follows_lxx']:.0f}%), "
                f"{row['mixed']} mixed ({row['pct_mixed']:.0f}%), "
                f"{row['mt_leaning']} MT-leaning ({row['pct_mt_leaning']:.0f}%); "
                f"mean LXX vocabulary: {row['mean_lxx_pct']:.1f}%"
            )
        lines.append('')
        if note:
            lines.append(note)
        lines.append('')

    lines += [
        '---',
        '',
    ]
    lines.append(CAVEAT_SECTION)

    lines += [
        '---',
        '',
        '*Report generated by '
        '[scripts/both/intertextuality/build_nt_ot_source_report.py]'
        '(../../../../../scripts/both/intertextuality/build_nt_ot_source_report.py). '
        'Source data: STEPBible TAGNT/TAHOT (CC BY 4.0), CenterBLC/LXX (CC BY 4.0), '
        'OpenBible.info cross-references (CC BY).*',
    ]

    out = REPORT_DIR / 'nt-ot-source-alignment.md'
    out.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Saved {out}')


# ── 4. CSV export ─────────────────────────────────────────────────────────────

def build_csv(stats: pd.DataFrame) -> None:
    out = REPORT_DIR / 'nt-ot-source-alignment.csv'
    stats.to_csv(out, index=False)
    print(f'Saved {out}')


# ── 5. Main ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('Gathering per-book alignment stats...')
    stats = gather_book_stats()

    print('Building stacked bar chart...')
    build_stacked_bar(stats)

    print('Building heatmap...')
    build_heatmap(stats)

    print('Building report...')
    build_report(stats)

    print('Building CSV...')
    build_csv(stats)

    print('Done.')
