---
title: "Handover — night run 2026-11-09 to 10, stopped early at the usage limit"
category: handover
created: 2026-11-10
updated: 2026-11-10
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "Opus 5.5, 2026-11-06"
tags: [handover, night-run, heartbeat, lanes, review-loop, stage-2]
target_ref: a8e23d17
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Handover — night run 2026-11-09 to 10, stopped early at the usage limit

Written at about 01:55 UTC on 2026-11-10 by the orchestrating session, when
its usage limit was reached. It is short on purpose; the measured record is
`~/.local/state/coding-harness/night/2026-11-08-a/lane-watch.log`.

## Where we are

The session stopped orchestrating at about 01:55 UTC. Runner jobs that were
already started keep running as shell processes and end on their own; nobody
commits their results until a session resumes. Nothing was merged.

## Pull requests waiting for the maintainer

- #362 night-stall-guard (bead coding-harness-ibde): phase 6 without a
  finding, full check green at `847517bc`. It narrows the ask rules for
  merging calls; read the note in its body before merging.
- #359 origin-cell, #360 no-work-done, #361 research note: opened earlier;
  their CI state was not read again this night.

## Lanes at the stop (state not read after 01:55 UTC)

- explore-provenance (bead coding-harness-g19n): runner repair of finding
  EP6-8 started. Finding EP6-7 is open and needs the maintainer: the question
  with three options is in the bead notes. Two hand interventions so far
  (`1cbeed87`, `a04b37f3`); a third must be asked.
- triage-verb (bead coding-harness-o2s1): runner repair of the three MAJOR
  findings P6-1 to P6-3 started; then a phase-6 re-check, then the pull
  request.
- go-wire-apis (bead coding-harness-36za): phase 6 started a third time after
  the hand repair `f2cb4082` (test helper); it waits at the verify lock. Two
  hand repairs so far (`5c38017f`, `f2cb4082`).
- verify-slots (bead coding-harness-u1ha): all three draft attempts failed
  only because the orchestrator's `decisions.md` lacked the two decision
  statements. They are added but **not committed**; the tree also holds the
  third attempt's spec and plan (GLM 5.3), uncommitted. A document check
  (`bash scripts/verify_all.sh --job docs`) was queued. Next: if it is green,
  accept the draft by hand (first hand acceptance of this change), commit,
  stop at the plan card.
- review-fewer-rounds (bead coding-harness-3rtn): draft started, waits at the
  verify lock; the branch was 83 commits behind `origin/main`. Stop at the
  plan card.

## Parked for the maintainer

- swarm-report-format (bead coding-harness-4q9y): spec and plan pushed
  (`da0dc829`); the plan card waits; the interview was skipped by the
  orchestrator with reasons and needs confirming.
- central-config (bead coding-harness-twvx): two fallback explorations pushed
  on `feat/central-config`; five open points for the interview are in the
  bead notes.

## Lessons of this night

- A second full check beside the lock holder pushed both past the runner's
  30-minute limit; one green run alone takes 26 to 28 minutes, so the margin
  is thin (epic coding-harness-bxxt).
- One test fails across local midnight (bead coding-harness-bxxt.5).
- The disk fell to 3 GiB; 50 clean, merged worktrees were removed (the log
  line that says 51 is wrong).
- An explore on the fallback route or with GLM Flash cannot read the tracker:
  put the bead's intent into `research.md` before the first call.
- `explore --stage2-off` refuses a `--class` flag.
- Clock times in the chat between 00:52 and 01:22 UTC were estimated and up
  to 40 minutes late; the log carries measured times.

## Resume here

Read the task outputs and `git status` of the five lane worktrees, commit
what the runner finished, then answer the EP6-7 question on bead
coding-harness-g19n.

## Addendum — 2026-11-10, 02:55 UTC: the session resumed and ran on

The usage limit lifted shortly after the record above was written, and the
same session continued. Everything above this heading describes the stand at
01:55 UTC; where the two disagree, this addendum holds. Nothing was merged.

### Pull requests of this night

- #362 (named above; bead coding-harness-ibde): unchanged, full check green
  at `847517bc` (00:20 UTC), phase 6 without a finding.
- #364, new: measured wire APIs of the Go models (bead coding-harness-36za);
  full check green at `f2cb4082` (02:11 UTC), phase 6 without a finding.

Read before merging: #362 changes `.claude/settings.json`, and its body
states which spellings of a merging call still pass without a question. #364
removes nine "wire API not measured" skips in `model-endpoints.yaml`, which
admits those models to the paid review ladder and the research swarm. The
follow-up for the Google endpoint is bead coding-harness-twdu.

### Lanes at 02:55 UTC

- **triage-verb** (bead coding-harness-o2s1) — running. Phase 6 found three
  MAJOR rows (a reason text that grants guard authority, a root-level file
  dropped from the location, CRLF rewritten to LF). The runner repaired all
  three (`16ed2a62`, Codex, first attempt); the phase-6 re-check holds the
  verify lock. Next: commit the verdict unchanged; when clean, open the pull
  request with `Closes-Bead: coding-harness-o2s1`.
- **review-fewer-rounds** (bead coding-harness-3rtn) — running. The draft of
  spec, design, plan and an ADR draft waits behind the verify lock. Its branch
  was 83 commits behind `origin/main` and is not synced. Next: commit the
  runner's result, stop at the plan card.
- **explore-provenance** (bead coding-harness-g19n) — parked. The third
  re-check found two MAJOR rows: EP6-7 (a hand repair, `a04b37f3`, edits the
  research files of three other changes, outside the protected scope of the
  spec) and EP6-8 (a YAML alias corrupts the review line on publication). The
  runner refuses to repair EP6-8 while EP6-7 is undecided.
- **verify-slots** (bead coding-harness-u1ha) — parked at the plan card. All
  three draft attempts failed only on missing decision statements; these were
  added, restating the maintainer's two answers of 2026-11-09, and the third
  attempt was accepted by hand.
- **swarm-report-format** (bead coding-harness-4q9y) — parked at the plan
  card (`da0dc829`).
- **central-config** (bead coding-harness-twvx) — parked before the
  interview. Two fallback explorations are committed; the research header
  still lacks neighbours, class and provenance.

Fewer than five lanes ran from 02:40 UTC on: every other queued item needs
the maintainer. The four follow-up beads (coding-harness-3h96, -twbl, -3ha6,
-4bhp) repair code that is not on `main` yet and wait for four merges:
pull requests #359 and #360, triage-verb and explore-provenance.

### Needed from the maintainer

1. Merge decisions: #359, #360, #361, #362, #364 and this handover (#363).
2. explore-provenance, row EP6-7 (options in the notes of bead
   coding-harness-g19n). Recommended: a small pull request of its own
   corrects the three research headers, merges first, and the change drops
   its own edits.
3. Plan cards (veto or go): verify-slots, swarm-report-format,
   review-fewer-rounds once its draft is committed.
4. swarm-report-format: confirm the interview skip (notes of bead
   coding-harness-4q9y).
5. central-config: the interview; five open points stand in the notes of bead
   coding-harness-twvx.
6. Still open from earlier: target numbers for the epic coding-harness-bxxt,
   and the expired claims on beads coding-harness-dca4, -csm and -xay1.

### Hand interventions, counted per change

- night-stall-guard, 2: one hand acceptance (`065f7b12`) and one hand edit
  (`9e4e1d31`); both named in #362.
- go-wire-apis, 2: two hand repairs, the second `f2cb4082` (a test helper
  lacked a new required argument); named in #364.
- explore-provenance, 2: `1cbeed87` and `a04b37f3`; a third must be asked.
- verify-slots, 1: the acceptance of the third draft attempt.

### Lessons added after 01:55 UTC

- A draft may not edit `decisions.md`, and a decision record needs a
  statement beginning "In the context of" and ending with its date. A change
  opened without it fails every draft attempt on that alone; three attempts
  were spent on verify-slots before this was read.
- A change in a function signature surfaced only in the full check, 25
  minutes in: the targeted check after the repair did not select the three
  tests that call the function through a helper.
- A hand repair that touches files of other changes becomes a review finding
  of its own (EP6-7). The next one is asked first.
- Prose times between 00:52 and 01:22 UTC were estimated and up to 40 minutes
  late; they are corrected in the log and in the notes of beads
  coding-harness-twvx and -4q9y. Every time now comes from `date -u`.

### Resume here (replaces the section above)

Read the last lines of
`~/.local/state/coding-harness/night/2026-11-08-a/lane-watch.log` and
`queue.txt` beside it, then answer the list under "Needed from the
maintainer" from the top. A further addendum records how triage-verb and
review-fewer-rounds ended.

## Addendum — 2026-11-10, 06:40 UTC: the last two lanes ended, the run is over

No runner job runs any more. Nothing was merged. Both remaining lanes ended
parked, so the night closes with two new pull requests (#362, #364) and six
changes waiting for the maintainer.

- **triage-verb** (bead coding-harness-o2s1) — parked. The phase-6 re-check
  (full check green at `16ed2a62`) found three new MAJOR rows; the verdict is
  committed unchanged (`de4d8fb1`). P6-4 (an extensionless root file such as
  `Makefile` is dropped from the location) and P6-5 (an external URL counts
  as a production location) are the second and third finding of the mechanism
  the first repair addressed; P6-6 is a damaged table row that validation
  skips instead of refusing. Case repair ends here by the rule in
  `AGENTS.md`. No pull request was opened.
- **review-fewer-rounds** (bead coding-harness-3rtn) — parked. All three
  draft attempts failed the document job on one gate only: `decisions.md`
  carries no decision statement for its twelve questions. The last attempt
  (spec, design, plan, the draft of ADR 0026, the runner's findings) is
  committed unchanged and not accepted (`2098684d`). No plan card is shown
  yet.

### Added to "Needed from the maintainer"

1. triage-verb: a mechanism repair that decides "is this a tracked repository
   path" at one choke point (recommended), or a `Boundary` in the spec that
   names the supported spellings. Context in the notes of bead
   coding-harness-o2s1.
2. review-fewer-rounds: may the orchestrator write the twelve decision
   statements that restate the answers of 2026-11-09, or does the maintainer
   word them? Each needs an "accepting that" clause the answers do not state.
   Context in the notes of bead coding-harness-3rtn. This replaces the plan
   card for review-fewer-rounds in the list above.

### What the last hours showed

- The session did nothing between 03:11 and 06:36 UTC. Measured: the draft
  of review-fewer-rounds was committed at 03:08:56 UTC, the triage-verb
  re-check wrote its last output at 03:11:03 UTC, the watchdog logged a wake
  at 03:19 UTC, and the next action of the session (the note on bead
  coding-harness-3rtn) carries 06:36:45 UTC. The half-hourly heartbeat left
  no line in the log in between. The cause was not read.
- Two bead notes carry a wrong time: the note on bead coding-harness-3rtn
  says 03:12 UTC and the note on bead coding-harness-o2s1 says 06:40 UTC;
  they were written at 06:36 and 06:37 UTC.
- The missing decision statement stopped a second change (after
  verify-slots). `make change` or the interview prompt should produce it;
  no bead was opened for this at night.

### Resume here (final)

Answer "Needed from the maintainer" in the first addendum from the top, then
the two points added here. The run state folder
`~/.local/state/coding-harness/night/2026-11-08-a/` holds the log and the
queue.
