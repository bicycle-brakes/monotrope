---
title: "Research — flaky-popen-signal"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-oag7
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-21", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# flaky popen signal — Research

Stage-2 call, 2026-11-21: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1149 files, 5142 commits, 12 rules.

## Runner exploration — 2026-11-21

Research complete. Here is the prose, ready to append to `plans/changes/flaky-popen-signal/research.md`:

---

## What exists today — the flake reports behind bead coding-harness-oag7

The change's tracker entry is bead `coding-harness-oag7`; the research skeleton names it in its frontmatter (`plans/changes/flaky-popen-signal/research.md`, field `bead:`) and `plans/INDEX.md` carries the row (draft, implementation status none, dated 2026-11-21, `plans/INDEX.md:600`). The bead's own notes live in the Dolt tracker under `.beads/` and were **not read**: the tracker is a database my read-only file tools cannot open, and no rendered copy is committed (repository house rule 2). The branch `fix/flaky-popen-signal` exists with one commit, `d9bc9e6b` "chore(flaky-popen-signal): open change folder for coding-harness-oag7"; the folder holds only `research.md` — no `spec.md`, `decisions.md` or `plan.md` yet.

Two CI flake observations are written down in committed handovers, and one named test:

- 2026-11-16: PR #404's first CI run went red on `test_an_interrupt_on_the_main_thread_kills_the_launched_group[Terminated]`, described there as "a flaky test that is not the leak test the PR fixed"; the PR merged after a rerun (`docs/journal/handover/2026-11-16-day-six-lanes.md`, section "Validation", lines 155–157).
- 2026-11-20: "A second flaky interrupt test failed once in CI on #419 (noted on bead coding-harness-oag7)"; the validation section records "#419 (after one rerun of a flaky interrupt test)" as green and merged (`docs/journal/handover/2026-11-20-day-run.md`, lines 116–117 and 145–146). **The handover does not name which test failed** — that fact lives only in the bead notes or the CI run logs, both unread here.
- PR #419 itself was a text/rules change (the "exhausted review ladder goes to phase 6" AGENTS.md rule, `docs/journal/handover/2026-11-20-day-run.md:30`), so its red came from the unmodified suite on Linux CI.

The failing test named on 2026-11-16 is `test_an_interrupt_on_the_main_thread_kills_the_launched_group` (`tests/test_stage2.py:26515–26571`), parametrized over `[KeyboardInterrupt, stage2.Terminated]`. It monkeypatches `subprocess.Popen.communicate` to raise after a handshake proves the launched group's descendant is running (heartbeat file plus pidfile, watchdog at 1500×0.02 s), runs `world.run("explore")`, and demands the descendant's pid disappear (liveness poll, 300×0.02 s, `_child_alive`) and the group leader be reaped. Its `finally` cleanup `killpg`s the leader suppressing only `ProcessLookupError` (`tests/test_stage2.py:26567–26571`).

A concrete failure mechanism in the same test family is already on record, twice: `test_a_signal_during_process_creation_leaves_no_child[False-SIGTERM]` failed with `PermissionError: [Errno 1] Operation not permitted` raised by the test's own cleanup `os.killpg(pid, signal.SIGKILL)` — first in the go-access-point lane (attempt diagnostics in `plans/changes/archive/2026-11-06-go-access-point/findings.md`, lines ~170–208, stderr "terminated: the run stopped; 1 running program group(s) killed."), then again in repair-targeted-check (`plans/changes/archive/2026-11-16-repair-targeted-check/findings.md`, lines ~37–77, stderr "0 running program group(s) killed."), both on 2026-10-31, darwin, full suite `-n auto`. The current cleanup of that test suppresses `ProcessLookupError` and `ChildProcessError` but not `PermissionError` or `OSError` (`tests/test_stage2.py:26923–26931`). Per POSIX semantics an `EPERM` from `killpg` means the group still exists but this process may not signal it — a fact from the backtraces; *why* the group is unsignalable (pid/group-id reuse under load being the candidate) is an open question, not established. That pid reuse is a known hazard in this suite is documented in the helper `_reaped_pid` (`tests/test_ci.py:2611–2624`): "A concurrently spawning process could take the freed pid back in between; when that happened the caller would inject a live process's number".

## What exists today — the production machinery the flaky tests exercise

- `scripts/stage2.py:963–968` — `_LIVE_GROUPS` (set of running timed programs' group ids) with `_LIVE_LOCK` and `_LAUNCH_STOPPED`; `KILL_DRAIN_SECONDS = 5`.
- `kill_live()` (`scripts/stage2.py:971–979`) sets `_LAUNCH_STOPPED`, then `killpg(SIGKILL)`s every registered group.
- `TERMINATING_SIGNALS = (SIGTERM, SIGHUP, SIGQUIT)` (`scripts/stage2.py:984`); the `Terminated` exception carries the signum and means exit 128+signum, 143 for SIGTERM (`scripts/stage2.py:987–993`).
- `defer_launch_signals()` (`scripts/stage2.py:996–1017`) — the fix for the original race: on the main thread only, it installs record-and-pending handlers for SIGINT and the terminating signals around `Popen`, restores the previous handlers afterwards, then re-raises each pending signal with `signal.raise_signal`. Its docstring records why `pthread_sigmask` was rejected (the blocked mask would pass into the child).
- `launch()` (`scripts/stage2.py:1025–1108`) — with a timeout or deadline it `Popen`s with `start_new_session=True`, registers `process.pid` in `_LIVE_GROUPS` under `_LIVE_LOCK` (`1069–1081`), refuses to start when `_LAUNCH_STOPPED` is set before or after creation (`1061–1062`, `1083–1084`), ends leftovers through `verify_lock.end_lingering_group` (`1088`, review row F6-5), and on any `BaseException` kills the group first, then drains bounded by `KILL_DRAIN_SECONDS` (`1089–1097`). Main installs the termination handlers at `scripts/stage2.py:11538–11556`; the tests assert the handler does not leak past main (`tests/test_stage2.py:23487`, `23516`).
- The verify runner has a parallel copy of the same pattern for gate processes: `_hold_launch_signals()` (`scripts/verify_run.py:453–471`, explicitly "in the same form of the runner's `defer_launch_signals`", row F6-3 cited at `506–509`) and the `interrupted()` handler that SIGTERMs then SIGKILLs live gate groups (`scripts/verify_run.py:584–607`). `verify_lock.end_lingering_group(group)` (`scripts/verify_lock.py:905–923`) sends SIGTERM then SIGKILL, each suppressing `OSError`, with a bounded wait polling `_group_alive`.
- The test family: `test_an_interrupted_runner_kills_its_running_programs` (`tests/test_stage2.py:23449–23463`, criterion DL-B-5), `test_a_terminated_runner_kills_its_running_programs` (`23466–23487`), `test_a_hangup_or_quit_kills_the_running_programs_like_sigterm` (`23490–23516`, marked "Phase-6 row F6-8" for SIGHUP/SIGQUIT), `test_a_timeout_does_not_wait_for_an_escaped_descendant` (`23519–23560`, DL-B-6, monkeypatches `KILL_DRAIN_SECONDS` to 0.5), `test_a_timeout_kills_the_whole_process_group` (`~7500–7547`), `test_a_launch_after_the_interrupt_starts_no_program` (`26574–26607`), and `test_a_signal_during_process_creation_leaves_no_child` (`26879–26933`, parametrized SIGTERM/SIGINT × main-thread/worker). Shared helpers: `_child_alive` (`tests/test_stage2.py:23407–23419` — `kill(pid, 0)`, with a Linux `/proc/<pid>/stat` zombie check; on macOS any `/proc` read error counts as alive) and `_interrupting_verb` (`23422–23446` — launches `sh -c 'echo $$ > pidfile; exec sleep 30'` in a thread through `stage2.launch`, bounded wait, then interrupts).
- `test_a_signal_during_process_creation_leaves_no_child` originates in review-loop-deep-b phase-6 row F6-8 (`plans/changes/archive/2026-11-06-review-loop-deep-b/findings.md:426`): a real SIGTERM delivered after `_fork_exec` created the child but before `Popen` returned left the timed program running because `process` was still `None` and no group was registered; fixed in `scripts/stage2.py` and pinned by the test. The DL-B-5/DL-B-6 criteria themselves come from the cloud-runner review (`docs/journal/handover/2026-10-25-cloud-runner-fixes.md:478–481`: an interrupted runner left reviewers running; fix = a table of live pids, `killpg` each on KeyboardInterrupt/SIGTERM).
- The CI environment where both 2026-11 flakes happened: `.github/workflows/ci.yml` step `pytest` runs `python3 -m pytest tests/ -q -n auto` on `ubuntu-latest` (`ci.yml:27` and `ci.yml:82`). The 2026-10-31 `PermissionError` observations, by contrast, are darwin worktree runs recorded in the two archived findings files.
- `test_verify_runner_cleans_on_interrupt` (`tests/test_ci.py:2763–2811`, parametrized SIGINT/SIGTERM/SIGHUP/SIGQUIT) signals the runner (`scripts/verify_all.sh`, started as its own session leader by `_start_runner`, `tests/test_ci.py:2587–2598`) only while the second gate is inside its sleep, "so the arrival is deterministic"; its comment cites bead coding-harness-bxxt.6 (the wrapper forwards the signal to the scheduler, which kills the live gate group).

## What is unclear (open questions, not guesses)

- **Which test failed on PR #419** (2026-11-20): the handover names no test; the answer is in bead `coding-harness-oag7`'s notes (Dolt tracker, not read) or the CI run log (not read). Everything above about that failure is its written trace only.
- **What the failure mode of each CI flake was** (assertion vs. cleanup exception): the #419 log and #404's run log are not read; the only recorded failure modes are the 2026-10-31 `PermissionError` backtraces quoted in the archived findings.
- **Why `killpg` returned EPERM** on 2026-10-31: the error is recorded; its cause (group-id/pid reuse, a still-alive unkillable member, or another mechanism) is not established by any committed text.
- **Whether `defer_launch_signals`' re-raise of pending signals can itself lose a signal** when the restore and the `raise_signal` sequence races a second arriving signal: no committed text discusses it; the code is `scripts/stage2.py:1013–1017`. This is a question for the interview or a test, not an established fault.
- **No committed policy for handling flaky tests was found** — the only "flaky" rule in `docs/` is the slip-counter report contract's sentence "A full green immediately followed by a full red of one identity is reported separately as a flaky-test signal" (`docs/WORKFLOW.md:647–649`). Search was a case-insensitive grep for "flaky|flake" across `docs/` on 2026-11-21; nothing outside handover prose and that sentence matched.

## Neighbouring work (already known)

- `plans/changes/flaky-swarm-leak-test/` (bead coding-harness-yb1l) — the previous flaky-test change: the swarm torn-log flake, fixed and reviewed (four loop rounds plus phase 6, `findings.md` rows L1-1…L4-3); its row L3-1 records that the natural CI flake was never reproduced and the criterion allowed a forced reproduction.
- `plans/changes/slip-counter/` — the change whose report contract defines the flaky-test signal (`docs/WORKFLOW.md:647–649`); merged per `docs/journal/handover/2026-11-20-day-run.md:139–140`, folder not yet archived.
- A distinct, unrepaired timing flake: `test_before_admission_execution_budget_is_shared_and_wait_free` (tests in `tests/test_verify_before_admission.py`), hit 2026-11-17 and "not investigated" (`docs/journal/handover/2026-11-18-night-run-2026-11-17-a.md:75`) — same suite, different family (verify admission budget, not Popen/signals).
- Bead coding-harness-bxxt.6 (cited in `tests/test_ci.py:2798–2801`) — the earlier fix that made the verify runner's wrapper forward signals so the live gate group is killed; content not read (tracker), known through the test comment.

## Which files a change would have to touch

- The tests named above, all in `tests/test_stage2.py` (the interrupt/signal family, `~23407–23560`, `~26515–26933`) and possibly `tests/test_ci.py` (`~2587–2934`) — where any de-flaking of the tests themselves lives.
- `scripts/stage2.py` (`defer_launch_signals`, `launch`, `kill_live`, `Terminated`, the main handler at `~11538–11556`) and `scripts/verify_run.py` (`_hold_launch_signals`, `interrupted`) plus `scripts/verify_lock.py` (`end_lingering_group`) — only if the production side changes; today's evidence points at the tests' cleanup and liveness verdicts, not at an established production fault, but the production copy-pattern between `stage2.py` and `verify_run.py` means a change to one likely names the other.
- `plans/changes/flaky-popen-signal/` — `research.md` (this file) and later the phase artefacts; `plans/INDEX.md` carries the row.
- `.github/workflows/ci.yml` is generated (`scripts/ci_gates.py --generate-ci`, header of `ci.yml`); a retry-at-CI-level idea would go through the gate file and decisions, not a hand edit — stated as where a change *would* live, not as a recommendation.

---

**Not read, stated as not read:** bead `coding-harness-oag7`'s tracker record, the GitHub CI logs of PR #404 and #419, and the full history of the two 2026-10-31 archived findings files beyond the quoted diagnostics blocks.
