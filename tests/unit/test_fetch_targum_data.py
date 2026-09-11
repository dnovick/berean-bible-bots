"""Tests for scripts/fetch_targum_data.py's response parsing — no real
network calls (urllib.request.urlopen is mocked). Per
docs/policies/test-coverage.md's priority plan (issue #676, Phase 2).
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import fetch_targum_data as ftd  # noqa: E402


def _fake_response(payload: dict) -> MagicMock:
    resp = MagicMock()
    resp.read.return_value = json.dumps(payload).encode("utf-8")
    resp.__enter__ = lambda self: resp
    resp.__exit__ = lambda self, *a: None
    return resp


class TestFetchChapter:
    def test_parses_hebrew_verse_list_from_sefaria_response(self) -> None:
        payload = {"he": ["verse one", "verse two", "verse three"]}
        with patch.object(ftd.urllib.request, "urlopen", return_value=_fake_response(payload)):
            result = ftd.fetch_chapter("Onkelos_Genesis", 1)
        assert result == ["verse one", "verse two", "verse three"]

    def test_non_string_entries_become_empty_strings(self) -> None:
        # Sefaria sometimes returns nested lists (e.g. for versified
        # sub-verses) instead of a plain string — must not crash.
        payload = {"he": ["verse one", ["nested", "list"], None]}
        with patch.object(ftd.urllib.request, "urlopen", return_value=_fake_response(payload)):
            result = ftd.fetch_chapter("Onkelos_Genesis", 1)
        assert result == ["verse one", "", ""]

    def test_missing_he_key_returns_empty_list(self) -> None:
        with patch.object(ftd.urllib.request, "urlopen", return_value=_fake_response({})):
            assert ftd.fetch_chapter("Onkelos_Genesis", 1) == []

    def test_network_error_returns_empty_list_not_an_exception(self) -> None:
        with patch.object(ftd.urllib.request, "urlopen", side_effect=OSError("timed out")):
            assert ftd.fetch_chapter("Onkelos_Genesis", 1) == []
