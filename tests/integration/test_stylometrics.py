"""Behavioral tests for bible_grammar.discourse.stylometrics, requiring
real corpus data — data/processed/macula_syntax_ot.parquet and
macula_syntax.parquet. Per docs/policies/test-coverage.md's priority plan
(issue #676, Phase 4).

Regression guard: book_style_profile()'s noun_pct (both languages) and the
Greek branch's verbal_pct used to be hardcoded to 0.0 for every book,
because the code checked for a column named 'sp' that doesn't exist
anywhere in this corpus — the real equivalents are 'type_' (Hebrew) and
'class_' (Greek). Fixed directly against real corpus evidence.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.discourse.stylometrics import book_style_profile

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


class TestHebrewBookStyleProfile:
    def test_genesis_noun_pct_is_not_zero(self) -> None:
        # Regression guard: noun_pct used to be hardcoded to 0.0 for every
        # Hebrew book (the code checked a non-existent 'sp' column).
        # Observed: 28.19% of Genesis's 32,363 tokens are common/proper
        # nouns (this corpus's 'type_' column).
        _skip_if_ot_missing()
        profile = book_style_profile('Gen', lang='H')
        assert profile['total_tokens'] == 32363
        assert profile['noun_pct'] >= 20.0

    def test_genesis_verbal_pct_is_plausible(self) -> None:
        # Observed: 15.13% of Genesis's tokens are one of the finite/
        # nonfinite verbal 'type_' values (wayyiqtol, qatal, etc.).
        _skip_if_ot_missing()
        profile = book_style_profile('Gen', lang='H')
        assert profile['verbal_pct'] >= 10.0


class TestGreekBookStyleProfile:
    def test_matthew_verbal_pct_is_not_zero(self) -> None:
        # Regression guard: verbal_pct/noun_pct used to be hardcoded to
        # 0.0 for every Greek book (same non-existent 'sp' column check).
        # Observed: 22.26% of Matthew's 18,299 tokens have a non-null
        # 'mood' value (i.e. are a finite or nonfinite verb form).
        _skip_if_nt_missing()
        profile = book_style_profile('Mat', lang='G')
        assert profile['total_tokens'] == 18299
        assert profile['verbal_pct'] >= 15.0

    def test_matthew_noun_pct_is_not_zero(self) -> None:
        # Observed: 46.54% of Matthew's tokens fall in the noun/det/pron
        # 'class_' categories.
        _skip_if_nt_missing()
        profile = book_style_profile('Mat', lang='G')
        assert profile['noun_pct'] >= 30.0
