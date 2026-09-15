"""Behavioral tests for bible_grammar.stems.pual (/pual), requiring real
corpus data — data/processed/. Distinct from tests/unit/test_stem_analysis.py,
which tests the shared StemConfig/StemAnalysis base classes with synthetic
data — this file tests pual.py's own functions against the real OT.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.stems import pual as _mod
from bible_grammar.stems.pual import (
    pual_data, pual_conjugation_profile, pual_top_roots,
    pual_root_conjugation, pual_book_distribution, pual_stem_comparison,
    pual_dominant_roots, pual_semantic_categories, pual_report,
    print_pual_overview, print_pual_conjugation, print_pual_top_roots,
    print_pual_root_conjugation, print_pual_book_distribution,
    print_pual_dominant_roots, print_pual_semantic_categories,
    pual_conjugation_chart, pual_book_chart, pual_stem_chart,
    pual_root_heatmap, pual_semantic_chart, pual_top_roots_chart,
)

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestPualOverview:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(pual_data()) >= 420   # observed: 459

    def test_conjugation_profile_qatal_leads(self) -> None:
        # Observed: qatal 59.1% is the top conjugation form — Pual
        # (intensive-passive) skews heavily toward qatal.
        _skip_if_missing()
        df = pual_conjugation_profile()
        top = df.iloc[df['pct'].idxmax()]
        assert top['form'] == 'qatal'
        assert top['pct'] >= 45.0


class TestPualRoots:
    def test_yalad_is_top_root(self) -> None:
        # ילד (bear/give birth → passive "be born") is Pual's single most
        # frequent root. Observed: count 25, ~41.7%.
        _skip_if_missing()
        df = pual_top_roots(3)
        top = df.iloc[0]
        assert top['root'] == 'ילד'
        assert top['count'] >= 20


class TestPualBooks:
    def test_isaiah_leads_book_distribution(self) -> None:
        _skip_if_missing()
        df = pual_book_distribution()
        top = df.iloc[0]
        assert top['book'] == 'Isa'
        assert top['count'] >= 60


class TestPualRootConjugation:
    def test_yalad_appears_in_the_crosstab(self) -> None:
        _skip_if_missing()
        df = pual_root_conjugation()
        assert 'ילד' in df.index
        assert df.loc['ילד'].sum() >= 20


class TestPualStemComparison:
    def test_qal_dominates_every_book_over_pual(self) -> None:
        # Observed: Genesis qal 76.5% vs. pual 0.5%.
        _skip_if_missing()
        df = pual_stem_comparison()
        assert (df['qal'] > df['pual']).all()


class TestPualDominantRoots:
    def test_tsara_is_a_top_dominant_root(self) -> None:
        # Observed: צרע (be leprous) is ~75% Pual of its total occurrences.
        _skip_if_missing()
        df = pual_dominant_roots()
        row = df[df['root'] == 'צרע'].iloc[0]
        assert row['hif_pct'] >= 65.0


class TestPualSemanticCategories:
    def test_other_dominates_semantic_categories(self) -> None:
        # Observed: 'passive (other)' catch-all is 94.8% of all Pual
        # tokens — this stem's classifier finds very few tokens matching
        # its narrower named categories.
        _skip_if_missing()
        df = pual_semantic_categories()
        top = df.sort_values('count', ascending=False).iloc[0]
        assert top['pct'] >= 85.0


class TestPualReport:
    def test_writes_a_real_markdown_report(self, tmp_path: Path, monkeypatch) -> None:
        # pual_report() generates its embedded charts internally via the
        # shared StemAnalysis instance's real _chart_dir — redirect it too,
        # or this silently writes real PNGs into the tracked output/ tree.
        _skip_if_missing()
        monkeypatch.setattr(_mod._ANALYSIS, '_chart_dir', tmp_path)
        out = pual_report(output_dir=str(tmp_path))
        assert Path(out).exists()
        text = Path(out).read_text(encoding='utf-8')
        assert 'Pual' in text
        assert len(text) > 500


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            print_pual_overview,
            print_pual_conjugation,
            lambda: print_pual_top_roots(10),
            print_pual_root_conjugation,
            print_pual_book_distribution,
            print_pual_dominant_roots,
            print_pual_semantic_categories,
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
            pual_conjugation_chart,
            pual_book_chart,
            pual_stem_chart,
            pual_root_heatmap,
            pual_semantic_chart,
            pual_top_roots_chart,
        )
        for fn in fns:
            out = fn()
            assert out is not None, f"{fn.__name__} returned None"
            assert Path(out).exists(), f"{fn.__name__} did not write a file"
            assert Path(out).stat().st_size > 0
