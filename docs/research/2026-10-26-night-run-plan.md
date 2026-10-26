---
title: "Night-run plan — 2026-10-26/27"
category: research
created: 2026-10-26
updated: 2026-10-26
last_reviewed: 2026-10-26
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-26"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-yuw
tags: [night-run, plan, stage-2, phase-6, merge]
---

# Night-run plan — 2026-10-26/27

**This is the plan for tonight. It does not report a run.** The maintainer
asked for it on 2026-10-26 at about 17:15 UTC, during the day session. It
follows the [previous plan](2026-10-25-night-run-plan.md). One orchestrating
Claude Code session works the queue below, one step at a time (night runs
stay sequential, coding-harness-cj6b). The plan grants no new model,
architecture or deployment permission. Task state stays in Beads.

## State at the start

Measured 2026-10-26 at about 17:20 UTC against `main` `a5345532`. Nine pull
requests are open. These are the ones the queue touches:

- **#158, the research swarm (ADR 0020), a decision pull request.** The
  findings F-66 to F-71 (Unicode line separators splitting foreign text, and
  an unchecked malformed claim in the handoff gate) are repaired. A fresh
  Sonnet 5.5 re-check is running. **The maintainer merges it.**
- **#248, mutation evidence must reach the gate's script.** The maintainer
  answered R7 (2026-10-26: replace the deny-list with an allow-list). A
  Sonnet 5.5 repair is running.
- **#250, review-loop runner defects, part B.** The loop is finished (round 2
  was clean). Phase 6 (Sonnet 5.5) found two MINOR rows (F6-1, F6-2). Their
  repair is running. **The maintainer merges it**, because it changes how
  the runner reads `model-endpoints.yaml` (2026-10-25 plan).
- **Branch `decide/terms-expiry` (coding-harness-abra, due 2026-10-31).**
  The spec, design, plan and ADR 0022 draft are committed. The `gilt_bis`
  dates are in `model-endpoints.yaml`, written by hand. The ADR answer is
  recorded as yes. GLM 5.3 Flash is implementing.
- #235 → #236 → #238 (a stack of finding-table fixes), #228 (F6-4 re-check)
  and #229 (loop state block): unchanged since the 2026-10-25 night.
- #245 (the cloud session's handover): the maintainer's to merge.

## Maintainer's answers, 2026-10-26 (interview, conversation)

The maintainer made answers 1 and 2 standing rules for every night run
(coding-harness-yuw.4: they go into `AGENTS.md` and `docs/WORKFLOW.md`).

1. **Codex at capacity.** Wait 4 minutes and retry once. If the retry also
   fails, Sonnet 5.5 takes that one step:
   - a repair through `stage2.py repair <change> --stage2-off "<reason>"`;
   - a phase-6 review or re-check through a read-only Sonnet 5.5 sub-agent,
     whose rows are recorded unchanged.

   Each such step carries its reason, and the run continues. This replaces
   the 2026-10-25 stop rule "when Codex does not start, stop".
2. **Another edge case of the same mechanism at a phase-6 re-check.**
   Record the finding, park that pull request, and continue with the next
   queue item. The maintainer decides in the morning.
3. **After the queue.** First coding-harness-m98e (detect Codex at capacity
   and fall back; its interview is done). Then coding-harness-680l with
   coding-harness-fmir (the class in a bead becomes machine-readable; a bead
   names its change folder). Each runs the full workflow for its class.
   m98e ends in a decision pull request, because it amends ADR 0017.

**Already settled, not asked again:**
- Day sessions may run two foreign calls at once (maintainer, 2026-10-26).
  At night it stays one at a time.
- The Sonnet window of 2026-10-26 (17:26 to 19:26 CET) ends before the run
  starts. After it, Codex is the default again.

## Merge rules tonight

The orchestrator merges with `--match-head-commit` only when all of the
following hold:
- CI is green;
- after phase 6, no BLOCKER or MAJOR is open;
- the pull request is not a decision pull request.

**The maintainer merges these:** #158, #250, #245, the `terms-expiry`
decision pull request, and m98e's decision pull request.

## Queue

1. Finish what the day session left running: the #248 repair, the #250
   repair and the #158 re-check. Then a fresh phase-6 re-check on #248 and
   on #250.
2. #248: merge once it is clean.
3. #158 and #250: when clean, mark them ready with the decision block in the
   body, for the maintainer.
4. `terms-expiry`:
   1. When the implementation is green, run the review loop (phase 4b) and
      then phase 6.
   2. Open the decision pull request `decide(model-terms): …`. The
      maintainer merges it before 2026-10-31.
5. The stack #235, then #236, then #238. Merge `main` in, then phase 6, then
   merge. Retarget each to `main` after its base merges.
6. #228 (re-check of F6-4), then #229 (phase 6).
7. coding-harness-m98e, then coding-harness-680l with coding-harness-fmir
   (answer 3).
8. Handover pull request in the morning.

## Stop rules

- A security BLOCKER stops the run.
- A leak-check BLOCK stops without fallback.
- When neither Codex nor Sonnet starts, stop. Merge nothing that lacks
  phase 6.
- An edge case of the same mechanism parks only its own pull request
  (answer 2).
