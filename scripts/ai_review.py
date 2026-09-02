"""AI code review for a GitHub PR using the Anthropic API.

Posts a review comment and commit status via bbb-reviewer-01[bot].
The commit status context is "codex-review" — required by branch protection
as a hard merge gate.

Usage:
    python scripts/ai_review.py --pr N [--model claude-opus-5]

Credentials: the Anthropic SDK auto-discovers credentials from the Claude Code
installation. Do not set ANTHROPIC_API_KEY if you have an identity-linked key
(sk-ant-...) — unset it and let auto-discovery handle authentication.

Requires:
    ~/.config/berean-bots/github-apps.json with reviewer credentials
"""

import argparse
import json
import re as _re
import subprocess
import sys
from pathlib import Path
from typing import Any

import anthropic
import requests

REPO = "dnovick/berean-bible-bots"
STATUS_CONTEXT = "codex-review"
MAX_DIFF_CHARS = 500_000
GITHUB_API = "https://api.github.com"
DEFAULT_MODEL = "claude-opus-5"

# Static across every call — cached (prompt caching) so repeated runs (retries, or
# reviewing multiple PRs in a session) don't repay the token cost of the rules text.
REVIEW_PROMPT_RULES = """\
You are a code reviewer for the berean-bible-bots project — a Biblical Hebrew/Greek/Aramaic \
grammar statistics and lesson generation tool.

Review the pull request diff below and check for violations of the project rules.
Be specific about file paths when flagging issues.

## Rules

1. **Three-format rule**: Scope is `data/lessons/<course>/ch<N>/exercises/<name>/` directories
   ONLY — book-content exercises tied to a lesson chapter. A NEW exercise directory must ship
   all three files from the start: `<name>.md`, `<name>.html`, and `<name>.pdf` — flag that as
   blocking. For an EXISTING exercise directory whose `.html`/`.md` is modified without a
   corresponding `.pdf` change: this is NOT blocking on its own — PDF generation for existing
   exercises is driven by an independent Python data structure (`src/bible_grammar/exercise_pdf/*.py`),
   not derived from the `.html`/`.md`, so content-only fixes legitimately don't require a same-PR
   PDF regen. Only flag it (as a warning, not blocking) if the PR description does not already
   name a tracking issue for the resulting drift. This rule does NOT apply to course reading
   resources under `data/courses/<course>/<instance>/common/` or `.../session-<N>/` (e.g. Psalm
   119 acrostic readings, sight-reading passages) — those are HTML-only by established project
   convention and must never be flagged under this rule.

2. **No transliterations**: Tables, lesson pages, and flashcard decks must never include
   a transliteration column or inline transliteration for Hebrew, Aramaic, or Greek text.

3. **RTL display**: In HTML exercises, a verse reference (e.g. "Gen 1:1") and Hebrew text
   must never appear on the same line. Hebrew must use `direction:rtl; unicode-bidi:embed`.

4. **Dropdown fields**: In HTML exercises, Stem, Conjugation, PGN (Person/Gender/Number),
   Yes/No, and Function fields must use `<select>` elements, not `<input type="text">`.
   `scripts/validate_exercises.py`'s `dropdown-required-fields` check already verifies this
   precisely (exact header-keyword matching) — its output is included below. Trust that
   output over your own reading of the diff: if a file has zero `dropdown-required-fields`
   warnings there, do NOT flag a dropdown-fields issue for it yourself, even if a column name
   (e.g. "Translation", "Weakness Effect", "Root") looks superficially Function-adjacent —
   the validator already excludes free-text-appropriate columns like Root/Translation/Notes.

5. **Answer row alignment**: Every `.answer-row td` must align cell-for-cell with table
   columns — no colspan shortcuts, no bunching all content into the first cell.
   `scripts/validate_exercises.py`'s `answer-row-alignment` and `answer-row-empty` checks
   already verify this precisely by parsing the actual DOM and counting `<td>` cells — its
   output is included below. Counting table cells by reading a large text diff is unreliable;
   trust the validator's output over your own cell-count reasoning. If a file has zero
   `answer-row-alignment` / `answer-row-empty` warnings in the validator output, do NOT flag
   an alignment issue for it yourself.

6. **Lesson structure**: New lesson directories must contain a `README.md` as the lesson.
   A separate `<topic>.md` lesson file alongside a `README.md` is not allowed.

7. **BBH name conventions**: Must use BBH spellings — Alef (not Aleph), Bet (not Beth),
   Het (not Chet), Tet (not Teth), Kaf (not Kaph), Samek (not Samekh), Qof (not Qoph),
   Taw (not Tav), Shewa (not Sheva), Pathach (not Patah), Hateph (not Hatef),
   Holem Waw (not Holem Vav).

8. **No lint directives in output strings**: Never place `# noqa` or `# type: ignore`
   inside a string literal that gets written to a file or printed as output.

9. **Chapter accuracy (BBH Ch28+)**: If the diff adds or modifies a BBH lesson for
   chapters 28 and above, verify the chapter number matches its topic:
   Ch28=Hophal Strong, Ch29=Hophal Weak, Ch30=Piel Strong, Ch31=Piel Weak,
   Ch32=Pual Strong, Ch33=Pual Weak, Ch34=Hithpael Strong, Ch35=Hithpael Weak.
"""

# Varies per PR/commit, but is byte-identical across retries of the same commit (e.g. a
# billing-error retry, or re-running after fixing an unrelated script bug) — cached too, so
# same-commit retries are cheap even though cross-commit runs are always a fresh cache write.
REVIEW_PROMPT_PR = """\
## PR: {title}

{description}

## Diff

```
{diff}
```

## Automated validator output (ground truth for rules 4 and 5)

This is the actual output of `scripts/validate_exercises.py` run against this PR's checked-out
tree, filtered to files touched by this diff. It parses the real DOM — trust it completely for
answer-row-alignment, answer-row-empty, and dropdown-required-fields; do not second-guess it by
re-counting cells yourself.

```
{validator_output}
```

## Response

Return ONLY valid JSON with this exact structure (no markdown fences, no other text):

{{
  "approved": true,
  "summary": "one-sentence overall verdict",
  "findings": [
    {{
      "rule": "name of the rule from the list above",
      "severity": "blocking",
      "file": "repo-relative path or null",
      "description": "specific description of the issue"
    }}
  ]
}}

Approve (`approved: true`) if there are zero blocking findings. Severity `warning` never
blocks approval. If the diff does not touch lesson or exercise content and has no violations,
approve it with an empty findings list.
"""


def _get_reviewer_token() -> str:
    script = Path(__file__).parent / "github_app_token.py"
    result = subprocess.run(
        [sys.executable, str(script), "--role", "reviewer"],
        capture_output=True, text=True, check=True,
    )
    return result.stdout.strip()


def _gh_headers(token: str, accept: str = "application/vnd.github+json") -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": accept,
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _get_pr(pr_number: int, token: str) -> dict[str, Any]:
    resp = requests.get(
        f"{GITHUB_API}/repos/{REPO}/pulls/{pr_number}",
        headers=_gh_headers(token),
    )
    resp.raise_for_status()
    return resp.json()


def _get_diff(pr_number: int, token: str) -> str:
    resp = requests.get(
        f"{GITHUB_API}/repos/{REPO}/pulls/{pr_number}",
        headers=_gh_headers(token, accept="application/vnd.github.diff"),
    )
    resp.raise_for_status()
    return resp.text


def _post_status(sha: str, state: str, description: str,
                 pr_number: int, token: str) -> None:
    resp = requests.post(
        f"{GITHUB_API}/repos/{REPO}/statuses/{sha}",
        headers=_gh_headers(token),
        json={
            "state": state,
            "context": STATUS_CONTEXT,
            "description": description[:140],
            "target_url": f"https://github.com/{REPO}/pull/{pr_number}",
        },
    )
    resp.raise_for_status()


def _post_review(pr_number: int, body: str, event: str, token: str) -> None:
    resp = requests.post(
        f"{GITHUB_API}/repos/{REPO}/pulls/{pr_number}/reviews",
        headers=_gh_headers(token),
        json={"body": body, "event": event},
    )
    resp.raise_for_status()


_DIFF_PATH_RE = _re.compile(r"^diff --git a/(\S+) b/\S+", _re.MULTILINE)


def _get_validator_output(diff: str) -> str:
    """Run validate_exercises.py against the local checked-out tree and filter its
    output to just the files touched by this diff, so the model gets precise,
    DOM-parsed ground truth for the alignment/dropdown checks instead of having to
    (unreliably) count HTML table cells itself in a large text diff.
    """
    paths = _DIFF_PATH_RE.findall(diff)
    if not paths:
        return "(no exercise files in this diff)"
    repo_root = Path(__file__).parent.parent
    result = subprocess.run(
        [sys.executable, str(repo_root / "scripts" / "validate_exercises.py")],
        capture_output=True, text=True, cwd=repo_root,
    )
    lines = (result.stdout + result.stderr).splitlines()
    relevant = [ln for ln in lines if any(p in ln for p in paths)]
    if not relevant:
        return "(validate_exercises.py reported no warnings or errors for any file in this diff)"
    return "\n".join(relevant)


def _run_ai_review(diff: str, title: str, description: str, model: str) -> dict[str, Any]:
    client = anthropic.Anthropic()
    truncated = diff[:MAX_DIFF_CHARS]
    if len(diff) > MAX_DIFF_CHARS:
        truncated += f"\n\n[Diff truncated — showing first {MAX_DIFF_CHARS:,} chars]"
    validator_output = _get_validator_output(diff)
    pr_block = REVIEW_PROMPT_PR.format(
        title=title,
        description=description or "(no description provided)",
        diff=truncated,
        validator_output=validator_output,
    )
    # Two cache breakpoints: the rules block is identical on every call (any PR, any run) so
    # it's always a cache hit after the first; the PR block is only a cache hit when this
    # exact commit's diff is re-reviewed (retries), but still worth marking — a retry after
    # a transient error (billing, a script bug) re-sends the same ~200K-token diff otherwise.
    message = client.messages.create(
        model=model,
        max_tokens=8192,
        thinking={"type": "disabled"},
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": REVIEW_PROMPT_RULES,
                 "cache_control": {"type": "ephemeral"}},
                {"type": "text", "text": pr_block,
                 "cache_control": {"type": "ephemeral"}},
            ],
        }],
    )
    usage = message.usage
    cache_read = getattr(usage, "cache_read_input_tokens", 0) or 0
    cache_created = getattr(usage, "cache_creation_input_tokens", 0) or 0
    print(
        f"  Tokens: {usage.input_tokens:,} input, {usage.output_tokens:,} output"
        f" ({cache_read:,} cache read, {cache_created:,} cache written)"
    )

    text_blocks = [b for b in message.content if b.type == "text"]
    if not text_blocks:
        block_types = [b.type for b in message.content]
        raise SystemExit(
            f"AI review returned no text content (stop_reason={message.stop_reason!r}, "
            f"content block types={block_types!r}, output_tokens={message.usage.output_tokens}). "
            "This previously happened silently (defaulting to an empty {} result, which reads "
            "as a bogus 'REJECTED, 0 findings' review) when the model spent its whole max_tokens "
            "budget on extended thinking with none left for the actual response."
        )
    content = text_blocks[0].text
    # Strip markdown code fences if the model wrapped the JSON
    content = _re.sub(r"^```(?:json)?\s*", "", content.strip())
    content = _re.sub(r"\s*```$", "", content)
    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:
        if message.stop_reason == "max_tokens":
            raise SystemExit(
                f"AI review response was truncated (hit max_tokens={message.usage.output_tokens} "
                "output tokens) before the JSON could be closed. Increase max_tokens in "
                "_run_ai_review() or shrink the diff."
            ) from exc
        raise


def _build_review_body(result: dict[str, Any], model: str) -> str:
    approved = result.get("approved", False)
    summary = result.get("summary", "Review complete.")
    findings = result.get("findings", [])
    blocking = [f for f in findings if f.get("severity") == "blocking"]
    warnings = [f for f in findings if f.get("severity") != "blocking"]

    lines = [
        f"## AI Code Review ({model})\n",
        f"**{summary}**\n",
    ]
    if blocking:
        lines.append("\n### Blocking Issues\n")
        for f in blocking:
            ref = f" (`{f['file']}`)" if f.get("file") else ""
            lines.append(f"- **{f['rule']}**{ref}: {f['description']}")
    if warnings:
        lines.append("\n### Warnings\n")
        for f in warnings:
            ref = f" (`{f['file']}`)" if f.get("file") else ""
            lines.append(f"- **{f['rule']}**{ref}: {f['description']}")
    if not findings:
        lines.append("\nNo issues found.")
    if not approved and not blocking:
        lines.append("\n_Note: review rejected despite no blocking findings — check summary._")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="AI code review for a GitHub PR.")
    parser.add_argument("--pr", type=int, required=True, help="PR number to review")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"Anthropic model (default: {DEFAULT_MODEL})")
    args = parser.parse_args()

    print(f"Fetching PR #{args.pr}...")
    token = _get_reviewer_token()
    pr = _get_pr(args.pr, token)
    head_sha: str = pr["head"]["sha"]
    title: str = pr["title"]
    description: str = pr.get("body") or ""

    print(f"  Title : {title}")
    print(f"  SHA   : {head_sha[:8]}")

    diff = _get_diff(args.pr, token)
    print(f"  Diff  : {len(diff):,} chars")

    print(f"Running AI review ({args.model})...")
    result = _run_ai_review(diff, title, description, args.model)

    approved: bool = result.get("approved", False)
    summary: str = result.get("summary", "Review complete.")
    findings: list[dict[str, Any]] = result.get("findings", [])
    blocking_count = sum(1 for f in findings if f.get("severity") == "blocking")

    print(f"  Result   : {'APPROVED' if approved else 'REJECTED'}")
    print(f"  Summary  : {summary}")
    print(f"  Findings : {len(findings)} total, {blocking_count} blocking")

    review_body = _build_review_body(result, args.model)
    event = "APPROVE" if approved else "REQUEST_CHANGES"
    state = "success" if approved else "failure"

    print("Posting PR review...")
    _post_review(args.pr, review_body, event, token)

    print("Posting commit status...")
    _post_status(head_sha, state, summary, args.pr, token)

    print("Done.")
    sys.exit(0 if approved else 1)


if __name__ == "__main__":
    main()
