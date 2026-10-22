---
title: "Decisions — failed-check-secrets"
status: draft
implementation_status: none
date: 2026-10-16
last_reviewed: 2026-10-16
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-8hr
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# failed-check-secrets — Decisions

## SKIP · interview

status: skipped
reason: A bounded fix whose requirement the bead already states (coding-harness-8hr: scrub secret-rule matches from failed-check diagnostics before they are written or sent, and test that a failed attempt whose traceback holds a fixture key can still be retried). The maintainer pre-approved the merge of this bead's pull request on 2026-10-16 under two conditions (no open BLOCKER after the phase-6 Opus review, green CI). What stays open is mechanics, decided below as details with their reasons.

## Details the orchestrating session decides

These are `[DETAIL]` items (the agent decides and writes its reason down);
none of them changes a decision of record.

1. **Redact secret rules only.** The redaction covers matches of rules whose
   name starts with `secret:` (`SECRET_PREFIX` in `scripts/leakcheck.py`).
   Reason: the bead names secret-rule matches, and the `tests/` exemption
   applies to the same class. A match of a non-secret rule in a diagnostic
   keeps blocking the retry, because it may be customer data and must not be
   silently replaced.
2. **Replace with the rule name, not the value.** A matched span becomes
   `[secret:<rule name>]`, with its place kept. Reason: the check's own report
   already keeps rule name and place and never the match; the attempt's
   diagnostics then stay useful for repair. The existing `[credential]` marker
   stays for the routing credential.
3. **One seam for both channels.** The redaction is applied where the
   diagnostics strings are built (`verify_evidence` and `attempt_block`), so the
   quoted block in `findings.md` and the retry prompt receive the same redacted
   text. Reason: both come from the same problem strings, so one seam covers
   both.
4. **A failed denylist read stays a refusal.** If the denylist cannot be read
   at redaction time, the runner refuses as the check does ("Unchecked is not
   clean"). Reason: redacting without the rule set would pass unchecked text.
5. **The test follows the existing pattern.** A test plants a fixture key in a
   failing `make verify` traceback, using the existing `LEAK`/`DENYLIST` pair
   and the `make` stand-in, and asserts that the retry prompt contains no key
   and the second attempt passes the leak check. Reason: the research names this
   test shape as already established.
