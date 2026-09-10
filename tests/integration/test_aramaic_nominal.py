"""Behavioral tests for bible_grammar.ot.aramaic_nominal, requiring real
corpus data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot.aramaic_nominal import aramaic_noun_data, aramaic_noun_state_profile

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestAramaicNounData:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(aramaic_noun_data()) >= 2200   # observed: 2,306


class TestAramaicNounStateProfile:
    def test_determined_state_leads(self) -> None:
        # Unlike Hebrew, Aramaic marks definiteness with a distinct
        # "determined" state (the emphatic ending) rather than a prefixed
        # article — and it's the most common noun state in the corpus.
        # Observed: 803 tokens, 41.8%.
        _skip_if_missing()
        df = aramaic_noun_state_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['form'] == 'determined'
        assert top['pct'] >= 35.0
