"""Behavioral tests for bible_grammar.stems.hiphil (/hiphil), requiring real
corpus data — data/processed/. Distinct from tests/unit/test_stem_analysis.py,
which tests the shared StemConfig/StemAnalysis base classes with synthetic
data — this file tests hiphil.py's own functions against the real OT.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.stems.hiphil import (
    hiphil_data, hiphil_conjugation_profile, hiphil_top_roots, hiphil_book_distribution,
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
