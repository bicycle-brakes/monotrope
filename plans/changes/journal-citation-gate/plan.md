---
title: "Plan — journal-citation-gate"
status: draft
implementation_status: none
date: 2026-11-19
last_reviewed: 2026-11-19
updated: 2026-11-20
supersedes: null
superseded_by: null
bead: coding-harness-x9ed
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-19"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, provenance]
---

# Plan — journal-citation-gate

```text
For you:     The journal-date check accepts patterns and runner records while still catching undated citations.
Done when:   Focused tests cover both exemptions and real undated citations, and make verify passes.
Appetite:    2 hours for phase 4, including repairs; stop at the limit.
Not now:     A new gate, runner changes, non-Markdown scans, and journal immutability.
Pre-mortem:  suppose it failed: most likely because an exemption hides nearby hand-written citations.
Starts unless you say stop.
```

## Implementation

1. In `scripts/check_research_handoff.py`, expose character spans from opening marker through the end of the closing marker on each parsed run through `parse_text`, without a second parser; preserve callers, existing verdicts and messages, including line handling for LF, CRLF, CR and Unicode separators; if parsing a research file fails, the citation check scans that file without exemptions.
2. In `tests/test_provenance.py`, retain tracked Markdown scanning and date, empty-target and placeholder rules; apply the spec's elision, possessive, path-alphabet and `.md` emphasis normalisation before checking patterns and dates. Exempt whole reader-accepted envelopes only in active or archived change research files. Scan all other text, including malformed files and other paths.
3. In `tests/test_provenance.py` and `tests/test_research_handoff.py`, test the shared reader and citation check with real-shaped envelopes, prose inside and outside, multiple envelopes including a valid run followed by a malformed run, parse-level success even when whole-change validation fails, malformed and forged envelopes, quoted emphasis and typographic possessives, trailing wildcard patterns, marker-only targets, placeholders, Unicode and mixed line endings, and mutations. Keep the existing enforcer and its mutation proof.
4. In `tests/test_provenance.py`, exempt an active or archived change's `findings.md` as a whole and make the failure message name `<file>:<line>` with one fixed reason instead of the cited target (agent detail S-13).
5. Do not touch `decisions/gates.yaml`, `docs/governance/regelwerk.md`, runner code, journal records, or unrelated provenance checks; no held path needs an orchestrator bootstrap edit.

Verification:

```sh
make verify
```

## Criterion ledger

- 1: tests/test_provenance.py::test_patterns_are_not_journal_citations — a glob ending in `*` or containing `*.md` is reported.
- 2: tests/test_provenance.py::test_runner_envelopes_are_not_journal_citations — a path inside a parseable envelope or its audit prose is reported, including when later whole-change validation fails.
- 3: tests/test_provenance.py::test_undated_citations_outside_runner_envelopes_are_reported — an undated path or one with emphasis followed by a closing quote or typographic possessive passes through the tracked-file check.
- 4: tests/test_provenance.py::test_existing_exemptions_and_elisions — a dated target, marker-only directory, placeholder or elision is reported after normalisation.
- 5: tests/test_provenance.py::test_malformed_or_forged_envelopes_remain_scannable — a malformed envelope or one outside change research hides a citation, or a valid run remains exempt in a file with a malformed run.
- 5: tests/test_research_handoff.py::test_envelope_spans_share_reader_validation — spans differ from accepted marker boundaries, parsing verdicts or messages change, or mixed line endings and Unicode shift a span.
- 6: tests/test_provenance.py::test_change_findings_are_runner_records — an undated path in a change's `findings.md` is reported, or the same text in another file passes.
- 7: tests/test_provenance.py::test_failure_message_never_repeats_the_target — the message carries the cited target or quoting it creates a new hit.

## Runner route — 2026-11-19

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-11-20

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-11-19 17:13:02–17:14:16 UTC, 74 s — draft · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-19 17:32:49–17:34:36 UTC, 107 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-19 17:38:50–17:40:25 UTC, 95 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-19 17:44:44–17:46:57 UTC, 134 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-19 17:47:12–18:17:19 UTC, 1807 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-19 18:17:31–18:28:24 UTC, 653 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-19 18:28:35–18:29:17 UTC, 42 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-19 18:29:29–18:32:19 UTC, 170 s — implement · hand finish · route orchestrator · model claude-opus-5-5 · accepted · targeted tests 141 passed; full `make verify` green afterwards (6330 passed, 17 skipped; 784 s execution, 1356 s admission wait); root cause: review row S-6 quotes an emphasised undated example and each failed attempt's record quoted the message back; fix by agent detail S-13 (findings.md exempt, message without target) · measured by the orchestrator
2026-11-19 22:22:04–23:06:52 UTC, 2688 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-19 23:07:03–23:08:16 UTC, 74 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · rejected · measured by the runner
2026-11-19 23:08:27–23:09:10 UTC, 43 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
