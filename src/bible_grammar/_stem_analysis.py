"""
Generic Hebrew verb stem analysis.

All Hebrew derived stems (Hiphil, Niphal, Piel, Pual, Hithpael, Hophal, ...)
follow the same analytical pattern. StemConfig + StemAnalysis implement that
pattern once; individual stem modules supply a StemConfig and thin wrappers.

Usage
-----
from bible_grammar._stem_analysis import StemAnalysis, StemConfig

config = StemConfig(
    name='niphal',
    macula_value='niphal',
    display='Niphal (נִפְעַל)',
    conj_order=[...],
    genre_books={...},
    default_comparison_books=[...],
)
_ANALYSIS = StemAnalysis(config)

niphal_data = _ANALYSIS.data
niphal_conjugation_profile = _ANALYSIS.conjugation_profile
...
"""

from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import pandas as pd

from ._utils import strip_diacritics as _strip, load_ot_data


# ── Default conjugation order (same for all Hebrew stems) ────────────────────

_DEFAULT_CONJ_ORDER: list[str] = [
    'wayyiqtol', 'qatal', 'yiqtol', 'weqatal',
    'imperative', 'jussive', 'cohortative',
    'participle active', 'infinitive construct', 'infinitive absolute',
]

_DEFAULT_GENRE_BOOKS: dict[str, list[str]] = {
    'Narrative': ['Gen', 'Exo', 'Num', 'Jos', 'Jdg', '1Sa', '2Sa', '1Ki', '2Ki'],
    'Law':       ['Lev', 'Deu'],
    'Prophecy':  ['Isa', 'Jer', 'Ezk'],
    'Poetry':    ['Psa', 'Pro', 'Job'],
}

_DEFAULT_COMPARISON_BOOKS: list[str] = [
    'Gen', 'Exo', 'Deu', 'Psa', 'Isa', 'Jer', 'Pro', 'Job',
]

_ALL_STEMS: list[str] = [
    'qal', 'niphal', 'piel', 'hiphil', 'hithpael', 'pual', 'hophal',
]


# ── Configuration ─────────────────────────────────────────────────────────────

@dataclass
class StemConfig:
    """Configuration for a single Hebrew verb stem analysis."""
    name: str                # 'hiphil', 'niphal', etc.
    macula_value: str        # value in MACULA `stem` column
    display: str             # display label: 'Hiphil (הִפְעִיל)'
    conj_order: list[str] = field(default_factory=lambda: list(_DEFAULT_CONJ_ORDER))
    genre_books: dict[str, list[str]] = field(default_factory=lambda: dict(_DEFAULT_GENRE_BOOKS))
    default_comparison_books: list[str] = field(
        default_factory=lambda: list(_DEFAULT_COMPARISON_BOOKS))
    chart_color: str = '#1565C0'  # highlight colour in stem comparison chart


# ── Core class ────────────────────────────────────────────────────────────────

class StemAnalysis:
    """Generic analysis engine for any Hebrew verb stem."""

    def __init__(self, config: StemConfig) -> None:
        self.config = config
        self._chart_dir = Path('output') / 'charts' / 'ot' / 'verbs'

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _load(self) -> pd.DataFrame:
        df = load_ot_data().copy()
        df['_lem'] = df['lemma'].apply(_strip)
        return df

    def _stem_df(self, df: pd.DataFrame) -> pd.DataFrame:
        return df[df['stem'] == self.config.macula_value].copy()

    def _book_col(self, df: pd.DataFrame) -> str:
        return 'book_id' if 'book_id' in df.columns else 'book'

    def _top_glosses(self, h: pd.DataFrame) -> pd.Series:
        return (
            h.groupby('_lem')['english']
            .agg(lambda x: x.value_counts().index[0] if len(x) > 0 else '')
        )

    def _ensure_chart_dir(self) -> Path:
        self._chart_dir.mkdir(parents=True, exist_ok=True)
        return self._chart_dir

    # ── Data functions ────────────────────────────────────────────────────────

    def data(self, book: str | None = None) -> pd.DataFrame:
        """Return all tokens for this stem, optionally filtered to one book."""
        df = self._load()
        h = self._stem_df(df)
        if book:
            bcol = self._book_col(h)
            h = h[h[bcol] == book]
        return h

    def conjugation_profile(self, book: str | None = None) -> pd.DataFrame:
        """Count tokens by conjugation type. Returns DataFrame: form, count, pct."""
        h = self.data(book)
        counts = {f: 0 for f in self.config.conj_order}
        for t in h['type_']:
            t_str = str(t).strip()
            if t_str in counts:
                counts[t_str] += 1
        total = sum(counts.values())
        records = [
            {'form': f, 'count': counts[f],
             'pct': round(counts[f] / total * 100, 1) if total else 0.0}
            for f in self.config.conj_order
        ]
        return pd.DataFrame(records)

    def top_roots(self, n: int = 30, book: str | None = None) -> pd.DataFrame:
        """Return the top-n most frequent roots. Columns: root, lemma, count, pct, top_gloss."""
        h = self.data(book)
        vc = h.groupby(['_lem', 'lemma']).size().reset_index(name='count')
        vc = vc.sort_values('count', ascending=False).head(n)
        total = vc['count'].sum()
        vc['pct'] = (vc['count'] / total * 100).round(1)
        top_g = self._top_glosses(h)
        vc['top_gloss'] = vc['_lem'].map(top_g).fillna('')
        return vc.rename(columns={'_lem': 'root'}).reset_index(drop=True)

    def root_conjugation(
        self,
        roots: list[str] | None = None,
        top_n: int = 15,
    ) -> pd.DataFrame:
        """Return a root × conjugation crosstab (counts)."""
        h = self.data()
        if roots is None:
            roots = h['_lem'].value_counts().head(top_n).index.tolist()
        h_sub = h[h['_lem'].isin(roots)]
        ct = pd.crosstab(h_sub['_lem'], h_sub['type_'])
        ct = ct.reindex(index=roots, columns=self.config.conj_order, fill_value=0)
        return ct

    def book_distribution(self) -> pd.DataFrame:
        """Count tokens per book with % of all-OT occurrences of this stem.
        Columns: book, count, pct, pct_of_book_verbs."""
        df = self._load()
        h = self._stem_df(df)
        bcol = self._book_col(df)

        book_counts = h[bcol].value_counts().reset_index()
        book_counts.columns = ['book', 'count']
        total = book_counts['count'].sum()
        book_counts['pct'] = (book_counts['count'] / total * 100).round(1)

        all_v = df[df['class_'] == 'verb'][bcol].value_counts().reset_index()
        all_v.columns = ['book', 'total_verbs']
        book_counts = book_counts.merge(all_v, on='book', how='left')
        book_counts['pct_of_book_verbs'] = (
            book_counts['count'] / book_counts['total_verbs'] * 100
        ).round(1)
        return book_counts.sort_values('count', ascending=False)

    def stem_comparison(self, books: list[str] | None = None) -> pd.DataFrame:
        """Return verb stem percentages for a set of books (rows=books, cols=stems)."""
        df = self._load()
        if books is None:
            books = self.config.default_comparison_books
        bcol = self._book_col(df)
        rows: list[dict[str, Any]] = []
        for b in books:
            bv = df[(df['class_'] == 'verb') & (df[bcol] == b)]
            tot = len(bv)
            row: dict[str, Any] = {'book': b}
            for s in _ALL_STEMS:
                cnt = (bv['stem'] == s).sum()
                row[s] = round(cnt / tot * 100, 1) if tot else 0.0
            rows.append(row)
        return pd.DataFrame(rows).set_index('book')

    def dominant_roots(
        self,
        min_pct: float = 70.0,
        min_tokens: int = 10,
    ) -> pd.DataFrame:
        """Roots where this stem accounts for ≥ min_pct of all occurrences.
        Columns: lemma, root, {stem}_count, total, pct, top_gloss."""
        df = self._load()
        stem_val = self.config.macula_value
        verbs = df[df['class_'] == 'verb']
        grp = verbs.groupby(['lemma', '_lem', 'stem']).size().reset_index(name='count')
        pivot = grp.pivot_table(
            index=['lemma', '_lem'], columns='stem', values='count', fill_value=0
        ).reset_index()

        if stem_val not in pivot.columns:
            return pd.DataFrame()

        pivot['total'] = pivot.drop(columns=['lemma', '_lem']).sum(axis=1)
        pivot['hif_pct'] = (pivot[stem_val] / pivot['total'] * 100).round(1)
        result = pivot[
            (pivot['hif_pct'] >= min_pct) &
            (pivot[stem_val] >= min_tokens)
        ].copy()

        h = self._stem_df(df)
        top_g = self._top_glosses(h)
        result['top_gloss'] = result['_lem'].map(top_g).fillna('')
        result = result.rename(columns={stem_val: f'{stem_val}_count', '_lem': 'root'})
        count_col = f'{stem_val}_count'
        return result[['lemma', 'root', count_col, 'total', 'hif_pct', 'top_gloss']].sort_values(
            count_col, ascending=False
        ).reset_index(drop=True)

    def semantic_categories(self, semantic_fn: Callable[[str], str]) -> pd.DataFrame:
        """Assign each token a semantic category using semantic_fn(gloss) → category.
        Returns DataFrame: category, count, pct."""
        h = self.data().copy()
        h['category'] = h['english'].apply(semantic_fn)
        counts = h['category'].value_counts().reset_index()
        counts.columns = ['category', 'count']
        total = counts['count'].sum()
        counts['pct'] = (counts['count'] / total * 100).round(1)
        return counts

    # ── Print functions ───────────────────────────────────────────────────────

    def print_overview(self) -> None:
        """Print a quick statistical overview of this stem in the OT."""
        df = self._load()
        h = self._stem_df(df)
        all_v = df[df['class_'] == 'verb']

        total = len(h)
        pct = round(total / len(all_v) * 100, 1) if all_v.shape[0] else 0.0
        unique_roots = h['_lem'].nunique()
        books_with = h['book'].nunique()

        disp = self.config.display
        print()
        print('╔' + '═' * 78 + '╗')
        print('║' + f'  {disp} — OT Overview'.center(78) + '║')
        print('╚' + '═' * 78 + '╝')
        print()
        print(f"  Total {self.config.name} tokens:        {total:>6,}")
        print(f"  % of all OT verb tokens:    {pct:>6.1f}%")
        print(f"  Unique roots:               {unique_roots:>6,}")
        print(f"  Books containing this stem: {books_with:>6,} of 39")
        print()

        top5 = h['book'].value_counts().head(5)
        print(f"  Top 5 books by {self.config.name} count:")
        for book, cnt in top5.items():
            p = cnt / total * 100
            bar = '█' * int(p / 1)
            print(f"    {book:<8} {cnt:>4}  ({p:>4.1f}%)  {bar}")
        print()

        top_roots = h['_lem'].value_counts().head(5)
        print(f"  Top 5 {self.config.name} roots:")
        for root, cnt in top_roots.items():
            gl = h[h['_lem'] == root]['english'].value_counts().index[0]
            print(f"    {root:<8} {cnt:>4}  ({gl})")
        print()

    def print_conjugation(self, book: str | None = None) -> None:
        """Print conjugation distribution."""
        df = self.conjugation_profile(book)
        total = df['count'].sum()
        scope = book or 'Whole OT'

        print()
        print('═' * 72)
        print(f"  {self.config.display} conjugation profile: {scope}  (total: {total:,})")
        print('─' * 72)
        for _, row in df.iterrows():
            if row['count'] == 0:
                continue
            bar = '█' * int(row['pct'] / 1.5)
            print(f"  {row['form']:<24} {row['count']:>5}  {row['pct']:>5.1f}%  {bar}")
        print()

    def print_top_roots(self, n: int = 25, book: str | None = None) -> None:
        """Print the top roots table."""
        df = self.top_roots(n, book)
        scope = book or 'Whole OT'

        print()
        print('═' * 72)
        print(f"  Top {n} {self.config.display} roots: {scope}")
        print('─' * 72)
        print(f"  {'#':<4} {'Root':<10} {'Lemma':<14} {'Count':>6} {'%':>6}  Gloss")
        print('  ' + '─' * 68)
        for i, row in df.iterrows():
            print(f"  {i+1:<4} {row['root']:<10} {row['lemma']:<14} {row['count']:>6} "
                  f"{row['pct']:>5.1f}%  {row['top_gloss']}")
        print()

    def print_root_conjugation(
        self,
        roots: list[str] | None = None,
        top_n: int = 15,
    ) -> None:
        """Print root × conjugation frequency table."""
        ct = self.root_conjugation(roots, top_n)
        h = self.data()
        top_g = self._top_glosses(h)

        abbrev = {
            'wayyiqtol': 'wayyiq', 'qatal': 'qatal', 'yiqtol': 'yiqtol',
            'weqatal': 'weqtl', 'imperative': 'impv', 'jussive': 'juss',
            'cohortative': 'coh', 'participle active': 'ptc',
            'infinitive construct': 'inf.c', 'infinitive absolute': 'inf.a',
        }
        display_cols = [c for c in self.config.conj_order if c in ct.columns]

        print()
        print('═' * 90)
        print(f"  {self.config.display}: Root × Conjugation frequency")
        print('─' * 90)
        header = f"  {'Root':<10} {'Gloss':<18}" + ''.join(
            f"{abbrev.get(c, c[:6]):>7}" for c in display_cols
        ) + f"  {'Total':>6}"
        print(header)
        print('  ' + '─' * 86)
        for root in ct.index:
            row_vals = [ct.loc[root, c] for c in display_cols]
            total = sum(row_vals)
            gloss = str(top_g.get(root, ''))[:16]
            vals_str = ''.join(f"{v:>7}" for v in row_vals)
            print(f"  {root:<10} {gloss:<18}{vals_str}  {total:>6}")
        print()

    def print_book_distribution(self, top_n: int = 25) -> None:
        """Print distribution across books."""
        df = self.book_distribution().head(top_n)

        print()
        print('═' * 76)
        print(f"  {self.config.display} distribution across books (top {top_n})")
        print('─' * 76)
        print(f"  {'Book':<8} {'Count':>6} {'% of OT':>12} {'% of book verbs':>16}  Chart")
        print('  ' + '─' * 72)
        for _, row in df.iterrows():
            bar = '█' * int(row['pct'] * 1.5)
            print(f"  {row['book']:<8} {row['count']:>6} {row['pct']:>11.1f}%"
                  f" {row['pct_of_book_verbs']:>15.1f}%  {bar}")
        print()

    def print_dominant_roots(self, top_n: int = 25) -> None:
        """Print roots where this stem is dominant (≥70% of all occurrences)."""
        df = self.dominant_roots().head(top_n)
        stem_val = self.config.macula_value
        count_col = f'{stem_val}_count'

        print()
        print('═' * 76)
        print(f"  {self.config.display}-dominant roots (≥70% of all occurrences)")
        print(f"  These are functionally '{self.config.display}-only' verbs")
        print('─' * 76)
        stem_hdr = self.config.name[:6]
        print(f"  {'Root':<10} {'Lemma':<14} {stem_hdr:>7} {'Total':>7} {'%':>7}  Gloss")
        print('  ' + '─' * 72)
        for _, row in df.iterrows():
            print(f"  {row['root']:<10} {row['lemma']:<14} {row[count_col]:>7} "
                  f"{row['total']:>7} {row['hif_pct']:>6.1f}%  {row['top_gloss']}")
        print()

    def print_semantic_categories(self, semantic_fn: Callable[[str], str]) -> None:
        """Print semantic function distribution."""
        df = self.semantic_categories(semantic_fn)
        total = df['count'].sum()

        print()
        print('═' * 72)
        print(f"  {self.config.display} semantic function categories  (total: {total:,})")
        print('─' * 72)
        for _, row in df.iterrows():
            bar = '█' * int(row['pct'] / 2)
            print(f"  {row['category']:<35} {row['count']:>5}  {row['pct']:>5.1f}%  {bar}")
        print()
        print("  Note: categories derived from MACULA english gloss annotations.")
        print()

    # ── Chart functions ───────────────────────────────────────────────────────

    def conjugation_chart(self, book: str | None = None) -> Path | None:
        """Save a horizontal bar chart of conjugation distribution."""
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            return None

        df = self.conjugation_profile(book)
        df = df[df['count'] > 0].sort_values('pct')

        fig, ax = plt.subplots(figsize=(9, 5))
        colors = plt.cm.Blues(  # type: ignore[attr-defined]
            [0.4 + 0.5 * (i / max(len(df) - 1, 1)) for i in range(len(df))]
        )
        bars = ax.barh(df['form'], df['pct'], color=colors)
        for bar, val in zip(bars, df['pct']):
            ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                    f"{val:.1f}%", va='center', fontsize=9)

        scope = book or 'Whole OT'
        ax.set_title(f"{self.config.display} Conjugation Distribution — {scope}",
                     fontsize=13, fontweight='bold')
        ax.set_xlabel("% of tokens")
        ax.set_xlim(0, df['pct'].max() * 1.18)
        ax.yaxis.grid(False)
        ax.xaxis.grid(True, linestyle='--', alpha=0.5)
        ax.set_axisbelow(True)
        fig.tight_layout()

        fname = f'{self.config.name}_conjugation{"_"+book if book else ""}.png'
        out = self._ensure_chart_dir() / fname
        fig.savefig(out, dpi=150, bbox_inches='tight')
        plt.close(fig)
        return out

    def book_chart(self, top_n: int = 20) -> Path | None:
        """Save a bar chart of top books by count."""
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            return None

        df = self.book_distribution().head(top_n)
        fig, ax1 = plt.subplots(figsize=(13, 5))

        x = range(len(df))
        ax1.bar(x, df['count'], color='steelblue', alpha=0.8, label=f'{self.config.name} count')
        ax1.set_ylabel('Token count', color='steelblue')
        ax1.tick_params(axis='y', labelcolor='steelblue')

        ax2 = ax1.twinx()
        ax2.plot(x, df['pct_of_book_verbs'], 'o-', color='darkorange',
                 linewidth=1.8, markersize=5, label='% of book verbs')
        ax2.set_ylabel('% of book verbs', color='darkorange')
        ax2.tick_params(axis='y', labelcolor='darkorange')

        ax1.set_xticks(list(x))
        ax1.set_xticklabels(df['book'].tolist(), rotation=40, ha='right', fontsize=9)
        ax1.set_title(f"{self.config.display} Distribution Across Books (top {top_n})",
                      fontsize=13, fontweight='bold')

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
        fig.tight_layout()

        out = self._ensure_chart_dir() / f'{self.config.name}_books.png'
        fig.savefig(out, dpi=150, bbox_inches='tight')
        plt.close(fig)
        return out

    def stem_comparison_chart(self, books: list[str] | None = None) -> Path | None:
        """Save a stacked bar chart of all verb stems with this stem highlighted."""
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            return None

        if books is None:
            books = self.config.default_comparison_books

        df = self.stem_comparison(books)
        stem_val = self.config.macula_value
        base_colors = {
            'qal': '#5B9BD5', 'niphal': '#ED7D31', 'piel': '#A9D18E',
            'hiphil': '#FF0000', 'hithpael': '#FFC000',
            'pual': '#9DC3E6', 'hophal': '#C9C9C9',
        }
        # Override the highlight color for this stem
        colors = dict(base_colors)
        colors[stem_val] = self.config.chart_color

        fig, ax = plt.subplots(figsize=(12, 6))
        x = range(len(books))
        bottoms = [0.0] * len(books)

        for stem in _ALL_STEMS:
            vals = [df.loc[b, stem] if b in df.index else 0 for b in books]
            bars = ax.bar(x, vals, bottom=bottoms, color=colors.get(stem, '#AAAAAA'),
                          label=stem, edgecolor='white', linewidth=0.4)
            for bar, val, bot in zip(bars, vals, bottoms):
                if val >= 5:
                    is_this_stem = stem == stem_val
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bot + val / 2,
                        f"{val:.0f}%",
                        ha='center', va='center', fontsize=7,
                        color='white' if stem in ('qal', stem_val) else 'black',
                        fontweight='bold' if is_this_stem else 'normal',
                    )
            bottoms = [b + v for b, v in zip(bottoms, vals)]

        ax.set_xticks(list(x))
        ax.set_xticklabels(books, fontsize=11)
        ax.set_ylabel('% of verb tokens')
        ax.set_ylim(0, 105)
        ax.set_title(
            f'Verb Stem Distribution by Book — {self.config.display} highlighted',
            fontsize=13, fontweight='bold')
        ax.legend(loc='upper right', fontsize=9, ncol=2)
        ax.yaxis.grid(True, linestyle='--', alpha=0.3)
        ax.set_axisbelow(True)
        fig.tight_layout()

        out = self._ensure_chart_dir() / f'{self.config.name}_stem_comparison.png'
        fig.savefig(out, dpi=150, bbox_inches='tight')
        plt.close(fig)
        return out

    def root_heatmap(self, top_n: int = 15) -> Path | None:
        """Save a heatmap of top roots × conjugation (row-normalised %)."""
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            return None

        ct = self.root_conjugation(top_n=top_n)
        h = self.data()
        top_g = self._top_glosses(h)

        display_cols = [c for c in self.config.conj_order if c in ct.columns]
        ct_sub = ct[display_cols]
        row_totals = ct_sub.sum(axis=1)
        pct_matrix = ct_sub.div(row_totals, axis=0) * 100

        col_abbrev = {
            'wayyiqtol': 'wayyiq', 'qatal': 'qatal', 'yiqtol': 'yiqtol',
            'weqatal': 'weqtl', 'imperative': 'impv', 'jussive': 'juss',
            'cohortative': 'coh', 'participle active': 'ptc.act',
            'infinitive construct': 'inf.cst', 'infinitive absolute': 'inf.abs',
        }
        ylabels = [
            f"{root}  ({top_g.get(root, '')[:14]})" for root in pct_matrix.index
        ]
        xlabels = [col_abbrev.get(c, c[:8]) for c in display_cols]

        fig, ax = plt.subplots(figsize=(12, max(6, top_n * 0.5 + 1)))
        im = ax.imshow(pct_matrix.values, cmap='YlOrRd', aspect='auto', vmin=0, vmax=60)

        ax.set_xticks(range(len(xlabels)))
        ax.set_xticklabels(xlabels, rotation=30, ha='right', fontsize=9)
        ax.set_yticks(range(len(ylabels)))
        ax.set_yticklabels(ylabels, fontsize=9)

        for i in range(len(pct_matrix.index)):
            for j in range(len(display_cols)):
                val = pct_matrix.values[i, j]
                if val > 1:
                    ax.text(j, i, f"{val:.0f}", ha='center', va='center',
                            fontsize=7, color='black' if val < 35 else 'white')

        plt.colorbar(im, ax=ax, label='% of root tokens in this conjugation')
        ax.set_title(
            f"{self.config.display}: Top {top_n} Roots × Conjugation (row-% normalised)",
            fontsize=12, fontweight='bold')
        fig.tight_layout()

        out = self._ensure_chart_dir() / f'{self.config.name}_root_heatmap.png'
        fig.savefig(out, dpi=150, bbox_inches='tight')
        plt.close(fig)
        return out

    def top_roots_chart(self, top_n: int = 20) -> Path | None:
        """Save a horizontal bar chart of the top roots."""
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            return None

        df = self.top_roots(top_n)
        df = df.sort_values('count')

        labels = [f"{row['root']}  ({row['top_gloss'][:16]})" for _, row in df.iterrows()]

        fig, ax = plt.subplots(figsize=(10, max(6, top_n * 0.45)))
        colors = plt.cm.viridis(  # type: ignore[attr-defined]
            [0.2 + 0.6 * (i / max(len(df) - 1, 1)) for i in range(len(df))]
        )
        bars = ax.barh(labels, df['count'], color=colors)
        for bar, val in zip(bars, df['count']):
            ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height() / 2,
                    str(val), va='center', fontsize=8)

        ax.set_title(f"Top {top_n} {self.config.display} Roots (whole OT)",
                     fontsize=13, fontweight='bold')
        ax.set_xlabel("Token count")
        ax.xaxis.grid(True, linestyle='--', alpha=0.5)
        ax.set_axisbelow(True)
        fig.tight_layout()

        out = self._ensure_chart_dir() / f'{self.config.name}_top_roots.png'
        fig.savefig(out, dpi=150, bbox_inches='tight')
        plt.close(fig)
        return out

    def semantic_chart(self, semantic_fn: Callable[[str], str]) -> Path | None:
        """Save a pie chart of semantic function categories."""
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            return None

        df = self.semantic_categories(semantic_fn)
        df = df.sort_values('count', ascending=False)

        colors = [
            '#D32F2F', '#1565C0', '#2E7D32', '#F57F17',
            '#6A1B9A', '#00838F', '#4E342E',
        ]

        fig, ax = plt.subplots(figsize=(9, 7))
        wedges, texts, autotexts = ax.pie(  # type: ignore[misc]
            df['count'],
            labels=[f"{r['category']}\n({r['count']:,})" for _, r in df.iterrows()],
            autopct='%1.1f%%',
            colors=colors[:len(df)],
            startangle=140,
            pctdistance=0.75,
        )
        for t in texts:
            t.set_fontsize(9)
        for at in autotexts:
            at.set_fontsize(8)
            at.set_color('white')

        ax.set_title(f"{self.config.display} Semantic Function Distribution (whole OT)",
                     fontsize=13, fontweight='bold', pad=20)
        fig.tight_layout()

        out = self._ensure_chart_dir() / f'{self.config.name}_semantic.png'
        fig.savefig(out, dpi=150, bbox_inches='tight')
        plt.close(fig)
        return out
