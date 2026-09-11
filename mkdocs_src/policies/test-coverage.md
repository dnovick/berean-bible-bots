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

**Update `unit_min_percent` in an environment matching CI's exact package list** (the
install line in `review-pr.yml`), never just "wherever `pytest` happens to run." A local
dev environment routinely has optional packages CI doesn't (e.g. `reportlab`, only
installed locally for `exercise_pdf/` work) — any test whose statements only execute when
such a package is importable will silently inflate a locally-measured `unit_min_percent`
above what CI can ever reach, and the very next PR's real CI run fails the ratchet with no
code change of its own. Caught exactly this way once already (issue #676, `exercise_pdf/`
full builder sweep PR) — fixed by re-measuring in an isolated venv built from CI's install
line. `full_min_percent` doesn't have this problem since it's never CI-enforced.

## Branch coverage, not just line coverage

As of 2026-09-10, `[coverage:run]` sets `branch = True`. Line coverage only asks whether a
line executed at all; branch coverage additionally asks whether *both* outcomes of every
conditional were exercised (an `if` with only its true side ever hit is not fully covered).
This is a stricter, more honest signal — a test suite can hit 100% line coverage while
never exercising a function's error paths or `else` branches at all. The tradeoff: branch
coverage percentages are meaningfully lower than line-coverage percentages for the same
test suite (measured at the point of this change: line/statement coverage was 24.39% full,
10.71% unit; the combined branch+statement number `scripts/check_coverage.py` actually
reports is lower — 23.15% full, 9.34% unit). `coverage-baseline.json` was re-measured under
this metric when it was turned on — the ratchet still works the same way, just against a
different (stricter) number.

## Scope

- Tracks `src/bible_grammar/` and `scripts/` (see `[coverage:run]` in `setup.cfg`).
- Does not track `tests/` itself, `mkdocs_src/`, or lesson/exercise content generation output.
- **Excluded from the coverage target**: one-off migration/fixup scripts already run
  historically against the repo and not part of the standing pipeline (`migrate_lessons_phase2.py`,
  `migrate_lessons_phase5.py`, `fix_rtl_wrappers.py`, `fix_collapsed_html_answers.py`,
  `fix_bbh_spelling.py`, `remove_readme_files_sections.py`, `convert_inputs_to_selects.py`,
  `inject_colab_setup.py` — see `[coverage:run]`'s `omit` list in `setup.cfg`). Owner decision
  (2026-09-10, issue #676): writing tests to verify a migration nobody will run again isn't
  worth it — better to be honest that this code isn't maintained than to inflate the number.
  If any of these scripts is ever run again, un-omit it and write a real test first.
- This policy governs the ratchet mechanism only — it does not replace
  [Capability Development Policy](capability-development.md)'s behavioral-test requirement
  for the 27 slash-command capabilities. A capability can raise the coverage number without
  satisfying that policy (a pure-logic unit test counts toward coverage but isn't a
  behavioral test), and vice versa isn't possible (a behavioral test always raises coverage).

## Priority for closing the pre-existing gap

Issue #662 (the original gap — `exercise_pdf/`, all 6 `validate_*.py` scripts, `ai_review.py`,
and a full sweep of the ~53 non-capability `src/bible_grammar/` modules) is closed. Coverage
is now tracked toward an 80% target in **issue #676**, which has the current phased plan
(the `exercise_pdf/` builder sweep, remaining `scripts/`, broadening already-tested
capability modules to their `print_*`/`*_chart` functions, the `discourse/` subpackage
missed by the original sweep, and the last few untested `core/` modules).

## Review Cadence

- **Per-PR:** `scripts/check_coverage.py` runs automatically in CI (unit mode); run
  `--full` locally before a substantial PR.
- **Policy review:** revisit when Foundry's own OA or standards change in a way that affects
  the cited section, or when this project's broader Foundry-alignment work reaches a
  checkpoint (this doc moves from `status: draft` to `status: active` at that point,
  mirroring `docs/policies/autonomous-actions.md`).
