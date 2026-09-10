"""Behavioral tests for bible_grammar.verbal_syntax.conditionals, requiring
real corpus data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.verbal_syntax.conditionals import conditional_clauses, conditional_summary

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestConditionalClauses:
    def test_genesis_total(self) -> None:
        _skip_if_missing()
        assert len(conditional_clauses('Gen')) >= 75   # observed: 82


class TestConditionalSummary:
    def test_open_future_is_the_most_common_type(self) -> None:
        # "Real — open future" (אִם + yiqtol, e.g. "if you do X, then Y
        # will happen") is the most common conditional pattern in Genesis.
        # Observed: count 37, 45.1%.
        _skip_if_missing()
        df = conditional_summary('Gen')
        top = df.sort_values('count', ascending=False).iloc[0]
        assert 'open future' in top['condition_type']
        assert top['pct'] >= 35.0
