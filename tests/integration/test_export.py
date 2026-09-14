"""Behavioral tests for bible_grammar.reporting.export (/export), requiring
real corpus data — data/processed/. Writes to output/exports/ (gitignored),
the same location the capability writes to in normal use.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

import pandas as pd

from bible_grammar.reporting.export import (
    export_word_study,
    export_csv,
    export_html_page,
    export_genre_compare,
    export_divine_names,
    export_semantic_profile,
    export_all,
)

_WORDS_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "words.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORDS_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORDS_PARQUET}")


class TestExportWordStudy:
    def test_shalom_export_produces_all_four_files(self) -> None:
        # export_word_study returns real, on-disk paths for HTML plus three
        # CSVs (by-book, morphology, collocates). The collocates CSV
        # requires collocations() to actually return data — before the
        # collocation.py homonym-letter fix this key was always None for
        # Hebrew OT words (see test_collocation.py).
        _skip_if_missing()
        result = export_word_study('H7965')
        for key in ('html', 'csv_by_book', 'csv_morphology', 'csv_collocates'):
            path = result[key]
            assert path is not None, f"{key} was not generated"
            assert path.exists(), f"{key} path does not exist on disk: {path}"


class TestExportCsv:
    def test_writes_a_real_csv_file(self) -> None:
        df = pd.DataFrame({'a': [1, 2], 'b': ['x', 'y']})
        path = export_csv(df, 'test-export-csv-behavioral', subdir='_test-scratch')
        assert path.exists()
        text = path.read_text(encoding='utf-8')
        assert 'a,b' in text
        assert '1,x' in text


class TestExportHtmlPage:
    def test_writes_a_real_html_page_with_a_table(self) -> None:
        df = pd.DataFrame({'Lemma': ['שָׁלוֹם'], 'Count': [237]})
        path = export_html_page(
            [{'heading': 'Test Section', 'text': 'A test paragraph.', 'df': df}],
            title='Behavioral Export Test',
            slug='test-export-html-page-behavioral',
        )
        assert path.exists()
        text = path.read_text(encoding='utf-8')
        assert 'Behavioral Export Test' in text
        assert 'Test Section' in text
        assert '237' in text


class TestExportGenreCompare:
    def test_ot_export_produces_html_and_per_feature_csvs(self) -> None:
        # Observed: OT export produces one HTML report plus 3 CSVs (one
        # per feature: verb_stem, verb_conjugation, pos).
        _skip_if_missing()
        result = export_genre_compare('OT')
        assert result['html'].exists()
        for feat in ('verb_stem', 'verb_conjugation', 'pos'):
            assert result[feat].exists()


class TestExportDivineNames:
    def test_ot_only_export_produces_html_and_csv(self) -> None:
        _skip_if_missing()
        result = export_divine_names(['OT'])
        assert result['html'].exists()
        assert result['OT'].exists()


class TestExportSemanticProfile:
    def test_shalom_export_produces_a_real_html_report(self) -> None:
        _skip_if_missing()
        result = export_semantic_profile('H7965')
        assert result['html'].exists()
        text = result['html'].read_text(encoding='utf-8')
        # Avoid a direct Hebrew string literal: the corpus's stored
        # combining-mark order for niqqud can differ byte-for-byte from a
        # hand-typed literal even when both render identically (observed:
        # shin-dot/pathach swapped) — assert on the ASCII fields instead.
        assert 'H7965' in text
        assert 'peace' in text


class TestExportAll:
    def test_runs_every_exporter_and_returns_real_paths(self) -> None:
        # Restricting word_studies to one term keeps this fast while still
        # exercising every exporter export_all orchestrates (divine names,
        # both genre comparisons, one semantic profile).
        _skip_if_missing()
        result = export_all(word_studies=['H7965'])
        assert set(result.keys()) == {'divine_names', 'genre_compare', 'semantic_profiles'}
        assert len(result['genre_compare']) == 2  # OT + NT
        for paths in result.values():
            for p in paths:
                assert p.exists()
