---
title: "Session handover — eleven runner and gate fixes from a cloud session, as of 2026-10-25"
category: handover
created: 2026-10-25
updated: 2026-10-25
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "Opus 5.5, 2026-10-25"
tags: [handover, cloud, stage-2, runner, gates]
target_ref: f8a6b33
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

On 2026-10-25 the maintainer told this Claude Code cloud session that it
was the only writer, and asked it to take over the whole workflow (spec,
plan and implementation) for the open beads it could do there. The cloud
container reaches GitHub and the Claude API, but not Codex, GLM (Z.ai) or
OpenCode Go. So the runner's model calls, the review loop (phase 4b) and
the phase-6 Codex review could not run. This session wrote research, spec,
plan and code by hand for each change, and recorded the deviation in each
change folder.

Result, as of 2026-10-25 about 13:00 UTC, against `main` `f8a6b33`:

- **Pull request #228** (restore-symlink-parent, coding-harness-10w):
  - F6-4 repaired by hand under the maintainer's answer Q-2 (strict), commit `62ae966`.
  - `main` merged in (`4b65a4d`); the body is current.
  - Hosted CI green.
  - A phase-6 re-check in a fresh Codex session is owed.
- **Eleven new draft pull requests (#234 to #244)**, one bead each. All are
  built red-first, with `make verify` green except the gates this
  container cannot run (listed below). For each, the review loop and the
  phase-6 Codex review are owed.

| PR | Bead | What it fixes | Base |
|---|---|---|---|
| #234 | coding-harness-0c8 | the pre-existing-change check sees index-only changes | main |
| #235 | coding-harness-6jg | an unreadable finding table refuses the whole review round | main |
| #236 | coding-harness-2i9j | finding lines without a closing pipe are read; unreadable answers are kept | #235 |
| #237 | coding-harness-4x2c | `verify_all.sh` exports a relative `PYTHON` as absolute (the cause of the local leerprobe red) | main |
| #238 | coding-harness-vque | a malformed finding line beside valid rows refuses the round | #236 |
| #239 | coding-harness-7g6h | the runner clears the ledger's `not yet written` marker for tests that exist | main |
| #240 | coding-harness-rcyf | `findings.md` goes back when the commit guard refuses a repair | main |
| #241 | coding-harness-e7m | the explorer is told its role; an answer naming no repository file is refused | main |
| #242 | coding-harness-fdz | an attempt's new files are added intent-to-add before `make verify` | main |
| #243 | coding-harness-b5w | a run starts on a failed run's derived leftovers | main |
| #244 | coding-harness-k2r | interview-minimums reads no record inside a fence | main |

Hosted CI was green on #234, #235 and #237 when checked (about 12:00 UTC);
the later ones were not checked before this note.

## What to do first

1. **Replay the tracker writes (below) from the Mac**, before anything
   else writes the tracker. They exist only in this container's Dolt
   database: `tools/bd dolt push` was refused by the container's proxy
   (HTTP 403 on `refs/dolt/data`), and the container is reclaimed after
   the session.
2. **Merge #237 first** once reviewed: it makes `PYTHON=.venv/bin/python3
   make verify` green on leerprobe locally, so every later local verify
   is clean.
3. **For each pull request, run the review loop and the phase-6 Codex
   review** (`stage2.py review-loop <change>`, then `review <change>`). The
   change folder names match the pull requests' branches:
   - `dirty-index`
   - `review-loop-row-ids`
   - `review-row-closing-pipe`
   - `verify-absolute-python`
   - `review-mixed-malformed-row`
   - `ledger-marker`
   - `repair-restore-status`
   - `explore-role`
   - `verify-stages-new-files`
   - `tolerate-derived-leftovers`
   - `interview-fenced-examples`
4. **#228 needs its phase-6 re-check** of the F6-4 repair (`62ae966`) in a
   fresh read-only Codex session.
5. **Merge order with conflicts in mind:**
   - #235 → #236 → #238 are stacked; retarget each to `main` after its base merges.
   - #240 and #228 both touch `run_attempts`; whichever merges second needs a look at that hunk.
   - #234, #242 and #243 touch the pre-existing-change check and `verify_attempt` near each other.

## Tracker writes to replay

All made in this container on 2026-10-25, none pushed:

```sh
tools/bd update coding-harness-0c8 --claim
tools/bd update coding-harness-6jg --claim
tools/bd update coding-harness-2i9j --claim
tools/bd update coding-harness-vque --claim
tools/bd update coding-harness-4x2c --claim
tools/bd update coding-harness-7g6h --claim
tools/bd update coding-harness-rcyf --claim
tools/bd update coding-harness-e7m --claim
tools/bd update coding-harness-fdz --claim
tools/bd update coding-harness-b5w --claim
tools/bd update coding-harness-k2r --claim
tools/bd close coding-harness-y9q --reason="Already fixed on main by df7d2a5 (fix(make): make venv refuses a python3 that cannot install the lock); found open on 2026-10-25."
tools/bd comments add coding-harness-4x2c "2026-10-25: cause measured — a relative PYTHON (.venv/bin/python3) reaches the leerprobe gate's foreign repository, where it names nothing; fix in PR #237."
tools/bd dolt push
```

Each bead is closed by its pull request's last commit (`Closes-Bead:`)
after the merge.

## What is measured

- **Local leerprobe red (coding-harness-4x2c), cause found.**
  `scripts/kit/probe.py` on `f8a6b33`:
  - green with `PYTHON` unset;
  - red with exactly the two `test_ci` cases when `PYTHON=.venv/bin/python3`;
  - green with an absolute `PYTHON`.

  An earlier guess in this session (uncommitted files) was wrong and is
  refuted in the change's `research.md`. Until #237 merges, run local
  verifies with an absolute `PYTHON`.
- **Container limits:**
  - `test_an_unreadable_target_is_named_by_its_repository_path` fails because the container runs as root.
  - 16 `tests/test_pi_contract.py` cases error because the pinned Pi needs Node 26 and the container has Node 22.
  - The `ruleset` gate cannot reach the GitHub API through the proxy.
  - `tools/bd dolt push` is refused (403).
- **Side finding, not filed:** the `pi` test stand-in in
  `tests/test_stage2.py` reads `calls.jsonl` while a parallel swarm member
  may be appending to it. Once in this session, a run failed with a
  `JSONDecodeError` from the stand-in; four reruns passed. It is recorded
  in `plans/changes/review-loop-row-ids/findings.md` and can touch any
  parallel-swarm test. It is related to coding-harness-jik (load-sensitive
  tests).

## What is open and needs the maintainer

- **#229** (loop-state-block, coding-harness-i70): rows L3-1 to L3-5 are
  undecided. The PR body describes them.
- **coding-harness-4295**: which model takes the two research-swarm seats
  (a decision pull request; recommendation in the bead: `mimo-v2.6-pro`).
- **coding-harness-e7m, first route:** moving `--stage2-off` explore from
  Haiku 5.5 to Sonnet 5.5 is a model-routing decision (beads
  coding-harness-ylu, coding-harness-f44). #241 took the bead's second
  route instead.
- **coding-harness-70rw** (retry a malformed paid answer once) is a
  proposal, not decided.
- **coding-harness-99v7** (gate: research before interview) is a feature.
  It owes three interview answers and the ADR question; not started.

## Not done here, and why

Everything that needs Pi, Codex, OpenCode Go, the macOS Terminal or paid
model trials:

- coding-harness-bas, coding-harness-rm8 and coding-harness-nlq (session launch);
- coding-harness-k9rw (probing free models);
- coding-harness-duue and coding-harness-vcci (Pi alternatives for Codex);
- coding-harness-km1 (comparing OpenCode Go reviewers).

coding-harness-6ie and coding-harness-83e each hold an open question in
their bead text, so they were left for the maintainer.

# Addendum, 2026-10-25 about 15:15 UTC

## Whole-runner review and its fixes

An Opus 5.5 subagent reviewed the stage-2 runner read-only, over `main`
`f8a6b33` with #228 and #234 to #244 merged together. It found six rows,
each reproduced. Each is fixed red-first in the pull request it came from:

| Row | Severity | Pull request | What it fixes |
|---|---|---|---|
| R-1 | MAJOR | #239 | an aliased plan is refused before its ledger marker is cleared, so no write leaves the worktree |
| R-2 | MAJOR | #238 | an unclosed finding-shaped line alone refuses the round, so it cannot end the loop clean |
| R-3 | MINOR | #243 | a stamp-only leftover is judged on masked file versions, not by diff line prefixes |
| R-4 | MINOR | #240 | `findings.md` goes back only before a commit, never after a refused restoration |
| R-5 | MINOR | #242 | the intent-to-add entries are dropped right after `make verify` |
| R-6 | MINOR | #241 | an over-long word cannot crash explore's repository-file check |

## A twelfth pull request

**#246** locks the `pi` test stand-in's call log, so parallel swarm members
no longer race on it. This was the side finding above (the `JSONDecodeError`
from the stand-in). Its bead was created in this container only; the
replay commands are in #246's body. Run them with the others above.

## Integration

All thirteen runner pull requests (#228, #234 to #244, #246) were merged
together on a scratch branch. The conflicts were mechanical: tests appended
at the end of `tests/test_stage2.py`, and functions inserted next to each
other in `scripts/stage2.py`. No logic conflict. The merge order above
stands; whichever of each pair merges second needs `main` merged in.

## #229 (loop-state-block)

- **L3-1 and L3-5: repaired.** The maintainer took both rows in the
  conversation. A Sonnet 5.5 subagent repaired them instead of Codex
  (`53e9dda`, then `3b2f1a4` for the frontmatter date). The change folder's
  `findings.md` records the deviation from ADR 0017.
- **L3-4: already done** on 2026-10-24 (`72979ad`).
- **L3-2 and L3-3 (two docstrings): open.** Their wording lives only in the
  loop record on the maintainer's machine.
- The loop record still lists L3-1 and L3-5 as open. Mark them there.
- Hosted CI is green on `3b2f1a4`. Phase 6 is owed.

## CI at 15:10 UTC

Green on #228, #229 and #234 to #246.
