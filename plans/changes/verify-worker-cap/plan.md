---
title: "Plan — verify-worker-cap"
status: draft
implementation_status: partial
date: 2026-10-29
last_reviewed: 2026-10-29
updated: 2026-11-01
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

- 1: tests/test_ci.py::test_runner_derives_worker_default_from_machine_size — a captured gate value differs from independently stated CPU/memory fixtures on either platform
- 2: tests/test_ci.py::test_runner_preserves_explicit_worker_value — a non-empty caller value is overwritten or rejected
- 3: tests/test_ci.py::test_runner_defaults_empty_worker_value — empty and unset produce different defaults
- 4: tests/test_ci.py::test_runner_worker_detection_degrades_without_failure — partial readings produce the wrong bound or unusable probes fail a passing gate
- 5: tests/test_ci.py::test_runner_worker_default_preserves_gate_verdicts — inherited values, blocking/advisory status or later-gate execution differ
- 6: tests/test_ci.py::test_the_makefile_runs_what_the_one_list_runs — the canonical command and make test recipe diverge
- 6: not a test — phase-6 review compares the implementation diff with the protected paths and confirms no worker setting outside the local runner; any such edit refutes the boundary
- 7: not a test — review the paired full-run records against commit, commands, actual worker counts, outcomes and lock/isolation evidence; missing or mismatched evidence refutes the criterion

## Runner route — 2026-11-01

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-10-30 22:29:51–22:58:33 UTC, 1722 s — implement · attempt 1 · route flash · model glm-5.3-flash · accepted · measured by the runner
2026-10-31 15:36:27–16:03:54 UTC, 1648 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-10-31 16:04:06–17:00:11 UTC, 3365 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-10-31 17:00:17–18:31:52 UTC, 5494 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-10-31 19:08:22–19:36:24 UTC, 1681 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-10-31 19:36:37–20:06:41 UTC, 1804 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-10-31 20:06:49–21:39:29 UTC, 5560 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-10-31 21:49:36–22:39:28 UTC, 2992 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-10-31 22:39:35–2026-11-01 00:02:07 UTC, 4951 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-11-01 00:02:13–00:17:47 UTC, 934 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner

## Measured full runs — 2026-10-31

Recorded by the orchestrator (review rows L1-1 and L1-7). Both runs used the
commands of "Verification and boundaries" above, sequentially, at commit
`9236275e9f964bc56b6ce303c5eecf3f907c2f16`, on Darwin arm64 with 8 logical
CPUs and 8589934592 bytes (8 GiB) of physical memory.

| Workers | Start–end (UTC) | Wall time | Lock wait | pytest time | Outcome |
|---|---|---|---|---|---|
| 4 | 14:41:36–14:56:22 | 886.08 s | none (`[verify-lock] admitted`, memory 52 % free) | 710.73 s | 4411 passed, 17 skipped, 0 failed; second suite 104 passed; VERIFY GREEN |
| 8 | 14:56:22–15:34:54 | 2311.46 s | 1507 s (`[verify-lock] admitted after 1507s`, memory 57 % free) | 627.68 s | 4411 passed, 17 skipped, 0 failed; second suite 104 passed; VERIFY GREEN |

Isolation, stated plainly: the machine lock admitted each run alone, so no
second `make verify` overlapped a measured pytest span. The machine was not
otherwise idle: Codex and Pi runner calls of other lanes ran during both runs,
and the eight-worker run waited 1507 s for two of their verify runs to release
the lock. Its wall time is therefore not a measure of eight workers; the pytest times are 710.73 s and 627.68 s; one sample each proves no speedup (spec, non-goals). The actual
worker count was set by `PYTEST_XDIST_AUTO_NUM_WORKERS`; the quiet pytest
output does not print the started workers, so the count was not observed
separately. The logs stayed in the session scratchpad and are not committed.

Worker count, observed separately (review row L2-3), at `71b15fc6` on
2026-10-31 21:48 UTC: `PYTEST_XDIST_AUTO_NUM_WORKERS=4 python -m pytest
tests/test_ci.py -n auto` printed `created: 4/4 workers`, the same with `=8`
printed `created: 8/8 workers` (165 passed, 2 skipped each). The full runs
above use the same `-n auto` gate command and the same variable. Stated
plainly: step 4 also asks that no implement, repair or draft run during the
full runs; on 2026-10-31 four other lanes ran Codex and Pi calls meanwhile,
so the full runs are not isolated in that sense. A quiet-machine repeat is
owed before the numbers are used as a performance claim; whether to make it
before the merge is the maintainer's call.

## Quiet-machine runs — 2026-11-01

Recorded by the orchestrator (review rows L4-1, L4-2; the maintainer asked
for this repeat before the merge on 2026-10-31). Both runs at commit
`7074572438990a110bf11738eb99216095195ee4`, Darwin arm64, 8 logical CPUs,
8589934592 bytes of memory, sequentially. The script waited until no
`scripts/stage2.py`, `verify_all.sh` or `make verify` process was left
(09:50:47 to 10:50:52 UTC) and started no other job until both runs ended;
the maintainer's idle desktop apps stayed open. `PYTEST_ADDOPTS=-v` was set
only so that pytest prints its worker line; the gate command is unchanged.

| Workers | Command | Start–end (UTC) | Wall time | Lock | Workers started | pytest time | Outcome |
|---|---|---|---|---|---|---|---|
| 4 | `/usr/bin/time -p env PYTHON="$PWD/.venv/bin/python3" PYTEST_ADDOPTS=-v PYTEST_XDIST_AUTO_NUM_WORKERS=4 bash scripts/verify_all.sh` | 10:50:52–11:06:27 | 934.72 s | admitted at once | `created: 4/4 workers` | 751.57 s | 4421 passed, 17 skipped, 0 failed; 104 passed; VERIFY GREEN |
| 8 | the same with `=8` | 11:06:27–11:19:46 | 799.14 s | admitted at once | `created: 8/8 workers` | 613.89 s | 4421 passed, 17 skipped, 0 failed; 104 passed; VERIFY GREEN |

One sample each; the spec's non-goals keep this from being a speedup claim.

Appetite, stated plainly (review row L5-1): the recorded phase-4 spans sum to
30151 s (about 8.4 h; 1722 s implement, 28429 s for nine repair attempts),
against the spec's appetite, much of it waiting for the shared verify slot
while five lanes ran. The maintainer chose on 2026-11-01 about 11:35 UTC to
merge with the default of four workers; continuing past the stop was the
maintainer's call, and the runner stop at the appetite is bead
coding-harness-uxa9.

Trade-off, stated plainly (review row L5-2): on this machine the new default
(4) is slower than the old `-n auto` (8) on a quiet machine — pytest 751.57 s
against 613.89 s on 2026-11-01 — and keeps memory headroom for the other
lanes; whether the bounds may loosen is measured in bead coding-harness-351h.
