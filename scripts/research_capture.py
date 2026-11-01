#!/usr/bin/env python3
"""The attended F-1 offline capture of the research swarm's free-context isolation.

Phase-6 finding F-1 and plan step 6 require evidence that the real pinned Pi,
started through the swarm's own launch paths, sends no private context and has
no local tool in a free (public) context. This tool produces that evidence
without any external request:

* a scratch world: a fake repository (canaries in tracked files, git history
  and an untracked file, plus discovery traps), a fake HOME (dotfiles, ssh-like
  and claude-like directories) and a fake XDG_STATE_HOME outside that HOME;
  fake API-key-shaped canaries in the parent environment;
* a loopback OpenAI-compatible mock server that records every request (the
  full JSON body, tool schemas, headers with the transport key redacted) and
  answers from a script that asks the model side to call file, shell and
  private-address tools;
* the swarm's real command builders (`Run.pi_command` for the online, online
  free and repository seats; `stage2_availability.probe_go` for the reachability
  probe) pointed at that server through the same `models.json` the runner
  writes into Pi's agent directory, started through `stage2.PI_WRAPPER`;
* a verdict per criterion 8, 9 and 47 from what the server recorded: missing
  evidence is FAIL, never PASS.

The real Pi runs only with `--attended` (the maintainer is present, F-1).
`--dry-run-stand-in` swaps in a stand-in Pi so the tool itself can be tested.
Exit: 0 all verdicts PASS, 1 a verdict FAIL, 2 refused or unusable.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import ipaddress
import json
import os
import re
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
from dataclasses import dataclass, field
from datetime import UTC, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
GUARD = REPO_ROOT / "tests" / "pi_network_guard.mjs"
SCHEMA_VERSION = 1
GO = "opencode-go"
PUBLIC_TOOLS = frozenset({"public_search", "public_fetch"})
FIXED_MODELS = ("deepseek-v4.1-flash", "mimo-v2.6-pro", "qwen3.8-flash")
FREE_MODELS = ("alpha-free", "beta-free")
ONLINE_MODEL, REPOSITORY_MODEL, PROBE_MODEL = FIXED_MODELS[0], FIXED_MODELS[2], FIXED_MODELS[1]
FIXTURE_CHANGE = "capture-fixture"
# The capture's own Go address record, the shape `stage2_go` reads: the fake
# repository's `model-endpoints.yaml` declares it, so the seat launches resolve
# their offline defaults against a valid record instead of the working tree's
# held file. The bases name the real documented host; only the installed rows
# are re-pointed at the mock by the capture's transport hardening seam.
CAPTURE_ADDRESS = {
    "host": "opencode.ai",
    "apis": {
        "openai-completions": {
            "basis": "https://opencode.ai/zen/go/v1",
            "quelle": "https://opencode.ai/docs/go (the capture's fixture record)",
            "gelesen": "2026-10-31",
        }
    },
}
ERROR_TEXT = re.compile(
    r"(error|not found|unknown tool|denied|refus|blocked|not allowed|invalid|forbidden|unavailable|failed|cannot"
    r"|no such|unsupported|not available"
    # The destination check's own refusals read as statements, not as errors (the 2026-10-19 real-Pi capture):
    # "only https:// destinations are fetched - no http, no file" and "only port 443 is fetched".
    r"|only https|only port|no http, no file)",
    re.I,
)
SENSITIVE_HEADERS = ("authorization", "x-api-key", "api-key", "proxy-authorization")
OS_SANDBOX_PROFILE = (
    '(version 1)(allow default)(deny network-outbound)(allow network-outbound (remote ip "localhost:*"))'
)


# ---------------------------------------------------------------------------
# The mock model server
# ---------------------------------------------------------------------------


class MockServer:
    """Loopback OpenAI-compatible server: records every request, answers from a per-seat script.

    `/m/<seat>/v1/chat/completions` is a model call; `/api/models/providers/opencode-go` and `/metadata` are
    the two catalog sources; anything else is a `sink` hit (a tool that reached the server it must not).
    """

    def __init__(self, secrets: list[str] | tuple[str, ...] = ()) -> None:
        self.secrets = [s for s in secrets if s]
        self.records: list[dict] = []
        self.scripts: dict[str, list[dict]] = {}
        self.counters: dict[str, int] = {}
        self.catalog_models: list[dict] = []
        self.metadata: dict = {}
        self.lock = threading.Lock()
        self._server = ThreadingHTTPServer(("127.0.0.1", 0), _handler_class(self))
        self._server.daemon_threads = True
        self.port = self._server.server_address[1]
        self.url = f"http://127.0.0.1:{self.port}"
        self._thread = threading.Thread(target=lambda: self._server.serve_forever(poll_interval=0.05), daemon=True)

    def __enter__(self) -> MockServer:
        self._thread.start()
        return self

    def __exit__(self, *_exc: object) -> None:
        self._server.shutdown()
        self._server.server_close()
        self._thread.join(timeout=10)

    def script(self, seat: str, steps: list[dict]) -> None:
        self.scripts[seat] = list(steps)

    def redact(self, text: str) -> str:
        for secret in self.secrets:
            text = text.replace(secret, "[REDACTED]")
        return text

    def record(self, kind: str, seat: str | None, method: str, path: str, headers: dict, body) -> dict:
        lowered = {name.lower(): value for name, value in headers.items()}
        auth = "absent"
        token = lowered.get("authorization", "") or lowered.get("x-api-key", "") or lowered.get("api-key", "")
        if token:
            auth = "present-matches-transport-key" if any(s in token for s in self.secrets) else "present-other"
        shown = {
            name: ("[REDACTED]" if name in SENSITIVE_HEADERS else self.redact(value)) for name, value in lowered.items()
        }
        with self.lock:
            key = seat or kind
            index = self.counters.get(key, 0)
            self.counters[key] = index + 1
            item = {
                "seat": seat,
                "kind": kind,
                "index": index,
                "method": method,
                "path": path,
                "headers": shown,
                "auth": auth,
                "body": body,
                "at": datetime.now(UTC).isoformat(timespec="milliseconds"),
            }
            self.records.append(item)
        return item

    def next_step(self, seat: str) -> dict | None:
        with self.lock:
            steps = self.scripts.get(seat) or []
            return steps.pop(0) if steps else None


def _handler_class(server: MockServer):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *_args: object) -> None:
            pass

        def _send(self, status: int, kind: str, data: bytes) -> None:
            try:
                self.send_response(status)
                self.send_header("Content-Type", kind)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            except OSError:
                pass

        def _body(self):
            length = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(length) if length else b""
            if not raw.strip():
                return None
            try:
                return json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, ValueError):
                return {"unparseable": raw.decode("utf-8", errors="replace")[:2000]}

        def do_GET(self) -> None:  # noqa: N802 - stdlib callback
            path = self.path.split("?", 1)[0]
            if path == "/api/models/providers/opencode-go":
                server.record("catalog", "catalog", "GET", self.path, dict(self.headers), None)
                self._send(200, "application/json", json.dumps(server.catalog_models).encode())
            elif path == "/metadata":
                server.record("catalog", "metadata", "GET", self.path, dict(self.headers), None)
                self._send(200, "application/json", json.dumps(server.metadata).encode())
            else:
                server.record("sink", None, "GET", self.path, dict(self.headers), None)
                self._send(200, "text/plain", b"sink\n")

        def do_POST(self) -> None:  # noqa: N802
            body = self._body()
            match = re.fullmatch(r"/m/([^/]+)/v1/chat/completions", self.path)
            if not match:
                server.record("sink", None, "POST", self.path, dict(self.headers), body)
                self._send(404, "application/json", b'{"error":{"message":"no route"}}')
                return
            seat = match.group(1)
            record = server.record("model", seat, "POST", self.path, dict(self.headers), body)
            step = server.next_step(seat)
            if step is None:
                step = {"content": "No finding."}
                record["script_exhausted"] = True
            record["answered_tool_calls"] = [call["name"] for call in step.get("tool_calls", [])]
            self._answer(step, body if isinstance(body, dict) else {})

        def _answer(self, step: dict, request: dict) -> None:
            if "tool_calls" in step:
                message = {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": f"call_{index}",
                            "type": "function",
                            "function": {"name": call["name"], "arguments": json.dumps(call["arguments"])},
                        }
                        for index, call in enumerate(step["tool_calls"])
                    ],
                }
                finish = "tool_calls"
            else:
                message = {"role": "assistant", "content": step.get("content", "No finding."), "tool_calls": None}
                finish = "stop"
            payload = {
                "id": "chatcmpl-capture",
                "object": "chat.completion",
                "created": 1760486400,
                "model": request.get("model", "capture-model"),
                "choices": [{"index": 0, "message": message, "finish_reason": finish}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20},
            }
            if request.get("stream"):
                chunk = {
                    "id": payload["id"],
                    "object": "chat.completion.chunk",
                    "created": payload["created"],
                    "model": payload["model"],
                    "choices": [{"index": 0, "delta": message, "finish_reason": finish}],
                }
                data = b"data: " + json.dumps(chunk).encode() + b"\n\ndata: [DONE]\n\n"
                self._send(200, "text/event-stream", data)
            else:
                self._send(200, "application/json", json.dumps(payload).encode())

    return Handler


# ---------------------------------------------------------------------------
# Reading recorded exchanges
# ---------------------------------------------------------------------------


def _flat(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            part.get("text", json.dumps(part)) if isinstance(part, dict) else str(part) for part in content
        )
    return "" if content is None else json.dumps(content)


def tool_schemas(body) -> list[dict]:
    """The tools a request declared, however the provider schema nests them."""
    found = []
    for tool in (body or {}).get("tools") or []:
        inner = tool.get("function") if isinstance(tool.get("function"), dict) else tool
        found.append(
            {
                "name": inner.get("name"),
                "description": inner.get("description"),
                "parameters": inner.get("parameters"),
            }
        )
    return found


def declared_tool_names(records: list[dict]) -> set[str]:
    return {s["name"] for r in records for s in tool_schemas(r.get("body")) if s.get("name")}


def tool_attempts(records: list[dict]) -> list[dict]:
    """Every tool call the script made a seat attempt, with the outcome the next request carried back."""
    calls: dict[str, dict] = {}
    results: dict[str, str] = {}
    for record in records:
        for message in (record.get("body") or {}).get("messages") or []:
            if message.get("role") == "assistant":
                for call in message.get("tool_calls") or []:
                    function = call.get("function") or {}
                    raw = function.get("arguments")
                    try:
                        arguments = json.loads(raw) if isinstance(raw, str) else (raw or {})
                    except ValueError:
                        arguments = {"raw": raw}
                    calls.setdefault(
                        call.get("id"), {"id": call.get("id"), "name": function.get("name"), "arguments": arguments}
                    )
            elif message.get("role") == "tool":
                results[message.get("tool_call_id")] = _flat(message.get("content"))
    attempts = []
    for ident, call in calls.items():
        text = results.get(ident)
        outcome = "no-result-recorded" if text is None else ("error" if ERROR_TEXT.search(text) else "returned-content")
        attempts.append({**call, "outcome": outcome, "result_excerpt": (text or "")[:400]})
    return attempts


def _private_address(url: str) -> bool:
    host = urlsplit(url).hostname or ""
    if host in ("localhost", "") or host.endswith(".localhost"):
        return True
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        return False
    return address.is_private or address.is_loopback or address.is_link_local or address.is_reserved


def _scan_text(record: dict) -> dict[str, str]:
    return {
        "body": json.dumps(record.get("body"), sort_keys=True, ensure_ascii=False),
        "headers": json.dumps(record.get("headers"), sort_keys=True, ensure_ascii=False),
        "path": str(record.get("path") or ""),
    }


def canary_hits(records: list[dict], canaries: list[dict]) -> dict[str, list[dict]]:
    """For every canary, each recorded exchange and part (body, headers, path) where its value appears."""
    hits: dict[str, list[dict]] = {c["name"]: [] for c in canaries}
    for record in records:
        parts = _scan_text(record)
        for canary in canaries:
            for where, text in parts.items():
                if canary["value"] in text:
                    hits[canary["name"]].append(
                        {"seat": record.get("seat"), "index": record.get("index"), "where": where}
                    )
    return hits


def _check(criterion: str, title: str, reasons: list[str], failed: bool, evidence: dict | None = None, observed=False):
    verdict = "FAIL" if failed else ("OBSERVED" if observed else "PASS")
    return {"criterion": criterion, "title": title, "verdict": verdict, "reasons": reasons, "evidence": evidence or {}}


def evaluate(records: list[dict], canaries: list[dict], seat_kinds: dict[str, str], **_extra) -> list[dict]:
    """Verdicts for criteria 8, 9 and 47 (and the repository seat's isolation), from the recorded exchanges."""
    by_seat: dict[str, list[dict]] = {}
    for record in records:
        if record.get("kind") == "model":
            by_seat.setdefault(record["seat"], []).append(record)
    public = [seat for seat, kind in seat_kinds.items() if kind == "public"]
    probes = [seat for seat, kind in seat_kinds.items() if kind == "probe"]
    repositories = [seat for seat, kind in seat_kinds.items() if kind == "repository"]
    sinks = [r for r in records if r.get("kind") == "sink"]
    catalog = [r for r in records if r.get("kind") == "catalog"]
    hits = canary_hits(records, canaries)

    def hit_list(seats: list[str], *, only: set[str] | None = None, first_only=False) -> list[str]:
        found = []
        for canary in canaries:
            if only is not None and canary["class"] not in only:
                continue
            for hit in hits[canary["name"]]:
                if hit["seat"] in seats and (not first_only or hit["index"] == 0):
                    found.append(
                        f"{canary['name']} ({canary['class']}) in {hit['seat']} request {hit['index']} {hit['where']}"
                    )
        return found

    checks = []
    # Criterion 8: no private canary in any outbound request of a free context, the probe or the catalog reads.
    reasons, failed = [], False
    silent = [seat for seat in public if not by_seat.get(seat)]
    if not public or silent:
        failed = True
        reasons.append(f"no recorded model request for public seat(s) {silent or 'at all'}: missing evidence is FAIL")
    found = hit_list(public + ["catalog", "metadata"])
    found += [f"{c['name']} in a sink request" for c in canaries for h in hits[c["name"]] if h["seat"] is None]
    if found:
        failed = True
        reasons += [f"private canary reached an outbound request: {item}" for item in found]
    for record in catalog:
        if record.get("auth") != "absent" or "cookie" in (record.get("headers") or {}):
            failed = True
            reasons.append(f"a catalog request carried credentials ({record.get('path')})")
    if not failed:
        reasons.append(
            f"{sum(len(by_seat[s]) for s in public)} public-seat request(s) and {len(catalog)} catalog request(s) "
            "carry no canary and no credential"
        )
    checks.append(_check("8", "No private canary in an outbound request of a free context", reasons, failed))

    # Criterion 9: no local tool, no private-address reach, no discovered private context in a free context.
    reasons, failed = [], False
    for seat in public:
        names = declared_tool_names(by_seat.get(seat, []))
        extra = sorted(names - PUBLIC_TOOLS)
        if not names:
            failed = True
            reasons.append(f"{seat}: no tool schema recorded: missing evidence is FAIL")
        if extra:
            failed = True
            reasons.append(f"{seat}: local tool(s) declared in a free context: {extra}")
        attempts = tool_attempts(by_seat.get(seat, []))
        promised = sum(len(r.get("answered_tool_calls") or []) for r in by_seat.get(seat, []))
        if promised and (len(attempts) < promised or any(a["outcome"] == "no-result-recorded" for a in attempts)):
            failed = True
            reasons.append(
                f"{seat}: {promised} tool call(s) were asked for but only {len(attempts)} result(s) came back: missing evidence is FAIL"
            )
        for attempt in attempts:
            url = (attempt["arguments"] or {}).get("url", "") if isinstance(attempt["arguments"], dict) else ""
            undeclared = attempt["name"] not in PUBLIC_TOOLS
            private = attempt["name"] == "public_fetch" and url and _private_address(url)
            if (undeclared or private) and attempt["outcome"] != "error":
                failed = True
                reasons.append(
                    f"{seat}: {attempt['name']} {attempt['arguments']} was not refused ({attempt['outcome']})"
                )
    if sinks:
        failed = True
        reasons += [f"a request reached the sink server: {r.get('method', '?')} {r['path']}" for r in sinks]
    if not failed:
        reasons.append("only the public tools were declared; file, shell and private-address attempts were refused")
    checks.append(_check("9", "No local tool, private-address reach or discovered private context", reasons, failed))

    # Criterion 47: the reachability probe's payload carries no canary and declares no tool.
    reasons, failed = [], False
    silent = [seat for seat in probes if not by_seat.get(seat)]
    if not probes or silent:
        failed = True
        reasons.append("no recorded probe request: missing evidence is FAIL")
    found = hit_list(probes)
    if found:
        failed = True
        reasons += [f"private canary in the probe payload: {item}" for item in found]
    tools = declared_tool_names([r for seat in probes for r in by_seat.get(seat, [])])
    if tools:
        failed = True
        reasons.append(f"the probe declared tool(s): {sorted(tools)}")
    if not failed:
        reasons.append("the probe payload carries no canary and declares no tool")
    checks.append(_check("47", "The reachability probe's outbound payload", reasons, failed))

    if repositories:
        reasons, failed, observed = [], False, False
        silent = [seat for seat in repositories if not by_seat.get(seat)]
        if silent:
            failed = True
            reasons.append(f"no recorded request for {silent}")
        first = hit_list(repositories, first_only=True)
        if first:
            failed = True
            reasons += [f"canary in the first request (before any tool ran): {item}" for item in first]
        always = hit_list(repositories, only={"env", "state", "transport-key"})
        if always:
            failed = True
            reasons += [f"canary that must never reach a model: {item}" for item in always]
        later = hit_list(repositories, only={"home"})
        if later:
            # The path lock (Q-16) is required now, so a home read is a regression of F-24, not an observation
            # (deep review RS-1-4).
            failed = True
            reasons += [f"home canary read past the path lock (finding F-24): {item}" for item in later]
        if not failed and not observed:
            reasons.append("no environment, home, state or transport-key canary reached the repository seat")
        checks.append(
            _check(
                "repository-seat",
                "Repository seat: parent environment and state stay out",
                reasons,
                failed,
                observed=observed,
            )
        )
    return checks


# ---------------------------------------------------------------------------
# The scratch world
# ---------------------------------------------------------------------------


@dataclass
class World:
    root: Path
    repo: Path
    home: Path
    state_home: Path
    canaries: list[dict]
    parent_env: dict[str, str]
    key: str
    dead_port: int
    notes: list[str] = field(default_factory=list)


def _git(repo: Path, home: Path, *args: str) -> None:
    env = {
        "PATH": os.environ.get("PATH", ""),
        "HOME": str(home),
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_AUTHOR_NAME": "Capture",
        "GIT_AUTHOR_EMAIL": "capture@example.invalid",
        "GIT_COMMITTER_NAME": "Capture",
        "GIT_COMMITTER_EMAIL": "capture@example.invalid",
    }
    subprocess.run(
        ["git", "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", "-C", str(repo), *args],
        env=env,
        check=True,
        capture_output=True,
        stdin=subprocess.DEVNULL,
    )


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def build_world(scratch: Path, seed: str | None = None) -> World:
    """Fake repository, HOME and state directory with synthetic canaries; nothing real is read."""
    root = Path(scratch)
    root.mkdir(parents=True, exist_ok=True)
    repo, home, state_home = root / "repo", root / "home", root / "xdg-state"
    for directory in (repo, home, state_home):
        directory.mkdir(parents=True, exist_ok=True)

    def canary(name: str, klass: str) -> dict:
        digest = hashlib.sha256(f"{seed}:{name}".encode()).hexdigest()[:12] if seed else secrets.token_hex(6)
        prefix = {"transport-key": "CANARY-KEY"}.get(klass, f"CANARY-{klass.upper().replace('-', '')}")
        return {"name": name, "class": klass, "value": f"{prefix}-{digest}"}

    canaries: dict[str, dict] = {}

    def add(name: str, klass: str) -> str:
        canaries[name] = canary(name, klass)
        return canaries[name]["value"]

    # the fake HOME: dotfiles, ssh-like and claude-like directories
    where = {}
    for name, relative in (
        ("home-ssh", ".ssh/id_canary"),
        ("home-bashrc", ".bashrc"),
        ("home-claude", ".claude/CLAUDE.md"),
        ("home-gh", ".config/gh/hosts.yml"),
        ("home-aws", ".aws/credentials"),
    ):
        value = add(name, "home")
        target = home / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"synthetic {name}: {value}\n", encoding="utf-8")
        where[name] = f"$HOME/{relative}"
    # the fake state store, outside the fake HOME (Q-15)
    state_file = state_home / "coding-harness" / "stage2" / FIXTURE_CHANGE / "research" / "canary-state.txt"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(f"synthetic stored peer result: {add('state-store', 'state')}\n", encoding="utf-8")
    where["state-store"] = "$XDG_STATE_HOME/.../canary-state.txt"
    # the fake repository
    (repo / "AGENTS.md").write_text(
        f"# Fixture rules\nsynthetic tracked rule {add('repo-tracked', 'repo')}\n", encoding="utf-8"
    )
    where["repo-tracked"] = "repo/AGENTS.md (tracked, a context file Pi would discover)"
    (repo / "CLAUDE.md").write_text("See AGENTS.md.\n", encoding="utf-8")
    skill = repo / ".pi" / "skills" / "trap" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text(f"---\nname: trap\ndescription: trap\n---\n{add('repo-skill', 'repo')}\n", encoding="utf-8")
    where["repo-skill"] = "repo/.pi/skills/trap/SKILL.md (tracked discovery trap)"
    prompts = repo / ".pi" / "prompts"
    prompts.mkdir(parents=True)
    (prompts / "trap.md").write_text(f"{add('repo-prompt', 'repo')}\n", encoding="utf-8")
    where["repo-prompt"] = "repo/.pi/prompts/trap.md (tracked discovery trap)"
    (repo / "README.md").write_text("fixture\n", encoding="utf-8")
    (repo / "model-endpoints.yaml").write_text(capture_declaration(), encoding="utf-8")
    _git(repo, home, "init", "-q", "-b", "main")
    _git(repo, home, "add", "-A")
    _git(repo, home, "commit", "-q", "-m", "fixture")
    history = repo / "history-secret.txt"
    history.write_text(f"{add('repo-history', 'repo')}\n", encoding="utf-8")
    _git(repo, home, "add", "history-secret.txt")
    _git(repo, home, "commit", "-q", "-m", "add a secret")
    _git(repo, home, "rm", "-q", "history-secret.txt")
    _git(repo, home, "commit", "-q", "-m", "remove the secret (still in history)")
    where["repo-history"] = "repo git history only (added then removed)"
    (repo / "untracked-notes.txt").write_text(f"{add('repo-untracked', 'repo')}\n", encoding="utf-8")
    where["repo-untracked"] = "repo/untracked-notes.txt (untracked)"
    # the parent environment
    parent_env: dict[str, str] = {}
    for name, variable in (
        ("env-key", "AWS_SECRET_ACCESS_KEY"),
        ("env-anthropic", "ANTHROPIC_API_KEY"),
        ("env-openai", "OPENAI_API_KEY"),
        ("env-token", "GITHUB_TOKEN"),
    ):
        parent_env[variable] = add(name, "env")
        where[name] = f"parent environment variable {variable}"
    key = add("transport-key", "transport-key")
    where["transport-key"] = "OPENCODE_API_KEY handed to Pi (allowed in the Authorization header only)"
    dead = _free_port()
    parent_env.update(HOME=str(home), XDG_STATE_HOME=str(state_home))
    parent_env.update(
        {
            name: f"http://127.0.0.1:{dead}"
            for name in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy")
        }
    )
    parent_env.update(NO_PROXY="127.0.0.1,localhost", no_proxy="127.0.0.1,localhost")
    ordered = []
    for item in canaries.values():
        ordered.append({**item, "where": where[item["name"]]})
    return World(root, repo, home, state_home, ordered, parent_env, key, dead)


@contextlib.contextmanager
def replaced_environment(parent_env: dict[str, str]):
    """The process environment becomes the synthetic parent environment (plus PATH and locale); restored after."""
    saved = dict(os.environ)
    keep = {
        name: saved[name] for name in ("PATH", "LANG", "LC_ALL", "LC_CTYPE", "TERM", "TZ", "TMPDIR") if name in saved
    }
    os.environ.clear()
    os.environ.update(keep)
    os.environ.update(parent_env)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(saved)


# ---------------------------------------------------------------------------
# The stand-in Pi (--dry-run-stand-in)
# ---------------------------------------------------------------------------

STAND_IN = r"""#!{python}
# research-capture stand-in Pi: posts the request a Pi seat would send to the base URL of its
# models.json, follows scripted tool calls (undeclared tools are refused), prints the final text.
import json, os, sys, urllib.request
args = sys.argv[1:]
if args[:1] == ["--version"]:
    print("{pin}")
    sys.exit(0)
def option(name):
    return args[args.index(name) + 1] if name in args else None
model = option("--model").split("/", 1)[1]
agent = os.environ["PI_CODING_AGENT_DIR"]
models = json.load(open(os.path.join(agent, "models.json")))["providers"]["opencode-go"]["models"]
base = next(m["baseUrl"] for m in models if m["id"] == model)
tools = [] if "--no-tools" in args else [t for t in (option("--tools") or "").split(",") if t]
system = open(option("--append-system-prompt")).read() if os.path.isfile(option("--append-system-prompt") or "") else ""
messages = [{{"role": "system", "content": system}}, {{"role": "user", "content": args[-1]}}]
leak = os.environ.get("LEAK_CANARY")
if leak:
    messages[1]["content"] += " " + leak
def post():
    body = {{"model": model, "messages": messages, "stream": True}}
    if tools:
        body["tools"] = [{{"type": "function", "function": {{"name": t, "description": t,
                          "parameters": {{"type": "object", "properties": {{}}}}}}}} for t in tools]
    req = urllib.request.Request(base + "/chat/completions", data=json.dumps(body).encode(),
        headers={{"Content-Type": "application/json", "Authorization": "Bearer " + os.environ.get("OPENCODE_API_KEY", "")}})
    raw = urllib.request.urlopen(req, timeout=30).read().decode()
    line = next(l for l in raw.splitlines() if l.startswith("data: {{"))
    choice = json.loads(line[6:])["choices"][0]
    return choice.get("message") or choice["delta"]
for _ in range(3):
    message = post()
    calls = message.get("tool_calls") or []
    if not calls:
        print(message.get("content") or "")
        break
    messages.append({{"role": "assistant", "content": None, "tool_calls": calls}})
    for call in calls:
        name = call["function"]["name"]
        text = "stand-in ran " + name if name in tools else "Error: tool " + name + " not found"
        if name in ("public_fetch", "public_search") and name in tools:
            text = "Error: stand-in has no network; the destination is refused"
        messages.append({{"role": "tool", "tool_call_id": call["id"], "content": text}})
"""


def install_stand_in(directory: Path, pin: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "pin-standin-pi"
    path.write_text(STAND_IN.format(python=sys.executable, pin=pin), encoding="utf-8")
    path.chmod(0o755)
    return path


# ---------------------------------------------------------------------------
# Driving the swarm's real launch paths
# ---------------------------------------------------------------------------


class Runner:
    """The runner module as the swarm sees it, with the Pi wrapper (and the launch seam) swapped in."""

    def __init__(self, stage2, wrapper: Path, hardening, calls: list[dict]) -> None:
        self._stage2 = stage2
        self.PI_WRAPPER = wrapper
        self._hardening = hardening
        self.calls = calls

    def __getattr__(self, name: str):
        return getattr(self._stage2, name)

    def launch(self, command, root, env, secret=None, timeout=None, limit=None):
        command, env = self._hardening(list(command), dict(env))
        done = self._stage2.launch(command, root, env, secret, timeout=timeout, limit=limit)
        self.calls.append({"argv": command, "returncode": done.returncode, "stderr": done.stderr or ""})
        return done


def render_prompt(name: str, topic: str) -> str:
    base = (REPO_ROOT / "prompts" / "research-swarm" / name).read_text(encoding="utf-8")
    report = (REPO_ROOT / "prompts" / "research-swarm" / "report.md").read_text(encoding="utf-8")
    base = (
        base.replace("{{TOPIC_ID}}", "1")
        .replace("{{TOPIC_NAME}}", "Synthetic capture topic")
        .replace("{{TOPIC_SCOPE}}", "A synthetic scope that names no real file.")
        .replace("{{TOPIC}}", topic)
    )
    return f"{base}\n\n{report}"


def public_script(port: int, home: Path) -> list[dict]:
    attempts = [
        {"name": "public_fetch", "arguments": {"url": f"http://127.0.0.1:{port}/sink/private-http"}},
        {"name": "public_fetch", "arguments": {"url": f"https://127.0.0.1:{port}/sink/private-https"}},
        {"name": "public_fetch", "arguments": {"url": "https://169.254.169.254/latest/meta-data/"}},
        {"name": "public_fetch", "arguments": {"url": "https://localhost/"}},
        {"name": "public_search", "arguments": {"query": "synthetic capture query"}},
        {"name": "read", "arguments": {"path": str(home / ".ssh" / "id_canary")}},
        {"name": "read", "arguments": {"path": "AGENTS.md"}},
        {"name": "bash", "arguments": {"command": "cat ~/.ssh/id_canary; env"}},
        {"name": "ls", "arguments": {"path": "."}},
    ]
    return [{"tool_calls": attempts}, {"content": "No finding."}]


def repository_script(world: World) -> list[dict]:
    attempts = [
        {"name": "read", "arguments": {"path": "AGENTS.md"}},
        {"name": "read", "arguments": {"path": "untracked-notes.txt"}},
        {"name": "read", "arguments": {"path": str(world.home / ".ssh" / "id_canary")}},
        {"name": "read", "arguments": {"path": str(next(world.state_home.rglob("canary-state.txt")))}},
        {"name": "grep", "arguments": {"pattern": "CANARY", "path": "."}},
        {"name": "ls", "arguments": {"path": "."}},
    ]
    return [{"tool_calls": attempts}, {"content": "No finding."}]


def catalog_fixture(server: MockServer) -> None:
    def definition(ident: str) -> dict:
        return {
            "id": ident,
            "name": ident,
            "provider": GO,
            "api": "openai-completions",
            "baseUrl": "https://opencode.ai/zen/go/v1",
            "reasoning": False,
            "input": ["text"],
            "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
            "contextWindow": 128000,
            "maxTokens": 4096,
        }

    server.catalog_models = [definition(i) for i in (*FIXED_MODELS, *FREE_MODELS)]
    server.metadata = {GO: {"models": {i: {"id": i, "tool_call": True} for i in FREE_MODELS}}}


CATALOG_DRIVER = r"""
const { collectCatalog } = await import(process.argv[1]);
console.log(JSON.stringify(await collectCatalog(JSON.parse(process.argv[2]))));
"""


def collect_catalog(runner, server: MockServer, hardening) -> tuple[dict, list[str]]:
    """The real pinned-Pi catalog helper and the real selection, with both sources replaced by the mock."""
    import stage2_swarm

    helper = SCRIPT_DIR / "stage2_research_catalog.mjs"
    with tempfile.TemporaryDirectory(prefix="capture-catalog-") as tmp:
        env = runner.foreign_env({"HOME": tmp, "PI_CODING_AGENT_DIR": tmp})
        command, env = hardening(
            [
                "node",
                "--input-type=module",
                "-e",
                CATALOG_DRIVER,
                helper.as_uri(),
                json.dumps({"catalogBaseUrl": server.url, "metadataUrl": server.url + "/metadata"}),
            ],
            env,
        )
        done = subprocess.run(
            command, cwd=tmp, env=env, capture_output=True, text=True, timeout=90, check=False, stdin=subprocess.DEVNULL
        )
    if done.returncode != 0:
        raise RuntimeError(f"the catalog helper ended {done.returncode}: {done.stderr[-400:]}")
    bridge = json.loads(done.stdout)
    selection = stage2_swarm.select_research_catalog(
        bridge,
        {"provider": GO, "suffix": "-free", "include": [], "exclude": []},
        list(FIXED_MODELS),
        expected_version=runner.PI_VERSION,
        address=capture_policy(),
    )
    return selection, [line for line in done.stderr.splitlines() if "pi-network-guard" in line]


def synthetic_selection(pin: str) -> dict:
    """Stand-in mode has no pinned Pi to run the catalog helper: a labelled synthetic selection."""
    store = {GO: {"models": [], "lastModified": 0}}
    return {
        "selected": list(FREE_MODELS),
        "N": len(FREE_MODELS),
        "pi_version": pin,
        "selection_outcome": "selected",
        "synthetic": True,
        "models_store": store,
    }


def capture_policy():
    """The address policy of the capture's own record, as `stage2_go` holds one."""
    import stage2_go

    records = {
        api: stage2_go.BaseRecord(api=api, base=part["basis"], source=part["quelle"], read=part["gelesen"])
        for api, part in CAPTURE_ADDRESS["apis"].items()
    }
    return stage2_go.AddressPolicy(host=CAPTURE_ADDRESS["host"], apis=records)


def capture_declaration() -> str:
    """The fake repository's `model-endpoints.yaml`: the capture's own address record."""
    api, record = next(iter(CAPTURE_ADDRESS["apis"].items()))
    return (
        "endpunkte:\n"
        f"  - name: {GO}\n"
        "    adresse:\n"
        f"      host: {CAPTURE_ADDRESS['host']}\n"
        "      apis:\n"
        f"        {api}:\n"
        f"          basis: {json.dumps(record['basis'])}\n"
        f"          quelle: {json.dumps(record['quelle'])}\n"
        f"          gelesen: {json.dumps(record['gelesen'])}\n"
    )


def store_for_run(selection: dict, labels: dict[str, str]) -> dict:
    """Copy the fetched store, filling synthetic stand-in rows from the fixture record."""
    store = json.loads(json.dumps(selection["models_store"]))
    entry = store.setdefault(GO, {"models": []})
    known = {m["id"] for m in entry["models"]}
    template = next(iter(entry["models"]), None) or {
        "name": "x",
        "provider": GO,
        "api": "openai-completions",
        "reasoning": False,
        "input": ["text"],
        "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
        "contextWindow": 128000,
        "maxTokens": 4096,
    }
    for ident in labels:
        if ident not in known:
            entry["models"].append({**template, "id": ident, "name": ident})
    for model in entry["models"]:
        if "baseUrl" not in model:
            model["baseUrl"] = CAPTURE_ADDRESS["apis"][model["api"]]["basis"]
    return store


def tree_hash(directory: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in directory.rglob("*") if p.is_file()):
        digest.update(path.relative_to(directory).as_posix().encode() + b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def sha256_file(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def pi_facts(stage2, wrapper: Path, full: bool) -> dict:
    pi_dir = REPO_ROOT / "tools" / "pi"
    packages = pi_dir / "node_modules" / "@earendil-works"
    facts: dict = {
        "pin": stage2.PI_VERSION,
        "wrapper": str(wrapper),
        "wrapper_sha256": sha256_file(wrapper),
        "pin_manifest_sha256": sha256_file(pi_dir / "package.json"),
        "lock_sha256": sha256_file(pi_dir / "package-lock.json"),
        "node_version_declared": (pi_dir / ".node-version").read_text().strip()
        if (pi_dir / ".node-version").is_file()
        else None,
    }
    try:
        lock = json.loads((pi_dir / "package-lock.json").read_text(encoding="utf-8"))
        entry = lock["packages"]["node_modules/@earendil-works/pi-coding-agent"]
        facts["lock_entry"] = {
            "version": entry.get("version"),
            "integrity": entry.get("integrity"),
            "resolved": entry.get("resolved"),
        }
    except (OSError, KeyError, ValueError):
        facts["lock_entry"] = "not read"
    installed = packages / "pi-coding-agent" / "package.json"
    try:
        facts["installed_version"] = json.loads(installed.read_text(encoding="utf-8")).get("version")
    except (OSError, ValueError):
        facts["installed_version"] = "not installed"
    if full and packages.is_dir():
        facts["source_hashes"] = {p.name: tree_hash(p) for p in sorted(packages.iterdir()) if p.is_dir()}
    else:
        facts["source_hashes"] = "not computed (stand-in mode)" if not full else "not installed"
    with contextlib.suppress(OSError, subprocess.SubprocessError):
        facts["node_version_measured"] = subprocess.run(
            ["node", "--version"], capture_output=True, text=True, timeout=20, check=False
        ).stdout.strip()
    return facts


def commit_of() -> dict:
    def git(*args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(REPO_ROOT), *args], capture_output=True, text=True, check=False
        ).stdout.strip()

    return {
        "sha": git("rev-parse", "HEAD"),
        "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "dirty": bool(git("status", "--porcelain")),
    }


def excerpt(text: str, limit: int = 600) -> str:
    return text if len(text) <= limit else text[:limit] + f"... [{len(text) - limit} more characters]"


def state_store_guard(world: World) -> dict:
    """Q-15 evidence: the runner's own placement guard on the fake state store, and on one inside the fake HOME."""
    from stage2_research_store import Store, StoreWriteError, research_dir

    outcomes = {}
    git_dir = world.repo / ".git"
    for label, state in (("outside-home", world.state_home), ("inside-home", world.home / ".local" / "state")):
        saved = os.environ.get("XDG_STATE_HOME")
        os.environ["XDG_STATE_HOME"] = str(state)
        try:
            Store(research_dir(FIXTURE_CHANGE, REPO_ROOT)).assert_outside(world.repo, git_dir, home=world.home)
            outcomes[label] = "accepted"
        except StoreWriteError as error:
            outcomes[label] = f"refused: {error}"
        finally:
            if saved is None:
                os.environ.pop("XDG_STATE_HOME", None)
            else:
                os.environ["XDG_STATE_HOME"] = saved
    return outcomes


# ---------------------------------------------------------------------------
# The run
# ---------------------------------------------------------------------------


def execute(args, scratch: Path) -> dict:
    import stage2
    import stage2_availability
    from stage2_research_run import Run

    real = not args.dry_run_stand_in
    world = build_world(scratch / "world", seed=args.seed)
    wrapper = stage2.PI_WRAPPER if real else install_stand_in(scratch / "bin", stage2.PI_VERSION)
    if real and not GUARD.is_file():
        raise RuntimeError(f"the network guard {GUARD} is missing; the real Pi does not start without it")
    sandbox = bool(args.os_sandbox and sys.platform == "darwin" and shutil.which("sandbox-exec"))
    guard_lines: list[str] = []
    runner_calls: list[dict] = []
    transport_routes: list[dict] = []

    def hardening(command: list[str], env: dict[str, str]):
        """Everything the capture adds around a production command: the guard, dead proxies, the optional OS sandbox."""
        # This capture-only transport seam runs after production command construction
        # and (for the probe) dispatch admission. Never hand a loopback row to admission.
        agent = env.get("PI_CODING_AGENT_DIR")
        models_path = Path(agent) / "models.json" if agent else None
        if models_path is not None and models_path.is_file():
            installed = json.loads(models_path.read_text(encoding="utf-8"))
            for row in installed.get("providers", {}).get(GO, {}).get("models", []):
                route = f"{server.url}/m/{labels.get(row['id'], 'unused-' + row['id'])}/v1"
                transport_routes.append({"model": row["id"], "original_base": row["baseUrl"], "mock_base": route})
                row["baseUrl"] = route
            models_path.write_text(json.dumps(installed), encoding="utf-8")
        for name in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
            env[name] = f"http://127.0.0.1:{world.dead_port}"
        env.update(NO_PROXY="127.0.0.1,localhost", no_proxy="127.0.0.1,localhost")
        if real:
            env["NODE_OPTIONS"] = f"--import {GUARD}"
        if args.stand_in_leak and not real:
            env["LEAK_CANARY"] = next(c["value"] for c in world.canaries if c["name"] == "env-key")
        if sandbox:
            command = ["sandbox-exec", "-p", OS_SANDBOX_PROFILE, *command]
        return command, env

    key = world.key
    with replaced_environment(world.parent_env), MockServer(secrets=[key]) as server:
        runner = Runner(stage2, wrapper, hardening, runner_calls)
        catalog_fixture(server)
        state_guard = state_store_guard(world)
        catalog_note = None
        try:
            if real:
                selection, denials = collect_catalog(runner, server, hardening)
                guard_lines += denials
            else:
                selection = synthetic_selection(stage2.PI_VERSION)
                catalog_note = "synthetic selection: the catalog helper needs the pinned Pi (stand-in mode)"
        except Exception as error:  # noqa: BLE001 - recorded; the run then has no dynamic free selection
            selection = synthetic_selection(stage2.PI_VERSION)
            selection["error"] = f"{type(error).__name__}: {error}"
            catalog_note = f"catalog collection failed: {selection['error']}"
        free = list(selection.get("selected") or [])[:2]
        if len(free) < 2 and not real:
            free = list(FREE_MODELS)
        seats = [
            {"label": "online", "role": "online", "model": ONLINE_MODEL, "tools": "public", "kind": "public"},
            *(
                {
                    "label": f"online-free-{i + 1}",
                    "role": "online_free",
                    "model": m,
                    "tools": "public",
                    "kind": "public",
                }
                for i, m in enumerate(free)
            ),
            {
                "label": "repository",
                "role": "repository",
                "model": REPOSITORY_MODEL,
                "tools": "repository",
                "kind": "repository",
            },
        ]
        labels = {seat["model"]: seat["label"] for seat in seats}
        labels[PROBE_MODEL] = "probe"
        store = store_for_run(selection, labels)
        for seat in seats:
            server.script(
                seat["label"],
                repository_script(world) if seat["kind"] == "repository" else public_script(server.port, world.home),
            )
        server.script("probe", [{"content": "OK"}])

        run = Run.__new__(Run)
        run.root, run.change, run.runner, run.key = world.repo, FIXTURE_CHANGE, runner, key
        run.selection = {"catalog": {"models_store": store}}
        run.entries = {}
        results = []
        for number, seat in enumerate(seats, start=1):
            template = "repository.md" if seat["kind"] == "repository" else "public.md"
            prompt = render_prompt(template, "a synthetic public subject")
            entry = run.entry(
                "topics",
                seat["role"],
                number,
                {"endpoint": GO, "model": seat["model"]},
                prompt,
                topic=1,
                tools=seat["tools"],
            )
            seat_dir = scratch / "seats" / seat["label"]
            seat_dir.mkdir(parents=True)
            command, cwd, env = run.pi_command(entry, prompt, seat_dir)
            command, env = hardening(command, env)
            started = time.monotonic()
            try:
                done = subprocess.run(
                    command,
                    cwd=cwd,
                    env=env,
                    stdin=subprocess.DEVNULL,
                    capture_output=True,
                    text=True,
                    errors="replace",
                    timeout=args.timeout,
                    check=False,
                )
                code, out, err = done.returncode, done.stdout, done.stderr
            except subprocess.TimeoutExpired as error:
                code, out, err = None, "", f"timed out after {args.timeout}s: {error}"
            receipts = seat_dir / "research" / "receipts.jsonl"
            results.append(
                {
                    **seat,
                    "argv": command,
                    "cwd": str(cwd),
                    "exit_code": code,
                    "stdout": out,
                    "stderr": err,
                    "seconds": round(time.monotonic() - started, 1),
                    "receipts_path": str(receipts) if seat["tools"] == "public" else None,
                    "receipts": [line for line in receipts.read_text(encoding="utf-8").split("\n") if line]
                    if receipts.is_file()
                    else [],
                }
            )
        probe_audit: list[str] = []
        original = stage2_availability._checked_probe
        stage2_availability._checked_probe = lambda *_args, **_kwargs: None
        probe_error = None
        try:
            stage2_availability.probe_go(
                runner,
                world.repo,
                FIXTURE_CHANGE,
                PROBE_MODEL,
                key,
                probe_audit,
                store,
                # The offline fixture grants no paid-model terms: the declaration
                # check is outside this capture, just like _checked_probe above.
                admission=lambda _root, _model: None,
            )
        except Exception as error:  # noqa: BLE001 - a failed probe is evidence, recorded
            probe_error = f"{type(error).__name__}: {error}"
        finally:
            stage2_availability._checked_probe = original
        records = [dict(r) for r in server.records]
    return {
        "world": world,
        "records": records,
        "results": results,
        "selection": selection,
        "catalog_note": catalog_note,
        "store_guard": state_guard,
        "probe_error": probe_error,
        "transport_routes": transport_routes,
        "probe_call": runner_calls[-1:] or None,
        "sandbox": sandbox,
        "guard_lines": guard_lines,
        "wrapper": wrapper,
        "seats": seats,
        "real": real,
        "stage2": stage2,
        "url_port": server.port,
    }


def method_lines(real: bool) -> list[str]:
    return [
        "Scratch world: a fake repository (canaries in tracked files, discovery traps under .pi/, git history and an untracked file), a fake HOME and a fake XDG_STATE_HOME outside it; fake API-key-shaped canaries replace the process environment for the run. No real file or secret is read.",
        "Mock server: loopback, random port, records every request body, tool schema and header (the transport key redacted); answers from a script that calls file, shell, search and private-address tools.",
        "Launch paths: the online, online-free and repository seats are built by the swarm's own Run.pi_command (production argv, scratch HOME and agent directory, restricted environment, measured models.json written by activate_overlay) and the reachability probe by stage2_availability.probe_go; both start "
        + (
            "the pinned Pi through stage2.PI_WRAPPER."
            if real
            else "the STAND-IN Pi (dry run): this is a test of the tool, not of Pi."
        ),
        "Models store: "
        + (
            "the real pinned-Pi catalog helper and the real select_research_catalog read the mock catalog; only the installed transport configuration is then re-pointed at the seat routes of the mock."
            if real
            else "synthetic (stand-in mode); the catalog helper needs the pinned Pi."
        ),
        "Go address record: the fake repository declares the capture's own record (stage2_go's shape), so the seat launches resolve their offline defaults against it and never against the working tree's held file; the probe assesses the same refreshed definition it installs, and dispatch re-checks it against the fixture record. Only the capture transport seam rewrites the installed base to loopback after admission; transport_routes records the original and mock destinations. No loopback URL passes a production address check.",
        "Skipped on purpose: the dispatcher's declaration check and exact-prompt leak check (covered by their own tests; the probe's _checked_probe is stubbed because the fake repository has no declaration).",
        "Verdicts: criterion 8 = no canary or credential in any outbound request of a free context or catalog read; 9 = only the two public tools declared, undeclared and private-address attempts refused, nothing reached the sink; 47 = the probe payload carries no canary and no tool. Missing evidence is FAIL. A tool attempt counts as refused when its result text reads as an error (a heuristic; the excerpts are in the report for a human read).",
    ]


def enforcement(real: bool, sandbox: bool) -> dict:
    enforced = [
        "The mock server binds 127.0.0.1 only; every model route and both catalog sources point at it.",
        "Each seat runs with the production scratch HOME, scratch agent directory and restricted environment (public seats: PATH only plus their own variables).",
        "The parent environment, HOME and XDG_STATE_HOME are replaced by synthetic canary values for the whole run.",
        "Proxy variables of every child point at a dead loopback port.",
    ]
    not_enforced = [
        "No kernel-level or firewall block of the network: that needs root or a sandbox, neither is used by default.",
        "Name resolution is not blocked: a Node lookup before a denied connect, or any native resolver call, may reach a resolver.",
        "A native subprocess a tool might start (curl, ssh, git) is outside the Node guard.",
        "Other processes on this machine are not controlled; the maintainer watches the run.",
    ]
    if real:
        enforced.append(
            "Every Node process of Pi and the catalog helper preloads tests/pi_network_guard.mjs, which denies fetch/http/https/net/tls to any non-loopback host before the connection is made (its denials are proven by tests/pi_contract_driver.mjs)."
        )
    else:
        not_enforced.insert(
            0,
            "Stand-in mode: the Node guard is not loaded (the stand-in is Python); nothing but the stand-in talks to the mock, and the stand-in contacts no other address by construction.",
        )
    if sandbox:
        enforced.append(
            "macOS sandbox-exec denies outbound network except localhost around every command (NOT self-tested: a self-test would need an external attempt)."
        )
    else:
        not_enforced.append("The optional --os-sandbox (macOS sandbox-exec) is off.")
    return {"enforced": enforced, "not_enforced": not_enforced}


def build_report(data: dict) -> dict:
    world: World = data["world"]
    records = data["records"]
    seat_kinds = {seat["label"]: seat["kind"] for seat in data["seats"]}
    seat_kinds["probe"] = "probe"
    checks = evaluate(records, world.canaries, seat_kinds)
    checks.append(
        _check(
            "state-store-guard",
            "Runner placement guard on the fake state store (Q-15)",
            [f"{k}: {v}" for k, v in data["store_guard"].items()],
            not (
                data["store_guard"].get("outside-home") == "accepted"
                and data["store_guard"].get("inside-home", "").startswith("refused")
            ),
        )
    )
    if data["real"]:
        selection = data["selection"]
        reasons = [f"selected free ids: {selection.get('selected')}", f"outcome: {selection.get('selection_outcome')}"]
        broken = bool(selection.get("error") or selection.get("synthetic") or len(selection.get("selected") or []) < 2)
        if selection.get("error"):
            reasons.append(f"the catalog helper or selection failed: {selection['error']}")
        checks.append(_check("catalog", "Dynamic Go free selection from the mock catalog", reasons, broken))
    hits = canary_hits(records, world.canaries)
    seats_out = []
    labels = [seat["label"] for seat in data["seats"]] + ["probe"]
    by_label = {r["label"]: r for r in data["results"]}
    for label in labels:
        mine = [r for r in records if r.get("kind") == "model" and r.get("seat") == label]
        result = by_label.get(label, {})
        schemas = tool_schemas(mine[0].get("body")) if mine else []
        denials = [
            line
            for line in (
                result.get("stderr", "") + "\n" + "\n".join(a["result_excerpt"] for a in tool_attempts(mine))
            ).splitlines()
            if "pi-network-guard" in line
        ]
        seats_out.append(
            {
                "label": label,
                "kind": seat_kinds[label],
                "model": result.get("model", PROBE_MODEL if label == "probe" else None),
                "argv": result.get("argv")
                or (data["probe_call"][0]["argv"] if label == "probe" and data["probe_call"] else None),
                "cwd": result.get("cwd"),
                "exit_code": result.get(
                    "exit_code",
                    data["probe_call"][0]["returncode"] if label == "probe" and data["probe_call"] else None,
                ),
                "stdout_excerpt": excerpt(result.get("stdout", "")),
                "stderr_excerpt": excerpt(result.get("stderr", "")),
                "tool_schemas": schemas,
                "tool_attempts": tool_attempts(mine),
                "requests": mine,
                "guard_denials": denials,
                "receipts": {
                    "path": result.get("receipts_path"),
                    "count": len(result.get("receipts") or []),
                    "lines": (result.get("receipts") or [])[:20],
                },
                "system_prompt_excerpt": excerpt(
                    next(
                        (
                            m.get("content") if isinstance(m.get("content"), str) else _flat(m.get("content"))
                            for m in (mine[0]["body"].get("messages") or [])
                            if m.get("role") in ("system", "developer")
                        ),
                        "",
                    ),
                    800,
                )
                if mine
                else "",
            }
        )
    verdict = "FAIL" if any(c["verdict"] == "FAIL" for c in checks) else "PASS"
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "mode": "real-pi" if data["real"] else "stand-in",
        "commit": commit_of(),
        "pi": pi_facts(data["stage2"], data["wrapper"], full=data["real"]),
        "method": method_lines(data["real"]),
        "enforcement": enforcement(data["real"], data["sandbox"]),
        "canaries": world.canaries,
        "canary_hits": hits,
        "catalog": {
            "note": data["catalog_note"],
            "synthetic": bool(data["selection"].get("synthetic")),
            "selection_outcome": data["selection"].get("selection_outcome"),
            "selected_free": data["selection"].get("selected"),
            "pi_version": data["selection"].get("pi_version"),
            "error": data["selection"].get("error"),
            "requests": [r for r in records if r.get("kind") == "catalog"],
            "guard_denials": data["guard_lines"],
        },
        "probe": {"error": data["probe_error"], "call": data["probe_call"]},
        "transport_routes": data["transport_routes"],
        "sink_requests": [r for r in records if r.get("kind") == "sink"],
        "seats": seats_out,
        "checks": checks,
        "verdict": verdict,
    }


def render_markdown(report: dict) -> str:
    lines = [
        f"# F-1 offline capture - {report['verdict']}",
        "",
        f"- Mode: `{report['mode']}`"
        + (" (a test of the tool, NOT the F-1 evidence)" if report["mode"] != "real-pi" else ""),
        f"- Generated: {report['generated_at']}",
        f"- Commit: `{report['commit']['sha']}` on `{report['commit']['branch']}`"
        + (" (working tree dirty)" if report["commit"]["dirty"] else ""),
        f"- Pi pin: `{report['pi']['pin']}`; installed: `{report['pi'].get('installed_version')}`; lock: `{report['pi'].get('lock_entry')}`",
        f"- Pi pin manifest sha256: `{report['pi'].get('pin_manifest_sha256')}`; wrapper sha256: `{report['pi'].get('wrapper_sha256')}`",
        "",
        "## Verdicts",
        "",
    ]
    for check in report["checks"]:
        name = f"Criterion {check['criterion']}" if check["criterion"].isdigit() else check["criterion"]
        lines.append(f"- {name} - {check['title']}: **{check['verdict']}**")
        lines += [f"  - {reason}" for reason in check["reasons"]]
    lines += ["", "## Method", ""] + [f"- {item}" for item in report["method"]]
    lines += ["", "## Network: enforced and not enforced", "", "Enforced:", ""] + [
        f"- {i}" for i in report["enforcement"]["enforced"]
    ]
    lines += ["", "Not enforced:", ""] + [f"- {i}" for i in report["enforcement"]["not_enforced"]]
    lines += ["", "## Source hashes", "", "```json", json.dumps(report["pi"].get("source_hashes"), indent=2), "```"]
    lines += ["", "## Canaries", "", "| name | class | where | value | appeared in |", "|---|---|---|---|---|"]
    for canary in report["canaries"]:
        seen = report["canary_hits"].get(canary["name"]) or []
        where = "; ".join(sorted({f"{h['seat']}#{h['index']} {h['where']}" for h in seen})) or "nowhere"
        lines.append(f"| {canary['name']} | {canary['class']} | {canary['where']} | `{canary['value']}` | {where} |")
    lines += ["", "## Seats"]
    for seat in report["seats"]:
        lines += [
            "",
            f"### {seat['label']} ({seat['kind']}, model `{seat['model']}`)",
            "",
            f"- Exit code: {seat['exit_code']}; model requests recorded: {len(seat['requests'])}",
            f"- Declared tools: {[t['name'] for t in seat['tool_schemas']] or 'none'}",
            f"- Receipts: {seat['receipts']['count']} line(s)",
            f"- Guard denials seen: {len(seat['guard_denials'])}",
        ]
        if seat["argv"]:
            lines.append(f"- argv: `{' '.join(seat['argv'])}`")
        if seat["system_prompt_excerpt"]:
            lines += ["", "System prompt excerpt:", "", "```", seat["system_prompt_excerpt"], "```"]
        if seat["tool_schemas"]:
            lines += ["", "Tool schemas:", "", "```json", json.dumps(seat["tool_schemas"], indent=2)[:3000], "```"]
        if seat["tool_attempts"]:
            lines += ["", "| tool attempt | arguments | outcome | result excerpt |", "|---|---|---|---|"]
            for attempt in seat["tool_attempts"]:
                lines.append(
                    f"| {attempt['name']} | `{json.dumps(attempt['arguments'])[:120]}` | {attempt['outcome']} | {attempt['result_excerpt'][:120]!r} |"
                )
        for line in seat["receipts"]["lines"][:5]:
            lines.append(f"- receipt: `{line[:200]}`")
    lines += [
        "",
        "## Catalog metadata isolation",
        "",
        f"- {report['catalog']['note'] or 'real catalog helper and real selection ran against the mock'}",
        f"- Selected free ids: {report['catalog']['selected_free']}; requests recorded: {len(report['catalog']['requests'])}",
    ]
    lines += ["", "## Reachability probe", "", f"- Error: {report['probe']['error'] or 'none'}"]
    lines += ["", "Full outbound payloads are in the JSON report (`seats[].requests[].body`).", ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument(
        "--scratch", required=True, help="scratch directory for the world, seat directories and the stand-in"
    )
    parser.add_argument(
        "--out", help="report path prefix: writes <out>.json and <out>.md (default <scratch>/capture-report)"
    )
    parser.add_argument(
        "--attended", action="store_true", help="the maintainer is present: required to start the real pinned Pi"
    )
    parser.add_argument("--dry-run-stand-in", action="store_true", help="use a stand-in Pi; tests the tool, not Pi")
    parser.add_argument(
        "--stand-in-leak", action="store_true", help="test only: the stand-in leaks an environment canary"
    )
    parser.add_argument(
        "--os-sandbox",
        action="store_true",
        help="macOS only: wrap every command in sandbox-exec denying non-loopback network",
    )
    parser.add_argument("--seed", help="deterministic canaries (tests); default random")
    parser.add_argument("--timeout", type=int, default=300, help="seconds per seat process")
    args = parser.parse_args(argv)
    if not args.dry_run_stand_in and not args.attended:
        print(
            "research_capture: the real pinned Pi starts only with --attended (the maintainer is present, F-1); "
            "use --dry-run-stand-in to test the tool.",
            file=sys.stderr,
        )
        return 2
    scratch = Path(args.scratch)
    if scratch.exists() and any(scratch.iterdir()):
        print(f"research_capture: {scratch} is not empty; give a fresh scratch directory.", file=sys.stderr)
        return 2
    scratch.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(SCRIPT_DIR))
    out = Path(args.out) if args.out else scratch / "capture-report"
    try:
        data = execute(args, scratch)
        report = build_report(data)
    except Exception as error:  # noqa: BLE001 - an unusable run is exit 2, never a PASS
        print(f"research_capture: the capture could not run: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    out.parent.mkdir(parents=True, exist_ok=True)
    Path(f"{out}.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    Path(f"{out}.md").write_text(render_markdown(report), encoding="utf-8")
    print(f"research_capture: {report['verdict']} ({report['mode']}); report {out}.json and {out}.md")
    for check in report["checks"]:
        print(f"  {check['criterion']}: {check['verdict']}")
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
