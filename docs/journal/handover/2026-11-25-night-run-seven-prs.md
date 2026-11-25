---
title: "Session handover — night run 2026-11-24-a: seven pull requests, verify speed-ups, tracker clean-up"
category: handover
created: 2026-11-25
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "Opus 5.5, 2026-11-25"
tags: [handover, night-run, lanes, tracker, verify-speed]
target_ref: 18a13d3d
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
updated: 2026-11-25
---

# Resume here

## Where we are

Session 52db2bf0 (profile `~/.claude-mp`) took over the lanes of the bddh
session (handover PR #448) on the evening of 2026-11-24 and ran night run
`2026-11-24-a` until 10:00 Europe/Berlin on 2026-11-25. Run state:
`~/.local/state/coding-harness/night/2026-11-24-a/` (`lanes.txt`,
`lane-watch.log`, `handles.txt`, `epic-mapping/`).

Seven pull requests were opened (six lanes plus one ADR pointer); every question
asked during the night was answered by the maintainer in the morning, and the
lanes they unblocked are running. Nothing was merged.

## Next step

1. Merge the ready pull requests (table below); each last commit carries its
   `Closes-Bead` trailer, so `make close-merged` closes the beads.
2. Answer the two open questions below (isolated-writing-attempts start,
   pi-work-route explore).
3. Review the epic mapping and the P1 triage (tracker section below).

## Needed from the maintainer

**Merge (all phase-6 clean, `make verify` green on the PR head or before the reviewer):**

| PR | Lane | Bead | What |
|---|---|---|---|
| #449 | adr-0021-pointer | coding-harness-firy (closed) | one pointer line from ADR 0021 decision 6 to ADR 0025 |
| #450 | review-diff-4000 | coding-harness-mwzv.4 | review-loop rounds carry 4,000 diff lines |
| #451 | repair-scope-guard | coding-harness-t83 | a repair cannot keep out-of-scope files; journal held; fail closed on a missing inventory |
| #452 | test-ci-shared-tree | coding-harness-bxxt.12 | the orphan-script control test no longer writes into the shared scripts/ |
| #453 | frontmatter-batch-log | coding-harness-bxxt.21 | frontmatter-current gate 6.23 s -> 0.28 s, output identical |
| #454 | availability-scrub-import | coding-harness-vg9.2 | read_intelligence uses the runner it is given |
| #455 | slow-test-fixes | coding-harness-bxxt.16 | three tests 29.2 s -> 11.7 s, every check kept |

Also still open from the evening: #446 (house rule 11), #444 and #448 (handovers).

**Open questions (one each):**

1. **isolated-writing-attempts (coding-harness-s9r): when does the implementation start?** All 69 spec-review rows of three rounds are decided (Q-26..Q-47); the final draft is a26b064a with a 24-hour phase-4 appetite. It touches scripts/stage2.py heavily, like the open stage2 lanes; recommendation: start after the stage2 pull requests are merged, on a clean main.
2. **pi-work-route (coding-harness-363r.3): explore run 2 was incomplete too** (337a5a40): deepseek-v4.1-flash timed out on repository topics 1, 2 and 4 under the 10-minute topic limit; every other slot is valid. Options: raise `topics` in research-swarm-limits.yaml (the agy session's trust-pyramid-swarm lane also edits that file), swap deepseek out of the repository trio, or go on with the partial research. A rerun recomputes all repository topics (coding-harness-f6qj).

**Answered during the night (2026-11-25 morning), now in progress:**

- cheap-checks-admission (bxxt.13): option A (worker cap, lock rule 24ag unchanged; Q-1); spec reviewed in three rounds (D-1..D-6); final draft being written.
- detached-job-launcher (a6ns.1): F-1 repaired (stop finds a reparented descendant by its job token); F-1..F-4 finished by hand (9889619f); phase-6 re-check running.
- red-first-baseline (7aso): P6-4 as one choke point for every pytest end without a record; repair running.
- findings-per-model (qut1): F6-1 as one shared parse for report and gate; repair running.
- isolated-writing-attempts (s9r): round-3 rows as recommended (Q-44..Q-47); final draft done.

## Decisions and preferences (maintainer, 2026-11-24/25)

- Structural repairs: qut1 model-name and branch resolution (round 1), qut1
  full-match status reader and legacy target lists, t83 fail closed on any
  inventory failure; t83 P6-1 (implicit global excludes file) as a named
  Boundary.
- advance-verb: the separate ADR 0026 draft was removed and ADR 0021 amended
  on the branch (Q-26).
- isolated-writing-attempts: all 42 rows of round 1 and 17 of round 2 decided
  as recommended (Q-26..Q-43); Q-41 amends Q-27 (a check the attempt's own tree
  broke falls through).
- Implementation runs on Sonnet (`--stage2-off`) while GLM through Z.ai is out
  (weekly limit 100 % until 2026-11-29 02:48; coding-harness-b5pu).
- Tracker: closed 8b0u, tscc (close-merged), 0n4s, kw40, bt8, 7kzl (branch
  deleted), firy, s55e, yb1l, tlr4; new beads nu3z (measured, see below),
  7tcp (two-week swarm-test count, due ~2026-11-30), m77s, 6ser, d1p7,
  bxxt.12-23, vg9.1, vg9.2, u9wh.
- 363r.3 (implement through DeepSeek via Pi) pulled forward to tonight.

## Open work and blockers

| Lane | Bead | Branch | State at 09:25 CET |
|---|---|---|---|
| standin-call-counter | coding-harness-bxxt.14 | fix/standin-call-counter | implemented a2846c56; loop 2 rounds, all rows fixed; phase 6 running |
| detached-job-launcher | coding-harness-a6ns.1 | feat/detached-job-launcher | F-1..F-4 fixed; phase-6 re-check running; tmux smoke test still owed |
| findings-per-model | coding-harness-qut1 | feat/findings-per-model | F6-1 repair running |
| red-first-baseline | coding-harness-7aso | fix/red-first-baseline | P6-4 repair running |
| cheap-checks-admission | coding-harness-bxxt.13 | fix/cheap-checks-admission | final draft being written; then plan card |
| isolated-writing-attempts | coding-harness-s9r | feat/isolated-attempts | final draft a26b064a; waits for the start decision |
| pi-work-route | coding-harness-363r.3 | feat/pi-work-route | explore run 2 incomplete; waits for the maintainer |
| ladder-next-step | coding-harness-hwll | feat/ladder-next-step | after red-first-baseline and review-diff-4000 merge |
| advance-verb | coding-harness-z40g | feat/advance-verb | after hwll |

## Tracker work prepared for the maintainer

- **Epic mapping (read-only proposal):**
  `~/.local/state/coding-harness/night/2026-11-24-a/epic-mapping/epic-mapping.json`
  and `epic-mapping-summary.md`: 344 active beads, 188 proposed moves into 8
  domain epics, 3 low-confidence items (3kv1, 0887, uzjq), possible duplicates
  (g4iq/h9ge, kgwu/5ane.19/qwpx.1, bxxt.4/kpaq), data errors (5q2p two
  parents, 1jg.4 id). Nothing was written; a script applies it after review.
- **P1 triage:** 19 non-epic P1s against the limit of 10; an external proposal
  lists ten to keep; 363r.3 stays P1 (pulled forward).

## Working state

- GLM through Claude Code: Claude Code 2.1.331 prints
  `[claude-code:unrecognized_model]` even against an unreachable endpoint
  (measured offline); the cause tonight was the Z.ai weekly limit.
- Runner Claude calls run on the default profile (CLAUDE_CONFIG_DIR is not
  passed; bead coding-harness-m77s); its 5-hour limit was hit twice tonight
  (spec-review fell back to deepseek once).
- coding-harness-nu3z measured: `make index` runs bare `python3` (Python 3.9.6);
  venv_guard cannot re-enter .venv on Python < 3.10 (no `sys.orig_argv`) and
  blames the environment.
- External analyses of verify speed and of a stage2.py split were checked by
  read-only subagents; confirmed gaps became bxxt.12-23, vg9.1, vg9.2; the
  corrections are in the notes of coding-harness-vg9.

## Orchestrator mistakes

- Two test-only rows were triaged as criterion rows instead of guard-test rows;
  the runner's red-first proof rejected every repair attempt, and the code was
  finished by hand (review-diff-4000 R-1, test-ci-shared-tree R-1). Recorded
  as memory `test-file-rows-are-guard-rows`.
- One accidental `git stash push` of a lane's test change; restored by SHA at
  once and the entry dropped; nothing lost.
- One repair started with `&` inside a command (against the background-mode
  rule); stopped before its model call, records committed unchanged
  (dc9f69be); the first `kill` failed on zsh word splitting (memory
  zsh-kill-word-splitting).
- detached-job-launcher F-4 was again a test-only row triaged as a criterion
  row; finished by hand. New beads coding-harness-ugkk (repair refuses such
  rows up front) and coding-harness-5vts (new_change.py writes the bead text as
  the research topic) turn two of tonight's lessons into code.
- A zsh `$base:tests` path lost its revision to the `:t` modifier and one
  timing run measured nothing; repeated with `${base}`.

## Validation

- Every PR above: phase 6 clean, full `make verify` green on the reviewed head
  (repair-scope-guard also on the merged head after merging origin/main).
- Measurements: frontmatter gate 6.23 s -> 0.28 s (median of 5, same commit,
  output identical); three tests 29.2 s -> 11.7 s (same command, load 1.8-2.1).
- Not read: PR #447.
