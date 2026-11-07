---
title: "Plan — explore-provenance"
status: draft
implementation_status: partial
date: 2026-11-04
last_reviewed: 2026-11-06
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-g19n
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, explore, provenance]
---

# Plan — explore-provenance

```text
For you:     Explore and all active model-written research carry complete, truthful metadata and retain every known producer.
Done when:   Publication and resume regressions pass, the one-time normalisation preserves producer lists, the complete active-file census passes, and make verify is green.
Appetite:    2 additional hours of phase 4 from the Q-3 restart, repairs included — a stop, not an estimate; earlier measured time stays recorded.
Not now:     Archived research, other changes' findings or contracts, repository-wide provenance enforcement, model routes and the new-change skeleton.
Pre-mortem:  suppose it failed: most likely because normalisation replaced several historical contributors with the latest publisher.
Starts unless you say stop.
```

Implements [spec.md](spec.md), including the wider normalisation and attribution
scope expressly authorised by maintainer answers Q-2 and Q-3 in `decisions.md`
on 2026-11-06. Class remains `bounded`: no design file or ADR is due.
Existing implementation is partial; this redraft specifies its remaining repair.

## Build sequence and files

1. Attempt: repair `scripts/stage2.py` so the explicit research-publication
   preparation and `publish_research()` retain evidence-backed producer records
   while adding the accepted contribution. Keep `append()` generic: an audit
   without accepted output never changes authorship. A single producer remains
   a mapping; several use a non-empty `produced_by` list. Each record keeps
   `kind: llm-session`, program `name`, ISO date `version` and known `model`
   identity. Map current single-model endpoints through `producer_for()` and
   mixed swarm publication to `stage2-research-swarm`; never assign a guessed
   model to an old program. Remove only generated opening notices, replace
   complete owned metadata spans, reject unreadable inputs before writing,
   reset review to pending and atomically publish once, preserving other bytes
   and mode. Update same-day/repeated-publication assertions to retain prior
   attribution rather than overwrite it.
2. Attempt: keep `scripts/stage2_research_run.py` and
   `scripts/stage2_research_snapshot.py` aligned with that preparation. Freeze
   exact prepared bytes and publication day before writing; reuse those bytes
   after a crash or on a later date. Resume accepts original frozen input before
   publication, or the exact corrected prefix with the recorded tail length
   and digest afterward, ignoring only the existing `updated:` stamp. Preserve
   old bindings without publication fields; malformed or digest-only partial
   records refuse reuse. Build the private brief from the corrected research
   with its explained `0000-00-00` sentinel. Retain the exact prepared research
   portion of that brief and its digest in the new binding, and reuse it only
   after the source binding is verified: adding a producer record must not
   change prompt hashes after publication. Bindings lacking that optional brief
   keep their existing preparation behavior. Do not ignore arbitrary producer,
   review, body or tail changes or weaken frozen-input checks.
3. Attempt: repair `scripts/normalise_active_research.py`, already added by the
   previous repair, as the explicitly invoked one-time normaliser. Share the
   complete contract check with the census, recursively validating every
   mapping/list member and duplicate owned/nested keys. Discover active files
   by `plans/changes/*/research.md`; use accepted unquoted publications and
   existing model attribution, not only a `human-written` label. Preserve all
   known contributors, splitting legacy compound model attribution into records
   with a separate model identity and retaining evidence-backed programs/dates;
   the latest audit identifies one contribution, not the whole document.
   Recover attribution already lost by this branch from the pre-correction Git
   versions (the branch base is `9633355e915bc64266d26b49575f63e486641471`;
   consult earlier branch versions for files created later), comparing original
   and final contributor sets. Do not replace historical dates with the edit
   date or manufacture evidence. Unknown evidence or invalid metadata stops
   preparation with a path-specific error. Default mode reports candidates;
   `--write` uses `write_atomic()` only after every candidate is prepared and
   validated. A second run makes no further changes. Keep this script's
   explicit non-gate registration in `scripts/ci_gates.py`: CI checks results
   and never rewrites research.
4. Attempt: extend `tests/test_explore_provenance.py` so the enabled census checks
   every contract field and producer-list member, unreadable files, duplicate
   keys, program/date evidence, date ordering and notices, independently of the
   current provenance label. Retain tests distinguishing quoted/fenced examples
   and failed audits from accepted publication. Add fixtures for single and
   multiple producers, legacy compound models, missing historical evidence,
   idempotence, preservation of unrelated bytes, dry-run and validation of the
   entire batch before writing. The repository-data test stays enabled; the
   candidate attempt may need the orchestrator's backfill before its final green
   verification, so report that dependency rather than skip or weaken the test.
5. Attempt: extend `tests/test_stage2.py` for Flash and explicit Haiku fallback,
   pending review, repeated publications and retention of earlier producers;
   extend `tests/test_stage2_swarm.py` for complete/incomplete swarm publication
   and earlier producer retention. Keep real skeleton inputs and local model
   stand-ins. Extend `tests/test_stage2_research_deep_review.py` for byte/mode
   preservation, refusal before writing, atomic failure and later-day resume
   without rerunning successful seats. Keep
   `tests/test_stage2_research_store.py` regressions for exact bindings, crash
   windows, corrupt records and foreign header/body/tail edits; retain snapshot
   and handoff regressions as verification dependencies, without editing them.
6. Orchestrator bootstrap after the accepted attempt: restore any producer
   knowledge lost by the previous backfill, run the repaired normaliser over
   all active research and review every changed research diff against its
   pre-correction attribution and publication evidence. The complete inventory
   below replaces the former two-file exception; only metadata/generated notices
   may change, and compliant files stay byte-identical. Coordinate cross-folder
   writes with the owning lanes. Never ask the attempt to edit these cross-folder
   files: the runner restores paths outside its allowed change area. Run the
   enabled census and targeted checks again, then `make verify`.
7. Attempt/runner: align `plans/changes/explore-provenance/spec.md` and
   `plans/changes/explore-provenance/plan.md` with actual implementation status
   and replace ledger markers only when tests exist. The runner owns audit and
   review evidence in `plans/changes/explore-provenance/findings.md`, measured
   Time used entries, and regeneration of `plans/INDEX.md`; no earlier evidence
   is erased. `plans/changes/explore-provenance/decisions.md` remains the
   maintainer's unchanged source of answers. No file is deleted.

## Active research inventory

As read at `8bc239c4` on 2026-11-06, every path below is in the one-time
normalisation and census scope. For each file, the orchestrator corrects only
non-compliant metadata/generated opening notices, restores known contributors,
and preserves its research; a compliant file receives no write. All of these
research paths are explicitly authorised by Q-2/Q-3, including other lanes.
Re-scan before applying; name any newly present path here before editing it.

- `plans/changes/adr-0016-docs-check/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/adr-owning-change/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/architecture-reconcile/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/attempt-diagnostics/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/beads-close-themselves/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/ci-bead-summary/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/ci-minutes/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/codex-drafts/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/codex-repairs/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/codex-takeover/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/criterion-test-ledger/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/dirty-index/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/docs-job-report-header/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/draft-gates-only/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/explore-provenance/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/explore-role/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/explorer-reviewer-agents/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/fail-fast-attempts/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/failed-check-secrets/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/failed-check-spans/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/free-member-rate-limit/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/go-access-point/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/guard-test/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/haiku-5-5/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/handover-at-95/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/harness-decide-adr/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/hermes-runner/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/index-merge-regenerates/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/interview-context/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/interview-fenced-examples/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/kimi-admission/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/ledger-instance-layout/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/ledger-marker/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/loop-structure-first/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/loop-until-clean/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/malformed-answer-retry/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/merge-queue/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/mutation-evidence-module/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/pi-catalog-redirect/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/pi-pin/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/plan-held-paths/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/provenance-location/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/raising-fault-test/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/ratchet-mutation-evidence/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/red-first-install/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/red-first-own-refs/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/red-first-pytest-failed/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/registry-block-last/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/repair-fixed-line-format/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/repair-fixed-lines/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/repair-restore-status/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/research-currency/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/research-swarm/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/restore-symlink-parent/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/review-loop-deep-a/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/review-loop-deep-b/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/review-release-lock/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/review-verdict-validated/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/run-report/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/runner-time-line/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/runner-time-line-exits/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/sol-effort/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/stage2-format/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/stage2-repair/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/stage2-session/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/swarm-test-speed/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/terms-expiry/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/terms-test-fixtures/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/test-key-runtime/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/test-strength-rows/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/time-records-data/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/tolerate-derived-leftovers/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/venv-pycache/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/verify-absolute-python/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/verify-machine-lock/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/verify-stages-new-files/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/verify-worker-cap/research.md` — Normalise if needed; retain research and contributors.
- `plans/changes/workflow-promises/research.md` — Normalise if needed; retain research and contributors.

## Limits and route

No held path needs an implementation edit. Any later need to edit a held path
(`provenance.yaml`, `decisions/gates.yaml`, `model-endpoints.yaml`, `.claude/`,
`.codex/`, `.agents/`, `.pi/`, `.mcp.json`, `CLAUDE.md`, `prompts/`, `templates/`,
`.github/`, `.beads/`, `AGENTS.md`, `README.md` or a committed human-decided
prefix) belongs to the orchestrator after the accepted attempt. Leave
`scripts/new_change.py`, `scripts/check_frontmatter_current.py`,
`scripts/check_research_handoff.py`, archived research, living specs, research
findings and other changes' non-research files untouched. The normaliser is an
explicit one-time tool, not a new scheduled correction or general gate.

Explore used Stage 2, route `flash`, endpoint `glm-coding-plan`, model
`glm-5.3-flash`, on 2026-11-04; no Stage-1 Explore fallback is recorded.
Historical implementation/repair fallback receipts and measured durations are
retained below. Q-3 authorises two additional repair hours from this restart;
stop and report unfinished work when that tranche is spent.

At `8bc239c4`, `templates/plan.md` and
`scripts/validate_change_artefacts.py` are absent; follow the phase-3 prompt's
form and report that validator as unavailable. `findings.md` has call/check
receipts but no phase-2a rows to resolve. The latest in-tree handover dated
2026-11-03 was read; live hosted pull-request state and current session ownership
were not read within this runner's worktree/Git-only boundary. This draft edits
only this change's spec and plan; cross-folder correction is phase-4 work.

## Verification

Use offline fixtures. For each new regression, show the named fault is rejected
and the corrected behavior passes; existing string assertions must allow a
producer list without dropping checks on its members. Compare the final
backfill against pre-correction Git metadata, not only the already normalised
working tree. Keep the independent fault fixtures even though the normaliser
and census share a validator. The orchestrator runs the write command only
after the candidate attempt, then repeats the census and final verification.

```sh
.venv/bin/python3 -m ruff check scripts/stage2.py scripts/stage2_research_run.py scripts/stage2_research_snapshot.py scripts/normalise_active_research.py scripts/ci_gates.py tests/test_stage2.py tests/test_stage2_swarm.py tests/test_stage2_research_deep_review.py tests/test_stage2_research_store.py tests/test_explore_provenance.py
.venv/bin/python3 -m ruff format --check scripts/stage2.py scripts/stage2_research_run.py scripts/stage2_research_snapshot.py scripts/normalise_active_research.py scripts/ci_gates.py tests/test_stage2.py tests/test_stage2_swarm.py tests/test_stage2_research_deep_review.py tests/test_stage2_research_store.py tests/test_explore_provenance.py
.venv/bin/python3 -m pytest -q tests/test_stage2.py -k explore
.venv/bin/python3 -m pytest -q tests/test_stage2_swarm.py tests/test_stage2_research_deep_review.py tests/test_stage2_research_store.py tests/test_stage2_research_snapshot.py tests/test_research_handoff.py tests/test_explore_provenance.py
.venv/bin/python3 scripts/normalise_active_research.py
.venv/bin/python3 scripts/normalise_active_research.py --write
.venv/bin/python3 -m pytest -q tests/test_explore_provenance.py
python3 scripts/check_interview_minimums.py --change explore-provenance
python3 scripts/check_research_handoff.py --change explore-provenance
python3 scripts/check_criterion_ledger.py
make verify
```

## Criterion ledger

- 1: tests/test_stage2.py::test_explore_publishes_truthful_research_provenance — Flash or fallback leaves false provenance
- 1: tests/test_stage2_swarm.py::test_swarm_publication_corrects_research_provenance — complete/incomplete swarm publication retains false provenance
- 2: tests/test_stage2.py::test_explore_publishes_truthful_research_provenance — the publication's producer/date is wrong
- 2: tests/test_stage2.py::test_research_publication_preserves_all_producers — repeated publication discards an earlier program/model contribution
- 2: tests/test_stage2_swarm.py::test_swarm_publication_preserves_prior_producers — the swarm overwrites earlier authorship or is attributed to one model
- 3: tests/test_stage2.py::test_explore_resets_review_without_changing_lifecycle — approval survives publication
- 3: tests/test_stage2_swarm.py::test_swarm_publication_corrects_research_provenance — swarm research claims human approval
- 4: tests/test_stage2.py::test_explore_removes_only_opening_skeleton_text — a notice survives or authored quotation disappears
- 4: tests/test_stage2_swarm.py::test_swarm_publication_corrects_research_provenance — opening notices survive swarm publication
- 5: tests/test_stage2_research_deep_review.py::test_research_publication_preserves_unrelated_bytes — unrelated metadata/body bytes or line endings change
- 5: tests/test_explore_provenance.py::test_normaliser_preserves_research_and_is_idempotent — correction changes research or repeats a write
- 5: tests/test_explore_provenance.py::test_normaliser_preserves_unrelated_metadata_bytes — correction rewrites class, lifecycle, owner or unrelated header formatting
- 6: tests/test_stage2_research_deep_review.py::test_research_publication_is_one_atomic_replacement — failed replacement changes bytes or success needs two replacements
- 7: tests/test_explore_provenance.py::test_active_model_research_has_no_false_human_provenance — any active model-written research fails the whole contract
- 7: tests/test_explore_provenance.py::test_normaliser_keeps_all_known_producers — compound model attribution is collapsed or an earlier contributor is lost
- 7: not a test — phase-6 review compares every corrected research header with pre-correction Git attribution and publication evidence, rejecting lost contributors, invented facts, changed findings or archive edits
- 8: tests/test_stage2_research_deep_review.py::test_corrected_skeleton_publication_keeps_swarm_resume — successful seats rerun solely because of corrected metadata
- 8: tests/test_stage2_research_deep_review.py::test_resume_reuses_publication_bytes_and_day — a later day or crash changes prepared publication bytes
- 8: tests/test_stage2_research_deep_review.py::test_producer_history_survives_swarm_resume — retaining historical producer lists changes the private brief hash and reruns successful seats
- 8: tests/test_stage2_research_store.py::test_binding_accepts_only_exact_research_provenance_publication — foreign edits pass or the exact publication/crash state cannot resume
- 9: tests/test_explore_provenance.py::test_normaliser_preserves_research_and_is_idempotent — repeated normalisation changes compliant bytes
- 9: tests/test_explore_provenance.py::test_normaliser_dry_run_and_batch_preparation — default invocation writes or a preparation error leaves a partially corrected batch
- 9: tests/test_explore_provenance.py::test_normaliser_refuses_unknown_historical_metadata — unsupported producer/date evidence is invented
- 10: tests/test_explore_provenance.py::test_census_rejects_incomplete_publication_metadata — any owned field or date violation passes
- 10: tests/test_explore_provenance.py::test_census_requires_publication_and_reads_scalar_spellings — quoted/fenced examples or failed audits count as publication
- 10: tests/test_explore_provenance.py::test_census_names_unreadable_headers — an unreadable header is silently skipped
- 10: tests/test_explore_provenance.py::test_census_reports_undecodable_research — undecodable bytes abort or escape the census
- 10: tests/test_explore_provenance.py::test_census_reports_opening_skeleton_notices — a model-written file retains a generated opening notice
- 10: tests/test_explore_provenance.py::test_active_census_is_enabled — the repository-data census is skipped
- 10: tests/test_explore_provenance.py::test_census_accepts_and_checks_every_producer — a valid list is refused or one invalid/duplicate list member passes

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
