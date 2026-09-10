"""Behavioral tests for bible_grammar.core.lxx_query (/lxx-query), requiring
real corpus data — data/processed/lxx.parquet.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.core.lxx_query import lxx_by_book, lxx_verb_stats

_LXX_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "lxx.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _LXX_PARQUET.exists():
        pytest.skip(f"Data file not found: {_LXX_PARQUET}")


class TestLxxByBook:
    def test_eirene_total_and_top_book(self) -> None:
        # εἰρήνη (peace, G1515) in the LXX: observed 223 total occurrences
        # across all books, with Isaiah the single most frequent book (29).
        _skip_if_missing()
        df = lxx_by_book(strongs='G1515')
        assert df['count'].sum() == 223
        top = df.sort_values('count', ascending=False).iloc[0]
        assert top['book_id'] == 'Isa'
        assert top['count'] >= 25


class TestLxxVerbStats:
    def test_lego_is_dominated_by_present_active_participle(self) -> None:
        # λέγω (to say, G3004) is the LXX's most common speech verb —
        # overwhelmingly Present Active Participle ("saying"), the
        # standard LXX formula introducing direct speech.
        _skip_if_missing()
        df = lxx_verb_stats(strongs='G3004')
        top = df.iloc[0]
        assert top['tense'] == 'Present'
        assert top['voice'] == 'Active'
        assert top['mood'] == 'Participle'
        assert top['count'] >= 900
