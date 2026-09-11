"""Behavioral tests for bible_grammar.discourse.information_structure,
requiring real corpus data — data/processed/macula_syntax_ot.parquet and
macula_syntax.parquet. Per docs/policies/test-coverage.md's priority plan
(issue #676, Phase 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.discourse.information_structure import (
    ot_information_profile,
    nt_information_profile,
)

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)
_MACULA_NT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_ot_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


def _skip_if_nt_missing() -> None:
    if not _MACULA_NT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_NT_PARQUET}")


class TestOtInformationProfile:
    def test_genesis_is_overwhelmingly_paratactic(self) -> None:
        # Hebrew narrative chains clauses with waw rather than
        # subordinating conjunctions. Observed: parataxis_ratio 0.8402,
        # nominal_clause_pct 5.41% out of 1,533 verses / 32,363 tokens.
        _skip_if_ot_missing()
        profile = ot_information_profile('Gen')
        assert profile['total_verses'] == 1533
        assert profile['parataxis_ratio'] >= 0.75
        assert profile['nominal_clause_pct'] <= 10.0

    def test_fronting_is_rare_in_genesis(self) -> None:
        # Observed: only 3 fronted elements out of 1,533 verses
        # (fronted_ratio 0.002) — Hebrew's default VSO order rarely needs
        # topicalization/fronting in narrative.
        _skip_if_ot_missing()
        profile = ot_information_profile('Gen')
        assert profile['fronted_ratio'] <= 0.05


class TestNtInformationProfile:
    def test_matthew_kai_dominates_connective_density(self) -> None:
        # Observed: kai_per1k 63.88, far above any other Greek connective
        # (de_per1k 27.0, gar_per1k 6.78) — καί is the default NT narrative
        # connective, much like waw in Hebrew.
        _skip_if_nt_missing()
        profile = nt_information_profile('Mat')
        assert profile['total_verses'] == 1068
        assert profile['kai_per1k'] >= 50.0
        assert profile['kai_per1k'] > profile['de_per1k']
