"""Tests for scripts/add_paper.py's bibliography helpers and the
metadata-inference API call. Per docs/policies/test-coverage.md's
priority plan (issue #676, Phase 2). Anthropic API calls are mocked —
no real network calls (same pattern as tests/unit/test_ai_review.py).
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import add_paper as ap  # noqa: E402


class TestBiblioHelpers:
    def test_load_missing_biblio_returns_empty_list(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr(ap, "_BIBLIO_PATH", tmp_path / "bibliography.json")
        assert ap._load_biblio() == []

    def test_save_sorts_entries_by_filename(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr(ap, "_BIBLIO_PATH", tmp_path / "bibliography.json")
        entries = [{"filename": "zeta.pdf"}, {"filename": "alpha.pdf"}]
        ap._save_biblio(entries)
        loaded = ap._load_biblio()
        assert [e["filename"] for e in loaded] == ["alpha.pdf", "zeta.pdf"]

    def test_registered_filenames_extracts_the_set(self) -> None:
        entries = [{"filename": "a.pdf"}, {"filename": "b.pdf"}, {"other": "x"}]
        assert ap._registered_filenames(entries) == {"a.pdf", "b.pdf"}


class TestInferMetadata:
    def test_no_api_key_returns_empty_dict_without_calling_the_api(self, monkeypatch) -> None:
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        result = ap._infer_metadata("Some paper text about Hebrew syntax.")
        assert result == {}

    def test_successful_call_parses_json_response(self, monkeypatch) -> None:
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-fake")
        fake_client = MagicMock()
        text_block = MagicMock()
        text_block.text = '{"title": "Test Paper", "author": "Doe, J.", "year": "2020"}'
        fake_message = MagicMock(content=[text_block])
        fake_client.messages.create.return_value = fake_message

        with patch("anthropic.Anthropic", return_value=fake_client):
            result = ap._infer_metadata("Some paper text.")

        assert result == {"title": "Test Paper", "author": "Doe, J.", "year": "2020"}

    def test_response_wrapped_in_markdown_fence_is_unwrapped(self, monkeypatch) -> None:
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-fake")
        fake_client = MagicMock()
        text_block = MagicMock()
        text_block.text = '```json\n{"title": "Fenced"}\n```'
        fake_message = MagicMock(content=[text_block])
        fake_client.messages.create.return_value = fake_message

        with patch("anthropic.Anthropic", return_value=fake_client):
            result = ap._infer_metadata("Some paper text.")

        assert result == {"title": "Fenced"}

    def test_api_error_returns_empty_dict_not_an_exception(self, monkeypatch) -> None:
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-fake")
        fake_client = MagicMock()
        fake_client.messages.create.side_effect = RuntimeError("boom")

        with patch("anthropic.Anthropic", return_value=fake_client):
            result = ap._infer_metadata("Some paper text.")

        assert result == {}
