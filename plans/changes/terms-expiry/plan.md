---
title: "Plan — terms-expiry"
status: draft
implementation_status: none
date: 2026-10-26
last_reviewed: 2026-10-26
updated: 2026-10-27
supersedes: null
superseded_by: null
bead: coding-harness-abra
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "GLM 5.3, 2026-10-26"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, model-terms, stage-2]
---

# Plan — terms-expiry

```text
For you:     Paid Go models stop being admitted after their terms reading expires, with model-and-date warnings from seven days before expiry.
Done when:   Deterministic tests hold criteria 1–10, both DeepSeek entries expire on 2026-10-31, the renewal procedure is documented, and make verify is green.
Appetite:    4 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Automatic renewal, background monitoring, new model permissions, other endpoint families or rebuilding saved review runs.
Pre-mortem:  suppose it failed: most likely because a saved selection bypasses the current date check before a later paid call.
Starts unless you say stop.
```

Implements `spec.md` and `design.md` at baseline `97980181`, inspected
2026-10-26. This draft changes no implementation. Explore was written by the
orchestrating Claude Code session (Opus 5.5); `research.md` records no
Stage-1 fallback route to carry forward. No `templates/plan.md` exists;
this follows the phase-3 card, ledger and time-section form.

## Files and steps

1. `tests/test_stage2_terms_expiry.py` (new) — add the ledger's regressions,
   using synthetic processes and the existing `World`/availability helpers;
   control only the terms UTC date seam. Cover missing/empty/type-invalid
   dates (including YAML-native dates), malformed strings, timestamps,
   impossible dates and leap days; seven/eight/one/zero/minus-one day
   boundaries; UTC/local disagreement; preparation, legacy and saved loops;
   first-call, retry, replacement and receipt expiry; warning persistence
   through release; migration and preservation of prior admission guards.
   For the midnight case prepare at 23:59 UTC on expiry, consume within 900
   seconds on the next day, and prove no expired paid call reaches the stub.
   Snapshot history, consumed stages and round count must survive refusal.
   Also cross midnight after the parent's batch validation; tool-free paid
   probes must still be checked as paid calls.
2. `scripts/stage2.py` — add a small UTC-date seam for terms and a strict
   `valid_until` parser reusing `DATE_ONLY`/calendar validation. Extend
   `terms_problem` without changing its return contract or existing checks;
   absent/malformed/expired dates return model-specific reasons. Keep
   expiry authoritative over prose and never infer/renew dates at runtime.
   Use the same assessment in a deterministic warning helper over declared
   readings, including otherwise skipped records. Print current warnings
   on each terms-evaluating `review_loop`, legacy or resumed, before model
   calls; add them to written round notes, including free rounds. Keep
   `declaration_problem`, preflight and per-member/retry/replacement checks
   binding so a saved member may refuse the round without changing history.
   Recheck expiry immediately before paid reviewer launch, after earlier
   parent/batch validation. Do not infer admission class from `free=True`:
   paid availability probes use it only to disable tools. Preserve the
   discovered free exception and existing leak-refusal propagation.
3. `scripts/stage2_availability.py` — evaluate/print warnings during
   preparation, filter expired candidates before probing through the shared
   admission check, store warnings in optional
   `state["availability"]["terms_warnings"]` and render them in `report`.
   Read older receipts with no warning list. Recheck current admission at
   dispatch even if receipt freshness and bindings still pass. Preserve
   existing acknowledgment, digest, age, retry, leak and no-empty-round rules.
4. `tests/test_stage2.py` — update `pin_entry`, `pin_the_ladder` and direct
   positive terms records with explicit synthetic expiry dates; pin the
   terms-only clock where necessary so existing tests never age into skips
   or mask retention/training/date failures behind a missing expiry.
5. `tests/test_stage2_availability.py` — adapt clock-controlled preparation
   fixtures to the terms date seam; keep receipt-age and reachability tests
   independent of today's calendar date.
6. `tests/test_stage2_session.py` — date `World.declare_go` fixtures and add
   the ledger's interactive regression proving an expired Go declaration
   starts no terminal/transport; existing declaration and leak tests stand.
7. `model-endpoints.yaml` — done by the orchestrator by hand before phase 4
   (the runner holds this file): every Go `modelle_terms` record carries a
   quoted `valid_until` (non-DeepSeek: `gelesen` + 30 days, so 2026-11-06,
   2026-11-16 or 2026-11-21); both DeepSeek records carry `gelesen:
   "2026-10-25"`, `valid_until: "2026-10-31"` and the monthly-agreement
   qualification. The implementation must not edit this file; tests that need
   other dates use synthetic declarations.
8. `docs/WORKFLOW.md` — document required expiry, inclusive UTC cutoff,
   seven-day warnings, refusal of saved expired members, the source-date or
   reading-plus-30-day rule, and sourced renewal through a maintainer-merged
   decision PR; distinguish declared dates from automatic extensions.
9. `docs/adr/0022-paid-model-terms-expire.md` — not edited in phase 4 (a
   human-decided path the runner refuses); a divergence between it and the
   implementation is reported in `findings.md` for the orchestrator to carry
   into the decision pull request by hand.
10. `plans/changes/terms-expiry/plan.md` — mark ledger tests written as they
    land and leave measured phase-4 time to the runner below.
11. `plans/changes/terms-expiry/findings.md` — retain existing runner evidence
    and later review rows; record validation evidence without inventing a
    reviewer verdict or maintainer answer.
12. `plans/INDEX.md` — regenerate through `scripts/plans_registry.py --index`
    during runner preparation; the drafting call does not edit it.

No file is deleted. `spec.md`, `design.md` and the research addendum are
draft inputs, not permission to change criteria during implementation.

## Verification

Before verification in a fresh worktree, the orchestrator sets up the local
toolchain once, as required by `AGENTS.md` and `tools/pi/README.md`:

```sh
make venv
bash tools/pi/install.sh
tools/pi/pi --version
```

The version must match `tools/pi/package.json`. The first draft attempt's
2026-10-26 verification failed because the pinned Pi was not installed;
changing these artifacts cannot repair that prerequisite. The drafting
call leaves installation to the orchestrator and never weakens or skips
the real Pi contract tests to obtain a green run.

Show new behavioral regressions red against the baseline runner, then green
with the fix; migration assertions run after the declaration update. Use
synthetic provider processes only. The full suite checks fixture compatibility.

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2_terms_expiry.py tests/test_stage2_session.py tests/test_stage2_availability.py tests/test_stage2.py
.venv/bin/python3 scripts/check_interview_minimums.py --change terms-expiry
.venv/bin/python3 scripts/check_criterion_ledger.py
.venv/bin/python3 scripts/plans_registry.py --index
make verify
```

The runner owns derived-file preparation, full verification and the commit.
`scripts/validate_change_artefacts.py` is absent at the inspected baseline;
do not add it or claim its requested `--check` passed. The registry gate
needs tracker access outside this drafting call's allowed read scope; leave
it to the runner. A feature's ADR answer remains owed to the maintainer;
the draft runner's existing one-change tolerance is not an answer or a
release exemption, and the drafting agent must not create an answer file.

## Criterion ledger

- 1: tests/test_stage2_terms_expiry.py::test_paid_terms_require_a_usable_expiry — a missing or unusable date admits a paid model
- 2: tests/test_stage2_terms_expiry.py::test_expiry_is_inclusive_on_the_utc_day — admission uses the local date or the wrong side of midnight
- 3: tests/test_stage2_terms_expiry.py::test_expiry_skips_name_model_and_reason — preparation or review hides the model, reason or expired date
- 4: tests/test_stage2_terms_expiry.py::test_expiry_warning_window_on_preparation_and_review — warning boundaries or fresh, legacy and resumed display differ
- 4: tests/test_stage2_terms_expiry.py::test_every_paid_dispatch_rechecks_terms_at_one_point — a paid send bypasses the shared terms guard or research preparation omits visible and durable warnings
- 5: tests/test_stage2_terms_expiry.py::test_saved_admission_cannot_authorize_an_expired_call — a fresh receipt or saved round dispatches an expired member or alters prior history
- 5: tests/test_stage2_terms_expiry.py::test_paid_retries_and_replacements_recheck_expiry — a probe retry, compatibility probe, replacement or malformed-answer retry bypasses the date guard
- 5: tests/test_stage2_session.py::test_an_expired_go_model_starts_no_interactive_session — interactive launch starts a terminal or transport after expiry
- 5: tests/test_stage2_session.py::test_go_session_rechecks_terms_after_command_construction — terms expire after command construction but the interactive transport still starts
- 6: tests/test_stage2_terms_expiry.py::test_non_deepseek_records_receive_reading_plus_thirty_days — a record is missed, has the wrong deadline or a fabricated re-read
- 7: tests/test_stage2_terms_expiry.py::test_both_deepseek_records_use_the_documented_expiry — either record lacks the October 25 reading, October 31 deadline or retention qualification
- 8: not a test — phase-6 review reads docs/WORKFLOW.md and ADR 0022 against the renewal decision; red if source/date evidence or maintainer merge is optional
- 8: tests/test_stage2_terms_expiry.py::test_terms_evaluation_never_renews_the_declaration — preparation, review or admission changes endpoint-file bytes
- 9: tests/test_stage2_terms_expiry.py::test_expiry_preserves_prior_admission_guards — future expiry overrides a skip, unread/training-enabled terms or empty-selection refusal
- 9: tests/test_stage2.py::test_free_class_admission_is_bound_to_discovery_and_purpose — the free exception broadens beyond discovery and its purpose
- 9: tests/test_stage2.py::test_each_call_runs_its_own_leak_check — a later call bypasses the leak scan
- 10: tests/test_stage2_terms_expiry.py::test_expiry_warnings_survive_receipt_round_and_release — model/date warning evidence disappears after preparation or release

## Not touched

No edits to `scripts/stage2_session.py` are planned: it inherits the shared
declaration guard. No historical ADR, new model id, wire-API skip, cost value,
credential, leak rule, free discovery rule, restart/recovery policy,
`decisions/answers/`, `decisions/gates.yaml`, `provenance.yaml` or kit behavior
changes. No extra live source fetch is claimed; use the recorded DeepSeek
re-read. No tracker write, commit, push or repository-changing git command
belongs to this drafting call.

## Runner route — 2026-10-26

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-10-27

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-10-26 17:12:13–18:10:46 UTC, 3512 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-10-26 18:10:52–18:42:36 UTC, 1904 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-10-26 18:42:43–18:48:51 UTC, 368 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · accepted · measured by the runner
2026-10-26 21:51:34–22:19:05 UTC, 1652 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-10-27 00:12:38–00:35:56 UTC, 1398 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-10-27 00:36:02–01:00:06 UTC, 1444 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-10-27 01:00:12–01:09:51 UTC, 580 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-10-27 07:07:33–07:31:57 UTC, 1464 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-10-27 07:32:03–07:51:32 UTC, 1169 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · accepted · measured by the runner
2026-10-27 09:19:18–09:51:26 UTC, 1928 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-10-27 09:52:21–10:33:46 UTC, 2485 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · accepted · measured by the runner
2026-10-27 11:02:56–11:35:25 UTC, 1949 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
