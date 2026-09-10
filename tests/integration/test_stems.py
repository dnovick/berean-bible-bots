"""Behavioral tests for the 6 non-Hiphil stem modules (bible_grammar.stems.qal,
niphal, piel, pual, hophal, hithpael), requiring real corpus data —
data/processed/macula_syntax_ot.parquet. Mirrors tests/integration/test_hiphil.py
(#654, batch 2) for the stems that were still untested per
docs/policies/test-coverage.md's priority plan (issue #662, item 4).

Each stem module is a thin StemConfig/StemAnalysis wiring layer (see
_stem_analysis.py, already covered by tests/unit/test_stem_analysis.py with
synthetic data) — what's untested per-module is whether the wiring itself
(the macula_value string, conj_order) actually pulls correct real numbers
for THAT stem out of the true corpus. Every expected value here was directly
observed by running the capability, not invented.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.stems import qal, niphal, piel, pual, hophal, hithpael

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestQal:
    # Qal is the base/unmarked stem — roughly half of all OT verb tokens.
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(qal.qal_data()) >= 48000   # observed: 50,179

    def test_top_conjugation_is_wayyiqtol(self) -> None:
        # Narrative-dominated corpus — wayyiqtol ("and it came to pass...")
        # is the default narrative-past form, unsurprisingly Qal's most
        # frequent conjugation. Observed: 22.9%.
        _skip_if_missing()
        df = qal.qal_conjugation_profile()
        top = df.iloc[df['pct'].idxmax()]
        assert top['form'] == 'wayyiqtol'
        assert top['pct'] >= 18.0

    def test_top_root_is_amar(self) -> None:
        # אמר (say) — "he said" is the single most common verb in OT
        # narrative. Observed: count 5284, 34.6% of top-5 shown.
        _skip_if_missing()
        df = qal.qal_top_roots(5)
        top = df.iloc[0]
        assert top['root'] == 'אמר'
        assert top['count'] >= 5000

    def test_top_book_is_genesis(self) -> None:
        _skip_if_missing()
        df = qal.qal_book_distribution()
        top = df.sort_values('count', ascending=False).iloc[0]
        assert top['book'] == 'Gen'
        assert top['count'] >= 3500


class TestNiphal:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(niphal.niphal_data()) >= 4000   # observed: 4,144

    def test_top_root_is_lacham(self) -> None:
        # לחם (fight) — the paradigm reciprocal/middle sense of Niphal
        # ("fight [each other]"). Observed: count 167, 25.3%.
        _skip_if_missing()
        df = niphal.niphal_top_roots(5)
        top = df.iloc[0]
        assert top['root'] == 'לחם'
        assert top['count'] >= 150


class TestPiel:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(piel.piel_data()) >= 6000   # observed: 6,484

    def test_top_root_is_davar(self) -> None:
        # דבר (speak) — the textbook Piel example (intensive of a Qal
        # sense that doesn't independently exist). Observed: count 1090,
        # 47.4% of top-5 shown.
        _skip_if_missing()
        df = piel.piel_top_roots(5)
        top = df.iloc[0]
        assert top['root'] == 'דבר'
        assert top['count'] >= 1000


class TestPual:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(pual.pual_data()) >= 400   # observed: 459 — Pual is rare

    def test_top_root_is_yalad(self) -> None:
        # ילד (bear/beget) — "was born" is the textbook Pual passive
        # example. Observed: count 25, 30.1%.
        _skip_if_missing()
        df = pual.pual_top_roots(5)
        top = df.iloc[0]
        assert top['root'] == 'ילד'
        assert top['count'] >= 20


class TestHophal:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(hophal.hophal_data()) >= 380   # observed: 419 — Hophal is rare

    def test_top_root_is_mut(self) -> None:
        # מות (die/kill) — "was put to death", the passive of Hiphil's
        # causative "put to death". Observed: count 68, 41.5%.
        _skip_if_missing()
        df = hophal.hophal_top_roots(5)
        top = df.iloc[0]
        assert top['root'] == 'מות'
        assert top['count'] >= 60


class TestHithpael:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(hithpael.hithpael_data()) >= 850   # observed: 914

    def test_top_root_is_palal(self) -> None:
        # פלל (pray) — "prayed [for oneself]", the textbook reflexive
        # Hithpael example. Observed: count 80, 26.9%.
        _skip_if_missing()
        df = hithpael.hithpael_top_roots(5)
        top = df.iloc[0]
        assert top['root'] == 'פלל'
        assert top['count'] >= 70
