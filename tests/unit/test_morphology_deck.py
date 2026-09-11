"""Tests for bible_grammar.morphology_deck — pure logic, no I/O beyond
writing to a tmp_path (no corpus data dependency at all: this module just
formats a caller-supplied list of DeckCard objects into three flashcard
file formats). Per docs/policies/test-coverage.md's priority plan
(issue #662, item 4).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.morphology_deck import DeckCard, DeckConfig, MorphologyDeckWriter


def _sample_cards() -> list[DeckCard]:
    return [
        DeckCard(
            num=1, front="קָטַל", ref="Gen 1:1", root="קטל", stem="Qal",
            conj="Perfect", pgn="3ms", gloss="he killed", section="PERFECT",
            tag="qal-perfect", back_txt="Qal Perfect 3ms — he killed",
            back_fd="Qal|Perfect|3ms|he killed",
        ),
        DeckCard(
            num=2, front="קָטְלָה", ref="Gen 1:2", root="קטל", stem="Qal",
            conj="Perfect", pgn="3fs", gloss="she killed", section="PERFECT",
            tag="qal-perfect", back_txt="Qal Perfect 3fs — she killed",
            back_fd="Qal|Perfect|3fs|she killed",
        ),
    ]


def _sample_config() -> DeckConfig:
    return DeckConfig(
        chapter=13,
        stem="Qal",
        quality="Strong",
        deck_name="BBH Chapter 13 — Qal Strong",
        description="Test deck description.",
        diagnostics=[("קָטַל", "Qal Perfect 3ms")],
        coverage=[{"conj": "Perfect", "detail": "קטל", "cards": 2}],
    )


class TestMorphologyDeckWriter:
    def test_write_all_produces_all_three_files(self, tmp_path: Path) -> None:
        writer = MorphologyDeckWriter(_sample_config(), _sample_cards())
        writer.write_all(tmp_path, "ch13-morphology-deck")

        md = tmp_path / "ch13-morphology-deck.md"
        txt = tmp_path / "ch13-morphology-deck.txt"
        fd = tmp_path / "ch13-morphology-deck-fd.txt"
        assert md.exists()
        assert txt.exists()
        assert fd.exists()

    def test_md_contains_chapter_header_and_cards(self, tmp_path: Path) -> None:
        writer = MorphologyDeckWriter(_sample_config(), _sample_cards())
        writer.write_all(tmp_path, "ch13-morphology-deck")
        content = (tmp_path / "ch13-morphology-deck.md").read_text()
        assert "Chapter 13" in content
        assert "קָטַל" in content
        assert "he killed" in content

    def test_txt_has_anki_import_headers(self, tmp_path: Path) -> None:
        writer = MorphologyDeckWriter(_sample_config(), _sample_cards())
        writer.write_all(tmp_path, "ch13-morphology-deck")
        content = (tmp_path / "ch13-morphology-deck.txt").read_text()
        assert "#separator:tab" in content
        assert "#deck:BBH Chapter 13 — Qal Strong" in content
        # front(ref)\tback\ttag — tab-separated, one row per card
        assert "קָטַל (Gen 1:1)\tQal Perfect 3ms — he killed\tqal-perfect" in content

    def test_fd_uses_deck_name_as_tag_column(self, tmp_path: Path) -> None:
        writer = MorphologyDeckWriter(_sample_config(), _sample_cards())
        writer.write_all(tmp_path, "ch13-morphology-deck")
        content = (tmp_path / "ch13-morphology-deck-fd.txt").read_text()
        assert "Qal|Perfect|3ms|he killed\tBBH Chapter 13 — Qal Strong" in content

    def test_grouped_preserves_section_order_and_membership(self) -> None:
        cards = _sample_cards() + [
            DeckCard(
                num=3, front="נִקְטַל", ref="paradigm", root="קטל", stem="Niphal",
                conj="Perfect", pgn="3ms", gloss="he was killed",
                section="NIPHAL", tag="niphal-perfect",
                back_txt="Niphal Perfect 3ms", back_fd="Niphal|Perfect|3ms",
            ),
        ]
        writer = MorphologyDeckWriter(_sample_config(), cards)
        grouped = writer._grouped()
        sections = [s for s, _ in grouped]
        assert sections == ["PERFECT", "NIPHAL"]
        assert len(grouped[0][1]) == 2
        assert len(grouped[1][1]) == 1
