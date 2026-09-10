# Multica Evaluation

**Status:** In progress  
**GitHub Issue:** [#584 — Evaluate Multica as issue tracker and agent orchestration platform](https://github.com/dnovick/berean-bible-bots/issues/584)  
**Audience:** David Novick, Mark (BTP)  
**Last updated:** 2026-09-10

---

## Goal

Evaluate Multica as a replacement for GitHub Issues (berean-bible-bots) and Linear (BTP/Mark). The berean-bible-bots workspace is the test vehicle. Produce a recommendation: **adopt, defer, or reject**.

---

## Workspace Setup

The Multica workspace was configured as follows:

- **Workspace:** `berean-bible-bots`, ID `00e1b263-d36a-4006-b571-7f36b5b51607`
- **CLI:** `multica` v0.4.42, installed via `brew install multica-ai/tap/multica`
- **Auth:** PAT-based; daemon running locally
- **Runtimes auto-detected:** `Claude (Mac.lan)` and `Codex (Mac.lan)` (both online)
- **Built-in agent:** Mika (Chief of Staff, idle, max 3 concurrent tasks)

### Label Taxonomy Created

The Foundry issue-triage-standard was replicated using Multica custom labels:

| Group | Labels |
|---|---|
| Priority | P1: Urgent, P2: High, P3: Medium, P4: Low |
| Timing | Timing: Now, Timing: This Month, Timing: This Quarter, Timing: Later, Timing: Someday |
| Area | Area: Lessons, Area: Exercises, Area: Orchestration, Area: Infrastructure, Area: Reports |

### GitHub Issues Migrated

All 28 open GitHub issues were migrated to Multica as BERE-1 through BERE-28. Each issue has:
- Title prefixed with `[GH#N]` for traceability
- Description body linking back to the original GitHub issue
- Priority, Timing, and Area labels applied
- Appropriate status (`in_progress` for active work, `backlog` for queued)

123 closed GitHub issues have **not** been migrated — pending owner decision on whether historical record is wanted in Multica.

---

## Issue Tracking — Findings

### Priority levels (P1–P4)
✅ **Supported.** Multica has a native `priority` field with values `urgent / high / medium / low / none`. These map cleanly to the Foundry P1–P4 taxonomy. Labels were also created (P1–P4) to surface priority in the board view alongside the native field.

### Timing buckets
✅ **Supported via labels.** No built-in bucket concept exists, but the five Foundry timing buckets (Now / This Month / This Quarter / Later / Someday) were implemented as custom labels. This works, but requires naming-convention discipline — there is no enforcement preventing an issue from having two conflicting timing labels.

### GitHub issue import
⚠️ **No built-in importer — scripted migration works.** There is no `multica issue import` command or UI import path. All 28 open issues were successfully migrated with a ~100-line Python script using `multica issue create --description-file`. The same script handles the 123 closed issues when/if wanted.

### Label groups / milestones / cycles
⚠️ **Labels yes; milestones and cycles no.** Labels are a flat namespace — there is no formal grouping (no "Priority" group vs. "Timing" group). The naming convention (`P1:`, `Timing:`) provides visual grouping in the UI, which is workable. There is no sprint/cycle concept — this would need to be simulated with labels or status fields. This is a meaningful gap vs. Linear.

### External issue reporting
❌ **Not supported.** Multica requires workspace membership. Anyone reporting a bug must be invited to the workspace first. This is a regression vs. GitHub Issues, which allows any GitHub user to file an issue. For a project that might accept community contributions or bug reports, this is a real limitation.

### GitHub integration
🔲 **Not yet tested.** See [GH#586](https://github.com/dnovick/berean-bible-bots/issues/586).

---

## Agent Orchestration — Findings

### Runtime architecture

The Multica daemon runs **locally on Mac**. When `multica setup cloud` ran, it auto-detected two installed runtimes:

```
Claude (Mac.lan)  — provider: claude   — status: online
Codex (Mac.lan)   — provider: codex    — status: online
```

"Local" runtime mode means all agent work happens on this machine — using the local repo, filesystem, and API keys. Multica coordinates the work; the Mac executes it.

### The three orchestration primitives

**Agents** — named workers tied to a runtime. Each has a runtime (Claude or Codex), model, thinking level, custom instructions, MCP servers, and a max concurrent task limit. Mika is a special built-in Chief of Staff agent whose role is planning and routing — not code execution. Specialist agents can be created with task-specific instructions.

**Autopilots** — trigger-driven agents. Triggers are schedule-based (cron) or webhook-based. Two execution modes:
- `create_issue` — creates a Multica issue on each trigger, then assigns it to an agent
- `run_only` — fires the agent directly from a description/prompt, with no issue created

**Squads** — a team of agents with a leader. The leader receives an issue, breaks it into sub-issues, and dispatches each to a squad member. Members can work in parallel (fan-out) or in sequence (staged barrier groups — stage 2 doesn't start until stage 1 finishes). Not yet tested end-to-end.

### Four ways to invoke an agent

| Path | Description | When to use |
|---|---|---|
| Issue → assign | Create issue, assign to agent, it runs | Specific, well-scoped task |
| Chat with Mika | Describe a goal; Mika drafts the issue brief and assigns it | Goal is clear but not yet broken down |
| Autopilot `create_issue` | Scheduled/webhook trigger creates an issue and runs it | Recurring work (weekly review, report builds) |
| Autopilot `run_only` | Agent fires directly from a prompt; no issue created | Lightweight triggered execution |

### Repo isolation — key finding

`multica repo checkout` description: *"Creates a git worktree from the daemon's bare clone cache. Used by agents to check out repos on demand."*

**Multica manages its own repo worktrees.** The daemon maintains a bare clone cache; each agent run gets its own isolated worktree. This means:
- No need to manually maintain separate clones for concurrent agent runs
- Working directory isolation between parallel agents is automatic
- Existing interactive sessions (the two clones currently in use) remain separate

This directly resolves the repo isolation concern raised during evaluation.

### CLI/API driven
✅ **Yes.** Full CLI (`multica` v0.4.42) and PAT-based REST API. Claude can create, update, label, and assign issues programmatically — as demonstrated by the bulk migration script.

### Parallel agent fan-out
✅ **Yes (via Squads).** Squad members can be dispatched in parallel. `max_concurrent_tasks` is configurable per agent.

### Session continuity across context resets
🔲 **Not yet tested.** Key open question — when an agent run is interrupted, does resuming start fresh from the issue description or pick up mid-run?

---

## ⚠️ Critical Implication: Issue Quality Becomes Essential

In an interactive Claude Code session, Claude can ask clarifying questions mid-task. In headless agent mode, **the issue description is the only brief the agent gets.** There is no back-and-forth.

This means:
- Vague issues produce vague or incorrect results
- The issue body must include: what to do, what "done" looks like, any constraints or standards to follow, and links to relevant files or specs

**A well-written issue for this project should include:**
- A clear deliverable (not just "fix X" — but "the HTML exercise at path Y should have Z behavior")
- A reference to the relevant standard (e.g., `mkdocs_src/standards/exercises.md`)
- A definition of done verifiable by a tool (e.g., "validate_exercises.py passes with 0 warnings")
- Any file paths the agent needs to know about

Mika's role becomes more valuable as a "pre-flight" step — she can review an issue before it's assigned and flag gaps in the brief before the agent runs.

---

## Migration Assessment

### GitHub Issues → Multica
**Effort: Moderate (one-time, scripted).** No built-in import path exists. The Python migration script handles it well. Time to migrate all 151 issues (28 open + 123 closed) is estimated at under 30 minutes of script runtime with no manual work. The script is reusable for ongoing sync if needed.

The bigger consideration is ongoing workflow: once migrated, do you work in GitHub Issues or Multica? Running both in parallel creates drift.

### Mark's Linear → Multica
🔲 **Not yet assessed.** See [GH#585](https://github.com/dnovick/berean-bible-bots/issues/585).

### Linear export → Multica import path
🔲 **Not yet assessed.** See [GH#585](https://github.com/dnovick/berean-bible-bots/issues/585).

---

## Open Questions

1. **Session continuity** — when a headless agent run is interrupted, does resuming start fresh or continue mid-run?
2. **GitHub sync** — can Multica subscribe to GitHub webhooks and mirror issue state bidirectionally? (#586)
3. **GitHub Actions integration** — can Multica trigger or be triggered by GitHub Actions on issue state changes? (#586)
4. **Mark's Linear comparison** — feature-for-feature comparison not yet done (#585)
5. **Cycles** — no built-in sprint/cycle concept; how does this affect the Foundry 2-week cadence?

---

## Remaining Evaluation Steps

- [ ] Test agent orchestration end-to-end: assign a real issue to the Claude agent and observe the run
- [ ] Verify repo worktree isolation in practice
- [ ] Test session continuity (interrupt + resume)
- [ ] Assess GitHub integration (#586)
- [ ] Compare with Mark's Linear setup (#585)
- [ ] Produce final go/no-go recommendation

---

## Preliminary Impression

Multica's **agent orchestration** story is genuinely stronger than GitHub Issues — Agents, Autopilots, Squads, and automatic repo worktree isolation are built for exactly the multi-agent workflows this project is moving toward. The daemon-based local runtime model means no cloud dependency for execution.

The **issue tracking** side is functional but thinner than GitHub Issues or Linear: no cycles, no external issue intake, no bulk import, and a flat label namespace. For David's solo use on berean-bible-bots, these gaps are manageable. For Mark's use on larger BTP projects with external contributors or sprint-based planning, they may be more significant.

The most important unresolved question before a recommendation: **can Multica and GitHub Issues coexist** (Multica for orchestration, GitHub Issues for public-facing bug reports and PR linkage), or does adopting Multica mean replacing GitHub Issues entirely?
