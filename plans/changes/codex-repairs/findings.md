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

Stage-2 call, 2026-10-13: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Z.ai weekly limit exhausted until 2026-10-14 14:34 CEST (HTTP 429, code 1310), and Claude Code 2.1.296 refuses the GLM names (bead coding-harness-6th) · leak check clean over 416 files, 1023 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `AGENTS.md` +1 -1
> - `docs/WORKFLOW.md` +22 -14
> - `docs/adr/0015-glm-5-3-repairs-taken-findings.md` +8 -2
> - `docs/adr/0017-codex-repairs-taken-findings.md` +6 -3
> - `model-endpoints.yaml` +3 -2
> - `plans/changes/codex-repairs/plan.md` +14 -12
> - `prompts/04-implement.md` +9 -5
> - `prompts/04b-review-loop.md` +1 -1
> - `scripts/stage2.py` +74 -29
> - `scripts/stage2_runs.py` +2 -1
> - `tests/test_stage2.py` +554 -159
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed `tests/test_stage2.py`.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 19 lines of this gate left out …]
> ...........................................FF........................... [ 75%]
> ........................................................................ [ 78%]
> ........................................................................ [ 82%]
> ........................................................................ [ 86%]
> ........................................................................ [ 90%]
> ........................................................................ [ 94%]
> ........................................................................ [ 97%]
> ..........................................                               [100%]
> =================================== FAILURES ===================================
> _________ test_adr_0017_supersedes_0015_and_keeps_the_repair_contract __________
>
>     def test_adr_0017_supersedes_0015_and_keeps_the_repair_contract() -> None:
>         """Criterion 21. Planted fault: marker missing, 0015's body rewritten, or a retained rule dropped."""
>         old = (REPO_ROOT / "docs" / "adr" / "0015-glm-5-3-repairs-taken-findings.md").read_text(encoding="utf-8")
>         new = (REPO_ROOT / "docs" / "adr" / "0017-codex-repairs-taken-findings.md").read_text(encoding="utf-8")
>         assert adr_0017_problems(old, new) == []
>         assert adr_0017_problems(old.replace("status: superseded", "status: accepted", 1), new)
>         assert adr_0017_problems(old.replace('superseded_by: "0017"\n', "", 1), new)
>         assert adr_0017_problems(old.replace("The repair of taken findings runs on GLM 5.3", "x", 1), new)
> >       assert adr_0017_problems(old, new.replace("the maximum stays three rounds", "no limit", 1))
> E       assert []
> E        +  where [] = adr_0017_problems('---\ntitle: "ADR 0015 — GLM 5.3 repairs the findings the orchestrator takes, and no reviewer repairs its own"\ncatego...w of the change that carries this record reads it against\n  `plans/changes/stage2-repair/decisions.md`, Q-1 to Q-5.\n', '---\ntitle: "ADR 0017 — Codex repairs the taken findings"\ncategory: adr\nstatus: accepted\ncreated: 2026-10-13\nlast...ion body preserved and protected areas\n  untouched. Passing stand-in tests are not evidence of  [… 24 characters left out …]
> E        +    where '---\ntitle: "ADR 0017 — Codex repairs the taken findings"\ncategory: adr\nstatus: accepted\ncreated: 2026-10-13\nlast...ion body preserved and protected areas\n  untouched. Passing stand-in tests are not evidence of a live Codex repair.\n' = <built-in method replace of str object at 0x79a592d000>('the maximum stays three rounds', 'no limit', 1)
> E        +      where <built-in method replace of str object at 0x79a592d000> = '---\ntitle: "ADR 0017 — Codex repairs the taken findings"\ncategory: adr\nstatus: accepted\ncreated: 2026-10-13\nlast...ion body preserved and protected areas\n  untouched. Passing stand-in tests are not evidence of a live Codex repair.\n'.replace
>
> tests/test_stage2.py:6705: AssertionError
> ____________ test_codex_repair_doctrine_and_endpoint_remarks_agree _____________
>
>     def test_codex_repair_doctrine_and_endpoint_remarks_agree() -> None:
>         """Criterion 20. Planted fault: an active GLM repair claim, a blanket ban or a false confinement claim."""
>         paths = [
>             "scripts/stage2.py",
>             "docs/WORKFLOW.md",
>             "AGENTS.md",
>             "prompts/04-implement.md",
>             "prompts/04b-review-loop.md",
>             "model-endpoints.yaml",
>         ]
>         texts = {name: (REPO_ROOT / name).read_text(encoding="utf-8") for name in paths}
>         assert codex_repair_doctrine_problems(texts) == []
>         for name, needle, replacement in (
>             ("scripts/stage2.py", "repair       <change>   # Codex", "repair       <change>   # GLM 5.3"),
>             ("docs/WORKFLOW.md", "a fresh read-only Codex session", "a session"),
>             ("docs/WORKFLOW.md", "The exception (ADR 0017)", "A reviewer never repairs its own findings"),
>             ("AGENTS.md", "Codex repairs the findings the orchestrator takes", "GLM 5.3 repairs the findings"),
>             ("prompts/04b-review-loop.md", "gives them to Codex in one call", "gives them to GLM 5.3 in one call"),
>             ("model-endpoints.yaml", "`glm-5.3` repaired the findings", "`glm-5.3` repairs the findings"),
>         ):
> >           assert needle in texts[name], (name, needle)
> E           AssertionError: ('docs/WORKFLOW.md', 'a fresh read-only Codex session')
> E           assert 'a fresh read-only Codex session' in '---\ntitle: "Workflow and model routing — phases and stages"\ncategory: governance\nstatus: current\ncreated: 2026-09... files despite good naming, add an LSP MCP\nserver — and only when that is not enough, think about a semantic index.\n'
>
> tests/test_stage2.py:6757: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_adr_0017_supersedes_0015_and_keeps_the_repair_contract
> FAILED tests/test_stage2.py::test_codex_repair_doctrine_and_endpoint_remarks_agree
> 2 failed, 1896 passed, 16 skipped in 326.11s (0:05:26)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 8840 earlier lines left out …]
> templates/handover.md:22:81 error MD013/line-length Line length [Expected: 80; Actual: 200]
> templates/handover.md:48:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> templates/spec.md:21 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/spec.md:39:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> templates/spec.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
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
> tools/claude-code/README.md:72:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:74:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:75:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> make: *** [verify] Error 1
> ````

Stage-2 call, 2026-10-13: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 416 files, 1024 commits, 12 rules.

Stage-2 call, 2026-10-13: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 416 files, 1024 commits, 12 rules.

Stage-2 call, 2026-10-13: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 416 files, 1026 commits, 12 rules.

Stage-2 call, 2026-10-13: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 416 files, 1026 commits, 12 rules.

Stage-2 call, 2026-10-13: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 416 files, 1028 commits, 12 rules.

Stage-2 call, 2026-10-13: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 416 files, 1029 commits, 12 rules.

Stage-2 call, 2026-10-13: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 416 files, 1033 commits, 12 rules.

## Phase 6 — Codex, 2026-10-13

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-4 | BLOCKER | SPEC | base | `plans/changes/codex-repairs/design.md:53`; `scripts/stage2.py:188` | [DIVERGENT] For a Codex repair, the design says the prompt prohibits commands, while the accepted spec and implemented prompt explicitly permit tests and `make verify`. These contracts give opposite instructions for the same attempt. [criterion 20] | Codex | fixed — not a test — design and plan permit tests and `make verify`, and prohibit commits and repository-changing git commands. | no |
| F-5 | MAJOR | SPEC | base | `scripts/stage2.py:2179`; `scripts/stage2.py:2888` | A retry can delete the previous attempt’s audit line, quoted diagnostics and changed-file evidence while retaining its own audit and all repair rows. The checker protects only the latest audit line; isolated execution reaches the checkpoint callback with the earlier evidence missing. Passing retries must preserve that evidence. [criteria 11–12] | Codex | fixed — tests/test_stage2.py::test_a_repair_retry_cannot_remove_earlier_attempt_evidence | no |
| F-6 | MAJOR | SPEC | base | `scripts/stage2.py:931`; `scripts/stage2.py:2194` | A repair can change an unrelated phase-2a finding’s status from `taken` to `fixed` while preserving the repair rows and current audit. The preservation check excludes phase-2a tables, so isolated execution accepts the altered status and reaches the checkpoint callback. Findings outside the repair batch must remain unchanged. [criterion 14] | Codex | fixed — tests/test_stage2.py::test_a_repair_cannot_change_a_finding_outside_its_batch | no |
| F-7 | MAJOR | SPEC | base | `scripts/stage2.py:1926`; `scripts/stage2.py:2436` | If attempt 1 records its time span but fails another post-run check, attempt 2 can record no time and still reach the checkpoint. Every attempt compares against the invocation’s original time log, so the failed attempt’s entry satisfies the retry’s gate. Isolated execution reproduces acceptance without an attempt-2 entry. [criterion 13] | Codex | fixed — tests/test_stage2.py::test_each_repair_retry_must_add_its_own_time_entry | no |

Phase 6 verdict: codex 01a13656-f0d8-7403-ae69-d52375b8b4f5, 2026-10-13
Reviewer session: codex 01a13656-f0d8-7403-ae69-d52375b8b4f5 — a fresh session reviewed: no phase-2a session was recorded

## Phase 4b — loop rows, released 2026-10-13

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | BLOCKER | SPEC | base | docs/WORKFLOW.md, `review` bullet of "The runner is the only way"; prompts/06-review.md, `**Session:**` (and its Model paragraph); scripts/stage2.py, `review()` docstring | [DIVERGENT] The fresh-session rule for a phase-6 re-check is missing from the places that state the session rule: the `review` bullet, the `06-review.md` Session paragraph and `review()`'s docstring still say the runner resumes a recorded Codex phase-2a session whenever one stands, while the repair section and the runner start fresh whenever `findings.md` already holds a `## Phase 6` block. For a re-check of a change with a recorded 2a session the reader is told two opposite sessions, and the prompt tells the reviewer it continues the 2a thread when it does not (criteria 18 and 20). | deepseek-v4.1-flash | fixed — tests/test_stage2.py::test_codex_repair_doctrine_and_endpoint_remarks_agree | no | agree |
| L1-2 | MINOR | SPEC | base | plans/changes/codex-repairs/design.md, "Data model" and "Interfaces"; plans/changes/codex-repairs/plan.md, step 1 | The fresh re-check is described as selected by phase-6 rows whose Status begins `fixed` (the plan says fixed rows disable the 2a resume), while the runner starts fresh whenever `findings.md` already holds a `## Phase 6` block; a re-check whose phase-6 rows are not fixed still starts fresh, so the design and the plan state a narrower trigger than the change implements and a reader would expect a resumed session there (criterion 18). | deepseek-v4.1-flash | fixed — not a test — design.md and plan.md identify an earlier `## Phase 6` block in findings.md as the fresh re-check trigger, regardless of row status | no | agree |
| L1-3 | MINOR | SPEC | base | model-endpoints.yaml, `openai-codex` remark | The Codex entry names drafting and the phase-6 review as its uses but was not updated to name the repair, although every taken finding now goes to that endpoint and the GLM entry records the move; a reader of the endpoint file cannot see from the Codex entry that repair prompts reach it (criterion 20; plan step 3 promises the endpoint remarks). | deepseek-v4.1-flash | fixed — not a test — the openai-codex remark names repair of taken findings through stage2.py repair (ADR 0017) | no | agree |
| L2-1 | MINOR | MAINT | diff | tests/test_stage2.py:5450 | The change renames the top-level test `test_a_credential_refusal_puts_the_original_statuses_back` to `test_a_leak_block_after_a_failed_attempt_leaves_the_original_statuses`, although its own plan (`plans/changes/codex-repairs/plan.md`, step 2) promises "keep existing top-level test names because other plans name them". `plans/changes/stage2-repair/plan.md:374` still names the old function as the evidence holding that change's phase-6 finding F-8, so a maintainer following the citation finds no such test; `scripts/check_criterion_ledger.py` reads ledger sections only, so no gate turns red on the dangling reference. | mimo-v2.6-flash | fixed — not a test — restored test_a_credential_refusal_puts_the_original_statuses_back | no | agree |
| L2-2 | MINOR | SPEC | diff | plans/changes/codex-repairs/plan.md, "Time used" | Plan step 5 promises that the plan "measures phase 4 under `Time used`", but the section records the implement session as "span not measured" and says "the orchestrator supplies the measured span of this session before the appetite is compared", and the orchestrating session's own fix after the failed implementation attempt is logged "not timed". The 4-hour appetite of phase 4, repair rounds included, is therefore still unmeasured: no entry gives a start and an end for the implementation, and the appetite comparison the card asks for cannot be made from what the change wrote. | mimo-v2.6-flash | rejected — no session clock was read; plan.md says the span is not measured, and the pull request names the appetite as not measured rather than invent a span |  | agree |
| L2-3 | MINOR | MAINT | diff | scripts/stage2.py:2376 | When a Codex repair call moves HEAD, the new stop raises its CallFailed before the `restore_findings(kept)` branch, so a model that both commits and edits `findings.md` leaves its own `fixed` Status standing in the worktree, and that attempt gets no quoted diagnostics block and no changed-file evidence. The next `repair <change>` reads the phase-6 row as already `fixed` and takes only the remaining rows, so the finding is never repaired until someone edits it back by hand. ADR 0017 states that failed attempts have "their model-written statuses ... restored" and retain their diagnostics; the two moved-HEAD tests plant no `findings.md` edit, so nothing holds this case. | mimo-v2.6-flash | fixed — tests/test_stage2.py::test_a_codex_repair_that_commits_findings_restores_statuses_and_records_diagnostics | no | agree |
| L2-4 | MINOR | MAINT | diff | scripts/stage2.py:1049 | `review()` selects the re-check by the presence of any line starting `## Phase 6` in `findings.md`, but then records the session line "a fresh session reviewed: a re-check after a repair starts fresh". A second `review` run after an earlier verdict when no repair has run at all — an orchestrator's re-run after a red gate or a lost verdict — gets that sentence written into its findings.md, so the audit trail asserts a repair that never happened; the re-check test seeds a `fixed` row and never covers the no-repair case, and the reason should state the rule the code uses (an earlier `## Phase 6` block). | mimo-v2.6-flash | fixed — tests/test_stage2.py::test_a_phase6_rerun_without_repair_records_the_actual_recheck_reason | no | agree |
| L2-5 | MINOR | SPEC | diff | plans/changes/codex-repairs/spec.md, "Definition of Done" | The Definition of Done names the files the decision pull request must carry and omits `prompts/06-review.md`, which this change edits and which criterion 18's amendment and the doctrine test (`codex_repair_doctrine_problems`, the "06-review Model paragraph" and "06-review Session paragraph" rules) now depend on. The same section claims "the file list demonstrates the protected areas and non-goals are respected", which it cannot do for a file it leaves off the list. | mimo-v2.6-flash | fixed — not a test — Definition of Done now lists prompts/06-review.md | no | disagree — The DoD lists required files, not an exhaustive change boundary; the PR diff can still demonstrate that protected areas were respected. |
| L3-1 | MAJOR | SPEC | base | `docs/WORKFLOW.md` §4, "What every call then carries" and "Reads: confined for the Claude Code calls" | Criterion 20 promises the workflow agrees on the Codex repair route, but the confinement doctrine still describes the pre-ADR-0017 repair. `repair` is listed among "Every Claude Code call (explore, the draft's GLM attempt, implement, repair, `spec-review` and the Sonnet 5.5 fallback attempts)" that start in the worktree with `--restricted` and no `--add-dir`, and the Codex sentence names only the read-only review call and "a draft's Codex call" in `workspace-write`, adding "what such a call writes outside the change folder the runner puts back before it verifies". Since ADR 0017 the repair's first two attempts are workspace-write Codex calls: nothing confines their reads except the prompt's request — the residual risk ADR 0017 itself records — and what such a call writes outside the change folder is exactly what `checkpoint` commits (`git add -A`), not what gets put back; only the Sonnet fallback, already covered by the list's own "Sonnet 5.5 fallback attempts", is a Claude Code call. `codex_repair_doctrine_problems` reads none of these sentences and plants nothing there, so the suite stays green while the page states the opposite of the change. | mimo-v2.6-pro | fixed — tests/test_stage2.py::test_codex_repair_doctrine_and_endpoint_remarks_agree | no | agree |
| L3-2 | MINOR | MAINT | base | `docs/WORKFLOW.md` §4, "Explore, the draft, implement and repair send more than a review does" | The paragraph this change edited still names Z.ai as the destination of the repair prompt: "so they reach Z.ai in that prompt before the verdict (ADR 0015, since ADR 0017 to Codex instead of Z.ai). Far more of this repository goes to Z.ai than before 2026-10-06." The wrong destination stands in the main clause, the correction sits in a parenthesis, and the sentence after it reaffirms Z.ai volume, so a reader of the repository's egress paragraph — the one a person reads to decide what leaves the machine and where unreleased loop rows go before the verdict — still learns Z.ai, while the rows go to Codex and, on the fallback attempt, to the Sonnet 5.5 call on Anthropic, a destination the paragraph never names. | mimo-v2.6-pro | fixed — not a test — WORKFLOW §4 names Codex (OpenAI) for repair prompts and Anthropic for the Sonnet 5.5 fallback, with no Z.ai claim for repairs | no | disagree — The original sentence explicitly identifies Codex as the destination after ADR 0017, and the workflow already specifies the Sonnet fallback; moving the qualifier into the main clause is editorial. |
| L3-3 | MINOR | MAINT | base | `scripts/stage2.py`, `run_attempts`, the moved-HEAD block; `tests/test_stage2.py`, `test_a_codex_repair_that_commits_findings_restores_statuses_and_records_diagnostics` | When a Codex call moves HEAD, the run stops before any post-run check runs, yet the block the runner writes under the attempt's audit line begins "Attempt N (route) failed its post-run checks." No post-run check ran — `verify_attempt`, the measured-time check and the repair-answer check were never reached — so `findings.md` after such a stop tells a maintainer who was not there that the checks rejected the attempt, and the real reason ("the repair call moved HEAD from … to …") stands only in one line inside the block. The test pins this header for the moved-HEAD case, so the misleading wording is what the suite enforces. | mimo-v2.6-pro | fixed — tests/test_stage2.py::test_a_codex_repair_that_commits_findings_restores_statuses_and_records_diagnostics | no | agree |

Rounds run: 3

Stage-2 call, 2026-10-13: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 416 files, 1033 commits, 12 rules.

Stage-2 call, 2026-10-13: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 416 files, 1034 commits, 12 rules.

Stage-2 call, 2026-10-13: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 416 files, 1037 commits, 12 rules.

## Phase 6 — Codex, 2026-10-13

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-8 | MAJOR | SPEC | base | `scripts/stage2.py:2369`; `scripts/stage2.py:2841` | If the first completed Codex attempt deletes `plan.md`, verification records a post-run failure, but constructing the retry prompt raises an uncaught `FileNotFoundError`. No second Codex call starts. Isolated execution of the current functions reproduces this; the failed attempt must receive one fresh retry with its diagnostics. [criterion 4] | Codex | fixed — tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan | no |
| F-9 | BLOCKER | SPEC | base | `scripts/stage2.py:74`; `scripts/stage2.py:1343`; `docs/WORKFLOW.md:853` | [DIVERGENT] For a Stage-2 repair, the runner’s help still lists repair among Claude Code calls with restricted file access, and its formatter comment says work models have no command tool. The active workflow and repair prompt instead describe Codex repairs with command tools and unconfined reads. These current instructions give opposite accounts of the same repair’s capabilities. [criterion 20] | Codex | fixed — not a test — runner help and formatter comment distinguish command-capable Codex workspace-write repairs from restricted Sonnet fallback calls | no |

Phase 6 verdict: codex 01a1367f-5874-7d22-b7d0-060ad7a7feed, 2026-10-13
Reviewer session: codex 01a1367f-5874-7d22-b7d0-060ad7a7feed — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Stage-2 call, 2026-10-13: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 416 files, 1039 commits, 12 rules.

Stage-2 call, 2026-10-13: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 416 files, 1041 commits, 12 rules.

Stage-2 call, 2026-10-13: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 416 files, 1043 commits, 12 rules.

Stage-2 call, 2026-10-13: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 416 files, 1044 commits, 12 rules.

## Phase 6 — Codex, 2026-10-13

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-10 | MAJOR | SPEC | base | `scripts/stage2.py:2506`; `scripts/stage2.py:2850` | If a completed Codex attempt deletes `spec.md` and fails a post-run check, constructing the next prompt raises an uncaught `FileNotFoundError`: only `plan.md` is restored. Isolated execution reproduces both cases—deletion by attempt 1 prevents the fresh Codex retry; deletion by attempt 2 prevents the Sonnet fallback. The prescribed next attempt must receive the failed attempt’s diagnostics. [criteria 4–5] | Codex | fixed — tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan | no |

Phase 6 verdict: codex 01a136aa-2a43-7370-ac31-a0a5732edea6, 2026-10-13
Reviewer session: codex 01a136aa-2a43-7370-ac31-a0a5732edea6 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Stage-2 call, 2026-10-13: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 416 files, 1046 commits, 12 rules.

Stage-2 call, 2026-10-13: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 416 files, 1048 commits, 12 rules.

## Phase 6 — Codex, 2026-10-13

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-11 | MAJOR | SPEC | base | `scripts/stage2.py:2372`; `scripts/stage2.py:718–719` | If a completed Codex attempt deletes `prompts/04-implement.md` or `AGENTS.md` and fails verification, constructing the next prompt raises an uncaught `FileNotFoundError`. The restoration list covers only change-folder inputs. Isolated execution reproduces both cases: deletion by attempt 1 prevents the fresh Codex retry; deletion by attempt 2 prevents the Sonnet fallback. Both prompt dependencies must remain available so the prescribed next attempt receives the failed attempts’ diagnostics. [criteria 4–5] | Codex | open | — |

Phase 6 verdict: codex 01a136c5-c1ff-7882-a91f-235052d1cc35, 2026-10-13
Reviewer session: codex 01a136c5-c1ff-7882-a91f-235052d1cc35 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check
