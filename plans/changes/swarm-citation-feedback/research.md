---
title: "Research — swarm-citation-feedback"
status: draft
implementation_status: none
date: 2026-11-14
last_reviewed: 2026-11-14
updated: 2026-11-14
supersedes: null
superseded_by: null
bead: coding-harness-t2wm
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-14", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# swarm citation feedback — Research

Stage-2 call, 2026-11-14: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1064 files, 4198 commits, 12 rules.

## Runner exploration — 2026-11-14

Exploration complete. Here is the research, written as prose ready to append to `plans/changes/swarm-citation-feedback/research.md`.

---

## What exists today

**The resolver.** `scripts/stage2_research_refs.py` resolves citations exclusively against frozen source bytes. `resolve_research_reference(sources, path, reference)` returns a typed extent `{path, reference, supported, excerpt, start_line, end_line}` or an explicit `{supported: False, reason}` with per-case reasons: "invalid reference", "path is absent from the frozen packet", "heading is absent or ambiguous" (`_markdown_extent`, including `criterion <n>`), "definition is absent or ambiguous" (`_python_extent`, AST-based), "mapping key is absent or not citable" (YAML/JSON dotted keys), "whole-word reference is absent" (all other suffixes). The module docstring states no function here opens a repository file. `research_claim_evidence(sources, citations)` in the same file implements claim-level assembly — "An unsupported citation invalidates the entire claim before excerpts are capped" — with the shared 4000-character budget. No production caller was found for `research_claim_evidence`; only `tests/test_stage2_research_refs.py` exercises it, and the `ci_gates.py` contract entry for `stage2_research_refs.py` describes "legacy dispatcher integration remains pending".

**Claim evidence during report validation.** The pipeline does not call `research_claim_evidence`; `scripts/stage2_research_report.py` has its own assembly. `_reference(citation, topic, sources, history, receipts)` routes by topic: topics ≥ 9 resolve a citation only through `_page_reference` (a public HTTPS URL matching a retained 200-status `public_fetch` receipt's request or final URL; otherwise reason "no runner evidence"); topics 1–8 with a `path::reference` string go to `resolve_research_reference`; topic 6 additionally accepts a full commit hash present in the runner-supplied history packet; everything else is "no runner evidence". `_evidence(...)` is all-or-nothing per claim: one unsupported citation yields `evidence_status: "unsupported"` and strips every excerpt, while `path`/`reference`/`reason` are retained; supported claims get excerpts capped to one shared 4000-Unicode-character budget in citation order with `truncated` marks. `validate_research_report(...)` enforces the evidence floor: it raises `ResearchReportError("report has no runner-backed evidence claim")` only when *no* claim is valid (exception: topic 5 with an empty neighbour packet). The docstring pins: "Questions keep links to unsupported claims: later judgement never erases raw human decisions."

**Where failure reasons travel.** Per-citation failure reasons are retained and visible downstream — but never to the seat that wrote the report. The judge packet (`scripts/stage2_research_judge.py`, `_packet_text`) carries every validated report minus its `raw` copy, so the judge sees `resolved` with each citation's reason; `_inputs` requires `evidence_status` in ("valid", "unsupported"), and `research_claim_scores` counts unsupported claims under their own name and takes no judgement for them (`prompts/research-swarm/judge.md`: judge only claims whose evidence status is valid). Publication (`scripts/stage2_research_run.py`, `compose`) writes each validated report as a `research-swarm/v2 report` JSON fence including `resolved`. The handoff inventory (`scripts/research_handoff.py`, `_valid_claims`, `derive_inventory`) counts only valid claims — neighbour relations "count" only when at least one listed claim is valid — while `[DECISION]` questions keep their claim links regardless. The gate `research-handoff` (`scripts/check_research_handoff.py`, declared in `decisions/gates.yaml` and `docs/governance/gate-catalog.md`) requires every criterion basis to name supported claims or answered records; unsupported claims stay in the record but support nothing.

**The only feedback channel today: the one correction.** `scripts/stage2_research_run.py` (`stage_topics`) invalidates a rejected answer (`invalidate` sets outcome `invalid-report` and `error` to the one-line `str(error)`) and plans exactly one correction by the same frozen seat, model, effort and tools (`correction_entry`). `correction_prompt` appends the seat's original brief with "Your answer for topic N was rejected by the report validator: \<reason\>" plus the fenced rejected answer. The reason is only the validation error line — for the evidence-floor failure that is exactly "report has no runner-backed evidence claim"; the per-citation `resolved` reasons are not part of any correction prompt. When at least one claim is runner-backed, the report validates and no correction happens at all: a seat whose citations partially fail receives no signal anywhere. Boundaries (ADR 0020 point 9, amended 2026-11-10): one correction per topic report, ceiling `39 + 3N` rising to at most `72 + 6N` with corrections, correction runs inside the seat's remaining original topic allowance (`remaining_topic_allowance`, `correction_slot_allowance`), in a second non-overlapping dispatch batch, resume adoption via `stored_correction_final`, bounded slot ids via `correction_slot_id`/`CORRECTION_SUFFIX`.

**Map scope.** `scripts/stage2_research_map.py` resolves merged finder locators against frozen bytes with the same resolver; unresolved entries keep `status: "unresolved"` with the resolver's `reason` and get no topic scope; resolved neighbour artifacts map to spec packets, `self`, or a `no-spec` gap.

**Doctrine.** ADR 0020 (`docs/adr/0020-phase-1-research-swarm.md`) point 6: "The runner joins resolved source/packet-commit/receipt excerpts in citation order and caps their total at 4,000 Unicode characters per claim… Missing, ambiguous or unparseable references remain unsupported" and "Bad references remain unsupported; a report needs at least one evidence-backed claim". Point 9 holds the correction amendment. `prompts/research-swarm/report.md` ("Evidence boundary") tells seats the citation forms per topic and that "One bad citation makes the entire claim unsupported and removes every attached excerpt, while retaining the claim. Every report needs at least one runner-backed claim… Do not invent source text to meet the evidence floor." `prompts/research-swarm/repository.md` tells finders "A line number alone is never a citation". `docs/WORKFLOW.md` contains no "citation" wording at all (not found there; the doctrine lives in ADR 0020, prompts and code).

**Pinned tests.** `tests/test_stage2_swarm.py`: `test_topic_report_gets_one_same_seat_correction` (asserts the correction prompt carries the original brief, the seat's own rejected answer and the rejection reason, and no peer content; exactly one correction; no substitution), plus tests for security/time boundaries, persistence and resume, first-batch reuse audit, invocation accounting, user-data delivery and bounded slot ids. `tests/test_stage2_research_report.py`: `test_report_bad_citation_invalidates_whole_claim_without_dropping_it`, `test_report_without_any_supported_claim_fails_except_empty_neighbours`, `test_report_one_shared_unicode_excerpt_cap_in_citation_order`. `tests/test_stage2_research_refs.py` pins the resolver reasons and `research_claim_evidence`.

## Where it lives

Resolver `scripts/stage2_research_refs.py` (`resolve_research_reference`, `research_claim_evidence`) · report validation `scripts/stage2_research_report.py` (`_reference`, `_page_reference`, `_evidence`, `validate_research_report`) · correction and publication `scripts/stage2_research_run.py` (`validate_topic`, `invalidate`, `correction_prompt`, `correction_entry`, `stage_topics`, `stored_correction_final`, `compose`, `publish`) · judge `scripts/stage2_research_judge.py` (`_inputs`, `_packet_text`, `research_claim_scores`) · handoff `scripts/research_handoff.py` and `scripts/check_research_handoff.py` · prompts `prompts/research-swarm/report.md`, `prompts/research-swarm/repository.md`, `prompts/research-swarm/judge.md` · ADR `docs/adr/0020-phase-1-research-swarm.md` · tests as listed above.

## What is unclear about it

- **The change's goal is not written anywhere I could read.** The bead `coding-harness-t2wm` description lives in the tracker (Dolt database under `.beads/`), which I cannot open with read-only file tools; the skeleton `research.md` and `plans/INDEX.md` carry only title and status. Which feedback direction is intended — richer rejection reasons in the correction prompt, a correction trigger for partially unsupported reports, or something else — is an open question for the maintainer (interview), not a fact.
- **Not found (searched, absent):** no mechanism returns per-citation failure reasons to the authoring seat (`correction_prompt` carries only the one-line validation error); no stage feeds citation outcomes back after a report that validated. **Not there (absent by design, per ADR 0020 point 6):** per-citation retry, prose-only or line-number citations, and any second resolution pass.
- Two claim-level assemblies exist: `research_claim_evidence` (refs, test-consumed) and `_evidence` (report, pipeline-consumed), with the same invalidation and cap semantics; whether they should be unified is unevaluated — `ci_gates.py` still calls the refs integration "pending".
- No test pins what a seat sees when rejection is the evidence-floor failure; the pinned correction-prompt assertions use a template-fields fault ("report fields do not match the template").
- Not read in depth (recorded as open, not as absence): `stage2_research_dispatch.py`, `stage2_research_limits.py`, `stage2_research_store.py`, `stage2_research_snapshot.py`, `stage2_research_history.py`, the finder/public prompts, and the full body of `check_research_handoff.py` (only its evidence-status handling around lines 161, 340, 368 was seen via search).

## Which files a change would have to touch

`scripts/stage2_research_report.py` (rejection reasons, evidence floor, `resolved` shape) · `scripts/stage2_research_run.py` (`correction_prompt`, `invalidate`, `stage_topics`, resume adoption) · possibly `scripts/stage2_research_refs.py` (resolver reasons, claim assembly) · possibly `scripts/stage2_research_judge.py` and `scripts/research_handoff.py`/`scripts/check_research_handoff.py` if what the judge or gate sees changes · prompts `prompts/research-swarm/report.md` (and `judge.md`/`repository.md` if doctrine moves) · policy text ADR 0020 (points 6/9) and `docs/WORKFLOW.md` if the contract changes — an ADR amendment is a maintainer decision PR (house rule 8) · tests `tests/test_stage2_swarm.py`, `tests/test_stage2_research_report.py`, `tests/test_stage2_research_refs.py`, `tests/test_research_handoff.py`, `tests/test_stage2_research_judge.py`.

## Neighbours known before the finders

`plans/changes/swarm-report-format/spec.md` (active, bead coding-harness-4q9y — the one-correction mechanism; its non-goals explicitly exclude changing "evidence resolution, scoring, handoff derivation", and its criterion 4 requires a rejection reason "suitable for a correction request") · `plans/changes/archive/2026-11-06-research-swarm/spec.md` (the swarm itself) · `plans/changes/archive/2026-11-06-swarm-time-limits/spec.md` (time limits the correction allowance reuses) · `plans/changes/swarm-test-speed/spec.md` (co-named in swarm-report-format's neighbours header) · no living spec covers the swarm (`plans/specs/` holds only `implementation-verification/spec.md`).
