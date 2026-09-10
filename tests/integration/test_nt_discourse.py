"""Behavioral tests for bible_grammar.nt.nt_discourse, requiring real corpus
data — data/processed/macula_syntax.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).

Found and fixed a real bug while gathering ground truth for this file:
PARTICLE_REGISTRY keyed ἀλλά ("but") as '0235' (zero-padded), but the raw
`strong` column in the MACULA data stores it unpadded as '235' — every
other registry entry happens to be a 4-digit number that doesn't need
padding, so only this one particle was silently reported as 0 occurrences.
Fixed by dropping the leading zero to match the raw data format (see
nt_discourse.py's PARTICLE_REGISTRY).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.nt.nt_discourse import nt_particle_frequency, nt_kai_profile

_SYNTAX_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _SYNTAX_PARQUET.exists():
        pytest.skip(f"Data file not found: {_SYNTAX_PARQUET}")


class TestParticleFrequency:
    def test_kai_dominates(self) -> None:
        # καί ("and") is the NT's most common particle by a wide margin.
        # Observed: count 8978, 47.0%.
        _skip_if_missing()
        df = nt_particle_frequency()
        top = df.sort_values('count', ascending=False).iloc[0]
        assert top['lemma'] == 'καί'
        assert top['count'] >= 8500

    def test_alla_is_not_zero(self) -> None:
        # Regression guard for the PARTICLE_REGISTRY '0235' vs '235' bug
        # described in this file's module docstring. Observed: count 638.
        _skip_if_missing()
        df = nt_particle_frequency()
        alla = df[df['lemma'] == 'ἀλλά'].iloc[0]
        assert alla['count'] >= 600


class TestKaiProfile:
    def test_additive_is_the_dominant_function(self) -> None:
        # Observed: additive (plain coordination) 8060 tokens, 89.8% —
        # by far καί's most common discourse function.
        _skip_if_missing()
        df = nt_kai_profile()
        top = df.sort_values('count', ascending=False).iloc[0]
        assert top['function'] == 'additive'
        assert top['pct'] >= 85.0
