---
title: "Night-run plan — 2026-10-20/21"
category: research
created: 2026-10-20
updated: 2026-10-20
last_reviewed: 2026-10-20
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-20"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-yuw
tags: [night-run, plan, stage-2, handover]
---

# Night-run plan — 2026-10-20/21

**Proposed operational plan, not an execution report.** The maintainer asked
on 2026-10-20 (about 20:25 UTC) for tonight's plan. It follows the
[night-run concept](2026-10-12-night-run.md) and the form of the
[previous night's plan](2026-10-19-night-run-plan.md): one orchestrating
Claude Code session, a queue set in advance, every result a pull request or a
pushed commit, no merge. It grants no new model, architecture, merge or
deployment permission. Task state stays in Beads.

## Three priorities

1. Finish the research swarm's round-12 repair (F-54, F-55) and give it one
   phase-6 re-check, so the maintainer can decide the merge of
   [PR #158](https://github.com/bicycle-brakes/monotrope/pull/158) in the
   morning.
2. Review the six runner-fix pull requests (#187 to #192, findings R-14 to
   R-27 of the review-swarm runner review) with Opus 5.5 and merge them, once
   the DeepSeek session (repairs) and the Codex session (review) are done
   with them (maintainer, 2026-10-20).
3. Leave pushed checkpoints and one morning handover by 08:00
   Europe/Berlin.

## Starting state (measured 2026-10-20, about 20:26 UTC)

- **Research swarm** (bead coding-harness-icw): worktree
  `.claude/worktrees/research-swarm`, branch `explore/research-swarm`, HEAD
  `b149992` (F-54 and F-55 taken). The Sonnet 5.5 repair of both rows lies
  uncommitted in six files. The runner rejected it at 13:19Z on one wrong
  test (mixed `int`/`str` sort keys) and the missing time line; the test was
  corrected by hand. Red first is shown by hand against `b149992`: both new
  tests fail there with an assertion. Full `make verify` at 13:20Z–13:36Z:
  3108 passed, 16 skipped, **red only on `ruff-check`** (UP038 in
  `scripts/check_research_handoff.py:335`, SIM102 in
  `scripts/stage2_research_dispatch.py:211`).
- **Phase-6 round 12** (Codex, `87a9773`): no BLOCKER, F-54 and F-55 MAJOR.
- **Runner-fix pull requests:** #187 (R-23, R-25 to R-27; bead
  coding-harness-0an), #188 (R-19 to R-21; coding-harness-011), #189 (R-2,
  R-3; coding-harness-5j4), #190 (R-14; coding-harness-1wo), #191 (R-15;
  coding-harness-4p1), #192 (R-16, R-17, R-22; coding-harness-wqw). Each was
  green in CI on its first push; #188 to #191 have new CI runs in progress
  since 20:23Z. All six change `scripts/stage2.py`; each is mergeable alone
  (GitHub, #192 not yet computed), their combination is not measured.
  Tonight a DeepSeek session repairs them and a Codex session reviews them
  (maintainer, 2026-10-20); this session does not touch their branches.
- **Bead coding-harness-9wp** (the runner writes the time line itself) is
  claimed by the other session, branch `fix/runner-time-line`; no pull
  request yet. That session is idle; it writes no beads.
- **Models:** Codex has quota again (maintainer, 2026-10-20 about 20:45
  UTC; this lifts the stop of 12:55 UTC the same day). The maintainer's own
  Codex session reviewing #187 to #192 draws on the same quota. GLM through Z.ai stays off until 2026-10-21 14:34
  Europe/Berlin; GLM through OpenCode Go works. Claude budget for the night:
  not read.
- **DeepSeek route:** `implement` and `repair` cannot name DeepSeek today
  (`implement` is GLM Flash, `repair` Codex then Sonnet); `session` can,
  as an interactive Pi window with the leak check before launch and no
  post-run checks. Whether such a window works unattended is not measured.
- **Machine:** 8 GB RAM, swap 7.1 of 8 GB in use at 20:26Z. Memory is the
  limit: one heavy job at a time.

## Queue

| # | Item | Worker | Done when, or stop |
|---|---|---|---|
| 1 | Research swarm: fix the two ruff findings, full `make verify`, book F-54 and F-55 `fixed — tests/…` with the hand red-first evidence, add the measured line under `## Time used`, commit, push; refresh PR #158's body (F-54, F-55 no longer known limits) | Orchestrator (Opus 5.5) | `make verify` green; pushed. Tell the other session the worktree is free again |
| 2 | Phase-6 re-check, round 13, of the research swarm: `stage2.py review research-swarm` | Fresh read-only Codex session; Opus 5.5 (effort medium) if Codex reports its quota spent | Findings committed unchanged in `findings.md`. No BLOCKER and no MAJOR: the morning page recommends the merge decision |
| 3 | Repair round-13 MAJOR or BLOCKER rows, if any | DeepSeek v4.1 Flash on OpenCode Go through `stage2.py session research-swarm --model opencode-go/deepseek-v4.1-flash` (maintainer, 2026-10-20); the orchestrator then checks red first against the pre-repair commit, runs `make verify` and books the rows by hand, because `session` runs no post-run checks. Sonnet 5.5 if the session writes nothing within 60 minutes | Rows fixed, `make verify` green, pushed. No round 14 tonight; whatever remains goes to the morning page |
| 4 | Review and merge the open runner pull requests #187 to #192 (maintainer, 2026-10-20: review with Opus, then merge) | One fresh read-only Opus 5.5 sub-agent (effort medium, maintainer 2026-10-20) per pull request, findings as a review comment on the pull request; the orchestrator merges | Starts only when the DeepSeek and Codex sessions are done with them: no push to the branch for 60 minutes and CI green. Order, small first: #187, #192, #188, #189, #190, #191. Per pull request: Opus review; a BLOCKER or MAJOR is repaired by DeepSeek through `stage2.py session` with red first and `make verify` checked by hand, or the pull request is left open with the reason; then bring the branch up to date with `origin/main` by a merge commit (no rebase, no force push), full `make verify` green, CI green, merge with a merge commit. **One pull request at a time.** `.claude/settings.json` asks before every merge command, so a merge waits for the maintainer's approval if he is not there; the morning page lists what waits |
| 5 | Phase 1 for bead coding-harness-py5 (every reviewer runs two more rounds inside its own context): `plans/changes/reviewer-inner-rounds/research.md` | Sonnet 5.5 sub-agent, own worktree (not `stage2.py explore`: GLM Flash via Z.ai is off, and `--stage2-off` routes to Haiku, which wrote no research — bead coding-harness-e7m) | `research.md` pushed as a draft pull request with the interview questions (ADR change: at least 5) on the morning page. No spec, no code. Inputs: the 19-pass yield of PR #184 (6 of 17 later passes found nothing) and how Pi and OpenCode Go keep one context across turns |
| 6 | Reserve: measure test quality with mutation testing (bead coding-harness-bvy) on `scripts/check_research_handoff.py` | Sonnet 5.5 sub-agent, own worktree; the tool in a scratch environment, not in the lock | A dated note under `docs/research/` with tool and version, commit, score, surviving mutants by kind and run time, as a pull request. Appetite 2 hours; stops when the run would not finish by 06:00 Europe/Berlin |
| 7 | Reserve: close bead coding-harness-y9q (`make venv` picks an unusable `python3`) if PR #174, merged, meets its acceptance | Orchestrator | Acceptance checked against `main`; bead closed with the evidence, or a note on what is missing |
| 8 | Reserve: check whether the F-53 rework (timing tests assert order, not speed) already fixed bead coding-harness-jik (a store test times out under full `make verify` load) | Orchestrator, read only | Bead closed with the evidence, or a note naming what still fails |
| 9 | Reserve: reconcile the repository with `docs/WORKFLOW.md` (bead coding-harness-i0l) | Sonnet 5.5 sub-agent, read only | A dated table under `docs/research/` (described, built, enforced) as a pull request; it includes the stop hook the doctrine describes and the README lists as not built |
| 10 | Reserve: measure the kit probe's pytest with `-n auto` (bead coding-harness-7so) | Orchestrator | A dated measurement (before, after, commit) as a comment on the bead; a change only as a pull request |
| 11 | Reserve: the CI job summary lists the beads a pull request changed (bead coding-harness-1jg.4) | DeepSeek v4.1 Flash through `stage2.py session` in the change's own worktree, red test first; the orchestrator checks red first and `make verify` by hand; Sonnet 5.5 if the session writes nothing within 60 minutes | `make verify` green, pull request open; not touching `scripts/stage2.py` |
| 12 | Reserve: translate the German left in `docs/governance/` (bead coding-harness-yim) | Sonnet 5.5 sub-agent, own worktree | One pull request for `docs/governance/` alone; `scripts/` and `tests/` stay untouched tonight because #187 to #192 change them |
| 13 | Morning handover | Orchestrator | A dated file under `docs/journal/handover/` as a pull request by 08:00 Europe/Berlin |

Items run strictly one after another. **No two `make verify` runs at the same
time** and at most one sub-agent at a time, because of the memory limit.

## Not tonight

- No merge except #187 to #192 under item 4; in particular not #158 or #184.
- No Orca evaluation (bead coding-harness-dzp) tonight: the maintainer
  holds it back for a research-swarm run after #158 (2026-10-20).
- No GLM call through Z.ai.
- No implementation of coding-harness-py5; no live research-swarm run.
- The maintainer decisions R-22 (provenance class of
  `decisions/gates.yaml`) and R-24 (may the runner set the `Broke a test`
  mark it proved) are not taken; the morning page asks them, one at a time.
- No work in the other session's worktree `runner-time-line`
  (coding-harness-9wp), and none on the branches of #187 to #192 while the
  DeepSeek and Codex sessions still push to them.

## Stop rules

- At 10 % of a five-hour window left, start no new large step; at about 5 %
  checkpoint and wait for the reset.
- Two failed repairs, an exhausted appetite, a missing maintainer decision or
  an unresolved ambiguity stop that item; record the reason and go on with
  the next independent item. No question is asked overnight and no answer is
  invented.
- A leak-check BLOCK ends foreign calls without fallback.
- Tracker first, git second. This session is the only tracker writer; it
  writes a checkpoint comment on the item's bead after each green step and
  only while no `make verify` runs.
- A sub-agent commits and pushes after every green step and ends its report
  with a `Resume:` line. One that has handed back and lingers is stopped.
- No force push, amend, bare stash, customer instance or secret read.

## Morning page (08:00 Europe/Berlin)

One page: the round-13 verdict for #158 and whether it is ready to merge; the
what of #187 to #192 was merged, what waits for a merge approval and why; the interview
questions of coding-harness-py5; the mutation score if item 6 ran; the
decisions R-22 and R-24; pull requests awaiting the maintainer; where work
stopped and why; measured spans.
