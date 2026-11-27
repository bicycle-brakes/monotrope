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
