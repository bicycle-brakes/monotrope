---
title: "Findings — stamp-day-source"
category: findings
status: draft
implementation_status: none
date: 2026-11-28
created: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-5v6t
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — stamp-day-source

Stage-2 call, 2026-11-28: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1325 files, 6163 commits, 12 rules.

Stage-2 call, 2026-11-28: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1328 files, 6165 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-28

Spec fingerprint: sha256:9263c942f0d98bb8cd1b2742a46dada495f9827f5d7f83e697cbd8a3fc433a5c

Spec review commit: 349e5146ef95b8e6cd3f012d58d6c15fa403c3f1

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | [AMBIGUITY] | SPEC | base | spec.md Open decisions [DETAIL]; AC 1, AC 2, AC 3 | The [DETAIL] requires a checkpoint to "bind its stamp to its own commit day" but does not say how. Reading A: the runner sets the commit's date itself. One clock reading supplies both the stamp and the date `git commit` records in `checkpoint()` (scripts/stage2.py:9957); today no `GIT_COMMITTER_DATE` is set there, so git's own clock decides. The recorded commit time can then be hours earlier than the real commit: a stamp at 23:50 and a commit at 01:30 is recorded as 23:50. That may conflict with the non-goal "Redesigning clocks". Reading B: git keeps its own clock. The runner restamps just before `git add -A` and compares the recorded `%cs` afterwards. That leaves a race between stamp and commit, and on a mismatch the commit already exists, which AC 5's "does not create that checkpoint" rules out. The two readings record different history and need different AC 2/3 tests: under A the runner overrides any commit date the test supplies, under B the test has to supply it. | Opus | in spec — reading A (one clock reading for stamp and commit dates); [DETAIL] S-1..S-6 (bounded standing grant) | — |
| S-2 | [AMBIGUITY] | SPEC | base | spec.md AC 1, AC 2, AC 3, AC 6 ("runner-maintained `updated:` stamp") | The set of documents is not defined. Reading A: every changed held document in the checkpoint counts, because `prepare_derived` (scripts/stage2.py:8218-8230) stamps each one, including files the model edited such as `docs/WORKFLOW.md` in 6bf5c6fc. Reading B: only documents the runner writes itself (`stamp_updated` on findings.md and plan.md, `publish_research`). Under B the incident's own file is outside AC 1/2/3, and a fix that refreshes only the runner's own records passes every criterion. Also open: whether files with a header under `frontmatter: optional` prefixes, which `stamp_updated` also stamps, are in the set. | Opus | in spec — reading A (every changed held document); [DETAIL] S-1..S-6 | — |
| S-3 | [AMBIGUITY] | SPEC | base | spec.md AC 1 ("at least") vs AC 3 ("uses that commit's calendar day") | AC 1 allows a stamp later than the commit day; AC 3 asks for that exact day. They differ on a changed document whose `updated:` is already later than the commit day but within the future allowance, e.g. a model wrote tomorrow's date. Under "at least" the refresh keeps that date; under "uses" it lowers it to the commit day. AC 3 is refuted only by the preceding day or a stale report. A later stamp therefore refutes neither AC 1 nor AC 3, even though at 00:30 +0100 the check reports the 10th as FUTURE (not stale). | Opus | in spec — stamp equals the commit day, later dates lowered; [DETAIL] S-1..S-6 | — |
| S-4 | MAJOR | SPEC | base | spec.md AC 5 | AC 5 names no failure, so no test can trigger one and the criterion cannot go red. The spec neither includes nor excludes these candidates: `CannotStamp` (not valid UTF-8); a header that `stamped()` silently leaves unchanged, i.e. no frontmatter or two `updated:` lines (scripts/check_frontmatter_current.py:476-482), which the verifier reports today; the aliased or hard-linked path `prepare_derived` refuses; a recorded commit day that differs from the stamp; a clock or offset that cannot be read. | Opus | in spec — AC 5 failures named (UTF-8, no frontmatter, two updated lines); [DETAIL] S-1..S-6 | — |
| S-5 | MAJOR | SPEC | base | spec.md AC 5 | The spec does not say what the runner does when AC 5 refuses a checkpoint after verification passed. It could raise `CheckpointRolledBack` and restore the baseline, with the attempt either saved through `save_attempt` or lost, or raise `CallFailed` and leave the tree in place. Also unstated: whether the attempt counts as failed and the next route runs, and what line is written to findings.md. If a mismatch can only be seen after `git commit` has run (S-1 reading B), "does not create" also needs a decision on undoing the runner's own commit. | Opus | in spec — CheckpointRolledBack, attempt saved, counts as failed; [DETAIL] S-1..S-6 | — |
| S-6 | MINOR | SPEC | base | spec.md AC 6 ("refreshes a stamp for a checkpoint"); scripts/stage2.py:9589-9600 | If the refresh happens at the checkpoint, a refreshed document is committed with different bytes from the ones `prepare_derived` stamped and `make verify` or the targeted checks passed. The spec does not say whether a stamp-only difference after verification is acceptable, or whether the frontmatter gate (or more) must run again on the refreshed tree before the commit. | Opus | in spec — stamp-only diff accepted, frontmatter gate reruns; [DETAIL] S-1..S-6 | — |
