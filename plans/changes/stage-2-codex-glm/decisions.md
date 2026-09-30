---
title: "Decisions — stage-2-codex-glm"
status: accepted
implementation_status: none
date: 2026-09-30
last_reviewed: 2026-09-30
updated: 2026-09-30
supersedes: null
superseded_by: null
bead: coding-harness-bc9
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# stage-2-codex-glm — Decisions

Phase 1a (interview), held with the maintainer on 2026-09-30 against
`research.md`, section "Open points for the phase 1a interview". The
maintainer answered from a phone, one question at a time.

## Decided before the interview

Relayed from the lakeswitch-ai session, where the maintainer decided the
routing on 2026-09-30; the one-page proposal itself was not approved there:

- Spec review (2a) on Codex `gpt-6.1-sol` at effort `max`; the same Codex
  agent does the review (6), resumed with `codex exec resume`.
- Implement (4) on Sonnet 5.5 at effort `medium`.
- Before phase 6, a review loop: GLM 5.3 at effort `max` reviews, Sonnet
  adapts, at most two rounds.
- Codex reads GLM's findings only after its own verdict.
- Kimi is dropped.
- Framework content only; customer code goes to neither vendor.

The same day the maintainer moved this work from the lakeswitch-ai session
to the Coding Harness session.

## Answers

1. **D-13 (four criteria before another vendor reviews): amend it by an
   ADR, option 1.** Criteria 3 (a green leak check) and 4 (a declared
   endpoint with residency) stay hard and are enforced by the runners on
   every call. Criterion 2 is stated to govern lakeswitch-ai content, which
   this change never sends. Criterion 1 (three measured full runs before)
   is replaced by measuring the first three stage-2 runs, with a stop rule.
   Accepted loss: no measured stage-1 baseline before the first foreign
   call.

2. **Scope: everything in one change, option 1.** All five work packages
   of the proposal, including the GLM loop, in one change and one pull
   request (estimated 9 to 11 hours, two sessions). The research
   recommended the smaller version; the maintainer chose the whole.

3. **Stage 2 by change class: yes, as a doctrine table, option 1.** A
   one-sentence change and a spike get no stage 2; `bounded` gets the GLM
   loop only, with review (6) on Fable 5.1; `feature` and `architectural`
   get Codex 2a, the GLM loop and Codex 6. No gate checks that a class is
   right; the table says so. Depends on the change classes of
   `feat/harness-decide-adr` (pull request #54) being merged first.

4. **The ADR: yes (ADR 0007).** Follows from answer 1 and was not asked
   separately: amending an interview decision goes through an ADR the gate
   `decision-continuity` maps. ADR 0007 records the D-13 amendment, where
   framework content may flow, and Kimi's removal. The pull request is
   therefore a decision PR.

5. **Measuring the first three stage-2 runs: in this change.** Follows from
   answer 1 and was not asked separately: it replaces criterion 1. Recorded
   per finding: reviewer, taken or rejected, and whether a taken finding
   turned a green test red. After three runs a short evaluation; if taken
   findings broke tests, stage 2 falls back to Fable.

6. **Personal-use declaration for the ChatGPT subscription: declare it,
   option 1.** In `model-endpoints.yaml`, dated 2026-09-30, with the same
   three expiry conditions as the GLM declaration, and the account's
   data-use setting recorded beside it (the maintainer reads it once; not
   read yet).

7. **Evidence rule for review findings: adopt as written, option 1.** A
   Codex or GLM finding is taken only when a test demonstrates it or the
   spec supports it; otherwise it is rejected with a reason and stays in
   `findings.md` as a disagreement. Applies to every repair round.
   Consequence accepted: a finding about something the spec does not cover
   needs a test, or it is rejected.

8. **Sonnet 5.5 for implement: every change, option 1.** One routing table
   for the whole repository, as with the routing decisions of 2026-09-29.

9. **One condition per acceptance criterion: in this change.** The sentence
   "One condition per criterion; where a trigger, state or failure applies,
   begin with When / While / If" goes into `prompts/02-spec.md` with this
   change, keeping the "Refuted by" rule. The research recommended a change
   of its own because pull request #54 edits the same file; the maintainer
   chose this change, so the edit lands after #54 is merged in.

## Consequences for the order of work

- This change's implementation starts after pull request #54 is merged and
  `origin/main` is merged into `feat/stage-2-codex-glm` (answers 3 and 9).
- Spec and plan may be written before that, against #54's branch.

## Addendum — after the spec review (2026-09-30)

Stated by the maintainer on 2026-09-30 in the coordinating Claude Code
session (<https://claude.ai/code/session_018qxAGMFNS3mM37eUEm5DuQ>), after the
phase 2a review, and relayed to the planning session by the coordinating
session. Recorded as relayed; the text above is unchanged.

10. **The appetite stays at 9–11 hours; the local proofs are dropped.** The
    maintainer's reason: data protection matters for LakeSwitch's content,
    not for Coding Harness's own, and stage 2 sends only Coding Harness
    content. Dropped: the local proofs of read confinement for both
    programs, of hooks and memories being off, and of which settings survive
    `codex exec resume`. Kept, because they cost nothing: model, effort and
    sandbox pinned on every call, standard input from `/dev/null`, and the
    session id read from the call's own `thread.started` event when the call
    runs. The leak check before every call stays: it is a hard criterion of
    D-13 (answer 1). This answers the phase 2a reviewer's estimate of 12–15
    hours (`findings.md`, "Scope against the appetite").

11. **The customer instance's checkout on the same disk is an accepted
    residual risk.** There is no confinement and no proof: the foreign
    reviewers can read the whole disk. Their prompts ask them to read
    nothing outside the worktree and the repository's git directory — a
    request, not a lock, and the doctrine and ADR 0007 say so in those
    words. The maintainer chose this over a proof of about one hour.

12. **Until stage 2 is implemented and merged, spec review (2a) and review
    (6) run on Opus 5.5 for the whole repository** (pull request #58, not
    merged on 2026-09-30), this change's own phase 6 included; when this
    change merges, its routing replaces those interim rows, and a review
    Codex does not do falls back to Fable 5.1, as answer 3 decided.

Consequences: `spec.md` criteria 22, 24 and 33 are changed and marked so;
the `[GAP]`s 1–4 of the spec are dropped; the numbering of the criteria is
unchanged.
