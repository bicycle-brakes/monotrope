---
title: "Decisions — phase6-english"
category: decisions
status: draft
implementation_status: none
date: 2026-11-22
created: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-24
supersedes: null
superseded_by: null
bead: coding-harness-tscc
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, phase-6, language]
---

# phase6-english — Decisions

Class: bounded (bead coding-harness-tscc).

## The bead (read from the tracker by the orchestrator, 2026-11-22)

> House rule 1 makes the repository English, but on 2026-11-19/20 the Codex phase-6 reviewer wrote two verdicts in German (slip-counter findings.md: P6-1 of 2026-11-19 and R1 of 2026-11-20); they were committed unchanged under the rule for reviewer output. Maintainer decision 2026-11-20: (1) the phase-6 review prompt states 'Answer in English'; (2) the runner detects a verdict that is not English and asks once more, as it does for a malformed answer; a second non-English answer is kept as it came, with a notice. The two existing German verdicts stay as recorded.

Notes add a third German verdict (loop-record-other-worktree, F6-1/F6-2, 2026-11-20) and on 2026-11-21 the mandatory-spec-review phase-6 rows F-4..F-6 were German too.

## SKIP · interview

status: skipped
reason: The maintainer decided the remedy on 2026-11-20 (quoted in the bead): the prompt line, one re-ask, keep the second answer with a notice, leave the recorded verdicts. The maintainer asked for no question windows until the block on 2026-11-23 10:00. The details are [DETAIL] items below; the maintainer's veto on the Plan Card stays.

## [DETAIL] items decided by the orchestrator

- **How "not English" is detected:** a dependency-free heuristic over the finding cells of the verdict — the share of common German function words and of the letters ä, ö, ü, ß among all words; above a fixed threshold the answer is not English. Code spans, paths and identifiers are removed before counting. Reason: no new dependency, and the three recorded verdicts are clearly separable; the test pins them (German) and the English verdicts of the same day (English).
- **Where the re-ask lives:** the same retry path the runner uses for a malformed phase-6 answer, so it counts against the same one-retry budget and leaves the same record line. Reason: the maintainer's "as it does for a malformed answer".
- **The notice:** a second non-English answer is committed as it came, with one line in the verdict block saying it was kept although not English. Reason: the maintainer's decision.
- **The prompt line** "Answer in English." is added to the phase-6 review prompt; `prompts/` is runner-held, so it is an orchestrator hand edit after the accepted attempt.
- **Scope: phase 6 only.** Other reviewers (spec-review, loop) are not changed. Reason: the bead names phase 6.
