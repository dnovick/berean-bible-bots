"""
Christological titles: frequency analysis of titles Jesus used to refer to Himself.

IMPORTANT — speaker attribution caveat
───────────────────────────────────────
The STEPBible TAGNT data does not tag speakers. This module therefore counts
*all* occurrences of each title pattern in the Gospels (and Acts/Epistles where
relevant), not only instances where Jesus is the speaker or referent.

For most titles this is a minor caveat:
  • "Son of Man" — every instance in the Gospels is Jesus speaking of Himself.
  • Johannine "I AM" sayings — all are Jesus speaking.
  • "Son of God" — also used by demons, the high priest, the centurion; ~30%
    of occurrences are NOT Jesus self-referential.
  • "Son of David" — almost entirely crowds/petitioners addressing Jesus,
    not self-reference.
  • "Lord" / "Christ" — too broad; included for completeness with caveats.

The `self_ref_confidence` field in each title record documents the reliability.

Pattern strategy
────────────────
Each title is matched by requiring that a set of Strong's numbers ALL appear
in the same verse (verse-level co-occurrence).  This is conservative — it may
miss a verse where the title is split across very long sentences, but it avoids
false positives from phrase-search windowing across sentence boundaries.

Usage
─────
from bible_grammar.names.christological_titles import (
    title_counts, print_title_counts, title_report,
    TITLE_REGISTRY,
)

# Terminal table
print_title_counts()

# With NT epistles included
print_title_counts(scope='NT')

# Markdown report
title_report(output_dir='output/reports')
"""

from __future__ import annotations
import pandas as pd
from pathlib import Path

# ── Title registry ────────────────────────────────────────────────────────────
#
# Each entry:
#   label            : display name
#   strongs          : list of Strong's numbers that must ALL appear in the same verse
#   greek            : Greek phrase
#   notes            : concise description / caveat
#   self_ref_confidence : 'high' | 'medium' | 'low'
#   scope            : 'gospels' | 'NT' (books to search)
#   group            : grouping for report sections

TITLE_REGISTRY: list[dict] = [
    # ── Son of Man ─────────────────────────────────────────────────────────
    {
        'label':  'Son of Man',
        'strongs': ['G5207', 'G0444'],
        'greek':  'ὁ υἱὸς τοῦ ἀνθρώπου',
        'notes':  'Jesus\'s most frequent self-designation. Every Gospel instance is '
                  'Jesus speaking. One instance each in Acts (7:56, Stephen\'s vision) '
                  'and Rev (1:13, 14:14) extend the pattern.',
        'self_ref_confidence': 'high',
        'scope':  'NT',
        'group':  'Son titles',
    },

    # ── Son of God ─────────────────────────────────────────────────────────
    {
        'label':  'Son of God',
        'strongs': ['G5207', 'G2316'],
        'greek':  'υἱὸς τοῦ θεοῦ',
        'notes':  'Used both by Jesus (implicitly) and by others — demons (Mt 8:29), '
                  'disciples (Mt 14:33), the high priest (Mt 26:63), the centurion '
                  '(Mt 27:54). Counts include all speakers.',
        'self_ref_confidence': 'medium',
        'scope':  'NT',
        'group':  'Son titles',
    },

    # ── Son of the Father ──────────────────────────────────────────────────
    {
        'label':  'Son / the Father',
        'strongs': ['G5207', 'G3962'],
        'greek':  'ὁ υἱός … ὁ πατήρ',
        'notes':  'Verses where both "Son" and "Father" appear — captures Jesus\'s '
                  '"I and the Father…" and "the Son does what the Father does" discourse '
                  '(esp. John). Includes some third-person references.',
        'self_ref_confidence': 'medium',
        'scope':  'gospels',
        'group':  'Son titles',
    },

    # ── Son of David ───────────────────────────────────────────────────────
    {
        'label':  'Son of David',
        'strongs': ['G5207', 'G1138'],
        'greek':  'υἱὸς Δαυίδ',
        'notes':  'Predominantly crowds and petitioners addressing Jesus, not '
                  'self-reference. Included to show messianic address frequency. '
                  'Absent from John.',
        'self_ref_confidence': 'low',
        'scope':  'gospels',
        'group':  'Son titles',
    },

    # ── I AM — absolute ───────────────────────────────────────────────────
    {
        'label':  'I AM (absolute)',
        'strongs': ['G1473', 'G1510'],
        'greek':  'ἐγώ εἰμι',
        'notes':  'Absolute "I am he / it is I" — includes Jhn 8:58 ("before Abraham '
                  'was, I AM"), the arrest scene (Jhn 18:5–8), and walking-on-water '
                  'pericopes. Also catches non-theological ego+eimi uses. '
                  'High concentration in John.',
        'self_ref_confidence': 'medium',
        'scope':  'gospels',
        'group':  'I AM sayings',
    },

    # ── Johannine I AM predicate sayings ──────────────────────────────────
    {
        'label':  'I AM — Bread of Life',
        'strongs': ['G1473', 'G1510', 'G0740'],
        'greek':  'ἐγώ εἰμι ὁ ἄρτος τῆς ζωῆς',
        'notes':  'John 6:35, 41, 48, 51. All Jesus speaking.',
        'self_ref_confidence': 'high',
        'scope':  'gospels',
        'group':  'I AM sayings',
    },
    {
        'label':  'I AM — Light of the World',
        'strongs': ['G1473', 'G1510', 'G5457'],
        'greek':  'ἐγώ εἰμι τὸ φῶς τοῦ κόσμου',
        'notes':  'John 8:12. Jesus speaking.',
        'self_ref_confidence': 'high',
        'scope':  'gospels',
        'group':  'I AM sayings',
    },
    {
        'label':  'I AM — the Door / Gate',
        'strongs': ['G1473', 'G1510', 'G2374'],
        'greek':  'ἐγώ εἰμι ἡ θύρα',
        'notes':  'John 10:7, 9. Jesus speaking.',
        'self_ref_confidence': 'high',
        'scope':  'gospels',
        'group':  'I AM sayings',
    },
    {
        'label':  'I AM — the Good Shepherd',
        'strongs': ['G1473', 'G1510', 'G4166'],
        'greek':  'ἐγώ εἰμι ὁ ποιμὴν ὁ καλός',
        'notes':  'John 10:11, 14. Jesus speaking.',
        'self_ref_confidence': 'high',
        'scope':  'gospels',
        'group':  'I AM sayings',
    },
    {
        'label':  'I AM — the Resurrection',
        'strongs': ['G1473', 'G1510', 'G0386'],
        'greek':  'ἐγώ εἰμι ἡ ἀνάστασις',
        'notes':  'John 11:25. Jesus speaking.',
        'self_ref_confidence': 'high',
        'scope':  'gospels',
        'group':  'I AM sayings',
    },
    {
        'label':  'I AM — the Way',
        'strongs': ['G1473', 'G1510', 'G3598'],
        'greek':  'ἐγώ εἰμι ἡ ὁδός',
        'notes':  'John 14:6 (Way, Truth, and Life). Jesus speaking.',
        'self_ref_confidence': 'high',
        'scope':  'gospels',
        'group':  'I AM sayings',
    },
    {
        'label':  'I AM — the True Vine',
        'strongs': ['G1473', 'G1510', 'G0288'],
        'greek':  'ἐγώ εἰμι ἡ ἄμπελος',
        'notes':  'John 15:1, 5. Jesus speaking.',
        'self_ref_confidence': 'high',
        'scope':  'gospels',
        'group':  'I AM sayings',
    },

    # ── Lord ───────────────────────────────────────────────────────────────
    {
        'label':  'Lord (Kyrios)',
        'strongs': ['G2962'],
        'greek':  'κύριος',
        'notes':  'Extremely broad — includes narrator references, disciples addressing '
                  'Jesus, and Jesus\'s own usage. Cannot be filtered to self-reference '
                  'without speaker tagging.',
        'self_ref_confidence': 'low',
        'scope':  'gospels',
        'group':  'Other titles',
    },

    # ── Christ / Messiah ──────────────────────────────────────────────────
    {
        'label':  'Christ / Messiah',
        'strongs': ['G5547'],
        'greek':  'Χριστός',
        'notes':  'Includes all uses as title and as part of "Jesus Christ". '
                  'Jesus rarely uses this term of Himself (Mt 23:10 is an exception); '
                  'most instances are narrator or epistolary.',
        'self_ref_confidence': 'low',
        'scope':  'NT',
        'group':  'Other titles',
    },

    # ── Bridegroom ─────────────────────────────────────────────────────────
    {
        'label':  'Bridegroom',
        'strongs': ['G3566'],
        'greek':  'νυμφίος',
        'notes':  'Mt 9:15, Mk 2:19–20, Lk 5:34–35 — Jesus refers to himself as '
                  '"the bridegroom." Also Jhn 3:29 (John the Baptist speaking). '
                  'Mostly self-referential in Synoptics.',
        'self_ref_confidence': 'high',
        'scope':  'gospels',
        'group':  'Other titles',
    },

    # ── Prophet ────────────────────────────────────────────────────────────
    {
        'label':  'Prophet',
        'strongs': ['G4396'],
        'greek':  'προφήτης',
        'notes':  'Mt 13:57, Mk 6:4, Lk 4:24, 13:33 — Jesus calls himself a prophet '
                  '("a prophet is not without honour…"). Counts all prophet occurrences '
                  'in the Gospels; most are not self-referential.',
        'self_ref_confidence': 'low',
        'scope':  'gospels',
        'group':  'Other titles',
    },
]

# Canonical Gospel + Acts book order for display
_GOSPEL_BOOKS = ['Mat', 'Mrk', 'Luk', 'Jhn']
_NT_BOOKS = ['Mat', 'Mrk', 'Luk', 'Jhn', 'Act', 'Rom', '1Co', '2Co', 'Gal',
             'Eph', 'Php', 'Col', '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm',
             'Heb', 'Jas', '1Pe', '2Pe', '1Jn', '2Jn', '3Jn', 'Jud', 'Rev']

_CONFIDENCE_LABELS = {
    'high':   '✓ High — almost exclusively Jesus self-reference',
    'medium': '~ Medium — some instances from others / ambiguous',
    'low':    '✗ Low  — many non-self-referential instances',
}


# ── Core computation ──────────────────────────────────────────────────────────

def _load_nt() -> pd.DataFrame:
    from ..core import db as _db
    df = _db.load()
    return df[df['source'] == 'TAGNT'].copy()


def _count_title(nt_df: pd.DataFrame, title: dict,
                 speaking_verses: set | None = None) -> dict[str, int]:
    """
    Return {book_id: verse_count} for a given title entry.

    If speaking_verses is provided, restrict to those (book, ch, vs) tuples.
    """
    books = _GOSPEL_BOOKS if title['scope'] == 'gospels' else _NT_BOOKS
    strongs_list = title['strongs']
    label = title['label']
    counts = {}
    for book in books:
        b = nt_df[nt_df['book_id'] == book]
        if b.empty:
            counts[book] = 0
            continue
        # Intersect verse sets for all required strongs
        verse_set = None
        for s in strongs_list:
            vs = set(b[b['strongs'].str.contains(s, na=False, regex=False)]
                     [['chapter', 'verse']].apply(tuple, axis=1))
            verse_set = vs if verse_set is None else verse_set & vs
        verse_set = verse_set or set()
        # Apply speaker filter if provided
        if speaking_verses is not None:
            from ..discourse.speaker import ALLOWLIST_VERSES
            if label in ALLOWLIST_VERSES:
                # Use exact allowlist — restrict to known Jesus-speaking refs
                allowed = {(ch, vs) for (bk, ch, vs) in ALLOWLIST_VERSES[label]
                           if bk == book}
                verse_set = verse_set & allowed
            else:
                # Use MACULA subjref detection
                allowed_cvs = {(ch, vs) for (bk, ch, vs) in speaking_verses
                               if bk == book}
                verse_set = verse_set & allowed_cvs
        counts[book] = len(verse_set)
    return counts


def title_counts(
    scope: str = 'gospels',
    *,
    groups: list[str] | None = None,
    speaker_filter: bool = False,
) -> 'pd.DataFrame':
    """
    Return a DataFrame: rows=titles, columns=book counts + Total.

    Parameters
    ----------
    scope          : 'gospels' (Mat/Mrk/Luk/Jhn only) or 'NT' (all 27 books)
    groups         : optional list of group names to include; None = all
    speaker_filter : if True, restrict each title to verses where Jesus is
                     the speaker — using curated allowlists (high-confidence
                     titles) or MACULA subjref detection (others).
    """
    import pandas as pd

    nt = _load_nt()
    books = _GOSPEL_BOOKS if scope == 'gospels' else _NT_BOOKS

    # Pre-compute MACULA speaking verses once for the whole call
    speaking_verses: set | None = None
    if speaker_filter:
        from ..discourse.speaker import jesus_speaking_verse_set
        target_books = list(set(books) & {'Mat', 'Mrk', 'Luk', 'Jhn',
                                          'Act', 'Rom', '1Co'})
        speaking_verses = set(jesus_speaking_verse_set(books=target_books))

    rows = []
    for title in TITLE_REGISTRY:
        if groups and title['group'] not in groups:
            continue
        # For gospel-scope queries, skip NT-only titles
        if scope == 'gospels' and title['scope'] == 'NT':
            counts = _count_title(nt, {**title, 'scope': 'NT'},
                                  speaking_verses)
            # Filter to gospel books only
            counts = {b: counts.get(b, 0) for b in _GOSPEL_BOOKS}
        else:
            counts = _count_title(nt, title, speaking_verses)
            counts = {b: counts.get(b, 0) for b in books}

        total = sum(counts.values())
        row = {
            'title':       title['label'],
            'greek':       title['greek'],
            'confidence':  title['self_ref_confidence'],
            'group':       title['group'],
            **{b: counts.get(b, 0) for b in books},
            'Total':       total,
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    return df


def _book_name(book_id: str) -> str:
    from ..core.reference import book_info
    info = book_info(book_id)
    return info['name'] if info else book_id


# ── Terminal output ───────────────────────────────────────────────────────────

def print_title_counts(scope: str = 'gospels', *,
                       speaker_filter: bool = False) -> None:
    """Print a formatted title frequency table to stdout."""
    df = title_counts(scope=scope, speaker_filter=speaker_filter)
    books = _GOSPEL_BOOKS if scope == 'gospels' else _NT_BOOKS
    # Filter to books with any count
    active_books = [b for b in books if df[b].sum() > 0]

    w = 72
    print(f"\n{'═'*w}")
    scope_label = 'Gospels' if scope == 'gospels' else 'New Testament'
    print(f"  Christological Titles — {scope_label}")
    print("  Counts are verse-level co-occurrences (see confidence column)")
    print(f"{'═'*w}\n")

    # Print by group
    for group in ['Son titles', 'I AM sayings', 'Other titles']:
        sub = df[df['group'] == group]
        if sub.empty:
            continue
        print(f"  {group}")
        print(f"  {'-'*w}")

        # Header
        bk_hdr = ''.join(f"{_book_name(b)[:4]:>6}" for b in active_books)
        print(f"  {'Title':<28} {bk_hdr}  {'Total':>5}  Confidence")
        print(f"  {'-'*27} {'------' * len(active_books)}  -----  ----------")

        for _, row in sub.iterrows():
            bk_vals = ''.join(f"{row[b]:>6}" for b in active_books)
            conf = {'high': '✓', 'medium': '~', 'low': '✗'}[row['confidence']]
            print(f"  {row['title']:<28} {bk_vals}  {row['Total']:>5}  {conf} {row['confidence']}")
        print()

    print("  Confidence key:")
    for k, v in _CONFIDENCE_LABELS.items():
        print(f"    {v}")
    print()


# ── Chart ─────────────────────────────────────────────────────────────────────

def title_chart(
    scope: str = 'gospels',
    *,
    groups: list[str] | None = None,
    output_path: str | None = None,
    figsize: tuple = (13, 7),
) -> str:
    """
    Grouped bar chart: x=titles, groups=Gospel books (or NT sections).
    Returns path to the saved PNG.
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

    df = title_counts(scope=scope, groups=groups)
    books = _GOSPEL_BOOKS if scope == 'gospels' else _NT_BOOKS
    active_books = [b for b in books if df[b].sum() > 0]

    if output_path is None:
        out_dir = Path('output') / 'charts' / 'nt' / 'names'
        out_dir.mkdir(parents=True, exist_ok=True)
        output_path = str(out_dir / f'christological-titles-{scope}.png')

    # Sort by Total descending for readability
    df = df.sort_values('Total', ascending=False).reset_index(drop=True)

    x = np.arange(len(df))
    n_books = len(active_books)
    width = 0.8 / n_books
    colors = [plt.get_cmap('tab10')(i) for i in range(10)]

    fig, ax = plt.subplots(figsize=figsize)

    for i, book in enumerate(active_books):
        offset = (i - n_books / 2 + 0.5) * width
        ax.bar(x + offset, df[book], width,
               label=_book_name(book),
               color=colors[i % len(colors)],
               edgecolor='white', linewidth=0.4, alpha=0.9)

    ax.set_xticks(x)
    ax.set_xticklabels(df['title'], rotation=35, ha='right', fontsize=8)
    ax.set_ylabel('Verses with title pattern', fontsize=9)
    ax.set_title(
        f'Christological Title Frequency — {scope.title()}\n'
        f'(verse-level co-occurrence; see confidence notes for speaker attribution caveats)',
        fontsize=10, fontweight='bold', pad=10,
    )
    ax.yaxis.grid(True, linestyle='--', alpha=0.4)
    ax.set_axisbelow(True)
    ax.legend(fontsize=8, loc='upper right')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    return output_path


# ── Verse detail lookup ───────────────────────────────────────────────────────

def title_verses(label: str, *, book: str | None = None) -> 'pd.DataFrame':
    """
    Return a DataFrame of every verse matching a given title, with KJV text.

    Parameters
    ----------
    label : title label as it appears in TITLE_REGISTRY (e.g. 'Son of Man')
    book  : optional book_id to restrict to (e.g. 'Mat')
    """
    import pandas as pd

    title = next((t for t in TITLE_REGISTRY if t['label'] == label), None)
    if title is None:
        available = [t['label'] for t in TITLE_REGISTRY]
        raise ValueError(f"Unknown title {label!r}. Available: {available}")

    nt = _load_nt()
    books = ([book] if book
             else (_GOSPEL_BOOKS if title['scope'] == 'gospels' else _NT_BOOKS))

    rows = []
    for bk in books:
        b = nt[nt['book_id'] == bk]
        if b.empty:
            continue
        verse_set = None
        for s in title['strongs']:
            vs = set(b[b['strongs'].str.contains(s, na=False, regex=False)]
                     [['chapter', 'verse']].apply(tuple, axis=1))
            verse_set = vs if verse_set is None else verse_set & vs

        for ch, vs in sorted(verse_set or set()):
            # Get KJV text
            kjv_words = b[(b['chapter'] == ch) & (b['verse'] == vs)]['translation'].dropna()
            kjv = ' '.join(str(t).strip().rstrip('¶').strip() for t in kjv_words if str(t).strip())
            rows.append({
                'reference': f'{_book_name(bk)} {ch}:{vs}',
                'book_id': bk,
                'chapter': ch,
                'verse': vs,
                'kjv_text': kjv,
            })

    return pd.DataFrame(rows)


# ── Markdown report ───────────────────────────────────────────────────────────

def title_report(
    output_dir: str = 'output/reports/nt/names',
    *,
    include_verses: bool = True,
) -> str:
    """
    Generate a Markdown report with frequency table, chart, and verse listings.
    Returns the path to the saved file.
    """
    from pathlib import Path

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = title_counts(scope='gospels')
    chart_path = title_chart(
        scope='gospels',
        output_path=str(out_dir / 'christological-titles-chart.png'),
    )

    lines = [
        "# Christological Titles: Jesus's Self-Designations in the Gospels",
        "",
        "Frequency analysis of the major titles Jesus used to refer to Himself, "
        "counted by verse-level co-occurrence of the relevant Greek Strong's numbers "
        "across the four Gospels.",
        "",
        "> **Speaker attribution note:** The STEPBible TAGNT data does not tag speakers. "
        "Counts reflect all occurrences of each title pattern in a given verse, "
        "regardless of who is speaking. The **Confidence** column indicates how "
        "reliably each title reflects Jesus's own self-designation vs. others' usage.",
        "",
        "| Confidence | Meaning |",
        "|---|---|",
        "| ✓ High | Virtually all instances are Jesus speaking of Himself |",
        "| ~ Medium | Mix of Jesus speaking and others; ~60–80% self-referential |",
        "| ✗ Low | Many instances from narrators, disciples, or opponents |",
        "",
    ]

    # Summary frequency table
    lines += [
        "## Summary",
        "",
        f"![Christological titles chart]({Path(chart_path).name})",
        "",
    ]

    for group in ['Son titles', 'I AM sayings', 'Other titles']:
        sub = df[df['group'] == group]
        if sub.empty:
            continue
        lines += [f"### {group}", ""]
        lines += [
            "| Title | Greek | Mat | Mrk | Luk | Jhn | Total | Confidence |",
            "|---|---|---:|---:|---:|---:|---:|---|",
        ]
        for _, row in sub.sort_values('Total', ascending=False).iterrows():
            conf_sym = {'high': '✓', 'medium': '~', 'low': '✗'}[row['confidence']]
            lines.append(
                f"| {row['title']} | {row['greek']} "
                f"| {row['Mat']} | {row['Mrk']} | {row['Luk']} | {row['Jhn']} "
                f"| **{row['Total']}** | {conf_sym} {row['confidence']} |"
            )
        lines.append("")

    # Per-title detail with notes and verses
    lines += ["---", "", "## Title Details", ""]

    for title in TITLE_REGISTRY:
        conf_sym = {'high': '✓', 'medium': '~', 'low': '✗'}[title['self_ref_confidence']]
        lines += [
            f"### {title['label']}",
            "",
            f"**Greek:** {title['greek']}  ",
            f"**Strongs:** {', '.join(title['strongs'])}  ",
            f"**Confidence:** {conf_sym} {title['self_ref_confidence']}  ",
            "",
            f"{title['notes']}",
            "",
        ]

        if include_verses:
            try:
                vdf = title_verses(title['label'])
                if not vdf.empty:
                    lines += [
                        "| Reference | Text |",
                        "|---|---|",
                    ]
                    for _, row in vdf.iterrows():
                        txt = row['kjv_text']
                        if len(txt) > 120:
                            txt = txt[:117] + '...'
                        lines.append(f"| {row['reference']} | {txt} |")
                    lines.append("")
            except Exception:
                pass

    lines += [
        "---",
        "",
        "_Source: STEPBible TAGNT (CC BY 4.0, Tyndale House Cambridge). "
        "Counts are verse-level co-occurrences of Strong's numbers; "
        "speaker attribution requires additional annotation not present in this dataset. "
        "Cross-reference data: scrollmapper / OpenBible.info (CC-BY)._",
    ]

    md_path = out_dir / 'christological-titles.md'
    md_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"  Saved: {md_path}")
    print(f"  Chart: {chart_path}")
    return str(md_path)
