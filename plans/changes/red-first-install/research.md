---
title: "Research — red-first-install"
status: draft
implementation_status: none
date: 2026-10-16
last_reviewed: 2026-10-16
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-omp
class: bounded
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, red-first]
---

# A missing Pi install counts as red in the red-first check — Research

Phase 1 for bead coding-harness-omp, seeded by the orchestrating session on
2026-10-16 against `origin/main` at `6029bbf`.

## The question

The phase-6 round-2 review of the pi-pin change (2026-10-15) found that
`red_first` in `scripts/stage2.py` checks out the baseline with
`git worktree add`. That checkout has no `tools/pi/node_modules` (ignored by
git), so `require_installed_pi` fails the real-Pi tests with exit 1, and the
check counts that as red. Measured then in a scratch copy:
`test_real_opencode_provider_contracts` ends in ERROR with pytest exit 1 when
`node_modules` is absent. Effect: test-only repairs of real-Pi tests that pass
on the baseline code pass red-first without any real red run. Needed (bead
text): the baseline check must see the pinned install, or count only an
assertion failure as red, with a test that a missing install is not red.

## Known so far (read, not run)

- Related beads: coding-harness-0ho (red-first exception for test-only fixes,
  in phase 4 on `explore/guard-test` since 2026-10-16, which also changes the
  red-first path) and coding-harness-y17 (test-strength findings have no
  red-first form).
- `tools/pi/install.sh` installs the pinned Pi into `tools/pi/node_modules`
  (ADR 0019); the runner's scratch checkouts do not run it.

## To explore

1. Where `red_first` builds the baseline checkout, how it runs the tests there
   and how it decides red versus green (exit code, outcome parsing).
2. Which other ignored files a baseline checkout misses that tests need
   (`.venv`, generated files, `node_modules`), and how other runner checkouts
   (draft, implement attempts) provide them.
3. The two fix directions: give the baseline the pinned install (link or copy
   the main worktree's `node_modules`, or run `install.sh`) versus classify
   outcomes so only a failed assertion is red (setup errors, skips and
   collection errors are not). Which is smaller and which is safer.
4. How the change must coordinate with 0ho's red-first changes on
   `explore/guard-test` to avoid a conflict in the same function.
5. Which tests cover `red_first` today, so a test with a missing install can
   follow them.
