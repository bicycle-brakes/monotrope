---
title: "Session handover — interview-minimums implemented, the decision pull request is open, 2026-10-08"
category: handover
created: 2026-10-08
updated: 2026-10-08
last_reviewed: 2026-10-08
owner: Data Architect
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: cline, version: "2026-10-08"}
status: pending
review: {status: pending, approved_by: null, approved_at: null}
tags: [handover, interview, gates, workflow, cline]
bead: coding-harness-6yg
---

# interview-minimums — implemented, decision pull request open

## Where we are

The mandatory feature/ADR interviews are implemented end to end on branch
`feat/interview-minimums` (worktree `.claude/worktrees/interview-minimums`,
base `cc020f5`), bead `coding-harness-6yg`, claimed as
`cline-interview-minimums`. Phases 1–7 ran in order: research, ten decisions
(four asked, six given or refined with reasons), spec with twelve acceptance
criteria, Codex spec review (nine rows, all in spec, four ambiguities settled
by the maintainer as Q-5–Q-8), the waiver of phase 2b recorded in the spec's
non-goals, plan, implementation, `make verify` green, GLM review loop round 1
(eight rows: six taken, two rejected with reasons), Codex phase-6 review
(eleven rows F-10–F-20: every one taken and repaired), and a final green
`make verify` after each repair round. The decision pull request on this
branch is the release; **no merge without the maintainer's explicit order.**

## What the change holds

- `prompts/01a-interview.md`: the duty with the minimums and the
  machine-readable question record (`## Q-n ·` fields, `## SKIP · interview`).
- `prompts/02-spec.md`: the spec gate names the interview check before the
  spec passes.
- `docs/WORKFLOW.md`, `AGENTS.md`: phase table, duty paragraph, class
  section, stage-1 table, workflow table — the optionality wording is gone.
- `scripts/check_interview_minimums.py`: the gate (exit 0/1/3) — counts
  distinct maintainer-answered records per class, sees ADR paths in every
  diff state (committed, index, unstaged, untracked), base per context
  (first parent on the main line, else the merge base; detached at
  `origin/main` exits 3), cut-off `2026-10-08` against the spec date,
  archived post-cut-off changes measured, `--change` strict.
- `tests/test_check_interview_minimums.py`: 36 cases — the spec's
  counterexample matrix plus the loop and phase-6 rows, Git-isolated
  fixtures (F-19).
- `decisions/gates.yaml` + regenerated `.github/workflows/ci.yml`: the gate,
  verify, block, both.

## Evidence

- Final `make verify`: **VERIFY GREEN — every local gate of the 'verify' job
  passed** (pytest 1300+ passed, ruff, plans-registry, adr-answers,
  interview-minimums, ci-drift, gate-schema and the rest), 2026-10-08, after
  the phase-6 repairs.
- Review evidence stands unchanged in
  `plans/changes/interview-minimums/findings.md`: phase 2a nine rows `in
  spec`; phase 4b eight rows decided (L1-5 and L1-8 rejected with reasons,
  named as accepted limits in the pull request); phase 6 eleven rows, all
  `taken`, each with the test that holds it.

## Decisions and preferences

- The maintainer's ten decisions and the Q-7 base refinement are recorded in
  `plans/changes/interview-minimums/decisions.md`; nothing was asked twice.
- The ADR question of this change was answered "no" as stated by the
  maintainer and is recorded in
  `decisions/answers/interview-minimums/adr.yaml`; this pull request is
  therefore a **decision pull request** (title `decide(workflow): …`, label
  `decision`, body from `.github/PULL_REQUEST_TEMPLATE/decision.md`).
- Accepted limits, stated in the pull request: a multi-commit direct push to
  `main` shows only its last commit to the gate (RB-M6 makes that path a
  pull request anyway), and the `goes_red` mutation test deliberately
  resembles its neighbour — the ratchet's price.

## Parallel sessions and ownership

- Only this session wrote bead `coding-harness-6yg` and the files of
  `plans/changes/interview-minimums`. `.claude/worktrees/stage2-mimo`
  (OpenCode) and `mimo-watch-audit` were not touched; no other bead was
  claimed, closed or reprioritised.

## Resume

The maintainer reads the decision pull request and merges it — or comments.
After the merge: archive `plans/changes/interview-minimums/` per
`plans/_README.md`, close the bead (`tools/bd close coding-harness-6yg
--reason=…`), `tools/bd dolt push`, then delete the worktree. Nothing else is
open on this change.
