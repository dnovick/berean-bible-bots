"""Behavioral tests for bible_grammar.verbal_syntax.infinitives, requiring
real corpus data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.verbal_syntax.infinitives import infinitive_usage

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestInfinitiveUsage:
    def test_genesis_totals(self) -> None:
        # Observed: 435 infinitive construct tokens, 55 infinitive absolute.
        _skip_if_missing()
        r = infinitive_usage('Gen')
        assert r['inf_cst_total'] >= 400
        assert r['inf_abs_total'] >= 45

    def test_lamed_is_the_dominant_governing_preposition(self) -> None:
        # לְ + infinitive construct is the standard Hebrew purpose/result
        # construction ("in order to...") — by far the most common
        # preposition governing an infinitive construct. Observed: 286 of
        # 435 (~66%).
        _skip_if_missing()
        r = infinitive_usage('Gen')
        by_prep = r['inf_cst_by_prep']
        assert max(by_prep, key=by_prep.get) == 'ל'
        assert by_prep['ל'] >= 250
