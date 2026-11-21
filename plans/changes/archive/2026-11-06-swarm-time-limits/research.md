---
title: "Research — swarm-time-limits"
status: accepted
implementation_status: done
date: 2026-11-04
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-ht1b
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm, version: "glm-5.3-flash, 2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# swarm time limits — Research

Stage-2 call, 2026-11-04: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 873 files, 3233 commits, 12 rules.

## Runner exploration — 2026-11-04

## What exists today

The repository runs two swarm systems with two independent time-limit mechanisms, one set of bounded runner-owned steps, and one class of model calls with **no** time limit at all.

**1 · The review-loop swarm (phase 4b) — one round deadline.** The constant `REVIEWER_MINUTES = 45` (`scripts/stage2.py:252`, comment: raised from 30 by the maintainer on 2026-10-24, code citation "spec, criterion 15") bounds a whole round: before the swarm starts, one deadline is set as `time.monotonic() + REVIEWER_MINUTES * 60` (`scripts/stage2.py:8376`), and it covers members, the malformed-answer retry (`scripts/stage2.py:8387-8390`, `8409`) and every replacement (`scripts/stage2.py:8431-8466`). Doctrine: "One deadline of `REVIEWER_MINUTES` covers the round's members and every replacement (R-8)" (`docs/WORKFLOW.md:1429`). A late replacement gets only what is left, via `remaining(deadline)` (`scripts/stage2.py:2635-2645`); an expired deadline raises `NotStarted("the round time limit expired; no further reviewer starts")` (`scripts/stage2.py:547`, `2645`) — DL-B-10 — and every stop names the limit and the seconds actually granted, not "45 minutes" — DL-B-14 (`plans/changes/review-loop-deep-b/spec.md:79`, limit sentence in `run_reviewer` at `scripts/stage2.py:2740-2745`). R-8's origin: the 2026-10-20 runner review found each Flash replacement running with its own 30 minutes, one Flash round ≈ 2 hours (`docs/journal/handover/2026-10-20-review-swarm-runner-review.md:152-156`). One documented exception: when every free member fails with a rate-limit/unavailability error, the Flash swarm takes the round in the same call with its own deadline, so one call can take two round limits (`docs/WORKFLOW.md:1421-1425`; `plans/changes/free-member-rate-limit/spec.md:60`; bead `coding-harness-pj98` named there).

Enforcement is by process group: `launch(..., timeout=, deadline=)` (`scripts/stage2.py:895-978`) starts a timed child with `start_new_session=True`, registers it in `_LIVE_GROUPS`, kills the whole group on timeout and raises `StepTimedOut` naming the limit (`scripts/stage2.py:976-978`); the drain after a kill is `KILL_DRAIN_SECONDS = 5` (`scripts/stage2.py:838`); an interrupted runner kills every live group (`kill_live`, `scripts/stage2.py:841-848`, handlers at `8778-8791`). A reviewer that ran into its limit is recorded as "its whole process group was killed (R-20)" (`scripts/stage2.py:568`).

**2 · The research swarm (phase 1, ADR 0020) — per-stage allowances inside one run deadline.** `MINUTES = {"finders": 10.0, "merge": 10.0, "sentence": 5.0, "topics": 10.0, "judge": 15.0}` and `RUN_MINUTES = 150.0` (`scripts/stage2_research_run.py:66-67`); the run deadline is `began + RUN_MINUTES * 60` (property `deadline`, `scripts/stage2_research_run.py:328-330`; `CLOCK = time.monotonic` injectable at `:54`). Each pre-judge stage passes `reserve=MINUTES["judge"] * 60.0` (`scripts/stage2_research_run.py:931, 967, 991, 1095`) — doctrine: "the judge keeps a reserved 15 minutes inside a 150-minute run — with no retry and no debate" (`docs/WORKFLOW.md:982-983`). The dispatcher (`scripts/stage2_research_dispatch.py`, docstring lines 1-7: "owns queueing, deadlines, timeout, cancellation and reaping") computes each slot's allowance as `min(role_allowance, deadline − reserve − now)` (`:250-251`), SIGTERMs and then SIGKILLs a slot over its allowance as a group, keeping its output (`_stop_and_reap` `:100-122`, `supervise` `:259-291`, `grace=2.0`), marks late slots `not-started-deadline` (`:220-222`, `:247-249`), and knows exactly six outcomes `ok | failed | timed-out | cancelled | not-started-deadline | refused` (`:26`). Preparation steps each get `PREPARATION_SECONDS = 60.0` (`scripts/stage2_research_run.py:75`; call sites `:379`, `:1005`, `:1442`). Spec anchors: criterion 19 (finite deadlines, required-first, judge reserve, no retries; refuted-by list) and criterion 54 (a resumed run gets its own deadlines) in `plans/changes/research-swarm/spec.md:375-376, 480-481`, plus the deadline section `plans/changes/research-swarm/spec.md:655-670` (catalog 60 s, topic author 5, finder/researcher/merge 10, judge 15, run 150; a topic launches only with positive pre-reserve time left). The `150.0` value is pinned by `test_amended_graph_and_deadlines_bound_every_launch` (`tests/test_stage2_swarm.py:1562, 1571`).

**3 · Bounded runner-owned steps and probes.** `TOOL_SECONDS = 300`, `VERIFY_SECONDS = 1800`, `GIT_SECONDS = 120` (`scripts/stage2.py:3991-3993`), `RED_FIRST_MINUTES = 10` (`:432`), `PI_DISCOVERY_SECONDS = 120` (`:371`), `PI_VERSION_SECONDS = 30` (`:256`) — every abort names its limit, "never a silent cut" (`scripts/stage2.py:3957`; the R-19/R-20/R-21 repair, `docs/journal/handover/2026-10-20-review-swarm-runner-review.md:339, 473`). `docs/WORKFLOW.md:480-484`: queue and memory waits consume no runner step limit; the configured limits still bind the executing check. Availability preflight: `PROBE_SECONDS = 60`, `PROBE_RETRY_SECONDS = 180`, `FREE_PROBE_SECONDS = 120`, `FREE_PROBE_RETRY_SECONDS = 360`, `CATALOG_SECONDS = 70`, `INTELLIGENCE_SECONDS = 20` (`scripts/stage2_availability.py:49-64, 78`); the preparation receipt expires after 900 seconds (`plans/changes/loop-until-clean/spec.md:225`).

**4 · Model calls with no time limit — "not there" today.** `run_codex` (`scripts/stage2.py:2548-2595`) calls `launch` with neither `timeout` nor `deadline` (`:2585`), so it takes the plain `subprocess.run` branch (`:916-927`): no process group, no registration in `_LIVE_GROUPS` — no timeout kill and no kill on an interrupted runner. Every Codex route rides it: `draft` (`:7882`), `implement`/`repair` (`:7216`), and the review verbs the docstring names (`:2559-2560`). Likewise `run_work_model` (`scripts/stage2.py:4580`) accepts `timeout`/`limit` but none of its four call sites passes them: `spec_review` (`:2999`), `explore` (`:6795`), `implement`/`repair` Claude routes (`:7220`), `draft` Claude routes (`:7884`). What exists there is measurement only: an attempt's span is recorded (`started_wall, started_mono`, `scripts/stage2.py:7200-7203`) — measured and bounded are two different things. `CLI_TIMEOUT = 30.0` / `OSASCRIPT_TIMEOUT = 30.0` (`scripts/stage2_session.py:62-63`) bound only transcript reading, not a model call.

## Where it lives

Review loop: `scripts/stage2.py` (constants `:252, :838`, round deadline `:8374-8466`, `remaining` `:2635`, `launch` `:895-978`). Research swarm: `scripts/stage2_research_run.py` (`:66-67, :75, :328-330, :857-881`) and `scripts/stage2_research_dispatch.py` (`:26, :250-251, :259-291`). Probes: `scripts/stage2_availability.py:49-78`. Doctrine: `docs/WORKFLOW.md:480-484, :982-983, :1421-1430`. Criteria: `plans/changes/research-swarm/spec.md` (19, 54, deadline section), `plans/changes/loop-until-clean/spec.md:197-205` (doctrine criterion 15), `plans/changes/review-loop-deep-b/spec.md:68, 79`, `plans/changes/free-member-rate-limit/spec.md:60`. Review origin: `docs/journal/handover/2026-10-20-review-swarm-runner-review.md`. Tests: `tests/test_stage2.py` (`:5861, :5894`, the DL-B-10/DL-B-14 tests named in `plans/changes/review-loop-deep-b/findings.md:44-47`), `tests/test_stage2_swarm.py:1562`, `tests/test_stage2_research_dispatch.py`.

## What is unclear

- The bead `coding-harness-ht1b` carries the change's class and motivation in its description, which I could not read with this phase's read-only tools (the tracker is the Dolt database; no rendered copy exists in the tree). What "swarm-time-limits" is meant to change — the values, the unbounded single-model calls, or something else — is an open question for the interview.
- The `REVIEWER_MINUTES` comment cites "spec, criterion 15"; the only criterion 15 I found (`plans/changes/loop-until-clean/spec.md:197-205`) is about phase-4b doctrine agreement, not verbatim about the 45-minute stop. A spec criterion whose text names the reviewer time limit directly was not found (search for "is stopped", "45 minutes", "30 minutes" over all `plans/changes/**/spec.md` — no match); the limit lives in code and in `docs/WORKFLOW.md:1429`.
- No statement was found anywhere about a cap or doctrine sentence for the combined two-round-limit call (free drop → Flash takeover, `docs/WORKFLOW.md:1424`); the 2 × 45 minutes stand as written.
- `RUN_MINUTES = 150.0` and the `MINUTES` allowances are hard-coded constants; nothing read offers a flag or declaration to tune them per run. Not found ≠ not there: I read the runner scripts and the doctrine, not every ADR body.

## Files a change would have to touch

`scripts/stage2.py` (constants `:252, :256, :371, :432, :838, :3991-3993`; round deadline `:8374-8466`; `run_codex` `:2548-2595`; `run_work_model` `:4580` and call sites `:2999, :6795, :7220, :7884`), `scripts/stage2_research_run.py` (`:66-67, :75`), `scripts/stage2_research_dispatch.py` (`:26, :250-251`), `scripts/stage2_availability.py` (`:49-78`), `docs/WORKFLOW.md` (`:982-983, :1421-1430`), the tests named above, and the criteria that restate the limits (`plans/changes/research-swarm/spec.md`, `plans/changes/loop-until-clean/spec.md`, `plans/changes/free-member-rate-limit/spec.md`, `plans/changes/review-loop-deep-b/spec.md`).

**Neighbours known:** `plans/changes/research-swarm/spec.md`, `plans/changes/loop-until-clean/spec.md`, `plans/changes/free-member-rate-limit/spec.md`, `plans/changes/review-loop-deep-b/spec.md`, `plans/changes/malformed-answer-retry/spec.md`, `plans/changes/fail-fast-attempts/spec.md`, `plans/changes/swarm-test-speed/spec.md`, `plans/changes/time-records-data/spec.md`, `plans/changes/archive/2026-10-07-stage2-mimo/` (REVIEWER_MINUTES history), living spec `plans/specs/implementation-verification/spec.md`.
