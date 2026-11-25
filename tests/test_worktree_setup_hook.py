"""The checkout hook sets up a new worktree (bead coding-harness-wg4z).

Every test builds a throwaway repository whose `make`, `tools/pi/install.sh`,
`tools/pi/pi`, `.venv/bin/python3` and `bd` are stubs that record where and how
they ran, so nothing is downloaded. The hook sits in a shared directory named
by an absolute `core.hooksPath`, the layout a real main checkout uses: a new
worktree invokes that one copy, and the hook must still work in the worktree.

The hook under test is the versioned `.beads/hooks/post-checkout`. Until the
lane-setup block is applied to it, the tests insert `SETUP_BLOCK` (the
reference block) above its Beads-managed section; once the versioned hook
carries the block itself, the tests run it unchanged.
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
BEADS_BEGIN = "# --- BEGIN BEADS INTEGRATION"
ZERO = "0" * 40
PIN = "1.2.3"

SETUP_BLOCK = r"""# --- BEGIN LANE SETUP (bead coding-harness-wg4z) ---
# A new worktree (all-zero previous object, branch-checkout flag 1) gets its
# own .venv and pinned Pi here, in the foreground and above the Beads-managed
# block, so a Beads failure cannot skip it. HARNESS_NO_LANE_SETUP=1 opts out;
# HARNESS_LANE_SETUP_TIMEOUT bounds the whole setup (default 600 seconds).
# Step output goes to lane-setup.log in the worktree's Git directory; stderr
# shows one start line, one result line and a LANE SETUP FAILED line per
# failure. A setup failure never changes the hook's exit status.
_ls_perl='my $t = shift @ARGV; my $pid = fork; defined $pid or die "lane setup: fork failed: $!\n"; if ($pid == 0) { setpgrp(0, 0); exec { $ARGV[0] } @ARGV or do { print STDERR "lane setup: cannot run $ARGV[0]: $!\n"; exit 127 }; } setpgrp($pid, $pid); $SIG{ALRM} = sub { kill "TERM", -$pid; sleep 1; kill "KILL", -$pid; waitpid($pid, 0); print STDERR "lane setup: stopped after ${t}s\n"; exit 124 }; alarm $t; waitpid($pid, 0); my $rc = $?; alarm 0; exit($rc & 127 ? 128 + ($rc & 127) : $rc >> 8);'
_ls_say() {
  printf '%s\n' "$1" >&2
  printf '%s\n' "$1" >>"$_ls_log" 2>/dev/null
}
_ls_timeout() {
  _ls_stopped=1
  _ls_failed=$((_ls_failed + 1))
  _ls_say "LANE SETUP FAILED: $1 timed out at the ${_ls_limit}s setup limit (HARNESS_LANE_SETUP_TIMEOUT); log: $_ls_log"
}
_ls_step() {
  _ls_label=$1
  shift
  [ -z "$_ls_stopped" ] || return 0
  _ls_left=$((_ls_deadline - $(date +%s)))
  if [ "$_ls_left" -le 0 ]; then
    _ls_timeout "$_ls_label"
    return 0
  fi
  printf '== %s\n' "$_ls_label" >>"$_ls_log"
  if command -v perl >/dev/null 2>&1; then
    perl -e "$_ls_perl" "$_ls_left" "$@" >>"$_ls_log" 2>&1 </dev/null
  else
    printf '%s\n' "lane setup: perl not found; $_ls_label runs without the setup limit" >>"$_ls_log"
    "$@" >>"$_ls_log" 2>&1 </dev/null
  fi
  _ls_rc=$?
  if [ "$_ls_rc" -eq 124 ] && [ "$(date +%s)" -ge "$_ls_deadline" ]; then
    _ls_timeout "$_ls_label"
  elif [ "$_ls_rc" -ne 0 ]; then
    _ls_failed=$((_ls_failed + 1))
    _ls_say "LANE SETUP FAILED: $_ls_label (exit $_ls_rc); log: $_ls_log"
  fi
}
_lane_setup() {
  _ls_root=$(git rev-parse --show-toplevel 2>/dev/null) || _ls_root=
  _ls_gitdir=$(git rev-parse --absolute-git-dir 2>/dev/null) || _ls_gitdir=
  if [ -z "$_ls_root" ] || [ -z "$_ls_gitdir" ]; then
    printf '%s\n' "LANE SETUP FAILED: locate the new worktree; log: none" >&2
    return 0
  fi
  _ls_log="$_ls_gitdir/lane-setup.log"
  : >"$_ls_log" 2>/dev/null || _ls_log=/dev/null
  _ls_limit=$(printf '%s' "${HARNESS_LANE_SETUP_TIMEOUT-}" | sed 's/^0*//')
  case "$_ls_limit" in ''|*[!0-9]*) _ls_limit=600 ;; esac
  _ls_deadline=$(($(date +%s) + _ls_limit))
  _ls_failed=0
  _ls_stopped=
  cd "$_ls_root" || return 0
  _ls_say "lane setup: start: $_ls_root (limit ${_ls_limit}s); log: $_ls_log"
  _ls_step "make venv" make venv
  _ls_step "bash tools/pi/install.sh" bash tools/pi/install.sh
  _ls_step "yaml import check" .venv/bin/python3 -c 'import yaml'
  _ls_pin=$(sed -n 's/^[[:space:]]*"@earendil-works\/pi-coding-agent":[[:space:]]*"\([^"]*\)".*/\1/p' tools/pi/package.json 2>/dev/null | head -n 1)
  _ls_step "pi version check" sh -c 'want=$1; [ -n "$want" ] || { echo "tools/pi/package.json declares no pin"; exit 1; }; [ -f tools/pi/pi ] || { echo "tools/pi/pi is missing"; exit 1; }; got=$(tools/pi/pi --version) || { echo "tools/pi/pi --version failed"; exit 1; }; echo "tools/pi/pi --version printed $got; pinned $want"; [ "$got" = "$want" ]' lane-setup-pi "$_ls_pin"
  if [ -n "$_ls_stopped" ]; then
    _ls_say "lane setup: result: stopped at the ${_ls_limit}s limit, $_ls_failed failed; log: $_ls_log"
  elif [ "$_ls_failed" -eq 0 ]; then
    _ls_say "lane setup: result: ok; log: $_ls_log"
  else
    _ls_say "lane setup: result: $_ls_failed step(s) failed; log: $_ls_log"
  fi
}
case "$1" in
  *[!0]*|'') ;;
  *)
    if [ "$3" = 1 ] && [ "${HARNESS_NO_LANE_SETUP-}" != 1 ]; then
      (_lane_setup)
    fi
    ;;
esac
# --- END LANE SETUP ---
"""

MAKE_STUB = r"""#!/bin/sh
if [ "$1" = "-C" ]; then cd "$2" || exit 1; shift 2; fi
printf '%s|%s\n' "$(pwd -P)" "$*" >>"$STUB_RECORD_DIR/make"
echo "STUB-MAKE-STDOUT"
echo "STUB-MAKE-STDERR" >&2
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
    """The versioned hook, with the reference block until it carries one."""
    text = VERSIONED_HOOK.read_text(encoding="utf-8")
    if "HARNESS_NO_LANE_SETUP" in text:
        return text
    assert BEADS_BEGIN in text, "the versioned hook lost its Beads-managed block"
    return text.replace(BEADS_BEGIN, SETUP_BLOCK + BEADS_BEGIN, 1)


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
    ):
        proc = subprocess.run(["git", *args], cwd=main, env=env, capture_output=True, text=True)
        assert proc.returncode == 0, proc.stderr
    return Lane(main=main, hook=hook, records=records, env=env, root=root)


def _failures(stderr: str) -> list[str]:
    return [line for line in stderr.splitlines() if line.startswith("LANE SETUP FAILED:")]


def _starts(stderr: str) -> list[str]:
    return [line for line in stderr.splitlines() if line.startswith("lane setup: start")]


def _results(stderr: str) -> list[str]:
    return [line for line in stderr.splitlines() if line.startswith("lane setup: result")]


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
    assert "lane setup: result" in log


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
