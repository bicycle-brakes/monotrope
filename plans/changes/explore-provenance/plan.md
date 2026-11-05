---
title: "Plan — explore-provenance"
status: draft
implementation_status: partial
date: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-05
supersedes: null
superseded_by: null
bead: coding-harness-g19n
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, explore, provenance]
---

# Plan — explore-provenance

```text
For you:     Explore declares model-written research truthfully and removes its empty-file notices; affected active research is corrected once.
Done when:   Both Explore routes pass provenance, preservation and swarm-resume regressions, the active-file correction is complete, and make verify is green.
Appetite:    2 hours of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     Archived research, repository-wide provenance enforcement, model routes and changes to the new-change skeleton.
Pre-mortem:  suppose it failed: most likely because the header correction invalidated the swarm's stored resume binding.
Starts unless you say stop.
```

Implements [spec.md](spec.md) and the maintainer's answered scope in
`decisions.md`, Q-1; class `bounded` needs neither design nor ADR.

## Build sequence and files

1. Attempt: change `scripts/stage2.py` to prepare the publication bytes with an
   explicit research-publication mode rather than changing every `append()`.
   Correct only the frontmatter's provenance, producer, review and `updated:`,
   and remove only the generated opening paragraph and blockquote. Parse the
   header to locate complete metadata spans (inline or block mappings), splice
   the original bytes instead of dumping YAML, and preserve unrelated bytes,
   title and file mode. Use `producer_for(endpoint)` for Flash and Haiku,
   `stage2-research-swarm` for the swarm, and today's publication date; review
   becomes `{status: pending, approved_by: null, approved_at: null}`. Collapse
   replaced fields to one occurrence. Run the correction only with publication,
   not the pre-call audit append; rejected/empty answers leave the skeleton's
   authorship alone. Feed the final bytes through the existing `write_atomic()`
   once, keeping generic findings/audit append behavior intact.
2. Attempt: change `scripts/stage2_research_run.py` so `Run.publish()` uses the
   same prepared research bytes for its stored binding and its actual atomic
   publication, for complete and incomplete records. Keep compose, envelopes,
   failed-clear recomposition and write-failure recovery behavior unchanged.
3. Attempt: change `scripts/stage2_research_snapshot.py` to let `stored_binding()`
   additionally record the exact normalized digest of the runner-prepared
   corrected prefix (before the appended tail). `changed_against_stored()`
   accepts the original prefix for a not-yet-written publication, or that exact
   corrected prefix only with the recorded tail's matching length and digest.
   Existing records without the additional digest keep their current behavior.
   Do not globally ignore provenance/review fields, skeleton text or arbitrary
   body changes; leave the frozen-input drift check strict. The existing drift
   check runs before publication, so no blanket snapshot exemption is needed.
4. Attempt: extend `tests/test_stage2.py` with publication tests over Flash and
   the explicit Haiku fallback: real skeleton input, stale/inline/block metadata,
   prior approval, missing metadata, repeated publication, class preservation and
   rejection before a publishable answer. Use local model stand-ins only.
5. Attempt: extend `tests/test_stage2_swarm.py` with complete and incomplete
   publication tests starting from the real skeleton; assert truthful producer,
   pending review, no notices and unchanged structured research records. Extend
   `tests/test_stage2_research_deep_review.py` with a publication-byte test for
   CRLF/lone-CR preservation and a failed-replace/one-replace test; keep existing
   append and forged-envelope regressions meaningful. Add a skeleton-started,
   incomplete-then-resumed run that reuses successful seats and retries the judge.
6. Attempt: extend `tests/test_stage2_research_store.py` to exercise stored-binding
   comparison before publication, after corrected publication, with old records,
   and after foreign header, research-body and tail edits; exact runner bytes are
   the only new accepted state. Add `tests/test_explore_provenance.py` with a
   repository-data test scanning active `*/research.md` files (never archives)
   for false `human-written` declarations with published model evidence. Keep
   this last test skipped with the bootstrap reason until step 7, so the attempt
   does not depend on the orchestrator's cross-folder correction.
7. Orchestrator bootstrap, after the accepted attempt: correct
   `plans/changes/explore-provenance/research.md` and
   `plans/changes/loop-until-clean/research.md`, the affected active files at
   `a2b00438` (2026-11-04), using the same narrowly scoped correction. Their
   Explore audit evidence identifies `glm-coding-plan`/`glm-5.3-flash`, hence
   producer `claude-code`, with versions `2026-11-04` and `2026-10-14`
   respectively; stamp `updated:` on the actual correction day. Preserve the
   findings and historical call lines. Coordinate the latter file with its lane
   owner, enable the repository-data test in `tests/test_explore_provenance.py`,
   and prove it red against an affected pre-correction copy and green afterward.
   Re-scan active research first; if the affected set changed, name any additional
   paths in this plan before editing them under the already answered scope.
8. Attempt/orchestrator: update implementation status in
   `plans/changes/explore-provenance/spec.md` and
   `plans/changes/explore-provenance/plan.md` as appropriate, and replace each
   ledger's `not yet written` marker once its test exists. The runner owns
   `plans/changes/explore-provenance/findings.md`, generated `plans/INDEX.md`
   updates and measured entries under Time used. No files are deleted.

## Limits and route

The attempt does not edit either research backfill file; the orchestrator owns
those cross-folder corrections after the accepted attempt. No held path needs
an edit. Leave `scripts/new_change.py`, `scripts/check_frontmatter_current.py`,
`scripts/check_research_handoff.py`, `provenance.yaml`, `decisions/`, `docs/adr/`,
`AGENTS.md`, `prompts/`, `templates/`, settings, model declarations, archived
research and living specs untouched. No general cleanup command or new gate.

Explore used Stage 2, route `flash`, endpoint `glm-coding-plan`, model
`glm-5.3-flash` on 2026-11-04; no Stage-1 Explore fallback is recorded.
At `a2b00438`, `templates/plan.md` and
`scripts/validate_change_artefacts.py` do not exist: use the phase-3 prompt's
form and report the missing validator. `findings.md` contains draft-call
evidence and no phase-2a rows. The latest handover was read; current hosted
pull-request state and other sessions were not read within this runner boundary.

## Verification

For every new behavior test, record red on the uncorrected behavior and green
with the fix; when a planted fault raises, catch that specific exception in the
test and fail with `assert` or `pytest.fail`. Keep the fake providers offline.
Run the targeted checks in the attempt, and again after the bootstrap correction;
the orchestrator runs the final full verification after enabling the census test.

```sh
.venv/bin/python3 -m ruff check scripts/stage2.py scripts/stage2_research_run.py scripts/stage2_research_snapshot.py tests/test_stage2.py tests/test_stage2_swarm.py tests/test_stage2_research_deep_review.py tests/test_stage2_research_store.py tests/test_explore_provenance.py
.venv/bin/python3 -m ruff format --check scripts/stage2.py scripts/stage2_research_run.py scripts/stage2_research_snapshot.py tests/test_stage2.py tests/test_stage2_swarm.py tests/test_stage2_research_deep_review.py tests/test_stage2_research_store.py tests/test_explore_provenance.py
.venv/bin/python3 -m pytest -q tests/test_stage2.py -k explore
.venv/bin/python3 -m pytest -q tests/test_stage2_swarm.py tests/test_stage2_research_deep_review.py tests/test_stage2_research_store.py tests/test_stage2_research_snapshot.py tests/test_research_handoff.py tests/test_explore_provenance.py
python3 scripts/check_interview_minimums.py --change explore-provenance
python3 scripts/check_research_handoff.py --change explore-provenance
python3 scripts/check_criterion_ledger.py
make verify
```

## Criterion ledger

- 1: tests/test_stage2.py::test_explore_publishes_truthful_research_provenance — Flash or Haiku leaves the human-written declaration
- 1: tests/test_stage2_swarm.py::test_swarm_publication_corrects_research_provenance — complete or incomplete swarm records retain false provenance
- 2: tests/test_stage2.py::test_explore_publishes_truthful_research_provenance — the endpoint's producing program or publication date is wrong
- 2: tests/test_stage2_swarm.py::test_swarm_publication_corrects_research_provenance — a mixed swarm is attributed to one model or has no producer date
- 3: tests/test_stage2.py::test_explore_resets_review_without_changing_lifecycle — old approval survives publication or lifecycle fields change
- 3: tests/test_stage2_swarm.py::test_swarm_publication_corrects_research_provenance — published swarm research claims approval
- 4: tests/test_stage2.py::test_explore_removes_only_opening_skeleton_text — either notice survives or authored prose is removed
- 4: tests/test_stage2_swarm.py::test_swarm_publication_corrects_research_provenance — either generated opening notice survives swarm publication
- 5: tests/test_stage2_research_deep_review.py::test_research_publication_preserves_unrelated_bytes — a non-owned header/body span or its line endings change
- 6: tests/test_stage2_research_deep_review.py::test_research_publication_is_one_atomic_replacement — failed replacement changes bytes or success needs two replacements
- 7: tests/test_explore_provenance.py::test_active_model_research_has_no_false_human_provenance — an affected active research file remains after bootstrap
- 7: not a test — orchestrator reviews the two backfill diffs against their historical audit lines and unchanged body bytes; phase-6 review rejects invented attribution or archive edits
- 8: tests/test_stage2_research_deep_review.py::test_corrected_skeleton_publication_keeps_swarm_resume — successful seats rerun after a corrected incomplete publication
- 8: tests/test_stage2_research_store.py::test_binding_accepts_only_exact_research_provenance_publication — foreign edits pass, corrected publication cannot resume, or the pre-publication crash state stops matching

## Runner route — 2026-11-04

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-11-04

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM 5.3 Flash failed both attempts (ruff, then six red tests), 2026-11-04; continues from the kept attempt.

## Runner route — 2026-11-04

Stage-1 route: implement · model claude-sonnet-5-5 · reason: second Sonnet attempt, 2026-11-04: test_corrected_skeleton_publication_keeps_swarm_resume and test_swarm_publication_corrects_research_provenance are red because a resume after the corrected publication reruns every finder and seat; trace where the resume compares research.md (stage2_research_snapshot.changed_against_stored and the caller that records publication= in stored_binding) and make the stored binding carry the prepared corrected bytes before the write.

## Time used

2026-11-04 16:42:41–18:07:04 UTC, 5063 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-04 18:07:14–18:28:19 UTC, 1264 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-04 18:28:30–19:13:16 UTC, 2687 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-04 19:13:50–19:52:12 UTC, 2301 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-04 19:53:44–20:54:30 UTC, 3645 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · accepted · measured by the runner
2026-11-04 22:24:34–2026-11-05 00:08:44 UTC, 6250 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-05 08:51:51–09:21:28 UTC, 1777 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner

## Appetite overrun — 2026-11-04

Phase 4 took 14,960 s (about 4.2 h) against the 2-hour appetite: five implement attempts (two GLM 5.3 Flash, three Sonnet 5.5), measured above. The orchestrator did not stop at the limit; it reported the overrun after review-loop round 1, and the maintainer set a further 1.5 h for repairs (loop rows L1-4, L1-7, L1-9).
