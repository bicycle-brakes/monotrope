---
title: "Research — origin-check-across-blocks"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-3h96
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, model: glm-5.3-flash, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
class: bounded
tags: [research]
neighbours:
  - plans/changes/origin-cell/spec.md
  - plans/changes/repair-targeted-check/spec.md
---

# origin check across blocks — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

## Intent of the change — from the bead, 2026-11-10

Written by the orchestrator before the first exploration, because an
explorer cannot read the tracker (bead coding-harness-3h96).

Class: bounded.

The Origin check of the repair brake validates only the newest phase-6 block
of `findings.md`. Once a newer phase-6 block exists, an older phase-6 row
with an invalid Origin cell escapes validation: `origin_refusal(None, text)`
returns `None` while `repair_targets` still selects the earlier row. The
`repair` verb can then call a model on an accepted finding whose provenance
is invalid. This was phase-6 finding F-1 of the change origin-cell (bead
coding-harness-ywbh; Codex, 2026-11-09, reproduced with the source
functions); that change is merged (pull request #359).

Wanted: every outstanding repair target is validated across all phase-6
blocks before any effect — before a model call and before a write.

To explore: where `origin_refusal` and `repair_targets` live in
`scripts/stage2.py`, how each reads the phase-6 blocks, which tests pin the
Origin check today, and which other callers rely on the newest-block
reading.

Stage-2 call, 2026-11-10: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 993 files, 3828 commits, 12 rules.

## Runner exploration — 2026-11-10

Exploration complete. Here is the research, as prose ready to append to `plans/changes/origin-check-across-blocks/research.md`.

---

## What exists today

**The Origin check is newest-block only.** `origin_refusal(record, findings_text)` (scripts/stage2.py:3586, `origin_refusal`) finds every `## Phase 6` heading in findings.md with a regex and parses only the text from the **last** one onward (`heads[-1]`, scripts/stage2.py:3597-3598). An inline comment states this is deliberate: "A re-check supersedes earlier phase-6 blocks, even when the newest block has no rows. Do not change findings_rows: repair targeting and the brake still read their full history" (scripts/stage2.py:3595-3596). "Accepted" is `accepted_row` (scripts/stage2.py:3571): Status begins `taken` or `fixed`, case-insensitively; the vocabulary is `ORIGIN_VALUE = re.compile(r"base|fix-r[1-9][0-9]*")` (scripts/stage2.py:3583). The loop-record place has no such narrowing — `record_rows` (scripts/stage2.py:3473) reads every table line of the whole record.

**Repair targeting is all-blocks.** `repair_targets(ctx, record)` (scripts/stage2.py:3080) reads findings.md through `findings_rows` (scripts/stage2.py:3046), whose docstring says "Every released block and every phase-6 table is read", and returns every `taken` row from all three places (record, released, phase-6) plus the ids of undecided phase-6 rows. Its only caller is `repair` (scripts/stage2.py:9203; grep over `scripts/` found no other).

**The gap, mechanically.** `repair` (scripts/stage2.py:9189) computes `taken` first (9203), refuses undecided rows (9204-9205 — a `taken` row is decided, so this refusal cannot catch it), then calls `origin_refusal` (9207-9209), then refuses doubled ids and legacy fixed markers (9213-9226), and only then reaches the model attempts via `run_attempts` (scripts/stage2.py:9264) — the prompt embeds the selected rows under `## Taken rows` (`repair_prompt`, scripts/stage2.py:9180) — and the writes: `mark_repaired_findings(ctx, taken, fixes)` before the commit (scripts/stage2.py:9278, defined at 7399-7424) rewrites the Status cell of exactly the selected rows "in its place", walking the whole file by section, older phase-6 blocks included; `mark_repaired_record` follows after the commit (scripts/stage2.py:9279, defined at 7428). So an older block's `taken` row with an invalid Origin is selected, shown to the repair model, and written without ever being validated — phase-6 finding F-1 of the merged change origin-cell, accepted as follow-up bead coding-harness-3h96 (plans/changes/origin-cell/findings.md:377, reproduced there with the source functions: `origin_refusal(None, text)` returns `None` while `repair_targets` selects the earlier row).

**Why the check is narrow — the prior blocker.** The narrowing is the fix for L4-1, a BLOCKER of the same change: the first version scanned every phase-6 table on all four verbs and refused on decided rows released before the check existed, carrying reviewer-supplied Origins such as `impl` or `scope`; the only way past was hand-editing released history (plans/changes/origin-cell/findings.md:401). Two tests pin the narrow reading as intended: `test_legacy_released_origin_does_not_hold_verbs` (tests/test_stage2.py:8290-8317, parametrized over all four verbs × whether the newest block has a row) plants an **old phase-6 row with status `fixed` and Origin `impl`** plus a released row with Origin `diff reading` and requires exit 0 from every verb; `test_origin_release_controls_keep_distinct_validation_scopes` (tests/test_stage2.py:8371-8393) plants a superseded phase-6 block whose `fixed` row carries Origin `scope` and asserts "ordinary release must ignore superseded phase-6 provenance" (assertion at 8377), and proves `--restart`/`--stage-failed` never reach Origin validation by monkeypatching `origin_refusal` to fail the test if called (8382-8385). Both pin decided (`fixed`) rows; neither plants the F-1 shape (old block, status `taken`).

**Documented promises.** The Origin paragraph (docs/WORKFLOW.md:1583-1592) says the four verbs "refuse, naming the row and its place, while a taken or fixed row in the loop record **or a phase-6 table** carries any other value", then exempts released history and `--restart`/`--stage-failed`. Read literally, "a phase-6 table" names any table; the implementation reads only the newest. The repair section separately says `repair` "takes every taken row — of the loop record, of every released block and of every phase-6 table — to Codex in one guarded call" (docs/WORKFLOW.md:1645-1647). `test_origin_workflow_assigns_provenance_to_the_orchestrator` (tests/test_stage2.py:8252-8262) pins exact phrases of the paragraph ("also sets each accepted row's `Origin`", "`base` for a finding that existed before any repair and that no repair caused", "the orchestrator corrects the cell"), so paragraph edits must keep them.

**Where multiple phase-6 blocks occur.** Every re-check appends a new `## Phase 6` block and leaves older ones standing (superseding rule, scripts/stage2.py:3595; the rejected-answer block deliberately avoids a `## Phase 6` heading so it starts no re-check, `rejected_review_block`, scripts/stage2.py:3161-3178). Multi-block findings.md files are common: counting `^## Phase 6` over `plans/**/findings.md` gives 10 for `plans/changes/repair-targeted-check/findings.md`, 8 for `red-first-own-refs`, 5 for `status-fields-restore`, 4 each for `guard-test` and `swarm-test-speed`.

**Reachability.** `folder_of` (scripts/stage2.py:1406-1412) resolves only `plans/changes/<change>/`, so archived changes under `plans/changes/archive/` are unreachable by the verbs; the live form of the gap concerns active changes. Old phase-6 blocks with Status `taken` do exist in the tree — e.g. `plans/changes/archive/2026-11-06-pi-pin/findings.md` rows F-5–F-14 (lines 472-481) and `plans/changes/archive/2026-10-08-interview-minimums/findings.md` rows F-10–F-17 (lines 66-76); in every row I read there, the Origin cell is `base`, i.e. valid. Whether any **active** change holds an old phase-6 `taken` row with an invalid Origin was not measured exhaustively — not found in what I read is not "not there".

**Test infrastructure available.** The Origin test block lives at tests/test_stage2.py:8205-8500: `INVALID_ORIGINS` (8208), `ORIGIN_VERBS` (8209), `ORIGIN_PLACES = ("record", "phase-6")` (8210), `set_row_origin` (8214, record only), `plant_origin` (8226 — plants exactly **one** phase-6 block), `origin_state` (8243, findings.md + record bytes as the no-effect oracle), `phase6_cells`/`phase6_block` (9241/9251). No helper plants a second phase-6 block beside a first; the two legacy tests write blocks directly via `world.write_findings(...)` (8300, 8376).

## Where it lives

- `scripts/stage2.py` — `folder_of` 1406 · `findings_rows` 3046 · `repair_targets` 3080 · `record_rows` 3473 · `accepted_row` 3571 · `ORIGIN_VALUE` 3583 · `origin_refusal` 3586 · `fix_r_only` 3670 (repair brake, reads record rows only) · `check_repair_answer` 7222 · `mark_repaired_findings` 7399 · `mark_repaired_record`/`_mark_record_rows` 7428/7459 · `repair` 9189 · `review` 3271 · `release` 3961 · `review_loop` 9316. Callers of `origin_refusal`: review 3286, release 3967, repair 9207, review_loop 9339. Caller of `repair_targets`: repair 9203 only.
- `tests/test_stage2.py` — the Origin block 8205-8500; tests that must stay green: `test_invalid_accepted_origins_hold_all_consuming_verbs` 8265, `test_legacy_released_origin_does_not_hold_verbs` 8290, `test_uppercase_accepted_status_holds_invalid_origin` 8320, `test_origin_release_controls_keep_distinct_validation_scopes` 8371, `test_origin_refusal_identifies_rows_sources_and_correction` 8432, `test_valid_origins_preserve_existing_admission_checks` 8457, `test_nonaccepted_rows_need_no_origin` 8489, `test_origin_workflow_assigns_provenance_to_the_orchestrator` 8252.
- `docs/WORKFLOW.md` — Origin paragraph 1580-1602; "Repairing taken findings (repair)" 1637-1649; record-identity/Origin compatibility note 1618-1623.
- Predecessor artifacts: `plans/changes/origin-cell/` (research.md, spec.md, plan.md, decisions.md, findings.md) — F-1 at findings.md:377, L4-1 at findings.md:401, L4-3 (the restart/stage-failed boundary test's origin) at findings.md:403, L3-1 (maintainer's answer that accepted rows include `taken` and `fixed`) at findings.md:400.

## What is unclear about it

1. **Promise vs implementation.** Whether docs/WORKFLOW.md:1588's "a phase-6 table" should, after the change, name every table, only the newest, or only the outstanding repair targets, is an open wording decision; the pinned test phrases (tests/test_stage2.py:8252) constrain any edit. The pinned tests also show the maintainer's intent runs the other way for decided rows: superseded and legacy provenance must not hold verbs (8290, 8371).
2. **Where the widened validation can live without breaking pins.** Widening `origin_refusal` itself to all phase-6 blocks contradicts the assertion at tests/test_stage2.py:8377 for ordinary release and the 8316 exit-0 assertions; validating the rows `repair_targets` already selected, on the repair path alone, contradicts no test I read. I state the constraint, not the design.
3. **Live exposure today.** No exhaustive measurement exists of active changes carrying an old phase-6 `taken` row with an invalid Origin.
4. **Place naming.** A refusal naming an older block has no place word today: `origin_refusal`'s places are "loop record"/"phase-6 table" (scripts/stage2.py:3599-3602) and `repair_targets` returns "record"/"released"/"phase-6" (3093-3102).

## Which files a change would have to touch

- `scripts/stage2.py` — the validation window: `origin_refusal` (3586) and/or the pre-call sequence in `repair` (9203-9209); possibly the refusal text's place naming (3599-3615). The inline comment at 3595-3596 forbids solving this in `findings_rows` (3046); `repair_targets` (3080) is a read-only surface with one caller.
- `tests/test_stage2.py` — a guard test for the F-1 shape (old phase-6 block with a `taken` row of invalid Origin, newest block present and empty or rowless, `repair` must refuse before any model call or write) and likely a helper to plant multiple phase-6 blocks (8226 plants one). All eight green tests above bound the change.
- `docs/WORKFLOW.md` — the Origin paragraph (1580-1602) and/or the repair section (1637-1649), only insofar as the guarantee's wording moves.

**Suggested `neighbours:` entries for the runner:** `plans/changes/origin-cell/spec.md` (merged predecessor, PR #359) · `plans/changes/repair-targeted-check/spec.md` (repair targeted-check flow this verb runs) · `docs/WORKFLOW.md` (living spec carrying both paragraphs).
