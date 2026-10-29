---
title: "Plan — verify-worker-cap"
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
produced_by: {kind: llm-session, name: codex, version: "2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, verification]
---

# Plan — verify-worker-cap

```text
For you:     Local verification chooses a smaller worker default from CPU and memory; your explicit worker value wins.
Done when:   Default, override and detection-failure tests pass, isolated four/eight-worker runs are recorded, and make verify is green.
Appetite:    2 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Test-speed optimisation, hosted CI or make test changes, machine locking, or Stage-2 environment forwarding.
Pre-mortem:  suppose it failed: most likely because a failed machine probe breaks verification instead of leaving a usable fallback.
Starts unless you say stop.
```

Baseline `c67a94ca`, inspected 2026-10-29. Implements `spec.md` and the
existing reasoned interview skip. Bounded: no design or ADR. There is no
`templates/plan.md`; this follows `prompts/03-plan.md`. Explore used Stage 2,
GLM 5.3 Flash through `glm-coding-plan`; no Stage-1 fallback is recorded.

## Files and steps

1. In `tests/test_ci.py`, extend the temporary runner-tree harness with controlled resource commands on PATH and a gate that reports the inherited environment. Simulate macOS (`uname`, `sysctl -n hw.logicalcpu`, `sysctl -n hw.memsize`) and Linux (`uname`, `nproc`, `awk` reading `MemTotal` from `/proc/meminfo`, in KiB); fake tool outputs so tests do not depend on the host. Cover 8 cores/8 GiB → 4, 16/4 → 2, odd cores rounded down, and one core or less than 2 GiB → 1. Prove the new default regression red against the unchanged script before editing it.
2. In `scripts/verify_all.sh`, add a small default-selection block after argument handling/list-only exit and before gates execute. Preserve any non-empty exported `PYTEST_XDIST_AUTO_NUM_WORKERS` verbatim; otherwise read the platform's resources with the standard commands above, ignoring failures and validating positive decimal integers before arithmetic. CPU bound is `max(1, cores / 2)`, memory bound is `max(1, bytes / 2147483648)`; use the minimum of available bounds, export it, or unset the variable when neither is valid. Keep Bash 3.2 compatibility, the interpreter choice, gate list and gate loop unchanged; no new script or dependency.
3. Complete the same test file with unset/empty parity, explicit `8` and arbitrary non-empty pass-through, CPU-only/memory-only/neither-readable cases, missing commands, malformed/zero/negative readings, and a synthetic multi-gate run proving environment propagation and existing block/advisory/continue behavior. Clear inherited worker settings in default tests. Replace each implemented ledger entry's `not yet written` marker in this plan.
4. After the separate machine-lock change is available, acquire its verification slot through the orchestrating session and perform both full runs below on identical code/tests with the pinned environment; do not start implement, repair, draft, a kit probe or other local verification concurrently. Confirm actual worker counts in pytest output; a failed or overlapping measurement is void. Record commit, date, platform, logical cores, physical memory, exact command, wall time, pytest pass/skip/failure counts and lock/isolation evidence here, outside the initially empty time section if measurement tables are needed. Do not claim a speedup from one sample per count.
5. Update only `plans/changes/verify-worker-cap/spec.md`, `plans/changes/verify-worker-cap/plan.md` and, for review/evidence, `plans/changes/verify-worker-cap/findings.md` as implementation progresses. Record measured phase-4 spans under Time used. Stop at the appetite; if the lock prerequisite is unavailable, report that blocker rather than substitute overlapping measurements.

## Verification and boundaries

Focused command:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 -m pytest tests/test_ci.py -q
```

Full gate command:

```bash
make verify
```

Within the verification slot, run these sequentially; `make verify` invokes
the same script. Explicit values avoid any dependency on host auto-detection:

```bash
/usr/bin/time -p env PYTHON="$PWD/.venv/bin/python3" PYTEST_XDIST_AUTO_NUM_WORKERS=4 bash scripts/verify_all.sh
/usr/bin/time -p env PYTHON="$PWD/.venv/bin/python3" PYTEST_XDIST_AUTO_NUM_WORKERS=8 bash scripts/verify_all.sh
```

Do not change `decisions/gates.yaml`, `.github/workflows/ci.yml`, `Makefile`,
`docs/governance/gate-catalog.md`, `scripts/stage2.py`, dependencies, unrelated
tests or the machine-lock implementation. Existing command-consistency tests
remain in place. Compare the implementation diff with the declared files;
the cap only covers invocations through `verify_all.sh`.

## Criterion ledger

- 1: not yet written tests/test_ci.py::test_runner_derives_worker_default_from_machine_size — a captured gate value differs from independently stated CPU/memory fixtures on either platform
- 2: not yet written tests/test_ci.py::test_runner_preserves_explicit_worker_value — a non-empty caller value is overwritten or rejected
- 3: not yet written tests/test_ci.py::test_runner_defaults_empty_worker_value — empty and unset produce different defaults
- 4: not yet written tests/test_ci.py::test_runner_worker_detection_degrades_without_failure — partial readings produce the wrong bound or unusable probes fail a passing gate
- 5: not yet written tests/test_ci.py::test_runner_worker_default_preserves_gate_verdicts — inherited values, blocking/advisory status or later-gate execution differ
- 6: tests/test_ci.py::test_the_makefile_runs_what_the_one_list_runs — the canonical command and make test recipe diverge
- 6: not a test — phase-6 review compares the implementation diff with the protected paths and confirms no worker setting outside the local runner; any such edit refutes the boundary
- 7: not a test — review the paired full-run records against commit, commands, actual worker counts, outcomes and lock/isolation evidence; missing or mismatched evidence refutes the criterion

## Time used
