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
