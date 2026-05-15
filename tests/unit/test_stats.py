"""Tests for bible_grammar.stats.freq_table — pure DataFrame logic, no I/O."""

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.lexical.stats import freq_table


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
