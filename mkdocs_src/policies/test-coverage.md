---
type: policy
scope: berean-bible-bots
status: draft
created: 2026-09-10
version: "0.1"
foundry-ref: "Operating Agreement F-1.7 §5 (Quality Standards) — Behavioral Verification Principle"
---

# Test Coverage Policy

**Status: draft.** This project's Foundry alignment is still in progress — this document
is one piece of that ongoing work, not a finished artifact. Expect it to change.

This is the coverage-measurement and coverage-regression policy for this repo. It exists
because, until now, there was no tooling installed (`pytest-cov`/`coverage`), no
configuration anywhere, and no stated policy on what coverage is required or how it's
tracked — raised as a follow-up from the [Capability Development Policy](capability-development.md)
work (issue #654) and tracked as issue #662.

## Why "must not decrease" instead of a hard minimum

As of this policy's creation, whole-repo coverage is **13.54%** (measured with all local
data built — see [Two measurement modes](#two-measurement-modes) below). That number is low
mainly because it includes ~20,000 lines of hand-tuned exercise-PDF generation code
(`src/bible_grammar/exercise_pdf/bbh.py` alone is 12,000+ lines) and dozens of `scripts/`
report builders that were never designed to be tested in isolation — not because the tested
capabilities themselves are unreliable (see the 23 analysis capabilities behaviorally tested
under issue #654, batches 1–5).

A hard minimum percentage (e.g. "80% required") would be meaningless at this starting point —
either set low enough to be satisfied trivially, or high enough to block all normal work until
a large, separate effort closes the gap first. A **"coverage must not decrease" ratchet** is
the sustainable version of the same discipline: every PR is required to leave coverage at or
above where it found it, so the number can only climb over time, driven by whatever priority
work is already happening — no separate crash project required.

## Two measurement modes

Coverage over `src/bible_grammar/` and `scripts/` is measured two ways, because integration
tests need `data/processed/*.parquet` built locally, and CI never builds that data (see
[Capability Development Policy — Testing Requirements](capability-development.md#testing-requirements)):

| Mode | Command | What it measures | Enforced where |
|---|---|---|---|
| **unit** | `python scripts/check_coverage.py` | `pytest tests/ -m "not integration"` | CI (`review-pr.yml`), blocking — matches the existing pytest CI step |
| **full** | `python scripts/check_coverage.py --full` | the complete suite, integration tests included | Local only, manual — run before a substantial PR, the same way `ai_review.py` is a manual step CI can't fully replace |

Both floors live in `coverage-baseline.json` at the repo root (`unit_min_percent`,
`full_min_percent`). `--full` skips gracefully (exit 0, with a warning) rather than failing
if `data/processed/` isn't built locally — a suite with every integration test skipped would
report a misleadingly low number, not a real regression.

## Updating the baseline

The baseline is only ever raised deliberately, in the same PR that earns the increase:

```bash
python scripts/check_coverage.py --update-baseline          # after adding unit tests
python scripts/check_coverage.py --full --update-baseline   # after adding integration tests
```

Never hand-edit `coverage-baseline.json`'s percentages — the tolerance (0.1 percentage
points, to absorb line-count rounding noise) only makes sense paired with a number the
script actually measured. A PR that lowers a floor number must say why in its description
(e.g. deliberate dead-code removal that dropped total statement count) — silently lowering
the ratchet defeats the policy.

## Scope

- Tracks `src/bible_grammar/` and `scripts/` (see `[coverage:run]` in `setup.cfg`).
- Does not track `tests/` itself, `mkdocs_src/`, or lesson/exercise content generation output.
- This policy governs the ratchet mechanism only — it does not replace
  [Capability Development Policy](capability-development.md)'s behavioral-test requirement
  for the 27 slash-command capabilities. A capability can raise the coverage number without
  satisfying that policy (a pure-logic unit test counts toward coverage but isn't a
  behavioral test), and vice versa isn't possible (a behavioral test always raises coverage).

## Priority for closing the pre-existing gap

Tracked in issue #662, which also covers testing gaps outside coverage tooling itself.
Priority order (highest real-world stakes first, per that issue):

1. **`exercise_pdf/`** — generates the actual PDF files students download; zero test
   coverage of PDF generation logic today.
2. **`scripts/validate_*.py`** — the actual CI-enforced quality gate for all lesson/exercise
   content (1,522 lines across 6 files); nothing tests the validators themselves.
3. **`scripts/ai_review.py`** — real branching logic (retry/backoff, the content-rejection
   circuit breaker, the generated-file diff filter, pre-flight token-count escalation) with
   zero coverage.
4. Remaining ~53 non-capability `src/bible_grammar/` modules (internal/support modules not
   exposed as their own slash command), including all 6 non-Hiphil stem modules.

## Review Cadence

- **Per-PR:** `scripts/check_coverage.py` runs automatically in CI (unit mode); run
  `--full` locally before a substantial PR.
- **Policy review:** revisit when Foundry's own OA or standards change in a way that affects
  the cited section, or when this project's broader Foundry-alignment work reaches a
  checkpoint (this doc moves from `status: draft` to `status: active` at that point,
  mirroring `docs/policies/autonomous-actions.md`).
