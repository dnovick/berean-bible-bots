"""Tests for bible_grammar.poetry — pure-logic helpers, plus behavioral tests
against real corpus data (marked `integration`, requires data/processed/).
Broadened under issue #676 Phase 3 to cover the module's remaining public
functions."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot.poetry import (
    _jaccard,
    detect_acrostic,
    acrostic_known,
    split_cola,
    is_superscription,
    verse_cola,
    verse_parallel_pairs,
    book_word_pairs,
    parallelism_type,
    book_parallelism_stats,
    compare_poetry_books,
    poetry_report,
    detect_chiasm,
    verse_meter,
    book_meter_stats,
    print_verse_analysis,
    print_book_pairs,
    print_parallelism_stats,
    print_chiasm,
    print_acrostic,
    print_meter_stats,
    print_verse_meter,
)

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


@pytest.mark.integration
class TestColaSplitting:
    def test_split_cola_on_a_real_verse(self) -> None:
        # Observed: Psa 1:1 (17 words) splits into 3 cola of sizes [15, 4, 2].
        _skip_if_missing()
        from bible_grammar.core._utils import load_ot_h
        df = load_ot_h()
        verse_df = df[(df['book'] == 'Psa') & (df['chapter'] == 1) & (df['verse'] == 1)]
        cola = split_cola(verse_df)
        assert len(cola) == 3
        assert [len(c) for c in cola] == [15, 4, 2]

    def test_verse_cola_returns_real_hebrew_text(self) -> None:
        # Observed: Psa 19:2 splits into 3 cola of sizes [5, 3, 4].
        _skip_if_missing()
        cola = verse_cola('Psa', 19, 2)
        assert len(cola) == 3
        assert [len(c) for c in cola] == [5, 3, 4]


class TestIsSuperscription:
    def test_psalm_19_verse_1_is_a_superscription(self) -> None:
        # Observed: Psa 19:1 ("To the choirmaster, a Psalm of David") is a
        # superscription; Psa 1:1 and Psa 3:1 are not.
        _skip_if_missing()
        assert is_superscription('Psa', 19, 1) is True
        assert is_superscription('Psa', 1, 1) is False
        assert is_superscription('Psa', 3, 1) is False


@pytest.mark.integration
class TestParallelism:
    def test_verse_parallel_pairs_returns_real_lemma_pairs(self) -> None:
        # Observed: Psa 1:1 returns 18 lemma-pair rows.
        _skip_if_missing()
        df = verse_parallel_pairs('Psa', 1, 1)
        assert len(df) >= 15
        assert {'lemma_a', 'lemma_b', 'same_lemma', 'domain_overlap'}.issubset(df.columns)

    def test_book_word_pairs_finds_real_recurring_pairs(self) -> None:
        # Observed: Lamentations has 24 recurring word pairs (min_count=2).
        _skip_if_missing()
        df = book_word_pairs('Lam')
        assert len(df) >= 15
        assert df['count'].min() >= 2

    def test_psalm_1_1_is_synthetic_parallelism(self) -> None:
        # Observed: parallelism_type('Psa', 1, 1) == ('synthetic', 0.23).
        _skip_if_missing()
        ptype, score = parallelism_type('Psa', 1, 1)
        assert ptype == 'synthetic'
        assert 0.0 <= score <= 1.0

    def test_lamentations_is_mostly_synthetic(self) -> None:
        # Observed: Lam synthetic 141/154 verses (91.6%).
        _skip_if_missing()
        df = book_parallelism_stats('Lam')
        top = df.sort_values('count', ascending=False).iloc[0]
        assert top['type'] == 'synthetic'
        assert top['pct'] >= 80.0

    def test_compare_poetry_books_agrees_with_individual_stats(self) -> None:
        # Cross-check: compare_poetry_books's per-book synthetic % should
        # match book_parallelism_stats for the same book. Observed:
        # Lam synthetic 91.6%, Sng synthetic 96.6%.
        _skip_if_missing()
        df = compare_poetry_books(['Lam', 'Sng'])
        assert df.loc['synthetic', 'Lam'] >= 85.0
        assert df.loc['synthetic', 'Sng'] >= 85.0


@pytest.mark.integration
class TestPoetryReport:
    def test_writes_a_real_markdown_report(self, tmp_path) -> None:
        # poetry_report() takes an output_dir override — never let it write
        # to the real (git-tracked) output/reports/ in a test.
        _skip_if_missing()
        out = poetry_report('Lam', output_dir=str(tmp_path), top_n_pairs=10)
        path = Path(out)
        assert path.exists()
        content = path.read_text()
        assert '## Parallelism Type Distribution' in content
        assert len(content) > 200


@pytest.mark.integration
class TestChiasm:
    def test_detect_chiasm_returns_a_real_structure(self) -> None:
        # Observed: detect_chiasm('Psa', 1, 1, 6) returns a 6-verse ABC-C'B'A'
        # pattern with pivot=None (even verse count) and is_chiasm=False
        # (mean_score too low to qualify — Psa 1 isn't a real chiasm).
        _skip_if_missing()
        result = detect_chiasm('Psa', 1, 1, 6)
        assert result['pattern'] == ['A', 'B', 'C', "C'", "B'", "A'"]
        assert result['pivot'] is None
        assert isinstance(result['is_chiasm'], bool)
        assert len(result['pairs']) == 3


@pytest.mark.integration
class TestMeter:
    def test_verse_meter_returns_real_syllable_counts(self) -> None:
        # Observed: Psa 1:1 → cola=[0,2,1], pattern='0+2+1', meter_type='other'.
        _skip_if_missing()
        result = verse_meter('Psa', 1, 1)
        assert result['meter_type'] in {'qinah(3+2)', 'balanced(2+2)', 'other'}
        assert len(result['syllables']) == len(result['cola'])

    def test_lamentations_is_mostly_non_qinah(self) -> None:
        # Observed: Lam meter_type value_counts — other 140 (90.9%),
        # qinah(3+2) 9 (5.8%), balanced(2+2) 5 (3.2%). A real, mildly
        # counter-intuitive fact: despite Lamentations being famous for the
        # 3+2 "qinah" (lament) meter, most of its 154 verses don't
        # cleanly match that specific stress pattern under this analyzer.
        _skip_if_missing()
        df = book_meter_stats('Lam')
        assert len(df) >= 140
        vc = df['meter_type'].value_counts()
        assert vc.idxmax() == 'other'


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            lambda: print_verse_analysis('Psa', 1, 1),
            lambda: print_book_pairs('Lam', top_n=10, min_count=2),
            lambda: print_parallelism_stats('Lam'),
            lambda: print_chiasm('Psa', 1, 1, 6),
            lambda: print_acrostic('Lam', 1, 1, 22),
            lambda: print_meter_stats('Lam'),
            lambda: print_verse_meter('Psa', 1, 1),
        )
        for fn in fns:
            capsys.readouterr()
            fn()
            out = capsys.readouterr().out
            assert len(out.strip()) > 30, f"{fn} produced no real output"
