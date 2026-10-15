"""tests/test_stage2_attempt.py — the supervisor of one isolated writing attempt (ADR 0018).

Each test drives `scripts/stage2_attempt.py` through its real seams: the pure
validators, the recorded stand-in transport, and the journal. The suite never
starts a real container; the live probes of `scripts/check_stage2_isolation.py`
measure the production adapters.
"""

from __future__ import annotations

import io
import json
import subprocess
import sys
import tarfile
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import stage2_attempt  # noqa: E402

# ---------------------------------------------------------------------------
# Fixtures and helpers
# ---------------------------------------------------------------------------


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A small repository with one baseline commit."""
    root = tmp_path / "tree"
    root.mkdir()
    _git(root, "init", "-q")
    _git(root, "config", "user.name", "test")
    _git(root, "config", "user.email", "test@invalid")
    _git(root, "config", "commit.gpgsign", "false")
    (root / "docs").mkdir()
    (root / "docs" / "readme.md").write_text("one\n", encoding="utf-8")
    (root / "keep.txt").write_text("untouched\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "baseline")
    return root


@pytest.fixture
def baseline(repo: Path) -> str:
    done = _git(repo, "rev-parse", "HEAD")
    assert done.returncode == 0
    return done.stdout.decode().strip()


@pytest.fixture
def state_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    named = tmp_path / "state"
    monkeypatch.setenv("STAGE2_STATE_DIR", str(named))
    return named


@pytest.fixture
def stand_in(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    named = tmp_path / "runtime"
    monkeypatch.setenv("STAGE2_RUNTIME_STAND_IN", str(named))
    return named


@pytest.fixture
def secrets(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    named = tmp_path / "secrets.env"
    named.write_text("GLM_KEY=glm-secret-123\n", encoding="utf-8")
    monkeypatch.setenv("CC_SECRETS", str(named))
    return named


@pytest.fixture(autouse=True)
def denylist(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A hermetic leak denylist: no test reads the maintainer's own list."""
    named = tmp_path / "denylist.txt"
    named.write_text("test-secret=stage2-test-secret\n", encoding="utf-8")
    monkeypatch.setenv("LEAKCHECK_DENYLIST", str(named))
    return named


def _tar(files: dict[str, bytes], extra: list[tuple[tarfile.TarInfo, bytes]] | None = None) -> bytes:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w") as target:
        for name, data in files.items():
            info = tarfile.TarInfo(name=name)
            info.size = len(data)
            target.addfile(info, io.BytesIO(data))
        for info, data in extra or []:
            target.addfile(info, io.BytesIO(data))
    return buffer.getvalue()


def _log_entries(stand_in_dir: Path) -> list[dict]:
    log = stand_in_dir / "runtime-calls.jsonl"
    if not log.exists():
        return []
    return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]


def _fake_cli_command() -> list[str]:
    return [
        sys.executable,
        "-c",
        "import sys, pathlib; pathlib.Path(sys.argv[1]).write_bytes(b'answer bytes'); print('model says hi')",
        stage2_attempt.ANSWER_PLACEHOLDER,
    ]


def _launch(
    repo: Path,
    baseline: str,
    *,
    command: list[str] | None = None,
    endpoint: str = "glm-coding-plan",
    inner_env: dict[str, str] | None = None,
) -> stage2_attempt.WriterRun:
    return stage2_attempt.launch_writer_call(
        root=repo,
        spec=stage2_attempt.WriterSpec(
            verb="implement",
            change="isolated-attempts",
            endpoint=endpoint,
            model="glm-5.3-flash",
            prompt="Write the phase.",
            inner_command=command or _fake_cli_command(),
            inner_env=inner_env if inner_env is not None else {"PATH": "/usr/bin:/bin"},
            baseline=baseline,
        ),
    )


def _measured_lock(tmp_path: Path, *, programs: list[str] | None = None) -> Path:
    lock = {
        "images": {
            "model": {"reference": "localhost/x-model", "digest": "sha256:" + "a" * 8, "measured": True},
            "verifier": {"reference": "localhost/x-verifier", "digest": "sha256:" + "b" * 8, "measured": True},
        },
        "boundary": {
            "programs": programs or ["podman", "docker", "container"],
            "require": [
                "non-root-user",
                "read-only-rootfs",
                "cap-drop-all",
                "private-candidate-volume",
                "api-only-egress",
            ],
        },
    }
    named = tmp_path / "measured.lock.yaml"
    named.write_text(yaml.safe_dump(lock), encoding="utf-8")
    return named


@pytest.fixture
def fake_podman(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A container program that records its own start and exits cleanly."""
    marker = tmp_path / "podman-ran"
    executable = tmp_path / "bin" / "podman"
    executable.parent.mkdir(parents=True, exist_ok=True)
    executable.write_text(f"#!/bin/sh\ntouch '{marker}'\nexit 0\n", encoding="utf-8")
    executable.chmod(0o755)
    monkeypatch.setenv("STAGE2_CONTAINER_PROGRAM", str(executable))
    marker.touch()  # the fixture proof: the test deletes it and expects it to stay absent
    marker.unlink()
    return marker


# ---------------------------------------------------------------------------
# The one selected login (criterion 4)
# ---------------------------------------------------------------------------


def test_only_the_selected_login_is_passed(
    repo: Path,
    baseline: str,
    state_dir: Path,
    stand_in: Path,
    secrets: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A launch carries exactly the selected endpoint's login — never another token."""
    monkeypatch.setenv("OPENAI_API_KEY", "intruder-token")
    monkeypatch.setenv("SSH_AUTH_SOCK", "/tmp/agent-sock")
    login = stage2_attempt.selected_login("glm-coding-plan", lambda name: {"GLM_KEY": "glm-secret-123"}.get(name))
    assert login.env_pairs == {"ANTHROPIC_AUTH_TOKEN": "glm-secret-123", "ANTHROPIC_API_KEY": "glm-secret-123"}
    assert login.file is None
    run = _launch(repo, baseline)
    assert run.done.returncode == 0
    entries = [entry for entry in _log_entries(stand_in) if entry.get("op") == "run"]
    assert len(entries) == 1
    passed = entries[0]["env"]
    assert passed["ANTHROPIC_AUTH_TOKEN"] == "glm-secret-123"
    assert "OPENAI_API_KEY" not in passed, "another provider's token must never reach the call"
    assert "SSH_AUTH_SOCK" not in passed, "an agent socket must never reach the call"
    assert passed["PATH"] == "/usr/bin:/bin"


def test_the_selected_login_refuses_what_is_missing_or_unknown(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A missing login or an unknown endpoint refuses before any call starts."""
    with pytest.raises(stage2_attempt.BoundaryRefused):
        stage2_attempt.selected_login("glm-coding-plan", lambda name: None)
    with pytest.raises(stage2_attempt.BoundaryRefused):
        stage2_attempt.selected_login("unknown-endpoint", lambda name: "x")
    monkeypatch.setitem(stage2_attempt.LOGIN_FILES, "openai-codex", str(tmp_path / "auth.json"))
    with pytest.raises(stage2_attempt.BoundaryRefused):
        stage2_attempt.selected_login("openai-codex", lambda name: None)
    (tmp_path / "auth.json").write_text("{}\n", encoding="utf-8")
    login = stage2_attempt.selected_login("openai-codex", lambda name: None)
    assert login.file == tmp_path / "auth.json"
    assert login.env_pairs == {}, "a file login is the one secret input, not environment variables"


# ---------------------------------------------------------------------------
# The container program and the boundary it must express (criterion 6)
# ---------------------------------------------------------------------------


def test_backend_selection_preserves_required_capabilities(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Every supported backend receives the same confinement; an unknown name refuses."""
    assert stage2_attempt.program_problem("podman") is None
    assert stage2_attempt.program_problem("docker") is None
    assert stage2_attempt.program_problem("container") is None
    assert stage2_attempt.program_problem("/opt/homebrew/bin/podman") is None
    assert stage2_attempt.program_problem("orbstack") is not None
    monkeypatch.setenv("STAGE2_CONTAINER_PROGRAM", str(tmp_path / "no-such-dir" / "podman"))
    monkeypatch.delenv("STAGE2_RUNTIME_STAND_IN", raising=False)
    with pytest.raises(stage2_attempt.BoundaryRefused):
        stage2_attempt.selected_program()
    request = stage2_attempt.RunRequest(
        image="img", argv=["claude"], env={}, volumes=[("vol", "/work", False)], networks=[]
    )
    lock = {"boundary": {"require": ["read-only-rootfs"]}}
    podman = stage2_attempt.PodmanRuntime("podman").run_argv(request, lock)
    for flag in ("--user", "1000:1000", "--cap-drop", "ALL", "--read-only", "--network", "none", "-v", "vol:/work"):
        assert flag in podman, f"the Podman adapter must request {flag}"
    docker = stage2_attempt.DockerRuntime("docker").run_argv(request, lock)
    for flag in ("--cap-drop", "ALL", "--read-only", "--network", "none"):
        assert flag in docker, f"the Docker adapter must request {flag}"
    apple = stage2_attempt.AppleContainerRuntime("container").run_argv(request, lock)
    assert "--cap-drop" in apple and "ALL" in apple
    with pytest.raises(stage2_attempt.BoundaryRefused):
        stage2_attempt.AppleContainerRuntime("container").populate(
            stage2_attempt.InvocationState(id="x", verb="v", endpoint="e", model="m", baseline="b"), "vol", b""
        )
    weak = {"boundary": {"programs": ["podman"], "require": ["non-root-user"]}}
    assert stage2_attempt.lock_problem(weak, "podman") is not None, "a weaker lock is a refusal, not a grant"
    assert stage2_attempt.lock_problem(weak, "docker") is not None


# ---------------------------------------------------------------------------
# Refusal before launch (criterion 7)
# ---------------------------------------------------------------------------


def test_missing_boundary_prerequisites_never_launch_a_writer(
    repo: Path,
    baseline: str,
    state_dir: Path,
    fake_podman: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A missing runtime, image, profile or login refuses; nothing is launched, not even Stage 1."""
    monkeypatch.delenv("STAGE2_RUNTIME_STAND_IN", raising=False)
    unmeasured = tmp_path / "unmeasured.lock.yaml"
    unmeasured.write_text("images:\n  model: {measured: false}\n", encoding="utf-8")
    monkeypatch.setenv("STAGE2_RUNTIME_LOCK", str(unmeasured))
    with pytest.raises(stage2_attempt.BoundaryRefused):
        _launch(repo, baseline)
    assert not fake_podman.exists(), "an unmeasured image must not launch any container program call"

    monkeypatch.setenv("STAGE2_RUNTIME_LOCK", str(_measured_lock(tmp_path)))
    with pytest.raises(stage2_attempt.BoundaryRefused):  # openai-codex declares api_hosts: []
        _launch(repo, baseline, endpoint="openai-codex")
    assert not fake_podman.exists(), "an unqualified API profile must not launch a writer"

    empty_secrets = tmp_path / "empty-secrets.env"
    empty_secrets.write_text("# nothing\n", encoding="utf-8")
    monkeypatch.setenv("CC_SECRETS", str(empty_secrets))
    with pytest.raises(stage2_attempt.BoundaryRefused):
        _launch(repo, baseline, endpoint="glm-coding-plan")
    assert not fake_podman.exists(), "a missing login must not launch a writer"

    monkeypatch.setenv("STAGE2_CONTAINER_PROGRAM", "orbstack")
    with pytest.raises(stage2_attempt.BoundaryRefused):
        _launch(repo, baseline)
    assert not fake_podman.exists(), "an unknown backend must not be substituted"


# ---------------------------------------------------------------------------
# Export, topology, publication (criteria 11, 14)
# ---------------------------------------------------------------------------


def test_publication_rejects_untrusted_topology(tmp_path: Path) -> None:
    """Traversal, absolute paths, links, special files and topology swaps are refused."""
    cases = [
        ({"docs/a.md": b"a\n"}, {"../escape.txt": b"x"}, "an escaping path does not publish"),
        ({"docs/a.md": b"a\n"}, {"/etc/passwd": b"x"}, "an escaping path does not publish"),
        ({"p/x.txt": b"in dir\n"}, {"p": b"file"}, "a file replacing a directory does not publish"),
        ({"p": b"plain file\n"}, {"p/x.txt": b"x"}, "a directory replacing a file does not publish"),
    ]
    for baseline_files, additions, expected in cases:
        extra = []
        for name, data in additions.items():
            info = tarfile.TarInfo(name=name)
            info.size = len(data)
            extra.append((info, data))
        delta = stage2_attempt.diff_candidate(_tar(baseline_files), _tar({**baseline_files, **additions}))
        _ = extra
        assert any(expected in problem for problem in delta.problems), (expected, delta.problems)

    link = tarfile.TarInfo(name="docs/link.md")
    link.type = tarfile.SYMTYPE
    link.linkname = "/etc/passwd"
    baseline = _tar({"docs/a.md": b"a\n"})
    delta = stage2_attempt.diff_candidate(baseline, _tar({"docs/a.md": b"a\n"}, [link]))
    assert any("a link or special file does not publish" in problem for problem in delta.problems)

    delta = stage2_attempt.diff_candidate(baseline, _tar({"docs/a.md": b"\x00\x01binary"}))
    assert any("content is not a regular file's" in problem for problem in delta.problems)

    twice = io.BytesIO()
    with tarfile.open(fileobj=twice, mode="w") as target:
        for data in (b"one\n", b"two\n"):
            info = tarfile.TarInfo(name="docs/a.md")
            info.size = len(data)
            target.addfile(info, io.BytesIO(data))
    delta = stage2_attempt.diff_candidate(_tar({}), twice.getvalue())
    assert any("a duplicate path does not publish" in problem for problem in delta.problems)

    root = tmp_path / "host"
    root.mkdir()
    state = stage2_attempt.InvocationState(id="pub", verb="v", endpoint="e", model="m", baseline="b")
    bad = stage2_attempt.CandidateDelta(
        entries=[stage2_attempt.DeltaEntry(path=Path("../escape.txt"), data=b"x")], problems=["escaped"]
    )
    with pytest.raises(stage2_attempt.BoundaryRefused):
        stage2_attempt.publish_delta(bad, root, state)
    assert list(root.iterdir()) == [], "a refused publication must not touch the host"


def test_safe_nested_file_changes_can_be_published(repo: Path, tmp_path: Path, state_dir: Path) -> None:
    """New directories, new files, edits and explicit deletions publish; twice is stable."""
    baseline_archive = stage2_attempt.worktree_tar(repo, _git(repo, "rev-parse", "HEAD").stdout.decode().strip())
    candidate_files = {
        "docs/readme.md": b"one\n",
        "docs/new/deep/file.md": b"nested\n",
    }
    candidate_archive = _tar(candidate_files)
    delta = stage2_attempt.diff_candidate(baseline_archive, candidate_archive)
    assert delta.problems == [], delta.problems
    paths = {entry.path.as_posix() for entry in delta.entries}
    assert paths == {"docs/new/deep/file.md", "keep.txt"}, paths
    published = tmp_path / "host"
    published.mkdir()
    state = stage2_attempt.InvocationState(id="safe", verb="v", endpoint="e", model="m", baseline="b")
    applied = stage2_attempt.publish_delta(delta, published, state)
    assert (published / "docs" / "new" / "deep" / "file.md").read_bytes() == b"nested\n"
    assert [entry.path.as_posix() for entry in applied if entry.data is None] == ["keep.txt"]
    assert not (published / "keep.txt").exists()
    again = stage2_attempt.diff_candidate(candidate_archive, candidate_archive)
    assert again.entries == [], "an unchanged candidate produces no second publication"


def test_publication_requires_the_exact_clean_verified_bytes(tmp_path: Path, state_dir: Path) -> None:
    """Unscanned bytes never land; what lands is exactly the validated bytes."""
    root = tmp_path / "host"
    root.mkdir()
    delta = stage2_attempt.CandidateDelta(
        entries=[stage2_attempt.DeltaEntry(path=Path("plans/note.md"), data=b"hello\n")]
    )
    state = stage2_attempt.InvocationState(id="scan", verb="v", endpoint="e", model="m", baseline="b")

    def finding(path: Path, data: bytes) -> list[str]:
        return ["the selected token appears"] if b"hello" in data else []

    with pytest.raises(stage2_attempt.BoundaryRefused):
        stage2_attempt.publish_delta(delta, root, state, scan=finding)
    assert list(root.iterdir()) == [], "a blocked scan must leave the host untouched"

    applied = stage2_attempt.publish_delta(delta, root, state, scan=lambda path, data: [])
    assert applied[0].written == b"hello\n"
    assert (root / "plans" / "note.md").read_bytes() == applied[0].written
    assert state.journal[0]["path"] == "plans/note.md"


# ---------------------------------------------------------------------------
# The invocation lock and the journal's undo (criteria 15, 16)
# ---------------------------------------------------------------------------


def test_publication_preserves_intervening_host_work(repo: Path, baseline: str) -> None:
    """A host change between launch and publication refuses; the undo skips changed files."""
    before = stage2_attempt.host_state(repo)
    (repo / "keep.txt").write_text("concurrent edit\n", encoding="utf-8")
    with pytest.raises(stage2_attempt.BoundaryRefused):
        stage2_attempt.assert_host_state(repo, before)

    (repo / "keep.txt").write_text("untouched\n", encoding="utf-8")
    state = stage2_attempt.InvocationState(id="lock", verb="v", endpoint="e", model="m", baseline=baseline)
    delta = stage2_attempt.CandidateDelta(
        entries=[stage2_attempt.DeltaEntry(path=Path("keep.txt"), data=b"published\n")]
    )
    applied = stage2_attempt.publish_delta(delta, repo, state)
    assert (repo / "keep.txt").read_bytes() == b"published\n"
    (repo / "keep.txt").write_text("foreign\n", encoding="utf-8")
    undone = stage2_attempt.undo_owned(repo, applied, baseline)
    assert undone == "", "an intervening change is not ours to undo"
    assert (repo / "keep.txt").read_bytes() == b"foreign\n"


def test_publication_failure_undoes_only_owned_writes(repo: Path, baseline: str) -> None:
    """A failed publication restores exactly its own writes — no foreign file, no ref, no commit."""
    head_before = _git(repo, "rev-parse", "HEAD").stdout.decode().strip()
    refs_before = _git(repo, "for-each-ref").stdout
    state = stage2_attempt.InvocationState(id="undo", verb="v", endpoint="e", model="m", baseline=baseline)
    delta = stage2_attempt.CandidateDelta(
        entries=[
            stage2_attempt.DeltaEntry(path=Path("keep.txt"), data=b"published\n"),
            stage2_attempt.DeltaEntry(path=Path("new/owned.md"), data=b"owned\n"),
            stage2_attempt.DeltaEntry(path=Path("docs/other.md"), data=b"not mine\n"),
        ]
    )
    (repo / "docs" / "other.md").write_text("another writer's file\n", encoding="utf-8")
    applied = stage2_attempt.publish_delta(delta, repo, state)
    assert (repo / "new" / "owned.md").exists()
    stage2_attempt.undo_owned(repo, applied, baseline)
    assert (repo / "keep.txt").read_bytes() == b"untouched\n"
    assert not (repo / "new" / "owned.md").exists(), "an owned created file is removed"
    assert not (repo / "new").exists(), "an owned empty directory is pruned"
    assert (repo / "docs" / "other.md").read_bytes() == b"another writer's file\n"
    assert _git(repo, "rev-parse", "HEAD").stdout.decode().strip() == head_before
    assert _git(repo, "for-each-ref").stdout == refs_before, "no ref is rewritten"


# ---------------------------------------------------------------------------
# Cleanup and recovery (criterion 22)
# ---------------------------------------------------------------------------


def test_recovery_cleans_only_recorded_owned_resources(tmp_path: Path, state_dir: Path, stand_in: Path) -> None:
    """Recovery removes exactly the resources a failed invocation recorded — never a foreign one."""
    runtime = stage2_attempt.StandInRuntime(stand_in)
    healthy = stage2_attempt.InvocationState(id="aaaa1111aaaa", verb="v", endpoint="e", model="m", baseline="b")
    healthy.resources = [{"kind": "volume", "name": "owned-vol", "invocation": healthy.id}]
    healthy.save()

    foreign = stage2_attempt.InvocationState(id="bbbb2222bbbb", verb="v", endpoint="e", model="m", baseline="b")
    foreign.cleanup_pending = "resources remain: foreign-vol"
    foreign.resources = [
        {"kind": "volume", "name": "foreign-vol", "invocation": foreign.id},
        {"kind": "volume", "name": "spoofed-vol", "invocation": "not-the-owner"},
    ]
    foreign.save()

    still = stage2_attempt.reconcile_pending(runtime)
    assert still == []
    removed = [entry for entry in _log_entries(stand_in) if entry["op"] == "remove"]
    assert len(removed) == 1
    names = {entry["name"] for entry in removed[0]["resources"]}
    assert names == {"foreign-vol"}, "only the recorded, matching owner's resources are removed"
    assert "spoofed-vol" not in names, "a resource naming another owner is never touched"
    assert "owned-vol" not in names, "a state without pending cleanup is not another invocation's business"
    assert not foreign.path.exists()
    assert healthy.path.exists()

    leftover = stage2_attempt.InvocationState(id="cccc3333cccc", verb="v", endpoint="e", model="m", baseline="b")
    leftover.resources = [{"kind": "volume", "name": "stuck-vol", "invocation": leftover.id}]
    leftover.save()

    class Stuck(stage2_attempt.StandInRuntime):
        def remove_resources(self, resources):  # noqa: ARG002
            return [entry["name"] for entry in resources]

    assert stage2_attempt.cleanup_state(leftover, Stuck(stand_in)) is False
    reloaded = stage2_attempt.InvocationState.load(leftover.id)
    assert reloaded.cleanup_pending == "resources remain: stuck-vol", "an unfinished cleanup stays visible"


# ---------------------------------------------------------------------------
# Fresh state per attempt (supports criterion 1, proven in tests/test_stage2.py)
# ---------------------------------------------------------------------------


def test_each_attempt_gets_its_own_recorded_state(
    repo: Path, baseline: str, state_dir: Path, stand_in: Path, secrets: Path
) -> None:
    """Two attempts never share a volume name or an invocation identity."""
    first = _launch(repo, baseline)
    second = _launch(repo, baseline)
    assert first.state.id != second.state.id
    creates = [entry for entry in _log_entries(stand_in) if entry["op"] == "volume create"]
    names = [entry["name"] for entry in creates]
    assert len(names) == 2 and len(set(names)) == 2, "each attempt must create its own candidate volume"
    runs = [entry for entry in _log_entries(stand_in) if entry["op"] == "run"]
    assert len(runs) == 2
    first_volumes = [volume[0] for volume in runs[0]["volumes"]]
    second_volumes = [volume[0] for volume in runs[1]["volumes"]]
    assert not set(first_volumes) & set(second_volumes), "no writable volume is reused between attempts"
    assert first.answer_path is not None and first.answer_path.read_bytes() == b"answer bytes"
