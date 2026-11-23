---
title: "Findings — plan-card-what-line"
category: findings
status: draft
implementation_status: none
date: 2026-11-22
created: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-kg8n
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — plan-card-what-line

Stage-2 call, 2026-11-22: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1168 files, 5352 commits, 12 rules.

Stage-2 call, 2026-11-22: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1171 files, 5354 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-22

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | MAJOR | SPEC | base | spec.md criteria 2–4; decisions.md [DETAIL] "One new first field" | [AMBIGUITY] The spec does not say whether `What:` sits on one physical line or may wrap onto continuation lines inside the card block. Today the card puts each field on one line, and three sentences rarely fit on one. Reading A, one line: the prompt-form test pins exactly seven lines, and the value is the rest of the `What:` line. A card whose `What:` label line is empty, with the sentences on the lines below it, is then "blank" and refused under criterion 3. Reading B, wrapped: the value runs until the next label, so that same card passes, and the form test can no longer pin a fixed line count. Criterion 4 trims only surrounding whitespace, so under B it is also open whether line breaks inside the value are folded before the comparison with `For you:`. | Opus | in spec — [DETAIL] decided by the orchestrator: What: may wrap onto continuation lines indented under it, like a long For you: today; the check joins them before judging. Reason: three sentences rarely fit one line | — |
| F-2 | MAJOR | SPEC | base | spec.md criteria 1 and 3; Problem, second bullet | [AMBIGUITY] Criterion 1 makes `What:` the first field, but its refuter reads only the prompt. Criteria 3–4 make the draft check test that `What:` is present, is not blank and is not a copy of `For you:`. They do not test where it sits. Yet the Problem section says the check exists to protect field order. Reading A: `What:` joins the ordered label walk in `card_problem`, so a subject card with `What:` after `For you:` or after `Pre-mortem:` is refused. Reading B: the check tests presence only, so that card passes, and drafted cards put `What:` first only as far as the model follows the prompt. Also open under A: whether `What:` must be the first line of the block or only come before `For you:` (today's walk accepts other lines between labels). | Opus | in spec — [DETAIL] decided by the orchestrator: the draft check also requires What: to be the first field of the card block. Reason: the reader meets it first | — |
| F-3 | MAJOR | SPEC | base | spec.md criterion 6; [DETAIL] "A missing or unreadable date refuses measurement" | [AMBIGUITY] "Refuses the attempt" can mean two things, and the runs differ. Reading A: an unreadable spec date or adoption day is one more post-run problem in `verify_draft`. The attempt fails, its diagnostics go to `codex-repair` and then to the GLM attempt. That is three model calls against a fault in `decisions/adoption.yaml` that no draft is allowed to repair. Reading B: a `Refused` stop of the runner, matching the adoption pattern's "not measured" (exit 3 in the gates), with no further attempt. A third reading splits the case by source: a fault in the adoption record stops the runner, while a malformed spec date that the attempt wrote itself is a problem a repair attempt can fix. Each reading gives a different outcome for the same broken input. | Opus | in spec — [DETAIL] decided by the orchestrator: reading A — an unreadable spec date or adoption day is one more post-run problem of the draft attempt (verify_draft), so the attempt fails with that diagnostic and is retried as today. Reason: same path as every draft check | — |
| F-4 | MAJOR | SPEC | base | spec.md criterion 2; Non-goals, third bullet | [AMBIGUITY] Criterion 2 is stated about the drafted card ("the `What:` field explains in at most three … sentences"), but its refuter reads only the instruction. Reading A: the draft check also counts sentences and refuses a fourth. A sentence boundary then has to be defined ("e.g.", "1.5 h", file paths with dots), and a drafted four-sentence `What:` is refused. Reading B: only the prompt is checked, so that card passes the draft check and criterion 2 still counts as met. The non-goals exclude automated judgment of meaning, not counting sentences, so neither reading is ruled out. Under B, "short", "plain-language" and "one concrete example" in a drafted card have no input that turns any check red. | Opus | in spec — [DETAIL] decided by the orchestrator: the draft check counts sentences in What: (a sentence ends with a full stop, question or exclamation mark followed by space or end) and refuses more than three. Reason: the criterion must be checkable on the card | — |
| F-5 | MAJOR | SPEC | base | spec.md criterion 7; [DETAIL] "The widening rule also covers `What:`" | [AMBIGUITY] Criterion 7 and the [DETAIL] say a `What:` that "promises" a non-goal widens the scope. The existing rule in `prompts/03-plan.md` says a line widens when it "includes" something spec.md names as a non-goal or no criterion covers. `What:` is meant to carry today's problem, an example and the main risk, so it can name a non-goal area without promising it. Reading A, the existing "includes" wording extended to `What:`: a risk sentence that names a non-goal (e.g. "the full redesign stays separate") widens the scope. The card's last line then asks for "ok", and ordinary implementation waits on an approval, which is exactly what criterion 9's refuter forbids. Reading B, "promises": only a deliverable stated in `What:` widens, and the prompt has to word the rule differently for `What:` than for `For you:`/`Done when:`. | Opus | in spec — [DETAIL] decided by the orchestrator: the existing widening rule applies to What: with its own wording (a line widens when it includes a non-goal); no new verb. Reason: one rule | — |
| F-6 | MINOR | SPEC | base | spec.md criteria 3, 5, 6 | A gap: whether a plan is subject depends on spec.md's own `date:`. In the runner's draft path, that date is written by the same attempt the check judges. A failed attempt's diagnostics go to the repair attempt, which starts on the same tree and may edit spec.md. Criterion 6 refuses only a missing or malformed date. A valid date on or before the adoption day lets a five-field card pass as old: for example, a draft run on 2026-11-30 that writes `date: 2026-11-20`. The spec does not say whether the date is taken as written or checked against something the attempt cannot change, such as the baseline spec or the folder's opening commit. So the implementer decides whether criterion 6's protection against an unknown date also covers a wrong date. No stated criterion catches that input. | Opus | in spec — [DETAIL] decided by the orchestrator: the subject test reads the spec date from the committed spec at the attempt's base, not the attempt's own edit, so an attempt cannot opt out by changing its date. Reason: the judged attempt must not set its own rule | — |

Stage-2 call, 2026-11-22: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1171 files, 5359 commits, 12 rules.

> Attempt 1 (codex) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/plan-card-what-line/draft-attempt-1-20261122T084500477951Z (e8ff7cdef041); `git diff b68e5718df06 refs/stage2/attempts/plan-card-what-line/draft-attempt-1-20261122T084500477951Z` shows it.
>
> The runner put back:
> - `plans/changes/plan-card-what-line/plan.md`
> - `plans/changes/plan-card-what-line/spec.md`

Stage-2 call, 2026-11-22: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1171 files, 5359 commits, 12 rules.

> Attempt 2 (codex-repair) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/plan-card-what-line/draft-attempt-2-20261122T084514406767Z (0ba8045d884c); `git diff b68e5718df06 refs/stage2/attempts/plan-card-what-line/draft-attempt-2-20261122T084514406767Z` shows it.

Stage-2 call, 2026-11-22: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 1171 files, 5359 commits, 12 rules.

Stage-2 call, 2026-11-22: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1171 files, 5362 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-22

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-7 | MAJOR | SPEC | base | spec.md criterion 5; Terms, "`What:` value" | [AMBIGUITY] The Terms say how to build the `What:` value: join its indented continuation lines and fold line breaks to single spaces. Nothing says how to build the `For you:` value that criterion 5 compares it with, and real `For you:` lines do wrap (`plans/changes/archive/2026-11-16-midnight-stamp-test/plan.md:21-22`). F-1's triage settled only the `What:` side. Reading A: the `For you:` value is only the text on its label line. A wrapped `For you:` copied word for word into `What:` then compares the full `What:` text against the first line alone, never matches, and passes. Reading B: the `For you:` value is joined and folded the same way as `What:`. That same copy is then refused. The two readings also disagree on a one-line `What:` that copies a two-line `For you:`: passed under A, refused under B. The refuter's "identical values" cannot be built until one reading is chosen. | Opus | in spec — [DETAIL] decided by the orchestrator: the For you: value is built the same way as the What: value (continuation lines joined, line breaks folded to single spaces), and both are compared case-insensitively after collapsing whitespace. Reason: one rule for both sides of the comparison | — |
| F-8 | MINOR | SPEC | base | spec.md criterion 7 (with criterion 8) | [AMBIGUITY] Does an unreadable date count as a problem for every card, or only when the date would change the verdict? Reading A, every card: a drafted card with a valid `What:` still fails while, for example, the `date:` of the spec committed at the base is malformed. No attempt can fix that, because criterion 8 reads the committed copy (and the adoption record is a held path), so all three attempts fail. Reading B, only when it matters: the date is needed only to decide whether a card that fails the `What:` checks is exempt, so a card that passes those checks passes whatever the date. The refuter tests only a five-field card, and both implementations pass it. Nothing turns red if the date read is skipped for a valid six-field card. | Opus | in spec — [DETAIL] decided by the orchestrator: reading B — an unreadable date is a problem only when the card lacks a valid What:; a card with a valid What: passes whatever the date. Reason: the date only decides whether What: is required | — |
| F-9 | MINOR | SPEC | base | spec.md Terms, "Adoption day"; Definition of Done, second bullet | [AMBIGUITY] The adoption day "is this change's merge date", but `decisions/adoption.yaml` is a human-decided path that has to be written in this pull request, before the merge date is known. Reading A: the orchestrator writes a fixed day in the pull request (the day it is written, or the expected merge day), and "merge date" is an approximation. Reading B: the recorded day must equal the actual merge day, so it is set or corrected at merge time. Under A, if the merge comes later than the recorded day, a change first drafted on another branch in between becomes subject on its next re-draft. If the recorded day is later than the merge, plans drafted after the merge but on or before that day are exempt without `What:`. No criterion reads the recorded value, so neither choice can turn anything red. | Opus | in spec — [DETAIL] decided by the orchestrator: the cutoff is a dated constant in the check's own script, set to the day the pull request is opened, not decisions/adoption.yaml; the orchestrator updates it in the same PR if the merge slips past a day with drafted plans. Reason: no human-decided file, and the date is known when the PR is written | — |
| F-10 | MINOR | SPEC | base | spec.md criterion 2, refuter | Criterion 2 requires short, plain-language sentences that cover the present problem, one example, the change and the main risk. Its refuter fails the instruction only if it drops the example, the change or the risk, or allows more than three sentences. Picture an instruction like "`What:` <one example, what changes, the main risk; up to three sentences>". It drops "the present problem", "short" and "plain-language" and still passes the refuter. "Plain words, readable without the spec" is the core of the maintainer's request (decisions.md, the bead), yet no test of the prompt text can fail on it. | Opus | in spec — [DETAIL] decided by the orchestrator: the refuter also covers an instruction that drops the present problem or the plain-language requirement. Reason: all four parts and the plainness must be able to go red | — |

Stage-2 call, 2026-11-22: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1171 files, 5365 commits, 12 rules.

> Attempt 1 (codex) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/plan-card-what-line/draft-attempt-1-20261122T085708498369Z (f1f9840bc804); `git diff 96ef5cdd4886 refs/stage2/attempts/plan-card-what-line/draft-attempt-1-20261122T085708498369Z` shows it.

Stage-2 call, 2026-11-22: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1171 files, 5365 commits, 12 rules.

> Attempt 2 (codex-repair) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/plan-card-what-line/draft-attempt-2-20261122T085720136235Z (11b025625ab6); `git diff 96ef5cdd4886 refs/stage2/attempts/plan-card-what-line/draft-attempt-2-20261122T085720136235Z` shows it.

Stage-2 call, 2026-11-22: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 1171 files, 5365 commits, 12 rules.

Stage-2 call, 2026-11-23: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason GLM Flash: Z.ai 5-hour limit until 22:33 CET (bead coding-harness-363r.4); Sonnet answers on the default profile again · leak check clean over 1188 files, 5573 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/plan-card-what-line/plan.md` +11 -11
> - `scripts/stage2.py` +102 -9
> - `tests/test_check_question_context.py` +76 -0
> - `tests/test_run_report.py` +19 -1
> - `tests/test_stage2.py` +113 -0
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `tests/test_check_question_context.py`, `tests/test_stage2.py`.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> E       AssertionError: assert ['present pro...uation lines'] == []
> E         
> E         Left contains 6 more items, first extra item: 'present problem'
> E         Use -v to get more diff
>
> tests/test_check_question_context.py:243: AssertionError
> __________________ test_what_field_is_in_scope_widening_rule ___________________
> [gw2] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/plan-card-what-line/.venv/bin/python3
>
>     def test_what_field_is_in_scope_widening_rule() -> None:
>         # Criterion 9. Planted fault: What: leaves the widening rule, so an uncovered inclusion escapes approval.
>         paragraph = _widening_paragraph(_plan_prompt())
> >       assert "`What:`" in paragraph and "includes" in paragraph
> E       assert ('`What:`' in 'A card **widens** the scope when its `For you:` or `Done when:` line includes what `spec.md` names as a non-goal or n...efore phase 4 starts: its last line names what widens and asks for that "ok" in place of `Starts unless you say stop.`')
>
> tests/test_check_question_context.py:265: AssertionError
> ____________________ test_what_field_is_first_in_plan_card _____________________
> [gw1] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/plan-card-what-line/.venv/bin/python3
>
>     def test_what_field_is_first_in_plan_card() -> None:
>         # Criterion 1. Planted fault: What: elsewhere in the card, or an existing field moved.
>         plan = _plan_prompt()
> >       _assert_what_first(plan)
>
> tests/test_check_question_context.py:215: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> plan = '# Phase 3 · Plan\n\n**Model:** gpt-6.1-terra — Codex (`gpt-6.1-terra`) at effort [`CODEX_EFFORTS["draft"]`](../script...`/clear`. The plan is a file; whoever executes it does not need your\nreasoning, and fresh context beats continuity.\n'
>
>     def _assert_what_first(plan: str) -> None:
>         lines = _card_lines(plan)
> >       assert lines[0].startswith("What:"), "What: must be the card's first field"
> E       AssertionError: What: must be the card's first field
> E       assert False
> E        +  where False = <built-in method startswith of str object at 0x10923b570>('What:')
> E        +    where <built-in method startswith of str object at 0x10923b570> = 'For you:     <what changes for the maintainer>'.startswith
>
> tests/test_check_question_context.py:207: AssertionError
> ___________________ test_valid_what_passes_without_spec_date ___________________
> [gw10] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/plan-card-what-line/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3464/popen-gw...---|---|---|---|---|---|---|\n| R1 | MAJOR | SPEC | criterion 1 | spec.md:1 | FB1 unique body | Opus 5.5 | open | — |')
>
>     def test_valid_what_passes_without_spec_date(world: World) -> None:
>         # Criteria 12 and 3. Planted fault: the date is read before the card is judged.
>         for day in (None, "not-a-date", "2026-13-45"):
> >           assert draft_problems(world, PLAN_CARD, day) == [], day
> E           AssertionError: 2026-13-45
> E           assert ['Derived-fil... be in 1..12'] == []
> E             
> E             Left contains one more item: 'Derived-file preparation failed: index renderer exited 1\nTraceback (most recent call last):\n  File "/var/folders/44...return datetime.date(year, month, day)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nValueError: month must be in 1..12'
> E             Use -v to get more diff
>
> tests/test_stage2.py:5554: AssertionError
> ___________________ test_plan_card_refuses_unreadable_dates ____________________
> [gw9] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/plan-card-what-line/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3464/popen-gw...---|---|---|---|---|---|---|\n| R1 | MAJOR | SPEC | criterion 1 | spec.md:1 | FB1 unique body | Opus 5.5 | open | — |')
>
>     def test_plan_card_refuses_unreadable_dates(world: World) -> None:
>         # Criterion 7. Planted fault: an unreadable date lets a five-field card pass as old.
>         for day in (None, "yesterday", "2026-02-30"):
>             problems = draft_problems(world, WHAT_OLD_CARD, day)
> >           assert stage2.WHAT_DATE_PROBLEM in problems, (day, problems)
> E           AssertionError: ('2026-02-30', ['Derived-file preparation failed: index renderer exited 1
> E             Traceback (most recent call last):
> E               File ...tetime.date(year, month, day)
> E                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
> E             ValueError: day is out of range for month'])
> E           assert "`plan.md`'s card does not open with a valid `What:` line and the spec date, which decides whether `What:` is required, cannot be read" in ['Derived-file preparation failed: index renderer exited 1\nTraceback (most recent call last):\n  File "/var/folders/4...atetime.date(year, month, day)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nValueError: day is out of range for month']
> E            +  where "`plan.md`'s card does not open with a valid `What:` line and the spec date, which decides whether `What:` is required, cannot be read" = stage2.WHAT_DATE_PROBLEM
>
> tests/test_stage2.py:5605: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_check_question_context.py::test_what_field_requires_plain_explanation
> FAILED tests/test_check_question_context.py::test_what_field_is_in_scope_widening_rule
> FAILED tests/test_check_question_context.py::test_what_field_is_first_in_plan_card
> FAILED tests/test_stage2.py::test_valid_what_passes_without_spec_date - Asser...
> FAILED tests/test_stage2.py::test_plan_card_refuses_unreadable_dates - Assert...
> 5 failed, 7 passed in 18.17s
> ```
