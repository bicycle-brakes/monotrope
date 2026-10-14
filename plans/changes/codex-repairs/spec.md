---
title: "Spec — codex-repairs"
status: draft
implementation_status: none
date: 2026-10-13
last_reviewed: 2026-10-13
updated: 2026-10-13
supersedes: null
superseded_by: null
bead: coding-harness-0ga
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, repair, codex]
class: feature
appetite: 4
change: codex-repairs
adr_question: {proposed: "yes", reason: "It replaces the repair routing and reviewer separation of ADR 0015 with Codex repairs and a fresh Codex re-check, as requested in the interview."}
adr_files: [docs/adr/0015-glm-5-3-repairs-taken-findings.md, docs/adr/0017-codex-repairs-taken-findings.md]
---

# Spec — `codex-repairs`

Taken review findings are repaired by Codex (`gpt-6.1-sol`), with the existing
evidence and checkpoint rules and a fresh Codex session for the phase-6
re-check (bead coding-harness-0ga). Research: [research.md](research.md).
Decisions: [decisions.md](decisions.md), Q-1 to Q-5, answered by the maintainer
on 2026-10-13. The ADR proposal takes effect only on merge.

## Problem

The exploration read the existing route against `origin/main` at `3199a28`
and the runner against `9ddb38a` on 2026-10-13 (research, "Where it stands"
and "Runner exploration").

- Repairs use GLM 5.3 twice before Sonnet 5.5, spending the Z.ai budget the
  maintainer reported exhausted; the requested Codex route does not exist.
- The shared attempt loop can start only Claude Code, although the drafting
  route already starts Codex for a writing task in its workspace sandbox.
- The current doctrine prohibits a reviewer from repairing its own findings.
  Codex already reviews phase 6, so moving its repairs requires the explicit
  exception the maintainer chose: the same model, in a fresh re-check session.

## Terms

- **Taken finding:** a loop-record row, a released loop row or a phase-6 row
  whose Status begins `taken`; the orchestrator has decided to repair it.
- **Post-run failure:** a completed model call is rejected by preparation,
  verification, the measured-time check or the repair-answer/evidence check;
  inability to start a required runner command retains its existing stop
  behavior and does not advance the chain.
- **Call failure:** the model process cannot start or finish successfully, or
  its transport response lacks the required answer file or thread event,
  or the answer is empty (amended 2026-10-13, phase 2a F-3: as the Claude Code
  path treats an empty answer today); this is distinct from a repair answer
  rejected by a post-run check.
- **Fresh session:** a new Codex call without `resume`; a read-only re-check
  receives neither the repair thread nor its conversation history.

## Acceptance criteria

1. When `repair <change>` runs with Stage 2 on, its first attempt uses Codex
   `gpt-6.1-sol` at effort `max`.
   *Refuted by:* a first repair attempt on GLM, Flash, Sonnet or another effort.

2. When a Codex repair attempt starts, it uses the existing Codex writing
   configuration: `workspace-write`, hooks and memories disabled, and no
   added directory, automatic approval or sandbox bypass.
   *Refuted by:* a read-only repair, an enabled discovery feature or a widening flag.

3. When a repair attempt starts, it receives all taken findings from both
   phases in one batch under the existing repair-input contract.
   *Refuted by:* an omitted source, a separate call per row, a rejected or fixed
   row listed for repair, missing spec/plan inputs, or unreleased loop rows
   copied into the worktree by the runner.

4. If the first completed Codex attempt fails a post-run check, exactly one
   fresh Codex attempt follows with that attempt's diagnostics.
   *Refuted by:* no retry, a resumed repair thread, another model or omitted diagnostics.

5. If the second completed Codex attempt fails a post-run check, the last
   attempt uses Sonnet 5.5 at effort `medium` with both attempts' diagnostics.
   *Refuted by:* GLM as fallback, missing earlier evidence or a fourth attempt.

6. If a repair model call fails, the run stops without another model call or
   a runner checkpoint.
   *Refuted by:* automatic fallback after an unavailable Codex call or a
   checkpoint after that failure; while HEAD is unchanged, the existing
   baseline restoration must still remove the failed call's edits.

7. When `repair <change> --stage2-off <reason>` runs, Sonnet 5.5 alone repairs
   the findings with the supplied reason recorded in findings and plan.
   *Refuted by:* a Codex/GLM call, a second Sonnet attempt, a lost reason or a
   route entry counted as measured time.

8. When any repair route runs, it requires no GLM credential.
   *Refuted by:* reading `GLM_KEY`, refusing because it is missing or passing
   Z.ai authentication into a repair call.

9. When any repair attempt is due, its endpoint and model must pass the
   existing declaration check before the call starts.
   *Refuted by:* an undeclared Codex or Sonnet attempt reaching its endpoint.

10. If the leak check blocks the exact prompt of any repair attempt, no
    further repair model call starts.
    *Refuted by:* a call on the blocked prompt or a fallback after the block.

11. When any repair attempt starts, its existing audit-line format records
    the actual route, endpoint, model and later-attempt reason for the run count.
    *Refuted by:* a Codex repair counted as GLM, an unreadable audit line or a
    missing reason for the retry or Sonnet fallback.

12. When a repair attempt fails a post-run check, its audit line is followed
    by the existing quoted diagnostics and changed-file evidence.
    *Refuted by:* lost evidence, model-written finding statuses surviving the
    failure, or diagnostics of a failed attempt absent from the next prompt.

13. If verification is red or the measured-time entry is missing, the repair
    attempt cannot produce a checkpoint.
    *Refuted by:* a runner commit despite red `make verify` or unchanged time evidence.

14. When a repair passes all checks, the runner produces exactly one clean
    descendant checkpoint with the existing fixed-status bookkeeping.
    *Refuted by:* zero or multiple commits, a dirty tree, an incorrect fixed
    status, another finding altered, or the private loop record marked before
    the checkpoint succeeds.

15. When a code finding is fixed, its named test must demonstrate the failure
    against the baseline's code under the existing red-first proof.
    *Refuted by:* accepting a missing test, a test already green on the
    baseline or an interpreter failure as proof that the defect was shown.

16. When a finding is answered `fixed — not a test — <reason>`, that exception
    is accepted only if the orchestrator took it as `not a test`.
    *Refuted by:* a code finding escaping its test requirement or a taken text
    finding losing its fixed status and reason.

17. If a Codex repair call moves HEAD, the runner stops before restoration,
    further model calls or its own checkpoint, without rewriting that history.
    *Refuted by:* resetting the model's commit, continuing verification or
    fallback, or adding a runner commit after HEAD moved.

18. When phase 6 re-checks repaired phase-6 findings, it starts a fresh
    read-only Codex session. A `review` run is a re-check when `findings.md`
    already holds a `## Phase 6` block; the first phase-6 review keeps its
    existing session rule (ADR 0016, decision 6) unchanged (amended
    2026-10-13, phase 2a F-1).
    *Refuted by:* resuming the repair thread, a prior phase-6 thread or a
    historical Codex phase-2a thread, or giving the verdict call write access.

19. When `repair` finishes, re-checking and the loop's `Broke a test` mark
    remain the orchestrator's next action under the existing round budget.
    *Refuted by:* `repair` starting a review, setting the mark or adding a loop round.

20. When current instructions describe repairs, the runner help and comments,
    workflow, repository rules, phase prompts and endpoint remarks agree on
    the Codex route and fresh-session re-check exception.
    *Refuted by:* an active GLM repair instruction, a blanket ban contradicting
    the exception, or a claim that Codex lacks command tools or that its
    configured sandbox was measured by the tests. The repair text sent to a
    Codex attempt (`REPAIR_FORMAT` and the phase prompt it carries) says Codex
    may run tests and `make verify` but must not commit or run any git command
    that changes the repository; the Sonnet attempt keeps its file-tools
    sentence (amended 2026-10-13, phase 2a F-2).
    *Also refuted by:* a Codex repair prompt saying it cannot run commands, or
    one without the no-commit instruction.

21. When the decision pull request introduces the new repair ADR, it
    supersedes ADR 0015 while preserving that record as marked history.
    *Refuted by:* rewriting ADR 0015's decision body, omitting its supersession
    marker or dropping its unchanged evidence, status or loop-budget rules
    from the replacement.

## Non-goals

- Changing the initial phase-4 implementer, Explore, the drafting fallback,
  the spec reviewer, the review-loop ladder or its round budget.
- An automatic budget/availability switch, a GLM repair fallback, a different
  phase-6 model or an additional review round.
- Changing the red-first proof for test-strength findings, adding call time
  limits or broadening enforcement of Codex's reads and sandbox.
- Rewriting historical change specs, decisions, findings or audit lines.

## Protected areas

- Other ADRs and the decision-continuity map: no D- or O-number changes.
- `scripts/leakcheck.py`, `provenance.yaml`, `decisions/gates.yaml`, the ADR
  answer format and `.claude/settings.json`: the routing change uses the
  existing declarations, gates and permission policy.
- The run-count schema, parser and probe: they already support Codex audit
  lines and retain historical GLM routes; only the outdated route comment
  needs correction (`scripts/stage2_runs.py`).
- Customer instances and files outside this worktree: framework work only.

## Definition of Done

- `make verify` green once the orchestrating session records the maintainer's
  stated ADR answer; every criterion has its ledger evidence.
- The same decision pull request carries `scripts/stage2.py`,
  `tests/test_stage2.py`, the route comment in `scripts/stage2_runs.py`,
  `AGENTS.md`, `docs/WORKFLOW.md`,
  `model-endpoints.yaml`, `prompts/04-implement.md`,
  `prompts/04b-review-loop.md`, `prompts/06-review.md`, ADR 0017 and ADR 0015's
  history marker.
- The file list demonstrates the protected areas and non-goals are respected.
- The pull request closes `coding-harness-0ga`; its closing commit carries
  `Closes-Bead: coding-harness-0ga`.
- Special runs: none required; stand-in tests show configured calls, not the
  real CLI's confinement or a measured live repair.

## Open decisions

None open. Q-1 to Q-5 settle the model, findings, fallback, explicit outage
switch and supersession; the ADR-question answer is still owed to the
orchestrating session and is not recorded by this draft.

I decided the following reversible details and recorded their reasons:

- `[DETAIL]` Class `feature`: this replaces routing within an existing runner
  without adding a subsystem or breaking its command interface; phase 2b runs
  because the change proposes an ADR.
- `[DETAIL]` Appetite: 4 hours of phase 4, repair rounds included, as a stop;
  existing transports and repair checks make this a bounded delivery effort.
- `[DETAIL]` Audit routes `codex`, `codex-repair`, `stage-1`: reuse the
  drafting route names and existing audit schema instead of adding a format.
- `[DETAIL]` ADR 0017: 0016 is the highest ADR in this worktree on 2026-10-13;
  only the new draft is written here, and phase 4 adds ADR 0015's marker.
- `[DETAIL]` (2026-10-13, phase 2a) F-1: a re-check is a `review` run with
  an earlier `## Phase 6` block in `findings.md`, the one marker every
  re-check has and no first review has; the first review's resume rule of
  ADR 0016 stays, so ADR 0016 and `prompts/06-review.md` stay true. F-2: Codex
  is told what it can do (run tests and `make verify`) and what it may not
  (commit, change the repository through git), as a draft is; the Sonnet
  attempt's sentence stays true for Sonnet. F-3: an empty answer is a call
  failure, as on the Claude Code path today, so a silent Codex never reaches
  Sonnet without `--stage2-off` (Q-4).
- `[DETAIL]` A moved-HEAD stop follows the existing Codex drafting precedent,
  because Codex has command tools and repair must not rewrite its history.
- `[DETAIL]` No plan template exists in this tree; the phase-3 prompt supplies
  the card, ledger and time-log form. The artefact validator is also absent;
  no class, criterion or decision is altered to compensate for a missing gate.
