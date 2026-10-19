---
title: "Night-run plan — 2026-10-19/20"
category: research
created: 2026-10-19
updated: 2026-10-19
last_reviewed: 2026-10-19
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-19"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-yuw
tags: [night-run, plan, stage-2, handover]
---

# Night-run plan — 2026-10-19/20

**Proposed operational plan, not an execution report.** The maintainer asked
on 2026-10-19 (about 14:30 UTC) to plan tonight's session. It follows the
[night-run concept](2026-10-12-night-run.md) and the form of the
[previous night's plan](2026-10-18-night-run-plan.md): one orchestrating
Claude Code session, a queue set in advance, every result a pull request, no
merge. It grants no new model, architecture, merge or deployment permission.
Task state stays in Beads.

## Three priorities

1. Bring the research swarm (coding-harness-icw, draft
   [PR #158](https://github.com/MPAdesso/coding-harness/pull/158)) to a clean
   phase-6 verdict, so the maintainer can decide on its merge in the morning.
2. Do it within this machine's memory: one heavy job at a time.
3. Leave pushed checkpoints, accurate pull requests and one morning handover
   by 08:00 Europe/Berlin.

## Starting state (measured 2026-10-19, 14:30 UTC)

- Research swarm at `9194568`, origin/main merged in (with pytest-xdist from
  [PR #168](https://github.com/MPAdesso/coding-harness/pull/168)); full
  `make verify` green there: 3020 passed, 16 skipped, pytest 8 min 23 s, the
  whole run about 10 min.
- Phase-6 review: rounds 1 to 3 through fresh read-only Codex sessions found
  8, 5 and 3 rows. Every row through F-27 is fixed; F-1 (the attended real-Pi
  capture) is closed by the maintainer's ruling. Decisions Q-15 to Q-17 are
  recorded.
- Appetite for the research swarm: 17 h 20 min; about 13 h used (orchestrator
  sum of the plan's Time used sections, estimate).
- Machine: 8 GB RAM, swap 9.2 of 10 GB in use at 14:26 UTC, load around 18
  during `make verify`. Memory, not CPU, is the limit.
- [PR #169](https://github.com/MPAdesso/coding-harness/pull/169), a
  read-only session's handover, reports the nightly drift gate red for twenty
  nights (91 findings: finished changes whose artefacts were never archived).
- The main checkout's environment was repaired today: `.venv` rebuilt on
  Python 3.12.15 from the lock, the pinned Pi installed.
- Claude and Codex budget for the night: not read. GLM through Z.ai stays off
  until 2026-10-21 20:34 Asia/Singapore; GLM through OpenCode Go works.

## Queue

| # | Item | Worker | Done when, or stop |
|---|---|---|---|
| 1 | Phase-6 review, round 4: `stage2.py review research-swarm` | Fresh read-only Codex session | Findings committed unchanged in `findings.md` |
| 2 | Triage round 4 and repair taken rows | Orchestrator triages; one Sonnet sub-agent repairs by hand, red test first | Rows `fixed — tests/…`; full `make verify` green; pushed. A row that needs a maintainer decision stays open with a prepared question |
| 3 | Round 5 only if round 4 took a BLOCKER or MAJOR | Fresh read-only Codex session | Rounds stop at round 5; whatever remains goes to the morning page |
| 4 | Prepare #158: refresh the PR body (span, commits, findings); amend the spec line on the repository seat's absolute-path reads per Q-16 | Orchestrator | Body and spec current, pushed; the PR stays a draft until the maintainer has read the morning page |
| 5 | Archive proposal for the finished changes behind the red nightly drift gate (#169: 91 findings, 16 changes whose bead is closed) | Haiku or Sonnet sub-agent, read-only on the changes | One table in a pull request: per change its bead, bead status, artefact status and a proposal (living spec, ADR or plain archive) with a one-line reason; nothing moved |
| 6 | Remove worktrees whose branch is merged into origin/main (AGENTS.md: removed after the merge) | Orchestrator | Only a worktree with a clean status, no unpushed commit and a merged branch is removed; every other one is listed with its reason in the morning page |
| 7 | Reserve, only if 1–6 end early: `make venv` picks the first `python3` on PATH (the system's 3.9 here, which cannot install the lock); make it fail clearly or pick the pinned version (coding-harness-y9q) | Sonnet sub-agent, own worktree | Test red first, then green; `make verify` green; pull request open |
| 8 | Reserve: kit probe runs its pytest single-process (163 s, measured by #169's session); measure it with `-n auto` (coding-harness-7so) | Haiku sub-agent | A dated measurement in the bead; a change only as a pull request |
| 9 | Reserve: failed-check diagnostics copy test secrets into `findings.md` (coding-harness-8hr, security). Spec and plan are drafted; no plan card was accepted | Orchestrator | Commit the two uncommitted call records on its branch; put the plan card on the morning page. No implementation before the maintainer has seen the card |
| 10 | Reserve: `make verify` runs while new files are untracked, so the kit probe misses them (coding-harness-fdz) | Codex through `stage2.py draft`, after an explore | `research.md`, spec and plan drafted; questions and the plan card on the morning page; no implementation |
| 11 | Morning handover | Orchestrator | A dated file under `docs/journal/handover/` as a pull request by 08:00 Europe/Berlin |

Items run strictly one after another. **No two `make verify` runs at the same
time** and at most one sub-agent at a time, because of the memory limit.

## Not tonight

- No merge of any pull request, including #158 and #169.
- Acting on the drift-gate clean-up from #169: moving any change, making
  `make staleness` strict, or adding an archive step to the phase-7 prompt.
  Each needs the maintainer's decision; item 5 only prepares the per-change
  ones.
- No live research-swarm run; offline tests and local doubles only.
- No new beads for wishes already recorded (Leantime, splitting `stage2.py`,
  learning from review feedback, current research, a VS Code surface,
  interactive Pi model choice).

## Stop rules

- At 10 % of a five-hour window left, start no new large step; at about 5 %
  checkpoint and wait for the reset.
- Two failed repairs, an exhausted appetite, a missing maintainer decision or
  an unresolved ambiguity stop that item; record the reason and go on with
  the next independent item. No question is asked overnight and no answer is
  invented.
- A leak-check BLOCK ends foreign calls without fallback.
- Tracker first, git second. The orchestrator is the only tracker writer; it
  writes a checkpoint comment on coding-harness-icw after each green step and
  only while no `make verify` runs.
- A sub-agent that has handed back and lingers is stopped.
- No force push, amend, bare stash, customer instance or secret read.

## Morning page (08:00 Europe/Berlin)

One page: the phase-6 verdict for #158 and whether it is ready to merge, the
archive table to decide, the plan cards of items 9 and 10, pull requests
awaiting the maintainer, the worktrees removed or kept, where work stopped and
why, measured spans against the appetite, and the time the morning review
took.
