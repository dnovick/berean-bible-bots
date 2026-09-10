"""
Verb governance analysis — which preposition (if any) introduces a Hebrew
verb's complement, versus a bare or אֵת-marked direct object, versus no
complement at all.

Data source: the tree-based extraction in ``core/verb_governance.py``, which
walks the MACULA Hebrew lowfat constituency trees (not the flattened word
table) so that a preposition is only counted as "governed by" a verb when it
is that verb's actual sibling argument within the same clause — not merely
the next preposition to appear in the verse.

Primary functions:
  verb_governance_summary()      — one table: every complement type this verb
                                    takes (each preposition, bare/marked
                                    direct object, no complement), with counts
  verb_preposition_distribution() — just the preposition breakdown
  verb_governance_examples()      — sample verses for one complement type,
                                     for spot-checking / qualitative reading

Print wrappers:
  print_verb_governance()

Usage
─────
from bible_grammar.ot.verb_governance import print_verb_governance

# How does בטח (trust) govern its complement?
print_verb_governance('H0982')

# Same, but only Qal (Hiphil "cause to trust" governs differently)
print_verb_governance('H0982', stem='qal')
"""

from __future__ import annotations
import re
import unicodedata
import pandas as pd
from typing import Optional

from ..core.verb_governance import load_verb_governance
from .prepositions import PREP_GLOSS

_governance_cache: Optional[pd.DataFrame] = None


def _load_nfc() -> pd.DataFrame:
    """Load the governance table with lemma columns NFC-normalized.

    Raw MACULA lemma text is not NFC-composed, so it won't match literal
    Hebrew string keys typed by a human (e.g. PREP_GLOSS) without this —
    the same gap core/_utils.py::load_ot_data() already works around for
    the flattened word table. Cached once per process, same pattern.
    """
    global _governance_cache
    if _governance_cache is None:
        df = load_verb_governance().copy()
        for col in ('verb_lemma', 'prep_lemma', 'head_lemma'):
            df[col] = df[col].apply(
                lambda x: unicodedata.normalize('NFC', str(x)) if pd.notna(x) else x
            )
        _governance_cache = df
    return _governance_cache


def _norm_verb_strongs(s: str) -> str:
    """Normalise a Strong's number for comparison against strongnumberx,
    which is stored WITHOUT an 'H' prefix and WITH leading zeros (e.g.
    '0982'). Accepts 'H0982', 'H982', '0982', or '982'."""
    s = re.sub(r'^[Hh]', '', s.strip())
    return s.lstrip('0') or '0'


def _scope(strongs: str, book: Optional[str] = None,
           stem: Optional[str] = None) -> pd.DataFrame:
    df = _load_nfc()
    target = _norm_verb_strongs(strongs)
    df = df[df['verb_strongnumberx'].str.lstrip('0') == target]
    if book is not None:
        df = df[df['book'] == book]
    if stem is not None:
        df = df[df['verb_stem'].str.lower() == stem.lower()]
    return df


def verb_governance_summary(
    strongs: str,
    book: Optional[str] = None,
    stem: Optional[str] = None,
    position: str = 'any',
) -> pd.DataFrame:
    """
    One table covering every way this verb's complement is expressed:
    each preposition it takes, bare vs. אֵת-marked direct object, and
    occurrences with no qualifying complement in their clause.

    Parameters
    ----------
    strongs : str
        Strong's number, e.g. 'H0982' (accepts 'H982', '0982', '982' too).
    book : str, optional
        Restrict to one OT book abbreviation (e.g. 'Isa').
    stem : str, optional
        Restrict to one stem (e.g. 'qal', 'hiphil') — governance often
        differs by stem (e.g. Qal בטח 'trust IN' vs. Hiphil 'cause X to trust').
    position : {'any', 'first'}
        'any' (default) counts every prepositional argument the verb has in
        its clause (a clause can have more than one PP — see e.g. Isa 36:9,
        which has three). 'first' counts only the first PP encountered after
        the verb per occurrence, useful for a "primary complement" view.

    Returns
    -------
    DataFrame with columns: category, count, pct
        pct is out of total verb occurrences in scope (not total argument
        rows) — so the categories do NOT need to sum to 100% when a single
        occurrence contributes more than one PP under position='any'.
    """
    scoped = _scope(strongs, book=book, stem=stem)
    total_occurrences = scoped['verb_xml_id'].nunique()
    if total_occurrences == 0:
        return pd.DataFrame(columns=['category', 'count', 'pct'])

    pp = scoped[scoped['arg_role'] == 'pp']
    if position == 'first':
        pp = pp.sort_values('arg_index').groupby('verb_xml_id', as_index=False).first()

    prep_counts = pp['prep_lemma'].value_counts()

    obj = scoped[scoped['arg_role'].isin(['o', 'o2'])]
    bare_obj = int((~obj['has_object_marker']).sum())
    marked_obj = int(obj['has_object_marker'].sum())

    none_count = int((scoped[scoped['arg_role'] == 'none']['verb_xml_id']).nunique())

    rows = []
    for prep, count in prep_counts.items():
        gloss = PREP_GLOSS.get(prep, '')
        label = f"{prep} ({gloss})" if gloss else prep
        rows.append({'category': label, 'count': int(count)})
    if marked_obj:
        rows.append({'category': 'direct object (with אֵת)', 'count': marked_obj})
    if bare_obj:
        rows.append({'category': 'direct object (bare)', 'count': bare_obj})
    if none_count:
        rows.append({'category': 'no complement found', 'count': none_count})

    result = pd.DataFrame(rows).sort_values('count', ascending=False).reset_index(drop=True)
    result['pct'] = (result['count'] / total_occurrences * 100).round(1)
    return result


def verb_preposition_distribution(
    strongs: str,
    book: Optional[str] = None,
    stem: Optional[str] = None,
    position: str = 'any',
) -> pd.DataFrame:
    """
    Just the preposition breakdown for this verb (no object/none rows).

    Returns
    -------
    DataFrame with columns: lemma, gloss, count, pct
        pct is out of total prepositional-argument instances (not total
        verb occurrences).
    """
    scoped = _scope(strongs, book=book, stem=stem)
    pp = scoped[scoped['arg_role'] == 'pp']
    if position == 'first':
        pp = pp.sort_values('arg_index').groupby('verb_xml_id', as_index=False).first()

    if pp.empty:
        return pd.DataFrame(columns=['lemma', 'gloss', 'count', 'pct'])

    counts = pp['prep_lemma'].value_counts().reset_index()
    counts.columns = ['lemma', 'count']
    counts['pct'] = (counts['count'] / counts['count'].sum() * 100).round(1)
    counts['gloss'] = counts['lemma'].map(PREP_GLOSS).fillna('')
    return counts[['lemma', 'gloss', 'count', 'pct']]


def verb_governance_examples(
    strongs: str,
    category: Optional[str] = None,
    book: Optional[str] = None,
    stem: Optional[str] = None,
    top_n: int = 8,
) -> pd.DataFrame:
    """
    Sample verses for one complement type, for spot-checking against the
    actual text rather than trusting the aggregate counts blindly.

    Parameters
    ----------
    category : str, optional
        A preposition lemma (e.g. 'בְּ'), 'o' (direct object, any marking),
        or 'none' (no complement). Omit to get a mixed sample across all
        categories.

    Returns
    -------
    DataFrame with columns: ref, arg_role, prep_lemma, complement, verb_stem, verb_type
    """
    scoped = _scope(strongs, book=book, stem=stem)
    if category == 'none':
        scoped = scoped[scoped['arg_role'] == 'none']
    elif category == 'o':
        scoped = scoped[scoped['arg_role'].isin(['o', 'o2'])]
    elif category is not None:
        scoped = scoped[(scoped['arg_role'] == 'pp') & (scoped['prep_lemma'] == category)]

    scoped = scoped.copy()
    scoped['complement'] = scoped['arg_text'].fillna('') + ' (' + scoped['arg_gloss'].fillna('') + ')'
    out = scoped[['ref', 'arg_role', 'prep_lemma', 'complement', 'verb_stem', 'verb_type']]
    return out.head(top_n).reset_index(drop=True)


def print_verb_governance(
    strongs: str,
    book: Optional[str] = None,
    stem: Optional[str] = None,
) -> None:
    scope_note = ''
    if book:
        scope_note += f' [{book}]'
    if stem:
        scope_note += f' [{stem}]'

    summary = verb_governance_summary(strongs, book=book, stem=stem)
    print(f'\n=== Verb Governance: {strongs}{scope_note} ===')
    if summary.empty:
        print('  No occurrences found.')
        return
    print(summary.to_string(index=False))

    print('\n--- Preposition distribution (any position in clause) ---')
    preps = verb_preposition_distribution(strongs, book=book, stem=stem)
    if not preps.empty:
        print(preps.to_string(index=False))
    else:
        print('  (this verb takes no prepositional complements in scope)')

    print('\n--- Sample verses ---')
    examples = verb_governance_examples(strongs, book=book, stem=stem, top_n=10)
    if not examples.empty:
        print(examples.to_string(index=False))
