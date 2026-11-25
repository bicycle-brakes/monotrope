---
title: "Plan — test-ci-shared-tree"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.12
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, tests, xdist]
---

# Plan — test-ci-shared-tree

```text
For you:     Parallel tests no longer see the orphan file made by the control test.
Done when:   Isolation and orphan-detection regressions and make verify pass.
Appetite:    One hour of phase 4 including repairs; stop at the limit.
Not now:     Work-stealing scheduling and a parallel kit probe.
Pre-mortem:  suppose it failed: most likely because the control test no longer exercises the real glob.
Starts unless you say stop.
```

## Build sequence

1. In `tests/test_ci.py`, let `_scripts()` accept a root while preserving `REPO_ROOT` as its default; create a temporary `scripts/` directory with an actual uncalled `.sh` file in the existing control test, and pass that root through the same glob and `_heimatlose_namen` classification. Keep the test name and its use of the real caller lists, and update its docstring.
2. In `tests/test_ci.py`, add a regression that runs the control test with an isolated temporary root while observing file creation, and fails on any write inside the checkout; add a regression checking the default glob against a controlled checkout root, including both `.py` and `.sh` and the existing `test_` exclusion. Demonstrate that removing `.sh` from the glob and bypassing orphan classification make the control test fail.
3. Update `plans/changes/test-ci-shared-tree/plan.md` ledger markers when the new tests exist. The runner owns call evidence in `plans/changes/test-ci-shared-tree/findings.md` and regeneration of `plans/INDEX.md`.

No files are deleted. Leave `scripts/kit/probe.py`, CI configuration, scheduler and tracker untouched. No held path is assigned to the implementation attempt. This bounded change needs no design or ADR; no phase-2a rows were present on 2026-11-25.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_ci.py
make verify
```

## Criterion ledger

- 1: not yet written tests/test_ci.py::test_orphan_control_does_not_write_to_checkout — the control test writes its orphan under the checkout.
- 2: tests/test_ci.py::test_the_glob_itself_finds_a_real_orphan_shell_script — the glob omits `.sh` or classification fails to report the orphan.
- 3: not yet written tests/test_ci.py::test_scripts_defaults_to_checkout_inventory — the default glob reads another root or omits a qualifying script.

## Explore route

On 2026-11-25, Explore used the Stage-1 route with `claude-haiku-5-5` because GLM 5.3 Flash through Z.ai had reached its weekly limit, as recorded in `research.md`.

## Time used

2026-11-25 00:51:01–00:53:03 UTC, 122 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
