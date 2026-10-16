---
title: "Spec — loop-until-clean"
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
tags: [spec, stage2, review-loop, opencode-go, swarm]
class: feature
appetite: 8
change: loop-until-clean
adr_question: {proposed: "yes", reason: "It replaces the three-round budget of ADR 0011 (decisions 3 and 8) and ADR 0017 (decision 6) with rounds until a clean round on a free swarm and a named ladder, as the maintainer answered in Q-1 to Q-8."}
adr_files: [docs/adr/0021-review-swarms-until-clean.md]
---

# Spec — `loop-until-clean`

The goal in one sentence: after this change the review loop (phase 4b) runs
rounds until a round is clean — round 1 a parallel swarm of the OpenCode Go
models currently offered free over the implementation's diff alone, then one
rung of a named ladder per round — with the repair brake and the ladder's end
as the only stops (bead `coding-harness-4fk`, which took over
`coding-harness-dx0` by Q-4). Research: [research.md](research.md). Decisions:
[decisions.md](decisions.md), Q-1 to Q-8, answered by the maintainer on
2026-10-14. The ADR proposal takes effect only on merge.

## Problem

Read in this worktree on 2026-10-14; the research's statements stand against
`main` at `e0cea42` (research, "Runner exploration").

- **The loop stops at three rounds while the goal is a clean round.** The
  runner refuses a fourth round (`MAX_ROUNDS = 3`, `scripts/stage2.py`,
  `review_loop`), and the first night run hit exactly that: "Round 4 of the
  review loop was not possible: the runner stops at three rounds"
  (`docs/journal/handover/2026-10-12-night-run-first-rehearsal.md`, §4; bead
  coding-harness-dx0, ROADMAP.md Now 3: "review rounds until one finds
  nothing").
- **A clean round does not end the loop — it extends it.** Round 2 runs
  unconditionally after a finding-less round 1, and two clean rounds stop the
  loop with a refusal (`test_a_round_without_a_finding_still_counts`;
  ADR 0011 decision 3, "Rounds 1 and 2 both run"). That is the opposite of
  rounds until clean.
- **Round 1 runs one model, not a swarm.** The maintainer's swarm decision —
  the free models first, in parallel, on the implementation's code (Q-5, Q-8;
  handover 2026-10-14-night-run-third, "first stage all free models") — has no
  form in the runner: one call per round, one model per call.
- **The ladder holds three rungs of nine.** Six of the models the maintainer
  ordered (Q-1) are not declared anywhere, and a round past the third is
  refused because the ladder has no rung for it (`round_number > len(models)`,
  `scripts/stage2.py`).
- **Every statement of the round rule is written for three rounds.** The
  round-3 condition, the "at most three rounds" gate line and the
  "at most three calls per change" terms reasoning stand in eight files
  (research, "Where it lives"), and the fix-r escalation reads "not a third
  round" (`docs/WORKFLOW.md` §2; `templates/findings.md`) — a wording with no
  meaning in an unbounded loop.
- **A stale citation.** `taken_in_round`'s docstring cites "ADR 0015,
  decision 5", superseded by ADR 0017 on 2026-10-13 (research, "What is
  unclear").

## Terms

- **Free stage (the swarm)** — the models the `opencode-go` entry's free-stage
  list names: OpenCode Go models currently offered free, determined by a check
  before the stage runs; they review round 1 in parallel, and only the
  implementation's diff reaches them.
- **Ladder** — the entry's model list in order, after the free stage's
  members; one rung per round from round 2 on. **Rung** — one model of it.
- **Clean round** — a round none of whose rows has a Status beginning `taken`
  or `fixed`; a round that wrote no row is clean.
- **fix-r round** — a round with at least one taken row in which every taken
  row's Origin begins `fix-r`.
- **Fresh free check** — reading which models OpenCode Go currently offers
  free, before the free stage runs, and bringing the entry's free-stage list
  up to date.

## Acceptance criteria

1. When a round's decided rows contain no row whose Status begins `taken` or
   `fixed`, the loop is clean and the next `review-loop` call is refused with
   a refusal that names the clean round — after round 1 as after any later
   round.
   *Refuted by:* a second round that starts after a clean round 1, or a
   refusal that names a round cap instead of the round's cleanliness (today's
   behavior at round 2).

2. When the first round starts, the runner calls every model of the entry's
   free-stage list in parallel — each an isolated reviewer call of today's
   shape — and writes all their rows as one round: one heading, one id series
   `L1-<k>`, each row carrying its model in the Reviewer cell.
   *Refuted by:* a first round with one model, member calls run one after
   another, rows under two headings, or a row attributed to a model that did
   not write it.

3. While the free stage reviews, its calls carry the change's diff and the
   loop prompt and no repository read tools; the ladder's rounds keep the four
   read tools of today.
   *Refuted by:* a free-stage call with `read`, or a ladder round that loses
   its tools.

4. When a free-stage member's call fails, the round still stands with the rows
   of the members that answered and names the failed member in the round's
   block; a round in which no member answered writes nothing.
   *Refuted by:* a whole round discarded over one member, rows written from a
   failed call, or a round written from no answer at all.

5. Before the free stage runs, the fresh free check is made and the entry's
   free-stage list brought up to date, with the check's date in the entry's
   remark; a free model the entry does not declare is named — in the run's
   record or handover — and not called.
   *Refuted by:* a swarm calling a model the entry does not list, or the loop
   prompt, `docs/WORKFLOW.md` §4 and the entry's remark stating no check.

6. When a model joins the ladder, the entry's remark carries the reading of
   its data terms — retention and training — with the date it was read; a
   model whose terms show retention or training, or cannot be read, is not on
   the ladder and is named in the change's findings.
   *Refuted by:* a new ladder model without a dated terms reading, or one with
   retention or training on the ladder.

7. While the free stage's models may run with unread data terms — the
   acceptance recorded in the entry's remark, because only the implementation's
   diff reaches them — no ladder model runs on unread terms.
   *Refuted by:* a ladder model without a terms reading riding the free
   stage's acceptance, or the acceptance absent from the remark.

8. When round *n* (n ≥ 2) starts, it calls the (n−1)-th rung of the entry's
   ladder in the entry's order, and no model id stands as a literal in the
   runner.
   *Refuted by:* a skipped or repeated rung, or an id literal in
   `scripts/stage2.py`.

9. When the last rung's round has left a taken row, the next `review-loop`
   call is refused with a report that names the maintainer; the last rung is
   not repeated, and no model is substituted for a rung the address refuses.
   *Refuted by:* a round past the ladder's last rung, a repeated last rung, or
   a fallback model after a refused id.

10. When each of two consecutive rounds left at least one taken row and every
    taken row of both has Origin `fix-r`, the next round is refused with a
    report that names the maintainer — at any round number, before the ladder
    ends.
    *Refuted by:* a round that starts after two fix-r rounds, or a brake that
    fires while a taken row of Origin `base` stands in either round.

11. When a round's taken row is repaired to `fixed`, it still counts as taken
    for the next round's admission and for the run count.
    *Refuted by:* a repaired row cancelling the next round or shrinking the
    count.

12. When a row of the record stands undecided, the next round and the release
    are still refused.
    *Refuted by:* a round starting over an undecided row, or a release with
    one.

13. When rounds are released into `findings.md`, the `Rounds run:` line and
    the next `review-loop` call still count every round — a free-stage round's
    heading included — at any round number.
    *Refuted by:* a round heading the counter cannot read, or a round lost
    from the count after its release.

14. When `probe` runs, it makes one call per model the entry lists for the
    loop — free stage and ladder alike — with the declaration and the leak
    check in front of each.
    *Refuted by:* a declared loop model the probe skips, or a probe call
    without its checks.

15. When the loop's rule is stated in the repository, every statement agrees:
    rounds run until a clean round, round 1 is the free swarm on the diff
    alone, the ladder bounds the loop, two fix-r rounds stop it — in
    `AGENTS.md` (the 4b row and the Stage-2 paragraph, within its 200-line
    cap), `docs/WORKFLOW.md` (the phase table, §2's escalation sentence, the
    model table, the verb list, §4's loop and repair sections),
    `prompts/02a-spec-review.md`, `prompts/04b-review-loop.md`,
    `prompts/06-review.md`, `templates/findings.md`'s Origin note, and the
    runner's module docstring and help; no live text says "at most three
    rounds" or a round-3 condition; and `taken_in_round`'s docstring cites
    ADR 0017 decision 6 as amended by ADR 0021, not the superseded ADR 0015.
    *Refuted by:* a leftover "three rounds" or round-3 sentence, two
    disagreeing statements, or the stale citation.

16. When the decision pull request carries ADR 0021, it amends ADR 0011's
    decisions 3 and 8 and ADR 0017's decision 6, states the clean stop, the
    free swarm with its diff-only confinement, the ladder with its terms rule,
    the fix-r brake and the new call bound, and changes neither amended
    record's body.
    *Refuted by:* a rewritten sentence in ADR 0011 or ADR 0017, or a point
    missing from ADR 0021.

## Non-goals

- The research swarm (bead coding-harness-icw): phase 1 keeps GLM 5.3 Flash;
  Q-8's narrowing of the free-models rule is recorded here for that change to
  read, not built.
- Round 1 reading the code's structure first (coding-harness-mvk), the live
  view of a round (coding-harness-uco) and the diagnostics of failed attempts
  (coding-harness-cit): separate beads, untouched.
- The phase-6 reviewer (Codex), the spec review (2a, Opus 5.5), the repair
  routing of ADR 0017, the evidence rule, `Broke a test` ownership, the loop
  record's place outside the worktree, and the verdict-before-release order.
- A numeric round cap of any height, a repeat of the last rung, or an
  automatic model substitution after a refused id.
- The runner fetching the vendor's free list or terms pages itself: the fresh
  free check and the terms readings are the orchestrator's steps; the runner
  stays offline and calls what the entry declares.
- The German keys of `model-endpoints.yaml` and any translation of them, and
  anything of stage 1 or the interactive `session` verb beyond the
  declaration's reading of the entry.

## Protected areas

- `scripts/leakcheck.py`, `provenance.yaml`, `decisions/gates.yaml` and
  `.claude/settings.json`: the change uses the existing checks and permission
  policy.
- The bodies of ADR 0011 and ADR 0017 (and every other record under
  `docs/adr/`): the amendment is stated in ADR 0021 alone, and no D- or
  O-number moves, so `scripts/check_decision_continuity.py`'s map changes
  nothing.
- `model-endpoints.yaml`'s German keys, and the run-count schema, parser and
  probe of `scripts/stage2_runs.py` beyond a stale comment.
- `AGENTS.md`'s 200-line cap.
- Customer instances and everything outside this worktree.

## Definition of Done

- `verify` green once the maintainer's stated ADR answer is recorded; every
  criterion has its ledger evidence.
- Moved in the same pull request: `scripts/stage2.py`,
  `tests/test_stage2.py`, `model-endpoints.yaml`,
  `prompts/02a-spec-review.md`, `prompts/04b-review-loop.md`,
  `prompts/06-review.md`, `docs/WORKFLOW.md`, `AGENTS.md`,
  `templates/findings.md`, `docs/adr/0021-review-swarms-until-clean.md` and
  `ROADMAP.md` — or the row that says why a file stayed.
- The pull request's file list shows the protected areas untouched and the
  non-goals unbuilt.
- Bead: the pull request closes `coding-harness-4fk`, and its last commit
  carries the trailer `Closes-Bead: coding-harness-4fk`.
- Special runs: the compatibility probe over every newly declared id — one
  call each, the id and the first line of its answer in the pull request
  body — and this change's own review loop running under the new code.

## Open decisions

None open. Q-1 to Q-8 settle the ladder and its order, the meaning of clean,
the brake, the merge with the swarm bead, the parallel first round, the
ladder's end, the terms rule and the free first stage; the ADR-question answer
is still owed to the orchestrating session and is not recorded by this draft.

I decided the following reversible details and recorded their reasons:

- `[DETAIL]` Class `feature`, ADR question proposed "yes": the change replaces
  the round budget inside the existing runner and adds a stage to an existing
  loop — no new subsystem — while its subject is an ADR-level decision.
- `[DETAIL]` Appetite 8 hours of phase 4, repair rounds included, as a stop;
  the runner work, six declarations with live terms readings and the doctrine
  sweep are each bounded and known from research.
- `[DETAIL]` The free stage's membership is the entry's free-stage list, and
  the fresh free check updates that list before the stage runs: the yaml
  stays what the runner calls, so Q-7's declaration rule and Q-8's fresh check
  hold without giving the runner a network call. A free model found but not
  declared is named, not called.
- `[DETAIL]` The free stage's calls carry no repository read tools (Pi's
  measured `--no-tools`): the maintainer's condition "only the implementation's
  code is read" is a lock there or not at all — Pi confines nothing
  (ADR 0011 decision 4).
- `[DETAIL]` An empty free-stage list refuses the run and names it, because a
  silent re-route onto the ladder would blur which stage a round belongs to.
- `[DETAIL]` The ids take the entry's lowercase form (`glm-5.3-flash`,
  `qwen3.8-flash`, `gpt-6-luna`, `claude-haiku-5.5`, `minimax-m2.7`,
  `longcat-2.0`); the probe measures each against the address, and a refused
  id stops the run (criterion 9) rather than moving the spelling silently.
- `[DETAIL]` ADR 0021 amends ADR 0011 and ADR 0017 without touching their
  files, following the ADR 0007/0011 precedent; `adr_files` therefore lists
  only the new record. 0018 was the first free number on 2026-10-14; 0018 to 0020 were taken or claimed by 2026-10-16, so the record is 0021.
- `[DETAIL]` A free-stage round's heading joins its members comma-separated
  without spaces, so the round counter's heading regex reads it unchanged.
