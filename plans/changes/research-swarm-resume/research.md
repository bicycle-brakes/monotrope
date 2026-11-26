---
title: "Research — research-swarm-resume"
status: draft
implementation_status: none
date: 2026-11-26
last_reviewed: 2026-11-26
updated: 2026-11-26
supersedes: null
superseded_by: null
bead: coding-harness-f6qj
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-26", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
class: bounded
---

# research swarm resume — Research

Stage-2 call, 2026-11-26: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM through Z.ai at its weekly limit until 2026-11-29 · leak check clean over 1286 files, 6036 commits, 12 rules.

## Runner exploration — 2026-11-26

# Research: research-swarm-resume

Read-only findings for `plans/changes/research-swarm-resume/`. Nothing here is a design or a recommendation.

## What exists today

**The change folder.** `plans/changes/research-swarm-resume/` holds only `research.md`. Its frontmatter has `class: bounded`, `bead: coding-harness-f6qj` and `provenance: human-written`. Its body is the skeleton text plus one stage-2 call line dated 2026-11-26. There is no `spec.md`, `decisions.md`, `design.md` or `plan.md`. The change's problem statement is therefore not written in any artefact I could read. The folder's name and the bead id are the only record of what it is for.

**Resume is already implemented for the research swarm.** Per `docs/WORKFLOW.md`, section "Resume after an abort (Q-13)", a later run of the same change reuses finished contributions. A slot is reused only when its resume binding (digests of the frozen inputs), stage, topic, seat, endpoint, model and exact prompt hash match, and its result was `ok` and validates. The run gets its own run id, deadlines and receipt.

**The reuse decision.** Source: `scripts/stage2_research_store.py`, `plan_reuse` and `SLOT_KEY_FIELDS` (`stage`, `topic`, `seat`, `endpoint`, `model`, `prompt_sha256`), with `REUSABLE_OUTCOME = "ok"`. For each planned slot, `plan_reuse` does one of the following:
- It names a mismatch on a key field.
- It names a non-`ok` outcome.
- It names a failed validation (`_valid`).
- It names the slot as `interrupted` when a launch record exists without a result.
- It names results that have no planned slot as `not planned`.
- It names results of older runs as `not the latest run`.
- Otherwise it reuses the record.

**The source is the latest stored run only.** Source: `Store.resume_source` in the same file. It returns no usable source when:
- a run directory has an unreadable `run.json`;
- the latest run recorded a refused slot (security refusal);
- the latest run is `complete` and its record marker `research-swarm/v2 run <id> -->` appears in `research.md`;
- the frozen binding has changed (`changed_against_stored`).

Each of these cases is named as a reason. The test `test_only_the_latest_stored_run_is_a_source` and `test_a_changed_binding_reuses_nothing_and_names_the_paths` (both in `tests/test_stage2_research_store.py`) cover the first and last of these.

**Where the run uses it.** Source: `scripts/stage2_research_run.py`, `Run.open` and `Run.run_stage`.
- `Run.open` runs in this order: load limits; read the declaration; select roles; check the Pi runner and the leak key where Go seats are used; open the store and check it lies outside the repository and home; take the store lock (`StoreLocked` refuses); freeze the inputs; call `resume_source`; reuse the previous publication prefix and producer day; start a new run id with `start_run`.
- `Run.run_stage` calls `plan_reuse`, adopts the reused records with `Store.adopt` (each keeps `reused_from` and `launched_in`), and dispatches only the remaining slots. A reused slot starts no call and gets no leak-check audit line.
- `Run.on_terminal` writes each slot's terminal record as it ends, so a finished contribution survives a kill.
- `Run.audit` writes the launch record before a call starts. This is what lets an interrupted launch be named later.

**The reuse is visible in the run's audit.** Source: `stage2_research_run.py`, the run summary structure that includes `"resume"`, with `not_reused` and per-record `reused_from`. Adopted records keep their original times, and a corrected seat's remaining allowance is computed from those times (`Run.remaining_topic_allowance`, `Run.seat_used_seconds`). When the stored times are unknown, the full topic allowance is charged (`Run.seat_used_seconds`, the fallback branch).

**The verb entry point.** Source: `scripts/stage2.py`, `prepare_explore` and `explore`. `prepare_explore` writes a single-use receipt. `explore` consumes it through `stage2_availability` before `stage2_swarm.run` is called, so a resumed run needs a new receipt from a new `prepare-explore`. `scripts/stage2_swarm.py`, `run`, delegates to `stage2_research_run`.

**Existing tests.** In `tests/test_stage2_research_store.py`, the names that cover resume include:
- `test_reuse_requires_the_exact_binding_seat_model_and_prompt`
- `test_unfinished_outcomes_are_never_reused_and_are_named`
- `test_interrupted_and_invalid_results_are_not_reused_and_are_named`
- `test_a_matching_valid_result_is_never_also_a_launch`
- `test_adopted_results_carry_their_source_run_and_original_times`
- `test_a_reused_result_keeps_the_run_that_launched_it`
- `test_a_refused_run_is_never_a_resume_source`
- `test_a_complete_run_clears_the_store_and_a_cleared_store_has_no_source`
- `test_one_run_per_change_and_a_killed_runs_lock_is_released`
- `test_digest_only_publication_reports_binding_drift_without_reuse`

`tests/test_stage2_research_deep_review.py` and `tests/test_stage2_swarm.py` also match the resume and reuse names. I did not read them.

## What is unclear

- **The problem the change is meant to solve.** The folder has no spec, and I could not read the bead (`coding-harness-f6qj`) because my tools are read-only and the tracker is a shell command. Resume already exists in code and doctrine, so the gap this change addresses is not visible in the artefacts I read. This is an open question for the maintainer, not an inference.
- **The `neighbours:` header.** The `research.md` frontmatter has no `neighbours:` key. `docs/WORKFLOW.md` says the header is required for a swarm run. For this bounded explore it is not checked, but the header is absent as a fact.
- **The provenance line.** The frontmatter still says `provenance: human-written`. The body asks whoever fills the file with a language model to set `ai-drafted-reviewed`, `produced_by:` and `review:`. This explore output is model-produced, and I have not changed the header.
- **Not read in full.** In `stage2_research_run.py`, lines after the first 1290 were not read, including the correction-adoption branch (around the `stored correction` docstring), the run finish and publication path, and the summary written to `research.md`. In `stage2_research_store.py`, `Store.start_run`, `finish_run`, `clear`, `recover_staged` and `adopt` were not read in full. Claims about how a publication is finished and how staged writes are recovered therefore rest on the names and docstrings only.
- **`docs/WORKFLOW.md` says "reused only when its result was ok and validates".** The code additionally refuses reuse after a refused slot in the latest run and after a published complete run. Both refusals are stated in the code but not in that doc paragraph.
- **No test was run.** I have no shell access in this phase, so the test names above are taken from the source, not from a run.

## Which files a change would have to touch

Files that carry the resume behaviour today:
- `scripts/stage2_research_store.py`: `Store.resume_source`, `plan_reuse`, `Store.adopt`, `SLOT_KEY_FIELDS`, `REUSABLE_OUTCOME`
- `scripts/stage2_research_run.py`: `Run.open`, `Run.run_stage`, `Run.on_terminal`, `Run.audit`, `Run.correction_entry`, `Run.remaining_topic_allowance`
- `scripts/stage2.py`: `prepare_explore`, `explore` (receipt consumption before the run)
- `scripts/stage2_swarm.py`: `run`
- `docs/WORKFLOW.md`: section "Resume after an abort (Q-13)"
- `tests/test_stage2_research_store.py` and `tests/test_stage2_research_deep_review.py`

Files that carry the interface and would change only if the resume contract changes: `scripts/stage2_research_snapshot.py` (`stored_binding`, `stored_publication`, `stored_brief`) and `scripts/stage2_research_dispatch.py`, which serialises launches and terminal outcomes.
