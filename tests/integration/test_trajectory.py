"""Behavioral tests for bible_grammar.lexical.trajectory (/trajectory),
requiring real corpus data plus the word-level Hebrew<->LXX alignment
(data/processed/word_alignment.parquet, built via scripts/build_word_alignment.py).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.lexical.trajectory import word_trajectory

_WORD_ALIGNMENT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "word_alignment.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORD_ALIGNMENT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORD_ALIGNMENT_PARQUET}")


class TestWordTrajectory:
    def test_shalom_has_high_continuity_into_the_nt(self) -> None:
        # שָׁלוֹם (peace, H7965) -> εἰρήνη is the paradigm case of strong
        # OT-LXX-NT lexical continuity: same Greek word throughout, at
        # near-100% consistency, carried straight into NT usage.
        # Observed: ot_total 237, lxx_total 223, lxx_consistency 100.0,
        # nt_strongs G1515, nt_total 92, continuity 'high'.
        _skip_if_missing()
        t = word_trajectory('H7965')
        assert t['ot_total'] == 237
        assert t['lxx_primary_g'] == 'G1515'
        assert t['lxx_consistency'] >= 95.0
        assert t['nt_strongs'] == 'G1515'
        assert t['nt_total'] >= 80
        assert t['continuity'] == 'high'
