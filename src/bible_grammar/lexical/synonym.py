"""
Synonym comparison: side-by-side profile of near-synonym Hebrew or Greek roots.

For each root shows OT/NT frequency, morphological distribution, primary LXX
translation equivalent(s), and NT usage — making differences in usage pattern,
register, and theological trajectory visible at a glance.

Usage
-----
from bible_grammar.lexical.synonym import compare_synonyms, print_synonym_comparison

# Two Hebrew roots for "love"
compare_synonyms(['H157', 'H2836'])

# Three roots for "word"
compare_synonyms(['H1697', 'H0565', 'H6310'])

# Greek words for love
compare_synonyms(['G26', 'G5368', 'G5360'], corpus='NT')

# Accept lemmas too
compare_synonyms(['אָהַב', 'חָשַׁק'])
compare_synonyms(['ἀγάπη', 'φιλία'], corpus='NT')
"""

from __future__ import annotations
import pandas as pd
from .wordstudy import _lookup_lex, word_study
from ..core.reference import BOOKS

_BOOK_IDS = {b[0] for b in BOOKS}


def _resolve(term: str) -> str:
    """Resolve a term (strongs or lemma) to a canonical strongs string."""
    from .wordstudy import resolve_strongs
    result = resolve_strongs(term)
    if result is None:
        raise ValueError(f"Cannot resolve {term!r} to a Strong's number")
    return result


def compare_synonyms(
    terms: list[str],
    *,
    corpus: str | None = None,
    book: str | list[str] | None = None,
    book_group: str | None = None,
    top_books: int = 5,
    top_forms: int = 5,
) -> list[dict]:
    """
    Build a side-by-side comparison profile for two or more synonym roots.

    Parameters
    ----------
    terms       : List of Strong's numbers or lemmas to compare
    corpus      : 'OT', 'NT', or None (auto-detected from strongs prefix)
    book        : Restrict all profiles to one book or list of books
    book_group  : 'torah', 'prophets', 'writings', 'gospels', 'pauline'
    top_books   : Number of top books to include in each profile (default 5)
    top_forms   : Number of top morphological forms to include (default 5)

    Returns a list of profile dicts (one per term), each containing:
      strongs, lemma, translit, gloss, definition,
      total, by_book (DataFrame), top_forms (DataFrame),
      lxx_equivalents (DataFrame, Hebrew only),
      nt_trajectory (list of dicts, Hebrew only),
      shared_lxx (set — LXX lemmas shared with other terms in the set)
    """
    resolved = [_resolve(t) for t in terms]

    profiles = []
    for strongs in resolved:
        ws = word_study(strongs)
        lex = _lookup_lex(strongs) or {}

        profile = {
            'strongs':    strongs,
            'lemma':      ws['lemma'] or lex.get('lemma', ''),
            'translit':   ws['translit'] or lex.get('translit', ''),
            'gloss':      ws['gloss'] or lex.get('gloss', ''),
            'definition': ws['definition'] or lex.get('definition', ''),
            'total':      ws['total_occurrences'],
            'by_book':    ws['by_book'].head(top_books),
            'top_forms':  ws['morphological_forms'].head(top_forms),
            'lxx_equivalents': ws['translation_equivalents'],
            'nt_trajectory':   ws.get('nt_lxx_equiv', []),
        }
        profiles.append(profile)

    # Mark LXX equivalents shared across terms (overlap analysis)
    all_lxx: list[set] = []
    for p in profiles:
        te = p['lxx_equivalents']
        if not te.empty and 'lxx_strongs' in te.columns:
            all_lxx.append(set(te['lxx_strongs'].tolist()))
        else:
            all_lxx.append(set())

    for i, p in enumerate(profiles):
        others = set().union(*(all_lxx[j] for j in range(len(profiles)) if j != i))
        p['shared_lxx'] = all_lxx[i] & others

    return profiles


def print_synonym_comparison(
    terms: list[str],
    *,
    corpus: str | None = None,
    book: str | list[str] | None = None,
    book_group: str | None = None,
) -> None:
    """
    Print a formatted side-by-side synonym comparison.

    Parameters match compare_synonyms().
    """
    profiles = compare_synonyms(terms, corpus=corpus, book=book, book_group=book_group)
    n = len(profiles)

    print(f"\n{'═'*70}")
    print(f"  Synonym Comparison  ({n} terms)")
    print(f"{'═'*70}\n")

    # Header row
    for p in profiles:
        is_heb = p['strongs'].startswith('H')
        lang = "Hebrew" if is_heb else "Greek"
        print(f"  ┌─ {p['strongs']}  [{lang}]")
        if p['lemma']:
            print(f"  │  Lemma      : {p['lemma']}")
        if p['translit']:
            print(f"  │  Translit   : {p['translit']}")
        if p['gloss']:
            print(f"  │  Gloss      : {p['gloss']}")
        print(f"  │  Occurrences: {p['total']:,}")
        print(f"  └{'─'*50}")
        print()

    # Frequency comparison
    print(f"  {'─'*70}")
    print("  FREQUENCY COMPARISON")
    print(f"  {'─'*70}")
    [f"{p['strongs']} ({p['lemma'] or p['gloss']})" for p in profiles]
    max_total = max(p['total'] for p in profiles) or 1
    for p in profiles:
        bar_len = int(p['total'] / max_total * 30)
        bar = '█' * bar_len
        label = f"{p['strongs']} {p['lemma'] or ''}"
        print(f"  {label:<22} {p['total']:>5}  {bar}")
    print()

    # LXX translation equivalents (Hebrew only)
    if any(p['strongs'].startswith('H') for p in profiles):
        print(f"  {'─'*70}")
        print("  LXX TRANSLATION EQUIVALENTS  (word-level alignment)")
        print(f"  {'─'*70}")
        for p in profiles:
            if not p['strongs'].startswith('H'):
                continue
            te = p['lxx_equivalents']
            label = f"  {p['strongs']} {p['lemma'] or p['gloss']}"
            if te.empty:
                print(f"{label}: (no alignment data)")
            else:
                parts = []
                for _, row in te.head(5).iterrows():
                    g = row.get('lxx_lemma', '')
                    pct = row.get('pct', 0)
                    shared = '†' if row.get('lxx_strongs', '') in p['shared_lxx'] else ''
                    parts.append(f"{g}{shared} {pct:.0f}%")
                print(f"{label}: {' | '.join(parts)}")
        if any(any(p['shared_lxx']) for p in profiles):
            print("\n  † = LXX rendering shared with another term in this comparison")
        print()

    # NT trajectory (Hebrew only)
    if any(p.get('nt_trajectory') for p in profiles):
        print(f"  {'─'*70}")
        print("  OT → LXX → NT TRAJECTORY")
        print(f"  {'─'*70}")
        for p in profiles:
            traj = p.get('nt_trajectory', [])
            label = f"  {p['strongs']} {p['lemma'] or p['gloss']}"
            if not traj:
                print(f"{label}: (no NT trajectory)")
            else:
                for eq in traj:
                    print(
                        f"{label} → {eq['lemma']} ({eq['strongs']})  NT: {eq['nt_total']:,} occurrences")  # noqa: E501
        print()

    # Distribution by book
    print(f"  {'─'*70}")
    print(f"  DISTRIBUTION  (top {profiles[0]['by_book'].shape[0]} books each)")
    print(f"  {'─'*70}")
    for p in profiles:
        print(f"\n  {p['strongs']} {p['lemma'] or p['gloss']}:")
        for _, row in p['by_book'].iterrows():
            bar = '█' * min(int(row['pct'] / 2), 25)
            name = row.get('book_name', row['book_id'])
            print(f"    {name:<20} {row['count']:4d}  ({row['pct']:5.1f}%)  {bar}")

    # Morphological forms
    print(f"\n  {'─'*70}")
    print(f"  MORPHOLOGICAL FORMS  (top {profiles[0]['top_forms'].shape[0]} each)")
    print(f"  {'─'*70}")
    for p in profiles:
        tf = p['top_forms']
        if tf.empty:
            continue
        print(f"\n  {p['strongs']} {p['lemma'] or p['gloss']}:")
        print(tf.to_string(index=False, max_rows=p['top_forms'].shape[0]))

    print()


def synonym_table(terms: list[str], *, corpus: str | None = None) -> pd.DataFrame:
    """
    Compact tabular summary — one row per term — suitable for notebook display.

    Columns: strongs, lemma, gloss, total_occurrences,
             lxx_primary, lxx_primary_pct, nt_occurrences
    """
    profiles = compare_synonyms(terms, corpus=corpus)
    rows = []
    for p in profiles:
        te = p['lxx_equivalents']
        lxx_primary = te.iloc[0]['lxx_lemma'] if not te.empty else ''
        lxx_pct = te.iloc[0]['pct'] if not te.empty else 0.0
        nt_total = sum(e['nt_total'] for e in p.get('nt_trajectory', []))
        rows.append({
            'strongs':           p['strongs'],
            'lemma':             p['lemma'],
            'gloss':             p['gloss'],
            'total_occurrences': p['total'],
            'lxx_primary':       lxx_primary,
            'lxx_primary_pct':   lxx_pct,
            'nt_occurrences':    nt_total,
        })
    return pd.DataFrame(rows)
