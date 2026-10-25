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

# Addendum, 2026-10-25 about 16:40 UTC: pre-review of the eleven pull requests

At the maintainer's request, a read-only Opus 5.5 subagent reviewed each of
#234 to #244 before phase 6. Each row was reproduced, then fixed red-first:
by this session, or by a Sonnet 5.5 subagent whose diff this session read
before committing. Each change folder's `findings.md` has a section
"Pre-review by an Opus 5.5 subagent, 2026-10-25" with every row. **This
stands in for nothing: phase 6 (Codex) is still owed on every pull request.**

| PR | Heaviest rows | Head after the fixes |
|---|---|---|
| #234 | 1 minor (a test that could not fail) | `69a3cd7` |
| #235 | 4 minor; 1 on the not-now list | `90399c6` |
| #236 | 1 major (named a skipped header line, against decision Q-1 (2)), 6 minor | `25a126a` |
| #237 | 2 minor (an unquoted interpreter path) | `22627f8` |
| #238 | 1 major (spec missed the R-2 behaviour), 4 minor | `9d3d25a` |
| #239 | 4 minor | `30c7d7e` |
| #240 | 1 minor, 1 nit | `b1693d7` |
| #241 | 3 major (absolute paths, a trailing full stop, an echoed refusal), 4 minor | `04cf97d` |
| #242 | 2 minor (argument-list overflow, names read as patterns) | `18d46c1` |
| #243 | 2 major (line endings let a whole-file change pass, or refused a real stamp), 5 minor | `82a91c9` |
| #244 | 2 minor (a CRLF fence never closed), 4 nits | `fec1046` |

- **The stack #235, #236, #238** carries the fixes forward by merge commits.
  The merge into #238 adjusted one planted test line that #238 now rightly
  refuses; the commit message says why.
- **When #240 and #228 are both merged,** the `restore_findings(kept)` call
  from #240 should become #228's `put_findings_back(original=error)`, or
  that one findings write skips the alias preflight. #240's `findings.md`
  says so.
- **Known limits written into the specs** rather than fixed:
  - #238: a finding without its ID column; phases 6 and 2a do not use the
    check.
  - #241: the file check is a heuristic.
- Hosted CI was green on every head above at 16:37 UTC.

# Addendum, 2026-10-25 about 19:10 UTC: every finding not yet worked

At the maintainer's request, five read-only Opus 5.5 subagents reviewed the
review loop (parts A and B) and the research swarm (parts 1 to 3) in depth.
Three fix agents then worked the findings test-first. This addendum lists
everything that is **not** fixed yet, with where it stands. Full reports with
reproductions are in each change folder's `findings.md`.

## What was fixed, for orientation

- **#249** (`fix/review-loop-deep-a`, `a41e064`): DL-A-1 to DL-A-10, loop
  control and state. Draft; no bead yet.
- **#250** (`fix/review-loop-deep-b`, `6ade811`): DL-B-1 to DL-B-7, DL-B-10,
  DL-B-11, DL-B-12, DL-B-14, plus RS-3-3 and RS-3-8 (catalog fields in
  `activate_overlay`). Draft; no bead yet.
- **#238** (`5b480ea`): the two known limits listed above (a finding
  without its ID column; phases 6 and 2a without the check) are now fixed.
- **#158** (`explore/research-swarm`): a fix agent is working every RS row
  and coding-harness-jik; its first commit `fe864e5` addresses the two
  BLOCKERs RS-3-2 and RS-1-2. Until its report, every RS row below counts
  as open.

## Needs a decision of the maintainer

| Row | What is wrong | Recommendation |
|---|---|---|
| DL-B-13 (**due 2026-10-31**) | The DeepSeek retention reading says "valid through 2026-10-31", but the runner only checks that `aufbewahrung` is non-empty, so it admits the model for ever. | A machine-readable `gilt_bis: YYYY-MM-DD` in `modelle_terms`, checked by `terms_problem`; a past date skips and names the model. Decision pull request. |
| DL-B-8 | Where every OpenCode Go call goes is taken from the pi.dev catalog's per-model `baseUrl`, never compared with a declared address. Test P6-14 even asserts it. | Declare `adresse: https://opencode.ai/zen/go/v1` on the `opencode-go` entry; drop, with a notice, any overlay definition whose `baseUrl` or `api` differs. Decision pull request. |
| DL-B-9 | The repair brake (ADR 0021 decision 7) reads an Origin cell (`base` / `fix-r<N>`) that no prompt tells a reviewer how to fill. | The orchestrator sets Origin when it decides a row; the runner refuses a taken row whose Origin is neither. No prompt change. |
| DL-A open 1 | With #249, a loop record lost for good blocks the change: `--restart` needs a completed round, so no verb continues. | A recovery verb; it touches ADR 0021 decision 9. |
| #247 mixed case | The maintainer answered "also solve the mixed case": a free member with 429 must be remembered without a written round. | ADR 0021 amendment (decision pull request with interview), then a dropped-member entry in the loop record. Not started. |
| coding-harness-4295, e7m, 70rw, 99v7 | As listed under "What is open and needs the maintainer" above. | Unchanged. |

## Agent work still owed (no decision needed)

- **WORKFLOW §4b** does not yet describe #249's `Record digest:` line, the
  `Loop attempt:` no-round line or the lost-record refusal.
- **Merge order #249 / #250 / #229 / #238:** all four change `review_loop`,
  `reviewer_blocks`, `_record_lines` or the release; whoever merges later
  needs a conflict resolution (agent).
- **Stand-in race in the test suite:** parallel Pi stand-ins append to
  `calls.jsonl` while others read it; one `JSONDecodeError` flake seen in
  `test_ineligible_paid_models_are_skipped_and_named`.
- **`stage2.cut_rounds`** raises `ValueError` (strict `zip`) on a loop record
  with no round headings (seen by research review 2, on main).
- **#229 L3-2 / L3-3:** the maintainer answered "search and repair
  yourself": check every docstring #229 touches, fix stale ones, note in
  `plans/changes/loop-state-block/findings.md` that the match with L3-2/L3-3
  is uncertain. Not started.
- **coding-harness-csm** (runner precheck): the maintainer answered "yes,
  build it": merge main into `feat/runner-precheck`, check the plan against
  today's runner, build test-first, ask on a material deviation. Not started.
- **Known limits of #250:** a rung refused at replacement stays in the run
  snapshot (`release-loop --stage-failed` retires it); in a narrow race a
  call line is written for a replacement that then does not start (named,
  not consumed); dropped catalog fields are named on stderr only, not in the
  record.
- **Beads:** #249 and #250 carry `bead: to be filed`; the tracker push is
  refused from the container (403).

## Research swarm rows (on #158, in work)

| Row | Severity | In one line |
|---|---|---|
| RS-3-2 | BLOCKER | `file://` paths pass the path lock; Pi reads any file and sends it to a Go model (F-24 repair incomplete). First fix in `fe864e5`. |
| RS-1-2 | BLOCKER | U+2028/2029/0085 in a web excerpt break the handoff gate; CI turns red repository-wide. First fix in `fe864e5`. |
| RS-1-5 | MAJOR | Web text reaches the judge with system-prompt authority; `unresolved` claims need no disagreement. |
| RS-1-9 | MAJOR | An unclosed fence earlier in research.md hides later runs; the gate says "exempt". |
| RS-1-4 | MAJOR | The capture grades a home-canary leak OBSERVED and still passes; a regression of F-24 goes unseen. |
| RS-1-6 | MAJOR | Judge packet limit 200,000 characters is exceeded by ordinary reports (about 290,000 at five claims each). |
| RS-1-1 | MAJOR | A failed store clear re-binds the wrong text; the next run reuses nothing (39 calls again). |
| RS-1-8, RS-2-6 | MAJOR | research.md is rewritten non-atomically and with universal newlines; a kill loses earlier research, CRLF is rewritten. |
| RS-3-1 | MAJOR | One malformed catalog row makes Pi reject all of models.json; free models vanish, seats call an unchecked endpoint. |
| RS-3-3 | MAJOR | `samplingParams` swaps the model in the request body (fixed on main by #250; the branch's own copy is in work). |
| RS-3-4 | MAJOR | Research Pi commands lack `--offline`; Pi downloads unpinned `rg`/`fd` and runs them with the key. |
| RS-1-3, RS-1-7, RS-1-10, RS-1-11, RS-1 dead branch | MINOR/NIT | Later numbered lists read as criteria; empty-packet gap not enforced; forged envelope trusted; NFC and confusables. |
| RS-2-1 | MINOR | `release-loop` deletes the research store and its lock. |
| RS-2-2, RS-2-3, RS-2-4, RS-2-5 | MINOR/NIT | Tracked symlinks and submodules stop the freeze; store guard misses the common git dir; older results never reused; reuse chain loses its origin. |
| RS-3-5 to RS-3-8, RS-3 NIT | MINOR/NIT | Nested duplicate key kills the source; curly-quote symlink passes the lock; absent `baseUrl` admitted; a non-string header crashes; Pi's system prompt carries local paths unchecked. |
| coding-harness-jik | — | Harden the four load-sensitive F-53 tests. Research review 2 measured that they hold up to load 29 but take 10 to 21 s each. |

## Seen but not reviewed (no finding yet)

- Review A did not cover: the availability probe and its timed exclusion
  (`PROBE_RETRY_SECONDS` 180 s against the ADR's 60 s), real multi-process
  lock races, whether draft or explore can also write findings.md, several
  restarts in a row.
- Review B did not cover: a live Pi run, Pi's real `--no-tools` behaviour,
  the probe and stage2-session paths.
- Research review 1 did not cover: whether `--restricted`/`dontAsk` confine
  the Haiku repository seat to the worktree; `stage2_research_tools.mjs`;
  `stage2_research_refs` (also splits with `splitlines`, possible false
  heading).
- Research review 2 noted, without a finding: macOS `fsync` is not
  `F_FULLFSYNC`; a case-insensitive file system could collide two free slot
  ids; orphan `.tmp-*` files stay until a complete publication;
  `Store.clear` is test-only; the freeze reads the repository twice within
  60 s.
- Research review 3 did not cover: live pi.dev and models.dev behaviour,
  Pi's `compat` and `thinkingLevelMap` fields.
