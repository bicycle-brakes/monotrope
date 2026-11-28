---
title: "Findings — restore-keeps-runner-entries"
category: findings
status: draft
implementation_status: none
date: 2026-11-28
created: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-7awf
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — restore-keeps-runner-entries

Stage-2 call, 2026-11-28: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1325 files, 6183 commits, 12 rules.

Stage-2 call, 2026-11-28: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1328 files, 6184 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-28

Spec fingerprint: sha256:579547cd8068e287946392ca7c91203769870bbd0760f23ff014848f0cee7de7

Spec review commit: 20182e5aee6b95305cc5a7485c0fea6f512ca318

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | [AMBIGUITY] | SPEC | base | spec.md, criterion 1 and its *Refuted by*; `scripts/stage2.py:12879`, `:12883`, `:12885`, `:12931`–`:12932` | The spec does not say which runner writes count as a "runner-written record". Reading A: only the `> credential scan skipped` records, the one runner line the research traced in that interval. Under A, the `CheckpointRolledBack` restore at `:12932` still erases `FINDINGS_RESTORED_NOTICE`, the restoration line and the record from the checkpoint scan (`:9865`). Reading B: every write the runner makes to findings.md (audit line, attempt block, restore notice, restoration line, and the `fixed —` statuses that `before_commit` writes). Under B, the same restore at `:12932` would have to keep the repair statuses that bead coding-harness-rcyf requires it to remove. The "audit record" in the refutation names nothing the research found written between the call and the restore. | Opus | in spec — reading B (every runner-written line survives); [DETAIL] S-1..S-6 (bounded standing grant) | — |
| S-2 | [AMBIGUITY] | SPEC | base | spec.md, summary line and criteria 1–3; `scripts/stage2.py:12293`–`:12307`, `:12527`, `:12618`, `:12706`–`:12707`, `:12776`, `:12932` | The spec does not say which restorations are covered. Criteria 1–3 apply only when "an attempt edits findings", which matches the edit-triggered restore at `:12570`. But `put_findings_back` restores the snapshot on every failure, whether or not the attempt touched findings.md (`:12527` credential found, `:12618` verifier refused, `:12776` any failure). The parent-gone batch at `:12706` writes `findings_before`, and `:12932` restores after the checkpoint scan. Reading A: only restorations of an attempt's edit preserve records. The record from the scan at `:12524` is then still erased at `:12527` and `:12618` when the attempt left findings.md untouched, and these are the exits where no later scan writes it again. Reading B: every restoration of findings.md preserves runner records, as the summary line ("Runner-authored findings survive restoration") states. | Opus | in spec — every restoration path covered; [DETAIL] S-1..S-6 | — |
| S-3 | MAJOR | SPEC | base | spec.md, criterion 1, *Refuted by*; `scripts/stage2.py:12807`; `tests/test_stage2_fail_fast.py:609` | Criterion 1 does not say when "absent after restoration" is checked. While the unsafe path stays changed, the scan at `:12807` appends the same skip record again after the restore. A check on the final file or the commit is therefore green on today's code. The existing `test_a_genuine_scan_record_survives_the_restore_of_an_edit` is such a check: it asserts on `HEAD`, and its plant writes the record on every scan call. The refuting state is only reachable right after the restore and before `:12807`, or on an exit with no later scan (`:12527`, `:12618`, `:12932`). The criterion names none of these, so a test that passes against today's code would meet it. | Opus | in spec — checked right after the restore, single-write plant; [DETAIL] S-1..S-6 | — |
| S-4 | MAJOR | SPEC | base | spec.md, criterion 5; `scripts/stage2.py:13769`, `:12498`, `:12521`, `:12635`, `:12804` | Criterion 5's repair half has no case that can refute it. Repair runs with `key = None` (`:13769`), and every scan in `run_attempts` only runs when `key is not None`, so a repair attempt never writes a scan record that a restore could lose. The research's "repair path (around :13420 and :13486)" is the draft verb's loop, not repair. With "audit record" undefined (S-1), there is no input under which repair "loses a genuine record". | Opus | in spec — criterion 5 covers draft and implement, repair out of scope; [DETAIL] S-1..S-6 | — |
| S-5 | MAJOR | SPEC | base | spec.md, criterion 4 and Open decisions [DETAIL]; `scripts/stage2.py:12524`, `:12569` | The spec does not say whether a record the scan produced must already be in findings.md when a safety refusal stops the run. Today the scan writes it at `:12524`, before the preflight at `:12569`, so it remains after a refusal. The [DETAIL] ("preserve trusted runner writes separately") allows holding the record and writing it only after the restore. Combined with criterion 4 (no write after a refusal), that design never writes the record on any refused restoration. Criterion 4's "additional findings write" also has no stated reference point: findings.md as it stood before the scan, or as it stood just before the refusal. | Opus | in spec — scan record written before preflight survives a refusal; [DETAIL] S-1..S-6 | — |
| S-6 | MINOR | SPEC | base | spec.md, criteria 1 and 5; `scripts/stage2.py:12776`, `:12807` | The spec does not say whether a kept record and the identical record the later scan writes may both remain. On a failure path the record is kept through the restore at `:12776`, the attempt block follows it, and `:12807` appends the same `> credential scan skipped` line again. Today that path ends with one copy. The implementer must decide whether the second copy is suppressed, and the spec is silent on it. | Opus | in spec — identical runner record not appended twice; [DETAIL] S-1..S-6 | — |
