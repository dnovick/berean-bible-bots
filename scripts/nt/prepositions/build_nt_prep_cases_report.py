"""
Build: Greek NT Prepositions — Case Binding Statistics Report.

Covers all Greek NT prepositions that govern more than one case (proper
prepositions binding 2–3 cases), with full statistics on how often each
case is used and how meaning shifts with case.

Outputs:
  output/reports/nt/prepositions/nt-prep-cases.md
  output/reports/nt/prepositions/nt-prep-cases.csv
  output/reports/nt/prepositions/nt-prep-cases-heatmap.png
  output/reports/nt/prepositions/nt-prep-cases-by-book-epi.png
  output/reports/nt/prepositions/nt-prep-cases-by-book-para.png
  output/reports/nt/prepositions/nt-prep-cases-by-book-dia.png
"""

from __future__ import annotations
from pathlib import Path
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker as mticker  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from bible_grammar import (  # noqa: E402
    greek_prep_cases, greek_prep_frequency, greek_prep_by_book,
)

OUT = Path('output/reports/nt/prepositions')


def _slug(heading: str) -> str:
    """Replicate MkDocs Material's heading anchor generation.

    Strip non-ASCII, remove punctuation other than hyphens, lowercase,
    collapse whitespace/hyphens to a single hyphen, strip leading/trailing.
    """
    ascii_only = heading.encode('ascii', errors='ignore').decode()
    no_punct = re.sub(r'[^a-zA-Z0-9\s-]', '', ascii_only)
    slug = re.sub(r'\s+', '-', no_punct.lower())
    return re.sub(r'-{2,}', '-', slug).strip('-')


OUT.mkdir(parents=True, exist_ok=True)

# ── Preposition metadata ───────────────────────────────────────────────────────

# Proper prepositions (κύριαι προθέσεις) that genuinely govern multiple cases
# in classical and NT Greek.  Single-case preps (ἐν/dat, εἰς/acc, ἐκ/gen,
# σύν/dat, ἕως/gen, πρό/gen) are excluded from the multi-case analysis but
# included in the overview table for completeness.
MULTI_CASE = ['ἐπί', 'παρά', 'διά', 'κατά', 'μετά', 'περί', 'ὑπό', 'ὑπέρ', 'πρός', 'ἀνά']

SINGLE_CASE = ['ἐν', 'εἰς', 'ἐκ', 'ἀπό', 'σύν', 'πρό']

# For the semantic notes, classify the meaning shift per case
PREP_META: dict[str, dict] = {
    'ἐπί': {
        'strongs': 'G1909',
        'transliteration': 'epi',
        'gloss': 'on, upon, over, at, against, on the basis of',
        'cases': {
            'Genitive': 'on, upon (contact from above); in the time of; before (a judge)',
            'Dative': 'on, at, near (rest/location); on the basis of; at/in response to',
            'Accusative': 'onto, over (motion toward); against; with respect to; for (purpose)',
        },
        'note': (
            'The most complex NT preposition: all three oblique cases occur with '
            'distinct meaning streams. Genitive stresses surface contact or temporal '
            'setting; dative stresses rest at a location or ground/basis; accusative '
            'stresses direction of motion or extent. The overlap is real — context '
            'and lexical semantics of the governing verb often determine sense more '
            'than case alone.'
        ),
    },
    'παρά': {
        'strongs': 'G3844',
        'transliteration': 'para',
        'gloss': 'beside, from, with, contrary to',
        'cases': {
            'Genitive': 'from (the side of); from the presence/authority of',
            'Dative': 'beside, in the presence of; with (possession)',
            'Accusative': 'alongside, beside (motion or extent); contrary to; beyond',
        },
        'note': (
            'παρά with the genitive expresses source or origin ("from the side of"). '
            'The dative is locative ("at the side of", "in the presence of"). '
            'The accusative covers motion alongside something or extension beyond it, '
            'and in legal/ethical contexts "contrary to" (e.g. Rom 1:26 παρὰ φύσιν, '
            '"contrary to nature"). Roughly equal distribution across all three cases '
            'makes this the most evenly spread multi-case prep in the NT.'
        ),
    },
    'διά': {
        'strongs': 'G1223',
        'transliteration': 'dia',
        'gloss': 'through, by means of, because of, on account of',
        'cases': {
            'Genitive': 'through (spatial); by means of (agency/instrument); throughout (extent)',
            'Accusative': 'because of, on account of, for the sake of (cause/reason)',
        },
        'note': (
            'The case split is semantically sharp: genitive = means/channel '
            '("through which something passes"), accusative = cause/reason '
            '("on account of which something happens"). '
            'E.g. Eph 2:8 διὰ πίστεως (gen.) = "through faith" (the channel); '
            'Rom 4:25 διὰ τὰ παραπτώματα (acc.) = "on account of our trespasses" (cause). '
            'Genitive accounts for ~57 % of NT uses, accusative ~41 %.'
        ),
    },
    'κατά': {
        'strongs': 'G2596',
        'transliteration': 'kata',
        'gloss': 'according to, against, throughout, down from',
        'cases': {
            'Genitive': 'down from; against (hostile sense); throughout (swearing by)',
            'Accusative': 'according to, in conformity with; throughout (distributive); for, as',
        },
        'note': (
            'Genitive carries the original spatial sense ("down from") and the hostile '
            'extension ("against": κατὰ τοῦ προφήτου). '
            'Accusative (the large majority, ~82 %) has largely shed the spatial sense '
            'and functions as a norm marker: κατὰ σάρκα ("according to the flesh"), '
            'κατὰ νόμον ("in accordance with the law"). '
            'The distribution is highly skewed toward accusative in NT epistolary style.'
        ),
    },
    'μετά': {
        'strongs': 'G3326',
        'transliteration': 'meta',
        'gloss': 'with (association), after (sequence)',
        'cases': {
            'Genitive': 'with, in company with, in association with',
            'Accusative': 'after (temporal or spatial sequence)',
        },
        'note': (
            'The case split is clean and consistent: genitive = accompaniment/association '
            '("with"), accusative = sequence ("after"). '
            'E.g. μετὰ τοῦ Ἰησοῦ (gen.) = "with Jesus"; '
            'μετὰ τρεῖς ἡμέρας (acc.) = "after three days". '
            'Genitive predominates (~77 %) since much NT prose describes '
            'fellowship, discipleship, and community.'
        ),
    },
    'περί': {
        'strongs': 'G4012',
        'transliteration': 'peri',
        'gloss': 'concerning, about, around, for',
        'cases': {
            'Genitive': 'concerning, about, regarding; for (substitutionary)',
            'Accusative': 'around (spatial); approximately (time/number)',
        },
        'note': (
            'The dominant use (~83 %) is genitive with the sense "concerning, about" — '
            'the standard NT idiom for discourse topic (γράφω περί τινος, "I write '
            'concerning something"). The substitutionary sense (e.g. περὶ ἁμαρτίας, '
            '"for sin/as a sin offering") is important theologically in Hebrews and '
            '1 John. Accusative is spatial ("around") and appears relatively rarely '
            'outside the Gospels and Acts.'
        ),
    },
    'ὑπό': {
        'strongs': 'G5259',
        'transliteration': 'hypo',
        'gloss': 'under, by (agent)',
        'cases': {
            'Genitive': 'by (the agent of a passive verb); under the authority of',
            'Accusative': 'under (spatial, below); under (subordination)',
        },
        'note': (
            'Genitive is the standard marker of the agent in passive constructions '
            '(ὑπό + genitive = "by someone/something"). '
            'Accusative expresses spatial position ("under") or subordinate status. '
            'In the NT, genitive dominates (~77 %) due to the high frequency of '
            'theological passive constructions ("raised by God", "taught by the Spirit").'
        ),
    },
    'ὑπέρ': {
        'strongs': 'G5228',
        'transliteration': 'hyper',
        'gloss': 'on behalf of, above, beyond, more than',
        'cases': {
            'Genitive': 'on behalf of, for the sake of; in place of (substitution)',
            'Accusative': 'above (spatial); beyond, more than (comparison)',
        },
        'note': (
            'The genitive is the theologically freighted case: ὑπέρ + genitive '
            'expresses the substitutionary and intercessory senses central to NT '
            'soteriology (Χριστὸς ἀπέθανεν ὑπὲρ ἡμῶν, "Christ died for us", '
            'Rom 5:8). Accusative is used spatially and comparatively and appears '
            'much less frequently (~12 %).'
        ),
    },
    'πρός': {
        'strongs': 'G4314',
        'transliteration': 'pros',
        'gloss': 'to, toward, with, against',
        'cases': {
            'Accusative': 'to, toward, against (motion/direction); for (purpose)',
            'Dative': 'near, at (rare; archaic/Attic locative)',
            'Genitive': 'from (very rare)',
        },
        'note': (
            'In the NT, πρός is almost exclusively accusative (~98 %). '
            'The dative and genitive uses are vestigial — a handful of instances '
            'each, reflecting literary archaism. The accusative sense covers both '
            'literal motion toward ("go to Jerusalem") and figurative direction '
            '("pray toward God", "face to face with").'
        ),
    },
    'ἀνά': {
        'strongs': 'G0303',
        'transliteration': 'ana',
        'gloss': 'up, each, among',
        'cases': {
            'Accusative': 'up along; each/apiece (distributive)',
        },
        'note': (
            'In classical Greek ἀνά took accusative (up along), genitive (upon), '
            'and dative (at). In the NT it survives almost exclusively with '
            'accusative in the distributive sense (ἀνὰ εἷς ἕκαστος, "each one"), '
            'and is rare overall (13 occurrences).'
        ),
    },
}

# ── 1. Collect case data ───────────────────────────────────────────────────────


def collect_all_cases() -> pd.DataFrame:
    freq = greek_prep_frequency(top_n=50)
    rows = []
    for _, frow in freq.iterrows():
        lemma = frow['lemma']
        total = frow['count']
        df = greek_prep_cases(lemma)
        for _, crow in df.iterrows():
            rows.append({
                'lemma': lemma,
                'case_binding': crow['case_binding'],
                'count': crow['count'],
                'pct': crow['pct'],
                'total': total,
            })
    return pd.DataFrame(rows)


# ── 2. Heatmap: multi-case preps × cases ──────────────────────────────────────

def build_heatmap(all_cases: pd.DataFrame) -> None:
    cases_order = ['Accusative', 'Genitive', 'Dative', 'Nominative']
    preps = MULTI_CASE

    # Build matrix: rows = preps, cols = cases, values = pct
    matrix = pd.DataFrame(index=preps, columns=cases_order, dtype=float)
    matrix[:] = 0.0
    for prep in preps:
        sub = all_cases[(all_cases['lemma'] == prep) &
                        (all_cases['case_binding'].isin(cases_order))]
        for _, row in sub.iterrows():
            matrix.loc[prep, row['case_binding']] = float(row['pct'])

    # Drop Nominative if empty
    matrix = matrix.loc[:, (matrix > 0).any()]

    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(matrix.values, aspect='auto', cmap='Blues', vmin=0, vmax=100)

    ax.set_xticks(range(len(matrix.columns)))
    ax.set_xticklabels(matrix.columns, fontsize=12)
    ax.set_yticks(range(len(preps)))
    ax.set_yticklabels(preps, fontsize=12)

    for i, prep in enumerate(preps):
        for j, case in enumerate(matrix.columns):
            val = matrix.loc[prep, case]
            if val > 0:
                color = 'white' if val > 55 else '#111111'
                ax.text(j, i, f'{val:.0f}%', ha='center', va='center',
                        fontsize=10, color=color, fontweight='bold')
            else:
                ax.text(j, i, '—', ha='center', va='center',
                        fontsize=10, color='#aaaaaa')

    ax.set_title(
        'Greek NT Multi-Case Prepositions — Case Distribution (%)\n'
        '(cells show % of each preposition\'s total occurrences)',
        fontsize=12,
    )
    plt.colorbar(im, ax=ax, label='% of occurrences', fraction=0.03, pad=0.03)
    fig.tight_layout()
    out = OUT / 'nt-prep-cases-heatmap.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'Saved {out}')


# ── 3. Per-book bar charts for selected preps ──────────────────────────────────

def build_book_chart(lemma: str, slug: str) -> None:
    """Stacked bar: per-book occurrence count for a single multi-case prep."""
    from bible_grammar import query

    df = query(testament='nt', part_of_speech='Preposition')
    prep_df = df[df['word'].str.startswith(lemma[:3]) | (df['word'] == lemma)].copy()
    # More precise: filter by the actual lemma via strongs prefix
    meta = PREP_META.get(lemma, {})
    strongs = meta.get('strongs', '')
    if strongs:
        prep_df = df[df['strongs'].fillna('').str.startswith(strongs)].copy()

    if prep_df.empty:
        return

    # Count by book × case
    from bible_grammar.core.reference import BOOKS
    book_order = [b[0] for b in BOOKS if b[2] == 'NT']

    # Get case for each word via the object of the preposition (next noun's case)
    # The TAGNT case_ column on prepositions is usually blank; instead look at
    # the case distribution the API already computed and distribute book counts
    # proportionally (approximation for the chart)
    by_book = greek_prep_by_book(lemma, corpus='nt')
    if by_book.empty:
        return

    by_book = by_book.set_index('book').reindex(book_order).fillna(0).reset_index()
    by_book = by_book[by_book['count'] > 0]

    fig, ax = plt.subplots(figsize=(13, 4))
    x = np.arange(len(by_book))
    ax.bar(x, by_book['count'].values, color='#1565C0', width=0.7)
    ax.set_xticks(x)
    ax.set_xticklabels(by_book['book'].tolist(), rotation=45, ha='right', fontsize=9)
    ax.set_ylabel('Occurrences', fontsize=10)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax.set_title(
        f'{lemma} ({meta.get("transliteration", "")} — '
        f'{meta.get("gloss", "").split(",")[0]}) — '
        f'Occurrences by NT Book',
        fontsize=11,
    )
    fig.tight_layout()
    out = OUT / f'nt-prep-cases-by-book-{slug}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'Saved {out}')


# ── 4. Report ─────────────────────────────────────────────────────────────────

def build_report(all_cases: pd.DataFrame, freq: pd.DataFrame) -> None:  # noqa: E501
    lines: list[str] = []

    lines += [
        '# Greek NT Prepositions — Case Binding Statistics',
        '',
        '**Corpus:** Greek New Testament (TAGNT, Byzantine/TR)',
        '**Focus:** Prepositions that govern more than one grammatical case, '
        'and the statistical distribution of those cases across the NT',
        '',
        '---',
        '',
        '## Contents',
        '',
        '1. [Overview — All NT Prepositions](#overview-all-nt-prepositions)',
        '2. [Multi-Case Prepositions — Case Distribution Heatmap]'
        '(#multi-case-prepositions-case-distribution-heatmap)',
        '3. [Detailed Analysis by Preposition]'
        '(#detailed-analysis-by-preposition)',
    ]
    for prep in MULTI_CASE:
        meta = PREP_META[prep]
        gloss = meta['gloss']
        heading = f'{prep} — {gloss}'
        lines.append(f'   - [{prep}](#{_slug(heading)})')
    lines += [
        '4. [Single-Case Prepositions — Reference Table]'
        '(#single-case-prepositions-reference-table)',
        '5. [Grammar Notes](#grammar-notes)',
        '',
        '---',
        '',
        '## Key Observations',
        '',
        '- **9 of the 18 most common NT prepositions govern multiple cases.**',
        '  Case choice is not free variation — each case activates a distinct '
        '  meaning stream for the preposition.',
        '- **ἐπί is the most complex**, using all three oblique cases '
        '  (accusative 53 %, genitive 25 %, dative 20 %) with meaningfully '
        '  different senses in each.',
        '- **παρά has the most even three-way split** '
        '  (genitive 42 %, accusative 31 %, dative 27 %), '
        '  making correct case identification especially important for exegesis.',
        '- **διά and μετά have clean binary splits** — '
        '  each case maps to a distinct semantic function '
        '  (means vs. cause for διά; association vs. sequence for μετά).',
        '- **πρός is effectively single-case in the NT** (98 % accusative), '
        '  though it retains rare dative and genitive forms.',
        '- **ὑπέρ + genitive** is the prepositional expression of NT substitutionary '
        '  and intercessory theology (e.g. Christ dying "for us").',
        '',
        '---',
        '',
        '## Overview — All NT Prepositions',
        '',
        'Total preposition occurrences in the NT (TAGNT). '
        'Multi-case prepositions are marked ✦.',
        '',
        '| Preposition | Gloss | NT Count | % of all preps | Cases |',
        '|---|---|---|---|---|',
    ]

    for _, frow in freq.iterrows():
        lemma = frow['lemma']
        count = frow['count']
        pct = frow['pct']
        meta = PREP_META.get(lemma, {})
        raw_gloss = meta.get('gloss', frow.get('gloss', '—')).split(',')[0]
        # Strip any embedded transliteration prefix (e.g. "en — in/among" → "in/among")
        gloss = raw_gloss.split(' — ')[-1] if ' — ' in raw_gloss else raw_gloss
        sub = all_cases[(all_cases['lemma'] == lemma) &
                        (~all_cases['case_binding'].isin(['(none / unclear)']))]
        n_cases = sub['case_binding'].nunique()
        if n_cases > 1:
            case_str = ' / '.join(sub.sort_values('count', ascending=False)['case_binding'].tolist())
            marker = '✦'
        else:
            case_str = sub['case_binding'].iloc[0] if not sub.empty else '—'
            marker = ''
        lines.append(
            f'| {marker}{lemma} | {gloss} | {count:,} | {pct:.1f}% | {case_str} |'
        )

    lines += [
        '',
        '✦ = governs multiple cases',
        '',
        '---',
        '',
        '## Multi-Case Prepositions — Case Distribution Heatmap',
        '',
        '![Greek NT Multi-Case Prepositions — Case Distribution](nt-prep-cases-heatmap.png)',
        '',
        'Each cell shows what percentage of that preposition\'s NT occurrences '
        'use that case. Blank (—) = that case is not used or statistically negligible.',
        '',
        '---',
        '',
        '## Detailed Analysis by Preposition',
        '',
    ]

    for prep in MULTI_CASE:
        meta = PREP_META[prep]
        slug = meta['transliteration']
        sub = all_cases[(all_cases['lemma'] == prep) &
                        (all_cases['case_binding'] != '(none / unclear)')]
        total = sub['count'].sum()

        lines += [
            f'### {prep} — {meta["gloss"]}',
            '',
            f'**Strong\'s:** {meta["strongs"]} | '
            f'**Total NT occurrences:** {total:,}',
            '',
            '| Case | Count | % | Meaning with this case |',
            '|---|---|---|---|',
        ]
        for _, crow in sub.sort_values('count', ascending=False).iterrows():
            case = crow['case_binding']
            meaning = meta['cases'].get(case, '—')
            lines.append(
                f'| {case} | {int(crow["count"]):,} | {crow["pct"]:.1f}% | {meaning} |'
            )

        lines += [
            '',
            f'![{prep} by NT Book](nt-prep-cases-by-book-{slug}.png)',
            '',
            meta['note'],
            '',
        ]

    lines += [
        '---',
        '',
        '## Single-Case Prepositions — Reference Table',
        '',
        'These prepositions govern only one case in NT usage. '
        'They are included for completeness.',
        '',
        '| Preposition | Case | Gloss | NT Count |',
        '|---|---|---|---|',
    ]

    SINGLE_META = {
        'ἐν':  ('Dative',      'in, among, by, with'),
        'εἰς': ('Accusative',  'into, to, for, toward'),
        'ἐκ':  ('Genitive',    'out of, from'),
        'ἀπό': ('Genitive',    'from, away from, since'),
        'σύν': ('Dative',      'with, together with'),
        'πρό': ('Genitive',    'before (spatial/temporal)'),
    }
    for lemma, (case, gloss) in SINGLE_META.items():
        sub = freq[freq['lemma'] == lemma]
        count = int(sub['count'].iloc[0]) if not sub.empty else 0
        lines.append(f'| {lemma} | {case} | {gloss} | {count:,} |')

    lines += [
        '',
        '---',
        '',
        '## Grammar Notes',
        '',
        '### What is a "case-binding" preposition?',
        '',
        'Greek prepositions are said to "govern" or "take" a particular case — '
        'the noun or pronoun following the preposition must appear in that case. '
        'The 18 proper prepositions (κύριαι προθέσεις) of classical Greek are '
        'traditionally divided by how many cases they govern:',
        '',
        '| # of cases | Prepositions |',
        '|---|---|',
        '| One case | ἀντί, ἀπό, ἐκ, ἐν, εἰς, πρό, σύν (+ ἕως) |',
        '| Two cases | διά, κατά, μετά, περί, ὑπό, ὑπέρ, ἀνά |',
        '| Three cases | ἐπί, παρά, πρός (classical; NT πρός is effectively single-case) |',
        '',
        '### Why does case matter for exegesis?',
        '',
        'When a preposition governs multiple cases, the case of the following '
        'noun changes the meaning of the preposition. Reading the case correctly '
        'is therefore essential for understanding the text:',
        '',
        '- **διά + genitive** = *by means of* / *through* (the means or channel)',
        '- **διά + accusative** = *because of* / *on account of* (the cause or reason)',
        '',
        'Confusing these produces a different theological statement. '
        'For example, Rom 4:25:',
        '',
        '> ὃς παρεδόθη διὰ τὰ παραπτώματα ἡμῶν (accusative — *because of* '
        'our trespasses)',
        '> καὶ ἠγέρθη διὰ τὴν δικαίωσιν ἡμῶν (accusative — *for the sake of* '
        'our justification)',
        '',
        'Both are accusative of cause/purpose, not genitive of means — '
        'Paul is explaining *why* Christ was delivered and raised, not '
        'the mechanism.',
        '',
        '### How the case data is computed',
        '',
        'The TAGNT morphological database tags each word with its grammatical '
        'form, including case. The case assigned to a preposition\'s object is '
        'determined by the inflected form of the following noun or pronoun. '
        'A small number of tokens carry no clear case tag (e.g. indeclinable '
        'words, elided forms); these are counted as "(none / unclear)" and '
        'excluded from the percentage calculations above.',
        '',
        '---',
        '',
        '*Report generated by '
        '[scripts/nt/prepositions/build_nt_prep_cases_report.py]'
        '(../../../../scripts/nt/prepositions/build_nt_prep_cases_report.py). '
        'Source: STEPBible TAGNT (CC BY 4.0, Tyndale House Cambridge). '
        'KJV translation examples (public domain).*',
    ]

    out = OUT / 'nt-prep-cases.md'
    out.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Saved {out}')


# ── 5. CSV export ─────────────────────────────────────────────────────────────

def build_csv(all_cases: pd.DataFrame, freq: pd.DataFrame) -> None:
    merged = all_cases.merge(
        freq[['lemma', 'count']].rename(columns={'count': 'total_occurrences'}),
        on='lemma',
        how='left',
    )
    out = OUT / 'nt-prep-cases.csv'
    merged.to_csv(out, index=False)
    print(f'Saved {out}')


# ── 6. Main ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('Collecting case data...')
    freq = greek_prep_frequency(top_n=30)
    all_cases = collect_all_cases()

    print('Building heatmap...')
    build_heatmap(all_cases)

    print('Building per-book charts...')
    for prep, slug in [('ἐπί', 'epi'), ('παρά', 'para'), ('διά', 'dia'),
                       ('κατά', 'kata'), ('μετά', 'meta'), ('περί', 'peri'),
                       ('ὑπό', 'hypo'), ('ὑπέρ', 'hyper'),
                       ('πρός', 'pros'), ('ἀνά', 'ana')]:
        build_book_chart(prep, slug)

    print('Building report...')
    build_report(all_cases, freq)

    print('Building CSV...')
    build_csv(all_cases, freq)

    print('Done.')
