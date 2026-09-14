"""Tests for bible_grammar.stats.freq_table — pure DataFrame logic, no I/O."""

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.lexical.stats import (
    freq_table, verb_stems_by_book, pos_distribution,
    greek_verb_forms, niphal_perfects_by_book,
)

_WORDS_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "words.parquet"
)


def _skip_if_missing() -> None:
    if not _WORDS_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORDS_PARQUET}")


class TestFreqTable:
    def _make_df(self) -> pd.DataFrame:
        return pd.DataFrame({
            "book_id": ["Gen", "Gen", "Gen", "Exo", "Exo", "Lev"],
            "stem":    ["Qal", "Niphal", "Qal", "Qal", "Piel", "Qal"],
            "pos":     ["Verb", "Verb", "Verb", "Verb", "Verb", "Verb"],
        })

    def test_single_column_counts(self) -> None:
        df = self._make_df()
        result = freq_table(df, "book_id")
        counts = dict(zip(result["book_id"], result["count"]))
        assert counts["Gen"] == 3
        assert counts["Exo"] == 2
        assert counts["Lev"] == 1

    def test_default_sorted_descending(self) -> None:
        df = self._make_df()
        result = freq_table(df, "book_id")
        assert result.iloc[0]["count"] >= result.iloc[1]["count"]
        assert result.iloc[1]["count"] >= result.iloc[2]["count"]

    def test_sort_false_preserves_groupby_order(self) -> None:
        df = self._make_df()
        result = freq_table(df, "book_id", sort=False)
        assert "count" in result.columns
        assert len(result) == 3

    def test_multi_column_groupby(self) -> None:
        df = self._make_df()
        result = freq_table(df, ["book_id", "stem"])
        gen_qal = result[(result["book_id"] == "Gen") & (result["stem"] == "Qal")]
        assert gen_qal.iloc[0]["count"] == 2

    def test_output_columns(self) -> None:
        df = self._make_df()
        result = freq_table(df, "stem")
        assert "stem" in result.columns
        assert "count" in result.columns

    def test_empty_dataframe(self) -> None:
        df = pd.DataFrame({"book_id": pd.Series([], dtype=str),
                           "stem": pd.Series([], dtype=str)})
        result = freq_table(df, "book_id")
        assert len(result) == 0
        assert "count" in result.columns

    def test_total_count_preserved(self) -> None:
        df = self._make_df()
        result = freq_table(df, "stem")
        assert result["count"].sum() == len(df)

    def test_reset_index(self) -> None:
        df = self._make_df()
        result = freq_table(df, "book_id")
        assert list(result.index) == list(range(len(result)))


@pytest.mark.integration
class TestVerbStemsByBook:
    def test_genesis_qal_leads(self) -> None:
        # Observed: Genesis has 3,612 Qal verb tokens, far more than any
        # other stem (Hiphil second at 402).
        _skip_if_missing()
        df = verb_stems_by_book(book='Gen')
        top = df.iloc[0]
        assert top['stem'] == 'Qal'
        assert top['count'] >= 3000


@pytest.mark.integration
class TestPosDistribution:
    def test_noun_leads_ot_pos_distribution(self) -> None:
        # Observed: Noun 124,877 tokens, the single largest OT part of
        # speech, ahead of Verb (65,710).
        _skip_if_missing()
        df = pos_distribution()
        top = df.iloc[0]
        assert top['part_of_speech'] == 'Noun'
        assert top['count'] >= 100000


@pytest.mark.integration
class TestGreekVerbForms:
    def test_present_active_indicative_leads_romans(self) -> None:
        # Observed: present/active/indicative 253 in Romans, the single
        # largest tense/voice/mood combination.
        _skip_if_missing()
        df = greek_verb_forms(book='Rom')
        top = df.iloc[0]
        assert top['tense'] == 'Present'
        assert top['voice'] == 'Active'
        assert top['mood'] == 'Indicative'
        assert top['count'] >= 200


@pytest.mark.integration
class TestNiphalPerfectsByBook:
    def test_jeremiah_leads(self) -> None:
        # The CLAUDE.md flagship example ("how many niphal perfect verbs
        # are in a particular book"). Observed: Jeremiah leads with 290,
        # ahead of Isaiah (259).
        _skip_if_missing()
        df = niphal_perfects_by_book()
        top = df.iloc[0]
        assert top['book_id'] == 'Jer'
        assert top['count'] >= 250
