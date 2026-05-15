"""Infinitive construct and absolute usage analysis."""
from __future__ import annotations

from ._common import _load_macula, _filter_book, _strip_diacritics, _PREP_DISPLAY
from ..ot.prepositions import find_governing_prep


def infinitive_usage(book: str) -> dict:
    """
    Analyse infinitive construct and absolute usage in a book.

    Returns a dict with keys:
      inf_cst_total, inf_abs_total,
      inf_cst_by_prep, inf_cst_by_role,
      inf_abs_examples, inf_cst_examples
    """
    df = _load_macula()
    book_df = _filter_book(df, book).reset_index(drop=True)

    inf_cst_rows = book_df[book_df['type_'] == 'infinitive construct']
    inf_abs_rows = book_df[book_df['type_'] == 'infinitive absolute']

    inf_cst_by_prep: dict[str, int] = {}
    inf_cst_by_role: dict[str, int] = {}
    inf_cst_examples: list[dict] = []

    for _, row in inf_cst_rows.iterrows():
        actual_pos = book_df.index.get_loc(row.name)
        prep = find_governing_prep(book_df, actual_pos)
        inf_cst_by_prep[prep] = inf_cst_by_prep.get(prep, 0) + 1
        role = str(row.get('role', ''))
        inf_cst_by_role[role] = inf_cst_by_role.get(role, 0) + 1
        if len(inf_cst_examples) < 30:
            inf_cst_examples.append({
                'book': book,
                'chapter': int(row['chapter']),
                'verse': int(row['verse']),
                'text': str(row.get('text', '')),
                'lemma': str(row.get('lemma', '')),
                'stem': str(row.get('stem', '')),
                'governing_prep': prep,
                'role': role,
                'gloss': str(row.get('gloss', '')),
            })

    inf_abs_examples: list[dict] = []
    for _, row in inf_abs_rows.iterrows():
        actual_pos = book_df.index.get_loc(row.name)
        paronomastic = False
        root = _strip_diacritics(str(row.get('lemma', '')))
        for delta in (-2, -1, 1, 2):
            nbr_pos = actual_pos + delta
            if 0 <= nbr_pos < len(book_df):
                nbr = book_df.iloc[nbr_pos]
                if (_strip_diacritics(str(nbr.get('lemma', ''))) == root
                        and nbr.get('class_') == 'verb'
                        and nbr.get('type_') != 'infinitive absolute'):
                    paronomastic = True
                    break
        inf_abs_examples.append({
            'chapter': int(row['chapter']),
            'verse': int(row['verse']),
            'text': str(row.get('text', '')),
            'lemma': str(row.get('lemma', '')),
            'stem': str(row.get('stem', '')),
            'gloss': str(row.get('gloss', '')),
            'paronomastic': paronomastic,
        })

    return {
        'inf_cst_total':    len(inf_cst_rows),
        'inf_abs_total':    len(inf_abs_rows),
        'inf_cst_by_prep':  inf_cst_by_prep,
        'inf_cst_by_role':  inf_cst_by_role,
        'inf_cst_examples': inf_cst_examples,
        'inf_abs_examples': inf_abs_examples,
    }


def print_infinitive_usage(book: str) -> None:
    """Print a formatted infinitive usage analysis for a book."""
    result = infinitive_usage(book)

    print()
    print('═' * 72)
    print(f"  Infinitive usage: {book}")
    print(f"  Infinitive construct: {result['inf_cst_total']}  |  "
          f"Infinitive absolute: {result['inf_abs_total']}")
    print('─' * 72)

    print("\n  Infinitive Construct — governing preposition:")
    by_prep = sorted(result['inf_cst_by_prep'].items(), key=lambda x: -x[1])
    total_cst = result['inf_cst_total'] or 1
    for prep, cnt in by_prep:
        desc = _PREP_DISPLAY.get(prep, prep)
        pct = cnt / total_cst * 100
        bar = '█' * int(pct / 3)
        print(f"    {prep:<8} {desc:<32} {cnt:>4}  {pct:>5.1f}%  {bar}")

    print("\n  Infinitive Construct — clause role:")
    role_labels = {'v': 'verb (main predicate)', 's': 'subject',
                   'o': 'object', 'adv': 'adverbial', 'p': 'predicate',
                   '': 'unlabelled'}
    for role, cnt in sorted(result['inf_cst_by_role'].items(), key=lambda x: -x[1]):
        label = role_labels.get(role, role)
        print(f"    {role or '–':<6} {label:<28} {cnt:>4}")

    print("\n  Infinitive Absolute — sample (with paronomastic flag):")
    for ex in result['inf_abs_examples'][:20]:
        paro = '⟦paronomastic⟧' if ex['paronomastic'] else ''
        print(f"    {book} {ex['chapter']}:{ex['verse']:<4}  "
              f"{ex['text']:<20}  {ex['lemma']:<12}  {ex['gloss'][:20]:<20}  {paro}")
    print()
