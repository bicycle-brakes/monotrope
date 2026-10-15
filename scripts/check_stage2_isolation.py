#!/usr/bin/env python3
"""check_stage2_isolation.py - measure the writing boundary, never assume it
(ADR 0018, plan step 7, spec criterion 23).

**What this command does.** It exercises the production supervisor
(`scripts/stage2_attempt.py`) and its adapters with local probe programs and
synthetic login data - never a paid model call - and reports, for the real
backend it finds, whether:

* host files (home, worktree, Git metadata, secrets) are unreadable through
  file tools and shell commands (criterion 2);
* host state cannot be altered from inside an attempt (criterion 3);
* only the selected endpoint's login material is visible (criterion 4);
* external egress is limited to the declared API hosts (criterion 5);
* a second attempt starts without the first one's state (criterion 9);
* the verifier holds no credential, no egress and no host access (criterion 13);
* cleanup removes exactly the invocation's own resources, and an interrupted
  invocation is recovered at the next start (criterion 22).

Every probe section runs as a real writing attempt: the same preflight, the
same private volumes, the same egress proxy the `draft`/`implement`/`repair`
verbs use - only the inner command is the probe, and the login is synthetic.

**What this command is not.** It is not a substitute for the repository suite:
the normal test run exercises the checker's logic on the stand-in transport,
while the live boundary evidence is this command's report, produced on real
macOS and Linux machines at named commits. A missing runtime, an unmeasured
image or an undeclared endpoint profile makes the command *fail* with exit 2 -
it never skips a probe and never claims green.

**The report and its cache.** The report (`tools/stage2/isolation-report.json`
by default) carries the commit, platform, backend version, image digests and
the policy hash, plus every probe's outcome; it is scrubbed - no host paths,
no credential values. `--cache` stores a green report under a fingerprint of
exactly those identities; an entry is reused only when every identity matches.
`--build` rebuilds the locked images first and records their digests in
`tools/stage2/runtime.lock.yaml`, preserving the file's text.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform as platform_module
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import stage2  # noqa: E402
import stage2_attempt  # noqa: E402
from stage2_attempt import ANSWER_PLACEHOLDER, BoundaryRefused  # noqa: E402

# The probes sign in through the endpoint's env-token form with synthetic
# values from a temporary secrets file: a real login never touches a probe.
PROBE_ENDPOINT = "glm-coding-plan"
PROBE_MINUTES = 10
SELECTED_VALUE = "st2-selected-credential-value"
UNRELATED_VALUE = "st2-unrelated-credential-value"
REPORT_SCHEMA = "stage2-isolation-report/1"
POLICY_SCRIPTS = ("scripts/stage2_attempt.py", "scripts/stage2_egress.py", "scripts/stage2_verify_inside.py")

# The probes every section owes. A report missing one is not a report:
# the command fails until every outcome stands (criterion 23).
REQUIRED_PROBES: dict[str, tuple[str, ...]] = {
    "host-files": (
        "read sentinel",
        "shell-read sentinel",
        "read worktree file",
        "read git metadata",
        "read host secrets file",
    ),
    "host-writes": ("write sentinel", "write worktree file", "write git HEAD", "write git hook"),
    "credentials": (
        "selected credential travels",
        "unrelated credential absent",
        "no agent socket variable",
        "no gpg agent variable",
        "host secrets file unreadable",
    ),
    "egress": (
        "declared api host admitted",
        "unapproved host denied",
        "address literal denied",
        "ipv6 address denied",
        "direct dns denied",
        "proxy bypass denied",
        "gateway port denied",
    ),
    "retry": ("prior attempt marker absent", "fresh candidate writes"),
    "verifier": (
        "verifier cannot read host files",
        "verifier has no selected credential",
        "verifier has no agent socket",
        "verifier has no egress",
        "verifier cannot resolve names",
        "verifier writes its candidate",
    ),
    "cleanup": (
        "controlled exit leaves no resources",
        "interrupted invocation recovered",
        "unrelated resource survives",
    ),
}


# ---------------------------------------------------------------------------
# The probe program. It travels as an input file and runs inside the
# container (or, hermetically, wherever the tests point it); every task
# answers "did the required refusal happen".
# ---------------------------------------------------------------------------

PROBE = r"""
import json, os, socket, subprocess, sys
from urllib.parse import urlparse

def read_task(path):
    try:
        with open(path, "rb") as handle:
            data = handle.read(64)
        return False, "read {} bytes".format(len(data))
    except OSError as error:
        return True, type(error).__name__

def shell_read_task(path):
    done = subprocess.run(["/bin/sh", "-c", "cat \"$P\""], env={**os.environ, "P": path},
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return done.returncode != 0, "exit {}".format(done.returncode)

def write_task(path):
    try:
        with open(path, "ab"):
            pass
        return False, "opened for writing"
    except OSError as error:
        return True, type(error).__name__

def env_missing_task(name):
    return name not in os.environ, "present" if name in os.environ else "absent"

def env_value_missing_task(value):
    hits = [name for name, found in os.environ.items() if value in found]
    return not hits, "visible as {}".format(hits) if hits else "absent"

def env_value_present_task(value):
    hits = [name for name, found in os.environ.items() if value in found]
    return bool(hits), "visible as {}".format(hits) if hits else "absent"

def connect_task(host, port):
    try:
        socket.create_connection((host, int(port)), timeout=5).close()
        return False, "connected"
    except OSError as error:
        return True, type(error).__name__

def proxy_target():
    named = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if not named:
        return None
    parsed = urlparse(named)
    return parsed.hostname, parsed.port or 8080

def connect_proxy_task(host, port, admitted):
    target = proxy_target()
    if target is None:
        return False, "no proxy is configured; the CONNECT path is unmeasured"
    try:
        with socket.create_connection(target, timeout=5) as sock:
            sock.sendall("CONNECT {}:{} HTTP/1.1\r\nHost: {}:{}\r\n\r\n".format(host, port, host, port).encode())
            status = sock.recv(1024).split(b"\r\n", 1)[0].decode(errors="replace")
        if admitted:
            return " 403" not in status, status
        return " 403" in status, status
    except OSError as error:
        return False, type(error).__name__

def resolve_task(host):
    try:
        socket.getaddrinfo(host, 443)
        return False, "resolved"
    except OSError as error:
        return True, type(error).__name__

def marker_write_task(name):
    path = "/work/marker-{}".format(name)
    try:
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(name)
        return True, "written"
    except OSError as error:
        return False, type(error).__name__

def marker_read_task(name):
    path = "/work/marker-{}".format(name)
    return not os.path.exists(path), "still there" if os.path.exists(path) else "absent"

def work_write_task():
    try:
        with open("/work/probe-wrote.txt", "w", encoding="utf-8") as handle:
            handle.write("probe")
        return True, "written"
    except OSError as error:
        return False, type(error).__name__

def gateway_task(port):
    gateway = None
    try:
        with open("/proc/net/route", encoding="utf-8") as handle:
            for line in handle.read().splitlines()[1:]:
                fields = line.split()
                if len(fields) > 2 and fields[1] == "00000000":
                    raw = bytes.fromhex(fields[2])
                    gateway = ".".join(str(part) for part in raw[::-1])
                    break
    except OSError:
        return True, "no routing table"
    if gateway is None:
        return True, "no default route"
    return connect_task(gateway, port)

def dispatch(task):
    parts = task.split()
    kind = parts[0]
    if kind == "read":
        return read_task(parts[1])
    if kind == "shell-read":
        return shell_read_task(parts[1])
    if kind == "write":
        return write_task(parts[1])
    if kind == "env-missing":
        return env_missing_task(parts[1])
    if kind == "env-value-missing":
        return env_value_missing_task(parts[1])
    if kind == "env-value-present":
        return env_value_present_task(parts[1])
    if kind == "connect":
        return connect_task(parts[1], parts[2])
    if kind == "connect-proxy":
        return connect_proxy_task(parts[1], parts[2], admitted=False)
    if kind == "connect-admitted":
        return connect_proxy_task(parts[1], 443, admitted=True)
    if kind == "resolve":
        return resolve_task(parts[1])
    if kind == "marker-write":
        return marker_write_task(parts[1])
    if kind == "marker-read":
        return marker_read_task(parts[1])
    if kind == "work-write":
        return work_write_task()
    if kind == "gateway":
        return gateway_task(parts[1])
    return False, "unknown task {}".format(kind)

def main():
    tasks, answer = sys.argv[1:-1], sys.argv[-1]
    payload = json.dumps({"results": {task: list(dispatch(task)) for task in tasks}})
    print(payload)
    try:
        os.makedirs(os.path.dirname(answer) or ".", exist_ok=True)
        with open(answer, "w", encoding="utf-8") as handle:
            handle.write(payload)
    except OSError:
        pass  # the printed line is the answer; a read-only answer path is fine

main()
"""


def run_probe_program(tasks: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> dict[str, list]:
    """Run the probe program itself and return its task results.

    The hermetic vehicle: the tests run the same program the container would
    run, against whichever filesystem and environment they point it at, so a
    broken probe is caught without a backend. The live sections below never
    use this - they launch the probe through the production supervisor.
    """
    with tempfile.TemporaryDirectory(prefix="stage2-probe-") as tmp:
        program = Path(tmp) / "probe.py"
        program.write_text(PROBE, encoding="utf-8")
        answer = Path(tmp) / "answer.md"
        done = subprocess.run(
            [sys.executable, str(program), *tasks, str(answer)],
            cwd=cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            errors="replace",
            check=False,
            timeout=120,
        )
        for line in reversed(done.stdout.splitlines()):
            if line.startswith("{"):
                return json.loads(line)["results"]
        return {"the probe produced no answer": [False, f"exit {done.returncode}: {done.stderr[-160:]}"]}


# ---------------------------------------------------------------------------
# Identities, fingerprint, cache, the lock update (criterion 23)
# ---------------------------------------------------------------------------


def policy_hash() -> str:
    """sha256 over the boundary's own code and its required capabilities."""
    digest = hashlib.sha256()
    for name in POLICY_SCRIPTS:
        digest.update((REPO_ROOT / name).read_bytes())
    require = (stage2_attempt.runtime_lock().get("boundary") or {}).get("require") or []
    digest.update(json.dumps(require, sort_keys=True).encode())
    return digest.hexdigest()


def program_version(executable: str) -> str:
    done = subprocess.run(
        [executable, "--version"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, check=False
    )
    if done.returncode != 0 or not done.stdout.strip():
        raise BoundaryRefused(f"{executable} --version could not be read; the backend is unusable.")
    return done.stdout.strip().splitlines()[0]


def current_commit() -> str:
    return stage2_attempt._git(REPO_ROOT, "rev-parse", "HEAD").stdout.decode().strip()


def identities(root: Path) -> dict:
    """Everything a cached report must match to count for this machine."""
    kind, executable = stage2_attempt.selected_program()
    lock = stage2_attempt.runtime_lock()
    images = {}
    for role in ("model", "verifier"):
        entry = (lock.get("images") or {}).get(role) or {}
        images[role] = {
            "reference": entry.get("reference"),
            "digest": entry.get("digest"),
            "measured": bool(entry.get("measured")),
        }
    return {
        "schema": REPORT_SCHEMA,
        "commit": current_commit(),
        "platform": {
            "system": platform_module.system(),
            "release": platform_module.release(),
            "machine": platform_module.machine(),
        },
        "program": {"name": kind, "version": program_version(executable)},
        "images": images,
        "policy_hash": policy_hash(),
        "endpoint": PROBE_ENDPOINT,
        "api_hosts": stage2_attempt.api_hosts(root, PROBE_ENDPOINT),
    }


def fingerprint(identity: dict) -> str:
    return hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()


def load_cache(path: Path, identity: dict) -> dict | None:
    """The cached report, but only when every identity matches exactly."""
    try:
        cached = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return cached if cached.get("fingerprint") == fingerprint(identity) else None


def update_lock_digests(updates: dict[str, dict]) -> None:
    """Record measured image digests in the lock, preserving its text.

    The lock is documentation as much as data; the checker replaces exactly
    the four placeholder lines per role and refuses when the shape changed.
    """
    path = stage2_attempt.lock_path()
    text = path.read_text(encoding="utf-8")
    fields = (
        ("digest", "null", lambda values: '"{}"'.format(values["digest"])),
        ("measured", "false", lambda _values: "true"),
        ("measured_at", "null", lambda values: '"{}"'.format(values["measured_at"])),
        ("measured_commit", "null", lambda values: '"{}"'.format(values["measured_commit"])),
    )
    for role, values in updates.items():
        # The capture runs to the next sibling key or the end of file - the
        # verifier's block is the last one the lock holds.
        block = re.search(rf"^  {role}:\n(.*?)(?=^  \w+:|\Z)", text, re.MULTILINE | re.DOTALL)
        if block is None:
            raise BoundaryRefused(f"the runtime lock has no {role} image block; update {path} by hand.")
        replaced = block.group(1)
        for field, old, render in fields:
            pattern = rf"^(\s+){field}: {old}$"
            replaced, count = re.subn(
                pattern,
                rf"\g<1>{field}: {render(values)}",
                replaced,
                count=1,
                flags=re.MULTILINE,
            )
            if count != 1:
                raise BoundaryRefused(f"the runtime lock's {role} {field} line changed shape; update {path} by hand.")
        text = text[: block.start(1)] + replaced + text[block.end(1) :]
    path.write_text(text, encoding="utf-8")


def build_images(root: Path) -> dict:
    """Build both locked roles from the Containerfile and record their digests."""
    _kind, executable = stage2_attempt.selected_program()
    lock = stage2_attempt.runtime_lock()
    updates: dict[str, dict] = {}
    for role in ("model", "verifier"):
        reference = ((lock.get("images") or {}).get(role) or {}).get("reference")
        if not reference:
            raise BoundaryRefused(f"the runtime lock names no reference for the {role} image.")
        done = subprocess.run(
            [executable, "build", "-f", "tools/stage2/Containerfile", "--target", role, "-t", reference, "."],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            check=False,
        )
        if done.returncode != 0:
            raise BoundaryRefused(f"the {role} image build failed: {done.stdout[-400:]}")
        identity = subprocess.run(
            [executable, "inspect", "--format", "{{.Digest}}", reference],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=False,
        ).stdout.strip()
        if not identity:
            local = subprocess.run(
                [executable, "inspect", "--format", "{{.Id}}", reference],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                check=False,
            ).stdout.strip()
            identity = "sha256:" + local.split(":")[-1]
        updates[role] = {"digest": identity, "measured_at": stage2.today(), "measured_commit": current_commit()}
    update_lock_digests(updates)
    return updates


# ---------------------------------------------------------------------------
# The live probe sections. Each runs real writing attempts through the
# production supervisor and returns {probe name: (ok, detail)}.
# ---------------------------------------------------------------------------


def synthetic_secrets(directory: Path) -> Path:
    """A temporary secrets file carrying the selected key and an unrelated one."""
    path = directory / "secrets.env"
    path.write_text(
        "# synthetic probe credentials (ADR 0018) - not real logins\n"
        f"export GLM_KEY='{SELECTED_VALUE}'\n"
        f"export UNRELATED_PROBE_KEY='{UNRELATED_VALUE}'\n",
        encoding="utf-8",
    )
    return path


def probe_launch(root: Path, tasks: list[str], secrets: Path) -> tuple[dict[str, list], str]:
    """One production launch whose inner command is the probe.

    Returns the task results and the invocation id, so the cleanup section can
    verify what the launch left behind. The synthetic secrets file is the only
    login source for the launch (`CC_SECRETS`, restored afterwards).
    """
    spec = stage2_attempt.WriterSpec(
        verb="probe",
        change="isolated-attempts",
        endpoint=PROBE_ENDPOINT,
        model="isolation-probe",
        prompt="Isolation boundary probe (ADR 0018). Do not answer; the probe program writes its own result.",
        inner_command=[
            "python3",
            f"{stage2_attempt.CANDIDATE_WORK}/.stage2/probe.py",
            *tasks,
            ANSWER_PLACEHOLDER,
        ],
        inner_env={},
        baseline=stage2_attempt._rev_of(root, "HEAD"),
        input_files={".stage2/probe.py": PROBE.encode("utf-8")},
        timeout=PROBE_MINUTES * 60,
    )
    previous = os.environ.get("CC_SECRETS")
    os.environ["CC_SECRETS"] = str(secrets)
    try:
        run = stage2_attempt.launch_writer_call(root=root, spec=spec)
    finally:
        if previous is None:
            os.environ.pop("CC_SECRETS", None)
        else:
            os.environ["CC_SECRETS"] = previous
    try:
        if run.done.returncode != 0:
            stderr = run.done.stderr
            text = stderr.decode(errors="replace") if isinstance(stderr, bytes) else str(stderr)
            raise BoundaryRefused(f"the probe launch ended {run.done.returncode}: {text[-200:]}")
        if run.answer_path is None:
            raise BoundaryRefused("the probe wrote no answer; a missing answer is never a pass.")
        return json.loads(run.answer_path.read_text(encoding="utf-8"))["results"], run.state.id
    finally:
        run.discard()


def section_host_files(root: Path, sentinel: Path, secrets: Path) -> dict[str, tuple[bool, str]]:
    results, _ = probe_launch(
        root,
        [
            f"read {sentinel}",
            f"shell-read {sentinel}",
            f"read {root / 'model-endpoints.yaml'}",
            f"read {root / '.git' / 'HEAD'}",
            f"read {Path.home() / '.config' / 'cc-routing' / 'secrets.env'}",
        ],
        secrets,
    )
    return dict(zip(REQUIRED_PROBES["host-files"], (tuple(found) for found in results.values()), strict=False))


def section_host_writes(root: Path, sentinel: Path, secrets: Path) -> dict[str, tuple[bool, str]]:
    results, _ = probe_launch(
        root,
        [
            f"write {sentinel}",
            f"write {root / 'model-endpoints.yaml'}",
            f"write {root / '.git' / 'HEAD'}",
            f"write {root / '.git' / 'hooks' / 'pre-commit'}",
        ],
        secrets,
    )
    return dict(zip(REQUIRED_PROBES["host-writes"], (tuple(found) for found in results.values()), strict=False))


def section_credentials(root: Path, sentinel: Path, secrets: Path) -> dict[str, tuple[bool, str]]:
    results, _ = probe_launch(
        root,
        [
            f"env-value-present {SELECTED_VALUE}",
            f"env-value-missing {UNRELATED_VALUE}",
            "env-missing SSH_AUTH_SOCK",
            "env-missing GPG_AGENT_INFO",
            f"read {Path.home() / '.config' / 'cc-routing' / 'secrets.env'}",
        ],
        secrets,
    )
    return dict(zip(REQUIRED_PROBES["credentials"], (tuple(found) for found in results.values()), strict=False))


def section_egress(root: Path, _sentinel: Path, secrets: Path, declared: str) -> dict[str, tuple[bool, str]]:
    results, _ = probe_launch(
        root,
        [
            f"connect-admitted {declared}",
            "connect example.com 443",
            "connect 1.1.1.1 443",
            "connect 2606:4700:4700::1111 443",
            "resolve example.com",
            "connect-proxy example.com 443",
            "gateway 8080",
            "gateway 443",
        ],
        secrets,
    )
    return dict(zip(REQUIRED_PROBES["egress"], (tuple(found) for found in results.values()), strict=False))


def section_retry(root: Path, _sentinel: Path, secrets: Path) -> dict[str, tuple[bool, str]]:
    """Two full launches: the second must see nothing the first left."""
    first, _ = probe_launch(root, ["marker-write st2-retry", "work-write"], secrets)
    second, _ = probe_launch(root, ["marker-read st2-retry", "work-write"], secrets)
    wrote_first = tuple(first.get("work-write", [False, "missing result"]))
    wrote_second = tuple(second.get("work-write", [False, "missing result"]))
    return {
        "prior attempt marker absent": tuple(second.get("marker-read st2-retry", [False, "missing result"])),
        "fresh candidate writes": (
            bool(wrote_first[0] and wrote_second[0]),
            f"first {wrote_first[1]}, second {wrote_second[1]}",
        ),
    }


def section_verifier(root: Path, sentinel: Path, secrets: Path) -> dict[str, tuple[bool, str]]:
    """The verifier role, launched the production way: no network, no credential.

    `run_verifier` is the one entry the verbs use - fresh volumes, the shim's
    inputs, cleanup in its finally - so the probe travels as an input and the
    answer comes back on stdout.
    """
    declared = stage2_attempt.api_hosts(root, PROBE_ENDPOINT)[0]
    baseline = stage2_attempt._rev_of(root, "HEAD")
    command = [
        "python3",
        f"{stage2_attempt.CANDIDATE_WORK}/.stage2/probe.py",
        f"read {sentinel}",
        f"env-value-missing {SELECTED_VALUE}",
        "env-missing SSH_AUTH_SOCK",
        f"connect {declared} 443",
        "connect 1.1.1.1 443",
        f"resolve {declared}",
        "work-write",
        f"{stage2_attempt.CANDIDATE_WORK}/.stage2/verifier-probe-answer.md",
    ]
    done, _post = stage2_attempt.run_verifier(
        root,
        stage2_attempt.worktree_tar(root, baseline),
        stage2_attempt.git_tar(root, baseline),
        command,
        # The selected value travels under a *model* credential name; the
        # verifier role must strip it before anything starts (criterion 13).
        {"GLM_KEY": SELECTED_VALUE},
        timeout=PROBE_MINUTES * 60,
        inputs={".stage2/probe.py": PROBE.encode("utf-8")},
    )
    stdout = done.stdout if isinstance(done.stdout, str) else done.stdout.decode(errors="replace")
    results: dict[str, list] = {}
    for line in reversed(stdout.splitlines()):
        if line.startswith("{"):
            results = json.loads(line)["results"]
            break
    if not results:
        return {
            name: (False, f"the verifier probe produced no answer (exit {done.returncode})")
            for name in REQUIRED_PROBES["verifier"]
        }
    return dict(zip(REQUIRED_PROBES["verifier"], (tuple(found) for found in results.values()), strict=False))


def _stand_in_log_entries(runtime) -> list[dict]:
    log = getattr(runtime, "log", None)
    if log is None or not log.is_file():
        return []
    return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines() if line.strip()]


def _leftover_names(runtime, invocation_id: str) -> list[str]:
    """Resources a real backend still holds for this invocation, or stand-in evidence."""
    if stage2_attempt._stand_in_dir() is not None:
        created = [
            entry.get("name")
            for entry in _stand_in_log_entries(runtime)
            if entry.get("op") in ("volume create", "network create") and entry.get("invocation") == invocation_id
        ]
        removed = {
            resource.get("name")
            for entry in _stand_in_log_entries(runtime)
            if entry.get("op") == "remove"
            for resource in entry.get("resources", [])
        }
        return [name for name in created if name not in removed]
    _kind, executable = stage2_attempt.selected_program()
    leftovers: list[str] = []
    for kind, argv in (
        ("volume", ["volume", "ls", "--filter", f"name=stage2-{invocation_id[:12]}", "--format", "{{.Name}}"]),
        ("network", ["network", "ls", "--filter", f"name=stage2-{invocation_id[:12]}", "--format", "{{.Name}}"]),
        ("container", ["ps", "-a", "--filter", f"name=egress-proxy-{invocation_id[:12]}", "--format", "{{.Names}}"]),
    ):
        done = subprocess.run([executable, *argv], stdout=subprocess.PIPE, text=True, check=False)
        if done.returncode != 0:
            # A query that cannot run is not an empty answer: an unreadable
            # state never counts as "nothing left".
            leftovers.append(f"{kind}: the listing failed (exit {done.returncode})")
            continue
        leftovers += [f"{kind}:{line}" for line in done.stdout.splitlines() if line.strip()]
    return leftovers


def section_cleanup(root: Path, _sentinel: Path, secrets: Path) -> dict[str, tuple[bool, str]]:
    """Controlled exit, interrupted recovery, and the decoy that must survive."""
    runtime = stage2_attempt.choose_runtime()
    results: dict[str, tuple[bool, str]] = {}
    # A controlled exit: a full launch whose own cleanup must leave nothing.
    _results, invocation = probe_launch(root, ["work-write"], secrets)
    state_gone = not (stage2_attempt.state_dir() / f"{invocation}.json").exists()
    leftovers = _leftover_names(runtime, invocation)
    results["controlled exit leaves no resources"] = (
        state_gone and not leftovers,
        f"state file {'gone' if state_gone else 'remains'}; leftovers {leftovers or 'none'}",
    )
    # An interrupted invocation: a planted state file whose cleanup never ran.
    interrupted = stage2_attempt.InvocationState(
        id=stage2_attempt.new_invocation_id(),
        verb="probe",
        endpoint=PROBE_ENDPOINT,
        model="isolation-probe",
        baseline="0" * 40,
    )
    runtime.create_volume(interrupted, "cand")
    runtime.create_network(interrupted, "priv", internal=True)
    interrupted.cleanup_pending = "planted by the isolation probe"
    interrupted.save()
    # A user-owned decoy: created outside any recorded cleanup, never a
    # restoration surface (spec protected areas).
    decoy = stage2_attempt.InvocationState(
        id=stage2_attempt.new_invocation_id(), verb="decoy", endpoint="-", model="-", baseline="0" * 40
    )
    decoy_name = runtime.create_volume(decoy, "decoy")
    still = stage2_attempt.reconcile_pending(runtime)
    recovered = not interrupted.path.exists() and interrupted.id not in still
    results["interrupted invocation recovered"] = (recovered, ", ".join(still) or "recovered")
    if stage2_attempt._stand_in_dir() is not None:
        # _leftover_names answers "what does this invocation still hold": the
        # decoy must still hold its volume - it was never a cleanup subject.
        survived = decoy_name in _leftover_names(runtime, decoy.id)
    else:
        _kind, executable = stage2_attempt.selected_program()
        listed = subprocess.run(
            [executable, "volume", "ls", "--filter", f"name={decoy_name}", "--format", "{{.Name}}"],
            stdout=subprocess.PIPE,
            text=True,
            check=False,
        ).stdout.split()
        survived = decoy_name in listed
    results["unrelated resource survives"] = (survived, decoy_name if survived else "removed")
    # The probe removes the decoy it created; nothing user-owned is touched.
    runtime.remove_resources(decoy.resources)
    return results


# ---------------------------------------------------------------------------
# Report assembly and the command
# ---------------------------------------------------------------------------


def build_report(sections: dict[str, dict[str, tuple[bool, str]]], identity: dict) -> tuple[dict, list[str]]:
    """The scrubbed report, and every problem: a missing or failed probe."""
    problems: list[str] = []
    carried: dict[str, dict] = {}
    for name, required in REQUIRED_PROBES.items():
        found = sections.get(name)
        if found is None:
            problems.append(f"{name}: the section did not run")
            continue
        probes = {}
        for probe in required:
            if probe not in found:
                problems.append(f"{name}: the probe '{probe}' did not run")
                continue
            ok, detail = found[probe]
            probes[probe] = {"ok": bool(ok), "detail": str(detail)[:160]}
            if not ok:
                problems.append(f"{name}: '{probe}' failed - {detail}")
        carried[name] = {"probes": probes}
    report = {**identity, "sections": carried, "problems": problems}
    return report, problems


def prerequisite_problems(root: Path, program: str | None, build: bool) -> list[str]:
    """Everything that must hold before any probe starts; the command never skips."""
    problems: list[str] = []
    if stage2_attempt._stand_in_dir() is not None:
        # The test transport executes the inner command on the host: whatever
        # it produced would measure this machine, not the boundary.
        return ["STAGE2_RUNTIME_STAND_IN is set; the probes would not run in containers."]
    setting = stage2_attempt.program_setting()
    setting_problem = stage2_attempt.program_problem(setting)
    if setting_problem:
        return [setting_problem]
    if program is not None and program != setting:
        problems.append(
            f"--program {program} disagrees with STAGE2_CONTAINER_PROGRAM={setting}; "
            "the launches read the environment, so set the environment instead."
        )
    try:
        kind, executable = stage2_attempt.selected_program()
        program_version(executable)
    except BoundaryRefused as error:
        return problems + [f"the container backend is unusable: {error}"]
    profile = stage2_attempt.profile_problem(root, PROBE_ENDPOINT)
    if profile:
        problems.append(f"the probe endpoint is not qualified: {profile}")
    if not build:
        try:
            lock = stage2_attempt.runtime_lock()
            problem = stage2_attempt.lock_problem(lock, kind)
            if problem:
                problems.append(f"the runtime lock is unmeasured: {problem} (run with --build)")
        except BoundaryRefused as error:
            problems.append(f"the runtime lock cannot be read: {error}")
    return problems


def main(argv: list[str] | None = None) -> int:
    """Measure; write the report and, when green, the cache; fail loudly."""
    parser = argparse.ArgumentParser(description="Measure the stage-2 writing boundary (ADR 0018).")
    parser.add_argument("--program", choices=stage2_attempt.PROGRAMS, default=None, help="the backend to measure")
    parser.add_argument("--build", action="store_true", help="build the locked images first and record digests")
    parser.add_argument("--report", type=Path, default=REPO_ROOT / "tools" / "stage2" / "isolation-report.json")
    parser.add_argument("--cache", type=Path, default=REPO_ROOT / "tools" / "stage2" / "isolation-cache.json")
    args = parser.parse_args(argv)
    root = REPO_ROOT
    problems = prerequisite_problems(root, args.program, args.build)
    if problems:
        for problem in problems:
            print(f"refused: {problem}", file=sys.stderr)
        print("the boundary is not measured; nothing was skipped.", file=sys.stderr)
        return 2
    try:
        if args.build:
            build_images(root)
        identity = identities(root)
    except BoundaryRefused as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    if not args.build:
        cached = load_cache(args.cache, identity)
        if cached is not None:
            print(
                f"cached report reused: commit {identity['commit'][:12]}, {identity['program']['name']} "
                f"{identity['program']['version']}, policy {identity['policy_hash'][:12]}."
            )
            args.report.write_text(json.dumps(cached, indent=1, sort_keys=True) + "\n", encoding="utf-8")
            return 0
    with tempfile.TemporaryDirectory(prefix="stage2-isolation-") as tmp:
        workdir = Path(tmp)
        sentinel = workdir / "sentinel.txt"
        sentinel.write_text("a host sentinel the attempt must never see (ADR 0018)", encoding="utf-8")
        secrets = synthetic_secrets(workdir)
        declared = identity["api_hosts"][0]
        runners = (
            ("host-files", lambda: section_host_files(root, sentinel, secrets)),
            ("host-writes", lambda: section_host_writes(root, sentinel, secrets)),
            ("credentials", lambda: section_credentials(root, sentinel, secrets)),
            ("egress", lambda: section_egress(root, sentinel, secrets, declared)),
            ("retry", lambda: section_retry(root, sentinel, secrets)),
            ("verifier", lambda: section_verifier(root, sentinel, secrets)),
            ("cleanup", lambda: section_cleanup(root, sentinel, secrets)),
        )
        sections: dict[str, dict[str, tuple[bool, str]]] = {}
        for name, runner in runners:
            try:
                sections[name] = runner()
            except BoundaryRefused as error:
                print(f"refused while running {name}: {error}", file=sys.stderr)
                return 2
        report, problems = build_report(sections, identity)
    report["fingerprint"] = fingerprint(identity)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    for section_name, section in report["sections"].items():
        for probe, outcome in section["probes"].items():
            mark = "ok" if outcome["ok"] else "FAILED"
            print(f"{mark:6} {section_name}: {probe} ({outcome['detail']})")
    if problems:
        print(f"the boundary leaked {len(problems)} probes; see {args.report}", file=sys.stderr)
        return 1
    args.cache.write_text(json.dumps(report, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"the boundary held: commit {identity['commit'][:12]}, report at {args.report}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BoundaryRefused as error:
        print(f"refused: {error}", file=sys.stderr)
        raise SystemExit(2) from None
