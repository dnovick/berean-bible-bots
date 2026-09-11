"""Tests for scripts/github_app_token.py's pure logic — PEM normalization
and the bot git-author string format. Per docs/policies/test-coverage.md's
priority plan (issue #676, Phase 2). No network/credentials needed.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import github_app_token  # noqa: E402


class TestNormalizePem:
    def test_already_well_formed_key_is_unchanged(self) -> None:
        key = "-----BEGIN RSA PRIVATE KEY-----\nABCD\n-----END RSA PRIVATE KEY-----\n"
        assert github_app_token._normalize_pem(key) == key

    def test_literal_backslash_n_is_converted_to_real_newlines(self) -> None:
        # Common env-var encoding issue: a PEM stored in an env var often
        # has its real newlines escaped as the two characters '\' 'n'.
        key = "-----BEGIN RSA PRIVATE KEY-----\\nABCD\\n-----END RSA PRIVATE KEY-----"
        result = github_app_token._normalize_pem(key)
        assert "\\n" not in result
        assert result.startswith("-----BEGIN RSA PRIVATE KEY-----\n")
        assert result.endswith("-----END RSA PRIVATE KEY-----\n")

    def test_missing_newlines_are_reconstructed_by_wrapping_the_body(self) -> None:
        # If newlines were stripped entirely (all on one line), rebuild
        # by wrapping the base64 body at 64 chars, standard PEM width.
        body = "A" * 130
        key = f"-----BEGIN RSA PRIVATE KEY-----{body}-----END RSA PRIVATE KEY-----"
        result = github_app_token._normalize_pem(key)
        lines = result.strip("\n").split("\n")
        assert lines[0] == "-----BEGIN RSA PRIVATE KEY-----"
        assert lines[-1] == "-----END RSA PRIVATE KEY-----"
        assert all(len(line) <= 64 for line in lines[1:-1])
        assert result.endswith("\n")

    def test_trailing_newline_is_always_present(self) -> None:
        key = "-----BEGIN X-----\nABC\n-----END X-----"
        assert github_app_token._normalize_pem(key).endswith("\n")


class TestGitAuthorString:
    def test_builds_expected_bot_author_string(self, tmp_path, monkeypatch) -> None:
        config_path = tmp_path / "github-apps.json"
        config_path.write_text(json.dumps({
            "author": {"slug": "bbb-author-01", "installation_id": 158082057},
        }))
        monkeypatch.setattr(github_app_token, "CONFIG_PATH", config_path)

        result = github_app_token.git_author_string("author")
        assert result == "bbb-author-01[bot] <158082057+bbb-author-01[bot]@users.noreply.github.com>"

    def test_missing_config_file_raises_systemexit(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setattr(github_app_token, "CONFIG_PATH", tmp_path / "does-not-exist.json")
        try:
            github_app_token.git_author_string("author")
            assert False, "expected SystemExit"
        except SystemExit as exc:
            assert "not found" in str(exc)

    def test_missing_slug_field_raises_systemexit(self, tmp_path, monkeypatch) -> None:
        config_path = tmp_path / "github-apps.json"
        config_path.write_text(json.dumps({"author": {"installation_id": 1}}))
        monkeypatch.setattr(github_app_token, "CONFIG_PATH", config_path)
        try:
            github_app_token.git_author_string("author")
            assert False, "expected SystemExit"
        except SystemExit as exc:
            assert "slug" in str(exc)
