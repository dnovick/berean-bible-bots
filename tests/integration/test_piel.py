"""Behavioral tests for bible_grammar.stems.piel (/piel), requiring real
corpus data — data/processed/. Distinct from tests/unit/test_stem_analysis.py,
which tests the shared StemConfig/StemAnalysis base classes with synthetic
data — this file tests piel.py's own functions against the real OT.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.stems import piel as _mod
from bible_grammar.stems.piel import (
    piel_data, piel_conjugation_profile, piel_top_roots,
    piel_root_conjugation, piel_book_distribution, piel_stem_comparison,
    piel_dominant_roots, piel_semantic_categories, piel_report,
    print_piel_overview, print_piel_conjugation, print_piel_top_roots,
    print_piel_root_conjugation, print_piel_book_distribution,
    print_piel_dominant_roots, print_piel_semantic_categories,
    piel_conjugation_chart, piel_book_chart, piel_stem_chart,
    piel_root_heatmap, piel_semantic_chart, piel_top_roots_chart,
)

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestPielOverview:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(piel_data()) >= 6200   # observed: 6484

    def test_conjugation_profile_qatal_leads(self) -> None:
        # Observed: qatal 24.9% is the top conjugation form.
        _skip_if_missing()
        df = piel_conjugation_profile()
        top = df.iloc[df['pct'].idxmax()]
        assert top['form'] == 'qatal'
        assert top['pct'] >= 20.0


class TestPielRoots:
    def test_davar_is_top_root(self) -> None:
        # דבר (speak, intensive "speak forcefully/at length") is Piel's
        # single most frequent root. Observed: count 1090, ~59.1%.
        _skip_if_missing()
        df = piel_top_roots(3)
        top = df.iloc[0]
        assert top['root'] == 'דבר'
        assert top['count'] >= 1000


class TestPielBooks:
    def test_psalms_leads_book_distribution(self) -> None:
        _skip_if_missing()
        df = piel_book_distribution()
        top = df.iloc[0]
        assert top['book'] == 'Psa'
        assert top['count'] >= 800


class TestPielRootConjugation:
    def test_davar_appears_in_the_crosstab(self) -> None:
        _skip_if_missing()
        df = piel_root_conjugation()
        assert 'דבר' in df.index
        assert df.loc['דבר'].sum() >= 1000


class TestPielStemComparison:
    def test_qal_dominates_every_book_over_piel(self) -> None:
        # Observed: Genesis qal 76.5% vs. piel 7.1%.
        _skip_if_missing()
        df = piel_stem_comparison()
        assert (df['qal'] > df['piel']).all()


class TestPielDominantRoots:
    def test_davar_is_a_top_dominant_root(self) -> None:
        # Observed: דבר is ~95.5% Piel of its total occurrences.
        _skip_if_missing()
        df = piel_dominant_roots()
        row = df[df['root'] == 'דבר'].iloc[0]
        assert row['hif_pct'] >= 90.0


class TestPielSemanticCategories:
    def test_denominative_is_the_largest_named_category(self) -> None:
        # Observed: 'denominative' 1,171 tokens (18.1%), the largest
        # named semantic category (after the 'other' catch-all).
        _skip_if_missing()
        df = piel_semantic_categories()
        named = df[df['category'] != 'other']
        top = named.sort_values('count', ascending=False).iloc[0]
        assert top['category'] == 'denominative'
        assert top['pct'] >= 15.0


class TestPielReport:
    def test_writes_a_real_markdown_report(self, tmp_path: Path, monkeypatch) -> None:
        # piel_report() generates its embedded charts internally via the
        # shared StemAnalysis instance's real _chart_dir — redirect it too,
        # or this silently writes real PNGs into the tracked output/ tree.
        _skip_if_missing()
        monkeypatch.setattr(_mod._ANALYSIS, '_chart_dir', tmp_path)
        out = piel_report(output_dir=str(tmp_path))
        assert Path(out).exists()
        text = Path(out).read_text(encoding='utf-8')
        assert 'Piel' in text
        assert len(text) > 500


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            print_piel_overview,
            print_piel_conjugation,
            lambda: print_piel_top_roots(10),
            print_piel_root_conjugation,
            print_piel_book_distribution,
            print_piel_dominant_roots,
            print_piel_semantic_categories,
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
            piel_conjugation_chart,
            piel_book_chart,
            piel_stem_chart,
            piel_root_heatmap,
            piel_semantic_chart,
            piel_top_roots_chart,
        )
        for fn in fns:
            out = fn()
            assert out is not None, f"{fn.__name__} returned None"
            assert Path(out).exists(), f"{fn.__name__} did not write a file"
            assert Path(out).stat().st_size > 0
