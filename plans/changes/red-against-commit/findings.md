---
title: "Findings — red-against-commit"
category: findings
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-qvf7
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — red-against-commit

Stage-2 call, 2026-11-21: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1162 files, 5204 commits, 12 rules.

Stage-2 call, 2026-11-21: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1165 files, 5210 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-21

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | MAJOR | SPEC | base | criterion 1, criterion 7, Open decisions (second [DETAIL]) | [AMBIGUITY] Criterion 1 says the selected commit is "retained in the resulting fixed status", and the [DETAIL] says the "resolved full commit ID" goes into "evidence". Reading A: the Status keeps the SHA as the fixed line wrote it, which may be abbreviated, and only the `Broke a test` mark carries the full ID. Reading B: the runner rewrites the Status to `fixed — tests/<path>::<function> — red against <full sha>`. This matters because the runner writes only the Status cell of a findings.md row (`mark_repaired_findings`, scripts/stage2.py:8813). Marks go only to loop-record rows (`_mark_record_rows`, 8892). Under A, a phase-6 row keeps only the short input, which the [DETAIL]'s own reason says can later become ambiguous. A test for criterion 1 that checks the Status text passes under one reading and fails under the other. | Opus | open | — |
| S-2 | MAJOR | SPEC | base | criterion 7, Definition of Done (files that move) | *What is missing.* The spec never gives the text of the success mark for a selected-commit proof. Today an ordinary proof gets `yes — <anchor>` (scripts/stage2.py:8755) and a guard proof gets `yes — guard test — <anchor>` (8744). The builder has to invent the new form: a suffix on the ordinary mark, its own label, or something else. Until a form exists, criterion 7's refutation ("a mark omitting or misidentifying the commit") can only be checked against whatever the builder picks. Several places tell the orchestrator which marks to write by hand: `prompts/04b-review-loop.md` step 3 (lines 108–111), `RECORD_INTRO` (scripts/stage2.py:610–616) and `templates/findings.md`:120. The spec does not say whether any of them names the new mark, and only `RECORD_INTRO` sits in a file on the Definition of Done list. | Opus | open | — |
| S-3 | MAJOR | SPEC | base | Definition of Done (`prompts/04-implement.md` moves), criterion 11, Protected areas | *What is missing.* `prompts/` is in `RUNNER_HELD` (scripts/stage2.py:7745), so `uncommittable` refuses any stage-2 attempt that changes `prompts/04-implement.md`. Yet the Definition of Done requires that file to move with the change, and criterion 11 depends on it. The accepted precedent, guard-test's spec under Protected areas, says runner-held paths stay protected during model attempts and that the coordinated updates are listed in the plan. This spec says nothing about who edits the held prompt, in which phase, or outside which runner step. If nobody decides, the phase-4 checkpoint refuses the change, or the prompt edit is dropped. | Opus | open | — |
| S-4 | MAJOR | SPEC | base | criterion 11, Terms "Saved attempt", decisions.md [DETAIL] "Where the commit is named" | *What is missing.* The repair attempt writes the SHA into its fixed line, but nothing says how it learns which commit comes before the fix or which saved-attempt refs exist for this change. The Sonnet fallback runs "with the available file tools; you cannot run commands" (`REPAIR_FORMAT_FILE_TOOLS`, scripts/stage2.py:389–394), so it cannot list refs or read history. No prompt today names saved-attempt refs. The builder has to decide among three options: the runner puts candidates (the run-start HEAD and this change's saved-attempt refs) into the repair prompt, the orchestrator passes a SHA in the taken reason, or the attempt finds the commit itself. In the bead's case, the fix already committed, the last option leaves the form usable on the Codex route only. | Opus | open | — |
| S-5 | MAJOR | SPEC | base | criterion 1 (`<sha>`), criterion 2 ("malformed") | *What is missing.* The spec never defines what `<sha>` accepts, so "malformed" has no boundary. Open questions: whether only hex object names count; the minimum and maximum length (Git abbreviates down to 4 characters, and SHA-256 IDs have 64); whether upper case is allowed; whether revisions such as `HEAD~1`, a branch name or a tag name are malformed or valid if they resolve to an eligible commit. It also does not say where the token ends when text follows it on the line. The parser and criterion 2's "malformed" refutation inputs have to be invented, and two builders could disagree on whether `red against HEAD~1` is refused. | Opus | open | — |
| S-6 | MINOR | SPEC | base | criterion 2 ("ambiguous") | [AMBIGUITY] Reading A: an abbreviation is ambiguous if it is a prefix of two objects of any type in the store, which is what plain `git rev-parse` refuses. Reading B: it is ambiguous only if it is a prefix of two commits, which is what Git's commit-type lookup does (`<prefix>^{commit}` picks the commit). Test input: a prefix shared by one commit and one blob or tree. Reading A refuses it and B accepts it. The private clone copies unreferenced objects too (`_private_repository`, scripts/stage2.py:8050), so such collisions count wherever the check runs. | Opus | open | — |
| S-7 | MINOR | SPEC | base | criterion 2 ("not an ancestor of the run-start HEAD"), Terms "Saved attempt" ("reachable from") | [AMBIGUITY] Test input: `red against <run-start HEAD>`. Reading A, inclusive (`git merge-base --is-ancestor` counts a commit as its own ancestor, and the Terms say "reachable from", which includes a saved ref's tip): HEAD is eligible. The proof then matches the ordinary form, but the Status and mark carry the suffix. Reading B, strict ancestor: HEAD is refused with a reason. The spec also does not say whether HEAD and a saved-attempt tip are treated alike. | Opus | open | — |
| S-8 | MINOR | SPEC | base | criterion 9 (`not a test` form) | [AMBIGUITY] A `not a test` reason is free text: `fixed_status` takes everything after the first dash as the reason (scripts/stage2.py:8552–8558). Test input: `fixed — not a test — docs only — red against 1a2b3c4d` on a row taken `taken — not a test — …`. Reading A: refused, because criterion 9 says "the selected-commit suffix is refused". Reading B: accepted as today, because the reason is free text and criterion 9 also says the form's "existing … rules remain in force". The criterion's two halves give opposite results for this line. | Opus | open | — |
