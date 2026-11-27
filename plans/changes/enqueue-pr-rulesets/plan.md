---
title: "Plan — enqueue-pr-rulesets"
status: draft
implementation_status: none
date: 2026-11-27
last_reviewed: 2026-11-27
updated: 2026-11-27
supersedes: null
superseded_by: null
bead: coding-harness-3wtk
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-27"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, merge-queue]
---

# Plan — enqueue-pr-rulesets

```text
For you:     Eligible pull requests can pass the ruleset and released-loop checks without these two false refusals.
Done when:   Regression tests prove both repairs and the remaining refusals, and make verify is green.
Appetite:    2 hours for implementation and repairs; stop at the limit.
Not now:     Changing required checks, the runner's state format, or other admission safeguards.
Pre-mortem:  suppose it failed: most likely because an unreadable response is mistaken for absent protection.
Starts unless you say stop.
```

## Steps and files

1. In `scripts/enqueue_pr.py`, accept the specific 404 at the classic required-checks endpoint as absent classic protection while retaining the ruleset union and all other refusals; in `released_problems`, exempt only the runner's anchored `Loop state: {…}` form before malformed-table detection, without changing the phase-6 parser or row checks.
2. In `tests/test_enqueue_pr.py`, add fake GitHub and released-block regression cases named in the ledger, including a pipe in the state, unrelated errors, missing and failing ruleset checks, and malformed lookalikes; do not call a real queue.
3. The orchestrator regenerates `plans/INDEX.md` if the registry requires it after the new artifact headers; no held path is assigned to the implementation attempt.

Phase 1 fallback: Stage 1, `claude-haiku-5-5` through `claude-code-plan`, because GLM through Z.ai was at its weekly limit until 2026-11-29 (research dated 2026-11-27).

## Verification

```sh
python3 -m pytest -q tests/test_enqueue_pr.py
python3 scripts/jobs.py start -- env -u HARNESS_JOB_RECORD make verify
```

Inspect the detached job's exit with `python3 scripts/jobs.py list`; a successful start is not a green verification.

## Criterion ledger

- 1: not yet written tests/test_enqueue_pr.py::test_ruleset_only_branch_without_classic_protection — the 404 refuses or a ruleset check disappears.
- 2: not yet written tests/test_enqueue_pr.py::test_ruleset_only_branch_requires_head_checks — a missing or failing required check passes.
- 3: not yet written tests/test_enqueue_pr.py::test_classic_protection_other_errors_refuse — an unrelated 404 or 403 passes.
- 4: not yet written tests/test_enqueue_pr.py::test_released_runner_state_line_is_accepted — a runner state line containing a pipe is refused.
- 5: not yet written tests/test_enqueue_pr.py::test_released_state_lookalikes_refuse — an unrelated malformed pipe-bearing line passes.

## Do not touch

Do not edit `scripts/stage2.py`, repository settings, tracker data, other changes, or held paths during the implementation attempt; do not change the required-check set or enqueue a real pull request in tests.

## Time used

2026-11-27 21:12:51–21:14:48 UTC, 118 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
