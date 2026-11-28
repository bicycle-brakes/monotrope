---
title: "Findings — bead-topic-in-research"
category: findings
status: draft
implementation_status: none
date: 2026-11-28
created: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-5vts
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — bead-topic-in-research

Stage-2 call, 2026-11-28: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1325 files, 6163 commits, 12 rules.

Stage-2 call, 2026-11-28: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1328 files, 6165 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-28

Spec fingerprint: sha256:06199c762fbbd970347507a1bdb93f04e1b5163ca5e1ed8da6754a7916a16550

Spec review commit: 6601cce77f3812e1b1eb3ea35497a1550ad862f9

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | MAJOR | SPEC | base | spec.md, AC1 ("the description differs from the tracker text"); AC4 | [AMBIGUITY] Reading A: copy the description byte-for-byte as Markdown. Then any Markdown or runner syntax in the description becomes part of research.md's structure. An unclosed ``` or ~~~ fence hides everything after it from `stage2.research_visible_text`, so `research_census.publication_evidence` no longer sees the later `Stage-2 call, … explore` line or the `## Runner exploration —` heading. A `<!-- research-swarm/v2 …` line is read as a run envelope, which is exactly what `stage2.quote_research_records` defuses in model text. `##` lines split the topic section. Reading B: trim, quote, fence or escape the text so the file keeps its structure. But then the written text differs from the tracker text, and AC1 as written goes red. The spec picks neither reading. It is also silent on leading or trailing whitespace, CRLF and indentation in a non-empty description. | Opus | in spec — description written as a blockquote; [DETAIL] S-1..S-3 (bounded standing grant) | — |
| S-2 | MINOR | SPEC | base | spec.md, AC1 ("an existing open bead"); AC6 | [AMBIGUITY] Reading A: "open" means any status other than closed, matching AC6, which refuses only `closed`. Then the topic section is also required for `in_progress`, `blocked` or `deferred` beads. Reading B: the literal tracker status `open`. Then no criterion covers creation for a claimed (`in_progress`) bead, and an implementation or test set that writes the topic only for `open` passes every criterion. | Opus | in spec — reading A (every status but closed); [DETAIL] S-1..S-3 | — |
| S-3 | MINOR | SPEC | base | spec.md, AC1 and AC2 ("tracker description"); research.md, "What is unclear", first two bullets | The spec does not name the export field the text is read from. research.md says it is unverified whether an export row carries a description at all, and under which key (`plans_registry._bead_statuses` keeps only `id` and `status`). So the implementer has to decide three things. Which key is read. Whether other text fields of a tracker record (design, acceptance criteria, notes) belong to the topic. And whether a key that is present with a non-string value (null, number, list) counts as "absent" under AC2 or as a refusal. | Opus | in spec — description key of the export row only, absence named; [DETAIL] S-1..S-3 | — |
