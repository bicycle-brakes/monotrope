---
title: "Findings — stage2-off-reason"
category: findings
status: draft
implementation_status: none
date: 2026-11-28
created: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-73gi.6
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — stage2-off-reason

Stage-2 call, 2026-11-28: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1325 files, 6215 commits, 12 rules.

Stage-2 call, 2026-11-28: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1328 files, 6217 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-28

Spec fingerprint: sha256:1bb95c8468c2a4796f80b38506afc90d402777bb01dc1b266665bfad1cf79f51

Spec review commit: 480ec27bbc5462662b6cede8006a4faf9478e9c3

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | [AMBIGUITY] | SPEC | base | spec.md criterion 6; scripts/run_report.py:459, :372 | The process report reads `ps -axo pid,etime,command` and splits each command on whitespace (scripts/run_report.py:459), so it cannot tell where one argument ends and the next begins. Criterion 6 can be read two ways. Reading A: "a valid invocation with a supplied reason" means every reason the runner accepts, including the quoted multi-word reasons the instructions show (`"Z.ai unavailable"`), placed before the change. Then `implement --stage2-off "Z.ai unavailable" alpha` must report `alpha`, and `implement --stage2-off "after beta failed" alpha` must not report `beta`. A parser that skips one token after the flag fails both: the first gives an unread change, the second names `beta`. The same happens with `--stage2-off="Z.ai down" alpha`. Reading A needs a different source of the argument list, beyond this bounded fix. Reading B: only single-token reasons are covered. Change-first forms already pass on the current code, and multi-word reasons before the change stay unread or misread. The two readings give a different parser scope and different tests. | Opus | in spec — criterion 6 rewritten (never the reason; unknown for unsplittable multi-word) (bounded standing grant) | — |
| S-2 | MAJOR | SPEC | base | spec.md criterion 4 and Definition of Done; decisions.md "SKIP · interview"; scripts/stage2.py:14744-14752 | decisions.md and the bead say the guard at scripts/stage2.py:14744-14752 and its test `test_a_change_name_after_the_stage2_off_flag_is_named_as_eaten` are removed. The spec never says so. With a mandatory value, `explore --stage2-off demo` still takes `demo` as the value, so the guard still fires on that input. Two builds are possible. Keep the guard: the refusal says "was taken as the --stage2-off reason". Delete it: `folder_of` refuses with "Name the change" (scripts/stage2.py:1926). Both satisfy criterion 4 and every other criterion. The builder has to choose, and no criterion or Definition-of-Done item fails if the guard and its test stay. | Opus | in spec — criterion 4: guard and its test removed, refusal from the missing change | — |
| S-3 | [AMBIGUITY] | SPEC | base | spec.md criterion 7 and Definition of Done; README.md:250; scripts/stage2.py:46, :14612 | "Current runner instructions" can be read two ways. Reading A: only the four files the Definition of Done names (docs/WORKFLOW.md, prompts/01-explore.md, prompts/04-implement.md, AGENTS.md). Then three places keep the optional form and criterion 7 still passes: README.md:250 (`--stage2-off [REASON]`), the module docstring at scripts/stage2.py:46 (`--stage2-off [REASON]`) and the `--help` text at scripts/stage2.py:14612 ("record the optional reason"). Reading B: every current text that shows the invocation. Then those three must change too, although README.md is not among the files the Definition of Done names. | Opus | in spec — criterion 7 lists the instruction files; AGENTS.md proposed, not edited | — |
| S-4 | MAJOR | SPEC | base | scripts/stage2.py:7536; docs/WORKFLOW.md:1119; spec.md criteria 1 and 7 | When the model process fails, the runner tells the caller to "rerun the verb or add --stage2-off." (scripts/stage2.py:7536). docs/WORKFLOW.md:1119 describes the same next step as `implement <change> --stage2-off`. Once criterion 1 holds, doing exactly what the runner says is refused with exit 2. The spec does not say whether this runtime message counts as a current runner instruction under criterion 7, or whether it changes at all. If WORKFLOW.md:1119 is updated as the Definition of Done requires and the message is not, the documentation and the runner's own output disagree. | Opus | in spec — criterion 7 covers runtime next-step messages | — |
