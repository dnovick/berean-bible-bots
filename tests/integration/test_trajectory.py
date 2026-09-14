"""Behavioral tests for bible_grammar.lexical.trajectory (/trajectory),
requiring real corpus data plus the word-level Hebrew<->LXX alignment
(data/processed/word_alignment.parquet, built via scripts/build_word_alignment.py).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.lexical.trajectory import (
    word_trajectory, print_trajectory, trajectory_chart,
    save_trajectory_report, batch_trajectories,
)

_WORD_ALIGNMENT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "word_alignment.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORD_ALIGNMENT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORD_ALIGNMENT_PARQUET}")


class TestWordTrajectory:
    def test_shalom_has_high_continuity_into_the_nt(self) -> None:
        # שָׁלוֹם (peace, H7965) -> εἰρήνη is the paradigm case of strong
        # OT-LXX-NT lexical continuity: same Greek word throughout, at
        # near-100% consistency, carried straight into NT usage.
        # Observed: ot_total 237, lxx_total 223, lxx_consistency 100.0,
        # nt_strongs G1515, nt_total 92, continuity 'high'.
        _skip_if_missing()
        t = word_trajectory('H7965')
        assert t['ot_total'] == 237
        assert t['lxx_primary_g'] == 'G1515'
        assert t['lxx_consistency'] >= 95.0
        assert t['nt_strongs'] == 'G1515'
        assert t['nt_total'] >= 80
        assert t['continuity'] == 'high'


class TestPrintTrajectory:
    def test_prints_real_output(self, capsys) -> None:
        _skip_if_missing()
        print_trajectory('H7965')
        out = capsys.readouterr().out
        assert 'H7965' in out
        assert '237' in out
        assert len(out.strip()) > 200


class TestTrajectoryChart:
    def test_produces_a_real_png(self, tmp_path: Path) -> None:
        _skip_if_missing()
        out = trajectory_chart('H7965', output_path=str(tmp_path / 'traj.png'))
        assert Path(out).exists()
        assert Path(out).stat().st_size > 0


class TestSaveTrajectoryReport:
    def test_writes_a_real_markdown_report_with_chart(self, tmp_path: Path) -> None:
        # Defaults to output/reports/ot/lexicon/ (git-tracked) — always
        # redirect via output_dir in tests.
        _skip_if_missing()
        out = save_trajectory_report('H7965', output_dir=str(tmp_path))
        assert Path(out).exists()
        text = Path(out).read_text(encoding='utf-8')
        assert 'H7965' in text
        assert len(text) > 500
        pngs = list(tmp_path.glob('*.png'))
        assert len(pngs) == 1


class TestBatchTrajectories:
    def test_generates_one_report_per_root(self, tmp_path: Path) -> None:
        _skip_if_missing()
        paths = batch_trajectories(['H7965', 'H2617'], output_dir=str(tmp_path))
        assert len(paths) == 2
        for p in paths:
            assert Path(p).exists()
            assert Path(p).stat().st_size > 0
