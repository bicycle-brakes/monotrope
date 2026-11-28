---
title: "Plan — restore-keeps-runner-entries"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-7awf
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, runner]
---

# Plan — restore-keeps-runner-entries

```text
For you:     Runner records remain in findings when an attempt's edits are restored.
Done when:   Restoration, attribution and safety regressions pass for implement and repair, and make verify is green.
Appetite:    2 hours for phase 4 including repairs; stop at the limit.
Not now:     Changes to scan policy, attempt acceptance or record formats.
Pre-mortem:  suppose it failed: most likely because a forged record is mistaken for a runner write.
Starts unless you say stop.
```

## Build sequence

1. Change `scripts/stage2.py`: trace all `run_attempts` restoration branches for implement and repair, including refusal and repeated recovery, and preserve the actual runner-origin writes made after the snapshot across restoration without copying attempt-origin bytes. Keep recovery preflight and refusals ahead of writes, and avoid duplicating records on repeated restores; do not rely on a later scan to recreate a record.
2. Change `tests/test_stage2_fail_fast.py`: exercise both verbs with a genuine record written once between call and restore, an attempt edit including a forged scan line, and repeated restoration; verify the genuine record survives exactly once, forged content disappears, and runner-only writes do not count as edits. Exercise refusal without a subsequent findings write. Keep existing scan and attribution regressions.
3. Update the ledger in `plans/changes/restore-keeps-runner-entries/plan.md` when new tests exist. The runner records evidence in `plans/changes/restore-keeps-runner-entries/findings.md`; no file is deleted and no held path needs an implementation edit.

Explore used Stage 1 via `claude-code-plan`, model `claude-haiku-5-5`, because GLM through Z.ai had reached its weekly limit until 2026-11-29 (`research.md`, 2026-11-28).

## Criterion ledger

- 1: not yet written tests/test_stage2_fail_fast.py::test_runner_records_survive_restore_without_a_second_scan — restoring loses or duplicates the sole genuine record.
- 2: tests/test_stage2_fail_fast.py::test_a_forged_scan_record_is_restored_away — a forged scan line survives.
- 3: tests/test_stage2_fail_fast.py::test_the_runners_scan_record_is_not_an_attempt_edit — a runner-only record triggers an edit notice.
- 4: not yet written tests/test_stage2_fail_fast.py::test_record_preservation_respects_restoration_refusal — findings are written after a safety refusal.
- 5: not yet written tests/test_stage2_fail_fast.py::test_implement_and_repair_preserve_only_runner_records — either verb loses the genuine record or keeps an attempt edit.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2_fail_fast.py
python3 scripts/jobs.py start -- make verify
```

Check the detached verification job's exit with `python3 scripts/jobs.py list` before phase 6.

## Do not touch

Leave scan policy, record format, attempt acceptance and held paths unchanged.

## Time used

2026-11-28 04:08:04–04:09:50 UTC, 105 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
