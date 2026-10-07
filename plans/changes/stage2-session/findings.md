---
title: "Findings — stage2-session"
category: findings
status: draft
implementation_status: none
date: 2026-10-07
created: 2026-10-07
last_reviewed: 2026-10-07
updated: 2026-10-07
supersedes: null
superseded_by: null
bead: coding-harness-amp
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — stage2-session

Stage-2 call, 2026-10-07: spec-review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 270 files, 607 commits, 12 rules.

## Phase 2a — Codex, 2026-10-07

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | MAJOR | SPEC | base | `spec.md:44–51,74–85,113–117`; `research.md:58–61` | [GAP] No accepted OpenCode model or provider/model mapping is identified. Research reports no OpenCode declaration; undeclared transports must be refused, and new endpoint approvals are excluded. Only PR #89 is a prerequisite. Implementing the OpenCode path therefore requires an unstated declaration dependency or an invented supported-model contract; no permitted positive OpenCode invocation is specified. | Codex | in spec — Supported models and prerequisites: existing Codex positive path; OpenCode Go activation depends on the separately approved declaration, with fixture-only positive tests until then | — |
| F-2 | MAJOR | SPEC | base | `spec.md:37–38,66–77` | [AMBIGUITY] Consider Terminal accepting the command while its shell cannot find the CLI. Reading “Dispatch” as terminal acceptance produces success and a successful-dispatch audit. Reading AC8’s missing-executable refutation as requiring executable startup produces failure and a failed-dispatch audit. The spec gives these different outcomes for the same launch state without defining which boundary determines success. | Codex | in spec — maintainer said "mach weiter" to the recommendation on 2026-10-07; Terms and criterion 8 distinguish prerequisite refusal from Terminal acceptance and subsequent GUI-window failures | — |
| F-3 | MAJOR | SPEC | base | `spec.md:44–47` | [GAP] The association between a change and its dedicated worktree is undefined. Two attached, non-main linked worktrees can contain the same tracked change directory, so resolving that directory within the current root does not identify which worktree belongs to the change. For an invocation from the other change’s worktree, the implementer must invent the association that determines acceptance or refusal. | Codex | in spec — Supported models and prerequisites fixes the canonical main-checkout/.claude/worktrees/change association and attached-branch requirement | — |

Reviewer session: codex 01a116cd-d624-7ee0-9e14-3db0027c8eff

Stage-2 call, 2026-10-07: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 274 files, 612 commits, 12 rules.

Implementation attempt outcome, 2026-10-07: operator terminated the known
GLM CLI process after more than 15 minutes without an answer or code changes.
CLI exit 143, runner exit 1; the worktree needed no restore. This is not a
completed implementation or review. Claude Code also reported that its local
catalog did not describe glm-5.3-flash; that warning alone does not establish
the cause of the missing response. No credentials were read by the orchestrator.

Stage-2 call, 2026-10-07: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 274 files, 614 commits, 12 rules.

Implementation attempt outcome, 2026-10-07: the second GLM Flash attempt ran
as a file-tool worker and wrote the session verb: `scripts/stage2_session.py`
(the dispatch helper), `scripts/stage2.py` (session wiring, the required
`--model` and optional `--handover`, and the refusals for other verbs),
`tests/test_stage2_session.py` (refusal and dispatch tests over temporary
linked worktrees with fake CLI, effective-policy and Terminal stand-ins), the
`.stage2-sessions/` ignore entry, the workflow section "The interactive
session (`session`)", and this record. No command ran in the worker session:
`make verify`, the registry check and any repair belong to the runner step
that follows. The GUI/model smoke test is unrun. Review loop and final review
have not started.

Stage-2 call, 2026-10-07: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 276 files, 614 commits, 12 rules.

Implementation attempt outcome, 2026-10-07: the repair attempt reviewed the
attempt-2 code against the block gates and repaired three defects, all in
`tests/test_stage2_session.py`: the denylist refusal is now asserted against
the rendered verdict on standard output instead of standard error, and the two
OpenCode dispatch tests now script the `osascript` stand-in step that runs the
launch command, so the recorded interactive `opencode` call exists and is
asserted exactly once. `scripts/stage2_session.py`, the session wiring in
`scripts/stage2.py`, the workflow section and the ignore entry stood the
review unchanged. No command ran in the worker session: `make verify`, the
registry check, the review loop and the final review belong to the runner
steps that follow. The GUI/model smoke test is unrun.

Stage-2 call, 2026-10-07: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 276 files, 615 commits, 12 rules.
