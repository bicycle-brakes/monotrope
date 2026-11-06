"""Offline regressions for the conflict-marker gate (bead coding-harness-i76l).

`scripts/check_conflict_markers.py` blocks merge-conflict markers in tracked
text and Git's own whitespace faults in staged and unstaged changes. Every test
builds a disposable real Git repository in a temporary directory, runs the gate
as a command, and pairs each planted fault with a passing control on the same
repository, so no marker-bearing file is ever committed here: the marker text is
assembled at run time and never begins a line of this file.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
GATE = REPO_ROOT / "scripts/check_conflict_markers.py"
KIT = REPO_ROOT / "scripts" / "kit"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(KIT))
import check_conflict_markers as gate_module  # noqa: E402
import ci_gates  # noqa: E402
import probe  # noqa: E402

LT = "<" * 7
EQ = "=" * 7
GT = ">" * 7


@pytest.fixture(autouse=True)
def isolated_git_config(monkeypatch: pytest.MonkeyPatch) -> None:
    """Disposable repositories must not inherit personal signing, hook or whitespace settings."""
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", os.devnull)


def _git(cwd: Path, *args: str) -> str:
    done = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, check=False)
    if done.returncode:
        raise AssertionError(f"git -C {cwd} {' '.join(args)} failed: {done.stderr}")
    return done.stdout


def make_repo(root: Path, files: dict[str, bytes | str]) -> Path:
    """A real repository with one commit holding `files`."""
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "--quiet")
    _git(root, "config", "user.email", "test@example.invalid")
    _git(root, "config", "user.name", "Test")
    for rel, body in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body if isinstance(body, bytes) else body.encode("utf-8"))
    _git(root, "add", "-A")
    _git(root, "commit", "--quiet", "-m", "base")
    return root


def run_gate(root: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    """Run the scanner as a command, the way the verification list does."""
    return subprocess.run(
        [sys.executable, str(GATE), "--root", str(root)],
        capture_output=True,
        text=True,
        env={**os.environ, **(env or {})},
        cwd=root if root.is_dir() else None,
        timeout=120,
        check=False,
    )


def _snapshot(root: Path) -> dict[str, object]:
    """Everything a read-only check must leave alone."""
    files = {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file() and ".git" not in path.relative_to(root).parts
    }
    return {
        "head": _git(root, "rev-parse", "HEAD"),
        "refs": _git(root, "for-each-ref"),
        "index": (root / ".git" / "index").read_bytes(),
        "status": _git(root, "status", "--porcelain"),
        "files": files,
    }


# ---------------------------------------------------------------------------
# Criterion 1 — markers already committed turn the gate red.
# ---------------------------------------------------------------------------

# (path, marker line, wrapper) — the marker prefix, its suffix, and where it stands.
MARKER_CASES = [
    pytest.param("src/mod.py", LT, "", "plain", id="open-bare"),
    pytest.param("src/mod.py", LT, " HEAD", "plain", id="open-label"),
    pytest.param("src/mod.py", LT + "<<", " longer", "plain", id="open-longer"),
    pytest.param("src/mod.py", EQ, "", "plain", id="mid-bare"),
    pytest.param("src/mod.py", EQ, " label", "plain", id="mid-label"),
    pytest.param("src/mod.py", EQ + "==", "", "plain", id="mid-longer"),
    pytest.param("src/mod.py", GT, "", "plain", id="close-bare"),
    pytest.param("src/mod.py", GT, " feature/branch", "plain", id="close-label"),
    pytest.param("src/mod.py", GT + ">>", "", "plain", id="close-longer"),
    pytest.param("docs/guide.md", LT, " HEAD", "fenced", id="fenced-example"),
    pytest.param("plans/changes/x/plan.md", EQ, "", "crlf", id="crlf-plan"),
    pytest.param("data/notes.txt", GT, " other", "latin1", id="non-utf8"),
]


def _body(marker: str, wrapper: str) -> bytes:
    if wrapper == "fenced":
        return f"# Title\n\n```\n{marker}\n```\n".encode()
    if wrapper == "crlf":
        return f"line one\r\n{marker}\r\nline three\r\n".encode()
    if wrapper == "latin1":
        return b"caf\xe9\n" + marker.encode("ascii") + b"\n"
    return f"first = 1\n{marker}\nlast = 2\n".encode()


@pytest.mark.parametrize(("rel", "prefix", "suffix", "wrapper"), MARKER_CASES)
def test_gate_goes_red_when_committed_text_contains_markers(
    tmp_path: Path, rel: str, prefix: str, suffix: str, wrapper: str
) -> None:
    clean = "first = 1\nlast = 2\n"
    root = make_repo(tmp_path / "repo", {rel: clean})
    control = run_gate(root)
    assert control.returncode == 0, control.stdout + control.stderr

    path = root / rel
    path.write_bytes(_body(prefix + suffix, wrapper))
    _git(root, "add", "-A")
    _git(root, "commit", "--quiet", "-m", "commit unresolved text")
    assert _git(root, "status", "--porcelain") == "", "the planted tree must be clean"

    done = run_gate(root)
    assert done.returncode == 2, done.stdout + done.stderr
    line = 4 if wrapper == "fenced" else 2
    assert f"{rel}:{line}:" in done.stdout, done.stdout


# ---------------------------------------------------------------------------
# Criterion 2 — every path and line is reported; nothing is written.
# ---------------------------------------------------------------------------


def test_reports_all_marker_locations_without_writes(tmp_path: Path) -> None:
    root = make_repo(
        tmp_path / "repo",
        {
            "a.txt": f"one\n{LT} HEAD\nthree\n{GT} other\n",
            "sub/b.md": f"{EQ}\nsecond file\n",
            "clean.txt": "nothing here\n",
        },
    )
    (root / "staged.txt").write_text("staged\n", encoding="utf-8")
    _git(root, "add", "staged.txt")
    _git(root, "status", "--porcelain")  # settle Git's own opportunistic index refresh first
    before = _snapshot(root)

    done = run_gate(root)

    assert done.returncode == 2, done.stdout + done.stderr
    for expected in ("a.txt:2:", "a.txt:4:", "sub/b.md:1:"):
        assert expected in done.stdout, f"{expected} missing from: {done.stdout}"
    assert "clean.txt:" not in done.stdout
    assert _snapshot(root) == before, "checking changed repository content, index or refs"


# ---------------------------------------------------------------------------
# Criterion 3 — only tracked text is measured, and fixtures only by exact name.
# ---------------------------------------------------------------------------


def test_only_tracked_text_and_exact_fixture_names_are_measured(tmp_path: Path) -> None:
    marker_text = f"{LT} HEAD\n{EQ}\n{GT} other\n"
    root = make_repo(
        tmp_path / "repo",
        {
            "fixtures/a.txt": "clean\n",
            "fixtures/a.txt.bak": "clean\n",
            "fixtures/a.txt2": "clean\n",
            "binary.bin": b"\0binary\n" + marker_text.encode(),
            "ok.md": "fine\n",
        },
    )
    outside = tmp_path / "outside.txt"
    outside.write_text(marker_text, encoding="utf-8")
    (root / "link.txt").symlink_to(outside)
    _git(root, "add", "link.txt")
    # A gitlink entry whose directory holds marker text: a submodule is never entered.
    head = _git(root, "rev-parse", "HEAD").strip()
    _git(root, "update-index", "--add", "--cacheinfo", f"160000,{head},vendor/sub")
    _git(root, "commit", "--quiet", "-m", "link and gitlink")
    (root / "vendor" / "sub").mkdir(parents=True)
    (root / "vendor" / "sub" / "x.txt").write_text(marker_text, encoding="utf-8")
    (root / "untracked.txt").write_text(marker_text, encoding="utf-8")
    (root / "ok.md").unlink()

    control = run_gate(root)
    report = control.stdout + control.stderr
    assert control.returncode == 0, f"binary, untracked, symlink, submodule or deleted path was measured: {report}"

    # Production exceptions start empty and no flag skips anything.
    assert frozenset() == gate_module.FIXTURE_EXCEPTIONS
    skip_flag = subprocess.run(
        [sys.executable, str(GATE), "--root", str(root), "--skip", "fixtures/a.txt"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert skip_flag.returncode != 0, "the gate accepted a skip flag"

    for rel in ("fixtures/a.txt", "fixtures/a.txt.bak", "fixtures/a.txt2"):
        (root / rel).write_text(marker_text, encoding="utf-8")
    _git(root, "add", "fixtures")
    _git(root, "commit", "--quiet", "-m", "markers in three fixtures")

    measured = gate_module.measure(root, frozenset({"fixtures/a.txt"}))
    assert sorted(measured.markers) == ["fixtures/a.txt.bak", "fixtures/a.txt2"], measured.markers
    assert not measured.errors

    exempt_all = gate_module.measure(root, frozenset({"fixtures/a.txt", "fixtures/a.txt.bak", "fixtures/a.txt2"}))
    assert exempt_all.markers == {}

    # The same exact list excludes a named fixture from the whitespace check, and only it.
    (root / "fixtures" / "a.txt").write_text("trailing   \n", encoding="utf-8")
    (root / "fixtures" / "a.txt2").write_text("trailing   \n", encoding="utf-8")
    named = gate_module.measure(root, frozenset({"fixtures/a.txt"}))
    assert len(named.diff_findings) == 1
    assert "a.txt2" in named.diff_findings[0][1] and "fixtures/a.txt:" not in named.diff_findings[0][1]
    both = gate_module.measure(root, frozenset({"fixtures/a.txt", "fixtures/a.txt2"}))
    assert both.diff_findings == []


# ---------------------------------------------------------------------------
# Criterion 4 — Git's whitespace check holds staged and unstaged changes.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("layer", ["unstaged", "staged", "staged-then-restored"])
def test_gate_goes_red_when_git_diff_check_finds_a_fault(tmp_path: Path, layer: str) -> None:
    root = make_repo(tmp_path / "repo", {"notes.txt": "clean line\n"})
    control = run_gate(root)
    assert control.returncode == 0, control.stdout + control.stderr

    faulty = "clean line   \n"
    path = root / "notes.txt"
    path.write_text(faulty, encoding="utf-8")
    if layer != "unstaged":
        _git(root, "add", "notes.txt")
    if layer == "staged-then-restored":
        path.write_text("clean line\n", encoding="utf-8")

    done = run_gate(root)
    assert done.returncode == 2, done.stdout + done.stderr
    assert "trailing whitespace" in done.stdout, done.stdout
    assert "notes.txt" in done.stdout


# ---------------------------------------------------------------------------
# Criterion 5 — what could not be measured is a failure, never a clean report.
# ---------------------------------------------------------------------------


def test_gate_goes_red_when_inspection_cannot_complete(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = make_repo(tmp_path / "repo", {"ok.txt": "fine\n"})
    control = run_gate(root)
    assert control.returncode == 0, control.stdout + control.stderr

    # Not a repository.
    plain = tmp_path / "plain"
    plain.mkdir()
    done = run_gate(plain)
    assert done.returncode == 2, done.stdout + done.stderr
    assert "not measured" in done.stdout

    # A root that does not exist.
    missing = run_gate(tmp_path / "absent")
    assert missing.returncode == 2, missing.stdout + missing.stderr

    # A Git command that fails.
    fake = tmp_path / "fakebin"
    fake.mkdir()
    (fake / "git").write_text("#!/bin/sh\nexit 3\n", encoding="utf-8")
    (fake / "git").chmod(0o755)
    failing = run_gate(root, {"PATH": f"{fake}{os.pathsep}{os.environ['PATH']}"})
    assert failing.returncode == 2, failing.stdout + failing.stderr
    assert "not measured" in failing.stdout

    # A tracked regular file that cannot be read.
    def refuse(_path: Path) -> bytes:
        raise PermissionError(13, "Permission denied")

    with monkeypatch.context() as patch:
        patch.setattr(gate_module, "_read_bytes", refuse)
        result = gate_module.measure(root)
    assert any("ok.txt" in error for error in result.errors), result.errors
    assert not result.clean

    if hasattr(os, "geteuid") and os.geteuid() != 0:
        locked = root / "ok.txt"
        locked.chmod(0)
        try:
            unreadable = run_gate(root)
        finally:
            locked.chmod(0o644)
        assert unreadable.returncode == 2, unreadable.stdout + unreadable.stderr
        assert "ok.txt" in unreadable.stdout


# ---------------------------------------------------------------------------
# Criterion 6 — the one gate list runs the check, blocking, in every path.
# ---------------------------------------------------------------------------

DECLARED_COMMAND = "python3 scripts/check_conflict_markers.py"


def test_gate_is_blocking_in_every_verification_path() -> None:
    declared = [g for g in ci_gates.gates() if g["id"] == "conflict-markers"]
    if not declared:
        pytest.skip("the held gate declaration is added by the orchestrator bootstrap (plan step 5)")
    (gate,) = declared
    assert gate["command"] == DECLARED_COMMAND
    assert gate["job"] == "verify"
    assert gate["enforcement"] == "block"
    assert gate["placement"] == "both"
    assert gate["floor"] is False
    assert "docs" in gate["subsets"]
    assert ci_gates.misst_in(gate, "lokal") and ci_gates.misst_in(gate, "ci")
    assert ci_gates.in_job(gate, "verify") and ci_gates.in_job(gate, "docs")

    expected = f"conflict-markers\tblock\t{DECLARED_COMMAND}"
    for job in ("verify", "docs"):
        for placement in ("lokal", "ci"):
            listed = subprocess.run(
                [
                    sys.executable,
                    str(REPO_ROOT / "scripts" / "ci_gates.py"),
                    "--commands",
                    "--tsv",
                    "--job",
                    job,
                    "--placement",
                    placement,
                ],
                capture_output=True,
                text=True,
                cwd=REPO_ROOT,
                check=False,
            )
            assert listed.returncode == 0, listed.stderr
            assert expected in listed.stdout.splitlines(), f"{job}/{placement} omits or alters the gate"

    workflow = ci_gates.generate_ci().splitlines()
    start = workflow.index("        id: conflict-markers")
    step: list[str] = []
    for line in workflow[start:]:
        if line.startswith("      - name:"):
            break
        step.append(line)
    assert f"        run: {DECLARED_COMMAND}" in step
    assert not any("continue-on-error" in line for line in step), "the hosted step is advisory"


# ---------------------------------------------------------------------------
# Criterion 8 — the gate and its tests travel with the gate machinery.
# ---------------------------------------------------------------------------


def test_gate_and_tests_travel_with_the_kit() -> None:
    manifest = yaml.safe_load((KIT / "manifest.yaml").read_text(encoding="utf-8"))
    prefixes = {rule["prefix"] for rule in manifest["rules"]}
    for rel in ("scripts/check_conflict_markers.py", "tests/test_check_conflict_markers.py"):
        assert rel in prefixes, f"{rel} has no rule of its own in scripts/kit/manifest.yaml"
        assert probe.rolle(rel) == ("mechanismus", rel)
        assert (REPO_ROOT / rel).is_file()
    # The gate declaration travels as mechanism; where it names this script, the script is present.
    assert probe.rolle("decisions/gates.yaml") is not None
    assert probe.rolle("decisions/gates.yaml")[0] == "mechanismus"
