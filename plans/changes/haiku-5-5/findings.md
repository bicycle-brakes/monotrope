---
title: "Findings — haiku-5-5"
category: findings
status: draft
implementation_status: none
date: 2026-10-14
created: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-eao
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — haiku-5-5

Stage-2 call, 2026-10-14: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 419 files, 1145 commits, 12 rules.

Stage-2 call, 2026-10-14: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 422 files, 1157 commits, 12 rules.

Stage-2 call, 2026-10-14: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 422 files, 1158 commits, 12 rules.

Stage-2 call, 2026-10-14: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 422 files, 1159 commits, 12 rules.

## Phase 6 — Opus 5.5, 2026-10-14

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | MINOR | SPEC | base | `model-endpoints.yaml:53`; `model-endpoints.yaml:68`; `tests/test_model_endpoints.py`; `tests/test_stage2.py:828` | Nothing measures the `anthropic-api` half of the criterion or the removal of the old id. If `anthropic-api` listed `claude-haiku-4-5` instead of `claude-haiku-5-5`, or either Anthropic endpoint listed `claude-haiku-4-5` beside the new id, `make verify` would stay green: the display-name resolution tests are satisfied by any one endpoint carrying `claude-haiku-5-5` (here `claude-code-plan`), and the only runner test that reads the declaration, the `--stage2-off` explore test, consults `claude-code-plan` alone. A test should require both endpoints to list `claude-haiku-5-5` and neither to list `claude-haiku-4-5`. [criterion 2] | Opus 5.5 | taken — criterion 2: a test asserts both Anthropic endpoints list claude-haiku-5-5 and neither lists claude-haiku-4-5; fixed by `tests/test_stage2.py::test_both_anthropic_endpoints_authorize_haiku_5_5_instead_of_4_5` (guard test, plants each fault itself; red first impossible because the code was already right — completed by the orchestrating session after three runner attempts) | no |
| F-2 | MINOR | SPEC | base | `AGENTS.md:35`; `docs/WORKFLOW.md:702`; `docs/WORKFLOW.md:723`; `docs/WORKFLOW.md:1079`; `scripts/stage2.py:28` | Of the operative Haiku instructions, only the §3 routing rows and the two prompts' Model lines are guarded: the rows and the commit prompt go red through display-name resolution once `claude-haiku-4-5` is no longer declared, and the explore prompt's "Haiku 5.5 explores" is pinned. The five prose spots this change rewrote — the `--stage2-off` sentence in `AGENTS.md`, `docs/WORKFLOW.md` §4's flash-rows paragraph, its `explore` verb entry and its stage-2-run fallback sentence, and the runner's module docstring — have no test; restoring "Haiku 4.5" in any of them leaves `make verify` green, so the refutation the criterion names cannot be measured there. A test should refuse a Haiku 4.5 pin in these files. [criterion 3] | Opus 5.5 | taken — criterion 3: a test rejects a Haiku 4.5 instruction in AGENTS.md, docs/WORKFLOW.md operative sections and the stage2.py docstring; fixed by `tests/test_stage2.py::test_the_current_haiku_instructions_reject_4_5` (guard test, plants each fault itself; completed by the orchestrating session) | no |

Checked: the runner's `HAIKU` constant and its only consumer `explore()` under `--stage2-off`, the audit line that records the model from that tuple, and the new assertion on it (criterion 1); both Anthropic endpoint lists and every reader of them (criterion 2); every remaining "Haiku 4.5" or `claude-haiku-4-5` outside dated records — only the two planted wrong-model fixtures in `tests/test_stage2.py` and two German example comments in `tests/test_model_endpoints.py` remain, both allowed by the spec's last `[DETAIL]` (criterion 3); the renamed `REIST_NICHT` key against the parametrized test id it measures, with entry count and `DECKEL` unchanged (criterion 4); the protected areas and non-goals untouched in `git diff origin/main...HEAD`. No correctness fault was found; both rows are untested refutations, not wrong behaviour.

Phase 6 verdict: opus-5.5, 2026-10-14

Re-check F-1 — confirmed fixed. `test_both_anthropic_endpoints_authorize_haiku_5_5_instead_of_4_5` reads `model-endpoints.yaml` itself and asserts, per endpoint by name, that `anthropic-api` and `claude-code-plan` each list `claude-haiku-5-5` and neither lists `claude-haiku-4-5`, so it no longer depends on display-name resolution being satisfied by one endpoint. Planted into the real declaration and restored one at a time, each fault turned it red: `claude-haiku-5-5` replaced by `claude-haiku-4-5` on `anthropic-api` (line 53) and on `claude-code-plan` (line 68), and `claude-haiku-4-5` added beside the new id on each endpoint. Red first could not hold because the declaration was already right; the in-test planted copies and these mutations stand in for it.

Re-check F-2 — confirmed fixed. `test_the_current_haiku_instructions_reject_4_5` rejects `Haiku 4.5` or `claude-haiku-4-5` in `AGENTS.md` (whole file), `docs/WORKFLOW.md` §3 and §4, both phase prompts and every docstring of `scripts/stage2.py`. All five spots the row names lie inside what it reads: `docs/WORKFLOW.md:702`, `:723` and `:1079` are in §4 (lines 614–1117), and `scripts/stage2.py:28` is in the module docstring. Restoring "Haiku 4.5" in each of the five, one at a time in the real file and restored afterwards, turned the test red with the file named in the message. Accepted limit, not a new row: the pattern does not catch other spellings such as `Haiku-4.5` or `claude-haiku-4.5`, and `docs/WORKFLOW.md` outside §3 and §4 is not read; neither is a spot the row named.

Phase 6 re-check: opus-5.5, 2026-10-15

## Phase 4b — loop rows, released 2026-10-14

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MAJOR | MAINT | base | `plans/changes/haiku-5-5/research.md:12` and `:21-25` against the appended body from `:27` on | The research body is the GLM 5.3 Flash answer the runner appended (`Stage-2 call ... model glm-5.3-flash`, line 27), but the file still declares `provenance: human-written`, has no `produced_by:` or `review:`, and keeps the skeleton sentence "this file is empty until it has run"; the note at lines 21–25 says whoever fills it with a language model must set `ai-drafted-reviewed` and add both fields, whose class carries `review_required: true`, so model prose is declared as human work and the declared review requirement is skipped. | deepseek-v4.1-flash | taken — not a test — metadata: the research header now declares the GLM exploration (`ai-drafted-reviewed`, `produced_by`, `review` pending) and drops the skeleton sentence; repaired by the orchestrating session | no | agree |
| L1-2 | MINOR | MAINT | maintainer-trip | `docs/adr/0007-stage-2-reviews-by-codex-and-glm.md:86` and `:117` against `docs/WORKFLOW.md:1079` and `AGENTS.md:35` | Two current authorities disagree about the stage-1 fallback: the ADR, still live and amended only by ADR 0011 and ADR 0016, returns phases 1 and 4 to "Haiku 4.5 and Sonnet 5.5" and says "Haiku 4.5 explores", while the updated doctrine now names Haiku 5.5; nothing in the ADR marks that sentence historical, so a reader who follows it gets the old model. | deepseek-v4.1-flash | rejected — ADR 0007 is a dated record the spec protects (non-goal "Rewriting dated records", Q-1); the operative doctrine is docs/WORKFLOW.md and AGENTS.md, which name Haiku 5.5; a dated amendment would be a decision PR of its own, named in this PR as an accepted limit |  | disagree — the spec settles this case: its non-goal "Rewriting dated records" and its third `[DETAIL]` keep ADRs as dated records even where they describe old fallback rules (Q-1); the operative doctrine a reader follows today, `docs/WORKFLOW.md` §3/§4 and `AGENTS.md`, names Haiku 5.5 |
| L1-3 | MINOR | SPEC | promised-not-done | `plans/changes/haiku-5-5/plan.md:39` against `plans/changes/haiku-5-5/plan.md:59-65` | The plan's own change list says to "record measured phase-4 time below", but the Time used section records that no start or end was readable and says "the runner's record may complete the span"; the runner writes only a call date per audit line (`scripts/stage2.py:700`) and measures no start or end anywhere, so the promised measurement is absent and cannot be completed the way the sentence says. | deepseek-v4.1-flash | rejected — the section states truthfully that a file-tools attempt cannot read the clock; that runner limitation predates this change (third night run, 2026-10-14) and is outside its scope |  | agree |

Rounds run: 2

Kept from the loop record:

mimo-v2.6-flash reported no finding.
The answer was not only six-cell rows; what is not one is kept below as it came.

No findings — every operative Haiku reference (runner constant, both endpoint declarations, §3/§4 routing tables, both phase prompts, AGENTS.md, stage2 docstrings, tests and the probe entry) now reads `claude-haiku-5-5`/Haiku 5.5 consistently, the remaining Haiku 4.5 mentions are in dated records the spec protects, and the kit exemption list and cap are unchanged.

Stage-2 call, 2026-10-15: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 422 files, 1168 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/haiku-5-5/plan.md` +20 -0
>
> Diagnostics:
> ```text
> - L1-1: no fixed line
> - F-1: no fixed line
> - F-2: no fixed line
> - expected: no taken row carries this id
> - found: no taken row carries this id
> - relevant: no taken row carries this id
> - proposal: no taken row carries this id
> - Resume: no taken row carries this id
> ```

Stage-2 call, 2026-10-15: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 422 files, 1168 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/haiku-5-5/plan.md` +34 -2
> - `tests/test_stage2.py` +61 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-1: no fixed line
> - F-1: no fixed line
> - F-2: no fixed line
> - expected: no taken row carries this id
> - found: no taken row carries this id
> - relevant: no taken row carries this id
> - proposal: no taken row carries this id
> - Resume: no taken row carries this id
> ```

Stage-2 call, 2026-10-15: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 422 files, 1168 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/haiku-5-5/plan.md` +6 -2
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - F-1: tests/test_stage2.py::test_both_anthropic_endpoints_authorize_haiku_5_5_instead_of_4_5: pytest ended 0 on the baseline's code; red first is exit 1 or 2
> - F-2: tests/test_stage2.py::test_the_current_haiku_instructions_reject_4_5: pytest ended 0 on the baseline's code; red first is exit 1 or 2
> ```
