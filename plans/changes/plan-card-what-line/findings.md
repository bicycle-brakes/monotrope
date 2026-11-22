---
title: "Findings — plan-card-what-line"
category: findings
status: draft
implementation_status: none
date: 2026-11-22
created: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
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
