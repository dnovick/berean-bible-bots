"""Behavioral tests for bible_grammar.nt.nt_noun_profile, requiring real
corpus data — data/processed/macula_syntax.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.nt.nt_noun_profile import nt_noun_data, nt_noun_top_lemmas

_SYNTAX_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _SYNTAX_PARQUET.exists():
        pytest.skip(f"Data file not found: {_SYNTAX_PARQUET}")


class TestNounProfile:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(nt_noun_data()) >= 27000   # observed: 28,455

    def test_theos_is_top_lemma(self) -> None:
        # θεός (God) is the NT's most frequent noun lemma. Observed: count 1311.
        _skip_if_missing()
        df = nt_noun_top_lemmas(30)
        top = df.iloc[0]
        assert top['lemma'] == 'θεός'
        assert top['count'] >= 1200

    def test_top_lemmas_does_not_crash_on_null_gloss_lemmas(self) -> None:
        # Regression guard: nt_noun_top_lemmas() used to crash with
        # IndexError for any lemma whose every token has a null gloss (e.g.
        # δύσις/G1424, a single-occurrence word) — value_counts() drops NaN,
        # so a group that's entirely null has an EMPTY value_counts() even
        # though the group itself is non-empty; the old `if len(x) else ''`
        # guard checked the wrong thing. Run across the full top-30 (which
        # includes low-frequency lemmas) rather than just the top handful.
        # n=3000 comfortably covers all ~2,399 unique noun lemma groups,
        # including δύσις itself.
        _skip_if_missing()
        df = nt_noun_top_lemmas(3000)
        assert not df.empty
        assert 'top_gloss' in df.columns
        assert (df['lemma'] == 'δύσις').any()
