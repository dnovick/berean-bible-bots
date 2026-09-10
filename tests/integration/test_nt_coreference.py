"""Behavioral tests for bible_grammar.nt.nt_coreference, requiring real
corpus data — data/processed/macula_syntax.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.nt.nt_coreference import nt_referent_data, nt_referent_frequency

_SYNTAX_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _SYNTAX_PARQUET.exists():
        pytest.skip(f"Data file not found: {_SYNTAX_PARQUET}")


class TestReferentData:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(nt_referent_data()) >= 14000   # observed: 14,471


class TestReferentFrequency:
    def test_paulos_is_top_referent(self) -> None:
        # Παῦλος (Paul) leads NT referent chains — unsurprising given how
        # much of the NT is Pauline epistle, with Paul as author and
        # frequent self-referent. Observed: top chain has ref_count 151,
        # anchored at Rom 1:1 (Paul's self-introduction).
        _skip_if_missing()
        df = nt_referent_frequency(top_n=5)
        top = df.iloc[0]
        assert top['antecedent_lemma'] == 'Παῦλος'
        assert top['ref_count'] >= 140
