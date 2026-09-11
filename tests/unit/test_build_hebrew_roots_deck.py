"""Tests for scripts/build_hebrew_roots_deck.py's pure helpers. Per
docs/policies/test-coverage.md's priority plan (issue #676, Phase 2).
"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import build_hebrew_roots_deck as bhr  # noqa: E402


class TestNid:
    def test_pads_short_id_to_four_digits(self) -> None:
        assert bhr.nid("H6") == "H0006"

    def test_strips_variant_letter_suffix(self) -> None:
        assert bhr.nid("H0430G") == "H0430"

    def test_non_strongs_string_passed_through(self) -> None:
        assert bhr.nid("not-a-strongs") == "not-a-strongs"


class TestStripVowels:
    def test_keeps_only_consonants(self) -> None:
        assert bhr.strip_vowels("בְּרֵאשִׁית") == "בראשית"

    def test_non_hebrew_text_becomes_empty(self) -> None:
        assert bhr.strip_vowels("hello 123") == ""


class TestExtractGloss:
    def test_extracts_def_element_text(self) -> None:
        xml_str = f'<entry xmlns="{bhr.NS}"><meaning><def>to create</def></meaning></entry>'
        el = ET.fromstring(xml_str)
        assert bhr.extract_gloss(el) == "to create"

    def test_falls_back_to_usage_when_no_meaning(self) -> None:
        xml_str = f'<entry xmlns="{bhr.NS}"><usage>used of creation</usage></entry>'
        el = ET.fromstring(xml_str)
        assert bhr.extract_gloss(el) == "used of creation"

    def test_empty_entry_returns_empty_string(self) -> None:
        xml_str = f'<entry xmlns="{bhr.NS}"></entry>'
        el = ET.fromstring(xml_str)
        assert bhr.extract_gloss(el) == ""
