"""Behavioral tests for bible_grammar.stems.niphal (/niphal), requiring
real corpus data — data/processed/. Distinct from tests/unit/test_stem_analysis.py,
which tests the shared StemConfig/StemAnalysis base classes with synthetic
data — this file tests niphal.py's own functions against the real OT.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.stems import niphal as _mod
from bible_grammar.stems.niphal import (
    niphal_data, niphal_conjugation_profile, niphal_top_roots,
    niphal_root_conjugation, niphal_book_distribution, niphal_stem_comparison,
    niphal_dominant_roots, niphal_semantic_categories, niphal_report,
    print_niphal_overview, print_niphal_conjugation, print_niphal_top_roots,
    print_niphal_root_conjugation, print_niphal_book_distribution,
    print_niphal_dominant_roots, print_niphal_semantic_categories,
    niphal_conjugation_chart, niphal_book_chart, niphal_stem_chart,
    niphal_root_heatmap, niphal_semantic_chart, niphal_top_roots_chart,
)

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestNiphalOverview:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(niphal_data()) >= 3900   # observed: 4144

    def test_conjugation_profile_qatal_leads(self) -> None:
        # Observed: qatal 27.0% is the top conjugation form.
        _skip_if_missing()
        df = niphal_conjugation_profile()
        top = df.iloc[df['pct'].idxmax()]
        assert top['form'] == 'qatal'
        assert top['pct'] >= 20.0


class TestNiphalRoots:
    def test_lacham_is_top_root(self) -> None:
        # לחם (fight, reciprocal/middle "fight one another") is Niphal's
        # single most frequent root. Observed: count 167, ~36.2%.
        _skip_if_missing()
        df = niphal_top_roots(3)
        top = df.iloc[0]
        assert top['root'] == 'לחם'
        assert top['count'] >= 150


class TestNiphalBooks:
    def test_jeremiah_leads_book_distribution(self) -> None:
        _skip_if_missing()
        df = niphal_book_distribution()
        top = df.iloc[0]
        assert top['book'] == 'Jer'
        assert top['count'] >= 350


class TestNiphalRootConjugation:
    def test_lacham_appears_in_the_crosstab(self) -> None:
        _skip_if_missing()
        df = niphal_root_conjugation()
        assert 'לחם' in df.index
        assert df.loc['לחם'].sum() >= 150


class TestNiphalStemComparison:
    def test_qal_dominates_every_book_over_niphal(self) -> None:
        # Observed: Genesis qal 76.5% vs. niphal 4.2%.
        _skip_if_missing()
        df = niphal_stem_comparison()
        assert (df['qal'] > df['niphal']).all()


class TestNiphalDominantRoots:
    def test_lacham_is_a_top_dominant_root(self) -> None:
        # Observed: לחם is ~94.4% Niphal of its total occurrences.
        _skip_if_missing()
        df = niphal_dominant_roots()
        row = df[df['root'] == 'לחם'].iloc[0]
        assert row['hif_pct'] >= 90.0


class TestNiphalSemanticCategories:
    def test_passive_is_the_largest_named_category(self) -> None:
        # Observed: 'passive' 111 tokens (2.7%), the largest named
        # semantic category (after the 'other' catch-all).
        _skip_if_missing()
        df = niphal_semantic_categories()
        named = df[df['category'] != 'other']
        top = named.sort_values('count', ascending=False).iloc[0]
        assert top['category'] == 'passive'
        assert top['count'] >= 90


class TestNiphalReport:
    def test_writes_a_real_markdown_report(self, tmp_path: Path, monkeypatch) -> None:
        # niphal_report() generates its embedded charts internally via the
        # shared StemAnalysis instance's real _chart_dir — redirect it too,
        # or this silently writes real PNGs into the tracked output/ tree.
        _skip_if_missing()
        monkeypatch.setattr(_mod._ANALYSIS, '_chart_dir', tmp_path)
        out = niphal_report(output_dir=str(tmp_path))
        assert Path(out).exists()
        text = Path(out).read_text(encoding='utf-8')
        assert 'Niphal' in text
        assert len(text) > 500


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            print_niphal_overview,
            print_niphal_conjugation,
            lambda: print_niphal_top_roots(10),
            print_niphal_root_conjugation,
            print_niphal_book_distribution,
            print_niphal_dominant_roots,
            print_niphal_semantic_categories,
        )
        for fn in fns:
            capsys.readouterr()
            fn()
            out = capsys.readouterr().out
            assert len(out.strip()) > 30, f"{fn} produced no real output"


class TestChartFunctions:
    def test_chart_functions_produce_real_pngs(self, tmp_path, monkeypatch) -> None:
        _skip_if_missing()
        monkeypatch.setattr(_mod._ANALYSIS, '_chart_dir', tmp_path)
        fns = (
            niphal_conjugation_chart,
            niphal_book_chart,
            niphal_stem_chart,
            niphal_root_heatmap,
            niphal_semantic_chart,
            niphal_top_roots_chart,
        )
        for fn in fns:
            out = fn()
            assert out is not None, f"{fn.__name__} returned None"
            assert Path(out).exists(), f"{fn.__name__} did not write a file"
            assert Path(out).stat().st_size > 0
