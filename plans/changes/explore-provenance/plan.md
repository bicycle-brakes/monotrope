---
title: "Plan — explore-provenance"
status: draft
implementation_status: partial
date: 2026-11-04
last_reviewed: 2026-11-09
updated: 2026-11-14
supersedes: null
superseded_by: null
bead: coding-harness-g19n
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-09"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, explore, provenance]
---

# Plan — explore-provenance

```text
For you:     Explore records its producers truthfully, and the census rejects new research metadata defects while existing debt stays visible.
Done when:   Publication, resume and census regressions pass, the legacy exemption only shrinks, and make verify is green without bulk correction.
Appetite:    No further phase-4 hours; Q-3's additional two-hour tranche is spent according to Q-4. Stop if further implementation or repair is needed.
Not now:     Normalising existing research, recovering producers from history, archive cleanup, provenance policy and model routing.
Pre-mortem:  suppose it failed: most likely because the legacy exemption admitted a new defective research file.
Starts unless you say stop.
```

Implements [spec.md](spec.md) after the maintainer's Q-4 answer of 2026-11-07:
ship the Explore fix and future-file census; defer historical correction to
bead coding-harness-2i7x — normalise existing research. Q-1 through Q-3 still
supply the publication and whole-metadata contract, not the withdrawn bulk edit.
Class remains `bounded`, so no design file or ADR is due. Code is already
partial; review and verification must establish completion. This draft does
not renew implementation time or erase the previous attempts' measurements.

## Build sequence and files

1. Preserve the publication implementation in `scripts/stage2.py`:
   `research_publication()` prepares the owned provenance/producer/review/
   updated spans and removes only generated opening notices;
   `publish_research()` adds the accepted output through one `write_atomic()`
   replacement, preserving mode and unrelated bytes. Plain `append()` remains
   generic so a failed-call audit does not change authorship. Retain prior
   producer/model records, split known compound model identities into records,
   deduplicate identical contributions, and add the current program/date/model.
   Refuse unreadable or ambiguous attribution before publication rather than
   guessing a producer or discarding evidence. Preserve historical lifecycle
   dates; the census reports invalid ones instead of silently repairing them.
2. Preserve publication/resume alignment in `scripts/stage2_research_run.py`
   and `scripts/stage2_research_snapshot.py`: store exact prepared bytes and
   their publication day before writing, together with the private brief's
   research bytes and digest. Reuse the verified original frozen input before
   publication or the exact prepared prefix and recorded tail afterward;
   ignore only the existing `updated:` stamp. Retain old-binding compatibility
   and reject malformed, digest-only or foreign header/body/tail states.
   Keep the private brief's explained `0000-00-00` date sentinel out of published
   metadata so later-day resume preserves successful seats and prompt hashes.
3. Keep `scripts/research_census.py` as the read-only metadata library and its
   library registration in `scripts/ci_gates.py`. It recognises accepted,
   unquoted publication and existing model attribution, checks every owned
   field, nested/list member, program/date evidence and date ordering, and
   reports malformed metadata. It never invokes Git history or writes research.
   `scripts/normalise_active_research.py` was removed when Q-4 was applied
   (`0a5aeb3f`, 2026-11-09); leave it absent and do not restore its registration.
4. Keep the enabled repository census and independent fault fixtures in
   `tests/test_explore_provenance.py`. Gather findings before filtering the
   fixed full-path `UNCORRECTED` set; reject any unlisted defect. Remove listed
   paths as they become compliant or archived; no expansion or automatic
   date/directory exception is authorised. Retain complete producer/list,
   duplicate-key, date, notice, quoted/failed evidence and unreadable-input
   cases. Repair rows L9-1 and L9-2 authorise the I/O-error and read-only
   regressions below; the census scan lives in the library so baseline proofs
   exercise production code rather than copying its repair with the tests.
5. Verify `tests/test_stage2.py` for Flash and explicit Haiku fallback, pending
   review, opening-only removal and producer preservation; verify
   `tests/test_stage2_swarm.py` for complete/incomplete publication and several
   known models. Verify `tests/test_stage2_research_deep_review.py` for byte/mode
   preservation, refusal before writing, replacement failure, frozen brief and
   later-day resume. Verify `tests/test_stage2_research_store.py` for exact
   bindings, crash windows and corrupt/foreign state. Change these test files
   only if an authorised implementation repair is required; do not weaken their
   assertions to accommodate the reduced backfill scope.
6. Runner/orchestrator: retain the Q-4 scope in
   `plans/changes/explore-provenance/spec.md` and
   `plans/changes/explore-provenance/plan.md`; preserve call and review evidence
   in `plans/changes/explore-provenance/findings.md` and measured time below.
   The runner regenerates `plans/INDEX.md` after artifact-header edits.
   `plans/changes/explore-provenance/decisions.md` stays unchanged. No phase-2a
   review rows with an open Status exist in findings as read on 2026-11-09.

## Orchestrator boundary and untouched files

The attempt owns only the source/test files named above and this change's
permitted artifacts. Any required held-path edit belongs to the orchestrator
as bootstrap work after an accepted attempt: `provenance.yaml`,
`decisions/gates.yaml`, `model-endpoints.yaml`, `.claude/`, `.codex/`,
`.agents/`, `.pi/`, `.mcp.json`, `CLAUDE.md`, `prompts/`, `templates/`,
`.github/`, `.beads/`, `AGENTS.md`, `README.md`, and every committed prefix
whose only allowed class is `human-decided`. No such edit is currently planned.

Leave other changes' research and other artifacts, archives, living specs,
`scripts/new_change.py`, `scripts/check_frontmatter_current.py` and
`scripts/check_research_handoff.py` untouched. The former active-research
inventory is withdrawn by Q-4, not a bootstrap assignment. Verify
`tests/test_stage2_research_snapshot.py` and `tests/test_research_handoff.py`
as dependencies without editing them. Do not use a global metadata stamp or a
normaliser to make this change's verification pass.

Explore used Stage 2, route `flash`, endpoint `glm-coding-plan`, model
`glm-5.3-flash`, on 2026-11-04; no Stage-1 Explore fallback is recorded.
The historical implementation/repair fallback receipts remain below.

## Verification

Run the following offline checks, then the runner's full verification.
The I/O-error and read-only regressions are authorised by repair rows L9-1
and L9-2; ledger validity alone does not prove a criterion passes. Reject any
legacy-list additions relative to `0a5aeb3f` in the final diff review.

```sh
.venv/bin/python3 -m ruff check scripts/stage2.py scripts/stage2_research_run.py scripts/stage2_research_snapshot.py scripts/research_census.py scripts/ci_gates.py tests/test_stage2.py tests/test_stage2_swarm.py tests/test_stage2_research_deep_review.py tests/test_stage2_research_store.py tests/test_explore_provenance.py
.venv/bin/python3 -m ruff format --check scripts/stage2.py scripts/stage2_research_run.py scripts/stage2_research_snapshot.py scripts/research_census.py scripts/ci_gates.py tests/test_stage2.py tests/test_stage2_swarm.py tests/test_stage2_research_deep_review.py tests/test_stage2_research_store.py tests/test_explore_provenance.py
.venv/bin/python3 -m pytest -q tests/test_stage2.py -k 'explore or research_publication_preserves_all_producers'
.venv/bin/python3 -m pytest -q tests/test_stage2_swarm.py tests/test_stage2_research_deep_review.py tests/test_stage2_research_store.py tests/test_stage2_research_snapshot.py tests/test_research_handoff.py tests/test_explore_provenance.py
python3 scripts/check_interview_minimums.py --change explore-provenance
python3 scripts/check_research_handoff.py --change explore-provenance
python3 scripts/check_criterion_ledger.py
make verify
```

At `2c8eef87` on 2026-11-09, `templates/plan.md` and
`scripts/validate_change_artefacts.py` are absent. This plan follows the phase-3
prompt's card, file list and ledger; the named artifact validator is unavailable,
not green. The runner owns `plans_registry.py --check` and the full gate run.
Earlier draft failures in findings report stale `updated:` stamps in restored
research outside this scope. They are historical diagnostics: the read-only
frontmatter-currency check on 2026-11-09 found no current findings. No global
stamp or bulk provenance correction was performed.
Live hosted PR state and current parallel-session ownership were not read
within this runner's worktree/Git-only boundary; the latest relevant in-tree
handover was read. No tracker write, commit or cross-folder edit is part of this
redraft. Draft checks on 2026-11-09 passed the interview minimum, criterion
ledger, required-header/structure checks and preservation of route/time history;
the research-handoff check reports this change exempt without swarm evidence.
Keep the Definition of Done pending until the runner's full run is green.

## Criterion ledger

- 2: tests/test_stage2_research_deep_review.py::test_next_day_swarm_resume_passes_research_census — a later-day resumed envelope disagrees with retained producer attribution
- 8: tests/test_stage2_research_deep_review.py::test_next_day_swarm_resume_passes_research_census — a later-day resume fails the census or repeats successful seats
- 1: tests/test_stage2.py::test_explore_publishes_truthful_research_provenance — Flash or fallback leaves false provenance
- 1: tests/test_stage2_swarm.py::test_swarm_publication_corrects_research_provenance — complete/incomplete swarm publication leaves false provenance
- 2: tests/test_stage2.py::test_explore_publishes_truthful_research_provenance — the publication's producer or date is wrong
- 2: tests/test_stage2.py::test_research_publication_preserves_all_producers — a repeated publication loses an earlier contribution
- 2: tests/test_stage2_swarm.py::test_swarm_publication_preserves_prior_producers — several known models collapse into one producer
- 3: tests/test_stage2.py::test_explore_resets_review_without_changing_lifecycle — approval survives publication
- 3: tests/test_stage2_swarm.py::test_swarm_publication_corrects_research_provenance — swarm research claims approval
- 4: tests/test_stage2.py::test_explore_removes_only_opening_skeleton_text — a notice survives or an authored quotation disappears
- 4: tests/test_stage2_swarm.py::test_swarm_publication_corrects_research_provenance — opening notices survive swarm publication
- 5: tests/test_stage2_research_deep_review.py::test_research_publication_preserves_unrelated_bytes — unrelated metadata, prose or line endings change
- 6: tests/test_stage2_research_deep_review.py::test_research_publication_is_one_atomic_replacement — failed replacement changes bytes or success needs two replacements
- 6: tests/test_stage2_research_deep_review.py::test_invalid_research_publication_is_refused_without_writing — invalid preparation alters the file
- 7: tests/test_explore_provenance.py::test_active_model_research_has_no_false_human_provenance — an unlisted active file violates the contract
- 7: tests/test_explore_provenance.py::test_active_census_is_enabled — the repository-data guard is skipped
- 7: tests/test_explore_provenance.py::test_census_exemption_is_limited_to_the_listed_files — an exemption hides a new file's defect
- 8: tests/test_stage2_research_deep_review.py::test_corrected_skeleton_publication_keeps_swarm_resume — successful seats repeat after correction
- 8: tests/test_stage2_research_deep_review.py::test_resume_reuses_publication_bytes_and_day — a later day or crash changes prepared publication bytes
- 8: tests/test_stage2_research_deep_review.py::test_producer_history_survives_swarm_resume — retained producers change private brief hashes
- 8: tests/test_stage2_research_store.py::test_binding_accepts_only_exact_research_provenance_publication — foreign edits pass or the exact publication cannot resume
- 9: tests/test_explore_provenance.py::test_uncorrected_stock_only_shrinks — a compliant or archived path remains exempt
- 9: tests/test_explore_provenance.py::test_census_exemption_is_limited_to_the_listed_files — a directory-wide exception hides an unlisted file
- 9: not a test — phase-6 diff review compares UNCORRECTED with its fixed 0a5aeb3f set and rejects every addition
- 10: tests/test_explore_provenance.py::test_census_rejects_incomplete_publication_metadata — an owned-field or date defect goes unreported
- 10: tests/test_explore_provenance.py::test_census_accepts_and_checks_every_producer — a bad list member or nested duplicate passes
- 10: tests/test_explore_provenance.py::test_census_requires_publication_and_reads_scalar_spellings — quoted examples or failed audits establish publication
- 10: tests/test_explore_provenance.py::test_census_reads_real_line_endings — CRLF hides a metadata violation
- 10: tests/test_explore_provenance.py::test_census_names_unreadable_headers — a bad header is silently skipped
- 10: tests/test_explore_provenance.py::test_census_reports_undecodable_research — invalid UTF-8 aborts or escapes the census
- 10: tests/test_explore_provenance.py::test_census_reports_opening_skeleton_notices — an opening notice goes unreported
- 10: tests/test_explore_provenance.py::test_census_reports_read_errors — an OSError aborts without a path-specific census finding
- 10: tests/test_explore_provenance.py::test_census_is_read_only_without_history — the census writes research or requires Git-history reconstruction

## Runner route — 2026-11-04

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-11-04

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM 5.3 Flash failed both attempts (ruff, then six red tests), 2026-11-04; continues from the kept attempt.

## Runner route — 2026-11-04

Stage-1 route: implement · model claude-sonnet-5-5 · reason: second Sonnet attempt, 2026-11-04: test_corrected_skeleton_publication_keeps_swarm_resume and test_swarm_publication_corrects_research_provenance are red because a resume after the corrected publication reruns every finder and seat; trace where the resume compares research.md (stage2_research_snapshot.changed_against_stored and the caller that records publication= in stored_binding) and make the stored binding carry the prepared corrected bytes before the write.

## Runner route — 2026-11-06

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Runner route — 2026-11-09

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Runner route — 2026-11-11

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Runner route — 2026-11-13

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-11-04 16:42:41–18:07:04 UTC, 5063 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-04 18:07:14–18:28:19 UTC, 1264 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-04 18:28:30–19:13:16 UTC, 2687 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-04 19:13:50–19:52:12 UTC, 2301 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-04 19:53:44–20:54:30 UTC, 3645 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · accepted · measured by the runner
2026-11-04 22:24:34–2026-11-05 00:08:44 UTC, 6250 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-05 08:51:51–09:21:28 UTC, 1777 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-05 11:52:54–13:32:37 UTC, 5983 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-05 14:33:13–16:21:03 UTC, 6470 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-05 18:58:04–20:01:38 UTC, 3814 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-05 20:02:03–2026-11-06 01:00:56 UTC, 17931 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-11-06 01:01:07–05:50:49 UTC, 17380 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · accepted · measured by the runner
2026-11-06 15:40:31–16:10:43 UTC, 1812 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-06 16:10:52–16:52:51 UTC, 2518 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · accepted · measured by the runner
2026-11-06 22:12:15–2026-11-07 00:14:35 UTC, 7339 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-09 12:45:59–17:54:05 UTC, 18485 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-09 17:54:20–18:00:14 UTC, 354 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · accepted · measured by the runner
2026-11-09 20:06:15–20:15:59 UTC, 584 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-09 20:16:39–20:19:42 UTC, 184 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-11-09 20:20:05–20:21:48 UTC, 103 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-10 13:55:49–15:17:25 UTC, 4895 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-10 15:17:41–20:29:01 UTC, 18679 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · accepted · measured by the runner
2026-11-10 21:58:36–23:42:35 UTC, 6238 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-10 23:42:50–2026-11-11 02:36:28 UTC, 10417 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-11-11 02:36:39–03:31:54 UTC, 3314 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · accepted · measured by the runner
2026-11-11 20:51:37–20:56:32 UTC, 295 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-13 16:20:05–16:22:50 UTC, 165 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-13 16:23:10–16:25:18 UTC, 128 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-11-13 16:25:39–16:28:56 UTC, 197 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-13 19:47:05–20:05:28 UTC, 1102 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-13 20:44:24–20:46:14 UTC, 110 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner

## Appetite overrun — 2026-11-04

Phase 4 took 14,960 s (about 4.2 h) against the 2-hour appetite: five implement attempts (two GLM 5.3 Flash, three Sonnet 5.5), measured above. The orchestrator did not stop at the limit; it reported the overrun after review-loop round 1, and the maintainer set a further 1.5 h for repairs (loop rows L1-4, L1-7, L1-9).

## One-time correction — 2026-11-13 (decisions.md#Q-6)

The orchestrator corrects the headers of
`plans/changes/decision-statement-skeleton/research.md` and
`plans/changes/verify-step-limit/research.md` (provenance, producer, review,
the leftover skeleton notice); no other folder is touched.

## Header-only correction as a rule — 2026-11-14 (decisions.md#Q-8)

Until this change merges, the orchestrator corrects the header of every
research file of another change that the census flags — provenance, producer,
review, the leftover skeleton notice and the `updated:` stamp; never content.
After the merge of main on 2026-11-14 the census flagged
`plans/changes/origin-check-across-blocks/research.md` (opening skeleton
notice only); its notice was removed and its `updated:` stamped.
