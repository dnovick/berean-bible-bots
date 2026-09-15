"""Behavioral tests for bible_grammar.ot.ot_numbers, requiring real corpus
data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot import ot_numbers as _mod
from bible_grammar.ot.ot_numbers import (
    ot_number_data,
    ot_top_number_lemmas,
    ot_number_frequency,
    ot_number_gender_profile,
    ot_number_state_profile,
    ot_number_book_distribution,
    ot_number_genre_profile,
    ot_number_polarity_table,
    print_ot_number_overview,
    print_ot_number_frequency,
    print_ot_number_gender,
    print_ot_number_state,
    print_ot_number_book_distribution,
    print_ot_number_genre_profile,
    print_ot_number_polarity,
    ot_number_frequency_chart,
    ot_number_genre_chart,
    ot_number_book_chart,
)

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestNumberData:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(ot_number_data()) >= 6600   # observed: 6,801

    def test_echad_is_top_number(self) -> None:
        # אֶחָד ("one") is the OT's most frequently used number word.
        # Observed: count 862, Strong's H259.
        _skip_if_missing()
        df = ot_top_number_lemmas(5)
        top = df.iloc[0]
        assert top['lemma'] == 'אֶחָד'
        assert top['strong_h'] == 'H259'
        assert top['count'] >= 800


class TestNumberFrequency:
    def test_echad_leads_frequency_table(self) -> None:
        # Observed: אֶחָד ("one") leads with 862 occurrences, 12.7% of all
        # OT number tokens.
        _skip_if_missing()
        df = ot_number_frequency()
        top = df.iloc[0]
        assert top['lemma'] == 'אֶחָד'
        assert top['pct'] >= 10.0


class TestNumberGenderProfile:
    def test_masculine_leads_gender_profile(self) -> None:
        # Observed: masculine 42.6%, feminine 26.7%, both/ambiguous 30.7%.
        _skip_if_missing()
        df = ot_number_gender_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['gender'] == 'masculine'
        assert top['pct'] >= 35.0


class TestNumberStateProfile:
    def test_absolute_dominates_state_profile(self) -> None:
        # Observed: absolute 86.2%, construct 13.8% — number words rarely
        # appear in construct state.
        _skip_if_missing()
        df = ot_number_state_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['state'] == 'absolute'
        assert top['pct'] >= 80.0


class TestNumberBookDistribution:
    def test_numbers_book_leads(self) -> None:
        # Observed: the book of Numbers itself leads number-word frequency
        # at 14.3% of all OT occurrences — fitting for a census book.
        _skip_if_missing()
        df = ot_number_book_distribution()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['book'] == 'Num'
        assert top['pct'] >= 10.0


class TestNumberGenreProfile:
    def test_historical_books_lead_genre_profile(self) -> None:
        # Observed: Historical 48.1%, the largest genre share of number
        # tokens (genealogies, censuses, chronicles).
        _skip_if_missing()
        df = ot_number_genre_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['genre'] == 'Historical'
        assert top['pct'] >= 40.0


class TestNumberPolarityTable:
    def test_echad_row_is_predominantly_masculine(self) -> None:
        # Hebrew numeral "polar gender" agreement — אֶחָד ("one") skews
        # masculine at 72.1% (observed), the numeral's base cardinal form.
        _skip_if_missing()
        df = ot_number_polarity_table().set_index('value')
        row = df.loc[1]
        assert row['lemma'] == 'אֶחָד'
        assert row['masc_pct'] >= 60.0


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            print_ot_number_overview,
            print_ot_number_frequency,
            print_ot_number_gender,
            print_ot_number_state,
            print_ot_number_book_distribution,
            print_ot_number_genre_profile,
            print_ot_number_polarity,
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
        for fn in (ot_number_frequency_chart, ot_number_genre_chart, ot_number_book_chart):
            out = fn()
            assert out is not None, f"{fn.__name__} returned None"
            assert Path(out).exists(), f"{fn.__name__} did not write a file"
            assert Path(out).stat().st_size > 0
