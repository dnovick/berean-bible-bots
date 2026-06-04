"""Build NT and LXX Greek Personal Pronouns report.

Covers the full personal pronoun system:
  1st person: ἐγώ / ἡμεῖς (I / we)
  2nd person: σύ / ὑμεῖς (you sg / you pl)
  3rd person: αὐτός, αὐτή, αὐτό (he / she / it) with full gender paradigm
  Reflexives: ἐμαυτοῦ, σεαυτοῦ, ἑαυτοῦ

Outputs:
  output/reports/nt/lexicon/greek-pronouns/greek-pronouns-report.md
  output/reports/nt/lexicon/greek-pronouns/pronouns-nt-distribution.png
  output/reports/nt/lexicon/greek-pronouns/pronouns-lxx-distribution.png
  output/reports/nt/lexicon/greek-pronouns/pronouns-nt-by-book.png
  output/reports/nt/lexicon/greek-pronouns/pronouns-case-breakdown.png
  output/reports/nt/lexicon/greek-pronouns/greek-pronouns.csv
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.patches as mpatches  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, '.')
from src.bible_grammar.core import db as _db  # noqa: E402

REPORT_DIR = Path('output/reports/nt/lexicon/greek-pronouns')
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────────────

_words = _db.load()
_lxx = _db.load_lxx()
_trans = _db.load_translations()
_kjv = _trans[_trans['translation'] == 'KJV']

nt = _words[_words['source'] == 'TAGNT'].copy()
lxx_canon = _lxx[~_lxx['is_deuterocanon']].copy()


def kjv_text(book: str, ch: int, vs: int) -> str:
    r = _kjv[
        (_kjv['book_id'] == book) & (_kjv['chapter'] == ch) &
        (_kjv['verse'] == vs)
    ]
    t = r['text'].values[0] if len(r) else ''
    return (t[:115] + '…') if len(t) > 115 else t


# ── Pronoun groupings ─────────────────────────────────────────────────────────

# TAGNT uses G3165 for all non-nominative 1st-person forms (μου/μοι/με/ἡμῶν…)
# and G1473 for ἐγώ nominative; G4771 covers all 2nd-person forms.

P1_STRONGS = {'G1473', 'G3165'}   # 1st person (sg + pl)
P2_STRONGS = {'G4771'}             # 2nd person (sg + pl)
P3_STRONGS = {'G0846'}             # αὐτός (3rd person + intensive + identical)
REFL_STRONGS = {'G1683', 'G4572', 'G1438'}  # reflexives

NT_BOOK_ORDER = [
    'Mat', 'Mrk', 'Luk', 'Jhn', 'Act',
    'Rom', '1Co', '2Co', 'Gal', 'Eph', 'Php', 'Col',
    '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm',
    'Heb', 'Jas', '1Pe', '2Pe', '1Jn', '2Jn', '3Jn', 'Jud', 'Rev',
]
NT_BOOK_NAMES = {
    'Mat': 'Matthew', 'Mrk': 'Mark', 'Luk': 'Luke', 'Jhn': 'John',
    'Act': 'Acts', 'Rom': 'Romans', '1Co': '1 Cor', '2Co': '2 Cor',
    'Gal': 'Galatians', 'Eph': 'Ephesians', 'Php': 'Philippians',
    'Col': 'Colossians', '1Th': '1 Thess', '2Th': '2 Thess',
    '1Ti': '1 Tim', '2Ti': '2 Tim', 'Tit': 'Titus', 'Phm': 'Philemon',
    'Heb': 'Hebrews', 'Jas': 'James', '1Pe': '1 Peter', '2Pe': '2 Peter',
    '1Jn': '1 John', '2Jn': '2 John', '3Jn': '3 John', 'Jud': 'Jude',
    'Rev': 'Revelation',
}
OT_BOOK_NAMES = {
    'Gen': 'Genesis', 'Exo': 'Exodus', 'Lev': 'Leviticus', 'Num': 'Numbers',
    'Deu': 'Deuteronomy', 'Jos': 'Joshua', 'Jdg': 'Judges', 'Rut': 'Ruth',
    '1Sa': '1 Sam', '2Sa': '2 Sam', '1Ki': '1 Kgs', '2Ki': '2 Kgs',
    '1Ch': '1 Chr', '2Ch': '2 Chr', 'Ezr': 'Ezra', 'Neh': 'Nehemiah',
    'Est': 'Esther', 'Job': 'Job', 'Psa': 'Psalms', 'Pro': 'Proverbs',
    'Ecc': 'Ecclesiastes', 'Sng': 'Song', 'Isa': 'Isaiah', 'Jer': 'Jeremiah',
    'Lam': 'Lamentations', 'Ezk': 'Ezekiel', 'Dan': 'Daniel', 'Hos': 'Hosea',
    'Jol': 'Joel', 'Amo': 'Amos', 'Mic': 'Micah', 'Nah': 'Nahum',
    'Hab': 'Habakkuk', 'Zep': 'Zephaniah', 'Hag': 'Haggai', 'Zec': 'Zechariah',
    'Mal': 'Malachi',
}

PERSON_COLORS = {
    '1st person': '#2166ac',
    '2nd person': '#d6604d',
    '3rd person (αὐτός)': '#4dac26',
    'Reflexive': '#8856a7',
}

CASE_ORDER = ['Nominative', 'Genitive', 'Dative', 'Accusative']
CASE_COLORS = {
    'Nominative': '#1a6faf',
    'Genitive':   '#e07b39',
    'Dative':     '#2a9d2a',
    'Accusative': '#c44040',
}


# ── Chart helpers ─────────────────────────────────────────────────────────────

def _save(fig: plt.Figure, name: str) -> Path:
    out = REPORT_DIR / name
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Chart: {out}')
    return out


# ── Chart 1: NT overall distribution bar ─────────────────────────────────────

def chart_nt_distribution() -> Path:
    p1 = len(nt[nt['strongs'].isin(P1_STRONGS)])
    p2 = len(nt[nt['strongs'].isin(P2_STRONGS)])
    p3 = len(nt[nt['strongs'].isin(P3_STRONGS)])
    rf = len(nt[nt['strongs'].isin(REFL_STRONGS)])

    labels = ['1st person\n(ἐγώ/ἡμεῖς)',
              '2nd person\n(σύ/ὑμεῖς)',
              '3rd person\n(αὐτός)',
              'Reflexive\n(ἑαυτοῦ etc.)']
    values = [p1, p2, p3, rf]
    colors = [PERSON_COLORS[k] for k in PERSON_COLORS]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(labels, values, color=colors, alpha=0.9, width=0.55)
    for bar, v in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 60,
                f'{v:,}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax.set_ylabel('NT Occurrences')
    ax.set_title('Greek Personal Pronouns — NT Occurrence by Person',
                 fontsize=11, fontweight='bold')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))
    plt.tight_layout()
    return _save(fig, 'pronouns-nt-distribution.png')


# ── Chart 2: NT by book (stacked, top 15 books) ──────────────────────────────

def chart_nt_by_book() -> Path:
    groups = {
        '1st person': P1_STRONGS,
        '2nd person': P2_STRONGS,
        '3rd person (αὐτός)': P3_STRONGS,
    }
    books_hit: set[str] = set()
    data: dict[str, dict[str, int]] = {g: {} for g in groups}

    for grp, strongs in groups.items():
        for book, cnt in nt[nt['strongs'].isin(strongs)].groupby('book_id').size().items():
            data[grp][book] = int(cnt)
            books_hit.add(book)

    # Top 15 books by total pronouns
    totals = {b: sum(data[g].get(b, 0) for g in groups) for b in books_hit}
    top_books = sorted(totals, key=lambda b: -totals[b])[:15]
    # Keep canonical order among top books
    books = [b for b in NT_BOOK_ORDER if b in top_books]
    labels = [NT_BOOK_NAMES.get(b, b) for b in books]

    x = np.arange(len(books))
    width = 0.65
    fig, ax = plt.subplots(figsize=(13, 5))
    bottom = np.zeros(len(books))
    for grp in groups:
        vals = [data[grp].get(b, 0) for b in books]
        ax.bar(x, vals, width, bottom=bottom,
               label=grp, color=PERSON_COLORS[grp], alpha=0.9)
        bottom += np.array(vals, dtype=float)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=8.5)
    ax.set_ylabel('Occurrences')
    ax.set_title('Personal Pronouns by NT Book (Top 15) — Stacked by Person',
                 fontsize=11, fontweight='bold')
    ax.legend(fontsize=9, loc='upper right')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{int(v):,}'))
    plt.tight_layout()
    return _save(fig, 'pronouns-nt-by-book.png')


# ── Chart 3: Case breakdown per person ───────────────────────────────────────

def chart_case_breakdown() -> Path:
    persons = [
        ('1st sg', nt[nt['strongs'].isin(P1_STRONGS) & (nt['number'] == 'Singular')]),
        ('1st pl', nt[nt['strongs'].isin(P1_STRONGS) & (nt['number'] == 'Plural')]),
        ('2nd sg', nt[nt['strongs'].isin(P2_STRONGS) & (nt['number'] == 'Singular')]),
        ('2nd pl', nt[nt['strongs'].isin(P2_STRONGS) & (nt['number'] == 'Plural')]),
        ('3rd αὐτός\n(all)', nt[nt['strongs'].isin(P3_STRONGS)]),
    ]

    fig, axes = plt.subplots(1, 5, figsize=(14, 4.5), sharey=False)
    for ax, (label, sub) in zip(axes, persons):
        case_ct = sub.groupby('case_').size()
        vals = [case_ct.get(c, 0) for c in CASE_ORDER]
        colors = [CASE_COLORS[c] for c in CASE_ORDER]
        bars = ax.bar(CASE_ORDER, vals, color=colors, alpha=0.9)
        for bar, v in zip(bars, vals):
            if v > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, v + 5,
                        str(v), ha='center', va='bottom', fontsize=7.5)
        ax.set_title(label, fontsize=9, fontweight='bold')
        ax.set_xticks(range(4))
        ax.set_xticklabels(['Nom', 'Gen', 'Dat', 'Acc'], fontsize=8)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{int(v):,}'))

    # Add legend
    patches = [mpatches.Patch(color=CASE_COLORS[c], label=c) for c in CASE_ORDER]
    fig.legend(handles=patches, loc='lower center', ncol=4,
               fontsize=8.5, bbox_to_anchor=(0.5, -0.05))
    fig.suptitle('NT Personal Pronouns — Case Breakdown by Person/Number',
                 fontsize=11, fontweight='bold')
    plt.tight_layout(rect=[0, 0.06, 1, 1])
    return _save(fig, 'pronouns-case-breakdown.png')


# ── Chart 4: LXX distribution (1st + 2nd person) ────────────────────────────

def chart_lxx_distribution() -> Path:
    p1_lxx = lxx_canon[lxx_canon['strongs'].isin({'G1473', 'G3165'})]
    p2_lxx = lxx_canon[lxx_canon['strongs'].isin({'G4771'})]

    # Top 10 books each
    def top_books(sub: pd.DataFrame, n: int = 10) -> pd.Series:
        return sub.groupby('book_id').size().sort_values(ascending=False).head(n)

    p1_top = top_books(p1_lxx)
    p2_top = top_books(p2_lxx)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5))
    for ax, series, color, title in [
        (ax1, p1_top, PERSON_COLORS['1st person'], '1st Person (ἐγώ/ἡμεῖς) — LXX Canonical'),
        (ax2, p2_top, PERSON_COLORS['2nd person'], '2nd Person (σύ/ὑμεῖς) — LXX Canonical'),
    ]:
        labels = [OT_BOOK_NAMES.get(b, b) for b in series.index]
        bars = ax.bar(range(len(labels)), series.values, color=color, alpha=0.9)
        for bar, v in zip(bars, series.values):
            ax.text(bar.get_x() + bar.get_width() / 2, v + 2,
                    str(v), ha='center', va='bottom', fontsize=8)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=8.5)
        ax.set_title(title, fontsize=9, fontweight='bold')
        ax.set_ylabel('Occurrences')

    plt.tight_layout()
    return _save(fig, 'pronouns-lxx-distribution.png')


# ── Report ────────────────────────────────────────────────────────────────────

def build_report() -> Path:

    p1_total = len(nt[nt['strongs'].isin(P1_STRONGS)])
    p2_total = len(nt[nt['strongs'].isin(P2_STRONGS)])
    p3_total = len(nt[nt['strongs'].isin(P3_STRONGS)])
    rf_total = len(nt[nt['strongs'].isin(REFL_STRONGS)])
    grand_total = p1_total + p2_total + p3_total + rf_total

    p1_lxx = len(lxx_canon[lxx_canon['strongs'].isin({'G1473', 'G3165'})])
    p2_lxx = len(lxx_canon[lxx_canon['strongs'].isin({'G4771'})])
    rf_lxx = len(lxx_canon[lxx_canon['strongs'].isin({'G1438'})])

    lines = [
        '# Greek Personal Pronouns — NT and LXX Study',
        '',
        '**Corpus:** NT Greek (TAGNT) · LXX Greek (canonical books)  ',
        '**Translation:** KJV',
        '',
        '## Contents',
        '',
        '- [Overview](#overview)',
        '- [Key Observations](#key-observations)',
        '- [Complete Paradigms](#complete-paradigms)',
        '  - [1st Person — ἐγώ / ἡμεῖς](#1st-person--ἐγώ--ἡμεῖς)',
        '  - [2nd Person — σύ / ὑμεῖς](#2nd-person--σύ--ὑμεῖς)',
        '  - [3rd Person — αὐτός αὐτή αὐτό](#3rd-person--αὐτός-αὐτή-αὐτό)',
        '  - [Reflexive Pronouns](#reflexive-pronouns)',
        '- [Distribution Charts](#distribution-charts)',
        '- [NT Occurrence by Book](#nt-occurrence-by-book)',
        '- [LXX Distribution](#lxx-distribution)',
        '- [Case Breakdown](#case-breakdown)',
        '- [Key Passages](#key-passages)',
        '- [Summary Table](#summary-table)',
        '',
        '---',
        '',
        '## Overview',
        '',
        'Greek has a **rich personal pronoun system** covering three persons, two numbers '
        '(singular and plural), and — for the third person — three genders. Unlike Hebrew, '
        'Greek verbs already encode person/number in their endings, so personal pronouns '
        'are **used for emphasis, contrast, or disambiguation** rather than as a grammatical '
        'requirement. When an author writes ἐγὼ instead of simply using the verbal ending, '
        'the pronoun adds **rhetorical weight**.',
        '',
        f'**NT total personal pronoun tokens:** {grand_total:,}  ',
        f'**LXX canonical (1st + 2nd person):** {p1_lxx + p2_lxx:,}',
        '',
        '---',
        '',
        '## Key Observations',
        '',
        f'- **αὐτός dominates the NT** ({p3_total:,} tokens, '
        f'{p3_total / grand_total * 100:.0f}% of all personal pronoun tokens). '
        'It functions as the standard 3rd-person pronoun across all genders and numbers. '
        'In its genitive and dative forms (αὐτοῦ, αὐτῷ, αὐτοῖς) it is the workhorse '
        'of narrative reference — especially in the Gospels.',
        '',
        f'- **2nd person σύ/ὑμεῖς** ({p2_total:,} NT tokens) appears more than 1st person '
        f'({p1_total:,}) in absolute terms, reflecting the dialogical nature of the Gospels '
        'and Epistles. Jesus\'s direct address to disciples, crowds, and opponents drives '
        'the count.',
        '',
        '- **Nominative case is emphatic.** Greek verbs already encode person; a pronoun '
        'in the nominative reinforces or contrasts the subject. John\'s "**ἐγώ** εἰμι" '
        'sayings (8:12, 8:58, 10:7, 11:25, 14:6, 15:1, 15:5, 18:5–6) are the most '
        'theologically charged uses of the 1st-person nominative in the NT.',
        '',
        '- **Genitive is the most common case** for all personal pronouns — as possessives '
        '(μου, σου, αὐτοῦ) they modify nouns throughout the NT. The genitive of αὐτός '
        'alone (αὐτοῦ/αὐτῆς/αὐτῶν) accounts for over 2,000 tokens.',
        '',
        '- **LXX 1st-person concentration in Psalms and the Prophets.** The Psalms have the '
        'highest density of 1st-person pronouns (prayer/lament idiom); Ezekiel and Jeremiah '
        'carry heavy divine 1st-person speech. This differs from the NT where the Gospels '
        'and Acts dominate.',
        '',
        '- **ἑαυτοῦ (reflexive)** has 331 NT tokens and 655 LXX canonical tokens. '
        'In the NT it covers all three persons reflexively (himself/herself/itself/themselves). '
        'The specific first- and second-person reflexives (ἐμαυτοῦ, σεαυτοῦ) have '
        'negligible NT use but are attested in the LXX.',
        '',
        '---',
        '',
        '## Complete Paradigms',
        '',
        '### 1st Person — ἐγώ / ἡμεῖς',
        '',
        'The first-person pronoun has no gender distinction. The emphatic oblique forms '
        '(ἐμοῦ/ἐμοί/ἐμέ) are stressed alternatives to the enclitic forms (μου/μοι/με).',
        '',
        '| Case | Singular | Emphatic sg | Plural |',
        '|---|---|---|---|',
        '| **Nominative** | ἐγώ | — | ἡμεῖς |',
        '| **Genitive** | μου *(enclitic)* | ἐμοῦ *(emphatic)* | ἡμῶν |',
        '| **Dative** | μοι *(enclitic)* | ἐμοί *(emphatic)* | ἡμῖν |',
        '| **Accusative** | με *(enclitic)* | ἐμέ *(emphatic)* | ἡμᾶς |',
        '',
        '**NT occurrence counts:**',
        '',
        '| Form | Case | NT count |',
        '|---|---|---:|',
    ]

    p1_sg = nt[nt['strongs'].isin(P1_STRONGS) & (nt['number'] == 'Singular')]
    p1_pl = nt[nt['strongs'].isin(P1_STRONGS) & (nt['number'] == 'Plural')]
    for df_sub, label in [(p1_sg, 'sg'), (p1_pl, 'pl')]:
        for case in CASE_ORDER:
            ct = len(df_sub[df_sub['case_'] == case])
            if ct > 0:
                forms = df_sub[df_sub['case_'] == case]['word'].value_counts().head(2).index.tolist()
                clean = [f.rstrip('.,;:·¶') for f in forms]
                lines.append(f'| {" / ".join(clean)} | {case} {label} | {ct:,} |')

    lines += [
        '',
        '---',
        '',
        '### 2nd Person — σύ / ὑμεῖς',
        '',
        'The second-person pronoun also has no gender distinction. '
        'The forms σου/σοι/σε are enclitic (unstressed); they appear far more '
        'frequently than the nominative σύ since Greek verbs already mark 2nd person.',
        '',
        '| Case | Singular | Plural |',
        '|---|---|---|',
        '| **Nominative** | σύ | ὑμεῖς |',
        '| **Genitive** | σου | ὑμῶν |',
        '| **Dative** | σοι | ὑμῖν |',
        '| **Accusative** | σε | ὑμᾶς |',
        '',
        '**NT occurrence counts:**',
        '',
        '| Form | Case | NT count |',
        '|---|---|---:|',
    ]

    p2_sg = nt[nt['strongs'].isin(P2_STRONGS) & (nt['number'] == 'Singular')]
    p2_pl = nt[nt['strongs'].isin(P2_STRONGS) & (nt['number'] == 'Plural')]
    for df_sub, label in [(p2_sg, 'sg'), (p2_pl, 'pl')]:
        for case in CASE_ORDER:
            ct = len(df_sub[df_sub['case_'] == case])
            if ct > 0:
                forms = df_sub[df_sub['case_'] == case]['word'].value_counts().head(2).index.tolist()
                clean = [f.rstrip('.,;:·¶') for f in forms]
                lines.append(f'| {" / ".join(clean)} | {case} {label} | {ct:,} |')

    lines += [
        '',
        '---',
        '',
        '### 3rd Person — αὐτός αὐτή αὐτό',
        '',
        'αὐτός is a **three-gender pronoun** with full case and number inflection. '
        'It serves three distinct functions in the NT:',
        '',
        '1. **Personal pronoun** (most common) — "he/she/it/they" in oblique cases',
        '2. **Intensive adjective** — nominative case, meaning "himself/herself/itself/themselves"',
        '3. **Identical adjective** — attributive position, meaning "the same"',
        '',
        '| Case | Masc. Sg | Fem. Sg | Neut. Sg | Masc. Pl | Fem. Pl | Neut. Pl |',
        '|---|---|---|---|---|---|---|',
        '| **Nominative** | αὐτός | αὐτή | αὐτό | αὐτοί | αὐταί | αὐτά |',
        '| **Genitive** | αὐτοῦ | αὐτῆς | αὐτοῦ | αὐτῶν | αὐτῶν | αὐτῶν |',
        '| **Dative** | αὐτῷ | αὐτῇ | αὐτῷ | αὐτοῖς | αὐταῖς | αὐτοῖς |',
        '| **Accusative** | αὐτόν | αὐτήν | αὐτό | αὐτούς | αὐτάς | αὐτά |',
        '',
        '> **Note:** Masc./Neut. share Gen/Dat forms; Gen/Pl is αὐτῶν for all genders.',
        '',
        '**NT occurrence counts:**',
        '',
        '| Form | Gender | Case | Number | NT count |',
        '|---|---|---|---|---:|',
    ]

    p3 = nt[nt['strongs'] == 'G0846']
    by_gnc = p3.groupby(['gender', 'number', 'case_']).size().reset_index(name='n')
    gen_order = ['Masculine', 'Feminine', 'Neuter']
    num_order = ['Singular', 'Plural']
    for gender in gen_order:
        for number in num_order:
            for case in CASE_ORDER:
                sub = by_gnc[
                    (by_gnc['gender'] == gender) & (by_gnc['number'] == number) &
                    (by_gnc['case_'] == case)
                ]
                if len(sub) == 0:
                    continue
                ct = sub['n'].values[0]
                form_df = p3[
                    (p3['gender'] == gender) & (p3['number'] == number) &
                    (p3['case_'] == case)
                ]
                form = form_df['word'].value_counts().index[0].rstrip('.,;:·¶') if len(form_df) else ''
                lines.append(f'| {form} | {gender} | {case} | {number} | {ct:,} |')

    lines += [
        '',
        '---',
        '',
        '### Reflexive Pronouns',
        '',
        'Greek has dedicated reflexive pronouns for each person. In the NT, '
        'ἑαυτοῦ (3rd person) does duty for all three persons reflexively.',
        '',
        '| Pronoun | Strongs | Meaning | NT | LXX (canonical) |',
        '|---|---|---|---:|---:|',
        f'| ἐμαυτοῦ | G1683 | myself | {len(nt[nt["strongs"]=="G1683"]):,} | {len(lxx_canon[lxx_canon["strongs"]=="G1683"]):,} |',  # noqa: E225 E501
        f'| σεαυτοῦ | G4572 | yourself | {len(nt[nt["strongs"]=="G4572"]):,} | {len(lxx_canon[lxx_canon["strongs"]=="G4572"]):,} |',  # noqa: E225 E501
        f'| ἑαυτοῦ | G1438 | himself/herself/themselves | {len(nt[nt["strongs"]=="G1438"]):,} | {len(lxx_canon[lxx_canon["strongs"]=="G1438"]):,} |',  # noqa: E225 E501
        '',
        '> **ἑαυτοῦ paradigm:** Gen sg ἑαυτοῦ/ἑαυτῆς · Dat sg ἑαυτῷ/ἑαυτῇ · '
        'Acc sg ἑαυτόν/ἑαυτήν · Gen pl ἑαυτῶν · Dat pl ἑαυτοῖς · Acc pl ἑαυτούς/ἑαυτάς. '
        'No nominative exists (the reflexive always refers back to the subject).',
        '',
        '---',
        '',
        '## Distribution Charts',
        '',
        '![NT overall distribution](pronouns-nt-distribution.png)',
        '',
        '---',
        '',
        '## NT Occurrence by Book',
        '',
        '![NT by book](pronouns-nt-by-book.png)',
        '',
        '---',
        '',
        '## LXX Distribution',
        '',
        '![LXX distribution](pronouns-lxx-distribution.png)',
        '',
        '---',
        '',
        '## Case Breakdown',
        '',
        '![Case breakdown](pronouns-case-breakdown.png)',
        '',
        '---',
        '',
        '## Key Passages',
        '',
        '### ἐγώ εἰμι — The "I am" Sayings of Jesus',
        '',
        'The combination ἐγώ εἰμι carries enormous theological weight in John\'s Gospel. '
        'The emphatic nominative ἐγώ (rather than simply εἰμι alone) evokes the LXX '
        'rendering of Exodus 3:14 (ἐγώ εἰμι ὁ ὤν, "I am the one who is") and '
        'Isaiah 43:10 (ἐγώ εἰμι, "I am he").',
        '',
        '| Reference | KJV |',
        '|---|---|',
    ]

    i_am_refs = [
        ('Jhn', 8, 58), ('Jhn', 6, 35), ('Jhn', 8, 12),
        ('Jhn', 10, 7), ('Jhn', 10, 11), ('Jhn', 11, 25),
        ('Jhn', 14, 6), ('Jhn', 15, 1),
    ]
    for bk, ch, vs in i_am_refs:
        lines.append(f'| {NT_BOOK_NAMES.get(bk, bk)} {ch}:{vs} | {kjv_text(bk, ch, vs)} |')

    lines += [
        '',
        '### αὐτός — Intensive Use',
        '',
        'When αὐτός appears in the **nominative** case without a preceding article, '
        'it intensifies the subject: "he himself," "she herself."',
        '',
        '| Reference | KJV |',
        '|---|---|',
    ]

    intensive_refs = [
        ('Jhn', 2, 25), ('Luk', 24, 36), ('Mat', 8, 24),
        ('Jhn', 4, 2), ('1Jn', 2, 6),
    ]
    for bk, ch, vs in intensive_refs:
        lines.append(f'| {NT_BOOK_NAMES.get(bk, bk)} {ch}:{vs} | {kjv_text(bk, ch, vs)} |')

    lines += [
        '',
        '### σύ/ὑμεῖς — Direct Address',
        '',
        '| Reference | KJV |',
        '|---|---|',
    ]

    direct_refs = [
        ('Mat', 16, 15), ('Jhn', 21, 17), ('Mat', 5, 48),
        ('Luk', 22, 70), ('Jhn', 10, 30),
    ]
    for bk, ch, vs in direct_refs:
        lines.append(f'| {NT_BOOK_NAMES.get(bk, bk)} {ch}:{vs} | {kjv_text(bk, ch, vs)} |')

    lines += [
        '',
        '---',
        '',
        '## Summary Table',
        '',
        '| Pronoun | Strongs | Person | NT tokens | LXX (canonical) | Notes |',
        '|---|---|---|---:|---:|---|',
        f'| ἐγώ | G1473 | 1st sg (nom) | {len(nt[nt["strongs"]=="G1473"]):,} | {len(lxx_canon[lxx_canon["strongs"]=="G1473"]):,} | Emphatic nominative |',  # noqa: E225 E501
        f'| μου/μοι/με | G3165 | 1st sg+pl (obl) | {len(nt[nt["strongs"]=="G3165"]):,} | {len(lxx_canon[lxx_canon["strongs"]=="G3165"]):,} | Enclitic + plural forms |',  # noqa: E225 E501
        f'| σύ/σου/σοι/σε | G4771 | 2nd sg+pl | {len(nt[nt["strongs"]=="G4771"]):,} | {len(lxx_canon[lxx_canon["strongs"]=="G4771"]):,} | All 2nd person forms |',  # noqa: E225 E501
        f'| αὐτός | G0846 | 3rd (all genders) | {p3_total:,} | — | Pronoun + intensive + identical |',
        f'| ἑαυτοῦ | G1438 | Reflexive (all persons) | {rf_total:,} | {rf_lxx:,} | No nominative form |',
        '',
        '---',
        '',
        '*Greek NT data: TAGNT (Byzantine/Textus Receptus, STEPBible CC BY 4.0).*  ',
        '*LXX data: CenterBLC LXX (CC BY 4.0).*  ',
        '*Generated by [scripts/nt/lexicon/build_greek_pronouns_report.py]'
        '(../../../../scripts/nt/lexicon/build_greek_pronouns_report.py).*',
    ]

    out = REPORT_DIR / 'greek-pronouns-report.md'
    out.write_text('\n'.join(lines), encoding='utf-8')
    print(f'  Report: {out}')
    return out


def build_csv() -> Path:
    rows = []
    for strongs, person, grp in [
        ('G1473', '1st', '1st person'), ('G3165', '1st', '1st person'),
        ('G4771', '2nd', '2nd person'), ('G0846', '3rd', '3rd person (αὐτός)'),
        ('G1438', 'Refl', 'Reflexive'), ('G1683', 'Refl', 'Reflexive'),
        ('G4572', 'Refl', 'Reflexive'),
    ]:
        sub = nt[nt['strongs'] == strongs]
        for _, r in sub[['book_id', 'chapter', 'verse', 'word', 'case_', 'gender', 'number']].iterrows():
            rows.append({
                'strongs': strongs, 'person': person, 'group': grp,
                'book': r['book_id'], 'chapter': r['chapter'], 'verse': r['verse'],
                'word': r['word'], 'case': r['case_'],
                'gender': r['gender'], 'number': r['number'],
            })
    out = REPORT_DIR / 'greek-pronouns.csv'
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f'  CSV: {out}')
    return out


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('Building charts...')
    chart_nt_distribution()
    chart_nt_by_book()
    chart_case_breakdown()
    chart_lxx_distribution()

    print('Building report...')
    build_report()

    print('Building CSV...')
    build_csv()

    print('Done.')
