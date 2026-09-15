"""Behavioral tests for bible_grammar.verbal_syntax.verb_forms, requiring
real corpus data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #676, Phase 3).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.verbal_syntax.verb_forms import (
    verb_form_profile, print_verb_form_profile, verb_form_chart,
    wayyiqtol_chains, print_wayyiqtol_chains,
    stem_distribution, print_stem_distribution, stem_chart,
    aspect_comparison, print_aspect_comparison, aspect_comparison_chart,
    GENRE_SETS,
)
from bible_grammar.core._utils import load_ot_data

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestVerbFormProfile:
    def test_genesis_1_is_wayyiqtol_dominant(self) -> None:
        # Observed: Genesis 1 has 50 wayyiqtol tokens (49.5%), the classic
        # narrative-chain signature of Hebrew prose.
        _skip_if_missing()
        df = verb_form_profile('Gen', 1)
        top = df.iloc[df['pct'].idxmax()]
        assert top['form'] == 'wayyiqtol'
        assert top['pct'] >= 40.0


class TestGenreSets:
    def test_every_genre_sets_book_code_matches_real_data(self) -> None:
        # Regression guard: GENRE_SETS previously used SBL-style
        # abbreviations (e.g. 'Exod', '1Sam') that didn't match this
        # corpus's real book_id values ('Exo', '1Sa'), so
        # aspect_comparison(GENRE_SETS['narrative']) silently returned
        # near-zero results for 12 of 16 books. All codes now verified.
        _skip_if_missing()
        df = load_ot_data()
        real_books = set(df['book_id' if 'book_id' in df.columns else 'book'].unique())
        for genre, books in GENRE_SETS.items():
            bad = [b for b in books if b not in real_books]
            assert not bad, f"{genre} has invalid book codes: {bad}"


class TestWayyiqtolChains:
    def test_genesis_1_has_real_chains(self) -> None:
        # Observed: Genesis 1 has 15 wayyiqtol chains of length >= 2.
        _skip_if_missing()
        chains = wayyiqtol_chains('Gen', 1)
        assert len(chains) >= 10
        assert all(c['length'] >= 2 for c in chains)

    def test_chain_break_types_are_classified(self) -> None:
        _skip_if_missing()
        chains = wayyiqtol_chains('Gen', 1)
        break_types = {c['break_type'] for c in chains}
        assert 'modal/jussive (speech or wish)' in break_types


class TestStemDistribution:
    def test_genesis_qal_dominates(self) -> None:
        # Observed: Genesis Qal 3,855 tokens (76.5%), far ahead of any
        # other stem.
        _skip_if_missing()
        df = stem_distribution('Gen')
        top = df.iloc[0]
        assert top['stem'] == 'qal'
        assert top['pct'] >= 70.0


class TestAspectComparison:
    def test_narrative_genre_set_has_real_data(self) -> None:
        # Regression guard for the GENRE_SETS fix: aspect_comparison
        # should return substantial real counts across the whole narrative
        # genre set, not near-zero from mismatched book codes.
        _skip_if_missing()
        df = aspect_comparison(GENRE_SETS['narrative'])
        total = sum(
            df[(b, 'count')].sum() for b in GENRE_SETS['narrative']
            if (b, 'count') in df.columns
        )
        assert total >= 30000


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            lambda: print_verb_form_profile('Gen', 1),
            lambda: print_wayyiqtol_chains('Gen', 1),
            lambda: print_stem_distribution('Gen'),
            lambda: print_aspect_comparison(['Gen', 'Psa']),
        )
        for fn in fns:
            capsys.readouterr()
            fn()
            out = capsys.readouterr().out
            assert len(out.strip()) > 30, f"{fn} produced no real output"


class TestChartFunctions:
    def test_chart_functions_produce_real_pngs(self, tmp_path: Path) -> None:
        _skip_if_missing()
        out1 = verb_form_chart('Gen', 1, output_path=str(tmp_path / 'verb_form.png'))
        out2 = stem_chart('Gen', output_path=str(tmp_path / 'stem.png'))
        out3 = aspect_comparison_chart(
            ['Gen', 'Psa'], output_path=str(tmp_path / 'aspect.png'))
        for out in (out1, out2, out3):
            assert out is not None
            assert Path(out).exists()
            assert Path(out).stat().st_size > 0
