"""Tests for scripts/ai_review.py's real branching logic — the generated-file
diff filter, retry/backoff, the content-rejection circuit breaker, and the
pre-flight token-count escalation — per docs/policies/test-coverage.md's
priority plan (issue #662, item 3). No real network calls: the Anthropic
client and `requests`/`subprocess` calls are all mocked.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import anthropic
import httpx
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import ai_review  # noqa: E402


def _fake_request() -> httpx.Request:
    return httpx.Request("POST", "https://api.anthropic.com/v1/messages")


def _rate_limit_error() -> anthropic.RateLimitError:
    resp = httpx.Response(429, request=_fake_request())
    return anthropic.RateLimitError("rate limited", response=resp, body=None)


class TestIsGeneratedPath:
    def test_mkdocs_nav_yml_is_generated(self) -> None:
        assert ai_review._is_generated_path("mkdocs_nav.yml") is True

    def test_mkdocs_courses_mirror_is_generated(self) -> None:
        assert ai_review._is_generated_path("mkdocs_src/courses/bbh/ch1/index.md") is True

    def test_real_source_file_is_not_generated(self) -> None:
        assert ai_review._is_generated_path("src/bible_grammar/lexical/wordstudy.py") is False


class TestFilterGeneratedFiles:
    _DIFF = (
        "diff --git a/mkdocs_nav.yml b/mkdocs_nav.yml\n"
        "index 111..222 100644\n"
        "--- a/mkdocs_nav.yml\n"
        "+++ b/mkdocs_nav.yml\n"
        "@@ -1,1 +1,2 @@\n"
        "+- New: new.md\n"
        "diff --git a/src/bible_grammar/foo.py b/src/bible_grammar/foo.py\n"
        "index 333..444 100644\n"
        "--- a/src/bible_grammar/foo.py\n"
        "+++ b/src/bible_grammar/foo.py\n"
        "@@ -1,1 +1,2 @@\n"
        "+def foo(): pass\n"
    )

    def test_drops_generated_file_block(self) -> None:
        filtered, dropped_files, dropped_chars = ai_review._filter_generated_files(self._DIFF)
        assert dropped_files == 1
        assert dropped_chars > 0
        assert "mkdocs_nav.yml" not in filtered
        assert "src/bible_grammar/foo.py" in filtered
        assert "def foo()" in filtered

    def test_no_generated_files_is_a_no_op(self) -> None:
        diff = (
            "diff --git a/src/bible_grammar/foo.py b/src/bible_grammar/foo.py\n"
            "+def foo(): pass\n"
        )
        filtered, dropped_files, dropped_chars = ai_review._filter_generated_files(diff)
        assert dropped_files == 0
        assert dropped_chars == 0
        assert filtered == diff


class TestCallWithRetries:
    def test_succeeds_first_try_without_sleeping(self, monkeypatch) -> None:
        monkeypatch.setattr(ai_review.time, "sleep", MagicMock())
        fn = MagicMock(return_value="ok")
        result = ai_review._call_with_retries(fn, "test")
        assert result == "ok"
        assert fn.call_count == 1
        ai_review.time.sleep.assert_not_called()

    def test_retries_transient_error_then_succeeds(self, monkeypatch) -> None:
        sleep_mock = MagicMock()
        monkeypatch.setattr(ai_review.time, "sleep", sleep_mock)
        fn = MagicMock(side_effect=[_rate_limit_error(), _rate_limit_error(), "ok"])
        result = ai_review._call_with_retries(fn, "test")
        assert result == "ok"
        assert fn.call_count == 3
        assert sleep_mock.call_count == 2

    def test_exhausts_retries_and_raises_systemexit(self, monkeypatch) -> None:
        monkeypatch.setattr(ai_review.time, "sleep", MagicMock())
        fn = MagicMock(side_effect=_rate_limit_error())
        with pytest.raises(SystemExit, match="failed after"):
            ai_review._call_with_retries(fn, "test-label")
        assert fn.call_count == ai_review.MAX_TRANSIENT_RETRIES

    def test_non_retryable_error_propagates_immediately(self, monkeypatch) -> None:
        # A bad-auth/malformed-request style error is not in _RETRYABLE_ERRORS —
        # retrying it would just burn time on a guaranteed repeat failure.
        monkeypatch.setattr(ai_review.time, "sleep", MagicMock())
        fn = MagicMock(side_effect=ValueError("not retryable"))
        with pytest.raises(ValueError, match="not retryable"):
            ai_review._call_with_retries(fn, "test")
        assert fn.call_count == 1
        ai_review.time.sleep.assert_not_called()


class TestBuildReviewBody:
    def test_approved_no_findings(self) -> None:
        body = ai_review._build_review_body(
            {"approved": True, "summary": "Looks good.", "findings": []}, "claude-haiku"
        )
        assert "No issues found." in body
        assert "Blocking Issues" not in body

    def test_rejected_with_blocking_finding(self) -> None:
        result = {
            "approved": False,
            "summary": "Violates three-format rule.",
            "findings": [
                {"severity": "blocking", "rule": "three-format",
                 "file": "data/lessons/bbh/ch99/exercises/foo/foo.md",
                 "description": "Missing .pdf"},
            ],
        }
        body = ai_review._build_review_body(result, "claude-haiku")
        assert "### Blocking Issues" in body
        assert "three-format" in body
        assert "Missing .pdf" in body
        assert "_Note: review rejected despite no blocking findings" not in body

    def test_rejected_with_no_blocking_findings_adds_note(self) -> None:
        # Edge case the function explicitly handles: rejected overall, but
        # every finding was non-blocking — flag the inconsistency rather
        # than silently rendering a review with no visible reason.
        result = {"approved": False, "summary": "Judgment call.", "findings": []}
        body = ai_review._build_review_body(result, "claude-haiku")
        assert "_Note: review rejected despite no blocking findings" in body


class TestGetValidatorOutput:
    def test_no_files_in_diff_short_circuits(self) -> None:
        assert ai_review._get_validator_output("") == "(no exercise files in this diff)"

    def test_filters_validator_output_to_diff_paths(self, monkeypatch) -> None:
        diff = (
            "diff --git a/data/lessons/bbh/ch1/exercises/foo/foo.html b/...\n"
            "+<table></table>\n"
        )
        fake_result = MagicMock(
            stdout="WARN   data/lessons/bbh/ch1/exercises/foo/foo.html  —  issue\n"
                   "WARN   data/lessons/bbh/ch2/exercises/bar/bar.html  —  unrelated\n",
            stderr="",
        )
        with patch.object(ai_review.subprocess, "run", return_value=fake_result) as run_mock:
            output = ai_review._get_validator_output(diff)
        run_mock.assert_called_once()
        assert "ch1/exercises/foo" in output
        assert "ch2/exercises/bar" not in output

    def test_no_relevant_warnings_reports_clean(self, monkeypatch) -> None:
        diff = "diff --git a/data/lessons/bbh/ch1/exercises/foo/foo.html b/...\n"
        fake_result = MagicMock(stdout="", stderr="")
        with patch.object(ai_review.subprocess, "run", return_value=fake_result):
            output = ai_review._get_validator_output(diff)
        assert "no warnings or errors" in output


class TestContentRejectionCircuitBreaker:
    def test_stops_after_max_rejections_without_calling_the_model(self, monkeypatch) -> None:
        monkeypatch.setattr(sys, "argv", ["ai_review.py", "--pr", "999"])
        monkeypatch.setattr(ai_review, "_get_reviewer_token", lambda: "fake-token")
        monkeypatch.setattr(
            ai_review, "_get_pr",
            lambda pr, token: {"head": {"sha": "abc123"}, "title": "t", "body": "d"},
        )
        monkeypatch.setattr(
            ai_review, "_count_prior_rejections",
            lambda pr, token: ai_review.MAX_CONTENT_REJECTIONS,
        )
        run_review_mock = MagicMock()
        monkeypatch.setattr(ai_review, "_run_ai_review", run_review_mock)
        get_diff_mock = MagicMock()
        monkeypatch.setattr(ai_review, "_get_diff", get_diff_mock)
        post_comment_mock = MagicMock()
        monkeypatch.setattr(ai_review, "_post_issue_comment", post_comment_mock)
        post_status_mock = MagicMock()
        monkeypatch.setattr(ai_review, "_post_status", post_status_mock)

        with pytest.raises(SystemExit) as exc_info:
            ai_review.main()

        assert exc_info.value.code == 2
        # The whole point of the breaker: no diff fetch, no model call —
        # stop spending API calls once the threshold is hit.
        get_diff_mock.assert_not_called()
        run_review_mock.assert_not_called()
        post_comment_mock.assert_called_once()
        post_status_mock.assert_called_once()
        assert post_status_mock.call_args.args[1] == "failure"


class TestPreflightTokenCountEscalation:
    def test_haiku_escalates_to_opus_when_diff_exceeds_context_window(self, monkeypatch) -> None:
        monkeypatch.setenv(ai_review.API_KEY_ENV_VAR, "sk-ant-fake")

        fake_client = MagicMock()
        fake_client.messages.count_tokens.return_value = MagicMock(
            input_tokens=ai_review.HAIKU_CONTEXT_LIMIT + 1
        )
        text_block = MagicMock(type="text", text='{"approved": true, "summary": "ok", "findings": []}')
        fake_message = MagicMock(
            content=[text_block],
            usage=MagicMock(input_tokens=10, output_tokens=5,
                            cache_read_input_tokens=0, cache_creation_input_tokens=0),
            stop_reason="end_turn",
        )
        fake_client.messages.create.return_value = fake_message

        with patch.object(ai_review.anthropic, "Anthropic", return_value=fake_client), \
             patch.object(ai_review, "_get_validator_output", return_value="(no findings)"):
            ai_review._run_ai_review(
                "diff --git a/foo.py b/foo.py\n+pass\n", "title", "desc",
                ai_review.DEFAULT_MODEL,
            )

        # Pre-flight escalation must happen BEFORE any billed generate call —
        # the whole point is never paying for a Haiku call that's guaranteed
        # to 400 on an oversized diff.
        create_kwargs = fake_client.messages.create.call_args.kwargs
        assert create_kwargs["model"] == ai_review.ESCALATION_MODEL

    def test_haiku_stays_on_haiku_for_a_small_diff(self, monkeypatch) -> None:
        monkeypatch.setenv(ai_review.API_KEY_ENV_VAR, "sk-ant-fake")

        fake_client = MagicMock()
        fake_client.messages.count_tokens.return_value = MagicMock(input_tokens=100)
        text_block = MagicMock(type="text", text='{"approved": true, "summary": "ok", "findings": []}')
        fake_message = MagicMock(
            content=[text_block],
            usage=MagicMock(input_tokens=10, output_tokens=5,
                            cache_read_input_tokens=0, cache_creation_input_tokens=0),
            stop_reason="end_turn",
        )
        fake_client.messages.create.return_value = fake_message

        with patch.object(ai_review.anthropic, "Anthropic", return_value=fake_client), \
             patch.object(ai_review, "_get_validator_output", return_value="(no findings)"):
            ai_review._run_ai_review(
                "diff --git a/foo.py b/foo.py\n+pass\n", "title", "desc",
                ai_review.DEFAULT_MODEL,
            )

        create_kwargs = fake_client.messages.create.call_args.kwargs
        assert create_kwargs["model"] == ai_review.DEFAULT_MODEL
