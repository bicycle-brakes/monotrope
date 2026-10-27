---
title: "Decisions — review-loop-deep-b"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-27
supersedes: null
superseded_by: null
bead: coding-harness-pc7g
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# review-loop-deep-b — Decisions

Class: bounded (one counted interview record or a reasoned skip owed).

## Q-1 · Which defects of the deep review are fixed

context: |
  Topic: the deep review of the review loop, part B (DL-B-1 to DL-B-14),
  and two research-swarm rows that reach main's overlay (RS-3-3, RS-3-8).
  Intention: decide whether the runner defects the reviewers found are
  repaired now or left as findings.
  Today: the reviews reported them with reproductions; nothing was changed.
  Repository change: one branch repairs the runner defects in
  scripts/stage2.py and model-endpoints.yaml, with their tests.
  Architecture change: none; three rows that need one (B-8, B-9, B-13) stay
  open questions.
asked: 2026-10-25, conversation
answer: "Bitte korrigiere auch alle Fehler im Runner die der reviewer gefunden hat" (please also fix every runner error the reviewer found — stated in German, translated by the agent)
answered_by: maintainer
status: answered

In the context of a deep review that reproduced runner defects in how the
review loop chooses, calls and reads its members, facing the choice between
repairing them now and leaving them as findings, we decided to repair every
runner defect on one branch and to put the three rows that need a new
declaration or prompt to the maintainer, to achieve a loop that neither
leaks a key nor loses a paid round to an admission slip, accepting that some
existing tests change their expectations with it. — 2026-10-25

## [DETAIL] The scope cut

- **Fixed here:** DL-B-1 to DL-B-7, DL-B-10, DL-B-11, DL-B-12, DL-B-14 —
  each is a runner defect with a smallest fix that changes no rule.
- **Not here: DL-B-8** (the catalog's `baseUrl` decides where a call goes).
  The fix needs a declared address in `model-endpoints.yaml` and a rule what
  to do with a differing one: a design question, not a defect fix.
- **Not here: DL-B-9** (the repair brake reads an Origin cell no reviewer is
  told how to fill). The fix is either a prompt change (`prompts/` is
  `human-written`) or a new ownership rule for the cell.
- **Not here: DL-B-13** (a retention reading that names an end date admits
  for ever). The fix is a new schema field in the declaration.
- The three go to `findings.md` as open questions for the maintainer, each
  with a recommendation. Reason: each needs a decision this change may not
  take (house rule 8, ADR 0008).

## [DETAIL] DL-B-12 is edited, not proposed

`provenance.yaml` maps no prefix for `model-endpoints.yaml`, so it is not
reserved for `human-decided`; an agent commit added an exclusion there
before (`48ba7d6`). The edit adds machine-readable ids to an exclusion the
maintainer already decided (ADR 0007 decision 3) and admits nothing.
Reason: the decision exists, only its data was missing.

## [DETAIL] What a secrets-file value is

Every value of the secrets file of eight or more characters is scrubbed,
and `OPENCODE_GO_KEY` and `GLM_KEY` whatever their length. A shorter value
(`OTHER=1` in the test world) would replace ordinary characters across the
answer. Reason: the file holds keys; a flag value is no credential.
