---
title: "Spec — draft-gates-only"
status: draft
implementation_status: partial
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-77qj
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, verification]
class: bounded
appetite: 1
adr_files: []
---

# Spec — draft-gates-only

The draft verb checks its documents with the existing document gate subset,
leaving the full suite to implement, repair and the orchestrator (bead
`coding-harness-77qj`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

As researched on 2026-10-31 and checked at `119636d9`, `verify_draft` in
`scripts/stage2.py` runs `make verify` after derived-file preparation. It
therefore occupies a verification slot with code checks after a call whose
retained output is documents. The interview skip records the maintainer's
request for shorter draft cycles; it does not promise a measured speedup.

The merged gate subset already selects the document checks through
`bash scripts/verify_all.sh --job docs` (`decisions/gates.yaml`,
`scripts/ci_gates.py`, `tests/test_ci.py`). The draft caller does not use it.
The draft section of `docs/WORKFLOW.md` still describes the full check.

## Terms

**Document gates:** the existing `docs` subset of the `verify` job, selected
from `decisions/gates.yaml`; this change owns no separate gate list.

## Acceptance criteria

1. When a draft attempt reaches gate verification after put-back and
   derived-file preparation, it runs only the existing document gate subset.
   *Refuted by:* the draft invokes the full suite, runs a code gate such as
   pytest, or substitutes its own gate list for the existing subset.

2. When the draft runs its document checks, they retain machine-wide
   admission and the existing `VERIFY_SECONDS` execution limit.
   *Refuted by:* a check starts without admission, its child cannot re-enter
   the inherited admission, or queue time consumes the execution limit.

3. If the document check exits nonzero, cannot start, times out or is refused
   admission, the draft attempt fails with diagnostics identifying that
   check under the existing retry and commit rules.
   *Refuted by:* such a failure is accepted or committed as a passing draft,
   escapes the retry chain, or is reported as a failed `make verify` run.

4. When the document gates check ADR answers during a draft, only that
   change's own missing answer is tolerated through the existing gate-owned
   tolerance.
   *Refuted by:* another change's missing answer, a refused answer file or a
   different blocking gate is tolerated, or an owed answer is not reported.

5. When a draft is checked, the existing derived-file preparation and checks
   for spec, plan, plan card, Time used heading and new ADR count still apply.
   *Refuted by:* preparation is skipped or runs after the document gates, or
   an artifact failure formerly rejected by these checks is accepted.

6. When implement or repair reaches its post-run verification, it still runs
   the full `make verify` suite.
   *Refuted by:* either path selects the document subset or omits full
   verification because the draft already passed.

7. When a reader follows the draft section of `docs/WORKFLOW.md`, it names
   the document check and its exit code as the draft gate.
   *Refuted by:* that section still says draft runs `make verify`, or
   describes output parsing as the source of the gate verdict.

## Non-goals

- Changing subset membership, enforcement levels, CI jobs or `make verify`.
- Fixing the subset report header's full-job gate count; that reporting
  issue is separate work if needed, as recorded in `decisions.md`.
- Shortening the shared timeout, benchmarking a speedup, or changing
  admission, retry routing, put-back, credential checks or commit ownership.
- Changing the interview decision, adding an ADR, or adding a make target.
- Phase 2b does not run for this bounded change.

## Protected areas

- `decisions/gates.yaml`, `scripts/ci_gates.py`, `scripts/verify_all.sh`,
  `Makefile` and `.github/`: the existing subset and full verification
  mechanism are already decided and must remain intact.
- `prompts/`, `templates/`, `provenance.yaml`, `AGENTS.md`, endpoint and
  harness configuration: no policy or routing change is required.
- `docs/adr/` and `decisions/answers/`: this change creates no architecture
  decision and records no answer for the maintainer.

## Definition of Done

- `PYTHON=.venv/bin/python3 make verify` is green after implementation.
- The same pull request updates `scripts/stage2.py`, `tests/test_stage2.py`
  and `docs/WORKFLOW.md`, carries this spec, `plan.md` and review evidence in
  `findings.md`, and regenerates `plans/INDEX.md` through its renderer.
- The pull request's file list demonstrates that protected areas and
  non-goals were respected.
- The pull request closes the document-only draft verification work
  (`coding-harness-77qj`); its last commit carries
  `Closes-Bead: coding-harness-77qj`.
- Special runs: none; the existing subset tests and runner regression tests
  provide the evidence, without live model calls.

## Open decisions

None open. The bounded class and interview skip are already recorded in
`decisions.md`; no research swarm handoff applies.

[DETAIL] Use the existing shell runner directly, keep `VERIFY_SECONDS`, and
leave subset membership and report formatting alone, for the reasons already
recorded in `decisions.md`.

[DETAIL] Set a one-hour phase-4 appetite, repairs included: this is one caller
change with regression tests, and the limit stops expansion into the gate
mechanism.

[DETAIL] No `templates/plan.md` exists at `119636d9`; use the required card,
file steps, verification, criterion ledger and empty Time used section from
`prompts/03-plan.md`, as neighbouring bounded plans do.
