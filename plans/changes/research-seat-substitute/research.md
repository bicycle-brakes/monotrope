---
title: "Research — research-seat-substitute"
status: draft
implementation_status: none
date: 2026-11-27
last_reviewed: 2026-11-27
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-0ysc
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-28", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# research seat substitute — Research

## Topic (bead coding-harness-0ysc)

Class: bounded. Maintainer 2026-11-25 (session 9200c6b1), step 1 of the swarm
optimisation. Measured 2026-11-25 on every v2 run in the repository: 2 of 10
runs complete (detached-job-launcher 1/4, ontology-relation-layer 1/4,
pi-work-route 0/2), mostly because single seats time out
(deepseek-v4.1-flash on repository topics). Change
`scripts/stage2_research_run.py`: a seat that times out or fails gets exactly
one substitute from its own trio (the next reachable admitted model of that
seat's class, recorded in the run's history with the reason); only a seat
whose substitute also fails leaves the run incomplete. Together with
`coding-harness-n76m` (finder limit follows the measured repository size).
Measure: completion rate of the next runs.

Further evidence (orchestrator, 2026-11-27): `state-first-records` runs 4
(`355d1c04`) and 5 (`a6cd8479`) ended incomplete because finder slot
`finders-0-2` (repository seat 2, `mimo-v2.6-flash`) returned a tool-call
text instead of finder JSON (`invalid-report`); run 6 completed after the
orchestrator moved that seat to `glm-5.3-flash` by hand. An invalid report is
a failure of the same kind as a timeout for this change.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-28: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM through Z.ai at its weekly limit until 2026-11-29 · leak check clean over 1319 files, 6146 commits, 12 rules.

## Runner exploration — 2026-11-28

## Research: research-seat-substitute (bead coding-harness-0ysc)

Read-only exploration, 2026-11-28. Sources are repository files and the handovers named below. I did not run the swarm, read any run records, or check the live provider state.

### What exists today

**Preparation-time substitutes (exist).** `scripts/stage2_availability.py`, `_Selection.fill`, builds a substitute pool of admitted Go models with tool support, ordered by `anfragen_5h` (cheapest first, ties by id). Each seat whose preferred model is unusable or unreachable at preparation takes the cheapest reachable pool model that no seat of its trio holds, marked `substitute for <seat>`. The pool is written into the selection (`selection.pool`, same file, `prepare_research` path). The design is in `docs/adr/0020-phase-1-research-swarm.md` (substitutes section, around the "Substitutes form one pool" paragraph) and in the archived `plans/changes/archive/2026-11-06-research-swarm/decisions.md`, Q-14.

**Run-time seat handling (does not exist for timeouts or failures).** `scripts/stage2_research_run.py`, module docstring: "The run never probes, refreshes the catalog, retries or swaps a seat." The same is stated in `docs/adr/0020-phase-1-research-swarm.md` ("no swap, re-probe or retry"). A selected seat stays fixed for the whole run; its model is never replaced after the receipt is consumed.

**What a failed seat gets today, by stage** (`scripts/stage2_research_run.py`):

- **Finders** (`stage_finders`, `require_ok`): a finder whose outcome is not `ok` (timeout, process failure, or invalid report) stops the run before the merge, the sentence and every topic. There is no correction and no substitute. The finder seats are the repository seats (`research_roles`, `finder_agents` = `repository_agents`), so the finder slot `finders-0-2` in the handover is the same seat as repository seat 2.
- **Topics, invalid report** (`stage_topics`, `correction_entry`, `stored_correction_final`): a process-successful answer that fails format or citation validation gets exactly one correction call from the same frozen seat (same model, effort and tools) in a second dispatch batch. A second invalid answer ends the seat. The correction uses the seat's remaining topic allowance only.
- **Topics, timeout or process failure** (`stage_topics`, `run_stage`): no correction, no retry, no substitute. The outcome is recorded (`timed-out`, `failed`, `invalid-report`, etc.). If the seat is required and not `ok`, `stage_topics` raises `Stop("required topic slots did not finish with a valid report …; no judge starts.")`.
- **Free online seats** (`topic_entries`, `required=False`): a failure is named and does not stop the run. `docs/adr/0020-phase-1-research-swarm.md` states this explicitly ("best-effort: failure is named, never hidden or substituted").

**Timeouts.** Per-role limits come from `research-swarm-limits.yaml`, read once per invocation by `scripts/stage2_research_limits.py`. Current values in that file: `run_minutes: 240`, `topics: 15`, `finders: 60`, `merge: 15`, `sentence: 7.5`, `judge: 22.5`. The `topics: 15` value was raised 1.5× from 10 on 2026-11-26 (comment in the file, maintainer). The handover `docs/journal/handover/2026-11-25-night-run-seven-prs.md` (item 2, pi-work-route) reports deepseek-v4.1-flash timing out on repository topics 1, 2 and 4 under the older 10-minute limit.

**The measured problem as recorded (not verified here).** The bead text (in `plans/changes/research-seat-substitute/research.md`, Topic section) cites 2 of 10 v2 runs complete and single-seat timeouts. The `state-first-records` evidence (runs 4 and 5 incomplete on an invalid tool-call-text finder report, run 6 complete after a manual seat move) comes from the orchestrator's note in the same file, dated 2026-11-27. I read these figures from the file and the handover; I did not open the run records they refer to.

**Where a seat's substitute would have to come from at run time.** Two places hold the candidates: the frozen receipt's `pool` (written by `stage2_availability.py` at preparation), and the live catalog (`stage2_go.py`, `definition_of`/`assess`). The run's own Go send path (`launch` in `stage2_research_run.py`) already checks each Go send against the stored definition and the admission verdict. Free online members (`online_free`) are the only seats that run an admission callback at dispatch (`free_admission`). A repository or paid-online seat has no such check at dispatch.

### Where it lives

- `scripts/stage2_research_run.py`: `Run.stage_finders`, `Run.stage_topics`, `Run.correction_entry`, `Run.stored_correction_final`, `Run.run_stage`, `Run.launch`, `Run.topic_entries`, `Run.require_ok`.
- `scripts/stage2_availability.py`: `_Selection.fill`, `_Selection.usable`, `_Selection.reachable`, `research_roles`, `probe_free_research`.
- `scripts/stage2_research_limits.py` and `research-swarm-limits.yaml` (repository root): time limits.
- `scripts/stage2_research_judge.py`: `TOPIC_OUTCOMES` (`ok`, `failed`, `timed-out`, `cancelled`, `not-started-deadline`, `refused`, `invalid-report`).
- Rules: `docs/adr/0020-phase-1-research-swarm.md` (substitute pool, no swap, best-effort free seats); `docs/WORKFLOW.md` (phase 1 section, around the research swarm).
- Archived design: `plans/changes/archive/2026-11-06-research-swarm/` (`design.md` on the substitute pool, `decisions.md` Q-14 and the later decision that supersedes Q-12 and Q-14 in part).
- Tests named in the archived plan: `tests/test_stage2_research_availability.py` (`test_preferred_models_come_first_and_substitutes_never_take_them`, `test_substitute_is_the_cheapest_reachable_unused_pool_model`, `test_pool_requires_tool_support_and_a_measured_wire_api`), `tests/test_stage2_swarm.py` (`test_selection_is_frozen_for_the_run_and_recorded`). I did not open these files, so their current state is unread.

### What is unclear

1. **The ADR says no swap, and the bead asks for a swap.** `docs/adr/0020-phase-1-research-swarm.md` and the module docstring both forbid a run-time swap. The change would introduce one. That reconciliation is a decision for the maintainer; I have not resolved it.
2. **Whether the frozen receipt keeps the pool.** `stage2_availability.py` writes `pool` into the selection (line-level: `"pool": selection.pool`). I did not confirm that `consume_research` carries it into the run's `state`, or that `research_roles` can see it. Unread.
3. **Admission of a run-time substitute.** Only free online seats are checked at dispatch (`free_admission`). A substitute for a repository seat would need the same Go definition check plus the framework data-class exclusion (`stage2_swarm.exclusion_problem`, `data_class = "framework"`). Whether the existing code path can be reused without a second route is unread.
4. **Substitute for a finder.** The finder stage stops on any non-`ok` result before merge. The bead says a timed-out or invalid seat gets one substitute "from its own trio". Whether a finder substitute also changes the finder-stage `valid` filter and the `Stop` in `require_ok` is unread.
5. **Substitute versus correction.** An invalid topic answer already gets one correction from the same seat. Whether a substitute should replace that correction, follow it, or leave it alone is not stated anywhere in the sources I read.
6. **Run-time timeout limit.** The handover measurement used the 10-minute topic limit. The current file uses 15 minutes. The baseline for "completion rate of the next runs" should be stated with that cut-off.
7. **Unread: the measured runs.** The completion counts (2 of 10, 1 of 4, and so on) come from the bead text and handovers. I have not checked them against the run records under `plans/` or the store.

### Which files a change would have to touch

- `scripts/stage2_research_run.py`: finder stage (`stage_finders`, `require_ok`), topic stage (`stage_topics`, `correction_entry`, a new substitute entry builder), `run_stage` (only if a substitute needs a new dispatch batch), `launch` (admission for a non-free Go substitute).
- `scripts/stage2_availability.py`: the pool must reach the run (`research_roles` or the consumed `state`); no new probe at run time, which the ADR forbids.
- `scripts/stage2_research_judge.py` and `scripts/stage2_research_report.py`: the outcome record must name the substitute and its reason in the run's history (`stage2_research_history.py`).
- `docs/adr/0020-phase-1-research-swarm.md` and `docs/WORKFLOW.md`: the no-swap rule changes, so a decision record is needed first.
- Tests: `tests/test_stage2_research_availability.py`, `tests/test_stage2_swarm.py` and the research-run tests; no test file was read for this exploration.
