---
type: policy
scope: berean-bible-bots
status: active
created: 2026-08-31
version: "1.0"
foundry-ref: "Operating Agreement F-1.7 §6 (Progressive Autonomy) + §3 (Decision Authority)"
---

# Autonomous Action Policies

This document is the **per-domain trust matrix** that the Foundry Operating Agreement (§6) delegates to each project. It defines which action categories operate at Phase 1, 2, or 3 for this project, and the criteria for promotion between phases.

---

## Phase Definitions

| Phase | Model | Gate |
|---|---|---|
| **1** | Present → owner approves → act | Default for all new action types |
| **2** | Act → post-hoc owner review | Promoted after demonstrated reliability |
| **3** | Full autonomy; no review required | Not currently granted to any domain |

**Promotion criteria (all three required):**
1. ~5 successful executions at the current phase with no incidents
2. Explicit owner request to promote
3. A rollback or audit mechanism exists for the domain

**Demotion:** any domain may be demoted back to Phase 1 after an incident, at the owner's discretion.

---

## Domain Trust Matrix

| # | Domain | Current Phase | Scope | Restrictions |
|---|---|---|---|---|
| 1 | **Content file writes** | 2 | Lesson `.md`, exercise `.html`/`.md`/`.pdf`, paradigm files, Anki decks written during an assigned task | Owner reviews via `git diff` before commit |
| 2 | **Script execution** | 2 | Build scripts, `exercise_pdf.py`, validators (`validate_courses.py`, `validate_lessons.py`), lint (`flake8`, `mypy`) run as part of the assigned task | Scripts that post to external systems (GitHub API, Anthropic API) are governed by their own domain below |
| 3 | **Git staging + commit** | 2 | `git add <specific paths>`, `git commit` on the current feature branch | Destructive ops (`reset --hard`, `clean -f`, `checkout --`) are Phase 1. Never `git add -A` / `git add .` (shared-worktree rule). Commit message must describe the *why* |
| 4 | **Git push (feature branch)** | 2 | `git push` to the current feature branch | Pushes to `main` are blocked by branch protection and require a PR |
| 5 | **Branch creation** | 2 | `git checkout -b` + `git push -u` for the standard PR workflow | Deleting branches is Phase 1 |
| 6 | **GitHub — issue creation** | 2 | `gh issue create --assignee dnovick` when identifying new work items during a session | Issue body must accurately describe the work; owner reviews in GitHub |
| 7 | **GitHub — PR creation** | 1 | `gh pr create` via author bot | Owner initiates by asking Claude to open the PR; Claude creates it and reports back |
| 8 | **GitHub — AI code review** | 1 | `python scripts/ai_review.py --pr N` | Owner triggers manually; posts review comment + `claude-review` commit status via reviewer bot |
| 9 | **GitHub — PR merge** | 1 | `gh pr merge --squash` | Owner requests explicitly in session; both `review` and `claude-review` status checks must be green |
| 10 | **Anthropic API (ai_review.py)** | 1 | Direct API calls via `scripts/ai_review.py` | Only triggered by owner via explicit `ai_review.py` invocation; uses SDK auto-discovery |

---

## Standing Approvals (Phase-2 Automations)

These are Phase-2 behaviors already in effect, recorded here for auditability:

| Behavior | Approved | Notes |
|---|---|---|
| Commit + push after non-trivial changes without asking | Yes | CLAUDE.md + `memory/feedback_commit_push_auto.md` |
| Run `flake8` + `mypy` before every commit | Yes | CLAUDE.md lint-before-commit rule |
| Run `validate_courses.py` + `validate_lessons.py` in CI | Yes | `.github/workflows/review-pr.yml` |
| Create GitHub issues with `--assignee dnovick` | Yes | `memory/feedback_github_issues.md` |

---

## Actions That Are Always Phase 1

Regardless of any future promotions, the following remain owner-gated:

- Pushing to `main` directly (blocked by branch protection; cannot be promoted)
- Merging a PR (`gh pr merge`)
- Deleting branches, tags, or releases
- Modifying branch protection rules or GitHub App permissions
- Any action affecting billing, secrets, or repository access
- Installing new Python packages or MCP servers
- Running `scripts/ai_review.py` (Anthropic API cost + review authority)

These are not candidates for promotion — they are owner-only by design.

---

## Claude Code Settings Encoding

Claude Code's `permissions.allow` list in `.claude/settings.local.json` is the mechanical layer that suppresses prompts for Phase 2 actions. It is a **usability optimization**, not the primary safety mechanism — `CLAUDE.md` behavioral rules and agent judgment are the actual enforcement.

### How the layers interact

| Layer | Role |
|---|---|
| `permissions.allow` | Skips the interactive prompt for pre-approved commands |
| `CLAUDE.md` behavioral rules | Defines what the agent *should* do (enforced by judgment) |
| `docs/policies/autonomous-actions.md` | The durable policy record (this file) |

### Current alignment (evaluated 2026-09-01)

Phase 2 actions are broadly covered by the allow list (`git *`, `python *`, `gh issue *`, `flake8 *`, `mypy *`). One misalignment was found and corrected:

**`Bash(gh pr *)` was too broad** — it allowed `gh pr create` and `gh pr merge` without prompting, contradicting the Phase 1 policy for those actions. Fixed by replacing it with the Phase 2-only sub-commands:
- `Bash(gh pr checks *)` — checking CI status (Phase 2)
- `Bash(gh pr view *)` — reading PR details (Phase 2)
- `Bash(gh pr list *)` — listing PRs (Phase 2)

`gh pr create`, `gh pr merge`, and `gh pr review` remain outside the allow list and will prompt for approval (Phase 1 behavior).

### Maintenance

When a new Phase 2 action is approved (promotion criteria met — see above), add it to `permissions.allow` via the `update-config` skill. When an action is demoted back to Phase 1, remove it from the allow list.

---

## Review Cadence

- **Per-session:** Claude surfaces any Phase-1 actions needed and waits for explicit approval before proceeding.
- **Per-PR:** Owner reviews the `git diff` before merge; both `review` and `claude-review` checks must pass.
- **Policy review:** revisit this document when a new action type is introduced or after any demotion incident.
