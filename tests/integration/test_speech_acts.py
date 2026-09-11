"""Behavioral tests for bible_grammar.discourse.speech_acts, requiring
real corpus data — data/processed/macula_syntax_ot.parquet and
macula_syntax.parquet. Per docs/policies/test-coverage.md's priority plan
(issue #676, Phase 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.discourse.speech_acts import ot_speech_act_profile, nt_speech_act_profile

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


class TestOtSpeechActProfile:
    def test_genesis_is_dominated_by_unclassified_and_directive(self) -> None:
        # Observed: 1,533 verses total. unclassified 45.0% (690), directive
        # 26.7% (409) — Genesis narrative is mostly non-speech description
        # plus commands (e.g. "let there be...", divine/patriarchal orders).
        _skip_if_ot_missing()
        df = ot_speech_act_profile(book='Gen')
        by_type = df.set_index('speech_act_type')
        assert df['count'].sum() == 1533
        assert by_type.loc['unclassified', 'pct'] >= 40.0
        assert by_type.loc['directive', 'pct'] >= 20.0


class TestNtSpeechActProfile:
    def test_matthew_directive_and_assertive_are_prominent(self) -> None:
        # Observed: 1,068 verses total. unclassified 33.1% (354), directive
        # 33.0% (352), assertive 23.2% (248) — Matthew's teaching discourse
        # (commands, declarations) contrasts with Genesis's narrative mix.
        _skip_if_nt_missing()
        df = nt_speech_act_profile(book='Mat')
        by_type = df.set_index('speech_act_type')
        assert df['count'].sum() == 1068
        assert by_type.loc['directive', 'pct'] >= 25.0
        assert by_type.loc['assertive', 'pct'] >= 15.0
