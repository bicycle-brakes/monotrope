---
title: "Night-run plan — 2026-10-21/22"
category: research
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-21"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-yuw
tags: [night-run, plan, stage-2, research-swarm, phase-6]
---

# Night-run plan — 2026-10-21/22

**Proposed operational plan, not an execution report.** The maintainer asked
on 2026-10-21 (about 18:00 Europe/Berlin) for a plan for tonight's session.
It follows the [night-run concept](2026-10-12-night-run.md) and the form of
the [previous plan](2026-10-20-night-run-plan.md): one orchestrating Claude
Code session, a queue set in advance, every result a pull request, no merge.
It grants no new model, architecture, merge or deployment permission. Task
state stays in Beads.

## Three priorities

1. Bring the research swarm (bead coding-harness-icw,
   [PR #158](https://github.com/bicycle-brakes/monotrope/pull/158)) to a
   phase-6 round without BLOCKER or MAJOR, so the maintainer can decide its
   merge in the morning.
2. One heavy job at a time: the machine has 8 GB RAM and 8.0 of 9.2 GB swap
   in use (measured 2026-10-21, about 18:00).
3. Pushed checkpoints, an accurate PR body and one morning page by 08:00
   Europe/Berlin.

## Starting state (2026-10-21, about 18:00 Europe/Berlin)

- #158 at `febe2aa` pushed up to `825ae65`: CI green at `825ae65`
  (run 39618859539). Since round 13 it carries Q-18 (the maintainer chooses
  the seat models on intelligence against cost) and the exclusion fix from
  PR #208.
- Phase-6 round 14 (2026-10-21): Codex F-58 to F-60 (MAJOR), independent
  deepseek-v4.1-flash through Pi D-3 to D-7 (one MAJOR). All eight rows were
  taken. The runner's repair failed twice with Codex (attempt 1: an older
  test went red; attempt 2: red-first proof refused on form) and is running
  attempt 3 on Sonnet 5.5; its result is not read at the time of writing.
- Open point in the repair: the orchestrator's taken status for D-6 said an
  exclusion "binds whatever its declared class". That contradicts the earlier
  reviewed rule O197-2 (a customer-only exclusion does not deny framework
  admission), and attempt 2 rewrote that test. The orchestrator proposed to
  restore it and keep D-6 to: an unknown class is malformed (exit 2), an
  exclusion of the public class binds the online seats. **The maintainer
  answered on 2026-10-21 (about 18:30): exclusions stay class-scoped as
  before** ("sperrung für kundenkonto wie vorgesehen"); the work is bead
  coding-harness-dxso.
- Budget: Claude and Codex not read. GLM through Z.ai is available again
  since 2026-10-21 14:34 Europe/Berlin; GLM through OpenCode Go works.
- The Artificial Analysis key (`ARTIFICIAL_ANALYSIS_API_KEY`) is not yet
  provided; the live intelligence reading stays unverified.

## Queue

| # | Item | Worker | Done when, or stop |
|---|---|---|---|
| 1 | Read the round-14 repair result (attempt 3, Sonnet 5.5). Then bead coding-harness-dxso: restore the O197-2 test (a customer-only exclusion does not deny framework admission); an exclusion naming no declared data class is malformed (exit 2); an exclusion of the public class binds the online seats and free researchers; correct D-6's Status | Orchestrator; one Sonnet sub-agent for the repair, red test first | Every round-14 row `fixed — tests/…` or left open with its reason; coding-harness-dxso closed; full `make verify` green; committed and pushed |
| 2 | Phase-6 round 15: `stage2.py review research-swarm` | Fresh read-only Codex session | Findings committed unchanged in `findings.md` |
| 3 | Triage round 15 and repair taken rows through `stage2.py repair research-swarm` | Orchestrator triages; Codex repairs, Sonnet after two failed checks (ADR 0017) | Rows fixed, `make verify` green, pushed. A row that needs a maintainer decision stays open with a prepared question |
| 4 | Round 16 only if round 15 took a BLOCKER or MAJOR | Fresh read-only Codex session | Rounds stop at round 16; the rest goes to the morning page |
| 5 | Refresh #158: merge origin/main if it moved, PR body (rounds 14–16, commits, known limits), wait for green CI | Orchestrator | Body current, CI green, decision block drafted for the morning page; no merge |
| 6 | Reserve: name the slow tests for the CI work (bead coding-harness-7so): one local `pytest --durations=30` run, read-only | Orchestrator | A dated measurement as a comment on the bead; no code change |
| 7 | Morning handover | Orchestrator | A dated file under `docs/journal/handover/` as a pull request by 08:00 Europe/Berlin |

Items run strictly one after another. **No two `make verify` runs at the same
time** and at most one foreign call or sub-agent at a time.

## Not tonight

- No merge of any pull request, including #158.
- No independent Pi reviewer: `stage2.py session` needs the maintainer to
  start the command in the VS Code terminal (bead coding-harness-rm8), so
  DeepSeek does not run unattended. Codex alone reviews rounds 15 and 16.
- No live research-swarm run and no Artificial Analysis call; offline tests
  and local doubles only.
- No work on the beads recorded today: Pi as a phase-6 reviewer
  (coding-harness-duue), Pi as a repair fallback (coding-harness-vcci),
  providers other than OpenCode Go (coding-harness-fqf9), the CI/verify split
  and dev/test/prod (coding-harness-7so beyond item 6), the agent dashboard
  candidates (coding-harness-326), TokenEconomizer (coding-harness-52pd), the
  class in every bead (coding-harness-680l). Each needs an interview first.

## Stop rules

- At 10 % of a five-hour window left, start no new large step; at about 5 %
  checkpoint and wait for the reset.
- Two failed repairs, a missing maintainer decision or an unresolved ambiguity
  stop that item; record the reason and go on with the next independent item.
  No question is asked overnight and no answer is invented.
- A leak-check BLOCK ends foreign calls without fallback.
- Tracker first, git second. The orchestrator is the only tracker writer; it
  writes a checkpoint comment on coding-harness-icw after each green step and
  only while no `make verify` runs.
- No force push, amend, bare stash, customer instance or secret read; the
  Artificial Analysis key is never read or printed.

## Morning page (08:00 Europe/Berlin)

One page: the phase-6 verdict for #158 and its decision block, the D-6
repair (bead coding-harness-dxso), pull requests awaiting the maintainer, where work
stopped and why, the CI slow-test measurement, and the time the morning
review took.
