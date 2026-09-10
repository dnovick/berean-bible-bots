"""Behavioral tests for bible_grammar.ot.cantillation, requiring real corpus
data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot.cantillation import parse_verse

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestParseVerse:
    def test_genesis_1_1_athnach_falls_on_elohim(self) -> None:
        # Genesis 1:1's Athnach (the primary H2 verse divider) famously
        # falls on אֱלֹהִים, splitting "In the beginning God created" from
        # "the heavens and the earth" — real, well-known Masoretic
        # cantillation, not an invented fact.
        _skip_if_missing()
        node = parse_verse('Gen', 1, 1)
        assert node.accent == 'SOP'
        assert len(node.children) == 2

        ath_subtree, sil_subtree = node.children
        assert ath_subtree.accent == 'ATH'
        assert sil_subtree.accent == 'SIL'

        ath_words = [w.text for w in ath_subtree.words]
        assert any('אֱלֹהִ' in w for w in ath_words)
