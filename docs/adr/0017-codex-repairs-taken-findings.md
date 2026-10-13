---
title: "ADR 0017 — Codex repairs the taken findings"
category: adr
status: accepted
created: 2026-10-13
last_reviewed: 2026-10-13
updated: 2026-10-13
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: codex, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, stage-2, repair, codex, review-loop]
---

# ADR 0017 — Codex repairs the taken findings

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, the pull request's state is the decision's state: open
  is proposed, closed is rejected. Supersedes ADR 0015; its amendments of
  ADR 0011's decisions 2 and 3 are restated below. Amends no D- or O-number.
* Review: the maintainer chose the direction on 2026-10-13 in the answers
  recorded as Q-1 to Q-5 in `plans/changes/codex-repairs/decisions.md`: fresh
  Codex re-check (Q-1), both kinds of findings (Q-2), Codex twice then Sonnet
  after failed post-checks (Q-3), explicit Stage-1 switch for unavailable
  Codex (Q-4), and supersession of ADR 0015 (Q-5). The spec proposes "yes" to
  the ADR question; this draft records no answer. The acceptance is the
  merge commit and is written nowhere else, so the header's `review` stays
  pending (ADR 0008) · Decider: maintainer · prepared by Codex.
* Date: 2026-10-13 · takes effect on merge.

## Context

ADR 0015 routes taken findings of phases 4b and 6 to GLM 5.3. The maintainer
asked that Sol (`gpt-6.1-sol`) implement review fixes instead and reported
that GLM 5.3 had consumed most of the exhausted Z.ai budget (the request
recorded in `plans/changes/codex-repairs/research.md`, 2026-10-13).

The repair attempt loop currently starts only Claude Code. The drafting
route already starts Codex with writing access through the runner, and the
evidence and checkpoint checks do not depend on GLM (research, "Runner
exploration", read at `9ddb38a`, 2026-10-13; ADR 0016).

Codex is also the phase-6 reviewer. ADR 0015's same-model prohibition must
therefore change explicitly, rather than remain as a promise the new route
cannot keep. The maintainer accepts the same model judging a repair in a
fresh session (Q-1). Review calls remain read-only.

## Decision Drivers

* No Z.ai budget is spent on repairs.
* Every taken finding still carries the existing evidence and checkpoint guards.
* A re-check receives no repair-session history.
* An unavailable Codex call does not silently switch the repair budget.
* The earlier routing decision remains readable as superseded history.

## Considered Options

* **Codex repairs both kinds, with a fresh Codex re-check** — chosen (Q-1, Q-2).
* **Keep GLM 5.3 repairs** — preserves model separation but spends the budget
  the maintainer wants to reserve.
* **Codex repairs only one kind of finding** — retains two repair routes and
  some GLM repair spend; rejected in Q-2.
* **Another phase-6 model or an extra loop round** — adds independent model
  review or another pass, but moves its budget or changes the round count;
  rejected in Q-1.
* **GLM as last attempt, or no last attempt** — respectively spends Z.ai
  budget or abandons a repair after two post-check failures; Q-3 chose Sonnet.
* **Automatic fallback on Codex call failure** — avoids an explicit restart
  but hides an availability-driven budget switch; rejected in Q-4.

## Decision

Chosen option: "Codex repairs both kinds, with a fresh Codex re-check",
because it implements the maintainer's model choice without weakening the
repair evidence contract.

1. **Codex repairs all taken findings in one batch** through `python3
   scripts/stage2.py repair <change>`: loop-record rows, released loop rows
   and phase-6 findings. Each Codex attempt starts `gpt-6.1-sol` at effort
   `max` in a fresh session, with the existing `workspace-write` configuration,
   hooks and memories off, and no added directory, automatic approval or
   bypass. Repair reads no GLM key and never routes to `glm-coding-plan`.
2. **Only post-run failures advance the chain:** Codex; a fresh Codex attempt
   with the first attempt's diagnostics; Sonnet 5.5 at effort `medium` on
   Stage 1 with both diagnostics. A model call failure stops; with unchanged
   HEAD, the existing restoration returns the worktree to baseline. When
   Codex is unavailable, the orchestrator deliberately starts
   `--stage2-off <reason>`, which uses Sonnet alone and records why. A
   declaration refusal or leak-check BLOCK stops without fallback.
3. **The orchestrator decides, the verb repairs, the reviewer re-checks.**
   The orchestrator writes `taken — <reason>` or `rejected — <reason>`, or
   takes a finding no test can show as `taken — not a test — <reason>`.
   Repair keeps those inputs, requests one fixed line per row and a measured
   time entry, and starts no review. The runner checks each exact prompt,
   prepares and formats the result, runs `make verify`, checks the time and
   evidence, writes statuses and makes one clean descendant checkpoint.
   A Codex call that moves HEAD stops before restoration or a runner commit.
4. **The existing proof and statuses stand.** A code finding requires a
   defined test the runner demonstrates red against baseline code; a finding
   taken as `not a test` is proven by the separate re-check. Fixed rows read
   `fixed — tests/<path>::<function>` or `fixed — not a test — <reason>`.
   Failed attempts retain their audit, quoted diagnostics and changed-file
   evidence, while their model-written statuses are restored. Private loop
   rows are marked only after the checkpoint; unreleased rows reach the
   repair in the prompt rather than a worktree file.
5. **The same model may repair phase-6 findings; a fresh session re-checks.**
   A phase-6 verdict after an earlier `## Phase 6` block in `findings.md` — a
   re-check — runs Codex read-only without resuming the repair, a prior
   verdict or a historical phase-2a session; the first phase-6 review keeps
   the resume rule of ADR 0016. Loop marks may
   resume only that new verdict thread after its verdict. This replaces ADR
   0015's blanket reviewer/repairer separation; it does not give review calls
   write tools or move any review to another model.
6. **The loop budget and run count stand.** A fixed row counts as taken;
   round 3 requires a taken or fixed row in round 2, and the maximum stays
   three rounds. The orchestrator writes `Broke a test` from the repair
   evidence before the next round or release. Audit lines and historical GLM
   counts retain their format. Initial implementation, Explore and draft's
   GLM fallback retain their models.

## Consequences

* Repair spend moves from Z.ai to the Codex subscription. A last attempt or
  deliberate Stage-1 run still spends Claude budget; no cost is measured here.
* Codex receives unreleased loop rows in repair prompts. Its repair thread
  is discarded; a fresh verdict does not receive that history. The same
  model's judgment may still be correlated, a limit Q-1 accepts.
* Codex can run commands inside its configured sandbox. The prompt instructs
  that it may run tests and `make verify` but must not commit or run a git
  command that changes the repository; the runner checks HEAD, but does not
  measure sandbox enforcement or broaden read confinement. ADR 0016's
  residual risks for ignored files, external paths and the git directory
  remain; the tests measure the invocation and runner behavior with stand-ins.
* A dead Codex call needs an explicit retry or Stage-1 restart. It does not
  consume the post-check fallback without the orchestrator's choice.
* ADR 0015 gains a supersession marker in this change's implementation, with
  its original decision body retained. No D- or O-number changes, so neither
  the continuity map nor the original ADR 0011 file changes.

## Validation

* The criterion ledger in `plans/changes/codex-repairs/plan.md` names the
  route, failed-call, declaration/leak, evidence, checkpoint and fresh-session
  tests, including an old Codex phase-2a thread that must not be resumed.
* `.venv/bin/python -m pytest tests/test_stage2.py tests/test_stage2_runs.py
  tests/test_model_endpoints.py -q` and `make verify` pass after the
  maintainer's stated ADR answer is recorded by the orchestrating session.
* Phase 6 checks this record against Q-1 to Q-5 and the PR file list confirms
  that ADR 0015 is marked, its decision body preserved and protected areas
  untouched. Passing stand-in tests are not evidence of a live Codex repair.
