---
title: "Plan — night-heartbeat"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-7x3c
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, night-run, heartbeat]
---

# Plan — night-heartbeat

```text
For you:     Every night run follows a fixed 30-minute wake routine with a lane file and an honest supervision log.
Done when:   The workflow and instruction pointer agree, every criterion has walkthrough evidence, and required checks pass.
Appetite:    1 hour of phase 4, repairs included; a stop, not an estimate.
Not now:     A new scheduler, runner automation, status display, notifications or recovery during a usage-limit pause.
Pre-mortem:  suppose it failed: most likely because the first wake was scheduled but never rearmed.
Starts unless you say stop.
```

Implements `spec.md` from `d8b3bf8c`, read 2026-11-06. Class bounded:
no design or ADR. There is no `templates/plan.md`; follow `prompts/03-plan.md`.
Explore used Stage 2, GLM 5.3 Flash through `glm-coding-plan` on 2026-11-06;
no Stage-1 exploration fallback is recorded. No open phase-2a rows exist in
the supplied `findings.md` (read 2026-11-06).

## Files and steps

1. **Runner:** change `docs/WORKFLOW.md`, under “Night runs”, adding the routine
   without replacing the existing capacity and parking rules. Before unattended
   work, create a run-specific local directory (for example
   `${XDG_STATE_HOME:-~/.local/state}/coding-harness/night/<run-id>/`) holding
   `lanes.txt`, `busy/` and append-only `lane-watch.log`. Document lane entries
   as lane id, worktree, current item and next authorised action; retain parked
   reasons/questions in the run's existing handover record, remove parked lanes
   from the watch list, and update entries when work changes. These files are
   session state, never a replacement tracker or committed task list.
2. In that section, require a 30-minute scheduled return to the same session
   and verification that the harness will deliver it. Use an existing session
   scheduler or a foreground `sleep 1800` submitted as its own background tool
   job with completion delivery; never shell `&` or `nohup`. Record the returned
   wake handle and due time. A background process without delivery is not a wake.
   If that facility is unavailable, report the missing supervision instead of
   declaring the run ready. Start and verify run-bounded keep-awake (on macOS,
   `caffeinate -i -t <remaining-run-seconds>` as a separately owned background
   job); record its handle and expiry. Do not introduce a scheduler adapter.
3. Document the wake order: rearm once for 30 minutes and retain its handle;
   read the lane file; check actual job completion/activity and busy ownership;
   serve eligible idle work immediately; park decisions for the morning; append
   one UTC summary line with each lane's observed state and action plus the next
   due time. A busy marker names owner/activity and is cleared when that work
   finishes; verify an apparent leftover against the owner's current activity,
   never blindly launch a duplicate or treat a marker as permanent proof.
   Log unchecked state as unknown. On resume, add the gap from the last actual
   check, refresh lane state and rearm; never invent missed successful wakes.
   At finish/all parked, cancel the owned wake and keep-awake handles, clear owned
   markers and record why the run ended. Markers live at `busy/<lane-id>`;
   each names its owner and current activity. Do not kill by broad pattern.
4. **Orchestrator bootstrap, after the accepted attempt:** change the existing
   night-job bullet in `AGENTS.md` to include this exact sentence on the same
   physical line, preserving its existing rule and the 200-line budget:
   “Every night run arms a recurring 30-minute wake, keeps the machine awake,
   and checks and logs its lanes as described in `docs/WORKFLOW.md`, ‘Night runs’.”
   The maintainer authorised this pointer in `decisions.md`; the stage-2 attempt
   must not edit or commit this held path.
5. Record a compact scenario walkthrough and its observations in this `plan.md`:
   setup, two successive wakes, running job, genuine busy work, abandoned marker,
   idle eligible lane, parked question, usage-limit gap, resume and teardown.
   Use synthetic lane data and timestamps; label it a procedure simulation, not
   evidence of real timer delivery. Check the actual harness's scheduling and
   completion semantics before claiming live readiness; when unavailable, record
   that limit and leave the live demonstration unperformed. No model call or
   30-minute sleep is needed for the walkthrough. The trial file
   `plans/changes/night-heartbeat/trial-lane-watchdog.sh.txt` stays reference only.

The criteria govern an operator procedure, not executable enforcement;
text-matching tests would not establish that the orchestrator follows it.

## Criterion ledger

- 1: not a test — review setup and walkthrough wake handle/due time; refuted by absent delivery or an idle-only trigger.
- 2: not a test — review setup and walkthrough keep-awake ownership/expiry; refuted by absent or unbounded keep-awake.
- 3: not a test — reconstruct the walkthrough from its lane file alone; refuted by missing next work or a watched parked lane.
- 4: not a test — walkthrough running job, busy owner and abandoned marker; refuted by duplicate dispatch or unchecked permanent busy state.
- 5: not a test — count one summary per handled wake in the walkthrough; refuted by missing, per-lane or invented observations.
- 6: not a test — walk two successive wakes; refuted by a missing next handle or rearming delayed until after lane work.
- 7: not a test — walkthrough idle authorised work and a question; refuted by deferral of eligible work or dispatch past a decision.
- 8: not a test — walkthrough a usage-limit gap and resume; refuted by fabricated checks or an assertion of service while unavailable.
- 9: not a test — walkthrough teardown with another run present; refuted by a surviving owned wake or cancellation of the other run.

## Verification and limits

```bash
python3 scripts/check_interview_minimums.py --change night-heartbeat
python3 scripts/check_criterion_ledger.py
python3 scripts/check_research_handoff.py --change night-heartbeat
.venv/bin/python -m pytest -q tests/test_entry_points.py
python3 scripts/plans_registry.py --check
```

The orchestrator runs the entry-point tests after its bootstrap edit. The
runner regenerates `plans/INDEX.md`, updates its own `findings.md`, and runs
the required verification and commit. Its full implementation gate is
`make verify`; an orchestrator-only text edit uses CI plus the targeted check
above under the repository's text-change rule. The referenced
`scripts/validate_change_artefacts.py` does not exist at the inspected baseline;
do not report it green. Tracker-backed checks belong to the orchestrator/runner;
this draft does not access tracker state outside the worktree.

Create no implementation file. Change only the two documentation paths named
above, this plan for evidence/time, and runner-owned findings/index. Do not
edit other change specs, historical night plans/handovers, trial reference,
runner code, hooks, model/gate configuration, ADRs or tracker state. The current
PR state and live session scheduler were not read by this draft. Stop at the
one-hour appetite with remaining work recorded; do not weaken criteria.

## Draft checks — 2026-11-06

The interview gate and criterion-ledger gate passed. Research handoff reported
the change exempt because no research-swarm/v2 run exists. Both artifact
headers, all nine refuting cases, the opening card and empty time section
were checked. An in-memory index render differs from `plans/INDEX.md`;
regeneration is left to the runner. The tracker-backed registry check,
missing artifact validator, full verification and live wake delivery are
not reported green by this draft. No commit was made.

## Time used
