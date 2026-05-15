"""
Hapax legomena: words occurring exactly once (or rarely) in a corpus or book.

A "hapax legomenon" (Greek: "said only once") is a word that appears exactly
once in a given corpus. Biblical hapaxes are significant for lexicography and
translation because their meaning must be inferred from context, cognates, or
ancient translations.

Usage
-----
from bible_grammar.lexical.hapax import hapax_legomena, hapax_table, hapax_summary

# All hapaxes in the OT (by Strong's lemma)
hapax_legomena(corpus='OT')

# Hapaxes in a specific book
hapax_legomena(book='Job')          # Job has the most OT hapaxes
hapax_legomena(book='Rev')          # NT book

# Hapaxes by POS
hapax_legomena(corpus='OT', part_of_speech='Verb')

# Allow 'rare' words (appearing <= N times)
hapax_legomena(corpus='OT', max_count=5)

# Print formatted table
hapax_table(book='Job', top_n=20)

# Summary stats: hapax count per book, sorted by count
hapax_summary(corpus='OT')
"""

from __future__ import annotations
import re
import pandas as pd
from ..core import db as _db
from ..core.reference import BOOKS, book_info
from .lexicon import lookup as _lex_lookup

_BOOK_ORDER = {b[0]: b[3] for b in BOOKS}
_OT_IDS = {b[0] for b in BOOKS if b[2] == "OT"}
_NT_IDS = {b[0] for b in BOOKS if b[2] == "NT"}


def _words() -> pd.DataFrame:
    return _db.load()


def _translations() -> pd.DataFrame:
    return _db.load_translations()


def _lookup_gloss(strongs: str) -> tuple[str, str]:
    """Return (lemma, gloss) for a Strong's number, or ('', '') if not found."""
    if not strongs:
        return "", ""
    entry = _lex_lookup(strongs.strip("{}"))
    if not entry:
        return "", ""
    return entry.get("lemma", ""), entry.get("gloss", "")


def _extract_strongs(s: str, source: str) -> list[str]:
    """Extract primary Strong's number(s) from a strongs cell."""
    if not isinstance(s, str) or not s:
        return []
    if source == "TAHOT":
        matches = re.findall(r'\{(H\d+[A-Z]?)\}', s)
        return matches[:1]  # primary only
    else:
        m = re.match(r'^(G\d+)', s)
        return [m.group(1)] if m else []


def _kjv_verse(book_id: str, chapter: int, verse: int) -> str:
    tr = _translations()
    row = tr[
        (tr["book_id"] == book_id) &
        (tr["chapter"] == chapter) &
        (tr["verse"] == verse) &
        (tr["translation"] == "KJV")
    ]
    return row.iloc[0]["text"] if not row.empty else ""


def hapax_legomena(
    *,
    corpus: str | None = None,
    book: str | None = None,
    part_of_speech: str | None = None,
    max_count: int = 1,
    min_count: int = 1,
    include_gloss: bool = True,
    include_context: bool = True,
    scope: str = "corpus",
) -> pd.DataFrame:
    """
    Find hapax legomena — words occurring rarely in a given scope.

    Parameters
    ----------
    corpus       : 'OT' or 'NT'. Defaults to 'OT' (or inferred from book).
    book         : Restrict search to a specific book (e.g. 'Job', 'Rev').
    part_of_speech : Filter by POS (e.g. 'Verb', 'Noun').
    max_count    : Maximum total occurrences to qualify (default 1 = strict hapax).
    min_count    : Minimum occurrences (default 1, set higher to exclude missing data).
    include_gloss : Add lemma/gloss columns from TBESH/TBESG lexicons.
    include_context: Add KJV verse text for the (first) occurrence.
    scope        : 'corpus' — count occurrences across the whole OT/NT.
                   'book'   — count occurrences within the specified book only.
                   Use scope='book' with book= to find words unique to one book.

    Returns
    -------
    DataFrame with columns:
      strongs, lemma, gloss, word (surface), book_id, chapter, verse,
      reference, corpus_count, [context_text]
    Sorted by canonical book order, then chapter, verse.
    """
    df = _words()

    # Determine source
    if book is not None:
        b_info = book_info(book)
        testament = b_info.get("testament", "OT")
        source = "TAHOT" if testament == "OT" else "TAGNT"
    else:
        source = "TAHOT" if (corpus or "OT").upper() == "OT" else "TAGNT"

    base = df[df["source"] == source].copy()

    if part_of_speech is not None:
        base = base[base["part_of_speech"].str.lower().str.contains(
            part_of_speech.lower(), na=False)]

    # Extract primary strongs for each word token
    base["_strongs"] = base.apply(
        lambda r: _extract_strongs(r["strongs"], source), axis=1)
    base = base[base["_strongs"].map(len) > 0].copy()
    base["_strongs"] = base["_strongs"].map(lambda x: x[0])

    if scope == "book" and book is not None:
        # Count only within the book
        count_base = base[base["book_id"] == book]
        count_col = "book_count"
    else:
        # Count across entire corpus
        count_base = base
        count_col = "corpus_count"

    counts = count_base.groupby("_strongs").size().rename(count_col)
    rare_strongs = counts[(counts >= min_count) & (counts <= max_count)].index

    if book is not None:
        hits = base[
            (base["book_id"] == book) &
            (base["_strongs"].isin(rare_strongs))
        ].copy()
    else:
        hits = base[base["_strongs"].isin(rare_strongs)].copy()

    if hits.empty:
        return pd.DataFrame(columns=["strongs", "lemma", "gloss", "word",
                                     "book_id", "chapter", "verse",
                                     "reference", count_col])

    hits = hits.rename(columns={"_strongs": "strongs_clean"})
    hits["reference"] = hits.apply(
        lambda r: f"{r['book_id']} {r['chapter']}:{r['verse']}", axis=1)
    hits[count_col] = hits["strongs_clean"].map(counts)

    # Keep first occurrence per strongs (canonical order)
    hits["_order"] = hits["book_id"].map(_BOOK_ORDER).fillna(99)
    hits = hits.sort_values(["_order", "chapter", "verse", "word_num"])

    # Deduplicate: one row per strongs, using first occurrence
    first_occ = hits.drop_duplicates(subset="strongs_clean", keep="first").copy()

    if include_gloss:
        glosses = first_occ["strongs_clean"].apply(_lookup_gloss)
        first_occ["lemma"] = glosses.map(lambda x: x[0])
        first_occ["gloss"] = glosses.map(lambda x: x[1])
    else:
        first_occ["lemma"] = ""
        first_occ["gloss"] = ""

    if include_context:
        first_occ["context_text"] = first_occ.apply(
            lambda r: _kjv_verse(r["book_id"], r["chapter"], r["verse"]), axis=1)

    out_cols = ["strongs_clean", "lemma", "gloss", "word",
                "book_id", "chapter", "verse", "reference", count_col]
    if include_context:
        out_cols.append("context_text")

    result = first_occ[out_cols].rename(columns={"strongs_clean": "strongs"})
    return result.reset_index(drop=True)


def hapax_summary(
    corpus: str = "OT",
    *,
    max_count: int = 1,
    part_of_speech: str | None = None,
) -> pd.DataFrame:
    """
    Count of hapax legomena per book, sorted descending.

    Parameters
    ----------
    corpus         : 'OT' or 'NT'
    max_count      : Maximum occurrences to qualify as hapax (default 1)
    part_of_speech : Filter by POS

    Returns
    -------
    DataFrame: book_id, book_name, hapax_count, total_lemmas, pct_hapax
    """
    df = _words()
    source = "TAHOT" if corpus.upper() == "OT" else "TAGNT"
    base = df[df["source"] == source].copy()

    if part_of_speech is not None:
        base = base[base["part_of_speech"].str.lower().str.contains(
            part_of_speech.lower(), na=False)]

    base["_strongs"] = base.apply(
        lambda r: _extract_strongs(r["strongs"], source), axis=1)
    base = base[base["_strongs"].map(len) > 0].copy()
    base["_strongs"] = base["_strongs"].map(lambda x: x[0])

    # Corpus-wide counts
    corpus_counts = base.groupby("_strongs").size()
    hapax_set = set(corpus_counts[corpus_counts <= max_count].index)

    base["_is_hapax"] = base["_strongs"].isin(hapax_set)

    book_ids = [b[0] for b in BOOKS if b[2] == corpus.upper()]

    rows = []
    for bk in book_ids:
        book_data = base[base["book_id"] == bk]
        if book_data.empty:
            continue
        total_lemmas = book_data["_strongs"].nunique()
        hapax_in_book = book_data[book_data["_is_hapax"]]["_strongs"].nunique()
        pct = round(hapax_in_book / total_lemmas * 100, 1) if total_lemmas else 0
        rows.append({
            "book_id": bk,
            "book_name": book_info(bk)["name"],
            "hapax_count": hapax_in_book,
            "total_lemmas": total_lemmas,
            "pct_hapax": pct,
        })

    result = pd.DataFrame(rows)
    result["_order"] = result["book_id"].map(_BOOK_ORDER).fillna(99)
    return result.sort_values("hapax_count", ascending=False).drop(
        columns="_order").reset_index(drop=True)


def hapax_table(
    book: str | None = None,
    corpus: str = "OT",
    *,
    top_n: int = 50,
    max_count: int = 1,
    part_of_speech: str | None = None,
    scope: str = "corpus",
) -> None:
    """
    Print a formatted hapax legomena table to the console.

    Parameters
    ----------
    book     : Restrict to a specific book (optional)
    corpus   : 'OT' or 'NT' (used when book is None)
    top_n    : Max rows to print
    max_count: Maximum occurrences to qualify
    scope    : 'corpus' or 'book'
    """
    df = hapax_legomena(
        corpus=corpus, book=book, max_count=max_count,
        part_of_speech=part_of_speech, scope=scope,
        include_gloss=True, include_context=True,
    )
    if df.empty:
        print("No hapax legomena found.")
        return

    title = "Hapax Legomena"
    if book:
        title += f" — {book_info(book)['name']}"
    else:
        title += f" — {corpus}"
    if max_count > 1:
        title += f" (≤{max_count} occurrences)"

    print(f"\n{'='*72}")
    print(f"  {title}  ({len(df)} unique lemmas)")
    print(f"{'='*72}")
    print(f"  {'Strongs':<10} {'Lemma':<18} {'Gloss':<28} {'Ref':<14}")
    print(f"  {'-'*68}")
    for _, row in df.head(top_n).iterrows():
        gloss = (row['gloss'] or '')[:27]
        lemma = (row['lemma'] or row['word'] or '')[:17]
        print(f"  {row['strongs']:<10} {lemma:<18} {gloss:<28} {row['reference']:<14}")
    if len(df) > top_n:
        print(f"  ... {len(df) - top_n} more")
    print()
