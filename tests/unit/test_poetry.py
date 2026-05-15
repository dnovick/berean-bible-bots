"""Tests for bible_grammar.poetry helper functions — pure logic, no I/O."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot.poetry import _jaccard


class TestJaccard:
    def test_identical_sets(self) -> None:
        assert _jaccard({1, 2, 3}, {1, 2, 3}) == 1.0

    def test_disjoint_sets(self) -> None:
        assert _jaccard({1, 2}, {3, 4}) == 0.0

    def test_partial_overlap(self) -> None:
        # |{1,2} ∩ {2,3}| / |{1,2} ∪ {2,3}| = 1/3
        result = _jaccard({1, 2}, {2, 3})
        assert abs(result - 1 / 3) < 1e-9

    def test_one_empty(self) -> None:
        assert _jaccard(set(), {1, 2}) == 0.0

    def test_both_empty(self) -> None:
        assert _jaccard(set(), set()) == 0.0

    def test_frozenset_input(self) -> None:
        a = frozenset(["שָׁלוֹם", "טוֹב"])
        b = frozenset(["שָׁלוֹם", "רָע"])
        result = _jaccard(a, b)
        assert abs(result - 1 / 3) < 1e-9

    def test_single_element_match(self) -> None:
        assert _jaccard({"x"}, {"x"}) == 1.0

    def test_symmetric(self) -> None:
        a = {1, 2, 3}
        b = {2, 3, 4, 5}
        assert _jaccard(a, b) == _jaccard(b, a)

    def test_subset(self) -> None:
        # |{1,2} ∩ {1,2,3}| / |{1,2,3}| = 2/3
        result = _jaccard({1, 2}, {1, 2, 3})
        assert abs(result - 2 / 3) < 1e-9

    def test_string_elements(self) -> None:
        a = {"heaven", "earth", "day"}
        b = {"earth", "sea", "night"}
        # intersection: {earth}, union: 5 items
        result = _jaccard(a, b)
        assert abs(result - 1 / 5) < 1e-9
