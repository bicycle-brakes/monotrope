---
title: "Findings — bd-1-3-4"
category: findings
status: draft
implementation_status: none
date: 2026-11-14
created: 2026-11-14
last_reviewed: 2026-11-14
updated: 2026-11-15
supersedes: null
superseded_by: null
bead: coding-harness-tr84
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — bd-1-3-4

Stage-2 call, 2026-11-14: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 1073 files, 4223 commits, 12 rules.

Stage-2 call, 2026-11-14: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1076 files, 4226 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/bd-1-3-4/plan.md` +8 -8
> - `tests/test_beads_install.py` +564 -0
> - `tools/beads/VERSION` +1 -1
> - `tools/beads/install.sh` +1 -1
> - `tools/cloud-env/README.md` +6 -4
> - `tools/cloud-env/setup.sh` +5 -3
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `tests/test_beads_install.py`; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before post-run verification: `.venv/bin/ruff check` exited 1
> tests/test_beads_install.py:355:5: F841 Local variable `pin` is assigned to but never used
>     |
> 353 |     dispatched — not the versioned one, not the one on PATH, and not even when
> 354 |     BD_PIN_BYPASS=1 asks for the blocked verbs' escape hatch."""
> 355 |     pin = _pin()
>     |     ^^^ F841
> 356 |     ns = _sandbox(tmp_path)
> 357 |     log = tmp_path / "mismatching-bd.log"
>     |
>     = help: Remove assignment to unused variable `pin`
>
> Found 1 error.
> No fixes available (1 hidden fix can be enabled with the `--unsafe-fixes` option).
> ```

Stage-2 call, 2026-11-14: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 1077 files, 4237 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/bd-1-3-4/plan.md` +8 -8
> - `tests/test_beads_install.py` +6 -3
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>     
>             self._close_pipe_fds(p2cread, p2cwrite,
>                                  c2pread, c2pwrite,
>                                  errread, errwrite)
>     
>             # Wait for exec to fail or succeed; possibly raising an
>             # exception (limited in size)
>             errpipe_data = bytearray()
>             while True:
>                 part = os.read(errpipe_read, 50000)
>                 errpipe_data += part
>                 if not part or len(errpipe_data) > 50000:
>                     break
>         finally:
>             # be sure the FD is closed no matter what
>             os.close(errpipe_read)
>     
>         if errpipe_data:
>             try:
>                 pid, sts = os.waitpid(self.pid, 0)
>                 if pid == self.pid:
>                     self._handle_exitstatus(sts)
>                 else:
>                     self.returncode = sys.maxsize
>             except ChildProcessError:
>                 pass
>     
>             try:
>                 exception_name, hex_errno, err_msg = (
>                         errpipe_data.split(b':', 2))
>                 # The encoding here should match the encoding
>                 # written in by the subprocess implementations
>                 # like _posixsubprocess
>                 err_msg = err_msg.decode()
>             except ValueError:
>                 exception_name = b'SubprocessError'
>                 hex_errno = b'0'
>                 err_msg = 'Bad exception data from child: {!r}'.format(
>                               bytes(errpipe_data))
>             child_exception_type = getattr(
>                     builtins, exception_name.decode('ascii'),
>                     SubprocessError)
>             if issubclass(child_exception_type, OSError) and hex_errno:
>                 errno_num = int(hex_errno, 16)
>                 if err_msg == "noexec:chdir":
>                     err_msg = ""
>                     # The error must be from chdir(cwd).
>                     err_filename = cwd
>                 elif err_msg == "noexec":
>                     err_msg = ""
>                     err_filename = None
>                 else:
>                     err_filename = orig_executable
>                 if errno_num != 0:
>                     err_msg = os.strerror(errno_num)
>                 if err_filename is not None:
> >                   raise child_exception_type(errno_num, err_msg, err_filename)
> E                   FileNotFoundError: [Errno 2] No such file or directory: 'bash'
>
> /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/subprocess.py:1955: FileNotFoundError
> =========================== short test summary info ============================
> FAILED tests/test_beads_install.py::test_wrapper_selects_pinned_versioned_binary
> FAILED tests/test_beads_install.py::test_wrapper_blocks_schema_verbs[init] - ...
> FAILED tests/test_beads_install.py::test_wrapper_refuses_version_mismatch[versioned-binary-True]
> FAILED tests/test_beads_install.py::test_wrapper_blocks_schema_verbs[migrate]
> FAILED tests/test_beads_install.py::test_wrapper_refuses_version_mismatch[path-binary-False]
> FAILED tests/test_beads_install.py::test_wrapper_blocks_schema_verbs[upgrade]
> FAILED tests/test_beads_install.py::test_cloud_pin_and_checksum_match_repository
> FAILED tests/test_beads_install.py::test_wrapper_refuses_version_mismatch[versioned-binary-False]
> FAILED tests/test_beads_install.py::test_install_routes_request_canonical_release[installer-Darwin-arm64]
> FAILED tests/test_beads_install.py::test_wrapper_missing_binary_exits_127 - F...
> FAILED tests/test_beads_install.py::test_install_routes_request_canonical_release[installer-Linux-amd64]
> FAILED tests/test_beads_install.py::test_install_routes_refuse_unverified_archive[installer-missing-checksum]
> FAILED tests/test_beads_install.py::test_install_routes_install_verified_archive[installer-Linux-amd64]
> FAILED tests/test_beads_install.py::test_install_routes_refuse_unverified_archive[installer-wrong-digest]
> FAILED tests/test_beads_install.py::test_install_routes_refuse_unverified_archive[cloud-wrong-digest]
> FAILED tests/test_beads_install.py::test_install_routes_request_canonical_release[cloud-Linux-amd64]
> FAILED tests/test_beads_install.py::test_install_routes_install_verified_archive[cloud-Linux-amd64]
> FAILED tests/test_beads_install.py::test_install_routes_install_verified_archive[installer-Darwin-arm64]
> 18 failed in 1.12s
> ```

Stage-2 call, 2026-11-14: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 1077 files, 4243 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/bd-1-3-4/plan.md` +8 -8
> - `tests/test_beads_install.py` +7 -1
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> ........F.........                                                       [100%]
> =================================== FAILURES ===================================
> _________________ test_cloud_pin_and_checksum_match_repository _________________
> [gw6] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/bd-1-3-4/.venv/bin/python3
>
>     def test_cloud_pin_and_checksum_match_repository() -> None:
>         """Criterion 4: the standalone cloud setup carries the repository's pin and
>         the very digest its referenced checksum file commits — so the two
>         installation routes cannot drift apart while both look maintained."""
>         pin = _pin()
>         text = SETUP.read_text(encoding="utf-8")
>         version = re.search(r"^BD_VERSION=(\S+)", text, re.M)
>         assert version is not None, "the cloud setup declares no BD_VERSION"
>         assert version.group(1) == pin, f"the cloud setup installs bd {version.group(1)}, the repository pins {pin}"
>         line = re.search(r"^BD_SHA256=([0-9a-f]{64})(.*)$", text, re.M)
>         assert line is not None, "the cloud setup declares no 64-hex-digit BD_SHA256"
>         referenced = re.search(r"tools/beads/checksums/(\S+\.sha256)", line.group(2))
>         assert referenced is not None, "the BD_SHA256 line names no repository checksum file it should equal"
>         name = f"beads_{pin}_linux_amd64.tar.gz.sha256"
>         assert referenced.group(1) == name, f"the cloud checksum comment names {referenced.group(1)}, not the pinned {name}"
>         sums = REPO_ROOT / "tools" / "beads" / "checksums" / name
> >       assert sums.is_file(), (
>             f"{sums.relative_to(REPO_ROOT)} is missing — commit the verified v{pin} release digest first (bd-1-3-4)"
>         )
> E       AssertionError: tools/beads/checksums/beads_1.3.4_linux_amd64.tar.gz.sha256 is missing — commit the verified v1.3.4 release digest first (bd-1-3-4)
> E       assert False
> E        +  where False = is_file()
> E        +    where is_file = PosixPath('/Users/mikypiky/coding-harness/.claude/worktrees/bd-1-3-4/tools/beads/checksums/beads_1.3.4_linux_amd64.tar.gz.sha256').is_file
>
> tests/test_beads_install.py:564: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_beads_install.py::test_cloud_pin_and_checksum_match_repository
> 1 failed, 17 passed in 1.73s
> ```

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1079 files, 4255 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1079 files, 4255 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1079 files, 4255 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1079 files, 4255 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1079 files, 4255 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 1079 files, 4255 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1079 files, 4255 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1079 files, 4255 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 1079 files, 4255 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1079 files, 4255 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1079 files, 4255 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 1079 files, 4255 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 1079 files, 4255 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 1079 files, 4255 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 1079 files, 4255 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model step-5-preview · leak check clean over 1079 files, 4255 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 1079 files, 4255 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 1079 files, 4255 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 1079 files, 4255 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 1079 files, 4255 commits, 12 rules.

Stage-2 call, 2026-11-14: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1079 files, 4255 commits, 12 rules.

Stage-2 call, 2026-11-14: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1079 files, 4255 commits, 12 rules.

Stage-2 call, 2026-11-14: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1079 files, 4255 commits, 12 rules.

Stage-2 call, 2026-11-15: review-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1079 files, 4270 commits, 12 rules.

Stage-2 call, 2026-11-15: review-loop · endpoint opencode-go · model hy3 · leak check clean over 1079 files, 4387 commits, 12 rules.
