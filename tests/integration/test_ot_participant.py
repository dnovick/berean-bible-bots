"""Behavioral tests for bible_grammar.ot.ot_participant, requiring real
corpus data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot.ot_participant import ot_participant_data, ot_participant_subject_verbs

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestParticipantData:
    def test_moses_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(ot_participant_data('Moses')) >= 700   # observed: 766


class TestParticipantSubjectVerbs:
    def test_moses_most_common_subject_verb_is_said(self) -> None:
        # Moses's most common subject-verb pairing is אָמַר ("said") —
        # consistent with his role as the one who relays God's words to
        # Israel throughout the Torah. Observed: count 182.
        _skip_if_missing()
        df = ot_participant_subject_verbs('Moses', top_n=5)
        top = df.iloc[0]
        assert top['verb_lemma'] == 'אָמַר'
        assert top['count'] >= 150
