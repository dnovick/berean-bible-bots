"""Tests for bible_grammar.reporting.charts — no corpus data dependency
(these take a plain caller-supplied DataFrame), so they're genuine unit
tests despite producing real matplotlib output. Per
docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

import matplotlib
matplotlib.use("Agg")  # headless — no display needed for tests

from bible_grammar.reporting.charts import bar_chart, grouped_bar, heatmap


def _freq_df() -> pd.DataFrame:
    return pd.DataFrame({"label": ["alpha", "beta", "gamma"], "count": [10, 25, 5]})


def _grouped_df() -> pd.DataFrame:
    return pd.DataFrame({
        "cat": ["a", "a", "b", "b"],
        "grp": ["x", "y", "x", "y"],
        "count": [1, 2, 3, 4],
    })


class TestBarChart:
    def test_returns_a_figure(self) -> None:
        fig = bar_chart(_freq_df(), x="label", y="count")
        assert fig is not None

    def test_writes_a_real_png_file(self, tmp_path: Path) -> None:
        out = tmp_path / "bar.png"
        bar_chart(_freq_df(), x="label", y="count", output_path=out)
        assert out.exists()
        assert out.stat().st_size > 1000
        with open(out, "rb") as f:
            assert f.read(8) == b"\x89PNG\r\n\x1a\n"


class TestGroupedBar:
    def test_writes_a_real_png_file(self, tmp_path: Path) -> None:
        out = tmp_path / "grouped.png"
        grouped_bar(_grouped_df(), x="cat", hue="grp", output_path=out)
        assert out.exists()
        assert out.stat().st_size > 1000


class TestHeatmap:
    def test_writes_a_real_png_file(self, tmp_path: Path) -> None:
        out = tmp_path / "heat.png"
        heatmap(_grouped_df(), index="cat", columns="grp", output_path=out)
        assert out.exists()
        assert out.stat().st_size > 1000
