"""Behavioral tests for bible_grammar.stems.hiphil (/hiphil), requiring real
corpus data — data/processed/. Distinct from tests/unit/test_stem_analysis.py,
which tests the shared StemConfig/StemAnalysis base classes with synthetic
data — this file tests hiphil.py's own functions against the real OT.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.stems import hiphil as _mod
from bible_grammar.stems.hiphil import (
    hiphil_data, hiphil_conjugation_profile, hiphil_top_roots, hiphil_book_distribution,
    hiphil_root_conjugation, hiphil_stem_comparison, hiphil_dominant_roots,
    hiphil_semantic_categories, hiphil_report, hiphil_object_verbs,
    print_hiphil_overview, print_hiphil_conjugation, print_hiphil_top_roots,
    print_hiphil_root_conjugation, print_hiphil_book_distribution,
    print_hiphil_dominant_roots, print_hiphil_semantic_categories,
    hiphil_conjugation_chart, hiphil_book_chart, hiphil_stem_chart,
    hiphil_root_heatmap, hiphil_semantic_chart, hiphil_top_roots_chart,
)

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestHiphilOverview:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(hiphil_data()) >= 9000   # observed: 9409

    def test_conjugation_profile_yiqtol_leads(self) -> None:
        # Hiphil skews toward yiqtol/qatal more than the OT-wide average
        # (Qal is wayyiqtol-dominant); observed: yiqtol 21.5% is the top form.
        _skip_if_missing()
        df = hiphil_conjugation_profile()
        top = df.iloc[df['pct'].idxmax()]
        assert top['form'] == 'yiqtol'
        assert top['pct'] >= 18.0


class TestHiphilRoots:
    def test_bo_is_top_root(self) -> None:
        # בוא (bring/come, causative "cause to come" = bring) is Hiphil's
        # single most frequent root. Observed: count 548, ~27%.
        _skip_if_missing()
        df = hiphil_top_roots(5)
        top = df.iloc[0]
        assert top['root'] == 'בוא'
        assert top['count'] >= 500


class TestHiphilBooks:
    def test_psalms_leads_book_distribution(self) -> None:
        _skip_if_missing()
        df = hiphil_book_distribution()
        top = df.iloc[0]
        assert top['book'] == 'Psa'
        assert top['count'] >= 800


class TestHiphilRootConjugation:
    def test_bo_and_nakah_lead_wayyiqtol(self) -> None:
        # Observed: root×conjugation crosstab, indexed by root — בוא and נכה
        # both show real wayyiqtol counts (155 and 194).
        _skip_if_missing()
        df = hiphil_root_conjugation()
        assert df.loc['בוא', 'wayyiqtol'] >= 100
        assert df.loc['נכה', 'wayyiqtol'] >= 150


class TestHiphilStemComparison:
    def test_qal_dominates_every_book_over_hiphil(self) -> None:
        # Observed: Genesis qal 76.5% vs. hiphil 9.8% — hiphil is a
        # substantial but minority stem in every book's stem-comparison row.
        _skip_if_missing()
        df = hiphil_stem_comparison()
        assert (df['qal'] > df['hiphil']).all()
        assert df.loc['Gen', 'hiphil'] >= 8.0


class TestHiphilDominantRoots:
    def test_nakah_is_a_top_dominant_root(self) -> None:
        # Observed: נָכָה (root נכה) is ~96.2% Hiphil of its total occurrences
        # — a near-exclusively-Hiphil root.
        _skip_if_missing()
        df = hiphil_dominant_roots()
        row = df[df['root'] == 'נכה'].iloc[0]
        assert row['hif_pct'] >= 90.0


class TestHiphilSemanticCategories:
    def test_causative_motion_is_the_largest_named_category(self) -> None:
        # Observed: 'causative motion / transfer' 2,895 tokens (30.8%),
        # the largest named semantic category (after the 'other' catch-all).
        _skip_if_missing()
        df = hiphil_semantic_categories()
        named = df[df['category'] != 'other']
        top = named.sort_values('count', ascending=False).iloc[0]
        assert top['category'] == 'causative motion / transfer'
        assert top['pct'] >= 25.0


class TestHiphilObjectVerbs:
    def test_is_an_alias_for_top_roots(self) -> None:
        # hiphil_object_verbs() is documented as a backwards-compat alias
        # for hiphil_top_roots(30, book).
        _skip_if_missing()
        import pandas as pd
        pd.testing.assert_frame_equal(hiphil_object_verbs(), hiphil_top_roots(30, None))


class TestHiphilReport:
    def test_writes_a_real_markdown_report(self, tmp_path: Path, monkeypatch) -> None:
        # hiphil_report() generates its embedded charts internally via the
        # shared StemAnalysis instance's real _chart_dir — redirect it too,
        # or this silently writes real PNGs into the tracked output/ tree.
        _skip_if_missing()
        monkeypatch.setattr(_mod._ANALYSIS, '_chart_dir', tmp_path)
        out = hiphil_report(output_dir=str(tmp_path))
        assert Path(out).exists()
        text = Path(out).read_text(encoding='utf-8')
        assert 'Hiphil' in text
        assert len(text) > 500


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            print_hiphil_overview,
            print_hiphil_conjugation,
            lambda: print_hiphil_top_roots(10),
            print_hiphil_root_conjugation,
            print_hiphil_book_distribution,
            print_hiphil_dominant_roots,
            print_hiphil_semantic_categories,
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
            hiphil_conjugation_chart,
            hiphil_book_chart,
            hiphil_stem_chart,
            hiphil_root_heatmap,
            hiphil_semantic_chart,
            hiphil_top_roots_chart,
        )
        for fn in fns:
            out = fn()
            assert out is not None, f"{fn.__name__} returned None"
            assert Path(out).exists(), f"{fn.__name__} did not write a file"
            assert Path(out).stat().st_size > 0
