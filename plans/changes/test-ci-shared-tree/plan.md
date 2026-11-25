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

1. In `tests/test_ci.py`, parameterize `_scripts()` with a repository root defaulting to `REPO_ROOT`; retain its non-recursive inventory. Keep the control test's name, create its orphan under `tmp_path`, call the real glob and classification, and read the real `CI_FILE`, `RUNNER` and `OHNE_AUFRUFER` in place.
2. In `tests/test_ci.py`, add a spy checking the classification inputs. Add a write watcher for `Path.write_text`, `Path.write_bytes`, write-mode built-in and `io.open`, write/create-flagged `os.open`, `os.replace`, `os.rename`, `Path.touch` and `Path.mkdir`; reject targets anywhere in the checkout, including removed files and temporary directories. Prove detection with a planted write under a `tmp_path` stand-in; assert its target is inside that stand-in and outside the checkout before running it. Native writes outside Python file APIs remain a test limit.
3. In `tests/test_ci.py`, make both inventory tests assert their default inventory is non-empty; test that each rejects an empty inventory. Test the default glob against a controlled root containing top-level `.py`, `.sh`, `test_` and nested files, and demonstrate that dropping `.sh` or bypassing orphan classification turns the control test red.
4. Update the ledger in `plans/changes/test-ci-shared-tree/plan.md` when the new tests exist. The runner owns call evidence in `plans/changes/test-ci-shared-tree/findings.md` and regeneration of `plans/INDEX.md`.

No files are deleted. Leave `scripts/kit/probe.py`, CI configuration, scheduler, `test_an_orphan_shell_script_gets_flagged` and tracker untouched. No held path is assigned to the implementation attempt. This bounded change needs no design or ADR.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_ci.py
make verify
```

## Criterion ledger

- 1: tests/test_ci.py::test_orphan_control_does_not_write_to_checkout — an attempted checkout write goes undetected.
- 2: tests/test_ci.py::test_the_glob_itself_finds_a_real_orphan_shell_script — the glob omits `.sh` or classification fails to report the orphan.
- 3: tests/test_ci.py::test_scripts_defaults_to_checkout_inventory — the default glob reads another root or includes the wrong files.
- 4: tests/test_ci.py::test_inventory_checks_reject_empty_inventory — either inventory check passes with an empty list.
- 5: tests/test_ci.py::test_orphan_control_does_not_write_to_checkout — a write that is later removed goes undetected.
- 6: tests/test_ci.py::test_orphan_write_watcher_detects_standin_write — the watcher misses a planted write in a temporary stand-in.
- 7: tests/test_ci.py::test_orphan_write_watcher_detects_standin_write — a target outside the stand-in or inside the checkout is accepted.
- 8: tests/test_ci.py::test_orphan_control_uses_real_caller_inputs — substituted caller inputs pass the spy check.

## Explore route

On 2026-11-25, Explore used the Stage-1 route with `claude-haiku-5-5` because GLM 5.3 Flash through Z.ai had reached its weekly limit, as recorded in `research.md`.

## Runner route — 2026-11-25

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM 5.3 Flash via Z.ai: weekly limit at 100 % until 2026-11-29 (bead coding-harness-b5pu).

## Runner route — 2026-11-25

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-11-25 00:51:01–00:53:03 UTC, 122 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 00:57:06–00:59:08 UTC, 122 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 01:02:26–01:04:00 UTC, 94 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 01:07:58–01:09:44 UTC, 105 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 01:10:20–01:15:00 UTC, 279 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_ci.py`, `tests/test_repo_settings.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-25 01:49:00–01:51:22 UTC, 143 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-25 01:51:33–01:53:12 UTC, 99 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · rejected · measured by the runner
2026-11-25 01:53:23–01:54:56 UTC, 93 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
