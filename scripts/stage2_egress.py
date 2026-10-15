#!/usr/bin/env python3
"""stage2_egress.py - the trusted proxy that confines a writer's network (ADR 0018).

**What this is.** The only network path an isolated writing attempt has. The
proxy runs in its own container attached to the attempt's private network and
the outbound network; the writer is attached to the private network alone, so
every connection must arrive here as an HTTP `CONNECT` for one exact declared
API host on port 443. Everything else is refused and closed.

**What this is not.** It is not a name filter the writer could bypass: the
model container sits on an internal network with no outbound route, no
published ports, no host networking and no direct DNS - the proxy environment
variables are a convenience for the CLI, never the enforcement. The
admission gate is a pure function (`connect_target_allowed`), so the suite
can hold every refusal without any network at all.

Usage (the supervisor starts it detached):

    python3 scripts/stage2_egress.py serve --hosts api.z.ai --bind 0.0.0.0 --port 8080
"""

from __future__ import annotations

import argparse
import ipaddress
import socket
import sys
import threading
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from stage2_attempt import api_profile_problems  # noqa: E402

ONLY_HTTPS_PORT = 443


def _is_address(text: str) -> bool:
    try:
        ipaddress.ip_address(text)
    except ValueError:
        return False
    return True


def connect_target_allowed(host: str, port: int, api_hosts: list[str]) -> tuple[bool, str]:
    """The one admission gate: an exact declared API host on the HTTPS port, nothing else.

    A wildcard, an address literal, a port suffix, an undeclared or local
    name, and any port but 443 are refused with the reason; the refusal is the
    product, not the allowance.
    """
    if port != ONLY_HTTPS_PORT:
        return False, f"only port {ONLY_HTTPS_PORT} is proxied, not {port}"
    if not api_hosts:
        return False, "no API host is declared for this attempt"
    problems = api_profile_problems([host])
    if problems:
        return False, f"the CONNECT target is not a canonical declared name: {problems[0]}"
    if _is_address(host):
        return False, f"the CONNECT target {host} is an address literal"
    if host not in api_hosts:
        return False, f"the CONNECT target {host} is not a declared API host"
    return True, ""


def address_is_permitted(ip_text: str) -> bool:
    """Whether a resolved address may be dialled: only globally routable ones."""
    try:
        address = ipaddress.ip_address(ip_text)
    except ValueError:
        return False
    return address.is_global


def resolve_permitted(host: str) -> list[str]:
    """The host's addresses that may be dialled; an empty list refuses the CONNECT."""
    try:
        infos = socket.getaddrinfo(host, ONLY_HTTPS_PORT, proto=socket.IPPROTO_TCP)
    except OSError:
        return []
    permitted = []
    for info in infos:
        address = str(info[4][0])
        if address_is_permitted(address) and address not in permitted:
            permitted.append(address)
    return permitted


def _read_line(sock: socket.socket) -> bytes:
    buffer = bytearray()
    while len(buffer) < 8192:
        one = sock.recv(1)
        if not one:
            break
        buffer += one
        if buffer.endswith(b"\r\n") or buffer.endswith(b"\n"):
            break
    return bytes(buffer)


def serve_connection(stream: socket.socket, api_hosts: list[str], dial) -> bool:
    """Handle one proxied connection; return True when it was allowed.

    `dial(address, port)` opens the upstream socket; the handshake reads the
    request line and headers, refuses anything but an admitted CONNECT, and
    otherwise relays both directions until either side closes. No content is
    logged and no TLS is terminated: the proxy enforces the name, then pipes.
    """
    request_line = _read_line(stream)
    if not request_line:
        return False
    while True:
        line = _read_line(stream)
        if not line or line in (b"\r\n", b"\n"):
            break
    parts = request_line.decode(errors="replace").split()
    if len(parts) != 3 or parts[0].upper() != "CONNECT":
        stream.sendall(b"HTTP/1.1 403 Forbidden\r\n\r\n")
        return False
    target, _, port_text = parts[1].rpartition(":")
    try:
        port = int(port_text)
    except ValueError:
        stream.sendall(b"HTTP/1.1 403 Forbidden\r\n\r\n")
        return False
    allowed, _reason = connect_target_allowed(target, port, api_hosts)
    if not allowed or not target:
        stream.sendall(b"HTTP/1.1 403 Forbidden\r\n\r\n")
        return False
    upstream = None
    for address in resolve_permitted(target):
        try:
            upstream = dial(address, port)
            break
        except OSError:
            continue
    if upstream is None:
        stream.sendall(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
        return False
    try:
        stream.sendall(b"HTTP/1.1 200 Connection established\r\n\r\n")
        _relay(stream, upstream)
    finally:
        try:
            upstream.close()
        except OSError:
            pass
    return True


def _relay(one: socket.socket, two: socket.socket) -> None:
    """Move bytes both ways until either side closes."""

    def pump(source: socket.socket, sink: socket.socket) -> None:
        try:
            while True:
                chunk = source.recv(65536)
                if not chunk:
                    break
                sink.sendall(chunk)
        except OSError:
            pass
        finally:
            try:
                sink.shutdown(socket.SHUT_WR)
            except OSError:
                pass

    threads = [threading.Thread(target=pump, args=(one, two)), threading.Thread(target=pump, args=(two, one))]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def serve(bind: str, port: int, api_hosts: list[str]) -> int:
    """Accept connections until stopped; every refusal is closed, none is logged with content."""
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((bind, port))
    listener.listen(16)
    while True:
        connection, _ = listener.accept()
        thread = threading.Thread(target=_serve_one, args=(connection, api_hosts), daemon=True)
        thread.start()


def _serve_one(connection: socket.socket, api_hosts: list[str]) -> None:
    try:
        serve_connection(connection, api_hosts, socket.create_connection)
    except OSError:
        pass
    finally:
        try:
            connection.close()
        except OSError:
            pass


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("command", choices=["serve"])
    parser.add_argument("--hosts", required=True, help="comma-separated exact API host names")
    parser.add_argument("--bind", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args(argv)
    api_hosts = [host for host in args.hosts.split(",") if host]
    problems = api_profile_problems(api_hosts)
    if problems:
        print(f"the egress policy refuses its own profile: {problems[0]}", file=sys.stderr)
        return 2
    serve(args.bind, args.port, api_hosts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
