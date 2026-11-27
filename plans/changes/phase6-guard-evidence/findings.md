---
title: "Findings — phase6-guard-evidence"
category: findings
status: draft
implementation_status: none
date: 2026-11-26
created: 2026-11-26
last_reviewed: 2026-11-27
updated: 2026-11-27
supersedes: null
superseded_by: null
bead: coding-harness-mwzv.6
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-26"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — phase6-guard-evidence

Stage-2 call, 2026-11-26: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1294 files, 6062 commits, 12 rules.

Stage-2 call, 2026-11-26: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1297 files, 6063 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-26

Spec fingerprint: sha256:605025bd7b72e83436f8de14cf87674bf3cdea6e6fbb836a09422940609b500b

Spec review commit: 970c5c6f67cdae4344c02f7218194b2444573b9f

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | [AMBIGUITY] | SPEC | base | spec.md, AC1 and AC4; decisions.md Q-1 ("natural sentence punctuation", "including") | Reading A: AC1 is a closed list. Only `yes.`, `yes. <text>`, `no. <reason>` and `no — <reason>` join today's forms. `yes — <text>`, `Yes.`, `No, <reason>`, `no - <reason>` (hyphen), `no – <reason>` (en dash) and `yes!` stay refused, so a Codex line ending `catches without switch: yes — the assertion fails` still throws away the whole review. Reading B: Q-1 names a class ("sentence-ending punctuation … including", "natural sentence punctuation"), and those variants are accepted too. AC4's "a verdict other than `yes` or `no`" then has to say whether capitalised `Yes`/`No` count. The two readings give different regexes and different AC4 refutation cases. | Opus | in spec — Reading B closed grammar (case-insensitive yes/no, trailing ./!, separator [,;:.!—–-]) recorded in AC1 & [DETAIL] S-1 (bounded standing grant) | — |
| S-2 | [AMBIGUITY] | SPEC | base | spec.md, AC2; decisions.md Q-1 ("minor harmless Markdown wrapping such as backticks around the test path"); scripts/stage2.py:341-342, :4894 | Reading A: AC2 literally. Only backticks around the whole node id (`` `tests/x.py::test_y` ``) are accepted. Reading B: Q-1's "such as". Other harmless wrapping is accepted too: the path alone (`` `tests/x.py`::test_y ``), the whole line in backticks as the prompt's own template prints it (stage2.py:341-342), or a bold `**Guard evidence:**` label. Under A these lines refuse the answer beside `No finding.`. Beside finding rows they are silently ignored, because `phase6_rows` refuses only lines whose stripped text begins `Guard evidence:` (stage2.py:4894). So a malformed wrapped line ending `catches without switch: maybe` passes beside a finding. Under B they are guard-evidence lines: a well-formed one is accepted, and AC4 must refuse a malformed one. | Opus | in spec — Reading A (backticks on node ID or file path only; no bold/whole-line wrapping) recorded in AC2, Non-goals & [DETAIL] S-2 (bounded standing grant) | — |
| S-3 | [AMBIGUITY] | SPEC | base | spec.md, Protected areas and Definition of Done; decisions.md Q-1 ("and `PHASE6_GUARD_EVIDENCE` if clarifying examples help") | Reading A: `PHASE6_GUARD_EVIDENCE` and `PHASE6_ANSWER_FORMAT` are "review instructions outside the existing parser", so they are protected. The prompt keeps `<yes\|no and reason>` and its backtick-wrapped template line. Reading B: they belong to the parser surface that Q-1 lets the change edit, so the prompt may show the newly accepted forms and Codex gets different instructions. The DoD check ("shown by the pull request's file list") cannot tell the two apart: both constants live in `scripts/stage2.py`, which this change edits anyway. | Opus | in spec — Reading A (prompt constants untouched; parser + tests only) recorded in Protected areas, Non-goals & [DETAIL] S-3 (bounded standing grant) | — |
| S-4 | MAJOR | SPEC | base | spec.md, AC4 ("a missing fault") and AC6; scripts/stage2.py:387; tests/test_stage2.py:23209, :23278 | The spec never says what counts as a "missing fault". The fault group `\S.+?` needs at least two characters, so today a one-character fault such as `fault: x` is refused. AC4 does not say whether that is a missing fault, and AC6 does not protect it, so the implementer has to decide. The existing fixtures for the verdict cases use exactly that fault: the `maybe` line at :23209 and the bare-`no` assertion at :23278. They are refused because of the fault, not the verdict word, and stay green even if `maybe` or a bare `no` were accepted. Regression tests for AC4 built from them cannot go red on AC4's "verdict other than yes or no" or "no without a reason" cases. | Opus | in spec — non-empty fault >= 1 non-whitespace char (`\S.*?`) and multi-char faults in verdict tests recorded in AC4, DoD & [DETAIL] S-4 | — |
| S-5 | MINOR | SPEC | base | spec.md, AC2 ("parametrized test ID") | The spec does not say what may stand inside the brackets. pytest IDs can contain spaces, hyphens, dots, `/`, nested brackets and ` — `. The implementer has to pick a character class (`[\w-]+`, `[^\]\s]+`, `[^\]]+`), and `tests/x.py::test_y[a b]` or `test_y[1.5-x/y]` is accepted by one and refused by another. AC2's refutation does not say which. It is also silent on whether an empty `test_y[]` is valid. | Opus | in spec — `\[[^\]]+\]` (non-empty brackets, rejecting `[]`) recorded in AC2 & [DETAIL] S-5 | — |
| S-6 | MINOR | SPEC | base | spec.md, AC6 (Refuted by); scripts/stage2.py:388 | AC6's condition covers every form already accepted, but its refutation lists only a bare `yes` and a `yes` or reasoned `no` with a comma, semicolon or colon. The current regex makes that punctuation optional (`[,;:]?`), so `yes <text>` and `no <reason>` with only a space are accepted today. A change that stops accepting them breaks AC6's condition, yet the stated refutation case does not catch it. | Opus | in spec — space-only `yes <text>` and `no <reason>` added to AC6 Refuted by & [DETAIL] S-6 | — |

Stage-2 call, 2026-11-27: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1297 files, 6069 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-27

Spec fingerprint: sha256:b7170a9a9da746e259884697def25ad117b42056fc26ee74f944690139d5e98c

Spec review commit: d1b0c9697ef17103c249e541daf02e19f6555e7c

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-7 | [AMBIGUITY] | SPEC | base | spec.md, AC1 and AC4; spec.md, [DETAIL] Spec-review S-1 | AC1 and the recorded decision give different separator sets for `no`. AC1 allows `[,;:.—–-]` before a `no` reason, with no `!`. The [DETAIL] for S-1 records one set for both words, "`[,;:.!—–-]` before prose/reason (`yes` prose optional; `no` reason mandatory)", which includes `!`. AC4 lists `no!` only among the forms that have no reason. Reading A (AC1): `catches without switch: no! it only fails under the switch` is not evidence, so the answer is refused, even beside a valid verdict. Reading B (the [DETAIL]): the line is valid evidence and the answer is accepted. The two readings need different regexes, and no criterion goes red under either one. | Opus | in spec — Reading B uniform separator set `[,;:.!—–-]` recorded in AC1 & [DETAIL] S-7..S-10 (bounded standing grant) | — |
| S-8 | [AMBIGUITY] | SPEC | base | spec.md, AC1, AC4 and AC6; scripts/stage2.py:388; decisions.md Q-1 ("accepting no relaxation of the requirement that every `no` carries an explicit reason") | AC1's grammar is `no`, then optional punctuation, then whitespace, then a reason. Its own example `no — <reason>` has a space before the dash, so it only fits if `— <reason>` is itself the reason. Reading A: punctuation after the space counts as reason text, as it does today (`no[,;:]?\s+\S.*`). Then `catches without switch: no —`, `no -` and `no .` are accepted, and AC6 requires that because they are accepted today. Reading B: a dash or mark after the space is a separator and a reason must follow it. Then those lines are a `no` without a reason, which AC4 and Q-1 refuse, and AC6 breaks. The two criteria contradict each other on these lines. The answer decides whether a cut-off `no —` releases a verdict. | Opus | in spec — Reading B recorded in AC1, AC4, AC6 & [DETAIL] S-7..S-10 (`no` reason requires >=1 `\w`, rejecting `no —`/`no -`/`no .`) | — |
| S-9 | MINOR | SPEC | base | spec.md, AC1, AC2 and AC4; spec.md, [DETAIL] Spec-review S-1 ("explicit closed grammar") | The [DETAIL] calls the grammar closed, but AC4 refuses only the forms it lists. No criterion goes red when the parser accepts forms outside AC1 and AC2. Examples: `yes?`, `yes…`, a single unpaired backtick (`` `tests/x.py::test_y ``), or a whole-pattern `re.IGNORECASE`. AC1 makes only the verdict word case-insensitive, but that flag would turn `guard evidence: … — FAULT: … — CATCHES WITHOUT SWITCH: yes` into evidence. Beside `No finding.` that line refuses the answer today, and it would then be accepted. A parser built with `(?i)` and `\W*` after the verdict word passes all six criteria. | Opus | in spec — AC2 & AC4 tightened (`(?i:yes|no)` only; wrong-case labels, `yes?`/`yes…`, unpaired backticks refused) | — |
| S-10 | MINOR | SPEC | base | spec.md, AC2 | AC2 names backtick wrapping and a parametrized suffix as alternatives, and its refutation tests each one alone. A parser can accept `` `tests/x.py::test_y` `` and `tests/x.py::test_y[case]` but refuse `` `tests/x.py::test_y[case]` ``. That is the full node ID in backticks, which AC2's own words describe, and the parser still meets every stated refutation. The spec also does not say whether the suffix may stand outside the backticks (`` `tests/x.py::test_y`[case] `` or `` `tests/x.py`::test_y[case] ``), so whoever implements it has to decide. | Opus | in spec — AC2 explicitly covers combined backticks + `[<id>]` and refuses split `` `node`[id] `` | — |
