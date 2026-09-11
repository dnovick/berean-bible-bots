"""Tests for scripts/build_psalm119_memorization.py's pure helpers, plus a
real behavioral check of load_stanzas() against the actual
data/studies/psalm-119/psalm-119-text.yaml. Per docs/policies/test-coverage.md's
priority plan (issue #676, Phase 2).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import build_psalm119_memorization as bpm  # noqa: E402

_DATA_YAML = bpm.DATA_YAML


class TestMakeSlug:
    def test_combines_zero_padded_number_and_ascii_name(self) -> None:
        assert bpm.make_slug({"num": 1, "name": "Alef"}) == "01-alef"

    def test_two_digit_number(self) -> None:
        assert bpm.make_slug({"num": 22, "name": "Taw"}) == "22-taw"


class TestBlankKeyWord:
    def test_blanks_the_key_word_preserving_maqqef(self) -> None:
        result = bpm.blank_key_word("אֶת־תּוֹרַת יְהוָה", "תּוֹרַת")
        assert result == "אֶת־______ יְהוָה"

    def test_word_not_present_returns_text_unchanged(self) -> None:
        text = "אַשְׁרֵי תְמִימֵי דָרֶךְ"
        assert bpm.blank_key_word(text, "לֹא־קַיָּם") == text


class TestSafeHtml:
    def test_escapes_html_special_characters(self) -> None:
        result = bpm.safe_html('<script>alert(1)</script> & "quotes"')
        assert "<script>" not in result
        assert "&lt;script&gt;" in result
        assert "&amp;" in result
        assert "&quot;quotes&quot;" in result


class TestSortByPosition:
    def test_orders_pairs_by_their_position_in_text(self) -> None:
        text = "אחת שתים שלוש"
        pairs = [("שלוש", "three"), ("אחת", "one"), ("שתים", "two")]
        ordered = bpm._sort_by_position(pairs, text)
        assert [w for w, _ in ordered] == ["אחת", "שתים", "שלוש"]


class TestLoadStanzasBehavioral:
    def test_all_22_acrostic_stanzas_present(self) -> None:
        # Psalm 119's acrostic structure has exactly 22 stanzas, one per
        # Hebrew letter. Observed: stanza 1 is Alef (א).
        if not _DATA_YAML.exists():
            pytest.skip(f"Data file not found: {_DATA_YAML}")
        stanzas = bpm.load_stanzas()
        assert len(stanzas) == 22
        assert stanzas[0]["name"] == "Alef"
        assert stanzas[0]["letter"] == "א"
