---
title: "Findings — runner-stamps-provenance"
category: findings
status: draft
implementation_status: none
date: 2026-11-16
created: 2026-11-16
last_reviewed: 2026-11-16
updated: 2026-11-16
supersedes: null
superseded_by: null
bead: coding-harness-f9sv
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — runner-stamps-provenance

Stage-2 call, 2026-11-16: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1101 files, 4461 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: red; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: ` [… 45 characters left out …]
> - plans/changes/runner-stamps-provenance/spec.md is missing after the draft.
> - plans/changes/runner-stamps-provenance/plan.md is missing after the draft.
> ```

Stage-2 call, 2026-11-16: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1102 files, 4461 commits, 12 rules.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/runner-stamps-provenance/spec.md` +72 -0
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: red; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: ` [… 45 characters left out …]
> - plans/changes/runner-stamps-provenance/plan.md is missing after the draft.
> ```

Stage-2 call, 2026-11-16: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 1103 files, 4461 commits, 12 rules.

> Attempt 3 (glm): the runner put back what a draft may not change:
> - `plans/INDEX.md`

Stage-2 call, 2026-11-16: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1104 files, 4464 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-16

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | BLOCKER | SPEC | base | `spec.md`: goal sentence, Problem 1, AC 1–3, Definition of Done (migration script, "Special runs") and Open decisions (the migration [DETAIL] and the bead [GAP]), compared with `decisions.md` Q-4 | The spec contradicts the maintainer's answered Q-4 ("teilen"), which was recorded in commit 7ce29215 after the draft commit 516da7d2. Q-4 says this change stamps `produced_by` (program, model, publication date) after explore, draft and repair, and makes every verb's post-run check refuse a failing producer header in the files that run touched. Q-4 moves the migration and the tree-wide check to coding-harness-2i7x. The spec differs in five ways: (a) it stamps after `draft` only (AC 1). (b) It adds a tree-wide check over every artifact, live and archived, to `plans-registry` (AC 2). (c) It migrates every header (AC 3, DoD `scripts/migrate_producer_headers.py`, "Special runs"). (d) It counts "50 research.md headers", where Q-4 counts 271 of 620 producer headers under `plans/` failing. (e) It keeps a [GAP] about the bead's content that `decisions.md` already answers, and lets that scope enter later as an amendment during implementation. Built as written, AC 2 without the migration turns open lanes red, which is the reason Q-4 split the change. The explore and repair stamps and the per-run check that Q-4 keeps have no criterion at all. | Opus | open | — |
| F-2 | MAJOR | SPEC | base | AC 1; `research_publication` / `research_header_producers` in `scripts/stage2.py` (the helper the stamp generalizes) | [AMBIGUITY] AC 1 does not say what the stamp does with a `produced_by` that is already in the header. Reading A, the generalized `research_publication` behaviour: existing records are kept (legacy forms are normalised through `research_header_producers`) and the runner's record is appended. The drafting session's self-description, which may name the wrong program or model, then stands beside the truthful record, and an earlier draft's producer stays in the list. Reading B, replace: the header carries only the accepting attempt's runner record, and the producer of an earlier draft or attempt is lost. That loss is real, because a later draft attempt starts on the tree the failed one left: in this change, attempt 2 (codex) wrote `spec.md` +72 lines and attempt 3 (glm) was accepted. The two readings give different headers for every draft and different test expectations. | Opus | open | — |
| F-3 | MAJOR | SPEC | base | AC 1, "Refuted by" | AC 1 cannot go red on what the change exists for, a truthful producer. Its refutation names only a free-form value or an unknown program name. A stamp that writes the same known record on every draft (for example `{kind: llm-session, name: pi, version: <today>}`), names `codex` after the GLM route was accepted, or leaves out or misstates `model` passes it. Q-4 requires program, model and publication date. No input and state are given that would refute a well-formed but false stamp, for example: GLM route accepted, so the record must read `name: claude-code`, `model: glm-5.3`, `version: <run day>`. | Opus | open | — |
| F-4 | MAJOR | SPEC | base | AC 1; `draft()` in `scripts/stage2.py` (`verify_draft` runs before `checkpoint`) | Missing: where in a draft attempt the stamp runs, and whether a failed attempt's files are stamped. `draft()` runs `verify_draft`, whose document checks include the `plans-registry` block gate, and then commits. If the stamp runs before verify, the gate checks the stamped bytes. If it runs after verify (for example at the checkpoint), then with AC 2 in `plans-registry`, every draft whose session wrote a free-form header fails its post-run check before the stamp can fix it, so the attempt is retried or the run fails. The spec also does not say whether a failed attempt's artifacts are stamped before the next attempt starts on that tree. | Opus | open | — |
| F-5 | MAJOR | SPEC | base | AC 1 ("whichever form the drafting session wrote"), AC 4 | Missing: what happens when a header cannot be stamped. The helper the stamp generalizes raises `Refused` on non-UTF-8 bytes, missing frontmatter, YAML anchors or aliases, a header that is not a mapping, and a legacy `produced_by` it cannot interpret (`ValueError` from `research_header_producers`). The spec does not say whether such a refusal fails the attempt with a diagnostic and moves to the next route, stops the whole draft run, or makes the runner write a header. It also does not say where a missing field goes when the header has no `tags:` line. | Opus | open | — |
| F-6 | MAJOR | SPEC | base | AC 1 scope; `draft_keep()` in `scripts/stage2.py` | Missing: which draft-published files are stamped besides `spec.md`, `design.md` and `plan.md`. `draft_keep()` keeps every changed path under the change folder except `decisions.md`, plus the new ADR file under `docs/adr/`. Examples are `research.md`, `findings.md`, or an extra file such as `plans/changes/stage2-session/adr-0007-session-amendment.md`. AC 1 leaves those with the session's hand-written header. AC 2, or Q-4's check of the files a run touched, then makes the draft red on them. For the ADR outside `plans/`, nothing checks it. | Opus | open | — |
| F-7 | MAJOR | SPEC | base | AC 2; Terms "metadata contract" and "free-form header"; `metadata_problems()` in `scripts/research_census.py` | [AMBIGUITY] It is unclear what "the metadata contract's record form" includes. Reading A: only the per-record shape the Terms list (`kind`, `name` in `PROGRAMS`, ISO `version`, optional non-empty `model`). Reading B: the "contract reader exposed" from `research_census.py`, that is `metadata_problems()`. Reading B also requires `kind == llm-session` (the Terms' free-form list does not name a wrong `kind`), `provenance: ai-drafted-reviewed`, a pending `review`, exactly one of each field, and every producer `version` inside `date..updated`. Under B, a well-formed record whose `version` precedes its `date`, or a `human-written` artifact that carries a record, is red; under A both are green. Because AC 1 stamps only four fields, under B a stamped draft whose session wrote a later `date` or `last_reviewed` still fails. | Opus | open | — |
| F-8 | MINOR | SPEC | base | AC 2, AC 3; Open decisions, first [DETAIL]; `artefacts()` in `scripts/plans_registry.py` | AC 2 and AC 3 cover "any Markdown artifact under plans/", and the [DETAIL] says the gate "already walks every Markdown artifact". `artefacts()` actually skips `_README.md`, `INDEX.md` and every file whose name starts with `_`. A free-form header in `plans/_README.md` (which has a `produced_by` today) or in a `_`-prefixed file in a change folder would therefore stand while `make verify` stays green. That refutes AC 2 as worded unless the walk is widened, and the spec does not decide whether it is. | Opus | open | — |
| F-9 | MINOR | SPEC | base | AC 1 (`review` stamped to the contract's pending form); Non-goal "No automation of approval" | [AMBIGUITY] It is unclear what a re-draft does to an artifact a human has approved. Reading A: the stamp resets `review` to pending, because the content changed and needs approval again. Reading B: the stamp keeps the human's approval, as the non-goal ("`review: approved` stays a human edit") suggests. AC 1 forces A without saying so. No artifact under `plans/` is approved today, but `draft` can run again on a change whose earlier draft is committed. | Opus | open | — |
