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

Stage-2 call, 2026-11-28: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1328 files, 6167 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-28

Spec fingerprint: sha256:00cae96f9abb2a598747828a899a10bf5cee33eab2a9a10228f8ca3520c36325

Spec review commit: 657d0b6a150880a7572a7b53c18034a9193526a2

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-4 | MAJOR | SPEC | fix-r1 | spec.md, Open decisions, [DETAIL] S-1 ("every line prefixed with `> `"); scripts/stage2.py::research_visible_text; scripts/check_research_handoff.py::_lines | [AMBIGUITY] The spec does not say which line break "every line" means, and the code that reads research.md splits lines in three different ways. `stage2.research_visible_text` uses `str.splitlines`, which also breaks at CR, VT, FF, U+001C–U+001E, U+0085, U+2028 and U+2029. `check_research_handoff._lines` breaks at LF, CRLF and CR only. The `(?m)^` patterns (`RESEARCH_OPENING_END`, `research_census.SINGLE_PUBLICATION`) start a line only after LF. `render_beads_export._ohne_maschinenlokales` records that the tracker keeps such characters raw inside a text. Reading A: the prefix goes after each LF. Then a description with a U+2028 followed by three backticks has a fence with no prefix at the start of a line, as `research_visible_text` sees it. That unclosed fence hides the later `Stage-2 call, … explore` line and the `## Runner exploration —` heading, so `research_census.publication_evidence` finds no publication. A bare CR followed by three backticks and `research-swarm/v2 x` is a record outside an envelope for `check_research_handoff`. S-1 says neither can happen, yet its planted test, written with LF line breaks, still passes. Reading B: the prefix goes after every `str.splitlines` boundary. Then the structure is safe, but the spec does not say whether the original separator is kept or replaced by LF. That choice decides whether the de-quoted text equals the tracker text, so AC1 goes red under one of the two. | Opus | in spec — line breaks normalised to LF, other separators to space; [DETAIL] S-4, S-5 | — |
| S-5 | MINOR | SPEC | base | spec.md, AC1 (refuted by "the description differs from the tracker text"); Open decisions, [DETAIL] S-1 ("blank lines as `>`") | [AMBIGUITY] Under S-1 the bytes under the heading never equal the tracker text. The spec names neither the mapping back to plain text that AC1's refutation must compare through nor a rule for whitespace. Reading A: the description is stripped, as AC2 does to test for emptiness, and a line holding only spaces or tabs counts as blank and is written as `>`. Then a description whose third line holds three spaces and that ends in a line break comes back without those spaces and without the final break. Reading B: every character is kept. A line holding only whitespace becomes `> ` followed by its spaces, and the final line break gives a closing `>` line (it does not under `str.splitlines`). A test written for one reading fails an implementation of the other. A test that compares only after normalising whitespace cannot go red under either. Round-1 S-1 already named this gap (leading or trailing whitespace, CRLF, indentation), and its decision answers only the fence and heading part. | Opus | in spec — reading A (stripped, whitespace-only lines blank, inverse mapping for AC1); [DETAIL] S-4, S-5 | — |

Stage-2 call, 2026-11-28: spec-review · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1328 files, 6169 commits, 12 rules.
## Phase 2a — fallback deepseek-v4.1-flash, 2026-11-28

Spec fingerprint: sha256:65297dcc1a6fc78c1e35a93ac6bcb14d296029e2c99f2efad1a725e53c9cc037

Spec review commit: 082b20858e83dd04ef3ab91425018c466991d47b

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-6 | [AMBIGUITY] MINOR | SPEC | base | spec.md, AC5 ("the generated opening notices are removed as before"); scripts/new_change.py::BODY_TEMPLATE, first notice ("this file is empty until it has run") | [AMBIGUITY] The spec fixes where the notices sit (Open decisions: notices before the topic section) and that they are removed, but never whether their wording survives the change. Reading A: "as before" binds the notice bytes, so every generated skeleton keeps the sentence that the file is empty while a topic section sits under it — the skeleton's first statement about itself becomes false in every change created from now on. Reading B: "as before" binds only the removal, so the notice is reworded to stop claiming emptiness; `stage2.skeleton_notices` reads `BODY_TEMPLATE` at call time, so the removal matches either wording. Both readings satisfy AC1–AC6 unchanged, so no criterion goes red on the difference, and a test set written under one reading contradicts an implementation of the other. | deepseek-v4.1-flash | in spec — reading A (notice bytes unchanged); [DETAIL] S-6 | — |
