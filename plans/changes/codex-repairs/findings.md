---
title: "Findings — codex-repairs"
category: findings
status: draft
implementation_status: none
date: 2026-10-13
created: 2026-10-13
last_reviewed: 2026-10-13
updated: 2026-10-13
supersedes: null
superseded_by: null
bead: coding-harness-0ga
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — codex-repairs

Stage-2 call, 2026-10-13: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 410 files, 1020 commits, 12 rules.

ADR answer owed: decisions/answers/codex-repairs/adr.yaml does not exist and the gate tolerated that for this run; the answer is the maintainer's (python3 scripts/harness.py decide adr).

Stage-2 call, 2026-10-13: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 416 files, 1022 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-10-13

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | MAJOR | SPEC | base | `spec.md`, criterion 18, Protected areas, Definition of Done; `decisions.md`, Q-1; `research.md`, "The reviewer's own findings" | [AMBIGUITY] It is not said which `review` runs start fresh. Today `review` resumes a recorded Codex phase-2a session on every run, a second run after a repair included (`recorded_2a_session`, then `run_codex(..., resume=recorded)`), so that thread also holds the first verdict. ADR 0016 decision 6 and the Session paragraph of `prompts/06-review.md` state the resume as the rule, and three change folders under `plans/changes/` hold such a session line. Reading 1: no phase-6 verdict call resumes anything any more. The first review of such a change then changes too, and ADR 0016 decision 6 and `prompts/06-review.md` become false, while the spec protects the other ADRs and leaves that prompt out of the files the pull request carries. Reading 2: the first phase-6 review still resumes the 2a session and only a re-check is fresh. The runner then needs a rule for what makes a run a re-check — an earlier `## Phase 6` block, a phase-6 row with Status `fixed`, a `repair` audit line — and the spec gives none; the three differ for a second `review` after a repair of loop rows only. Q-1's "as `review` already starts one after a repair" holds only where no Codex phase-2a session is recorded. (criterion 18) | Opus | taken — not a test — spec criterion 18 amended: a re-check is a `review` run after an earlier `## Phase 6` block; the first review keeps ADR 0016's rule | — |
| F-2 | MAJOR | SPEC | base | `spec.md`, criteria 3, 17 and 20, Definition of Done | Nothing says what a Codex repair attempt is told about commands and commits. Every repair prompt today carries "with the available file tools; you cannot run commands" (`REPAIR_FORMAT` in `scripts/stage2.py`) and "you have file tools but no command tool" (`prompts/04-implement.md`, the body that `implement` and the Sonnet attempt also receive, where the sentence is true). The spec keeps "the existing repair-input contract", forbids a claim that Codex lacks command tools, and stops the whole run when a Codex call moves HEAD. It leaves three things to the builder: whether Codex may run tests or `make verify` itself, whether it is told not to commit and to run no git command that changes the repository (as a draft is), and whether the prompt differs between the Codex attempts and the Sonnet attempt. No criterion goes red on any answer: criterion 20 reaches the sentence in the phase prompt but names only the runner's help and comments, not the `REPAIR_FORMAT` text it sends, and nothing covers an instruction about committing. (criteria 3, 17, 20) | Opus | taken — not a test — spec criterion 20 amended: the Codex repair text allows tests and `make verify`, forbids commits and repository-changing git commands; Sonnet's sentence stays | — |
| F-3 | MINOR | SPEC | base | `spec.md`, Terms ("Post-run failure", "Call failure"), criteria 4 and 6; `decisions.md`, Q-4 | [AMBIGUITY] A model call that ends with exit 0 and an empty answer is sorted nowhere. The Terms name a call failed when the answer file or the thread event is missing and say nothing of an answer that is there and empty. Reading 1: a call failure, as the runner treats an empty answer on the Claude Code path today (`run_work_model`, "the answer is empty") — the run stops, the baseline is restored, no further attempt starts. Reading 2: a completed call whose answer the repair-answer check rejects ("no fixed line"), which is what `run_codex` as it stands would hand on — a second Codex attempt starts on the first one's tree, and Sonnet after it. Q-4 chose against a switch to Sonnet "when Codex does not answer"; under reading 2 a Codex that returns nothing twice reaches Sonnet without `--stage2-off`. (criteria 4 and 6) | Opus | taken — not a test — spec Terms amended: an empty answer is a call failure | — |
