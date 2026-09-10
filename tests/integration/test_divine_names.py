"""Behavioral tests for bible_grammar.names.divine_names (/divine-names),
requiring real corpus data — data/processed/words.parquet.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.names.divine_names import divine_name_summary

_WORDS_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "words.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORDS_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORDS_PARQUET}")


class TestDivineNameSummaryOT:
    def test_yhwh_dominates_ot_divine_names(self) -> None:
        # The Tetragrammaton (YHWH) is by far the most frequent OT divine
        # name — observed 6,513 occurrences, ~66% of all divine-name
        # tokens, with Jeremiah the top book.
        _skip_if_missing()
        df = divine_name_summary('OT')
        top = df.iloc[0]
        assert top['label'] == 'YHWH'
        assert top['total'] >= 6000
        assert top['pct'] >= 60.0
        assert 'Jeremiah' in top['top_books']

    def test_elohim_is_second(self) -> None:
        # Observed: 2,602 occurrences, ~26%, Deuteronomy the top book.
        _skip_if_missing()
        df = divine_name_summary('OT')
        elohim = df[df['label'] == 'Elohim'].iloc[0]
        assert elohim['total'] >= 2400
        assert 'Deuteronomy' in elohim['top_books']
