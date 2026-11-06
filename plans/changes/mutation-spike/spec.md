---
title: "Spec — mutation-spike"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-bvy
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, spike, mutation-testing]
class: spike
appetite: 2
adr_files: []
neighbours: []
---

# Spec — mutation-spike

Measure how well existing tests detect generated faults in two Python scripts,
and leave a reproducible, bounded calibration for the maintainer to assess
(bead coding-harness-bvy). Research: `research.md`. Decisions: `decisions.md`.

## Problem

The repository checks for named planted-fault evidence but has no measured
mutation score for its scripts. The research, read at `761e61a6` on 2026-11-06,
quotes `docs/testing.md`: real mutation testing is planned, not built. Counting
tests or recognising their names does not measure which generated faults they
miss (`research.md`, “What exists today”).

The original assignment asks for a dated measurement with tool/version,
revision, score, survivor kinds and runtime in a scratch environment, within
two hours (`docs/research/2026-10-20-night-run-plan.md`, reserve item 6).
The later interview skip fixes both targets as
`scripts/check_research_handoff.py` and `scripts/stage2_availability.py`, and
excludes adding anything to `make verify` before a maintainer decision
(`decisions.md`, “SKIP · interview”, 2026-11-06). This resolves the older
research's uncertainty about the second target.

## Terms

- **Mutant:** one tool-generated source variation, measured against the stated
  existing test selection; mutations of imported helpers are outside the target.
- **Killed / survived:** a valid mutant is detected / not detected by that
  selection. Timeouts, invalid mutants and untested mutants remain distinct.
- **Score:** a fraction with its counts, denominator and exclusions stated;
  a sampled or interrupted run describes only the evaluated subset.

## Acceptance criteria

1. When the spike ends, one dated note under `docs/research/` accounts for both
   named targets, with a completed or explicitly incomplete measurement status.
   *Refuted by:* either target is absent, or an unfinished run is called complete.

2. When a measurement is reported, its setup identifies the source commit,
   measurement date, Python and mutation-tool versions, exact commands,
   mutation scope, test selection and relevant configuration.
   *Refuted by:* a reader cannot identify the measured source or reproduce the
   stated setup without guessing a version, command or scope.

3. When mutants are evaluated for a target, the same selected tests pass first
   against its unmutated source in the measurement environment.
   *Refuted by:* a failing or unrecorded baseline supplies a claimed valid score.

4. When a score is reported for a target, it is reconstructible from separately
   reported killed, survived, timed-out, invalid and untested counts and an
   explicit denominator and exclusion policy.
   *Refuted by:* the arithmetic cannot be reproduced, an error is counted as a
   kill, or a subset score is presented as a whole-script result.

5. When surviving mutants exist, the note groups them by fault kind with counts
   and source locations or mutant identifiers, distinguishing observed test gaps
   from suspected equivalent mutations and unreviewed survivors.
   *Refuted by:* survivor totals cannot be reconciled, survivors are merely
   listed without kinds, or a suspected equivalent mutant is silently discarded.

6. When the run ends or stops, the note records baseline and mutation elapsed
   time per target, total phase-4 time, and any interruption or tool limitation.
   *Refuted by:* runtime is missing, setup time disappears from the appetite,
   or interrupted work is indistinguishable from completed work.

7. While the spike runs, measurements stay within two hours of phase-4 work,
   including setup and reporting, with remaining coverage explicitly unmeasured
   when the budget is exhausted.
   *Refuted by:* work continues beyond the appetite or missing coverage is
   replaced by an estimated result presented as measured.

8. When the note recommends a next step, it ties that recommendation to the
   measured evidence and its limits without changing the verification policy.
   *Refuted by:* the recommendation generalises beyond the measured selection
   without qualification, or the change introduces a score threshold or gate.

## Non-goals

- Repairing survivors, strengthening tests or changing either target's behaviour.
- Measuring other scripts, including `scripts/research_handoff.py`, or claiming
  a repository-wide test-quality score.
- A recurring mutation service, CI integration, a minimum score, or a new gate.
- Changing the existing named planted-fault evidence rule or evaluating its
  precision and recall.
- Installing mutation dependencies into the repository's dependency lock.
- Phase 2b design and an ADR: this class is `spike`, with no architecture change.

## Protected areas

`scripts/` and `tests/` are measurement inputs, unchanged in the submitted tree;
generated mutations belong only in disposable copies. `pyproject.toml`,
`requirements-ci.txt`, `Makefile`, `decisions/gates.yaml`, `.github/`, prompts,
templates, endpoint declarations and governance stay unchanged because this
spike measures existing behaviour rather than adopting a new practice.

## Definition of Done

- The dated note `docs/research/2026-11-06-mutation-testing-baseline.md` holds
  the criteria above; incomplete coverage remains labelled, with its reason.
- CI is green for this text-only change; no new local `make verify` step is
  introduced. The runner performs its required post-run checks.
- The pull request file list shows protected areas unchanged and no scratch
  environment, mutant cache or raw temporary logs committed.
- The pull request names the mutation-measurement bead and its final commit
  carries `Closes-Bead: coding-harness-bvy` only when the orchestrator accepts
  the evidence as satisfying the assignment; drafting does not close it.
- Special run evidence: the baseline and mutation commands, results and measured
  source commit are recorded in the note and summarised in the pull request.

## Open decisions

None open.

- [DETAIL] Use a dated baseline note at the path above so the measurement has
  one reviewable home; its actual run date is stated even if reporting is later.
- [DETAIL] Start with mutmut in a disposable environment; record the installed
  version and any incompatibility rather than pinning a repository dependency.
  Tool configuration and bounded sampling are reversible measurement details.
- [DETAIL] Report partial or failed measurements honestly at the two-hour stop;
  an incomplete run is evidence about feasibility, not a fabricated score.
  Record whether broader measurement is needed before adopting any practice.
- [DETAIL] `neighbours: []` records no confirmed neighbour set: this exploration
  was a single Flash run, not a complete research swarm with a binding handoff.
