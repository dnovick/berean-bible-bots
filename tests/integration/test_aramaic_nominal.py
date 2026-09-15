"""Behavioral tests for bible_grammar.ot.aramaic_nominal, requiring real
corpus data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot import aramaic_nominal as _mod
from bible_grammar.ot.aramaic_nominal import (
    aramaic_noun_data,
    aramaic_noun_state_profile,
    aramaic_pron_data,
    aramaic_prep_data,
    aramaic_adj_data,
    aramaic_noun_gender_profile,
    aramaic_noun_number_profile,
    aramaic_noun_gender_state,
    aramaic_noun_top_lemmas,
    aramaic_noun_state_by_book,
    aramaic_pron_type_profile,
    aramaic_prep_frequency,
    aramaic_class_distribution,
    print_aramaic_nominal_overview,
    print_aramaic_noun_state,
    print_aramaic_noun_gender,
    print_aramaic_noun_top_lemmas,
    print_aramaic_noun_state_by_book,
    print_aramaic_pron_profile,
    print_aramaic_prep_frequency,
    aramaic_noun_state_chart,
    aramaic_noun_state_book_chart,
    aramaic_prep_chart,
)

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestAramaicNounData:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(aramaic_noun_data()) >= 2200   # observed: 2,306


class TestAramaicNounStateProfile:
    def test_determined_state_leads(self) -> None:
        # Unlike Hebrew, Aramaic marks definiteness with a distinct
        # "determined" state (the emphatic ending) rather than a prefixed
        # article — and it's the most common noun state in the corpus.
        # Observed: 803 tokens, 41.8%.
        _skip_if_missing()
        df = aramaic_noun_state_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['form'] == 'determined'
        assert top['pct'] >= 35.0


class TestAramaicOtherDataFunctions:
    def test_pron_prep_adj_data_are_non_empty(self) -> None:
        # Observed: pron 662, prep 1004, adj 244 tokens.
        _skip_if_missing()
        assert len(aramaic_pron_data()) >= 600
        assert len(aramaic_prep_data()) >= 900
        assert len(aramaic_adj_data()) >= 200


class TestAramaicNounGenderProfile:
    def test_masculine_dominates_gender_profile(self) -> None:
        # Observed: masculine 76.9%, feminine 21.5%.
        _skip_if_missing()
        df = aramaic_noun_gender_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['form'] == 'masculine'
        assert top['pct'] >= 65.0


class TestAramaicNounNumberProfile:
    def test_singular_dominates_number_profile(self) -> None:
        # Observed: singular 74.0%, plural 25.4%.
        _skip_if_missing()
        df = aramaic_noun_number_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['form'] == 'singular'
        assert top['pct'] >= 65.0


class TestAramaicNounGenderState:
    def test_masculine_determined_is_the_top_cell(self) -> None:
        # Observed: masculine/determined 639, the largest single cell.
        _skip_if_missing()
        df = aramaic_noun_gender_state()
        assert df.loc['masculine', 'determined'] >= 500
        assert df.loc['masculine', 'determined'] == df.values.max()


class TestAramaicNounTopLemmas:
    def test_melekh_leads_top_lemmas(self) -> None:
        # מֶלֶךְ ("king") is the most frequent Aramaic noun — fitting for
        # Daniel's court narratives. Observed: count 180, mostly
        # determined state, gloss "king".
        _skip_if_missing()
        df = aramaic_noun_top_lemmas(5)
        top = df.iloc[0]
        assert top['lemma'] == 'מֶלֶךְ'
        assert top['count'] >= 150


class TestAramaicNounStateByBook:
    def test_daniel_and_ezra_both_present(self) -> None:
        # Observed: Dan and Ezr are the only two Aramaic-portion books.
        _skip_if_missing()
        ct = aramaic_noun_state_by_book()
        assert set(ct.index) == {'Dan', 'Ezr'}
        assert (ct.loc['Dan'].sum() > ct.loc['Ezr'].sum())


class TestAramaicPronTypeProfile:
    def test_pronominal_suffix_dominates(self) -> None:
        # Observed: pronominal (suffix) 84.6%, far ahead of any other
        # pronoun type.
        _skip_if_missing()
        df = aramaic_pron_type_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['form'] == 'pronominal'
        assert top['pct'] >= 70.0


class TestAramaicPrepFrequency:
    def test_lamed_leads_preposition_frequency(self) -> None:
        # Observed: לְ ("to/for") leads at 42.5% of Aramaic preposition
        # tokens, ahead of בְּ ("in", 25.4%).
        _skip_if_missing()
        df = aramaic_prep_frequency(5)
        top = df.iloc[0]
        assert top['lemma'] == 'לְ'
        assert top['pct'] >= 35.0


class TestAramaicClassDistribution:
    def test_noun_leads_class_distribution(self) -> None:
        # Observed: noun 30.5%, the single largest part-of-speech class.
        _skip_if_missing()
        df = aramaic_class_distribution()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['class_'] == 'noun'
        assert top['pct'] >= 25.0


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            print_aramaic_nominal_overview,
            print_aramaic_noun_state,
            print_aramaic_noun_gender,
            print_aramaic_noun_top_lemmas,
            print_aramaic_noun_state_by_book,
            print_aramaic_pron_profile,
            print_aramaic_prep_frequency,
        )
        for fn in fns:
            capsys.readouterr()
            fn()
            out = capsys.readouterr().out
            assert len(out.strip()) > 30, f"{fn} produced no real output"


class TestChartFunctions:
    def test_chart_functions_produce_real_pngs(self, tmp_path, monkeypatch) -> None:
        _skip_if_missing()
        monkeypatch.setattr(_mod, '_CHART_DIR', tmp_path)
        for fn in (aramaic_noun_state_chart, aramaic_noun_state_book_chart, aramaic_prep_chart):
            out = fn()
            assert out is not None, f"{fn.__name__} returned None"
            assert Path(out).exists(), f"{fn.__name__} did not write a file"
            assert Path(out).stat().st_size > 0
