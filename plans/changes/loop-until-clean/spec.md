---
title: "Spec — loop-until-clean"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-16
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-4fk
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, review-loop, opencode-go, swarm]
class: feature
appetite: 8
change: loop-until-clean
adr_question: {proposed: "yes", reason: "It replaces the three-round budget of ADR 0011 (decisions 3 and 8) and ADR 0017 (decision 6) with rounds until a clean round on a free swarm and a named ladder, as the maintainer answered in Q-1 to Q-8."}
adr_files: [docs/adr/0021-review-swarms-until-clean.md]
---

# Spec — `loop-until-clean`

The goal in one sentence: phase 4b reviews until a decided round leaves no
accepted finding, starting with a free swarm, then a three-Flash swarm, then
single-model rounds, bounded by the declared ladder and the repair brake
(bead `coding-harness-4fk`, implementation review as a swarm).
Research: [research.md](research.md). Decisions: [decisions.md](decisions.md),
Q-1 through Q-10 and the details of 2026-10-16; Q-10 replaces Q-5's round
number, and Q-9 replaces the earlier draft's per-free-model declaration.
The proposal takes effect on merge; this draft implements nothing.

## Problem

Evidence in `research.md`, exploration of 2026-10-14 at `e0cea42`:

- The runner refuses round 4 even with accepted findings: `MAX_ROUNDS = 3`
  in `scripts/stage2.py`, encountered in the first night run's handover of
  2026-10-12, section 4.
- A finding-less first round still admits round 2; the existing test
  `test_a_round_without_a_finding_still_counts` pins this behavior.
- Every round makes one reviewer call; neither parallel swarm exists.
- The configured ladder has three models, against the maintainer's nine
  named models; the doctrine and its tests repeat the three-round budget.
- `taken_in_round` cites superseded ADR 0015 instead of ADR 0017 decision 6.

## Terms

- **Accepted finding** — a row whose Status begins `taken` or `fixed`;
  fixing a finding preserves the fact that the review accepted it.
- **Clean round** — a completed round with all rows decided and no accepted
  finding; no rows or all rejected rows count as clean (Q-2).
- **Free swarm** — round 1, all distinct `opencode-go` model ids ending in
  `-free` returned by the pinned Pi's check for this run, reviewed in parallel.
- **Flash swarm** — round 2, the eligible members of DeepSeek V4.1 Flash,
  MiMo-V2.6-Flash and LongCat-2.0 reviewed in parallel (Q-10).
- **Ladder** — the nine named paid models of Q-1, the first three grouped
  into round 2; each remaining eligible model gets one later round in order.
- **Free check** — invocation of the repository-pinned Pi's `--list-models`
  before round 1, filtering exact provider `opencode-go` and suffix `-free`.
  This checks the installed catalog afresh, not the vendor's live offer or
  billing: its freshness is limited by the Pi pin. The list is not evidence
  that the provider actually bills a call at zero cost.
- **fix-r round** — a round with an accepted finding in which every accepted
  row's Origin begins `fix-r` (the repair that caused it).
- **Implementation diff** — source-code and test changes against the merge
  base with `origin/main`, including staged, unstaged and untracked code,
  with only bounded hunk context; no plans, decisions, documentation,
  endpoint declarations, unrelated files or added repository-reading instructions
  outside the quoted source hunks.

## Acceptance criteria

1. When a completed round is clean, the next `review-loop` call refuses
   further review and names the clean round, including after round 1.
   *Refuted by:* another reviewer call after a clean round, including a
   round containing only rejected findings.

2. When a swarm round starts, every eligible member is called in parallel
   and its findings form one round with unique `L<n>-<k>` ids and the actual
   model in each row's Reviewer cell.
   *Refuted by:* serial member calls, missing or misattributed rows, colliding
   ids, or more than one heading for round 1 or round 2.

3. While the free swarm reviews, its only repository content is the
   implementation diff and it has no tools; paid rounds retain today's
   `read,grep,find,ls` tools.
   *Refuted by:* a free call receiving plan/documentation canaries, a whole
   source file outside hunk context, an added repository-reading instruction
   outside quoted source hunks or a tool, or round 2 losing the paid reviewers' tools.

4. When a swarm member fails, the round records the failure beside the
   answering members' rows, but no round is completed if every member fails.
   *Refuted by:* discarding successful members, inventing findings for failed
   members, or counting an all-failed round as clean.

5. When round 1 of a review-loop run is admitted, the runner checks the
   pinned Pi's free list before review calls and records its date and exact
   member list, automatically admitting newly found free Go models without
   per-model YAML entries.
   *Refuted by:* reusing yesterday's list, excluding an undeclared matching
   Go model, calling a Zen model, omitting the recorded date/list, or making
   a model call after an empty, failed or unreadable check.

6. When a paid model is admitted to either paid stage, its declaration
   contains a dated reading of retention and training terms; unreadable or
   retaining/training models are skipped and named for the handover.
   *Refuted by:* a paid call without that reading or a silently omitted
   ineligible model.

7. While unread terms are accepted for the free stage, that permission is
   declared as a class confined to discovered free Go models on the diff.
   *Refuted by:* a paid or Zen call admitted under that class, a guessed
   `-free` id not in this run's discovery, or no declared acceptance.

8. When a paid round is admitted, round 2 calls the eligible first three
   models together and subsequent rounds call one remaining eligible rung
   each in Q-1 order, with model ids held in configuration rather than code.
   *Refuted by:* treating the first three as three sequential rounds,
   interleaving a later rung, repeating a consumed rung, or hardcoding ids.

9. When no eligible paid stage remains after a non-clean round, the loop
   stops with a report to the maintainer and substitutes no model.
   *Refuted by:* repeating the final rung, another address/model after a
   refused id, or reporting exhaustion as a clean result.

10. When the last two consecutive rounds are fix-r rounds, the next round
    refuses and reports to the maintainer, regardless of its round number.
    *Refuted by:* a further call after two such rounds, or a brake firing
    when either round has an accepted `base` finding.

11. When an accepted row becomes `fixed`, it remains accepted for admitting
    the next round and counting the run.
    *Refuted by:* a repair turning the preceding round clean or reducing
    the recorded round count.

12. When a record has an undecided row, the next round and release remain
    refused under today's row-decision and `Broke a test` rules.
    *Refuted by:* a reviewer call or release over an undecided row or a fixed
    row missing its required evidence mark.

13. When rounds are released into `findings.md`, every completed round and
    its admission state remain recoverable for subsequent calls.
    *Refuted by:* lost swarm counts, a clean/brake/exhaustion stop bypassed
    after release, or replaying a consumed model after configuration changes.

14. When `probe` runs, it checks each distinct discovered free model and
    eligible declared paid model once, with declaration and leak checks
    before every model call.
    *Refuted by:* a missing member, repeated probe call, an unchecked call
    or a free probe gaining repository tools or content beyond criterion 3.

15. When live repository text describes phase 4b, it agrees on the two swarms,
    automatic Go discovery with its pin limitation, clean stop, paid ladder
    bound and repair brake, with no operative three-round rule.
    *Refuted by:* a conflicting sentence in `AGENTS.md`, `docs/WORKFLOW.md`,
    `prompts/02a-spec-review.md`, `prompts/04b-review-loop.md`,
    `prompts/06-review.md`, `templates/findings.md`, the endpoint remark or
    runner help/docstrings, an obsolete ADR 0015 citation, or AGENTS.md
    exceeding its existing 200-line limit.

16. When this decision pull request carries ADR 0021, it amends ADR 0011
    decisions 3 and 8 and ADR 0017 decision 6 with the agreed two-swarm
    structure, automatic free discovery, privacy exception, stops and call
    bound, preserving both older records' bodies.
    *Refuted by:* an omitted agreement, the old per-free-model admission
    rule, a sequential Flash round, or rewriting either historical body.

## Non-goals

- Research swarm, structure-first review, live progress display and failure
  diagnostics; spec-review and phase-6 model routing; repair routing.
- Changing the phase-6 verdict-before-release order, row evidence ownership,
  the external location of the loop record, or stage 1 and interactive sessions.
- An arbitrary round cap, repeated final models or automatic address/model
  fallbacks; a vendor catalog updater or a billing-verification service.
- A free stage with full repository access or paid models using the free
  class exception; translating existing German configuration keys.

## Protected areas

- `scripts/leakcheck.py`, `provenance.yaml`, `decisions/gates.yaml`,
  `.claude/settings.json`: retain the existing security and permission policy.
- Existing ADR bodies and `scripts/check_decision_continuity.py`: the new
  record amends ADRs without changing a D- or O-number or its continuity map.
- `scripts/handover_schema.py` and `scripts/stage2_runs.py`: current numeric
  fields already allow more than three rounds; preserve their schema.
- Customer instances and paths outside this worktree; AGENTS.md's line cap.

## Definition of Done

- All ledger evidence passes and `make verify` is green.
- The same pull request carries the runner, its tests, the endpoint entry,
  doctrine paths in criterion 15, `ROADMAP.md`, the runner-generated
  `plans/INDEX.md` and `docs/adr/0021-review-swarms-until-clean.md`.
- The file list leaves protected areas and non-goals untouched.
- The pull request closes the implementation-review swarm work item
  (`coding-harness-4fk`); its final commit has `Closes-Bead: coding-harness-4fk`.
- Phase 4 records dated paid-terms sources and skipped ids for the handover;
  the compatibility probe and this change's own new loop have evidence with
  their commits in the decision pull request. No live provider call is made
  merely to draft these files.

## Open decisions

None open. The maintainer's Q-9 and Q-10 settle discovery and the Flash round;
`decisions/answers/loop-until-clean/adr.yaml` already records the ADR answer
on 2026-10-16 and is not changed here.

I decide the following reversible details and state their reasons:

- `[DETAIL]` Keep class `feature`, the existing ADR proposal and appetite
  eight hours: this redraft corrects the recorded interpretation of the same
  runner change, without widening its budget or replacing a human answer.
- `[DETAIL]` The entry declares the free stage as a class; a run-local
  discovery snapshot supplies its members, so Q-9 requires no YAML edits.
  An empty or failed discovery refuses rather than silently skipping stage 1.
- `[DETAIL]` Round 2 retains paid read tools. Only the free stage was limited
  to the implementation diff; Q-10 does not extend that exception.
- `[DETAIL]` Partial swarm success remains a completed, visibly partial
  round under criterion 4; its successful rows decide clean under Q-2.
  An empty or unparseable answer is failure, not proof of no finding.
- `[DETAIL]` Pin the paid stage membership and skipped ids for the run,
  retaining stage consumption through release: an edited YAML must not replay
  already-used reviewers. Failure before a completed round consumes no stage.
- `[DETAIL]` Preserve duplicate reports with separate ids and reviewers;
  the orchestrator rejects duplicates explicitly, avoiding silent loss.
- `[DETAIL]` ADR 0021 is the existing unmerged draft for this change, already
  named by the maintainer's ADR answer; update it rather than create 0022.
