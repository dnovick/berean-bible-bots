"""Behavioral tests for bible_grammar.lexical.collocation (/collocations),
requiring real corpus data — data/processed/.

These tests guard against a real regression found while writing them: every
TAHOT (Hebrew OT) strongs cell in this corpus carries a STEPBible homonym
disambiguation letter (e.g. '{H7965G}'), but collocations() was comparing
the letter-preserving root against a plain, letter-stripped user target —
so it silently returned an empty DataFrame for every single Hebrew OT query,
with no error. Fixed by stripping the trailing letter on both sides before
comparing (see _strip_variant in collocation.py).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.lexical.collocation import collocations

_WORDS_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "words.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORDS_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORDS_PARQUET}")


class TestCollocationsHebrewOT:
    def test_shalom_top_collocate_is_amar(self) -> None:
        # שָׁלוֹם (peace, H7965): its single strongest collocate is אָמַר
        # (to say) — the idiom "ask/say [about] the peace of" (שָׁאַל
        # לְשָׁלוֹם, דִּבֶּר שָׁלוֹם) accounts for this. Observed:
        # co_count 116, log_likelihood ~125.
        _skip_if_missing()
        df = collocations('H7965', corpus='OT', top_n=10)
        assert not df.empty
        top = df.iloc[0]
        assert top['strongs'] == 'H559'
        assert top['co_count'] >= 100

    def test_common_ot_targets_are_never_empty(self) -> None:
        # Regression guard: these all returned an empty DataFrame under the
        # bug described in this file's module docstring.
        _skip_if_missing()
        for strongs in ('H7965', 'H3068', 'H0430', 'H1254'):
            df = collocations(strongs, corpus='OT', top_n=5)
            assert not df.empty, f"{strongs} unexpectedly returned no collocates"


class TestCollocationsGreekNT:
    def test_theos_top_collocate_columns(self) -> None:
        _skip_if_missing()
        df = collocations('G2316', corpus='NT', top_n=10)
        assert not df.empty
        for col in ('strongs', 'lemma', 'gloss', 'co_count', 'pmi', 'log_likelihood'):
            assert col in df.columns
