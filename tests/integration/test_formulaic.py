"""Behavioral tests for bible_grammar.discourse.formulaic, requiring real
corpus data — data/processed/macula_syntax_ot.parquet and
macula_syntax.parquet. Per docs/policies/test-coverage.md's priority plan
(issue #676, Phase 4).

Regression guard: 7 of the 10 HEBREW_FORMULAS entries used to match zero
verses, ever, because their patterns used lemma spellings that don't match
this corpus (a pointed Tetragrammaton where the corpus stores it unpointed;
a participle surface form where the corpus's lemma column always uses the
Qal-perfect citation form for verbs). Fixed directly against real corpus
evidence — these tests confirm every formula still matches real verses.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.discourse.formulaic import ot_formula_profile, nt_formula_profile

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
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestOtFormulaProfile:
    def test_every_hebrew_formula_matches_at_least_one_verse(self) -> None:
        # Regression guard: previously 7 of 10 entries had count == 0 for
        # every book, due to lemma-form mismatches against the real corpus.
        _skip_if_ot_missing()
        df = ot_formula_profile()
        assert len(df) == 10
        assert (df['count'] > 0).all()

    def test_ko_amar_yhwh_is_the_most_frequent_prophetic_formula(self) -> None:
        # Observed: "Thus says YHWH" (כֹּה אָמַר יהוה) is the single most
        # frequent formula in the corpus, with 293 occurrences.
        _skip_if_ot_missing()
        df = ot_formula_profile()
        top = df.iloc[0]
        assert top['key'] == 'ko_amar_yhwh'
        assert top['count'] >= 250

    def test_arur_and_barukh_yhwh_use_the_qal_perfect_citation_form(self) -> None:
        # Regression guard for the two participle-vs-citation-form fixes:
        # 'arur' (cursed) and 'barukh_yhwh' (blessed be YHWH) both use verbs
        # whose surface form in the text is a passive participle, but this
        # corpus's lemma column always cites verbs in the Qal perfect 3ms.
        # Observed: arur count 63, barukh_yhwh count 42.
        _skip_if_ot_missing()
        df = ot_formula_profile().set_index('key')
        assert df.loc['arur', 'count'] >= 40
        assert df.loc['barukh_yhwh', 'count'] >= 30


class TestNtFormulaProfile:
    def test_gegraptai_is_the_most_frequent_greek_formula(self) -> None:
        # Observed: "It is written" (γέγραπται, citation formula) is the
        # most frequent Greek formula, with 192 occurrences.
        _skip_if_nt_missing()
        df = nt_formula_profile()
        top = df.iloc[0]
        assert top['key'] == 'gegraptai'
        assert top['count'] >= 150
