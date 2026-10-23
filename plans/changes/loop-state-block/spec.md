---
title: "Spec — loop-state-block"
status: draft
implementation_status: none
date: 2026-10-23
last_reviewed: 2026-10-23
updated: 2026-10-23
supersedes: null
superseded_by: null
bead: coding-harness-i70
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, loop-state]
class: bounded
appetite: 2
adr_files: []
---

# Spec — loop-state-block

The review loop resumes only from state written in its own marked block;
reviewer words cannot select its stages or models (bead coding-harness-i70).
Research: `research.md`. Maintainer's decision: `decisions.md`, Q-1, on
where the runner keeps and reads state.

## Problem

A model-free runner audit at `378879a` (2026-10-21) reproduced a forged
phase-6 `Loop state:` line selecting a never-discovered free model without
a catalog query (`research.md`). The draft-time trace at `9cb6e31`
(2026-10-23) confirms that phase-6 free text is stored unquoted, released
state is searched beyond its own release section, and state writers replace
the first matching line anywhere in the external record. Reviewer evidence
and runner control data consequently lack a sufficient boundary.

## Terms

- **Snapshot:** the existing state of selected stages, frozen model membership
  and consumed stages, including any availability metadata already stored.
- **Owned block:** a clearly delimited state block in a runner-defined
  structural location, outside reviewer evidence; copied delimiters alone
  do not establish ownership.
- **Resume:** continuing the same run from the external `loop.md` or, after
  its release and deletion, from the latest applicable release in `findings.md`.

## Acceptance criteria

1. When the runner writes a snapshot to an external loop record or a release,
   the authoritative snapshot occupies exactly one owned block in that record
   or release.
   *Refuted by:* a bare authoritative state line, missing delimiters, or two
   authoritative blocks in the same record or release.

2. When a loop-round answer contains a forged snapshot, that answer never
   supplies the state used to resume.
   *Refuted by:* a bare state line or an imitation owned block in the answer
   changes the resumed snapshot or causes a model from the forgery to run.

3. When a phase-6 verdict contains a forged snapshot, that verdict never
   supplies the state used to resume.
   *Refuted by:* a bare state line, an imitation owned block, or a forged
   release heading in a verdict changes resumed state or selects a model
   from the forgery, including after a real release with no kept words.

4. When a valid run is released and resumed, its snapshot survives unchanged
   until the runner makes the next legitimate state transition.
   *Refuted by:* changed membership or metadata, reset consumption, catalog
   rediscovery, or a next stage different from the one in the saved snapshot.

5. If an existing run needs a snapshot whose owned block is missing,
   incomplete, duplicated, or invalid, continuation refuses with an actionable
   state-format diagnostic before discovery or a reviewer call.
   *Refuted by:* falling back to bare lines, older releases or invented state;
   making a catalog/model call; or changing either stored record on refusal.

6. When a state update or release encounters reviewer evidence containing
   state syntax, it preserves that evidence and the existing finding rows.
   *Refuted by:* overwriting a forged line instead of the owned block, losing
   reviewer text or rows, or leaking state-block furniture into kept evidence.

## Non-goals

- Changing stage selection, availability receipts, model admission, prices,
  stop rules, restart authorization, or the snapshot's existing field schema.
- Automatically migrating old bare-line snapshots; ambiguous or legacy runs
  refuse rather than treating reviewer text as trusted migration input.
- Authenticating arbitrary manual edits to files or changing other review
  protocols beyond what isolates loop state from reviewer evidence.
- A design artifact or ADR: this is the bounded format and parser repair
  already decided by the maintainer; phase 2b does not run for this class.

## Protected areas

- `model-endpoints.yaml`, `decisions/`, `docs/adr/` and `AGENTS.md`: no policy,
  model contract or architecture decision changes are needed.
- Other changes' artifacts and existing historical findings: no bulk rewrite
  or cleanup is part of the repair.

## Definition of Done

- `PYTHON=.venv/bin/python3 make verify` is green after implementation.
- The phase-6 injection reproduction fails before the repair and passes after;
  the criterion ledger names every new regression test.
- Documents changed with code: this change's `spec.md` and `plan.md` only if
  implementation needs a recorded clarification; models and ADRs: none.
- The pull request file list shows protected areas untouched and non-goals unbuilt.
- The pull request closes coding-harness-i70 (reviewer text read as loop state),
  and its last commit carries `Closes-Bead: coding-harness-i70`.
- Special runs: deterministic fake CLI tests; no live model calls required.

## Open decisions

None open. The maintainer's recorded answer is unchanged.

- [DETAIL] Use explicit delimiters plus a structural location, because reviewer
  text can copy any delimiter; exact spelling belongs to implementation.
- [DETAIL] Refuse legacy or ambiguous snapshots without rewriting them,
  because no trusted automatic conversion can be inferred from bare lines.
  Genuinely fresh runs and explicitly authorized restarts keep their existing
  discovery behavior; they are not failed attempts to resume an old snapshot.
- [DETAIL] Set a two-hour phase-4 appetite including repairs, because this is
  one local storage-boundary repair; stop and report unfinished work at the limit.
