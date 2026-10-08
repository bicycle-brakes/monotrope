---
title: "Plan — runner-derived-files"
status: accepted
implementation_status: done
date: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-08
supersedes: null
superseded_by: null
bead: coding-harness-mfv
owner: Data Architect
provenance: ai-generated
produced_by: {kind: llm-session, name: codex, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [stage-2, runner, derived-files]
---

# Plan — runner-derived-files

```text
For you:     Correct file-only implementations no longer fail on stale derived metadata.
Done when:   Regression tests prove preparation and refusal behavior, and make verify is green.
Appetite:    2 hours; a stop, not an estimate.
Not now:     Review-loop integration, model-policy changes, unrelated clean documents.
Pre-mortem:  suppose it failed: most likely because preparation rewrites unrelated documents.
Starts unless you say stop.
```

1. scripts/stage2.py: prepare changed held header stamps and regenerate the
   index before verification; return scrubbed bounded preparation errors.
2. tests/test_stage2.py: run real render/stamp mechanisms with model stand-ins;
   cover first-attempt success, write scope, order/retries, failure and red tests.
3. plans/changes/runner-derived-files/{research,decisions,spec,plan,findings}.md:
   phase evidence; plans/INDEX.md: deterministic registry output.
4. docs/journal/handover/2026-10-08-runner-derived-files.md: resumable evidence.

Verification: `.venv/bin/python3 -m pytest -q tests/test_stage2.py`;
`GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false make verify`.
Criterion tests (tests/test_stage2.py): first-attempt success (1);
`test_preparation_stamps_only_changed_held_documents` and the two internal
link-target cases (2);
`test_each_retry_prepares_before_verify_and_keeps_real_failure_diagnostics` (3, 5);
renderer-failure, invalid-UTF8 and Git-failure diagnostic tests (4);
credential-free renderer environment test (3);
`test_preparation_collects_all_document_refusals_in_one_bounded_diagnostic` (4);
`test_broken_renderer_uses_existing_repair_limits_and_checkpoints_only_after_green`
holds the maintainer-confirmed continuation and the three-attempt limit (4).
Criterion faults: omit index render (1), stamp every document (2), move render
after verify or skip on retry (3), ignore renderer exit (4), ignore verify exit (5).
Codex implements directly per the maintainer's budget override and because
this change repairs the implementation route itself. No gate is relaxed.

## Time used

2026-10-08 10:31:06–10:48:08 UTC, 1022 seconds, Codex implementation and verification session; waits counted.
2026-10-08 10:48:08–10:58:12 UTC, 604 seconds, continuation from the previous measured checkpoint; review repairs and waits counted.
2026-10-08 12:17:11–12:34:05 UTC, 1015 seconds, resumed after the maintainer answer; retry and alias regression work plus verification waits counted. The human-answer break is excluded.
2026-10-08 12:41:33–12:48:20 UTC, 408 seconds, round-2 repairs and complete verification; waits counted.

2026-10-08 12:57:55–13:04:43 UTC, 408 seconds, final-review blocker repairs and complete verification; waits counted.
