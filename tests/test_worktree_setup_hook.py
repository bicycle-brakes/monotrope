"""The checkout hook sets up a new worktree (bead coding-harness-wg4z).

Every test builds a throwaway repository whose `make`, `tools/pi/install.sh`,
`tools/pi/pi`, `.venv/bin/python3` and `bd` are stubs that record where and how
they ran, so nothing is downloaded. The hook sits in a shared directory named
by an absolute `core.hooksPath`, the layout a real main checkout uses: a new
worktree invokes that one copy, and the hook must still work in the worktree.

The hook under test is the versioned `.beads/hooks/post-checkout`, copied
unchanged into the shared hooks directory.
"""

from __future__ import annotations

import os
import re
import shutil
import stat
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
VERSIONED_HOOK = REPO / ".beads" / "hooks" / "post-checkout"
ZERO = "0" * 40
PIN = "1.2.3"


MAKE_STUB = r"""#!/bin/sh
if [ "$1" = "-C" ]; then cd "$2" || exit 1; shift 2; fi
printf '%s|%s\n' "$(pwd -P)" "$*" >>"$STUB_RECORD_DIR/make"
echo "STUB-MAKE-STDOUT"
echo "STUB-MAKE-STDERR" >&2
if [ -n "${STUB_MAKE_CHILD:-}" ]; then
  sleep "$STUB_MAKE_CHILD" &
  echo $! >"$STUB_RECORD_DIR/make-child"
fi
if [ -n "${STUB_MAKE_SLEEP:-}" ]; then
  sleep "$STUB_MAKE_SLEEP"
  echo woke >>"$STUB_RECORD_DIR/make-woke"
fi
if [ "${STUB_MAKE_NO_VENV:-}" != 1 ]; then
  mkdir -p .venv/bin
  cp "$STUB_PYTHON_TEMPLATE" .venv/bin/python3
  chmod +x .venv/bin/python3
fi
if [ "${STUB_MAKE_FAIL:-}" = 1 ]; then exit 1; fi
exit 0
"""

PYTHON_STUB = r"""#!/bin/sh
printf '%s|%s\n' "$(pwd -P)" "$*" >>"$STUB_RECORD_DIR/python"
echo "STUB-PYTHON-OUTPUT"
if [ "${STUB_YAML_FAIL:-}" = 1 ]; then
  echo "ModuleNotFoundError: No module named yaml" >&2
  exit 1
fi
exit 0
"""

INSTALL_STUB = r"""#!/bin/sh
here=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd -P)
printf '%s|%s\n' "$(pwd -P)" "$here" >>"$STUB_RECORD_DIR/install"
echo "STUB-INSTALL-OUTPUT"
if [ "${STUB_INSTALL_FAIL:-}" = 1 ]; then exit 1; fi
exit 0
"""

PI_STUB = r"""#!/bin/sh
printf '%s|%s\n' "$(pwd -P)" "$*" >>"$STUB_RECORD_DIR/pi"
if [ "${STUB_PI_FAIL:-}" = 1 ]; then echo "pi broke" >&2; exit 1; fi
printf '%s\n' "${STUB_PI_VERSION:-1.2.3}"
"""

BD_STUB = r"""#!/bin/sh
printf '%s\n' "$*" >>"$STUB_RECORD_DIR/bd"
exit "${STUB_BD_EXIT:-0}"
"""

PACKAGE_JSON = f'{{\n  "dependencies": {{\n    "@earendil-works/pi-coding-agent": "{PIN}"\n  }}\n}}\n'

SETUP_RECORDS = ("make", "install", "python", "pi")


def hook_text() -> str:
    """Read the versioned hook without altering it."""
    return VERSIONED_HOOK.read_text(encoding="utf-8")


def test_lane_setup_precedes_managed_block() -> None:
    text = hook_text()
    if os.environ.get("STAGE2_PLANT_FAULT") == "1":
        text = text.replace("BEGIN LANE SETUP", "REMOVED LANE SETUP")
    setup = text.find("# --- BEGIN LANE SETUP")
    setup_end = text.find("# --- END LANE SETUP")
    beads = text.find("# --- BEGIN BEADS INTEGRATION")
    assert 0 <= setup < setup_end < beads, "lane setup must be entirely above the managed block"


def test_managed_beads_block_matches_origin_main() -> None:
    original = subprocess.run(
        ["git", "show", "origin/main:.beads/hooks/post-checkout"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    text = hook_text()
    if os.environ.get("STAGE2_PLANT_FAULT") == "1":
        text = text.replace("This section is managed by beads.", "Changed managed block.")

    def managed_block(hook: str) -> str:
        begin = "# --- BEGIN BEADS INTEGRATION"
        end = "# --- END BEADS INTEGRATION"
        assert hook.count(begin) == 1 and hook.count(end) == 1, "managed block markers must be unique"
        start = hook.index(begin)
        finish = hook.index(end)
        assert start < finish, "managed block markers must be ordered"
        return hook[start:finish]

    assert managed_block(text) == managed_block(original), "Beads-managed block differs from origin/main"


def _write_exec(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


@dataclass
class Lane:
    main: Path
    hook: Path
    records: Path
    env: dict[str, str]
    root: Path

    def git(self, *args: str, cwd: Path | None = None, **extra: str):
        return subprocess.run(
            ["git", *args],
            cwd=cwd or self.main,
            env={**self.env, **extra},
            capture_output=True,
            text=True,
        )

    def add_worktree(self, name: str = "lane", **extra: str):
        path = self.root / name
        proc = self.git("worktree", "add", "-q", "-b", name, str(path), **extra)
        return proc, path

    def quiet_worktree(self, name: str = "lane") -> Path:
        path = self.root / name
        proc = subprocess.run(
            ["git", "-c", "core.hooksPath=/dev/null", "worktree", "add", "-q", "-b", name, str(path)],
            cwd=self.main,
            env=self.env,
            capture_output=True,
            text=True,
        )
        assert proc.returncode == 0, proc.stderr
        return path

    def head(self, cwd: Path) -> str:
        return self.git("rev-parse", "HEAD", cwd=cwd).stdout.strip()

    def run_hook(self, cwd: Path, *args: str, **extra: str):
        return subprocess.run(
            [str(self.hook), *args],
            cwd=cwd,
            env={**self.env, **extra},
            capture_output=True,
            text=True,
        )

    def new_worktree_hook(self, cwd: Path, **extra: str):
        return self.run_hook(cwd, ZERO, self.head(cwd), "1", **extra)

    def record(self, name: str) -> list[str]:
        path = self.records / name
        if not path.exists():
            return []
        return path.read_text(encoding="utf-8").splitlines()

    def log(self, worktree: Path) -> Path:
        gitdir = self.git("rev-parse", "--absolute-git-dir", cwd=worktree)
        return Path(gitdir.stdout.strip()) / "lane-setup.log"


@pytest.fixture
def lane(tmp_path: Path) -> Lane:
    root = tmp_path.resolve()
    main = root / "main"
    records = root / "records"
    stubbin = root / "stubbin"
    hooks = root / "shared-hooks"
    records.mkdir()
    _write_exec(stubbin / "make", MAKE_STUB)
    template = stubbin / "python3-template"
    _write_exec(template, PYTHON_STUB)
    hook = hooks / "post-checkout"
    _write_exec(hook, hook_text())

    _write_exec(main / "tools" / "pi" / "install.sh", INSTALL_STUB)
    _write_exec(main / "tools" / "pi" / "pi", PI_STUB)
    (main / "tools" / "pi" / "package.json").write_text(PACKAGE_JSON, "utf-8")
    _write_exec(main / "tools" / "beads" / "bin" / "bd", BD_STUB)
    (main / "README.md").write_text("lane\n", encoding="utf-8")

    env = {
        key: value
        for key, value in os.environ.items()
        if not key.startswith(("GIT_", "STUB_", "HARNESS_NO_LANE", "HARNESS_LANE"))
    }
    env.update(
        GIT_CONFIG_GLOBAL=os.devnull,
        GIT_CONFIG_NOSYSTEM="1",
        GIT_AUTHOR_NAME="Lane Test",
        GIT_AUTHOR_EMAIL="lane@example.invalid",
        GIT_COMMITTER_NAME="Lane Test",
        GIT_COMMITTER_EMAIL="lane@example.invalid",
        PATH=f"{stubbin}{os.pathsep}{os.environ.get('PATH', '')}",
        STUB_RECORD_DIR=str(records),
        STUB_PYTHON_TEMPLATE=str(template),
    )
    for args in (
        ["init", "-q", "-b", "main"],
        ["add", "-A"],
        ["commit", "-q", "-m", "init"],
        ["config", "core.hooksPath", str(hooks)],
        ["update-ref", "refs/remotes/origin/main", "HEAD"],
    ):
        proc = subprocess.run(["git", *args], cwd=main, env=env, capture_output=True, text=True)
        assert proc.returncode == 0, proc.stderr
    return Lane(main=main, hook=hook, records=records, env=env, root=root)


def _failures(stderr: str) -> list[str]:
    return [line for line in stderr.splitlines() if line.startswith("LANE SETUP FAILED:")]


def _starts(stderr: str) -> list[str]:
    return [line for line in stderr.splitlines() if line.startswith("lane setup: start")]


def _results(stderr: str) -> list[str]:
    return [
        line
        for line in stderr.splitlines()
        if line == "lane setup: ok" or (line.startswith("lane setup: failed (") and line.endswith(" checks)"))
    ]


def _assert_no_setup(lane: Lane, stderr: str) -> None:
    for name in SETUP_RECORDS:
        assert lane.record(name) == [], f"{name} ran: {lane.record(name)}"
    assert _starts(stderr) == []
    assert _results(stderr) == []
    assert _failures(stderr) == []


# Criterion 1
def test_new_worktree_runs_venv_in_worktree(lane: Lane) -> None:
    proc, worktree = lane.add_worktree()
    assert proc.returncode == 0, proc.stderr
    assert lane.record("make") == [f"{worktree}|venv"]
    assert (worktree / ".venv" / "bin" / "python3").exists()
    assert not (lane.main / ".venv").exists()


# Criterion 2
def test_new_worktree_runs_pi_install_in_worktree(lane: Lane) -> None:
    proc, worktree = lane.add_worktree()
    assert proc.returncode == 0, proc.stderr
    assert lane.record("install") == [f"{worktree}|{worktree / 'tools' / 'pi'}"]


# Criterion 3
@pytest.mark.parametrize("fault", ["STUB_YAML_FAIL", "STUB_MAKE_NO_VENV"])
def test_yaml_check_reports_failure(lane: Lane, fault: str) -> None:
    worktree = lane.quiet_worktree()
    clean = lane.new_worktree_hook(worktree)
    assert _failures(clean.stderr) == [], clean.stderr
    assert f"{worktree}|-c import yaml" in lane.record("python")

    if fault == "STUB_MAKE_NO_VENV":
        shutil.rmtree(worktree / ".venv")
    broken = lane.new_worktree_hook(worktree, **{fault: "1"})
    failures = _failures(broken.stderr)
    assert len(failures) == 1, broken.stderr
    assert "yaml" in failures[0]


# Criterion 4
@pytest.mark.parametrize("fault", ["mismatch", "fails", "missing", "prefixed"])
def test_pi_version_check_reports_failure(lane: Lane, fault: str) -> None:
    worktree = lane.quiet_worktree()
    clean = lane.new_worktree_hook(worktree)
    assert _failures(clean.stderr) == [], clean.stderr
    assert f"{worktree}|--version" in lane.record("pi")

    extra: dict[str, str] = {}
    if fault == "mismatch":
        extra["STUB_PI_VERSION"] = "1.2.4"
    elif fault == "prefixed":
        extra["STUB_PI_VERSION"] = f"v{PIN}"
    elif fault == "fails":
        extra["STUB_PI_FAIL"] = "1"
    else:
        (worktree / "tools" / "pi" / "pi").unlink()
    broken = lane.new_worktree_hook(worktree, **extra)
    failures = _failures(broken.stderr)
    assert len(failures) == 1, broken.stderr
    assert "pi version check" in failures[0]


# Criterion 5
@pytest.mark.parametrize(
    ("fault", "step"),
    [
        ("STUB_MAKE_FAIL", "make venv"),
        ("STUB_INSTALL_FAIL", "bash tools/pi/install.sh"),
        ("STUB_YAML_FAIL", "yaml import check"),
        ("STUB_PI_FAIL", "pi version check"),
    ],
)
def test_each_setup_failure_names_step(lane: Lane, fault: str, step: str) -> None:
    worktree = lane.quiet_worktree()
    proc = lane.new_worktree_hook(worktree, **{fault: "1"})
    failures = _failures(proc.stderr)
    assert len(failures) == 1, proc.stderr
    assert step in failures[0]
    assert str(lane.log(worktree)) in failures[0]


# Criterion 6
def test_setup_failure_does_not_fail_checkout(lane: Lane) -> None:
    every_fault = {
        "STUB_MAKE_FAIL": "1",
        "STUB_INSTALL_FAIL": "1",
        "STUB_YAML_FAIL": "1",
        "STUB_PI_FAIL": "1",
    }
    proc, worktree = lane.add_worktree(**every_fault)
    assert proc.returncode == 0, proc.stderr
    assert len(_failures(proc.stderr)) == 4, proc.stderr

    direct = lane.new_worktree_hook(worktree, **every_fault)
    assert direct.returncode == 0, direct.stderr
    assert len(_failures(direct.stderr)) == 4, direct.stderr


# Criterion 7
def test_opt_out_skips_setup(lane: Lane) -> None:
    proc, worktree = lane.add_worktree(HARNESS_NO_LANE_SETUP="1")
    assert proc.returncode == 0, proc.stderr
    _assert_no_setup(lane, proc.stderr)
    assert not lane.log(worktree).exists()
    assert len(lane.record("bd")) == 1


# Criterion 8
def test_other_checkouts_skip_setup(lane: Lane) -> None:
    branch = lane.git("checkout", "-q", "-b", "other")
    assert branch.returncode == 0, branch.stderr
    _assert_no_setup(lane, branch.stderr)

    (lane.main / "README.md").write_text("changed\n", encoding="utf-8")
    files = lane.git("checkout", "--", "README.md")
    assert files.returncode == 0, files.stderr
    _assert_no_setup(lane, files.stderr)

    head = lane.head(lane.main)
    direct = lane.run_hook(lane.main, ZERO, head, "0")
    _assert_no_setup(lane, direct.stderr)
    assert len(lane.record("bd")) == 3


# Criterion 9
@pytest.mark.parametrize(
    ("bd_exit", "setup_fault"),
    [("0", ""), ("5", ""), ("5", "STUB_YAML_FAIL"), ("0", "STUB_PI_FAIL")],
)
def test_beads_integration_is_preserved(lane: Lane, bd_exit: str, setup_fault: str) -> None:
    worktree = lane.quiet_worktree()
    head = lane.head(worktree)
    extra = {"STUB_BD_EXIT": bd_exit}
    if setup_fault:
        extra[setup_fault] = "1"
    proc = lane.run_hook(worktree, ZERO, head, "1", **extra)
    assert lane.record("bd") == [f"hooks run post-checkout {ZERO} {head} 1"]
    assert proc.returncode == int(bd_exit), proc.stderr
    assert len(_starts(proc.stderr)) == 1

    other = lane.run_hook(worktree, head, head, "0", **extra)
    assert lane.record("bd")[-1] == f"hooks run post-checkout {head} {head} 0"
    assert other.returncode == int(bd_exit), other.stderr


# Criterion 10
def test_setup_finishes_before_worktree_add_returns(lane: Lane) -> None:
    proc, worktree = lane.add_worktree(STUB_MAKE_SLEEP="1")
    assert proc.returncode == 0, proc.stderr
    assert lane.record("make-woke") == ["woke"]
    assert lane.record("pi") == [f"{worktree}|--version"]
    log = lane.log(worktree).read_text(encoding="utf-8")
    assert "lane setup: ok" in log or "lane setup: failed (" in log


# Criterion 11
def test_setup_timeout_stops_and_reports_step_and_limit(lane: Lane) -> None:
    started = time.monotonic()
    proc, worktree = lane.add_worktree(HARNESS_LANE_SETUP_TIMEOUT="1", STUB_MAKE_SLEEP="5")
    elapsed = time.monotonic() - started
    assert proc.returncode == 0, proc.stderr
    assert elapsed < 5, f"the overdue step ran on for {elapsed:.1f}s"
    failures = _failures(proc.stderr)
    assert len(failures) == 1, proc.stderr
    assert "make venv" in failures[0]
    assert re.search(r"\b1s\b", failures[0]), failures[0]
    assert str(lane.log(worktree)) in failures[0]
    for name in ("install", "python", "pi"):
        assert lane.record(name) == [], f"{name} ran after the limit"
    assert len(_results(proc.stderr)) == 1

    time.sleep(max(0.0, 6.5 - (time.monotonic() - started)))
    assert lane.record("make-woke") == [], "the overdue step was not stopped"


# Criterion 12
def test_setup_precedes_failing_beads(lane: Lane) -> None:
    _proc, worktree = lane.add_worktree(STUB_BD_EXIT="1")
    assert lane.record("bd"), "the Beads integration did not run"
    assert lane.record("make") == [f"{worktree}|venv"]
    assert lane.record("pi") == [f"{worktree}|--version"]


# Criterion 13
def test_setup_output_uses_worktree_git_log(lane: Lane) -> None:
    proc, worktree = lane.add_worktree()
    assert proc.returncode == 0, proc.stderr
    log = lane.log(worktree)
    assert log.parent != lane.main / ".git"
    text = log.read_text(encoding="utf-8")
    markers = (
        "STUB-MAKE-STDOUT",
        "STUB-MAKE-STDERR",
        "STUB-INSTALL-OUTPUT",
        "STUB-PYTHON-OUTPUT",
        PIN,
    )
    for marker in markers:
        assert marker in text, marker
        assert marker not in proc.stdout, marker
        assert marker not in proc.stderr, marker
    assert not (lane.main / ".git" / "lane-setup.log").exists()
    assert not (worktree / "lane-setup.log").exists()


# Criterion 14
@pytest.mark.parametrize("fault", ["", "STUB_INSTALL_FAIL"])
def test_setup_emits_start_and_result(lane: Lane, fault: str) -> None:
    extra = {fault: "1"} if fault else {}
    proc, _worktree = lane.add_worktree(**extra)
    assert proc.returncode == 0, proc.stderr
    assert len(_starts(proc.stderr)) == 1, proc.stderr
    assert len(_results(proc.stderr)) == 1, proc.stderr
    lines = proc.stderr.splitlines()
    assert lines.index(_starts(proc.stderr)[0]) < lines.index(_results(proc.stderr)[0])


# Criterion 15
@pytest.mark.parametrize("value", [None, "", "0", "true", "11", " 1"])
def test_only_one_opts_out(lane: Lane, value: str | None) -> None:
    extra = {} if value is None else {"HARNESS_NO_LANE_SETUP": value}
    proc, worktree = lane.add_worktree(**extra)
    assert proc.returncode == 0, proc.stderr
    assert lane.record("make") == [f"{worktree}|venv"]
    assert lane.record("pi") == [f"{worktree}|--version"]
    assert len(_starts(proc.stderr)) == 1, proc.stderr


# ---------------------------------------------------------------------------
# Review-loop round 2 (hand finish by the orchestrator, 2026-11-25)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("value", ["0", "-5", "abc"])
def test_invalid_limit_falls_back_with_one_warning(lane: Lane, value: str) -> None:
    """L2-1 (decisions S-8): an invalid limit falls back to 600 and says so once."""
    proc, _ = lane.add_worktree(HARNESS_LANE_SETUP_TIMEOUT=value)
    warnings = [line for line in proc.stderr.splitlines() if line.startswith("lane setup: warning:")]
    assert len(warnings) == 1, proc.stderr
    assert f"HARNESS_LANE_SETUP_TIMEOUT={value}" in warnings[0] and "using 600" in warnings[0], proc.stderr


def test_summary_uses_the_decided_forms(lane: Lane) -> None:
    """L2-10 (decisions S-7): 'lane setup: ok' / 'lane setup: failed (N checks)', then the log path."""
    ok, _ = lane.add_worktree("good")
    lines = ok.stderr.splitlines()
    assert "lane setup: ok" in lines, ok.stderr
    assert lines[lines.index("lane setup: ok") + 1].startswith("lane setup: log: "), ok.stderr
    bad, _ = lane.add_worktree("bad", STUB_INSTALL_FAIL="1", STUB_YAML_FAIL="1")
    assert "lane setup: failed (2 checks)" in bad.stderr.splitlines(), bad.stderr


def test_every_failure_line_names_the_retry_command(lane: Lane) -> None:
    """L2-15: a failed setup names the deliberate rerun, and the rerun works."""
    proc, path = lane.add_worktree(STUB_INSTALL_FAIL="1")
    failures = _failures(proc.stderr)
    assert failures and all("retry: bash .beads/hooks/post-checkout --lane-setup" in f for f in failures), proc.stderr
    rerun = lane.run_hook(path, "--lane-setup")
    assert rerun.returncode == 0, rerun.stderr
    assert "lane setup: ok" in rerun.stderr.splitlines(), rerun.stderr
    assert len(lane.record("install")) == 2


def test_untrusted_state_is_skipped_and_can_be_set_up_deliberately(lane: Lane) -> None:
    """L2-5 (maintainer, security): a state off origin/main that changes the setup inputs is not run."""
    assert lane.git("checkout", "-q", "-b", "foreign").returncode == 0
    (lane.main / "Makefile").write_text("venv:\n\t@echo foreign\n", encoding="utf-8")
    assert lane.git("add", "Makefile").returncode == 0
    assert lane.git("commit", "-q", "-m", "foreign makefile").returncode == 0
    assert lane.git("checkout", "-q", "main").returncode == 0
    path = lane.root / "foreign-lane"
    proc = lane.git("worktree", "add", "-q", str(path), "foreign")
    assert proc.returncode == 0, proc.stderr
    assert any(line.startswith("lane setup: skipped:") for line in proc.stderr.splitlines()), proc.stderr
    assert lane.record("make") == [], "an untrusted Makefile ran"
    rerun = lane.run_hook(path, "--lane-setup")
    assert lane.record("make"), rerun.stderr


def test_a_trusted_branch_with_unchanged_inputs_is_set_up(lane: Lane) -> None:
    """L2-5: a new branch whose setup inputs equal origin/main's is trusted."""
    proc, _ = lane.add_worktree("own")
    assert not any(line.startswith("lane setup: skipped:") for line in proc.stderr.splitlines()), proc.stderr
    assert lane.record("make"), proc.stderr


def test_without_perl_the_unenforced_limit_is_named(lane: Lane, tmp_path: Path) -> None:
    """L2-11: without perl the hook says the per-step limit is not enforced."""
    nopl = tmp_path / "noperl-bin"
    nopl.mkdir()
    for folder in os.environ.get("PATH", "").split(os.pathsep):
        if not folder or not Path(folder).is_dir():
            continue
        for entry in Path(folder).iterdir():
            target = nopl / entry.name
            if entry.name.startswith("perl") or target.exists():
                continue
            try:
                target.symlink_to(entry)
            except OSError:
                continue
    path_env = os.pathsep.join([lane.env["PATH"].split(os.pathsep)[0], str(nopl)])
    proc, _ = lane.add_worktree(PATH=path_env)
    assert any("perl not found" in line and "shell watchdog" in line for line in proc.stderr.splitlines()), proc.stderr


def test_a_step_never_started_names_the_step_that_used_the_budget(lane: Lane) -> None:
    """L2-20: when the limit is spent, the next step is reported as not started, naming the previous one."""
    proc, _ = lane.add_worktree(HARNESS_LANE_SETUP_TIMEOUT="1", STUB_MAKE_SLEEP="3")
    text = proc.stderr
    assert "not started" in text and "used up by make venv" in text or "make venv timed out" in text, text


def test_without_perl_a_hanging_step_still_stops(lane: Lane, tmp_path: Path) -> None:
    """Phase-6 P6-2: without perl the limit still ends an overdue step and reports it."""
    nopl = tmp_path / "noperl-bin2"
    nopl.mkdir()
    for folder in os.environ.get("PATH", "").split(os.pathsep):
        if not folder or not Path(folder).is_dir():
            continue
        for entry in Path(folder).iterdir():
            target = nopl / entry.name
            if entry.name.startswith("perl") or target.exists():
                continue
            try:
                target.symlink_to(entry)
            except OSError:
                continue
    path_env = os.pathsep.join([lane.env["PATH"].split(os.pathsep)[0], str(nopl)])
    started = time.monotonic()
    proc, _ = lane.add_worktree(PATH=path_env, HARNESS_LANE_SETUP_TIMEOUT="2", STUB_MAKE_SLEEP="30")
    assert time.monotonic() - started < 20, "the hanging step was not stopped"
    assert any("make venv timed out" in line for line in _failures(proc.stderr)), proc.stderr


def test_an_unwritable_log_is_reported(lane: Lane) -> None:
    """Phase-6 P6-3: an unwritable log is named on stderr and in the summary."""
    path = lane.quiet_worktree("ro")
    gitdir = Path(lane.git("rev-parse", "--absolute-git-dir", cwd=path).stdout.strip())
    log = gitdir / "lane-setup.log"
    log.mkdir()  # a directory where the log file would go cannot be truncated
    proc = lane.new_worktree_hook(path)
    assert any("cannot be written" in line for line in proc.stderr.splitlines()), proc.stderr
    assert "lane setup: log: unavailable" in proc.stderr.splitlines(), proc.stderr


def test_without_perl_the_watchdog_ends_the_steps_children(lane: Lane, tmp_path: Path) -> None:
    """Phase-6 P6-5: without perl an overdue step's child process is ended with it."""
    nopl = tmp_path / "noperl-bin3"
    nopl.mkdir()
    for folder in os.environ.get("PATH", "").split(os.pathsep):
        if not folder or not Path(folder).is_dir():
            continue
        for entry in Path(folder).iterdir():
            target = nopl / entry.name
            if entry.name.startswith("perl") or target.exists():
                continue
            try:
                target.symlink_to(entry)
            except OSError:
                continue
    path_env = os.pathsep.join([lane.env["PATH"].split(os.pathsep)[0], str(nopl)])
    proc, _ = lane.add_worktree(
        PATH=path_env, HARNESS_LANE_SETUP_TIMEOUT="2", STUB_MAKE_SLEEP="30", STUB_MAKE_CHILD="40"
    )
    assert any("make venv timed out" in line for line in _failures(proc.stderr)), proc.stderr
    child = int((lane.records / "make-child").read_text().strip())
    time.sleep(1)
    alive = subprocess.run(["kill", "-0", str(child)], capture_output=True).returncode == 0
    if alive:
        subprocess.run(["kill", "-KILL", str(child)], capture_output=True)
    assert not alive, "the step's child outlived the watchdog"
