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
