---
title: "Findings — time-records-data"
category: findings
status: draft
implementation_status: none
date: 2026-10-31
created: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-11-03
supersedes: null
superseded_by: null
bead: coding-harness-v6vk
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — time-records-data

Stage-2 call, 2026-10-31: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 789 files, 2840 commits, 12 rules.

Stage-2 call, 2026-11-03: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 841 files, 3100 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +18 -1
> - `plans/changes/time-records-data/plan.md` +8 -8
> - `scripts/ci_gates.py` +7 -1
> - `scripts/harness.py` +139 -4
> - `scripts/kit/manifest.yaml` +9 -0
> - `scripts/run_report.py` +25 -28
> - `scripts/stage2.py` +30 -39
> - `scripts/time_records.py` +227 -0
> - `tests/test_harness_time_log.py` +223 -0
> - `tests/test_run_report.py` +59 -0
> - `tests/test_stage2.py` +42 -0
> - `tests/test_time_records.py` +197 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed `scripts/stage2.py`; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before `make verify`: `.venv/bin/ruff check` exited 1
> tests/test_harness_time_log.py:67:14: ARG001 Unused function argument: `root`
>    |
> 67 | def run_args(root: Path, argv: list[str]) -> tuple[int, list[str]]:
>    |              ^^^^ ARG001
> 68 |     """One in-process run; an argparse refusal exits, and its exit code is the verdict."""
> 69 |     out: list[str] = []
>    |
>
> Found 1 error.
> ```

Stage-2 call, 2026-11-03: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 844 files, 3106 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/time-records-data/plan.md` +8 -8
> - `tests/test_harness_time_log.py` +15 -15
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>         assert code == 2 and plan.read_text(encoding="utf-8") == "# Plan\n\nnothing here\n"
>         doubled = PLAN + "\n## Time used\n\nmore\n"
>         plan.write_text(doubled, encoding="utf-8")
>         code, _ = run_args(argv_for(root))
>         assert code == 2 and plan.read_text(encoding="utf-8") == doubled
>         reset()
>         # A symlinked plan never receives the write; the link and its target survive untouched.
>         plan.unlink()
>         plan.symlink_to(outside)
>         code, _ = run_args(argv_for(root))
>         assert code == 2 and outside.read_bytes() == b"untouched\n" and plan.is_symlink()
>         reset()
>         # A hard-linked plan never receives the write through its link.
>         plan.unlink()
>         os.link(outside, plan)
>         code, _ = run_args(argv_for(root))
>         assert code == 2 and outside.read_bytes() == b"untouched\n"
>         reset()
>         # An aliased change folder never receives the write through the link.
>         shutil.rmtree(plan.parent)
>         plan.parent.symlink_to(outside_dir, target_is_directory=True)
> >       (outside_dir / "plan.md").write_bytes(healthy)
>
> tests/test_harness_time_log.py:185: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/pathlib.py:1036: in write_bytes
>     with self.open(mode='wb') as f:
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> self = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-199/popen-gw0/test_invalid_input_and_unsafe_0/outside-change/plan.md')
> mode = 'wb', buffering = -1, encoding = None, errors = None, newline = None
>
>     def open(self, mode='r', buffering=-1, encoding=None,
>              errors=None, newline=None):
>         """
>         Open the file pointed to by this path and return a file object, as
>         the built-in open() function does.
>         """
>         if "b" not in mode:
>             encoding = io.text_encoding(encoding)
> >       return io.open(self, mode, buffering, encoding, errors, newline)
> E       FileNotFoundError: [Errno 2] No such file or directory: '/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-199/popen-gw0/test_invalid_input_and_unsafe_0/outside-change/plan.md'
>
> /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/pathlib.py:1013: FileNotFoundError
> ----------------------------- Captured stderr call -----------------------------
> usage: harness.py time-log [-h] --start START --end END --seconds SECONDS
>                            --verb ACTIVITY --attempt ATTEMPT --route ROUTE
>                            --model MODEL --result {accepted,rejected}
>                            [--root ROOT]
>                            change
> harness.py time-log: error: argument --result: invalid choice: 'maybe' (choose from accepted, rejected)
> usage: harness.py time-log [-h] --start START --end END --seconds SECONDS
>                            --verb ACTIVITY --attempt ATTEMPT --route ROUTE
>                            --model MODEL --result {accepted,rejected}
>                            [--root ROOT]
>                            change
> harness.py time-log: error: the following arguments are required: --seconds
> usage: harness.py time-log [-h] --start START --end END --seconds SECONDS
>                            --verb ACTIVITY --attempt ATTEMPT --route ROUTE
>                            --model MODEL --result {accepted,rejected}
>                            [--root ROOT]
>                            change
> harness.py time-log: error: the following arguments are required: --model
> usage: harness.py time-log [-h] --start START --end END --seconds SECONDS
>                            --verb ACTIVITY --attempt ATTEMPT --route ROUTE
>                            --model MODEL --result {accepted,rejected}
>                            [--root ROOT]
>                            change
> harness.py time-log: error: the following arguments are required: --start
> usage: harness.py time-log [-h] --start START --end END --seconds SECONDS
>                            --verb ACTIVITY --attempt ATTEMPT --route ROUTE
>                            --model MODEL --result {accepted,rejected}
>                            [--root ROOT]
>                            change
> harness.py time-log: error: the following arguments are required: --result
> =========================== short test summary info ============================
> FAILED tests/test_harness_time_log.py::test_time_log_appends_one_counted_record
> FAILED tests/test_time_records.py::test_atomic_publish_leaves_the_plan_on_failure
> FAILED tests/test_harness_time_log.py::test_invalid_input_and_unsafe_destination_leave_bytes_unchanged
> 3 failed, 18 passed in 9.73s
> ```

Stage-2 call, 2026-11-03: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 844 files, 3106 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/time_records.py` +1 -1
> - `tests/test_harness_time_log.py` +2 -1
> - `tests/test_time_records.py` +1 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before `make verify`: `.venv/bin/ruff check` exited 1
> scripts/time_records.py:196:9: PTH105 `os.replace()` should be replaced by `Path.replace()`
>     |
> 194 |             os.fsync(out.fileno())
> 195 |         temporary.chmod(mode)
> 196 |         os.replace(temporary, plan)
>     |         ^^^^^^^^^^ PTH105
> 197 |     except BaseException:
> 198 |         temporary.unlink(missing_ok=True)
>     |
>
> Found 1 error.
> ```

Stage-2 call, 2026-11-03: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 844 files, 3111 commits, 12 rules.

Stage-2 call, 2026-11-03: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 844 files, 3111 commits, 12 rules.

Stage-2 call, 2026-11-03: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 844 files, 3111 commits, 12 rules.

Stage-2 call, 2026-11-03: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 844 files, 3111 commits, 12 rules.

Stage-2 call, 2026-11-03: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 844 files, 3111 commits, 12 rules.

Stage-2 call, 2026-11-03: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 844 files, 3111 commits, 12 rules.

Stage-2 call, 2026-11-03: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 844 files, 3111 commits, 12 rules.

Stage-2 call, 2026-11-03: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 844 files, 3111 commits, 12 rules.

Stage-2 call, 2026-11-03: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 844 files, 3111 commits, 12 rules.

Stage-2 call, 2026-11-03: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 844 files, 3111 commits, 12 rules.

Stage-2 call, 2026-11-03: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 844 files, 3111 commits, 12 rules.

Stage-2 call, 2026-11-03: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 844 files, 3111 commits, 12 rules.

Stage-2 call, 2026-11-03: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 844 files, 3111 commits, 12 rules.

Stage-2 call, 2026-11-03: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 844 files, 3111 commits, 12 rules.

Stage-2 call, 2026-11-03: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 844 files, 3111 commits, 12 rules.

Stage-2 call, 2026-11-03: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 844 files, 3111 commits, 12 rules.

Stage-2 call, 2026-11-03: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 844 files, 3111 commits, 12 rules.

Stage-2 call, 2026-11-03: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 844 files, 3111 commits, 12 rules.

Stage-2 call, 2026-11-03: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 844 files, 3111 commits, 12 rules.

Stage-2 call, 2026-11-03: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 844 files, 3111 commits, 12 rules.

Stage-2 call, 2026-11-03: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 844 files, 3113 commits, 12 rules.

Stage-2 call, 2026-11-03: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 844 files, 3114 commits, 12 rules.

Stage-2 call, 2026-11-03: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 844 files, 3114 commits, 12 rules.

Loop attempt: 2026-11-03 — no round was written; the review-loop calls above consumed no stage; audit calls: 2

Notice: the data terms of mimo-v2.6-pro expire on 2026-11-06 (3 days left).

glm-5.3-flash was asked again with the format reminder: the first answer was malformed

From glm-5.3-flash:

glm-5.3-flash's first answer, which was not in the required format:

The answer was not only six-cell rows; what is not one is kept below as it came.

> | R1 | MAJOR | SPEC | prompts/04-implement.md (the `appetite is a stop` block) | The change keeps the sentence `A break inside a session counts, and the record says so` directly above the command it introduces, but the command's fixed record has no slot for a break note and the new text moves the break's only mention to the session's status message, which does not survive `/clear`; the doctrine the change consolidated now asks the session to write an annotation the one fixed record cannot carry, so the two sentences contradict each other in the same paragraph. |
> | R2 | MINOR | SPEC | prompts/04-implement.md (the time-log command template) | The template fixes the activity and the outcome as literals while the spec requires the record to carry the activity's actual result; nothing marks those two fields as caller-substituted the way the start, attempt and model fields are, so a session that follows the template verbatim records every span as an accepted session span regardless of what happened. |
> | R3 | MINOR | MAINT | scripts/time_records.py (`publish_atomic`) | The docstring promises temporary file, fsync, rename and a directory fsync, but the branch taken when the destination is missing performs a plain non-atomic write with no durability step at all; a caller reaching the default publisher with a vanished destination silently receives weaker guarantees than the documented contract, while any failure after the write is reported as merely a synchronization warning. |
> | R4 | MINOR | MAINT | scripts/harness.py (`time_log` heading check) | The requirement of exactly one time heading counts heading lines also inside code fences, so a plan that legitimately quotes the heading in an unindented fenced example is refused as if it carried a second time section, and the refusal names only the count, leaving the maintainer to guess that a fenced quote tripped it. |
> | R5 | MINOR | SPEC | plans/changes/time-records-data/spec.md (neighbours header) | The change's own research enumerates the neighbours and states three active changes declare protected areas inside the module this change rewrites, yet the shipped spec carries an empty neighbours list, so the cross-change overlap the research says the spec phase must reconcile is nowhere visible in the header a maintainer of the neighbouring changes would read. |
> | R6 | MINOR | MAINT | plans/changes/time-records-data/research.md (frontmatter) | The research text itself records that the class declaration and the neighbours header are owed in its frontmatter before a swarm run and are written only by the runner, but the shipped file still presents neither, so the artefact contradicts its own statement of what is owed. |

From glm-5.3-flash:

glm-5.3-flash's second answer, which was not in the required format:

The answer was not only six-cell rows; what is not one is kept below as it came.

> | R1 | MAJOR | SPEC | prompts/04-implement.md, "The appetite is a stop" paragraph (the time-log command line) | The command the prompt hands to sessions is fixed as `--result accepted`, not a `<accepted\|rejected>` placeholder like every other field; a span that ends on a rejected or cut outcome (a stop, a failed verification before the stop, a parked span) is thereby instructed to record "accepted", so the plan's record can name an outcome the activity never had — spec criterion 2 and the spec's own `[DETAIL]` ("outcome names the actual activity result") are refuted by the instruction itself, and no test covers the rejected-session path.
> | R2 | MINOR | MAINT | scripts/time_records.py, `publish_atomic` (the `FileNotFoundError` branch) | When the destination is found missing at publish time, the shared default writer falls back to a plain non-atomic `plan.write_bytes(content)` with no temporary file, no fsync and no directory sync, contradicting the module's own documented contract ("temporary file, fsync, rename, directory fsync"); an existing plan deleted between the caller's checks is silently recreated outside the safe path, while the in-tree callers only dodge this by pre-checking existence themselves.
> | R3 | MINOR | MAINT | scripts/stage2.py, `REPAIR_FORMAT` (the Codex repair prompt, shell-capable) and `scripts/stage2.py`, `REPAIR_FORMAT_FILE_TOOLS` | The change gave interactive sessions a live machine command for time entries, and `prompts/04-implement.md` was updated to forbid calling it for runner-measured attempts ("A model running under the Stage-2 runner never calls it"); the embedded repair prompts the runner hands to Codex — the one Stage-2 role with a command tool — still carry only the old "write no entry under `## Time used`" sentence, so the only instruction those attempts see names the hand-write route and is silent about the new command, and the doctrine test (`test_runner_time_doctrine_preserves_interactive_measurement`) asserts nothing beyond the same hand-write clause.
> | R4 | MINOR | MAINT | scripts/harness.py, `time_log` (`--route`) | The command accepts any non-blank route with no relation to who calls it, so an interactive session following the prompt incompletely can pass e.g. `--route flash` and the report's fixed-format attempt rows will present an interactive span as a runner-model attempt; nothing at the command boundary warns or refuses, although the spec's `[DETAIL]` and `docs/WORKFLOW.md` both pin `route orchestrator` as the marker of a session-logged span.

Stage-2 call, 2026-11-03: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 844 files, 3114 commits, 12 rules.

Stage-2 call, 2026-11-03: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 844 files, 3116 commits, 12 rules.

Stage-2 call, 2026-11-03: review-loop · endpoint opencode-go · model hy3 · leak check clean over 844 files, 3117 commits, 12 rules.

Stage-2 call, 2026-11-03: review-loop · endpoint opencode-go · model hy3 · leak check clean over 844 files, 3117 commits, 12 rules.

Stage-2 call, 2026-11-03: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 844 files, 3118 commits, 12 rules.

Loop attempt: 2026-11-03 — no round was written; the review-loop calls above consumed no stage; audit calls: 1

Notice: the data terms of mimo-v2.6-pro expire on 2026-11-06 (3 days left).
