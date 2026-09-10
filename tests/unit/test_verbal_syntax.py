"""Tests for bible_grammar.verbal_syntax — pure-logic helpers, plus behavioral
tests against real corpus data (marked `integration`, requires data/processed/)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.verbal_syntax import (
    _strip_diacritics, VERB_FORM_ORDER, VERB_FORM_LABELS,
    verb_form_profile, wayyiqtol_chains,
)

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestStripDiacritics:
    def test_removes_hebrew_vowel_points(self) -> None:
        # בְּרֵאשִׁית with vowels → bare consonants
        pointed = "בְּרֵאשִׁית"
        stripped = _strip_diacritics(pointed)
        assert stripped == "בראשית"

    def test_removes_cantillation(self) -> None:
        # Etnahta U+0591 is cantillation
        with_accent = "בְּרֵאשִׁ֣ית"
        assert _strip_diacritics(with_accent) == "בראשית"

    def test_plain_ascii_unchanged(self) -> None:
        assert _strip_diacritics("hello") == "hello"

    def test_empty_string(self) -> None:
        assert _strip_diacritics("") == ""

    def test_removes_dagesh(self) -> None:
        # בּ has a dagesh (U+05BC combining character)
        with_dagesh = "בּ"  # bet + dagesh
        assert _strip_diacritics(with_dagesh) == "ב"

    def test_latin_with_accents(self) -> None:
        # é → e (Latin combining acute)
        assert _strip_diacritics("é") == "e"

    def test_mixed_pointed_and_plain(self) -> None:
        mixed = "H7965 שָׁלוֹם"
        result = _strip_diacritics(mixed)
        assert "שלום" in result
        assert "H7965" in result


class TestVerbFormConstants:
    def test_form_order_has_expected_entries(self) -> None:
        assert "wayyiqtol" in VERB_FORM_ORDER
        assert "qatal" in VERB_FORM_ORDER
        assert "yiqtol" in VERB_FORM_ORDER
        assert "infinitive construct" in VERB_FORM_ORDER
        assert "infinitive absolute" in VERB_FORM_ORDER

    def test_form_labels_cover_form_order(self) -> None:
        for form in VERB_FORM_ORDER:
            assert form in VERB_FORM_LABELS, f"Missing label for {form!r}"

    def test_labels_are_short(self) -> None:
        for form, label in VERB_FORM_LABELS.items():
            assert len(label) <= 10, f"Label {label!r} is too long for chart axis"

    def test_unique_entries(self) -> None:
        assert len(VERB_FORM_ORDER) == len(set(VERB_FORM_ORDER))


@pytest.mark.integration
class TestVerbFormProfileBehavioral:
    """Genesis is wayyiqtol-heavy narrative — the textbook example of Hebrew
    narrative sequencing. Verified live before writing these assertions:
    wayyiqtol is Genesis's single most frequent verb form, at ~42% of all
    verb tokens (2105 of ~5039)."""

    def test_wayyiqtol_dominates_genesis_narrative(self) -> None:
        _skip_if_missing()
        df = verb_form_profile('Gen')
        top = df.iloc[0]
        assert top['form'] == 'wayyiqtol'
        assert top['pct'] >= 35.0

    def test_all_pcts_sum_to_100(self) -> None:
        _skip_if_missing()
        df = verb_form_profile('Gen')
        assert abs(df['pct'].sum() - 100.0) < 1.0


@pytest.mark.integration
class TestWayyiqtolChainsBehavioral:
    """Gen 1's creation account is built from wayyiqtol chains. Verified live:
    chapter 1 has 15 chains; the first spans verses 3-5 (הָיָה 'it was' ...
    רָאָה 'he saw' ... בָּדַל 'he separated' ... קָרָא 'he called'), broken by a
    qatal/weqatal summary clause."""

    def test_gen_1_has_multiple_chains(self) -> None:
        _skip_if_missing()
        chains = wayyiqtol_chains('Gen', 1)
        assert len(chains) >= 10

    def test_gen_1_first_chain_verses_and_break(self) -> None:
        _skip_if_missing()
        chains = wayyiqtol_chains('Gen', 1)
        first = chains[0]
        assert first['start_verse'] == 3
        assert first['end_verse'] == 5
        assert first['length'] >= 3
        lemmas = [v['lemma'] for v in first['verbs']]
        assert 'רָאָה' in lemmas   # "he saw" (Gen 1:4)
        assert 'קָרָא' in lemmas   # "he called" (Gen 1:5)
