"""
Hebrew MT ↔ LXX translation equivalence analysis.

Since no freely-available word-level alignment dataset exists, this module uses
verse-level co-occurrence statistics: for each OT verse, it pairs every Hebrew
word (from TAHOT) with every Greek word (from LXX) in the same verse, then
aggregates co-occurrence counts across the corpus.

This is a standard statistical approach to translation equivalence in computational
biblical studies (cf. Tov 1999, Lust et al.), and works well for:
  - High-frequency verbs with consistent translations (e.g., עָשָׂה → ποιέω)
  - Asking "which Greek lemmas most often appear alongside Niphal of נָגַד?"
  - Comparing how different Hebrew stems of the same root are rendered in LXX

Limitations:
  - Multi-word verses introduce noise (a Greek word may co-occur with many
    Hebrew words in a long verse even if it only translates one of them)
  - Short verses (~3-5 words) give much tighter, more reliable pairings
  - Untranslated / added words in the LXX are not distinguished
"""

from __future__ import annotations
import pandas as pd
from pathlib import Path
from . import db as _db

_REPO_ROOT = Path(__file__).resolve().parents[2]
_PROCESSED = _REPO_ROOT / "data" / "processed"
ALIGNMENT_PARQUET = _PROCESSED / "alignment.parquet"


def build_alignment(
    heb_df: pd.DataFrame | None = None,
    lxx_df: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """
    Build verse-level co-occurrence alignment between TAHOT and LXX.

    Returns a DataFrame with columns:
      book_id, chapter, verse,
      heb_word, heb_strongs, heb_stem, heb_conjugation, heb_part_of_speech,
      lxx_word, lxx_lemma, lxx_lemma_translit, lxx_strongs, lxx_part_of_speech,
      lxx_tense, lxx_voice, lxx_mood

    One row per (Hebrew word, Greek word) pair in the same verse.
    """
    if heb_df is None:
        heb_df = _db.load()
    if lxx_df is None:
        lxx_df = _db.load_lxx()

    # Hebrew: OT only, keep relevant columns
    heb = heb_df[heb_df["source"] == "TAHOT"][[
        "book_id", "chapter", "verse",
        "word", "strongs", "stem", "conjugation", "part_of_speech",
    ]].copy()
    heb.columns = [
        "book_id", "chapter", "verse",
        "heb_word", "heb_strongs", "heb_stem", "heb_conjugation", "heb_pos",
    ]

    # LXX: canonical books only, keep relevant columns
    lxx = lxx_df[~lxx_df["is_deuterocanon"]][[
        "book_id", "chapter", "verse",
        "word", "lemma", "lemma_translit", "strongs", "part_of_speech",
        "tense", "voice", "mood",
    ]].copy()
    lxx.columns = [
        "book_id", "chapter", "verse",
        "lxx_word", "lxx_lemma", "lxx_lemma_translit", "lxx_strongs",
        "lxx_pos", "lxx_tense", "lxx_voice", "lxx_mood",
    ]

    # Cross-join on (book_id, chapter, verse) — every Hebrew word paired with
    # every Greek word in the same verse
    merged = heb.merge(lxx, on=["book_id", "chapter", "verse"], how="inner")
    return merged


def save_alignment(df: pd.DataFrame | None = None) -> pd.DataFrame:
    """Build (if needed) and save the alignment table."""
    if df is None:
        print("  Building verse-level Hebrew↔LXX alignment pairs...")
        df = build_alignment()
    df.to_parquet(ALIGNMENT_PARQUET, index=False)
    print(f"  Saved alignment: {ALIGNMENT_PARQUET}  ({len(df):,} pairs)")
    return df


def load_alignment() -> pd.DataFrame:
    if ALIGNMENT_PARQUET.exists():
        return pd.read_parquet(ALIGNMENT_PARQUET)
    raise FileNotFoundError(
        "No alignment data found. Run: python scripts/build_db.py"
    )


def translation_equivalents(
    *,
    heb_strongs: str | None = None,
    heb_stem: str | None = None,
    heb_conjugation: str | None = None,
    heb_pos: str | None = None,
    lxx_pos: str | None = None,
    book: str | list[str] | None = None,
    book_group: str | None = None,
    min_count: int = 2,
    top_n: int = 20,
) -> pd.DataFrame:
    """
    Find the most common LXX Greek lemmas that co-occur with a Hebrew word/stem.

    Parameters
    ----------
    heb_strongs    : Hebrew Strong's number, e.g. 'H1254' (בָּרָא) or '{H1254A}'
    heb_stem       : Stem filter, e.g. 'Niphal', 'Qal', 'Piel'
    heb_conjugation: Conjugation filter, e.g. 'Perfect', 'Imperfect'
    heb_pos        : Part of speech filter, e.g. 'Verb', 'Noun'
    book           : Restrict to a book or list of books
    book_group     : 'torah', 'prophets', 'writings', etc.
    min_count      : Minimum co-occurrence count to include
    top_n          : Return top N lemmas by count

    Returns a DataFrame ranked by co-occurrence count:
      lxx_lemma, lxx_lemma_translit, lxx_strongs, lxx_pos,
      count, pct (percentage of total matches)

    Examples
    --------
    # What Greek lemmas translate בָּרָא (H1254)?
    translation_equivalents(heb_strongs='H1254')

    # How is the Niphal of נָתַן (H5414) rendered in the LXX?
    translation_equivalents(heb_strongs='H5414', heb_stem='Niphal')

    # What Greek verbs translate Qal verbs in Isaiah?
    translation_equivalents(heb_pos='Verb', heb_stem='Qal', book='Isa')
    """
    from .reference import book_ids_for_group

    df = load_alignment()

    mask = pd.Series(True, index=df.index)

    if heb_strongs is not None:
        # Strip curly braces and suffix letters from TAHOT strongs like {H1254A}
        clean = heb_strongs.strip("{}").upper()
        mask &= df["heb_strongs"].str.upper().str.contains(clean, na=False)
    if heb_stem is not None:
        mask &= df["heb_stem"].str.lower().str.contains(heb_stem.lower(), na=False)
    if heb_conjugation is not None:
        mask &= df["heb_conjugation"].str.lower().str.contains(
            heb_conjugation.lower(), na=False)
    if heb_pos is not None:
        mask &= df["heb_pos"].str.lower().str.contains(heb_pos.lower(), na=False)
    if lxx_pos is not None:
        mask &= df["lxx_pos"].str.lower().str.contains(lxx_pos.lower(), na=False)
    if book is not None:
        vals = [book] if isinstance(book, str) else book
        mask &= df["book_id"].isin(vals)
    if book_group is not None:
        mask &= df["book_id"].isin(book_ids_for_group(book_group))

    filtered = df[mask]
    if filtered.empty:
        return pd.DataFrame(columns=[
            "lxx_lemma", "lxx_lemma_translit", "lxx_strongs",
            "lxx_pos", "count", "pct"
        ])

    counts = (
        filtered.groupby(["lxx_lemma", "lxx_lemma_translit", "lxx_strongs", "lxx_pos"])
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )
    counts = counts[counts["count"] >= min_count].head(top_n)
    total = counts["count"].sum()
    counts["pct"] = (counts["count"] / total * 100).round(1)
    return counts.reset_index(drop=True)


def hebrew_sources(
    *,
    lxx_lemma: str | None = None,
    lxx_strongs: str | None = None,
    heb_stem: str | None = None,
    heb_pos: str | None = None,
    book: str | list[str] | None = None,
    min_count: int = 2,
    top_n: int = 20,
) -> pd.DataFrame:
    """
    Reverse lookup: given a Greek LXX lemma, what Hebrew roots/stems does it translate?

    Parameters
    ----------
    lxx_lemma  : Greek lemma (Unicode), e.g. 'ποιέω'
    lxx_strongs: Greek Strong's, e.g. 'G4160'
    heb_stem   : Filter Hebrew results by stem
    book       : Restrict to a book or list
    min_count  : Minimum co-occurrence count
    top_n      : Return top N results

    Returns a DataFrame ranked by count:
      heb_strongs, heb_stem, heb_pos, count, pct

    Examples
    --------
    # What Hebrew roots does ποιέω translate?
    hebrew_sources(lxx_lemma='ποιέω')

    # What Hebrew stems does κύριος come from?
    hebrew_sources(lxx_strongs='G2962')
    """
    df = load_alignment()
    mask = pd.Series(True, index=df.index)

    if lxx_lemma is not None:
        mask &= df["lxx_lemma"].str.lower() == lxx_lemma.lower()
    if lxx_strongs is not None:
        mask &= df["lxx_strongs"].str.upper() == lxx_strongs.upper()
    if heb_stem is not None:
        mask &= df["heb_stem"].str.lower().str.contains(heb_stem.lower(), na=False)
    if heb_pos is not None:
        mask &= df["heb_pos"].str.lower().str.contains(heb_pos.lower(), na=False)
    if book is not None:
        vals = [book] if isinstance(book, str) else book
        mask &= df["book_id"].isin(vals)

    filtered = df[mask]
    if filtered.empty:
        return pd.DataFrame(columns=["heb_strongs", "heb_stem", "heb_pos", "count", "pct"])

    counts = (
        filtered.groupby(["heb_strongs", "heb_stem", "heb_pos"])
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )
    counts = counts[counts["count"] >= min_count].head(top_n)
    total = counts["count"].sum()
    counts["pct"] = (counts["count"] / total * 100).round(1)
    return counts.reset_index(drop=True)
