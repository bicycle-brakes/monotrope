---
title: "Plan — go-reasoning-contract"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-1zqh
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, pi, reasoning, contract-tests]
---

# Plan — go-reasoning-contract

```text
For you:     The two native Go API contracts cover reasoning requests and replies offline.
Done when:   Both protocols pass the reasoning contracts and make verify is green.
Appetite:    4 hours of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     Live model calls, Google, Codex effort, or changes to provider policy.
Pre-mortem:  suppose it failed: most likely because the test never reaches the real Pi exchange.
Starts unless you say stop.
```

## Build sequence and files

The plan is not ready to execute: first resolve the measurement gap in
`spec.md` and incorporate findings S3 and S4 into the spec. Show the final
card only after that redraft.

1. Change `tests/test_pi_contract.py`: add separate reasoning-enabled synthetic
   rows for Messages and Responses without changing the existing plain-text or
   Google contracts. Use the pinned Pi and its actual request building and
   response parsing, the production Go overlay and reviewer launch, synthetic
   address policy and credentials, and the existing guarded loopback transport.
   Verify the activated row retains `reasoning: true`; repoint only the
   transport after the address check. Request `--thinking max` through the
   production reviewer and assert each API's native setting. For the synthetic
   Responses row, the saved attempt expected `high`; confirm the pinned Pi's
   actual mapping before asserting it, without deriving the expected value from
   the request under test.
2. Extend that file's stub with protocol-valid streamed reasoning and text
   events for each API, distinct markers, and assertions on the actual answer
   returned to the runner. Require setup, exchange and teardown to succeed;
   missing Pi or a blocked loopback port is a failure, never a skip. Keep the
   network guard, route and credential assertions, and existing test names.
   Check both protocols and prove the assertions reject an omitted setting,
   lost text and leaked reasoning.
3. The saved state at commit `f9a1cd1a` shows the first and third repair checks
   failed in pytest setup for the Messages case; the second changed no files
   and reported no fixed line. Its recorded diagnostics do not give the
   underlying setup exception, so its root cause is unknown, not proven to be
   the test body. First check `installed_pi` and the isolated project's setup
   with the plain-text case, capture the full traceback if setup fails, and
   correct the environment before changing assertions. The attempted patch
   changed the shared row for all three APIs; keep the new cases separate.
4. Maintain this change's `spec.md` and `plan.md` as needed; the runner owns
   `findings.md` and time entries. No held path is edited, no file is deleted,
   and no design or ADR is due for a bounded change.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_pi_contract.py
python3 scripts/check_interview_minimums.py --root . --change go-reasoning-contract
python3 scripts/check_criterion_ledger.py --root .
make verify
```

The runner performs the final full check and commit. Explore used the Stage-1
fallback, route `stage-1`, model `claude-haiku-5-5`, because GLM 5.3 Flash
returned `claude-code:unrecognized_model` on 2026-11-21. Do not touch the
Google case, Codex settings, provider declarations or production policy.

## Criterion ledger

- 1: not yet written tests/test_pi_contract.py::test_go_reasoning_request_contract — Messages omits or disables the native thinking budget
- 2: not yet written tests/test_pi_contract.py::test_go_reasoning_request_contract — Responses omits or changes the expected effort
- 3: not yet written tests/test_pi_contract.py::test_go_reasoning_response_contract — Messages loses text
- 4: not yet written tests/test_pi_contract.py::test_go_reasoning_response_contract — Messages exposes reasoning
- 5: not yet written tests/test_pi_contract.py::test_go_reasoning_response_contract — Responses loses text
- 6: not yet written tests/test_pi_contract.py::test_go_reasoning_response_contract — Responses exposes reasoning

## Time used

2026-11-21 18:02:47–18:05:22 UTC, 155 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 22:26:20–22:29:15 UTC, 175 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
