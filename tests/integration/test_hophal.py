"""Behavioral tests for bible_grammar.stems.hophal (/hophal), requiring
real corpus data — data/processed/. Distinct from tests/unit/test_stem_analysis.py,
which tests the shared StemConfig/StemAnalysis base classes with synthetic
data — this file tests hophal.py's own functions against the real OT.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.stems import hophal as _mod
from bible_grammar.stems.hophal import (
    hophal_data, hophal_conjugation_profile, hophal_top_roots,
    hophal_root_conjugation, hophal_book_distribution, hophal_stem_comparison,
    hophal_dominant_roots, hophal_semantic_categories, hophal_report,
    print_hophal_overview, print_hophal_conjugation, print_hophal_top_roots,
    print_hophal_root_conjugation, print_hophal_book_distribution,
    print_hophal_dominant_roots, print_hophal_semantic_categories,
    hophal_conjugation_chart, hophal_book_chart, hophal_stem_chart,
    hophal_root_heatmap, hophal_semantic_chart, hophal_top_roots_chart,
)

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestHophalOverview:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(hophal_data()) >= 380   # observed: 419

    def test_conjugation_profile_yiqtol_leads(self) -> None:
        # Observed: yiqtol 44.5% is the top conjugation form — Hophal
        # (passive-causative) skews toward yiqtol more than active stems.
        _skip_if_missing()
        df = hophal_conjugation_profile()
        top = df.iloc[df['pct'].idxmax()]
        assert top['form'] == 'yiqtol'
        assert top['pct'] >= 35.0


class TestHophalRoots:
    def test_mut_is_top_root(self) -> None:
        # מות (die → causative-passive "be put to death") is Hophal's
        # single most frequent root. Observed: count 68, ~53.5%.
        _skip_if_missing()
        df = hophal_top_roots(3)
        top = df.iloc[0]
        assert top['root'] == 'מות'
        assert top['count'] >= 55


class TestHophalBooks:
    def test_exodus_leads_book_distribution(self) -> None:
        _skip_if_missing()
        df = hophal_book_distribution()
        top = df.iloc[0]
        assert top['book'] == 'Exo'
        assert top['count'] >= 45


class TestHophalRootConjugation:
    def test_mut_appears_in_the_crosstab(self) -> None:
        _skip_if_missing()
        df = hophal_root_conjugation()
        assert 'מות' in df.index
        assert df.loc['מות'].sum() >= 55


class TestHophalStemComparison:
    def test_qal_dominates_every_book_over_hophal(self) -> None:
        # Observed: Genesis qal 76.5% vs. hophal 0.4% — Hophal is the
        # rarest of the 7 stems in every book.
        _skip_if_missing()
        df = hophal_stem_comparison()
        assert (df['qal'] > df['hophal']).all()


class TestHophalDominantRoots:
    def test_shazar_is_exclusively_hophal(self) -> None:
        # Observed: שזר (twisted) is 100% Hophal of its total occurrences
        # (count 21).
        _skip_if_missing()
        df = hophal_dominant_roots()
        row = df[df['root'] == 'שזר'].iloc[0]
        assert row['hif_pct'] >= 95.0


class TestHophalSemanticCategories:
    def test_other_dominates_semantic_categories(self) -> None:
        # Observed: the 'causative-passive (other)' catch-all is 99.5% of
        # all Hophal tokens — this stem's semantic classifier finds very
        # few tokens matching its narrower named categories.
        _skip_if_missing()
        df = hophal_semantic_categories()
        top = df.sort_values('count', ascending=False).iloc[0]
        assert top['pct'] >= 90.0


class TestHophalReport:
    def test_writes_a_real_markdown_report(self, tmp_path: Path, monkeypatch) -> None:
        # hophal_report() generates its embedded charts internally via the
        # shared StemAnalysis instance's real _chart_dir — redirect it too,
        # or this silently writes real PNGs into the tracked output/ tree.
        _skip_if_missing()
        monkeypatch.setattr(_mod._ANALYSIS, '_chart_dir', tmp_path)
        out = hophal_report(output_dir=str(tmp_path))
        assert Path(out).exists()
        text = Path(out).read_text(encoding='utf-8')
        assert 'Hophal' in text
        assert len(text) > 500


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            print_hophal_overview,
            print_hophal_conjugation,
            lambda: print_hophal_top_roots(10),
            print_hophal_root_conjugation,
            print_hophal_book_distribution,
            print_hophal_dominant_roots,
            print_hophal_semantic_categories,
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
            hophal_conjugation_chart,
            hophal_book_chart,
            hophal_stem_chart,
            hophal_root_heatmap,
            hophal_semantic_chart,
            hophal_top_roots_chart,
        )
        for fn in fns:
            out = fn()
            assert out is not None, f"{fn.__name__} returned None"
            assert Path(out).exists(), f"{fn.__name__} did not write a file"
            assert Path(out).stat().st_size > 0
