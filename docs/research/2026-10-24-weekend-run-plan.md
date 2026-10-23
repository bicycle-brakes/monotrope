---
title: "Weekend-run plan — 2026-10-24/25"
category: research
created: 2026-10-23
updated: 2026-10-23
last_reviewed: 2026-10-23
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-23"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-yuw
tags: [weekend-run, plan, stage-2, runner, review-loop]
---

# Weekend-run plan — 2026-10-24/25

**Operational plan, not an execution report, and not yet in force.** It was
drafted by the orchestrating session on 2026-10-23 at the maintainer's
request ("plan a weekend session, take the beads not yet done, look at all
beads"). The frame below is a **proposal** that copies the frame of the
night run of 2026-10-22/23 (`docs/research/2026-10-22-night-run-plan.md`);
it holds only once the maintainer confirms it. Task state stays in Beads.

## Tracker state read for this plan

Read 2026-10-23 about 12:00 UTC with `tools/bd list` and `tools/bd ready`,
`origin/main` at `e73f77a`:

- 114 beads open, 7 in progress, 79 of the open ones ready (unblocked).
- In progress: coding-harness-9wp (this night's item 2, PR #225 in repair),
  coding-harness-3ar (epic), coding-harness-6jg, coding-harness-6th,
  coding-harness-csm, coding-harness-k9rw, coding-harness-icw. Whether the
  last five are still worked or only left claimed was not read.

## Frame (proposed, needs the maintainer's confirmation)

- **Models:** as the repository routes them: GLM 5.3 Flash implements,
  Sonnet 5.5 is the runner's fallback, Codex Sol (`gpt-6.1-sol`) drafts,
  repairs and re-checks phase 6. One orchestrating Claude Code session, one
  change at a time.
- **Window:** Saturday 2026-10-24 morning to Sunday 2026-10-25 evening,
  Europe/Berlin. **Clocks go back on Sunday 2026-10-25 at 03:00 CEST to
  02:00 CET**; times in the handover are written in UTC.
- **Merges:** the orchestrator merges only the `fix/` pull requests of
  block A and B, each with CI green and a fresh phase-6 re-check without an
  open BLOCKER or MAJOR. Decision pull requests (#158, any ADR, the
  night-run routine) and #219 stay with the maintainer.
- **Repairs:** at most two repair rounds per pull request; after that the
  pull request stays open and the next item starts. A security BLOCKER stops
  the run at once.
- **Budget:** at 10 % left no new item starts; at about 5 % the handover is
  written as a pull request and the run stops. Claude weekly budget: 84 %
  used at 2026-10-22 about 22:50 CEST, current value not read.
- **Permissions:** the allow rules in `.claude/settings.local.json` of this
  machine cover `stage2.py`, `git push origin fix/*`, `gh pr *` and
  `PYTHON=.venv/bin/python3 make verify*` (added 2026-10-23). A command
  with a pipe or another prefix is refused; worktree creation and tracker
  closes were refused once after a merge (handover of 2026-10-23).

## Queue

Each item runs the seven phases in a new worktree from `origin/main` on a
`fix/` branch. "Direction" names where the decided direction is recorded;
an item without one needs a maintainer answer before it starts (house rule:
no item invents an answer).

### Block 0 — carried over from the night

| # | Item | Bead | Direction | State 2026-10-23 |
|---|---|---|---|---|
| 0 | Runner time line on every post-call exit | coding-harness-9wp | night plan, item 2 | PR #225, repair round 1 running |

### Block A — runner safety, Saturday

| # | Item | Bead | Class | Direction |
|---|---|---|---|---|
| A1 | A restore through a symlinked parent is refused | coding-harness-10w | bounded | night plan, item 6 |
| A2 | Reviewer text in the phase-6 verdict is not read back as loop state | coding-harness-i70 | bounded | night plan, item 7 |
| A3 | The pytest bytecode cache in the venv is not a tool the attempt wrote | coding-harness-q94b | bounded | **needs an answer**: exclude `__pycache__` under the venv, or snapshot after a warm-up |
| A4 | An empty, refused or malformed phase-6 answer is not a finished review | coding-harness-5mx | bounded | proposed in the bead (runner audit 2026-10-21); **needs a confirmation** |
| A5 | The review verb takes the record lock before it releases the loop record | coding-harness-751 | bounded | proposed in the bead: refuse and keep the record; **needs a confirmation** |
| A6 | The dirty-tree check sees index-only changes; the commit keeps staged content | coding-harness-0c8 | bounded | **needs an answer** |

### Block B — review loop and gates, Sunday

| # | Item | Bead | Class | Direction |
|---|---|---|---|---|
| B1 | Gate phase-order | coding-harness-99v7 | bounded | night plan, item 4 |
| B2 | Rows without a closing pipe keep the raw answer | coding-harness-2i9j | bounded | night plan, position 8 |
| B3 | A malformed row next to a valid one stays in the decision table | coding-harness-vque | bounded | proposed in the bead; **needs a confirmation** |
| B4 | A refused repair attempt does not leave its row marked fixed | coding-harness-rcyf | bounded | **not read in full**; check the bead first |

### Block C — needs the maintainer, not unattended

| Item | Bead | Why it waits |
|---|---|---|
| Research swarm repair (F-65, L4-1 to L4-3) on #158 | coding-harness-icw, coding-harness-k9rw | decision PR; night item 3; can run on the maintainer's word |
| Night-run routine research, then interview | coding-harness-yuw.2 | night item 5; the research can run alone, the interview cannot |
| A clean free round ends the review loop, so no Flash or paid model reads the change | no bead yet | observed on #223 and #225 (2026-10-22/23); is this ADR 0021's intent? |
| Explicit maintainer restart of a completed loop | coding-harness-0xjr | ADR 0021 amendment |
| Isolate each writing attempt (closes znc, 6ie, b5w as one class) | coding-harness-s9r | feature; container choice open since 2026-10-15 |
| Carry the permission rules with the kit | coding-harness-oatb | feature; research first |
| One place for phase models and effort | coding-harness-ylu | ADR |

### Hygiene, between items

- Local `make verify` is red on `leerprobe` (two tests in `tests/test_ci.py`)
  while hosted CI is green: no bead yet; create one with the measurement.
- The flaky SIGKILL test under full load (coding-harness-jik).
- Check whether coding-harness-6th, coding-harness-csm, coding-harness-6jg,
  coding-harness-k9rw and coding-harness-icw are still worked; unclaim what
  is not.

## Not this weekend

Vision and evaluations (coding-harness-25h, coding-harness-dzp,
coding-harness-al8, coding-harness-52pd, coding-harness-jru,
coding-harness-326), the rename (coding-harness-fjr), public readiness
(coding-harness-lir), the `stage2.py` refactor (coding-harness-vg9), the
translation (coding-harness-yim) and every ADR change that owes its own
research and five interview answers.

## Realistic size

Measured on 2026-10-23: item 2 of the night took about 80 minutes for
implement (two failed GLM Flash attempts, then Sonnet 5.5) and about 15
minutes for the free round and phase 6, before its first repair. At two to
three hours per bounded item including review and repair, block A fills
Saturday and block B fills Sunday; block C needs the maintainer.

## Weekend page

The handover lists: the pull requests awaiting a merge, where an item stuck
and why, the answers block C still needs, and the measured hours per item.
