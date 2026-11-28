---
title: "Research — stage2-off-reason"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-73gi.6
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-28", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# stage2 off reason — Research

## Topic (bead coding-harness-73gi.6)

Class: bounded. The flag takes an optional value, so a change name can be swallowed as the reason; a guard at scripts/stage2.py:11401 catches that after the fact. Make the value mandatory (no nargs='?'), delete the guard and its test, and keep the recorded reason where it is.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-28: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM through Z.ai at its weekly limit until 2026-11-29 · leak check clean over 1325 files, 6213 commits, 12 rules.

## Runner exploration — 2026-11-28

Research for `stage2-off-reason`, ready to append to `plans/changes/stage2-off-reason/research.md`. I read files only and changed nothing.

## What exists today

**The flag and its guard.** `--stage2-off` is declared in `build_parser` in `scripts/stage2.py` with `nargs="?"` and `const="stage 2 disabled by caller"`, so a bare flag is accepted and records that default text. The guard the bead names is not at line 11401. In the main dispatch of `scripts/stage2.py`, around lines 14744–14752, a block refuses with "the change name `<x>` was taken as the --stage2-off reason" when `--stage2-off` has a value, no change is given, and `plans/changes/<value>/` exists. The same dispatch refuses `--stage2-off` for verbs other than explore, implement and repair (around line 14753). Line 11401 in `scripts/stage2.py` does not contain this check, so the bead's line reference is stale.

**Where the value goes.** `explore` (`scripts/stage2.py`, around lines 11694–11734) takes `stage2_off` as a parameter. When it is set, the route is `stage-1`, Haiku 5.5 is the endpoint, and `--class` and `--availability-reported` are refused. The value is passed to `begin_work_call(...)`, which records it. `implement` (around line 13005) and `repair` (around line 13604) use the same parameter and select Sonnet 5.5 as the Stage-1 model. I did not read `begin_work_call` itself, so the place where the reason is written is named but not confirmed.

**The parser in run reports.** `scripts/run_report.py`, `parse_processes` (around lines 361–389), treats `--stage2-off` as taking an optional value. It looks at the following token and skips it as a reason only when the token is not a known change name and does not start with `-`. Otherwise it reads the token as the next option or change.

**Help text and docstrings.** `scripts/stage2.py` names the optional form in its module docstring (around lines 46 and 92) and in the `--stage2-off` help string (around line 14612, "record the optional reason").

**Tests that cover the flag.**
- `tests/test_stage2.py`, `test_a_change_name_after_the_stage2_off_flag_is_named_as_eaten` (around lines 7620–7627): exercises the guard, asserts its message text, and asserts no model call.
- `tests/test_stage2.py`, `test_stage2_off_is_only_for_work_verbs` (around lines 7630–7634): runs `draft`, the review verbs and `release-loop` with a bare `--stage2-off` and expects exit 2 with no calls. Whether argparse's own refusal of a missing value also exits 2 is not verified here.
- `tests/test_stage2.py` also has many `--stage2-off <reason>` calls (for example lines 2305–2339, 4086–4120, 15038, 25788–25804). These pass a value and are not affected by a mandatory value.
- `tests/test_stage2.py`, around lines 24878–25046: several tests read `prompts/` and `docs/WORKFLOW.md` and assert the literal string `--stage2-off [REASON]` is present, and that some phrases are absent. Changing that text in the docs or prompts will change what these tests find.
- `tests/test_run_report.py`, `test_stage2_off_without_reason_preserves_change` (around lines 940–952): asserts the optional-value parsing for five argument forms, including `--stage2-off --class bounded alpha` and `alpha --stage2-off`.
- `tests/test_stage2_session.py` around line 1144: a bare `--stage2-off` on the `session` verb with no model is expected to exit 2. This path is in `scripts/stage2_session.py`, which has no `stage2_off` handling of its own (a grep found none).

**Text that carries the optional form.**
- `prompts/01-explore.md` (lines 6 and 17) and `prompts/04-implement.md` (line 6) state `--stage2-off [REASON]`.
- `docs/WORKFLOW.md` uses the bracketed form at lines 1064, 1114, 1321, 1336, 1341 and 2228. Line 1119 gives the next step as `implement <change> --stage2-off` with no reason, and lines 1608 and 1647 mention `--stage2-off` without a value. Those bare forms would be refused once the value is mandatory.
- `docs/adr/0015-glm-5-3-repairs-taken-findings.md` (line 109) and `docs/adr/0017-codex-repairs-taken-findings.md` (line 88) describe the flag with an optional reason.
- Several handovers and research notes quote bare or reasoned forms as history. I did not classify them and did not edit them.

**Decision record.** `plans/changes/stage2-off-reason/decisions.md` skips phase 1a as a bounded fix under the standing grant of 2026-11-25. Its frontmatter has `provenance: ai-drafted-reviewed` and `review: {status: pending}`.

## What is unclear

- **Whether a bare `--stage2-off` is still needed.** The bead's design makes the value mandatory and removes the guard. The docs at WORKFLOW.md line 1119 and the tests in `test_stage2.py` around lines 7630–7634 still use a bare flag. The research does not show whether any live runner path or handover command depends on the bare form.
- **Run-report parser.** `parse_processes` reads process lists from live `ps` output. Older processes started with a bare flag may still be running when the change lands. Whether the optional-value branch in `run_report.py` should stay for that reason, or be removed with the guard, is not settled by anything I read.
- **Where the reason is recorded.** The bead says to keep the recorded reason where it is. I did not read `begin_work_call` or the call-record writer to confirm the exact field and file.
- **Other active or archived changes.** A grep found `--stage2-off` or `stage2-off` mentions in `plans/changes/stage2-session/plan.md`, `plans/changes/repair-scope-guard/findings.md`, `plans/changes/ontology-relation-layer/research.md`, and several archived `spec.md` and `research.md` files (for example `archive/2026-11-06-stage2-repair/spec.md`, `archive/2026-11-06-haiku-5-5/spec.md`, `archive/2026-10-07-stage2-flash-runner/spec.md`). I did not open them and cannot say whether any of them binds the optional form.
- **Neighbour specs.** `plans/specs/` has no file whose name contains "stage2" (the Glob returned none). The neighbours I can name from what I read are `plans/changes/stage2-session/` (active, mentions the flag) and the archived `2026-11-06-stage2-repair` and `2026-10-07-stage2-flash-runner` changes. I did not confirm that any of them is a spec under `plans/specs/`.

## Which files a change would have to touch

- `scripts/stage2.py`: the `--stage2-off` declaration in `build_parser` (`nargs`, `const`), the guard block in the main dispatch, and the help text and docstring that name the optional form.
- `scripts/run_report.py`: the optional-value branch in `parse_processes`, if the parser is to match the new form.
- `tests/test_stage2.py`: delete `test_a_change_name_after_the_stage2_off_flag_is_named_as_eaten`; re-check `test_stage2_off_is_only_for_work_verbs`; update the string assertions around lines 24878–25046 if the prompt or doc wording changes.
- `tests/test_run_report.py`: `test_stage2_off_without_reason_preserves_change`, if the parser changes.
- `prompts/01-explore.md`, `prompts/04-implement.md`, `docs/WORKFLOW.md` (lines listed above), and possibly the two ADRs: the bracketed form and the bare-flag examples.
- Not expected to change: `scripts/stage2_session.py` and `tests/test_stage2_session.py`, which refuse a bare flag on the session verb independently.
