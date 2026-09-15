"""Behavioral tests for bible_grammar.stems.qal (/qal), requiring real
corpus data — data/processed/. Distinct from tests/unit/test_stem_analysis.py,
which tests the shared StemConfig/StemAnalysis base classes with synthetic
data — this file tests qal.py's own functions against the real OT.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.stems import qal as _mod
from bible_grammar.stems.qal import (
    qal_data, qal_conjugation_profile, qal_top_roots,
    qal_root_conjugation, qal_book_distribution, qal_stem_comparison,
    qal_dominant_roots, qal_semantic_categories, qal_report,
    print_qal_overview, print_qal_conjugation, print_qal_top_roots,
    print_qal_root_conjugation, print_qal_book_distribution,
    print_qal_dominant_roots, print_qal_semantic_categories,
    qal_conjugation_chart, qal_book_chart, qal_stem_chart,
    qal_root_heatmap, qal_semantic_chart, qal_top_roots_chart,
)

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestQalOverview:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(qal_data()) >= 48000   # observed: 50179

    def test_conjugation_profile_wayyiqtol_leads(self) -> None:
        # Observed: wayyiqtol 22.9% is the top conjugation form — Qal's
        # sheer volume (the base/simple stem) makes narrative wayyiqtol
        # forms dominant, as expected.
        _skip_if_missing()
        df = qal_conjugation_profile()
        top = df.iloc[df['pct'].idxmax()]
        assert top['form'] == 'wayyiqtol'
        assert top['pct'] >= 18.0


class TestQalRoots:
    def test_amar_is_top_root(self) -> None:
        # אמר ("said") is Qal's single most frequent root by a wide
        # margin. Observed: count 5,284, ~46.6% of its own total token
        # count (i.e. Qal אמר forms alone).
        _skip_if_missing()
        df = qal_top_roots(3)
        top = df.iloc[0]
        assert top['root'] == 'אמר'
        assert top['count'] >= 5000


class TestQalBooks:
    def test_genesis_leads_book_distribution(self) -> None:
        _skip_if_missing()
        df = qal_book_distribution()
        top = df.iloc[0]
        assert top['book'] == 'Gen'
        assert top['count'] >= 3500


class TestQalRootConjugation:
    def test_amar_appears_in_the_crosstab(self) -> None:
        _skip_if_missing()
        df = qal_root_conjugation()
        assert 'אמר' in df.index
        assert df.loc['אמר'].sum() >= 5000


class TestQalStemComparison:
    def test_qal_dominates_every_book(self) -> None:
        # Qal is the base stem — it should be the largest single column
        # in every book's stem-comparison row. Observed: Genesis 76.5%.
        _skip_if_missing()
        df = qal_stem_comparison()
        for other in ('niphal', 'piel', 'hiphil', 'hithpael', 'pual', 'hophal'):
            assert (df['qal'] > df[other]).all()


class TestQalDominantRoots:
    def test_amar_is_a_top_dominant_root(self) -> None:
        # Observed: אמר is ~99.5% Qal of its total occurrences.
        _skip_if_missing()
        df = qal_dominant_roots()
        row = df[df['root'] == 'אמר'].iloc[0]
        assert row['hif_pct'] >= 95.0


class TestQalSemanticCategories:
    def test_other_action_is_the_largest_named_category(self) -> None:
        # Observed: 'other action' 28,564 tokens (56.9%), the largest
        # named semantic category — Qal's sheer breadth as the base stem
        # means most tokens don't fit a narrow semantic bucket.
        _skip_if_missing()
        df = qal_semantic_categories()
        named = df[df['category'] != 'other']
        top = named.sort_values('count', ascending=False).iloc[0]
        assert top['category'] == 'other action'
        assert top['pct'] >= 45.0


class TestQalReport:
    def test_writes_a_real_markdown_report(self, tmp_path: Path, monkeypatch) -> None:
        # qal_report() generates its embedded charts internally via the
        # shared StemAnalysis instance's real _chart_dir — redirect it too,
        # or this silently writes real PNGs into the tracked output/ tree.
        _skip_if_missing()
        monkeypatch.setattr(_mod._ANALYSIS, '_chart_dir', tmp_path)
        out = qal_report(output_dir=str(tmp_path))
        assert Path(out).exists()
        text = Path(out).read_text(encoding='utf-8')
        assert 'Qal' in text
        assert len(text) > 500


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            print_qal_overview,
            print_qal_conjugation,
            lambda: print_qal_top_roots(10),
            print_qal_root_conjugation,
            print_qal_book_distribution,
            print_qal_dominant_roots,
            print_qal_semantic_categories,
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
            qal_conjugation_chart,
            qal_book_chart,
            qal_stem_chart,
            qal_root_heatmap,
            qal_semantic_chart,
            qal_top_roots_chart,
        )
        for fn in fns:
            out = fn()
            assert out is not None, f"{fn.__name__} returned None"
            assert Path(out).exists(), f"{fn.__name__} did not write a file"
            assert Path(out).stat().st_size > 0
