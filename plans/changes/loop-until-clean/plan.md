---
title: "Plan — loop-until-clean"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-4fk
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, review-loop, opencode-go, swarm]
---

# Plan — `loop-until-clean`

```text
For you:     The review loop runs until a round finds nothing — round 1 a swarm of the free OpenCode Go models on the diff alone, then one ladder model per round; the repair brake and the ladder's end stop it.
Done when:   The 16 criteria hold with their ledger tests green, every new rung is declared with its data terms read, and make verify is green once your stated ADR answer is recorded.
Appetite:    8 h of phase 4, repair rounds included; a stop, not an estimate.
Not now:     The research swarm, the structure-first round, the live round view; the phase-6 and 2a reviewers, repair routing, and any numeric round cap.
Pre-mortem:  suppose it failed: most likely because the merged swarm round broke the round counting that survives a release.
Starts unless you say stop.
```

Implements [spec.md](spec.md), shaped by [design.md](design.md). The eight
interview answers stand; no ADR answer is recorded here.

## Steps

1. **`scripts/stage2.py`** — remove `MAX_ROUNDS`; add `free_stage(root)`
   reading the entry's `swarm` key (refusing an empty one by name); round 1
   calls every free-stage member in parallel through today's isolated Pi
   launch but with `--no-tools`, merges their rows into one round under one
   heading (members comma-joined without spaces, ids `L1-<k>`, Reviewer cell
   per row, a failed member named in the block, nothing written when no
   member answered); rounds 2 and later call `modelle`'s rungs after the
   `swarm` members; admission refusals in order — undecided rows, a clean
   previous round, two consecutive fix-r rounds (all taken rows of both
   Origin `fix-r`), then the ladder's end reported to the maintainer with no
   repeated rung; `taken_in_round` keeps its rule at every round number and
   its docstring cites ADR 0017 decision 6 as amended by ADR 0021; `probe`
   walks `modelle`; module docstring and help state the new rule.
2. **`tests/test_stage2.py`** — write the ledger's new tests; adapt the
   existing loop tests to the new rule, keeping the names other live ledgers
   name (`test_round_three_starts_after_a_fixed_round_two_row`),
   replacing `test_a_round_without_a_finding_still_counts` and
   `test_the_loop_stops_at_three_rounds` with the clean-stop and ladder-end
   tests, and folding `test_round_three_starts_only_after_a_taken_row` into
   them; move the doctrine needles of
   `test_the_prompts_name_the_ladder_and_the_limit`,
   `test_workflow_section_4_routes_the_three_reviews`,
   `test_agents_md_names_the_loop_and_the_runner` (`agents_md_problems`) and
   `test_section_4_says_what_a_round_can_read` from "three rounds" and the
   round-3 condition to rounds until clean, the swarm, the brake and the
   ladder's end, with the free stage's no-tools reach stated apart from the
   ladder's unconfined one.
3. **`model-endpoints.yaml`** — the `opencode-go` entry: `modelle` grows to
   the loop's models in the maintainer's Q-1 order (ids in the entry's
   lowercase form), the new `swarm` key names the free stage's three, and the
   `bemerkung` is rewritten with each new model's price, monthly limit and
   privacy-table reading (dated, read live in phase 4 from the Go page), the
   free stage's unread-terms acceptance, the fresh-check rule with its date,
   and the DeepSeek ZDR note refreshed past 2026-10-31; a model whose terms
   show retention or training, or cannot be read, stays off the ladder and is
   named in `findings.md`.
4. **Doctrine** — `prompts/04b-review-loop.md` (the gate line, the swarm
   round, the free stage's diff-only reach, the fresh free check as the
   orchestrator's step), `prompts/06-review.md` and
   `prompts/02a-spec-review.md` (their loop-limit sentences),
   `docs/WORKFLOW.md` (the phase table's 4b row, §2's escalation sentence,
   the model table's 4b row, the verb list, §4's review-loop and repair
   sections), `AGENTS.md` (the 4b row and the Stage-2 paragraph, within 200
   lines) and `templates/findings.md` (the Origin note's brake consequence)
   state the one rule: rounds until clean, free swarm first, ladder bound,
   fix-r brake, `make verify` green after each repair.
5. **`docs/adr/0021-review-swarms-until-clean.md`** — written by phase 2b;
   phase 4 adjusts it only where a measurement contradicts it, and records no
   ADR answer: that is the maintainer's, stated in the conversation.
6. **`ROADMAP.md`** — Now 3's bead line moves with the merge;
   **`plans/INDEX.md`** — refreshed by the runner's derived-file preparation.
7. **`plans/changes/loop-until-clean/plan.md`** — each `not yet written`
   ledger entry flips when its test exists, and `## Time used` carries each
   run's measured line; the runner writes `findings.md`.
8. **`scripts/handover_schema.py`** and **`scripts/stage2_runs.py`** — read
   against rounds above three; change only what breaks, expected nothing
   beyond a stale comment.

The runner verifies and makes the checkpoint. The orchestrating session alone
records the maintainer's stated ADR answer in `decisions/answers/
loop-until-clean/adr.yaml`, then the reviews and the decision pull request
(`decide(loop-until-clean): …`, label `decision`, decision template) run; the
pull request names bead `coding-harness-4fk`.

## Do not touch

`scripts/leakcheck.py`, `provenance.yaml`, `decisions/gates.yaml`,
`.claude/settings.json`; the bodies of ADR 0011, ADR 0017 and every other
record under `docs/adr/`, and `scripts/check_decision_continuity.py`'s map (no
D- or O-number moves); the archived plans of `plans/changes/archive/` —
`test_the_adr_draft_states_every_point` reads the stage2-mimo design as
history; `model-endpoints.yaml`'s German keys; the parser, probe and schema
of `scripts/stage2_runs.py`; stage 1's models and escalation; the `session`
verb beyond the declaration's reading of `modelle`; the repair routing of
ADR 0017; the evidence rule and `Broke a test` ownership; customer instances.
Tests use local stand-ins; no live model call is part of the test suite.

## Explore fallback carried forward

None to carry: phase 1 ran as a stage-2 call (2026-10-14, route `flash`,
endpoint `glm-coding-plan`, model `glm-5.3-flash`, leak check clean —
`research.md`, header line), not as a Stage-1 route.

## Verification

```sh
.venv/bin/python -m pytest tests/test_stage2.py tests/test_stage2_runs.py tests/test_model_endpoints.py -q
python3 scripts/check_interview_minimums.py --change loop-until-clean
python3 scripts/check_criterion_ledger.py
make verify
```

`python3 scripts/validate_change_artefacts.py --check` is named by the phase
prompt but has not landed (bead coding-harness-jc3); it cannot run in this
tree, and nothing was changed to compensate for its absence.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_a_clean_round_ends_the_loop — a second round starts after a clean round 1, or the refusal names a round cap
- 2: not yet written tests/test_stage2.py::test_round_one_runs_the_free_swarm_as_one_round — one model called, member calls sequential, two headings, or a row without its model
- 3: not yet written tests/test_stage2.py::test_the_free_stage_reads_nothing_beyond_the_diff — a free-stage call with read tools, or a ladder round without them
- 4: not yet written tests/test_stage2.py::test_a_silent_swarm_member_does_not_sink_the_round — a failed member erases the answering members' rows, or a wholly silent round is written
- 4: tests/test_stage2.py::test_a_call_without_an_answer_is_not_a_round — a round written from no answer at all
- 5: not yet written tests/test_stage2.py::test_the_loop_texts_name_the_fresh_free_check — the check step or its recorded date missing from the loop prompt, WORKFLOW §4 or the entry's remark
- 6: not yet written tests/test_model_endpoints.py::test_every_new_ladder_model_carries_its_terms_reading — a new ladder model without a dated terms reading, or retention or training on the ladder
- 7: not yet written tests/test_model_endpoints.py::test_unread_terms_reach_the_free_stage_alone — a ladder model on unread terms, or the acceptance missing from the remark
- 8: tests/test_stage2.py::test_a_round_calls_its_rung_from_the_entry — a skipped or repeated rung
- 8: tests/test_stage2.py::test_reordering_the_ladder_touches_no_code — a reorder or a swarm change that needs a code edit
- 9: not yet written tests/test_stage2.py::test_the_loop_stops_when_the_ladder_ends — a repeated last rung or a round past the ladder
- 10: not yet written tests/test_stage2.py::test_two_fix_r_rounds_stop_the_loop — a round starts after two fix-r rounds, or the brake fires over a base finding
- 11: tests/test_stage2.py::test_round_three_starts_after_a_fixed_round_two_row — a repaired row cancels the next round
- 12: tests/test_stage2.py::test_an_undecided_loop_row_holds_the_next_round_and_the_release — a round starting over an undecided row
- 13: not yet written tests/test_stage2.py::test_every_round_counts_after_release — a swarm heading the counter misreads, or a released round is lost from the count
- 14: not yet written tests/test_stage2.py::test_the_probe_walks_every_declared_loop_model — a declared loop model the probe skips
- 15: not yet written tests/test_stage2.py::test_the_loop_doctrine_names_rounds_until_clean — a live "at most three rounds", a round-3 condition, disagreeing texts, or the stale ADR-0015 citation
- 16: not yet written tests/test_stage2.py::test_adr_0021_amends_the_round_budget — a rewritten body of ADR 0011 or 0017, or a point missing from ADR 0021

## Runner handoff — 2026-10-14

Drafting attempts 1 (codex) and 2 (codex-repair) failed their calls; this
draft is attempt 3 (glm, `glm-5.3`). No phase-2a rows were open in
`findings.md`, so none had to be worked in. This call writes `spec.md`,
`design.md`, `plan.md` and the one new ADR file, commits nothing and runs no
git command; the runner owns `make verify` and the checkpoint, the
orchestrating session owns the tracker and the ADR answer. Resume: read the
four files against Q-1 to Q-8, have the maintainer answer the ADR question,
then spec review (2a) and the card above.

## Time used

Nothing yet — phase 4 has not run.
