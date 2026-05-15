"""Unit tests for _stem_analysis.StemConfig and StemAnalysis (no data required)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

import pytest
from unittest.mock import patch

import pandas as pd

from bible_grammar.stems._stem_analysis import StemConfig, StemAnalysis, _DEFAULT_CONJ_ORDER


class TestStemConfig:
    def test_defaults_populated(self):
        cfg = StemConfig(name='niphal', macula_value='niphal', display='Niphal')
        assert cfg.conj_order == _DEFAULT_CONJ_ORDER
        assert 'Narrative' in cfg.genre_books
        assert len(cfg.default_comparison_books) > 0

    def test_custom_conj_order(self):
        custom = ['qatal', 'yiqtol']
        cfg = StemConfig(name='piel', macula_value='piel', display='Piel',
                         conj_order=custom)
        assert cfg.conj_order == custom

    def test_independent_defaults(self):
        cfg1 = StemConfig(name='piel', macula_value='piel', display='Piel')
        cfg2 = StemConfig(name='niphal', macula_value='niphal', display='Niphal')
        cfg1.conj_order.append('extra')
        assert 'extra' not in cfg2.conj_order


class TestStemAnalysisConjugationProfile:
    """Test conjugation_profile using a mock DataFrame (no real data)."""

    def _make_analysis(self) -> StemAnalysis:
        cfg = StemConfig(name='hiphil', macula_value='hiphil', display='Hiphil')
        return StemAnalysis(cfg)

    def _mock_hiphil_df(self) -> pd.DataFrame:
        return pd.DataFrame({
            'stem': ['hiphil'] * 10,
            'type_': ['qatal', 'qatal', 'yiqtol', 'wayyiqtol', 'qatal',
                      'imperative', 'yiqtol', 'qatal', 'participle active', 'wayyiqtol'],
            'book': ['Gen'] * 10,
            'book_id': ['Gen'] * 10,
            'lemma': ['אמר'] * 10,
            '_lem': ['אמר'] * 10,
            'english': ['say'] * 10,
        })

    def test_conjugation_profile_counts(self):
        sa = self._make_analysis()
        df = self._mock_hiphil_df()
        # Patch data() to return our mock
        with patch.object(sa, 'data', return_value=df):
            result = sa.conjugation_profile()

        assert not result.empty
        qatal_row = result[result['form'] == 'qatal']
        assert qatal_row.iloc[0]['count'] == 4

    def test_conjugation_profile_pct_sums(self):
        sa = self._make_analysis()
        df = self._mock_hiphil_df()
        with patch.object(sa, 'data', return_value=df):
            result = sa.conjugation_profile()

        non_zero = result[result['count'] > 0]
        assert abs(non_zero['pct'].sum() - 100.0) < 0.5

    def test_conjugation_profile_empty(self):
        sa = self._make_analysis()
        empty = pd.DataFrame({'stem': [], 'type_': []})
        with patch.object(sa, 'data', return_value=empty):
            result = sa.conjugation_profile()
        assert result['pct'].sum() == 0.0

    def test_conjugation_profile_has_all_conj_rows(self):
        sa = self._make_analysis()
        df = self._mock_hiphil_df()
        with patch.object(sa, 'data', return_value=df):
            result = sa.conjugation_profile()
        assert set(result['form']) == set(sa.config.conj_order)


class TestStemAnalysisTopRoots:
    def _make_analysis(self) -> StemAnalysis:
        cfg = StemConfig(name='hiphil', macula_value='hiphil', display='Hiphil')
        return StemAnalysis(cfg)

    def _mock_df(self) -> pd.DataFrame:
        return pd.DataFrame({
            'stem': ['hiphil'] * 6,
            'type_': ['qatal'] * 6,
            'book': ['Gen'] * 6,
            'book_id': ['Gen'] * 6,
            '_lem': ['אמר', 'אמר', 'אמר', 'הלך', 'הלך', 'ראה'],
            'lemma': ['אמר', 'אמר', 'אמר', 'הלך', 'הלך', 'ראה'],
            'english': ['say', 'say', 'say', 'go', 'go', 'see'],
        })

    def test_top_roots_returns_correct_order(self):
        sa = self._make_analysis()
        df = self._mock_df()
        with patch.object(sa, 'data', return_value=df):
            result = sa.top_roots(n=3)

        assert result.iloc[0]['root'] == 'אמר'
        assert result.iloc[0]['count'] == 3

    def test_top_roots_pct_sums_to_100(self):
        sa = self._make_analysis()
        df = self._mock_df()
        with patch.object(sa, 'data', return_value=df):
            result = sa.top_roots(n=10)
        assert abs(result['pct'].sum() - 100.0) < 0.5

    def test_top_roots_has_gloss(self):
        sa = self._make_analysis()
        df = self._mock_df()
        with patch.object(sa, 'data', return_value=df):
            result = sa.top_roots(n=3)
        assert 'top_gloss' in result.columns
        assert result[result['root'] == 'אמר']['top_gloss'].iloc[0] == 'say'


class TestStemAnalysisSemanticCategories:
    def test_semantic_categories_columns(self):
        cfg = StemConfig(name='hiphil', macula_value='hiphil', display='Hiphil')
        sa = StemAnalysis(cfg)
        df = pd.DataFrame({
            'stem': ['hiphil'] * 5,
            '_lem': ['x'] * 5,
            'english': ['kill', 'save', 'bring', 'kill', 'declare'],
            'book': ['Gen'] * 5,
        })
        with patch.object(sa, 'data', return_value=df):
            result = sa.semantic_categories(lambda g: 'test-cat')
        assert 'category' in result.columns
        assert 'count' in result.columns
        assert 'pct' in result.columns
        assert result.iloc[0]['count'] == 5
