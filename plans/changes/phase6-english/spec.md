---
title: "Spec — phase6-english"
status: draft
implementation_status: none
date: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
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

The phase-6 reviewer is asked to answer in English, and a detected German verdict gets one further chance without losing a second German verdict (bead coding-harness-tscc). Research: `research.md`. Decisions: `decisions.md`.

## Problem

On 2026-11-19 and 2026-11-20, German finding text was recorded in phase-6 verdicts although repository documents are English; the examples and the maintainer's remedy are recorded in `research.md` and `decisions.md` (2026-11-22). The phase-6 prompt does not ask for English, and the runner accepts German finding rows because its format check is language-neutral. The runner currently rejects malformed phase-6 verdicts without a retry; the retry for malformed output identified by the research belongs to the separate review loop.

## Terms

**Detected German verdict:** a structurally valid phase-6 verdict whose finding cells pass the dependency-free German-language heuristic described in `decisions.md`; it is an approximation, not a general language classifier.

## Acceptance criteria

1. When phase 6 requests a verdict, the reviewer-facing phase-6 prompt says `Answer in English.`
   *Refuted by:* the prompt used for a verdict omits that instruction.
2. When finding text from the recorded German phase-6 verdicts is assessed, the heuristic detects it as German.
   *Refuted by:* a recorded German verdict from `slip-counter` on 2026-11-19 or 2026-11-20, or `loop-record-other-worktree` on 2026-11-20, passes without detection.
3. When English phase-6 finding text includes code spans, paths or identifiers, those tokens do not by themselves cause German detection.
   *Refuted by:* an English finding is flagged solely because a code span, path or identifier contains German words or letters.
4. When the first structurally valid verdict is detected as German, the runner requests one replacement in English in the same reviewer thread before recording a verdict or releasing loop rows.
   *Refuted by:* the runner accepts the first German verdict, releases rows first, starts a different reviewer thread, or requests more than one replacement.
5. When the replacement is structurally valid and detected as German, the runner records it as the verdict with a notice that it was kept although detected as non-English.
   *Refuted by:* the runner discards or translates that replacement, omits the notice, or calls the reviewer a third time.
6. When the replacement is structurally valid and not detected as German, the runner records the replacement as the verdict without a non-English notice.
   *Refuted by:* the first verdict is recorded instead, or the replacement is accompanied by the non-English notice.
7. When a verdict is malformed, the existing malformed-verdict rejection and no-release behavior remains in force, including for a replacement.
   *Refuted by:* a malformed answer creates an authoritative verdict, releases loop rows, or is accepted because it is the replacement.
8. When a verdict requires no language retry, the existing verdict, release, and loop-mark sequence remains in force.
   *Refuted by:* a valid English finding or `No finding.` receives an extra verdict call, or the verdict, release and mark order changes.
9. When the runner makes the replacement call, the existing per-call leak check and call audit apply to it.
   *Refuted by:* the replacement reaches the reviewer after a leak-check refusal, or its call has no audit record.

## Non-goals

- Translating or rewriting recorded verdicts, or changing phase-2a review and phase-4b review-loop behavior.
- Detecting every non-English language or guaranteeing the language of loop-row marks, guard-evidence text, quoted material or runner display messages; the heuristic examines finding cells only.
- Introducing a language-detection dependency or changing the malformed-verdict policy.

## Protected areas

Historical findings and runner display texts remain unchanged; they are evidence and outside the maintainer's selected remedy. No ADR or model endpoint changes are needed.

## Definition of Done

- `make verify` green; the same pull request updates `docs/WORKFLOW.md` and `prompts/06-review.md` alongside the runner and tests.
- Protected areas untouched and non-goals unbuilt, shown by the pull request's file list.
- The pull request closes bead coding-harness-tscc and its last commit carries `Closes-Bead: coding-harness-tscc`.
- Special runs: none.

## Open decisions

None open.

[DETAIL] The retry covers verdict finding cells only, as decided in `decisions.md`; the separately generated loop marks remain outside detection even though research found German marks too. A bounded heuristic can miss other languages or very short German text and can misclassify mixed prose; it is not a language guarantee.

[DETAIL] There is no existing malformed-answer retry in phase 6 to share: retain its rejection behavior and use one language retry for a structurally valid German verdict. This implements the specified one-retry remedy without changing a separate failure policy.

[DETAIL] Three hours of phase 4, including repairs, is the stop for this bounded change; it leaves time to calibrate against the recorded examples and exercise the retry boundary.
