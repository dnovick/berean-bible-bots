"""Behavioral tests for bible_grammar.lexical.synonym (/synonym), requiring
real corpus data — data/processed/.
"""

import sys
import unicodedata
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.lexical.synonym import compare_synonyms, synonym_table

_WORDS_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "words.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORDS_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORDS_PARQUET}")


class TestSynonymTable:
    def test_shalom_and_chesed_frequencies(self) -> None:
        # שָׁלוֹם (peace, H7965) vs חֶסֶד (kindness, H2617): both take a
        # single, non-overlapping LXX equivalent at 100% consistency.
        # Observed: shalom 237 occurrences / eirene 100%; chesed 247 / eleos 100%.
        _skip_if_missing()
        df = synonym_table(['H7965', 'H2617'])
        shalom = df[df['strongs'] == 'H7965'].iloc[0]
        chesed = df[df['strongs'] == 'H2617'].iloc[0]
        assert shalom['total_occurrences'] == 237
        # NFC-normalize — the corpus stores this lemma in a polytonic (non-NFC) form.
        assert unicodedata.normalize('NFC', shalom['lxx_primary']) == unicodedata.normalize('NFC', 'εἰρήνη')
        assert chesed['total_occurrences'] == 247
        assert chesed['lxx_primary'] == 'ἔλεος'


class TestCompareSynonyms:
    def test_ahav_dominates_chashaq_in_frequency(self) -> None:
        # אָהֵב (love, H0157) vs חָשַׁק (desire/cling to, H2836): אהב is the
        # common general-purpose verb, חשק a rare intensive synonym.
        # Observed: 211 occurrences vs 11.
        _skip_if_missing()
        profiles = compare_synonyms(['H0157', 'H2836'])
        by_strongs = {p['strongs']: p for p in profiles}
        assert by_strongs['H0157']['total'] == 211
        assert by_strongs['H2836']['total'] == 11

    def test_ahav_top_book_is_genesis(self) -> None:
        _skip_if_missing()
        profiles = compare_synonyms(['H0157', 'H2836'])
        ahav = next(p for p in profiles if p['strongs'] == 'H0157')
        top = ahav['by_book'].iloc[0]
        assert top['book_id'] == 'Gen'
        assert top['count'] == 14
