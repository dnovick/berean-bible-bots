"""Behavioral tests for bible_grammar.nt.nt_participles, requiring real
corpus data — data/processed/macula_syntax.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.nt.nt_participles import nt_participle_data, nt_participle_top_lemmas

_SYNTAX_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _SYNTAX_PARQUET.exists():
        pytest.skip(f"Data file not found: {_SYNTAX_PARQUET}")


class TestParticiples:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(nt_participle_data()) >= 6400   # observed: 6,653

    def test_lego_is_top_lemma(self) -> None:
        # λέγω ("saying") is the NT's most frequent participle lemma —
        # the standard way of introducing direct speech. Observed: count
        # 494, present tense.
        _skip_if_missing()
        df = nt_participle_top_lemmas(5)
        top = df.iloc[0]
        assert top['lemma'] == 'λέγω'
        assert top['top_tense'] == 'present'
        assert top['count'] >= 450
