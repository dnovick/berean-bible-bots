"""Behavioral tests for bible_grammar.nt.nt_moods, requiring real corpus
data — data/processed/macula_syntax.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.nt.nt_moods import nt_mood_profile, nt_subjunctive_profile

_SYNTAX_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _SYNTAX_PARQUET.exists():
        pytest.skip(f"Data file not found: {_SYNTAX_PARQUET}")


class TestMoodProfile:
    def test_indicative_dominates(self) -> None:
        # The indicative (statement of fact) is the NT's overwhelmingly
        # dominant mood/form — narrative and epistolary prose alike.
        # Observed: 15,617 tokens, 55.1%.
        _skip_if_missing()
        df = nt_mood_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['form'] == 'indicative'
        assert top['pct'] >= 50.0


class TestSubjunctiveProfile:
    def test_aorist_active_is_top_cell(self) -> None:
        # Observed: aorist/active count 948, the largest single cell in
        # the tense x voice crosstab.
        _skip_if_missing()
        df = nt_subjunctive_profile()
        assert df.loc['aorist', 'active'] >= 900
        assert df.loc['aorist', 'active'] == df.values.max()
