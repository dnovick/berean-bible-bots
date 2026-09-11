"""Tests for scripts/build_bbh_decks.py's pure card-flattening and
rendering functions. Per docs/policies/test-coverage.md's priority plan
(issue #676, Phase 2).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import build_bbh_decks as bbd  # noqa: E402

_SAMPLE_DECK = {
    "deck": {"title": "Test Deck", "description": "A test.", "id": "test-deck"},
    "groups": [
        {"name": "Group A", "tag": "group-a", "cards": [
            {"front": "א", "back": "Alef", "tags": []},
        ]},
    ],
}


class TestAllCards:
    def test_injects_group_tag_into_each_card(self) -> None:
        cards = bbd._all_cards(_SAMPLE_DECK)
        assert cards == [{"front": "א", "back": "Alef", "tags": ["group-a"]}]

    def test_does_not_duplicate_an_already_present_group_tag(self) -> None:
        deck = {"groups": [{"name": "G", "tag": "g", "cards": [
            {"front": "x", "back": "y", "tags": ["g"]},
        ]}]}
        cards = bbd._all_cards(deck)
        assert cards[0]["tags"] == ["g"]


class TestRenderMd:
    def test_includes_title_description_and_card_table(self) -> None:
        md = bbd.render_md(_SAMPLE_DECK)
        assert md.startswith("# Test Deck")
        assert "*A test.*" in md
        assert "test-deck.txt" in md
        assert "## Group A" in md
        assert "| 1 | א | Alef |" in md

    def test_escapes_pipe_characters_in_back_field(self) -> None:
        deck = {
            "deck": {"title": "T", "description": "d", "id": "t"},
            "groups": [{"name": "G", "cards": [
                {"front": "x", "back": "a | b"},
            ]}],
        }
        md = bbd.render_md(deck)
        assert "a \\| b" in md
