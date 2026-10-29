"""The run report of the active changes - and the cases in which its figures hold.

`scripts/run_report.py` reads what the runner wrote into a change folder and
prints it back as one local snapshot (plans/changes/run-report/spec.md). Every
fixture builds a small repository in `tmp_path`; the system sources (`ps`, the
macOS memory commands, `/proc/meminfo`) are injected, never really probed, and
no test starts a model, network or verification run. Each test names the fault
that turns it red; the fault is the ledger's em-dash text of its criterion.
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import run_report  # noqa: E402
import stage2  # noqa: E402

PS_ARGV = ("ps", "-axo", "pid,etime,command")
MEMINFO_QUIET = "MemTotal:  1000000 kB\nMemAvailable:  610000 kB\n"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def runner_line(
    verb: str = "implement",
    attempt: int = 1,
    route: str = "flash",
    model: str = "glm-5.3-flash",
    accepted: bool = True,
    seconds: int = 600,
) -> str:
    """One canonical runner time entry, built with the runner's own writer."""
    started = datetime(2026, 10, 28, 9, 0, 0)
    ended = started + timedelta(seconds=seconds)
    return stage2.time_entry(verb, attempt, route, model, accepted, started, ended, seconds)


def call_line(
    verb: str = "draft",
    clean: bool = True,
    fields: str = "attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol",
) -> str:
    check = "leak check clean over 7 files, 8 commits, 9 rules." if clean else "leak check BLOCK."
    body = f"{verb} · {fields} · {check}" if fields else check
    return f"Stage-2 call, 2026-10-28: {body}"


CARD = "For you:     demo.\nDone when:   demo holds.\nAppetite:    {appetite}\nNot now:     demo.\nPre-mortem:  demo.\n"


def plan_text(
    *,
    appetite: str = "2 hours of phase 4, repairs included; a stop, not an estimate.",
    frontmatter_appetite: str | None = None,
    card: bool = True,
    with_time: bool = True,
    time_body: str = "",
) -> str:
    header = "---\ntitle: demo\n"
    if frontmatter_appetite is not None:
        header += f"appetite: {frontmatter_appetite}\n"
    text = header + "---\n\n# Plan — demo\n\n"
    if card:
        text += "```text\n" + CARD.format(appetite=appetite) + "```\n\n"
    if with_time:
        text += "## Time used\n\n" + time_body + "\n"
    return text


def findings_text(*lines: str) -> str:
    return "---\ntitle: x\n---\n\n# Findings\n\n" + "\n\n".join(lines) + "\n"


def make_change(root: Path, name: str, plan: str | None = None, findings: str | None = None) -> Path:
    folder = root / "plans" / "changes" / name
    folder.mkdir(parents=True, exist_ok=True)
    if plan is not None:
        (folder / "plan.md").write_text(plan, encoding="utf-8")
    if findings is not None:
        (folder / "findings.md").write_text(findings, encoding="utf-8")
    return folder


def proc_fixture(tmp_path: Path, meminfo: str = MEMINFO_QUIET) -> Path:
    """An injected /proc directory, so memory figures never depend on the test machine."""
    proc = tmp_path / "proc"
    proc.mkdir(exist_ok=True)
    (proc / "meminfo").write_text(meminfo, encoding="utf-8")
    return proc


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


def ps_output(*lines: str) -> str:
    return "\n".join(["  PID   TIME COMMAND", *lines]) + "\n"


def run_main(root: Path, capsys, *args: str, run=None, proc_dir: Path | None = None) -> tuple[int, str]:
    code = run_report.main(["--root", str(root), *args], run=run if run is not None else fake_run(), proc_dir=proc_dir)
    captured = capsys.readouterr()
    return code, captured.out


def blocks(out: str) -> dict[str, list[str]]:
    """The output split per `change:` block and the live block, keyed by the token after the marker."""
    parts: dict[str, list[str]] = {}
    current: str | None = None
    for line in out.splitlines():
        if line.startswith("change: "):
            current = line[len("change: ") :]
            parts[current] = []
        elif line.startswith("live figures"):
            current = "live"
            parts[current] = []
        elif current is not None:
            parts[current].append(line)
    return parts


# ---------------------------------------------------------------------------
# The twelve criteria
# ---------------------------------------------------------------------------


def test_default_lists_active_changes_then_live(tmp_path: Path, capsys) -> None:
    """Fault: an archive appears, a plan-less active folder disappears, the ordering varies,
    or the live block is missing or repeated (spec criterion 1)."""
    root = tmp_path
    make_change(root, "alpha", plan=plan_text(time_body=runner_line()), findings="")
    make_change(root, "beta")  # an active folder without a plan.md must still be reported
    make_change(root, "archive/2026-10-01-old", plan=plan_text(time_body=runner_line()), findings="")
    proc = proc_fixture(tmp_path)
    code, out = run_main(root, capsys, proc_dir=proc)
    assert code == 0
    assert "UTC snapshot" in out  # one dated snapshot header
    assert out.index("change: alpha") < out.index("change: beta") < out.index("live figures")
    assert out.count("live figures") == 1
    assert "2026-10-01-old" not in out  # the archive is never included
    alpha = blocks(out)["alpha"]
    assert any("attempt: implement" in line for line in alpha)
    beta = blocks(out)["beta"]
    assert any("plan: not read" in line for line in beta)  # present, and honest about its plan


def test_selection_is_confined_and_never_falls_back(tmp_path: Path, capsys, monkeypatch) -> None:
    """Fault: another change is reported for a selection, a missing change looks empty and
    healthy, a selection escapes the active-change directory, or a symlink pulls in a
    foreign plan (spec criterion 2)."""
    root = tmp_path
    make_change(root, "alpha", plan=plan_text(time_body=runner_line()), findings="")
    make_change(root, "zeta", plan=plan_text(time_body=runner_line()), findings="")
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "plan.md").write_text(plan_text(time_body=runner_line()), encoding="utf-8")
    (root / "plans" / "changes" / "link").symlink_to(outside)
    proc = proc_fixture(tmp_path)

    code, out = run_main(root, capsys, "--change", "alpha", proc_dir=proc)
    assert code == 0
    assert "change: alpha" in out
    assert "change: zeta" not in out and "change: link" not in out

    code, out = run_main(root, capsys, "--change", "missing", proc_dir=proc)
    assert code == 0
    assert "not an active change" in out  # identified, not empty and healthy
    assert "change: alpha" not in out and "change: zeta" not in out
    assert "live figures" in out  # the report never falls back, and never goes empty

    code, out = run_main(root, capsys, "--change", "../alpha", proc_dir=proc)
    assert code == 0
    assert "not an active change" in out and "change: alpha" not in out  # no traversal

    code, out = run_main(root, capsys, "--change", "archive", proc_dir=proc)
    assert code == 0
    assert "not an active change" in out  # the archive is not an active change

    monkeypatch.setenv("CHANGE", "missing-env")
    code, out = run_main(root, capsys, proc_dir=proc)
    assert "not an active change" in out and "change: alpha" not in out
    monkeypatch.setenv("CHANGE", "zeta")
    code, out = run_main(root, capsys, proc_dir=proc)
    assert "change: zeta" in out and "change: alpha" not in out


def test_attempts_and_unfinished_calls_keep_recorded_metadata(tmp_path: Path, capsys) -> None:
    """Fault: a rejected attempt disappears, a clean leak check becomes an accepted verdict,
    missing fields are invented, or a repeated attempt number overwrites an earlier attempt
    (spec criterion 3)."""
    root = tmp_path
    body = "\n".join(
        [
            runner_line(verb="implement", attempt=1, accepted=True, seconds=600),
            runner_line(verb="implement", attempt=1, accepted=False, seconds=900),  # same number again
            runner_line(verb="implement", attempt=2, accepted=True, seconds=300),
        ]
    )
    findings = findings_text(
        call_line(),  # a clean leak check, with no measured completion behind it
        "Stage-2 session, 2026-10-28: an interactive session without fields.",
        call_line(verb="spec-review", clean=False, fields="route codex"),
    )
    make_change(root, "alpha", plan=plan_text(time_body=body), findings=findings)
    proc = proc_fixture(tmp_path)
    code, out = run_main(root, capsys, proc_dir=proc)
    assert code == 0
    alpha = blocks(out)["alpha"]
    attempts = [line for line in alpha if line.strip().startswith("attempt:")]
    assert len(attempts) == 3  # a repeated attempt number never overwrites history
    assert sum("rejected" in line for line in attempts) == 1
    calls = [line for line in alpha if line.strip().startswith("call:")]
    assert len(calls) == 3  # calls stay even without a measured completion
    assert all("verdict not recorded" in line for line in calls)
    assert not any("accepted" in line for line in calls)  # a clean leak check is not a verdict
    assert "attempt 1" in calls[0] and "route codex" in calls[0] and "model gpt-6.1-sol" in calls[0]
    assert "attempt not read" in calls[1] and "route not read" in calls[1]  # a session: no fields
    assert "route codex" in calls[2] and "model not read" in calls[2]  # absent fields, not invented
    assert any("evidence of a call" in line for line in alpha)


def test_measured_durations_sum_without_audit_or_live_double_counting(tmp_path: Path, capsys) -> None:
    """Fault: accepted, rejected or exact orchestrator seconds are omitted or counted twice,
    a call line or a live elapsed time enters the sum, or a following section contributes
    (spec criterion 4)."""
    root = tmp_path
    sums = "\n".join(
        [
            runner_line(accepted=True, seconds=600),
            runner_line(accepted=False, seconds=900),
            "- 2026-10-27 10:00–10:05, 300 s",  # a dated orchestrator record with explicit seconds
        ]
    )
    after = runner_line(attempt=2, seconds=600)  # behind the next heading: not the time section
    make_change(
        root,
        "sums",
        plan=plan_text(time_body=sums + "\n## Criterion ledger\n\n" + after + "\n"),
        findings=findings_text(call_line()),
    )
    ranges = "\n".join(
        [
            "- 2026-10-27 10:00–10:10 UTC",  # same-day clock endpoints
            "- 2026-10-27 23:55–2026-10-28 00:05 UTC",  # endpoints that carry their own date
            "- 2026-10-27 10:10–10:00 UTC",  # a non-positive range: rejected, never counted
        ]
    )
    make_change(root, "ranges", plan=plan_text(time_body=ranges), findings="")
    run = fake_run({PS_ARGV: ps_output("  501 01:00:00 make verify")})
    proc = proc_fixture(tmp_path)
    code, out = run_main(root, capsys, run=run, proc_dir=proc)
    assert code == 0
    sums_block = blocks(out)["sums"]
    assert "  time recorded: 1800 s" in sums_block  # 600 + 900 + 300, each record once
    assert not any("2400" in line for line in out.splitlines())  # the following section adds nothing
    ranges_block = blocks(out)["ranges"]
    assert "  time recorded: 1200 s" in ranges_block  # both ranges read from their endpoints
    assert "  unread lines: 1 — the time subtotal is incomplete" in ranges_block
    live = blocks(out)["live"]
    assert any("pid 501" in line and "verify" in line for line in live)  # shown live, never summed


def test_unread_time_is_visible_and_totals_are_partial(tmp_path: Path, capsys) -> None:
    """Fault: a malformed or approximate record supplies a guessed duration, an unread record
    vanishes silently, or an unreadable or missing section is presented as a measured zero
    (spec criterion 5)."""
    root = tmp_path
    body = "\n".join(
        [
            runner_line(seconds=600),
            "",
            "- 2026-10-06, about 10 min, by the orchestrating session; no appetite beyond the round.",
            "Readings of `date` at the step boundaries: 18:10 start and 18:44 stop.",
            runner_line(seconds=300).replace("accepted", "acceped"),  # runner-shaped but broken
        ]
    )
    make_change(root, "partial", plan=plan_text(time_body=body), findings="")
    make_change(root, "nosection", plan=plan_text(with_time=False, appetite="1 h of phase 4"), findings="")
    proc = proc_fixture(tmp_path)
    code, out = run_main(root, capsys, proc_dir=proc)
    assert code == 0
    partial = blocks(out)["partial"]
    assert "  time recorded: 600 s" in partial
    assert "  unread lines: 3 — the time subtotal is incomplete" in partial
    assert not any("610" in line or "660" in line or "900" in line for line in partial)  # nothing guessed
    nosection = blocks(out)["nosection"]
    assert any("time: not read" in line for line in nosection)
    assert not any("time recorded" in line for line in nosection)  # a missing section is not zero
    assert not any("half the appetite" in line for line in nosection)  # no comparison without time


def test_card_appetite_warns_at_half_including_rejected_time(tmp_path: Path, capsys) -> None:
    """Fault: the inclusive half boundary is wrong (1799 warns or 1800 does not against a
    one-hour appetite), rejected time is excluded, or a contradictory frontmatter budget
    wins over the card (spec criterion 6)."""
    root = tmp_path
    make_change(
        root, "just-under", plan=plan_text(appetite="1 h of phase 4", time_body=runner_line(seconds=1799)), findings=""
    )
    make_change(
        root,
        "at-half",
        plan=plan_text(appetite="1 h of phase 4", time_body=runner_line(accepted=False, seconds=1800)),
        findings="",
    )
    make_change(
        root,
        "card-wins",
        plan=plan_text(appetite="1 h of phase 4", frontmatter_appetite="99", time_body=runner_line(seconds=1800)),
        findings="",
    )
    proc = proc_fixture(tmp_path)
    code, out = run_main(root, capsys, proc_dir=proc)
    assert code == 0
    under = blocks(out)["just-under"]
    assert not any("warn:" in line for line in under)  # 1799 s against 1 h stays quiet
    half = blocks(out)["at-half"]
    warn = [line for line in half if "warn:" in line]
    assert warn and any("1800 s" in line for line in warn)  # rejected time counts
    assert any("half: 1800 s" in line for line in warn)  # the boundary is inclusive
    wins = blocks(out)["card-wins"]
    assert any("warn:" in line for line in wins)  # the card decides, not the frontmatter
    assert not any("99" in line for line in wins)


def test_unread_appetite_never_becomes_zero(tmp_path: Path, capsys) -> None:
    """Fault: an absent, unreadable, conflicting or non-positive card value becomes a zero
    budget, a ratio or a threshold verdict (spec criterion 7)."""
    root = tmp_path
    make_change(root, "no-card", plan=plan_text(card=False, frontmatter_appetite="2"), findings="")
    make_change(root, "unitless", plan=plan_text(appetite="2", frontmatter_appetite="2"), findings="")
    make_change(root, "zero", plan=plan_text(appetite="0 hours", frontmatter_appetite="2"), findings="")
    make_change(
        root, "competing", plan=plan_text(appetite="2 hours; at most 3 hours", frontmatter_appetite="2"), findings=""
    )
    make_change(
        root,
        "competing-time",
        plan=plan_text(
            appetite="2 hours; at most 3 hours", frontmatter_appetite="2", time_body=runner_line(seconds=600)
        ),
        findings="",
    )
    proc = proc_fixture(tmp_path)
    code, out = run_main(root, capsys, proc_dir=proc)
    assert code == 0
    for name in ("no-card", "unitless", "zero", "competing", "competing-time"):
        block = blocks(out)[name]
        assert any("appetite not read" in line for line in block), name
        assert not any("appetite: " in line for line in block), name  # no fabricated budget
        assert not any("warn:" in line for line in block), name  # no threshold verdict
        assert not any("appetite" in line and "%" in line for line in block), name  # no ratio


def test_process_filter_emits_only_permitted_fields(tmp_path: Path, capsys) -> None:
    """Fault: an option hides a supported runner invocation, a substring match adds unrelated
    processes, or command arguments beyond pid, label, change and elapsed leak (spec criterion 8)."""
    root = tmp_path
    make_change(root, "run-report", plan=plan_text(), findings="")
    listing = ps_output(
        "    1 00:01:02 python3 scripts/stage2.py implement run-report",
        "    2 00:02:03 python3 scripts/stage2.py implement --stage2-off reason run-report",
        "    3 00:30:00 make verify",
        "    4 1-02:03:04 bash scripts/verify_all.sh",
        "    9 00:00:10 python3 scripts/stage2.py draft run-report",
        "    5 00:01:00 vim scripts/stage2.py implement",  # an editor, not an invocation
        "    6 00:01:00 bash -c make verify",  # a shell wrapper
        "    7 00:01:00 tail -f scripts/stage2.py",  # a reader of the file
        "    8 00:10:00 echo SENTINEL-COMMAND run-report",  # an unrelated command
    )
    run = fake_run({PS_ARGV: listing})
    proc = proc_fixture(tmp_path)
    code, out = run_main(root, capsys, run=run, proc_dir=proc)
    assert code == 0
    live = "\n".join(blocks(out)["live"])
    for row in [
        "pid 1 · implement · change run-report · elapsed 00:01:02",
        "pid 2 · implement · change run-report · elapsed 00:02:03",  # the option hides nothing
        "pid 3 · verify · change not read · elapsed 00:30:00",
        "pid 4 · verify · change not read · elapsed 1-02:03:04",
        "pid 9 · draft · change run-report · elapsed 00:00:10",
    ]:
        assert f"    {row}" in live
    for absent in ("pid 5", "pid 6", "pid 7", "pid 8", "vim", "tail", "echo", "SENTINEL-COMMAND", "--stage2-off"):
        assert absent not in live


def test_memory_sources_preserve_units_and_unknowns(tmp_path: Path) -> None:
    """Fault: stored compressor pages stand for occupied ones, the page size or the physical
    denominator is dropped, zswap units or the MemTotal denominator are wrong, or a missing
    field becomes zero (spec criterion 9)."""
    run = fake_run(
        {
            ("memory_pressure",): "System-wide memory free percentage: 68%\n",
            ("vm_stat",): (
                "Mach Virtual Memory Statistics: (page size of 16384 bytes)\n"
                "Pages free: 1.\n"
                "Pages occupied by compressor: 100000.\n"
                "Pages stored in compressor: 999999.\n"
            ),
            ("sysctl", "-n", "hw.memsize"): "17179869184\n",
        }
    )
    snapshot = run_report.macos_memory(run)
    assert snapshot.available.startswith("68% of physical memory")
    assert snapshot.available_percent == 68.0
    assert "9.5% of physical memory" in snapshot.compressed  # 100000 occupied pages of 16384 bytes
    assert "hw.memsize" in snapshot.compressed  # the physical denominator is named
    assert "999999" not in snapshot.compressed  # stored pages never stand for occupied ones

    stored_only = fake_run(
        {
            ("memory_pressure",): "System-wide memory free percentage: 68%\n",
            ("vm_stat",): "Mach Virtual Memory Statistics: (page size of 16384 bytes)\n"
            "Pages stored in compressor: 999999.\n",
            ("sysctl", "-n", "hw.memsize"): "17179869184\n",
        }
    )
    snapshot = run_report.macos_memory(stored_only)
    assert snapshot.compressed.startswith("not read") and "999999" not in snapshot.compressed
    assert snapshot.available_percent == 68.0  # one missing piece never erases the other

    no_sysctl = fake_run(
        {
            ("memory_pressure",): "Free percentage: 40%\n",
            ("vm_stat",): "Mach Virtual Memory Statistics: (page size of 16384 bytes)\n"
            "Pages occupied by compressor: 10.\n",
        },
        fail={("sysctl", "-n", "hw.memsize")},
    )
    snapshot = run_report.macos_memory(no_sysctl)
    assert snapshot.compressed.startswith("not read")  # no denominator, no percentage
    assert snapshot.available_percent == 40.0

    proc = tmp_path / "proc"
    proc.mkdir()
    (proc / "meminfo").write_text(
        "MemTotal:  1000000 kB\nMemAvailable:  250000 kB\nZswap:  50000 kB\nZswapped:  999999 kB\n",
        encoding="utf-8",
    )
    snapshot = run_report.linux_memory(proc)
    assert snapshot.available.startswith("25.0% of physical memory")
    assert "5.0% of MemTotal" in snapshot.compressed and "zswap" in snapshot.compressed
    assert "999999" not in snapshot.compressed  # uncompressed Zswapped bytes are never substituted

    (proc / "meminfo").write_text("MemTotal:  1000000 kB\nMemAvailable:  250000 kB\n", encoding="utf-8")
    snapshot = run_report.linux_memory(proc)
    assert snapshot.compressed.startswith("not read")  # a missing source is not zero

    (proc / "meminfo").write_text("MemTotal:  0 kB\nZswap:  50000 kB\n", encoding="utf-8")
    snapshot = run_report.linux_memory(proc)
    assert snapshot.available.startswith("not read") and snapshot.available_percent is None
    assert snapshot.compressed.startswith("not read")  # a non-positive denominator reads as not read


def test_low_memory_warning_is_advisory_and_strictly_below_floor(tmp_path: Path, capsys) -> None:
    """Fault: 24 percent fails to warn, 25 percent warns, or the report starts, stops or
    locks a verification step instead of advising (spec criterion 10)."""
    root = tmp_path
    make_change(root, "alpha", plan=plan_text(), findings="")
    run = fake_run({PS_ARGV: ps_output("  7 00:00:07 make verify")})

    low = proc_fixture(tmp_path, meminfo="MemTotal:  1000000 kB\nMemAvailable:  240000 kB\n")
    code, out = run_main(root, capsys, run=run, proc_dir=low)
    assert code == 0
    assert "below the 25% floor" in out  # 24 percent warns
    assert "starts, stops and blocks nothing" in out  # advisory, not an interlock
    assert "pid 7" in out  # the verify process is shown, not started, stopped or locked

    at_floor = proc_fixture(tmp_path, meminfo="MemTotal:  1000000 kB\nMemAvailable:  250000 kB\n")
    code, out = run_main(root, capsys, run=run, proc_dir=at_floor)
    assert code == 0
    assert "below the 25% floor" not in out  # 25 percent is not below the floor

    unread = proc_fixture(tmp_path, meminfo="MemTotal:  1000000 kB\nZswap:  50000 kB\n")
    code, out = run_main(root, capsys, run=run, proc_dir=unread)
    assert "below the 25% floor" not in out  # an unread percentage never warns
    assert "available: not read" in out
    started = {tuple(argv) for argv in run.calls}
    assert started == {PS_ARGV}  # only the process probe ran; no verification was launched


def test_source_failures_are_independent_bounded_and_exit_zero(tmp_path: Path, capsys) -> None:
    """Fault: a failed process probe suppresses valid change totals, a missing memory tool
    hangs the report, an unreadable plan crashes, or a traceback replaces a bounded
    source-specific diagnostic (spec criterion 11)."""
    root = tmp_path
    make_change(root, "alpha", plan=plan_text(time_body=runner_line()), findings="")
    proc = proc_fixture(tmp_path)

    no_ps = fake_run({}, fail={PS_ARGV})
    code, out = run_main(root, capsys, run=no_ps, proc_dir=proc)
    assert code == 0
    assert "  time recorded: 600 s" in blocks(out)["alpha"]  # the change totals stand
    assert "processes: not read" in out  # the failed probe is named, bounded
    assert "available: 61.0%" in out  # the independent source still reads

    ps_only = fake_run({PS_ARGV: ps_output("  7 00:00:07 make verify")})
    absent = tmp_path / "absent-proc"  # a memory source that is not there, on any OS
    code, out = run_main(root, capsys, run=ps_only, proc_dir=absent)
    assert code == 0
    assert "pid 7" in out  # the process table stands
    assert "available: not read" in out and "compressed: not read" in out  # the missing source is named

    broken = root / "plans" / "changes" / "broken"
    broken.mkdir()
    (broken / "plan.md").write_bytes(b"\xff\xfe not utf-8")
    code, out = run_main(root, capsys, proc_dir=proc)
    assert code == 0
    assert "Traceback" not in out  # a bounded diagnostic, never an exception dump
    assert "change: broken" in out
    assert any("plan: not read" in line for line in blocks(out)["broken"])
    assert "  time recorded: 600 s" in blocks(out)["alpha"]  # the other change is untouched


def test_report_is_read_only_local_and_does_not_echo_prose(tmp_path: Path, capsys) -> None:
    """Fault: a sentinel in findings prose, a process argument or a memory diagnostic reaches
    the output, an input file changes, or a forbidden command runs (spec criterion 12)."""
    root = tmp_path
    sentinel_findings = (
        "---\ntitle: x\n---\n\n# Findings\n\n"
        "> SENTINEL-PROMPT and SENTINEL-ANSWER quoted from an attempt diagnostic.\n\n" + call_line() + "\n"
    )
    make_change(root, "alpha", plan=plan_text(time_body=runner_line()), findings=sentinel_findings)
    run = fake_run(
        {
            PS_ARGV: ps_output(
                "    3 00:30:00 make verify",
                "    8 00:10:00 echo SENTINEL-COMMAND-ARG alpha",
            ),
            ("memory_pressure",): "System-wide memory free percentage: 61%\nSENTINEL-MEMORY-DIAGNOSTIC\n",
            ("vm_stat",): "Mach Virtual Memory Statistics: (page size of 16384 bytes)\n"
            "Pages occupied by compressor: 5.\nSENTINEL-VM-EXTRA\n",
            ("sysctl", "-n", "hw.memsize"): "17179869184\n",
        }
    )
    proc = proc_fixture(tmp_path, meminfo=MEMINFO_QUIET + "SENTINEL-PROC  1 kB\n")

    def tree() -> tuple[list[str], dict[str, bytes]]:
        entries = sorted(str(p.relative_to(root)) for p in root.rglob("*"))
        files = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}
        return entries, files

    before = tree()
    code, out = run_main(root, capsys, run=run, proc_dir=proc)
    assert code == 0
    for sentinel in (
        "SENTINEL-PROMPT",
        "SENTINEL-ANSWER",
        "SENTINEL-COMMAND-ARG",
        "SENTINEL-MEMORY-DIAGNOSTIC",
        "SENTINEL-VM-EXTRA",
        "SENTINEL-PROC",
    ):
        assert sentinel not in out
    assert tree() == before  # every file byte and directory entry as it was
    started = {tuple(argv) for argv in run.calls}
    assert started == {PS_ARGV}  # with proc_dir injected, ps is the only probed command
    snapshot = run_report.macos_memory(run)  # the macOS parsers bound their output the same way
    assert "SENTINEL-MEMORY-DIAGNOSTIC" not in snapshot.available
    assert "SENTINEL-VM-EXTRA" not in snapshot.compressed


def test_make_report_passes_change_as_data_and_is_not_a_gate(tmp_path: Path, capsys, monkeypatch) -> None:
    """Fault: the make recipe interpolates the selection into the shell line, or reporting
    becomes a verification gate (spec criterion 12)."""
    makefile = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")
    phony = next(line for line in makefile.splitlines() if line.startswith(".PHONY:"))
    assert "report" in phony.split()
    recipe = next(line for line in makefile.splitlines() if line.startswith("\t") and "run_report.py" in line)
    assert recipe == "\t@export CHANGE; python3 scripts/run_report.py"  # the value never enters the line
    assert "$(CHANGE)" not in makefile  # no interpolation: the selection stays data
    gates = (REPO_ROOT / "decisions" / "gates.yaml").read_text(encoding="utf-8")
    assert "run_report" not in gates and "make report" not in gates  # reporting is not a gate

    root = tmp_path
    make_change(root, "alpha", plan=plan_text(), findings="")
    make_change(root, "beta", plan=plan_text(), findings="")
    monkeypatch.setenv("CHANGE", "beta")
    proc = proc_fixture(tmp_path)
    code, out = run_main(root, capsys, proc_dir=proc)  # no --change: the environment selects
    assert code == 0
    assert "change: beta" in out and "change: alpha" not in out


def test_exact_range_with_unmeasured_prose_stays_unread(tmp_path: Path) -> None:
    """An exact range must not override prose declaring the record unmeasured."""
    for prose in ("about 30 min", "approximately 30 min", "not measured by the orchestrator"):
        folder = make_change(tmp_path, "alpha", plan=plan_text(time_body=f"2026-10-28 10:00–10:30 UTC, {prose}"))
        reading, _ = run_report.read_time(folder / "plan.md")
        assert reading.unread == 1
        assert reading.seconds == 0
    assert run_report.parse_time_line("2026-10-28 10:00–10:30 UTC") is not None


def test_session_calls_keep_explicit_fields_and_dispatch_state() -> None:
    for state in ("accepted", "failed (PRIVATE_DETAIL)", "pending"):
        rows = run_report.call_rows(
            findings_text(
                f"Stage-2 session, 2026-10-28: attempt abc123 · model glm-5.3-flash · "
                f"endpoint glm-coding-plan · leak check clean over 7 files · dispatch {state}."
            )
        )
        assert len(rows) == 1
        row = rows[0]
        assert "attempt abc123" in row and "model glm-5.3-flash" in row
        assert "endpoint glm-coding-plan" in row and "route not read" in row
        assert f"dispatch {state.split()[0]}" in row
        assert "verdict not recorded" not in row and "PRIVATE_DETAIL" not in row


def test_change_listing_failure_keeps_live_block(tmp_path: Path, capsys, monkeypatch) -> None:
    proc = proc_fixture(tmp_path)
    code, out = run_main(tmp_path, capsys, proc_dir=proc)
    assert code == 0
    assert "change list: not read (plans/changes:" in out and "live figures:" in out
    changes = tmp_path / "plans" / "changes"
    changes.mkdir(parents=True)
    original = Path.iterdir

    def denied(path):
        if path == changes:
            raise PermissionError("PRIVATE_DETAIL")
        return original(path)

    monkeypatch.setattr(Path, "iterdir", denied)
    code, out = run_main(tmp_path, capsys, proc_dir=proc)
    assert code == 0 and "change list: not read (plans/changes:" in out
    assert "live figures:" in out and "PRIVATE_DETAIL" not in out


def test_runner_options_with_values_do_not_hide_change() -> None:
    for command in (
        "python3 scripts/stage2.py implement --stage2-off reason alpha",
        "python3 scripts/stage2.py session --model glm-5.3-flash alpha",
        "python3 scripts/stage2.py session --model=glm-5.3-flash alpha",
    ):
        rows = run_report.parse_processes(ps_output(f"123 00:10 {command}"), frozenset({"alpha"}))
        assert len(rows) == 1 and rows[0].change == "alpha"


def test_shebang_runner_is_matched_without_matching_wrapper() -> None:
    rows = run_report.parse_processes(
        ps_output(
            "123 00:10 ./scripts/stage2.py implement alpha",
            "124 00:10 echo ./scripts/stage2.py implement alpha",
            "125 00:10 sh -c ./scripts/stage2.py implement alpha",
        ),
        frozenset({"alpha"}),
    )
    assert [(row.pid, row.change) for row in rows] == [("123", "alpha")]


def test_unread_meminfo_names_each_missing_reading(tmp_path: Path) -> None:
    snapshot = run_report.linux_memory(tmp_path)
    assert "not read" in snapshot.available and "MemAvailable/MemTotal" in snapshot.available
    assert "not read" in snapshot.compressed and "Zswap/MemTotal" in snapshot.compressed


def test_plan_failure_preserves_independent_findings_calls(tmp_path: Path) -> None:
    folder = make_change(tmp_path, "alpha", findings=findings_text(call_line()))
    for unreadable in (False, True):
        if unreadable:
            (folder / "plan.md").write_bytes(b"\xff")
        out = "\n".join(run_report.change_block(folder, "alpha"))
        assert "plan: not read" in out
        assert "call: draft · attempt 1 · route codex" in out
        assert "time recorded: 0" not in out


def test_time_failure_preserves_runner_reason(tmp_path: Path) -> None:
    plan = tmp_path / "plan.md"
    reading, reason = run_report.read_time(plan)
    assert not reading.section_read and "cannot be read" in reason
    plan.write_text("# No time section\n", encoding="utf-8")
    reading, reason = run_report.read_time(plan)
    assert not reading.section_read and "has no `## Time used` heading" in reason


def test_readable_appetite_survives_unrelated_card_defect(tmp_path: Path) -> None:
    text = plan_text(appetite="2 hours", time_body=runner_line(seconds=3600))
    for defective in (
        text.replace("Pre-mortem:  demo.\n", ""),
        text.replace("Not now:     demo.\nPre-mortem:  demo.", "Pre-mortem:  demo.\nNot now:     demo."),
    ):
        assert stage2.card_problem(defective) is not None
        folder = make_change(tmp_path, "alpha", plan=defective)
        out = "\n".join(run_report.change_block(folder, "alpha"))
        assert "appetite: 7200 s" in out
        assert "at or over half the appetite" in out


def test_annotated_orchestrator_seconds_are_recorded(tmp_path: Path) -> None:
    body = "\n".join(
        [
            "2026-10-29 01:01:00–01:02:44 UTC, 104 s — review loop round 1 · measured with `date -u`",
            "2026-10-29 01:44:14–01:44:32 UTC, 18 s — review loop round 2 · measured with `date -u`",
            # Explicit seconds remain authoritative even when endpoints disagree.
            "2026-10-29 02:00:00–02:01:00 UTC, 7 s — orchestrator check",
            runner_line(seconds=600),
            runner_line(seconds=300).replace("accepted", "acceped"),
        ]
    )
    folder = make_change(tmp_path, "alpha", plan=plan_text(time_body=body), findings="")
    reading, reason = run_report.read_time(folder / "plan.md")
    assert reason == "" and reading.section_read
    assert reading.seconds == 729
    assert reading.unread == 1  # the malformed runner entry still cannot become time
    assert len(reading.attempts) == 1


def test_stage2_off_without_reason_preserves_change() -> None:
    for arguments in (
        "--stage2-off alpha",
        "--stage2-off --class bounded alpha",
        "--stage2-off reason alpha",
        "--stage2-off=reason alpha",
        "alpha --stage2-off",
    ):
        rows = run_report.parse_processes(
            ps_output(f"123 00:10 python3 scripts/stage2.py implement {arguments}"),
            frozenset({"alpha"}),
        )
        assert len(rows) == 1 and rows[0].change == "alpha", arguments


def test_unread_plan_reason_never_exposes_absolute_path(tmp_path: Path) -> None:
    folder = make_change(tmp_path / "PRIVATE-PATH", "alpha", findings="")
    for content in (None, b"\xff", b"# No time section\n"):
        if content is not None:
            (folder / "plan.md").write_bytes(content)
        out = "\n".join(run_report.change_block(folder, "alpha"))
        expected = "cannot be read." if content in (None, b"\xff") else "has no `## Time used` heading."
        assert f"time: not read (plan.md {expected})" in out
        assert str(tmp_path) not in out
        assert "PRIVATE-PATH" not in out


def test_unreadable_change_metadata_preserves_other_changes_and_live(tmp_path: Path, capsys, monkeypatch) -> None:
    unreadable = make_change(tmp_path, "run-report", plan=plan_text())
    make_change(tmp_path, "alpha", plan=plan_text(time_body=runner_line(seconds=600)))
    proc = proc_fixture(tmp_path)
    run = fake_run({PS_ARGV: ps_output("123 00:10 make verify")})
    original = Path.stat

    def denied(path, *args, **kwargs):
        if path == unreadable:
            raise PermissionError("PRIVATE_DETAIL")
        return original(path, *args, **kwargs)

    monkeypatch.setattr(Path, "stat", denied)
    code, out = run_main(tmp_path, capsys, run=run, proc_dir=proc)
    assert code == 0
    assert "plans/changes/run-report: not read" in out
    assert "change: alpha" in out and "time recorded: 600 s" in out
    assert "live figures:" in out and "pid 123 · verify" in out
    assert "available: 61.0%" in out
    assert run.calls == [list(PS_ARGV)]
    assert "PRIVATE_DETAIL" not in out and "internal error" not in out


def test_echo_naming_python_runner_is_not_a_runner() -> None:
    rows = run_report.parse_processes(
        ps_output(
            "123 00:10 echo python3 scripts/stage2.py implement run-report",
            "124 00:10 /usr/bin/python3 -u scripts/stage2.py implement run-report",
        ),
        frozenset({"run-report"}),
    )
    assert [(row.pid, row.label, row.change) for row in rows] == [("124", "implement", "run-report")]


def test_verification_options_before_target_or_script_are_visible() -> None:
    rows = run_report.parse_processes(
        ps_output(
            "123 00:10 make -j2 verify",
            "124 00:10 make --no-print-directory verify",
            "125 00:10 bash -e scripts/verify_all.sh",
            "126 00:10 bash -c echo scripts/verify_all.sh",
            "127 00:10 make -f verify unrelated",
        ),
        frozenset(),
    )
    assert [(row.pid, row.label, row.change) for row in rows] == [
        (pid, "verify", "not read") for pid in ("123", "124", "125")
    ]
