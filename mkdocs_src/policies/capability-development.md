---
type: policy
scope: berean-bible-bots
status: draft
created: 2026-09-10
version: "0.1"
foundry-ref: "Operating Agreement F-1.7 §5 (Quality Standards) — Documentation as Teaching (Rationale Rule); Verification Honesty"
---

# Capability Development Policy

**Status: draft.** This project's Foundry alignment is still in progress — this document
is one piece of that ongoing work, not a finished artifact. Expect it to change.

This is the implementation/testing/documentation standard for an **analysis capability** —
a Python module under `src/bible_grammar/` paired with its `.claude/commands/*.md` slash
command (the project's 27 existing examples: `/verb-prep`, `/word-study`, `/role-search`, …).
It exists because none of this was previously written down: every convention in the 27
existing commands was followed by reading precedent, not by a stated rule, and testing
coverage was never defined at all — as of this document's creation, **zero of 27
capabilities have a committed test that verifies behavior against real corpus data.**

Scope note, mirroring Foundry's own `documentation-standard.md`: this policy governs
durable capability artifacts (code, docs, tests) — not code comments, commit messages, or
conversational output during a session.

---

## Implementation Requirements

- Module lives under the matching subpackage (`core/`, `ot/`, `nt/`, `lexical/`, `names/`,
  `discourse/`, `stems/`, `reporting/`, `intertextuality/`, `verbal_syntax/`, `exercise_pdf/`)
  — create a new subpackage only if the capability doesn't fit an existing one.
- Public functions are exported from `src/bible_grammar/__init__.py`, grouped near related
  existing imports (not appended at the end).
- `flake8` and `mypy --ignore-missing-imports` pass clean (already required by `CLAUDE.md`'s
  lint-before-commit rule; restated here because it's part of what "done" means for a
  capability specifically, not just a general commit hygiene rule).
- A paired `.claude/commands/<name>.md` file, following the shape common to all 27 existing
  commands: H1 title, one-paragraph description, `**Usage:**` line, `**Examples:**` bullets,
  `**Output includes:**` bullets, a `---` separator, then an embedded Python block that parses
  `$ARGUMENTS` and calls the module's `print_*` wrapper.

---

## Documentation Requirements

Per Foundry's Documentation as Teaching principle: docs explain not just *what* a capability
does but *why the result should be trusted* and *how it fits* among related capabilities —
the same standard `docs/features.md`'s existing sections already meet (e.g. Verb Governance's
section explains *why* a tree-walk beats a word-adjacency scan, with a concrete failure case,
not just a function signature).

A capability is not documented until all three of these exist:

1. **`docs/features.md`** — a section with: an explanation paragraph (the methodology/trust
   rationale), a runnable Python code example, and a line reading `**Slash command:**
   \`/name ...\`` with at least one real example invocation.
2. **`docs/commands.md`** — one row in the appropriate category table.
3. **`README.md`'s Feature Summary`** — a bullet, but only when the capability represents a
   new category-level capability, not for every incremental command (bar: does it expand
   what a reader scanning the Feature Summary alone would know exists).

---

## Testing Requirements

Per Foundry's Behavioral Verification Principle: code review is never sufficient alone — a
capability must be observed producing correct output on real, known cases before it's
considered done. This project does not adopt Foundry's full multi-tier verification taxonomy
(disproportionate for a solo research repo); it adopts the underlying discipline, at one tier:

**A capability requires a pytest file under `tests/unit/` (or `tests/integration/` if it
depends on live external data fetches) containing at least one *behavioral* test** — a test
that runs the capability against real corpus data (not a mock, not a synthetic string) and
asserts a known-correct answer, the same kind of verification already done ad hoc for
`verb_governance` today (validated against Isa 36:9 and 2Ki 18:5's known text) but never
before captured as a committed, repeatable test.

This is a **different, additional tier** from the pure-logic unit tests already in this repo
(`test_phrase.py`, `test_poetry.py`, `test_verbal_syntax.py` — all explicitly scoped "no I/O"
in their own docstrings). Pure-logic tests for isolable helper functions remain good practice
but do not by themselves satisfy this requirement.

A PR introducing or changing a capability states, in its description, what was actually run
and what the evidence was — "should work" or "code review looks correct" is not a testing
claim. (Adapted from Foundry's `issue-closure-evidence-standard.md`: done = the implementing
PR + what was tested + the evidence, not "the code exists.")

---

## Backfill: Existing Capabilities Without Behavioral Tests

Per owner decision (2026-09-10): backfill is required as part of adopting this policy, not
deferred as unscheduled debt. As of this document's creation, **no capability has a committed
behavioral test** — this is a larger gap than a first pass suggested (checking actual test
file contents, not just filenames, showed the 3 commands with *any* related test file
(`phrase-search`, `poetry`, `verbal-syntax`) are pure-logic-only, not behavioral).

Tracked in issue #654. Given the scale (effectively all 27 capabilities), that issue's first
task is a short audit to produce the final authoritative list and priority order — not
committing to exact per-capability line-item work in this document, which would go stale
immediately.

---

## Review Cadence

- **Per-capability:** this policy's three requirement sections are the acceptance bar for
  calling a new capability "done" — reference them in the PR description.
- **Policy review:** revisit when Foundry's own OA or standards change in a way that affects
  the cited sections, or when this project's broader Foundry-alignment work reaches a
  checkpoint (this doc moves from `status: draft` to `status: active` at that point, mirroring
  `docs/policies/autonomous-actions.md`).
