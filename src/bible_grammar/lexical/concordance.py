"""
Concordance: find all occurrences of a Hebrew or Greek lemma with verse context.

Works across all three corpora:
  - TAHOT  (Hebrew/Aramaic OT) — match on strongs or surface word
  - TAGNT  (Greek NT)          — match on strongs or surface word
  - LXX    (Greek OT)          — match on lemma, lemma_translit, or strongs

Usage
-----
from bible_grammar.lexical.concordance import concordance, lemma_frequency

# Every occurrence of בָּרָא (H1254) in the OT
concordance(strongs='H1254')

# Qal stem only, with KJV context
concordance(strongs='H1254', stem='Qal', context='KJV')

# Greek ποιέω in NT
concordance(strongs='G4160', corpus='NT')

# ποιέω in LXX with book filter
concordance(strongs='G4160', corpus='LXX', book='Gen')

# Frequency table: how often does each lemma appear?
lemma_frequency(strongs='H5414', corpus='OT')
"""

from __future__ import annotations
import pandas as pd
from ..core import db as _db
from ..core.reference import BOOKS, book_ids_for_group

_BOOK_ORDER = {b[0]: b[3] for b in BOOKS}


def _words() -> pd.DataFrame:
    return _db.load()


def _lxx() -> pd.DataFrame:
    return _db.load_lxx()


def _translations() -> pd.DataFrame:
    return _db.load_translations()


def _verse_text(book_id: str, chapter: int, verse: int, translation: str = "KJV") -> str:
    tr = _translations()
    row = tr[
        (tr["book_id"] == book_id) &
        (tr["chapter"] == chapter) &
        (tr["verse"] == verse) &
        (tr["translation"] == translation)
    ]
    if row.empty:
        return ""
    return row.iloc[0]["text"]


def _reconstruct_hebrew(book_id: str, chapter: int, verse: int) -> str:
    """Join TAHOT word tokens into a verse string (right-to-left display order)."""
    df = _words()
    verse_words = df[
        (df["book_id"] == book_id) &
        (df["chapter"] == chapter) &
        (df["verse"] == verse) &
        (df["source"] == "TAHOT")
    ].sort_values("word_num")
    if verse_words.empty:
        return ""
    return " ".join(verse_words["word"].tolist())


def _reconstruct_lxx(book_id: str, chapter: int, verse: int) -> str:
    """Join LXX word tokens into a verse string."""
    df = _lxx()
    verse_words = df[
        (df["book_id"] == book_id) &
        (df["chapter"] == chapter) &
        (df["verse"] == verse)
    ].sort_values("word_num")
    if verse_words.empty:
        return ""
    return " ".join(verse_words["word"].tolist())


def _reconstruct_nt(book_id: str, chapter: int, verse: int) -> str:
    """Join TAGNT word tokens into a verse string."""
    df = _words()
    verse_words = df[
        (df["book_id"] == book_id) &
        (df["chapter"] == chapter) &
        (df["verse"] == verse) &
        (df["source"] == "TAGNT")
    ].sort_values("word_num")
    if verse_words.empty:
        return ""
    return " ".join(verse_words["word"].tolist())


def concordance(
    *,
    strongs: str | None = None,
    word: str | None = None,
    lemma: str | None = None,
    lemma_translit: str | None = None,
    stem: str | None = None,
    part_of_speech: str | None = None,
    corpus: str = "OT",
    book: str | list[str] | None = None,
    book_group: str | None = None,
    context: str | None = "KJV",
    include_hebrew: bool = True,
    include_lxx: bool = False,
    sort_by: str = "canonical",
) -> pd.DataFrame:
    """
    Find all occurrences of a lemma with verse context.

    Parameters
    ----------
    strongs        : Strong's number, e.g. 'H1254' or 'G4160'
    word           : Match on surface word form (partial match)
    lemma          : Match on lemma (LXX Unicode lemma, e.g. 'ποιέω')
    lemma_translit : Match on LXX transliterated lemma, e.g. 'poieo'
    stem           : Filter by Hebrew stem (Qal, Niphal, etc.)
    part_of_speech : Filter by POS (Verb, Noun, etc.)
    corpus         : 'OT', 'NT', or 'LXX'
    book           : book_id or list of book_ids to restrict search
    book_group     : 'torah', 'prophets', 'writings', 'gospels', 'pauline'
    context        : 'KJV', 'Vulgate', 'Hebrew', 'Greek', or None for no context
    include_hebrew : Include Hebrew word column in output (OT only)
    include_lxx    : Also search the LXX when corpus='OT'
    sort_by        : 'canonical' (Bible order) or 'book' (alphabetical)

    Returns
    -------
    DataFrame with columns:
      reference, book_id, chapter, verse,
      word, strongs, [stem, part_of_speech, ...morphology...],
      context_text
    """
    if corpus.upper() == "LXX":
        return _concordance_lxx(
            strongs=strongs, word=word, lemma=lemma,
            lemma_translit=lemma_translit,
            part_of_speech=part_of_speech,
            book=book, book_group=book_group,
            context=context, sort_by=sort_by,
        )

    source = "TAHOT" if corpus.upper() == "OT" else "TAGNT"
    df = _words()
    mask = df["source"] == source

    if strongs is not None:
        clean = strongs.strip("{}").upper()
        mask &= df["strongs"].str.upper().str.contains(clean, na=False)
    if word is not None:
        mask &= df["word"].str.contains(word, na=False)
    if stem is not None:
        mask &= df["stem"].str.lower().str.contains(stem.lower(), na=False)
    if part_of_speech is not None:
        mask &= df["part_of_speech"].str.lower().str.contains(
            part_of_speech.lower(), na=False)
    if book is not None:
        vals = [book] if isinstance(book, str) else book
        mask &= df["book_id"].isin(vals)
    if book_group is not None:
        mask &= df["book_id"].isin(book_ids_for_group(book_group))

    hits = df[mask].copy()
    if hits.empty:
        return pd.DataFrame(columns=["reference", "book_id", "chapter", "verse",
                                     "word", "strongs", "context_text"])

    # Build reference string and attach context
    hits["reference"] = hits.apply(
        lambda r: f"{r['book_id']} {r['chapter']}:{r['verse']}", axis=1)

    if context == "KJV":
        hits["context_text"] = hits.apply(
            lambda r: _verse_text(r["book_id"], r["chapter"], r["verse"], "KJV"), axis=1)
    elif context in ("Vulgate", "VulgClementine"):
        hits["context_text"] = hits.apply(
            lambda r: _verse_text(r["book_id"], r["chapter"], r["verse"], "VulgClementine"), axis=1)
    elif context == "Hebrew":
        hits["context_text"] = hits.apply(
            lambda r: _reconstruct_hebrew(r["book_id"], r["chapter"], r["verse"]), axis=1)
    elif context == "Greek":
        hits["context_text"] = hits.apply(
            lambda r: _reconstruct_nt(r["book_id"], r["chapter"], r["verse"]), axis=1)
    else:
        hits["context_text"] = ""

    # Sort
    hits["_order"] = hits["book_id"].map(_BOOK_ORDER).fillna(99)
    hits = hits.sort_values(["_order", "chapter", "verse", "word_num"])

    keep_cols = ["reference", "book_id", "chapter", "verse", "word_num",
                 "word", "strongs"]
    if corpus.upper() == "OT":
        keep_cols += ["stem", "conjugation", "part_of_speech", "state"]
    else:
        keep_cols += ["tense", "voice", "mood", "part_of_speech"]
    keep_cols.append("context_text")
    keep_cols = [c for c in keep_cols if c in hits.columns]

    return hits[keep_cols].reset_index(drop=True)


def _concordance_lxx(
    *,
    strongs: str | None,
    word: str | None,
    lemma: str | None,
    lemma_translit: str | None,
    part_of_speech: str | None,
    book: str | list[str] | None,
    book_group: str | None,
    context: str | None,
    sort_by: str,
) -> pd.DataFrame:
    df = _lxx()
    mask = pd.Series(True, index=df.index)

    if strongs is not None:
        clean = strongs.strip("{}").upper()
        mask &= df["strongs"].str.upper().str.contains(clean, na=False)
    if word is not None:
        mask &= df["word"].str.contains(word, na=False)
    if lemma is not None:
        mask &= df["lemma"].str.lower() == lemma.lower()
    if lemma_translit is not None:
        mask &= df["lemma_translit"].str.lower().str.contains(
            lemma_translit.lower(), na=False)
    if part_of_speech is not None:
        mask &= df["part_of_speech"].str.lower().str.contains(
            part_of_speech.lower(), na=False)
    if book is not None:
        vals = [book] if isinstance(book, str) else book
        mask &= df["book_id"].isin(vals)
    if book_group is not None:
        mask &= df["book_id"].isin(book_ids_for_group(book_group))

    # Exclude deuterocanon by default unless explicitly requested
    mask &= ~df["is_deuterocanon"]

    hits = df[mask].copy()
    if hits.empty:
        return pd.DataFrame(columns=["reference", "book_id", "chapter", "verse",
                                     "word", "lemma", "strongs", "context_text"])

    hits["reference"] = hits.apply(
        lambda r: f"{r['book_id']} {r['chapter']}:{r['verse']}", axis=1)

    if context == "KJV":
        hits["context_text"] = hits.apply(
            lambda r: _verse_text(r["book_id"], r["chapter"], r["verse"], "KJV"), axis=1)
    elif context in ("Vulgate", "VulgClementine"):
        hits["context_text"] = hits.apply(
            lambda r: _verse_text(r["book_id"], r["chapter"], r["verse"], "VulgClementine"), axis=1)
    elif context == "Greek":
        hits["context_text"] = hits.apply(
            lambda r: _reconstruct_lxx(r["book_id"], r["chapter"], r["verse"]), axis=1)
    else:
        hits["context_text"] = ""

    hits["_order"] = hits["book_id"].map(_BOOK_ORDER).fillna(99)
    hits = hits.sort_values(["_order", "chapter", "verse", "word_num"])

    keep_cols = ["reference", "book_id", "chapter", "verse", "word_num",
                 "word", "lemma", "lemma_translit", "strongs",
                 "tense", "voice", "mood", "part_of_speech", "context_text"]
    keep_cols = [c for c in keep_cols if c in hits.columns]
    return hits[keep_cols].reset_index(drop=True)


def lemma_frequency(
    *,
    strongs: str | None = None,
    stem: str | None = None,
    part_of_speech: str | None = None,
    corpus: str = "OT",
    book_group: str | None = None,
    top_n: int = 50,
) -> pd.DataFrame:
    """
    Frequency breakdown of a lemma by book.

    Parameters
    ----------
    strongs        : Strong's number
    stem           : Filter by Hebrew stem
    part_of_speech : Filter by POS
    corpus         : 'OT', 'NT', or 'LXX'
    book_group     : Limit to a named group
    top_n          : Top N books by count

    Returns a DataFrame: book_id, book_name, count, pct
    """
    from ..core.reference import book_info

    df = concordance(
        strongs=strongs, stem=stem, part_of_speech=part_of_speech,
        corpus=corpus, book_group=book_group, context=None,
    )
    if df.empty:
        return pd.DataFrame(columns=["book_id", "book_name", "count", "pct"])

    counts = (
        df.groupby("book_id")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(top_n)
    )
    counts["book_name"] = counts["book_id"].apply(
        lambda b: book_info(b)["name"] if b in {bk[0] for bk in BOOKS} else b)
    counts["_order"] = counts["book_id"].map(_BOOK_ORDER).fillna(99)
    counts = counts.sort_values("_order").drop(columns="_order")
    total = counts["count"].sum()
    counts["pct"] = (counts["count"] / total * 100).round(1)
    return counts[["book_id", "book_name", "count", "pct"]].reset_index(drop=True)


def top_lemmas(
    *,
    corpus: str = "OT",
    part_of_speech: str | None = None,
    stem: str | None = None,
    book: str | list[str] | None = None,
    book_group: str | None = None,
    top_n: int = 30,
    min_count: int = 1,
) -> pd.DataFrame:
    """
    Most frequent lemmas (by Strong's number) across a corpus or book set.

    Returns a DataFrame: strongs, count, pct
    """
    if corpus.upper() == "LXX":
        df = _lxx()
        mask = ~df["is_deuterocanon"]
    else:
        source = "TAHOT" if corpus.upper() == "OT" else "TAGNT"
        df = _words()
        mask = df["source"] == source

    if part_of_speech is not None:
        mask &= df["part_of_speech"].str.lower().str.contains(
            part_of_speech.lower(), na=False)
    if stem is not None and corpus.upper() != "LXX":
        mask &= df["stem"].str.lower().str.contains(stem.lower(), na=False)
    if book is not None:
        vals = [book] if isinstance(book, str) else book
        mask &= df["book_id"].isin(vals)
    if book_group is not None:
        mask &= df["book_id"].isin(book_ids_for_group(book_group))

    counts = (
        df[mask]
        .groupby("strongs")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )
    counts = counts[counts["count"] >= min_count].head(top_n)
    total = counts["count"].sum()
    counts["pct"] = (counts["count"] / total * 100).round(1)
    return counts.reset_index(drop=True)
