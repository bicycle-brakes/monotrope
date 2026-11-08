---
title: "Plan — outcome-test"
status: draft
implementation_status: partial
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-08
supersedes: null
superseded_by: null
bead: coding-harness-3nm5
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, measurement, outcome-test]
---

# Plan — outcome-test

```text
For you:     Eight fixed questions show how a fresh session answers current harness rules before startup conventions change.
Done when:   Offline tests hold the ten criteria, one real baseline is recorded with its commit, and make verify is green.
Appetite:    2 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Nightly runs, CI gates, new model launchers or changes to routing and startup hooks.
Pre-mortem:  suppose it failed: most likely because copied expected answers hide a changed rule.
Starts unless you say stop.
```

The measurement scope is decided: a new Claude Code session with its usual
start context and read access to the repository (`decisions.md#Q-2`,
maintainer 2026-11-08); the spec records it under "Decided scope".

## Files and steps

1. Create `tests/test_outcome_test.py`: use temporary Git repositories and
   injected doctrine/code to demonstrate missing behaviour first and exercise
   the ledger without models, real hooks or the shared tracker.
2. Create `scripts/outcome_test_questions.json`: store schema version 1 and
   the eight identifiers, texts, answer types and named source resolvers below;
   store no expected values or solution excerpts.
3. Create `scripts/outcome_test.py`: implement `questions` and `record` with
   the snapshot, source-reading, scoring and append contract below.
4. Change `docs/WORKFLOW.md`: document the chosen measurement scope, invocation,
   baseline and pre-change procedure, typed-answer limits and history fields;
   distinguish incorrect answers from an unmeasured run.
5. After the accepted implementation attempt, the orchestrator administers
   one real baseline in a separate fresh session under the answered scope;
   `record` creates `docs/research/outcome-test-results.jsonl` from that run.
   Record its actual score, not a requirement for eight correct answers.
6. Update `plans/changes/outcome-test/plan.md` with landed test references and
   runner-measured time; the runner maintains
   `plans/changes/outcome-test/findings.md` and regenerates `plans/INDEX.md`.

No file is deleted. Keep `decisions.md` unchanged until an actual maintainer
answer is available; the orchestrator owns that record and subsequent spec
revision. No design, ADR or held-path bootstrap edit is due. In particular,
do not edit `AGENTS.md`, `prompts/`, `templates/`, `.github/`, `decisions/`,
`provenance.yaml`, `model-endpoints.yaml`, harness configuration, the tracker,
existing runner modules, verification admission or startup hooks.

## Implementation contract

- Repository root is the script's own root. `questions` prints one JSON
  questionnaire containing a UUID run identifier, UTC preparation time, full
  `HEAD`, question-set SHA-256, relevant source-file SHA-256 values, eight
  question texts and answer shapes, but no expected values. Local Git calls
  are read-only argument lists with finite timeouts. Refuse dirty measured
  source/question/tool files, so a commit and fingerprints describe the same
  measurement. An uncommitted result history alone must not prevent another run.
- `record --questionnaire FILE --answers FILE --harness TEXT --model TEXT
  --context TEXT --access TEXT --fresh-session --purpose baseline|pre-change`
  reads the exported questionnaire and submitted JSON answer object. A
  pre-change run also requires `--target AGENTS.md|handover-convention`.
  These are data, never command text. All four context labels are required;
  they must follow the scope settled in the spec. `--fresh-session` records
  the administrator's attestation, not proof of a context reset.
- The administrator exports the questionnaire to a temporary file, supplies
  only its question/answer instructions to the separately started session,
  saves that session's answer object temporarily, and records it. The script
  starts no session. A foreign session must use the existing `stage2.py`
  launch/leak-check path; no direct CLI/API shortcut is added.

| ID | Question asks for | Live source and reading rule |
|---|---|---|
| repair-model | Primary repair model's exact identifier | `docs/WORKFLOW.md`, “The routing”, the `Repair after 4b and 6` row's model cell |
| repair-fallback | Fallback model's exact name after two failed checks | The same row's explicit fallback clause, excluding effort text |
| verify-floor | Default memory floor as a number in percent, without an environment override | `scripts/verify_lock.py`, literal assignment `DEFAULT_MEMORY_FLOOR` |
| verify-floor-override | Environment variable overriding that floor | The same Python file, literal assignment `FLOOR_ENV` |
| run-plans | Repository-relative directory containing dated run plans | `docs/orchestration.md`, dated run-plan links under “What a lane is”; resolve links relative to that file and require one common directory |
| handovers | Repository-relative session-handover directory | `docs/WORKFLOW.md`, “The eighth movement”, the handover table's date/name path |
| tracker-command | Repository-relative tracker executable | `AGENTS.md`, the `Use ... never bare ...` house rule |
| instructions | Filename that would replace the repository instructions | `AGENTS.md`, its opening sole-instruction-file declaration; require that declaration and read the filename explicitly said to silently replace it |

- AST-read the two Python literals without importing or executing their
  module. Prose readers require one unambiguous supported declaration in
  the specified section; absent, conflicting or unrecognised declarations
  are `not read`. Do not read the historical ADR-answer YAML as model routing.
  Keep today's literal answers out of the question file and runtime defaults.
- Re-read all sources and derive all expected values during recording. Check
  `HEAD`, question fingerprint and source fingerprints against the export,
  and recheck before append; refuse a stale snapshot. Never grade submitted
  expectations or use stored questionnaire metadata as the answer key.
- Require a JSON object keyed by question ID; reject malformed JSON, duplicate
  keys, unknown IDs and a malformed questionnaire with exit 3, no append.
  Missing, blank or wrong-type answers are incorrect with the denominator
  still eight. String answers match case-sensitively after outer whitespace;
  directory answers may omit a trailing slash. Numeric answers must be finite
  JSON numbers equal to the live floor; booleans are not numbers. No substring,
  synonym, prose, partial-credit or model-based grading.
- Append schema version, run ID, preparation/recording UTC times, full commit,
  question and source hashes, the four session labels and freshness
  attestation, purpose/target, eight ID/verdict pairs and `correct`/`total`
  counts. Repository history contains neither submitted answer texts nor
  expected values or source excerpts (`decisions.md#Q-3`, maintainer,
  2026-11-08). Retain submitted answers only in the external user state
  directory with private file permissions; refuse a state directory inside
  the repository.
  Summary exit codes: 0 = eight correct, 1 = measured with incorrect answers,
  3 = not measured/recording failed. Both measured outcomes append one record.
- The only repository destination is
  `docs/research/outcome-test-results.jsonl`; the external answer archive is
  the second persistent destination. Validate the outgoing record with the
  history reader's validator before retaining answers or appending. Validate
  existing rows and refuse malformed/unsupported history or duplicate run IDs
  before writing. Serialize
  appends under a lock on the real regular result file; reject symlinks in its
  path. Save the original end position and roll back a failed append while
  holding that lock; never rewrite older lines or claim crash-proof storage.
  Write no scratch files or bytecode in the repository. Source failures and
  output failures produce bounded diagnostics without raw unrelated file text.
- The orchestrator runs the baseline after the tool/question/source files
  have an accepted commit, then includes its result in the PR. A before-change
  run measures the old source commit, before the proposed instruction or
  handover-convention edit; later comparisons require the same question set
  and session scope. No automated comparison or change-detection hook is built.

## Criterion ledger

- 1: tests/test_outcome_test.py::test_question_set_has_eight_fixed_topics — a source-value edit alters IDs or a topic is missing
- 2: tests/test_outcome_test.py::test_expected_answers_follow_live_sources — changed source values leave old answers correct or code import runs
- 3: tests/test_outcome_test.py::test_questionnaire_contains_no_answer_key — derived-value sentinels enter subject material
- 4: tests/test_outcome_test.py::test_session_metadata_and_fresh_attestation_are_required — an anonymous or unattested run is recorded
- 4: not a test — phase-6 review reads the baseline's session provenance against the answered scope; a reset cannot be proved from metadata alone
- 5: tests/test_outcome_test.py::test_grading_is_exact_and_keeps_denominator_eight — omitted answers, wrong types or contradictory prose earn points or shrink the total
- 6: tests/test_outcome_test.py::test_unread_or_changed_evidence_prevents_recording — missing, conflicting or changed sources produce a score or append
- 7: tests/test_outcome_test.py::test_measured_runs_append_one_dated_commit_bound_line — metadata or verdicts are missing, earlier bytes change or expected values are stored
- 8: tests/test_outcome_test.py::test_bad_history_and_append_failure_preserve_old_records — invalid history, duplicate IDs or failed writes appear successful or destroy earlier bytes
- 9: not a test — the orchestrator records an actual fresh-session baseline at an accepted commit; phase-6 review checks it and both documented pre-change triggers
- 10: tests/test_outcome_test.py::test_tool_only_writes_explicit_history — a model, tracker, Git mutation or substituted output path is used

## Verification

```sh
.venv/bin/python -m pytest tests/test_outcome_test.py -q
python3 scripts/check_interview_minimums.py --change outcome-test
python3 scripts/check_criterion_ledger.py
python3 scripts/check_research_handoff.py --change outcome-test
make verify
```

Use fixtures for every parser, changed/ambiguous declarations, snapshot drift,
grading errors and failed appends. Never run a real model in the test suite.
The runner owns full verification, derived metadata and the commit.
`scripts/validate_change_artefacts.py` and a separate plan template do not
exist at input commit `86a1d919`; do not claim that absent validator passed.
Use `templates/spec.md` and the phase-3 prompt's card/ledger form.

## Explore route

Research records Stage-2 explore on 2026-11-06: route `flash`, endpoint
`glm-coding-plan`, model `glm-5.3-flash`. No Stage-1 fallback is recorded.
The class is `bounded` as recorded in the maintainer interview; there is no
complete `research-swarm/v2` run and therefore no swarm handoff to invent.

## Runner route — 2026-11-06

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

2026-11-06 16:19:48–16:56:45 UTC, 2217 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-06 16:56:54–17:16:09 UTC, 1155 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-06 17:16:22–17:39:27 UTC, 1385 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-08 00:50:05–01:37:24 UTC, 2839 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-08 01:56:56–05:28:36 UTC, 12699 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-08 13:24:08–18:22:14 UTC, 17886 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-08 18:45:00–20:52:37 UTC, 7657 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
