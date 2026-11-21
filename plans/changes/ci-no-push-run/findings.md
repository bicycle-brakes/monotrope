---
title: "Findings — ci-no-push-run"
category: findings
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-dmmy
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — ci-no-push-run

Stage-2 call, 2026-11-21: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1150 files, 5175 commits, 12 rules.

Stage-2 call, 2026-11-21: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1153 files, 5177 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-21

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | MAJOR | SPEC | base | `spec.md`, Non-goals (third bullet); `decisions.md` Q-1 statement and [DETAIL] "Risk named in the spec" | [AMBIGUITY] The spec and its basis disagree about what the maintainer accepted. In decisions.md, the acceptance of "no hosted run tests main" with the queue switched off rests on a mitigation: "the ruleset gate reports a switched-off queue on the next local make verify" (and in [DETAIL], "already reports"). The spec says the opposite: the check accepts strict up-to-date checks instead, so it does not always report a disabled queue. The spec is right: `tests/test_repo_settings.py` reports only when neither the strict rule nor the queue rule is present. The maintainer's quoted answer does not mention the disabled-queue case. Reading A: the acceptance holds without conditions, and nothing is built, as the spec has it. Reading B: the acceptance depended on that report, so a criterion is owed that makes a disabled queue visible even when the strict flag is on. A person has to decide which acceptance stands. | Opus | open | — |
| F-2 | MINOR | SPEC | base | `spec.md`, criterion 7 | [AMBIGUITY] "A `GITHUB_REF` pointing to `main` alone no longer identifies a hosted main-line run" can be read two ways. Reading A: `GITHUB_REF` stops being a signal at all. Reading B: "alone" means `GITHUB_REF=refs/heads/main` still counts when it comes with a push event, for example in a repository that takes the kit and keeps a push trigger (research, "The kit carries the trigger set"). Input that separates them: a detached checkout at `origin/main`, `GITHUB_REF=refs/heads/main`, `GITHUB_EVENT_NAME=push`, and an unclaimed ADR edit. Under A the gate exits 3; under B it uses the first parent and exits 1. The refutation text does not settle it: "silently passes instead of reporting not measured" does not cover an exit 1. That exit 1 is what `tests/test_check_interview_minimums.py:419-424` asserts today. | Opus | open | — |
| F-3 | MAJOR | SPEC | base | `spec.md`, criteria 6–7, with `decisions.md` [DETAIL] (signal `GITHUB_EVENT_NAME == merge_group`) | Hole: the spec does not say whether the merge-group signal applies to every process in the hosted merge-group run or only to the gate measuring the checked-out candidate. The test suite runs inside that run (the `pytest` step of `ci.yml`), and the gate's fixture tests inherit its environment. `run_gate` removes only `GITHUB_REF` (`tests/test_check_interview_minimums.py:151`). If the fixtures are not shielded, every one that expects the merge base or NOT MEASURED will use the first parent and fail, but only in the merge-group run. The DoD's local `make verify` and the pull-request run never set that variable, so nothing the spec names goes red before the decision pull request's own queue run fails. | Opus | open | — |
| F-4 | MINOR | SPEC | base | `spec.md`, criterion 8, refutation | [AMBIGUITY] (a) "The workflow describes the former hosted push as the first-parent run" could mean `docs/WORKFLOW.md`, or `.github/workflows/ci.yml` together with its generator comments in `scripts/ci_gates.py`. (b) It is unclear whether wording that assumes a push run, without saying a push starts verification, is refuted. Examples: `decisions/gates.yaml:18` "a push run is never cancelled"; `docs/WORKFLOW.md:536` "the hosted main-line run", which can be read as the old push or reread as the merge-group run; and the gate's docstrings at `scripts/check_interview_minimums.py:42-46,121-122,129`, which say a detached HEAD uses the merge base. Narrow reading: only a claim that a push starts verification fails, so these lines can stay. Wide reading: every current description that assumes the push run must change. | Opus | open | — |
| F-5 | MINOR | SPEC | base | `spec.md`, criterion 8 | The positive half of the criterion cannot go red. The criterion says the documents "describe the retained events and the merge-group first-parent measurement", but only the negative half has a refuting case. Counter-case: delete "and on pushes to `main`" from `docs/WORKFLOW.md:579` and the push clause from `decisions/gates.yaml:16`, and add nothing about `merge_group`, schedule/dispatch or the merge-group first-parent base. That passes every listed refutation. `merge_group` is missing from that WORKFLOW sentence even today. | Opus | open | — |
| F-6 | MINOR | SPEC | base | `spec.md`, criteria 1–3; `scripts/ci_gates.py:773,822` | Hole: the spec does not decide whether `github.event_name == 'push'` leaves the `if:` conditions of the gates and verify jobs. Criterion 1 covers only the trigger, and criteria 2–3 pass either way. Today `tests/test_ci.py::test_drift_job_runs_on_schedule_and_dispatch_only` requires push to appear in the matrix job's condition, so whoever builds this has to choose. | Opus | open | — |
