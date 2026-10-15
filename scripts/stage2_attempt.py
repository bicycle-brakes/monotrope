#!/usr/bin/env python3
"""stage2_attempt.py - the trusted supervisor of one isolated writing attempt (ADR 0018).

**What this is.** The one module through which every automatic writing call
(`draft`, `implement`, `repair`) and every interactive `session` lifetime
reaches a model: it selects the container program, refuses an unproven
boundary before anything starts, populates a private candidate from the run
baseline, launches the writer in a fresh container, stops it before inspecting
its result, exports and validates what changed, and publishes only validated
bytes to the host worktree - journalled, so a failed publication undoes only
this invocation's own writes. A failed attempt leaves the host worktree at its
baseline except for the runner's evidence; the next attempt starts from the
same baseline plus scrubbed diagnostics, never from a failed candidate.

**Boundary summary** (the acceptance criteria name the refutations):

1. one fresh container, one private candidate volume per attempt - never a
   reusable volume, home or host launch;
2. no host path mount: the candidate is built from `git archive` of the
   baseline commit plus permitted evidence bytes, and the private Git
   metadata is a fresh `--no-local --no-hardlinks` clone without hooks,
   source configuration, alternates or credential helpers, mounted read-only
   into the writer;
3. one selected login: the endpoint's own key or auth file, never another
   provider's token, a full sign-in directory, a keychain or an agent socket;
4. egress through the trusted proxy only (`stage2_egress`), model on the
   private network only, verifier with no network and no model credentials;
5. refusal before launch when the program, image, login, API profile or
   qualification is missing or unmeasured - a Stage-1 call follows the same
   refusal, and no refusal advances the routing table.

**The test transport.** When `STAGE2_RUNTIME_STAND_IN` names a directory, the
supervisor uses `StandInRuntime`: it records every runtime operation as one
JSON line in `<dir>/runtime-calls.jsonl` and executes the writer's command
line after `--` transparently, with the supervisor-constructed environment and
the host worktree as its directory. The suite runs on it; production never
selects it (the variable is unset) and the live probes in
`scripts/check_stage2_isolation.py` measure the real adapters instead.

Exit codes of the `session-supervisor` subcommand: 0 the verified edits are
published uncommitted, 1 the session or its checks failed and the candidate
was discarded, 2 refused before the launch.
"""

from __future__ import annotations

import argparse
import base64
import io
import ipaddress
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

PROGRAMS = ("podman", "docker", "container")
DEFAULT_PROGRAM = "podman"
# The fixed non-root identity the images define (tools/stage2/Containerfile).
NON_ROOT = "1000:1000"
# The candidate's mount point and the runner-owned paths inside it.
CANDIDATE_WORK = "/work"
CANDIDATE_PROMPT = f"{CANDIDATE_WORK}/.stage2/prompt.md"
CANDIDATE_ANSWER = f"{CANDIDATE_WORK}/.stage2/answer.md"
CANDIDATE_RENDER = f"{CANDIDATE_WORK}/.stage2/render.md"
CANDIDATE_CONFIG = f"{CANDIDATE_WORK}/.stage2/config"
# Placeholders an inner command or environment may carry; the supervisor
# substitutes the host staging paths (test transport) or the candidate paths
# (production) and materialises the input files accordingly. A value carrying
# no placeholder passes through unchanged.
PROMPT_PLACEHOLDER = "@STAGE2_PROMPT_FILE@"
ANSWER_PLACEHOLDER = "@STAGE2_ANSWER_FILE@"
RENDER_PLACEHOLDER = "@STAGE2_RENDER@"
CONFIG_PLACEHOLDER = "@STAGE2_CONFIG_DIR@"
# The candidate's work directory in an interactive command: the dispatch cannot
# know it as a host path, because production runs the command inside the image.
WORK_PLACEHOLDER = "@STAGE2_WORK@"
PLACEHOLDERS = (PROMPT_PLACEHOLDER, ANSWER_PLACEHOLDER, RENDER_PLACEHOLDER, CONFIG_PLACEHOLDER, WORK_PLACEHOLDER)
# Runner-owned candidate paths that are inputs or diagnostics, never publication.
RUNNER_PREFIXES = (".stage2/", ".git/")
# What the verifier's own tooling creates inside the candidate while the checks
# run: the wrapped interpreter and ruff the gate list calls by path, tool
# caches, Python's bytecode. Runner-owned noise - never a model change, never
# publication, and never a refusal reason in the exported candidate.
VERIFIER_NOISE = (".venv/", ".pytest_cache/", ".ruff_cache/", ".mypy_cache/", "htmlcov/")


def _is_verifier_noise(name: str) -> bool:
    return (
        name.startswith(VERIFIER_NOISE)
        or name == ".coverage"
        or name.endswith(".pyc")
        or "/__pycache__/" in name
        or name.startswith("__pycache__/")
    )


# Environment names that carry credentials of any provider, or an agent
# socket; a launch environment holding an unselected one is a refusal.
CREDENTIAL_ENV_NAMES = (
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_API_KEY",
    "OPENAI_API_KEY",
    "OPENCODE_API_KEY",
    "GLM_KEY",
    "OPENCODE_GO_KEY",
    "SSH_AUTH_SOCK",
    "GPG_AGENT_INFO",
)
# The one login form per endpoint: its secret line, or its auth file. Nothing
# else - no home, no sign-in directory, no keychain, no agent socket.
LOGIN_FILES = {
    "openai-codex": "~/.codex/auth.json",
    "claude-code-plan": "~/.claude/.credentials.json",
}
LOGIN_ENV = {
    "glm-coding-plan": ("GLM_KEY", ("ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_API_KEY")),
    "opencode-go": ("OPENCODE_GO_KEY", ("OPENCODE_API_KEY",)),
}

_HOST_LABEL = r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?"
_HOST_FORM = re.compile(rf"{_HOST_LABEL}(?:\.{_HOST_LABEL})+")


class BoundaryRefused(Exception):
    """The boundary is unavailable or unproven: the call does not start (exit 2)."""


class AttemptCallFailed(Exception):
    """The writer could not be started or was stopped by its limit.

    `what` carries the limit's name so the caller can raise the exact
    CallFailed text the routing contract has always produced.
    """

    def __init__(self, message: str, what: str | None = None) -> None:
        super().__init__(message)
        self.what = what


# ---------------------------------------------------------------------------
# The container program (criterion 6)
# ---------------------------------------------------------------------------


def program_setting() -> str:
    """The raw setting: an environment value or the default."""
    return os.environ.get("STAGE2_CONTAINER_PROGRAM", DEFAULT_PROGRAM)


def program_problem(setting: str) -> str | None:
    """Why the setting names no supported backend, or None."""
    base = os.path.basename(setting.rstrip("/"))
    if base not in PROGRAMS:
        return (
            f"STAGE2_CONTAINER_PROGRAM names {setting!r}; its basename is none of "
            f"{', '.join(PROGRAMS)}. The runner never substitutes a backend."
        )
    return None


def program_executable(setting: str) -> str:
    """The executable the adapters call: an explicit path as it stands, else the bare name."""
    return setting


def selected_program() -> tuple[str, str]:
    """(kind, executable) of the selected backend, or the refusal."""
    setting = program_setting()
    problem = program_problem(setting)
    if problem:
        raise BoundaryRefused(problem)
    executable = program_executable(setting)
    if os.path.sep in setting:
        if not (Path(executable).is_file() and os.access(executable, os.X_OK)):
            raise BoundaryRefused(f"the selected container program {executable} is not an executable file.")
    elif shutil.which(executable) is None:
        raise BoundaryRefused(
            f"the container program {executable!r} is not usable; install it (tools/stage2/README.md) "
            "or set STAGE2_CONTAINER_PROGRAM. The runner never substitutes a backend."
        )
    return os.path.basename(setting.rstrip("/")), executable


# ---------------------------------------------------------------------------
# The runtime lock (criterion 7: an unmeasured identity refuses the launch)
# ---------------------------------------------------------------------------


def lock_path() -> Path:
    named = os.environ.get("STAGE2_RUNTIME_LOCK")
    return Path(named) if named else REPO_ROOT / "tools" / "stage2" / "runtime.lock.yaml"


def runtime_lock() -> dict:
    """The lock, defensively loaded: a file that cannot be read is a refusal, not an empty grant."""
    try:
        data = yaml.safe_load(lock_path().read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as error:
        raise BoundaryRefused(f"the runtime lock {lock_path()} cannot be read: {error}") from None
    if not isinstance(data, dict):
        raise BoundaryRefused(f"the runtime lock {lock_path()} holds no mapping.")
    return data


def lock_problem(lock: dict, program: str) -> str | None:
    """Why the lock does not prove the boundary for `program`, or None."""
    if program not in (lock.get("boundary") or {}).get("programs", []):
        return f"the runtime lock does not list {program} among its supported programs."
    require = (lock.get("boundary") or {}).get("require") or []
    needed = ("non-root-user", "read-only-rootfs", "cap-drop-all", "private-candidate-volume", "api-only-egress")
    missing = [name for name in needed if name not in require]
    if missing:
        return "the runtime lock's boundary requirements are missing: " + ", ".join(missing)
    for role in ("model", "verifier"):
        image = (lock.get("images") or {}).get(role) or {}
        if not image.get("measured") or not image.get("digest"):
            return f"the {role} image is not measured: no digest stands in the runtime lock; run the isolation gate."
    return None


def image_reference(lock: dict, role: str) -> str:
    """The immutable image identity a launch requires; an unmeasured role refuses."""
    image = (lock.get("images") or {}).get(role) or {}
    reference, digest = image.get("reference"), image.get("digest")
    if not image.get("measured") or not reference or not digest:
        raise BoundaryRefused(f"the {role} image is not measured; no writing call starts (criterion 7).")
    return f"{reference}@{digest}"


# ---------------------------------------------------------------------------
# The endpoint's API profile (spec: Selected API)
# ---------------------------------------------------------------------------


def _is_address(text: str) -> bool:
    try:
        ipaddress.ip_address(text)
    except ValueError:
        return False
    return True


def api_profile_problems(hosts: object) -> list[str]:
    """Every reason the profile is not a list of exact canonical host names."""
    if not isinstance(hosts, list) or not hosts:
        return ["the profile is empty or absent: it approves nothing, the call is refused"]
    problems = []
    for host in hosts:
        if not isinstance(host, str):
            problems.append(f"{host!r} is not a host name")
            continue
        name = host.strip()
        if name != host or name != name.lower() or name.endswith("."):
            problems.append(f"{host!r} is not a lowercased canonical name")
        elif "*" in name or ":" in name or "/" in name or "@" in name:
            problems.append(f"{host!r} carries a wildcard, port, path or userinfo")
        elif _is_address(name):
            problems.append(f"{host!r} is an address literal, not a name")
        elif not _HOST_FORM.fullmatch(name):
            problems.append(f"{host!r} is not a canonical host name")
    return problems


def api_hosts(root: Path, endpoint: str) -> list[str]:
    """The declared `api_hosts` of one endpoint; `[]` when it declares none."""
    try:
        data = yaml.safe_load((root / "model-endpoints.yaml").read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return []
    found = next((e for e in data.get("endpunkte") or [] if isinstance(e, dict) and e.get("name") == endpoint), None)
    if not isinstance(found, dict):
        return []
    hosts = found.get("api_hosts")
    return list(hosts) if isinstance(hosts, list) else []


def profile_problem(root: Path, endpoint: str) -> str | None:
    """Why the endpoint's profile does not approve egress, or None."""
    problems = api_profile_problems(api_hosts(root, endpoint))
    if problems:
        return f"the endpoint {endpoint} declares no qualified API profile ({problems[0]}); the call is refused."
    return None


# ---------------------------------------------------------------------------
# The one selected login (criterion 4)
# ---------------------------------------------------------------------------


@dataclass
class Login:
    """The selected endpoint's login material, and nothing else."""

    endpoint: str
    env_pairs: dict[str, str] = field(default_factory=dict)
    file: Path | None = None
    secret_name: str | None = None

    def problems(self) -> list[str]:
        """What makes this login unfit, or an empty list."""
        found = [
            f"{name} is not a known credential variable" for name in self.env_pairs if name not in CREDENTIAL_ENV_NAMES
        ]
        if self.endpoint in LOGIN_FILES and self.file is None:
            found.append(f"the {self.endpoint} login file is missing")
        if self.endpoint in LOGIN_ENV and not self.env_pairs:
            found.append(f"the {self.endpoint} key is missing")
        return found


def selected_login(endpoint: str, read_secret: Callable[[str], str | None]) -> Login:
    """Only the selected endpoint's login: its key as the CLI's own variables, or its auth file.

    Never a host home, a full sign-in directory, a keychain or an agent
    socket; a missing login refuses the call before it starts.
    """
    if endpoint in LOGIN_ENV:
        secret_name, variables = LOGIN_ENV[endpoint]
        value = read_secret(secret_name)
        if value is None:
            raise BoundaryRefused(
                f"the selected login {secret_name} is not in the secrets file; no writing call starts."
            )
        return Login(endpoint=endpoint, env_pairs={name: value for name in variables}, secret_name=secret_name)
    if endpoint in LOGIN_FILES:
        path = Path(LOGIN_FILES[endpoint]).expanduser()
        if not path.is_file():
            raise BoundaryRefused(
                f"the selected login file {path} does not exist; sign in on the host, then retry "
                "(tools/stage2/README.md)."
            )
        return Login(endpoint=endpoint, file=path)
    raise BoundaryRefused(f"the endpoint {endpoint} has no declared login form; no writing call starts.")


# The interactive sign-in forms a session may carry: the CLI's own state, copied
# into the attempt's disposable login input - never mounted, never read into a
# runner variable (ADR 0012's recorded answer for `session`, plan step 6).
INTERACTIVE_LOGINS = {
    "openai-codex": ("~/.codex/auth.json", ".stage2/codex-home", "CODEX_HOME"),
    "opencode-go": ("~/.pi/agent", ".stage2/pi-home", "PI_CODING_AGENT_DIR"),
}
# A copied sign-in stays small: an interactive login is credentials, not luggage.
LOGIN_COPY_LIMIT = 200
LOGIN_COPY_BYTES = 8 * 1024 * 1024


def interactive_login(endpoint: str, stand_in: bool) -> tuple[dict[str, bytes], dict[str, str]]:
    """The selected session CLI's own sign-in state, as copied input files and its variables.

    Codex signs in from `auth.json`; Pi from its agent directory, the one place
    the recorded session decision keeps. Nothing else - no host home, no other
    provider's state, no agent socket. A missing sign-in state refuses a
    production launch: the attempt has no way to authenticate there. The test
    transport tolerates a missing one, because its stand-in CLIs never sign in.
    """
    if endpoint not in INTERACTIVE_LOGINS:
        raise BoundaryRefused(f"the endpoint {endpoint} has no interactive sign-in form; no session starts.")
    source, home, variable = INTERACTIVE_LOGINS[endpoint]
    origin = Path(source).expanduser()
    if not origin.exists():
        if stand_in:
            return {}, {}
        raise BoundaryRefused(
            f"the interactive sign-in {origin} does not exist; sign in on the host, then start the session "
            "(tools/stage2/README.md)."
        )
    files: dict[str, bytes] = {}
    if origin.is_file():
        files[f"{home}/{origin.name}"] = origin.read_bytes()
    else:
        found = sorted(path for path in origin.rglob("*") if path.is_file() and not path.is_symlink())
        total = 0
        if len(found) > LOGIN_COPY_LIMIT:
            raise BoundaryRefused(f"the interactive sign-in {origin} holds {len(found)} files; no session starts.")
        for path in found:
            data = path.read_bytes()
            total += len(data)
            if total > LOGIN_COPY_BYTES:
                raise BoundaryRefused(
                    f"the interactive sign-in {origin} is larger than a login copy needs; no session starts."
                )
            files[f"{home}/{path.relative_to(origin).as_posix()}"] = data
    return files, {variable: f"{CANDIDATE_WORK}/{home}"}


# ---------------------------------------------------------------------------
# Invocation state (design: "Invocation state"; criterion 22)
# ---------------------------------------------------------------------------


def state_dir() -> Path:
    named = os.environ.get("STAGE2_STATE_DIR")
    if named:
        return Path(named)
    base = os.environ.get("XDG_STATE_HOME")
    return (Path(base) if base else Path.home() / ".local" / "state") / "coding-harness" / "stage2-runtime"


def new_invocation_id() -> str:
    return os.urandom(12).hex()


def _encode(value: object) -> object:
    """JSON-safe state values: bytes travel base64-encoded."""
    if isinstance(value, bytes):
        return {"__bytes_b64__": base64.b64encode(value).decode()}
    if isinstance(value, dict):
        return {str(key): _encode(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_encode(item) for item in value]
    return value


def _decode(value: object) -> object:
    if isinstance(value, dict):
        if set(value) == {"__bytes_b64__"}:
            return base64.b64decode(str(value["__bytes_b64__"]))
        return {str(key): _decode(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_decode(item) for item in value]
    return value


@dataclass
class InvocationState:
    """What one invocation recorded about itself - never a login value."""

    id: str
    verb: str
    endpoint: str
    model: str
    baseline: str
    attempt: int = 1
    phase: str = "launch"
    resources: list[dict[str, str]] = field(default_factory=list)
    journal: list[dict[str, object]] = field(default_factory=list)
    cleanup_pending: str | None = None
    detail: dict[str, object] = field(default_factory=dict)

    def label(self, kind: str) -> str:
        return f"stage2-{self.id[:12]}-{kind}"

    def record(self, kind: str, name: str) -> dict[str, str]:
        entry = {"kind": kind, "name": name, "invocation": self.id}
        self.resources.append(entry)
        return entry

    @property
    def path(self) -> Path:
        return state_dir() / f"{self.id}.json"

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {key: _encode(value) for key, value in self.__dict__.items()}
        self.path.write_text(json.dumps(payload, indent=1, sort_keys=True), encoding="utf-8")

    @classmethod
    def load(cls, invocation_id: str) -> InvocationState:
        path = state_dir() / f"{invocation_id}.json"
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise BoundaryRefused(f"the invocation state {path} cannot be read: {error}") from None
        if not isinstance(data, dict) or data.get("id") != invocation_id:
            raise BoundaryRefused(f"the invocation state {path} does not name {invocation_id}.")
        known = set(cls.__dataclass_fields__)  # type: ignore[attr-defined]
        decoded = {str(key): _decode(value) for key, value in data.items() if key in known}
        return cls(**decoded)  # type: ignore[arg-type]

    def delete(self) -> None:
        try:
            self.path.unlink()
        except OSError:
            pass


def reconcile_pending(runtime: Runtime) -> list[str]:
    """Retry the cleanups earlier invocations could not finish; return what still stands.

    Only resources whose recorded `invocation` matches their state file's id
    are touched - never an unrelated container or volume, and never a global
    prune.
    """
    still: list[str] = []
    if not state_dir().is_dir():
        return still
    for path in sorted(state_dir().glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            still.append(path.name)
            continue
        if not isinstance(data, dict) or not data.get("cleanup_pending"):
            continue
        owner = str(data.get("id", ""))
        resources = [r for r in data.get("resources") or [] if isinstance(r, dict) and r.get("invocation") == owner]
        leftover = runtime.remove_resources(resources)
        if leftover:
            still.append(owner)
        else:
            path.unlink(missing_ok=True)
    return still


def cleanup_state(state: InvocationState, runtime: Runtime) -> bool:
    """Remove the invocation's recorded resources; say so when that does not finish."""
    leftover = runtime.remove_resources(state.resources)
    if leftover:
        state.cleanup_pending = "resources remain: " + ", ".join(leftover)
        state.save()
        return False
    state.delete()
    return True


# ---------------------------------------------------------------------------
# Runtime adapters. Each translates the same operations into its program's
# argument vectors; the argv builders are pure, so tests inspect confinement
# without running a container, and an adapter that cannot express a required
# boundary refuses instead of launching weaker.
# ---------------------------------------------------------------------------


@dataclass
class RunRequest:
    """One `run` of a container: the inner argv, its environment and its confinement."""

    image: str
    argv: list[str]
    env: dict[str, str]
    volumes: list[tuple[str, str, bool]]  # (volume, container path, read-only)
    networks: list[str]  # empty means no network at all
    user: str = NON_ROOT
    timeout: float | None = None
    stdin: bytes | None = None
    cwd: str = CANDIDATE_WORK
    attached: bool = False  # an interactive lifetime shares the Terminal's stdio
    transparent_cwd: Path | None = None  # the test transport's host directory
    detach: bool = False  # a long-running helper (the egress proxy) starts detached
    name: str | None = None  # the container name a detached helper is recorded under


def base_confinement_argv(request: RunRequest) -> list[str]:
    """The confinement every backend must express: non-root, all capabilities dropped."""
    return ["--user", request.user, "--cap-drop", "ALL", "--security-opt", "no-new-privileges"]


def base_mount_argv(request: RunRequest) -> list[str]:
    argv: list[str] = []
    for volume, path, read_only in request.volumes:
        argv += ["-v", f"{volume}:{path}" + (":ro" if read_only else "")]
    return argv


def _child_argv(
    program_argv: list[str], stdin: bytes | None = None, timeout: float | None = None
) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            program_argv, input=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=timeout
        )
    except FileNotFoundError as error:
        raise BoundaryRefused(f"{program_argv[0]} could not be started: {error}") from None
    except subprocess.TimeoutExpired:
        raise BoundaryRefused(f"{program_argv[0]} was stopped by its limit") from None


class Runtime:
    """The operations every backend provides. Names are per-invocation labels."""

    name = "abstract"

    def create_volume(self, state: InvocationState, kind: str) -> str:
        raise NotImplementedError

    def create_network(self, state: InvocationState, kind: str, *, internal: bool) -> str:
        raise NotImplementedError

    def populate(self, state: InvocationState, volume: str, tar_bytes: bytes) -> None:
        raise NotImplementedError

    def run_argv(self, request: RunRequest, lock: dict) -> list[str]:
        raise NotImplementedError

    def run(self, request: RunRequest) -> subprocess.CompletedProcess:
        raise NotImplementedError

    def start_detached(self, request: RunRequest) -> subprocess.CompletedProcess:
        """Start a long-running helper and return at once; the name is recorded by the caller."""
        raise NotImplementedError

    def export_volume(self, state: InvocationState, volume: str) -> bytes:
        """The volume's content as a tar archive, read by the trusted exporter."""
        raise NotImplementedError

    def remove_resources(self, resources: list[dict[str, str]]) -> list[str]:
        """Remove exactly these recorded resources; return the names that remain."""
        raise NotImplementedError


class PodmanRuntime(Runtime):
    """Rootless Podman: the default backend, and the one the live probes measure."""

    name = "podman"

    def __init__(self, executable: str) -> None:
        self.executable = executable

    def create_volume(self, state: InvocationState, kind: str) -> str:
        name = state.label(kind)
        _child_argv([self.executable, "volume", "create", name])
        state.record("volume", name)
        return name

    def create_network(self, state: InvocationState, kind: str, *, internal: bool) -> str:
        name = state.label(kind)
        argv = [self.executable, "network", "create"]
        if internal:
            argv.append("--internal")
        argv.append(name)
        _child_argv(argv)
        state.record("network", name)
        return name

    def run_argv(self, request: RunRequest, lock: dict) -> list[str]:
        require = (lock.get("boundary") or {}).get("require") or []
        argv = [self.executable, "run", "--rm"]
        if request.detach:
            argv.append("--detach")
        if request.name:
            argv += ["--name", request.name]
        argv += ["--network", ",".join(request.networks) if request.networks else "none"]
        argv += base_confinement_argv(request)
        if "read-only-rootfs" in require:
            argv.append("--read-only")
        argv += base_mount_argv(request)
        for name, value in request.env.items():
            argv += ["--env", f"{name}={value}"]
        if request.cwd:
            argv += ["--workdir", request.cwd]
        if request.attached:
            argv += ["-i", "-t"]
        argv += [request.image, "--", *request.argv]
        return argv

    def run(self, request: RunRequest) -> subprocess.CompletedProcess:
        return _child_argv(self.run_argv(request, runtime_lock()), request.stdin, request.timeout)

    def start_detached(self, request: RunRequest) -> subprocess.CompletedProcess:
        return _child_argv(self.run_argv(request, runtime_lock()))

    def populate(self, state: InvocationState, volume: str, tar_bytes: bytes) -> None:
        image = image_reference(runtime_lock(), "model")
        argv = [
            self.executable,
            "run",
            "--rm",
            "--network",
            "none",
            "-v",
            f"{volume}:{CANDIDATE_WORK}",
            image,
            "--",
            "tar",
            "-x",
            "-p",
            "-C",
            CANDIDATE_WORK,
        ]
        _child_argv(argv, tar_bytes)

    def export_volume(self, state: InvocationState, volume: str) -> bytes:
        image = image_reference(runtime_lock(), "model")
        argv = [
            self.executable,
            "run",
            "--rm",
            "--network",
            "none",
            "-v",
            f"{volume}:{CANDIDATE_WORK}:ro",
            image,
            "--",
            "tar",
            "-cf",
            "-",
            "-C",
            CANDIDATE_WORK,
            ".",
        ]
        return _child_argv(argv).stdout

    def remove_resources(self, resources: list[dict[str, str]]) -> list[str]:
        leftover = []
        for entry in resources:
            kind, name = entry.get("kind"), entry.get("name")
            if kind == "volume":
                done = _child_argv([self.executable, "volume", "rm", "--force", str(name)])
            elif kind == "network":
                done = _child_argv([self.executable, "network", "rm", str(name)])
            elif kind == "container":
                done = _child_argv([self.executable, "rm", "--force", str(name)])
            else:
                continue
            if done.returncode != 0:
                leftover.append(str(name))
        return leftover


class DockerRuntime(PodmanRuntime):
    """Docker: the same operations in its own argument spelling, the same boundary."""

    name = "docker"

    def run_argv(self, request: RunRequest, lock: dict) -> list[str]:
        require = (lock.get("boundary") or {}).get("require") or []
        argv = [self.executable, "run", "--rm"]
        if request.detach:
            argv.append("--detach")
        if request.name:
            argv += ["--name", request.name]
        argv += ["--network", ",".join(request.networks) if request.networks else "none"]
        argv += base_confinement_argv(request)
        if "read-only-rootfs" in require:
            argv += ["--read-only", "--tmpfs", "/tmp:rw,size=268435456,noexec"]
        argv += base_mount_argv(request)
        for name, value in request.env.items():
            argv += ["--env", f"{name}={value}"]
        if request.cwd:
            argv += ["--workdir", request.cwd]
        if request.attached:
            argv += ["-i", "-t"]
        argv += [request.image, "--", *request.argv]
        return argv


class AppleContainerRuntime(Runtime):
    """Apple `container`: its own argument vectors, refusing what it cannot express."""

    name = "container"

    def __init__(self, executable: str) -> None:
        self.executable = executable

    def create_volume(self, state: InvocationState, kind: str) -> str:
        raise BoundaryRefused(
            "the Apple container adapter cannot yet express a private named volume; "
            "the boundary is unproven for it and the call is refused."
        )

    def create_network(self, state: InvocationState, kind: str, *, internal: bool) -> str:
        if internal:
            raise BoundaryRefused(
                "the Apple container adapter cannot express an internal network without an "
                "outbound route; the boundary is unproven for it and the call is refused."
            )
        name = state.label(kind)
        _child_argv([self.executable, "network", "create", name])
        state.record("network", name)
        return name

    def run_argv(self, request: RunRequest, lock: dict) -> list[str]:
        if not request.volumes:
            raise BoundaryRefused("the Apple container adapter has no volume mapping; the call is refused.")
        argv = [self.executable, "run", "--rm", *base_confinement_argv(request)]
        if request.detach:
            raise BoundaryRefused(
                "the Apple container adapter cannot start the egress helper detached; the call is refused."
            )
        argv += ["--network", request.networks[0] if request.networks else "none"]
        argv += base_mount_argv(request)
        for name, value in request.env.items():
            argv += ["--env", f"{name}={value}"]
        argv += [request.image, "--", *request.argv]
        return argv

    def run(self, request: RunRequest) -> subprocess.CompletedProcess:
        return _child_argv(self.run_argv(request, runtime_lock()), request.stdin, request.timeout)

    def populate(self, state: InvocationState, volume: str, tar_bytes: bytes) -> None:
        raise BoundaryRefused("the Apple container adapter cannot populate a private volume; the call is refused.")

    def export_volume(self, state: InvocationState, volume: str) -> bytes:
        raise BoundaryRefused("the Apple container adapter cannot export a private volume; the call is refused.")

    def remove_resources(self, resources: list[dict[str, str]]) -> list[str]:
        leftover = []
        for entry in resources:
            if entry.get("kind") == "network":
                done = _child_argv([self.executable, "network", "rm", str(entry.get("name"))])
                if done.returncode != 0:
                    leftover.append(str(entry.get("name")))
        return leftover


def choose_runtime() -> Runtime:
    """The runtime the setting names, or the stand-in the tests recorded."""
    stand_in = os.environ.get("STAGE2_RUNTIME_STAND_IN")
    if stand_in:
        return StandInRuntime(Path(stand_in))
    kind, executable = selected_program()
    if kind == "podman":
        return PodmanRuntime(executable)
    if kind == "docker":
        return DockerRuntime(executable)
    return AppleContainerRuntime(executable)


class StandInRuntime(Runtime):
    """The test transport: record every operation, execute the writer transparently.

    Production never selects it: `STAGE2_RUNTIME_STAND_IN` is a test variable
    the World fixtures set. The live probes measure the real adapters, never
    this one.
    """

    name = "stand-in"

    def __init__(self, directory: Path) -> None:
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)
        self.log = self.directory / "runtime-calls.jsonl"

    def _record(self, entry: dict[str, object]) -> None:
        with self.log.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, sort_keys=True) + "\n")

    def create_volume(self, state: InvocationState, kind: str) -> str:
        name = state.label(kind)
        self._record({"op": "volume create", "name": name, "invocation": state.id})
        state.record("volume", name)
        return name

    def create_network(self, state: InvocationState, kind: str, *, internal: bool) -> str:
        name = state.label(kind)
        self._record({"op": "network create", "name": name, "internal": internal, "invocation": state.id})
        state.record("network", name)
        return name

    def populate(self, state: InvocationState, volume: str, tar_bytes: bytes) -> None:
        self._record({"op": "populate", "volume": volume, "bytes": len(tar_bytes), "invocation": state.id})

    def export_volume(self, state: InvocationState, volume: str) -> bytes:
        self._record({"op": "export", "volume": volume, "invocation": state.id})
        return b""

    def remove_resources(self, resources: list[dict[str, str]]) -> list[str]:
        self._record({"op": "remove", "resources": [dict(r) for r in resources]})
        return []

    def start_detached(self, request: RunRequest) -> subprocess.CompletedProcess:
        self._record(
            {
                "op": "start-detached",
                "argv": request.argv,
                "name": request.name,
                "networks": request.networks,
                "volumes": [list(volume) for volume in request.volumes],
                "image": request.image,
            }
        )
        return subprocess.CompletedProcess(request.argv, 0, "", "")

    def run(self, request: RunRequest) -> subprocess.CompletedProcess:
        """Execute the inner command with the supervisor-constructed environment.

        The candidate is the host directory `transparent_cwd`: the writes land
        where the runner's snapshot mathematics already reads them, which is
        what makes the stand-in transparent for the suite. A failure to start
        or a stop by the limit raises `AttemptCallFailed`, exactly as a real
        adapter's failed child would.
        """
        argv = request.argv[1:] if request.argv and request.argv[0] == "--" else list(request.argv)
        cwd = request.transparent_cwd or Path.cwd()
        self._record(
            {
                "op": "run",
                "argv": argv,
                "env": dict(request.env),
                "cwd": str(cwd),
                "volumes": [list(volume) for volume in request.volumes],
                "networks": request.networks,
                "image": request.image,
                "user": request.user,
            }
        )
        try:
            if request.attached:
                done = subprocess.run(argv, cwd=cwd, env=request.env, check=False, timeout=request.timeout)
                return subprocess.CompletedProcess(argv, done.returncode, "", "")
            return subprocess.run(
                argv,
                cwd=cwd,
                env=request.env,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                errors="replace",
                check=False,
                timeout=request.timeout,
            )
        except subprocess.TimeoutExpired as error:
            raise AttemptCallFailed(f"{argv[0]} was stopped by its limit", what="its limit") from error
        except OSError as error:
            raise AttemptCallFailed(f"{argv[0]} could not be started: {error}") from error


# ---------------------------------------------------------------------------
# The candidate: trusted inputs, an independent Git, no host mount
# ---------------------------------------------------------------------------


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def _rev_of(root: Path, ref: str) -> str:
    done = _git(root, "rev-parse", ref)
    if done.returncode != 0:
        raise BoundaryRefused(f"the ref {ref} could not be read: {done.stderr.decode(errors='replace')[:200]}")
    return done.stdout.decode().strip()


def _ref_exists(root: Path, ref: str) -> bool:
    return _git(root, "rev-parse", "--verify", "--quiet", ref).returncode == 0


def private_git_snapshot(root: Path, baseline: str, dest: Path, origin_ref: str = "origin/main") -> None:
    """A self-contained Git directory at `baseline`, without the host's metadata.

    `--no-local --no-hardlinks` copies the objects; the fresh clone carries no
    hooks, no source configuration, no alternates and no credential helper.
    The remote is removed so the candidate metadata holds no host path, and
    the baseline and `origin/main` stay as the refs the gates read.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    done = _git(root, "clone", "--no-local", "--no-hardlinks", "--no-checkout", "--quiet", str(root), str(dest))
    if done.returncode != 0:
        raise BoundaryRefused(
            f"the private Git snapshot could not be built: {done.stderr.decode(errors='replace')[:200]}"
        )
    steps: list[tuple[str, ...]] = [
        ("remote", "remove", "origin"),
        ("checkout", "--detach", "--quiet", baseline),
    ]
    if _ref_exists(root, origin_ref):
        steps.append(("update-ref", "refs/remotes/origin/main", _rev_of(root, origin_ref)))
    steps += [
        ("config", "--unset-all", "credential.helper"),
        ("config", "core.hooksPath", "/dev/null"),
        ("config", "commit.gpgsign", "false"),
        ("config", "gc.auto", "0"),
    ]
    for args in steps:
        _git(dest, *args)
    hooks = dest / "hooks"
    if hooks.is_dir():
        shutil.rmtree(hooks, ignore_errors=True)


def _tar_bytes(builder: Callable[[tarfile.TarFile], None]) -> bytes:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w") as target:
        builder(target)
    return buffer.getvalue()


def _add_bytes(target: tarfile.TarFile, name: str, data: bytes, mode: int = 0o644) -> None:
    info = tarfile.TarInfo(name=name)
    info.size = len(data)
    info.mode = mode
    info.mtime = 0
    target.addfile(info, io.BytesIO(data))


def worktree_tar(root: Path, baseline: str, permitted: dict[Path, bytes] | None = None) -> bytes:
    """The candidate's worktree bytes: the baseline snapshot plus permitted evidence.

    The tracked tree comes from `git archive` of the baseline commit - trusted
    bytes, not a working-tree read. `.beads/` stays out: the live tracker
    database is never a passed input; a gate that needs the tracker gets the
    fresh render the runner prepared. Uncommitted content reaches the
    candidate only through `permitted` (the run baseline's findings evidence).
    """
    done = subprocess.run(
        ["git", "-C", str(root), "archive", "--format=tar", baseline],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if done.returncode != 0:
        raise BoundaryRefused(f"the baseline snapshot could not be built: {done.stderr.decode(errors='replace')[:200]}")

    def build(target: tarfile.TarFile) -> None:
        with tarfile.open(fileobj=io.BytesIO(done.stdout), mode="r:") as source:
            for member in source:
                if member.name == ".beads" or member.name.startswith(".beads/"):
                    continue
                fileobj = source.extractfile(member) if member.isreg() else None
                target.addfile(member, fileobj)
        for relative, data in sorted((permitted or {}).items()):
            _add_bytes(target, relative.as_posix(), data)

    return _tar_bytes(build)


def git_tar(root: Path, baseline: str) -> bytes:
    """A tar of the private Git metadata (a fresh snapshot's content), for its own volume."""
    with tempfile.TemporaryDirectory(prefix="stage2-git-") as tmp:
        private_git_snapshot(root, baseline, Path(tmp) / "git")
        base = Path(tmp) / "git"

        def build(target: tarfile.TarFile) -> None:
            for path in sorted(base.rglob("*")):
                if path.is_dir():
                    continue
                info = tarfile.TarInfo(name=f"git/{path.relative_to(base).as_posix()}")
                info.size = path.stat().st_size
                info.mode = 0o444
                info.mtime = 0
                target.addfile(info, path.open("rb"))

        return _tar_bytes(build)


def input_files_tar(files: dict[str, bytes]) -> bytes:
    """A tar of the runner's input files (prompt, render, config), for their own volume."""

    def build(target: tarfile.TarFile) -> None:
        for name, data in sorted(files.items()):
            _add_bytes(target, name, data)

    return _tar_bytes(build)


def merge_tars(candidate: bytes, inputs: bytes) -> bytes:
    """One tar holding both volumes' entries, the inputs winning on a name.

    The input volume mounts at the candidate's `.stage2`, so a writer's answer
    and its login copies land on the *input* volume while the trusted export
    reads the candidate: the launcher merges both exports into one map so the
    answer survives (ADR 0018; found while writing the isolation probes).
    """

    def build(target: tarfile.TarFile) -> None:
        for payload in (inputs, candidate):
            with tarfile.open(fileobj=io.BytesIO(payload), mode="r:") as source:
                for member in source.getmembers():
                    extracted = source.extractfile(member)
                    data = extracted.read() if extracted is not None else b""
                    target.addfile(member, io.BytesIO(data) if member.isfile() else None)

    return _tar_bytes(build)


# ---------------------------------------------------------------------------
# Export, validation, publication (criteria 11, 14, 15, 16)
# ---------------------------------------------------------------------------


@dataclass
class DeltaEntry:
    path: Path
    data: bytes | None  # None names an explicit deletion
    mode: int = 0o644


@dataclass
class CandidateDelta:
    """The typed, relative result: entries, the model's own paths, the derived ones."""

    entries: list[DeltaEntry] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)
    model_paths: list[Path] = field(default_factory=list)
    derived_paths: list[Path] = field(default_factory=list)
    transparent: bool = False

    def paths(self) -> list[Path]:
        return [entry.path for entry in self.entries]


def _tar_file_map(archive: bytes, *, noise: bool = False) -> tuple[dict[Path, bytes], list[str]]:
    """Read a tar into {relative path: bytes}; refuse non-regular and escaping members.

    Directory entries carry no content and are skipped: publication creates
    the parent directories an entry needs, and ordinary new directories stay
    allowed (criterion 11). `noise` drops the verifier's own tooling paths
    before any link or content check sees them - they are the runner's, not
    the model's, and a wrapper symlink of `.venv/bin` must not refuse an
    otherwise publishable candidate.
    """
    files: dict[Path, bytes] = {}
    problems: list[str] = []
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as source:
        for member in source:
            relative = Path(member.name)
            if relative.is_absolute() or ".." in relative.parts:
                problems.append(f"{member.name}: an escaping path does not publish")
                continue
            if noise and _is_verifier_noise(member.name):
                continue
            if member.isdir():
                continue
            if member.issym() or member.islnk() or member.isdev():
                problems.append(f"{member.name}: a link or special file does not publish")
                continue
            if not member.isreg():
                continue
            if relative in files:
                problems.append(f"{member.name}: a duplicate path does not publish")
                continue
            extracted = source.extractfile(member)
            files[relative] = extracted.read() if extracted else b""
    return files, problems


def diff_candidate(
    baseline_archive: bytes,
    candidate_archive: bytes,
    *,
    derived: frozenset[str] = frozenset(),
    binary_ok: frozenset[str] = frozenset(),
) -> CandidateDelta:
    """The typed relative delta between the baseline snapshot and the stopped candidate.

    Changed and new regular files become entries; a baseline file absent from
    the candidate becomes an explicit deletion. Runner-owned paths
    (`.stage2/`, `.git/`) never publish. Content that is not a text file's -
    and that the baseline does not already carry at the same path - is
    refused, so a special file cannot masquerade as a document.
    """
    baseline_files, baseline_problems = _tar_file_map(baseline_archive)
    candidate_files, candidate_problems = _tar_file_map(candidate_archive, noise=True)
    delta = CandidateDelta(problems=[*baseline_problems, *candidate_problems])
    all_paths: set[Path] = set(baseline_files) | set(candidate_files)
    for relative in sorted(all_paths):
        if any(relative.as_posix().startswith(prefix) for prefix in RUNNER_PREFIXES):
            continue
        old, new = baseline_files.get(relative), candidate_files.get(relative)
        if new is None:
            if old is not None:
                # A deletion is an owned change like any other: it is
                # classified, so the evidence names it and the verifier's own
                # cleanup of a path can never read as the model's work.
                entry = DeltaEntry(path=relative, data=None)
                delta.entries.append(entry)
                (delta.derived_paths if relative.as_posix() in derived else delta.model_paths).append(relative)
            continue
        if new == old:
            continue
        if b"\x00" in new and relative.as_posix() not in binary_ok and b"\x00" not in (old or b""):
            delta.problems.append(f"{relative.as_posix()}: content is not a regular file's")
            continue
        entry = DeltaEntry(path=relative, data=new, mode=0o644)
        delta.entries.append(entry)
        (delta.derived_paths if relative.as_posix() in derived else delta.model_paths).append(relative)
    # Topology swaps are refused before any host write (criterion 11): a file
    # must not replace a directory the baseline fills, and a directory must
    # not replace a file the baseline carries. Ordinary new directories and
    # files below existing ones stay allowed.
    baseline_dirs: set[Path] = set()
    for relative in baseline_files:
        baseline_dirs.update(relative.parents)
    for entry in delta.entries:
        if entry.data is None:
            continue
        if entry.path in baseline_dirs and entry.path not in baseline_files:
            delta.problems.append(f"{entry.path.as_posix()}: a file replacing a directory does not publish")
        if any(parent in baseline_files for parent in entry.path.parents):
            delta.problems.append(f"{entry.path.as_posix()}: a directory replacing a file does not publish")
    return delta


def validate_delta(delta: CandidateDelta) -> list[str]:
    """The publication validator: the delta's own problems, restated for the refusal."""
    return list(delta.problems)


def compose_candidate(baseline_archive: bytes, delta: CandidateDelta) -> bytes:
    """The candidate the verifier sees: trusted baseline bytes plus the validated delta.

    Nothing is extracted from a stopped candidate's archive here: the entries
    were typed and validated by `diff_candidate`, and composition applies
    exactly them to the trusted snapshot. A delta that still carries problems
    refuses instead of composing.
    """
    problems = validate_delta(delta)
    if problems:
        raise BoundaryRefused("the candidate does not compose: " + "; ".join(problems[:3]))
    files, _ = _tar_file_map(baseline_archive)
    for entry in delta.entries:
        if entry.data is None:
            files.pop(entry.path, None)
        else:
            files[entry.path] = entry.data

    def build(target: tarfile.TarFile) -> None:
        for relative, data in sorted(files.items()):
            _add_bytes(target, relative.as_posix(), data)

    return _tar_bytes(build)


@dataclass
class JournalEntry:
    path: Path
    had_old: bool
    old_bytes: bytes | None
    old_mode: int
    old_was_dir: bool
    written: bytes | None  # what this publication left there; None names a deletion


class Journal:
    """The publication journal of one invocation: what it overwrote, and what it wrote."""

    def __init__(self, state: InvocationState) -> None:
        self.state = state

    def add(self, entry: JournalEntry) -> None:
        self.state.journal.append(
            {
                "path": entry.path.as_posix(),
                "had_old": entry.had_old,
                "old_was_dir": entry.old_was_dir,
                "old_mode": entry.old_mode,
                "written": None if entry.written is None else base64.b64encode(entry.written).decode(),
            }
        )


def _materialise(root: Path, entry: DeltaEntry) -> JournalEntry:
    """Write one validated entry without following links; journal what it replaced."""
    path = root / entry.path
    old_bytes: bytes | None = None
    old_mode = 0
    old_was_dir = path.is_dir() and not path.is_symlink()
    had_old = path.exists() or path.is_symlink()
    if had_old and not old_was_dir:
        try:
            old_bytes = path.read_bytes()
            old_mode = path.stat().st_mode & 0o777
        except OSError:
            old_bytes = None
    if entry.data is None:
        if old_was_dir:
            shutil.rmtree(path)
        elif had_old:
            path.unlink()
        return JournalEntry(path, had_old, old_bytes, old_mode, old_was_dir, None)
    if old_was_dir:
        raise BoundaryRefused(f"{entry.path.as_posix()}: publication refuses to replace a directory with a file")
    if had_old:
        path.unlink()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(entry.data)
    path.chmod(entry.mode or 0o644)
    return JournalEntry(path, had_old, old_bytes, old_mode, old_was_dir, entry.data)


def publish_delta(
    delta: CandidateDelta,
    root: Path,
    state: InvocationState,
    *,
    only: set[Path] | None = None,
    scan: Callable[[Path, bytes], list[str]] | None = None,
) -> list[JournalEntry]:
    """Apply the validated entries to the host worktree, journalled, without following links.

    `scan` is the credential scan of the exact bytes: a finding refuses the
    publication before the first host write, so unscanned bytes never land.
    """
    problems = validate_delta(delta)
    if problems:
        raise BoundaryRefused("the candidate's publication was rejected: " + "; ".join(problems[:3]))
    selected = [entry for entry in delta.entries if only is None or entry.path in only]
    if scan is not None:
        for entry in selected:
            if entry.data is not None:
                findings = scan(entry.path, entry.data)
                if findings:
                    raise BoundaryRefused(
                        f"the candidate's publication was rejected: {entry.path.as_posix()}: {findings[0]}"
                    )
    applied: list[JournalEntry] = []
    journal = Journal(state)
    try:
        for entry in selected:
            journal_entry = _materialise(root, entry)
            journal.add(journal_entry)
            applied.append(journal_entry)
            # Saved after every entry: an interruption leaves the journal on
            # disk, so the next invocation can reconcile exactly these writes.
            state.save()
    except OSError as error:
        undone = undo_owned(root, applied, state.baseline)
        raise BoundaryRefused(
            f"the publication failed part way ({error}); the runner undid its own writes "
            f"({undone or 'nothing to undo'})."
        ) from None
    state.save()
    return applied


def undo_owned(root: Path, applied: list[JournalEntry], baseline: str) -> str:
    """Undo exactly the still-matching writes of this publication, nothing else.

    An entry whose file no longer holds the bytes this publication wrote is
    left alone - an intervening change is never overwritten - and no ref is
    touched; the index entries of the undone paths go back to HEAD.
    """
    undone: list[str] = []
    for entry in reversed(applied):
        try:
            current: bytes | None = entry.path.read_bytes()
        except OSError:
            current = None
        is_file = entry.path.is_file() and not entry.path.is_symlink()
        if entry.written is not None:
            # This publication wrote the file: undo it only if it still holds
            # exactly those bytes; an intervening change is never overwritten.
            if not is_file or current != entry.written:
                continue
            entry.path.unlink()
        else:
            # This publication deleted the file: undo the deletion only if the
            # path is still absent; a recreated file is another writer's now.
            if entry.path.exists() or entry.path.is_symlink():
                continue
        if entry.had_old and entry.old_bytes is not None:
            entry.path.parent.mkdir(parents=True, exist_ok=True)
            entry.path.write_bytes(entry.old_bytes)
            entry.path.chmod(entry.old_mode or 0o644)
        else:
            parent = entry.path.parent
            while parent not in (root, parent.parent):
                try:
                    parent.rmdir()
                except OSError:
                    break
                parent = parent.parent
        undone.append(entry.path.as_posix())
    if undone:
        subprocess.run(
            ["git", "-C", str(root), "restore", "--staged", "--", *undone],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    return ", ".join(undone)


# ---------------------------------------------------------------------------
# Host-state equality for the invocation lock (criterion 15)
# ---------------------------------------------------------------------------


def host_state(root: Path, keep: frozenset[Path] | set[Path] = frozenset()) -> tuple[str, str]:
    """The identity a publication must find on return: HEAD and the worktree tree hash.

    `keep` names the evidence paths the runner itself may still write while
    the attempt runs - `findings.md`, whose blocks are the intentional
    exception a failed run leaves behind. They are dropped from the tree hash,
    so the runner's own evidence never reads as an intervening change; every
    other path counts.
    """
    head = _rev_of(root, "HEAD")
    saved_index = os.environ.get("GIT_INDEX_FILE")
    tmp_index = tempfile.NamedTemporaryFile(prefix="stage2-state-", suffix=".index", delete=False)
    tmp_index.close()
    try:
        os.environ["GIT_INDEX_FILE"] = tmp_index.name
        _git(root, "read-tree", "HEAD")
        _git(root, "add", "-A")
        for relative in sorted(keep, key=lambda path: path.as_posix()):
            _git(root, "rm", "--cached", "--quiet", "--", relative.as_posix())
        written = _git(root, "write-tree")
        tree = written.stdout.decode().strip() if written.returncode == 0 else ""
    finally:
        if saved_index is None:
            os.environ.pop("GIT_INDEX_FILE", None)
        else:
            os.environ["GIT_INDEX_FILE"] = saved_index
        os.unlink(tmp_index.name)
    return head, tree


def assert_host_state(root: Path, expected: tuple[str, str], keep: frozenset[Path] | set[Path] = frozenset()) -> None:
    """Refuse when the host baseline changed while the attempt ran (criterion 15)."""
    if host_state(root, keep) != expected:
        raise BoundaryRefused(
            "the host worktree changed while the attempt ran; publication refuses to overwrite the intervening work."
        )


# ---------------------------------------------------------------------------
# The writer launch (criteria 1, 2, 3, 7, 8, 9)
# ---------------------------------------------------------------------------


@dataclass
class WriterSpec:
    """What one writing attempt is told to do, and what it may see.

    `inner_command` and `inner_env` may carry the placeholder tokens; the
    supervisor substitutes the host staging paths (test transport) or the
    candidate paths (production) and materialises the input files. The login
    is not part of the spec: the supervisor reads only the selected endpoint's
    material at launch time, so the spec never carries a secret.
    """

    verb: str
    change: str
    endpoint: str
    model: str
    prompt: str
    inner_command: list[str]
    inner_env: dict[str, str]
    baseline: str
    attempt: int = 1
    permitted: dict[Path, bytes] = field(default_factory=dict)
    input_files: dict[str, bytes] = field(default_factory=dict)
    timeout: float | None = None
    limit_name: str = "its time limit"
    derived_paths: frozenset[str] = frozenset()
    binary_ok: frozenset[str] = frozenset()
    # An interactive lifetime shares the Terminal's stdio, and it signs in
    # with the maintainer's own interactive sign-in state - never a runner
    # secret (plan step 6, ADR 0012's recorded answer).
    attached: bool = False
    interactive_login: bool = False


@dataclass
class WriterRun:
    """A stopped writer and its validated result - or the refusal's evidence."""

    done: subprocess.CompletedProcess
    runtime: Runtime
    state: InvocationState
    delta: CandidateDelta
    answer_path: Path | None = None
    transparent: bool = False
    diagnostics: list[str] = field(default_factory=list)
    # The trusted baseline snapshot this attempt was built from (production
    # only): the verifier composes its candidate from these bytes and the
    # validated delta, never from a second export.
    baseline_archive: bytes | None = None

    def publish(self, root: Path, *, only: set[Path] | None = None, scan=None) -> list[JournalEntry]:
        if self.transparent or self.delta.transparent:
            return []
        return publish_delta(self.delta, root, self.state, only=only, scan=scan)

    def discard(self) -> None:
        cleanup_state(self.state, self.runtime)


def _stand_in_dir() -> Path | None:
    named = os.environ.get("STAGE2_RUNTIME_STAND_IN")
    return Path(named) if named else None


def _read_secret(secret_name: str) -> str | None:
    """Read one secret line at call time through the runner's own reader."""
    from stage2 import read_secret  # local import: the runner stays the only secrets reader

    return read_secret(secret_name)


def prepare_render(root: Path) -> bytes:
    """The fresh tracker render a gate may need, made at the allowed access point.

    The render is one file, made by `scripts/bead_render.py` on the host and
    copied into the candidate's inputs; its bytes join the outgoing leak scan
    with the prompt. In the test transport nothing is rendered: the fixtures
    preset the render themselves. A render that cannot be made is a refusal -
    a gate without its input must fail the launch, not run unbounded.
    """
    if _stand_in_dir() is not None:
        return b""
    done = subprocess.run(
        [sys.executable, "scripts/bead_render.py"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if done.returncode != 0:
        raise BoundaryRefused(
            "the fresh tracker render could not be prepared: " + done.stderr.decode(errors="replace")[:200]
        )
    named = done.stdout.decode(errors="replace").splitlines()
    if not named:
        raise BoundaryRefused("the fresh tracker render could not be prepared: no path was reported.")
    try:
        return Path(named[0].split("\t")[0]).read_bytes()
    except OSError as error:
        raise BoundaryRefused(f"the fresh tracker render could not be read: {error}") from None


def preflight(root: Path, endpoint: str) -> tuple[Runtime, dict]:
    """Everything that must hold before a writer starts; every refusal happens here.

    The test transport skips the production lock and profile checks (the suite
    has neither a measured image nor a declared profile), but the program
    setting is validated in both worlds: an unknown backend never silently
    becomes the stand-in.
    """
    problem = program_problem(program_setting())
    if problem:
        raise BoundaryRefused(problem)
    runtime = choose_runtime()
    if _stand_in_dir() is None:
        kind, _ = selected_program()
        lock = runtime_lock()
        problem = lock_problem(lock, kind)
        if problem:
            raise BoundaryRefused(problem)
        problem = profile_problem(root, endpoint)
        if problem:
            raise BoundaryRefused(problem)
        reconcile_pending(runtime)
        return runtime, lock
    return runtime, runtime_lock()


def _staging(state: InvocationState) -> Path:
    staging = state_dir() / state.id
    staging.mkdir(parents=True, exist_ok=True)
    return staging


def _targets(state: InvocationState, stand_in: bool) -> tuple[dict[str, str], Path]:
    """Where each placeholder points: host staging paths (test) or candidate paths (production)."""
    staging = _staging(state)
    if stand_in:
        return (
            {
                PROMPT_PLACEHOLDER: str(staging / "prompt.md"),
                ANSWER_PLACEHOLDER: str(staging / "answer.md"),
                RENDER_PLACEHOLDER: str(staging / "render.md"),
                CONFIG_PLACEHOLDER: str(staging / "config"),
            },
            staging,
        )
    return (
        {
            PROMPT_PLACEHOLDER: CANDIDATE_PROMPT,
            ANSWER_PLACEHOLDER: CANDIDATE_ANSWER,
            RENDER_PLACEHOLDER: CANDIDATE_RENDER,
            CONFIG_PLACEHOLDER: CANDIDATE_CONFIG,
        },
        staging,
    )


def _input_files(spec: WriterSpec, root: Path) -> dict[str, bytes]:
    """The runner-owned input files the candidate receives, placeholders materialised."""
    files: dict[str, bytes] = {".stage2/prompt.md": spec.prompt.encode("utf-8"), **spec.input_files}
    render = prepare_render(root)
    if render:
        files[".stage2/render.md"] = render
    referenced = any(CONFIG_PLACEHOLDER in str(part) for part in spec.inner_command) or any(
        CONFIG_PLACEHOLDER in value for value in spec.inner_env.values()
    )
    if referenced:
        # The config placeholder names a directory; the marker keeps it a real
        # directory inside the input volume.
        files[".stage2/config/.keep"] = b""
    return files


def _substitute(value: str, targets: dict[str, str]) -> str:
    for placeholder, target in targets.items():
        if placeholder in value:
            return value.replace(placeholder, target)
    return value


def payload_scan_problems(payloads: list[tuple[str, bytes]]) -> list[str]:
    """The outgoing payload scan (criterion 8): the leak rules over the exact bytes.

    `checked_prompt` scans the tree and the prompt text; this scan covers the
    payload pieces a tree scan cannot see - the fresh tracker render, the
    runner's input files, the permitted evidence - under the same rules, so
    every byte made visible to the model was scanned. One hit refuses the
    call before the writer starts.
    """
    import leakcheck

    rules, reason = leakcheck.read_denylist(leakcheck.default_denylist())
    if reason:
        raise BoundaryRefused(f"the outgoing payload cannot be scanned ({reason}); the call does not start.")
    problems: list[str] = []
    for name, data in payloads:
        text = data.decode("utf-8", errors="replace")
        for number, line in enumerate(text.split("\n"), 1):
            for rule in rules:
                found = rule.pattern.search(line)
                if found:
                    problems.append(f"{name}:{number} - rule '{rule.name}' matches (length {len(found.group(0))})")
                    break
    return problems


def launch_writer_call(*, root: Path, spec: WriterSpec) -> WriterRun:
    """One isolated writing attempt: preflight, fresh candidate, launch, stop, export.

    The writer is stopped before its result is inspected, and the export runs
    through the trusted exporter, never through candidate-controlled code on
    the host. Every refusal happens before the launch.
    """
    runtime, lock = preflight(root, spec.endpoint)
    state = InvocationState(
        id=new_invocation_id(),
        verb=spec.verb,
        endpoint=spec.endpoint,
        model=spec.model,
        baseline=spec.baseline,
        attempt=spec.attempt,
    )
    state.detail["root"] = str(root)
    state.detail["program"] = "stand-in" if _stand_in_dir() is not None else program_setting()
    state.save()
    try:
        return _launch(spec, root, runtime, lock, state)
    except AttemptCallFailed:
        cleanup_state(state, runtime)
        raise
    except Exception:
        state.cleanup_pending = state.cleanup_pending or "the launch did not complete"
        state.save()
        raise


def _launch(spec: WriterSpec, root: Path, runtime: Runtime, lock: dict, state: InvocationState) -> WriterRun:
    stand_in = _stand_in_dir() is not None
    targets, staging = _targets(state, stand_in)
    files = _input_files(spec, root)
    if stand_in:
        # The transparent transport materialises the input files where the
        # placeholders point, so the fake CLIs read exactly what production's
        # candidate volume would hold.
        for placeholder, name in (
            (PROMPT_PLACEHOLDER, ".stage2/prompt.md"),
            (RENDER_PLACEHOLDER, ".stage2/render.md"),
        ):
            if placeholder in targets and name in files:
                target = Path(targets[placeholder])
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(files[name])
    command = [_substitute(str(part), targets) for part in spec.inner_command]
    env = {name: _substitute(value, targets) for name, value in spec.inner_env.items()}
    payloads = [("prompt", spec.prompt.encode("utf-8"))]
    payloads += [(name, data) for name, data in sorted(files.items())]
    payloads += [(f"permitted/{relative.as_posix()}", data) for relative, data in sorted(spec.permitted.items())]
    hits = payload_scan_problems(payloads)
    if hits:
        raise BoundaryRefused("the outgoing payload is not clean: " + hits[0] + " The call does not start.")
    if spec.interactive_login:
        login_files, login_env = interactive_login(spec.endpoint, stand_in)
        files.update(login_files)
        env.update(login_env)
        login_file = None
        # An interactive session carries no runner-read credential at all; its
        # sign-in state travels as copied files, so no credential name may
        # stand in the environment.
        selected_pairs = {}
    else:
        try:
            login = selected_login(spec.endpoint, _read_secret)
        except BoundaryRefused:
            # The test transport runs the suite's codex routes without a host
            # sign-in: a missing login *file* is tolerated there and passes no
            # credential at all. Production keeps the refusal (criterion 4).
            if not stand_in or spec.endpoint not in LOGIN_FILES:
                raise
            login = Login(endpoint=spec.endpoint)
        env.update(login.env_pairs)
        login_file = login.file
        selected_pairs = login.env_pairs
    leaked = [name for name in env if name in CREDENTIAL_ENV_NAMES and name not in selected_pairs]
    if leaked:
        raise BoundaryRefused(
            "the launch environment would carry an unselected credential: " + ", ".join(sorted(leaked))
        )
    if not stand_in:
        for name in ("HOME", "TMPDIR", "PATH", "BEAD_RENDER", *CREDENTIAL_ENV_NAMES):
            env.pop(name, None)
        proxy_name = f"egress-proxy-{state.id[:12]}"
        env["HTTPS_PROXY"] = f"http://{proxy_name}:8080"
        env["https_proxy"] = f"http://{proxy_name}:8080"
        env["NO_PROXY"] = proxy_name
        env["BEAD_RENDER"] = CANDIDATE_RENDER
        if login_file is not None:
            # The one login file travels as a copied input under its own home,
            # pointed at by the CLI's own variable - never as a mounted
            # sign-in directory, keychain or agent socket (criterion 4).
            if spec.endpoint == "openai-codex":
                home, variable = ".stage2/codex-home", "CODEX_HOME"
            else:
                home, variable = ".stage2/claude-home", "CLAUDE_CONFIG_DIR"
            files[f"{home}/{login_file.name}"] = login_file.read_bytes()
            env[variable] = f"{CANDIDATE_WORK}/{home}"
    work = worktree_tar(root, spec.baseline, spec.permitted)
    if stand_in:
        request = RunRequest(
            image="stand-in",
            argv=command,
            env=env,
            volumes=[(state.label("cand"), CANDIDATE_WORK, False)],
            networks=["stand-in-egress"],
            timeout=spec.timeout,
            transparent_cwd=root,
            attached=spec.attached,
        )
        done = runtime.run(request)
        return WriterRun(
            done=done,
            runtime=runtime,
            state=state,
            delta=CandidateDelta(transparent=True),
            answer_path=Path(targets[ANSWER_PLACEHOLDER]) if (staging / "answer.md").exists() else None,
            transparent=True,
            baseline_archive=work,
        )
    cand = runtime.create_volume(state, "cand")
    gitvol = runtime.create_volume(state, "git")
    inputvol = runtime.create_volume(state, "in")
    egressvol = runtime.create_volume(state, "egress")
    runtime.populate(state, cand, work)
    runtime.populate(state, gitvol, git_tar(root, spec.baseline))
    runtime.populate(state, inputvol, input_files_tar(files))
    proxy_net = runtime.create_network(state, "priv", internal=True)
    out_net = runtime.create_network(state, "out", internal=False)
    image = image_reference(lock, "model")
    egress_script = (REPO_ROOT / "scripts" / "stage2_egress.py").read_bytes()
    runtime.populate(state, egressvol, input_files_tar({"stage2_egress.py": egress_script}))
    hosts = api_hosts(root, spec.endpoint)
    proxy_request = RunRequest(
        image=image,
        argv=[
            "python3",
            "/egress/stage2_egress.py",
            "serve",
            "--hosts",
            ",".join(hosts),
            "--bind",
            "0.0.0.0",
            "--port",
            "8080",
        ],
        env={},
        volumes=[(egressvol, "/egress", True)],
        networks=[proxy_net, out_net],
        detach=True,
        name=proxy_name,
    )
    runtime.start_detached(proxy_request)
    state.record("container", proxy_name)
    state.save()
    request = RunRequest(
        image=image,
        argv=command,
        env=env,
        volumes=[
            (cand, CANDIDATE_WORK, False),
            (gitvol, f"{CANDIDATE_WORK}/.git", True),
            (inputvol, f"{CANDIDATE_WORK}/.stage2", False),
        ],
        networks=[proxy_net],
        timeout=spec.timeout,
        attached=spec.attached,
    )
    done = runtime.run(request)
    # The candidate's `.stage2` is the input volume's mount point, so the
    # model's answer (and any login copy) lands on the *input* volume while
    # the trusted export reads the candidate: merge both exports, the
    # candidate winning on a name, or the answer is lost (ADR 0018).
    exported = merge_tars(runtime.export_volume(state, cand), runtime.export_volume(state, inputvol))
    staged = staging / "candidate.tar"
    staged.write_bytes(exported)
    delta = diff_candidate(work, exported, derived=spec.derived_paths, binary_ok=spec.binary_ok)
    candidate_map, _ = _tar_file_map(exported, noise=True)
    answer_bytes = candidate_map.get(Path(".stage2/answer.md"))
    answer_path: Path | None = staging / "answer.md"
    if answer_bytes is None:
        answer_path = None
    else:
        answer_path.write_bytes(answer_bytes)
    return WriterRun(
        done=done, runtime=runtime, state=state, delta=delta, answer_path=answer_path, baseline_archive=work
    )


class Verifier:
    """The credential-free checker: every launch through the runtime, no network."""

    def __init__(self, root: Path, candidate_tar: bytes | None = None) -> None:
        self.root = root
        self.candidate_tar = candidate_tar
        self.stand_in = _stand_in_dir() is not None
        self.runtime = choose_runtime()

    def env(self, extra: dict[str, str]) -> dict[str, str]:
        checked = dict(extra)
        for name in CREDENTIAL_ENV_NAMES:
            checked.pop(name, None)
        return checked

    def run(self, command: list[str], env: dict[str, str], timeout: float | None = None) -> subprocess.CompletedProcess:
        checked = self.env(env)
        if self.stand_in:
            return subprocess.run(
                command,
                cwd=self.root,
                env=checked,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                errors="replace",
                check=False,
                timeout=timeout,
            )
        if self.candidate_tar is None:
            raise BoundaryRefused("the verifier has no candidate to check; verification refuses to run.")
        lock = runtime_lock()
        state = InvocationState(
            id=f"verif-{new_invocation_id()}", verb="verifier", endpoint="-", model="-", baseline="-"
        )
        cand = self.runtime.create_volume(state, "verif")
        self.runtime.populate(state, cand, self.candidate_tar)
        image = image_reference(lock, "verifier")
        request = RunRequest(
            image=image, argv=command, env=checked, volumes=[(cand, CANDIDATE_WORK, False)], networks=[]
        )
        return self.runtime.run(request)


# ---------------------------------------------------------------------------
# The verifier role (criterion 13): no model credentials, no network
# ---------------------------------------------------------------------------


VERIFY_SHIM = REPO_ROOT / "scripts" / "stage2_verify_inside.py"


def run_verifier(
    root: Path,
    candidate_tar: bytes,
    git_tar_bytes: bytes,
    command: list[str],
    env: dict[str, str],
    timeout: float | None = None,
    inputs: dict[str, bytes] | None = None,
) -> tuple[subprocess.CompletedProcess, bytes | None]:
    """Run the credential-free verifier against the composed candidate; return (done, post-tar).

    The stand-in executes the verification shim on the host with the caller's
    environment and the suite's own PATH and HOME - the test transport, never
    production. Production populates fresh volumes: the composed candidate
    read-write, the private Git read-write (the red-first proof creates a
    worktree in it), the shim and its inputs at `.stage2`; the verifier runs
    with no network and no model credential (criterion 13), and its timed-out
    check is a finished failure, not a hung launch. The post-tar is the
    candidate volume's export after the checks ran, so the runner can re-diff
    what its own preparation changed.
    """
    checked = {name: value for name, value in env.items() if name not in CREDENTIAL_ENV_NAMES}
    if _stand_in_dir() is not None:
        checked["PATH"] = os.environ.get("PATH", checked.get("PATH", "/usr/bin:/bin"))
        checked.setdefault("HOME", os.environ.get("HOME", str(root)))
        # The shim must know it is the test transport: on the host it neither
        # wraps `.venv` nor builds a candidate's Git - the world already holds
        # both.
        stand_in = _stand_in_dir()
        if stand_in is not None:
            checked["STAGE2_RUNTIME_STAND_IN"] = str(stand_in)
        done = subprocess.run(
            [sys.executable, str(VERIFY_SHIM)],
            cwd=root,
            env=checked,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            errors="replace",
            check=False,
            timeout=timeout,
        )
        return done, None
    lock = runtime_lock()
    state = InvocationState(id=f"verif-{new_invocation_id()}", verb="verifier", endpoint="-", model="-", baseline="-")
    state.save()
    try:
        runtime = choose_runtime()
        cand = runtime.create_volume(state, "verif")
        gitvol = runtime.create_volume(state, "verifgit")
        invol = runtime.create_volume(state, "verifin")
        runtime.populate(state, cand, candidate_tar)
        runtime.populate(state, gitvol, git_tar_bytes)
        files = {".stage2/stage2_verify_inside.py": VERIFY_SHIM.read_bytes(), **(inputs or {})}
        runtime.populate(state, invol, input_files_tar(files))
        image = image_reference(lock, "verifier")
        request = RunRequest(
            image=image,
            argv=command,
            env=checked,
            volumes=[
                (cand, CANDIDATE_WORK, False),
                (gitvol, f"{CANDIDATE_WORK}/.git", False),
                (invol, f"{CANDIDATE_WORK}/.stage2", False),
            ],
            networks=[],
            timeout=timeout,
        )
        done = runtime.run(request)
        post = runtime.export_volume(state, cand)
        return done, post
    finally:
        cleanup_state(state, runtime)


# ---------------------------------------------------------------------------
# The session supervisor subcommand (criterion 20, step 6)
# ---------------------------------------------------------------------------


SESSION_DIR = ".stage2-sessions"
POLICY_PLACEHOLDER = "@STAGE2_POLICY_FILE@"
POLICY_INPUT = ".stage2/policy"
# The checks a session's candidate must pass before its edits return: the
# preparation, the format step and `make verify` - no measured time entry,
# which stays the automatic verbs' duty (plan step 6).
SESSION_VERIFY_MINUTES = 90


def _session_record(root: Path, invocation_id: str) -> tuple[Path, dict]:
    """The dispatch's state: `<root>/.stage2-sessions/session-<id>/invocation.json`."""
    directory = root / SESSION_DIR / f"session-{invocation_id}"
    state_file = directory / "invocation.json"
    if not state_file.is_file():
        raise BoundaryRefused(f"no invocation {invocation_id} is recorded under {SESSION_DIR}/; nothing runs.")
    try:
        record = json.loads(state_file.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise BoundaryRefused(f"the invocation state cannot be read: {error}") from error
    if not isinstance(record, dict):
        raise BoundaryRefused("the invocation state is not a record; nothing runs.")
    return directory, record


def _session_outcome(stage2, root: Path, record: dict, invocation_id: str, outcome: str) -> None:
    """One result line beside the dispatch's audit line, scrubbed of nothing - it holds no secret.

    The line's own prefix stays distinct from the dispatch audit's (`Stage-2
    session, ...`), so a reader filtering for either finds exactly one form.
    """
    findings = root / "plans" / "changes" / str(record.get("change", "")) / "findings.md"
    line = f"Session attempt {invocation_id} · {outcome} ({stage2.today()})."
    try:
        if findings.exists():
            stage2.append(findings, line)
    except OSError:
        # The outcome is printed regardless; a missing audit line is a visible
        # gap, never a silent one.
        print(f"session supervisor: the outcome line could not be written to {findings}.", file=sys.stderr)


def _session_checks(root: Path, candidate_tar: bytes | None) -> tuple[list[str], list[str]]:
    """The candidate's checks through the credential-free verifier; (problems, formatted)."""
    env = {
        "VERIFY_MODE": "session",
        "PATH": "/usr/local/bin:/usr/bin:/bin",
        "HOME": "/home/runner",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    if _stand_in_dir() is not None:
        env["PATH"] = os.environ.get("PATH", env["PATH"])
        env["HOME"] = os.environ.get("HOME", env["HOME"])
    command = (
        [sys.executable, str(VERIFY_SHIM)]
        if _stand_in_dir() is not None
        else ["python3", f"{CANDIDATE_WORK}/.stage2/stage2_verify_inside.py"]
    )
    done, _post = run_verifier(
        root,
        candidate_tar,
        git_tar(root, _rev_of(root, "HEAD")) if candidate_tar is not None else None,
        command,
        env,
        timeout=SESSION_VERIFY_MINUTES * 60,
    )
    if done.returncode != 0:
        tail = (done.stdout or done.stderr or "").strip().splitlines()
        detail = tail[-1][:200] if tail else "no output"
        return [f"the session's checks ended {done.returncode}: {detail}"], []
    for line in (done.stdout or "").splitlines():
        stripped = line.strip()
        if stripped.startswith("{"):
            try:
                report = json.loads(stripped)
            except ValueError:
                continue
            formatted = [str(entry) for entry in report.get("formatted", [])]
            return [str(problem) for problem in report.get("problems", [])], formatted
    return ["the session's checks produced no report; a missing report is never a pass"], []


def run_session_supervisor(invocation_id: str) -> int:
    """The whole interactive lifetime inside the Terminal window.

    The Terminal command carries the opaque id alone: the prompt, the
    declaration and the login are read here, from the dispatch's state file
    and the CLI's own sign-in, never from the command line and never from the
    runner's secrets. The lifetime runs in a fresh candidate populated from
    the dispatch's baseline (criterion 1); a normal exit runs the checks in
    the credential-free verifier and returns the verified edits uncommitted
    (criterion 20), a cancellation or a failed check discards the candidate.
    Dispatch acceptance alone is never completion: only a normal exit with
    green checks returns 0.
    """
    import stage2  # local import: this process is started by Terminal, not by the runner

    record: dict | None = None
    try:
        root = Path.cwd()
        directory, record = _session_record(root, invocation_id)
        change = str(record.get("change", ""))
        endpoint = str(record.get("endpoint", ""))
        baseline = str(record.get("baseline", ""))
        prompt = str(record.get("prompt", ""))
        command = [str(part) for part in (record.get("inner_command") or [])]
        if not command or not baseline or not change:
            raise BoundaryRefused("the invocation state is incomplete; nothing runs.")
        keep = {Path("plans") / "changes" / change / "findings.md"}
        expected = host_state(root, keep=keep)
        stand_in = _stand_in_dir() is not None
        runtime = choose_runtime()
        lock = runtime_lock()
        if not stand_in:
            kind, _ = selected_program()
            problem = lock_problem(lock, kind)
            if problem:
                raise BoundaryRefused(problem)
            problem = profile_problem(root, endpoint)
            if problem:
                raise BoundaryRefused(problem)
        # The policy copy travels as an input file; its placeholder becomes the
        # candidate path in production and the private copy's path in the test
        # transport, where the CLI runs where the files are.
        input_files: dict[str, bytes] = {}
        policy_name = str(record.get("policy") or "")
        if policy_name:
            policy_copy = directory / policy_name
            input_files[f"{POLICY_INPUT}/{policy_name}"] = policy_copy.read_bytes()
            policy_target: str = str(policy_copy) if stand_in else f"{CANDIDATE_WORK}/{POLICY_INPUT}/{policy_name}"
        else:
            policy_target = ""
        # The placeholders become real paths here, where the transport is known:
        # candidate paths in production, the dispatch's own paths in the test
        # transport, whose CLI runs where the files are.
        work_target = str(root) if stand_in else CANDIDATE_WORK
        command = [
            part.replace(POLICY_PLACEHOLDER, policy_target).replace(WORK_PLACEHOLDER, work_target) for part in command
        ]
        spec = WriterSpec(
            verb="session",
            change=change,
            endpoint=endpoint,
            model=str(record.get("model", "")),
            prompt=prompt,
            inner_command=command,
            # The window's own environment, through the runner's allow-list: the
            # PATH that resolves the CLI, the TERM a TUI needs, the HOME the
            # login copy comes from. Production strips the host paths from it
            # before the container sees them (stage2_attempt._launch).
            inner_env={
                **stage2.foreign_env({}),
                **{str(key): str(value) for key, value in (record.get("inner_env") or {}).items()},
            },
            baseline=baseline,
            input_files=input_files,
            attached=True,
            interactive_login=True,
        )
        run = launch_writer_call(root=root, spec=spec)
        if run.done.returncode != 0:
            run.discard()
            _session_outcome(stage2, root, record, invocation_id, "cancelled; the candidate was discarded")
            print(
                f"session supervisor: the CLI ended {run.done.returncode}; the candidate is discarded.",
                file=sys.stderr,
            )
            return 1
        if run.transparent:
            # The test transport wrote the worktree directly: the checks run in
            # place, and no second publication exists to make.
            problems, formatted = _session_checks(root, None)
            for line in formatted:
                print(f"session supervisor: {line}")
            if problems:
                _session_outcome(stage2, root, record, invocation_id, "failed its checks; the run stops")
                for problem in problems:
                    print(f"session supervisor: {problem}", file=sys.stderr)
                run.discard()
                return 1
            run.discard()
            _session_outcome(stage2, root, record, invocation_id, "verified; the edits stand uncommitted")
            print("session supervisor: the checks are green; the edits stand in the worktree uncommitted.")
            return 0
        # A stopped candidate is inspected only through its validated delta.
        problems = validate_delta(run.delta)
        if problems:
            run.discard()
            raise BoundaryRefused("the session's candidate was rejected: " + "; ".join(problems[:3]))
        candidate_tar = compose_candidate(run.baseline_archive, run.delta)
        problems, formatted = _session_checks(root, candidate_tar)
        for line in formatted:
            print(f"session supervisor: {line}")
        if problems:
            run.discard()
            _session_outcome(stage2, root, record, invocation_id, "failed its checks; the candidate was discarded")
            for problem in problems:
                print(f"session supervisor: {problem}", file=sys.stderr)
            return 1
        applied: list = []
        try:
            assert_host_state(root, expected, keep=keep)
            # The evidence path is the runner's: a candidate that touched it
            # publishes everything else, never its findings.md (criterion 21).
            only = {entry.path for entry in run.delta.entries} - keep
            applied = publish_delta(run.delta, root, run.state, only=only)
        except BaseException:
            undo_owned(root, applied, baseline)
            run.discard()
            raise
        run.discard()
        _session_outcome(stage2, root, record, invocation_id, "verified; the edits are back uncommitted")
        print("session supervisor: the verified edits are back in the worktree, uncommitted.")
        return 0
    except BoundaryRefused as error:
        if record is not None:
            _session_outcome(stage2, root, record, invocation_id, f"refused: {error}")
        print(f"session supervisor: {error}", file=sys.stderr)
        return 2
    except AttemptCallFailed as error:
        if record is not None:
            _session_outcome(stage2, root, record, invocation_id, "cancelled; the candidate was discarded")
        print(f"session supervisor: {error}; the candidate is discarded.", file=sys.stderr)
        return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("command", choices=["session-supervisor"])
    parser.add_argument("invocation", help="the opaque invocation identifier the dispatch recorded")
    args = parser.parse_args(argv)
    if args.command == "session-supervisor":
        return run_session_supervisor(args.invocation)
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BoundaryRefused as error:
        print(f"refused: {error}", file=sys.stderr)
        raise SystemExit(2) from None
