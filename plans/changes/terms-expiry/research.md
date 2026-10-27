---
title: "Research — terms-expiry"
status: draft
implementation_status: none
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-27
supersedes: null
superseded_by: null
bead: coding-harness-abra
class: feature
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
- add a machine-readable `valid_until: YYYY-MM-DD` to each `modelle_terms`
  record;
- `terms_problem` skips a model whose `valid_until` has passed and names it;
- re-read the DeepSeek terms now and record the result (this file).

The change is a decision pull request: `model-endpoints.yaml` is
`human-decided`.

## Questions for the interview (phase 1a)

This is a feature. It needs at least three answers. If it amends ADR 0021
(decision 5, terms reading), it needs five. Not asked yet:

1. Does `valid_until` replace the prose date in `aufbewahrung`, or stand beside
   it?
2. Is `valid_until` required on every record, or only where the source names a
   validity date?
3. On the day itself (`valid_until` = today), is the model still admitted?
4. Does an expired record skip the model silently, or does the availability
   report name it on every run?
5. Should `deepseek-v4.1-flash` get `valid_until: 2026-10-31` in this change,
   from today's reading?
6. Does this amend ADR 0021, decision 5, or only the declaration format?

## What is not read

- Whether DeepSeek renews the agreement for November. The page gave no date
  beyond 2026-10-31.
- Whether other providers on the Go page carry validity dates. Only the
  DeepSeek rows were asked for.

## Draft preparation addendum — 2026-10-26

Repository inspection at `97980181` resolves implementation gaps without
changing the five maintainer answers in `decisions.md`:

- `terms_problem` is at lines 1279–1302 in `scripts/stage2.py` at this
  commit, rather than the earlier line number above. `ladder` filters with
  it, and `declaration_problem` calls it before paid Go dispatch, including
  the interactive session path. Extending that shared guard reaches saved
  selections as well as new ones; expiry can refuse a saved round without
  rebuilding its historical membership.
- `scripts/stage2_availability.py` prepares and renders receipts; its state
  already retains `terms_skipped`. `review_loop` writes round notes and
  releases them to findings. These are the existing boundaries for warning
  display and evidence; no background service is needed.
- Every existing Go terms record, including explicit wire-API skips, has
  `gelesen`. Other than DeepSeek's documented expiry, the migration can
  apply the maintainer's reading-plus-30-days rule to those dates without
  claiming a new source reading. Other provider pages remain not read;
  no additional provider end date is asserted by this draft.
- `templates/spec.md`, `templates/design.md` and `templates/adr.md` exist;
  `templates/plan.md` and `scripts/validate_change_artefacts.py` do not.
  The plan follows `prompts/03-plan.md`; existing interview, criterion-ledger
  and registry checks remain the available gates.
- The cited `docs/journal/handover/2026-10-25-cloud-runner-fixes.md` is not
  present in this worktree and was not read. The latest available handover,
  `docs/journal/handover/2026-10-23-night-run.md` with its addenda, was read;
  the change's own research and later interview carry its current intent.
  GitHub PR state could not be read because the API connection failed.

The source re-read above is retained as supplied evidence; this drafting
call fetched no external source and wrote no implementation or tracker data.

Draft validation on 2026-10-26: the change-specific interview check and
criterion-ledger check passed. YAML headers, the ADR claim, the runner's
original plan-card check and the empty phase-4 time section passed local
structural checks. The ADR-answer gate reports the missing maintainer answer
as expected; no answer was written. Full `make verify`, registry generation
and tracker-dependent checks belong to the orchestrating runner.

### Draft retry validation — 2026-10-26

The second draft call at the same baseline re-read the existing spec,
design, plan, ADR proposal and runner diagnostics. `findings.md` contains
attempt diagnostics, with no open phase-2a rows to incorporate. The
change-specific interview check and repository criterion-ledger check
both passed again. No acceptance criterion or maintainer answer changed.

The plan now carries the existing worktree-toolchain prerequisites:
`make venv`, `bash tools/pi/install.sh` and the pinned-version check.
The first attempt's supplied evidence reports 16 Pi contract setup errors
from the missing installation; it does not justify changing a criterion
or weakening those tests. This draft installed nothing, ran no full
`make verify`, and leaves its fresh result to the orchestrator. The absent
artifact validator and tracker-dependent registry remain unmeasured here.
Current external PR state and live-session registry were not read because
this call is restricted to the worktree and repository git directory.

### Third draft attempt — 2026-10-26

The GLM route (attempt 3, after the two failed Codex attempts) re-read the
draft artifacts against the tree at `97980181`: `terms_problem`
(`scripts/stage2.py` lines 1279–1302) and every caller — `ladder`,
`skipped_models`, `declaration_problem` (reached by `preflight`,
`checked_prompt` and `stage2_session.py` line 185), so the saved-round and
interactive paths share the guard; the availability receipt, whose digest
covers the whole receipt, so an added warning list changes no digest rule;
and the 18 `modelle_terms` records (reading dates 2026-10-07/17/22; +30
day deadlines 2026-11-06/16/21; both DeepSeek entries on 2026-10-31). The
ledger's named existing tests are defined
(`test_free_class_admission_is_bound_to_discovery_and_purpose`,
`test_each_call_runs_its_own_leak_check`); its not-yet-written files and
functions do not exist. The markdownlint gate is `report`, not `block`;
the only blocking failure of both earlier attempts stays the worktree's
missing pinned Pi install, an orchestrator prerequisite no artifact can
supply. Edits this attempt: the spec's goal line follows the template
scaffold, criterion 3 now carries the recorded-date naming its refutation
already demanded, and the four headers name this attempt's producer.
