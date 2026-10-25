---
title: "Research — terms-expiry"
status: draft
implementation_status: none
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-abra
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, model-terms, stage-2, decision]
---

# terms-expiry — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md). The
orchestrating session wrote it at `origin/main` on 2026-10-25, during the
night run. Its source is finding DL-B-13 of the deep review, part B, from the
cloud session of 2026-10-25 (`docs/journal/handover/2026-10-25-cloud-runner-fixes.md`,
PR #245).

## The finding

`terms_problem` in `scripts/stage2.py` (line 1243 at `origin/main`, 2026-10-25)
admits a paid model when all four of these hold:
- `gelesen` is an ISO date;
- `quelle` is set;
- `aufbewahrung` is a non-empty string;
- `training` is `Not used`.

It reads nothing inside `aufbewahrung`. The record for `deepseek-v4-pro`
in `model-endpoints.yaml` (line 259) carries its expiry only as prose:
`"0 days (DeepSeek zero-data-retention agreement, valid through
2026-10-31)"`. From 2026-11-01 on, the runner would go on admitting that
model, although the reading it rests on has expired.

## Source re-read, 2026-10-25 about 21:45 UTC

The source is the privacy table of the Go page, https://opencode.ai/docs/go.
It was read on 2026-10-25 through a fetch tool. The quotes below are what the
tool returned for the DeepSeek rows; they were not compared with a browser
rendering.

- `| DeepSeek V4.1 Flash | Not used | 0 days* |`
- `| DeepSeek V4 Pro | Not used | 0 days* |`
- The footnote: "ZDR agreement is renewed monthly. The current agreement is
  valid through October 31, 2026."
- The page shows no "last updated" date.

## New: deepseek-v4.1-flash has the same condition

The asterisk is on **both** DeepSeek rows. But the record for
`deepseek-v4.1-flash` (lines 184 to 191, `gelesen: "2026-10-07"`) says only
`aufbewahrung: "0 days"`. It does not mention the monthly agreement. That
model sits in the Flash swarm (`flash_swarm`, line 356) and is the cheapest
rung of the `opencode-go` set. So the expiry concerns two models, not one.
Whether the asterisk was already on the Flash row on 2026-10-07 was not read.

## What the maintainer decided (2026-10-25, conversation)

Night-run plan, answer 2 (`docs/research/2026-10-25-night-run-plan.md`):
- add a machine-readable `gilt_bis: YYYY-MM-DD` to each `modelle_terms`
  record;
- `terms_problem` skips a model whose `gilt_bis` has passed and names it;
- re-read the DeepSeek terms now and record the result (this file).

The change is a decision pull request: `model-endpoints.yaml` is
`human-decided`.

## Questions for the interview (phase 1a)

This is a feature. It needs at least three answers. If it amends ADR 0021
(decision 5, terms reading), it needs five. Not asked yet:

1. Does `gilt_bis` replace the prose date in `aufbewahrung`, or stand beside
   it?
2. Is `gilt_bis` required on every record, or only where the source names a
   validity date?
3. On the day itself (`gilt_bis` = today), is the model still admitted?
4. Does an expired record skip the model silently, or does the availability
   report name it on every run?
5. Should `deepseek-v4.1-flash` get `gilt_bis: 2026-10-31` in this change,
   from today's reading?
6. Does this amend ADR 0021, decision 5, or only the declaration format?

## What is not read

- Whether DeepSeek renews the agreement for November. The page gave no date
  beyond 2026-10-31.
- Whether other providers on the Go page carry validity dates. Only the
  DeepSeek rows were asked for.
