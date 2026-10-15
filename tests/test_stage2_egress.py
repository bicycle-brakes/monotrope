"""tests/test_stage2_egress.py — the trusted proxy's admission gate (ADR 0018).

The gate is pure, so every refusal is held without any network; one socket
test proves the wire behaviour end to end with a socket pair and a fake
upstream dial. The live probes of `scripts/check_stage2_isolation.py` measure
the production path through a real container.
"""

from __future__ import annotations

import socket
import sys
import threading
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import stage2_egress  # noqa: E402

DECLARED = ["api.z.ai", "opencode.ai"]


def test_proxy_refuses_host_and_tls_name_bypasses() -> None:
    """Wildcard, IP, local, mismatched or uninspectable names never pass the gate."""
    refusals = [
        ("*.z.ai", 443, "wildcard"),
        ("192.0.2.10", 443, "address"),
        ("api.z.ai:8443", 443, "wildcard"),
        ("127.0.0.1", 443, "address"),
        ("localhost", 443, "canonical"),
        ("telemetry.example.com", 443, "not a declared API host"),
        ("api.z.ai", 80, "only port 443"),
        ("api.z.ai", 8080, "only port 443"),
        ("", 443, "canonical"),
        ("api .z.ai", 443, "canonical"),
        ("API.Z.AI.", 443, "canonical"),
    ]
    for host, port, fragment in refusals:
        allowed, reason = stage2_egress.connect_target_allowed(host, port, DECLARED)
        assert not allowed, (host, port)
        assert fragment in reason, (host, port, reason)

    with_no_hosts = stage2_egress.connect_target_allowed("api.z.ai", 443, [])
    assert not with_no_hosts[0], "an empty profile approves nothing"

    allowed, reason = stage2_egress.connect_target_allowed("api.z.ai", 443, DECLARED)
    assert allowed and reason == ""
    allowed, _ = stage2_egress.connect_target_allowed("opencode.ai", 443, DECLARED)
    assert allowed


def test_only_globally_routable_addresses_may_be_dialled() -> None:
    """A resolved private, loopback or link-local address refuses the dial."""
    for address in ("127.0.0.1", "10.0.0.5", "192.168.1.1", "172.16.0.9", "::1", "fe80::1", "169.254.1.1"):
        assert not stage2_egress.address_is_permitted(address), address
    assert stage2_egress.address_is_permitted("203.0.113.10")


def test_the_wire_refuses_a_bypass_and_relays_the_declared_path(monkeypatch: pytest.MonkeyPatch) -> None:
    """On the socket: a forbidden CONNECT is answered 403 and closed; the declared one relays."""
    monkeypatch.setattr(stage2_egress, "resolve_permitted", lambda host: ["203.0.113.10"])
    client, server = socket.socketpair()
    dialled: list[tuple[str, int]] = []
    upstream_in, upstream_out = socket.socketpair()
    client.settimeout(5)

    def fake_dial(address: str, port: int) -> socket.socket:
        dialled.append((address, port))
        return upstream_out

    threading.Thread(target=stage2_egress.serve_connection, args=(server, DECLARED, fake_dial), daemon=True).start()
    client.sendall(b"CONNECT telemetry.example.com:443 HTTP/1.1\r\nHost: telemetry.example.com\r\n\r\n")
    answer = client.recv(1024)
    assert answer.startswith(b"HTTP/1.1 403")
    assert dialled == [], "a refused CONNECT never dials"

    client.close()
    server.close()
    upstream_in.close()
    upstream_out.close()

    client, server = socket.socketpair()
    upstream_in, upstream_out = socket.socketpair()
    dialled = []
    client.settimeout(5)
    threading.Thread(target=stage2_egress.serve_connection, args=(server, DECLARED, fake_dial), daemon=True).start()
    client.sendall(b"CONNECT api.z.ai:443 HTTP/1.1\r\n\r\n")
    answer = b""
    while b"\r\n\r\n" not in answer:
        answer += client.recv(1024)
    assert answer.startswith(b"HTTP/1.1 200"), answer
    assert dialled == [("203.0.113.10", 443)], dialled
    upstream_in.sendall(b"tls-bytes")
    assert client.recv(1024) == b"tls-bytes"
    client.sendall(b"client-bytes")
    assert upstream_out.recv(1024) == b"client-bytes"
    client.close()
    server.close()
    upstream_in.close()
    upstream_out.close()
