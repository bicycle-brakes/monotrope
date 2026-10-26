---
title: "ADR 0022 — Paid-model terms readings expire on a declared UTC date"
category: adr
status: accepted
created: 2026-10-26
last_reviewed: 2026-10-26
updated: 2026-10-26
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: Claude Code, version: "GLM 5.3, 2026-10-26"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, model-terms, stage-2, opencode-go]
---

# ADR 0022 — Paid-model terms readings expire on a declared UTC date

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, the pull request's state is the decision's state: open
  is proposed, closed is rejected. Amends ADR 0021 decision 5 and its
  availability amendment's paid-terms prerequisite; supersedes no ADR.
  Amends no D- or O-number.
* Review: the maintainer chose mandatory dates, renewal by decision pull
  request, seven-day warnings and a 30-day default in the conversations of
  2026-10-25/26 (`plans/changes/terms-expiry/decisions.md`). Acceptance is
  the merge commit, recorded nowhere else; the header's review remains
  pending · Decider: maintainer · prepared by GLM 5.3 through stage 2.
* Date: 2026-10-26 · takes effect on merge.

## Context

Paid OpenCode Go models need sourced retention/training readings under ADR
0021. At `97980181` (2026-10-26), `terms_problem` checks the reading's date,
source, retention text and training permission but no expiry. DeepSeek V4
Pro's end date occurs only in prose; DeepSeek V4.1 Flash lacks even that
qualification. The recorded source re-read of 2026-10-25 says both models'
zero-retention agreement is valid through 2026-10-31
(`plans/changes/terms-expiry/research.md`). No November renewal is claimed.

## Decision Drivers

* A paid model must not receive calls on an expired terms reading.
* The maintainer needs notice before reviewers become unavailable.
* Every reading needs an end date, even when the provider states none.
* Source readings and endpoint edits remain subject to maintainer approval.
* Existing free-class confinement, leak checks and run history remain binding.

## Considered Options

* **Declared expiry with advance warnings:** enforce dates in shared paid
  admission, retain evidence and renew readings by decision pull request.
  This prevents indefinite validity but owes periodic source re-reading.
* **Retention prose and manual reminders:** leave the machine admission rule
  unchanged and rely on the operator to spot dates. This is less work for
  the runner but can send code after an agreement expires.
* **Automatic rolling expiry:** extend dates during runs. This reduces
  operator work but grants renewed admission without renewed source evidence
  or the maintainer's merge.

## Decision

Chosen option: "Declared expiry with advance warnings", because it enforces
the recorded maintainer answers without granting approval by omission.

1. Every paid `modelle_terms` reading requires a quoted ISO calendar date
   `gilt_bis`. Missing, unusable or passed dates exclude and name the model;
   expiry diagnostics include the recorded date when one has passed.
2. A reading is valid through its named UTC day and expires on the next
   UTC day. The date stands beside retention prose; prose is not parsed for
   admission. Current per-call checks apply even to saved run membership.
3. Preparation and terms-evaluating review-loop invocations warn from seven
   days before expiry through the expiry day, naming model and date.
   Warnings remain in successful preparation receipts and written round
   evidence, including release to findings. Warnings never relax admission.
4. The agent re-reads the source, records source and reading date, and
   proposes each new or renewed entry in a decision pull request; the
   maintainer merges. Use the source's explicit end date, otherwise the
   reading date plus 30 calendar days. The runner does not renew dates.
5. Migrate both DeepSeek readings from the documented 2026-10-25 re-read to
   expiry 2026-10-31. Other existing records keep their reading dates and
   gain reading date plus 30 days, including explicitly skipped records.
6. Existing skip, source, retention, training and declaration checks still
   apply. The discovered free diff-only class keeps ADR 0021's confined
   exception. Saved membership/history is not rewritten to bypass expiry;
   refusal may stop a saved round without consuming it or claiming success.

## Consequences

* Readings require periodic renewal; models may drop from new selections or
  block a saved paid round until their renewal is merged.
* The warning repeats on terms-evaluating runs; there is no background
  monitoring or automatic source fetch.
* A future date is not an independent grant of admission. Wire-API skips,
  unread/training-enabled terms, declarations and leak refusals still bind.
* This changes no other endpoint's admission policy and grants no new model
  or provider permission.

## Validation

* The change's criterion ledger maps malformed/missing dates, UTC boundaries,
  warning boundaries, saved receipts, retries, replacements and interactive
  dispatch to deterministic tests with synthetic model processes.
* Migration tests check every declared record, both DeepSeek entries and
  the 30-day rule without relying on the wall clock or live provider access.
* `make verify` and the phase-6 review confirm code, workflow text and this
  proposal agree; merge makes the amendment effective. No ADR answer is
  recorded by the drafting agent.
