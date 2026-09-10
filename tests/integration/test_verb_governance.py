"""Behavioral tests for bible_grammar's verb-governance capability (/verb-prep),
requiring the real MACULA lowfat tree extraction — data/processed/. Every
expected value here was directly observed by running the capability against
the real corpus, not invented (per docs/policies/capability-development.md's
Behavioral Verification requirement).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot.verb_governance import (
    verb_governance_summary, verb_preposition_distribution, verb_governance_examples,
)

_GOVERNANCE_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_verb_governance.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _GOVERNANCE_PARQUET.exists():
        pytest.skip(f"Data file not found: {_GOVERNANCE_PARQUET}")


# ── בטח (H0982, trust) — the capability's primary worked example ──────────────

class TestBatachGovernance:
    def test_bet_is_top_preposition(self) -> None:
        _skip_if_missing()
        df = verb_preposition_distribution('H0982')
        top = df.iloc[0]
        assert top['lemma'] == 'בְּ'
        assert top['count'] >= 65   # observed: 70

    def test_summary_covers_all_categories(self) -> None:
        _skip_if_missing()
        df = verb_governance_summary('H0982')
        categories = ' '.join(df['category'].tolist())
        assert 'בְּ' in categories
        assert 'direct object' in categories
        assert 'no complement found' in categories

    def test_hiphil_shifts_to_direct_object(self) -> None:
        # Causative בטח (Hiphil, "cause X to trust") takes an accusative
        # direct object for the person made to trust, unlike Qal's
        # PP-only complement. Observed: direct object (with אֵת) is the
        # top category for Hiphil, at 4/5 occurrences.
        _skip_if_missing()
        df = verb_governance_summary('H0982', stem='hiphil')
        top = df.iloc[0]
        assert top['category'] == 'direct object (with אֵת)'


# ── Clause-boundary correctness — the capability's core value proposition ────

class TestClauseBoundaryCorrectness:
    def test_isa_36_9_separates_reflexive_dative_from_true_complement(self) -> None:
        # תִּבְטַח לְךָ עַל־מִצְרַיִם — "you trust FOR YOURSELF upon Egypt."
        # A naive word-adjacency scan would report the first preposition (לְ,
        # reflexive dative) as the governed complement. The tree-based
        # extractor correctly finds ALL THREE pp siblings for this one
        # clause in document order: לְ (reflexive), עַל (Egypt, the true
        # complement), לְ (chariotry — a second real complement).
        _skip_if_missing()
        # top_n high enough to cover all of Isaiah's H0982 rows (21 as of
        # writing) — the default top_n=8 truncates before reaching 36:9.
        examples = verb_governance_examples('H0982', book='Isa', top_n=100)
        isa_36_9 = examples[examples['ref'].str.startswith('ISA 36:9')]
        assert len(isa_36_9) == 3
        preps = isa_36_9['prep_lemma'].tolist()
        assert preps == ['לְ', 'עַל', 'לְ']

    def test_2ki_18_5_does_not_leak_across_clause_boundary(self) -> None:
        # "...בטח... ואחריו לא היה כמהו" — "...trusted... and after him there
        # was none like him." אחריו belongs to the SECOND, unrelated clause.
        # A naive scan mis-attributes it to בטח; the tree-based extractor
        # correctly finds only ONE pp arg (בְּ, "in Yahweh") for this
        # occurrence — never אחר.
        _skip_if_missing()
        examples = verb_governance_examples('H0982', book='2Ki')
        v5 = examples[examples['ref'].str.startswith('2KI 18:5')]
        assert len(v5) == 1
        assert v5.iloc[0]['prep_lemma'] == 'בְּ'


# ── Second verb — confirms the extractor generalizes, not a one-off fit ──────

class TestYareGovernance:
    def test_yare_takes_direct_object_or_min(self) -> None:
        # יָרֵא (fear, H3372): standard BH grammar pattern is either a bare/
        # marked accusative (fear X) or מִן (fear FROM a source of danger).
        _skip_if_missing()
        df = verb_governance_summary('H3372')
        categories = df['category'].tolist()
        assert any('direct object' in c for c in categories)
        assert any(c.startswith('מִן') for c in categories)
