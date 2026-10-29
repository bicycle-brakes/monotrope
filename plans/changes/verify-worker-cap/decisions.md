---
title: "Decisions — verify-worker-cap"
status: draft
implementation_status: none
date: 2026-10-29
last_reviewed: 2026-10-29
updated: 2026-10-29
supersedes: null
superseded_by: null
bead: coding-harness-l7sc
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview]
---

# verify-worker-cap — Decisions

Class: bounded (one counted interview record or a reasoned skip owed; a
reasoned skip below). Reason for the class: the change adds one default to
`scripts/verify_all.sh` and its tests; the gate command, CI and the Makefile
stay as they are, so no gate, ADR or doctrine text changes.

## SKIP · interview

status: skipped
reason: the bead (coding-harness-l7sc) states the remedy in full — `scripts/verify_all.sh` exports PYTEST_XDIST_AUTO_NUM_WORKERS when the caller has not set it, derived from the machine (about half the cores, bounded by memory; 4 on the 8-core, 8 GB Mac), an explicit caller value wins, gate command, CI and Makefile unchanged, a 4-versus-8 worker measurement in isolation — and the maintainer decided on 2026-10-29 that it is its own bead in lane A after coding-harness-p6mu; no question remains open that only the maintainer can answer.

## Details for the draft

[DETAIL] **One string everywhere stays.** The cap is an environment default
set inside `verify_all.sh`, not a change of `-n auto`; so
`decisions/gates.yaml`, `.github/workflows/ci.yml`, the `Makefile` and
`docs/governance/gate-catalog.md` keep their pinned command. Reason: the
research names four pins held by tests (`tests/test_ci.py`,
`tests/test_gate_catalog.py`, the `ci-drift` gate); the bead keeps them.

[DETAIL] **The caller wins, including an empty value is not a value.** An
already exported, non-empty PYTEST_XDIST_AUTO_NUM_WORKERS is passed through
unchanged; unset or empty gets the derived default. Reason: the bead says an
explicit value wins; an empty string is not a worker count.

[DETAIL] **The derivation is deterministic and testable.** Half the logical
cores, at least 1, and at most one worker per 2 GB of physical memory, read
with standard tools (`sysctl` on macOS, `nproc` and `/proc/meminfo` on
Linux); when neither can be read, the variable stays unset and xdist's own
`auto` applies. Reason: 8 cores and 8 GB give 4, as the bead names; a
machine whose size cannot be read must not fail verify.

[DETAIL] **The runner's env allow list is not widened.** The default is set
inside `verify_all.sh`, which every runner-started verify runs, so the
`stage2.py` ENV_ALLOW drop no longer matters for the default. Reason: only
lane A changes `scripts/stage2.py` tonight, and the bead names one place.

[DETAIL] **Measurement: one isolated full run each with 4 and 8 workers,**
under the verify lock, recorded with commit and date in `plan.md`'s time
section. Reason: the bead asks for it; one run each is what it names.
