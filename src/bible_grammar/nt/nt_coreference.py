"""
NT coreference and anaphora chain analysis.

The MACULA Greek NT dataset includes a `referent` column on ~14,471 tokens
(primarily pronouns and relative clauses) that contains a MACULA xml_id
pointing to the token's antecedent.  This enables tracking who a pronoun
or relative clause refers to throughout a passage or book.

Format:  space-separated xml_id list (multiple antecedents for plural pronouns)
Example: 'n43014023002'  → Ἰησοῦς (Jesus) @ Jhn 14:23

Coverage: ~14,471 NT tokens have referent data — primarily pronouns (αὐτός,
          relative pronoun ὅς, etc.) and occasionally demonstratives.

Questions this answers
──────────────────────
  • How many times is Jesus referenced by pronoun in each Gospel?
  • Where does Paul refer back to himself in his letters?
  • How dense is pronominal reference to the Spirit in John 14–16?
  • Which participants receive the most pronominal references per book?
  • What is the referent profile of αὐτός (him/her/it) per book?

Public API
──────────
nt_referent_data(book=None)                    → DataFrame (tokens with referent)
nt_referent_frequency(book=None, top_n=20)     → DataFrame (antecedents by ref count)
nt_entity_chain(entity_xml_id, book=None)      → DataFrame (all tokens referring to entity)
nt_pronoun_referents(pronoun, book=None, top_n=20) → DataFrame
nt_book_entity_density(book, top_n=15)         → DataFrame

print_nt_referent_overview()                   → None
print_nt_referent_frequency(book=None, top_n=20) → None
print_nt_entity_chain(entity_xml_id, ...)      → None
print_nt_pronoun_referents(pronoun, ...)       → None
print_nt_book_entity_density(book, top_n=15)   → None

nt_referent_book_chart(top_n=20)               → Path | None
nt_entity_density_chart(book, top_n=15)        → Path | None

KNOWN_ENTITIES                                 → dict[str, str]
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd

_CHART_DIR = Path('output') / 'charts' / 'nt' / 'coreference'


# ── known entity anchor IDs ───────────────────────────────────────────────────
# MACULA xml_id of the first occurrence used as the canonical referent anchor.
# These are the top antecedents discovered by frequency analysis.
KNOWN_ENTITIES: dict[str, str] = {
    # Individuals
    'Jesus (Mat)':   'n40001021005',
    'Jesus (Mrk)':   'n41003007003',
    'Jesus (Luk)':   'n42003021001',
    'Jesus (Jhn)':   'n43014023002',
    'Jesus (Act)':   'n44001001001',
    'Paul (Rom)':    'n45001001001',
    'Paul (1Co)':    'n46003022002',
    'Paul (2Co)':    'n47001001001',
    'Paul (Gal)':    'n48001001001',
    'Paul (Php)':    'n50001001001',
    'Paul (Col)':    'n51001001001',
    'Peter (Jhn)':   'n43013037003',
    'Thomas (Jhn)':  'n43014005003',
    'Philip (Jhn)':  'n43014008003',
    'Judas (Jhn)':   'n43014022003',
    # Groups
    'Disciples (Mat)': 'n40005001015',
    'Disciples (Jhn)': 'n43013023006',
    'Brothers (2Co)':  'n47008001004',
}


# ── helpers ───────────────────────────────────────────────────────────────────

def _load_nt() -> pd.DataFrame:
    from ..core.syntax import load_syntax
    return load_syntax()


def _parse_referent(ref: str) -> list[str]:
    if not ref or not isinstance(ref, str):
        return []
    return [r.strip() for r in ref.split() if r.strip()]


# ── data access ───────────────────────────────────────────────────────────────

def nt_referent_data(
    book: str | list[str] | None = None,
) -> pd.DataFrame:
    """
    All NT tokens that have a `referent` annotation, with resolved columns.

    Returns the original DataFrame rows plus:
      antecedent_lemma, antecedent_gloss, antecedent_book, antecedent_ref
    (based on the first referent ID if multiple are present).
    """
    df = _load_nt()
    if book is not None:
        if isinstance(book, str):
            book = [book]
        df = df[df['book'].isin(book)]

    has_ref = df[df['referent'].notna() & (df['referent'] != '')].copy()
    if has_ref.empty:
        return has_ref

    id_map = _load_nt().set_index('xml_id')[['lemma', 'gloss', 'book', 'ref']].to_dict('index')

    ant_lemmas, ant_glosses, ant_books, ant_refs = [], [], [], []
    for ref_str in has_ref['referent']:
        ids = _parse_referent(ref_str)
        if ids:
            info = id_map.get(ids[0], {})
            ant_lemmas.append(info.get('lemma', ''))
            ant_glosses.append(info.get('gloss', ''))
            ant_books.append(info.get('book', ''))
            ant_refs.append(info.get('ref', ''))
        else:
            ant_lemmas.append('')
            ant_glosses.append('')
            ant_books.append('')
            ant_refs.append('')

    has_ref = has_ref.copy()
    has_ref['antecedent_lemma'] = ant_lemmas
    has_ref['antecedent_gloss'] = ant_glosses
    has_ref['antecedent_book'] = ant_books
    has_ref['antecedent_ref'] = ant_refs
    return has_ref.reset_index(drop=True)


def nt_referent_frequency(
    book: str | list[str] | None = None,
    *,
    top_n: int = 20,
) -> pd.DataFrame:
    """
    Most referenced antecedents (by count of pronominal references).

    Returns: antecedent_lemma, antecedent_gloss, antecedent_ref,
             antecedent_book, ref_count.
    """
    df = nt_referent_data(book=book)
    if df.empty:
        return pd.DataFrame()

    result = (
        df.groupby(['antecedent_lemma', 'antecedent_gloss',
                    'antecedent_ref', 'antecedent_book'])
        .size()
        .reset_index(name='ref_count')
        .sort_values('ref_count', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
    return result


def nt_entity_chain(
    entity_xml_id: str,
    *,
    book: str | list[str] | None = None,
) -> pd.DataFrame:
    """
    All tokens that reference a specific entity (given by its MACULA xml_id).

    Useful for tracking how often and where a named person or entity is
    referred to by pronoun.
    """
    df = _load_nt()
    if book is not None:
        if isinstance(book, str):
            book = [book]
        df = df[df['book'].isin(book)]

    mask = df['referent'].notna() & df['referent'].str.contains(
        entity_xml_id, na=False, regex=False
    )
    return df[mask].copy().reset_index(drop=True)


def nt_pronoun_referents(
    pronoun: str,
    *,
    book: str | list[str] | None = None,
    top_n: int = 20,
) -> pd.DataFrame:
    """
    What entities does a given pronoun lemma refer to, and how often?

    Parameters
    ----------
    pronoun : lemma e.g. 'αὐτός', 'ὅς', 'ἐκεῖνος', 'οὗτος'
    """
    df = nt_referent_data(book=book)
    subset = df[df['lemma'] == pronoun]
    if subset.empty:
        return pd.DataFrame()
    return (
        subset.groupby(['antecedent_lemma', 'antecedent_gloss', 'antecedent_ref'])
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def nt_book_entity_density(
    book: str,
    *,
    top_n: int = 15,
) -> pd.DataFrame:
    """
    Most frequently referenced entities within a single NT book.

    Returns: antecedent_lemma, antecedent_gloss, antecedent_ref, ref_count, chapter_spread.
    """
    df = nt_referent_data(book=book)
    if df.empty:
        return pd.DataFrame()

    result = (
        df.groupby(['antecedent_lemma', 'antecedent_gloss', 'antecedent_ref'])
        .agg(
            ref_count=('chapter', 'count'),
            chapter_spread=('chapter', 'nunique'),
        )
        .reset_index()
        .sort_values('ref_count', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
    return result


def nt_entity_chapter_distribution(
    entity_xml_id: str,
    book: str,
) -> pd.DataFrame:
    """Count of pronominal references to an entity by chapter within a book."""
    df = nt_entity_chain(entity_xml_id, book=book)
    if df.empty:
        return pd.DataFrame(columns=['chapter', 'count'])
    return df['chapter'].value_counts().sort_index().reset_index().rename(
        columns={'chapter': 'chapter', 'count': 'count'}
    )


# ── print functions ───────────────────────────────────────────────────────────

def print_nt_referent_overview() -> None:
    df = _load_nt()
    has_ref = df[df['referent'].notna() & (df['referent'] != '')]
    pron = df[df['class_'] == 'pron']
    has_ref_pron = pron[pron['referent'].notna() & (pron['referent'] != '')]
    w = 58
    print(f"\n{'═'*w}")
    print("  NT Coreference / Referent Coverage")
    print(f"{'═'*w}")
    print(f"  Total NT tokens           : {len(df):>9,}")
    ref_pct = len(has_ref) / len(df) * 100
    print(f"  Tokens with referent link : {len(has_ref):>9,} ({ref_pct:.1f}%)")
    print(f"  Pronoun tokens            : {len(pron):>9,}")
    pron_pct = len(has_ref_pron) / len(pron) * 100
    print(f"  Pronouns with referent    : {len(has_ref_pron):>9,} ({pron_pct:.1f}%)")
    print()


def print_nt_referent_frequency(
    book: str | list[str] | None = None,
    *,
    top_n: int = 20,
) -> None:
    if isinstance(book, str):
        scope = f" ({book})"
    elif book is None:
        scope = " (all NT)"
    else:
        scope = f" ({', '.join(book)})"
    df = nt_referent_frequency(book=book, top_n=top_n)
    w = 72
    print(f"\n{'═'*w}")
    print(f"  Most Referenced Antecedents{scope}")
    print(f"{'═'*w}")
    if df.empty:
        print("  No results found.")
        print()
        return
    print(f"  {'Lemma':<14} {'Gloss':<20} {'Ref':<20} {'Book':<6} {'Count':>6}")
    print(f"  {'-'*13} {'-'*19} {'-'*19} {'-'*5} {'-'*6}")
    for _, row in df.iterrows():
        print(f"  {str(row['antecedent_lemma']):<14} {str(row['antecedent_gloss']):<20} "
              f"{str(row['antecedent_ref']):<20} {str(row['antecedent_book']):<6} "
              f"{row['ref_count']:>6,}")
    print()


def print_nt_entity_chain(
    entity_xml_id: str,
    *,
    book: str | list[str] | None = None,
    entity_label: str = '',
) -> None:
    df = nt_entity_chain(entity_xml_id, book=book)
    scope = f" ({book})" if isinstance(book, str) else ""
    label = entity_label or entity_xml_id
    w = 60
    print(f"\n{'═'*w}")
    print(f"  Pronominal references to: {label}{scope}")
    print(f"{'═'*w}")
    if df.empty:
        print("  No references found.")
        print()
        return
    print(f"  Total references: {len(df):,}")
    ch_counts = df['chapter'].value_counts().sort_index()
    print(f"  Chapter spread  : {df['chapter'].nunique()} chapters")
    print("\n  Chapter distribution:")
    for ch, cnt in ch_counts.items():
        bar = '█' * min(cnt, 40)
        print(f"    Ch {int(ch):>3}: {bar} {cnt}")
    print()


def print_nt_pronoun_referents(
    pronoun: str,
    *,
    book: str | list[str] | None = None,
    top_n: int = 20,
) -> None:
    scope = f" ({book})" if isinstance(book, str) else ""
    df = nt_pronoun_referents(pronoun, book=book, top_n=top_n)
    w = 68
    print(f"\n{'═'*w}")
    print(f"  What does {pronoun} refer to?{scope}")
    print(f"{'═'*w}")
    if df.empty:
        print("  No results found.")
        print()
        return
    print(f"  {'Antecedent':<14} {'Gloss':<22} {'Ref':<20} {'Count':>6}")
    print(f"  {'-'*13} {'-'*21} {'-'*19} {'-'*6}")
    for _, row in df.iterrows():
        print(f"  {str(row['antecedent_lemma']):<14} {str(row['antecedent_gloss']):<22} "
              f"{str(row['antecedent_ref']):<20} {row['count']:>6,}")
    print()


def print_nt_book_entity_density(
    book: str,
    *,
    top_n: int = 15,
) -> None:
    df = nt_book_entity_density(book, top_n=top_n)
    w = 68
    print(f"\n{'═'*w}")
    print(f"  Most Referenced Entities in {book}")
    print(f"{'═'*w}")
    if df.empty:
        print("  No results found.")
        print()
        return
    print(f"  {'Lemma':<14} {'Gloss':<22} {'Ref':<20} {'Refs':>5} {'Chs':>4}")
    print(f"  {'-'*13} {'-'*21} {'-'*19} {'-'*5} {'-'*4}")
    for _, row in df.iterrows():
        print(f"  {str(row['antecedent_lemma']):<14} {str(row['antecedent_gloss']):<22} "
              f"{str(row['antecedent_ref']):<20} {row['ref_count']:>5,} "
              f"{row['chapter_spread']:>4}")
    print()


# ── chart functions ───────────────────────────────────────────────────────────

def nt_referent_book_chart(
    *,
    top_n: int = 20,
) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = _load_nt()
    has_ref = df[df['referent'].notna() & (df['referent'] != '')]
    book_counts = has_ref['book'].value_counts().head(top_n)

    _CHART_DIR.mkdir(parents=True, exist_ok=True)
    out = _CHART_DIR / 'referent_by_book.png'

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(book_counts.index[::-1], book_counts.values[::-1], color='steelblue')
    ax.set_xlabel('Tokens with referent annotation')
    ax.set_title(f'NT Coreference Coverage — Top {top_n} Books')
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def nt_entity_density_chart(
    book: str,
    *,
    top_n: int = 15,
) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_book_entity_density(book, top_n=top_n)
    if df.empty:
        return None

    _CHART_DIR.mkdir(parents=True, exist_ok=True)
    out = _CHART_DIR / f'entity_density_{book}.png'

    labels = [f"{row['antecedent_lemma']} ({row['antecedent_gloss'][:15]})"
              for _, row in df.iterrows()]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(labels[::-1], df['ref_count'][::-1], color='darkorange')
    ax.set_xlabel('Reference count')
    ax.set_title(f'Most Referenced Entities in {book}')
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out
