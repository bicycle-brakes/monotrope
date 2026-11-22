---
title: "Findings — red-first-root-refs"
category: findings
status: draft
implementation_status: none
date: 2026-11-22
created: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-dk0h
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — red-first-root-refs

Stage-2 call, 2026-11-22: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1168 files, 5349 commits, 12 rules.

Stage-2 call, 2026-11-22: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1171 files, 5350 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-22

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | BLOCKER | SPEC | base | `spec.md`, AC 8 and Terms; `decisions.md`, "Both snapshots"; `scripts/stage2.py:8679`, `:8692-8708` | [AMBIGUITY] AC 8 and decisions.md put root references into `_ref_targets`. But `_private_repository` also calls `_ref_targets` on the source, and setup restores whatever it returns into the clone. Reading A: widen `_ref_targets` itself, so the source's ORIG_HEAD, FETCH_HEAD and the rest are read and copied into the private store. Setup then has to carry multi-line FETCH_HEAD bytes, which neither the `update-ref --stdin` lines nor the `symbolic-ref` restore loop can express. So setup fails for any source that has fetched, unless a new copy path is invented. The source is normally a linked worktree whose `.git` is a file, so it has no "direct child of the Git directory". A FIFO named `ORIG_HEAD` in the source would block or refuse setup, and AC 5 (private store only) and AC 6 do not cover that. Reading B: root references enter only the two snapshots taken on the private store, and setup is unchanged. The private store then starts with HEAD as its only root reference. The "existing" or "pre-existing" root reference in the refutation cases of AC 2, 3, 4 and 5 can then exist only if a test plants it after setup, never through a proof. research.md ("What is unclear", item 3) left this open, and neither spec.md nor decisions.md settles it. | Opus | in spec — [DETAIL] decided by the orchestrator: reading B — root references enter only the two snapshots taken on the private store; _ref_targets for the source and the setup copy are unchanged, so the private store starts with HEAD as its only root reference and any root reference that appears or changes during the proof is a persistent change. decisions.md is corrected. Reason: no new copy path, and the comparison sees exactly what the test created | — |
| F-2 | MAJOR | SPEC | base | `spec.md`, Terms and AC 1; `decisions.md`, "Which root references" | [AMBIGUITY] decisions.md bases the set on "git's own pseudo-ref naming". spec.md Terms defines it as uppercase letters, digits and underscores ending in `HEAD`, plus `AUTO_MERGE`. The two give different sets. Git's own root-reference rule (`is_root_ref` in refs.c) is uppercase, `-` and `_`, ending in `_HEAD`. It also lists HEAD, AUTO_MERGE, BISECT_EXPECTED_REV, NOTES_MERGE_PARTIAL, NOTES_MERGE_REF and MERGE_AUTOSTASH; FETCH_HEAD and MERGE_HEAD are separate pseudorefs. Literal Terms reading: a named test that leaves `NOTES_MERGE_REF` (a conflicted `git notes merge`), `MERGE_AUTOSTASH` (a conflicted `git merge --autostash`) or `BISECT_EXPECTED_REV` in the private store passes the proof. That is the persistent change F-10 describes, and AC 1 does not see it. "Git's own naming" reading: those are refused. The [DETAIL] on AUTO_MERGE ("the recorded examples include it") does not say whether Git's other irregular names are in or out. | Opus | in spec — [DETAIL] decided by the orchestrator: git's own set — every direct child of the private git directory that git treats as a root reference or pseudoref (is_root_ref: uppercase, hyphen and underscore ending in _HEAD, plus HEAD, AUTO_MERGE, BISECT_EXPECTED_REV, NOTES_MERGE_PARTIAL, NOTES_MERGE_REF, MERGE_AUTOSTASH) plus FETCH_HEAD and MERGE_HEAD; the spec lists them. Reason: the persistent change F-10 describes covers all of them | — |
| F-3 | MINOR | SPEC | base | `spec.md`, Terms ("consists solely of uppercase ASCII letters"), AC 1 and AC 5 | The spec does not say whether an entry's name is taken from the directory listing or as Git resolves it. On a case-insensitive filesystem (default APFS; the runner runs on darwin), a named test can write `.git/orig_head` directly, and Git resolves that file as `ORIG_HEAD` (`git rev-parse ORIG_HEAD` opens it). Its listed name is not uppercase, so an implementation that matches the listing never measures it and the proof accepts. An implementation that matches names case-insensitively refuses. Neither AC 1 nor AC 5 decides which outcome is correct. | Opus | in spec — [DETAIL] decided by the orchestrator: names are taken from the directory listing of the private store and compared case-sensitively as listed; any entry whose upper-cased name matches the set counts. Reason: a case-insensitive filesystem must not hide a reference | — |

Stage-2 call, 2026-11-22: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1171 files, 5356 commits, 12 rules.
