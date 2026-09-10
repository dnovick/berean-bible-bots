"""Behavioral tests for bible_grammar.nt.nt_verb_profile, requiring real
corpus data — data/processed/macula_syntax.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.nt.nt_verb_profile import nt_verb_data, nt_verb_top_lemmas, nt_verb_tense_profile

_SYNTAX_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _SYNTAX_PARQUET.exists():
        pytest.skip(f"Data file not found: {_SYNTAX_PARQUET}")


class TestVerbProfile:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(nt_verb_data()) >= 27000   # observed: 28,357

    def test_eimi_is_top_lemma(self) -> None:
        # εἰμί ("to be") is the NT's single most frequent verb. Observed:
        # count 2457.
        _skip_if_missing()
        df = nt_verb_top_lemmas(5)
        top = df.iloc[0]
        assert top['lemma'] == 'εἰμί'
        assert top['count'] >= 2300

    def test_aorist_and_present_dominate_tense_profile(self) -> None:
        # Aorist (simple past narrative) and present are the NT's two
        # dominant tenses, together well over 3/4 of all verb tokens.
        # Observed: aorist 41.6%, present 40.8%.
        _skip_if_missing()
        df = nt_verb_tense_profile()
        top2_pct = df.sort_values('pct', ascending=False).head(2)['pct'].sum()
        assert top2_pct >= 75.0
