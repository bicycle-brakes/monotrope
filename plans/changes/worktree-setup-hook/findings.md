---
title: "Findings — worktree-setup-hook"
category: findings
status: draft
implementation_status: none
date: 2026-11-25
created: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-wg4z
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — worktree-setup-hook

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1235 files, 5900 commits, 12 rules.

Stage-2 call, 2026-11-25: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1238 files, 5903 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-25

Spec fingerprint: sha256:5ea12f48640ef7ceda22a74c4d1ffeeda77821f727307bb2752f07aab547c98b

Spec review commit: 21235d1c400086aa1daeb41e68b5c8cb58dc1d07

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | [AMBIGUITY] | SPEC | base | spec.md, Open decisions (first [DETAIL]); criteria 1–6 | "Without blocking checkout" can be read two ways, and the readings build different hooks. (a) Setup runs in the foreground. `git worktree add`, and the harness that called it, returns only after `make venv` (pip over the whole `requirements-ci.txt`) and `npm ci` have finished. That takes time and needs the network, and failure messages reach the caller's standard error before git returns. (b) Setup is detached into the background. The checkout returns at once, an agent may start work before `.venv` and `tools/pi/node_modules` exist, and the criterion-5 message appears after git has returned or reaches no one. Criteria 1–6 do not choose between the readings. | Opus | open | — |
| S-2 | MINOR | SPEC | base | spec.md, criteria 1–4 | The spec puts no limit on how long setup may take. `npm ci`, pip and the `tools/pi/pi --version` check can stall on a dead network or a misbehaving Pi. Under the foreground reading, that holds the checkout open. In the same file, the Beads block caps its call with `BEADS_HOOK_TIMEOUT` (default 300 s, `.beads/hooks/post-checkout:9`), and `scripts/stage2.py:290` caps `pi --version`. The spec says neither whether setup has a limit nor what is reported when one is exceeded. | Opus | open | — |
| S-3 | MINOR | SPEC | base | spec.md, criteria 1 and 9; Protected areas | "Outside the managed block" allows the setup section above the BEGIN marker or below the END marker, and the two behave differently. The managed block exits on a nonzero `bd` result (`.beads/hooks/post-checkout:34`). A section below the block is therefore skipped whenever `bd` fails. A section above it delays `bd` by the whole setup. The spec does not say whether a qualifying checkout still gets setup when the Beads integration fails, so a criterion-1 test with a failing `bd` stub has no defined expected result. | Opus | open | — |
| S-4 | MINOR | SPEC | base | spec.md, criterion 5 | "Prominently" cannot go red: the refutation checks only that a message exists and names the step. The spec also does not say where the output of `make venv`, pip and `npm ci` goes. It could pass through to standard error (git sends hook output there), be suppressed, or be written to a log. That choice decides whether the failure line can be seen at all among the install output. | Opus | open | — |
| S-5 | MINOR | SPEC | base | spec.md, criterion 7 | Only the value `1` is specified. Whether `HARNESS_NO_LANE_SETUP=0`, `true`, `yes` or an empty value skips setup is left to whoever builds it. For `0`, an "any non-empty value" reading and an "exactly `1`" reading give opposite results, and no criterion can go red on either. | Opus | open | — |
| S-6 | MINOR | SPEC | base | spec.md, Definition of Done, second and fourth items | "Retire the obsolete tracker memory after the hook is available" names no point in time. Inside the pull request that closes the bead, the hook is not yet on `main`. After the merge, the change is closed and nothing checks the retirement. Unlike the other items, this one cannot be checked from the pull request. | Opus | open | — |
