---
title: "Plan — address-notice-once"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-zywb
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2-runner, output]
---

# Plan — address-notice-once

```text
For you:     Repeated address notices appear once per runner call; evidence stays available.
Done when:   Tests count notices across paths and concurrent work, preserve records, and make verify passes.
Appetite:    4 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Terms warnings, stream unification, grouped model summaries and cross-process deduplication.
Pre-mortem:  suppose it failed: most likely because suppressing console noise also hides evidence.
Starts unless you say stop.
```

## Files and steps

1. Change `scripts/stage2_go.py`: provide one process-local, thread-safe console notice boundary keyed by the complete assessment notice; atomically decide and print on the caller's existing stream, retaining the first occurrence's prefix and wording. A new process starts with an empty set; do not change assessment or admission.
2. Change `scripts/stage2.py`: route dispatch, discovery, reviewer and round-note console announcements through that boundary, including the later loop that reprints round notes; keep per-round evidence independent of the console set and retain a distinct notice once per record, including success and exception paths.
3. Change `scripts/stage2_availability.py`: route probe and preparation-report console notices through the same boundary, preserving each report's non-notice lines, first-occurrence stream and sanitisation; leave stored state and audit evidence intact. Preserve report construction for record consumers rather than filtering the underlying state.
4. Change `tests/test_stage2_go_access.py`: add deterministic stand-in tests for repeated discovery, probing, reporting and dispatch in one call, both notice kinds, different models and paths, a new process, concurrent emitters, per-record evidence, both audit paths, stream and unchanged admission. Update existing expectations that assumed repeated console prints without weakening evidence assertions.
5. Update this change's `spec.md`, `plan.md` and `findings.md` as work advances. The orchestrator regenerates `plans/INDEX.md` and owns all held paths, tracker actions, verification and commit; the implementation attempt edits no held path. No Stage-1 Explore fallback was recorded.

Do not touch `scripts/stage2_research_run.py` or `scripts/stage2_session.py` merely to suppress their durable audit lines; those lines are evidence. Do not change model policy, terms warnings, other change folders or the protected areas of the spec.

## Verification

```sh
.venv/bin/python -m pytest tests/test_stage2_go_access.py tests/test_stage2_free.py tests/test_stage2_availability.py tests/test_stage2_research_availability.py tests/test_stage2_research_catalog.py tests/test_stage2_swarm.py tests/test_stage2_session.py -q
python3 scripts/check_interview_minimums.py --change address-notice-once
python3 scripts/check_criterion_ledger.py
python3 scripts/check_research_handoff.py
python3 scripts/plans_registry.py --check
make verify
```

The runner regenerates the index before the registry check and runs full verification. `templates/plan.md` and `scripts/validate_change_artefacts.py` are absent at this draft's base; the named available checks do not claim that the absent validator ran.

## Criterion ledger

- 1: not yet written tests/test_stage2_go_access.py::test_address_notice_once_across_runner_paths — the same notice is absent or printed twice across both streams during one call.
- 2: not yet written tests/test_stage2_go_access.py::test_distinct_address_notices_each_print_once — a model, path pair, wire API or notice kind is lost or repeated.
- 3: not yet written tests/test_stage2_go_access.py::test_address_notice_is_printed_in_each_process — the second process inherits the first process's suppression.
- 4: not yet written tests/test_stage2_go_access.py::test_concurrent_address_notices_print_once — simultaneous emitters print more than one line or none.
- 5: not yet written tests/test_stage2_go_access.py::test_address_notice_records_survive_console_deduplication — a later round or report loses or repeats a distinct notice.
- 6: not yet written tests/test_stage2_go_access.py::test_address_notice_audits_survive_console_deduplication — a research-seat or session audit loses the notice.
- 7: not yet written tests/test_stage2_go_access.py::test_first_address_notice_preserves_text_and_stream — the first notice changes text or output stream.
- 8: not yet written tests/test_stage2_go_access.py::test_address_notice_deduplication_does_not_change_admission — suppression changes admission, refusal or destination.

## Time used

2026-11-21 16:55:05–16:57:45 UTC, 160 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
