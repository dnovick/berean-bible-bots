"""Behavioral tests for bible_grammar.ot.ot_discourse, requiring real corpus
data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot import ot_discourse as _mod
from bible_grammar.ot.ot_discourse import (
    ot_discourse_wayyiqtol_density,
    ot_discourse_speech_density,
    ot_discourse_lexical_diversity,
    ot_discourse_peak_score,
    ot_discourse_episode_boundaries,
    ot_discourse_narrative_profile,
    print_ot_discourse_overview,
    print_ot_wayyiqtol_density,
    print_ot_speech_density,
    print_ot_peak_score,
    print_ot_episode_boundaries,
    ot_discourse_density_chart,
    ot_discourse_peak_chart,
)

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestWayyiqtolDensity:
    def test_genesis_has_50_chapters_and_real_wayyiqtol_counts(self) -> None:
        # Observed: 50 chapters, 2,105 total wayyiqtol tokens across the book.
        _skip_if_missing()
        df = ot_discourse_wayyiqtol_density('Gen')
        assert len(df) == 50
        assert df['wayyiqtol_count'].sum() >= 2000
        assert (df['density'] >= 0).all()
        assert (df['density'] <= 100).all()


class TestSpeechDensity:
    def test_genesis_speech_verb_total(self) -> None:
        # Observed: 720 speech-verb tokens (אָמַר/דָּבַר/נָאַם/קָרָא) across
        # Genesis's 50 chapters.
        _skip_if_missing()
        df = ot_discourse_speech_density('Gen')
        assert len(df) == 50
        assert df['speech_count'].sum() >= 650


class TestLexicalDiversity:
    def test_genesis_ttr_is_in_a_plausible_range(self) -> None:
        # Observed: mean TTR across Genesis's 50 chapters is ~0.242 —
        # narrative prose reuses vocabulary heavily (low TTR), unlike
        # poetry's typically higher lexical diversity.
        _skip_if_missing()
        df = ot_discourse_lexical_diversity('Gen')
        assert len(df) == 50
        assert 0.1 <= df['ttr'].mean() <= 0.4


class TestPeakScore:
    def test_genesis_38_is_the_narrative_peak(self) -> None:
        # Observed: Genesis 38 (Judah and Tamar) scores highest (0.739) —
        # a dense, self-contained dramatic episode.
        _skip_if_missing()
        df = ot_discourse_peak_score('Gen')
        top = df.loc[df['peak_score'].idxmax()]
        assert int(top['chapter']) == 38
        assert top['peak_score'] >= 0.6


class TestEpisodeBoundaries:
    def test_wayehi_scene_setters_dominate_genesis_boundaries(self) -> None:
        # Observed: 50 total boundaries in Genesis, 44 of them the wayehi
        # ("and it came to pass") scene-setting formula.
        _skip_if_missing()
        df = ot_discourse_episode_boundaries('Gen')
        assert len(df) >= 40
        counts = df['boundary_type'].value_counts()
        assert counts.get('scene-setter (wayehi)', 0) >= 40


class TestNarrativeProfile:
    def test_genesis_profile_matches_peak_score(self) -> None:
        # ot_discourse_narrative_profile is a summary wrapper — its peak
        # chapter/score must agree with ot_discourse_peak_score directly.
        _skip_if_missing()
        profile = ot_discourse_narrative_profile('Gen')
        assert profile['total_tokens'] == 32363
        assert profile['peak_chapter'] == 38
        assert profile['wayyiqtol_total'] == 2105


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            lambda: print_ot_discourse_overview('Gen'),
            lambda: print_ot_wayyiqtol_density('Gen'),
            lambda: print_ot_speech_density('Gen'),
            lambda: print_ot_peak_score('Gen'),
            lambda: print_ot_episode_boundaries('Gen'),
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
        for fn in (ot_discourse_density_chart, ot_discourse_peak_chart):
            out = fn('Gen')
            assert out is not None, f"{fn.__name__} returned None"
            assert Path(out).exists(), f"{fn.__name__} did not write a file"
            assert Path(out).stat().st_size > 0
