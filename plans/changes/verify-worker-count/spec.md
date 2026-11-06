---
title: "Spec — verify-worker-count"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-xay1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, spike, verify, measurement]
class: spike
appetite: 4
adr_files: []
neighbours: []
---

# Spec — `verify-worker-count`

The goal is to establish the actually started pytest-xdist worker count in at
least five local verification runs and append the evidence to the existing
baseline (bead coding-harness-xay1 — observed verification worker counts).
Research: `research.md`. Scope: `decisions.md`, the reasoned interview skip.

## Problem

The five runs on revision `bc2fe411`, dated 2026-11-05, record a configured
worker setting of four, but their retained quiet pytest output does not show
how many workers actually started. The baseline explicitly names that gap;
the verification-duration review deferred it to this spike (research.md,
"Where the count is and is not observable"; decisions.md, interview skip).
An environment setting alone cannot close this evidence gap.

## Terms

**Actual worker count:** the workers whose startup pytest-xdist reports for
the full suite's pytest gate in that run, distinct from its configured setting
and from any pytest invocation inside another gate.

## Acceptance criteria

1. When a run is counted toward this spike, its full-suite pytest output supplies a directly observed worker-startup count.
   *Refuted by:* its only worker evidence is an environment value, a CPU count, another gate's output, or output without a startup count.

2. When the spike is complete, its evidence includes at least five serial, completed, green, full local verification runs on one clean revision through ordinary machine-wide admission.
   *Refuted by:* fewer than five qualifying runs, a dirty or different revision among them, a partial job, an admission bypass, or an incomplete or failed run counted as qualifying.

3. When the results are published, a dated addendum to `docs/research/2026-11-04-verify-duration-baseline.md` preserves the existing baseline and binds each new run's observed count and quoted startup line to its date, revision, exact command, retained output reference and final verdict.
   *Refuted by:* an old row is overwritten, a new count lacks a traceable run and startup line, or a retrospective count is assigned to one of the five original runs.

4. When the addendum concludes, it states what the new observations establish about actual versus configured workers and the limits of that conclusion.
   *Refuted by:* it equates the configured value with observation, leaves the worker-count question unanswered, or claims a faster configuration or a hosted-runner result from these local samples.

## Non-goals

- Changing worker sizing, comparing four against eight workers, measuring peak memory, or loosening the cap; these remain separate work.
- Forwarding worker settings through the Stage-2 runner or measuring hosted CI.
- Adding permanent instrumentation, a history field, a plugin, or a new gate; the recorded decision permits a baseline option that prints the count.
- Re-running the original revision to fill its historical rows or revising the warning-budget proposal from this sample.
- Phase 2b design and an ADR: this is a measurement spike, with no architecture change.

## Protected areas

Executable code and tests, including `scripts/verify_all.sh`,
`scripts/verify_duration.py`, `scripts/verify_lock.py`, `scripts/stage2.py`,
`tests/`, `Makefile` and `pyproject.toml`, remain untouched because the chosen
measurement route uses existing output options. Gate definitions,
`.github/`, instructions, prompts, templates, configuration and all other
runner-held paths remain untouched; neither admission nor enforcement changes.

## Definition of Done

- All four criteria have evidence; five qualifying `make verify` runs are green.
- The dated addendum is in `docs/research/2026-11-04-verify-duration-baseline.md`; no ADR or model changes.
- The pull request's file list respects the protected areas and non-goals.
- The pull request closes the observed-worker-count task (coding-harness-xay1), with final trailer `Closes-Bead: coding-harness-xay1`.
- Special runs: the five measurements, each identified by revision and date in the addendum and referenced in the pull request body.

## Open decisions

None open.

- [DETAIL] Use pytest verbosity for these baseline runs, because research.md records an earlier successful observation with `PYTEST_ADDOPTS=-v`; this avoids permanent runtime changes.
- [DETAIL] Use five new runs and preserve the original rows, because the original quiet output cannot establish the missing historical fact.
- [DETAIL] Set a four-hour phase-4 appetite, including measurement and write-up, because the prior baseline took about twenty minutes of execution per run and admission wait must fit too; this is a stop, not an estimate.
