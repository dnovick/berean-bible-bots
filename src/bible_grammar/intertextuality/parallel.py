"""
Parallel passage viewer: Hebrew MT | LXX Greek | KJV side by side.

For OT passages, shows all three columns verse by verse.
For NT passages, shows Greek (TAGNT) | KJV.
Word-level detail is also available for deeper analysis.

Usage
-----
from bible_grammar.intertextuality.parallel import parallel_passage, print_parallel, parallel_words

# OT passage — three columns
parallel_passage('Gen', 1, 1, end_verse=5)

# NT passage — two columns
parallel_passage('Jhn', 1, 1, end_verse=14)

# Cross-chapter range
parallel_passage('Isa', 53, 1, end_chapter=53, end_verse=12)

# Print formatted to console
print_parallel('Gen', 1, 1, end_verse=5)

# Word-level detail for a single verse
parallel_words('Gen', 1, 1)
"""

from __future__ import annotations
import pandas as pd
from ..core import db as _db
from ..core.reference import book_info, BOOKS

_BOOK_ORDER = {b[0]: b[3] for b in BOOKS}

_OT_IDS = {b[0] for b in BOOKS if b[2] == "OT"}
_NT_IDS = {b[0] for b in BOOKS if b[2] == "NT"}


def _words() -> pd.DataFrame:
    return _db.load()


def _lxx() -> pd.DataFrame:
    return _db.load_lxx()


def _translations() -> pd.DataFrame:
    return _db.load_translations()


def _verse_text(df: pd.DataFrame, source: str,
                book_id: str, chapter: int, verse: int) -> str:
    """Reconstruct verse text by joining word tokens in order."""
    rows = df[
        (df["book_id"] == book_id) &
        (df["chapter"] == chapter) &
        (df["verse"] == verse) &
        (df["source"] == source)
    ].sort_values("word_num")
    return " ".join(rows["word"].tolist())


def _lxx_verse(lxx_df: pd.DataFrame, book_id: str, chapter: int, verse: int) -> str:
    rows = lxx_df[
        (lxx_df["book_id"] == book_id) &
        (lxx_df["chapter"] == chapter) &
        (lxx_df["verse"] == verse)
    ].sort_values("word_num")
    return " ".join(rows["word"].tolist())


def _kjv_verse(tr_df: pd.DataFrame, book_id: str, chapter: int, verse: int) -> str:
    row = tr_df[
        (tr_df["book_id"] == book_id) &
        (tr_df["chapter"] == chapter) &
        (tr_df["verse"] == verse) &
        (tr_df["translation"] == "KJV")
    ]
    return row.iloc[0]["text"] if not row.empty else ""


def _vulgate_verse(tr_df: pd.DataFrame, book_id: str, chapter: int, verse: int) -> str:
    row = tr_df[
        (tr_df["book_id"] == book_id) &
        (tr_df["chapter"] == chapter) &
        (tr_df["verse"] == verse) &
        (tr_df["translation"] == "VulgClementine")
    ]
    return row.iloc[0]["text"] if not row.empty else ""


def _verse_range(
    book_id: str,
    start_chapter: int, start_verse: int,
    end_chapter: int, end_verse: int,
) -> list[tuple[int, int]]:
    """Return list of (chapter, verse) pairs for a range."""
    book_info(book_id)
    # For simplicity, fetch all data and filter — handles cross-chapter ranges
    df = _words()
    source = "TAHOT" if book_id in _OT_IDS else "TAGNT"
    book_data = df[(df["book_id"] == book_id) & (df["source"] == source)]

    # Build sorted unique (chapter, verse) pairs within the range
    cv_pairs = (
        book_data[["chapter", "verse"]]
        .drop_duplicates()
        .sort_values(["chapter", "verse"])
    )

    result = []
    for _, row in cv_pairs.iterrows():
        ch, vs = int(row["chapter"]), int(row["verse"])
        if ch < start_chapter or (ch == start_chapter and vs < start_verse):
            continue
        if ch > end_chapter or (ch == end_chapter and vs > end_verse):
            break
        result.append((ch, vs))
    return result


def parallel_passage(
    book_id: str,
    start_chapter: int,
    start_verse: int,
    *,
    end_chapter: int | None = None,
    end_verse: int | None = None,
    include_lxx: bool = True,
    include_vulgate: bool = False,
) -> pd.DataFrame:
    """
    Build a verse-by-verse parallel passage table.

    Parameters
    ----------
    book_id        : Bible book ID (e.g. 'Gen', 'Isa', 'Jhn')
    start_chapter  : Starting chapter number
    start_verse    : Starting verse number
    end_chapter    : Ending chapter (defaults to start_chapter)
    end_verse      : Ending verse (defaults to start_verse)
    include_lxx    : Include LXX column for OT books (default True)
    include_vulgate: Include Latin Vulgate column (default False)

    Returns
    -------
    DataFrame with columns:
      reference, hebrew (OT) or greek_nt (NT), lxx (OT only), kjv, [vulgate]

    Examples
    --------
    parallel_passage('Gen', 1, 1, end_verse=5)
    parallel_passage('Isa', 53, 1, end_verse=12)
    parallel_passage('Jhn', 1, 1, end_verse=18)
    parallel_passage('Psa', 22, 1, end_verse=5)
    """
    if end_chapter is None:
        end_chapter = start_chapter
    if end_verse is None:
        end_verse = start_verse

    is_ot = book_id in _OT_IDS
    df = _words()
    lxx_df = _lxx() if is_ot and include_lxx else None
    tr_df = _translations()

    verses = _verse_range(book_id, start_chapter, start_verse, end_chapter, end_verse)
    if not verses:
        return pd.DataFrame(columns=["reference", "hebrew" if is_ot else "greek_nt",
                                     "lxx", "kjv"])

    rows = []
    source = "TAHOT" if is_ot else "TAGNT"
    for ch, vs in verses:
        ref = f"{book_id} {ch}:{vs}"
        orig = _verse_text(df, source, book_id, ch, vs)
        kjv = _kjv_verse(tr_df, book_id, ch, vs)
        row = {"reference": ref, "hebrew" if is_ot else "greek_nt": orig, "kjv": kjv}
        if is_ot and include_lxx:
            row["lxx"] = _lxx_verse(lxx_df, book_id, ch, vs)
        if include_vulgate:
            row["vulgate"] = _vulgate_verse(tr_df, book_id, ch, vs)
        rows.append(row)

    col_order = ["reference"]
    col_order += ["hebrew"] if is_ot else ["greek_nt"]
    if is_ot and include_lxx:
        col_order.append("lxx")
    col_order.append("kjv")
    if include_vulgate:
        col_order.append("vulgate")

    return pd.DataFrame(rows)[col_order]


def print_parallel(
    book_id: str,
    start_chapter: int,
    start_verse: int,
    *,
    end_chapter: int | None = None,
    end_verse: int | None = None,
    include_lxx: bool = True,
    include_vulgate: bool = False,
    width: int = 72,
) -> None:
    """
    Print a formatted parallel passage to the console.

    Each verse is printed as a block: reference header, then each
    text column labeled and wrapped.
    """
    if end_chapter is None:
        end_chapter = start_chapter
    if end_verse is None:
        end_verse = start_verse

    df = parallel_passage(
        book_id, start_chapter, start_verse,
        end_chapter=end_chapter, end_verse=end_verse,
        include_lxx=include_lxx, include_vulgate=include_vulgate,
    )

    is_ot = book_id in _OT_IDS
    info = book_info(book_id)

    end_ref = f"{end_chapter}:{end_verse}" if (
        end_chapter != start_chapter or end_verse != start_verse) else ""
    title = f"{info['name']} {start_chapter}:{start_verse}"
    if end_ref:
        title += f"–{end_ref}"
    print(f"\n{'='*width}")
    print(f"  {title}")
    print(f"{'='*width}")

    for _, row in df.iterrows():
        print(f"\n  {row['reference']}")
        print(f"  {'-'*(width-2)}")
        if is_ot:
            _print_col("  HEB", row.get("hebrew", ""), width)
            if "lxx" in row and row["lxx"]:
                _print_col("  LXX", row["lxx"], width)
        else:
            _print_col("   GK", row.get("greek_nt", ""), width)
        _print_col("  KJV", row["kjv"], width)
        if "vulgate" in row and row.get("vulgate"):
            _print_col("  VUL", row["vulgate"], width)

    print()


def _print_col(label: str, text: str, width: int) -> None:
    """Print a labeled, word-wrapped text column."""
    if not text:
        print(f"{label}: (no data)")
        return
    indent = " " * (len(label) + 2)
    words = text.split()
    line_words: list[str] = []
    first = True
    for w in words:
        line_words.append(w)
        if len(" ".join(line_words)) > width - len(label) - 4:
            prefix = f"{label}: " if first else indent
            print(prefix + " ".join(line_words[:-1]))
            line_words = [w]
            first = False
    if line_words:
        prefix = f"{label}: " if first else indent
        print(prefix + " ".join(line_words))


def parallel_words(
    book_id: str,
    chapter: int,
    verse: int,
    *,
    include_lxx: bool = True,
) -> dict:
    """
    Word-level parallel for a single verse.

    Returns a dict with:
      'reference': str
      'hebrew'   : DataFrame of TAHOT words (OT only)
      'lxx'      : DataFrame of LXX words (OT only)
      'greek_nt' : DataFrame of TAGNT words (NT only)
      'kjv'      : str
    """
    is_ot = book_id in _OT_IDS
    df = _words()
    tr_df = _translations()
    ref = f"{book_id} {chapter}:{verse}"

    result: dict = {"reference": ref}

    if is_ot:
        heb = df[
            (df["book_id"] == book_id) &
            (df["chapter"] == chapter) &
            (df["verse"] == verse) &
            (df["source"] == "TAHOT")
        ].sort_values("word_num")[
            ["word_num", "word", "transliteration", "translation",
             "strongs", "stem", "conjugation", "part_of_speech"]
        ].reset_index(drop=True)
        result["hebrew"] = heb

        if include_lxx:
            lxx_df = _lxx()
            lxx_v = lxx_df[
                (lxx_df["book_id"] == book_id) &
                (lxx_df["chapter"] == chapter) &
                (lxx_df["verse"] == verse)
            ].sort_values("word_num")[
                ["word_num", "word", "transliteration", "translation",
                 "lemma", "lemma_translit", "strongs",
                 "tense", "voice", "mood", "part_of_speech"]
            ].reset_index(drop=True)
            result["lxx"] = lxx_v
    else:
        nt = df[
            (df["book_id"] == book_id) &
            (df["chapter"] == chapter) &
            (df["verse"] == verse) &
            (df["source"] == "TAGNT")
        ].sort_values("word_num")[
            ["word_num", "word", "transliteration", "translation",
             "strongs", "tense", "voice", "mood", "part_of_speech"]
        ].reset_index(drop=True)
        result["greek_nt"] = nt

    result["kjv"] = _kjv_verse(tr_df, book_id, chapter, verse)
    return result
