"""Behavioral tests for bible_grammar.discourse.information_structure,
requiring real corpus data — data/processed/macula_syntax_ot.parquet and
macula_syntax.parquet. Per docs/policies/test-coverage.md's priority plan
(issue #676, Phase 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.discourse import information_structure as _mod
from bible_grammar.discourse.information_structure import (
    ot_information_profile,
    nt_information_profile,
    ot_clause_linking_comparison,
    nt_clause_linking_comparison,
    print_ot_information_profile,
    print_nt_information_profile,
    print_ot_clause_linking_comparison,
    print_nt_clause_linking_comparison,
    nt_clause_linking_chart,
    nt_information_heatmap,
    ot_clause_linking_chart,
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
        pytest.skip(f"Data file not found: {_MACULA_NT_PARQUET}")


class TestOtInformationProfile:
    def test_genesis_is_overwhelmingly_paratactic(self) -> None:
        # Hebrew narrative chains clauses with waw rather than
        # subordinating conjunctions. Observed: parataxis_ratio 0.8402,
        # nominal_clause_pct 5.41% out of 1,533 verses / 32,363 tokens.
        _skip_if_ot_missing()
        profile = ot_information_profile('Gen')
        assert profile['total_verses'] == 1533
        assert profile['parataxis_ratio'] >= 0.75
        assert profile['nominal_clause_pct'] <= 10.0

    def test_fronting_is_rare_in_genesis(self) -> None:
        # Observed: only 3 fronted elements out of 1,533 verses
        # (fronted_ratio 0.002) — Hebrew's default VSO order rarely needs
        # topicalization/fronting in narrative.
        _skip_if_ot_missing()
        profile = ot_information_profile('Gen')
        assert profile['fronted_ratio'] <= 0.05


class TestNtInformationProfile:
    def test_matthew_kai_dominates_connective_density(self) -> None:
        # Observed: kai_per1k 63.88, far above any other Greek connective
        # (de_per1k 27.0, gar_per1k 6.78) — καί is the default NT narrative
        # connective, much like waw in Hebrew.
        _skip_if_nt_missing()
        profile = nt_information_profile('Mat')
        assert profile['total_verses'] == 1068
        assert profile['kai_per1k'] >= 50.0
        assert profile['kai_per1k'] > profile['de_per1k']


class TestOtClauseLinkingComparison:
    def test_deuteronomy_is_more_hypotactic_than_genesis(self) -> None:
        # The module's own documented example question: "Is Deuteronomy
        # more hypotactic than Genesis? (law vs. narrative)". Observed:
        # Gen parataxis_ratio 0.8402/hypotaxis_per1k 25.03 vs. Deu
        # parataxis_ratio 0.4703/hypotaxis_per1k 41.73 — law code shows
        # markedly less parataxis and more subordination than narrative.
        _skip_if_ot_missing()
        df = ot_clause_linking_comparison(['Gen', 'Deu'])
        assert df.loc['Gen', 'parataxis_ratio'] > df.loc['Deu', 'parataxis_ratio']
        assert df.loc['Deu', 'hypotaxis_per1k'] > df.loc['Gen', 'hypotaxis_per1k']

    def test_unknown_book_is_silently_dropped(self) -> None:
        _skip_if_ot_missing()
        df = ot_clause_linking_comparison(['Gen', 'NotARealBook'])
        assert list(df.index) == ['Gen']


class TestNtClauseLinkingComparison:
    def test_romans_uses_more_gar_than_matthew(self) -> None:
        # The module's own documented example question: "Which NT book
        # uses the most γάρ? (Paul is dominant)". Observed: Rom gar_per1k
        # 20.28 vs. Mat gar_per1k 6.78 — epistolary argumentation leans on
        # γάρ far more than narrative.
        _skip_if_nt_missing()
        df = nt_clause_linking_comparison(['Mat', 'Rom'])
        assert df.loc['Rom', 'gar_per1k'] > df.loc['Mat', 'gar_per1k']
        assert df.loc['Mat', 'kai_per1k'] > df.loc['Rom', 'kai_per1k']


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_ot_missing()
        _skip_if_nt_missing()
        fns = (
            lambda: print_ot_information_profile('Gen'),
            lambda: print_nt_information_profile('Mat'),
            lambda: print_ot_clause_linking_comparison(['Gen', 'Deu']),
            lambda: print_nt_clause_linking_comparison(['Mat', 'Rom']),
        )
        for fn in fns:
            capsys.readouterr()
            fn()
            out = capsys.readouterr().out
            assert len(out.strip()) > 30, f"{fn} produced no real output"

    def test_print_profile_handles_unknown_book_gracefully(self, capsys) -> None:
        _skip_if_ot_missing()
        print_ot_information_profile('NotARealBook')
        out = capsys.readouterr().out
        assert 'No data' in out


class TestChartFunctions:
    def test_chart_functions_produce_real_pngs(self, tmp_path, monkeypatch) -> None:
        _skip_if_ot_missing()
        _skip_if_nt_missing()
        monkeypatch.setattr(_mod, '_CHART_DIR', tmp_path)
        fns = (
            lambda: nt_clause_linking_chart(['Mat', 'Rom']),
            lambda: nt_information_heatmap(['Mat', 'Rom']),
            lambda: ot_clause_linking_chart(['Gen', 'Deu']),
        )
        for fn in fns:
            out = fn()
            assert out is not None, f"{fn} returned None"
            assert Path(out).exists(), f"{fn} did not write a file"
            assert Path(out).stat().st_size > 0
