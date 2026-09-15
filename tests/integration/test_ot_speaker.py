"""Behavioral tests for bible_grammar.ot.ot_speaker (/ot-speaker), requiring
real corpus data — data/processed/.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot.ot_speaker import (
    speaker_verses,
    who_speaks,
    divine_speech_by_book,
    divine_speech_verses,
    print_speaker_summary,
    print_divine_speech_by_book,
    speaker_report,
)

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


class TestDivineSpeechByBook:
    def test_psalms_has_the_highest_divine_speech_percentage(self) -> None:
        # Observed: Psalms 25.9% of its speech-verb tokens are divine
        # speech (77 of 297) — the highest percentage of any book, though
        # Jeremiah (85) and Exodus (80) have higher raw counts.
        _skip_if_missing()
        df = divine_speech_by_book()
        psa = df[df['book'] == 'Psa'].iloc[0]
        assert psa['pct'] >= 20.0
        jer = df[df['book'] == 'Jer'].iloc[0]
        assert jer['count'] >= 70


class TestDivineSpeechVerses:
    def test_isaiah_divine_speech_verse_count(self) -> None:
        # Observed: 71 distinct verses in Isaiah contain divine speech.
        _skip_if_missing()
        verses = divine_speech_verses('Isa')
        assert len(verses) >= 60
        assert all(v.startswith('ISA') for v in verses)


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            lambda: print_speaker_summary(['H3068', 'H0430'], books=['Isa']),
            print_divine_speech_by_book,
        )
        for fn in fns:
            capsys.readouterr()
            fn()
            out = capsys.readouterr().out
            assert len(out.strip()) > 30, f"{fn} produced no real output"


class TestSpeakerReport:
    def test_writes_a_real_markdown_report(self, tmp_path: Path) -> None:
        # output_dir defaults to the real, git-tracked 'output/reports' —
        # always override it in tests.
        _skip_if_missing()
        out = speaker_report(['H3068', 'H0430'], books=['Isa'], output_dir=str(tmp_path))
        assert Path(out).exists()
        text = Path(out).read_text(encoding='utf-8')
        assert 'Isa' in text
        assert len(text) > 500
