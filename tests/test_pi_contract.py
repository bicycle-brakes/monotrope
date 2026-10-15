"""The offline Pi contracts: the real pinned Pi against a loopback stand-in.

Every case here starts the actual installed Pi through the repository wrapper
(`tools/pi/pi`), pointed at a loopback HTTP stand-in that answers OpenAI-style
chat completions from a script: a tool call, a stop, an error. No hosted
model, no user configuration, no external network: the credentials are
synthetic, the HOME and agent directories are scratch, and a test-only preload
(`tests/pi_network_guard.mjs`) denies every non-loopback connection the child
attempts. The reviewer-shaped cases run the runner's own `run_reviewer` and
inject only the test transport at its subprocess seam - no second flag list
exists.

Missing Pi, missing Node, a refused loopback bind, a timeout or a malformed
exchange FAILS its case (spec, criterion 12). The suite never skips.

Each test comes with its fault: armed traps, an undeclared tool, an outside
path, a foreign credential or a broken exchange is planted one at a time and
named in the test.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import types
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import stage2  # noqa: E402

PKG = "@earendil-works/pi-coding-agent"
GUARD = REPO_ROOT / "tests" / "pi_network_guard.mjs"
DRIVER = REPO_ROOT / "tests" / "pi_contract_driver.mjs"
POLICY_SOURCE = REPO_ROOT / "scripts" / "stage2_session_policy.mjs"
SYNTHETIC_KEY = "ok-contract-synthetic-key"
PLANTED_KEY = "ok-TRAP-credential-never-send"
SENTINEL_IN = "INSIDE-CONTENT-7f3a41"
SENTINEL_OUT = "OUTSIDE-SENTINEL-b2c95e"
GO_NATIVE = "https://opencode.ai/zen/go/v1"
ZEN_NATIVE = "https://opencode.ai/zen/v1"


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
            **os.environ,
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
            finish = "stop"
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
        **os.environ,
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

    The launch command itself stays production code: the seam adds only the
    network-guard preload and plants the scratch `models.json` that repoints
    the OpenCode providers at the loopback stand-in. No second isolation-flag
    list is maintained here - the reviewer flags are `run_reviewer`'s own.
    """
    calls: list[dict] = []
    providers: dict = {}
    original_launch = stage2.launch
    original_env = stage2.foreign_env

    def guarded_launch(command, cwd, env, key=None, timeout=None, limit=None):
        env = {**env, "NODE_OPTIONS": f"--import {GUARD}"}
        calls.append({"argv": list(command), "cwd": str(cwd), "env": dict(env)})
        return original_launch(command, cwd, env, key, timeout=timeout, limit=limit)

    def planted_env(own):
        env = original_env(own)
        agent = env.get("PI_CODING_AGENT_DIR")
        if agent and providers:
            Path(agent, "models.json").write_text(json.dumps({"providers": providers}), encoding="utf-8")
        return env

    monkeypatch.setattr(stage2, "launch", guarded_launch)
    monkeypatch.setattr(stage2, "foreign_env", planted_env)
    return types.SimpleNamespace(calls=calls, providers=providers)


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """A controlled project: one sentinel file a tool may read."""
    root = tmp_path / "project"
    root.mkdir()
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


REVIEWER_FLAGS = [
    "--print",
    "--no-session",
    "--no-approve",
    "--no-extensions",
    "--no-mcp",
    "--no-skills",
    "--no-prompt-templates",
    "--no-themes",
    "--offline",
]


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
        ctx = types.SimpleNamespace(change="demo", root=project)
        answer = stage2.run_reviewer(
            ctx, "contract-rung", "Review the change demo as the appended instructions say.", SYNTHETIC_KEY
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
    """Plant the discovery and configuration traps in the project, with their markers' names."""
    traps = {
        ".pi/extensions/trap-extension.mjs": EXTENSION_TRAP,
        ".pi/agent/models.json": json.dumps(
            {"providers": {"opencode-go": {"baseUrl": "http://127.0.0.1:9/v1", "apiKey": "!touch trap-command-ran"}}}
        ),
        ".pi/skills/trap-skill/SKILL.md": "TRAP-SKILL-TEXT\n",
        ".pi/mcp.json": json.dumps({"mcpServers": {"trap": {"command": "touch", "args": ["trap-mcp-ran"]}}}),
        ".pi/prompts/trap-prompt.md": "TRAP-PROMPT-TEXT\n",
        ".pi/themes/trap-theme.json": json.dumps({"colors": {"primary": "#000000"}}),
        ".pi/auth.json": json.dumps({"opencode-go": {"key": PLANTED_KEY}}),
        "AGENTS.md": "TRAP-CONTEXT-TEXT\n",
    }
    for relative, text in traps.items():
        path = project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return traps


@pytest.mark.usefixtures("installed_pi")
def test_real_reviewer_ignores_discovery_traps(project: Path, transport) -> None:
    """Criterion 7: among armed traps the clean reviewer call uses only its scratch configuration."""
    arm_traps(project)
    # positive activation controls: each trap leaves its marker when it really executes
    done = subprocess.run(
        ["node", str(project / ".pi" / "extensions" / "trap-extension.mjs")],
        cwd=project,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert done.returncode == 0, done.stderr
    assert (project / "trap-extension-ran").is_file(), "the extension trap cannot prove its own execution"
    subprocess.run(["touch", "trap-command-ran"], cwd=project, capture_output=True, timeout=60, check=True)
    for marker in ("trap-extension-ran", "trap-command-ran"):
        (project / marker).unlink()

    standin = StandIn([{"content": "No finding."}])
    transport.providers["opencode-go"] = {"baseUrl": standin.url}
    try:
        ctx = types.SimpleNamespace(change="demo", root=project)
        answer = stage2.run_reviewer(
            ctx, "contract-rung", "Review the change demo as the appended instructions say.", SYNTHETIC_KEY
        )
        assert "No finding." in answer
        assert len(standin.requests) == 1, "the call went anywhere but the loopback stand-in"
    finally:
        standin.close()
    for marker in (
        "trap-extension-ran",
        "trap-command-ran",
        "trap-mcp-ran",
    ):
        assert not (project / marker).exists(), f"the armed trap {marker} fired"
    for exchange in standin.requests:
        assert "TRAP-CONTEXT-TEXT" not in json.dumps(exchange.body), "a planted context file reached the model"
        assert PLANTED_KEY not in json.dumps(exchange.body), "a planted credential reached the model"
        assert PLANTED_KEY not in json.dumps(exchange.headers), "a planted credential travelled in a header"
        assert "127.0.0.1:9" not in json.dumps(exchange.body), "a planted baseUrl reached the exchange"


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
            "--print",
            "--no-session",
            "--no-approve",
            "--no-extensions",
            "-e",
            str(copy),
            "--no-mcp",
            "--no-skills",
            "--no-prompt-templates",
            "--no-themes",
            "--offline",
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
        blocked = message_text(standin.requests[2]) + message_text(standin.requests[3])
        assert "outside the worktree" in blocked, f"the policy's refusal is not visible to the model: {blocked[:400]}"
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
    # the chat-completions wire API is the one the runner's requests take (`/chat/completions`)
    assert native_base_urls("opencode-go", "openai-completions") == {GO_NATIVE}, (
        "the installed opencode-go catalog lost its native address"
    )
    assert native_base_urls("opencode", "openai-completions") == {ZEN_NATIVE}, (
        "the installed opencode (Zen) catalog lost its native address"
    )
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
