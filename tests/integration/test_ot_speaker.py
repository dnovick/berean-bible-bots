"""Behavioral tests for bible_grammar.ot.ot_speaker (/ot-speaker), requiring
real corpus data — data/processed/.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot.ot_speaker import speaker_verses, who_speaks

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestSpeakerVerses:
    def test_yhwh_elohim_speaks_repeatedly_in_isaiah(self) -> None:
        _skip_if_missing()
        df = speaker_verses(['H3068', 'H0430'], books=['Isa'])
        assert len(df) > 0
        assert df['count'].sum() >= 30   # observed: 37 total rows/occurrences


class TestWhoSpeaks:
    def test_job_is_the_dominant_speaker_in_job(self) -> None:
        # Job (H0347) speaks far more than any other character in his own
        # book — the dialogue's central voice. Observed: 47 verb tokens,
        # nearly 5x the second-place speaker (Elihu, 10).
        _skip_if_missing()
        df = who_speaks('Job', top_n=10)
        top = df.iloc[0]
        assert top['speaker_strong'] == 'H347'
        assert top['verb_count'] >= 40

    def test_god_appears_among_job_speakers(self) -> None:
        # God's speeches (Job 38-41) should register even though Job
        # himself dominates the raw count.
        _skip_if_missing()
        df = who_speaks('Job', top_n=20)
        assert (df['speaker_strong'] == 'H3068').any() or (df['speaker_strong'] == 'H430').any()
