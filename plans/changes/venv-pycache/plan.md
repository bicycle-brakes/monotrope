---
title: "Plan — venv-pycache"
status: draft
implementation_status: none
date: 2026-10-24
last_reviewed: 2026-10-24
updated: 2026-10-24
supersedes: null
superseded_by: null
bead: coding-harness-q94b
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, tool-integrity]
---

# Plan — venv-pycache

```text
For you:     Test-written venv caches no longer refuse an attempt; other environment changes still do.
Done when:   Regression tests prove cache deletion before tool use, repeated checks and continued integrity refusal, and make verify is green.
Appetite:    2 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Environment rebuilds, caches outside the venv, model routing or retry-policy changes.
Pre-mortem:  suppose it failed: most likely because a later check mistakes the runner's own deletion for tampering.
Starts unless you say stop.
```

## Files and steps

1. Change `scripts/stage2.py`: normalize eligible cache writes at the shared
   `tool_problem` boundary, with safe deletion and narrowly updated baseline
   bookkeeping; retain `tool_state` coverage of every file and symlink.
2. Change `tests/test_stage2.py`: add the regressions named below using
   temporary environments and the existing `World`/local command stand-ins.
3. Update `plans/changes/venv-pycache/plan.md`: convert pending ledger entries
   as tests land; leave measured time to the runner. The runner updates
   `plans/changes/venv-pycache/findings.md` and `plans/INDEX.md`.
   No implementation file is created or deleted.

## Implementation contract

- Leave the `before is None` behavior unchanged. With a baseline, inspect
  current digests before comparing, find new or content-changed regular files
  below an exact `__pycache__` component inside `.venv/`, and unlink them.
  Include arbitrary suffixes and nested directories; never delete unchanged
  files, directories or symlinks. Retain the initial digest's full coverage.
- Use no-follow directory handling from the `.venv/` root down: a linked
  root, parent, cache directory or file is never a cleanup route. A changed
  link or non-regular replacement remains a difference, not a cache exemption.
  Do not classify the `unreadable` sentinel as cache bytes eligible for trust.
- After each successful unlink, remove only that path's old cache entry from
  the shared baseline dictionary. This records a runner-owned deletion, not
  acceptance of new bytes. Re-read current state before comparing; do not
  rebaseline surviving files. Missing files not deleted by this cleanup stay
  differences. Repeated checks/attempts use this same dictionary, so a
  recreated cache is new and deleted again. Document this narrow mutation.
- On inspection/deletion failure, return a path-naming problem and run no
  tools. Keep successful earlier deletion bookkeeping if a later deletion
  fails. All non-cache differences, including mixed cache/package changes,
  retain the existing refusal and first-differing-path behavior.
- Keep the existing guard call sites in `verify_attempt`, `format_step`,
  `red_first`, `fixed_test_proof` and `verify_draft`; the common boundary
  performs cleanup before their runner-owned steps. Exercise verification
  and draft paths with local launch seams that assert cache absence at the
  first tool invocation; a simulated failed cleanup must invoke no step.
- Preserve existing regression names. Parameterize cache additions/changes,
  protected file mutations, aliases and filesystem failures. Assert actual
  bytes/absence and unrelated baseline entries, not only a green return.
  Add a mixed changed-cache/changed-source case and a three-check sequence:
  clean, clean again, then regenerated cache cleaned against the same baseline.
- Do not touch tracker, ADRs, decisions, prompts, workflow, kit, dependency
  pins, other change artifacts or caches outside `.venv/`. No design is due
  for this bounded change. Do not alter routing, retry or checkpoint policy.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_tool_check_deletes_new_venv_cache — a new cache file survives or alone refuses the check
- 1: not yet written tests/test_stage2.py::test_venv_cache_cleanup_precedes_runner_tools — the first verify or draft step sees the planted cache
- 2: not yet written tests/test_stage2.py::test_tool_check_deletes_changed_venv_cache — changed baseline cache bytes survive or their deletion refuses the check
- 2: not yet written tests/test_stage2.py::test_venv_cache_cleanup_precedes_runner_tools — tool execution precedes removal of changed cache bytes
- 3: not yet written tests/test_stage2.py::test_tool_check_preserves_unchanged_venv_cache — unchanged cache bytes are removed or rewritten
- 4: not yet written tests/test_stage2.py::test_venv_cache_cleanup_survives_repeated_checks — the shared baseline refuses its own deletion or trusts regenerated bytes
- 5: tests/test_stage2.py::test_a_changed_venv_file_is_named_and_refused — source, pth or symlink mutations go unnoticed
- 5: tests/test_stage2.py::test_an_attempt_that_plants_a_venv_package_fails_before_any_step — a changed package reaches a runner step
- 5: tests/test_stage2.py::test_red_first_refuses_a_changed_venv — the baseline proof runs a changed interpreter
- 5: not yet written tests/test_stage2.py::test_cache_cleanup_keeps_other_venv_mutations_refused — outside-cache bytecode, deletion, executable or mixed source/cache tampering passes
- 6: not yet written tests/test_stage2.py::test_venv_cache_cleanup_never_follows_symlinks — an alias target changes or a changed link is exempted
- 7: not yet written tests/test_stage2.py::test_venv_cache_cleanup_failure_stops_runner_tools — unreadable or undeletable cache is accepted or any step runs

## Verification

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 -m pytest tests/test_stage2.py -q
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 scripts/check_interview_minimums.py --change venv-pycache
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 scripts/check_criterion_ledger.py
PYTHON=$PWD/.venv/bin/python3 make verify
```

Show the new/changed cache tests red on the input runner, then green after
repair; inject filesystem failures deterministically rather than relying on
host permissions. No live model call is needed. The runner regenerates the
index, runs full verification and makes the one commit. The requested
`scripts/validate_change_artefacts.py` and a plan template are absent at input
commit `4dc80fa`; use the existing gates and the phase-3 prompt's form.

## Explore route

Research was written by the orchestrating Claude Code Opus 5.5 session on
2026-10-24 from the measured failure at `7586f1a`; no separate exploration
call or Stage-1 fallback was recorded. Phase 2b is omitted by class.

## Time used
