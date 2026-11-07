"""The offline Pi contracts: the real pinned Pi against a loopback stand-in.

Every case here starts the actual installed Pi through the repository wrapper
(`tools/pi/pi`), pointed at a loopback HTTP stand-in that answers OpenAI-style
chat completions from a script: a tool call, a stop, an error. No hosted
model, no user configuration, no external network: the credentials are
synthetic, the HOME and agent directories are scratch, and a test-only preload
(`tests/pi_network_guard.mjs`) denies every non-loopback connection the child
attempts. The reviewer-shaped cases run the runner's own `run_reviewer` and
inject test transport at its subprocess seam. Helper launches derive their
isolation flags from that same production command.

Missing Pi, missing Node, a refused loopback bind, a timeout or a malformed
exchange FAILS its case (spec, criterion 12). The suite never skips.

Each test comes with its fault: armed traps, an undeclared tool, an outside
path, a foreign credential or a broken exchange is planted one at a time and
named in the test.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import types
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import stage2  # noqa: E402
import stage2_availability as availability  # noqa: E402
import stage2_free  # noqa: E402
import stage2_go  # noqa: E402
import stage2_swarm  # noqa: E402
from terms_fixtures import admissible_terms  # noqa: E402
from test_stage2 import World  # noqa: E402
from test_stage2 import git as run_git  # noqa: E402
from test_stage2 import world as stage2_world  # noqa: E402
from test_stage2_research_catalog import sources as research_catalog_sources  # noqa: E402

world = stage2_world
catalog_sources = research_catalog_sources
# The repository's own Pi wrapper, read before any test world re-points `stage2.PI_WRAPPER` at a stand-in.
REAL_PI_WRAPPER = stage2.PI_WRAPPER
# The runtime search path before a test world replaces it: the real Pi wrapper needs Node on it.
REAL_PATH = os.environ.get("PATH", "")

PKG = "@earendil-works/pi-coding-agent"
GUARD = REPO_ROOT / "tests" / "pi_network_guard.mjs"
DRIVER = REPO_ROOT / "tests" / "pi_contract_driver.mjs"
POLICY_SOURCE = REPO_ROOT / "scripts" / "stage2_session_policy.mjs"
SYNTHETIC_KEY = "ok-contract-synthetic-key"
PLANTED_KEY = "ok-TRAP-credential-never-send"
SENTINEL_IN = "INSIDE-CONTENT-7f3a41"
SENTINEL_OUT = "OUTSIDE-SENTINEL-b2c95e"
GO_NATIVE = "https://opencode.ai/zen/go/v1"
GO_MOVED = "https://opencode.ai/inference/go/v1"
# The move notice names paths only, never the authority (criterion 11).
GO_MOVED_PATH = "/inference/go/v1"
ZEN_NATIVE = "https://opencode.ai/zen/v1"
# Pi 1.5.0 ships Zen at this base (read from the installed catalog, 2026-11-04); the runner never
# selects Zen (scripts/stage2.py, the free rule), the synthetic ZEN_NATIVE stays the fixtures' start.
ZEN_SHIPPED = "https://opencode.ai/inference/openai/v1"
# The shipped 1.5.0 catalog addresses (spec criteria 2-3, decisions.md Q-1): the moved Go
# endpoints the installed package must carry by itself - no live store, no overlay supplies them.
GO_SHIPPED = "https://opencode.ai/inference/go/openai/v1"
GO_SHIPPED_MESSAGES = "https://opencode.ai/inference/go/anthropic"
PI_MOVED_PIN = "1.5.0"


def declare_contract_models(root: Path) -> None:
    """Synthetic, dated admission for loopback wire tests; never use live terms."""
    models = ["contract-rung", "acme-1-free", "synthetic-protocol-check-free", "deepseek-v4.1-flash"]
    terms = {model: admissible_terms(quelle="synthetic loopback contract") for model in models}
    (root / "model-endpoints.yaml").write_text(
        yaml.safe_dump(
            {
                "endpunkte": [
                    {
                        "name": "opencode-go",
                        "modelle": models,
                        "modelle_terms": terms,
                        # The synthetic Go address record (go-access-point): the loopback
                        # wire tests route the admitted HTTPS target at the transport
                        # seam, and the address tests here read this record, never the
                        # held real file.
                        "adresse": {
                            "host": "opencode.ai",
                            "apis": {
                                "openai-completions": {
                                    "basis": GO_NATIVE,
                                    "quelle": "the synthetic contract record (go-access-point)",
                                    "gelesen": "2026-10-31",
                                }
                            },
                        },
                    }
                ]
            }
        ),
        encoding="utf-8",
    )


def contract_address_policy() -> stage2_go.AddressPolicy:
    """The address policy of the contract record, as `load_address_policy` returns one."""
    return stage2_go.AddressPolicy(
        host="opencode.ai",
        apis={
            "openai-completions": stage2_go.BaseRecord(
                api="openai-completions", base=GO_NATIVE, source="the synthetic contract record", read="2026-10-31"
            )
        },
    )


def contract_ctx(root: Path, model: str = "contract-rung") -> types.SimpleNamespace:
    """A reviewer context whose refreshed store holds the model as the record assessed it.

    The row keeps the recorded base: assessment and the move notice read as
    production reads them, and the wire tests repoint the actual destination
    at the loopback through the transport seam's models.json override.
    """
    return types.SimpleNamespace(
        change="demo",
        root=root,
        models_store={
            "opencode-go": {
                "models": [
                    {
                        "id": model,
                        "provider": "opencode-go",
                        "api": "openai-completions",
                        "baseUrl": GO_NATIVE,
                        "reasoning": False,
                        "input": ["text"],
                        "contextWindow": 128000,
                        "maxTokens": 4096,
                    }
                ],
                "lastModified": 0,
            }
        },
    )


class ContractFailure(Exception):
    """A contract that cannot run or cannot be answered fails; it never skips."""


def _manifest_pin() -> str:
    try:
        manifest = json.loads((REPO_ROOT / "tools" / "pi" / "package.json").read_text(encoding="utf-8"))
        pin = manifest["dependencies"][PKG]
    except (OSError, json.JSONDecodeError, KeyError) as error:
        raise ContractFailure(f"tools/pi/package.json does not pin {PKG}: {error}") from None
    if not re.fullmatch(r"\d+\.\d+\.\d+", pin):
        raise ContractFailure(f"tools/pi/package.json pins {pin!r}, not an exact version")
    return pin


PIN = _manifest_pin()


def require_installed_pi() -> str:
    """Fail the run - never skip - when the pinned Pi or its Node is missing (spec, criterion 12)."""
    if shutil.which("node") is None:
        pytest.fail(
            "the Pi contracts need Node (tools/pi/.node-version) on PATH; missing prerequisites fail, they do not skip"
        )
    wrapper = stage2.PI_WRAPPER
    if not wrapper.is_file():
        pytest.fail(f"the repository Pi wrapper {wrapper} is missing; run bash tools/pi/install.sh")
    with tempfile.TemporaryDirectory(prefix="pi-contract-") as tmp:
        env = {
            **contract_environment(),
            "HOME": tmp,
            "PI_CODING_AGENT_DIR": tmp,
        }
        try:
            done = subprocess.run(
                [str(wrapper), "--version"],
                cwd=tmp,
                env=env,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                errors="replace",
                timeout=120,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            pytest.fail(f"the pinned Pi {PIN} could not be checked ({error}); run bash tools/pi/install.sh")
    if done.returncode != 0 or done.stdout.strip() != PIN:
        said = done.stdout.strip() or "nothing"
        pytest.fail(
            f"the pinned Pi {PIN} is not installed or will not start (printed {said!r}, ended {done.returncode}): "
            f"{done.stderr.strip()[:400]}; run bash tools/pi/install.sh"
        )
    return str(wrapper)


@pytest.fixture(scope="module")
def installed_pi() -> str:
    """The suite's mandatory prerequisite, checked once: the pinned install answers."""
    return require_installed_pi()


# ---------------------------------------------------------------------------
# The loopback stand-in
# ---------------------------------------------------------------------------


@dataclass
class Exchange:
    """One request the stand-in received: path, lower-cased headers, parsed body."""

    path: str
    headers: dict
    body: dict


class _Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args: object) -> None:  # the suite reads the captured exchanges, not the log
        pass

    def _standin(self) -> StandIn:
        return self.server.standin  # type: ignore[attr-defined]

    def do_GET(self) -> None:  # noqa: N802 - the base class spells it this way
        self._standin().requests.append(Exchange(self.path, dict(self.headers), {}))
        self._send_bytes(200, "text/plain", b"contract stand-in alive\n")

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        try:
            body = json.loads(raw.decode("utf-8")) if raw.strip() else {}
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._standin().failures.append("a request the stand-in could not parse arrived")
            self._send_json(400, {"error": {"message": "unparseable request body"}})
            return
        self._standin().requests.append(Exchange(self.path, {k.lower(): v for k, v in self.headers.items()}, body))
        if not self.path.endswith("/chat/completions"):
            self._send_json(404, {"error": {"message": f"no contract route for {self.path}"}})
            return
        try:
            self._standin()._completions(self, body)
        except ContractFailure as error:
            # a scripted exchange that cannot be answered fails the run loudly - never a silent skip
            self._standin().failures.append(str(error))
            self._send_json(500, {"error": {"message": str(error)}})
        except Exception as error:  # noqa: BLE001 - the failure is recorded, then answered
            self._standin().failures.append(f"{type(error).__name__}: {error}")
            self._send_json(500, {"error": {"message": "stand-in fault"}})

    def _send_json(self, status: int, payload: dict) -> None:
        self._send_bytes(status, "application/json", json.dumps(payload).encode("utf-8"))

    def _send_bytes(self, status: int, kind: str, data: bytes) -> None:
        try:
            self.send_response(status)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except OSError:
            pass


class StandIn:
    """A loopback OpenAI-compatible chat-completions server with a script.

    Each POST ending in /chat/completions consumes the next entry of `script`
    and every request is captured. A streaming request is answered with one
    server-sent event, a non-streaming one with a JSON body; both carry the
    same message. `sleep` and `error` entries serve the mandatory-failure
    contracts. The bind is loopback-only and refused ports fail the case.
    """

    def __init__(self, script: list[dict]) -> None:
        self.script = list(script)
        self.requests: list[Exchange] = []
        self.failures: list[str] = []
        self._server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        self._server.standin = self
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        self.url = f"http://127.0.0.1:{self._server.server_address[1]}/v1"

    def _completions(self, handler: _Handler, body: dict) -> None:
        if not self.script:
            raise ContractFailure("the stand-in ran out of script: Pi asked for more turns than the contract scripted")
        answer = self.script.pop(0)
        if "wait_for" in answer:
            # Hold the reply until a marker file exists (bounded): Pi starts background helpers
            # (an MCP server) while it waits for the model, and ends them with the reply. On a loaded
            # machine (parallel tests) the reply used to win that race.
            deadline = time.monotonic() + 20
            while not Path(answer["wait_for"]).exists() and time.monotonic() < deadline:
                time.sleep(0.05)
        if "sleep" in answer:
            time.sleep(answer["sleep"])
            return
        if "error" in answer:
            handler._send_json(int(answer.get("status", 401)), {"error": answer["error"]})
            return
        payload = self._completion(answer, body)
        if body.get("stream"):
            message = payload["choices"][0]["message"]
            chunk = {
                "id": payload["id"],
                "object": "chat.completion.chunk",
                "created": payload["created"],
                "model": payload["model"],
                "choices": [{"index": 0, "delta": message, "finish_reason": payload["choices"][0]["finish_reason"]}],
            }
            data = b"data: " + json.dumps(chunk).encode("utf-8") + b"\n\ndata: [DONE]\n\n"
            handler._send_bytes(200, "text/event-stream", data)
        else:
            handler._send_json(200, payload)

    def _completion(self, answer: dict, request: dict) -> dict:
        if "tool_calls" in answer:
            message = {
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {
                        "id": f"call_{index}",
                        "type": "function",
                        "function": {"name": call["name"], "arguments": json.dumps(call["arguments"])},
                    }
                    for index, call in enumerate(answer["tool_calls"])
                ],
            }
            finish = "tool_calls"
        else:
            message = {"role": "assistant", "content": answer.get("content", "No finding."), "tool_calls": None}
            finish = answer.get("finish_reason", "stop")
        return {
            "id": "chatcmpl-contract",
            "object": "chat.completion",
            "created": 1760486400,
            "model": request.get("model", "contract-model"),
            "choices": [{"index": 0, "message": message, "finish_reason": finish}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20},
        }

    def close(self) -> None:
        self._server.shutdown()
        self._server.server_close()
        self._thread.join(timeout=10)


# ---------------------------------------------------------------------------
# Launch helpers
# ---------------------------------------------------------------------------


def run_pi(
    project: Path,
    scratch: Path,
    *args: str,
    key: str = SYNTHETIC_KEY,
    providers: dict | None = None,
    timeout: int = 180,
    env_extra: dict | None = None,
) -> subprocess.CompletedProcess:
    """Start the actual pinned Pi through the repository wrapper, offline and guarded.

    Scratch HOME and agent directory, a synthetic `OPENCODE_API_KEY`, the
    network guard preloaded, the provider addresses repointed at a loopback
    stand-in through the scratch `models.json` - the measured override seam.
    """
    agent = scratch / "agent"
    home = scratch / "home"
    agent.mkdir(parents=True, exist_ok=True)
    home.mkdir(parents=True, exist_ok=True)
    (agent / "settings.json").write_text(json.dumps({"retry": {"enabled": False}}), encoding="utf-8")
    if providers:
        (agent / "models.json").write_text(json.dumps({"providers": providers}), encoding="utf-8")
    env = {
        **contract_environment(),
        "HOME": str(home),
        "PI_CODING_AGENT_DIR": str(agent),
        "OPENCODE_API_KEY": key,
        "NODE_OPTIONS": f"--import {GUARD}",
        **(env_extra or {}),
    }
    try:
        return subprocess.run(
            [str(stage2.PI_WRAPPER), *args],
            cwd=project,
            env=env,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise ContractFailure(f"Pi did not end within {timeout}s: {error}") from None


@pytest.fixture
def transport(monkeypatch: pytest.MonkeyPatch) -> types.SimpleNamespace:
    """The test transport, injected at the runner's subprocess seam (plan step 5).

    The default command comes from production code; the seam adds a network
    guard, a resource-read observer and loopback transport configuration.
    Trap controls grant project trust and omit individual guards. MCP controls
    explicitly request its built-in extension so --no-extensions cannot mask
    --no-mcp. Helper flags are captured from `run_reviewer` as well.
    """
    calls: list[dict] = []
    providers: dict = {}
    controls = {"trusted": False, "omit": None, "mcp_control": False}
    original_launch = stage2.launch

    def repoint(env):
        """Route the admitted HTTPS target at the loopback stand-in, at the transport seam.

        The runner's own checked `models.json` stays as it was through every
        assessment and the offline overlay validation; only the launch that
        reaches Pi has each activated model's base replaced, and the production
        host check is never relaxed for the loopback URL.
        """
        base = providers.get("opencode-go", {}).get("baseUrl")
        agent = env.get("PI_CODING_AGENT_DIR")
        path = Path(agent, "models.json") if agent else None
        if not base or path is None or not path.is_file():
            return
        activated = json.loads(path.read_text(encoding="utf-8"))
        for entry in activated.get("providers", {}).values():
            for model in entry.get("models", []):
                model["baseUrl"] = base
        path.write_text(json.dumps(activated), encoding="utf-8")

    def guarded_launch(command, cwd, env, key=None, timeout=None, limit=None):
        if command[0] == "node":
            # The offline overlay validation is the runner's check of the checked
            # configuration, not a reviewer call: it is neither guarded nor recorded.
            return original_launch(command, cwd, env, key, timeout=timeout, limit=limit)
        repoint(env)
        env = {
            **env,
            "NODE_OPTIONS": f"--import {GUARD} --import {DRIVER}",
            "CONTRACT_RESOURCE_LOG": str(Path(cwd) / "resource-reads.jsonl"),
        }
        command = list(command)
        if controls["trusted"]:
            command[command.index("--no-approve")] = "--approve"
        if controls["omit"]:
            command.remove(controls["omit"])
        if controls["mcp_control"]:
            command[1:1] = ["-e", "builtin:mcp"]
        calls.append({"argv": list(command), "cwd": str(cwd), "env": dict(env)})
        done = original_launch(command, cwd, env, key, timeout=timeout, limit=limit)
        calls[-1]["result"] = done
        return done

    monkeypatch.setattr(stage2, "launch", guarded_launch)
    return types.SimpleNamespace(calls=calls, providers=providers, controls=controls)


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """A controlled project: one sentinel file a tool may read."""
    root = tmp_path / "project"
    root.mkdir()
    declare_contract_models(root)
    (root / "sentinel.txt").write_text(SENTINEL_IN + "\n", encoding="utf-8")
    return root


def scratch_of(tmp_path: Path) -> Path:
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    return scratch


def tool_names(exchange: Exchange) -> set[str]:
    """The tools the request declared, however the provider schema nests them."""
    found = set()
    for tool in exchange.body.get("tools", []):
        name = tool.get("name") or tool.get("function", {}).get("name")
        if name:
            found.add(name)
    return found


def message_text(exchange: Exchange) -> str:
    """Every text the exchange's conversation carries, flattened for a substring check."""
    pieces = []
    for message in exchange.body.get("messages", []):
        content = message.get("content")
        if isinstance(content, str):
            pieces.append(content)
        elif isinstance(content, list):
            pieces.extend(str(part) for part in content)
    return "\n".join(pieces)


def provider_data(provider: str) -> dict:
    """A provider's catalog of the installed Pi - the native address's own home.

    Pi 1.2.0 keeps each provider's models, with their `baseUrl`, in
    `pi-ai/dist/providers/data/<provider>.json`, grouped by wire API; the
    provider's `.js` module holds no address any more (measured 2026-10-15).
    """
    root = REPO_ROOT / "tools" / "pi" / "node_modules" / "@earendil-works" / "pi-ai" / "dist" / "providers" / "data"
    candidate = root / f"{provider}.json"
    if not candidate.is_file():
        pytest.fail(f"the installed Pi's catalog {candidate} is missing; run bash tools/pi/install.sh")
    try:
        return json.loads(candidate.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        pytest.fail(f"the installed Pi's catalog {candidate} cannot be read: {error}")


def native_base_urls(provider: str, api: str) -> set[str]:
    """The addresses the installed Pi's catalog gives a provider's models of one wire API."""
    section = provider_data(provider).get(api)
    if not isinstance(section, dict) or not section:
        pytest.fail(f"the installed Pi's {provider} catalog holds no {api} models; the wire API moved")
    return {model.get("baseUrl") for model in section.values() if isinstance(model, dict)}


# ---------------------------------------------------------------------------
# The catalog move: the locked 1.5.0 install and its shipped Go addresses
# ---------------------------------------------------------------------------


@pytest.mark.usefixtures("installed_pi")
def test_real_catalog_move_uses_locked_pi_1_5_0() -> None:
    """Ledger 1: manifest, lock graph, lock entry and running wrapper agree on exactly Pi 1.5.0.

    Every point is anchored to the literal version, so a floating pin, a lock the manifest
    outgrew, a stale install or a wrapper reporting another version fails this contract
    instead of passing the move.
    """
    pin = _manifest_pin()
    assert pin == PI_MOVED_PIN, f"tools/pi/package.json pins {pin!r}, not the moved {PI_MOVED_PIN}"
    lock_path = REPO_ROOT / "tools" / "pi" / "package-lock.json"
    try:
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        pytest.fail(f"tools/pi/package-lock.json cannot be read: {error}")
    packages = lock.get("packages", {})
    root_pin = packages.get("", {}).get("dependencies", {}).get(PKG)
    assert root_pin == PI_MOVED_PIN, (
        f"the lock's root graph pins {root_pin!r}, not the moved {PI_MOVED_PIN}; regenerate the lock with npm"
    )
    entry = packages.get(f"node_modules/{PKG}", {})
    assert entry.get("version") == PI_MOVED_PIN, (
        f"the lock's installed-package entry holds {entry.get('version')!r}, not the moved {PI_MOVED_PIN}"
    )
    resolved = entry.get("resolved")
    assert isinstance(resolved, str) and resolved.endswith(f"pi-coding-agent-{PI_MOVED_PIN}.tgz"), (
        f"the lock resolves {resolved!r}, not the {PI_MOVED_PIN} tarball"
    )
    installed_manifest = REPO_ROOT / "tools" / "pi" / "node_modules" / PKG / "package.json"
    try:
        installed = json.loads(installed_manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        pytest.fail(f"the installed Pi's package.json cannot be read: {error}; run bash tools/pi/install.sh")
    assert installed.get("version") == PI_MOVED_PIN, (
        f"the installed Pi is {installed.get('version')!r}, not the moved {PI_MOVED_PIN}; run bash tools/pi/install.sh"
    )
    with tempfile.TemporaryDirectory(prefix="pi-contract-pin-") as tmp:
        env = {
            **contract_environment(),
            "HOME": tmp,
            "PI_CODING_AGENT_DIR": tmp,
        }
        try:
            done = subprocess.run(
                [str(stage2.PI_WRAPPER), "--version"],
                cwd=tmp,
                env=env,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                errors="replace",
                timeout=120,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            pytest.fail(f"the pinned Pi {PI_MOVED_PIN} could not be checked ({error}); run bash tools/pi/install.sh")
    assert done.returncode == 0 and done.stdout.strip() == PI_MOVED_PIN, (
        f"tools/pi/pi --version printed {done.stdout.strip()!r} and ended {done.returncode}, "
        f"not the moved {PI_MOVED_PIN}: {done.stderr.strip()[:400]}; run bash tools/pi/install.sh"
    )


@pytest.mark.usefixtures("installed_pi")
def test_real_catalog_move_contains_new_go_models() -> None:
    """Ledger 2: the shipped opencode-go catalog carries the 2026-11-04 Go models on the moved base.

    The evidence is the installed package's own data file - no live store, no overlay, no
    refresh; a catalog entry alone grants no permission to call its model (spec criterion 2).
    """
    catalog = {
        model["id"]: model
        for model in provider_data("opencode-go").get("openai-completions", {}).values()
        if isinstance(model, dict)
    }
    for model_id in ("kimi-k3.1-pro", "minimax-m3.1-flash", "step-5-preview"):
        model = catalog.get(model_id)
        assert model is not None, (
            f"{model_id}: absent from the installed Pi's shipped opencode-go catalog (openai-completions)"
        )
        assert model.get("api") == "openai-completions", (
            f"{model_id}: the shipped catalog files it under {model.get('api')!r}, not openai-completions"
        )
        assert model.get("baseUrl") == GO_SHIPPED, (
            f"{model_id}: the shipped base is {model.get('baseUrl')!r}, not {GO_SHIPPED}"
        )


@pytest.mark.usefixtures("installed_pi")
def test_real_catalog_move_keeps_messages_catalog_base() -> None:
    """Ledger 3: the shipped opencode-go Messages entries carry anthropic-messages on the moved base.

    Catalog evidence for the separate Messages follow-up - no wire exchange is measured or
    admitted here (spec criterion 3).
    """
    catalog = {
        model["id"]: model
        for model in provider_data("opencode-go").get("anthropic-messages", {}).values()
        if isinstance(model, dict)
    }
    for model_id in ("qwen3.8-flash", "qwen3.8-max", "qwen3.7-plus", "minimax-m3"):
        model = catalog.get(model_id)
        assert model is not None, (
            f"{model_id}: absent from the installed Pi's shipped opencode-go catalog (anthropic-messages)"
        )
        assert model.get("api") == "anthropic-messages", (
            f"{model_id}: the shipped catalog files it under {model.get('api')!r}, not anthropic-messages"
        )
        assert model.get("baseUrl") == GO_SHIPPED_MESSAGES, (
            f"{model_id}: the shipped base is {model.get('baseUrl')!r}, not {GO_SHIPPED_MESSAGES}"
        )


@pytest.mark.usefixtures("installed_pi")
@pytest.mark.parametrize("last_modified", [0, 946684800000])
@pytest.mark.parametrize("model_id", ["synthetic-protocol-check-free", "deepseek-v4.1-flash"])
def test_real_refreshed_definition_resolves_without_newer_server_date(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, last_modified: int, model_id: str
) -> None:
    """P6-14: production scratch config activates new and replaced APIs without forged cache dates.

    The activated base is an admitted same-host changed path (go-access-point):
    a foreign host would now be dropped at activation, so the exact-activation
    proof runs on the move the record admits.
    """
    definition = {
        "id": model_id,
        "provider": "opencode-go",
        "api": "openai-completions",
        "baseUrl": GO_MOVED,
        "contextWindow": 123456,
        "maxTokens": 1234,
        "reasoning": False,
        "input": ["text"],
    }
    store = {"opencode-go": {"models": [definition], "lastModified": last_modified, "checkedAt": 1234567890}}
    runtime = REPO_ROOT / "tools/pi/node_modules" / PKG / "dist/core/model-runtime.js"
    script = """
const { ModelRuntime } = await import(process.argv[1]);
globalThis.fetch = async () => { throw new Error('network forbidden'); };
const runtime = await ModelRuntime.create({
  credentials: { async read() {}, async list() { return []; } },
  modelsPath: process.argv[2], refreshOnCreate: false,
});
const result = await runtime.refresh({ providers: ['opencode-go'], allowNetwork: false });
if (runtime.getError() || result.errors.size) throw new Error(runtime.getError() || 'refresh failed');
console.log(JSON.stringify(runtime.getModel('opencode-go', process.argv[3]) ?? null));
"""
    observed = []
    real_launch = stage2.launch

    def resolve_launch(command, cwd, env, *_args, **_kwargs):
        if command[0] == "node":
            return real_launch(command, cwd, env, *_args, **_kwargs)
        agent = Path(env["PI_CODING_AGENT_DIR"])
        if "update" in command:
            (agent / "models-store.json").write_text(json.dumps(store))
            return subprocess.CompletedProcess(command, 0, "refreshed", "")
        assert json.loads((agent / "models-store.json").read_text()) == store, "server evidence was rewritten"
        done = subprocess.run(
            ["node", "--input-type=module", "-e", script, runtime.as_uri(), str(agent / "models.json"), model_id],
            cwd=cwd,
            env={**contract_environment(), "PI_OFFLINE": "1", "HOME": env["HOME"]},
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        assert done.returncode == 0, done.stderr
        resolved = json.loads(done.stdout)
        assert resolved is not None, "the fresh model was not activated"
        for field in ("api", "baseUrl", "contextWindow", "maxTokens", "input", "reasoning"):
            assert resolved[field] == definition[field], f"fresh {field} was not activated"
        observed.append(resolved)
        if "--list-models" in command:
            return subprocess.CompletedProcess(command, 0, f"provider model\nopencode-go {model_id}\n", "")
        return subprocess.CompletedProcess(command, 0, "No finding.", "")

    monkeypatch.setattr(stage2, "launch", resolve_launch)
    monkeypatch.setattr(stage2, "reviewer_key", lambda: SYNTHETIC_KEY)
    monkeypatch.setattr(
        stage2, "free_rule", lambda _root: {"provider": "opencode-go", "id_suffix": "", "include": [{"id": model_id}]}
    )
    # Discovery reads the exclusions of the declaration (DL-B-2) and drops every id when it cannot.
    # The real entry's copy carries the synthetic record: the held file has none until the
    # orchestrator's bootstrap, and a test never waits on it (plan step 8). The copy also drops the
    # candidate from `modelle`: the free stage leaves declared paid ids unselected (pi-catalog-move,
    # criterion 5), and this scratch world needs its one id selectable to prove the replaced
    # definition still activates. The declared-paid behavior itself is contract-tested in
    # tests/test_stage2_availability.py, not here.
    data = yaml.safe_load((REPO_ROOT / "model-endpoints.yaml").read_text(encoding="utf-8"))
    entry = next(item for item in data["endpunkte"] if item.get("name") == "opencode-go")
    entry["modelle"] = [model for model in entry.get("modelle") or [] if model != model_id]
    entry["adresse"] = {
        "host": "opencode.ai",
        "apis": {
            "openai-completions": {
                "basis": GO_NATIVE,
                "quelle": "the synthetic contract record (go-access-point)",
                "gelesen": "2026-10-31",
            }
        },
    }
    (tmp_path / "model-endpoints.yaml").write_text(yaml.safe_dump(data), encoding="utf-8")
    discovery = stage2.discover_free(tmp_path)
    assert discovery["selected"] == [model_id]
    assert discovery["models_store"] == store
    assert any(GO_MOVED_PATH in notice for notice in discovery["notices"]), "the same-host move ran silent"
    declare_contract_models(tmp_path)
    ctx = types.SimpleNamespace(change="demo", root=tmp_path, models_store=discovery["models_store"])
    for free in (True, False):
        stage2.run_reviewer(ctx, model_id, "Review demo.", SYNTHETIC_KEY, free=free)
    assert len(observed) == 3


@pytest.mark.usefixtures("installed_pi")
@pytest.mark.parametrize("model_id", ["synthetic-protocol-check-free", "deepseek-v4.1-flash"])
def test_real_resolution_uses_the_assessed_base(tmp_path: Path, model_id: str) -> None:
    """Ledger 4: the real pinned Pi keeps the assessed base after validation.

    The scratch state is the reviewer's own - the refreshed store and the
    models.json `activate_overlay` writes against the contract record - and
    the activated base is the record's moved path. Validation must keep it:
    a shipped or cached base returning for these ids fails the case
    (`deepseek-v4.1-flash` ships on the recorded path, so Pi knows a base to
    wrongly restore).
    """
    definition = {
        "id": model_id,
        "provider": "opencode-go",
        "api": "openai-completions",
        "baseUrl": GO_MOVED,
        "contextWindow": 123456,
        "maxTokens": 1234,
        "reasoning": False,
        "input": ["text"],
    }
    store = {"opencode-go": {"models": [definition], "lastModified": 946684800000, "checkedAt": 1234567890}}
    root = tmp_path / "declaration"
    root.mkdir()
    declare_contract_models(root)
    policy = stage2_go.load_address_policy(root)
    agent = tmp_path / "agent"
    agent.mkdir()
    (agent / "models-store.json").write_text(json.dumps(store), encoding="utf-8")
    dropped, notices = stage2.activate_overlay(agent, store, policy)
    assert dropped == {}, f"the assessed definition was dropped: {dropped}"
    assert any(GO_MOVED_PATH in notice for notice in notices), "the same-host move ran silent"
    home = tmp_path / "home"
    home.mkdir()
    stage2.check_overlay(agent, home, model_id, policy=policy)


def contract_environment() -> dict[str, str]:
    """Only runtime search and locale cross from the parent; credentials never do."""
    return {name: value for name, value in os.environ.items() if name in {"PATH", "LANG", "LC_ALL", "LC_CTYPE", "TZ"}}


def reviewer_flags() -> list[str]:
    """Capture the production prefix without starting Pi or copying its flag list."""
    commands = []

    def capture(command, *_args, **_kwargs):
        commands.append(command)
        return subprocess.CompletedProcess(command, 0, "captured", "")

    with tempfile.TemporaryDirectory(prefix="pi-flags-") as tmp, patch.object(stage2, "launch", capture):
        root = Path(tmp)
        declare_contract_models(root)
        store = {
            "opencode-go": {
                "models": [
                    {
                        "id": "contract-rung",
                        "provider": "opencode-go",
                        "api": "openai-completions",
                        "baseUrl": GO_NATIVE,
                    },
                ],
                "lastModified": 0,
            }
        }
        stage2.run_reviewer(
            types.SimpleNamespace(change="contract", root=root, models_store=store),
            "contract-rung",
            "capture only",
            SYNTHETIC_KEY,
        )
    # The overlay check launches Pi too; the reviewer's own command is the one that declares its tools.
    command = next(command for command in commands if "--tools" in command)
    return command[1 : command.index("--tools")]


REVIEWER_FLAGS = reviewer_flags()


# ---------------------------------------------------------------------------
# Criterion 6: the reviewer's tool contract, on real Pi
# ---------------------------------------------------------------------------


@pytest.mark.usefixtures("installed_pi")
def test_real_reviewer_tool_contract(project: Path, transport) -> None:
    """Criterion 6: a real reviewer-shaped call declares exactly read,grep,find,ls; an undeclared tool cannot execute."""
    standin = StandIn(
        [
            {"tool_calls": [{"name": "read", "arguments": {"path": "sentinel.txt"}}]},
            {"tool_calls": [{"name": "bash", "arguments": {"command": f"echo pwned >> {project / 'sentinel.txt'}"}}]},
            {"content": "No finding."},
        ]
    )
    transport.providers["opencode-go"] = {"baseUrl": standin.url}
    try:
        answer = stage2.run_reviewer(
            contract_ctx(project),
            "contract-rung",
            "Review the change demo as the appended instructions say.",
            SYNTHETIC_KEY,
        )
        assert "No finding." in answer, "the scripted stop never reached the runner"
        assert len(standin.requests) == 3, f"expected the scripted three turns, saw {len(standin.requests)}"
        declared = tool_names(standin.requests[0])
        assert declared == {"read", "grep", "find", "ls"}, (
            f"the model saw {sorted(declared)}, not the four reviewer tools"
        )
        assert SENTINEL_IN in message_text(standin.requests[1]), "the positive control read never executed"
        for exchange in standin.requests:
            assert tool_names(exchange) <= {"read", "grep", "find", "ls"}, "a foreign tool was declared"
        assert (project / "sentinel.txt").read_text(encoding="utf-8") == SENTINEL_IN + "\n", (
            "an undeclared tool changed the sentinel"
        )
    finally:
        standin.close()
    # the launch was the runner's own construction, through the wrapper, under the guard
    (call,) = transport.calls
    assert call["argv"][0] == str(stage2.PI_WRAPPER), "the reviewer did not start through the repository wrapper"
    assert call["argv"][call["argv"].index("--tools") + 1] == "read,grep,find,ls"
    assert call["argv"][call["argv"].index("--model") + 1] == "opencode-go/contract-rung"
    assert "NODE_OPTIONS" in call["env"] and "pi_network_guard" in call["env"]["NODE_OPTIONS"]
    assert call["env"]["OPENCODE_API_KEY"] == SYNTHETIC_KEY


def _git(project: Path, *args: str) -> None:
    run = subprocess.run(
        [
            shutil.which("git"),
            "-C",
            str(project),
            "-c",
            "user.name=t",
            "-c",
            "user.email=t@example.invalid",
            "-c",
            "commit.gpgsign=false",
            *args,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert run.returncode == 0, run.stderr


@pytest.mark.usefixtures("installed_pi")
def test_real_free_reviewer_has_only_the_implementation_diff(transport, tmp_path: Path) -> None:
    """Criterion 3: the real free launch declares no tools and its only content is the bounded diff."""
    root = tmp_path / "free-project"
    for relative, text in {
        "scripts/helpers.py": "value = 1\n",
        "docs/note.md": "DOC-CANARY-free-contract\n",
        "plans/changes/demo/plan.md": "PLAN-CANARY-free-contract\n",
        "AGENTS.md": "CONTEXT-CANARY-free-contract\n",
    }.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    declare_contract_models(root)
    _git(root, "init", "--quiet", "--initial-branch=main")
    _git(root, "add", "-A")
    _git(root, "commit", "--quiet", "-m", "base")
    _git(root, "update-ref", "refs/remotes/origin/main", "HEAD")
    # the working tree changes: one candidate source file, canaries it must not carry
    (root / "scripts" / "helpers.py").write_text("value = 2\nDIFF-CANARY-free-contract = True\n", encoding="utf-8")
    (root / "docs" / "note.md").write_text(
        "DOC-CANARY-free-contract\nDOC-CANARY-CHANGED-free-contract\n", encoding="utf-8"
    )
    (root / "AGENTS.md").write_text(
        "CONTEXT-CANARY-free-contract\nCONTEXT-CANARY-CHANGED-free-contract\n", encoding="utf-8"
    )
    (root / "tests").mkdir()
    (root / "tests" / "test_new.py").write_text("UNTRACKED-CANARY-free-contract = True\n", encoding="utf-8")
    # the prompt as the loop composes it: the free body, the round head, the answer format, the diff
    prompt = "\n\n".join(
        [
            stage2.FREE_REVIEW_BODY,
            "This is round 1; you are `acme-1-free`.",
            stage2.ANSWER_FORMAT,
            f"## The implementation diff\n\n{stage2.free_diff(root)[0]}",
        ]
    )
    standin = StandIn([{"content": "No finding."}])
    transport.providers["opencode-go"] = {"baseUrl": standin.url}
    try:
        answer = stage2.run_reviewer(
            contract_ctx(root, model="acme-1-free"),
            "acme-1-free",
            prompt,
            SYNTHETIC_KEY,
            free=True,
        )
        assert "No finding." in answer, "the scripted stop never reached the runner"
    finally:
        standin.close()
    (call,) = transport.calls
    argv = call["argv"]
    assert "--no-tools" in argv and "--tools" not in argv, "the free launch declared tools"
    assert not Path(call["cwd"]).is_relative_to(root), "the free member started in the worktree"
    (exchange,) = standin.requests
    assert tool_names(exchange) == set(), "the model was offered a tool schema"
    one = message_text(exchange)
    for canary in ("DIFF-CANARY-free-contract", "UNTRACKED-CANARY-free-contract"):
        assert canary in one, f"the diff hunk holding {canary} did not travel"
    for canary in (
        "DOC-CANARY-free-contract",
        "DOC-CANARY-CHANGED-free-contract",
        "PLAN-CANARY-free-contract",
        "CONTEXT-CANARY-free-contract",
        stage2.READ_REQUEST,
    ):
        assert canary not in one, f"a free payload carries {canary}"
    for message in exchange.body.get("messages", []):
        assert message.get("role") != "tool" and not message.get("tool_calls"), "a tool result travelled"


# ---------------------------------------------------------------------------
# Criterion 7: discovery and configuration traps stay off
# ---------------------------------------------------------------------------


EXTENSION_TRAP = (
    "// a trap extension: it marks the moment it is loaded, so its absence after a call means it never loaded\n"
    'import { appendFileSync } from "node:fs";\n'
    'appendFileSync("trap-extension-ran", "loaded");\n'
    "export default function (pi) {\n"
    '  pi.registerFlag("trap-extension-flag", { description: "armed trap", type: "boolean", default: true });\n'
    "}\n"
)


def arm_traps(project: Path) -> dict[str, str]:
    """Project resources Pi actually discovers; each has a real-Pi positive control."""
    theme = REPO_ROOT / "tools/pi/node_modules/@earendil-works/pi-coding-agent/dist/modes/interactive/theme/dark.json"
    traps = {
        ".pi/extensions/trap-extension.js": EXTENSION_TRAP,
        ".pi/skills/trap-skill/SKILL.md": "---\nname: trap-skill\ndescription: TRAP-SKILL-TEXT\n---\nTRAP-SKILL-BODY\n",
        ".pi/mcp.json": json.dumps(
            {
                "mcpServers": {
                    "trap": {"command": "node", "args": [str(DRIVER), "mcp-trap", str(project / "trap-mcp-ran")]}
                }
            }
        ),
        ".pi/prompts/trap-prompt.md": "TRAP-PROMPT-TEXT\n",
        ".pi/themes/trap-theme.json": theme.read_text(),
        "AGENTS.md": "TRAP-CONTEXT-TEXT\n",
    }
    for relative, text in traps.items():
        path = project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return traps


@pytest.mark.usefixtures("installed_pi")
def test_real_reviewer_ignores_discovery_traps(project: Path, transport) -> None:
    """Criterion 7: flags suppress armed resources even with project trust granted.

    Each positive control removes exactly its isolation flag from the captured
    production command and starts real Pi. The preload observes actual resource
    reads; it neither loads resources nor imitates Pi's discovery API.
    """
    arm_traps(project)
    checks = {
        "--no-extensions": "trap-extension-ran",
        "--no-mcp": "trap-mcp-ran",
        "--no-skills": ".pi/skills/trap-skill/SKILL.md",
        "--no-context-files": "TRAP-CONTEXT-TEXT",
        "--no-prompt-templates": ".pi/prompts/trap-prompt.md",
        "--no-themes": ".pi/themes/trap-theme.json",
    }

    def call(omit=None, trusted=True):
        for marker in ("trap-extension-ran", "trap-mcp-ran", "resource-reads.jsonl"):
            (project / marker).unlink(missing_ok=True)
        transport.controls.update(trusted=trusted, omit=omit)
        reply = {"content": "No finding."}
        if omit == "--no-mcp":
            reply["wait_for"] = str(project / "trap-mcp-ran")
        standin = StandIn([reply])
        transport.providers["opencode-go"] = {"baseUrl": standin.url}
        try:
            answer = stage2.run_reviewer(contract_ctx(project), "contract-rung", "Review demo.", SYNTHETIC_KEY)
            assert "No finding." in answer
            assert len(standin.requests) == 1
            reads = (
                (project / "resource-reads.jsonl").read_text() if (project / "resource-reads.jsonl").exists() else ""
            )
            observed = {
                "--no-extensions": (project / "trap-extension-ran").exists(),
                "--no-mcp": (project / "trap-mcp-ran").exists(),
                "--no-context-files": "TRAP-CONTEXT-TEXT" in json.dumps(standin.requests[0].body),
            }
            observed.update({flag: path in reads for flag, path in checks.items() if flag not in observed})
            return observed
        finally:
            standin.close()

    assert not any(call(trusted=False).values()), "a trap fired under the production flags"
    assert not any(call().values()), "an isolation flag failed with project trust granted"
    for flag in checks:
        # --no-extensions also suppresses the built-in MCP extension. Explicitly
        # request it in this paired control so --no-mcp is tested independently.
        transport.controls["mcp_control"] = flag == "--no-mcp"
        assert not any(call().values())
        assert call(omit=flag)[flag], f"{flag}: its real-Pi positive control did not fire"


@pytest.mark.usefixtures("installed_pi")
def test_real_reviewer_ignores_ambient_credentials(project: Path, transport, tmp_path: Path) -> None:
    """The scratch agent directory excludes saved auth and command-valued models config.

    Positive controls start real Pi with its ambient agent directory instead;
    both saved auth and model commands must demonstrably affect those calls.
    """
    ambient = tmp_path / "ambient-agent"
    ambient.mkdir()
    original_env = stage2.foreign_env

    def ambient_env(own):
        env = original_env(own)
        home_agent = Path(env["HOME"]) / ".pi" / "agent"
        home_agent.mkdir(parents=True, exist_ok=True)
        for name in ("models.json", "auth.json"):
            shutil.copyfile(ambient / name, home_agent / name)
        return env

    with patch.object(stage2, "foreign_env", ambient_env):
        for command_key in (False, True):
            marker = project / "trap-command-ran"
            standin = StandIn([{"content": "No finding."}, {"content": "positive"}])
            model = {"baseUrl": standin.url}
            if command_key:
                model["apiKey"] = f"!touch {marker}; printf {PLANTED_KEY}"
            (ambient / "models.json").write_text(json.dumps({"providers": {"opencode-go": model}}))
            (ambient / "auth.json").write_text(
                json.dumps({} if command_key else {"opencode-go": {"type": "api_key", "key": PLANTED_KEY}})
            )
            transport.providers["opencode-go"] = {"baseUrl": standin.url}
            try:
                stage2.run_reviewer(contract_ctx(project), "contract-rung", "Review demo.", SYNTHETIC_KEY)
                assert not marker.exists()
                assert PLANTED_KEY not in json.dumps(standin.requests[0].headers)
                scratch = tmp_path / ("command-control" if command_key else "auth-control")
                scratch.mkdir()
                done = run_pi(
                    project,
                    scratch,
                    *REVIEWER_FLAGS,
                    "--model",
                    "opencode-go/contract-rung",
                    "positive",
                    env_extra={"PI_CODING_AGENT_DIR": str(ambient), "OPENCODE_API_KEY": ""},
                )
                assert done.returncode == 0, done.stderr
                assert len(standin.requests) == 2
                assert PLANTED_KEY in json.dumps(standin.requests[1].headers)
                assert marker.exists() == command_key
            finally:
                standin.close()


# ---------------------------------------------------------------------------
# Criterion 8: a real extension's tool exchange
# ---------------------------------------------------------------------------


@pytest.mark.usefixtures("installed_pi")
def test_real_extension_tool_input_and_result(project: Path, tmp_path: Path) -> None:
    """Criterion 8: the registered tool receives the requested structured input and its result reaches the model."""
    scratch = scratch_of(tmp_path)
    echo_log = scratch / "echo.jsonl"
    standin = StandIn(
        [
            {
                "tool_calls": [
                    {
                        "name": "contract-echo",
                        "arguments": {"sentence": "structured input", "count": 3, "deep": {"nested": True}},
                    }
                ]
            },
            {"content": "done"},
        ]
    )
    try:
        done = run_pi(
            project,
            scratch,
            *REVIEWER_FLAGS,
            "-e",
            str(DRIVER),
            "--model",
            "opencode-go/contract-rung",
            "--",
            "Use the contract-echo tool once, then stop.",
            providers={"opencode-go": {"baseUrl": standin.url}},
            env_extra={"CONTRACT_ECHO_LOG": str(echo_log)},
        )
        assert done.returncode == 0, f"Pi ended {done.returncode}: {done.stderr[-600:]}"
        assert echo_log.is_file(), "the extension's execute never ran"
        received = [json.loads(line) for line in echo_log.read_text(encoding="utf-8").splitlines()]
        assert received == [{"sentence": "structured input", "count": 3, "deep": {"nested": True}}], (
            f"the tool received misbound input: {received}"
        )
        assert len(standin.requests) == 2, f"expected the scripted two turns, saw {len(standin.requests)}"
        result_text = message_text(standin.requests[1])
        assert "echo:structured input:3:" in result_text, (
            f"the tool result never reached the model: {result_text[:400]}"
        )
    finally:
        standin.close()


# ---------------------------------------------------------------------------
# Criterion 9: the production session policy on real Pi
# ---------------------------------------------------------------------------


@pytest.mark.usefixtures("installed_pi")
def test_real_session_policy_blocks_foreign_reads(project: Path, tmp_path: Path) -> None:
    """Criterion 9: the real policy lets the in-worktree read through and blocks the outside and symlink reads."""
    scratch = scratch_of(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "outside.txt").write_text(SENTINEL_OUT + "\n", encoding="utf-8")
    (project / "escape").symlink_to(outside)
    private = scratch / "policy"
    private.mkdir()
    copy = private / "stage2-session-policy.mjs"
    shutil.copyfile(POLICY_SOURCE, copy)
    standin = StandIn(
        [
            {"tool_calls": [{"name": "read", "arguments": {"path": "sentinel.txt"}}]},
            {"tool_calls": [{"name": "read", "arguments": {"path": "../outside/outside.txt"}}]},
            {"tool_calls": [{"name": "read", "arguments": {"path": "escape/outside.txt"}}]},
            {"content": "done"},
        ]
    )
    try:
        done = run_pi(
            project,
            scratch,
            *REVIEWER_FLAGS,
            "-e",
            str(copy),
            "--model",
            "opencode-go/contract-rung",
            "--",
            "Read the files the conversation asks for.",
            providers={"opencode-go": {"baseUrl": standin.url}},
        )
        assert done.returncode == 0, f"Pi ended {done.returncode}: {done.stderr[-600:]}"
        assert len(standin.requests) == 4, f"expected the scripted four turns, saw {len(standin.requests)}"
        assert SENTINEL_IN in message_text(standin.requests[1]), "the allowed in-worktree read never executed"
        for exchange in standin.requests:
            body = json.dumps(exchange.body)
            assert SENTINEL_OUT not in body, "an outside read's content entered a tool result"
        for exchange in standin.requests[2:4]:
            latest = [message for message in exchange.body["messages"] if message["role"] == "tool"][-1]
            assert "outside the worktree" in json.dumps(latest), latest
    finally:
        standin.close()


@pytest.mark.usefixtures("installed_pi")
def test_real_session_binding_holds_the_assessed_base(project: Path, tmp_path: Path) -> None:
    """Ledger 7: real Pi resolves the session's checked base, not the ambient one.

    The private launch directory is composed as `stage2_session.run` does it:
    the policy copy with the checked-model sidecar beside it, the definition
    the record assessed. The scratch agent configuration names another
    (`ambient`) base for the provider; the registered binding must win, and
    the request's route shows which base held.
    """
    private = tmp_path / "private"
    private.mkdir()
    copy = private / "stage2-session-policy.mjs"
    shutil.copyfile(POLICY_SOURCE, copy)
    standin = StandIn([{"content": "ok"}])
    try:
        model = {
            "id": "contract-rung",
            "name": "Contract Rung",
            "api": "openai-completions",
            "baseUrl": f"{standin.url}/checked",
            "compat": {"maxTokensField": "max_tokens"},
            "thinkingLevelMap": {"off": None, "low": "low", "high": "high"},
            "inputLimits": {"images": {"resize": {"maxWidth": 2000, "maxHeight": 2000}}},
            "reasoning": False,
            "input": ["text"],
            "contextWindow": 123456,
            "maxTokens": 1234,
        }
        (private / "checked-model.json").write_text(
            json.dumps({"provider": "opencode-go", "model": model}),
            encoding="utf-8",
        )
        done = run_pi(
            project,
            scratch_of(tmp_path),
            *REVIEWER_FLAGS,
            "-e",
            str(copy),
            "--model",
            "opencode-go/contract-rung",
            "answer ok",
            providers={"opencode-go": {"baseUrl": f"{standin.url}/ambient"}},
        )
        assert done.returncode == 0, f"Pi ended {done.returncode}: {done.stderr[-600:]}"
        assert len(standin.requests) == 1, f"expected one scripted turn, saw {len(standin.requests)}"
        (exchange,) = standin.requests
        assert "/checked/chat/completions" in exchange.path, (
            f"the ambient base won over the checked binding: {exchange.path}"
        )
        assert exchange.body.get("max_tokens") == model["maxTokens"], "the checked compat flag was lost"
        assert "max_completion_tokens" not in exchange.body
    finally:
        standin.close()


# ---------------------------------------------------------------------------
# Criterion 10: the model listing is a real provider table
# ---------------------------------------------------------------------------


@pytest.mark.usefixtures("installed_pi")
def test_real_model_listing_is_a_provider_table(tmp_path: Path) -> None:
    """Criterion 10: `--list-models` on real Pi prints a table naming both OpenCode providers, no credential echoed."""
    scratch = scratch_of(tmp_path)
    done = run_pi(scratch, scratch, "--list-models", timeout=120)
    assert done.returncode == 0, f"the listing ended {done.returncode}: {done.stderr[-600:]}"
    table = done.stdout
    with pytest.raises(json.JSONDecodeError):
        json.loads(table)
    # the real table: a header row naming the provider and model columns, then one row per model
    # whose first column is the provider id - `opencode` (Zen) is a different id from `opencode-go`
    lines = [line.split() for line in table.splitlines() if line.strip()]
    assert lines and lines[0][:2] == ["provider", "model"], f"the listing is no provider/model table: {lines[:1]}"
    providers = {row[0] for row in lines[1:]}
    assert "opencode-go" in providers, "the opencode-go provider is absent from the real listing"
    assert "opencode" in providers, "the opencode (Zen) provider is absent from the real listing"
    assert SYNTHETIC_KEY not in table and PLANTED_KEY not in table, "a credential was echoed into the listing"


# ---------------------------------------------------------------------------
# Criterion 11: the OpenCode providers' native addresses and key mapping
# ---------------------------------------------------------------------------


@pytest.mark.usefixtures("installed_pi")
def test_real_opencode_provider_contracts(tmp_path: Path) -> None:
    """Criterion 11: the native addresses hold in the installed sources, and each provider's request carries only the synthetic key."""
    # the chat-completions wire API is the one the runner's requests take (`/chat/completions`);
    # the shipped 1.5.0 catalog carries its own Go base (GO_SHIPPED, spec criteria 2-3), while the
    # synthetic GO_NATIVE record above keeps its own starting point for the loopback fixtures
    assert native_base_urls("opencode-go", "openai-completions") == {GO_SHIPPED}, (
        f"the installed opencode-go catalog's native base is not the shipped {GO_SHIPPED}"
    )
    assert native_base_urls("opencode", "openai-completions") == {ZEN_SHIPPED}, (
        f"the installed opencode (Zen) catalog's native base is not the shipped {ZEN_SHIPPED}"
    )
    catalog = {model["id"]: model for model in provider_data("opencode-go")["openai-completions"].values()}
    # Every admitted rung must use the measured wire API, including ids carried
    # under another API in Pi's shipped catalog. Missing ids fail closed too.
    for rung in stage2.ladder(REPO_ROOT):
        assert rung in catalog, f"{rung}: wire API not measured as openai-completions"
        assert catalog[rung]["baseUrl"] == GO_SHIPPED
    scratch = scratch_of(tmp_path)
    for provider, model in (("opencode-go", "contract-go-model"), ("opencode", "contract-zen-model")):
        standin = StandIn([{"content": "ok"}])
        try:
            done = run_pi(
                scratch,
                scratch,
                *REVIEWER_FLAGS,
                "--model",
                f"{provider}/{model}",
                "answer ok",
                providers={name: {"baseUrl": standin.url} for name in ("opencode-go", "opencode")},
            )
            assert done.returncode == 0, f"{provider} ended {done.returncode}: {done.stderr[-600:]}"
            assert standin.requests, f"the {provider} request never reached the loopback override"
            (exchange,) = standin.requests
            assert exchange.path.endswith("/chat/completions"), f"the {provider} request took an unexpected route"
            assert exchange.body.get("model") == model, (
                f"the {provider} model id arrived as {exchange.body.get('model')!r}"
            )
            headers = json.dumps(exchange.headers)
            assert SYNTHETIC_KEY in headers, (
                f"the synthetic OPENCODE_API_KEY never authenticated the {provider} request"
            )
            assert PLANTED_KEY not in headers, "a foreign credential authenticated the request"
            assert SYNTHETIC_KEY not in json.dumps(exchange.body), f"the {provider} key travelled in the body"
        finally:
            standin.close()


# ---------------------------------------------------------------------------
# Criterion 11: the network guard denies every external destination
# ---------------------------------------------------------------------------


def test_contract_network_guard_denies_external_destinations(tmp_path: Path) -> None:
    """Criterion 11: the guard allows the loopback and denies every planted external attempt; no real request is made."""
    if shutil.which("node") is None:
        pytest.fail("the guard contract needs Node on PATH; missing prerequisites fail, they do not skip")
    standin = StandIn([{"content": "ok"}])
    try:
        done = subprocess.run(
            ["node", "--import", str(GUARD), str(DRIVER), "network-guard", f"{standin.url}/ping"],
            cwd=tmp_path,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
    finally:
        standin.close()
    assert done.returncode == 0, f"the guard driver crashed: {done.stderr[-600:]}"
    outcomes = {}
    for line in done.stdout.splitlines():
        if line.strip():
            record = json.loads(line)
            outcomes[record["attempt"]] = record["outcome"]
    assert outcomes.get("loopback-fetch") == "allowed", f"the guard broke the loopback: {outcomes}"
    for name in ("external-fetch", "external-http", "external-net", "external-tls"):
        assert outcomes.get(name) == "denied", f"the guard let {name} through: {outcomes.get(name)!r}"


# ---------------------------------------------------------------------------
# Criterion 12: prerequisites and failures are mandatory
# ---------------------------------------------------------------------------


@pytest.mark.usefixtures("installed_pi")
def test_contract_prerequisites_and_failures_are_mandatory(
    project: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Criterion 12: missing Pi, missing Node, a wrong pin, a timeout and a malformed exchange fail - none skips."""
    with monkeypatch.context() as quiet, pytest.raises(pytest.fail.Exception, match="need Node"):
        quiet.setattr(shutil, "which", lambda *_: None)
        require_installed_pi()
    with monkeypatch.context() as quiet, pytest.raises(pytest.fail.Exception, match="install.sh"):
        quiet.setattr(stage2, "PI_WRAPPER", tmp_path / "no-wrapper-here")
        require_installed_pi()

    class Off:
        returncode = 0
        stdout = "9.9.9\n"
        stderr = ""

    with (
        monkeypatch.context() as quiet,
        pytest.raises(pytest.fail.Exception, match="not installed or will not start"),
    ):
        quiet.setattr(subprocess, "run", lambda *_args, **_kwargs: Off())
        require_installed_pi()

    # a stand-in that sleeps past the limit is a failed contract, not a slow skip
    slow = StandIn([{"sleep": 30}])
    try:
        with pytest.raises(ContractFailure, match="did not end within"):
            run_pi(
                project,
                tmp_path,
                *REVIEWER_FLAGS,
                "--model",
                "opencode-go/contract-rung",
                "answer briefly",
                providers={"opencode-go": {"baseUrl": slow.url}},
                timeout=2,
            )
    finally:
        slow.close()

    # an exchange the script cannot answer fails loudly instead of passing
    empty = StandIn([])
    try:
        done = run_pi(
            project,
            tmp_path,
            *REVIEWER_FLAGS,
            "--model",
            "opencode-go/contract-rung",
            "answer briefly",
            providers={"opencode-go": {"baseUrl": empty.url}},
        )
        assert done.returncode != 0, "Pi succeeded against a stand-in that could not answer"
        assert empty.failures, "the stand-in swallowed the unusable exchange"
    finally:
        empty.close()


@pytest.mark.usefixtures("installed_pi")
def test_real_truncated_pi_print_failure_is_refused(project: Path, transport) -> None:
    """Criterion 13: the runner refuses the real Pi result of a length finish.

    Measured on Pi 1.2.0: Pi appends a context edit that removes the truncated
    assistant message before printing, so the process returns zero with empty
    stdout. The runner's empty-answer guard refuses it; the separate unit test
    covers nonzero print refusals.
    """
    standin = StandIn([{"content": "partial review", "finish_reason": "length"}])
    transport.providers["opencode-go"] = {"baseUrl": standin.url}
    try:
        with pytest.raises(stage2.CallFailed, match="answer is empty"):
            stage2.run_reviewer(contract_ctx(project), "contract-rung", "Review demo.", SYNTHETIC_KEY)
        assert len(standin.requests) == 1
        result = transport.calls[-1]["result"]
        assert result.returncode == 0 and not result.stdout.strip(), (
            "Pi's measured truncated-print behavior changed; recheck the refusal path"
        )
    finally:
        standin.close()


@pytest.mark.usefixtures("installed_pi")
def test_contract_environment_excludes_parent_provider_keys(
    project: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A parent provider secret cannot enter the real Pi process."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", PLANTED_KEY)
    log = tmp_path / "child-env.json"
    standin = StandIn([{"content": "ok"}])
    try:
        done = run_pi(
            project,
            scratch_of(tmp_path),
            *REVIEWER_FLAGS,
            "-e",
            str(DRIVER),
            "--model",
            "opencode-go/contract-rung",
            "ok",
            providers={"opencode-go": {"baseUrl": standin.url}},
            env_extra={"CONTRACT_ENV_LOG": str(log)},
        )
        assert done.returncode == 0, done.stderr
        child = json.loads(log.read_text())
        assert "ANTHROPIC_API_KEY" not in child
        assert PLANTED_KEY not in json.dumps(child)
        assert child["OPENCODE_API_KEY"] == SYNTHETIC_KEY
    finally:
        standin.close()


@pytest.mark.usefixtures("installed_pi")
def test_real_catalog_headers_remain_literal(tmp_path: Path) -> None:
    """P6-15, as RS-3-3 changed it: pinned Pi's real composer sees no catalog header, so none is executed or sent."""
    headers = {
        "X-Command": "!printf catalog-command-ran",
        "X-Env": "$CATALOG_SECRET/${CATALOG_SECRET}",
        "X-Escapes": "$$ $! ! trailing$",
        "X-Plain": "catalog-value",
    }
    store = {
        stage2.OPENCODE: {
            "models": [
                {
                    "id": "synthetic-free",
                    "api": "openai-completions",
                    "baseUrl": GO_NATIVE,
                    "headers": headers,
                }
            ],
            "lastModified": 0,
        }
    }
    evidence = json.dumps(store)
    stage2.activate_overlay(tmp_path, store, contract_address_policy())
    composer = REPO_ROOT / "tools/pi/node_modules" / PKG / "dist/core/provider-composer.js"
    script = """
import fs from 'node:fs';
const { resolveConfiguredModelHeaders } = await import(process.argv[1]);
const config = JSON.parse(fs.readFileSync(process.argv[2], 'utf8')).providers['opencode-go'];
const model = { id: 'synthetic-free', provider: 'opencode-go', type: 'chat' };
console.log(JSON.stringify(resolveConfiguredModelHeaders(model, config, undefined,
  { CATALOG_SECRET: 'environment-must-not-be-read' })));
"""
    done = subprocess.run(
        ["node", "--input-type=module", "-e", script, composer.as_uri(), str(tmp_path / "models.json")],
        cwd=tmp_path,
        env=contract_environment(),
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert done.returncode == 0, done.stderr
    # Since RS-3-3 (change review-loop-deep-b) catalog headers are not activated at all: Pi neither
    # evaluates nor sends them.
    assert "catalog-command-ran" not in done.stdout and "catalog-value" not in done.stdout
    assert "headers" not in (tmp_path / "models.json").read_text()
    assert json.dumps(store) == evidence


# ---------------------------------------------------------------------------
# Both free-model preparations on the shipped Go catalog (bead coding-harness-wb40, spec criteria 9-10)
# ---------------------------------------------------------------------------

GO = "opencode-go"
CONTRACT_NOW = dt.datetime(2026, 11, 5, 12, 0, tzinfo=dt.UTC)


def shipped_go_models() -> list[dict]:
    """Every opencode-go model of the installed Pi's own catalog, one row per id, whatever its wire API.

    The rows are the shipped data itself - the contract invents no roster. An id the package files under
    two wire APIs keeps its first row, as a fresh catalog holds one row per id.
    """
    rows: dict[str, dict] = {}
    for section in provider_data(GO).values():
        if not isinstance(section, dict):
            continue
        for model in section.values():
            if isinstance(model, dict) and isinstance(model.get("id"), str):
                rows.setdefault(model["id"], {**model, "provider": GO})
    if not rows:
        pytest.fail("the installed Pi's opencode-go catalog holds no model; run bash tools/pi/install.sh")
    return list(rows.values())


@pytest.fixture
def offline_world(
    world: World, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, catalog_sources
) -> types.SimpleNamespace:
    """A test world holding the repository's current declaration and the installed Pi's shipped Go catalog.

    Only the sources are local stand-ins: the forced refresh writes the shipped rows as the fresh overlay,
    the listing is the real pinned Pi's own, the capability evidence is synthetic, every model request is
    answered by the world's stand-in program, and Python may reach no non-loopback address.
    """
    models = shipped_go_models()
    ids = {m["id"] for m in models}
    if "beam-free" not in ids:
        pytest.fail("the installed Pi's catalog no longer carries beam-free; the collision is not exercised")
    scratch = scratch_of(tmp_path)
    with monkeypatch.context() as real:
        real.setattr(stage2, "PI_WRAPPER", REAL_PI_WRAPPER)
        done = run_pi(scratch, scratch, "--list-models", timeout=120, env_extra={"PATH": REAL_PATH})
    if done.returncode != 0:
        pytest.fail(f"the real Pi listing ended {done.returncode}: {done.stderr[-600:]}")
    listing = done.stdout

    shutil.copyfile(REPO_ROOT / "model-endpoints.yaml", world.root / "model-endpoints.yaml")
    text = world.research.read_text(encoding="utf-8").replace("class: bounded", "class: feature\nneighbours: []")
    world.research.write_text(text, encoding="utf-8")
    run_git(world.root, "add", "-A")
    run_git(world.root, "commit", "--quiet", "-m", "the repository's current declaration")
    declaration = yaml.safe_load((world.root / "model-endpoints.yaml").read_text(encoding="utf-8"))
    entry = next(item for item in declaration["endpunkte"] if item["name"] == GO)

    real_connect = socket.socket.connect

    def loopback_only(self, address, *args, **kwargs):
        if isinstance(address, tuple) and address[0] not in ("127.0.0.1", "::1", "localhost"):
            raise AssertionError(f"the offline contract tried to reach {address[0]}")
        return real_connect(self, address, *args, **kwargs)

    monkeypatch.setattr(socket.socket, "connect", loopback_only)

    def no_intelligence(_key):
        raise AssertionError("the offline contract tried to read the intelligence source")

    monkeypatch.delenv(availability.INTELLIGENCE_KEY_ENV, raising=False)
    monkeypatch.setattr(availability, "INTELLIGENCE_FETCH", no_intelligence)
    monkeypatch.setattr(availability, "now", lambda: CONTRACT_NOW)
    monkeypatch.setattr(stage2, "terms_today", lambda: CONTRACT_NOW.date())
    # The real catalog_bridge launches the production helper's CLI, which imports the pinned
    # runtime, reads its baseline and constructs the bridge. Only HTTP transport is redirected:
    # Pi's source serves unmodified shipped rows as a synthetic fresh response; models.dev's
    # tool support is labelled synthetic evidence, not a capability claim about these models.
    catalog_sources.pi_models = models
    catalog_sources.metadata = {
        "source": "synthetic successful capability evidence for the offline preparation contract",
        GO: {"models": {m["id"]: {"id": m["id"], "tool_call": True} for m in models}},
    }
    preload = tmp_path / "synthetic-catalog-transport.mjs"
    preload.write_text(
        f"import {json.dumps(GUARD.as_uri())};\n"
        "const fetch = globalThis.fetch;\n"
        f"const local = {json.dumps(catalog_sources.url)};\n"
        "globalThis.fetch = (input, init) => {\n"
        "  const url = new URL(input instanceof Request ? input.url : input);\n"
        "  if (url.origin === 'https://pi.dev' && url.pathname === '/api/models/providers/opencode-go')\n"
        "    return fetch(local + url.pathname + url.search, init);\n"
        "  if (url.href === 'https://models.dev/api.json') return fetch(local + '/metadata', init);\n"
        "  return fetch(input, init);\n"
        "};\n",
        encoding="utf-8",
    )
    real_run = subprocess.run
    helper = REPO_ROOT / "scripts" / "stage2_research_catalog.mjs"

    def local_catalog_transport(command, *args, **kwargs):
        if len(command) == 2 and str(command[1]) == str(helper):
            command = [shutil.which("node", path=REAL_PATH), command[1]]
            kwargs["env"] = {
                **kwargs["env"],
                "PATH": REAL_PATH,
                "NODE_OPTIONS": f"--import {preload}",
            }
        return real_run(command, *args, **kwargs)

    monkeypatch.setattr(subprocess, "run", local_catalog_transport)
    monkeypatch.setenv("PATH", os.environ["PATH"] + os.pathsep + REAL_PATH)
    real_launch = stage2.launch

    def local_sources(command, cwd, env, *args, **kwargs):
        if "update" in command and "--models" in command:
            store = {GO: {"models": models, "lastModified": 0, "checkedAt": 1}}
            (Path(env["PI_CODING_AGENT_DIR"]) / "models-store.json").write_text(json.dumps(store), encoding="utf-8")
            return subprocess.CompletedProcess(command, 0, "refreshed", "")
        if "--list-models" in command:
            return subprocess.CompletedProcess(command, 0, listing, "")
        return real_launch(command, cwd, env, *args, **kwargs)

    monkeypatch.setattr(stage2, "launch", local_sources)
    return types.SimpleNamespace(
        world=world,
        catalog_sources=catalog_sources,
        paid={str(model) for model in entry["modelle"]},
        free_ids=sorted(i for i in ids if i.endswith("-free")),
    )


def probed_models(calls: list[dict]) -> set[str]:
    return {
        call["argv"][call["argv"].index("--model") + 1].split("/")[-1] for call in calls if "--model" in call["argv"]
    }


def run_offline_contract(setup: types.SimpleNamespace) -> None:
    """Run both production preparations on the shipped catalog; an AssertionError names what broke.

    The preparations are the production `prepare-loop` and `prepare-explore` paths; the contract checks the
    complete receipts and that no paid id is a free member of either.
    """
    w = setup.world
    w.script(pi=[{"stdout": "OK"}] * 400, claude=[{"stdout": "OK"}] * 12)
    start = len(w.reviews())
    assert w.run("prepare-loop") == 0, "the review preparation refused the shipped Go catalog"
    review = json.loads(w.record().with_name("availability.json").read_text(encoding="utf-8"))
    assert availability.verify(review, review["report_id"]), "the review receipt is not a valid sealed receipt"
    state = review["state"]
    assert not set(state["free"]["selected"]) & setup.paid, "a paid id is a free member of the review swarm"
    assert "paid model" in state["availability"]["skipped"].get("beam-free", ""), "review hides the paid drop"
    assert f"Skipped: beam-free: {stage2_free.PAID_REASON}" in availability.report(state)
    review_calls = w.reviews()[start:]
    assert "beam-free" not in probed_models(review_calls), "review probed a paid id as a free candidate"

    middle = len(w.reviews())
    assert w.run("prepare-explore", "demo") == 0, "the research preparation refused the shipped Go catalog"
    path = availability.research_receipt_path("demo", stage2, w.root)
    research = json.loads(path.read_text(encoding="utf-8"))
    assert availability.verify(research, research["report_id"]), "the research receipt is not a valid sealed receipt"
    state = research["state"]
    reasons = {item["id"]: item["reason"] for item in state["catalog"]["candidates"]}
    assert reasons.get("beam-free") == "paid-admitted", f"research kept the paid id: {reasons.get('beam-free')}"
    assert not set(state["free"]["selected"]) & setup.paid, "a paid id is a free member of the research swarm"
    assert f"Dropped (free): beam-free: {stage2_free.PAID_REASON}" in availability.research_report(state)
    source_requests = setup.catalog_sources.requests
    assert any(path.startswith("/api/models/providers/opencode-go") for path, _ in source_requests), (
        "the research catalog helper did not retrieve the shipped rows through the local Pi source"
    )
    assert any(path == "/metadata" for path, _ in source_requests), "synthetic capability evidence was not read"
    research_calls = w.reviews()[middle:]
    assert "beam-free" not in probed_models(research_calls), "research probed a paid id as a free candidate"
    for call in [*review_calls, *research_calls]:
        assert call["path"] == str(w.bin / "pin-pi"), "a model request left the stand-in program"


@pytest.mark.usefixtures("installed_pi")
def test_shipped_catalog_prepares_both_swarms_offline(offline_world: types.SimpleNamespace) -> None:
    """Criterion 9: both production preparations run on the installed Pi's shipped Go catalog, offline.

    The shipped catalog carries `beam-free`, which the declaration admits as paid: both preparations drop it
    before any probe and still finish with a sealed receipt. A catalog move that breaks either preparation
    fails here, before merge; missing prerequisites fail the test, they never skip it.
    """
    run_offline_contract(offline_world)


@pytest.mark.usefixtures("installed_pi")
@pytest.mark.parametrize(
    "fault_name, expected, diagnostic",
    [
        (
            "review preparation refuses",
            "the review preparation refused the shipped Go catalog",
            "planted: the review preparation refuses",
        ),
        (
            "research preparation refuses",
            "the research preparation refused the shipped Go catalog",
            "planted: the research preparation refuses",
        ),
        (
            "research catalog helper refuses",
            "the research preparation refused the shipped Go catalog",
            "planted: the production research catalog helper refuses",
        ),
        (
            "review bypasses the shared selection",
            "the review preparation refused the shipped Go catalog",
            f"refused: the model beam-free is {stage2_free.PAID_REASON}",
        ),
        (
            "research bypasses the shared selection",
            "the research preparation refused the shipped Go catalog",
            f"refused: beam-free is {stage2_free.PAID_REASON}",
        ),
    ],
)
def test_both_preparation_contracts_detect_planted_faults(
    offline_world: types.SimpleNamespace,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    fault_name: str,
    expected: str,
    diagnostic: str,
) -> None:
    """Criterion 10: the same contract assertions fail for a refusing or bypassing preparation, on either path.

    Planted faults, one at a time: the review preparation refuses, the research preparation refuses, the
    review preparation skips the shared selection's paid veto, the research preparation does the same.
    """
    # Parametrization gives every fault a fresh world and a clean control.
    run_offline_contract(offline_world)  # no fault, no failure
    capsys.readouterr()  # Only the fault run may supply its diagnostic.

    def refuse_review(*_args, **_kwargs):
        raise stage2.Refused("planted: the review preparation refuses")

    def refuse_research(*_args, **_kwargs):
        raise stage2_swarm.ResearchCatalogError("planted: the research preparation refuses")

    def bypass(include_adds: bool):
        real = stage2_free.select

        def planted(candidates, policy, **kwargs):
            if policy.include_adds == include_adds:
                kwargs["paid"] = ()
            return real(candidates, policy, **kwargs)

        return planted

    real_run = subprocess.run

    def refuse_catalog_helper(command, *args, **kwargs):
        if len(command) == 2 and str(command[1]) == str(REPO_ROOT / "scripts/stage2_research_catalog.mjs"):
            return subprocess.CompletedProcess(
                command,
                1,
                json.dumps({"exit_code": 1, "reason": "planted: the production research catalog helper refuses"}),
                "",
            )
        return real_run(command, *args, **kwargs)

    faults = {
        "research catalog helper refuses": (subprocess, "run", refuse_catalog_helper),
        "review preparation refuses": (stage2, "discover_free", refuse_review),
        "research preparation refuses": (stage2_swarm, "select_research_catalog", refuse_research),
        "review bypasses the shared selection": (stage2_free, "select", bypass(True)),
        "research bypasses the shared selection": (stage2_free, "select", bypass(False)),
    }
    target, attribute, planted = faults[fault_name]
    with monkeypatch.context() as fault:
        fault.setattr(target, attribute, planted)
        with pytest.raises(AssertionError, match="^" + re.escape(expected) + r"(?:\n|$)"):
            run_offline_contract(offline_world)
        assert diagnostic in capsys.readouterr().err, "the contract failed for a different cause than the planted fault"
