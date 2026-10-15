"""tests/test_stage2_isolation.py — the boundary checker and its probe program (ADR 0018).

**What this file measures.** Two things, and it keeps them apart:

* *Always:* the checker's own logic — the probe program's task outcomes, the
  report assembly that demands every named probe (criterion 23), the
  fingerprint cache, and the refusal path that fails instead of skipping.
  Every criterion test plants the fault it guards against and watches the
  checker catch it, then runs the clean case and watches it pass.
* *Only under `STAGE2_ISOLATION_LIVE=1`:* the real sections of
  `scripts/check_stage2_isolation.py` — production launches against the real
  backend. An opted-in live run without prerequisites FAILS here; it never
  skips. The normal suite stays on the hermetic branch: the actual macOS and
  Linux reports are separate completion evidence (criterion 23), not these
  tests.
"""

from __future__ import annotations

import json
import os
import socket
import sys
import tempfile
import threading
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import check_stage2_isolation as checker  # noqa: E402
import stage2_attempt  # noqa: E402

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _identity() -> dict:
    return {
        "schema": checker.REPORT_SCHEMA,
        "commit": "0" * 40,
        "platform": {"system": "test", "release": "1", "machine": "x"},
        "program": {"name": "podman", "version": "test"},
        "images": {"model": {"reference": "r", "digest": "d", "measured": True}},
        "policy_hash": "p" * 64,
        "endpoint": checker.PROBE_ENDPOINT,
        "api_hosts": ["api.z.ai"],
    }


def _section_problems(section: str, found: dict[str, tuple[bool, str]]) -> list[str]:
    """Assemble one section into a report and return the problems it names."""
    _report, problems = checker.build_report({section: found}, _identity())
    return problems


def _bound_listener() -> tuple[int, socket.socket]:
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    sock.listen(8)
    return sock.getsockname()[1], sock


class _ConnectProxy:
    """A local CONNECT endpoint that answers every request with one status."""

    def __init__(self, status: bytes) -> None:
        self._status = status
        self._server = socket.socket()
        self._server.bind(("127.0.0.1", 0))
        self._server.listen(8)
        self.port = self._server.getsockname()[1]
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._serve, daemon=True)

    def _serve(self) -> None:
        self._server.settimeout(0.2)
        while not self._stop.is_set():
            try:
                conn, _ = self._server.accept()
            except (TimeoutError, OSError):
                continue
            try:
                conn.recv(4096)
                conn.sendall(self._status)
            except OSError:
                pass
            finally:
                conn.close()

    def __enter__(self) -> _ConnectProxy:
        self._thread.start()
        return self

    def __exit__(self, *_exc: object) -> None:
        self._stop.set()
        self._thread.join(timeout=2)
        self._server.close()


def _live_run(section: str) -> None:
    """The opted-in live branch: run the real section, refusing to skip."""
    problems = checker.prerequisite_problems(REPO_ROOT, None, False)
    assert not problems, (
        "STAGE2_ISOLATION_LIVE=1 was requested but the boundary is not measurable - "
        "live probes fail, they never skip: " + "; ".join(problems)
    )
    with tempfile.TemporaryDirectory(prefix="stage2-live-") as tmp:
        workdir = Path(tmp)
        sentinel = workdir / "sentinel.txt"
        sentinel.write_text("host sentinel (ADR 0018)", encoding="utf-8")
        secrets = checker.synthetic_secrets(workdir)
        if section == "egress":
            declared = stage2_attempt.api_hosts(REPO_ROOT, checker.PROBE_ENDPOINT)[0]
            found = checker.section_egress(REPO_ROOT, sentinel, secrets, declared)
        elif section == "retry":
            found = checker.section_retry(REPO_ROOT, sentinel, secrets)
        else:
            found = {
                "host-files": checker.section_host_files,
                "host-writes": checker.section_host_writes,
                "credentials": checker.section_credentials,
                "verifier": checker.section_verifier,
                "cleanup": checker.section_cleanup,
            }[section](REPO_ROOT, sentinel, secrets)
    problems = _section_problems(section, found)
    assert not problems, f"the live boundary leaked: {problems}"


def _live_or(section: str, hermetic) -> None:  # type: ignore[no-untyped-def]
    if os.environ.get("STAGE2_ISOLATION_LIVE") == "1":
        _live_run(section)
        return
    hermetic()


# ---------------------------------------------------------------------------
# Criterion 2 — host files are unreadable through file tools and shell
# ---------------------------------------------------------------------------


def test_live_host_files_are_unreadable(tmp_path: Path) -> None:
    """A sentinel in the host home/worktree must stay unreadable inside an attempt."""

    def hermetic() -> None:
        sentinel = tmp_path / "sentinel.txt"
        sentinel.write_text("host secret\n", encoding="utf-8")
        # The planted fault: the probe runs where the sentinels exist, exactly
        # as a broken mount namespace would allow - the checker must flag it.
        leaked = checker.run_probe_program([f"read {sentinel}", f"shell-read {sentinel}"], cwd=tmp_path)
        assert leaked[f"read {sentinel}"][0] is False
        assert leaked[f"shell-read {sentinel}"][0] is False
        found = {
            "read sentinel": leaked[f"read {sentinel}"],
            "shell-read sentinel": leaked[f"shell-read {sentinel}"],
            "read worktree file": (False, "read 12 bytes"),
            "read git metadata": (False, "read 4 bytes"),
            "read host secrets file": (False, "read 9 bytes"),
        }
        problems = _section_problems("host-files", found)
        assert any("read sentinel" in problem for problem in problems)
        assert any("shell-read sentinel" in problem for problem in problems)
        # The clean case: nothing the container would see exists to read.
        gone = tmp_path / "absent" / "sentinel.txt"
        clean = checker.run_probe_program([f"read {gone}", f"shell-read {gone}"], cwd=tmp_path)
        assert clean[f"read {gone}"][0] is True
        assert clean[f"shell-read {gone}"][0] is True

    _live_or("host-files", hermetic)


# ---------------------------------------------------------------------------
# Criterion 3 — host state cannot be altered from inside an attempt
# ---------------------------------------------------------------------------


def test_live_attempt_cannot_write_host_state(tmp_path: Path) -> None:
    """A write attempt against host paths must fail inside the boundary."""

    def hermetic() -> None:
        target = tmp_path / "worktree-file.txt"
        target.write_text("host state\n", encoding="utf-8")
        # The planted fault: on the host the write succeeds - exactly what a
        # leaked mount would allow - and the checker must call it a leak.
        wrote = checker.run_probe_program([f"write {target}"], cwd=tmp_path)
        assert wrote[f"write {target}"][0] is False
        found = {
            "write sentinel": (False, "opened for writing"),
            "write worktree file": wrote[f"write {target}"],
            "write git HEAD": (False, "opened for writing"),
            "write git hook": (False, "opened for writing"),
        }
        problems = _section_problems("host-writes", found)
        assert any("write worktree file" in problem for problem in problems)
        # The clean case: a read-only directory refuses the write.
        readonly = tmp_path / "readonly"
        readonly.mkdir()
        readonly.chmod(0o500)
        try:
            refused = checker.run_probe_program([f"write {readonly / 'file'}"], cwd=tmp_path)
            assert refused[f"write {readonly / 'file'}"][0] is True
        finally:
            readonly.chmod(0o700)

    _live_or("host-writes", hermetic)


# ---------------------------------------------------------------------------
# Criterion 4 — only the selected endpoint's login is visible
# ---------------------------------------------------------------------------


def test_live_attempt_sees_only_selected_credentials(tmp_path: Path) -> None:
    """An unrelated credential value in the environment must be reported; the selected one must travel."""

    def hermetic() -> None:
        path = os.environ.get("PATH", "/usr/bin:/bin")
        # The planted fault: the unrelated value and the agent socket travel -
        # exactly what a whole-home mount would do - and must be reported.
        leaked = checker.run_probe_program(
            [
                f"env-value-present {checker.SELECTED_VALUE}",
                f"env-value-missing {checker.UNRELATED_VALUE}",
                "env-missing SSH_AUTH_SOCK",
                "env-missing GPG_AGENT_INFO",
            ],
            cwd=tmp_path,
            env={
                "PATH": path,
                "GLM_KEY": checker.SELECTED_VALUE,
                "UNRELATED_PROBE_KEY": checker.UNRELATED_VALUE,
                "SSH_AUTH_SOCK": "/tmp/agent.sock",
            },
        )
        assert leaked[f"env-value-present {checker.SELECTED_VALUE}"][0] is True
        assert leaked[f"env-value-missing {checker.UNRELATED_VALUE}"][0] is False
        assert leaked["env-missing SSH_AUTH_SOCK"][0] is False
        found = {
            "selected credential travels": leaked[f"env-value-present {checker.SELECTED_VALUE}"],
            "unrelated credential absent": leaked[f"env-value-missing {checker.UNRELATED_VALUE}"],
            "no agent socket variable": leaked["env-missing SSH_AUTH_SOCK"],
            "no gpg agent variable": leaked["env-missing GPG_AGENT_INFO"],
            "host secrets file unreadable": (True, "FileNotFoundError"),
        }
        problems = _section_problems("credentials", found)
        assert any("unrelated credential absent" in problem for problem in problems)
        assert any("no agent socket variable" in problem for problem in problems)
        assert not any("selected credential travels" in problem for problem in problems)
        # The clean case: only the selected value travels.
        clean = checker.run_probe_program(
            [
                f"env-value-present {checker.SELECTED_VALUE}",
                f"env-value-missing {checker.UNRELATED_VALUE}",
                "env-missing SSH_AUTH_SOCK",
                "env-missing GPG_AGENT_INFO",
            ],
            cwd=tmp_path,
            env={"PATH": path, "GLM_KEY": checker.SELECTED_VALUE},
        )
        assert clean[f"env-value-present {checker.SELECTED_VALUE}"][0] is True
        assert clean[f"env-value-missing {checker.UNRELATED_VALUE}"][0] is True
        assert clean["env-missing SSH_AUTH_SOCK"][0] is True

    _live_or("credentials", hermetic)


# ---------------------------------------------------------------------------
# Criterion 5 — egress is limited to the selected API
# ---------------------------------------------------------------------------


def test_live_egress_allows_only_the_selected_api(tmp_path: Path) -> None:
    """Unapproved hosts, addresses and names must be refused; an admitting proxy is the fault."""

    def hermetic() -> None:
        port, listener = _bound_listener()
        try:
            # The planted fault: a direct connection a boundary failed to stop.
            leaked = checker.run_probe_program([f"connect 127.0.0.1 {port}"], cwd=tmp_path)
            assert leaked[f"connect 127.0.0.1 {port}"][0] is False
            found = {
                "declared api host admitted": (True, "HTTP/1.1 200 Connection established"),
                "unapproved host denied": leaked[f"connect 127.0.0.1 {port}"],
                "address literal denied": (True, "OSError"),
                "ipv6 address denied": (True, "OSError"),
                "direct dns denied": (True, "gaierror"),
                "proxy bypass denied": (True, "HTTP/1.1 403 Forbidden"),
                "gateway port denied": (True, "no default route"),
            }
            problems = _section_problems("egress", found)
            assert any("unapproved host denied" in problem for problem in problems)
        finally:
            listener.close()
        # A refusing proxy is the required answer; an admitting one is the fault.
        with _ConnectProxy(b"HTTP/1.1 403 Forbidden\r\n\r\n") as proxy:
            denied = checker.run_probe_program(
                ["connect-proxy example.com 443", "connect-admitted example.com"],
                cwd=tmp_path,
                env={"HTTPS_PROXY": f"http://127.0.0.1:{proxy.port}"},
            )
            assert denied["connect-proxy example.com 443"][0] is True
            assert denied["connect-admitted example.com"][0] is True
        with _ConnectProxy(b"HTTP/1.1 200 Connection established\r\n\r\n") as proxy:
            admitted = checker.run_probe_program(
                ["connect-proxy example.com 443"],
                cwd=tmp_path,
                env={"HTTPS_PROXY": f"http://127.0.0.1:{proxy.port}"},
            )
            assert admitted["connect-proxy example.com 443"][0] is False
        # A proxy that is down must never count as enforcement.
        missing = checker.run_probe_program(
            ["connect-proxy example.com 443"], cwd=tmp_path, env={"HTTPS_PROXY": "http://127.0.0.1:1"}
        )
        assert missing["connect-proxy example.com 443"][0] is False

    _live_or("egress", hermetic)


# ---------------------------------------------------------------------------
# Criterion 9 — a retry starts without the prior attempt's state
# ---------------------------------------------------------------------------


def test_live_retry_has_no_prior_attempt_state(tmp_path: Path) -> None:
    """A marker one attempt wrote must be absent for the next one."""

    def hermetic() -> None:
        shared = tmp_path / "shared-candidate"
        shared.mkdir()
        # The planted fault: the second attempt lands in the first one's tree.
        checker.run_probe_program(["marker-write st2-retry"], cwd=shared)
        reused = checker.run_probe_program(["marker-read st2-retry"], cwd=shared)
        assert reused["marker-read st2-retry"][0] is False
        found = {
            "prior attempt marker absent": reused["marker-read st2-retry"],
            "fresh candidate writes": (True, "written"),
        }
        problems = _section_problems("retry", found)
        assert any("prior attempt marker absent" in problem for problem in problems)
        # The clean case: a fresh candidate sees nothing.
        fresh = tmp_path / "fresh-candidate"
        fresh.mkdir()
        clean = checker.run_probe_program(["marker-read st2-retry"], cwd=fresh)
        assert clean["marker-read st2-retry"][0] is True

    _live_or("retry", hermetic)


# ---------------------------------------------------------------------------
# Criterion 13 — the verifier has no host access, no credential, no egress
# ---------------------------------------------------------------------------


def test_live_verifier_has_no_host_access_credentials_or_egress(tmp_path: Path) -> None:
    """The verifier role strips model credentials; the checker reports host reads and egress."""

    def hermetic() -> None:
        # The credential strip is the verifier role's own code: a planted
        # model credential must not survive `Verifier.env`.
        checked = stage2_attempt.Verifier(tmp_path, None).env(
            {"GLM_KEY": checker.SELECTED_VALUE, "PATH": os.environ.get("PATH", "/usr/bin:/bin")}
        )
        assert "GLM_KEY" not in checked
        sentinel = tmp_path / "sentinel.txt"
        sentinel.write_text("host secret\n", encoding="utf-8")
        port, listener = _bound_listener()
        try:
            # The planted faults, through the same probe the container would
            # run: on the host the sentinel is readable and the port
            # reachable, while the stripped credential keeps its task green.
            results = checker.run_probe_program(
                [
                    f"read {sentinel}",
                    f"env-value-missing {checker.SELECTED_VALUE}",
                    "env-missing SSH_AUTH_SOCK",
                    f"connect 127.0.0.1 {port}",
                ],
                cwd=tmp_path,
                env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "GLM_KEY": checker.SELECTED_VALUE},
            )
        finally:
            listener.close()
        assert results[f"read {sentinel}"][0] is False
        assert results[f"env-value-missing {checker.SELECTED_VALUE}"][0] is True
        assert results["env-missing SSH_AUTH_SOCK"][0] is True
        assert results[f"connect 127.0.0.1 {port}"][0] is False
        found = {
            "verifier cannot read host files": results[f"read {sentinel}"],
            "verifier has no selected credential": results[f"env-value-missing {checker.SELECTED_VALUE}"],
            "verifier has no agent socket": results["env-missing SSH_AUTH_SOCK"],
            "verifier has no egress": results[f"connect 127.0.0.1 {port}"],
            "verifier cannot resolve names": (True, "gaierror"),
            "verifier writes its candidate": (True, "written"),
        }
        problems = _section_problems("verifier", found)
        assert any("verifier cannot read host files" in problem for problem in problems)
        assert any("verifier has no egress" in problem for problem in problems)
        assert not any("verifier has no selected credential" in problem for problem in problems)

    _live_or("verifier", hermetic)


# ---------------------------------------------------------------------------
# Criterion 22 — cleanup removes exactly the invocation's own resources
# ---------------------------------------------------------------------------


def test_live_cleanup_and_interrupted_attempt_recovery(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Recovery cleans the interrupted invocation and never the decoy."""

    def hermetic() -> None:
        stand_in = tmp_path / "runtime"
        monkeypatch.setenv("STAGE2_RUNTIME_STAND_IN", str(stand_in))
        monkeypatch.setenv("STAGE2_STATE_DIR", str(tmp_path / "state"))
        runtime = stage2_attempt.choose_runtime()
        interrupted = stage2_attempt.InvocationState(
            id=stage2_attempt.new_invocation_id(),
            verb="probe",
            endpoint=checker.PROBE_ENDPOINT,
            model="isolation-probe",
            baseline="0" * 40,
        )
        cand = runtime.create_volume(interrupted, "cand")
        priv = runtime.create_network(interrupted, "priv", internal=True)
        interrupted.cleanup_pending = "planted by the test"
        interrupted.save()
        # A user-owned decoy: created outside any recorded cleanup, never a
        # restoration surface (spec protected areas).
        decoy = stage2_attempt.InvocationState(
            id=stage2_attempt.new_invocation_id(), verb="decoy", endpoint="-", model="-", baseline="0" * 40
        )
        decoy_name = runtime.create_volume(decoy, "decoy")
        still = stage2_attempt.reconcile_pending(runtime)
        assert not interrupted.path.exists(), "the interrupted invocation was not recovered"
        assert interrupted.id not in still
        log = [json.loads(line) for line in (stand_in / "runtime-calls.jsonl").read_text().splitlines() if line.strip()]
        removed = {
            resource.get("name")
            for entry in log
            if entry.get("op") == "remove"
            for resource in entry.get("resources", [])
        }
        assert cand in removed and priv in removed, "the interrupted resources were not cleaned"
        assert decoy_name not in removed, "the decoy was removed - a user-owned resource was deleted"
        assert decoy_name in checker._leftover_names(runtime, decoy.id), "the decoy must survive recovery"

    _live_or("cleanup", hermetic)


# ---------------------------------------------------------------------------
# Criterion 23 — the report demands every probe and the exact identities
# ---------------------------------------------------------------------------


def test_qualification_report_requires_all_probes_and_exact_identities(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A report missing a probe or an identity is not a report; the cache matches exactly."""

    def version_shim() -> str:
        shim = tmp_path / "fake-podman"
        shim.write_text("#!/bin/sh\necho podman version 9.9.9\n", encoding="utf-8")
        shim.chmod(0o755)
        return str(shim)

    # A missing section is a problem; a missing probe is a problem.
    _report, problems = checker.build_report({}, _identity())
    assert len(problems) == len(checker.REQUIRED_PROBES)
    assert all("did not run" in problem for problem in problems)
    found = {name: (True, "ok") for name in checker.REQUIRED_PROBES["host-files"]}
    _report, problems = checker.build_report({"host-files": found}, _identity())
    assert problems == []
    partial = dict(list(found.items())[:-1])
    _report, problems = checker.build_report({"host-files": partial}, _identity())
    assert problems == [f"host-files: the probe '{checker.REQUIRED_PROBES['host-files'][-1]}' did not run"]

    # The identities are real: backend version, commit, policy hash, declared hosts.
    monkeypatch.setattr(stage2_attempt, "selected_program", lambda: ("podman", version_shim()), raising=True)
    identity = checker.identities(REPO_ROOT)
    assert identity["program"] == {"name": "podman", "version": "podman version 9.9.9"}
    assert len(identity["commit"]) == 40
    assert len(identity["policy_hash"]) == 64
    assert identity["api_hosts"] == ["api.z.ai"]
    assert identity["images"]["model"]["reference"] == "localhost/coding-harness-stage2-model"

    # The cache reuses only an exact fingerprint match.
    cache = tmp_path / "cache.json"
    cached = {"fingerprint": checker.fingerprint(identity), "sections": {}}
    cache.write_text(json.dumps(cached), encoding="utf-8")
    assert checker.load_cache(cache, identity) == cached
    other = {**identity, "commit": "1" * 40}
    assert checker.load_cache(cache, other) is None


def test_the_isolation_gate_refuses_without_prerequisites(monkeypatch: pytest.MonkeyPatch) -> None:
    """Without a usable backend the command exits 2 and measures nothing (exit 2, never a skip)."""

    def refusing_program() -> tuple[str, str]:
        raise stage2_attempt.BoundaryRefused("podman is not installed (test)")

    monkeypatch.setattr(stage2_attempt, "selected_program", refusing_program, raising=True)
    assert checker.main(["--program", "podman"]) == 2
