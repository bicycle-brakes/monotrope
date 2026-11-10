---
title: "Findings — review-fewer-rounds"
category: findings
status: draft
implementation_status: none
date: 2026-11-10
created: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-3rtn
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — review-fewer-rounds

Stage-2 call, 2026-11-10: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 960 files, 3796 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/adr/0026-focused-review-with-a-shadow-period.md` +111 -0
> - `plans/changes/review-fewer-rounds/design.md` +179 -0
> - `plans/changes/review-fewer-rounds/plan.md` +201 -0
> - `plans/changes/review-fewer-rounds/spec.md` +291 -0
>
> Diagnostics:
> ````text
> - `bash scripts/verify_all.sh --job docs` exited 1
> The gates that blocked, each with its last lines:
> ── [question-context] $ lauf_cmd
>   - plans/changes/review-fewer-rounds/decisions.md: Q-1 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-2 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-3 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-4 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-5 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-6 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-7 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-8 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-9 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-10 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-11 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-12 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
> question-context NOT MEASURED: 12 unreadable evidence — exit 3, nothing measured.
> ── [question-context] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 34414 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
> tools/claude-code/README.md:17:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:18:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:23:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:24:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:25:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:29:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:38:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:41:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:67:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:99:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:99:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:99:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:100:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:101:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:102:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> ````

Stage-2 call, 2026-11-10: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason the first draft attempt failed · leak check clean over 965 files, 3803 commits, 12 rules.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`
> - `plans/changes/review-fewer-rounds/decisions.md`

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/review-fewer-rounds/decisions.md` +76 -0
> - `plans/changes/review-fewer-rounds/plan.md` +5 -2
>
> Diagnostics:
> ````text
> - `bash scripts/verify_all.sh --job docs` exited 1
> The gates that blocked, each with its last lines:
> ── [question-context] $ lauf_cmd
>   - plans/changes/review-fewer-rounds/decisions.md: Q-1 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-2 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-3 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-4 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-5 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-6 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-7 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-8 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-9 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-10 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-11 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-12 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
> question-context NOT MEASURED: 12 unreadable evidence — exit 3, nothing measured.
> ── [question-context] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 34470 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
> tools/claude-code/README.md:17:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:18:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:23:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:24:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:25:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:29:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:38:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:41:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:67:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:99:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:99:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:99:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:100:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:101:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:102:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> ````

Stage-2 call, 2026-11-10: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 965 files, 3806 commits, 12 rules.

> Attempt 3 (glm): the runner put back what a draft may not change:
> - `plans/INDEX.md`
> - `plans/changes/review-fewer-rounds/decisions.md`

> Attempt 3 (glm) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/review-fewer-rounds/decisions.md` +118 -6
> - `plans/changes/review-fewer-rounds/plan.md` +8 -7
>
> Diagnostics:
> ````text
> - `bash scripts/verify_all.sh --job docs` exited 1
> The gates that blocked, each with its last lines:
> ── [question-context] $ lauf_cmd
>   - plans/changes/review-fewer-rounds/decisions.md: Q-1 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-2 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-3 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-4 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-5 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-6 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-7 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-8 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-9 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-10 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-11 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/review-fewer-rounds/decisions.md: Q-12 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
> question-context NOT MEASURED: 12 unreadable evidence — exit 3, nothing measured.
> ── [question-context] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 34527 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
> tools/claude-code/README.md:17:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:18:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:23:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:24:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:25:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:29:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:38:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:41:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:67:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:99:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:99:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:99:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:100:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:101:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:102:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> ````

Stage-2 call, 2026-11-10: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 965 files, 3823 commits, 12 rules.

Stage-2 call, 2026-11-10: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 965 files, 3882 commits, 12 rules.

Stage-2 call, 2026-11-10: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 965 files, 3894 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-10

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | MAJOR | SPEC | spec | Criteria 2, 15, 20, 25 against criterion 4 | [AMBIGUITY] Criterion 4 says the central declaration supplies seats, round count and the phase-6 limit, and that no prompt, test or doc may fix those values on its own. Q-4 makes "which and how many models sit in a round" changeable. Yet criterion 2 refutes anything but fifteen and five calls, criterion 25 anything but three, criterion 15 "any fourth review", and criterion 20 requires the docs to describe a "three-model" round. Reading A: these numbers are runner invariants. Tests then assert 15, 5, 3 and the review cap literally, and a maintainer edit to the declaration (for example two seats per lens) is either refused or turns criteria 2, 15 and 25 red. Those tests and docs then break criterion 4. Reading B: the numbers describe only the initial configuration. Tests derive the expected counts from the declaration, and a mis-seated declaration still passes criterion 2. The spec also does not say whether the Q-15 small-change rule, the Q-14 free-round seating, the night exception and the family rule are configurable values or fixed code. | Opus | open | — |
| S-2 | MAJOR | SPEC | spec | Terms; criteria 2, 3, 25; `[DETAIL]` small-change seat | [GAP] Criteria 2, 3 and 25 depend on "model family" and "lineage", and the spec uses the two side by side. Terms defines neither. `model-endpoints.yaml` has no family or lineage field, and `scripts/stage2.py` has no such concept. An implementer would have to invent five things: whether lineage and family are the same thing; whether family means the vendor of the weights, the serving provider (such as `opencode-go`) or the base model a model was derived from; where each reviewer's family is declared; how the implementer's family is found (from the route or from the model); and how the validator refuses a model with no declared family. The answer decides whether `gpt-6.1-terra` counts as self-family when `gpt-6.1-sol` implemented the change, and so whether criterion 3 can go red at all. | Opus | open | — |
| S-3 | MAJOR | SPEC | spec | Criterion 2 ("best measured precision", "an unmeasured precision claim"); `[DETAIL]` initial precision seat | [AMBIGUITY] Reading A: the declaration names a model and cites a dated measurement (the 2026-11-08 aggregate of 91%), and the validator only checks that the citation is there. The criterion then goes red only on a missing citation, never on a stale or wrong one. Reading B: the runner computes the best accepted share from loop rows when it prepares a run and seats the winner. Then the measurement window, the minimum row count, the tie rule and the basis (per lens or aggregate) all have to be specified, and a configured seat that is no longer best refutes. The spec says neither what form a "measured" claim takes nor what the refuting fixture would look like. | Opus | open | — |
| S-4 | MAJOR | SPEC | spec | `[DETAIL]` out-of-lens BLOCKERs; Terms "Capture"; criterion 8 | [AMBIGUITY] A lens reviewer may report a BLOCKER outside its own lens, and the spec does not say which lens's counts it enters. Reading A: it is a capture of the reviewer's own lens. It raises that lens's S and, usually as a singleton, its f1, singleton share and jackknife total, even though it belongs to another defect class. Reading B: it counts toward the lens whose class it belongs to. That lens then holds a capture from a reviewer outside its trio, which breaks the three-seat basis of the criterion 8 formulas. Reading C: it is accepted and repaired but left out of every lens observation. The same fixture gives a different S and f1 under each reading. | Opus | open | — |
| S-5 | MAJOR | SPEC | spec | Criterion 7; Terms "Capture"; criterion 8 | [GAP] Criterion 8's f1/f2/f3 come from the "explicit accepted-defect grouping", but the spec never says how that grouping is recorded. It is open who writes it (the orchestrator at triage or the runner), where it lives (a `findings.md` column or the run state), what form it takes (a group id, a canonical row), and whether one defect found by reviewers of two lenses (say a missing retry test, which fits both "tests as evidence" and "state, retry") is merged or counted in each lens. Without a recorded form, no test can turn "combining different defects merely because they share a location or category" red, because the runner would only echo a judgment it cannot check. The counts also cannot be recomputed from `findings.md`. | Opus | open | — |
| S-6 | MAJOR | SPEC | spec | Criterion 17 with criteria 9, 25; `scripts/stage2.py:450` | [GAP] The runner cuts every review diff at `REVIEW_DIFF_MAX_LINES = 2000`, and today a cut round merely can never count as clean. Under criterion 17, cut input leaves a round incomplete with no completion evidence, while criteria 9 and 25 require the whole diff. A change over 2000 lines (the A1 run had 2617) could therefore never complete round 1 or the free round, and no criterion lets the run move on. The spec does not say which of these applies: keep the bound, raise it, make it configurable, split the diff across calls, or let a marked cut round complete. A 12-hour change like this one is itself likely to exceed the bound. | Opus | open | — |
| S-7 | MAJOR | SPEC | spec | Criterion 17; Boundary ("pause completion"); Q-8 downside | [AMBIGUITY] The spec does not say what happens after a required seat fails, for example on an exhausted quota or a timeout. Reading A: the whole loop pauses until that frozen seat succeeds on retry, so round-1 triage, the repair and the shadow round 2 all wait, possibly for a quota window of hours. Reading B: only the affected lens loses its observation. The other seats' accepted rows are triaged and repaired, and shadow round 2 still runs because criterion 9 makes it independent of stopping signals. It is also unstated whether the maintainer may re-seat (the Boundary forbids only doing so "silently"), and how a retry relates to the completed seats that criterion 6 keeps. Q-8's accepted downside allows either "fewer reviewers or waits". | Opus | open | — |
| S-8 | MAJOR | SPEC | decisions | Criterion 10 ("evidence-based end of shadow if clear"); Non-goals; criteria 5, 11; Q-11, Q-12 | [AMBIGUITY] Reading A follows Q-12 ("ends after 10 changes when the data are clear; otherwise the runner asks the maintainer") and Q-11 ("the better trigger decides from then on"). Clear data end shadow without asking the maintainer, and the run records the calibration decision and switches mode. Reading B follows the Non-goal "automatic promotion from shadow", criterion 5 ("unapproved live threshold") and criterion 11 ("approved calibrated live policy"). Every end of shadow then needs the maintainer's approval, so "clear" and "unclear" differ only in what the report says. "Clear" also has no definition: no margin and no minimum number of would-stop misses. As a result, the clear/unclear branch of criterion 10 cannot be made red. | Opus | open | — |
| S-9 | MAJOR | SPEC | spec | Criteria 5, 10, 11 ("unapproved live threshold", "recorded calibration decision") | [GAP] The validator must refuse an unapproved live threshold, and criteria 10 and 11 forbid a winning trigger without a recorded calibration decision. The spec does not say what the declaration carries as proof of approval: a decision-record id, a dated approver field, or a path or hash of the calibration report. It also does not say where the calibration decision is recorded once this change's `decisions.md` is closed. Without that, the validator can only check that some field is non-empty, and a hand-set `mode: live` citing an invented reference passes criterion 5. | Opus | open | — |
| S-10 | MAJOR | SPEC | spec | Criterion 1 against criterion 23; Approved lens questions | [GAP] Criterion 1 is refuted by "an unapproved question list reaching a model", but criterion 23 (and Q-10) lets later additions apply without approval. The spec does not say how the declaration tells the approved fifteen apart from additions, for example by giving each question an origin: the Q-13 approval, or the id of the phase-6 finding that justified it. Without that marker, a legitimate addition trips criterion 1, and the validator cannot refuse an addition made without an uncovered phase-6 finding, which is criterion 23's refuting case. It is also unstated who derives an addition (the phase-6 reviewer, the orchestrator or a repair attempt) and who decides that "no question covers" a finding. | Opus | open | — |
| S-11 | MAJOR | SPEC | spec | Criterion 23 ("applies immediately") against criterion 6 (frozen policy) | [AMBIGUITY] The question list lives in the central declaration. Reading A: the addition is committed on the branch of the change whose phase 6 found it and appears in that change's PR. It reaches main, and other lanes, only when that PR merges, so it is not immediate. Reading B: it is committed to main at once and applies to the next round of every run. That contradicts criterion 6, which freezes the policy of runs in progress. Reading C: it applies only to loops started afterwards. Each reading needs different runner behaviour: re-reading the questions each round, or a frozen snapshot per run. | Opus | open | — |
| S-12 | MAJOR | SPEC | spec | Criterion 10 ("would-stop MAJOR/BLOCKER misses"); criterion 9; Q-11 comparison | [GAP] Round 2 has no lenses and reviews the whole diff after the round-1 repair. To report would-stop misses per lens, each accepted round-2 defect must be assigned to a lens. It must also be classed either as something round 1 missed or as a defect the round-1 repair introduced; research records that repairs create further findings. The spec names no attribution step (who assigns the lens, recorded where) and does not say whether repair-introduced defects are excluded from the misses. It also defines a candidate threshold only for the singleton share. Without thresholds for the jackknife and Chao candidates, their would-stop sets cannot be computed, so the single Q-11 comparison of triggers cannot be done. | Opus | open | — |
| S-13 | MAJOR | SPEC | spec | Criterion 10 ("ten complete shadow changes") | [AMBIGUITY] Reading A: every change completed under shadow counts, including small changes. Their one-seat lenses produce no overlap and no usable singleton signal, so ten small changes could reach the count with no calibration data at all. Reading B: only full three-seat changes count, which can take much longer and leaves small-change runs out of the report. "Complete" is also undefined. It could mean both loop rounds done, phase 6 done, or merged, and the spec does not say whether a change stopped at the phase-6 limit counts. The refuting case "counting incomplete … runs" cannot be built until that is settled. | Opus | open | — |
| S-14 | MAJOR | SPEC | spec | Criterion 15 ("night run", "single-mechanism repair evidence") | [GAP] "Night run" is defined nowhere, and `scripts/stage2.py` has no such mode. It could be a clock window (which timezone, which hours), an explicit unattended flag, or the maintainer's absence. The runner also needs a recorded claim to check that "open findings all belong to one repaired mechanism", such as rows tagged with a mechanism id and linked to the repair commit. Who records that claim and in what form is unspecified, so the runner would either trust free text or not check at all. Either way, "a night third review without the single-mechanism repair evidence" cannot be made red. | Opus | open | — |
| S-15 | MAJOR | SPEC | decisions | Criterion 15 ("an ordinary third review", "any fourth review"); Q-5 proposal options | [AMBIGUITY] After the stop, Q-5 offers the maintainer three proposals: a named limit in the PR, a mechanism repair, or stop. Reading A: the review caps are absolute. A mechanism repair the maintainer chooses after the stop is then never re-checked by phase 6, and the change merges with an unreviewed repair or not at all. Reading B: the maintainer's recorded choice authorizes another re-check. The spec then has to say how that authorization is recorded and how it differs from the forbidden "state release or loss resetting the budget". The two readings give the runner different refusal rules. | Opus | open | — |
| S-16 | MINOR | SPEC | spec | Criterion 16 | [UNTESTABLE] No test can observe whether a repair is "case-only" or a "mechanism" repair; that is a property of the repair's content. "The same defective mechanism" also has no recorded link between findings. A refuting case could only be built if the spec named a link field and an obligation it creates, for example two linked rows and a repair prompt missing the mechanism instruction; it names neither. Its scope is also unclear. Q-5 places the rule in phase-6 re-checks, criterion 16 names no phase, and `AGENTS.md` already applies it to every repair. | Opus | open | — |
| S-17 | MAJOR | SPEC | spec | Criterion 13; Q-6, Q-7 | [AMBIGUITY] The MINOR rule covers tests, security and false statements (repair), clear style (rides along) and taste (named as a PR limit), and stops there. Other MINORs are not covered: a maintainability MINOR from the fifth lens (a duplicated rule, hidden coupling; research measured 65% of loop rows as MAINT), or a small logic or state defect that is neither a test nor a security issue. Reading A: these count as style and only ride along, so maintainability MINORs never require a repair. Reading B: they are defects and require one, so on their own they can trigger the last repair after round 2. Q-6 sends every round-2 MINOR through this rule, so the answer decides whether round 2 ends in a repair. | Opus | open | — |
| S-18 | MAJOR | SPEC | decisions | Criterion 14; Q-8 ("block new and changed files") | [AMBIGUITY] Reading A, the file-level reading of Q-8's wording: any markdownlint error in a changed file blocks. This change edits `docs/WORKFLOW.md` (146 lines longer than 80 characters) and `AGENTS.md` (35), so it and every later change touching them would have to clean legacy lines, close to the non-goal "repository-wide Markdown cleanup". Under this reading, a legacy error on an untouched line of a changed file blocks, which criterion 14 lists as a refuting case ("an unchanged legacy defect failing"). Reading B, line-level: only errors on changed lines block. The spec also does not name the base for "changed": the PR merge base in CI or something else for a local `make verify`. | Opus | open | — |
| S-19 | MINOR | SPEC | spec | Criterion 21 | [UNTESTABLE] The weekly clean-up is an orchestrator action outside the runner. Triage has no status that separates a clear style finding left standing from a taste limit, and "a week" has no defined start or end. So neither the input nor the state needed to show "clear findings being discarded" can be constructed. As written, the criterion is a statement of intent. | Opus | open | — |
| S-20 | MINOR | SPEC | spec | Criterion 22; Formality inventory | [UNTESTABLE] "An omitted formality" needs a reference list to compare the inventory against. Reading A: the inventory is its own reference, so the criterion cannot go red. Reading B: the reference is the formality categories behind the measured 26% of 296 rows. Neither the spec nor the research lists those categories, so the refuting case cannot be built. Reading C: Q-1's four named formalities are the reference; the inventory already covers them, so the criterion is green by construction. | Opus | open | — |
| S-21 | MINOR | SPEC | spec | Criterion 11; `[DETAIL]` "S=0 is undefined"; criterion 8 | [AMBIGUITY] Criterion 11's live evaluation is built in this change, but the spec gives no rule for a lens whose singleton share is undefined (S=0) or whose observation is incomplete. Reading A: undefined means not triggered (research's proposal), so a change with no accepted round-1 findings on any lens goes straight to phase 6. Reading B: undefined means triggered, leaning toward re-review as the Boundary's "zero accepted findings are weak evidence" suggests. Neither the configured comparison nor any listed declaration field covers this case. | Opus | open | — |
