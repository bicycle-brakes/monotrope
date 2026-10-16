---
title: "Research — failed-check-secrets"
status: draft
implementation_status: none
date: 2026-10-16
last_reviewed: 2026-10-16
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-8hr
class: bounded
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, leak-check]
---

# Failed-check diagnostics that carry test secrets — Research

Phase 1 for bead coding-harness-8hr, seeded by the orchestrating session on
2026-10-16 against `origin/main` at `6029bbf`.

## The question

On 2026-10-15 the draft of the pi-pin change (bead coding-harness-agx) failed
its first attempt's `make verify`: the disk was full, and a test raised
`OSError` (ENOSPC). The runner wrote the pytest traceback into that change's
`findings.md`, and the traceback held a test fixture's fake key value. The
leak check matched it (rules `secret:openai-style-key` and
`secret:generic-api-key-assignment`). The retry prompt carries the failure
text, so the leak check blocked attempt 2 and the draft stopped. Needed (bead
text): scrub secret-rule matches from diagnostics before they are written or
sent, and test that a failed attempt whose traceback holds a fixture key can
still be retried.

## Known so far (read, not run)

- The leak check exempts `tests/` from its secret rules ("12 secret rules not
  applied under tests/" in every stage-2 INFO line), so the fixture key is
  legal where it lives and becomes a finding only once copied elsewhere.
- A leak-check BLOCK stops without fallback (AGENTS.md, stage 2); the fix must
  not weaken that rule. It must keep the secret out of the text instead.

## To explore

1. Where the runner turns a failed post-run check (`make verify`, red-first,
   other checks) into text: which function, which files it writes
   (`findings.md`, the loop record, the plan's time section) and which prompts
   it reaches on a retry.
2. Where the leak check's secret rules live and whether the runner can reuse
   them to redact a string (the same rule set, not a second copy).
3. Every path where diagnostics leave the runner: written files, retry
   prompts, audit lines, handover notes. Which of them the leak check reads.
4. What redaction should look like so the diagnostics stay useful (rule name
   and position kept, value replaced), and whether non-test secrets in a
   traceback must still block rather than be redacted.
5. Which tests cover the failure-text path today, so a test with a fixture key
   in a failing traceback can follow them.
