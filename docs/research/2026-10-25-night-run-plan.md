---
title: "Night-run plan — 2026-10-25/26"
category: research
created: 2026-10-25
updated: 2026-10-25
last_reviewed: 2026-10-25
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-yuw
tags: [night-run, plan, stage-2, phase-6, merge]
---

# Night-run plan — 2026-10-25/26

**This is a proposed plan for tonight. It does not report a run.** The
maintainer asked for it on 2026-10-25 at about 19:30 UTC, after the
weekend's cloud session. It follows the
[previous plan](2026-10-21-night-run-plan.md). One orchestrating Claude Code
session works a queue set in advance. The plan grants no new model,
architecture or deployment permission. Task state stays in Beads.

## State at the start

Measured 2026-10-25 at 19:30 UTC against `main` `f8a6b33`:

- 22 pull requests were open. 18 of them are runner, gate or test fixes from
  the cloud session of 2026-10-25 (#228, #229, #234 to #244, #246 to #250).
  Each is a draft. Phase 6, the Codex review, is owed on each.
- The cloud session's handover (#245) was still being edited at 19:27 UTC.
  A fix agent of that session was working on the research swarm (#158). Its
  tracker writes exist only in its container: the push to `refs/dolt/data`
  was refused with HTTP 403.

## Maintainer's answers, 2026-10-25 (interview, conversation)

1. **Review depth tonight.** The small fixes get phase 6 only, with no
   review loop: #234 to #244 and #246 to #248. Each `findings.md` records
   the skipped loop as a deviation, with this answer as the reason. #249 and
   #250 get the full loop and then phase 6. The rule holds for this night
   only.
2. **Expiring terms record (DL-B-13, due 2026-10-31).** Add a
   machine-readable `gilt_bis: YYYY-MM-DD` to `modelle_terms`.
   `terms_problem` skips a model whose date has passed and names it. Also
   re-read the DeepSeek retention terms now and record the result. This is
   one decision pull request.
3. **Call address of OpenCode Go (DL-B-8).** Warn only. When a catalog
   entry's `baseUrl` or `api` differs from the declared address, the runner
   names it, and the call still runs. Overlay definitions are not dropped.
4. **Origin cell for the repair brake (DL-B-9).** The orchestrator sets
   Origin (`base` or `fix-r<N>`) when it decides a row. The runner refuses a
   taken row whose Origin is neither. No prompt changes.
5. **Lost loop record (DL-A open point 1).** Add a recovery verb, for
   example `stage2.py recover-loop <change> --reason`. It starts a new
   record and writes the loss and its reason into `findings.md`. This is a
   decision pull request with an interview: an amendment to ADR 0021,
   decision 9.
6. **Explore model under `--stage2-off` (coding-harness-e7m).** Keep
   Haiku 5.5. After #241, read the next two or three explore runs. Switch
   to Sonnet 5.5 only if they still fail.
7. **README rework (#219).** Haiku 5.5 may merge it tonight, once it is
   brought up to date with `main` and CI is green.

**Already settled, not asked again:**
- Research-swarm seats (coding-harness-4295) were settled by Q-18 on #158's
  branch (`d4a0cf1`, 2026-10-22). The open-items list in #245 is stale on
  this point.
- One retry of a malformed paid answer (coding-harness-70rw) was answered
  on 2026-10-24.
- The mixed 429 case of #247 was answered ("also solve the mixed case").
  Its ADR 0021 amendment and interview are still owed.

## Merge rules tonight

These are the rules of 2026-10-21, extended by answer 7 above. Haiku 5.5
merges with `--match-head-commit` only when all of the following hold:
- CI is green;
- after phase 6, no BLOCKER or MAJOR is open;
- the pull request is not a decision pull request.

**The maintainer merges these:**
- #158: the research swarm, a decision pull request.
- #250: it changes `model-endpoints.yaml`; the maintainer reads it first.
- every decision pull request from answers 2 and 5.

## Queue

0. **Precondition: the cloud session has ended.** Until it has, nothing
   writes the tracker (house rule 4).
1. From the Mac, replay the tracker writes listed in #245 and #246, then run
   `tools/bd dolt push`.
2. Check that Codex starts: one `stage2.py review` in a worktree.
3. #237 (relative `PYTHON` exported as absolute): phase 6, then merge.
   After this, a local `make verify` is green.
4. One at a time, each with phase 6 and then a merge: #234, #239, #240,
   #241, #242, #243, #244, #246, #247, #248. Before each, merge `main` in.
5. The stack #235, then #236, then #238. Retarget each to `main` after its
   base merges.
6. #228: re-check of the F6-4 repair. Then #229: phase 6.
7. #249 and #250: merge `main` in and resolve conflicts (agent), then the
   review loop and phase 6.
8. Handover pull request in the morning.

## Stop rules

- A security BLOCKER stops the run.
- When a phase-6 re-check finds another edge case of the same mechanism,
  stop and ask instead of patching case by case.
- When Codex does not start, stop. Merge nothing that lacks phase 6.
