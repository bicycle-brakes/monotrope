"""The swarm's public research tools, tested without Pi and without network.

`scripts/stage2_research_tools.mjs` is the ONLY extension a free researcher's
Pi context loads (plans/changes/research-swarm/design.md). A node driver
(`stage2_research_tools_driver.mjs`) loads a copy of it and exercises its
destination checks, address classification, redirect handling and tool gate
over a scripted transport: local file schemes, embedded credentials, odd
ports, private, loopback and link-local addresses — reached directly, through
a redirect, or through a rebinding second lookup.

Each refusal rule has a case that goes red when the rule is removed. The
suite skips when `node` is not installed.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
EXTENSION = HERE.parent / "scripts" / "stage2_research_tools.mjs"
DRIVER = HERE / "stage2_research_tools_driver.mjs"

pytestmark = pytest.mark.skipif(
    shutil.which("node") is None, reason="node is not installed; the extension is JavaScript"
)

PUBLIC_IP = "93.184.216.34"  # a public address for the scripted lookups
NEXT_IP = "203.0.113.5"  # public (TEST-NET-3) for the redirect hop
PRIVATE_IP = "10.9.9.9"

OTHER_TOOLS = ("read", "write", "edit", "bash", "grep", "find", "ls", "webfetch", "mystery-tool")


@dataclass
class World:
    home: Path  # $HOME for the node run
    copy: Path  # the copy of the extension that is loaded, in a generic scratch path

    def run(self, cases: list[dict]) -> list[dict]:
        request = {"module": str(self.copy), "cases": cases}
        done = subprocess.run(
            ["node", str(DRIVER)],
            input=json.dumps(request),
            capture_output=True,
            text=True,
            timeout=60,
            env={**os.environ, "HOME": str(self.home)},
            check=False,
        )
        assert done.returncode == 0, done.stderr
        return json.loads(done.stdout)

    def call(self, **fields: object) -> dict:
        return self.run([dict(fields)])[0]


@pytest.fixture
def world(tmp_path: Path) -> World:
    # The runner copies the extension to a generic scratch path before loading;
    # the tests load a copy for the same reason — no repository path in play.
    copy = tmp_path / "scratch" / "research-tools.mjs"
    copy.parent.mkdir(parents=True)
    shutil.copy(EXTENSION, copy)
    return World(tmp_path / "home", copy)


def thrown(answer: dict, *, mentioning: str) -> None:
    assert "threw" in answer, answer
    assert mentioning in answer["threw"], answer["threw"]


# --- the extension as Pi loads it -----------------------------------------------------------------


def test_the_extension_registers_two_tools_and_one_gate(world: World) -> None:
    answer = world.call(mode="load")
    assert answer["tools"] == ["public_search", "public_fetch"], answer
    assert answer["handlers"] == ["tool_call"], answer


def test_the_extension_refuses_a_host_without_register_tool(world: World) -> None:
    answer = world.call(mode="load-without-host")
    thrown(answer, mentioning="registerTool")


def test_only_the_public_tools_pass_the_gate(world: World) -> None:
    assert world.call(mode="handler", toolName="public_search")["result"] is None
    assert world.call(mode="handler", toolName="public_fetch")["result"] is None
    for tool in OTHER_TOOLS:
        answer = world.call(mode="handler", toolName=tool)
        result = answer["result"]
        assert result is not None and result["block"] is True, (tool, answer)
        assert "does not exist in a free researcher context" in result["reason"], result


# --- destinations ---------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("url", "reason"),
    [
        ("file:///etc/passwd", "only https://"),
        ("http://example.com/x", "only https://"),
        ("https://user:" + "pass" + "@example.com/x", "embedded credentials"),
        ("https://example.com:8443/x", "port 443"),
        ("https://localhost/x", "local host names"),
        ("https://host.local/x", "local host names"),
        ("not a url", "not a valid URL"),
        ("", "required"),
    ],
)
def test_a_local_or_authenticated_destination_is_refused(world: World, url: str, reason: str) -> None:
    thrown(world.call(mode="validate", url=url), mentioning=reason)


# --- addresses ------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("ip", "private"),
    [
        (PRIVATE_IP, True),
        ("192.168.1.7", True),
        ("172.16.0.9", True),
        ("172.32.0.9", False),
        ("100.64.0.1", True),
        ("100.128.0.1", False),
        ("169.254.3.4", True),
        ("0.1.2.3", True),
        ("127.0.0.1", True),
        ("8.8.8.8", False),
        ("::1", True),
        ("::", True),
        ("fe80::1", True),
        ("fd00::1", True),
        ("::ffff:127.0.0.1", True),
        ("::ffff:8.8.8.8", False),
        ("2001:4860:4860::8888", False),
    ],
)
def test_the_address_classification(world: World, ip: str, private: bool) -> None:
    assert world.call(mode="private-ip", ip=ip)["private"] is private, ip


def test_a_lookup_that_returns_a_private_address_is_refused(world: World) -> None:
    answer = world.call(
        mode="fetch",
        url="https://example.com/x",
        transport={"lookups": [[PRIVATE_IP]], "responses": [{"status": 200, "body": "hi"}]},
    )
    thrown(answer, mentioning="private address")


@pytest.mark.parametrize(
    "ip",
    ["127.0.0.1", "::1", "fe80::1", "fd12::34", "::ffff:192.168.0.9", "169.254.1.2", "100.100.100.100"],
)
def test_no_private_shape_reaches_a_fetch(world: World, ip: str) -> None:
    answer = world.call(
        mode="fetch",
        url="https://example.com/x",
        transport={"lookups": [[ip]], "responses": [{"status": 200, "body": "hi"}]},
    )
    thrown(answer, mentioning="private address")


def test_public_tools_cannot_read_local_or_private_sources(world: World) -> None:
    """Criterion 9's ledger row: the isolation in one sweep.

    The gate blocks a local-file or shell tool, a fetch refuses every private
    shape, and a redirect cannot smuggle a private address in through its own
    fresh lookup. Each rule's dedicated counterpart stands above; this row's
    named proof binds them to the ledger.
    """
    answers = world.run(
        [{"mode": "handler", "toolName": "read"}, {"mode": "handler", "toolName": "bash"}]
        + [
            {
                "mode": "fetch",
                "url": "https://example.com/x",
                "transport": {"lookups": [[ip]], "responses": [{"status": 200, "body": "hi"}]},
            }
            for ip in ("127.0.0.1", "::1", "fe80::1", "fd12::34", "::ffff:192.168.0.9")
        ]
        + [
            {
                "mode": "fetch",
                "url": "https://example.com/start",
                "transport": {
                    "lookups": [[PUBLIC_IP], [PRIVATE_IP]],
                    "responses": [
                        {"status": 302, "location": "https://elsewhere.example/next", "body": ""},
                        {"status": 200, "body": "secret"},
                    ],
                },
            }
        ]
    )
    for answer in answers[:2]:
        assert answer["result"]["block"] is True and "does not exist" in answer["result"]["reason"], answer
    for answer in answers[2:]:
        thrown(answer, mentioning="private address")


def test_an_empty_lookup_is_refused(world: World) -> None:
    answer = world.call(
        mode="fetch",
        url="https://example.com/x",
        transport={"lookups": [[]], "responses": [{"status": 200, "body": "hi"}]},
    )
    thrown(answer, mentioning="no address")


# --- redirects ------------------------------------------------------------------------------------


def test_a_redirect_to_a_non_https_destination_is_refused(world: World) -> None:
    answer = world.call(
        mode="fetch",
        url="https://example.com/start",
        transport={
            "lookups": [[PUBLIC_IP]],
            "responses": [{"status": 302, "location": "http://example.com/next", "body": ""}],
        },
    )
    thrown(answer, mentioning="only https://")


def test_a_redirect_whose_fresh_lookup_turns_private_is_refused(world: World) -> None:
    """DNS rebinding: the first hop resolves public, the redirect's own lookup
    returns a private address — the per-hop revalidation must catch it."""
    answer = world.call(
        mode="fetch",
        url="https://example.com/start",
        transport={
            "lookups": [[PUBLIC_IP], [PRIVATE_IP]],
            "responses": [
                {"status": 302, "location": "https://elsewhere.example/next", "body": ""},
                {"status": 200, "body": "secret"},
            ],
        },
    )
    thrown(answer, mentioning="private address")
    assert answer["seen"]["lookups"][1]["hostname"] == "elsewhere.example"


# --- the happy paths ------------------------------------------------------------------------------


def test_a_public_fetch_pins_the_validated_address_and_records_a_receipt(world: World) -> None:
    answer = world.call(
        mode="fetch",
        url="https://example.com/x",
        transport={
            "lookups": [[PUBLIC_IP]],
            "responses": [{"status": 200, "body": "<html><title>Hi</title>hello page</html>"}],
        },
    )
    assert "threw" not in answer, answer
    receipt = answer["receipt"]
    assert receipt["kind"] == "fetch" and receipt["status"] == 200
    assert receipt["final_url"] == "https://example.com/x"
    assert receipt["title"] == "Hi"
    assert receipt["retrieved"] and receipt["bytes"] > 0
    assert answer["receipts"] == [receipt], "one receipt, written by the tool step"
    gets = answer["seen"]["gets"]
    assert len(gets) == 1 and gets[0]["pinnedIp"] == PUBLIC_IP, gets
    assert gets[0]["url"] == "https://example.com/x", "the host name stays the TLS name"


def test_a_redirect_is_followed_over_a_fresh_public_lookup(world: World) -> None:
    answer = world.call(
        mode="fetch",
        url="https://example.com/start",
        transport={
            "lookups": [[PUBLIC_IP], [NEXT_IP]],
            "responses": [
                {"status": 301, "location": "https://next.example/y", "body": ""},
                {"status": 200, "body": "arrived"},
            ],
        },
    )
    assert "threw" not in answer, answer
    assert answer["receipt"]["final_url"] == "https://next.example/y"
    assert [entry["hostname"] for entry in answer["seen"]["lookups"]] == ["example.com", "next.example"]
    assert answer["seen"]["gets"][1]["pinnedIp"] == NEXT_IP


def test_search_records_a_receipt_and_parses_results(world: World) -> None:
    html = (
        '<a class="result__a" href="https://a.example/x">A title</a>'
        '<a class="result__snippet" href="#">A snippet &amp; more</a>'
    )
    answer = world.call(
        mode="search",
        query="public practice",
        transport={"lookups": [[PUBLIC_IP]], "responses": [{"status": 200, "body": html}]},
    )
    assert "threw" not in answer, answer
    assert answer["results"][0]["title"] == "A title"
    assert answer["results"][0]["url"] == "https://a.example/x"
    assert "A snippet & more" in answer["results"][0]["snippet"]
    assert answer["receipts"][0]["kind"] == "search"


def test_the_parser_skips_pages_without_results(world: World) -> None:
    answer = world.call(mode="parse", html="<html><title>nothing</title></html>")
    assert answer["results"] == []


# --- the counterpart: a rule removed stops biting -------------------------------------------------


def test_the_private_range_table_bites(world: World) -> None:
    """Cut the private ranges out of a copy; the private lookup then passes.

    This is the test's counterpart: it plants the fault and shows the rule,
    not an accident of the driver, is what refuses the address.
    """
    source = EXTENSION.read_text(encoding="utf-8")
    cut = source.replace('  ["10.0.0.0", 8],\n', "").replace('  ["127.0.0.0", 8],\n', "")
    assert cut != source, "the private-range lines were not found — the extension changed"
    wounded = world.copy.parent / "wounded.mjs"
    wounded.write_text(cut, encoding="utf-8")
    request = {
        "module": str(wounded),
        "cases": [
            {
                "mode": "fetch",
                "url": "https://example.com/x",
                "transport": {"lookups": [[PRIVATE_IP]], "responses": [{"status": 200, "body": "hi"}]},
            }
        ],
    }
    done = subprocess.run(
        ["node", str(DRIVER)],
        input=json.dumps(request),
        capture_output=True,
        text=True,
        timeout=60,
        env={**os.environ, "HOME": str(world.home)},
        check=False,
    )
    assert done.returncode == 0, done.stderr
    answer = json.loads(done.stdout)[0]
    assert "threw" not in answer, answer
    assert answer["receipt"]["status"] == 200
