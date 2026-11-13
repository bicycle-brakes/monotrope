---
title: "Research — no-work-ledger-marker"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-11
supersedes: null
superseded_by: null
bead: coding-harness-twbl
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, model: glm-5.3-flash, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
class: bounded
tags: [research]
neighbours:
  - plans/changes/no-work-done/spec.md
---

# no work ledger marker — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md). The
intent below was written by the orchestrator (Claude Code) before the first
call; the runner exploration (GLM 5.3 Flash) follows it unchanged.

## Intent of the bead (written by the orchestrator before the first call)

Bead coding-harness-twbl, class bounded, a follow-up of phase-6 finding F-1
of the change no-work-done (bead coding-harness-te7q, merged with pull
request #360 on 2026-11-10). The no-work check rejects an implement or repair
attempt that changed only the runner's own bookkeeping. The gap: a rejected
attempt leaves a new test; the retry restores the ledger marker `not yet
written`; verification clears the marker again; and the path-only candidate
filter counts that ledger edit, which the runner itself made, as work of the
model. The finding was reproduced in memory with `clear_written` and
`attempt_has_work`. Wanted: the clearing of a ledger marker by the runner is
discounted before the check decides whether there was work; a retry whose
only change is that clearing is rejected as no work done.

Questions for the exploration: where `attempt_has_work`, `clear_written` and
the candidate filter live in `scripts/stage2.py` and in which order they run
within one attempt; which other runner-owned writes the check already
discounts and how (findings file, plan index, stamp-only edits, the plan's
time section); which tests of `tests/test_stage2.py` pin the check; what the
spec of no-work-done states about this accepted limit.

Stage-2 call, 2026-11-10: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1007 files, 3892 commits, 12 rules.

## Runner exploration — 2026-11-10

The exploration is complete. Here is the research, ready to append to `plans/changes/no-work-ledger-marker/research.md`.

---

## What exists today

**The no-work check.** `NO_WORK = "no work done"` is a module constant in `scripts/stage2.py`, directly above `attempt_has_work(root, before, after, findings, plan, *, model_after=None)` (same file). Its docstring: "Measure surviving model work after verification, excluding writes the runner owns." The only production call site is inside `run_attempts` (the attempt loop both verbs share: `implement` and `repair` each call `run_attempts`); it is called after verification as `attempt_has_work(root, before, worktree_tree(root), ctx.findings, ctx.plan, model_after=after)`. The draft verb's own route loop measures files with `attempt_files` for the attempt block only and has no `attempt_has_work` use — one call site, in `run_attempts`, is the whole production surface.

**The four discounts the check applies today**, in `attempt_has_work` itself:

1. *The candidate filter (path-only)* — with `model_after` given, the candidate set is built from `git diff-tree -r -z --name-only --no-renames` between `before` and `model_after` (the post-call snapshot), and any changed path not in that set is skipped with `continue`. The filter compares paths, not content: once a path is a candidate, every surviving change to it inside the attempt window counts for the model.
2. *Runner-owned records* — the findings file and `plans/INDEX.md` are skipped wholesale by path.
3. *Stamp-only edits* — a same-mode content modification whose only difference is the frontmatter `updated:` line is skipped via `_mask_stamp(..., dated=False)` on both blobs; this covers malformed replacement values and stamps on any document (`_mask_stamp` docstring; test `test_stamp_only_work_discount_is_symmetric`).
4. *The plan's time body* — for the plan path, `_minus_time_body` (which cuts the body of `## Time used` using `time_records.TIME_HEADING` and `FOLLOWING_HEADING`) makes a plan whose only change is time records a skip; a stamp-masked plan body is skipped too.

**The order within one attempt**, all in `run_attempts` and `verify_attempt`:

1. Attempt start: `baseline_time` (the plan's text as it stands), `inputs_before`, and `lifecycle_before = lifecycle_snapshot(ctx.folder)` — whole-document bytes of the lifecycle docs, from which `restore_lifecycle_fields` restores trusted *frontmatter* only; the `not yet written` marker in the `## Criterion ledger` body is not a lifecycle field and is not restored there.
2. `before = worktree_tree(root)` — the comment at the second snapshot says it outright: "Both snapshots stand around the model call alone: the runner's own writes … fall outside both of them."
3. The model call.
4. `after = worktree_tree(root)` — later passed as `model_after`, so it defines the candidate set.
5. Credential scrub (`remove_changed_credential`), then `restore_attempt_lifecycle()` → `restore_lifecycle_fields` (frontmatter fields back).
6. `verify_attempt`: alias/hard-link refusals for the plan → `format_step` → `cheap_checks` → `check_criterion_ledger.clear_written(root, plan)` → `prepare_derived` (stamp held documents, render the index) → intent-to-add and `make verify` (full mode) or the targeted selection (repair mode). The clearing's origin is bead coding-harness-7g6h; the comment in `verify_attempt` says "The marker of a test the attempt wrote is derivable, so it is not the attempt's to forget."
7. The work measurement (step: `attempt_has_work`, above), whose verdict leads `problems`; the comment there says an attempt without work is rejected whatever verification said and the answer check below never runs.

**The ledger clearing itself.** `check_criterion_ledger.clear_written(root, plan)` in `scripts/check_criterion_ledger.py` replaces `: not yet written ` with `: ` on every ledger entry whose named test file and function exist in the tree; fenced lines and entries whose test is missing keep the marker; plan.md is written only when something was cleared. Two tests pin the ordering: `test_the_ledger_is_cleared_after_formatting_before_stamping_and_verify` (clearing follows Ruff's normalization, precedes stamping and `make verify`) and `test_the_ledger_is_cleared_before_the_documents_are_stamped`.

**Where the marker comes back for a retry.** On a rejected attempt that still has a route, `persist_time_entry(..., retry=True)` writes the plan as the pre-call text plus the one new entry — its docstring: "`retry` persists the entry on the pre-call plan", and the call-site comment: "A rejected attempt that will be retried gets its plan back at the pre-call bytes plus this entry, so the restore below keeps the entry and drops the model's other plan edits." Since the pre-call bytes carry the marker, the clearing a rejected attempt's verification made is undone at the retry boundary while a newly written test file stays in the tree — the two halves of F-1's first sentence.

**The mechanism, restated against the current code.** In the retry: the model call changes only discarded time-body text on plan.md, so plan.md is in the candidate set (the filter is path-only). Verification's `clear_written` then clears the marker — the test file from the rejected attempt still exists, so the entry qualifies. That clearing is a plan-body change outside `## Time used` and not a stamp, so discounts 3 and 4 do not cover it, and `attempt_has_work` returns True. The model's own change is discounted by `_minus_time_body`; the only surviving difference is the runner's own ledger edit, counted as model work. This matches finding F-1, which recorded an in-memory reproduction using the actual `clear_written` and `attempt_has_work` returning True "despite no model change outside the time body."

**Where F-1 and its status live.** `plans/changes/no-work-done/findings.md`, phase-6 table, row F-1 (MAJOR, SPEC, reviewer Codex), status: "accepted limit — follow-up bead coding-harness-twbl (maintainer 2026-11-09: PR now, MAJOR as follow-up bead)". Its `Where` cell cites `scripts/stage2.py:4890–4899` — those numbers have aged; the function now stands at `attempt_has_work` as named above.

**What the no-work-done spec says.** `plans/changes/no-work-done/spec.md` does not state this accepted limit — searched for "marker", "criterion ledger" and "limit"; only the Non-goals section matches, and it names different limits (route order, verification commands, extending the check to other verbs). The limits that do bind the fix are the acceptance criteria: criterion 1 (an attempt without work against its attempt baseline is rejected; refuted-by list: no-edit, same-byte rewrite, findings-only, time-body-only), criterion 2 (real work passes regardless of kind or path, including plan prose outside the time body), criterion 4 (an all-empty run exits 1 without a checkpoint commit), criterion 6 (a measurement failure prevents acceptance rather than counting as work). "Attempt baseline" is defined in its terms section as the state immediately before the model call, "including earlier attempts' retained changes and runner records; an earlier attempt's work is not this attempt's work". The same rule is stated for readers in `docs/WORKFLOW.md`'s implement-loop passage ("The verdict measures surviving model work after formatting and derived preparation, discounting the generated index and stamp-only changes in any document … Each call is compared with its own pre-call state … rejected as `no work done` through the existing retry path"). A companion comment in the lifecycle-restore test pins the sibling rule: "an attempt whose only change is the restored fields leaves no model work and is rejected (no-work-done; maintainer 2026-11-09)".

**The tests that pin the check** (`tests/test_stage2.py`): the `NO_WORK_EDITS` table (no-edit, same-bytes, findings-only, time-body-only) with `test_no_work_attempt_is_rejected` (both verbs, HEAD unchanged, three NO_WORK occurrences), `test_discarded_model_changes_are_no_work` (held-stamp, index, format-only), `test_bookkeeping_scenario_has_no_implicit_work`, `test_no_work_diagnostic_names_the_verbs_contract`, `test_no_work_guard_detects_bypassed_check` (the STAGE2_PLANT_FAULT always-true predicate), `test_idle_retry_cannot_reuse_previous_work`, `test_work_check_accepts_nonempty_changes` (ten `WORK_EDITS` kinds, including plan prose, binary, file-mode), `test_stamp_only_work_discount_is_symmetric`, `test_work_check_uses_unbounded_changes`, `test_no_work_rejection_reaches_existing_retry`, `test_postverify_credential_refusal_has_no_no_work_diagnostic` (a credential refusal must skip the final tree snapshot and never produce a NO_WORK verdict), and `test_runner_accepts_attempt_without_model_time_entry` (the old model-added-time-line check is gone). The clearing side is pinned by `test_implement_clears_the_ledger_marker_of_a_test_the_attempt_wrote`, the two ordering tests above, and the alias/hard-link refusals (`test_clearing_the_ledger_refuses_an_aliased_parent_or_a_hard_link`, `test_clearing_the_ledger_never_writes_through_an_aliased_plan`). The affected plan-write path is additionally covered by the retry/time-entry machinery around `persist_time_entry`.

## What is unclear about it

- At byte level, a runner marker clearing and a model edit with the same result on the same path are indistinguishable through the path-only candidate filter; the exploration records the mechanism, not a choice between masking the exact lines `clear_written` would clear and narrowing the candidate filter for paths whose model-diff is fully discounted. Both would satisfy F-1's sentence "Discount ledger clearing before deciding work"; which one is a spec decision.
- The exact bytes of the retry plan write rest on `persist_time_entry`'s docstring and call-site comment; I did not read the bodies of `time_records.write_entry` and `stamp_updated`, which the retry branch calls.
- Whether the ledger gate (`check_criterion_ledger.run`) cares about a cleared-versus-kept marker mismatch after a discounted retry is not researched; I read only the helpers `clear_written` uses (`_lines`, `_fenced`, `ledger_sections`, `parse_entry`).
- "Not found" versus "not there": the accepted limit is recorded in `plans/changes/no-work-done/findings.md` only; a search of the no-work-done spec found no statement of it, so a spec-phase clarification there (if wanted) would be new text, not an edit of existing wording.

## Which files a change would have to touch

- `scripts/stage2.py` — `attempt_has_work` (the measurement and its discounts) and, depending on the shape of the discount, the call site inside `run_attempts` (to know what the clearing changed).
- `scripts/check_criterion_ledger.py` — if the discount needs to compute the clearing without writing, a read-only counterpart beside `clear_written` lives there.
- `tests/test_stage2.py` — a regression beside the no-work block (the `NO_WORK_EDITS` table through `test_postverify_credential_refusal_has_no_no_work_diagnostic`) and beside the ledger-clearing tests (`test_implement_clears_the_ledger_marker_of_a_test_the_attempt_wrote`).
- `docs/WORKFLOW.md` — the implement-loop paragraph that enumerates the discounts (findings and time body, index, stamp-only, per-call baseline).
- Possibly `plans/specs/implementation-verification/spec.md`, whose criterion 1 already names the no-work check and the runner-owned bookkeeping.
- The change's own artifacts under `plans/changes/no-work-ledger-marker/`, with `plans/INDEX.md` regenerated by the runner. The no-work-done artifacts are accepted history and stay untouched; its criteria 1, 2, 4 and 6 remain the contract the fix must hold.

## Draft-stage repository checks — 2026-11-10

Read against input commit `c54bbdd5`; these checks resolve repository gaps,
not maintainer decisions:

- Ledger clearing has two verification paths: `verify_attempt` calls it in
  full mode, while `_targeted_body` calls it before selecting targeted checks
  or falling back to full verification. Both need the same attribution.
- `persist_time_entry`'s retry branch actually calls
  `time_records.write_entry(..., text=prior, publish=restore)`, stamps the
  recovered plan and updates the retry input bytes. Thus the plan body comes
  from pre-call text, not from the failed attempt's cleared ledger.
- `clear_written` returns criterion numbers, not unique entry identities;
  several entries may name tests for one criterion. A discount needs the
  actual changed entries, not merely those numbers or later eligibility.
- No `templates/plan.md` or `scripts/validate_change_artefacts.py` exists in
  this input tree. The phase-3 prompt supplies the plan form; interview,
  criterion-ledger and registry checks are present.
