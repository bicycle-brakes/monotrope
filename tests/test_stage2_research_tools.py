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
NEXT_IP = "8.8.4.4"  # a public address for the scripted redirect hop
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
        ("::ffff:808:808", False),
        ("0:0:0:0:0:ffff:808:808", False),
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
    [
        "192.0.0.1",
        "192.0.2.1",
        "192.88.99.1",
        "198.18.0.1",
        "198.19.255.255",
        "198.51.100.1",
        "203.0.113.1",
        "224.0.0.1",
        "239.255.255.255",
        "240.0.0.1",
        "ff02::1",
        "2001:db8::1",
        "3fff::1",
        "2002:c000:0201::1",
        "100::1",
        "::ffff:c000:201",
        "::ffff:192.0.2.1",
        "0:0:0:0:0:ffff:e000:1",
    ],
)
def test_non_global_lookup_addresses_never_reach_the_transport(world: World, ip: str) -> None:
    for lookups in ([[ip]], [[PUBLIC_IP, ip]], [[PUBLIC_IP], [ip]]):
        answer = world.call(
            mode="fetch",
            url="https://example.com/x",
            transport={
                "lookups": lookups,
                "responses": ([{"status": 302, "location": "https://next.example/x"}] if len(lookups) == 2 else [])
                + [{"status": 200, "body": "must not be read"}],
            },
        )
        thrown(answer, mentioning="private address")
        assert len(answer["seen"]["gets"]) == len(lookups) - 1, answer


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


@pytest.mark.parametrize("all_addresses", [False, True])
@pytest.mark.parametrize("ipv6_first", [False, True])
def test_node_transport_pins_the_resolved_ipv6_family(world: World, all_addresses: bool, ipv6_first: bool) -> None:
    # L1-8: an IPv6-only or IPv6-first DNS result reaches the real HTTPS lookup callback.
    address = "2001:4860:4860::8888"
    lookups = [{"address": address, "family": 6}]
    if ipv6_first:
        lookups.append({"address": PUBLIC_IP, "family": 4})
    answer = world.call(
        mode="node-fetch",
        url="https://example.com/ipv6",
        all=all_addresses,
        transport={"lookups": [lookups], "responses": [{"status": 200, "body": "IPv6 page"}]},
    )
    assert "threw" not in answer, answer
    pinned = answer["seen"]["pinned"]
    assert pinned == ([{"address": lookups[:1]}] if all_addresses else [{"address": address, "family": 6}])
    assert answer["receipt"]["status"] == 200


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


# A DuckDuckGo HTML answer as the endpoint serves it: every result anchor is a
# redirect wrapper whose `uddg` parameter carries the destination (F-10).
WRAPPED = (
    '<a rel="nofollow" class="result__a" '
    'href="//duckduckgo.com/l/?uddg=https%3A%2F%2Fa.example%2Fguide%3Fpart%3D2&amp;rut=abc123">A guide</a>'
    '<a class="result__snippet" href="//duckduckgo.com/l/?uddg=https%3A%2F%2Fa.example%2Fguide">Snippet</a>'
    '<a rel="nofollow" class="result__a" '
    'href="//duckduckgo.com/l/?uddg=http%3A%2F%2Fplain.example%2F&amp;rut=def">Plain http</a>'
    '<a rel="nofollow" class="result__a" href="https://duckduckgo.com/y.js?ad_domain=ads.example">Advert</a>'
)


def test_search_results_carry_the_decoded_destination(world: World) -> None:
    # F-10. Planted fault: a result keeps the wrapper URL, so its receipt and its citation never meet.
    answer = world.call(mode="parse", html=WRAPPED)
    assert answer["results"] == [{"title": "A guide", "url": "https://a.example/guide?part=2", "snippet": "Snippet"}], (
        "the wrapper is decoded; a non-https destination and an advert without one are dropped"
    )
    fetched = world.call(
        mode="fetch",
        url=answer["results"][0]["url"],
        transport={"lookups": [[PUBLIC_IP]], "responses": [{"status": 200, "body": "<title>Guide</title>"}]},
    )
    assert fetched["receipt"]["url"] == "https://a.example/guide?part=2", "the decoded destination is fetchable"


def test_the_tool_parameters_are_json_schemas(world: World) -> None:
    # F-2(a). Planted fault: a `{query: "string"}` map that no JSON-schema validator accepts as a schema.
    schemas = world.call(mode="load")["schemas"]
    for tool, field in (("public_search", "query"), ("public_fetch", "url")):
        schema = schemas[tool]
        assert schema["type"] == "object" and schema["required"] == [field], schema
        assert schema["properties"][field]["type"] == "string", schema
        assert schema["additionalProperties"] is False, schema


def test_the_tools_run_as_pi_calls_them(world: World) -> None:
    # F-2(a). Planted fault: `execute({ query })` destructures Pi's tool-call id, or a bare string is returned.
    search, fetch = world.run(
        [
            {
                "mode": "pi-execute",
                "tool": "public_search",
                "params": {"query": "public practice"},
                "transport": {"lookups": [[PUBLIC_IP]], "responses": [{"status": 200, "body": WRAPPED}]},
            },
            {
                "mode": "pi-execute",
                "tool": "public_fetch",
                "params": {"url": "https://a.example/guide"},
                "transport": {
                    "lookups": [[PUBLIC_IP]],
                    "responses": [{"status": 200, "body": "<html><title>Guide</title>text</html>"}],
                },
            },
        ]
    )
    for answer in (search, fetch):
        assert "threw" not in answer, answer
        content = answer["result"]["content"]
        assert [part["type"] for part in content] == ["text"], answer["result"]
    assert "q=public%20practice" in search["seen"]["gets"][0]["url"], "the query from the params reaches the search"
    assert json.loads(search["result"]["content"][0]["text"])[0]["url"] == "https://a.example/guide?part=2"
    assert search["receipts"][0]["kind"] == "search"
    receipt = json.loads(fetch["result"]["content"][0]["text"])
    assert receipt["url"] == "https://a.example/guide" and receipt["title"] == "Guide"
    assert fetch["receipts"] == [receipt], "the tool step under Pi writes its receipt"


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
