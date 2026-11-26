---
title: "Findings — verify-two-slots"
category: findings
status: accepted
implementation_status: done
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-26
updated: 2026-11-26
supersedes: null
superseded_by: null
bead: coding-harness-u1ha
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — verify-two-slots

Stage-2 call, 2026-11-21: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1146 files, 5069 commits, 12 rules.

Stage-2 call, 2026-11-21: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1149 files, 5072 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-21

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S2-1 | MAJOR | SPEC | base | `spec.md` criteria 2 and 4; Open decisions, first [DETAIL] | [AMBIGUITY] The spec doesn't say whose capacity applies when live entries carry different `HARNESS_VERIFY_SLOTS` values. Criterion 2 only covers "all new entries" using one value, and criterion 4 has no such condition. Reading A: each entry compares the occupied count with its own value. A `=1` run then enters an empty machine, but a later default entry joins beside it, so `=1` does not mean "run alone". A `=1` waiter at the head of the queue with one slot taken either holds a `=2` waiter behind it (a free slot stays unused) or is overtaken (a later waiter passes a live earlier one); criterion 4 refutes both. Reading B: the lowest value among live holders and waiters governs, kept in shared state, so a `=1` entry keeps the machine to itself for its whole run. Each reading gives different tests for criteria 2 and 4. | Opus | in spec — [DETAIL] decided by the orchestrator: Reading B — publish each updated holder's and waiter's configured slots (1 or 2) in shared state/queue records; only the head live waiter may acquire, and effective capacity is min(all live holders' slots, head live waiter's slots), so a =1 entry drains to 0 before entering, runs alone for its duration, and is never overtaken; update criterion 4 to refer to capacity free under effective capacity | — |
| S2-2 | MAJOR | SPEC | base | `spec.md` criterion 2; Open decisions, first [DETAIL] ("consistent values must be supplied to all new entries") | [AMBIGUITY] The spec doesn't say whether `HARNESS_VERIFY_SLOTS` travels to child processes. The memory-floor override does: `inherit_env` copies it explicitly (`scripts/verify_lock.py:771-772`). The runner's allow-list for launched calls holds no `HARNESS_*` name (`scripts/stage2.py:412-425`). Reading A: the setting travels like the floor override, so the operator's value reaches the independent entries the runner and its agents start. Reading B: it does not travel, so an independent entry started under the allow-list (for example an agent's own `make verify`) uses the default 2 while the runner's in-process full check uses `=1`. Criterion 2's condition, "all new entries", then cannot be met by setting the variable once, and a reduction to 1 is not machine-wide. Which processes the operator must reach, and how, is left to the builder. | Opus | in spec — [DETAIL] decided by the orchestrator: Reading A — verify_lock.inherit_env forwards HARNESS_VERIFY_SLOTS to local child processes just like FLOOR_ENV (HARNESS_VERIFY_MIN_FREE_PCT), while stage2.py's foreign-call ENV_ALLOW stays closed (no HARNESS_* variables sent to foreign model calls) | — |
| S2-3 | MAJOR | SPEC | base | `spec.md` criteria 4 and 10; Open decisions, second [DETAIL] ("FIFO applies among updated waiters") | [AMBIGUITY] The spec doesn't say whether an older single-slot checkout's waiter must ever get in while updated admissions keep overlapping. Reading A: updated waiters ignore an earlier old waiter. The old waiter needs the exclusive lock, and it gets that only if both slots happen to be empty at one of its non-blocking polls every 0.25 s (`verify_lock.py:122`, `:635`). On a busy night an old lane can therefore wait without end: the queue wait has no deadline and uses up no step limit (`verify_run.py:924-925`). Lanes opened before the merge are exactly these. Reading B: updated waiters stay behind an earlier-registered old waiter. A free slot then stays unused, which criterion 4 refutes. Criterion 10 forbids only overlap, so no criterion can fail on either choice. | Opus | in spec — [DETAIL] decided by the orchestrator: Reading B — updated waiters honor FIFO behind an earlier live legacy waiter in the shared verify.queue directory (an empty queue record counts as an exclusive 1-slot waiter), draining shared slots to 0 so legacy checkouts never starve; state this explicitly in criteria 4 and 10 | — |
| S2-4 | MAJOR | SPEC | base | `spec.md` criterion 12 ("run durations", "individual wall times") | [AMBIGUITY] Two measures of a run's length fit the text. Reading A: wall time from launch to exit, including the cheap phase and the admission and memory waits. Reading B: the execution seconds the history records. `run_end.seconds` sums the gate segments and leaves out the queue and memory waits (`scripts/verify_duration.py:16-17`), and criterion 11 keeps wait apart from execution. The machine has 8 GiB, a 25 % floor and 30 s rechecks, so the second simultaneous run's memory gate can hold it for minutes. The same trial can then pass the 1.6× limit under B and fail it under A. | Opus | in spec — [DETAIL] decided by the orchestrator: Reading A — the 1.6x threshold in criterion 12 measures end-to-end wall time of each make verify invocation from launch to exit (starting with both slots free), while also recording execution seconds and admission/memory wait seconds separately in measurements.md for diagnosis | — |
| S2-5 | MAJOR | SPEC | base | `spec.md` criterion 12 ("representative night load"; *Basis:* Q-3 at `b5c2105b`) | The trial's load condition is defined only by answer Q-3 on the unmerged branch `feat/verify-slots`. `research.md` ("What is unclear") says those records cannot be read from this tree, and spec, research and decisions give no process mix, load figure or bound. Whoever runs the trial decides what counts as representative. The refutation asks only that the sampled load be recorded. No recorded load makes a trial invalid, so the load part of the criterion cannot go red, and this review cannot check it against its basis. | Opus | in spec — [DETAIL] decided by the orchestrator: inline the Q-3 load definition directly into spec.md (keep b5c2105b as provenance only, not an external dependency): run the paired trial under normal active workstation/harness load (other non-verify lanes may keep working, not requiring a clean-room idle machine, and with no third verify run contending for the slots), recording background processes/lanes, start/end 1m/5m/15m load averages, and start/minimum available memory %; refute if those readings are missing or a third verify overlapped | — |
| S2-6 | MAJOR | SPEC | base | `spec.md` criterion 12 ("no test turns red or flaky because of parallelism"; "An unrelated content failure is investigated separately") | This clause cannot go red independently. One serial run and one simultaneous pair cannot show flakiness, which needs repetition. The spec also gives no rule for deciding whether a red in a parallel run is caused by parallelism or is an unrelated content failure: no rerun count, no serial rerun of the failing test, no named decider. The person running the trial makes that call and can always file a red as unrelated. | Opus | in spec — [DETAIL] decided by the orchestrator: make criterion 12's failure attribution explicit and refutable: all three runs (1 serial + 2 simultaneous) must exit 0; if any test fails in a simultaneous run, rerun that test serially on the same revision — passing serially classifies it as parallelism-caused (trial fails, stop and report), while failing serially classifies it as a content failure that must be fixed and the paired trial repeated green before completion; note honestly that one paired trial verifies zero observed failures rather than statistical long-run flake proof | — |
| S2-7 | MAJOR | SPEC | base | `spec.md` criterion 12 ("on the implemented revision"); Definition of Done ("identified by revision") | [AMBIGUITY] The spec doesn't say whether the trial must be repeated when review-loop or phase-6 repairs change `scripts/verify_lock.py` or `scripts/verify_run.py` after it ran. Reading A: the trial must be on the last revision that changes code, so every such repair means a new serial run and a new pair, roughly 30 minutes each time against the 4-hour stop. Reading B: any revision that contains the implementation counts. The pull request can then cite a trial of code it no longer contains. | Opus | in spec — [DETAIL] decided by the orchestrator: Reading A scoped to runtime code — the recorded trial in measurements.md must match the final revision of scripts/ (git diff <trial-commit>..HEAD -- scripts/ must be empty); later doc-only, test-only, or plans/ edits do not invalidate it if verified and noted, whereas any later scripts/ repair requires rerunning the paired trial (stopping at the 4-hour appetite if reached) | — |
| S2-8 | MINOR | SPEC | base | `spec.md` criterion 3 | [AMBIGUITY] "Exactly `1` or `2`": the module's own precedent strips the floor override before parsing it (`memory_floor()`, `verify_lock.py:394`). Reading A: compare the string exactly, so ` 2`, `2\n`, `02` and `+2` are refused. Reading B: strip and parse as the floor does, so they are accepted. The criterion also doesn't say whether a valid descendant refuses an invalid value. Today nested entries return before any queue or memory reading (`verify_lock.py:744-748`), so with an invalid floor they never refuse. The literal "the entry refuses" would make every nested entry read and refuse the setting. | Opus | in spec — [DETAIL] decided by the orchestrator: Reading A for parsing (exact string '1' or '2', no stripping, no '+2'/'02') and match existing hold_admission precedence (verify_lock.py:744-748): a validated inherited descendant returns before reading HARNESS_VERIFY_SLOTS, so criterion 3 applies to independent entries only | — |
| S2-9 | MINOR | SPEC | base | `spec.md` criterion 7 (refutation "blocks capacity indefinitely") | This clause cannot be refuted by any finite test. The spec gives no time within which a dead holder's slot must become usable again once its last inherited descriptor closes, so each test author invents their own timeout and a slow release passes. | Opus | in spec — [DETAIL] decided by the orchestrator: set an explicit finite release bound in criterion 7 — once a dead holder and its last surviving protected descendant close their inherited lock descriptors, its slot becomes reservable by the next live waiter within 2 poll intervals (<= 1 s at default POLL_SECONDS=0.25, or <= 2 * poll_seconds in tests) | — |
| S2-10 | MINOR | SPEC | base | `spec.md` Protected areas and Definition of Done; `decisions/gates.yaml:49-59` | Two requirements conflict. The protected header of `decisions/gates.yaml` describes one slot as current behaviour ("who needs the machine's verify slot", line 50; "runs outside the slot", line 59). The Definition of Done asks for current behaviour to be described but lists only four docs, and the Protected areas forbid touching `gates.yaml`. The builder must either leave single-slot wording in the gate list or break the protected area, and the spec doesn't say which. | Opus | in spec — [DETAIL] decided by the orchestrator: keep decisions/gates.yaml strictly untouched (human-decided protected area); update only the four listed living docs (docs/WORKFLOW.md, docs/orchestration.md, docs/how-it-works.md, docs/governance/gate-catalog.md) and note the single-slot comment in decisions/gates.yaml:49-59 as an accepted out-of-scope follow-up for a separate decision PR | — |

Stage-2 call, 2026-11-21: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1149 files, 5078 commits, 12 rules.

Stage-2 call, 2026-11-21: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1149 files, 5079 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-21

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S2-11 | MAJOR | SPEC | base | `spec.md` criterion 2 with criterion 7 | [AMBIGUITY] It is unclear what makes a holder one of the "live updated holders". Reading A: a holder counts while its slot is reserved. A killed `HARNESS_VERIFY_SLOTS=1` holder whose protected child still holds the inherited descriptor then keeps effective capacity at 1, and no `2` waiter may join. Reading B: a holder counts while its process is alive. Once that supervisor dies its `1` stops counting, and a `2` waiter takes the other slot next to the surviving exclusive child. Criterion 7 keeps the slot reserved but does not say whether the setting survives with it; criterion 10 states survival only for old holders. Test that tells them apart: SIGKILL a `1` supervisor while its child runs, then queue a `2` waiter. The criterion goes red under A and stays green under B. | Opus | in spec — [DETAIL] decided by the orchestrator: Reading A — a reserved slot keeps its holder's configured slots value until the final inherited descriptor closes, so a killed `HARNESS_VERIFY_SLOTS=1` supervisor whose protected child survives keeps effective capacity at 1 and no `2` waiter joins beside that child; state this in criterion 7 and add the SIGKILL-then-queue test the finding names. Reason: consistent with S2-1 (`=1` runs alone for its duration); the safe reading never overlaps an exclusive run | — |
| S2-12 | MINOR | SPEC | base | `spec.md` Terms "Slot"; criterion 7 | [AMBIGUITY] It is unclear which descendants keep a slot. Reading A: only descendants that hold the inherited lock descriptor keep it ("release their inherited ownership"). The current accepted overlap then stays: after an intermediate process is killed hard, a protected descendant in another process group that never inherited the descriptor may outlive the slot (`scripts/verify_lock.py:44-49`). Reading B: the Slot term covers "protected descendants' lifetime", and criterion 7 is refuted by "a replacement overlaps a surviving protected child". That overlap is then a failure, and it needs process tracking beyond the descriptor. The spec's Boundary neither carries over nor withdraws the existing limit. | Opus | in spec — [DETAIL] decided by the orchestrator: Reading A — only descendants holding the inherited lock descriptor keep a slot; carry the existing accepted overlap (`scripts/verify_lock.py:44-49`) into the spec's Boundary explicitly and reword the Slot term to match. Reason: process tracking beyond the descriptor is outside Slice 1 (Option A, maintainer 2026-11-21) | — |
| S2-13 | MAJOR | SPEC | base | `spec.md` criterion 12, load paragraph | [AMBIGUITY] It is unclear which overlap invalidates the serial baseline. Reading A: only a "third verify" is barred. During the serial run, another lane's protected check may then take the free second slot and inflate the serial time, which makes the 1.6 ratio easier to meet. That check could be a stage2 targeted check through `hold_admission`, or even another `make verify`. Reading B: "serial" means no other protected admission overlaps the serial run, and "verify" includes targeted admissions, which use the same slots (`research.md`, "The scheduler and its callers"). The two readings accept different trials. | Opus | in spec — [DETAIL] decided by the orchestrator: Reading B — serial means no other protected admission overlaps the serial run, targeted stage2 checks through `hold_admission` included; the trial records every protected admission seen during each run and is refuted by any overlap. Reason: Reading A lets an unrelated check inflate the serial time and makes 1.6x easier to pass | — |
| S2-14 | MINOR | SPEC | base | `spec.md` criterion 12 | [AMBIGUITY] It is unclear where the two simultaneous runs execute. Reading A: both run in the same worktree. They then share the working tree, its caches and the tree snapshot `verify_run` compares across the admission (`scripts/verify_run.py:913-954`), so one run's writes can make the other rerun its cheap gates or refuse. Reading B: they run in two worktrees at the trial revision, the cross-worktree case the bead targets. Wall times and the "parallelism-caused" classification differ between the two. | Opus | in spec — [DETAIL] decided by the orchestrator: Reading B — the two simultaneous runs execute in two separate worktrees at the trial revision. Reason: the cross-worktree case is what the bead targets, and a shared tree makes `verify_run`'s snapshot comparison interfere | — |
| S2-15 | MINOR | SPEC | base | `spec.md` criterion 12 | Hole: the spec fixes neither the order of the serial run and the pair nor the cache state each starts from (first run after checkout, or warm). A cold serial baseline followed by a warm pair lowers the ratio, and a cold pair raises it, so whoever runs the trial decides the result. Only "both slots free" is fixed. | Opus | in spec — [DETAIL] decided by the orchestrator: fix the order and cache state — one discarded warm-up run per worktree, then the serial run, then the pair, all warm; record the order and the warm-up run ids. Reason: removes the result's dependence on who runs the trial | — |
| S2-16 | MINOR | SPEC | base | `spec.md` criterion 12, refutation list | [AMBIGUITY] "admission and memory wait seconds" has two readings. Reading A: the one combined queue-plus-memory figure the history already records (`admission_wait_seconds`, `scripts/verify_duration.py:286`). Reading B: separate queue-wait and memory-wait seconds. Nothing measures these today, so they need new instrumentation or log timing, and the `_log` lines carry no timestamps (`scripts/verify_lock.py:174-176`). Under A a trial that records one figure is complete; under B it is refuted for a missing reading. | Opus | in spec — [DETAIL] decided by the orchestrator: Reading A — the one combined figure the history already records (`admission_wait_seconds`, `scripts/verify_duration.py:286`); a queue/memory split is a non-goal of Slice 1. Reason: no new instrumentation in the minimal slice | — |
| S2-17 | MINOR | SPEC | base | `spec.md` criterion 12, load paragraph | Hole: "minimum available memory percentage" has no sampling method or interval, yet "missing readings invalidate the trial". The text is satisfied by one reading at the start and one at the end, and equally by continuous sampling. The non-goals exclude RAM-minimum telemetry, so the implementer has to invent an outside sampler and its interval. A missing-reading case cannot be built until the expected readings are defined. | Opus | in spec — [DETAIL] decided by the orchestrator: sample available memory % every 5 seconds from an outside sampler for each run's whole duration; a gap longer than 15 seconds counts as a missing reading and invalidates the trial. Reason: makes the missing-reading case buildable without RAM telemetry in the product (non-goal stays) | — |
| S2-18 | MINOR | SPEC | base | `spec.md` criterion 12, failure paragraph | [AMBIGUITY] It is unclear what happens after a content failure. Reading A: a serial failure "must be fixed before repeating the complete trial green", so the implementer repairs it and repeats on their own, within the four-hour stop. Reading B: "If the trial cannot run or fails, stop and report" covers every failed trial, content failures included, so the implementer stops. The spec also does not classify a parallel-run failure that is not a test, such as a gate timeout or a failing non-pytest gate: the rerun rule names only "that test". | Opus | in spec — [DETAIL] decided by the orchestrator: Reading B — every failed trial stops and is reported, content failures included; a parallel-run failure that is not a test (gate timeout, failing non-pytest gate) also stops and reports. Reason: the four-hour appetite and the maintainer decide repairs, not the implementer mid-trial | — |
| S2-19 | MINOR | SPEC | base | `spec.md` criteria 1 and 4 | These two refutations cannot go red as written: "the second cannot reserve an otherwise free slot" (criterion 1) and "a free slot under the effective capacity remains unused" (criterion 4) have no time bound. Only criterion 7 bounds reservation, at two queue poll intervals, and only after the final inherited descriptor closes. A test for a waiter that arrives at an already free slot needs a deadline the spec does not give. | Opus | in spec — [DETAIL] decided by the orchestrator: add the bound criterion 7 already uses — a waiter at the head of the queue reserves a free slot under effective capacity within two queue poll intervals; criteria 1 and 4 refute against that deadline. Reason: gives both refutations a time limit a test can check | — |

Stage-2 call, 2026-11-21: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1149 files, 5085 commits, 12 rules.

Stage-2 call, 2026-11-21: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1149 files, 5088 commits, 12 rules.

Stage-2 call, 2026-11-21: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1149 files, 5089 commits, 12 rules.

Stage-2 call, 2026-11-21: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1149 files, 5109 commits, 12 rules.

Stage-2 call, 2026-11-21: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1149 files, 5112 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +38 -19
> - `docs/governance/gate-catalog.md` +5 -3
> - `docs/how-it-works.md` +6 -4
> - `docs/orchestration.md` +3 -2
> - `plans/changes/verify-two-slots/measurements.md` +62 -0
> - `scripts/stage2.py` +6 -6
> - `scripts/verify_lock.py` +495 -139
> - `scripts/verify_run.py` +14 -14
> - `tests/test_stage2.py` +2 -2
> - `tests/test_verify_before_admission.py` +137 -3
> - `tests/test_verify_duration.py` +66 -0
> - `tests/test_verify_lock.py` +623 -38
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `scripts/verify_lock.py`, `tests/test_verify_lock.py`.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>     
>         monkeypatch.setattr(verify_run, "gate_process", spying_gate_process)
>     
>         holder_one = holder_two = None
>         try:
>             # Both slots occupied before any scheduler starts, so both runs must queue.
>             holder_one = _start_slot_holder(checkout, "one")
>             holder_two = _start_slot_holder(checkout, "two")
>     
>             budget_a = {"deadline": 100.0}
>             budget_b = {"deadline": 200.0}
>             with scheduler_run(root_a, budget=budget_a) as outcome_a:
>                 _wait_queue_count(1)
> >               with scheduler_run(root_b, budget=budget_b) as outcome_b:
>
> tests/test_verify_before_admission.py:694: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/contextlib.py:158: in __exit__
>     self.gen.throw(value)
> tests/test_verify_before_admission.py:287: in scheduler_run
>     raise outcome["error"]  # type: ignore[misc]
> tests/test_verify_before_admission.py:268: in body
>     result = verify_run.run_verification(
> scripts/verify_run.py:921: in run_verification
>     with verify_lock.hold_admission(admission_command or ["verify-run", job]) as lock_fds:
> /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/contextlib.py:137: in __enter__
>     return next(self.gen)
> scripts/verify_lock.py:1094: in hold_admission
>     with _independent_admission_guard():
> /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/contextlib.py:137: in __enter__
>     return next(self.gen)
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
>     @contextlib.contextmanager
>     def _independent_admission_guard() -> Iterator[None]:
>         """Refuse a second independent admission in one process, held or still acquiring.
>     
>         One process owns at most one independent admission, including while it is
>         still acquiring it: a concurrent entry would overwrite the process's
>         published ownership and its admission state, so the second request is
>         refused promptly with a diagnostic. A nested entry never reaches this
>         guard — it reuses its ancestor's admission.
>         """
>         global _ACQUIRING
>         with _ACTIVE_LOCK:
>             if _ACTIVE is not None or _ACQUIRING:
> >               raise VerifyLockRefused(
>                     "this process already holds or is acquiring an independent admission; a second one is refused"
>                 )
> E               verify_lock.VerifyLockRefused: this process already holds or is acquiring an independent admission; a second one is refused
>
> scripts/verify_lock.py:611: VerifyLockRefused
> ----------------------------- Captured stderr call -----------------------------
> [verify-lock] waiting for admission: slot 1: holder pid 20102 (holder, started 2026-11-21T17:03:24); slot 2: holder pid 20111 (holder, started 2026-11-21T17:03:24)
> [verify-lock] admitted after 60s
> [verify-lock] available memory 69% at or above the 0% floor; starting
> =============================== warnings summary ===============================
> tests/test_verify_lock.py::test_second_in_process_admission_refused_during_acquisition
>   /Users/mikypiky/coding-harness/.claude/worktrees/verify-two-slots/.venv/lib/python3.12/site-packages/_pytest/threadexception.py:82: PytestUnhandledThreadExceptionWarning: Exception in thread Thread-1 (<lambda>)
>   
>   Traceback (most recent call last):
>     File "/opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/threading.py", line 1075, in _bootstrap_inner
>       self.run()
>     File "/opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/threading.py", line 1012, in run
>       self._target(*self._args, **self._kwargs)
>     File "/Users/mikypiky/coding-harness/.claude/worktrees/verify-two-slots/tests/test_verify_lock.py", line 1606, in <lambda>
>       first = threading.Thread(target=lambda: list(verify_lock.hold_admission(["first", "entry"])))
>                                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
>   TypeError: '_GeneratorContextManager' object is not iterable
>   
>     warnings.warn(pytest.PytestUnhandledThreadExceptionWarning(msg))
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_verify_lock.py::test_second_in_process_admission_refused_during_acquisition
> FAILED tests/test_verify_lock.py::test_two_slot_fifo_and_dead_waiter - Assert...
> FAILED tests/test_verify_lock.py::test_slot_release_preserves_peer_and_inherited_child
> FAILED tests/test_verify_lock.py::test_slot_setting_and_capacity_reduction - ...
> FAILED tests/test_verify_before_admission.py::test_two_slot_scheduler_preserves_wait_context_and_descriptors
> 5 failed, 24 passed, 1 warning in 76.52s (0:01:16)
> ```

Stage-2 call, 2026-11-21: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 1150 files, 5169 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_verify_before_admission.py` +121 -44
> - `tests/test_verify_lock.py` +41 -21
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>                 "PROBE_OUT": str(one_holder_out),
>                 "PROBE_STARTED": str(holder_started),
>                 "PROBE_SLEEP": "1.0",
>                 verify_lock.SLOTS_ENV: "1",
>             },
>         )
>         assert _wait_until(holder_started.is_file), "the setting-1 holder never started its protected work"
>         follower_out = tmp_path / "two-follower.json"
>         follower = _supervised(state, RECORD_BODY, {"PROBE_OUT": str(follower_out), "PROBE_SLEEP": "0.1"})
>         assert not _wait_until(follower_out.is_file, 0.6), (
>             "a setting-2 follower reserved capacity beside a setting-1 holder"
>         )
>         assert holder.wait(timeout=60) == 0 and follower.wait(timeout=60) == 0
>         holder_span, follower_span = _interval(one_holder_out), _interval(follower_out)
>         assert follower_span[0] >= holder_span[1] - 0.05, (
>             f"a setting-1 holder shared capacity: {holder_span} then {follower_span}"
>         )
>     
>         # a setting-1 head waiter on a free machine: it reserves at once, and a
>         # later setting-2 entry can only follow once the exclusive hold drains
>         log = tmp_path / "order.log"
>         names = {"PROBE_LOG": str(log), "PROBE_SLEEP": "0.3"}
>         first = _supervised(state, ORDER_BODY, {**names, "PROBE_NAME": "one", verify_lock.SLOTS_ENV: "1"})
> >       assert _wait_until(lambda: len(_records(state)) >= 1), "the setting-1 waiter never registered"
> E       AssertionError: the setting-1 waiter never registered
> E       assert False
> E        +  where False = _wait_until(<function test_slot_setting_and_capacity_reduction.<locals>.<lambda> at 0x11776bec0>)
>
> tests/test_verify_lock.py:1422: AssertionError
> ______________________ test_two_slot_fifo_and_dead_waiter ______________________
> [gw9] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/verify-two-slots/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3036/popen-gw9/test_two_slot_fifo_and_dead_wa0')
>
>     def test_two_slot_fifo_and_dead_waiter(tmp_path: Path) -> None:
>         """Criterion 4. Live waiters reserve in registration order; a dead waiter blocks nobody.
>     
>         Fault this pins: a later waiter overtaking a live earlier one, a dead
>         waiter blocking progress, or the eligible head unable to reserve the one
>         free slot within two queue polls after it frees up. One slot stays
>         occupied while the two waiters queue, so the head waiter takes the free
>         slot and the later waiter can only follow after the head's protected work
>         ends — the write order is the reservation order, never a race between two
>         nearly simultaneous starts.
>         """
>         state = tmp_path / "state"
>         log = tmp_path / "fifo.log"
>         body = {"PROBE_LOG": str(log)}
>     
>         with fake_slot_holder(state, 1):
>             # both slots occupied while the two waiters register: neither may reserve yet
>             with fake_slot_holder(state, 2):
>                 first = _supervised(state, ORDER_BODY, {**body, "PROBE_NAME": "first", "PROBE_SLEEP": "0.7"})
>                 assert _wait_until(lambda: len(_records(state)) >= 1), "the first waiter never registered"
>                 second = _supervised(state, ORDER_BODY, {**body, "PROBE_NAME": "second", "PROBE_SLEEP": "0.1"})
>                 assert _wait_until(lambda: len(_records(state)) >= 2), "the second waiter never registered"
>             # one slot freed: the head waiter takes it, and the later waiter can only
>             # follow once the head's protected work is done — the head was never overtaken
>             assert first.wait(timeout=60) == 0 and second.wait(timeout=60) == 0
>         order = log.read_text(encoding="utf-8").split()
>         assert order == ["first", "second"], f"admission left registration order: {order}"
>     
>         # a dead waiter's record is pruned and the next live head proceeds at once
>         dead_log = tmp_path / "dead.log"
>         with fake_holder(state):
>             doomed = _supervised(state, ORDER_BODY, {"PROBE_LOG": str(dead_log), "PROBE_NAME": "doomed"})
>             assert _wait_until(lambda: len(_records(state)) >= 1), "the doomed waiter never registered"
>             os.kill(doomed.pid, signal.SIGKILL)
>             doomed.wait(timeout=10)
>             survivor = _supervised(state, ORDER_BODY, {"PROBE_LOG": str(dead_log), "PROBE_NAME": "survivor"})
> >           assert _wait_until(lambda: len(_records(state)) >= 2), "the survivor never registered"
> E           AssertionError: the survivor never registered
> E           assert False
> E            +  where False = _wait_until(<function test_two_slot_fifo_and_dead_waiter.<locals>.<lambda> at 0x115723e20>)
>
> tests/test_verify_lock.py:1527: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_verify_lock.py::test_slot_setting_and_capacity_reduction - ...
> FAILED tests/test_verify_lock.py::test_two_slot_fifo_and_dead_waiter - Assert...
> 2 failed, 27 passed in 17.85s
> ```

Stage-2 call, 2026-11-21: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 1150 files, 5176 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_verify_lock.py` +10 -6
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> ..........................F..                                            [100%]
> =================================== FAILURES ===================================
> ___________________ test_slot_setting_and_capacity_reduction ___________________
> [gw9] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/verify-two-slots/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3037/popen-gw9/test_slot_setting_and_capacity0')
>
>     def test_slot_setting_and_capacity_reduction(tmp_path: Path) -> None:
>         """Criterion 2. A setting-`1` entry never shares capacity, as holder or as head waiter.
>     
>         Fault this pins: a `1` holder sharing the machine with another admission,
>         a head `1` waiter entering before all holders drain, or a mixed setting
>         ignoring a holder's or the head waiter's setting.
>         """
>         state = tmp_path / "state"
>     
>         # a setting-1 holder: a setting-2 follower must drain instead of taking the second slot
>         one_holder_out = tmp_path / "one-holder.json"
>         holder_started = tmp_path / "holder-started.json"
>         holder = _supervised(
>             state,
>             RECORD_BODY,
>             {
>                 "PROBE_OUT": str(one_holder_out),
>                 "PROBE_STARTED": str(holder_started),
>                 "PROBE_SLEEP": "1.0",
>                 verify_lock.SLOTS_ENV: "1",
>             },
>         )
>         assert _wait_until(holder_started.is_file), "the setting-1 holder never started its protected work"
>         follower_out = tmp_path / "two-follower.json"
>         follower = _supervised(state, RECORD_BODY, {"PROBE_OUT": str(follower_out), "PROBE_SLEEP": "0.1"})
>         assert not _wait_until(follower_out.is_file, 0.6), (
>             "a setting-2 follower reserved capacity beside a setting-1 holder"
>         )
>         assert holder.wait(timeout=60) == 0 and follower.wait(timeout=60) == 0
>         holder_span, follower_span = _interval(one_holder_out), _interval(follower_out)
>         assert follower_span[0] >= holder_span[1] - 0.05, (
>             f"a setting-1 holder shared capacity: {holder_span} then {follower_span}"
>         )
>     
>         # a setting-1 head waiter queues behind a live holder; a later setting-2
>         # entry cannot overtake it, and follows only once the exclusive hold drains
>         log = tmp_path / "order.log"
>         names = {"PROBE_LOG": str(log), "PROBE_SLEEP": "0.3"}
>         with fake_slot_holder(state, 1):
>             first = _supervised(state, ORDER_BODY, {**names, "PROBE_NAME": "one", verify_lock.SLOTS_ENV: "1"})
> >           assert _wait_until(lambda: len(_records(state)) >= 1), "the setting-1 waiter never registered"
> E           AssertionError: the setting-1 waiter never registered
> E           assert False
> E            +  where False = _wait_until(<function test_slot_setting_and_capacity_reduction.<locals>.<lambda> at 0x11500d620>)
>
> tests/test_verify_lock.py:1423: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_verify_lock.py::test_slot_setting_and_capacity_reduction - ...
> 1 failed, 28 passed in 17.74s
> ```

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model step-5-preview · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model step-5-preview · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model step-5-preview · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: review-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1150 files, 5179 commits, 12 rules.

Stage-2 call, 2026-11-21: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1150 files, 5184 commits, 12 rules.

Stage-2 call, 2026-11-21: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1150 files, 5184 commits, 12 rules.

Stage-2 call, 2026-11-21: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1150 files, 5184 commits, 12 rules.

Stage-2 call, 2026-11-21: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1150 files, 5199 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/orchestration.md` +6 -5
> - `scripts/verify_lock.py` +4 -2
> - `tests/test_verify_lock.py` +45 -15
>
> Diagnostics:
> ````text
> - lifecycle fields: plans/changes/verify-two-slots/plan.md, plans/changes/verify-two-slots/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: red) because the targeted coverage was not safe: `scripts/verify_lock.py` is shared execution infrastructure
> - `make verify` exited 1
> The gates that blocked, each with its last lines:
> ── [frontmatter-current] $ python3 scripts/check_frontmatter_current.py
> docs/WORKFLOW.md: stale — updated 2026-11-19 is older than its last change 2026-11-21 (8eb868dc)
> docs/governance/gate-catalog.md: stale — updated 2026-11-14 is older than its last change 2026-11-21 (8eb868dc)
> fix: python3 scripts/check_frontmatter_current.py --stamp
> ── [frontmatter-current] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 51177 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:20:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:21:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:25:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:25:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:25:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:27:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:30:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:31:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:40:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:45:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:46:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:69:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:134:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:134:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:134:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:135:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:136:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:137:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/verify-two-slots/stage2/attempts/verify-two-slots/attempt-1-20261121T171110154894Z-ee330d01.md
> ````

Stage-2 call, 2026-11-21: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason first Codex post-run check failed · leak check clean over 1150 files, 5202 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/verify_lock.py` +20 -9
> - `tests/test_verify_lock.py` +28 -0
>
> Diagnostics:
> ````text
> - lifecycle fields: plans/changes/verify-two-slots/plan.md, plans/changes/verify-two-slots/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: red) because the targeted coverage was not safe: `scripts/verify_lock.py` is shared execution infrastructure
> - `make verify` exited 1
> The gates that blocked, each with its last lines:
> ── [frontmatter-current] $ python3 scripts/check_frontmatter_current.py
> docs/WORKFLOW.md: stale — updated 2026-11-19 is older than its last change 2026-11-21 (8eb868dc)
> docs/governance/gate-catalog.md: stale — updated 2026-11-14 is older than its last change 2026-11-21 (8eb868dc)
> fix: python3 scripts/check_frontmatter_current.py --stamp
> ── [frontmatter-current] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 51225 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:20:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:21:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:25:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:25:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:25:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:27:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:30:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:31:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:40:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:45:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:46:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:69:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:134:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:134:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:134:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:135:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:136:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:137:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/verify-two-slots/stage2/attempts/verify-two-slots/attempt-2-20261121T171110154894Z-ee330d01.md
> ````

Stage-2 call, 2026-11-21: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 1150 files, 5206 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/verify_lock.py` +7 -4
> - `tests/test_verify_lock.py` +4 -0
>
> Diagnostics:
> ````text
> - lifecycle fields: plans/changes/verify-two-slots/plan.md, plans/changes/verify-two-slots/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: red) because the targeted coverage was not safe: `scripts/verify_lock.py` is shared execution infrastructure
> - `make verify` exited 1
> The gates that blocked, each with its last lines:
> ── [frontmatter-current] $ python3 scripts/check_frontmatter_current.py
> docs/WORKFLOW.md: stale — updated 2026-11-19 is older than its last change 2026-11-21 (8eb868dc)
> docs/governance/gate-catalog.md: stale — updated 2026-11-14 is older than its last change 2026-11-21 (8eb868dc)
> fix: python3 scripts/check_frontmatter_current.py --stamp
> ── [frontmatter-current] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 51275 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:20:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:21:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:25:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:25:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:25:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:27:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:30:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:31:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:40:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:45:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:46:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:69:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:134:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:134:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:134:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:135:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:136:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:137:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/verify-two-slots/stage2/attempts/verify-two-slots/attempt-3-20261121T171110154894Z-ee330d01.md
> ````

Stage-2 call, 2026-11-21: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1150 files, 5210 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/orchestration.md` +3 -3
> - `scripts/verify_lock.py` +22 -9
> - `tests/test_verify_lock.py` +61 -15
>
> Diagnostics:
> ````text
> - lifecycle fields: plans/changes/verify-two-slots/plan.md, plans/changes/verify-two-slots/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: red) because the targeted coverage was not safe: `scripts/verify_lock.py` is shared execution infrastructure
> - `make verify` exited 1
> The gates that blocked, each with its last lines:
> ── [pytest] $ python3 -m pytest tests/ -q -n auto
> [… 153 lines of this gate left out …]
>             # The queue entry proves the scheduler is past the cheap phase and waiting; it stays there
>             # for a real second before the holder lets go.
>             queue = world.state / "coding-harness" / verify_lock.QUEUE_DIR
>             deadline = time.monotonic() + 60
>             while time.monotonic() < deadline and not (queue.is_dir() and any(queue.iterdir())):
>                 time.sleep(0.02)
>             time.sleep(1.0)
>             holder.terminate()
>     
>         monkeypatch.setattr(stage2, "VERIFY_SECONDS", 30.0)
>         monkeypatch.setattr(stage2, "launch", launch)
>         _real_gate_shell(monkeypatch)
>         monkeypatch.setattr(stage2.verify_lock, "hold_admission", hold_admission)
>         releaser = threading.Thread(target=release_when_queued)
>         releaser.start()
>         try:
>             _holder_acquired(ready)
>             uncovered_implementation(world)
>             assert world.run("implement") == 0, "the queue wait starved the shared allowance"
>             assert marker.read_text(encoding="utf-8").strip() == "done"
>         finally:
>             releaser.join(timeout=90)
>             if holder.poll() is None:
>                 holder.kill()
>                 holder.wait(timeout=10)
>     
>         # Three gate launches: the slow cheap gate, the document subset, then the protected full check.
>         assert len(deadlines) == 3, deadlines
> >       assert len(waits) == 1 and waits[0] > 0.8, waits
> E       AssertionError: [0.004682332975789905]
> E       assert (1 == 1 and 0.004682332975789905 > 0.8)
> E        +  where 1 = len([0.004682332975789905])
>
> tests/test_stage2.py:2953: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 31 files, 3 commits, 1 rules, 1 prompt texts
> implement: verified and committed · route flash · attempt 1
> ----------------------------- Captured stderr call -----------------------------
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=64698) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/verify-two-slots/tests/test_stage2.py:24185: DeprecationWarning: This process (pid=64704) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_before_admission_execution_budget_is_shared_and_wait_free
> 1 failed, 6587 passed, 17 skipped, 5 warnings in 654.02s (0:10:54)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 51319 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:20:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:21:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:25:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:25:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:25:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:27:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:30:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:31:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:40:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:45:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:46:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:69:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:134:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:134:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:134:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:135:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:136:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:137:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/verify-two-slots/stage2/attempts/verify-two-slots/attempt-1-20261121T171854828448Z-01f0fa3a.md
> ````

Stage-2 call, 2026-11-21: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason first Codex post-run check failed · leak check clean over 1150 files, 5226 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/verify-two-slots/plan.md, plans/changes/verify-two-slots/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - no work done: the attempt left no model work after runner bookkeeping, derived preparation and formatting; repair the taken rows of the loop record
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>                 # The world's PATH holds only the stand-ins and git, so `sleep` is named by its path.
>                 "command": f"/bin/sleep 1.5 && echo done > {marker}",
>                 "enforcement": "block",
>                 "cost": "seconds",
>                 "floor": True,
>                 "needs_tracker": False,
>                 "needs_history": False,
>                 "placement": "both",
>                 "reason": "The cheap gate whose active seconds the shared allowance must survive.",
>             },
>         )
>         datei.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
>         git(world.root, "add", "-A")
>         git(world.root, "commit", "--quiet", "-m", "a slow cheap gate joins the verify job")
>     
>         ready = world.state / "holder-ready-budget"
>         holder = _real_holder(ready, seconds=30.0)
>         deadlines: list[float] = []
>         waits: list[float] = []
>         real_launch = stage2.launch
>         real_hold = stage2.verify_lock.hold_admission
>     
>         def launch(command, root, env, *rest, **kwargs):
>             if _gate_launch(command) is not None:
>                 deadlines.append(kwargs.get("deadline"))
>             return real_launch(command, root, env, *rest, **kwargs)
>     
>         @contextlib.contextmanager
>         def hold_admission(command):
>             # The wait happens when the admission is entered, not when it is requested.
>             entered = time.monotonic()
>             with real_hold(command) as owned:
>                 waits.append(time.monotonic() - entered)
>                 yield owned
>     
>         def release_when_queued() -> None:
>             # The queue entry proves the scheduler is past the cheap phase and waiting; it stays there
>             # for a real second before the holder lets go.
>             queue = world.state / "coding-harness" / verify_lock.QUEUE_DIR
>             deadline = time.monotonic() + 60
>             while time.monotonic() < deadline and not (queue.is_dir() and any(queue.iterdir())):
>                 time.sleep(0.02)
>             time.sleep(1.0)
>             holder.terminate()
>     
>         monkeypatch.setattr(stage2, "VERIFY_SECONDS", 30.0)
>         monkeypatch.setattr(stage2, "launch", launch)
>         _real_gate_shell(monkeypatch)
>         monkeypatch.setattr(stage2.verify_lock, "hold_admission", hold_admission)
>         releaser = threading.Thread(target=release_when_queued)
>         releaser.start()
>         try:
>             _holder_acquired(ready)
>             uncovered_implementation(world)
>             assert world.run("implement") == 0, "the queue wait starved the shared allowance"
>             assert marker.read_text(encoding="utf-8").strip() == "done"
>         finally:
>             releaser.join(timeout=90)
>             if holder.poll() is None:
>                 holder.kill()
>                 holder.wait(timeout=10)
>     
>         # Three gate launches: the slow cheap gate, the document subset, then the protected full check.
>         assert len(deadlines) == 3, deadlines
> >       assert len(waits) == 1 and waits[0] > 0.8, waits
> E       AssertionError: [0.0033052919898182154]
> E       assert (1 == 1 and 0.0033052919898182154 > 0.8)
> E        +  where 1 = len([0.0033052919898182154])
>
> tests/test_stage2.py:2953: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 31 files, 3 commits, 1 rules, 1 prompt texts
> implement: verified and committed · route flash · attempt 1
> ----------------------------- Captured stderr call -----------------------------
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_before_admission_execution_budget_is_shared_and_wait_free
> 1 failed, 15 passed in 69.15s (0:01:09)
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/verify-two-slots/stage2/attempts/verify-two-slots/attempt-2-20261121T171854828448Z-01f0fa3a.md
> ```

Stage-2 call, 2026-11-21: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 1150 files, 5227 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/verify_lock.py` +4 -0
> - `tests/test_verify_lock.py` +7 -5
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/verify-two-slots/plan.md, plans/changes/verify-two-slots/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>                 # The world's PATH holds only the stand-ins and git, so `sleep` is named by its path.
>                 "command": f"/bin/sleep 1.5 && echo done > {marker}",
>                 "enforcement": "block",
>                 "cost": "seconds",
>                 "floor": True,
>                 "needs_tracker": False,
>                 "needs_history": False,
>                 "placement": "both",
>                 "reason": "The cheap gate whose active seconds the shared allowance must survive.",
>             },
>         )
>         datei.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
>         git(world.root, "add", "-A")
>         git(world.root, "commit", "--quiet", "-m", "a slow cheap gate joins the verify job")
>     
>         ready = world.state / "holder-ready-budget"
>         holder = _real_holder(ready, seconds=30.0)
>         deadlines: list[float] = []
>         waits: list[float] = []
>         real_launch = stage2.launch
>         real_hold = stage2.verify_lock.hold_admission
>     
>         def launch(command, root, env, *rest, **kwargs):
>             if _gate_launch(command) is not None:
>                 deadlines.append(kwargs.get("deadline"))
>             return real_launch(command, root, env, *rest, **kwargs)
>     
>         @contextlib.contextmanager
>         def hold_admission(command):
>             # The wait happens when the admission is entered, not when it is requested.
>             entered = time.monotonic()
>             with real_hold(command) as owned:
>                 waits.append(time.monotonic() - entered)
>                 yield owned
>     
>         def release_when_queued() -> None:
>             # The queue entry proves the scheduler is past the cheap phase and waiting; it stays there
>             # for a real second before the holder lets go.
>             queue = world.state / "coding-harness" / verify_lock.QUEUE_DIR
>             deadline = time.monotonic() + 60
>             while time.monotonic() < deadline and not (queue.is_dir() and any(queue.iterdir())):
>                 time.sleep(0.02)
>             time.sleep(1.0)
>             holder.terminate()
>     
>         monkeypatch.setattr(stage2, "VERIFY_SECONDS", 30.0)
>         monkeypatch.setattr(stage2, "launch", launch)
>         _real_gate_shell(monkeypatch)
>         monkeypatch.setattr(stage2.verify_lock, "hold_admission", hold_admission)
>         releaser = threading.Thread(target=release_when_queued)
>         releaser.start()
>         try:
>             _holder_acquired(ready)
>             uncovered_implementation(world)
>             assert world.run("implement") == 0, "the queue wait starved the shared allowance"
>             assert marker.read_text(encoding="utf-8").strip() == "done"
>         finally:
>             releaser.join(timeout=90)
>             if holder.poll() is None:
>                 holder.kill()
>                 holder.wait(timeout=10)
>     
>         # Three gate launches: the slow cheap gate, the document subset, then the protected full check.
>         assert len(deadlines) == 3, deadlines
> >       assert len(waits) == 1 and waits[0] > 0.8, waits
> E       AssertionError: [0.0027734999312087893]
> E       assert (1 == 1 and 0.0027734999312087893 > 0.8)
> E        +  where 1 = len([0.0027734999312087893])
>
> tests/test_stage2.py:2953: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 31 files, 3 commits, 1 rules, 1 prompt texts
> implement: verified and committed · route flash · attempt 1
> ----------------------------- Captured stderr call -----------------------------
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_before_admission_execution_budget_is_shared_and_wait_free
> 1 failed, 15 passed in 68.92s (0:01:08)
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/verify-two-slots/stage2/attempts/verify-two-slots/attempt-3-20261121T171854828448Z-01f0fa3a.md
> ```

Stage-2 call, 2026-11-21: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1150 files, 5239 commits, 12 rules.

Runner restoration, 2026-11-21: repair · attempt 1 · route codex — lifecycle fields: plans/changes/verify-two-slots/plan.md, plans/changes/verify-two-slots/spec.md — unchanged

Stage-2 call, 2026-11-21: review-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1150 files, 5266 commits, 12 rules.

Stage-2 call, 2026-11-22: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1150 files, 5300 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +7 -2
> - `docs/orchestration.md` +5 -1
> - `scripts/verify_lock.py` +13 -12
> - `tests/test_verify_lock.py` +106 -52
>
> Diagnostics:
> ````text
> - lifecycle fields: plans/changes/verify-two-slots/plan.md, plans/changes/verify-two-slots/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: red) because the targeted coverage was not safe: `scripts/verify_lock.py` is shared execution infrastructure
> - `make verify` exited 1
> The gates that blocked, each with its last lines:
> ── [leerprobe] $ python3 scripts/kit/probe.py --strict
> BLOCK (1):
>   - 1 red case(s) without a declared reason
>       tests.test_verify_lock::test_legacy_exclusive_lock_excludes_both_slots
>       
>       Add them with: python3 scripts/kit/probe.py --messen
>
> INFO  (1):
>   - 1582 of 1627 cases carry into a foreign repository (97 %)
>       mechanismus 116 · bestand 1034 file(s)
>
> BLOCK (1), repeated last:
>   - 1 red case(s) without a declared reason
> ── [leerprobe] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 51395 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:20:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:21:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:25:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:25:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:25:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:27:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:30:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:31:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:40:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:45:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:46:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:69:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:134:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:134:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:134:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:135:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:136:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:137:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/verify-two-slots/stage2/attempts/verify-two-slots/attempt-1-20261122T032046245593Z-2aa9d4cf.md
> ````

Stage-2 call, 2026-11-22: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason first Codex post-run check failed · leak check clean over 1150 files, 5320 commits, 12 rules.

Runner restoration, 2026-11-22: repair · attempt 2 · route codex-repair — lifecycle fields: plans/changes/verify-two-slots/plan.md, plans/changes/verify-two-slots/spec.md — unchanged

## Phase 6 — Opus 5.5, 2026-11-22

Reviewer: Opus 5.5 through Claude Code's read-only `reviewer` agent at HEAD `bec58b9c`, because Codex is usage-limited until 2026-11-23 16:40; the maintainer allowed it on 2026-11-22 ("Ich erlaube dir alle offenen Phase 6 Schritte mit Opus zu machen"). The reviewer had Read, Grep and Glob only and ran no command. Its rows are recorded unchanged.

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| O6-1 | BLOCKER | TEST | base | tests/test_verify_lock.py | `test_legacy_exclusive_lock_excludes_both_slots` gets its "older checkout" by running `git show origin/main:scripts/verify_lock.py` (line 1842). Today that ref is the single-slot base, so the test passes; once this branch merges, `origin/main` holds the two-slot code: the "old" holder (default setting 2) reserves slot 1, the newcomer reserves slot 2 at once, and `assert not _wait_until(newcomer_out.is_file, 0.7)` fails every time, so `make verify` on `main` turns red; the second half's order assertion turns flaky; without `origin/main` the test skips and criterion 10 has no coverage. Pin a fixed pre-change revision (the merge base 3b8a1ccf) instead of a moving ref. [10] | Opus 5.5 | fixed — guard test — tests/test_verify_lock.py::test_legacy_exclusive_lock_excludes_both_slots | — |
| O6-2 | MAJOR | TEST | base | scripts/verify_lock.py | Criterion 2's second paragraph has no regression: local child processes receive `HARNESS_VERIFY_SLOTS` and the foreign-model allow-list stays closed to `HARNESS_*`. No test reads `SLOTS_ENV` in `inherit_env` output; deleting lines 1145-1146, or adding `HARNESS_VERIFY_SLOTS` to `ENV_ALLOW` in `scripts/stage2.py`, leaves every test green. The plan asks `tests/test_stage2.py` to check that the full and targeted runner paths keep the setting. [2] | Opus 5.5 | fixed — guard test — tests/test_verify_lock.py::test_slot_setting_reaches_local_children_not_foreign_calls | — |
| O6-3 | MINOR | TEST | base | tests/test_verify_duration.py | `test_two_slot_context_does_not_mix_holder_waits` calls `verify_duration.record_end` twice with an explicit `AdmissionContext` the test supplies; it starts no admission, publishes no holder record and never runs `admission_context()`. A fault where context resolution returns the peer's slot record, or one holder overwrites the other's record, keeps it green. [11] | Opus 5.5 | fixed — guard test — tests/test_verify_duration.py::test_two_slot_context_does_not_mix_holder_waits | — |
| O6-4 | MINOR | SPEC | base | scripts/verify_lock.py | When a setting-1 supervisor is SIGKILLed while its child holds `verify.lock`, `verify.holder.exclusive.json` stays behind; if an older-checkout waiter then takes `verify.lock` exclusively before any updated waiter prunes, `_prune_stale_holders_locked` keeps the stale record and `_describe_occupancy` (lines 423-426) prefers it over `read_holder`, so every wait log names the dead holder and leaves out the live legacy holder. [9] | Opus 5.5 | rejected — known MINOR limit, recorded: only a wait-log description is wrong, in the rare case of a SIGKILLed setting-1 supervisor followed by an older-checkout holder; admission itself stays correct. A fix touches scripts/ and would void the criterion-12 trial (about 70 minutes of the one verify slot); follow-up bead instead; decided by the orchestrator | — |
| O6-5 | MINOR | SPEC | base | plans/changes/verify-two-slots/measurements.md | The admission observation is a 5-second holder-record sample, not per-admission intervals, and the queue was not sampled, so a contending third waiter or a sub-5-second admission could be missed; the raw evidence sits only in a session scratchpad; the post-trial commit bec58b9c is not listed as a later plans-only change and the `scripts/` diff check is stated as "at recording" only. [12] | Opus 5.5 | fixed — not a test — orchestrator hand edit (this commit) of measurements.md: state the 5-second sampling limit and the unsampled queue plainly, list the later plans-only commits; no rerun (limit recorded, not hidden) | — |
| O6-6 | MINOR | MAINT | base | docs/WORKFLOW.md | Four living docs date the new behaviour "since 2026-11-21" or "Until 2026-11-21" (`docs/WORKFLOW.md`, `docs/orchestration.md`, `docs/how-it-works.md`, `docs/governance/gate-catalog.md`); the change is unmerged on 2026-11-22, so on `main` the date would be false. [DoD, living docs] | Opus 5.5 | fixed — not a test — dated the four living docs by the change (bead coding-harness-u1ha) instead of 2026-11-21 | — |

Stage-2 call, 2026-11-22: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1150 files, 5372 commits, 12 rules.

Runner restoration, 2026-11-22: repair · attempt 1 · route codex — lifecycle fields: plans/changes/verify-two-slots/plan.md, plans/changes/verify-two-slots/spec.md — unchanged

Stage-2 call, 2026-11-22: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1150 files, 5373 commits, 12 rules.

Runner restoration, 2026-11-22: repair · attempt 1 · route codex — lifecycle fields: plans/changes/verify-two-slots/plan.md, plans/changes/verify-two-slots/spec.md — unchanged

Stage-2 call, 2026-11-22: repair · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Codex usage-limited until 2026-11-23 16:40; maintainer: repairs to Sonnet meanwhile · leak check clean over 1150 files, 5374 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +2 -2
> - `docs/governance/gate-catalog.md` +2 -2
> - `docs/how-it-works.md` +3 -3
> - `docs/orchestration.md` +3 -3
> - `tests/test_verify_duration.py` +106 -53
> - `tests/test_verify_lock.py` +37 -4
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/verify-two-slots/plan.md, plans/changes/verify-two-slots/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: targeted verification, not the full `make verify`; result: green; test files `tests/test_check_criterion_ledger.py`, `tests/test_check_interview_minimums.py`, `tests/test_check_question_context.py`, `tests/test_explorer_reviewer_agents.py`, `tests/test_frontmatter_current.py`, `tests/test_gate_catalog.py`, `tests/test_kit.py`, `tests/test_leakcheck.py`, `tests/test_model_endpoints.py`, `tests/test_outcome_test.py`, `tests/test_stage2_session.py`, `tests/test_stage2_swarm.py`, `tests/test_templates.py`, `tests/test_verify_duration.py`, `tests/test_verify_lock.py`, `tests/test_workflow_entry.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6
> - O6-1: tests/test_verify_lock.py::test_legacy_exclusive_lock_excludes_both_slots: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure or pytest's own failed outcome
> - O6-2: tests/test_verify_lock.py::test_slot_setting_reaches_local_children_but_not_foreign_calls: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure or pytest's own failed outcome
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/verify-two-slots/stage2/attempts/verify-two-slots/attempt-1-20261122T152101425315Z-054daf7c.md
> ```

Stage-2 call, 2026-11-22: repair · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Codex usage-limited until 2026-11-23 16:40; maintainer: repairs to Sonnet meanwhile · leak check clean over 1150 files, 5377 commits, 12 rules.

Runner restoration, 2026-11-22: repair · attempt 1 · route stage-1 — lifecycle fields: plans/changes/verify-two-slots/plan.md, plans/changes/verify-two-slots/spec.md — unchanged

## Phase 6 — Opus 5.5, 2026-11-22 (re-check of O6-1..O6-6)

Re-check by Opus 5.5 through Claude Code's read-only `reviewer` agent at HEAD `8628bd1b` (maintainer permission of 2026-11-22). Verdict on the repaired rows: O6-1 fixed (`tests/test_verify_lock.py:32` pins `3b8a1ccf`, `:1852-1859`, no skip), O6-2 fixed (`tests/test_verify_lock.py:1909-1933`), O6-6 fixed (no "2026-11-21" in the four docs), O6-3 uses real admissions but see O6R-1 and O6R-2. Its rows are recorded unchanged; O6R-3 is the orchestrator's, from the full `make verify` of 2026-11-22 at `8628bd1b` (pytest green, 6592 passed; `leerprobe` red).

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| O6R-1 | MINOR | TEST | fix-r1 | tests/test_verify_duration.py | The rewrite left assertions and docstring claims that test nothing: lines 2461-2462 assert that `"wait: 3.5"`, `"wait: 99.0"` and `"peer-env"` are absent from the report, but nothing in the rewritten test produces those values; the docstring (2361-2363) claims the test pins "a later holder's context overwrites an earlier holder's record" and "the stale environment of an overlapping admission speaks for either run", yet no supervisor gets a stale `HARNESS_VERIFY_ADMISSION_ID` and no holder record is read. Fix: drop the dead assertions, or restore the stale-environment case (one supervisor started with a stale `HARNESS_VERIFY_ADMISSION_ID`=peer-env, asserted never to reach the run's record), and align the docstring. | Opus 5.5 | fixed — not a test — dropped the dead assertions and aligned the docstring with what the test plants | unknown |
| O6R-2 | MINOR | TEST | base | tests/test_verify_duration.py | O6-3 is only partly covered: both children resolve their context through the supervisor's environment (`scripts/verify_lock.py:1238` sets `HARNESS_VERIFY_ADMISSION_ID`; `admission_context()` returns at 685-687 before `_nested_record()` at 688), so the record-based path with two holders live is never reached and the `SLOT_HOLDER_NAMES` records are never read. Fix: in each child, run a nested descendant with `inherit_env` (which drops the fresh id) and assert it resolves its own ancestor's admission_id with reused=True, never the peer's. | Opus 5.5 | fixed — guard test — tests/test_verify_duration.py::test_two_slot_context_does_not_mix_holder_waits | unknown |
| O6R-3 | MAJOR | TEST | fix-r1 | tests/test_verify_lock.py | The full `make verify` at `8628bd1b` is red on the blocking `leerprobe` gate: "2 red case(s) without a declared reason" — `test_legacy_exclusive_lock_excludes_both_slots` (needs this repository's revision 3b8a1ccf, absent in the kit's throwaway repo) and `test_slot_setting_reaches_local_children_not_foreign_calls` (reads `scripts/stage2.py`, which the kit does not carry). Declaring them in `scripts/kit/probe.py` REIST_NICHT is not enough on its own: the two case names add the phase word "verify" and `tests/test_kit.py::test_the_kit_does_not_describe_the_phases` then counts five phase names in probe.py. Fix: make both cases carry — the older checkout's single-slot module as a committed test fixture instead of `git show <revision>`, and the allow-list check reading the runner only where it exists with the kit's own reason otherwise — or another way that leaves `leerprobe` and `tests/test_kit.py` green. | orchestrator (Opus 5.5) | fixed — guard test — tests/test_verify_lock.py::test_legacy_exclusive_lock_excludes_both_slots | unknown |

Stage-2 call, 2026-11-22: repair · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Codex usage-limited until 2026-11-23 16:40; maintainer: repairs to Sonnet meanwhile · leak check clean over 1150 files, 5386 commits, 12 rules.

Runner restoration, 2026-11-22: repair · attempt 1 · route stage-1 — lifecycle fields: plans/changes/verify-two-slots/plan.md, plans/changes/verify-two-slots/spec.md — unchanged
