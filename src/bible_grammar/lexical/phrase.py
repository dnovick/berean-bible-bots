"""
Phrase search for Hebrew OT, Greek NT, and LXX.

Finds consecutive word sequences within a verse. Each position in the
phrase can be specified as a Strong's number, a lemma, a morphology
constraint dict, or a wildcard.

Usage
-----
from bible_grammar.lexical.phrase import phrase_search

# Hebrew: דְּבַר יְהוָה  "word of the LORD"
phrase_search(['H1697', 'H3068'])

# Greek NT: λόγος θεοῦ  "word of God"
phrase_search(['G3056', 'G2316'], corpus='NT')

# LXX: same phrase in Septuagint
phrase_search(['G3056', 'G2316'], corpus='LXX')

# Accept lemmas directly (resolved automatically)
phrase_search(['λόγος', 'θεός'], corpus='NT')
phrase_search(['דָּבָר', 'יְהוָה'], corpus='OT')

# Mixed: Niphal perfect followed by any noun
phrase_search([{'stem': 'Niphal', 'conjugation': 'Perfect'}, {'pos': 'Noun'}])

# Wildcard: word of ??? God  (any word between)
phrase_search(['H1697', '*', 'H0430'])

Constraint dict keys (for morphology-based positions):
  strongs, lemma, pos, stem, conjugation, tense, voice, mood,
  person, number, gender, case_, state
"""

from __future__ import annotations
import re
import unicodedata
import pandas as pd
from ..core import db as _db
from ..core._utils import norm_strongs as _norm_strongs, norm_strongs_user as _query_strongs

# Corpus identifiers
_OT = "OT"
_NT = "NT"
_LXX = "LXX"

_OT_BOOKS = None
_NT_BOOKS = None


def _ot_book_ids() -> set:
    global _OT_BOOKS
    if _OT_BOOKS is None:
        from ..core.reference import all_book_ids
        _OT_BOOKS = set(all_book_ids("OT"))
    return _OT_BOOKS


def _nt_book_ids() -> set:
    global _NT_BOOKS
    if _NT_BOOKS is None:
        from ..core.reference import all_book_ids
        _NT_BOOKS = set(all_book_ids("NT"))
    return _NT_BOOKS


# ── strongs normalisation ─────────────────────────────────────────────────────

# ── token matching ────────────────────────────────────────────────────────────

def _resolve_token(token: str | dict | None) -> dict:
    """
    Convert a user token to a canonical constraint dict with key 'strongs',
    'lemma', or morphology keys.

    Accepts: strongs string, lemma string, constraint dict, '*' wildcard.
    """
    if token is None or token == '*':
        return {'wildcard': True}

    if isinstance(token, dict):
        return token

    if isinstance(token, str):
        # Strong's number?
        if re.match(r'^[HG]\d', token.strip().upper()):
            return {'strongs': _query_strongs(token)}
        # Looks like a lemma — try to resolve
        from .wordstudy import resolve_strongs
        resolved = resolve_strongs(token)
        if resolved:
            return {'strongs': _query_strongs(resolved)}
        # Keep as lemma
        return {'lemma': unicodedata.normalize('NFC', token.strip().lower())}

    raise TypeError(f"Unsupported token type: {type(token)}")


def _matches_row(row: pd.Series, constraint: dict, is_lxx: bool = False) -> bool:
    """Check whether a single word row satisfies a constraint dict."""
    if constraint.get('wildcard'):
        return True

    if 'strongs' in constraint:
        norm = _norm_strongs(str(row.get('strongs', '')))
        target = constraint['strongs']
        # Strip trailing variant letter from both sides for root comparison
        norm_root = re.sub(r'[A-Z]$', '', norm)
        target_root = re.sub(r'[A-Z]$', '', target)
        if norm_root != target_root:
            return False

    if 'lemma' in constraint:
        stored = unicodedata.normalize('NFC',
                                       str(row.get('lemma', '')).strip().lower())
        if constraint['lemma'] not in stored:
            return False

    for key, col in [
        ('pos',         'part_of_speech'),
        ('stem',        'stem'),
        ('conjugation', 'conjugation'),
        ('tense',       'tense'),
        ('voice',       'voice'),
        ('mood',        'mood'),
        ('person',      'person'),
        ('number',      'number'),
        ('gender',      'gender'),
        ('case_',       'case_'),
        ('state',       'state'),
    ]:
        if key in constraint:
            val = str(row.get(col, '')).lower()
            if constraint[key].lower() not in val:
                return False

    return True


# ── main search ───────────────────────────────────────────────────────────────

def phrase_search(
    tokens: list,
    *,
    corpus: str = 'OT',
    book: str | list[str] | None = None,
    book_group: str | None = None,
    chapter: int | None = None,
    include_kjv: bool = True,
    max_results: int = 500,
) -> pd.DataFrame:
    """
    Search for a consecutive word sequence within verses.

    Parameters
    ----------
    tokens      : List of search tokens. Each element may be:
                    - A Strong's number string: 'H1697', 'G3056'
                    - A lemma string: 'λόγος', 'שָׁלוֹם', 'דָּבָר'
                    - A constraint dict: {'pos': 'Verb', 'stem': 'Niphal'}
                    - '*' or None — wildcard (matches any word)
    corpus      : 'OT' (Hebrew/Aramaic TAHOT), 'NT' (Greek TAGNT), or 'LXX'
    book        : Restrict to one book or list of books (book_id, e.g. 'Gen')
    book_group  : 'torah', 'prophets', 'writings', 'gospels', 'pauline'
    chapter     : Restrict to a single chapter number
    include_kjv : Attach KJV verse text to results (default True)
    max_results : Cap on number of results returned (default 500)

    Returns a DataFrame with columns:
      book_id, chapter, verse,
      word_1 .. word_N  (surface form of each matched word)
      strongs_1 .. strongs_N
      reference  (e.g. 'Gen 1:1')
      kjv_text   (if include_kjv=True)

    Examples
    --------
    # דְּבַר יְהוָה "word of the LORD" anywhere in OT
    phrase_search(['H1697', 'H3068'])

    # Same phrase in Jeremiah only
    phrase_search(['H1697', 'H3068'], book='Jer')

    # λόγος θεοῦ in NT
    phrase_search(['G3056', 'G2316'], corpus='NT')

    # Using lemmas
    phrase_search(['λόγος', 'θεός'], corpus='NT')

    # Niphal perfect followed by a noun in Isaiah
    phrase_search([{'stem': 'Niphal', 'conjugation': 'Perfect'}, {'pos': 'Noun'}],
                  book='Isa')

    # Wildcard: H1697 + anything + H3068
    phrase_search(['H1697', '*', 'H3068'])
    """
    from ..core.reference import book_ids_for_group

    corpus = corpus.upper()
    is_lxx = (corpus == _LXX)

    # Load appropriate dataframe
    if is_lxx:
        df = _db.load_lxx()
        df = df[~df['is_deuterocanon']].copy()
    else:
        df = _db.load()
        if corpus == _OT:
            df = df[df['source'] == 'TAHOT'].copy()
        else:
            df = df[df['source'] == 'TAGNT'].copy()

    # Book / group filters
    if book_group is not None:
        df = df[df['book_id'].isin(book_ids_for_group(book_group))]
    if book is not None:
        vals = [book] if isinstance(book, str) else book
        df = df[df['book_id'].isin(vals)]
    if chapter is not None:
        df = df[df['chapter'] == chapter]

    if df.empty:
        return pd.DataFrame()

    # Resolve tokens to constraint dicts
    constraints = [_resolve_token(t) for t in tokens]
    n = len(constraints)

    if n == 0:
        return pd.DataFrame()

    # Sort by position
    df = df.sort_values(['book_id', 'chapter', 'verse', 'word_num']).reset_index(drop=True)

    # Build a set of candidate starting rows for position 0
    # For efficiency, pre-filter on the first non-wildcard constraint
    next((i for i, c in enumerate(constraints) if not c.get('wildcard')), None)

    rows_out = []

    # Group by verse for efficient consecutive-word checking
    for (book_id, ch, vs), verse_df in df.groupby(['book_id', 'chapter', 'verse'],
                                                  sort=False):
        verse_df = verse_df.sort_values('word_num').reset_index(drop=True)
        words = verse_df.to_dict('records')
        nw = len(words)

        if nw < n:
            continue

        for start in range(nw - n + 1):
            matched = True
            for offset, constraint in enumerate(constraints):
                if not _matches_row(words[start + offset], constraint, is_lxx):
                    matched = False
                    break
            if matched:
                row: dict = {
                    'book_id':   book_id,
                    'chapter':   ch,
                    'verse':     vs,
                    'reference': f"{book_id} {ch}:{vs}",
                }
                for offset in range(n):
                    w = words[start + offset]
                    row[f'word_{offset+1}'] = w.get('word', '')
                    row[f'strongs_{offset+1}'] = _norm_strongs(str(w.get('strongs', '')))
                    if is_lxx:
                        row[f'lemma_{offset+1}'] = w.get('lemma', '')
                rows_out.append(row)
                if len(rows_out) >= max_results:
                    break
        if len(rows_out) >= max_results:
            break

    if not rows_out:
        return pd.DataFrame()

    result = pd.DataFrame(rows_out)

    # Attach KJV text
    if include_kjv:
        try:
            tr = _db.load_translations()
            kjv = tr[tr['translation'] == 'KJV'][['book_id', 'chapter', 'verse', 'text']]
            kjv = kjv.rename(columns={'text': 'kjv_text'})
            result = result.merge(kjv, on=['book_id', 'chapter', 'verse'], how='left')
        except Exception:
            pass

    return result.reset_index(drop=True)


def proximity_search(
    tokens: list,
    *,
    within: int = 5,
    ordered: bool = False,
    corpus: str = 'OT',
    book: str | list[str] | None = None,
    book_group: str | None = None,
    include_kjv: bool = True,
    max_results: int = 500,
) -> pd.DataFrame:
    """
    Find verses where two or more tokens appear within N words of each other,
    optionally crossing verse boundaries.

    Parameters
    ----------
    tokens   : List of 2+ search tokens (same formats as phrase_search:
               Strong's numbers, lemmas, or morphology constraint dicts).
               Wildcards ('*') are not meaningful here and will be ignored.
    within   : Maximum word distance between the first and last matched token
               (counts intervening words, including across verse boundaries).
               E.g. within=5 means at most 4 words between the two terms.
    ordered  : If True, tokens must appear in the given order (left to right).
               If False (default), any order is accepted.
    corpus   : 'OT', 'NT', or 'LXX'
    book     : Restrict to one book or list of books
    book_group: 'torah', 'prophets', 'writings', 'gospels', 'pauline'
    include_kjv: Attach KJV verse text for the verse of the first match token
    max_results: Cap on number of results (default 500)

    Returns a DataFrame with columns:
      book_id, chapter_1, verse_1, word_num_1, word_1, strongs_1,
      book_id, chapter_2, verse_2, word_num_2, word_2, strongs_2,
      distance, reference, kjv_text (if include_kjv)

    For 3+ tokens: columns extend to _3, _4 etc., distance is span of all.

    Examples
    --------
    # אמונה and חסד within 5 words in Psalms
    proximity_search(['H0530', 'H2617'], within=5, book_group='writings')

    # ברית and שלום within 8 words anywhere in OT
    proximity_search(['H1285', 'H7965'], within=8)

    # πίστις and ἀγάπη within 7 words in Paul
    proximity_search(['G4102', 'G26'], within=7, corpus='NT', book_group='pauline')

    # Ordered: H6944 (holy) before H2617 (kindness) within 10 words
    proximity_search(['H6944', 'H2617'], within=10, ordered=True)
    """
    from ..core.reference import book_ids_for_group
    from .wordstudy import _BOOK_ORDER

    corpus = corpus.upper()
    is_lxx = (corpus == _LXX)

    # Load and filter corpus
    if is_lxx:
        df = _db.load_lxx()
        df = df[~df['is_deuterocanon']].copy()
    else:
        df = _db.load()
        df = df[df['source'] == ('TAHOT' if corpus == _OT else 'TAGNT')].copy()

    if book_group is not None:
        df = df[df['book_id'].isin(book_ids_for_group(book_group))]
    if book is not None:
        vals = [book] if isinstance(book, str) else book
        df = df[df['book_id'].isin(vals)]

    if df.empty:
        return pd.DataFrame()

    # Build global position index: sort by canonical book order → ch → vs → word_num
    df = df.copy()
    df['_book_order'] = df['book_id'].map(_BOOK_ORDER).fillna(999)
    df = df.sort_values(['_book_order', 'chapter', 'verse', 'word_num']).reset_index(drop=True)
    df['_gpos'] = df.index  # global sequential position

    # Resolve tokens (skip wildcards)
    constraints = [_resolve_token(t) for t in tokens if t != '*']
    n = len(constraints)
    if n < 2:
        raise ValueError("proximity_search requires at least 2 non-wildcard tokens")

    # For each constraint, find all matching row indices (global positions)
    match_sets: list[pd.Index] = []
    for constraint in constraints:
        if constraint.get('wildcard'):
            match_sets.append(df.index)
            continue
        matched = [i for i, row in df.iterrows() if _matches_row(row, constraint, is_lxx)]
        match_sets.append(pd.Index(matched))

    if any(len(s) == 0 for s in match_sets):
        return pd.DataFrame()

    # Build result rows: for each hit of token[0], find hits of all other tokens
    # within the window.  Use numpy for speed on large sets.
    import numpy as np

    pos_arrays = [df.loc[s, '_gpos'].values for s in match_sets]
    idx_arrays = [s.values for s in match_sets]

    rows_out = []

    # Iterate over positions of the anchor (first token)
    for anchor_idx, anchor_pos in zip(idx_arrays[0], pos_arrays[0]):
        candidate_idxs = [anchor_idx]
        candidate_pos = [anchor_pos]
        ok = True

        for ti in range(1, n):
            # Find positions of token ti within [anchor_pos - within, anchor_pos + within]
            lo = anchor_pos - within
            hi = anchor_pos + within
            cands = pos_arrays[ti]
            in_window = idx_arrays[ti][(cands >= lo) & (cands <= hi)]

            if len(in_window) == 0:
                ok = False
                break

            if ordered:
                # Must be after previous token
                prev_pos = candidate_pos[-1]
                cands_ordered = [(i, pos_arrays[ti][np.where(idx_arrays[ti] == i)[0][0]])
                                 for i in in_window
                                 if pos_arrays[ti][np.where(idx_arrays[ti] == i)[0][0]] > prev_pos]
                if not cands_ordered:
                    ok = False
                    break
                # Pick the closest one
                best_i, best_pos = min(cands_ordered, key=lambda x: x[1])
            else:
                # Pick the closest to anchor
                best_i = in_window[
                    np.argmin(np.abs(pos_arrays[ti][
                        np.isin(idx_arrays[ti], in_window)] - anchor_pos))
                ]
                best_pos = int(df.loc[best_i, '_gpos'])

            candidate_idxs.append(best_i)
            candidate_pos.append(best_pos)

        if not ok:
            continue

        # Distance = span of global positions
        distance = max(candidate_pos) - min(candidate_pos)

        row_out: dict = {'distance': distance}
        for ti, (ridx, rpos) in enumerate(zip(candidate_idxs, candidate_pos)):
            w = df.loc[ridx]
            suffix = f'_{ti+1}'
            row_out[f'book_id{suffix}'] = w['book_id']
            row_out[f'chapter{suffix}'] = int(w['chapter'])
            row_out[f'verse{suffix}'] = int(w['verse'])
            row_out[f'word_num{suffix}'] = int(w['word_num'])
            row_out[f'word{suffix}'] = w['word']
            row_out[f'strongs{suffix}'] = _norm_strongs(str(w.get('strongs', '')))
            if is_lxx:
                row_out[f'lemma{suffix}'] = w.get('lemma', '')

        # Reference = location of first token
        r1 = df.loc[candidate_idxs[0]]
        row_out['reference'] = f"{r1['book_id']} {int(r1['chapter'])}:{int(r1['verse'])}"
        rows_out.append(row_out)

        if len(rows_out) >= max_results:
            break

    if not rows_out:
        return pd.DataFrame()

    result = pd.DataFrame(rows_out).sort_values('distance').reset_index(drop=True)

    if include_kjv:
        try:
            tr = _db.load_translations()
            kjv = tr[tr['translation'] == 'KJV'][['book_id', 'chapter', 'verse', 'text']]
            kjv = kjv.rename(columns={'book_id': 'book_id_1', 'chapter': 'chapter_1',
                                      'verse': 'verse_1', 'text': 'kjv_text'})
            result = result.merge(kjv, on=['book_id_1', 'chapter_1', 'verse_1'], how='left')
        except Exception:
            pass

    return result


def print_proximity_results(
    df: pd.DataFrame,
    *,
    max_rows: int = 25,
) -> None:
    """Print proximity search results in a readable format."""
    if df.empty:
        print("  No matches found.")
        return

    total = len(df)
    shown = min(total, max_rows)
    print(f"  {total:,} match{'es' if total != 1 else ''}"
          f"{' (showing first ' + str(shown) + ')' if total > max_rows else ''}:\n")

    # Find token count (proximity cols are word_1, word_2 ... not word_num_1)
    n_tokens = sum(1 for c in df.columns
                   if c.startswith('word_') and c[5:].isdigit())

    for _, row in df.head(max_rows).iterrows():
        ref = row['reference']
        dist = int(row['distance'])
        parts = []
        for i in range(1, n_tokens + 1):
            w = row.get(f'word_{i}', '')
            ref_i = f"{row.get(f'book_id_{i}', '')} {row.get(
                f'chapter_{i}', '')}:{row.get(f'verse_{i}', '')}"
            same_verse = all(
                row.get(f'book_id_{j}') == row.get('book_id_1') and
                row.get(f'chapter_{j}') == row.get('chapter_1') and
                row.get(f'verse_{j}') == row.get('verse_1')
                for j in range(1, n_tokens + 1)
            )
            if same_verse:
                parts.append(str(w))
            else:
                parts.append(f"{w} ({ref_i})")
        words_str = '  …  '.join(parts)
        print(f"  [{ref}]  {words_str}  (dist: {dist})")
        if 'kjv_text' in row and pd.notna(row.get('kjv_text', '')):
            text = str(row['kjv_text'])
            if len(text) > 100:
                text = text[:97] + '...'
            print(f"    {text}")
    print()


def print_phrase_results(
    df: pd.DataFrame,
    *,
    max_rows: int = 30,
    show_strongs: bool = False,
) -> None:
    """Print phrase search results in a readable format."""
    if df.empty:
        print("  No matches found.")
        return

    total = len(df)
    shown = min(total, max_rows)
    print(f"  {total:,} match{'es' if total != 1 else ''}"
          f"{' (showing first ' + str(shown) + ')' if total > max_rows else ''}:\n")

    word_cols = [c for c in df.columns if c.startswith('word_')]
    strongs_cols = [c for c in df.columns if c.startswith('strongs_')]
    [c for c in df.columns if c.startswith('lemma_')]

    for _, row in df.head(max_rows).iterrows():
        words = '  '.join(str(row[c]) for c in word_cols)
        ref = row['reference']
        print(f"  [{ref}]  {words}")
        if show_strongs:
            strongs = '  '.join(str(row[c]) for c in strongs_cols)
            print(f"           {strongs}")
        if 'kjv_text' in row and pd.notna(row['kjv_text']):
            text = str(row['kjv_text'])
            if len(text) > 100:
                text = text[:97] + '...'
            print(f"    {text}")
    print()
