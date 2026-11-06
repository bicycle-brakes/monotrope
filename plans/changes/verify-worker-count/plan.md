---
title: "Plan — verify-worker-count"
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
tags: [plan, spike, verify, measurement]
---

# Plan — `verify-worker-count`

```text
For you:     You can see how many pytest workers actually started in each new baseline run.
Done when:   At least five green full runs have quoted startup counts in a dated baseline addendum.
Appetite:    4 hours of phase 4, including measurement and write-up; stop at the limit.
Not now:     Worker sizing, peak memory, hosted CI, runner forwarding or permanent instrumentation.
Pre-mortem:  suppose it failed: most likely because configured workers were mistaken for observed workers.
Starts unless you say stop.
```

## Files and steps

1. Use the locked worktree environment and pinned Pi already required for verification. After the draft is committed by the runner, record the full revision (`git rev-parse HEAD`), clean-tree check (`git status --porcelain`), UTC date, platform, logical CPUs, physical memory and ambient workload. Do not edit tracked files between samples.
2. Run the command below five times serially, through the harness's background-job mode, one job per call; retain each job's complete stdout/stderr and exit status, checking revision and cleanliness before and after each sample. Leave the machine-wide admission state and lock markers unchanged. Clear an inherited worker override so the existing local default applies; verbosity is a measurement-only option. Identify the full-suite `pytest` gate, distinct from the ruleset gate's pytest invocation. Quote its `created: N/N workers` startup line (or an equally explicit xdist startup summary), final test summary, gate result and `VERIFY GREEN` verdict for each sample. If output lacks an actual count, keep it as excluded evidence and stop rather than infer a number or add runtime code. Failed or incomplete samples do not count; disclose them and stop for diagnosis outside this spike.
3. Change `docs/research/2026-11-04-verify-duration-baseline.md`: append a dated methodology, per-run evidence table and startup excerpts without rewriting the original content. Each row identifies its retained job output, revision, UTC start/end, exact command, configured setting (unknown when unread), observed workers, pytest pass/skip/failure totals, verdict, execution seconds and admission wait separately. State background workload and comparability limits; conclude what was observed without a sizing or speed recommendation. Update the header's `updated` and `last_reviewed` dates.
4. Update `plans/changes/verify-worker-count/spec.md` and `plans/changes/verify-worker-count/plan.md` with truthful implementation status and evidence; record phase-4 spans under Time used only after work occurs. Update `plans/changes/verify-worker-count/findings.md` only with review findings/evidence. No file is deleted; no design or ADR file is created. The orchestrator regenerates derived `plans/INDEX.md` after header changes and owns commit/PR operations; no held-path edit is needed.

## Verification and boundaries

Measurement and verification command, unchanged for each sample (the environment option supplies worker visibility without changing the gate command):

```bash
env -u PYTEST_XDIST_AUTO_NUM_WORKERS PYTEST_ADDOPTS='-v --durations=30' PYTHON=.venv/bin/python3 make verify
```

Retain the selected interpreter/dependency versions and exact command with the sample set. No code, dependencies, tests, gate definitions, lock configuration, hosted workflow or prior measurement rows change. Document-only edits after the samples use the document gates under repository rules; the five measurement runs themselves supply full verification evidence. Exploration used Stage 2, GLM 5.3 Flash, on 2026-11-06; no Stage-1 fallback was recorded. Phase 2b does not run for a spike.

The criteria concern empirical observations and document review; a unit test cannot establish how many workers these real runs started.

## Criterion ledger

- 1: not a test — review each retained full-suite pytest startup line against its addendum count; a setting-only count or a line from another gate refutes it.
- 2: not a test — review five distinct job outputs, exit statuses, clean revision checks and admission evidence; a missing, failed, partial, bypassed or different-revision sample refutes it.
- 3: not a test — compare the addendum with retained outputs and the pre-change baseline; a changed historical row or an untraceable new count refutes it.
- 4: not a test — review the conclusion against the five observations and stated limits; configured-as-observed, unsupported speed or hosted claims refute it.

## Time used

2026-11-06 03:32:16–04:38:18 UTC, 3961 s — implement · attempt 1 · route flash · model glm-5.3-flash · accepted · measured by the runner
