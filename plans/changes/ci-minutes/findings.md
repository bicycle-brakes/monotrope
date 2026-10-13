---
title: "Findings — ci-minutes"
category: findings
status: draft
implementation_status: none
date: 2026-10-13
created: 2026-10-13
last_reviewed: 2026-10-13
updated: 2026-10-13
supersedes: null
superseded_by: null
bead: coding-harness-cac
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — ci-minutes

Stage-2 call, 2026-10-13: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Claude Code 2.1.296 refused glm-5.3(-flash) as an unrecognized model before any call (bead coding-harness-6th) · leak check clean over 407 files, 1010 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `.github/workflows/ci.yml` +3 -2
> - `decisions/gates.yaml` +2 -2
> - `docs/WORKFLOW.md` +4 -0
> - `plans/changes/ci-minutes/plan.md` +6 -4
> - `pyproject.toml` +1 -1
> - `ruff.toml` +1 -1
> - `scripts/check_research_currency.py` +1 -1
> - `scripts/ci_gates.py` +6 -1
> - `tests/test_ci.py` +40 -1
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> ........................................................................ [  3%]
> ........................................................................ [  7%]
> ........................................................................ [ 11%]
> ................................s..........s..............F...ss........ [ 15%]
> .........................ss.sssssss..s.......s.......................... [ 19%]
> ........................................................................ [ 22%]
> ........................................................................ [ 26%]
> ........................................................................ [ 30%]
> ........................................................................ [ 34%]
> ........................................................................ [ 38%]
> ........................................................................ [ 41%]
> ......................................................................s. [ 45%]
> ........................................................................ [ 49%]
> ........................................................................ [ 53%]
> ........................................................................ [ 57%]
> ........................................................................ [ 60%]
> ........................................................................ [ 64%]
> ........................................................................ [ 68%]
> ........................................................................ [ 72%]
> ........................................................................ [ 76%]
> ........................................................................ [ 79%]
> ........................................................................ [ 83%]
> ........................................................................ [ 87%]
> ........................................................................ [ 91%]
> ........................................................................ [ 95%]
> ........................................................................ [ 98%]
> ....................                                                     [100%]
> =================================== FAILURES ===================================
> _________________ test_the_mutation_ratchet_only_turns_one_way _________________
>
>     def test_the_mutation_ratchet_only_turns_one_way() -> None:
>         """An entry in the ratchet whose gate has long been covered lies.
>     
>         And an entry for a gate that no longer exists keeps an exception open for
>         something nobody runs any more.
>         """
>         quellen = {p: p.read_text(encoding="utf-8") for p in _testdateien()}
>         bekannt = {g["id"]: g for g in gates()}
>     
>         verwaist = sorted(set(OHNE_MUTATIONSTEST) - set(bekannt))
>         assert not verwaist, f"Exception for a gate that does not exist: {verwaist}"
>     
>         ueberholt = []
>         for gid in OHNE_MUTATIONSTEST:
>             ziel = _pruefling(bekannt[gid])
>             if ziel and any(MUTATIONS_NAMEN.search(t) for p, t in quellen.items() if ziel in t):
>                 ueberholt.append(gid)
> >       assert not ueberholt, f"long since covered, but still in the ratchet: {ueberholt}"
> E       AssertionError: long since covered, but still in the ratchet: ['plans-registry', 'plans-registry-strict']
> E       assert not ['plans-registry', 'plans-registry-strict']
>
> tests/test_ci.py:1885: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_ci.py::test_the_mutation_ratchet_only_turns_one_way - Asser...
> 1 failed, 1875 passed, 16 skipped in 310.68s (0:05:10)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [leerprobe] $ lauf_cmd
> BLOCK (1):
>   - 2 rote(r) Fall/Faelle ohne deklarierten Grund
>       tests.test_ci::test_the_interpreter_floor_is_declared_once
>       tests.test_ci::test_the_mutation_ratchet_only_turns_one_way
>       
>       Nachtragen mit: python3 scripts/kit/probe.py --messen
>
> INFO  (1):
>   - 932 von 970 Faellen tragen in ein fremdes Repo (96 %)
>       mechanismus 83 · bestand 324 Datei(en)
> ── [leerprobe] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 8617 earlier lines left out …]
> templates/handover.md:22:81 error MD013/line-length Line length [Expected: 80; Actual: 200]
> templates/handover.md:48:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> templates/spec.md:21 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/spec.md:39:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> templates/spec.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:17:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:18:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:23:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:24:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:25:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:29:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:38:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:41:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:72:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:74:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:75:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> make: *** [verify] Error 1
> ````

Stage-2 call, 2026-10-13: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 408 files, 1011 commits, 12 rules.

Stage-2 call, 2026-10-13: repair · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Z.ai weekly limit exhausted until 2026-10-14 14:34 CEST (HTTP 429, code 1310), and Claude Code 2.1.296 refuses the GLM names (bead coding-harness-6th) · leak check clean over 408 files, 1011 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/ci-minutes/spec.md` +3 -2
> - `scripts/kit/probe.py` +6 -4
> - `tests/test_ci.py` +10 -0
> - `tools/cloud-env/README.md` +5 -3
> - `tools/cloud-env/setup.sh` +3 -3
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - `plan.md` did not add a measured line below `## Time used`
> ```

Stage-2 call, 2026-10-13: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 408 files, 1012 commits, 12 rules.

Stage-2 call, 2026-10-13: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 408 files, 1013 commits, 12 rules.

Stage-2 call, 2026-10-13: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 408 files, 1014 commits, 12 rules.

## Phase 6 — Codex, 2026-10-13

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | MINOR | SPEC | base | `tests/test_ci.py:781–787` | The schedule test checks only event-name substrings. On `b5de3a5`, appending `\|\| true` to the matrix job’s generated condition and supplying the matching workflow in memory leaves this test, the existing drift/merge-ref/summary checks and `ci-drift` green. That condition runs `gates` on schedule and manual dispatch alongside `drift`, so the promised drift-only behavior lacks an effective regression check. [criterion 5] | Codex | fixed — tests/test_ci.py::test_the_schedule_runs_only_the_drift_job (exact conditions for the matrix, summary and drift jobs, committed and generated; an appended `|| true` was measured to go red) | no |

Phase 6 verdict: codex 01a13596-2046-7a62-a426-31b0958e11db, 2026-10-13
Reviewer session: codex 01a13596-2046-7a62-a426-31b0958e11db — a fresh session reviewed: no phase-2a session was recorded

## Phase 4b — loop rows, released 2026-10-13

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MAJOR | SPEC | base | `tools/cloud-env/setup.sh` line 46, `tools/cloud-env/README.md` lines 17 and 23, and the non-goal in `plans/changes/ci-minutes/spec.md` | The change scopes the cloud-environment script out as installing only the sibling repository's interpreter, and its criterion 8 forbids any other statement that this repository is checked under 3.11. But setup.sh line 46 builds this repository's own `.venv` with `--python 3.11`, and the README calls that venv "what `make venv` builds"; after `requires-python = ">=3.12"` that environment is below the new floor, and `make verify` in it fails the lock check `test_the_environment_matches_the_lock`. Either build that venv with 3.12 or correct the non-goal and the README. | deepseek-v4.1-flash | fixed — tests/test_ci.py::test_the_cloud_environment_builds_the_venv_with_the_floor | no | agree |
| L1-2 | MINOR | MAINT | base | `scripts/kit/probe.py`, the new `REIST_NICHT` entry and the `DECKEL` comment | The interpreter-floor test is declared as `bestand-dieses-repos`, but in the probe's throwaway repository it goes red because `pyproject.toml` is missing; the module's own documented mapping sends a missing file to `braucht-die-vollstaendige-suite`. The comment that raises the cap with "same reason as the other cases" therefore records the wrong cause, so the entry no longer says why the case is red. | deepseek-v4.1-flash | fixed — not a test — the probe entry now reads `braucht-die-vollstaendige-suite` and the DECKEL comment names the missing file | no | agree |
| L2-1 | MINOR | SPEC | repair | plans/changes/ci-minutes/decisions.md (addendum, last [DETAIL]), plans/changes/ci-minutes/plan.md ("Not touched"), plans/changes/ci-minutes/spec.md (Definition of Done) | The change's own records contradict its file list: decisions.md states "`tools/cloud-env/` is not touched" and the plan's "Not touched" section repeats it, yet the change modifies tools/cloud-env/setup.sh (coding-harness venv 3.11 to 3.12, `uv python install 3.11 3.12`) and tools/cloud-env/README.md and pins that very line with the new test `test_the_cloud_environment_builds_the_venv_with_the_floor`. The spec's "Moved in the same pull request" list omits those files and also `scripts/ci_gates.py`, `tests/test_ci.py` and `scripts/kit/probe.py`, and the plan's steps and criterion ledger never mention the cloud-env work or its test (only the Time-used notes a repair happened), so a maintainer checking the Definition of Done "shown by the pull request's file list" cannot match the two. | mimo-v2.6-flash | fixed — not a test — decisions.md, plan.md (Not touched) and spec.md (Definition of Done) now name the cloud-env, ci_gates, test and probe files the change moves | no | agree |
| L2-2 | MINOR | MAINT | repair | tools/cloud-env/setup.sh, coding-harness block (`uv venv --allow-existing --python 3.12 "$R/.venv"`) | `--allow-existing` leaves an already existing `.venv` untouched, so on a cloud snapshot created before this change the coding-harness venv stays on Python 3.11 while tools/cloud-env/README.md now claims it is built on Python 3.12 and pyproject.toml requires `>=3.12`; the following `uv pip install --require-hashes` does not check the venv's interpreter, so the session runs the suite below the declared floor with nothing red and no note in the script or README that an old venv must be rebuilt. | mimo-v2.6-flash | rejected — measured 2026-10-13 with uv: `uv venv --allow-existing --python 3.12` over an existing 3.11 venv leaves `v/bin/python -V` at 3.12.4 and pyvenv.cfg at 3.12.4; the interpreter is switched, not kept |  | disagree — The recorded experiment shows that `uv venv --allow-existing --python 3.12` switches the existing 3.11 environment to 3.12.4; an undeclared interpreter would also fail the lock check. |
| L3-1 | MAJOR | SPEC | fix-r2 | `plans/changes/ci-minutes/spec.md`, Definition of Done (the amendment line "loop rounds 1 and 2: L1-1, L1-2, L2-1") | The Definition of Done credits an amendment of loop round 2 (L2-1), but no round-2 repair stands in the change: `findings.md` ends at the round-2 review line and `plan.md`'s `## Time used` ends with the round-1 repair, so L2-1 and its fix are untraceable and the measured line the runner demands per attempt — the very check that refused an earlier attempt — is missing; either the record or the citation is wrong. | mimo-v2.6-pro | fixed — not a test — plan.md's Time used now records the round-2 repair (orchestrator, text only, no runner call) and the round-3 repairs | no | disagree — Commit `1259efc` contains the round-2 repair. No runner call made it, so no runner audit line was expected; the missing time-log entry does not make the repair untraceable or its citation false. |
| L3-2 | MINOR | MAINT | fix-r1 | `tests/test_ci.py`, `test_the_cloud_environment_builds_the_venv_with_the_floor` | The test cuts the coding-harness block out of `tools/cloud-env/setup.sh` by splitting on the literal `R=/home/user/coding-harness` and on the first `fi` substring anywhere, so any comment or word beginning with "fi" (file, first, find) inside the block truncates it and fails the count with "found []" although the `uv venv` line is unchanged; the parse, not the script, decides what is checked, and the failure names the wrong cause. | mimo-v2.6-pro | fixed — tests/test_ci.py::test_the_cloud_environment_builds_the_venv_with_the_floor (the block now ends at its own `fi` line) | no | agree |
| L3-3 | MINOR | MAINT | base | `tests/test_ci.py:725`, `test_every_declared_interpreter_gets_a_leg` | This test travels with the kit and now rejects the schema-valid interpreter 3.11 with the rationale "no repository of the maintainer targets 3.11": an adopting repository that does target 3.11 gets a red test asserting another maintainer's portfolio, while `scripts/ci_gates.py`'s schema still accepts such a list; unlike the `main` push filter, which the spec's non-goals name as a known portability limit, this second portability limit is recorded nowhere. | mimo-v2.6-pro | fixed — tests/test_ci.py::test_every_declared_interpreter_gets_a_leg (asserts a non-empty list; this repository's 3.12 floor stays pinned by test_one_version_is_the_interpreter_floor, which does not travel) | no | agree |

Rounds run: 3

Stage-2 call, 2026-10-13: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 408 files, 1014 commits, 12 rules.

Stage-2 call, 2026-10-13: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 408 files, 1015 commits, 12 rules.

## Phase 6 — Codex, 2026-10-13

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-2 | MINOR | SPEC | base | `tests/test_ci.py:777–778` | The cancellation test accepts a concurrency group containing `${{ github.run_id }}` because it checks only event/ref substrings. Such a group separates successive runs of the same pull request, preventing cancellation. An in-memory replay on `88e44bf` with the matching generated workflow passes all 15 targeted CI tests, schema validation and `ci-drift`. [criterion 4] | Codex | fixed — tests/test_ci.py::test_only_pull_request_runs_cancel_superseded_runs (the group is compared exactly; a group with `${{ github.run_id }}` was measured to go red) | no |
| F-3 | MINOR | SPEC | base | `tests/test_ci.py:724–727,753–757` | Declaring `tools.python: ["3.12", "3.11"]` and regenerating the workflow adds a prohibited 3.11 leg while preserving the first-entry floor checks. An in-memory replay on `88e44bf` passes all 15 targeted CI tests, schema validation and `ci-drift`; no test rejects the additional 3.11 entry. [criterion 2] | Codex | fixed — tests/test_ci.py::test_one_version_is_the_interpreter_floor (the floor is the oldest declared version, not the first; `["3.12", "3.11"]` was measured to go red) | no |
| F-4 | MINOR | SPEC | base | `decisions/gates.yaml:16` | The header documents which events run each job but omits that newer pull-request runs cancel superseded runs. This cancellation policy must appear in the gate-file header as well as the workflow guide. [criterion 8] | Codex | fixed — not a test — the `job` key in the header of decisions/gates.yaml now says a newer pull-request run cancels the older one and a push run is never cancelled | no |

Phase 6 verdict: codex 01a135a5-8323-7913-bafa-07b76c72cb09, 2026-10-13
Reviewer session: codex 01a135a5-8323-7913-bafa-07b76c72cb09 — a fresh session reviewed: no phase-2a session was recorded
