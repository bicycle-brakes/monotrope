---
title: "Spec — loop-until-clean"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-16
updated: 2026-10-17
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
Q-1 through Q-10 and both addenda of 2026-10-16; Q-10 replaces Q-5's round
number, Q-9 replaces per-free-model declarations, and the final addendum
requires a forced live catalog refresh and a configurable free-selection rule.
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

The decisions addendum after `a0d5bc8` corrects that draft's catalog claim:
the recorded Pi 1.2.0 source reading found a remote catalog on `pi.dev`,
normally cached for four hours, with `pi update models` forcing a refresh.
Merely listing installed models does not meet the live-check requirement.

## Terms

- **Accepted finding** — a row whose Status begins `taken` or `fixed`;
  fixing a finding preserves the fact that the review accepted it.
- **Clean round** — a completed round with all rows decided and no accepted
  finding; no rows or all rejected rows count as clean (Q-2).
- **Free swarm** — round 1, all distinct models in this run's freshly
  retrieved catalog selected by the configured free-stage rule, in parallel.
  Initially the rule selects provider `opencode-go`, ids ending `-free`,
  plus dated, reasoned inclusions, minus dated, reasoned exclusions; Zen
  models remain excluded regardless of an inclusion.
- **Flash swarm** — round 2, the eligible members of DeepSeek V4.1 Flash,
  MiMo-V2.6-Flash and LongCat-2.0 reviewed in parallel (Q-10).
- **Ladder** — the nine named paid models of Q-1, the first three grouped
  into round 2; each remaining eligible model gets one later round in order.
- **Free check** — a forced network refresh of Pi's catalog followed by
  listing and selecting models for this run. The live source is `pi.dev`,
  not OpenCode Go's own model endpoint; no stale-cache fallback is allowed.
  Catalog membership is not a measurement of actual zero-cost billing.
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
   Q-13: a failed Flash member is replaced by the cheapest admitted model not
   in the round and not consumed, on the same paid prompt, then by the next,
   each model at most once, until one answers or the ladder is spent; each
   swap is recorded as `<model> failed: <reason>; replaced by <model>` and
   printed, the reason naming the last scrubbed line of Pi's standard error,
   and a printed stderr tail carries the member's model id.
   *Also refuted by:* a failed Flash member left unreplaced while an
   unconsumed rung exists, a replacement called twice or left as a later
   rung, a swap neither recorded nor printed, a reason without Pi's last
   error line, or a changed `flash_swarm` list (it stays hand-kept; a
   differing set from the three cheapest gets a notice and a record line,
   never a refusal).

5. When a fresh review-loop run is admitted, its free membership is selected
   from a successfully forced live Pi catalog refresh by the YAML free-stage
   rule, with the check time and exact resulting list recorded.
   *Refuted by:* listing before refresh, reusing a four-hour cache after a
   failed/timed-out refresh, excluding a newly matching Go id merely because
   it has no individual declaration, calling Zen or an excluded/absent id,
   omitting the check time/list, launching after an empty/unreadable check,
   or needing a runner-code edit to change the provider/match/include/exclude
   rule. Include/exclude entries without a date or reason also refute it.
   Q-13: only ids in the freshly fetched overlay that the refresh persisted
   are selected; an id only Pi's shipped list carries is not. *Also refuted
   by:* selecting such an id, or a refresh that left no readable overlay
   still starting the free stage. A non-free overlay id without a
   `modelle_terms` record is named (stderr, one record line) and never
   admitted.

6. When a paid model is admitted to either paid stage, its declaration
   contains a dated reading of retention and training terms; unreadable or
   retaining/training models are skipped and named for the handover.
   *Refuted by:* a paid call without that reading or a silently omitted
   ineligible model. Fail closed: `gelesen` must be an ISO date
   (YYYY-MM-DD) and an empty `uebersprungen` counts as absent only beside a
   valid `gelesen`; a non-date, a bare boolean or a missing date admits
   nothing.

7. While unread terms are accepted for the free stage, that permission is
   declared as a class confined to discovered free Go models on the diff.
   *Refuted by:* a paid or Zen call admitted under that class, a guessed
   `-free` id not in this run's discovery, or no declared acceptance.

8. When a paid round is admitted, round 2 calls the eligible first three
   models together and subsequent rounds call one remaining eligible rung
   each cheapest first (Q-13: the runner orders the `modelle` set by the
   declared `anfragen_5h`, descending, ties by id, a model without the value
   last and named), with model ids and cost values held in configuration
   rather than code.
   *Refuted by:* treating the first three as three sequential rounds,
   interleaving a later rung, repeating a consumed rung, hardcoding ids, an
   order that follows list position instead of `anfragen_5h`, or a model
   without the value dropped silently instead of ordered last and named.

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
    live Pi catalog discovery and its source limitation, the configurable
    free-selection rule, clean stop, paid ladder
    bound and repair brake, with no operative three-round rule.
    *Refuted by:* a conflicting sentence in `AGENTS.md`, `docs/WORKFLOW.md`,
    `prompts/02a-spec-review.md`, `prompts/04b-review-loop.md`,
    `prompts/06-review.md`, `templates/findings.md`, the endpoint remark or
    runner help/docstrings, an obsolete ADR 0015 citation, or AGENTS.md
    exceeding its existing 200-line limit.

16. When this decision pull request carries ADR 0021, it amends ADR 0011
    decisions 3 and 8 and ADR 0017 decision 6 with the agreed two-swarm
    structure, live free discovery and configurable selection, privacy exception, stops and call
    bound, preserving both older records' bodies.
    *Refuted by:* an omitted agreement, the old per-free-model admission
    rule, a sequential Flash round, or rewriting either historical body.

## Non-goals

- Research swarm, structure-first review, live progress display and failure
  diagnostics; spec-review and phase-6 model routing; repair routing.
- Changing the phase-6 verdict-before-release order, row evidence ownership,
  the external location of the loop record, or stage 1 and interactive sessions.
- An arbitrary round cap, repeated final models or automatic address/model
  fallbacks; replacing Pi's catalog with OpenCode Go's own endpoint or adding
  a billing-verification service.
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

None open. The maintainer's Q-9, Q-10 and final addendum settle live discovery,
configurable selection and the Flash round;
`decisions/answers/loop-until-clean/adr.yaml` already records the ADR answer
on 2026-10-16 and is not changed here.

I decide the following reversible details and state their reasons:

- `[DETAIL]` Keep class `feature`, the existing ADR proposal and appetite
  eight hours: this redraft corrects the recorded interpretation of the same
  runner change, without widening its budget or replacing a human answer.
- `[DETAIL]` The entry declares the free stage as a class; a run-local
  snapshot supplies its members without individual declarations. Apply
  includes only to ids present under the configured provider in that live
  catalog; exclusions win over matches and includes. This makes exceptions
  editable without guessing ids or admitting Zen. Invalid rules, an empty
  selection or failed refresh/listing refuse rather than skipping stage 1.
- `[DETAIL]` Force `tools/pi/pi update models` before `--list-models` in
  one scratch agent directory per fresh run/probe, with a timeout. Record
  UTC check time, source `pi.dev`, Pi version, rule, catalog and selected ids;
  this proves the chosen source was refreshed, not actual free billing.
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
