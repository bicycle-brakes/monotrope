---
title: "Plan — night-heartbeat"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-07
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
   scheduler wake or a background tool job running `sleep 1800` whose
   completion the harness delivers to the orchestrating session; never shell `&` or `nohup`. Record the returned
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
   Log unchecked state as unknown. On resume, rearm first, refresh lane state
   and record the gap from the last actual check; never invent missed successful wakes.
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
   `plans/changes/night-heartbeat/trial-lane-watchdog.sh.txt` was committed by
   the orchestrator as reference evidence before this change's implementation
   attempt; it stays reference only and adds no supported implementation path.

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
edit other change specs or historical night plans/handovers. The taken
review rows authorise corrections to `research.md` and a historical header
and non-executable mode for the existing trial reference; no other path is
added. Do not edit runner code, hooks, model/gate configuration, ADRs or tracker state. The current
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

## Walkthrough — procedure simulation, 2026-11-06

Written by the phase-4 implement attempt. **This is a procedure
simulation** with synthetic lanes, handles and timestamps: it exercises
the documented wake order on paper and is not evidence of real timer
delivery. No model call, no `sleep 1800`, no background job and no
overnight wait was run. This attempt has file tools only and could not
probe the harness's actual scheduling and background-completion
semantics, so that check stays unperformed and is recorded here as a
limit: live readiness is neither claimed nor denied. The live
demonstration remains open for the orchestrator's bootstrap and a real
night run. The trial file `trial-lane-watchdog.sh.txt` stays reference
only.

Scenario: run `2026-11-06-a`, watched by orchestrating session S1
(later its successor S2), on a machine where a second, older run
`2026-11-06-b` is already active with its own wake `W-b4` (due
05:10Z) and keep-awake `KA-b`.

**Setup — 2026-11-06T23:05Z.** S1 creates the run state directory
`${XDG_STATE_HOME:-~/.local/state}/coding-harness/night/2026-11-06-a/`
and records run id `2026-11-06-a` and the directory path in its handover
file `docs/journal/handover/2026-11-06-night-a.md` (a synthetic record in
this simulation, not a file created by this change). It writes `lanes.txt`
(empty `busy/`, empty `lane-watch.log`):

    l1 | .claude/worktrees/docs-sweep   | docs-sweep, explore dispatched | on completion: dispatch stage2.py implement docs-sweep
    l2 | .claude/worktrees/spec-polish  | spec-polish, repair dispatched | on completion: dispatch stage2.py review spec-polish
    l3 | .claude/worktrees/rename-util  | rename-util, awaiting triage   | orchestrator: triage loop rows (busy marker)
    l4 | .claude/worktrees/triage-43    | triage-43, plan accepted       | dispatch stage2.py implement triage-43

It arms wake `W1` (handle bg-101, due 23:35:00Z), verifies the facility
reports it deliverable to this session, starts keep-awake `KA-a`
(`caffeinate -i -t 28500`, handle bg-102, expiry 07:00:00Z — the intended
run period), and records all handles and times in the run state. Every
lane entry names lane id, worktree, current item and next authorised
action, so the file alone reconstructs the watch list.

**Wake W1 — 2026-11-06T23:35Z, delivered.** Rearm first: `W2` (bg-103,
due 00:05:00Z), handle retained before any lane work. Lane file read. l1's
explore finished 23:21Z → idle with eligible work, `stage2.py implement
docs-sweep` dispatched now; entry updated (current item: implement
dispatched; next action: on completion dispatch review). l2's repair
finished 23:12Z → idle with eligible work, `stage2.py review spec-polish`
dispatched now; entry updated (current item: review dispatched; next
action: record review outcome; if green, lane complete). l3 holds marker `busy/l3` ("owner
S1 · activity: triage loop rows for rename-util") — genuine busy work,
still in progress → left untouched, no duplicate dispatched. l4's
implement needs a maintainer decision (two queued changes edit the same
hot file; which runs first?) → parked: question written to the run's
handover record, l4 removed from `lanes.txt`, not started. One summary
line appended:

    2026-11-06T23:35:41Z | W1 due 23:35Z | l1 idle served: implement dispatched | l2 idle served: review dispatched | l3 busy: triage loop rows (marker busy/l3) | l4 parked: hot-file decision -> morning | next W2 00:05Z

**Wake W2 — 2026-11-07T00:05Z, delivered.** Rearm first: `W3` (bg-104,
due 00:35:00Z). l1 implement and l2 review are running runner calls (no
markers) → left running. l3's marker is now a leftover: the triage
finished 23:52Z, its findings are recorded, and its owner shows no
current activity → the owner's actual activity is checked before anything
happens, the marker is cleared, and l3's idle eligible work
(`stage2.py implement rename-util`) is dispatched in this wake — not
deferred to the next timer, not duplicated. One summary line appended:

    2026-11-07T00:05:38Z | W2 due 00:05Z | l1 running | l2 running | l3 marker verified finished (triage 23:52Z), cleared; implement dispatched | next W3 00:35Z

**Gap — W3 missed.** W3 (due 00:35:00Z) is not delivered: S1 hit its
usage limit at 00:19Z. No check is logged for the missed wake and no
service is claimed; `lane-watch.log` stays silent after the 00:05:38Z
line.

**Resume — 2026-11-07T02:14Z.** Usage returns; successor session S2
finds run id `2026-11-06-a` and its state-directory path in the run's
handover file and reopens that directory, with no chat memory of S1.
Its ownership record identifies KA-a and the wake handles as run a's
resources; S2 takes over their management as successor owner of run a.
`lanes.txt` at that moment (entries as last updated):

    l1 | .claude/worktrees/docs-sweep   | docs-sweep implement (dispatched 23:35Z) | on completion: dispatch stage2.py review docs-sweep
    l2 | .claude/worktrees/spec-polish  | spec-polish review (dispatched 23:35Z) | on completion: record review outcome; if green, lane complete
    l3 | .claude/worktrees/rename-util  | rename-util implement (dispatched 00:05Z) | on completion: dispatch stage2.py review rename-util

S2 retires the missed W3 handle and rearms first: `W4` (bg-118, due
02:44:00Z). Lane state is refreshed
from actual job activity, not from the gap: l1's implement finished
00:41Z and l2's review finished 01:02Z green (both read from their runner
records now) → l1's next authorised action (`stage2.py review docs-sweep`)
is dispatched now; l2 has no next action → lane complete, entry removed.
l3's implement is still running → left running. S2's first summary line
names the gap explicitly:

    2026-11-07T02:14:25Z | resume | gap: 00:05:38Z-02:14Z unobserved (usage limit; no checks claimed) | l1 idle served: review dispatched | l2 complete, off the list | l3 running | next W4 02:44Z

**Wake W4 and teardown — 2026-11-07T02:44Z, delivered.** Rearm first:
`W5` (bg-122, due 03:14:00Z). Then: l1's review finished 02:39Z green →
lane complete, entry removed. l3's implement finished 02:38Z, but its
next step (review) is not eligible: the finished triage recorded a
maintainer decision (a spec Boundary) as its prerequisite → l3 is parked
with that question in the run's handover record, entry removed, not
started. All remaining work is done or parked, so the run ends in this
wake: S2 cancels exactly the run's own handles (W5 and KA-a), identified
by the run-state ownership record, and checks `busy/` for the run's own markers (none left — l3's marker was cleared at W2);
run b's `W-b4` and `KA-b` are left untouched. The end and its reason go
into the run's handover record; `lanes.txt` is empty and `lane-watch.log`
holds one line per handled wake plus the resume check, and no invented checks:

    2026-11-07T02:44:33Z | W4 due 02:44Z | l1 complete, off the list | l3 parked: maintainer decision before review -> morning, off the list | run ended: all work complete or parked; W5 cancelled, KA-a cancelled, no owned markers left | run b untouched

**Observations against the criterion ledger.**

1. Setup recorded wake handle and due time and verified that delivery was
   offered; the missed W3 later shows as a gap, not as service. The wake
   is periodic and time-based — no idle-only trigger substitutes for it.
2. Keep-awake owned (bg-102), bounded to the intended run period with a
   recorded expiry, started before unattended work.
3. At resume, S2 reconstructed lanes and next steps from all three retained
   entries in `lanes.txt`, then checked actual job activity; parked lanes (l4 at W1, l3 at teardown) and completed lanes
   (l2) left the watch list.
4. W1 left genuine busy work untouched (no duplicate); W2 verified the
   leftover marker against its owner's activity, cleared it and
   dispatched once — no duplicate dispatch, no permanent busy state.
5. Three delivered wakes (W1, W2, W4) and one resume check, four summary
   lines — one per handled wake or resume, each covering all watched lanes
   plus the next due time or the end record; missed W3 produced no line and no invented observation.
6. W1 armed W2 and W2 armed W3 before lane work. W3 was missed;
   resume retired the missed handle and armed W4 (bg-118) at 02:14Z.
   W4 was delivered at 02:44Z and armed W5 (bg-122) before lane work;
   teardown cancelled W5. Each armed handle is accounted for: W1, W2
   and W4 delivered once, W3 missed, W5 cancelled.
7. Idle lanes with eligible work (l1 and l2 at W1, l3 at W2, l1 at
   resume) were served in the wake that found them; decisions (l4's
   hot-file question, l3's Boundary prerequisite) were parked with their
   questions, never started.
8. The usage-limit interruption is recorded as an unobserved interval in
   the resume line; no check was fabricated for the missed W3 and no
   service was claimed for the gap.
9. Teardown cancelled only run a's owned wake and keep-awake; run b's
   handles survived untouched.

**Limits.** No live wake was armed, no delivery observed and no machine
keep-awake started: the harness's scheduling and completion semantics
were not exercised by this attempt, and the plan's live-readiness check
stays with the orchestrator's bootstrap and a real night run.

## Time used

2026-11-06 14:38:22–15:22:15 UTC, 2633 s — implement · attempt 1 · route flash · model glm-5.3-flash · accepted · measured by the runner
2026-11-07 08:27:20–08:50:50 UTC, 1410 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
