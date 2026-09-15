"""Behavioral tests for bible_grammar.ot.aramaic_profile, requiring real
corpus data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot import aramaic_profile as _mod
from bible_grammar.ot.aramaic_profile import (
    aramaic_data,
    aramaic_verb_data,
    aramaic_stem_profile,
    aramaic_conj_profile,
    aramaic_stem_conj,
    aramaic_top_roots,
    aramaic_book_distribution,
    aramaic_stem_by_book,
    print_aramaic_overview,
    print_aramaic_stem_profile,
    print_aramaic_conj_profile,
    print_aramaic_stem_conj,
    print_aramaic_top_roots,
    print_aramaic_book_distribution,
    aramaic_stem_chart,
    aramaic_conj_chart,
    aramaic_stem_book_chart,
)

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestAramaicData:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(aramaic_data()) >= 7400   # observed: 7,549

    def test_verb_token_count(self) -> None:
        _skip_if_missing()
        assert len(aramaic_verb_data()) >= 1000   # observed: 1,069


class TestAramaicStemProfile:
    def test_peal_dominates(self) -> None:
        # Peal (the Aramaic base stem, analogous to Hebrew Qal) is by far
        # the most common Aramaic verb stem. Observed: 633 tokens, 59.2%.
        _skip_if_missing()
        df = aramaic_stem_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['form'] == 'peal'
        assert top['pct'] >= 50.0


class TestAramaicConjProfile:
    def test_qatal_leads(self) -> None:
        # Observed: qatal (perfect) 394 tokens, 36.9% — the most common
        # Aramaic conjugation, ahead of participle active (24.6%).
        _skip_if_missing()
        df = aramaic_conj_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['form'] == 'qatal'
        assert top['pct'] >= 30.0


class TestAramaicStemConj:
    def test_peal_qatal_is_the_top_cell(self) -> None:
        # Observed: Peal qatal 225, the largest single stem/conjugation
        # cell — Peal is both the most common stem and qatal the most
        # common conjugation.
        _skip_if_missing()
        df = aramaic_stem_conj('peal')
        assert df.loc['peal', 'qatal'] >= 200


class TestAramaicTopRoots:
    def test_hoh_and_amar_tie_for_top_root(self) -> None:
        # Observed: הוה ("be") and אֲמַר ("said") tie for the most frequent
        # Aramaic root, count 71 each (27.8%), both predominantly Peal.
        _skip_if_missing()
        df = aramaic_top_roots(5)
        top = df.iloc[0]
        assert top['lemma'] in ('הוה', 'אֲמַר')
        assert top['count'] >= 65


class TestAramaicBookDistribution:
    def test_daniel_leads(self) -> None:
        # Observed: Daniel 5,687 Aramaic tokens (851 verbs), far ahead of
        # Ezra's 1,835 — Daniel's Aramaic section is much larger.
        _skip_if_missing()
        df = aramaic_book_distribution().set_index('book')
        assert df.loc['Dan', 'tokens'] >= 5000
        assert df.loc['Dan', 'tokens'] > df.loc['Ezr', 'tokens']


class TestAramaicStemByBook:
    def test_peal_leads_in_both_daniel_and_ezra(self) -> None:
        # Observed: Peal 526 in Daniel, 104 in Ezra — the dominant stem in
        # both books with substantial Aramaic content.
        _skip_if_missing()
        df = aramaic_stem_by_book()
        assert df.loc['Dan', 'peal'] >= 500
        assert df.loc['Ezr', 'peal'] >= 90


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            print_aramaic_overview,
            print_aramaic_stem_profile,
            print_aramaic_conj_profile,
            lambda: print_aramaic_stem_conj('peal'),
            print_aramaic_top_roots,
            print_aramaic_book_distribution,
        )
        for fn in fns:
            capsys.readouterr()
            fn()
            out = capsys.readouterr().out
            assert len(out.strip()) > 30, f"{fn} produced no real output"


class TestChartFunctions:
    def test_chart_functions_produce_real_pngs(self, tmp_path, monkeypatch) -> None:
        _skip_if_missing()
        monkeypatch.setattr(_mod, '_CHART_DIR', tmp_path)
        fns = (aramaic_stem_chart, aramaic_conj_chart, aramaic_stem_book_chart)
        for fn in fns:
            out = fn()
            assert out is not None, f"{fn.__name__} returned None"
            assert Path(out).exists(), f"{fn.__name__} did not write a file"
            assert Path(out).stat().st_size > 0
