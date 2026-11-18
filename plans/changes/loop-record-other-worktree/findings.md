---
title: "Findings — loop-record-other-worktree"
category: findings
status: draft
implementation_status: none
date: 2026-11-18
created: 2026-11-18
last_reviewed: 2026-11-18
updated: 2026-11-19
supersedes: null
superseded_by: null
bead: coding-harness-e82i
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-18"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — loop-record-other-worktree

Stage-2 call, 2026-11-18: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1114 files, 4591 commits, 12 rules.

Stage-2 call, 2026-11-18: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1117 files, 4592 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-18

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | MAJOR | SPEC | base | spec.md criterion 3, Terms; decisions.md Q-1 | [AMBIGUITY] "An archive beside the state directory" can mean two places, because the spec uses "state directory" for two things. Terms use it for one worktree's `stage2/<change>@<digest>/`, while criterion 1 uses "the current state directory" for the base that holds every key. Reading A: the archive sits inside `stage2/` next to the key directories. It then shares the namespace that criterion 1's scan and the `--supersedes` key check read, so both have to skip it, and its name must not let a second supersession of the same key overwrite the first archive. Reading B: the archive sits next to `stage2/` in its own tree, where the scan never meets it. Criterion 3's test checks a path, so it depends on which reading holds. The accounting line in criterion 2 names only the key, so under neither reading do findings.md or the workflow (criterion 10) say how to find a given archive. | Opus | in spec | — |
| S-2 | MAJOR | SPEC | base | spec.md criteria 1, 2, 5; decisions.md Q-1 ("the audit calls it accounts for") | [AMBIGUITY] Which audit calls the line accounts for. Reading A: every review-loop audit line still pending in the current findings since the last release or restart, i.e. what `lost_record_refusal` counts. Reading B: only the calls that belong to the superseded record. Audit lines carry no key, so B needs an attribution rule the spec does not give. The two readings split when criterion 1 names two or more keys. Under A, superseding one key clears the refusal, the other record is never named again and stays active at its key. Under B, the refusal keeps firing until each record is superseded. The spec also does not say whether supersession is allowed when no call is pending. Criterion 5 lists no such refusal, so as written any worktree of the change could archive another worktree's idle record with a line that accounts for 0 calls. | Opus | in spec | — |
| S-3 | MAJOR | SPEC | base | spec.md criteria 2, 4, 9; docs/WORKFLOW.md "A release needs a `Phase 6 verdict:` line … after the last `Loop restarted:` line" | [AMBIGUITY] What kind of line `--restart --supersedes` writes. Reading A: supersession is a restart under the ADR 0021 amendment, so its one line is a `Loop restarted: <date> after round <N> — …` line. Every existing restart reader then applies to it: the verdict floor, the stop floor, `restarted_fresh` and the "already restarted" refusal. N has to come from a record that findings.md has never contained. Reading B: it is a new kind of line that only the lost-record check and round numbering learn about. Then release's floor (`max(last release, last restart)`) does not move, and a `Phase 6 verdict:` line already in findings.md before the supersession releases the new run's rows. That breaks the amendment's rule that a restarted run is released only after a new phase-6 verdict, and no criterion goes red. | Opus | in spec | — |
| S-4 | MAJOR | SPEC | base | spec.md criteria 5 and 7 | Hole: criteria 5 and 7 conflict for an interrupted supersession. Supersession writes in two places, findings.md in the worktree and the archive in the state directory, so it cannot be one atomic step. If the archive is moved first and the run stops before the line is written, the retry finds the key missing at its old place. Criterion 5 says a missing key must be refused with nothing changed; criterion 7 says the retry completes. If the line is written first and the run stops before the move, findings.md already shows a restart while the record is still active at the old key, which is criterion 7's "false completed restart". Avoiding that would need the current worktree's review-loop to look across keys, which Q-1 allows for one command only. The spec does not say which half-done state is allowed, how a retry recognises it, or whether "absent at the old key but present in the archive" counts as missing. It also does not say what observable state makes a "false completed restart" (exit status, a line in findings.md, or a fresh review-loop being let through), so that part of criterion 7 has no defined red case. | Opus | in spec | — |
| S-5 | MINOR | SPEC | base | spec.md criterion 1 | [AMBIGUITY] Which refusal criterion 1 means by "the missing-record refusal". Reading A: only `lost_record_refusal`'s message, used by review-loop, release-loop, `--stage-failed` and prepare-loop. Reading B: also the other no-record refusals. Those are `restart_loop`'s "has no completed loop round and its loop record is missing; the maintainer must account for the stale audit lines in findings.md by hand" and triage's "the change has no loop record here". Under A, the incident's own path (the maintainer trying `release-loop --restart --reason`, as L4's handover asked) still gets a message that names no key and sends them to the hand reconciliation this change replaces. Under B it names the keys. The tests for criterion 1 differ between the two. | Opus | in spec | — |
| S-6 | MINOR | SPEC | base | spec.md criteria 2 and 4 | [AMBIGUITY] What "its rounds" in the accounting line means. Reading A: how many round headings the superseded record has, e.g. "3 rounds". Reading B: which round numbers it holds, e.g. "rounds 4–6". They differ whenever the old record did not start at round 1 because the old worktree released earlier rounds. Under A, a new findings.md that lacks that earlier release gives a next round of 4, which reuses a number from the superseded record and breaks criterion 4. Criterion 2's "misstates" cannot be tested until one reading is fixed. The same is open for "the audit calls accounted for": a count, or the lines named. | Opus | in spec | — |
| S-7 | MINOR | SPEC | base | spec.md criterion 9; scripts/stage2.py `release` (no-record branch) | Hole: the spec does not say what release-loop does after a supersession when no new round has run. Today, `release` with no record and no released block in findings.md (exactly the incident's state after supersession) appends `Loop rows: none — the loop did not run for this change.` once a verdict line stands. Criterion 9 keeps that behaviour, so the runner would write a false line, which is the kind of untrue record Q-1 set out to avoid. The spec does not say whether release-loop should refuse in that state, write nothing, or write that line. | Opus | in spec | — |

Stage-2 call, 2026-11-18: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1117 files, 4598 commits, 12 rules.

Stage-2 call, 2026-11-18: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1117 files, 4600 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-18

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-8 | MAJOR | SPEC | base | spec.md criteria 2 and 4; decisions.md S-6; scripts/stage2.py:10863, 10743-10744, 4521 | Hole: the spec does not say how the run after a supersession numbers its rounds or applies its stops. Criterion 4 and S-6 assume the next round simply continues after N. The runner numbers rounds by counting them, though, not from the restart line. `_review_round` takes `rounds_run(record, findings) + 1`, and a release block stores only a count (`Rounds run: <n>`). The stops use `last = max(history, rounds_run)` and run only when `last > restart_floor`. After a supersession, findings.md holds none of rounds 1..N, so the round count and the round number no longer match. Unchanged, the first fresh round is round 1. If an implementation moves only that first round to N+1, three things are still open. (a) Which number the run's second round gets. (b) Which number a continued round gets after the run's own release: with the count rule, round 3 again after releasing two rounds. (c) Whether the stops fire. A clean round N+1 with no rows leaves `history` empty and `last` = 1 ≤ N, so the clean stop does not fire and the next paid stage runs. Criterion 4's refutation only covers reuse of earlier numbers. No criterion goes red when the run's clean stop or repair brake does not fire after a supersession. | Opus | in spec | — |
| S-9 | MAJOR | SPEC | base | spec.md criteria 5 and 7; decisions.md S-4 | [AMBIGUITY] What counts as an "unfinished archived supersession". S-4 defines it as "absent at its old place, present in the archive, no accounting line for it". The archive tree is shared by every worktree of the state directory, but each worktree has its own findings.md. Reading A: any archive of the key that the current findings.md does not name is unfinished. Then worktree B can complete a supersession that worktree C already finished, and write a line for rounds that C's findings already accounts for. When one key has two timestamped archives, the spec also does not say which one B's line names. Reading B: only an archive this worktree started counts, which means the archive has to record where it came from. Then B is refused as "missing", and criterion 1 points B at C's fresh record as the only active other key. Separate case: the run crashes after archiving K1 but before archiving K2. A retry that names only K2 passes every check in criterion 5 (K2 is the only active key and calls are pending). It writes a line without K1 and takes N from K2 alone. After that no call is pending, so a later request for K1 is refused and K1 is never accounted for. None of criterion 7's red cases (irretrievable, line while active, duplicate) catches this. | Opus | in spec | — |
| S-10 | MINOR | SPEC | base | spec.md criteria 1 and 9; scripts/stage2.py:4723-4734 | Hole: the spec does not say what plain `release-loop --restart --reason` (without `--supersedes`) does while other-worktree records of the change are active. `restart_loop` checks for a lost record only when findings.md has no completed round. Example: the old worktree released rounds 1–3 and then ran rounds 4–6 without releasing them. The new worktree's findings.md then holds rounds 1–3 and the pending audit lines. A plain restart succeeds with "after round 3" and accounts for every pending call. The other record stays active at its key, and the fresh run numbers its rounds from 4, repeating the old record's 4–6. A later `--supersedes` for that key is refused by criterion 5 because no call is pending. Criterion 9 keeps this behaviour, and criterion 1 never applies because nothing is refused. Whether a plain restart should refuse, or name the other keys, while they are active is left to the implementer. | Opus | in spec | — |
| S-11 | MINOR | SPEC | base | spec.md criteria 9 and 10; scripts/stage2.py:4620-4624 | [AMBIGUITY] Which releases criterion 10 covers. Reading A: every restart line with no round after it. That changes plain restarts: today a release after a plain restart with no new round exits 0 and writes nothing, because a released block stands. Criterion 9 says that release behaviour stays in force. Reading B: only supersession restarts. Then the runner has to tell the two kinds of `Loop restarted:` line apart by their text, which S-3 meant to avoid. The criterion also cannot go red for its "refuses" half. If the new worktree's findings.md already holds a released block, today's code returns exit 0 without writing anything. That passes the refutation ("writes … or otherwise changes findings") even though nothing refused. | Opus | in spec | — |
| S-12 | MINOR | SPEC | base | spec.md criteria 3 and 8; scripts/stage2_availability.py:1355; scripts/stage2.py:4638-4654 | Hole: the spec does not say which files the archive takes from the key directory. Besides `loop.md` and the research entries that criterion 8 keeps in place, the directory can hold `availability.json`. That is the prepare-loop receipt the next fresh `review-loop` consumes, and `remove_loop_record` deletes it together with every other non-research entry. Criterion 3 says "the loop record", and criterion 8 lists research state, research receipts and probe audits. Neither covers this receipt. Reading A: only `loop.md` moves, and the old worktree's receipt stays at its key. Reading B: everything that a release would delete moves. A test of "preserved unchanged" checks different contents under each reading. | Opus | in spec | — |
| S-13 | MINOR | SPEC | base | spec.md criterion 2; decisions.md S-1, S-3, S-4 | Hole: the spec does not fix how the archive path is written in the accounting line, and that line goes into findings.md, which is committed. Reading A: the absolute path. It contains the maintainer's home directory, and findings.md is checked by the leak check against its denylist. Reading B: a path relative to the state directory, or written with `${XDG_STATE_HOME:-~/.local/state}` as docs/WORKFLOW.md writes record paths. Two things depend on the form: the test for criterion 2's "misstates … archive path", and how a retry matches a line to its archive (S-4). | Opus | in spec | — |

Stage-2 call, 2026-11-18: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1117 files, 4612 commits, 12 rules.

Stage-2 call, 2026-11-18: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1117 files, 4613 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-18

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-14 | MAJOR | SPEC | base | spec.md criteria 4 and 9; scripts/stage2.py:4723 (`restart_loop`), 4454-4466 (`rounds_run`), 4281-4298 (`history_rounds`) | Hole: the spec does not say what N a plain `release-loop --restart` writes once a supersession run has been released. Today `restart_loop` takes `last = max(highest round in history_rounds, rounds_run)`. `history_rounds` only knows rounds that have rows, and `rounds_run` adds up the `Rounds run:` counts. The two agree only while round numbers start at 1, which a supersession breaks. Example 1: supersede at N=3, run round 4 with rows and round 5 clean with no finding, release (`Rounds run: 2`), then restart plainly. The line says "after round 4" and the next fresh round is 5 again. Example 2: the run's only round, 4, is clean with no finding. The line says "after round 1" and round 2 repeats an archived round number. Two things are open. Does criterion 4's "each subsequent round" still apply after a later plain restart? Does criterion 9 ("existing … restart … behavior remains in force") stop the implementer from making restart's N follow the restart floor? As written, the runner writes a false "after round" line and no criterion goes red for it. | Opus | in spec | — |
| S-15 | MAJOR | SPEC | base | spec.md criteria 5, 9 and 13 | Hole: criteria 13 and 5 together can leave the maintainer no way to restart. Criterion 13 refuses a plain restart while any other worktree holds an active record of the change, and points to `--supersedes`. Criterion 5 refuses `--supersedes` when the current findings.md has no pending audit call. Example: worktree B carries a released block and no pending call, while worktree A has started a new record whose audit lines never reached B's findings.md. A parallel or re-sliced lane gets there. So does an orphaned record of a removed worktree, or A's DL-A-3 crash leftover whose release block B already carries. B then cannot restart at all, and the refusal points to a command that also refuses. Today that restart succeeds. The spec does not say whether B is meant to stay blocked until A releases, or what the maintainer does instead other than deleting a record directory by hand. | Opus | in spec | — |
| S-16 | MINOR | SPEC | base | spec.md criteria 1, 5, 13, Protected areas; scripts/stage2.py:3921-3933 | [AMBIGUITY] Which keys count as "other worktree keys" of the change. A key is only `<change>@<8 hex of the resolved root>`, and `<state>/coding-harness/stage2/` is shared by every checkout on the machine that runs the runner (the triage test plants a "sibling-repo" record there). Reading A: every `<change>@<digest>` directory except the current one. That includes other clones or repositories with a change of the same name. Criterion 13 then refuses a plain restart because of another repository's record, and `--supersedes` can archive that record, because criterion 5 decides "another change" by name only. Reading B: only digests of this repository's current worktrees (e.g. from `git worktree list`). That never touches another repository, but it misses a record whose worktree has been removed (§3 removes worktrees after merge), which may be exactly the incident's v1 state. The tests for criteria 1 and 13 differ between the two readings. | Opus | in spec | — |
| S-17 | MINOR | SPEC | base | spec.md criteria 2, 3 and 16; decisions.md S-1, S-3, S-9 | Hole: the spec does not fix the archive layout when more than one key is superseded. S-1 names the directory `<change>@<digest>@<UTC timestamp>` for a single key, but criterion 3 and S-9 put every key of one supersession into one directory. Two things are open. Which digest goes in the name: one of the superseded keys (which one?) or the superseding worktree's? Does each record go under `<dir>/<key>/`, or loose in `<dir>/`, where two `loop.md` files would collide? S-3's line form also has room for only one key, while criterion 2 asks for "each record's … archive path". Criterion 2's "misstates … archive path", criterion 3's "preserved unchanged" and criterion 16's match by directory name would all be tested against a layout the implementer makes up. | Opus | in spec | — |
| S-18 | MINOR | SPEC | base | spec.md criteria 1, 5 and 7; decisions.md S-9 | Hole: an unfinished supersession whose key set changes before the retry can be neither completed nor abandoned. Example: the run stops after K1 has moved into the staging archive (manifest {K1, K2}), and before the retry worktree D starts a record of the change. Criterion 5 now requires the full active and unfinished set {K1, K2, D}, but criterion 7 completes only the manifest's set {K1, K2}, so every request is refused. Meanwhile K1 is neither active nor accounted for, and criterion 1's refusal does not name it because it sits in an archive. The same dead end follows if K2 becomes unreadable after K1 has moved. The spec gives no way to roll back or abandon an unfinished supersession, and does not say which of the two criteria wins. | Opus | in spec | — |

Stage-2 call, 2026-11-18: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1117 files, 4619 commits, 12 rules.

Stage-2 call, 2026-11-18: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1117 files, 4621 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +53 -2
> - `scripts/stage2.py` +438 -24
> - `tests/test_stage2.py` +560 -0
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `scripts/stage2.py`, `tests/test_stage2.py`; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before post-run verification: `.venv/bin/ruff check` exited 1
> scripts/stage2.py:4936:5: ARG001 Unused function argument: `change`
>      |
> 4935 | def _supersede_accounting_line(
> 4936 |     change: str,
>      |     ^^^^^^ ARG001
> 4937 |     keys: list[str],
> 4938 |     rounds: dict[str, list[int]],
>      |
>
> tests/test_stage2.py:1376:18: ARG001 Unused function argument: `world`
>      |
> 1376 | def archive_base(world: World) -> Path:
>      |                  ^^^^^ ARG001
> 1377 |     """The archive directory of superseded records, beside the records in the state directory."""
> 1378 |     return stage2.record_base().parent / stage2.ARCHIVE_DIR_NAME
>      |
>
> Found 2 errors.
> ```

Stage-2 call, 2026-11-18: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 1117 files, 4631 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/stage2.py` +1 -2
> - `tests/test_stage2.py` +11 -11
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>                 TEST_FLASH[0],
>                 "taken — test_a",
>                 "yes",
>                 "agree",
>             ],
>         ]
>         world.write_findings(
>             stage2.RELEASE_HEADING + " 2026-11-17",
>             stage2.render_table(stage2.RELEASED_COLUMNS, released_rows),
>             "Rounds run: 2",
>         )
>         other = other_worktree(world)
>         key = stage2.record_key("demo", other)
>         write_foreign_record(other, [3, 4])
> >       assert supersede(world, key) == 0
>
> tests/test_stage2.py:1804: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> tests/test_stage2.py:1386: in supersede
>     return world.run("release-loop", "demo", "--restart", *options, "--reason", reason)
> tests/test_stage2.py:372: in run
>     return stage2.main([*argv, *options, "--root", str(self.root)])
> scripts/stage2.py:11784: in main
>     return _run(args)
> scripts/stage2.py:11864: in _run
>     release_loop(
> scripts/stage2.py:5130: in release_loop
>     supersede_loop(root, change, supersedes, reason or "")
> scripts/stage2.py:5025: in supersede_loop
>     archive_name = _supersession_archive_name(archive_base, change, current.split("@", 1)[1])
> scripts/stage2.py:4879: in _supersession_archive_name
>     stamp = dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H-%M-%SZ")
> tests/runner_clock_guard.py:186: in wrapper
>     _judge(sys._getframe(1), label)
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> frame = <frame at 0x119c47010, file '/Users/mikypiky/coding-harness/.claude/worktrees/loop-record-other-worktree/scripts/stage2.py', line 4879, code _supersession_archive_name>
> api = 'datetime.now'
>
>     def _judge(frame: types.FrameType, api: str) -> None:
>         code = frame.f_code
>         if not is_guarded(code.co_filename) or code.co_qualname == BOUNDARY_QUALNAME:
>             return
>         read = Read(api, code.co_filename, frame.f_lineno, code.co_qualname, _state["in_test"])
>         READS.append(read)
> >       raise RunnerClockRead(f"runner clock read outside clock_now: {read}")
> E       runner_clock_guard.RunnerClockRead: runner clock read outside clock_now: datetime.now read in _supersession_archive_name at /Users/mikypiky/coding-harness/.claude/worktrees/loop-record-other-worktree/scripts/stage2.py:4879
>
> tests/runner_clock_guard.py:160: RunnerClockRead
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_supersede_rejects_invalid_requests_without_changes
> FAILED tests/test_stage2.py::test_supersede_archives_only_the_old_loop_record
> FAILED tests/test_stage2.py::test_supersede_accounts_for_old_rounds_and_calls
> FAILED tests/test_stage2.py::test_supersede_release_requires_a_new_round - ru...
> FAILED tests/test_stage2.py::test_supersede_preserves_research_siblings - run...
> FAILED tests/test_stage2.py::test_supersede_recovers_from_interrupted_writes
> FAILED tests/test_stage2.py::test_supersede_clean_round_stops_next_stage - ru...
> FAILED tests/test_stage2.py::test_plain_restart_refuses_active_other_worktree_records
> FAILED tests/test_stage2.py::test_plain_restart_after_supersession_uses_highest_round
> FAILED tests/test_stage2.py::test_supersede_starts_fresh_after_old_round_numbers
> FAILED tests/test_stage2.py::test_supersede_requires_a_new_verdict - runner_c...
> FAILED tests/test_stage2.py::test_supersede_without_pending_audit_calls - run...
> FAILED tests/test_stage2.py::test_supersede_retry_matches_archive_directory
> FAILED tests/test_stage2.py::test_supersede_respects_both_record_locks - runn...
> FAILED tests/test_stage2.py::test_supersede_repair_brake_uses_fresh_rounds - ...
> ERROR tests/test_stage2.py::test_supersede_archives_only_the_old_loop_record
> ERROR tests/test_stage2.py::test_supersede_accounts_for_old_rounds_and_calls
> ERROR tests/test_stage2.py::test_supersede_release_requires_a_new_round - Fai...
> ERROR tests/test_stage2.py::test_supersede_preserves_research_siblings - Fail...
> ERROR tests/test_stage2.py::test_supersede_recovers_from_interrupted_writes
> ERROR tests/test_stage2.py::test_supersede_clean_round_stops_next_stage - Fai...
> ERROR tests/test_stage2.py::test_plain_restart_refuses_active_other_worktree_records
> ERROR tests/test_stage2.py::test_plain_restart_after_supersession_uses_highest_round
> ERROR tests/test_stage2.py::test_supersede_starts_fresh_after_old_round_numbers
> ERROR tests/test_stage2.py::test_supersede_requires_a_new_verdict - Failed: r...
> ERROR tests/test_stage2.py::test_supersede_without_pending_audit_calls - Fail...
> ERROR tests/test_stage2.py::test_supersede_retry_matches_archive_directory - ...
> ERROR tests/test_stage2.py::test_supersede_respects_both_record_locks - Faile...
> ERROR tests/test_stage2.py::test_supersede_repair_brake_uses_fresh_rounds - F...
> 15 failed, 3 passed, 14 errors in 6.71s
> ```

Stage-2 call, 2026-11-18: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 1117 files, 4631 commits, 12 rules.

Stage-2 call, 2026-11-18: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed; Sonnet attempt 3 stopped at the Claude usage limit; continues from the saved attempt · leak check clean over 1117 files, 4636 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/loop-record-other-worktree/plan.md` +16 -16
> - `scripts/stage2.py` +1 -1
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> ----------------------------- Captured stdout call -----------------------------
> release-loop: the loop of demo restarts after round 2; the next review-loop is a fresh run.
> INFO  (1):
>   - leak check clean: 30 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 30 files, 2 commits, 1 rules, 1 prompt texts
> review-loop: round 3 written to /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1815/popen-gw4/test_supersede_starts_fresh_af0/state/coding-harness/stage2/demo@d41c09a0/loop.md: 2 rows from 2 of 2 members
> release-loop: 2 loop rows appended to plans/changes/demo/findings.md
> ----------------------------- Captured stderr call -----------------------------
> refused: taken rows are not repaired yet (L3-1, L3-2); run `repair` and make `make verify` green before the next round starts.
> ________________ test_supersede_repair_brake_uses_fresh_rounds _________________
> [gw0] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/loop-record-other-worktree/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1815/popen-gw...s/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1815/popen-gw0/test_supersede_repair_brake_us0/state'))
> capsys = <_pytest.capture.CaptureFixture object at 0x1075946b0>
>
>     def test_supersede_repair_brake_uses_fresh_rounds(world: World, capsys) -> None:
>         """Criterion 15: the brake stops on two fresh fix-r rounds after the restart floor - the rounds
>         released before the supersession are never counted into it.
>         Planted fault: the brake reads rounds before the restart floor."""
>         released_rows = [
>             [
>                 "L1-1",
>                 "MAJOR",
>                 "MAINT",
>                 "fix-r1",
>                 "src/app.py:1",
>                 "finding one",
>                 TEST_FLASH[0],
>                 "taken — test_a",
>                 "yes",
>                 "agree",
>             ],
>             [
>                 "L2-1",
>                 "MAJOR",
>                 "MAINT",
>                 "fix-r2",
>                 "src/app.py:2",
>                 "finding two",
>                 TEST_FLASH[0],
>                 "taken — test_a",
>                 "yes",
>                 "agree",
>             ],
>         ]
>         world.write_findings(
>             stage2.RELEASE_HEADING + " 2026-11-17",
>             stage2.render_table(stage2.RELEASED_COLUMNS, released_rows),
>             "Rounds run: 2",
>         )
>         other = other_worktree(world)
>         key = stage2.record_key("demo", other)
>         write_foreign_record(other, [3, 4])
>         assert supersede(world, key) == 0
>         # Round 5 takes the fresh run's free stage, round 6 the Flash stage: two members each.
>         world.script(pi=[{"stdout": rows(1)}] * (2 * len(TEST_FREE)))
>         assert world.run("review-loop") == 0, "the brake counted the superseded or released rounds"
>         decide_record(world, status="taken — test_a", broke="yes", origin="fix-r1")
> >       assert world.run("review-loop") == 0, "the brake fired one fresh fix-r round early"
> E       AssertionError: the brake fired one fresh fix-r round early
> E       assert 2 == 0
> E        +  where 2 = run('review-loop')
> E        +    where run = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1815/popen-gw...s/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1815/popen-gw0/test_supersede_repair_brake_us0/state')).run
>
> tests/test_stage2.py:1809: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> release-loop: the loop of demo restarts after round 4; the next review-loop is a fresh run.
> INFO  (1):
>   - leak check clean: 30 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 30 files, 2 commits, 1 rules, 1 prompt texts
> review-loop: round 5 written to /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1815/popen-gw0/test_supersede_repair_brake_us0/state/coding-harness/stage2/demo@3b1d0894/loop.md: 2 rows from 2 of 2 members
> ----------------------------- Captured stderr call -----------------------------
> refused: taken rows are not repaired yet (L5-1, L5-2); run `repair` and make `make verify` green before the next round starts.
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_supersede_rejects_invalid_requests_without_changes
> FAILED tests/test_stage2.py::test_supersede_starts_fresh_after_old_round_numbers
> FAILED tests/test_stage2.py::test_supersede_repair_brake_uses_fresh_rounds - ...
> 3 failed, 15 passed in 6.91s
> ```

Stage-2 call, 2026-11-18: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Sonnet rerun left 3 of 18 new tests red (supersede invalid requests, fresh round numbers, repair brake); second Sonnet pass from that tree · leak check clean over 1117 files, 4646 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_stage2.py` +10 -6
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: red) because the targeted coverage was not safe: the whole tests/test_stage2.py requires full verification until coding-harness-vg9 splits it
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [frontmatter-current] $ python3 scripts/check_frontmatter_current.py
> docs/WORKFLOW.md: stale — updated 2026-11-15 is older than its last change 2026-11-18 (4ddb081b)
> fix: python3 scripts/check_frontmatter_current.py --stamp
> ── [frontmatter-current] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> make: *** [verify] Error 1
> ```

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1117 files, 4655 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1117 files, 4655 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1117 files, 4655 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1117 files, 4655 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1117 files, 4655 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1117 files, 4655 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 1117 files, 4655 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1117 files, 4655 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1117 files, 4655 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 1117 files, 4655 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1117 files, 4655 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1117 files, 4655 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 1117 files, 4655 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 1117 files, 4655 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 1117 files, 4655 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 1117 files, 4655 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model step-5-preview · leak check clean over 1117 files, 4655 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 1117 files, 4655 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 1117 files, 4655 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 1117 files, 4655 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 1117 files, 4655 commits, 12 rules.

Stage-2 call, 2026-11-18: review-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1117 files, 4655 commits, 12 rules.

Stage-2 call, 2026-11-18: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1117 files, 4667 commits, 12 rules.

Runner restoration, 2026-11-18: repair · attempt 1 · route codex — lifecycle fields: plans/changes/loop-record-other-worktree/plan.md, plans/changes/loop-record-other-worktree/spec.md — unchanged

Stage-2 call, 2026-11-18: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1117 files, 4679 commits, 12 rules.

Stage-2 call, 2026-11-18: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1117 files, 4679 commits, 12 rules.

Stage-2 call, 2026-11-18: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1117 files, 4679 commits, 12 rules.

Stage-2 call, 2026-11-18: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1117 files, 4688 commits, 12 rules.

Runner restoration, 2026-11-19: repair · attempt 1 · route codex — lifecycle fields: plans/changes/loop-record-other-worktree/plan.md, plans/changes/loop-record-other-worktree/spec.md — unchanged

Stage-2 call, 2026-11-19: review-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1117 files, 4698 commits, 12 rules.

Stage-2 call, 2026-11-19: review-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1117 files, 4698 commits, 12 rules.
