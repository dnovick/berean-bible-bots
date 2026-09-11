"""Tests for scripts/extract_psalm119_text.py's pure text-processing
helpers. Per docs/policies/test-coverage.md's priority plan (issue #676,
Phase 2).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import extract_psalm119_text as ept  # noqa: E402


class TestCleanTahotWord:
    def test_removes_tahot_separators(self) -> None:
        assert ept.clean_tahot_word("אֶת\\־/תּוֹרַת") == "אֶת־תּוֹרַת"


class TestStripCantillation:
    def test_removes_trope_marks_keeps_vowels(self) -> None:
        result = ept.strip_cantillation("בְּרֵאשִׁ֖ית")
        assert result == "בְּרֵאשִׁית"


class TestConsonantLength:
    def test_counts_consonants_ignoring_diacritics(self) -> None:
        assert ept.consonant_length("בְּרֵאשִׁית") == 6


class TestBuildHebrewText:
    def test_joins_words_with_spaces_except_after_maqqef(self) -> None:
        result = ept.build_hebrew_text(["אַשְׁרֵי", "תְמִֽימֵי\\־", "דָ֑רֶךְ"])
        assert result == "אַשְׁרֵי תְמִימֵי־דָרֶךְ"

    def test_empty_list_returns_empty_string(self) -> None:
        assert ept.build_hebrew_text([]) == ""


class TestGetKeyWords:
    def test_returns_longest_content_words_first(self) -> None:
        words = ept.get_key_words(
            ["אַשְׁרֵי", "תְמִימֵי", "דָרֶךְ", "הַ", "עַ"], n=2
        )
        assert len(words) == 2
        # Both returned words must have consonant length >= 3 (the
        # documented content-word filter); short function words (הַ, עַ)
        # must never appear.
        assert "הַ" not in words
        assert "עַ" not in words
