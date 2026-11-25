---
title: "Plan — availability scrub import"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-vg9.2
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, availability]
---

# Plan — availability scrub import

```text
For you:     Availability errors use the active runner's redactor without loading a second runner.
Done when:   The redaction, runner substitution, import guard and existing intelligence checks pass, as does make verify.
Appetite:    2 hours for implementation and repair rounds; stop when spent.
Not now:     Moving the redactor or refactoring the runner.
Pre-mortem:  suppose it failed: most likely because an error path still uses a different runner.
Starts unless you say stop.
```

## Files

- `scripts/stage2_availability.py` — add keyword-only `runner` to `read_intelligence`, pass it from `prepare_research`, and replace the local import with `runner.scrub`, preserving replacement, truncation and returned fields.
- `tests/test_stage2_research_availability.py` — pass the imported runner at both direct calls; add a substituted-redactor error test and an AST guard for imports anywhere in the availability module; retain existing redaction and success checks.

## Verification command

```sh
make verify
```

## Criterion ledger

- 1: not yet written tests/test_stage2_research_availability.py::test_intelligence_error_uses_supplied_runner_scrub — a substituted redactor is bypassed or its result is missing from the status.
- 2: tests/test_stage2_research_availability.py::test_intelligence_errors_redact_credential_fragments — an error escapes or an injected credential fragment of eight or more characters survives in the reading.
- 2: not yet written tests/test_stage2_research_availability.py::test_intelligence_errors_redact_whole_credential — the whole credential injected into the exception survives in the reading.
- 3: not yet written tests/test_stage2_research_availability.py::test_availability_never_imports_stage2 — an `Import` or `ImportFrom` AST node imports `stage2`, including within a function.
- 4: tests/test_stage2_research_availability.py::test_the_report_weighs_intelligence_against_cost_and_names_the_source — matching scores or their report change.
- 4: tests/test_stage2_research_availability.py::test_unmatched_intelligence_has_per_model_reason_and_cost_only_caveat — an unmatched model loses its reason.

## Not touched

`scripts/stage2.py`, other availability functions except the caller's argument, and shared-secrets design remain outside scope. No held path needs an orchestrator bootstrap edit.

## Explore route

Stage 1 via `claude-code-plan`, model `claude-haiku-5-5`: GLM 5.3 Flash via Z.ai had reached its weekly limit until 2026-11-29, as recorded in `research.md` on 2026-11-25.

## Time used

2026-11-25 02:36:28–02:37:48 UTC, 80 s — draft · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 02:40:00–02:41:30 UTC, 90 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 02:45:16–02:46:48 UTC, 91 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
