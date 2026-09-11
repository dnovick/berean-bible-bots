"""Behavioral tests for bible_grammar.nt.greek_prepositions, requiring real
corpus data — data/processed/words.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4;
broadened under issue #676 Phase 3).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.nt.greek_prepositions import (
    greek_prep_frequency,
    greek_prep_by_book,
    greek_prep_distribution_table,
    greek_prep_cases,
    greek_prep_collocates,
    compare_greek_preps,
    nt_lxx_compare,
    print_greek_prep_frequency,
    print_greek_prep_by_book,
    print_greek_prep_distribution,
    print_greek_prep_cases,
    print_greek_prep_collocates,
    print_compare_greek_preps,
    print_nt_lxx_compare,
)

_WORDS_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "words.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORDS_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORDS_PARQUET}")


class TestGreekPrepFrequency:
    def test_en_is_the_most_common_nt_preposition(self) -> None:
        # ἐν ("in/among") is the NT's most frequent preposition. Observed:
        # count 2743, 25.1%.
        _skip_if_missing()
        df = greek_prep_frequency('nt', top_n=5)
        top = df.iloc[0]
        assert top['lemma'] == 'ἐν'
        assert top['pct'] >= 20.0

    def test_en_by_book_leads_in_luke(self) -> None:
        # Observed: Luk 359 (13.1% of all ἐν occurrences), the most of any book.
        _skip_if_missing()
        df = greek_prep_by_book('ἐν')
        top = df.sort_values('count', ascending=False).iloc[0]
        assert top['book'] == 'Luk'
        assert top['count'] >= 300

    def test_distribution_table_en_leads_totals(self) -> None:
        # Observed: Total row — ἐν 2743, εἰς 1766, ἐκ 913.
        _skip_if_missing()
        df = greek_prep_distribution_table()
        totals = df.loc['Total']
        assert totals.idxmax() == 'ἐν'
        assert totals.max() >= 2500

    def test_en_governs_the_dative_overwhelmingly(self) -> None:
        # Observed: Dative 2704 (98.6%) — ἐν ("in/among/by") is a
        # textbook dative-governing preposition.
        _skip_if_missing()
        df = greek_prep_cases('ἐν')
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['case_binding'] == 'Dative'
        assert top['pct'] >= 90.0

    def test_definite_article_is_the_top_en_collocate(self) -> None:
        # Observed: ὁ (definite article) collocates with ἐν 1,050 times —
        # far more than any other word, as expected for a preposition
        # governing an articular dative object.
        _skip_if_missing()
        df = greek_prep_collocates('ἐν', top_n=5)
        top = df.iloc[0]
        assert top['collocate'] == 'ὁ'
        assert top['count'] >= 900

    def test_compare_en_and_eis_shares_definite_article_as_top(self) -> None:
        # Observed: ὁ collocates with ἐν 1,050 times and εἰς 845 times —
        # both prepositions' most common object is an articular noun.
        _skip_if_missing()
        df = compare_greek_preps('ἐν', 'εἰς', top_n=5)
        top = df.iloc[0]
        assert top['collocate'] == 'ὁ'
        assert top['count_ἐν'] >= 900
        assert top['count_εἰς'] >= 700

    def test_en_governs_dative_more_consistently_in_nt_than_lxx(self) -> None:
        # Observed: ἐν governs Dative 98.6% of the time in the NT vs. 95.8%
        # in the LXX — a real but modest difference given ἐν's already
        # near-universal dative-government in both corpora.
        _skip_if_missing()
        df = nt_lxx_compare('ἐν')
        top = df.sort_values('pct_nt', ascending=False).iloc[0]
        assert top['case_binding'] == 'Dative'
        assert top['pct_nt'] >= top['pct_lxx']


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            print_greek_prep_frequency,
            lambda: print_greek_prep_by_book('ἐν'),
            print_greek_prep_distribution,
            lambda: print_greek_prep_cases('ἐν'),
            lambda: print_greek_prep_collocates('ἐν'),
            lambda: print_compare_greek_preps('ἐν', 'εἰς'),
            lambda: print_nt_lxx_compare('ἐν'),
        )
        for fn in fns:
            capsys.readouterr()
            fn()
            out = capsys.readouterr().out
            assert len(out.strip()) > 50, f"{fn} produced no real output"
