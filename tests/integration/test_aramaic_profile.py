"""Behavioral tests for bible_grammar.ot.aramaic_profile, requiring real
corpus data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot.aramaic_profile import aramaic_data, aramaic_verb_data, aramaic_stem_profile

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestAramaicData:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(aramaic_data()) >= 7400   # observed: 7,549

    def test_verb_token_count(self) -> None:
        _skip_if_missing()
        assert len(aramaic_verb_data()) >= 1000   # observed: 1,069


class TestAramaicStemProfile:
    def test_peal_dominates(self) -> None:
        # Peal (the Aramaic base stem, analogous to Hebrew Qal) is by far
        # the most common Aramaic verb stem. Observed: 633 tokens, 59.2%.
        _skip_if_missing()
        df = aramaic_stem_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['form'] == 'peal'
        assert top['pct'] >= 50.0
