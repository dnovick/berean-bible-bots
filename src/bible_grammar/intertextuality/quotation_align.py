"""
NT quotation word alignment: traces which Hebrew words NT authors quote,
and whether they follow LXX vocabulary or diverge toward the MT.

For each NT→OT quotation pair, this module:
  1. Fetches the NT verse (TAGNT), OT verse (TAHOT), and LXX verse
  2. Identifies which NT Greek words appear in the LXX rendering of the
     same OT verse (LXX-following words)
  3. Identifies NT Greek words whose Hebrew root equivalent (via IBM Model 1
     alignment) differs from the LXX rendering (MT-leaning divergences)
  4. Produces per-word alignment verdicts: LXX | MT-diverge | neutral

Usage
-----
from bible_grammar.intertextuality.quotation_align import quotation_align, print_quotation_align

# Single NT verse
quotation_align('Mat', 4, 4)

# Print formatted analysis
print_quotation_align('Mat', 4, 4)

# Batch: all high-confidence quotations in Hebrews
from bible_grammar.intertextuality.quotation_align import batch_align
df = batch_align(nt_book='Heb', min_votes=50)
"""

from __future__ import annotations
import re
import pandas as pd
from ..core import db as _db
from .quotations import nt_quotations

_CONTENT_POS = {'Noun', 'Verb', 'Adjective', 'Adverb'}


def _norm_g(strongs: str) -> str:
    """Normalise a Greek strongs to G + unpadded number (strip variant letter)."""
    m = re.match(r'^G0*(\d+)[A-Z]?$', strongs.strip().upper())
    return f"G{m.group(1)}" if m else strongs.strip().upper()


def _norm_h(strongs: str) -> str:
    """Extract and normalise the content Hebrew strongs from a TAHOT cell."""
    braced = re.findall(r'\{([HG]\d+[A-Z]?)\}', strongs)
    for b in braced:
        if not re.match(r'H9\d+', b):
            m = re.match(r'^H0*(\d+)([A-Z]?)$', b)
            return f"H{m.group(1)}{m.group(2)}" if m else b
    return ''


def _is_content(pos: str) -> bool:
    return any(p.lower() in pos.lower() for p in _CONTENT_POS)


def quotation_align(
    nt_book: str,
    nt_chapter: int,
    nt_verse: int,
    *,
    min_votes: int = 5,
    content_only: bool = True,
) -> list[dict]:
    """
    Word-level alignment analysis for an NT verse's OT quotations.

    For each OT cross-reference, returns a list of word-alignment dicts,
    one per content word in the NT verse.

    Parameters
    ----------
    nt_book/nt_chapter/nt_verse : NT verse coordinates
    min_votes   : Minimum cross-reference vote threshold
    content_only: If True, only analyse nouns, verbs, adjectives, adverbs

    Returns a list of dicts, one per (NT verse, OT ref) pair:
    {
      nt_ref     : str  e.g. 'Mat 4:4'
      ot_ref     : str  e.g. 'Deu 8:3'
      votes      : int
      words      : list of per-word dicts:
        {
          nt_word      : surface form
          nt_strongs   : normalised Greek strongs
          nt_lemma     : lemma (from TAGNT)
          nt_pos       : part of speech
          lxx_match    : bool  — this strongs appears in the LXX verse
          heb_root     : str   — Hebrew strongs aligned to this Greek word (IBM Model 1)
          heb_word     : str   — Hebrew surface form
          verdict      : 'LXX' | 'MT-diverge' | 'LXX+MT' | 'neutral'
                          LXX       = matches LXX exactly (Greek strongs in LXX verse)
                          MT-diverge= NT word's Hebrew root is present in OT verse but
                                      the LXX renders it differently
                          LXX+MT    = both (LXX uses this strongs AND it aligns to OT Hebrew)
                          neutral   = function word or no alignment data
        }
      lxx_following_pct : float  — % content words that follow LXX
      mt_diverge_count  : int    — content words that diverge from LXX toward MT
      summary           : str    — 'follows LXX' | 'mixed' | 'MT-leaning'
    }
    """
    from ..core.ibm_align import load_word_alignment

    words_df = _db.load()
    lxx_df = _db.load_lxx()
    align_df = load_word_alignment()

    # NT verse
    nt_rows = words_df[
        (words_df['source'] == 'TAGNT') &
        (words_df['book_id'] == nt_book) &
        (words_df['chapter'] == nt_chapter) &
        (words_df['verse'] == nt_verse)
    ].sort_values('word_num')

    if nt_rows.empty:
        return []

    # Cross-references
    xrefs = nt_quotations(nt_book=nt_book, min_votes=min_votes)
    xrefs = xrefs[
        (xrefs['nt_chapter'] == nt_chapter) &
        (xrefs['nt_verse'] == nt_verse)
    ]

    if xrefs.empty:
        return []

    results = []
    for _, xref in xrefs.iterrows():
        ot_b = xref['ot_book']
        ot_ch = xref['ot_chapter']
        ot_vs = xref['ot_verse']
        ot_ref = f"{ot_b} {ot_ch}:{ot_vs}"

        # LXX verse — build set of normalised strongs present
        lxx_verse = lxx_df[
            (lxx_df['book_id'] == ot_b) &
            (lxx_df['chapter'] == ot_ch) &
            (lxx_df['verse'] == ot_vs)
        ]
        lxx_strongs_set = {
            _norm_g(s)
            for s in lxx_verse['strongs'].dropna()
            if _norm_g(s).startswith('G')
        }

        # OT Hebrew verse — set of normalised content strongs
        ot_verse = words_df[
            (words_df['source'] == 'TAHOT') &
            (words_df['book_id'] == ot_b) &
            (words_df['chapter'] == ot_ch) &
            (words_df['verse'] == ot_vs)
        ]
        ot_heb_strongs = {_norm_h(s) for s in ot_verse['strongs'].dropna() if _norm_h(s)}

        # IBM alignment for this OT verse: Greek strongs → Hebrew root
        verse_align = align_df[
            (align_df['book_id'] == ot_b) &
            (align_df['chapter'] == ot_ch) &
            (align_df['verse'] == ot_vs)
        ]
        # Map lxx_strongs → (heb_strongs, heb_word) for this verse
        lxx_to_heb: dict[str, tuple[str, str]] = {}
        for _, arow in verse_align.iterrows():
            g = _norm_g(str(arow['lxx_strongs']))
            h = str(arow['heb_strongs'])
            hw = str(arow['heb_word'])
            if g not in lxx_to_heb:
                lxx_to_heb[g] = (h, hw)

        # Analyse each NT word
        word_results = []
        content_count = 0
        lxx_match_count = 0
        mt_diverge_count = 0

        for _, nrow in nt_rows.iterrows():
            pos = str(nrow.get('part_of_speech', ''))
            if content_only and not _is_content(pos):
                continue

            g_strongs = _norm_g(str(nrow.get('strongs', '')))
            nt_word = str(nrow.get('word', ''))
            nt_lemma = str(nrow.get('lemma', nrow.get('word', '')))

            in_lxx = g_strongs in lxx_strongs_set
            heb_root, heb_word = lxx_to_heb.get(g_strongs, ('', ''))

            # Determine verdict
            if in_lxx and heb_root and heb_root in ot_heb_strongs:
                verdict = 'LXX+MT'
            elif in_lxx:
                verdict = 'LXX'
            elif heb_root and heb_root in ot_heb_strongs:
                # NT uses a Greek word whose Hebrew root is in the OT verse
                # but the LXX used a different Greek word — MT-leaning divergence
                verdict = 'MT-diverge'
            else:
                verdict = 'neutral'

            content_count += 1
            if verdict in ('LXX', 'LXX+MT'):
                lxx_match_count += 1
            elif verdict == 'MT-diverge':
                mt_diverge_count += 1

            word_results.append({
                'nt_word':    nt_word,
                'nt_strongs': g_strongs,
                'nt_lemma':   nt_lemma,
                'nt_pos':     pos,
                'lxx_match':  in_lxx,
                'heb_root':   heb_root,
                'heb_word':   heb_word,
                'verdict':    verdict,
            })

        lxx_pct = round(lxx_match_count / content_count * 100, 1) if content_count else 0
        if lxx_pct >= 70:
            summary = 'follows LXX'
        elif lxx_pct >= 40 or mt_diverge_count > 0:
            summary = 'mixed'
        else:
            summary = 'MT-leaning'

        results.append({
            'nt_ref':             f"{nt_book} {nt_chapter}:{nt_verse}",
            'ot_ref':             ot_ref,
            'votes':              int(xref['votes']),
            'words':              word_results,
            'lxx_following_pct':  lxx_pct,
            'mt_diverge_count':   mt_diverge_count,
            'summary':            summary,
        })

    return results


def print_quotation_align(
    nt_book: str,
    nt_chapter: int,
    nt_verse: int,
    *,
    min_votes: int = 5,
) -> None:
    """Print a formatted word-alignment analysis for an NT verse."""
    from ..lexical.wordstudy import _kjv_verse

    results = quotation_align(nt_book, nt_chapter, nt_verse, min_votes=min_votes)
    nt_ref = f"{nt_book} {nt_chapter}:{nt_verse}"
    kjv = _kjv_verse(nt_book, nt_chapter, nt_verse)

    print(f"\n{'═'*70}")
    print(f"  NT Quotation Alignment: {nt_ref}")
    if kjv:
        print(f"  \"{kjv[:90]}{'...' if len(kjv) > 90 else ''}\"")
    print(f"{'═'*70}\n")

    if not results:
        print(f"  No cross-references found (min_votes={min_votes}).\n")
        return

    for res in results:
        print(f"  ┌─ OT source: {res['ot_ref']}  (confidence votes: {res['votes']})")
        print(f"  │  Text alignment: {res['summary'].upper()}"
              f"  ({res['lxx_following_pct']:.0f}% follows LXX"
              f"{', ' + str(res['mt_diverge_count']) + ' MT-diverge' if res['mt_diverge_count'] else ''})")  # noqa: E501
        print(f"  └{'─'*60}")
        print()

        # Verdict legend
        _V = {'LXX': '✓ LXX', 'LXX+MT': '✓ LXX+MT', 'MT-diverge': '≠ MT', 'neutral': '·'}
        print(f"  {'NT word':<22} {'Strongs':<9} {'Verdict':<12} {'Hebrew root':<10} {'Hebrew word'}")  # noqa: E501
        print(f"  {'-'*21} {'-'*8} {'-'*11} {'-'*9} {'-'*20}")

        for w in res['words']:
            verdict_str = _V.get(w['verdict'], w['verdict'])
            heb = f"{w['heb_root']:<10} {w['heb_word']}" if w['heb_root'] else ''
            print(f"  {w['nt_word']:<22} {w['nt_strongs']:<9} {verdict_str:<12} {heb}")
        print()

        # OT verse KJV
        from ..lexical.wordstudy import _kjv_verse as _kjv
        ot_parts = res['ot_ref'].split()
        if len(ot_parts) == 2:
            ot_book = ot_parts[0]
            ch_vs = ot_parts[1].split(':')
            if len(ch_vs) == 2:
                ot_kjv = _kjv(ot_book, int(ch_vs[0]), int(ch_vs[1]))
                if ot_kjv:
                    print(
                        f"  OT ({res['ot_ref']}): \"{ot_kjv[:95]}{'...' if len(ot_kjv) > 95 else ''}\"")  # noqa: E501
                    print()


def batch_align(
    *,
    nt_book: str | list[str] | None = None,
    ot_book: str | list[str] | None = None,
    min_votes: int = 50,
) -> pd.DataFrame:
    """
    Run quotation_align() across all matching NT quotations.

    Returns a summary DataFrame with one row per (NT verse, OT ref):
      nt_ref, ot_ref, votes, lxx_following_pct, mt_diverge_count, summary,
      total_content_words
    """
    xrefs = nt_quotations(nt_book=nt_book, ot_book=ot_book, min_votes=min_votes)
    if xrefs.empty:
        return pd.DataFrame()

    seen: set = set()
    rows = []

    for _, xref in xrefs.iterrows():
        nb = xref['nt_book']
        nch = xref['nt_chapter']
        nvs = xref['nt_verse']
        key = (nb, nch, nvs)
        if key in seen:
            continue
        seen.add(key)

        try:
            results = quotation_align(nb, nch, nvs, min_votes=min_votes)
        except Exception:
            continue

        for res in results:
            rows.append({
                'nt_ref':             res['nt_ref'],
                'ot_ref':             res['ot_ref'],
                'votes':              res['votes'],
                'lxx_following_pct':  res['lxx_following_pct'],
                'mt_diverge_count':   res['mt_diverge_count'],
                'total_content_words': len(res['words']),
                'summary':            res['summary'],
            })

    if not rows:
        return pd.DataFrame()

    return (pd.DataFrame(rows)
            .sort_values(['votes', 'lxx_following_pct'], ascending=[False, False])
            .reset_index(drop=True))
