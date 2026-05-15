"""Frequency tables and aggregation helpers."""

from __future__ import annotations
import pandas as pd
from ..core.query import query as _query


def freq_table(df: pd.DataFrame, groupby: str | list[str],
               sort: bool = True) -> pd.DataFrame:
    """Return a count DataFrame grouped by one or more columns."""
    cols = [groupby] if isinstance(groupby, str) else groupby
    result = df.groupby(cols, dropna=False).size().reset_index(name="count")
    if sort:
        result = result.sort_values("count", ascending=False)
    return result.reset_index(drop=True)


def verb_stems_by_book(testament: str | None = None,
                       book: str | None = None) -> pd.DataFrame:
    """Count Hebrew verb stems, optionally filtered by testament or book."""
    kwargs: dict = {"part_of_speech": "Verb", "source": "TAHOT"}
    if testament:
        kwargs["testament"] = testament
    if book:
        kwargs["book"] = book
    df = _query(**kwargs)
    return freq_table(df, ["book_id", "stem"])


def pos_distribution(source: str = "TAHOT",
                     book: str | None = None) -> pd.DataFrame:
    """Part-of-speech distribution for a source (TAHOT or TAGNT)."""
    kwargs: dict = {"source": source}
    if book:
        kwargs["book"] = book
    df = _query(**kwargs)
    return freq_table(df, "part_of_speech")


def greek_verb_forms(book_group: str | None = None,
                     book: str | None = None) -> pd.DataFrame:
    """Tense × voice × mood counts for Greek verbs."""
    kwargs: dict = {"source": "TAGNT", "part_of_speech": "Verb"}
    if book_group:
        kwargs["book_group"] = book_group
    if book:
        kwargs["book"] = book
    df = _query(**kwargs)
    return freq_table(df, ["tense", "voice", "mood"])


def niphal_perfects_by_book() -> pd.DataFrame:
    """Count of niphal perfect verbs in each OT book."""
    df = _query(source="TAHOT", stem="Niphal", conjugation="Perfect")
    return freq_table(df, "book_id")
