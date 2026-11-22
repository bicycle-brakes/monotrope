---
title: "Spec — red-first-root-refs"
status: draft
implementation_status: none
date: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-dk0h
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, red-first, refs]
class: bounded
adr_files: []
---

# Spec — red-first-root-refs

The private proof repository detects changes to root references as well as ordinary references (bead coding-harness-dk0h). Research: `research.md`. Decisions: `decisions.md`.

## Problem

On 2026-11-03, the predecessor's phase-6 finding F-10 showed that a qualifying named test can create `ORIG_HEAD` and still pass the proof: neither private-reference snapshot measures that root reference (`research.md`, “What exists today”). The same omission affects multi-line `FETCH_HEAD`, so comparing only one object identifier would not close the gap.

## Terms

**Proof:** the baseline red-first run, the fixed-code run, or either the planted or clean guard-test run; each runs a named test in a private repository.

**Root reference:** a direct child of the private Git directory whose name, uppercased, is `HEAD`, `AUTO_MERGE`, `BISECT_EXPECTED_REV`, `NOTES_MERGE_PARTIAL`, `NOTES_MERGE_REF`, `MERGE_AUTOSTASH`, `FETCH_HEAD`, or `MERGE_HEAD`, or consists only of ASCII letters, hyphens and underscores and ends in `_HEAD` after uppercasing. Names come from the directory listing and are compared and reported with their original spelling, case-sensitively. The existing `HEAD` retains its logical comparison; other root-reference entries are compared as complete file bytes, including multi-line contents.

The private repository starts with `HEAD` as its only root reference; setup and source-side reference restoration stay unchanged. In the cases below, an existing non-`HEAD` root reference is planted in the private repository after setup and before the snapshots.

## Acceptance criteria

1. When a named test creates a previously absent root reference in the private repository, the proof refuses and names that reference.
   *Refuted by:* A qualifying test creating `ORIG_HEAD` with `git update-ref ORIG_HEAD HEAD`, `orig_head`, `AUTO_MERGE`, `BISECT_EXPECTED_REV`, `NOTES_MERGE_PARTIAL`, `NOTES_MERGE_REF`, `MERGE_AUTOSTASH`, `FETCH_HEAD`, `MERGE_HEAD`, or a matching hyphenated `_HEAD` name is accepted or its listed name is absent from the refusal.
2. When a named test changes a root reference other than `HEAD` in the private repository, the proof refuses and names that reference.
   *Refuted by:* A qualifying test changes only a later line of an existing multi-line `FETCH_HEAD`, or changes only the spelling of a listed root-reference name, and the proof accepts it or omits the changed name from the refusal.
3. When a named test deletes an existing root reference other than `HEAD` from the private repository, the proof refuses and names that reference.
   *Refuted by:* A qualifying test removes a pre-existing private `ORIG_HEAD` and the proof accepts it or omits its name.
4. When a root reference other than `HEAD` is unchanged in name and complete bytes during the named test, it does not by itself invalidate the proof.
   *Refuted by:* An unchanged, multi-line private `FETCH_HEAD` causes an otherwise qualifying proof to be refused.
5. If a matching private root-reference entry cannot be safely measured before or after the test, the proof refuses without blocking and still removes its private repository.
   *Refuted by:* A FIFO or symbolic link named `ORIG_HEAD` is followed or blocks the proof, an unreadable entry is accepted, or a measurement failure leaves the private repository behind.
6. When source-repository references change during a proof, those changes alone do not invalidate the private proof.
   *Refuted by:* A concurrent source `FETCH_HEAD` change refuses an otherwise qualifying proof or changes the source on the proof's behalf.
7. When ordinary private references are packed without a logical change, the proof continues to accept the otherwise qualifying test.
   *Refuted by:* `git pack-refs --all` alone refuses a proof whose logical references remain unchanged.
8. When the root-reference comparison runs, both pre-existing private-reference snapshots include the root references defined above.
   *Refuted by:* Either snapshot misses a created `ORIG_HEAD` or a complete multi-line `FETCH_HEAD` change.

## Non-goals

- Detecting transient changes restored before the post-test snapshot, changes outside the private store, or new classes of Git metadata.
- Altering proof outcome classification, source-reference restoration, or the Git version supported by the existing runner.
- Rewriting historical findings or handovers; the parked finding remains a historical record.

## Protected areas

The source repository's references, index and worktree are read-only during proof execution. Existing logical handling of `HEAD`, ordinary references, packing, and malformed `packed-refs` remains in force.

## Definition of Done

- `make verify` green, including the existing reference-guard tests and the new regressions.
- Living documents: none found naming this limit in the 2026-11-22 search; historical records remain intact.
- Protected areas untouched and non-goals unbuilt, shown by the pull request's file list.
- The pull request closes bead coding-harness-dk0h and its last commit carries `Closes-Bead: coding-harness-dk0h`.
- Special runs: none.

## Open decisions

None open.

- [DETAIL] The spec-review decisions in `findings.md` F-2 and F-3 clarify and supersede the earlier shorthand in `decisions.md`: include the listed irregular Git names and match case-insensitively while preserving listed spelling, so Git references cannot escape the private comparison through their names.
- [DETAIL] The spec-review decision in `findings.md` F-1 keeps source setup unchanged: only private proof snapshots gain root-reference measurements, avoiding a new source-copy path.
- [DETAIL] Keep `HEAD`'s logical comparison and compare the other named root files as bytes: this preserves the established acceptance of equivalent `HEAD` rewrites while measuring all of `FETCH_HEAD` as decided.
- [DETAIL] Refuse nonregular or unreadable matching entries before reading them: the existing private-ref guard already refuses unsafe entries, and a FIFO must not block a proof.
- [DETAIL] Leave malformed `packed-refs` handling unchanged: the recorded scope concerns direct children of the Git directory, not a change to packed-ref syntax.
