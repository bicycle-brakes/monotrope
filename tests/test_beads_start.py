"""The repository start hook: reconcile first, prime second, write only alone.

`tools/claude-code/hooks/beads-start.sh` replaces the direct
`tools/bd prime --hook-json` session start: the starting session is the tracker
writer (house rule 4), so it runs `scripts/close_merged_beads.py --write` to
completion before the prime context is built — and it only writes when it is
provably alone (no recap child, no compaction, a readable scan, no live clash
or sibling worktree). The hook is exercised directly against a sandbox
project with disposable Git history, a recording fake `tools/bd` and a fake
session registry under a fake HOME — this repository's tracker and registry
are never touched.

The subject itself (`tools/claude-code/`) is part of this repo and does not
travel with the kit — where it is absent, this file skips (skipif below).
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
HOOKS = REPO_ROOT / "tools" / "claude-code" / "hooks"
HOOK = HOOKS / "beads-start.sh"
SCAN = HOOKS / "session-scan.sh"

# The script plus its import closure: the sandbox copies render through the
# sandbox's own fake wrapper, never through this repo's tracker.
SCRIPTS = ("close_merged_beads.py", "bead_render.py", "render_beads_export.py", "check_bead_export.py")

MAIN = "coding-harness-main"
MERGE_SHA_NOTE = "#291"

PRIME_TEXT = '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"PRIME-KONTEXT"}}\n'

STUB = """#!/bin/bash
# Recording stand-in for the pinned tools/bd (test fixture, never this repo's).
printf '%s\\n' "$*" >>"${BEADS_STUB_LOG:?}"
case "$1" in
  export)
    out=""
    while [ $# -gt 0 ]; do
      if [ "$1" = "-o" ]; then out=$2; fi
      shift
    done
    if [ -z "$out" ]; then echo "export: no -o target" >&2; exit 1; fi
    cp "${BEADS_STUB_RENDER:?}" "$out"
    ;;
  close)
    if [ "$2" = "${BEADS_STUB_REFUSE:-}" ]; then
      echo "assignee is worker-a, actor is the reconciler" >&2
      exit 1
    fi
    ;;
  dolt)
    if [ "${BEADS_STUB_PUSH_RC:-0}" != "0" ]; then
      echo "dolt push: the remote refused" >&2
      exit "${BEADS_STUB_PUSH_RC}"
    fi
    ;;
  prime)
    cat "${BEADS_STUB_PRIME:?}"
    ;;
esac
exit 0
"""

pytestmark = pytest.mark.skipif(
    not (HOOK.is_file() and SCAN.is_file()) or shutil.which("jq") is None,
    reason="tools/claude-code is part of this repo and does not travel (kit probe); the scan needs jq",
)


def _git(cwd: Path, *args: str) -> str:
    erg = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=120, check=False)
    assert erg.returncode == 0, f"git {' '.join(args)} failed: {erg.stderr}"
    return erg.stdout.strip()


def _commit(cwd: Path, message: str) -> str:
    erg = subprocess.run(
        [
            "git",
            "-c",
            "user.email=test@example.invalid",
            "-c",
            "user.name=Test",
            "-c",
            "commit.gpgsign=false",
            "commit",
            "--allow-empty",
            "-m",
            message,
            "--quiet",
        ],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert erg.returncode == 0, erg.stderr
    return _git(cwd, "rev-parse", "HEAD")


def _project(
    tmp_path: Path,
    *,
    name: str = "main",
    push_rc: int = 0,
    refuse: str = "",
) -> SimpleNamespace:
    """A sandbox project: Git history with one merged declaration, fake
    wrapper, the hook with its scan, and a fake HOME with an empty registry."""
    origin = tmp_path / f"origin-{name}"
    origin.mkdir()
    _git(origin, "init", "--initial-branch=main", "--quiet")
    _git(origin, "config", "user.email", "test@example.invalid")
    _git(origin, "config", "user.name", "Test")
    _commit(origin, "base of the fixture history")
    merged = _commit(origin, f"feat(hook): the merged work ({MERGE_SHA_NOTE})\n\nCloses-Bead: {MAIN}")

    klon = tmp_path / f"klon-{name}"
    _git(tmp_path, "clone", "--quiet", str(origin), str(klon))
    scripts = klon / "scripts"
    scripts.mkdir()
    for script in SCRIPTS:
        (scripts / script).write_bytes((REPO_ROOT / "scripts" / script).read_bytes())
    hooks_dir = klon / "tools" / "claude-code" / "hooks"
    hooks_dir.mkdir(parents=True)
    for source in (HOOK, SCAN):
        (hooks_dir / source.name).write_bytes(source.read_bytes())
        (hooks_dir / source.name).chmod(0o755)
    stub = klon / "tools" / "bd"
    stub.write_text(STUB, encoding="utf-8")
    stub.chmod(0o755)

    home = tmp_path / f"home-{name}"
    (home / ".claude" / "sessions").mkdir(parents=True)
    prime = tmp_path / f"prime-{name}.json"
    prime.write_text(PRIME_TEXT, encoding="utf-8")
    render = tmp_path / f"render-{name}.jsonl"
    render.write_text(json.dumps({"id": MAIN, "status": "open"}) + "\n", encoding="utf-8")
    log = tmp_path / f"stub-{name}.log"

    return SimpleNamespace(
        origin=origin,
        klon=klon,
        home=home,
        hooks_dir=hooks_dir,
        log=log,
        render=render,
        prime=prime,
        push_rc=push_rc,
        refuse=refuse,
        merged=merged,
    )


def _session(home: Path, *, pid: int, sid: str, cwd: Path) -> None:
    """A fake registry entry, as Claude Code writes it to ~/.claude/sessions/.

    `procStart` stays empty on purpose: the scan compares it only when present,
    and a test that faked `ps` localisation would check the wrong thing.
    """
    satz = {
        "pid": pid,
        "sessionId": sid,
        "cwd": str(cwd),
        "name": None,
        "status": None,
        "kind": "interactive",
        "procStart": "",
    }
    (home / ".claude" / "sessions" / f"{pid}.json").write_text(json.dumps(satz), encoding="utf-8")


def _start(
    ns: SimpleNamespace,
    *,
    sid: str = "sess-a",
    source: str = "startup",
    extra: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    payload = {"session_id": sid, "hook_event_name": "SessionStart", "cwd": str(ns.klon), "source": source}
    env = {key: value for key, value in os.environ.items() if key != "BEAD_RENDER"}
    env.update(
        HOME=str(ns.home),
        CLAUDE_PROJECT_DIR=str(ns.klon),
        BEADS_STUB_LOG=str(ns.log),
        BEADS_STUB_RENDER=str(ns.render),
        BEADS_STUB_PUSH_RC=str(ns.push_rc),
        BEADS_STUB_REFUSE=ns.refuse,
        BEADS_STUB_PRIME=str(ns.prime),
    )
    if extra:
        env.update(extra)
    return subprocess.run(
        ["bash", str(ns.hooks_dir / "beads-start.sh")],
        input=json.dumps(payload),
        cwd=ns.klon,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )


def _calls(ns: SimpleNamespace) -> list[str]:
    if not ns.log.exists():
        return []
    return ns.log.read_text(encoding="utf-8").splitlines()


def _wrote(ns: SimpleNamespace) -> bool:
    return any(line.startswith("close ") or line.startswith("dolt") for line in _calls(ns))


def _path_without_jq(tmp_path: Path) -> str:
    """A PATH that can run the hook but cannot read a registry: no jq."""
    bin_dir = tmp_path / "bin-ohne-jq"
    bin_dir.mkdir()
    for name in (
        "bash",
        "sh",
        "dirname",
        "mktemp",
        "rm",
        "cat",
        "sleep",
        "head",
        "grep",
        "git",
        "ps",
        "sed",
        "tr",
        "basename",
        "cp",
    ):
        found = shutil.which(name)
        assert found, f"{name} is missing — a jq-less PATH cannot be built here"
        (bin_dir / name).symlink_to(found)
    (bin_dir / "python3").symlink_to(sys.executable)
    return str(bin_dir)


def test_reconcile_finishes_before_prime(tmp_path: Path) -> None:
    """Criterion 10: the writing reconciliation completes before prime runs —
    and when it fails, the prime context still arrives, with the failure in
    German and never as a claim that nothing is pending."""
    ns = _project(tmp_path)
    erg = _start(ns)
    assert erg.returncode == 0, erg.stderr
    assert erg.stdout == PRIME_TEXT, "a quiet success passes prime's JSON through untouched"
    assert erg.stderr.strip() == "", "a successful run is quiet"

    calls = _calls(ns)
    close_at = calls.index(f"close {MAIN} --reason=merged into main: declared by commit {ns.merged} (PR #291)")
    push_at = calls.index("dolt push")
    prime_at = calls.index("prime --hook-json")
    assert close_at < push_at < prime_at, f"the order broke: {calls}"

    failed = _project(tmp_path, name="failed", push_rc=1)
    erg = _start(failed)
    assert erg.returncode == 0, erg.stderr
    kontext = json.loads(erg.stdout)["hookSpecificOutput"]["additionalContext"]
    assert "PRIME-KONTEXT" in kontext, "a reconciliation failure lost the prime context"
    assert "Beads-Abgleich fehlgeschlagen" in kontext
    assert "nichts offen" in kontext, "the failure must not read as a statement about pending closures"
    assert "Beads-Abgleich fehlgeschlagen" in erg.stderr

    calls = _calls(failed)
    close_line = f"close {MAIN} --reason=merged into main: declared by commit {failed.merged} (PR #291)"
    assert calls.index(close_line) < calls.index("prime --hook-json"), f"prime ran before the attempt: {calls}"


def test_secondary_or_uncertain_start_never_writes(tmp_path: Path) -> None:
    """Criterion 11: another live session in the same checkout or a sibling
    worktree, a recap child and an unreadable eligibility check all skip the
    write — while the prime context still arrives. The fixture bead is open
    and declared: were the hook to write, the fake wrapper would log it."""
    clash = _project(tmp_path, name="clash")
    _session(clash.home, pid=os.getpid(), sid="sess-b", cwd=clash.klon)
    erg = _start(clash, sid="sess-a")
    assert erg.returncode == 0, erg.stderr
    assert not _wrote(clash), "a second session in the same checkout wrote the tracker"
    assert "prime --hook-json" in _calls(clash)
    kontext = json.loads(erg.stdout)["hookSpecificOutput"]["additionalContext"]
    assert "PRIME-KONTEXT" in kontext and "übersprungen" in kontext

    sibling = _project(tmp_path, name="sibling")
    wt = sibling.klon.parent / f"wt-{sibling.klon.name}"
    _git(sibling.klon, "worktree", "add", "--quiet", str(wt), "-b", "wt-branch")
    _session(sibling.home, pid=os.getpid(), sid="sess-c", cwd=wt)
    erg = _start(sibling)
    assert erg.returncode == 0, erg.stderr
    assert not _wrote(sibling), "a sibling worktree session wrote the tracker"
    assert "prime --hook-json" in _calls(sibling)
    assert "übersprungen" in json.loads(erg.stdout)["hookSpecificOutput"]["additionalContext"]

    child = _project(tmp_path, name="child")
    erg = _start(child, extra={"CLAUDE_RECAP_CHILD": "1"})
    assert erg.returncode == 0, erg.stderr
    assert not _wrote(child), "a recap child wrote the tracker"
    assert "prime --hook-json" in _calls(child)
    assert "übersprungen" in json.loads(erg.stdout)["hookSpecificOutput"]["additionalContext"]

    unscannable = _project(tmp_path, name="unscannable")
    (unscannable.hooks_dir / "session-scan.sh").unlink()
    erg = _start(unscannable)
    assert erg.returncode == 0, erg.stderr
    assert not _wrote(unscannable), "a missing scan still allowed writing"
    assert "prime --hook-json" in _calls(unscannable)

    unreadable = _project(tmp_path, name="unreadable")
    erg = _start(unreadable, extra={"PATH": _path_without_jq(tmp_path)})
    assert erg.returncode == 0, erg.stderr
    assert not _wrote(unreadable), "an unreadable eligibility check still allowed writing"
    assert "prime --hook-json" in _calls(unreadable)
    assert erg.stdout == PRIME_TEXT, "without jq the prime context passes through untouched"
    assert "übersprungen" in erg.stderr


@pytest.mark.parametrize("failed_query", ["--show-toplevel", "--git-common-dir"])
def test_uninspectable_live_peer_prevents_writing(tmp_path: Path, failed_query: str) -> None:
    """A failed peer Git query leaves ownership unknown, even with stdout."""
    ns = _project(tmp_path)
    peer = tmp_path / "peer"
    _git(ns.klon, "worktree", "add", "--quiet", str(peer), "-b", "peer")
    _session(ns.home, pid=os.getpid(), sid="peer-session", cwd=peer)
    real_git = shutil.which("git")
    assert real_git is not None
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_git = bin_dir / "git"
    fake_git.write_text(
        "#!/bin/bash\n"
        'if [ "$3" = "$PEER_CWD" ] && [ "${!#}" = "$FAILED_QUERY" ]; then\n'
        '  printf "untrusted-output\\n"\n'
        "  exit 128\n"
        "fi\n"
        'exec "$REAL_GIT" "$@"\n'
    )
    fake_git.chmod(0o755)
    extra = {
        "PATH": str(bin_dir) + os.pathsep + os.environ["PATH"],
        "REAL_GIT": real_git,
        "PEER_CWD": str(peer),
        "FAILED_QUERY": failed_query,
    }
    scan = subprocess.run(
        ["bash", str(ns.hooks_dir / "session-scan.sh"), "sess-a", str(ns.klon), "--strict"],
        env={**os.environ, **extra, "HOME": str(ns.home)},
        capture_output=True,
        text=True,
        check=False,
    )
    assert scan.returncode != 0, "strict scanning concealed uncertain peer ownership"
    result = _start(ns, extra=extra)
    assert result.returncode == 0, result.stderr
    assert not _wrote(ns), "uncertain peer ownership allowed reconciliation"
    assert "prime --hook-json" in _calls(ns)
    context = json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
    assert "PRIME-KONTEXT" in context and "Scan fehlgeschlagen" in context


def test_missing_jq_names_missing_tool(tmp_path: Path) -> None:
    ns = _project(tmp_path)
    result = _start(ns, extra={"PATH": _path_without_jq(tmp_path)})
    assert result.returncode == 0
    assert "jq fehlt" in result.stderr
    assert "Identität unvollständig" not in result.stderr
    assert not _wrote(ns)


def test_missing_python_names_missing_tool_before_scan(tmp_path: Path) -> None:
    ns = _project(tmp_path)
    bin_dir = Path(_path_without_jq(tmp_path))
    (bin_dir / "python3").unlink()
    jq = shutil.which("jq")
    assert jq is not None
    (bin_dir / "jq").symlink_to(jq)
    result = _start(ns, extra={"PATH": str(bin_dir)})
    # The watchdog for both scan and prime needs Python. Without it, the
    # eligibility diagnostic must name the dependency before trying the scan.
    assert result.returncode != 0
    assert "python3 fehlt" in result.stderr
    assert "Sitzungs-Scan fehlgeschlagen" not in result.stderr
    assert not _wrote(ns)


@pytest.mark.parametrize("broken", ["missing", "unreadable", "invalid", "entry-unreadable"])
def test_unreadable_registry_never_writes(tmp_path: Path, broken: str) -> None:
    ns = _project(tmp_path)
    registry = ns.home / ".claude" / "sessions"
    if broken == "missing":
        registry.rmdir()
    elif broken == "unreadable":
        registry.chmod(0o000)
    else:
        entry = registry / "123.json"
        entry.write_text("not JSON" if broken == "invalid" else "{}")
        if broken == "entry-unreadable":
            entry.chmod(0o000)
    try:
        result = _start(ns)
        assert result.returncode == 0, result.stderr
        assert not _wrote(ns), "an unreadable registry was trusted as empty"
        context = json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
        assert "PRIME-KONTEXT" in context and "Scan fehlgeschlagen" in context
    finally:
        if registry.exists():
            registry.chmod(0o700)


def test_timeout_stops_descendants_before_prime(tmp_path: Path) -> None:
    ns = _project(tmp_path)
    marker = tmp_path / "orphan-write"
    script = ns.klon / "scripts" / "close_merged_beads.py"
    script.write_text(
        "import subprocess, sys, time\n"
        f"subprocess.Popen([sys.executable, '-c', \"import time; from pathlib import Path; time.sleep(0.5); Path({str(marker)!r}).touch()\"])\n"
        "time.sleep(5)\n"
    )
    result = _start(ns, extra={"BEADS_START_RECONCILE_TIMEOUT": "0.1"})
    assert result.returncode == 0, result.stderr
    assert "abgebrochen" in result.stderr
    assert "prime --hook-json" in _calls(ns)
    time.sleep(0.6)
    assert not marker.exists(), "a descendant wrote after prime"


def test_prime_failure_preserves_reconciliation_diagnostic(tmp_path: Path) -> None:
    ns = _project(tmp_path, push_rc=1)
    stub = ns.klon / "tools" / "bd"
    stub.write_text(STUB.replace("  prime)", "  prime)\n    exit 9"))
    result = _start(ns)
    assert result.returncode == 1
    assert "prime --hook-json fehlgeschlagen" in result.stderr
    assert "Beads-Abgleich fehlgeschlagen" in result.stderr
    assert "publication failed" in result.stderr


def test_startup_budget_reaches_publication_before_prime(tmp_path: Path) -> None:
    ns = _project(tmp_path)
    # Keep the close bound above the one-second admission floor. The batch
    # must complete some closes before exhausting its budget and publishing.
    for i in range(14):
        _commit(ns.origin, f"complete item {i}\n\nCloses-Bead: coding-harness-item-{i}")
    ns.render.write_text(
        ns.render.read_text()
        + "".join(json.dumps({"id": f"coding-harness-item-{i}", "status": "open"}) + "\n" for i in range(14))
    )
    stub = ns.klon / "tools" / "bd"
    stub.write_text(
        STUB.replace("  close)", "  close)\n    sleep 0.2").replace(
            "    ;;\n  dolt)", '    printf "completed-close %s\\n" "$2" >>"${BEADS_STUB_LOG:?}"\n    ;;\n  dolt)'
        )
    )
    result = _start(
        ns,
        extra={
            "BEADS_START_RECONCILE_TIMEOUT": "3",
            "BEADS_START_BUDGET_RESERVE": "0.1",
            "CLOSE_MERGED_BD_TIMEOUT": "1.5",
        },
    )
    assert result.returncode == 0, result.stderr
    calls = _calls(ns)
    assert "dolt push" in calls, (calls, result.stderr)
    closes = [call.split()[1] for call in calls if call.startswith("close ")]
    completed = [call.split()[1] for call in calls if call.startswith("completed-close ")]
    assert 0 < len(completed) < 15, (calls, result.stderr)
    assert completed == closes, "every attempted close must finish before publication"
    assert all(calls.index(f"completed-close {bid}") < calls.index("dolt push") for bid in completed)
    assert calls.index("dolt push") < calls.index("prime --hook-json")
    assert "startup budget exhausted" in result.stderr
    assert "abgebrochen" not in result.stderr


@pytest.mark.parametrize("prime", ['{"hookSpecificOutput":[]}', '{"hookSpecificOutput":"context"}', "[]", '"context"'])
def test_note_fold_failure_preserves_prime(tmp_path: Path, prime: str) -> None:
    ns = _project(tmp_path)
    ns.prime.write_text(prime + "\n")
    result = _start(ns, extra={"CLAUDE_RECAP_CHILD": "1"})
    assert result.returncode == 0, result.stderr
    assert result.stdout == prime + "\n"
    assert "Prime-Kontext unverändert" in result.stderr
    assert not _wrote(ns)


def test_successful_command_keeps_background_work(tmp_path: Path) -> None:
    ns = _project(tmp_path)
    marker = tmp_path / "background-completed"
    script = ns.klon / "scripts" / "close_merged_beads.py"
    script.write_text(
        "import subprocess, sys\n"
        f"subprocess.Popen([sys.executable, '-c', \"import time; from pathlib import Path; time.sleep(0.4); Path({str(marker)!r}).touch()\"])\n"
    )
    result = _start(ns)
    assert result.returncode == 0, result.stderr
    assert "prime --hook-json" in _calls(ns)
    deadline = time.monotonic() + 3
    while not marker.exists() and time.monotonic() < deadline:
        time.sleep(0.05)
    assert marker.exists(), "the watchdog killed background work after successful completion"


def test_budget_bounds_are_scaled_through_the_environment() -> None:
    # The budget tests scale the production bounds through these variables, not
    # by patching a copy of the source, so a scaling that did not apply cannot
    # silently run the tests at production bounds.
    code = "import sys; sys.path.insert(0, sys.argv[1]); import close_merged_beads as m; print(m.BD_TIMEOUT)"
    env = {**os.environ, "CLOSE_MERGED_BD_TIMEOUT": "0.25"}
    result = subprocess.run(
        [sys.executable, "-c", code, str(REPO_ROOT / "scripts")], env=env, capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "0.25"
    assert "BEADS_START_BUDGET_RESERVE" in HOOK.read_text()
