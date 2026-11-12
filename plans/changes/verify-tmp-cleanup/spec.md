---
title: "Spec — verify-tmp-cleanup"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-12
updated: 2026-11-12
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.3
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, model: glm-5.3, version: "2026-11-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, verification, temporary-files]
class: bounded
appetite: 4
adr_files: []
neighbours: [docs/research/2026-11-09-make-verify-long-term.md]
---

# Spec — verify-tmp-cleanup

Full checks remove their own pytest temporary files at the end; the next
check removes leftovers from hard-killed runs (bead coding-harness-bxxt.3).
Research: `research.md`. Decisions: `decisions.md`, answered Q-1 of
2026-11-12, which supersedes the previous supervisor-based plan.

## Problem

- Exploration on 2026-11-10 found no run-end removal of pytest temporary
  roots; pytest prunes old numbered roots only at a later session's start
  (`research.md`, "What exists today").
- The orchestrator reported two finished runs leaving 1.3 and 1.5 GiB and
  a full-volume failure on 2026-11-09; exploration did not reproduce those
  measurements (`research.md`, "Intent of the bead").
- The interview records about 630 MB in four killed runs' locked folders
  on 2026-11-12, which pytest skips for three days regardless of retention
  settings (`decisions.md#Q-1`). That answer chooses a small runner-local
  lifecycle, leaving the admission module unchanged.
- Rejected-attempt code remains at checkout `2fd91ebc`; its supervisor-based
  wiring and tests must be replaced, rather than extended (`research.md`,
  "Redraft baseline — 2026-11-12").
- The draft's document-job check also fails in that obsolete wiring before
  executing gates; this remains an implementation blocker, not evidence
  against the document requirements (`research.md`, "Draft retry diagnosis
  — 2026-11-12").

## Terms

**Run:** One admitted execution of `scripts/verify_all.sh`, including job
subsets and `--ci`; `--list` executes no gates and is excluded.
**Run area:** A directory named for that runner shell's process id under
one private parent shared by runs using the same temporary location.
**Orphan:** An unretained run area whose named process no longer exists.
**Retained:** Explicitly kept after an unsuccessful run for inspection.

## Acceptance criteria

1. When a run starts, it receives its own run area, including when it
   inherits admission from an ancestor.
   *Refuted by:* Two live runs share an area or a nested run deletes its
   parent's area.
2. When pytest inherits the run's environment without a conflicting explicit
   basetemp option, its session roots and parallel workers stay in that area.
   *Refuted by:* A real serial, repeated-session or two-worker probe records
   a temporary path outside the area.
3. When a run ends normally without a retention request, it removes its area
   and preserves its execution status if removal succeeds.
   *Refuted by:* A green or red run leaves files or cleanup masks its verdict.
4. When a run is interrupted by SIGINT, SIGTERM, SIGHUP or SIGQUIT without a
   retention request, its runner removes its area on the catchable exit path.
   *Refuted by:* A completed interrupt leaves the area or reports success.
5. If `HARNESS_VERIFY_KEEP_TMP=1` is set and a run ends unsuccessfully through
   its exit handler, it retains its area and reports its absolute path.
   *Refuted by:* Failed/interrupted evidence disappears, has no reported
   path, or is deleted by the next run's orphan sweep.
6. When a run succeeds, it removes its area even with a retention request.
   *Refuted by:* A successful run with `HARNESS_VERIFY_KEEP_TMP=1` retains it.
7. When a later run starts under the same parent, it removes unretained areas
   named for dead processes and leaves areas named for live processes alone.
   *Refuted by:* A hard-killed runner's area survives the next start after
   its process is gone, or an area with a live process id is removed.
8. While managing run areas, verification leaves unrelated paths and symlink
   targets untouched.
   *Refuted by:* A live sibling, parent sentinel, historical default pytest
   root or external target of a managed symlink is removed or modified.
9. If allocation or required removal fails, verification reports the path
   and failure and returns an unsuccessful status.
   *Refuted by:* Gates start without an area, removal failure is silent,
   or cleanup turns a failure into success.
10. When run-area management runs, gate commands, admission reuse, worker
    selection, duration ownership and job-selection contracts remain intact.
    *Refuted by:* Gate/Makefile pins change, nested work queues again,
    duration ownership changes, worker choices disappear, `--list` allocates
    an area, or the implementation changes `scripts/verify_lock.py`.
11. If inherited pytest options select a basetemp outside management, the
    run refuses before gates with an explanation and preserves unrelated options.
    *Refuted by:* An accepted basetemp spelling escapes containment without
    refusal, or unrelated `PYTEST_ADDOPTS` are rewritten.

## Non-goals

- Independently launched targeted, cheap or red-first Stage-2 checks, direct
  `make test`/pytest calls, and children replacing the inherited environment.
- Historical default pytest roots, arbitrary temporary files and kit scratch
  repositories; only pytest paths inheriting the run environment are covered.
- A free-disk floor (separate work, bead coding-harness-87b0), memory policy,
  scheduling, gate membership or duration-record changes.
- Immediate deletion after SIGKILL; Q-1 explicitly accepts waiting for the
  next run. A killed run cannot honor a request that its exit handler never
  processed; its numeric area is reclaimable at the next start.
- A retention expiry policy, ownership database, leases or a new supervisor.
- Design phase 2b and an ADR: this remains the bounded change selected in
  research and the interview.

## Protected areas

`scripts/verify_lock.py` stays unchanged, as Q-1 requires; its existing
process-group supervision remains responsible for ending protected work.
`decisions/gates.yaml`, `Makefile`, `pyproject.toml`, `scripts/stage2.py`,
`scripts/kit/probe.py` and `scripts/verify_duration.py` stay unchanged.
No held configuration, governance, prompt, template or ADR is edited.

## Boundary

Orphan detection follows Q-1's process-id rule, not descendant leases: a
reused live process id delays cleanup; detached descendants after a hard
kill are outside the guarantee. The managed parent is private to the user;
concurrent hostile substitution by that same user is outside this bounded
fix. Static symlinks must not cause deletion outside the parent. A run using
another temporary location cannot discover earlier areas. Existing unused
supervisor temporary-scope code is not expanded or removed by this change.

## Definition of Done

- `PYTHON=.venv/bin/python3 make verify` is green at the implementation commit.
- The pull request carries `scripts/verify_all.sh`, `tests/test_ci.py`,
  removal of superseded temporary-scope tests in `tests/test_verify_lock.py`,
  and this change's artifacts; the runner regenerates `plans/INDEX.md`.
- Real isolated probes demonstrate placement, normal and interrupted cleanup,
  retention, live-process protection and recovery after SIGKILL.
- The file list shows protected areas unchanged and non-goals unbuilt.
- The pull request closes bead coding-harness-bxxt.3 and its last commit
  carries `Closes-Bead: coding-harness-bxxt.3`.

## Open decisions

None open. Q-1 was answered by the maintainer on 2026-11-12; this redraft
records no new maintainer answer. The eleven criteria retain their numbering;
Q-1 replaces supervisor/descendant-liveness promises with the runner's
process-id lifecycle in criteria 4 and 7.

- [DETAIL] Use `${TMPDIR:-/tmp}/coding-harness-verify-${UID}` as the shared
  parent, with an absolute resolved path and private permissions. Unlike the
  previous draft's parent selection, this does not derive a nested runner's
  parent from its ancestor's exported pytest root; `TMPDIR` stays unchanged.
- [DETAIL] Use numeric process-id directory names and export the area through
  `PYTEST_DEBUG_TEMPROOT`; pytest can number successive sessions within it
  without changing gate commands or adding per-run metadata.
- [DETAIL] Only exactly `HARNESS_VERIFY_KEEP_TMP=1` requests retention; the
  exit handler moves unsuccessful areas to `kept-<pid>` and reports that
  path, so numeric orphan sweeps leave deliberately retained evidence alone.
- [DETAIL] Preserve an existing nonzero status on removal failure; otherwise
  return 2. Signal exits use 128 plus the signal number.
- [DETAIL] Keep the existing four-hour phase-4 stop limit, repairs included;
  historical rejected-attempt time remains evidence in `findings.md`.

These reversible details are chosen here to keep Q-1's implementation small.
