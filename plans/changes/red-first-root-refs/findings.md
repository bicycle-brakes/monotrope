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

Stage-2 call, 2026-11-22: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1171 files, 5357 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-22

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-4 | MAJOR | SPEC | base | `spec.md`, Terms ¶2 ("setup and source-side reference restoration stay unchanged"), AC 6, DoD item 3; `scripts/stage2.py:8679`; `tests/test_stage2.py:19519` | No criterion goes red if proof setup starts reading the source's root references. Terms ¶2 and the F-1 decision say setup stays unchanged. AC 6's refutation only needs a source `FETCH_HEAD` that changes while the named test runs. The source is read only at setup, before that change happens. The remedy F-10 records is to widen `_ref_targets` with `--include-root-refs` or a direct listing. `_private_repository` (`scripts/stage2.py:8679`) calls the same function on the source, so that widening would copy the source's `ORIG_HEAD` into the clone. A source with a multi-line `FETCH_HEAD`, or a linked-worktree source whose `.git` is a file, would also go through a path the F-1 decision ruled out. AC 1–8 still pass, because a root reference copied at setup stays the same across the run. `reset_tree` (`tests/test_stage2.py:19519`) already leaves an `ORIG_HEAD` in the source of the guard-proof tests, and nothing turns red. No criterion states the refuting case: a source that holds `ORIG_HEAD` and a multi-line `FETCH_HEAD` before the proof starts (and a linked-worktree source), where the proof must accept and the private store must start with `HEAD` as its only root reference. DoD item 3 cannot catch it either. Every protected behaviour is in `scripts/stage2.py`, which this change has to edit, so the pull request's file list shows nothing. | Opus | in spec — [DETAIL] decided by the orchestrator: add a criterion — proof setup never reads the source's root references: a source with ORIG_HEAD and a multi-line FETCH_HEAD sets up unchanged and the private store starts without them; refuted if setup copies or fails on them. Reason: the F-1 decision must be able to go red | — |
| F-5 | MINOR | SPEC | base | `spec.md`, Terms ¶1 ("whose name, uppercased, is `HEAD`" … "The existing `HEAD` retains its logical comparison; other root-reference entries are compared as complete file bytes"), AC 2 | [AMBIGUITY] Terms makes any entry whose name uppercases to `HEAD` a root reference. It keeps "the existing `HEAD`" on the logical comparison and compares "other" entries as bytes. AC 2's spelling-change refutation covers only references other than `HEAD`. Nothing says which group an entry spelled `head` or `Head` belongs to. Case: on the darwin runner's case-insensitive APFS, a named test runs `os.rename('.git/HEAD', '.git/head')`, and Git still resolves `HEAD` through that file. Reading A: only the entry spelled exactly `HEAD` is HEAD. `head` is then a new entry compared as bytes, so the proof refuses and names `head`. Reading B: any entry whose name uppercases to `HEAD` is HEAD and keeps the logical comparison. The logical HEAD has not changed, so the proof accepts. On a case-sensitive filesystem the same question decides whether a separate `.git/Head` written by the test is refused or ignored. | Opus | in spec — [DETAIL] decided by the orchestrator: an entry whose name is exactly HEAD keeps the logical comparison; any other entry whose name only uppercases to HEAD (head, Head) is compared as file bytes like the other root references. Reason: a lowercase copy is a stray file the test created | — |
| F-6 | MINOR | SPEC | base | `spec.md`, Terms ¶1 ("whose name, uppercased, is … or consists only of ASCII letters, hyphens and underscores"), AC 1 | [AMBIGUITY] Terms requires ASCII-only names for the `_HEAD` rule but not for the irregular names, which match when the "name, uppercased, is …". It does not say which uppercasing applies. Reading A: Unicode uppercasing, such as Python's `str.upper()`. `BIſECT_EXPECTED_REV` and `NOTEſ_MERGE_REF` (with U+017F, long s) uppercase to listed names. A named test that creates one is refused, and the listed spelling is reported. Reading B: ASCII-only uppercasing, which matches the `_HEAD` rule. Those entries are then not root references, and the proof accepts. On a filesystem whose case-insensitive lookup folds `ſ` to `s`, as Unicode case folding does, Git reading `BISECT_EXPECTED_REV` would open that file. Under Reading B a reference then escapes the comparison through its name, which the F-3 decision set out to prevent. AC 1 lists only ASCII spellings, so neither reading can go red. | Opus | in spec — [DETAIL] decided by the orchestrator: every name, irregular names included, must be ASCII before uppercasing; a non-ASCII name never matches. Reason: one rule for the whole set | — |

Stage-2 call, 2026-11-22: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1171 files, 5361 commits, 12 rules.

> Attempt 1 (codex) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/red-first-root-refs/draft-attempt-1-20261122T084824280823Z (60370d0310cc); `git diff 0b8664407e49 refs/stage2/attempts/red-first-root-refs/draft-attempt-1-20261122T084824280823Z` shows it.

Stage-2 call, 2026-11-22: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1171 files, 5361 commits, 12 rules.

> Attempt 2 (codex-repair) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/red-first-root-refs/draft-attempt-2-20261122T084840266546Z (beac2538dbf1); `git diff 0b8664407e49 refs/stage2/attempts/red-first-root-refs/draft-attempt-2-20261122T084840266546Z` shows it.

Stage-2 call, 2026-11-22: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 1171 files, 5361 commits, 12 rules.
