"""The machine-facts block of the night-run start - and the cases in which its readings hold.

`scripts/machine_facts.py` prints one dated, read-only snapshot: free disk on
the invoking worktree's filesystem, host-wide swap, the repository's registered
non-bare worktrees, and the runner and verification invocations the existing
run report recognizes (plans/changes/night-machine-facts/spec.md). Every
fixture injects its sources - clock, statvfs, system commands, the Linux proc
path - and never probes the real machine's pressure, so the tests are
deterministic on macOS and Linux. Each test names the fault that turns it red;
the fault is the ledger's em-dash text of its criterion. Timeout cases
exercise the shared bounded command reader through the snapshot collector.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import machine_facts  # noqa: E402
import run_report  # noqa: E402

GIB = 1024**3
FRSIZE = 4096
T0 = datetime(2026, 11, 6, 21, 0, 0)
T1 = datetime(2026, 11, 6, 21, 5, 0)
STAMP_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")

SWAPUSAGE = "total = 4096.00M used = 512.00M free = 3584.00M (M = megs)\n"
# 0.5 GiB used of 2.0 GiB total: `used` and `free` must not be confused (free holds 1.5 GiB).
MEMINFO = "MemTotal:  16384000 kB\nSwapTotal:   2097152 kB\nSwapFree:    1572864 kB\n"
MEMINFO_ZERO = "MemTotal:  16384000 kB\nSwapTotal:         0 kB\nSwapFree:          0 kB\n"
MEMINFO_WRONG = "MemTotal:  16384000 kB\nSwapTotal:   1048576 kB\nSwapFree:    2097152 kB\n"

MAIN = "worktree /repo/main\nHEAD abc123\nbranch refs/heads/main\n"
LINKED = "worktree /repo/linked wt\nHEAD def456\nbranch refs/heads/feature\n"
STALE = "worktree /repo/stale\nHEAD 0000000\nprunable git status file missing\n"
BARE = "worktree /repo/bare\nbare\n"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def clock(start: datetime, step_seconds: int = 300):
    """An injected clock: each reading moves the stamp forward, so successive snapshots differ."""
    current = start

    def now() -> datetime:
        nonlocal current
        value = current
        current += timedelta(seconds=step_seconds)
        return value

    return now


def statvfs_result(available_bytes: int, total_bytes: int = 0) -> os.statvfs_result:
    """One statvfs reading; `f_bavail` carries the user-available bytes, `f_bfree` the raw total."""
    blocks_total = total_bytes // FRSIZE
    return os.statvfs_result((FRSIZE, FRSIZE, blocks_total, blocks_total, available_bytes // FRSIZE, 0, 0, 0, 0, 0))


def fake_statvfs(table: dict[Path, os.statvfs_result]):
    """An injected statvfs: it records every path it is asked about and answers only what was declared."""
    asked: list[Path] = []

    def statvfs(path: str | os.PathLike[str]) -> os.statvfs_result:
        asked.append(Path(path))
        return table[Path(path)]

    statvfs.asked = asked  # type: ignore[attr-defined]
    return statvfs


def fake_run(outputs: dict[tuple[str, ...], str] | None = None, fail: set[tuple[str, ...]] | None = None):
    """An injected run_command: it records every argv and answers only what was declared."""
    calls: list[list[str]] = []

    def run(argv: list[str]) -> str:
        calls.append(list(argv))
        key = tuple(argv)
        if fail and key in fail:
            raise run_report.SourceError(f"not read ({argv[0]}: injected failure)")
        if outputs and key in outputs:
            return outputs[key]
        return ""

    run.calls = calls  # type: ignore[attr-defined]
    return run


def git_keys(worktree: Path) -> dict[tuple[str, ...], str]:
    """The read-only git answer of one worktree: the top level of the invoking directory."""
    return {("git", "-C", str(worktree), "rev-parse", "--show-toplevel"): f"{worktree}\n"}


def worktree_list_fixture(*entries: str) -> str:
    """One `-z` porcelain table: NUL-terminated attributes and empty record separators."""
    return "".join(entry.rstrip("\n").replace("\n", "\0") + "\0\0" for entry in entries)


def ps_output(*lines: str) -> str:
    return "\n".join(["  PID   TIME COMMAND", *lines]) + "\n"


def proc_fixture(tmp_path: Path, meminfo: str = MEMINFO) -> Path:
    """An injected /proc directory, so the swap figures never depend on the test machine."""
    proc = tmp_path / "proc"
    proc.mkdir(exist_ok=True)
    (proc / "meminfo").write_text(meminfo, encoding="utf-8")
    return proc


def snapshot(run, statvfs, *, cwd: Path, proc_dir: Path) -> machine_facts.MachineSnapshot:
    """One collector call with the shared fixture clock and proc path."""
    return machine_facts.collect_snapshot(run=run, statvfs=statvfs, now=clock(T0), proc_dir=proc_dir, cwd=cwd)


PS_TABLE = ps_output(
    "12345 03:12 python3 scripts/stage2.py implement night-machine-facts --route flash",
    "12346 00:05 /bin/zsh -c python3 scripts/stage2.py implement night-machine-facts",
    "12347 12:00 make verify",
    "12348 1-02:00:00 /Applications/Editor.app/Contents/MacOS/editor plans/changes/night-machine-facts/plan.md",
    '12349 00:01 echo "python3 scripts/stage2.py implement night-machine-facts"',
)


# ---------------------------------------------------------------------------
# The seven criteria
# ---------------------------------------------------------------------------


def test_cli_prints_fresh_dated_machine_block(tmp_path: Path, capsys) -> None:
    """Fault: a field or the UTC stamp is absent, or successive changed sources reuse stale
    values instead of collecting one fresh snapshot per invocation (spec criterion 1)."""
    worktree = tmp_path / "repo"
    (worktree / "plans" / "changes" / "night-machine-facts").mkdir(parents=True)
    proc = proc_fixture(tmp_path)
    table = {worktree: statvfs_result(5 * GIB)}
    outputs = {
        **git_keys(worktree),
        ("git", "-C", str(worktree), "worktree", "list", "--porcelain", "-z"): worktree_list_fixture(MAIN),
        ("ps", "-axo", "pid,etime,command"): ps_output(),
    }
    run = fake_run(outputs)
    code = machine_facts.main([], run=run, statvfs=fake_statvfs(table), now=clock(T0), proc_dir=proc, cwd=worktree)
    first = capsys.readouterr().out
    assert code == 0
    stamp = STAMP_RE.search(first)
    assert stamp is not None and stamp.group(0) == "2026-11-06T21:00:00Z"
    for label in ("free disk:", "swap:", "registered worktrees:", "running jobs:"):
        assert label in first, f"the field {label} is missing"
    assert "5.0 GiB available" in first
    assert "0.5 GiB used of 2.0 GiB total" in first
    assert "registered worktrees: 1 (git worktree list" in first
    assert "none matched" in first

    # A second invocation with changed sources must collect again, never replay the first block.
    (proc / "meminfo").write_text(MEMINFO_ZERO, encoding="utf-8")
    table[worktree] = statvfs_result(6 * GIB)
    outputs[("git", "-C", str(worktree), "worktree", "list", "--porcelain", "-z")] = worktree_list_fixture(
        MAIN, LINKED, BARE
    )
    code = machine_facts.main([], run=run, statvfs=fake_statvfs(table), now=clock(T1), proc_dir=proc, cwd=worktree)
    second = capsys.readouterr().out
    assert code == 0
    stamp2 = STAMP_RE.search(second)
    assert stamp2 is not None and stamp2.group(0) == "2026-11-06T21:05:00Z"
    assert "6.0 GiB available" in second and "5.0 GiB available" not in second
    assert "0.0 GiB used of 0.0 GiB total" in second and "0.5 GiB used" not in second
    assert "registered worktrees: 2 (git worktree list" in second


def test_disk_reports_worktree_available_space(tmp_path: Path) -> None:
    """Fault: the home volume's space is reported, used bytes count as free, or the unit or the
    filesystem scope is missing (spec criterion 2)."""
    worktree = tmp_path / "repo"
    home = tmp_path / "home"
    worktree.mkdir()
    home.mkdir()
    # The worktree volume offers 5 GiB of its 40; the home volume lies in wait with 40 free.
    table = {worktree: statvfs_result(5 * GIB, 40 * GIB), home: statvfs_result(40 * GIB, 40 * GIB)}
    statvfs = fake_statvfs(table)
    run = fake_run(git_keys(worktree))
    out = machine_facts.render(snapshot(run, statvfs, cwd=worktree, proc_dir=proc_fixture(tmp_path)))
    disk_line = next(line for line in out.splitlines() if line.startswith("free disk:"))
    assert "5.0 GiB available" in disk_line
    assert "40.0 GiB" not in disk_line  # neither the home volume's figure nor the raw total
    assert "GiB" in disk_line and "filesystem" in disk_line and "worktree" in disk_line  # unit and scope
    assert str(tmp_path) not in out  # the scope is named, no absolute path is printed
    assert statvfs.asked == [worktree]  # the home volume was never probed


def test_swap_reports_used_and_total_on_both_platforms(tmp_path: Path) -> None:
    """Fault: used and total are confused, a macOS meg value or a Linux kB value is misconverted,
    or a valid zero-total reading is labelled unreadable (spec criterion 3)."""
    # macOS: 512 MiB used of 4096 MiB total, exactly 0.5 and 4.0 GiB.
    run = fake_run({("sysctl", "-n", "vm.swapusage"): SWAPUSAGE})
    assert machine_facts.swap_field(run, None) == "0.5 GiB used of 4.0 GiB total (host-wide)"
    # Linux: SwapTotal 2097152 kB, SwapFree 1572864 kB - 0.5 GiB used of 2.0 GiB total.
    proc = proc_fixture(tmp_path)
    assert machine_facts.swap_field(run, proc) == "0.5 GiB used of 2.0 GiB total (host-wide)"
    # A configured-but-empty swap is a readable zero, not a failure.
    (proc / "meminfo").write_text(MEMINFO_ZERO, encoding="utf-8")
    assert machine_facts.swap_field(run, proc) == "0.0 GiB used of 0.0 GiB total (host-wide)"
    # macOS readings that cannot hold are refused: negative, non-finite, and not the meg format.
    for answer in (
        "total = 4096.00M used = -5.00M free = 4101.00M (M = megs)\n",
        "total = nan M used = 0.00M free = nan M (M = megs)\n",
        "total = 4.0G used = 1.0G\n",
    ):
        run = fake_run({("sysctl", "-n", "vm.swapusage"): answer})
        assert "not read" in machine_facts.swap_field(run, None), answer
    # Linux refuses an inconsistent table (free above total) and a missing swap section.
    run = fake_run({})
    (proc / "meminfo").write_text(MEMINFO_WRONG, encoding="utf-8")
    assert "not read" in machine_facts.swap_field(run, proc)
    (proc / "meminfo").write_text("MemTotal:  16384000 kB\n", encoding="utf-8")
    assert "not read" in machine_facts.swap_field(run, proc)


def test_worktrees_count_registered_non_bare_entries(tmp_path: Path) -> None:
    """Fault: the main checkout, a linked or stale registration, a bare entry or a path with
    whitespace yields the wrong count, or an unrelated filesystem directory is counted
    (spec criterion 4)."""
    worktree = tmp_path / "repo"
    (worktree / "unrelated").mkdir(parents=True)  # a real directory git has never registered
    outputs = {
        **git_keys(worktree),
        ("git", "-C", str(worktree), "worktree", "list", "--porcelain", "-z"): worktree_list_fixture(
            MAIN, LINKED, STALE, BARE
        ),
    }
    run = fake_run(outputs)
    out = machine_facts.render(
        snapshot(run, fake_statvfs({worktree: statvfs_result(GIB)}), cwd=worktree, proc_dir=proc_fixture(tmp_path))
    )
    line = next(line for line in out.splitlines() if line.startswith("registered worktrees:"))
    assert line == "registered worktrees: 3 (git worktree list; non-bare entries, stale registrations included)"
    assert "/repo/bare" not in out and "linked wt" not in out  # paths never print; entries are counted only
    assert "unrelated" not in out  # the count comes from git's table, never the directory listing


def test_jobs_use_existing_process_recognition(tmp_path: Path, monkeypatch) -> None:
    """Fault: a real invocation is lost, a shell wrapper or a quoted command is counted as a job,
    change attribution is guessed for an unknown change, runner recognition claims `none` when
    its definitions are gone, or raw command arguments leak into the block (spec criterion 5)."""
    worktree = tmp_path / "repo"
    (worktree / "plans" / "changes" / "night-machine-facts").mkdir(parents=True)
    proc = proc_fixture(tmp_path)

    def block(run, root: Path) -> str:
        return machine_facts.render(snapshot(run, fake_statvfs({root: statvfs_result(GIB)}), cwd=root, proc_dir=proc))

    outputs = {
        **git_keys(worktree),
        ("git", "-C", str(worktree), "worktree", "list", "--porcelain", "-z"): worktree_list_fixture(MAIN),
        ("ps", "-axo", "pid,etime,command"): PS_TABLE,
    }
    out = block(fake_run(outputs), worktree)
    job_lines = [line for line in out.splitlines() if line.lstrip().startswith("pid ")]
    assert len(job_lines) == 2  # the implement invocation and `make verify`; wrapper, editor and echo are not jobs
    assert "pid 12345 · implement · change night-machine-facts · elapsed 03:12" in out
    assert "pid 12347 · verify · change not read · elapsed 12:00" in out
    assert "--route" not in out and "flash" not in out  # raw arguments never print
    assert "zsh" not in out and "echo" not in out and "Editor" not in out  # non-jobs never print

    # An unknown change is never guessed into a name.
    outputs = {
        **git_keys(worktree),
        ("ps", "-axo", "pid,etime,command"): ps_output("12350 05:00 python3 scripts/stage2.py implement not-a-change"),
    }
    assert "pid 12350 · implement · change not read · elapsed 05:00" in block(fake_run(outputs), worktree)

    # The shared change list is unreadable: the readable row survives, attribution says `not read`.
    broken = tmp_path / "broken"
    (broken / "plans").mkdir(parents=True)
    (broken / "plans" / "changes").write_text("not a directory\n", encoding="utf-8")
    outputs = {
        **git_keys(broken),
        ("ps", "-axo", "pid,etime,command"): ps_output(
            "12345 03:12 python3 scripts/stage2.py implement night-machine-facts"
        ),
    }
    assert "pid 12345 · implement · change not read · elapsed 03:12" in block(fake_run(outputs), broken)

    # The runner definitions are unavailable: recognition says so instead of claiming no runners.
    monkeypatch.setattr(run_report, "stage2", None)
    monkeypatch.setattr(run_report, "KNOWN_VERBS", frozenset())
    outputs = {**git_keys(worktree), ("ps", "-axo", "pid,etime,command"): PS_TABLE}
    out = block(fake_run(outputs), worktree)
    assert "runner recognition: not read (runner verb definitions unavailable)" in out
    assert "pid 12347 · verify · change not read · elapsed 12:00" in out  # verification still renders
    assert "· implement ·" not in out  # no runner row - and the note above says why, so this is no silent `none`


def test_sources_fail_independently_without_becoming_a_gate(tmp_path: Path, capsys) -> None:
    """Fault: a failed or malformed source becomes zero or `none`, suppresses an independent field,
    leaks raw diagnostics, or turns a valid invocation into a failing admission check (criterion 6).
    Timeout coordination is also exercised in test_sources_timeout_independently."""
    worktree = tmp_path / "repo"
    (worktree / "plans" / "changes").mkdir(parents=True)
    proc = proc_fixture(tmp_path)
    git_outputs = {
        **git_keys(worktree),
        ("git", "-C", str(worktree), "worktree", "list", "--porcelain", "-z"): worktree_list_fixture(MAIN, LINKED),
    }
    statvfs = fake_statvfs({worktree: statvfs_result(2 * GIB)})

    # The swap file is unreadable and `ps` fails: the readable fields remain, and the exit stays zero.
    (proc / "meminfo").write_bytes(b"\xff\xfe no swap here\n")
    run = fake_run(git_outputs, fail={("ps", "-axo", "pid,etime,command")})
    code = machine_facts.main([], run=run, statvfs=statvfs, proc_dir=proc, cwd=worktree, now=clock(T0))
    out = capsys.readouterr().out
    assert code == 0
    assert "free disk: 2.0 GiB available" in out  # the independently readable fields remain
    assert "registered worktrees: 2 (git worktree list" in out
    assert "swap: not read (meminfo: SwapTotal/SwapFree unreadable)" in out
    assert "running jobs:\n  not read (ps: injected failure)" in out
    assert "0.0 GiB used" not in out and "none matched" not in out  # no safe zero, no false `none`
    assert "Traceback" not in out and "no swap here" not in out  # raw diagnostics never echo

    # Git cannot identify the worktree: only its field is lost; disk, swap and processes stay.
    (proc / "meminfo").write_text(MEMINFO, encoding="utf-8")
    revparse = ("git", "-C", str(worktree), "rev-parse", "--show-toplevel")
    run = fake_run(
        {
            ("git", "-C", str(worktree), "worktree", "list", "--porcelain", "-z"): worktree_list_fixture(MAIN),
            ("ps", "-axo", "pid,etime,command"): ps_output(
                "12345 03:12 python3 scripts/stage2.py implement night-machine-facts"
            ),
        },
        fail={revparse},
    )
    code = machine_facts.main([], run=run, statvfs=statvfs, proc_dir=proc, cwd=worktree, now=clock(T0))
    out = capsys.readouterr().out
    assert code == 0
    assert "free disk: 2.0 GiB available" in out
    assert "registered worktrees: not read (worktree: not identified)" in out
    assert "swap: 0.5 GiB used of 2.0 GiB total (host-wide)" in out
    assert "pid 12345 · implement · change not read · elapsed 03:12" in out

    # A malformed swap table and a failing disk reader are bounded, each on its own field.
    (proc / "meminfo").write_text("MemTotal: 1 kB\n", encoding="utf-8")

    def denied(_path: str | os.PathLike[str]) -> os.statvfs_result:
        raise OSError(13, "Permission denied")

    run = fake_run(git_outputs)
    code = machine_facts.main([], run=run, statvfs=denied, proc_dir=proc, cwd=worktree, now=clock(T0))
    out = capsys.readouterr().out
    assert code == 0
    assert "free disk: not read (statvfs: unavailable)" in out
    assert "Permission denied" not in out  # the bounded reason, never the diagnostic
    assert "swap: not read (meminfo:" in out
    assert "registered worktrees: 2 (git worktree list" in out


def test_snapshot_is_local_and_read_only(tmp_path: Path) -> None:
    """Fault: the snapshot writes a file (bytecode included), runs a mutation, network or tracker
    command beyond its read-only sources, or leaves state behind (spec criterion 7)."""

    worktree = tmp_path / "repo"
    (worktree / "plans" / "changes").mkdir(parents=True)
    outputs = {
        **git_keys(worktree),
        ("git", "-C", str(worktree), "worktree", "list", "--porcelain", "-z"): worktree_list_fixture(MAIN, BARE),
        ("ps", "-axo", "pid,etime,command"): PS_TABLE,
    }
    run = fake_run(outputs)
    machine_facts.render(
        snapshot(run, fake_statvfs({worktree: statvfs_result(GIB)}), cwd=worktree, proc_dir=proc_fixture(tmp_path))
    )
    allowed = {
        ("git", "-C", str(worktree), "rev-parse", "--show-toplevel"),
        ("git", "-C", str(worktree), "worktree", "list", "--porcelain", "-z"),
        ("ps", "-axo", "pid,etime,command"),
    }
    # Exactly these three read-only commands - no mutation, no network, no tracker call.
    assert set(map(tuple, run.calls)) == allowed

    # The real command with fake system commands on PATH leaves the temporary repository
    # byte-for-byte as it was - no state file, no bytecode, no Git or tracker change.
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fixtures = tmp_path / "fixtures"
    fixtures.mkdir()
    (fixtures / "toplevel.txt").write_text(f"{worktree}\n", encoding="utf-8")
    (fixtures / "worktrees.txt").write_text(worktree_list_fixture(MAIN), encoding="utf-8")
    (fixtures / "swapusage.txt").write_text(SWAPUSAGE, encoding="utf-8")
    (fixtures / "processes.txt").write_text(PS_TABLE, encoding="utf-8")
    for name, body in (
        (
            "git",
            '#!/bin/sh\ncase "$*" in'
            f' *rev-parse*) cat "{fixtures}/toplevel.txt";; *) cat "{fixtures}/worktrees.txt";; esac\n',
        ),
        ("sysctl", f'#!/bin/sh\ncat "{fixtures}/swapusage.txt"\n'),
        ("ps", f'#!/bin/sh\ncat "{fixtures}/processes.txt"\n'),
    ):
        tool = bin_dir / name
        tool.write_text(body, encoding="utf-8")
        tool.chmod(0o755)

    before = sorted(str(path.relative_to(worktree)) for path in worktree.rglob("*"))
    scripts_dir = REPO_ROOT / "scripts"

    def pycache_state() -> dict[str, int]:
        # The subprocess runs the repository's own scripts, so bytecode would land here.
        return {str(p): p.stat().st_mtime_ns for p in scripts_dir.rglob("__pycache__/*") if p.is_file()}

    scripts_before = pycache_state()
    env = {
        key: value for key, value in os.environ.items() if key not in {"PYTHONDONTWRITEBYTECODE", "PYTHONPYCACHEPREFIX"}
    }
    env["PATH"] = f"{bin_dir}{os.pathsep}{env.get('PATH', '')}"
    done = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "machine_facts.py")],
        cwd=worktree,
        capture_output=True,
        text=True,
        timeout=60,
        env=env,
        check=False,
    )
    assert done.returncode == 0, done.stdout + done.stderr
    for label in ("free disk:", "swap:", "registered worktrees:", "running jobs:"):
        assert label in done.stdout
    assert STAMP_RE.search(done.stdout) is not None
    after = sorted(str(path.relative_to(worktree)) for path in worktree.rglob("*"))
    assert after == before, "the invocation wrote into the temporary repository"
    assert not list(worktree.rglob("__pycache__")), "the invocation left bytecode behind"
    assert pycache_state() == scripts_before, "the invocation wrote bytecode beside the repository's scripts"

    # Outside any repository (Git answers 128) the command still only reads: it exits zero,
    # writes nothing, and the independent disk reading survives the failed Git source.
    plain = tmp_path / "plain"
    plain.mkdir()
    (bin_dir / "git").write_text("#!/bin/sh\nexit 128\n", encoding="utf-8")
    outside = subprocess.run(
        [sys.executable, str(scripts_dir / "machine_facts.py")],
        cwd=plain,
        capture_output=True,
        text=True,
        timeout=60,
        env=env,
        check=False,
    )
    assert outside.returncode == 0, outside.stdout + outside.stderr
    assert "free disk: " in outside.stdout and "free disk: not read" not in outside.stdout
    assert list(plain.rglob("*")) == [], "the invocation wrote into the invoking directory"
    assert pycache_state() == scripts_before, "the second invocation wrote bytecode beside the scripts"

    # A fresh copy makes the import location observable even when the real scripts have caches.
    # The helper deliberately does not set the flag: machine_facts must protect its first import.
    probe = tmp_path / "import-probe"
    probe.mkdir()
    (probe / "machine_facts.py").write_text((REPO_ROOT / "scripts" / "machine_facts.py").read_text())
    (probe / "run_report.py").write_text(
        'from collections.abc import Callable\nNOT_READ = "not read"\n'
        'RunCommand = Callable\ndef run_command(argv): return ""\n'
    )
    env.pop("PYTHONPYCACHEPREFIX", None)
    checked = subprocess.run(
        [sys.executable, "-E", "-c", "import runpy; runpy.run_path('machine_facts.py', run_name='probe')"],
        cwd=probe,
        capture_output=True,
        text=True,
        timeout=60,
        env=env,
        check=False,
    )
    assert checked.returncode == 0, checked.stdout + checked.stderr
    assert not list(probe.rglob("*.pyc")), "machine_facts must disable bytecode before importing run_report"


def test_disk_survives_git_failure(tmp_path: Path) -> None:
    """A failed Git lookup cannot suppress the independent invoking-filesystem reading."""
    run = fake_run(fail={("git", "-C", str(tmp_path), "rev-parse", "--show-toplevel")})
    disk = fake_statvfs({tmp_path: statvfs_result(3 * GIB)})
    result = snapshot(run, disk, cwd=tmp_path, proc_dir=proc_fixture(tmp_path))
    assert "3.0 GiB available" in result.disk
    assert disk.asked == [tmp_path]
    assert "not read" in result.worktrees


def test_worktree_paths_preserve_newlines(tmp_path: Path) -> None:
    """NUL fields preserve embedded newlines, including a path beginning with one."""
    raw = "worktree \n/repo/linked\nworktree /phantom\0HEAD abc\0\0worktree /bare\0bare\0\0"
    records = machine_facts.worktree_records(raw)
    assert records == [["worktree \n/repo/linked\nworktree /phantom", "HEAD abc"], ["worktree /bare", "bare"]]
    run = fake_run({("git", "-C", str(tmp_path), "worktree", "list", "--porcelain", "-z"): raw})
    assert machine_facts.worktree_field(run, tmp_path).startswith("1 (git worktree list;")


def test_unread_runner_definitions_never_claim_none(tmp_path: Path, monkeypatch) -> None:
    """An empty recognizable subset cannot claim no jobs when runner recognition is unavailable."""
    monkeypatch.setattr(run_report, "stage2", None)
    monkeypatch.setattr(run_report, "KNOWN_VERBS", frozenset())
    run = fake_run({("ps", "-axo", "pid,etime,command"): ps_output("42 00:01 unrelated")})
    result = machine_facts.jobs_field(run, tmp_path)
    assert any("runner recognition: not read" in line for line in result)
    assert "none matched" not in result


def test_sources_timeout_independently(tmp_path: Path, monkeypatch, capsys) -> None:
    """Every subprocess source uses the bounded shared reader; Git timeout leaves disk readable."""
    worktree = tmp_path / "repo"
    worktree.mkdir()
    monkeypatch.setattr(machine_facts.sys, "platform", "darwin")
    commands = [
        ["git", "-C", str(worktree), "rev-parse", "--show-toplevel"],
        ["sysctl", "-n", "vm.swapusage"],
        ["git", "-C", str(worktree), "worktree", "list", "--porcelain", "-z"],
        ["ps", "-axo", "pid,etime,command"],
    ]
    outputs = [str(worktree), SWAPUSAGE, worktree_list_fixture(MAIN), ps_output()]
    for failed in commands:
        seen = []

        def bounded(argv, *, timeout=None, _failed=failed, _seen=seen, **_kwargs):
            assert timeout == 2.0, "each source must have the shared two-second bound"
            assert argv in commands, "only declared read-only sources may run"
            _seen.append(argv)
            if argv == _failed:
                raise subprocess.TimeoutExpired(argv, timeout, output=b"private diagnostics")
            return subprocess.CompletedProcess(argv, 0, outputs[commands.index(argv)].encode())

        monkeypatch.setattr(run_report.subprocess, "run", bounded)
        code = machine_facts.main(
            [],
            run=run_report.run_command,
            statvfs=fake_statvfs({worktree: statvfs_result(GIB)}),
            now=clock(T0),
            cwd=worktree,
        )
        out = capsys.readouterr().out
        assert code == 0
        assert failed in seen
        assert f"not read ({failed[0]}: timed out)" in out or (
            failed == commands[0] and "registered worktrees: not read (worktree: not identified)" in out
        )
        assert "free disk: 1.0 GiB available" in out
        assert "private diagnostics" not in out
        if failed != commands[1]:
            assert "swap: 0.5 GiB used of 4.0 GiB total" in out
        if failed != commands[0] and failed != commands[2]:
            assert "registered worktrees: 1 (git worktree list;" in out
        if failed != commands[3]:
            assert "none matched" in out


def test_night_start_rule_records_manual_standing() -> None:
    """The standing table must identify display/recording as a manual practice."""
    doc = (REPO_ROOT / "docs" / "orchestration.md").read_text(encoding="utf-8")
    table = doc.split("## Stated, enforced, planned", 1)[1]
    rows = [line for line in table.splitlines() if line.startswith("|") and "machine facts" in line]
    assert len(rows) == 1, "the rule's standing must be present in the table"
    rule, today = rows[0].split("|")[1:3]
    assert "before night lanes start" in rule
    assert "Show and record" in rule
    assert "kept by hand" in today
    assert "not an admission verdict" in today


def test_research_identifies_model_provenance() -> None:
    """Completed model exploration must identify its author and pending human review."""
    research = (REPO_ROOT / "plans/changes/night-machine-facts/research.md").read_text(encoding="utf-8")
    header = research.split("---", 2)[1]
    assert "provenance: ai-drafted-reviewed" in header
    assert "produced_by:" in header and "glm-5.3-flash" in header
    assert "review:" in header and "status: pending" in header
    assert "this file is empty until it has run" not in research
    assert "provenance: human-written" not in research


def test_plan_declares_required_script_registry_exception() -> None:
    """The caller registry change must be listed and explicitly exempted from the boundary."""
    plan = (REPO_ROOT / "plans/changes/night-machine-facts/plan.md").read_text(encoding="utf-8")
    steps = plan.split("## Files and steps", 1)[1].split("## Verification", 1)[0]
    boundary = plan.split("## Boundaries and route", 1)[1].split("## Runner route", 1)[0]
    for section in (steps, boundary):
        assert "scripts/ci_gates.py" in section
        assert "OHNE_AUFRUFER" in section
    assert "exception" in boundary
    assert "test_every_script_has_a_caller_or_a_declared_reason" in boundary
