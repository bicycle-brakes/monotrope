---
title: "Plan — failed-check-spans"
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
tags: [plan, stage2, leak-check]
---

# Plan — failed-check-spans

```text
For you:     Failed-check diagnostics no longer leak a secret suffix next to the routing key, and a blocking rule next to it still blocks.
Done when:   The F-4 and F-5 reproductions are tests, red before and green after, and make verify is green.
Appetite:    1 hour of phase 4, including repairs; stop at the limit.
Not now:     Other scrub callers, leak-check semantics, marker formats.
Pre-mortem:  suppose it failed: most likely because a format-line test expects the old scrubbed text or a refusal now escapes format_step.
Starts unless you say stop.
```

## Changes

- `tests/test_stage2.py`: add the F-4 reproduction (a formatted target whose
  path holds key and suffix, through `verify_attempt`), the F-5 reproduction
  (identical secret and non-secret pattern over key and suffix) and the
  credential-only non-secret case; red before the production edit.
- `scripts/stage2.py`: `format_step` and `_not_run` return their line through
  `protect_diagnostics`; `_protect_diagnostics` runs the non-secret rules on
  the original text, skipping matches wholly inside a credential span, with
  one span finder shared by both rule kinds; docstring updated.
- `plans/changes/failed-check-spans/plan.md`: measured time below.

## Verification

Run the three new tests before the production edit (red) and after it
(green), then `PYTHON=.venv/bin/python3 make verify`.

## Criterion ledger

- 1: tests/test_stage2.py::test_a_format_line_overlapping_the_credential_keeps_the_whole_secret_span — the format line or its later protection keeps the suffix.
- 2: tests/test_stage2.py::test_a_nonsecret_match_extending_beyond_the_credential_refuses — the credential scrub hides the blocking match.
- 3: tests/test_stage2.py::test_a_nonsecret_match_inside_the_credential_alone_does_not_refuse — the credential alone causes a refusal.
- 4: tests/test_stage2.py::test_secret_rule_overlapping_a_credential_protects_the_original_span — the existing regression of #215 turns red.

## Time used

2026-10-22 16:09–16:16, 7 min

Phase 1 to the production commit, by the orchestrated night session itself
(the stage-2 runner calls were refused by the session permission classifier);
start and end read from `date` (Europe/Berlin).
2026-10-22 20:47:19–20:57:29 UTC, 610 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-10-22 20:57:35–21:03:11 UTC, 336 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · accepted · measured by the runner
