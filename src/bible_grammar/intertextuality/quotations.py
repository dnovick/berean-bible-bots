"""
NT quotations / allusions of the OT — three-way text comparison.

Cross-reference data from scrollmapper (OpenBible.info CC-BY).
For each NT→OT reference pair, retrieves:
  - NT verse (TAGNT Greek word forms)
  - OT Hebrew verse (TAHOT)
  - LXX Greek verse (CenterBLC/LXX)

Usage
-----
from bible_grammar.intertextuality.quotations import nt_quotations, verse_comparison

# All NT→OT references with votes >= 50
df = nt_quotations(min_votes=50)

# Detailed three-way comparison for a specific NT verse
cmp = verse_comparison('Heb', 2, 8)
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd
from ..core import db as _db

_REPO_ROOT = Path(__file__).resolve().parents[2]
_XREF_FILE = _REPO_ROOT / "scrollmapper-data" / "sources_backup" / "extras" / "cross_references.txt"

# Map scrollmapper abbreviations → our book_id codes
_SM_TO_BOOK_ID: dict[str, str] = {
    "Gen": "Gen", "Exod": "Exo", "Lev": "Lev", "Num": "Num", "Deut": "Deu",
    "Josh": "Jos", "Judg": "Jdg", "Ruth": "Rut", "1Sam": "1Sa", "2Sam": "2Sa",
    "1Kgs": "1Ki", "2Kgs": "2Ki", "1Chr": "1Ch", "2Chr": "2Ch",
    "Ezra": "Ezr", "Neh": "Neh", "Esth": "Est", "Job": "Job", "Ps": "Psa",
    "Prov": "Pro", "Eccl": "Ecc", "Song": "Sng", "Isa": "Isa", "Jer": "Jer",
    "Lam": "Lam", "Ezek": "Ezk", "Dan": "Dan", "Hos": "Hos", "Joel": "Jol",
    "Amos": "Amo", "Obad": "Oba", "Jonah": "Jon", "Mic": "Mic", "Nah": "Nah",
    "Hab": "Hab", "Zeph": "Zep", "Hag": "Hag", "Zech": "Zec", "Mal": "Mal",
    "Matt": "Mat", "Mark": "Mrk", "Luke": "Luk", "John": "Jhn", "Acts": "Act",
    "Rom": "Rom", "1Cor": "1Co", "2Cor": "2Co", "Gal": "Gal", "Eph": "Eph",
    "Phil": "Php", "Col": "Col", "1Thess": "1Th", "2Thess": "2Th",
    "1Tim": "1Ti", "2Tim": "2Ti", "Titus": "Tit", "Phlm": "Phm",
    "Heb": "Heb", "Jas": "Jas", "1Pet": "1Pe", "2Pet": "2Pe",
    "1John": "1Jn", "2John": "2Jn", "3John": "3Jn", "Jude": "Jud",
    "Rev": "Rev",
}

_NT_IDS = {
    "Mat", "Mrk", "Luk", "Jhn", "Act", "Rom", "1Co", "2Co", "Gal", "Eph",
    "Php", "Col", "1Th", "2Th", "1Ti", "2Ti", "Tit", "Phm", "Heb", "Jas",
    "1Pe", "2Pe", "1Jn", "2Jn", "3Jn", "Jud", "Rev",
}

_OT_IDS = {
    "Gen", "Exo", "Lev", "Num", "Deu", "Jos", "Jdg", "Rut", "1Sa", "2Sa",
    "1Ki", "2Ki", "1Ch", "2Ch", "Ezr", "Neh", "Est", "Job", "Psa", "Pro",
    "Ecc", "Sng", "Isa", "Jer", "Lam", "Ezk", "Dan", "Hos", "Jol", "Amo",
    "Oba", "Jon", "Mic", "Nah", "Hab", "Zep", "Hag", "Zec", "Mal",
}

_xref_cache: pd.DataFrame | None = None


def _load_xrefs() -> pd.DataFrame:
    global _xref_cache
    if _xref_cache is not None:
        return _xref_cache

    if not _XREF_FILE.exists():
        raise FileNotFoundError(
            f"Cross-reference file not found: {_XREF_FILE}\n"
            "Make sure the scrollmapper-data submodule is initialized."
        )

    rows = []
    with open(_XREF_FILE, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("From"):
                continue
            parts = line.split("\t")
            if len(parts) < 3:
                continue
            from_ref, to_ref, votes_str = parts[0], parts[1], parts[2]
            try:
                votes = int(votes_str.split("#")[0].strip())
            except ValueError:
                continue

            from_book, from_ch, from_vs = _parse_ref(from_ref)
            to_ref_first = to_ref.split("-")[0]  # handle ranges like Prov.8.22-Prov.8.30
            to_book, to_ch, to_vs = _parse_ref(to_ref_first)

            if from_book is None or to_book is None:
                continue

            rows.append({
                "from_book": from_book, "from_chapter": from_ch, "from_verse": from_vs,
                "to_book":   to_book,   "to_chapter":   to_ch,   "to_verse":   to_vs,
                "votes": votes,
                "from_ref_raw": from_ref,
                "to_ref_raw": to_ref,
            })

    _xref_cache = pd.DataFrame(rows)
    return _xref_cache


def _parse_ref(ref: str) -> tuple[str | None, int, int]:
    """Parse 'Book.chapter.verse' → (book_id, chapter, verse)."""
    parts = ref.strip().split(".")
    if len(parts) < 3:
        return None, 0, 0
    sm_book = parts[0]
    book_id = _SM_TO_BOOK_ID.get(sm_book)
    try:
        ch = int(parts[1])
        vs = int(parts[2])
    except ValueError:
        return None, 0, 0
    return book_id, ch, vs


def nt_quotations(
    *,
    nt_book: str | list[str] | None = None,
    ot_book: str | list[str] | None = None,
    min_votes: int = 10,
    top_n: int | None = None,
) -> pd.DataFrame:
    """
    Return NT→OT cross-references, filtered by relevance vote score.

    Parameters
    ----------
    nt_book   : Restrict NT side to one or more book_ids (e.g. 'Heb', 'Rom')
    ot_book   : Restrict OT side to one or more book_ids (e.g. 'Isa', 'Psa')
    min_votes : Minimum vote score (higher = stronger consensus). Default 10.
                Use >= 50 for probable direct quotes; >= 100 for certain quotes.
    top_n     : Return only the top N results sorted by votes descending.

    Returns
    -------
    DataFrame with columns:
      nt_book, nt_chapter, nt_verse,
      ot_book, ot_chapter, ot_verse,
      votes, from_ref_raw, to_ref_raw
    """
    xrefs = _load_xrefs()

    # Filter to NT→OT direction only
    mask = xrefs["from_book"].isin(_NT_IDS) & xrefs["to_book"].isin(_OT_IDS)
    df = xrefs[mask].copy()
    df = df.rename(columns={
        "from_book": "nt_book", "from_chapter": "nt_chapter", "from_verse": "nt_verse",
        "to_book":   "ot_book", "to_chapter":   "ot_chapter", "to_verse":   "ot_verse",
    })

    if min_votes is not None:
        df = df[df["votes"] >= min_votes]
    if nt_book is not None:
        books = [nt_book] if isinstance(nt_book, str) else nt_book
        df = df[df["nt_book"].isin(books)]
    if ot_book is not None:
        books = [ot_book] if isinstance(ot_book, str) else ot_book
        df = df[df["ot_book"].isin(books)]

    df = df.sort_values("votes", ascending=False).reset_index(drop=True)
    if top_n is not None:
        df = df.head(top_n)
    return df


def verse_comparison(
    book: str,
    chapter: int,
    verse: int,
    *,
    min_votes: int = 5,
) -> dict:
    """
    Three-way comparison for an NT verse: NT Greek | OT Hebrew | LXX Greek.

    Parameters
    ----------
    book, chapter, verse : NT verse reference (book_id, e.g. 'Heb')
    min_votes            : Minimum vote threshold for cross-references to include

    Returns a dict with:
      'nt'  : list of word dicts (word, lemma, strongs, pos, tense, voice, mood)
      'refs': list of {ot_ref, ot_words, lxx_words, votes} dicts, one per OT target
    """
    words_df = _db.load()
    lxx_df = _db.load_lxx()

    # NT words for this verse
    nt_words = words_df[
        (words_df["book_id"] == book) &
        (words_df["chapter"] == chapter) &
        (words_df["verse"] == verse) &
        (words_df["source"] == "TAGNT")
    ].copy()

    nt_list = nt_words[[
        "word", "strongs", "part_of_speech", "conjugation",
        "stem", "person", "number", "gender",
    ]].to_dict("records")

    # Cross-refs from this NT verse to OT
    xrefs = nt_quotations(nt_book=book, min_votes=min_votes)
    xrefs = xrefs[
        (xrefs["nt_chapter"] == chapter) & (xrefs["nt_verse"] == verse)
    ]

    refs = []
    for _, row in xrefs.iterrows():
        ot_b, ot_ch, ot_vs = row["ot_book"], row["ot_chapter"], row["ot_verse"]

        ot_words = words_df[
            (words_df["book_id"] == ot_b) &
            (words_df["chapter"] == ot_ch) &
            (words_df["verse"] == ot_vs) &
            (words_df["source"] == "TAHOT")
        ][["word", "strongs", "stem", "part_of_speech"]].to_dict("records")

        lxx_words = lxx_df[
            (lxx_df["book_id"] == ot_b) &
            (lxx_df["chapter"] == ot_ch) &
            (lxx_df["verse"] == ot_vs)
        ][["word", "lemma", "lemma_translit", "strongs", "part_of_speech",
           "tense", "voice", "mood"]].to_dict("records")

        refs.append({
            "ot_ref": f"{ot_b} {ot_ch}:{ot_vs}",
            "ot_book": ot_b, "ot_chapter": ot_ch, "ot_verse": ot_vs,
            "votes": row["votes"],
            "ot_words": ot_words,
            "lxx_words": lxx_words,
        })

    return {"nt_ref": f"{book} {chapter}:{verse}", "nt": nt_list, "refs": refs}


def quotation_table(
    book: str,
    chapter: int,
    verse: int,
    *,
    min_votes: int = 5,
) -> pd.DataFrame:
    """
    Tabular form of verse_comparison — one row per (NT word position, OT ref),
    suitable for display in a notebook.

    Columns: nt_verse_ref, ot_verse_ref, votes,
             nt_words (space-joined), ot_words (space-joined), lxx_words (space-joined)
    """
    cmp = verse_comparison(book, chapter, verse, min_votes=min_votes)
    nt_text = " ".join(w["word"] for w in cmp["nt"]) if cmp["nt"] else "(no data)"
    rows = []
    for ref in cmp["refs"]:
        ot_text = " ".join(w["word"] for w in ref["ot_words"]) or "(no data)"
        lxx_text = " ".join(w["word"] for w in ref["lxx_words"]) or "(no data)"
        rows.append({
            "nt_ref":    cmp["nt_ref"],
            "ot_ref":    ref["ot_ref"],
            "votes":     ref["votes"],
            "nt_text":   nt_text,
            "ot_text":   ot_text,
            "lxx_text":  lxx_text,
        })
    if not rows:
        return pd.DataFrame(columns=[
            "nt_ref", "ot_ref", "votes", "nt_text", "ot_text", "lxx_text"
        ])
    return pd.DataFrame(rows)


def quotation_summary(
    *,
    nt_book: str | list[str] | None = None,
    ot_book: str | list[str] | None = None,
    min_votes: int = 25,
) -> pd.DataFrame:
    """
    Summarize NT→OT quotation density: how many quotation pairs per NT book.

    Returns a DataFrame with columns:
      nt_book, total_references, unique_nt_verses, unique_ot_verses, top_ot_source
    """
    df = nt_quotations(nt_book=nt_book, ot_book=ot_book, min_votes=min_votes)
    if df.empty:
        return pd.DataFrame(columns=[
            "nt_book", "total_references", "unique_nt_verses",
            "unique_ot_verses", "top_ot_source"
        ])

    def _top_ot(sub: pd.DataFrame) -> str:
        return sub["ot_book"].value_counts().index[0]

    summary = (
        df.groupby("nt_book")
        .agg(
            total_references=("votes", "count"),
            unique_nt_verses=("nt_verse", "nunique"),
            unique_ot_verses=("ot_verse", "nunique"),
            top_ot_source=("ot_book", lambda s: s.value_counts().index[0]),
        )
        .reset_index()
        .sort_values("total_references", ascending=False)
    )
    return summary
