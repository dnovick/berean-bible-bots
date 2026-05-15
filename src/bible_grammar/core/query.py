"""Filtered query API over the word DataFrame."""

from __future__ import annotations
import pandas as pd
from . import db as _db


def _df() -> pd.DataFrame:
    return _db.load()


def reload() -> None:
    """Force reload from disk (useful after rebuilding the database)."""
    _db.invalidate_cache()


def _lxx_df() -> pd.DataFrame:
    return _db.load_lxx()


def lxx_query(
    *,
    book: str | list[str] | None = None,
    lxx_book: str | None = None,
    testament: str | None = None,
    chapter: int | None = None,
    verse: int | None = None,
    book_group: str | None = None,
    include_deuterocanon: bool = False,
    part_of_speech: str | None = None,
    tense: str | None = None,
    voice: str | None = None,
    mood: str | None = None,
    person: str | None = None,
    number: str | None = None,
    gender: str | None = None,
    case_: str | None = None,
) -> pd.DataFrame:
    """
    Query the LXX Septuagint word data (CenterBLC/LXX, Rahlfs 1935).

    Parameters
    ----------
    book                 : canonical book_id (e.g. 'Gen', 'Isa') or list
    lxx_book             : LXX-native book name (e.g. 'Exod', '1Mac')
    testament            : 'OT' (canonical) — NT not in LXX
    chapter / verse      : filter to specific chapter or verse
    book_group           : 'torah', 'prophets', 'writings', 'gospels', 'pauline'
    include_deuterocanon : include deuterocanonical books (default False)
    part_of_speech       : 'Verb', 'Noun', 'Adjective', etc.
    tense                : 'Aorist', 'Present', 'Perfect', etc.
    voice                : 'Active', 'Middle', 'Passive'
    mood                 : 'Indicative', 'Participle', 'Infinitive', etc.
    person               : '1st', '2nd', '3rd'
    number               : 'Singular', 'Plural'
    gender               : 'Masculine', 'Feminine', 'Neuter'
    case_                : 'Nominative', 'Genitive', 'Dative', 'Accusative', 'Vocative'

    Examples
    --------
    # Aorist passives in Isaiah LXX
    lxx_query(book='Isa', tense='Aorist', voice='Passive')

    # All verbs in LXX Genesis
    lxx_query(book='Gen', part_of_speech='Verb')

    # Deuterocanonical books only
    lxx_query(include_deuterocanon=True, lxx_book='Sir')
    """
    from .reference import all_book_ids, book_ids_for_group

    df = _lxx_df()
    mask = pd.Series(True, index=df.index)

    if not include_deuterocanon:
        mask &= ~df["is_deuterocanon"]

    if lxx_book is not None:
        mask &= df["lxx_book"] == lxx_book
    if book is not None:
        vals = [book] if isinstance(book, str) else book
        mask &= df["book_id"].isin(vals)
    if testament is not None:
        ids = all_book_ids(testament.upper())
        mask &= df["book_id"].isin(ids)
    if book_group is not None:
        mask &= df["book_id"].isin(book_ids_for_group(book_group))
    if chapter is not None:
        mask &= df["chapter"] == chapter
    if verse is not None:
        mask &= df["verse"] == verse

    def _c(col: str, val: str) -> pd.Series:
        return df[col].str.lower().str.contains(val.lower(), na=False)

    if part_of_speech is not None:
        mask &= _c("part_of_speech", part_of_speech)
    if tense is not None:
        mask &= _c("tense", tense)
    if voice is not None:
        mask &= _c("voice", voice)
    if mood is not None:
        mask &= _c("mood", mood)
    if person is not None:
        mask &= _c("person", person)
    if number is not None:
        mask &= _c("number", number)
    if gender is not None:
        mask &= _c("gender", gender)
    if case_ is not None:
        mask &= _c("case_", case_)

    return df[mask].reset_index(drop=True)


def _tr_df() -> pd.DataFrame:
    return _db.load_translations()


def translation_query(
    *,
    translation: str | list[str] | None = None,
    book: str | list[str] | None = None,
    testament: str | None = None,
    chapter: int | None = None,
    verse: int | None = None,
    book_group: str | None = None,
    search: str | None = None,
) -> pd.DataFrame:
    """
    Query translation verses (KJV, VulgClementine).

    Parameters
    ----------
    translation : 'KJV' or 'VulgClementine' (or list of both)
    book        : book_id string or list, e.g. 'Gen' or ['Mat','Mrk']
    testament   : 'OT' or 'NT'
    chapter     : filter to a single chapter number
    verse       : filter to a single verse number
    book_group  : 'torah', 'prophets', 'writings', 'gospels', 'pauline'
    search      : case-insensitive substring search within verse text

    Examples
    --------
    translation_query(translation='KJV', book='Gen', chapter=1)
    translation_query(book_group='pauline', search='grace')
    translation_query(translation=['KJV','VulgClementine'], book='Jhn', chapter=3, verse=16)
    """
    from .reference import all_book_ids, book_ids_for_group

    df = _tr_df()
    mask = pd.Series(True, index=df.index)

    if translation is not None:
        vals = [translation] if isinstance(translation, str) else translation
        mask &= df["translation"].isin(vals)
    if testament is not None:
        ids = all_book_ids(testament.upper())
        mask &= df["book_id"].isin(ids)
    if book_group is not None:
        mask &= df["book_id"].isin(book_ids_for_group(book_group))
    if book is not None:
        vals = [book] if isinstance(book, str) else book
        mask &= df["book_id"].isin(vals)
    if chapter is not None:
        mask &= df["chapter"] == chapter
    if verse is not None:
        mask &= df["verse"] == verse
    if search is not None:
        mask &= df["text"].str.contains(search, case=False, na=False)

    return df[mask].reset_index(drop=True)


def query(
    *,
    source: str | None = None,
    book: str | list[str] | None = None,
    testament: str | None = None,
    chapter: int | None = None,
    verse: int | None = None,
    language: str | None = None,
    part_of_speech: str | None = None,
    stem: str | None = None,
    conjugation: str | None = None,
    tense: str | None = None,
    voice: str | None = None,
    mood: str | None = None,
    person: str | None = None,
    number: str | None = None,
    gender: str | None = None,
    case_: str | None = None,
    state: str | None = None,
    book_group: str | None = None,
) -> pd.DataFrame:
    """
    Return a filtered DataFrame of word rows.

    All filters are case-insensitive substring matches unless noted.
    book_group accepts: 'torah', 'prophets', 'writings', 'gospels', 'pauline'

    Examples
    --------
    # Niphal perfect verbs in Genesis
    query(book='Gen', stem='Niphal', conjugation='Perfect')

    # All verbs in the Torah
    query(book_group='torah', part_of_speech='Verb')

    # Greek aorist passive indicatives in Paul
    query(book_group='pauline', tense='Aorist', voice='Passive', mood='Indicative')
    """
    from .reference import all_book_ids, book_ids_for_group

    df = _df()
    mask = pd.Series(True, index=df.index)

    def _isin(col: str, val: str | list[str]) -> pd.Series:
        vals = [val] if isinstance(val, str) else val
        vals_lower = [v.lower() for v in vals]
        return df[col].str.lower().isin(vals_lower)

    def _contains(col: str, val: str) -> pd.Series:
        return df[col].str.lower().str.contains(val.lower(), na=False)

    if source is not None:
        mask &= _isin("source", source)
    if testament is not None:
        ids = all_book_ids(testament.upper())
        mask &= df["book_id"].isin(ids)
    if book_group is not None:
        mask &= df["book_id"].isin(book_ids_for_group(book_group))
    if book is not None:
        if isinstance(book, str):
            book = [book]
        mask &= df["book_id"].isin(book)
    if chapter is not None:
        mask &= df["chapter"] == chapter
    if verse is not None:
        mask &= df["verse"] == verse
    if language is not None:
        mask &= _contains("language", language)
    if part_of_speech is not None:
        mask &= _contains("part_of_speech", part_of_speech)
    if stem is not None:
        mask &= _contains("stem", stem)
    if conjugation is not None:
        mask &= _contains("conjugation", conjugation)
    if tense is not None:
        mask &= _contains("tense", tense)
    if voice is not None:
        mask &= _contains("voice", voice)
    if mood is not None:
        mask &= _contains("mood", mood)
    if person is not None:
        mask &= _contains("person", person)
    if number is not None:
        mask &= _contains("number", number)
    if gender is not None:
        mask &= _contains("gender", gender)
    if case_ is not None:
        mask &= _contains("case_", case_)
    if state is not None:
        mask &= _contains("state", state)

    return df[mask].reset_index(drop=True)
