"""Tests for each stem module's gloss-keyword semantic classifier
(_qal_semantic_fn, _niphal_semantic_fn, etc.) — pure logic, no I/O. Per
docs/policies/test-coverage.md's priority plan (issue #662, item 4): these
were the one genuinely stem-specific piece of logic in each module (the
rest delegates to the shared StemAnalysis engine, already covered by
test_stem_analysis.py).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.stems.qal import _qal_semantic_fn
from bible_grammar.stems.niphal import _niphal_semantic_fn
from bible_grammar.stems.piel import _piel_semantic_fn
from bible_grammar.stems.pual import _pual_semantic_fn
from bible_grammar.stems.hophal import _hophal_semantic_fn
from bible_grammar.stems.hithpael import _hithpael_semantic_fn


class TestQalSemanticFn:
    def test_speech_gloss(self) -> None:
        assert _qal_semantic_fn('said') == 'speech / communication'

    def test_motion_gloss(self) -> None:
        assert _qal_semantic_fn('went') == 'motion / movement'

    def test_stative_gloss(self) -> None:
        assert _qal_semantic_fn('was heavy') == 'stative / condition'

    def test_creation_worship_gloss(self) -> None:
        assert _qal_semantic_fn('created') == 'creation / worship'

    def test_unmatched_gloss_falls_back_to_other(self) -> None:
        assert _qal_semantic_fn('xyzzy-not-a-real-verb') == 'other action'


class TestNiphalSemanticFn:
    def test_reciprocal_gloss(self) -> None:
        assert _niphal_semantic_fn('met each other') == 'reciprocal'

    def test_reflexive_gloss(self) -> None:
        assert _niphal_semantic_fn('hide himself') == 'reflexive'

    def test_passive_gloss(self) -> None:
        assert _niphal_semantic_fn('was given') == 'passive'

    def test_unmatched_gloss_falls_back_to_other(self) -> None:
        assert _niphal_semantic_fn('xyzzy-not-a-real-verb') == 'other'


class TestPielSemanticFn:
    def test_declarative_gloss(self) -> None:
        assert _piel_semantic_fn('declared righteous') == 'declarative'

    def test_factitive_gloss(self) -> None:
        assert _piel_semantic_fn('sanctified') == 'factitive'

    def test_intensive_gloss(self) -> None:
        assert _piel_semantic_fn('shattered') == 'intensive'

    def test_unmatched_gloss_falls_back_to_other(self) -> None:
        assert _piel_semantic_fn('xyzzy-not-a-real-verb') == 'other'


class TestPualSemanticFn:
    def test_birth_gloss(self) -> None:
        assert _pual_semantic_fn('was born') == 'passive (birth)'

    def test_passive_intensive_gloss(self) -> None:
        assert _pual_semantic_fn('was shattered') == 'passive intensive'

    def test_unmatched_gloss_falls_back_to_passive_other(self) -> None:
        assert _pual_semantic_fn('xyzzy-not-a-real-verb') == 'passive (other)'


class TestHophalSemanticFn:
    def test_death_gloss(self) -> None:
        assert _hophal_semantic_fn('was put to death') == 'causative-passive (death/judgment)'

    def test_motion_gloss(self) -> None:
        assert _hophal_semantic_fn('was brought') == 'causative-passive (motion/transfer)'

    def test_unmatched_gloss_falls_back_to_other(self) -> None:
        assert _hophal_semantic_fn('xyzzy-not-a-real-verb') == 'causative-passive (other)'


class TestHithpaelSemanticFn:
    def test_reciprocal_gloss(self) -> None:
        assert _hithpael_semantic_fn('looked at each other') == 'reciprocal'

    def test_reflexive_gloss(self) -> None:
        assert _hithpael_semantic_fn('humbled himself') == 'reflexive'

    def test_iterative_gloss(self) -> None:
        # 'prayed' is deliberately classified under the iterative bucket
        # here (not reflexive) — the standard Hithpael-prayer gloss
        # ("prayed", "interceded") is treated as habitual/repeated action.
        assert _hithpael_semantic_fn('prayed') == 'iterative'

    def test_unmatched_gloss_falls_back_to_other(self) -> None:
        assert _hithpael_semantic_fn('xyzzy-not-a-real-verb') == 'other'
