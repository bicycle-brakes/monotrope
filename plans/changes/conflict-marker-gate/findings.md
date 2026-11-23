---
title: "Findings — conflict-marker-gate"
category: findings
status: draft
implementation_status: none
date: 2026-11-05
created: 2026-11-05
last_reviewed: 2026-11-05
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-i76l
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — conflict-marker-gate

Stage-2 call, 2026-11-05: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 902 files, 3337 commits, 12 rules.

Stage-2 call, 2026-11-22: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1171 files, 5382 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-22

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | MAJOR | SPEC | base | `decisions.md` "SKIP · interview"; `spec.md` Problem bullet 3, AC7, Non-goals bullet 1, Open decisions bullet 5 | [AMBIGUITY] The maintainer approved "a small helper for merging main into a change branch that stops with the conflicted paths instead of continuing". Reading A (the spec's): the existing `pr_sync.py merge-main` already is that helper, so the change only extends `tests/test_pr_sync.py`. Reading B: the orchestrator proposed the helper as something to build, so the change would add a new command or script. The spec's non-goal "no new merge command" and the protected `scripts/pr_sync.py` rule that out. The spec settles this as a `[DETAIL]`, but whether something named in the approved scope is built or reused is a scope question for the maintainer, not a detail the draft can decide. | Opus | in spec — [DETAIL] decided by the orchestrator: reading A; the existing pr_sync.py merge-main is the helper, the change pins its stop-on-conflict behaviour with tests and names it in docs/WORKFLOW.md as the orchestrator's one way to merge main into a change branch | — |
| S-2 | MAJOR | SPEC | base | `spec.md` AC7 ("leaves the target branch, index, working files and remote branch unchanged"); Open decisions bullet 5 | [AMBIGUITY] "index" can mean Git's staging area or `plans/INDEX.md`; the existing `test_other_conflicts_preserve_target` reads it as `plans/INDEX.md` (`index_before`). "remote branch" can mean the branch on origin (what that test checks with `origin_ref`) or the local remote-tracking refs. Under the narrow reading the current helper passes, as the spec claims. Under the broad reading (every ref unchanged and `.git/index` byte-identical), a regression fails on unchanged code: `merge_main` runs `git fetch origin`, which moves `refs/remotes/origin/main` before the conflict is found, and `ensure_clean`'s `git status` can rewrite the index stat cache. Making that pass means editing the protected `scripts/pr_sync.py`. | Opus | in spec — [DETAIL] decided by the orchestrator: index means both Git's staging area and plans/INDEX.md, each unchanged; remote branch means the branch on origin, unchanged; local remote-tracking refs may move by the fetch | — |
| S-3 | MAJOR | SPEC | base | `spec.md` Terms "Named fixture exception"; AC3; AC4; AC8; DoD "Move together"; Non-goals bullet 3 | Missing: the spec requires a "reviewed allowlist" that starts empty but leaves four things undecided. (1) Where it lives: a constant in `scripts/check_conflict_markers.py`, or a data file, which the "Move together" list does not name. (2) Whether it travels with the kit as mechanism or stays per repository; if it lives in the script, a kit target that needs a fixture has to edit a travelling mechanism file. (3) How a test plants a non-empty list for AC3's sibling and prefix-match refutation, since a user-supplied skip flag is a non-goal. (4) What happens when a listed path is untracked or absent: ignored, reported, or failed. The builder would have to invent all four. | Opus | in spec — [DETAIL] decided by the orchestrator: the allowlist is a constant in scripts/check_conflict_markers.py, starts empty, travels with the kit as mechanism, names exact tracked paths only, and changes only through a reviewed pull request | — |
| S-4 | MINOR | SPEC | base | `spec.md` Open decisions bullet 4; AC5 ("a non-repository root"); AC6 ("a command different from the declared one"); Protected areas, last sentence | Missing: the `decisions/gates.yaml` schema requires `cost` (seconds or minutes), which decides whether the gate runs before admission or inside the verify slot. The spec gives job, placement, subset, floor and enforcement, but not cost. It also never states the declared command string, including whether the check takes a root argument (AC5 names a "non-repository root") or uses the working directory. AC6's refutation, and the gate-metadata mutation test it implies, compare against that string. The orchestrator alone writes the entry, so the implementer's test and the orchestrator's entry must agree on values the spec leaves open. | Opus | in spec — [DETAIL] decided by the orchestrator: declared cost in seconds, measured once on the change; it runs before admission with the other cheap document gates; the declared command is named in the spec | — |
| S-5 | MINOR | SPEC | base | `spec.md` AC4 ("When Git's whitespace/error check reports a fault" vs refutation "a trailing-whitespace fault passes in either change layer") | [AMBIGUITY] `git diff --check` follows `core.whitespace` from the invoking user's global and system config and the `whitespace` gitattribute. Reading A: the check reports whatever the local Git configuration flags, so on a machine with `core.whitespace=-blank-at-eol` trailing whitespace passes and the verdict depends on the machine. Reading B: the check pins Git's default rules, using a config override and isolated config, so trailing whitespace fails everywhere. The two readings lead to different implementations and different refuting cases. | Opus | in spec — [DETAIL] decided by the orchestrator: the gate runs git diff --check with a fixed core.whitespace value passed on the command line, so the user's global and system Git configuration cannot change the verdict; gitattributes in the repository still apply | — |

Stage-2 call, 2026-11-22: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1171 files, 5384 commits, 12 rules.

> Attempt 1 (codex) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/conflict-marker-gate/draft-attempt-1-20261122T155017349605Z (0274e81e5f59); `git diff 5e44bc0455b8 refs/stage2/attempts/conflict-marker-gate/draft-attempt-1-20261122T155017349605Z` shows it.

Stage-2 call, 2026-11-22: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1171 files, 5384 commits, 12 rules.

> Attempt 2 (codex-repair) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/conflict-marker-gate/draft-attempt-2-20261122T155028524517Z (00f073258976); `git diff 5e44bc0455b8 refs/stage2/attempts/conflict-marker-gate/draft-attempt-2-20261122T155028524517Z` shows it.

Stage-2 call, 2026-11-22: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 1171 files, 5384 commits, 12 rules.

Stage-2 call, 2026-11-22: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1171 files, 5386 commits, 12 rules.

Stage-2 call, 2026-11-22: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1171 files, 5388 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-22

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-6 | MAJOR | SPEC | base | `spec.md` AC7 ("leaves … Git's staging area … unchanged"; refuted by "moves the staging area"); AC2 ("without changing repository content or refs"); Open decisions, bullet "Unchanged-by-merge wording (S-2)" | [AMBIGUITY] The S-2 decision says which index is meant, but not what "unchanged" is compared against. Reading A: the staged entries are the same before and after, as `git ls-files -s` or `git write-tree` shows. The current helper passes this. Reading B: `.git/index` is byte-identical. `merge_main` runs `ensure_clean` (`git status --porcelain`) before it reports a conflict. `git status` rewrites the index file when entries are racily clean, which they are in a disposable-repo test that commits and runs within the same second. Under B, an AC7 regression test fails on unchanged code, and it can only pass by editing the protected `scripts/pr_sync.py`. AC2 has the same split for the check itself: its worktree `git diff --check` may write a refreshed stat cache, which breaks AC2 under B and not under A. | Opus | in spec — [DETAIL] decided by the orchestrator: reading A; unchanged means the same staged entries before and after (git ls-files -s), not a byte-identical .git/index | — |
| S-7 | MAJOR | SPEC | fix-r1 | `spec.md` AC4 ("a user's global and system Git configuration cannot change the verdict while repository `.gitattributes` still apply"; refuted by "a machine whose Git configuration disables a whitespace rule"); Open decisions, bullet "Whitespace verdict (S-5)" | [AMBIGUITY] The S-5 decision pins only `core.whitespace` with `-c`. `git diff --check` also obeys the `whitespace` attribute from the global attributes file (`core.attributesFile`, by default `~/.config/git/attributes`), from the system `gitattributes` and from `.git/info/attributes`, and that attribute overrides `core.whitespace` per path. A global `core.autocrlf` also decides whether a trailing CR on an unstaged CRLF line is reported. Reading A: "Git configuration" means config variables only, so a machine with `* -whitespace` in its global attributes file may pass trailing whitespace, and the refutation does not cover that. Reading B: the verdict must not depend on the machine, so the check must also neutralise global and system attributes and config. Under B the spec must also say whether the untracked `.git/info/attributes` counts as "repository `.gitattributes`". A test that plants a global attributes file goes red under B against an implementation built exactly to the stated mechanism. | Opus | in spec — [DETAIL] decided by the orchestrator: the gate also neutralises attribute sources outside the repository (core.attributesFile set empty on the command line, GIT_ATTR_NOSYSTEM=1); .git/info/attributes and the committed .gitattributes still apply | — |
| S-8 | MINOR | SPEC | fix-r1 | `spec.md` Open decisions, bullet "Helper (S-1)" and the sentence "its status stands in `findings.md`"; DoD "Move together"; `findings.md` S-1 Status | [AMBIGUITY] The S-1 status that the spec points to says the change "names it in docs/WORKFLOW.md as the orchestrator's one way to merge main into a change branch". The spec instead says merge-main is "already named in `docs/WORKFLOW.md` §3 … not rebuilt", and `docs/WORKFLOW.md` is not on the "Move together" list. Reading A: no doctrine edit, because §3's existing "supported local merge" sentence is enough, and the pull request touches no workflow document. Reading B: the change adds wording that makes merge-main the orchestrator's required way to merge main into a change branch. That is the gap the `31d35400` trigger exposed. Under B, `docs/WORKFLOW.md` (kit mechanism) and possibly its portable form `templates/agents-mergeable-prs.md` join a file list that the DoD says demonstrates the scope. | Opus | in spec — [DETAIL] decided by the orchestrator: reading A; no doctrine edit, the existing supported-local-merge sentence in docs/WORKFLOW.md §3 names merge-main; the S-1 status wording is superseded by this | — |

Stage-2 call, 2026-11-22: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1171 files, 5389 commits, 12 rules.

> Attempt 1 (codex) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/conflict-marker-gate/draft-attempt-1-20261122T182613975018Z (2fbc8a5f370a); `git diff 21a30f1c1ae7 refs/stage2/attempts/conflict-marker-gate/draft-attempt-1-20261122T182613975018Z` shows it.

Stage-2 call, 2026-11-22: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1171 files, 5389 commits, 12 rules.

> Attempt 2 (codex-repair) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/conflict-marker-gate/draft-attempt-2-20261122T182628863827Z (f8cdc8dacc7c); `git diff 21a30f1c1ae7 refs/stage2/attempts/conflict-marker-gate/draft-attempt-2-20261122T182628863827Z` shows it.

Stage-2 call, 2026-11-22: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 1171 files, 5389 commits, 12 rules.

Stage-2 call, 2026-11-22: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1171 files, 5390 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-22

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-9 | MAJOR | SPEC | fix-r2 | `spec.md` AC4 (body "the verdict is identical whatever the invoking user's global and system Git configuration … say" vs refutation "… configuration or attribute files disable a whitespace rule"); Open decisions, bullets "Whitespace verdict (S-5)" and "Attribute sources outside the repository (S-7)" | [AMBIGUITY] The decided mechanism pins `core.whitespace`, empties `core.attributesFile` and sets `GIT_ATTR_NOSYSTEM=1`. Other global or system configuration still changes what `git diff --check` compares, most plainly `core.autocrlf` and `core.eol`. With global `core.autocrlf=true`, Git converts a CRLF line added to an unstaged change in a file committed with LF before diffing, so no fault is reported. Without it, the trailing CR is reported as `blank-at-eol`. S-7 named `core.autocrlf`, but its decision covered attribute sources only. Reading A: the three listed means are the whole requirement, and the body's "whatever … configuration" is read through the narrower refutation ("disable a whitespace rule"). The CRLF case then stays machine-dependent and AC4 holds. Reading B: the body governs, so the check must also neutralise line-ending and filter configuration. It can do that per variable or by isolating global and system configuration wholesale (`GIT_CONFIG_GLOBAL`, `GIT_CONFIG_NOSYSTEM`), which also drops settings a checkout may rely on, such as `safe.directory`. Refuting case under B: `GIT_CONFIG_GLOBAL` names a file with `core.autocrlf=true`, and an unstaged change adds a CRLF line. An implementation built exactly to the listed mechanism stays green there, which refutes AC4. | Opus | in spec — [DETAIL] decided by the orchestrator: the gate runs every git call with GIT_CONFIG_GLOBAL=/dev/null and GIT_CONFIG_NOSYSTEM=1 in addition to the S-5/S-7 settings, so no global or system configuration of any kind reaches the verdict; repository configuration and committed attributes still apply | — |
| S-10 | MINOR | SPEC | base | `spec.md` Terms "Tracked text" (no NUL byte anywhere); AC3 ("binary files … do not cause marker findings"; refuted by "a binary … marker is scanned"); AC4 ("reports a fault in staged or unstaged changes … the check fails with its diagnostic") | [AMBIGUITY] The spec calls a file binary when it holds a NUL byte anywhere. `git diff --check` treats a file as binary only when a NUL appears in its first 8000 bytes or an attribute marks it binary. Planted input: a staged or unstaged change adds a `<<<<<<< x` line to a file whose first NUL comes after byte 8000. Git reports "leftover conflict marker" for that file, but the spec classes the file as binary. Reading A: AC4 governs, so every `git diff --check` fault fails the check. This binary file then causes a marker finding, which refutes AC3. Reading B: AC3 governs, so the check must drop Git's marker diagnostics for paths it classes as binary. That needs a per-path filter over Git's output that AC4 does not mention, and it refutes AC4's "fails with its diagnostic". The two readings lead to different code and opposite verdicts for the same planted file. | Opus | in spec — [DETAIL] decided by the orchestrator: binary follows Git's own definition (a NUL byte in the first 8000 bytes, or a binary attribute) for both the marker scan and the whitespace check, so the two never disagree | — |

Stage-2 call, 2026-11-22: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1171 files, 5392 commits, 12 rules.

> Attempt 1 (codex) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/conflict-marker-gate/draft-attempt-1-20261122T204659101373Z (dc4326aa6cc0); `git diff 0db5abf6d256 refs/stage2/attempts/conflict-marker-gate/draft-attempt-1-20261122T204659101373Z` shows it.

Stage-2 call, 2026-11-22: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1171 files, 5392 commits, 12 rules.

> Attempt 2 (codex-repair) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/conflict-marker-gate/draft-attempt-2-20261122T204710371923Z (14325cc06d1d); `git diff 0db5abf6d256 refs/stage2/attempts/conflict-marker-gate/draft-attempt-2-20261122T204710371923Z` shows it.

Stage-2 call, 2026-11-22: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 1171 files, 5392 commits, 12 rules.

Stage-2 call, 2026-11-22: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1171 files, 5404 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/check_conflict_markers.py` +230 -0
> - `scripts/kit/manifest.yaml` +6 -0
> - `tests/test_check_conflict_markers.py` +462 -0
> - `tests/test_pr_sync.py` +13 -5
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `scripts/check_conflict_markers.py`, `tests/test_pr_sync.py`.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>         # A tracked symlink whose target carries the markers — the target itself stays untracked,
>         # so a scanner that follows the link would scan text Git does not track at that path.
>         _write(root, "elsewhere.txt", "<<<<<<< target\n")
>         os.symlink("elsewhere.txt", root / "link")
>         _git(root, "add", "link")
>         _git(root, "commit", "--quiet", "-m", "tracks a symlink")
>         # A gitlink entry in the index without any submodule checkout.
>         blob = _git(root, "hash-object", "-w", "README.md").strip()
>         _git(root, "update-index", "--add", "--cacheinfo", f"160000,{blob},sub")
>         _git(root, "commit", "--quiet", "-m", "registers a submodule without a checkout")
>         # A tracked path deleted from the worktree, still in the index.
>         _write(root, "docs/gone.md", "content\n")
>         _git(root, "add", "docs/gone.md")
>         _git(root, "commit", "--quiet", "-m", "adds a file that is then deleted")
>         (root / "docs" / "gone.md").unlink()
> >       assert _run_gate(root).returncode == 0, "none of the non-text entries may be scanned"
> E       AssertionError: none of the non-text entries may be scanned
> E       assert 2 == 0
> E        +  where 2 = CompletedProcess(args=['/Users/mikypiky/coding-harness/.claude/worktrees/conflict-marker-gate/.venv/bin/python3', 'scr...ikypiky/pytest-3242/popen-gw1/test_non_text_and_absent_entri0/entries/docs/gone.md'; it was not measured\n", stderr='').returncode
> E        +    where CompletedProcess(args=['/Users/mikypiky/coding-harness/.claude/worktrees/conflict-marker-gate/.venv/bin/python3', 'scr...ikypiky/pytest-3242/popen-gw1/test_non_text_and_absent_entri0/entries/docs/gone.md'; it was not measured\n", stderr='') = _run_gate(PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3242/popen-gw1/test_non_text_and_absent_entri0/entries'))
>
> tests/test_check_conflict_markers.py:270: AssertionError
> ______________ test_gate_goes_red_when_inspection_cannot_complete ______________
> [gw3] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/conflict-marker-gate/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3242/popen-gw3/test_gate_goes_red_when_inspec0')
>
>     def test_gate_goes_red_when_inspection_cannot_complete(tmp_path: Path) -> None:
>         """A non-repository root, a failed Git command and an unreadable tracked
>         file each fail the check and say what was not measured."""
>         done = _run_gate(tmp_path / "nowhere")
>         assert done.returncode == 2, done.stdout + done.stderr
>         assert "not measured" in done.stdout or "not a Git work tree" in done.stdout, done.stdout
>     
>         plain = tmp_path / "plain"
>         plain.mkdir()
>         done = _run_gate(plain)
>         assert done.returncode == 2, done.stdout + done.stderr
>         assert "not a Git work tree" in done.stdout, done.stdout
>     
>         root = _repo(tmp_path, "inspection")
>         _write(root, "docs/note.md", "readable\n")
>         _commit(root, "clean base")
>         assert _run_gate(root).returncode == 0
>     
>         real_git = shutil.which("git")
>         assert real_git, "the shim leg needs a real git to delegate to"
>         failing = tmp_path / "shim-failing"
>         failing.mkdir()
>         shim = failing / "git"
>         shim.write_text(
>             f'#!/bin/sh\nif [ "$1" = "ls-files" ]; then echo "shim: ls-files refused" >&2; exit 7; fi\nexec "{real_git}" "$@"\n',
>             encoding="utf-8",
>         )
>         shim.chmod(0o755)
>         delegating = tmp_path / "shim-ok"
>         delegating.mkdir()
>         passing = delegating / "git"
>         passing.write_text(f'#!/bin/sh\nexec "{real_git}" "$@"\n', encoding="utf-8")
>         passing.chmod(0o755)
>         shim_env = {**os.environ, "PATH": f"{failing}{os.pathsep}{os.environ['PATH']}"}
>         done = _run_gate(root, env=shim_env)
> >       assert done.returncode == 2, done.stdout + done.stderr
> E       AssertionError: conflict-markers: measured pass — no marker line in tracked text, no whitespace fault in the changes
> E         OK — no deviation.
> E         
> E       assert 0 == 2
> E        +  where 0 = CompletedProcess(args=['/Users/mikypiky/coding-harness/.claude/worktrees/conflict-marker-gate/.venv/bin/python3', 'scr...: measured pass — no marker line in tracked text, no whitespace fault in the changes\nOK — no deviation.\n', stderr='').returncode
>
> tests/test_check_conflict_markers.py:378: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_check_conflict_markers.py::test_reports_all_marker_locations_without_writes
> FAILED tests/test_check_conflict_markers.py::test_gate_is_blocking_in_every_verification_path
> FAILED tests/test_check_conflict_markers.py::test_gate_goes_red_when_committed_text_contains_markers[>>>>>>>- topic]
> FAILED tests/test_check_conflict_markers.py::test_committed_marker_forms_in_every_kind_of_text
> FAILED tests/test_check_conflict_markers.py::test_gate_goes_red_when_committed_text_contains_markers[>>>>>>>-]
> FAILED tests/test_check_conflict_markers.py::test_only_tracked_text_and_exact_fixture_names_are_measured
> FAILED tests/test_check_conflict_markers.py::test_non_text_and_absent_entries_are_not_scanned
> FAILED tests/test_check_conflict_markers.py::test_gate_goes_red_when_inspection_cannot_complete
> 8 failed, 13 passed in 1.86s
> ```

Stage-2 call, 2026-11-22: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 1173 files, 5408 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/conflict-marker-gate/plan.md` +8 -8
> - `scripts/check_conflict_markers.py` +13 -4
> - `tests/test_check_conflict_markers.py` +94 -17
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `tests/test_check_conflict_markers.py`.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> .............F.......                                                    [100%]
> =================================== FAILURES ===================================
> _______________ test_gate_is_blocking_in_every_verification_path _______________
> [gw4] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/conflict-marker-gate/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3244/popen-gw4/test_gate_is_blocking_in_every0')
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x10904e930>
>
>     def test_gate_is_blocking_in_every_verification_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
>         """The declared entry derives blocking on every verification path — the
>         full local verify job, its docs subset ahead of every minutes gate, and the
>         hosted workflow without an advisory valve.
>     
>         The held gate list belongs to the orchestrator bootstrap (plan step 5),
>         so the derivation is proven against a gate file that carries the
>         declaration beside this repository's real list; once the bootstrap has
>         registered the entry, the real list and the generated workflow must carry
>         exactly it.
>         """
>         real_doc = yaml.safe_load((REPO_ROOT / "decisions" / "gates.yaml").read_text(encoding="utf-8"))
>         registered = next((entry for entry in real_doc["gates"] if entry["id"] == "conflict-markers"), None)
>         gates_list = [*real_doc["gates"]]
>         if registered is None:
>             gates_list.append(yaml.safe_load(DECLARED_ENTRY))
>     
>         root = tmp_path / "gate-list"
>         (root / "decisions").mkdir(parents=True)
>         gate_file = root / "decisions" / "gates.yaml"
>         gate_file.write_text(yaml.safe_dump({**real_doc, "gates": gates_list}, sort_keys=False), encoding="utf-8")
>         monkeypatch.setattr(ci_gates, "GATE_FILE", gate_file)
>     
> >       gate = next((entry for entry in ci_gates.gates() if entry["id"] == "conflict-markers"), None)
>
> tests/test_check_conflict_markers.py:451: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> scripts/ci_gates.py:506: in gates
>     return _gates_aus(GATE_FILE)
> scripts/ci_gates.py:466: in _gates_aus
>     fehler = validate_schema(doc)
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> doc = {'gates': [{'command': 'python3 -m pytest tests/ -q -n auto', 'cost': 'minutes', 'enforcement': 'block', 'floor': True...'enforcement': 'report', 'floor': False, ...}, ...], 'retired': [], 'schema_version': 3, 'tools': {'python': ['3.12']}}
>
>     def validate_schema(doc: dict[str, Any] | None = None) -> list[str]:
>         """Prueft die Gate-Datei gegen ihr Schema. Liefert Fehler, leer = ok."""
>         if doc is None:
>             if not GATE_FILE.is_file():
>                 return [f"Gate-Datei fehlt: {GATE_FILE}"]
>             doc = yaml.safe_load(GATE_FILE.read_text(encoding="utf-8"))
>         fehler: list[str] = []
>         if not isinstance(doc, dict):
>             return ["die Gate-Datei ist kein Mapping"]
>         version = doc.get("schema_version")
>         if type(version) is not int or version != SCHEMA_VERSION:
>             fehler.append(f"schema_version muss {SCHEMA_VERSION} sein, ist {version!r}")
>         fehler.extend(_tools_fehler(doc.get("tools")))
>         gate_liste = doc.get("gates")
>         if not isinstance(gate_liste, list) or not gate_liste:
>             fehler.append("'gates' fehlt oder ist leer")
>             return fehler
>         bekannt: set[str] = set()
>         for g in gate_liste:
> >           gid = g.get("id")
> E           AttributeError: 'list' object has no attribute 'get'
>
> scripts/ci_gates.py:380: AttributeError
> =========================== short test summary info ============================
> FAILED tests/test_check_conflict_markers.py::test_gate_is_blocking_in_every_verification_path
> 1 failed, 20 passed in 1.45s
> ```

Stage-2 call, 2026-11-22: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 1173 files, 5408 commits, 12 rules.

Stage-2 call, 2026-11-23: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1177 files, 5410 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/check_conflict_markers.py` +275 -0
> - `scripts/kit/manifest.yaml` +6 -0
> - `tests/test_check_conflict_markers.py` +504 -0
> - `tests/test_pr_sync.py` +17 -6
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `tests/test_check_conflict_markers.py`; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before post-run verification: `.venv/bin/ruff check` exited 1
> tests/test_check_conflict_markers.py:458:9: SIM108 Use ternary operator `covered = path.startswith(prefix) if prefix.endswith("/") else path == prefix or path.startswith(prefix + "/")` instead of `if`-`else`-block
>     |
> 456 |       for rule in manifest.get("rules", []):
> 457 |           prefix = rule.get("prefix", "")
> 458 | /         if prefix.endswith("/"):
> 459 | |             covered = path.startswith(prefix)
> 460 | |         else:
> 461 | |             covered = path == prefix or path.startswith(prefix + "/")
>     | |_____________________________________________________________________^ SIM108
> 462 |           if covered and (best is None or len(prefix) > len(best.get("prefix", ""))):
> 463 |               best = rule
>     |
>     = help: Replace `if`-`else`-block with `covered = path.startswith(prefix) if prefix.endswith("/") else path == prefix or path.startswith(prefix + "/")`
>
> Found 1 error.
> No fixes available (1 hidden fix can be enabled with the `--unsafe-fixes` option).
> ```

Stage-2 call, 2026-11-23: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 1179 files, 5416 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_check_conflict_markers.py` +10 -11
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>
> tests/test_check_conflict_markers.py:492: AssertionError
> ______________ test_gate_goes_red_when_inspection_cannot_complete ______________
> [gw1] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/conflict-marker-gate/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3255/popen-gw1/test_gate_goes_red_when_inspec0')
>
>     def test_gate_goes_red_when_inspection_cannot_complete(tmp_path: Path) -> None:
>         """A non-repository root, a failed Git command and an unreadable tracked
>         file each produce an unsuccessful exit that explains what was not
>         measured; the controls pass."""
>         passed = _run_gate(_repo(tmp_path / "control"))
>         assert passed.returncode == 0, passed.stdout + passed.stderr
>     
>         nowhere = _run_gate(tmp_path / "nowhere")
>         assert nowhere.returncode == 2, nowhere.stdout + nowhere.stderr
>         assert "not a Git work tree" in nowhere.stdout
>     
>         plain_dir = tmp_path / "plain-dir"
>         plain_dir.mkdir()
>         bare = _run_gate(plain_dir)
>         assert bare.returncode == 2, bare.stdout + bare.stderr
>         assert "not a Git work tree" in bare.stdout
>     
>         real_git = shutil.which("git")
>         assert real_git, "git must be on the path for these fixtures"
>         refusing_dir = tmp_path / "shim-refusing"
>         refusing_dir.mkdir()
>         refusing = refusing_dir / "git"
>         refusing.write_text(
>             "#!/bin/sh\n"
>             'for arg in "$@"; do\n'
>             '  if [ "$arg" = "ls-files" ]; then\n'
>             '    echo "shim: ls-files refused" >&2\n'
>             "    exit 7\n"
>             "  fi\n"
>             "done\n"
>             f'exec "{real_git}" "$@"\n',
>             encoding="utf-8",
>         )
>         refusing.chmod(0o755)
>         refusing_env = {**os.environ, "PATH": f"{refusing_dir}{os.pathsep}{os.environ.get('PATH', '')}"}
>         committed = _repo(tmp_path / "committed")
>         _write(committed, "docs/note.md", "readable\n")
>         _commit(committed, "a readable file")
>         shimmed = _run_gate(committed, env=refusing_env)
>         assert shimmed.returncode == 2, shimmed.stdout + shimmed.stderr
>         assert "not measured" in shimmed.stdout, "a failed Git command produced a successful report"
>     
>         delegating_dir = tmp_path / "shim-delegating"
>         delegating_dir.mkdir()
>         delegating = delegating_dir / "git"
>         delegating.write_text(f'#!/bin/sh\nexec "{real_git}" "$@"\n', encoding="utf-8")
>         delegating.chmod(0o755)
>         passing_env = {**os.environ, "PATH": f"{delegating_dir}{os.pathsep}{os.environ.get('PATH', '')}"}
>         passed_through = _run_gate(committed, env=passing_env)
> >       assert passed_through.returncode == 0, passed_through.stdout + passed_through.stderr
> E       AssertionError: BLOCK (1):
> E           - git diff --check could not be read (  -a  --text    treat all files as text.)
> E               the repository was not measured
> E         
> E       assert 2 == 0
> E        +  where 2 = CompletedProcess(args=['/Users/mikypiky/coding-harness/.claude/worktrees/conflict-marker-gate/.venv/bin/python3', '/Us...heck could not be read (  -a  --text    treat all files as text.)\n      the repository was not measured\n', stderr='').returncode
>
> tests/test_check_conflict_markers.py:391: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_check_conflict_markers.py::test_gate_goes_red_when_committed_text_contains_markers[>>>>>>>- topic]
> FAILED tests/test_check_conflict_markers.py::test_gate_goes_red_when_committed_text_contains_markers[=======-]
> FAILED tests/test_check_conflict_markers.py::test_gate_goes_red_when_committed_text_contains_markers[>>>>>>>-!! longer]
> FAILED tests/test_check_conflict_markers.py::test_gate_goes_red_when_committed_text_contains_markers[<<<<<<<-]
> FAILED tests/test_check_conflict_markers.py::test_gate_goes_red_when_committed_text_contains_markers[=======- topic]
> FAILED tests/test_check_conflict_markers.py::test_gate_goes_red_when_committed_text_contains_markers[<<<<<<<- topic]
> FAILED tests/test_check_conflict_markers.py::test_gate_goes_red_when_committed_text_contains_markers[<<<<<<<-!! longer]
> FAILED tests/test_check_conflict_markers.py::test_gate_goes_red_when_committed_text_contains_markers[>>>>>>>-]
> FAILED tests/test_check_conflict_markers.py::test_gate_goes_red_when_committed_text_contains_markers[=======-!! longer]
> FAILED tests/test_check_conflict_markers.py::test_only_tracked_text_and_exact_fixture_names_are_measured
> FAILED tests/test_check_conflict_markers.py::test_gate_goes_red_when_git_diff_check_finds_a_fault
> FAILED tests/test_check_conflict_markers.py::test_gate_goes_red_when_an_allowlist_entry_names_no_tracked_path
> FAILED tests/test_check_conflict_markers.py::test_gate_goes_red_when_inspection_cannot_complete
> 13 failed, 6 passed in 1.32s
> ```

Stage-2 call, 2026-11-23: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 1179 files, 5418 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/conflict-marker-gate/plan.md` +8 -8
> - `scripts/check_conflict_markers.py` +23 -17
>
> Diagnostics:
> ````text
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: red) because the targeted coverage was not safe: `scripts/kit/manifest.yaml` is an input kind the targeted selector does not cover
> - `make verify` exited 1
> The gates that blocked, each with its last lines:
> ── [pytest] $ python3 -m pytest tests/ -q -n auto
> [… 90 lines of this gate left out …]
> ........................................................................ [ 93%]
> ........................................................................ [ 94%]
> ........................................................................ [ 95%]
> ........................................................................ [ 96%]
> ........................................................................ [ 97%]
> ........................................................................ [ 98%]
> ........................................................................ [ 99%]
> ..............................                                           [100%]
> =================================== FAILURES ===================================
> _____________ test_every_script_has_a_caller_or_a_declared_reason ______________
> [gw2] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/conflict-marker-gate/.venv/bin/python3
>
>     def test_every_script_has_a_caller_or_a_declared_reason() -> None:
>         """A tool without a caller cannot be told apart from a forgotten one.
>     
>         On 2026-08-14, nine of twenty-one scripts had none — and nowhere did it say
>         which of them were intentional. Since then the rule is: every script —
>         `*.py` as well as `*.sh` — stands either in a `run:` step (`ci.yml`, both
>         jobs) or in `ci_gates.OHNE_AUFRUFER` with a reason (RB-G3).
>     
>         `ci_gates.py` itself is the caller of the local runner; it counts as wired
>         as soon as `verify_all.sh` starts it.
>         """
>         from ci_gates import OHNE_AUFRUFER
>     
>         ci = CI_FILE.read_text(encoding="utf-8")
>         runner = RUNNER.read_text(encoding="utf-8")
>     
>         heimatlos = _heimatlose_namen([p.name for p in _scripts()], ci, runner, OHNE_AUFRUFER)
> >       assert not heimatlos, (
>             "Without a caller and without a reason:\n  "
>             + "\n  ".join(heimatlos)
>             + "\n\nEither a step in ci.yml or a line in ci_gates.OHNE_AUFRUFER."
>         )
> E       AssertionError: Without a caller and without a reason:
> E           check_conflict_markers.py
> E         
> E         Either a step in ci.yml or a line in ci_gates.OHNE_AUFRUFER.
> E       assert not ['check_conflict_markers.py']
>
> tests/test_ci.py:3569: AssertionError
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=21809) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/conflict-marker-gate/tests/test_stage2.py:24881: DeprecationWarning: This process (pid=21810) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_ci.py::test_every_script_has_a_caller_or_a_declared_reason
> 1 failed, 6780 passed, 17 skipped, 5 warnings in 628.91s (0:10:28)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 53770 earlier lines left out …]
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
> ````
