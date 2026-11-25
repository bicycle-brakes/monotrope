---
title: "Research — cheap-checks-admission"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.13
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-25", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
class: bounded
neighbours: []
---

# cheap checks admission — Research

## Topic (bead coding-harness-bxxt.13, copied by the orchestrator 2026-11-25)

Class: bounded.

Why: scripts/stage2.py:6578 PYTEST uses -n auto; cheap_checks (8529) runs it
at 8599-8606, both callers outside the admission (9252-9275 strip the lock
env; 9440-9443 'without an admission'); the worker cap targeted_pytest_env
(8996-9034) applies only at 9163. When a touched path appears or vanishes
(8955) the targeted run selects leerprobe (8968; ~200 s) through run_gates,
documented as outside the admission (9038). On an 8 GB machine this bypasses
the two-slot limit and the memory floor. What: cap cheap-check workers like
targeted runs, and run leerprobe in targeted runs under the admission.
Related: coding-harness-9bv1 (ENV_ALLOW drops
PYTEST_XDIST_AUTO_NUM_WORKERS), coding-harness-bxxt.11.

Checked 2026-11-24 at origin/main 18a13d3d by read-only subagents (session
claude-mp, night run 2026-11-24-a), from an external verify-speed analysis.



PARENT
↑ ○ coding-harness-bxxt: (EPIC) Verify speed and machine load P1

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-25: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM 5.3 Flash via Z.ai: weekly limit at 100 % until 2026-11-29 (bead coding-harness-b5pu) · leak check clean over 1202 files, 5764 commits, 12 rules.

## Runner exploration — 2026-11-25

Research for `cheap-checks-admission`, ready to append to `plans/changes/cheap-checks-admission/research.md`. I read only the repository, with Grep, Glob and Read; I did not run any command or edit a file.

## What exists today

**Pytest worker count is fixed in one constant.** `scripts/stage2.py`, `PYTEST` (line 6578), is `(".venv/bin/python3", "-m", "pytest", "-q", "-n", "auto")`. Its uses are in `cheap_checks` (`scripts/stage2.py`, defined at line 8529, the pytest run at about line 8600) and in the targeted run (`scripts/stage2.py`, around line 9161). `-n auto` lets xdist choose the worker count itself.

**The targeted run caps workers; the cheap checks do not.** `targeted_pytest_env` (`scripts/stage2.py`, line 8996) sets `PYTEST_XDIST_AUTO_NUM_WORKERS` from `worker_default()` when the caller has not set it (lines 9007 to 9033). The targeted run passes that environment to pytest (`scripts/stage2.py`, around line 9163). `cheap_checks` does not call `targeted_pytest_env`. I found no other reference to `PYTEST_XDIST_AUTO_NUM_WORKERS` in `scripts/stage2.py` besides those lines.

**The worker rule lives in `scripts/verify_run.py`.** `worker_default()` (line 342) takes half the logical cores and the memory in 2-GiB steps, the smaller of the two. Its docstring (lines 325 to 332) says the full check and the targeted check both size through this rule, each reading the machine its own way. `verify_run.py` lines 717 to 722 apply it to `PYTEST_XDIST_AUTO_NUM_WORKERS` when the variable is empty. `scripts/verify_duration.py` line 203 reads the same variable for the duration history.

**Both `cheap_checks` callers run outside the admission.**
- In the targeted path, `scripts/stage2.py` lines 9251 to 9252 strip `verify_lock.LOCK_ENV` and `verify_lock.TOKEN_ENV` from the environment before anything is started. The comment reads "Nothing a targeted run starts carries or claims the verify admission." Line 9275 calls `cheap_checks` on that environment. I did not read the name of the enclosing function.
- A second caller, `scripts/stage2.py` around line 9441, passes the verify environment with a comment (line 9440) reading "without an admission: none is held yet."

**Leerprobe is selected by the targeted path.** In `targeted_selection` (`scripts/stage2.py`, line 8862), the condition at line 8968 adds the gate `leerprobe` whenever the touched paths change membership: `(membership and gate["id"] == "leerprobe")`. Membership is computed at line 8955 as a path that appeared or vanished relative to `before`. The gate is added to the list returned at line 8972, and `run_gates` (`scripts/stage2.py`, line 9037) runs the chosen gates (called at line 9172). `run_gates` is called without an admission in this path, as the targeted code's comments say.

**The gate list marks leerprobe as minutes.** `decisions/gates.yaml` declares `leerprobe` with `cost: minutes` and `command: python3 scripts/kit/probe.py --strict`. It also declares `pytest` with `cost: minutes`, `command: python3 -m pytest tests/ -q -n auto`. The same file's header (line 60) documents the optional `needs_admission` boolean. `scripts/ci_gates.py` validates it (line 416), records it (line 488), and derives protection from it (line 501: a gate is cheap only when `cost == "seconds"` and `needs_admission` is not true).

**The two-phase scheduler is already in `verify_run.py`.** The module docstring (lines 17 and 24) says unprotected gates execute first, and that protected work is `minutes` gates plus `seconds` gates marked `needs_admission: true`, entering one admission. The test file `tests/test_verify_before_admission.py` proves this: `test_all_cheap_failures_finish_without_queueing` (line 361), `test_only_protected_work_enters_one_admission` (line 394), and `test_seconds_only_jobs_never_request_admission` (line 433). Those proofs test the scheduler in `verify_run.py`, not the targeted path in `stage2.py`.

**`ENV_ALLOW` does not carry the worker variable.** `scripts/stage2.py` line 458 defines `ENV_ALLOW` as the environment a foreign program receives. The tuple's first entries are PATH, HOME, USER, LOGNAME, SHELL, TMPDIR, LANG, LC_ALL, LC_CTYPE, TERM and TZ. `PYTEST_XDIST_AUTO_NUM_WORKERS` is not in the tuple. I read only its first 14 lines.

**The earlier change left its spec as a draft.** `plans/changes/verify-cheap-before-admission/` holds `research.md`, `spec.md` and `seconds-gate-audit.md`. Its `spec.md` front matter reads `implementation_status: none`, yet `scripts/verify_run.py` already implements the two-phase order (see above). Which of those documents is current is not settled by any artefact I read.

**Neighbours on disk.** `plans/changes/verify-cheap-before-admission/` (bead coding-harness-bxxt.6) is the closest; `plans/changes/verify-two-slots/` and `plans/changes/verify-cheap-first/` (the archived `plans/changes/archive/2026-11-16-verify-cheap-first/`) are also related. The `plans/changes/verify-step-limit/` change is named in the earlier research.

## Where it lives

- `scripts/stage2.py`: `PYTEST`, `ENV_ALLOW`, `cheap_checks`, `targeted_selection`, `targeted_pytest_env`, `run_gates`, and the targeted-path admission strip.
- `scripts/verify_run.py`: `worker_default`, the worker rule, and the two-phase scheduler.
- `scripts/verify_duration.py`: the worker variable as read for history.
- `scripts/ci_gates.py`: `needs_admission` validation, the record, and the cheap-gate predicate.
- `decisions/gates.yaml`: the `pytest` and `leerprobe` declarations and the `needs_admission` header.
- `tests/test_verify_before_admission.py`: the scheduler proofs.

## What is unclear

- **Which code path a targeted run actually takes.** The topic states that the targeted run selects leerprobe under `run_gates`, outside the admission. I confirmed the selection and the call. I did not read the body of `run_gates`, so I cannot say whether it refuses or waits on admission, or whether it passes the worker variable.
- **Whether `cheap_checks` inherits the worker cap.** I read that `cheap_checks` runs `[*PYTEST, *tests]` (line 8600) with no environment argument at that line. I did not read its whole body, so I did not confirm which environment it receives.
- **Whether `ENV_ALLOW` is the only filter.** `ENV_ALLOW` is for foreign programs. I did not verify that the cheap-check pytest run goes through it. The claim that `coding-harness-9bv1` drops the variable therefore stays unverified here.
- **Current status of the scheduler.** The spec of `verify-cheap-before-admission` says none is implemented; the scheduler code and its proofs are present. Which artefact is current is open.
- **The line numbers in the topic.** Most match the symbols above when I checked them. I did not check every number, and this research cites symbols rather than lines.
- **Tracker state of `coding-harness-bxxt.13` and `.11`.** Not read; no rendered copy is committed and the reader was not run.
- **`docs/research/2026-11-09-make-verify-long-term.md`.** Not read in this pass.

## Which files a change would have to touch

`scripts/stage2.py` (`cheap_checks`, `targeted_pytest_env`, `targeted_selection`, `run_gates`, and the admission strip in the targeted path); `scripts/verify_run.py` (the worker rule and, for leerprobe, the scheduler's protected set); `decisions/gates.yaml` (the leerprobe declaration; a held path, orchestrator-owned); `scripts/ci_gates.py` only if the protected set is derived differently; `tests/test_verify_before_admission.py` and `tests/test_stage2.py` for the targeted path; `docs/WORKFLOW.md` and `docs/testing.md` for the timing text. Whether `scripts/kit/manifest.yaml` needs a rule depends on whether a new helper is added.
