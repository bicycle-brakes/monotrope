---
title: "Research — no-work-done"
status: draft
implementation_status: none
date: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-te7q
owner: Data Architect
provenance: human-written
tags: [research]
---

# no work done — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-07: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 922 files, 3570 commits, 12 rules.

## Runner exploration — 2026-11-07

The exploration is complete. Here is the research, ready to append to `plans/changes/no-work-done/research.md` (replacing the "this file is empty until it has run" placeholder line; per the skeleton's note the frontmatter then moves to `provenance: ai-drafted-reviewed` with `produced_by:` and `review:`).

**Suggested `neighbours:` header values:** `plans/specs/implementation-verification/spec.md` · `plans/changes/archive/2026-10-07-stage2-flash-runner/spec.md` · `plans/changes/archive/2026-10-08-runner-derived-files/spec.md` · `plans/changes/redraft-after-scope/spec.md`

---

## What exists today

**The bug this change owns.** The handover of the heartbeat night states it plainly: "the runner accepts an implement attempt that changed only its own bookkeeping as 'verified and committed' (three times: mutation-spike on Flash, verify-worker-count on Flash and on Sonnet). Check every accepted implement diff by hand until it is fixed" (`docs/journal/handover/2026-11-06-heartbeat-night.md`, "Open work and blockers", bead `coding-harness-te7q`). The lanes table in the same file records the victims: mutation-spike ("implement accepted empty (te7q)") and verify-worker-count ("implement accepted empty twice (te7q)"), and question Q-M8 parks mutation-spike until te7q merges. The neighbouring change redraft-after-scope felt it too: its findings and plan both record that its spike implement went to Sonnet "on 2026-11-06 Flash implement was accepted with an empty diff on both spikes tried (beads bvy and xay1; bug coding-harness-te7q)" (`plans/changes/redraft-after-scope/findings.md`, stage-2-call line; `plans/changes/redraft-after-scope/plan.md`, "Stage-1 route").

**Acceptance today asks for no work at all.** The implement verb's contract is the archived Flash-runner spec's criterion 10: after a zero-exit model process with a non-empty answer, the runner runs `make verify`, requires exit 0 and "changed bytes below the plan's `## Time used` heading", stages, makes one checkpoint commit and requires a clean worktree (`plans/changes/archive/2026-10-07-stage2-flash-runner/spec.md`, criterion 10, "Success means the post-run checks hold"). Nothing in that list requires the model to have changed a source file. The code follows the spec exactly: `run_attempts` calls the model, runs `verify_attempt`, and when the problem list is empty commits through `checkpoint` and prints "verified and committed · route … · attempt …" (`scripts/stage2.py`, `run_attempts` and the print at its acceptance branch; `verify_attempt`; `checkpoint`). `verify_attempt` runs the format step, cheap checks (ruff, selected pytest), derived preparation and `make verify` — all of which stay green on an untouched, already-green tree (`scripts/stage2.py`, `verify_attempt`, "Format, run the cheap checks, clear derivable ledger markers, stamp documents, render, `make verify`").

**Why the no-op commit is never empty.** The runner writes bookkeeping before and after the call: `begin_work_call` appends the attempt's audit line to `findings.md` before the model starts (`scripts/stage2.py`, `begin_work_call`, "Check and record one explore/implement attempt in its phase artefact"), and `persist_time_entry` writes the measured span into `plan.md` after the verdict. `checkpoint` stages with `git add -A` and commits everything that is not held or uncommittable; the change folder `plans/changes/<change>/` is always committable (`scripts/stage2.py`, `checkpoint` and `uncommittable` — the change's own folder is explicitly not in the held set). A model that changed nothing therefore still yields a commit of pure runner bookkeeping — exactly the "changed only its own bookkeeping" the handover names.

**The historical trajectory that opened the hole.** The runner once required the model to add a time line itself; that check was dropped in favour of runner measurement, and the test that pins the new behaviour says so in its docstring: "Planted fault: the old check for a model-added line rejects this otherwise green attempt" (`tests/test_stage2.py::test_runner_accepts_attempt_without_model_time_entry`). The work-proof the old line carried implicitly went with it; nothing replaced it.

**The measurement a work check would need already exists, but only for reporting.** Around the model call the runner takes two tree snapshots and computes `files = attempt_files(root, before, worktree_tree(root))` — the files the model itself changed, with the runner's own writes falling outside both snapshots by design (`scripts/stage2.py`, `run_attempts`, the "Both snapshots stand around the model call alone" comment; `worktree_tree`; `attempt_files`). This value feeds only the failure blocks and diagnostics ("Files the attempt changed (lines added, removed)"), never the verdict.

**Findings edits are explicitly not work.** `findings.md` is runner-owned: an attempt's edit of it is restored from the pre-call snapshot before any post-run check reads model-written state, and the edit alone never fails the attempt (`scripts/stage2.py`, `run_attempts`, the "findings.md is runner-owned" block; doctrine: `docs/WORKFLOW.md` §4 phase-4 text, "an edit you make there is put back before the checks"). Any "no work" rule must therefore judge work after the findings restore and excluding runner-owned bookkeeping.

**A clean-start precondition exists to build on.** `implement` refuses pre-existing changes outside its `findings.md` before the first call (`scripts/stage2.py`, `implement` calling `refuse_preexisting`; the Flash-runner spec terms call this the "Implementation baseline"). Every post-call difference outside the runner's own bookkeeping is therefore attributable to the attempt.

**The runner's only existing machine definition of "implementation source" lives in the review loop, not in implement.** The review loop's free stage skips itself when the change carries no source diff — `state["free"]["skipped"] = "free stage skipped: no implementation source diff"` — using `free_diff`, whose per-file gate `_free_candidate` admits only Python under `scripts/` and `tests/` and executable non-text files under `tools/`, and refuses documentation, plans, declarations, locks, binaries and dependency/generated trees (`scripts/stage2.py`, `free_diff`, `_free_candidate` and the `FREE_DIFF_SKIP_PARTS`/`FREE_DIFF_TEXT_SUFFIXES` constants). No equivalent notion exists on the implement/repair acceptance path (searched `scripts/stage2.py` for acceptance-time diff checks; none found — "not there" as of this reading).

**Repair is a different shape.** The repair verb shares `run_attempts` and would commit a bookkeeping-only diff the same way, but it carries an answer-level work proof implement lacks: the model must answer one fixed line per taken row, a code row needs a red-first test the runner proves on the attempt's code, and a guard-test row is proven red with `STAGE2_PLANT_FAULT=1` and green without it (`scripts/stage2.py`, `repair` and `REPAIR_ANSWER`; `tests/test_stage2.py` red-first/guard clusters). Whether that proof already catches a repair that changed nothing is an open question below, not a fact I verified.

**The guard-test doctrine any new check falls under.** A runner check is defended by a guard test whose source names `STAGE2_PLANT_FAULT` and plants a real fault; phase 6 reads every guard test and refuses one that "only fails conditionally on the switch, planting no real fault" (`scripts/stage2.py`, `PHASE6_GUARD_INSTRUCTION` and `GUARD_SWITCH`; mechanism examples in `tests/test_stage2.py` around the red-first proof tests).

## Where it lives

- Acceptance flow: `scripts/stage2.py` — `run_attempts` (verb loop, verdict, "verified and committed" print), `verify_attempt` (checks), `checkpoint` (commit), `attempt_files` + `worktree_tree` (the existing model-change measurement, report-only today), `persist_time_entry` and `begin_work_call` (the runner's own bookkeeping).
- The verbs: `implement` (`scripts/stage2.py`, routes Flash → Flash-repair → Sonnet stage-1; `--stage2-off` runs Sonnet once) and `repair` (`scripts/stage2.py`, `repair`, Codex → Codex-repair → Sonnet).
- The "source vs bookkeeping" classifier: `scripts/stage2.py` — `_free_candidate`, `free_diff`, `FREE_DIFF_SKIP_PARTS`/`FREE_DIFF_TEXT_SUFFIXES`; the loop's skip string "free stage skipped: no implementation source diff".
- Baseline cleanliness: `scripts/stage2.py` — `refuse_preexisting`, `changed_paths`, `derived_leftover` (the `updated:`-stamp exemption named in `refuse_preexisting`).
- Tests: `tests/test_stage2.py` — `World`/`world.script` stand-ins, `successful_implementation` (plants `src/app.py`), the acceptance tests near `test_runner_accepts_attempt_without_model_time_entry`; `tests/test_stage2_fail_fast.py` — the planted-fault cluster (its row L5-3 test is about findings-shaped lines, not empty diffs).
- Doctrine: `docs/WORKFLOW.md` §4 phase-4 runner text (runner runs `make verify`, measures attempts, makes the checkpoint commit; findings-restore rule); `prompts/04-implement.md` (file-only route, runner owns checks and commit).
- Specs: the living `plans/specs/implementation-verification/spec.md` (derived-file preparation; its criterion 1 makes a findings.md-only first attempt pass with a regenerated index — the bookkeeping-only shape this change must keep distinguishing from real work); the archived acceptance contract `plans/changes/archive/2026-10-07-stage2-flash-runner/spec.md` criterion 10; the archived derived-files change `plans/changes/archive/2026-10-08-runner-derived-files/spec.md`.
- Bug record: `docs/journal/handover/2026-11-06-heartbeat-night.md` (bug text, lanes table, Q-M8); `plans/changes/redraft-after-scope/findings.md` and `plan.md` (route reason citing te7q).

## What is unclear about it

- **The bead's own text is unread (not read ≠ not there).** The tracker is the Dolt database under `.beads/` transported via `refs/dolt/data`; as a read-only file explorer I read no tracker entry, so `coding-harness-te7q`'s description — which per the 2026-10-22 convention names the change's class — its acceptance criteria, and any maintainer wording about what counts as "work" are open questions for the interview.
- **The class is not declared in the tree.** The `research.md` skeleton carries no `class:` key and no `spec.md` exists yet; the only class declaration so far is whatever `--class` this explore run was given. `bounded` and `spike` are both plausible shapes for a runner-check fix; nothing in the repository decides it.
- **The three accepted no-op diffs themselves were not read.** The victims' worktrees (`mutation-spike`, `verify-worker-count`) are outside this worktree, so exactly which files those commits touched — findings/plan bookkeeping only, or also stamps and `plans/INDEX.md` — is known only from the handover's summary sentence, not from the diffs.
- **Whether a Sonnet stage-1 no-op was distinguishable from the Flash ones** in the same runs (route, diagnostics, what the answer said) — unread, same reason as above.
- **What counts as work for a legitimate non-code change.** `_free_candidate` counts only `scripts/`/`tests/` Python and executable `tools/` files; a change that legitimately edits only docs would produce a diff the existing classifier calls "no implementation source". Whether the implement acceptance may reuse that notion or needs its own is recorded here as a tension, not answered.
- **Whether repair's existing proofs already refuse a no-op repair** — `check_repair_answer` demands fixed lines and the runner proves named tests on the attempt's code; whether those proofs can pass green on an unchanged tree was not traced to a verdict. Open question, not a fact.
- **Whether the exemption for derived stamps (`derived_leftover`) interacts with a work check** — a first Flash attempt that creates only `findings.md` passes today with a regenerated index (living spec criterion 1); how a "no work" rule treats that accepted shape is unstated anywhere I read.

## Which files a change would have to touch

- `scripts/stage2.py` — the acceptance path: `run_attempts` (where the verdict is decided and `files` is already measured) or `verify_attempt` (where checks live); `implement` and `repair` wire their checks through the shared loop, so a verb-level difference is wiring, not a new loop.
- `tests/test_stage2.py` — the acceptance cluster around `test_runner_accepts_attempt_without_model_time_entry`, `successful_implementation` as the green fixture to contrast a no-op against; a new guard test naming `STAGE2_PLANT_FAULT` per the house mechanism.
- `tests/test_stage2_fail_fast.py` — where planted-fault tests live, if the fault belongs there rather than beside the acceptance tests.
- `docs/WORKFLOW.md` §4 — the phase-4 runner text would need a sentence about the new acceptance condition, beside the existing "verified and committed"/findings-restore wording.
- `prompts/04-implement.md` — only if the model-facing contract changes (today it says the runner runs checks and commits; a no-work refusal is runner-side and may not need prompt text — undecided).
- The living spec `plans/specs/implementation-verification/spec.md` or a new `spec.md` for this change, per the workflow's normal phase 2 — not a code file, but where a new acceptance criterion would be written down.
- `plans/INDEX.md` is derived (`scripts/plans_registry.py` renders it); a change never hand-edits it.
