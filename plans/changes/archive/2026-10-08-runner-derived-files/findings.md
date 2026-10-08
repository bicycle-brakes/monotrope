---
title: "Findings — runner-derived-files"
category: findings
status: accepted
implementation_status: done
date: 2026-10-08
created: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-08
supersedes: null
superseded_by: null
bead: coding-harness-mfv
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — runner-derived-files

Stage-2 call, 2026-10-08: spec-review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 299 files, 675 commits, 12 rules.

## Phase 2a — Codex, 2026-10-08

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | MAJOR | SPEC | base | spec.md:34–37, criteria 4–5 | [AMBIGUITY] If the index renderer exits nonzero after an otherwise valid Flash attempt, two readings satisfy criterion 4: return diagnostics to the repair flow, triggering another model call within the existing retry limits; or terminate the run immediately, triggering no further attempt. Both skip verification/checkpoint and remain red. Criterion 5 requires repair for real test failures but does not settle continuation after preparation failures. | Codex | resolved — maintainer confirmed existing repair attempts on 2026-10-08; criterion 4 and decisions.md record the answer | — |

Reviewer session: codex 01a11b11-e83e-7741-a824-70da82915b88

Stage-2 call, 2026-10-08: review-loop · endpoint glm-coding-plan · model glm-5.3 · leak check clean over 301 files, 676 commits, 12 rules.

Stage-2 call, 2026-10-08: review-loop · endpoint glm-coding-plan · model glm-5.3 · leak check clean over 301 files, 681 commits, 12 rules.

Stage-2 call, 2026-10-08: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 301 files, 682 commits, 12 rules.

## Phase 6 — Codex, 2026-10-08

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-2 | BLOCKER | SPEC | base | scripts/stage2.py:1191–1206 | A tracked `plans/INDEX.md` hard-linked to a clean unheld file passes the `resolve()` checks. When an attempt adds findings.md, the real renderer overwrites both paths, corrupting the unheld file’s body, while preparation returns success. Reproduced with both linked files initially clean. Aliased paths must be refused before writing. [Criterion 2] | Codex | repaired — hardlink refusal regression for document and index; both failed before repair; resolved by blocker-free Codex re-review | no |
| F-3 | BLOCKER | SPEC | base | scripts/stage2.py:1186; scripts/stage2.py:912–915 | With `OPENAI_API_KEY` in the caller environment, both preparation Git commands inherit that key: `changed_paths()` calls `_git_output()`, whose subprocess calls omit `env`. The sanitized environment reaches only the renderer. Reproduced with a planted key; the credential test intercepts only `launch()` and misses these Git calls. Preparation commands must receive no model secrets. [Criterion 3] | Codex | repaired — preparation Git environment regression failed before repair; explicit sanitized environment added; resolved by blocker-free Codex re-review | no |
| F-4 | BLOCKER | SPEC | base | scripts/stage2.py:1187–1217 | An attempt that writes `paths: [null]` to provenance.yaml and changes a held document causes `is_held()` to raise `AttributeError`. `load_map()` accepts the list, and preparation does not catch this exception. Reproduced: `verify_attempt()` raises instead of returning diagnostics, terminating implementation before the existing repair attempts can run. Preparation failures must return bounded, scrubbed diagnostics and enter the repair flow. [Criterion 4] | Codex | repaired — three malformed-path-map regressions failed before repair; records validated before use; resolved by blocker-free Codex re-review | no |

Phase 6 verdict: codex 01a11b11-e83e-7741-a824-70da82915b88, 2026-10-08

## Phase 4b — GLM loop rows, released 2026-10-08

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MAJOR | SPEC | criterion 4 | spec.md:34-37; findings.md:28; scripts/stage2.py:1372-1382 | The shipped code settles an ambiguity the change itself leaves open: findings.md row F-1 records two readings of criterion 4 (after a preparation failure, retry within the existing attempt limits or stop the run at once) with status open, and the handover says the maintainer's answer was still pending and the spec gate must not be marked green until it is recorded — yet the implementation commits to the retry reading, so a deterministic renderer failure now burns the Flash repair and the Sonnet fallback on identical diagnostics before the run fails. Record the decision and close F-1, or make criterion 4 name the wanted behaviour. | GLM | taken — maintainer confirmed existing repair flow on 2026-10-08; criterion 4 and renderer-repair limit regression | no | disagree — F-1 is resolved, and criterion 4 explicitly records the maintainer-confirmed repair flow and attempt limits. |
| L1-2 | MINOR | SPEC | criterion 3 | scripts/stage2.py:1196; tests/test_stage2.py:770-868 | Criterion 3 promises that no preparation command receives model secrets, but nothing measures it: the index renderer runs as a direct subprocess that no stand-in records, so no test ever asserts its environment, and a later edit routing a credential-bearing environment into preparation would stay green. The construction looks clean (the allow-listed verify environment, the key passed only for scrubbing), but the promise is held by reading, not by a test. | GLM | taken — test_preparation_commands_receive_no_model_or_caller_credentials | no | disagree — A regression now asserts the renderer’s environment; the remaining Git credential inheritance fault is F-3. |
| L1-3 | MINOR | MAINT | code | scripts/stage2.py:1185,1197-1202 | A git failure inside preparation escapes the bounded-diagnostics contract: changed_paths raises Refused (say a concurrent index lock between the preflight call and verification), which the except tuple does not list, so instead of a bounded preparation diagnostic reaching the repair flow the whole verb aborts as a refusal after the model call — the wrong exit class for a post-call problem — leaving that attempt's edits uncommitted and never offered for repair. | GLM | taken — test_git_failure_in_preparation_is_a_bounded_scrubbed_diagnostic | no | disagree — Preparation now catches Refused and returns bounded, scrubbed diagnostics; its regression passes. |
| L1-4 | MINOR | MAINT | base | docs/journal/handover/2026-10-08-runner-derived-files.md:37-38 | The handover's evidence count does not match the diff: it reports seven new focused regressions passed, while the change adds exactly six test functions (first-attempt refresh, stamp scope, retry order, renderer failure, invalid UTF-8, outside-worktree refusal); a maintainer resuming from the handover counts six and hunts for a seventh test that does not exist. | GLM | taken — handover distinguishes six new regressions from seven selected cases | no | disagree — The handover now distinguishes six new regressions from seven selected cases, including one existing test. |
| L1-5 | MINOR | SPEC | base | plans/changes/runner-derived-files/plan.md:48-49 | The change's own plan leaves the measured-span section under its time heading empty although implementation_status is partial and the handover reports tests written and run: the time record the implement route enforces on every other change was never kept here, so the stated appetite went untracked and the plan artefact contradicts the discipline this very change wires into the runner. | GLM | rejected — snapshot preceded measured phase-4 end; plan records 10:31:06–10:48:08 UTC |  | disagree — The plan now records four measured spans under “Time used.” |
| L2-1 | MINOR | MAINT | impl | scripts/stage2.py:1185-1194 | The stamp loop raises at the first offending document in sorted order and returns one refusal, so an attempt that leaves several refused paths (one aliased plus one unreadable document) burns one repair attempt per path and can exhaust the whole attempt budget with `make verify` never started; the loop already visits every changed path and could collect all offenders into the single bounded diagnostic. | GLM | taken — test_preparation_collects_all_document_refusals_in_one_bounded_diagnostic | no | disagree — Document refusals are now collected into one bounded diagnostic; the multiple-refusal regression passes. |
| L2-2 | MINOR | MAINT | impl | scripts/stage2.py:1216-1228 | `verify_attempt` now stamps held documents and runs the index renderer — writes to the tree and execution of repository code the model just edited — before `make verify`, but its docstring still says only "Run `make verify` and return bounded diagnostics", so a later caller reusing the helper (the contemplated review-loop integration) would get tree mutations its documented contract does not mention. | GLM | taken — verify_attempt docstring names preparation writes and execution | no | disagree — The docstring now explicitly describes stamping, index rendering, tree writes and renderer execution. |

Rounds run: 2

Stage-2 call, 2026-10-08: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 301 files, 683 commits, 12 rules.

Stage-2 call, 2026-10-08: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 301 files, 685 commits, 12 rules.

## Phase 6 — Codex, 2026-10-08

Codex reported no finding.

The answer was not only six-cell rows; what is not one is kept below as it came.

No findings: checked all acceptance criteria, the F-2–F-4 repairs and their counterexamples; all 222 runner tests passed.

Phase 6 verdict: codex 01a11b11-e83e-7741-a824-70da82915b88, 2026-10-08
