---
title: "Night-run plan — 2026-10-22/23"
category: research
created: 2026-10-22
updated: 2026-10-22
last_reviewed: 2026-10-22
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-22"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-yuw
tags: [night-run, plan, stage-2, runner, research-swarm]
---

# Night-run plan — 2026-10-22/23

**Operational plan, not an execution report.** It was prepared with the
maintainer in the joint window of 2026-10-22 (morning, Europe/Berlin), the
first one under the maintainer's new daily shape: decide and test together
in a flexible window, then work alone at night (bead coding-harness-yuw.2).
Every frame rule below is the maintainer's answer of that window; it holds
for this night only and grants nothing beyond it. Task state stays in Beads.

## Frame (maintainer, 2026-10-22)

- **Models:** as the repository routes them. Codex Sol (`gpt-6.1-sol`)
  repairs and re-checks phase 6, GLM 5.3 Flash explores and implements (Z.ai
  is available again since 2026-10-21 14:34 Europe/Berlin), Sonnet 5.5 is
  the fallback. One orchestrating Claude Code session; one sub-agent at a
  time.
- **End:** at the latest 08:00 Europe/Berlin. At 10 percent budget left no
  new large item starts; at about 5 percent the handover is written and the
  night stops. The handover comes as a pull request in every case.
- **Merges:** the orchestrator may merge only the fix pull requests against
  `scripts/stage2.py` of this queue and the phase-order gate (items 1, 2, 4,
  6, 7), and only with CI green and a fresh phase-6 re-check without an open
  BLOCKER or MAJOR. Decision pull requests (#158, the night-run routine, any
  ADR), #219 and #220 stay with the maintainer.
- **Repairs:** at most two repair rounds per pull request (Codex Sol, then a
  fresh re-check). After two rounds that still leave findings, the pull
  request stays open and unmerged, its findings go into the handover, and
  the next item starts. A security BLOCKER stops the night at once.
- **Interview records:** the maintainer's answers of 2026-10-22 count as the
  bounded interview record of each item (quoted with date and source
  "conversation 2026-10-22"); no item invents an answer.

## Queue (in this order)

| # | Item | Bead | Decided direction (2026-10-22) | Where |
|---|---|---|---|---|
| 1 | Failed-check diagnostics: F-4 and F-5 of #215 | coding-harness-8hr | collect every secret span on the original text, replace once | new worktree from `origin/main` |
| 2 | Runner time line: F-6 of #216 | coding-harness-9wp | write the time line in one place every post-call exit passes through; a test per exit; the immediate stop without fallback stays | new worktree from `origin/main` |
| 3 | Swarm test on #158, then F-65 | coding-harness-icw, coding-harness-k9rw | fresh `prepare-loop`, report, `review-loop`; F-65: any YAML error in an `answer:` field exits 3 "not measured", the prose fallback only for non-YAML text | `.claude/worktrees/research-swarm` |
| 4 | Gate phase-order | coding-harness-99v7 | answered interview records require `research.md` or a reasoned skip; prospective only | new worktree from `origin/main` |
| 5 | Research for the night-run routine | coding-harness-yuw.2 | simple single-model `stage2.py explore` over the six night-run notes (2026-10-12 to 2026-10-21); interview in the next joint window | new worktree from `origin/main` |
| 6 | Restore follows a symlinked parent | coding-harness-10w | a restore path that resolves outside the worktree is refused: nothing written, path named, run ends without fallback | new worktree from `origin/main` |
| 7 | Reviewer text read as loop state | coding-harness-i70 | the runner writes its state into a marked block of its own and reads state only there | new worktree from `origin/main` |

Not tonight: coding-harness-5mx, coding-harness-0c8, coding-harness-751,
coding-harness-hs0o, and coding-harness-04xk (an ADR 0018 change that owes
its own research and five interview answers).

## Starting state (2026-10-22, about 13:30 Europe/Berlin)

- Merged today: #213, #214, #217, #218 (eight Go models admitted on their
  data terms), #216 at `aed2999` (10:22 UTC) with F-6 open, #215 at
  `4239f8c` (10:44 UTC) with F-4 and F-5 open.
- #158 at `f187eb5`: `origin/main` merged in, `make verify` green
  (3334 passed). It carries both parts of coding-harness-k9rw: free models
  are probed with a request of the real size in `prepare-loop` and
  `prepare-explore`; paid models keep the small probe.
- Swarm test on #158: two attempts at 09:48 and 09:52 UTC stopped in round 1
  because `cat-jam-free` passed the small probe and answered the real request
  with 429. `release-loop --stage-failed` refuses before the first snapshot.
  The new probe should report it unavailable instead; not yet measured.
- Measured at 09:52 UTC: `mimo-v2.5-pro` answers "Unsupported model"
  although admitted today.
- Budget: Claude and Codex not read.

## Morning page

The handover lists: the three priorities for the maintainer, the pull
requests awaiting a merge, where an item stuck and why, and the time the
morning review took (trial criterion of coding-harness-yuw.2).
