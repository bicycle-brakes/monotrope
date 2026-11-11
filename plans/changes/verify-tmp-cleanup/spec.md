---
title: "Spec — verify-tmp-cleanup"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-11
updated: 2026-11-11
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.3
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, verification, temporary-files]
class: bounded
appetite: 4
adr_files: []
neighbours: [docs/research/2026-11-09-make-verify-long-term.md]
---

# Spec — verify-tmp-cleanup

Each full verification run owns its pytest temporary area and removes it
after use, including failure and interruption, unless the caller explicitly
keeps a failed run for inspection (bead coding-harness-bxxt.3).
Research: `research.md`. Decisions: `decisions.md`.

## Problem

- On 2026-11-10, exploration found that verification never assigns or removes
  a run-specific pytest temporary area; pytest's default retains numbered
  roots until a later session prunes them (`research.md`, "What exists today").
- The orchestrator recorded two finished runs leaving 1.3 and 1.5 GiB and a
  full-volume failure on 2026-11-09; these figures are the intent's report,
  not a measurement reproduced by exploration (`research.md`, "Intent of
  the bead" and "Evidence of that root on this machine").
- Process cleanup already covers ordinary endings and trapped signals,
  but does not remove files; indiscriminate temporary-root cleanup would
  also remove unrelated hook/statusline data (`research.md`, "What cleans
  up today" and "Constraints a base folder must respect", 2026-11-10).

## Terms

**Run:** An executing invocation of `scripts/verify_all.sh`, including job
subsets and `--ci`; `--list` executes no gates and is not a run.
**Run area:** The run's private temporary directory containing its pytest
session roots; successive pytest sessions need not share a basetemp.
**Retained:** Deliberately kept after an unsuccessful run for inspection.
**Orphan:** An unretained managed area whose supervisor and protected work
have ended; age or a missing supervisor alone does not prove this.

## Acceptance criteria

1. When a run starts, it receives a distinct run area even if it inherits
   verification admission from an ancestor.
   *Refuted by:* Two runs share an area, or a nested run removes its parent's area.
2. When a pytest session inherits the run's environment, its temporary
   session root and xdist worker directories lie inside that run area.
   *Refuted by:* A real serial or parallel pytest probe reports a temporary
   path outside the area, including a second session in the same run.
3. When a run ends normally without an explicit retention request, its run
   area is removed before its supervisor returns the original run status.
   *Refuted by:* A successful or failed run leaves its area, or cleanup masks
   a failing status when removal succeeds.
4. When the supervisor receives SIGINT, SIGTERM, SIGHUP or SIGQUIT, the run
   area is removed after protected process cleanup, absent requested retention.
   *Refuted by:* A signal leaves the area, removes it while the supervised
   group can still write, or changes the existing 128-plus-signal status.
5. If `HARNESS_VERIFY_KEEP_TMP=1` is set and the run ends unsuccessfully,
   its run area is retained with its absolute path reported to the caller.
   *Refuted by:* The area is removed immediately or by a later sweep, or no
   usable inspection path is reported; interrupted runs count as unsuccessful.
6. When a run succeeds, its run area is removed regardless of the retention
   variable's value.
   *Refuted by:* A successful run with `HARNESS_VERIFY_KEEP_TMP=1` leaves its area.
7. When a later run starts in the same managed temporary location, it reclaims
   orphan areas without reclaiming areas still used by protected work.
   *Refuted by:* A completed hard-killed run's orphan survives the next start,
   or a surviving protected child loses its area when its supervisor is killed.
8. While allocating, sweeping or removing run areas, verification leaves
   unrelated paths and symlink targets untouched.
   *Refuted by:* An active sibling run, the caller's parent contents outside
   the managed subtree, a default pytest root, unrelated file or substituted
   symlink target is removed or modified.
9. If allocation or required cleanup cannot complete safely, the invocation
   reports the affected area and reason and returns an unsuccessful status.
   *Refuted by:* Gates start after allocation failed, cleanup failure is
   silent, success is returned despite it, or an existing failure/signal
   status is replaced by success.
10. When run-area management is enabled, existing gate commands, admission
    reuse, worker selection and execution verdicts retain their contracts.
    *Refuted by:* Gate/Makefile command pins change, nested work waits on its
    own admission, duration ownership changes, worker overrides are lost,
    or `--list` allocates an area or enters admission.
11. If inherited pytest options explicitly select a basetemp outside run
    management, the run refuses before executing gates with an explanation.
    *Refuted by:* `PYTEST_ADDOPTS` redirects pytest writes outside the area
    without a refusal, or unrelated pytest options are discarded.

## Non-goals

- Independently launched Stage-2 targeted, cheap and red-first pytest checks,
  direct `make test`/pytest calls, and subprocesses deliberately replacing
  the inherited pytest environment; they require a separate extension.
- Reclaiming historical default `pytest-of-*` roots, arbitrary temporary
  files, kit scratch repositories or application caches.
- A free-disk admission floor (separate work, bead coding-harness-87b0),
  changes to memory policy, scheduling, duration records or gate membership.
- Immediate cleanup after an uncatchable SIGKILL of the supervisor; recovery
  happens on a later run, once protected work has ended.
- A retention browser, expiry policy or automatic deletion of explicitly
  retained areas; the caller removes those areas after inspection.
- Design phase 2b and an ADR: this remains the bounded lifecycle fix already
  classified in `research.md` and `decisions.md`.

## Protected areas

`decisions/gates.yaml`, `Makefile`, `pyproject.toml`, `scripts/stage2.py`,
`scripts/kit/probe.py` and `scripts/verify_duration.py` stay unchanged: the
existing gate source, dependency/configuration contract and separate test
entry points do not need edits. No held harness configuration, governance
file, prompt, template or ADR is edited.

## Boundary

The promise covers pytest sessions inheriting the runner environment,
including the ordinary pytest gate and kit probe; it does not capture every
temporary write by every test. Cleanup follows the existing process-group
supervision boundary: descendants detached into another group after a hard
kill of an intermediate process are not guaranteed detectable. An area whose
liveness or ownership cannot be established safely is left untouched and
reported, rather than guessed orphaned. A later run using another temporary
parent cannot discover an orphan in the previous parent.

## Definition of Done

- `PYTHON=.venv/bin/python3 make verify` is green at the implementation commit.
- The same pull request carries `scripts/verify_all.sh`,
  `scripts/verify_lock.py`, `tests/test_ci.py`, `tests/test_verify_lock.py`
  and the change artifacts; the runner regenerates `plans/INDEX.md`.
- The file list demonstrates the protected areas untouched and non-goals unbuilt.
- The pull request closes bead coding-harness-bxxt.3 and its last commit
  carries `Closes-Bead: coding-harness-bxxt.3`.
- Revision-bound evidence covers real pytest/xdist placement, exit/signal
  cleanup, requested retention and hard-kill recovery in isolated fixtures.

## Open decisions

None open. The reasoned interview skip remains a skip; this draft records
no maintainer answer and does not claim that the skip was confirmed.

- [DETAIL] Use exactly `HARNESS_VERIFY_KEEP_TMP=1` as the request; absent,
  empty or other values mean normal removal, making retention explicit.
- [DETAIL] Use a private managed subtree under the caller's
  `PYTEST_DEBUG_TEMPROOT`, or the platform temporary parent when unset;
  keep `TMPDIR` unchanged so unrelated temporary writers keep their contract.
- [DETAIL] Retain interrupted runs on the same explicit request, because an
  interrupted check also needs inspectable failure evidence; after SIGKILL,
  recovery honors that request when the run's final outcome is unknown.
- [DETAIL] Preserve a pre-existing nonzero/signal status on cleanup failure;
  turn an otherwise successful invocation into exit 2 and report the failure.
- [DETAIL] Reject conflicting inherited `--basetemp` options rather than
  deleting a caller-owned directory or silently claiming containment.
- [DETAIL] The phase-4 appetite is four hours including repairs, a stop limit
  chosen for the lifecycle and process tests; no previous appetite is recorded.

These reversible details specify the operational interface without widening
the full-check scope fixed in `decisions.md`.
