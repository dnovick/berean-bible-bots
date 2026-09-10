"""Behavioral tests for bible_grammar.ot.ot_numbers, requiring real corpus
data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot.ot_numbers import ot_number_data, ot_top_number_lemmas

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestNumberData:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(ot_number_data()) >= 6600   # observed: 6,801

    def test_echad_is_top_number(self) -> None:
        # אֶחָד ("one") is the OT's most frequently used number word.
        # Observed: count 862, Strong's H259.
        _skip_if_missing()
        df = ot_top_number_lemmas(5)
        top = df.iloc[0]
        assert top['lemma'] == 'אֶחָד'
        assert top['strong_h'] == 'H259'
        assert top['count'] >= 800
