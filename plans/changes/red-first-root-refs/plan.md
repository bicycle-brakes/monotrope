---
title: "Plan — red-first-root-refs"
status: draft
implementation_status: none
date: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-dk0h
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, red-first, refs]
---

# Plan — red-first-root-refs

```text
For you:     Proofs refuse persistent changes to their private root references and name them.
Done when:   Root-reference regressions and existing reference guards pass, as does make verify.
Appetite:    4 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Detecting restored transient changes or changing proof outcome rules.
Pre-mortem:  suppose it failed: most likely because a multi-line or unsafe root reference escaped measurement.
Starts unless you say stop.
```

## Files and steps

1. Change `tests/test_stage2.py`: add the ledger's regressions first and demonstrate that the creation and multi-line cases go red on the current code. Parameterize the baseline and fixed proofs, and exercise both guard-test legs through their actual shared path; inject pre-existing private files after clone setup, so change and deletion are measured against the real pre-test snapshots.
2. Change `scripts/stage2.py`: extend both private snapshots to measure matching direct root entries as complete bytes, without using `rev-parse` for multi-line pseudo-refs; retain the existing logical `HEAD` treatment. Refuse unsafe nonregular or unreadable entries before Git or a byte reader can follow or block on them, and let the shared guard name all differences and clean up on failures.
3. Keep `_private_repository`'s source ref restoration independent of the new private-only snapshot data: `_ref_targets` is also used by clone setup, which must not feed arbitrary multi-line root-file bytes to `update-ref` or copy concurrent source pseudo-refs. Continue using `run_git` for Git launches, and preserve the existing comparison, scrubbing, packing and malformed `packed-refs` behavior.
4. Update `plans/changes/red-first-root-refs/spec.md`, `plans/changes/red-first-root-refs/plan.md` and `plans/changes/red-first-root-refs/findings.md` as the work advances; the orchestrator owns the derived `plans/INDEX.md` if regeneration is required. No living limit text was found in the 2026-11-22 search; leave archived findings and handovers unchanged.

Do not touch ADRs, prompts, templates, source-repository state, proof classification, unrelated Git metadata or other changes. No held path needs an implementation edit; the orchestrator alone handles any held path if one becomes necessary.

## Verification

```sh
.venv/bin/python -m pytest tests/test_stage2.py -q
python3 scripts/check_interview_minimums.py --change red-first-root-refs
python3 scripts/check_criterion_ledger.py
python3 scripts/plans_registry.py --check
make verify
```

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_proofs_refuse_created_root_refs — creation of ORIG_HEAD, AUTO_MERGE or another matching name is accepted or unnamed.
- 2: not yet written tests/test_stage2.py::test_proofs_refuse_changed_multiline_fetch_head — changing a later FETCH_HEAD line is accepted or unnamed.
- 3: not yet written tests/test_stage2.py::test_proofs_refuse_deleted_root_refs — deletion of a pre-existing private ORIG_HEAD is accepted or unnamed.
- 4: not yet written tests/test_stage2.py::test_proofs_accept_unchanged_root_refs — an unchanged multi-line FETCH_HEAD refuses an otherwise qualifying run.
- 5: not yet written tests/test_stage2.py::test_proofs_refuse_unsafe_root_refs — FIFO, symlink or read failure is followed, blocks, is accepted, or prevents cleanup.
- 6: not yet written tests/test_stage2.py::test_proofs_ignore_source_root_ref_changes — a concurrent source FETCH_HEAD write invalidates a private proof or the proof writes the source.
- 7: tests/test_stage2.py::test_proofs_accept_packing_unchanged_refs — packing logically unchanged ordinary refs refuses the proof.
- 8: not yet written tests/test_stage2.py::test_private_ref_snapshots_measure_root_refs — either snapshot misses creation or a later FETCH_HEAD line change.

## Time used

2026-11-22 08:31:48–08:34:17 UTC, 149 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
