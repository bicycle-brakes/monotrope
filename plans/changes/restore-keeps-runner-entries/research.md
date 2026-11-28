---
title: "Research — restore-keeps-runner-entries"
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
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-28", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# restore keeps runner entries — Research

## Topic (bead coding-harness-7awf)

Class: bounded. Seen twice in fail-fast-attempts (bead coding-harness-5tyh, loop rows L1-2 and L9-3): when the runner restores findings.md after an attempt that edited a protected file, it also drops the entries the runner itself wrote (scan/audit lines). Case repair ended at the second case; needs a structural fix (restore only model-written content, or re-append runner entries after the restore).

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-28: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM through Z.ai at its weekly limit until 2026-11-29 · leak check clean over 1325 files, 6182 commits, 12 rules.

## Runner exploration — 2026-11-28

Research for `restore-keeps-runner-entries` (bead `coding-harness-7awf`), read-only, no commands run. Sources are named by file and symbol. Nothing was executed, so no test result is claimed.

## What exists today

**The restore of `findings.md` after a rejected attempt.** In `run_attempts` (`scripts/stage2.py`), the runner takes a snapshot of `findings.md` before the model call (`kept = snapshot_findings()`, and `findings_before = ctx.findings.read_bytes()` just after it). After the call it reads the bytes the attempt left (`findings_after_call`) before any runner write. It then runs `remove_changed_credential(..., findings=ctx.findings)`. Only if the attempt edited the file (`findings_after_call != findings_before`) does it call `restore_findings(kept)`. That writes the pre-call snapshot back over the whole file. Both the `implement` and `repair` verbs pass the restore callback: `implement` through `restore_work_input(root, ctx.findings, text.encode("utf-8"))` (around `scripts/stage2.py:13063`), and `repair` the same way (around `:13849`).

**The runner's own entries.** `remove_changed_credential` (`scripts/stage2.py`, around `:7693`) writes a `> credential scan skipped <path>: …` record into `findings.md` through `record_credential_scan_skips` (around `:7742`) whenever it cannot inspect a changed path's parent. That is the only runner-written line in this path that I traced. The same function runs again at other call sites in `run_attempts` (around `:12498`, `:12524`, `:12635`, `:12807`) and in the repair path (around `:13420` and `:13486`).

**The guard that accepts those records.** `only_scan_records_added` and `findings_body_problem` (`scripts/stage2.py`, around `:10748` and `:10759`) treat an added `> credential scan skipped ` line as bookkeeping rather than an edit, and the repair check uses the same guard (around `:10862`).

**Earlier review rows.** The fail-fast-attempts change (archived at `plans/changes/archive/2026-11-06-fail-fast-attempts/`) carries row L9-3 in its `findings.md`. It records the mechanism, and it says the case repair ended there and the structural remedy goes to the maintainer as a follow-up. Row L5-4 records the same shape. It was rejected, because the second scan after the diagnostics block re-appends the record before the checkpoint. The comment in `scripts/stage2.py` about the L1-2 and L5-3 rows matches this. The change's own `decisions.md` names the two remedies from the bead: restore only model-written content, or re-append the runner's entries after the restore.

**Existing tests.** `tests/test_stage2_fail_fast.py` contains three tests that touch this path:
- `test_the_runners_scan_record_is_not_an_attempt_edit` (row L1-2): the runner's record must survive and must not be credited to the attempt.
- `test_a_forged_scan_record_is_restored_away` (row L5-3): a forged line of the same shape is restored away.
- `test_a_genuine_scan_record_survives_the_restore_of_an_edit` (row L5-4): a genuine record survives when the attempt also edited the file.

## Where the mechanism lives

- `scripts/stage2.py`: `run_attempts` (restore and scan order), `remove_changed_credential`, `record_credential_scan_skips`, `only_scan_records_added`, `findings_body_problem`, the implement callbacks near `:13035`–`:13063`, and the repair callbacks near `:13786`–`:13849`.
- `tests/test_stage2_fail_fast.py`: the three tests above.

## What is unclear

- **Order of the audit line.** I read that the restore (around `:12570`) comes after the first scan (around `:12524`). I did not trace where this attempt's audit line is written. The bead names "scan/audit lines", so whether an audit line is also lost is not established.
- **Repair path.** The repair snapshot (around `:13786`) and its restore (around `:13849`) have the same shape. I did not trace whether a credential scan runs between them, so whether the repair path loses records the same way is not established.
- **Current test status.** I could not run the tests (read-only). Row L5-4's record of a pass dates from 2026-10-29 and predates any later change to `scripts/stage2.py`. Whether the three tests pass on this branch today is not established.
- **Second scan.** The survival of the record in the L9-3 case depends on a second scan that re-appends it. I did not trace that call site's exact position relative to the restore, so the claim rests on the row's own description.
- **Header.** `research.md` carries no `neighbours:` header. The swarm needs one, so the runner's `prepare-explore` step will refuse until it is added. Known neighbours: `plans/changes/archive/2026-11-06-fail-fast-attempts/` (its spec, decisions and findings), and `tests/test_stage2_fail_fast.py`.
