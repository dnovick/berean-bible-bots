"""Behavioral tests for bible_grammar.nt.greek_prepositions, requiring real
corpus data — data/processed/words.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.nt.greek_prepositions import greek_prep_frequency

_WORDS_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "words.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORDS_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORDS_PARQUET}")


class TestGreekPrepFrequency:
    def test_en_is_the_most_common_nt_preposition(self) -> None:
        # ἐν ("in/among") is the NT's most frequent preposition. Observed:
        # count 2743, 25.1%.
        _skip_if_missing()
        df = greek_prep_frequency('nt', top_n=5)
        top = df.iloc[0]
        assert top['lemma'] == 'ἐν'
        assert top['pct'] >= 20.0
