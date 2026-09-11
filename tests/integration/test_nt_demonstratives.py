"""Behavioral tests for bible_grammar.nt.nt_demonstratives, requiring real
corpus data — data/processed/macula_syntax.parquet (MACULA Greek NT).
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.nt import nt_demonstratives as _mod
from bible_grammar.nt.nt_demonstratives import (
    nt_demo_data,
    nt_demo_frequency,
    nt_demo_case_profile,
    nt_demo_gender_profile,
    nt_demo_use_profile,
    nt_demo_book_distribution,
    nt_demo_genre_profile,
    nt_demo_near_far_comparison,
    nt_demo_top_cooccurrences,
    print_nt_demo_overview,
    print_nt_demo_frequency,
    print_nt_demo_case,
    print_nt_demo_gender,
    print_nt_demo_use,
    print_nt_demo_book_distribution,
    print_nt_demo_genre_profile,
    print_nt_demo_near_far,
    nt_demo_frequency_chart,
    nt_demo_case_chart,
    nt_demo_genre_heatmap,
    nt_demo_book_chart,
)

_SYNTAX_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _SYNTAX_PARQUET.exists():
        pytest.skip(f"Data file not found: {_SYNTAX_PARQUET}")


class TestDemonstratives:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(nt_demo_data()) >= 1650   # observed: 1,709

    def test_houtos_dominates(self) -> None:
        # οὗτος ("this") is overwhelmingly the most common NT demonstrative.
        # Observed: count 1388, 81.2% of all demonstrative tokens.
        _skip_if_missing()
        df = nt_demo_frequency()
        top = df.iloc[0]
        assert top['lemma'] == 'οὗτος'
        assert top['pct'] >= 75.0

    def test_accusative_leads_case_profile(self) -> None:
        # Observed: accusative 652 (38.2%), nominative 592 (34.6%).
        _skip_if_missing()
        df = nt_demo_case_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['case_'] == 'accusative'
        assert top['pct'] >= 30.0

    def test_neuter_leads_gender_profile(self) -> None:
        # Observed: neuter 731 (42.8%), masculine 641 (37.5%).
        _skip_if_missing()
        df = nt_demo_gender_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['gender'] == 'neuter'
        assert top['pct'] >= 35.0

    def test_attributive_predicate_dominates_use_profile(self) -> None:
        # Observed: attributive/predicate 974 (57.0%) vs. substantival 735
        # (43.0%).
        _skip_if_missing()
        df = nt_demo_use_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['use'] == 'attributive/predicate'
        assert top['pct'] >= 50.0

    def test_john_has_the_most_demonstrative_tokens(self) -> None:
        # Observed: Jhn 318 (18.6% of all NT demonstratives).
        _skip_if_missing()
        df = nt_demo_book_distribution()
        top = df.sort_values('count', ascending=False).iloc[0]
        assert top['book'] == 'Jhn'
        assert top['count'] >= 280

    def test_gospels_lead_genre_profile(self) -> None:
        # Observed: Gospels 898 (52.5%) of all demonstrative tokens.
        _skip_if_missing()
        df = nt_demo_genre_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['genre'] == 'Gospels'
        assert top['pct'] >= 45.0

    def test_houtos_far_outnumbers_ekeinos_in_every_genre(self) -> None:
        # Observed: in every genre group, near-demonstrative οὗτος ("this")
        # heavily outnumbers far-demonstrative ἐκεῖνος ("that") — e.g.
        # Gospels 694 vs. 181.
        _skip_if_missing()
        df = nt_demo_near_far_comparison()
        assert (df['οὗτος'] > df['ἐκεῖνος']).all()

    def test_theos_is_the_top_houtos_cooccurrence(self) -> None:
        # Observed: θεός co-occurs with οὗτος 225 times, the most of any
        # lemma.
        _skip_if_missing()
        df = nt_demo_top_cooccurrences(n=5)
        top = df.iloc[0]
        assert top['lemma'] == 'θεός'
        assert top['count'] >= 200


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            print_nt_demo_overview,
            print_nt_demo_frequency,
            print_nt_demo_case,
            print_nt_demo_gender,
            print_nt_demo_use,
            print_nt_demo_book_distribution,
            print_nt_demo_genre_profile,
            print_nt_demo_near_far,
        )
        for fn in fns:
            capsys.readouterr()
            fn()
            out = capsys.readouterr().out
            assert len(out.strip()) > 50, f"{fn.__name__} produced no real output"


class TestChartFunctions:
    def test_chart_functions_produce_real_pngs(self, tmp_path, monkeypatch) -> None:
        _skip_if_missing()
        monkeypatch.setattr(_mod, '_CHART_DIR', tmp_path)
        fns = (nt_demo_frequency_chart, nt_demo_case_chart, nt_demo_genre_heatmap, nt_demo_book_chart)
        for fn in fns:
            out = fn()
            assert out is not None, f"{fn.__name__} returned None"
            assert Path(out).exists(), f"{fn.__name__} did not write a file"
            assert Path(out).stat().st_size > 0
