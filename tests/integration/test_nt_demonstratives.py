"""Behavioral tests for bible_grammar.nt.nt_demonstratives, requiring real
corpus data — data/processed/macula_syntax.parquet (MACULA Greek NT).
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.nt.nt_demonstratives import nt_demo_data, nt_demo_frequency

_SYNTAX_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _SYNTAX_PARQUET.exists():
        pytest.skip(f"Data file not found: {_SYNTAX_PARQUET}")


class TestDemonstratives:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(nt_demo_data()) >= 1650   # observed: 1,709

    def test_houtos_dominates(self) -> None:
        # οὗτος ("this") is overwhelmingly the most common NT demonstrative.
        # Observed: count 1388, 81.2% of all demonstrative tokens.
        _skip_if_missing()
        df = nt_demo_frequency()
        top = df.iloc[0]
        assert top['lemma'] == 'οὗτος'
        assert top['pct'] >= 75.0
