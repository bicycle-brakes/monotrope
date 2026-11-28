---
title: "Plan — stamp-day-source"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-5v6t
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, frontmatter]
---

# Plan — stamp-day-source

```text
For you:     Runner checkpoints keep document dates current across midnight.
Done when:   The midnight and +0100 commit tests pass, and make verify is green.
Appetite:    3 hours for phase 4, repairs included — a stop, not an estimate.
Not now:     Changing historical date rules or manual Git commits.
Pre-mortem:  suppose it failed: most likely because the commit and stamp still read different instants.
Starts unless you say stop.
```

## Scope and sequence

The change is bounded, so no design or ADR is due. Explore used Stage 1, endpoint `claude-code-plan`, model `claude-haiku-5-5`, because GLM through Z.ai was at its weekly limit until 2026-11-29 (`research.md`, 2026-11-28).

1. In `scripts/stage2.py`, bind the checkpoint's runner-maintained document stamps and Git committer timestamp to one captured, offset-aware instant at the checkpoint boundary. Refresh eligible changed documents after the last runner writes and before staging; pass the same instant to Git as its committer date. A verification crossing midnight must not create a stale checkpoint. Preserve the existing single clock boundary, held-path restoration, scope checks, and failure handling; refuse the checkpoint if the date or stamp cannot be established. Do not use a separate fresh clock read for the commit.
2. In `tests/test_stage2.py`, exercise a real temporary Git checkpoint across midnight, including 00:30 +0100 (23:30 UTC), and check its committed header against its actual `%cs` and the frontmatter check. Exercise a stamp failure and a held-path case. The earlier preparation and later checkpoint must use independently controlled instants so the crossing is real in the test.
3. In `tests/test_frontmatter_current.py`, retain the existing recorded-offset and merge tests; add only coverage needed to assert the checkpoint integration using the real check, without changing the historical date rule.
4. Update `plans/changes/stamp-day-source/plan.md` for completed ledger entries and `## Time used`, and `plans/changes/stamp-day-source/spec.md` for implementation status. The runner owns the generated `plans/INDEX.md`; do not edit it by hand. No held paths require an implementation edit.

The refresh changes only the `updated:` line on eligible runner-maintained documents and must not admit a held path to the checkpoint. If a refresh after verification changes bytes, rerun the relevant frontmatter check on the final bytes before committing; do not silently commit when that check fails. Do not touch `scripts/check_frontmatter_current.py`, historical commits, unrelated clocks or other change folders.

Scope note (orchestrator, 2026-11-28): spec [DETAIL] S-4 is read under S-12 — the refusal for a document without frontmatter applies only to runner-maintained documents (held, `frontmatter: required`, outside every `human-decided` prefix). Generated or frontmatter-free held files such as `plans/INDEX.md` are not stamped and never refuse a checkpoint; implement attempt 1 was rejected because it refused every checkpoint on `plans/INDEX.md`.

## Verification

```sh
.venv/bin/python3 -m pytest tests/test_frontmatter_current.py tests/test_stage2.py -q
python3 scripts/check_interview_minimums.py --change stamp-day-source
python3 scripts/check_criterion_ledger.py
python3 scripts/plans_registry.py --check
make verify
```

The runner starts the full `make verify` through `python3 scripts/jobs.py start -- make verify` and owns the checkpoint.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_checkpoint_stamp_matches_recorded_commit_day — the committed stamp precedes the checkpoint's recorded day
- 2: not yet written tests/test_stage2.py::test_checkpoint_stamp_survives_midnight — a pre-midnight stamp remains stale after the post-midnight checkpoint
- 3: not yet written tests/test_stage2.py::test_checkpoint_stamp_uses_commit_offset_at_half_past_midnight — 00:30 +0100 is stamped with the previous UTC day
- 4: tests/test_frontmatter_current.py::test_the_committers_own_offset_decides_the_day — the checker uses UTC instead of the recorded offset
- 4: tests/test_frontmatter_current.py::test_a_merge_commit_never_counts — a merge replaces the last non-merge reference
- 5: not yet written tests/test_stage2.py::test_checkpoint_stamp_failure_prevents_commit — a failed stamp still produces a checkpoint
- 6: not yet written tests/test_stage2.py::test_checkpoint_stamp_preserves_content_and_held_paths — refresh changes other content or commits a protected path

## Runner route — 2026-11-28

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM through Z.ai at its weekly limit until 2026-11-29.

## Time used

2026-11-28 00:14:51–00:16:51 UTC, 120 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-28 03:15:14–03:40:47 UTC, 1534 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
