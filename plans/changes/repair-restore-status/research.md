---
title: "Research — repair-restore-status"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-rcyf
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, repair]
---

# repair-restore-status — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md),
written by the orchestrating session at `origin/main` `f8a6b33`
(2026-10-25).

## The finding

On 2026-10-22 (pull request #158, repair after round 4), a Codex repair
attempt changed a human-written prompt. The runner refused the attempt and
restored the worktree, but `findings.md` kept the row's
`fixed — tests/test_research_handoff.py::test_yaml_answer_errors_are_not_measured`
although the restore had removed that test. The orchestrator reset the row
to `taken` by hand (bead coding-harness-rcyf).

## Cause, read and reproduced at `f8a6b33`

In `run_attempts`, a passing attempt runs `before_commit` first, which for
`repair` is `mark_repaired_findings`: it writes each taken row's `fixed —`
Status into `findings.md`. Then `checkpoint` runs the commit guard
(`uncommittable`). When the attempt changed a path a stage-2 run does not
commit, `checkpoint` restores the tree with `restore_baseline` but keeps
`allowed`, which holds `findings.md`, and raises `CallFailed`. Every other
failure path in `run_attempts` puts `findings.md` back with
`restore_findings(kept)`; this one did not. A test that plants a change to
`model-endpoints.yaml` reproduces it without model calls.

## Options

1. Restore `findings.md` from the pre-call snapshot when `checkpoint`
   refuses, as the other failure paths do.
2. Undo only the Status cells `mark_repaired_findings` wrote.
3. Refuse up front a taken row whose fix lies in a path a stage-2 run may
   not write (the bead's "consider"): the runner cannot know where a fix
   lies before the attempt, so this is not a fix of the reproduced path.

Option 1 uses the existing mechanism and covers any write `before_commit`
makes.
