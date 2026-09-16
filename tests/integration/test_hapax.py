"""Behavioral tests for bible_grammar.lexical.hapax, requiring real corpus
data — data/processed/words.parquet.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.lexical.hapax import hapax_legomena, hapax_summary, hapax_table

_WORDS_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "words.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORDS_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORDS_PARQUET}")


class TestHapaxLegomena:
    def test_job_hapaxes_are_real_and_gloss_populated(self) -> None:
        # Observed: Job has 180 corpus-wide hapax legomena (words occurring
        # exactly once in the whole OT) that also happen to occur in Job.
        _skip_if_missing()
        df = hapax_legomena(book='Job')
        assert len(df) == 180
        for col in ('strongs', 'lemma', 'gloss', 'word', 'reference', 'corpus_count'):
            assert col in df.columns
        assert (df['corpus_count'] == 1).all()
        # First row (canonical order) — Job 2:8, גָּרַד ("to scrape").
        first = df.iloc[0]
        assert first['strongs'] == 'H1623'
        assert first['reference'] == 'Job 2:8'

    def test_scope_book_finds_words_unique_to_one_book_not_the_corpus(self) -> None:
        # scope='book' counts occurrences WITHIN the book only, so it can
        # include words that repeat elsewhere in the OT but appear only
        # once in this specific book — a materially different (larger)
        # set than the corpus-wide default.
        _skip_if_missing()
        corpus_scope = hapax_legomena(book='Job', scope='corpus')
        book_scope = hapax_legomena(book='Job', scope='book')
        assert len(book_scope) >= len(corpus_scope)

    def test_part_of_speech_filter_narrows_to_verbs(self) -> None:
        _skip_if_missing()
        df = hapax_legomena(corpus='OT', part_of_speech='Verb')
        assert len(df) >= 400   # observed: 504
        assert len(df) < 2000   # sanity: must be a real filter, not everything

    def test_max_count_widens_to_rare_not_just_strict_hapax(self) -> None:
        _skip_if_missing()
        strict = hapax_legomena(book='Job', max_count=1)
        rare = hapax_legomena(book='Job', max_count=5)
        assert len(rare) > len(strict)
        assert (rare['corpus_count'] <= 5).all()

    def test_include_context_adds_real_kjv_text(self) -> None:
        _skip_if_missing()
        df = hapax_legomena(book='Job', include_context=True)
        assert 'context_text' in df.columns
        assert (df['context_text'].str.len() > 0).mean() > 0.8


class TestHapaxSummary:
    def test_first_chronicles_leads_by_raw_hapax_count(self) -> None:
        # Real observed behavior — NOT what this module's own docstring
        # claims ("Job has the most OT hapaxes"): by raw count, 1
        # Chronicles leads (811), driven by its genealogies, which mint a
        # large number of proper names that each occur exactly once. Job
        # is famous for RARE vocabulary (a different, scholarly-register
        # claim), but is not the top book by this function's literal
        # count — it comes in 7th at 180. Verified against real data,
        # not assumed from the docstring.
        _skip_if_missing()
        df = hapax_summary(corpus='OT')
        top = df.iloc[0]
        assert top['book_id'] == '1Ch'
        assert top['hapax_count'] >= 700

        job_row = df[df['book_id'] == 'Job'].iloc[0]
        assert job_row['hapax_count'] == 180
        assert job_row['hapax_count'] < top['hapax_count']

    def test_pct_hapax_is_a_real_fraction_of_total_lemmas(self) -> None:
        _skip_if_missing()
        df = hapax_summary(corpus='OT')
        row = df[df['book_id'] == 'Job'].iloc[0]
        assert row['total_lemmas'] >= 1800
        expected_pct = round(row['hapax_count'] / row['total_lemmas'] * 100, 1)
        assert row['pct_hapax'] == expected_pct

    def test_part_of_speech_filter_changes_the_ranking(self) -> None:
        _skip_if_missing()
        all_pos = hapax_summary(corpus='OT')
        verbs_only = hapax_summary(corpus='OT', part_of_speech='Verb')
        assert not all_pos.equals(verbs_only)
        assert (verbs_only['hapax_count'] <= all_pos.set_index('book_id')
                .loc[verbs_only['book_id'], 'hapax_count'].values).all()


class TestHapaxTable:
    def test_prints_real_output_for_job(self, capsys) -> None:
        _skip_if_missing()
        hapax_table(book='Job', top_n=5)
        out = capsys.readouterr().out
        assert 'Job' in out
        assert '180 unique lemmas' in out
        assert 'H1623' in out
        assert '175 more' in out

    def test_empty_result_prints_a_clear_message(self, capsys) -> None:
        # A part_of_speech filter that matches nothing real should print
        # the "No hapax legomena found" message rather than crash.
        _skip_if_missing()
        hapax_table(book='Job', part_of_speech='NotARealPartOfSpeech')
        out = capsys.readouterr().out
        assert 'No hapax legomena found' in out
