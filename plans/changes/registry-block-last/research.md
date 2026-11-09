---
title: "Research — registry-block-last"
status: draft
implementation_status: partial
date: 2026-11-03
last_reviewed: 2026-11-03
updated: 2026-11-03
supersedes: null
superseded_by: null
bead: coding-harness-2g7y
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-03"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, verification, stage-2]
---

# registry-block-last — Research

Measured by the orchestrator on 2026-11-03 (no explore run: the cause was
found while diagnosing a failed repair; bead `coding-harness-2g7y`).

- The stage-2 runner shows a repairing model only the last lines of a red
  gate (`verify_evidence` in `scripts/stage2.py`, "[… N lines of this gate
  left out …]").
- `scripts/_verdict.py` `Verdict.render()` prints BLOCK first, then DRIFT,
  then INFO. `scripts/plans_registry.py --check` reports 261 DRIFT findings
  on `origin/main` at `b424be3a` and 317 on `feat/guard-test` (2026-11-03),
  so a BLOCK line never reaches the tail.
- Recorded cost on `origin/main` and the guard-test branch: the changes
  terms-test-fixtures (2 attempts), workflow-promises (2) and guard-test (3)
  failed on a plans-registry block whose reason the model never saw
  (`plans/changes/*/findings.md`, "[plans-registry] RED"). In guard-test the
  hidden line was `status 'in-review' is none of ['accepted', 'draft',
  'superseded']`, reproduced in a scratch worktree.
- Six scripts render through `_verdict.py`; `tests/test_pr_sync.py` and
  `tests/test_leakcheck.py` assert substrings of `render()`, none its order.
