---
title: "Plan — swarm-citation-feedback"
status: draft
implementation_status: none
date: 2026-11-14
last_reviewed: 2026-11-14
updated: 2026-11-14
supersedes: null
superseded_by: null
bead: coding-harness-t2wm
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, research-swarm, citations]
---

# Plan — swarm-citation-feedback

```text
For you:     Copied Markdown headings resolve, rejected citations explain their faults, and briefs guide citation and fetching.
Done when:   All seven criteria have passing regression evidence and make verify is green with both prompt edits included.
Appetite:    3 hours of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     Runner-issued ids, corrections of valid reports, seat replacement or changed time limits.
Pre-mortem:  suppose it failed: most likely because citation details were lost before the correction prompt was built.
Starts unless you say stop.
```

## Basis and ownership

Implement the seven criteria of `spec.md`; the small-repair choice and residual
spelling risk are settled in `decisions.md#Q-1`. Class remains `bounded`, so no
`design.md` or ADR draft is due. The attempt owns code and tests below;
only the orchestrator edits the held `prompts/` paths after acceptance.

## Build sequence and files

1. Attempt: add regression cases in `tests/test_stage2_research_refs.py` for
   bare/prefixed headings (one through six marks, spaces/tabs), equal extents,
   literal hash titles, ambiguity, case/formatting and nonstructural matches.
   In `scripts/stage2_research_refs.py`, change only Markdown heading lookup:
   preserve exact lookup first; if no title matches, remove one leading ATX
   run with following whitespace and compare within the existing scan. Never
   fall back after ambiguity, alter the recorded original reference, broaden
   Python/mapping lookup or open a live file.
2. Attempt: in `scripts/stage2_research_report.py`, attach plain structured
   citation diagnostics to `ResearchReportError` at the evidence-floor failure,
   using already computed resolved entries: local claim id, original citation
   and reason for each `supported: false` reference, in claim/citation order.
   Preserve the exception's existing message and type, strict schema, valid
   result shape and all-or-nothing excerpts. Empty evidence lists and earlier
   extraction/schema failures retain their generic error without invented
   references. Add diagnostic tests to `tests/test_stage2_research_report.py`.
3. Attempt: in `scripts/stage2_research_run.py`, carry those optional primitive
   diagnostics through invalidation into the existing rejected-attempt record;
   keep `error` as text. Append the diagnostics as fenced, delimiter-neutralised
   data in `correction_prompt`, alongside the existing answer/reason. Do not
   put them in launcher system instructions or perform another resolution.
   Keep missing diagnostics compatible with older generic-error records. Rebuild
   prompts deterministically from retained fields so exact prompt hashes and
   corrected-final adoption still agree. Use the same plumbing for a rejected
   correction's retained evidence without requesting a second correction.
4. Attempt: in `tests/test_stage2_swarm.py`, use canned reports to cover two
   failed references with distinct reasons, a good reference in an unsupported
   claim, generic format errors, and an online failure using only its own
   receipt context. Assert data/instruction separation, no peer markers, one
   same-seat correction, persisted diagnostics and reuse of the valid corrected
   result without another launch. Add a mixed valid/unsupported report case
   proving no correction; keep existing security/time and accounting tests.
5. Orchestrator, after the accepted attempt: in
   `prompts/research-swarm/report.md`, add an explicitly fictional Markdown
   heading and its bare-title evidence string beside the evidence rules;
   describe optional opening marks without changing the existing base JSON
   example. In `prompts/research-swarm/public.md`, instruct at most three
   `public_fetch` calls per topic attempt (failures count), then reporting from
   successful own receipts and recording unread material. Keep the evidence
   floor and public-only boundary explicit. The attempt never edits these held
   paths. Attempt-owned tests for the prompt criteria are completed against
   the orchestrator's edits; do not weaken them to accept the original wording.
6. Attempt: add the Markdown-example fixture in
   `tests/test_stage2_research_report.py`; in `tests/test_stage2_swarm.py`, test
   `online_topic_prompt` directly for topics 9–11, which both required and free
   seats use, to check the budget/report instruction without launching a run.
   Update `plans/changes/swarm-citation-feedback/plan.md` ledger markers when
   tests exist; update `plans/changes/swarm-citation-feedback/spec.md` headers
   to reflect implementation. Orchestrator: record final evidence in
   `plans/changes/swarm-citation-feedback/findings.md` and regenerate
   `plans/INDEX.md` after artifact header edits. No deletion is planned.

## Verification

```sh
.venv/bin/python3 -m pytest tests/test_stage2_research_refs.py tests/test_stage2_research_report.py -q
.venv/bin/python3 -m pytest tests/test_stage2_swarm.py -q -k 'citation or correction or unsupported_claims or online_brief'
.venv/bin/python3 scripts/check_interview_minimums.py --change swarm-citation-feedback
.venv/bin/python3 scripts/check_research_handoff.py --change swarm-citation-feedback
.venv/bin/python3 scripts/check_criterion_ledger.py
make verify
```

Measure the new regression cases red before repairs and green afterwards.
Run the prompt tests after the orchestrator supplies the held edits; code-only
acceptance is not the final verification of all seven criteria. Stop at the
three-hour appetite including repair rounds and report unfinished work.

## Criterion ledger

- 1: not yet written tests/test_stage2_research_refs.py::test_reference_markdown_accepts_opening_heading_marks — a copied heading fails or returns a different extent
- 2: not yet written tests/test_stage2_research_refs.py::test_reference_markdown_prefix_tolerance_keeps_exact_boundaries — prefix tolerance overrides exact titles, ambiguity or structural limits
- 2: tests/test_stage2_research_refs.py::test_reference_heading_keeps_inline_formatting_and_case — case or formatting differences become supported
- 2: tests/test_stage2_research_refs.py::test_reference_reads_only_frozen_bytes_and_refuses_escape — live files or escaping paths become evidence
- 3: not yet written tests/test_stage2_research_report.py::test_report_evidence_floor_retains_each_failed_citation_reason — failure diagnostics omit or misattribute a reference or include a good reference
- 3: not yet written tests/test_stage2_swarm.py::test_citation_failures_reach_same_seat_correction — the correction contains only the generic reason instead of each original citation and reason
- 4: not yet written tests/test_stage2_swarm.py::test_citation_feedback_is_own_data_and_survives_resume — diagnostics enter instruction authority, cross seats or disappear before deterministic prompt reconstruction and adoption
- 4: tests/test_stage2_swarm.py::test_topic_correction_keeps_security_and_time_boundaries — a correction bypasses leak, receipt or original time boundaries
- 5: not yet written tests/test_stage2_research_report.py::test_report_prompt_markdown_example_resolves — the documented heading/citation pair cannot resolve or is missing
- 6: not yet written tests/test_stage2_swarm.py::test_online_brief_names_fetch_budget — a public topic prompt omits the three-fetch budget or report/unread instructions
- 7: not yet written tests/test_stage2_swarm.py::test_partly_unsupported_citations_do_not_trigger_correction — a valid mixed report is retried or its unsupported claim/question link is lost
- 7: tests/test_stage2_research_report.py::test_report_bad_citation_invalidates_whole_claim_without_dropping_it — partial excerpts survive or the unsupported claim disappears
- 7: tests/test_stage2_research_report.py::test_report_one_shared_unicode_excerpt_cap_in_citation_order — the existing excerpt cap or order changes

## Limits and draft context

Do not touch judge, handoff, dispatcher, state-store API, public tool code,
model declarations, limits, ADRs, workflow doctrine or other change folders.
The two prompt files are the only held source edits and belong to the
orchestrator; no implementation attempt edits any held prefix.

Phase 1 used Stage 2, route `flash`, model `glm-5.3-flash` on 2026-11-14;
no Stage-1 fallback is recorded. At drafting baseline 3d7cc0e2 (2026-11-14),
`templates/plan.md` and `scripts/validate_change_artefacts.py` are absent;
this plan follows the supplied phase-3 form. Research contains no complete
research-swarm/v2 run; neighbours are not a swarm-derived obligation here.
The existing `findings.md` contains only the runner audit, no open phase-2a rows.
The latest handover read is `docs/journal/handover/2026-11-13-night-five-lanes.md`;
it predates this change. Live PR state could not be read (GitHub connection
failed); current parallel-session ownership was not read inside this runner's
worktree-only boundary. Tracker, index regeneration, full verification and
commit belong to the runner/orchestrator, not this drafting call.

## Draft validation — 2026-11-14

Interview-minimums, criterion-ledger and frontmatter-current passed on the
uncommitted draft over 3d7cc0e2; research-handoff reported the explicit
no-v2-evidence exemption. Required headers, card placement and empty time
section were checked. The general artifact validator is absent; registry
checking was not run because its tracker renderer can read outside this
worktree. Full `make verify`, index regeneration and the commit remain with
the runner. This is document validation, not implementation test evidence.

## Runner route — 2026-11-14

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

2026-11-14 17:16:06–17:20:34 UTC, 267 s — draft · attempt 1 · route codex · model gpt-6.1-sol · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-14 17:22:47–17:47:15 UTC, 1468 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-14 17:47:24–17:54:51 UTC, 446 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-14 17:54:58–17:55:38 UTC, 40 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
