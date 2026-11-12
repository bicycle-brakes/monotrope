---
title: "ADR 0025 — A runner repair passes a targeted check; one full make verify precedes phase 6"
category: adr
status: accepted
created: 2026-11-08
last_reviewed: 2026-11-08
updated: 2026-11-12
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, stage-2, repair, review-loop, verification]
---

# ADR 0025 — A runner repair passes a targeted check; one full make verify precedes phase 6

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, open is proposed and closed is rejected. Amends ADR 0021
  decision 6; supersedes no ADR. Amends no D- or O-number.
* Review: the maintainer decided on 2026-11-08, in the conversation, that
  ADR 0021 decision 6 changes together with the runner change that makes a
  repair pass on a targeted check (pull request #343, bead
  coding-harness-gxwg), and that the amendment travels in a decision pull
  request of its own (answer "Fertig machen + ADR-PR"), and answered its
  interview the same day (`plans/changes/adr-repair-check/decisions.md`,
  Q-1 to Q-5). Decider: maintainer ·
  prepared by Claude Code. Acceptance is the merge commit; the review header
  remains pending.
* Date: 2026-11-08 · takes effect on merge.

## Context

ADR 0021 decision 6 ends "requiring `make verify` green after repair as
today". Every runner repair therefore paid for a full `make verify`, even for
a narrow edit. Full checks run one at a time under the machine-wide verify
admission (`docs/WORKFLOW.md`, "One admission per user and machine"), so a
repair cycle waits for the lock and then for the whole suite. The workflow
records a full run at 12 to 13 minutes (measured 2026-10-30); the lane times
this decision should shorten are not measured.

The maintainer had already let a targeted check stand in for a full one after
a hand repair by the orchestrator (2026-10-30, bead coding-harness-24ag). The
change `repair-targeted-check` extends that rule to runner repairs and adds an
enforced full check before phase 6 (`plans/changes/repair-targeted-check/`,
on the branch of #343). Without this amendment the ADR would contradict the
gate the runner enforces (review-loop row L8-3 of that change; bead
coding-harness-firy).

## Decision

ADR 0021 decision 6's last sentence is replaced by:

1. After a runner repair the runner runs a targeted check: the tests linked
   to the touched files, the prior retry selections, ruff on the touched
   Python files, and the gates the touched file kinds feed.
2. When that selection is not safe, the full `make verify` runs instead, as
   the fallback for that repair.
3. One fresh green full `make verify` on the head under review is required
   before phase 6. A red, unstartable or timed-out run stops the review;
   runner audit lines in `findings.md` do not count as a new head.
4. The orchestrator measures repair duration, verify-lock wait and every
   failure the full check before phase 6 finds that a targeted check missed,
   over five changes or two weeks, whichever comes first, and reports the
   result to the maintainer.
5. This rule holds from the merge. The testing-strategy spike (bead
   coding-harness-1ga5) may amend or replace it with an ADR of its own; the
   measurement of point 4 enters that spike as a finding.

The rest of ADR 0021 decision 6 stands unchanged.

## Consequences

* A repair cycle no longer waits for a full run unless its selection is
  unsafe; the effect on cycle and lane times is not yet measured.
* A targeted check can miss a test the touch map does not link to a touched
  file. The full `make verify` before phase 6 catches such a miss before the
  review, and CI remains the full gate of the pull request.
* A repair can be marked fixed on a targeted result that the full check
  later turns red; that red stops phase 6 until it is repaired.

## Validation

* #343 carries the runner implementation and its criterion tests; this
  pull request carries only the ADR text.
* CI on this pull request is its gate; merge, not this draft, accepts the ADR.

## Implement and draft amendment — the targeted check covers more verbs, 2026-11-12

The maintainer answered the interview of the change
`targeted-check-more-verbs` on 2026-11-11 and 2026-11-12
(`plans/changes/targeted-check-more-verbs/decisions.md`, Q-1 to Q-6; bead
coding-harness-0swp). Implement attempts still paid for a full `make verify`
under the machine-wide verify admission, and a draft's document check
queued for the same admission. This amendment extends decisions 1 to 4; it
takes effect when the maintainer merges the decision pull request that
carries it, and until then the decisions above stand as written.

1. Implement takes the targeted check of decision 1 on every route, with
   the full fallback of decision 2. The selection follows import links from
   the touched code transitively, and takes every touched or reachable test
   file whole. A `scripts/stage2.py` edit, a selection of the whole
   `tests/test_stage2.py`, shared test configuration, an unsafe or unreadable
   input, and existing code without a reachable test still fall back to the
   full `make verify` (Q-3).
2. An implement attempt whose new production code (an added Python or shell
   file) no test reaches, as the current link inventory proves, is refused
   before any test runs and before a full fallback is admitted; its
   diagnostics name the file and ask for its test. An unreadable inventory
   proves nothing and keeps the fallback (Q-4).
3. A targeted red fails the attempt; the full check never runs to override
   it. The existing guards of each route (cheap checks, answer proofs,
   protected-path and checkpoint guards) remain mandatory.
4. A draft's post-run check runs only the locally runnable document gates of
   the gate registry, without pytest or code gates and outside the
   machine-wide verify admission; its existing artefact checks and its one
   tolerated missing ADR answer stay as they were (Q-2).
5. Decision 3 stands unchanged: a fresh green full `make verify` of the head
   under review precedes phase 6, and CI keeps running the complete suite.
6. Decision 4's measurement of misses becomes automatic. A slip is a
   completed red full check before phase 6 on the same repository content
   and gate configuration as an accepted targeted green. The runner appends
   one slip per full run to the local duration history; `python -m
   scripts.verify_duration slips --repository <path> --since <UTC> --until
   <UTC>` counts the distinct slipped full runs of one repository in a
   half-open UTC interval and reports missing or incomplete evidence as
   unavailable, never as zero. Admission refusals, launch failures,
   timeouts, unreadable identities and CI-only failures are not counted.
   A night run's morning handover reports that count with its repository
   and interval (Q-5).

Cost consequence: an implement attempt with safe coverage no longer waits
for the verify admission or the whole suite, and a draft no longer waits for
the admission at all; a targeted miss surfaces at the full check before
phase 6 and is then counted. The amendment adds no new ADR and supersedes
none.
