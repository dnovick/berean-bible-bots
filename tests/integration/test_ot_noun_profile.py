"""Behavioral tests for bible_grammar.ot.ot_noun_profile, requiring real
corpus data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot.ot_noun_profile import ot_noun_data, ot_noun_top_lemmas, ot_noun_state_profile

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestNounData:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(ot_noun_data()) >= 140000   # observed: 143,975

    def test_yhwh_is_top_lemma(self) -> None:
        # יהוה is the OT's single most frequent noun-tagged lemma.
        # Observed: count 6,521 — consistent (same order of magnitude) with
        # divine_names.py's independent YHWH count of 6,513
        # (tests/integration/test_divine_names.py).
        _skip_if_missing()
        df = ot_noun_top_lemmas(5)
        top = df.iloc[0]
        assert top['lemma'] == 'יהוה'
        assert top['count'] >= 6000


class TestNounStateProfile:
    def test_hebrew_has_no_determined_state(self) -> None:
        # Unlike Aramaic (see test_aramaic_nominal.py), Hebrew marks
        # definiteness with a prefixed article, not a distinct
        # "determined" noun state — the state profile should show 0%
        # determined.
        _skip_if_missing()
        df = ot_noun_state_profile()
        determined = df[df['form'] == 'determined'].iloc[0]
        assert determined['count'] == 0
