---
title: "Findings — isolated-writing-attempts"
category: findings
status: draft
implementation_status: none
date: 2026-11-24
created: 2026-11-24
last_reviewed: 2026-11-24
updated: 2026-11-24
supersedes: null
superseded_by: null
bead: coding-harness-s9r
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — isolated-writing-attempts

Stage-2 call, 2026-11-24: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1203 files, 5665 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/adr/0027-isolated-writing-attempts.md` +48 -0
> - `plans/changes/isolated-writing-attempts/design.md` +63 -0
> - `plans/changes/isolated-writing-attempts/plan.md` +68 -0
> - `plans/changes/isolated-writing-attempts/spec.md` +144 -0
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: not completed; gates none; not the full `make verify`; a fresh full `make verify` is still required before phase 6
> - the attempt left more than one new ADR file: `docs/adr/0026-isolated-attempts.md`, `docs/adr/0027-isolated-writing-attempts.md`
> ```

Stage-2 call, 2026-11-24: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1208 files, 5665 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/isolated-writing-attempts/design.md` +1 -1
> - `plans/changes/isolated-writing-attempts/plan.md` +1 -1
> - `plans/changes/isolated-writing-attempts/spec.md` +3 -3
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: not completed; gates none; not the full `make verify`; a fresh full `make verify` is still required before phase 6
> - the attempt left more than one new ADR file: `docs/adr/0026-isolated-attempts.md`, `docs/adr/0027-isolated-writing-attempts.md`
> ```

Stage-2 call, 2026-11-24: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.4 · reason two Codex draft attempts failed · leak check clean over 1208 files, 5666 commits, 12 rules.

> Attempt 3 (glm) failed its call: claude call failed: exit 1 ([claude-code:unrecognized_model] {"model":"glm-5.4","query_source":"sdk"})
>
> the attempt is saved at refs/stage2/attempts/isolated-writing-attempts/draft-attempt-3-20261124T171121272561Z (4d1b4c992f9b); `git diff d0e0ed6cc8c2 refs/stage2/attempts/isolated-writing-attempts/draft-attempt-3-20261124T171121272561Z` shows it.
>
> The runner put back:
> - `docs/adr/0027-isolated-writing-attempts.md`
> - `plans/changes/isolated-writing-attempts/design.md`
> - `plans/changes/isolated-writing-attempts/plan.md`
> - `plans/changes/isolated-writing-attempts/spec.md`

Stage-2 call, 2026-11-24: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1203 files, 5674 commits, 12 rules.

Stage-2 call, 2026-11-24: spec-review · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1207 files, 5681 commits, 12 rules.
## Phase 2a — fallback deepseek-v4.1-flash, 2026-11-24

Spec fingerprint: sha256:736f03a2e5598e2099b9e0e22055a3338b6e6d1584622cbc0010089401acebab

Spec review commit: acba01223a8a5cb459fa886824ad795fef8a11da

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| 2a-1 | [AMBIGUITY] | SPEC | base | spec.md criteria 11, 17, 19 | Criterion 17 refuses a start when the lane carries uncommitted or untracked changes, with no exception for the call that just failed, while criterion 19 has draft and implement run through the lifecycle with isolation disabled in PR 1 and criterion 11 demands their fall-through. Reading A: 17 governs isolated attempts only, so a non-isolated fall-through starts on the lane tree the failed call left dirty; then "starts from the saved state" is empty for those verbs (criterion 14 saves state for isolated attempts only) and the next route inherits the failed bytes. Reading B: 17 governs every attempt in the lifecycle, so the first failed draft or implement call in PR 1 refuses its own fall-through and criterion 11 cannot be met for draft and implement before PR 2. The spec settles neither. | deepseek-v4.1-flash | open | — |
| 2a-2 | [AMBIGUITY] | SPEC | base | spec.md criteria 3, 17 | "Tracked and untracked files" has two readings for the same words in both criteria. Reading A: untracked means the entries `git status --porcelain` reports, so `.venv`, `node_modules`, `tools/pi/node_modules` and test caches stay outside the check. Reading B: every path no commit tracks counts, ignored ones included; then nearly every lane refuses every attempt, and criterion 3 rejects an attempt in which Python merely wrote a `__pycache__` into the linked `.venv`. The two readings differ in whether the change works at all and in what a test must assert. | deepseek-v4.1-flash | open | — |
| 2a-3 | [AMBIGUITY] | SPEC | base | spec.md criteria 3, 16, 17, 18 | "Runner-owned records" is used by three criteria and enumerated nowhere; the file it names, `findings.md`, also carries reviewer rows, statuses, human notes and orchestrator edits. Reading A: whole files are exempt, so a model that rewrites the lane's findings prose is accepted, and criterion 3 cannot go red for that file. Reading B: only the runner's own blocks and marks are exempt, so the check needs a byte-level boundary between runner blocks and everything else in the same file, and criterion 16 requires the runner to write inside that boundary mid-run. Which files, and which spans of them, count is left to the implementer. | deepseek-v4.1-flash | open | — |
| 2a-4 | [AMBIGUITY] | SPEC | base | spec.md criteria 11, 13 | The two criteria overlap on one input. A model that deletes the `Makefile` or breaks an import in `scripts/stage2.py` makes verification unstartable: criterion 11 sends "its post-run checks are red" to the next route, criterion 13 stops the run on "an unstartable verification". Reading A: unstartable wins, one attempt ends the run. Reading B: unstartable is a red post-run check and the next route starts. The spec names both triggers and gives no precedence, so the count of model calls in a run depends on which is chosen. | deepseek-v4.1-flash | open | — |
| 2a-5 | [AMBIGUITY] | SPEC | base | spec.md criteria 9, 13 | Criterion 9 says the runner stops when "either restored checksum still differs" and names no basis for the comparison. Reading A: compare against the checksum taken before the attempt; a fresh `make venv` and `tools/pi/install.sh` do not reproduce a byte-identical environment (build ids, timestamps, resolved versions), so restoration is ineffective on the first rejection and every environment rejection stops the run, making the rebuild path a stop before a stop. Reading B: rebaseline the restored environment; then an ineffective restoration is never detected and criterion 13's "ineffective restoration" cannot go red. | deepseek-v4.1-flash | open | — |
| 2a-6 | [AMBIGUITY] | SPEC | base | spec.md criteria 8, 9 | Criterion 8 does not say which object carries the read-only permissions. Reading A: set on the link inside the attempt worktree; a symlink's own mode is ignored on Linux and macOS, so ordinary writes through the link still succeed and the criterion's refutation always holds. Reading B: set on the lane's `.venv` and Pi themselves, which makes the shared lane environment non-writable for the duration; the spec then says nothing about who restores the write bit after a rejection, after an accepted attempt, or after a crashed runner, and a lane left read-only is one no later `make venv` or `make verify` can use. | deepseek-v4.1-flash | open | — |
| 2a-7 | [AMBIGUITY] | SPEC | base | spec.md criteria 2, 3, 11, 13 | Criterion 3 ends with "rejects the attempt" and does not say what rejection does to the run, while criterion 13 lists the stopping causes and omits it. Reading A: a lane change ends the run as an internal failure, since the lane is no longer trusted for a pinned base. Reading B: it falls through like a model failure, with the next route in a new worktree from the saved state. Two builds follow, and a test written against one reading fails against the other. | deepseek-v4.1-flash | open | — |
| 2a-8 | [AMBIGUITY] | SPEC | base | spec.md criteria 6, 7, 21 | The spec fixes where the worktree lives (criterion 4) but never where the invocation record, the process-id lock and the saved-state index are written, and criterion 5's "record keys scanned" names a term the spec does not define. Reading A: they sit in the state directory beside the worktrees, outside the repository and outside every lane. Reading B: they sit inside each attempt worktree or in the lane's git directory. The two differ for worktree discovery, for whether those records make the lane dirty under criteria 3 and 17, and for what a foreign harness can find after the worktree is removed by criterion 14. | deepseek-v4.1-flash | open | — |
| 2a-9 | [AMBIGUITY] | SPEC | base | spec.md criteria 1, 6, 9, 19 | "Isolation disabled" is defined only by contrast and the criteria do not say what the lifecycle still does in that mode. Reading A: only the worktree is skipped; checksums, the invocation record, the lock and the lane check still run, so PR 1's draft and implement keep their damage detection. Reading B: the whole isolation is off, and PR 1's draft and implement only route their call through the module, keeping the lane writes and the manual clean-up the change exists to end. The damage exposure of the first pull request depends on the reading. | deepseek-v4.1-flash | open | — |
| 2a-10 | [AMBIGUITY] | SPEC | base | spec.md criterion 20, Non-goals, Definition of Done | "The later rollout" is claimed and disclaimed at once. Reading A: criterion 20 and the DoD's later-rollout evidence ship in this change, and the Non-goals move only the evidence gate that decides PR 2, so the evidence named in the DoD has no criterion here to judge it. Reading B: PR 2 is itself one of the follow-up changes, criterion 20 describes code this change does not contain and can never go red in it, and the DoD asks for evidence in a pull request this change does not produce. | deepseek-v4.1-flash | open | — |
| 2a-11 | MAJOR | SPEC | base | spec.md criterion 18 | Criterion 18 cannot go red as written. It is satisfied by either of two commits joined by "or", and the second, the orchestrator's records commit, happens outside the runner and outside any test the change can write; a run that leaves the records uncommitted in the lane satisfies neither commit yet is indistinguishable from one whose orchestrator will commit them later. No input and no state refutes it without a defined observable (for example the record present in the tree of the next landing commit), so it states an intention rather than a criterion. | deepseek-v4.1-flash | open | — |
| 2a-12 | [AMBIGUITY] | SPEC | base | spec.md criterion 22 (with decisions Q-5, Q-8) | "The doctrine" is not named down to sentences, and the decisions disagree about which they are: Q-5 amends the `docs/WORKFLOW.md` section 3 sentence, Q-8 the section 4 sentences "The runner is the only way" and "a failed call stops". Reading A: only section 4 changes, and the section 3 sentence that "a failed model process stops instead of silently changing route" stands unchanged, so the doctrine still contradicts criterion 11 while a document test on section 4 is green. Reading B: both sections change. The spec names files only, and the DoD repeats the file list. | deepseek-v4.1-flash | open | — |

Stage-2 call, 2026-11-24: spec-review · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1207 files, 5688 commits, 12 rules.
## Phase 2a — fallback deepseek-v4.1-flash (Opus re-check of the fallback review, same round), 2026-11-24

Spec fingerprint: sha256:736f03a2e5598e2099b9e0e22055a3338b6e6d1584622cbc0010089401acebab

Spec review commit: 914fe2be657aaa77ae09d609d72d182246399f4e

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| 2a-13 | [AMBIGUITY] | SPEC | base | spec.md criteria 3, 17 | "Tracked and untracked files" is undefined at the boundary that decides whether the change works at all. Reading A: untracked means what `git status --porcelain` lists, so ignored paths stay outside the check — and `.venv/` is gitignored in this repository (`.gitignore:30`), as is `tools/pi/node_modules/`. Reading B: every path no commit tracks counts, ignored ones included; then criterion 17 refuses any lane that carries a `.venv` (no attempt ever starts) and criterion 3 rejects an attempt in which Python merely wrote a `__pycache__` through the linked environment. The two readings differ in whether any attempt can run and in what a test asserts. | deepseek-v4.1-flash | open | — |
| 2a-14 | [AMBIGUITY] | SPEC | base | spec.md criteria 3, 16, 17, 18 | "Runner-owned records" drives four criteria and is enumerated nowhere; the file the criteria point at, `findings.md`, also carries reviewer rows, status cells, human notes and orchestrator edits. Reading A: whole files are exempt, so a model that rewrites the lane's findings prose or `plan.md` is accepted and criterion 3 can never go red for those files. Reading B: only the runner's own blocks, audit lines and marks are exempt, so the check needs a byte-level boundary inside one file and criterion 16 has the runner writing into that boundary mid-run. | deepseek-v4.1-flash | open | — |
| 2a-15 | [AMBIGUITY] | SPEC | base | spec.md criteria 9, 13 | Criterion 9 stops the run when "either restored checksum still differs" and names no basis for the comparison. Reading A: compare against the checksum taken before the attempt; a fresh `make venv` plus `tools/pi/install.sh` does not reproduce a byte-identical tree, so every environment rejection stops the run and criterion 11's "clean baseline after an environment checksum rejection" is unreachable. Reading B: rebaseline after the rebuild; then criterion 13's "ineffective restoration" can never go red. | deepseek-v4.1-flash | open | — |
| 2a-16 | [AMBIGUITY] | SPEC | base | spec.md criteria 8, 9 | Criterion 8 says "file permissions make its linked lane environment and Pi read-only" and never names the object that carries the mode. Reading A: the mode goes on the link inside the attempt worktree; a symlink's own mode is ignored on Linux and macOS, so ordinary writes through the link still succeed and the criterion's refutation holds by construction. Reading B: the mode goes on the lane's `.venv` and Pi themselves; then criterion 9's rebuild and reinstall need the write bit back, no criterion says who restores it after an accepted attempt, a rejection or a killed runner, and a lane left read-only fails the next `make verify`. | deepseek-v4.1-flash | open | — |
| 2a-17 | [AMBIGUITY] | SPEC | base | spec.md criteria 11, 13 | One input satisfies both triggers and the criteria give no precedence: a model that deletes the `Makefile` or breaks an import in `scripts/stage2.py` makes verification unstartable, which criterion 11 calls "its post-run checks are red" (next route starts) and criterion 13 calls "an unstartable verification" (whole run stops). Reading A: unstartable wins, one model call ends the run. Reading B: unstartable is a red post-run check and the next route starts. The number of model calls in a night follows from the choice, and a test written for one reading fails for the other. | deepseek-v4.1-flash | open | — |
| 2a-18 | [AMBIGUITY] | SPEC | base | spec.md criteria 3, 13, 15 | Criterion 3 ends in "rejects the attempt" and criterion 13's stop list omits a lane change, so what a lane-change rejection does to the run is open. Reading A: it stops the run, since the lane is no longer a trusted pinned base. Reading B: it falls through like a model failure, the next route starting from the saved state in a new worktree. Criterion 15 stops explicitly for a moved lane, which reads as evidence for A and as a contrast that leaves B open for criterion 3. | deepseek-v4.1-flash | open | — |
| 2a-19 | [AMBIGUITY] | SPEC | base | spec.md criteria 1, 19 | "Isolation disabled" is defined only by contrast, and no criterion says what the lifecycle still does in that mode — the mode PR 1 ships draft and implement in. Reading A: only the worktree is skipped, while checksums, the invocation record, the lock and the lane check still run, so PR 1's draft and implement keep the damage detection. Reading B: the whole isolation is off and PR 1 only routes the call through the module, keeping the lane writes and the hand clean-up the change exists to end. Criterion 1's refutation ("starts its model outside that lifecycle") is judged differently under the two. | deepseek-v4.1-flash | open | — |
| 2a-20 | [AMBIGUITY] | SPEC | base | spec.md criterion 20, Non-goals, Definition of Done | The later rollout is claimed and disclaimed at once. Reading A: PR 2 is in this change, so criterion 20 can go red here; then the DoD's "later rollout evidence" is judged by no criterion, and the gate that authorises it was moved out by Q-25 into a follow-up bead that has not landed. Reading B: PR 2 is a follow-up too, so criterion 20 describes code this change does not contain and can never go red in it, while the DoD still asks for evidence in a pull request this change does not produce. | deepseek-v4.1-flash | open | — |
| 2a-21 | [AMBIGUITY] | SPEC | base | spec.md criterion 22, Definition of Done (with docs/WORKFLOW.md §4, docs/adr/0017-codex-repairs-taken-findings.md) | "The doctrine" is not named down to files and sentences, and the rule lives in at least three places: `docs/WORKFLOW.md` §4's repair section ("a failed call stops the run without a fallback", line 2110), ADR 0017 decision 2 ("A model call failure stops", line 85), and the AGENTS.md Stage-2 paragraph that cites ADR 0017. Reading A: only `docs/WORKFLOW.md` changes; ADR 0017 decision 2 then still requires the stop criterion 11 forbids, while a document test over WORKFLOW.md is green. Reading B: WORKFLOW.md and ADR 0017 both change, the latter through the new ADR's partial supersession. decisions Q-5 and Q-8 name different sections (§3 and §4); both sentences sit in §4 of the current file. | deepseek-v4.1-flash | open | — |
| 2a-22 | [AMBIGUITY] | SPEC | base | spec.md criteria 5, 6, 14, 21 | The invocation record, the process-id lock and the saved-state index get a schema (criterion 21) but no place and no lifetime, and criterion 5's "record keys scanned" names a term the spec never defines. Reading A: they sit in the state directory beside the worktrees, outside the repository and outside every lane. Reading B: they sit inside each attempt worktree or in the lane's git directory; criterion 14's worktree removal then destroys the lock and the saved-state index that prune and the next route read, and their presence decides whether the lane reads dirty under criteria 3 and 17. | deepseek-v4.1-flash | open | — |
| 2a-23 | MAJOR | SPEC | base | spec.md criterion 18 | Criterion 18 cannot go red as written. It is satisfied by either of two commits joined by "or"; the second, the orchestrator's records commit, happens outside the runner and outside any test this change can write, and a run that leaves the records uncommitted in the lane satisfies neither while being indistinguishable from one whose orchestrator will commit them later. No input and no state refutes it without a defined observable (for example the record present in the tree of the next landing commit). | deepseek-v4.1-flash | open | — |
| 2a-24 | [AMBIGUITY] | SPEC | base | spec.md criteria 3, 15, 16 | Criterion 3 requires the lane's files unchanged when an isolated attempt ends, criterion 15 lands the accepted checkpoint on the lane HEAD — which changes the lane's tracked files — and criterion 16 writes lane records immediately after a failed attempt. Nothing fixes the order of the lane check against the landing commit or against those record writes. Reading A: the check runs before landing and covers only the model's damage. Reading B: it runs at the end of the whole lifecycle, exempting the landed checkpoint and the records as runner-owned; criterion 3's red case then includes a landing that carried more than the attempt's tree. | deepseek-v4.1-flash | open | — |
