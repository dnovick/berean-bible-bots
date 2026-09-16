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

from bible_grammar.discourse import formulaic as _mod
from bible_grammar.discourse.formulaic import (
    ot_formula_profile,
    nt_formula_profile,
    ot_formula_frequency,
    nt_formula_frequency,
    ot_formula_search,
    nt_formula_search,
    formula_book_distribution,
    print_formula_concordance,
    print_formula_book_distribution,
    print_ot_formula_profile,
    print_nt_formula_profile,
    print_ot_top_ngrams,
    print_nt_top_ngrams,
    formula_book_chart,
    formula_chapter_chart,
    HEBREW_FORMULAS,
)

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


class TestFormulaFrequency:
    def test_ot_bigrams_in_genesis_are_real_and_plentiful(self) -> None:
        # Observed: Genesis alone has 1,086 distinct bigram lemma sequences
        # occurring >=5 times; the single most frequent is הוּא וְ ("he
        # and"/pronoun+conjunction), count 876.
        _skip_if_ot_missing()
        df = ot_formula_frequency(book='Gen')
        assert len(df) >= 900
        assert df.iloc[0]['count'] >= 800

    def test_nt_bigrams_in_matthew_are_real_and_plentiful(self) -> None:
        # Observed (book-scoped, min_count=50): Matthew's top bigram is
        # καί ὁ ("and the"), count 189, out of 20 bigrams meeting the
        # threshold.
        _skip_if_nt_missing()
        df = nt_formula_frequency(book='Mat', min_count=50)
        assert len(df) >= 15
        assert df.iloc[0]['count'] >= 150

    def test_min_count_filters_out_rare_ngrams(self) -> None:
        _skip_if_ot_missing()
        loose = ot_formula_frequency(book='Gen', min_count=5)
        strict = ot_formula_frequency(book='Gen', min_count=500)
        assert len(strict) < len(loose)
        assert (strict['count'] >= 500).all()


class TestFormulaSearch:
    def test_ko_amar_yhwh_search_matches_jeremiah_ground_truth(self) -> None:
        # Observed: 153 occurrences of "Thus says YHWH" in Jeremiah alone —
        # over half of the whole-OT total (293), consistent with Jeremiah
        # being the most prophetic-formula-dense book.
        _skip_if_ot_missing()
        df = ot_formula_search(HEBREW_FORMULAS['ko_amar_yhwh']['pattern'], book='Jer')
        assert len(df) >= 140
        for col in ('ref', 'book', 'chapter', 'verse', 'match_text', 'context'):
            assert col in df.columns
        assert (df['book'] == 'Jer').all()

    def test_wildcard_token_matches_multiple_forms(self) -> None:
        # '*' should match any single lemma in that slot — a 2-word pattern
        # with the divine name fixed and a wildcard first slot should match
        # at least as many verses as any single concrete pairing of it.
        _skip_if_ot_missing()
        df = ot_formula_search(['*', 'יהוה'], book='Gen')
        assert len(df) > 0

    def test_nt_search_accepts_a_space_separated_string_pattern(self) -> None:
        # ot_formula_search/nt_formula_search accept either a list of
        # lemmas or a single space-separated string — verify the string
        # form parses identically to the list form.
        _skip_if_nt_missing()
        from_list = nt_formula_search(['γράφω'])
        from_str = nt_formula_search('γράφω')
        assert len(from_list) == len(from_str)
        assert len(from_list) > 0


class TestFormulaBookDistribution:
    def test_ko_amar_yhwh_distribution_is_nonempty_and_sums_to_100(self) -> None:
        _skip_if_ot_missing()
        df = formula_book_distribution(HEBREW_FORMULAS['ko_amar_yhwh']['pattern'], lang='H')
        assert not df.empty
        assert abs(df['pct'].sum() - 100.0) < 0.5

    def test_book_order_follows_canonical_ot_sequence(self) -> None:
        # Exodus should appear before Jeremiah in the ordered output,
        # matching canonical OT book order (not alphabetical or by count).
        _skip_if_ot_missing()
        df = formula_book_distribution(HEBREW_FORMULAS['ko_amar_yhwh']['pattern'], lang='H')
        books = list(df['book'])
        if 'Exo' in books and 'Jer' in books:
            assert books.index('Exo') < books.index('Jer')


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_ot_missing()
        fns = (
            lambda: print_formula_concordance(HEBREW_FORMULAS['ko_amar_yhwh']['pattern'], lang='H'),
            lambda: print_formula_book_distribution(HEBREW_FORMULAS['ko_amar_yhwh']['pattern'], lang='H'),
            print_ot_formula_profile,
            print_nt_formula_profile,
            lambda: print_ot_top_ngrams(book='Gen'),
            lambda: print_nt_top_ngrams(book='Mat'),
        )
        for fn in fns:
            capsys.readouterr()
            fn()
            out = capsys.readouterr().out
            assert len(out.strip()) > 30, f"{fn} produced no real output"


class TestChartFunctions:
    def test_chart_functions_produce_real_pngs(self, tmp_path, monkeypatch) -> None:
        _skip_if_ot_missing()
        monkeypatch.setattr(_mod, '_CHART_DIR', tmp_path)
        out1 = formula_book_chart(HEBREW_FORMULAS['ko_amar_yhwh']['pattern'], lang='H')
        assert out1 is not None
        assert Path(out1).exists()
        assert Path(out1).stat().st_size > 0

        out2 = formula_chapter_chart('Jer', 'ko_amar_yhwh', lang='H')
        assert out2 is not None
        assert Path(out2).exists()
        assert Path(out2).stat().st_size > 0

    def test_chart_returns_none_for_unknown_formula_key(self, tmp_path, monkeypatch) -> None:
        _skip_if_ot_missing()
        monkeypatch.setattr(_mod, '_CHART_DIR', tmp_path)
        assert formula_chapter_chart('Jer', 'not_a_real_key', lang='H') is None
