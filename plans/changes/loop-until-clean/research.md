---
title: "Research — loop-until-clean"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-dx0
owner: Data Architect
provenance: human-written
tags: [research]
---

# loop until clean — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-10-14: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 418 files, 1129 commits, 12 rules.

## Runner exploration — 2026-10-14

Phase 1 (explore) for `loop-until-clean` is done. The skeleton `plans/changes/loop-until-clean/research.md` exists (status `draft`, bead `coding-harness-dx0`, `provenance: human-written`, stage-2 call line already written by the runner); per my brief I do not edit it — the following is the prose to append, in the file's structure. Everything below was read in this worktree (`explore/loop-until-clean`, on top of `main` at `e0cea42`).

## What exists today

The review loop (phase 4b) is the stage-2 loop between spec review (2a) and phase 6. Its bound is three rounds: round 1 and 2 always run, round 3 starts only when round 2 wrote at least one row whose status begins `taken` or `fixed`, and a fourth round is refused (ADR 0011, decision 3, `docs/adr/0011-stage-2-reviews-through-opencode-go.md`; AGENTS.md, phase table row 4b and the Stage-2 paragraph). The change's own origin is recorded: on the first night run "Round 4 of the review loop was not possible: the runner stops at three rounds (ADR 0011; bead coding-harness-dx0 is the change to lift it)" (`docs/journal/handover/2026-10-12-night-run-first-rehearsal.md`, §4 "Stuck or not as planned"), and ROADMAP.md lists the bead under Now 3, "Stage 2 that can be trusted", as "review rounds until one finds nothing (coding-harness-dx0)".

The runner enforces the bound in `scripts/stage2.py`, verb `review-loop` (function `review_loop`): four refusals stand in this order — (1) `done_rounds >= MAX_ROUNDS` refuses with "N rounds have run; the loop stops at 3", (2) undecided rows hold the next round (`undecided_refusal`), (3) round 3 requires `taken_in_round` over round 2's rows, refusing "round 2 wrote no taken row; the loop stops at 2", (4) `round_number > len(models)` refuses because the ladder has no rung for it. `MAX_ROUNDS = 3` is a module constant (`scripts/stage2.py`, near `ROW_COLUMNS`). The round count survives the record's deletion after a release: `release` writes a `Rounds run: <n>` line into `findings.md`, and `rounds_run` counts `## Round <n> —` headings in the loop record plus every `Rounds run:` line in `findings.md` (regexes `ROUND_HEADING`, `ROUNDS_LINE`). `taken_in_round` counts a status beginning `taken` or `fixed`, so a repaired row does not cancel round 3 — its docstring cites "ADR 0015, decision 5", while the rule now stands in ADR 0017, decision 6 ("A fixed row counts as taken; round 3 requires a taken or fixed row in round 2, and the maximum stays three rounds", `docs/adr/0017-codex-repairs-taken-findings.md`).

"Clean" is already a stop condition at exactly one place, and not a success state: a round that reports no finding still counts as a round, and two of them stop the loop before round 3 (`tests/test_stage2.py`, `test_a_round_without_a_finding_still_counts`); a clean round 1 does not stop the loop — round 2 runs unconditionally (`test_a_round_without_a_finding_still_counts` again; ADR 0011 decision 3 "Rounds 1 and 2 both run"). The full cap is `test_the_loop_stops_at_three_rounds` (the fourth call is refused, also after the release), the round-3 condition is `test_round_three_starts_only_after_a_taken_row`, and `test_a_call_without_an_answer_is_not_a_round` states that a failed call writes no round while "the loop itself still runs to three".

The ladder is data: `review_loop` takes `ladder(root)`, the ordered `modelle` list of the `opencode-go` entry in `model-endpoints.yaml` — today `deepseek-v4.1-flash`, `mimo-v2.6-flash`, `mimo-v2.6-pro`, one rung per round — and reordering is "a one-line pull request" (ADR 0011 decisions 3 and 8; the entry's `bemerkung`). The entry also carries the cost and terms frame the cap sits in: the Go plan's monthly limits per rung (USD 60 / 60 / 15) and the maintainer's accepted terms risk, with ADR 0011 decision 8 reasoning "the loop makes at most three calls per change".

Adjacent rules an unbounded loop meets: after each round's repair `make verify` must be green before the next round starts; the phase-6 reviewer writes its verdict before any loop row exists (rows live outside the repository, `${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/<change>/loop.md`, until `release-loop`); "two consecutive rounds of `fix-r` origin are an escalation, not a third round" (`docs/WORKFLOW.md` §2 "The findings process"; `templates/findings.md`, Origin column); "a finding already rejected in an earlier round may only reappear with new evidence attached" (`prompts/06-review.md`; `templates/findings.md`); and stage 1 has its own, separate escalation "after two failed review rounds, move up to Opus 5.5" (`docs/WORKFLOW.md` §3). The handover form already anticipates the change's wording: its field is `review_rounds` — "rounds until clean" (`scripts/handover_schema.py`).

Related open work in the same theme, as recorded: coding-harness-mvk "Review-loop round 1 looks at the structure of the code first" (explored on its own branch, `docs/journal/handover/2026-10-14-night-run-third.md`, exploration table), coding-harness-uco "live view of a round" and coding-harness-cit "diagnostics of failed attempts" (ROADMAP.md Now 3), and two recorded rules waiting for their change — the review of the implementation as an OpenCode Go swarm (bead coding-harness-4fk) and research as a swarm (coding-harness-icw) — same handover, "Recorded rules still waiting for their change".

## Where it lives

Every statement of the three-round rule, by file: `scripts/stage2.py` (constant `MAX_ROUNDS`; the `review_loop` refusals; `rounds_run`; `taken_in_round`; the module docstring's "at most three rounds"); `prompts/04b-review-loop.md` (the gate line "at most three rounds — round 3 only when round 2 wrote at least one taken row"); `prompts/06-review.md` ("at most three rounds, one rung of the ladder each, round 3 only when round 2 wrote a taken row"); `prompts/02a-spec-review.md` ("The review loop between the two phases runs at most three rounds on the ladder" — the same 4b loop, referenced from 2a); `docs/WORKFLOW.md` (phase table row 4b; §2 escalation sentence; the model table's row "4b Review loop — the ladder"; the verb list's `review-loop` entry; §4 "The review loop (phase 4b)" with "At most three rounds, and round 3 only when round 2 wrote at least one taken row"; §4 "Repairing taken findings" with "A fixed row counts as a taken one for round 3 and for the run count"); `AGENTS.md` (row 4b and the Stage-2 paragraph); `docs/adr/0011-stage-2-reviews-through-opencode-go.md` (decisions 3, 7, 8, the consequence bullets "Nothing leaves before the merge…" and "A rule, not proof, at three places", and the option "The model of round 2"); `docs/adr/0017-codex-repairs-taken-findings.md` (decision 6, "the maximum stays three rounds"); `model-endpoints.yaml` (the `opencode-go` entry: `modelle` order and the bemerkung's ladder sentence).

The rule is pinned by doctrine tests in `tests/test_stage2.py`: `test_workflow_section_4_routes_the_three_reviews` requires the needles "model-endpoints.yaml", "modelle[n-1]" and "round 3 only when round 2 wrote a taken row" in WORKFLOW §4's 4b row; `agents_md_problems` / `test_agents_md_names_the_loop_and_the_runner` require "three rounds" and the round-3 condition in AGENTS.md's 4b row and hold AGENTS.md at 200 lines; the criterion-23 test requires the loop text to name "three rounds" and "round 3 only when round 2 wrote" and the same limit in 2a and 6; `test_the_adr_draft_states_every_point` requires "at most three rounds" in ADR 0011 and in a matching design.md draft; `adr_0017_problems` / `test_adr_0017_supersedes_0015_and_keeps_the_repair_contract` require "round 3 requires a taken or fixed row in round 2" and "the maximum stays three rounds" in ADR 0017, and that ADR 0015's body stays untouched. The prior change `stage2-repair` documents the same mechanics in its research (`plans/changes/stage2-repair/research.md`, the paragraph on `RELEASED_COLUMNS`, `released_rows` and `rounds_run`).

## What is unclear

- Which model would serve round 4 and later. The ladder has exactly three rungs and `review_loop` refuses a round without a rung; ADR 0011 decision 3 fixes the mapping round *n* → `modelle[n-1]`. No record read states an answer.
- The meaning of one ADR sentence: decision 3 reads "Rounds 1 and 2 both run, each still held by an undecided row". The mechanism I found is `undecided_refusal` (a round is refused while rows stand undecided); whether the ADR sentence means exactly that hold rule is my reading, not a recorded statement.
- What "clean" means for the stop rule. Today's gate keys on statuses beginning `taken`/`fixed` (`taken_in_round`); a round with rows that are all rejected, and a round with no rows at all, are both "no taken row". The bead's phrase "until one finds nothing" is not defined anywhere I read.
- Whether ADR 0011 decision 8's bound ("the loop makes at most three calls per change", part of the accepted-terms reasoning) gets a replacement bound or rests on the subscription limits in `model-endpoints.yaml`. Not recorded.
- How the escalation rule (two consecutive `fix-r`-origin rounds go to the maintainer, not a third round) and an unbounded loop fit together. Not recorded.
- Ordering against the recorded swarm rules (coding-harness-4fk, coding-harness-icw) and the sibling loop change (coding-harness-mvk): nothing read states which lands first.
- The citation in `taken_in_round`'s docstring points at "ADR 0015, decision 5", but ADR 0015 is superseded by ADR 0017 and the rule now stands in 0017's decision 6. Whether the citation moves with this change is unrecorded.
- Not read: the bead `coding-harness-dx0` itself (the tracker is the Dolt database; no rendered copy is committed and I have no shell in this phase), and `plans/changes/coding-harness-dx0` does not exist — the change directory is `plans/changes/loop-until-clean/`.

## Not found

- `plans/specs/` holds one spec only (`implementation-verification/spec.md`); a search there for "review loop", "review-loop" and "round" found no match.
- `templates/` contains no occurrence of "three rounds" or "round 3"; the only round rule there is the `fix-r` escalation in `templates/findings.md` (Origin column).

## Which files a change would have to touch

Code and tests: `scripts/stage2.py` (`MAX_ROUNDS`, `review_loop`, `rounds_run`, `taken_in_round`, `ROUNDS_LINE`, the module docstring); `tests/test_stage2.py` (`test_a_round_without_a_finding_still_counts`, `test_a_call_without_an_answer_is_not_a_round`, `test_the_loop_stops_at_three_rounds`, `test_round_three_starts_only_after_a_taken_row`, `test_workflow_section_4_routes_the_three_reviews`, `agents_md_problems`, `test_agents_md_names_the_loop_and_the_runner`, the criterion-23 test, `test_the_adr_draft_states_every_point`, `adr_0017_problems`, `test_adr_0017_supersedes_0015_and_keeps_the_repair_contract`). Doctrine: `prompts/04b-review-loop.md`, `prompts/06-review.md`, `prompts/02a-spec-review.md`, `docs/WORKFLOW.md` (five places named above), `AGENTS.md` (two places, within its 200-line cap), `templates/findings.md` only if the escalation wording moves. Records: `docs/adr/0011-…md` (amendment), `docs/adr/0017-…md` (decision 6 says the maximum "stays" three rounds), `model-endpoints.yaml` only if the ladder itself changes. Status text: `ROADMAP.md` Now 3, `plans/INDEX.md` row for this research. Reporting only, if counts change shape: `scripts/handover_schema.py` (`review_rounds`) and `scripts/stage2_runs.py` (the ledger's round count).
