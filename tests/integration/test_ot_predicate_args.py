"""Behavioral tests for bible_grammar.ot.ot_predicate_args, requiring real
corpus data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot.ot_predicate_args import ot_frame_data, ot_agent_verbs

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestFrameData:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(ot_frame_data()) >= 65000   # observed: 68,207


class TestAgentVerbs:
    def test_elohim_most_common_agent_verb_is_said(self) -> None:
        # "God said" (Genesis 1's creation refrain, and many other verses)
        # makes אָמַר Elohim's most common agent-role verb.
        # Observed: count 60.
        _skip_if_missing()
        df = ot_agent_verbs('אֱלֹהִים', top_n=5)
        top = df.iloc[0]
        assert top['lemma'] == 'אָמַר'
        assert top['count'] >= 50
