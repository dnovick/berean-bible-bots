"""Behavioral tests for bible_grammar.ot.prepositions, requiring real corpus
data — data/processed/words.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot.prepositions import prep_frequency

_WORDS_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "words.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORDS_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORDS_PARQUET}")


class TestPrepFrequency:
    def test_le_is_the_most_common_ot_preposition(self) -> None:
        # לְ ("to/for") is the OT's most frequent preposition. Observed:
        # count 20,430, 31.8%.
        _skip_if_missing()
        df = prep_frequency(top_n=5)
        top = df.iloc[0]
        assert top['lemma'] == 'לְ'
        assert top['pct'] >= 25.0
