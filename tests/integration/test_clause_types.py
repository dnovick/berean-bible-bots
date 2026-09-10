"""Behavioral tests for bible_grammar.verbal_syntax.clause_types, requiring
real corpus data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.verbal_syntax.clause_types import clause_type_profile

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestClauseTypeProfile:
    def test_genesis_is_overwhelmingly_verbal(self) -> None:
        # Hebrew narrative is verb-clause-dominated — nominal clauses are
        # the exception. Observed: Genesis has 1,533 verses, 1,453 verbal
        # clauses (94.8%) vs. only 25 nominal clauses (1.6%).
        _skip_if_missing()
        df = clause_type_profile('Gen')
        by_feature = df.set_index('feature')
        assert by_feature.loc['total verses', 'count'] >= 1500
        assert by_feature.loc['verbal clauses', 'per_100_verses'] >= 90.0
        assert by_feature.loc['nominal clauses', 'per_100_verses'] <= 5.0
