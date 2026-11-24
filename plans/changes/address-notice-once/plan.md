---
title: "Plan — address-notice-once"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-24
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

1. Change `scripts/stage2_go.py`: provide one shared, thread-safe console notice boundary keyed by the complete assessment notice, scoped to an entry invocation; call it only at existing console print sites, atomically choose and print on the original stream and prefix, and print normally outside a scope. Share its state with concurrent workers and reset it on every exit, including exceptions.
2. Change `scripts/stage2.py`: open the scope at `main` for each invocation, including nested availability and research work; route dispatch, discovery, reviewer and round-note console announcements through it, including any later console reprint. Keep round evidence independent, deduplicating within each existing notice section on success and exception paths.
3. Change `scripts/stage2_availability.py`: buffer existing preparation console announcements until the report is known; print each report notice once in its existing report and suppress matching buffered announcements. Print notices absent from the report once on their original stream; on early failure flush only held console announcements using the first site's wording and stream. Do not print assessment-only notices on early failure. Preserve the report's other lines and sanitisation and keep probe and installation audits and stored state independent of console suppression.
4. Change `tests/test_stage2_go_access.py`: add the ledger tests using deterministic stand-ins and actual entry paths; cover both notice kinds and streams, two invocations in one process, direct calls outside an entry, concurrent workers, both preparation reports, early failure and silent assessment-only notices, both round sections, all audits, and unchanged admission. Update old console assertions only where needed and retain evidence assertions.
5. Update `plans/changes/address-notice-once/spec.md`, `plans/changes/address-notice-once/plan.md` and `plans/changes/address-notice-once/findings.md` as work advances. The orchestrator regenerates `plans/INDEX.md` if needed and owns held paths, tracker actions, verification and commit; the implementation attempt edits no held path. No Stage-1 Explore fallback was recorded.

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

- 1: not yet written tests/test_stage2_go_access.py::test_address_notice_once_across_runner_paths — the same notice is absent or printed twice across both streams during one entry, including an early preparation failure.
- 2: not yet written tests/test_stage2_go_access.py::test_distinct_address_notices_each_print_once — a model, path pair, wire API or notice kind is lost or repeated.
- 3: not yet written tests/test_stage2_go_access.py::test_address_notice_is_printed_in_each_entry — the second entry in the same process inherits the first entry's suppression.
- 4: not yet written tests/test_stage2_go_access.py::test_concurrent_address_notices_print_once — simultaneous emitters print more than one line or none.
- 5: not yet written tests/test_stage2_go_access.py::test_address_notice_records_survive_console_deduplication — either existing round section or a report loses or repeats a notice within that section, including a failed round.
- 6: not yet written tests/test_stage2_go_access.py::test_address_notice_audits_survive_console_deduplication — a research-seat or session audit loses the notice.
- 7: not yet written tests/test_stage2_go_access.py::test_first_address_notice_preserves_text_and_stream — the first notice outside a preparation report changes text or output stream.
- 8: not yet written tests/test_stage2_go_access.py::test_address_notice_deduplication_does_not_change_admission — suppression changes admission, refusal or destination.
- 9: not yet written tests/test_stage2_go_access.py::test_preparation_report_keeps_notices_without_prior_console_duplicates — either preparation report omits or repeats a notice, or also prints it earlier; notices absent from the report still appear once.
- 10: not yet written tests/test_stage2_go_access.py::test_probe_and_install_audits_keep_address_notices — suppression removes an existing probe or installation audit line.
- 11: not yet written tests/test_stage2_go_access.py::test_direct_calls_keep_notice_output — a direct call outside an entry inherits suppression and fails to print.
- 12: not yet written tests/test_stage2_go_access.py::test_assessment_only_notices_stay_silent — a refused session binding or early research-preparation failure prints an assessment-only notice.
- 13: not yet written tests/test_stage2_go_access.py::test_early_preparation_failure_flushes_original_stream — a held discovery notice is missing, duplicated, reworded or sent to stdout instead of stderr on early refusal.

## Draft provenance

2026-11-21 16:55:05–16:57:45 UTC, 160 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner

## Runner route — 2026-11-24

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

2026-11-21 16:55:05–16:57:45 UTC, 160 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 17:03:02–17:05:25 UTC, 143 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 17:20:49–17:22:33 UTC, 105 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-24 07:03:23–07:49:15 UTC, 2753 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-24 07:49:33–08:01:06 UTC, 693 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-24 08:01:23–08:02:52 UTC, 89 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
