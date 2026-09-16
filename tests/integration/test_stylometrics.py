"""Behavioral tests for bible_grammar.discourse.stylometrics, requiring
real corpus data — data/processed/macula_syntax_ot.parquet and
macula_syntax.parquet. Per docs/policies/test-coverage.md's priority plan
(issue #676, Phase 4).

Regression guard: book_style_profile()'s noun_pct (both languages) and the
Greek branch's verbal_pct used to be hardcoded to 0.0 for every book,
because the code checked for a column named 'sp' that doesn't exist
anywhere in this corpus — the real equivalents are 'type_' (Hebrew) and
'class_' (Greek). Fixed directly against real corpus evidence.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.discourse import stylometrics as _mod
from bible_grammar.discourse.stylometrics import (
    book_style_profile,
    msttr,
    style_comparison,
    print_style_profile,
    print_style_comparison,
    style_radar_chart,
    style_heatmap,
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


class TestHebrewBookStyleProfile:
    def test_genesis_noun_pct_is_not_zero(self) -> None:
        # Regression guard: noun_pct used to be hardcoded to 0.0 for every
        # Hebrew book (the code checked a non-existent 'sp' column).
        # Observed: 28.19% of Genesis's 32,363 tokens are common/proper
        # nouns (this corpus's 'type_' column).
        _skip_if_ot_missing()
        profile = book_style_profile('Gen', lang='H')
        assert profile['total_tokens'] == 32363
        assert profile['noun_pct'] >= 20.0

    def test_genesis_verbal_pct_is_plausible(self) -> None:
        # Observed: 15.13% of Genesis's tokens are one of the finite/
        # nonfinite verbal 'type_' values (wayyiqtol, qatal, etc.).
        _skip_if_ot_missing()
        profile = book_style_profile('Gen', lang='H')
        assert profile['verbal_pct'] >= 10.0


class TestGreekBookStyleProfile:
    def test_matthew_verbal_pct_is_not_zero(self) -> None:
        # Regression guard: verbal_pct/noun_pct used to be hardcoded to
        # 0.0 for every Greek book (same non-existent 'sp' column check).
        # Observed: 22.26% of Matthew's 18,299 tokens have a non-null
        # 'mood' value (i.e. are a finite or nonfinite verb form).
        _skip_if_nt_missing()
        profile = book_style_profile('Mat', lang='G')
        assert profile['total_tokens'] == 18299
        assert profile['verbal_pct'] >= 15.0

    def test_matthew_noun_pct_is_not_zero(self) -> None:
        # Observed: 46.54% of Matthew's tokens fall in the noun/det/pron
        # 'class_' categories.
        _skip_if_nt_missing()
        profile = book_style_profile('Mat', lang='G')
        assert profile['noun_pct'] >= 30.0


class TestMsttr:
    def test_genesis_msttr_matches_the_profile_value(self) -> None:
        # msttr() is the same computation book_style_profile() embeds as
        # msttr_1k — observed 0.209 for Genesis, window=1000 (default).
        _skip_if_ot_missing()
        assert msttr('Gen', lang='H') == book_style_profile('Gen', lang='H')['msttr_1k']

    def test_matthew_msttr_is_higher_than_genesis(self) -> None:
        # Observed: Mat 0.2904 vs. Gen 0.209 — Matthew's Greek shows
        # higher lexical variety per 1,000-token window than Genesis's
        # Hebrew narrative.
        _skip_if_ot_missing()
        _skip_if_nt_missing()
        assert msttr('Mat', lang='G') > msttr('Gen', lang='H')


class TestStyleComparison:
    def test_deuteronomy_has_higher_ttr_than_genesis(self) -> None:
        # Observed: Deu ttr 0.0615 vs. Gen ttr 0.0543 — Deuteronomy's more
        # varied legal/hortatory vocabulary against Genesis's larger,
        # more repetitive narrative corpus.
        _skip_if_ot_missing()
        df = style_comparison(['Gen', 'Deu'], lang='H')
        assert df.loc['Deu', 'ttr'] > df.loc['Gen', 'ttr']

    def test_romans_has_higher_ttr_and_hina_density_than_matthew(self) -> None:
        # Observed: Rom ttr 0.1487 vs. Mat 0.0913; Rom hina_per1k 4.23 vs.
        # Mat 2.24 — Paul's doctrinal argumentation (ἵνα purpose/result
        # clauses) outpaces Matthew's narrative Greek on both metrics.
        _skip_if_nt_missing()
        df = style_comparison(['Mat', 'Rom'], lang='G')
        assert df.loc['Rom', 'ttr'] > df.loc['Mat', 'ttr']
        assert df.loc['Rom', 'hina_per1k'] > df.loc['Mat', 'hina_per1k']

    def test_unknown_book_is_silently_dropped(self) -> None:
        _skip_if_ot_missing()
        df = style_comparison(['Gen', 'NotARealBook'], lang='H')
        assert list(df.index) == ['Gen']


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_ot_missing()
        _skip_if_nt_missing()
        fns = (
            lambda: print_style_profile('Gen', lang='H'),
            lambda: print_style_profile('Mat', lang='G'),
            lambda: print_style_comparison(['Gen', 'Deu'], lang='H'),
            lambda: print_style_comparison(['Mat', 'Rom'], lang='G'),
        )
        for fn in fns:
            capsys.readouterr()
            fn()
            out = capsys.readouterr().out
            assert len(out.strip()) > 30, f"{fn} produced no real output"

    def test_print_profile_handles_unknown_book_gracefully(self, capsys) -> None:
        _skip_if_ot_missing()
        print_style_profile('NotARealBook', lang='H')
        out = capsys.readouterr().out
        assert 'No data' in out


class TestChartFunctions:
    def test_chart_functions_produce_real_pngs(self, tmp_path, monkeypatch) -> None:
        _skip_if_ot_missing()
        _skip_if_nt_missing()
        monkeypatch.setattr(_mod, '_CHART_DIR', tmp_path)
        out1 = style_radar_chart(['Gen', 'Deu'], lang='H')
        assert out1 is not None
        assert Path(out1).exists()
        assert Path(out1).stat().st_size > 0

        out2 = style_heatmap(['Mat', 'Rom'], lang='G')
        assert out2 is not None
        assert Path(out2).exists()
        assert Path(out2).stat().st_size > 0
