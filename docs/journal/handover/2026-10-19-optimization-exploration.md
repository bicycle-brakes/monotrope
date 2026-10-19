---
title: "Session handover — optimization exploration, as of 2026-10-19"
category: handover
created: 2026-10-19
updated: 2026-10-19
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: opencode
  version: "2026-10-19"
tags: [handover, session, optimization, verify, plans-lifecycle]
target_ref: 59630b7
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

This session explored only — no code, no tracker write, no gate change. It
answered one question the maintainer asked ("how can this repository be
optimised?") with measurements, and it found three things that are broken
independently of any optimisation:

1. **The nightly drift gate has been red for twenty consecutive nights.**
   Green on 2026-09-24 to 2026-09-29, then red every night from 2026-09-30 to
   2026-10-19 (GitHub run history, 2026-10-19). The findings are real and
   reproducible locally: 91 of them.
2. **The checkout's locked environment cannot run.** `.venv/bin/` has no
   interpreter (only pip, pytest and the activate scripts; state since
   2026-10-07), so `scripts/verify_all.sh` falls back to `python3` on PATH —
   which on this machine is another repository's virtualenv. The guard that
   exists for exactly this case checks only that PyYAML imports.
3. **The runtime work finished while this session ran.** PR #168
   (`perf/verify-xdist`) was merged at 2026-10-19 13:49; the pytest gate now
   runs `-n auto` (20:38 to 3:58, measured by that pull request).

The conversation also covered two questions that are **decisions, not work**:
whether this harness should expose parts of itself as an MCP server, and what
better uses exist than that. Both are recorded under "Open decisions" below.

## What was explored and measured

All numbers carry their cut-off date 2026-10-19, against `main` at `6477d04`
unless said otherwise.

| Area | Measurement | Where |
|---|---|---|
| Local `make verify` | about 24 minutes | this session, sequential run |
| `pytest` alone | 2285 tests, 20:38 | measured by the parallel session, idle machine |
| `pytest` with `-n 4` / `-n 8` | 4:57 / 5:47 and 8:09 | this session, **under load** — not comparable |
| Kit probe (`leerprobe`) | 163 s, runs its own pytest | this session |
| `plans-registry` | 2.3 s, 91 DRIFT findings | this session, exit 0 without `--strict` |
| Live changes | 21 directories, 106 artefacts, 26,836 lines, 3.8 MB | this session |
| Beads behind them | 16 closed, 1 in_progress, 1 open, 2 deferred, 1 without bead | tracker render, 2026-10-19 |
| Beads total | 139: 66 open, 9 in_progress, 62 closed, 2 deferred; 24 of the live ones P0/P1 | tracker render, 2026-10-19 |
| Handovers | 38 files, 7,071 lines, 428 KB; the last eight are night-run handovers | this session |
| Worktrees | 37 under `.claude/worktrees/`, 3.3 GB, 8 with branches already merged into main | this session |
| German residue | 156 of 12,554 lines in `scripts/`, 207 of 27,668 in `tests/`; 2 gate `reason` fields (`docs-links`, `ramp-valves`) | this session |
| Nightly drift | green 24.–29.09., red every night 30.09.–19.10. | GitHub run history, 2026-10-19 |

**On the parallel-run numbers:** the two `-n` runs this session took ran while
other sessions were working, and they collected 2,176 tests against the other
measurement's 2,994 on a different branch. They are reported for completeness
and for one finding that holds regardless of load: **two parallel runs produced
identical results** — no test order dependence, no serial test needed.

**On the 91 findings:** 83 artefact lines across 16 changes whose bead is
closed while the artefact still says `implementation_status: none` or
`partial` ("The tracker says finished, the artefact contradicts"), plus 8
beads that are `in_progress` with no artefact at all. The per-pull-request
gate `plans-registry` measures the same rule but classifies it DRIFT, and
`Verdict.exit_code()` returns 0 for DRIFT without `--strict` — by design,
because the tracker moves without a commit here. The strict variant exists
only as `plans-registry-strict` in the nightly drift job.

## What must be done

Ordered by cost-to-benefit, not by size.

### Immediately — mechanical, high effect

1. **The night gate must stop being noise.** Twenty red nights is not a gate.
   Three parts: (a) make `make staleness` strict, or surface the DRIFT count
   where work happens — today only the nightly CI log shows it; (b) archive the
   16 changes whose beads are closed, deciding per change what belongs into a
   living spec under `plans/specs/` and what into an ADR; (c) kill the cause:
   add "bead closed means the change is archived" as a step in the phase-7
   prompt (`prompts/07-commit.md`), so closing a bead without archiving stops
   being possible to forget.
2. **Repair the locked environment.** `.venv/bin/` has no interpreter, so no
   local before/after measurement on this machine runs on the pinned
   interpreter, and `test_the_environment_matches_the_lock` is red (markupsafe
   3.0.3 against the locked 3.0.4, pydantic 2.10.6 against 2.13.5). One
   `make venv` run, then re-measure.
3. **Install the pinned Pi** (`bash tools/pi/install.sh`). Without
   `tools/pi/node_modules` the pytest gate is red for environmental reasons —
   10 errors in `tests/test_pi_contract.py`. A control run without xdist
   produced the identical errors, so this is not a parallelism problem. The
   topic of bead coding-harness-omp.
4. **Confirm the merged state.** PR #168 landed at 13:49; one clean
   `make verify` on a repaired environment should land near 8 minutes instead
   of 24. That number is not yet measured on this machine.

### This week — stage 2 and the runtime remainder

1. **Stage 2 that can be trusted** (roadmap "Now" 3): nine P1 beads are open or
   in progress — coding-harness-znc (a failed attempt's work is deleted, not
   saved), coding-harness-8hr (failed-check diagnostics copy test secrets into
   a finding), coding-harness-0ho (red-first exception for test-only fixes),
   coding-harness-83e, coding-harness-csm, coding-harness-6ie,
   coding-harness-6jg, coding-harness-s9r, coding-harness-fdz. This is the
   largest open risk bundle in the tracker.
2. **The runtime remainder after parallelism.** About 100 `test_stage2.py`
   tests cost 4–8 s each (git subprocesses) — no parallelism fixes that, only
   fewer subprocesses per test. The kit probe costs 163 s and does not use
   `-n`; it is the second-largest gate now.

### Structural — the optimisation levers

1. **The change lifecycle leaks.** 21 live changes, 16 of them finished. The
   rule that would archive them keys on `implementation_status: done`, which
   nobody sets when a bead closes. Once the night-gate item above is worked,
   decide whether a cap belongs here: the roadmap caps its themes at three
   "Now", nothing caps the number of live changes, and each one costs 5–6
   artefacts with full frontmatter.
2. **Two manifests answer one question.** `scripts/kit/manifest.yaml`
   classifies roles (mechanism/bestand), `scripts/export/manifest.yaml`
   decides what travels per prefix — and a test asserts that neither is
   derivable from the other. Two lists to one question is the drift pattern
   `decisions/gates.yaml` exists against (D-10). One classification with two
   projections would remove the duplication without losing either answer.
3. **German residue** (bead coding-harness-yim, roadmap "Next"): the two gate
   `reason` fields first, then `docs/governance/regelwerk.md` and
   `quality-gates.md`. Small, visible, gate-near.
4. **Bead coding-harness-bt8** (P2, open since 2026-09-17, untouched): 35
   corpus findings. Until it is worked, `docs-links` stays at `report` and
   reports without blocking.
5. **37 worktrees, 3.3 GB**, 8 of them with branches already merged into
   main. AGENTS.md asks for removal after the merge; these are leftovers.

## Open decisions — the maintainer's, not work items

1. **MCP.** This repository documents "no MCP server today" (WORKFLOW.md § 8,
    the `.mcp.json` row). A read-only slice — gates, phase prompts, templates
    and tracker reads through the existing access points — would cost 1–2 days
    and would turn house rule 4 ("one writer per tracker", stated but not
    enforced until the D-60 guard exists) into a capability boundary. Reversing
    § 8 is a decision pull request under house rule 8.
2. **Bead coding-harness-i0l** ("reconcile repository state with
   WORKFLOW.md"): several findings of this session belong there — the § 8
   statement, the DRIFT-does-not-block semantics, and the broken environment.

## Unfinished and blocked

- Nothing of this session is half-done: it was read-only by instruction.
- The 91 drift findings are **not** cleaned here. That is the night-gate item,
  part b, and needs a decision per change (living spec, ADR, or archive), not
  a bulk move.
- My `-n 4` / `-n 8` numbers are load artefacts; do not quote them as the
  effect of parallelism. The merged PR #168 measured 3:58 on an idle machine.

## Branch, commit, pull request

This handover travels as its own pull request from
`docs/handover-2026-10-19-optimization-exploration`, branched from
`origin/main` at `59630b7` (which already contains PR #168). **It opens,
changes and closes no bead** — the tracker belongs to the first writing
session in this checkout (house rule 4), and this session wrote nothing to it.

## Parallel sessions

- Bead coding-harness-d5a and PR #168 (now merged) owned the runtime work;
  the worktree `verify-xdist` was created for it at 14:59.
- PR #158 (`explore/research-swarm`, ADR 0020) was open and in progress.
- A second session ran the test suite in this checkout while this session
  measured; that is the reason the parallel-run numbers above are marked as
  load artefacts.

## Next step

The night-gate item, parts a and b together: switch `make staleness` to the
strict call, then work the 16 changes whose beads are closed — for each one
decide living spec, ADR, or plain archive. That is the only item that is both
mechanical and removes twenty nights of red.
