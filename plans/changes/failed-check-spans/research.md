---
title: "Research — failed-check-spans"
status: draft
implementation_status: none
date: 2026-10-22
last_reviewed: 2026-10-22
updated: 2026-10-22
supersedes: null
superseded_by: null
bead: coding-harness-8hr
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, leak-check]
---

# failed-check-spans — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md),
written by the orchestrated night session itself at `origin/main` `d99eb92`
(2026-10-22): the scope is two findings already reproduced by a reviewer, so
no separate exploration call was made.

## What exists today

The merged change `failed-check-secrets` (pull request #215, merged at
`4239f8c`) redacts secret-rule matches in failed-check diagnostics. Its last
phase-6 re-check (Codex, 2026-10-22, `plans/changes/failed-check-secrets/findings.md`)
left two MAJOR rows open:

- **F-4** — `format_step` in `scripts/stage2.py` returns its one-line report
  through `scrub(...)`, which replaces the routing credential before any
  secret span is found. The line is later protected again by
  `protect_diagnostics` (the listing and the checkpoint record in
  `run_attempts`), but by then a secret-rule match that overlapped the
  credential is already cut: the reviewer's path
  `tests/ROUTEKEY-987654321:FIXKEY-123456.py` comes back as
  `tests/[credential]:FIXKEY-123456.py`, and the suffix survives.
  `_not_run` (the "not run" line of the same step) uses `scrub` the same way.
- **F-5** — `_protect_diagnostics` in `scripts/stage2.py` runs the
  non-secret rules on `scrub(original, key)`, the credential-replaced text,
  while the secret rules already run on the original. A non-secret match
  that starts inside the credential and ends outside it is destroyed by the
  scrub, is not seen, and the following secret replacement then hides it:
  the reviewer's identical secret and non-secret pattern
  `ROUTEKEY-[0-9]+:FIXKEY-[0-9]+` yields `[credential][secret:pair]` and no
  refusal.

## Where it lives

- `scripts/stage2.py`: `credential_spans`, `scrub`, `protect_diagnostics`,
  `_protect_diagnostics`, `format_step`, `_not_run`, `verify_attempt`
  (appends the format line to `formatted`), `run_attempts` (protects the
  listing and the `record` lines).
- `tests/test_stage2.py`: `test_secret_rule_overlapping_a_credential_protects_the_original_span`
  (the F-3 repair, the shape the new tests follow),
  `test_nonsecret_diagnostic_matches_still_refuse` (criterion 5 without a
  credential), `test_an_unreadable_target_is_named_by_its_repository_path`
  (calls `verify_attempt` with a `formatted` list).

## What is unclear

- Why the non-secret check used credential-scrubbed text: the docstring says
  "Non-secret rules check credential-safe text" and the code comment says
  "Non-secret checks retain credential precedence". The measured effect is
  that a non-secret match lying wholly inside the routing credential does not
  refuse; whether that is relied on is not stated in the spec of #215. Not
  found: a test that pins it.
- `format_step`'s callers handle `Refused` from `verify_attempt` (restore the
  findings, re-raise); `prepare_derived` already raises it from
  `protect_diagnostics` inside `verify_attempt`.

## Files a change would touch

`scripts/stage2.py`, `tests/test_stage2.py`, this change folder,
`plans/INDEX.md` (regenerated).
