---
title: "Spec — research-swarm-resume"
status: draft
implementation_status: none
date: 2026-11-26
last_reviewed: 2026-11-26
updated: 2026-11-26
supersedes: null
superseded_by: null
bead: coding-harness-f6qj
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-26"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, research-swarm, resume]
class: bounded
appetite: 4
adr_files: []
---

# Spec — research-swarm-resume

Finished repository research contributions survive an aborted run and are reused on a matching resume (bead `coding-harness-f6qj`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

The maintainer recorded that consecutive runs with unchanged selection and tree recomputed all repository-topic seats because their prompt hashes changed, while finder, merge, sentence and online seats reused successfully (2026-11-25, `decisions.md` Q-1; the two observed changes and runs are named there). The exploration at commit `39004d9e` describes the existing exact binding and prompt-hash reuse checks and the persistence of terminal results (`research.md`); it did not establish the source of the drift.

## Acceptance criteria

1. When a research swarm resumes a stored incomplete run under the store's matching-resume rule (`changed_against_stored`, including after committing an earlier incomplete run's appended publication to `research.md` and its `updated:` restamp so `HEAD` has moved, and across multi-run chains such as run 1 → run 2 → run 3) with the same selection, each repository-topic prompt for topics 1–8 is byte-identical to its corresponding prompt in the origin run.
   *Refuted by:* A corresponding prompt for any of topics 1–8 differs between run 1 and a matching resumed run 2 or run 3 because of a run identifier, publication growth, `updated:` restamp, moved `HEAD`, timestamp, changing commit count or another non-frozen input.
   *Basis:* `decisions.md#Q-1`.
2. When two repository-topic seats fail in run 1 (seats A and B), run 2 reuses every other finished valid repository-topic seat from run 1 and succeeds on seat A while failing seat B, and run 3 resumes run 2, run 3 reuses both the run-1 seats carried forward and seat A from run 2 without relaunching them, validating reused seats against the replayed origin baseline (`sources`, `map`, `history`) while newly launched seats on a resumed run validate against the live worktree view (accepting origin-baseline citations from the replayed packet as well).
   *Refuted by:* A successful repository-topic seat from run 1 or run 2 is launched again, rejected by validation against drifted post-publication `research.md`/HEAD state, or its stored result is not adopted.
   *Basis:* `decisions.md#Q-1`.
3. When a failed repository-topic seat is resumed, it is launched again rather than adopted as a successful result.
   *Refuted by:* The failed seat is reused or never launched.
   *Basis:* `decisions.md#Q-1`.
4. When a binding, seat identity, model, prompt hash or result validity fails the existing reuse checks, the affected result is not reused.
   *Refuted by:* A mismatched or invalid result is adopted despite the existing checks.
   *Basis:* `decisions.md#Q-1`; `research.md`, “The reuse decision”.
5. When a repository-topic prompt for topics 1–8 is built on run 1 or on any matching resumed run in the chain, its `# Finder map (data)` packet preserves every resolved entry's non-empty locator, `extent` (start and end line) and `excerpt_sha256` from the origin run's frozen inputs (matching run 1), and topic 6 preserves `# Mapped history (data)` from the origin run's baseline `HEAD`; judge composition (`compose`) and published `map`/`history` fences use those same replayed baseline inputs while the resumed run's `baseline HEAD` line and manifest `head`/`digest` keep the resumed run's own freeze and record the origin baseline HEAD in a dedicated field (`origin_head`).
   *Refuted by:* A repository-topic prompt drops or blanks resolved map `extent` or `excerpt_sha256` fields, topic 6 drops `# Mapped history (data)`, or reused-seat validation / judge composition reads drifted post-publication `research.md` or moved-`HEAD` history that disagrees with the prompt.
   *Basis:* `decisions.md#Q-1`.

## Non-goals

- Changing the matching-resume comparison rules (`changed_against_stored`), the exact `prompt_sha256` / slot-identity reuse checks, the selection of seats, or the research swarm's availability and retry policies. (Adding replayable origin-baseline fields to the stored run record so matching resumes can replay run 1's inputs is explicitly in scope.)
- Maintaining prompt-hash compatibility with slots stored under a pre-fix drifted prompt hash: pre-fix slots whose prompt hash still matches and validates are reused under criterion 4, and any pre-fix slot recorded under a drifted hash is recomputed once without clearing the store or relaxing validation.
- Repairing unrelated research-swarm failures or altering published research semantics beyond recording the replayed baseline inputs and `origin_head` on a resumed run.

## Protected areas

Model configuration, leak checks, and unrelated changes remain untouched: this is a resume fix, not a change to security or model routing.

## Definition of Done

- `make verify` green; a deterministic three-run regression (run 1 fails repository-topic seats A and B and commits its publication -> run 2 reuses all other repository-topic seats from run 1, launches only A and B among repository-topic seats, succeeds on A, fails B, and commits its publication -> run 3 reuses both the carried-forward run-1 seats and seat A from run 2, launches only seat B among repository-topic seats, and reaches the judge, with non-empty resolved `extent`/`excerpt_sha256` and topic-6 `# Mapped history (data)`) and the existing reuse boundary tests pass.
- Documentation changes: update `docs/WORKFLOW.md` Q-13 if the stored run record carries additional replayable baseline fields; no ADR changes expected.
- Protected areas and non-goals remain untouched, shown by the pull request's file list.
- The pull request closes bead `coding-harness-f6qj`, and its last commit carries `Closes-Bead: coding-harness-f6qj`.
- Special runs: none.

## Open decisions

None open.

[DETAIL] A four-hour phase-4 appetite is a reversible stop for this bounded fix; it keeps the investigation and regression proportionate to the stated scope.

[DETAIL] Spec-review S-1 (matching resume definition): Adopt Reading B — a matching resume follows the store's existing `changed_against_stored` contract, including resuming after committing an earlier incomplete run's appended `research.md` publication (moved `HEAD`, appended tail and `updated:` restamp). Repository-topic prompts (including map entries resolved from `research.md` and topic 6's `# Mapped history (data)`) derive from the origin run's stored baseline inputs rather than the moved `HEAD` or appended tail (bounded standing grant).

[DETAIL] Spec-review S-2 & S-7 (evidence preservation): Repository prompts carry resolved finder-map `extent` and `excerpt_sha256` (not full excerpt text, Reading A of S-7) and topic 6 carries `# Mapped history (data)`. Byte-identity is achieved strictly by replaying the origin run's baseline inputs (criterion 5), never by dropping or blanking `extent`, `excerpt_sha256`, or `# Mapped history (data)` (bounded standing grant).

[DETAIL] Spec-review S-3 (pre-fix stores): Existing `plan_reuse` and `validate_research_report` checks stay strict (criterion 4 and Non-goals); pre-fix stored slots with matching hashes and valid results are reused, while pre-fix slots with previously drifted hashes are recomputed once without wiping the store (bounded standing grant).

[DETAIL] Spec-review S-4 (stored baseline fields): Adopt Reading A — persisting the replayable origin-baseline inputs (such as baseline `HEAD` and the frozen origin `research.md` snapshot or resolved baseline inputs) in the stored run record is allowed and does not weaken `changed_against_stored` or prompt-hash validation; `docs/WORKFLOW.md` Q-13 may be updated to note the stored baseline fields (bounded standing grant).

[DETAIL] Spec-review S-5 & S-10 (multi-run resume chains & three-run regression): Adopt Reading A of S-5 — when run 2 resumes run 1, run 2 persists run 1's replayed origin-baseline inputs into run 2's stored run record so run 3 (reading only the latest stored run) reproduces the exact same origin prompts and reuses seats launched in both run 1 and run 2. The three-run regression (S-10) fails repository-topic seats A and B in run 1, succeeds on A and fails B in run 2, and launches only B among repository-topic seats in run 3 before proceeding to the judge (bounded standing grant).

[DETAIL] Spec-review S-6, S-8 & S-9 (consistent replay, live relaunched seats, manifest baseline HEAD): Reused stored seats validate against the replayed origin baseline (`sources`, `map`, `history`), while newly launched repository seats on a resumed run (which execute with `cwd = self.root` against the live worktree) validate against the live freeze while also accepting origin-baseline citations from the replayed packet (S-8). For publication (S-9, Reading B), the resumed run's `baseline HEAD` line and manifest `head`/`digest` keep the resumed run's own freeze so `head` and `digest` stay consistent, while the replayed origin HEAD is recorded in a dedicated field (`origin_head`) alongside the replayed `map`/`history` fences (bounded standing grant).
