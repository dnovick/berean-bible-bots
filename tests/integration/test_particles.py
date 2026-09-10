"""Behavioral tests for bible_grammar.verbal_syntax.particles, requiring
real corpus data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.verbal_syntax.particles import discourse_particles

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestDiscourseParticles:
    def test_genesis_total(self) -> None:
        _skip_if_missing()
        assert len(discourse_particles('Gen')) >= 4500   # observed: 4,714

    def test_vav_dominates(self) -> None:
        # וְ ("and") is by far Hebrew's most common discourse particle —
        # the connective backbone of Hebrew narrative prose.
        # Observed: 4,134 of 4,714 tokens (~88%).
        _skip_if_missing()
        df = discourse_particles('Gen')
        top = df['particle_label'].value_counts()
        assert top.index[0] == 'וְ'
        assert top.iloc[0] >= 4000
