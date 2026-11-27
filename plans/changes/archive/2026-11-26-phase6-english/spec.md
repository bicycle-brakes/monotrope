---
title: "Spec — phase6-english"
status: accepted
implementation_status: done
date: 2026-11-22
last_reviewed: 2026-11-26
updated: 2026-11-26
supersedes: null
superseded_by: null
bead: coding-harness-tscc
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, phase-6, language]
class: bounded
appetite: 3
adr_files: []
---

# Spec — phase6-english

The phase-6 reviewer is asked for an English verdict, and a detected German verdict gets one further chance without discarding a valid answer (bead coding-harness-tscc). Research: `research.md`. Decisions: `decisions.md`.

## Problem

On 2026-11-19 and 2026-11-20, phase-6 findings were recorded in German despite the repository's English rule; `research.md` identifies the verdicts and the maintainer's remedy (2026-11-22). The verdict prompt does not ask for English and the language-neutral format check accepts German finding rows. Phase 6 currently rejects malformed verdicts without retry; the research found a separate retry in the review loop.

## Terms

**Detected German verdict:** one fixed, dependency-free heuristic scores the concatenated Finding column (the sixth cell) of all rows in a structurally valid reviewer verdict. It excludes text inside paired backticks and double quotation marks (`"…"`, `“…”`, `„…“` and `«…»`) before counting; outside those spans, tokens containing a slash, a dot between word characters, an underscore or a `:line` suffix are excluded. Single quotation marks and apostrophes are not quotation delimiters. A verdict without finding rows is never detected as German. This is an approximation, not a general language classifier: a German row among English rows can be missed.

## Acceptance criteria

1. When phase 6 requests a verdict, `prompts/06-review.md` tells the reviewer `Answer in English.`
   *Refuted by:* the verdict prompt omits that instruction.
2. When the recorded German verdicts from `slip-counter` on 2026-11-17 (reviewer rows R-1 and R-2 only, excluding the orchestrator's H-1), 2026-11-19 and 2026-11-20 and `loop-record-other-worktree` on 2026-11-20 are assessed, the heuristic detects each verdict as German.
   *Refuted by:* any of those verdicts passes undetected.
3. When the recorded English verdicts from `slip-counter` on 2026-11-20 (P6-1 and P6-2 together) and `loop-record-other-worktree` on 2026-11-20 (F6-1) and 2026-11-21 (R6-1 through R6-3) are assessed, the heuristic does not detect them as German.
   *Refuted by:* any of those three verdicts is detected as German.
4. When an English finding contains German text inside paired backticks or any specified pair of double quotation marks, or contains tokens matching the specified path and identifier rule, those excluded tokens do not contribute to its German score.
   *Refuted by:* adding any of those excluded tokens changes the score or makes the finding German.
5. When a valid first verdict is detected as German, its evidence is saved and the retry passes admission, the runner requests exactly one replacement by resuming its reviewer thread before recording a verdict or releasing loop rows.
   *Refuted by:* the first verdict is immediately accepted, rows are released first, the request does not resume the first thread, or more than one replacement is requested.
6. When requesting that replacement, the runner asks in one sentence for the same findings again in English in the same table form.
   *Refuted by:* the reminder omits English, the same findings or the same table form.
7. When a structurally valid replacement is returned, the runner records that replacement as the verdict without comparing its findings with the first answer.
   *Refuted by:* the runner records the first answer instead, rejects a changed finding or `No finding.`, translates the replacement, or changes its reviewer text.
8. When the recorded replacement is detected as German, the verdict block says it was kept although detected as non-English.
   *Refuted by:* the notice is absent or another replacement is requested.
9. When the recorded replacement is not detected as German, the verdict block has no non-English notice.
   *Refuted by:* the notice is present.
10. When a replacement is recorded, the first answer is retained in a protected local answer file whose path is named in a notice in the verdict block, and is not quoted in `findings.md`.
    *Refuted by:* the file cannot be retrieved from the named path while the worktree exists, or the first answer is quoted in the findings.
11. When a recorded replacement comes back on a different reviewer thread, the verdict uses that returned thread, the session record names both threads, and the marks call resumes the returned thread.
    *Refuted by:* the new thread is rejected or either thread is absent from the session record, or the verdict or marks use the old thread.
12. If the replacement is malformed or its call fails or returns no thread, other than a leak-check block, the runner records the first valid verdict with a non-English notice naming the replacement failure and proceeds with the first thread; if a malformed answer returned another thread, the notice also names both threads.
    *Refuted by:* the malformed or failed replacement becomes the verdict, the first verdict or failure notice is lost, a returned different thread is omitted, or the marks use another thread.
13. If the replacement's leak check blocks, the review stops without a fallback verdict or releasing loop rows.
    *Refuted by:* a replacement call, fallback verdict or release follows the block.
14. When the first verdict is malformed, the existing rejected-evidence and no-release behavior remains in force.
    *Refuted by:* a malformed first answer creates a verdict or releases rows.
15. When a valid verdict needs no language retry, the existing verdict, release and loop-mark sequence remains in force.
    *Refuted by:* `No finding.` or a valid English finding gets another verdict call, or verdict, release and mark order changes.
16. When the runner starts a language replacement call, its own leak check and the distinct `review (language retry)` audit line apply.
    *Refuted by:* the call bypasses its leak check or has no correctly labelled audit line.
17. When the findings differ from the committed version only by permitted review audit lines including `review (language retry)`, the existing fresh-verification check accepts that audit-only difference.
    *Refuted by:* the new audit line alone causes a dirty-tree refusal, or non-audit edits are accepted.
18. When a valid first verdict is detected as German and evidence saving succeeds, the runner saves its answer as protected local evidence before attempting the replacement, including when the replacement leak check later blocks.
    *Refuted by:* the replacement is attempted before the file is saved, or a blocked replacement leaves no saved first answer.
19. If saving the first answer as protected evidence fails, the runner asks for no replacement and records the first verdict with a notice naming the save failure.
    *Refuted by:* a replacement is requested, or the first verdict or failure notice is missing.

## Non-goals

- Translating historical verdicts; changing phase-2a review, the phase-4b review loop, or the phase-6 loop-marks prompt.
- Detecting every non-English language or guaranteeing the language of loop marks, guard evidence, quotations or display messages.
- Introducing a language-detection dependency or Codex call time limits, or changing the treatment of a malformed first verdict.

## Protected areas

Historical findings and runner display texts remain unchanged: they are evidence or outside the selected remedy. Model endpoints and ADRs are outside this bounded change.

## Definition of Done

- `make verify` green; the same pull request updates `docs/WORKFLOW.md` and `prompts/06-review.md` alongside the runner and tests.
- Protected areas untouched and non-goals unbuilt, shown by the pull request's file list.
- The pull request closes bead coding-harness-tscc and its last commit carries `Closes-Bead: coding-harness-tscc`.
- Special runs: none.

## Open decisions

None open.

[DETAIL] The scored unit is the combined Finding cells, with paired quotation marks and backticks excluded; this gives one score per answer and avoids penalising a quotation. The recorded examples pin both sides of the threshold. The heuristic can miss short or mixed German prose and misclassify other prose.

[DETAIL] A failed replacement retains the valid first verdict, as the orchestrator decided in spec-review row S-2. A leak-check BLOCK is the exception: the repository's rule requires the run to stop without fallback. The verdict and marks prompts remain separate; marks are outside this remedy.

[DETAIL] The replacement reminder asks for the same findings and table in English; the resumed thread already holds the guard-evidence instructions. The runner retains the first answer as protected evidence instead of quoting a second verdict.

[DETAIL] The held prompt is edited and its prompt test added by the orchestrator after the accepted implementation attempt. Three hours of phase 4, including repairs, is the stop for this bounded change.

[DETAIL] A structurally valid replacement can change or remove findings, including BLOCKERs; the runner does not compare the answers because it cannot judge their meaning. The local evidence file is not carried by a branch push and disappears with its worktree. Straight and typographic double quotes are excluded, but apostrophes are not; the path and identifier rule is deliberately finite and testable.
