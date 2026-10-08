---
title: "Findings — touch-map-comments"
category: findings
status: draft
implementation_status: none
date: 2026-10-08
created: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-08
supersedes: null
superseded_by: null
bead: coding-harness-cff
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — touch-map-comments

Stage-2 call, 2026-10-08: review-loop · endpoint glm-coding-plan · model glm-5.3 · leak check clean over 269 files, 632 commits, 12 rules.

Stage-2 call, 2026-10-08: review-loop · endpoint glm-coding-plan · model glm-5.3 · leak check clean over 270 files, 633 commits, 12 rules.

Stage-2 call, 2026-10-08: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 270 files, 634 commits, 12 rules.

## Phase 6 — Codex, 2026-10-08

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | BLOCKER | SPEC | fix-r2 | `scripts/touch_map.py:252` | For valid Bash `echo x$'a\'b' # scripts/comment_tool.py`, followed by another comment, the word-start restriction misclassifies the ANSI-C string as plain single quotes. Both comments survive and produce false links. Both must be removed; commit `829c44d` handled this input correctly. [AC 2] | Codex | closed — 7d6b62d; F-1 case in test_a_substitution_nests_its_own_quotes | no |
| F-2 | BLOCKER | MAINT | base | `scripts/touch_map.py:238` | For valid Bash `echo "$$(" # scripts/comment_tool.py`, `$$` expands to the process ID and `(` is literal. The scanner instead opens a substitution at the second dollar, retains this and subsequent comments, and creates false links. The baseline correctly removed those comments. | Codex | closed — 7d6b62d; F-2 case in test_a_substitution_nests_its_own_quotes | no |
| F-3 | BLOCKER | SPEC | base | `scripts/touch_map.py:256` | For `x="$(case x in\nx)\n# scripts/comment_tool.py\nprintf '%s' ok;;\nesac)"`, with `\n` representing newlines, the scanner closes the substitution at the case pattern’s `x)`. It consequently preserves the comment and creates a false link. The substitution ends at `esac)`; the intervening comment must be removed. [AC 1] | Codex | closed — 7d6b62d; F-3 case in test_a_substitution_nests_its_own_quotes | no |

Phase 6 verdict: codex 01a118d3-3548-7d30-bfd2-2892d1942ef6, 2026-10-08
Reviewer session: codex 01a118d3-3548-7d30-bfd2-2892d1942ef6 — a fresh session reviewed: no phase-2a session was recorded

## Phase 4b — GLM loop rows, released 2026-10-08

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MINOR | MAINT | test | tests/test_touch_map.py:491 | Every new case opens and closes the command substitution on a single line, so no test pins the scanner's central mechanism — a substitution context carried across lines; a later refactor that resets the state stack at each line keeps the whole suite green and silently turns a comment inside a multi-line substitution back into code. | GLM | taken — multi-line substitution case in test_a_substitution_nests_its_own_quotes | no | agree |
| L1-2 | MINOR | MAINT | code | scripts/touch_map.py:251 | An apostrophe is tagged as the ANSI-C kind by looking only at the raw previous character, so after a backslash-escaped dollar the quote is treated as backslash-escaping: in a line like `echo \$'a\'b' # c` the shell keeps the backslashes literal, leaves the hash inside a quote that runs on to the next lines, while the scanner strips the hash as a comment — the escaped dollar is invisible to the look behind. | GLM | taken — escaped-dollar case in test_a_substitution_nests_its_own_quotes | no | agree |
| L2-1 | MINOR | MAINT | round 2 | scripts/touch_map.py:251 | The ANSI-C test takes any `$` before an apostrophe as the opening of `$'…'`, so in `$$'a\' # c` — the shell's PID parameter followed by a plain quote — the backslash escapes the closing apostrophe, the string stays open past the end of the line, and the `#` text is kept as code with the open string carried into the next line, where a comment read as code can make a false link; the shell reads `'a\'` as a closed plain quote and `# c` as a comment. Requiring the `$` to start a word (after a blank, `=`, `(` or at the start of the line) keeps the two readings apart. | GLM | taken — `$$'` case in test_a_substitution_nests_its_own_quotes; `$'` counts only where the `$` starts a word | no | agree |
| L2-2 | MINOR | MAINT | round 2 | tests/test_touch_map.py:505 | The two added asserts are tagged `loop row L1-1` and `loop row L1-2`, identifiers of the review-loop record, which is kept outside the repository; nothing in the worktree resolves them — the change's own findings file holds no rows — so a maintainer reading the suite cannot look up what the tags refer to. | GLM | rejected — release-loop copies these rows into findings.md after the phase-6 verdict, where the ids resolve |  | disagree — The assertions explain their cases locally; unresolved loop identifiers demonstrate no correctness fault, spec gap, or ineffective gate. |

Rounds run: 2

Kept from the loop record:

The answer was not only six-cell rows; what is not one is kept below as it came.

|R-3|MINOR|MAINT|doc|scripts/touch_map.py:283|The docstring's list of quotes the scanner still misreads reads as complete but leaves out an apostrophe in a YAML word that does not sit between two letters — a value that ends the line, `name: Don't` — which still opens a quote and flips the rest of the file, exactly the failure mode the change set out to remove.

Stage-2 call, 2026-10-08: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 270 files, 634 commits, 12 rules.

Stage-2 call, 2026-10-08: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 270 files, 636 commits, 12 rules.

## Phase 6 — Codex, 2026-10-08

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-4 | BLOCKER | SPEC | fix-r3 | `scripts/touch_map.py:273` | For valid Bash `x="$(echo case)" # scripts/comment_tool.py`, followed by another comment, the scanner treats the argument `case` as a reserved word. Its unmatched case counter prevents the substitution from closing, so both comments survive and produce false links. Both must be removed; `9453197` handled this input correctly. [AC 1] | Codex | closed — 4e678b0; F-4 case in test_a_substitution_nests_its_own_quotes | no |
| F-5 | BLOCKER | SPEC | fix-r3 | `scripts/touch_map.py:226` | For `x="\\$(\n# scripts/comment_tool.py\n)"`, where `\\` means two backslashes and `\n` means newlines, Bash recognizes the substitution because the backslashes escape each other. `_live_dollar` instead treats the dollar as escaped, preserves the inner comment and creates a false link. The comment must be removed; `9453197` handled this input correctly. [AC 1] | Codex | closed — 4e678b0; F-5 case in test_a_substitution_nests_its_own_quotes | no |
| F-6 | BLOCKER | SPEC | base | `scripts/touch_map.py:285` | For valid Bash `x="$(printf %s ${v%)}\n# scripts/comment_tool.py\n)"`, with `\n` representing newlines, the `)` inside `${v%)}` belongs to the suffix-removal pattern. The scanner incorrectly closes the command substitution there, preserving the subsequent comment and creating a false link. Only the final `)` closes the substitution; the comment must be removed. [AC 1] | Codex | closed — 4e678b0; F-6 case in test_a_substitution_nests_its_own_quotes | no |

Phase 6 verdict: codex 01a118d3-3548-7d30-bfd2-2892d1942ef6, 2026-10-08
