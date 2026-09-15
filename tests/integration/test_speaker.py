"""Behavioral tests for bible_grammar.discourse.speaker, requiring real
corpus data — data/processed/macula_syntax.parquet (MACULA NT subjref
links).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.discourse.speaker import (
    jesus_speaking_verse_set, is_jesus_speaking, filter_to_jesus_speech,
    ALLOWLIST_VERSES,
)

_MACULA_NT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_NT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_NT_PARQUET}")


class TestJesusSpeakingVerseSet:
    def test_matthew_has_real_speech_introducing_verses(self) -> None:
        # jesus_speaking_verse_set() flags verses where a speech verb has
        # Jesus as its grammatical subject — the *introducing* verse of a
        # discourse, not every verse of the discourse content. Observed:
        # Matthew has 147 such verses, including the Sermon on the
        # Mount's introduction (Mat 5:2, "he opened his mouth ... saying").
        _skip_if_missing()
        s = jesus_speaking_verse_set(books=['Mat'])
        assert len(s) >= 100
        assert ('Mat', 5, 2) in s


class TestIsJesusSpeaking:
    def test_sermon_on_the_mount_introduction_is_true(self) -> None:
        # Mat 5:2 contains the actual speech-introducing verb.
        _skip_if_missing()
        assert is_jesus_speaking('Mat', 5, 2) is True

    def test_beatitude_content_verse_is_false(self) -> None:
        # Mat 5:3 (a Beatitude) is speech CONTENT within the same
        # discourse, but contains no speech-introducing verb of its own —
        # the MACULA subjref detector correctly does not flag it, since
        # it operates per-verse, not per-discourse-block.
        _skip_if_missing()
        assert is_jesus_speaking('Mat', 5, 3) is False

    def test_narrator_genealogy_verse_is_false(self) -> None:
        _skip_if_missing()
        assert is_jesus_speaking('Mat', 1, 1) is False

    def test_allowlist_title_overrides_subjref_detection(self) -> None:
        # The 'Bridegroom' allowlist marks Mat 9:15 even though it's an
        # indirect/parabolic reference, not a first-person speech-intro
        # verb with Jesus as subjref.
        _skip_if_missing()
        assert is_jesus_speaking('Mat', 9, 15, title='Bridegroom') is True


class TestFilterToJesusSpeech:
    def test_allowlist_title_filters_correctly(self) -> None:
        _skip_if_missing()
        candidates = list(ALLOWLIST_VERSES['Bridegroom']) + [('Jhn', 3, 29)]
        result = filter_to_jesus_speech(candidates, title='Bridegroom')
        assert set(result) == ALLOWLIST_VERSES['Bridegroom']
        assert ('Jhn', 3, 29) not in result
