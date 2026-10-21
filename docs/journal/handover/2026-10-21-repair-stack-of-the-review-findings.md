---
title: "Session handover — the repair stack of the review-swarm findings, as of 2026-10-21"
category: handover
created: 2026-10-21
updated: 2026-10-21
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: pi
  version: "Sonnet-class session through Pi, 2026-10-21"
tags: [handover, session, review-loop, stage-2, runner, stack]
target_ref: 7241e94
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

The 28 findings of the review-swarm review (`2026-10-20-review-swarm-runner-review.md`)
are now built: every one that a pull request can carry sits in the stack below,
each change green under `make verify` and each in a pull request of its own. Ten
pull requests, stacked so that every one reviews alone: #188 to #192 (the first
batch), #194 and #196 (bead `coding-harness-3ql`, in its two parts), #197
(`coding-harness-16z`), #198 (`coding-harness-tex`), #199 (R-24), #200 and #201
(two decision pull requests) and #202 (the written read boundary). **Nothing is
merged by this session**, and the merge order is the stack order.

The other session in the main checkout wrote its own handover for the same night
(`2026-10-21-night-run-tenth.md`, PR #195) and merged #187 there. Two sessions,
two handovers, no conflict: that one covers the research swarm and #158, this one
the review findings.

## The stack, in merge order

| PR | Bead | Findings | Base | Head commit |
|---|---|---|---|---|
| #188 | `coding-harness-011` | R-19, R-20, R-21 — the runner's own tooling, hashed and bounded | `main` | `639b9d4` |
| #189 | `coding-harness-5j4` | R-2, R-3 — record keyed by worktree, anchored release cut | `fix/runner-own-tooling` | `8329f3c` |
| #190 | `coding-harness-1wo` | R-14 — one runner per loop record | `fix/record-dir-key` | `c6f3292` |
| #191 | `coding-harness-4p1` | R-15 — the paid diff is bounded, and a cut round cannot end the loop | `fix/review-loop-lock` | `0380ed9` |
| #192 | `coding-harness-wqw` | R-16, R-17, R-22-runner-half — the commit guard, git resolved once | `fix/review-prompt-bounds` | `0678b6d` |
| #194 | `coding-harness-3ql` (part 1) | R-6, R-10 — round and consumption in one write; shifted mark refused | `fix/commit-guard` | `726ceb2` |
| #196 | `coding-harness-3ql` (part 2) | R-7, R-8, R-9, R-11, R-13, R-12, `ll5` | `fix/loop-record-order` | `c2ba73c` |
| #197 | `coding-harness-16z` | R-4 — the `ausgeschlossen` list binds both admission paths | `fix/loop-limits-deadline` | `4c5861f` |
| #198 | `coding-harness-tex` | R-1 — `release-loop --stage-failed` retires a wedged stage | `fix/excluded-binds` | `412349b` |
| #199 | `coding-harness-0an` | R-24 — the repair writes the mark its own proof shows | `fix/retire-failed-stage` | `f7ab041` |
| #200 | `coding-harness-wqw` | R-22 — `decisions/gates.yaml` is `human-decided` (decision PR) | `fix/repair-mark` | `9446abe` |
| #205 | `coding-harness-mkg` | the dead ladder rung is replaced (decision PR; #201 was closed by a force-push and re-opened with this number) | `decide/gates-provenance` | `1e92f57` |
| #202 | `coding-harness-8df` | R-5 — the read boundary written down, enforcement named as its own work | `decide/ladder-rung` | `7241e94` |

Every PR names its findings and its tests in the body; every one was verified
locally with `PYTHON=.venv/bin/python3 make verify` in the worktree that holds
it (about 2300 tests, 16 skipped), and **every PR of this stack was green in CI
when this handover was written** (2026-10-21, 09:30 UTC). The stack was rebased
onto the new #192 head (`0678b6d`, the other session's commit-guard work) after
the maintainer asked for it.

## The maintainer's answers, night interview of 2026-10-20

Eleven questions, answered one by one, in the order they were asked:

1. **Q-1** `decisions/gates.yaml` is `human-decided`, like the rulebook → #200.
2. **Q-2** the `ausgeschlossen` list binds the code → #197.
3. **Q-3** the read boundary is written down now, enforced later, and the
   isolation **must** come; `tmux`, `herdr`, `orca` are to be read as possible
   carriers → #202 plus bead `coding-harness-8df`.
4. **Q-4** the ADR 0021 amendment comes as its own decision PR, `tex` as a direct
   runner PR → #198, amendment open (see below).
5. **Q-5** `3ql` splits in two, `ll5` rides in the second → #194, #196.
6. **Q-6** R-12 hangs on `3ql` → #196.
7. **Q-7** the dead ladder rung is replaced, not removed → #201.
8. **Q-8** build by hand, not through `stage2.py` → all of it.
9. **Q-9** every block as its own stacked PR, the night ends with this handover.
10. **Q-10** repair as long as it goes, even all night on one block.
11. **Q-11** the repair writes a mark only where its own proof shows one → #199.

## What the review of this batch changed

The first six review comments on the stack were partly already answered by a
rebase (the three "reverts" in #192 were the older base, `078a0f7`), and three
were real. All six are repaired and each repair carries a test that fails
without it:

- **#191, P2** a cut diff no longer allows a clean finish; found on the way: a
  round without rows hit `KeyError` in the repair brake (`4e8fcbf`).
- **#192, P1** the draft may commit its own new ADR under `docs/adr/` again
  (`human-decided` blocked it and wiped the draft); **P2** a refusal no longer
  discards pre-existing `findings.md` entries (`7550921`).

A second review round then read the whole stack and found four more, all
repaired the same way — a test per finding, red first:

- **#194, P2** the shifted-mark refusal was too broad: a Status cell carrying a
  `|` with a valid mark in the last cell is a legitimate row and stays one
  (`726ceb2`).
- **#196, P2** the second probe was neither checked nor audited: admission,
  `checked_prompt` and the audit line now sit inside the probe loop
  (`c2ba73c`).
- **#198, P2** after `release-loop` the snapshot lives in `findings.md`, so a
  run whose next stage lost every member could not be retired; `read_state(None,
  findings_text)` now supplies it (`412349b`).
- **#199, P2** `scripts/stage2_runs.py::measure` counted only a bare `yes`, so a
  proven repair's mark vanished from the metrics; it reads the leading word
  now (`f7ab041`).

## Value that is still open

- **The ADR 0021 amendment ("a stage may end as failed")** is not written. The
  `interview-minimums` gate refuses an ADR change without a change folder whose
  spec lists it under `adr_files` and whose `decisions.md` carries five
  maintainer answers. The night interview supplies five substantive answers
  (Q-1, Q-2, Q-3, Q-4a, Q-7), so the amendment can be opened as a change of its
  own with those records. Until then #198 stands without it.
- **R-5's enforcement** (the paid swarm's read boundary) is a bead and a
  paragraph, not a mechanism. `tmux` alone separates no filesystems; `herdr` and
  `orca` are unread.
- **The Kimi ids in `model-endpoints.yaml`**: `excluded_problem` binds an entry
  only when it names ids (`modelle`), and the Kimi entry is prose. Adding the ids
  is a decision PR for the maintainer.
- **The nine open PRs of the first batch** (#188 to #192) still await the
  maintainer's review; #187 is merged (`c3196a2`), so #188's base is stale and
  wants a rebase once someone starts merging.

## Resume action

Read the CI state of #197 to #202 (`gh pr checks <n>`); rebase the stack from
the bottom whenever the maintainer merges a lower PR, since every base names the
branch below it. Then open the ADR 0021 amendment as a change folder with the
five answers above.

## Tracker state (cut-off 2026-10-21, 03:00 UTC)

Claimed and commented, never created: `coding-harness-3ql`, `coding-harness-16z`,
`coding-harness-tex`, `coding-harness-0an`, `coding-harness-wqw`,
`coding-harness-4p1`, `coding-harness-ll5`, `coding-harness-8df`,
`coding-harness-mkg`. No bead was closed: closing follows a merge, and merging
is the maintainer's.
