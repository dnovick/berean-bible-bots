"""Matplotlib/seaborn chart helpers. All functions accept output_path to save PNG."""

from __future__ import annotations
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
_DEFAULT_FIGSIZE = (12, 6)


def bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str = "count",
    title: str = "",
    xlabel: str = "",
    ylabel: str = "Count",
    top_n: int | None = 20,
    output_path: str | Path | None = None,
    figsize: tuple = _DEFAULT_FIGSIZE,
) -> plt.Figure:
    """Horizontal bar chart of a freq_table DataFrame."""
    data = df.copy()
    if top_n:
        data = data.nlargest(top_n, y)
    data = data.sort_values(y, ascending=True)

    fig, ax = plt.subplots(figsize=figsize)
    ax.barh(data[x].astype(str), data[y])
    ax.set_title(title, fontsize=14)
    ax.set_xlabel(ylabel)
    ax.set_ylabel(xlabel or x)
    fig.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150)

    return fig


def grouped_bar(
    df: pd.DataFrame,
    x: str,
    hue: str,
    y: str = "count",
    title: str = "",
    top_n: int | None = None,
    output_path: str | Path | None = None,
    figsize: tuple = (14, 6),
) -> plt.Figure:
    """Grouped bar chart (e.g. stem counts per book)."""
    data = df.copy()
    if top_n:
        top_vals = data.groupby(x)[y].sum().nlargest(top_n).index
        data = data[data[x].isin(top_vals)]

    fig, ax = plt.subplots(figsize=figsize)
    sns.barplot(data=data, x=x, y=y, hue=hue, ax=ax)
    ax.set_title(title, fontsize=14)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150)

    return fig


def heatmap(
    df: pd.DataFrame,
    index: str,
    columns: str,
    values: str = "count",
    title: str = "",
    output_path: str | Path | None = None,
    figsize: tuple = (14, 8),
) -> plt.Figure:
    """Pivot-based heatmap (e.g. tense × voice)."""
    pivot = df.pivot_table(index=index, columns=columns,
                           values=values, fill_value=0, aggfunc="sum")
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(pivot, annot=True, fmt="d", cmap="YlOrRd", ax=ax)
    ax.set_title(title, fontsize=14)
    fig.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150)

    return fig
