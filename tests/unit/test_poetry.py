"""Tests for bible_grammar.poetry — pure-logic helpers, plus behavioral tests
against real corpus data (marked `integration`, requires data/processed/)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot.poetry import _jaccard, detect_acrostic, acrostic_known

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


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


@pytest.mark.integration
class TestDetectAcrosticBehavioral:
    """Psalm 119 is the canonical acrostic: 22 stanzas of 8 verses, each
    stanza's 8 verses all starting with that stanza's Hebrew letter in
    alphabetic order. Verified live before writing these assertions:
    detect_acrostic('Psa', 119, 1, 176, stanza_size=8) returns a perfect
    176/176 match with zero mismatches."""

    def test_psalm_119_is_full_acrostic_at_stanza_size_8(self) -> None:
        _skip_if_missing()
        result = detect_acrostic('Psa', 119, 1, 176, stanza_size=8)
        assert result['is_acrostic'] is True
        assert result['pattern'] == 'full'
        assert result['pct_match'] >= 99.0
        assert result['match_count'] == result['total'] == 176

    def test_psalm_119_first_stanza_is_alef(self) -> None:
        _skip_if_missing()
        result = detect_acrostic('Psa', 119, 1, 176, stanza_size=8)
        first_stanza = result['hits'][:8]
        assert all(h['expected'] == 'א' for h in first_stanza)
        assert all(h['match'] for h in first_stanza)

    def test_psalm_119_wrong_stanza_size_is_not_detected_as_acrostic(self) -> None:
        # Sanity check on the *shape* of the pattern: treating Ps 119 as a
        # one-letter-per-verse acrostic (the default stanza_size=1) is wrong
        # — its real structure is 8 verses per letter — and should NOT read
        # as a full acrostic. Guards against a future change silently making
        # detect_acrostic over-eager (e.g. matching on the alef prefix alone).
        _skip_if_missing()
        result = detect_acrostic('Psa', 119, 1, 176, stanza_size=1)
        assert result['is_acrostic'] is False

    def test_acrostic_known_includes_psalm_119(self) -> None:
        _skip_if_missing()
        assert 119 in acrostic_known('Psa')
