---
title: "Session handover — night run of 2026-10-21/22 (Claude), as of 2026-10-22"
category: handover
created: 2026-10-22
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-22"
tags: [handover, night-run, research-swarm, review-loop, stage-2]
target_ref: f26bc28
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
updated: 2026-10-22
---

# Resume here

## Where we are

The night run of 2026-10-21/22 worked the queue of the reordered night plan
(`docs/research/2026-10-21-night-run-plan.md`, addendum of PR #212) and ended
early at about 01:00Z on 2026-10-22, by the maintainer's choice, because Codex
stopped starting (two `stage2.py review` calls failed at start with exit 1 and
only "Reading additional input from stdin..."; the cause was not read). Five
pull requests are open and none was merged tonight: PR #158 (research swarm)
stopped after phase-6 round 18 by the maintainer's instruction with one MAJOR
row open; PRs #213 and #214 carry the maintainer's decision to restart a
completed review loop; PR #215 (bead coding-harness-8hr) and PR #216 (bead
coding-harness-9wp) are fixes that each stopped at an open phase-6 point.

## Next step

Check whether Codex starts again (a `python3 scripts/stage2.py review
runner-time-line` in `.claude/worktrees/runner-time-line`); if it does, run the
missing final phase-6 re-check of PR #216, because that pull request unblocks
every later runner change.

## Needed from the maintainer

1. **Merge PR #213, then PR #214** (restart of a completed review loop). PR
   #213 is the decision PR (ADR 0021 restart amendment, Q-17 of
   `loop-until-clean`); PR #214 targets #213's branch and lands in `main` only
   after #213. Recommendation: merge both; then an agent restarts PR #158's
   loop on your request and reports the availability check first.
2. **PR #158 (research swarm), F-65:** rounds 15, 16, 17 and 18 each found a
   new way for an empty or ambiguous YAML answer to close a research
   obligation in `value()` of `scripts/check_research_handoff.py` (comment or
   null, `[]`/`{}`, duplicate keys, a merge key plus duplicates). The
   historical-prose fallback swallows every YAML error. Question: should any
   YAML error in an `answer:` field report "not measured" (exit 3), so the
   fallback only reads text that is not YAML at all? Recommendation: yes;
   consequence: older `decisions.md` answers written as unquoted prose with a
   colon would need quoting — not yet measured which ones.
3. **PR #215 (bead coding-harness-8hr), F-4 and F-5:** three phase-6 passes
   in a row found a new MAJOR where credential scrubbing and denylist
   redaction meet. Question: collect every rule's spans (secret, non-secret,
   known credential) on the original text first and replace once, inside
   this change? Recommendation: yes, in this change, because every open row
   is that order-of-operations defect.
4. **PR #216 (bead coding-harness-9wp)** changes `prompts/04-implement.md`
   (provenance `human-written`): it removes the request that the model write a
   time line. It needs your reading and your merge after the final re-check.

## Decisions and preferences

- 2026-10-21, maintainer: Haiku 5.5 may merge tonight's pull requests with
  `--match-head-commit`, only with green CI, no open BLOCKER after phase 6,
  and never a decision PR. No pull request met all conditions tonight.
- 2026-10-21, maintainer: work PR #158 only through phase-6 round 18, then
  record and move to the beads.
- 2026-10-21, maintainer: restart PR #158's review loop explicitly (answer
  "ja, ausdrücklicher neustart der schleife"; Q-17; bead coding-harness-0xjr).
- 2026-10-22, maintainer: end the night after Codex failed (option A).
- Night-run stop rule applied by the orchestrator: when a phase-6 re-check
  finds a further edge case of the same mechanism, stop and ask instead of a
  further case-by-case repair.
- `make verify` runs with an absolute interpreter path here:
  `PYTHON=$PWD/.venv/bin/python3 make verify`. A relative `PYTHON` breaks the
  kit probe (the foreign repository resolves it in its own directory), and this
  shell's first `python3` is `/usr/bin/python3` 3.9 without PyYAML.

## Open work and blockers

Task status is in Beads; this lists what blocks what.

- Research swarm (PR #158, bead coding-harness-4295 closes with it): F-65 open;
  waits for decision 2 and for the loop restart (PRs #213, #214).
- Restart of a completed review loop (bead coding-harness-0xjr): PRs #213 and
  #214, CI green; waits for the maintainer's merge.
- Diagnostics carry test secrets into findings.md (bead coding-harness-8hr):
  draft PR #215; F-4, F-5 open; waits for decision 3. Review loop complete (4
  rounds, 17 rows released and marked by phase 6).
- Runner writes the measured time line itself (bead coding-harness-9wp, part
  1): PR #216; F-1 to F-4 fixed; the final phase-6 re-check failed at Codex
  start. Part 2 (load-sensitive tests, related bead coding-harness-jik) lives
  on PR #158's branch and was not touched.
- Fast pre-check before make verify (bead coding-harness-csm): spec and plan
  drafted in `.claude/worktrees/runner-precheck` (148 commits behind main on
  2026-10-22). Not started tonight: an implementation through the runner would
  fail the old time-line check until PR #216 is merged.
- New finding: since PR #158's record-key change the runner names a loop
  record `<change>@<root digest>`; a record written under the old key
  (`<change>`) is silently not found and `review-loop` would start a fresh
  run. For bead coding-harness-8hr the record was copied by hand to the new key
  on 2026-10-22 (a `MOVED.txt` stays in the old directory). Not yet a bead.
- New finding: `mimo-v2.6-flash` was reported on 2026-10-22 as "not admitted;
  data terms have not been read", although it was a Flash-swarm member on
  2026-10-20. Not investigated.
- New finding: a review loop whose single free-swarm row is rejected ends clean
  before any paid round (ADR 0021, decision 1). PR #216's loop ended that way
  after one false row; phase 6 then found four MAJOR rows.

## Working state and parallel-session boundary

As of 2026-10-22 about 01:05Z; no other session was reported in this
repository during the night. This handover's own branch is
`docs/handover-2026-10-22-night-run` from `origin/main` `f26bc28`.

| Pull request | Branch | Head | State |
|---|---|---|---|
| #158 | `explore/research-swarm` | `6df087e` | draft, decision PR, CI green |
| #213 | `decide/review-loop-restart` | `072af73` | decision PR, CI green |
| #214 | `feat/review-loop-restart` (base #213) | `af42d2c` | CI green |
| #215 | `explore/failed-check-secrets` | `564104a` | draft |
| #216 | `fix/runner-time-line` | `6968a6d` | open, CI not read |

Worktrees under `.claude/worktrees/`: `research-swarm`, `review-loop-restart`,
`review-loop-restart-verb`, `failed-check-secrets`, `runner-time-line`,
`runner-precheck`, and this handover's. Every branch above is pushed; no
uncommitted file was left in them (read with `git status --short` at each
commit).

Loop records (outside the repository, `~/.local/state/coding-harness/stage2/`):
`runner-time-line@d46ceb36` was released by its phase 6; the record of
`failed-check-secrets` was released by its phase 6; the old directory
`failed-check-secrets` keeps the original copy and `MOVED.txt`.

## Validation

- PR #158: full `make verify` 2026-10-21 21:58–22:09Z on the F-63 state: 3262
  passed, 16 skipped, every gate green after a date stamp across midnight. F-64
  verified by the runner's post-run `make verify` (`aed7f6f`); red first by hand
  (9 failing before the fix). Round 18 is review-only.
- PR #214: full `make verify` GREEN at `af42d2c`, 2026-10-21 22:17–22:22Z, 2378
  passed; red first: 4 new tests fail on `origin/main`.
- PR #215: full `make verify` GREEN at `41c6d29`, 2026-10-21 22:56–23:00Z, 2397
  passed; later repairs (`7f47cb4`, `315158a`, `8a57193`, `c733cd8`) verified by
  the runner's post-run `make verify`.
- PR #216: full `make verify` GREEN at `6859453`, 2026-10-21 23:17–23:22Z, 2383
  passed; red first: 9 runner-time tests fail on `origin/main`; repairs
  `5f7ff03`, `4e6d022` verified by the runner.
- Not run: the final phase-6 re-check of PR #216 (Codex did not start); any
  check of PR #216's CI; the WORKFLOW.md reconciliation (bead
  coding-harness-i0l).
