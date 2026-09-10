"""Behavioral tests for bible_grammar.verbal_syntax.disjunctive, requiring
real corpus data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.verbal_syntax.disjunctive import disjunctive_clauses

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestDisjunctiveClauses:
    def test_genesis_total(self) -> None:
        _skip_if_missing()
        assert len(disjunctive_clauses('Gen')) >= 320   # observed: 344

    def test_circumstantial_background_is_the_top_function(self) -> None:
        # Disjunctive (subject-first) clauses most often mark
        # circumstantial background information in Genesis's narrative.
        # Observed: 159 of 344 clauses (~46%).
        _skip_if_missing()
        df = disjunctive_clauses('Gen')
        top = df['discourse_function'].value_counts().index[0]
        assert top == 'circumstantial / background'
