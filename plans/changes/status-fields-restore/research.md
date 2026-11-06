---
title: "Research — status-fields-restore"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-ljmi
owner: Data Architect
provenance: human-written
tags: [research]
---

# status fields restore — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-06: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 909 files, 3351 commits, 12 rules.

## Runner exploration — 2026-11-06

The exploration is complete. Here is the research, ready to append to `plans/changes/status-fields-restore/research.md`.

---

**Proposed `neighbours:` header value:** `plans/changes/repair-restore-status/spec.md`, `plans/changes/repair-fixed-lines/spec.md`, `plans/changes/stage2-repair/spec.md`

## What exists today

**The bead and its only in-repo description.** The change belongs to bead `coding-harness-ljmi` (`plans/changes/status-fields-restore/research.md` frontmatter, `plans/INDEX.md` line 412: draft / none). The only statements the repository carries about it are in the night-run plan of 2026-11-03 (`docs/research/2026-11-03-night-run-plan.md`, the lanes table line 39 and the backlog table line 53): "Runner puts back status fields after a repair (bead coding-harness-ljmi): explore only; implementation after lane C, for `scripts/stage2.py`". The same plan (rules section, "Backlog added") declares every backlog item a `bounded` change that explores through GLM 5.3 Flash and stops at the interview, and orders the implementation after lane C (bead `coding-harness-4tr4`) because both touch `scripts/stage2.py`. The change folder was opened with commit `64d34bcd` ("chore(status-fields-restore): open the change folder", branch `fix/status-fields-restore`). The research frontmatter carries no `class:` field yet; the night-run plan is the only class declaration on record.

**Two different "status field" systems exist, and the bead's title fits both readings.**

*System 1 — the stage-2 row cells.* A stage-2 finding row has nine cells, ten in a released block (the extra `Phase 6` cell): the headers are `ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test` (`templates/findings.md`, "Stage 2" section). The Status vocabulary is `taken — <reason>`, `taken — not a test — <reason>`, `taken — guard test — <reason>`, `fixed — tests/<path>::<function>`, `fixed — not a test — <reason>`, `fixed — guard test — tests/<path>::<function>`, `rejected — <reason>` (`templates/findings.md`, same section). The rows live in three places: the loop record outside the repository (`${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/…`, `plans/changes/stage2-repair/spec.md` §Terms "Loop record"; the 2026-11-03 handover shows `change@commit`-shaped folders such as `guard-test@8d312694`), the released block of `findings.md`, and its phase-6 table (same spec, §Terms). The `Broke a test` mark is what decides a fixed row: `undecided` (`scripts/stage2.py`, symbol `undecided`, docstring) says "the orchestrator writes the mark after the repair, before the next round or the release (spec, criterion 25)", and the refusal in `undecided_refusal` names the allowed values (`yes`, `no`, `yes — <reason>`, `no — <reason>`). A fixed row still counts as accepted: `accepted_row` treats `taken` and `fixed` alike, "a repair preserves the fact that the review accepted the finding" (`scripts/stage2.py`, symbol `accepted_row`, docstring citing criterion 11).

*System 2 — the frontmatter pair.* Every `plans/` artefact carries `status` (moves when the project decides) and `implementation_status` (moves when the code moves) — `plans/_README.md` §Frontmatter and `docs/WORKFLOW.md` §"The plans tree". `scripts/plans_registry.py` validates both (symbol `REQUIRED`; the `done`-but-not-archived drift check; the D4 check that `partial`/`done` demand a `plan.md`) and renders them into `plans/INDEX.md`. No runner verb writes `implementation_status` anywhere: the only occurrence in `scripts/stage2.py` is the `none` seeded into a new findings.md (`findings_header`), and `scripts/new_change.py` seeds `none` for new change folders. Nothing in the runner ever moves these fields; the archive proposal document says a decision pull request sets `accepted` / `done` (`docs/research/2026-10-19-archive-proposal.md`, "The table" and the paragraph after it).

**Who writes the row statuses today.** Two writers. The orchestrator, for a hand repair: it sets the Status cell to one of the three fixed statuses *and* the `Broke a test` cell from the evidence, after backing up `loop.md`; otherwise the next round refuses with "taken rows are not repaired yet" (`docs/WORKFLOW.md` §4, "Hand repairs by the orchestrator"). The runner, during `repair <change>`: `mark_repaired_findings` rewrites only the Status cell (index 7) of the taken findings.md rows, between the post-run checks and the checkpoint commit — the `repair` verb wires it as `before_commit` (`scripts/stage2.py`, symbols `mark_repaired_findings` and `repair`, docstring "Only the Status cell (index 7) of a taken row changes"); `mark_repaired_record` rewrites the record's rows after the commit — wired as `after_commit` — writing the Status cell *and* the last-cell mark (`scripts/stage2.py`, symbols `mark_repaired_record`, `_mark_record_rows`, line where `mark = (marks or {}).get(cells[0], cells[-1])`). A record-marking failure is reported, not retried: "mark <ids> by hand" (`_mark_record_rows` and its caller, both `raise CallFailed`). The marks come from `check_repair_answer`, which returns the fixed statuses and the `Broke a test` marks its own evidence proves (red-first run, guard-test double proof, or `no — not a test`).

**The put-back paths that already exist** (all inside `run_attempts`, `scripts/stage2.py`, and shared by `implement` and `repair`):

1. *Failed attempt:* every attempt snapshots findings.md before the model call (`snapshot_findings`; `repair` and `implement` both pass it) and puts it back whenever the attempt fails — on a failed call, on a moved HEAD, and on the retry path after failed post-run checks (`put_findings_back` and the restore loops; docstring: "the model's own edits to the file - a Status it wrote itself included - go, so no failed run leaves them behind (phase 6, F-2)").
2. *Refused checkpoint commit:* when `checkpoint` raises `CheckpointRolledBack` after `mark_repaired_findings` wrote statuses, findings.md is put back to the snapshot — but only while no commit exists, and never after a `Refused` stop; the code comment names bead `coding-harness-rcyf` ("`before_commit` may have written statuses (a repair's `fixed — <test>`) that the refused commit's restore just undid the work for; findings.md is kept by that restore, so it goes back here").
3. *Moved HEAD:* the model's files are measured first, then findings.md is restored alone, "so its own statuses go and the audit stays" (the HEAD-stop branch in `run_attempts`).
4. *The guard:* `check_repair_answer` requires every findings.md row to stand cell for cell as it stood before the repair, taken rows' Status cells excepted — "the runner restores an edit outside the taken rows' Status before this check (spec, criterion 8)" (docstring); `findings_body_problem` protects the whole file apart from the runner's one `updated:` refresh.
5. *Release reconciliation:* when `release-loop` finds the record already released, it re-reconciles the standing block because "Repair may have changed Status cells" (`scripts/stage2.py`, symbol `release`, comment before the atomic block replacement).

**Existing test evidence** (`tests/test_stage2.py`): `test_a_passing_repair_ends_in_one_checkpoint_commit_with_its_statuses`, `test_a_failed_repair_writes_no_fixed_status`, `test_a_failed_repair_puts_every_status_back_as_it_stood` (docstring "Phase 6, F-2"), `test_a_credential_refusal_puts_the_original_statuses_back`, `test_guard_repairs_write_statuses_and_marks_only_after_complete_proof`, and `test_repair_refuses_legacy_completed_taken_statuses_before_call`.

**The nearest neighbours.** `plans/changes/repair-restore-status/spec.md` (bead `coding-harness-rcyf`, delivered by PR #240 per `docs/journal/handover/2026-10-25-cloud-runner-fixes.md`) already specifies exactly one put-back: findings.md goes back when the commit guard refuses a passing repair, "so no row stays `fixed` by a test the restore removed". `plans/changes/repair-fixed-lines/spec.md` (bead `coding-harness-ugi`) fixed the answer parsing and made hand repairs use the same `fixed — …` vocabulary, including the orchestrator's `Broke a test` mark. `plans/changes/stage2-repair/spec.md` (bead `coding-harness-g2f`, ADR 0015) is the base contract of the repair verb: the three row places, the refusal rules, and the fixed-line forms. `docs/WORKFLOW.md` §4's repair section (1555–1570 region) and the hand-repair doctrine (1671–1700) carry the same rules as prose; `prompts/04b-review-loop.md` steps 2–3 state that the runner writes each row's Status and the orchestrator writes `Broke a test` from the run's evidence.

## Where it lives

- `scripts/stage2.py` — `repair_targets` (which rows are taken, per place), `repair` (the verb: refusals, routes, wiring of `before_commit`/`after_commit`/`snapshot_findings`/`restore_findings`), `check_repair_answer` and `findings_body_problem` (the cell-for-cell guard), `mark_repaired_findings` (findings.md Status cells), `mark_repaired_record` / `_mark_record_rows` (record Status cells plus marks), `run_attempts` (snapshot, `put_findings_back`, the `CheckpointRolledBack` and moved-HEAD restores), `undecided` / `undecided_refusal` (the mark decides a fixed row), `accepted_row`, the `REPAIR_ANSWER` / `REPAIR_FORMAT` prompt constants, `findings_header` (the frontmatter seeding).
- `tests/test_stage2.py` — the repair status tests listed above.
- `docs/WORKFLOW.md` §4 — the repair section and "Hand repairs by the orchestrator"; `prompts/04b-review-loop.md` steps 2–3; `templates/findings.md` Stage-2 section.
- `scripts/plans_registry.py`, `scripts/new_change.py`, `plans/_README.md`, `plans/INDEX.md` — the frontmatter pair and its gate.

## What is unclear about it

1. **The bead's own defect statement is not readable from this worktree.** The tracker is the Dolt database under `.beads/` of the main checkout, transported via `refs/dolt/data` (AGENTS.md house rule 2); no rendered copy is committed, and the explorer reads nothing outside this worktree. What the repository does carry (night-run plan lines 39 and 53, `plans/INDEX.md` line 412, the research frontmatter) holds only the title, the scheduling and the class context — no symptom, no incident. "Not found in this worktree" and "not in the tracker" are different statements; only the first is made here.
2. **Which "status fields" the title means is not stated anywhere in the repository.** The row cells (System 1) and the frontmatter pair (System 2) both exist and both have unautomated corners. The verb "puts back" reads as restoring lost values, which fits System 1's restore family; System 2's fields are never written by the runner at all, so there is nothing to put back today. The interview should settle the reading.
3. **Candidate residual loss paths found in the code** (facts about the current mechanism, each needing the interview to confirm or drop):
   - Findings.md rows receive the Status cell but never the `Broke a test` mark: `mark_repaired_findings` writes only index 7, while `_mark_record_rows` writes the mark into the record. After a runner repair of released or phase-6 rows, findings.md carries `fixed — …` with an untouched mark cell, whereas a hand repair sets both cells (`docs/WORKFLOW.md`, "Hand repairs by the orchestrator"). Whether any consumer needs the mark in findings.md is unverified — `undecided` reads record rows, `repair_targets` reads only Status cells.
   - A drifted row is silently skipped: `mark_repaired_findings` marks a row only when its whole cell list still equals what `repair_targets` read; a row that changed in between is left as it stands, with no refusal and no report, and the checkpoint commit proceeds.
   - A failed record marking leaves the record's statuses unwritten and only names the ids (`_mark_record_rows`' `CallFailed` paths); the next `repair` then re-repairs, because `repair_targets` still sees `taken` there.
   - The `CheckpointRolledBack` and moved-HEAD restores remove the statuses deliberately, and the record keeps none either because `after_commit` never ran, so both places agree on `taken` — that is the delivered, specified behaviour (`plans/changes/repair-restore-status/spec.md`, criteria 1–2), not a gap.
4. **The motivating incident is not on record here.** The closest recorded observation is the 2026-11-02 handover lesson "Hand repairs need the `Broke a test` cell" (a loop row set to `fixed` by hand without that cell refused the next round on lane C; `docs/journal/handover/2026-11-02-five-lane-night.md`, "Lessons for the run plan"). No file names an incident for `coding-harness-ljmi` itself; the bead was created by the orchestrator on 2026-11-03 about 16:10 UTC from that night's experience.
5. **Overlap with the delivered neighbour must be ruled out.** Bead `coding-harness-rcyf` already delivered one status put-back (the refused-commit path, PR #240). If the new bead's case turns out to be the same path, the change duplicates delivered scope; the interview must name the differing case.

## Which files a change would have to touch

- `scripts/stage2.py` — the marking and restoring functions named above (`mark_repaired_findings`, `mark_repaired_record`, `_mark_record_rows`, the restore branches of `run_attempts`, `repair`), plus the `REPAIR_ANSWER` / `REPAIR_FORMAT` prompt constants if the contract text moves; this is the file the night-run plan names as the implementation target.
- `tests/test_stage2.py` — the repair status tests and the change's own new tests.
- `docs/WORKFLOW.md` §4 and `prompts/04b-review-loop.md` — if the responsibility split between runner and orchestrator (who writes Status and `Broke a test`, and when) changes.
- `templates/findings.md` — only if the Status vocabulary itself changes.
- `plans/INDEX.md` — regenerates through `scripts/plans_registry.py --index`; never typed by hand.
- Frontmatter of this change's artefacts — the `class:` header still needs to be declared consistently for the runner's routing checks.
