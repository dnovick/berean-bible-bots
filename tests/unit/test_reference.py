"""Tests for bible_grammar.reference — pure static data, no I/O."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.core.reference import (
    book_info, all_book_ids, book_ids_for_group,
    BOOKS, TORAH, PROPHETS, WRITINGS, GOSPELS, PAULINE,
)


class TestBookInfo:
    def test_genesis(self) -> None:
        info = book_info("Gen")
        assert info["name"] == "Genesis"
        assert info["testament"] == "OT"
        assert info["canonical_order"] == 1
        assert info["chapter_count"] == 50

    def test_revelation(self) -> None:
        info = book_info("Rev")
        assert info["name"] == "Revelation"
        assert info["testament"] == "NT"
        assert info["canonical_order"] == 66
        assert info["chapter_count"] == 22

    def test_psalms(self) -> None:
        info = book_info("Psa")
        assert info["chapter_count"] == 150

    def test_unknown_raises(self) -> None:
        with pytest.raises(KeyError):
            book_info("Xyz")


class TestAllBookIds:
    def test_all_count(self) -> None:
        ids = all_book_ids()
        assert len(ids) == 66

    def test_ot_count(self) -> None:
        ot = all_book_ids("OT")
        assert len(ot) == 39

    def test_nt_count(self) -> None:
        nt = all_book_ids("NT")
        assert len(nt) == 27

    def test_ot_starts_with_gen(self) -> None:
        ot = all_book_ids("OT")
        assert ot[0] == "Gen"

    def test_nt_starts_with_mat(self) -> None:
        nt = all_book_ids("NT")
        assert nt[0] == "Mat"

    def test_canonical_order_preserved(self) -> None:
        ids = all_book_ids()
        gen_idx = ids.index("Gen")
        rev_idx = ids.index("Rev")
        assert gen_idx < rev_idx


class TestBookIdsForGroup:
    def test_torah_count(self) -> None:
        ids = book_ids_for_group("torah")
        assert len(ids) == 5
        assert set(ids) == TORAH

    def test_pentateuch_alias(self) -> None:
        assert book_ids_for_group("pentateuch") == book_ids_for_group("torah")

    def test_torah_canonical_order(self) -> None:
        ids = book_ids_for_group("torah")
        assert ids == ["Gen", "Exo", "Lev", "Num", "Deu"]

    def test_gospels_count(self) -> None:
        ids = book_ids_for_group("gospels")
        assert len(ids) == 4
        assert set(ids) == GOSPELS

    def test_pauline_count(self) -> None:
        ids = book_ids_for_group("pauline")
        assert len(ids) == 13

    def test_unknown_raises(self) -> None:
        with pytest.raises(ValueError):
            book_ids_for_group("deuterocanon")

    def test_case_insensitive(self) -> None:
        assert book_ids_for_group("TORAH") == book_ids_for_group("torah")


class TestGroupSets:
    def test_no_overlap_torah_prophets(self) -> None:
        assert TORAH & PROPHETS == set()

    def test_no_overlap_torah_writings(self) -> None:
        assert TORAH & WRITINGS == set()

    def test_all_ot_books_in_some_group(self) -> None:
        grouped = TORAH | PROPHETS | WRITINGS
        # Historical books (Jos, Jdg, 1-2Sa, 1-2Ki) are not in any named group
        ot_ids = set(all_book_ids("OT"))
        ungrouped = ot_ids - grouped
        # Verify the ungrouped set contains only the expected historical books
        assert "Gen" not in ungrouped    # Torah
        assert "Isa" not in ungrouped    # Prophets
        assert "Psa" not in ungrouped    # Writings
        assert "Jos" in ungrouped        # Historical — intentionally ungrouped
        assert "1Sa" in ungrouped
        assert "1Ki" in ungrouped

    def test_nt_groups_non_overlapping(self) -> None:
        assert GOSPELS & PAULINE == set()
