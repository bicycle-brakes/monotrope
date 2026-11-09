---
title: "Plan — explore-provenance"
status: draft
implementation_status: partial
date: 2026-11-04
last_reviewed: 2026-11-09
updated: 2026-11-09
supersedes: null
superseded_by: null
bead: coding-harness-g19n
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by:
  - kind: llm-session
    name: codex
    version: "2026-11-09"
    model: gpt-6.1-sol
  - kind: llm-session
    name: claude-code
    version: "2026-11-09"
    model: glm-5.3
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, explore, provenance]
---

# Plan — explore-provenance

```text
For you:     Explore publishes truthful metadata; the census catches new defects while the recorded old files await separate correction.
Done when:   Publication and resume regressions, the census with fixed legacy exceptions, and make verify pass without a historical backfill.
Appetite:    No additional phase-4 budget; Q-3's two-hour repair tranche is spent — stop before further implementation needs more time.
Not now:     One-time normalisation, historical producer recovery, other changes' research, archives, model routes and the new-change skeleton.
Pre-mortem:  suppose it failed: most likely because legacy exceptions also hid defects in new research.
Starts unless you say stop.
```

Implements [spec.md](spec.md) under the maintainer's Q-4 answer of 2026-11-07.
Class remains `bounded`: no design file or ADR is due. The current tree at
`ff594213` (2026-11-09) already has the narrowed implementation; this plan
records its required shape and remaining verification, not a fresh repair
budget. Retain working code, verify it, and report any unmet criterion before
spending further phase-4 time.

## Build sequence and files

1. Attempt: retain the publication boundary in `scripts/stage2.py`.
   `research_publication()` prepares complete owned metadata spans, keeps all
   known input producer/model records and removes only generated opening notices;
   `publish_research()` appends accepted output in one `write_atomic()`
   replacement, retaining unrelated bytes and mode. Map single-model endpoints
   through `producer_for()` and record the current model separately. Generic
   `append()` remains generic: an audit or rejected answer is not authorship.
   Refuse unreadable/ambiguous input before publication; do not reconstruct
   missing producers from Git history.
2. Attempt: retain `scripts/stage2_research_run.py`'s prepared swarm publication
   bytes/day and private brief, and `scripts/stage2_research_snapshot.py`'s
   exact binding of those inputs. Mixed swarms use `stage2-research-swarm`.
   Resume reuses frozen bytes across crashes and calendar days, accepts only
   the original source or exact corrected prefix with its recorded tail, and
   ignores only the existing `updated:` stamp. The private brief uses
   `0000-00-00` for its date and keeps its prepared bytes/digest. Preserve old
   bindings lacking optional publication/brief fields; reject malformed or
   digest-only partial records. Never ignore foreign producer, review, body
   or tail edits to make reuse succeed.
3. Attempt: retain `scripts/research_census.py` as a read-only validation
   library with no normalisation entry point. Validate every contract field,
   producer-list member, duplicate owned/nested key and date relationship.
   Identify model-written research by existing attribution or accepted unquoted
   publication evidence, independently of its current provenance label.
   `scripts/ci_gates.py` registers this library's caller, the pytest census;
   CI never rewrites research.
4. Attempt: retain `tests/test_explore_provenance.py`'s enabled scan of every
   `plans/changes/*/research.md`, excluding archives, and report defects before
   filtering the explicit `UNCORRECTED` paths. Freeze the maximum exception set
   to that file at `ff594213`; only remove corrected or archived entries, never
   add new failures or directory exemptions. Keep adversarial fixtures for
   quoted/fenced text, failed calls, LF/CRLF, missing/duplicate fields, invalid
   dates, every producer member and opening notices. Extend unreadable-input
   coverage to an `OSError` raised for one path and require a path-specific
   finding while the scan continues to another invalid file; do not silently
   skip it or abort the whole scan. This remains outstanding if verification
   finds the current read/decode handling incomplete.
5. Attempt: retain regressions in `tests/test_stage2.py` for Flash/explicit
   fallback, review reset, notices and producer retention; in
   `tests/test_stage2_swarm.py` for complete/incomplete swarm publication and
   earlier contributors; in `tests/test_stage2_research_deep_review.py` for
   unrelated bytes/mode, preparation refusal, atomic failure, private brief
   and later-day resume; and in `tests/test_stage2_research_store.py` for exact
   bindings, crash states, corrupt records and foreign edits. Use local model
   stand-ins. Do not weaken producer preservation because the historical
   backfill was deferred.
6. Runner/orchestrator: retain the narrowed spec in
   `plans/changes/explore-provenance/spec.md`, this
   `plans/changes/explore-provenance/plan.md`, the unchanged maintainer answers
   in `plans/changes/explore-provenance/decisions.md` and audit/review evidence
   in `plans/changes/explore-provenance/findings.md`. The runner regenerates
   `plans/INDEX.md` after header edits and records measured time. Preserve
   earlier routes and durations below: phase 4 already ran, so Time used is
   not reset by this redraft. No new answer is written for the maintainer.
7. Orchestrator verification: confirm the PR has no cross-folder historical
   research corrections and no `scripts/normalise_active_research.py`, removed
   before this draft by `ff594213`. That removed script is not reintroduced;
   its Git-history recovery belongs to the separate historical-provenance
   correction task (bead coding-harness-2i7x, named by the census library).
   Run targeted checks and `make verify`, then proceed through review. Red
   checks are reported; they do not authorise another repair tranche.

## Limits and route

No held path needs an implementation edit. If one becomes necessary, only the
orchestrator may make the bootstrap edit after an accepted attempt: held paths
include `provenance.yaml`, `decisions/gates.yaml`, `model-endpoints.yaml`,
`.claude/`, `.codex/`, `.agents/`, `.pi/`, `.mcp.json`, `CLAUDE.md`, `prompts/`,
`templates/`, `.github/`, `.beads/`, `AGENTS.md`, `README.md` and any committed
prefix allowing only `human-decided`, matched without regard to letter case.
The current plan assigns no edits to those paths.

Leave `scripts/new_change.py`, `scripts/check_frontmatter_current.py`,
`scripts/check_research_handoff.py`, `tests/test_stage2_research_snapshot.py`,
`tests/test_research_handoff.py`, other changes' files, archived research and
living specs untouched. The last two test modules are verification dependencies.
There are no new files to create and no further files to delete.

Explore used Stage 2, route `flash`, endpoint `glm-coding-plan`, model
`glm-5.3-flash`, on 2026-11-04; no Stage-1 Explore fallback is recorded.
Historical implementation/repair fallback receipts remain below. Q-4 defers
historical normalisation, not the complete future-publication contract.

## Verification

Run from the worktree with offline fixtures. These commands verify the shipped
contract; none performs a historical rewrite. For additional repair, stop at
the spent appetite before editing implementation. Preserve independent fault
fixtures even where publisher and census share opening-notice detection.

```sh
.venv/bin/python3 -m ruff check scripts/stage2.py scripts/stage2_research_run.py scripts/stage2_research_snapshot.py scripts/research_census.py scripts/ci_gates.py tests/test_stage2.py tests/test_stage2_swarm.py tests/test_stage2_research_deep_review.py tests/test_stage2_research_store.py tests/test_explore_provenance.py
.venv/bin/python3 -m ruff format --check scripts/stage2.py scripts/stage2_research_run.py scripts/stage2_research_snapshot.py scripts/research_census.py scripts/ci_gates.py tests/test_stage2.py tests/test_stage2_swarm.py tests/test_stage2_research_deep_review.py tests/test_stage2_research_store.py tests/test_explore_provenance.py
.venv/bin/python3 -m pytest -q tests/test_stage2.py -k 'explore or research_publication'
.venv/bin/python3 -m pytest -q tests/test_stage2_swarm.py tests/test_stage2_research_deep_review.py tests/test_stage2_research_store.py tests/test_stage2_research_snapshot.py tests/test_research_handoff.py tests/test_explore_provenance.py
python3 scripts/check_interview_minimums.py --change explore-provenance
python3 scripts/check_research_handoff.py --change explore-provenance
python3 scripts/check_criterion_ledger.py
make verify
```

At `ff594213` on 2026-11-09, `templates/plan.md` and
`scripts/validate_change_artefacts.py` are absent; this plan follows the phase-3
prompt's form, and the unavailable artifact validator cannot be reported green.
`findings.md` contains runner receipts, not open phase-2a rows to resolve.
The latest in-tree handover dated 2026-11-06 was read and checked against the
newer Q-4 record and current tree. Live hosted PR state and current session
ownership were not read within the runner's worktree/Git-only boundary.

### Draft validation — 2026-11-09

Measured against the working tree based on `ff594213`:

- Interview minimums pass for this change; research handoff reports the
  legacy exemption because no research-swarm/v2 evidence is present.
- `python3 scripts/check_criterion_ledger.py` passes, including the explicit
  not-yet-written read-error test for criterion 10. Reading
  `census_findings()` confirms that it catches decoding errors but currently
  lets an `OSError` escape. Passing existing tests does not close this gap.
- `.venv/bin/python3 -m pytest -q tests/test_explore_provenance.py tests/test_stage2_research_deep_review.py::test_spec_covers_private_brief_normalization`
  passes: 53 tests. This is targeted evidence, not full publication/resume or
  implementation acceptance.
- `python3 scripts/check_frontmatter_current.py` exits 1 on research files
  outside this change whose `updated` predates their edit in `ff594213`.
  The earlier draft's docs-job receipt records the same blocking gate.
  Do not run a repository-wide stamp from this attempt: those paths are
  outside its write scope and remain protected by this spec.
- Full `make verify` is left to the runner. Neither an unavailable validator
  nor the known red date gate is reported green; no acceptance criterion,
  class or maintainer answer is changed to bypass them.

Third draft attempt (claude-code · glm-5.3, 2026-11-09), verified by reading
rather than running: every ledger-named test below is defined in its file and
`test_census_reports_unreadable_research` is not; `UNCORRECTED` holds exactly
the deferred stock the spec's term names; `census_findings()` catches
`UnicodeDecodeError` but not an `OSError` from reading a research file
(`tests/test_explore_provenance.py:103`), so the not-yet-written entry stands;
`scripts/research_census.py` is the read-only library registered in
`ci_gates.OHNE_AUFRUFER` and `scripts/normalise_active_research.py` is absent;
`research_publication()`, `publish_research()`, `research_opening_notices()`
and the `0000-00-00` brief sentinel exist where the build sequence names them.
Every `frontmatter-current` finding names a clean file outside this change
folder, last changed by `ff594213`; the repository-wide stamp stays outside
this draft's write scope, as it was outside the two before it.

## Criterion ledger

- 1: tests/test_stage2.py::test_explore_publishes_truthful_research_provenance — Flash or fallback leaves false provenance
- 1: tests/test_stage2_swarm.py::test_swarm_publication_corrects_research_provenance — complete/incomplete swarm retains false provenance
- 2: tests/test_stage2.py::test_explore_publishes_truthful_research_provenance — the publication program, model or date is wrong
- 2: tests/test_stage2.py::test_research_publication_preserves_all_producers — publication discards an earlier input contribution
- 2: tests/test_stage2_swarm.py::test_swarm_publication_preserves_prior_producers — swarm overwrites earlier attribution
- 3: tests/test_stage2.py::test_explore_resets_review_without_changing_lifecycle — approval survives publication
- 3: tests/test_stage2_swarm.py::test_swarm_publication_corrects_research_provenance — swarm claims human approval
- 4: tests/test_stage2.py::test_explore_removes_only_opening_skeleton_text — a notice survives or authored quotation disappears
- 4: tests/test_stage2_swarm.py::test_swarm_publication_corrects_research_provenance — opening notices survive a swarm publication
- 5: tests/test_stage2_research_deep_review.py::test_research_publication_preserves_unrelated_bytes — unrelated metadata, prose or line endings change
- 6: tests/test_stage2_research_deep_review.py::test_research_publication_is_one_atomic_replacement — failure changes prior bytes or success needs two replacements
- 6: tests/test_stage2_research_deep_review.py::test_invalid_research_publication_is_refused_without_writing — invalid input is rewritten
- 7: tests/test_explore_provenance.py::test_active_model_research_has_no_false_human_provenance — an unlisted active file violates the contract
- 7: tests/test_explore_provenance.py::test_active_census_is_enabled — the repository-data check is skipped
- 8: tests/test_stage2_research_deep_review.py::test_corrected_skeleton_publication_keeps_swarm_resume — corrected metadata reruns successful seats
- 8: tests/test_stage2_research_deep_review.py::test_resume_reuses_publication_bytes_and_day — a later day or crash changes prepared bytes
- 8: tests/test_stage2_research_deep_review.py::test_producer_history_survives_swarm_resume — retained producers change private-brief hashes
- 8: tests/test_stage2_research_store.py::test_binding_accepts_only_exact_research_provenance_publication — foreign edits pass as unchanged input
- 9: tests/test_explore_provenance.py::test_uncorrected_stock_only_shrinks — a corrected or archived entry stays exempt
- 9: tests/test_explore_provenance.py::test_census_exemption_is_limited_to_the_listed_files — exempting one path also exempts new research
- 9: not a test — phase-6 review compares UNCORRECTED with its fixed set at ff594213 (2026-11-09), rejecting added paths or wildcard exemptions
- 10: tests/test_explore_provenance.py::test_census_rejects_incomplete_publication_metadata — a contract field or date violation passes
- 10: tests/test_explore_provenance.py::test_census_requires_publication_and_reads_scalar_spellings — quoted examples or failed calls establish publication
- 10: tests/test_explore_provenance.py::test_census_names_unreadable_headers — malformed or missing frontmatter is skipped
- 10: tests/test_explore_provenance.py::test_census_reports_undecodable_research — invalid UTF-8 aborts or escapes the report
- 10: not yet written tests/test_explore_provenance.py::test_census_reports_unreadable_research — one read error aborts scanning or loses its path-specific finding
- 10: tests/test_explore_provenance.py::test_census_reports_opening_skeleton_notices — generated notices over published research escape the report
- 10: tests/test_explore_provenance.py::test_census_reads_real_line_endings — CRLF hides publication or false provenance
- 10: tests/test_explore_provenance.py::test_census_accepts_and_checks_every_producer — a list member is invalid or silently dropped

## Runner route — 2026-11-04

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-11-04

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM 5.3 Flash failed both attempts (ruff, then six red tests), 2026-11-04; continues from the kept attempt.

## Runner route — 2026-11-04

Stage-1 route: implement · model claude-sonnet-5-5 · reason: second Sonnet attempt, 2026-11-04: test_corrected_skeleton_publication_keeps_swarm_resume and test_swarm_publication_corrects_research_provenance are red because a resume after the corrected publication reruns every finder and seat; trace where the resume compares research.md (stage2_research_snapshot.changed_against_stored and the caller that records publication= in stored_binding) and make the stored binding carry the prepared corrected bytes before the write.

## Runner route — 2026-11-06

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

## Appetite overrun — 2026-11-04

Phase 4 took 14,960 s (about 4.2 h) against the 2-hour appetite: five implement attempts (two GLM 5.3 Flash, three Sonnet 5.5), measured above. The orchestrator did not stop at the limit; it reported the overrun after review-loop round 1, and the maintainer set a further 1.5 h for repairs (loop rows L1-4, L1-7, L1-9).
